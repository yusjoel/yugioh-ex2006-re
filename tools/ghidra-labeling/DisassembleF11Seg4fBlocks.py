# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF11Seg4fBlocks.py -- f11 Seg-4f THUMB disassembly [0x0808bb7c..0x0808cabc)
#
# 25 real functions (equip zone scan callbacks):
#   fn01 0x0808bb7c  scan_zone_rescue_cat_substate_d
#   fn02 0x0808bc10  scan_zone_a_feather_of_the_phoenix_substate_e
#   fn03 0x0808bc4c  scan_zone_centrifugal_field_substate_e
#   fn04 0x0808bd04  scan_zone_fulfillment_contract_substate_e
#   fn05 0x0808bd78  scan_zone_re_fusion_substate_e
#   fn06 0x0808bdec  scan_zone_beast_soul_swap_substate_b
#   fn07 0x0808be6c  scan_zone_vampire_genesis_substate_be
#   fn09 0x0808bfcc  scan_zone_king_skull_servants_substate_e
#   fn10 0x0808c058  scan_zone_double_attack_substate_b
#   fn11 0x0808c0c8  scan_zone_battery_charger_substate_e
#   fn12 0x0808c154  scan_zone_hero_signal_substate_bd
#   fn13 0x0808c264  scan_zone_level_conversion_lab_substate_b
#   fn14 0x0808c2a0  scan_zone_rock_bombardment_substate_d
#   fn15 0x0808c2f8  scan_zone_wroughtweiler_substate_e
#   fn16 0x0808c350  scan_zone_power_bond_substate_c
#   fn17 0x0808c3d0  scan_zone_summon_priest_substate_d
#   fn19 0x0808c45c  scan_zone_bubble_shuffle_substate_b
#   fn20 0x0808c4a8  scan_zone_fusion_recovery_substate_e
#   fn21 0x0808c4fc  scan_zone_miracle_fusion_substate_ce
#   fn22 0x0808c5ec  scan_zone_dragons_mirror_substate_ce
#   fn23 0x0808c6dc  scan_zone_spiritual_earth_art_substate_e
#   fn24 0x0808c790  scan_zone_a_rival_appears_substate_b
#   fn25 0x0808c808  scan_zone_gilford_the_legend_substate_e
#   fn26 0x0808c97c  scan_zone_warrior_lady_wasteland_substate_d
#   fn27 0x0808ca64  scan_zone_divine_sword_phoenix_blade_substate_e
#
# Degenerate strong entries (NOT createFunction -- mid-body continuations):
#   0x0808be88 -- mid-body BNE after fn07 CMP; fn07+fn08 share single epilogue at 0x0808bfb2
#   0x0808c3da -- mid-body LDR r0 inside fn17; fn17+fn18 share single epilogue at 0x0808c444
#
# Weak entry (NOT createFunction):
#   0x0808bf4a -- mid-body MOV r4,r0 inside fn07 loop2 at offset+0xe from 0x0808bf3c
#
# Literal pools (93 DWords): force-created after disasm
#
# Post-disasm gate: ROM_INCBIN/.byte in [0x0808bb7c..0x0808cabc) == 0
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
# NOTE: 0x0808be88, 0x0808c3da (degenerate strong) and 0x0808bf4a (weak) are NOT here
# ---------------------------------------------------------------------------
FUNC_ENTRIES = [
    (0x0808bb7c, 'scan_zone_rescue_cat_substate_d'),
    (0x0808bc10, 'scan_zone_a_feather_of_the_phoenix_substate_e'),
    (0x0808bc4c, 'scan_zone_centrifugal_field_substate_e'),
    (0x0808bd04, 'scan_zone_fulfillment_contract_substate_e'),
    (0x0808bd78, 'scan_zone_re_fusion_substate_e'),
    (0x0808bdec, 'scan_zone_beast_soul_swap_substate_b'),
    (0x0808be6c, 'scan_zone_vampire_genesis_substate_be'),
    (0x0808bfcc, 'scan_zone_king_skull_servants_substate_e'),
    (0x0808c058, 'scan_zone_double_attack_substate_b'),
    (0x0808c0c8, 'scan_zone_battery_charger_substate_e'),
    (0x0808c154, 'scan_zone_hero_signal_substate_bd'),
    (0x0808c264, 'scan_zone_level_conversion_lab_substate_b'),
    (0x0808c2a0, 'scan_zone_rock_bombardment_substate_d'),
    (0x0808c2f8, 'scan_zone_wroughtweiler_substate_e'),
    (0x0808c350, 'scan_zone_power_bond_substate_c'),
    (0x0808c3d0, 'scan_zone_summon_priest_substate_d'),
    (0x0808c45c, 'scan_zone_bubble_shuffle_substate_b'),
    (0x0808c4a8, 'scan_zone_fusion_recovery_substate_e'),
    (0x0808c4fc, 'scan_zone_miracle_fusion_substate_ce'),
    (0x0808c5ec, 'scan_zone_dragons_mirror_substate_ce'),
    (0x0808c6dc, 'scan_zone_spiritual_earth_art_substate_e'),
    (0x0808c790, 'scan_zone_a_rival_appears_substate_b'),
    (0x0808c808, 'scan_zone_gilford_the_legend_substate_e'),
    (0x0808c97c, 'scan_zone_warrior_lady_wasteland_substate_d'),
    (0x0808ca64, 'scan_zone_divine_sword_phoenix_blade_substate_e'),
]

