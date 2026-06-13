# Refine Proposal: F05-Seg-5  [0x0804c6e8..0x0804d124)

## 段测绘

- 函数入口: 7 个命名函数 (6 fully within segment + 1 spanning into Seg-6)
  - 0x0804c76c  submit_slot_card_sprite_row_entry
  - 0x0804c910  apply_equip_activation_with_id_lookup
  - 0x0804c958  init_card_sprite_row_entry
  - 0x0804caf0  init_card_sprite_row_entry_alt
  - 0x0804cc8c  submit_slot_card_sprite_row_packed
  - 0x0804cdd8  check_card_slot_activation_eligible
  - 0x0804ce78  dispatch_card_eligibility_state_machine  (body spans Seg-5 + Seg-6; epilogue at 0x4d1d2)

- セグメント先頭 0x4c6e8..0x4c732: switchdataD_0804c6e8 jump table (6-entry) +
  case stubs for switchD_0804c6dc (in classify_card_id_summon_category from Seg-4b).
  5 DAT_ literal-pool slots: 0x4c704 / 0x4c70c / 0x4c714 / 0x4c71c / 0x4c72c.

- 残留自动名槽: 75 total (DAT_* and PTR_*)
  - switchdataD case pool: DAT_0804c704 / DAT_0804c70c / DAT_0804c714 / DAT_0804c71c / DAT_0804c72c  (x5)
  - submit_slot_card_sprite_row_entry pool: DAT_0804c7e8 / PTR_gP1LifePoints_0804c7ec /
    DAT_0804c7f0 / DAT_0804c7f4 / DAT_0804c7f8 / DAT_0804c81c / DAT_0804c8c0 / DAT_0804c8c4 /
    DAT_0804c8c8 / DAT_0804c8cc / DAT_0804c90c  (x11)
  - apply_equip_activation_with_id_lookup pool: DAT_0804c940  (x1)
  - init_card_sprite_row_entry pool: DAT_0804ca44 / DAT_0804ca48 / DAT_0804ca4c / DAT_0804ca50 /
    DAT_0804ca54 / DAT_0804ca58  (x6)
  - init_card_sprite_row_entry_alt pool: DAT_0804cbe0 / DAT_0804cbe4 / DAT_0804cbe8 /
    DAT_0804cbec / DAT_0804cbf0 / DAT_0804cbf4  (x6)
  - check_card_slot_activation_eligible BST pool: DAT_0804ce24 / DAT_0804ce28 / DAT_0804ce2c /
    DAT_0804ce34 / DAT_0804ce4c / DAT_0804ce60  (x6)
  - dispatch_card_eligibility_state_machine pool: DAT_0804ce9c / DAT_0804cea0 / DAT_0804cea4 /
    PTR_DAT_0804cd90 / DAT_0804cf6c / DAT_0804cf70 / DAT_0804cf74 / DAT_0804cf84 /
    DAT_0804cfb4 / DAT_0804d008 / DAT_0804d00c /
    PTR_gP1LifePoints_0804d034 / DAT_0804d038 / DAT_0804d03c /
    DAT_0804d054 / DAT_0804d058 /
    PTR_gP1LifePoints_0804d070 / DAT_0804d074 / DAT_0804d078 /
    DAT_0804d098 / DAT_0804d09c / DAT_0804d0a0 / DAT_0804d0ac /
    DAT_0804d0e4 / DAT_0804d0e8 / DAT_0804d0ec /
    DAT_0804d118 / DAT_0804d11c / DAT_0804d120 /
    PTR_gP1LifePoints_0804d164 / DAT_0804d168 / DAT_0804d16c / DAT_0804d170 / DAT_0804d174 /
    DAT_0804d178 / DAT_0804d194 /
    PTR_gP1LifePoints_0804d1d4 / DAT_0804d1d8 / DAT_0804d1dc / DAT_0804d1e0  (x40)

- ROM_INCBIN / .byte 块:
  - 0x0804c734  size 0x38  (between case stubs and submit_slot_card_sprite_row_entry)
  - 0x0804cca2  size 0xea  (between submit_slot_card_sprite_row_packed and check_card_slot_activation_eligible)
  - 0x0804cdac  size 0x2c  (orphan code stubs inside 0x4cca2 island)

---

## データブロック分類 (Rule 2/3) -- ref-scan 証拠

| ブロック | ref-scan (raw / THUMB+1) | 判定 | 理由 |
|---|---|---|---|
| 0x4c734 sz=0x38 | raw=0 thumb=0 (exhaustive 4B scan) | §5.1 | 全 ROM 0 引用. 位置: classify_card_id_summon_category 末尾 case stubs と submit_slot_card_sprite_row_entry の間のギャップバイト. |
| 0x4cca2 sz=0xea | block start raw=0 thumb=0; sub-addr 0x4cd34 has raw=1 ref from 0x086bb944 (compressed resource area at ROM offset 0x6bb944 = 6.7MB, beyond asm code end 0x537c0; non-code, benign coincidence) | §5.1 | 外部コード参照ゼロ. 内部に bx lr x2 (0x4ccfc / 0x4cd72) あり THUMB コード形状だが, 末尾 .word 0x0804cd90 リテラルプールが 0x4cd8c に存在し PTR_DAT_0804cd90 jump table へのポインタを提供. そのジャンプテーブル先の 0x4cdac ブロックも含めて全体が孤立コードアイランド. |
| 0x4cdac sz=0x2c | raw=7 (all 7 entries of PTR_DAT_0804cd90 at 0x4cd90..0x4cda8, all internal to orphan island) thumb=0 | §5.1 | 外部参照ゼロ; raw 参照7件は全て上記孤立アイランド内の PTR_DAT_0804cd90 ポインタテーブル (自身も孤立, 7エントリ=0x4cd90/94/98/9c/cda0/cda4/cda8). 孤立アイランドの一部. |

