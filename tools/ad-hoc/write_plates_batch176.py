#!/usr/bin/env python3
"""Write plate files for batch #176 (20 functions)."""
import os

BASE = os.path.join(os.path.dirname(__file__), '..', '..', 'doc', 'dev', 'eval')

plates = {
    '0805ce70': (
        'check_equip_slot_eligible_with_lp_slot_flag: '
        'Equip slot activation eligibility predicate. r0=card_slot_ptr. '
        'Three sequential checks: '
        '(1) calls check_neo_daedalus_placement_eligible -- returns 0 on fail; '
        '(2) reads gP1LifePoints[player_id*0x868+0x11c] (halfword), AND 0x1 -- if nonzero returns 0 (LP slot flag already occupied); '
        '(3) reads gP1LifePoints[player_id*0x868+0x10] (word) -- if 0 returns 0 (LP slot not active). '
        'All checks passed: returns 1. '
        'Part of check_equip_slot_eligible_* sibling cluster; '
        'guards LP slot activation flag is not occupied and base LP slot is active.\n\n'
        'Constants:\n'
        '- LP_SLOT_FLAG_OFFSET = 0x11c  (0x8e<<1)\n'
        '- LP_SLOT_FLAG_MASK   = 0x1\n'
        '- LP_BASE_OFFSET      = 0x10\n'
        '- PLAYER_STRIDE       = 0x868'
    ),

    '0805cf70': (
        'check_equip_slot_eligible_without_reserved_field_card: '
        'Equip slot activation eligibility predicate. r0=card_slot_ptr, r1=player_id. '
        'Checks that reserved-field card (card_id=0x12fb, no released card) is not on the field: '
        'calls count_field_copies_of_card(0x12fb); if count > 0 returns 0 (reserved card present). '
        'If card not on field, calls dispatch_effect_for_neo_daedalus_eligible_slot(r0, r1) '
        'and passes through its return value (1=allow, 0=deny). '
        'Part of check_equip_slot_eligible_* sibling cluster; '
        'guard condition: reserved card absent before dispatching neo_daedalus effect slot check.\n\n'
        'Constants:\n'
        '- RESERVED_CARD_ID = 0x12fb  (no released card name, reserved icid)'
    ),

    '0805d918': (
        'check_equip_slot_eligible_with_field_state_and_chain: '
        'Equip slot activation eligibility predicate. r0=card_slot_ptr, r1=u32 (must be 0, else immediate fail). '
        'Five sequential checks: '
        '(1) r1 != 0 returns 0; '
        '(2) gP1LifePoints[player_id*0x868+0x1ce8] word must equal card_slot_ptr player_id (field state pairing check); '
        '(3) gP1LifePoints[player_id*0x868+0x10d0] word bit0 must be 0 (global state flag clear); '
        '(4) calls check_neo_daedalus_placement_eligible(slot_ptr, 0); '
        '(5) gP1LifePoints[player_id*0x868+0x11c] byte[+3] bit0 must be 1 (LP slot byte flag); '
        '(6) calls check_value_in_slot_chain(player_id, card_id, 0xb). '
        'All passed returns 1. Part of check_equip_slot_eligible_* sibling cluster.\n\n'
        'Constants:\n'
        '- FIELD_STATE_OFFSET    = 0x1ce8\n'
        '- GLOBAL_FLAG_OFFSET    = 0x10d0\n'
        '- GLOBAL_FLAG_BIT_MASK  = 0x1\n'
        '- LP_SLOT_BYTE3_OFFSET  = 0x11c  (0x8e<<1)\n'
        '- LP_SLOT_BIT_MASK      = 0x1\n'
        '- PLAYER_STRIDE         = 0x868\n'
        '- CHAIN_TYPE_B          = 0xb'
    ),

    '0805da74': (
        'check_equip_slot_eligible_field6_max5: '
        'Equip slot activation eligibility predicate. r0=card_slot_ptr, no additional APCS params. '
        'Extracts player_id (byte[+2] bit0) and zone_idx (halfword[+4] bits[10:4] via lsls#0x11/lsrs#0x17 -> [0..63]). '
        'Calls dispatch_equip_slot_scan_with_field6_guard(player_id, zone_idx, 0, 5, 0) with max_count=5, stack_arg=0, mode=0; '
        'returns 1 if nonzero result, else 0. '
        'Part of check_equip_slot_eligible_* sibling cluster; '
        'qualifier indicates max scan slot count is 5.\n\n'
        'Constants:\n'
        '- MAX_SCAN_COUNT = 5\n'
        '- SCAN_STACK_ARG = 0\n'
        '- SCAN_MODE      = 0\n'
        '- PLAYER_STRIDE  = (implicit in callee)'
    ),

    '0805daa4': (
        'check_equip_slot_eligible_without_light_of_intervention_max2: '
        'Equip slot activation eligibility predicate. r0=card_slot_ptr. '
        'Two checks: '
        '(1) calls count_field_copies_of_card(0x135d=Light of Intervention, passcode=62867251) -- if present returns 0; '
        '(2) if Light of Intervention absent, extracts player_id and zone_idx, '
        'calls dispatch_equip_slot_scan_with_field6_guard with max_count=2, stack_arg=0, mode=0; '
        'returns 1 if nonzero, else 0. '
        'Light of Intervention on field prohibits special summon; '
        'this predicate guards absence then executes scan (max 2 slots).\n\n'
        'Constants:\n'
        '- LIGHT_OF_INTERVENTION_ID = 0x135d  (Light of Intervention, passcode=62867251)\n'
        '- MAX_SCAN_COUNT            = 2\n'
        '- SCAN_STACK_ARG            = 0\n'
        '- SCAN_MODE                 = 0'
    ),

    '0805dae4': (
        'invoke_effect_node_handler_with_zone_flag_guard: '
        'Effect node handler dispatch function (indeg=6 hub). r0=effect_node_ptr, r1=player_side_byte, r2=slot_type_byte. '
        'Flow: '
        '(1) r0=0 returns 0 immediately; '
        '(2) extracts player_id_bit (r7 bit0), computes zone_entry = zone_base + slot_type*0x14*... + player_id*0x868 + 0x0201c510, '
        'checks zone_word bit12 (lsls#0x13 -> bit31 == original bit12) -- if bit is 0 returns 0; '
        '(3) packs (r7 bit0, r2) combined byte, calls read_effect_slot_side_and_type -- if result matches packed value returns 0 '
        '(side/type already matched, no re-dispatch needed); '
        '(4) writes [gDuelEffectBase+0x4c0] = player_id_bit (set current active side flag); '
        '(5) calls invoke_effect_node_handler_3arg(effect_node, r7, r5); '
        '(6) writes [gDuelEffectBase+0x4c0] = 0 (clear active side flag). '
        'Returns invoke_effect_node_handler_3arg return value (0/nonzero).\n\n'
        'Constants:\n'
        '- ZONE_BASE        = 0x0201c510\n'
        '- PLAYER_STRIDE    = 0x868\n'
        '- ZONE_SLOT_STRIDE = 0x14  (slot_type*20)\n'
        '- ZONE_EFFECT_BIT  = bit12  (lsls#0x13 -> bit31 == original bit12)\n'
        '- EFFECT_SIDE_FLAG = 0x0201b290+0x4c0 = 0x0201b750'
    ),

    '0805e3a8': (
        'check_equip_slot_eligible_with_pool_and_hand_slot: '
        'Equip slot activation eligibility predicate (indeg=1). r0=card_slot_ptr, r1=player_id. '
        'Three sequential checks: '
        '(1) extracts zone_idx (halfword[+4] bits[10:4]) and card_id (halfword[+0]), '
        'calls check_zone_card_id_in_node_pool(zone_idx, card_id) -- if nonzero (already in pool) returns 0; '
        '(2) calls check_neo_daedalus_placement_eligible(slot_ptr, player_id) -- if 0 returns 0; '
        '(3) extracts player_id (bit0) and set_code (bits[10:4]), '
        'calls find_hand_slot_idx_by_set_code(player_id, set_code) -- if < 0 returns 0 (no matching combo card in hand). '
        'All passed returns 1.\n\n'
        'Constants:\n'
        '- ZONE_IDX_MASK = bits[10:4]  (lsls#0x11 / lsrs#0x17 -> [0..63])'
    ),

    '0805e518': (
        'check_equip_slot_eligible_type580_or_neo_daedalus_hand: '
        'Equip slot activation eligibility predicate. r0=card_slot_ptr. '
        'Two-path conditional return: '
        '(1) if halfword[+2] bits[11:6] (type_field) == 0x580 (0xb0<<3), returns 1 immediately (no further check); '
        '(2) if type_field == 0x80, calls check_neo_daedalus_placement_eligible then find_hand_slot_idx_by_set_code(player_id, set_code); '
        'if hand_slot >= 0 returns 1, else 0; '
        '(3) other type values return 0. '
        'Part of check_equip_slot_eligible_* sibling cluster; '
        'covers type=0x580 fast-pass path and type=0x80 neo_daedalus + hand check path.\n\n'
        'Constants:\n'
        '- TYPE_FIELD_MASK = 0xfc0       (0xfc<<4)\n'
        '- TYPE_580        = 0x580       (0xb0<<3; python: hex(0xb0<<3)=0x580)\n'
        '- TYPE_80         = 0x80'
    ),

    '0805e578': (
        'check_equip_slot_eligible_with_zone_success_count: '
        'Equip slot activation eligibility predicate (complex zone traversal). r0=card_slot_ptr. '
        'Saves/restores caller high registers r8/r9/r10 (prologue .hword 0x4645/0x464e/0x4657; epilogue 0x4698/0x46a1/0x46aa). '
        'Flow: '
        '(1) calls check_neo_daedalus_placement_eligible -- returns 0 on fail; '
        '(2) computes player monster zone count upper bound (gP1LifePoints[player*0x868+0xc]); '
        'if r9 (fail_count) >= bound jumps to result check; '
        '(3) iterates all monster zone slots: compares set_code bits[11:6] against slot_ptr set_code; '
        'on match calls check_card_field5_is_nonzero; if pass calls eval_equip_placement_full_check; '
        'if eval nonzero: sp[0] (success_count) +1; if eval 0: r9 (fail_count) +1; '
        '(4) after loop: sp[0]>0 AND r9<=1 returns 1, else 0. '
        'success_count > 0 AND fail count <= 1 means at least one placeable slot with acceptable failures.\n\n'
        'Constants:\n'
        '- ZONE_COUNT_OFFSET  = 0xc      (gP1LP[player*0x868]+0xc, from DAT_0805e67c=0x0201c4ec = gP1LP+0xc)\n'
        '- MONSTER_ZONE_BASE  = 0x120    (0x90<<1)\n'
        '- PLAYER_STRIDE      = 0x868\n'
        '- ZONE_IDX_STRIDE    = 0x14     (zone_idx*20 bytes)'
    ),

    '0805e6f4': (
        'check_equip_slot_eligible_without_banisher_mode1: '
        'Equip slot activation eligibility predicate. r0=card_slot_ptr. '
        'Two checks: '
        '(1) calls count_field_copies_of_card(0x1332=Banisher of the Light, passcode=61528025) -- if present returns 0; '
        '(2) if Banisher of the Light absent, extracts player_id and zone_idx, '
        'calls dispatch_equip_slot_scan_with_field6_guard with max_count=1, stack_arg=0, mode=1; '
        'returns 1 if nonzero, else 0. '
        'Banisher of the Light on field removes non-Spellcaster monsters from play; '
        'this predicate guards absence then performs mode=1 single-slot scan.\n\n'
        'Constants:\n'
        '- BANISHER_OF_LIGHT_ID = 0x1332  (Banisher of the Light, passcode=61528025)\n'
        '- MAX_SCAN_COUNT       = 1\n'
        '- SCAN_STACK_ARG       = 0\n'
        '- SCAN_MODE            = 1'
    ),

    '0805ea3c': (
        'check_equip_slot_eligible_with_type_e_zone_and_toon: '
        'Equip slot activation eligibility predicate (multi-compound conditions). r0=card_slot_ptr, r1=player_id. '
        'Uses high register save frame (prologue .hword 0x4647/0x4688). '
        'Six sequential checks: '
        '(1) extracts player_id and zone_type_id=0x1415, calls get_node_entity_id_in_slot(player_id, 0x1415, 0xb); '
        '(2) check_neo_daedalus_placement_eligible; '
        '(3) entity_id >= 0; '
        '(4) find_zone_descriptor_by_slot_id parses zone_descriptor, extracts zone_type(byte[0]), player(byte[1]), zone_idx; '
        '(5) zone_type must == 0xe; '
        '(6) check_card_field5_is_nonzero and check_card_has_equip_placement_type both pass; '
        'final condition: if check_card_stat_field8_is_6 succeeds, skip check_toon_world_equip_present, '
        'else check_toon_world_equip_present must pass. '
        'All conditions met returns 1.\n\n'
        'Constants:\n'
        '- ZONE_TYPE_E      = 0xe\n'
        '- ENTITY_TYPE_1415 = 0x1415\n'
        '- SLOT_TYPE_B      = 0xb'
    ),

    '0805ebc4': (
        'check_equip_slot_eligible_max1_or_byte3_flag: '
        'Equip slot activation eligibility predicate (three-value return, indeg=1). r0=card_slot_ptr. '
        'Extracts player_id and zone_idx, calls dispatch_equip_slot_scan_with_field6_guard with max_count=1, stack_arg=1, mode=0: '
        'if nonzero returns 2 (high-priority success). '
        'If scan returns 0, reads slot[+3] bits[5:4] (mask 0x30): '
        'if both bits clear (0x30 AND result==0) returns 1 (secondary success); '
        'else (bits[5:4] nonzero) returns 0 (fail). '
        'Three-value result: 2=scan success, 1=byte3 flags clear, 0=fail. '
        'Caller 0x08057470 uses r0==2 as trigger threshold.\n\n'
        'Constants:\n'
        '- MAX_SCAN_COUNT  = 1\n'
        '- SCAN_STACK_ARG  = 1\n'
        '- SCAN_MODE       = 0\n'
        '- BYTE3_FLAG_MASK = 0x30  (bits[5:4])'
    ),

    '0805f5e8': (
        'check_effect_node_zone_activation_dual_state: '
        'Effect node zone activation state query. r0=effect_node_ptr. '
        'Executes two count_effect_node_zone_activations passes: '
        '(1) writes slot[+0xa]=1 (halfword, activate temp flag); '
        'calls count_effect_node_zone_activations -- if 0 returns 0 (fail); '
        '(2) if first count nonzero, writes slot[+0xa]=0 (clear temp flag); '
        'calls count_effect_node_zone_activations again -- if 0 returns 0 (fail); '
        '(3) if second count also nonzero, returns 2. '
        'Result: 2=dual activation confirmed, 0=either phase failed. '
        'Verifies effect node has zone activations under both flag=1 and flag=0 states.\n\n'
        'Constants:\n'
        '- FLAG_HALFWORD_OFFSET = 0xa  (effect_node temp activation flag field offset; strh r0,[r4,#0xa])\n'
        '- ACTIVATION_SUCCESS   = 2    (return value when both counts nonzero)'
    ),

    '0805f968': (
        'check_equip_slot_eligible_type80_neo_daedalus_hand: '
        'Equip slot activation eligibility predicate (type=0x80 dedicated path). r0=card_slot_ptr. '
        'Three sequential checks: '
        '(1) halfword[+2] bits[11:6] (type_field via mask 0xfc0) must equal 0x80, else returns 0; '
        '(2) calls check_neo_daedalus_placement_eligible -- returns 0 on fail; '
        '(3) extracts player_id (bit0) and set_code (halfword[+4] bits[10:4]), '
        'calls find_hand_slot_idx_by_set_code -- if < 0 returns 0. '
        'All passed returns 1. '
        'Differs from check_equip_slot_eligible_type580_or_neo_daedalus_hand (0x0805e518): '
        'this function handles only type=0x80 single path, no type=0x580 fast-pass branch.\n\n'
        'Constants:\n'
        '- TYPE_FIELD_MASK = 0xfc0  (0xfc<<4)\n'
        '- TYPE_80         = 0x80'
    ),

    '0805f9e4': (
        'check_equip_slot_eligible_with_monster_count_gate: '
        'Equip slot activation eligibility predicate (monster count gate wrapper). r0=card_slot_ptr, r1=player_id. '
        'First checks target zone monster count: '
        'computes zone_base = gDuelFieldSlots[player_id*0x868 + zone_idx*0x14], reads zone[+0xc] (monster count word); '
        'if zone[+0xc] <= 1 returns 0 (insufficient monsters). '
        'If monster count > 1, calls check_equip_slot_eligible_neo_daedalus_full_guard(slot_ptr, player_id) '
        'and passes through its return value. '
        'Part of check_equip_slot_eligible_* sibling cluster; monster count > 1 is precondition.\n\n'
        'Constants:\n'
        '- MONSTER_COUNT_OFFSET = 0xc\n'
        '- MONSTER_COUNT_MIN    = 2  (must be > 1)\n'
        '- ZONE_SLOT_STRIDE     = 0x14  (20 bytes)\n'
        '- PLAYER_STRIDE        = 0x868\n'
        '- ZONE_BASE            = 0x0201c510'
    ),

    '0805fa84': (
        'check_equip_slot_eligible_with_spell_zone_and_effect_handlers: '
        'Equip slot activation eligibility predicate (spell zone + effect handler chain). r0=card_slot_ptr, r1=player_id. '
        'Four sequential checks: '
        '(1) extracts player_id, calls check_spell_zone_slot_placeable(player_id) -- if 0 returns 0; '
        '(2) calls dispatch_effect_handler_by_card_id(player_id, card_id, mode=0) -- if 0 returns 0; '
        '(3) calls dispatch_effect_handler_by_card_id(player_id, card_id, mode=1) -- if 0 returns 0; '
        '(4) calls check_neo_daedalus_placement_eligible(slot_ptr, player_id) -- passes through return value (1=allow, 0=deny). '
        'Guards that spell zone has open slot and both handlers pass before activation.'
    ),

    '0805fb3c': (
        'check_equip_slot_eligible_with_empty_monster_zones_and_handlers: '
        'Equip slot activation eligibility predicate (no monster zone + effect handler loop). r0=card_slot_ptr, r1=player_id. '
        'Five sequential checks: '
        '(1) check_neo_daedalus_placement_eligible -- returns 0 on fail; '
        '(2) count_occupied_monster_zones(player_id) -- if nonzero (monsters present) returns 0; '
        '(3) check_equip_slot_chain_absent(slot_ptr, player_id) -- if chain nonempty returns 0; '
        '(4) reads gP1LifePoints[player_id*0x868+0xc] for zone_count upper bound, '
        'loops zone_idx=[0..zone_count-1]: calls dispatch_effect_handler_by_card_id(player_id, card_id, zone_idx) -- '
        'if any returns nonzero immediately returns 1; '
        '(5) all zones exhausted with no match returns 0.\n\n'
        'Constants:\n'
        '- ZONE_COUNT_OFFSET = 0xc  (gP1LP[player*0x868]+0xc)\n'
        '- PLAYER_STRIDE     = 0x868'
    ),

    '0805feb0': (
        'check_equip_slot_eligible_type180_or_1c0_cross_player_handlers: '
        'Equip slot activation eligibility predicate (type 0x180/0x1c0 + cross-player handler loop). r0=card_slot_ptr, r1=player_id. '
        'Flow: '
        '(1) type_field = halfword[+2] bits[11:6] (via mask 0xfc0); '
        'if type_field != 0x180 (0xc0<<1) and != 0x1c0 (0x180+0x40) returns 0; '
        '(2) reads slot[+0x14] bit9 (lsls#0x16/lsrs#0x1f -> bit9); '
        'if bit9 == player_id bit0 returns 0 (must be opponent slot); '
        '(3) check_neo_daedalus_placement_eligible -- returns 0 on fail; '
        '(4) reads gP1LifePoints[player_id*0x868+0xc] for zone_count, '
        'loops zone_idx=[0..zone_count-1]: calls dispatch_effect_handler_by_card_id(player_id, card_id, zone_idx) -- '
        'on match returns 1; '
        '(5) no match returns 0.\n\n'
        'Constants:\n'
        '- TYPE_FIELD_MASK = 0xfc0     (0xfc<<4)\n'
        '- TYPE_180        = 0x180     (0xc0<<1; python: hex(0xc0<<1)=0x180)\n'
        '- TYPE_1C0        = 0x1c0     (0x180+0x40)\n'
        '- SLOT_BIT9       = bit9      (slot[+0x14] lsls#0x16/lsrs#0x1f)\n'
        '- ZONE_COUNT_OFF  = 0xc\n'
        '- PLAYER_STRIDE   = 0x868'
    ),

    '0805ff64': (
        'check_equip_slot_eligible_with_lp_active_and_neo_daedalus: '
        'Equip slot activation eligibility predicate (LP active state + neo_daedalus). r0=card_slot_ptr, r1=player_id. '
        'Two checks: '
        '(1) reads gP1LifePoints[player_id*0x868+0x10] (word, LP activation count); '
        'if 0 returns 0 (LP slot not active); '
        '(2) if nonzero, calls check_neo_daedalus_placement_eligible(slot_ptr, player_id) and passes through return value (1=allow, 0=deny). '
        'Differs from check_equip_slot_eligible_with_lp_slot_flag (0x0805ce70): '
        'this function checks [+0x10] LP activation count (nonzero=active), '
        'that function checks [+0x11c] bit0 flag (zero=available).\n\n'
        'Constants:\n'
        '- LP_ACTIVE_OFFSET = 0x10\n'
        '- PLAYER_STRIDE    = 0x868'
    ),

    '0806001c': (
        'check_equip_slot_eligible_type_b0_with_bit17_and_not_bit14: '
        'Equip slot activation eligibility predicate (zone_type_b0 base + word[+0x14] dual-bit gate). r0=card_slot_ptr. '
        'Two checks: '
        '(1) calls check_equip_slot_eligible_by_zone_type_b0_with_field5 -- if 0 returns 0; '
        '(2) reads slot[+0x14] (word), checks bit17 and bit14: '
        'if bit17=0 (lsls#0xe -> result >= 0) returns 0; '
        'if bit14=1 (lsls#0x11 -> result < 0) returns 0. '
        'Requires bit17=1 AND bit14=0. Both checks passed returns 1. '
        'Part of check_equip_slot_eligible_* sibling cluster; '
        'adds word[+0x14] bit combination check on top of zone_type_b0 base predicate.\n\n'
        'Constants:\n'
        '- BIT17_CHECK = slot[+0x14] bit17 -- lsls#0xe -> bge fail (requires bit17=1)\n'
        '- BIT14_CHECK = slot[+0x14] bit14 -- lsls#0x11 -> blt fail (requires bit14=0)'
    ),
}

all_ok = True
for addr, text in plates.items():
    bad = [c for c in text if ord(c) > 0x7f]
    if bad:
        print(f'NON-ASCII in {addr}: {set(bad)}')
        all_ok = False
    else:
        print(f'OK {addr}')

if all_ok:
    print('All plates ASCII-clean')
    for addr, text in plates.items():
        path = os.path.join(BASE, f'{addr}.plate.txt')
        with open(path, 'w', encoding='ascii') as f:
            f.write(text + '\n')
    print(f'Written {len(plates)} plate files to {BASE}')
else:
    print('ABORT: non-ASCII found')
    import sys
    sys.exit(1)
