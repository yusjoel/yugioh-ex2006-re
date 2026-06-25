# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF11Seg4cBlocks.py -- f11 Seg-4c THUMB disassembly [0x0808962c..0x0808a2ac)
#
# 23 real functions (equip zone scan callbacks):
#   fn01 0x0808962c  scan_zone_dark_scorpion_burglars_group_substate_d
#   fn02 0x08089684  scan_zone_book_of_life_substate_e
#   fn03 0x08089760  scan_zone_call_of_the_mummy_substate_b
#   fn04 0x080897b4  scan_zone_toon_table_of_contents_substate_d
#   fn05 0x0808980c  scan_zone_fushioh_richie_puppet_master_group_substate_e
#   fn06 0x08089898  scan_zone_lord_poison_substate_e
#   fn07 0x08089928  scan_zone_hidden_soldier_substate_b
#   fn08 0x08089990  scan_zone_monster_relief_familiar_knight_group_substate_b
#   fn09 0x080899e8  scan_zone_machine_duplication_group_substate_d
#   fn10 0x08089aa0  scan_zone_gravekeeper_spy_substate_d
#   fn11 0x08089b60  scan_zone_a_cat_of_ill_omen_substate_d
#   fn12 0x08089bb8  scan_zone_different_dimension_capsule_substate_d
#   fn13 0x08089c24  scan_zone_owl_of_luck_terraforming_group_substate_d
#   fn14 0x08089c7c  scan_zone_metamorphosis_substate_c
#   fn15 0x08089d08  scan_zone_rite_of_spirit_substate_e
#   fn16 0x08089d94  scan_zone_rope_of_spirit_substate_d
#   fn17 0x08089e44  scan_zone_goblin_zombie_substate_d
#   fn18 0x08089ed0  scan_zone_frontline_base_substate_b
#   fn19 0x08089f34  scan_zone_autonomous_action_unit_substate_e
#   fn20 0x08089fb8  scan_zone_tribute_doll_substate_b
#   fn21 0x0808a010  scan_zone_magic_evolution_group_substate_deb
#   fn22 0x0808a190  scan_zone_apprentice_magician_substate_d
#   fn23 0x0808a224  scan_zone_magical_scientist_substate_c
#
# Degenerate strong entries (NOT createFunction):
#   0x0808985e -- mid-loop BL opcode in fn05 (bytes f7ad fde9); no dispatch table entry
#   0x08089a58 -- mid-loop fall-through in fn09 (bytes 1c30 210b); no branch targets it
#   0x08089e78 -- mid-loop bitfield pair in fn17 (bytes 04c0 0cc4); no dispatch table entry
#   0x0808a28e -- mid-loop ldr+cmp+bcc in fn23 (bytes 6800 4285 d3da); no dispatch table entry
#
# Literal pools (76 DWords): force-created after disasm
# NOTE: 0x0808a046 = 0x0000 is alignment padding, NOT a pool DWord -- skip
#
# Post-disasm gate: ROM_INCBIN/.byte in [0x0808962c..0x0808a2ac) == 0
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
# 23 real function entry points (address order)
# ---------------------------------------------------------------------------
FUNC_ENTRIES = [
    (0x0808962c, 'scan_zone_dark_scorpion_burglars_group_substate_d'),
    (0x08089684, 'scan_zone_book_of_life_substate_e'),
    (0x08089760, 'scan_zone_call_of_the_mummy_substate_b'),
    (0x080897b4, 'scan_zone_toon_table_of_contents_substate_d'),
    (0x0808980c, 'scan_zone_fushioh_richie_puppet_master_group_substate_e'),
    (0x08089898, 'scan_zone_lord_poison_substate_e'),
    (0x08089928, 'scan_zone_hidden_soldier_substate_b'),
    (0x08089990, 'scan_zone_monster_relief_familiar_knight_group_substate_b'),
    (0x080899e8, 'scan_zone_machine_duplication_group_substate_d'),
    (0x08089aa0, 'scan_zone_gravekeeper_spy_substate_d'),
    (0x08089b60, 'scan_zone_a_cat_of_ill_omen_substate_d'),
    (0x08089bb8, 'scan_zone_different_dimension_capsule_substate_d'),
    (0x08089c24, 'scan_zone_owl_of_luck_terraforming_group_substate_d'),
    (0x08089c7c, 'scan_zone_metamorphosis_substate_c'),
    (0x08089d08, 'scan_zone_rite_of_spirit_substate_e'),
    (0x08089d94, 'scan_zone_rope_of_spirit_substate_d'),
    (0x08089e44, 'scan_zone_goblin_zombie_substate_d'),
    (0x08089ed0, 'scan_zone_frontline_base_substate_b'),
    (0x08089f34, 'scan_zone_autonomous_action_unit_substate_e'),
    (0x08089fb8, 'scan_zone_tribute_doll_substate_b'),
    (0x0808a010, 'scan_zone_magic_evolution_group_substate_deb'),
    (0x0808a190, 'scan_zone_apprentice_magician_substate_d'),
    (0x0808a224, 'scan_zone_magical_scientist_substate_c'),
]

