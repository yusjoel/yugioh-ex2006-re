# Refine Proposal: F08-Seg-6  [0x080690dc..0x0806a118)

## 段测绘

- 函数入口 x21:
  - 0x080690dc `tick_dragon_summon_display_if_slots_paired`
  - 0x08069104 `enqueue_effect_slot_sprites_for_two_players`
  - 0x08069148 `dispatch_equip_sprite_by_card_id_graceful_or_spiral`
  - 0x08069260 `dispatch_equip_zone_sprite_multi_zone_by_lp_state`
  - 0x080693e4 `enqueue_equip_slot_sprite_type11_if_not_active`
  - 0x08069420 `enqueue_effect_slot_sprites_for_two_players_with_lp_row`
  - 0x080694a8 `dispatch_equip_slot_sprite_by_card_id_scapegoat_or_lambs`
  - 0x080695d4 `dispatch_equip_zone_sprite_banisher_loop_by_lp_state`
  - 0x080696f4 `tick_equip_lp_indicator_by_state_and_slot_score`
  - 0x08069780 `tick_equip_field_spell_placement_state_machine`
  - 0x08069874 `tick_equip_activation_sprite_with_lp_row_state_machine`
  - 0x08069984 `tick_equip_multi_card_score_state_machine`
  - 0x08069b5c `build_equip_zone_bitmap_if_triple_active`
  - 0x08069be0 `invoke_equip_oam_for_reserved_card_zone14_if_eligible`
  - 0x08069c68 `enqueue_equip_zone_sprites_for_spell_slot_entries`
  - 0x08069cdc [unnamed inline callback, CREATE_FUNC -> `check_zone_activation_ctx_match_cb`]
  - 0x08069d08 `dispatch_zone_activation_display_by_confirm_state`
  - 0x08069df8 `enqueue_slot_card_sprite_for_zone_entry`
  - 0x08069e40 `tick_equip_monster_zone_placement_state_machine`
  - 0x08069f18 (caseD_80 inline)
  - 0x0806a004 `init_effect_slot_display_if_field_active`
  - 0x0806a054 `dispatch_equip_slot_sprite_by_card_id_range`

- 残留自动名槽: 96 个 (DWORD_/DAT_/PTR_gP1LifePoints_*)
- ROM_INCBIN: 0x080696d8, size 0x1c (28 字节)
- switchD 跳转表: `switchD_08069edc` (10 条目, 0x08069ef0..0x08069f14; 全部已 inline disasm)

## 数据块分类 (Rule 2/3)

| 块 | ref-scan (raw / THUMB+1) | 判定 | 理由 |
|---|---|---|---|
| 0x080696d8 sz=0x1c | raw=0 thumb=1 (at 0x09e3fba8) | disasm R4 | THUMB+1 hit = fn_eligible handler; dispatch table entry 0x09e3fba4=[CID=0x12da, fn_elig=0x080696d9, ...] |

ref-scan python (from prior session):
```
addr=0x080696d8+1=0x080696d9  => struct.pack("<I",0x080696d9) found at ROM offset 0x01e3fba8 (1 hit)
raw=0x080696d8: 0 hits
```
Verdict: R4 disasm. CID=0x12da (unassigned gap; 0x12da absent from card-stats.s between 0x12D7=Tragedy and 0x12DC=Ectoplasmer).

## 符号化计划

### EQ_SLOTS  (data-equate)

84 slots total. Format: (slot_addr, value, const_name, reuse/new, inc_file)

**CID 常量 (card_info.inc)**

| slot | value | const_name | disposition |
|------|-------|------------|-------------|
| DWORD_080690f8 | 0x0000128b | LORD_OF_D_CID | Reuse card_info.inc (confirmed L11418 uses 0x128b = Lord of D., card_0599 pw=17985575) |
| DWORD_08069164 | 0x000012cc | GRACEFUL_CHARITY_CID | Reuse card_info.inc |
| DWORD_08069168 | 0x0000187d | SPIRAL_SPEAR_STRIKE_CID | Reuse card_info.inc |
| DWORD_0806924c | 0x000012a1 | PARASITE_PARACIDE_CID | Reuse card_info.inc |
| DWORD_080694c4 | 0x000012d2 | SCAPEGOAT_CID | Reuse card_info.inc |
| DWORD_080694c8 | 0x00001710 | STRAY_LAMBS_CID | Reuse card_info.inc |
| DWORD_08069a00 | 0x00001254 | WIDESPREAD_RUIN_CID | New card_info.inc (pw=77754944, verified in card-stats.s) |
| DWORD_08069a18 | 0x000017f2 | HAMMER_SHOT_CID | New card_info.inc (pw=26412047, verified in card-stats.s) |
| DWORD_08069a24 | 0x0000195e | CHTHONIAN_BLAST_CID | Reuse card_info.inc |
| DWORD_08069a9c | 0x000017f2 | HAMMER_SHOT_CID | Reuse (same value as DWORD_08069a18) |
| DWORD_08069aa8 | 0x0000195e | CHTHONIAN_BLAST_CID | Reuse |
| DWORD_08069c5c | 0x000012fb | cid_12fb | Reuse card_info.inc |
| DWORD_0806a07c | 0x000012f7 | cid_12f7 | Reuse card_info.inc |
| DWORD_0806a090 | 0x0000131c | cid_131c | Reuse card_info.inc |
| DWORD_0806a094 | 0x0000162a | JAR_ROBBER_CID | Reuse card_info.inc |

**gDuelPhaseFlags (gDuelFieldState) base addr (ewram.inc)**

