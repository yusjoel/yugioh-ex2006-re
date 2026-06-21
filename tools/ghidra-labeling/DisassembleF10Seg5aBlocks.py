# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF10Seg5aBlocks.py -- f10 Seg-5a R4 disasm (6 ROM_INCBIN blocks)
#
#   BLK1 0x0807dd68/0x30 (48B): fn_eligible_magical_mallet
#     THUMB+1 ref from FS dispatch table; CID 0x198d = MAGICAL_MALLET_CID
#     Pool: 0x0807dd90=gDuelPhaseFlags, 0x0807dd94=JT-base 0x0807dd98
#     TRAP: 0x4687 at 0x0807dd8e = THUMB MOV PC,r0 -- do NOT createDWord!
#
#   BLK2 0x0807ddac/0x16c (364B): Magical Mallet dispatch sub-stubs (5 entries)
#     JT at 0x0807dd98..0x0807ddab (5 words): targets 0x7ddac/0x7ddec/0x7de20/0x7dea4/0x7dec8
#     Pool words: 0x7dde4, 0x7de08, 0x7de0c, 0x7de1c, 0x7de74, 0x7de80, 0x7de98, 0x7dec4, 0x7df10, 0x7df14
#     TRAP: 0x4687 at 0x7df0e = THUMB MOV PC,r0 -- do NOT createDWord!
#
#   BLK3 0x0807df90/0x2bc (700B): dispatch_equip_zone_sprite sub-stubs (12 unique entries)
#     JT at PTR_DAT_0807df1c (29 entries); 12 unique targets
#     Pool words: 0x7dfec, 0x7e014, 0x7e0b0, 0x7e0b4, 0x7e160, 0x7e1a8
#     No 0x4687 in BLK3
#
#   BLK4 0x0807e398/0x2c (44B): fn_eligible_ancient_gear_drill
#     THUMB+1 ref from FS dispatch table; CID 0x19ae = ANCIENT_GEAR_DRILL_CID
#     Pool: 0x0807e3bc=gDuelPhaseFlags, 0x0807e3c0=JT-base 0x0807e3c4
#     TRAP: 0x4687 at 0x0807e3ba = THUMB MOV PC,r0 -- do NOT createDWord!
#
#   BLK5 0x0807e438/0x16c (364B): Ancient Gear Drill dispatch sub-stubs (7 entries)
#     JT at 0x0807e3c4..0x0807e437 (29 entries); 7 unique targets
#     Pool words: 0x7e4ac, 0x7e530
#     No 0x4687 in BLK5
#
#   BLK6 0x0807e5d4/0x63c (1596B): 5 x fn_eligible stubs (BES Covered Core / D.D. Guide /
#     Disciple of Forbidden Spell / Malice Ascendant / Divine Dragon - Excelion)
#     5 independent THUMB stubs; each has 1 THUMB+1 ref from FS dispatch table
#     Stub boundaries (from review):
#       stub1: 0x7e5d4..0x7e6df (268B) CID=0x19bf BES Covered Core
#       stub2: 0x7e6e0..0x7e7e3 (260B) CID=0x19c0 D.D. Guide
#       stub3: 0x7e7e4..0x7e95f (380B) CID=0x19c2 Disciple of Forbidden Spell
#       stub4: 0x7e960..0x7e9f7 (152B) CID=0x19d0 Malice Ascendant
#       stub5: 0x7e9f8..0x7ec0f (536B) CID=0x19d3 Divine Dragon - Excelion
#     Pool words in BLK6: 0x7e660, 0x7e664, 0x7e68c, 0x7e760, 0x7e798, 0x7e7d8,
#       0x7e820, 0x7e8b8, 0x7e8e0, 0x7e948, 0x7e9e4, 0x7ea44, 0x7eae0, 0x7eb1c,
#       0x7eb80, 0x7ebb0, 0x7ebf8
#
# NOTE: All EOL text is pure ASCII (no CJK).

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


def _create_function(addr_int, fn_name):
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


