# Refine Proposal: F06-Seg-6  [0x08057458..0x08058550)

## 段测绘

- 段 ASM 行范围: L9463..L11807 (asm/06_equip_eligibility_b.s)
- 函数入口 x22 (全部已命名; 含第 23 个未标记函数 check_equip_slot_active_for_player_and_group @ 0x57678 — 见 disasm 计划):

| addr       | name                                         |
|------------|----------------------------------------------|
| 0x08057458 | set_lp_row_type2_fixed_for_equip_player      |
| 0x08057470 | tick_equip_lp_display_seq_by_phase           |
| 0x08057538 | dispatch_equip_zone_sprite_by_type_flag      |
| 0x0805756c | enqueue_lp_display_row_type2_for_card_player |
| 0x08057588 | enqueue_equip_slot_sprite_by_player_at_3     |
| 0x0805759c | set_lp_row_type4_for_slot_player             |
| 0x080575b0 | tick_equip_lp_bar_zone14_display_seq         |
| 0x08057660 | apply_lp_delta_for_slot_player_mode0         |
| 0x08057678 | (unlabeled) -> check_equip_slot_active_for_player_and_group |
| 0x080576b0 | tick_equip_chain_sprite_and_spell_zone_seq   |
| 0x08057874 | tick_equip_slot_score_fill_display_seq       |
| 0x08057c28 | tick_equip_banisher_zone_display_step        |
| 0x08057cf4 | check_neo_daedalus_placement_eligible_negated |
| 0x08057ea8 | set_lp_row_type2_for_equip_tier_abc          |
| 0x08057ecc | tick_equip_sprite_effect_node_seq            |
| 0x08057f98 | tick_equip_activation_if_not_dd_assailant    |
| 0x08057fcc | enqueue_equip_zone_sprite_mode1              |
| 0x08057ff4 | tick_equip_lp_score_and_card_id_seq          |
| 0x080583bc | tick_equip_bitmap_and_lp_chain_sprite_seq    |
| 0x08058444 | check_neo_daedalus_slot_eligible_negated     |
| 0x0805845c | enqueue_sprite_type11_for_equip_slot         |
| 0x0805847c | enqueue_equip_slot_sprite_with_field_bit_update |
| 0x080584cc | tick_equip_zone_bitmap_banisher_lp_seq       |
| 0x08058550 | tick_equip_activation_neo_daedalus_gate (Seg-7 first fn; boundary) |

- 残留自动名槽: 120 个 (DAT_/DWORD_/PTR_gP1LifePoints_) — 见 EQ/REF/RENAME 清单
  - python `.word` 计数 = 124; 其中 28 个 .word gP1LifePoints 已正确命名 (仅需 slot_label RENAME)
  - 有效残留需处理 = 120 个自动名槽 (含 gP1LP 槽的槽 label 重命名)

- ROM_INCBIN 块:
  - block1: ROM_INCBIN 0x57d0a, 0x2a (42 B) @ L10770
  - block2: ROM_INCBIN 0x57d4c, 0x15c (348 B) @ L10779

- 段内 CJK mojibake plate (非 ASCII): L10933 + L11806 -> 须整段 ASCII 重写 x2

---

## 数据块分类 (Rule 2/3) — ref-scan 证据

### block1: ROM_INCBIN 0x57d0a, 0x2a

**结构**: 2 字节 zero-pad (0x57d0a..0x57d0b) + THUMB fn (0x57d0c..0x57d33: push{r4,r5,lr}...mov pc,r0)

**ref-scan**:
- 0x08057d0d (THUMB+1) raw count = 1 at 0x09e40e8c
- 0x09e40e8c 上下文: CID=0x000014e6 (Emergency Provisions) handler 表第 4 槽, 周围均为 THUMB fn-ptr
- 核周边 ROM: 0x09e40e7c=0x000014e6 (合法 CID), 0x09e40e80..0x09e40e88=3 个 THUMB fn-ptr, 0x09e40e8c=0x08057d0d 是第 4 fn-ptr
- 判定: **真引用 -> R4 disasm**

**fn 语义**: 5-state 派发器 — 读 [gDuelPhaseFlags+0x4ac], state<=4 -> ptr_table[state] (via mov pc,r0 indirect jump); state>4 -> LAB_08057ea0 (return stub). ptr_table @ 0x57d38 (5 entries, raw addresses). conf: high (decoded from half-words, pointer table verified).

### block2: ROM_INCBIN 0x57d4c, 0x15c

**结构**: 3 THUMB sub-fn + 1 return stub (全部被 ptr_table 引用, raw 地址):
- sub-fn A @ 0x57d4c (0xac B): state=0 handler (clears slot[+8], trigger display op 0x3a, calls check_equip_slot_eligible, set_lp_row_type2_with_nonzero_flag)
- sub-fn B @ 0x57df8 (0x48 B): state=2 handler (reads LP, strh slot[+8], set_lp_display_row_type8)
- sub-fn C @ 0x57e40 (0x60 B): state=1/4 handler (check_activation_display_state_is_confirmed, invoke LP row update)
- return stub @ 0x57ea0 (0x8 B): movs r0,#1; pop {r4,r5}; pop {r1}; bx r1

