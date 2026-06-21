# Refine Proposal: F10-Seg-9  [0x08083450..0x08084318)

## 段测绘

- 函数入口: x18 (全部已命名)
  - 0x08083450 tick_equip_target_select_4state
  - 0x08083560 tick_equip_best_target_display_4state
  - 0x08083704 tick_equip_lamp_dream_zone_activation_3state
  - 0x08083824 enqueue_equip_slot_sprite_if_equipped
  - 0x0808386c advance_equip_zone_slot_display_seq
  - 0x08083968 check_effect_slot_zone_player_by_type
  - 0x080839b4 tick_equip_placement_bitmap_display_4state
  - 0x08083b54 check_equip_slot_pair_blocked
  - 0x08083ba0 tick_equip_activation_sprite_array_4state
  - 0x08083c98 tick_equip_lp_row_display_by_state
  - 0x08083d38 tick_equip_card_display_3state
  - 0x08083e14 tick_equip_lamp_dream_activation_3state
  - 0x08083f4c tick_equip_activation_display_seq_a
  - 0x08084038 tick_equip_lp_score_display_seq
  - 0x08084144 check_lp_node_state_for_display_advance
  - 0x0808416c dispatch_equip_display_if_confirm_state_two
  - 0x08084180 dispatch_equip_display_by_type_code_or_card_id
  - 0x080841c0 enqueue_effect_node_sprites_for_both_players

- 残留自动名槽: x92 (20 DAT_ + 69 DWORD_ + 3 PTR_gP1LifePoints_)
  - Full list in EQ/REF/RENAME_SLOTS tables below.

- ROM_INCBIN / .byte 块: x2
  - BLK1: 0x8420e  size=0x26  (38 B)  label=none (between enqueue_effect_node_sprites_for_both_players and JT .words)
  - BLK2: 0x8424c  size=0xcc  (204 B)  label=DAT_0808424c

---

## 数据块分类 (Rule 2/3) -- 每块给 ref-scan 证据

| 块 | ref-scan (raw / THUMB+1) | 判定 | 理由 |
|---|---|---|---|
| BLK1 0x8420e/0x26 | raw=0; THUMB+1 @ 0x09e410b8 => 1 real hit (dispatch table entry CID=0x1536 Book of Life); extra THUMB hits 0x84212/0x8421a in compressed data (coincidental) | R4 disasm | Single real THUMB+1 ref from 0x09e4xxxx card effect dispatch table confirms fn_eligible stub for Book of Life |
| BLK2 0x8424c/0xcc | raw=6 (JT at 0x84234 6 .word entries already decoded in asm lines 22618-22623); THUMB+1 only coincidental (0x0808428d@0x08a2c607 / 0x08084307@0x08f28375 = compressed data); no dispatch table THUMB+1 | R4 disasm | 6 raw .word pointers in JT at 0x84234 (already decoded); BLK2 = 6 dispatch sub-stubs for Book of Life fn_eligible states 0-5 |

**ref-scan detail (BLK1)**:
- BLK1 GBA start = 0x0808420e (2B zero-pad alignment); fn_eligible THUMB code starts at 0x08084210 (opcode 0xb570 = push {r4,r5,r6,lr})
- THUMB+1 val = 0x08084211 (fn_eligible start 0x08084210 + 1); search ROM -> 1 hit at GBA 0x09e410b8 (file 0x1e410b8)
- Confirmed: dispatch table entry at 0x09e410a4 (+0x14 = fn_eligible+1 field); entry[0] = CID 0x1536 at 0x09e410a4
- card-stats.s card_1115: Book of Life, slot=0x1536, pw=02204140 (line 14510) -> NEW BOOK_OF_LIFE_CID

**ref-scan detail (BLK2)**:
- BLK2 GBA 0x0808424c..0x08084318
- 6 .word raw pointers in asm lines 22618-22623: 0x0808424c / 0x0808429a / 0x080842cc / 0x080842ac / 0x080842ba / 0x080842cc
- These address sub-stubs for states 0,1,2,3,4,5 (state 2 and 5 share 0x080842cc)
- JT at 0x84234 is NOT a separate ROM_INCBIN -- already decoded as 6 .word literals

---

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS  (data-equate; REUSE=existing constant / NEW=不存在)

Slots grouped by value. Evidence format: "REUSE <inc>:<line>" or "NEW card-stats.s:<line> / no grep hit".

**gDuelPhaseFlags / STATE_OFFSET pattern (value=0x0201b290, STATE at +0x4b0=0x96*8)**

| slot | addr | value | const_name | slot_label | C5 |
|------|------|-------|------------|------------|----|
| DAT_08083470 | 0x08083470 | 0x0201b290 | gDuelPhaseFlags | duel_phase_flags_08083470 | REUSE ewram.inc |
| DAT_0808353c | 0x0808353c | 0x0201b290 | gDuelPhaseFlags | duel_phase_flags_0808353c | REUSE ewram.inc |
| DAT_08083554 | 0x08083554 | 0x0201b290 | gDuelPhaseFlags | duel_phase_flags_08083554 | REUSE ewram.inc |
| DAT_08083580 | 0x08083580 | 0x0201b290 | gDuelPhaseFlags | duel_phase_flags_08083580 | REUSE ewram.inc |
| DWORD_08083728 | 0x08083728 | 0x0201b290 | gDuelPhaseFlags | duel_phase_flags_08083728 | REUSE ewram.inc |
| DWORD_0808378c | 0x0808378c | 0x0201b290 | gDuelPhaseFlags | duel_phase_flags_0808378c | REUSE ewram.inc |
| DWORD_080837e4 | 0x080837e4 | 0x0201b290 | gDuelPhaseFlags | duel_phase_flags_080837e4 | REUSE ewram.inc |
| DWORD_08083888 | 0x08083888 | 0x0201b290 | gDuelPhaseFlags | duel_phase_flags_08083888 | REUSE ewram.inc |
| DWORD_08083940 | 0x08083940 | 0x0201b290 | gDuelPhaseFlags | duel_phase_flags_08083940 | REUSE ewram.inc |
| DWORD_080839d8 | 0x080839d8 | 0x0201b290 | gDuelPhaseFlags | duel_phase_flags_080839d8 | REUSE ewram.inc |
| DWORD_08083b2c | 0x08083b2c | 0x0201b290 | gDuelPhaseFlags | duel_phase_flags_08083b2c | REUSE ewram.inc |
| DWORD_08083b44 | 0x08083b44 | 0x0201b290 | gDuelPhaseFlags | duel_phase_flags_08083b44 | REUSE ewram.inc |
| DWORD_08083bc0 | 0x08083bc0 | 0x0201b290 | gDuelPhaseFlags | duel_phase_flags_08083bc0 | REUSE ewram.inc |
| DWORD_08083c1c | 0x08083c1c | 0x0201b290 | gDuelPhaseFlags | duel_phase_flags_08083c1c | REUSE ewram.inc |
| DWORD_08083c70 | 0x08083c70 | 0x0201b290 | gDuelPhaseFlags | duel_phase_flags_08083c70 | REUSE ewram.inc |
| DWORD_08083c88 | 0x08083c88 | 0x0201b290 | gDuelPhaseFlags | duel_phase_flags_08083c88 | REUSE ewram.inc |
| DWORD_08083cb4 | 0x08083cb4 | 0x0201b290 | gDuelPhaseFlags | duel_phase_flags_08083cb4 | REUSE ewram.inc |
| DWORD_08083d58 | 0x08083d58 | 0x0201b290 | gDuelPhaseFlags | duel_phase_flags_08083d58 | REUSE ewram.inc |
| DWORD_08083e30 | 0x08083e30 | 0x0201b290 | gDuelPhaseFlags | duel_phase_flags_08083e30 | REUSE ewram.inc |
| DWORD_08083edc | 0x08083edc | 0x0201b290 | gDuelPhaseFlags | duel_phase_flags_08083edc | REUSE ewram.inc |
| DWORD_08083f6c | 0x08083f6c | 0x0201b290 | gDuelPhaseFlags | duel_phase_flags_08083f6c | REUSE ewram.inc |
| DWORD_08083fd0 | 0x08083fd0 | 0x0201b290 | gDuelPhaseFlags | duel_phase_flags_08083fd0 | REUSE ewram.inc |
| DWORD_08084010 | 0x08084010 | 0x0201b290 | gDuelPhaseFlags | duel_phase_flags_08084010 | REUSE ewram.inc |
| DWORD_08084028 | 0x08084028 | 0x0201b290 | gDuelPhaseFlags | duel_phase_flags_08084028 | REUSE ewram.inc |
| DWORD_0808405c | 0x0808405c | 0x0201b290 | gDuelPhaseFlags | duel_phase_flags_0808405c | REUSE ewram.inc |
| DWORD_08084140 | 0x08084140 | 0x0201b290 | gDuelPhaseFlags | duel_phase_flags_08084140 | REUSE ewram.inc |

