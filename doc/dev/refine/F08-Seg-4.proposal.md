# Refine Proposal: F08-Seg-4  [0x08067160..0x08067fa4)

## 段测绘

- 函数入口 x21 (含首尾跨界函数):
  - 0x08067160 `dispatch_effect_zone_lp_sprites_by_slot_flags` (push @ line 6748)
  - 0x080671bc `[unnamed: check_activation_ctx_zone11_match_cb]` (no push, bx lr leaf; called via fn-ptr DAT_08067270)
  - 0x080671e8 `dispatch_activation_display_sprites_by_state`
  - 0x080672a4 `dispatch_equip_oam_by_zone_state_with_bit2_gate`
  - 0x08067334 `tick_zone_sprite_pipeline_opponent_side`
  - 0x0806734c `invoke_equip_zone_entry_with_zone11_gate`
  - 0x0806738c `dispatch_equip_zone_sprite_or_lp_indicator_by_type`
  - 0x080673e0 `enqueue_equip_zone_sprite_with_deck_count`
  - 0x08067440 `invoke_equip_slot_indicator_and_zone_slot_sprites`
  - 0x080674b8 `emit_equip_zone_bitmap_sprite_type11`
  - 0x08067594 `build_equip_target_bitmap_with_eligibility_gate`
  - 0x08067614 `tick_equip_banisher_sprite_state_machine`
  - 0x080676e0 `build_equip_target_bitmap_for_zone11_path`
  - 0x08067750 `tick_equip_chain_banisher_sprite_state`
  - 0x08067804 `enqueue_equip_chain_link_sprite_attr`
  - 0x080678c8 `enqueue_dual_equip_slot_sprites_with_whitelist_check`
  - 0x080679d8 `tick_equip_activation_sprite_state_with_eligibility`
  - 0x08067b5c `tick_equip_neo_daedalus_sprite_state_machine`
  - 0x08067c0c `tick_equip_head_slot_sprite_state_machine`
  - 0x08067ea0 `dispatch_equip_slot_sprite_with_field6_score`
  - 0x08067f90 `enqueue_sprite_attr_type11_from_slot`
- 残留自动名槽: 81 个 (DAT_/DWORD_/PTR_gP1LifePoints_*)
- ROM_INCBIN / .byte 块: 0 个 (python ref-scan 无 ROM_INCBIN/switchD 确认)

## 数据块分类 (Rule 2/3)

本段 0 ROM_INCBIN / 0 switchD，无数据块分类需要。Python 扫描段内 `ROM_INCBIN`/`.byte` 关键词: 0 命中，确认纯函数体段。

| 块 | ref-scan | 判定 | 理由 |
|----|----------|------|------|
| (无) | — | — | 段内无 ROM_INCBIN/.byte 块 |

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate; 共 46 唯一槽位 + 重复引用 = 81 总槽)

**说明**: 多个函数共用相同值时仅列该值对应的每个唯一槽地址。

#### 全局地址 — REF (RENAME 到 global label)

