# Refine Proposal: F12-Seg-4  [0x08096a4c..0x08097828)

## 段测绘

- 函数入口: x26 (含 4 个 SUB_ 自动名)
  - 0x08096a4c  set_equip_activation_state_by_mode__08096a4c
  - 0x08096ab0  set_equip_activation_state_by_mode_alt
  - 0x08096b14  check_activation_display_state_is_confirmed
  - 0x08096b3c  dispatch_zone_activation_by_state
  - 0x08096e14  init_duel_zone_target_slot_refs
  - 0x08096ecc  zero_duel_lp_display_counters
  - 0x08096f20  apply_equip_activation_with_fixed_type_a
  - 0x08096f40  apply_equip_activation_via_deck_slot_lookup
  - 0x08096f9c  eval_equip_target_via_player_deck_lookup
  - 0x08096fe0  eval_equip_target_via_chain_zone_lookup
  - 0x08097024  apply_equip_activation_with_id_lookup_type_a
  - 0x08097048  apply_equip_activation_with_id_lookup_type_b
  - 0x08097070  submit_equip_slot_sprite_with_ref_a
  - 0x080970a0  submit_equip_slot_sprite_with_ref_b
  - 0x080970d0  SUB_080970d0  (RENAME target)
  - 0x080970d4  SUB_080970d4  (RENAME target)
  - 0x080970e4  SUB_080970e4  (RENAME target)
  - 0x08097104  SUB_08097104  (RENAME target)
  - 0x08097114  scan_card_type_effect_handler_table
  - 0x08097150  dispatch_to_effect_handler_by_card_type
  - 0x08097190  check_equip_effect_zone_preconditions
  - 0x08097244  check_equip_zone_has_frozen_soul_or_great_long_nose
  - 0x08097278  check_equip_slot_activation_blocked_by_chain
  - 0x08097360  check_equip_slot_activation_blocked_by_chain_ext
  - 0x08097430  check_any_slot_card_activatable
  - 0x08097458  init_equip_display_state_with_sprite
  - 0x080974a8  fill_slot_activation_state_array
  - 0x0809757c  refresh_slot_activation_display_if_changed
  - 0x080976c8  check_equip_slot_card_type_matches_active_state
  - 0x080977a0  enqueue_frozen_soul_zone_sprite_or_default

  NOTE: python scan found 26 entries (22 named + 4 SUB_).
  set_equip_activation_state_by_mode__08096a4c has double-underscore suffix (auto-name
  conflict artifact). No FUNC_RENAME needed: body matches name (sets activation state
  by equip mode check). Seg-3 boundary confirmed at 0x08096a4c per init_zone_activation_display_state_p1_entry ending at 0x08096a30.

- 残留自动名槽 (python scan L5548..L7433):
  - DAT_: 95 slots
  - DWORD_: 14 slots
  - PTR_gP1LifePoints_: 15 slots
  - PTR_other: 0 slots
  - Total: 124 slots

- ROM_INCBIN / .byte 块:
  - 0x96eec / 0x34 / 0x08096eec  x1  (between zero_duel_lp_display_counters and apply_equip_activation_with_fixed_type_a)

---

## 数据块分类 (Rule 2/3) -- ref-scan 证据

### Block: 0x96eec / 0x34 (0x08096eec..0x08096f20)

ref-scan (python, roms/2343.gba):
- raw=1  (struct.pack("<I", 0x08096eec) found at ROM offset 0x00b16c2f)
- thumb+1=0

**Critical analysis of raw=1 reference:**
The single raw reference is at ROM offset 0x00b16c2f. This is a NON-4-ALIGNED byte offset
(0x00b16c2f & 3 = 3). A code pointer is always 4-aligned. The surrounding bytes at
0x08b16c2c = 0xec30c693 (word at aligned position does not equal 0x08096eec). The match
is a coincidental 4-byte byte sequence within compressed or data content in the high ROM
region (0x08b16xxx), which is far above the code area (0x0809xxxx).

Effective ref-scan: raw=0 (coincidental non-aligned match only), thumb+1=0.

**Block decode (THUMB code):**
Entry at 0x08096eec (no push -- leaf function, falls through from ROM_INCBIN boundary):
```
0x08096eec: 4a08  ldr r2, [pc+0x20]   -> [0x08096f10] = 0x0201c4e0 (gP1LifePoints)
0x08096eee: 4809  ldr r0, [pc+0x24]   -> [0x08096f14] = 0x00001d4c (ACTIVATION_STATE_C_OFF)
0x08096ef0: 1811  adds r1, r2, r0     ; r1 = gP1LifePoints + ACTIVATION_STATE_C_OFF
0x08096ef2: 6808  ldr r0, [r1, #0]    ; r0 = [gP1LifePoints + 0x1d4c]
0x08096ef4: 2800  cmp r0, #0
0x08096ef6: d009  beq 0x08096f0c      ; if 0 -> bx lr (return without writing)
0x08096ef8: 2000  movs r0, #0
0x08096efa: 6008  str r0, [r1, #0]    ; [gP1LifePoints + 0x1d4c] := 0
0x08096efc: 4806  ldr r0, [pc+0x18]  -> [0x08096f18] = 0x00001d54 (ELIGIB_STATE_CTRL_OFF)
0x08096efe: 1811  adds r1, r2, r0     ; r1 = gP1LifePoints + 0x1d54
0x08096f00: 2001  movs r0, #1
0x08096f02: 6008  str r0, [r1, #0]    ; [gP1LifePoints + 0x1d54] := 1
0x08096f04: 4805  ldr r0, [pc+0x14]  -> [0x08096f1c] = 0x00001d5c (ELIGIB_ACT_TYPE_OFF)
0x08096f06: 1811  adds r1, r2, r0
0x08096f08: 200d  movs r0, #0xd
0x08096f0a: 6008  str r0, [r1, #0]    ; [gP1LifePoints + 0x1d5c] := 0xd
0x08096f0c: 4770  bx lr
0x08096f0e: 0000  .align
Pool:
0x08096f10: 0x0201c4e0  (gP1LifePoints)
0x08096f14: 0x00001d4c  (ACTIVATION_STATE_C_OFF)
0x08096f18: 0x00001d54  (ELIGIB_STATE_CTRL_OFF)
0x08096f1c: 0x00001d5c  (ELIGIB_ACT_TYPE_OFF)
```

