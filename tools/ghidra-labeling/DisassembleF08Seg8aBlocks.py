# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF08Seg8aBlocks.py -- F08 Seg-8a R4 disasm (3 blocks)
#
# Block1: 0x0806ae18..0x0806b073 (0x25c B)
#   Jump table @0x0806adf4..0x0806ae14 (9 entries, raw-addr dispatch)
#   9 entries point into this block; unique entry points:
#     0x0806ae18 (table[8]=block start), 0x0806ae48, 0x0806ae90, 0x0806af52,
#     0x0806af84, 0x0806afac, 0x0806afec, 0x0806b01c (appears twice: table[0] and [1])
#   Parent: dispatch_equip_effect_slot_display_by_state_and_card (0x0806abec)
#   Pattern: raw-addr bx dispatch (not THUMB+1)
#
# Block2: 0x0806b098..0x0806b233 (0x19c B)
#   Jump table @0x0806b074..0x0806b094 (9 entries, raw-addr dispatch)
#   9 entries point into this block; unique entry points:
#     0x0806b098 (table[8]=block start), 0x0806b0d6, 0x0806b124, 0x0806b13c,
#     0x0806b1de, 0x0806b1ea, 0x0806b1f4 (appears 3x: table[1],[2],[5])
#   Parent: dispatch_equip_effect_slot_display_by_state_and_card (0x0806abec)
#   Pattern: raw-addr bx dispatch (not THUMB+1)
#
# Block3: 0x0806b2a8..0x0806b31b (0x74 B)
#   Jump table @0x0806b234..0x0806b2a4 (29 entries, raw-addr dispatch)
#   Block IS the target code stubs (not the jump table body which is at 0x6b234..0x6b2a8)
#   Unique entry points:
#     0x0806b2a8 (table[28]=block start), 0x0806b2ce, 0x0806b2e2, 0x0806b2f8,
#     0x0806b30a, 0x0806b314 (default/fallthrough)
#   Parent: dispatch_germ_momonga_trigger_display_by_state (0x0806b31c)
#   Pattern: raw-addr bx dispatch (not THUMB+1)
#
# NOTE: Each block uses clearListing + setTMode(THUMB) on full range first,
#   then individual DisassembleCommand per entry point (single-range only disasms first stub).
#
# NOTE: All plate text is pure ASCII (no CJK). Jython CJK = double-UTF-8 mojibake.
#
# backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260618_040745-pre-F08Seg8a

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.app.cmd.function import CreateFunctionCmd
from ghidra.program.model.address import AddressSet
from ghidra.program.model.symbol import SourceType
from ghidra.program.model.listing import CodeUnit
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
    lo = _addr(addr)
    cmd = DisassembleCommand(lo, None, True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm_flow 0x%08x: %s" % (addr, cmd.getStatusMsg()))
        return False
    return True


def _create_function(addr, name):
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
        print("[FN ] label fallback %s @ 0x%08x" % (name, addr))


def _set_plate(addr, text):
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


# ===========================================================================
# BLOCK 1: 0x0806ae18..0x0806b073 (0x25c B)
#   9-entry raw-addr jump table at 0x0806adf4..0x0806ae14
#   8 unique entry points
# ===========================================================================
BLOCK1_LO = 0x0806ae18
BLOCK1_HI = 0x0806b073

BLOCK1_FNS = [
    # Ordered by address; plate describes parent dispatch context
    (0x0806ae18, 'equip_effect_state_stub_default_ae18',
     'Default/case0 stub: dispatch_equip_effect_slot_display_by_state_and_card (0x0806abec) '
     'raw-addr jump table entry[8] at 0x0806ae14. '
     'Block range 0x0806ae18..0x0806b073.'),
    (0x0806ae48, 'equip_effect_state_stub_ae48',
     'Case stub: dispatch_equip_effect_slot_display_by_state_and_card (0x0806abec) '
     'raw-addr jump table entry[7] at 0x0806ae10. '
     'Block range 0x0806ae18..0x0806b073.'),
    (0x0806ae90, 'equip_effect_state_stub_ae90',
     'Case stub: dispatch_equip_effect_slot_display_by_state_and_card (0x0806abec) '
     'raw-addr jump table entry[6] at 0x0806ae0c. '
     'Block range 0x0806ae18..0x0806b073.'),
    (0x0806af52, 'equip_effect_state_stub_af52',
     'Case stub: dispatch_equip_effect_slot_display_by_state_and_card (0x0806abec) '
     'raw-addr jump table entry[5] at 0x0806ae08. '
     'Block range 0x0806ae18..0x0806b073.'),
    (0x0806af84, 'equip_effect_state_stub_af84',
     'Case stub: dispatch_equip_effect_slot_display_by_state_and_card (0x0806abec) '
     'raw-addr jump table entry[4] at 0x0806ae04. '
     'Block range 0x0806ae18..0x0806b073.'),
    (0x0806afac, 'equip_effect_state_stub_afac',
     'Case stub: dispatch_equip_effect_slot_display_by_state_and_card (0x0806abec) '
     'raw-addr jump table entry[2] at 0x0806adfc. '
     'Block range 0x0806ae18..0x0806b073.'),
    (0x0806afec, 'equip_effect_state_stub_afec',
     'Case stub: dispatch_equip_effect_slot_display_by_state_and_card (0x0806abec) '
     'raw-addr jump table entry[1] at 0x0806adf8. '
     'Block range 0x0806ae18..0x0806b073.'),
    (0x0806b01c, 'equip_effect_state_stub_b01c',
     'Case stub (shared, table[0]+[3]): dispatch_equip_effect_slot_display_by_state_and_card '
     '(0x0806abec) raw-addr jump table entries at 0x0806adf4 and 0x0806ae00. '
     'Block range 0x0806ae18..0x0806b073.'),
]

# ===========================================================================
# BLOCK 2: 0x0806b098..0x0806b233 (0x19c B)
#   9-entry raw-addr jump table at 0x0806b074..0x0806b094
#   7 unique entry points
# ===========================================================================
BLOCK2_LO = 0x0806b098
BLOCK2_HI = 0x0806b233

BLOCK2_FNS = [
    (0x0806b098, 'equip_effect_state_stub_default_b098',
     'Default/case0 stub: dispatch_equip_effect_slot_display_by_state_and_card (0x0806abec) '
     'raw-addr jump table entry[8] at 0x0806b094. '
     'Block range 0x0806b098..0x0806b233.'),
    (0x0806b0d6, 'equip_effect_state_stub_b0d6',
     'Case stub: dispatch_equip_effect_slot_display_by_state_and_card (0x0806abec) '
     'raw-addr jump table entry[7] at 0x0806b090. '
     'Block range 0x0806b098..0x0806b233.'),
    (0x0806b124, 'equip_effect_state_stub_b124',
     'Case stub: dispatch_equip_effect_slot_display_by_state_and_card (0x0806abec) '
     'raw-addr jump table entry[6] at 0x0806b08c. '
     'Block range 0x0806b098..0x0806b233.'),
    (0x0806b13c, 'equip_effect_state_stub_b13c',
     'Case stub: dispatch_equip_effect_slot_display_by_state_and_card (0x0806abec) '
     'raw-addr jump table entry[4] at 0x0806b084. '
     'Block range 0x0806b098..0x0806b233.'),
    (0x0806b1de, 'equip_effect_state_stub_b1de',
     'Case stub: dispatch_equip_effect_slot_display_by_state_and_card (0x0806abec) '
     'raw-addr jump table entry[3] at 0x0806b080. '
     'Block range 0x0806b098..0x0806b233.'),
    (0x0806b1ea, 'equip_effect_state_stub_b1ea',
     'Case stub: dispatch_equip_effect_slot_display_by_state_and_card (0x0806abec) '
     'raw-addr jump table entry[0] at 0x0806b074. '
     'Block range 0x0806b098..0x0806b233.'),
    (0x0806b1f4, 'equip_effect_state_stub_b1f4',
     'Case stub (shared, table[1]+[2]+[5]): dispatch_equip_effect_slot_display_by_state_and_card '
     '(0x0806abec) raw-addr jump table entries at 0x0806b078, 0x0806b07c, 0x0806b088. '
     'Block range 0x0806b098..0x0806b233.'),
]

# ===========================================================================
# BLOCK 3: 0x0806b2a8..0x0806b31b (0x74 B)
#   29-entry raw-addr jump table at 0x0806b234..0x0806b2a4 (already in asm as .word)
#   Block IS target code stubs (not the jump table body)
#   6 unique entry points
# ===========================================================================
BLOCK3_LO = 0x0806b2a8
BLOCK3_HI = 0x0806b31b

BLOCK3_FNS = [
    (0x0806b2a8, 'equip_germ_momonga_state_stub_b2a8',
     'Case stub: dispatch_germ_momonga_trigger_display_by_state (0x0806b31c) '
     'raw-addr jump table entry[28] at 0x0806b2a4. '
     'Block range 0x0806b2a8..0x0806b31b.'),
    (0x0806b2ce, 'equip_germ_momonga_state_stub_b2ce',
     'Case stub: dispatch_germ_momonga_trigger_display_by_state (0x0806b31c) '
     'raw-addr jump table entry[26] at 0x0806b29c. '
     'Block range 0x0806b2a8..0x0806b31b.'),
    (0x0806b2e2, 'equip_germ_momonga_state_stub_b2e2',
     'Case stub: dispatch_germ_momonga_trigger_display_by_state (0x0806b31c) '
     'raw-addr jump table entry[25] at 0x0806b298. '
     'Block range 0x0806b2a8..0x0806b31b.'),
    (0x0806b2f8, 'equip_germ_momonga_state_stub_b2f8',
     'Case stub: dispatch_germ_momonga_trigger_display_by_state (0x0806b31c) '
     'raw-addr jump table entry[20] at 0x0806b284. '
     'Block range 0x0806b2a8..0x0806b31b.'),
    (0x0806b30a, 'equip_germ_momonga_state_stub_b30a',
     'Case stub: dispatch_germ_momonga_trigger_display_by_state (0x0806b31c) '
     'raw-addr jump table entry[0] at 0x0806b234. '
     'Block range 0x0806b2a8..0x0806b31b.'),
    (0x0806b314, 'equip_germ_momonga_state_stub_default_b314',
     'Default stub (most table entries): dispatch_germ_momonga_trigger_display_by_state (0x0806b31c) '
     'raw-addr jump table entries[1..19,21..24,27] at 0x0806b238..0x0806b2a0 (most point here). '
     'Block range 0x0806b2a8..0x0806b31b.'),
]


def main():
    print("=== DisassembleF08Seg8aBlocks (DRY=%s) ===" % DRY)
    print("  Block1: 0x%08x..0x%08x (%d stubs)" % (BLOCK1_LO, BLOCK1_HI, len(BLOCK1_FNS)))
    print("  Block2: 0x%08x..0x%08x (%d stubs)" % (BLOCK2_LO, BLOCK2_HI, len(BLOCK2_FNS)))
    print("  Block3: 0x%08x..0x%08x (%d stubs)" % (BLOCK3_LO, BLOCK3_HI, len(BLOCK3_FNS)))
    total_fns = len(BLOCK1_FNS) + len(BLOCK2_FNS) + len(BLOCK3_FNS)
    print("  Total stubs: %d" % total_fns)

    if DRY:
        for addr, name, _ in BLOCK1_FNS:
            print("[dry] Block1 fn: %s @ 0x%08x" % (name, addr))
        for addr, name, _ in BLOCK2_FNS:
            print("[dry] Block2 fn: %s @ 0x%08x" % (name, addr))
        for addr, name, _ in BLOCK3_FNS:
            print("[dry] Block3 fn: %s @ 0x%08x" % (name, addr))
        print("[dry] total stubs=%d" % total_fns)
        return

    # =========================================================================
    # Block1: 0x0806ae18..0x0806b073
    # =========================================================================
    print("\n--- Block1: 0x%08x..0x%08x (%d stubs) ---" % (
        BLOCK1_LO, BLOCK1_HI, len(BLOCK1_FNS)))
    _clear_and_set_thumb(BLOCK1_LO, BLOCK1_HI)
    # Disassemble each entry individually (raw-addr dispatch not flow-linked)
    for addr, name, _ in BLOCK1_FNS:
        _disasm_flow(addr)
    for addr, name, plate_text in BLOCK1_FNS:
        _create_function(addr, name)
        _set_plate(addr, plate_text)
    print("  Block1: %d stubs created" % len(BLOCK1_FNS))

    # =========================================================================
    # Block2: 0x0806b098..0x0806b233
    # =========================================================================
    print("\n--- Block2: 0x%08x..0x%08x (%d stubs) ---" % (
        BLOCK2_LO, BLOCK2_HI, len(BLOCK2_FNS)))
    _clear_and_set_thumb(BLOCK2_LO, BLOCK2_HI)
    for addr, name, _ in BLOCK2_FNS:
        _disasm_flow(addr)
    for addr, name, plate_text in BLOCK2_FNS:
        _create_function(addr, name)
        _set_plate(addr, plate_text)
    print("  Block2: %d stubs created" % len(BLOCK2_FNS))

    # =========================================================================
    # Block3: 0x0806b2a8..0x0806b31b
    # =========================================================================
    print("\n--- Block3: 0x%08x..0x%08x (%d stubs) ---" % (
        BLOCK3_LO, BLOCK3_HI, len(BLOCK3_FNS)))
    _clear_and_set_thumb(BLOCK3_LO, BLOCK3_HI)
    for addr, name, _ in BLOCK3_FNS:
        _disasm_flow(addr)
    for addr, name, plate_text in BLOCK3_FNS:
        _create_function(addr, name)
        _set_plate(addr, plate_text)
    print("  Block3: %d stubs created" % len(BLOCK3_FNS))

    print("\n=== DisassembleF08Seg8aBlocks DONE ===")
    print("  Total new functions: %d" % total_fns)
    print("  Block1: %d stubs (dispatch_equip_effect_slot_display_by_state_and_card)" % len(BLOCK1_FNS))
    print("  Block2: %d stubs (dispatch_equip_effect_slot_display_by_state_and_card)" % len(BLOCK2_FNS))
    print("  Block3: %d stubs (dispatch_germ_momonga_trigger_display_by_state)" % len(BLOCK3_FNS))


main()
