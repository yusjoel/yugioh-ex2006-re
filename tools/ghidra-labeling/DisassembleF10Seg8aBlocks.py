# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF10Seg8aBlocks.py -- f10 Seg-8a R4 disasm (2 ROM_INCBIN blocks)
#
#   BLK1: fn_eligible_two_pronged_attack @ 0x080827d4..0x080828ab (0xd8 bytes)
#     FS table THUMB+1 ref: ROM[0x09e3fc60]=0x080827d5 (CID=0x12e7 Two-Pronged Attack)
#     FS entry: [+0x0]=0x12e7 (TWO_PRONGED_ATTACK_CID), [+0x14]=0x080827d5 (fn_eligible+1)
#     ROM[0x827d4]=0xb5f0 (PUSH {r4..r7,lr} confirmed THUMB fn entry)
#     Literal pools in BLK1 (ROM-verified):
#       0x08082880 = 0x0201e2a0 (gDuelCardCtxBase) -- createDWord
#       0x08082884 = 0xfffc7fff (DUAL_LABEL_RENDER_STATE_CLEAR) -- createDWord
#       0x080828a4 = 0x0201b290 (gDuelPhaseFlags) -- createDWord
#       0x080828a8 = 0x080828ac (ptr to JT base) -- createDWord
#     NOTE: 0x080828a0 = 0x00004687 is THUMB code (mov pc,r0 = 0x4687 ldrb + misc)
#           DO NOT createDWord at 0x080828a0 -- it is code, not a literal pool word
#     JT at 0x080828ac (6x.word) already decoded in asm as .word entries -- NO action
#
#   BLK2: 4 sub-stubs @ 0x080828c4..0x080829bb (0xf8 bytes)
#     Reached via JT at 0x080828ac (already decoded in asm):
#       JT[0]=0x080828c4, JT[1]=0x08082954, JT[2]=0x080828f4,
#       JT[3]=0x08082954, JT[4]=0x08082924, JT[5]=0x08082954
#     4 unique entry points: 0x828c4, 0x828f4, 0x82924, 0x82954
#     ROM bytes verified:
#       0x828c4 hword=0x78aa (THUMB code start), 0x828f4 hword=0x78a9,
#       0x82924 hword=0x78a9, 0x82954 hword=0xf014
#     BLK2 ends at 0x829bc (hword=0xb570 = next fn tick_equip_display_by_card_id_group_a_4state)
#     Literal pools in BLK2 (ROM-verified):
#       0x080828ec = 0x08082771 (fn ptr to check_effect_slot_zone_field_by_type+1 code?) -- createDWord
#       0x080828f0 = 0x0201b290 (gDuelPhaseFlags) -- createDWord
#       0x0808291c = 0x08082771 (same) -- createDWord
#       0x08082920 = 0x0201b290 -- createDWord
#       0x0808294c = 0x08082771 -- createDWord
#       0x08082950 = 0x0201b290 -- createDWord
#       0x08082988 = 0x0201c4e0 -- createDWord
#       0x0808298c = 0x00001d68 (ELIGIB_SPRITE_CTRL_OFF) -- createDWord
#       0x08082990 = 0x00001d6c (ELIGIB_ANIM_STATE_OFF) -- createDWord
#       0x08082994 = 0x0201b290 -- createDWord
#       0x080829ac = 0x0201b290 -- createDWord
#     NOTE: 0x08082771 is THUMB code addr (inside check_effect_slot_zone_field_by_type body)
#           treated as raw ROM address constant in pool, createDWord is correct
#
# NOTE: All EOL/plate text is pure ASCII (no CJK). Ghidra Jython mojibake prevention.

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
        print("[dword ok] 0x%08x" % addr_int)
    except Exception as e:
        print("[warn] createDWord 0x%08x: %s" % (addr_int, e))
    if label:
        sm = currentProgram.getSymbolTable()
        sm.createLabel(a, label, SourceType.USER_DEFINED)
    if eol:
        cu = listing.getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)


def _create_label(addr_int, label, eol=None):
    a = _addr(addr_int)
    sm = currentProgram.getSymbolTable()
    sm.createLabel(a, label, SourceType.USER_DEFINED)
    if eol:
        listing = currentProgram.getListing()
        cu = listing.getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)
    print("[label ok] 0x%08x %s" % (addr_int, label))


def _create_function(addr_int, fn_name, plate_text=None):
    a = _addr(addr_int)
    fm = currentProgram.getFunctionManager()
    fn = fm.getFunctionAt(a)
    if fn is not None:
        fn.setName(fn_name, SourceType.USER_DEFINED)
        print("[fn rename] 0x%08x -> %s" % (addr_int, fn_name))
    else:
        fn = createFunction(a, fn_name)
        if fn is not None:
            print("[fn create] 0x%08x %s" % (addr_int, fn_name))
        else:
            print("[warn] createFunction 0x%08x %s failed" % (addr_int, fn_name))
    if plate_text and fn is not None:
        listing = currentProgram.getListing()
        cu = listing.getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.PLATE_COMMENT, plate_text)
            print("[plate ok] 0x%08x" % addr_int)