| 槽 | 值 | GAS_label | 证据 |
|----|-----|-----------|------|
| DAT_080671dc @ 0x080671dc | 0x0201b290 | gDuelPhaseFlags | reuse ewram.inc:351; EQUIP_ACTIVE_CTX_OFF consumer |
| DAT_08067228 @ 0x08067228 | 0x0201b290 | gDuelPhaseFlags | reuse ewram.inc:351 |
| DAT_080672cc @ 0x080672cc | 0x0201b290 | gDuelPhaseFlags | reuse ewram.inc:351 |
| DAT_0806763c @ 0x0806763c | 0x0201b290 | gDuelPhaseFlags | reuse ewram.inc:351 |
| DAT_0806776c @ 0x0806776c | 0x0201b290 | gDuelPhaseFlags | reuse ewram.inc:351 |
| DAT_08067a14 @ 0x08067a14 | 0x0201b290 | gDuelPhaseFlags | reuse ewram.inc:351 |
| DAT_08067a9c @ 0x08067a9c | 0x0201b290 | gDuelPhaseFlags | reuse ewram.inc:351 |
| DAT_08067ba4 @ 0x08067ba4 | 0x0201b290 | gDuelPhaseFlags | reuse ewram.inc:351 |
| DWORD_08067c40 @ 0x08067c40 | 0x0201b290 | gDuelPhaseFlags | reuse ewram.inc:351 |
| DWORD_08067d60 @ 0x08067d60 | 0x0201b290 | gDuelPhaseFlags | reuse ewram.inc:351 |
| DWORD_08067e40 @ 0x08067e40 | 0x0201b290 | gDuelPhaseFlags | reuse ewram.inc:351 |
| DWORD_08067e58 @ 0x08067e58 | 0x0201b290 | gDuelPhaseFlags | reuse ewram.inc:351 |
| DWORD_08067ef8 @ 0x08067ef8 | 0x0201b290 | gDuelPhaseFlags | reuse ewram.inc:351 |
| DAT_08067224 @ 0x08067224 | 0x0201e2a0 | gDuelCardCtxBase | reuse ewram.inc:218; ldr then +0x4 for phase ts |
| DAT_080674b4 @ 0x080674b4 | 0x0201c510 | gDuelFieldSlots | reuse ewram.inc:312 |
| DAT_08067580 @ 0x08067580 | 0x0201c510 | gDuelFieldSlots | reuse ewram.inc:312 |
| DAT_0806789c @ 0x0806789c | 0x0201c510 | gDuelFieldSlots | reuse ewram.inc:312 |
| DAT_080679d4 @ 0x080679d4 | 0x0201c510 | gDuelFieldSlots | reuse ewram.inc:312 |
| DAT_08067a98 @ 0x08067a98 | 0x0201c510 | gDuelFieldSlots | reuse ewram.inc:312 |
| DAT_08067b38 @ 0x08067b38 | 0x0201c510 | gDuelFieldSlots | reuse ewram.inc:312 |
| DWORD_08067ca4 @ 0x08067ca4 | 0x0201c510 | gDuelFieldSlots | reuse ewram.inc:312 |
| DWORD_08067ef4 @ 0x08067ef4 | 0x0201c510 | gDuelFieldSlots | reuse ewram.inc:312 |
| DAT_08067bf8 @ 0x08067bf8 | 0x0201c740 | gP1SlotSetCodeArray | reuse ewram.inc:330; Neo Daedalus OAM dispatch context base |

gP1LifePoints REF slots (PTR_gP1LifePoints_* already use correct global name, DWORD_* slots need rename):

| 槽 | 值 | 目标 | 证据 |
|----|-----|------|------|
| PTR_gP1LifePoints_0806724c | 0x0201c4e0 | gP1LifePoints | already named; reuse ewram.inc:79 |
| PTR_gP1LifePoints_0806726c | 0x0201c4e0 | gP1LifePoints | already named; reuse ewram.inc:79 |
| PTR_gP1LifePoints_08067294 | 0x0201c4e0 | gP1LifePoints | already named; reuse ewram.inc:79 |
| PTR_gP1LifePoints_080672f8 | 0x0201c4e0 | gP1LifePoints | already named; reuse ewram.inc:79 |
| PTR_gP1LifePoints_08067588 | 0x0201c4e0 | gP1LifePoints | already named; reuse ewram.inc:79 |
| PTR_gP1LifePoints_0806766c | 0x0201c4e0 | gP1LifePoints | already named; reuse ewram.inc:79 |
| PTR_gP1LifePoints_080676a0 | 0x0201c4e0 | gP1LifePoints | already named; reuse ewram.inc:79 |
| DWORD_08067de4 @ 0x08067de4 | 0x0201c4e0 | gP1LifePoints | reuse ewram.inc:79; in tick_equip_head_slot_sprite_state_machine |
| DWORD_08067e98 @ 0x08067e98 | 0x0201c4e0 | gP1LifePoints | reuse ewram.inc:79; in tick_equip_head_slot_sprite_state_machine |

#### 偏移/阈值常量 EQ (真正的 .equ 值)

