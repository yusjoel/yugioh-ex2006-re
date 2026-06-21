# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF10Seg2Blocks.py -- f10 Seg-2 R4 disasm (8 ROM_INCBIN blocks)
#   BLK1 0x7af66/0x3a: 2B pad + fn_eligible_lighten_the_load (THUMB+1 @0x9e46fe8 -> 0x7af69)
#   BLK2 0x7afb8/0x110: Lighten the Load dispatch sub-stubs (6 unique entries)
#   BLK3 0x7b4d4/0x2c: fn_eligible_hero_kid_hyena shared (THUMB+1 @0x9e45428,0x9e46028 -> 0x7b4d5)
#   BLK4 0x7b574/0x144: Hero Kid/Hyena dispatch sub-stubs (7 unique entries incl default)
#   BLK5 0x7b7dc/0x28: fn_eligible_rescue_cat (THUMB+1 @0x9e470f0 -> 0x7b7dd)
#   BLK6 0x7b878/0xe0: Rescue Cat dispatch sub-stubs (7 unique entries incl default)
#   BLK7 0x7b9f4/0x28: fn_eligible_gatling_dragon (THUMB+1 @0x9e47108 -> 0x7b9f5)
#   BLK8 0x7ba30/0x100: Gatling Dragon dispatch sub-stubs (5 unique entries)
#
# Literal pool force-splits (createDWord):
#   BLK1: 0x7af98 (gDuelPhaseFlags), 0x7af9c (dispatch table ptr 0x7afa0)
#   BLK3: 0x7b4f8 (gDuelPhaseFlags), 0x7b4fc (dispatch table ptr 0x7b500)
#         NOTE: 0x7b4f4 = 0x4687 MOV PC,r0 CODE -- DO NOT createDWord there!
#   BLK5: 0x7b7fc (gDuelPhaseFlags), 0x7b800 (dispatch table ptr 0x7b804)
#   BLK7: 0x7ba14 (gDuelPhaseFlags), 0x7ba18 (dispatch table ptr 0x7ba1c)
#   BLK2/4/6/8: inline pool words handled by PoolFix pass if needed.
#
# fn_eligible functions created:
#   fn_eligible_lighten_the_load  @ 0x0807af68  CID=0x1847
#   fn_eligible_hero_kid_hyena    @ 0x0807b4d4  CID=0x19a7+0x1867 (shared)
#   fn_eligible_rescue_cat        @ 0x0807b7dc  CID=0x1876
#   fn_eligible_gatling_dragon    @ 0x0807b9f4  CID=0x1878
#
# PLATE=1: fn_eligible_hero_kid_hyena (ASCII only, applied after createFunction)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.address import AddressSet
from ghidra.program.model.data import DWordDataType, DataTypeConflictHandler
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