孤立アイランド全体構造 (0x4cca2..0x4cdd7, 0x136 bytes):
```
0x4cca2..0x4cd8b: ROM_INCBIN 0xea - orphan THUMB code (2 fns with bx lr)
0x4cd8c:          .word 0x0804cd90 (literal pool for orphan code, refs PTR_DAT)
0x4cd90..0x4cda8: PTR_DAT_0804cd90 (7-entry ptr table -> 0x4cdac/0x4cdb6/0x4cdc2)
0x4cdac..0x4cdd7: ROM_INCBIN 0x2c - orphan THUMB stubs (3 entry points from ptr table)
```
全て §5.1 登記.

---

## 符号化計画 (R1/R2/R3)

### EQ_SLOTS (data-equate; 67 スロット)

凡例: (slot_addr, rom_value, const_name, slot_label, inc_file)

#### switchdataD_0804c6e8 case literal pool (Guardian weapon CIDs)

| スロット | 値 | 定数名 | スロットラベル | inc |
|---|---|---|---|---|
| 0x0804c704 | 0x0000165c | BUTTERFLY_DAGGER_ELMA_CID | classify_summon_cat_butterfly_dagger_elma_cid | card_info.inc NEW |
| 0x0804c70c | 0x0000165d | SHOOTING_STAR_BOW_CID | classify_summon_cat_shooting_star_bow_cid | card_info.inc EXISTS |
| 0x0804c714 | 0x0000165e | GRAVITY_AXE_GRARL_CID | classify_summon_cat_gravity_axe_grarl_cid | card_info.inc NEW |
| 0x0804c71c | 0x0000165f | WICKED_BREAKING_FLAMBERGE_BAOU_CID | classify_summon_cat_wicked_breaking_flamberge_cid | card_info.inc NEW |
| 0x0804c72c | 0x00001661 | TWIN_SWORDS_FLASHING_LIGHT_TRYCE_CID | classify_summon_cat_twin_swords_tryce_cid | card_info.inc NEW |

