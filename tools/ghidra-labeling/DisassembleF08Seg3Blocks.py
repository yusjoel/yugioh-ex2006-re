# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF08Seg3Blocks.py -- F08 Seg-3 R4 disasm (1 block, 8 new stub functions)
#
# Block: 0x080668c0..0x08066a8b (0x1cc = 460B)
#   ROM_INCBIN DAT_080668c0 (8 raw refs from jump table at 0x08066890; 0 THUMB+1 refs)
#   Dispatch mechanism: ldr r0,[r0,#0]; .hword 0x4687 (MOV PC,r0) -- raw-addr branch
#   Table base: dispatch_equip_zone_by_effect_type_jump_table @ 0x08066890
#   Table: 12 entries (index = state - 0x75); 8 unique targets + 4 fall-through to 0x08066a8c
#
#   8 stub entry points (8 raw refs):
#     0x080668c0: dispatch_equip_effect_type_stub_80  (state=0x80, entry[11] @ 0x080668bc)
#     0x0806691c: dispatch_equip_effect_type_stub_7f  (state=0x7f, entry[10] @ 0x080668b8)
#     0x08066934: dispatch_equip_effect_type_stub_7e  (state=0x7e, entry[9]  @ 0x080668b4)
#     0x08066a58: dispatch_equip_effect_type_stub_7d  (state=0x7d, entry[8]  @ 0x080668b0)
#     0x08066a62: dispatch_equip_effect_type_stub_78  (state=0x78, entry[3]  @ 0x0806689c)
#     0x08066a6e: dispatch_equip_effect_type_stub_77  (state=0x77, entry[2]  @ 0x08066898)
#     0x08066a7a: dispatch_equip_effect_type_stub_76  (state=0x76, entry[1]  @ 0x08066894)
#     0x08066a86: dispatch_equip_effect_type_stub_75  (state=0x75, entry[0]  @ 0x08066890)
#
#   States 0x79..0x7c (entries[4..7] @ 0x080668a0..0x080668ac) -> 0x08066a8c (fall-through outside block)
#
# Machine-code self-check (first instruction per stub):
#   0x080668c0: 0x1c30 = adds r0,r6,#0
#   0x0806691c: 0x8834 = ldrh r4,[r6,#0]     (confirmed ldrh r4,[r6,0*2])
#   0x08066934: 0x2400 = movs r4,#0
#   0x08066a58: 0x1c28 = adds r0,r5,#0
#   0x08066a62: 0x1c28 = adds r0,r5,#0       (ROM at 0x08066a62: bytes 28 1c)
#   0x08066a6e: 0x2001 = movs r0,#1           (ROM at 0x08066a6e: bytes 01 20)
#   0x08066a7a: 0x1c28 = adds r0,r5,#0       (ROM bytes 28 1c; 0x08066a7c=2100=movs r1,#0 is 2nd insn)
#   0x08066a86: 0x1c28 = adds r0,r5,#0       (ROM at 0x08066a86: bytes 28 1c)
#
# backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260617_215450-pre-F08Seg3

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

# ===========================================================================
# BLOCK: 0x080668c0..0x08066a8b (8 stubs, 8 raw refs from jump table)
# ===========================================================================
BLOCK_LO = 0x080668c0
BLOCK_HI = 0x08066a8b  # inclusive end; 0x08066a8c is first inst after block (LAB_08066a8c)