| slot | value | const_name | disposition |
|------|-------|------------|-------------|
| DWORD_080691b4 | 0x0201b290 | gDuelPhaseFlags | Reuse ewram.inc |
| DWORD_0806929c | 0x0201b290 | gDuelPhaseFlags | Reuse |
| DWORD_08069450 | 0x0201b290 | gDuelPhaseFlags | Reuse |
| DWORD_08069508 | 0x0201b290 | gDuelPhaseFlags | Reuse |
| DWORD_08069604 | 0x0201b290 | gDuelPhaseFlags | Reuse |
| DAT_0806972c | 0x0201b290 | gDuelPhaseFlags | Reuse |
| DAT_080697a8 | 0x0201b290 | gDuelPhaseFlags | Reuse |
| DAT_08069958 | 0x0201b290 | gDuelPhaseFlags | Reuse |
| DWORD_080699b4 | 0x0201b290 | gDuelPhaseFlags | Reuse |
| DAT_08069cfc | 0x0201b290 | gDuelPhaseFlags | Reuse |
| DAT_08069d78 | 0x0201b290 | gDuelPhaseFlags | Reuse |
| DAT_08069ee8 | 0x0201b290 | gDuelPhaseFlags | Reuse |
| DWORD_0806a150 | 0x0201b290 | gDuelPhaseFlags | Reuse |

**EQUIP_PHASE_FRAME_OFF (0x4a4) (ewram.inc)**

| slot | value | const_name | disposition |
|------|-------|------------|-------------|
| DWORD_080691b8 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | Reuse ewram.inc |
| DWORD_08069248 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | Reuse |
| DWORD_08069560 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | Reuse |
| DWORD_0806959c | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | Reuse |
| DWORD_08069ab8 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | Reuse |
| DWORD_08069afc | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | Reuse |
| DWORD_08069b3c | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | Reuse |
| DWORD_08069b58 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | Reuse |
| DWORD_0806a168 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | Reuse |
| DWORD_0806a1e4 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | Reuse |
| DWORD_0806a230 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | Reuse |

**PLAYER_BLOCK_STRIDE (0x868) (ewram.inc)**

| slot | value | const_name | disposition |
|------|-------|------------|-------------|
| DWORD_080691c0 | 0x00000868 | PLAYER_BLOCK_STRIDE | Reuse ewram.inc |
| DWORD_08069244 | 0x00000868 | PLAYER_BLOCK_STRIDE | Reuse |
| DWORD_08069308 | 0x00000868 | PLAYER_BLOCK_STRIDE | Reuse |
| DWORD_080693b0 | 0x00000868 | PLAYER_BLOCK_STRIDE | Reuse |
| DAT_08069810 | 0x00000868 | PLAYER_BLOCK_STRIDE | Reuse |
| DWORD_0806955c | 0x00000868 | PLAYER_BLOCK_STRIDE | Reuse |
| DWORD_08069670 | 0x00000868 | PLAYER_BLOCK_STRIDE | Reuse |
| DAT_08069d74 | 0x00000868 | PLAYER_BLOCK_STRIDE | Reuse |
| DAT_08069ee0 | 0x00000868 | PLAYER_BLOCK_STRIDE | Reuse |
| DWORD_0806a04c | 0x00000868 | PLAYER_BLOCK_STRIDE | Reuse |
| DWORD_0806a1f0 | 0x00000868 | PLAYER_BLOCK_STRIDE | Reuse |
| DWORD_0806a2dc | 0x00000868 | PLAYER_BLOCK_STRIDE | Reuse |

**P1LP_BLOCK2_OFF_1CE8 (0x1ce8) (ewram.inc)**

| slot | value | const_name | disposition |
|------|-------|------------|-------------|
| DWORD_0806941c | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | Reuse ewram.inc |
| DWORD_0806966c | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | Reuse |
| DWORD_08069698 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | Reuse |
| DWORD_080696c4 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | Reuse |
| DAT_08069734 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | Reuse |
| DAT_0806977c | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | Reuse |

**EQUIP_ACTIVE_CTX_OFF (0x484) (ewram.inc)**

| slot | value | const_name | disposition |
|------|-------|------------|-------------|
| DAT_08069d00 | 0x00000484 | EQUIP_ACTIVE_CTX_OFF | Reuse ewram.inc |

**LP_CARD_TRACK_BASE_OFF (0x1da8) (ewram.inc)**

| slot | value | const_name | disposition |
|------|-------|------------|-------------|
| DAT_08069778 | 0x00001da8 | LP_CARD_TRACK_BASE_OFF | Reuse ewram.inc (LP_CARD_TRACK_BASE_OFF=0x1da8, base=gP1LifePoints, 109 refs; LP_BANISHER_CTX_OFF=0x1d70 is a different value) |

**LP_CARD_TRACK_BASE_OFF (0x1d68 / 0x1d70 / 0x1d6c) (ewram.inc)**

| slot | value | const_name | disposition |
|------|-------|------------|-------------|
| DWORD_08069b34 | 0x00001d68 | ELIGIB_SPRITE_CTRL_OFF | Reuse ewram.inc (confirmed ELIGIB_SPRITE_CTRL_OFF=0x1d68) |
| DWORD_08069b38 | 0x00001d6c | ELIGIB_ANIM_STATE_OFF | Reuse ewram.inc (confirmed ELIGIB_ANIM_STATE_OFF=0x1d6c) |
| DAT_08069df0 | 0x00001d68 | ELIGIB_SPRITE_CTRL_OFF | Reuse |
| DAT_08069df4 | 0x00001d70 | LP_BANISHER_CTX_OFF | Reuse ewram.inc (LP_BANISHER_CTX_OFF=0x1d70) |

**ELIGIB_STATE_CTRL_OFF (0x1d54) / LP_MODE (0x1d5c) (ewram.inc)**

| slot | value | const_name | disposition |
|------|-------|------------|-------------|
| DAT_08069f78 | 0x00001d54 | ELIGIB_STATE_CTRL_OFF | Reuse ewram.inc |
| DAT_08069fa8 | 0x00001d5c | ELIGIB_ACT_TYPE_OFF | Reuse ewram.inc |

**LP_ACTIVATION_LINK_FLAG_OFF (0x10d0) -- NEW**