# ---------------------------------------------------------------------------
# 93 literal pool DWords (all inside [0x0808bb7c..0x0808cabc), all 4B aligned)
# ---------------------------------------------------------------------------
POOL_DWORDS = [
    # fn01 (0x0808bb7c)
    0x0808bc04, 0x0808bc08, 0x0808bc0c,
    # fn02 (0x0808bc10)
    0x0808bc44, 0x0808bc48,
    # fn03 (0x0808bc4c)
    0x0808bc9c, 0x0808bca0, 0x0808bca4, 0x0808bcfc, 0x0808bd00,
    # fn04 (0x0808bd04)
    0x0808bd6c, 0x0808bd70, 0x0808bd74,
    # fn05 (0x0808bd78)
    0x0808bde0, 0x0808bde4, 0x0808bde8,
    # fn06 (0x0808bdec)
    0x0808be5c, 0x0808be60, 0x0808be64, 0x0808be68,
    # fn07+fn08 (0x0808be6c) -- pool1 at 0x0808bf18..0x0808bf2c, pool2 at 0x0808bfc0..0x0808bfc8
    0x0808bf18, 0x0808bf1c, 0x0808bf20, 0x0808bf24, 0x0808bf28, 0x0808bf2c,
    0x0808bfc0, 0x0808bfc4, 0x0808bfc8,
    # fn09 (0x0808bfcc)
    0x0808c044, 0x0808c048, 0x0808c04c, 0x0808c050, 0x0808c054,
    # fn10 (0x0808c058)
    0x0808c0b8, 0x0808c0bc, 0x0808c0c0, 0x0808c0c4,
    # fn11 (0x0808c0c8)
    0x0808c148, 0x0808c14c, 0x0808c150,
    # fn12 (0x0808c154)
    0x0808c254, 0x0808c258, 0x0808c25c, 0x0808c260,
    # fn13 (0x0808c264)
    0x0808c298, 0x0808c29c,
    # fn14 (0x0808c2a0)
    0x0808c2f0, 0x0808c2f4,
    # fn15 (0x0808c2f8)
    0x0808c348, 0x0808c34c,
    # fn16 (0x0808c350)
    0x0808c3c4, 0x0808c3c8, 0x0808c3cc,
    # fn17+fn18 (0x0808c3d0)
    0x0808c450, 0x0808c454, 0x0808c458,
    # fn19 (0x0808c45c)
    0x0808c4a4,
    # fn20 (0x0808c4a8)
    0x0808c4f4, 0x0808c4f8,
    # fn21 (0x0808c4fc) -- pool1 at 0x0808c56c..0x0808c574, pool2 at 0x0808c5e4..0x0808c5e8
    0x0808c56c, 0x0808c570, 0x0808c574,
    0x0808c5e4, 0x0808c5e8,
    # fn22 (0x0808c5ec) -- pool1 at 0x0808c65c..0x0808c664, pool2 at 0x0808c6d4..0x0808c6d8
    0x0808c65c, 0x0808c660, 0x0808c664,
    0x0808c6d4, 0x0808c6d8,
    # fn23 (0x0808c6dc)
    0x0808c784, 0x0808c788, 0x0808c78c,
    # fn24 (0x0808c790)
    0x0808c7f8, 0x0808c7fc, 0x0808c800, 0x0808c804,
    # fn25 (0x0808c808)
    0x0808c894, 0x0808c898, 0x0808c918, 0x0808c91c, 0x0808c920, 0x0808c924, 0x0808c974, 0x0808c978,
    # fn26 (0x0808c97c)
    0x0808ca4c, 0x0808ca50, 0x0808ca54, 0x0808ca58, 0x0808ca5c, 0x0808ca60,
    # fn27 (0x0808ca64)
    0x0808cab4, 0x0808cab8,
]


