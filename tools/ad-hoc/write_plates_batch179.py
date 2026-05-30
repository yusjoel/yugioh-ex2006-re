import os

outdir = r'E:\Workspace\yugioh-ex2006-re\doc\dev\eval'

plates = {}

plates['08063a6c'] = (
    "Check whether target equip slot satisfies neo-daedalus special placement conditions during equip activation. "
    "Extracts player_id(bit0) and zone_idx(bits[6:2]) from slot[+2], passes flag=1 to dispatch_equip_slot_scan_with_field6_guard for field6 guard scan; "
    "if scan passes, calls check_equip_slot_chain_absent to confirm no chain node occupying the slot; "
    "if both pass, calls dispatch_effect_for_neo_daedalus_eligible_slot to trigger neo-daedalus effect. Returns 0 on any failure.\n\n"
    "Constants:\n"
    "- EQUIP_FLAG = 1 (scan_flag, r1 to dispatch_equip_slot_scan_with_field6_guard)\n"
    "- ZONE_IDX_SHIFT = 2 (bits[6:2] from slot[+2])"
)

plates['08063c14'] = (
    "Verifies that opponent LP exceeds threshold before triggering neo-daedalus effect during equip activation. "
    "Extracts player_id from slot[+2].bit0, computes opponent=1^player_id, reads LP-related value at gP1LifePoints+opponent*0x868+0x10; "
    "if value > 1 calls dispatch_effect_for_neo_daedalus_eligible_slot; else returns 0. "
    "Used to ensure neo-daedalus effect triggers only when opponent LP is sufficient.\n\n"
    "Constants:\n"
    "- gP1LifePoints = 0x0201c4e0 (player LP struct base)\n"
    "- player_stride = 0x868 (per-player offset)\n"
    "- LP_CHECK_OFFSET = 0x10 (offset within player LP struct)\n"
    "- LP_THRESHOLD = 1 (value must be > 1 to proceed)"
)

plates['08063e80'] = (
    "Thin wrapper over check_neo_daedalus_placement_eligible, mapping bool return to {2, 0}. "
    "Used by callers that distinguish between eligible (2) and ineligible (0), carrying more semantic information than a plain bool. "
    "No parameter setup needed; r0 is passed directly to callee.\n\n"
    "Constants:\n"
    "- RETURN_ELIGIBLE = 2 (return value when eligible)\n"
    "- RETURN_FAIL = 0 (return value when ineligible)"
)

plates['08063e94'] = (
    "Dual-path equip eligibility check that distinguishes target card type flags, verifying Ultimate Offering chain state "
    "and neo-daedalus placement conditions separately. If slot[+3] bits[5:4] (mask 0x30) == 0 (normal card): reads LP bit17 "
    "at gP1LifePoints+opponent*0x868+0x8e<<1; if bit17==1 fails; then calls check_value_in_slot_chain(player, zone, icid=0x12f3/Ultimate Offering) "
    "to confirm no chain node with Ultimate Offering; if passes returns 1. "
    "If bits[5:4] != 0 (special card type): extracts player_id and zone_idx, calls check_value_in_slot_chain + LP activation flag check + check_neo_daedalus_placement_eligible.\n\n"
    "Constants:\n"
    "- CARD_TYPE_MASK = 0x30 (slot[+3] bits[5:4], type flags)\n"
    "- gP1LifePoints = 0x0201c4e0\n"
    "- player_stride = 0x868\n"
    "- LP_CHECK_OFFSET = 0x8e<<1 = 0x11c (offset within player LP block)\n"
    "- LP_BIT17 = bit17 (lsrs r0,r0,#0x11; ands r0,r3 where r3=1)\n"
    "- ICID_ULTIMATE_OFFERING = 0x12f3 (Ultimate Offering)"
)

