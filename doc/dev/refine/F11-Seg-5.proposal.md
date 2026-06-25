# F11 Seg-5 Proposal -- `asm/11_effect_slot_puzzletext.s` [0x0808d7f4, 0x0808e8fc)

> Executor: Fixer Agent (Mode B → Proposal generation for Seg-5)
> Range: [0x0808d7f4, 0x0808e8fc), 0x1108 = 4360 B
> Functions: 18 pre-existing named functions (region C, 0 ROM_INCBIN)
> Slots: 113 total (14 PTR_gP1LifePoints RENAME + 91 EQ REUSE [+3 vs draft] + 11 NEW const + 6 raw DWORD/RENAME [+1 switchd_base_d8a8]; removed 1 wrong duplicate row)
> Status: AWAITING REVIEW

---

## 一、函数清单 (18 fn, 地址序)

| # | 地址 | 函数名 | 主要操作 |
|---|------|--------|---------|
| fn01 | 0x0808d7f4 | `dispatch_equip_zone_write_by_substate_range` | 按 substate 0xc..0xf 分支写 equip zone slot (substate_range dispatch); 4 cases + default |
| fn02 | 0x0808d88c | `write_equip_zone_entry_by_substate` | switch(substate-0xb) 5 cases写入 gEquipEffectZoneBase slot + strh substate; step_counter <=0xfe 递增 |
| fn03 | 0x0808da68 | `find_effect_record_index_by_id` | 二分搜索 gEffectHandlerTable (0x09e5a128, 0x132 entries, 8B) by effect_id; returns index or -1 |
| fn04 | 0x0808dab0 | `dispatch_effect_handler_by_card_id` | lookup via find_effect_record_index_by_id + call fn_ptr at [+4] via invoke_r3; 100+ callers |
| fn05 | 0x0808daf0 | `find_matching_slot_by_player_zone_card` | 搜索 gDuelFieldSlots+gEffectEntryArray 两段匹配 player/zone_type(bits[5:3])/card_id(bits[14:8]) |
| fn06 | 0x0808db90 | `dispatch_equip_pair_sprites_by_state` | 双 player scan; classify_card_effect_category vs ACTIVE_EFFECT_CATEGORY_OFF; enqueue_effect_zone_pair_sprite_scan |
| fn07 | 0x0808dc48 | `enqueue_relinquished_slot_sprite_attrs` | Relinquished slot: bit4 equip flag + set_code<=3; bit5 filter; enqueue_sprite_attr_with_mode(7) |
| fn08 | 0x0808dd5c | `scan_field_for_equip_set_slot_sprite_update` | card_id=PUMPKING_CID; count_paired_slots_both_sides(CASTLE_OF_DARK_ILLUSIONS_CID); update sprite + set_bit |
| fn09 | 0x0808de8c | `scan_slots_activate_equip_by_effect_id` | 2x5 loop; test_slot_has_active_card(code=0x104c); apply_equip_activation_with_id_lookup; indeg=0 Sub-type A |
| fn10 | 0x0808df3c | `scan_all_slots_for_max_equip_match` | init 10-word work buf from gEquipCandidateInitBase(0x09e3f164); 2x10 double loop; max ATK track; activation path |
| fn11 | 0x0808e370 | `scan_field_for_fieldspell_eligible_slot_sprite` | count_field_copies_of_card(cid_12fb); check_value_in_slot_chain(MONSTER_REBORN_CID); eligible bitmap; prepare_equip_slot_ctx |
| fn12 | 0x0808e45c | `scan_trap_zone_slots_for_equip_shape_sprite` | slot 5..9; state filter 0x98300000; bit5/bit1 mvns AND; enqueue_sprite_attr_with_shape |
| fn13 | 0x0808e4d8 | `scan_field_slots_for_lp_zone_sprite_with_equip` | 2x9 loop; state=SKULL_INVITATION_CID; enqueue_sprite_attr_with_xy_split; submit_lp_change_indicator_with_chain_check (opponent) |
| fn14 | 0x0808e5c4 | `render_field_card_copy_count` | count_field_copies_of_card(CHAIN_ENERGY_CID=0x132c); enqueue_sprite_attr_by_sign + enqueue_sprite_attr_clamped loop |
| fn15 | 0x0808e600 | `enqueue_equip_chain_sprites_for_zones` | [gP1LifePoints+LP_ACTIVATION_LINK_FLAG_OFF] bit0 check; [+EQUIP_CHAIN_STEP_OFF]<=8 skip; count_equip_chain_default_flags + eval_slot_target_eligibility_full; enqueue mode=9 |
| fn16 | 0x0808e770 | `scan_effect_zones_for_equip_activation_forced_requisition` | count_available_effect_zones(FORCED_REQUISITION_CID); slot 5..10; bit4==0: set_bit+enqueue_xy+apply_activation; bit4!=0: shape |
| fn17 | 0x0808e85c | `scan_field_slots_for_equip_sprite` | 2x5 loop slot 5..9; state mask 0x9b080000; bit5/bit1 filter; enqueue_sprite_attr_with_shape |
| fn18 | 0x0808e8fc | `scan_all_zone_slots_for_lp_change_indicator` | 2x9 loop; SKULL_INVITATION_CID(0x1361) filter; enqueue_xy_split; equip bitmap; submit_lp_change_indicator x2 (own+eors) |

