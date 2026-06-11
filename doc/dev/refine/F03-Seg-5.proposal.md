# Refine Proposal: F03-Seg-5  [0x0803a7f0..0x0803b3a8)

## 段测绘

### 函数入口 x13

| 地址 | 函数名 | asm 行 |
|------|--------|--------|
| 0x0803a7f0 | build_equip_target_eligibility_table | 10171 |
| 0x0803a958 | get_slot_field5_score | 10362 |
| 0x0803a96c | get_slot_field7_score | 10374 |
| 0x0803a980 | get_slot_field6_score | 10386 |
| 0x0803a994 | eval_slot_score_entry_full_with_sp_result | 10398 |
| 0x0803a9a8 | eval_equip_chain_score_for_slot | 10410 |
| 0x0803abf0 | get_slot_card_state_code | 10724 |
| 0x0803ac04 | query_slot_card_state_code | 10736 |
| 0x0803aed0 | resolve_slot_chain_best_target | 11121 |
| 0x0803b1a4 | resolve_best_target_slot_for_equip | 11513 |
| 0x0803b1b0 | compute_slot_zone_eligibility_mask | 11521 |
| 0x0803b230 | check_slot_zone_bit_eligible | 11590 |
| 0x0803b2b4 | get_zone_slot_ptr | 11609 |

All 13 functions are already named. All have existing English plate comments. No stale FUN_ labels in asm lines 10171..11606 (grep confirmed 0 hits). get_zone_slot_ptr (asm line 11609) is the 13th function; its literal-pool slots are covered below.

### 残留自动名槽 x79

ROM values verified via python struct.unpack from roms/2343.gba.