**ref-scan** (内部引用验证):
- 0x08057d4c raw count=1 at 0x08057d38 (ptr_table entry 0)
- 0x08057df8 raw count=1 at 0x08057d40 (ptr_table entry 2)
- 0x08057e40 raw count=2 at 0x08057d3c+0x57d48 (ptr_table entries 1+4)
- 0x08057ea0 raw count=1 at 0x08057d44 (ptr_table entry 3)

ptr_table at 0x57d38 referenced from block1 fn via ldr r1,[pc,#0x10] -> 0x57d34 -> ptr-to-table 0x57d38. Chain: block1 fn-ptr (Emergency Provisions handler) -> ptr_table -> block2 sub-fns. Interlocking references: all block2 sub-fns are reachable only via indirect jump from block1. 判定: **真引用 -> R4 disasm (block1 + block2 连锁)**.

| 块 | ref-scan (raw / THUMB+1) | 判定 | 理由 |
|----|--------------------------|------|------|
| 0x57d0a sz=0x2a | raw=0 thumb+1=1 @ 0x09e40e8c | R4 disasm | CID 0x14e6 handler fn-ptr; 0x09e40e84=CID 合法; true ref |
| 0x57d4c sz=0x15c | raw 4 hits (ptr_table内); thumb=0 | R4 disasm | 4 sub-fns all reached via block1 indirect jump; ptr_table owns all refs |

---

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate; 先标注复用 inc 或新建)

共 96 个数值常量槽，按值分组。格式: (slot_addr, value, const_name, slot_label, inc)

**gDuelPhaseFlags (0x0201b290) x17 -- 复用 ewram.inc**:
```
(0x08057488, gDuelPhaseFlags, tick_equip_lp_display_seq_duel_phase_base)
(0x08057504, gDuelPhaseFlags, tick_equip_lp_display_seq_phase_base_b)
(0x08057508, EQUIP_ACTIVATION_STEP_OFF, tick_equip_lp_display_seq_step_off_b)  <- 0x4ac
(0x080575cc, gDuelPhaseFlags, tick_equip_lp_bar_z14_phase_base)
(0x08057708, gDuelPhaseFlags, tick_equip_chain_phase_base_a)
(0x0805772c, gDuelPhaseFlags, tick_equip_chain_phase_base_b)
(0x080577e0, gDuelPhaseFlags, tick_equip_chain_phase_base_c)
(0x08057864, gDuelPhaseFlags, tick_equip_chain_phase_base_d)
(0x080578b4, gDuelPhaseFlags, tick_equip_slot_score_phase_base)
(0x080579f0, gDuelPhaseFlags, tick_equip_slot_score_phase_base_b)
(0x08057b64, gDuelPhaseFlags, tick_equip_slot_score_phase_base_c)
(0x08057b8c, gDuelPhaseFlags, tick_equip_slot_score_phase_base_d)
(0x08057c44, gDuelPhaseFlags, tick_equip_banisher_phase_base)
(0x08057f08, gDuelPhaseFlags, tick_equip_sprite_eff_phase_base)
(0x08058018, gDuelPhaseFlags, tick_equip_lp_score_phase_base)
(0x0805834c, gDuelPhaseFlags, tick_equip_lp_score_phase_base_b)
(0x080583d4, gDuelPhaseFlags, tick_equip_bitmap_chain_phase_base)
(0x080584e4, gDuelPhaseFlags, tick_equip_zone_bitmap_phase_base)
```
Note: 17 gDuelPhaseFlags + some EQUIP_ACTIVATION_STEP_OFF -- counted together below.

**EQUIP_ACTIVATION_STEP_OFF (0x000004ac) x17 -- 复用 duel_field.inc**:
```
(0x0805748c, EQUIP_ACTIVATION_STEP_OFF, tick_equip_lp_display_seq_step_off)
(0x080575d0, EQUIP_ACTIVATION_STEP_OFF, tick_equip_lp_bar_z14_step_off)
(0x0805770c, EQUIP_ACTIVATION_STEP_OFF, tick_equip_chain_step_off_a)
(0x08057730, EQUIP_ACTIVATION_STEP_OFF, tick_equip_chain_step_off_b)
(0x080577e4, EQUIP_ACTIVATION_STEP_OFF, tick_equip_chain_step_off_c)
(0x08057868, EQUIP_ACTIVATION_STEP_OFF, tick_equip_chain_step_off_d)
(0x080578b8, EQUIP_ACTIVATION_STEP_OFF, tick_equip_slot_score_step_off)
(0x080579f4, EQUIP_ACTIVATION_STEP_OFF, tick_equip_slot_score_step_off_b)
(0x08057b68, EQUIP_ACTIVATION_STEP_OFF, tick_equip_slot_score_step_off_c)
(0x08057b90, EQUIP_ACTIVATION_STEP_OFF, tick_equip_slot_score_step_off_d)
(0x08057c48, EQUIP_ACTIVATION_STEP_OFF, tick_equip_banisher_step_off)
(0x08057f0c, EQUIP_ACTIVATION_STEP_OFF, tick_equip_sprite_eff_step_off)
(0x0805801c, EQUIP_ACTIVATION_STEP_OFF, tick_equip_lp_score_step_off)
(0x08058350, EQUIP_ACTIVATION_STEP_OFF, tick_equip_lp_score_step_off_b)
(0x080583d8, EQUIP_ACTIVATION_STEP_OFF, tick_equip_bitmap_chain_step_off)
(0x080584e8, EQUIP_ACTIVATION_STEP_OFF, tick_equip_zone_bitmap_step_off)
```
(17th EQUIP_ACTIVATION_STEP_OFF = 0x08057508 above in gDuelPhaseFlags group)

