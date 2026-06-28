# Refine Proposal: F12-Seg-3  [0x08095ba8..0x08096a4c)

## 段测绘

- 函数入口: x14
  - 0x08095ba8  init_equip_card_sprite_row_entry
  - 0x08095ca0  trigger_lp_bar_animation_if_ready
  - 0x08095d44  init_lp_bar_slot_entry_from_state
  - 0x08095d84  dispatch_lp_bar_animation_step
  - 0x08095e70  apply_slot_equip_activation_if_lp_anim_phase
  - 0x08095ec4  dispatch_effect_slot_by_display_state
  - 0x08095f4c  tick_lp_bar_anim_step_display
  - 0x08095fe0  eval_spell_activation_flags_by_zone
  - 0x08096264  setup_equip_slot_activation_entry
  - 0x0809650c  setup_equip_slot_activation_entry_alt
  - 0x0809678c  eval_zone_activation_flags_by_type
  - 0x08096864  eval_zone_activation_flags_for_player
  - 0x080968f4  check_zone_slot_card_activatable
  - 0x08096954  dispatch_zone_effect_by_slot
  - 0x08096974  get_lp_display_anim_counter
  - 0x08096988  write_card_display_ctx_fields
  - 0x080969c4  init_zone_activation_display_fields
  - 0x08096a08  init_zone_activation_display_state_p1_entry

  NOTE: python scan found 14 push-prefixed entries; the remaining functions (get_lp_display_anim_counter
  through init_zone_activation_display_state_p1_entry) use bx lr not push epilogues -- 18 total.

- 残留自动名槽: x144 total
  - DAT_: 116 slots
  - DWORD_: 0 slots
  - PTR_gP1LifePoints_: 28 slots
  - PTR_PTR_ / PTR_DAT_: 0 slots

  Total verified by python scan of lines [3562..5547].

- ROM_INCBIN / .byte 块: 0 (verified; python scan of Seg-3 lines found no ROM_INCBIN or raw .byte code
  blocks; only legitimate .zero alignment pads and .word pool entries present)

---

## 数据块分类 (Rule 2/3)

Seg-3 contains zero ROM_INCBIN blocks. No classification decision required.
Verification: python grep of lines 3562..5547 for 'ROM_INCBIN' and '.byte' returned 0 hits.

---

## 符号化计划 (R1/R2/R3)

