# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF11Seg1Blocks.py -- f11 Seg-1 THUMB disassembly of 2 ROM_INCBIN blocks
#
# Blocks:
#   BLK1 0x080850f0/0x28: fn_activate handler for CID 0x196a (Scarr, Scout of Dark World)
#         Single function: dispatch_equip_slot_display_by_type_scarr
#         THUMB+1 ref at 0x09e46248 (dispatch table fn_activate slot)
#         fn-ptr table at 0x08085118..0x0808512c (6 raw .word entries) already in asm
#         clearListing 0x080850f0..0x08085118 (stop before fn-ptr table which is in asm)
#
#   BLK2 0x08085130/0x14c: 16 entry points, 3 degenerate skips, 13 createFunction targets
#         clearListing 0x08085130..0x0808527c
#         Degenerate skips (NOT createFunction):
#           0x080851cc: second halfword of BL at 0x80851ca/cc (mid-BL split)
#           0x0808520e: 0x0000 padding byte after B instruction
#           0x08085210: literal pool = gP1LifePoints (0x0201c4e0) -> createDWord
#         13 createFunction targets:
#           0x08085130, 0x08085140, 0x08085142, 0x08085144, 0x08085150,
#           0x080851a8, 0x080851d4, 0x08085200, 0x08085204,
#           0x08085228, 0x08085230, 0x08085248, 0x0808524a
#
# Plate text for clear_equip_slot_attr_bits_and_activate: reviewer nuance: bit 0 also cleared
#   -> plate says "bits 0,2,3,4" (RSBS-negate of 0x1d clears bits 0,2,3,4 of slot+6)
#
# Post-disasm gate: ROM_INCBIN/.byte-code grep in [0x080850f0,0x0808527c) == 0
# All EOL/plate text is pure ASCII. Ghidra Jython mojibake prevention.

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.address import AddressSet
from ghidra.program.model.data import DWordDataType
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import SourceType
from java.math import BigInteger

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _clear_and_tmode(lo_int, hi_int):
    lo = _addr(lo_int)
    hi = _addr(hi_int)
    try:
        clearListing(lo, hi)
    except Exception as e:
        print("[warn] clearListing 0x%08x..0x%08x: %s" % (lo_int, hi_int, e))
    ctx = currentProgram.getProgramContext()
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        ctx.setValue(tmode, lo, hi, BigInteger.ONE)
    print("[tmode] set THUMB 0x%08x..0x%08x" % (lo_int, hi_int))


def _disasm_stub(entry_int):
    a = _addr(entry_int)
    cmd = DisassembleCommand(a, None, True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm 0x%08x: %s" % (entry_int, cmd.getStatusMsg()))
    else:
        print("[disasm ok] 0x%08x" % entry_int)


def _create_dword(addr_int, label=None, eol=None):
    a = _addr(addr_int)
    listing = currentProgram.getListing()
    dt = DWordDataType.dataType
    try:
        listing.clearCodeUnits(a, _addr(addr_int + 3), False)
        listing.createData(a, dt)
    except Exception as e:
        print("[warn] createDWord 0x%08x: %s" % (addr_int, e))
    if label:
        sym_table = currentProgram.getSymbolTable()
        try:
            sym_table.createLabel(a, label, SourceType.USER_DEFINED)
            for s in sym_table.getSymbols(a):
                if s.getName() == label:
                    s.setPrimary()
                    break
        except Exception as e:
            print("[warn] label dword 0x%08x %s: %s" % (addr_int, label, e))
    if eol:
        cu = listing.getCodeUnitAt(a)
        if cu:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)


def _make_label(addr_int, name, eol=None):
    sym_table = currentProgram.getSymbolTable()
    listing = currentProgram.getListing()
    try:
        sym_table.createLabel(_addr(addr_int), name, SourceType.USER_DEFINED)
        for s in sym_table.getSymbols(_addr(addr_int)):
            if s.getName() == name:
                s.setPrimary()
                break
    except Exception as e:
        print("[warn] makeLabel 0x%08x %s: %s" % (addr_int, name, e))
    if eol:
        cu = listing.getCodeUnitAt(_addr(addr_int))
        if cu:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)


def _create_func(addr_int, name):
    fn = getFunctionAt(_addr(addr_int))
    if fn is None:
        fn = createFunction(_addr(addr_int), name)
    if fn is not None:
        try:
            fn.setName(name, SourceType.USER_DEFINED)
            print("[func] %s @ 0x%08x" % (name, addr_int))
        except Exception as e:
            print("[warn] setName 0x%08x %s: %s" % (addr_int, name, e))
    else:
        print("[FAIL] createFunction 0x%08x %s" % (addr_int, name))


def _set_plate(addr_int, plate_text):
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(_addr(addr_int))
    if cu is None:
        print("[FAIL] PLATE 0x%08x: no code unit (WARN=FAIL)" % addr_int)
        return
    try:
        cu.setComment(CodeUnit.PLATE_COMMENT, plate_text)
        print("[plate] 0x%08x OK" % addr_int)
    except Exception as e:
        print("[FAIL] PLATE 0x%08x: %s (WARN=FAIL)" % (addr_int, e))