**EQUIP_ACTIVATION_AUX_OFF (0x000004b4) x8 -- 新建 duel_field.inc**:
```
(0x080579f8, EQUIP_ACTIVATION_AUX_OFF, tick_equip_slot_score_aux_off)
(0x08057a50, EQUIP_ACTIVATION_AUX_OFF, tick_equip_slot_score_aux_off_b)
(0x08057a8c, EQUIP_ACTIVATION_AUX_OFF, tick_equip_slot_score_aux_off_c)
(0x08057acc, EQUIP_ACTIVATION_AUX_OFF, tick_equip_slot_score_aux_off_d)
(0x08057b04, EQUIP_ACTIVATION_AUX_OFF, tick_equip_slot_score_aux_off_e)
(0x08057bd8, EQUIP_ACTIVATION_AUX_OFF, tick_equip_slot_score_aux_off_f)
(0x08057bfc, EQUIP_ACTIVATION_AUX_OFF, tick_equip_slot_score_aux_off_g)
(0x08057c10, EQUIP_ACTIVATION_AUX_OFF, tick_equip_slot_score_aux_off_h)
```
Evidence: gDuelPhaseFlags+0x4b4 = secondary activation counter; distinct from EQUIP_ACTIVATION_STEP_OFF (0x4ac); seen in tick_equip_slot_score_fill_display_seq plate "AUX_OFFSET=0x4b4". conf: high.

**PLAYER_BLOCK_STRIDE (0x00000868) x13 -- 复用 ewram.inc**:
```
(0x080576a4, PLAYER_BLOCK_STRIDE, tick_equip_chain_player_stride)
(0x08057b5c, PLAYER_BLOCK_STRIDE, tick_equip_slot_score_player_stride)
(0x08057c80, PLAYER_BLOCK_STRIDE, tick_equip_banisher_player_stride)
(0x08057f04, PLAYER_BLOCK_STRIDE, tick_equip_sprite_eff_player_stride)
(0x080580b8, PLAYER_BLOCK_STRIDE, tick_equip_lp_score_player_stride_a)
(0x080580f4, PLAYER_BLOCK_STRIDE, tick_equip_lp_score_player_stride_b)
(0x08058120, PLAYER_BLOCK_STRIDE, tick_equip_lp_score_player_stride_c)
(0x0805814c, PLAYER_BLOCK_STRIDE, tick_equip_lp_score_player_stride_d)
(0x08058178, PLAYER_BLOCK_STRIDE, tick_equip_lp_score_player_stride_e)
(0x080581ec, PLAYER_BLOCK_STRIDE, tick_equip_lp_score_player_stride_f)
(0x08058434, PLAYER_BLOCK_STRIDE, tick_equip_bitmap_chain_player_stride)
(0x080584c4, PLAYER_BLOCK_STRIDE, enqueue_equip_slot_sprite_fd_player_stride)
(0x08058540, PLAYER_BLOCK_STRIDE, tick_equip_zone_bitmap_player_stride)
```

**gDuelFieldSlots (0x0201c510) x3 -- 复用 ewram.inc**:
```
(0x080576a8, gDuelFieldSlots, tick_equip_chain_slot_base)
(0x08057b60, gDuelFieldSlots, tick_equip_slot_score_slot_base)
(0x080584c8, gDuelFieldSlots, enqueue_equip_slot_sprite_fd_slot_base)
```

**gDuelCardCtxBase (0x0201e2a0) x4 -- 复用 ewram.inc**:
```
(0x080574d4, gDuelCardCtxBase, tick_equip_lp_display_seq_ctx_base)
(0x08057904, gDuelCardCtxBase, tick_equip_slot_score_ctx_base)
(0x08057988, gDuelCardCtxBase, tick_equip_slot_score_ctx_base_b)
(0x080581f0, gDuelCardCtxBase, tick_equip_lp_score_ctx_base)
```

