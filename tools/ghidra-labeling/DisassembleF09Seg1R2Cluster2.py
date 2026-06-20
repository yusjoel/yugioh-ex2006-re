# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF09Seg1R2Cluster2.py -- F09 Seg-1 REMEDIATION Cluster-2
#   Remediates partial-disasm residue in [0x0806f85e..0x0806ff0a).
#   9 ROM_INCBIN blocks + 11 companion .byte blocks -> full THUMB disasm.
#   Also applies 18 EQ_SLOTS (14 REUSE + 4 NEW) and 2 REF_SLOTS.
#
#   NEW constants (must be added to .inc files before running):
#     constants/card_info.inc:  SPIRIT_MESSAGE_N_CID=0x1498, SPIRIT_MESSAGE_A_CID=0x1499
#                               CARD_DISPLAY_OP31_LP_BAR_SUB=0x011d
#     constants/oam_attr.inc:   OAM_EQUIP_LP_SPRITE_P1_5E=0x0000805e
#
#   Execution order:
#   CLUSTER-2A (Destiny Board):
#     Step A1:  B2g -- equip_lp_sub_fb76 body (shared epilogue) FIRST
#     Step A2:  B2f -- equip_lp_sub_fb70 body
#     Step A2b: B2a -- equip_lp_sub_fa4c body (added per review #1)
#     Step A3:  B2e -- equip_lp_sub_fb64 body
#     Step A4:  B2d -- equip_lp_sub_fb58 body
#     Step A5:  B2c -- equip_lp_sub_fb4c body
#     Step A6:  B5  -- equip_lp_sub_fb14 body (ROM_INCBIN 0x6fb16/0x32) + createDWord fb48
#     Step A7:  B4  -- equip_lp_sub_fa74 body (ROM_INCBIN 0x6fa78/0x8c) + createDWord fb04/08/0c/10
#     Step A8:  B3  -- equip_lp_sub_fa5e body (ROM_INCBIN 0x6fa62/0x12)
#     Step A9:  B2  -- eligible_sub_stubs_fa08 body (ROM_INCBIN 0x6fa0a/0x36 + b+pad 0x6fa40)
#     Step A10: B1  -- eligible_destiny_board_f85c body (ROM_INCBIN 0x6f85e/0x136, multi-pass)
#   CLUSTER-2B (Cathedral of Nobles):
#     Step B1:  B7g -- equip_chain_act_sub_ff46 body (shared epilogue) FIRST
#     Step B2:  B7f -- equip_chain_act_sub_ff3c body
#     Step B3:  B7e -- equip_chain_act_sub_ff2c body
#     Step B4:  B7d -- equip_chain_act_sub_ff1a body
#     Step B5:  B7c -- equip_chain_act_sub_ff0a body
#     Step B6:  B9  -- equip_chain_act_sub_fef0 body (ROM_INCBIN 0x6fef2/0x18)
#     Step B7:  B8  -- equip_chain_act_sub_fedc body (ROM_INCBIN 0x6fede/0x12)
#     Step B8:  B7  -- eligible_sub_stubs_fe88 body (ROM_INCBIN 0x6fe8a/0x4a + b+pad 0x6fed4)
#               + createDWord fed8
#     Step B9:  B6  -- eligible_cathedral_of_nobles_fdec body (ROM_INCBIN 0x6fdee/0x26)
#               + createDWord fe0c + fe10
#   EQ/REF:    Apply all 18 equate slots + 2 REF slots
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).
# NOTE: b+pad words (0x6fa40=0x0000e09a, 0x6fed4=0x0000e038) are cleared by
#       disassembly and decoded as b + .zero 2 (byte-identical).
# NOTE: .word 0x00004708 at 0x6ff4c decoded as bx r1 + .zero 2 (byte-identical).

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.address import AddressSet
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import SourceType, RefType
from java.math import BigInteger

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass


# ---------------------------------------------------------------------------
# EQ_SLOTS: (slot_addr, value, const_name, slot_label)
# Applied after disasm (createDWord must exist first)
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # B1 pools (ROM_INCBIN 0x6f85e/0x136)
    (0x0806f92c, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'player_stride_f92c'),
    (0x0806f930, 0x0201c510, 'gDuelFieldSlots',               'gduel_slots_f930'),
    (0x0806f934, 0x0000805e, 'OAM_EQUIP_LP_SPRITE_P1_5E',    'oam_lp_sprite_f934'),
    (0x0806f954, 0x00001497, 'SPIRIT_MESSAGE_I_CID',          'spirit_msg_i_f954'),
    (0x0806f95c, 0x00001498, 'SPIRIT_MESSAGE_N_CID',          'spirit_msg_n_f95c'),
    (0x0806f964, 0x00001499, 'SPIRIT_MESSAGE_A_CID',          'spirit_msg_a_f964'),
    (0x0806f988, 0x0000149a, 'SPIRIT_MESSAGE_L_CID',          'spirit_msg_l_f988'),
    (0x0806f98c, 0x0201b290, 'gDuelPhaseFlags',               'gduel_phase_f98c'),
    # B4 pools (ROM_INCBIN 0x6fa78/0x8c)
    (0x0806fb04, 0x0000805e, 'OAM_EQUIP_LP_SPRITE_P1_5E',    'oam_lp_sprite_fb04'),
    (0x0806fb08, 0x00001379, 'GRAVEROBBER_CID',               'graverobber_fb08'),
    (0x0806fb0c, 0x0201b290, 'gDuelPhaseFlags',               'gduel_phase_fb0c'),
    (0x0806fb10, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',         'equip_frame_fb10'),
    # B5 pool (ROM_INCBIN 0x6fb16/0x32)
    (0x0806fb48, 0x0000805e, 'OAM_EQUIP_LP_SPRITE_P1_5E',    'oam_lp_sprite_fb48'),
    # B6 pools (ROM_INCBIN 0x6fdee/0x26)
    (0x0806fe0c, 0x0201b290, 'gDuelPhaseFlags',               'gduel_phase_fe0c'),
    # B7 pool (ROM_INCBIN 0x6fe8a/0x4a)
    (0x0806fed8, 0x0000011d, 'CARD_DISPLAY_OP31_LP_BAR_SUB', 'card_disp_sub_fed8'),
]

# REF_SLOTS: (slot_addr, target, gas_label, slot_label)
REF_SLOTS = [
    (0x0806f990, 0x0806f994, 'equip_lp_disp_table_f994',        'equip_lp_tbl_f990'),
    (0x0806fe10, 0x0806fe14, 'equip_chain_act_disp_table_fe14', 'equip_chain_tbl_fe10'),
]


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _set_tmode(lo_int, hi_int):
    lo = _addr(lo_int)
    hi = _addr(hi_int)
    ctx = currentProgram.getProgramContext()
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        ctx.setValue(tmode, lo, hi, BigInteger.ONE)
        print("[ok ] setTMode=THUMB 0x%08x..0x%08x" % (lo_int, hi_int))
    else:
        print("[warn] TMode register not found")


def _clear_listing(lo_int, hi_int):
    lo = _addr(lo_int)
    hi = _addr(hi_int)
    try:
        clearListing(lo, hi)
        print("[ok ] clearListing 0x%08x..0x%08x" % (lo_int, hi_int))
    except Exception as e:
        print("[warn] clearListing 0x%08x..0x%08x: %s" % (lo_int, hi_int, e))


