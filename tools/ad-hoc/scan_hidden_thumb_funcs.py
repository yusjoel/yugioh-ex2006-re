# -*- coding: utf-8 -*-
"""
扫描 asm/all.s 中所有 ROM_INCBIN 段, 通过 Thumb 函数入口/出口字节签名定位
被 Ghidra 漏掉的隐藏函数。

入口: halfword 0xB5xx (push {regs, lr}), 2 字节对齐
出口 (优先级高→低):
  1. 0xBDxx               pop {regs, pc}
  2. 0xBCxx 0x4770        pop {regs}; bx lr
  3. 0x4770               bx lr (leaf, 仅在 prologue=0xB500 时接受)

强约束: epilogue 寄存器集 == prologue 寄存器集 (避免随机字节噪声匹配)。
窗口: ≤ 0x800 (2KB)
最小函数长度: 8 字节

输出: temp/hidden_thumb_func_candidates.csv
"""

import os
import re
import struct
import sys

ROM_PATH = "roms/2343.gba"
ASM_PATH = "asm/all.s"
OUT_CSV = "temp/hidden_thumb_func_candidates.csv"

WINDOW = 0x800
MIN_LEN = 8
MAX_LEN = 0x800
ROM_BASE = 0x08000000
CODE_LO = 0x080000C0
CODE_HI = 0x08180000  # 上限收紧到 ROM 0x180000 (≥此址多为数据, 实测有 cbz / 不合法 adr 假阳)
MAX_INCBIN_SIZE = 0x4000  # 跳过 ≥ 16KB 的 incbin (基本都是图/音/字库等纯数据)

INCBIN_RE = re.compile(r'ROM_INCBIN\s+0x([0-9a-fA-F]+),\s+0x([0-9a-fA-F]+)')


def parse_incbin(asm_path):
    incbin = []
    with open(asm_path, encoding="utf-8") as f:
        for line in f:
            if ".macro" in line:
                continue
            m = INCBIN_RE.search(line)
            if not m:
                continue
            off = int(m.group(1), 16)
            length = int(m.group(2), 16)
            incbin.append((off, length))
    return incbin


def scan_func_in_window(rom, base_off, length):
    """在 [base_off, base_off+length) 内按对齐扫 prologue, 配对首个合法 epilogue。"""
    end = base_off + length
    candidates = []
    i = base_off
    while i < end - 1:
        # 2 字节对齐
        if (i & 1) != 0:
            i += 1
            continue
        hw = struct.unpack_from("<H", rom, i)[0]
        # 必须是 push {..., lr}: 0xB5xx
        if (hw & 0xff00) != 0xb500:
            i += 2
            continue
        push_regs = hw & 0xff  # r0-r7 mask
        # 在 [i+4, min(i+WINDOW, end)) 找 epilogue
        scan_lo = i + 4
        scan_hi = min(i + WINDOW, end)
        found_at = None
        found_kind = None
        j = scan_lo
        while j < scan_hi - 1:
            if (j & 1) != 0:
                j += 1
                continue
            ehw = struct.unpack_from("<H", rom, j)[0]
            # 1) BDxx pop {regs, pc}
            if (ehw & 0xff00) == 0xbd00:
                pop_regs = ehw & 0xff
                if pop_regs == push_regs:
                    found_at = j + 2
                    found_kind = "pop_pc"
                    break
            # 2) (BC??)+ 47YY  连续 1+ 个 pop 后跟 bx rN
            #    例: bc30 bc02 4708 (先 pop {r4,r5}, 再 pop {r1}, 再 bx r1)
            #    严格约束:
            #      a) total_popped (所有 bc 累计) ⊇ push_regs
            #      b) popcount(total_popped - push_regs) == 1 (恰好多出 1 位接 lr)
            #      c) 多出的位 = bx 目标寄存器 Rm
            #    或经典 bx lr: total_popped == push_regs, Rm == 14
            if (ehw & 0xff00) == 0xbc00:
                chain_at = j
                total_popped = 0
                chain_count = 0
                while chain_at + 2 <= scan_hi and chain_count < 4:
                    chw = struct.unpack_from("<H", rom, chain_at)[0]
                    if (chw & 0xff00) != 0xbc00:
                        break
                    total_popped |= chw & 0xff
                    chain_at += 2
                    chain_count += 1
                if chain_count > 0 and chain_at + 2 <= scan_hi:
                    next_hw = struct.unpack_from("<H", rom, chain_at)[0]
                    if (next_hw & 0xff87) == 0x4700:
                        rm = ((next_hw >> 3) & 0xf) | (((next_hw >> 6) & 1) << 3)
                        if rm == 14 and total_popped == push_regs:
                            found_at = chain_at + 2
                            found_kind = "pop_bx_lr"
                            break
                        elif rm < 8 and (push_regs & ~total_popped) == 0:
                            extra = total_popped & ~push_regs & 0xff
                            if extra == (1 << rm):
                                found_at = chain_at + 2
                                found_kind = "pop_bx_rN"
                                break
            # 3) 4770 (bx lr) — 仅当 prologue=B500 (push {lr} only)
            if ehw == 0x4770 and push_regs == 0:
                found_at = j + 2
                found_kind = "bx_lr"
                break
            j += 2

        if found_at is not None:
            flen = found_at - i
            if MIN_LEN <= flen <= MAX_LEN:
                candidates.append({
                    "rom_offset": i,
                    "rom_addr": ROM_BASE + i,
                    "length": flen,
                    "push_hw": hw,
                    "epilogue_kind": found_kind,
                    "incbin_base": base_off,
                    "incbin_end": end,
                })
                # 跳到 epilogue 之后, 同一 incbin 里可能多个函数
                i = found_at
                continue
        i += 2
    return candidates