plates['08063f28'] = (
    "Guards neo-daedalus effect dispatch with LP area bit0 flag during equip activation. "
    "Reads LP halfword at gP1LifePoints+player*0x868+0x8e<<1, checks bit0; "
    "if bit0==1 (specific LP state active) returns 0; "
    "if bit0==0 calls dispatch_effect_for_neo_daedalus_eligible_slot. "
    "Scenario: equip activation where LP area specific flag is not yet set, allowing neo-daedalus effect to trigger.\n\n"
    "Constants:\n"
    "- gP1LifePoints = 0x0201c4e0\n"
    "- player_stride = 0x868\n"
    "- LP_OFFSET = 0x8e<<1 = 0x11c\n"
    "- LP_BIT0_FLAG = 1 (AND mask, bit0 of halfword at offset)"
)

plates['08064074'] = (
    "Comprehensive equip eligibility check that chains chain-count verification, neo-daedalus placement eligibility, "
    "card pair ID resolution, field8 attribute, and field5 score checks before triggering effect. "
    "First calls count_slots_with_chain_field_match to confirm opponent field=1 chain slot exists; "
    "then check_neo_daedalus_placement_eligible; traverses gDuelFieldState+0x4cc/0x4d4 to confirm exactly 1 slot with code=8; "
    "checks zone_type=0x80<<2=0x200 slot flag; calls resolve_slot_card_id_for_pair to get paired card_id; "
    "checks field8 != 9; gets field5 score <= 0x5dc; "
    "if all pass writes slot[+0xa]:=r3 (pair_index) then calls lookup+dispatch_effect_handler_by_card_id.\n\n"
    "Constants:\n"
    "- gDuelFieldState = 0x0201b290\n"
    "- STATE_CHAIN_COUNT_OFFSET = 0x4cc (chain active count area)\n"
    "- STATE_CHAIN_BASE_OFFSET = 0x4d4\n"
    "- gDuelFieldSlots = 0x0201c510\n"
    "- player_stride = 0x868\n"
    "- CHAIN_CODE_TARGET = 8 (slot code to count)\n"
    "- ZONE_TYPE_MASK = 0xfc<<4 = 0xfc0\n"
    "- ZONE_TYPE_TARGET = 0x80<<2 = 0x200\n"
    "- SCORE_MAX = 0x5dc (1500)"
)

plates['08064204'] = (
    "Checks whether equip slot satisfies Sacred Beast pair neo-daedalus placement conditions. "
    "Calls in sequence: (1) check_equip_slot_eligible_by_tier_and_banisher_scan for basic tier and banisher conditions; "
    "(2) check_field_spell_neo_daedalus_group_placeable to confirm placeable; "
    "(3) count_available_monster_slots > 2; "
    "(4) count_paired_slots_with_field5_default(player, icid=0x19a3/Uria) OR "
    "count_paired_slots_with_field5_default(player, icid=0x19a4/Hamon) > 0. "
    "All conditions met returns 1, else 0. "
    "Scenario is equip activation for Sacred Beast Uria (Uria, Lord of Searing Flames) or Hamon (Hamon, Lord of Striking Thunder).\n\n"
    "Constants:\n"
    "- ICID_URIA = 0x19a3 (Uria, Lord of Searing Flames; cid=2012)\n"
    "- ICID_HAMON = 0x19a4 (Hamon, Lord of Striking Thunder; cid=2013)\n"
    "- MIN_MONSTER_SLOTS = 2 (count_available_monster_slots must be > 2)"
)

plates['080643e0'] = (
    "Checks whether equip slot satisfies neo-daedalus placement eligibility under the condition that no equip slot is currently active. "
    "First calls count_equip_slots_active_only(player); if any active equip slot exists returns 0; "
    "then calls count_paired_slots_with_field5_default(player, card_id); if paired slot exists returns 0; "
    "finally calls check_neo_daedalus_placement_eligible. "
    "Scenario: equip activation requires no other equip in active state on field for this neo-daedalus effect to be allowed.\n\n"
    "Constants:\n"
    "- (no additional literals; all thresholds determined by callee internals)"
)

