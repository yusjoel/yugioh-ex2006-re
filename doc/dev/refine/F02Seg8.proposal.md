# Refine Proposal: F02-Seg-8  [0x08032e80..0x08033654)

## 段测绘

- 函数入口: 23 个
  - 0x08032e80  count_monster_slots_by_state
  - 0x08032ef0  count_monster_slots_by_state_all
  - 0x08032f00  count_eligible_zone_slots_for_player
  - 0x08032f6c  count_eligible_zone_slots_all_flags
  - 0x08032f7c  count_slot_card_pair_allowed_for_card
  - 0x08032fa4  count_unpaired_slots_for_card
  - 0x08032fd8  count_field_cards_pair_allowed_for_card
  - 0x08033088  check_toon_world_equip_present
  - 0x0803309c  count_active_slots_with_field6_value
  - 0x0803310c  count_occupied_all_field_zones
  - 0x08033188  count_occupied_monster_zones
  - 0x080331bc  count_occupied_monster_zones_with_effect_bonus
  - 0x08033214  count_monster_slots_by_fnptr
  - 0x08033258  count_field_slots_with_field8_is_9
  - 0x08033294  count_slots_with_chain_field_match
  - 0x080332f0  count_slots_matching_card_pair
  - 0x08033334  count_monster_slots_by_chain_head_id
  - 0x08033370  count_active_cards_in_zone_by_player
  - 0x080333ac  check_slot_placement_blocked_by_field_effect
  - 0x0803352c  check_monster_slot_accepts_card
  - 0x080335b8  count_available_monster_slots
  - 0x08033610  count_monster_slots_accepting_card
  - 0x08033634  get_first_placeable_monster_slot

- 残留自动名槽: 44 个 (全段无 PTR_/DWORD_ 混名; 4 个已为 PTR_gP1LifePoints_* 格式)
  - DAT_08032ee8 = 0x00000868 x1
  - DAT_08032eec = 0x0201c510 x1
  - DAT_08032f64 = 0x00000868 x1
  - DAT_08032f68 = 0x0201c510 x1
  - DAT_0803307c = 0x00000868 x1
  - DAT_08033080 = 0x0201c510 x1
  - PTR_gP1LifePoints_08033084 = gP1LifePoints x1
  - DAT_08033098 = 0x000012be x1
  - DAT_08033104 = 0x00000868 x1
  - DAT_08033108 = 0x0201c510 x1
  - PTR_gP1LifePoints_08033178 = gP1LifePoints x1
  - DAT_0803317c = 0x00000868 x1
  - DAT_08033180 = 0x000010d0 x1
  - DAT_08033184 = 0x0201bb90 x1
  - DAT_080331b4 = 0x00000868 x1
  - DAT_080331b8 = 0x0201c510 x1
  - PTR_gP1LifePoints_08033208 = gP1LifePoints x1
  - DAT_0803320c = 0x000010d0 x1
  - DAT_08033210 = 0x0201bb90 x1
  - DAT_08033250 = 0x00000868 x1
  - DAT_08033254 = 0x0201c510 x1
  - DAT_0803328c = 0x00000868 x1
  - DAT_08033290 = 0x0201c510 x1
  - DAT_080332e8 = 0x0201c510 x1
  - DAT_080332ec = 0x00000868 x1
  - DAT_0803332c = 0x00000868 x1
  - DAT_08033330 = 0x0201c510 x1
  - DAT_08033368 = 0x00000868 x1
  - DAT_0803336c = 0x0201c510 x1
  - DAT_080333a4 = 0x00000868 x1
  - DAT_080333a8 = 0x0201c510 x1
  - DAT_080334bc = 0x0201c5ec x1
  - DAT_080334c0 = 0x00000868 x1
  - DAT_080334c4 = 0x000013d4 x1
  - DAT_080334c8 = 0xffffeb50 x1
  - DAT_080334cc = 0x00001432 x1
  - DAT_080334d0 = 0x000017ee x1
  - DAT_080334d4 = 0x0201c4fc x1
  - PTR_gP1LifePoints_080334d8 = gP1LifePoints x1
  - DAT_08033528 = 0x00001472 x1
  - DAT_080335a4 = 0x00000868 x1
  - DAT_080335a8 = 0x0201c510 x1
  - DAT_080335ac = 0x0201bb90 x1
  - DAT_080335f8 = 0x000016df x1