| 槽 | 值 | equate | 所在 inc | 证据 |
|----|-----|--------|----------|------|
| DAT_08067250 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc:250 | reuse ×14 total |
| DAT_080672fc | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc:250 | reuse |
| DAT_080674b0 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc:250 | reuse |
| DAT_0806757c | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc:250 | reuse |
| DAT_08067670 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc:250 | reuse |
| DAT_080676a4 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc:250 | reuse |
| DAT_08067898 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc:250 | reuse |
| DAT_080679d0 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc:250 | reuse |
| DAT_08067a94 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc:250 | reuse |
| DAT_08067b34 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc:250 | reuse |
| DAT_08067bf4 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc:250 | reuse |
| DWORD_08067ca0 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc:250 | reuse |
| DWORD_08067de8 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc:250 | reuse |
| DWORD_08067ef0 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc:250 | reuse |
| DAT_08067a90 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc:434 | reuse; [gDuelPhaseFlags+0x4a4] frame counter |
| DAT_08067b30 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc:434 | reuse |
| DWORD_08067d64 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc:434 | reuse |
| DWORD_08067de0 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc:434 | reuse |
| DWORD_08067e44 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc:434 | reuse |
| DWORD_08067e5c | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc:434 | reuse |
| DAT_080671e0 | 0x00000484 | EQUIP_ACTIVE_CTX_OFF | duel_field.inc:360 | reuse; [gDuelPhaseFlags+0x484] equip ctx ptr |
| DAT_08067298 | 0x00001d70 | LP_BANISHER_CTX_OFF | ewram.inc:421 | reuse; [gP1LifePoints+0x1d70]; face-down slot list ptr context; conf high |
| DAT_0806758c | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc:275 | reuse; [gP1LifePoints+0x1ce8]; LP display block2 |
| DWORD_08067e9c | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc:275 | reuse |
| DAT_08067590 | 0x00001cf4 | FIELD_STATE_OFF | duel_field.inc:205 | reuse; [gP1LifePoints+0x1cf4] activation phase state |
| DAT_080678a0 | 0x00001cbc | CHAIN_LINK_COUNTER_OFF | duel_field.inc:207 | reuse; [gP1LifePoints+0x1cbc] chain link counter |
| DAT_080678a4 | 0x00001cb8 | DUEL_ACTIVE_PLAYER_OFF | duel_field.inc:155 | reuse; [gP1LifePoints+0x1cb8] active turn player |
| DWORD_08067188 | 0x00000bb8 | LP_COST_3000 | duel_field.inc:200 | reuse; r1 arg to submit_effect_zone_lp_and_shape_sprites = 3000 LP amount |
| DWORD_080671b4 | 0x00000bb8 | LP_COST_3000 | duel_field.inc:200 | reuse |
| DWORD_080671b8 | 0x00001388 | LP_COST_5000 | duel_field.inc:312 | reuse; r1 arg to enqueue_sprite_attr_record_with_cap = 5000 LP cap param |
| DAT_08067584 | 0x00001102 | SWORDS_OF_REVEALING_LIGHT_CID | card_info.inc:847 | reuse; Swords of Revealing Light filter in emit_equip_zone_bitmap_sprite_type11 |
| DWORD_08067ca8 | 0x0000123b | CRUSH_CARD_CID | card_info.inc:620 | reuse |
| DWORD_08067d08 | 0x0000123b | CRUSH_CARD_CID | card_info.inc:620 | reuse |
| DWORD_08067dec | 0x0000123b | CRUSH_CARD_CID | card_info.inc:620 | reuse |
| DWORD_08067cac | 0x0000188c | DECK_DEVASTATION_VIRUS_CID | card_info.inc:627 | reuse |
| DWORD_08067d0c | 0x0000188c | DECK_DEVASTATION_VIRUS_CID | card_info.inc:627 | reuse |
| DWORD_08067df0 | 0x0000188c | DECK_DEVASTATION_VIRUS_CID | card_info.inc:627 | reuse |
| DAT_08067b9c | 0x00001232 | MAGICAL_LABYRINTH_CID | card_info.inc:785 | reuse; Magical Labyrinth -> redirect to Wall Shadow |
| DAT_08067ba0 | 0x00001117 | WALL_SHADOW_CID | card_info.inc:712 | reuse; Wall Shadow substitute target |
| DWORD_08067400 | 0x000011d8 | NEEDLE_WORM_CID | card_info.inc:717 | reuse; Needle Worm -> deck-count=5 |
| DWORD_08067cc0 | 0x000005db | CARD_FIELD3_THRESHOLD_1499 | NEW card_info.inc (域裁定见下) | Crush Card targeting: get_card_extended_stat_field3 > 1499 -> target; field3(ATK)-domain, NOT field5 score; conf: high |
| DWORD_08067d20 | 0x000005db | CARD_FIELD3_THRESHOLD_1499 | NEW | reuse |
| DWORD_08067e04 | 0x000005db | CARD_FIELD3_THRESHOLD_1499 | NEW | reuse |
| DWORD_08067ce4 | 0x000005dc | CARD_FIELD3_THRESHOLD_1500 | NEW card_info.inc (域裁定见下) | Deck Devastation Virus targeting: get_card_extended_stat_field3_raw <= 1500 -> target; field3(ATK)-domain, NOT LP threshold; conf: high |
| DWORD_08067d5c | 0x000005dc | CARD_FIELD3_THRESHOLD_1500 | NEW | reuse |
| DWORD_08067e3c | 0x000005dc | CARD_FIELD3_THRESHOLD_1500 | NEW | reuse |

#### NEW EQ (新建 card_info.inc 条目)