def main():
    if DRY:
        print("DRY RUN -- DisassembleF11Seg1Blocks:")
        print("  BLK1: 1 disasm, 1 createFunction (dispatch_equip_slot_display_by_type_scarr)")
        print("  BLK2: 13 disasm, 13 createFunction, 1 createDWord (gP1LifePoints pool @0x08085210)")
        print("  3 degenerate skips: 0x080851cc (mid-BL), 0x0808520e (padding), 0x08085210 (pool)")
        print("  All 14 plates: pure ASCII")
        return

    # =====================================================================
    # BLK1: 0x080850f0/0x28 -- dispatch_equip_slot_display_by_type_scarr
    # clearListing 0x080850f0..0x08085118 (fn-ptr table starts at 0x08085118, keep in asm)
    # fn entry at 0x080850f0; prologue 0xb510 = push{r4,lr}
    # THUMB+1 ref at 0x09e46248: [fn_act+1=0x080850f1, CID=0x196a, fn_elig+1=0x080661fd]
    # =====================================================================
    print("=== BLK1: dispatch_equip_slot_display_by_type_scarr @0x080850f0 ===")
    _clear_and_tmode(0x080850f0, 0x08085118)
    _disasm_stub(0x080850f0)
    _create_func(0x080850f0, 'dispatch_equip_slot_display_by_type_scarr')
    _set_plate(0x080850f0,
        "fn_activate for Scarr, Scout of Dark World (CID 0x196a).\n"
        "Reads [gDuelPhaseFlags+SLOT_DISPLAY_TYPE_OFF]; if <= 5 dispatches to one of 6\n"
        "sub-handler entries via raw-ptr table at 0x08085118 (MOV PC, R0); else falls through.\n"
        "Returns result of sub-handler (0=advance, 1=skip/done).")

    # =====================================================================
    # BLK2: 0x08085130/0x14c -- 13 createFunction targets + 3 degenerate skips
    # clearListing 0x08085130..0x0808527c
    # Degenerate skips:
    #   0x080851cc: second halfword of BL at 0x80851ca (mid-BL; NOT a function entry)
    #   0x0808520e: 0x0000 padding; NOT a function entry
    #   0x08085210: literal pool word = gP1LifePoints (0x0201c4e0); createDWord only
    # =====================================================================
    print("=== BLK2: 13 sub-function stubs @0x08085130..0x0808527c ===")
    _clear_and_tmode(0x08085130, 0x0808527c)

    # createDWord for gP1LifePoints literal pool slot (degenerate skip #3)
    _create_dword(0x08085210, 'gp1lp_blk2_pool_85210',
                  'gP1LifePoints=0x0201c4e0 literal pool slot; NOT a function entry')

    # Per-entry DisassembleCommand for each of the 13 valid EPs (address order)
    for ep in [0x08085130, 0x08085140, 0x08085142, 0x08085144, 0x08085150,
               0x080851a8, 0x080851d4, 0x08085200, 0x08085204,
               0x08085228, 0x08085230, 0x08085248, 0x0808524a]:
        _disasm_stub(ep)

    # createFunction + setName + plate for each of the 13 EPs
    # Note: 0x080850f0 plate uses "bits 0,2,3,4" per reviewer nuance (bit 0 also cleared)

    # --- type-0 standalone handler and cascade alt-entries ---
    _create_func(0x08085130, 'clear_equip_slot_attr_bits_and_activate')
    _set_plate(0x08085130,
        "Type-0 sub-handler. Clears bits 15-17 of slot+4 (sprite attr word) and\n"
        "bits 0,2,3,4 of slot+6 (display byte via RSBS-negate of 0x1d), then falls through\n"
        "to check player-zone match and set LP activation.")

    _create_func(0x08085140, 'store_equip_slot_attr_byte_and_activate')
    _set_plate(0x08085140,
        "Alt-entry into type-0 body after sprite-word clear. Executes STRB r0,[r4,#6]\n"
        "to store pre-computed display byte, then falls through to player-zone match check.")

    _create_func(0x08085142, 'load_equip_slot_player_and_activate')
    _set_plate(0x08085142,
        "Alt-entry; skips display byte store. Loads player-flag byte at slot+2,\n"
        "then falls through to eval_equip_slot_player_match_and_set_lp_active logic.")

    _create_func(0x08085144, 'eval_equip_slot_player_match_and_set_lp_active')
    _set_plate(0x08085144,
        "Core type-0 eval: extracts bit0 of slot+2 as player side; loads slot+0x14 word;\n"
        "checks bits 11 and 9 vs player (same-side guard -> return 1).\n"
        "Calls count_effect_node_zone_activations; if 0 returns 1.\n"
        "Checks gDuelCardCtxBase[player+8]==1: if yes writes 1 to gEquipLpActivBitmap[player];\n"
        "else calls invoke_card_display_op_0x31_sub1(0x13a).\n"
        "Increments SLOT_DISPLAY_TYPE, returns 0.")

    _create_func(0x08085150, 'check_equip_slot_zone_bit9_and_activate')
    _set_plate(0x08085150,
        "Alt-entry inside type-0 eval; re-enters after bit-11 check.\n"
        "Tests bit 9 of slot+0x14 vs player side (second same-side guard -> return 1).\n"
        "Falls through to activation path.")

    # --- type-1/4 shared handler ---
    _create_func(0x080851a8, 'check_lp_pending_and_set_equip_activation_state')
    _set_plate(0x080851a8,
        "Types 1 and 4 sub-handler (table[1,4]). Reads [gP1LifePoints+LP_ACTIVATION_PENDING_OFF]:\n"
        "if zero returns 1 (no pending, skip). Else extracts player from slot+2,\n"
        "loads CID from slot+0, calls set_equip_activation_state_by_mode(\n"
        "  player, CID, check_effect_node_handler_for_slot+1).\n"
        "Increments SLOT_DISPLAY_TYPE, returns 0.")

    # --- type-2/5 shared handler and cascade alt-entries ---
    _create_func(0x080851d4, 'enqueue_equip_slot_sprite_if_display_confirmed')
    _set_plate(0x080851d4,
        "Types 2 and 5 sub-handler (table[2,5]). Calls check_activation_display_state_is_confirmed:\n"
        "if not confirmed decrements SLOT_DISPLAY_TYPE by 2, returns 0.\n"
        "If confirmed: loads ELIGIB_SPRITE_CTRL_OFF and ELIGIB_ANIM_STATE_OFF from gP1LifePoints;\n"
        "calls enqueue_equip_slot_sprite_with_code_rotation then count_effect_node_zone_activations;\n"
        "if activations <= 1 returns 1; checks bits 4-2 of slot+6 <= 1,\n"
        "then increments SLOT_DISPLAY_TYPE and returns 0.")

    _create_func(0x08085200, 'check_activation_count_lte1_and_advance')
    _set_plate(0x08085200,
        "Alt-entry after enqueue sprite call; CMP r0,#1; BLE -> return 1\n"
        "(if activation count <= 1 skip advance). Else loads byte at slot+6,\n"
        "extracts bits 4-2, tests > 1 -> return 1;\n"
        "else increments SLOT_DISPLAY_TYPE and returns 0.")

    _create_func(0x08085204, 'check_slot_display_field_and_advance_type')
    _set_plate(0x08085204,
        "Alt-entry with byte already in r4; extracts bits 4-2 from r4 (3-bit display field 0-7);\n"
        "if > 1 returns 1; else branches to increment-SLOT_DISPLAY_TYPE path (returns 0).")

    _create_func(0x08085228, 'store_decremented_display_type_and_return')
    _set_plate(0x08085228,
        "Minimal stub: immediately branches to store path at 0x808526a (STR r0,[r1]; return 0).\n"
        "Entered with r0 = display_type - 2 and r1 = ptr to SLOT_DISPLAY_TYPE_OFF.\n"
        "Stores the decremented value and returns 0.\n"
        "Shared tail for type-2/5 not-confirmed path.")

    # --- type-3 standalone handler and cascade alt-entries ---
    _create_func(0x08085230, 'activate_or_enqueue_type3_equip_slot_display')
    _set_plate(0x08085230,
        "Type-3 sub-handler (table[3]). Reads player from slot+2;\n"
        "checks gDuelCardCtxBase[player*4+8]: if == 1 writes 1 to\n"
        "[gP1LifePoints+LP_ACTIVATION_PENDING_OFF] and increments SLOT_DISPLAY_TYPE, returns 0.\n"
        "Else calls invoke_card_display_op_0x31_sub1(0x13b)\n"
        "then increments SLOT_DISPLAY_TYPE, returns 0.")

    _create_func(0x08085248, 'complete_lp_pending_offset_and_set')
    _set_plate(0x08085248,
        "Alt-entry mid-computation of LP_ACTIVATION_PENDING_OFF:\n"
        "r3 already holds 0xea (from prior MOVS at 0x8085246); LSLS r3,r3,#5 -> r3=0x1d40;\n"
        "ADDS r0,r0,r3; STR r1,[r0]; then branches to increment-SLOT_DISPLAY_TYPE path.")

    _create_func(0x0808524a, 'write_lp_activation_pending_and_advance')
    _set_plate(0x0808524a,
        "Alt-entry with r0 = final gP1LifePoints+LP_ACTIVATION_PENDING_OFF ptr and r1=1 computed;\n"
        "STR r1,[r0] writes activation pending; branches to increment-SLOT_DISPLAY_TYPE path,\n"
        "returns 0.")

    print("")
    print("=== DisassembleF11Seg1Blocks DONE ===")
    print("BLK1: dispatch_equip_slot_display_by_type_scarr @0x080850f0")
    print("BLK2: 13 functions from 0x08085130..0x0808524a")
    print("DWord: gP1LifePoints pool @0x08085210")
    print("Degenerate skips: 0x080851cc (mid-BL), 0x0808520e (padding), 0x08085210 (pool)")


main()