- ROM_INCBIN / .byte 块: 0 个 (本段无任何 incbin/byte 块)

## 数据块分类 (Rule 2/3) -- 每块给 ref-scan 证据

本段无 ROM_INCBIN/.byte 数据块，跳过此节。

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate)

共 37 个 EQ 槽 (33 复用 + 4 新建卡牌 ID + 1 新建全局地址):

#### EQ_REUSE (33 槽，全复用已有 constants/*.inc):

| slot | value | const_name | inc | slot_label |
|------|-------|-----------|-----|-----------|
| DAT_08032ee8 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | count_monster_slots_by_state_stride |
| DAT_08032eec | 0x0201c510 | gDuelFieldSlots | ewram.inc | count_monster_slots_by_state_base |
| DAT_08032f64 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | count_eligible_zone_slots_stride |
| DAT_08032f68 | 0x0201c510 | gDuelFieldSlots | ewram.inc | count_eligible_zone_slots_base |
| DAT_0803307c | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | count_field_cards_pair_stride |
| DAT_08033080 | 0x0201c510 | gDuelFieldSlots | ewram.inc | count_field_cards_pair_base |
| DAT_08033104 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | count_active_field6_stride |
| DAT_08033108 | 0x0201c510 | gDuelFieldSlots | ewram.inc | count_active_field6_base |
| DAT_0803317c | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | count_occupied_all_zones_stride |
| DAT_08033180 | 0x000010d0 | EFFECT_ZONE_BITMASK_OFF | duel_field.inc | count_occupied_all_zones_bitmask_off |
| DAT_08033184 | 0x0201bb90 | gEquipChainSlotRefs | ewram.inc | count_occupied_all_zones_effect_ctx |
| DAT_080331b4 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | count_occupied_monster_zones_stride |
| DAT_080331b8 | 0x0201c510 | gDuelFieldSlots | ewram.inc | count_occupied_monster_zones_base |
| DAT_0803320c | 0x000010d0 | EFFECT_ZONE_BITMASK_OFF | duel_field.inc | count_occ_monster_bonus_bitmask_off |
| DAT_08033210 | 0x0201bb90 | gEquipChainSlotRefs | ewram.inc | count_occ_monster_bonus_effect_ctx |
| DAT_08033250 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | count_monster_by_fnptr_stride |
| DAT_08033254 | 0x0201c510 | gDuelFieldSlots | ewram.inc | count_monster_by_fnptr_base |
| DAT_0803328c | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | count_field8_is_9_stride |
| DAT_08033290 | 0x0201c510 | gDuelFieldSlots | ewram.inc | count_field8_is_9_base |
| DAT_080332e8 | 0x0201c510 | gDuelFieldSlots | ewram.inc | count_chain_field_match_base |
| DAT_080332ec | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | count_chain_field_match_stride |
| DAT_0803332c | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | count_slots_card_pair_stride |
| DAT_08033330 | 0x0201c510 | gDuelFieldSlots | ewram.inc | count_slots_card_pair_base |
| DAT_08033368 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | count_monster_chain_head_stride |
| DAT_0803336c | 0x0201c510 | gDuelFieldSlots | ewram.inc | count_monster_chain_head_base |
| DAT_080333a4 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | count_active_zone_card_stride |
| DAT_080333a8 | 0x0201c510 | gDuelFieldSlots | ewram.inc | count_active_zone_card_base |
| DAT_080334c0 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | check_slot_blocked_field_stride |
| DAT_080334c8 | 0xffffeb50 | NODE_POOL_NEG_OFFSET | duel_field.inc | check_slot_blocked_node_neg_off |
| DAT_080334d4 | 0x0201c4fc | gP1AltHandCountBase | ewram.inc | check_slot_blocked_alt_hand_base |
| DAT_080335a4 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | check_monster_slot_accepts_stride |
| DAT_080335a8 | 0x0201c510 | gDuelFieldSlots | ewram.inc | check_monster_slot_accepts_base |
| DAT_080335ac | 0x0201bb90 | gEquipChainSlotRefs | ewram.inc | check_monster_slot_effect_ctx |

#### EQ_NEW (5 槽，新建常量):