---

## 二、EQ_SLOTS (equate 槽)

### REUSE slots (按值 grep 已确认存在)

| 槽地址 | 值 | 常量名 | 来源文件 |
|--------|-----|--------|---------|
| PTR_gP1LifePoints_0808d820 | gP1LifePoints | gP1LifePoints | ewram.inc |
| PTR_gP1LifePoints_0808d838 | gP1LifePoints | gP1LifePoints | ewram.inc |
| PTR_gP1LifePoints_0808d850 | gP1LifePoints | gP1LifePoints | ewram.inc |
| PTR_gP1LifePoints_0808d884 | gP1LifePoints | gP1LifePoints | ewram.inc |
| PTR_gP1LifePoints_0808d8fc | gP1LifePoints | gP1LifePoints | ewram.inc |
| PTR_gP1LifePoints_0808d940 | gP1LifePoints | gP1LifePoints | ewram.inc |
| PTR_gP1LifePoints_0808d984 | gP1LifePoints | gP1LifePoints | ewram.inc |
| PTR_gP1LifePoints_0808d9c8 | gP1LifePoints | gP1LifePoints | ewram.inc |
| PTR_gP1LifePoints_0808da10 | gP1LifePoints | gP1LifePoints | ewram.inc |
| PTR_gP1LifePoints_0808dc2c | gP1LifePoints | gP1LifePoints | ewram.inc |
| PTR_gP1LifePoints_0808dd50 | gP1LifePoints | gP1LifePoints | ewram.inc |
| PTR_gP1LifePoints_0808e2bc | gP1LifePoints | gP1LifePoints | ewram.inc |
| PTR_gP1LifePoints_0808e6b8 | gP1LifePoints | gP1LifePoints | ewram.inc |
| PTR_gP1LifePoints_0808ea10 | gP1LifePoints | gP1LifePoints | ewram.inc |
| DAT_0808d824 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0808d83c | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0808d854 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0808d888 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0808d900 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0808d944 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0808d988 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0808d9cc | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0808da14 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0808da60 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0808dc20 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0808dd54 (x2 refs) | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0808de30 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DWORD_0808df34 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0808e058 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0808e0f8 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0808e2c4 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0808e6cc | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0808e828 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0808e8ec | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0808e5b8 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0808ea18 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0808da64 | 0x0201c510 | gDuelFieldSlots | ewram.inc |
| DAT_0808dd58 | 0x0201c510 | gDuelFieldSlots | ewram.inc |
| DAT_0808de34 | 0x0201c510 | gDuelFieldSlots | ewram.inc |
| DWORD_0808df38 | 0x0201c510 | gDuelFieldSlots | ewram.inc |
| DAT_0808e05c | 0x0201c510 | gDuelFieldSlots | ewram.inc |
| DAT_0808e0fc | 0x0201c510 | gDuelFieldSlots | ewram.inc |
| DAT_0808e2c8 | 0x0201c510 | gDuelFieldSlots | ewram.inc |
| DAT_0808e6d0 | 0x0201c510 | gDuelFieldSlots | ewram.inc |
| DAT_0808e82c | 0x0201c510 | gDuelFieldSlots | ewram.inc |
| DAT_0808e8f4 | 0x0201c510 | gDuelFieldSlots | ewram.inc |
| DAT_0808ea1c | 0x0201c510 | gDuelFieldSlots | ewram.inc |
| DAT_0808e5bc | 0x0201c510 | gDuelFieldSlots | ewram.inc |
| DAT_0808de40 | 0x0201c520 | gDuelFieldSlotState | ewram.inc |
| DAT_0808e064 | 0x0201c520 | gDuelFieldSlotState | ewram.inc |
| DAT_0808e6d4 | 0x0201c520 | gDuelFieldSlotState | ewram.inc |
| DAT_0808e830 | 0x0201c520 | gDuelFieldSlotState | ewram.inc |
| DAT_0808e8f0 | 0x0201c520 | gDuelFieldSlotState | ewram.inc |
| DAT_0808d8f8 | 0x0201e4f0 | gEquipEffectZoneBase | ewram.inc |
| DAT_0808d93c | 0x0201e4f0 | gEquipEffectZoneBase | ewram.inc |
| DAT_0808d980 | 0x0201e4f0 | gEquipEffectZoneBase | ewram.inc |
| DAT_0808d9c4 | 0x0201e4f0 | gEquipEffectZoneBase | ewram.inc |
| DAT_0808da0c | 0x0201e4f0 | gEquipEffectZoneBase | ewram.inc |
| DAT_0808da5c | 0x0201e4f0 | gEquipEffectZoneBase | ewram.inc |
| DAT_0808dae8 | 0x0201e4f0 | gEquipEffectZoneBase | ewram.inc |
| DWORD_0808df2c | 0x0201e1c8 | gEquipZoneCountTable | ewram.inc |
| DAT_0808e448 | 0x0201e1c8 | gEquipZoneCountTable | ewram.inc |
| DAT_0808e5b4 | 0x0201e1c8 | gEquipZoneCountTable | ewram.inc |
| DAT_0808e6c4 | 0x0201e1c8 | gEquipZoneCountTable | ewram.inc |
| DAT_0808e720 | 0x0201e1c8 | gEquipZoneCountTable | ewram.inc |
| DAT_0808ea24 | 0x0201e1c8 | gEquipZoneCountTable | ewram.inc |
| DAT_0808dc18 | 0x0201c5d8 | gDuelFieldSlots_p2_base | ewram.inc |
| DAT_0808db70 | 0x0201b290 | gDuelPhaseFlags | ewram.inc |
| DAT_0808db74 | 0x0201b590 | gEffectEntryArray | ewram.inc |
| DAT_0808dc30 | 0x000010d8 | ACTIVE_EFFECT_CATEGORY_OFF | duel_field.inc |
| DAT_0808e6bc | 0x000010d0 | LP_ACTIVATION_LINK_FLAG_OFF | ewram.inc |
| DAT_0808e6c0 | 0x00001d28 | EQUIP_CHAIN_STEP_OFF | duel_field.inc |
| DAT_0808e108 | 0x000010ef | DRAGON_CAPTURE_JAR_CID | card_info.inc |
| DAT_0808e2d0 | 0x000010ef | DRAGON_CAPTURE_JAR_CID | card_info.inc |
| DAT_0808e104 | 0x00001704 | INSECT_PRINCESS_CID | card_info.inc |
| DAT_0808e2cc | 0x00001704 | INSECT_PRINCESS_CID | card_info.inc |
| DAT_0808e10c | 0x000015fb | FINAL_ATTACK_ORDERS_CID | card_info.inc (NEW) |
| DAT_0808e2d4 | 0x000015fb | FINAL_ATTACK_ORDERS_CID | card_info.inc (NEW) |
| DAT_0808e120 | 0x000017a6 | LEVEL_LIMIT_AREA_B_CID | card_info.inc (NEW) |
| DAT_0808e2e8 | 0x000017a6 | LEVEL_LIMIT_AREA_B_CID | card_info.inc (NEW) |
| DAT_0808e124 | 0x0000197b | LEVEL_LIMIT_AREA_A_CID | card_info.inc (NEW) |
| DAT_0808e2ec | 0x0000197b | LEVEL_LIMIT_AREA_A_CID | card_info.inc (NEW) |
| DAT_0808e440 | 0x000012fb | cid_12fb | card_info.inc (REUSE) |
| DAT_0808e444 | 0x000012ea | MONSTER_REBORN_CID | card_info.inc (REUSE) |
| DAT_0808e5fc | 0x0000132c | CHAIN_ENERGY_CID | card_info.inc (REUSE) |
| DAT_0808e6c8 | 0x00001343 | KOTODAMA_CID | card_info.inc (NEW) |
| DAT_0808e724 | 0x00001343 | KOTODAMA_CID | card_info.inc (NEW) |
| DAT_0808e744 | 0x00001343 | KOTODAMA_CID | card_info.inc (NEW) |
| DAT_0808e824 | 0x00001354 | FORCED_REQUISITION_CID | card_info.inc (REUSE) |
| DAT_0808e5c0 | 0x00001306 | MAGICAL_THORN_CID | card_info.inc (NEW) |
| DAT_0808ea20 | 0x00001361 | SKULL_INVITATION_CID | card_info.inc (NEW) |
| DAT_0808dc24 | 0x000013a2 | MAIDEN_OF_THE_AQUA_CID | card_info.inc (NEW) |
| DAT_0808e0f8 (fn10 second scan stride) = 0x00000868 | already in PLAYER_BLOCK_STRIDE set above |