def main():
    if DRY:
        print("DRY RUN -- DisassembleF11Seg4fBlocks:")
        print("  clearListing + setTMode: 0x0808bb7c..0x0808cabb")
        print("  %d per-function DisassembleCommand entries" % len(FUNC_ENTRIES))
        print("  %d createFunction calls" % len(FUNC_ENTRIES))
        print("  Degenerate strong skips (NOT createFunction):")
        print("    0x0808be88 (mid-body BNE after fn07 CMP; fn07+fn08 combined)")
        print("    0x0808c3da (mid-body LDR r0 inside fn17; fn17+fn18 combined)")
        print("  Weak entry skips (NOT createFunction):")
        print("    0x0808bf4a (mid-body MOV r4,r0 inside fn07 loop2)")
        print("  %d createDWord pool slots" % len(POOL_DWORDS))
        print("  All text pure ASCII")
        return

    print("=== DisassembleF11Seg4fBlocks [0x0808bb7c..0x0808cabc) ===")

    # Step 1: clearListing + setTMode for entire range
    _clear_and_tmode(0x0808bb7c, 0x0808cabb)

    # Step 2: Per-function DisassembleCommand (25 entries, address order)
    # NOTE: do NOT disasm at degenerate/weak addrs:
    #   0x0808be88, 0x0808c3da (degenerate strong -- mid-body continuations)
    #   0x0808bf4a (weak -- mid-body MOV)
    print("--- Disassembling %d function entries ---" % len(FUNC_ENTRIES))
    for ep_addr, ep_name in FUNC_ENTRIES:
        _disasm_stub(ep_addr)

    # Step 3: createFunction for all 25 entries
    print("--- Creating %d functions ---" % len(FUNC_ENTRIES))
    for ep_addr, ep_name in FUNC_ENTRIES:
        _create_func(ep_addr, ep_name)

    # Step 4: force-createDWord for all 93 pool addresses
    print("--- Creating %d literal pool DWords ---" % len(POOL_DWORDS))
    for pool_addr in POOL_DWORDS:
        _create_dword(pool_addr)

    print("")
    print("=== DisassembleF11Seg4fBlocks DONE ===")
    print("  disasm=%d  createFunc=%d  pool_dwords=%d" % (
        len(FUNC_ENTRIES), len(FUNC_ENTRIES), len(POOL_DWORDS)))
    print("  Degenerate strong skips (NOT createFunction):")
    print("    0x0808be88 (mid-body BNE after fn07 CMP; fn07+fn08 share epilogue 0x0808bfb2)")
    print("    0x0808c3da (mid-body LDR r0 inside fn17; fn17+fn18 share epilogue 0x0808c444)")
    print("  Weak entry skips (NOT createFunction):")
    print("    0x0808bf4a (mid-body MOV r4,r0 inside fn07 loop2 at +0xe from 0x0808bf3c)")


main()