plates['08064418'] = (
    "Three-way zone_type dispatcher that routes to different equip eligibility predicates based on slot[+2].bits[11:6] (zone_type). "
    "zone_type=6: returns 1 unconditionally eligible. "
    "zone_type=0xf: locates slot in gDuelFieldSlots, reads [+0xc] chain flag, checks bit1 (AND mask=2) nonzero "
    "then calls check_equip_slot_eligible_bls_envoy_absent_with_zone_field_match. "
    "zone_type=0x16: locates slot, checks chain flag bit2 (AND mask=4) nonzero "
    "then calls check_equip_slot_eligible_field_spell_effect_type_e_with_zone_field5. "
    "Other zone_type: returns 0.\n\n"
    "Constants:\n"
    "- ZONE_TYPE_ALWAYS_ELIGIBLE = 6 (unconditional eligible)\n"
    "- ZONE_TYPE_BLS_ENVOY = 0xf (15; chain flag bit1 required)\n"
    "- ZONE_TYPE_FIELD_SPELL_E = 0x16 (22, zone type for field-spell effect E path; chain flag bit2 required)\n"
    "- player_stride = 0x868\n"
    "- gDuelFieldSlots = 0x0201c510\n"
    "- CHAIN_FLAG_BIT1 = 0x2 (mask for zone_type=0xf path)\n"
    "- CHAIN_FLAG_BIT2 = 0x4 (mask for zone_type=0x16 path)\n"
    "- ZONE_TYPE_FIELD = slot[+2].bits[11:6] = lsls #0x14 / lsrs #0x1a"
)

plates['0806460c'] = (
    "Three-step equip eligibility verification: first calls check_effect_slot_matches_zone_entry to confirm effect slot matches zone entry; "
    "then decodes zone_player_id and zone_idx from output and calls invoke_effect_node_with_active_flag_3arg to trigger effect node; "
    "if effect node activates successfully, finally calls check_equip_slot_eligible_in_target_bitmap to verify slot eligibility in equip target bitmap. "
    "Any step failing returns 0. Called by multiple equip zone handlers (indeg=10).\n\n"
    "Constants:\n"
    "- ZONE_PLAYER_SHIFT = 0x18 (lsls #0x18; extracts bits[7:0] of zone entry output = zone_player_id)\n"
    "- ZONE_IDX_SHIFT = 0x10 (lsls #0x10; combined with lsrs #0x18 extracts bits[15:8] = zone_idx)"
)

plates['080655ec'] = (
    "Equip activation LP effect submission function. "
    "First calls dispatch_equip_lp_delta_by_card_id to dispatch LP delta; "
    "then calls increment_lp_bar_display_counter to increment display counter. "
    "Based on slot[+2].bit0 player_id, performs two sentinel checks for each direction "
    "(>= 0 = positive; <= 0 = negative/zero), "
    "calling submit_lp_indicator_with_slot_xor_flag or submit_effect_zone_lp_and_shape_sprites respectively. "
    "Finally calls decrement_lp_bar_display_counter to restore counter. "
    "Called by 11 equip zone handlers (indeg=11).\n\n"
    "Constants:\n"
    "- PLAYER_BIT_MASK = bit0 of slot[+2] (lsls/lsrs #0x1f)"
)

plates['08066530'] = (
    "Determines whether to enqueue a graveyard spell sprite based on equip slot zone flags. "
    "Reads slot[+6].bits[4:2] (3-bit zone flag); if all zero returns 0 directly. "
    "Otherwise extracts bits[4:2]-1 as zone_type_index, reads slot[+2].bit0 as player_id, "
    "calls read_effect_slot_zone_type(slot, zone_type_index-1) to get zone_type. "
    "Then calls find_hand_slot_idx_by_set_code(zone_type, player_id) to find hand slot index; "
    "if found (>= 0), computes gDuelFieldSlots player offset and calls enqueue_graveyard_spell_sprite_with_zone_ref. "
    "Finally clears slot[+6] zone bits and sets bit7=1, returns 0x80.\n\n"
    "Constants:\n"
    "- ZONE_FLAG_MASK = 0x1c (bits[4:2] of slot[+6])\n"
    "- player_stride = 0x868\n"
    "- gDuelFieldSlots = 0x0201c8f8 (hand slot array base)\n"
    "- RETURN_ZONE_CLEARED = 0x80 (zone bits cleared flag)"
)