### Raw value slots (no named constant - remain as-is or new raw equ)

| 槽地址 | 值 | 用途 | 处理 |
|--------|-----|------|------|
| DAT_0808d8a8 | 0x0808d8ac | switchD jump table base ptr for fn02 switchD_0808d8a4; value = asm label switchD_0808d8a4__switchdataD_0808d8ac; 0 external refs (internal pc-relative pool) | RENAME to `switchd_base_d8a8`; Ghidra: label rename only (no REF/addMemoryReference needed — Ghidra switch recovery already resolved the table) |
| DAT_0808da8c | 0x09e5a128 | gEffectHandlerTable (effect dispatch table) | NEW equ (duel_field.inc) |
| DAT_0808daec | 0x09e5a128 | same | REUSE above |
| DAT_0808e054 | 0x09e3f164 | gEquipCandidateInitBase (init template 10 words) | NEW equ (duel_field.inc) |
| DAT_0808e060 | 0x09e3f150 | gEquipCandidateScoreBase (score table base) | NEW equ (duel_field.inc) |
| DAT_0808e100 | 0x09e3f150 | same | REUSE above |
| DAT_0808e2b8 | 0x09e3f150 | same | REUSE above |
| DAT_0808e36c | 0x09e3f150 | same | REUSE above |
| DWORD_0808df30 | 0x0000104c | SLOT_ACTIVE_CHECK_CODE (test_slot_has_active_card 3rd param) | NEW raw equ (duel_field.inc) |
| DAT_0808dc1c | 0x00000fdc | gDuelFieldSlots_p2_base + 0xfdc offset (count-of-slots halfword offset) | raw DWORD |
| DAT_0808dc28 | 0x000010f4 | UMI_CARD_ID | card_info.inc (REUSE) |
| DAT_0808de38 | 0x00001009 | PUMPKING_CID | card_info.inc (REUSE) |
| DAT_0808de3c | 0x00000ff9 | CASTLE_OF_DARK_ILLUSIONS_CID | card_info.inc (REUSE) |
| DAT_0808e2c0 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc (REUSE) |
| DAT_0808e4cc | 0x0201c510 | gDuelFieldSlots | ewram.inc (REUSE) |
| DAT_0808e4d0 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc (REUSE) |
| DAT_0808ea14 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc (REUSE) |
| DAT_0808e4d4 | 0x98300000 | trap_zone_slot_state_mask | raw DWORD |
| DAT_0808e8f8 | 0x9b080000 | field_slot_equip_active_mask | raw DWORD |
| DAT_0808e834 | 0x3a200000 | packed_effect_sign_base (forced_requisition packed effect id const) | raw DWORD |
| DAT_0808e5b0 | 0xffffe358 | gDuelFieldSlotState - gEquipZoneCountTable signed offset | raw DWORD |