def _disasm_stub(entry_int):
    a = _addr(entry_int)
    cmd = DisassembleCommand(a, None, True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm 0x%08x: %s" % (entry_int, cmd.getStatusMsg()))
    else:
        print("[disasm ok] 0x%08x" % entry_int)


def _create_dword(addr_int, eol=None):
    a = _addr(addr_int)
    listing = currentProgram.getListing()
    dt = DWordDataType.dataType
    try:
        listing.clearCodeUnits(a, _addr(addr_int + 3), False)
        listing.createData(a, dt)
        print("[dword ok] 0x%08x" % addr_int)
    except Exception as e:
        print("[warn] createDWord 0x%08x: %s" % (addr_int, e))
    if eol:
        try:
            listing.setComment(a, CodeUnit.EOL_COMMENT, eol)
        except Exception as e:
            print("[warn] EOL 0x%08x: %s" % (addr_int, e))


def _set_eol(addr_int, text):
    listing = currentProgram.getListing()
    try:
        listing.setComment(_addr(addr_int), CodeUnit.EOL_COMMENT, text)
    except Exception as e:
        print("[warn] EOL 0x%08x: %s" % (addr_int, e))


def _set_plate(addr_int, text):
    listing = currentProgram.getListing()
    try:
        listing.setComment(_addr(addr_int), CodeUnit.PLATE_COMMENT, text)
    except Exception as e:
        print("[warn] PLATE 0x%08x: %s" % (addr_int, e))


def _create_fn(addr_int, name, plate=None):
    a = _addr(addr_int)
    fm = currentProgram.getFunctionManager()
    sym_tbl = currentProgram.getSymbolTable()
    fn = fm.getFunctionAt(a)
    if fn is None:
        fn = fm.getFunctionContaining(a)
        if fn is not None:
            entry = fn.getEntryPoint()
            if entry.getOffset() != addr_int:
                fn = None
    if fn is not None:
        old_name = fn.getName()
        fn.setName(name, SourceType.USER_DEFINED)
        print("[fn rename] 0x%08x: %s -> %s" % (addr_int, old_name, name))
    else:
        body = AddressSet(a, _addr(addr_int + 0x80))
        try:
            fn2 = fm.createFunction(name, a, body, SourceType.USER_DEFINED)
            if fn2 is not None:
                print("[fn create] %s @ 0x%08x" % (name, addr_int))
            else:
                print("[WARN] createFunction returned None @ 0x%08x" % addr_int)
                existing = [s.getName() for s in sym_tbl.getSymbols(a)]
                if name not in existing:
                    sym_tbl.createLabel(a, name, SourceType.USER_DEFINED)
                    print("[label] created %s @ 0x%08x" % (name, addr_int))
        except Exception as e:
            print("[WARN] createFunction error @ 0x%08x: %s" % (addr_int, e))
            existing = [s.getName() for s in sym_tbl.getSymbols(a)]
            if name not in existing:
                sym_tbl.createLabel(a, name, SourceType.USER_DEFINED)
                print("[label] created %s @ 0x%08x" % (name, addr_int))
    if plate:
        _set_plate(addr_int, plate)


def main():
    print("=== DisassembleF10Seg2Blocks (DRY=%s) ===" % DRY)

    if DRY:
        print("[dry] BLK1: 2B pad + fn_eligible_lighten_the_load @ 0x7af68 (CID=0x1847)")
        print("[dry] BLK2: 6 dispatch sub-stubs @ 0x7afb8..0x7b0c8")
        print("[dry] BLK3: fn_eligible_hero_kid_hyena @ 0x7b4d4 (CID=0x19a7+0x1867 shared)")
        print("[dry] BLK4: 7 dispatch sub-stubs @ 0x7b574..0x7b6b8")
        print("[dry] BLK5: fn_eligible_rescue_cat @ 0x7b7dc (CID=0x1876)")
        print("[dry] BLK6: 7 dispatch sub-stubs @ 0x7b878..0x7b958")
        print("[dry] BLK7: fn_eligible_gatling_dragon @ 0x7b9f4 (CID=0x1878)")
        print("[dry] BLK8: 5 dispatch sub-stubs @ 0x7ba30..0x7bb30")
        print("[dry] fn_eligible createFunction: 4 stubs")
        print("[dry] PLATE=1: fn_eligible_hero_kid_hyena")
        return

    # ------------------------------------------------------------------
    # BLK1: 0x0807af66 / 0x3a (58B) -- fn_eligible Lighten the Load
    #   2B padding at 0x7af66 (0x0000), THUMB stub starts at 0x7af68
    #   push{r4..r7,lr} = 0xb5f0 at 0x7af68
    #   Literal pool: gDuelPhaseFlags at 0x7af98, dispatch table ptr at 0x7af9c
    # ------------------------------------------------------------------
    print("--- BLK1: 2B pad + fn_eligible_lighten_the_load (0x7af66/0x3a) ---")
    _clear_and_tmode(0x0807af66, 0x0807af9f)
    # 2B pad at 0x7af66 -- clearListing will mark as undefined bytes; disasm from 0x7af68
    _disasm_stub(0x0807af68)
    _create_dword(0x0807af98, 'gDuelPhaseFlags pool word: ldr from fn_eligible_lighten_the_load+0x30')
    _create_dword(0x0807af9c, 'dispatch table ptr 0x0807afa0: ldr from fn_eligible_lighten_the_load')
    _set_eol(0x0807af68, 'fn_eligible_lighten_the_load CID=SERIAL_SPELL_CID? No: CID=0x1847 (Lighten the Load)')
    _create_fn(0x0807af68, 'fn_eligible_lighten_the_load')

    # ------------------------------------------------------------------
    # BLK2: 0x0807afb8 / 0x110 (272B) -- Lighten the Load dispatch sub-stubs
    #   6-entry dispatch table at 0x7afa0..0x7afb4 (already in asm as .word)
    #   6 unique sub-stubs (no separate default beyond these 6):
    #   0x7afb8, 0x7aff0, 0x7b02c, 0x7b058, 0x7b098, 0x7b0ac
    # ------------------------------------------------------------------
    print("--- BLK2: Lighten the Load dispatch sub-stubs (0x7afb8/0x110) ---")
    _clear_and_tmode(0x0807afb8, 0x0807b0c7)
    for entry in [0x0807afb8, 0x0807aff0, 0x0807b02c, 0x0807b058, 0x0807b098, 0x0807b0ac]:
        _disasm_stub(entry)
    _set_eol(0x0807afb8, 'lighten_the_load_dispatch_default: BLK2 table[0] default stub')
    _set_eol(0x0807aff0, 'lighten_the_load_dispatch_zone_check: BLK2 table[1] zone-check branch')
    _set_eol(0x0807b02c, 'lighten_the_load_dispatch_state_write: BLK2 table[2] state-write stub')
    _set_eol(0x0807b058, 'lighten_the_load_dispatch_slot_lookup: BLK2 table[3] slot-lookup stub')
    _set_eol(0x0807b098, 'lighten_the_load_dispatch_slot_sprite: BLK2 table[4] slot-sprite stub')
    _set_eol(0x0807b0ac, 'lighten_the_load_dispatch_player_extract: BLK2 table[5] player-extract stub')

    # ------------------------------------------------------------------
    # BLK3: 0x0807b4d4 / 0x2c (44B) -- fn_eligible Hero Kid + Hyena (shared)
    #   THUMB stub starts at 0x7b4d4 (push{r4..r6,lr} = 0xb570)
    #   0x7b4f4 = 0x4687 MOV PC,r0 CODE -- do NOT createDWord there!
    #   0x7b4f6 = 0x0000 alignment pad -- consumed by disasm
    #   Literal pool: gDuelPhaseFlags at 0x7b4f8, dispatch table ptr at 0x7b4fc
    # ------------------------------------------------------------------
    print("--- BLK3: fn_eligible_hero_kid_hyena (0x7b4d4/0x2c) ---")
    _clear_and_tmode(0x0807b4d4, 0x0807b4ff)
    _disasm_stub(0x0807b4d4)
    # CRITICAL: 0x7b4f4 = 0x4687 MOV PC,r0 (code, not data); consumed by DisassembleCommand
    # Do NOT createDWord at 0x7b4f4. Pool starts at 0x7b4f8.
    _create_dword(0x0807b4f8, 'gDuelPhaseFlags pool word: ldr from fn_eligible_hero_kid_hyena')
    _create_dword(0x0807b4fc, 'dispatch table ptr 0x0807b500: ldr from fn_eligible_hero_kid_hyena')
    _set_eol(0x0807b4d4, 'fn_eligible_hero_kid_hyena: shared stub for CID=0x19a7 (Hero Kid) and CID=0x1867 (Hyena)')
    plate_text = (
        "Shared fn_eligible stub for Hero Kid (CID=0x19a7) and Hyena (CID=0x1867). "
        "Both FS handler table entries at ROM FS 0x09e45428 and 0x09e46028 route here. "
        "Dispatch table: 0x0807b500 (29 entries)."
    )
    _create_fn(0x0807b4d4, 'fn_eligible_hero_kid_hyena', plate=plate_text)

    # ------------------------------------------------------------------
    # BLK4: 0x0807b574 / 0x144 (324B) -- Hero Kid/Hyena dispatch sub-stubs
    #   29-entry dispatch table at 0x7b500..0x7b570 (already in asm as .word)
    #   7 unique sub-stubs (6 specialized + 1 default):
    #   0x7b574 (1 ref, table[28]), 0x7b5d0 (1 ref, table[27]), 0x7b630 (1 ref, table[26])
    #   0x7b680 (1 ref, table[25]), 0x7b690 (1 ref, table[20]), 0x7b6a2 (1 ref, table[0])
    #   0x7b6ac (23 refs = default for 23 of 29 table entries)
    # ------------------------------------------------------------------
    print("--- BLK4: Hero Kid/Hyena dispatch sub-stubs (0x7b574/0x144) ---")
    _clear_and_tmode(0x0807b574, 0x0807b6b7)
    for entry in [0x0807b574, 0x0807b5d0, 0x0807b630, 0x0807b680, 0x0807b690, 0x0807b6a2, 0x0807b6ac]:
        _disasm_stub(entry)
    _set_eol(0x0807b574, 'hero_kid_hyena_dispatch_base: BLK4 table[28] stub')
    _set_eol(0x0807b5d0, 'hero_kid_hyena_dispatch_5d0: BLK4 table[27] stub')
    _set_eol(0x0807b630, 'hero_kid_hyena_dispatch_630: BLK4 table[26] stub')
    _set_eol(0x0807b680, 'hero_kid_hyena_dispatch_680: BLK4 table[25] stub')
    _set_eol(0x0807b690, 'hero_kid_hyena_dispatch_690: BLK4 table[20] stub')
    _set_eol(0x0807b6a2, 'hero_kid_hyena_dispatch_6a2: BLK4 table[0] stub')
    _set_eol(0x0807b6ac, 'hero_kid_hyena_dispatch_default: BLK4 default (23 of 29 table entries)')

    # ------------------------------------------------------------------
    # BLK5: 0x0807b7dc / 0x28 (40B) -- fn_eligible Rescue Cat
    #   push{r4,r5,lr} = 0xb530 at 0x7b7dc
    #   Literal pool: gDuelPhaseFlags at 0x7b7fc, dispatch table ptr at 0x7b800
    #   Note: 0x7b800 raw refs=0 (no other addr stores 0x7b800); createDWord to prevent re-analysis
    # ------------------------------------------------------------------
    print("--- BLK5: fn_eligible_rescue_cat (0x7b7dc/0x28) ---")
    _clear_and_tmode(0x0807b7dc, 0x0807b803)
    _disasm_stub(0x0807b7dc)
    _create_dword(0x0807b7fc, 'gDuelPhaseFlags pool word: ldr from fn_eligible_rescue_cat')
    _create_dword(0x0807b800, 'dispatch table ptr 0x0807b804: ldr from fn_eligible_rescue_cat (raw refs=0, force-split)')
    _set_eol(0x0807b7dc, 'fn_eligible_rescue_cat CID=0x1876 (Rescue Cat); dispatch table at 0x0807b804 (29 entries)')
    _create_fn(0x0807b7dc, 'fn_eligible_rescue_cat')

    # ------------------------------------------------------------------
    # BLK6: 0x0807b878 / 0xe0 (224B) -- Rescue Cat dispatch sub-stubs
    #   29-entry dispatch table at 0x7b804..0x7b874 (already in asm as .word)
    #   7 unique sub-stubs:
    #   0x7b878 (1 ref base), 0x7b8cc (1 ref), 0x7b8e0 (1 ref, table[25])
    #   0x7b8fc (1 ref), 0x7b932 (1 ref), 0x7b944 (1 ref)
    #   0x7b94e (23 refs = default)
    # ------------------------------------------------------------------
    print("--- BLK6: Rescue Cat dispatch sub-stubs (0x7b878/0xe0) ---")
    _clear_and_tmode(0x0807b878, 0x0807b957)
    for entry in [0x0807b878, 0x0807b8cc, 0x0807b8e0, 0x0807b8fc, 0x0807b932, 0x0807b944, 0x0807b94e]:
        _disasm_stub(entry)
    _set_eol(0x0807b878, 'rescue_cat_dispatch_base: BLK6 table base stub')
    _set_eol(0x0807b8cc, 'rescue_cat_dispatch_8cc: BLK6 specialized stub')
    _set_eol(0x0807b8e0, 'rescue_cat_dispatch_8e0: BLK6 table[25] stub (1 ref)')
    _set_eol(0x0807b8fc, 'rescue_cat_dispatch_8fc: BLK6 specialized stub')
    _set_eol(0x0807b932, 'rescue_cat_dispatch_932: BLK6 specialized stub')
    _set_eol(0x0807b944, 'rescue_cat_dispatch_944: BLK6 specialized stub')
    _set_eol(0x0807b94e, 'rescue_cat_dispatch_default: BLK6 default (23 of 29 table entries)')

    # ------------------------------------------------------------------
    # BLK7: 0x0807b9f4 / 0x28 (40B) -- fn_eligible Gatling Dragon
    #   push{r4,r5,lr} = 0xb530 at 0x7b9f4
    #   Literal pool: gDuelPhaseFlags at 0x7ba14, dispatch table ptr at 0x7ba18
    # ------------------------------------------------------------------
    print("--- BLK7: fn_eligible_gatling_dragon (0x7b9f4/0x28) ---")
    _clear_and_tmode(0x0807b9f4, 0x0807ba1b)
    _disasm_stub(0x0807b9f4)
    _create_dword(0x0807ba14, 'gDuelPhaseFlags pool word: ldr from fn_eligible_gatling_dragon')
    _create_dword(0x0807ba18, 'dispatch table ptr 0x0807ba1c: ldr from fn_eligible_gatling_dragon')
    _set_eol(0x0807b9f4, 'fn_eligible_gatling_dragon CID=0x1878 (Gatling Dragon); dispatch table at 0x0807ba1c (5 entries)')
    _create_fn(0x0807b9f4, 'fn_eligible_gatling_dragon')

    # ------------------------------------------------------------------
    # BLK8: 0x0807ba30 / 0x100 (256B) -- Gatling Dragon dispatch sub-stubs
    #   5-entry dispatch table at 0x7ba1c..0x7ba2c (already in asm as .word)
    #   5 unique sub-stubs (no default needed, all unique):
    #   0x7ba30 (1 ref, table[4]), 0x7ba46 (1 ref, table[3]), 0x7ba84 (1 ref, table[2])
    #   0x7bad0 (1 ref, table[1]), 0x7bb24 (1 ref, table[0])
    # ------------------------------------------------------------------
    print("--- BLK8: Gatling Dragon dispatch sub-stubs (0x7ba30/0x100) ---")
    _clear_and_tmode(0x0807ba30, 0x0807bb2f)
    for entry in [0x0807ba30, 0x0807ba46, 0x0807ba84, 0x0807bad0, 0x0807bb24]:
        _disasm_stub(entry)
    _set_eol(0x0807ba30, 'gatling_dragon_dispatch_ba30: BLK8 table[4] stub')
    _set_eol(0x0807ba46, 'gatling_dragon_dispatch_ba46: BLK8 table[3] stub')
    _set_eol(0x0807ba84, 'gatling_dragon_dispatch_ba84: BLK8 table[2] stub')
    _set_eol(0x0807bad0, 'gatling_dragon_dispatch_bad0: BLK8 table[1] stub')
    _set_eol(0x0807bb24, 'gatling_dragon_dispatch_bb24: BLK8 table[0] stub')

    print("=== DisassembleF10Seg2Blocks Done ===")


main()
