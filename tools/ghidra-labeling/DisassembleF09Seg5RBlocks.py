# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF09Seg5RBlocks.py -- F09 Seg-5 REMEDIATION
#   Eliminates 2 ROM_INCBIN + 7 .byte CODE + 3 .byte DATA blocks in [0x08072d20..0x08074338).
#   See doc/dev/refine/F09-Seg5R.proposal.md for full analysis.
#
#   NO new constants (only REUSE: CARD_DISPLAY_OP31_LP_BAR_SUB in card_info.inc:1496).
#
#   Execution order:
#   Step 1: DATA .byte -> createDWord FIRST (3 slots):
#     0x08073168 -> .word trap_dustshoot_sub_3290  (dispatch table[0])
#     0x080735b4 -> .word machine_dup_sub_374c      (dispatch table[0])
#     0x0807388c -> .word cat_ill_omen_sub_3a46     (dispatch table[0])
#   Step 2: EQ_SLOT annotation (1 slot REUSE):
#     0x0807368c pool_b4_368c -> CARD_DISPLAY_OP31_LP_BAR_SUB=0x011d (card_info.inc:1496)
#   Step 3: CODE blocks -> DisassembleCommand in address order:
#     A1 @ 0x08073156/0x0a  bls-taken indirect dispatch in fn_eligible_trap_dustshoot_3140
#     B1 @ 0x08073218/0x12  bne-taken in trap_dustshoot_dispatch_sub_stubs_31e4
#     A2 @ 0x0807326c/0x04  entry stub trap_dustshoot_sub_326c
#     A3 @ 0x0807359e/0x0a  bls-taken indirect dispatch in fn_eligible_machine_dup_and_league_356c
#     B2 @ 0x08073636/0x56  bne-taken in machine_dup_dispatch_sub_stubs_3628 (2-path bne)
#     A4 @ 0x08073732/0x08  bcs-taken in machine_dup_sub_3704
#     A5 @ 0x0807387a/0x0a  bls-taken indirect dispatch in fn_eligible_cat_ill_omen_and_owl_of_luck
#     A6 @ 0x08073922/0x10  bne-taken in cat_ill_omen_dispatch_sub_stubs_3900
#     A7 @ 0x08073d30/0x0e  beq-taken in reasoning_dispatch_sub_stubs_3bc8 (2 beq sources)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).
# NOTE: No new function labels created; all CODE blocks are intra-function LAB_ continuations.
# NOTE: Ordering: DATA createDWord before CODE disasm to prevent Ghidra treating table entries as code.
# NOTE: clearListing ranges use [lo, hi-1] inclusive (end address = last byte of block).

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
# pool_b4_368c @ 0x7368c holds CARD_DISPLAY_OP31_LP_BAR_SUB=0x011d
# Label stays pool_b4_368c (not renamed to equate name: Seg-4R lesson)
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # REUSE card_info.inc:1496 -- pool_b4_368c @ 0x7368c
    (0x0807368c, 0x0000011d, 'CARD_DISPLAY_OP31_LP_BAR_SUB', 'pool_b4_368c'),
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
    """Clear listing [lo_int .. hi_int] inclusive (both are byte addresses)."""
    lo = _addr(lo_int)
    hi = _addr(hi_int)
    try:
        clearListing(lo, hi)
        print("[ok ] clearListing 0x%08x..0x%08x" % (lo_int, hi_int))
    except Exception as e:
        print("[warn] clearListing 0x%08x..0x%08x: %s" % (lo_int, hi_int, e))


def _disasm_at(stub_lo_int, label):
    lo = _addr(stub_lo_int)
    cmd = DisassembleCommand(lo, None, True)
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


