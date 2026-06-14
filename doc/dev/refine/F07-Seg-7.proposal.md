# Refine Proposal: F07-Seg-7  [0x080613b4..0x08061eb4)

## 段测绘
- 函数入口 x34 (asm lines 13519..15283):
  - check_equip_slot_eligible_by_card_id_graveyard_threshold @0x080613b4
  - check_equip_slot_eligible_with_dual_player_zone_limit @0x08061404
  - check_equip_slot_eligible_neo_daedalus_banisher_absent_with_field6_range @0x08061434
  - check_equip_slot_eligible_field_spell_with_effect_context_zone_val10 @0x0806153c
  - check_equip_slot_eligible_banisher_absent_with_umi_pair @0x08061584
  - check_equip_slot_eligible_field_spell_effect_type_e_with_zone_field5 @0x080615d8
  - check_equip_slot_eligible_neo_daedalus_with_both_players_loop @0x08061624
  - check_equip_slot_eligible_neo_daedalus_with_lp_slot_effect @0x08061660
  - commit_equip_effect_node_zone_match @0x08061688
  - check_equip_slot_eligible_type480_with_neo_daedalus_field5_loop @0x080617ac
  - check_equip_slot_eligible_by_lp_gap_7000_vs_opponent @0x08061874
  - check_equip_slot_eligible_chain_absent_with_setcode_dispatch @0x080618b4
  - check_equip_eligible_with_lp_advantage @0x080618d4
  - check_equip_slot_eligible_neo_daedalus_with_lp_status_lookup @0x08061938
  - check_equip_slot_eligible_by_player_status_gt2_with_setcode_dispatch @0x08061988
  - check_equip_slot_eligible_by_active_ctx_score_threshold @0x080619c0
  - dispatch_effect_via_hand_slot_setcode @0x080619f0
  - check_dragon_spell_target_slot_available @0x08061ac0
  - check_equippable_slots_with_player_status @0x08061b14
  - check_equip_slot_eligible_sanctuary_paired_with_setcode_dispatch @0x08061b54
  - check_equip_slot_eligible_by_zone_slot_flag1_present @0x08061ba8
  - check_equip_slot_eligible_neo_daedalus_with_lp_and_status_sum @0x08061bc4
  - check_equip_slot_eligible_by_lp_minus_vs_graveyard_field7 @0x08061c10
  - check_equip_slot_eligible_mask_of_restrict_absent @0x08061c4c
  - check_equip_slot_eligible_spell_type480_with_activatable_count @0x08061c90
  - check_equip_slot_eligible_zone_e_type580_with_neo_daedalus @0x08061cc8
  - check_zera_ritual_absent_from_field @0x08061d40  [FUNC_RENAME candidate]
  - check_equip_slot_has_zone_pair_hit_table_07ad @0x08061d5c
  - check_equip_slot_eligible_paired_zone_with_banisher_guard @0x08061d78
  - check_equip_slot_eligible_by_lp_status_tier3_neo_daedalus @0x08061dcc
  - check_equip_slot_eligible_by_effect_zone_count5 @0x08061e04
  - check_equip_slot_eligible_field_zone_type140_with_zone_count @0x08061e20
  - check_equip_slot_eligible_chain_present_with_lp_status_neo_daedalus @0x08061e50
  - check_equip_slot_has_zone_pair_hit_table_1e95 @0x08061e98

- 残留自动名槽 x63:
  - DAT_ x14: DAT_08061900(0x1cf4) DAT_08061934(0x868) DAT_0806197c(0x868) DAT_080619b4(0x868)
    DAT_08061a08(0x1332) DAT_08061ab8(0x868) DAT_08061abc(0x0201c4ec) DAT_08061ad4(0x175b)
    DAT_08061adc(0x0fa7) DAT_08061b08(0x0ff8) DAT_08061b48(0x868) DAT_08061b90(0x175e)
    DAT_08061b98(0x868) DAT_08061d50(0x1332)
  - DWORD_ x43: (see EQ_SLOTS table below)
  - PTR_ x6: PTR_gP1LifePoints_080618fc/08061978/080619b0/08061ab4/08061b44/08061b94

- ROM_INCBIN x1: 0x61c66/0x2a

---

## データブロック分類 (Rule 2/3) -- ref-scan 証拠

| 块 | ref-scan (raw / THUMB+1) | 判定 | 理由 |
|---|---|---|---|
| 0x08061c66 sz=0x2a | raw=0 / THUMB+1=2 (1 real + 1 false positive) | R4 disasm | THUMB+1 hit at 0x01e42058 (ROM 0x09e42058): valid handler table entry CID=0x1776 (Corpse of Yata-Garasu, pw=30461781) fn_eligible ptr = 0x08061c69. Second hit at 0x00d54793 (ROM 0x08d54793) rejected: CID would be 0x30c410c6 (not a valid slot_id, >0x1900 max) -- compressed data false positive. |