| slot | value | proposed_equate | 证据 |
|------|-------|-----------------|------|
| DWORD_080673fc @ 0x080673fc | 0x00001744 | SOUL_ABSORBING_BONE_TOWER_CID | card-stats.s line 19762: "Soul-Absorbing Bone Tower slot=0x1744 pw=63012333"; grep card_info.inc 0x1744 = 0 hits; enqueue_equip_zone_sprite_with_deck_count context: CID->deck-count=2 |
| DWORD_0806740c @ 0x0806740c | 0x000019d0 | MALICE_ASCENDANT_CID | card-stats.s line 22xxx: "Malice Ascendant slot=0x19D0 pw=14255590"; grep card_info.inc 0x19d0 = 0 hits; same fn context: CID->deck-count from count_extra_deck_cards_by_id |

### REF_SLOTS (fn-ptr)

| 槽 | 目标值 | GAS 表达式 | 证据 |
|----|--------|-----------|------|
| DAT_08067270 @ 0x08067270 | 0x080671bd | check_activation_ctx_zone11_match_cb+1 | ROM @ 0x08067270 = 0x080671bd (python 核对); 函数在 0x080671bc (0x080671bd&~1); bit0=1 THUMB ptr; 1 THUMB+1 ref (raw=0); body: takes (r0=player, r1=zone_idx); checks gDuelPhaseFlags+EQUIP_ACTIVE_CTX_OFF slot player match AND zone_idx==0xb, returns 0x800 or 0; passed as callback to init_zone_activation_display_fields at line 6909 |

### RENAME_SLOTS (纯改名 + EOL)

仅对 DAT_/DWORD_ 槽重命名 (PTR_gP1LifePoints_* 已有描述性名保留原名):

