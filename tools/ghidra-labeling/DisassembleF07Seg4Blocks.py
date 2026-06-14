# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF07Seg4Blocks.py -- F07 Seg-4 R4 disasm (5 ROM_INCBIN blocks -> THUMB code)
#
# Blocks (card effect handler dispatch table targets, 0x09e4xxxx range):
#
#   Block 1: 0x0805f47e..0x0805f49b (0x1e B) -- 1 sub-function
#     .zero 2 padding at 0x0805f47e (alignment), fn1 @ 0x0805f480
#     fn1: 0x0805f480 (THUMB+1=0x0805f481) -- CID=0x14d4 (A Feint Plan) @ 0x09e40dd4
#     Literal pool: 0x0805f494=gP1LifePoints(0x0201c4e0), 0x0805f498=FIELD_STATE_OFF(0x1cf4)
#     NOTE: 0x5f492 = bx lr instruction (0x4770), NOT a data slot; pool starts at 0x5f494.
#
#   Block 2: 0x0805f8b4..0x0805f8f3 (0x40 B) -- 1 sub-function
#     No .zero2 prefix; fn1 @ 0x0805f8b4
#     fn1: 0x0805f8b4 (THUMB+1=0x0805f8b5) -- CID=0x151c (Drop Off) @ 0x09e41068
#     Literal pool: 0x0805f8e8=gP1LifePoints(0x0201c4e0), 0x0805f8ec=P1LP_BLOCK2_OFF_1CE8(0x1ce8)
#     NOTE: Function name uses bit10 (31-21=10, lsls r0,r0,#21 -> blt; ROM[0x5f8de]=0x0540).
#
#   Block 3: 0x0805f92e..0x0805f967 (0x3a B) -- 1 sub-function
#     .zero 2 padding at 0x0805f92e, fn1 @ 0x0805f930
#     fn1: 0x0805f930 (THUMB+1=0x0805f931) -- CID=0x151e (Last Turn) @ 0x09e41098
#     Literal pool: 0x0805f958=gP1LifePoints(0x0201c4e0), 0x0805f95c=PLAYER_BLOCK_STRIDE(0x868),
#                   0x0805f960=P1LP_BLOCK2_OFF_1CE8(0x1ce8)
#
#   Block 4: 0x0805fa5c..0x0805fa83 (0x28 B) -- 1 sub-function
#     No .zero2 prefix; fn1 @ 0x0805fa5c
#     fn1: 0x0805fa5c (THUMB+1=0x0805fa5d) -- CID=0x12f4 + 13 other CIDs (shared utility)
#     Literal pool: 0x0805fa7c=gP1LifePoints(0x0201c4e0), 0x0805fa80=PLAYER_BLOCK_STRIDE(0x868)
#
#   Block 5: 0x0805fc10..0x0805fc3b (0x2c B) -- 1 sub-function
#     No .zero2 prefix; fn1 @ 0x0805fc10
#     fn1: 0x0805fc10 (THUMB+1=0x0805fc11) -- CID=0x1546 (Trap Dustshoot) @ 0x09e411b8
#     Literal pool: 0x0805fc34=gP1LifePoints(0x0201c4e0), 0x0805fc38=PLAYER_BLOCK_STRIDE(0x868)
#
# Paradigm: DisassembleF07Seg3Blocks.py (file 00 Seg-5c)
#   1. clearListing entire block range
#   2. setTMode=THUMB for entire range
#   3. createWord for .zero 2 pad where present
#   4. DisassembleCommand per fn entry (flow-based; NOT entire range at once)
#   5. createFunction + setName (USER_DEFINED)
#   6. setPlateComment (pure ASCII only)
#
# Literal pool DWORDs will be fixed post-export via FixF07Seg4LiteralPools.py
#
# Backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260614-141354-pre-f07seg4

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


def _create_function(entry_addr, func_name, plate_text, eol_text=None):
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
        # ASCII gate
        bad = any(ord(ch) > 127 for ch in plate_text)
        if bad:
            print("[FAIL] non-ASCII in plate @ 0x%08x -- skipping plate set" % entry_addr)
        else:
            cu.setComment(CodeUnit.PLATE_COMMENT, plate_text)
            print("[ok ] plate set (%d chars) @ 0x%08x" % (len(plate_text), entry_addr))
        if eol_text is not None:
            bad_eol = any(ord(ch) > 127 for ch in eol_text)
            if bad_eol:
                print("[FAIL] non-ASCII in EOL @ 0x%08x -- skipping EOL" % entry_addr)
            else:
                cu.setComment(CodeUnit.EOL_COMMENT, eol_text)
                print("[ok ] EOL set (%d chars) @ 0x%08x" % (len(eol_text), entry_addr))
    else:
        print("[warn] no CodeUnit at 0x%08x for plate" % entry_addr)


