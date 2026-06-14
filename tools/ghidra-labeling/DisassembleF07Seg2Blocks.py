# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF07Seg2Blocks.py -- F07 Seg-2 R4 disasm (2 ROM_INCBIN blocks -> THUMB code)
#
# Blocks (card effect handler dispatch table targets, 0x09e4xxxx range):
#
#   Block 1: 0x0805dd3e..0x0805dd57 (0x1a B)
#     .zero 2 padding at 0x0805dd3e (createWord to label the pad)
#     fn: 0x0805dd40 (THUMB+1=0x0805dd41) -- 1 dispatch table hit
#       ROM offset 0x09e40318: CID=0x134e (cid_134e), fn[1]=0x0805dd41
#
#   Block 2: 0x0805ddda..0x0805deab (0xd2 B)
#     .zero 2 padding at 0x0805ddda
#     fn1: 0x0805dddc (THUMB+1=0x0805dddd) -- 2 hits: CID=0x1352 (Numinous Healer),
#          CID=0x135a (Attack and Receive) -- shared handler
#     fn2: 0x0805de10 (THUMB+1=0x0805de11) -- 2 hits: CID=0x1353 (Appropriate, x2 entries)
#     fn3: 0x0805de50 (THUMB+1=0x0805de51) -- 1 hit: CID=0x1354 (Forced Requisition)
#     fn4: 0x0805de7c (THUMB+1=0x0805de7d) -- 1 hit: CID=0x1355 (Minor Goblin Official)
#
# Sub-fn boundaries verified by reviewer (bx lr positions):
#   fn1 end: 0x0805de0c (+0x32 from 0x5ddda)
#   fn2 end: 0x0805de4e (+0x74 from 0x5ddda)
#   fn3 end: 0x0805de78 (+0x9e from 0x5ddda)
#   fn4 end: 0x0805de9c (+0xc2 from 0x5ddda)
#
# Paradigm: DisassembleF07Seg1Blocks.py (file 00 Seg-5c)
#   1. clearListing entire block range
#   2. setTMode=THUMB for entire range
#   3. createWord for .zero 2 pad (Block 1 only)
#   4. DisassembleCommand per fn entry (flow-based; NOT entire range at once)
#   5. createFunction + setName (USER_DEFINED)
#   6. setPlateComment (pure ASCII only)
#
# Backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260614-pre-f07seg2

from ghidra.app.cmd.disassemble import DisassembleCommand
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


def _create_word(addr_int):
    """Force createWord at addr to label the 2-byte .zero alignment pad."""
    a = _addr(addr_int)
    try:
        clearListing(a, _addr(addr_int + 1))
        createWord(a)
        print("[ok ] createWord @ 0x%08x (2B .zero pad)" % addr_int)
    except Exception as e:
        print("[warn] createWord @ 0x%08x: %s" % (addr_int, e))


