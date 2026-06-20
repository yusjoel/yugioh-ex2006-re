# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixF09Seg4RLPPoolLabel.py -- Fix LP_CARD_TRACK_BASE_OFF pool label at 0x08072830
#
# Problem: DisassembleF09Seg4RBlocks.py set the slot label at 0x08072830 to
# "LP_CARD_TRACK_BASE_OFF" (same as the equate constant name).
# This causes GAS to emit:
#   LP_CARD_TRACK_BASE_OFF:
#       .word  LP_CARD_TRACK_BASE_OFF
# which resolves to the address of the label (0x08072830) not the value 0x1da8.
#
# Fix: rename the USER_DEFINED label at 0x08072830 to "pool_b8_2830" so the
# equate annotation still shows LP_CARD_TRACK_BASE_OFF as a comment but the
# .word value resolves correctly from the literal bytes.
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).

from ghidra.program.model.symbol import SourceType

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def main():
    print("=== FixF09Seg4RLPPoolLabel (DRY=%s) ===" % DRY)
    print("  Rename label at 0x08072830: LP_CARD_TRACK_BASE_OFF -> pool_b8_2830")

    if DRY:
        print("[dry] Would rename USER_DEFINED label at 0x08072830 -> pool_b8_2830")
        return

    a = _addr(0x08072830)
    sym_tbl = currentProgram.getSymbolTable()
    changed = False
    for sym in sym_tbl.getSymbols(a):
        if sym.getName() == "LP_CARD_TRACK_BASE_OFF" and sym.getSource() == SourceType.USER_DEFINED:
            sym.setName("pool_b8_2830", SourceType.USER_DEFINED)
            print("[ok ] Renamed LP_CARD_TRACK_BASE_OFF -> pool_b8_2830 @ 0x08072830")
            changed = True
        elif sym.getName() == "DAT_08072830":
            # Remove old auto label if present
            print("[info] Found DAT_ label (will be superceded by pool_b8_2830)")
    if not changed:
        # Also check if it's already pool_b8_2830
        for sym in sym_tbl.getSymbols(a):
            if sym.getName() == "pool_b8_2830":
                print("[info] Already named pool_b8_2830 -- no change needed")
                return
        print("[warn] LP_CARD_TRACK_BASE_OFF USER_DEFINED label not found at 0x08072830")
        print("[info] Symbols present: %s" % [s.getName() for s in sym_tbl.getSymbols(a)])
        # Create pool_b8_2830 label
        sym_tbl.createLabel(a, "pool_b8_2830", SourceType.USER_DEFINED)
        print("[ok ] Created pool_b8_2830 @ 0x08072830")

    print("\n=== FixF09Seg4RLPPoolLabel DONE ===")


main()