def _count_instrs(lo_int, hi_int):
    """Count instructions in range [lo_int..hi_int] inclusive."""
    listing = currentProgram.getListing()
    lo_a = _addr(lo_int)
    hi_a = _addr(hi_int)
    n = 0
    inst = listing.getInstructionAt(lo_a)
    while inst is not None and inst.getAddress().compareTo(hi_a) <= 0:
        n += 1
        inst = listing.getInstructionAfter(inst.getAddress())
    return n


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== DisassembleF09Seg5RBlocks (DRY=%s) ===" % DRY)
    print("  Remediates [0x08072d20..0x08074338) Seg-5 range")
    print("  2 ROM_INCBIN + 7 .byte CODE + 3 .byte DATA -> full THUMB disasm + DWORDs")
    print("  EQ_SLOTS=%d (1 REUSE: CARD_DISPLAY_OP31_LP_BAR_SUB)" % len(EQ_SLOTS))

    if DRY:
        print("[dry] Step 1: force_dword 0x73168 / 0x735b4 / 0x7388c")
        print("[dry] Step 2: EQ pool_b4_368c @ 0x7368c -> CARD_DISPLAY_OP31_LP_BAR_SUB=0x011d")
        print("[dry] Step 3: CODE A1@0x73156 B1@0x73218 A2@0x7326c A3@0x7359e B2@0x73636 A4@0x73732 A5@0x7387a A6@0x73922 A7@0x73d30")
        return

    # =======================================================================
    # Step 1: DATA .byte -> createDWord FIRST
    # Must precede all DC calls to prevent Ghidra treating table entry[0] as code
    # =======================================================================
    print("\n=== Step 1: DATA .byte -> createDWord ===")

    print("  [1a] 0x73168 -> .word trap_dustshoot_sub_3290 (dispatch table[0])")
    _force_dword(0x08073168)

    print("  [1b] 0x735b4 -> .word machine_dup_sub_374c (dispatch table[0])")
    _force_dword(0x080735b4)

    print("  [1c] 0x7388c -> .word cat_ill_omen_sub_3a46 (dispatch table[0])")
    _force_dword(0x0807388c)

    # =======================================================================
    # Step 2: EQ_SLOTS
    # pool_b4_368c @ 0x7368c is already a .word in asm; apply equate only
    # =======================================================================
    print("\n=== Step 2: EQ_SLOTS (%d) ===" % len(EQ_SLOTS))
    nEQ = 0
    for slot_int, value, cname, label in EQ_SLOTS:
        if _apply_eq(slot_int, value, cname, label):
            nEQ += 1
    print("[EQ] Applied %d/%d equates" % (nEQ, len(EQ_SLOTS)))

    # =======================================================================
    # Step 3: CODE blocks -> DisassembleCommand (address order)
    # =======================================================================
    print("\n=== Step 3: CODE blocks ===")

    # -----------------------------------------------------------------------
    # A1: bls-taken indirect dispatch in fn_eligible_trap_dustshoot_3140
    #   .byte 0x0a @ 0x73156..0x7315f
    #   bls LAB_08073156 at 0x8073152 (phase_code-0x62 <= 0x1e -> valid dispatch)
    #   5 halfwords: lsls r0,r0,#2; ldr r1,[pc,#8]; adds r0,r0,r1; ldr r0,[r0,#0]; mov r15,r0
    #   pool_b1_3164 @ 0x73164 = 0x08073168 = trap_dustshoot_dispatch_table_3168 (OUTSIDE range)
    # -----------------------------------------------------------------------
    print("\n--- A1: fn_eligible_trap_dustshoot_3140 indirect dispatch ---")
    print("  .byte 0x0a @ 0x73156..0x7315f; pool_b1_3164 @ 0x73164 OUTSIDE range")
    _clear_listing(0x08073156, 0x0807315f)
    _set_tmode(0x08073156, 0x0807315f)
    _disasm_at(0x08073156, 'A1_trap_dustshoot_dispatch')
    n = _count_instrs(0x08073156, 0x0807315f)
    print("  [check] %d instructions in A1 (expect 5)" % n)

    # -----------------------------------------------------------------------
    # B1: bne-taken path in trap_dustshoot_dispatch_sub_stubs_31e4
    #   ROM_INCBIN 0x73218/0x12 -> [0x08073218, 0x08073229]
    #   bne LAB_08073218 at 0x807320a (count_field_zone_cards_with_field5 returned nonzero)
    #   9 halfwords: ldrb r1,[r7,#2]; lsls r0,r1,#31; lsrs r0,r0,#31; ldrh r1,[r7,#0];
    #                movs r2,#1; BL set_lp_display_row_type5(0x080a1c2c); movs r0,#0x7f;
    #                b trap_dustshoot_default_32a0
    #   pools pool_b2_3210/3214 OUTSIDE range (at 0x73210/0x73214)
    # -----------------------------------------------------------------------
    print("\n--- B1: trap_dustshoot_dispatch_sub_stubs_31e4 bne-taken path ---")
    print("  ROM_INCBIN 0x73218/0x12; BL target: 0x080a1c2c = set_lp_display_row_type5")
    print("  pools pool_b2_3210/3214 OUTSIDE range")
    _clear_listing(0x08073218, 0x08073229)
    _set_tmode(0x08073218, 0x08073229)
    _disasm_at(0x08073218, 'B1_trap_dustshoot_bne_path')
    n = _count_instrs(0x08073218, 0x08073229)
    print("  [check] %d instructions in B1 (expect 9)" % n)

    # -----------------------------------------------------------------------
    # A2: entry stub trap_dustshoot_sub_326c
    #   .byte 0x04 @ 0x7326c..0x7326f
    #   raw=1 ref from trap_dustshoot_dispatch_table_3168[2] at 0x73170 = .word trap_dustshoot_sub_326c
    #   2 halfwords: ldrb r7,[r7,#2]; lsls r1,r7,#31
    #   Body at 0x73270..0x7327e already decoded; DC fall-through to existing code
    # -----------------------------------------------------------------------
    print("\n--- A2: trap_dustshoot_sub_326c entry stub ---")
    print("  .byte 0x04 @ 0x7326c..0x7326f; fall-through into decoded body 0x73270")
    _clear_listing(0x0807326c, 0x0807326f)
    _set_tmode(0x0807326c, 0x0807326f)
    _disasm_at(0x0807326c, 'A2_trap_dustshoot_sub_326c_entry')
    n = _count_instrs(0x0807326c, 0x0807326f)
    print("  [check] %d instructions in A2 entry (expect 2)" % n)

    # -----------------------------------------------------------------------
    # A3: bls-taken indirect dispatch in fn_eligible_machine_dup_and_league_356c
    #   .byte 0x0a @ 0x7359e..0x735a7
    #   bls LAB_0807359e at 0x807359a (phase_code-0x64 <= 0x1c -> valid dispatch)
    #   5 halfwords: lsls r0,r0,#2; ldr r1,[pc,#12]; adds r0,r0,r1; ldr r0,[r0,#0]; mov r15,r0
    #   pool_b3_35b0 @ 0x735b0 = 0x080735b4 = machine_dup_dispatch_table_35b4 (OUTSIDE range)
    # -----------------------------------------------------------------------
    print("\n--- A3: fn_eligible_machine_dup_and_league_356c indirect dispatch ---")
    print("  .byte 0x0a @ 0x7359e..0x735a7; pool_b3_35b0 @ 0x735b0 OUTSIDE range")
    _clear_listing(0x0807359e, 0x080735a7)
    _set_tmode(0x0807359e, 0x080735a7)
    _disasm_at(0x0807359e, 'A3_machine_dup_dispatch')
    n = _count_instrs(0x0807359e, 0x080735a7)
    print("  [check] %d instructions in A3 (expect 5)" % n)

    # -----------------------------------------------------------------------
    # B2: bne-taken path in machine_dup_dispatch_sub_stubs_3628
    #   ROM_INCBIN 0x73636/0x56 -> [0x08073636, 0x0807368b]
    #   bne LAB_08073636 at 0x8073632 (check_neo_daedalus_placement_eligible returned nonzero)
    #   2-path bne: 43 halfwords total
    #   NOT-taken: 0x7364c..0x7365a -> b machine_dup_default_3756 (stops DC)
    #   taken:     0x7365c..0x7368a -> b LAB_08073758 (stops DC)
    #   pool_b4_368c @ 0x7368c = CARD_DISPLAY_OP31_LP_BAR_SUB (OUTSIDE range, already .word)
    #   EQ applied in Step 2; clearListing stops at 0x7368b (not 0x7368c)
    # -----------------------------------------------------------------------
    print("\n--- B2: machine_dup_dispatch_sub_stubs_3628 bne-taken path (2-path) ---")
    print("  ROM_INCBIN 0x73636/0x56 -> [0x73636, 0x7368b]")
    print("  pool_b4_368c @ 0x7368c OUTSIDE clearListing range (EQ applied in Step 2)")
    _clear_listing(0x08073636, 0x0807368b)
    _set_tmode(0x08073636, 0x0807368b)
    _disasm_at(0x08073636, 'B2_machine_dup_bne_path')
    n = _count_instrs(0x08073636, 0x0807368b)
    print("  [check] %d instructions in B2 (expect ~38-43 across both paths)" % n)

    # Safety: re-verify pool_b4_368c at 0x7368c was NOT cleared
    d_check = getDataAt(_addr(0x0807368c))
    if d_check is not None and d_check.getLength() == 4:
        print("  [safety] pool_b4_368c @ 0x7368c still intact as 4B DWORD after B2 clear - OK")
    else:
        print("  [warn] pool_b4_368c @ 0x7368c may have been cleared; re-applying force_dword")
        _force_dword(0x0807368c)
        _apply_eq(0x0807368c, 0x0000011d, 'CARD_DISPLAY_OP31_LP_BAR_SUB', 'pool_b4_368c')

    # -----------------------------------------------------------------------
    # A4: bcs-taken path in machine_dup_sub_3704
    #   .byte 0x08 @ 0x73732..0x73739
    #   bcs LAB_08073732 at 0x807370a (slot[8] >= slot[10] -> early return)
    #   4 halfwords: BL decrement_lp_bar_display_counter(0x0804a870);
    #                movs r0,#0x64; b machine_dup_default_3756
    #   No pool words in block range
    # -----------------------------------------------------------------------
    print("\n--- A4: machine_dup_sub_3704 bcs-taken path ---")
    print("  .byte 0x08 @ 0x73732..0x73739; no pool words in block range")
    print("  BL target: 0x0804a870 = decrement_lp_bar_display_counter")
    _clear_listing(0x08073732, 0x08073739)
    _set_tmode(0x08073732, 0x08073739)
    _disasm_at(0x08073732, 'A4_machine_dup_3704_bcs_path')
    n = _count_instrs(0x08073732, 0x08073739)
    print("  [check] %d instructions in A4 (expect 4)" % n)

    # -----------------------------------------------------------------------
    # A5: bls-taken indirect dispatch in fn_eligible_cat_ill_omen_and_owl_of_luck
    #   .byte 0x0a @ 0x7387a..0x73883
    #   bls LAB_0807387a at 0x8073876 (phase_offset <= limit -> valid dispatch)
    #   5 halfwords: lsls r0,r0,#2; ldr r1,[pc,#8]; adds r0,r0,r1; ldr r0,[r0,#0]; mov r15,r0
    #   pool_b5_3888 @ 0x73888 = 0x0807388c = cat_ill_omen_dispatch_table_388c (OUTSIDE range)
    # -----------------------------------------------------------------------
    print("\n--- A5: fn_eligible_cat_ill_omen_and_owl_of_luck indirect dispatch ---")
    print("  .byte 0x0a @ 0x7387a..0x73883; pool_b5_3888 @ 0x73888 OUTSIDE range")
    _clear_listing(0x0807387a, 0x08073883)
    _set_tmode(0x0807387a, 0x08073883)
    _disasm_at(0x0807387a, 'A5_cat_ill_omen_dispatch')
    n = _count_instrs(0x0807387a, 0x08073883)
    print("  [check] %d instructions in A5 (expect 5)" % n)

    # -----------------------------------------------------------------------
    # A6: bne-taken path in cat_ill_omen_dispatch_sub_stubs_3900
    #   .byte 0x10 @ 0x73922..0x73931
    #   bne LAB_08073922 at 0x8073910 (dispatch_effect_handler_by_card_id returned nonzero)
    #   8 halfwords: ldrb r5,[r5,#2]; lsls r0,r5,#31; lsrs r0,r0,#31; movs r1,#0x5e;
    #                BL trigger_card_display_op31_if_not_active(0x08093390); movs r0,#0x7f;
    #                b cat_ill_omen_default_3a54
    #   No pool words in block range
    # -----------------------------------------------------------------------
    print("\n--- A6: cat_ill_omen_dispatch_sub_stubs_3900 bne-taken path ---")
    print("  .byte 0x10 @ 0x73922..0x73931; no pool words in block range")
    print("  BL target: 0x08093390 = trigger_card_display_op31_if_not_active")
    _clear_listing(0x08073922, 0x08073931)
    _set_tmode(0x08073922, 0x08073931)
    _disasm_at(0x08073922, 'A6_cat_ill_omen_3900_bne_path')
    n = _count_instrs(0x08073922, 0x08073931)
    print("  [check] %d instructions in A6 (expect 8)" % n)

    # -----------------------------------------------------------------------
    # A7: beq-taken path in reasoning_dispatch_sub_stubs_3bc8
    #   .byte 0x0e @ 0x73d30..0x73d3d
    #   beq LAB_08073d30 at 0x8073cb8 (check_card_field5_is_nonzero returned 0)
    #   beq LAB_08073d30 at 0x8073cc2 (check_card_not_equip_placement_type returned 0)
    #   (two convergent beq sources -> same target block)
    #   7 halfwords: adds r0,r4,#0; movs r1,#1; movs r2,#0;
    #                BL enqueue_equip_zone_sprite_attr_full(0x080495fc); movs r0,#0x7d;
    #                b LAB_08073d74
    #   No pool words in block range
    # -----------------------------------------------------------------------
    print("\n--- A7: reasoning_dispatch_sub_stubs_3bc8 beq-taken path ---")
    print("  .byte 0x0e @ 0x73d30..0x73d3d; no pool words in block range")
    print("  BL target: 0x080495fc = enqueue_equip_zone_sprite_attr_full")
    print("  Two convergent beq sources: 0x8073cb8 + 0x8073cc2 -> same LAB_08073d30")
    _clear_listing(0x08073d30, 0x08073d3d)
    _set_tmode(0x08073d30, 0x08073d3d)
    _disasm_at(0x08073d30, 'A7_reasoning_3bc8_beq_path')
    n = _count_instrs(0x08073d30, 0x08073d3d)
    print("  [check] %d instructions in A7 (expect 6-7)" % n)

    # =======================================================================
    # Summary
    # =======================================================================
    print("\n=== DisassembleF09Seg5RBlocks DONE ===")
    print("  DATA DWORDs: 3 (.byte -> .word)")
    print("  EQ applied: %d/1 (CARD_DISPLAY_OP31_LP_BAR_SUB REUSE card_info.inc:1496)" % nEQ)
    print("  CODE disasm: A1+B1+A2+A3+B2+A4+A5+A6+A7 = 9 CODE blocks")
    print("  All CODE blocks are intra-function LAB_ continuations; no new functions created")
    print("  Expected Seg-5 ROM_INCBIN residue after export: 0")
    print("  Expected Seg-5 .byte-code residue after export: 0")


main()
