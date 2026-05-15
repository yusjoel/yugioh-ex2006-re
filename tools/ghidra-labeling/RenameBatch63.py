# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RenameBatch63.py  (2026-05-15)
# Renames + plate comments for batch #63 (21 functions).
# Workaround for Jython "module too large" limit on RenameKnownFunctions.py.

from ghidra.program.model.symbol import SourceType
from ghidra.program.model.listing import CodeUnit

RUN_DRY = False
try:
    _args = list(getScriptArgs())
    if _args and _args[0].lower() in ("dry", "--dry", "1", "true"):
        RUN_DRY = True
except Exception:
    pass


RENAMES = [
    ("FUN_0802f8d8", "find_equip_chain_node_by_type_d",
        "Searches equip chain list of a player slot for a node with type nibble==0xd; returns entity_id or 0xffff. "
        "r0=player_key (bit0=player_id [0..1]); r1=slot_index [0..4]. "
        "Slot offset: slot_stride=0x14, player_stride=0x868, base=gDuelFieldSlots=0x0201c510. "
        "Reads [slot+0xa] halfword as chain head; if 0 returns 0xffff. "
        "Loop: sub-table base DAT_0802f918=0x14b0, node stride 8 (lsls #3); "
        "reads [node+0x2] byte low 4 bits (& 0xf); if ==0xd returns [node+0x0] halfword (entity_id); "
        "else reads [node+0x6] halfword (next ptr), if 0 exits with 0xffff. "
        "4 callers: FUN_0804369c, FUN_0804888c, FUN_08050038, FUN_0805ca50 (all duel_field). "
        "Params: r0=u32 player_key (bit0=player_id [0..1]); r1=u32 slot_index [0..4]. "
        "Returns r0=u16 entity_id (found) / 0xffff (not found). "
        "Side effects: none (pure read, leaf loop)."),

    ("FUN_0804888c", "setup_equip_slot_sprite_attr_by_card",
        "Computes and enqueues OAM sprite attributes for a specified equip slot. "
        "r0=slot_ptr (gDuelFieldSlots slot entry ptr) -> r8; r1=player_key (bit0=player_id [0..1]) -> r9; "
        "r2=slot_index [0..4]. "
        "Calls find_equip_chain_node_by_type_d(player_key, slot_idx); if result==0 silently exits. "
        "Reads gDuelFieldSlots+slot data, packs OAM attr word (attr0 bits[14:0]=card_graphic_id, "
        "attr1 bits[21:17]=equip_state, attr2=priority etc); "
        "large switch on card_id (r6) adjusts sprite tile/flip/mode; "
        "calls enqueue_sprite_attr_record. "
        "Called exclusively by run_equip_slot_display_update_state_machine (0x08099aac). "
        "Params: r0=ptr slot_entry; r1=u32 player_key (bit0=player_id [0..1]); r2=u16 slot_index [0..4]. "
        "Returns r0=void. "
        "Side effects: OAM sprite attr buffer via enqueue_sprite_attr_record."),

    ("FUN_080495dc", "enqueue_slot_sprite_attr_by_player",
        "Enqueues OAM sprite attr record for a player slot. "
        "r0=player_side [0..1]; r1=attr_halfword. "
        "If r0==0: uses default tile_id 0x55; else loads DAT_080495f8=0x8055 (alt tile_id). "
        "Truncates r1 to 16 bits (lsls/lsrs #0x10). "
        "Calls enqueue_sprite_attr_record(tile_id, attr_halfword, mode=1, flags=0). "
        "Exit via pop {r0}; bx r0 (non-standard return -- r0 overwritten, void). "
        "Called by FUN_080495fc (indeg=2). "
        "Params: r0=u32 player_side [0..1] (0=P1 tile 0x55, 1=P2 tile 0x8055); "
        "r1=u16 attr_halfword (OAM sprite attr word, truncated to 16 bits). "
        "Returns r0=void (pop {r0}; bx r0). "
        "Side effects: OAM sprite attr buffer via enqueue_sprite_attr_record (1 record)."),

    ("FUN_080495fc", "enqueue_equip_zone_sprite_attr_full",
        "Assembles and enqueues full OAM sprite attrs for equip zone area. "
        "r0=player_key (bit0=player_id [0..1]); r1=count_limit; r2=base_attr (stored on stack). "
        "Extracts player_id=r6&1, computes player_stride=player_id*0x868. "
        "Reads [gP1LifePoints+player_stride+0x10]; if exceeds r9 upper bound, clips. "
        "Calls count_field_copies_of_card(card_id=0x1332 Banisher of the Light): "
        "if copy present, calls enqueue_slot_sprite_attr_by_player (simplified 0x55/0x8055 tile path); "
        "else enters full OAM attr assembly path (bit-field pack + card_id switch dispatch) + "
        "enqueue_sprite_attr_record + increment_lp_bar_display_counter. "
        "14 callers including FUN_0806abec, FUN_080750c0 (duel_field). "
        "Params: r0=u32 player_key (bit0=player_id [0..1]); r1=u32 count_limit; r2=u16 base_attr. "
        "Returns r0=void. "
        "Side effects: OAM sprite attr buffer via enqueue_sprite_attr_record or enqueue_slot_sprite_attr_by_player. "
        "Constants: CARD_ID=0x1332 (Banisher of the Light)."),

    ("FUN_08093384", "trigger_equip_activation_candidate_scan",
        "3-instruction wrapper: sets r1=0, calls eval_field_equip_activation_candidates(r0, 0), "
        "returns via pop {r0}; bx r0 (void). "
        "Triggers a mode=0 (full-field) equip activation candidate scan. "
        "3 callers: FUN_0803c708 (card_data+duel main ctrl), FUN_0803c8e0 (duel_field), "
        "FUN_08099314 (duel_field). "
        "Params: r0=u32 player_id [0..1] (forwarded to eval_field_equip_activation_candidates). "
        "Returns r0=void (pop {r0}; bx r0 overwrites r0). "
        "Side effects: via eval_field_equip_activation_candidates (equip activation queue update)."),

    ("FUN_08097360", "check_equip_slot_activation_blocked_by_chain_ext",
        "Extended equip slot activation chain-block check. "
        "r0=player_side [0..1] -> r4; r1=slot_index [0..4] -> r5. "
        "Step 1: eval_slot_activation_guard_full(player, slot, mode=0); if r0==0 returns 0 (blocked). "
        "Step 2: check_value_in_slot_chain(player, 0xb, 0x15ff Diffusion Wave-Motion). "
        "Step 3: check_value_in_slot_chain(player, 0xb, 0x14a6 Amazoness Archers). "
        "Step 4: check_value_in_slot_chain(player, 0xb, 0x1669 Staunch Defender). "
        "Step 5: test_slot_has_active_card(player, slot, 0x16bf Berserk Gorilla) + "
        "check_node_in_slot_chain(player, slot, 0x16cb BLS Envoy of the Beginning, 4). "
        "Step 6: check_value_in_slot_chain(1-player, 0xb, 0x177a Earthbound Spirit's Invitation) + "
        "query_zone_chain_count_with_eligibility(player, slot, 0x1561 Toon Defense) + "
        "query_zone_chain_count_with_eligibility(player, slot, 0x1852 Astral Barrier) + "
        "count_equip_slots_with_active_chain(1-player, 0x1318 Ring of Magnetism) + "
        "query_slot_effect_eligibility_nonzero(player, slot, mode=1). "
        "All pass: returns 1; any fail: returns 0. "
        "Called exclusively by dispatch_equip_slot_display_state_by_phase (0x08097c2c). "
        "Params: r0=u32 player_side [0..1]; r1=u32 slot_index [0..4]. "
        "Returns r0=u32 1=check passed, 0=activation blocked. "
        "Side effects: none (read-only). "
        "Constants: CARD_ID=0x1669 (Staunch Defender); CARD_ID=0x177a (Earthbound Spirit's Invitation); "
        "CARD_ID=0x1561 (Toon Defense); CARD_ID=0x1852 (Astral Barrier); CARD_ID=0x1318 (Ring of Magnetism)."),

    ("FUN_08097c2c", "dispatch_equip_slot_display_state_by_phase",
        "Equip slot display state machine main dispatch. r0=player_side [0..1] -> r6 "
        "(via adds r6,r0,#0 @ 0x08097c34). "
        "Writes (1-player) to [DAT_08097c5c+0x4]; reads gP1LifePoints+0x1d2c (phase code); "
        "if phase > 0xb jumps to switchD caseD_6; else dispatches 12 cases (0..11) via switch table. "
        "Called exclusively by FUN_0809be70 (equip display driver). "
        "Tags: card_frame, card_ids, card_stats, duel_field, font_jp, game_str, settings. "
        "Params: r0=u32 player_side [0..1]. "
        "Returns r0=void (dispatch hub). "
        "Side effects: [DAT_08097c5c+0x4]:=(1-player_side)."),

    ("FUN_08099314", "dispatch_equip_field_phase_handler",
        "Equip field phase handler main dispatch. r0=player_side [0..1] -> r7 "
        "(via .hword 0x4657=mov r7,r0). "
        "Loads DAT_08099360=0x0201bb90 (duel turn struct); reads [struct+0x4]=player_key -> r8; "
        "computes player_side slot offset (stride 0x14); reads gP1LifePoints+0x1d2c (phase code); "
        "if >0xa jumps to switchD caseD_7; else dispatches 11 cases (0..0xa). "
        "case_0=check_equip_slot_card_type_matches_active_state; "
        "case_1=trigger_equip_activation_candidate_scan (0x08093384). "
        "Called exclusively by FUN_0809be70 (indeg=1). "
        "Params: r0=u32 player_side [0..1]. "
        "Returns r0=void (dispatch hub). "
        "Side effects: via case sub-functions."),

    ("FUN_08099aac", "run_equip_slot_display_update_state_machine",
        "Equip slot display update state machine main driver. r0=player_side [0..1] -> r10 "
        "(via .hword 0x4682=mov r10,r0). "
        "Loads DAT_08099af8=0x0201bb90 (equip state struct base); reads player_key, computes slot base "
        "(stride 0x14); reads gP1LifePoints+0x1d2c (phase code). "
        "Dispatches by phase: 0=LP bar sprite update "
        "(increment/decrement_lp_bar_display_counter, submit_lp_bar_sprite_row_by_type(0xe,...)); "
        "1=check_card_equip_eligibility_in_field; "
        "2=enqueue_equip_slot_sprite_attr; 3+=return 1 (skip). "
        "In case 1 path: calls setup_equip_slot_sprite_attr_by_card (0x0804888c). "
        "Called exclusively by FUN_0809be70 (indeg=1). "
        "Params: r0=u32 player_side [0..1]. "
        "Returns r0=u32 1 (state machine continue) / 0 (exit/no-op). "
        "Side effects: OAM sprite attr buffer via setup_equip_slot_sprite_attr_by_card / enqueue_equip_slot_sprite_attr."),

    ("FUN_08099e0c", "run_equip_spell_display_state_machine",
        "Equip spell display update state machine. r0=player_side [0..1] -> r5. "
        "Decodes callee-save regs (.hword 0x4657/464e/4645=mov r7/r6/r5=r0/r1/r2; "
        ".hword 0x4681=mov r9,r0); loads DAT_08099e54=0x0201bb90 (state struct base); "
        "reads player_key, computes slot offsets (stride 0x14); "
        "reads [struct+0x8]: if non-zero jumps to LAB_0809a16e (active handling path directly); "
        "else reads gP1LifePoints phase code and dispatches. "
        "Structurally symmetric to run_equip_slot_display_update_state_machine (0x08099aac); "
        "difference: checks [struct+0x8] (equip spell activation flag) before phase dispatch. "
        "Called exclusively by FUN_0809be70 (indeg=1). "
        "Params: r0=u32 player_side [0..1]. "
        "Returns r0=u32 1 (continue) / 0 (exit). "
        "Side effects: OAM sprite / state struct via case callees."),

    ("FUN_080984d0", "activate_effect_zone_display_for_slot",
        "Activates effect zone display for a specified slot. r0=player_side [0..1] -> r5. "
        "Loads DAT_0809855c=0x0201bb90 (duel turn struct); r7=[struct+0x4] (player_key); "
        "r1=[struct+0x1c] (effect_flags). "
        "Calls check_slot_card_effect_eligibility(r4=struct, r1=effect_flags) -> r8. "
        "If [struct+0x10]!=0: returns 1 (already active, skip). "
        "Else: writes [struct+0x10]=1 (marks activation-in-progress). "
        "If effect_flags&2==0: calls count_available_effect_zones(player=r7, zone_code=0x131d, mode=-1); "
        "if r4>0 calls enqueue_sprite_attr_by_sign(player, 0x131d) twice; "
        "calls count_zones_by_card_and_mode(0x1320, r5, mode); if r4>0 loops r4 times calling "
        "enqueue_sprite_attr_clamped(player, 0x1f4). Returns 1. "
        "Called exclusively by FUN_0809be70 (indeg=1). "
        "Params: r0=u32 player_side [0..1]. "
        "Returns r0=u32 1 (always, activation complete). "
        "Side effects: [0x0201bb90+0x10]:=1; OAM sprite attr buffer via enqueue_sprite_attr_by_sign "
        "+ enqueue_sprite_attr_clamped."),

    ("FUN_0809b178", "update_equip_activation_display_state",
        "Equip activation state update and display driver. r0=player_side [0..1] -> r6. "
        "Decodes callee-save regs (.hword 0x4657/464e/4645=mov r7/r6/r5); "
        "loads DAT_0809b23c=0x0201bb90 (duel turn struct); reads [struct+0x4]=player_key -> r9; "
        "computes player_side slot base (stride 0x14 -> r7) and opposite slot base (-> [sp,#0x4]); "
        "extracts player_id=r6&1, multiplies by player_stride=0x868, adds gDuelFieldSlots=0x0201c510 -> r8. "
        "Reads [r7+0x4] card entry, extracts stat bits (lsls/lsrs), compares with [r7+0xc] for valid equip pair; "
        "if matched: reads [r7+0x8] halfword, computes sign bit (rsbs/orrs/lsrs #0x1f). "
        "Reads DAT_0809b248=0x0201e20c (equip activation state word); "
        "if ==0: calls increment_lp_bar_display_counter + complex OAM bit-field assembly; "
        "if ==1: jumps to LAB_0809b708. "
        "Else: writes [gP1LifePoints+0x1cf8+player_side*4]=player_id, clears state word. "
        "Called exclusively by FUN_0809be70 (indeg=1). "
        "Params: r0=u32 player_side [0..1]. "
        "Returns r0=u32 (path-dependent; usually 1 or 0). "
        "Side effects: [gP1LifePoints+0x1cf8+player_side*4]:=player_id; "
        "[0x0201e20c]:=0; OAM sprite attr buffer via increment_lp_bar_display_counter et al."),

    ("FUN_0809bdfc", "scan_equip_chain_slots_for_attr_enqueue",
        "Iterates both players' equip chain slots (player [0..1], slot [0..8]), "
        "calls enqueue_equip_chain_attrs_for_slot_range for slots meeting mask condition. "
        "Entry: callee-save decode .hword 0x464f/4646=mov r7/r6=callee-save r9/r8; "
        ".hword 0x4680=mov r8,r0 (saves APCS r0=player_side); movs r0,#1; "
        ".hword 0x4681=mov r9,r0 (r9=1 constant, not a param); r6=0 (player iter). "
        "Outer loop [0..1], inner loop slot [0..8]: computes gDuelFieldSlots offset "
        "(player_id*0x868 + slot*0x14 + base + 0x64); reads entry high bits; "
        "if mask condition met (ands with DAT_0809be6c bit): calls enqueue_equip_chain_attrs_for_slot_range(player, slot). "
        "After loops: calls check_activation_phase_counter_is_six; "
        "if r0==0: calls set_player_state_bit_with_sprite_update(r8, 0x12, 1). Returns 1. "
        "Called exclusively by FUN_0809be70 (indeg=1). "
        "Params: r0=u32 player_side [0..1] (saved to r8 via .hword 0x4680). "
        "Returns r0=u32 1 (always). "
        "Side effects: OAM sprite attr buffer via enqueue_equip_chain_attrs_for_slot_range; "
        "[player_state] bit 0x12 via set_player_state_bit_with_sprite_update (cond)."),

    ("FUN_0809be70", "advance_equip_display_phase_via_table",
        "Advances equip display phase via function pointer table. r0=player_side [0..1]. "
        "Loads DAT_0809bea4=0x09e5aaec (function pointer table base); "
        "loads gP1LifePoints+0x1d28 (activation counter) -> r4; "
        "reads [r4]=counter, index into table (counter*4 + base), fetches function ptr. "
        "Calls FUN_0810e5cc(r0=player_side); if returns 0: writes [gP1LifePoints+0x1d2c]=0 (clear phase code), "
        "increments [gP1LifePoints+0x1d28] (counter+1), returns 0. "
        "If returns non-zero: returns 0. "
        "If table ptr==0: returns 1 (phase complete). "
        "3 callers: FUN_0809bebc, FUN_0809e168 (card display), FUN_080bc648 (duel_field). "
        "Params: r0=u32 player_side [0..1]. "
        "Returns r0=u32 0 (phase advancing) / 1 (phase complete or init). "
        "Side effects: [gP1LifePoints+0x1d2c]:=0 (cond); [gP1LifePoints+0x1d28]:=counter+1 (cond)."),

    ("FUN_080ac21c", "check_equip_card_valid_for_target_slot",
        "Checks whether equip card (card_id) is valid for a target monster slot. "
        "r0=player_key (bit0=player_id [0..1]) -> r6; "
        "r1=target_slot_ptr (ptr to gDuelFieldSlots monster slot) -> r8 (via .hword 0x4688); "
        "r2=equip_slot_idx [0..4] -> r10 (via .hword 0x4642). "
        "Extracts player_id=r6&1; computes equip_slot_idx*4 + target_slot_ptr*4 -> reads gDuelFieldSlots dword "
        "-> extracts card_id (lsls/lsrs 0x13 = bits[18:0]). "
        "Executes large switch (20+ cmp chain) on card_id (0x14af, 0x13a7, 0x129a, 0x12a3, 0x157c, "
        "0x1476, 0x147a, 0x147f, 0x1370 etc); each case calls different validity checker. "
        "Called exclusively by eval_equip_slot_target_eligibility_full (0x080bc418). "
        "Params: r0=u32 player_key (bit0=player_id [0..1]); "
        "r1=ptr target_slot_ptr (gDuelFieldSlots monster slot); "
        "r2=u32 equip_slot_idx [0..4]. "
        "Returns r0=u32 1=equip valid, 0=invalid. "
        "Side effects: none (read-only check). "
        "Constants: CARD_ID=0x13a7 (Injection Fairy Lily); CARD_ID=0x129a (Reflect Bounder); "
        "CARD_ID=0x12a3 (Little-Winguard); CARD_ID=0x1476 (Ancient Lamp); "
        "CARD_ID=0x147a (Mystical Beast Serket); CARD_ID=0x147f (Jowgen the Spiritualist); "
        "CARD_ID=0x1370 (Kiseitai); CARD_ID=0x157c (unknown; not in data.md or cards-ids-array.s)."),

    ("FUN_080ad720", "score_equip_targets_for_monster_slot",
        "Scores all equipable targets for a monster slot and collects results. "
        "r0=player_key (bit0=player_id) -> r7 (via adds r7,r0,#0 @ 0x080ad722); "
        "r1=equip_zone_count [0..N] -> r9 (via .hword 0x4691). "
        "Reads gP1LifePoints (via PTR_gP1LifePoints_080ad774), offset 0x87*32=0x10c0; "
        "reads halfword [base+offset] as monster_stat; extracts card_id (lsls/lsrs 0x13). "
        "Calls score_equip_slot_placement_for_ai(player=r7, monster_stat, mode=0) -> r6=score_count. "
        "Init r5=0 (slot iter); if r5<r6: calls eval_equip_target_slot_with_score(player, slot=r9, sp_buf, iter=r5); "
        "if returns -1 returns 0; else writes result to sp+4 buffer. r5++; loops r6 times. "
        "Returns 1 (all slots scored). "
        "Called exclusively by find_equip_slot_by_player_and_zone_count (0x080bb0f8). "
        "Params: r0=u32 player_key (bit0=player_id [0..1]); r1=u32 equip_zone_count [0..N]. "
        "Returns r0=u32 1=all scored, 0=a target returned -1 (invalid). "
        "Side effects: [sp+4..sp+4+count*2] written with scored halfwords."),

    ("FUN_080bb0f8", "find_equip_slot_by_player_and_zone_count",
        "Finds equip slots satisfying effect count condition for a player. "
        "r0=player_key -> r5 (bit0=player_id); r1=zone_count -> [sp,#0]. "
        "Internal counter r8=0 (not a caller input; movs r0,#0; .hword 0x4680=mov r8,r0). "
        "Reads gP1LifePoints+player_stride+0xc (zone_limit, via r4=0x90*2=0x120 offset); "
        "if r8>=zone_limit returns 1 (no slots available). "
        "Loop (base r7=gP1LifePoints+0x120+player_id*0x868): reads each sub-slot [r7+0x0] dword, "
        "extracts card_id (lsls/lsrs 0x13); calls check_card_field5_is_nonzero(card_id); "
        "if 0 jumps to LAB_080bb2ac (slot has no field5). "
        "Else: large switch on card_id (0x1488, 0x127d, 0x1578 etc), "
        "each case calls dispatch_effect_handler_by_card_id or enqueue_sprite_attr variant. "
        "Callers: FUN_080bb2d4, FUN_080bc54c (player 0), FUN_080bc5d4 (player 1). "
        "Params: r0=u32 player_key (bit0=player_id [0..1]); r1=u32 zone_count -> [sp,#0]. "
        "Returns r0=u32 0=found+processed, 1=no available slot or condition not met. "
        "Side effects: OAM sprite attr buffer + effect handling via case callees. "
        "Constants: CARD_ID=0x1488 (Gilasaurus); CARD_ID=0x127d (Manga Ryu-Ran); "
        "CARD_ID=0x1578 (Lava Golem)."),

    ("FUN_080bc418", "eval_equip_slot_target_eligibility_full",
        "Evaluates equip slot target eligibility and executes activation if conditions met. "
        "r0=player_side [0..1] -> r5; r1=slot_idx [0..4] -> r6; "
        "r2=check_mode (0=slot_binding_check, non-0=full_validity_check). "
        "If r2==0: reads [0x0201afe0+r6*4+0x198] to confirm slot binding; if non-zero sets r4=-1. "
        "If r2!=0: calls check_equip_card_valid_for_target_slot(r5, r6, 0); "
        "if not -1 sets r4=0 (passed). "
        "Then: calls check_slot_field_action_eligibility(r5, r6); if 0 returns 0. "
        "If passed: extended checks (check_field_spell_last_warrior_placeable, "
        "check_card_stat_field8_is_6, check_field_spell_neo_daedalus_group_placeable, "
        "check_toon_world_equip_present; count_field_copies_of_card for 0x15fb/0x197b); "
        "all pass: calls apply_slot_equip_activation_with_sprite(r5, r6, 0, 0). "
        "Returns 1=activation executed, 0=conditions not met. "
        "Callers: FUN_080bc54c (player 0), FUN_080bc5d4 (player 1). "
        "Params: r0=u32 player_side [0..1]; r1=u32 slot_idx [0..4]; "
        "r2=u32 check_mode (0=binding, non-0=full). "
        "Returns r0=u32 1=activated, 0=not met. "
        "Side effects: via apply_slot_equip_activation_with_sprite: OAM sprite + equip activation state; "
        "via init_equip_sub_entry_fields_from_slot: equip sub-entry fields. "
        "Constants: CARD_ID=0x15fb (Final Attack Orders); CARD_ID=0x197b (Level Limit - Area A)."),

    ("FUN_080bc54c", "run_equip_activation_state_machine_p1",
        "Equip activation state machine driver for player 0 (P1 side). "
        "No APCS input params; reads gP1LifePoints+0x1ce8 -> r5 (equip player_side); "
        "loads 0x0201afe0 (equip control struct) -> r4; reads [r4+0x8] (state code). "
        "State dispatch: 0 (bcc)=reads [gP1LifePoints+0x1cf4] (zone_count), if <=2 calls "
        "find_equip_slot_by_player_and_zone_count(r5, 0); if returns 0 increments [r4+0x8]; "
        "then calls dispatch_equip_activation_full_sequence(r5), if success increments [r4+0x8]. "
        "1 (beq LAB_080bc590)=calls dispatch_equip_activation_full_sequence(r5), fail->0. "
        "2 (beq LAB_080bc5ac)=calls compute_equip_zone_score_with_cache(r5), "
        "loops slot [0..4] calling eval_equip_slot_target_eligibility_full(r5, slot, mode=0). "
        "3+=returns 1. "
        "Called exclusively by FUN_080bc71c (duel_field, indeg=1). "
        "Params: none. "
        "Returns r0=u32 0=state machine running/fail, 1=terminated/success. "
        "Side effects: [0x0201afe0+0x8]:=counter+1; activation and sprite via callees."),

    ("FUN_080bc5d4", "run_equip_activation_state_machine_p2",
        "Equip activation state machine driver for player 1 (P2 side). "
        "Structurally symmetric to run_equip_activation_state_machine_p1 (0x080bc54c); "
        "differences: state 0 calls find_equip_slot_by_player_and_zone_count(r5, zone_count=1) "
        "(P1 uses zone_count=0); state 2 calls eval_equip_slot_target_eligibility_full(r5, slot, mode=1) "
        "(P1 uses mode=0). "
        "No APCS input params; reads gP1LifePoints+0x1ce8 -> r5 (player_side); "
        "loads 0x0201afe0 -> r4; reads [r4+0x8] dispatch. "
        "Called exclusively by FUN_080bc71c (duel_field, indeg=1). "
        "Params: none. "
        "Returns r0=u32 0=running/fail, 1=terminated/success. "
        "Side effects: [0x0201afe0+0x8]:=counter+1; activation and sprite via callees."),

    ("FUN_080bc648", "dispatch_equip_activation_phase_by_state",
        "Dispatches equip activation phase handling by state code. "
        "Reads gP1LifePoints+0x1ce8 (equip activation player_side) -> r4; "
        "loads 0x0201afe0 (equip activation control struct) -> r5; "
        "reads [r5+0x8] (state code); dispatches: "
        "0=check_equip_effect_zone_preconditions + check_equip_slot_activation_blocked_by_chain + "
        "eval_equip_monster_zone_score_full + try_activate_equip_via_two_tables "
        "(clears [gP1LifePoints+0x1d28/0x1d2c], increments [r5+0x8]); "
        "1=submit_lp_bar_sprite_row_by_type(3,0) + [r5+0x8]++; "
        "2=advance_equip_display_phase_via_table(r4) -- if returns non-zero [r5+0x8]++; "
        "3=FUN_0809be70(r4) -- if returns 0 [r5+0x8]++; "
        "4+=enqueue_sprite_attr_record(0x10/0x8010,...) + returns 1. "
        "Called exclusively by FUN_080bc71c (duel_field, indeg=1). "
        "Params: none. "
        "Returns r0=u32 0 (state machine running) / 1 (terminated/complete). "
        "Side effects: [gP1LifePoints+0x1d28]:=0; [gP1LifePoints+0x1d2c]:=0 (state 0 path); "
        "[0x0201afe0+0x8]:=counter+1; OAM sprite attr buffer via enqueue_sprite_attr_record "
        "/ submit_lp_bar_sprite_row_by_type."),
]