| slot | value | const_name | inc | slot_label | 证据 |
|------|-------|-----------|-----|-----------|-----|
| DAT_080334bc | 0x0201c5ec | gDuelFieldSpellZoneBase | ewram.inc | check_slot_blocked_fz_base | gDuelFieldSlots+0xdc=slot[11](P0 field-spell zone); 6 raw refs; check_slot_placement_blocked_by_field_effect r10 base |
| DAT_080334cc | 0x00001432 | GROUND_COLLAPSE_FIELD_CARD_ID | card_info.inc | check_slot_blocked_ground_collapse_id | plate: "Ground_Collapse_id=0x1432"; 18 raw refs; field-spell node check in monster-zone path |
| DAT_080334d0 | 0x000017ee | OJAMA_KING_CARD_ID | card_info.inc | check_slot_blocked_ojama_king_id | plate: "OjamaKing_id=0x17ee"; 13 raw refs; field-spell node check (Ojama King monster-zone limit effect) |
| DAT_08033098 | 0x000012be | TOON_WORLD_CARD_ID | card_info.inc | check_toon_world_card_id | plate: "0x12be (Toon World)"; 9 raw refs; check_toon_world_equip_present only caller |
| DAT_080335f8 | 0x000016df | SPATIAL_COLLAPSE_CARD_ID | card_info.inc | count_avail_monster_spatial_id | plate: "special_card=0x16df"; 16 raw refs; count_available_monster_slots spatial collapse clamp |

### REF_SLOTS (USER-label + DATA-ref)

0 槽。本段无需 REF_SLOTS 操作:
- 4 个 PTR_gP1LifePoints_* 槽已为 DATA-ref 形式 (值为 gP1LifePoints 符号), 处理为 RENAME_SLOTS。
- 其余槽均为整数立即数, 走 EQ 路径。

### RENAME_SLOTS (纯改名 + EOL)

共 7 槽:

| slot | slot_label | eol_ascii |
|------|-----------|-----------|
| PTR_gP1LifePoints_08033084 | count_field_cards_pair_lp_base | gP1LifePoints: hand count + special zone offset 0x83<<3 |
| PTR_gP1LifePoints_08033178 | count_occupied_all_zones_lp_base | gP1LifePoints: slot array base (r6+0x30=gDuelFieldSlots) + bitmask off 0x10d0 |
| PTR_gP1LifePoints_08033208 | count_occ_monster_bonus_lp_base | gP1LifePoints: bitmask field off 0x10d0; effect ctx ref |
| PTR_gP1LifePoints_080334d8 | check_slot_blocked_lp_base | gP1LifePoints: entity state lookup offset 0x1c, slot_idx at [+0x1c]/[+0x20] |
| DAT_08033528 | check_slot_blocked_equip_key | 0x1472: equip-whitelist chain key (check_slot_card_is_equip_whitelist + get_node_entity_id_in_slot spell/trap path); 31 raw refs |
| DAT_08033528 (注: 独立 RENAME) | -- 见上 -- | -- |
| DAT_080334c4 | check_slot_blocked_node_pool_off | 0x13d4 = gEquipNodePool - gDuelFieldSpellZoneBase (1 raw ref; derived offset, no standalone const) |

修正: 共 6 个 RENAME (4 PTR + 2 独立 DAT RENAME):

| slot | slot_label | eol_ascii |
|------|-----------|-----------|
| PTR_gP1LifePoints_08033084 | count_field_cards_pair_lp_base | gP1LifePoints: hand count[+0x14] + alt zone array 0x83<<3=0x418 |
| PTR_gP1LifePoints_08033178 | count_occupied_all_zones_lp_base | gP1LifePoints: +0x30=gDuelFieldSlots scan base; +0x10d0=EFFECT_ZONE_BITMASK_OFF |
| PTR_gP1LifePoints_08033208 | count_occ_monster_bonus_lp_base | gP1LifePoints: +0x10d0=EFFECT_ZONE_BITMASK_OFF bitmask flag |
| PTR_gP1LifePoints_080334d8 | check_slot_blocked_lp_base | gP1LifePoints: effect entity ctx slot+0x1c(P0_idx)/+0x20(P1_idx) |
| DAT_08033528 | check_slot_blocked_equip_key | 0x1472: equip-whitelist chain key; spell/trap zone path; 31 raw refs |
| DAT_080334c4 | check_slot_blocked_node_pool_off | 0x13d4 = gEquipNodePool - gDuelFieldSpellZoneBase (1 raw ref; derived) |