# ---------------------------------------------------------------------------
# Block definitions
# ---------------------------------------------------------------------------

BLOCKS = [
    # Block 1: 0x0805f47e..0x0805f49b (0x1e B) -- 1 sub-function
    # .zero 2 padding at 0x0805f47e, fn1 @ 0x0805f480
    # CID=0x14d4 (A Feint Plan, pw=68170903)
    {
        'name': '1',
        'lo': 0x0805f47e,
        'hi': 0x0805f49b,
        'pad_word': 0x0805f47e,
        'fns': [
            {
                'entry': 0x0805f480,
                'name': 'check_field_state_leq3_for_cid_14d4',
                'plate': (
                    'Reached via card effect handler dispatch table 0x09e40de0. '
                    'CID=0x14d4 (A Feint Plan, pw=68170903). fn2 of handler list. '
                    'Reads gP1LifePoints+FIELD_STATE_OFF(0x1cf4); '
                    'returns 1 if field_state <= 3, 0 if field_state > 3. '
                    'Exit: bx lr. '
                    'Lit pool: 0x5f494=gP1LifePoints(0x0201c4e0), 0x5f498=FIELD_STATE_OFF(0x1cf4). '
                    'NOTE: 0x5f492 = bx lr instruction (0x4770), NOT a data slot.'
                ),
                'eol': None,
            },
        ],
    },

    # Block 2: 0x0805f8b4..0x0805f8f3 (0x40 B) -- 1 sub-function
    # No .zero2 prefix; fn1 @ 0x0805f8b4
    # CID=0x151c (Drop Off, pw=55773067)
    {
        'name': '2',
        'lo': 0x0805f8b4,
        'hi': 0x0805f8f3,
        'pad_word': None,
        'fns': [
            {
                'entry': 0x0805f8b4,
                'name': 'check_zone640_opponent_turn_bit10_for_cid_151c',
                'plate': (
                    'Reached via card effect handler dispatch table 0x09e41068. '
                    'CID=0x151c (Drop Off, pw=55773067). fn2 of handler list. '
                    'Gate: curr_turn==opponent AND zone_type==0x640 AND slot[+0x14].bit10 set '
                    '(lsls r0,r0,#21 -> blt; ROM[0x5f8de]=0x0540; 31-21=bit10). '
                    'Returns 1 if all gates pass, 0 otherwise. Exit: bx lr. '
                    'Lit pool: 0x5f8e8=gP1LifePoints(0x0201c4e0), 0x5f8ec=P1LP_BLOCK2_OFF_1CE8(0x1ce8).'
                ),
                'eol': None,
            },
        ],
    },

    # Block 3: 0x0805f92e..0x0805f967 (0x3a B) -- 1 sub-function
    # .zero 2 padding at 0x0805f92e, fn1 @ 0x0805f930
    # CID=0x151e (Last Turn, pw=28566710)
    {
        'name': '3',
        'lo': 0x0805f92e,
        'hi': 0x0805f967,
        'pad_word': 0x0805f92e,
        'fns': [
            {
                'entry': 0x0805f930,
                'name': 'check_opp_turn_lp_leq1000_return2_for_cid_151e',
                'plate': (
                    'Reached via card effect handler dispatch table 0x09e41098. '
                    'CID=0x151e (Last Turn, pw=28566710). fn3 of handler list. '
                    'Gate: player LP<=1000 AND curr_turn==opponent -> return 2; else return 0. '
                    '0xfa<<2=0x3e8=1000 LP threshold (movs r0,#0xfa; lsls r0,r0,#2). '
                    'Exit: bx lr. .zero 2 pad at 0x0805f92e. '
                    'Lit pool: 0x5f958=gP1LifePoints(0x0201c4e0), 0x5f95c=PLAYER_BLOCK_STRIDE(0x868), '
                    '0x5f960=P1LP_BLOCK2_OFF_1CE8(0x1ce8).'
                ),
                'eol': None,
            },
        ],
    },

    # Block 4: 0x0805fa5c..0x0805fa83 (0x28 B) -- 1 sub-function
    # No .zero2 prefix; fn1 @ 0x0805fa5c
    # 14 CIDs (shared utility function): 0x12f4 + 0x14ee (De-Spell Germ Weapon) + 12 others
    {
        'name': '4',
        'lo': 0x0805fa5c,
        'hi': 0x0805fa83,
        'pad_word': None,
        'fns': [
            {
                'entry': 0x0805fa5c,
                'name': 'check_player_lp_state_off10_nonzero',
                'plate': (
                    'Shared utility: reached via handler tables for 14 CIDs across 0x09e3xxxx and 0x09e4xxxx. '
                    'Includes CID=0x12f4 (0x09e3xxxx) and CID=0x14ee (De-Spell Germ Weapon) among others. '
                    'Reads gP1LifePoints[player_id*0x868+0x10]; '
                    'returns 1 if field nonzero (LP state active), 0 if zero. '
                    'player_id = ldrb [slot_ptr+2] & 1. Exit: bx lr. '
                    'Lit pool: 0x5fa7c=gP1LifePoints(0x0201c4e0), 0x5fa80=PLAYER_BLOCK_STRIDE(0x868).'
                ),
                'eol': None,
            },
        ],
    },

    # Block 5: 0x0805fc10..0x0805fc3b (0x2c B) -- 1 sub-function
    # No .zero2 prefix; fn1 @ 0x0805fc10
    # CID=0x1546 (Trap Dustshoot, pw=64697231)
    {
        'name': '5',
        'lo': 0x0805fc10,
        'hi': 0x0805fc3b,
        'pad_word': None,
        'fns': [
            {
                'entry': 0x0805fc10,
                'name': 'check_player_zone_count_above3_for_cid_1546',
                'plate': (
                    'Reached via card effect handler dispatch table 0x09e411b8. '
                    'CID=0x1546 (Trap Dustshoot, pw=64697231). fn2 of handler list. '
                    'Reads gP1LifePoints[player_id*0x868+0x0c] (zone/hand count field). '
                    'Returns 1 if count > 3 (>=4 zones/cards), 0 otherwise. '
                    'ZONE_COUNT_OFFSET=0x0c (gP1ZoneHandCount=0x0201c4ec=gP1LifePoints+0xc). '
                    'Exit: bx lr (via adds r0,r3,#0; bls+0 -> r3 stays 0; movs r3,#1 when >3). '
                    'Lit pool: 0x5fc34=gP1LifePoints(0x0201c4e0), 0x5fc38=PLAYER_BLOCK_STRIDE(0x868).'
                ),
                'eol': None,
            },
        ],
    },
]