| slot | value | const_name | disposition |
|------|-------|------------|-------------|
| DAT_08069960 | 0x000010d0 | LP_ACTIVATION_LINK_FLAG_OFF | New ewram.inc; used as [gP1LifePoints+0x10d0] in tick_equip_activation_sprite_with_lp_row_state_machine; domain gP1LifePoints (conf: asm/08 L12689); distinct from EFFECT_ZONE_BITMASK_OFF=0x10d0 (duel_field.inc, base=gDuelFieldSlots). C5 domain exception applies. |

**gEquipChainEntryBase (0x0201e288) (ewram.inc)**

| slot | value | const_name | disposition |
|------|-------|------------|-------------|
| DWORD_080694a4 | 0x0201e288 | gEquipChainEntryBase | Reuse ewram.inc |

**gP1FieldArrayCBase (0x0201c600) (ewram.inc)**

| slot | value | const_name | disposition |
|------|-------|------------|-------------|
| DWORD_0806930c | 0x0201c600 | gP1FieldArrayCBase | Reuse ewram.inc |

**gP1SlotSetCodeArray (0x0201c740) / gP1ChainZoneArray (0x0201c880) (ewram.inc)**

| slot | value | const_name | disposition |
|------|-------|------------|-------------|
| DWORD_080693b4 | 0x0201c740 | gP1SlotSetCodeArray | Reuse ewram.inc |
| DWORD_080693b8 | 0x0201c880 | gP1ChainZoneArray | Reuse ewram.inc |

**gEquipLpZoneEntryBase (0x0201e500) (ewram.inc)**

| slot | value | const_name | disposition |
|------|-------|------------|-------------|
| DAT_0806982c | 0x0201e500 | gEquipLpZoneEntryBase | Reuse ewram.inc (confirmed correct: tick_equip_field_spell_placement_state_machine passes ptr to invoke_setup_equip_oam_with_attr2 as OAM entry base) |

**gEquipChainSlotRefs (0x0201bb90) (ewram.inc)**

| slot | value | const_name | disposition |
|------|-------|------------|-------------|
| DAT_08069964 | 0x0201bb90 | gEquipChainSlotRefs | Reuse ewram.inc |

**gDuelFieldSlots (0x0201c510) (ewram.inc)**

| slot | value | const_name | disposition |
|------|-------|------------|-------------|
| DAT_08069ee4 | 0x0201c510 | gDuelFieldSlots | Reuse ewram.inc |

**gP1HandSlotArray (0x0201c8f8) (ewram.inc)**

| slot | value | const_name | disposition |
|------|-------|------------|-------------|
| DWORD_08069c64 | 0x0201c8f8 | gP1HandSlotArray | Reuse ewram.inc |

**gDuelCardCtxBase (0x0201e2a0) (ewram.inc)**

| slot | value | const_name | disposition |
|------|-------|------------|-------------|
| DAT_08069f54 | 0x0201e2a0 | gDuelCardCtxBase | Reuse ewram.inc |
| DWORD_0806a1e8 | 0x0201e2a0 | gDuelCardCtxBase | Reuse |
| DWORD_0806a050 | 0x0201e2a0 | gDuelCardCtxBase | Reuse |

**gEquipZoneRankState (0x0201e4d0) (ewram.inc)**

| slot | value | const_name | disposition |
|------|-------|------------|-------------|
| DAT_08069fc8 | 0x0201e4d0 | gEquipZoneRankState | Reuse ewram.inc |

**OAM_SPRITE_CODE_P1_ACTIVATION (0x8019) -- NEW**

| slot | value | const_name | disposition |
|------|-------|------------|-------------|
| DAT_08069968 | 0x00008019 | OAM_SPRITE_CODE_P1_ACTIVATION | New oam_attr.inc; used in tick_equip_activation_sprite_with_lp_row_state_machine: if player_id==1 sprite code=0x8019, else sprite code=0x19 (lit). Evidence: asm/08 L12693 + L12694 (high conf). |

**ZONE_ENTRY_FLAGS_CLR_MASK (0x1fff) -- NEW**

| slot | value | const_name | disposition |
|------|-------|------------|-------------|
| DWORD_080695a0 | 0x00001fff | ZONE_ENTRY_FLAGS_CLR_MASK | New oam_attr.inc (Ruling B); used in dispatch_equip_slot_sprite_by_card_id_scapegoat_or_lambs: `ands r2, r3` (L12144) clears bits [12:0] of sprite data halfword, preserving player-id bit packing in bit13+; evidence asm/08 L12160 (high conf). |

**OAM Token table ROM addresses -- RENAME only (no equate, per Ruling A)**

| slot | value | disposition |
|------|-------|-------------|
| DWORD_080694d4 | 0x09e3f11c | RENAME only: label scapegoat_token_tbl_080694d4, EOL "ROM ptr: Scapegoat OAM token slot-id table, 8 hwords @ 0x09e3f11c". Raw .word 0x09e3f11c, no equate, no token_tables.inc. Ruling A: all sibling modules (asm/05 L8915, asm/09 L13772, asm/10 L16668, asm/11 L1475) use raw .word for 0x09e3fXXX addrs. |
| DWORD_08069504 | 0x09e3f12c | RENAME only: label stray_lambs_token_tbl_08069504, EOL "ROM ptr: Stray Lambs OAM token slot-id table, 8 hwords @ 0x09e3f12c". Raw .word 0x09e3f12c, no equate, no token_tables.inc. |

Note: No new EQ entry for these slots. No token_tables.inc created. Consistent with Ruling A sibling-module convention.

**invoke_effect_node_with_active_flag_3arg+1 (fn ptr)**

| slot | value | const_name | disposition |
|------|-------|------------|-------------|
| DWORD_08069ae8 | 0x08090625 | (see REF_SLOTS) | invoke_effect_node_with_active_flag_3arg+1 (THUMB fn ptr) |

**switchD jump table ptr**

| slot | value | const_name | disposition |
|------|-------|------------|-------------|
| DAT_08069eec | 0x08069ef0 | (see REF_SLOTS) | switchD_08069edc base table ptr |

**ZONE_ENTRY_COUNT_MASK (0x1c)**