plates['080665d4'] = (
    "Zone state machine dispatch for equip slots containing specific reserved icid values. "
    "Reads slot[+0] halfword = card_id; "
    "if matches icid=0x162c or icid=0x184c (both reserved/unreleased cards, cid=0xFFFF) sets r1=3; "
    "if matches icid=0x1051 (also reserved, cid=0xFFFF) sets r1=5; else r1=0. "
    "Then reads current zone state at gDuelFieldState+0x4a0: "
    "state 0x80 -> calls trigger_card_display_op31_if_not_active with player_id and op_code=0xf5, returns 0x7f; "
    "state 0x7f -> calls init_effect_slot_display_context with r1 (clamped <=0x20)+6 and card_id, returns 0x7e; "
    "state 0x7e -> calls enqueue_effect_slot_sprites_descending; default -> returns 0.\n\n"
    "Constants:\n"
    "- ICID_RESERVED_A = 0x162c (cid=0xFFFF, reserved; r1 selector=3)\n"
    "- ICID_RESERVED_B = 0x184c (cid=0xFFFF, reserved; same as 0x162c branch; r1=3)\n"
    "- ICID_RESERVED_C = 0x1051 (cid=0xFFFF, reserved; r1=5)\n"
    "- gDuelFieldState = 0x0201b290\n"
    "- EQUIP_STATE_OFFSET = 0x4a0 (= 0x94<<3)\n"
    "- OP_CODE = 0xf5 (trigger_card_display_op31 arg)\n"
    "- gP1LifePoints = 0x0201c4e0 (player_stride=0x868)\n"
    "- DISPLAY_CTX_ARG_CAP = 0x20 (clamp upper bound for r1 passed to init_effect_slot_display_context)\n"
    "- gDisplayState = 0x0201e2a0"
)

plates['080666f4'] = (
    "Iterates over both players (player_id=0,1) to check equip zone state and update sprites. "
    "Entry: r0=slot_ptr saved to r7; r8=gP1LifePoints base; r9=gDuelFieldSlots. "
    "Outer loop r6=0..1 (player_id). Each iteration: reads gDuelFieldState[0x1ce8 + r6*0x38 + 0x2c] (activity flag); "
    "if nonzero calls render_zone_sprite_with_effect_dispatch_by_slot(slot_ptr, player_id, 0). "
    "If zero reads [+0x0] slot entry and [+0x4] zone_idx, computes bitmap value from gDuelFieldSlots target slot vs expected; "
    "if equal calls update_equip_target_bitmap_zone15(slot_ptr, entry, zone_idx, 0).\n\n"
    "Constants:\n"
    "- gP1LifePoints_base = 0x0201c4e0 (via DWORD_08066730)\n"
    "- gDuelFieldState_zone15 = 0x0201bbbc (via DWORD_08066738)\n"
    "- gDuelFieldSlots_base = 0x0201c4e0 + 0x30 offset (r8+0x30)\n"
    "- STATE_ZONE_OFFSET = 0x1ce8 (sub-struct offset)\n"
    "- player_stride = 0x868\n"
    "- LOOP_COUNT = 2 (player 0 and 1)"
)

plates['08066bf0'] = (
    "Iterates over all 11 zone slots (idx=0..10) for both players (player_id=0,1) to invoke effect nodes and dispatch sprite attributes. "
    "Entry: r0=slot_ptr saved to r6; r8=DWORD_08066c3c (0x0201e1c8, equip active zone count table base). "
    "Outer loop r0=0..1 (player_id); inner loop r5=0..10 (zone_idx). "
    "Each iteration: reads zone_player_id from [r8+player_id*0x38+zone_idx*8+0], XORs with player_id, "
    "then calls invoke_effect_node_with_active_flag_3arg(slot_ptr, zone_player_id, zone_idx). "
    "If returns nonzero calls dispatch_slot_sprite_attr_with_equip_head_flag(slot_ptr, zone_player_id, zone_idx, flag=1).\n\n"
    "Constants:\n"
    "- gEquipZoneCountTable = 0x0201e1c8 (via DWORD_08066c3c)\n"
    "- ZONE_COUNT = 11 (idx 0..10)\n"
    "- PLAYER_COUNT = 2 (player 0 and 1)\n"
    "- EQUIP_HEAD_FLAG = 1"
)

