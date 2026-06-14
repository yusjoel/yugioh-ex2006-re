# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF07Seg3Blocks.py -- F07 Seg-3 R4 disasm (4 ROM_INCBIN blocks -> THUMB code)
#
# Blocks (card effect handler dispatch table targets, 0x09e4xxxx range):
#
#   Block 1: 0x0805e744..0x0805e78f (0x4c B) -- 2 sub-functions
#     No .zero2 prefix (fn1 starts at block start 0x5e744)
#     fn1: 0x0805e744 (THUMB+1=0x0805e745) -- CID=0x13f9 (Fairy Box) @ 0x09e43948
#     fn2: 0x0805e778 (THUMB+1=0x0805e779) -- CID=0x13fa (Torrential Tribute) @ 0x09e407c8
#          fn2 EOL: "type_field in [6..8] returns 1, else 0"
#
#   Block 2: 0x0805ed4a..0x0805ed73 (0x2a B) -- 1 sub-function
#     .zero 2 padding at 0x0805ed4a, fn1 starts at 0x5ed4c
#     fn1: 0x0805ed4c (THUMB+1=0x0805ed4d) -- CID=0x144e (unassigned) @ 0x09e439c0
#
#   Block 3: 0x0805ed8e..0x0805ee1f (0x92 B) -- 3 sub-functions
#     .zero 2 padding at 0x0805ed8e, fn1 starts at 0x5ed90
#     fn1: 0x0805ed90 (THUMB+1=0x0805ed91) -- CID=0x1450 (Spirit of the Breeze) @ 0x09e439e4;
#                                              ALSO CID=0x1855 (Castle Gate) @ 0x09e47014
#     fn2: 0x0805edc0 (THUMB+1=0x0805edc1) -- CID=0x1451 (Dancing Fairy) @ 0x09e439fc
#          fn1/fn2 differ only in branch cond at byte offset 31: fn1=BNE(0xd1) fn2=BEQ(0xd0)
#     fn3: 0x0805edf0 (THUMB+1=0x0805edf1) -- CID=0x1460 (Meteor of Destruction) @ 0x09e40a2c
#
#   Block 4: 0x0805ee9c..0x0805ef87 (0xec B) -- 5 sub-functions
#     No .zero2 prefix (fn1 starts at block start 0x5ee9c)
#     fn1: 0x0805ee9c (THUMB+1=0x0805ee9d) -- CID=0x1468 (Destiny Board) @ 0x09e43a2c
#          Exit: pop{r1}/bx r1 (0xbc02/0x4708)
#     fn2: 0x0805eeb8 (THUMB+1=0x0805eeb9) -- CID=0x146f (Cathedral of Nobles) @ 0x09e4660c
#          Exit: pop{r1}/bx r1
#     fn3: 0x0805eee4 (THUMB+1=0x0805eee5) -- CID=0x1472 (Embodiment of Apophis) @ 0x09e40ad4
#          Exit: pop{r1}/bx r1
#     fn4: 0x0805ef10 (THUMB+1=0x0805ef11) -- CID=0x1475 (Makiu) @ 0x09e40b04
#          Exit: pop{r1}/bx r1
#     fn5: 0x0805ef4c (THUMB+1=0x0805ef4d) -- CID=0x147f (Jowgen the Spiritualist) @ 0x09e4663c
#          Exit: pop{r1}/bx r1
#
# Sub-fn boundaries verified by reviewer:
#   Block1: fn1 end 0x0805e778, fn2 end 0x0805e790 (bx lr 0x4770)
#   Block2: fn1 end 0x0805ed74 (bx lr)
#   Block3: fn1 end 0x0805edc0, fn2 end 0x0805edf0, fn3 end 0x0805ee20 (bx lr)
#   Block4: fn1-fn5 end via pop{r1}/bx r1 (0xbc02/0x4708)
#           fn1 end 0x0805eeb8, fn2 end 0x0805eee4, fn3 end 0x0805ef10
#           fn4 end 0x0805ef4c, fn5 end 0x0805ef88
#
# Paradigm: DisassembleF07Seg2Blocks.py (file 00 Seg-5c)
#   1. clearListing entire block range
#   2. setTMode=THUMB for entire range
#   3. createWord for .zero 2 pad where present
#   4. DisassembleCommand per fn entry (flow-based; NOT entire range at once)
#   5. createFunction + setName (USER_DEFINED)
#   6. setPlateComment (pure ASCII only)
#   7. EOL comment on fn2 of Block1 (subscripted semantics note)
#
# Backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260614-130344-pre-f07seg3

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
        cu.setComment(CodeUnit.PLATE_COMMENT, plate_text)
        print("[ok ] plate set (%d chars) @ 0x%08x" % (len(plate_text), entry_addr))
        if eol_text is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol_text)
            print("[ok ] EOL set (%d chars) @ 0x%08x" % (len(eol_text), entry_addr))
    else:
        print("[warn] no CodeUnit at 0x%08x for plate" % entry_addr)