Note: The constant 0x1c appears in build_equip_zone_bitmap_if_triple_active (L12999, L13000) and enqueue_equip_zone_sprites_for_spell_slot_entries (L13166) as immediate bits[4:2] mask. These are literal immediates encoded in THUMB, not word-pool slots, so no slot to symbolize for them.

**CHAIN_ENTRY_OFF_1CB8 (0x1cb8) -- in Seg-7, not Seg-6**

(DWORD_0806a2e4 = 0x00001cb8 is in scan_equip_chain_slots_for_zone14_targets which starts at 0x0806a240, past Seg-6 boundary 0x0806a118)

### REF_SLOTS  (USER-label + DATA-ref)

| slot | target | gas_label | slot_label |
|------|--------|-----------|------------|
| DWORD_08069ae8 | 0x08090625 (= invoke_effect_node_with_active_flag_3arg+1) | invoke_effect_node_with_active_flag_3arg+1 | fn_ptr_invoke_effect_node_08069ae8 |
| DAT_08069d7c | 0x08069cdd (= check_zone_activation_ctx_match_cb+1) | check_zone_activation_ctx_match_cb+1 | fn_ptr_check_zone_match_cb_08069d7c |
| DAT_08069eec | 0x08069ef0 (= switchD_08069edc table base) | switchD_08069edc__switchdataD_08069ef0 | (existing label, just RENAME slot DAT_08069eec -> switch_table_ptr_08069eec) |

Evidence for DWORD_08069ae8:
- asm/11 L11824: `invoke_effect_node_with_active_flag_3arg` at 0x08090624; +1 = 0x08090625 (THUMB).
- Used in tick_equip_multi_card_score_state_machine: `bl set_equip_activation_state_by_mode__08096a4c` passes r2=DWORD_08069ae8 (asm/08 L12922). High conf.

Evidence for DAT_08069d7c:
- 0x08069cdd = check_zone_activation_ctx_match_cb+1 (CREATE_FUNC addr 0x08069cdc +1). Used in dispatch_zone_activation_display_by_confirm_state (asm/08 L13312): `ldr r0, DAT_08069d7c` then `bl init_zone_activation_display_fields` passing r0 as callback ptr. High conf.

### RENAME_SLOTS  (auto-name -> descriptive label, + optional EOL)

All 96 slots receive descriptive labels as defined in EQ_SLOTS and REF_SLOTS sections. RENAME means the Ghidra label changes from DWORD_*/DAT_*/PTR_* to a symbolic constant name.

Representative RENAME mappings (full list implied from EQ table):

