# Refine Proposal: F11-Seg-3a  [0x08086cdc..0x080872e4)

## 段测绘

- 函数入口: x4
  - 0x08086cdc  dispatch_equip_zone_activation_state
  - 0x080871a8  populate_equip_zone_entries_substate_d
  - 0x0808724c  populate_equip_zone_entries_substate_e
  - 0x080872a4  write_equip_zone_entries_substate_d_range
- 残留自动名槽: 40 DAT_ + 6 PTR_gP1LifePoints_ = 46 unique defs
  - 40 DAT_ slots (EQ or REF, enumerated below)
  - 6 PTR_gP1LifePoints_ slots (RENAME to gp1lp_ptr_*)
- ROM_INCBIN / .byte 块: 0 (verified by python scan of L3831..L4611)
- CJK mojibake plate: L3829 (dispatch_equip_zone_activation_state plate, UTF-8 bytes 0xe8..);
  must be fully rewritten to ASCII.

Python C13 count: 46 unique slot defs. EQ=36, REF=4 (raw DAT_), RENAME=6 (PTR_).
All 46 accounted for in the three tables below = C13 satisfied.

---

## 数据块分类 (Rule 2/3)

No ROM_INCBIN or .byte blocks in range. No ref-scan required. Section N/A.

---

## 符号化计划

### EQ_SLOTS  (data-equate; all REUSE from existing constants)

ROM byte verification: all values read with python struct.unpack_from('<I', rom, addr-0x08000000)[0]
and match the asm .word literals. Confidence: high for all.

| slot | addr | value | const_name | source .inc | slot_label |
|------|------|-------|------------|-------------|------------|
| DAT_08086d14 | L3862 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | gduelphaseflag_86d14 |
| DAT_08086dc4 | L3921 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc | equip_phase_frame_86dc4 |
| DAT_08086dc8 | L3923 | 0x00001716 | EARTH_CHANT_CID | card_info.inc | earth_chant_cid_86dc8 |
| DAT_08086e50 | L3995 | 0x000019d9 | END_OF_WORLD_CID | card_info.inc | end_of_world_cid_86e50 |
| DAT_08086e54 | L3997 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc | gduelcardctx_86e54 |
| DAT_08086e5c | L4001 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | player_stride_86e5c |
| DAT_08086e60 | L4003 | 0x0201c600 | gP1FieldArrayCBase | ewram.inc | gp1fieldarrayc_86e60 |
| DAT_08086e64 | L4005 | 0x09e5a0c4 | gEquipEffectZoneTable | card_info.inc | gequipeffzone_86e64 |
| DAT_08086e80 | L4020 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | player_stride_86e80 |
| DAT_08086eac | L4043 | 0x09e5a0c4 | gEquipEffectZoneTable | card_info.inc | gequipeffzone_86eac |
| DAT_08086f24 | L4108 | 0x00001d70 | LP_BANISHER_CTX_OFF | ewram.inc | lp_banisher_ctx_86f24 |
| DAT_08086f28 | L4110 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | player_stride_86f28 |
| DAT_08086f2c | L4112 | 0x09e5a0c4 | gEquipEffectZoneTable | card_info.inc | gequipeffzone_86f2c |
| DAT_08086f70 | L4148 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc | equip_phase_frame_86f70 |
| DAT_08086f74 | L4150 | 0x09e5a0c4 | gEquipEffectZoneTable | card_info.inc | gequipeffzone_86f74 |
| DAT_08086f78 | L4152 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc | gduelcardctx_86f78 |
| DAT_08086f9c | L4170 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc | gduelcardctx_86f9c |
| DAT_0808704c | L4258 | 0x00001d6c | ELIGIB_ANIM_STATE_OFF | ewram.inc | eligib_anim_state_8704c |
| DAT_08087050 | L4260 | 0x00001d70 | LP_BANISHER_CTX_OFF | ewram.inc | lp_banisher_ctx_87050 |
| DAT_08087054 | L4262 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | player_stride_87054 |
| DAT_080870f4 | L4343 | 0x00001d68 | ELIGIB_SPRITE_CTRL_OFF | ewram.inc | eligib_sprite_ctrl_870f4 |
| DAT_080870f8 | L4345 | 0x00001d70 | LP_BANISHER_CTX_OFF | ewram.inc | lp_banisher_ctx_870f8 |
| DAT_080870fc | L4347 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | player_stride_870fc |
| DAT_08087100 | L4349 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | gduelphaseflag_87100 |
| DAT_08087104 | L4351 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc | equip_phase_frame_87104 |
| DAT_0808715c | L4395 | 0x09e5a0c4 | gEquipEffectZoneTable | card_info.inc | gequipeffzone_8715c |
| DAT_08087160 | L4397 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | player_stride_87160 |
| DAT_08087164 | L4399 | 0x0201c600 | gP1FieldArrayCBase | ewram.inc | gp1fieldarrayc_87164 |
| DAT_08087168 | L4401 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc | gduelcardctx_87168 |
| DAT_080871a4 | L4431 | 0x000019da | SAMSARA_CID | card_info.inc | samsara_cid_871a4 |
| DAT_0808723c | L4511 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | player_stride_8723c |
| DAT_08087240 | L4513 | 0x0201c740 | gP1SlotSetCodeArray | ewram.inc | gp1slotsetcode_87240 |
| DAT_08087244 | L4515 | 0x000005dc | CARD_FIELD3_THRESHOLD_1500 | card_info.inc | field3_thresh_87244 |
| DAT_08087248 | L4517 | 0x000012a1 | zone_query_hand_tag_12a1 | duel_field.inc | zone_hand_tag_87248 |
| DAT_080872a0 | L4567 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | player_stride_872a0 |
| DAT_080872e0 | L4605 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | player_stride_872e0 |

