# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF11Seg4dBlocks.py -- f11 Seg-4d THUMB disassembly [0x0808a2ac..0x0808ad8c)
#
# 24 real functions (equip zone scan callbacks):
#   fn01 0x0808a2ac  scan_zone_emblem_of_dragon_destroyer_substate_de
#   fn02 0x0808a378  scan_zone_reserved_icid_group_substate_d
#   fn03 0x0808a3b8  scan_zone_senri_eye_dark_scorpion_group_substate_d
#   fn04 0x0808a3e8  scan_zone_fairy_of_the_spring_substate_e
#   fn05 0x0808a440  scan_zone_arsenal_robber_substate_d
#   fn06 0x0808a498  scan_zone_magical_dimension_substate_b
#   fn07 0x0808a4f0  scan_zone_dark_scorpion_meanae_substate_de
#   fn08 0x0808a598  scan_zone_iron_blacksmith_kotetsu_substate_d
#   fn09 0x0808a5f0  scan_zone_pandemonium_substate_d
#   fn10 0x0808a67c  scan_zone_archfiend_roar_substate_e
#   fn11 0x0808a708  scan_zone_ray_of_hope_substate_e
#   fn12 0x0808a788  scan_zone_witch_doctor_of_chaos_substate_e
#   fn13 0x0808a83c  scan_zone_chaosrider_gustaph_substate_e
#   fn14 0x0808a894  scan_zone_chaos_envoy_group_substate_e
#   fn15 0x0808a920  scan_zone_recycle_substate_e
#   fn16 0x0808a978  scan_zone_primal_seed_substate_f
#   fn17 0x0808a9b4  scan_zone_dimension_removal_group_substate_f
#   fn18 0x0808aa38  scan_zone_manju_of_ten_thousand_hands_substate_d
#   fn19 0x0808aab4  scan_zone_salvage_substate_e
#   fn20 0x0808ab44  scan_zone_ultra_evolution_pill_substate_b
#   fn21 0x0808ab9c  scan_zone_jade_insect_whistle_substate_d
#   fn22 0x0808abf4  scan_zone_abyss_soldier_lady_ninja_group_substate_b
#   fn23 0x0808ac48  scan_zone_arsenal_summoner_substate_d
#   fn24 0x0808aca0  scan_zone_guardian_equip_group_substate_e
#
# Degenerate strong entries (NOT createFunction):
#   0x0808a44c -- mid-loop LDR r1,[PC+#n] inside fn05 (bytes 4911); no dispatch table entry
#   0x0808a450 -- mid-loop MUL r2,r1 inside fn05 (bytes 434a); no dispatch table entry
#   0x0808a996 -- mid-body MOVS r1,#0xf inside fn16 (bytes 210f); no dispatch table entry
#
# Weak entries (NOT createFunction):
#   0x0808a974 -- literal pool PLAYER_BLOCK_STRIDE (0x00000868) in fn15 pool area
#   0x0808a9c2 -- mid-code MOV r1,r2 inside fn17 body (bytes 1c11)
#   0x0808ab2c -- epilogue bytes bcf0/bc01/0047 inside fn19 (fn19 POP+BX)
#
# Literal pools (60 DWords): force-created after disasm
# NOTE: 0x0808ab92 = 0x0000 is alignment padding (2B gap before fn20 pool) -- skip
#
# Post-disasm gate: ROM_INCBIN/.byte in [0x0808a2ac..0x0808ad8c) == 0
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
# 24 real function entry points (address order)
# ---------------------------------------------------------------------------
FUNC_ENTRIES = [
    (0x0808a2ac, 'scan_zone_emblem_of_dragon_destroyer_substate_de'),
    (0x0808a378, 'scan_zone_reserved_icid_group_substate_d'),
    (0x0808a3b8, 'scan_zone_senri_eye_dark_scorpion_group_substate_d'),
    (0x0808a3e8, 'scan_zone_fairy_of_the_spring_substate_e'),
    (0x0808a440, 'scan_zone_arsenal_robber_substate_d'),
    (0x0808a498, 'scan_zone_magical_dimension_substate_b'),
    (0x0808a4f0, 'scan_zone_dark_scorpion_meanae_substate_de'),
    (0x0808a598, 'scan_zone_iron_blacksmith_kotetsu_substate_d'),
    (0x0808a5f0, 'scan_zone_pandemonium_substate_d'),
    (0x0808a67c, 'scan_zone_archfiend_roar_substate_e'),
    (0x0808a708, 'scan_zone_ray_of_hope_substate_e'),
    (0x0808a788, 'scan_zone_witch_doctor_of_chaos_substate_e'),
    (0x0808a83c, 'scan_zone_chaosrider_gustaph_substate_e'),
    (0x0808a894, 'scan_zone_chaos_envoy_group_substate_e'),
    (0x0808a920, 'scan_zone_recycle_substate_e'),
    (0x0808a978, 'scan_zone_primal_seed_substate_f'),
    (0x0808a9b4, 'scan_zone_dimension_removal_group_substate_f'),
    (0x0808aa38, 'scan_zone_manju_of_ten_thousand_hands_substate_d'),
    (0x0808aab4, 'scan_zone_salvage_substate_e'),
    (0x0808ab44, 'scan_zone_ultra_evolution_pill_substate_b'),
    (0x0808ab9c, 'scan_zone_jade_insect_whistle_substate_d'),
    (0x0808abf4, 'scan_zone_abyss_soldier_lady_ninja_group_substate_b'),
    (0x0808ac48, 'scan_zone_arsenal_summoner_substate_d'),
    (0x0808aca0, 'scan_zone_guardian_equip_group_substate_e'),
]