| 旧名 | 新 slot label | EOL (可选) |
|------|--------------|------------|
| DAT_080671dc | gDuelPhaseFlags_dispatch_effect_zone_80671dc | gDuelPhaseFlags |
| DAT_080671e0 | equip_active_ctx_off_dispatch_effect_zone_80671e0 | EQUIP_ACTIVE_CTX_OFF=0x484 |
| DAT_08067224 | gDuelCardCtxBase_dispatch_act_80067224 | gDuelCardCtxBase |
| DAT_08067228 | gDuelPhaseFlags_dispatch_act_08067228 | gDuelPhaseFlags |
| DAT_08067250 | player_stride_dispatch_act_08067250 | PLAYER_BLOCK_STRIDE |
| DAT_08067270 | cb_check_zone11_match_08067270 | init_zone_activation_display_fields callback |
| DAT_08067298 | lp_banisher_ctx_off_dispatch_act_08067298 | LP_BANISHER_CTX_OFF=0x1d70 |
| DAT_080672cc | gDuelPhaseFlags_dispatch_oam_080672cc | gDuelPhaseFlags |
| DAT_080672fc | player_stride_dispatch_oam_080672fc | PLAYER_BLOCK_STRIDE |
| DAT_0806757c | player_stride_emit_bitmap_0806757c | PLAYER_BLOCK_STRIDE |
| DAT_08067580 | gDuelFieldSlots_emit_bitmap_08067580 | gDuelFieldSlots |
| DAT_08067584 | swords_cid_emit_bitmap_08067584 | SWORDS_OF_REVEALING_LIGHT_CID=0x1102 |
| DAT_0806758c | p1lp_block2_off_emit_bitmap_0806758c | P1LP_BLOCK2_OFF_1CE8 |
| DAT_08067590 | field_state_off_emit_bitmap_08067590 | FIELD_STATE_OFF=0x1cf4 |
| DAT_0806763c | gDuelPhaseFlags_tick_banisher_0806763c | gDuelPhaseFlags |
| DAT_08067670 | player_stride_tick_banisher_08067670 | PLAYER_BLOCK_STRIDE |
| DAT_080676a4 | player_stride_tick_banisher_080676a4 | PLAYER_BLOCK_STRIDE |
| DAT_0806776c | gDuelPhaseFlags_tick_chain_ban_0806776c | gDuelPhaseFlags |
| DAT_08067898 | player_stride_enq_chain_link_08067898 | PLAYER_BLOCK_STRIDE |
| DAT_0806789c | gDuelFieldSlots_enq_chain_link_0806789c | gDuelFieldSlots |
| DAT_080678a0 | chain_link_ctr_off_enq_chain_link_080678a0 | CHAIN_LINK_COUNTER_OFF=0x1cbc |
| DAT_080678a4 | duel_active_player_off_enq_chain_link_080678a4 | DUEL_ACTIVE_PLAYER_OFF=0x1cb8 |
| DAT_080679d0 | player_stride_enq_dual_080679d0 | PLAYER_BLOCK_STRIDE |
| DAT_080679d4 | gDuelFieldSlots_enq_dual_080679d4 | gDuelFieldSlots |
| DAT_08067a14 | gDuelPhaseFlags_tick_act_eligib_08067a14 | gDuelPhaseFlags |
| DAT_08067a90 | equip_phase_frame_off_tick_act_08067a90 | EQUIP_PHASE_FRAME_OFF=0x4a4 |
| DAT_08067a94 | player_stride_tick_act_08067a94 | PLAYER_BLOCK_STRIDE |
| DAT_08067a98 | gDuelFieldSlots_tick_act_08067a98 | gDuelFieldSlots |
| DAT_08067a9c | gDuelPhaseFlags_tick_act_08067a9c | gDuelPhaseFlags |
| DAT_08067b30 | equip_phase_frame_off_tick_act_08067b30 | EQUIP_PHASE_FRAME_OFF=0x4a4 |
| DAT_08067b34 | player_stride_tick_act_08067b34 | PLAYER_BLOCK_STRIDE |
| DAT_08067b38 | gDuelFieldSlots_tick_act_08067b38 | gDuelFieldSlots |
| DAT_08067b9c | magical_labyrinth_cid_08067b9c | MAGICAL_LABYRINTH_CID=0x1232 |
| DAT_08067ba0 | wall_shadow_cid_08067ba0 | WALL_SHADOW_CID=0x1117 |
| DAT_08067ba4 | gDuelPhaseFlags_tick_neodaed_08067ba4 | gDuelPhaseFlags |
| DAT_08067bf4 | player_stride_tick_neodaed_08067bf4 | PLAYER_BLOCK_STRIDE |
| DAT_08067bf8 | gP1SlotSetCodeArray_tick_neodaed_08067bf8 | gP1SlotSetCodeArray |
| DWORD_08067188 | lp_cost_3000_dispatch_07188 | LP_COST_3000=0xbb8 |
| DWORD_080671b4 | lp_cost_3000_dispatch_071b4 | LP_COST_3000=0xbb8 |
| DWORD_080671b8 | lp_cost_5000_dispatch_071b8 | LP_COST_5000=0x1388 |
| DWORD_080673fc | soul_absorbing_bone_tower_cid_073fc | SOUL_ABSORBING_BONE_TOWER_CID=0x1744 |
| DWORD_08067400 | needle_worm_cid_07400 | NEEDLE_WORM_CID=0x11d8 |
| DWORD_0806740c | malice_ascendant_cid_0740c | MALICE_ASCENDANT_CID=0x19d0 |
| DWORD_08067ca0 | player_stride_tick_head_07ca0 | PLAYER_BLOCK_STRIDE |
| DWORD_08067ca4 | gDuelFieldSlots_tick_head_07ca4 | gDuelFieldSlots |
| DWORD_08067ca8 | crush_card_cid_tick_head_07ca8 | CRUSH_CARD_CID=0x123b |
| DWORD_08067cac | ddv_cid_tick_head_07cac | DECK_DEVASTATION_VIRUS_CID=0x188c |
| DWORD_08067cc0 | field3_threshold_1499_07cc0 | CARD_FIELD3_THRESHOLD_1499=0x5db |
| DWORD_08067ce4 | field3_threshold_1500_07ce4 | CARD_FIELD3_THRESHOLD_1500=0x5dc |
| DWORD_08067d08 | crush_card_cid_tick_head_07d08 | CRUSH_CARD_CID=0x123b |
| DWORD_08067d0c | ddv_cid_tick_head_07d0c | DECK_DEVASTATION_VIRUS_CID=0x188c |
| DWORD_08067d20 | field3_threshold_1499_07d20 | CARD_FIELD3_THRESHOLD_1499=0x5db |
| DWORD_08067d5c | field3_threshold_1500_07d5c | CARD_FIELD3_THRESHOLD_1500=0x5dc |
| DWORD_08067d60 | gDuelPhaseFlags_tick_head_07d60 | gDuelPhaseFlags |
| DWORD_08067d64 | equip_phase_frame_off_tick_head_07d64 | EQUIP_PHASE_FRAME_OFF=0x4a4 |
| DWORD_08067de0 | equip_phase_frame_off_tick_head_07de0 | EQUIP_PHASE_FRAME_OFF=0x4a4 |
| DWORD_08067de8 | player_stride_tick_head_07de8 | PLAYER_BLOCK_STRIDE |
| DWORD_08067dec | crush_card_cid_tick_head_07dec | CRUSH_CARD_CID=0x123b |
| DWORD_08067df0 | ddv_cid_tick_head_07df0 | DECK_DEVASTATION_VIRUS_CID=0x188c |
| DWORD_08067e04 | field3_threshold_1499_07e04 | CARD_FIELD3_THRESHOLD_1499=0x5db |
| DWORD_08067e3c | field3_threshold_1500_07e3c | CARD_FIELD3_THRESHOLD_1500=0x5dc |
| DWORD_08067c40 | gDuelPhaseFlags_tick_head_07c40 | gDuelPhaseFlags |
| DWORD_08067e40 | gDuelPhaseFlags_tick_head_07e40 | gDuelPhaseFlags |
| DWORD_08067e44 | equip_phase_frame_off_tick_head_07e44 | EQUIP_PHASE_FRAME_OFF=0x4a4 |
| DWORD_08067e58 | gDuelPhaseFlags_tick_head_07e58 | gDuelPhaseFlags |
| DWORD_08067e5c | equip_phase_frame_off_tick_head_07e5c | EQUIP_PHASE_FRAME_OFF=0x4a4 |
| DWORD_08067e98 | gP1LifePoints_tick_head_07e98 | gP1LifePoints |
| DWORD_08067e9c | p1lp_block2_off_tick_head_07e9c | P1LP_BLOCK2_OFF_1CE8=0x1ce8 |
| DWORD_08067ef0 | player_stride_dispatch_f6_07ef0 | PLAYER_BLOCK_STRIDE |
| DWORD_08067ef4 | gDuelFieldSlots_dispatch_f6_07ef4 | gDuelFieldSlots |
| DWORD_08067ef8 | gDuelPhaseFlags_dispatch_f6_07ef8 | gDuelPhaseFlags |
| DAT_080674b0 | player_stride_invoke_slot_ind_074b0 | PLAYER_BLOCK_STRIDE |
| DAT_080674b4 | gDuelFieldSlots_invoke_slot_ind_074b4 | gDuelFieldSlots |

