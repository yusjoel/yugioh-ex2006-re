# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF11Seg4gBlocks.py -- f11 Seg-4g THUMB disassembly [0x0808cabc..0x0808d7f4)
#
# 20 real functions (equip zone scan callbacks):
#   fn01 0x0808cabc  scan_zone_level_modulation_substate_e
#   fn02 0x0808cb54  scan_zone_water_dragon_substate_e
#   fn03 0x0808cbd4  scan_zone_scarr_dark_world_substate_d
#   fn04 0x0808cc5c  scan_zone_pot_of_avarice_substate_e
#   fn05 0x0808ccb4  scan_zone_boss_rush_substate_d
#   fn06 0x0808cd34  scan_zone_gateway_dark_world_substate_e
#   fn07 0x0808cdc0  scan_zone_forces_of_darkness_substate_e
#   fn08 0x0808ce3c  scan_zone_roll_out_substate_e
#   fn09 0x0808cf88  scan_zone_armed_changer_substate_e_b
#   fn10 0x0808d054  scan_zone_magical_mallet_substate_b
#   fn11 0x0808d060  scan_zone_inferno_reckless_summon_substate_d_e_b
#   fn12 0x0808d1bc  scan_zone_white_horns_dragon_substate_e
#   fn13 0x0808d224  scan_zone_magnet_circle_lv2_substate_b
#   fn14 0x0808d294  scan_zone_ancient_gear_drill_substate_d
#   fn15 0x0808d324  scan_zone_damage_condenser_substate_d
#   fn16 0x0808d3d8  scan_zone_gokipon_substate_d
#   fn17 0x0808d494  scan_zone_symbol_of_heritage_substate_e
#   fn18 0x0808d5b0  scan_zone_generation_shift_substate_d_c
#   fn19 0x0808d694  scan_zone_flute_summoning_kuriboh_substate_d
#   fn20 0x0808d704  scan_zone_group_handler_multi_card
#
# Degenerate strong entries (NOT createFunction -- mid-body/mid-pool):
#   0x0808d20e -- mid-body CMP r2,r1 inside fn12 at offset+0x52 (fn12 range [0x0808d1bc..0x0808d224))
#   0x0808d21e -- upper half of pool word gP1LifePoints at 0x0808d21c inside fn12 pool
#   0x0808d7de -- alignment pad, upper half of SLOT_CARD_SET_CODE_MASK at 0x0808d7dc inside fn20 pool
#
# Weak entry (NOT createFunction):
#   0x0808d58c -- mid-body CMP r1,r0 inside fn17 at offset+0xf8 (fn17 range [0x0808d494..0x0808d5b0))
#
# Literal pools (82 DWords): force-created after disasm
#
# Post-disasm gate: ROM_INCBIN/.byte in [0x0808cabc..0x0808d7f4) == 0
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


# ---------------------------------------------------------------------------
# 20 real function entry points (address order)
# NOTE: 0x0808d20e, 0x0808d21e, 0x0808d7de (degenerate) and 0x0808d58c (weak) are NOT here
# ---------------------------------------------------------------------------
FUNC_ENTRIES = [
    (0x0808cabc, 'scan_zone_level_modulation_substate_e'),
    (0x0808cb54, 'scan_zone_water_dragon_substate_e'),
    (0x0808cbd4, 'scan_zone_scarr_dark_world_substate_d'),
    (0x0808cc5c, 'scan_zone_pot_of_avarice_substate_e'),
    (0x0808ccb4, 'scan_zone_boss_rush_substate_d'),
    (0x0808cd34, 'scan_zone_gateway_dark_world_substate_e'),
    (0x0808cdc0, 'scan_zone_forces_of_darkness_substate_e'),
    (0x0808ce3c, 'scan_zone_roll_out_substate_e'),
    (0x0808cf88, 'scan_zone_armed_changer_substate_e_b'),
    (0x0808d054, 'scan_zone_magical_mallet_substate_b'),
    (0x0808d060, 'scan_zone_inferno_reckless_summon_substate_d_e_b'),
    (0x0808d1bc, 'scan_zone_white_horns_dragon_substate_e'),
    (0x0808d224, 'scan_zone_magnet_circle_lv2_substate_b'),
    (0x0808d294, 'scan_zone_ancient_gear_drill_substate_d'),
    (0x0808d324, 'scan_zone_damage_condenser_substate_d'),
    (0x0808d3d8, 'scan_zone_gokipon_substate_d'),
    (0x0808d494, 'scan_zone_symbol_of_heritage_substate_e'),
    (0x0808d5b0, 'scan_zone_generation_shift_substate_d_c'),
    (0x0808d694, 'scan_zone_flute_summoning_kuriboh_substate_d'),
    (0x0808d704, 'scan_zone_group_handler_multi_card'),
]