**ELIGIB_SPRITE_CTRL_OFF (0x00001d68) x4 -- 复用 ewram.inc**:
```
(0x0805765c, ELIGIB_SPRITE_CTRL_OFF, tick_equip_lp_bar_z14_sprite_ctrl_off)
(0x080577bc, ELIGIB_SPRITE_CTRL_OFF, tick_equip_chain_sprite_ctrl_off)
(0x08057bd0, ELIGIB_SPRITE_CTRL_OFF, tick_equip_slot_score_sprite_ctrl_off)
(0x08057f80, ELIGIB_SPRITE_CTRL_OFF, tick_equip_sprite_eff_sprite_ctrl_off)
```

**ELIGIB_ANIM_STATE_OFF (0x00001d6c) x1 -- 复用 ewram.inc**:
```
(0x08057bd4, ELIGIB_ANIM_STATE_OFF, tick_equip_slot_score_anim_state_off)
```

**P1LP_BLOCK2_OFF_1CE8 (0x00001ce8) x1 -- 复用 ewram.inc**:
```
(0x08058284, P1LP_BLOCK2_OFF_1CE8, tick_equip_lp_score_lp_block2_off)
```

**FIELD_STATE_OFF (0x00001cf4) x1 -- 复用 duel_field.inc** (confirmed: asm/06 AUX_OFFSET_CF4):
```
(0x08058288, FIELD_STATE_OFF, tick_equip_lp_score_field_state_off)
```

**OAM_ATTR0_HIDDEN (0x0000ffff) x3 -- 复用 oam_attr.inc** (semantic: LP row sentinel / bitmask all-1s):
```
(0x08057584, OAM_ATTR0_HIDDEN, enqueue_lp_row_type2_lp_row_clear)
(0x08058408, OAM_ATTR0_HIDDEN, tick_equip_bitmap_chain_full_mask)
(0x08058514, OAM_ATTR0_HIDDEN, tick_equip_zone_bitmap_full_mask)
```
Note: C5 -- same value 0xffff has 3 distinct semantic uses (LP row sentinel, bit mask), all in different functions, reuse single existing constant (OAM_ATTR0_HIDDEN already defined, not fabricating new). slot_label distinguishes context.

**invoke_effect_node_handler_2arg+1 (0x080905e9) x2 -- REF fn-ptr**:
```
(0x080575fc, invoke_effect_node_handler_2arg+1, tick_equip_lp_bar_z14_mode_fn)
(0x08057f48, invoke_effect_node_handler_2arg+1, tick_equip_sprite_eff_mode_fn)
```
(Handled under REF_SLOTS below)

**DON_ZALOOG_CID (0x00001532) x2 -- 复用 card_info.inc**:
```
(0x0805804c, DON_ZALOOG_CID, tick_equip_lp_score_don_zaloog_cid_a)
(0x080581fc, DON_ZALOOG_CID, tick_equip_lp_score_don_zaloog_cid_b)
```

**lookup_equip_card_score_cid_1388 (0x00001388) x3 -- 复用 card_info.inc**:
```
(0x08058048, lookup_equip_card_score_cid_1388, tick_equip_lp_score_cid_1388_a)
(0x080581f8, lookup_equip_card_score_cid_1388, tick_equip_lp_score_cid_1388_b)
(0x080583a8, lookup_equip_card_score_cid_1388, tick_equip_bitmap_cid_1388)
```
Note: C5 strict -- 0x1388 in card-domain CID context. Existing card_info.inc has lookup_equip_card_score_cid_1388 (BST node). LP_COST_5000 same value but duel_field domain, not applicable here. Use card_info.inc constant. conf: high (all 3 slots in BST dispatch / score comparison context).

**DARK_SCORPION_GORG_THE_STRONG_CID (0x00001685) x2 -- 复用 card_info.inc**:
```
(0x08058064, DARK_SCORPION_GORG_THE_STRONG_CID, tick_equip_lp_score_gorg_cid_a)
(0x08058214, DARK_SCORPION_GORG_THE_STRONG_CID, tick_equip_lp_score_gorg_cid_b)
```

**DARK_SCORPION_MEANAE_CID (0x00001686) x2 -- 复用 card_info.inc**:
```
(0x08058074, DARK_SCORPION_MEANAE_CID, tick_equip_lp_score_meanae_cid_a)
(0x08058238, DARK_SCORPION_MEANAE_CID, tick_equip_lp_score_meanae_cid_b)
```

**CLIFF_THE_TRAP_REMOVER_CID (0x0000161e) x2 -- 新建 card_info.inc**:
```
(0x08058044, CLIFF_THE_TRAP_REMOVER_CID, tick_equip_lp_score_cliff_cid_a)
(0x080581f4, CLIFF_THE_TRAP_REMOVER_CID, tick_equip_lp_score_cliff_cid_b)
```
Evidence: data/card-stats.s L16681: card_1282 @ Cliff the Trap Remover slot=0x161E pw=06967870. conf: high.

