# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# TagFunctionsByIORegs.py
#
# 方法论 doc/dev/methodology/function-naming.md §四 (方法 2: 硬件寄存器簇).
#
# 对每个函数, 遍历指令的 references-from, 收集落在以下区间的 target:
#   GBA IO MMIO   [0x04000000, 0x04000400)   (96 reg, 名字来自 constants/gba_io.inc)
#   PALRAM        [0x05000000, 0x05000400)
#   VRAM          [0x06000000, 0x06018000)
#   OAM           [0x07000000, 0x07000400)
#
# 按地址区间归类到 family, 主导 family = 命中次数最多的家族.
# 输出 temp/ghidra-funcs-io-tags.csv 一行一函数:
#   address, name, primary_family, all_families (按命中数降序),
#   total_refs, unique_regs, top_regs (top 5 + 命中数)
#
# 同时 stdout 打印 family 计数 + 已命名函数的 tag (用于核对 tag 逻辑).
#
# 此脚本 *只读*: 不 createFunction / 不 setName / 不 setComment.
# 但 ghidra-run-script.bat 的 -noanalysis (无 -readOnly) 仍会 "Save succeeded",
# 因为没改东西, 落到磁盘也是空 op.
#
# 用法:
#   tools\asm-regen\ghidra-run-script.bat TagFunctionsByIORegs.py

import os
import re


IO_LO = 0x04000000
IO_HI = 0x04000400

PAL_LO  = 0x05000000
PAL_HI  = 0x05000400
VRAM_LO = 0x06000000
VRAM_HI = 0x06018000
OAM_LO  = 0x07000000
OAM_HI  = 0x07000400


# 不重叠区间, 按 IO 寄存器分类的 family.
# 0x04000000-0x04000400 全覆盖.
IO_FAMILIES = [
    (0x04000000, 0x04000008, "display"),  # DISPCNT/STAT/VCOUNT
    (0x04000008, 0x04000040, "bg"),       # BGxCNT/HOFS/VOFS/Pxx/X/Y
    (0x04000040, 0x04000050, "win"),      # WIN0/1H/V, WININ/OUT, MOSAIC
    (0x04000050, 0x04000058, "blend"),    # BLDCNT/BLDALPHA/BLDY
    (0x04000058, 0x040000B0, "snd"),      # SOUNDxCNT, WAVE_RAM, FIFO_A/B
    (0x040000B0, 0x04000100, "dma"),      # DMA0-3
    (0x04000100, 0x04000120, "timer"),    # TM0-3CNT
    (0x04000120, 0x04000130, "sio"),      # SIODATA, SIOCNT
    (0x04000130, 0x04000134, "input"),    # KEYINPUT/CNT
    (0x04000134, 0x04000200, "sio"),      # RCNT/IR/JOY*
    (0x04000200, 0x04000400, "sys"),      # IE/IF/WAITCNT/IME/POSTFLG/HALTCNT
]


def repo_root():
    try:
        src = getSourceFile().getAbsolutePath()
        return os.path.dirname(os.path.dirname(os.path.dirname(src)))
    except Exception:
        return os.getcwd()


def parse_gba_io_inc(path):
    """Returns dict {addr_int: reg_name}."""
    out = {}
    pat = re.compile(r"^\.equ\s+(\w+),\s+0x([0-9A-Fa-f]+)")
    f = open(path, "r")
    try:
        for line in f:
            m = pat.match(line.strip())
            if m:
                out[int(m.group(2), 16)] = m.group(1)
    finally:
        f.close()
    return out


def family_for(addr_int):
    if PAL_LO <= addr_int < PAL_HI:
        return "pal"
    if VRAM_LO <= addr_int < VRAM_HI:
        return "vram"
    if OAM_LO <= addr_int < OAM_HI:
        return "obj"
    if not (IO_LO <= addr_int < IO_HI):
        return None
    for lo, hi, fname in IO_FAMILIES:
        if lo <= addr_int < hi:
            return fname
    return "io"


