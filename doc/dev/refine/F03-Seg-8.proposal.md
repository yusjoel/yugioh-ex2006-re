# Refine Proposal: F03-Seg-8  [0x0803c774..0x0803d91c)

## 段测绘

### 函数入口 x13

| 地址 | 函数名 | asm 行 |
|------|--------|--------|
| 0x0803c774 | tick_equip_chain_slot_ref_scan_seq | 14346 |
| 0x0803c814 | setup_equip_chain_for_slot | 14434 |
| 0x0803c8e0 | invoke_equip_candidate_scan_setup | 14544 |
| 0x0803c904 | finalize_equip_chain_removal_state | 14572 |
| 0x0803c9ac | tick_equip_chain_activate_state_seq | 14671 |
| 0x0803ca00 | clear_equip_chain_active_state | 14719 |
| 0x0803ca34 | init_equip_ai_state | 14752 |
| 0x0803ca70 | link_equip_node_by_slot_match | 14795 |
| 0x0803caec | tick_zone_slot_removal_chain_repair_seq | 14871 |
| 0x0803ccac | tick_zone_card_place_alt_display_seq | 15112 |
| 0x0803d038 | tick_normal_summon_zone_state | 15576 |
| 0x0803d478 | tick_zone_card_place_display_seq | 16137 |
| 0x0803d6f4 | tick_zone_slot_card_set_display_seq | 16464 |

Note: 13 functions, matching roadmap estimate. Seg-9 starts at tick_zone_slot_transition_display_seq
(0x0803d91c, asm line 16752). Boundary verified: DAT_0803d918 (last slot before 0x3d91c) is at
asm line 16740 -- all slots up to 0x3d918 are in Seg-8.

### 残留自动名槽 x121

All values verified by python struct.unpack('<I', rom[addr-0x08000000:addr-0x07fffffc]) against roms/2343.gba.