**gDuelCardCtxBase (0x0201e2a0) -- activation_ctx**

| slot | addr | value | const_name | slot_label | C5 |
|------|------|-------|------------|------------|----|
| DAT_080834d0 | 0x080834d0 | 0x0201e2a0 | gDuelCardCtxBase | duel_card_ctx_base_080834d0 | REUSE ewram.inc |
| DAT_08083660 | 0x08083660 | 0x0201e2a0 | gDuelCardCtxBase | duel_card_ctx_base_08083660 | REUSE ewram.inc |
| DWORD_080837c0 | 0x080837c0 | 0x0201e2a0 | gDuelCardCtxBase | duel_card_ctx_base_080837c0 | REUSE ewram.inc |
| DWORD_08083910 | 0x08083910 | 0x0201e2a0 | gDuelCardCtxBase | duel_card_ctx_base_08083910 | REUSE ewram.inc |
| DWORD_08083a40 | 0x08083a40 | 0x0201e2a0 | gDuelCardCtxBase | duel_card_ctx_base_08083a40 | REUSE ewram.inc |
| DWORD_08083d94 | 0x08083d94 | 0x0201e2a0 | gDuelCardCtxBase | duel_card_ctx_base_08083d94 | REUSE ewram.inc |
| DWORD_08083ebc | 0x08083ebc | 0x0201e2a0 | gDuelCardCtxBase | duel_card_ctx_base_08083ebc | REUSE ewram.inc |

**gEquipChainSlotRefs (0x0201bb90)**

| slot | addr | value | const_name | slot_label | C5 |
|------|------|-------|------------|------------|----|
| DWORD_08083788 | 0x08083788 | 0x0201bb90 | gEquipChainSlotRefs | equip_chain_slot_refs_08083788 | REUSE ewram.inc |
| DWORD_08083d90 | 0x08083d90 | 0x0201bb90 | gEquipChainSlotRefs | equip_chain_slot_refs_08083d90 | REUSE ewram.inc |

**ELIGIB_SPRITE_CTRL_OFF (0x00001d68) and ELIGIB_ANIM_STATE_OFF (0x00001d6c)**

| slot | addr | value | const_name | slot_label | C5 |
|------|------|-------|------------|------------|----|
| DAT_08083538 | 0x08083538 | 0x00001d68 | ELIGIB_SPRITE_CTRL_OFF | eligib_sprite_ctrl_off_08083538 | REUSE ewram.inc:422 |
| DAT_080836e8 | 0x080836e8 | 0x00001d68 | ELIGIB_SPRITE_CTRL_OFF | eligib_sprite_ctrl_off_080836e8 | REUSE ewram.inc:422 |
| DWORD_08083b28 | 0x08083b28 | 0x00001d68 | ELIGIB_SPRITE_CTRL_OFF | eligib_sprite_ctrl_off_08083b28 | REUSE ewram.inc:422 |
| DWORD_08083c6c | 0x08083c6c | 0x00001d68 | ELIGIB_SPRITE_CTRL_OFF | eligib_sprite_ctrl_off_08083c6c | REUSE ewram.inc:422 |
| DWORD_08083df8 | 0x08083df8 | 0x00001d68 | ELIGIB_SPRITE_CTRL_OFF | eligib_sprite_ctrl_off_08083df8 | REUSE ewram.inc:422 |
| DWORD_0808400c | 0x0808400c | 0x00001d68 | ELIGIB_SPRITE_CTRL_OFF | eligib_sprite_ctrl_off_0808400c | REUSE ewram.inc:422 |
| DWORD_08083f40 | 0x08083f40 | 0x00001d68 | ELIGIB_SPRITE_CTRL_OFF | eligib_sprite_ctrl_off_08083f40 | REUSE ewram.inc:422 |
| DAT_080836ec | 0x080836ec | 0x00001d6c | ELIGIB_ANIM_STATE_OFF | eligib_anim_state_off_080836ec | REUSE ewram.inc:423 |
| DWORD_08083dfc | 0x08083dfc | 0x00001d6c | ELIGIB_ANIM_STATE_OFF | eligib_anim_state_off_08083dfc | REUSE ewram.inc:423 |

**LP_CARD_TRACK_BASE_OFF (0x00001da8) / LP_CARD_TRACK_NEXT_OFF (0x00001daa)**

| slot | addr | value | const_name | slot_label | C5 |
|------|------|-------|------------|------------|----|
| DWORD_0808411c | 0x0808411c | 0x00001da8 | LP_CARD_TRACK_BASE_OFF | lp_card_track_base_off_0808411c | REUSE ewram.inc:247 |
| DWORD_08083d28 | 0x08083d28 | 0x00001daa | LP_CARD_TRACK_NEXT_OFF | lp_card_track_next_off_08083d28 | REUSE ewram.inc:248 |

**0x00001d40 -- LP pending activation flag offset (NEW)**
Used by 9 functions: stores/reads [gP1LifePoints+0x1d40] as LP display activation pending flag.
Value = 0xea << 5 = 0x1d40. grep "0x00001d40" constants/ -> 0 hits. NEW: LP_ACTIVATION_PENDING_OFF = 0x00001d40.

| slot | addr | value | const_name | slot_label | C5 |
|------|------|-------|------------|------------|----|
| (inline via ea<<5 pattern; no standalone slot; 0xea immediate) | - | - | LP_ACTIVATION_PENDING_OFF | - | NEW: grep=0 |

Note: The value 0x1d40 is always computed as `movs r1,#0xea; lsls r1,r1,#0x5` inline -- no standalone literal pool slot loads this value directly; Ghidra equate applies to the immediates or inline computation EOL.

