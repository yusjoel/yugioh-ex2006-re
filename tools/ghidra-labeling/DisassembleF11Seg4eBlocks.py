# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF11Seg4eBlocks.py -- f11 Seg-4e THUMB disassembly [0x0808ad8c..0x0808bb7c)
#
# 25 real functions (equip zone scan callbacks):
#   fn01 0x0808ad8c  scan_zone_avatar_of_the_pot_substate_b
#   fn02 0x0808add0  scan_zone_monster_gate_substate_d
#   fn03 0x0808ae4c  scan_zone_archlord_zerato_light_group_substate_b
#   fn04 0x0808ae98  scan_zone_ninjitsu_transformation_substate_bd
#   fn05 0x0808affc  scan_zone_beckoning_light_substate_e
#   fn06 0x0808b07c  scan_zone_spirit_of_the_pharaoh_substate_e
#   fn07 0x0808b12c  scan_zone_nubian_guard_substate_e
#   fn08 0x0808b1ac  scan_zone_spirit_caller_substate_e
#   fn09 0x0808b240  scan_zone_emissary_of_the_afterlife_substate_d
#   fn10 0x0808b2c8  scan_zone_night_assailant_substate_e
#   fn11 0x0808b350  scan_zone_soul_reversal_substate_e
#   fn12 0x0808b3a8  scan_zone_human_wave_tactics_substate_d
#   fn13 0x0808b43c  scan_zone_first_sarcophagus_substate_bd
#   fn14 0x0808b454  scan_zone_howling_insect_group_substate_bd
#   fn15 0x0808b52c  scan_zone_dark_factory_mass_prod_substate_e
#   fn16 0x0808b584  scan_zone_abyssal_designator_substate_bd
#   fn17 0x0808b688  scan_zone_graveyard_fourth_dimension_substate_e
#   fn18 0x0808b6e0  scan_zone_two_man_cell_battle_substate_b
#   fn19 0x0808b750  scan_zone_big_wave_small_wave_substate_b
#   fn20 0x0808b7dc  scan_zone_magicians_circle_substate_d
#   fn21 0x0808b874  scan_zone_mokey_mokey_king_substate_e
#   fn22 0x0808b8e8  scan_zone_monster_reincarnation_substate_e
#   fn23 0x0808b940  scan_zone_lighten_the_load_substate_b
#   fn24 0x0808b988  scan_zone_behemoth_king_substate_e
#   fn25 0x0808b9e0  scan_zone_hex_sealed_fusion_group_substate_c
#
# Degenerate strong entries (NOT createFunction):
#   0x0808b40e -- mid-body MOVS r1,#0xd (bytes 210d) inside fn12 at offset+0x66; no dispatch entry
#   0x0808b95a -- mid-body LSRS r1,r1,#24 (bytes 0e09) inside fn23 at offset+0x1a; no dispatch entry
#
# Weak entries (NOT createFunction):
#   0x0808b58a -- mid-prologue MOV r5,r8 (bytes 4645) inside fn16 prologue at offset+0x06; no dispatch entry
#   0x0808b798 -- upper half of BL@0x0808b796 (bytes f9eb) inside fn19 body at offset+0x48; no dispatch entry
#
# Literal pools (76 DWords): force-created after disasm
#
# Post-disasm gate: ROM_INCBIN/.byte in [0x0808ad8c..0x0808bb7c) == 0
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
# 25 real function entry points (address order)
# ---------------------------------------------------------------------------
FUNC_ENTRIES = [
    (0x0808ad8c, 'scan_zone_avatar_of_the_pot_substate_b'),
    (0x0808add0, 'scan_zone_monster_gate_substate_d'),
    (0x0808ae4c, 'scan_zone_archlord_zerato_light_group_substate_b'),
    (0x0808ae98, 'scan_zone_ninjitsu_transformation_substate_bd'),
    (0x0808affc, 'scan_zone_beckoning_light_substate_e'),
    (0x0808b07c, 'scan_zone_spirit_of_the_pharaoh_substate_e'),
    (0x0808b12c, 'scan_zone_nubian_guard_substate_e'),
    (0x0808b1ac, 'scan_zone_spirit_caller_substate_e'),
    (0x0808b240, 'scan_zone_emissary_of_the_afterlife_substate_d'),
    (0x0808b2c8, 'scan_zone_night_assailant_substate_e'),
    (0x0808b350, 'scan_zone_soul_reversal_substate_e'),
    (0x0808b3a8, 'scan_zone_human_wave_tactics_substate_d'),
    (0x0808b43c, 'scan_zone_first_sarcophagus_substate_bd'),
    (0x0808b454, 'scan_zone_howling_insect_group_substate_bd'),
    (0x0808b52c, 'scan_zone_dark_factory_mass_prod_substate_e'),
    (0x0808b584, 'scan_zone_abyssal_designator_substate_bd'),
    (0x0808b688, 'scan_zone_graveyard_fourth_dimension_substate_e'),
    (0x0808b6e0, 'scan_zone_two_man_cell_battle_substate_b'),
    (0x0808b750, 'scan_zone_big_wave_small_wave_substate_b'),
    (0x0808b7dc, 'scan_zone_magicians_circle_substate_d'),
    (0x0808b874, 'scan_zone_mokey_mokey_king_substate_e'),
    (0x0808b8e8, 'scan_zone_monster_reincarnation_substate_e'),
    (0x0808b940, 'scan_zone_lighten_the_load_substate_b'),
    (0x0808b988, 'scan_zone_behemoth_king_substate_e'),
    (0x0808b9e0, 'scan_zone_hex_sealed_fusion_group_substate_c'),
]