**OTOHIME_CID (0x00001503) x1 -- 新建 card_info.inc**:
```
(0x08057fbc, OTOHIME_CID, tick_equip_activation_if_not_otohime_cid)
```
Evidence: data/card-stats.s L13925: card_1070 @ Otohime slot=0x1503 pw=39751093. conf: high.
FUNC_RENAME needed (see below): function plate says "D. D. Assailant" but CID 0x1503 = Otohime, not D.D. Assailant (D.D. Assailant = slot 0x172C, card_1503). Naming phase error confirmed.

**EQUIP_ZONE_SPRITE_ATTR_MODE1 (0x0000152a) x1 -- 新建 duel_field.inc**:
```
(0x08057ff0, EQUIP_ZONE_SPRITE_ATTR_MODE1, enqueue_equip_zone_sprite_mode1_attr)
```
Evidence: enqueue_equip_zone_sprite_mode1 plate: "SPRITE_ATTR=0x152a (equip zone sprite variant)". Sibling of EQUIP_ZONE_SPRITE_ATTR=0x0fb6 (mode=2). Note: card_info.inc has Swarm of Scarabs CID=0x152a but here usage is sprite attr param to enqueue_sprite_attr_with_mode -- different domain, not a CID. conf: high (plate explicitly identifies this as sprite attr constant, not card ID filter).

**EQUIP_ACT_SCORE_MODE_103 (0x00000103) x1 -- 复用 duel_field.inc**:
```
(0x08058348, EQUIP_ACT_SCORE_MODE_103, tick_equip_lp_score_mode_103)
```

---

### REF_SLOTS (USER-label + DATA-ref)

**gP1LifePoints refs x28 -- 已正确 .word gP1LifePoints; 仅 slot_label RENAME**:
(28 PTR_gP1LifePoints_* / DWORD_* slots — all holding gP1LifePoints; slot labels in RENAME_SLOTS below)

**fn-ptr REF slots x4**:
```
(0x080575fc, invoke_effect_node_handler_2arg+1, tick_equip_lp_bar_z14_mode_fn)   -- DWORD_080575fc
(0x08057f48, invoke_effect_node_handler_2arg+1, tick_equip_sprite_eff_mode_fn)   -- DWORD_08057f48
(0x08057778, check_equip_slot_active_for_player_and_group+1, tick_equip_chain_slot_active_fn)  -- DAT_08057778
(0x08057b88, check_equip_slot_active_for_player_and_group+1, tick_equip_slot_score_slot_active_fn) -- DAT_08057b88
```
ROM values verified: 0x080575fc=0x080905e9 (invoke_effect_node_handler_2arg at 0x080905e8+1); 0x08057778=0x08057679 (fn at 0x57678+1); 0x08057b88=0x08057679. conf: high.

**ptr table REF slots x5**:
```
(0x08057d34, 0x08057d38, dispatch_emergency_provisions_ptr_table_ref)  -- .word 0x08057d38
(0x08057d38, block2_sub_fn_A, ep_state_dispatch_table_0)  -- PTR_DAT_08057d38 -> block2 sub-fn A label
(0x08057d3c, block2_sub_fn_C, ep_state_dispatch_table_1)  -- .word 0x08057e40
(0x08057d40, block2_sub_fn_B, ep_state_dispatch_table_2)  -- .word 0x08057df8
(0x08057d44, ep_state_dispatch_stub, ep_state_dispatch_table_3)  -- .word 0x08057ea0
(0x08057d48, block2_sub_fn_C, ep_state_dispatch_table_4)  -- .word 0x08057e40 (dup)
```
Note: These 5 .word slots (0x57d38..0x57d48) are already explicit in asm as individual .word lines. They need labels for the sub-fn destinations post-disasm. After R4 disasm creates labels for block2 sub-fns, replace raw addresses with symbolic labels.

---

### RENAME_SLOTS (纯改名 + EOL)