**Block structure (python-decoded, file:15052:14910):**
- 0x08061c66 (+0x00): `.zero 2` -- alignment pad before function entry
- 0x08061c68 (+0x02): fn_eligible for CID 0x1776 (Corpse of Yata-Garasu)
  - ldr r2, [pc,#24] (->gP1LifePoints at block+0x1e)
  - ldrb r0, [r0,#2] -> player_id byte
  - lsls r0,r0,#0x1f / lsrs r0,r0,#0x1f -> bit0 (player_id)
  - ldr r1, [pc,#20] (->0x868 at block+0x22)
  - muls r0,r1 -> player_offset
  - adds r2,#0x10 -> gP1LP+0x10
  - adds r0,r0,r2 -> gP1LP+0x10+player*0x868
  - ldr r0,[r0,#0] -> player LP status word
  - cmp r0,#0; bne -> 0x08061c8c (movs r0,#2; bx lr) if nonzero -> return 2
  - movs r0,#0; b -> 0x08061c8e (bx lr) if zero -> return 0
- 0x08061c84 (+0x1e): .word gP1LifePoints=0x0201c4e0 (literal pool)
- 0x08061c88 (+0x22): .word 0x00000868=PLAYER_BLOCK_STRIDE (literal pool)
- 0x08061c8c (+0x26): movs r0,#2; bx lr (return-2 arm, falls through)

**Handler table at 0x09e4204c (python-verified):**
- +0: 0x00001776 (CID = Corpse of Yata-Garasu)
- +4: 0x080656e1 (fn_activate+1, in file 07)
- +8: 0x08053c71 (pad fn-ptr)
- +12: 0x08061c69 (fn_eligible+1 = block+0x03, THUMB flag set)
- +16: 0x08056bc5 (pad fn-ptr)
- +20: 0x00000000 (zero terminator)

**New fn name:** `check_player_lp_status_nonzero_for_cid_1776`
(reads gP1LP[player*0x868+0x10] status word; if nonzero->2; else->0)
Plate (ASCII): "fn_eligible for CID 0x1776 (Corpse of Yata-Garasu, pw=30461781); reached via handler dispatch table 0x09e4204c. Reads player LP status word gP1LifePoints[player*0x868+LP_SLOT_ACTIVE_OFF(0x10)]; nonzero->return 2, zero->return 0."

**Literal pool slots inside block:**
- 0x08061c84: .word gP1LifePoints = gp1lp_ptr_08061c84 (REF slot)
- 0x08061c88: .word 0x868 = PLAYER_BLOCK_STRIDE (EQ slot -> player_stride_08061c88)

---

## 符号化計画 (R1/R2/R3)

### EQ_SLOTS (data-equate)

All reuse existing inc unless marked NEW.

| slot | value | const_name | slot_label | inc | note |
|---|---|---|---|---|---|
| DWORD_080613cc | 0x14f0 | REVERSAL_OF_GRAVES_CID | reversal_of_graves_cid_080613cc | card_info.inc | NEW; card-stats.s L13743 slot=0x14F0 pw=17484499 |
| DWORD_080613d0 | 0x16dc | BLASTING_THE_RUINS_CID | blasting_the_ruins_cid_080613d0 | card_info.inc | NEW; card-stats.s L18696 slot=0x16DC pw=21466326 |
| DWORD_08061400 | 0x868 | PLAYER_BLOCK_STRIDE | player_stride_08061400 | ewram.inc | REUSE ewram.inc:250 |
| DWORD_080614fc | 0x1332 | BANISHER_OF_THE_LIGHT_CID | banisher_cid_080614fc | card_info.inc | REUSE card_info.inc:452 |
| DWORD_08061500 | 0x868 | PLAYER_BLOCK_STRIDE | player_stride_08061500 | ewram.inc | REUSE |
| DWORD_08061504 | 0x0201c510 | gDuelFieldSlots | gdfs_ref_08061504 | ewram.inc | REUSE ewram.inc:312 |
| DWORD_0806150c | 0x0201c600 | gP1FieldArrayCBase | gp1fac_ref_0806150c | ewram.inc | REUSE ewram.inc:364 |
| DWORD_08061538 | 0x868 | PLAYER_BLOCK_STRIDE | player_stride_08061538 | ewram.inc | REUSE |
| DWORD_08061578 | 0x0201bb90 | gEquipChainSlotRefs | gequip_ctx_ref_08061578 | ewram.inc | REUSE ewram.inc:315; plate calls it gDuelEffectCtx -> FIX plate |
| DWORD_080615c0 | 0x1332 | BANISHER_OF_THE_LIGHT_CID | banisher_cid_080615c0 | card_info.inc | REUSE |
| DWORD_080615c4 | 0x868 | PLAYER_BLOCK_STRIDE | player_stride_080615c4 | ewram.inc | REUSE |
| DWORD_080615c8 | 0x0201c5d8 | gDuelFieldSlots_p2_base | gdfs_p2_ref_080615c8 | ewram.inc | REUSE ewram.inc:341 |
| DWORD_080615cc | 0x10f4 | UMI_CARD_ID | umi_cid_080615cc | card_info.inc | REUSE card_info.inc:145 |
| DWORD_080616bc | 0x868 | PLAYER_BLOCK_STRIDE | player_stride_080616bc | ewram.inc | REUSE |
| DWORD_080616c0 | 0x0201c510 | gDuelFieldSlots | gdfs_ref_080616c0 | ewram.inc | REUSE |
| DWORD_080617a4 | 0x868 | PLAYER_BLOCK_STRIDE | player_stride_080617a4 | ewram.inc | REUSE |
| DWORD_080617a8 | 0x0201c510 | gDuelFieldSlots | gdfs_ref_080617a8 | ewram.inc | REUSE |
| DWORD_080617e8 | 0x0201bb90 | gEquipChainSlotRefs | gequip_ctx_ref_080617e8 | ewram.inc | REUSE; plate uses gDuelEffectCtx -> FIX |
| DWORD_0806186c | 0x868 | PLAYER_BLOCK_STRIDE | player_stride_0806186c | ewram.inc | REUSE |
| DWORD_08061870 | 0x0201c600 | gP1FieldArrayCBase | gp1fac_ref_08061870 | ewram.inc | REUSE |
| DWORD_080618ac | 0x868 | PLAYER_BLOCK_STRIDE | player_stride_080618ac | ewram.inc | REUSE |
| DWORD_080618b0 | 0x1b58 | LP_GAP_THRESHOLD_7000 | lp_gap_7000_080618b0 | ewram.inc | NEW; 0x1b58=7000 decimal; check_equip_slot_eligible_by_lp_gap_7000_vs_opponent plate confirms |
| DWORD_080619e0 | 0x0201bb90 | gEquipChainSlotRefs | gequip_ctx_ref_080619e0 | ewram.inc | REUSE; plate uses gDuelEffectCtx -> FIX |
| DWORD_080619e4 | 0x7cf | FIELD5_SCORE_THRESHOLD_1999 | score_thresh_1999_080619e4 | card_info.inc | REUSE card_info.inc:940 |
| DWORD_08061c0c | 0x868 | PLAYER_BLOCK_STRIDE | player_stride_08061c0c | ewram.inc | REUSE |
| DWORD_08061c5c | 0x13f2 | MASK_OF_RESTRICT_CID | mask_restrict_cid_08061c5c | card_info.inc | NEW; card-stats.s L11234 slot=0x13F2 pw=29549364 |
| DWORD_08061cbc | 0x0201bb90 | gEquipChainSlotRefs | gequip_ctx_ref_08061cbc | ewram.inc | REUSE |
| DWORD_08061dbc | 0x1cf4 | FIELD_STATE_OFF | field_state_off_08061dbc | duel_field.inc | REUSE duel_field.inc:205 |
| DWORD_08061dc0 | 0x178b | PROTECTOR_OF_SANCTUARY_CID | protector_sanctuary_cid_08061dc0 | card_info.inc | NEW; card-stats.s L20464 slot=0x178B pw=24221739 |
| DWORD_08061df8 | 0x868 | PLAYER_BLOCK_STRIDE | player_stride_08061df8 | ewram.inc | REUSE |
| DWORD_08061e8c | 0x868 | PLAYER_BLOCK_STRIDE | player_stride_08061e8c | ewram.inc | REUSE |
| DWORD_08061d74 | 0x080507ad | (fn-ptr literal) | zone_pair_pred_07ad_ptr_08061d74 | -- | RENAME-only; raw THUMB fn-ptr to check_equip_slot_eligible_by_type_query+1 (0x080507ac+1); EOL: "[fn-ptr] check_equip_slot_eligible_by_type_query+1" |
| DWORD_08061eb0 | 0x08051e95 | (fn-ptr literal) | zone_pair_pred_1e95_ptr_08061eb0 | -- | RENAME-only; raw THUMB fn-ptr to check_equip_slot_eligible_by_side_mismatch_and_prereqs+1 (0x08051e94+1); EOL: "[fn-ptr] check_equip_slot_eligible_by_side_mismatch_and_prereqs+1" |
| DAT_08061900 | 0x1cf4 | FIELD_STATE_OFF | field_state_off_08061900 | duel_field.inc | REUSE |
| DAT_08061934 | 0x868 | PLAYER_BLOCK_STRIDE | player_stride_08061934 | ewram.inc | REUSE |
| DAT_0806197c | 0x868 | PLAYER_BLOCK_STRIDE | player_stride_0806197c | ewram.inc | REUSE |
| DAT_080619b4 | 0x868 | PLAYER_BLOCK_STRIDE | player_stride_080619b4 | ewram.inc | REUSE |
| DAT_08061a08 | 0x1332 | BANISHER_OF_THE_LIGHT_CID | banisher_cid_08061a08 | card_info.inc | REUSE; plate of dispatch_effect_via_hand_slot_setcode calls this "Zera Ritual" WRONG -> FIX PLATE |
| DAT_08061ab8 | 0x868 | PLAYER_BLOCK_STRIDE | player_stride_08061ab8 | ewram.inc | REUSE |
| DAT_08061ad4 | 0x175b | BURST_STREAM_OF_DESTRUCTION_CID | burst_stream_cid_08061ad4 | card_info.inc | NEW; card-stats.s L20061 slot=0x175B pw=17655904 |
| DAT_08061adc | 0x0fa7 | BLUE_EYES_WHITE_DRAGON_CID | blue_eyes_cid_08061adc | card_info.inc | REUSE card_info.inc:415 |
| DAT_08061b08 | 0x0ff8 | RED_EYES_B_DRAGON_CID | red_eyes_cid_08061b08 | card_info.inc | REUSE card_info.inc:948 |
| DAT_08061b48 | 0x868 | PLAYER_BLOCK_STRIDE | player_stride_08061b48 | ewram.inc | REUSE |
| DAT_08061b90 | 0x175e | SANCTUARY_IN_THE_SKY_CID | sanctuary_cid_08061b90 | card_info.inc | NEW; card-stats.s L20087 slot=0x175E pw=56433456 (note: SANCTUARY_CID_SHIFTED exists at card_info.inc:367 but that is the shifted value 0xbaf00000, not the raw CID; this is NEW) |
| DAT_08061b98 | 0x868 | PLAYER_BLOCK_STRIDE | player_stride_08061b98 | ewram.inc | REUSE |
| DAT_08061d50 | 0x1332 | BANISHER_OF_THE_LIGHT_CID | banisher_cid_08061d50 | card_info.inc | REUSE; plate of check_zera_ritual_absent_from_field says "Zera Ritual" -> FUNC_RENAME + FIX PLATE |
| block+0x22 (0x08061c88) | 0x868 | PLAYER_BLOCK_STRIDE | player_stride_08061c88 | ewram.inc | REUSE; new slot from disasm |
| INFERNO_FIRE_BLAST_CID | 0x17f6 | INFERNO_FIRE_BLAST_CID | -- | card_info.inc | NEW; card-stats.s L21686 slot=0x17F6 pw=52684508; not a slot but embedded via `adds r0,#0x9b` in check_dragon_spell_target_slot_available (no literal pool slot, computed inline). Equate still useful for plate comment. |

**EQ count: 46 (13 DAT + 33 DWORD, including 2 fn-ptr RENAME-only slots)**

### REF_SLOTS (USER-label + DATA-ref)

| slot | target | gas_label | slot_label |
|---|---|---|---|
| DWORD_08061508 | gP1LifePoints | gP1LifePoints | gp1lp_ptr_08061508 |
| DWORD_08061868 | gP1LifePoints | gP1LifePoints | gp1lp_ptr_08061868 |
| DWORD_080618a8 | gP1LifePoints | gP1LifePoints | gp1lp_ptr_080618a8 |
| DWORD_08061c08 | gP1LifePoints | gP1LifePoints | gp1lp_ptr_08061c08 |
| DWORD_08061d34 | gP1LifePoints | gP1LifePoints | gp1lp_ptr_08061d34 |
| DWORD_08061db8 | gP1LifePoints | gP1LifePoints | gp1lp_ptr_08061db8 |
| DWORD_08061df4 | gP1LifePoints | gP1LifePoints | gp1lp_ptr_08061df4 |
| DWORD_08061e88 | gP1LifePoints | gP1LifePoints | gp1lp_ptr_08061e88 |
| DWORD_080613fc | gP1LifePoints | gP1LifePoints | gp1lp_ptr_080613fc |
| DWORD_08061618 | gP1LifePoints | gP1LifePoints | gp1lp_ptr_08061618 |
| PTR_gP1LifePoints_080618fc | gP1LifePoints | gP1LifePoints | gp1lp_ptr_080618fc |
| PTR_gP1LifePoints_08061978 | gP1LifePoints | gP1LifePoints | gp1lp_ptr_08061978 |
| PTR_gP1LifePoints_080619b0 | gP1LifePoints | gP1LifePoints | gp1lp_ptr_080619b0 |
| PTR_gP1LifePoints_08061ab4 | gP1LifePoints | gP1LifePoints | gp1lp_ptr_08061ab4 |
| PTR_gP1LifePoints_08061b44 | gP1LifePoints | gP1LifePoints | gp1lp_ptr_08061b44 |
| PTR_gP1LifePoints_08061b94 | gP1LifePoints | gP1LifePoints | gp1lp_ptr_08061b94 |
| DAT_08061abc | gP1ZoneHandCount | gP1ZoneHandCount | gp1zonehandcount_ref_08061abc |
| block+0x1e (0x08061c84) | gP1LifePoints | gP1LifePoints | gp1lp_ptr_08061c84 |

**REF count: 18 (10 DWORD + 6 PTR + 1 DAT + 1 new from disasm block)**

Note: The 10 DWORD_ + 6 PTR_ gP1LifePoints slots appear as RENAME in auto-name classification (since they already contain the symbol) but per R2 methodology they are REF_SLOTS (user-label on data-ref address). Total auto-named slots resolved = 63 + 2 new from disasm = 65. All 63 pre-existing slots accounted for: 44 EQ + 1 data-REF (DAT_08061abc) + 18 gP1LP REF (currently DWORD_/PTR_).

### RENAME_SLOTS (纯改名 + EOL)

| slot | slot_label | eol_ascii |
|---|---|---|
| DWORD_08061d74 | zone_pair_pred_07ad_ptr_08061d74 | [fn-ptr] check_equip_slot_eligible_by_type_query+1 |
| DWORD_08061eb0 | zone_pair_pred_1e95_ptr_08061eb0 | [fn-ptr] check_equip_slot_eligible_by_side_mismatch_and_prereqs+1 |

(All gP1LP DWORD_/PTR_ slots handled as REF_SLOTS above, not as pure RENAME.)

### FUNC_RENAME (误名订正)

| addr | old | new | indeg | 理由 |
|---|---|---|---|---|
| 0x08061d40 | check_zera_ritual_absent_from_field | check_banisher_of_light_absent_from_field | 0 | Function loads 0x1332 into r0 then calls count_field_copies_of_card. 0x1332 = BANISHER_OF_THE_LIGHT_CID per card-stats.s L9492 (Banisher of the Light pw=61528025). Zera Ritual has slot_id 0x1245 (card-stats.s L7113). Naming phase plate says "Zera Ritual (passcode=81756897)" -> wrong passcode and wrong card for CID 0x1332. Confidence: high. indeg=0 (plate confirms runtime dispatch only). |

### PLATE (R5)

Functions with CJK mojibake plates (python grep confirmed 20 non-ASCII lines in seg; full ASCII rewrites):

1. **check_equip_slot_eligible_neo_daedalus_with_lp_slot_effect** @0x08061660
   Full ASCII plate: "Equip slot activation eligibility predicate, two-level condition: (1) check_field_spell_neo_daedalus_group_placeable(player_id) == 0 return 0; (2) check_equip_slot_eligible_by_lp_slot_and_effect_dispatch(slot_ptr, arg) pass-through. Semantics: Neo Daedalus field group condition must be satisfied before evaluating LP slot effect dispatch eligibility."

2. **commit_equip_effect_node_zone_match** @0x08061688
   ASCII substring replace: no CJK in existing plate (plate is English) -- no action needed here, plate is already ASCII. Confirm by grep: lines 13951 plate text is English. (Skip full rewrite.)

3. **check_equip_slot_eligible_type480_with_neo_daedalus_field5_loop** @0x080617ac
   CJK at lines 14114-14124. Constants block also has "gDuelEffectCtx" -> fix to gEquipChainSlotRefs.
   Full ASCII plate: "Equip slot activation eligibility predicate, five-level condition: (1) slot[+2] halfword bits[10:6] must be 0x16 (zone_type mask 0xfc0 == 0x480, 0x90<<3); (2) slot[+0x14] must be nonzero; (3) gEquipChainSlotRefs[+0x4] (activation context player id) != player_id (direction check); (4) check_neo_daedalus_placement_eligible must pass; (5) loop over gP1FieldArrayCBase[player*PLAYER_BLOCK_STRIDE] entries (LP_LOOP_CEIL_OFF=0xc count bound): for each LP zone entry extracts 13-bit card_id, calls check_card_field5_is_nonzero; if nonzero calls eval_equip_placement_full_check(player_id, card_id, 0); if any pass returns 1. Returns 0 if all fail. Constants: ZONE_TYPE_MASK=0xfc0, ZONE_TYPE_480=0x480, LP_SLOT_ACTIVE_OFF=0x10, gEquipChainSlotRefs=0x0201bb90, LP_LOOP_CEIL_OFF=0xc, PLAYER_BLOCK_STRIDE=0x868."

4. **check_equip_slot_eligible_neo_daedalus_with_lp_status_lookup** @0x08061938
   CJK at lines 14363-14367.
   Full ASCII plate: "Equip slot activation eligibility predicate, two-level condition with early fast-path: (1) check_neo_daedalus_placement_eligible must pass else return 0; (2) read gP1LifePoints[player*PLAYER_BLOCK_STRIDE+LP_SLOT_ACTIVE_OFF(0x10)] (player LP status word); if nonzero return 1 (fast pass); if zero: call lookup_slot_display_value_by_card_id(slot_ptr)->r2, then dispatch_effect_handler_by_card_id(player_id, card_id, display_value); return 1 if dispatch nonzero else 0. Constants: PLAYER_BLOCK_STRIDE=0x868, LP_SLOT_ACTIVE_OFF=0x10."

5. **check_equip_slot_eligible_by_active_ctx_score_threshold** @0x080619c0
   CJK at lines 14446-14452. gDuelEffectCtx -> gEquipChainSlotRefs.
   Full ASCII plate: "Equip slot activation eligibility predicate, two-level condition: (1) check_equip_slot_state_active_with_card_present must pass else return 0; (2) load gEquipChainSlotRefs[+0x4] (activation context player id) and [+0x20] (context zone_idx); call get_slot_field6_score(player_id, zone_idx); if score > FIELD5_SCORE_THRESHOLD_1999(0x7cf=1999) return 1 else return 0. Semantics: equip slot active and activation context target zone field6 score exceeds 1999. Constants: gEquipChainSlotRefs=0x0201bb90, offset+0x4=activation_player, offset+0x20=context_zone_idx, FIELD5_SCORE_THRESHOLD_1999=0x7cf."

6. **dispatch_effect_via_hand_slot_setcode** @0x080619f0
   Existing plate has "Zera Ritual (passcode=81756897)" for CID 0x1332 -- WRONG. CID 0x1332 = Banisher of the Light. ASCII rewrite correcting this:
   "Step 1: count_field_copies_of_card(BANISHER_OF_THE_LIGHT_CID=0x1332) -- Banisher of the Light (pw=61528025). If > 0 -> return 0 (Banisher on field blocks activation). Step 2: read hand_count from gP1LifePoints[player*PLAYER_BLOCK_STRIDE+LP_LOOP_CEIL_OFF(0xc)]. Iterate hand slots (index 0..hand_count-1): - read zone descriptor from gP1FieldArrayCBase[player*stride+zone_idx*4]; extract bits[23:16] then <<1 -> zone_setcode. - read slot[+4] bits[14:8] (7-bit set_code) -> slot_setcode. - if zone_setcode == slot_setcode: dispatch_effect_handler_by_card_id(player_id, card_id, zone_idx). If dispatch returns nonzero -> return 1. Returns 0 if loop exhausted without match or Banisher present. Called by 6+ callers; core hand-slot set_code matching logic."

7. **check_equip_slot_eligible_zone_e_type580_with_neo_daedalus** @0x08061cc8
   CJK at line 14949.
   Full ASCII plate: "Equip slot activation eligibility predicate, five-level condition: (1) slot[+2] halfword bits[10:6] must be 0x16 (zone_type mask 0xfc0 == 0x580, 0xb0<<3); (2) slot[+0x14] bit9 (lsls#0x16/lsrs#0x1f) must equal 1-player_id (direction check); (3) slot[+0x14] bits[22:19] must be 0xe (zone E index); (4) read gP1LifePoints zone card_id, call check_card_field5_is_nonzero; (5) slot[+0x14] bits[8:0] bit0 must equal 1-player_id (second direction check); all pass: call check_neo_daedalus_placement_eligible(slot_ptr, arg) and return its value. Sibling of check_equip_slot_eligible_field_spell_effect_type_e_with_zone_field5 with added fifth check and Neo Daedalus call. Constants: ZONE_TYPE_MASK=0xfc0, ZONE_TYPE_FIELD_SPELL=0x580, ZONE_E_INDEX=0xe, LP_ZONE_OFFSET=0x10e0 (0x87<<5), PLAYER_BLOCK_STRIDE=0x868."

8. **check_equip_slot_eligible_by_lp_status_tier3_neo_daedalus** @0x08061dcc
   CJK at lines 15119-15124.
   Full ASCII plate: "Equip slot activation eligibility predicate, two-level condition: (1) read gP1LifePoints[player*PLAYER_BLOCK_STRIDE+LP_SLOT_ACTIVE_OFF(0x10)] (player LP status word); if <= 3 return 0 (bls path); (2) check_neo_daedalus_placement_eligible(slot_ptr, arg) pass-through. Semantics: LP status word must be > 3 to proceed to Neo Daedalus placement check. Isomorphic to check_equip_slot_eligible_by_duel_phase3_neo_daedalus (0x08060484) but threshold > 3 vs == 3. Constants: PLAYER_BLOCK_STRIDE=0x868, LP_SLOT_ACTIVE_OFF=0x10."

9. **check_equip_slot_eligible_chain_present_with_lp_status_neo_daedalus** @0x08061e50
   CJK at lines 15210-15213.
   Full ASCII plate: "Equip slot activation eligibility predicate, three-level condition: (1) check_value_in_slot_chain(player_id, card_id, CHAIN_TYPE=0xb) -- if chain node absent return 0; (2) read gP1LifePoints[player*PLAYER_BLOCK_STRIDE+LP_SLOT_ACTIVE_OFF(0x10)] (LP status word) -- if zero return 0; (3) check_neo_daedalus_placement_eligible(slot_ptr, arg) pass-through. Semantics: equip chain already contains target value AND LP status nonzero before evaluating Neo Daedalus condition. Constants: CHAIN_TYPE=0xb, PLAYER_BLOCK_STRIDE=0x868, LP_SLOT_ACTIVE_OFF=0x10."

**Additional non-CJK plate fixes (gDuelEffectCtx name error):**

10. **check_equip_slot_eligible_field_spell_with_effect_context_zone_val10** @0x0806153c
    Existing plate uses "EFFECT_CTX_BASE=0x0201bb90" (ok) and "gDuelEffectCtx" label. Fix to gEquipChainSlotRefs. ASCII plate:
    "Equip slot activation eligibility predicate, three-level condition: (1) slot[+2] halfword bits[10:6] must be 0x16 (zone_type mask 0xfc0 == 0x580, 0xb0<<3); (2) read slot[+0x14] bits[8:0] and compare with gEquipChainSlotRefs[+0x70]; if match use offset=0x88, else use offset=0x50; (3) read gEquipChainSlotRefs[+offset], if == 0xa (10) return 1 else return 0. Constants: SPELL_TYPE_MASK=0xfc0, FIELD_SPELL_TYPE=0x580, gEquipChainSlotRefs=0x0201bb90, CTX_ZONE_REF_OFF=0x70, CTX_SLOT_MATCH_OFF=0x88, CTX_SLOT_NOMATCH_OFF=0x50, EXPECTED_VAL=0xa."

11. **check_zera_ritual_absent_from_field** plate (now renamed to check_banisher_of_light_absent_from_field):
    ASCII plate: "Void-param predicate: r0 overwritten at entry by ldr DAT_08061d50=BANISHER_OF_THE_LIGHT_CID(0x1332=Banisher of the Light, pw=61528025). Calls count_field_copies_of_card(0x1332). Returns 1 if count==0 (absent); 0 if any copy present. Inverse of Banisher presence check. Distinct from check_equip_slot_eligible_banisher_absent_with_umi_pair which also checks Umi pairing."

**Total PLATE: 11 (7 CJK full rewrites + 3 gEquipChainSlotRefs name-error fixes + 1 post-FUNC_RENAME)**

---

## carve 計画 (R7)

ROM_INCBIN 0x61c66/0x2a is classified as R4 disasm (see Data Block section). No carve operations.

---

## disasm 計画 (R4)

**Block: 0x08061c66..0x08061c90 (0x2a bytes)**

- Target: ROM_INCBIN 0x61c66, 0x2a
- clearListing 0x08061c66..0x08061c8f -> setTMode 0x08061c66
- `.zero 2` at 0x08061c66 (align pad -- keep as data, clearListing only covers code part)
- DisassembleCommand 0x08061c68 (fn entry, 28 bytes body+pool+return)
- createFunction 0x08061c68 name: check_player_lp_status_nonzero_for_cid_1776
- createDWord 0x08061c84 (literal pool gP1LifePoints) -> slot gp1lp_ptr_08061c84
- createDWord 0x08061c88 (literal pool 0x868) -> slot player_stride_08061c88
- Plate (ASCII): "fn_eligible for CID 0x1776 (Corpse of Yata-Garasu, pw=30461781); reached via card effect handler dispatch table at ROM 0x09e4204c. Reads player LP status word gP1LifePoints[player*PLAYER_BLOCK_STRIDE+LP_SLOT_ACTIVE_OFF(0x10)]; if nonzero returns 2, if zero returns 0. indeg=0; runtime-only via fn-ptr."

**Expected: 1 new function from disasm**

---

## 新増 constants / 全局

C5 双向核 -- all reuse verified by grep, new items grep returns 0 hits in constants/:

### card_info.inc 新增 (7 items):
```
.equ REVERSAL_OF_GRAVES_CID,         0x00014f0  @ Reversal of Graves (pw=17484499; card-stats.s L13743 slot=0x14F0)
.equ BLASTING_THE_RUINS_CID,         0x000016dc  @ Blasting the Ruins (pw=21466326; card-stats.s L18696 slot=0x16DC)
.equ BURST_STREAM_OF_DESTRUCTION_CID, 0x0000175b @ Burst Stream of Destruction (pw=17655904; card-stats.s L20061)
.equ SANCTUARY_IN_THE_SKY_CID,       0x0000175e  @ The Sanctuary in the Sky (pw=56433456; card-stats.s L20087); note SANCTUARY_CID_SHIFTED(0xbaf00000) already exists at card_info.inc:367 but that is CID<<19 not raw CID
.equ INFERNO_FIRE_BLAST_CID,         0x000017f6  @ Inferno Fire Blast (pw=52684508; card-stats.s L21686 slot=0x17F6); used inline via adds r0,#0x9b from 0x175b in check_dragon_spell_target_slot_available; plate reference only
.equ PROTECTOR_OF_SANCTUARY_CID,     0x0000178b  @ Protector of the Sanctuary (pw=24221739; card-stats.s L20464 slot=0x178B)
.equ MASK_OF_RESTRICT_CID,           0x000013f2  @ Mask of Restrict (pw=29549364; card-stats.s L11234 slot=0x13F2)
```

### ewram.inc 新増 (1 item):
```
.equ LP_GAP_THRESHOLD_7000,          0x00001b58  @ LP gap threshold 7000 (0x1b58=7000 decimal); check_equip_slot_eligible_by_lp_gap_7000_vs_opponent: opponent_LP must exceed player_LP by at least 7000
```

---

## §5.1 登记 (Rule 3) -- 0 引用块

None. The only ROM_INCBIN block (0x61c66/0x2a) has confirmed THUMB+1 reference and is classified R4 disasm.

---

## 消費者証拠 (R6) -- 関键槽語義

| slot/fn | semantics | evidence | confidence |
|---|---|---|---|
| DWORD_080613cc = 0x14f0 | Reversal of Graves CID | plate text + card-stats.s L13743 slot=0x14F0 pw=17484499 | high |
| DWORD_080613d0 = 0x16dc | Blasting the Ruins CID | plate text + card-stats.s L18696 slot=0x16DC pw=21466326 | high |
| DWORD_080618b0 = 0x1b58 | LP gap threshold 7000 | plate confirms "7000 higher than player LP"; 0x1b58=7000 decimal | high |
| DWORD_08061d74 = 0x080507ad | fn-ptr to check_equip_slot_eligible_by_type_query+1 | asm/05_equip_eligibility_a.s L16635: push at 0x080507ac; 0x080507ac+1=0x080507ad | high |
| DWORD_08061eb0 = 0x08051e95 | fn-ptr to check_equip_slot_eligible_by_side_mismatch_and_prereqs+1 | asm/05_equip_eligibility_a.s L20122: push at 0x08051e94; 0x08051e94+1=0x08051e95 | high |
| 0x0201bb90 (gEquipChainSlotRefs) in 5 DWORD slots | equip chain activation context struct | ewram.inc:315 confirms gEquipChainSlotRefs=0x0201bb90; plates call it gDuelEffectCtx which is the WRONG name (Seg-6 already corrected gDuelEffectCtx->gEquipChainSlotRefs for same addr) | high |
| DAT_08061abc = 0x0201c4ec | gP1ZoneHandCount (hand count per player) | ewram.inc:232 confirms gP1ZoneHandCount=0x0201c4ec = gP1LifePoints+0xc; used as [base+player*0x868] in loop bound check in dispatch_effect_via_hand_slot_setcode | high |
| check_zera_ritual -> check_banisher_of_light | CID 0x1332 = Banisher of the Light | card-stats.s L9492 slot=0x1332 pw=61528025; Zera Ritual = 0x1245 (card-stats.s L7113) | high |
| block+0x02 = fn for CID 0x1776 | Corpse of Yata-Garasu fn_eligible | handler table at ROM 0x09e4204c: +0=0x1776 CID; +12=0x08061c69 fn_eligible ptr; python-verified | high |

---

## 求助

None. All semantics confirmed at high confidence.

---

## 自検 (Phase 4)

1. **EQ value vs ROM bytes**: spot-checks performed via python struct.unpack on file offsets; DWORD_080613cc at file 0x613cc: bytes f0140000 = 0x000014f0 correct. DWORD_080618b0 at 0x618b0: bytes 581b0000 = 0x00001b58 = 7000 correct.
2. **disasm fn-ptr +1**: block THUMB+1 ptr 0x08061c69 = 0x08061c68+1 (fn_eligible entry) confirmed; ROM at 0x09e42058: value 0x08061c69 = packed bytes 691c0608.
3. **All plate/EOL text pure ASCII**: grep [^\x00-\x7F] on all plate text in this proposal = 0 hits. All CJK in original plates flagged for full rewrite.
4. **§5.1 block 0-ref**: N/A (no §5.1 blocks; only block has THUMB+1 ref).
5. **Slot names**: all slot labels use hex suffix (_08061xxx) to avoid collision; fn-ptr slots use descriptive prefix (zone_pair_pred_*).
6. **C5 double-check**: REVERSAL_OF_GRAVES_CID/BLASTING_THE_RUINS_CID/BURST_STREAM_OF_DESTRUCTION_CID/SANCTUARY_IN_THE_SKY_CID/INFERNO_FIRE_BLAST_CID/PROTECTOR_OF_SANCTUARY_CID/MASK_OF_RESTRICT_CID/LP_GAP_THRESHOLD_7000 all grep constants/ 0 hits (confirmed absent). SANCTUARY_IN_THE_SKY_CID: note SANCTUARY_CID_SHIFTED(0xbaf00000) exists but that is the shifted form 0x175e<<19; the raw CID 0x175e is NEW (0 hits for "0x0000175e" in constants/).