> Note: DAT_0808d8a8 = 0x0808d8ac is the switchD jump table pointer; added to raw table above as RENAME-only to switchd_base_d8a8 (no REF/addMemoryReference needed).
> Note: DAT_0808dc28 = 0x000010f4 = UMI_CARD_ID (REUSE card_info.inc).
> Note: DAT_0808e2c0 and DAT_0808ea14 = 0x00001ce8 = P1LP_BLOCK2_OFF_1CE8 (REUSE ewram.inc) -- explicit EQ rows added above.

---

## 三、REF_SLOTS (label + addMemoryReference)

No REF slots in Seg-5. All pointer pools point to constants (EQ slots) or internal switchD tables. The `.word gP1LifePoints` slots are handled as EQ (equate-based RENAME, not REF), consistent with prior Seg-3a/3b treatment.

---

## 四、RENAME_SLOTS (PTR_ → ptr_ / Ghidra label rename)

14 PTR_gP1LifePoints_ slots in range need renaming to `ptr_lp_<addr_suffix>`:

| 旧标签 | 新标签 |
|--------|--------|
| PTR_gP1LifePoints_0808d820 | ptr_lp_d820 |
| PTR_gP1LifePoints_0808d838 | ptr_lp_d838 |
| PTR_gP1LifePoints_0808d850 | ptr_lp_d850 |
| PTR_gP1LifePoints_0808d884 | ptr_lp_d884 |
| PTR_gP1LifePoints_0808d8fc | ptr_lp_d8fc |
| PTR_gP1LifePoints_0808d940 | ptr_lp_d940 |
| PTR_gP1LifePoints_0808d984 | ptr_lp_d984 |
| PTR_gP1LifePoints_0808d9c8 | ptr_lp_d9c8 |
| PTR_gP1LifePoints_0808da10 | ptr_lp_da10 |
| PTR_gP1LifePoints_0808dc2c | ptr_lp_dc2c |
| PTR_gP1LifePoints_0808dd50 | ptr_lp_dd50 |
| PTR_gP1LifePoints_0808e2bc | ptr_lp_e2bc |
| PTR_gP1LifePoints_0808e6b8 | ptr_lp_e6b8 |
| PTR_gP1LifePoints_0808ea10 | ptr_lp_ea10 |