def main():
    print("=== DisassembleF10Seg5aBlocks (DRY=%s) ===" % DRY)

    if DRY:
        print("[DRY] Would process 6 ROM_INCBIN blocks:")
        print("[DRY] BLK1 0x0807dd68/0x30: fn_eligible_magical_mallet (push THUMB; 2 pool DWords)")
        print("[DRY]   NOTE: 0x0807dd8e=0x4687 MOV PC,r0 THUMB code -- NOT createDWord")
        print("[DRY] BLK2 0x0807ddac/0x16c: 5 Magical Mallet dispatch sub-stubs")
        print("[DRY]   5 entries: 0x7ddac/0x7ddec/0x7de20/0x7dea4/0x7dec8")
        print("[DRY]   10 pool DWords; NOTE: 0x7df0e=0x4687 MOV PC,r0 code -- NOT createDWord")
        print("[DRY] BLK3 0x0807df90/0x2bc: 12 equip_zone dispatch sub-stubs")
        print("[DRY]   12 entries; 6 pool DWords; no 0x4687")
        print("[DRY] BLK4 0x0807e398/0x2c: fn_eligible_ancient_gear_drill (push THUMB; 2 pool DWords)")
        print("[DRY]   NOTE: 0x0807e3ba=0x4687 MOV PC,r0 THUMB code -- NOT createDWord")
        print("[DRY] BLK5 0x0807e438/0x16c: 7 Ancient Gear Drill dispatch sub-stubs")
        print("[DRY]   7 entries; 2 pool DWords; no 0x4687")
        print("[DRY] BLK6 0x0807e5d4/0x63c: 5 fn_eligible stubs")
        print("[DRY]   5 entries: 0x7e5d4/0x7e6e0/0x7e7e4/0x7e960/0x7e9f8")
        print("[DRY]   17 pool DWords; no 0x4687")
        return

    # -----------------------------------------------------------------------
    # BLK1: fn_eligible_magical_mallet (0x0807dd68..0x0807dd97, 48B)
    # -----------------------------------------------------------------------
    print("--- BLK1: fn_eligible_magical_mallet ---")
    _clear_and_tmode(0x0807dd68, 0x0807dd97)
    _disasm_stub(0x0807dd68)  # push {r4,r5,r6,r7,lr} THUMB entry

    # Pool words at +0x28 and +0x2c; NOT the 0x4687 at +0x26 (0x0807dd8e = MOV PC,r0 code)
    _create_dword(0x0807dd90, 'mallet_eligible_phase_flags',
                  'gDuelPhaseFlags=0x0201b290: duel phase flags struct base')
    _create_dword(0x0807dd94, 'mallet_eligible_jtable_ptr',
                  '0x0807dd98: Magical Mallet dispatch jump table base (5 entries)')

    _create_function(0x0807dd68, 'fn_eligible_magical_mallet')

    # -----------------------------------------------------------------------
    # BLK2: Magical Mallet dispatch sub-stubs (0x0807ddac..0x0807df17, 364B)
    # -----------------------------------------------------------------------
    print("--- BLK2: Magical Mallet dispatch sub-stubs ---")
    _clear_and_tmode(0x0807ddac, 0x0807df17)

    # Per-stub DisassembleCommand (5 entry points)
    _disasm_stub(0x0807ddac)  # case0 (case 0 of JT, first entry)
    _disasm_stub(0x0807ddec)  # case1
    _disasm_stub(0x0807de20)  # case2
    _disasm_stub(0x0807dea4)  # case3
    _disasm_stub(0x0807dec8)  # case4

    # Pool DWords (10 total; NOT 0x7df0e=0x4687 MOV PC,r0 code)
    _create_dword(0x0807dde4, 'mallet_stub0_lp_base',
                  'gP1LifePoints=0x0201c4e0: LP state struct base')
    _create_dword(0x0807de08, 'mallet_stub1_card_ctx',
                  'gDuelCardCtxBase=0x0201e2a0: duel card activation context base')
    _create_dword(0x0807de0c, 'mallet_stub1_effect_ptr',
                  'invoke_effect_node_active_fn_ptr=0x08065991: THUMB+1 fn-ptr (slot B)')
    _create_dword(0x0807de1c, 'mallet_stub1_effect_ptr_b',
                  'invoke_effect_node_with_active_flag+1=0x08065991: dup check_equip_activation_at_slot11+1 (slot B)')
    _create_dword(0x0807de74, 'mallet_stub2_lp_base',
                  'gP1LifePoints=0x0201c4e0: LP state struct base (sub-stub 2)')
    _create_dword(0x0807de80, 'mallet_stub2_phase_flags',
                  'gDuelPhaseFlags=0x0201b290: duel phase flags struct base (sub-stub 2)')
    _create_dword(0x0807de98, 'mallet_stub3_phase_flags',
                  'gDuelPhaseFlags=0x0201b290: duel phase flags struct base (sub-stub 3)')
    _create_dword(0x0807dec4, 'mallet_stub3_frame_off',
                  'EQUIP_PHASE_FRAME_OFF=0x000004a4: [gDuelPhaseFlags+0x4a4] equip phase frame slot')
    _create_dword(0x0807df10, 'mallet_stub4_phase_flags',
                  'gDuelPhaseFlags=0x0201b290: duel phase flags struct base (sub-stub 4)')
    _create_dword(0x0807df14, 'mallet_stub4_frame_off',
                  'EQUIP_PHASE_FRAME_OFF=0x000004a4: [gDuelPhaseFlags+0x4a4] equip phase frame slot')

    # Sub-stub labels
    _create_label(0x0807ddac, 'equip_mallet_case0_0807ddac',
                  'Magical Mallet dispatch case 0 (JT entry 4)')
    _create_label(0x0807ddec, 'equip_mallet_case1_0807ddec',
                  'Magical Mallet dispatch case 1 (JT entry 3)')
    _create_label(0x0807de20, 'equip_mallet_case2_0807de20',
                  'Magical Mallet dispatch case 2 (JT entry 2)')
    _create_label(0x0807dea4, 'equip_mallet_case3_0807dea4',
                  'Magical Mallet dispatch case 3 (JT entry 1)')
    _create_label(0x0807dec8, 'equip_mallet_case4_0807dec8',
                  'Magical Mallet dispatch case 4 (JT entry 0)')

    # -----------------------------------------------------------------------
    # BLK3: dispatch_equip_zone_sprite sub-stubs (0x0807df90..0x0807e24b, 700B)
    # -----------------------------------------------------------------------
    print("--- BLK3: equip_zone dispatch sub-stubs (12 entries) ---")
    _clear_and_tmode(0x0807df90, 0x0807e24b)

    # 12 unique entry points from jump table at PTR_DAT_0807df1c
    _disasm_stub(0x0807df90)   # state 0x1c (JT entry[28])
    _disasm_stub(0x0807dff4)
    _disasm_stub(0x0807e01c)
    _disasm_stub(0x0807e0bc)
    _disasm_stub(0x0807e124)
    _disasm_stub(0x0807e164)
    _disasm_stub(0x0807e1c6)
    _disasm_stub(0x0807e1f0)
    _disasm_stub(0x0807e1fc)
    _disasm_stub(0x0807e208)
    _disasm_stub(0x0807e212)
    _disasm_stub(0x0807e242)   # default/fallthrough

    # Pool DWords (6 total; no 0x4687 in BLK3)
    _create_dword(0x0807dfec, 'equip_zone_stub0_lp_base',
                  'gP1LifePoints=0x0201c4e0: LP state struct base')
    _create_dword(0x0807e014, 'equip_zone_stub1_lp_base',
                  'gP1LifePoints=0x0201c4e0: LP state struct base (stub 1)')
    _create_dword(0x0807e0b0, 'equip_zone_stub2_field_slots',
                  'gDuelFieldSlots=0x0201c510: duel field zone slot array base')
    _create_dword(0x0807e0b4, 'equip_zone_stub2_phase_flags',
                  'gDuelPhaseFlags=0x0201b290: duel phase flags struct base')
    _create_dword(0x0807e160, 'equip_zone_stub5_oam_data',
                  '0x0201e500: equip zone OAM data base')
    _create_dword(0x0807e1a8, 'equip_zone_stub6_oam_data',
                  '0x0201e500: equip zone OAM data base (dup)')

    # Sub-stub labels
    _create_label(0x0807df90, 'equip_zone_stub_0807df90',
                  'equip zone sprite state sub-stub @ 0x0807df90 (state 0x1c)')
    _create_label(0x0807dff4, 'equip_zone_stub_0807dff4',
                  'equip zone sprite state sub-stub @ 0x0807dff4')
    _create_label(0x0807e01c, 'equip_zone_stub_0807e01c',
                  'equip zone sprite state sub-stub @ 0x0807e01c')
    _create_label(0x0807e0bc, 'equip_zone_stub_0807e0bc',
                  'equip zone sprite state sub-stub @ 0x0807e0bc')
    _create_label(0x0807e124, 'equip_zone_stub_0807e124',
                  'equip zone sprite state sub-stub @ 0x0807e124')
    _create_label(0x0807e164, 'equip_zone_stub_0807e164',
                  'equip zone sprite state sub-stub @ 0x0807e164')
    _create_label(0x0807e1c6, 'equip_zone_stub_0807e1c6',
                  'equip zone sprite state sub-stub @ 0x0807e1c6')
    _create_label(0x0807e1f0, 'equip_zone_stub_0807e1f0',
                  'equip zone sprite state sub-stub @ 0x0807e1f0')
    _create_label(0x0807e1fc, 'equip_zone_stub_0807e1fc',
                  'equip zone sprite state sub-stub @ 0x0807e1fc')
    _create_label(0x0807e208, 'equip_zone_stub_0807e208',
                  'equip zone sprite state sub-stub @ 0x0807e208')
    _create_label(0x0807e212, 'equip_zone_stub_0807e212',
                  'equip zone sprite state sub-stub @ 0x0807e212')
    _create_label(0x0807e242, 'equip_zone_stub_0807e242',
                  'equip zone sprite state sub-stub @ 0x0807e242 (default)')

    # -----------------------------------------------------------------------
    # BLK4: fn_eligible_ancient_gear_drill (0x0807e398..0x0807e423, 44B)
    # -----------------------------------------------------------------------
    print("--- BLK4: fn_eligible_ancient_gear_drill ---")
    _clear_and_tmode(0x0807e398, 0x0807e423)
    _disasm_stub(0x0807e398)  # push {r4,r5,r6,lr} THUMB entry

    # Pool words; NOT 0x7e3ba=0x4687 MOV PC,r0 code
    _create_dword(0x0807e3bc, 'ag_drill_eligible_phase_flags',
                  'gDuelPhaseFlags=0x0201b290: duel phase flags struct base')
    _create_dword(0x0807e3c0, 'ag_drill_eligible_jtable_ptr',
                  '0x0807e3c4: Ancient Gear Drill dispatch jump table base')

    _create_function(0x0807e398, 'fn_eligible_ancient_gear_drill')

    # -----------------------------------------------------------------------
    # BLK5: Ancient Gear Drill dispatch sub-stubs (0x0807e438..0x0807e5a3, 364B)
    # -----------------------------------------------------------------------
    print("--- BLK5: Ancient Gear Drill dispatch sub-stubs (7 entries) ---")
    _clear_and_tmode(0x0807e438, 0x0807e5a3)

    # 7 unique entry points (per proposal BLK5 section)
    _disasm_stub(0x0807e438)   # case0
    _disasm_stub(0x0807e46a)   # case1
    _disasm_stub(0x0807e47e)   # case2
    _disasm_stub(0x0807e538)   # case3
    _disasm_stub(0x0807e57c)   # case4
    _disasm_stub(0x0807e58e)   # case5
    _disasm_stub(0x0807e598)   # default

    # Pool DWords (2 total; no 0x4687)
    _create_dword(0x0807e4ac, 'ag_drill_stub0_phase_flags',
                  'gDuelPhaseFlags=0x0201b290: duel phase flags struct base (sub-stub 0)')
    _create_dword(0x0807e530, 'ag_drill_stub2_phase_flags',
                  'gDuelPhaseFlags=0x0201b290: duel phase flags struct base (sub-stub 2)')

    # Sub-stub labels
    _create_label(0x0807e438, 'ag_drill_case0_0807e438',
                  'AG Drill dispatch case 0')
    _create_label(0x0807e46a, 'ag_drill_case1_0807e46a',
                  'AG Drill dispatch case 1')
    _create_label(0x0807e47e, 'ag_drill_case2_0807e47e',
                  'AG Drill dispatch case 2')
    _create_label(0x0807e538, 'ag_drill_case3_0807e538',
                  'AG Drill dispatch case 3')
    _create_label(0x0807e57c, 'ag_drill_case4_0807e57c',
                  'AG Drill dispatch case 4')
    _create_label(0x0807e58e, 'ag_drill_case5_0807e58e',
                  'AG Drill dispatch case 5')
    _create_label(0x0807e598, 'ag_drill_default_0807e598',
                  'AG Drill dispatch default/fallthrough')

    # -----------------------------------------------------------------------
    # BLK6: 5 x fn_eligible stubs (0x0807e5d4..0x0807ec0f, 1596B)
    # -----------------------------------------------------------------------
    print("--- BLK6: 5 fn_eligible stubs ---")
    _clear_and_tmode(0x0807e5d4, 0x0807ec0f)

    # Per-stub DisassembleCommand (5 stubs; each independently disassembled)
    _disasm_stub(0x0807e5d4)   # stub1: BES Covered Core CID=0x19bf (268B)
    _disasm_stub(0x0807e6e0)   # stub2: D.D. Guide CID=0x19c0 (260B)
    _disasm_stub(0x0807e7e4)   # stub3: Disciple of Forbidden Spell CID=0x19c2 (380B)
    _disasm_stub(0x0807e960)   # stub4: Malice Ascendant CID=0x19d0 (152B)
    _disasm_stub(0x0807e9f8)   # stub5: Divine Dragon - Excelion CID=0x19d3 (536B)

    # Pool DWords (17 total; no 0x4687 in BLK6)
    # stub1 (BES Covered Core) pools
    _create_dword(0x0807e660, 'bes_covered_stub1_field_slots',
                  'gDuelFieldSlots=0x0201c510: duel field zone slot array base')
    _create_dword(0x0807e664, 'bes_covered_stub1_phase_flags',
                  'gDuelPhaseFlags=0x0201b290: duel phase flags struct base')
    _create_dword(0x0807e68c, 'bes_covered_stub1_card_ctx',
                  'gDuelCardCtxBase=0x0201e2a0: duel card activation context base')
    # stub2 (D.D. Guide) pools
    _create_dword(0x0807e760, 'dd_guide_stub2_field_slots',
                  'gDuelFieldSlots=0x0201c510: duel field zone slot array base')
    _create_dword(0x0807e798, 'dd_guide_stub2_phase_flags',
                  'gDuelPhaseFlags=0x0201b290: duel phase flags struct base')
    _create_dword(0x0807e7d8, 'dd_guide_stub2_lp_base',
                  'gP1LifePoints=0x0201c4e0: LP state struct base')
    # stub3 (Disciple of Forbidden Spell) pools
    _create_dword(0x0807e820, 'disciple_stub3_phase_flags',
                  'gDuelPhaseFlags=0x0201b290: duel phase flags struct base')
    _create_dword(0x0807e8b8, 'disciple_stub3_field_slots',
                  'gDuelFieldSlots=0x0201c510: duel field zone slot array base')
    _create_dword(0x0807e8e0, 'disciple_stub3_lp_base',
                  'gP1LifePoints=0x0201c4e0: LP state struct base')
    _create_dword(0x0807e948, 'disciple_stub3_field_slots_b',
                  'gDuelFieldSlots=0x0201c510: duel field zone slot array base (dup)')
    # stub4 (Malice Ascendant) pools
    _create_dword(0x0807e9e4, 'malice_asc_stub4_field_slots',
                  'gDuelFieldSlots=0x0201c510: duel field zone slot array base')
    # stub5 (Divine Dragon - Excelion) pools
    _create_dword(0x0807ea44, 'divine_dragon_stub5_phase_flags',
                  'gDuelPhaseFlags=0x0201b290: duel phase flags struct base')
    _create_dword(0x0807eae0, 'divine_dragon_stub5_field_slots',
                  'gDuelFieldSlots=0x0201c510: duel field zone slot array base')
    _create_dword(0x0807eb1c, 'divine_dragon_stub5_card_ctx',
                  'gDuelCardCtxBase=0x0201e2a0: duel card activation context base')
    _create_dword(0x0807eb80, 'divine_dragon_stub5_lp_base_a',
                  'gP1LifePoints=0x0201c4e0: LP state struct base (A)')
    _create_dword(0x0807ebb0, 'divine_dragon_stub5_lp_base_b',
                  'gP1LifePoints=0x0201c4e0: LP state struct base (B)')
    _create_dword(0x0807ebf8, 'divine_dragon_stub5_lp_base_c',
                  'gP1LifePoints=0x0201c4e0: LP state struct base (C)')

    # Create named functions for all 5 BLK6 fn_eligible stubs
    _create_function(0x0807e5d4, 'fn_eligible_bes_covered_core')
    _create_function(0x0807e6e0, 'fn_eligible_dd_guide')
    _create_function(0x0807e7e4, 'fn_eligible_disciple_forbidden_spell')
    _create_function(0x0807e960, 'fn_eligible_malice_ascendant')
    _create_function(0x0807e9f8, 'fn_eligible_divine_dragon_excelion')

    print("")
    print("=== DisassembleF10Seg5aBlocks DONE ===")
    print("=== BLK1: fn_eligible_magical_mallet @ 0x0807dd68 (2 pool DWords) ===")
    print("=== BLK2: 5 Magical Mallet sub-stubs @ 0x0807ddac (10 pool DWords) ===")
    print("=== BLK3: 12 equip_zone sub-stubs @ 0x0807df90 (6 pool DWords) ===")
    print("=== BLK4: fn_eligible_ancient_gear_drill @ 0x0807e398 (2 pool DWords) ===")
    print("=== BLK5: 7 AG Drill sub-stubs @ 0x0807e438 (2 pool DWords) ===")
    print("=== BLK6: 5 fn_eligible stubs @ 0x0807e5d4 (17 pool DWords) ===")
    print("=== createFunction: fn_eligible_magical_mallet + fn_eligible_ancient_gear_drill ===")
    print("=== createFunction: fn_eligible_bes_covered_core + fn_eligible_dd_guide ===")
    print("=== createFunction: fn_eligible_disciple_forbidden_spell ===")
    print("=== createFunction: fn_eligible_malice_ascendant + fn_eligible_divine_dragon_excelion ===")


main()