def filter_anomalies(rom, cand):
    """字节模式异常过滤: 函数体含 ≥ 16 连续字节全 0 或全 0xff。"""
    off = cand["rom_offset"]
    n = cand["length"]
    body = rom[off:off + n]
    # 16 连续 0
    run0 = 0
    runf = 0
    for b in body:
        if b == 0:
            run0 += 1
            runf = 0
            if run0 >= 16:
                return False, "16 连 0"
        elif b == 0xff:
            runf += 1
            run0 = 0
            if runf >= 16:
                return False, "16 连 ff"
        else:
            run0 = 0
            runf = 0
    return True, ""


def main():
    rom = open(ROM_PATH, "rb").read()
    incbin = parse_incbin(ASM_PATH)
    print(f"[scan] {len(incbin)} ROM_INCBIN 段, 共 {sum(L for _,L in incbin):#x} 字节")
    print(f"[scan] 跳过 ≥ 0x{MAX_INCBIN_SIZE:x} 的 incbin (推定为 data 区)")

    all_cands = []
    skipped_huge = 0
    for off, length in incbin:
        # 只扫 code 范围内 (跳过明显 data 段, 上限 CODE_HI)
        rom_addr = ROM_BASE + off
        if rom_addr >= CODE_HI:
            continue
        if rom_addr + length <= CODE_LO:
            continue
        # 跳过 ≥ MAX_INCBIN_SIZE 的大块 (data 区)
        if length >= MAX_INCBIN_SIZE:
            skipped_huge += 1
            continue
        # 截到 code range 内
        eff_off = max(off, CODE_LO - ROM_BASE)
        eff_len = min(off + length, CODE_HI - ROM_BASE) - eff_off
        if eff_len < MIN_LEN:
            continue
        cands = scan_func_in_window(rom, eff_off, eff_len)
        all_cands.extend(cands)

    print(f"[scan] 原始候选 {len(all_cands)} 条")

    # 异常过滤 1: 字节模式
    kept = []
    rejected = []
    for c in all_cands:
        ok, reason = filter_anomalies(rom, c)
        if ok:
            kept.append(c)
        else:
            c["reject_reason"] = reason
            rejected.append(c)
    print(f"[scan] 字节模式过滤后 {len(kept)} 条 (剔除 {len(rejected)})")

    # 异常过滤 2: 同 incbin 内 ≥5 个候选共享相同 push_hw → 视为 data table 假阳
    by_incbin_push = {}
    for c in kept:
        key = (c["incbin_base"], c["push_hw"])
        by_incbin_push.setdefault(key, []).append(c)
    suspicious = set()
    for key, cands in by_incbin_push.items():
        if len(cands) >= 5:
            for c in cands:
                suspicious.add(id(c))
            print(f"[suspicious incbin] 0x{key[0]:x} push 0x{key[1]:04x}: {len(cands)} 个相同 prologue")
    kept2 = [c for c in kept if id(c) not in suspicious]
    print(f"[scan] 重复 prologue 过滤后 {len(kept2)} 条 (剔除 {len(kept) - len(kept2)})")
    kept = kept2

    # 输出 CSV
    os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
    with open(OUT_CSV, "w", encoding="utf-8") as f:
        f.write("rom_addr,rom_offset,length,push_hw,epilogue_kind,incbin_base,incbin_end,byte_preview\n")
        for c in kept:
            preview = rom[c["rom_offset"]:c["rom_offset"] + min(16, c["length"])].hex()
            f.write(f"0x{c['rom_addr']:08x},0x{c['rom_offset']:x},{c['length']},"
                    f"0x{c['push_hw']:04x},{c['epilogue_kind']},"
                    f"0x{c['incbin_base']:x},0x{c['incbin_end']:x},{preview}\n")
    print(f"[done] -> {OUT_CSV}")

    # 简报
    by_kind = {}
    for c in kept:
        by_kind[c["epilogue_kind"]] = by_kind.get(c["epilogue_kind"], 0) + 1
    print(f"[summary] epilogue kinds: {by_kind}")
    incbin_with_funcs = len(set(c["incbin_base"] for c in kept))
    print(f"[summary] {incbin_with_funcs} 个 incbin 段含至少 1 个候选函数")


if __name__ == "__main__":
    main()
