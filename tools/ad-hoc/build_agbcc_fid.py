#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_agbcc_fid.py  --  agbcc libc.a + libgcc.a 全量 FID 匹配

承接 fid_poc_divsi3.py POC (验证 agbcc 版本兼容): 提取所有 .o 全局 T 符号
+ relocation, 在 roms/2343.gba 做 byte-pattern + mask 搜索, 输出唯一匹配.

输入  refs/agbcc/libgcc.a  (~30 个 .o, gcc runtime)
       refs/agbcc/libc.a     (~247 个 .o, newlib)
       roms/2343.gba         (32 MB ROM)
输出  temp/agbcc-fid-matches.csv
       columns: address, sym_name, archive, object, size, n_relocs

仅记录 size >= MIN_SIZE 且匹配数 == 1 的项 (唯一性保证).

人工再决定是否 append 到 doc/dev/naming-proposals.csv (score=5).
"""

import csv
import os
import re
import subprocess
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ROM = os.path.join(REPO_ROOT, "roms", "2343.gba")
ARCHIVES = [
    ("libgcc", os.path.join(REPO_ROOT, "refs", "agbcc", "libgcc.a")),
    ("libc",   os.path.join(REPO_ROOT, "refs", "agbcc", "libc.a")),
]

DEVKIT_BIN = r"D:\devkitPro\devkitARM\arm-none-eabi\bin"
NM      = os.path.join(DEVKIT_BIN, "nm.exe")
OBJDUMP = os.path.join(DEVKIT_BIN, "objdump.exe")
OBJCOPY = os.path.join(DEVKIT_BIN, "objcopy.exe")
AR      = os.path.join(DEVKIT_BIN, "ar.exe")

MIN_SIZE = 16  # 函数体小于此字节数不参与匹配 (太短易碰)
WORK = os.path.join(REPO_ROOT, "temp", "agbcc-fid-extract")
OUT  = os.path.join(REPO_ROOT, "temp", "agbcc-fid-matches.csv")


def extract_archive(arch_path, dest_dir):
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)
    out = subprocess.check_output([AR, "t", arch_path]).decode(errors="replace")
    members = [m.strip() for m in out.splitlines() if m.strip().endswith(".o")]
    # ar x 一次抽完所有
    subprocess.check_call([AR, "x", arch_path], cwd=dest_dir,
                          stderr=subprocess.DEVNULL)
    return [os.path.join(dest_dir, m) for m in members]


def get_global_text_symbols(obj_path):
    try:
        out = subprocess.check_output([NM, "--print-size", obj_path],
                                       stderr=subprocess.DEVNULL).decode(errors="replace")
    except subprocess.CalledProcessError:
        return []
    syms = []
    for line in out.splitlines():
        parts = line.split()
        if len(parts) >= 4 and parts[2] == "T":
            try:
                syms.append((parts[3], int(parts[0], 16), int(parts[1], 16)))
            except ValueError:
                pass
    return syms


def get_text_relocs(obj_path):
    try:
        out = subprocess.check_output([OBJDUMP, "-r", obj_path],
                                       stderr=subprocess.DEVNULL).decode(errors="replace")
    except subprocess.CalledProcessError:
        return []
    relocs = []
    in_text = False
    for line in out.splitlines():
        if line.startswith("RELOCATION RECORDS FOR [.text]"):
            in_text = True
            continue
        if in_text and line.startswith("RELOCATION RECORDS FOR "):
            in_text = False
            continue
        if not in_text:
            continue
        m = re.match(r"^([0-9a-f]+)\s+(R_ARM_\w+)\s+(\S+)", line)
        if m:
            relocs.append((int(m.group(1), 16), m.group(2), m.group(3)))
    return relocs


def get_text_bytes(obj_path):
    tmp = obj_path + ".text.bin"
    try:
        subprocess.check_call([OBJCOPY, "-O", "binary", "-j", ".text", obj_path, tmp],
                              stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        return None
    if not os.path.isfile(tmp):
        return None
    with open(tmp, "rb") as f:
        data = f.read()
    os.remove(tmp)
    return data


def reloc_mask_bytes(rel_type, offset):
    return [offset + d for d in range(4)]


def find_anchor(pattern, mask):
    best_start, best_len = 0, 0
    cur_start, cur_len = 0, 0
    for i, m in enumerate(mask):
        if m:
            if cur_len == 0:
                cur_start = i
            cur_len += 1
            if cur_len > best_len:
                best_len = cur_len
                best_start = cur_start
        else:
            cur_len = 0
    return best_start, best_len


def search_rom(rom, pattern, mask):
    anchor_start, anchor_len = find_anchor(pattern, mask)
    if anchor_len < 4:
        return []
    anchor = bytes(pattern[anchor_start:anchor_start + anchor_len])

    matches = []
    pos = 0
    n = len(pattern)
    rom_n = len(rom)
    while True:
        idx = rom.find(anchor, pos)
        if idx < 0:
            break
        ms = idx - anchor_start
        if ms < 0 or ms + n > rom_n:
            pos = idx + 1
            continue
        ok = True
        for k in range(n):
            if mask[k] and rom[ms + k] != pattern[k]:
                ok = False
                break
        if ok:
            matches.append(ms)
        pos = idx + 1
    return matches


def process_obj(obj_path, archive_name, rom):
    """返回 list[(rom_offset, sym_name, archive, obj_basename, size, n_relocs)]."""
    text = get_text_bytes(obj_path)
    if text is None or len(text) == 0:
        return [], 0
    syms = get_global_text_symbols(obj_path)
    if not syms:
        return [], 0
    relocs = get_text_relocs(obj_path)
    obj_base = os.path.basename(obj_path)

    results = []
    skipped_short = 0
    for sym_name, sym_off, sym_size in syms:
        if sym_size < MIN_SIZE:
            skipped_short += 1
            continue
        if sym_off + sym_size > len(text):
            continue
        fn_bytes = text[sym_off:sym_off + sym_size]
        fn_relocs = [r for r in relocs if sym_off <= r[0] < sym_off + sym_size]
        pattern = list(fn_bytes)
        mask = [1] * len(pattern)
        for r_off, r_type, _ in fn_relocs:
            for byte_off in reloc_mask_bytes(r_type, r_off - sym_off):
                if 0 <= byte_off < len(mask):
                    mask[byte_off] = 0

        matches = search_rom(rom, pattern, mask)
        if len(matches) == 1:
            results.append((matches[0], sym_name, archive_name, obj_base,
                            sym_size, len(fn_relocs), 1))
        elif len(matches) > 1:
            # 多匹配, 也记录但标 multi
            for m_off in matches:
                results.append((m_off, sym_name, archive_name, obj_base,
                                sym_size, len(fn_relocs), len(matches)))
    return results, skipped_short


def main():
    if not os.path.isdir(WORK):
        os.makedirs(WORK)

    print("[load  ] ROM = %s" % ROM)
    with open(ROM, "rb") as f:
        rom = f.read()
    print("[load  ] ROM size = %d" % len(rom))

    all_results = []
    total_objs = 0
    total_syms_attempted = 0
    total_skipped_short = 0
    by_archive = {}

    for archive_name, archive_path in ARCHIVES:
        ext_dir = os.path.join(WORK, archive_name)
        if not os.path.isdir(ext_dir):
            os.makedirs(ext_dir)
        objs = extract_archive(archive_path, ext_dir)
        print("[arch  ] %-8s -> %d .o files" % (archive_name, len(objs)))
        a_results = []
        for obj in objs:
            total_objs += 1
            res, skipped = process_obj(obj, archive_name, rom)
            a_results.extend(res)
            total_skipped_short += skipped
            total_syms_attempted += len(res) + skipped
        by_archive[archive_name] = a_results
        all_results.extend(a_results)

    unique_matches = [r for r in all_results if r[6] == 1]
    multi_matches = [r for r in all_results if r[6] > 1]

    print("\n[summary]")
    print("  .o files processed         = %d" % total_objs)
    print("  symbols too short skipped  = %d  (size < %d)" % (total_skipped_short, MIN_SIZE))
    print("  unique matches  (uniq=1)   = %d" % len(unique_matches))
    print("  multi matches   (uniq>1)   = %d  (need disambig)" % len(multi_matches))
    print()
    print("  -- by archive --")
    for name in by_archive:
        u = len([r for r in by_archive[name] if r[6] == 1])
        m = len([r for r in by_archive[name] if r[6] > 1])
        print("  %-8s   unique=%d   multi=%d" % (name, u, m))

    out_dir = os.path.dirname(OUT)
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["address", "sym_name", "archive", "object", "size", "n_relocs", "n_matches"])
        for ms, name, arch, obj, size, nr, nm_ in sorted(all_results):
            gba_addr = 0x08000000 + ms
            w.writerow(["0x%08x" % gba_addr, name, arch, obj, size, nr, nm_])

    print("\n[wrote ] %s" % OUT)
    print()
    print("  unique sample:")
    for ms, name, arch, obj, size, nr, nm_ in unique_matches[:15]:
        print("    0x%08x  %-30s  %s/%s  size=%d  reloc=%d" % (
            0x08000000 + ms, name, arch, obj, size, nr))


if __name__ == "__main__":
    sys.exit(main() or 0)