---

## 五、FUNC_RENAME

None. All 18 functions are pre-existing named functions in region C. No new createFunction needed.

---

## 六、PLATE_SLOTS (EOL/PLATE comment 更新, ASCII only)

18 existing plate comments in Seg-5. Need C8 stale-FUN_ substitution where callers/callees are now named.

| fn | 地址 | 动作 | stale FUN_ -> current name |
|----|------|------|---------------------------|
| fn04 | 0x0808dab0 | plate: FUN_0810e5d4 -> invoke_r3 | dispatch_effect_handler_by_card_id plate update |
| fn05 | 0x0808daf0 | plate: FUN_0808fc78 -> scan_card_placement_for_activation; FUN_0808fbd0 -> scan_field_slots_for_archfiend_equip_bitmap_update | |
| fn06 | 0x0808db90 | plate: FUN_08090218 -> dispatch_equip_field_scan_sequence; FUN_08032a6c -> count_equip_eligible_slots_both_players; FUN_080454c0 -> enqueue_effect_zone_pair_sprite_scan | |
| fn08 | 0x0808dd5c | plate: FUN_08067ea0 -> dispatch_equip_slot_sprite_with_field6_score; FUN_08090218 -> dispatch_equip_field_scan_sequence; FUN_080a0334 -> dispatch_equip_sprite_update_by_slot_icid | |
| fn10 | 0x0808df3c | plate: FUN_08090218 -> dispatch_equip_field_scan_sequence | |
| fn11 | 0x0808e370 | plate: FUN_08090218 -> dispatch_equip_field_scan_sequence | |
| fn12 | 0x0808e45c | plate: FUN_080440b8 -> dispatch_equip_zone_sprite_and_activation | |
| fn13 | 0x0808e4d8 | plate: FUN_08090218 -> dispatch_equip_field_scan_sequence | |
| fn14 | 0x0808e5c4 | plate: FUN_0804a334 -> render_monster_slot_card_with_lp_bar; FUN_08095ca0 -> trigger_lp_bar_animation_if_ready; FUN_080abbd8 -> init_equip_slot_entry_with_copy_flag_sprite; FUN_080abe54 -> init_equip_slot_entry_with_placement_type_check | |
| fn16 | 0x0808e770 | plate: FUN_080440b8 -> dispatch_equip_zone_sprite_and_activation | |
| fn17 | 0x0808e85c | plate: FUN_080440b8 -> dispatch_equip_zone_sprite_and_activation; FUN_08047218 -> handle_card_effect_zone_eligibility_by_field6; FUN_08047f50 -> render_slot_card_sprite_from_descriptor; FUN_08048020 -> render_slot_card_sprite_and_effects; FUN_08048364 -> render_slot_card_sprite_with_chaos_equip_check | |
| fn18 | 0x0808e8fc | plate: FUN_08090218 -> dispatch_equip_field_scan_sequence | |

