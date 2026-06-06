# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineSeg4LightRenames.py — p5 Seg-4 (0x1571c..0x16218)
#   大部分已被 b7/b10/b11/b9/b8 细化, 仅剩 2 个 R2 + 3 §5.1 登记 (后者不在脚本内):
#   - DAT_08015fe4 (0x01000012 cpu_set fill ctrl for zero_struct_36bytes) -> 改名
#   - PTR_DAT_08016060 (5-entry 跳转表, 仅被孤儿 dispatcher 0x1604c 引用) -> 改名标 orphan
from ghidra.program.model.symbol import SourceType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"): DRY = True
except Exception:
    pass

RENAME_SLOTS = [
 (0x08015fe4, 'zero_struct_36bytes_fill_ctrl',
  '= 0x01000012; bit24=0 cpu_set / bit26=1 fill / halfword / len=0x12=18 hw=36B'),
 (0x08016060, 'orphan_bg_screen_vram_jump_table',
  '5-entry; targets 0x16074/7a/80/86/8c (orphan handlers @0x16074 ROM_INCBIN, dead code, 0 ext refs)'),
]


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def main():
    print("=== RefineSeg4LightRenames (DRY=%s) ===" % DRY)
    listing = currentProgram.getListing()
    n = 0
    for slot_int, label, eol in RENAME_SLOTS:
        d = getDataAt(_addr(slot_int))
        if d is None or d.getLength() != 4:
            print("[FAIL] no 4B data @ 0x%08x" % slot_int); continue
        if DRY:
            print("[dry] 0x%08x rename %s +EOL" % (slot_int, label)); n += 1; continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        if eol:
            listing.getCodeUnitAt(_addr(slot_int)).setComment(CodeUnit.EOL_COMMENT, eol)
        print("[ok] 0x%08x -> %s" % (slot_int, label)); n += 1
    print("[done] %d (DRY=%s)" % (n, DRY))


main()