# ---------------------------------------------------------------------------
# 60 literal pool DWords (all inside [0x0808a2ac..0x0808ad8c))
# NOTE: 0x0808ab92 = 0x0000 is alignment padding (2B gap), NOT a pool DWord -- omitted
# ---------------------------------------------------------------------------
POOL_DWORDS = [
    # fn01 (0x0808a2ac)
    0x0808a364, 0x0808a368, 0x0808a36c, 0x0808a370, 0x0808a374,
    # fn02 (0x0808a378)
    0x0808a3b0, 0x0808a3b4,
    # fn03 (0x0808a3b8)
    0x0808a3e0, 0x0808a3e4,
    # fn04 (0x0808a3e8)
    0x0808a438, 0x0808a43c,
    # fn05 (0x0808a440)
    0x0808a490, 0x0808a494,
    # fn06 (0x0808a498)
    0x0808a4e8, 0x0808a4ec,
    # fn07 (0x0808a4f0)
    0x0808a53c, 0x0808a540, 0x0808a590, 0x0808a594,
    # fn08 (0x0808a598)
    0x0808a5e8, 0x0808a5ec,
    # fn09 (0x0808a5f0)
    0x0808a670, 0x0808a674, 0x0808a678,
    # fn10 (0x0808a67c)
    0x0808a6fc, 0x0808a700, 0x0808a704,
    # fn11 (0x0808a708)
    0x0808a77c, 0x0808a780, 0x0808a784,
    # fn12 (0x0808a788)
    0x0808a834, 0x0808a838,
    # fn13 (0x0808a83c)
    0x0808a88c, 0x0808a890,
    # fn14 (0x0808a894)
    0x0808a914, 0x0808a918, 0x0808a91c,
    # fn15 (0x0808a920): 0x0808a974 is PLAYER_BLOCK_STRIDE pool -- included as DWord
    0x0808a970, 0x0808a974,
    # fn16 (0x0808a978)
    0x0808a9ac, 0x0808a9b0,
    # fn17 (0x0808a9b4)
    0x0808aa2c, 0x0808aa30, 0x0808aa34,
    # fn18 (0x0808aa38)
    0x0808aaa8, 0x0808aaac, 0x0808aab0,
    # fn19 (0x0808aab4)
    0x0808ab34, 0x0808ab38, 0x0808ab3c, 0x0808ab40,
    # fn20 (0x0808ab44): 0x0808ab92 is alignment padding (0x0000) -- omitted
    0x0808ab94, 0x0808ab98,
    # fn21 (0x0808ab9c)
    0x0808abec, 0x0808abf0,
    # fn22 (0x0808abf4)
    0x0808ac40, 0x0808ac44,
    # fn23 (0x0808ac48)
    0x0808ac98, 0x0808ac9c,
    # fn24 (0x0808aca0)
    0x0808ad78, 0x0808ad7c, 0x0808ad80, 0x0808ad84, 0x0808ad88,
]


