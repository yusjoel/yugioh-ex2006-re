# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF09Seg4RBlocks.py -- F09 Seg-4 REMEDIATION
#   Eliminates 4 ROM_INCBIN + 4 .byte CODE + 4 .byte DATA blocks in [0x080719fc..0x08072d20).
#   See doc/dev/refine/F09-Seg4R.proposal.md for full analysis.
#
#   NO new constants (all REUSE existing ewram.inc + duel_field.inc constants).
#
#   Execution order:
#   Step 1: DATA .byte -> createDWord FIRST (4 slots):
#     0x08072430 -> .word last_turn_sub_2534
#     0x0807257c -> .word vampire_sub_26bc
#     0x08072734 -> .word equip_zone_sub_2856
#     0x08072830 -> .word LP_CARD_TRACK_BASE_OFF (then EQ)
#   Step 2: EQ_SLOTS (2 equates - REUSE existing constants):
#     0x08072830 LP_CARD_TRACK_BASE_OFF=0x1da8 (ewram.inc:247)
#     0x080727b4 lookup_equip_score_b_0x1b9=0x1b9 (duel_field.inc:332)
#   Step 3: .byte CODE blocks -> DisassembleCommand (4 blocks):
#     C1 @ 0x08071f74/0xc  bls-taken in fn_eligible_fengsheng_mirror_1f58
#     C2 @ 0x0807241c/0xc  bls-taken in fn_eligible_fiend_comedian_2404
#     C3 @ 0x0807256a/0xa  bls-taken in fn_eligible_last_turn_2540
#     C4 @ 0x08072838/0x10 beq-taken in equip_zone_sub_2804
#   Step 4: ROM_INCBIN blocks -> DisassembleCommand (4 blocks):
#     B1 @ 0x080720e2/0x12 bne-taken in field_spell_dispatch_sub_stubs_2004
#     B2 @ 0x0807270e/0x1e bne-taken in fn_eligible_vampire_lord_lady_26f4
#     B3 @ 0x0807276a/0x1e bne-taken in equip_zone_sub_stubs_274c
#     B4 @ 0x08072794/0x20 bne-target from B3 + 0x7f return path
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).
# NOTE: No new function labels created; all CODE blocks are intra-function LAB_ continuations.
# NOTE: Ordering: DATA createDWord before CODE disasm to prevent Ghidra treating table entries as code.

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
# Applied after createDWord (slot at 0x72830 must be DWORD first)
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # 0x72830: LP_CARD_TRACK_BASE_OFF literal pool -- REUSE ewram.inc:247
    (0x08072830, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF', 'LP_CARD_TRACK_BASE_OFF'),
    # 0x727b4: lookup_equip_score_b_0x1b9 literal pool -- REUSE duel_field.inc:332
    # Already a .word in asm; just apply equate rename
    (0x080727b4, 0x000001b9, 'lookup_equip_score_b_0x1b9', 'pool_b8_27b4'),
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


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== DisassembleF09Seg4RBlocks (DRY=%s) ===" % DRY)
    print("  Remediates [0x080719fc..0x08072d20)")
    print("  4 ROM_INCBIN + 4 .byte CODE + 4 .byte DATA -> full THUMB disasm + DWORDs")
    print("  EQ_SLOTS=%d (all REUSE)" % len(EQ_SLOTS))

    if DRY:
        print("[dry] Step 1: force_dword 0x72430/0x7257c/0x72734/0x72830")
        print("[dry] Step 2: EQ_SLOTS LP_CARD_TRACK_BASE_OFF@0x72830 + lookup_equip_score_b_0x1b9@0x727b4")
        print("[dry] Step 3: C1@0x71f74 C2@0x7241c C3@0x7256a C4@0x72838")
        print("[dry] Step 4: B1@0x720e2 B2@0x7270e B3@0x7276a B4@0x72794")
        return

    # =======================================================================
    # Step 1: DATA .byte -> createDWord FIRST
    # Must precede all DC calls to prevent Ghidra treating table entries as code
    # =======================================================================
    print("\n=== Step 1: DATA .byte -> createDWord ===")

    print("  [1a] 0x72430 -> .word last_turn_sub_2534 (dispatch table[0])")
    _force_dword(0x08072430)

    print("  [1b] 0x7257c -> .word vampire_sub_26bc (dispatch table[0])")
    _force_dword(0x0807257c)

    print("  [1c] 0x72734 -> .word equip_zone_sub_2856 (dispatch table[0])")
    _force_dword(0x08072734)

    print("  [1d] 0x72830 -> .word LP_CARD_TRACK_BASE_OFF (literal pool)")
    _force_dword(0x08072830)

    # =======================================================================
    # Step 2: EQ_SLOTS
    # =======================================================================
    print("\n=== Step 2: EQ_SLOTS (%d) ===" % len(EQ_SLOTS))
    nEQ = 0
    for slot_int, value, cname, label in EQ_SLOTS:
        if _apply_eq(slot_int, value, cname, label):
            nEQ += 1
    print("[EQ] Applied %d/%d equates" % (nEQ, len(EQ_SLOTS)))

    # =======================================================================
    # Step 3: .byte CODE blocks -> DisassembleCommand
    # =======================================================================
    print("\n=== Step 3: .byte CODE blocks ===")

    # -----------------------------------------------------------------------
    # C1: indirect dispatch in fn_eligible_fengsheng_mirror_1f58
    #   .byte 0xc @ 0x71f74..0x71f7f
    #   bls LAB_08071f74 at 0x8071f70 (bls taken = valid dispatch range)
    #   5 instrs: lsls r0,r0,#2; ldr r1,[pc,#12]; adds r0,r0,r1; ldr r0,[r0,#0]; mov r15,r0
    #   pad at 0x71f7e (0x0000 = movs r0,r0)
    # -----------------------------------------------------------------------
    print("\n--- C1: fn_eligible_fengsheng_mirror_1f58 dispatch ---")
    print("  .byte 0xc @ 0x71f74..0x71f7f; pool_1f84 @ 0x71f84 is OUTSIDE range")
    _clear_listing(0x08071f74, 0x08071f7f)
    _set_tmode(0x08071f74, 0x08071f7f)
    _disasm_at(0x08071f74, 'C1_fengsheng_dispatch')
    n = _count_instrs(0x08071f74, 0x08071f7f)
    print("  [check] %d instructions in C1 (expect 5+pad)" % n)

    # -----------------------------------------------------------------------
    # C2: indirect dispatch in fn_eligible_fiend_comedian_2404
    #   .byte 0xc @ 0x7241c..0x72427
    #   bls LAB_0807241c at 0x8072418 (bls taken = valid dispatch range)
    #   5 instrs: lsls r0,r0,#2; ldr r1,[pc,#12]; adds r0,r0,r1; ldr r0,[r0,#0]; mov r15,r0
    #   pad at 0x72426 (0x0000)
    #   pool_next_addr_242c @ 0x7242c = 0x08072430 (OUTSIDE range, already in asm)
    # -----------------------------------------------------------------------
    print("\n--- C2: fn_eligible_fiend_comedian_2404 dispatch ---")
    print("  .byte 0xc @ 0x7241c..0x72427; pool @ 0x7242c OUTSIDE range")
    _clear_listing(0x0807241c, 0x08072427)
    _set_tmode(0x0807241c, 0x08072427)
    _disasm_at(0x0807241c, 'C2_fiend_comedian_dispatch')
    n = _count_instrs(0x0807241c, 0x08072427)
    print("  [check] %d instructions in C2 (expect 5+pad)" % n)

    # -----------------------------------------------------------------------
    # C3: indirect dispatch in fn_eligible_last_turn_2540
    #   .byte 0xa @ 0x7256a..0x72573
    #   bls LAB_0807256a at 0x8072566 (bls taken = valid dispatch range)
    #   5 instrs: lsls r0,r1,#2; ldr r1,[pc,#8]; adds r0,r0,r1; ldr r0,[r0,#0]; mov r15,r0
    #   no trailing pad (size 0xa = 5 halfwords exactly)
    #   pool_b6_2578 @ 0x72578 = 0x0807257c (OUTSIDE range, already in asm)
    # -----------------------------------------------------------------------
    print("\n--- C3: fn_eligible_last_turn_2540 dispatch ---")
    print("  .byte 0xa @ 0x7256a..0x72573; pool_b6_2578 @ 0x72578 OUTSIDE range")
    _clear_listing(0x0807256a, 0x08072573)
    _set_tmode(0x0807256a, 0x08072573)
    _disasm_at(0x0807256a, 'C3_last_turn_dispatch')
    n = _count_instrs(0x0807256a, 0x08072573)
    print("  [check] %d instructions in C3 (expect 5)" % n)

    # -----------------------------------------------------------------------
    # C4: beq-taken path in equip_zone_sub_2804
    #   .byte 0x10 @ 0x72838..0x72847
    #   beq LAB_08072838 at 0x807280e (beq taken = LP tracking entry == 0)
    #   8 instrs: ldrb r3,[r3,#2]; lsls r0,r3,#31; lsrs r0,r0,#31; movs r1,#0xd;
    #             BL trigger_card_display_op31_if_not_active; movs r0,#0x7c; b LAB_08072866
    #   No pool words in range; pools at 0x7282c/0x72834 are BEFORE block and already in asm
    # -----------------------------------------------------------------------
    print("\n--- C4: equip_zone_sub_2804 beq-taken path ---")
    print("  .byte 0x10 @ 0x72838..0x72847; pools @ 0x7282c/0x72834 OUTSIDE (before) range")
    _clear_listing(0x08072838, 0x08072847)
    _set_tmode(0x08072838, 0x08072847)
    _disasm_at(0x08072838, 'C4_equip_zone_2804_beq_path')
    n = _count_instrs(0x08072838, 0x08072847)
    print("  [check] %d instructions in C4 (expect 7-8)" % n)

    # =======================================================================
    # Step 4: ROM_INCBIN blocks -> DisassembleCommand (address order)
    # =======================================================================
    print("\n=== Step 4: ROM_INCBIN blocks ===")

    # -----------------------------------------------------------------------
    # B1: bne-taken path in field_spell_dispatch_sub_stubs_2004
    #   ROM_INCBIN 0x720e2/0x12 -> [0x080720e2, 0x080720f3]
    #   bne LAB_080720e2 at 0x8072062 (bne taken = card IS field-type-7)
    #   9 instrs: ldrb r1,[r4,#2]; lsls r0,r1,#31; lsrs r0,r0,#31; ldrh r1,[r4,#0];
    #             movs r2,#1; BL set_lp_display_row_type5(0x080a1c2c); movs r0,#0x7f;
    #             b LAB_080720f6 (shared epilogue)
    #   No pool words in block range; adjacent pools at 0x720a4/0x720a8 are outside
    # -----------------------------------------------------------------------
    print("\n--- B1: field_spell_dispatch_sub_stubs_2004 bne-taken path ---")
    print("  ROM_INCBIN 0x720e2/0x12; no pool words in block range")
    print("  BL target: 0x080a1c2c = set_lp_display_row_type5")
    _clear_listing(0x080720e2, 0x080720f3)
    _set_tmode(0x080720e2, 0x080720f3)
    _disasm_at(0x080720e2, 'B1_field_spell_dispatch_bne_path')
    n = _count_instrs(0x080720e2, 0x080720f3)
    print("  [check] %d instructions in B1 (expect 9)" % n)

    # -----------------------------------------------------------------------
    # B2: bne-taken path in fn_eligible_vampire_lord_lady_26f4
    #   ROM_INCBIN 0x7270e/0x1e -> [0x0807270e, 0x0807272b]
    #   bne LAB_0807270e at 0x8072704 (bne taken = NOT hand-set-code path)
    #   15 halfwords: ldr r0,[pc,#28]; movs r2,#0x94; lsls r2,r2,#3; adds r1,r0,r2;
    #     ldr r1,[r1,#0]; subs r1,#0x7b; adds r2,r0,#0; cmp r1,#5;
    #     bls <taken>; b <return0 path>;
    #     [bls-taken]: lsls r0,r1,#2; ldr r1,[pc,#8]; adds r0,r0,r1; ldr r0,[r0,#0]; mov r15,r0
    #   pool_b7_272c @ 0x7272c (gDuelPhaseFlags) + pool_b7_2730 @ 0x72730 OUTSIDE range
    # -----------------------------------------------------------------------
    print("\n--- B2: fn_eligible_vampire_lord_lady_26f4 bne-taken path ---")
    print("  ROM_INCBIN 0x7270e/0x1e; pools pool_b7_272c @ 0x7272c + pool_b7_2730 @ 0x72730 OUTSIDE range")
    _clear_listing(0x0807270e, 0x0807272b)
    _set_tmode(0x0807270e, 0x0807272b)
    _disasm_at(0x0807270e, 'B2_vampire_lord_lady_bne_path')
    n = _count_instrs(0x0807270e, 0x0807272b)
    print("  [check] %d instructions in B2 (expect 15)" % n)

    # -----------------------------------------------------------------------
    # B3: bne-taken path in equip_zone_sub_stubs_274c
    #   ROM_INCBIN 0x7276a/0x1e -> [0x0807276a, 0x08072787]
    #   bne LAB_0807276a at 0x8072766 (bne taken = active card pointer IS present)
    #   14 instrs + 1 pad (0x0000 at 0x72786 = movs r0,r0 NOP)
    #   ldr r0,[pc,#36]; lsrs r1,r2,#31; lsls r1,r1,#2; adds r0,#8; adds r1,r1,r0;
    #   ldr r0,[r1,#0]; cmp r0,#1; bne->B4; movs r3,#0xea; lsls r3,r3,#5;
    #   adds r1,r4,r3; movs r0,#0; str r0,[r1,#0]; b->0x80727ae (inside B4)
    #   pool_b8_2788/278c/2790 OUTSIDE range
    #   B3 BEFORE B4: B3's b@0x72784->0x727ae resolves after B4 disasm
    # -----------------------------------------------------------------------
    print("\n--- B3: equip_zone_sub_stubs_274c bne-taken path ---")
    print("  ROM_INCBIN 0x7276a/0x1e; pools pool_b8_2788/278c/2790 OUTSIDE range")
    print("  NOTE: B3's b@0x72784->0x727ae (inside B4); process B3 first then B4")
    _clear_listing(0x0807276a, 0x08072787)
    _set_tmode(0x0807276a, 0x08072787)
    _disasm_at(0x0807276a, 'B3_equip_zone_274c_bne_path')
    n = _count_instrs(0x0807276a, 0x08072787)
    print("  [check] %d instructions in B3 (expect 14+pad)" % n)

    # -----------------------------------------------------------------------
    # B4: bne-target from B3 + 0x7f return path
    #   ROM_INCBIN 0x72794/0x20 -> [0x08072794, 0x080727b3]
    #   Also: B3's b@0x72784 lands at 0x727ae which is WITHIN B4 range
    #   16 halfwords: movs r0,#0x82; lsls r0,r0,#1; movs r1,#0xdc; lsls r1,r1,#1;
    #     ldr r2,[pc,#20]; movs r3,#0xdd; lsls r3,r3,#1; movs r4,#0;
    #     str r4,[sp,#0]; movs r4,#0xf; str r4,[sp,#4];
    #     BL invoke_card_display_op_0x31_sub3_with_packed_params(0x080933dc);
    #     [B3 branch target 0x727ae]: movs r0,#0x7f; b LAB_08072866 (epilogue); pad
    #   pool_b8_27b4 @ 0x727b4 (0x1b9 lookup_equip_score_b_0x1b9) OUTSIDE block end 0x727b3
    # -----------------------------------------------------------------------
    print("\n--- B4: equip_zone_sub_stubs_274c bne-target + 0x7f return path ---")
    print("  ROM_INCBIN 0x72794/0x20; pool_b8_27b4 @ 0x727b4 OUTSIDE range (block ends at 0x727b3)")
    print("  BL target: 0x080933dc = invoke_card_display_op_0x31_sub3_with_packed_params")
    _clear_listing(0x08072794, 0x080727b3)
    _set_tmode(0x08072794, 0x080727b3)
    _disasm_at(0x08072794, 'B4_equip_zone_274c_bne_target')
    n = _count_instrs(0x08072794, 0x080727b3)
    print("  [check] %d instructions in B4 (expect 15+pad)" % n)

    # =======================================================================
    # Summary
    # =======================================================================
    print("\n=== DisassembleF09Seg4RBlocks DONE ===")
    print("  DATA DWORDs: 4 (.byte -> .word)")
    print("  EQ applied: %d/2 (LP_CARD_TRACK_BASE_OFF + lookup_equip_score_b_0x1b9)" % nEQ)
    print("  CODE disasm: C1+C2+C3+C4 + B1+B2+B3+B4 = 8 blocks")
    print("  All CODE blocks are intra-function LAB_ continuations; no new functions created")
    print("  Expected Seg-4 ROM_INCBIN residue after export: 0")


main()