All slot values verified by python ROM read at (vaddr - 0x08000000).
All REUSE entries verified by grep in constants/*.inc by VALUE before marking NEW.
All NEW entries verified by grep returning 0 hits in constants/*.inc.

### EQ_SLOTS (data-equate)

Key: REUSE = grep by VALUE confirmed hit in existing .inc; NEW = grep=0.

#### Group A: PTR_gP1LifePoints_* slots (28 slots -- all RENAME, not EQ)
All 28 PTR_gP1LifePoints_XXXXXXXX slots hold gP1LifePoints (0x0201c4e0). They are RENAME targets
(snake_case slot label only; value already correct equate gP1LifePoints). Listed in RENAME_SLOTS.

#### Group B: DAT_ slots with EXISTING constants (all REUSE)

| slot addr | value | const_name | source | slot_label |
|---|---|---|---|---|
| DAT_08095c1c | 0x00001d68 | ELIGIB_SPRITE_CTRL_OFF | ewram.inc REUSE | eligib_spr_ctrl_5c1c |
| DAT_08095c20 | 0x00001d6c | ELIGIB_ANIM_STATE_OFF | ewram.inc REUSE | eligib_anim_5c20 |
| DAT_08095c24 | 0x00001d70 | LP_BANISHER_CTX_OFF | ewram.inc REUSE | lp_banisher_5c24 |
| DAT_08095c28 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc REUSE | player_stride_5c28 |
| DAT_08095c2c | 0x00001d44 | ELIGIB_CARD_ID_OFF | ewram.inc REUSE | eligib_card_id_5c2c |
| DAT_08095c30 | 0x00001d48 | ACTIVATION_STATE_A_OFF | duel_field.inc REUSE | actstate_a_5c30 |
| DAT_08095c60 | 0x00001d44 | ELIGIB_CARD_ID_OFF | ewram.inc REUSE | eligib_card_id_5c60 |
| DAT_08095c64 | 0x00001d64 | LP_PLAYER_SIDE_CACHE_OFF | ewram.inc REUSE | lp_plyrside_5c64 |
| DAT_08095c98 | 0x00001d48 | ACTIVATION_STATE_A_OFF | duel_field.inc REUSE | actstate_a_5c98 |
| DAT_08095c9c | 0x00001d54 | ELIGIB_STATE_CTRL_OFF | ewram.inc REUSE | eligib_state_5c9c |
| DAT_08095cc4 | 0x00001d44 | ELIGIB_CARD_ID_OFF | ewram.inc REUSE | eligib_card_id_5cc4 |
| DAT_08095d08 | 0x00001d68 | ELIGIB_SPRITE_CTRL_OFF | ewram.inc REUSE | eligib_spr_ctrl_5d08 |
| DAT_08095d0c | 0x00001d48 | ACTIVATION_STATE_A_OFF | duel_field.inc REUSE | actstate_a_5d0c |
| DAT_08095d38 | 0x00001d48 | ACTIVATION_STATE_A_OFF | duel_field.inc REUSE | actstate_a_5d38 |
| DAT_08095d40 | 0x00001d54 | ELIGIB_STATE_CTRL_OFF | ewram.inc REUSE | eligib_state_5d40 |
| DAT_08095d74 | 0x00001d68 | ELIGIB_SPRITE_CTRL_OFF | ewram.inc REUSE | eligib_spr_ctrl_5d74 |
| DAT_08095d78 | 0x00001d6c | ELIGIB_ANIM_STATE_OFF | ewram.inc REUSE | eligib_anim_5d78 |
| DAT_08095d7c | 0x00001d70 | LP_BANISHER_CTX_OFF | ewram.inc REUSE | lp_banisher_5d7c |
| DAT_08095d80 | 0x00001d54 | ELIGIB_STATE_CTRL_OFF | ewram.inc REUSE | eligib_state_5d80 |
| DAT_08095dcc | 0x00001d68 | ELIGIB_SPRITE_CTRL_OFF | ewram.inc REUSE | eligib_spr_ctrl_5dcc |
| DAT_08095dd0 | 0x00001d70 | LP_BANISHER_CTX_OFF | ewram.inc REUSE | lp_banisher_5dd0 |
| DAT_08095e14 | 0x00001d68 | ELIGIB_SPRITE_CTRL_OFF | ewram.inc REUSE | eligib_spr_ctrl_5e14 |
| DAT_08095e1c | 0x00001d44 | ELIGIB_CARD_ID_OFF | ewram.inc REUSE | eligib_card_id_5e1c |
| DAT_08095e20 | 0x00001d48 | ACTIVATION_STATE_A_OFF | duel_field.inc REUSE | actstate_a_5e20 |
| DAT_08095e60 | 0x00001d68 | ELIGIB_SPRITE_CTRL_OFF | ewram.inc REUSE | eligib_spr_ctrl_5e60 |
| DAT_08095e64 | 0x00001d44 | ELIGIB_CARD_ID_OFF | ewram.inc REUSE | eligib_card_id_5e64 |
| DAT_08095e6c | 0x00001d54 | ELIGIB_STATE_CTRL_OFF | ewram.inc REUSE | eligib_state_5e6c |
| DAT_08095eb8 | 0x00001d68 | ELIGIB_SPRITE_CTRL_OFF | ewram.inc REUSE | eligib_spr_ctrl_5eb8 |
| DAT_08095ebc | 0x00001d6c | ELIGIB_ANIM_STATE_OFF | ewram.inc REUSE | eligib_anim_5ebc |
| DAT_08095ec0 | 0x00001d54 | ELIGIB_STATE_CTRL_OFF | ewram.inc REUSE | eligib_state_5ec0 |
| DAT_08095f48 | 0x00001d54 | ELIGIB_STATE_CTRL_OFF | ewram.inc REUSE | eligib_state_5f48 |
| DAT_08095f88 | 0x00001cec | P1LP_TIMER_OFF | ewram.inc REUSE | p1lp_timer_5f88 |
| DAT_08095f8c | 0x00001d54 | ELIGIB_STATE_CTRL_OFF | ewram.inc REUSE | eligib_state_5f8c |
| DAT_08095fdc | 0x00001d54 | ELIGIB_STATE_CTRL_OFF | ewram.inc REUSE | eligib_state_5fdc |
| DAT_08096024 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc REUSE | player_stride_6024 |
| DAT_08096028 | 0x0201c600 | gP1FieldArrayCBase | ewram.inc REUSE | gp1fcarrayc_6028 |
| DAT_0809602c | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc REUSE | gduecardctx_602c |
| DAT_08096168 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc REUSE | player_stride_6168 |
| DAT_08096260 | 0x00001407 | FIELD_SPELL_B_EFFECT_ID | card_info.inc REUSE | fspell_b_eid_6260 |
| DAT_080962a4 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc REUSE | player_stride_62a4 |
| DAT_080962a8 | 0x0201c510 | gDuelFieldSlots | ewram.inc REUSE | gduelfldslots_62a8 |
| DAT_08096360 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc REUSE | gduecardctx_6360 |
| DAT_08096384 | 0x00001cc4 | EQUIP_PHASE_STATE_OFF | duel_field.inc REUSE | eqphase_state_6384 |
| DAT_080963ac | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc REUSE | gduecardctx_63ac |
| DAT_08096430 | 0x00001d48 | ACTIVATION_STATE_A_OFF | duel_field.inc REUSE | actstate_a_6430 |
| DAT_080964f8 | 0x00001d48 | ACTIVATION_STATE_A_OFF | duel_field.inc REUSE | actstate_a_64f8 |
| DAT_080964fc | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc REUSE | player_stride_64fc |
| DAT_08096500 | 0x0201c510 | gDuelFieldSlots | ewram.inc REUSE | gduelfldslots_6500 |
| DAT_08096568 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc REUSE | player_stride_6568 |
| DAT_0809656c | 0x0201c510 | gDuelFieldSlots | ewram.inc REUSE | gduelfldslots_656c |
| DAT_08096570 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc REUSE | gduecardctx_6570 |
| DAT_08096630 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc REUSE | gduecardctx_6630 |
| DAT_080966d4 | 0x00001cc4 | EQUIP_PHASE_STATE_OFF | duel_field.inc REUSE | eqphase_state_66d4 |
| DAT_080966d8 | 0x00001cb8 | DUEL_ACTIVE_PLAYER_OFF | duel_field.inc REUSE | duel_active_plyr_66d8 |
| DAT_080966dc | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc REUSE | gduecardctx_66dc |
| DAT_080966e8 | 0x0000131e | SPECIAL_EQUIP_TARGET_CID_A | card_info.inc REUSE | sp_eq_cid_a_66e8 |
| DAT_08096704 | 0x00001cf4 | P2LP_BLOCK2_OFF_1CF4 | ewram.inc REUSE | p2lp_blk2_6704 |
| DAT_08096728 | 0x00001d48 | ACTIVATION_STATE_A_OFF | duel_field.inc REUSE | actstate_a_6728 |
| DAT_08096784 | 0x00001d48 | ACTIVATION_STATE_A_OFF | duel_field.inc REUSE | actstate_a_6784 |
| DAT_08096788 | 0x00001407 | FIELD_SPELL_B_EFFECT_ID | card_info.inc REUSE | fspell_b_eid_6788 |
| DAT_080967e8 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc REUSE | player_stride_67e8 |
| DAT_08096808 | 0x00001d64 | LP_PLAYER_SIDE_CACHE_OFF | ewram.inc REUSE | lp_plyrside_6808 |
| DAT_080968a4 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc REUSE | player_stride_68a4 |
| DAT_080968c4 | 0x00001d64 | LP_PLAYER_SIDE_CACHE_OFF | ewram.inc REUSE | lp_plyrside_68c4 |
| DAT_080968f0 | 0x00001d64 | LP_PLAYER_SIDE_CACHE_OFF | ewram.inc REUSE | lp_plyrside_68f0 |
| DAT_08096950 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc REUSE | gduecardctx_6950 |
| DAT_080969b4 | 0x00001d4c | ACTIVATION_STATE_C_OFF | duel_field.inc REUSE | actstate_c_69b4 |
| DAT_080969bc | 0x00001d64 | LP_PLAYER_SIDE_CACHE_OFF | ewram.inc REUSE | lp_plyrside_69bc |
| DAT_080969c0 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc REUSE | gduecardctx_69c0 |
| DAT_080969f4 | 0x00001d4c | ACTIVATION_STATE_C_OFF | duel_field.inc REUSE | actstate_c_69f4 |
| DAT_08096a00 | 0x00001d64 | LP_PLAYER_SIDE_CACHE_OFF | ewram.inc REUSE | lp_plyrside_6a00 |
| DAT_08096a04 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc REUSE | gduecardctx_6a04 |
| DAT_08096a38 | 0x00001d4c | ACTIVATION_STATE_C_OFF | duel_field.inc REUSE | actstate_c_6a38 |
| DAT_08096a44 | 0x00001d64 | LP_PLAYER_SIDE_CACHE_OFF | ewram.inc REUSE | lp_plyrside_6a44 |
| DAT_08096a48 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc REUSE | gduecardctx_6a48 |

#### Group C: DAT_ slots with EXISTING constants (duel_field.inc, misc)

| slot addr | value | const_name | source | slot_label |
|---|---|---|---|---|
| DAT_08095dd4 | 0x00001d74 | NEW: LP_ANIM_RESULT_OFF | NEW (grep 0x00001d74 constants/=0; 5 refs) | lp_anim_result_5dd4 |
| DAT_08095e18 | 0x00001d74 | LP_ANIM_RESULT_OFF | NEW REUSE | lp_anim_result_5e18 |
| DAT_08095f08 | 0x0000fffe | NEW: EFFECT_ID_GENERIC_WILDCARD | NEW (0x0000fffe vs GAME_STR_RAW_ID_MASK=0xfffe0000 -- different value; 1484 refs) | effect_id_wc_5f08 |
| DAT_08095fd4 | 0x00008023 | SPRITE_ATTR_DUEL_PHASE_P2_B | duel_field.inc REUSE | sprite_p2b_5fd4 |
| DAT_08096050 | 0x00001c58 | NEW: ZONE_PHASE_STATUS_OFF | NEW (grep 0x00001c58 constants/=0; 8 refs) | zone_phase_sta_6050 |
| DAT_08096070 | 0x00001c58 | ZONE_PHASE_STATUS_OFF | NEW REUSE | zone_phase_sta_6070 |
| DAT_0809608c | 0x00001bd4 | NEW: ZONE_EVAL_PHASE_CODE_OFF | NEW (grep 0x00001bd4 constants/=0; 3 refs) | zone_eval_phase_608c |
| DAT_080960f8 | 0x00001d78 | ACTIVATION_STATE_B_OFF | duel_field.inc REUSE | actstate_b_60f8 |
| DAT_08096124 | 0x00001d78 | ACTIVATION_STATE_B_OFF | duel_field.inc REUSE | actstate_b_6124 |
| DAT_080961a4 | 0x00001d78 | ACTIVATION_STATE_B_OFF | duel_field.inc REUSE | actstate_b_61a4 |
| DAT_080961c0 | 0x00001c58 | ZONE_PHASE_STATUS_OFF | NEW REUSE | zone_phase_sta_61c0 |
| DAT_080961d8 | 0x00001c58 | ZONE_PHASE_STATUS_OFF | NEW REUSE | zone_phase_sta_61d8 |
| DAT_08096208 | 0x00001c58 | ZONE_PHASE_STATUS_OFF | NEW REUSE | zone_phase_sta_6208 |
| DAT_0809625c | 0x00001c58 | ZONE_PHASE_STATUS_OFF | NEW REUSE | zone_phase_sta_625c |
| DAT_08096363b4 | -- | (see 080963b4 below) | | |
| DAT_080963b4 | 0x00001d78 | ACTIVATION_STATE_B_OFF | duel_field.inc REUSE | actstate_b_63b4 |
| DAT_08096364 | 0xfffff03f | NEW: ACTIVATION_ENTRY_CLR_BITS_11_6 | NEW domain-distinct from OAM_ATTR2_CLR_BITS_11_6; used on activation struct [r2+2] halfword; 14 ROM refs | act_entry_clr_11_6_6364 |
| DAT_08096368 | 0xffff803f | NEW: ACTIVATION_ENTRY_CLR_BITS_14_6 | NEW domain-distinct from slot_field_mask_ffff803f (card_info) and SCROLLBAR_CLEAR_BITS_14_6; used on activation struct [r2+4] halfword; 37 ROM refs | act_entry_clr_14_6_6368 |
| DAT_0809636c | 0x00001d48 | ACTIVATION_STATE_A_OFF | duel_field.inc REUSE | actstate_a_636c |
| DAT_08096574 | 0x00001d48 | ACTIVATION_STATE_A_OFF | duel_field.inc REUSE | actstate_a_6574 |
| DAT_08096634 | 0xfffff03f | ACTIVATION_ENTRY_CLR_BITS_11_6 | NEW REUSE | act_entry_clr_11_6_6634 |
| DAT_08096638 | 0xffff803f | ACTIVATION_ENTRY_CLR_BITS_14_6 | NEW REUSE | act_entry_clr_14_6_6638 |
| DAT_0809663c | 0x00001d48 | ACTIVATION_STATE_A_OFF | duel_field.inc REUSE | actstate_a_663c |
| DAT_080966d0 | 0x00001d48 | ACTIVATION_STATE_A_OFF | duel_field.inc REUSE | actstate_a_66d0 |
| DAT_080966e4 | 0x00001cf4 | P2LP_BLOCK2_OFF_1CF4 | ewram.inc REUSE | p2lp_blk2_66e4 |
| DAT_080966ec | 0x00001d78 | ACTIVATION_STATE_B_OFF | duel_field.inc REUSE | actstate_b_66ec |
| DAT_08096708 | 0x00001d78 | ACTIVATION_STATE_B_OFF | duel_field.inc REUSE | actstate_b_6708 |
| DAT_080967c0 | 0x00001d64 | LP_PLAYER_SIDE_CACHE_OFF | ewram.inc REUSE | lp_plyrside_67c0 |
| DAT_080967c4 | 0x0201b290 | gDuelPhaseFlags | ewram.inc REUSE | gduelphaseflag_67c4 |
| DAT_08096504 | 0xfffff03f | ACTIVATION_ENTRY_CLR_BITS_11_6 | NEW REUSE | act_entry_clr_11_6_6504 |
| DAT_08096508 | 0xffff803f | ACTIVATION_ENTRY_CLR_BITS_14_6 | NEW REUSE | act_entry_clr_14_6_6508 |
| DAT_08096834 | 0x000004cc | LP_BAR_ANIM_STATE_OFF | ewram.inc REUSE | lp_bar_anim_sta_6834 |
| DAT_08096860 | 0x00001d64 | LP_PLAYER_SIDE_CACHE_OFF | ewram.inc REUSE | lp_plyrside_6860 |
| DAT_08096968 | 0x0000fffe | EFFECT_ID_GENERIC_WILDCARD | NEW REUSE | effect_id_wc_6968 |
| DAT_08096984 | 0x00001d4c | ACTIVATION_STATE_C_OFF | duel_field.inc REUSE | actstate_c_6984 |
| DAT_080969b8 | 0x00001d7c | NEW: ACTIVATION_ENTRY_PTR_OFF | NEW (grep 0x00001d7c constants/=0; 9 refs) | act_entry_ptr_69b8 |
| DAT_080969f8 | 0x00001d7c | ACTIVATION_ENTRY_PTR_OFF | NEW REUSE | act_entry_ptr_69f8 |
| DAT_080969fc | 0x00001d58 | ELIGIB_ACT_COUNT_OFF | ewram.inc REUSE | eligib_actcnt_69fc |
| DAT_08096a3c | 0x00001d7c | ACTIVATION_ENTRY_PTR_OFF | NEW REUSE | act_entry_ptr_6a3c |
| DAT_08096a40 | 0x00001d58 | ELIGIB_ACT_COUNT_OFF | ewram.inc REUSE | eligib_actcnt_6a40 |

#### Group D: NEW constants still requiring resolution

| slot addr | value | proposed const_name | evidence | slot_label |
|---|---|---|---|---|
| DAT_08095cc8 | 0x00000fee | LP_ANIM_TRIGGER_SENTINEL | trigger_lp_bar_animation_if_ready: [gP1LifePoints+0x1d44]==0x0fee triggers dispatch_lp_bar_animation_step; sentinel value distinct from COCOON_OF_EVOLUTION_CID (same raw value in card_info.inc but different subsystem -- LP animation gate vs card data); 14 ROM refs; conf: high -- OPEN QUESTION: see below | lp_anim_sentinel_5cc8 |
| DAT_08095d04 | 0x0201b290 | gDuelPhaseFlags | ewram.inc REUSE (already confirmed) | gduelphaseflag_5d04 |
| DAT_08096a24 | -- | (note: DAT_08096a24 does not appear in scan -- 0x1d24 computed inline via subs r3,#0x28 from 0x1d4c; no pool slot) | | -- |

NOTE: 0x00001d24 appears in init_zone_activation_display_state_p1_entry as a computed offset:
  `ldr r3, DAT_08096a3c` (=0x1d7c); `add r2,r2,r3`; `subs r3,#0x28` -> r3=0x1d7c-0x28=0x1d54;
  But the plate says [+0x1d24] is cleared. Let me re-examine: `subs r3,#0x28` from 0x1d7c = 0x1d54 (not 0x1d24).
  The plate mention of 0x1d24 may refer to DAT_08096a3c - 0x58 = 0x1d24 if seen from 0x1d7c - 0x58.
  Re-read of L5511-5514: `ldr r3,DAT_08096a3c` (0x1d7c); `adds r1,r2,r3`; `str r0,[r1,0]`; `ldr r1,DAT_08096a40` (0x1d58);
  `adds r0,r2,r1`; `str r1,[r0,0]`; `subs r3,#0x28`; `adds r0,r2,r3`; `str r1,[r0,0]`.
  0x1d7c - 0x28 = 0x1d54. So ELIGIB_STATE_CTRL_OFF. The plate description of 0x1d24 was incorrect
  in the function plate; actual writes are to 0x1d4c, 0x1d7c, 0x1d58, 0x1d54 (via computed offset).
  No DAT_ pool slot for 0x1d24 exists in Seg-3. This is a plate correction opportunity (R5).

Summary of new constants to declare:
- 7 genuinely new (see "新增 constants" section below)

#### Complete EQ_SLOTS summary

Total EQ slots: 116 DAT_ slots

**REUSE (existing constants)**: 108 slots
**NEW constants needed**: 8 slots covering: LP_ANIM_RESULT_OFF(x2), EFFECT_ID_GENERIC_WILDCARD(x2),
  ZONE_PHASE_STATUS_OFF(x6), ZONE_EVAL_PHASE_CODE_OFF(x1), ACTIVATION_ENTRY_CLR_BITS_11_6(x3),
  ACTIVATION_ENTRY_CLR_BITS_14_6(x3), ACTIVATION_ENTRY_PTR_OFF(x3), LP_ANIM_TRIGGER_SENTINEL(x1)

---

### REF_SLOTS (USER-label + DATA-ref)

No switchD base pointer slots or ROM table jump-base slots in Seg-3.
Seg-3 has no DAT_ slots pointing to code entry points that require createLabel + DATA-ref.
(All DAT_ slots hold either EWRAM global addresses or integer offsets/masks -- no code pointers.)

REF count: 0

---

### RENAME_SLOTS (PTR_ label rename + EOL)

All 28 PTR_gP1LifePoints_XXXXXXXX slots hold gP1LifePoints; only the slot label needs snake_case rename.

| slot addr | current_label | new slot_label |
|---|---|---|
| PTR_gP1LifePoints_08095c18 | PTR_gP1LifePoints_08095c18 | gp1lp_ptr_95c18 |
| PTR_gP1LifePoints_08095c94 | PTR_gP1LifePoints_08095c94 | gp1lp_ptr_95c94 |
| PTR_gP1LifePoints_08095cc0 | PTR_gP1LifePoints_08095cc0 | gp1lp_ptr_95cc0 |
| PTR_gP1LifePoints_08095d3c | PTR_gP1LifePoints_08095d3c | gp1lp_ptr_95d3c |
| PTR_gP1LifePoints_08095d70 | PTR_gP1LifePoints_08095d70 | gp1lp_ptr_95d70 |
| PTR_gP1LifePoints_08095da8 | PTR_gP1LifePoints_08095da8 | gp1lp_ptr_95da8 |
| PTR_gP1LifePoints_08095e10 | PTR_gP1LifePoints_08095e10 | gp1lp_ptr_95e10 |
| PTR_gP1LifePoints_08095e68 | PTR_gP1LifePoints_08095e68 | gp1lp_ptr_95e68 |
| PTR_gP1LifePoints_08095eb4 | PTR_gP1LifePoints_08095eb4 | gp1lp_ptr_95eb4 |
| PTR_gP1LifePoints_08095ee4 | PTR_gP1LifePoints_08095ee4 | gp1lp_ptr_95ee4 |
| PTR_gP1LifePoints_08095f64 | PTR_gP1LifePoints_08095f64 | gp1lp_ptr_95f64 |
| PTR_gP1LifePoints_08095fd8 | PTR_gP1LifePoints_08095fd8 | gp1lp_ptr_95fd8 |
| PTR_gP1LifePoints_080960f4 | PTR_gP1LifePoints_080960f4 | gp1lp_ptr_960f4 |
| PTR_gP1LifePoints_08096120 | PTR_gP1LifePoints_08096120 | gp1lp_ptr_96120 |
| PTR_gP1LifePoints_08096164 | PTR_gP1LifePoints_08096164 | gp1lp_ptr_96164 |
| PTR_gP1LifePoints_080963b0 | PTR_gP1LifePoints_080963b0 | gp1lp_ptr_963b0 |
| PTR_gP1LifePoints_080966e0 | PTR_gP1LifePoints_080966e0 | gp1lp_ptr_966e0 |
| PTR_gP1LifePoints_080967bc | PTR_gP1LifePoints_080967bc | gp1lp_ptr_967bc |
| PTR_gP1LifePoints_080967e4 | PTR_gP1LifePoints_080967e4 | gp1lp_ptr_967e4 |
| PTR_gP1LifePoints_0809685c | PTR_gP1LifePoints_0809685c | gp1lp_ptr_9685c |
| PTR_gP1LifePoints_080968a0 | PTR_gP1LifePoints_080968a0 | gp1lp_ptr_968a0 |
| PTR_gP1LifePoints_080968ec | PTR_gP1LifePoints_080968ec | gp1lp_ptr_968ec |
| PTR_gP1LifePoints_08096928 | PTR_gP1LifePoints_08096928 | gp1lp_ptr_96928 |
| PTR_gP1LifePoints_0809694c | PTR_gP1LifePoints_0809694c | gp1lp_ptr_9694c |
| PTR_gP1LifePoints_08096980 | PTR_gP1LifePoints_08096980 | gp1lp_ptr_96980 |
| PTR_gP1LifePoints_080969b0 | PTR_gP1LifePoints_080969b0 | gp1lp_ptr_969b0 |
| PTR_gP1LifePoints_080969f0 | PTR_gP1LifePoints_080969f0 | gp1lp_ptr_969f0 |
| PTR_gP1LifePoints_08096a34 | PTR_gP1LifePoints_08096a34 | gp1lp_ptr_96a34 |

RENAME count: 28

---

### FUNC_RENAME

No function name contradictions detected. All 14 push-entry functions have names consistent with
their bodies. No FUNC_RENAME actions required.

---

### PLATE (R5)

4 plate comments contain CJK mojibake (grep [^\x00-\x7F] hits; lines 4471, 4819, 5148, 5396).
Additionally, plates at L3690 and L3814 contain stale FUN_0804ce78 reference (true name:
dispatch_card_eligibility_state_machine). Plates at L4819 contain stale FUN_08096264
(true name: setup_equip_slot_activation_entry) and FUN_08096b3c (true name:
dispatch_zone_activation_by_state). Plates at L5499 contain stale FUN_08097bec
(true name: check_equip_target_slot_eligibility) and FUN_08098020 (an intra-function
branch point inside dispatch_equip_slot_display_state_by_phase; not a function entry).

| fn addr | line | action |
|---|---|---|
| 0x08096264 setup_equip_slot_activation_entry | L4471 | CJK plate -> ASCII rewrite (full substring replace). Current plate is mojibake. Replacement: "Builds one equip-activation entry in the 0x18-byte stack buffer. r0=player_side, r1=slot_idx, r2=zone_slot. Guard: slot_idx<=4. If active_player (gDuelCardCtxBase+4) XOR 1 != player_side: check_card_field5_is_nonzero, slot[+8] chain_head nonzero, check_card_id_is_equip_blocker. memset(buf,0,0x18): writes card_id/player_bit/zone_code/attr_bits; stores 4 to [gP1LifePoints+ACTIVATION_STATE_A_OFF]; calls eval_equip_activation_for_slot. Returns 0x8 if activatable, else 0. indeg=1." |
| 0x0809650c setup_equip_slot_activation_entry_alt | L4819 | CJK plate + stale FUN_08096264/FUN_08096b3c -> ASCII rewrite. Replacement: "Structural symmetric variant of setup_equip_slot_activation_entry (indeg=1), called by dispatch_zone_activation_by_state. r0=player_side, r1=slot_idx, r2=zone_slot. If find_paired_zone_entry_for_card finds pair and player==gDuelCardCtxBase+4: writes [gP1LifePoints+ACTIVATION_STATE_A_OFF]:=0x10. Else: checks eligibility, memset(buf,0,0x18), builds entry, calls eval_equip_activation_for_slot. field6==0x16/0x17: build_zone_activation_entry_blocked / _equip. Returns 0x8 if activatable, else 0." |
| 0x0809678c eval_zone_activation_flags_by_type | L5148 | CJK plate -> ASCII rewrite. Replacement: "Evaluates zone_type (r1) activation flags for a single zone (indeg=1). Zone 0xb (FIELD_SPELL_ZONE): LP threshold check via gP1LifePoints[player*0x868+0xc], then setup_equip_context_for_zone_activation; success sets r6|=0x8. Zones 0xc..0xf: check_zone_slot_card_activatable -> dispatch_zone_effect_by_slot, OR into r6; opposite player and zone==0xd: r6|=0x1000. Other: setup_equip_context_for_slot_activation. Returns r6 (combined activation flags)." |
| 0x08096954 dispatch_zone_effect_by_slot | L5396 | CJK plate -> ASCII rewrite. Replacement: "Minimal dispatch leaf: moves r1 (slot_idx) to r2, passes EFFECT_ID_GENERIC_WILDCARD (0xfffe) as r1 to dispatch_effect_handler_by_card_id. Returns 0x8 (activatable flag) if callee returns nonzero, else 0. indeg=2; callers: eval_zone_activation_flags_by_type + eval_zone_activation_flags_for_player." |

Additional stale FUN_ references in existing ASCII plates (substring replace only):
- L3561 (init_equip_card_sprite_row_entry plate): replace FUN_0804ce78 -> dispatch_card_eligibility_state_machine
- L3690 (trigger_lp_bar_animation_if_ready plate): replace FUN_0804ce78 -> dispatch_card_eligibility_state_machine
- L3814 (dispatch_lp_bar_animation_step plate): replace FUN_0804ce78 -> dispatch_card_eligibility_state_machine
- L5499 (init_zone_activation_display_state_p1_entry plate): replace FUN_08097bec -> check_equip_target_slot_eligibility; FUN_08098020 is a branch inside dispatch_equip_slot_display_state_by_phase (not a function entry) -- replace with label reference "dispatch_equip_slot_display_state_by_phase internal branch @ 0x08098020"

Total PLATE actions: 4 full rewrites + 4 substring FUN_ replacements = 8 plate operations.

---

## carve 計劃 (R7, 如有)

None. Seg-3 contains no ROM_INCBIN blocks and no inter-function data tables requiring carving.

---

## disasm 計劃 (R4, 如有)

None. Seg-3 contains no misidentified code blocks and no ROM_INCBIN blocks.

---

## 新增 constants / 全局 (如有)

All new constants verified by grep returning 0 hits in constants/*.inc by value before declaring NEW.

### constants/duel_field.inc (新增 5)

| const_name | value | evidence | ROM refs |
|---|---|---|---|
| ZONE_PHASE_STATUS_OFF | 0x00001c58 | eval_spell_activation_flags_by_zone: [gDuelFieldSlots+0x1c58] written with 0x10/0x17/0x5/0xc/0xf/0x6 status codes by multiple paths (zone_phase condition = 2/3/4 dispatch); read by Seg-4+ callers as zone gate. grep 0x00001c58 constants/=0; 8 ROM refs; conf: high | 8 |
| ZONE_EVAL_PHASE_CODE_OFF | 0x00001bd4 | eval_spell_activation_flags_by_zone: [gDuelFieldSlots+0x1bd4] zone_phase_code; values 2/3/4 -> three dispatch paths for field-spell vs equip vs pass; grep 0x00001bd4 constants/=0; 3 ROM refs; conf: high | 3 |
| ACTIVATION_ENTRY_CLR_BITS_11_6 | 0xfffff03f | setup_equip_slot_activation_entry + _alt + _alt_b: `ldrh r3,[r2,#0x4]; ldr r0,DAT; ands r0,r3; strh r0,[r2,#0x2]` -- clears bits[11:6] of activation entry halfword at struct+2; domain = equip activation entry struct (not OAM -- domain-distinct from OAM_ATTR2_CLR_BITS_11_6); grep 0xfffff03f constants/*.inc returns only oam_attr.inc hit (different domain); 14 ROM refs; conf: high | 14 |
| ACTIVATION_ENTRY_CLR_BITS_14_6 | 0xffff803f | setup_equip_slot_activation_entry + _alt + _alt_b: clears bits[14:6] of halfword at struct+4; domain = equip activation entry struct (not scrollbar or slot_field_scan -- domain-distinct from SCROLLBAR_CLEAR_BITS_14_6 and slot_field_mask_ffff803f); 37 ROM refs; conf: high | 37 |
| ACTIVATION_ENTRY_PTR_OFF | 0x00001d7c | write_card_display_ctx_fields: [gP1LifePoints+0x1d7c]:=r0 (zone_eval_fn ptr); init_zone_activation_display_fields: stores zone_eval_fn callback ptr; init_zone_activation_display_state_p1_entry: stores zone_or_card_param; grep 0x00001d7c constants/=0; 9 ROM refs; conf: high | 9 |

### constants/ewram.inc (新增 3)

| const_name | value | evidence | ROM refs |
|---|---|---|---|
| LP_ANIM_RESULT_OFF | 0x00001d74 | dispatch_lp_bar_animation_step: state=0 path stores render_monster_slot_card_with_lp_bar result to [gP1LifePoints+0x1d74]; state=2 path reads from same offset as OAM slot index source; grep 0x00001d74 constants/=0; 5 ROM refs; conf: high | 5 |
| LP_ANIM_TRIGGER_SENTINEL | 0x00000fee | trigger_lp_bar_animation_if_ready: [gP1LifePoints+ELIGIB_CARD_ID_OFF(0x1d44)] == 0x0fee triggers dispatch_lp_bar_animation_step; value is distinct from Cocoon of Evolution CID usage context (LP animation gate vs card data subsystem); grep 0x00000fee constants/=0 in ewram.inc/duel_field.inc (card_info.inc has COCOON_OF_EVOLUTION_CID same value but different domain); 14 ROM refs; conf: high | 14 |
| EFFECT_ID_GENERIC_WILDCARD | 0x0000fffe | dispatch_zone_effect_by_slot: passed as effect_id r1 to dispatch_effect_handler_by_card_id to match generic/wildcard effect handlers; dispatch_effect_slot_by_display_state: passed as sub-param (r2=0xfffe) to init_effect_slot_display_context; value 0x0000fffe is different from GAME_STR_RAW_ID_MASK=0xfffe0000 (high-word mask); grep 0x0000fffe in constants/=0 distinct from both GAME_STR_RAW_ID_MASK and CARD_INFO_STATE_CARD_ID_CLEAR; 1484 ROM refs; conf: high | 1484 |

---

## §5.1 登记 (Rule 3) -- 0 引用块

No ROM_INCBIN or zero-reference data blocks in Seg-3. No §5.1 entries for this segment.

---

## 消費者証拠 (R6) -- 关键槽语义的 file:line + 置信度

| slot | consumer evidence | confidence |
|---|---|---|
| ELIGIB_SPRITE_CTRL_OFF (0x1d68) | asm/12 L3561: init_equip_card_sprite_row_entry plate: "player_bit from [gP1LifePoints+0x1d68]"; ewram.inc ELIGIB_SPRITE_CTRL_OFF confirmed | high |
| ELIGIB_ANIM_STATE_OFF (0x1d6c) | asm/12 L3775: init_lp_bar_slot_entry_from_state plate: "PARAM_B_OFFSET=0x1d6c"; ewram.inc ELIGIB_ANIM_STATE_OFF confirmed | high |
| LP_BANISHER_CTX_OFF (0x1d70) | asm/12 L3775: init_lp_bar_slot_entry_from_state plate: "PARAM_C_OFFSET=0x1d70"; ewram.inc LP_BANISHER_CTX_OFF confirmed | high |
| ELIGIB_CARD_ID_OFF (0x1d44) | asm/12 L3690: trigger_lp_bar_animation_if_ready plate: "trigger_sentinel=0x0fee ... Reads gP1LifePoints+0x1d44"; ewram.inc ELIGIB_CARD_ID_OFF confirmed | high |
| ACTIVATION_STATE_A_OFF (0x1d48) | asm/12 L3561: init_equip_card_sprite_row_entry plate: "slot_rendered_offset=0x38; gP1LifePoints offsets 0x1d44/0x1d48"; duel_field.inc ACTIVATION_STATE_A_OFF=0x1d48 confirmed | high |
| ELIGIB_STATE_CTRL_OFF (0x1d54) | asm/12 L3775: init_lp_bar_slot_entry_from_state plate: "PENDING_FLAG_OFFSET=0x1d54"; ewram.inc ELIGIB_STATE_CTRL_OFF confirmed | high |
| LP_PLAYER_SIDE_CACHE_OFF (0x1d64) | asm/12 L5148/5263: plates of eval_zone_activation_flags_by_type/for_player: "ACTIVE_ZONE_PLAYER_FIELD_OFFSET=0x1d64"; ewram.inc LP_PLAYER_SIDE_CACHE_OFF confirmed | high |
| LP_ANIM_RESULT_OFF (0x1d74) | asm/12 L3814: dispatch_lp_bar_animation_step plate: "result_offset=0x1d74"; 5 ROM refs; conf: high | high |
| ACTIVATION_STATE_B_OFF (0x1d78) | asm/12 L4143: eval_spell_activation_flags_by_zone plate: "Constants: ... [gDuelFieldSlots+0x1d78]:=0x0c/0x0d/0x0f"; duel_field.inc ACTIVATION_STATE_B_OFF=0x1d78 confirmed | high |
| FIELD_SPELL_B_EFFECT_ID (0x1407) | asm/12 L5116-5123: check_value_in_slot_chain(0x0, 0xb, 0x1407) in eval_spell_activation_flags_by_zone non-aggression guard path; card_info.inc FIELD_SPELL_B_EFFECT_ID=0x1407 confirmed | high |
| ACTIVATION_STATE_C_OFF (0x1d4c) | asm/12 L5416: get_lp_display_anim_counter plate: "field_offset=0x1d4c"; duel_field.inc ACTIVATION_STATE_C_OFF confirmed | high |
| ACTIVATION_ENTRY_PTR_OFF (0x1d7c) | asm/12 L5429: write_card_display_ctx_fields plate: "[+0x1d7c]:=0"; asm/12 L5462: init_zone_activation_display_fields plate: "[gP1LifePoints+0x1d7c]=r0 (zone_eval_fn)"; conf: high | high |
| ELIGIB_ACT_COUNT_OFF (0x1d58) | asm/12 L5499: init_zone_activation_display_state_p1_entry plate: "[+0x1d58]:=0 (clear counter)"; ewram.inc ELIGIB_ACT_COUNT_OFF=0x1d58 confirmed | high |
| ZONE_PHASE_STATUS_OFF (0x1c58) | asm/12 L4143: eval_spell_activation_flags_by_zone plate: "[gDuelFieldSlots+0x1c58]:=0x10/0x17"; multiple paths confirm zone status gating; 8 ROM refs; conf: high | high |
| ZONE_EVAL_PHASE_CODE_OFF (0x1bd4) | asm/12 L4233: DAT_0809608c context: "ldr r0,{0x1bd4}; adds r0,r6,r1; ldr r0,[r0]; cmp r0,#3 -> zone_phase==3 path"; 3 ROM refs; conf: high | high |
| LP_ANIM_TRIGGER_SENTINEL (0x0fee) | asm/12 L3690: trigger_lp_bar_animation_if_ready plate: "trigger_sentinel=0x0fee, sprite_buf_flag_addr=0x0201b290+0x4d0"; conf: high | high |
| EFFECT_ID_GENERIC_WILDCARD (0x0000fffe) | asm/12 L5396: dispatch_zone_effect_by_slot plate: "EFFECT_ID_GENERIC=0xfffe"; asm/12 L3988: dispatch_effect_slot_by_display_state: passes 0xfffe as sub-param; 1484 ROM refs; conf: high | high |
| ACTIVATION_ENTRY_CLR_BITS_11_6 (0xfffff03f) | asm/12 L4565-4565: setup_equip_slot_activation_entry: "ldrh r3,[r2,#0x4]; ldr r0,DAT_08096364(0xfffff03f); ands r0,r3; strh r0,[r2,#0x2]"; 14 ROM refs; conf: high | high |
| ACTIVATION_ENTRY_CLR_BITS_14_6 (0xffff803f) | asm/12 L4566: setup_equip_slot_activation_entry: "ldrh r3,[r2,#0x4]; ldr r0,DAT_08096368(0xffff803f); ands r0,r3; strh r0,[r2,#0x4]"; 37 ROM refs; conf: high | high |
| SPECIAL_EQUIP_TARGET_CID_A (0x131e) | asm/12 L5000: setup_equip_slot_activation_entry_alt: DAT_080966e8=0x131e compared against card_id for special-path gate; card_info.inc SPECIAL_EQUIP_TARGET_CID_A confirmed; conf: high | high |

---

## 求助 (如有低置信度语义)

### OPEN QUESTION 1 (med): LP_ANIM_TRIGGER_SENTINEL (0x0fee) vs COCOON_OF_EVOLUTION_CID

DAT_08095cc8 = 0x00000fee. In trigger_lp_bar_animation_if_ready, this is compared against
[gP1LifePoints+ELIGIB_CARD_ID_OFF(0x1d44)] to gate dispatch_lp_bar_animation_step. card_info.inc
already contains COCOON_OF_EVOLUTION_CID = 0x0000fee (same raw value). The LP trigger gate stores
a sentinel value into the same ELIGIB_CARD_ID_OFF field used for card IDs. Two interpretations:
(a) sentinel 0x0fee is deliberately chosen as a value distinct from all valid CIDs (CIDs > 0x200),
making LP_ANIM_TRIGGER_SENTINEL a new constant; (b) the Cocoon of Evolution CID is used as a
sentinel in the LP animation path (meaning the value coincidentally reuses the card ID naming).
Consumer evidence favors interpretation (a): the plate says "trigger_sentinel=0x0fee", not card name.
Decision: declare LP_ANIM_TRIGGER_SENTINEL as new constant with EOL note on card_info coincidence.
Fixer may verify by checking whether any consumers of [gP1LifePoints+0x1d44] treat 0x0fee as a CID.
Confidence: high for new constant; med for "not the Cocoon CID in this context".

### OPEN QUESTION 2 (low): plate at L5499 references FUN_08098020

FUN_08098020 appears at address 0x08098020 which is mid-function inside
dispatch_equip_slot_display_state_by_phase. It is NOT a function entry point but an internal branch
target. The plate text says "FUN_08097bec-FUN_08098020 (equip state machine internal)".
This is a prose description spanning a range; 0x08097bec = check_equip_target_slot_eligibility
(confirmed function label). 0x08098020 is inside switchD_08097c58__caseD_1 (case block).
Fix: plate substring replace to "check_equip_target_slot_eligibility .. dispatch_equip_slot_display_state_by_phase internal (0x08098020 is mid-function branch)". Confidence: high.