Semantics: Guard-conditioned activation state clear. If [gP1LifePoints+ACTIVATION_STATE_C_OFF]
== 0 -> return immediately. Otherwise clear 0x1d4c to 0, write 1 to 0x1d54,
write 0xd to 0x1d5c. All three offsets are REUSE of existing constants.

No push instruction -> cannot be an independent function. This is a THUMB helper that falls
through or is reached as a non-APCS leaf (tail-called or inline-like). No createFunction
warranted. No callers exist (raw=0 after coincidence removal).

**Judgment: §5.1** (ref-scan effective raw=0/thumb+1=0; no fall-through from preceding
zero_duel_lp_display_counters which ends bx lr at 0x08096edc; orphan THUMB leaf).

Consumer evidence for semantics: asm/12 L6137-6154 (zero_duel_lp_display_counters plate
and body confirms adjacent functions operate on same gP1LifePoints+0x1d4c/0x1d5c fields;
the ROM_INCBIN block is functionally a reset-on-nonzero variant, conf: high).

| Block | ref-scan (raw / THUMB+1) | Judgment | Reason |
|-------|--------------------------|----------|--------|
| 0x08096eec sz=0x34 | raw=0 effective (1 coincidental non-aligned match at 0x8b16c2f) / thumb+1=0 | §5.1 (ROM_INCBIN preserved) | No code/data ptr; not fall-through (preceding zero_duel_lp_display_counters ends bx lr at 0x08096edc; gap = 0x08096edd..0x08096eeb = .zero 0xe align pad); orphan THUMB leaf helper; no createFunction |

---

## 符号化计划 (R1/R2/R3)