# ---------------------------------------------------------------------------
# 82 literal pool DWords (all inside [0x0808cabc..0x0808d7f4), all 4B aligned)
# ---------------------------------------------------------------------------
POOL_DWORDS = [
    # fn01 (0x0808cabc) -- pool at 0x0808cb48..0x0808cb50
    0x0808cb48, 0x0808cb4c, 0x0808cb50,
    # fn02 (0x0808cb54) -- pool at 0x0808cbc8..0x0808cbd0
    0x0808cbc8, 0x0808cbcc, 0x0808cbd0,
    # fn03 (0x0808cbd4) -- pool at 0x0808cc50..0x0808cc58
    0x0808cc50, 0x0808cc54, 0x0808cc58,
    # fn04 (0x0808cc5c) -- pool at 0x0808ccac..0x0808ccb0
    0x0808ccac, 0x0808ccb0,
    # fn05 (0x0808ccb4) -- pool at 0x0808cd28..0x0808cd30
    0x0808cd28, 0x0808cd2c, 0x0808cd30,
    # fn06 (0x0808cd34) -- pool at 0x0808cdb4..0x0808cdbc
    0x0808cdb4, 0x0808cdb8, 0x0808cdbc,
    # fn07 (0x0808cdc0) -- pool at 0x0808ce30..0x0808ce38
    0x0808ce30, 0x0808ce34, 0x0808ce38,
    # fn08 (0x0808ce3c) -- pool1 at 0x0808cea4..0x0808cea8, pool2 at 0x0808cf24..0x0808cf84
    0x0808cea4, 0x0808cea8,
    0x0808cf24, 0x0808cf28, 0x0808cf2c, 0x0808cf30,
    0x0808cf80, 0x0808cf84,
    # fn09 (0x0808cf88) -- pool1 at 0x0808d004..0x0808d010, pool2 at 0x0808d04c..0x0808d050
    0x0808d004, 0x0808d008, 0x0808d00c, 0x0808d010,
    0x0808d04c, 0x0808d050,
    # fn10 (0x0808d054) -- no pool (12B stub, no pool slots)
    # fn11 (0x0808d060) -- pool at 0x0808d1a4..0x0808d1b8
    0x0808d1a4, 0x0808d1a8, 0x0808d1ac, 0x0808d1b0, 0x0808d1b4, 0x0808d1b8,
    # fn12 (0x0808d1bc) -- pool at 0x0808d21c..0x0808d220
    0x0808d21c, 0x0808d220,
    # fn13 (0x0808d224) -- pool at 0x0808d28c..0x0808d290
    0x0808d28c, 0x0808d290,
    # fn14 (0x0808d294) -- pool at 0x0808d318..0x0808d320
    0x0808d318, 0x0808d31c, 0x0808d320,
    # fn15 (0x0808d324) -- pool at 0x0808d3c8..0x0808d3d4
    0x0808d3c8, 0x0808d3cc, 0x0808d3d0, 0x0808d3d4,
    # fn16 (0x0808d3d8) -- pool at 0x0808d47c..0x0808d490
    0x0808d47c, 0x0808d480, 0x0808d484, 0x0808d488, 0x0808d48c, 0x0808d490,
    # fn17 (0x0808d494) -- pool at 0x0808d5a0..0x0808d5ac
    0x0808d5a0, 0x0808d5a4, 0x0808d5a8, 0x0808d5ac,
    # fn18 (0x0808d5b0) -- pool at 0x0808d684..0x0808d690
    0x0808d684, 0x0808d688, 0x0808d68c, 0x0808d690,
    # fn19 (0x0808d694) -- pool at 0x0808d6f4..0x0808d700
    0x0808d6f4, 0x0808d6f8, 0x0808d6fc, 0x0808d700,
    # fn20 (0x0808d704) -- pool1 at 0x0808d7a0, pool2 at 0x0808d7dc..0x0808d7e0
    0x0808d7a0,
    0x0808d7dc, 0x0808d7e0,
]