# ---------------------------------------------------------------------------
# 76 literal pool DWords (all inside [0x0808962c..0x0808a2ac))
# NOTE: 0x0808a046 = 0x0000 is alignment padding, NOT a pool DWord -- omitted
# ---------------------------------------------------------------------------
POOL_DWORDS = [
    # fn01 (0x0808962c)
    0x0808967c, 0x08089680,
    # fn02 (0x08089684)
    0x080896f0, 0x080896f4, 0x080896f8, 0x08089758, 0x0808975c,
    # fn03 (0x08089760)
    0x080897ac, 0x080897b0,
    # fn04 (0x080897b4)
    0x08089804, 0x08089808,
    # fn05 (0x0808980c)
    0x0808988c, 0x08089890, 0x08089894,
    # fn06 (0x08089898)
    0x0808991c, 0x08089920, 0x08089924,
    # fn07 (0x08089928)
    0x08089988, 0x0808998c,
    # fn08 (0x08089990)
    0x080899e0, 0x080899e4,
    # fn09 (0x080899e8)
    0x08089a90, 0x08089a94, 0x08089a98, 0x08089a9c,
    # fn10 (0x08089aa0)
    0x08089b4c, 0x08089b50, 0x08089b54, 0x08089b58, 0x08089b5c,
    # fn11 (0x08089b60)
    0x08089bb0, 0x08089bb4,
    # fn12 (0x08089bb8)
    0x08089c18, 0x08089c1c, 0x08089c20,
    # fn13 (0x08089c24)
    0x08089c74, 0x08089c78,
    # fn14 (0x08089c7c)
    0x08089cfc, 0x08089d00, 0x08089d04,
    # fn15 (0x08089d08)
    0x08089d88, 0x08089d8c, 0x08089d90,
    # fn16 (0x08089d94)
    0x08089e34, 0x08089e38, 0x08089e3c, 0x08089e40,
    # fn17 (0x08089e44)
    0x08089ec4, 0x08089ec8, 0x08089ecc,
    # fn18 (0x08089ed0)
    0x08089f2c, 0x08089f30,
    # fn19 (0x08089f34)
    0x08089fac, 0x08089fb0, 0x08089fb4,
    # fn20 (0x08089fb8)
    0x0808a008, 0x0808a00c,
    # fn21 (0x0808a010): NOTE 0x0808a046=0x0000 is padding, NOT included
    0x0808a030, 0x0808a048, 0x0808a04c, 0x0808a058, 0x0808a064,
    0x0808a06c, 0x0808a078, 0x0808a080, 0x0808a08c, 0x0808a180,
    0x0808a184, 0x0808a188, 0x0808a18c,
    # fn22 (0x0808a190)
    0x0808a218, 0x0808a21c, 0x0808a220,
    # fn23 (0x0808a224)
    0x0808a2a0, 0x0808a2a4, 0x0808a2a8,
]


def main():
    if DRY:
        print("DRY RUN -- DisassembleF11Seg4cBlocks:")
        print("  clearListing + setTMode: 0x0808962c..0x0808a2ab")
        print("  %d per-function DisassembleCommand entries" % len(FUNC_ENTRIES))
        print("  %d createFunction calls" % len(FUNC_ENTRIES))
        print("  Degenerate skips (NOT createFunction):")
        print("    0x0808985e (mid-loop BL opcode in fn05)")
        print("    0x08089a58 (mid-loop fall-through in fn09)")
        print("    0x08089e78 (mid-loop bitfield pair in fn17)")
        print("    0x0808a28e (mid-loop ldr+cmp+bcc in fn23)")
        print("  %d createDWord pool slots (0x0808a046 padding excluded)" % len(POOL_DWORDS))
        print("  All text pure ASCII")
        return

    print("=== DisassembleF11Seg4cBlocks [0x0808962c..0x0808a2ac) ===")

    # Step 1: clearListing + setTMode for entire range
    _clear_and_tmode(0x0808962c, 0x0808a2ab)

    # Step 2: Per-function DisassembleCommand (23 entries, address order)
    print("--- Disassembling %d function entries ---" % len(FUNC_ENTRIES))
    for ep_addr, ep_name in FUNC_ENTRIES:
        _disasm_stub(ep_addr)

    # Step 3: createFunction for all 23 entries
    # NOTE: do NOT createFunction at degenerate addrs:
    #   0x0808985e (mid-loop BL opcode in fn05)
    #   0x08089a58 (mid-loop fall-through in fn09)
    #   0x08089e78 (mid-loop bitfield pair in fn17)
    #   0x0808a28e (mid-loop ldr+cmp+bcc in fn23)
    print("--- Creating %d functions ---" % len(FUNC_ENTRIES))
    for ep_addr, ep_name in FUNC_ENTRIES:
        _create_func(ep_addr, ep_name)

    # Step 4: force-createDWord for all pool addresses
    # NOTE: 0x0808a046 (value=0x0000) is alignment padding, NOT a pool DWord
    print("--- Creating %d literal pool DWords ---" % len(POOL_DWORDS))
    for pool_addr in POOL_DWORDS:
        _create_dword(pool_addr)

    print("")
    print("=== DisassembleF11Seg4cBlocks DONE ===")
    print("  disasm=%d  createFunc=%d  pool_dwords=%d" % (
        len(FUNC_ENTRIES), len(FUNC_ENTRIES), len(POOL_DWORDS)))
    print("  Degenerate skips (NOT createFunction):")
    print("    0x0808985e (mid-loop BL opcode in fn05)")
    print("    0x08089a58 (mid-loop fall-through in fn09)")
    print("    0x08089e78 (mid-loop bitfield pair in fn17)")
    print("    0x0808a28e (mid-loop ldr+cmp+bcc in fn23)")
    print("  Padding excluded: 0x0808a046=0x0000 (alignment)")


main()