def _disasm_flow(addr):
    """Disassemble at addr (single entry), let flow continue naturally."""
    lo = _addr(addr)
    cmd = DisassembleCommand(lo, None, True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm_flow 0x%08x: %s" % (addr, cmd.getStatusMsg()))
        return False
    return True


def _create_function(entry_addr, func_name, plate_text):
    fm = currentProgram.getFunctionManager()
    listing = currentProgram.getListing()
    fn = fm.getFunctionAt(_addr(entry_addr))
    if fn is None:
        fn = createFunction(_addr(entry_addr), func_name)
        if fn is None:
            fn = fm.getFunctionContaining(_addr(entry_addr))
    if fn is not None:
        fn.setName(func_name, SourceType.USER_DEFINED)
        print("[ok ] function: %s @ 0x%08x" % (func_name, entry_addr))
    else:
        print("[warn] could not obtain Function at 0x%08x" % entry_addr)
    cu = listing.getCodeUnitAt(_addr(entry_addr))
    if cu is not None:
        cu.setComment(CodeUnit.PLATE_COMMENT, plate_text)
        print("[ok ] plate set (%d chars) @ 0x%08x" % (len(plate_text), entry_addr))
    else:
        print("[warn] no CodeUnit at 0x%08x for plate" % entry_addr)


# ---------------------------------------------------------------------------
# Block definitions
# ---------------------------------------------------------------------------

BLOCKS = [
    # Block 1: 0x0805dd3e..0x0805dd57 (0x1a B) -- 1 sub-function
    # .zero 2 at 0x0805dd3e, fn @ 0x0805dd40
    {
        'name': '1',
        'lo': 0x0805dd3e,
        'hi': 0x0805dd57,
        'pad_word': 0x0805dd3e,  # createWord for the 2B .zero pad
        'fns': [
            {
                'entry': 0x0805dd40,
                'name': 'check_equip_zone_eligible_cid_134e',
                'plate': (
                    'Reached via card effect handler dispatch table 0x09e40318. '
                    'CID=0x134e (cid_134e, unassigned slot between Driving Snow 0x134d '
                    'and Numinous Healer 0x1352). Record at 0x09e4030c: '
                    '[CID=0x134e][fn[0]][fn[1]=0x0805dd41][fn[2]][fn[3]]. '
                    '1 dispatch table hit. fn_slot=1 in 24B dispatch record. '
                    '.zero 2 alignment pad precedes entry at 0x0805dd3e.'
                ),
            },
        ],
    },
    # Block 2: 0x0805ddda..0x0805deab (0xd2 B) -- 4 sub-functions
    # .zero 2 at 0x0805ddda, fn1 @ 0x0805dddc, fn2 @ 0x0805de10,
    # fn3 @ 0x0805de50, fn4 @ 0x0805de7c
    {
        'name': '2',
        'lo': 0x0805ddda,
        'hi': 0x0805deab,
        'pad_word': None,  # No createWord for block 2 pad (covered by clearListing+setTMode)
        'fns': [
            {
                'entry': 0x0805dddc,
                'name': 'check_equip_zone_eligible_numinous_healer_and_recv',
                'plate': (
                    'Reached via card effect handler dispatch table. Shared handler for '
                    'CID=0x1352 (Numinous Healer, pw=02130625) at 0x09e40378 and '
                    'CID=0x135a (Attack and Receive, pw=93553943) at 0x09e40438. '
                    '2 dispatch table hits. fn_slot=1 in 24B dispatch record. '
                    'bx lr at 0x0805de0c. .zero 2 pad precedes block at 0x0805ddda.'
                ),
            },
            {
                'entry': 0x0805de10,
                'name': 'check_equip_zone_eligible_appropriate',
                'plate': (
                    'Reached via card effect handler dispatch table. '
                    'CID=0x1353 (Appropriate) at 0x09e40390 and second entry at 0x09e43708. '
                    '2 dispatch table hits (same CID, two dispatch table records). '
                    'fn_slot=1 in 24B dispatch record. bx lr at 0x0805de4e. '
                    'Literal pool: gP1LifePoints @ 0x0805de44, FIELD_STATE_OFF @ 0x0805de48.'
                ),
            },
            {
                'entry': 0x0805de50,
                'name': 'check_equip_zone_eligible_forced_requisition',
                'plate': (
                    'Reached via card effect handler dispatch table 0x09e403a8. '
                    'CID=0x1354 (Forced Requisition, pw=74923978). '
                    '1 dispatch table hit. fn_slot=1 in 24B dispatch record. '
                    'bx lr at 0x0805de78.'
                ),
            },
            {
                'entry': 0x0805de7c,
                'name': 'check_equip_zone_eligible_minor_goblin_official',
                'plate': (
                    'Reached via card effect handler dispatch table 0x09e403c0. '
                    'CID=0x1355 (Minor Goblin Official, pw=01918087). '
                    '1 dispatch table hit. fn_slot=1 in 24B dispatch record. '
                    'bx lr at 0x0805de9c. '
                    'Literal pool: gP1LifePoints, PLAYER_BLOCK_STRIDE, 0x0bb8(=3000) '
                    'follow fn body.'
                ),
            },
        ],
    },
]


def main():
    print("=== DisassembleF07Seg2Blocks (DRY=%s) ===" % DRY)
    n_blocks = 0
    n_fns = 0

    for blk in BLOCKS:
        lo = blk['lo']
        hi = blk['hi']
        print("\n--- Block %s: 0x%08x..0x%08x (0x%x B) ---" % (blk['name'], lo, hi, hi - lo + 1))

        if DRY:
            print("[dry] clearListing+setTMode(0x%08x..0x%08x)" % (lo, hi))
            if blk.get('pad_word') is not None:
                print("[dry] createWord @ 0x%08x" % blk['pad_word'])
            for fn in blk['fns']:
                print("[dry] disasm_flow(0x%08x)" % fn['entry'])
                print("[dry] createFunction('%s')" % fn['name'])
                print("[dry] setPlate(%d chars)" % len(fn['plate']))
                n_fns += 1
            n_blocks += 1
            continue

        # Step 1: clearListing entire block, then setTMode=THUMB
        _clear_and_set_thumb(lo, hi)

        # Step 2: createWord for .zero pad if needed (Block 1 only)
        if blk.get('pad_word') is not None:
            _create_word(blk['pad_word'])

        # Step 3: disasm each function in the block (flow-based, per-entry)
        for fn in blk['fns']:
            entry = fn['entry']
            print("[...] disasm_flow(0x%08x)" % entry)
            if not _disasm_flow(entry):
                print("[FAIL] disasm at 0x%08x -- skipping function" % entry)
                continue
            _create_function(entry, fn['name'], fn['plate'])
            n_fns += 1

        n_blocks += 1

    print("\n=== DisassembleF07Seg2Blocks DONE ===")
    print("  Blocks processed: %d / %d" % (n_blocks, len(BLOCKS)))
    print("  Functions created: %d (expected 5: 1 in Block1 + 4 in Block2)" % n_fns)
    print("  DRY=%s" % DRY)


main()