def do_rename(old, new, comment):
    af = currentProgram.getAddressFactory()
    space = af.getDefaultAddressSpace()
    st = currentProgram.getSymbolTable()
    fm = currentProgram.getFunctionManager()

    # find by current name symbol OR by address if old starts with "FUN_"
    target = None
    syms = st.getSymbols(old)
    for s in syms:
        if s.getSymbolType().toString() == "Function":
            target = s
            break
    if target is None and old.startswith("FUN_"):
        try:
            addr_int = int(old[4:], 16)
            addr = space.getAddress(addr_int)
            func = fm.getFunctionAt(addr)
            if func is not None:
                target = func.getSymbol()
        except Exception:
            pass
    if target is None:
        print("[skip ] not found: %s" % old)
        return False
    if RUN_DRY:
        print("[dry  ] %s -> %s" % (old, new))
        return True
    try:
        target.setName(new, SourceType.USER_DEFINED)
    except Exception as e:
        print("[warn] rename %s: %s" % (old, e))
        return False
    is_rename_userdefined = not old.startswith("FUN_")
    try:
        if isinstance(comment, str):
            comment_u = comment.decode("utf-8")
        else:
            comment_u = comment
        func = fm.getFunctionAt(target.getAddress())
        if func is not None:
            listing = currentProgram.getListing()
            cu = listing.getCodeUnitAt(func.getEntryPoint())
            if cu is not None:
                existing = cu.getComment(CodeUnit.PLATE_COMMENT)
                if is_rename_userdefined or not existing:
                    cu.setComment(CodeUnit.PLATE_COMMENT, comment_u)
    except Exception as e:
        print("[warn] plate comment %s: %s" % (new, e))
    print("[ok] %s -> %s" % (old, new))
    return True


def main():
    ok = 0
    for old, new, comment in RENAMES:
        if do_rename(old, new, comment):
            ok += 1
    print("[done] RenameBatch63: %d/%d" % (ok, len(RENAMES)))


main()