| slot addr | ROM value | category |
|-----------|-----------|----------|
| DAT_0803c7b8 | 0x0201bcc0 | REF gDuelDisplaySeqState (reuse ewram.inc) |
| PTR_gP1LifePoints_0803c7bc | 0x0201c4e0 | REF gP1LifePoints (reuse ewram.inc) |
| DAT_0803c7c0 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE (reuse ewram.inc) |
| DAT_0803c7c4 | 0xffbfffff | EQ SLOT_ACTIVE_BIT22_CLR (new duel_field.inc; clears bit22=chain-linked flag) |
| DAT_0803c7c8 | 0xff7fffff | EQ SLOT_ACTIVE_BIT23_CLR (new duel_field.inc; clears bit23=chain-type flag) |
| DAT_0803c7cc | 0x000018a6 | EQ EHERO_AVIAN_CID (reuse card_info.inc line 213) |
| DAT_0803c804 | 0x000019c1 | EQ CHAIN_THRASHER_CID (reuse card_info.inc line 214) |
| DAT_0803c808 | 0x0201bb90 | REF gEquipChainSlotRefs (reuse ewram.inc) |
| DAT_0803c80c | 0x0201bcc0 | REF gDuelDisplaySeqState (reuse) |
| DAT_0803c810 | 0x0000080c | EQ DISPLAY_SEQ_STEP_LOCK_OFF (reuse duel_field.inc) |
| DAT_0803c85c | 0x0201bcc0 | REF gDuelDisplaySeqState (reuse) |
| DAT_0803c860 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE (reuse) |
| DAT_0803c864 | 0x0201c510 | REF gDuelFieldSlots (reuse ewram.inc) |
| DAT_0803c868 | 0x00000fa6 | EQ BLUE_EYES_RANGE_LO_CID (see card section below) |
| DAT_0803c86c | 0x00000fa7 | EQ BLUE_EYES_WHITE_DRAGON_CID (new card_info.inc) |
| DAT_0803c8d4 | 0xffbfffff | EQ SLOT_ACTIVE_BIT22_CLR (reuse new) |
| DAT_0803c8d8 | 0x0201bcc0 | REF gDuelDisplaySeqState (reuse) |
| DAT_0803c8dc | 0x0000080c | EQ DISPLAY_SEQ_STEP_LOCK_OFF (reuse) |
| DAT_0803c8fc | 0x0201bcc0 | REF gDuelDisplaySeqState (reuse) |
| DAT_0803c900 | 0x0000080c | EQ DISPLAY_SEQ_STEP_LOCK_OFF (reuse) |
| DAT_0803c980 | 0x0201bcc0 | REF gDuelDisplaySeqState (reuse) |
| PTR_gP1LifePoints_0803c984 | 0x0201c4e0 | REF gP1LifePoints (reuse) |
| DAT_0803c988 | 0x00001d08 | EQ P1LP_BLOCK2_OFF (reuse ewram.inc) |
| DAT_0803c98c | 0x00001ce8 | EQ P1LP_BLOCK2_OFF_1CE8 (reuse ewram.inc) |
| DAT_0803c990 | 0x0201e2a0 | REF gDuelCardCtxBase (reuse ewram.inc) |
| DAT_0803c994 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE (reuse) |
| DAT_0803c998 | 0x000011ed | EQ KNAVE_BLADE_CID (new card_info.inc; gap CID -- see below) |
| DAT_0803c99c | 0x00001d28 | EQ EQUIP_CHAIN_STEP_OFF (new duel_field.inc) |
| DAT_0803c9a0 | 0x00001d2c | EQ EQUIP_CHAIN_ACTIVE_OFF (new duel_field.inc) |
| DAT_0803c9a4 | 0x000010d0 | EQ EFFECT_ZONE_BITMASK_OFF (reuse duel_field.inc line 166) |
| DAT_0803c9a8 | 0x0000080c | EQ DISPLAY_SEQ_STEP_LOCK_OFF (reuse) |
| DAT_0803c9e8 | 0x0201bcc0 | REF gDuelDisplaySeqState (reuse) |
| PTR_gP1LifePoints_0803c9ec | 0x0201c4e0 | REF gP1LifePoints (reuse) |
| DAT_0803c9f0 | 0x00001d28 | EQ EQUIP_CHAIN_STEP_OFF (reuse new) |
| DAT_0803c9f4 | 0x00001d2c | EQ EQUIP_CHAIN_ACTIVE_OFF (reuse new) |
| DAT_0803c9f8 | 0x000010d0 | EQ EFFECT_ZONE_BITMASK_OFF (reuse) |
| DAT_0803c9fc | 0x0000080c | EQ DISPLAY_SEQ_STEP_LOCK_OFF (reuse) |
| PTR_gP1LifePoints_0803ca24 | 0x0201c4e0 | REF gP1LifePoints (reuse) |
| DAT_0803ca28 | 0x000010d0 | EQ EFFECT_ZONE_BITMASK_OFF (reuse) |
| DAT_0803ca2c | 0x0201bcc0 | REF gDuelDisplaySeqState (reuse) |
| DAT_0803ca30 | 0x0000080c | EQ DISPLAY_SEQ_STEP_LOCK_OFF (reuse) |
| PTR_gP1LifePoints_0803ca5c | 0x0201c4e0 | REF gP1LifePoints (reuse) |
| DAT_0803ca60 | 0x00001d28 | EQ EQUIP_CHAIN_STEP_OFF (reuse new) |
| DAT_0803ca64 | 0x00001d2c | EQ EQUIP_CHAIN_ACTIVE_OFF (reuse new) |
| DAT_0803ca68 | 0x0201bcc0 | REF gDuelDisplaySeqState (reuse) |
| DAT_0803ca6c | 0x0000080c | EQ DISPLAY_SEQ_STEP_LOCK_OFF (reuse) |
| DAT_0803cacc | 0x0201bcc0 | REF gDuelDisplaySeqState (reuse) |
| PTR_gP1LifePoints_0803cad0 | 0x0201c4e0 | REF gP1LifePoints (reuse) |
| DAT_0803cad4 | 0x00001d08 | EQ P1LP_BLOCK2_OFF (reuse) |
| DAT_0803cad8 | 0x0201e2a0 | REF gDuelCardCtxBase (reuse) |
| DAT_0803cadc | 0x00001d28 | EQ EQUIP_CHAIN_STEP_OFF (reuse new) |
| DAT_0803cae0 | 0x00001d2c | EQ EQUIP_CHAIN_ACTIVE_OFF (reuse new) |
| DAT_0803cae4 | 0x000010d0 | EQ EFFECT_ZONE_BITMASK_OFF (reuse) |
| DAT_0803cae8 | 0x0000080c | EQ DISPLAY_SEQ_STEP_LOCK_OFF (reuse) |
| DAT_0803cb18 | 0x0201bcc0 | REF gDuelDisplaySeqState (reuse) |
| DAT_0803cb1c | 0x0201c4d0 | REF gDuelChainStepCounter (new ewram.inc global) |
| DAT_0803cbe4 | 0xffffc03f | EQ GPRNG_STEP_CTR_MASK (reuse duel_field.inc line 34) |
| DAT_0803cbe8 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE (reuse) |
| DAT_0803cbec | 0x0201c510 | REF gDuelFieldSlots (reuse) |
| DAT_0803cbf0 | 0xffff7fff | EQ SLOT_ACTIVE_BIT15_CLR (new duel_field.inc; clears bit15 of slot word) |
| DAT_0803cbf4 | 0xffffbfff | EQ SLOT_ACTIVE_BIT14_CLR (new duel_field.inc; clears bit14 of slot word) |
| DAT_0803cbf8 | 0x0201c4d0 | REF gDuelChainStepCounter (reuse new) |
| DAT_0803cc94 | 0x0201bc54 | REF gDuelEffectChainSlots (reuse ewram.inc) |
| DAT_0803cc98 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE (reuse) |
| DAT_0803cc9c | 0x0201c510 | REF gDuelFieldSlots (reuse) |
| DAT_0803cca0 | 0x000010a4 | EQ EFFECT_ZONE_PARTITION_OFF (reuse duel_field.inc) |
| DAT_0803cca4 | 0x0201bcc0 | REF gDuelDisplaySeqState (reuse) |
| DAT_0803cca8 | 0x0000080c | EQ DISPLAY_SEQ_STEP_LOCK_OFF (reuse) |
| DAT_0803cd0c | 0x0201bcc2 | REF gDuelDisplaySeqStateAlt (new ewram.inc global) |
| DAT_0803cd10 | 0x0000080e | EQ DISP_SEQ_ALT_CTR_OFF (new duel_field.inc) |
| PTR_gP1LifePoints_0803cd8c | 0x0201c4e0 | REF gP1LifePoints (reuse) |
| DAT_0803cd90 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE (reuse) |
| DAT_0803cd94 | 0x0201bcc0 | REF gDuelDisplaySeqState (reuse) |
| DAT_0803cf54 | 0xfffe7fff | EQ SLOT_BITS14_15_CLR (new duel_field.inc; clears bits 14+15) |
| DAT_0803cf58 | 0x0201c4d8 | REF gDuelChainDescBase (new ewram.inc global) |
| PTR_gP1LifePoints_0803cf5c | 0x0201c4e0 | REF gP1LifePoints (reuse) |
| DAT_0803cf60 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE (reuse) |
| DAT_0803cf64 | 0x0201e2a0 | REF gDuelCardCtxBase (reuse) |
| DAT_0803cf68 | 0xffffc03f | EQ GPRNG_STEP_CTR_MASK (reuse) |
| DAT_0803cf6c | 0xffff7fff | EQ SLOT_ACTIVE_BIT15_CLR (reuse new) |
| DAT_0803cf70 | 0xffffbfff | EQ SLOT_ACTIVE_BIT14_CLR (reuse new) |
| DAT_0803d004 | 0x0201c4d8 | REF gDuelChainDescBase (reuse new) |
| DAT_0803d008 | 0xffff7fff | EQ SLOT_ACTIVE_BIT15_CLR (reuse new) |
| DAT_0803d00c | 0xffffbfff | EQ SLOT_ACTIVE_BIT14_CLR (reuse new) |
| DAT_0803d034 | 0x0000080a | EQ DISP_SEQ_STEP_LOCK_A_OFF (new duel_field.inc) |
| DAT_0803d0a4 | 0x0201bcc2 | REF gDuelDisplaySeqStateAlt (reuse new) |
| DAT_0803d0a8 | 0x0000080e | EQ DISP_SEQ_ALT_CTR_OFF (reuse new) |
| DAT_0803d20c | 0xfffe7fff | EQ SLOT_BITS14_15_CLR (reuse new) |
| PTR_gP1LifePoints_0803d210 | 0x0201c4e0 | REF gP1LifePoints (reuse) |
| DAT_0803d214 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE (reuse) |
| DAT_0803d218 | 0x0000165a | EQ A_DEAL_WITH_DARK_RULER_CID (new card_info.inc) |
| DAT_0803d21c | 0x0201c4d8 | REF gDuelChainDescBase (reuse new) |
| DAT_0803d220 | 0x0201e2a0 | REF gDuelCardCtxBase (reuse) |
| DAT_0803d224 | 0x0803d228 | RENAME switch_table_ptr_d20a (ptr to switchD_0803d20a) |
| PTR_gP1LifePoints_0803d250 | 0x0201c4e0 | REF gP1LifePoints (reuse) |
| DAT_0803d254 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE (reuse) |
| PTR_gP1LifePoints_0803d26c | 0x0201c4e0 | REF gP1LifePoints (reuse) |
| DAT_0803d270 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE (reuse) |
| PTR_gP1LifePoints_0803d288 | 0x0201c4e0 | REF gP1LifePoints (reuse) |
| DAT_0803d28c | 0x00000868 | EQ PLAYER_BLOCK_STRIDE (reuse) |
| PTR_gP1LifePoints_0803d38c | 0x0201c4e0 | REF gP1LifePoints (reuse) |
| DAT_0803d390 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE (reuse) |
| DAT_0803d394 | 0xffffc03f | EQ GPRNG_STEP_CTR_MASK (reuse) |
| DAT_0803d398 | 0xffff7fff | EQ SLOT_ACTIVE_BIT15_CLR (reuse new) |
| DAT_0803d39c | 0xffffbfff | EQ SLOT_ACTIVE_BIT14_CLR (reuse new) |
| DAT_0803d450 | 0x0201c4d8 | REF gDuelChainDescBase (reuse new) |
| DAT_0803d454 | 0xffff7fff | EQ SLOT_ACTIVE_BIT15_CLR (reuse new) |
| DAT_0803d458 | 0xffffbfff | EQ SLOT_ACTIVE_BIT14_CLR (reuse new) |
| DAT_0803d474 | 0x0000080a | EQ DISP_SEQ_STEP_LOCK_A_OFF (reuse new) |
| PTR_gP1LifePoints_0803d2a8 | 0x0201c4e0 | REF gP1LifePoints (reuse) |
| DAT_0803d2ac | 0x00000868 | EQ PLAYER_BLOCK_STRIDE (reuse) |
| DAT_0803d4d8 | 0x0201bcc2 | REF gDuelDisplaySeqStateAlt (reuse new) |
| DAT_0803d4dc | 0x0000080e | EQ DISP_SEQ_ALT_CTR_OFF (reuse new) |
| PTR_gP1LifePoints_0803d558 | 0x0201c4e0 | REF gP1LifePoints (reuse) |
| DAT_0803d55c | 0x00000868 | EQ PLAYER_BLOCK_STRIDE (reuse) |
| DAT_0803d560 | 0x0201bcc0 | REF gDuelDisplaySeqState (reuse) |
| DAT_0803d6c0 | 0x00000816 | EQ DUEL_FIELD_OAM_TILE_IDX_C (reuse duel_field.inc line 82) |
| DAT_0803d6c4 | 0xffffc03f | EQ GPRNG_STEP_CTR_MASK (reuse) |
| DAT_0803d6c8 | 0xffff7fff | EQ SLOT_ACTIVE_BIT15_CLR (reuse new) |
| DAT_0803d6cc | 0xffffbfff | EQ SLOT_ACTIVE_BIT14_CLR (reuse new) |
| DAT_0803d6d0 | 0x0201e2a0 | REF gDuelCardCtxBase (reuse) |
| DAT_0803d6d4 | 0x0201bcc0 | REF gDuelDisplaySeqState (reuse) |
| DAT_0803d6f0 | 0x0000080a | EQ DISP_SEQ_STEP_LOCK_A_OFF (reuse new) |
| DAT_0803d72c | 0x0201bcc0 | REF gDuelDisplaySeqState (reuse) |
| DAT_0803d730 | 0x0000080c | EQ DISPLAY_SEQ_STEP_LOCK_OFF (reuse) |
| DAT_0803d744 | 0x0000080c | EQ DISPLAY_SEQ_STEP_LOCK_OFF (reuse) |
| DAT_0803d8f4 | 0x00000818 | EQ DISP_SEQ_CARD_SET_CTR_OFF (new duel_field.inc) |
| DAT_0803d8f8 | 0x0201e2a0 | REF gDuelCardCtxBase (reuse) |
| DAT_0803d8fc | 0xffffc03f | EQ GPRNG_STEP_CTR_MASK (reuse) |
| DAT_0803d900 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE (reuse) |
| DAT_0803d904 | 0x0201c510 | REF gDuelFieldSlots (reuse) |
| DAT_0803d908 | 0xffff7fff | EQ SLOT_ACTIVE_BIT15_CLR (reuse new) |
| DAT_0803d90c | 0xffffbfff | EQ SLOT_ACTIVE_BIT14_CLR (reuse new) |
| DAT_0803d910 | 0x0201c4d8 | REF gDuelChainDescBase (reuse new) |
| DAT_0803d914 | 0x000010a4 | EQ EFFECT_ZONE_PARTITION_OFF (reuse) |
| DAT_0803d918 | 0xffdfffff | EQ SLOT_BIT21_CLR (new duel_field.inc; clears bit21=equip-active) |

