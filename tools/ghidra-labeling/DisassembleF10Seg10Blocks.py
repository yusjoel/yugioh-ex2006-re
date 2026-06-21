# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF10Seg10Blocks.py -- f10 Seg-10 THUMB disassembly of 5 ROM_INCBIN blocks
#
# Blocks:
#   BLK1 0x8474e/0x2a: 2B zero-pad + fn_eligible_mobius_the_frost_monarch@0x08084750
#   BLK2 0x84790/0x164: Mobius dispatch sub-stubs (4 unique entries) + fn_eligible_hade_hane@0x080848cc
#   BLK3 0x84918/0x180: Hade-Hane dispatch sub-stubs (4 unique entries)
#   BLK4 0x84af2/0x2a: 2B zero-pad + fn_eligible_ojama_king@0x08084af4
#   BLK5 0x84b34/0x10c: Ojama King dispatch sub-stubs (3 unique entries)
#
# Key notes:
#   - 0x4687 opcodes within sub-stubs = MOV PC,r0 (THUMB code) -- NOT createDWord
#   - 0xe0xx/0xd0xx = THUMB unconditional/conditional branches -- NOT createDWord
#   - JT entries (already in asm as .word) -- NOT clearListed, NOT createDWord'd
#   - clearListing + setTMode before each block range; per-stub DisassembleCommand
#   - createFunction at fn_eligible entry points
#   - BLK4 fn entry 0x08084af4 = 0xb570 = push{r4,r5,r6,lr} (no r7; proposal note harmless)
#
# CID constants:
#   MOBIUS_THE_FROST_MONARCH_CID = 0x17e2 (NEW card_info.inc)
#   HADE_HANE_CID = 0x17ec (NEW card_info.inc)
#   OJAMA_KING_CARD_ID = 0x17ee (REUSE card_info.inc:120)

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
            print("[warn] label 0x%08x %s: %s" % (addr_int, label, e))
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
            print("[func] created %s @ 0x%08x" % (name, addr_int))
        except Exception as e:
            print("[warn] setName 0x%08x %s: %s" % (addr_int, name, e))
    else:
        print("[FAIL] createFunction 0x%08x %s" % (addr_int, name))