# ---------------------------------------------------------------------------
# 76 literal pool DWords (all inside [0x0808ad8c..0x0808bb7c), all 4B aligned)
# ---------------------------------------------------------------------------
POOL_DWORDS = [
    # fn01 (0x0808ad8c)
    0x0808adc4, 0x0808adc8, 0x0808adcc,
    # fn02 (0x0808add0)
    0x0808ae40, 0x0808ae44, 0x0808ae48,
    # fn03 (0x0808ae4c)
    0x0808ae90, 0x0808ae94,
    # fn04 (0x0808ae98)
    0x0808afe4, 0x0808afe8, 0x0808afec, 0x0808aff0, 0x0808aff4, 0x0808aff8,
    # fn05 (0x0808affc)
    0x0808b070, 0x0808b074, 0x0808b078,
    # fn06 (0x0808b07c)
    0x0808b120, 0x0808b124, 0x0808b128,
    # fn07 (0x0808b12c)
    0x0808b1a0, 0x0808b1a4, 0x0808b1a8,
    # fn08 (0x0808b1ac)
    0x0808b234, 0x0808b238, 0x0808b23c,
    # fn09 (0x0808b240)
    0x0808b2bc, 0x0808b2c0, 0x0808b2c4,
    # fn10 (0x0808b2c8)
    0x0808b344, 0x0808b348, 0x0808b34c,
    # fn11 (0x0808b350)
    0x0808b3a0, 0x0808b3a4,
    # fn12 (0x0808b3a8)
    0x0808b430, 0x0808b434, 0x0808b438,
    # fn13 (0x0808b43c) -- no LDR PC-relative pool
    # fn14 (0x0808b454)
    0x0808b514, 0x0808b518, 0x0808b51c, 0x0808b520, 0x0808b524, 0x0808b528,
    # fn15 (0x0808b52c)
    0x0808b57c, 0x0808b580,
    # fn16 (0x0808b584)
    0x0808b674, 0x0808b678, 0x0808b67c, 0x0808b680, 0x0808b684,
    # fn17 (0x0808b688)
    0x0808b6d8, 0x0808b6dc,
    # fn18 (0x0808b6e0)
    0x0808b748, 0x0808b74c,
    # fn19 (0x0808b750)
    0x0808b7d0, 0x0808b7d4, 0x0808b7d8,
    # fn20 (0x0808b7dc)
    0x0808b868, 0x0808b86c, 0x0808b870,
    # fn21 (0x0808b874)
    0x0808b8d8, 0x0808b8dc, 0x0808b8e0, 0x0808b8e4,
    # fn22 (0x0808b8e8)
    0x0808b938, 0x0808b93c,
    # fn23 (0x0808b940)
    0x0808b980, 0x0808b984,
    # fn24 (0x0808b988)
    0x0808b9d8, 0x0808b9dc,
    # fn25 (0x0808b9e0)
    0x0808bb20, 0x0808bb24, 0x0808bb28, 0x0808bb2c, 0x0808bb74, 0x0808bb78,
]


def main():
    if DRY:
        print("DRY RUN -- DisassembleF11Seg4eBlocks:")
        print("  clearListing + setTMode: 0x0808ad8c..0x0808bb7b")
        print("  %d per-function DisassembleCommand entries" % len(FUNC_ENTRIES))
        print("  %d createFunction calls" % len(FUNC_ENTRIES))
        print("  Degenerate skips (NOT createFunction):")
        print("    0x0808b40e (mid-body MOVS r1,#0xd in fn12)")
        print("    0x0808b95a (mid-body LSRS r1,r1,#24 in fn23)")
        print("  Weak entry skips (NOT createFunction):")
        print("    0x0808b58a (mid-prologue MOV r5,r8 in fn16)")
        print("    0x0808b798 (upper half of BL inside fn19 body)")
        print("  %d createDWord pool slots" % len(POOL_DWORDS))
        print("  All text pure ASCII")
        return

    print("=== DisassembleF11Seg4eBlocks [0x0808ad8c..0x0808bb7c) ===")

    # Step 1: clearListing + setTMode for entire range
    _clear_and_tmode(0x0808ad8c, 0x0808bb7b)

    # Step 2: Per-function DisassembleCommand (25 entries, address order)
    # NOTE: do NOT disasm at degenerate/weak addrs:
    #   0x0808b40e, 0x0808b95a (degenerate strong -- mid-body)
    #   0x0808b58a, 0x0808b798 (weak -- mid-prologue/mid-BL)
    print("--- Disassembling %d function entries ---" % len(FUNC_ENTRIES))
    for ep_addr, ep_name in FUNC_ENTRIES:
        _disasm_stub(ep_addr)

    # Step 3: createFunction for all 25 entries
    print("--- Creating %d functions ---" % len(FUNC_ENTRIES))
    for ep_addr, ep_name in FUNC_ENTRIES:
        _create_func(ep_addr, ep_name)

    # Step 4: force-createDWord for all pool addresses
    print("--- Creating %d literal pool DWords ---" % len(POOL_DWORDS))
    for pool_addr in POOL_DWORDS:
        _create_dword(pool_addr)

    print("")
    print("=== DisassembleF11Seg4eBlocks DONE ===")
    print("  disasm=%d  createFunc=%d  pool_dwords=%d" % (
        len(FUNC_ENTRIES), len(FUNC_ENTRIES), len(POOL_DWORDS)))
    print("  Degenerate skips (NOT createFunction):")
    print("    0x0808b40e (mid-body MOVS r1,#0xd inside fn12 at +0x66)")
    print("    0x0808b95a (mid-body LSRS r1,r1,#24 inside fn23 at +0x1a)")
    print("  Weak entry skips (NOT createFunction):")
    print("    0x0808b58a (mid-prologue MOV r5,r8 inside fn16 prologue)")
    print("    0x0808b798 (upper half of BL@0x0808b796 inside fn19 body)")


main()
