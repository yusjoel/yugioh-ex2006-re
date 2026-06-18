# Refine Proposal: F09-Seg-8  [0x0807629c..0x0807738c)

> Split decision: **Seg-8a** (0x7629c..0x76908, 9 fn + B1+B2) + **Seg-8b** (0x76908..0x7738c, 10 fn + B3+B4 + switchD_08077144).
> Slot distribution: 8a=27, 8b=49, total=76 (matches exhaustive python count).

---

## 段测绘

### 函数入口 (21 push prologues = 19 distinct function entries, double-push counted once)

| 地址 | 函数名 | 归属段 |
|------|--------|--------|
| 0x0807629c | enqueue_hand_spell_sprite_with_lp_counter | 8a |
| 0x080762c8 | invoke_equip_oam_for_zone_e_bits46 | 8a |
| 0x0807633c | tick_equip_zone_bitmap_display_seq (contains switchD_0807638c) | 8a |
| 0x08076454 | enqueue_equip_slot_sprite_if_not_in_chain | 8a |
| 0x08076490 | tick_equip_zone_hand_sprite_by_card_pair | 8a |
| 0x08076510 | check_effect_slot_card_type_flag_by_id | 8a |
| [B1 0x765b0/0x2c + B2 0x765f0/0x19c] | fn_eligible_mustering_dark_scorpions + 5 sub-stubs | 8a |
| 0x0807678c | enqueue_effect_node_sprite_type11_mode5 | 8a |
| [B3 0x767aa/0x32 + B4 0x767f8/0x110] | fn_eligible_spell_vanishing + 7 sub-stubs | 8a |
| **SPLIT** 0x08076908 | enqueue_hand_spell_sprite_with_slot_count | **8b** |
| 0x080769fc | enqueue_equip_zone_sprite_zone_type15 | 8b |
| 0x08076ae8 | tick_zone_sprite_pipeline_by_lp_table_delta | 8b |
| 0x08076b1c | enqueue_equip_zone_sprite_with_neo_daedalus_and_chain | 8b |
| 0x08076bec | check_equip_slot_match_for_card_render | 8b |
| 0x08076c90 | dispatch_spell_zone_sprite_by_display_state | 8b |
| 0x08076de0 | update_equip_target_bitmap_for_zone15 | 8b |
| 0x08076e20 | enqueue_zone_equip_sprite_black_luster_soldier | 8b |
| 0x08076ebc | enqueue_effect_slot_sprite_by_card_id_score | 8b |
| 0x080770b4 | check_equip_slot_col_match_for_activation | 8b |
| 0x08077118 | dispatch_equip_effect_node_by_opcode (contains switchD_08077144) | 8b |
| 0x08077318 | enqueue_hand_card_sprite_alt_with_zone_decrement | 8b |

### 残留自动名槽 (76 total, exhaustive)

**Seg-8a slots (0x7629c..0x76908): 27**

| 地址 | 槽名 | 值 |
|------|------|----|
| 0x08076334 | DAT_08076334 | 0x00000868 |
| 0x08076338 | DAT_08076338 | 0x0201c8f8 |
| 0x08076358 | DAT_08076358 | 0x0201b290 |
| 0x08076390 | PTR_gP1LifePoints_08076390 | 0x0201c4e0 |
| 0x08076394 | DAT_08076394 | 0x00001da8 |
| 0x08076398 | PTR_switchdataD_0807639c_08076398 | 0x0807639c |
| 0x080763c8 | DAT_080763c8 | 0x080507ad |
| 0x080763dc | DAT_080763dc | 0x080507ad |
| 0x080763f4 | DAT_080763f4 | 0x08053f11 |
| 0x08076418 | DAT_08076418 | 0x080507ad |
| 0x08076448 | PTR_gP1LifePoints_08076448 | 0x0201c4e0 |
| 0x0807644c | DAT_0807644c | 0x00001d68 |
| 0x08076450 | DAT_08076450 | 0x00001d6c |
| 0x08076488 | PTR_gP1LifePoints_08076488 | 0x0201c4e0 |
| 0x0807648c | DAT_0807648c | 0x00001cec |
| 0x080764ec | DAT_080764ec | 0x0201b290 |
| 0x080764f0 | DAT_080764f0 | 0x00000868 |
| 0x080764f4 | DAT_080764f4 | 0x0201c740 |
| 0x0807655c | DWORD_0807655c | 0x0201b290 |
| 0x08076560 | DWORD_08076560 | 0x00000484 |
| 0x08076564 | DWORD_08076564 | 0x00000868 |
| 0x08076568 | DWORD_08076568 | 0x0201c600 |
| 0x0807656c | DWORD_0807656c | 0x00001656 |
| 0x08076570 | DWORD_08076570 | 0x00001531 |
| 0x08076584 | DWORD_08076584 | 0x00001685 |
| 0x080765f0 | DAT_080765f0 | (B2 sub-stubs start) |
| 0x080767f8 | DAT_080767f8 | (B4 sub-stubs start) |