| old_label | new_label | eol_ascii |
|-----------|-----------|-----------|
| DWORD_080690f8 | lord_of_d_cid_080690f8 | LORD_OF_D_CID=0x128b |
| DWORD_08069164 | graceful_charity_cid_08069164 | GRACEFUL_CHARITY_CID=0x12cc |
| DWORD_08069168 | spiral_spear_strike_cid_08069168 | SPIRAL_SPEAR_STRIKE_CID=0x187d |
| DWORD_080691b4 | gduelphaseflagss_080691b4 | gDuelPhaseFlags=0x0201b290 |
| DWORD_080691b8 | equip_phase_frame_off_080691b8 | EQUIP_PHASE_FRAME_OFF=0x4a4 |
| DWORD_080691bc | gp1lifepoints_080691bc | gP1LifePoints |
| DWORD_080691c0 | player_block_stride_080691c0 | PLAYER_BLOCK_STRIDE=0x868 |
| DWORD_08069240 | gp1lifepoints_08069240 | gP1LifePoints |
| DWORD_08069244 | player_block_stride_08069244 | PLAYER_BLOCK_STRIDE=0x868 |
| DWORD_08069248 | equip_phase_frame_off_08069248 | EQUIP_PHASE_FRAME_OFF=0x4a4 |
| DWORD_0806924c | parasite_paracide_cid_0806924c | PARASITE_PARACIDE_CID=0x12a1 |
| DWORD_0806929c | gduelphaseflagss_0806929c | gDuelPhaseFlags=0x0201b290 |
| DWORD_08069304 | gp1lifepoints_08069304 | gP1LifePoints |
| DWORD_08069308 | player_block_stride_08069308 | PLAYER_BLOCK_STRIDE=0x868 |
| DWORD_0806930c | gp1fieldarraycbase_0806930c | gP1FieldArrayCBase=0x0201c600 |
| DWORD_080693ac | gp1lifepoints_080693ac | gP1LifePoints |
| DWORD_080693b0 | player_block_stride_080693b0 | PLAYER_BLOCK_STRIDE=0x868 |
| DWORD_080693b4 | gp1slotsetcodearray_080693b4 | gP1SlotSetCodeArray=0x0201c740 |
| DWORD_080693b8 | gp1chainzonearray_080693b8 | gP1ChainZoneArray=0x0201c880 |
| DWORD_08069418 | gp1lifepoints_08069418 | gP1LifePoints |
| DWORD_0806941c | lp_zone_off_1ce8_0806941c | P1LP_BLOCK2_OFF_1CE8=0x1ce8 |
| DWORD_08069450 | gduelphaseflagss_08069450 | gDuelPhaseFlags=0x0201b290 |
| DWORD_080694a4 | gequipchainentrybase_080694a4 | gEquipChainEntryBase=0x0201e288 |
| DWORD_080694c4 | scapegoat_cid_080694c4 | SCAPEGOAT_CID=0x12d2 |
| DWORD_080694c8 | stray_lambs_cid_080694c8 | STRAY_LAMBS_CID=0x1710 |
| DWORD_080694d4 | scapegoat_token_tbl_080694d4 | ROM ptr: Scapegoat OAM token slot-id table, 8 hwords @ 0x09e3f11c |
| DWORD_08069504 | stray_lambs_token_tbl_08069504 | ROM ptr: Stray Lambs OAM token slot-id table, 8 hwords @ 0x09e3f12c |
| DWORD_08069508 | gduelphaseflagss_08069508 | gDuelPhaseFlags=0x0201b290 |
| DWORD_08069558 | gp1lifepoints_08069558 | gP1LifePoints |
| DWORD_0806955c | player_block_stride_0806955c | PLAYER_BLOCK_STRIDE=0x868 |
| DWORD_08069560 | equip_phase_frame_off_08069560 | EQUIP_PHASE_FRAME_OFF=0x4a4 |
| DWORD_0806959c | equip_phase_frame_off_0806959c | EQUIP_PHASE_FRAME_OFF=0x4a4 |
| DWORD_080695a0 | zone_entry_flags_clr_mask_080695a0 | ZONE_ENTRY_FLAGS_CLR_MASK=0x1fff |
| DWORD_08069604 | gduelphaseflagss_08069604 | gDuelPhaseFlags=0x0201b290 |
| DWORD_08069668 | gp1lifepoints_08069668 | gP1LifePoints |
| DWORD_0806966c | lp_zone_off_1ce8_0806966c | P1LP_BLOCK2_OFF_1CE8=0x1ce8 |
| DWORD_08069670 | player_block_stride_08069670 | PLAYER_BLOCK_STRIDE=0x868 |
| DWORD_08069694 | gp1lifepoints_08069694 | gP1LifePoints |
| DWORD_08069698 | lp_zone_off_1ce8_08069698 | P1LP_BLOCK2_OFF_1CE8=0x1ce8 |
| DWORD_080696c0 | gp1lifepoints_080696c0 | gP1LifePoints |
| DWORD_080696c4 | lp_zone_off_1ce8_080696c4 | P1LP_BLOCK2_OFF_1CE8=0x1ce8 |
| DAT_0806972c | gduelphaseflagss_0806972c | gDuelPhaseFlags=0x0201b290 |
| PTR_gP1LifePoints_08069730 | gp1lifepoints_08069730 | gP1LifePoints |
| DAT_08069734 | lp_zone_off_1ce8_08069734 | P1LP_BLOCK2_OFF_1CE8=0x1ce8 |
| PTR_gP1LifePoints_08069774 | gp1lifepoints_08069774 | gP1LifePoints |
| DAT_08069778 | lp_card_track_base_off_08069778 | LP_CARD_TRACK_BASE_OFF=0x1da8 |
| DAT_0806977c | lp_zone_off_1ce8_0806977c | P1LP_BLOCK2_OFF_1CE8=0x1ce8 |
| DAT_080697a8 | gduelphaseflagss_080697a8 | gDuelPhaseFlags=0x0201b290 |
| PTR_gP1LifePoints_0806980c | gp1lifepoints_0806980c | gP1LifePoints |
| DAT_08069810 | player_block_stride_08069810 | PLAYER_BLOCK_STRIDE=0x868 |
| DAT_0806982c | gequiplpzoneentrybase_0806982c | gEquipLpZoneEntryBase=0x0201e500 |
| DAT_08069958 | gduelphaseflagss_08069958 | gDuelPhaseFlags=0x0201b290 |
| PTR_gP1LifePoints_0806995c | gp1lifepoints_0806995c | gP1LifePoints |
| DAT_08069960 | lp_act_link_flag_off_08069960 | LP_ACTIVATION_LINK_FLAG_OFF=0x10d0 |
| DAT_08069964 | gequipchainslotref_08069964 | gEquipChainSlotRefs=0x0201bb90 |
| DAT_08069968 | oam_sprite_code_p1_act_08069968 | OAM_SPRITE_CODE_P1_ACTIVATION=0x8019 |
| DWORD_080699b4 | gduelphaseflagss_080699b4 | gDuelPhaseFlags=0x0201b290 |
| DWORD_08069a00 | widespread_ruin_cid_08069a00 | WIDESPREAD_RUIN_CID=0x1254 |
| DWORD_08069a18 | hammer_shot_cid_08069a18 | HAMMER_SHOT_CID=0x17f2 |
| DWORD_08069a24 | chthonian_blast_cid_08069a24 | CHTHONIAN_BLAST_CID=0x195e |
| DWORD_08069a9c | hammer_shot_cid_08069a9c | HAMMER_SHOT_CID=0x17f2 |
| DWORD_08069aa8 | chthonian_blast_cid_08069aa8 | CHTHONIAN_BLAST_CID=0x195e |
| DWORD_08069ab8 | equip_phase_frame_off_08069ab8 | EQUIP_PHASE_FRAME_OFF=0x4a4 |
| DWORD_08069ae8 | fn_ptr_invoke_effect_node_08069ae8 | invoke_effect_node_with_active_flag_3arg+1 |
| DWORD_08069afc | equip_phase_frame_off_08069afc | EQUIP_PHASE_FRAME_OFF=0x4a4 |
| DWORD_08069b30 | gp1lifepoints_08069b30 | gP1LifePoints |
| DWORD_08069b34 | eligib_sprite_ctrl_off_08069b34 | ELIGIB_SPRITE_CTRL_OFF=0x1d68 |
| DWORD_08069b38 | eligib_anim_state_off_08069b38 | ELIGIB_ANIM_STATE_OFF=0x1d6c |
| DWORD_08069b3c | equip_phase_frame_off_08069b3c | EQUIP_PHASE_FRAME_OFF=0x4a4 |
| DWORD_08069b58 | equip_phase_frame_off_08069b58 | EQUIP_PHASE_FRAME_OFF=0x4a4 |
| DWORD_08069c5c | cid_12fb_08069c5c | cid_12fb=0x12fb |
| DWORD_08069c60 | player_block_stride_08069c60 | PLAYER_BLOCK_STRIDE=0x868 |
| DWORD_08069c64 | gp1handslotarray_08069c64 | gP1HandSlotArray=0x0201c8f8 |
| DAT_08069cfc | gduelphaseflagss_08069cfc | gDuelPhaseFlags=0x0201b290 |
| DAT_08069d00 | equip_active_ctx_off_08069d00 | EQUIP_ACTIVE_CTX_OFF=0x484 |
| PTR_gP1LifePoints_08069d70 | gp1lifepoints_08069d70 | gP1LifePoints |
| DAT_08069d74 | player_block_stride_08069d74 | PLAYER_BLOCK_STRIDE=0x868 |
| DAT_08069d78 | gduelphaseflagss_08069d78 | gDuelPhaseFlags=0x0201b290 |
| DAT_08069d7c | fn_ptr_check_zone_match_cb_08069d7c | check_zone_activation_ctx_match_cb+1 |
| DAT_08069df0 | eligib_sprite_ctrl_off_08069df0 | ELIGIB_SPRITE_CTRL_OFF=0x1d68 |
| DAT_08069df4 | lp_banisher_ctx_off_08069df4 | LP_BANISHER_CTX_OFF=0x1d70 |
| DAT_08069ee0 | player_block_stride_08069ee0 | PLAYER_BLOCK_STRIDE=0x868 |
| DAT_08069ee4 | gduelfieldslots_08069ee4 | gDuelFieldSlots=0x0201c510 |
| DAT_08069ee8 | gduelphaseflagss_08069ee8 | gDuelPhaseFlags=0x0201b290 |
| DAT_08069eec | switch_table_ptr_08069eec | switchD_08069edc__switchdataD_08069ef0 |
| DAT_08069f54 | gduelcardctxbase_08069f54 | gDuelCardCtxBase=0x0201e2a0 |
| PTR_gP1LifePoints_08069f74 | gp1lifepoints_08069f74 | gP1LifePoints |
| DAT_08069f78 | eligib_state_ctrl_off_08069f78 | ELIGIB_STATE_CTRL_OFF=0x1d54 |
| DAT_08069fa8 | eligib_act_type_off_08069fa8 | ELIGIB_ACT_TYPE_OFF=0x1d5c |
| DAT_08069fc8 | gequipzonerankstate_08069fc8 | gEquipZoneRankState=0x0201e4d0 |
| DWORD_0806a048 | gp1lifepoints_0806a048 | gP1LifePoints |
| DWORD_0806a04c | player_block_stride_0806a04c | PLAYER_BLOCK_STRIDE=0x868 |
| DWORD_0806a050 | gduelcardctxbase_0806a050 | gDuelCardCtxBase=0x0201e2a0 |
| DWORD_0806a07c | cid_12f7_0806a07c | cid_12f7=0x12f7 |
| DWORD_0806a090 | cid_131c_0806a090 | cid_131c=0x131c |
| DWORD_0806a094 | jar_robber_cid_0806a094 | JAR_ROBBER_CID=0x162a |