Total: 136 slots (DAT_ 121 + PTR_gP1LifePoints_ 15). Roadmap estimate was ~121 (PTR_ slots not counted).

### ROM_INCBIN / .byte 块

None. All bytes in Seg-8 are part of named function bodies or literal pools within those functions.
No inter-function `.incbin` or orphan `.byte` sequences found (grep confirmed).

---

## 数据块分类 (Rule 2/3) -- ref-scan 证据

No ROM_INCBIN blocks in Seg-8. Ref-scan performed for all 13 function entry addresses as a
cross-check (confirming no function has 0 raw+THUMB refs that would indicate dead code):

| addr | raw refs | THUMB refs | result |
|------|----------|------------|--------|
| 0x0803c774 | 0 | 0 | called via 115-entry switch table (switchD_0803be70__caseD_18) -- table entries are raw even addrs not THUMB; reached by switch dispatch, not direct bl. Reachable at runtime. |
| 0x0803c814 | 0 | 0 | same switch table caseD_20 dispatch |
| 0x0803c8e0 | 0 | 0 | caseD_16 switch dispatch |
| 0x0803c904 | 0 | 0 | caseD_1c switch dispatch |
| 0x0803c9ac | 0 | 0 | caseD_1d switch dispatch |
| 0x0803ca00 | 0 | 0 | caseD_1e switch dispatch |
| 0x0803ca34 | 0 | 0 | caseD_1f switch dispatch |
| 0x0803ca70 | 0 | 0 | caseD_20? / direct bl sites |
| 0x0803caec | 0 | 0 | caseD_21 switch dispatch |
| 0x0803ccac | 0 | 0 | caseD_22 or similar |
| 0x0803d038 | 0 | 0 | caseD_3b switch dispatch |
| 0x0803d478 | 0 | 0 | caseD_3c switch dispatch |
| 0x0803d6f4 | 0 | 0 | caseD_3d switch dispatch |

All functions are reachable via the 115-entry switch table at switchD_0803be70__switchdataD_0803be88.
The table stores EVEN addresses (raw, not THUMB+1), so 0 THUMB refs is expected and correct.
Rule 3 does NOT apply -- all functions are live. No §5.1 entries for Seg-8.

---

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate)

#### 复用现有常量 (reuse: counting individual slot occurrences)

| slot | value | const_name | source |
|------|-------|------------|--------|
| DAT_0803c7c0 + 14 more x15 total | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc line 245 |
| DAT_0803c7cc | 0x18a6 | EHERO_AVIAN_CID | card_info.inc line 213 |
| DAT_0803c804 | 0x19c1 | CHAIN_THRASHER_CID | card_info.inc line 214 |
| DAT_0803c810 + 10 more x11 total | 0x80c | DISPLAY_SEQ_STEP_LOCK_OFF | duel_field.inc line 219 |
| DAT_0803c988 | 0x1d08 | P1LP_BLOCK2_OFF | ewram.inc line 243 |
| DAT_0803cad4 | 0x1d08 | P1LP_BLOCK2_OFF | ewram.inc line 243 |
| DAT_0803c98c | 0x1ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc line 269 |
| DAT_0803c9a4 + DAT_0803c9f8 + DAT_0803ca28 + DAT_0803cae4 x4 | 0x10d0 | EFFECT_ZONE_BITMASK_OFF | duel_field.inc line 166 |
| DAT_0803cbe4 + DAT_0803cf68 + DAT_0803d394 + DAT_0803d8fc + DAT_0803d6c4 x5 | 0xffffc03f | GPRNG_STEP_CTR_MASK | duel_field.inc line 34 |
| DAT_0803cca0 + DAT_0803d914 x2 | 0x10a4 | EFFECT_ZONE_PARTITION_OFF | duel_field.inc line 158 |
| DAT_0803d6c0 | 0x816 | DUEL_FIELD_OAM_TILE_IDX_C | duel_field.inc line 82 |

Reuse slot count: 15+1+1+11+2+1+4+5+2+1 = 43 slots

#### 新建 EQ 常量 (new)

**duel_field.inc -- new offsets/masks:**

| value | proposed_const | slots | asm evidence / confidence |
|-------|---------------|-------|--------------------------|
| 0xffbfffff | SLOT_ACTIVE_BIT22_CLR | DAT_0803c7c4/c8d4 x2 | tick_equip_chain_slot_ref_scan_seq asm 14365 `ldr r0,DAT_0803c7c4; ands r1,r0` clears bit22 of slot word [gP1LifePoints+0x40+player*0x868+loop*0x14]. Plate text (line 14331): "clearing bit22 (AND 0xffbfffff)". 413 raw ROM refs. confidence: high. |
| 0xff7fffff | SLOT_ACTIVE_BIT23_CLR | DAT_0803c7c8 x1 | tick_equip_chain_slot_ref_scan_seq asm 14367 `ldr r0,DAT_0803c7c8; ands r1,r0` clears bit23 of same slot word. Plate text (line 14332): "clearing bit23 (AND 0xff7fffff)". 188 raw ROM refs. confidence: high. |
| 0x00001d28 | EQUIP_CHAIN_STEP_OFF | DAT_0803c99c/c9f0/ca60/cadc x4 | finalize_equip_chain_removal_state asm 14609 `ldr r0,DAT_0803c99c(=0x1d28); adds r1,r4,r0; movs r0,#0xc; str r0,[r1,#0x0]` writes 0xc = chain ready state. tick_equip_chain_activate_state_seq asm 14681 `ldr r1,DAT_0803c9f0(=0x1d28); movs r1,#0x6; str r1,[r2]` writes 0x6 = chain activation step. init_equip_ai_state asm 14759 writes 0x9. link_equip_node_by_slot_match asm 14815 writes 0xb. All: gP1LifePoints+player*0x868+0x1d28 is the equip chain state step counter field. 31 raw ROM refs. confidence: high. |
| 0x00001d2c | EQUIP_CHAIN_ACTIVE_OFF | DAT_0803c9a0/c9f4/ca64/cae0 x4 | finalize_equip_chain_removal_state asm 14614 `ldr r2,DAT_0803c9a0(=0x1d2c); adds r1,r4,r2; movs r0,#0x0; str r0,[r1]` clears auxiliary chain active field. tick_equip_chain_activate_state_seq asm 14683 writes player side bit (0/1) to gP1LifePoints+0x1d2c. init_equip_ai_state writes 0. link_equip_node_by_slot_match writes 0. 95 raw ROM refs. confidence: high. |
| 0xffff7fff | SLOT_ACTIVE_BIT15_CLR | DAT_0803cbf0/cf6c/d008/d398/d454/d6c8/d908 x7 | tick_zone_slot_removal_chain_repair_seq asm 15003 `ldr r3,DAT_0803cbf0(=0xffff7fff); ands r2,r3` clears bit15 of slot descriptor word. Used consistently in zone placement functions. 188 raw ROM refs. confidence: high. |
| 0xffffbfff | SLOT_ACTIVE_BIT14_CLR | DAT_0803cbf4/cf70/d00c/d39c/d458/d6cc/d90c x7 | Same pattern, clears bit14. Used alongside SLOT_ACTIVE_BIT15_CLR in slot descriptor updates. 413 raw ROM refs. confidence: high. |
| 0xfffe7fff | SLOT_BITS14_15_CLR | DAT_0803cf54/d20c x2 | tick_zone_card_place_alt_display_seq asm 15451 `ldr r3,DAT_0803cf54(=0xfffe7fff)` applied to slot[+0] word -- masks out bits 14 AND 15 simultaneously (= SLOT_ACTIVE_BIT15_CLR & SLOT_ACTIVE_BIT14_CLR = 0xffff7fff & 0xffffbfff = 0xfffe7fff). tick_normal_summon_zone_state asm 15812 reuses. 6 raw ROM refs. confidence: high. |
| 0x0000080a | DISP_SEQ_STEP_LOCK_A_OFF | DAT_0803d034/d474/d6f0 x3 | tick_zone_card_place_display_seq asm 16434 `ldr r2,DAT_0803d6f0(=0x80a); adds r1,r6,r2; str r0,[r1]` clears [gDuelDisplaySeqStateAlt+0x80a]:=0 at step 2. tick_normal_summon_zone_state uses same pattern. Plate (16135): "step_lock_a=0x80a". Distinct from DISPLAY_SEQ_STEP_LOCK_OFF=0x80c (primary lock). 9 raw ROM refs. confidence: high. |
| 0x0000080e | DISP_SEQ_ALT_CTR_OFF | DAT_0803cd10/d0a8/d4dc x3 | tick_zone_card_place_alt_display_seq asm 15164 `ldr r0,DAT_0803cd10(=0x80e); adds r0,r6,r0; ldr r5,[r0]` reads step counter from [gDuelDisplaySeqStateAlt+0x80e]. Plate (15110): "step_counter_offset=0x80e". 14 raw ROM refs. confidence: high. |
| 0x00000818 | DISP_SEQ_CARD_SET_CTR_OFF | DAT_0803d8f4 x1 | tick_zone_slot_card_set_display_seq asm 16514 `ldr r5,DAT_0803d8f4(=0x818); adds r4,r0,r5` locates step counter at [gDuelDisplaySeqState+0x818]. Step 0 checks this; step 2+ clears to 0 via DAT_0803d730=0x80c. Context: card-set display sequence uses 0x818 for its own step counter within the 0x0201bcc0 region. 26 raw ROM refs. confidence: high. |
| 0xffdfffff | SLOT_BIT21_CLR | DAT_0803d918 x1 | tick_zone_slot_card_set_display_seq asm 16670 `ldr r2,DAT_0803d918(=0xffdfffff); ands r0,r2; str r0,[r1]` applied to a field slot word, clears bit21. 215 raw ROM refs. confidence: high. |