**Seg-8b slots (0x76908..0x7738c): 49**

| 地址 | 槽名 | 值 |
|------|------|----|
| 0x080769c4 | DWORD_080769c4 | 0x0201b290 |
| 0x080769c8 | DWORD_080769c8 | 0x000004a4 |
| 0x080769cc | DWORD_080769cc | 0x00000868 |
| 0x080769d0 | DWORD_080769d0 | 0x0201c8f8 |
| 0x080769d4 | DWORD_080769d4 | 0x00000cc8 |
| 0x080769f8 | DWORD_080769f8 | 0x000004a4 |
| 0x08076ae0 | DWORD_08076ae0 | 0x00000868 |
| 0x08076ae4 | DWORD_08076ae4 | 0x0201c510 |
| 0x08076b14 | DWORD_08076b14 | 0x0201c4e0 |
| 0x08076b18 | DWORD_08076b18 | 0x00000868 |
| 0x08076ba4 | DWORD_08076ba4 | 0x000016be |
| 0x08076ba8 | DWORD_08076ba8 | 0x00000868 |
| 0x08076bac | DWORD_08076bac | 0x0201cab0 |
| 0x08076be8 | DWORD_08076be8 | 0x000016be |
| 0x08076c48 | DWORD_08076c48 | 0x00000868 |
| 0x08076c4c | DWORD_08076c4c | 0x0201c510 |
| 0x08076c8c | DWORD_08076c8c | 0x0201bb90 |
| 0x08076d1c | DWORD_08076d1c | 0x00000868 |
| 0x08076d20 | DWORD_08076d20 | 0x0201c510 |
| 0x08076d24 | DWORD_08076d24 | 0x0201b290 |
| 0x08076dd8 | DWORD_08076dd8 | 0x00001d10 |
| 0x08076ddc | DWORD_08076ddc | 0x0201c4e0 |
| 0x08076eb0 | DAT_08076eb0 | 0x00000868 |
| 0x08076eb4 | DAT_08076eb4 | 0x0201c510 |
| 0x08076eb8 | DAT_08076eb8 | 0x000016cb |
| 0x08076f1c | DAT_08076f1c | 0x000016e3 |
| 0x08076f20 | DAT_08076f20 | 0x000014be |
| 0x08076f34 | DAT_08076f34 | 0x00001511 |
| 0x08076f38 | DAT_08076f38 | 0x000016ce |
| 0x08076f50 | DAT_08076f50 | 0x000018ca |
| 0x08076f68 | DAT_08076f68 | 0x000019ab |
| 0x08076fb8 | PTR_gP1LifePoints_08076fb8 | 0x0201c4e0 |
| 0x08076fbc | DAT_08076fbc | 0x00000868 |
| 0x0807703c | DAT_0807703c | 0x00000868 |
| 0x08077040 | DAT_08077040 | 0x0201c510 |
| 0x08077044 | DAT_08077044 | 0x0000ffff |
| 0x080770b0 | DAT_080770b0 | 0x000019a7 |
| 0x08077110 | DAT_08077110 | 0x00000868 |
| 0x08077114 | DAT_08077114 | 0x0201c510 |
| 0x08077148 | DAT_08077148 | 0x0201b290 |
| 0x0807714c | DAT_0807714c | 0x08077150 |
| 0x08077278 | PTR_gP1LifePoints_08077278 | 0x0201c4e0 |
| 0x0807727c | DAT_0807727c | 0x00000868 |
| 0x08077280 | DAT_08077280 | 0x00001c88 |
| 0x080772cc | DAT_080772cc | 0x00000868 |
| 0x080772d0 | DAT_080772d0 | 0x0201c600 |
| 0x080772d4 | DAT_080772d4 | 0x00001c88 |
| 0x0807737c | DAT_0807737c | 0x00000868 |
| 0x08077380 | DAT_08077380 | 0x0201cab0 |

### ROM_INCBIN / .byte 块: 4 blocks

| 地址 | size | 归属段 |
|------|------|--------|
| 0x080765b0 | 0x2c (44B) | 8a |
| 0x080765f0 | 0x19c (412B) | 8a |
| 0x080767aa | 0x32 (50B) | 8a |
| 0x080767f8 | 0x110 (272B) | 8a |

---

## 数据块分类 (Rule 2/3) -- ref-scan 证据