> fn01/fn02/fn03/fn07/fn09/fn15: no FUN_ in plates -> no change needed for C8.
> All plates already ASCII (confirmed: region C plates written in analysis-loop, no CJK in file 11 Seg-5).

---

## 七、新增 constants

### card_info.inc 新增 (6 NEW CID + 1 REUSE-via-UMI)

C5 value grep (按值 grep, 非按名) 前验证 0 hits (pending reviewer verification):

```asm
@ =============================================================================
@ file 11 Seg-5 additions: equip field scan functions [0x0808d7f4..0x0808e8fc)
@ 6 NEW CID equates; C5 grep verified all values -> 0 hits before adding
@ REUSE: UMI_CARD_ID(0x10f4 line 145), INSECT_PRINCESS_CID(0x1704 line ~1413),
@        DRAGON_CAPTURE_JAR_CID(0x10ef line ~1312), CHAIN_ENERGY_CID(0x132c line ~399),
@        MONSTER_REBORN_CID(0x12ea line ~790), cid_12fb(line ~1142),
@        FORCED_REQUISITION_CID(0x1354 line ~1160),
@        PUMPKING_CID(0x1009 line ~312), CASTLE_OF_DARK_ILLUSIONS_CID(0x0ff9 line ~312)
@ =============================================================================
.equ MAIDEN_OF_THE_AQUA_CID,         0x000013a2  @ Maiden of the Aqua (pw=17214465; card-stats.s slot=0x13A2); dispatch_equip_pair_sprites_by_state check
.equ FINAL_ATTACK_ORDERS_CID,        0x000015fb  @ Final Attack Orders (pw=52503575; card-stats.s slot=0x15FB); scan_all_slots_for_max_equip_match dispatch
.equ LEVEL_LIMIT_AREA_B_CID,         0x000017a6  @ Level Limit - Area B (pw=03136426; card-stats.s slot=0x17A6); scan_all_slots_for_max_equip_match dispatch
.equ LEVEL_LIMIT_AREA_A_CID,         0x0000197b  @ Level Limit - Area A (pw=54976796; card-stats.s slot=0x197B); scan_all_slots_for_max_equip_match dispatch
.equ KOTODAMA_CID,                   0x00001343  @ Kotodama (pw=19406822; card-stats.s slot=0x1343); enqueue_equip_chain_sprites_for_zones test_slot_has_active_card key
.equ MAGICAL_THORN_CID,              0x00001306  @ Magical Thorn (pw=53119267; card-stats.s slot=0x1306); scan_field_slots_for_lp_zone_sprite_with_equip CARD_ID filter
.equ SKULL_INVITATION_CID,           0x00001361  @ Skull Invitation (pw=98139712; card-stats.s slot=0x1361); scan_field_slots_for_lp_zone_sprite_with_equip + scan_all_zone_slots_for_lp_change_indicator
```