# ---------------------------------------------------------------------------
# Block definitions
# ---------------------------------------------------------------------------

BLOCKS = [
    # Block 1: 0x0805e744..0x0805e78f (0x4c B) -- 2 sub-functions
    # No .zero2 prefix; fn1 @ 0x0805e744, fn2 @ 0x0805e778
    {
        'name': '1',
        'lo': 0x0805e744,
        'hi': 0x0805e78f,
        'pad_word': None,
        'fns': [
            {
                'entry': 0x0805e744,
                'name': 'check_equip_type480_cross_player_for_cid_13f9',
                'plate': (
                    'Reached via card effect handler dispatch table 0x09e4393c. '
                    'CID=0x13f9 (Fairy Box). '
                    'Checks: type_bits (halfword[2..3] & 0xfc0) == 0x480; '
                    'slot[+0x14] != 0 (active); '
                    'gEquipChainSlotRefs[0] (active_player) != player_id (cross-player). '
                    'Returns 1 if all pass, 0 otherwise. bx lr exit. '
                    'Lit 0x5e770=gEquipChainSlotRefs(0x0201bb90). '
                    'Mask 0xfc0, type 0x480 from ROM bytes 0x1c02/0x20fc/0x0100/0x8851.'
                ),
                'eol': None,
            },
            {
                'entry': 0x0805e778,
                'name': 'check_equip_type_bits_range6_8_for_cid_13fa',
                'plate': (
                    'Reached via card effect handler dispatch table 0x09e407bc. '
                    'CID=0x13fa (Torrential Tribute, pw=53582869). '
                    '3-fn_ptr multi-entry: also 0x08064661+1 and 0x08050751+1. '
                    'Extracts bits[11:6] of halfword at slot_ptr[2..3] via lsl20+lsr26. '
                    'bgt->movs r0,#0; blt->movs r0,#0; range [6..8]->movs r0,#1. '
                    'Returns 1 if type_field in [6..8], else 0. bx lr exit.'
                ),
                'eol': 'type_field in [6..8] returns 1, else 0',
            },
        ],
    },
    # Block 2: 0x0805ed4a..0x0805ed73 (0x2a B) -- 1 sub-function
    # .zero 2 padding at 0x0805ed4a, fn1 @ 0x0805ed4c
    {
        'name': '2',
        'lo': 0x0805ed4a,
        'hi': 0x0805ed73,
        'pad_word': 0x0805ed4a,
        'fns': [
            {
                'entry': 0x0805ed4c,
                'name': 'check_slot_count_exceeds_2_for_cid_144e',
                'plate': (
                    'Reached via card effect handler dispatch table 0x09e439c0. '
                    'CID=0x144e (unassigned slot, not in card-stats.s). '
                    'CID=0x144f at 0x09e439cc shares fn_ptr 0x805ed4d (adjacent slot, same handler). '
                    'player_id = slot_ptr[2] & 1; '
                    'reads gP1LifePoints[player_id*0x868+0x10] (per-player slot count base); '
                    'returns 1 if count > 2, else 0. bx lr exit. '
                    '.zero 2 alignment pad precedes entry at 0x0805ed4a. '
                    'Lit 0x5ed68=gP1LifePoints(0x0201c4e0), 0x5ed6c=PLAYER_BLOCK_STRIDE(0x868).'
                ),
                'eol': None,
            },
        ],
    },
    # Block 3: 0x0805ed8e..0x0805ee1f (0x92 B) -- 3 sub-functions
    # .zero 2 padding at 0x0805ed8e, fn1 @ 0x0805ed90
    {
        'name': '3',
        'lo': 0x0805ed8e,
        'hi': 0x0805ee1f,
        'pad_word': 0x0805ed8e,
        'fns': [
            {
                'entry': 0x0805ed90,
                'name': 'check_zone_field6_hw_zero_for_cid_1450',
                'plate': (
                    'Reached via card effect handler dispatch table. '
                    'CID=0x1450 (Spirit of the Breeze) at 0x09e439e4; '
                    'ALSO CID=0x1855 (Castle Gate) at 0x09e47014 (second handler table). '
                    'Extracts player_id=slot_ptr[2]&1, zone_idx=slot_ptr[2]>>1; '
                    'computes addr=gDuelFieldSlots+zone_idx*16+player_id*(4+0x868); '
                    'reads halfword at [addr+6]; returns 1 if hw==0, 0 otherwise. '
                    'BNE (0xd1) at byte offset 31 confirms zero->return-1 path. '
                    'bx lr exit. .zero 2 pad at 0x0805ed8e. '
                    'Lit 0x5edb4=PLAYER_BLOCK_STRIDE(0x868), 0x5edb8=gDuelFieldSlots(0x0201c510).'
                ),
                'eol': None,
            },
            {
                'entry': 0x0805edc0,
                'name': 'check_zone_field6_hw_nonzero_for_cid_1451',
                'plate': (
                    'Reached via card effect handler dispatch table 0x09e439fc. '
                    'CID=0x1451 (Dancing Fairy, pw=90925163). '
                    'Identical structure to check_zone_field6_hw_zero_for_cid_1450 EXCEPT '
                    'branch condition inverted at byte offset 31: BEQ (0xd0) vs BNE (0xd1). '
                    'Returns 1 if halfword[+6] != 0 (field6 set), 0 if hw==0. '
                    'raw ref @0x824c74a is NOT 4B-aligned (foreign code, confirmed non-table). '
                    'bx lr exit.'
                ),
                'eol': None,
            },
            {
                'entry': 0x0805edf0,
                'name': 'check_opponent_lp_above_3000_for_cid_1460',
                'plate': (
                    'Reached via card effect handler dispatch table 0x09e40a2c. '
                    'CID=0x1460 (Meteor of Destruction, pw=33767325). '
                    'opponent_id = player_id ^ 1 (movs r1,#1; eors r0,r1); '
                    'reads gP1LifePoints[opponent_id*0x868] = opponent LP; '
                    'returns 1 if opponent_LP > 0xBB8 (3000 decimal), 0 otherwise. '
                    'bx lr exit. '
                    'Lit 0x5ee14=gP1LifePoints(0x0201c4e0), 0x5ee18=PLAYER_BLOCK_STRIDE(0x868), '
                    '0x5ee1c=0x0BB8 (3000 LP threshold).'
                ),
                'eol': None,
            },
        ],
    },
    # Block 4: 0x0805ee9c..0x0805ef87 (0xec B) -- 5 sub-functions
    # No .zero2 prefix; fn1 @ 0x0805ee9c
    # All fns exit via pop{r1}/bx r1 (0xbc02/0x4708)
    {
        'name': '4',
        'lo': 0x0805ee9c,
        'hi': 0x0805ef87,
        'pad_word': None,
        'fns': [
            {
                'entry': 0x0805ee9c,
                'name': 'check_free_monster_zone_for_cid_1468',
                'plate': (
                    'Reached via card effect handler dispatch table 0x09e43a2c. '
                    'CID=0x1468 (Destiny Board, pw=35506430; DESTINY_BOARD_CID in card_info.inc). '
                    'player_id = slot_ptr[2]&1; '
                    'calls find_first_available_monster_slot_for_player(player_id) (0x08033bf4); '
                    'returns 1 if result >= 0 (free monster zone exists), 0 if < 0. '
                    'Exit: pop{r1}/bx r1 (0xbc02/0x4708). '
                    'BL 0x5eea4->0x08033bf4 = find_first_available_monster_slot_for_player.'
                ),
                'eol': None,
            },
            {
                'entry': 0x0805eeb8,
                'name': 'check_neo_daedalus_no_banisher_for_cid_146f',
                'plate': (
                    'Reached via card effect handler dispatch table 0x09e4660c. '
                    'CID=0x146f (Cathedral of Nobles, pw=30236990). '
                    '3-fn_ptr entry: also 0x806fded+1 and 0x8052a21+1. '
                    '(1) check_field_spell_neo_daedalus_group_placeable(player_id) '
                    '    (BL->0x0803bb7c): if 0 -> return 0. '
                    '(2) count_field_copies_of_card(BANISHER_OF_THE_LIGHT_CID=0x1332) '
                    '    (BL->0x0803279c): if > 0 -> return 0; else return 1. '
                    'Exit: pop{r1}/bx r1. Lit 0x5eed8=BANISHER_OF_THE_LIGHT_CID(0x1332).'
                ),
                'eol': None,
            },
            {
                'entry': 0x0805eee4,
                'name': 'check_field_state24_neo_daedalus_for_cid_1472',
                'plate': (
                    'Reached via card effect handler dispatch table 0x09e40ad4. '
                    'CID=0x1472 (Embodiment of Apophis, pw=31386180; EMBODIMENT_OF_APOPHIS_CID). '
                    'Reads gP1LifePoints[FIELD_STATE_OFF=0x1cf4] = field_state; '
                    'if field_state not in {2,4} -> return 0; '
                    'else calls check_equip_slot_eligible_neo_daedalus_with_monster_placeable '
                    '(BL->0x080609a4, asm/07 L11238) and returns its result. '
                    'cmp r0,#2/beq + cmp r0,#4/beq confirm field_state check. '
                    'Exit: pop{r1}/bx r1. Lit 0x5eefc=gP1LifePoints, 0x5ef00=FIELD_STATE_OFF.'
                ),
                'eol': None,
            },
            {
                'entry': 0x0805ef10,
                'name': 'check_chain_match_opponent_for_cid_1475',
                'plate': (
                    'Reached via card effect handler dispatch table 0x09e40b04. '
                    'CID=0x1475 (Makiu, pw=09436822). '
                    '3-fn_ptr entry: also 0x080701a5+1 and 0x8052aa9+1. '
                    'Reads field_state at gP1LifePoints[FIELD_STATE_OFF=0x1cf4]; '
                    'if field_state != 2 -> return 0. '
                    'opponent_id = 1 - player_id; '
                    'calls count_slots_with_chain_field_match(opponent_id,0,0) '
                    '(BL->0x08033294, asm/02 L15873); '
                    'returns 1 if count > 0, else 0. Exit: pop{r1}/bx r1. '
                    'Lit 0x5ef24=gP1LifePoints, 0x5ef28=FIELD_STATE_OFF(0x1cf4).'
                ),
                'eol': None,
            },
            {
                'entry': 0x0805ef4c,
                'name': 'check_field_0c_nonzero_no_banisher_for_cid_147f',
                'plate': (
                    'Reached via card effect handler dispatch table 0x09e4663c. '
                    'CID=0x147f (Jowgen the Spiritualist, pw=41855169). '
                    '4-fn_ptr entry: also 0x8064661+1, 0x8053035+1, 0x8057661+1. '
                    'player_id = slot_ptr[2]&1; '
                    'reads gP1LifePoints[player_id*0x868+0x0c] (gP1ZoneHandCount-area); '
                    'if value == 0 -> return 0. '
                    'calls count_field_copies_of_card(BANISHER_OF_THE_LIGHT_CID=0x1332) '
                    '(BL->0x0803279c); if count > 0 -> return 0; else return 1. '
                    'Exit: pop{r1}/bx r1. '
                    'Lit 0x5ef74=gP1LifePoints, 0x5ef78=PLAYER_BLOCK_STRIDE, 0x5ef7c=0x1332.'
                ),
                'eol': None,
            },
        ],
    },
]


def main():
    print("=== DisassembleF07Seg3Blocks (DRY=%s) ===" % DRY)
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

    print("\n=== DisassembleF07Seg3Blocks DONE ===")
    print("  Blocks processed: %d / %d" % (n_blocks, len(BLOCKS)))
    print("  Functions created: %d (expected 11: 2+1+3+5)" % n_fns)
    print("  DRY=%s" % DRY)


main()
