"""Write plate .txt files for batch #123 and update naming-proposals.csv name column."""
import os
import csv

EVAL_DIR = "doc/dev/eval"
CSV_PATH = "doc/dev/naming-proposals.csv"

plates = {
    '08032500': ("find_field_slot_idx_by_card_id",
        "Traverse player-side field slots (slot 0..4, stride 0x14), read slot[0] low 13 bits (card_id), compare with target card_id; also require slot[+8] != 0 (equip_chain_head attached). If match, return current slot index r4 immediately; if no match after full scan, return -1 (rsbs #1,#0). indeg=0; grep 08032501 asm/all.s -> 0 hits; dead code or runtime fn-ptr. Constants: gDuelFieldSlots=0x0201c510, PLAYER_STRIDE=0x868, SLOT_COUNT=5."),
    '08033d98': ("count_hand_slots_with_field6_val_0x17",
        "Traverse player-side field spell/trap zone 5 slots (index 0..4, stride 0x14), count slots satisfying: (1) slot[0] low 13 bits card_id != 0; (2) slot[+8] (equip_chain_head) != 0; (3) get_card_extended_stat_field6(card_id) == 0x17. indeg=0, not referenced by any named function. Sibling of FUN_08033de4 (field6 target 0x17 vs 0x16). Constants: gDuelFieldSlots=0x0201c510, PLAYER_STRIDE=0x868, FIELD6_TARGET=0x17, SLOT_STRIDE=0x14, SLOT_COUNT=5."),
    '08033de4': ("count_hand_slots_with_field6_val_0x16",
        "Structurally symmetric sibling of 0x08033d98 (count_hand_slots_with_field6_val_0x17), sole difference is field6 target value changed from 0x17 to 0x16. Traverses player-side field spell/trap zone 5 slots (stride 0x14), counting card_id!=0 && equip_chain_head!=0 && get_card_extended_stat_field6(card_id)==0x16. indeg=0. Constants: gDuelFieldSlots=0x0201c510, PLAYER_STRIDE=0x868, FIELD6_TARGET=0x16."),
    '08037128': ("count_graveyard_entries_by_card_id",
        "Count entries in specified player-side graveyard array matching target card_id. Read gP1LifePoints+0x1c+player_id*0x868 for graveyard entry count, traverse graveyard word array at base offset 0x5d0 (=0xba<<3) with stride 4 bytes, extract low 13 bits of each word as card_id, compare with target r1 (16-bit truncated), accumulate counter r4 on match. Return total match count. indeg=0, referenced by runtime fn-ptr or dead code. Constants: gP1LifePoints, PLAYER_STRIDE=0x868, GRAVEYARD_COUNT_OFFSET=0x1c, GRAVEYARD_ARRAY_BASE=0x5d0 (=0xba<<3)."),
    '0803a994': ("eval_slot_score_entry_full_with_sp_result",
        "Thin wrapper over eval_slot_score_entry_full: allocates 0x24-byte stack frame (9 words), calls eval_slot_score_entry_full with stack area as output buffer; reads analysis result from sp+0x20 after call, cleans stack, pop{r1};bx r1 void exit. Called by 0x0807615c (duel_field) in equip slot match-check loop, passing player_id and effect_slot pointer, to obtain stack-written results in scenarios not relying on return value. Constants: FRAME_SIZE=0x24 (9 words), RESULT_OFFSET=0x20."),
    '08044618': ("render_equip_zone_sprite_with_chain_lp",
        "Composite function to render equip zone OAM sprite and trigger LP chain indicator. When r1 >= 0: get zone slot ptr with zone=0xb, immediately call enqueue_equip_zone_sprite_direct (no chain); extract card_type_index (bits[25:24]<<1 | bit[13]) and side_flag (bit[14]) from slot[0], find effect node for DAT_08044670=0x1379 (icid=0x1379=Graverobber) via find_effect_node_in_zone; if found, call enqueue_equip_zone_sprite_by_side to append side sprite; finally submit_lp_change_indicator_with_chain_check(r0=player_id, r1=0x7d0, r2=0, r3=effect_ptr). pop{r0};bx r0 void exit. Called by FUN_080583bc (duel_field) in equip activation case=1. Function: (1) unconditionally enqueue direct sprite; (2) enqueue side sprite conditioned on effect_node presence; (3) submit LP chain indicator. Constants: ZONE_B=0xb (equip zone), icid=0x1379 (Graverobber), LP_VAL=0x7d0 (=0xfa<<3 = 2000)."),
    '08044674': ("enqueue_graveyard_spell_sprite_and_lp",
        "Search graveyard for entry matching graveyard_ptr, if found construct OAM sprite attributes and enqueue, also enqueue LP bar sprite row. Flow: (1) find_graveyard_entry_by_ptr(r1=graveyard_ptr, r2=slot_ptr) locates graveyard entry, return 0 if result < 0; (2) extract col_side_packed and side_flag from slot[0], call check_card_type_is_spell to check if spell card; (3) set r1 (row_type: 0xc/0xb) based on spell/non-spell, compute LP base via gP1LP+0xc+player_id*0x868; (4) construct attr1/attr2 and call enqueue_sprite_attr_record(0x3f,...); (5) call enqueue_sprite_attr_with_type_select for non-spell path. Return 1. indeg=0. Constants: OAM_ATTR0=0x3f, PLAYER_STRIDE=0x868, LP_BASE_OFFSET=0xc, SPELL_ROW=0xc, NON_SPELL_ROW=0xb."),
    '08044714': ("enqueue_graveyard_spell_sprite_with_zone_ref",
        "Sibling of 0x08044674: search graveyard for entry at zone_ptr, on hit construct OAM sprite attributes and enqueue. Adds third parameter r8 (extra card_struct_ptr) to read additional flag from [r8+2] (bit0 XOR player_id yields flip_flag). Flow: find_graveyard_entry_by_ptr(r6=graveyard_ptr, r7=zone_slot_ptr); return 0 on failure. Success: extract col_side + side_flag; check_card_type_is_spell -> set row_type (0xb/0xc); compute flip_flag via eors+rsbs+orrs; construct attr; enqueue_sprite_attr_record(0x3f,...); call enqueue_sprite_attr_with_type_select for non-spell path. Return 1. indeg=9, multiple duel_field callers. Constants: OAM_ATTR0=0x3f, PLAYER_STRIDE=0x868, LP_OFFSET=0xc, SPELL_ROW=0xc, NON_SPELL_ROW=0xb."),
    '080448a0': ("enqueue_graveyard_spell_sprite_with_player_xor",
        "Third variant of three-sibling cluster (0x08044674 / 0x08044714 / 0x080448a0), with three extra high-register inputs r8/r9/r10 (saved via push {r5,r6,r7} block .hword 0x46xx sequence). Locate graveyard entry corresponding to zone_ptr (find_graveyard_entry_by_ptr); on success extract col_side + side_flag; compute flip_flag as (1 - player_id) XOR r2 bit0 (using subs r2,r4,r7 = 1-player_id); call check_card_type_is_spell -> set row_type; construct attr and enqueue_sprite_attr_record(0x3f,...); non-spell path appends enqueue_sprite_attr_with_type_select. Return 1. Called once by FUN_0806c780 (duel_field rendering). Constants: OAM_ATTR0=0x3f, PLAYER_STRIDE=0x868."),
    '08044a28': ("enqueue_hand_sprite_with_flip_flag_set",
        "Single-instruction trampoline wrapper over enqueue_hand_sprite_by_zone_set_code: fixes r2=1 (h_flip_flag=1) then directly tail-calls. indeg=10, called by 5 card_frame/duel_field rendering functions. Contrast with FUN_0807cef0 which calls same function with r2=0 (no flip). This wrapper is dedicated to hand sprite enqueue scenarios requiring horizontal flip. pop{r1};bx r1 void exit."),
    '08044ca4': ("enqueue_sprite_attr_row_0x29_by_player",
        "Select attr0 base by player_id (P1: 0x29, P2: 0x8029), truncate r1 to 16 bits, call enqueue_sprite_attr_record(attr0, r1_u16, 0, 0). Fixed row_type=0x29, attr2=0, attr3=0. Called by FUN_0807c388 in equip/effect activation state machine case=0x7d path, to enqueue fixed-row-0x29 sprite attribute record. pop{r0};bx r0 void exit. Constants: OAM_P1_ATTR0=0x29, OAM_P2_ATTR0=0x8029."),
    '08044cc4': ("enqueue_sprite_attr_row_0x29_with_flag2",
        "Structurally symmetric sibling of 0x08044ca4 (enqueue_sprite_attr_row_0x29_by_player), sole difference is attr3=2 (0x08044ca4 fixes attr3=0). Select attr0 base by player_id (P1: 0x29, P2: 0x8029), truncate r1 to 16 bits, call enqueue_sprite_attr_record(attr0, r1_u16, 0, 2). Called by FUN_08083ba0 in effect activation case=1 rendering path after trigger_card_display_op31. pop{r0};bx r0 void. Constants: OAM_P1_ATTR0=0x29, OAM_P2_ATTR0=0x8029, ATTR3_FLAG=2."),
    '08047c68': ("update_equip_target_bitmap_zone_d_no_flag",
        "Minimal wrapper over update_equip_target_bitmap_for_field: fixed zone=0xd (zone_d), r3=0 (no extra flag), pass-through r0/r1. pop{r1};bx r1 void exit. indeg=0. Sibling pair with 0x08047ef0 (zone=0xe, flag=0). Constants: ZONE_D=0xd, FLAG=0."),
    '08047c78': ("reset_equip_slot_ctx_with_bitmap_update_zone_d",
        "Composite function for equip slot context init plus zone_d bitmap update. Flow: (1) compute slot_mask=1<<(r0*16+r1) and save to r5; (2) move sp into r0 (.hword 0x4668=mov r0,sp), memset(sp, 0, 0x18) zero 24-byte context area; (3) strh r3,[sp,#0] write initial h-word; (4) read r2 (=r10) bit1, invert and write to [r2,+2] bit0 (player side flag modify); (5) call update_equip_target_bitmap_for_field with slot_mask and zone=0xd; (6) AND return value with slot_mask to test, return 1/0. indeg=0. Constants: ZONE_D=0xd, CTX_SIZE=0x18, BIT1_MASK=0x2."),
    '08047ef0': ("update_equip_target_bitmap_zone_e_no_flag",
        "Minimal wrapper over update_equip_target_bitmap_for_field: fixed zone=0xe, r3=0 (no extra flag), pass-through r0/r1. pop{r1};bx r1 void exit. indeg=3, called by three field rendering functions FUN_080584cc / FUN_080777d8 / FUN_0807c474. Sibling pair with 0x08047c68 (zone=0xd). Constants: ZONE_E=0xe, FLAG=0."),
    '08047f00': ("update_equip_bitmap_zone_e_with_slot_save",
        "Context-saving variant of zone_e equip target bitmap update: first read bitmap_ctx[+0] halfword and save to r5, zero bitmap_ctx[+0], call update_equip_target_bitmap_for_field(ctx, slot_mask, zone=0xe, flag=0), then restore r5 back to bitmap_ctx[+0]. Result pass-through. pop{r1};bx r1 void exit. Called by FUN_08059068 (duel_field). This function ensures context first field is temporarily zeroed then restored during bitmap update (avoids stale state interference). Constants: ZONE_E=0xe, FLAG=0."),
    '08048268': ("render_zone_sprite_with_effect_dispatch_by_slot",
        "Check card type eligibility by zone slot and render sprite, also dispatch card effect zone action. Flow: when r1=0 read [0x0201bb90+0] as player_id base r5, when r1!=0 read [0x0201bb90+4]; read r6 from same base at offset 0x1c (r1=0) / 0x20 (r1!=0). Index EWRAM zone table (DAT=0x0201bc54) by slot_idx r1 (lsls*5=stride 20), read slot word; extract card_id (low 13 bits to r4), col_side (bits[25:24]<<1|bit[14]), side_flag. Call query_slot_card_type_eligibility; return 0 if ineligible or card_id==0. check_card_field8_is_9: if type-9 card enqueue sprite with row_type=0x10 / attr0=P2 0x8031 (r5!=0) or 0x31. Otherwise check [r8+2]bit0 vs r5, construct attr0=0x33(P1)/0x8033(P2), row_type=r7 (with count_field_copies_of_card 0x80<<9 OR), call dispatch_card_effect_zone_action_by_card_id. Return 1/0. Constants: ZONE_TABLE=0x0201bc54, PLAYER_BASE=0x0201bb90, icid=0x1332 (Banisher of the Light), ROW10=0x10, P1_ATTR0=0x33, P2_ATTR0=0x8033, FIELD_COUNT_BIT=0x80<<9."),
    '08048560': ("render_zone_sprite_with_effect_dispatch_alt",
        "Sibling of FUN_08048268, nearly identical structure: read [0x0201bb90+0]/[+4] base by player_side_flag, index ZONE_TABLE=0x0201bc54 (stride 20) by slot_idx, extract card_id / col_side / side_flag; call query_slot_card_type_eligibility; return 0 if ineligible or empty. Differences: (1) in non-type-9 path r7 (side_flag) undergoes more bit processing as attr0 flag inject; (2) uses row_type=0x1a (vs FUN_08048268 0x10); (3) attr0=0x40 (vs 0x10). Shares icid=0x1332 (Banisher of the Light) count_field_copies_of_card post-OR bit 0x80<<9. indeg=0. Constants: ZONE_TABLE=0x0201bc54, PLAYER_BASE=0x0201bb90, icid=0x1332 (Banisher of the Light), ROW_TYPE=0x1a, FIELD_COUNT_BIT=0x80<<9, ATTR0=0x40."),
    '080499c4': ("render_pair_zone_sprites_if_field_card_present",
        "Query field copy count for icid 0x1332 (Banisher of the Light); if > 0 directly call render_matched_pair_zone_sprites and return; otherwise enter detailed pair-check loop: traverse P1/P2 hand and field zones, test pair eligibility per slot via check_card_pair_allowed, on match call render_spell_zone_card_sprite_with_id_tree to render corresponding zone sprite. On first pair found call increment_lp_bar_display_counter; at end call decrement_lp_bar_display_counter + scan_field_slots_for_equip_sprite. pop{r0};bx r0 void exit. Called by duel_field rendering functions and FUN_0806d960 / FUN_0807f0a4. Function: fast-path render if field copy present; else full pair scan+render. Constants: icid=0x1332 (Banisher of the Light), PLAYER_STRIDE=0x868, ZONE_A=0x0201c4f0, ZONE_B=0x0201c4f8."),
    '08049b44': ("render_spell_zone_sprite_with_field_copy_check",
        "Before rendering spell zone sprite, check field copy count (icid=0x1332=Banisher of the Light). If count_field_copies_of_card > 0: read slot halfword from gP1LP+player_id*0x868+0x10e0+r1*4, extract low 13 bits as card_id, call check_card_type_is_spell to decide zone_row (0xd=non-spell / 0xc=spell), select attr0 (P1=0x33 / P2=0x8033), construct attr and enqueue_sprite_attr_record, then call submit_lp_bar_sprite_row_by_type(0x23, 0). If count==0: call render_spell_zone_card_sprite_with_id_tree to render; then scan_field_slots_for_equip_sprite(player_id, 1). pop{r0};bx r0 void exit. Called by 5 duel_field functions. Constants: icid=0x1332 (Banisher of the Light), ZONE_OFFSET=0x10e0 (=0x87<<5), P1_ATTR0=0x33, P2_ATTR0=0x8033, SPELL_ROW=0xc, NON_SPELL_ROW=0xd, LP_ROW=0x23."),
}

# Write plate files
for addr, (name, plate_text) in plates.items():
    plate_path = os.path.join(EVAL_DIR, f"{addr}.plate.txt")
    with open(plate_path, 'w', encoding='ascii', newline='\n') as f:
        f.write(plate_text)
    print(f"Wrote {plate_path}")

# Update CSV name column
print(f"\nUpdating {CSV_PATH}...")
rows = []
updated = 0
with open(CSV_PATH, 'r', encoding='utf-8', newline='') as f:
    reader = csv.reader(f)
    header = next(reader)
    rows.append(header)
    # find column indices
    addr_col = header.index('address')
    name_col = header.index('name')
    for row in reader:
        if len(row) > addr_col:
            addr_val = row[addr_col].strip().lower().lstrip('0x')
            addr_8 = addr_val.zfill(8)
            if addr_8 in plates:
                old_name = row[name_col]
                new_name = plates[addr_8][0]
                if old_name != new_name:
                    row[name_col] = new_name
                    updated += 1
                    print(f"  {addr_8}: {old_name} -> {new_name}")
        rows.append(row)

with open(CSV_PATH, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print(f"\nCSV updated: {updated} rows changed")
print("Done.")
