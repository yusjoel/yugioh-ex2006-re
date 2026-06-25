# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF11Seg4bBlocks.py -- f11 Seg-4b THUMB disassembly [0x08088904..0x0808962c)
#
# 25 real functions (equip zone scan callbacks):
#   fn01 0x08088904  scan_zone_kycoo_dark_blade_group_substate_e
#   fn02 0x0808896c  scan_zone_bazoo_substate_e
#   fn03 0x080889c4  scan_zone_removed_accumulator_group_substate_e
#   fn04 0x08088a34  scan_zone_destiny_board_substate_bd
#   fn05 0x08088ad4  scan_zone_dark_sage_substate_d
#   fn06 0x08088b2c  scan_zone_cathedral_of_nobles_substate_bdc
#   fn07 0x08088c9c  scan_zone_foolish_burial_substate_d
#   fn08 0x08088d2c  scan_zone_removed_spirit_elemental_group_substate_e
#   fn09 0x08088db8  scan_zone_supply_substate_e
#   fn10 0x08088e0c  scan_zone_skull_lair_substate_e
#   fn11 0x08088e64  scan_zone_miracle_dig_substate_f
#   fn12 0x08088ed8  scan_zone_rope_of_life_substate_e
#   fn13 0x08088f7c  scan_zone_marauding_captain_group_substate_b
#   fn14 0x08088fe0  scan_zone_warrior_search_group_substate_d
#   fn15 0x08089068  scan_zone_warrior_returning_alive_substate_e
#   fn16 0x080890c0  scan_zone_spirit_ryu_substate_b
#   fn17 0x08089114  scan_zone_des_feral_imp_substate_e
#   fn18 0x08089150  scan_zone_agido_substate_e
#   fn19 0x080891f8  scan_zone_silent_fiend_soul_res_group_substate_e
#   fn20 0x08089284  scan_zone_maharaghi_substate_d
#   fn21 0x080892b4  scan_zone_super_robo_pair_substate_c
#   fn22 0x08089338  scan_zone_removed_zone_return_group_substate_e
#   fn23 0x08089378  scan_zone_last_turn_substate_d
#   fn25 0x0808941c  scan_zone_vampire_lord_lady_group_substate_d
#   fn26 0x08089558  scan_zone_pyramid_turtle_substate_d
#
# Degenerate strong entries (NOT createFunction):
#   0x0808939c -- mid-body bcs target of fn23 (Last Turn); NOT in dispatch table
#   0x08089560 -- mid-prologue second-push of fn26 (Pyramid Turtle); NOT in dispatch table
#
# Also NOT createFunction (weak entry):
#   0x8088ef6 -- mid-loop body of fn11 (Miracle Dig); ref from compressed data only
#
# Literal pools (~75 DWords): force-created after disasm
#
# Post-disasm gate: ROM_INCBIN/.byte in [0x08088904..0x0808962c) == 0
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
    (0x08088904, 'scan_zone_kycoo_dark_blade_group_substate_e'),
    (0x0808896c, 'scan_zone_bazoo_substate_e'),
    (0x080889c4, 'scan_zone_removed_accumulator_group_substate_e'),
    (0x08088a34, 'scan_zone_destiny_board_substate_bd'),
    (0x08088ad4, 'scan_zone_dark_sage_substate_d'),
    (0x08088b2c, 'scan_zone_cathedral_of_nobles_substate_bdc'),
    (0x08088c9c, 'scan_zone_foolish_burial_substate_d'),
    (0x08088d2c, 'scan_zone_removed_spirit_elemental_group_substate_e'),
    (0x08088db8, 'scan_zone_supply_substate_e'),
    (0x08088e0c, 'scan_zone_skull_lair_substate_e'),
    (0x08088e64, 'scan_zone_miracle_dig_substate_f'),
    (0x08088ed8, 'scan_zone_rope_of_life_substate_e'),
    (0x08088f7c, 'scan_zone_marauding_captain_group_substate_b'),
    (0x08088fe0, 'scan_zone_warrior_search_group_substate_d'),
    (0x08089068, 'scan_zone_warrior_returning_alive_substate_e'),
    (0x080890c0, 'scan_zone_spirit_ryu_substate_b'),
    (0x08089114, 'scan_zone_des_feral_imp_substate_e'),
    (0x08089150, 'scan_zone_agido_substate_e'),
    (0x080891f8, 'scan_zone_silent_fiend_soul_res_group_substate_e'),
    (0x08089284, 'scan_zone_maharaghi_substate_d'),
    (0x080892b4, 'scan_zone_super_robo_pair_substate_c'),
    (0x08089338, 'scan_zone_removed_zone_return_group_substate_e'),
    (0x08089378, 'scan_zone_last_turn_substate_d'),
    (0x0808941c, 'scan_zone_vampire_lord_lady_group_substate_d'),
    (0x08089558, 'scan_zone_pyramid_turtle_substate_d'),
]