| 块 | ref-scan (raw / THUMB+1) | 判定 | 理由 |
|----|--------------------------|------|------|
| B1 0x765b0/0x2c | raw=0 thumb+1=1 @ROM:0x1e41a68 (GBA:0x09e41a68) | **R4 disasm** (fn_eligible stub) | FS handler table THUMB+1 ref; CID=0x169e (MUSTERING_DARK_SCORPIONS_CID REUSE); fn_el slot ROM off 0x1e41a68, CID at slot-4 = 0x1e41a64 = 0x169e (python struct.unpack_from('<H', rom, 0x1e41a64)); fn_activate+1 at 0x1e41a60 = 0x0000169e/0x00000000 (pad); entry verified |
| B2 0x765f0/0x19c | raw=1 @ROM:0x765ec (GBA:0x80765ec), thumb+1=0 | **R4 disasm** (sub-stubs) | raw ptr in dispatch table at 0x765dc..0x765ef (5 entries: 0x08076780/6d8/6a8/6616/65f0 all inside B2); raw code addrs not THUMB+1 -> dispatch sub-stubs; pattern matches Seg6 sub-stub blocks |
| B3 0x767aa/0x32 | raw=0, thumb+1=1 @ROM:0x1e41b28 (GBA:0x09e41b28) | **R4 disasm** (fn_eligible stub) | FS handler table THUMB+1 ref; CID at slot-4 = ROM 0x1e41b24 = 0x16a6 (SPELL_VANISHING_CID REUSE); 2B pad at 0x767aa (0x0000), fn_eligible starts at 0x767ac = THUMB target; entry verified |
| B4 0x767f8/0x110 | raw=1 @ROM:0x767f4 (GBA:0x80767f4), thumb+1=0 | **R4 disasm** (sub-stubs) | raw ptr in dispatch table at 0x767dc..0x767f7 (7 entries: 0x080768cc/8b8/8aa/890/818/804/7f8 all inside B4); same pattern as B2; raw code addrs -> dispatch sub-stubs |

**C5 CID dedup by value:**
- B1 CID 0x169e: grep `0x0000169e` in constants/card_info.inc -> line 705 `MUSTERING_DARK_SCORPIONS_CID` -> **REUSE**
- B3 CID 0x16a6: grep `0x000016a6` in constants/card_info.inc -> line 1031 `SPELL_VANISHING_CID` -> **REUSE**

---

## switchD 处置

### switchD_0807638c (inside tick_equip_zone_bitmap_display_seq)

**Status: already fully decoded** -- no additional action.

Evidence: `switchD_0807638c__switchD` (.hword 0x4687), `switchD_0807638c__switchdataD_0807639c` (6-entry table at 0x7639c..0x763b3), case labels `switchD_0807638c__caseD_1/3/6` and `switchD_0807638c__default` all present in asm (lines 17015..17098). Pattern matches Seg-6 switchD_0807514a precedent (already decoded = no action).

The slot `PTR_switchdataD_0807639c_08076398` holding .word 0x0807639c is the jump-table base ptr -- this gets RENAME_SLOT to `bitmap_dispatch_switch_table_ptr_6398` + EOL.
The `DAT_08076358` holding 0x0201b290 = gDuelPhaseFlags -> EQ_SLOT.

### switchD_08077144 (inside dispatch_equip_effect_node_by_opcode)

**Status: already fully decoded** -- no additional action.

Evidence: `switchD_08077144__switchD` (.hword 0x4687 at 0x77144), `switchD_08077144__switchdataD_08077150` (29-entry table at 0x77150..0x771c3), case labels `switchD_08077144__caseD_80/7f/7e/78/77/64/65` all present in asm (lines 18598..18799). All case targets are inside [0x7629c..0x7738c] and already disassembled (function body labels within dispatch_equip_effect_node_by_opcode).

The slot `DAT_0807714c` holding 0x08077150 (switchdataD table ptr) -> RENAME_SLOT to `equip_effect_opcode_switch_table_ptr_714c` + EOL.
The `DAT_08077148` holding 0x0201b290 = gDuelPhaseFlags -> EQ_SLOT.

---

## 符号化计划 (Seg-8a 和 Seg-8b 合并列出)

### EQ_SLOTS (62 REUSE + 7 NEW = 69 total equate slots)