### FUNC_RENAME

0 个。全段 23 个函数名均无误名信号 (函数体操作与函数名一致; indeg 与功能对应)。

### PLATE (R5; 全 ASCII)

共 5 个 plate 需处理:

**P1: count_slots_with_chain_field_match (0x08033294) -- CJK 板重写**
```
Counts player (r0 bit0) monster zone slots 0..4 satisfying: slot occupied (bit9 set); if cond_a(r1!=0): slot[+0x8](equip_chain_head)!=0; if cond_b(r2!=0): slot[+0x6](chain_field)!=0. Both conditions pass -> count++. Pure leaf, no side effects. r0=u32 player_side [0..1]; r1=u32 cond_a_flag; r2=u32 cond_b_flag. Returns u32 count [0..5]. Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, slot_entry=0x14, slot+0x8=equip_chain_head, slot+0x6=chain_field.
```

**P2: count_monster_slots_by_chain_head_id (0x08033334) -- CJK 板重写**
```
Counts player (r0 bit0) monster zone slots 0..4 where: slot occupied (bit19 set) AND slot[+8] low16 == r1 (target_chain_head_id). Loop stride 0x14, descending r3=4..0. Returns hit count. Used to detect if a card is currently mounted as equip chain head on a monster zone slot. r0=u32 player_side [0..1]; r1=u32 target_chain_head_id. Returns u32 count [0..5]. Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, slot_entry=0x14. Field-spell IDs checked in caller check_slot_placement_blocked_by_field_effect: Ground_Collapse_id=0x1432, OjamaKing_id=0x17ee.
```

**P3: count_eligible_zone_slots_all_flags (0x08032f6c) -- stale FUN_08032f00 替换为现名**

旧板含 `FUN_08032f00` (已命名为 count_eligible_zone_slots_for_player), 全段重写:
```
Thin wrapper around count_eligible_zone_slots_for_player. Sets r2=-1 (movs r2,#1; rsbs r2,r2,#0 = all-flags) then calls count_eligible_zone_slots_for_player. Counts all eligible zone slots for given player side with all zone bits selected. r0=u8 player_id [0..1]. Returns r0=u8 count [0..5]. Constants: ZONE_FLAG_ALL=-1.
```

**P4: count_slot_card_pair_allowed_for_card (0x08032f7c) -- callers 行含 FUN_ (外部未命名); 无 FUN_ 指向本函数, 不强制改板**

现有板包含 `FUN_080ac584, FUN_080acc30, FUN_080b76e4` (均为尚未命名的外部函数), 不属于 C8 stale-subject 范畴, 跳过。

**P5: count_field_cards_pair_allowed_for_card (0x08032fd8) -- callers 行含 FUN_ (外部); 同上, 跳过**

实际需处理 plate: P1 + P2 + P3 = 3 个。

## carve 计划 (R7)

无。本段无 ROM_INCBIN 块，无 carve 需求。

## disasm 计划 (R4)

无。本段无误标数据块，无 disasm 需求。

## 新增 constants / 全局