# ---------------------------------------------------------------------------
# ~75 literal pool DWords (all inside [0x08088904..0x0808962c))
# ---------------------------------------------------------------------------
POOL_DWORDS = [
    # fn01 (0x08088904)
    0x08088964, 0x08088968,
    # fn02 (0x0808896c)
    0x080889bc, 0x080889c0,
    # fn03 (0x080889c4)
    0x08088a2c, 0x08088a30,
    # fn04 (0x08088a34)
    0x08088acc, 0x08088ad0,
    # fn05 (0x08088ad4)
    0x08088b24, 0x08088b28,
    # fn06 (0x08088b2c)
    0x08088c84, 0x08088c88, 0x08088c8c, 0x08088c90, 0x08088c94, 0x08088c98,
    # fn07 (0x08088c9c)
    0x08088d1c, 0x08088d20, 0x08088d24, 0x08088d28,
    # fn08 (0x08088d2c)
    0x08088dac, 0x08088db0, 0x08088db4,
    # fn09 (0x08088db8)
    0x08088e04, 0x08088e08,
    # fn10 (0x08088e0c)
    0x08088e5c, 0x08088e60,
    # fn11 (0x08088e64)
    0x08088ecc, 0x08088ed0, 0x08088ed4,
    # fn12 (0x08088ed8)
    # Note: two ldr ops both resolve to 0x08088f68; createDWord once
    0x08088f68, 0x08088f6c, 0x08088f70, 0x08088f74, 0x08088f78,
    # fn13 (0x08088f7c)
    0x08088fd8, 0x08088fdc,
    # fn14 (0x08088fe0)
    0x0808905c, 0x08089060, 0x08089064,
    # fn15 (0x08089068)
    0x080890b8, 0x080890bc,
    # fn16 (0x080890c0)
    0x0808910c, 0x08089110,
    # fn17 (0x08089114)
    0x08089148, 0x0808914c,
    # fn18 (0x08089150)
    0x080891bc, 0x080891c0, 0x080891c4, 0x080891f4,
    # fn19 (0x080891f8)
    0x08089278, 0x0808927c, 0x08089280,
    # fn20 (0x08089284)
    0x080892ac, 0x080892b0,
    # fn21 (0x080892b4): only valid CID pool words; 0x080892d4/0x080892d8 are CODE
    0x080892cc, 0x080892d0, 0x080892dc, 0x08089330, 0x08089334,
    # fn22 (0x08089338)
    0x08089370, 0x08089374,
    # fn23 (0x08089378, combined with 0x0808939c degenerate)
    0x0808940c, 0x08089410, 0x08089414, 0x08089418,
    # fn25 (0x0808941c)
    0x080894a4, 0x080894a8, 0x080894ac, 0x080894b0,
    0x080894f8, 0x080894fc,
    0x08089550, 0x08089554,
    # fn26 (0x08089558, combined with 0x08089560 degenerate)
    0x08089618, 0x0808961c, 0x08089620, 0x08089624, 0x08089628,
]


def main():
    if DRY:
        print("DRY RUN -- DisassembleF11Seg4bBlocks:")
        print("  clearListing + setTMode: 0x08088904..0x0808962c")
        print("  %d per-function DisassembleCommand entries" % len(FUNC_ENTRIES))
        print("  %d createFunction calls" % len(FUNC_ENTRIES))
        print("  Degenerate skips (NOT createFunction): 0x0808939c, 0x08089560")
        print("  Weak entry skip (NOT createFunction): 0x8088ef6")
        print("  %d createDWord pool slots" % len(POOL_DWORDS))
        print("  All text pure ASCII")
        return

    print("=== DisassembleF11Seg4bBlocks [0x08088904..0x0808962c) ===")

    # Step 1: clearListing + setTMode for entire range
    _clear_and_tmode(0x08088904, 0x0808962b)

    # Step 2: Per-function DisassembleCommand (25 entries, address order)
    print("--- Disassembling %d function entries ---" % len(FUNC_ENTRIES))
    for ep_addr, ep_name in FUNC_ENTRIES:
        _disasm_stub(ep_addr)

    # Step 3: createFunction for all 25 entries
    # NOTE: do NOT createFunction at degenerate addrs:
    #   0x0808939c (mid-body bcs target of fn23 Last Turn)
    #   0x08089560 (mid-prologue second-push of fn26 Pyramid Turtle)
    # NOTE: do NOT createFunction at weak entry:
    #   0x8088ef6 (mid-loop body of fn11, ref from compressed data only)
    print("--- Creating %d functions ---" % len(FUNC_ENTRIES))
    for ep_addr, ep_name in FUNC_ENTRIES:
        _create_func(ep_addr, ep_name)

    # Step 4: force-createDWord for all pool addresses
    print("--- Creating %d literal pool DWords ---" % len(POOL_DWORDS))
    for pool_addr in POOL_DWORDS:
        _create_dword(pool_addr)

    print("")
    print("=== DisassembleF11Seg4bBlocks DONE ===")
    print("  disasm=%d  createFunc=%d  pool_dwords=%d" % (
        len(FUNC_ENTRIES), len(FUNC_ENTRIES), len(POOL_DWORDS)))
    print("  Degenerate skips (NOT createFunction):")
    print("    0x0808939c (mid-body bcs target of fn23 Last Turn)")
    print("    0x08089560 (mid-prologue second-push of fn26 Pyramid Turtle)")
    print("  Weak entry skip (NOT createFunction):")
    print("    0x8088ef6 (mid-loop fn11, compressed data ref only)")


main()
