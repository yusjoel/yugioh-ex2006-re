# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF01Seg3PlateFix.py -- fix CJK plate for update_card_info_page_state (0x0801e36c)
# This is the adjacent function at the Seg-4 boundary whose plate references
# the old name card_info_page_step_03_unknown -> render_card_name_to_desc_page_vram.
# Pure ASCII replacement.

from ghidra.program.model.listing import CodeUnit

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
    print("=== RefineF01Seg3PlateFix (DRY=%s) ===" % DRY)

    # update_card_info_page_state (0x0801e36c): CJK plate with old func ref
    func_addr = 0x0801e36c
    new_plate = (
        '@ Per-frame state update for the card info page scene.\n'
        '@ Reads gPrng+0x148 (0x03000188) bits[1:0]; if nonzero: calls sync_state_and_init_sprite(1).\n'
        '@ Reads gCardInfoPageState+0x6 countdown; if nonzero: decrements and returns 1 when zero.\n'
        '@ Reads gPrng+0x146 display flags bit7/bit6 to adjust gCardInfoPageState+0x20 scroll offset.\n'
        '@ If gPrng+0x148 bit2 set and gSettings bits[2:0]==0:\n'
        '@   toggles gCardInfoPageState+0x0 bit0, then calls render_card_name_to_desc_page_vram.\n'
        '@ Returns 0 (continue) or 1 (trigger scene transition).\n'
        '@ indeg=1; caller: tick_card_info_page_by_state (0x0801e714).'
    )

    a = _addr(func_addr)
    cu = currentProgram.getListing().getCodeUnitAt(a)
    if cu is None:
        print("[WARN] 0x%08x: no code unit" % func_addr)
        return

    if DRY:
        print("[dry] PLATE 0x%08x: CJK->ASCII rewrite (%d chars)" % (func_addr, len(new_plate)))
        return

    cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)
    print("[PLT] 0x%08x: plate updated (ASCII, %d chars)" % (func_addr, len(new_plate)))
    print("=== RefineF01Seg3PlateFix DONE ===")

main()