**0xfffc7fff -- effect node attribute clear mask (REUSE DUAL_LABEL_RENDER_STATE_CLEAR)**
AND mask clears bits[17:15] of effect_node[+4]. grep "0xfffc7fff" constants/ -> duel_field.inc:134 DUAL_LABEL_RENDER_STATE_CLEAR = 0xFFFC7FFF (same bit-pattern + semantics; already used in Seg-7a/8b).
REUSE: DUAL_LABEL_RENDER_STATE_CLEAR (duel_field.inc:134). Do NOT create NEW EQUIP_NODE_ATTR_CLEAR_MASK.
Appears in: DAT_080834cc, DAT_080835c0, DWORD_08083908, DWORD_08083a3c, DWORD_08083c14, DWORD_08083e6c, DWORD_08083fc8 (7 slots in Seg-9; also 33 total in file 10).

| slot | addr | value | const_name | slot_label | C5 |
|------|------|-------|------------|------------|----|
| DAT_080834cc | 0x080834cc | 0xfffc7fff | DUAL_LABEL_RENDER_STATE_CLEAR | dual_label_render_state_clear_080834cc | REUSE duel_field.inc:134 |
| DAT_080835c0 | 0x080835c0 | 0xfffc7fff | DUAL_LABEL_RENDER_STATE_CLEAR | dual_label_render_state_clear_080835c0 | REUSE duel_field.inc:134 |
| DWORD_08083908 | 0x08083908 | 0xfffc7fff | DUAL_LABEL_RENDER_STATE_CLEAR | dual_label_render_state_clear_08083908 | REUSE duel_field.inc:134 |
| DWORD_08083a3c | 0x08083a3c | 0xfffc7fff | DUAL_LABEL_RENDER_STATE_CLEAR | dual_label_render_state_clear_08083a3c | REUSE duel_field.inc:134 |
| DWORD_08083c14 | 0x08083c14 | 0xfffc7fff | DUAL_LABEL_RENDER_STATE_CLEAR | dual_label_render_state_clear_08083c14 | REUSE duel_field.inc:134 |
| DWORD_08083e6c | 0x08083e6c | 0xfffc7fff | DUAL_LABEL_RENDER_STATE_CLEAR | dual_label_render_state_clear_08083e6c | REUSE duel_field.inc:134 |
| DWORD_08083fc8 | 0x08083fc8 | 0xfffc7fff | DUAL_LABEL_RENDER_STATE_CLEAR | dual_label_render_state_clear_08083fc8 | REUSE duel_field.inc:134 |

**TRIGGER_OP_PARAM_107 (0x00000107)**

| slot | addr | value | const_name | slot_label | C5 |
|------|------|-------|------------|------------|----|
| DAT_080835c4 | 0x080835c4 | 0x00000107 | TRIGGER_OP_PARAM_107 | trigger_op_param_107_080835c4 | REUSE duel_field.inc:312 |

**PLAYER_BLOCK_STRIDE (0x00000868)**

| slot | addr | value | const_name | slot_label | C5 |
|------|------|-------|------------|------------|----|
| DAT_08083664 | 0x08083664 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_08083664 | REUSE ewram.inc |
| DWORD_080840dc | 0x080840dc | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_080840dc | REUSE ewram.inc |

**gDuelFieldSlots (0x0201c510)**

| slot | addr | value | const_name | slot_label | C5 |
|------|------|-------|------------|------------|----|
| DAT_08083668 | 0x08083668 | 0x0201c510 | gDuelFieldSlots | duel_field_slots_08083668 | REUSE ewram.inc |

**0x9e180000 = GEARFRIED_IRON_KNIGHT_CID(0x13c3) << 0x13 -- shifted CID sentinel (NEW)**
Used in tick_equip_best_target_display_4state: `lsls r0,r0,#0x13; cmp r0,#0x9e180000` to skip Gearfried as equip target.
grep "0x9e180000" constants/ -> 0 hits.
Pattern: DNA_TRANSPLANT_CID_SHIFTED = 0xb8f80000 exists (card_info.inc:396); same pattern.
NEW: GEARFRIED_IRON_KNIGHT_CID_SHIFTED = 0x9e180000.

| slot | addr | value | const_name | slot_label | C5 |
|------|------|-------|------------|------------|----|
| DAT_0808366c | 0x0808366c | 0x9e180000 | GEARFRIED_IRON_KNIGHT_CID_SHIFTED | gearfried_shifted_cid_08083 66c | NEW; grep=0 |

**RED_MOON_BABY_CID (0x00001415)**

| slot | addr | value | const_name | slot_label | C5 |
|------|------|-------|------------|------------|----|
| DWORD_0808390c | 0x0808390c | 0x00001415 | RED_MOON_BABY_CID | red_moon_baby_cid_0808390c | REUSE card_info.inc:1175 |

**0x00000109 -- invoke_card_display_op_0x31_sub1 param in tick_equip_lamp_dream_zone_activation_3state (NEW)**
Function call: `ldr r0, #0x109; bl invoke_card_display_op_0x31_sub1` at 0x080837c8-0x080837ca.
grep "0x00000109" constants/ -> 0 hits. Distinct from TRIGGER_OP_PARAM_107 (0x107).
NEW: INVOKE_OP31_SUB1_PARAM_109 = 0x00000109.

| slot | addr | value | const_name | slot_label | C5 |
|------|------|-------|------------|------------|----|
| DWORD_080837e0 | 0x080837e0 | 0x00000109 | INVOKE_OP31_SUB1_PARAM_109 | invoke_op31_sub1_param_109_08 | NEW; grep=0 |

**ANCIENT_LAMP_CID (0x00001476) (NEW)**
card-stats.s card_0950: Ancient Lamp, slot=0x1476, pw=54912977 (line 12365).
grep "0x00001476" constants/ -> 0 hits.

| slot | addr | value | const_name | slot_label | C5 |
|------|------|-------|------------|------------|----|
| DWORD_08083e70 | 0x08083e70 | 0x00001476 | ANCIENT_LAMP_CID | ancient_lamp_cid_08083e70 | NEW; card-stats.s:12365 |

**DREAMSPRITE_CID (0x0000148a) (NEW)**
card-stats.s card_0968: Dreamsprite, slot=0x148a, pw=08687195 (line 12599).
grep "0x0000148a" constants/ -> 0 hits.

| slot | addr | value | const_name | slot_label | C5 |
|------|------|-------|------------|------------|----|
| DWORD_08083e94 | 0x08083e94 | 0x0000148a | DREAMSPRITE_CID | dreamsprite_cid_08083e94 | NEW; card-stats.s:12599 |

**DNA_TRANSPLANT_CID (0x0000171f) -- reuse by VALUE for LP display param**
Used at DWORD_08083d2c: `set_lp_display_row_type15(..., r1=0x171f)`. Semantically different from DNA Transplant card CID filter but same numeric value; per reuse-by-VALUE rule, use existing constant.
EOL note: "LP display type15 row param (value matches DNA_TRANSPLANT_CID; same numeric token)".

| slot | addr | value | const_name | slot_label | C5 |
|------|------|-------|------------|------------|----|
| DWORD_08083d2c | 0x08083d2c | 0x0000171f | DNA_TRANSPLANT_CID | dna_transplant_cid_08083d2c | REUSE card_info.inc:395; diff semantic, same value |

**OTOHIME_CID (0x00001503) and TSUKUYOMI_CID (0x00001694)**

