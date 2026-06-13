# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF05Seg3Blocks.py -- f05 Seg-3 R4 disasm (3 blocks)
#
#   Block A: ROM_INCBIN 0x0804ae40, 0x60 (96B) = check_card_is_toon_type (1 function)
#     Entry: 0x0804ae40 (bx lr @ 0x0804ae9e)
#     BL caller: 0x080897e2
#
#   Block B: ROM_INCBIN 0x0804af88, 0xc0 (192B) = 2 functions
#     FuncC: check_card_is_guardian_type  @ 0x0804af88 (0x7c B, bx lr @ 0x0804b002)
#     FuncD: check_card_is_dark_scorpion_type @ 0x0804b004 (0x44 B, bx lr @ 0x0804b046)
#     BL callers: FuncC=0x0808ac76; FuncD=0x0808a51e/0x0808a56e/0x080b844e
#
#   Block C: ROM_INCBIN 0x0804b250, 0x34 (52B) + switch table/stub 0x0804b250..0x0804b2db
#     FuncE: check_card_is_batteryman_type @ 0x0804b250 (0x1e B, bx lr @ 0x0804b26a)
#     FuncF: check_card_is_dark_world_range_type @ 0x0804b26c (switch dispatch via bhi)
#     Inline stub: dark_world_range_case1_ret @ 0x0804b2d4 (8B: movs r0,#1; b; movs r0,#0; bx lr)
#     Switch table PTR_DAT_0804b288 @ 0x0804b288..0x0804b2d3 (0x4c B, 19 entries x 4B)
#     BL callers: FuncE=0x0808c10c/0x080b2eca; FuncF=0x0808cc18/0x0808cd78/0x0808ce04
#
#   Pattern: DisassembleSeg9BlockB / DisassembleF01Seg6Blocks
#   - clearListing entire block range
#   - setTMode=THUMB for entire range
#   - per-function DisassembleCommand (not per-stub: these are full-size functions)
#   - createFunction with name for each entry point
#   - EQ slots for literal pools applied via createLabel + equate
#
#   Note on Block C FuncF: switch table at 0x0804b288 is data (pointers to case stubs).
#   The table is INSIDE the disasm range. Ghidra should treat it as data automatically
#   due to the bhi dispatch pattern.
#
from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.app.cmd.function import CreateFunctionCmd
from ghidra.program.model.address import AddressSet
from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit
from java.math import BigInteger

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass


# ---------------------------------------------------------------------------
# Block ranges
# ---------------------------------------------------------------------------
BLOCK_A_LO  = 0x0804ae40
BLOCK_A_HI  = 0x0804ae9f   # inclusive

BLOCK_B_LO  = 0x0804af88
BLOCK_B_HI  = 0x0804b047   # inclusive

BLOCK_C_LO  = 0x0804b250
BLOCK_C_HI  = 0x0804b2db   # inclusive (includes switch table + inline stub)

# Function entry points + names (address, name, size_bytes)
FUNCTIONS = [
    # Block A
    (0x0804ae40, 'check_card_is_toon_type',              0x60),
    # Block B
    (0x0804af88, 'check_card_is_guardian_type',           0x7c),
    (0x0804b004, 'check_card_is_dark_scorpion_type',      0x44),
    # Block C
    (0x0804b250, 'check_card_is_batteryman_type',         0x1e),
    (0x0804b26c, 'check_card_is_dark_world_range_type',   0x68),  # up to 0x0804b2d3
]