plates['08066d68'] = (
    "Searches player deck for Polymerization (icid=0x12e5) paired slot and enqueues graveyard spell sprite. "
    "Reads slot[+2].bit0=player_id; calls find_deck_slot_by_card_pair_match(player_id, card_id=0x12e5/Polymerization). "
    "If found (returns >= 0), computes gDuelFieldSlots hand slot address (player*0x868 + 0x0201c8f8 + found_idx*4), "
    "calls enqueue_graveyard_spell_sprite_with_zone_ref(slot_ptr, zone_ref). "
    "If not found skips. Returns 0 unconditionally.\n\n"
    "Constants:\n"
    "- ICID_POLYMERIZATION = 0x12e5 (Polymerization, cid=669)\n"
    "- player_stride = 0x868\n"
    "- gDuelFieldSlots_hand = 0x0201c8f8"
)

plates['08066dac'] = (
    "For both players (idx=0..1) checks equip zone entry match, triggers effect node, and updates equip target bitmap. "
    "Entry: r0=slot_ptr saved to r7; r8=0 (bitmap accumulator). "
    "Outer loop r6=0..1: calls check_effect_slot_matches_zone_entry(slot_ptr, idx, sp_out); if no match skips; "
    "decodes zone_player_id (bits[31:24]) and zone_idx (bits[23:16]) from sp output; "
    "calls invoke_effect_node_with_active_flag_3arg(slot_ptr, zone_player, zone_idx); if node inactive skips; "
    "sets bit(zone_player*4+zone_idx) into r8 (bitmap accumulator). "
    "After loop calls query_equip_target_bitmap_default(slot_ptr, r8) and returns 0.\n\n"
    "Constants:\n"
    "- PLAYER_COUNT = 2 (idx 0..1)\n"
    "- bitmap bit formula: 1 << (zone_player * 4 + zone_idx)"
)

plates['08066e0c'] = (
    "Dispatches equip OAM initialization based on current zone state at gDuelFieldState+0x4a0 with Cyber-Stein special handling. "
    "state=0x80: calls check_field_spell_neo_daedalus_group_placeable and count_available_monster_slots (both nonzero to continue); "
    "calls lookup_slot_display_value_by_card_id and dispatch_effect_handler_by_card_id; "
    "if handler returns nonzero calls trigger_card_display_op31_if_not_active(op=0x1a), returns 0x7f. "
    "state=0x7f: lookup_slot_display_value_by_card_id + init_effect_slot_display_context(player, 6, card_id, display_val), returns 0x7e. "
    "state=0x7e: if card_id=0x114a (Cyber-Stein, cid=361), calls get_monster_slot_entry_ptr + setup_equip_oam_entry_with_sprite_attr(sp[0]=0, mode=1); "
    "else get_monster_slot_entry_ptr + invoke_setup_equip_oam_with_attr2. default: returns 0.\n\n"
    "Constants:\n"
    "- gDuelFieldState = 0x0201b290\n"
    "- EQUIP_STATE_OFFSET = 0x4a0 (= 0x94<<3)\n"
    "- ICID_CYBER_STEIN = 0x114a (cid=361, Cyber-Stein; triggers special OAM setup)\n"
    "- OP_CODE_1A = 0x1a (trigger_card_display_op31 arg for state 0x80 path)"
)

