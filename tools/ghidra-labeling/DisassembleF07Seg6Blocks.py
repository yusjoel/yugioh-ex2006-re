# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF07Seg6Blocks.py -- F07 Seg-6 R4 disasm (3 blocks)
#   Block1: 0x08060a86..0x08060b15 (0x90 B) -- check_exodia_set_in_extra_for_cid_165b
#   Block2: 0x0806106e..0x0806109b (0x2e B) -- check_zone_type580_direction_mismatch_for_cid_16c6
#   Block3: 0x0806121c..0x08061243 (0x28 B) -- check_lp_zone_hand_above6_for_cid_16d1
#
#   Pattern: DisassembleSeg9BlockB.py / DisassembleSeg5cJpHandlers.py
#   - clearListing entire block range first (avoid ContextChangeException)
#   - setTMode=THUMB for entire range
#   - DisassembleCommand for each entry point
#   - createFunction + setName for each named function
#   - createDWord for literal pool slots (split from flow)
#   - setPlateComment (ASCII only) on each function
#
#   Block1: ROM 0x60a86, 0x90 bytes
#     - 2B padding: 0x08060a86 = 0x0000
#     - fn@0x08060a88: check_exodia_set_in_extra_for_cid_165b
#     - Dispatch table: 0x09e417c0, CID=0x165b (Contract with Exodia), fn_elig=0x08060a89
#     - Literal pool @ 0x08060af8..0x08060b0c (6 slots):
#         0x08060af8 = 0x00000fb7 (RIGHT_LEG_FORBIDDEN_ONE_CID)
#         0x08060afc = 0x00000fb8 (LEFT_LEG_FORBIDDEN_ONE_CID)
#         0x08060b00 = 0x00000fb9 (RIGHT_ARM_FORBIDDEN_ONE_CID)
#         0x08060b04 = 0x00000fba (LEFT_ARM_FORBIDDEN_ONE_CID)
#         0x08060b08 = 0x00000fbb (EXODIA_THE_FORBIDDEN_ONE_CID)
#         0x08060b0c = 0x00001645 (EXODIA_NECROSS_CID)
#
#   Block2: ROM 0x6106e, 0x2e bytes
#     - 2B padding: 0x0806106e = 0x0000
#     - fn@0x08061070: check_zone_type580_direction_mismatch_for_cid_16c6
#     - Dispatch table: 0x09e44658, CID=0x16c6 (Fenrir), fn_elig=0x08061071
#     - Leaf fn (no push/pop; adds r2,r0,#0 entry; bx lr exit)
#     - No literal pool slots in this block
#
#   Block3: ROM 0x6121c, 0x28 bytes
#     - fn@0x0806121c: check_lp_zone_hand_above6_for_cid_16d1
#     - Dispatch table: 0x09e41bb0, CID=0x16d1 (Chaos End), fn_elig=0x0806121d
#     - Literal pool @ 0x0806123c..0x08061240 (2 slots):
#         0x0806123c = 0x0201c4e0 (gP1LifePoints)
#         0x08061240 = 0x00000868 (PLAYER_BLOCK_STRIDE)
#     - PC-relative refs verified: ldr r2,[pc,#0x1c]@0x0806121e -> 0x0806123c; ldr r1,[pc,#0x18]@0x08061226 -> 0x08061240
#
#   backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260614-164740-pre-f07seg6

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.app.cmd.function import CreateFunctionCmd
from ghidra.program.model.address import AddressSet
from ghidra.program.model.symbol import SourceType
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.data import DWordDataType
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


def _clear_and_set_thumb(lo_addr, hi_addr):
    lo = _addr(lo_addr)
    hi = _addr(hi_addr)
    try:
        clearListing(lo, hi)
        print("[ok ] clearListing(0x%08x..0x%08x)" % (lo_addr, hi_addr))
    except Exception as e:
        print("[warn] clearListing(0x%08x..0x%08x): %s" % (lo_addr, hi_addr, e))
    ctx = currentProgram.getProgramContext()
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        ctx.setValue(tmode, lo, hi, BigInteger.ONE)
        print("[ok ] setTMode=THUMB 0x%08x..0x%08x" % (lo_addr, hi_addr))
    else:
        print("[warn] TMode register not found")