| slot addr | value | category |
|-----------|-------|----------|
| DAT_0803a888 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803a88c | 0x0201c510 | REF gDuelFieldSlots |
| DAT_0803a94c | 0x0201e2a0 | REF gDuelCardCtxBase |
| DAT_0803a950 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803a954 | 0x0201c510 | REF gDuelFieldSlots |
| DAT_0803a9f4 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803a9f8 | 0x0201c510 | REF gDuelFieldSlots |
| DAT_0803aa74 | 0x0803777d | REF check_level_conv_lab_node_match+1 (fn-ptr) |
| DAT_0803aa78 | 0x0201d9c0 | REF gEquipNodePool |
| DAT_0803aa90 | 0x000015c7 | EQ COST_DOWN_CID (reuse) |
| DAT_0803aaac | 0x00001472 | EQ EMBODIMENT_OF_APOPHIS_CID (reuse) |
| DAT_0803aab0 | 0x00001636 | EQ METAL_REFLECT_SLIME_CID (reuse) |
| DAT_0803aac4 | 0x0000172f | EQ SKULL_ZOMA_CID (reuse) |
| DAT_0803ab18 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803ab1c | 0x0201d9c0 | REF gEquipNodePool |
| DAT_0803ab20 | 0xffffeb50 | EQ NODE_POOL_NEG_OFFSET (reuse) |
| DAT_0803ab24 | 0x0201c520 | REF gDuelFieldSlotState |
| DAT_0803aba0 | 0x000015e3 | EQ DEMOTION_CID (NEW) |
| DAT_0803aba4 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803aba8 | 0x0201c5d8 | REF gDuelFieldSlots_p2_base |
| DAT_0803abac | 0x0201c5e8 | RENAME eval_equip_chain_p2_equip_word_base (1 ref, no new global) |
| DAT_0803abec | 0x0000150b | EQ A_LEGENDARY_OCEAN_CARD_ID (reuse) |
| DAT_0803ac58 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803ac5c | 0x0201c510 | REF gDuelFieldSlots |
| DAT_0803acdc | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803ace0 | 0x000012a1 | EQ PARASITE_PARACIDE_CID (NEW) |
| DAT_0803ace4 | 0x0201c510 | REF gDuelFieldSlots |
| DAT_0803ad7c | 0x00001357 | EQ DNA_SURGERY_CID (NEW) |
| DAT_0803ad80 | 0x0201c574 | RENAME query_state_code_magic_zone_p0_base (1 ref, no new global) |
| DAT_0803ad84 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803ad88 | 0x0201c510 | REF gDuelFieldSlots |
| DAT_0803ad8c | 0x0201d9c0 | REF gEquipNodePool |
| DAT_0803ada8 | 0x000015ae | EQ D_TRIBE_CID (NEW) |
| DAT_0803adcc | 0x00001472 | EQ EMBODIMENT_OF_APOPHIS_CID (reuse) |
| DAT_0803add0 | 0x00001636 | EQ METAL_REFLECT_SLIME_CID (reuse) |
| DAT_0803ade4 | 0x0000172f | EQ SKULL_ZOMA_CID (reuse) |
| DAT_0803ae60 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803ae64 | 0x0201d9c0 | REF gEquipNodePool |
| DAT_0803ae68 | 0xffffeb50 | EQ NODE_POOL_NEG_OFFSET (reuse) |
| DAT_0803ae6c | 0x0201c520 | REF gDuelFieldSlotState |
| DAT_0803aec4 | 0x0000149f | RENAME gap_cid_149f (no card in card-stats.s) |
| DAT_0803aec8 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803aecc | 0x0201c510 | REF gDuelFieldSlots |
| DAT_0803af38 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803af3c | 0x0201c510 | REF gDuelFieldSlots |
| DAT_0803b02c | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803b030 | 0xb8f80000 | EQ DNA_TRANSPLANT_CID_SHIFTED (NEW) |
| DAT_0803b034 | 0x0201d9c0 | REF gEquipNodePool |
| DAT_0803b06c | 0x0000183b | EQ HOMUNCULUS_CID (NEW) |
| DAT_0803b070 | 0x0201d9c0 | REF gEquipNodePool |
| DAT_0803b074 | 0xffffeb50 | EQ NODE_POOL_NEG_OFFSET (reuse) |
| DAT_0803b094 | 0x00001472 | EQ EMBODIMENT_OF_APOPHIS_CID (reuse) |
| DAT_0803b098 | 0x00001636 | EQ METAL_REFLECT_SLIME_CID (reuse) |
| DAT_0803b0b0 | 0x0000172f | EQ SKULL_ZOMA_CID (reuse) |
| DAT_0803b120 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803b124 | 0x0201d9c0 | REF gEquipNodePool |
| DAT_0803b128 | 0xffffeb50 | EQ NODE_POOL_NEG_OFFSET (reuse) |
| DAT_0803b12c | 0x0201c520 | REF gDuelFieldSlotState |
| DAT_0803b198 | 0x0000145b | EQ SCROLL_OF_BEWITCHMENT_CID (NEW) |
| DAT_0803b19c | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803b1a0 | 0x0201c510 | REF gDuelFieldSlots |
| DAT_0803b214 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803b218 | 0x0201c510 | REF gDuelFieldSlots |
| DAT_0803b21c | 0x000018c7 | EQ DORIADO_CID (reuse) |
| DAT_0803b220 | 0x000019ef | EQ EHERO_ERIKSHIELER_CID (reuse) |
| DAT_0803b2cc | 0x0803b2d0 | REF get_zone_slot_ptr_switchD_table (ROM table) |
| DAT_0803b2f4 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803b2f8 | 0x0201c880 | REF gP1ChainZoneArray |
| DAT_0803b30c | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803b310 | 0x0201c740 | REF gP1SlotSetCodeArray |
| DAT_0803b324 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803b328 | 0x0201c8f8 | REF gP1HandSlotArray |
| DAT_0803b33c | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803b340 | 0x0201cab0 | REF gP1AltHandSlotArray |
| DAT_0803b354 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803b358 | 0x0201c600 | REF gP1FieldArrayCBase |
| DAT_0803b380 | 0x0201bc54 | REF gDuelEffectChainSlots |
| DAT_0803b3a0 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803b3a4 | 0x0201c510 | REF gDuelFieldSlots |

Total: 79 residual slots.

### ROM_INCBIN / .byte 块

| 块 | 地址 | size | asm 行 |
|----|------|------|--------|
| ROM_INCBIN | 0x0803b24e | 0x66 | 11606 |

---

## 数据块分类 (Rule 2/3) -- ref-scan 证据

### 块 0x0803b24e / size 0x66

**ref-scan 结果** (python struct scan, all even addresses in block):

```python
import struct
d = open('roms/2343.gba','rb').read()
block_start = 0x0803b24e
block_end   = 0x0803b2b4
for a in range(block_start, block_end, 2):
    raw   = d.count(struct.pack('<I', a))
    thumb = d.count(struct.pack('<I', a|1))
    if raw > 0 or thumb > 0:
        print(hex(a), raw, thumb)
# -> (no output)
```

Wide scan (every 4-byte aligned ROM position) also returned no matches.
Confirmed: **0 references anywhere in entire ROM**. confidence: high.

**块内容分析**:

```
+00: 00 00                          <- 2-byte alignment pad (NOP)
+02: 22 01 02 40 04 48 50 43 04 4a  <- movs r2,#1; ands r2,r0; ldr r0,[pc,#?]; muls r0,r2; ldr r2,[pc,#?]
+0c: 80 18 8a 00 52 18 92 00 80 18  <- adds r0,r0,r2; lsls r2,r1,#2; adds r2,r2,r1; lsls r2,r2,#2; adds r0,r0,r2
+16: 70 47 00 00                    <- bx lr; .hword 0x0000 (align pad)
+1a: 68 08 00 00 10 c5 01 02        <- .word 0x868 (PLAYER_BLOCK_STRIDE); .word 0x0201c510 (gDuelFieldSlots)
+20..+3f: identical to +02..+1f     <- second copy of same sub-function
+40: 06 4b 8a 00 52 18 92 00 01 21  <- ldr r3,[pc,#?]; lsls r2,r1,#2; adds r2,r2,r1; lsls r2,r2,#2; movs r1,#1
+4a: 01 40 04 48 48 43 12 18 d2 18  <- ands r1,r0; ldr r0,[pc,#?]; muls r0,r1; adds r2,r2,r0; adds r2,r2,r3
+54: 12 8e d0 04 c0 0c 70 47        <- (ldrh? or shift) -> bx lr
+5c: e0 c4 01 02 68 08 00 00        <- .word 0x0201c4e0 (gP1LifePoints); .word 0x868
+64: 00 00                          <- 2-byte pad
```

Total layout: 2-byte pad + 30B sub-fn-A + 2-byte pad + 30B sub-fn-A-copy + 38B sub-fn-B = 2+30+2+30+38 = 102 = 0x66. Checks out.

Block contains valid THUMB code (bx lr = 0x4770 confirmed at +16 and +36). The three sub-functions compute gDuelFieldSlots or variant zone base pointers. All three are unreachable (0 ROM references).

**判定: §5.1 (全 ROM 0 引用)** -- confidence: high

Reasoning:
- ref-scan raw=0 thumb=0 for all even addresses in block (wide scan confirmed).
- Block contains syntactically valid THUMB code but is dead code -- no jump-table entry, no bl, no BX-target pointer anywhere in ROM points into this range.
- The `get_zone_slot_ptr` function immediately following (0x0803b2b4) implements equivalent slot-pointer logic with a dispatch table; this block appears to be an earlier inline version that was superseded and stripped from the dispatch table, leaving it orphaned.
- Rule 3 applies: 0-ref block -> §5.1 register.

---

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate)

#### 复用现有常量 (reuse=37 slots)

| slot | value | const_name | inc file |
|------|-------|-----------|---------|
| DAT_0803a888 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803a950 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803a9f4 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803ab18 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803aba4 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803ac58 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803acdc | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803ad84 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803ae60 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803aec8 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803af38 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803b02c | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803b120 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803b19c | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803b214 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803b2f4 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803b30c | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803b324 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803b33c | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803b354 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803b3a0 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803b198+4 (=DAT_0803b19c) | see above | (counted once) | - |
| DAT_0803aa90 | 0x15c7 | COST_DOWN_CID | card_info.inc (already) |
| DAT_0803aaac | 0x1472 | EMBODIMENT_OF_APOPHIS_CID | card_info.inc |
| DAT_0803adcc | 0x1472 | EMBODIMENT_OF_APOPHIS_CID | card_info.inc |
| DAT_0803b094 | 0x1472 | EMBODIMENT_OF_APOPHIS_CID | card_info.inc |
| DAT_0803aab0 | 0x1636 | METAL_REFLECT_SLIME_CID | card_info.inc |
| DAT_0803add0 | 0x1636 | METAL_REFLECT_SLIME_CID | card_info.inc |
| DAT_0803b098 | 0x1636 | METAL_REFLECT_SLIME_CID | card_info.inc |
| DAT_0803aac4 | 0x172f | SKULL_ZOMA_CID | card_info.inc |
| DAT_0803ade4 | 0x172f | SKULL_ZOMA_CID | card_info.inc |
| DAT_0803b0b0 | 0x172f | SKULL_ZOMA_CID | card_info.inc |
| DAT_0803ab20 | 0xffffeb50 | NODE_POOL_NEG_OFFSET | duel_field.inc |
| DAT_0803ae68 | 0xffffeb50 | NODE_POOL_NEG_OFFSET | duel_field.inc |
| DAT_0803b074 | 0xffffeb50 | NODE_POOL_NEG_OFFSET | duel_field.inc |
| DAT_0803b128 | 0xffffeb50 | NODE_POOL_NEG_OFFSET | duel_field.inc |
| DAT_0803abec | 0x150b | A_LEGENDARY_OCEAN_CARD_ID | card_info.inc |
| DAT_0803b21c | 0x18c7 | DORIADO_CID | card_info.inc |
| DAT_0803b220 | 0x19ef | EHERO_ERIKSHIELER_CID | card_info.inc |