28 gP1LP slots get slot_label renames:
```
(0x080574a8, DWORD_080574a8, tick_equip_lp_display_seq_gp1lp)
(0x080574d8, DWORD_080574d8, tick_equip_lp_display_seq_gp1lp_b)
(0x08057500, DWORD_08057500, tick_equip_lp_display_seq_gp1lp_c)
(0x08057534, DWORD_08057534, tick_equip_lp_display_seq_gp1lp_d)
(0x08057658, DWORD_08057658, tick_equip_lp_bar_z14_gp1lp)
(0x080577b8, PTR_gP1LifePoints_080577b8, tick_equip_chain_gp1lp_a)
(0x08057860, PTR_gP1LifePoints_08057860, tick_equip_chain_gp1lp_b)
(0x080578d4, PTR_gP1LifePoints_080578d4, tick_equip_slot_score_gp1lp_a)
(0x08057908, PTR_gP1LifePoints_08057908, tick_equip_slot_score_gp1lp_b)
(0x08057924, PTR_gP1LifePoints_08057924, tick_equip_slot_score_gp1lp_c)
(0x08057940, PTR_gP1LifePoints_08057940, tick_equip_slot_score_gp1lp_d)
(0x08057a40, PTR_gP1LifePoints_08057a40, tick_equip_slot_score_gp1lp_e)
(0x08057a90, PTR_gP1LifePoints_08057a90, tick_equip_slot_score_gp1lp_f)
(0x08057bcc, PTR_gP1LifePoints_08057bcc, tick_equip_slot_score_gp1lp_g)
(0x08057c7c, DWORD_08057c7c, tick_equip_banisher_gp1lp)
(0x08057f00, DWORD_08057f00, tick_equip_sprite_eff_gp1lp)
(0x080580b4, PTR_gP1LifePoints_080580b4, tick_equip_lp_score_gp1lp_a)
(0x080580f0, PTR_gP1LifePoints_080580f0, tick_equip_lp_score_gp1lp_b)
(0x0805811c, PTR_gP1LifePoints_0805811c, tick_equip_lp_score_gp1lp_c)
(0x08058148, PTR_gP1LifePoints_08058148, tick_equip_lp_score_gp1lp_d)
(0x08058174, PTR_gP1LifePoints_08058174, tick_equip_lp_score_gp1lp_e)
(0x080581e8, PTR_gP1LifePoints_080581e8, tick_equip_lp_score_gp1lp_f)
(0x080582b0, PTR_gP1LifePoints_080582b0, tick_equip_lp_score_gp1lp_g)
(0x080582dc, PTR_gP1LifePoints_080582dc, tick_equip_lp_score_gp1lp_h)
(0x080582f8, PTR_gP1LifePoints_080582f8, tick_equip_lp_score_gp1lp_i)
(0x08058378, PTR_gP1LifePoints_08058378, tick_equip_lp_score_gp1lp_j)
(0x08058430, PTR_gP1LifePoints_08058430, tick_equip_bitmap_chain_gp1lp)
(0x0805853c, DWORD_0805853c, tick_equip_zone_bitmap_gp1lp)
```

---

### FUNC_RENAME (误名订正)

| addr       | old_name                                   | new_name                               | indeg | 理由 |
|------------|--------------------------------------------|----------------------------------------|-------|------|
| 0x08057f98 | tick_equip_activation_if_not_dd_assailant  | tick_equip_activation_if_not_otohime   | 1     | CID 0x1503 = Otohime (card-stats.s L13925); naming phase error: confused card record #1503 (D.D. Assailant) with slot_id 0x1503 (Otohime). indeg=1 (only one bl ref in asm/06, asm/all.s is duplicate). conf: high. |

---

### PLATE (R5; 须整段 ASCII 重写)

**PLATE_SET P1** @ tick_equip_activation_if_not_dd_assailant (L10933: CJK mojibake + wrong name) -> tick_equip_activation_if_not_otohime:
```
Equip activation guard: filters out two card cases before invoking tick_equip_activation_state_machine.
Reads card_entry[+2].hword bits[13:6] (mask 0xff<<6=0x3fc0 via movs/lsls); if bits equal
0x8a<<5=0x1140 (type_code sentinel), skips and returns 1. Otherwise reads card_entry[+0].u16
card_id; if card_id == 0x1503 (OTOHIME_CID, Otohime, pw=39751093), also skips and returns 1.
Both exclusions bypass equip activation state machine. Only if neither condition met:
transparently calls tick_equip_activation_state_machine(r0=card_entry, r1=secondary_ptr) and
returns its value. indeg=0, Sub-type A (step-table dispatch). Exit: pop{r1}; bx r1.
```

**PLATE_SET P2** @ tick_equip_activation_neo_daedalus_gate (L11806: CJK mojibake):
```
Equip activation Neo Daedalus path conditional gate. Reads card_entry[+2].hword bits[11:2]
(mask 0xfc<<4=0xfc0 via movs 0xfc/lsls 0x4); if bits equal 0xf0<<2=0x3c0 (slot_type_code
sentinel), skips and returns 1. If not equal to 0x3c0, transparently passes r0/r1 to
tick_equip_activation_if_neo_daedalus_with_lp_row and returns its value. Sibling gate stub
of function at 0x08057430 (same family, opposite branch direction). indeg=0 fn-ptr driven.
Exit: pop{r1}; bx r1.
```

Note: L11830 (dispatch_equip_zone_sprite_by_slot_group) also has CJK plate text but that function is in Seg-7 (0x08058578 > 0x08058550). Out of scope for Seg-6.

---

## disasm 计划 (R4)

### block1 dispatch fn @ 0x08057d0c (in ROM_INCBIN 0x57d0a, 0x2a)