# ---------------------------------------------------------------------------
# EQ_SLOTS for disasm blocks: (slot_addr, value, const_name, slot_label)
#   Applied AFTER disasm so the slots exist as code/data.
# ---------------------------------------------------------------------------
DISASM_EQ_SLOTS = [
    # Block A -- check_card_is_toon_type literal pool
    (0x0804ae60, 0x000012a5, 'BLUE_EYES_TOON_DRAGON_CID',   'toon_type_bey_cid'),
    (0x0804ae64, 0x00001123, 'TOON_ALLIGATOR_CID',           'toon_type_alligator_cid'),
    (0x0804ae68, 0x0000127f, 'TOON_SUMMONED_SKULL_CID',      'toon_type_summoned_skull_cid'),
    (0x0804ae80, 0x0000154a, 'TOON_DARK_MAGICIAN_GIRL_CID',  'toon_type_dmg_cid'),
    (0x0804ae84, 0x000012be, 'TOON_WORLD_CARD_ID',           'toon_type_world_cid'),
    (0x0804ae98, 0x00001566, 'TOON_GOBLIN_AF_CID',           'toon_type_goblin_af_cid'),
    # Block B -- check_card_is_guardian_type literal pool
    (0x0804afa8, 0x0000152e, 'GUARDIAN_SPHINX_CID',          'guardian_type_sphinx_cid'),
    (0x0804afac, 0x000011a7, 'GUARDIAN_OF_THRONE_ROOM_CID',  'guardian_type_throne_room_cid'),
    (0x0804afb0, 0x00000ffe, 'METAL_GUARDIAN_CID',           'guardian_type_metal_cid'),
    (0x0804afb4, 0x0000111c, 'GATE_GUARDIAN_CID',            'guardian_type_gate_cid'),
    (0x0804afc8, 0x00001266, 'SKULL_GUARDIAN_CID',           'guardian_type_skull_cid'),
    (0x0804afe8, 0x0000170b, 'GUARDIAN_ANGEL_JOAN_CID',      'guardian_type_angel_joan_cid'),
    (0x0804affc, 0x000018b0, 'LOST_GUARDIAN_CID',            'guardian_type_lost_cid'),
    # Block B -- check_card_is_dark_scorpion_type literal pool
    (0x0804b020, 0x00001686, 'DARK_SCORPION_MEANAE_CID',     'dark_scorpion_meanae_cid'),
    (0x0804b02c, 0x00001656, 'DARK_SCORPION_CHICK_CID',      'dark_scorpion_chick_cid'),
    (0x0804b040, 0x0000169e, 'MUSTERING_DARK_SCORPIONS_CID', 'dark_scorpion_mustering_cid'),
    # Block C -- check_card_is_batteryman_type literal pool
    (0x0804b264, 0x000018c3, 'BATTERYMAN_AA_CID',            'batteryman_type_aa_cid'),
]

# RENAME_SLOTS for disasm blocks
# check_card_is_guardian_type_cid_1452: 0x1452 is unassigned slot_id
# dark_world_range_base_neg: 0xffffe69f = -0x1961 (addend)
# dark_world_range_switch_table: PTR at 0x0804b288
# dark_world_range_case1_ret: inline stub at 0x0804b2d4
DISASM_RENAME_SLOTS = [
    (0x0804afcc, 'check_card_is_guardian_type_cid_1452',
     'unassigned slot_id 0x1452; possibly deleted Guardian card; low-conf'),
    (0x0804b280, 'dark_world_range_base_neg',
     '0xffffe69f = -0x1961; adds card_id to map to range [0..0x12] for switch dispatch'),
]

# REF_SLOTS for BlockC switch table
DISASM_REF_SLOTS = [
    # PTR_DAT_0804b288 holds ptr to dark_world_range_case1_ret = 0x0804b2d4
    (0x0804b288, 0x0804b2d4, 'dark_world_range_case1_ret', 'dark_world_range_switch_table'),
]