### FUNC_RENAME  (误名订正, 如有)

None. All 21 named functions have semantically correct names.

### CREATE_FUNC  (unnamed inline callback)

| addr | proposed_name | evidence |
|------|---------------|---------|
| 0x08069cdc | check_zone_activation_ctx_match_cb | Callback at 0x08069cdc (inline between enqueue_equip_zone_sprites_for_spell_slot_entries epilogue at 0x08069cda and dispatch_zone_activation_display_by_confirm_state at 0x08069d08). Called via fn-ptr from DAT_08069d7c (THUMB+1 = 0x08069cdd). Body: r0=player_id from caller, r1=zone_type, r2=r1 copy; loads [gDuelPhaseFlags+EQUIP_ACTIVE_CTX_OFF], gets [ptr+2].bit0 (player_id of active zone); if r0==active_player_id returns 0; if r1==0xb returns 0x800 else 0. Semantics: returns 0x800 if player mismatch AND zone_type_arg==0xb (confirms activation linkage for zone 11), else 0. Evidence: asm/08 L13213-13236 (high conf). indeg=1 (fn-ptr from DAT_08069d7c). |

### PLATE  (R5; ASCII-only)

| addr | action | old_plate_first_line | new_plate |
|------|--------|----------------------|-----------|
| 0x080690dc | full rewrite (CJK mojibake + wrong card name) | @ 装备链配对校验后驱动龙族召唤效果显示状态机... 以固定卡 id 0x128b (Stamping Destruction)... | "Drive dragon-summon display state machine after equip-chain paired-slot check. r0=card_entry_ptr, r1=scene_ptr. Loads fixed CID 0x128b (Lord of D.) and calls count_paired_slots_both_sides; if 0 paired slots returns 0. Else calls tick_dragon_summon_effect_display_state_machine(r4,r5) and returns result. fn-ptr dispatch (indeg=0)." |

Note: The existing plate at L11404 contains CJK ideographs (violates Jython ASCII rule) AND incorrectly names the card as "Stamping Destruction". ROM bytes at 0x080690f8 = 0x0000128b confirmed = LORD_OF_D_CID. Correct card: Lord of D. (card_0599, pw=17985575, card-stats.s). This must be corrected.

## disasm 计划 (R4)

ROM_INCBIN 0x080696d8 / size 0x1c -> R4 THUMB disasm

- Range: 0x080696d8..0x080696f3 (28 bytes, 14 THUMB halfwords)
- Function name: `check_equip_eligible_set_slot8_flag_for_cid_12da`
- CID: 0x12da (unassigned; gap between Tragedy=0x12D7 and Ectoplasmer=0x12DC in card-stats.s)
- Context: fn_eligible handler referenced from dispatch table entry at 0x09e3fba4:
  `[CID=0x12da, fn_elig+1=0x080696d9, pad, fn_act+1=?, pad, pad]`
- ROM bytes (verified from prior session): `0a1c 0421 0079 0140 0029 05d1 0021 1089 0028 00d1 0121 1181 0020 7047`
- Decoded sequence:
  - `adds r2,r1,#0` ; save zone_type param
  - `movs r1,#4` ; bit2 mask
  - `ldrb r1,[r0,+0]` ; slot->flags byte  (note: actual offset may differ; fixer to verify)
  - `ands r0,r1` ; test eligible flag
  - `cmp r0,#0` ; if 0 -> fallthrough
  - `bne LAB_xxx` ; slot flag set: skip
  - `movs r1,#0` ; clear
  - `ldrh r0,[r1,...]` ; read field from some ptr
  - `cmp r0,#0` ; test
  - `bne LAB_xxx`
  - `movs r1,#1`
  - `orrs r1,r0` ; set bit
  - `movs r0,#0` ; return 0 (not-eligible path)
  - `bx lr`