C5 value-grep evidence (REUSE; spot-checked):
- 0x0201b290: ewram.inc `.equ gDuelPhaseFlags, 0x0201b290` (REUSE confirmed)
- 0x000004a4: ewram.inc `.equ EQUIP_PHASE_FRAME_OFF, 0x000004a4` (REUSE confirmed)
- 0x00001716: card_info.inc `.equ EARTH_CHANT_CID, 0x00001716` (REUSE confirmed)
- 0x000019d9: card_info.inc `.equ END_OF_WORLD_CID, 0x000019d9` (REUSE confirmed)
- 0x0201e2a0: ewram.inc `.equ gDuelCardCtxBase, 0x0201e2a0` (REUSE confirmed)
- 0x00000868: ewram.inc `.equ PLAYER_BLOCK_STRIDE, 0x868` (REUSE confirmed)
- 0x0201c600: ewram.inc `.equ gP1FieldArrayCBase, 0x0201c600` (REUSE confirmed)
- 0x09e5a0c4: card_info.inc `.equ gEquipEffectZoneTable, 0x09e5a0c4` (REUSE confirmed)
- 0x00001d70: ewram.inc `.equ LP_BANISHER_CTX_OFF, 0x00001d70` (REUSE confirmed)
- 0x00001d6c: ewram.inc `.equ ELIGIB_ANIM_STATE_OFF, 0x00001d6c` (REUSE confirmed)
- 0x00001d68: ewram.inc `.equ ELIGIB_SPRITE_CTRL_OFF, 0x00001d68` (REUSE confirmed)
- 0x000019da: card_info.inc `.equ SAMSARA_CID, 0x000019da` (REUSE confirmed)
- 0x0201c740: ewram.inc `.equ gP1SlotSetCodeArray, 0x0201c740` (REUSE confirmed)
- 0x000005dc: card_info.inc `.equ CARD_FIELD3_THRESHOLD_1500, 0x000005dc` (REUSE confirmed)
- 0x000012a1: duel_field.inc `.equ zone_query_hand_tag_12a1, 0x000012a1` (REUSE confirmed)
  (NOT PARASITE_PARACIDE_CID; used as find_effect_node_in_zone r2 node-type tag, same
   semantic domain as duel_field.inc entry; asm/11 L4487 bl find_effect_node_in_zone
   w/ r1=0xb(zone type), r2=DAT_08087248. conf: high)

### REF_SLOTS (fn-ptr addresses and switchdata base)

| slot | addr | value | gas_label | slot_label |
|------|------|-------|-----------|------------|
| DAT_08086d18 | L3864 | 0x08086d1c | switchD_08086d10__switchdataD_08086d1c | switchdata_86d18 |
| DAT_08086e98 | L4032 | 0x080869a9 | scan_equip_zones_for_eligible_type11_target+1 | scan_equip_zone11_fnptr_86e98 |
| DAT_08086fa0 | L4172 | 0x08086a39 | eval_equip_zone_score_with_field_card+1 | eval_equip_score_fnptr_86fa0 |
| DAT_08086fb0 | L4181 | 0x08086a39 | eval_equip_zone_score_with_field_card+1 | eval_equip_score_fnptr_86fb0 |

Consumer evidence:
- DAT_08086d18 (0x08086d1c): switchdata base, dispatched via `ldr r0,[r0,#0]; bx r0` at
  0x08086d0e/0x08086d10. Targets all fall within dispatch_equip_zone_activation_state body.
  asm/11 L3856 (reference), L3864 (def). conf: high.