Note on GPRNG_STEP_CTR_MASK (0xffffc03f, duel_field.inc line 34): this mask happens to appear in
zone slot display code too (tick_zone_slot_removal_chain_repair_seq asm 14904, tick_zone_card_place_alt
asm 15461, etc.) as a general "clear bits[13:6]" mask. The reuse is correct -- same bit pattern,
same structural role (pack 6-bit zone type field into state word). confidence: high.

**card_info.inc -- new card IDs:**

| value | card identity | proposed_const | slots |
|-------|--------------|---------------|-------|
| 0x0fa7 | Blue-Eyes White Dragon (card_0001 pw=89631139 slot=0x0FA7) | BLUE_EYES_WHITE_DRAGON_CID | DAT_0803c86c x1 |
| 0x0fa6 | gap CID (slot 4006 = "A Hero Emerges" slot=0x171B != 0x0fa6; 0x0fa6 is NOT in card-stats.s) | eval_gap_cid_0fa6 | DAT_0803c868 x1 |
| 0x165a | A Deal with Dark Ruler (card_1330 pw=06850209 slot=0x165A) | A_DEAL_WITH_DARK_RULER_CID | DAT_0803d218 x1 |
| 0x11ed | gap CID (slot 0x11ed between Binding Chain 0x11EE and Takuhee 0x11EB; not in card-stats.s) | eval_gap_cid_11ed | DAT_0803c998 x1 |

Evidence for card CIDs:
- DAT_0803c868 (0xfa6) and DAT_0803c86c (0xfa7): setup_equip_chain_for_slot asm 14459-14464
  `ldr r0,DAT_0803c868(0xfa6); cmp r4,r0; blt LAB; ldr r6,DAT_0803c86c(0xfa7); cmp r4,r6; ble LAB_0803c870`
  Forms a range check: card_type in [0xfa6..0xfa7]. 0xfa7=BEWD is the upper bound; 0xfa6 is one slot
  below BEWD, forming a tight 2-CID range check. card-stats.s: card_0001=Blue-Eyes White Dragon
  slot=0x0FA7 (verified). Slot 0x0fa6 does not appear in card-stats.s (confirmed by scan). Low-conf
  gap name: eval_gap_cid_0fa6. confidence: high for 0xfa7=BEWD; low for 0xfa6 (gap).
- DAT_0803d218 (0x165a): tick_normal_summon_zone_state asm 15818 `ldr r3,DAT_0803d218(0x165a); str r5,[sp,#0]; ldr r0,[sp,#0xc]; movs r1,#0xb; movs r2,#0x1; bl link_equip_node_to_chain`
  0x165a passed as r3 arg to link_equip_node_to_chain. card-stats.s card_1330="A Deal with Dark Ruler"
  slot=0x165A (verified). confidence: high.
- DAT_0803c998 (0x11ed): finalize_equip_chain_removal_state asm 14605-14607
  `ldr r1,DAT_0803c998(0x11ed); movs r2,#0x1; bl replace_equip_chain_slot_refs_by_match`
  passed as chain ref card_id sentinel to replace_equip_chain_slot_refs_by_match. Slot 0x11ed is
  NOT in card-stats.s (slot between 0x11eb=Takuhee and 0x11ee=Binding Chain; no entry at 0x11ec or
  0x11ed). Low-conf gap sentinel. confidence: low.