def _disasm_flow(addr):
    """Disassemble at addr, let flow continue naturally."""
    lo = _addr(addr)
    cmd = DisassembleCommand(lo, None, True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm_flow 0x%08x: %s" % (addr, cmd.getStatusMsg()))
        return False
    return True


def _create_function(addr, name):
    """Create a named function at addr."""
    a = _addr(addr)
    fn_mgr = currentProgram.getFunctionManager()
    sym_tbl = currentProgram.getSymbolTable()

    existing = fn_mgr.getFunctionAt(a)
    if existing is not None:
        if existing.getName() != name:
            existing.setName(name, SourceType.USER_DEFINED)
            print("[FN ] renamed existing function at 0x%08x -> %s" % (addr, name))
        else:
            print("[FN ] function already exists at 0x%08x: %s" % (addr, name))
        return

    cmd = CreateFunctionCmd(name, a, None, SourceType.USER_DEFINED)
    if cmd.applyTo(currentProgram):
        print("[FN ] created %s @ 0x%08x" % (name, addr))
    else:
        print("[warn] createFunction %s @ 0x%08x: %s" % (name, addr, cmd.getStatusMsg()))
        sym_tbl.createLabel(a, name, SourceType.USER_DEFINED)
        print("[FN ] created label (fallback) %s @ 0x%08x" % (name, addr))


def _set_plate(addr, text):
    """Set PLATE_COMMENT on the code unit at addr. text must be pure ASCII."""
    bad = any(ord(ch) > 127 for ch in text)
    if bad:
        print("[PLATE FAIL] non-ASCII in plate @ 0x%08x -- skipping" % addr)
        return
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(_addr(addr))
    if cu is None:
        print("[PLATE FAIL] no CodeUnit at 0x%08x" % addr)
        return
    cu.setComment(CodeUnit.PLATE_COMMENT, text)
    print("[PLATE ok] 0x%08x (%d chars)" % (addr, len(text)))


def _create_dword(addr, label_name):
    """Force a DWORD at addr and create a label."""
    a = _addr(addr)
    listing = currentProgram.getListing()
    sym_tbl = currentProgram.getSymbolTable()
    try:
        clearListing(a, a.add(3))
    except Exception:
        pass
    listing.createData(a, DWordDataType.dataType)
    sym_tbl.createLabel(a, label_name, SourceType.USER_DEFINED)
    print("[DW ] 0x%08x -> %s" % (addr, label_name))


def _count_instructions(lo_addr, hi_addr):
    lo = _addr(lo_addr)
    hi = _addr(hi_addr)
    listing = currentProgram.getListing()
    n = 0
    inst = listing.getInstructionAt(lo)
    while inst is not None and inst.getAddress().compareTo(hi) <= 0:
        n += 1
        inst = listing.getInstructionAfter(inst.getAddress())
    return n


# ---------------------------------------------------------------------------
# Block1: 0x08060a86..0x08060b15 (0x90 B)
# 2B pad at 0x08060a86, fn@0x08060a88
# Literal pool @ 0x08060af8..0x08060b0c (6 dwords)
# ---------------------------------------------------------------------------
BLOCK1_LO   = 0x08060a86
BLOCK1_HI   = 0x08060b15
BLOCK1_FN   = 0x08060a88
BLOCK1_NAME = "check_exodia_set_in_extra_for_cid_165b"
BLOCK1_POOL_LO = 0x08060af8
BLOCK1_POOL_SLOTS = [
    (0x08060af8, 'right_leg_cid_lit_0af8'),
    (0x08060afc, 'left_leg_cid_lit_0afc'),
    (0x08060b00, 'right_arm_cid_lit_0b00'),
    (0x08060b04, 'left_arm_cid_lit_0b04'),
    (0x08060b08, 'exodia_cid_lit_0b08'),
    (0x08060b0c, 'exodia_necross_cid_lit_0b0c'),
]
BLOCK1_PLATE = (
    "reached via card effect handler dispatch table 0x09e417c0, "
    "Contract with Exodia CID=0x165b (card_1331); "
    "fn_elig ptr 0x08060a89 at table[+0x10]. "
    "Verifies all 5 Exodia pieces in extra deck: "
    "RIGHT_LEG(0x0fb7)/LEFT_LEG(0x0fb8)/RIGHT_ARM(0x0fb9)/LEFT_ARM(0x0fba)/EXODIA(0x0fbb) "
    "via count_extra_deck_cards_by_id x5; also checks neo_daedalus placement and paired monster slots. "
    "Literal pool @ 0x08060af8: 5 Exodia piece CIDs + EXODIA_NECROSS_CID(0x1645)."
)

# ---------------------------------------------------------------------------
# Block2: 0x0806106e..0x0806109b (0x2e B)
# 2B pad at 0x0806106e, fn@0x08061070 (leaf fn)
# No literal pool
# ---------------------------------------------------------------------------
BLOCK2_LO   = 0x0806106e
BLOCK2_HI   = 0x0806109b
BLOCK2_FN   = 0x08061070
BLOCK2_NAME = "check_zone_type580_direction_mismatch_for_cid_16c6"
BLOCK2_PLATE = (
    "reached via card effect handler dispatch table 0x09e44658, "
    "Fenrir CID=0x16c6 (card_1416); "
    "fn_elig ptr 0x08061071 at table[+0x10]. "
    "Leaf fn (no push; entry: adds r2,r0,#0; exits via bx lr). "
    "Checks: zone_type halfword[+2] == 0x580 (0xb0<<3) AND detail_word bit9 != player_id. "
    "Returns 1 if both conditions pass, 0 otherwise."
)

# ---------------------------------------------------------------------------
# Block3: 0x0806121c..0x08061243 (0x28 B)
# fn@0x0806121c (no padding at start)
# Literal pool @ 0x0806123c..0x08061240 (2 dwords)
# ---------------------------------------------------------------------------
BLOCK3_LO   = 0x0806121c
BLOCK3_HI   = 0x08061243
BLOCK3_FN   = 0x0806121c
BLOCK3_NAME = "check_lp_zone_hand_above6_for_cid_16d1"
BLOCK3_POOL_SLOTS = [
    (0x0806123c, 'gp1lp_lit_123c'),
    (0x08061240, 'player_stride_lit_1240'),
]
BLOCK3_PLATE = (
    "reached via card effect handler dispatch table 0x09e41bb0, "
    "Chaos End CID=0x16d1 (card_1427); "
    "fn_elig ptr 0x0806121d at table[+0x10]. "
    "Reads gP1LifePoints[player*PLAYER_BLOCK_STRIDE+0x1c] (alt-hand count field); "
    "returns 1 if > 6 (hand count exceeds 6), 0 otherwise. "
    "Literal pool @ 0x0806123c: gP1LifePoints(0x0201c4e0), PLAYER_BLOCK_STRIDE(0x868). "
    "PC-relative: ldr r2,[pc,#0x1c]@0x0806121e->0x0806123c; ldr r1,[pc,#0x18]@0x08061226->0x08061240."
)


def main():
    print("=== DisassembleF07Seg6Blocks (DRY=%s) ===" % DRY)
    print("  3 blocks: B1(0x%08x..0x%08x) B2(0x%08x..0x%08x) B3(0x%08x..0x%08x)" % (
        BLOCK1_LO, BLOCK1_HI, BLOCK2_LO, BLOCK2_HI, BLOCK3_LO, BLOCK3_HI))

    if DRY:
        print("[dry] Block1: clearListing+setTMode -> fn@0x%08x=%s" % (BLOCK1_FN, BLOCK1_NAME))
        print("  literal pool: %d dwords @ 0x%08x" % (len(BLOCK1_POOL_SLOTS), BLOCK1_POOL_LO))
        print("[dry] Block2: clearListing+setTMode -> fn@0x%08x=%s (leaf)" % (BLOCK2_FN, BLOCK2_NAME))
        print("[dry] Block3: clearListing+setTMode -> fn@0x%08x=%s" % (BLOCK3_FN, BLOCK3_NAME))
        print("  literal pool: %d dwords" % len(BLOCK3_POOL_SLOTS))
        return

    # --- Block 1 ---
    print("\n--- Block1: 0x%08x..0x%08x (fn@0x%08x) ---" % (BLOCK1_LO, BLOCK1_HI, BLOCK1_FN))
    _clear_and_set_thumb(BLOCK1_LO, BLOCK1_HI)

    # Disassemble from function entry (2B pad at 0x08060a86 is skipped)
    if _disasm_flow(BLOCK1_FN):
        print("[ok ] Block1 fn 0x%08x" % BLOCK1_FN)
    else:
        print("[warn] Block1 fn 0x%08x FAILED" % BLOCK1_FN)

    # Force literal pool as DWORDs (clearListing the pool area first)
    for addr, lname in BLOCK1_POOL_SLOTS:
        _create_dword(addr, lname)

    _create_function(BLOCK1_FN, BLOCK1_NAME)
    _set_plate(BLOCK1_FN, BLOCK1_PLATE)

    n1 = _count_instructions(BLOCK1_FN, BLOCK1_POOL_LO - 1)
    print("[Block1] %d instructions (fn body)" % n1)

    # --- Block 2 ---
    print("\n--- Block2: 0x%08x..0x%08x (fn@0x%08x, leaf) ---" % (BLOCK2_LO, BLOCK2_HI, BLOCK2_FN))
    _clear_and_set_thumb(BLOCK2_LO, BLOCK2_HI)

    # Disassemble from function entry (2B pad at 0x0806106e is skipped)
    if _disasm_flow(BLOCK2_FN):
        print("[ok ] Block2 fn 0x%08x" % BLOCK2_FN)
    else:
        print("[warn] Block2 fn 0x%08x FAILED" % BLOCK2_FN)

    _create_function(BLOCK2_FN, BLOCK2_NAME)
    _set_plate(BLOCK2_FN, BLOCK2_PLATE)

    n2 = _count_instructions(BLOCK2_FN, BLOCK2_HI)
    print("[Block2] %d instructions" % n2)

    # --- Block 3 ---
    print("\n--- Block3: 0x%08x..0x%08x (fn@0x%08x) ---" % (BLOCK3_LO, BLOCK3_HI, BLOCK3_FN))
    _clear_and_set_thumb(BLOCK3_LO, BLOCK3_HI)

    # Disassemble from function entry
    if _disasm_flow(BLOCK3_FN):
        print("[ok ] Block3 fn 0x%08x" % BLOCK3_FN)
    else:
        print("[warn] Block3 fn 0x%08x FAILED" % BLOCK3_FN)

    # Force literal pool as DWORDs
    for addr, lname in BLOCK3_POOL_SLOTS:
        _create_dword(addr, lname)

    _create_function(BLOCK3_FN, BLOCK3_NAME)
    _set_plate(BLOCK3_FN, BLOCK3_PLATE)

    n3 = _count_instructions(BLOCK3_FN, BLOCK3_POOL_SLOTS[0][0] - 1)
    print("[Block3] %d instructions (fn body)" % n3)

    # Summary
    print("\n=== DisassembleF07Seg6Blocks DONE ===")
    print("  Block1=%d instr  Block2=%d instr  Block3=%d instr" % (n1, n2, n3))
    print("  Functions created:")
    print("    %s @ 0x%08x" % (BLOCK1_NAME, BLOCK1_FN))
    print("    %s @ 0x%08x" % (BLOCK2_NAME, BLOCK2_FN))
    print("    %s @ 0x%08x" % (BLOCK3_NAME, BLOCK3_FN))


main()