共 6 项新建 (均已确认现有 constants/*.inc 中无同值):

### card_info.inc 追加 (4 项):
```
.equ TOON_WORLD_CARD_ID,              0x000012be  @ Toon World field-magic card id; presence check via equip-zone scan; 9 raw refs
.equ GROUND_COLLAPSE_FIELD_CARD_ID,  0x00001432  @ Ground Collapse field spell card id (data.md line 900, passcode 90502999); placement-block check in check_slot_placement_blocked_by_field_effect; 18 raw refs
.equ OJAMA_KING_CARD_ID,             0x000017ee  @ Ojama King card id (data.md line 1639, passcode 90140980); monster-zone limit effect; placement-block check; 13 raw refs
.equ SPATIAL_COLLAPSE_CARD_ID,       0x000016df  @ Spatial Collapse field spell id; monster zone clamp in count_available_monster_slots; 16 raw refs
```

### ewram.inc 追加 (1 项):
```
.equ gDuelFieldSpellZoneBase,   0x0201c5ec  @ gDuelFieldSlots + 11*0x14 = P0 field-spell zone slot entry base; r10 base in check_slot_placement_blocked_by_field_effect; 6 raw refs
```

**注**: `0x00001472` (equip-whitelist chain key, 31 raw refs) 使用 RENAME 而非 EQ_NEW, 因为其在本段中是一次性独立数值槽用于 spell/trap 路径的 get_node_entity_id_in_slot 调用参数, 尚无确定的通用常量语义。但鉴于 31 raw refs 较多, 后续 Seg 若再次出现可考虑升格为 card_info.inc 常量。当前 proposal 标记为 RENAME+EOL。

### 注: 0x000013d4 不新建常量 (1 raw ref, 衍生值)

`DAT_080334c4 = 0x000013d4 = gEquipNodePool - gDuelFieldSpellZoneBase`。仅 1 个 ROM 原始引用, 属衍生偏移量, 改名为 `check_slot_blocked_node_pool_off` + EOL 注释即可。

## §5.1 登记 (Rule 3) -- 0 引用块

无。本段无 ROM_INCBIN/.byte 块，无 §5.1 登记需要。

## 消费者证据 (R6) -- 关键槽语义的 file:line + 置信度

| 槽 / 常量 | 消费者证据 | 置信度 |
|---------|---------|------|
| 0x000012be = TOON_WORLD_CARD_ID | asm/02_text_lp_fieldspell.s:15574 plate "0x12be (Toon World)"; check_toon_world_equip_present sole consumer | high |
| 0x00001432 = GROUND_COLLAPSE_FIELD_CARD_ID | data.md line 900: Ground Collapse (passcode 90502999); asm/02_text_lp_fieldspell.s:16036 plate (stale Yami_id text, P2 rewrites correctly to Ground_Collapse_id=0x1432); monster-zone field-spell node cmp | high |
| 0x000017ee = OJAMA_KING_CARD_ID | data.md line 1639: Ojama King (passcode 90140980); asm/05_equip_eligibility_a.s:17905 plate "0x17ee (Ojama King)"; doc/dev/eval/08052aa8.md:22 Ojama King confirmed; monster-zone limit effect semantic matches | high |
| 0x000016df = SPATIAL_COLLAPSE_CARD_ID | asm/02_text_lp_fieldspell.s:16321 plate "special_card=0x16df"; asm/13_equip_placement.s:10218 "CARD_ID_16DF=0x16df (Spatial Collapse)" | high |
| 0x0201c5ec = gDuelFieldSpellZoneBase | asm/02_text_lp_fieldspell.s:16036 plate "slot 0xb = field spell zone"; gDuelFieldSlots+11*0x14=0x0201c5ec; r10 base for player*0x868 scan in check_slot_placement_blocked_by_field_effect | high |
| 0x000010d0 = EFFECT_ZONE_BITMASK_OFF | constants/duel_field.inc:166 comment "(used as: r10=gDuelFieldSlots-0x30; r10+0x10d0=gDuelFieldSlots+0x10a0)"; asm:15671 adds r0,r6,r1 where r6=gP1LifePoints | high |
| 0x0201bb90 = gEquipChainSlotRefs | constants/ewram.inc:308; prior Seg-7 applied label; Seg-8 uses [+0x0][+0x4]=P0/P1 player id, [+0xc4][+0xd8]=active slots | high |
| 0x00001472 = equip-whitelist chain key | asm/02_text_lp_fieldspell.s:10147 plate "equip_ids=0x1472/0x1636/0x172f/0x1809"; asm:16243 DAT_08033528 passed as r2 to get_node_entity_id_in_slot in spell/trap path | med (card identity uncertain; no explicit name in plate) |
| 0x0201c4fc = gP1AltHandCountBase | constants/ewram.inc:328; used in spell/trap scan path: [gP1AltHandCountBase+player*0x868] = alt_hand_count | high |

## 求助

- 0x00001472 的卡牌名称未在 plate 中明确标注 (plate 仅写 "equip_ids=0x1472/0x1636/0x172f/0x1809")。若需要精确卡牌名可查 data/card-names.s card_name 条目。当前 RENAME + EOL 方案不依赖卡牌名 (confidence=med), 不影响 byte-identical。