def main():
    print("=== DisassembleF07Seg4Blocks (DRY=%s) ===" % DRY)
    n_blocks = 0
    n_fns = 0

    for blk in BLOCKS:
        lo = blk['lo']
        hi = blk['hi']
        print("\n--- Block %s: 0x%08x..0x%08x (0x%x B) ---" % (blk['name'], lo, hi, hi - lo + 1))

        if DRY:
            print("[dry] clearListing+setTMode(0x%08x..0x%08x)" % (lo, hi))
            if blk.get('pad_word') is not None:
                print("[dry] createWord @ 0x%08x (.zero2 pad)" % blk['pad_word'])
            for fn in blk['fns']:
                print("[dry] disasm_flow(0x%08x)" % fn['entry'])
                print("[dry] createFunction('%s')" % fn['name'])
                print("[dry] setPlate(%d chars)" % len(fn['plate']))
                if fn.get('eol'):
                    print("[dry] setEOL('%s')" % fn['eol'])
                n_fns += 1
            n_blocks += 1
            continue

        # Step 1: clearListing entire block, then setTMode=THUMB
        _clear_and_set_thumb(lo, hi)

        # Step 2: createWord for .zero2 pad if needed
        if blk.get('pad_word') is not None:
            _create_word(blk['pad_word'])

        # Step 3: disasm each sub-function in the block (flow-based, per-entry)
        for fn in blk['fns']:
            entry = fn['entry']
            print("[...] disasm_flow(0x%08x)" % entry)
            if not _disasm_flow(entry):
                print("[FAIL] disasm at 0x%08x -- skipping function" % entry)
                continue
            _create_function(entry, fn['name'], fn['plate'], fn.get('eol'))
            n_fns += 1

        n_blocks += 1

    print("\n=== DisassembleF07Seg4Blocks DONE ===")
    print("  Blocks processed: %d / %d" % (n_blocks, len(BLOCKS)))
    print("  Functions created: %d (expected 5: 1+1+1+1+1)" % n_fns)
    print("  DRY=%s" % DRY)


main()