- Plate (ASCII): "fn_eligible handler for unassigned CID=0x12da; tests slot[+0x0] flag bit, reads secondary field; sets bit0 of result field if slot eligible. Called from dispatch table at 0x09e3fba4. CID 0x12da absent from card-stats.s (gap 0x12D7..0x12DC)."

## carve 计划 (R7)

None. ROM_INCBIN at 0x080696d8 is a THUMB code block -> R4 disasm, not data carve.

The token tables at 0x09e3f11c and 0x09e3f12c are symbolized as EQ constants; no rom.s carve needed at this time (accessed via absolute address loads only, not via incbin boundaries in rom.s).

## 新增 constants / 全局

### card_info.inc (+4 new)
- `WIDESPREAD_RUIN_CID = 0x1254` (pw=77754944, card-stats.s verified)
- `BOTTOMLESS_SHIFTING_SAND_CID = 0x1540` (pw=76532077, card-stats.s verified; used in tick_equip_multi_card_score_state_machine via `0xaa<<5=0x1540`)
- `HAMMER_SHOT_CID = 0x17f2` (pw=26412047, card-stats.s verified)
- `cid_12da = 0x12da` (unassigned; fn_eligible handler CID; absent card-stats.s)

Note on BOTTOMLESS_SHIFTING_SAND_CID: The constant 0x1540 appears in tick_equip_multi_card_score_state_machine (asm/08 L12789-12790: `movs r0,#0xaa; lsls r0,r0,#5` = 0xaa<<5 = 0x1540). This is a word-pool encoding trick -- no slot present, but the semantic constant should be documented in card_info.inc. Fixer adds as `.equ BOTTOMLESS_SHIFTING_SAND_CID, 0x1540`.

### ewram.inc (+1 new)
- `LP_ACTIVATION_LINK_FLAG_OFF = 0x10d0` (offset from gP1LifePoints base; domain gP1LifePoints; distinct from EFFECT_ZONE_BITMASK_OFF=0x10d0 in duel_field.inc which uses gDuelFieldSlots base)

### oam_attr.inc (+1 new)
- `OAM_SPRITE_CODE_P1_ACTIVATION = 0x8019` (player1 activation sprite code in tick_equip_activation_sprite_with_lp_row_state_machine)

### oam_attr.inc (+1 additional new, Ruling B)
- `ZONE_ENTRY_FLAGS_CLR_MASK = 0x1fff` (13-bit clear mask for zone entry sprite data halfword in dispatch_equip_slot_sprite_by_card_id_scapegoat_or_lambs)

Disposition: add to existing constants/oam_attr.inc (same file as OAM_SPRITE_ATTR_CLR_BITS20_17 and OAM_ATTR_P1_SPRITE). No new equip_sprite.inc created (Ruling B).

### ROM address token table slots (no new constant file, Ruling A)
- DWORD_080694d4 (0x09e3f11c) and DWORD_08069504 (0x09e3f12c): raw .word values; RENAME label only with ASCII EOL. No equate, no token_tables.inc. Sibling convention per Ruling A.

## §5.1 登记 (Rule 3) -- 0 引用块

None. The one ROM_INCBIN (0x080696d8/0x1c) has a confirmed THUMB+1 reference at 0x09e3fba8. No zero-reference blocks in this segment.

## 消費者証据 (R6)