def main():
    if DRY:
        print("DRY RUN -- DisassembleF10Seg10Blocks: 5 blocks, 3 createFunction")
        return

    # =====================================================================
    # BLK1: 0x8474e/0x2a -- fn_eligible_mobius_the_frost_monarch
    # clearListing 0x0808474e..0x08084778 (stop before JT1 which is in asm)
    # fn entry at 0x08084750 (2B zero-pad at 0x8474e)
    # pool DWords: 0x08084770 (gDuelPhaseFlags) + 0x08084774 (JT1 base)
    # 0x0808476c = 0x4687 MOV PC,r0 -- THUMB code, NOT createDWord
    # JT1 (0x08084778..0x0808478f) = 6 .word entries, already in asm
    # =====================================================================
    print("=== BLK1: fn_eligible_mobius_the_frost_monarch @0x08084750 ===")
    _clear_and_tmode(0x0808474e, 0x08084778)
    _disasm_stub(0x08084750)
    _create_dword(0x08084770, 'gp1_mobius_blk1_pool0',
                  'gDuelPhaseFlags pool (fn_eligible_mobius_the_frost_monarch)')
    _create_dword(0x08084774, 'mobius_jt1_base_pool1',
                  'JT1 base = 0x08084778 (6 state dispatch entries for Mobius)')
    _create_func(0x08084750, 'fn_eligible_mobius_the_frost_monarch')
    _make_label(0x08084750, 'fn_eligible_mobius_the_frost_monarch',
                'fn_eligible: Mobius the Frost Monarch (MOBIUS_THE_FROST_MONARCH_CID=0x17e2); table 0x09e44cbc THUMB+1')

    # =====================================================================
    # BLK2: 0x84790/0x164 -- Mobius dispatch sub-stubs + fn_eligible_hade_hane
    # clearListing 0x08084790..0x080848f4 (stop before JT2)
    # 4 unique sub-stub entries: 0x08084790, 0x080847e4, 0x0808480c, 0x08084870
    # fn_eligible_hade_hane at 0x080848cc (push{lr}=0xb510; CID=0x17ec)
    # pool DWords listed below; NOT 0x4687 opcodes
    # JT2 (0x080848f4..0x08084918) = 9 .word entries, already in asm
    # =====================================================================
    print("=== BLK2: Mobius sub-stubs + fn_eligible_hade_hane @0x080848cc ===")
    _clear_and_tmode(0x08084790, 0x080848f4)

    _disasm_stub(0x08084790)  # state[0]
    _disasm_stub(0x080847e4)  # state[1,4] shared
    _disasm_stub(0x0808480c)  # state[2,5] shared
    _disasm_stub(0x08084870)  # state[3]
    _disasm_stub(0x080848cc)  # fn_eligible_hade_hane

    # Pool DWords in BLK2
    _create_dword(0x080847b4, None, 'DUAL_LABEL_RENDER_STATE_CLEAR pool (Mobius state[0] sub-stub)')
    _create_dword(0x080847dc, None, 'gP1LifePoints pool (Mobius state[1,4] sub-stub)')
    _create_dword(0x080847e0, None, 'gDuelPhaseFlags pool (Mobius state[1,4] sub-stub)')
    _create_dword(0x08084804, None, 'gP1LifePoints pool (Mobius state[2,5] sub-stub)')
    _create_dword(0x0808484c, None, 'gP1LifePoints pool (Mobius state[3] sub-stub)')
    _create_dword(0x08084850, None, 'ELIGIB_SPRITE_CTRL_OFF pool (Mobius state[3] sub-stub)')
    _create_dword(0x08084854, None, 'ELIGIB_ANIM_STATE_OFF pool (Mobius state[3] sub-stub)')
    _create_dword(0x0808486c, None, 'gDuelPhaseFlags pool (Mobius state[3] sub-stub)')
    _create_dword(0x080848a4, None, 'gDuelCardCtxBase pool (fn_eligible_hade_hane)')
    _create_dword(0x080848a8, None, 'gP1LifePoints pool (fn_eligible_hade_hane)')
    _create_dword(0x080848c8, None, 'gDuelPhaseFlags pool (fn_eligible_hade_hane)')
    _create_dword(0x080848ec, None, 'gDuelPhaseFlags pool (fn_eligible_hade_hane JT2 preamble)')
    _create_dword(0x080848f0, None, 'JT2 base = 0x080848f4 (9 state dispatch entries for Hade-Hane)')

    _create_func(0x080848cc, 'fn_eligible_hade_hane')
    _make_label(0x080848cc, 'fn_eligible_hade_hane',
                'fn_eligible: Hade-Hane (HADE_HANE_CID=0x17ec); dispatch table 0x09e44d04 THUMB+1')
    _make_label(0x08084790, 'mobius_dispatch_state_stubs',
                'Mobius the Frost Monarch (CID=0x17e2) state dispatch sub-stubs (BLK2)')

    # =====================================================================
    # BLK3: 0x84918/0x180 -- Hade-Hane dispatch sub-stubs
    # clearListing 0x08084918..0x08084af2
    # 4 unique sub-stub entries: 0x08084918, 0x0808498c, 0x080849f0, 0x08084a38
    # pool DWords listed below
    # =====================================================================
    print("=== BLK3: Hade-Hane sub-stubs @0x08084918..0x08084af2 ===")
    _clear_and_tmode(0x08084918, 0x08084af2)

    _disasm_stub(0x08084918)  # state[0]
    _disasm_stub(0x0808498c)  # state[3,6] shared
    _disasm_stub(0x080849f0)  # state[1,4,7] shared
    _disasm_stub(0x08084a38)  # state[2,5,8] shared

    # Pool DWords in BLK3
    _create_dword(0x08084968, None, 'DUAL_LABEL_RENDER_STATE_CLEAR pool (Hade-Hane state[0])')
    _create_dword(0x0808496c, None, 'gDuelCardCtxBase pool (Hade-Hane state[0])')
    _create_dword(0x08084970, None, 'gP1LifePoints pool (Hade-Hane state[0])')
    _create_dword(0x08084988, None, 'gDuelPhaseFlags pool (Hade-Hane state[0])')
    _create_dword(0x080849d0, None, 'gDuelCardCtxBase pool (Hade-Hane state[3,6])')
    _create_dword(0x080849d4, None, 'gP1LifePoints pool (Hade-Hane state[3,6])')
    _create_dword(0x080849ec, None, 'gDuelPhaseFlags pool (Hade-Hane state[3,6])')
    _create_dword(0x08084a10, None, 'gP1LifePoints pool (Hade-Hane state[1,4,7])')
    _create_dword(0x08084a34, None, 'gDuelPhaseFlags pool (Hade-Hane state[1,4,7])')
    _create_dword(0x08084a6c, None, 'gP1LifePoints pool (Hade-Hane state[2,5,8])')
    _create_dword(0x08084a70, None, 'ELIGIB_SPRITE_CTRL_OFF pool (Hade-Hane state[2,5,8])')
    _create_dword(0x08084a74, None, 'gDuelPhaseFlags pool (Hade-Hane state[2,5,8])')
    _create_dword(0x08084a8c, None, 'gDuelPhaseFlags pool (Hade-Hane state[2,5,8] exit)')

    _make_label(0x08084918, 'hade_hane_dispatch_state_stubs',
                'Hade-Hane (CID=0x17ec) state dispatch sub-stubs (BLK3)')

    # =====================================================================
    # BLK4: 0x84af2/0x2a -- fn_eligible_ojama_king
    # clearListing 0x08084af2..0x08084b1c (stop before JT3)
    # fn entry at 0x08084af4 (2B zero-pad at 0x84af2)
    # ROM: 0x08084af4 = 0xb570 = push{r4,r5,r6,lr}
    # pool DWords: 0x08084b14 (gDuelPhaseFlags) + 0x08084b18 (JT3 base)
    # JT3 (0x08084b1c..0x08084b33) = 6 .word entries, already in asm
    # CID: OJAMA_KING_CARD_ID=0x17ee (REUSE card_info.inc:120)
    # =====================================================================
    print("=== BLK4: fn_eligible_ojama_king @0x08084af4 ===")
    _clear_and_tmode(0x08084af2, 0x08084b1c)
    _disasm_stub(0x08084af4)
    _create_dword(0x08084b14, 'ojama_blk4_pool0',
                  'gDuelPhaseFlags pool (fn_eligible_ojama_king)')
    _create_dword(0x08084b18, 'ojama_jt3_base_pool1',
                  'JT3 base = 0x08084b1c (6 state dispatch entries for Ojama King)')
    _create_func(0x08084af4, 'fn_eligible_ojama_king')
    _make_label(0x08084af4, 'fn_eligible_ojama_king',
                'fn_eligible: Ojama King (OJAMA_KING_CARD_ID=0x17ee REUSE); dispatch table 0x09e44d1c THUMB+1')

    # =====================================================================
    # BLK5: 0x84b34/0x10c -- Ojama King dispatch sub-stubs
    # clearListing 0x08084b34..0x08084c40
    # 3 unique sub-stub entries: 0x08084b34, 0x08084b90, 0x08084bb4
    # pool DWords listed below (byte-scan verified)
    # KEY: 0x08084b60/bac/c10 = 0x08084a99 (check_equip_slot_target_not_blocked+1)
    #      NOT 0x08054899 which is at 0x08084fc8 in regular asm code
    # 0x4687 opcodes = MOV PC,r0 THUMB code -- NOT createDWord
    # =====================================================================
    print("=== BLK5: Ojama King sub-stubs @0x08084b34..0x08084c40 ===")
    _clear_and_tmode(0x08084b34, 0x08084c40)

    _disasm_stub(0x08084b34)  # state[0]
    _disasm_stub(0x08084b90)  # state[2,4] shared
    _disasm_stub(0x08084bb4)  # state[1,3,5] shared

    # Pool DWords in BLK5 (byte-scan verified)
    _create_dword(0x08084b5c, None, 'DUAL_LABEL_RENDER_STATE_CLEAR pool (Ojama King state[0])')
    _create_dword(0x08084b60, None, 'check_equip_slot_target_not_blocked_fn_ptr pool (state[0]); 0x08084a99')
    _create_dword(0x08084b8c, None, 'gDuelPhaseFlags pool (Ojama King state[0] exit)')
    _create_dword(0x08084bac, None, 'check_equip_slot_target_not_blocked_fn_ptr pool (state[1,3,5]); 0x08084a99')
    _create_dword(0x08084bb0, None, 'gDuelPhaseFlags pool (Ojama King state[1,3,5])')
    _create_dword(0x08084c08, None, 'gP1LifePoints pool (Ojama King state[2,4])')
    _create_dword(0x08084c0c, None, 'ELIGIB_SPRITE_CTRL_OFF pool (Ojama King state[2,4])')
    _create_dword(0x08084c10, None, 'check_equip_slot_target_not_blocked_fn_ptr pool (state[2,4]); 0x08084a99')
    _create_dword(0x08084c14, None, 'gDuelPhaseFlags pool (Ojama King state[2,4])')
    _create_dword(0x08084c34, None, 'gDuelPhaseFlags pool (Ojama King state[2,4] exit)')

    _make_label(0x08084b34, 'ojama_king_dispatch_state_stubs',
                'Ojama King (CID=0x17ee) state dispatch sub-stubs (BLK5)')

    print("")
    print("=== DisassembleF10Seg10Blocks DONE ===")
    print("Created: fn_eligible_mobius_the_frost_monarch@0x08084750")
    print("         fn_eligible_hade_hane@0x080848cc")
    print("         fn_eligible_ojama_king@0x08084af4")
    print("Disasm: BLK1(1stub)+BLK2(5stubs)+BLK3(4stubs)+BLK4(1stub)+BLK5(3stubs)")
    print("DWords: 2+13+13+2+10 = 40 createDWord calls")


main()
