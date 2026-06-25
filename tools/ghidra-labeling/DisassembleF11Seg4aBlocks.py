# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF11Seg4aBlocks.py -- f11 Seg-4a THUMB disassembly [0x08087d58..0x08088904)
#
# 21 real functions (equip zone scan callbacks):
#   fn01 0x08087d58  scan_zone_cid_12f4_substate_d
#   fn02 0x08087d9c  scan_zone_soul_release_substate_e
#   fn03 0x08087e08  scan_zone_last_will_substate_d
#   fn04 0x08087ebc  scan_zone_painful_choice_substate_d
#   fn05 0x08087fc0  scan_zone_magical_hats_substate_d
#   fn06 0x08088058  scan_zone_graverobber_substate_e
#   fn07 0x080880c0  scan_zone_summon_from_deck_group_a_substate_d
#   fn08 0x08088198  scan_zone_senju_substate_d
#   fn09 0x08088214  scan_zone_summon_from_deck_group_b_substate_d
#   fn10 0x08088284  scan_zone_sonic_bird_substate_d
#   fn11 0x08088304  scan_zone_dust_tornado_substate_b
#   fn12 0x08088360  scan_zone_graveyard_revival_group_substate_e
#   fn13 0x080883d4  scan_zone_spear_cretin_substate_e
#   fn14 0x0808846c  scan_zone_backup_soldier_substate_e
#   fn15 0x080884f8  scan_zone_serpentine_princess_substate_b
#   fn16 0x080885a8  scan_zone_cid_13ed_substate_b
#   fn17 0x080885d0  scan_zone_return_from_grave_group_substate_e
#   fn18 0x0808864c  scan_zone_de_fusion_substate_e
#   fn19 0x080886f8  scan_zone_insect_imitation_substate_d
#   fn20 0x080887b0  scan_zone_cid_1452_substate_e
#   fn21 0x0808882c  scan_zone_special_category_equip_group_substate_b
#
# Degenerate strong entries (NOT createFunction):
#   0x08088354 -- epilogue+pool of fn11; ref in compressed data
#   0x08088394 -- 2nd halfword of BL inside fn12; ref in compressed data
#   0x0808855a -- mid-loop body of fn15; ref in compressed data
#   0x0808866c -- mid-loop body of fn18; ref in compressed data
#   0x080887ec -- post-BL continuation of fn20; ref in compressed data
#   0x08088080 -- mid-loop body of fn06; ref in compressed data
#
# Literal pools (84 DWords): force-created after disasm
#
# Post-disasm gate: ROM_INCBIN/.byte in [0x08087d58..0x08088904) == 0
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
# 21 real function entry points (address order)
# ---------------------------------------------------------------------------
FUNC_ENTRIES = [
    (0x08087d58, 'scan_zone_cid_12f4_substate_d'),
    (0x08087d9c, 'scan_zone_soul_release_substate_e'),
    (0x08087e08, 'scan_zone_last_will_substate_d'),
    (0x08087ebc, 'scan_zone_painful_choice_substate_d'),
    (0x08087fc0, 'scan_zone_magical_hats_substate_d'),
    (0x08088058, 'scan_zone_graverobber_substate_e'),
    (0x080880c0, 'scan_zone_summon_from_deck_group_a_substate_d'),
    (0x08088198, 'scan_zone_senju_substate_d'),
    (0x08088214, 'scan_zone_summon_from_deck_group_b_substate_d'),
    (0x08088284, 'scan_zone_sonic_bird_substate_d'),
    (0x08088304, 'scan_zone_dust_tornado_substate_b'),
    (0x08088360, 'scan_zone_graveyard_revival_group_substate_e'),
    (0x080883d4, 'scan_zone_spear_cretin_substate_e'),
    (0x0808846c, 'scan_zone_backup_soldier_substate_e'),
    (0x080884f8, 'scan_zone_serpentine_princess_substate_b'),
    (0x080885a8, 'scan_zone_cid_13ed_substate_b'),
    (0x080885d0, 'scan_zone_return_from_grave_group_substate_e'),
    (0x0808864c, 'scan_zone_de_fusion_substate_e'),
    (0x080886f8, 'scan_zone_insect_imitation_substate_d'),
    (0x080887b0, 'scan_zone_cid_1452_substate_e'),
    (0x0808882c, 'scan_zone_special_category_equip_group_substate_b'),
]