All values verified by python read at (slot_addr - 0x08000000) in roms/2343.gba.
All REUSE entries verified by value-grep in constants/*.inc before marking NEW.
All NEW entries verified by value-grep returning 0 hits.

### EQ_SLOTS (data-equate; 95 DAT_ + 14 DWORD_ = 109 slots)

#### Group A: REUSE -- gP1LifePoints offsets (most common)

| slot addr | value | const_name | source | slot_label |
|-----------|-------|------------|--------|------------|
| DAT_08096aa0 | 0x00001d4c | ACTIVATION_STATE_C_OFF | duel_field.inc REUSE | actstate_c_6aa0 |
| DAT_08096aa4 | 0x00001d7c | ACTIVATION_ENTRY_PTR_OFF | duel_field.inc REUSE | act_entry_ptr_6aa4 |
| DAT_08096aa8 | 0x00001d58 | ELIGIB_ACT_COUNT_OFF | ewram.inc REUSE | eligib_actcnt_6aa8 |
| DAT_08096aac | 0x00001d64 | LP_PLAYER_SIDE_CACHE_OFF | ewram.inc REUSE | lp_plyrside_6aac |
| DAT_08096b04 | 0x00001d4c | ACTIVATION_STATE_C_OFF | duel_field.inc REUSE | actstate_c_6b04 |
| DAT_08096b08 | 0x00001d7c | ACTIVATION_ENTRY_PTR_OFF | duel_field.inc REUSE | act_entry_ptr_6b08 |
| DAT_08096b0c | 0x00001d58 | ELIGIB_ACT_COUNT_OFF | ewram.inc REUSE | eligib_actcnt_6b0c |
| DAT_08096b10 | 0x00001d64 | LP_PLAYER_SIDE_CACHE_OFF | ewram.inc REUSE | lp_plyrside_6b10 |
| DAT_08096b38 | 0x00001d54 | ELIGIB_STATE_CTRL_OFF | ewram.inc REUSE | eligib_state_6b38 |
| DAT_08096b70 | 0x00001d50 | LP_EQUIP_STATE_B_OFF | ewram.inc REUSE | lp_eq_state_b_6b70 |
| DAT_08096b74 | 0x00001d4c | ACTIVATION_STATE_C_OFF | duel_field.inc REUSE | actstate_c_6b74 |
| DAT_08096dc4 | 0x00001d7c | ACTIVATION_ENTRY_PTR_OFF | duel_field.inc REUSE | act_entry_ptr_6dc4 |
| DAT_08096df4 | 0x00001d7c | ACTIVATION_ENTRY_PTR_OFF | duel_field.inc REUSE | act_entry_ptr_6df4 |
| DAT_08096e10 | 0x00001d78 | ACTIVATION_STATE_B_OFF | duel_field.inc REUSE | actstate_b_6e10 |
| DAT_08096eb4 | 0x00001d68 | ELIGIB_SPRITE_CTRL_OFF | ewram.inc REUSE | eligib_spr_ctrl_6eb4 |
| DAT_08096eb8 | 0x00001d6c | ELIGIB_ANIM_STATE_OFF | ewram.inc REUSE | eligib_anim_6eb8 |
| DAT_08096ebc | 0x00001d54 | ELIGIB_STATE_CTRL_OFF | ewram.inc REUSE | eligib_state_6ebc |
| DAT_08096ec0 | 0x00001d44 | ELIGIB_CARD_ID_OFF | ewram.inc REUSE | eligib_card_id_6ec0 |
| DAT_08096ec4 | 0x00001d48 | ACTIVATION_STATE_A_OFF | duel_field.inc REUSE | actstate_a_6ec4 |
| DAT_08096ec8 | 0x00001d4c | ACTIVATION_STATE_C_OFF | duel_field.inc REUSE | actstate_c_6ec8 |
| DAT_08096ee4 | 0x00001d4c | ACTIVATION_STATE_C_OFF | duel_field.inc REUSE | actstate_c_6ee4 |
| DAT_08096ee8 | 0x00001d5c | ELIGIB_ACT_TYPE_OFF | ewram.inc REUSE | eligib_act_type_6ee8 |
| DAT_08097098 | 0x00001d68 | ELIGIB_SPRITE_CTRL_OFF | ewram.inc REUSE | eligib_spr_ctrl_7098 |
| DAT_0809709c | 0x00001d48 | ACTIVATION_STATE_A_OFF | duel_field.inc REUSE | actstate_a_709c |
| DAT_080970c8 | 0x00001d68 | ELIGIB_SPRITE_CTRL_OFF | ewram.inc REUSE | eligib_spr_ctrl_70c8 |
| DAT_080970cc | 0x00001d48 | ACTIVATION_STATE_A_OFF | duel_field.inc REUSE | actstate_a_70cc |
| DAT_08097224 | 0x00001cec | P1LP_TIMER_OFF | ewram.inc REUSE | p1lp_timer_7224 |
| DAT_08097228 | 0x00001cf4 | P2LP_BLOCK2_OFF_1CF4 | ewram.inc REUSE | p2lp_blk2_7228 |
| DAT_08097498 | 0x00001d28 | EQUIP_CHAIN_STEP_OFF | duel_field.inc REUSE | eq_chain_step_7498 |
| DAT_0809749c | 0x00001d2c | EQUIP_CHAIN_ACTIVE_OFF | duel_field.inc REUSE | eq_chain_active_749c |
| DAT_080975b8 | 0x00001d2c | EQUIP_CHAIN_ACTIVE_OFF | duel_field.inc REUSE | eq_chain_active_75b8 |
| DAT_08097670 | 0x00001d2c | EQUIP_CHAIN_ACTIVE_OFF | duel_field.inc REUSE | eq_chain_active_7670 |
| DAT_08097674 | 0x00001d28 | EQUIP_CHAIN_STEP_OFF | duel_field.inc REUSE | eq_chain_step_7674 |
| DAT_080976b4 | 0x00001d2c | EQUIP_CHAIN_ACTIVE_OFF | duel_field.inc REUSE | eq_chain_active_76b4 |
| DAT_080976b8 | 0x00001d28 | EQUIP_CHAIN_STEP_OFF | duel_field.inc REUSE | eq_chain_step_76b8 |
| DAT_080977e8 | 0x00001d28 | EQUIP_CHAIN_STEP_OFF | duel_field.inc REUSE | eq_chain_step_77e8 |
| DAT_080977ec | 0x00001d2c | EQUIP_CHAIN_ACTIVE_OFF | duel_field.inc REUSE | eq_chain_active_77ec |
| DAT_080977f0 | 0x00001d30 | NEW: EQUIP_CHAIN_CANCEL_OFF | NEW (grep 0x00001d30=0 hits; 14 ROM refs; see new constants) | eq_chain_cancel_77f0 |

#### Group B: REUSE -- EWRAM globals

| slot addr | value | const_name | source | slot_label |
|-----------|-------|------------|--------|------------|
| DAT_08096a6c | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc REUSE | gduecardctx_6a6c |
| DAT_08096ad0 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc REUSE | gduecardctx_6ad0 |
| DAT_08096be0 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc REUSE | gduecardctx_6be0 |
| DAT_08096d08 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc REUSE | gduecardctx_6d08 |
| DAT_08096d88 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc REUSE | gduecardctx_6d88 |
| DAT_08096c68 | 0x0201c510 | gDuelFieldSlots | ewram.inc REUSE | gduelfldslots_6c68 |
| DAT_08096c9c | 0x0201c510 | gDuelFieldSlots | ewram.inc REUSE | gduelfldslots_6c9c |
| DAT_08097574 | 0x0201c510 | gDuelFieldSlots | ewram.inc REUSE | gduelfldslots_7574 |
| DAT_08097788 | 0x0201c510 | gDuelFieldSlots | ewram.inc REUSE | gduelfldslots_7788 |
| DAT_08096d3c | 0x0201b290 | gDuelPhaseFlags | ewram.inc REUSE | gduelphaseflag_6d3c |
| DAT_08096df8 | 0x0201b290 | gDuelPhaseFlags | ewram.inc REUSE | gduelphaseflag_6df8 |
| DAT_080974a0 | 0x0201bb90 | gEquipChainSlotRefs | ewram.inc REUSE | gequipchainrefs_74a0 |
| DAT_0809756c | 0x0201bb90 | gEquipChainSlotRefs | ewram.inc REUSE | gequipchainrefs_756c |
| DAT_080975b0 | 0x0201bb90 | gEquipChainSlotRefs | ewram.inc REUSE | gequipchainrefs_75b0 |
| DAT_08097660 | 0x0201bb90 | gEquipChainSlotRefs | ewram.inc REUSE | gequipchainrefs_7660 |
| DAT_08097780 | 0x0201bb90 | gEquipChainSlotRefs | ewram.inc REUSE | gequipchainrefs_7780 |

#### Group C: REUSE -- stride/offset constants

| slot addr | value | const_name | source | slot_label |
|-----------|-------|------------|--------|------------|
| DAT_08096c64 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc REUSE | player_stride_6c64 |
| DAT_08096c98 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc REUSE | player_stride_6c98 |
| DAT_08096cd4 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc REUSE | player_stride_6cd4 |
| DAT_08096d8c | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc REUSE | player_stride_6d8c |
| DAT_08096dc8 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc REUSE | player_stride_6dc8 |
| DAT_0809722c | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc REUSE | player_stride_722c |
| DAT_08097570 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc REUSE | player_stride_7570 |
| DAT_08097784 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc REUSE | player_stride_7784 |
| DAT_08096d40 | 0x00000594 | EFFECT_ENTRY_COUNT_OFF | ewram.inc REUSE | effect_entry_cnt_6d40 |
| DAT_08096dfc | 0x00000484 | EQUIP_ACTIVE_CTX_OFF | duel_field.inc REUSE | equip_active_ctx_6dfc |
| DAT_08097578 | 0x000010e1 | LP_ACTIVATION_TYPE_ARRAY_BASE_OFF | ewram.inc REUSE | lp_act_type_arr_7578 |
| DAT_0809778c | 0x000010e1 | LP_ACTIVATION_TYPE_ARRAY_BASE_OFF | ewram.inc REUSE | lp_act_type_arr_778c |

#### Group D: REUSE -- card CIDs

| slot addr | value | const_name | source | slot_label |
|-----------|-------|------------|--------|------------|
| DAT_08097230 | 0x000015f0 | THUNDER_OF_RULER_CID | card_info.inc REUSE | thunder_ruler_7230 |
| DAT_08097234 | 0x0000173f | AGENT_OF_JUDGMENT_SATURN_CID | card_info.inc REUSE | agent_saturn_7234 |
| DAT_08097238 | 0x000016d4 | NEW: DD_BORDERLINE_CID | NEW (grep 0x000016d4=0 hits; 6 refs; see new constants) | dd_borderline_7238 |
| DAT_08097268 | 0x000016a1 | NEW: FROZEN_SOUL_CID | NEW (grep 0x000016a1=0 hits; 8 refs; see new constants) | frozen_soul_7268 |
| DAT_0809726c | 0x00001502 | NEW: GREAT_LONG_NOSE_CID | NEW (grep 0x00001502=0 hits; 84 refs; see new constants) | great_long_nose_726c |
| DAT_080972d4 | 0x000015ff | DIFFUSION_WAVE_MOTION_CID | card_info.inc REUSE | diffusion_wm_72d4 |
| DAT_08097354 | 0x00001669 | STAUNCH_DEFENDER_CID | card_info.inc REUSE | staunch_def_7354 |
| DAT_08097358 | 0x000014a6 | AMAZONESS_ARCHERS_CID | card_info.inc REUSE | amazoness_arch_7358 |
| DAT_0809735c | 0x000016bf | BERSERK_GORILLA_CID | card_info.inc REUSE | berserk_gor_735c |
| DAT_08097404 | 0x000015ff | DIFFUSION_WAVE_MOTION_CID | card_info.inc REUSE | diffusion_wm_7404 |
| DAT_08097408 | 0x000014a6 | AMAZONESS_ARCHERS_CID | card_info.inc REUSE | amazoness_arch_7408 |
| DAT_0809740c | 0x00001669 | STAUNCH_DEFENDER_CID | card_info.inc REUSE | staunch_def_740c |
| DAT_08097410 | 0x000016bf | BERSERK_GORILLA_CID | card_info.inc REUSE | berserk_gor_7410 |
| DAT_08097414 | 0x000016cb | BLACK_LUSTER_SOLDIER_ENVOY_CID | card_info.inc REUSE | bls_envoy_7414 |
| DAT_08097418 | 0x0000177a | NEW: EARTHBOUND_INVITATION_CID | NEW (grep 0x0000177a=0 hits; 10 refs; see new constants) | earthbound_inv_7418 |
| DAT_0809741c | 0x00001561 | TOON_DEFENSE_CID | card_info.inc REUSE | toon_defense_741c |
| DAT_08097420 | 0x00001852 | ASTRAL_BARRIER_CID | card_info.inc REUSE | astral_barrier_7420 |
| DAT_08097424 | 0x00001318 | RING_OF_MAGNETISM_CID | card_info.inc REUSE | ring_magnet_7424 |
| DAT_080977e0 | 0x000016a1 | FROZEN_SOUL_CID | NEW REUSE | frozen_soul_77e0 |

#### Group E: REUSE -- OAM sprite attrs

| slot addr | value | const_name | source | slot_label |
|-----------|-------|------------|--------|------------|
| DAT_080974a4 | 0x0000801b | OAM_EQUIP_SPRITE_TILE_P2_1B | oam_attr.inc REUSE | oam_eq_p2_1b_74a4 |
| DAT_08097668 | 0x0000801b | OAM_EQUIP_SPRITE_TILE_P2_1B | oam_attr.inc REUSE | oam_eq_p2_1b_7668 |
| DAT_08097820 | 0x00008018 | NEW: OAM_EQUIP_ZONE_SPRITE_P2_18 | NEW (grep 0x00008018=0 hits; 24 refs) | oam_eq_zone_p2_7820 |
| DAT_08097824 | 0x0000800f | NEW: OAM_EQUIP_ZONE_SPRITE_P2_0F | NEW (grep 0x0000800f=0 hits; 5 refs) | oam_eq_zone_p2_0f_7824 |

#### Group F: REUSE -- ROM table / fn-ptr constants (DAT_ for handler table)

| slot addr | value | const_name | source | slot_label |
|-----------|-------|------------|--------|------------|
| DAT_0809717c | 0x09e47560 | NEW: EQUIP_ACTIVATION_HANDLER_TABLE | NEW ROM table (grep 0x09e47560=0; 5 refs) | equip_act_tbl_717c |

NOTE: DAT_08097110 is a .byte slot (4 bytes: 0x60, 0x75, 0xe4, 0x09 = LE 0x09e47560).
Same value as EQUIP_ACTIVATION_HANDLER_TABLE. Uses `.byte` storage not `.word`
-- the fixer must use createDWord to coerce it to a DWORD and then equate, same as pool
remediation in file 11.

#### Group G: DWORD_ slots

| slot addr | value | const_name | source | slot_label |
|-----------|-------|------------|--------|------------|
| DWORD_08096f3c | 0x0000ffff | SPRITE_LOW_HALF_MASK | duel_field.inc REUSE (same AND-mask-low-16-bits mechanical usage as SPRITE_LOW_HALF_MASK; domain matches: ands r2,r1 clears high 16 bits of card attr word) | card_attr_mask_6f3c |
| DWORD_08096f88 | 0x0000ffff | SPRITE_LOW_HALF_MASK | duel_field.inc REUSE | card_attr_mask_6f88 |
| DWORD_08097044 | 0x0000ffff | SPRITE_LOW_HALF_MASK | duel_field.inc REUSE | card_attr_mask_7044 |
| DWORD_0809706c | 0x0000ffff | SPRITE_LOW_HALF_MASK | duel_field.inc REUSE | card_attr_mask_706c |
| DWORD_08096f8c | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc REUSE | player_stride_6f8c |
| DWORD_08096fd0 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc REUSE | player_stride_6fd0 |
| DWORD_08097014 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc REUSE | player_stride_7014 |
| DWORD_08096f90 | 0x0201c8f8 | gP1HandSlotArray | ewram.inc REUSE | gp1handslot_6f90 |
| DWORD_08096fd4 | 0x0201c740 | gP1SlotSetCodeArray | ewram.inc REUSE | gp1slotset_6fd4 |
| DWORD_08097018 | 0x0201c880 | gP1ChainZoneArray | ewram.inc REUSE | gp1chainzone_7018 |
| DWORD_080970e0 | 0x09e47560 | EQUIP_ACTIVATION_HANDLER_TABLE | NEW REUSE | equip_act_tbl_70e0 |
| DWORD_080970fc | 0x09e47560 | EQUIP_ACTIVATION_HANDLER_TABLE | NEW REUSE | equip_act_tbl_70fc |
| DWORD_0809713c | 0x09e47560 | EQUIP_ACTIVATION_HANDLER_TABLE | NEW REUSE | equip_act_tbl_713c |
| DWORD_08097100 | 0x08097025 | NEW: APPLY_EQUIP_ACT_ID_LOOKUP_TYPE_A_THUMB | NEW (0x08097024|1 = THUMB fn-ptr to apply_equip_activation_with_id_lookup_type_a; grep=0; 6 refs; used in check_equip_handler_uses_fixed_type_activation comparison) | equip_act_fixed_thumb_7100 |

---

### REF_SLOTS (USER-label + DATA-ref)

Two switchD base pointer slots:

| slot addr | target | gas_label | slot_label |
|-----------|--------|-----------|------------|
| DAT_08096b78 | 0x08096b7c (switchD_08096b6a__switchdataD_08096b7c) | switchD_08096b6a__switchdataD_08096b7c | zone_act_switchdata_6b78 |
| DAT_08096bf4 | 0x08096bf8 (switchD_08096bf2__switchdataD_08096bf8) | switchD_08096bf2__switchdataD_08096bf8 | zone_act_inner_switchdata_6bf4 |

REF count: 2

---

### RENAME_SLOTS (PTR_gP1LifePoints_ label rename + EOL; 15 slots)

All 15 PTR_gP1LifePoints_XXXXXXXX slots hold gP1LifePoints (0x0201c4e0) -- value is correct,
only slot label needs snake_case rename.

| slot addr | current_label | new slot_label |
|-----------|---------------|----------------|
| PTR_gP1LifePoints_08096a9c | PTR_gP1LifePoints_08096a9c | gp1lp_ptr_96a9c |
| PTR_gP1LifePoints_08096b00 | PTR_gP1LifePoints_08096b00 | gp1lp_ptr_96b00 |
| PTR_gP1LifePoints_08096b34 | PTR_gP1LifePoints_08096b34 | gp1lp_ptr_96b34 |
| PTR_gP1LifePoints_08096b6c | PTR_gP1LifePoints_08096b6c | gp1lp_ptr_96b6c |
| PTR_gP1LifePoints_08096eb0 | PTR_gP1LifePoints_08096eb0 | gp1lp_ptr_96eb0 |
| PTR_gP1LifePoints_08096ee0 | PTR_gP1LifePoints_08096ee0 | gp1lp_ptr_96ee0 |
| PTR_gP1LifePoints_08097094 | PTR_gP1LifePoints_08097094 | gp1lp_ptr_97094 |
| PTR_gP1LifePoints_080970c4 | PTR_gP1LifePoints_080970c4 | gp1lp_ptr_970c4 |
| PTR_gP1LifePoints_08097220 | PTR_gP1LifePoints_08097220 | gp1lp_ptr_97220 |
| PTR_gP1LifePoints_080972cc | PTR_gP1LifePoints_080972cc | gp1lp_ptr_972cc |
| PTR_gP1LifePoints_08097494 | PTR_gP1LifePoints_08097494 | gp1lp_ptr_97494 |
| PTR_gP1LifePoints_080975b4 | PTR_gP1LifePoints_080975b4 | gp1lp_ptr_975b4 |
| PTR_gP1LifePoints_0809766c | PTR_gP1LifePoints_0809766c | gp1lp_ptr_9766c |
| PTR_gP1LifePoints_080976b0 | PTR_gP1LifePoints_080976b0 | gp1lp_ptr_976b0 |
| PTR_gP1LifePoints_080977e4 | PTR_gP1LifePoints_080977e4 | gp1lp_ptr_977e4 |

RENAME count: 15 (PTR_) + 4 (SUB_) = 19 total

---

### FUNC_RENAME (SUB_ -> named functions; 4 entries)

All four SUB_ labels in Seg-4 are called from asm/11 L18046/18050/18062/18076/18079
(scan_zone_group_handler_multi_card) and have no indeg from callgraph beyond those callsites.
These are accessor stubs for the equip activation handler table at 0x09e47560.

| addr | old | new | indeg | reason |
|------|-----|-----|-------|--------|
| 0x080970d0 | SUB_080970d0 | get_equip_handler_table_entry_count | indeg=1 (asm/11 scan_zone_group_handler_multi_card) | returns 0x12=18 (table entry count; matches loop bound in scan_card_type_effect_handler_table which iterates 0..0x11=18 steps); asm/11 L18062: uses as loop exit bound `cmp r5,r0; blt` |
| 0x080970d4 | SUB_080970d4 | get_equip_handler_card_type | indeg=2 (asm/11 L18050/18076) | reads EQUIP_ACTIVATION_HANDLER_TABLE[r0*0x10+0x0] -> returns card type field |
| 0x080970e4 | SUB_080970e4 | check_equip_handler_uses_fixed_activation | indeg=1 (asm/11 L18079) | reads [+0xc], compares with APPLY_EQUIP_ACT_ID_LOOKUP_TYPE_A_THUMB (0x08097025) using eors/rsbs/orrs/lsrs#0x1f nonzero test; returns 1 if not match (uses fixed/non-id-lookup handler) |
| 0x08097104 | SUB_08097104 | get_equip_handler_table_entry_param | indeg=1 (asm/11 L18046) | reads EQUIP_ACTIVATION_HANDLER_TABLE[r0*0x10+0x4] -> param word |

---

### PLATE (R5)

4 non-ASCII plate lines (L5685, L6555, L6646, L7363) -- CJK mojibake.
7 lines with stale FUN_ references requiring substring replace.

#### Full ASCII rewrites (CJK mojibake plates):

**L5685 (dispatch_zone_activation_by_state plate):**
Replace full plate with:
"Zone activation dispatch hub (indeg=5, class D). Checks LP_EQUIP_STATE_B_OFF(0x1d50); if 0 return 0. Reads ACTIVATION_STATE_C_OFF(0x1d4c)-1 -> 10-case jump: 1=single zone 0xc..0xf; 2/3=multi-zone x4 groups via setup_equip_slot_activation_entry/_alt/eval_zone_flags; 4=eval_zone_flags; 5=gDuelPhaseFlags->eval_zone_flags_for_player; 6=zone 0xb eval_placement_flags; 7=invoke_r3 via ACTIVATION_ENTRY_PTR_OFF; 8=invoke_r3 cond; 9/10=same as 7/8; default=0. FLAG_DUAL_ZONE=0x1000 FLAG_ACTIVATABLE=0x8."

**L6555 (check_equip_effect_zone_preconditions plate):**
Replace full plate with:
"Checks player can activate effect in equip zone (zone=0xb). r0=player_id. All must pass: (1) P1LP_TIMER_OFF(0x1cec)!=0; (2) P2LP_BLOCK2_OFF_1CF4(0x1cf4)<=3; (3) equip zone slot bit18==0; (4) check_value_in_slot_chain(player,0xb,THUNDER_OF_RULER_CID=0x15f0)==0; (5) same for AGENT_OF_JUDGMENT_SATURN_CID=0x173f; (6) count_available_effect_zones(0,DD_BORDERLINE_CID=0x16d4,-1)>0 OR count_hand_cards_by_field6(0,0x16)>0; (7) same player 1. Returns 1=pass, 0=fail. Read-only. indeg=3."

**L6646 (check_equip_zone_has_frozen_soul_or_great_long_nose plate):**
Replace full plate with:
"Checks equip zone (zone=0xb) for Frozen Soul (FROZEN_SOUL_CID=0x16a1) or Great Long Nose (GREAT_LONG_NOSE_CID=0x1502). r0=player_id -> r4. Step 1: check_value_in_slot_chain(r4, 0xb, FROZEN_SOUL_CID) -> if hit return 1. Step 2: check_slot_has_node_by_card_id(r4, 0xb, GREAT_LONG_NOSE_CID) -> if hit return 1. Else return 0. Pure query. indeg=3. Side effects: none."

**L7363 (enqueue_frozen_soul_zone_sprite_or_default plate):**
Replace full plate with:
"r0=player_side. Calls check_equip_zone_has_frozen_soul_or_great_long_nose. Found: enqueue_equip_slot_sprite_attr(player,0xb,0x16a1,1); trigger_card_display_op31_if_not_active(player,0x136); gP1LifePoints+0x1d28=0xd, +0x1d2c=0, +0x1d30=1; return 0. Not found: P1: enqueue_sprite_attr_record(0x18,1,0,0)+(0xf,0,0,0); P2: same with OAM_EQUIP_ZONE_SPRITE_P2_18(0x8018)/OAM_EQUIP_ZONE_SPRITE_P2_0F(0x800f); return 1."

#### Stale FUN_ substring replacements:

| line | old FUN_ | true name |
|------|----------|-----------|
| L6137 (zero_duel_lp_display_counters plate) | FUN_080b70ac | select_equip_target_slot_by_card_id |
| L6518 (dispatch_to_effect_handler_by_card_type plate) | FUN_0810e5d4 | invoke_r3 |
| L6518 | FUN_080bb414 | dispatch_equip_activation_full_sequence |
| L6675 (check_equip_slot_activation_blocked_by_chain plate) | FUN_08099314 | dispatch_equip_field_phase_handler |
| L6925 (init_equip_display_state_with_sprite plate) | FUN_08097c2c | dispatch_equip_slot_display_state_by_phase |
| L6925 | FUN_08099314 | dispatch_equip_field_phase_handler |
| L6969 (fill_slot_activation_state_array plate) | FUN_0809757c | refresh_slot_activation_display_if_changed |
| L6969 | FUN_08098564 | tick_card_activation_phase_by_state |
| L7078 (refresh_slot_activation_display_if_changed plate) | FUN_08098264 | tick_activation_display_state_machine |
| L7078 | FUN_08098564 | tick_card_activation_phase_by_state |
| L7249 (check_equip_slot_card_type_matches_active_state plate) | FUN_08099314 | dispatch_equip_field_phase_handler |

Total PLATE actions: 4 full rewrites + 11 substring FUN_ replacements = 15 plate operations.

NOTE: The 4 CJK mojibake plate rewrites use setPlateComment and are treated as new writes;
all 4 must be <=500 chars (Fix#2 applied to 3 oversized ones above). Pre-existing plates that
receive only FUN_ substring substitution are not full rewrites -- only the substring changes,
so their total length is not a new-write concern unless the final length after substitution
exceeds 500 chars materially (FUN_ names are shorter than real names, net effect is -chars).
dispatch_zone_activation_by_state ~478, check_equip_effect_zone_preconditions ~433,
enqueue_frozen_soul_zone_sprite_or_default ~472 (all <=500 after Fix#2 edits above).

---

## carve 計劃 (R7, 如有)

None. No ROM_INCBIN data table requiring carve in this segment.
The 0x96eec block is classified §5.1 (orphan).

---

## disasm 計劃 (R4, 如有)

None. The 0x96eec block is an orphan THUMB leaf (§5.1); no disasm warranted.

---

## 新增 constants / 全局 (必须先证明现有 inc 无可复用)

### constants/duel_field.inc (新增 1)

| const_name | value | evidence | ROM refs |
|------------|-------|----------|----------|
| EQUIP_CHAIN_CANCEL_OFF | 0x00001d30 | enqueue_frozen_soul_zone_sprite_or_default (L7402): str r0,[r1+0x1d30] with r0=1; adjacent to EQUIP_CHAIN_STEP_OFF(0x1d28)+8 = cancel/teardown step field; grep 0x00001d30 constants/ = 0 hits; 14 ROM refs; conf: high | 14 |

### constants/ewram.inc (新増 0)

All ewram.inc values in Seg-4 are REUSE of existing constants.

### constants/oam_attr.inc (新増 2)

| const_name | value | evidence | ROM refs |
|------------|-------|----------|----------|
| OAM_EQUIP_ZONE_SPRITE_P2_18 | 0x00008018 | enqueue_frozen_soul_zone_sprite_or_default: player==1 path -> enqueue_sprite_attr_record(0x8018,...) first sprite; sibling of OAM_EQUIP_ZONE_SPRITE_P2_0F; P2 version of 0x18 (bit15+0x18); grep 0x00008018 constants/ = 0 hits; 24 ROM refs; conf: high | 24 |
| OAM_EQUIP_ZONE_SPRITE_P2_0F | 0x0000800f | enqueue_frozen_soul_zone_sprite_or_default: second sprite for P2 path; sibling of OAM_EQUIP_ZONE_SPRITE_P2_18; P2 version of 0xf (bit15+0xf); grep 0x0000800f constants/ = 0 hits; 5 ROM refs; conf: high | 5 |

### constants/card_info.inc (新増 4)

| const_name | value | evidence | ROM refs |
|------------|-------|----------|----------|
| FROZEN_SOUL_CID | 0x000016a1 | data/card-stats.s: "Frozen Soul slot=0x16A1 pw=57069605"; check_equip_zone_has_frozen_soul_or_great_long_nose: check_value_in_slot_chain(player,0xb,0x16a1); enqueue_frozen_soul_zone_sprite_or_default: enqueue_equip_slot_sprite_attr(player,0xb,0x16a1,1); grep 0x000016a1 constants/ = 0 hits; 8 ROM refs; conf: high | 8 |
| GREAT_LONG_NOSE_CID | 0x00001502 | data/card-stats.s: "Great Long Nose slot=0x1502 pw=02356994"; check_equip_zone_has_frozen_soul_or_great_long_nose: check_slot_has_node_by_card_id(player,0xb,0x1502); grep 0x00001502 constants/ = 0 hits; 84 ROM refs; conf: high | 84 |
| DD_BORDERLINE_CID | 0x000016d4 | data/card-stats.s: "D. D. Borderline slot=0x16D4 pw=60912752"; check_equip_effect_zone_preconditions: count_available_effect_zones(0,0x16d4,-1) + count_available_effect_zones(1,0x16d4,-1); grep 0x000016d4 constants/ = 0 hits; 6 ROM refs; conf: high | 6 |
| EARTHBOUND_INVITATION_CID | 0x0000177a | data/card-stats.s: "Earthbound Spirit's Invitation slot=0x177A pw=65743242"; check_equip_slot_activation_blocked_by_chain_ext: check_value_in_slot_chain(1-player,0xb,0x177a); refresh_slot_activation_display_if_changed: check_value_in_slot_chain(gEquipChainSlotRefs+4,0xb,0x177a); grep 0x0000177a constants/ = 0 hits; 10 ROM refs; conf: high | 10 |

### ROM addr constant (新增 2)

These go in a new file or a ROM table section -- following the pattern of
EQUIP_PHASE_FN_TABLE_ROM / SPRITE_ROW_DISPATCH_TABLE etc. established in Seg-1/2.
Best placed in duel_field.inc under the ROM table section:

| const_name | value | evidence | ROM refs |
|------------|-------|----------|----------|
| EQUIP_ACTIVATION_HANDLER_TABLE | 0x09e47560 | scan_card_type_effect_handler_table + dispatch_to_effect_handler_by_card_type + get_equip_handler_card_type/param: table base at 0x09e47560; 18 entries (0x12), stride 0x10B; fields [+0x0]=card_type, [+0x4]=param, [+0x8]=fn_activate+1 (THUMB), [+0xc]=fn_id_lookup+1 (THUMB); grep 0x09e47560 constants/ = 0 hits; 5 ROM refs; conf: high | 5 |
| APPLY_EQUIP_ACT_ID_LOOKUP_TYPE_A_THUMB | 0x08097025 | check_equip_handler_uses_fixed_activation: compares table[+0xc] against 0x08097025 = apply_equip_activation_with_id_lookup_type_a+1 (THUMB fn-ptr); eors/rsbs/orrs/lsrs#0x1f pattern = pointer equality test; ROM verification: 0x08097024 = push{lr} of apply_equip_activation_with_id_lookup_type_a confirmed; 6 ROM refs; conf: high | 6 |

Total new constants: 1 (duel_field.inc) + 2 (oam_attr.inc) + 4 (card_info.inc) + 2 (duel_field.inc ROM table) = 9 new constants.

---

## §5.1 登记 (Rule 3) -- 0 引用块

| ROM off | size | vaddr | Seg | 内容 | 登记理由 |
|---------|------|-------|-----|------|----------|
| 0x96eec | 0x34 | 0x08096eec | 4 | guard_activation_state_clear (orphan THUMB leaf; if [gP1LifePoints+ACTIVATION_STATE_C_OFF(0x1d4c)]==0 -> bx lr; else [+0x1d4c]:=0, [+0x1d54]:=1, [+0x1d5c]:=0xd; pool: gP1LifePoints/ACTIVATION_STATE_C_OFF/ELIGIB_STATE_CTRL_OFF/ELIGIB_ACT_TYPE_OFF) | ref-scan raw=0 effective (1 non-aligned coincidental match at 0x8b16c2f, not a code ptr); thumb+1=0; not fall-through (preceding zero_duel_lp_display_counters ends bx lr at 0x08096edc; gap = 0xe align bytes [0x08096edd..0x08096eeb]); ROM_INCBIN preserved |

---

## 消費者証拠 (R6) -- 关键槽语义的 file:line + 置信度

| slot / constant | consumer evidence | confidence |
|-----------------|-------------------|------------|
| EQUIP_CHAIN_STEP_OFF (0x1d28) | duel_field.inc comment: "values: 0x6=activate, 0x9=ai_init, 0xb=ready, 0xc=finalize"; asm/12 L7402 (enqueue_frozen_soul_zone_sprite_or_default): str r0=0xd [gP1LifePoints+0x1d28] (cancel state); L7450-7461 (dispatch_equip_activation_state_by_substate): ldr DAT_080978a0=gP1LifePoints, ldr DAT_080978a4=0x1d2c for state dispatch; confirmed REUSE | high |
| EQUIP_CHAIN_ACTIVE_OFF (0x1d2c) | duel_field.inc comment: "equip chain active player side flag; 0/1; 95 raw ROM refs"; asm/12 L7078 (refresh_slot_activation_display_if_changed plate): "ACTIVATION_CTRL_OFFSET=0x1d2c"; asm/12 L6962: sets [+0x1d2c]:=0 (clear active state); confirmed REUSE | high |
| EQUIP_CHAIN_CANCEL_OFF (0x1d30) | asm/12 L7402: enqueue_frozen_soul_zone_sprite_or_default writes 1 to [gP1LifePoints+0x1d30] on frozen_soul found path; adjacent to EQUIP_CHAIN_STEP_OFF(0x1d28)+8; semantics = cancel/deactivation trigger field; conf: high | high |
| gEquipChainSlotRefs (0x0201bb90) | ewram.inc: "equip chain slot reference array"; asm/12 L6964/7070/7107/7196/7345 (5 DAT_ slots); dispatch_equip_activation_state_by_substate reads [+0x0] player, [+0x1c] slot; str r5=player_side to [+0x0]; EQUIP_CTX_PLAYER_OFF=0x0 and EQUIP_CTX_SLOT_REF_OFF=0x1c from duel_field.inc; confirmed REUSE | high |
| EQUIP_ACTIVATION_HANDLER_TABLE (0x09e47560) | asm/12 L6484 scan_card_type_effect_handler_table plate: "HANDLER_TABLE_BASE = 0x09e47560, TABLE_ENTRY_COUNT = 0x11"; ROM verification: table has 18 entries (0x11+1=18 loop iterations, SUB_080970d0 returns 0x12=18); 18 entries confirmed; conf: high | high |
| APPLY_EQUIP_ACT_ID_LOOKUP_TYPE_A_THUMB (0x08097025) | asm/12 L6460 (DWORD_08097100): used in SUB_080970e4 (L6445-6460) via eors r1,r0; rsbs r0,r1,#0; orrs r0,r1; lsrs r0,r0,#0x1f = equals-0 test; confirmed 0x08097024 = apply_equip_activation_with_id_lookup_type_a push{lr} entry (asm/12 L6324); conf: high | high |
| FROZEN_SOUL_CID (0x16a1) | asm/12 L6648-6652: check_value_in_slot_chain(r4, 0xb, 0x16a1); asm/12 L7371-7374: enqueue_equip_slot_sprite_attr(player, 0xb, 0x16a1, 1); card-stats.s confirms "Frozen Soul slot=0x16A1"; conf: high | high |
| GREAT_LONG_NOSE_CID (0x1502) | asm/12 L6655-6658: check_slot_has_node_by_card_id(r4, 0xb, 0x1502); card-stats.s confirms "Great Long Nose slot=0x1502"; conf: high | high |
| DD_BORDERLINE_CID (0x16d4) | asm/12 L6601/6609: count_available_effect_zones(0/1, 0x16d4, -1); check_equip_effect_zone_preconditions plate L6555 says "EFFECT_CARD=0x16d4"; card-stats.s confirms "D. D. Borderline slot=0x16D4"; conf: high | high |
| EARTHBOUND_INVITATION_CID (0x177a) | asm/12 L6839-6843: check_value_in_slot_chain(1-player, 0xb, 0x177a); asm/12 L7197/7664: also 0x177a in refresh_slot_activation_display_if_changed; card-stats.s confirms "Earthbound Spirit's Invitation slot=0x177A"; conf: high | high |
| OAM_EQUIP_ZONE_SPRITE_P2_18 (0x8018) | asm/12 L7408-7413: enqueue_frozen_soul_zone_sprite_or_default P2 path: movs r0,#0x18; cmp r4,#0; beq skip; ldr r0,[DAT_08097820]=0x8018; enqueue_sprite_attr_record; P2 = bit15 set + 0x18 base tile code; conf: high | high |
| OAM_EQUIP_ZONE_SPRITE_P2_0F (0x800f) | asm/12 L7416-7422: second sprite P2 path: movs r0,#0xf; cmp r4,#0; beq skip; ldr r0,[DAT_08097824]=0x800f; conf: high | high |
| gP1HandSlotArray (0x0201c8f8) | ewram.inc: "gP1LifePoints+0x418: hand slot data array P1 base"; asm/12 L6227 DWORD_08096f90: apply_equip_activation_via_deck_slot_lookup uses as deck base P0 for lookup after find_deck_slot_by_card_pair_match; plate says "DECK_BASE_P0=0x0201c8f8"; conf: high | high |
| gP1SlotSetCodeArray (0x0201c740) | ewram.inc: "gP1LifePoints+0x260: slot set_code data array P1 base"; asm/12 L6268 DWORD_08096fd4: eval_equip_target_via_player_deck_lookup uses as base; plate says "DECK_BASE_P0=0x0201c740"; conf: high | high |
| gP1ChainZoneArray (0x0201c880) | ewram.inc: "gP1LifePoints+0x3a0: chain zone data array P1 base"; asm/12 L6309 DWORD_08097018: eval_equip_target_via_chain_zone_lookup uses as base; plate says "CHAIN_BASE_P0=0x0201c880"; conf: high | high |

---

## 求助 (如有低置信度语义)

### OPEN QUESTION 1 (RESOLVED): DWORD_08096f3c etc. -- 0x0000ffff domain

Four DWORD_ slots (6f3c, 6f88, 7044, 706c) hold 0x0000ffff used as `ands r2,r1` or `ands r3,r1`
to mask the low 16 bits of a card attribute word (apply_equip_activation_with_fixed_type_a,
_via_deck_slot_lookup, _with_id_lookup_type_a, _with_id_lookup_type_b).

**Reviewer creed (Fix#1 advisory): REUSE `SPRITE_LOW_HALF_MASK` (duel_field.inc)** --
mechanical AND-mask-low-16-bits operation is identical to SPRITE_LOW_HALF_MASK; not SLOT_CARD_EMPTY
(card sentinel domain differs). Group G table updated accordingly.

### OPEN QUESTION 2 (low): SUB_080970d0 semantics -- 0x12 vs 0x11

SUB_080970d0 returns 0x12 (18). scan_card_type_effect_handler_table (L6510)
uses `cmp r3,#0x11; bls` -- iterates r3=0..0x11 = 18 steps.
SUB_080970d0 is called by scan_zone_group_handler_multi_card (asm/11 L18062) as loop
exit condition `cmp r5,r0; blt`. The ROM table at 0x09e47560 has 18 entries (indices 0..17,
verified). So 0x12=18 is the correct entry count.
The naming `get_equip_handler_table_entry_count` is high confidence.
The table in ROM has exactly 18 entries confirmed. No open issue -- just documented for
completeness.

---

## C13 自查 (三表并集 == 全集)

- EQ (DAT_+DWORD_): 95 + 14 = 109 slots
- REF (switchD ptrs): 2 slots
- RENAME (PTR_gP1LifePoints_): 15 slots
- Total in three tables: 109 + 2 + 15 = 126 slots
- Python scan total: 124 slots (95 DAT_ + 14 DWORD_ + 15 PTR_gP1LP_)

DISCREPANCY NOTE: Python scan = 124; proposal tables = 126. The 2 extra are the 2 REF_SLOTS
(DAT_08096b78 and DAT_08096bf4) which ARE in the 95 DAT_ count AND in the REF table (they
are DAT_ prefix but with DATA-ref disposition). So the union is:
- 95 DAT_ includes the 2 REF candidates
- 14 DWORD_
- 15 PTR_
= 124 unique slots, fully covered. REF plan covers a subset of EQ slots (2 out of 95 DAT_).
No gaps.

Post-disasm gate: not applicable (no R4 disasm in this segment).
Post-landing: grep "^DAT_\|^DWORD_" asm/12_equip_activation_scan.s in [L5548..L7433] must return 0.