- 2 zero-pad bytes @ 0x57d0a (alignment)
- THUMB fn @ 0x57d0c..0x57d29: push{r4,r5,lr}; loads gDuelPhaseFlags+EQUIP_ACTIVATION_STEP_OFF; reads state; if state > 4 branches to 0x57ea0 (return stub); else ldr r1,[pc,#0x10] -> 0x57d34 -> .word 0x08057d38 (ptr-to-table); adds r0,r0,r1; ldr r0,[r0,#0]; mov pc,r0 (indirect jump via state index)
- Literal pool @ 0x57d2a..0x57d33: 2 zero + gDuelPhaseFlags (0x0201b290) + EQUIP_ACTIVATION_STEP_OFF (0x4ac)
- Function name: dispatch_emergency_provisions_equip_activation_state (conf: med -- CID 0x14e6 = Emergency Provisions, 5-state dispatch)
- Ghidra steps: clearListing(0x57d0a, 0x57d34) -> setTMode(0x57d0c) -> DisassembleCommand(0x57d0c) -> createFunction(0x57d0c) -> setName -> setPlateComment (ASCII)
- fn-ptr entry 0x08057d0d already exists in 0x09e40e8c (CID 0x14e6 Emergency Provisions handler table slot 4) -- no new CSV row needed (fn is new, add to naming-proposals.csv)

### unlabeled fn @ 0x08057678 (currently in apply_lp_delta_for_slot_player_mode0 dead-zone)

- THUMB fn @ 0x57678..0x576ab: ldrb r0,[r0,#2]; lsls/lsrs (player_id); cmp r3,r1; bne; cmp r2,#4; bgt; computes gDuelFieldSlots[player*PLAYER_BLOCK_STRIDE + slot*0x14]; ldr word; lsls #0x13; cmp; movs r0,#1/0; bx lr
- Literal pool: 0x576a2..0x576ab (0x00000868, 0x0201c510)
- Function name: check_equip_slot_active_for_player_and_group (conf: high -- decodes player_id from card_entry, checks gDuelFieldSlots bit, returns 1 if slot active)
- Ghidra steps: clearListing(0x57678, 0x576b0) -> setTMode(0x57678) -> DisassembleCommand(0x57678) -> createFunction(0x57678) -> setName -> setPlateComment (ASCII)
- THUMB fn-ptr 0x08057679 used in DAT_08057778 + DAT_08057b88 -> after disasm, these become REF slots pointing to check_equip_slot_active_for_player_and_group+1

### block2 sub-fns @ 0x08057d4c..0x08057ea7 (ROM_INCBIN 0x57d4c, 0x15c)

Four sub-functions reached via ptr_table indirect jump (raw addresses, not THUMB+1):
- sub-fn A @ 0x57d4c..0x57df7 (state=0): movs r0,#0; strh r0,[r4,#8]; ldrb; lsls/lsrs (player_id); movs r1,#0x3a; bl trigger_card_display_op31_if_not_active; ...set_lp_row_type2_with_nonzero_flag. Name: dispatch_ep_state0_lp_display (conf: med)
- sub-fn B @ 0x57df8..0x57e3f (state=2): adds r0,r4,#0; bl check_spell_zone_slot_placeable; ... strh. Name: dispatch_ep_state2_slot_display (conf: med)
- sub-fn C @ 0x57e40..0x57e9f (state=1/4): bl check_activation_display_state_is_confirmed; ... LP reads/updates. Name: dispatch_ep_state1_confirm_lp (conf: med)
- return stub @ 0x57ea0..0x57ea7: movs r0,#1; pop{r4,r5}; pop{r1}; bx r1. Name: dispatch_ep_state3_return (conf: high -- trivial stub)

Note: sub-fns are called via indirect jump (mov pc,r0), NOT bl. No push/pop{lr} in sub-fns -- they return through the original caller's pop{r1};bx r1 stack frame. Labels are data/jump-target labels, not function entry points in the traditional sense. Ghidra may not auto-detect as functions; create labels and disasm range.

Ghidra steps: clearListing(0x57d4c, 0x57ea8) -> setTMode(0x57d4c) -> DisassembleCommand per sub-fn starting addresses (4 separate commands: 0x57d4c, 0x57df8, 0x57e40, 0x57ea0) -> createLabel for each sub-fn start -> setPlateComment (ASCII, per sub-fn).

---

## carve 计划 (R7)

None. Both ROM_INCBIN blocks contain THUMB code (not structured data). Carve not applicable; use R4 disasm instead.

---

## 新增 constants / 全局

| name | value | file | grep-0-evidence |
|------|-------|------|-----------------|
| EQUIP_ACTIVATION_AUX_OFF | 0x000004b4 | duel_field.inc | grep "0x000004b4" constants/*.inc = 0 hits |
| CLIFF_THE_TRAP_REMOVER_CID | 0x0000161e | card_info.inc | grep "0x0000161e\|0x161e\|CLIFF" constants/*.inc = 0 hits; card-stats.s slot=0x161E card_1282 Cliff the Trap Remover |
| OTOHIME_CID | 0x00001503 | card_info.inc | grep "0x00001503\|0x1503\|OTOHIME" constants/*.inc = 0 hits; card-stats.s slot=0x1503 card_1070 Otohime |
| EQUIP_ZONE_SPRITE_ATTR_MODE1 | 0x0000152a | duel_field.inc | grep "0x0000152a\|0x152a\|MODE1.*sprite\|sprite.*mode1" constants/*.inc = 0 hits; distinct from EQUIP_ZONE_SPRITE_ATTR=0x0fb6 (mode=2) |

Rationale for EQUIP_ZONE_SPRITE_ATTR_MODE1:
- EQUIP_ZONE_SPRITE_ATTR (0x0fb6) exists for mode=2 sprite variant
- 0x152a is mode=1 sprite variant (sibling, different attr code, different fn)
- card_info.inc has Swarm of Scarabs CID=0x152a but usage in enqueue_equip_zone_sprite_mode1 is as sprite attr param to enqueue_sprite_attr_with_mode (r2 arg), not card_id filter
- C5 domain distinction: sprite attr domain vs CID domain (different base structures)
- conf: high (plate explicitly: "SPRITE_ATTR=0x152a (equip zone sprite variant)")

---

## §5.1 登记 (Rule 3) — 0 引用块

None in Seg-6. Both ROM_INCBIN blocks have valid references (block1: THUMB+1 ref from CID dispatch table; block2: raw refs from block1's ptr_table). No zero-reference orphan blocks in this segment.

---

## 消费者证据 (R6) — 关键槽语义的 file:line + 置信度

| 槽/常量 | 消费者 file:line | 置信度 |
|---------|-----------------|--------|
| EQUIP_ACTIVATION_AUX_OFF (0x4b4) | asm/06_equip_eligibility_b.s L10107 plate: "AUX_OFFSET=0x4b4" | high |
| OTOHIME_CID (0x1503) | data/card-stats.s L13925: card_1070 @ Otohime slot=0x1503 pw=39751093 | high |
| CLIFF_THE_TRAP_REMOVER_CID (0x161e) | data/card-stats.s L16681: card_1282 @ Cliff the Trap Remover slot=0x161E pw=06967870 | high |
| EQUIP_ZONE_SPRITE_ATTR_MODE1 (0x152a) | asm/06 L10969 plate: "SPRITE_ATTR=0x152a (equip zone sprite variant), MODE=1" | high |
| check_equip_slot_active_for_player_and_group fn | asm/06 L9972 DAT_08057778=0x08057679; L10541 DAT_08057b88=0x08057679; decoded THUMB code at 0x57678: player_id/slot_group predicate returning 0/1 | high |
| FUNC_RENAME tick_equip_activation_if_not_dd_assailant | data/card-stats.s L13925 (slot=0x1503=Otohime); L19554 card_1503=D.D.Assailant slot=0x172C -- naming phase conflated card record# with slot_id | high |
| block1 Emergency Provisions dispatch | 0x09e40e8c THUMB+1 ref; 0x09e40e7c CID=0x14e6 (ewram.inc Emergency Provisions card-stats.s L13613) | high |
| block2 sub-fns via ptr_table | 0x57d38 ptr_table: 5 entries; block1 fn loads ptr via ldr r1,[pc,#0x10]->0x57d34=ptr-to-table; indirect jump mov pc,r0 | high |

---

## 求助

None. All semantics resolved with file:line evidence.

---

## 自检结果

1. **EQ value ROM 核对** (selected critical slots):
   - 0x08057488 = 0x0201b290 (gDuelPhaseFlags) -- verified python: correct
   - 0x0805748c = 0x000004ac (EQUIP_ACTIVATION_STEP_OFF) -- verified: correct
   - 0x080574a8 = 0x0201c4e0 (gP1LifePoints) -- verified: correct (asm shows .word gP1LifePoints)
   - 0x08057fbc = 0x00001503 (OTOHIME_CID) -- verified: correct
   - 0x08058044 = 0x0000161e (CLIFF_THE_TRAP_REMOVER_CID) -- verified: correct
   - 0x08057ff0 = 0x0000152a (EQUIP_ZONE_SPRITE_ATTR_MODE1) -- verified: correct
   - 0x080579f8 = 0x000004b4 (EQUIP_ACTIVATION_AUX_OFF) -- verified: correct

2. **ptr_table entries** (raw addresses, not THUMB+1):
   - 0x57d38 = 0x08057d4c (block2 start = sub-fn A) -- raw, correct (not +1, indirect jump not bl)
   - 0x57d3c = 0x08057e40 (sub-fn C) -- raw, correct
   - 0x57d40 = 0x08057df8 (sub-fn B) -- raw, correct
   - 0x57d44 = 0x08057ea0 (return stub) -- raw, correct
   - 0x57d48 = 0x08057e40 (sub-fn C dup) -- raw, correct

3. **Plate/EOL ASCII check**: all proposed plate text above contains only printable ASCII (0x20-0x7e). No CJK, no unicode.

4. **§5.1 0-ref check**: N/A (no §5.1 blocks in Seg-6).

5. **Slot names**: all `^[a-z][a-z0-9_]+$`; disambiguation suffixes _a/_b/.._j/_b/_c used for multi-instance slots within same function.

6. **Non-ASCII in segment**: 2 CJK mojibake plate lines confirmed (L10933, L11806) -- both covered by PLATE_SET P1+P2 above.

7. **Stale FUN_ in segment**: 0 stale FUN_ patterns -- grep confirmed.
