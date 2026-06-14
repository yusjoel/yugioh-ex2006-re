# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF07Seg1Blocks.py -- F07 Seg-1 R4 disasm (4 ROM_INCBIN blocks -> THUMB code)
#
# Blocks (card effect handler dispatch table targets, 0x09e4xxxx range):
#
#   Block A: 0x0805c40a..0x0805c467 (0x5e B)
#     .zero 2 padding at 0x5c40a
#     fn1: 0x0805c40c (THUMB+1=0x0805c40d) -- 4 dispatch table hits (CIDs: Dream Clown 0x101e, etc.)
#     fn2: 0x0805c43c (THUMB+1=0x0805c43d) -- 21 dispatch table hits (CIDs: Fusion Sage 0x1308, etc.)
#
#   Block B: 0x0805c608..0x0805c62f (0x28 B)
#     fn: 0x0805c608 (THUMB+1=0x0805c609) -- 1 dispatch table hit (CID: 0x11a0 unassigned)
#
#   Block C: 0x0805cd86..0x0805cdaf (0x2a B)
#     .zero 2 padding at 0x5cd86
#     fn: 0x0805cd88 (THUMB+1=0x0805cd89) -- 15 dispatch table hits (CIDs: Lightforce Sword 0x12c8, etc.)
#
#   Block D: 0x0805cf1c..0x0805cf3b (0x20 B)
#     fn: 0x0805cf1c (THUMB+1=0x0805cf1d) -- 3 dispatch table hits (CIDs: House of Adhesive Tape 0x124f, etc.)
#
# Paradigm: DisassembleF06Seg2Block.py / F05-Seg-6 (file 00 Seg-5c)
#   1. clearListing entire block range
#   2. setTMode=THUMB for entire range
#   3. DisassembleCommand per fn entry (flow-based; NOT entire range at once)
#   4. createFunction + setName (USER_DEFINED)
#   5. setPlateComment (ASCII only)
#
# Backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260614-pre-f07seg1

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
    # Block A: 0x5c40a..0x5c467 (0x5e B) -- 2 sub-functions
    # .zero 2 at 0x5c40a, fn1 @ 0x5c40c, fn2 @ 0x5c43c
    {
        'name': 'A',
        'lo': 0x0805c40a,
        'hi': 0x0805c467,
        'fns': [
            {
                'entry': 0x0805c40c,
                'name': 'check_equip_slots_for_dreamer_blade_rabbit_dispatch',
                'plate': (
                    'Reached via card effect handler dispatch table 0x9e43xxx. '
                    'fn1 at 0x5c40c: 4 table hits, CIDs include 0x101e(Dream Clown), '
                    '0x1048(unassigned), 0x1197(unassigned), 0x1868(Blade Rabbit). '
                    'fn_slot=2 in 24B dispatch record. Leaf function.'
                ),
            },
            {
                'entry': 0x0805c43c,
                'name': 'check_equip_slots_for_sage_burial_army_dispatch',
                'plate': (
                    'Reached via card effect handler dispatch table 0x9e4xxxx. '
                    'fn2 at 0x5c43c: 21 table hits, CIDs include 0x1308(Fusion Sage), '
                    '0x1474(Foolish Burial), 0x14d0(Reinforcement of the Army), '
                    '0x1562(Toon Table of Contents), 0x159c(Different Dimension Capsule), '
                    '0x15a1(Terraforming) and 15 others. fn_slot=2 in 24B dispatch record.'
                ),
            },
        ],
    },
    # Block B: 0x5c608..0x5c62f (0x28 B) -- 1 sub-function
    {
        'name': 'B',
        'lo': 0x0805c608,
        'hi': 0x0805c62f,
        'fns': [
            {
                'entry': 0x0805c608,
                'name': 'check_equip_slots_for_cid_11a0_dispatch',
                'plate': (
                    'Reached via card effect handler dispatch table. '
                    'Hit at 0x9e46408: CID=0x11a0 (unassigned slot, not in card-stats.s), '
                    'fn_slot=2 in 24B record at table 0x9e463fc. '
                    'fn[0]=0x080672a5 fn[1]=0 fn[2]=0x0805c609 fn[3]=0x0805635d.'
                ),
            },
        ],
    },
    # Block C: 0x5cd86..0x5cdaf (0x2a B) -- 1 sub-function
    # .zero 2 at 0x5cd86, fn @ 0x5cd88
    {
        'name': 'C',
        'lo': 0x0805cd86,
        'hi': 0x0805cdaf,
        'fns': [
            {
                'entry': 0x0805cd88,
                'name': 'check_equip_slots_for_confiscation_duo_sentry_dispatch',
                'plate': (
                    'Reached via card effect handler dispatch table x15 tables. '
                    'CIDs include 0x12c8(Lightforce Sword), 0x12f0(unassigned), '
                    '0x1307(Restructer Revolution), 0x1324(Confiscation), '
                    '0x1325(Delinquent Duo), 0x132b(The Forceful Sentry) and 9 others. '
                    'fn_slot=2 in 24B dispatch record. .zero 2 padding precedes entry at 0x5cd86.'
                ),
            },
        ],
    },
    # Block D: 0x5cf1c..0x5cf3b (0x20 B) -- 1 sub-function
    {
        'name': 'D',
        'lo': 0x0805cf1c,
        'hi': 0x0805cf3b,
        'fns': [
            {
                'entry': 0x0805cf1c,
                'name': 'check_equip_slots_for_adhesive_tape_trap_hole_dispatch',
                'plate': (
                    'Reached via card effect handler dispatch table x3. '
                    'CIDs: 0x124f(House of Adhesive Tape), 0x1250(unassigned), '
                    '0x12e4(Trap Hole). fn_slot=2 in 24B dispatch record. '
                    'Table hits at 0x9e3f880, 0x9e3f898, 0x9e3fc10.'
                ),
            },
        ],
    },
]


def main():
    print("=== DisassembleF07Seg1Blocks (DRY=%s) ===" % DRY)
    n_blocks = 0
    n_fns = 0

    for blk in BLOCKS:
        lo = blk['lo']
        hi = blk['hi']
        print("\n--- Block %s: 0x%08x..0x%08x (0x%x B) ---" % (blk['name'], lo, hi, hi - lo + 1))

        if DRY:
            print("[dry] clearListing+setTMode(0x%08x..0x%08x)" % (lo, hi))
            for fn in blk['fns']:
                print("[dry] disasm_flow(0x%08x)" % fn['entry'])
                print("[dry] createFunction('%s')" % fn['name'])
                print("[dry] setPlate(%d chars)" % len(fn['plate']))
                n_fns += 1
            n_blocks += 1
            continue

        # Step 1: clearListing entire block, then setTMode=THUMB
        _clear_and_set_thumb(lo, hi)

        # Step 2: disasm each function in the block (flow-based, per-entry)
        for fn in blk['fns']:
            entry = fn['entry']
            print("[...] disasm_flow(0x%08x)" % entry)
            if not _disasm_flow(entry):
                print("[FAIL] disasm at 0x%08x -- skipping function" % entry)
                continue
            _create_function(entry, fn['name'], fn['plate'])
            n_fns += 1

        n_blocks += 1

    print("\n=== DisassembleF07Seg1Blocks DONE ===")
    print("  Blocks processed: %d / %d" % (n_blocks, len(BLOCKS)))
    print("  Functions created: %d (expected 5: fn1+fn2 in BlockA + 1 each in B,C,D)" % n_fns)
    print("  DRY=%s" % DRY)


main()