# 8 stub entry points with proposed names and plate descriptions
# Order: by raw ref (stub_80 first, descending state; then stubs_78..75 ascending)
BLOCK_FNS = [
    (0x080668c0, 'dispatch_equip_effect_type_stub_80',
     'state=0x80: dispatch_equip_zone_sprite_by_effect_type case handler. '
     'Entry[11] at table[0x080668bc]. First insn: adds r0,r6,#0 (0x1c30). '
     'Dispatched via raw-addr MOV PC,r0 from dispatch_equip_zone_by_effect_type_jump_table.'),
    (0x0806691c, 'dispatch_equip_effect_type_stub_7f',
     'state=0x7f: dispatch_equip_zone_sprite_by_effect_type case handler. '
     'Entry[10] at table[0x080668b8]. First insn: ldrh r4,[r6,#0] (0x8834). '
     'Dispatched via raw-addr MOV PC,r0 from dispatch_equip_zone_by_effect_type_jump_table.'),
    (0x08066934, 'dispatch_equip_effect_type_stub_7e',
     'state=0x7e: dispatch_equip_zone_sprite_by_effect_type case handler. '
     'Entry[9] at table[0x080668b4]. First insn: movs r4,#0 (0x2400). '
     'Dispatched via raw-addr MOV PC,r0 from dispatch_equip_zone_by_effect_type_jump_table.'),
    (0x08066a58, 'dispatch_equip_effect_type_stub_7d',
     'state=0x7d: dispatch_equip_zone_sprite_by_effect_type case handler. '
     'Entry[8] at table[0x080668b0]. First insn: adds r0,r5,#0 (0x1c28). '
     'Dispatched via raw-addr MOV PC,r0 from dispatch_equip_zone_by_effect_type_jump_table.'),
    (0x08066a62, 'dispatch_equip_effect_type_stub_78',
     'state=0x78: dispatch_equip_zone_sprite_by_effect_type case handler. '
     'Entry[3] at table[0x0806689c]. First insn: adds r0,r5,#0 (0x1c28 at 0x08066a62). '
     'Dispatched via raw-addr MOV PC,r0 from dispatch_equip_zone_by_effect_type_jump_table.'),
    (0x08066a6e, 'dispatch_equip_effect_type_stub_77',
     'state=0x77: dispatch_equip_zone_sprite_by_effect_type case handler. '
     'Entry[2] at table[0x08066898]. First insn: movs r0,#1 (0x2001 at 0x08066a6e). '
     'Dispatched via raw-addr MOV PC,r0 from dispatch_equip_zone_by_effect_type_jump_table.'),
    (0x08066a7a, 'dispatch_equip_effect_type_stub_76',
     'state=0x76: dispatch_equip_zone_sprite_by_effect_type case handler. '
     'Entry[1] at table[0x08066894]. First insn: adds r0,r5,#0 (0x1c28 at 0x08066a7a). '
     'Dispatched via raw-addr MOV PC,r0 from dispatch_equip_zone_by_effect_type_jump_table.'),
    (0x08066a86, 'dispatch_equip_effect_type_stub_75',
     'state=0x75: dispatch_equip_zone_sprite_by_effect_type case handler. '
     'Entry[0] at table[0x08066890]. First insn: adds r0,r5,#0 (0x1c28 at 0x08066a86). '
     'Dispatched via raw-addr MOV PC,r0 from dispatch_equip_zone_by_effect_type_jump_table.'),
]


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


def _disasm_stub(addr):
    """Disassemble one stub at addr using flow continuation."""
    lo = _addr(addr)
    cmd = DisassembleCommand(lo, None, True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm_flow 0x%08x: %s" % (addr, cmd.getStatusMsg()))
        return False
    print("[disasm] 0x%08x ok" % addr)
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
    """Set PLATE_COMMENT. text must be pure ASCII."""
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


def main():
    print("=== DisassembleF08Seg3Blocks (DRY=%s) ===" % DRY)
    print("  Block: 0x%08x..0x%08x (8 stub entries)" % (BLOCK_LO, BLOCK_HI))
    print("  Total: %d new functions" % len(BLOCK_FNS))

    if DRY:
        print("[dry] Block range: 0x%08x..0x%08x" % (BLOCK_LO, BLOCK_HI))
        for addr, name, _ in BLOCK_FNS:
            print("[dry] stub fn: %s @ 0x%08x" % (name, addr))
        return

    # Step 1: clearListing entire block range + setTMode THUMB
    print("\n--- Step1: clearListing + setTMode ---")
    _clear_and_set_thumb(BLOCK_LO, BLOCK_HI)

    # Step 2: Disassemble each stub entry individually
    # (raw-addr dispatch, stubs not flow-reachable from each other via normal fall-through)
    print("\n--- Step2: Disassemble 8 stubs ---")
    for addr, name, _ in BLOCK_FNS:
        _disasm_stub(addr)

    # Step 3: Create functions and set plates
    print("\n--- Step3: Create functions + set plates ---")
    for addr, name, plate_text in BLOCK_FNS:
        _create_function(addr, name)
        _set_plate(addr, plate_text)

    print("\n=== DisassembleF08Seg3Blocks DONE ===")
    print("  %d new functions created" % len(BLOCK_FNS))
    print("  States 0x75..0x80 (except fall-through 0x79..0x7c) -> 8 stub fns")


main()