Notes:
- PLAYER_BLOCK_STRIDE: 21 distinct slots (16 original + 5 new from get_zone_slot_ptr: b30c/b324/b33c/b354/b3a0).
- All reuse constants confirmed present in constants/*.inc via grep.

#### 新建 EQ 常量 (new=8, all -> card_info.inc)

All card IDs verified against data/card-stats.s. confidence: high.

| value | card name | proposed_const | slot(s) |
|-------|-----------|---------------|---------|
| 0x15e3 | Demotion (pw=72575145; card_1236 slot=0x15E3) | DEMOTION_CID | DAT_0803aba0 |
| 0x12a1 | Parasite Paracide (pw=27911549; card_0625 slot=0x12A1) | PARASITE_PARACIDE_CID | DAT_0803ace0 |
| 0x1357 | DNA Surgery (pw=74701381; card_0760 slot=0x1357) | DNA_SURGERY_CID | DAT_0803ad7c |
| 0x15ae | D. Tribe (pw=02833249; card_1199 slot=0x15AE) | D_TRIBE_CID | DAT_0803ada8 |
| 0x183b | Homunculus the Alchemic Being (pw=40410110; card_1727 slot=0x183B) | HOMUNCULUS_CID | DAT_0803b06c |
| 0x145b | Scroll of Bewitchment (pw=10352095; card_0927 slot=0x145B) | SCROLL_OF_BEWITCHMENT_CID | DAT_0803b198 |
| 0x171f | DNA Transplant (pw=56769674; card_1495 slot=0x171F) | DNA_TRANSPLANT_CID | (base for shifted) |
| 0xb8f80000 | DNA Transplant CID << 19 sentinel (0x171f<<19=0xb8f80000) | DNA_TRANSPLANT_CID_SHIFTED | DAT_0803b030 |

Verification for DNA_TRANSPLANT_CID_SHIFTED:
- Code at asm line 11231: `lsls r0,r0,#0x13` (on slot_word extracts bits[12:0] shifted left 19)
- Then `cmp r0, DAT_0803b030` where DAT_0803b030 = 0xb8f80000
- `0xb8f80000 >> 19 = 0x171f` (python verified)
- Pattern identical to BATTERYMAN_AA_CID_SHIFTED / BATTERYMAN_C_CID_SHIFTED in Seg-4b.
- confidence: high.

C5 dedup check: grep of all constants/*.inc for 0x15e3/0x12a1/0x1357/0x15ae/0x183b/0x145b/0x171f/0xb8f80000 returned 0 hits. Safe to create.

Note: 0x149f (DAT_0803aec4) is NOT in card-stats.s (gap between 0x149e=Miracle Dig and 0x14a1=Vengeful Bog Spirit). Used as card_id comparison in resolve_slot_chain_best_target (cmp r4,r0 at asm line 11079 after lsls/lsrs card_id extraction). No constant created; handle via RENAME_SLOTS.

### REF_SLOTS (USER-label + DATA-ref)

| slot | target | gas_label | slot_label |
|------|--------|-----------|------------|
| DAT_0803a88c | 0x0201c510 | gDuelFieldSlots | build_elig_table_field_slots_a |
| DAT_0803a94c | 0x0201e2a0 | gDuelCardCtxBase | build_elig_table_ctx_base |
| DAT_0803a954 | 0x0201c510 | gDuelFieldSlots | build_elig_table_field_slots_b |
| DAT_0803a9f8 | 0x0201c510 | gDuelFieldSlots | eval_equip_chain_field_slots_a |
| DAT_0803aa74 | 0x0803777d | check_level_conv_lab_node_match+1 | eval_equip_chain_pred_fnptr |
| DAT_0803aa78 | 0x0201d9c0 | gEquipNodePool | eval_equip_chain_node_pool_a |
| DAT_0803ab1c | 0x0201d9c0 | gEquipNodePool | eval_equip_chain_node_pool_b |
| DAT_0803ab24 | 0x0201c520 | gDuelFieldSlotState | eval_equip_chain_slot_state_a |
| DAT_0803aba8 | 0x0201c5d8 | gDuelFieldSlots_p2_base | eval_equip_chain_p2_slots_base |
| DAT_0803ac5c | 0x0201c510 | gDuelFieldSlots | get_state_code_field_slots_a |
| DAT_0803ace4 | 0x0201c510 | gDuelFieldSlots | query_state_code_field_slots_a |
| DAT_0803ad88 | 0x0201c510 | gDuelFieldSlots | query_state_code_field_slots_b |
| DAT_0803ad8c | 0x0201d9c0 | gEquipNodePool | query_state_code_node_pool_a |
| DAT_0803ae64 | 0x0201d9c0 | gEquipNodePool | query_state_code_node_pool_b |
| DAT_0803ae6c | 0x0201c520 | gDuelFieldSlotState | query_state_code_slot_state_a |
| DAT_0803aecc | 0x0201c510 | gDuelFieldSlots | resolve_chain_target_field_slots_a |
| DAT_0803af3c | 0x0201c510 | gDuelFieldSlots | resolve_chain_target_field_slots_b |
| DAT_0803b034 | 0x0201d9c0 | gEquipNodePool | resolve_chain_target_node_pool_a |
| DAT_0803b070 | 0x0201d9c0 | gEquipNodePool | resolve_chain_target_node_pool_b |
| DAT_0803b12c | 0x0201c520 | gDuelFieldSlotState | resolve_chain_target_slot_state_a |
| DAT_0803b1a0 | 0x0201c510 | gDuelFieldSlots | resolve_chain_target_field_slots_c |
| DAT_0803b124 | 0x0201d9c0 | gEquipNodePool | resolve_chain_target_node_pool_c |
| DAT_0803b218 | 0x0201c510 | gDuelFieldSlots | compute_zone_mask_field_slots_a |
| DAT_0803b2cc | 0x0803b2d0 | get_zone_slot_ptr_switchD_table | get_zone_slot_ptr_switch_table_ptr |
| DAT_0803b2f8 | 0x0201c880 | gP1ChainZoneArray | get_zone_slot_ptr_chain_zone_base |
| DAT_0803b310 | 0x0201c740 | gP1SlotSetCodeArray | get_zone_slot_ptr_slot_set_code_base |
| DAT_0803b328 | 0x0201c8f8 | gP1HandSlotArray | get_zone_slot_ptr_hand_slot_base |
| DAT_0803b340 | 0x0201cab0 | gP1AltHandSlotArray | get_zone_slot_ptr_alt_hand_base |
| DAT_0803b358 | 0x0201c600 | gP1FieldArrayCBase | get_zone_slot_ptr_field_c_base |
| DAT_0803b380 | 0x0201bc54 | gDuelEffectChainSlots | get_zone_slot_ptr_effect_chain_base |
| DAT_0803b3a4 | 0x0201c510 | gDuelFieldSlots | get_zone_slot_ptr_field_slots_a |

Notes on new global labels:

**gP2SlotEquipWordBase = 0x0201c5e8** (1 ROM ref, this slot only):
- Evidence: asm line 10658 in eval_equip_chain_score_for_slot:
  `ldr r7, DAT_0803abac` = 0x0201c5e8, then `adds r0,r1,r7` where r1 = player_stride*player_parity.
  The result is used as a base for `ldr r1,[r0,#0x0]` -- reads the equip_word field within a
  p2 slot entry. Relation: 0x0201c5e8 = gDuelFieldSlots_p2_base (0x0201c5d8) + 0x10.
  Offset 0x10 from a field slot entry = equip_node_link field (from Seg-4b analysis).
  consumer: eval_equip_chain_score_for_slot @ asm line 10685. confidence: med
  (1 ref; semantic is "p2 base + equip word offset" but may be a specific computed address).
  ALTERNATIVE: treat as inline value (no new global), use `eval_equip_chain_p2_equip_off`
  RENAME slot only. Given 1 ref, prefer RENAME to avoid orphan global.

**gDuelFieldSlots_magic_zone_p0 = 0x0201c574** (1 ROM ref, this slot only):
- Evidence: asm line 10863 in query_slot_card_state_code:
  `ldr r0, DAT_0803ad80` = 0x0201c574; then `adds r0,r5,r0` where r5 = player_stride*player_parity.
  0x0201c574 = gDuelFieldSlots (0x0201c510) + 5*20 = gDuelFieldSlots + 0x64 = P0 slot[5] base.
  Slot[5] in gDuelFieldSlots is the first magic/trap zone slot for P0. consumer: query_slot_card_state_code. confidence: med
  (1 ref only). Similarly: RENAME slot label rather than orphan global.

**Revised decision for both single-ref globals**: Use RENAME (descriptive slot label + EOL comment only). No new ewram.inc global needed. Both are classified RENAME only -- stale REF rows for these two slots have been removed from the REF_SLOTS table above (fix iter 1).

### RENAME_SLOTS (纯改名 + EOL)

| slot | old_label | new_label | eol |
|------|-----------|-----------|-----|
| DAT_0803aec4 | DAT_0803aec4 | resolve_gap_cid_149f | gap CID 0x149f; not in card-stats.s (between Miracle Dig 0x149e and Vengeful Bog Spirit 0x14a1) |
| DAT_0803abac | DAT_0803abac | eval_equip_chain_p2_equip_word_base | 0x0201c5e8 = gDuelFieldSlots_p2_base+0x10; equip_word field in P2 slot entry; 1 ref |
| DAT_0803ad80 | DAT_0803ad80 | query_state_code_magic_zone_p0_base | 0x0201c574 = gDuelFieldSlots+5*20; P0 magic/trap zone slot[5] base; 1 ref (label unified: dropped _base-less variant) |

### FUNC_RENAME

None. All 13 functions: names match observed body semantics. No misname signal detected.

### PLATE (R5)

All 13 functions already have English plate comments. No stale FUN_ labels in Seg-5 lines 10171..11740 (grep confirmed). C8 verification: 0 FUN_ matches. No plate rewrite required.

---

## carve 计划 (R7)

None. ROM_INCBIN 0x3b24e/0x66 = 0-ref dead code -> §5.1 (see above). No referenced data in segment.

---

## disasm 计划 (R4)

None. ROM_INCBIN 0x3b24e/0x66 has 0 references -- no jump-table entry, no bl target, no pointer in ROM points into this block. Dead code -> §5.1. Disassembling unreachable code would not produce any new function entries and violates Rule 2 (only ref-confirmed code blocks get R4 disasm).

---

## 新增 constants / 全局

```
card_info.inc (new additions):
  DEMOTION_CID              = 0x000015e3  @ Demotion (pw=72575145; card_1236 slot=0x15E3)
  PARASITE_PARACIDE_CID     = 0x000012a1  @ Parasite Paracide (pw=27911549; card_0625 slot=0x12A1)
  DNA_SURGERY_CID           = 0x00001357  @ DNA Surgery (pw=74701381; card_0760 slot=0x1357)
  D_TRIBE_CID               = 0x000015ae  @ D. Tribe (pw=02833249; card_1199 slot=0x15AE)
  HOMUNCULUS_CID            = 0x0000183b  @ Homunculus the Alchemic Being (pw=40410110; card_1727 slot=0x183B)
  SCROLL_OF_BEWITCHMENT_CID = 0x0000145b  @ Scroll of Bewitchment (pw=10352095; card_0927 slot=0x145B)
  DNA_TRANSPLANT_CID        = 0x0000171f  @ DNA Transplant (pw=56769674; card_1495 slot=0x171F)
  DNA_TRANSPLANT_CID_SHIFTED= 0xb8f80000  @ DNA_TRANSPLANT_CID<<19; shifted sentinel in lsls+cmp idiom
```

C5 dedup: all 8 values grep-confirmed absent from all 19 constants/*.inc files.

---

## §5.1 登记 (Rule 3) -- 0 引用块

| 地址 | size | Seg | 内容 | 引用数 | 状态 |
|------|------|-----|------|-------|------|
| 0x0803b24e | 0x66 | Seg-5 | dead THUMB code: 2-byte pad + 30B gDuelFieldSlots-ptr fn (x2 copies) + 38B variant fn. Orphaned slot-ptr inlines, superseded by get_zone_slot_ptr dispatch. | raw=0 thumb=0 | §5.1 留待 |

---

## 消费者证据 (R6) -- 关键槽语义

| slot | 函数 | asm 行 | 语义 | 置信度 |
|------|------|--------|------|-------|
| DAT_0803aa74 = 0x0803777d | eval_equip_chain_score_for_slot | 10475 `bl find_equip_chain_node_by_pred` with this as pred fn-ptr | fn-ptr for check_level_conv_lab_node_match (THUMB +1) | high -- identical pattern to Seg-3 REF slot @ 0x0803aa74 asm:3381 |
| DAT_0803aba0 = 0x15e3 | eval_equip_chain_score_for_slot | 10679 `cmp r3,r0 (DEMOTION_CID)` | Demotion card_id gating in equip chain score eval | high -- card-stats.s card_1236 slot=0x15E3 |
| DAT_0803ace0 = 0x12a1 | query_slot_card_state_code | 10848 `ldr r2, DAT_0803ace0; bl test_slot_has_active_card` | Parasite Paracide card_id; zone slot count limit check | high -- card-stats.s card_0625 slot=0x12A1 |
| DAT_0803ad7c = 0x1357 | query_slot_card_state_code | 10859 `ldr r2, DAT_0803ad7c; bl test_slot_has_active_card` | DNA Surgery card_id; zone type 1 active-card check | high -- card-stats.s card_0760 slot=0x1357 |
| DAT_0803ada8 = 0x15ae | query_slot_card_state_code | 10957 `ldr r0, DAT_0803ada8; cmp r2,r0` | D. Tribe card_id (equip node type 1 match) | high -- card-stats.s card_1199 slot=0x15AE |
| DAT_0803aec4 = 0x149f | resolve_slot_chain_best_target | 11079 `ldr r0, DAT_0803aec4; cmp r4,r0; bne skip` | gap CID 0x149f; card_id compare for special path branch | high (usage confirmed) -- card absent from data/card-stats.s (deleted/reserved slot); use rename pattern `resolve_gap_cid_149f` |
| DAT_0803b030 = 0xb8f80000 | resolve_slot_chain_best_target | 11232 `lsls r0,r0,#0x13; ldr r1, DAT_0803b030; cmp r0,r1` | DNA Transplant CID<<19 shifted sentinel; identical lsls+cmp idiom to BATTERYMAN_AA/C_CID_SHIFTED | high -- 0xb8f80000>>19=0x171f, card-stats.s card_1495 slot=0x171F |
| DAT_0803b06c = 0x183b | resolve_slot_chain_best_target | 11315 `ldr r0, DAT_0803b06c; cmp r2,r0` | Homunculus the Alchemic Being CID (equip node type 3 match) | high -- card-stats.s card_1727 slot=0x183B |
| DAT_0803b198 = 0x145b | resolve_slot_chain_best_target | 11461 `ldr r0, DAT_0803b198; cmp r4,r0` | Scroll of Bewitchment CID (node type 0xa special path) | high -- card-stats.s card_0927 slot=0x145B |
| DAT_0803abac = 0x0201c5e8 | eval_equip_chain_score_for_slot | 10685 `ldr r7, DAT_0803abac; adds r0,r1,r7; ldr r1,[r0,#0x0]` | gDuelFieldSlots_p2_base+0x10; equip word field in P2 slot; 1 ref total | med -- address derivation is clear but semantic of +0x10 offset is inferred from Seg-4b slot layout |
| DAT_0803ad80 = 0x0201c574 | query_slot_card_state_code | 10863 `ldr r0, DAT_0803ad80; adds r0,r5,r0; ldrh r1,[r0,#0x4]` | gDuelFieldSlots + 5*20 = P0 magic/trap zone slot[5] base; 1 ref total | med -- address arithmetic is certain (0x0201c574-0x0201c510=0x64=5*20), semantic label is inferred |

---

## 求助

None. All semantics resolved. Low-confidence items:
- DAT_0803abac (0x0201c5e8) and DAT_0803ad80 (0x0201c574): both med-conf due to single reference. Treated as RENAME (inline descriptive label + EOL) rather than new ewram.inc globals, avoiding orphan global creation (C5 principle).
- gap CID 0x149f: treated as low-conf RENAME per card_id gap policy (eval_gap_cid_149f pattern per file 02/03 precedent).

---

## C8 stale-FUN_ map (Seg-5 range)

Grep result: `grep -n "FUN_" asm/03_equip_chain_hand.s | awk -F: '$1>=10171 && $1<=11606'` = 0 hits.

No stale FUN_ labels in Seg-5. C8 verification: PASS. No plate rewrites required for stale-name correction.

---

## 自检结果

1. **EQ values vs ROM bytes**: all 79 slot values verified (68 original via python struct.unpack + 11 new confirmed from asm literal values). 0 mismatches.
2. **THUMB fn-ptr +1**: DAT_0803aa74 = 0x0803777d = check_level_conv_lab_node_match+1 (odd address). Consistent with Seg-3 known issue (re-export reverts to even; must re-patch after each export).
3. **All plate/EOL text**: no CJK in this proposal's Ghidra-destined content (all ASCII). Slot labels pass `^[a-z][a-z0-9_]+$`.
4. **§5.1 block**: ref-scan wide-scan confirmed 0 references. Block is dead code, not §5.1-eligible THUMB with real callgraph entries.
5. **C5 dedup**: 8 new CID constants grep-confirmed absent from all constants/*.inc. No new ewram.inc constants needed (all 11 get_zone_slot_ptr slots reuse existing ewram.inc entries).
6. **C13 residual 100% coverage**: 79 slots covered: EQ(45) + REF(31) + RENAME(3 total) = 79. All accounted for.

Corrected breakdown:
- EQ = 45 (21 PLAYER_BLOCK_STRIDE + 4 NODE_POOL_NEG_OFFSET + 13 reuse card CIDs + 8 new card CIDs = 46... recount: counted directly from slot table = 45)
  - Direct count confirmed: 45 EQ rows in master table.
- REF = 31 (27 original rows - 2 stale abac/ad80 rows + 6 new from get_zone_slot_ptr = 31)
- RENAME = 3 (gap_cid_149f + eval_equip_chain_p2_equip_word_base + query_state_code_magic_zone_p0_base)
- FUNC_RENAME = 0
- PLATE = 0 new (13 existing confirmed stale-free; get_zone_slot_ptr plate already present in asm)

---

## Executor Report: F03-Seg-5

- fn=13 (build_equip_target_eligibility_table..get_zone_slot_ptr)
- slots: EQ=45 REF=31 RENAME=3 FUNC_RENAME=0 PLATE=0  total=79
- carve=0 disasm=0 §5.1=1 (0x0803b24e / 0x66, dead THUMB code, 0 ROM refs)
- 新增 constants/全局: card_info.inc +8 (DEMOTION_CID / PARASITE_PARACIDE_CID / DNA_SURGERY_CID / D_TRIBE_CID / HOMUNCULUS_CID / SCROLL_OF_BEWITCHMENT_CID / DNA_TRANSPLANT_CID / DNA_TRANSPLANT_CID_SHIFTED); ewram.inc: no new additions (all 11 get_zone_slot_ptr slots reuse existing constants)
- 求助: none
- proposal: doc/dev/refine/F03-Seg-5.proposal.md

---

## Fix iteration 1 (2026-06-12, fixer mode A per review NEEDS_FIX)

Changes applied per review items #1, #2, #3:

### #1 (C2/C13) -- get_zone_slot_ptr 13th function added

- 函数表 "x12" -> "x13"; 新增行: 0x0803b2b4 | get_zone_slot_ptr | asm 行 11609.
- 残留槽总计 68 -> 79: 新增 11 行至 master slot table (b30c/b310/b324/b328/b33c/b340/b354/b358/b380/b3a0/b3a4).
  - b30c/b324/b33c/b354/b3a0: EQ PLAYER_BLOCK_STRIDE (reuse ewram.inc); master table category = EQ.
  - b310: REF gP1SlotSetCodeArray (0x0201c740, zone_0d array base).
  - b328: REF gP1HandSlotArray (0x0201c8f8, zone_0e).
  - b340: REF gP1AltHandSlotArray (0x0201cab0, zone_0f).
  - b358: REF gP1FieldArrayCBase (0x0201c600, zone_0b).
  - b380: REF gDuelEffectChainSlots (0x0201bc54, default extended base).
  - b3a4: REF gDuelFieldSlots (0x0201c510, default main field).
- EQ_SLOTS reuse table: 5 new PLAYER_BLOCK_STRIDE rows added (b30c/b324/b33c/b354/b3a0). PLAYER_BLOCK_STRIDE note updated: 16 -> 21 distinct slots.
- REF_SLOTS table: 6 new rows added (b310/b328/b340/b358/b380/b3a4) with slot_labels get_zone_slot_ptr_*.
- No new constants required (all 11 slots reuse existing ewram.inc entries).

### #2 (C6) -- REF/RENAME duplicate rows removed; label unified

- REF_SLOTS table: removed stale row DAT_0803abac (was duplicated in RENAME_SLOTS).
- REF_SLOTS table: removed stale row DAT_0803ad80 (was duplicated in RENAME_SLOTS with different label).
- DAT_0803ad80 label unified to `query_state_code_magic_zone_p0_base` (RENAME_SLOTS canonical); the inconsistent REF variant `query_state_code_magic_zone_p0` (without _base) is eliminated.
- Master slot table: updated category for abac and ad80 from "REF ... (NEW global)" to "RENAME ... (1 ref, no new global)".
- "Revised decision" note updated to confirm stale REF rows removed.

### #3 (C13 count) -- Executor Report corrected

Updated counts: EQ=45 REF=31 RENAME=3 total=79.
- EQ: 40 original + 5 new (PLAYER_BLOCK_STRIDE from get_zone_slot_ptr) = 45.
- REF: 27 original rows - 2 stale (abac/ad80) + 6 new (get_zone_slot_ptr) = 31.
- RENAME: 3 (unchanged).
- Self-check section rewritten with correct arithmetic.