def main():
    if DRY:
        print("DRY RUN -- DisassembleF11Seg4gBlocks:")
        print("  clearListing + setTMode: 0x0808cabc..0x0808d7f3")
        print("  %d per-function DisassembleCommand entries" % len(FUNC_ENTRIES))
        print("  %d createFunction calls" % len(FUNC_ENTRIES))
        print("  Degenerate strong skips (NOT createFunction):")
        print("    0x0808d20e (mid-body CMP r2,r1 inside fn12 at offset+0x52)")
        print("    0x0808d21e (upper half pool word gP1LifePoints at 0x0808d21c inside fn12)")
        print("    0x0808d7de (align pad, upper half SLOT_CARD_SET_CODE_MASK at 0x0808d7dc inside fn20)")
        print("  Weak entry skips (NOT createFunction):")
        print("    0x0808d58c (mid-body CMP r1,r0 inside fn17 at offset+0xf8)")
        print("  %d createDWord pool slots" % len(POOL_DWORDS))
        print("  All text pure ASCII")
        return

    print("=== DisassembleF11Seg4gBlocks [0x0808cabc..0x0808d7f4) ===")

    # Step 1: clearListing + setTMode for entire range
    _clear_and_tmode(0x0808cabc, 0x0808d7f3)

    # Step 2: Per-function DisassembleCommand (20 entries, address order)
    # NOTE: do NOT disasm at degenerate addrs: 0x0808d20e, 0x0808d21e, 0x0808d7de
    # NOTE: do NOT disasm at weak addr: 0x0808d58c
    print("--- Disassembling %d function entries ---" % len(FUNC_ENTRIES))
    for ep_addr, ep_name in FUNC_ENTRIES:
        _disasm_stub(ep_addr)

    # Step 3: createFunction for all 20 entries
    print("--- Creating %d functions ---" % len(FUNC_ENTRIES))
    for ep_addr, ep_name in FUNC_ENTRIES:
        _create_func(ep_addr, ep_name)

    # Step 4: force-createDWord for all pool addresses
    print("--- Creating %d literal pool DWords ---" % len(POOL_DWORDS))
    for pool_addr in POOL_DWORDS:
        _create_dword(pool_addr)

    print("")
    print("=== DisassembleF11Seg4gBlocks DONE ===")
    print("  disasm=%d  createFunc=%d  pool_dwords=%d" % (
        len(FUNC_ENTRIES), len(FUNC_ENTRIES), len(POOL_DWORDS)))
    print("  Degenerate strong skips (NOT createFunction):")
    print("    0x0808d20e (mid-body CMP r2,r1 inside fn12 at offset+0x52)")
    print("    0x0808d21e (upper half pool word gP1LifePoints at 0x0808d21c)")
    print("    0x0808d7de (align pad, upper half SLOT_CARD_SET_CODE_MASK at 0x0808d7dc)")
    print("  Weak entry skip:")
    print("    0x0808d58c (mid-body CMP r1,r0 inside fn17 at offset+0xf8)")


main()