# PLATE comments for disasm functions (pure ASCII)
DISASM_PLATES = [
    (0x0804ae40,
     "Bool whitelist: returns 1 if card_id is a Toon-type card. "
     "Checks 6 Toon IDs: Blue-Eyes Toon Dragon (0x12a5), Toon Alligator (0x1123), "
     "Toon Summoned Skull (0x127f), Toon Dark Magician Girl (0x154a), "
     "Toon World (0x12be), Toon Goblin Attack Force (0x1566). "
     "bx lr at 0x0804ae9e. indeg=1 (0x080897e2)."),
    (0x0804af88,
     "Bool whitelist: returns 1 if card_id is a Guardian-type card. "
     "Checks 8 Guardian IDs: Guardian Sphinx (0x152e), Guardian of the Throne Room (0x11a7), "
     "Metal Guardian (0x0ffe), Gate Guardian (0x111c), Skull Guardian (0x1266), "
     "slot 0x1452 (unassigned), Guardian Angel Joan (0x170b), Lost Guardian (0x18b0). "
     "bx lr at 0x0804b002. indeg=1 (0x0808ac76)."),
    (0x0804b004,
     "Bool whitelist: returns 1 if card_id is a Dark Scorpion-type card. "
     "Checks IDs: range [0x1656..0x1658] (Dark Scorpion Chick+2), "
     "0x1686=Dark Scorpion Meanae, 0x169e=Mustering of the Dark Scorpions. "
     "bx lr at 0x0804b046. indeg=3 (0x0808a51e/0x0808a56e/0x080b844e)."),
    (0x0804b250,
     "Bool whitelist: returns 1 if card_id is Batteryman AA (0x18c3) or "
     "Batteryman C (0x191c, computed as 0x18c3+0x59 via adds). "
     "bx lr at 0x0804b26a. indeg=2 (0x0808c10c/0x080b2eca)."),
    (0x0804b26c,
     "Bool range-switch: card_id - 0x1961 in [0..0x12] -> 19-entry switch table. "
     "Return-1 IDs (Dark World cluster): Zure(0x1961), Beiige(0x1965), Broww(0x1966), "
     "Brron(0x1967), Sillva(0x1968), Goldd(0x1969), Scarr(0x196a), "
     "Dark World Lightning(0x1970), Gateway to Dark World(0x1973). "
     "Out-of-range or non-DW IDs at same range -> return 0. "
     "Name reflects BST range [0x1961..0x1973]; not pure Dark World semantic. "
     "indeg=3 (0x0808cc18/0x0808cd78/0x0808ce04)."),
]

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _clear_and_thumb(lo_int, hi_int):
    lo = _addr(lo_int)
    hi = _addr(hi_int)
    try:
        clearListing(lo, hi)
        print("[ok ] clearListing 0x%08x..0x%08x" % (lo_int, hi_int))
    except Exception as e:
        print("[warn] clearListing: %s" % e)
    ctx = currentProgram.getProgramContext()
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        ctx.setValue(tmode, lo, hi, BigInteger.ONE)
        print("[ok ] setTMode=THUMB 0x%08x..0x%08x" % (lo_int, hi_int))
    else:
        print("[warn] TMode register not found")


