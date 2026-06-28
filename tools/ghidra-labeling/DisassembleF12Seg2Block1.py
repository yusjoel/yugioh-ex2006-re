# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF12Seg2Block1.py -- file 12 Seg-2 Block1 R4 disasm
#
# Block1: ROM_INCBIN 0x08095274 / 0xc0 (0x08095274..0x08095333)
#   10-entry jump table at 0x0809524c with 9 unique case-block entry points.
#   dispatch_equip_confirm_phase_by_step dispatches via `mov pc, r0` (0x4687, raw ptr).
#
# Jump table at 0x0809524c (10 entries, each 4B RAW pointers, not THUMB+1):
#   entry[0]: 0x0809530a   entry[1]: 0x0809529e   entry[2]: 0x080952aa
#   entry[3]: 0x08095292   entry[4]: 0x08095284   entry[5]: 0x0809528a
#   entry[6]: 0x0809528e   entry[7]: 0x08095274   entry[8]: 0x08095274 (shared)
#   entry[9]: 0x08095304
#
# 9 unique case-block entry points (9 DisassembleCommands):
#   0x08095274  Case[7+8]: ldr+ldrh+bl+b + pool
#   0x08095284  Case[4]:   bl+b
#   0x0809528a  Case[5]:   movs+b (falls to case[3]+1 at 0x8095294)
#   0x0809528e  Case[6]:   movs+b (falls to shared path at 0x8095290)
#   0x08095292  Case[3]+[6-fall]: movs+movs+movs+bl+b
#   0x0809529e  Case[1]:   movs+movs+movs+bl+b
#   0x080952aa  Case[2]:   larger sequence with cmp/b tree
#   0x08095304  Case[9]:   bl+b
#   0x0809530a  Case[0]:   ldr+adds+ldr+ldr+adds+ldr+adds+subs+movs+rsbs+bl+ldr+adds+b+pool*3
#
# Pool words inside Block1 (createDWord + equate):
#   0x8095280: 0x00001d5c (ELIGIB_ACT_TYPE_OFF -- ewram.inc:421 REUSE)
#   0x80952cc: 0x00001d6c (ELIGIB_ANIM_STATE_OFF -- ewram.inc:423 REUSE)
#   0x80952d0: 0x00001d68 (ELIGIB_SPRITE_CTRL_OFF -- ewram.inc:422 REUSE)
#   0x8095328: 0x00001d68 (ELIGIB_SPRITE_CTRL_OFF REUSE)
#   0x809532c: 0x00001d6c (ELIGIB_ANIM_STATE_OFF REUSE)
#   0x8095330: 0x00001d54 (ELIGIB_STATE_CTRL_OFF -- ewram.inc:419 REUSE)
#
# Post-disasm: ROM_INCBIN/.byte grep in [0x08095274, 0x08095334) must == 0
# No createFunction (jump targets, not standalone functions).
#
# NOTE: All text is pure ASCII.

from ghidra.app.cmd.disassemble import DisassembleCommand
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


# 9 unique case-block DisassembleCommand addresses
B1_CASES = [
    (0x08095274, 'dispatch_case_7_8_lp_anim', 'case[7+8]: ldr+ldrh+bl apply_slot_equip_activation_if_lp_anim_phase; b epilogue'),
    (0x08095284, 'dispatch_case_4_init_lp',   'case[4]: bl init_lp_bar_slot_entry_from_state; b epilogue'),
    (0x0809528a, 'dispatch_case_5_tickseq0',  'case[5]: movs r0,#0; b case[3]+1 (0x8095294) -- dispatch(1,0,1)'),
    (0x0809528e, 'dispatch_case_6_tickseq0b', 'case[6]: movs r0,#0; b shared_path 0x80952f2 -> dispatch(0,0,0)'),
    (0x08095292, 'dispatch_case_3_tickseq1',  'case[3]+[6-fall]: movs r0,#1; movs r1,#0; movs r2,#1; bl tick_equip_target_selection_display_seq; b epilogue'),
    (0x0809529e, 'dispatch_case_1_tickseq1',  'case[1]: movs r0,#1; movs r1,#1; movs r2,#0; bl tick_equip_target_selection_display_seq; b epilogue'),
    (0x080952aa, 'dispatch_case_2_anim_cmp',  'case[2]: ldr+adds+ldr cmp r2,#0xb; branches; bl dispatch_effect_slot_by_display_state; b epilogue'),
    (0x08095304, 'dispatch_case_9_lp_anim',   'case[9]: bl tick_lp_bar_anim_step_display; b epilogue'),
    (0x0809530a, 'dispatch_case_0_init_lp2',  'case[0]: loads offsets 0x1d68/0x1d6c; bl init_lp_bar_slot_entry_from_state; ldr 0x1d54; b 0x8095338 store path'),
]