def _check_mem_word(addr_int, expected):
    mem = currentProgram.getMemory()
    a = _addr(addr_int)
    try:
        actual = mem.getInt(a) & 0xFFFFFFFF
        match = (actual == (expected & 0xFFFFFFFF))
        status = 'OK' if match else 'MISMATCH'
        print("[check] 0x%08x: got=0x%08x exp=0x%08x %s" % (
            addr_int, actual, expected & 0xFFFFFFFF, status))
        return match
    except Exception as e:
        print("[check err] 0x%08x: %s" % (addr_int, e))
        return False


def main():
    print("=== DisassembleF10Seg8aBlocks (DRY=%s) ===" % DRY)

    if DRY:
        print("[DRY] BLK1: fn_eligible_two_pronged_attack (0x080827d4..0x080828ab)")
        print("[DRY]   clearListing + setTMode 0x080827d4..0x080828ab")
        print("[DRY]   disasm_stub 0x080827d4 (PUSH 0xb5f0 confirmed fn entry)")
        print("[DRY]   createDWord pool: 0x08082880=gDuelCardCtxBase, 0x08082884=attr_clear,")
        print("[DRY]     0x080828a4=gDuelPhaseFlags, 0x080828a8=JT_ptr (0x080828ac)")
        print("[DRY]   createFunction fn_eligible_two_pronged_attack @ 0x080827d4 + plate")
        print("[DRY] BLK2: 4 sub-stubs (0x080828c4..0x080829bb)")
        print("[DRY]   clearListing + setTMode 0x080828c4..0x080829bb")
        print("[DRY]   disasm_stub x4: 0x828c4/0x828f4/0x82924/0x82954")
        print("[DRY]   createDWord pool x11 in BLK2")
        print("[DRY]   createFunction x4: equip_sub_stub_a/b/c/shared_exit + plates")
        return

    # -----------------------------------------------------------------------
    # BLK1: fn_eligible_two_pronged_attack
    # Range: [0x080827d4, 0x080828ac) = 0xd8 bytes THUMB
    # JT at 0x080828ac already decoded as .word entries in asm -- NO action
    # -----------------------------------------------------------------------
    print("--- BLK1: fn_eligible_two_pronged_attack ---")

    # Verify key pool words before disasm
    _check_mem_word(0x080827d4, 0xb081b5f0)  # PUSH {r4..r7,lr} + sub sp,#8
    _check_mem_word(0x08082880, 0x0201e2a0)  # gDuelCardCtxBase
    _check_mem_word(0x08082884, 0xfffc7fff)  # DUAL_LABEL_RENDER_STATE_CLEAR
    _check_mem_word(0x080828a4, 0x0201b290)  # gDuelPhaseFlags
    _check_mem_word(0x080828a8, 0x080828ac)  # JT ptr

    _clear_and_tmode(0x080827d4, 0x080828ab)
    _disasm_stub(0x080827d4)  # fn entry: PUSH {r4,r5,r6,r7,lr}

    # Literal pool createDWords in BLK1
    _create_dword(0x08082880, 'fn_eligible_tpa_card_ctx_80',
                  'gDuelCardCtxBase=0x0201e2a0: duel card context base')
    _create_dword(0x08082884, 'fn_eligible_tpa_attr_clear_84',
                  'DUAL_LABEL_RENDER_STATE_CLEAR=0xfffc7fff: AND mask clears bits[15:14]')
    # 0x080828a0 = 0x00004687 is THUMB code (mov pc,r0 epilogue pattern) -- DO NOT createDWord
    _create_dword(0x080828a4, 'fn_eligible_tpa_phase_flags_a4',
                  'gDuelPhaseFlags=0x0201b290: duel phase state base')
    _create_dword(0x080828a8, 'fn_eligible_tpa_jt_ptr_a8',
                  'ptr to JT at 0x080828ac (6-entry index jump table)')

    _create_function(
        0x080827d4,
        'fn_eligible_two_pronged_attack',
        "@ fn_eligible for TWO_PRONGED_ATTACK_CID(0x12e7).\n"
        "@ Received via FS handler table 0x09e3fc4c:\n"
        "@   [+0x00]=0x12e7 (TWO_PRONGED_ATTACK_CID), [+0x14]=0x080827d5 (fn_eligible+1).\n"
        "@ Checks eligibility for equip activation by Two-Pronged Attack.\n"
        "@ Dispatches to 4 sub-stubs (equip_sub_stub_a/b/c/shared_exit) via JT at 0x080828ac.\n"
        "@ JT entries: [0]=0x080828c4, [1]=0x08082954(shared), [2]=0x080828f4,\n"
        "@             [3]=0x08082954(shared), [4]=0x08082924, [5]=0x08082954(shared)."
    )

    # -----------------------------------------------------------------------
    # BLK2: 4 sub-stubs [0x080828c4..0x080829bb]
    # Dispatched from JT at 0x080828ac (already decoded as .word entries)
    # DAT_080828c4 label already present in asm; 3 other stubs unlabeled
    # -----------------------------------------------------------------------
    print("--- BLK2: 4 sub-stubs (equip_sub_stub_a/b/c/shared_exit) ---")

    # Verify sub-stub entry hwords
    _check_mem_word(0x080828c4, 0xf01478aa)  # ldrb r2,[r5,#2] + bl ...
    _check_mem_word(0x080828f4, 0xf01478a9)  # ldrb r1,[r5,#2] + bl ...
    _check_mem_word(0x08082924, 0xf01478a9)  # same pattern
    _check_mem_word(0x08082954, 0x4802f014)  # bl + ldr

    _clear_and_tmode(0x080828c4, 0x080829bb)

    # Per-stub DisassembleCommand (one per unique JT entry)
    _disasm_stub(0x080828c4)  # equip_sub_stub_a (JT[0])
    _disasm_stub(0x080828f4)  # equip_sub_stub_b (JT[2])
    _disasm_stub(0x08082924)  # equip_sub_stub_c (JT[4])
    _disasm_stub(0x08082954)  # equip_sub_stub_shared_exit (JT[1,3,5])

    # Literal pool createDWords in BLK2
    # Note: 0x08082771 = addr inside check_effect_slot_zone_field_by_type body (raw ROM ptr)
    _create_dword(0x080828ec, 'equip_sub_a_zone_fn_ptr_ec',
                  'raw ROM ptr 0x08082771 (inside check_effect_slot_zone_field_by_type body)')
    _create_dword(0x080828f0, 'equip_sub_a_phase_flags_f0',
                  'gDuelPhaseFlags=0x0201b290')
    _create_dword(0x0808291c, 'equip_sub_b_zone_fn_ptr_1c',
                  'raw ROM ptr 0x08082771 (check_effect_slot_zone_field_by_type body)')
    _create_dword(0x08082920, 'equip_sub_b_phase_flags_20',
                  'gDuelPhaseFlags=0x0201b290')
    _create_dword(0x0808294c, 'equip_sub_c_zone_fn_ptr_4c',
                  'raw ROM ptr 0x08082771 (check_effect_slot_zone_field_by_type body)')
    _create_dword(0x08082950, 'equip_sub_c_phase_flags_50',
                  'gDuelPhaseFlags=0x0201b290')
    _create_dword(0x08082988, 'equip_sub_shared_field_ctx_88',
                  '0x0201c4e0: EWRAM equip field context (not yet named; field-area data base)')
    _create_dword(0x0808298c, 'equip_sub_shared_sprite_ctrl_8c',
                  'ELIGIB_SPRITE_CTRL_OFF=0x1d68: sprite ctrl halfword offset')
    _create_dword(0x08082990, 'equip_sub_shared_anim_state_90',
                  'ELIGIB_ANIM_STATE_OFF=0x1d6c: anim state halfword offset')
    _create_dword(0x08082994, 'equip_sub_shared_phase_flags_94',
                  'gDuelPhaseFlags=0x0201b290')
    _create_dword(0x080829ac, 'equip_sub_shared_phase_flags_ac',
                  'gDuelPhaseFlags=0x0201b290')

    # Create functions for each sub-stub
    _create_function(
        0x080828c4,
        'equip_sub_stub_a',
        "@ Sub-stub A for Two-Pronged Attack equip dispatch: reached via JT[0]=0x080828c4.\n"
        "@ Checks zone field via check_effect_slot_zone_field_by_type(r5, r2-bit0, r1-bit0).\n"
        "@ Updates state at [gDuelPhaseFlags+0x96*8] on match."
    )
    _create_function(
        0x080828f4,
        'equip_sub_stub_b',
        "@ Sub-stub B for Two-Pronged Attack equip dispatch: reached via JT[2]=0x080828f4.\n"
        "@ Checks zone field via check_effect_slot_zone_field_by_type(r5, r1-bit0, r3).\n"
        "@ Updates state at [gDuelPhaseFlags+0x96*8] on match."
    )
    _create_function(
        0x08082924,
        'equip_sub_stub_c',
        "@ Sub-stub C for Two-Pronged Attack equip dispatch: reached via JT[4]=0x08082924.\n"
        "@ Checks zone field via check_effect_slot_zone_field_by_type(r5, r1-bit0, r3).\n"
        "@ Same pattern as sub_stub_b with different zone qualifier."
    )
    _create_function(
        0x08082954,
        'equip_sub_stub_shared_exit',
        "@ Shared exit sub-stub: reached via JT[1,3,5]=0x08082954.\n"
        "@ Called by 3 JT entries as common exit path.\n"
        "@ Enqueues equip slot sprite and/or updates LP display.\n"
        "@ Terminal stub: returns to fn_eligible_two_pronged_attack caller."
    )

    print("")
    print("=== DisassembleF10Seg8aBlocks DONE ===")
    print("=== BLK1: fn_eligible_two_pronged_attack @ 0x080827d4 (4 pool DWords) ===")
    print("=== BLK2: 4 sub-stubs @ 0x828c4/0x828f4/0x82924/0x82954 (11 pool DWords) ===")


main()