# ---------------------------------------------------------------------------
# 84 literal pool DWords (all pools inside [0x08087d58..0x08088904))
# ---------------------------------------------------------------------------
POOL_DWORDS = [
    # fn01 (0x08087d58)
    0x08087d94, 0x08087d98,
    # fn02 (0x08087d9c)
    0x08087e00, 0x08087e04,
    # fn03 (0x08087e08)
    0x08087ea8, 0x08087eac, 0x08087eb0, 0x08087eb4, 0x08087eb8,
    # fn04 (0x08087ebc)
    0x08087f3c, 0x08087f40, 0x08087f44, 0x08087f48, 0x08087f4c,
    0x08087fb4, 0x08087fb8, 0x08087fbc,
    # fn05 (0x08087fc0)
    0x08088044, 0x08088048, 0x0808804c, 0x08088050, 0x08088054,
    # fn06 (0x08088058)
    0x080880b8, 0x080880bc,
    # fn07 (0x080880c0)
    0x08088180, 0x08088184, 0x08088188, 0x0808818c, 0x08088190, 0x08088194,
    # fn08 (0x08088198)
    0x08088208, 0x0808820c, 0x08088210,
    # fn09 (0x08088214)
    0x08088274, 0x08088278, 0x0808827c, 0x08088280,
    # fn10 (0x08088284)
    0x080882f8, 0x080882fc, 0x08088300,
    # fn11 (0x08088304)
    0x08088358, 0x0808835c,
    # fn12 (0x08088360)
    0x080883c8, 0x080883cc, 0x080883d0,
    # fn13 (0x080883d4)
    0x08088460, 0x08088464, 0x08088468,
    # fn14 (0x0808846c)
    0x080884e8, 0x080884ec, 0x080884f0, 0x080884f4,
    # fn15 (0x080884f8)
    0x08088598, 0x0808859c, 0x080885a0, 0x080885a4,
    # fn16 (0x080885a8)
    0x080885cc,
    # fn17 (0x080885d0)
    0x08088640, 0x08088644, 0x08088648,
    # fn18 (0x0808864c)
    0x080886e8, 0x080886ec, 0x080886f0, 0x080886f4,
    # fn19 (0x080886f8)
    0x080887a0, 0x080887a4, 0x080887a8, 0x080887ac,
    # fn20 (0x080887b0)
    0x08088820, 0x08088824, 0x08088828,
    # fn21 (0x0808882c)
    0x08088868, 0x0808886c, 0x08088870, 0x08088874, 0x08088880,
    0x08088898, 0x080888ac, 0x080888b4, 0x080888bc, 0x080888c4,
    0x080888cc, 0x080888d8, 0x08088900,
]


def main():
    if DRY:
        print("DRY RUN -- DisassembleF11Seg4aBlocks:")
        print("  clearListing + setTMode: 0x08087d58..0x08088904")
        print("  %d per-function DisassembleCommand entries" % len(FUNC_ENTRIES))
        print("  %d createFunction calls (degenerate skips: 0x08088354,0x08088394,"
              "0x0808855a,0x0808866c,0x080887ec,0x08088080)" % len(FUNC_ENTRIES))
        print("  %d createDWord pool slots" % len(POOL_DWORDS))
        print("  All text pure ASCII")
        return

    print("=== DisassembleF11Seg4aBlocks [0x08087d58..0x08088904) ===")

    # Step 1: clearListing + setTMode for entire range
    _clear_and_tmode(0x08087d58, 0x08088903)

    # Step 2: Per-function DisassembleCommand (21 entries, address order)
    print("--- Disassembling %d function entries ---" % len(FUNC_ENTRIES))
    for ep_addr, ep_name in FUNC_ENTRIES:
        _disasm_stub(ep_addr)

    # Step 3: createFunction for all 21 entries
    # NOTE: do NOT createFunction at degenerate addrs:
    #   0x08088354 (epilogue+pool fn11), 0x08088394 (mid-BL fn12),
    #   0x0808855a (mid-loop fn15), 0x0808866c (mid-loop fn18),
    #   0x080887ec (post-BL fn20), 0x08088080 (mid-loop fn06)
    print("--- Creating %d functions ---" % len(FUNC_ENTRIES))
    for ep_addr, ep_name in FUNC_ENTRIES:
        _create_func(ep_addr, ep_name)

    # Step 4: force-createDWord for all 84 pool addresses
    print("--- Creating %d literal pool DWords ---" % len(POOL_DWORDS))
    for pool_addr in POOL_DWORDS:
        _create_dword(pool_addr)

    print("")
    print("=== DisassembleF11Seg4aBlocks DONE ===")
    print("  disasm=%d  createFunc=%d  pool_dwords=%d" % (
        len(FUNC_ENTRIES), len(FUNC_ENTRIES), len(POOL_DWORDS)))
    print("  Degenerate skips (NOT createFunction):")
    print("    0x08088354 (epilogue+pool fn11)")
    print("    0x08088394 (mid-BL fn12)")
    print("    0x0808855a (mid-loop fn15)")
    print("    0x0808866c (mid-loop fn18)")
    print("    0x080887ec (post-BL fn20)")
    print("    0x08088080 (mid-loop fn06)")


main()