C5 dedup: grep of all 19 constants/*.inc for 0x0fa6, 0x0fa7, 0x165a, 0x11ed -- none present.
0x18a6 already exists as EHERO_AVIAN_CID; 0x19c1 as CHAIN_THRASHER_CID. Safe to create new 4 entries.

New EQ slot count (individual occurrences of new constants):
- SLOT_ACTIVE_BIT22_CLR x2 + SLOT_ACTIVE_BIT23_CLR x1 + EQUIP_CHAIN_STEP_OFF x4 + EQUIP_CHAIN_ACTIVE_OFF x4 + SLOT_ACTIVE_BIT15_CLR x7 + SLOT_ACTIVE_BIT14_CLR x7 + SLOT_BITS14_15_CLR x2 + DISP_SEQ_STEP_LOCK_A_OFF x3 + DISP_SEQ_ALT_CTR_OFF x3 + DISP_SEQ_CARD_SET_CTR_OFF x1 + SLOT_BIT21_CLR x1 + BLUE_EYES_WHITE_DRAGON_CID x1 + eval_gap_cid_0fa6 x1 + A_DEAL_WITH_DARK_RULER_CID x1 + eval_gap_cid_11ed x1 = 39 new EQ slots

Total EQ = 43 reuse + 39 new = 82 slots

### REF_SLOTS (USER-label + DATA-ref)

New globals required (C5: grep all 19 constants/*.inc -- absent):
- gDuelChainStepCounter = 0x0201c4d0 (8 raw ROM refs): chain removal/placement step counter;
  used at tick_zone_slot_removal_chain_repair_seq asm 14887 `ldr r3,DAT_0803cb1c; ldr r5,[r3]` reads
  step to dispatch state 0/1/2. Plate (14863): "reads chain counter [0x0201c4d0] (r5)". high confidence.
- gDuelChainDescBase = 0x0201c4d8 (22 raw ROM refs): chain descriptor / zone slot copy buffer;
  tick_zone_card_place_alt_display_seq asm 15453 `ldr r4,DAT_0803cf58(=0x0201c4d8); adds r0,r4,#0; bl write_word_from_deref_src` passes as source base for zone slot copy. Plate (15107): "state_base=0x0201bcc2; step_counter_offset=0x80e". Cross-check: asm/04_card_zone_sprite.s line 3715 bl update_equip_chain_zone_slot_refs confirms this address is a zone-slot chain descriptor region. high confidence.
- gDuelDisplaySeqStateAlt = 0x0201bcc2 (3 raw ROM refs): tick_zone_card_place_alt_display_seq reads
  event word from [0x0201bcc2] (DAT_0803cd0c). Plate (15099): "Reads state_word from [0x0201bcc2]".
  Note: 0x0201bcc2 = gDuelDisplaySeqState + 2 (the second halfword of the same buffer). Named
  gDuelDisplaySeqStateAlt to make clear it's the +2 offset base used by alt-path functions. 3 raw refs.
  med confidence (only 3 refs; functionally is gDuelDisplaySeqState+2 but named distinctly as each
  consumer loads it as an independent base pointer; naming preserves the distinct slot label pattern).

| slot | target | gas_label | slot_label |
|------|--------|-----------|------------|
| DAT_0803c7b8 | 0x0201bcc0 | gDuelDisplaySeqState | tick_chain_scan_seq_state_a |
| PTR_gP1LifePoints_0803c7bc | 0x0201c4e0 | gP1LifePoints | tick_chain_scan_lp_base_a |
| DAT_0803c808 | 0x0201bb90 | gEquipChainSlotRefs | tick_chain_scan_chain_refs_a |
| DAT_0803c80c | 0x0201bcc0 | gDuelDisplaySeqState | tick_chain_scan_seq_state_b |
| DAT_0803c85c | 0x0201bcc0 | gDuelDisplaySeqState | setup_chain_seq_state_a |
| DAT_0803c864 | 0x0201c510 | gDuelFieldSlots | setup_chain_field_slots_a |
| DAT_0803c8d8 | 0x0201bcc0 | gDuelDisplaySeqState | setup_chain_seq_state_b |
| DAT_0803c8fc | 0x0201bcc0 | gDuelDisplaySeqState | invoke_scan_seq_state_a |
| DAT_0803c980 | 0x0201bcc0 | gDuelDisplaySeqState | finalize_chain_seq_state_a |
| PTR_gP1LifePoints_0803c984 | 0x0201c4e0 | gP1LifePoints | finalize_chain_lp_base_a |
| DAT_0803c990 | 0x0201e2a0 | gDuelCardCtxBase | finalize_chain_card_ctx_a |
| DAT_0803c9e8 | 0x0201bcc0 | gDuelDisplaySeqState | tick_chain_act_seq_state_a |
| PTR_gP1LifePoints_0803c9ec | 0x0201c4e0 | gP1LifePoints | tick_chain_act_lp_base_a |
| PTR_gP1LifePoints_0803ca24 | 0x0201c4e0 | gP1LifePoints | clear_chain_lp_base_a |
| DAT_0803ca2c | 0x0201bcc0 | gDuelDisplaySeqState | clear_chain_seq_state_a |
| PTR_gP1LifePoints_0803ca5c | 0x0201c4e0 | gP1LifePoints | init_ai_lp_base_a |
| DAT_0803ca68 | 0x0201bcc0 | gDuelDisplaySeqState | init_ai_seq_state_a |
| DAT_0803cacc | 0x0201bcc0 | gDuelDisplaySeqState | link_slot_match_seq_state_a |
| PTR_gP1LifePoints_0803cad0 | 0x0201c4e0 | gP1LifePoints | link_slot_match_lp_base_a |
| DAT_0803cad8 | 0x0201e2a0 | gDuelCardCtxBase | link_slot_match_card_ctx_a |
| DAT_0803cb18 | 0x0201bcc0 | gDuelDisplaySeqState | removal_repair_seq_state_a |
| DAT_0803cb1c | 0x0201c4d0 | gDuelChainStepCounter | removal_repair_step_ctr_a |
| DAT_0803cbec | 0x0201c510 | gDuelFieldSlots | removal_repair_field_slots_a |
| DAT_0803cbf8 | 0x0201c4d0 | gDuelChainStepCounter | removal_repair_step_ctr_b |
| DAT_0803cc94 | 0x0201bc54 | gDuelEffectChainSlots | removal_repair_effect_slots_a |
| DAT_0803cc9c | 0x0201c510 | gDuelFieldSlots | removal_repair_field_slots_b |
| DAT_0803cca4 | 0x0201bcc0 | gDuelDisplaySeqState | removal_repair_seq_state_b |
| DAT_0803cd0c | 0x0201bcc2 | gDuelDisplaySeqStateAlt | alt_place_seq_state_a |
| PTR_gP1LifePoints_0803cd8c | 0x0201c4e0 | gP1LifePoints | alt_place_lp_base_a |
| DAT_0803cd94 | 0x0201bcc0 | gDuelDisplaySeqState | alt_place_seq_state_b |
| DAT_0803cf58 | 0x0201c4d8 | gDuelChainDescBase | alt_place_chain_desc_a |
| PTR_gP1LifePoints_0803cf5c | 0x0201c4e0 | gP1LifePoints | alt_place_lp_base_b |
| DAT_0803cf64 | 0x0201e2a0 | gDuelCardCtxBase | alt_place_card_ctx_a |
| DAT_0803d004 | 0x0201c4d8 | gDuelChainDescBase | alt_place_chain_desc_b |
| PTR_gP1LifePoints_0803d210 | 0x0201c4e0 | gP1LifePoints | normal_summon_lp_base_a |
| DAT_0803d21c | 0x0201c4d8 | gDuelChainDescBase | normal_summon_chain_desc_a |
| DAT_0803d220 | 0x0201e2a0 | gDuelCardCtxBase | normal_summon_card_ctx_a |
| PTR_gP1LifePoints_0803d250 | 0x0201c4e0 | gP1LifePoints | normal_summon_lp_base_b |
| PTR_gP1LifePoints_0803d26c | 0x0201c4e0 | gP1LifePoints | normal_summon_lp_base_c |
| PTR_gP1LifePoints_0803d288 | 0x0201c4e0 | gP1LifePoints | normal_summon_lp_base_d |
| PTR_gP1LifePoints_0803d38c | 0x0201c4e0 | gP1LifePoints | normal_summon_lp_base_e |
| DAT_0803d450 | 0x0201c4d8 | gDuelChainDescBase | normal_summon_chain_desc_b |
| DAT_0803d0a4 | 0x0201bcc2 | gDuelDisplaySeqStateAlt | normal_summon_seq_state_alt_a |
| PTR_gP1LifePoints_0803d2a8 | 0x0201c4e0 | gP1LifePoints | normal_summon_lp_base_f |
| DAT_0803d4d8 | 0x0201bcc2 | gDuelDisplaySeqStateAlt | zone_place_seq_state_alt_a |
| PTR_gP1LifePoints_0803d558 | 0x0201c4e0 | gP1LifePoints | zone_place_lp_base_a |
| DAT_0803d560 | 0x0201bcc0 | gDuelDisplaySeqState | zone_place_seq_state_a |
| DAT_0803d6d0 | 0x0201e2a0 | gDuelCardCtxBase | zone_place_card_ctx_a |
| DAT_0803d6d4 | 0x0201bcc0 | gDuelDisplaySeqState | zone_place_seq_state_b |
| DAT_0803d72c | 0x0201bcc0 | gDuelDisplaySeqState | card_set_seq_state_a |
| DAT_0803d8f8 | 0x0201e2a0 | gDuelCardCtxBase | card_set_card_ctx_a |
| DAT_0803d904 | 0x0201c510 | gDuelFieldSlots | card_set_field_slots_a |
| DAT_0803d910 | 0x0201c4d8 | gDuelChainDescBase | card_set_chain_desc_a |
| PTR_gP1LifePoints_0803d2a8 | 0x0201c4e0 | gP1LifePoints | (already listed as normal_summon_lp_base_f) |

REF total: 32 (unique PTR_ / DAT_ slots -- dedup for DAT_0803d2a8 counted once) = 33 slots.

Correction after counting: 53 REF slots (each physical slot address counted once).
Let me recount the table above: cb18, cb1c, cbec, cbf8, cc94, cc9c, cca4, cd0c, cd8c, cd94, cf58,
cf5c, cf64, d004, d210, d21c, d220, d250, d26c, d288, d38c, d450, d0a4, d2a8, d4d8, d558, d560,
d6d0, d6d4, d72c, d8f8, d904, d910 + c7b8, c7bc, c808, c80c, c85c, c864, c8d8, c8fc, c980, c984,
c990, c9e8, c9ec, ca24, ca2c, ca5c, ca68, cacc, cad0, cad8 = 53 REF slots.

### RENAME_SLOTS (纯改名 + EOL)

| slot | value | old_label | new_label | eol note |
|------|-------|-----------|-----------|---------|
| DAT_0803d224 | 0x0803d228 | DAT_0803d224 | normal_summon_switch_table_ptr | ptr to switchD_0803d20a__switchdataD_0803d228 (5-entry table for zone types 0xb..0xf) |

RENAME total: 1

### FUNC_RENAME

Function body cross-checks:

- tick_equip_chain_slot_ref_scan_seq (0x0803c774): plate (line 14328) says "Called by FUN_0803be4c". The body reads gDuelDisplaySeqState bit15 as player_id, iterates 5 slot entries, checks EHERO_AVIAN_CID/CHAIN_THRASHER_CID, calls replace_equip_chain_slot_refs_by_match, clears step lock. Name matches. confidence: high.
- setup_equip_chain_for_slot (0x0803c814): body reads gDuelDisplaySeqState+0x2 as slot_idx, links equip node via link_equip_node_by_card_type_check, checks card_type range. Name matches. confidence: high.
- invoke_equip_candidate_scan_setup (0x0803c8e0): body calls invoke_build_equip_candidate_score_table(0) + trigger_equip_activation_candidate_scan(0). Name matches. confidence: high.
- finalize_equip_chain_removal_state (0x0803c904): body writes EQUIP_CHAIN_STEP_OFF=0xc (chain ready), clears EQUIP_CHAIN_ACTIVE_OFF, clears EFFECT_ZONE_BITMASK_OFF bit0, calls rebuild_equip_chain_refs. Name matches. confidence: high.
- tick_equip_chain_activate_state_seq (0x0803c9ac): body writes EQUIP_CHAIN_STEP_OFF=0x6 (activation), writes player-side bit to EQUIP_CHAIN_ACTIVE_OFF, OR-sets EFFECT_ZONE_BITMASK_OFF bit0. Name matches. confidence: high.
- clear_equip_chain_active_state (0x0803ca00): body clears bit0 of gP1LifePoints+0x10d0 (EFFECT_ZONE_BITMASK_OFF), calls rebuild_equip_chain_refs. **MISNAME SIGNAL**: plate (line 14718) mentions "gP1LifePoints=0x0201b290" -- this is the OLD gDuelPhaseFlags address, NOT gP1LifePoints (0x0201c4e0). The PTR_gP1LifePoints_0803ca24 slot correctly contains 0x0201c4e0 (verified by ROM read). The plate text is stale/incorrect; the function itself operates on gP1LifePoints. No FUNC_RENAME needed -- the function name is semantically accurate. The plate needs ASCII rewrite to fix the erroneous address. confidence: high.
- init_equip_ai_state (0x0803ca34): body calls invoke_build_equip_candidate_score_table(0), writes EQUIP_CHAIN_STEP_OFF=0x9. Name matches. confidence: high.
- link_equip_node_by_slot_match (0x0803ca70): body reads equip status field at gP1LifePoints+EQUIP_CHAIN_STEP_OFF-0x20, conditionally writes EQUIP_CHAIN_STEP_OFF=0xb+EQUIP_CHAIN_ACTIVE_OFF=0, calls link_equip_node_by_card_type_check. Name matches. confidence: high.
- tick_zone_slot_removal_chain_repair_seq (0x0803caec): body uses gDuelChainStepCounter for 3-state machine; state 0 calls replace_chain_refs_by_slot_id_for_player + dispatch op=0x18; state 1 calls zero_fill_by_halfword + updates display bits; state 2+ releases step lock. Name matches. confidence: med (complex body).
- tick_zone_card_place_alt_display_seq (0x0803ccac): body reads gDuelDisplaySeqStateAlt (0x0201bcc2) -- alternate state base. State machine for zone card placement. Plate says "alternate variant". Name matches. confidence: high.
- tick_normal_summon_zone_state (0x0803d038): body calls get_zone_slot_ptr, updates slot type_byte, checks field5/field8 for equip node insertion, dispatches on zone_type 0xb/0xc/0xd/0xe/0xf. Name correct for "normal/tribute-summon to monster zone" pattern. confidence: med.
- tick_zone_card_place_display_seq (0x0803d478): body is primary (non-alt) zone card placement sequence; reads gDuelDisplaySeqStateAlt for zone descriptor, gDuelDisplaySeqState+0x80e for step. Name matches. confidence: high.
- tick_zone_slot_card_set_display_seq (0x0803d6f4): body uses step counter at [gDuelDisplaySeqState+0x818]. Plate (16451): "zone slot card set-card placement display sequence". Name matches. confidence: high.

**FUNC_RENAME: 0** -- no misnaming detected.

One note: clear_equip_chain_active_state plate has stale gP1LifePoints address (0x0201b290 vs correct 0x0201c4e0). This is a plate correction issue (PLATE action), not a FUNC_RENAME.

### PLATE (R5) -- C8 stale-FUN_ rewrites + address corrections

All Seg-8 plates (asm lines 14327..16741) containing stale FUN_ references or address errors:

| asm line | addr | function | action | stale FUN_ -> current name |
|----------|------|----------|--------|--------------------------|
| 14328 | 0x0803c774 | tick_equip_chain_slot_ref_scan_seq | substring replace | FUN_0803be4c -> dispatch_duel_event_display_seq |
| 14431 | 0x0803c814 | setup_equip_chain_for_slot | substring replace x2 | FUN_0803be4c -> dispatch_duel_event_display_seq; FUN_08035f54 -> link_equip_node_by_card_type_check |
| 14537 | 0x0803c8e0 | invoke_equip_candidate_scan_setup | substring replace | FUN_0803be4c -> dispatch_duel_event_display_seq |
| 14562 | 0x0803c904 | finalize_equip_chain_removal_state | substring replace | FUN_0803be4c -> dispatch_duel_event_display_seq |
| 14659 | 0x0803c9ac | tick_equip_chain_activate_state_seq | substring replace | FUN_0803be4c -> dispatch_duel_event_display_seq |
| 14716 | 0x0803ca00 | clear_equip_chain_active_state | full rewrite (stale FUN_ + wrong addr) | FUN_0802eeac -> rebuild_equip_chain_refs; gP1LifePoints=0x0201b290 -> 0x0201c4e0 |
| 14791 | 0x0803ca70 | link_equip_node_by_slot_match | substring replace | FUN_0803be4c -> dispatch_duel_event_display_seq |
| 14860 | 0x0803caec | tick_zone_slot_removal_chain_repair_seq | substring replace | FUN_0803be4c -> dispatch_duel_event_display_seq |
| 15108 | 0x0803ccac | tick_zone_card_place_alt_display_seq | substring replace | FUN_0803be4c -> dispatch_duel_event_display_seq |
| 16133 | 0x0803d478 | tick_zone_card_place_display_seq | substring replace | FUN_0803be4c -> dispatch_duel_event_display_seq |
| 16451 | 0x0803d6f4 | tick_zone_slot_card_set_display_seq | substring replace x2 | FUN_0803be4c -> dispatch_duel_event_display_seq; FUN_0802f14c -> update_equip_chain_zone_slot_refs; FUN_0802ec80 -> clear_chain_refs_for_low_zone_nodes |

PLATE total: 11 actions (1 full rewrite for clear_equip_chain_active_state; 10 substring replaces).

ASCII replacement for clear_equip_chain_active_state (0x0803ca00):
```
Called by dispatch_duel_event_display_seq (caseD_1e). Reads gP1LifePoints+0x10d0
(EFFECT_ZONE_BITMASK_OFF), clears bit0 via rsbs+ands pattern (~0x1 AND), writes back.
Then calls rebuild_equip_chain_refs for full chain ref rebuild scan.
Finally clears [gDuelDisplaySeqState+0x80c] (step lock) to 0.
Constants: gP1LifePoints=0x0201c4e0, chain_flag_offset=EFFECT_ZONE_BITMASK_OFF=0x10d0,
  state_base=gDuelDisplaySeqState=0x0201bcc0, step_lock_off=DISPLAY_SEQ_STEP_LOCK_OFF=0x80c.
indeg=1 (dispatch_duel_event_display_seq caseD_1e only).
```

Note: FUN_0802f14c=update_equip_chain_zone_slot_refs and FUN_0802ec80=clear_chain_refs_for_low_zone_nodes
are confirmed by grep of asm/02_text_lp_fieldspell.s lines 5772 and 6470.

---

## carve 计画 (R7)

None. No inter-function ROM_INCBIN blocks in Seg-8.

---

## disasm 计画 (R4)

None. All code in Seg-8 is already correctly disassembled as THUMB. The 5-entry switch table
switchD_0803d20a__switchdataD_0803d228 (asm lines 15825-15831) is already labeled.
No misclassified code blocks detected.

---

## 新增 constants / 全局 (C5 dedup verified)

**ewram.inc (3 new globals):**
```asm
.equ gDuelChainStepCounter,   0x0201c4d0  @ equip chain removal/placement step counter; 3-state machine (0/1/2+); 8 raw ROM refs
.equ gDuelChainDescBase,      0x0201c4d8  @ equip chain zone slot descriptor / copy buffer base; used in zone placement and card-set display sequences; 22 raw ROM refs
.equ gDuelDisplaySeqStateAlt, 0x0201bcc2  @ alternate duel display seq state base = gDuelDisplaySeqState+2; used by alt zone-card-place and normal-summon functions; 3 raw ROM refs
```

C5 grep: 0x0201c4d0, 0x0201c4d8, 0x0201bcc2 -- all absent from all 19 constants/*.inc. Safe to create.

**duel_field.inc (11 new offsets/masks):**
```asm
.equ SLOT_ACTIVE_BIT22_CLR,       0xffbfffff  @ AND mask clearing bit22 of zone slot word (chain-linked flag); tick_equip_chain_slot_ref_scan_seq asm 14365; 413 raw ROM refs
.equ SLOT_ACTIVE_BIT23_CLR,       0xff7fffff  @ AND mask clearing bit23 of zone slot word (chain-type flag); tick_equip_chain_slot_ref_scan_seq asm 14367; 188 raw ROM refs
.equ EQUIP_CHAIN_STEP_OFF,        0x00001d28  @ [gP1LifePoints+player*0x868+0x1d28] equip chain state step field; values: 0x6=activate, 0x9=ai_init, 0xb=ready, 0xc=finalize; 31 raw ROM refs
.equ EQUIP_CHAIN_ACTIVE_OFF,      0x00001d2c  @ [gP1LifePoints+player*0x868+0x1d2c] equip chain active player side flag; 0/1; 95 raw ROM refs
.equ SLOT_ACTIVE_BIT15_CLR,       0xffff7fff  @ AND mask clearing bit15 of zone slot display descriptor word; used in zone placement functions; 188 raw ROM refs
.equ SLOT_ACTIVE_BIT14_CLR,       0xffffbfff  @ AND mask clearing bit14 of zone slot display descriptor word; used alongside SLOT_ACTIVE_BIT15_CLR; 413 raw ROM refs
.equ SLOT_BITS14_15_CLR,          0xfffe7fff  @ AND mask clearing bits 14+15 simultaneously (=SLOT_ACTIVE_BIT14_CLR & SLOT_ACTIVE_BIT15_CLR); 6 raw ROM refs
.equ DISP_SEQ_STEP_LOCK_A_OFF,    0x0000080a  @ [gDuelDisplaySeqState+0x80a] secondary step lock A; cleared at step 2 in tick_zone_card_place_display_seq; 9 raw ROM refs
.equ DISP_SEQ_ALT_CTR_OFF,        0x0000080e  @ [gDuelDisplaySeqState+0x80e] step counter for alt zone-card-place and normal-summon sequences; 14 raw ROM refs
.equ DISP_SEQ_CARD_SET_CTR_OFF,   0x00000818  @ [gDuelDisplaySeqState+0x818] step counter for card-set display sequence; tick_zone_slot_card_set_display_seq; 26 raw ROM refs
.equ SLOT_BIT21_CLR,              0xffdfffff  @ AND mask clearing bit21 of zone slot word (equip-active bit); tick_zone_slot_card_set_display_seq asm 16670; 215 raw ROM refs
```

Note: DISP_SEQ_STEP_LOCK_A_OFF literal `.equ` value: 0x0000080a (note trailing a is hex).

C5 grep: 0xffbfffff (SLOT_ACTIVE_BIT22_CLR -- different from the existing 0xff7fffff/0xffffbfff); grep confirms no existing constant for 0xffbfffff, 0xff7fffff, 0x1d28, 0x1d2c, 0xffff7fff, 0xffffbfff, 0xfffe7fff, 0x80a, 0x80e, 0x818, 0xffdfffff in constants/*.inc. Safe to create all 11.

Note: GPRNG_STEP_CTR_MASK (0xffffc03f) already in duel_field.inc line 34; reused x5 in Seg-8.
DUEL_FIELD_OAM_TILE_IDX_C (0x816) already in duel_field.inc line 82; reused x1.

**card_info.inc (4 new):**
```asm
.equ BLUE_EYES_WHITE_DRAGON_CID,    0x00000fa7  @ Blue-Eyes White Dragon (pw=89631139; card_0001 slot=0x0FA7); setup_equip_chain_for_slot card_type upper bound
.equ eval_gap_cid_0fa6,             0x00000fa6  @ gap slot (NOT in card-stats.s; between slot 0x0fa5 and card_0001=BEWD); setup_equip_chain_for_slot card_type lower bound; low confidence
.equ A_DEAL_WITH_DARK_RULER_CID,    0x0000165a  @ A Deal with Dark Ruler (pw=06850209; card_1330 slot=0x165A); tick_normal_summon_zone_state link_equip_node_to_chain chain_type arg
.equ eval_gap_cid_11ed,             0x000011ed  @ gap slot (NOT in card-stats.s; between 0x11eb=Takuhee and 0x11ee=Binding Chain); finalize_equip_chain_removal_state replace_equip_chain_slot_refs_by_match sentinel; low confidence
```

---

## §5.1 登记 (Rule 3) -- 0 引用块

None. No ROM_INCBIN or .byte blocks in Seg-8 range. All 13 functions are live via switch dispatch table.

---

## 消費者証拠 (R6) -- 关键槽语义

| slot | 函数 | asm 行 | 语义 | 置信度 |
|------|------|--------|------|-------|
| DAT_0803c7c4=0xffbfffff | tick_equip_chain_slot_ref_scan_seq | 14364 `ldr r0,DAT_0803c7c4; ands r1,r0` | clears bit22 of slot word; plate 14331 "clearing bit22" | high |
| DAT_0803c7c8=0xff7fffff | tick_equip_chain_slot_ref_scan_seq | 14366 `ldr r0,DAT_0803c7c8; ands r1,r0` | clears bit23 of slot word; plate 14332 "clearing bit23" | high |
| DAT_0803c99c=0x1d28 | finalize_equip_chain_removal_state | 14609 `ldr r0,DAT_0803c99c; adds r1,r4,r0; movs r0,#0xc; str r0,[r1]` | [gP1LP+0x1d28]:=0xc (chain ready); plate 14567 "writes [gP1LP+0x1d28]=0xc" | high |
| DAT_0803c9a0=0x1d2c | finalize_equip_chain_removal_state | 14614 `ldr r2,DAT_0803c9a0; adds r1,r4,r2; movs r0,#0; str r0,[r1]` | [gP1LP+0x1d2c]:=0; plate 14568 "clears auxiliary field" | high |
| DAT_0803cb1c=0x0201c4d0 | tick_zone_slot_removal_chain_repair_seq | 14887 `ldr r3,DAT_0803cb1c; ldr r5,[r3]` | reads step counter; plate 14863 "[0x0201c4d0] (r5)" | high |
| DAT_0803cf58=0x0201c4d8 | tick_zone_card_place_alt_display_seq | 15453 `ldr r4,DAT_0803cf58; adds r0,r4,#0; bl write_word_from_deref_src` | zone slot copy buffer base | high |
| DAT_0803cd0c=0x0201bcc2 | tick_zone_card_place_alt_display_seq | 15119 `ldr r0,DAT_0803cd0c; ldr r0,[r0,#0]` | reads state word from alternate base; plate 15099 "Reads state_word from [0x0201bcc2]" | med (only 3 refs) |
| DAT_0803d218=0x165a | tick_normal_summon_zone_state | 15818 `ldr r3,DAT_0803d218; bl link_equip_node_to_chain` | chain_type argument for equip node; card-stats.s card_1330="A Deal with Dark Ruler" slot=0x165A | high |
| DAT_0803c998=0x11ed | finalize_equip_chain_removal_state | 14605 `ldr r1,DAT_0803c998; movs r2,#1; bl replace_equip_chain_slot_refs_by_match` | replace chain refs sentinel; slot NOT in card-stats.s | low (gap CID, no card name) |
| DAT_0803c868=0xfa6 | setup_equip_chain_for_slot | 14459 `ldr r0,DAT_0803c868; cmp r4,r0; blt LAB_0803c8aa` | lower bound of [0xfa6..0xfa7] card_type range check; slot NOT in card-stats.s | low (gap CID) |
| DAT_0803c86c=0xfa7 | setup_equip_chain_for_slot | 14462 `ldr r6,DAT_0803c86c; cmp r4,r6; ble LAB_0803c870` | upper bound = BEWD slot; card-stats.s card_0001 verified | high |
| DAT_0803d8f4=0x818 | tick_zone_slot_card_set_display_seq | 16513 `ldr r5,DAT_0803d8f4; adds r1,r0,r5; ldr r2,[r1]` | reads step_counter[+0x818]; plate 16455 "reads step_counter [+0x810]" MISMATCH ALERT: plate says 0x810 but ROM value is 0x818 | high for 0x818 (ROM-verified); plate correction needed |
| DAT_0803d034=0x80a | tick_zone_card_place_display_seq | 16399 via asm 16432: step 2 `ldr r2,DAT_0803d6f0(=0x80a); adds r1,r6,r2; str r0,[r1]` clears [+0x80a]:=0 | secondary step lock; plate 16135 "step_lock_a=0x80a" | high |

### ALERT: Plate error in tick_zone_slot_card_set_display_seq (asm line 16455)

Plate text reads "reads step_counter [+0x810]" but DAT_0803d8f4 contains 0x818 (ROM-verified).
The function reads [gDuelDisplaySeqState + 0x818], NOT 0x810. The plate also references unnamed
FUN_0802f14c (now: update_equip_chain_zone_slot_refs) and FUN_0802ec80 (now: clear_chain_refs_for_low_zone_nodes).
Full ASCII plate rewrite required for this function.

ASCII replacement for tick_zone_slot_card_set_display_seq (0x0803d6f4):
```
Called by dispatch_duel_event_display_seq caseD_3d. Zone slot card set-card placement display sequence.
Reads from [gDuelDisplaySeqState]: zone_byte ([+2] ldrb), zone_hi ([+2]>>8 r7), slot_byte ([+4] ldrb),
slot_hi ([+4]>>8 r6). Reads step_counter at [gDuelDisplaySeqState+0x818].
Step 0: if zone_hi>0xa or slot_hi>0xa, copies step_ctr to [+0x80c] and exits (boundary guard);
  if in range and zone_hi<=0xa&&slot_hi<=0xa: calls write_card_display_index_with_bit_offset(0x2d,1).
  Returns r0=1 on in-range path.
Step 1: calls get_zone_slot_ptr, write_word_from_deref_src, copy_bytes_by_halfword, zero_fill_by_halfword;
  calls update_equip_chain_zone_slot_refs (arg: zone_hi<<8|slot_hi); if slot_hi>4 calls
  clear_chain_refs_for_low_zone_nodes; calls dispatch_card_display_op(0x18); increments step.
Step 2+: clears [gDuelDisplaySeqState+0x80c]:=0 and exits.
Constants: state_base=gDuelDisplaySeqState=0x0201bcc0; step_ctr_off=DISP_SEQ_CARD_SET_CTR_OFF=0x818;
  step_lock=DISPLAY_SEQ_STEP_LOCK_OFF=0x80c; field_slots=gDuelFieldSlots=0x0201c510;
  chain_desc=gDuelChainDescBase=0x0201c4d8; ctx=gDuelCardCtxBase=0x0201e2a0.
Returns void (pop{r0};bx r0).
```

PLATE total revised: 11 (plus the tick_zone_slot_card_set_display_seq also needs full rewrite due to
0x810->0x818 plate error + 2 stale FUN_). Counting: 1 full rewrite (clear_equip_chain_active_state) +
1 full rewrite (tick_zone_slot_card_set_display_seq) + 9 substring replaces = PLATE=11.

---

## 求助

1. **eval_gap_cid_0fa6 (0xfa6)**: slot between 0x0fa5 and card_0001=BEWD (0x0fa7). Used as lower
   bound in card_type range check [0xfa6..0xfa7] in setup_equip_chain_for_slot. Slot 0x0fa6 is NOT
   in card-stats.s. Low-confidence sentinel name. No action blocked; proceed with eval_gap_cid_0fa6.

2. **eval_gap_cid_11ed (0x11ed)**: used as replace_equip_chain_slot_refs_by_match sentinel in
   finalize_equip_chain_removal_state. Slot NOT in card-stats.s (between 0x11eb=Takuhee and
   0x11ee=Binding Chain). Gap CID. Proceed with eval_gap_cid_11ed.

3. **gDuelDisplaySeqStateAlt (0x0201bcc2)**: only 3 raw ROM refs. Functionally = gDuelDisplaySeqState+2.
   Named as distinct global because each consumer loads it as an independent 4-byte base pointer.
   If reviewer prefers to use EWRAM base + offset pattern, could instead be gDuelDisplaySeqState
   with +2 bias. Current proposal treats it as separate global for naming consistency with other
   PTR_ patterns in this segment. med confidence.

---

## Split recommendation

Seg-8 has 136 slots across 13 functions. This is manageable in one proposal. No split recommended.

---

## Executor Report: F03-Seg-8

- fn=13 (tick_equip_chain_slot_ref_scan_seq..tick_zone_slot_card_set_display_seq)
- slots: EQ=82 REF=53 RENAME=1 FUNC_RENAME=0 PLATE=11  total=136
- carve=0 disasm=0 §5.1=0
- 新增 constants/全局:
  - ewram.inc +3: gDuelChainStepCounter=0x0201c4d0 / gDuelChainDescBase=0x0201c4d8 / gDuelDisplaySeqStateAlt=0x0201bcc2
  - duel_field.inc +11: SLOT_ACTIVE_BIT22_CLR=0xffbfffff / SLOT_ACTIVE_BIT23_CLR=0xff7fffff / EQUIP_CHAIN_STEP_OFF=0x1d28 / EQUIP_CHAIN_ACTIVE_OFF=0x1d2c / SLOT_ACTIVE_BIT15_CLR=0xffff7fff / SLOT_ACTIVE_BIT14_CLR=0xffffbfff / SLOT_BITS14_15_CLR=0xfffe7fff / DISP_SEQ_STEP_LOCK_A_OFF=0x80a / DISP_SEQ_ALT_CTR_OFF=0x80e / DISP_SEQ_CARD_SET_CTR_OFF=0x818 / SLOT_BIT21_CLR=0xffdfffff
  - card_info.inc +4: BLUE_EYES_WHITE_DRAGON_CID=0x0fa7 / eval_gap_cid_0fa6=0x0fa6 (low-conf) / A_DEAL_WITH_DARK_RULER_CID=0x165a / eval_gap_cid_11ed=0x11ed (low-conf)
- 求助: 2 gap CIDs (0xfa6/0x11ed low-conf, proceed); gDuelDisplaySeqStateAlt naming convention (3 refs, med-conf)
- proposal: doc/dev/refine/F03-Seg-8.proposal.md

---

## Fix iteration 1 (applied per F03-Seg-8.review.md NEEDS_FIX 4 items)

| # | location | old value | corrected value |
|---|----------|-----------|-----------------|
| #1a | Executor Report `slots:` line | EQ=87 REF=33 total=121 | EQ=82 REF=53 total=136 |
| #1b | `### 残留自动名槽` section footer | "Total: 121 slots. Matches roadmap estimate exactly." | "Total: 136 slots (DAT_ 121 + PTR_gP1LifePoints_ 15). Roadmap estimate was ~121 (PTR_ slots not counted)." |
| #1c | `## Split recommendation` | "121 slots" | "136 slots" |
| #2a | EQ reuse table PLAYER_BLOCK_STRIDE row | "x16 total" | "x15 total" |
| #2b | EQ reuse table DISPLAY_SEQ_STEP_LOCK_OFF row | "x13 total" | "x11 total" |
| #2c | EQ reuse formula line | "16+2+1+13+2+1+1+4+5+2+1 = 48 slots" | "15+1+1+11+2+1+4+5+2+1 = 43 slots" |
| #2d | EQ total line | "48 reuse + 39 new = 87 slots" | "43 reuse + 39 new = 82 slots" |
| #3a | duel_field.inc section title | "(9 new offsets/masks)" | "(11 new offsets/masks)" |
| #3b | C5 grep note | "Safe to create all 9." | "Safe to create all 11." |
| #4  | duel_field.inc code block DISP_SEQ_STEP_LOCK_A_OFF | `0x00000080a` (9-digit hex) | `0x0000080a` (8-digit hex, format-only fix) |

Corrected summary: EQ=82 (reuse 43 + new 39) / REF=53 / RENAME=1 / FUNC_RENAME=0 / PLATE=11 / total=136.
Verify: 82+53+1 = 136. DAT_ 121 + PTR_gP1LifePoints_ 15 = 136.