- DAT_08086e98 (0x080869a9 = scan_equip_zones_for_eligible_type11_target THUMB+1):
  asm/11 L4027-4028: `ldr r0, DAT_08086e98; bl init_zone_activation_display_state_p1_entry`
  => r0 (fn-ptr) passed as arg to init_zone_activation_display_state_p1_entry in caseD_80 path.
  0x080869a9 = 0x080869a8 + 1; 0x080869a8 is push-prologue of scan_equip_zones_for_eligible_type11_target
  (asm/11 L3367). conf: high.
- DAT_08086fa0/fb0 (0x08086a39 = eval_equip_zone_score_with_field_card THUMB+1):
  asm/11 L4167 (`ldr r2, DAT_08086fa0; bl select_equip_target_slot_by_card_id`): r2=fn-ptr arg.
  asm/11 L4175 (`ldr r0, DAT_08086fb0; bl init_zone_activation_display_state_p1_entry`): r0=fn-ptr arg.
  0x08086a39 = 0x08086a38 + 1; 0x08086a38 is push-prologue of eval_equip_zone_score_with_field_card
  (asm/11 L3451). conf: high.

### RENAME_SLOTS (PTR_gP1LifePoints_ -> gp1lp_ptr_<hex_addr>)

Pattern follows Seg-1/Seg-2 convention: lowercase hex of slot address, no 0x prefix.
All 6 slots hold `.word gP1LifePoints` (value 0x0201c4e0, confirmed in ROM).
EOL: `.@ gP1LifePoints` on the .word line.

| slot | slot_label | eol_ascii |
|------|------------|-----------|
| PTR_gP1LifePoints_08086e58 | gp1lp_ptr_86e58 | gP1LifePoints |
| PTR_gP1LifePoints_08086f20 | gp1lp_ptr_86f20 | gP1LifePoints |
| PTR_gP1LifePoints_08087048 | gp1lp_ptr_87048 | gP1LifePoints |
| PTR_gP1LifePoints_08087238 | gp1lp_ptr_87238 | gP1LifePoints |
| PTR_gP1LifePoints_0808729c | gp1lp_ptr_8729c | gP1LifePoints |
| PTR_gP1LifePoints_080872dc | gp1lp_ptr_872dc | gP1LifePoints |

### FUNC_RENAME

None. No function body vs. name contradiction detected for the 4 Seg-3a functions.

---

## PLATE plan (R5)

### 1. dispatch_equip_zone_activation_state (asm/11 L3829) -- CJK mojibake -> FULL ASCII REWRITE

Current: UTF-8 CJK bytes (L3829 raw=0xe8 0xa3 0x85 ...). Ghidra plate is corrupt mojibake.

Replacement (full ASCII, <500 chars after trimming):
```
Equip zone activation state dispatcher. Gate: [r7+0x4] bit2 set -> return 0. Else reads [gDuelPhaseFlags+0x4a0] state, subs 0x62 -> index [0..0x1e], dispatches via table at 0x08086d1c (0x1f entries). Notable: idx0=caseD_62(count_field_copies+enqueue_lp_sprite), idx2=caseD_64(find_zone_slot_allowed+setup_equip_oam), idx0x1a=caseD_7c(select_equip_target), idx0x1b=caseD_7d(init_zone_activation), idx0x1c=caseD_7e(invoke_card_display_op_sub13), idx0x1d=caseD_7f, idx0x1e=caseD_80, default=caseD_63.
```
Length: 497 chars. All ASCII. conf: high (directly read from function body + jump table).
Case index mapping: key=state_code-0x62; idx0x1a=case_0x7c, idx0x1b=case_0x7d, idx0x1c=case_0x7e, idx0x1d=case_0x7f, idx0x1e=case_0x80.
case_0x7e (idx0x1c): calls invoke_card_display_op_0x31_sub13 (NOT find_zone_slot_idx).
case_0x64 (idx2, target 0x808710c): find_zone_slot_idx_allowed_for_card + invoke_setup_equip_oam_with_attr2 (asm L4356-4381).

### 2. populate_equip_zone_entries_substate_d (asm/11 L4434-L4436) -- plate correction

Current plate mentions "gDuelCardPool=0x0201c740" which is incorrect.
0x0201c740 = gP1SlotSetCodeArray (ewram.inc); "gDuelCardPool" is not a defined constant.
Corrected substring: replace `gDuelCardPool=0x0201c740` with `gP1SlotSetCodeArray=0x0201c740`.
Also replace `gDuelZoneData (key=0x12a1)` with `zone_query_hand_tag_12a1=0x12a1`.
All ASCII. conf: high.

### 3. populate_equip_zone_entries_substate_e (asm/11 L4520-L4522) -- plate correction