### FUNC_RENAME (误名订正)

未发现函数名与函数体矛盾的误名。所有 20 个命名函数名称与其操作一致 (state machine ticks / bitmap builders / sprite enqueuers / zone dispatchers)。

FUNC_RENAME = 0。

### PLATE (R5; 新建 + 旧名更新)

需新建/更新 plate 的函数:

1. **新函数 `check_activation_ctx_zone11_match_cb` @ 0x080671bc** (目前无 label + 无 plate): 需添加 label + plate。
   - Plate (ASCII): "Callback: given (r0=player_id, r1=zone_idx), checks if gDuelPhaseFlags[EQUIP_ACTIVE_CTX_OFF] slot player_id matches r0 AND r1==0xb (chain zone 11). Returns 0x800 on match, 0 on mismatch. Called via fn-ptr stored at DAT_08067270. Params: r0=player_id, r1=zone_idx. Returns: r0=u32 (0x800 or 0). indeg=0 (fn-ptr only: 1 THUMB+1 ref, raw=0)."

2. **`dispatch_effect_zone_lp_sprites_by_slot_flags` @ 0x08067160**: already has plate; verify stale FUN_ = clean (confirmed above).

3. 其余 19 个命名函数均已有完整 plate。所有 plate 文本经 grep `[^\x00-\x7F]` 验证 = 0 非 ASCII 字符 (clean)。

**PLATE 新建/更新总计: 1** (新标注 check_activation_ctx_zone11_match_cb 函数 label + plate)

## carve 计划 (R7)

本段 0 ROM_INCBIN 块，carve = 0。

## disasm 计划 (R4)

本段 0 ROM_INCBIN / 0 switchD 块，disasm = 0。

## 新增 constants / 全局

添加到 `constants/card_info.inc`:
```
.equ SOUL_ABSORBING_BONE_TOWER_CID, 0x00001744  @ Soul-Absorbing Bone Tower (pw=63012333); enqueue_equip_zone_sprite_with_deck_count deck-count=2; 8 raw ROM refs
.equ MALICE_ASCENDANT_CID,          0x000019d0  @ Malice Ascendant (pw=14255590); enqueue_equip_zone_sprite_with_deck_count count_extra_deck_cards_by_id; 9 raw ROM refs
.equ CARD_FIELD3_THRESHOLD_1499,    0x000005db  @ field3(ATK) targeting threshold 1499; Crush Card Virus: field3>1499 -> target; field3(ATK)-domain (NOT field5 score); tick_equip_head_slot_sprite_state_machine 3 slots
.equ CARD_FIELD3_THRESHOLD_1500,    0x000005dc  @ field3(ATK) targeting threshold 1500; Deck Devastation Virus: field3_raw<=1500 -> target; field3(ATK)-domain (NOT LP threshold); tick_equip_head_slot_sprite_state_machine 3 slots
```