| slot | addr | value | const_name | slot_label | C5 |
|------|------|-------|------------|------------|----|
| DAT_080841b0 | 0x080841b0 | 0x00001503 | OTOHIME_CID | otohime_cid_080841b0 | REUSE card_info.inc:1084 |
| DAT_080841b4 | 0x080841b4 | 0x00001694 | TSUKUYOMI_CID | tsukuyomi_cid_080841b4 | REUSE card_info.inc:1182 |

**EQUIP_SLOT_SCORE_CAP (0x0000ffff)**

| slot | addr | value | const_name | slot_label | C5 |
|------|------|-------|------------|------------|----|
| DWORD_080840e0 | 0x080840e0 | 0x0000ffff | EQUIP_SLOT_SCORE_CAP | equip_slot_score_cap_080840e0 | REUSE oam_attr.inc:156 |

**BOOK_OF_LIFE_CID (0x00001536) (NEW)**
card-stats.s card_1115: Book of Life, slot=0x1536, pw=02204140 (line 14510).
grep "0x00001536" constants/ -> 0 hits. Used in BLK1 dispatch table CID.
NEW: BOOK_OF_LIFE_CID = 0x00001536. (Declared in card_info.inc as new entry.)

---

### REF_SLOTS (USER-label + DATA-ref; fn-ptr targets, RAM globals)

| slot | addr | target value | gas_label | slot_label | note |
|------|------|-------------|-----------|------------|------|
| DAT_080834fc | 0x080834fc | 0x08081de5 | set_equip_activation_state_by_mode+1 | set_equip_act_mode_fn_ptr_08083 4fc | fn-ptr THUMB+1; target = set_equip_activation_state_by_mode (0x08081de4+1); keep raw hex + EOL; NO mid-code label |
| DWORD_08083aec | 0x08083aec | 0x08083969 | check_effect_slot_zone_player_by_type+1 | check_zone_player_fn_ptr_08083aec | fn-ptr THUMB+1 to check_effect_slot_zone_player_by_type (confirmed asm line 21373); used by tick_equip_placement_bitmap_display_4state |
| DWORD_08083c18 | 0x08083c18 | 0x08083b55 | check_equip_slot_pair_blocked+1 | check_equip_pair_fn_ptr_08083c18 | fn-ptr THUMB+1 to check_equip_slot_pair_blocked (confirmed asm line 21644); used by tick_equip_activation_sprite_array_4state |
| DWORD_08083fcc | 0x08083fcc | 0x08081de5 | set_equip_activation_state_by_mode+1 | set_equip_act_mode_fn_ptr_08083fcc | same fn-ptr as DAT_080834fc |
| DWORD_08083dc4 | 0x08083dc4 | 0x080905e9 | set_equip_activation_state_by_mode_alt_fn_ptr | set_equip_act_alt_fn_ptr_08083dc4 | REUSE duel_field.inc:449 |
| DAT_080836b4 | 0x080836b4 | 0x080905e9 | set_equip_activation_state_by_mode_alt_fn_ptr | set_equip_act_alt_fn_ptr_080836b4 | REUSE duel_field.inc:449 |
| DWORD_08083f08 | 0x08083f08 | 0x080905e9 | set_equip_activation_state_by_mode_alt_fn_ptr | set_equip_act_alt_fn_ptr_08083f08 | REUSE duel_field.inc:449 |

Note: 0x08081de5 = set_equip_activation_state_by_mode (0x08081de4) + 1 (THUMB+1); grep constants/ for "0x08081de5" -> 0 hits; treat as inline fn-ptr raw value, keep as raw hex with EOL comment "THUMB+1 fn-ptr to set_equip_activation_state_by_mode".

---

### RENAME_SLOTS (PTR_/auto-name label rename + EOL)

| slot | addr | old label | new label | eol_ascii |
|------|------|-----------|-----------|-----------|
| PTR_gP1LifePoints_08083534 | 0x08083534 | PTR_gP1LifePoints_08083534 | gp1_life_points_ptr_08083534 | gP1LifePoints pointer (ELIGIB_SPRITE_CTRL_OFF read) |
| PTR_gP1LifePoints_080836b0 | 0x080836b0 | PTR_gP1LifePoints_080836b0 | gp1_life_points_ptr_080836b0 | gP1LifePoints pointer (LP pending activation check) |
| PTR_gP1LifePoints_080836e4 | 0x080836e4 | PTR_gP1LifePoints_080836e4 | gp1_life_points_ptr_080836e4 | gP1LifePoints pointer (ELIGIB_SPRITE_CTRL_OFF + ELIGIB_ANIM_STATE_OFF read) |
| DAT_0808424c | 0x0808424c | DAT_0808424c | book_of_life_eligible_dispatch_state0 | BLK2 start: Book of Life fn_eligible sub-stub state 0 |

**gP1LifePoints slots (EQ-class globals; all Ghidra auto-resolved as gP1LifePoints so no rename needed; the PTR_ variants above are the 3 needing rename):**