# Pool words inside Block1: (addr, value, eq_name)
B1_POOL_WORDS = [
    (0x08095280, 0x00001d5c, 'ELIGIB_ACT_TYPE_OFF'),
    (0x080952cc, 0x00001d6c, 'ELIGIB_ANIM_STATE_OFF'),
    (0x080952d0, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF'),
    (0x08095328, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF'),
    (0x0809532c, 0x00001d6c, 'ELIGIB_ANIM_STATE_OFF'),
    (0x08095330, 0x00001d54, 'ELIGIB_STATE_CTRL_OFF'),
]

B1_RANGE_START = 0x08095274
B1_RANGE_END   = 0x08095333  # inclusive (0xc0 bytes -> 0x08095274 + 0xc0 - 1 = 0x08095333)


def main():
    print("=== DisassembleF12Seg2Block1 (DRY=%s) ===" % DRY)
    print("  Block1: 0x08095274..0x08095333 (0xc0 bytes)")
    print("  9 unique case blocks + 6 pool words")

    listing = currentProgram.getListing()
    sym_tbl = currentProgram.getSymbolTable()
    eq_tbl  = currentProgram.getEquateTable()
    ctx     = currentProgram.getProgramContext()
    tmode   = ctx.getRegister("TMode")

    a_lo = _addr(B1_RANGE_START)
    a_hi = _addr(B1_RANGE_END)

    if DRY:
        print("[dry] clearListing 0x%08x..0x%08x" % (B1_RANGE_START, B1_RANGE_END))
        print("[dry] setTMode THUMB=1")
        for case_addr, case_label, case_eol in B1_CASES:
            print("[dry] DisassembleCommand @ 0x%08x  label=%s" % (case_addr, case_label))
        for pw_addr, pw_val, pw_eq in B1_POOL_WORDS:
            print("[dry] createDWord+EQ @ 0x%08x = 0x%08x (%s)" % (pw_addr, pw_val, pw_eq))
        print("[dry] done -- 9 case blocks, 6 pool words, no createFunction")
        return

    # Step 1: clearListing entire block
    print("[1] clearListing 0x%08x..0x%08x" % (B1_RANGE_START, B1_RANGE_END))
    try:
        clearListing(a_lo, a_hi)
        print("    done")
    except Exception as e:
        print("[WARN] clearListing: %s" % e)

    # Step 2: setTMode THUMB=1
    print("[2] setTMode THUMB=1 for 0x%08x..0x%08x" % (B1_RANGE_START, B1_RANGE_END))
    if tmode is not None:
        ctx.setValue(tmode, a_lo, a_hi, BigInteger.ONE)
        print("    TMode set")
    else:
        print("[WARN] TMode register not found")

    # Step 3: DisassembleCommand per case block (9 calls)
    print("[3] DisassembleCommand per unique case-block entry (9 calls)")
    for case_addr, case_label, case_eol in B1_CASES:
        print("    [3.x] @ 0x%08x (%s)" % (case_addr, case_label))
        ca = _addr(case_addr)
        cmd = DisassembleCommand(ca, None, False)
        if cmd.applyTo(currentProgram):
            print("          disasm ok")
        else:
            print("          [WARN] disasm: %s" % cmd.getStatusMsg())

    # Step 4: createLabel + EOL for each case block
    print("[4] createLabel + EOL for each case block")
    for case_addr, case_label, case_eol in B1_CASES:
        ca = _addr(case_addr)
        existing = [s.getName() for s in sym_tbl.getSymbols(ca)]
        if case_label not in existing:
            sym_tbl.createLabel(ca, case_label, SourceType.USER_DEFINED)
            print("    label created: %s @ 0x%08x" % (case_label, case_addr))
        else:
            print("    label already present: %s" % case_label)

        if case_eol:
            cu = listing.getCodeUnitAt(ca)
            if cu is not None:
                cu.setComment(CodeUnit.EOL_COMMENT, case_eol)

    # Step 5: createDWord on each pool word + equate reference
    print("[5] createDWord + equate on pool words (%d)" % len(B1_POOL_WORDS))
    for pw_addr, pw_val, pw_eq in B1_POOL_WORDS:
        pa = _addr(pw_addr)
        print("    [5.x] @ 0x%08x = 0x%08x (%s)" % (pw_addr, pw_val, pw_eq))
        try:
            listing.createData(pa, ghidra.program.model.data.DWordDataType.dataType)
            print("          createDWord ok")
        except Exception as e:
            print("          [WARN] createDWord: %s" % e)
        # equate reference
        eq = eq_tbl.getEquate(pw_eq)
        if eq is None:
            eq = eq_tbl.createEquate(pw_eq, pw_val & 0xFFFFFFFFFFFFFFFFL)
            print("          equate created: %s" % pw_eq)
        eq.addReference(pa, 0)
        print("          equate ref added")

    print("\n=== DisassembleF12Seg2Block1 DONE ===")
    print("  9 case blocks disassembled, 6 pool words created")
    print("  No createFunction (all are jump targets inside dispatch_equip_confirm_phase_by_step)")
    print("  POST-CHECK: grep ROM_INCBIN/.byte in [0x08095274, 0x08095334) must == 0")


main()