def _disasm_fn(addr_int, size):
    lo = _addr(addr_int)
    hi = _addr(addr_int + size - 1)
    cmd = DisassembleCommand(lo, AddressSet(lo, hi), True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm 0x%08x (%dB): %s" % (addr_int, size, cmd.getStatusMsg()))
        return False
    print("[ok ] disasm 0x%08x (%dB)" % (addr_int, size))
    return True


def _create_fn(addr_int, name):
    a = _addr(addr_int)
    fn_mgr = currentProgram.getFunctionManager()
    existing = fn_mgr.getFunctionAt(a)
    if existing is not None:
        if existing.getName() != name:
            existing.setName(name, SourceType.USER_DEFINED)
            print("[FN ] renamed 0x%08x -> %s" % (addr_int, name))
        else:
            print("[FN ] already exists 0x%08x: %s" % (addr_int, name))
        return
    cmd = CreateFunctionCmd(name, a, None, SourceType.USER_DEFINED)
    if cmd.applyTo(currentProgram):
        print("[FN ] created %s @ 0x%08x" % (name, addr_int))
    else:
        print("[warn] createFunction %s @ 0x%08x: %s" % (name, addr_int, cmd.getStatusMsg()))
        currentProgram.getSymbolTable().createLabel(a, name, SourceType.USER_DEFINED)
        print("[FN ] created label (fallback) %s @ 0x%08x" % (name, addr_int))


def _check_slot(slot_int, want):
    d = getDataAt(_addr(slot_int))
    if d is None or d.getLength() != 4:
        return False, "no 4B data"
    try:
        dv = d.getValue()
        iv = (int(dv.getValue()) & 0xffffffff) if hasattr(dv, 'getValue') else (int(dv) & 0xffffffff)
    except Exception:
        iv = None
    if iv is not None and iv != (want & 0xffffffff):
        return False, "value mismatch got=0x%x want=0x%x" % (iv, want)
    return True, None


def main():
    print("=== DisassembleF05Seg3Blocks (DRY=%s) ===" % DRY)
    listing = currentProgram.getListing()
    rm      = currentProgram.getReferenceManager()
    et      = currentProgram.getEquateTable()
    made    = set()

    if DRY:
        print("[dry] Blocks to disasm:")
        print("  BlockA 0x%08x..0x%08x (0x60 B) -> check_card_is_toon_type" % (BLOCK_A_LO, BLOCK_A_HI))
        print("  BlockB 0x%08x..0x%08x (0xc0 B) -> check_card_is_guardian_type + check_card_is_dark_scorpion_type" % (BLOCK_B_LO, BLOCK_B_HI))
        print("  BlockC 0x%08x..0x%08x -> check_card_is_batteryman_type + check_card_is_dark_world_range_type + switch table" % (BLOCK_C_LO, BLOCK_C_HI))
        print("[dry] Functions to create (%d):" % len(FUNCTIONS))
        for addr_int, name, size in FUNCTIONS:
            print("  0x%08x %s (%dB)" % (addr_int, name, size))
        print("[dry] EQ slots (%d), RENAME (%d), REF (%d), PLATE (%d)" % (
            len(DISASM_EQ_SLOTS), len(DISASM_RENAME_SLOTS), len(DISASM_REF_SLOTS), len(DISASM_PLATES)))
        return

    # --- 1. Clear + setTMode for each block ---
    _clear_and_thumb(BLOCK_A_LO, BLOCK_A_HI)
    _clear_and_thumb(BLOCK_B_LO, BLOCK_B_HI)
    _clear_and_thumb(BLOCK_C_LO, BLOCK_C_HI)

    # --- 2. Disassemble + create functions ---
    for addr_int, name, size in FUNCTIONS:
        _disasm_fn(addr_int, size)
        _create_fn(addr_int, name)

    # --- 3. Apply EQ slots in disasm blocks ---
    nEQ = 0
    for slot_int, value, cname, label in DISASM_EQ_SLOTS:
        ok, err = _check_slot(slot_int, value)
        if not ok:
            print("[EQ FAIL] 0x%08x: %s" % (slot_int, err)); continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        eq = et.getEquate(cname)
        if eq is None:
            eq = et.createEquate(cname, value)
        eq.addReference(_addr(slot_int), 0)
        print("[EQ ok] 0x%08x -> %s (%s)" % (slot_int, label, cname)); nEQ += 1

    # --- 4. RENAME_SLOTS in disasm blocks ---
    nRN = 0
    for slot_int, label, eol in DISASM_RENAME_SLOTS:
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        cu = listing.getCodeUnitAt(_addr(slot_int))
        if cu is not None and eol:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)
        print("[RN ok] 0x%08x -> %s" % (slot_int, label)); nRN += 1

    # --- 5. REF_SLOTS in disasm blocks ---
    nRF = 0
    for slot_int, tgt_int, gas_label, slot_label in DISASM_REF_SLOTS:
        d = getDataAt(_addr(slot_int))
        if d is None or d.getLength() != 4:
            print("[RF FAIL] no 4B data @ 0x%08x" % slot_int); continue
        if tgt_int not in made:
            createLabel(_addr(tgt_int), gas_label, True, SourceType.USER_DEFINED)
            made.add(tgt_int)
        ref = rm.addMemoryReference(_addr(slot_int), _addr(tgt_int), RefType.DATA, SourceType.USER_DEFINED, 0)
        rm.setPrimary(ref, True)
        createLabel(_addr(slot_int), slot_label, True, SourceType.USER_DEFINED)
        print("[RF ok] 0x%08x -> %s (ref->0x%08x %s)" % (slot_int, slot_label, tgt_int, gas_label)); nRF += 1

    # --- 6. PLATE comments for disasm functions ---
    nPL = 0
    for addr_int, plate_text in DISASM_PLATES:
        cu = listing.getCodeUnitAt(_addr(addr_int))
        if cu is None:
            print("[PL FAIL] no CodeUnit @ 0x%08x" % addr_int); continue
        cu.setComment(CodeUnit.PLATE_COMMENT, plate_text)
        print("[PL ok] 0x%08x plate set" % addr_int); nPL += 1

    print("[done] disasm_blocks=3 fns=%d EQ=%d RN=%d RF=%d PL=%d" % (
        len(FUNCTIONS), nEQ, nRN, nRF, nPL))
    print("=== DisassembleF05Seg3Blocks DONE ===")


main()