def _disasm_at(stub_lo_int, stub_hi_int, label):
    lo = _addr(stub_lo_int)
    hi = _addr(stub_hi_int)
    cmd = DisassembleCommand(lo, AddressSet(lo, hi), True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm %s @ 0x%08x: %s" % (label, stub_lo_int, cmd.getStatusMsg()))
    else:
        print("[ok ] disasm %s @ 0x%08x" % (label, stub_lo_int))


def _force_dword(addr_int):
    """Force a DWORD data item at addr_int (clears listing first)."""
    a = _addr(addr_int)
    a_end = _addr(addr_int + 3)
    listing = currentProgram.getListing()
    try:
        clearListing(a, a_end)
    except Exception as e:
        print("[warn] force_dword clearListing @ 0x%08x: %s" % (addr_int, e))
    try:
        listing.createData(a, ghidra.program.model.data.DWordDataType.dataType)
        print("[ok ] force_dword @ 0x%08x" % addr_int)
    except Exception as e:
        print("[warn] force_dword createData @ 0x%08x: %s" % (addr_int, e))


def _count_instrs(lo_int, hi_int):
    """Count instructions in range [lo_int..hi_int]."""
    listing = currentProgram.getListing()
    lo_a = _addr(lo_int)
    hi_a = _addr(hi_int)
    n = 0
    inst = listing.getInstructionAt(lo_a)
    while inst is not None and inst.getAddress().compareTo(hi_a) <= 0:
        n += 1
        inst = listing.getInstructionAfter(inst.getAddress())
    return n


def _check_dword(slot_int, want):
    d = getDataAt(_addr(slot_int))
    if d is None or d.getLength() != 4:
        return False, "no 4B data"
    try:
        dv = d.getValue()
        iv = (int(dv.getValue()) & 0xffffffff) if hasattr(dv, "getValue") else (int(dv) & 0xffffffff)
    except Exception:
        iv = None
    if iv is not None and iv != (want & 0xffffffff):
        return False, "value mismatch got=0x%x want=0x%x" % (iv, want)
    return True, None


def _apply_eq(slot_int, value, cname, label):
    """Apply equate + slot label to an existing DWORD at slot_int."""
    ok, err = _check_dword(slot_int, value)
    if not ok:
        print("[EQ FAIL] 0x%08x %s: %s" % (slot_int, cname, err))
        return False
    et = currentProgram.getEquateTable()
    createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
    eq = et.getEquate(cname)
    if eq is None:
        eq = et.createEquate(cname, value)
    eq.addReference(_addr(slot_int), 0)
    print("[EQ ok] 0x%08x -> %s (%s=0x%x)" % (slot_int, label, cname, value))
    return True


def _apply_ref(slot_addr_int, target_int, gas_label, slot_label):
    """Create USER_DEFINED label at target + DATA ref from slot + slot label."""
    sa = _addr(slot_addr_int)
    ta = _addr(target_int)
    sym_tbl = currentProgram.getSymbolTable()
    ref_mgr = currentProgram.getReferenceManager()

    tgt_names = [s.getName() for s in sym_tbl.getSymbols(ta)]
    if gas_label not in tgt_names:
        sym_tbl.createLabel(ta, gas_label, SourceType.USER_DEFINED)

    ref_mgr.addMemoryReference(sa, ta, RefType.DATA, SourceType.USER_DEFINED, 0)
    for ref in ref_mgr.getReferencesFrom(sa):
        if ref.getToAddress().equals(ta):
            ref_mgr.setPrimary(ref, True)

    slot_names = [s.getName() for s in sym_tbl.getSymbols(sa)]
    if slot_label not in slot_names:
        sym_tbl.createLabel(sa, slot_label, SourceType.USER_DEFINED)

    print("[REF] 0x%08x -> 0x%08x  %s  slot=%s" % (slot_addr_int, target_int, gas_label, slot_label))


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== DisassembleF09Seg1R2Cluster2 (DRY=%s) ===" % DRY)
    print("  Remediates [0x0806f85e..0x0806ff0a)")
    print("  9 ROM_INCBIN + 11 .byte blocks -> full THUMB disasm")
    print("  18 EQ + 2 REF slots applied after disasm")

    if DRY:
        print("[dry] CLUSTER-2A steps: A1(B2g shared epilogue) A2(B2f) A2b(B2a) A3(B2e) A4(B2d) A5(B2c) A6(B5) A7(B4) A8(B3) A9(B2) A10(B1 multi-pass)")
        print("[dry] CLUSTER-2B steps: B1(B7g shared epilogue) B2(B7f) B3(B7e) B4(B7d) B5(B7c) B6(B9) B7(B8) B8(B7) B9(B6)")
        print("[dry] EQ_SLOTS=%d REF_SLOTS=%d" % (len(EQ_SLOTS), len(REF_SLOTS)))
        return

    # =======================================================================
    # CLUSTER-2A: Destiny Board dispatch cluster
    # =======================================================================
    print("\n=== CLUSTER-2A: Destiny Board dispatch cluster ===")

    # -----------------------------------------------------------------------
    # Step A1: B2g -- equip_lp_sub_fb76 body (shared epilogue) FIRST
    #   .byte 0x10 @ 0x6fb78..0x6fb87 (entry movs r0,#0 @ 0x6fb76 already decoded)
    #   Creates LAB_0806fb78 as branch target for all Cluster-2A stubs
    # -----------------------------------------------------------------------
    print("\n--- Step A1: B2g equip_lp_sub_fb76 body (shared epilogue) ---")
    _clear_listing(0x0806fb78, 0x0806fb87)
    _set_tmode(0x0806fb78, 0x0806fb87)
    _disasm_at(0x0806fb78, 0x0806fb87, 'equip_lp_sub_fb76_body')
    n = _count_instrs(0x0806fb78, 0x0806fb87)
    print("    [check] %d instructions in B2g (expect 8)" % n)

    # -----------------------------------------------------------------------
    # Step A2: B2f -- equip_lp_sub_fb70 body
    #   .byte 0x4 @ 0x6fb72..0x6fb75 (entry adds r0,r6,#0 @ 0x6fb70 already decoded)
    #   BL enqueue_lp_counter_sprite_by_player; falls through to equip_lp_sub_fb76
    # -----------------------------------------------------------------------
    print("\n--- Step A2: B2f equip_lp_sub_fb70 body ---")
    _clear_listing(0x0806fb72, 0x0806fb75)
    _set_tmode(0x0806fb72, 0x0806fb75)
    _disasm_at(0x0806fb72, 0x0806fb75, 'equip_lp_sub_fb70_body')
    n = _count_instrs(0x0806fb72, 0x0806fb75)
    print("    [check] %d instructions in B2f (expect 2: BL + fallthrough)" % n)

    # -----------------------------------------------------------------------
    # Step A2b: B2a -- equip_lp_sub_fa4c body (added per review #1)
    #   .byte 0x10 @ 0x6fa4e..0x6fa5d (entry lsls r0,r5,#0x1f @ 0x6fa4c already decoded)
    #   7 instrs: lsrs r0,r0,#31; mov r1,r8; ldrh r2,[r1,#0]; movs r1,#6;
    #   BL init_effect_slot_display_context; movs r0,#0x7e; b LAB_0806fb78
    #   Must execute after Step A1 (LAB_0806fb78 must exist)
    # -----------------------------------------------------------------------
    print("\n--- Step A2b: B2a equip_lp_sub_fa4c body (review addition) ---")
    _clear_listing(0x0806fa4e, 0x0806fa5d)
    _set_tmode(0x0806fa4e, 0x0806fa5d)
    _disasm_at(0x0806fa4e, 0x0806fa5d, 'equip_lp_sub_fa4c_body')
    n = _count_instrs(0x0806fa4e, 0x0806fa5d)
    print("    [check] %d instructions in B2a (expect 7)" % n)

    # -----------------------------------------------------------------------
    # Step A3: B2e -- equip_lp_sub_fb64 body
    #   .byte 0xa @ 0x6fb66..0x6fb6f (entry adds r0,r6,#0 @ 0x6fb64 already decoded)
    #   5 instrs: movs r1,#0; BL check_zone_eligible_with_deck_flag+2; movs r0,#0x64; b LAB_0806fb78
    # -----------------------------------------------------------------------
    print("\n--- Step A3: B2e equip_lp_sub_fb64 body ---")
    _clear_listing(0x0806fb66, 0x0806fb6f)
    _set_tmode(0x0806fb66, 0x0806fb6f)
    _disasm_at(0x0806fb66, 0x0806fb6f, 'equip_lp_sub_fb64_body')
    n = _count_instrs(0x0806fb66, 0x0806fb6f)
    print("    [check] %d instructions in B2e (expect 4-5)" % n)

    # -----------------------------------------------------------------------
    # Step A4: B2d -- equip_lp_sub_fb58 body
    #   .byte 0xa @ 0x6fb5a..0x6fb63 (entry movs r0,#1 @ 0x6fb58 already decoded)
    #   5 instrs: subs r0,r0,r6; BL set_lp_row_type7_if_opponent_linked; movs r0,#0x76; b LAB_0806fb78
    # -----------------------------------------------------------------------
    print("\n--- Step A4: B2d equip_lp_sub_fb58 body ---")
    _clear_listing(0x0806fb5a, 0x0806fb63)
    _set_tmode(0x0806fb5a, 0x0806fb63)
    _disasm_at(0x0806fb5a, 0x0806fb63, 'equip_lp_sub_fb58_body')
    n = _count_instrs(0x0806fb5a, 0x0806fb63)
    print("    [check] %d instructions in B2d (expect 4-5)" % n)

    # -----------------------------------------------------------------------
    # Step A5: B2c -- equip_lp_sub_fb4c body
    #   .byte 0xa @ 0x6fb4e..0x6fb57 (entry adds r0,r6,#0 @ 0x6fb4c already decoded)
    #   5 instrs: movs r1,#1; BL check_zone_eligible_with_deck_flag; movs r0,#0x77; b LAB_0806fb78
    # -----------------------------------------------------------------------
    print("\n--- Step A5: B2c equip_lp_sub_fb4c body ---")
    _clear_listing(0x0806fb4e, 0x0806fb57)
    _set_tmode(0x0806fb4e, 0x0806fb57)
    _disasm_at(0x0806fb4e, 0x0806fb57, 'equip_lp_sub_fb4c_body')
    n = _count_instrs(0x0806fb4e, 0x0806fb57)
    print("    [check] %d instructions in B2c (expect 4-5)" % n)

    # -----------------------------------------------------------------------
    # Step A6: B5 -- equip_lp_sub_fb14 body
    #   ROM_INCBIN 0x6fb16/0x32 -> [0x0806fb16, 0x0806fb47]
    #   Stop BEFORE pool at 0x6fb48 (OAM_EQUIP_LP_SPRITE_P1_5E)
    #   createDWord(0x6fb48) after disasm
    # -----------------------------------------------------------------------
    print("\n--- Step A6: B5 equip_lp_sub_fb14 body ---")
    print("    ROM_INCBIN 0x6fb16/0x32; pool at 0x6fb48 (OAM_EQUIP_LP_SPRITE_P1_5E) OUTSIDE clearListing")
    _clear_listing(0x0806fb16, 0x0806fb47)
    _set_tmode(0x0806fb16, 0x0806fb47)
    _disasm_at(0x0806fb16, 0x0806fb47, 'equip_lp_sub_fb14_body')
    n = _count_instrs(0x0806fb16, 0x0806fb47)
    print("    [check] %d instructions in B5" % n)
    print("    Creating DWORD @ 0x6fb48 (OAM_EQUIP_LP_SPRITE_P1_5E=0x805e)")
    _force_dword(0x0806fb48)

    # -----------------------------------------------------------------------
    # Step A7: B4 -- equip_lp_sub_fa74 body
    #   ROM_INCBIN 0x6fa78/0x8c -> [0x0806fa78, 0x0806fb03]
    #   Stop BEFORE pools at 0x6fb04..0x6fb13
    #   4 createDWords after disasm: fb04/fb08/fb0c/fb10
    # -----------------------------------------------------------------------
    print("\n--- Step A7: B4 equip_lp_sub_fa74 body ---")
    print("    ROM_INCBIN 0x6fa78/0x8c; pools at 0x6fb04..0x6fb13 OUTSIDE clearListing")
    _clear_listing(0x0806fa78, 0x0806fb03)
    _set_tmode(0x0806fa78, 0x0806fb03)
    _disasm_at(0x0806fa78, 0x0806fb03, 'equip_lp_sub_fa74_body')
    n = _count_instrs(0x0806fa78, 0x0806fb03)
    print("    [check] %d instructions in B4" % n)
    print("    Creating DWORDs @ 0x6fb04/0x6fb08/0x6fb0c/0x6fb10")
    _force_dword(0x0806fb04)
    _force_dword(0x0806fb08)
    _force_dword(0x0806fb0c)
    _force_dword(0x0806fb10)

    # -----------------------------------------------------------------------
    # Step A8: B3 -- equip_lp_sub_fa5e body
    #   ROM_INCBIN 0x6fa62/0x12 -> [0x0806fa62, 0x0806fa73]
    #   9 instrs: cmp+beq, cmp+beq, b equip_lp_sub_fb76, movs r0,#0x7d, b LAB_0806fb78,
    #             movs r0,#0x7c, b LAB_0806fb78
    #   (entry bl get_current_slot_palette_color_index @ 0x6fa5e already decoded)
    # -----------------------------------------------------------------------
    print("\n--- Step A8: B3 equip_lp_sub_fa5e body ---")
    _clear_listing(0x0806fa62, 0x0806fa73)
    _set_tmode(0x0806fa62, 0x0806fa73)
    _disasm_at(0x0806fa62, 0x0806fa73, 'equip_lp_sub_fa5e_body')
    n = _count_instrs(0x0806fa62, 0x0806fa73)
    print("    [check] %d instructions in B3 (expect 7-9)" % n)

    # -----------------------------------------------------------------------
    # Step A9: B2 -- eligible_sub_stubs_fa08 body
    #   ROM_INCBIN 0x6fa0a/0x36 -> [0x0806fa0a, 0x0806fa3f]
    #   b+pad at 0x6fa40..0x6fa43 (0x0000e09a = b to 0x6fb78 + .zero 2)
    #   clearListing includes b+pad: 0x6fa0a..0x6fa43
    #   Stop BEFORE pools at 0x6fa44 (gDuelPhaseFlags) and 0x6fa48 (EQUIP_PHASE_FRAME_OFF)
    #   which are already in asm as .word entries - DO NOT createDWord
    # -----------------------------------------------------------------------
    print("\n--- Step A9: B2 eligible_sub_stubs_fa08 body + b+pad ---")
    print("    ROM_INCBIN 0x6fa0a/0x36 + b+pad @0x6fa40..0x6fa43")
    print("    Pools at 0x6fa44/0x6fa48 are OUTSIDE range and already in asm -- not cleared")
    _clear_listing(0x0806fa0a, 0x0806fa43)
    _set_tmode(0x0806fa0a, 0x0806fa43)
    _disasm_at(0x0806fa0a, 0x0806fa43, 'eligible_sub_stubs_fa08_body')
    n = _count_instrs(0x0806fa0a, 0x0806fa43)
    print("    [check] %d instructions in B2 (expect ~18-22 including b+pad decode)" % n)

    # -----------------------------------------------------------------------
    # Step A10: B1 -- eligible_destiny_board_f85c body (LARGEST BLOCK)
    #   ROM_INCBIN 0x6f85e/0x136 -> [0x0806f85e, 0x0806f993]
    #   Multi-pass approach due to ldr+b+.word CID pattern:
    #     a) clearListing(0x6f85e..0x6f953) then DisassembleCommand(0x6f85e)
    #        Flow stops at b @ 0x6f952 (after ldr r3,[pc,#0])
    #     b) createDWord for the 3 early pools: 0x6f92c/30/34
    #     c) createDWord(0x6f954) then DisassembleCommand(0x6f958) [resume after I CID]
    #     d) createDWord(0x6f95c) then DisassembleCommand(0x6f960) [resume after N CID]
    #     e) createDWord(0x6f964) then DisassembleCommand(0x6f968) [resume after A CID]
    #     f) After flow reaches 0x6f982..0x6f993:
    #        createDWord for remaining pools: 0x6f988/8c/90
    #     g) REF for pool 0x6f990 -> equip_lp_disp_table_f994
    # -----------------------------------------------------------------------
    print("\n--- Step A10: B1 eligible_destiny_board_f85c body (multi-pass) ---")
    print("    ROM_INCBIN 0x6f85e/0x136; 9 pools inside range")
    print("    Multi-pass due to ldr+b+.word CID triplet pattern at 0x6f950..0x6f967")

    # Phase a: clear code region up to first CID pool, disasm from entry
    print("    Phase a: clearListing 0x6f85e..0x6f953, disasm from 0x6f85e")
    _clear_listing(0x0806f85e, 0x0806f953)
    _set_tmode(0x0806f85e, 0x0806f993)
    _disasm_at(0x0806f85e, 0x0806f993, 'eligible_destiny_board_f85c_phase_a')
    # Phase b: createDWord for pools 0x6f92c/30/34 (inside ROM_INCBIN, before CID triplet)
    print("    Phase b: createDWord pools 0x6f92c/30/34")
    _force_dword(0x0806f92c)
    _force_dword(0x0806f930)
    _force_dword(0x0806f934)
    # Phase c: CID I pool at 0x6f954; then resume disasm from 0x6f958
    print("    Phase c: createDWord 0x6f954 (SPIRIT_MESSAGE_I_CID), resume disasm 0x6f958")
    _force_dword(0x0806f954)
    _disasm_at(0x0806f958, 0x0806f993, 'eligible_destiny_board_f85c_phase_c')
    # Phase d: CID N pool at 0x6f95c; then resume disasm from 0x6f960
    print("    Phase d: createDWord 0x6f95c (SPIRIT_MESSAGE_N_CID), resume disasm 0x6f960")
    _force_dword(0x0806f95c)
    _disasm_at(0x0806f960, 0x0806f993, 'eligible_destiny_board_f85c_phase_d')
    # Phase e: CID A pool at 0x6f964; then resume disasm from 0x6f968
    print("    Phase e: createDWord 0x6f964 (SPIRIT_MESSAGE_A_CID), resume disasm 0x6f968")
    _force_dword(0x0806f964)
    _disasm_at(0x0806f968, 0x0806f993, 'eligible_destiny_board_f85c_phase_e')
    # Phase f: remaining pools 0x6f988/8c/90
    print("    Phase f: createDWord remaining pools 0x6f988/8c/90")
    _force_dword(0x0806f988)
    _force_dword(0x0806f98c)
    _force_dword(0x0806f990)
    n = _count_instrs(0x0806f85e, 0x0806f993)
    print("    [check] %d instructions in B1 code region" % n)

    # =======================================================================
    # CLUSTER-2B: Cathedral of Nobles dispatch cluster
    # =======================================================================
    print("\n=== CLUSTER-2B: Cathedral of Nobles dispatch cluster ===")

    # -----------------------------------------------------------------------
    # Step B1: B7g -- equip_chain_act_sub_ff46 body (shared epilogue) FIRST
    #   .byte 0x4 @ 0x6ff48..0x6ff4b (entry movs r0,#0 @ 0x6ff46 already decoded)
    #   .word 0x00004708 @ 0x6ff4c (bx r1 + .zero 2) -> clearListing both ranges
    #   Creates LAB_0806ff48 as branch target for all Cluster-2B stubs
    # -----------------------------------------------------------------------
    print("\n--- Step B1: B7g equip_chain_act_sub_ff46 body (shared epilogue) ---")
    _clear_listing(0x0806ff48, 0x0806ff4b)
    _clear_listing(0x0806ff4c, 0x0806ff4f)
    _set_tmode(0x0806ff48, 0x0806ff4f)
    _disasm_at(0x0806ff48, 0x0806ff4f, 'equip_chain_act_sub_ff46_body')
    n = _count_instrs(0x0806ff48, 0x0806ff4f)
    print("    [check] %d instructions in B7g (expect 3: pop r4, pop r1, bx r1)" % n)

    # -----------------------------------------------------------------------
    # Step B2: B7f -- equip_chain_act_sub_ff3c body
    #   .byte 0x8 @ 0x6ff3e..0x6ff45 (entry ldrb r4,[r4,#2] @ 0x6ff3c already decoded)
    #   lsls r0,r4,#0x1f; lsrs r0,r0,#0x1f; BL enqueue_lp_counter_sprite_by_player
    #   (falls through to equip_chain_act_sub_ff46 movs r0,#0)
    # -----------------------------------------------------------------------
    print("\n--- Step B2: B7f equip_chain_act_sub_ff3c body ---")
    _clear_listing(0x0806ff3e, 0x0806ff45)
    _set_tmode(0x0806ff3e, 0x0806ff45)
    _disasm_at(0x0806ff3e, 0x0806ff45, 'equip_chain_act_sub_ff3c_body')
    n = _count_instrs(0x0806ff3e, 0x0806ff45)
    print("    [check] %d instructions in B7f (expect 3)" % n)

    # -----------------------------------------------------------------------
    # Step B3: B7e -- equip_chain_act_sub_ff2c body
    #   .byte 0xe @ 0x6ff2e..0x6ff3b (entry ldrb r4,[r4,#2] @ 0x6ff2c already decoded)
    #   lsls r0,r4,#0x1f; lsrs r0,r0,#0x1f; movs r1,#0; BL check_zone_eligible_with_deck_flag;
    #   movs r0,#0x64; b LAB_0806ff48
    # -----------------------------------------------------------------------
    print("\n--- Step B3: B7e equip_chain_act_sub_ff2c body ---")
    _clear_listing(0x0806ff2e, 0x0806ff3b)
    _set_tmode(0x0806ff2e, 0x0806ff3b)
    _disasm_at(0x0806ff2e, 0x0806ff3b, 'equip_chain_act_sub_ff2c_body')
    n = _count_instrs(0x0806ff2e, 0x0806ff3b)
    print("    [check] %d instructions in B7e (expect 6)" % n)

    # -----------------------------------------------------------------------
    # Step B4: B7d -- equip_chain_act_sub_ff1a body
    #   .byte 0x10 @ 0x6ff1c..0x6ff2b (entry ldrb r4,[r4,#2] @ 0x6ff1a already decoded)
    #   lsls r1,r4,#0x1f; lsrs r1,r1,#0x1f; movs r0,#1; subs r0,r0,r1;
    #   BL set_lp_row_type7_if_opponent_linked; movs r0,#0x6c; b LAB_0806ff48
    # -----------------------------------------------------------------------
    print("\n--- Step B4: B7d equip_chain_act_sub_ff1a body ---")
    _clear_listing(0x0806ff1c, 0x0806ff2b)
    _set_tmode(0x0806ff1c, 0x0806ff2b)
    _disasm_at(0x0806ff1c, 0x0806ff2b, 'equip_chain_act_sub_ff1a_body')
    n = _count_instrs(0x0806ff1c, 0x0806ff2b)
    print("    [check] %d instructions in B7d (expect 7)" % n)

    # -----------------------------------------------------------------------
    # Step B5: B7c -- equip_chain_act_sub_ff0a body
    #   .byte 0xe @ 0x6ff0c..0x6ff19 (entry ldrb r4,[r4,#2] @ 0x6ff0a already decoded)
    #   lsls r0,r4,#0x1f; lsrs r0,r0,#0x1f; movs r1,#1;
    #   BL check_zone_eligible_with_deck_flag; movs r0,#0x6d; b LAB_0806ff48
    # -----------------------------------------------------------------------
    print("\n--- Step B5: B7c equip_chain_act_sub_ff0a body ---")
    _clear_listing(0x0806ff0c, 0x0806ff19)
    _set_tmode(0x0806ff0c, 0x0806ff19)
    _disasm_at(0x0806ff0c, 0x0806ff19, 'equip_chain_act_sub_ff0a_body')
    n = _count_instrs(0x0806ff0c, 0x0806ff19)
    print("    [check] %d instructions in B7c (expect 6)" % n)

    # -----------------------------------------------------------------------
    # Step B6: B9 -- equip_chain_act_sub_fef0 body
    #   ROM_INCBIN 0x6fef2/0x18 -> [0x0806fef2, 0x0806ff09]
    #   (entry ldrb r4,[r4,#2] @ 0x6fef0 already decoded)
    #   lsls r4,r4,#0x1f; lsrs r4,r4,#0x1f; BL get_monster_slot_entry_ptr;
    #   adds r1,r0,#0; adds r0,r4,#0; movs r2,#1; movs r3,#0;
    #   BL invoke_setup_equip_oam_with_attr2; movs r0,#0x64; b LAB_0806ff48
    # -----------------------------------------------------------------------
    print("\n--- Step B6: B9 equip_chain_act_sub_fef0 body ---")
    _clear_listing(0x0806fef2, 0x0806ff09)
    _set_tmode(0x0806fef2, 0x0806ff09)
    _disasm_at(0x0806fef2, 0x0806ff09, 'equip_chain_act_sub_fef0_body')
    n = _count_instrs(0x0806fef2, 0x0806ff09)
    print("    [check] %d instructions in B9 (expect 10-12)" % n)

    # -----------------------------------------------------------------------
    # Step B7: B8 -- equip_chain_act_sub_fedc body
    #   ROM_INCBIN 0x6fede/0x12 -> [0x0806fede, 0x0806feef]
    #   (entry ldrb r1,[r4,#2] @ 0x6fedc already decoded)
    #   lsls r0,r1,#0x1f; lsrs r0,r0,#0x1f; ldrh r2,[r4,#0]; movs r1,#6; movs r3,#0;
    #   BL init_effect_slot_display_context; movs r0,#0x7e; b LAB_0806ff48
    # -----------------------------------------------------------------------
    print("\n--- Step B7: B8 equip_chain_act_sub_fedc body ---")
    _clear_listing(0x0806fede, 0x0806feef)
    _set_tmode(0x0806fede, 0x0806feef)
    _disasm_at(0x0806fede, 0x0806feef, 'equip_chain_act_sub_fedc_body')
    n = _count_instrs(0x0806fede, 0x0806feef)
    print("    [check] %d instructions in B8 (expect 8-9)" % n)

    # -----------------------------------------------------------------------
    # Step B8: B7 -- eligible_sub_stubs_fe88 body + b+pad
    #   ROM_INCBIN 0x6fe8a/0x4a -> [0x0806fe8a, 0x0806fed3]
    #   b+pad at 0x6fed4..0x6fed7 (0x0000e038 = b to 0x6ff48 + .zero 2)
    #   clearListing includes b+pad: 0x6fe8a..0x6fed7
    #   Stop BEFORE pool at 0x6fed8 (CARD_DISPLAY_OP31_LP_BAR_SUB=0x011d)
    #   createDWord(0x6fed8) after disasm
    #   (entry ldrb r1,[r4,#2] @ 0x6fe88 already decoded)
    # -----------------------------------------------------------------------
    print("\n--- Step B8: B7 eligible_sub_stubs_fe88 body + b+pad ---")
    print("    ROM_INCBIN 0x6fe8a/0x4a + b+pad @0x6fed4..0x6fed7")
    print("    Pool at 0x6fed8 (CARD_DISPLAY_OP31_LP_BAR_SUB=0x011d) OUTSIDE clearListing")
    _clear_listing(0x0806fe8a, 0x0806fed7)
    _set_tmode(0x0806fe8a, 0x0806fed7)
    _disasm_at(0x0806fe8a, 0x0806fed7, 'eligible_sub_stubs_fe88_body')
    n = _count_instrs(0x0806fe8a, 0x0806fed7)
    print("    [check] %d instructions in B7 (expect ~22)" % n)
    print("    Creating DWORD @ 0x6fed8 (CARD_DISPLAY_OP31_LP_BAR_SUB=0x011d)")
    _force_dword(0x0806fed8)

    # -----------------------------------------------------------------------
    # Step B9: B6 -- eligible_cathedral_of_nobles_fdec body
    #   ROM_INCBIN 0x6fdee/0x26 -> [0x0806fdee, 0x0806fe0b]
    #   Stop BEFORE pools at 0x6fe0c (gDuelPhaseFlags) and 0x6fe10 (equip_chain_act_disp_table_fe14)
    #   createDWord for both pools after disasm
    #   (entry push {r4,lr} @ 0x6fdec already decoded)
    # -----------------------------------------------------------------------
    print("\n--- Step B9: B6 eligible_cathedral_of_nobles_fdec body ---")
    print("    ROM_INCBIN 0x6fdee/0x26; pools at 0x6fe0c/0x6fe10 OUTSIDE clearListing")
    _clear_listing(0x0806fdee, 0x0806fe0b)
    _set_tmode(0x0806fdee, 0x0806fe0b)
    _disasm_at(0x0806fdee, 0x0806fe0b, 'eligible_cathedral_of_nobles_fdec_body')
    n = _count_instrs(0x0806fdee, 0x0806fe0b)
    print("    [check] %d instructions in B6 (expect 15)" % n)
    print("    Creating DWORDs @ 0x6fe0c (gDuelPhaseFlags) + 0x6fe10 (equip_chain_act_disp_table_fe14)")
    _force_dword(0x0806fe0c)
    _force_dword(0x0806fe10)

    # =======================================================================
    # EQ_SLOTS: Apply equates to all pool DWORDs
    # =======================================================================
    print("\n=== EQ_SLOTS: Applying %d equate slots ===" % len(EQ_SLOTS))
    nEQ = 0
    for slot_int, value, cname, label in EQ_SLOTS:
        if _apply_eq(slot_int, value, cname, label):
            nEQ += 1
    print("[EQ] Applied %d/%d equates" % (nEQ, len(EQ_SLOTS)))

    # =======================================================================
    # REF_SLOTS: Apply DATA refs for dispatch table pointers
    # =======================================================================
    print("\n=== REF_SLOTS: Applying %d ref slots ===" % len(REF_SLOTS))
    for slot_addr_int, target_int, gas_label, slot_label in REF_SLOTS:
        _apply_ref(slot_addr_int, target_int, gas_label, slot_label)

    # =======================================================================
    # Summary
    # =======================================================================
    print("\n=== DisassembleF09Seg1R2Cluster2 DONE ===")
    print("  CLUSTER-2A blocks: B2g/B2f/B2a/B2e/B2d/B2c/B5/B4/B3/B2/B1")
    print("  CLUSTER-2B blocks: B7g/B7f/B7e/B7d/B7c/B9/B8/B7/B6")
    print("  EQ_SLOTS=%d REF_SLOTS=%d" % (len(EQ_SLOTS), len(REF_SLOTS)))
    print("  9 ROM_INCBIN + 11 .byte -> DISASM; b+pad words decoded byte-identical")
    print("  NEW constants (must be in .inc files):")
    print("    SPIRIT_MESSAGE_N_CID=0x1498, SPIRIT_MESSAGE_A_CID=0x1499 (card_info.inc)")
    print("    OAM_EQUIP_LP_SPRITE_P1_5E=0x805e (oam_attr.inc)")
    print("    CARD_DISPLAY_OP31_LP_BAR_SUB=0x011d (card_info.inc)")


main()