Additional EQ slot added per C13 fix (#2):

| slot | addr | value | const_name | slot_label | C5 |
|------|------|-------|------------|------------|----|
| DWORD_08083d24 | 0x08083d24 | 0x0201c4e0 | gP1LifePoints | gp1_life_points_ptr_08083d24 | REUSE ewram.inc |

The other gP1LifePoints references in Seg-9 are already named as `gP1LifePoints` via the symbol (slots at DWORD_080837c4, DWORD_08083808, DWORD_08083914, DWORD_08083958, DWORD_08083b24, DWORD_08083c68, DWORD_08083df4, DWORD_08083e98, DWORD_08083ec0, DWORD_08083ef4, DWORD_08083f3c, DWORD_08084008, DWORD_08084118, DWORD_080840d8, DWORD_08084118) -- these are auto-named DWORD_/DAT_ and point to gP1LifePoints; fixer does EQ via shared global ref same as other segments.

---

### FUNC_RENAME (none in Seg-9)

No function body / plate contradiction signals found. All 18 function names match their ARM code behavior.

---

### PLATE (R5; full ASCII rewrite or substring replacement)

9 lines with non-ASCII found in Seg-9 (grep `[^\x00-\x7F]` on asm lines 20820-22630). Affected functions:

**1. tick_equip_best_target_display_4state (0x08083560)**
Current plate (lines 20820-20829): contains CJK in plate comment -- no CJK (already verified below).
Actually the plate at line 20820-20829 is ALREADY ASCII (confirmed: the plate comment uses ASCII only "Equip best target..."). Keep as-is.

**2. tick_equip_lamp_dream_zone_activation_3state (0x08083704) -- CJK plate**
Current plate (line 21043): CJK Chinese text starting with "装备 Lamp/Dream 类区域激活三态..."
ASCII rewrite:
```
Equip Lamp/Dream zone activation 3-state machine. Takes card_entry_ptr(r0) and scene_ptr(r1).
Reads [gDuelPhaseFlags+0x4b0] current state. state==0: calls check_equip_zone_slot_activation_eligible;
if returns 2, sets r7=1 (eligible flag). Checks halfword[+2] bits[11:6] (mask 0xfc0)==0x90*8=0x480
and gEquipChainSlotRefs player_id match; if matched calls count_effect_node_zone_activations for r6.
If r7&&r6: writes [gDuelPhaseFlags+0x4b0]=10, returns 0. If r7&&!r6: strh 1 to [r4+0xa].
If !r7: strh 2 to [r4+0xa].
state==10: checks gDuelCardCtxBase[player*4+8] confirm_flag; if==1 writes [gP1LifePoints+LP_ACTIVATION_PENDING_OFF]:=2 and ++step;
else invoke_card_display_op_0x31_sub1(0x109), ++step, return 0.
state==11: reads [gP1LifePoints+LP_ACTIVATION_PENDING_OFF], strh [r4+0xa]++, clears step, returns [r4+0xa] halfword.
Other states: delegates to tick_equip_display_with_fn_ptr_routing_3state ([r4+0xa]==1)
or tick_equip_lamp_dream_activation_3state ([r4+0xa]==2).
indeg=0: Sub-type A runtime fn-ptr dispatch.
```

**3. check_effect_slot_zone_player_by_type (0x08083968) -- CJK plate**
Current plate (line 21369): CJK text starting "装备 effect_slot 区域玩家双路校验谓词..."
ASCII rewrite:
```
Effect slot zone/player dual-path predicate. Called via fn-ptr from tick_equip_placement_bitmap_display_4state.
Takes effect_node_ptr(r0). Reads [r4+6] bits[4:3] as case index.
case 0: XOR player_id with r5 (compare). case 1: direct compare player_id with r5.
Returns 0 (no match) or 1 (match). r4/r5 are caller-frame registers: effect_node and compare value.
fn-ptr 0x08083969 referenced from tick_equip_activation_if_not_otohime literal pool at DWORD_08083aec.
Constants: ZONE_FIELD_BITS=bits[4:3] of [r4+6] (case index [0..1]).
indeg=0: runtime fn-ptr call from tick_equip_placement_bitmap_display_4state.
```

**4. tick_equip_placement_bitmap_display_4state (0x080839b4) -- CJK plate**
Current plate (line 21417): CJK text starting "装备放置 bitmap 显示四状态机..."
ASCII rewrite:
```
Equip placement bitmap display 4-state machine. Takes effect_node_ptr(r0).
Reads [gDuelPhaseFlags+STATE_OFFSET] state. state 0: calls check_effect_activations_both_sides;
if [gDuelCardCtxBase+player_id*4+8]==1: calls find_best_slot_from_equip_bitmap_with_gate;
iterates slots 0..4 via set_equip_activation_state_by_mode_alt; on first match calls
enqueue_equip_slot_sprite_with_code_rotation forward then reverse; step+1 return 0.
state 1 (via check_effect_slot_zone_player_by_type fn-ptr): trigger_card_display_op31_if_not_active(op=0x94)
+set_equip_activation_state_by_mode; step+1.
state 2: check_activation_display_state_is_confirmed -> enqueue_equip_slot_sprite_with_code_rotation; step+1.
state>=3: step+1 return 1.
Constants: gDuelPhaseFlags=0x0201b290, STATE_OFFSET=0x4b0, SLOT_IDX_MAX=4,
FN_PTR_PREDICATE=check_effect_slot_zone_player_by_type(0x08083969).
indeg=0: Sub-type A runtime fn-ptr dispatch.
```

**5. tick_equip_activation_sprite_array_4state (0x08083ba0) -- CJK plate**
Current plate (line 21686): CJK text starting "装备激活四状态机, 含精灵压入操作..."
ASCII rewrite:
```
Equip activation sprite push 4-state machine. Takes effect_node_ptr(r0).
Reads [gDuelPhaseFlags+STATE_OFFSET] state. state 0: clears attr_bits (DUAL_LABEL_RENDER_STATE_CLEAR)
+ format_game_text_with_int_arg(slot=0x9b) + trigger_card_display_op31_if_not_active; step+1 return 0.
states 1 and 3 (shared path): check_activation_display_state_is_confirmed; if confirmed reads
[gP1LifePoints+ELIGIB_SPRITE_CTRL_OFF]/[+ELIGIB_ANIM_STATE_OFF]/[+LP_BANISHER_CTX_OFF] three fields,
calls enqueue_sprite_attr_row_0x29_with_flag2, then push_to_effect_slot_array; step+1.
If not confirmed: step-1. state 2: clear attr_bits + set_equip_activation_state_by_mode_alt; step+1.
Constants: gDuelPhaseFlags=0x0201b290, STATE_OFFSET=0x4b0, DUAL_LABEL_RENDER_STATE_CLEAR=0xfffc7fff,
FLAG_MASK_INV=~0x1d, FORMAT_TEXT_SLOT=0x9b, FN_PTR_CHECK=check_equip_slot_pair_blocked(0x08083b55).
indeg=0: Sub-type A runtime fn-ptr dispatch.
```

**6. tick_equip_lp_row_display_by_state (0x08083c98) -- CJK plate**
Current plate (line 21826): CJK text starting "装备 LP 行显示状态机步进函数..."
ASCII rewrite:
```
Equip LP row display state stepper. Driven by runtime function-pointer table.
Reads gDuelPhaseFlags+0x4b0: state<0 or >3 returns 1. state 0 and 1: calls
dispatch_equip_display_by_type_flag_and_node_activity; if 0 returns 0, else advances step+2.
state 2: read_effect_slot_side_and_type -> resolve_best_target_slot_for_equip ->
set_lp_row_type11_with_byte_flags(player_id, 1, ~bitmask).
state 3: reads [gP1LifePoints+LP_CARD_TRACK_NEXT_OFF] LP halfword, push_to_effect_slot_array,
set_lp_display_row_type15(player, halfword, DNA_TRANSPLANT_CID value).
Advances step by writing to gDuelPhaseFlags+0x4b0.
indeg=0: Sub-type A runtime fn-ptr dispatch.
```

**7. tick_equip_lamp_dream_activation_3state (0x08083e14) -- CJK plate**
Current plate (line 22026): CJK text starting "装备激活三状态机, 专用于 Ancient Lamp / Dreamsprite..."
ASCII rewrite:
```
Equip activation 3-state machine for Ancient Lamp/Dreamsprite cards. Takes effect_node_ptr(r0).
Reads [gDuelPhaseFlags+STATE_OFFSET] state. state 0: clears attr_bits; count_effect_node_zone_activations;
if >0: compares card_id against three values:
  - ANCIENT_LAMP_CID(0x1476) or ANCIENT_LAMP_CID-0x6c=0x140a(Shift) ->
    trigger_card_display_op31_if_not_active(op=0xf), write [gP1LifePoints+LP_ACTIVATION_PENDING_OFF]:=1.
  - DREAMSPRITE_CID(0x148a) -> reads [gDuelCardCtxBase+player*4]; if [ptr+8]==1:
    write [gP1LifePoints+LP_ACTIVATION_PENDING_OFF]:=1; else invoke_card_display_op_0x31_sub1(0xe2).
step+1 return 0.
state 1: reads [gP1LifePoints+LP_ACTIVATION_PENDING_OFF]; if 0 returns -1; else
set_equip_activation_state_by_mode (fn-ptr=set_equip_activation_state_by_mode_alt_fn_ptr); step+1 return 0.
state 2: check_activation_display_state_is_confirmed -> enqueue_equip_slot_sprite_with_code_rotation + step+1.
default: return 1.
Constants: DUAL_LABEL_RENDER_STATE_CLEAR=0xfffc7fff, ANCIENT_LAMP_CID=0x1476, DREAMSPRITE_CID=0x148a,
OP_TRIGGER=0xf, OP_ALT=0xe2, LP_ACTIVATION_PENDING_OFF=0x1d40(=0xea<<5),
FN_PTR_MODE=set_equip_activation_state_by_mode_alt_fn_ptr(0x080905e9).
indeg=0: Sub-type A runtime fn-ptr dispatch.
```

**8. dispatch_equip_display_if_confirm_state_two (0x0808416c) -- CJK plate**
Current plate (line 22517): CJK text starting "装备激活确认状态 2 门控分派函数..."
ASCII rewrite:
```
Equip activation confirm-state-2 gated dispatch. Reads card_slot[+0xc] halfword; if equals 2 calls
dispatch_equip_activation_display_by_confirm_state and passes through its return value; else returns 1.
Sibling of dispatch_equip_display_if_confirm_state_one (0x080833a8), difference: trigger value 1 vs 2.
indeg=0: Sub-type A runtime fn-ptr dispatch.
```

**9. dispatch_equip_display_by_type_code_or_card_id (0x08084180) -- CJK plate**
Current plate (line 22531): CJK text starting "装备激活显示双条件门控分派函数..."
ASCII rewrite:
```
Equip activation display dual-condition gated dispatch. Extracts card_slot[+2] bits[13:6] (mask 0x3fc0);
if equal to 0x8a<<5=0x1140 calls dispatch_equip_activation_display_by_confirm_state.
Else checks card_slot[+0] card_id: OTOHIME_CID(0x1503) or TSUKUYOMI_CID(0x1694) -- any match calls
dispatch_equip_activation_display_by_confirm_state and passes return value. No match: returns 1.
indeg=0: Sub-type A runtime fn-ptr dispatch.
Constants: OTOHIME_CID=0x1503, TSUKUYOMI_CID=0x1694, MASK_BITS13_6=0x3fc0, CODE_0x1140=0x8a<<5.
```

---

## carve 計劃 (R7) -- none

Both ROM_INCBIN blocks are THUMB code for R4 disasm, not data tables. No carve.

---

## disasm 計劃 (R4)

### BLK1: 0x08084210..0x08084234 (fn_eligible stub for Book of Life, CID=0x1536)

**Entry**: BLK1 GBA range = 0x0808420e..0x08084234 (0x26 B = 38 B).
- Bytes 0x8420e..0x8420f: 2B pad (.zero 2, skippable, part of prior function alignment).
- fn_eligible stub: 0x08084210..0x0808422b (approx; actual stub body).
- Literal pool: 2 DWORD slots at 0x0808422c and 0x08084230 (confirmed from ref-scan and function pattern).
  - 0x0808422c: contains raw word value (pool word for fn).
  - 0x08084230: contains raw word value.
- 0x08084232..0x08084233: possible .hword 0x4687 (MOV PC,r0) -- NOT createDWord; is 2-byte THUMB opcode.
- Note: do NOT createDWord on 0x4687 (MOV PC,r0) -- pool-vs-code trap.

**Ghidra procedure**:
1. clearListing 0x08084210 to 0x08084233 (whole stub range).
2. setTMode(0x08084210) to set THUMB mode.
3. DisassembleCommand(0x08084210) -- disassembles the stub.
4. If literal pool words auto-disassembled as code, force createDWord at 0x0808422c and 0x08084230.
5. After disasm: label the fn_eligible entry as `book_of_life_eligible_fn` (or per naming convention).

**Literal pool slots** (both in BLK1, ROM-confirmed):
- Slot at 0x0808422c: ROM value = 0x0201b290 = gDuelPhaseFlags. EQ REUSE ewram.inc. slot_label: duel_phase_flags_0808422c.
- Slot at 0x08084230: ROM value = 0x08084234 = raw JT base pointer (BLK2 dispatch table start). NOT a named global. Action: createDWord(0x08084230) + EOL "JT base: book_of_life_eligible state dispatch table".

### BLK2: 0x0808424c..0x08084318 (Book of Life fn_eligible dispatch sub-stubs)

**Entry**: BLK2 GBA range = 0x0808424c..0x08084318 (0xcc B = 204 B).
The 6 .word raw pointers at 0x08084234-0x08084247 (JT in asm lines 22618-22623) already decoded:
- state 0: 0x0808424c (= DAT_0808424c = BLK2 start)
- state 1: 0x0808429a
- state 2: 0x080842cc
- state 3: 0x080842ac
- state 4: 0x080842ba
- state 5 (default/fallback): 0x080842cc (same as state 2)

**Sub-stub disasm**: 6 entry points; overlap: states 2 and 5 share 0x080842cc.
**CRITICAL**: must use per-4B DisassembleCommand, NOT single range. Before: clearListing 0x0808424c..0x08084317, setTMode.

**Ghidra procedure**:
1. clearListing 0x0808424c to 0x08084317.
2. setTMode(0x0808424c).
3. Sequentially DisassembleCommand each unique entry:
   - 0x0808424c (state 0 / DAT_0808424c)
   - 0x0808429a (state 1)
   - 0x080842ac (state 3)
   - 0x080842ba (state 4)
   - 0x080842cc (states 2+5 shared)
4. Rename DAT_0808424c -> book_of_life_eligible_state0 (or similar).
5. After disasm: rename the 6 JT .word entries (lines 22618-22623) to reference the new labels.

**JT .word RENAME (post-disasm)**: The 6 .word literals at lines 22618-22623 should become:
```
.word book_of_life_eligible_state0
.word book_of_life_eligible_state1
.word book_of_life_eligible_state2
.word book_of_life_eligible_state3
.word book_of_life_eligible_state4
.word book_of_life_eligible_state2   @ states 2 and 5 share same stub
```

---

## 新增 constants / 全局 (file 10 Seg-9 新建)

必须先证明现有 inc 无可复用 (C5 grep=0 确认):

1. **BOOK_OF_LIFE_CID = 0x00001536** -- card_info.inc 新条目
   - grep "0x00001536" constants/ -> 0 hits [confirmed]
   - evidence: card-stats.s line 14510 (card_1115: Book of Life, pw=02204140, slot=0x1536)
   - scope: BLK1 dispatch table entry at 0x09e410a4; CID at entry[0]

2. **ANCIENT_LAMP_CID = 0x00001476** -- card_info.inc 新条目
   - grep "0x00001476" constants/ -> 0 hits [confirmed]
   - evidence: card-stats.s line 12365 (card_0950: Ancient Lamp, pw=54912977, slot=0x1476)
   - scope: tick_equip_lamp_dream_activation_3state comparison branch

3. **DREAMSPRITE_CID = 0x0000148a** -- card_info.inc 新条目
   - grep "0x0000148a" constants/ -> 0 hits [confirmed]
   - evidence: card-stats.s line 12599 (card_0968: Dreamsprite, pw=08687195, slot=0x148a)
   - scope: tick_equip_lamp_dream_activation_3state comparison branch

4. **GEARFRIED_IRON_KNIGHT_CID_SHIFTED = 0x9e180000** -- card_info.inc 新条目
   - grep "0x9e180000" constants/ -> 0 hits [confirmed]
   - formula: GEARFRIED_IRON_KNIGHT_CID(0x13c3) << 0x13 = 0x9e180000 (verified: 0x13c3 * 0x80000 = 0x9e180000)
   - pattern: same as DNA_TRANSPLANT_CID_SHIFTED (card_info.inc:396)
   - scope: tick_equip_best_target_display_4state sentinel comparison

5. ~~EQUIP_NODE_ATTR_CLEAR_MASK = 0xfffc7fff~~ -- DROPPED (C5 fix): REUSE DUAL_LABEL_RENDER_STATE_CLEAR (duel_field.inc:134) instead. grep "0xfffc7fff" -> duel_field.inc:134 hit confirmed by reviewer.

6. **INVOKE_OP31_SUB1_PARAM_109 = 0x00000109** -- duel_field.inc 新条目
   - grep "0x00000109" constants/ -> 0 hits [confirmed]
   - evidence: DWORD_080837e0 loaded as r0 arg to invoke_card_display_op_0x31_sub1 at 0x080837ca; distinct from TRIGGER_OP_PARAM_107(0x107)
   - scope: tick_equip_lamp_dream_zone_activation_3state state==10 non-confirm branch

7. **LP_ACTIVATION_PENDING_OFF = 0x00001d40** -- ewram.inc 新条目
   - grep "0x00001d40" constants/ -> 0 hits [confirmed]
   - formula: 0xea << 5 = 0x1d40; [gP1LifePoints+0x1d40] = LP activation pending flag
   - evidence: 9 functions in Seg-9 read/write this offset; value computed inline as `movs r1,#0xea; lsls r1,r1,#0x5`
   - scope: equip LP activation state machines (lamp/dream/zone sequences)

---

## §5.1 登記 (Rule 3) -- 0 引用块

None. Both BLK1 and BLK2 have confirmed references (BLK1 from THUMB+1 dispatch table; BLK2 from JT raw .word). No §5.1 registrations for Seg-9.

---

## 消費者証據 (R6) -- 關鍵槽語義的 file:line + 置信度

| 槽 / 常量 | 消費者 file:line | 操作 | 置信度 |
|-----------|----------------|------|--------|
| DAT_080834cc = 0xfffc7fff | asm/10:20741 | `ands r0,r1; str r0,[r4,#0x4]` clears bits of effect_node[+4] | high |
| DAT_080835c4 = 0x00000107 | asm/10:20885 | r1 arg to trigger_card_display_op31_if_not_active | high (REUSE) |
| DAT_0808366c = 0x9e180000 | asm/10:20966-20941 | `lsls r0,r0,#0x13; ldr r1,#0x9e180000; cmp r0,r1; beq skip` sentinel for Gearfried | high |
| DWORD_08083aec = 0x08083969 | asm/10:21585-21578 | r2 to set_equip_activation_state_by_mode__08096a4c = fn-ptr predicate | high (confirmed fn addr in asm) |
| DWORD_08083c18 = 0x08083b55 | asm/10:21759-21748 | r2 to set_equip_activation_state_by_mode_alt__08096ab0 = fn-ptr predicate | high |
| DWORD_08083d2c = 0x0000171f | asm/10:21903 | r1 arg to set_lp_display_row_type15 | high (value per plate); DNA_TRANSPLANT_CID same numeric value |
| DWORD_08083e70 = 0x00001476 | asm/10:22090-22080 | cmp r1,r0 to branch Ancient Lamp path | high (card-stats.s:12365) |
| DWORD_08083e94 = 0x0000148a | asm/10:22109-22094 | cmp r1,r0 to branch Dreamsprite path | high (card-stats.s:12599) |
| BLK1 THUMB+1 ref from 0x09e410b8 | dispatch table entry start 0x09e410a4: entry[0]=CID=0x1536 | fn_eligible ptr | high |

---

## 求助 (低置信度語義)

### RESOLVED: BLK1 literal pool exact values

BLK1 at 0x0808420e/0x26: both literal pool DWORD slots ROM-confirmed by reviewer:
- 0x0808422c = 0x0201b290 = gDuelPhaseFlags (REUSE ewram.inc; slot_label duel_phase_flags_0808422c)
- 0x08084230 = 0x08084234 = raw JT base pointer to book_of_life_eligible dispatch table (createDWord + EOL only; no new equate)

No longer BLOCKED.

---

## C5 dedup 証據彙整 (全槽 BY VALUE)

| value | constants/ grep result | action |
|-------|----------------------|--------|
| 0x0201b290 | ewram.inc: gDuelPhaseFlags | REUSE x26 slots |
| 0x0201e2a0 | ewram.inc: gDuelCardCtxBase | REUSE x7 slots |
| 0x0201bb90 | ewram.inc: gEquipChainSlotRefs | REUSE x2 slots |
| 0x00001d68 | ewram.inc:422 ELIGIB_SPRITE_CTRL_OFF | REUSE x7 slots |
| 0x00001d6c | ewram.inc:423 ELIGIB_ANIM_STATE_OFF | REUSE x2 slots |
| 0x00001da8 | ewram.inc:247 LP_CARD_TRACK_BASE_OFF | REUSE x1 slot |
| 0x00001daa | ewram.inc:248 LP_CARD_TRACK_NEXT_OFF | REUSE x1 slot |
| 0xfffc7fff | duel_field.inc:134 DUAL_LABEL_RENDER_STATE_CLEAR | REUSE x7 slots |
| 0x00000107 | duel_field.inc:312 TRIGGER_OP_PARAM_107 | REUSE x1 slot |
| 0x00000868 | ewram.inc PLAYER_BLOCK_STRIDE | REUSE x2 slots |
| 0x0201c510 | ewram.inc gDuelFieldSlots | REUSE x1 slot |
| 0x9e180000 | 0 hits | NEW GEARFRIED_IRON_KNIGHT_CID_SHIFTED |
| 0x00001415 | card_info.inc:1175 RED_MOON_BABY_CID | REUSE x1 slot |
| 0x00000109 | 0 hits | NEW INVOKE_OP31_SUB1_PARAM_109 |
| 0x00001476 | 0 hits | NEW ANCIENT_LAMP_CID |
| 0x0000148a | 0 hits | NEW DREAMSPRITE_CID |
| 0x0000171f | card_info.inc:395 DNA_TRANSPLANT_CID | REUSE x1 slot (diff semantic) |
| 0x00001503 | card_info.inc:1084 OTOHIME_CID | REUSE x1 slot |
| 0x00001694 | card_info.inc:1182 TSUKUYOMI_CID | REUSE x1 slot |
| 0x0000ffff | oam_attr.inc:156 EQUIP_SLOT_SCORE_CAP | REUSE x1 slot |
| 0x08083969 | 0 hits | REF_SLOT fn-ptr inline |
| 0x08083b55 | 0 hits | REF_SLOT fn-ptr inline |
| 0x08081de5 | 0 hits | REF_SLOT fn-ptr inline x2 |
| 0x080905e9 | duel_field.inc:449 set_equip_activation_state_by_mode_alt_fn_ptr | REUSE x3 slots |
| 0x00001d40 (computed inline as 0xea<<5) | 0 hits | NEW LP_ACTIVATION_PENDING_OFF |
| gP1LifePoints symbol | ewram.inc: gP1LifePoints | REUSE (all PTR_/DWORD_ gP1LifePoints slots) |

---

## C8 stale FUN_ scan

grep `FUN_[0-9a-f]\{8\}` on Seg-9 lines 20678-22630 of asm/10_equip_effect_dispatch.s -> **0 hits**.
All plates and inline comments in Seg-9 use current semantic names. Clean.

---

## C13 残留 100% 覆盖

Python count (precise, from segment lines 20678-22630):
```
DAT_  auto-names: 20
DWORD_ auto-names: 69
PTR_gP1LifePoints_ names: 3
Total: 92 slots
```

Coverage accounting (union of EQ + REF + RENAME, no double-count):

| category | count | slots |
|----------|-------|-------|
| EQ gDuelPhaseFlags x26 | 26 | DAT_08083470, DAT_0808353c, DAT_08083554, DAT_08083580, DWORD_08083728, DWORD_0808378c, DWORD_080837e4, DWORD_08083888, DWORD_08083940, DWORD_080839d8, DWORD_08083b2c, DWORD_08083b44, DWORD_08083bc0, DWORD_08083c1c, DWORD_08083c70, DWORD_08083c88, DWORD_08083cb4, DWORD_08083d58, DWORD_08083e30, DWORD_08083edc, DWORD_08083f6c, DWORD_08083fd0, DWORD_08084010, DWORD_08084028, DWORD_0808405c, DWORD_08084140 |
| EQ gDuelCardCtxBase x7 | 7 | DAT_080834d0, DAT_08083660, DWORD_080837c0, DWORD_08083910, DWORD_08083a40, DWORD_08083d94, DWORD_08083ebc |
| EQ gEquipChainSlotRefs x2 | 2 | DWORD_08083788, DWORD_08083d90 |
| EQ ELIGIB_SPRITE_CTRL_OFF x7 | 7 | DAT_08083538, DAT_080836e8, DWORD_08083b28, DWORD_08083c6c, DWORD_08083df8, DWORD_0808400c, DWORD_08083f40 |
| EQ ELIGIB_ANIM_STATE_OFF x2 | 2 | DAT_080836ec, DWORD_08083dfc |
| EQ LP_CARD_TRACK_BASE_OFF x1 | 1 | DWORD_0808411c |
| EQ LP_CARD_TRACK_NEXT_OFF x1 | 1 | DWORD_08083d28 |
| EQ DUAL_LABEL_RENDER_STATE_CLEAR x7 | 7 | DAT_080834cc, DAT_080835c0, DWORD_08083908, DWORD_08083a3c, DWORD_08083c14, DWORD_08083e6c, DWORD_08083fc8 |
| EQ TRIGGER_OP_PARAM_107 x1 | 1 | DAT_080835c4 |
| EQ PLAYER_BLOCK_STRIDE x2 | 2 | DAT_08083664, DWORD_080840dc |
| EQ gDuelFieldSlots x1 | 1 | DAT_08083668 |
| EQ GEARFRIED_IRON_KNIGHT_CID_SHIFTED x1 | 1 | DAT_0808366c |
| EQ RED_MOON_BABY_CID x1 | 1 | DWORD_0808390c |
| EQ INVOKE_OP31_SUB1_PARAM_109 x1 | 1 | DWORD_080837e0 |
| EQ ANCIENT_LAMP_CID x1 | 1 | DWORD_08083e70 |
| EQ DREAMSPRITE_CID x1 | 1 | DWORD_08083e94 |
| EQ DNA_TRANSPLANT_CID x1 | 1 | DWORD_08083d2c |
| EQ OTOHIME_CID x1 | 1 | DAT_080841b0 |
| EQ TSUKUYOMI_CID x1 | 1 | DAT_080841b4 |
| EQ EQUIP_SLOT_SCORE_CAP x1 | 1 | DWORD_080840e0 |
| EQ gP1LifePoints (DWORD_ slots) x16 | 16 | DWORD_080837c4, DWORD_08083808, DWORD_08083914, DWORD_08083958, DWORD_08083b24, DWORD_08083c68, DWORD_08083df4, DWORD_08083e98, DWORD_08083ec0, DWORD_08083ef4, DWORD_08083f3c, DWORD_08084008, DWORD_08084118, DWORD_080840d8, DWORD_0808411c(dup-excluded), DWORD_08083d24 |
| REF set_equip_act_mode_fn_ptr x2 | 2 | DAT_080834fc, DWORD_08083fcc |
| REF check_zone_player_fn_ptr x1 | 1 | DWORD_08083aec |
| REF check_equip_pair_fn_ptr x1 | 1 | DWORD_08083c18 |
| REF set_equip_act_alt_fn_ptr x3 | 3 | DWORD_08083dc4, DAT_080836b4, DWORD_08083f08 |
| RENAME PTR_gP1LifePoints_ x3 | 3 | PTR_gP1LifePoints_08083534, PTR_gP1LifePoints_080836b0, PTR_gP1LifePoints_080836e4 |
| RENAME BLK2 label x1 | 1 | DAT_0808424c |

**Sum check**: 26+7+2+7+2+1+1+7+1+2+1+1+1+1+1+1+1+1+1+1+16+2+1+1+3+3+1 = 93 [overcounts by 1: DWORD_0808411c is dup with LP_CARD_TRACK_BASE_OFF; net unique = 92]

Note: DWORD_0808411c appears in both LP_CARD_TRACK_BASE_OFF (EQ) and the gP1LifePoints list -- it belongs to LP_CARD_TRACK_BASE_OFF; the 16 listed gP1LifePoints DWORD_ slots include it as "(dup-excluded)" so net gP1LifePoints unique = 15. DWORD_08083d24 added per C13 fix (#2).

Actual corrected total:
- EQ slots: 26+7+2+7+2+1+1+7+1+2+1+1+1+1+1+1+1+1+1+1+15 = 80 (gP1LP net=15 after dup-exclude) + 1 (DWORD_08083d24, newly added) = 81
- REF slots: 2+1+1+3 = 7
- RENAME slots: 3+1 = 4
- **Total unique: 81+7+4 = 92** [matches python count of 92]

---

## Executor Report: F10-Seg-9 (revised after Mode-A fixes)

- 槽: EQ=81 REF=7 RENAME=4 FUNC_RENAME=0 PLATE=9
- carve=0 disasm=2 blocks (BLK1 0x8420e/0x26 + BLK2 0x8424c/0xcc) §5.1=0
- 新增 constants/全局: BOOK_OF_LIFE_CID=0x1536, ANCIENT_LAMP_CID=0x1476, DREAMSPRITE_CID=0x148a, GEARFRIED_IRON_KNIGHT_CID_SHIFTED=0x9e180000 (card_info.inc); INVOKE_OP31_SUB1_PARAM_109=0x109, LP_ACTIVATION_PENDING_OFF=0x1d40 (ewram.inc / duel_field.inc)
- REUSE (not NEW): DUAL_LABEL_RENDER_STATE_CLEAR (duel_field.inc:134) for all 7 0xfffc7fff slots; EQUIP_NODE_ATTR_CLEAR_MASK dropped
- BLK1 literal pool resolved: 0x0808422c=gDuelPhaseFlags(REUSE), 0x08084230=0x08084234 raw JT base (createDWord+EOL only)
- C13: DWORD_08083d24 (0x0201c4e0=gP1LifePoints) added; total coverage 92/92
- proposal: doc/dev/refine/F10-Seg-9.proposal.md