def reg_name_for(addr_int, io_map):
    if addr_int in io_map:
        return io_map[addr_int]
    if PAL_LO <= addr_int < PAL_HI:
        return "PALRAM+0x%X" % (addr_int - PAL_LO)
    if VRAM_LO <= addr_int < VRAM_HI:
        return "VRAM+0x%X" % (addr_int - VRAM_LO)
    if OAM_LO <= addr_int < OAM_HI:
        return "OAM+0x%X" % (addr_int - OAM_LO)
    return "0x%08x" % addr_int


def main():
    root = repo_root()
    io_map = parse_gba_io_inc(os.path.join(root, "constants", "gba_io.inc"))
    print("[loaded] %d IO regs from gba_io.inc" % len(io_map))

    fm = currentProgram.getFunctionManager()
    listing = currentProgram.getListing()

    out_dir = os.path.join(root, "temp")
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    csv_path = os.path.join(out_dir, "ghidra-funcs-io-tags.csv")
    fcsv = open(csv_path, "w")
    fcsv.write("address,name,primary_family,all_families,total_refs,unique_regs,top_regs\n")

    family_counts = {}
    family_named = {}    # family -> [(name, addr), ...] for 已命名函数
    total = 0
    untagged = 0

    funcs = fm.getFunctions(True)
    while funcs.hasNext():
        f = funcs.next()
        total += 1
        ep = f.getEntryPoint()
        addr_int = ep.getOffset() & 0xFFFFFFFF
        name = f.getName()

        body = f.getBody()
        if body is None:
            untagged += 1
            fcsv.write("0x%08x,%s,,,0,0,\n" % (addr_int, name))
            continue

        instr_iter = listing.getInstructions(body, True)

        regs_hit = {}
        family_hit = {}
        total_refs = 0

        while instr_iter.hasNext():
            instr = instr_iter.next()
            for ref in instr.getReferencesFrom():
                ta = ref.getToAddress()
                if ta is None:
                    continue
                ta_int = ta.getOffset() & 0xFFFFFFFF
                fam = family_for(ta_int)
                if fam is None:
                    continue
                regs_hit[ta_int] = regs_hit.get(ta_int, 0) + 1
                family_hit[fam] = family_hit.get(fam, 0) + 1
                total_refs += 1

        if not family_hit:
            untagged += 1
            fcsv.write("0x%08x,%s,,,0,0,\n" % (addr_int, name))
            continue

        sorted_fam = sorted(family_hit.items(), key=lambda x: -x[1])
        primary = sorted_fam[0][0]
        family_counts[primary] = family_counts.get(primary, 0) + 1

        all_fams = "|".join(["%s:%d" % (fam, c) for fam, c in sorted_fam])

        sorted_regs = sorted(regs_hit.items(), key=lambda x: -x[1])[:5]
        top_regs = "|".join(["%s(%d)" % (reg_name_for(a, io_map), c) for a, c in sorted_regs])

        fcsv.write("0x%08x,%s,%s,%s,%d,%d,%s\n" % (
            addr_int, name, primary, all_fams, total_refs, len(regs_hit), top_regs))

        # Track 已命名函数 (name 不是 FUN_xxxxxxxx) 用于核对
        if not name.startswith("FUN_") and not name.startswith("SUB_") and not name.startswith("thunk_FUN_"):
            family_named.setdefault(primary, []).append((name, addr_int))

    fcsv.close()

    print("\n[done] TagFunctionsByIORegs")
    print("  total funcs       = %d" % total)
    print("  tagged            = %d (%.1f%%)" % (
        total - untagged, 100.0 * (total - untagged) / total if total else 0))
    print("  untagged          = %d  (函数体内无 IO/PAL/VRAM/OAM ref)" % untagged)
    print("\n  -- by primary family --")
    for fam in sorted(family_counts.keys(), key=lambda k: -family_counts[k]):
        print("    %-10s = %4d" % (fam, family_counts[fam]))

    print("\n  -- 已命名函数 vs 自动 family tag (sanity check) --")
    for fam in sorted(family_named.keys()):
        items = family_named[fam]
        print("    [%s] %d 个:" % (fam, len(items)))
        for nm, a in items[:8]:
            print("      0x%08x  %s" % (a, nm))
        if len(items) > 8:
            print("      ... +%d" % (len(items) - 8))

    print("\n  -> %s" % csv_path)


main()