**C5 双向核**:
- SOUL_ABSORBING_BONE_TOWER_CID (0x1744): grep card_info.inc "0x1744" = 0 hits; grep "SOUL_ABSORBING" = 0 hits. NEW 确认。card-stats.s line 19762 core record "slot=0x1744 pw=63012333" 坐实。
- MALICE_ASCENDANT_CID (0x19d0): grep card_info.inc "0x19d0" = 0 hits; grep "MALICE" = 0 hits. NEW 确认。card-stats.s "Malice Ascendant slot=0x19D0 pw=14255590" 坐实。
- **CARD_FIELD3_THRESHOLD_1499 (0x5db) / CARD_FIELD3_THRESHOLD_1500 (0x5dc) — 域裁定新建 (C5 例外子规则)**: 这两个值按值 grep **非 0 命中** (0x5db 已有 FIELD5_SCORE_THRESHOLD_1499; 0x5dc 已有 CARD_STAT_LP_THRESHOLD_1500 + LP_COST_1500)。但按 C5 例外 "语义截然不同的两实体各建独立 (读消费者裁定)" 应新建:
  - **消费者证据** (asm/08:8467-8495, tick_equip_head_slot_sprite_state_machine): Crush Card Virus (CID 0x123b) 路径 `bl get_card_extended_stat_field3; cmp r0,#0x5db; ble->非目标 / bgt->目标` (现实 YGO: 摧毁 ATK>=1500 怪兽); Deck Devastation Virus (CID 0x188c) 路径 `bl get_card_extended_stat_field3_raw; cmp r0,#0x5dc; bgt->非目标 / ble->目标 r7=1` (现实 YGO: 摧毁 ATK<=1500 怪兽)。**field3 = 怪兽 ATK** (病毒卡 AI 选标)。
  - **域区分**: 此处是**怪兽 ATK 选标阈值** (卡效果 AI), 与 CARD_STAT_LP_THRESHOLD_1500 ("LP 显示阈值 render_card_stats") / FIELD5_SCORE_THRESHOLD_1499 ("field5 资格 score gate") 语义截然不同。复用任一现有名 = 误名 (违反 R5/误名警觉)。
  - **先例**: 0x5dc 已存在 2 个独立常量 (CARD_STAT_LP_THRESHOLD_1500 + LP_COST_1500), 项目已接受同值多域常量。参 memory `feedback_c5_offset_value_collision_scope` (用户裁定同值碰撞按域各建独立)。
  - **per-slot 安全**: data-equate 仅作用本段 6 槽; file 05 的 FIELD5 槽 / 其他 LP 槽不受影响。
  - **置信度 high** (消费者机器码已逐指令核, 卡名/比较运算符/阈值一致)。

其他已建 constants 全部 **reuse** (无新 inc):
- PLAYER_BLOCK_STRIDE / gDuelFieldSlots / gP1LifePoints / gDuelPhaseFlags / gDuelCardCtxBase / gP1SlotSetCodeArray: ewram.inc
- EQUIP_PHASE_FRAME_OFF / LP_BANISHER_CTX_OFF / P1LP_BLOCK2_OFF_1CE8 / LP_COST_3000 / LP_COST_5000 / FIELD5_SCORE_THRESHOLD_1499 / CARD_STAT_LP_THRESHOLD_1500: ewram.inc / duel_field.inc / card_info.inc
- EQUIP_ACTIVE_CTX_OFF / CHAIN_LINK_COUNTER_OFF / DUEL_ACTIVE_PLAYER_OFF / FIELD_STATE_OFF: duel_field.inc
- SWORDS_OF_REVEALING_LIGHT_CID / CRUSH_CARD_CID / DECK_DEVASTATION_VIRUS_CID / MAGICAL_LABYRINTH_CID / WALL_SHADOW_CID / NEEDLE_WORM_CID: card_info.inc

## §5.1 登记 (Rule 3) — 0 引用块

本段无 ROM_INCBIN 块，§5.1 = 0。

## 消费者证据 (R6) — 关键槽语义