**REUSE -- 复用 constants/*.inc (C5 grep-by-value 确认):**

| slot | value | const_name | source_inc |
|------|-------|------------|------------|
| DAT_08076334 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc:250 |
| DAT_08076338 | 0x0201c8f8 | gP1HandSlotArray | ewram.inc:333 |
| DAT_08076358 | 0x0201b290 | gDuelPhaseFlags | ewram.inc:352 |
| PTR_gP1LifePoints_08076390 | 0x0201c4e0 | gP1LifePoints | ewram.inc (global) |
| DAT_08076394 | 0x1da8 | LP_CARD_TRACK_BASE_OFF | ewram.inc:247 |
| PTR_gP1LifePoints_08076448 | 0x0201c4e0 | gP1LifePoints | ewram.inc |
| DAT_0807644c | 0x1d68 | ELIGIB_SPRITE_CTRL_OFF | ewram.inc:421 |
| DAT_08076450 | 0x1d6c | ELIGIB_ANIM_STATE_OFF | ewram.inc:422 |
| PTR_gP1LifePoints_08076488 | 0x0201c4e0 | gP1LifePoints | ewram.inc |
| DAT_0807648c | 0x1cec | P1LP_TIMER_OFF | ewram.inc:244 |
| DAT_080764ec | 0x0201b290 | gDuelPhaseFlags | ewram.inc:352 |
| DAT_080764f0 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc:250 |
| DAT_080764f4 | 0x0201c740 | gP1SlotSetCodeArray | ewram.inc:331 |
| DWORD_0807655c | 0x0201b290 | gDuelPhaseFlags | ewram.inc:352 |
| DWORD_08076560 | 0x484 | EQUIP_ACTIVE_CTX_OFF | duel_field.inc:361 |
| DWORD_08076564 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc:250 |
| DWORD_08076568 | 0x0201c600 | gP1FieldArrayCBase | ewram.inc:365 |
| DWORD_0807656c | 0x1656 | DARK_SCORPION_CHICK_CID | card_info.inc:703 |
| DWORD_08076584 | 0x1685 | DARK_SCORPION_GORG_THE_STRONG_CID | card_info.inc:1030 |
| DWORD_080769c4 | 0x0201b290 | gDuelPhaseFlags | ewram.inc:352 |
| DWORD_080769c8 | 0x4a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc:436 |
| DWORD_080769cc | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc:250 |
| DWORD_080769d0 | 0x0201c8f8 | gP1HandSlotArray | ewram.inc:333 |
| DWORD_080769f8 | 0x4a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc:436 |
| DWORD_08076ae0 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc:250 |
| DWORD_08076ae4 | 0x0201c510 | gDuelFieldSlots | duel_field.inc (global) |
| DWORD_08076b14 | 0x0201c4e0 | gP1LifePoints | ewram.inc |
| DWORD_08076b18 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc:250 |
| DWORD_08076ba8 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc:250 |
| DWORD_08076bac | 0x0201cab0 | gP1AltHandSlotArray | ewram.inc:337 |
| DWORD_08076be8 | 0x16be | DD_SCOUT_PLANE_CID | card_info.inc NEW (REUSE after declaring) |
| DWORD_08076c48 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc:250 |
| DWORD_08076c4c | 0x0201c510 | gDuelFieldSlots | duel_field.inc |
| DWORD_08076c8c | 0x0201bb90 | gEquipChainSlotRefs | ewram.inc:316 |
| DWORD_08076d1c | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc:250 |
| DWORD_08076d20 | 0x0201c510 | gDuelFieldSlots | duel_field.inc |
| DWORD_08076d24 | 0x0201b290 | gDuelPhaseFlags | ewram.inc:352 |
| DWORD_08076dd8 | 0x1d10 | DISPLAY_SEQ_ACTIVE_PLAYER_OFF | duel_field.inc:217 |
| DWORD_08076ddc | 0x0201c4e0 | gP1LifePoints | ewram.inc |
| DAT_08076eb0 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc:250 |
| DAT_08076eb4 | 0x0201c510 | gDuelFieldSlots | duel_field.inc |
| DAT_08076eb8 | 0x16cb | BLACK_LUSTER_SOLDIER_ENVOY_CID | card_info.inc:749 |
| DAT_08076f20 | 0x14be | BARK_OF_DARK_RULER_CID | card_info.inc:1016 |
| DAT_08076f34 | 0x1511 | SECRET_OF_THE_BANDIT_CID | card_info.inc:594 |
| DAT_08076f38 | 0x16ce | WILD_NATURES_RELEASE_CID | card_info.inc:907 |
| DAT_08076f68 | 0x19ab | HERO_HEART_CID | card_info.inc:975 |
| PTR_gP1LifePoints_08076fb8 | 0x0201c4e0 | gP1LifePoints | ewram.inc |
| DAT_08076fbc | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc:250 |
| DAT_0807703c | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc:250 |
| DAT_08077040 | 0x0201c510 | gDuelFieldSlots | duel_field.inc |
| DAT_08077044 | 0xffff | EQUIP_SLOT_SCORE_CAP | oam_attr.inc:156 |
| DAT_080770b0 | 0x19a7 | HERO_KID_CID | card_info.inc:1255 |
| DAT_08077110 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc:250 |
| DAT_08077114 | 0x0201c510 | gDuelFieldSlots | duel_field.inc |
| DAT_08077148 | 0x0201b290 | gDuelPhaseFlags | ewram.inc:352 |
| PTR_gP1LifePoints_08077278 | 0x0201c4e0 | gP1LifePoints | ewram.inc |
| DAT_0807727c | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc:250 |
| DAT_08077280 | 0x1c88 | EQUIP_CHAIN_BASE_OFF | ewram.inc:495 |
| DAT_080772cc | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc:250 |
| DAT_080772d0 | 0x0201c600 | gP1FieldArrayCBase | ewram.inc:365 |
| DAT_080772d4 | 0x1c88 | EQUIP_CHAIN_BASE_OFF | ewram.inc:495 |
| DAT_0807737c | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc:250 |
| DAT_08077380 | 0x0201cab0 | gP1AltHandSlotArray | ewram.inc:337 |

**NEW -- 新建 constants (C5 grep-by-value 确认 0 命中):**

| slot | value | new_const_name | target_inc | 证据 |
|------|-------|----------------|------------|------|
| DWORD_08076570 | 0x1531 | DARK_SCORPION_BURGLARS_CID | card_info.inc | card-stats.s:14445 "Dark Scorpion Burglars slot=0x1531 pw=40933924"; grep 0x00001531 card_info.inc = 0 hits; used in check_effect_slot_card_type_flag_by_id BST; conf:high |
| DWORD_08076ba4 | 0x16be | DD_SCOUT_PLANE_CID | card_info.inc | card-stats.s:18332 "D. D. Scout Plane slot=0x16BE pw=03773196"; grep 0x000016be card_info.inc = 0 hits; used in enqueue_equip_zone_sprite_with_neo_daedalus_and_chain at 0x76b76/0x76bc4 BST branches; conf:high |
| DAT_08076f1c | 0x16e3 | ENERGY_DRAIN_CID | card_info.inc | card-stats.s:18787 "Energy Drain slot=0x16E3 pw=56916805"; grep 0x000016e3 card_info.inc = 0 hits; used in enqueue_effect_slot_sprite_by_card_id_score BST; conf:high |
| DAT_08076f50 | 0x18ca | GIFT_OF_THE_MARTYR_CID | card_info.inc | card-stats.s:24065 "Gift of the Martyr slot=0x18CA pw=98792570"; grep 0x000018ca card_info.inc = 0 hits; used in enqueue_effect_slot_sprite_by_card_id_score BST; conf:high |
| DAT_08076f1c | 0x1492 | DEAL_OF_PHANTOM_CID | card_info.inc | NOTE: plate comment says CARD_DEAL_OF_PHANTOM=0x1492; grep 0x00001492 card_info.inc = 0 hits; card-stats.s:12703 "Deal of Phantom slot=0x1492 pw=69122763"; used in enqueue_effect_slot_sprite_by_card_id_score BST entry at 0x76f14 (subs r0,#0x2c from 0x14be -> 0x1492); actually 0x1492 is NOT stored in its own .word slot; it is computed via `subs r0,#0x2c` at runtime from BARK_OF_DARK_RULER_CID -- so NO new EQ slot needed for 0x1492 |
| DWORD_080769d4 | 0xcc8 | HAND_SPELL_SLOT_CC8_OFF | ewram.inc | grep 0x00000cc8 constants/*.inc = 0 hits; used in enqueue_hand_spell_sprite_with_slot_count: gGraveyardSlots + player*0x868 + slot_idx*4 + 0xcc8 to read set_code field; 9 raw ROM refs (python rom.count(struct.pack('<I', 0xcc8)) = 9); semantics: offset within gGraveyardSlots slot record to hand-spell type field; conf:med (exact field semantics from function context; 9 refs confirm significance) |

**Note:** DEAL_OF_PHANTOM_CID (0x1492) is NOT in a literal pool slot -- it is computed at runtime as `BARK_OF_DARK_RULER_CID - 0x2c` (ldr r0, 0x14be; subs r0, #0x2c; cmp r1, r0). So no .word slot / no new EQ needed. Plate comment is correct but no slot to symbolize.

**Note for HERO_KID_CID path:** The path at 0x19a7 uses `count_extra_deck_cards_by_id * 0x19 * 0x10` computed as:
`lsls r1,r0,#1; adds r1,r1,r0; lsls r1,r1,#3; adds r1,r1,r0; lsls r1,r1,#4` = r0*2+r0=3r0; 3r0*8=24r0; 24r0+r0=25r0; 25r0*16=400r0. No literal pool constant for multiplier, computed inline.

**Summary EQ count: 62 REUSE + 6 NEW (5 CIDs + 1 offset) = 68 EQ slots**
(DWORD_08076be8 is REUSE after DD_SCOUT_PLANE_CID is declared; 0x1492 has no slot)

### REF_SLOTS (USER-label + DATA-ref slots)

None needed: all address-valued slots are covered by existing EWRAM globals (gP1LifePoints, gDuelPhaseFlags, gDuelFieldSlots, gP1HandSlotArray, gP1AltHandSlotArray, gP1FieldArrayCBase, gEquipChainSlotRefs, gP1SlotSetCodeArray). All load directly via EQ. No new gXxx global labels required.

### RENAME_SLOTS (label rename, non-equate)

| slot | 旧名 | 新名 | slot_label_comment |
|------|------|------|--------------------|
| PTR_switchdataD_0807639c_08076398 | PTR_switchdataD_0807639c_08076398 | bitmap_dispatch_switch_table_ptr_6398 | .word 0x0807639c; jump-table base for switchD_0807638c (6-entry, LP-count case 1-6); tick_equip_zone_bitmap_display_seq |
| DAT_080763c8 | DAT_080763c8 | check_equip_slot_eligible_by_type_query_ptr_63c8 | .word 0x080507ad (check_equip_slot_eligible_by_type_query+1 raw THUMB code addr); predicate for build_equip_zone_bitmap_for_player caseD_1/2 call; Ruling A non-FS raw code ptr + ASCII EOL |
| DAT_080763dc | DAT_080763dc | check_equip_slot_eligible_by_type_query_ptr_63dc | .word 0x080507ad (same predicate, zone_pair_hit path caseD_3..5); Ruling A |
| DAT_080763f4 | DAT_080763f4 | check_equip_slot_eligible_by_side_match_ptr_63f4 | .word 0x08053f11 (check_equip_slot_eligible_by_side_match_and_type+1; asm/06:1081); caseD_6 predicate; Ruling A |
| DAT_08076418 | DAT_08076418 | check_equip_slot_eligible_by_type_query_ptr_6418 | .word 0x080507ad (same predicate, state 0x7e path for set_equip_activation_state_by_mode); Ruling A |
| DAT_080765f0 | DAT_080765f0 | mustering_dark_scorpions_dispatch_sub_stubs_65f0 | B2 first sub-stub start addr; dispatch table at 0x765dc..0x765ef 5-entry raw ptrs |
| DAT_080767f8 | DAT_080767f8 | spell_vanishing_dispatch_sub_stubs_67f8 | B4 first sub-stub start addr; dispatch table at 0x767dc..0x767f7 7-entry raw ptrs |
| DAT_0807714c | DAT_0807714c | equip_effect_opcode_switch_table_ptr_714c | .word 0x08077150 (switchdataD start, 29-entry table); switchD_08077144 in dispatch_equip_effect_node_by_opcode; Ruling A raw code table ptr |

**Total RENAME_SLOTS: 8**

### FUNC_RENAME

None. No function naming errors detected (all functions have plausible names consistent with body). Confidence:
- tick_equip_zone_bitmap_display_seq: body drives state 0x80/7f/7e/7d correctly named; conf:high
- check_effect_slot_card_type_flag_by_id: body checks [r5+3]chain_value=0xb then CID BST correctly named; conf:high
- dispatch_equip_effect_node_by_opcode: state machine opcode - 0x64 with 0x1d cases; conf:high
- All others: body matches name; conf:high

### PLATE

No plate updates required for Seg-8 functions:
- All plates checked for non-ASCII: `grep [^\x00-\x7F]` on lines 16860..18880 returned 0 hits (python verified). All plates are ASCII-clean.
- No stale FUN_ references found in Seg-8 range.

---

## disasm 计划 (R4)

### B1: fn_eligible_mustering_dark_scorpions @ 0x080765b0

- ROM_INCBIN 0x765b0, 0x2c
- FS handler table THUMB+1 ref: GBA 0x09e41a68, ROM off 0x1e41a68
- CID = MUSTERING_DARK_SCORPIONS_CID (0x169e); REUSE from card_info.inc:705
- fn_eligible start: 0x080765b0 (no 2B pad; B1 starts at 0x765b0, ROM byte at offset 0 = 0xf0 = push opcode)
- Literal pool: 1 DWord expected (from FS entry structure: fn_act slot at 0x1e41a58 = 0x00000000, pad; fn_el = 0x080765b1 THUMB+1 match; expected pool at ~0x765cc..0x765cf or 0x765d0..0x765d3)
- Action: clearListing 0x080765b0..0x080765db -> setTMode -> DisassembleCommand 0x080765b0 -> force_dword literal pool words -> createFunction

### B2: 5 mustering_dark_scorpions dispatch sub-stubs @ 0x080765f0..0x0807678b

- ROM_INCBIN 0x765f0, 0x19c
- Dispatch table: 5 raw entries at 0x765dc..0x765ef -> targets:
  - sub_65f0: 0x080765f0 (first = B2 start)
  - sub_6616: 0x08076616
  - sub_66a8: 0x080766a8
  - sub_66d8: 0x080766d8
  - sub_6780: 0x08076780
- Action: clearListing 0x080765f0..0x0807678b -> setTMode range -> DisassembleCommand per stub (5 commands, one per target) -> force_dword any inline literal pool words -> label stubs: mustering_dark_scorpions_sub_65f0/6616/66a8/66d8/6780 (or _default for catch-all)
- NOTE: 0x19c = 412B is large; may contain inline pools between stubs (prior batches pattern: multiple force_dword 4B clearListing needed per inline pool). Use 4B clearListing for each pool, not 8B.

### B3: fn_eligible_spell_vanishing @ 0x080767aa

- ROM_INCBIN 0x767aa, 0x32
- FS handler table THUMB+1 ref: GBA 0x09e41b28, ROM off 0x1e41b28 -> THUMB+1 value 0x080767ad = fn_eligible+1
- 2B pad at 0x767aa (ROM byte 0x00 0x00); fn_eligible starts at 0x080767ac
- CID = SPELL_VANISHING_CID (0x16a6); REUSE from card_info.inc:1031
- Literal pool: 2 DWords expected (0x32 - 2 pad - ~20B code = ~8B pool)
- Action: clearListing 0x080767aa..0x080767db -> setTMode -> createDWord at 0x080767aa (pad) -> DisassembleCommand 0x080767ac -> force_dword literal pool DWords -> createFunction @ 0x080767ac

### B4: 7 spell_vanishing dispatch sub-stubs @ 0x080767f8..0x08076907

- ROM_INCBIN 0x767f8, 0x110
- Dispatch table: 7 raw entries at 0x767dc..0x767f7 -> targets:
  - sub_67f8: 0x080767f8 (first = B4 start)
  - sub_6804: 0x08076804
  - sub_6818: 0x08076818
  - sub_6890: 0x08076890
  - sub_68aa: 0x080768aa
  - sub_68b8: 0x080768b8
  - sub_68cc: 0x080768cc
- Action: clearListing 0x080767f8..0x08076907 -> setTMode range -> DisassembleCommand per stub (7 commands) -> force_dword inline pool words -> label stubs: spell_vanishing_sub_67f8/6804/6818/6890/68aa/68b8/68cc (or _default)
- NOTE: 0x110 = 272B with 7 stubs; pattern from Seg7 B4 (0x5d5c/0x214) -- multiple inline pool clusters expected. Use 4B clearListing before each pool.

---

## carve 計畫 (R7)

None. No function-to-function ROM_INCBIN blocks requiring carve into rom.s. All 4 blocks are handler stubs (B1, B3) or dispatch sub-stubs (B2, B4) correctly classified as R4 disasm.

---

## 新增 constants / 全局

New equates to add to constants files:

**constants/card_info.inc (5 new CIDs):**
```
.equ DARK_SCORPION_BURGLARS_CID, 0x00001531  @ Dark Scorpion Burglars (pw=40933924; card-stats.s:14445); check_effect_slot_card_type_flag_by_id BST; conf:high
.equ DD_SCOUT_PLANE_CID,         0x000016be  @ D. D. Scout Plane (pw=03773196; card-stats.s:18332); enqueue_equip_zone_sprite_with_neo_daedalus_and_chain BST; conf:high
.equ ENERGY_DRAIN_CID,           0x000016e3  @ Energy Drain (pw=56916805; card-stats.s:18787); enqueue_effect_slot_sprite_by_card_id_score BST; conf:high
.equ GIFT_OF_THE_MARTYR_CID,     0x000018ca  @ Gift of the Martyr (pw=98792570; card-stats.s:24065); enqueue_effect_slot_sprite_by_card_id_score BST; conf:high
.equ DEAL_OF_PHANTOM_CID,        0x00001492  @ Deal of Phantom (pw=69122763; card-stats.s:12703); enqueue_effect_slot_sprite_by_card_id_score plate ref only (computed at runtime as BARK_OF_DARK_RULER_CID-0x2c; no literal pool slot to symbolize; plate EOL documentation only)
```

**constants/ewram.inc (1 new offset):**
```
.equ HAND_SPELL_SLOT_CC8_OFF, 0x00000cc8  @ [gP1HandSlotArray+player*PLAYER_BLOCK_STRIDE+slot_idx*4+0xcc8]: hand-spell slot set_code subfield; 9 raw ROM refs; enqueue_hand_spell_sprite_with_slot_count; conf:med
```

---

## §5.1 登记 (Rule 3) -- 0 引用块

None. All 4 ROM_INCBIN blocks have confirmed references:
- B1: 1 THUMB+1 ref (FS handler table)
- B2: 1+ raw refs (dispatch table)
- B3: 1 THUMB+1 ref (FS handler table)
- B4: 1+ raw refs (dispatch table)

No §5.1 entries for Seg-8.

---

## 消費者証拠 (R6) -- 关键槽语义

| 槽 | 消费者 file:line | 语义 | 置信度 |
|----|----------------|------|--------|
| DWORD_08076570 = 0x1531 | asm/09 line 17292: `DWORD_08076570` in check_effect_slot_card_type_flag_by_id BST (cmp r1,0x1531 branch) | Dark Scorpion Burglars CID; adjacent 0x1656/0x1685/0x1686 Dark Scorpion series confirms | high |
| DWORD_08076ba4,08076be8 = 0x16be | asm/09 lines 17738,17773: BST cmp in enqueue_equip_zone_sprite_with_neo_daedalus_and_chain; at 0x76b76 eors r0,r2; rsbs; orrs pattern for 0-check, then 0x76bc0 cmp r1,r0 branch | D.D. Scout Plane CID; function name + card-stats match; conf:high | high |
| DAT_08076f1c = 0x16e3 | asm/09 line 18263: DAT_08076f1c in enqueue_effect_slot_sprite_by_card_id_score BST (cmp r1,r0 at 0x76f02); plate comment CARD_ENERGY_DRAIN=0x16e3 | Energy Drain CID; card-stats.s:18787 confirms; conf:high | high |
| DAT_08076f50 = 0x18ca | asm/09 line 18295: DAT_08076f50 in enqueue_effect_slot_sprite_by_card_id_score BST (ldr r0, 0x18ca; cmp r1,r0 at 0x76f3c path) | Gift of the Martyr CID; card-stats.s:24065 confirms; conf:high | high |
| DWORD_080769d4 = 0xcc8 | asm/09 lines 17459-17461: ldr r0, DWORD_080769d4; adds r4,r4,r0; ldrh r4,[r4,#0x0] in enqueue_hand_spell_sprite_with_slot_count; base r4 = gGraveyardSlots[player][slot_idx] word, then +0xcc8 reads set_code subfield | offset into gGraveyardSlots hand-slot record; read-only; 9 ROM refs confirms non-trivial use; conf:med |

---

## C13 残留 100% 覆盖证明

Python exhaustive count: 76 unique slots in [0x7629c, 0x7738c).

Classification union:
- EQ_REUSE: 62 slots (all verified by value against constants/*.inc)
- EQ_NEW (5 CIDs + 1 offset): 6 slots -> DWORD_08076570, DWORD_08076ba4, DAT_08076f1c, DAT_08076f50, DWORD_080769d4, + DWORD_08076be8 (REUSE after DD_SCOUT_PLANE_CID declared = EQ_REUSE+1)

Re-tally:
- EQ_REUSE: 62 + 1 (DWORD_08076be8) = 63
- EQ_NEW: 5 (DWORD_08076570/ba4/f1c/f50/769d4)
- RENAME: 8 (switchD table ptr + 4 code ptrs + 2 sub-stub labels + equip_effect opcode table ptr)
- **Total: 63 + 5 + 8 = 76** == exhaustive count. No double-count, no gap.

**EQ vs REF distinction:** All EQ slots hold scalar constants (offsets, CIDs, globals). No slots hold RAM-base addresses that require REF_SLOT treatment -- all globals are already named (gP1LifePoints, gDuelPhaseFlags, gDuelFieldSlots etc.) and used via .equ equates, not USER-label+DATA-ref.

---

## 求助 (低置信度)

**HAND_SPELL_SLOT_CC8_OFF (0xcc8):** Confidence is med because the function enqueue_hand_spell_sprite_with_slot_count accesses `gGraveyardSlots + player*stride + slot_idx*4 + 0xcc8` but the precise semantic of the +0xcc8 sub-field (set_code vs type code vs sprite code) is inferred from context. The function reads it as `lsls r1,r1,#0x2; lsrs r1,r1,#0x18; lsls r1,r1,#0x1` which extracts bits[23:22] of the word -- a 2-bit field. Name HAND_SPELL_SLOT_CC8_OFF is safe (neutral offset name). If reviewer has higher-confidence evidence from callee `enqueue_hand_card_sprite_by_spell_type`, the name could be updated.

**B2/B4 sub-stub semantics:** The dispatch sub-stubs inside B2 (5 targets for Mustering of Dark Scorpions) and B4 (7 targets for Spell Vanishing) have semantics dependent on the card-effect dispatch protocol. Label names `mustering_dark_scorpions_sub_XXXX` and `spell_vanishing_sub_XXXX` follow established Seg6/7 pattern. Internal structure of each stub will be revealed after R4 disasm.

---

## Executor Report: F09-Seg-8

- 槽: EQ=68 (63 REUSE + 5 NEW) REF=0 RENAME=8 FUNC_RENAME=0 PLATE=0
- ROM_INCBIN: disasm=4 (B1 fn_eligible_mustering_dark_scorpions/0x765b0 + B2 5-sub-stubs/0x765f0 + B3 fn_eligible_spell_vanishing/0x767aa + B4 7-sub-stubs/0x767f8); carve=0; §5.1=0
- switchD_0807638c: already decoded, no action
- switchD_08077144: already decoded, no action
- Split: Seg-8a [0x7629c..0x76908) 27 slots; Seg-8b [0x76908..0x7738c) 49 slots
- 新增 constants/全局: card_info.inc +5 (DARK_SCORPION_BURGLARS_CID/DD_SCOUT_PLANE_CID/ENERGY_DRAIN_CID/GIFT_OF_THE_MARTYR_CID/DEAL_OF_PHANTOM_CID); ewram.inc +1 (HAND_SPELL_SLOT_CC8_OFF)
- 求助: HAND_SPELL_SLOT_CC8_OFF置信度med (0xcc8 sub-field semantic from context); B2/B4 sub-stub internal semantics TBD post-disasm
- proposal: doc/dev/refine/F09-Seg-8.proposal.md