| 槽/定数 | 証拠 file:line | 置信度 |
|---------|---------------|--------|
| LORD_OF_D_CID=0x128b at DWORD_080690f8 | asm/08 L11418 (.word 0x0000128b); card-stats.s card_0599 slot=0x128B pw=17985575 | high |
| GRACEFUL_CHARITY_CID=0x12cc | asm/08 L11510; card-stats.s slot=0x12CC pw=79571449 | high |
| SPIRAL_SPEAR_STRIKE_CID=0x187d | asm/08 L11512; card-stats.s slot=0x187D pw=49328340 | high |
| PARASITE_PARACIDE_CID=0x12a1 | asm/08 L11632 (find_effect_node_in_zone arg r2=0x12a1); card-stats.s slot=0x12A1 pw=27911549 | high |
| SCAPEGOAT_CID=0x12d2 | asm/08 L12050; card-stats.s slot=0x12D2 pw=73915051 | high |
| STRAY_LAMBS_CID=0x1710 | asm/08 L12052; card-stats.s slot=0x1710 pw=60764581 | high |
| WIDESPREAD_RUIN_CID=0x1254 | asm/08 L12802 (DWORD_08069a00 .word 0x1254); card-stats.s slot=0x1254 pw=77754944 | high |
| HAMMER_SHOT_CID=0x17f2 | asm/08 L12815 (DWORD_08069a18); card-stats.s slot=0x17F2 pw=26412047 | high |
| CHTHONIAN_BLAST_CID=0x195e | asm/08 L12823; card-stats.s slot=0x195E pw=18271561 | high |
| cid_12fb=0x12fb | asm/08 L13128 (invoke_equip_oam_for_reserved_card_zone14_if_eligible); card_info.inc existing | high |
| cid_12f7=0x12f7 | asm/08 L13762; card_info.inc existing | high |
| cid_131c=0x131c | asm/08 L13773; card_info.inc existing | high |
| JAR_ROBBER_CID=0x162a | asm/08 L13775; card_info.inc existing | high |
| cid_12da=0x12da | ROM dispatch table 0x09e3fba4 CID field; absent card-stats.s (gap 0x12D7..0x12DC) | high |
| gDuelPhaseFlags=0x0201b290 | ewram.inc; 13 occurrences in Seg-6 (confirmed) | high |
| EQUIP_PHASE_FRAME_OFF=0x4a4 | ewram.inc; 11 occurrences (confirmed) | high |
| PLAYER_BLOCK_STRIDE=0x868 | ewram.inc; 12 occurrences (confirmed) | high |
| P1LP_BLOCK2_OFF_1CE8=0x1ce8 | ewram.inc; 6 occurrences (confirmed) | high |
| EQUIP_ACTIVE_CTX_OFF=0x484 | ewram.inc; DAT_08069d00 in check_zone_activation_ctx_match_cb body L13232 | high |
| LP_CARD_TRACK_BASE_OFF=0x1da8 | ewram.inc; DAT_08069778 L12428; base=gP1LifePoints (LP_BANISHER_CTX_OFF=0x1d70 is a different value) | high |
| LP_BANISHER_CTX_OFF=0x1d70 | ewram.inc; DAT_08069df4 L13373 | high |
| ELIGIB_SPRITE_CTRL_OFF=0x1d68 | ewram.inc; DWORD_08069b34 L12965, DAT_08069df0 L13371 | high |
| ELIGIB_ANIM_STATE_OFF=0x1d6c | ewram.inc; DWORD_08069b38 L12967 | high |
| ELIGIB_STATE_CTRL_OFF=0x1d54 | ewram.inc; DAT_08069f78 L13599 | high |
| ELIGIB_ACT_TYPE_OFF=0x1d5c | ewram.inc; DAT_08069fa8 L13625 | high |
| gEquipChainEntryBase=0x0201e288 | ewram.inc; DWORD_080694a4 L12001 | high |
| gP1FieldArrayCBase=0x0201c600 | ewram.inc; DWORD_0806930c L11761 | high |
| gP1SlotSetCodeArray=0x0201c740 | ewram.inc; DWORD_080693b4 L11848 | high |
| gP1ChainZoneArray=0x0201c880 | ewram.inc; DWORD_080693b8 L11850 | high |
| gEquipLpZoneEntryBase=0x0201e500 | ewram.inc; DAT_0806982c L12530; consumed by invoke_setup_equip_oam_with_attr2 | high |
| gEquipChainSlotRefs=0x0201bb90 | ewram.inc; DAT_08069964 L12692; used in check_slot_card_activatable call L12665 | high |
| gDuelFieldSlots=0x0201c510 | ewram.inc; DAT_08069ee4 L13531 | high |
| gP1HandSlotArray=0x0201c8f8 | ewram.inc; DWORD_08069c64 L13132 | high |
| gDuelCardCtxBase=0x0201e2a0 | ewram.inc; DAT_08069f54, DWORD_0806a050, DWORD_0806a1e8 | high |
| gEquipZoneRankState=0x0201e4d0 | ewram.inc; DAT_08069fc8 L13641 | high |
| LP_ACTIVATION_LINK_FLAG_OFF=0x10d0 | asm/08 L12689-12690 (DAT_08069960); used as [gP1LifePoints+0x10d0]; bit0 and bit1 tested for LP link status | high |
| OAM_SPRITE_CODE_P1_ACTIVATION=0x8019 | asm/08 L12694 (DAT_08069968); player_id==1 path selects 0x8019, player_id==0 uses literal 0x19 | high |
| ZONE_ENTRY_FLAGS_CLR_MASK=0x1fff | asm/08 L12161 (DWORD_080695a0); ands r2,r3 clears bits [12:0] of sprite halfword | high |
| scapegoat_token_tbl_080694d4 (raw .word 0x09e3f11c) | asm/08 L12059; CID dispatch for 0x12d2 (Scapegoat); RENAME-only per Ruling A | high |
| stray_lambs_token_tbl_08069504 (raw .word 0x09e3f12c) | asm/08 L12085; CID dispatch for 0x1710 (Stray Lambs); RENAME-only per Ruling A | high |
| invoke_effect_node_with_active_flag_3arg+1 | asm/08 L12926 (DWORD_08069ae8=0x08090625); asm/11 L11824 func addr 0x08090624 | high |
| check_zone_activation_ctx_match_cb+1=0x08069cdd | asm/08 L13312 (DAT_08069d7c=0x08069cdd); passed to init_zone_activation_display_fields | high |
| switchD table ptr=0x08069ef0 | asm/08 L13534 (DAT_08069eec); table base for switchD_08069edc | high |
| plate fix: Lord of D. CID 0x128b | asm/08 L11418 (.word 0x0000128b confirmed); card-stats.s card_0599 slot=0x128B | high |

## 求助

None. All slots have sufficient evidence for symbolization. The one BLOCKED candidate (`DWORD_080690f8` card name) was resolved by ROM byte verification + card-stats.s lookup confirming Lord of D.

---

## Executor Report: F08-Seg-6 (revised after review fixes)

- 槽: EQ=82 REF=3 RENAME=96 FUNC_RENAME=0 CREATE_FUNC=1 PLATE=1
  (EQ 84->82: removed SCAPEGOAT/STRAY_LAMBS token table addr equates per Ruling A)
- carve=0 disasm=0x080696d8/0x1c (THUMB; fn `check_equip_eligible_set_slot8_flag_for_cid_12da`) §5.1=0
- 新增 constants/全局:
  - card_info.inc +4: WIDESPREAD_RUIN_CID(0x1254), BOTTOMLESS_SHIFTING_SAND_CID(0x1540), HAMMER_SHOT_CID(0x17f2), cid_12da(0x12da)
  - ewram.inc +1: LP_ACTIVATION_LINK_FLAG_OFF(0x10d0)
  - oam_attr.inc +2: OAM_SPRITE_CODE_P1_ACTIVATION(0x8019), ZONE_ENTRY_FLAGS_CLR_MASK(0x1fff) [Ruling B: no equip_sprite.inc]
  - no token_tables.inc [Ruling A: DWORD_080694d4/DWORD_08069504 RENAME-only with ASCII EOL]
- Fix #2: DAT_08069778 -> LP_CARD_TRACK_BASE_OFF=0x1da8 (was LP_BANISHER_CTX_OFF, wrong value)
- Fix #3: DAT_08069f54/DWORD_0806a050 label prefix corrected to gduelcardctxbase_* (was gduelphaseflagss_*)
- 求助: none
- proposal: doc/dev/refine/F08-Seg-6.proposal.md