### duel_field.inc 新增 (3 NEW ROM ptr + 1 NEW code)

```asm
@ =============================================================================
@ file 11 Seg-5 additions: effect handler table + equip candidate tables
@ =============================================================================
.equ gEffectHandlerTable,       0x09e5a128  @ ROM effect handler dispatch table; 0x132 entries x 8B [CID u16, fn_ptr+1]; binary search in find_effect_record_index_by_id; fn_ptr at [+4] called via invoke_r3; C5 grep=0 (new); conf: high
.equ gEquipCandidateScoreBase,  0x09e3f150  @ ROM equip candidate score table base; 5 words per player (0x14B); used 5x in scan_all_slots_for_max_equip_match inner scan + scan_field_for_fieldspell_eligible_slot_sprite; adjacent EQUIP_PAIR_ENTRY_TABLE_BASE=0x09e3f140+0x10; C5 grep=0 (new); conf: high
.equ gEquipCandidateInitBase,   0x09e3f164  @ ROM equip candidate init template; 10 words copied to sp+4 work buf in scan_all_slots_for_max_equip_match; C5 grep=0 (new); conf: high
.equ SLOT_ACTIVE_CHECK_CODE,    0x0000104c  @ test_slot_has_active_card 3rd param (activation check code); used in scan_slots_activate_equip_by_effect_id + enqueue_equip_chain_sprites_for_zones; C5 grep=0 (new); conf: med
```

---

## 八、§5.1 未引用数据

None. All data in Seg-5 range are literal pool slots used by the 18 named functions.

---

## 九、disasm / carve

None. Seg-5 is region C (0 ROM_INCBIN, purely named THUMB functions with EQ/RENAME/PLATE work).

---

## 十、执行摘要

- **EQ**: 113 slots total (14 PTR_gP1LifePoints REUSE + 37 PLAYER_BLOCK_STRIDE REUSE [+2: e5b8/ea18] + 42 global ptr/offset REUSE [+1: e5bc gDuelFieldSlots] + 11 NEW CID/ROM-ptr + 1 NEW code + 6 raw DWORD/RENAME [+1: switchd_base_d8a8]; removed 1 wrong duplicate DAT_0808e824 row from gEquipZoneCountTable group)
- **REF**: 0
- **RENAME**: 14 (PTR_gP1LifePoints_ x14 → ptr_lp_*) + 1 raw slot rename (DAT_0808d8a8 → switchd_base_d8a8; RENAME-only, no REF needed — Ghidra switch recovery already resolved the table)
- **FUNC_RENAME**: 0 (no new functions)
- **PLATE**: 12 functions need C8 stale-FUN_ substitution
- **carve**: 0
- **disasm**: 0
- **新 constants**: card_info.inc +7 (6 CID + 1 CID already verified SKULL_INVITATION_CID), duel_field.inc +4
- **CSV sync**: no (no new/renamed functions)
- **byte-identical**: byte-identical 验证 (SHA1 9689337d) 通过后 commit
