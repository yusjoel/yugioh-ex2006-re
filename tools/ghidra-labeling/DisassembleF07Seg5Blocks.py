# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF07Seg5Blocks.py -- F07 Seg-5 R4 disasm (4 ROM_INCBIN/.byte blocks -> THUMB code)
#
# Blocks (card effect handler dispatch table targets, 0x09e4xxxx range):
#
#   Block 1: 0x0806008c..0x080600b3 (0x28 B) -- 1 sub-function
#     No .zero prefix; fn @ 0x0806008c
#     fn: 0x0806008c (THUMB+1=0x0806008d) -- CID=0x159a (Reasoning) @ 0x09e412c0
#     Lit pool: 0x080600a8=gP1LifePoints(0x0201c4e0), 0x080600ac=PLAYER_BLOCK_STRIDE(0x868)
#     Exit: bx lr at 0x080600b2. Block ends at 0x080600b3.
#
#   Block 2: 0x08060386..0x080603b7 (0x32 B) -- 1 sub-function
#     .zero 2 pad at 0x08060386; fn @ 0x08060388
#     fn: 0x08060388 (THUMB+1=0x08060389) -- CID=0x15dc (Helping Robo For Combat) @ 0x09e44290
#     Exit: bx lr at 0x080603b4. .zero 2 pad at 0x080603b6. Block ends at 0x080603b7.
#     Lit pool within fn: 2 pool slots within fn body (no named DAT_)
#
#   Block 3: 0x08060588..0x08060603 (0x7c B) -- 3 sub-functions
#     F1 @ 0x08060588 -- CID=0x15f0 (Thunder of Ruler) @ 0x09e41560
#       Lit pool: 0x080605a8=gP1LifePoints(0x0201c4e0), 0x080605ac=P1LP_BLOCK2_OFF_1CE8(0x1ce8),
#                 0x080605b0=FIELD_STATE_OFF(0x1cf4)
#       Exit: bx lr at 0x080605b6. F2 starts at 0x080605b8.
#     F2 @ 0x080605b8 -- CID=0x15f2 (Meteorain) @ 0x09e41590
#       Lit pool: 0x080605d0=gP1LifePoints(0x0201c4e0), 0x080605d4=P1LP_BLOCK2_OFF_1CE8(0x1ce8),
#                 0x080605ec=FIELD_STATE_OFF(0x1cf4)
#       Exit: bx lr at 0x080605e8. .zero 2 pad at 0x080605ea. F3 starts at 0x080605f0.
#     F3 @ 0x080605f0 -- CID=0x15f3 (Pineapple Blast) @ 0x09e415a8
#       push{r4,r5,lr} fn body continues into named asm past 0x08060604
#       Lit pool internal: within Block3 body up to 0x08060603 (no named slots in this sub-block)
#       Exit: pop{r4,r5};pop{r1};bx r1 at 0x0806063a/3c. End of body at 0x0806063e.
#
#   Block 4: 0x08060800..0x08060807 (0x08 B) -- 1 sub-function (.byte fn prologue)
#     .byte 0x10,0xb5,... = push{r4,lr}; fn body continues in named asm at 0x08060808
#     fn: 0x08060800 (THUMB+1=0x08060801) -- CID=0x1624 (Pitch-Black Power Stone)
#         @ tables 0x09e41638 and 0x09e46bd0; also 20 direct-bl callers
#     The .byte area is only 8 bytes; rest of fn body is in already-disassembled named asm.
#     Lit pool within fn body (in named asm area): 0x08060834=gP1LifePoints(0x0201c4e0)
#     Named pool slot in EQ_SLOTS: 0x08060838=DAT_08060838=P1LP_BLOCK2_OFF_1CE8(0x1ce8)
#
# Paradigm: DisassembleF07Seg4Blocks.py (file 00 Seg-5c)
#   1. clearListing entire block range
#   2. setTMode=THUMB for entire range
#   3. createWord for .zero 2 pad where present
#   4. DisassembleCommand per fn entry (flow-based; NOT entire range at once)
#   5. createFunction + setName (USER_DEFINED)
#   6. setPlateComment (pure ASCII only)
#
# Literal pool DWORDs will be fixed post-disasm via FixF07Seg5LiteralPools.py
#
# Backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260614-154713-pre-f07seg5

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
    # Block 1: 0x0806008c..0x080600b3 (0x28 B) -- 1 sub-function
    # No .zero prefix; fn @ 0x0806008c
    # CID=0x159a (Reasoning, pw=58577036)
    {
        'name': '1',
        'lo': 0x0806008c,
        'hi': 0x080600b3,
        'pad_word': None,
        'fns': [
            {
                'entry': 0x0806008c,
                'name': 'check_equip_slot_eligible_by_lp_slot_for_cid_159a',
                'plate': (
                    'Equip slot eligibility predicate for Reasoning (CID 0x159A, pw=58577036). '
                    'Leaf fn. '
                    'Reads gP1LifePoints[player*0x868+0x10] (LP slot activation count); '
                    'returns 1 if nonzero (LP active), 0 otherwise. '
                    'Reached via card effect handler dispatch table 0x09e412c0, Reasoning CID 0x159A. '
                    'Lit pool: 0x080600a8=gP1LifePoints(0x0201c4e0), 0x080600ac=PLAYER_BLOCK_STRIDE(0x868).'
                ),
                'eol': None,
            },
        ],
    },

    # Block 2: 0x08060386..0x080603b7 (0x32 B) -- 1 sub-function
    # .zero 2 padding at 0x08060386; fn @ 0x08060388
    # CID=0x15dc (Helping Robo For Combat, pw=47025270)
    {
        'name': '2',
        'lo': 0x08060386,
        'hi': 0x080603b7,
        'pad_word': 0x08060386,
        'fns': [
            {
                'entry': 0x08060388,
                'name': 'check_equip_slot_eligible_by_type_and_player_for_cid_15dc',
                'plate': (
                    'Equip slot eligibility predicate for Helping Robo For Combat (CID 0x15DC, pw=47025270). '
                    'Leaf fn. '
                    'Checks slot type field (halfword[+2] bits[10:4] via mask 0xfc0) against 0x180 (0xb0<<1). '
                    'Reads slot[+0x14] bit9 (lsls#0x16/lsrs#0x1f); compares against slot player bit0. '
                    'Verifies zone detail bits. Returns 1 on pass, 0 on fail. '
                    'Reached via card effect handler dispatch table 0x09e44290, Helping Robo For Combat CID 0x15DC. '
                    '.zero 2 alignment pad at 0x08060386 before fn entry.'
                ),
                'eol': None,
            },
        ],
    },

    # Block 3: 0x08060588..0x08060603 (0x7c B) -- 3 sub-functions
    # F1 @ 0x08060588 (CID 0x15f0), F2 @ 0x080605b8 (CID 0x15f2), F3 @ 0x080605f0 (CID 0x15f3)
    # F3 body extends beyond block into named asm at 0x08060604..0x0806063e
    {
        'name': '3',
        'lo': 0x08060588,
        'hi': 0x08060603,
        'pad_word': None,
        'fns': [
            # F1: Thunder of Ruler (CID 0x15f0)
            {
                'entry': 0x08060588,
                'name': 'check_equip_slot_eligible_by_active_player_phase_for_cid_15f0',
                'plate': (
                    'Equip slot eligibility predicate for Thunder of Ruler (CID 0x15F0, pw=91781589). '
                    'Leaf fn. '
                    'Gate: reads gP1LifePoints[player*0x868+0x1ce8] (active player id); '
                    'if not equal to slot player id returns 0. '
                    'Then reads gP1LifePoints+0x1cf4 (duel phase); if not equal to 1 returns 0. '
                    'Else returns 1. '
                    'Reached via card effect handler dispatch table 0x09e41560, Thunder of Ruler CID 0x15F0. '
                    'Lit pool: 0x080605a8=gP1LifePoints(0x0201c4e0), '
                    '0x080605ac=P1LP_BLOCK2_OFF_1CE8(0x1ce8), 0x080605b0=FIELD_STATE_OFF(0x1cf4).'
                ),
                'eol': None,
            },
            # F2: Meteorain (CID 0x15f2)
            {
                'entry': 0x080605b8,
                'name': 'check_equip_slot_eligible_by_active_player_phase_for_cid_15f2',
                'plate': (
                    'Equip slot eligibility predicate for Meteorain (CID 0x15F2, pw=64274292). '
                    'Leaf fn. Same active_player+duel_phase gate pattern as F1 (CID 0x15F0 sibling). '
                    'Gate: reads gP1LifePoints[player*0x868+0x1ce8] (active player); '
                    'if mismatch returns 0. '
                    'Reads gP1LifePoints+0x1cf4 (phase); if not 3 returns 1, '
                    'else reads opponent LP count at +0xc; returns 1 if 0, else 0. '
                    'Reached via card effect handler dispatch table 0x09e41590, Meteorain CID 0x15F2. '
                    'Lit pool: 0x080605d0=gP1LifePoints(0x0201c4e0), '
                    '0x080605d4=P1LP_BLOCK2_OFF_1CE8(0x1ce8), 0x080605ec=FIELD_STATE_OFF(0x1cf4). '
                    '.zero 2 pad at 0x080605ea before F3.'
                ),
                'eol': None,
            },
            # F3: Pineapple Blast (CID 0x15f3)
            {
                'entry': 0x080605f0,
                'name': 'check_equip_slot_eligible_by_monster_zone_type_for_cid_15f3',
                'plate': (
                    'Equip slot eligibility predicate for Pineapple Blast (CID 0x15F3, pw=90669991). '
                    'push{r4,r5,lr} fn. '
                    'Calls count_occupied_monster_zones(opponent); '
                    'compares result against player monster zone count (r4); '
                    'checks zone_type bits[10:4] mask 0xfc0 against 0x180; '
                    'verifies slot[+0x14] bit22 vs slot player bit0. '
                    'Returns 1 on all pass, 0 on fail. '
                    'Handler dispatch table 0x09e415a8, Pineapple Blast CID 0x15F3. '
                    'CID verified: read32(0x09e4159c)=0x000015f3; fn_ptr=0x080605f1 (THUMB+1). '
                    'BL target at 0x080605fe/0x08060600 = count_occupied_monster_zones @ 0x08033188.'
                ),
                'eol': None,
            },
        ],
    },

    # Block 4: 0x08060800..0x08060807 (0x08 B) -- 1 sub-function (.byte fn prologue)
    # No .zero prefix; fn @ 0x08060800
    # CID=0x1624 (Pitch-Black Power Stone); also 20 direct-bl callers
    # fn body continues into named asm at 0x08060808..0x08060850
    {
        'name': '4',
        'lo': 0x08060800,
        'hi': 0x08060807,
        'pad_word': None,
        'fns': [
            {
                'entry': 0x08060800,
                'name': 'check_equip_slot_eligible_active_player_with_chain_and_node_count',
                'plate': (
                    'Equip slot eligibility predicate: active player gate + chain absent + effect node count. '
                    'push{r4,lr}. '
                    'Gate: gP1LifePoints+0x1ce8 (active player id) vs slot player id (bit0 byte[+2]); '
                    'mismatch -> defer path. '
                    'Match: check_equip_slot_chain_absent; chain present -> defer. '
                    'count_effect_node_zone_activations; if >0 returns 2. '
                    'Defer: byte[+3] bits[5:4] mask 0x30; nonzero returns 0, else 3. '
                    'Handler for Pitch-Black Power Stone CID 0x1624 at tables 0x09e41638, 0x09e46bd0. '
                    'Also reached via 20 direct bl callers. '
                    'fn prologue in .byte 8B at 0x08060800; body continues named asm at 0x08060808. '
                    'Lit pool: 0x08060834=gP1LifePoints(0x0201c4e0), 0x08060838=P1LP_BLOCK2_OFF_1CE8(0x1ce8).'
                ),
                'eol': None,
            },
        ],
    },
]


def main():
    print("=== DisassembleF07Seg5Blocks (DRY=%s) ===" % DRY)
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
                print("[dry] createFunction('%s') plate=%d chars" % (fn['name'], len(fn['plate'])))
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

    print("\n=== DisassembleF07Seg5Blocks DONE ===")
    print("  Blocks processed: %d / %d" % (n_blocks, len(BLOCKS)))
    print("  Functions created: %d (expected 7: 1+1+3+1)" % n_fns)
    print("  DRY=%s" % DRY)


main()