| 槽/全局 | 函数 | file:line | 置信度 |
|---------|------|-----------|--------|
| gDuelPhaseFlags+0x4a0 (equip zone state) | dispatch_activation_display_sprites_by_state | asm/08 line 6863-6874 | high: movs r1,#0x94;lsls #3 = 0x4a0; ldr r0,[r0]; cmp r0,#0x7f/0x7e/0x80 state dispatch |
| EQUIP_ACTIVE_CTX_OFF=0x484 | check_activation_ctx_zone11_match_cb | asm/08 line 6795-6798 | high: ldr+adds gDuelPhaseFlags+0x484; ldr [r1] = equip ctx ptr; ldrb [+2] = player_id |
| LP_BANISHER_CTX_OFF=0x1d70 | dispatch_activation_display_sprites_by_state | asm/08 line 6920-6928 | high: gP1LifePoints+0x1d70 -> ldr [r1] -> pass to enqueue_face_down_slot_sprite_attr; ewram.inc:421 confirms LP_BANISHER_CTX_OFF |
| SOUL_ABSORBING_BONE_TOWER_CID=0x1744 | enqueue_equip_zone_sprite_with_deck_count | asm/08 line 7164-7188 | high: cmp card_id vs 0x1744 -> r2=2 (deck count=2); card-stats.s confirms slot/pw |
| MALICE_ASCENDANT_CID=0x19d0 | enqueue_equip_zone_sprite_with_deck_count | asm/08 line 7179-7196 | high: cmp card_id vs 0x19d0 -> count_extra_deck_cards_by_id; card-stats.s confirms slot/pw |
| CRUSH_CARD_CID=0x123b | tick_equip_head_slot_sprite_state_machine | asm/08 line 8452-8476 | high: cmp halfword[r1] vs 0x123b -> get_card_extended_stat_field3; card_info.inc:620 confirms |
| DECK_DEVASTATION_VIRUS_CID=0x188c | tick_equip_head_slot_sprite_state_machine | asm/08 line 8455-8483 | high: cmp vs 0x188c -> get_card_extended_stat_field3_raw; card_info.inc:627 confirms |
| CARD_FIELD3_THRESHOLD_1499=0x5db (field3/ATK) | tick_equip_head_slot_sprite_state_machine | asm/08 line 8469-8473 | high: Crush Card (0x123b) get_card_extended_stat_field3 > 0x5db -> target; field3=ATK domain; NEW domain-distinct const (not FIELD5 score) |
| CARD_FIELD3_THRESHOLD_1500=0x5dc (field3/ATK) | tick_equip_head_slot_sprite_state_machine | asm/08 line 8479-8483 | high: DDV (0x188c) get_card_extended_stat_field3_raw <= 0x5dc -> target r7=1; field3=ATK domain; NEW domain-distinct const (not LP threshold) |
| DAT_08067270 fn-ptr=0x080671bd | dispatch_activation_display_sprites_by_state | asm/08 line 6908-6909 | high: DAT_08067270 loaded as r0 arg, passed to bl init_zone_activation_display_fields (file 12); ROM py core = 0x080671bd confirmed |

## 求助 (低置信度语义) — 已裁定

1. **[已裁定 RESOLVED] 0x5db/0x5dc field3 阈值 → 新建 CARD_FIELD3_THRESHOLD_1499/1500** (域裁定, conf: high):
   - 裁定依据: 读消费者 (asm/08:8467-8495) 确认 field3 = 怪兽 ATK, 此处为 Crush Card Virus (ATK>1499) / Deck Devastation Virus (ATK<=1500) 的 AI 选标阈值, 与 CARD_STAT_LP_THRESHOLD_1500 ("LP 显示") / FIELD5_SCORE_THRESHOLD_1499 ("field5 资格 score") 语义截然不同。
   - 按 C5 例外子规则 "语义截然不同的两实体各建独立 (读消费者裁定)" + 先例 (0x5dc 已有 2 个独立常量) → **新建 CARD_FIELD3_THRESHOLD_1499 (0x5db) / CARD_FIELD3_THRESHOLD_1500 (0x5dc)** 进 card_info.inc。
   - 连带修正: 原 0x5db 槽 (med-conf 复用 FIELD5_SCORE_THRESHOLD_1499 = 误名) 一并改为 CARD_FIELD3_THRESHOLD_1499。详见上 §新增 constants C5 双向核。

2. **EQUIP_ZONE_STATE_OFF = 0x4a0** (not a slot, computed at runtime):
   - Multiple functions compute `0x94<<3 = 0x4a0` inline (no .word slot) to index gDuelPhaseFlags. This constant is referenced in EQUIP_PHASE_FRAME_OFF's comment ("adjacent to phase code node +0x4a0") but has no named equate.
   - Action: no new .word slot needed (runtime computation). No EQ slot plan required. Noted for documentation.