Notes:
- caseD_164e (0x1660 = Rod of Silence - Kay'est) computed inline as `movs r0,#0xb3; lsls r0,r0,#5` = 0xb3<<5 = 0x1660; no literal pool slot, no new constant.
- CID verification: 0x165c=Butterfly Dagger-Elma (pw=69243953 card_1332 slot=0x165C); 0x165d=Shooting Star Bow-Ceal (pw=95638658 card_1333 slot=0x165D exists); 0x165e=Gravity Axe-Grarl (pw=32022366 card_1334 slot=0x165E); 0x165f=Wicked-Breaking Flamberge-Baou (pw=68427465 card_1335 slot=0x165F); 0x1661=Twin Swords of Flashing Light-Tryce (pw=21900719 card_1337 slot=0x1661).

#### submit_slot_card_sprite_row_entry literal pool

| スロット | 値 | 定数名 | スロットラベル | inc |
|---|---|---|---|---|
| 0x0804c7e8 | 0x0000ffff | SLOT_CARD_EMPTY | submit_slot_sprite_id_mask | card_info.inc EXISTS (C5 reuse by value) |
| 0x0804c7f0 | 0x00001d08 | P1LP_BLOCK2_OFF | submit_slot_sprite_lp_block2_off | ewram.inc EXISTS |
| 0x0804c7f4 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | submit_slot_sprite_lp_block2_off_1ce8 | ewram.inc EXISTS |
| 0x0804c7f8 | 0x0201e2a0 | gDuelCardCtxBase | submit_slot_sprite_card_ctx_base | ewram.inc EXISTS |
| 0x0804c81c | 0x0201b290 | gDuelPhaseFlags | submit_slot_sprite_phase_flags_b | ewram.inc EXISTS |
| 0x0804c8c0 | 0x0201b290 | gDuelPhaseFlags | submit_slot_sprite_phase_flags_c | ewram.inc EXISTS |
| 0x0804c8c4 | 0xfffff03f | OAM_ATTR2_CLR_BITS_11_6 | submit_slot_sprite_attr2_clr_11_6 | oam_attr.inc NEW |
| 0x0804c8c8 | 0x000001ff | OAM_ATTR1_X_MASK | submit_slot_sprite_attr1_x_mask | oam_attr.inc EXISTS (C5 reuse) |
| 0x0804c8cc | 0xffff803f | SCROLLBAR_CLEAR_BITS_14_6 | submit_slot_sprite_attr2_clr_14_6 | gl_scrollbar.inc EXISTS (C5 reuse) |
| 0x0804c90c | 0x0201b290 | gDuelPhaseFlags | submit_slot_sprite_phase_flags_d | ewram.inc EXISTS |

Notes:
- 0xfffff03f = ~0x0fc0 = clears bits[11:6] in 32-bit word; used to clear OAM char-name bits after insert. 14 ROM literal refs. Not in any constants file. NEW constant OAM_ATTR2_CLR_BITS_11_6 in oam_attr.inc.
- 0xffff803f = SCROLLBAR_CLEAR_BITS_14_6 (gl_scrollbar.inc line 12): 37 ROM refs; C5 reuse by value even though semantic domain is OAM in this context.
- DAT_0804c81c slot is labeled as submit_slot_sprite_phase_flags_b (P1=player1 path); DAT_0804c8c0 as _c (P2 path in LAB_0804c820).

#### apply_equip_activation_with_id_lookup literal pool

| スロット | 値 | 定数名 | スロットラベル | inc |
|---|---|---|---|---|
| 0x0804c940 | 0x0000ffff | SLOT_CARD_EMPTY | apply_equip_activ_id_mask | card_info.inc EXISTS (C5 reuse) |

#### init_card_sprite_row_entry literal pool

| スロット | 値 | 定数名 | スロットラベル | inc |
|---|---|---|---|---|
| 0x0804ca44 | 0x000001ff | OAM_ATTR1_X_MASK | init_sprite_row_attr1_x_mask | oam_attr.inc EXISTS (C5 reuse) |
| 0x0804ca48 | 0xffff803f | SCROLLBAR_CLEAR_BITS_14_6 | init_sprite_row_attr2_clr_14_6 | gl_scrollbar.inc EXISTS (C5 reuse) |
| 0x0804ca4c | 0x0201b290 | gDuelPhaseFlags | init_sprite_row_phase_flags | ewram.inc EXISTS |
| 0x0804ca50 | 0x000004cc | LP_BAR_ANIM_STATE_OFF | init_sprite_row_slot_count_off | ewram.inc EXISTS (C5 reuse; same field acts as sprite row slot count) |
| 0x0804ca54 | 0xfffff03f | OAM_ATTR2_CLR_BITS_11_6 | init_sprite_row_attr2_clr_11_6 | oam_attr.inc NEW |
| 0x0804ca58 | 0x000004d4 | SPRITE_ROW_ENTRY_DATA_OFF | init_sprite_row_entry_data_off | ewram.inc NEW |

#### init_card_sprite_row_entry_alt literal pool

| スロット | 値 | 定数名 | スロットラベル | inc |
|---|---|---|---|---|
| 0x0804cbe0 | 0x000001ff | OAM_ATTR1_X_MASK | init_sprite_row_alt_attr1_x_mask | oam_attr.inc EXISTS (C5 reuse) |
| 0x0804cbe4 | 0xffff803f | SCROLLBAR_CLEAR_BITS_14_6 | init_sprite_row_alt_attr2_clr_14_6 | gl_scrollbar.inc EXISTS (C5 reuse) |
| 0x0804cbe8 | 0x0201b290 | gDuelPhaseFlags | init_sprite_row_alt_phase_flags | ewram.inc EXISTS |
| 0x0804cbec | 0x000004cc | LP_BAR_ANIM_STATE_OFF | init_sprite_row_alt_slot_count_off | ewram.inc EXISTS (C5 reuse) |
| 0x0804cbf0 | 0xfffff03f | OAM_ATTR2_CLR_BITS_11_6 | init_sprite_row_alt_attr2_clr_11_6 | oam_attr.inc NEW |
| 0x0804cbf4 | 0x000004d4 | SPRITE_ROW_ENTRY_DATA_OFF | init_sprite_row_alt_entry_data_off | ewram.inc NEW |

#### check_card_slot_activation_eligible BST literal pool

BST whitelist: card IDs forming BST comparison chain for special equip activation eligibility.
CID verification: 0x0fee=Cocoon of Evolution (pw=40240595); 0x1102=Swords of Revealing Light (pw=72302403); 0x1231=Kunai with Chain EXISTS; 0x1238=Metalmorph (pw=68540058); 0x1514=Blast with Chain EXISTS; 0x159c=Different Dimension Capsule EXISTS.

| スロット | 値 | 定数名 | スロットラベル | inc |
|---|---|---|---|---|
| 0x0804ce24 | 0x00001238 | METALMORPH_CID | check_slot_activ_bst_metalmorph_cid | card_info.inc NEW |
| 0x0804ce28 | 0x00001102 | SWORDS_OF_REVEALING_LIGHT_CID | check_slot_activ_bst_swords_reveal_cid | card_info.inc NEW |
| 0x0804ce2c | 0x00000fee | COCOON_OF_EVOLUTION_CID | check_slot_activ_bst_cocoon_evol_cid | card_info.inc NEW |
| 0x0804ce34 | 0x00001231 | KUNAI_WITH_CHAIN_CID | check_slot_activ_bst_kunai_chain_cid | card_info.inc EXISTS |
| 0x0804ce4c | 0x00001514 | BLAST_WITH_CHAIN_CID | check_slot_activ_bst_blast_chain_cid | card_info.inc EXISTS |
| 0x0804ce60 | 0x0000159c | DIFFERENT_DIMENSION_CAPSULE_CID | check_slot_activ_bst_dif_dim_cap_cid | card_info.inc EXISTS |

Notes: Remaining BST bounds (0xa0<<5=0x1400 and 0xcc<<5=0x1980) are computed inline; no literal pool slots.

#### dispatch_card_eligibility_state_machine literal pool

State machine uses gDuelPhaseFlags+ELIGIB_STATE_OFF (0x574) as the 32-entry switch state word.
gP1LifePoints+ELIGIB_*_OFF fields track equip eligibility context and animation state.

| スロット | 値 | 定数名 | スロットラベル | inc |
|---|---|---|---|---|
| 0x0804ce9c | 0x0201b290 | gDuelPhaseFlags | dispatch_eligib_phase_flags | ewram.inc EXISTS |
| 0x0804cea0 | 0x00000574 | ELIGIB_STATE_OFF | dispatch_eligib_state_off | ewram.inc NEW |
| 0x0804cf6c | 0x00000574 | ELIGIB_STATE_OFF | dispatch_eligib_caseD_0_state_off | ewram.inc NEW |
| 0x0804cf70 | 0x0201e2a0 | gDuelCardCtxBase | dispatch_eligib_caseD_1_card_ctx | ewram.inc EXISTS |
| 0x0804cf74 | 0x0201b290 | gDuelPhaseFlags | dispatch_eligib_caseD_1_phase_flags | ewram.inc EXISTS |
| 0x0804cf84 | 0x00000574 | ELIGIB_STATE_OFF | dispatch_eligib_caseD_1b_state_off | ewram.inc NEW |
| 0x0804d008 | 0x0201b290 | gDuelPhaseFlags | dispatch_eligib_caseD_1c_phase_flags | ewram.inc EXISTS |
| 0x0804d00c | 0x00000574 | ELIGIB_STATE_OFF | dispatch_eligib_caseD_1c_state_off | ewram.inc NEW |
| 0x0804d038 | 0x00000574 | ELIGIB_STATE_OFF | dispatch_eligib_caseD_2_state_off | ewram.inc NEW |
| 0x0804d03c | 0x00001d54 | ELIGIB_STATE_CTRL_OFF | dispatch_eligib_caseD_2_ctrl_off | ewram.inc NEW |
| 0x0804d054 | 0x0201b290 | gDuelPhaseFlags | dispatch_eligib_caseD_a_phase_flags | ewram.inc EXISTS |
| 0x0804d058 | 0x00000574 | ELIGIB_STATE_OFF | dispatch_eligib_caseD_a_state_off | ewram.inc NEW |
| 0x0804d074 | 0x00001d54 | ELIGIB_STATE_CTRL_OFF | dispatch_eligib_caseD_b_ctrl_off | ewram.inc NEW |
| 0x0804d078 | 0x00000574 | ELIGIB_STATE_OFF | dispatch_eligib_caseD_b_state_off | ewram.inc NEW |
| 0x0804d098 | 0x00001d5c | ELIGIB_ACT_TYPE_OFF | dispatch_eligib_caseD_b_act_type_off | ewram.inc NEW |
| 0x0804d09c | 0x00001d58 | ELIGIB_ACT_COUNT_OFF | dispatch_eligib_caseD_b_act_count_off | ewram.inc NEW |
| 0x0804d0a0 | 0x00000574 | ELIGIB_STATE_OFF | dispatch_eligib_caseD_b2_state_off | ewram.inc NEW |
| 0x0804d0ac | 0x00000574 | ELIGIB_STATE_OFF | dispatch_eligib_caseD_b3_state_off | ewram.inc NEW |
| 0x0804d0e4 | 0x00000584 | ELIGIB_RESULT_OFF | dispatch_eligib_caseD_14_result_off | ewram.inc NEW |
| 0x0804d0e8 | 0x0201b870 | gSpriteAttrBuf | dispatch_eligib_caseD_14_sprite_buf | ewram.inc EXISTS |
| 0x0804d0ec | 0x00000574 | ELIGIB_STATE_OFF | dispatch_eligib_caseD_14_state_off | ewram.inc NEW |
| 0x0804d118 | 0x0201b870 | gSpriteAttrBuf | dispatch_eligib_caseD_15_sprite_buf | ewram.inc EXISTS |
| 0x0804d11c | 0x00000584 | ELIGIB_RESULT_OFF | dispatch_eligib_caseD_15_result_off | ewram.inc NEW |
| 0x0804d120 | 0x00000574 | ELIGIB_STATE_OFF | dispatch_eligib_caseD_15_state_off | ewram.inc NEW |
| 0x0804d170 | 0x0201b290 | gDuelPhaseFlags | dispatch_eligib_caseD_1e_phase_flags | ewram.inc EXISTS |
| 0x0804d174 | 0x00000574 | ELIGIB_STATE_OFF | dispatch_eligib_caseD_1e_state_off | ewram.inc NEW |
| 0x0804d1dc | 0x0201b290 | gDuelPhaseFlags | dispatch_eligib_caseD_1f_phase_flags | ewram.inc EXISTS |
| 0x0804d1e0 | 0x00000584 | ELIGIB_RESULT_OFF | dispatch_eligib_caseD_1f_result_off | ewram.inc NEW |

Additional EQ slots (caseD_1e and caseD_1f body, still in Seg-5 through 0x4d123):

| スロット | 値 | 定数名 | スロットラベル | inc |
|---|---|---|---|---|
| 0x0804d168 | 0x00001d68 | ELIGIB_SPRITE_CTRL_OFF | dispatch_eligib_caseD_1e_sprite_ctrl_off | ewram.inc NEW |
| 0x0804d16c | 0x00008061 | SPRITE_ATTR_TYPE_HIDDEN_Y97 | dispatch_eligib_caseD_1e_sprite_hidden | oam_attr.inc NEW |
| 0x0804d178 | 0x00001d6c | ELIGIB_ANIM_STATE_OFF | dispatch_eligib_caseD_1f_anim_state_off | ewram.inc NEW |
| 0x0804d194 | 0x00001d44 | ELIGIB_CARD_ID_OFF | dispatch_eligib_caseD_1f_card_id_off | ewram.inc NEW |
| 0x0804d1d8 | 0x00001d54 | ELIGIB_STATE_CTRL_OFF | dispatch_eligib_caseD_1f_ctrl_off | ewram.inc NEW |

Notes on new constants (ewram.inc):
- ELIGIB_STATE_OFF = 0x574: [gDuelPhaseFlags+0x574] = 32-entry state word for dispatch_card_eligibility_state_machine; 18 ROM literal refs. Semantic: state index [0..0x1f].
- ELIGIB_RESULT_OFF = 0x584: [gDuelPhaseFlags+0x584] written with 0 (reset) or 1 (eligibility confirmed); 20 ROM literal refs.
  C5 collision note (user-mandated resolution): constants/duel_field.inc already defines GPRNG_SCENE_CTX_DISPLAY_FLAG_OFF = 0x00000584. Same numeric value but entirely different semantic domain and base register: GPRNG_SCENE_CTX_DISPLAY_FLAG_OFF is an offset applied to the value at gPrng+0x1c0 (a pointer dereference), while ELIGIB_RESULT_OFF is a direct offset from gDuelPhaseFlags. User has ruled: create ELIGIB_RESULT_OFF as an independent constant in ewram.inc; do NOT reuse GPRNG_SCENE_CTX_DISPLAY_FLAG_OFF (reuse would cause semantic confusion). This is a benign numeric collision between two unrelated structs at different EWRAM base addresses.
- SPRITE_ROW_ENTRY_DATA_OFF = 0x4d4: [gDuelPhaseFlags+0x4d4] = byte array for card sprite row entry flag data; 25 ROM literal refs. Used alongside LP_BAR_ANIM_STATE_OFF=0x4cc (count).
- ELIGIB_STATE_CTRL_OFF = 0x1d54: [gP1LifePoints+0x1d54] = eligibility state control word; 33 ROM literal refs.
- ELIGIB_ACT_COUNT_OFF = 0x1d58: [gP1LifePoints+0x1d58] = activation count field; 16 ROM literal refs.
- ELIGIB_ACT_TYPE_OFF = 0x1d5c: [gP1LifePoints+0x1d5c] = activation type flag (cmp #3); 17 ROM literal refs.
- ELIGIB_SPRITE_CTRL_OFF = 0x1d68: [gP1LifePoints+0x1d68] = sprite display control (0=show 0x61 sprite, non-0=use 0x8061 hidden); 105 ROM literal refs.
- ELIGIB_ANIM_STATE_OFF = 0x1d6c: [gP1LifePoints+0x1d6c] = animation state index (cmp 0xb/0xf); 56 ROM literal refs.
- ELIGIB_CARD_ID_OFF = 0x1d44: [gP1LifePoints+0x1d44] = card ID field accessed in caseD_1f; 9 ROM literal refs.

Note on new constants (oam_attr.inc):
- OAM_ATTR2_CLR_BITS_11_6 = 0xfffff03f: ~0x0fc0; clears bits[11:6] in 32-bit halfword word; used to clear OAM char-name field before OR-inserting tile index; 14 ROM literal refs.
- SPRITE_ATTR_TYPE_HIDDEN_Y97 = 0x00008061: OAM-style attr word; bit15=1 (OBJ disabled) | bits[5:0]=0x61=97 (Y coord); 81 ROM literal refs. Passed to enqueue_sprite_attr_record when [gP1LP+ELIGIB_SPRITE_CTRL_OFF] != 0. Contrast 0x0061 (OBJ enabled) used when field == 0.

New constants for card_info.inc:
- BUTTERFLY_DAGGER_ELMA_CID = 0x0000165c (pw=69243953 card_1332)
- GRAVITY_AXE_GRARL_CID = 0x0000165e (pw=32022366 card_1334)
- WICKED_BREAKING_FLAMBERGE_BAOU_CID = 0x0000165f (pw=68427465 card_1335)
- TWIN_SWORDS_FLASHING_LIGHT_TRYCE_CID = 0x00001661 (pw=21900719 card_1337)
- METALMORPH_CID = 0x00001238 (pw=68540058 card_0539)
- SWORDS_OF_REVEALING_LIGHT_CID = 0x00001102 (pw=72302403 card_0308)
- COCOON_OF_EVOLUTION_CID = 0x00000fee (pw=40240595 card_0079)

### REF_SLOTS (USER-label + DATA-ref): 0 スロット

No slots requiring REF label in this segment (all pointer values are addressed by EQ or RENAME).

### RENAME_SLOTS (改名 + EOL)

| スロット | 旧ラベル | 新ラベル | EOL |
|---|---|---|---|
| 0x0804c7ec | PTR_gP1LifePoints_0804c7ec | submit_slot_sprite_p1lp_ptr | .word gP1LifePoints ; 0x0201c4e0 |
| 0x0804d034 | PTR_gP1LifePoints_0804d034 | dispatch_eligib_caseD_2_p1lp_ptr | .word gP1LifePoints ; 0x0201c4e0 |
| 0x0804d070 | PTR_gP1LifePoints_0804d070 | dispatch_eligib_caseD_b_p1lp_ptr | .word gP1LifePoints ; 0x0201c4e0 |
| 0x0804d164 | PTR_gP1LifePoints_0804d164 | dispatch_eligib_caseD_1e_p1lp_ptr | .word gP1LifePoints ; 0x0201c4e0 |
| 0x0804d1d4 | PTR_gP1LifePoints_0804d1d4 | dispatch_eligib_caseD_1f_p1lp_ptr | .word gP1LifePoints ; 0x0201c4e0 |
| 0x0804cd90 | PTR_DAT_0804cd90 | orphan_slot_card_eligible_fn_table | orphan jump table (0 external refs); 7 entries pointing to 0x4cdac/0x4cdb6/0x4cdc2 |
| 0x0804cfb4 | DAT_0804cfb4 | dispatch_eligib_caseD_1_ineligible_cid_tbl | .word 0x09e3f118 ; ROM ptr: 10-entry CID array {0x14f9,0x154f,0x1550,0x1551,0x1730,0x1731,0x1670,0x1671,0x1672,0x1288} |
| 0x0804cea4 | DAT_0804cea4 | dispatch_eligib_switchdata_ptr | .word switchD_0804ce98__switchdataD_0804cea8 ; ptr to 32-entry jump table |

Note: PTR_DAT_0804cd90 at 0x4cd90 is not itself a ROM_INCBIN slot -- it is an existing label in
the asm for the jump table structure. The RENAME changes its label to orphan_slot_card_eligible_fn_table.
DAT_0804cea4 points to the 32-entry switch data table for dispatch_card_eligibility_state_machine.

### FUNC_RENAME: 0

No misnaming detected. All 7 functions' plates match their operations.
Note: plates for apply_equip_activation_with_id_lookup and init_card_sprite_row_entry* reference
FUN_* caller addresses (FUN_080432bc etc.) -- these are callers in Seg-6+ and will be fixed
when those segments are refined; NOT a Seg-5 FUNC_RENAME item.

### PLATE (R5): 0 rewrites required

No stale FUN_ references inside Seg-5's own function plates (the FUN_ refs are for callers
outside the segment and will be fixed in future segments).

---

## carve 計画 (R7): 0

No inter-function ROM_INCBIN with external references. All 3 ROM_INCBIN blocks are orphan
(0 external code refs) -> §5.1.

---

## disasm 計画 (R4): 0

No ROM_INCBIN with external THUMB references requiring disassembly in this segment.
The orphan 0x4cca2 and 0x4cdac blocks contain THUMB code but have zero external callers;
they are classified §5.1 per Rule 3 (0-ref -> defer, do not disasm).

---

## 新増 constants / 全局

### card_info.inc 追加 (7 新 CID)

```
.equ BUTTERFLY_DAGGER_ELMA_CID,            0x0000165c  @ Butterfly Dagger-Elma (pw=69243953); classify_card_id_summon_category case Guardian weapon
.equ GRAVITY_AXE_GRARL_CID,               0x0000165e  @ Gravity Axe-Grarl (pw=32022366); classify_card_id_summon_category case Guardian weapon
.equ WICKED_BREAKING_FLAMBERGE_BAOU_CID,  0x0000165f  @ Wicked-Breaking Flamberge-Baou (pw=68427465); classify_card_id_summon_category case Guardian weapon
.equ TWIN_SWORDS_FLASHING_LIGHT_TRYCE_CID, 0x00001661 @ Twin Swords of Flashing Light-Tryce (pw=21900719); classify_card_id_summon_category case Guardian weapon
.equ COCOON_OF_EVOLUTION_CID,             0x00000fee  @ Cocoon of Evolution (pw=40240595); check_card_slot_activation_eligible BST lower bound
.equ SWORDS_OF_REVEALING_LIGHT_CID,       0x00001102  @ Swords of Revealing Light (pw=72302403); check_card_slot_activation_eligible BST
.equ METALMORPH_CID,                      0x00001238  @ Metalmorph (pw=68540058); check_card_slot_activation_eligible BST (Kunai+7 computed inline elsewhere)
```

### oam_attr.inc 追加 (2 新定数)

```
.equ OAM_ATTR2_CLR_BITS_11_6,  0xfffff03f  @ AND mask clearing bits[11:6]; used to clear OAM char-name tile index field in sprite row packing (submit_slot_card_sprite_row_entry + init variants); 14 ROM refs
.equ SPRITE_ATTR_TYPE_HIDDEN_Y97, 0x00008061 @ OBJ disabled (bit15=1) | Y=0x61; passed to enqueue_sprite_attr_record when eligib_sprite_ctrl [gP1LP+0x1d68] != 0; 81 ROM refs
```

### ewram.inc 追加 (9 新定数)

All gDuelPhaseFlags-relative offsets (base=0x0201b290):

```
.equ SPRITE_ROW_ENTRY_DATA_OFF,  0x000004d4  @ [gDuelPhaseFlags+0x4d4] byte array for card sprite row entry flag data; init_card_sprite_row_entry iterates count(LP_BAR_ANIM_STATE_OFF) entries; 25 ROM refs
.equ ELIGIB_STATE_OFF,           0x00000574  @ [gDuelPhaseFlags+0x574] dispatch_card_eligibility_state_machine state word [0..0x1f]; indexes 32-entry switch table; 18 ROM refs
.equ ELIGIB_RESULT_OFF,          0x00000584  @ [gDuelPhaseFlags+0x584] eligibility result field; 0=pending, 1=confirmed; written by caseD_14/15/1f; 20 ROM refs
```

All gP1LifePoints-relative offsets (base=0x0201c4e0):

```
.equ ELIGIB_CARD_ID_OFF,         0x00001d44  @ [gP1LifePoints+0x1d44] card_id field accessed in dispatch_card_eligibility_state_machine caseD_1f; 9 ROM refs
.equ ELIGIB_STATE_CTRL_OFF,      0x00001d54  @ [gP1LifePoints+0x1d54] eligibility state control word; written to state values (0, 0xa, 0x1e etc.) by various cases; 33 ROM refs
.equ ELIGIB_ACT_COUNT_OFF,       0x00001d58  @ [gP1LifePoints+0x1d58] activation count field; written r0=1 in caseD_b; 16 ROM refs
.equ ELIGIB_ACT_TYPE_OFF,        0x00001d5c  @ [gP1LifePoints+0x1d5c] activation type flag; cmp r0,#3 in caseD_b determines branch; 17 ROM refs
.equ ELIGIB_SPRITE_CTRL_OFF,     0x00001d68  @ [gP1LifePoints+0x1d68] sprite display control; 0=display 0x61 attr, non-0=use 0x8061 hidden attr for enqueue_sprite_attr_record; 105 ROM refs
.equ ELIGIB_ANIM_STATE_OFF,      0x00001d6c  @ [gP1LifePoints+0x1d6c] animation state index; range check [0..0xf] in caseD_1f with thresholds 0xb/0xf; 56 ROM refs
```

---

## §5.1 登記 (Rule 3) -- 0 引用ブロック

| 地址 | 大小 | 所在 | 初判内容 | ref-scan 証拠 |
|---|---|---|---|---|
| 0x0804c734 | 0x38 (56B) | Seg-5 | Gap bytes between classify_card_id_summon_category tail and submit_slot_card_sprite_row_entry; opaque byte sequence | exhaustive 4B scan: 0 raw/thumb refs anywhere in ROM |
| 0x0804cca2 | 0xea (234B) | Seg-5 | Orphan THUMB code block (2 bx lr at 0x4ccfc/0x4cd72); loads ptr to PTR_DAT_0804cd90; between submit_slot_card_sprite_row_packed and check_card_slot_activation_eligible | block start: raw=0 thumb=0; only sub-addr 0x4cd34 has raw=1 ref from 0x086bb944 (compressed resource area, not code) |
| 0x0804cdac | 0x2c (44B) | Seg-5 | Orphan THUMB stubs (3 entry pts at 0x4cdac/0x4cdb6/0x4cdc2, return 0/1 based on arg comparisons); part of orphan island 0x4cca2..0x4cdd7 | raw=7 (all 7 entries of PTR_DAT_0804cd90 table at 0x4cd90..0x4cda8, all internal to orphan island; entries 0,1,3->0x4cdac, entries 4,5->0x4cdb6, entries 2,6->0x4cdc2) thumb=0; 0 external refs |

Total orphan island: 0x4cca2..0x4cdd7 (0x136 = 310 bytes). The PTR_DAT_0804cd90 table at
0x4cd90..0x4cda8 is between the two ROM_INCBIN blocks but is already an asm label (not ROM_INCBIN);
it is part of the same orphan island. The .word 0x0804cd90 literal at 0x4cd8c is inside the
first ROM_INCBIN block.

---

## 消費者証拠 (R6)

### submit_slot_card_sprite_row_entry (0x0804c76c)

Evidence: `asm/05_equip_eligibility_a.s` line 7824-8038. Confidence: high.
- r0=player_side [0..1], r1=card_id [0..0xffff], r2=slot_idx u16 (0=dynamic find), r3=slot_data_word.
- gP1LifePoints+P1LP_BLOCK2_OFF (0x1d08): ldr r2,[r2+r1] -> match check for player_id (line 7849-7863).
- gP1LifePoints+P1LP_BLOCK2_OFF_1CE8 (0x1ce8): ldr r3 adds r2,r2,r3 -> slot ptr offset (line 7855-7856).
- gDuelCardCtxBase (0x0201e2a0): loaded as equip context base for ldr r0,[r0,0x4] player_side check (line 7849-7863).
- gDuelPhaseFlags+0x480 (P1 path) / gDuelPhaseFlags+0x488 (P2 path): sprite row slot count at struct base.
- OAM_ATTR2_CLR_BITS_11_6 (0xfffff03f): ands r0,r3 before strh to clear char-name bits (line 7973-7975).
- LP_BAR_ANIM_STATE_OFF (0x4cc): slot count for P1 path counter increment (line 7993-7995).

### apply_equip_activation_with_id_lookup (0x0804c910)

Evidence: `asm/05_equip_eligibility_a.s` line 8041-8077. Confidence: high.
- plate comment: "indeg=61" -- called 61 times as THUMB function pointer from duel_field.
- SLOT_CARD_EMPTY (0x0000ffff): ands r1,r5 -> low-16bit card ID extract (line 8050-8051).
- Calls find_slot_idx_in_dual_list_by_id then apply_equip_activation_via_packed_attr.

### init_card_sprite_row_entry (0x0804c958)

Evidence: `asm/05_equip_eligibility_a.s` line 8079-8283. Confidence: high.
- plate comment: "3 callers from FUN_08095ba8/FUN_08095ca0/FUN_08095d84 (duel_field)".
- LP_BAR_ANIM_STATE_OFF (0x4cc): ldr r1=[gDuelPhaseFlags+0x4cc] = slot count (line 8154-8157).
- SPRITE_ROW_ENTRY_DATA_OFF (0x4d4): ldr r3=[base+0x4d4] used to iterate byte array (line 8169-8173).
- dispatch_card_effect_activation: called for each active slot card (line 8189).
- submit_slot_card_sprite_row_entry: called on activation match (line 8239).

### check_card_slot_activation_eligible (0x0804cdd8)

Evidence: `asm/05_equip_eligibility_a.s` line 8526-8614. Confidence: high.
- indeg=0 per plate (called via function pointer dispatch).
- BST: METALMORPH_CID(0x1238) as pivot: cmp r1,r0 beq return_special / bgt -> BST_high.
- SWORDS_OF_REVEALING_LIGHT_CID (0x1102): sub-BST lower bound beq return 0.
- COCOON_OF_EVOLUTION_CID (0x0fee): lower bound branch return 1 (not in whitelist).
- KUNAI_WITH_CHAIN_CID (0x1231): BST node beq return_special (line 8571).
- BLAST_WITH_CHAIN_CID (0x1514): higher-branch BST node (line 8576-8581).
- DIFFERENT_DIMENSION_CAPSULE_CID (0x159c): highest explicit BST node beq return_special (line 8592-8596).
- Return semantic: 0=not eligible, 1=eligible, BST whitelist hit extracts bit from [r4+4][29].

### dispatch_card_eligibility_state_machine (0x0804ce78)

Evidence: `asm/05_equip_eligibility_a.s` line 8616-9045. Confidence: high.
- ELIGIB_STATE_OFF (0x574): ldr r0=[gDuelPhaseFlags+0x574]; cmp r0,0x1f; dispatches 32-entry switch (line 8630-8638).
- ELIGIB_STATE_CTRL_OFF (0x1d54): read/written across caseD_2/b/1f as primary state control.
- ELIGIB_ACT_TYPE_OFF (0x1d5c): caseD_b reads [gP1LP+0x1d5c]; cmp r0,#3 determines activation path.
- ELIGIB_RESULT_OFF (0x584): written 0 (reset in caseD_14) / written 1 (confirm in caseD_1f epilogue).
- ELIGIB_SPRITE_CTRL_OFF (0x1d68): caseD_1e reads to choose 0x61 vs 0x8061 sprite attr type.
- ELIGIB_ANIM_STATE_OFF (0x1d6c): caseD_1f reads; cmp 0xb and cmp 0xf threshold checks.
- SPRITE_ATTR_TYPE_HIDDEN_Y97 (0x8061): ldr r1=0x8061; bl enqueue_sprite_attr_record on ctrl!=0.
- dispatch_eligib_caseD_1_ineligible_cid_tbl (0x09e3f118): ROM table of 10 CIDs for text lookup in caseD_1 fail path; ldr r1,DAT_0804cfb4; bl append_game_text_if_raw (line 8744-8749).

---

## 求助

None. All slots have sufficient consumer evidence.
Low-confidence items resolved:
- 0x0000ffff slots (DAT_0804c7e8 / DAT_0804c940): confirmed as 16-bit ID extract masks via consumer code (ands r1,r5 where r5=card_id_packed); C5 reuse of SLOT_CARD_EMPTY. Confidence: high (file:line 7837-7838 / 8050-8051).
- ELIGIB_*_OFF values: all derived from direct consumer code in dispatch_card_eligibility_state_machine; no ambiguity in read/write direction.
- PTR_DAT_0804cd90 orphan classification: confirmed 0 external refs via exhaustive scan; 0x086bb944 ref to 0x4cd34 is in compressed resource area (ROM offset 0x6bb944 = 6.7MB, beyond all asm code end 0x537c0). Confidence: high.
