# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixIsdCounterAddr.py — batch-4 附带: setup_isd_cell_anim_oam_entry(0x08015954) plate 里
#   propagated 的 0x02024330 错址订正 (slot 计数器实为 gGlState+0x8a0 = 0x02023d30)。
#   与 batch-4 alloc_palette_entry_slot 同一错误类。
# Usage: tools\asm-regen\ghidra-run-script.bat FixIsdCounterAddr.py [dry]
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"): DRY = True
except Exception:
    pass

ADDR = 0x08015954
OLD = u"EWRAM palette slot [0x02024330]+1"
NEW = u"EWRAM palette slot [gGlState+0x8a0 (0x02023d30)]+1"


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def main():
    cu = currentProgram.getListing().getCodeUnitAt(_addr(ADDR))
    txt = cu.getComment(CodeUnit.PLATE_COMMENT) if cu else None
    if txt is None:
        print("[FAIL] no plate @ 0x%08x" % ADDR); return
    if OLD not in txt:
        print("[FAIL] pattern not found"); return
    if DRY:
        print("[dry] would fix 0x02024330 -> gGlState+0x8a0"); return
    cu.setComment(CodeUnit.PLATE_COMMENT, txt.replace(OLD, NEW))
    print("[ok] plate fixed @ 0x%08x" % ADDR)


main()
