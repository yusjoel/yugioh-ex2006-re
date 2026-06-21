# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# PoolFixF10Seg5a.py -- f10 Seg-5a literal pool DWord fix
#   33 inline literal pool words in BLK2/BLK3/BLK5/BLK6 sub-stubs
#   that were not converted to DWords by DisassembleF10Seg5aBlocks.py
#   (Ghidra disassembler treats them as data but exports as DAT_ labels)
#
# All values are known constants (PLAYER_BLOCK_STRIDE, EQUIP_PHASE_FRAME_OFF, etc.)
# or ewram offsets. createDWord forces the split; EOL is purely ASCII.

from ghidra.program.model.data import DWordDataType
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import SourceType

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

# (addr, label, eol_ascii)
POOL_DWORDS = [
    # BLK2 Magical Mallet sub-stub pools
    (0x0807dde0, 'mallet_stub0_frame_off',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: [gDuelPhaseFlags+0x4a4] equip phase frame slot'),
    (0x0807dde8, 'mallet_stub0_player_stride',
     'PLAYER_BLOCK_STRIDE=0x868: byte stride between P1/P2 data blocks'),
    (0x0807de78, 'mallet_stub2_banisher_off',
     'LP_BANISHER_CTX_OFF=0x1d70: [gP1LifePoints+0x1d70] LP banisher context offset'),
    (0x0807de7c, 'mallet_stub2_player_stride_b',
     'PLAYER_BLOCK_STRIDE=0x868: byte stride between P1/P2 data blocks'),
    (0x0807de84, 'mallet_stub2_frame_off_b',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: [gDuelPhaseFlags+0x4a4] equip phase frame slot'),
    (0x0807de9c, 'mallet_stub3_frame_off_b',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: [gDuelPhaseFlags+0x4a4] equip phase frame slot'),
    (0x0807dedc, 'mallet_stub4_frame_off_b',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: [gDuelPhaseFlags+0x4a4] equip phase frame slot'),

    # BLK3 equip_zone dispatch sub-stub pools
    (0x0807dff0, 'equip_zone_stub0_lp_next_off',
     '0x1d8c: LP linked-list next offset'),
    (0x0807e018, 'equip_zone_stub1_lp_track_base',
     'LP_CARD_TRACK_BASE_OFF=0x1da8: [gP1LifePoints+0x1da8] LP card tracking base'),
    (0x0807e0ac, 'equip_zone_stub2_player_stride',
     'PLAYER_BLOCK_STRIDE=0x868: byte stride between P1/P2 data blocks'),
    (0x0807e0b8, 'equip_zone_stub2_frame_off_b',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: [gDuelPhaseFlags+0x4a4] equip phase frame slot'),
    (0x0807e0dc, 'equip_zone_stub3_frame_off',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: [gDuelPhaseFlags+0x4a4] equip phase frame slot'),
    (0x0807e224, 'equip_zone_stub11_frame_off',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: [gDuelPhaseFlags+0x4a4] equip phase frame slot'),

    # BLK5 Ancient Gear Drill sub-stub pools
    (0x0807e4b0, 'ag_drill_stub0_frame_off',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: [gDuelPhaseFlags+0x4a4] equip phase frame slot'),
    (0x0807e534, 'ag_drill_stub1_phase_flags_b',
     'gDuelPhaseFlags=0x0201b290: duel phase flags struct base'),
    (0x0807e578, 'ag_drill_stub3_frame_off',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: [gDuelPhaseFlags+0x4a4] equip phase frame slot'),

    # BLK6 fn_eligible stub pools
    # stub1 BES Covered Core
    (0x0807e65c, 'bes_covered_stub1_stride',
     'PLAYER_BLOCK_STRIDE=0x868: byte stride between P1/P2 data blocks'),
    (0x0807e690, 'bes_covered_stub1_lp_field_off',
     '0x1d10: LP field offset in fn_eligible_bes_covered_core'),
    (0x0807e6b4, 'bes_covered_stub1_lp_field_off_b',
     '0x1d10: LP field offset dup B in fn_eligible_bes_covered_core'),
    (0x0807e6dc, 'bes_covered_stub1_lp_ctr_off',
     '0x1d7a: LP counter offset in fn_eligible_bes_covered_core'),
    # stub2 D.D. Guide
    (0x0807e75c, 'dd_guide_stub2_stride',
     'PLAYER_BLOCK_STRIDE=0x868: byte stride between P1/P2 data blocks'),
    (0x0807e7dc, 'dd_guide_stub2_lp_next_off',
     'LP_CARD_TRACK_NEXT_OFF=0x1daa: [gP1LifePoints+0x1daa] LP card track next field'),
    (0x0807e7e0, 'dd_guide_stub2_stride_b',
     'PLAYER_BLOCK_STRIDE=0x868: byte stride between P1/P2 data blocks'),
    # stub3 Disciple of Forbidden Spell
    (0x0807e8b4, 'disciple_stub3_stride',
     'PLAYER_BLOCK_STRIDE=0x868: byte stride between P1/P2 data blocks'),
    (0x0807e8e4, 'disciple_stub3_lp_track_base',
     'LP_CARD_TRACK_BASE_OFF=0x1da8: [gP1LifePoints+0x1da8] LP card tracking base'),
    (0x0807e8e8, 'disciple_stub3_frame_off',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: [gDuelPhaseFlags+0x4a4] equip phase frame slot'),
    (0x0807e940, 'disciple_stub3_frame_off_b',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: [gDuelPhaseFlags+0x4a4] equip phase frame slot'),
    (0x0807e944, 'disciple_stub3_stride_b',
     'PLAYER_BLOCK_STRIDE=0x868: byte stride between P1/P2 data blocks'),
    # stub4 Malice Ascendant
    (0x0807e9e0, 'malice_asc_stub4_stride',
     'PLAYER_BLOCK_STRIDE=0x868: byte stride between P1/P2 data blocks'),
    # stub5 Divine Dragon - Excelion
    (0x0807eadc, 'divine_dragon_stub5_stride',
     'PLAYER_BLOCK_STRIDE=0x868: byte stride between P1/P2 data blocks'),
    (0x0807eae4, 'divine_dragon_stub5_frame_off',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: [gDuelPhaseFlags+0x4a4] equip phase frame slot'),
    (0x0807eb5c, 'divine_dragon_stub5_op_code',
     '0x103: trigger op code constant in fn_eligible_divine_dragon_excelion'),
    (0x0807ebb4, 'divine_dragon_stub5_frame_off_b',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: [gDuelPhaseFlags+0x4a4] equip phase frame slot'),
]


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


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


def main():
    print("=== PoolFixF10Seg5a (DRY=%s) ===" % DRY)
    if DRY:
        print("[DRY] Would createDWord at %d addresses" % len(POOL_DWORDS))
        for (addr, label, eol) in POOL_DWORDS:
            print("[DRY]   0x%08x %s" % (addr, label))
        return

    n = 0
    for (addr_int, label, eol_text) in POOL_DWORDS:
        _create_dword(addr_int, label, eol_text)
        n += 1

    print("")
    print("=== SUMMARY: %d DWords created ===" % n)


main()
