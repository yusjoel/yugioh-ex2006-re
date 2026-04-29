#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fid_nitrosdk_full_scan.py  --  对多个 NitroSDK 版本/架构组合做 FID 扫描

输入  refs/<sdk>/lib/<arch-build>/Rom/lib*.a
扫遍所有 .a 里的 .o, 抽全局 STT_FUNC, 套 reloc mask, 在 ROM 找 byte 唯一匹配.

用法:
   python tools/ad-hoc/fid_nitrosdk_full_scan.py
"""

import os
import shutil
import subprocess
import sys
from collections import defaultdict

from elftools.elf.elffile import ELFFile
from elftools.elf.relocation import RelocationSection


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ROM_PATH = os.path.join(REPO_ROOT, "roms", "2343.gba")
WORK_DIR = os.path.join(REPO_ROOT, "temp", "nitro-scan")

DEVKIT_BIN = r"D:\devkitPro\devkitARM\arm-none-eabi\bin"
AR = os.path.join(DEVKIT_BIN, "ar.exe")

# (label, root_dir_of_lib*.a)
VARIANTS = [
    ("v1.0_ARM9-TEG_Rom",   "refs/NitroSDK-1_0-040416/lib/ARM9-TEG/Rom"),
    ("v1.0_ARM9-BB_Rom",    "refs/NitroSDK-1_0-040416/lib/ARM9-BB/Rom"),
    ("v1.0_ARM7-TEG_Rom",   "refs/NitroSDK-1_0-040416/lib/ARM7-TEG/Rom"),
    ("v1.0_ARM7-BB_Rom",    "refs/NitroSDK-1_0-040416/lib/ARM7-BB/Rom"),
    ("v2.0RC3_ARM9-TS_Rom", "refs/NITRO SDK v2.0RC3/lib/ARM9-TS/Rom"),
    ("v2.0RC3_ARM9-TEG_Rom","refs/NITRO SDK v2.0RC3/lib/ARM9-TEG/Rom"),
]

MIN_SIZE = 8


def extract_lib(a_path, dest_dir):
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)
    subprocess.check_call([AR, "x", a_path], cwd=dest_dir, stderr=subprocess.DEVNULL)
    return [os.path.join(dest_dir, fn) for fn in os.listdir(dest_dir) if fn.endswith(".o")]


def analyze_obj(path):
    try:
        with open(path, "rb") as f:
            elf = ELFFile(f)
            section_data = {}
            section_size = {}
            rel_for_text = {}
            for i, sec in enumerate(elf.iter_sections()):
                if sec.name == ".text":
                    section_data[i] = sec.data()
                    section_size[i] = sec["sh_size"]
                if isinstance(sec, RelocationSection) and sec.name.startswith(".rel.text"):
                    tgt = sec["sh_info"]
                    rels = []
                    for r in sec.iter_relocations():
                        rels.append((r["r_offset"], r["r_info_type"]))
                    rel_for_text[tgt] = rels
            symtab = elf.get_section_by_name(".symtab")
            if symtab is None:
                return
            for sym in symtab.iter_symbols():
                if sym["st_info"]["type"] != "STT_FUNC":
                    continue
                if sym["st_info"]["bind"] != "STB_GLOBAL":
                    continue
                sec_idx = sym["st_shndx"]
                if sec_idx not in section_data:
                    continue
                offset = sym["st_value"]
                size = sym["st_size"]
                if size == 0:
                    size = section_size[sec_idx] - offset
                if size <= 0 or offset + size > section_size[sec_idx]:
                    continue
                data = section_data[sec_idx][offset:offset + size]
                relocs = [(r_off - offset, r_type)
                          for (r_off, r_type) in rel_for_text.get(sec_idx, [])
                          if offset <= r_off < offset + size]
                yield sym.name, data, relocs
    except Exception as e:
        return


def find_anchor(pattern, mask):
    bs, bl = 0, 0
    cs, cl = 0, 0
    for i, m in enumerate(mask):
        if m:
            if cl == 0:
                cs = i
            cl += 1
            if cl > bl:
                bl = cl
                bs = cs
        else:
            cl = 0
    return bs, bl


def search_rom(rom, pattern, mask):
    bs, bl = find_anchor(pattern, mask)
    if bl < 4:
        return []
    anchor = bytes(pattern[bs:bs + bl])
    n = len(pattern)
    rom_n = len(rom)
    matches = []
    pos = 0
    while True:
        idx = rom.find(anchor, pos)
        if idx < 0:
            break
        ms = idx - bs
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


def scan_variant(label, lib_root, rom):
    if not os.path.isdir(lib_root):
        return None
    a_files = sorted(fn for fn in os.listdir(lib_root)
                     if fn.endswith(".a") and not fn.endswith(".thumb.a"))
    a_files_thumb = sorted(fn for fn in os.listdir(lib_root)
                           if fn.endswith(".thumb.a"))
    extract_root = os.path.join(WORK_DIR, label)
    if os.path.isdir(extract_root):
        shutil.rmtree(extract_root)
    os.makedirs(extract_root)

    lib_data = []  # (libname, [obj_paths])
    for a_fn in a_files + a_files_thumb:
        libname = a_fn.replace(".a", "").replace(".thumb", ".thumb")
        dest = os.path.join(extract_root, libname)
        try:
            objs = extract_lib(os.path.join(lib_root, a_fn), dest)
        except Exception:
            continue
        lib_data.append((libname, objs))

    attempted = 0
    unique = 0
    multi = 0
    unique_hits = []  # (rom_addr, sym_name, libname, obj_basename, size)

    for libname, objs in lib_data:
        for obj in objs:
            for name, data, relocs in analyze_obj(obj):
                if len(data) < MIN_SIZE:
                    continue
                pattern = list(data)
                mask = [1] * len(pattern)
                for r_off, r_type in relocs:
                    for k in range(4):
                        if 0 <= r_off + k < len(mask):
                            mask[r_off + k] = 0
                matches = search_rom(rom, pattern, mask)
                attempted += 1
                if len(matches) == 1:
                    unique += 1
                    unique_hits.append((matches[0], name, libname,
                                        os.path.basename(obj), len(data)))
                elif len(matches) > 1:
                    multi += 1

    return {
        "label": label,
        "lib_count": len(lib_data),
        "attempted": attempted,
        "unique": unique,
        "multi": multi,
        "unique_hits": unique_hits,
    }


def main():
    print("[load  ] %s" % ROM_PATH)
    with open(ROM_PATH, "rb") as f:
        rom = f.read()

    if os.path.isdir(WORK_DIR):
        shutil.rmtree(WORK_DIR)
    os.makedirs(WORK_DIR)

    print()
    summary = []
    for label, lib_root_rel in VARIANTS:
        lib_root = os.path.join(REPO_ROOT, lib_root_rel)
        print("=" * 78)
        print("VARIANT: %s" % label)
        print("  root: %s" % lib_root)
        print("=" * 78)
        if not os.path.isdir(lib_root):
            print("  [missing dir, skipping]")
            continue
        result = scan_variant(label, lib_root, rom)
        if result is None:
            continue
        print("  libs=%d  funcs_attempted=%d  unique=%d  multi=%d" % (
            result["lib_count"], result["attempted"],
            result["unique"], result["multi"]))
        summary.append(result)
        # Show by-lib breakdown of unique hits
        by_lib = defaultdict(int)
        for ms, name, libname, obj, sz in result["unique_hits"]:
            by_lib[libname] += 1
        if by_lib:
            print("  by lib:")
            for ln in sorted(by_lib.keys()):
                print("    %-25s = %d" % (ln, by_lib[ln]))
        if result["unique_hits"]:
            print("  -- sample (top 12) --")
            for ms, name, libname, obj, sz in result["unique_hits"][:12]:
                print("    0x%08x  %-32s  size=%-5d  %s/%s" % (
                    0x08000000 + ms, name, sz, libname, obj))
        print()

    print("=" * 78)
    print("SUMMARY")
    print("=" * 78)
    for r in summary:
        print("  %-28s  attempted=%-5d  unique=%-3d  multi=%d" % (
            r["label"], r["attempted"], r["unique"], r["multi"]))


if __name__ == "__main__":
    sys.exit(main() or 0)