plates['08066ee0'] = (
    "Single-frame state machine driver for equip activation display sequence. "
    "Reads current state value from gDuelFieldState+0x4a0 (= 0x94<<3) and subtracts 0x64 (100); "
    "if out of range [0..0x1c] (28 cases) jumps to default (state=0x65, returns 0). "
    "Dispatches via jump table (29 cases, states 0x64..0x80): "
    "case 0x80: if card_id=0x1919 (T.A.D.P.O.L.E., cid=1910) writes gDuelFieldState[+0x4a4]=9, else writes [+0x4a4]=2, returns 0x7f. "
    "case 0x7f: find_card_pair_in_player_deck_list + enqueue_hand_sprite_with_flip_flag_set; "
    "if enqueued reads [gDuelFieldState+0x4a4]-=1 and if >0 returns 0x7e, else trigger_card_display_op31(0x15) returns 0x6f. "
    "case 0x7e: dispatch_effect_handler_by_card_id; if <=0 returns 0x64, "
    "else checks activation flag=1 path writes [gP1LifePoints+player*4+0x1d40]=1 returns 0x7d; "
    "else format_text + invoke_card_display_op_0x31_sub1 returns 0x7d. "
    "case 0x7d: checks [gP1LifePoints+player*4+0xd40]; nonzero returns 0x7f, zero returns 0x64. "
    "case 0x6f: set_lp_row_type7_if_opponent_linked -> returns 0x64. "
    "case 0x64: enqueue_lp_counter_sprite_by_player.\n\n"
    "Constants:\n"
    "- gDuelFieldState = 0x0201b290\n"
    "- EQUIP_STATE_OFFSET = 0x4a0 (= 0x94<<3)\n"
    "- STATE_MIN = 0x64 (100; subtracted before table lookup)\n"
    "- STATE_COUNT = 0x1d (29 cases, 0x64..0x80)\n"
    "- ICID_TADPOLE = 0x1919 (T.A.D.P.O.L.E., cid=1910; case 0x80 card_id check)\n"
    "- ACTIVATION_COUNTER_OFFSET = 0x4a4 (gDuelFieldState + 0x4a4)\n"
    "- LP_FLAG_OFFSET = 0x1d40 (= 0xea<<5; gP1LifePoints + player*4 + 0x1d40)\n"
    "- gDuelFieldSlots_hand = 0x0201c740 (hand slot base)\n"
    "- gDisplayState = 0x0201e2a0"
)

plates['080672a4'] = (
    "Gate-controls equip OAM dispatch based on slot[+4].bit2, then dispatches by zone state. "
    "Reads slot[+4] byte, ANDs 0x4; if bit2 nonzero returns 0 immediately (already processed). "
    "Else reads gDuelFieldState+0x4a0: "
    "state=0x80 -> checks gP1LifePoints[player*0x868+0x18] (activity flag) nonzero "
    "then calls trigger_card_display_op31_if_not_active(player, op=0x1b), returns 0x7f. "
    "state=0x7f -> calls init_effect_slot_display_context(player, 6, card_id, 0), returns 0x7e. "
    "state=0x7e -> calls get_monster_slot_entry_ptr + render_pair_zone_sprites_if_field_card_present, returns 0. "
    "default -> returns 0.\n\n"
    "Constants:\n"
    "- BIT2_GATE = 0x4 (slot[+4] bit2; non-zero = early exit)\n"
    "- gDuelFieldState = 0x0201b290\n"
    "- EQUIP_STATE_OFFSET = 0x4a0 (= 0x94<<3)\n"
    "- gP1LifePoints = 0x0201c4e0\n"
    "- player_stride = 0x868\n"
    "- ACTIVITY_FLAG_OFFSET = 0x18 (gP1LifePoints + player*0x868 + 0x18)\n"
    "- OP_CODE_1B = 0x1b (trigger_card_display_op31 arg)"
)

all_ok = True
for addr, text in plates.items():
    bad = [(i, hex(ord(c)), c) for i, c in enumerate(text) if ord(c) > 127]
    if bad:
        print(f'NON-ASCII in {addr}: {bad[:5]}')
        all_ok = False
    else:
        fpath = os.path.join(outdir, f'{addr}.plate.txt')
        with open(fpath, 'w', encoding='ascii') as f:
            f.write(text)
        print(f'WROTE {fpath}')

if all_ok:
    print('ALL PLATES ASCII-CLEAN AND WRITTEN')
else:
    print('ERRORS FOUND - plates NOT written for failed entries')