def main():
    if DRY:
        print("DRY RUN -- DisassembleF11Seg4dBlocks:")
        print("  clearListing + setTMode: 0x0808a2ac..0x0808ad8b")
        print("  %d per-function DisassembleCommand entries" % len(FUNC_ENTRIES))
        print("  %d createFunction calls" % len(FUNC_ENTRIES))
        print("  Degenerate skips (NOT createFunction):")
        print("    0x0808a44c (mid-loop LDR r1 in fn05)")
        print("    0x0808a450 (mid-loop MUL r2,r1 in fn05)")
        print("    0x0808a996 (mid-body MOVS r1,#0xf in fn16)")
        print("  Weak entry skips (NOT createFunction):")
        print("    0x0808a974 (PLAYER_BLOCK_STRIDE pool literal in fn15 pool area)")
        print("    0x0808a9c2 (mid-code MOV r1,r2 inside fn17 body)")
        print("    0x0808ab2c (fn19 POP+BX epilogue bytes)")
        print("  %d createDWord pool slots (0x0808ab92 padding excluded)" % len(POOL_DWORDS))
        print("  All text pure ASCII")
        return

    print("=== DisassembleF11Seg4dBlocks [0x0808a2ac..0x0808ad8c) ===")

    # Step 1: clearListing + setTMode for entire range
    _clear_and_tmode(0x0808a2ac, 0x0808ad8b)

    # Step 2: Per-function DisassembleCommand (24 entries, address order)
    # NOTE: do NOT disasm at degenerate/weak addrs:
    #   0x0808a44c, 0x0808a450 (fn05 mid-loop)
    #   0x0808a974 (fn15 pool)
    #   0x0808a996 (fn16 mid-body)
    #   0x0808a9c2 (fn17 mid-code)
    #   0x0808ab2c (fn19 epilogue)
    print("--- Disassembling %d function entries ---" % len(FUNC_ENTRIES))
    for ep_addr, ep_name in FUNC_ENTRIES:
        _disasm_stub(ep_addr)

    # Step 3: createFunction for all 24 entries
    print("--- Creating %d functions ---" % len(FUNC_ENTRIES))
    for ep_addr, ep_name in FUNC_ENTRIES:
        _create_func(ep_addr, ep_name)

    # Step 4: force-createDWord for all pool addresses
    # NOTE: 0x0808ab92 (value=0x0000) is alignment padding, NOT a pool DWord
    print("--- Creating %d literal pool DWords ---" % len(POOL_DWORDS))
    for pool_addr in POOL_DWORDS:
        _create_dword(pool_addr)

    print("")
    print("=== DisassembleF11Seg4dBlocks DONE ===")
    print("  disasm=%d  createFunc=%d  pool_dwords=%d" % (
        len(FUNC_ENTRIES), len(FUNC_ENTRIES), len(POOL_DWORDS)))
    print("  Degenerate skips (NOT createFunction):")
    print("    0x0808a44c (mid-loop LDR r1 in fn05)")
    print("    0x0808a450 (mid-loop MUL r2,r1 in fn05)")
    print("    0x0808a996 (mid-body MOVS r1,#0xf in fn16)")
    print("  Weak entry skips (NOT createFunction):")
    print("    0x0808a974 (PLAYER_BLOCK_STRIDE pool literal in fn15 pool area)")
    print("    0x0808a9c2 (mid-code MOV r1,r2 inside fn17 body)")
    print("    0x0808ab2c (fn19 POP+BX epilogue bytes)")
    print("  Padding excluded: 0x0808ab92=0x0000 (alignment gap)")


main()