Current plate mentions "gDuelCardPool_alt_base=gP1LifePoints+0x418 (0x83<<3)".
0x0201c8f8 = gP1HandSlotArray (ewram.inc `.equ gP1HandSlotArray, 0x0201c8f8`).
Corrected substring: replace `gDuelCardPool_alt_base=gP1LifePoints+0x418 (0x83<<3)` with
`gP1HandSlotArray=0x0201c8f8 (gP1LifePoints+0x418, 0x83<<3)`.
All ASCII. conf: high.

### 4. write_equip_zone_entry_by_substate (asm/11 L6286) -- stale FUN_ in plate

Line: `@ Write a player zone record ... Called in loops by FUN_080871a8 and other ...`
Replace `FUN_080871a8` -> `populate_equip_zone_entries_substate_d`.
R6 evidence: asm/11 L4493 `bl write_equip_zone_entry_by_substate @ 0808721a`, inside
populate_equip_zone_entries_substate_d body. conf: high.

### 5. init_zone_activation_display_state_p1_entry (asm/12 L5378) -- stale FUN_ in plate

Line: `Called from FUN_08086e90/FUN_08086fa6 (card display field spell activation path)`
- 0x08086e90 is a BL instruction address WITHIN dispatch_equip_zone_activation_state caseD_80
  (asm/11 L4028 `bl init_zone_activation_display_state_p1_entry @ 08086e90`), not a fn entry.
- 0x08086fa6 is a BL instruction address WITHIN dispatch_equip_zone_activation_state caseD_7d
  (asm/11 L4176 `bl init_zone_activation_display_state_p1_entry @ 08086fa6`), not a fn entry.
Replace `FUN_08086e90/FUN_08086fa6` -> `dispatch_equip_zone_activation_state (caseD_80/caseD_7d)`.
All ASCII. conf: high.

Note: `FUN_08097bec-FUN_08098020` stale references also in same asm/12 L5378 plate are outside
Seg-3a scope. Flag for Seg-3b/later pass.

---

## carve 计划 (R7)

None. No ROM_INCBIN in range.

---

## disasm 计划 (R4)

None. No undisassembled code blocks in range.

---

## 新增 constants / 全局

None. All 46 slots reuse existing constants. C5 value-grep confirmed 0 new equates needed.

---

## §5.1 登记 (Rule 3)

None. No zero-reference data blocks in range.

---

## 消费者证据 (R6) -- 关键槽语义

| slot | 消费者 file:line | 语义 | 置信度 |
|------|----------------|------|--------|
| DAT_08086dc8 = 0x1716 | asm/11 L3910-L3915: caseD_80 `ldr r0,DAT_08086dc8; cmp r2,r0; beq LAB_08086dd2` -- CID match gate | EARTH_CHANT_CID | high |
| DAT_08086e50 = 0x19d9 | asm/11 L3926-L3928: `ldr r0,DAT_08086e50; cmp r2,r0; bne LAB_08086e9c` -- CID match gate | END_OF_WORLD_CID | high |
| DAT_080871a4 = 0x19da | asm/11 L4404-L4406: caseD_62 `ldr r0,DAT_080871a4; bl count_field_copies_of_card` -- CID arg | SAMSARA_CID | high |
| DAT_08086e64/eac/f2c/f74/8715c = 0x09e5a0c4 | asm/11 L4006 gEquipEffectZoneTable ref already named in Seg-2 | gEquipEffectZoneTable | high |
| DAT_08087244 = 0x5dc | asm/11 L4474-L4476: `ldr r1,DAT_08087244; cmp r0,r1; bgt skip` after get_card_extended_stat_field3_raw | field3 ATK <=1500 gate | high |
| DAT_08087248 = 0x12a1 | asm/11 L4486-L4487: `ldr r2,DAT_08087248; bl find_effect_node_in_zone(r0=ctx, r1=0xb, r2=tag)` | zone_query_hand_tag_12a1 | high |
| DAT_08087240 = 0x0201c740 | asm/11 L4462-L4466: base for card_id read in populate_equip_zone_entries_substate_d loop | gP1SlotSetCodeArray | high |
| DAT_0808704c = 0x1d6c | asm/11 L4190: caseD_7c `ldr r2,DAT_0808704c; adds r0,r6,r2; ldr r1,[r0]; cmp r1,#0xb` | ELIGIB_ANIM_STATE_OFF | high |
| DAT_08086e98 = 0x080869a9 | asm/11 L4027-4028: r0 arg to init_zone_activation_display_state_p1_entry | scan_equip_zones THUMB fn-ptr | high |

---

## 求助

None. All slots have high-confidence semantic assignments from existing constants or direct consumer
evidence.
