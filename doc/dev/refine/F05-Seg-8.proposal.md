# Refine Proposal: F05-Seg-8  [0x08050e40..0x08051cc4)

## 段测绘

- 段范围: asm/05_equip_eligibility_a.s lines 17671..19858 (Seg-7 boundary at 0x08050e40)
- 函数入口: 24 个 (地址序)

| 地址 | 名称 |
|------|------|
| 0x08050e40 | check_equip_slot_eligible_with_whitelist_prereqs_2 |
| 0x08050eac | check_equip_slot_eligible_by_card_id_tree |
| 0x080511b0 | check_equip_slot_eligible_by_empty_equip_with_field6 |
| 0x08051200 | check_equip_slot_eligible_by_field5_score_no_prereqs |
| 0x08051274 | check_equip_slot_eligible_by_prereqs_only |
| 0x080512c0 | check_equip_slot_eligible_by_lp_zone_and_type |
| 0x08051318 | check_equip_slot_eligible_by_equip_type |
| 0x08051364 | check_equip_slot_eligible_by_not_field8_9_and_type |
| 0x080513d0 | check_equip_slot_eligible_by_card_id_pair |
| 0x080514b4 | check_equip_slot_eligible_by_opposite_side_with_guard |
| 0x0805153c | check_equip_slot_eligible_by_opposite_and_slot_guard |
| 0x080515a8 | check_equip_slot_eligible_by_field5_score |
| 0x08051614 | check_equip_slot_eligible_by_opposite_side_and_prereqs |
| 0x08051670 | build_equip_chain_for_monster_zone |
| 0x0805174c | check_equip_slot_eligible_by_opposite_type_and_prereqs |
| 0x080517b4 | check_equip_slot_eligible_by_card_id_score |
| 0x08051898 | check_equip_slot_eligible_by_field6_type_and_prereqs |
| 0x08051924 | check_equip_slot_eligible_by_type_and_unequipped |
| 0x08051998 | check_equip_slot_eligible_by_setcode_whitelist |
| 0x08051a08 | build_equip_chain_for_special_zone |
| 0x08051abc | check_equip_slot_eligible_by_side_and_setcode |
| 0x08051b20 | check_equip_slot_eligible_by_setcode_and_prereqs |
| 0x08051b9c | check_equip_slot_eligible_by_setcode_only |
| 0x08051c3c | check_equip_slot_eligible_by_setcode_and_slot8 |

- 残留自动名槽: 83 x DAT_/DWORD_ (列于 EQ_SLOTS / REF_SLOTS / RENAME_SLOTS 节)
- ROM_INCBIN / .byte 块: 1 (0x51bfc / 0x40)

Note: Seg-7 already symbolized `_0` and `_1` literal pool slots as `<funcname>_stride` / `<funcname>_gdfs` named labels. Seg-8's `_2` variant uses `DAT_08050e9c` / `DAT_08050ea0` and follows the same naming convention.

---

## 数据块分类 (Rule 2/3)

### ROM_INCBIN at 0x0805_1bfc, size 0x40 (64 bytes)

Content (hex): `131c042b0ddc01220a409800c0188000054951434018054942181068c004002806d100200ae000006808000010c5010200211089002800d10121081c70470000`

ref-scan (python, 2B-step exhaustive over [0x51bfc, 0x51c3c)):

| 查询地址 | raw 引用数 | 来源 |
|----------|-----------|------|
| 0x08051bfc (raw) | 0 | — |
| 0x08051bfd (THUMB) | 2 | 0x9e404ac / 0x9e410c4 |
| 0x08051c05 (THUMB) | 1 | 0x9c245a9 |
| 0x08051c21 (THUMB) | 1 | 0x9d8930a |

所有引用来自 0x09xxxxxx 压缩资源区 (非可执行代码), 属偶合数据匹配。真实代码引用 = 0。

内容逐半字解码为合法 THUMB 指令序列 (`adds r3,r2,#0` / `cmp r3,#4` / ...), 是一段孤立 THUMB 代码 (orphan dead code), 与相邻 check_equip_slot_eligible_by_setcode_only (0x51b9c..0x51bfa) 和 check_equip_slot_eligible_by_setcode_and_slot8 (0x51c3c..) 之间的 gap。

**判定: §5.1 (0 真实代码引用)**

---

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate)

共 83 槽。以下按值分组:

#### 复用 ewram.inc PLAYER_BLOCK_STRIDE (0x00000868)

| 槽地址 | 标签 | 值 | const_name | 槽 label |
|--------|------|----|------------|---------|
| 0x08050e9c | DAT_08050e9c | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_with_whitelist_prereqs_2_stride |
| 0x08050f24 | DAT_08050f24 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_card_id_tree_stride_a |
| 0x08051108 | DAT_08051108 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_card_id_tree_stride_b |
| 0x080511f0 | DWORD_080511f0 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_empty_equip_with_field6_stride |
| 0x08051244 | DWORD_08051244 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_field5_score_no_prereqs_stride |
| 0x080512b0 | DWORD_080512b0 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_prereqs_only_stride |
| 0x0805130c | DWORD_0805130c | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_lp_zone_and_type_stride |
| 0x08051354 | DWORD_08051354 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_equip_type_stride |
| 0x080513c0 | DAT_080513c0 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_not_field8_9_and_type_stride |
| 0x0805141c | DAT_0805141c | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_card_id_pair_stride |
| 0x08051528 | DAT_08051528 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_opposite_side_with_guard_stride |
| 0x08051594 | DAT_08051594 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_opposite_and_slot_guard_stride |
| 0x080515e4 | DAT_080515e4 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_field5_score_stride |
| 0x08051660 | DAT_08051660 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_opposite_side_and_prereqs_stride |
| 0x08051714 | DAT_08051714 | 0x00000868 | PLAYER_BLOCK_STRIDE | build_equip_chain_for_monster_zone_stride |
| 0x080517a4 | DAT_080517a4 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_opposite_type_and_prereqs_stride |
| 0x08051840 | DAT_08051840 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_card_id_score_stride |
| 0x08051914 | DAT_08051914 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_field6_type_and_prereqs_stride |
| 0x0805197c | DAT_0805197c | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_type_and_unequipped_stride |
| 0x080519f8 | DAT_080519f8 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_setcode_whitelist_stride |
| 0x08051a4c | DAT_08051a4c | 0x00000868 | PLAYER_BLOCK_STRIDE | build_equip_chain_for_special_zone_stride |
| 0x08051b10 | DAT_08051b10 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_side_and_setcode_stride |
| 0x08051b8c | DAT_08051b8c | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_setcode_and_prereqs_stride |
| 0x08051bec | DAT_08051bec | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_setcode_only_stride |
| 0x08051ca8 | DAT_08051ca8 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_setcode_and_slot8_stride |

(25 slots; 値 ROM 验证: 0x08050e9c->0x00000868 OK, all OK per python verify)

#### 复用 ewram.inc gDuelFieldSlots (0x0201c510)

| 槽地址 | 标签 | 槽 label |
|--------|------|---------|
| 0x08050ea0 | DAT_08050ea0 | check_equip_slot_eligible_with_whitelist_prereqs_2_gdfs |
| 0x08050f28 | DAT_08050f28 | check_equip_slot_eligible_by_card_id_tree_gdfs_a |
| 0x0805110c | DAT_0805110c | check_equip_slot_eligible_by_card_id_tree_gdfs_b |
| 0x080511f4 | DWORD_080511f4 | check_equip_slot_eligible_by_empty_equip_with_field6_gdfs |
| 0x08051248 | DWORD_08051248 | check_equip_slot_eligible_by_field5_score_no_prereqs_gdfs |
| 0x080512b4 | DWORD_080512b4 | check_equip_slot_eligible_by_prereqs_only_gdfs |
| 0x08051358 | DWORD_08051358 | check_equip_slot_eligible_by_equip_type_gdfs |
| 0x080513c4 | DAT_080513c4 | check_equip_slot_eligible_by_not_field8_9_and_type_gdfs |
| 0x08051420 | DAT_08051420 | check_equip_slot_eligible_by_card_id_pair_gdfs |
| 0x0805152c | DAT_0805152c | check_equip_slot_eligible_by_opposite_side_with_guard_gdfs |
| 0x08051598 | DAT_08051598 | check_equip_slot_eligible_by_opposite_and_slot_guard_gdfs |
| 0x080515e8 | DAT_080515e8 | check_equip_slot_eligible_by_field5_score_gdfs |
| 0x08051664 | DAT_08051664 | check_equip_slot_eligible_by_opposite_side_and_prereqs_gdfs |
| 0x08051718 | DAT_08051718 | build_equip_chain_for_monster_zone_gdfs |
| 0x080517a8 | DAT_080517a8 | check_equip_slot_eligible_by_opposite_type_and_prereqs_gdfs |
| 0x08051844 | DAT_08051844 | check_equip_slot_eligible_by_card_id_score_gdfs |
| 0x08051918 | DAT_08051918 | check_equip_slot_eligible_by_field6_type_and_prereqs_gdfs |
| 0x08051980 | DAT_08051980 | check_equip_slot_eligible_by_type_and_unequipped_gdfs |
| 0x080519fc | DAT_080519fc | check_equip_slot_eligible_by_setcode_whitelist_gdfs |
| 0x08051a50 | DAT_08051a50 | build_equip_chain_for_special_zone_gdfs |
| 0x08051b14 | DAT_08051b14 | check_equip_slot_eligible_by_side_and_setcode_gdfs |
| 0x08051b90 | DAT_08051b90 | check_equip_slot_eligible_by_setcode_and_prereqs_gdfs |
| 0x08051bf0 | DAT_08051bf0 | check_equip_slot_eligible_by_setcode_only_gdfs |
| 0x08051cac | DAT_08051cac | check_equip_slot_eligible_by_setcode_and_slot8_gdfs |

(24 slots; all = 0x0201c510 verified OK)

Note: DWORD_08051304 (0x0201c4e0) holds gP1LifePoints which is already a named symbol in ewram.inc; this slot is REF type (not EQ), see REF_SLOTS.

#### 复用 ewram.inc gEquipChainSlotRefs (0x0201bb90)

| 槽地址 | 标签 | 槽 label |
|--------|------|---------|
| 0x08051530 | DAT_08051530 | check_equip_slot_eligible_by_opposite_side_with_guard_dts |
| 0x0805159c | DAT_0805159c | check_equip_slot_eligible_by_opposite_and_slot_guard_dts |

(2 slots; 值 0x0201bb90 verified OK)

Semantic note: The plate comments in these functions say `gDuelTurnStruct = 0x0201bb90` with fields `[+0]=current_player` and `[+0x1c]=current_slot`. ewram.inc defines `gEquipChainSlotRefs = 0x0201bb90` (equip chain slot reference array). These are the same address accessed with different offsets/semantics. Per C5 policy, reuse the existing label `gEquipChainSlotRefs`; the fixer should update the plate text to read `gEquipChainSlotRefs` (removing the stale `gDuelTurnStruct` name that was coined in the plate but never committed to any inc file). Confidence: high (address verified, ewram.inc comment cites `replace_slot_chain_ref_by_id` as authoritative consumer).

#### 复用 ewram.inc gDuelPhaseFlags (0x0201b290) + offsets

`DAT_08051478 = 0x0201b290` -> `gDuelPhaseFlags` (ewram.inc, verified OK)
`DAT_0805147c = 0x000004cc` -> `LP_BAR_ANIM_STATE_OFF` (ewram.inc, verified OK)
`DAT_08051480 = 0x000004f4` -> NEW constant: `CHAIN_NODE_CARD_ARR_OFF` (see 新增 constants)
`DAT_08051484 = 0x000004d4` -> `SPRITE_ROW_ENTRY_DATA_OFF` (ewram.inc, verified OK)

Plate comment says `gDuelEquipNode_base = 0x0201b290` and `NODE_LIST_OFFSET = 0x4cc`. ewram.inc already defines `gDuelPhaseFlags = 0x0201b290` and `LP_BAR_ANIM_STATE_OFF = 0x4cc`. The ewram.inc name is authoritative (file 02 Seg-2 provenance). The 0x4f4 offset is new: `gDuelPhaseFlags+0x4f4` = card pointer array for chain node list. Usage confirmed at `check_equip_slot_eligible_by_card_id_pair` (0x0805142c branch, `DAT_08051484=0x4d4` = `SPRITE_ROW_ENTRY_DATA_OFF` for node entry array; `DAT_08051480=0x4f4` = card array offset). Confirmed in Seg-9 comment line 21592: `OFFSET_CARD_ARR=0x4f4`.

EQ slot mappings for this group:

| 槽地址 | 标签 | 值 | const_name | 槽 label |
|--------|------|----|------------|---------|
| 0x08051478 | DAT_08051478 | 0x0201b290 | gDuelPhaseFlags | check_equip_slot_eligible_by_card_id_pair_dpf |
| 0x0805147c | DAT_0805147c | 0x000004cc | LP_BAR_ANIM_STATE_OFF | check_equip_slot_eligible_by_card_id_pair_count_off |
| 0x08051480 | DAT_08051480 | 0x000004f4 | CHAIN_NODE_CARD_ARR_OFF (新建) | check_equip_slot_eligible_by_card_id_pair_carr_off |
| 0x08051484 | DAT_08051484 | 0x000004d4 | SPRITE_ROW_ENTRY_DATA_OFF | check_equip_slot_eligible_by_card_id_pair_earr_off |

#### 复用 ewram.inc P1LP_BLOCK2_OFF_1CE8 (0x1ce8)

| 槽地址 | 标签 | 值 | const_name | 槽 label |
|--------|------|----|------------|---------|
| 0x08051308 | DWORD_08051308 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | check_equip_slot_eligible_by_lp_zone_and_type_lp_off |

(1 slot; verified OK; used as `[gP1LifePoints + P1LP_BLOCK2_OFF_1CE8]` = LP zone offset)

#### 复用 card_info.inc existing CIDs

| 槽地址 | 标签 | 值 | const_name | 槽 label |
|--------|------|----|------------|---------|
| 0x08050f34 | DAT_08050f34 | 0x0000123b | CRUSH_CARD_CID | check_equip_slot_eligible_by_card_id_tree_cid_123b |
| 0x08050f40 | DAT_08050f40 | 0x000014e4 | BURST_BREATH_CID | check_equip_slot_eligible_by_card_id_tree_cid_14e4 |
| 0x08051424 | DAT_08051424 | 0x000012cd | CHAIN_DESTRUCTION_CID (新建) | check_equip_slot_eligible_by_card_id_pair_cid_12cd |
| 0x08051428 | DAT_08051428 | 0x0000184b | RARE_METALMORPH_CID | check_equip_slot_eligible_by_card_id_pair_cid_184b |
| 0x08050f2c | DAT_08050f2c | 0x00001835 | GAIA_SOUL_CID | check_equip_slot_eligible_by_card_id_tree_cid_1835 |
| 0x08051080 | DAT_08051080 | 0x00001706 | TORPEDO_FISH_CID (新建) | check_equip_slot_eligible_by_card_id_tree_cid_1706 |
| 0x080510a0 | DAT_080510a0 | 0x00001709 | CANNONBALL_SPEAR_SHELLFISH_CID | check_equip_slot_eligible_by_card_id_tree_cid_1709 |

#### 复用 card_info.inc SLOT_CARD_EMPTY (0x0000ffff)

| 槽地址 | 标签 | 值 | const_name | 槽 label |
|--------|------|----|------------|---------|
| 0x08051ab8 | DAT_08051ab8 | 0x0000ffff | SLOT_CARD_EMPTY | build_equip_chain_for_special_zone_pair_not_found |

(1 slot; value = 0xffff = no pair found sentinel, same value/semantic as SLOT_CARD_EMPTY)

#### 新建 CIDs (card_info.inc)

| 槽地址 | 标签 | 值 | 新 const_name | 卡名 | passcode | 槽 label |
|--------|------|----|-------------|------|----------|---------|
| 0x08050f30 | DAT_08050f30 | 0x000014ee | DE_SPELL_GERM_WEAPON_CID | De-Spell Germ Weapon | 54591086 | check_equip_slot_eligible_by_card_id_tree_cid_14ee |
| 0x08050f58 | DAT_08050f58 | 0x00001708 | ORCA_MEGA_FORTRESS_OF_DARKNESS_CID | Orca Mega-Fortress of Darkness | 63120904 | check_equip_slot_eligible_by_card_id_tree_cid_1708 |
| 0x08050f68 | DAT_08050f68 | 0x00001753 | ARCANE_ARCHER_OF_THE_FOREST_CID | Arcane Archer of the Forest | 55001420 | check_equip_slot_eligible_by_card_id_tree_cid_1753 |
| 0x08050f90 | DAT_08050f90 | 0x00001928 | SPIRITUAL_WATER_ART_AOI_CID | Spiritual Water Art - Aoi | 06540606 | check_equip_slot_eligible_by_card_id_tree_cid_1928 |
| 0x08050fa0 | DAT_08050fa0 | 0x0000188d | ELEMENTAL_BURST_CID | Elemental Burst | 61411502 | check_equip_slot_eligible_by_card_id_tree_cid_188d |
| 0x08050fbc | DAT_08050fbc | 0x0000192a | SPIRITUAL_WIND_ART_MIYABI_CID | Spiritual Wind Art - Miyabi | 79333300 | check_equip_slot_eligible_by_card_id_tree_cid_192a |
| 0x08051190 | DAT_08051190 | 0x0000194f | HYDROGEDDON_CID | Hydrogeddon | 22587018 | check_equip_slot_eligible_by_card_id_tree_cid_194f |
| 0x080511a0 | DAT_080511a0 | 0x00001950 | OXYGEDDON_CID | Oxygeddon | 58071123 | check_equip_slot_eligible_by_card_id_tree_cid_1950 |
| 0x08051848 | DAT_08051848 | 0x00001250 | check_equip_slot_eligible_by_card_id_score_cid_1250 | NOT in card-stats.s (unallocated) | — | (see RENAME_SLOTS; semantic conflict: GSETTINGS_TEXT_FIELD_A_OFF=0x1250 different domain) |
| 0x08051864 | DAT_08051864 | 0x000012e4 | TRAP_HOLE_CID | Trap Hole | 04206964 | check_equip_slot_eligible_by_card_id_score_cid_12e4 |
| 0x08051424 | DAT_08051424 | 0x000012cd | CHAIN_DESTRUCTION_CID | Chain Destruction | 01248895 | check_equip_slot_eligible_by_card_id_pair_cid_12cd |
| 0x08051080 | DAT_08051080 | 0x00001706 | TORPEDO_FISH_CID | Torpedo Fish | 90337190 | check_equip_slot_eligible_by_card_id_tree_cid_1706 |

All card names verified via data/card-stats.s (confidence: high).

CHAIN_DESTRUCTION_CID: not in card_info.inc (grep confirmed). card-stats.s card_0654 slot=0x12CD. plate comment confirmed: "0x12cd (Chain Destruction)".

C5 note for 0x1250: GSETTINGS_TEXT_FIELD_A_OFF = 0x1250 exists (ewram.inc line 270), but its semantic is `gSettings+0x1250` (display offset), whereas here 0x1250 is used as a card slot_id (`ldrh r1,[r6,#0x0]` = card_id, cmp to 0x1250). Value collision, different semantic domain -> RENAME only, no CID new build. Slot label: `check_equip_slot_eligible_by_card_id_score_cid_1250`. EOL: "card_id=0x1250 (not in card-stats.s; equip BST leaf; distinct from GSETTINGS_TEXT_FIELD_A_OFF=0x1250)".

#### 新建 score threshold constants (card_info.inc)

| 槽地址 | 标签 | 值 | 新 const_name | 语义 | 槽 label |
|--------|------|----|-------------|------|---------|
| 0x08051134 | DAT_08051134 | 0x000007cf | FIELD5_SCORE_THRESHOLD_1999 | score <= 1999 (0x7cf) pass; used in check_equip_slot_eligible_by_card_id_tree Hydrogeddon/Oxygeddon path | check_equip_slot_eligible_by_card_id_tree_score_max |

C5: FIELD5_SCORE_THRESHOLD_1299 = 0x513 exists (card_info.inc, from Seg-6). 0x7cf != 0x513 -> new OK. No existing const with value 0x7cf found in constants/ (grep confirmed).

Arithmetic verified: `0x7cf = 1999` decimal; no shift-compose involved (literal .word slot, not computed).

#### 复用 card_info.inc CARD_STAT_LP_THRESHOLD_999 (0x000003e7)

| 槽地址 | 标签 | 值 | const_name | 槽 label |
|--------|------|----|------------|---------|
| 0x08051868 | DAT_08051868 | 0x000003e7 | CARD_STAT_LP_THRESHOLD_999 | check_equip_slot_eligible_by_card_id_score_trap_threshold |

C5: card_info.inc:83 already defines `CARD_STAT_LP_THRESHOLD_999 = 0x000003e7`. Value identical -> strict reuse (non-offset scalar, user ruling). EOL: `999 threshold (shared literal CARD_STAT_LP_THRESHOLD_999; here used as field5 score compare)`.

#### 新建 slot type mask constants (duel_field.inc)

Used in check_equip_slot_eligible_by_card_id_score at 0x080517b4, inner type filter:
- `ldrh r0,[r6,#0x2]` -> slot bitfield at +2
- `movs r1,#0xfc; lsls r1,r1,#4` -> 0xfc0 mask (verified: 0xfc<<4 = 0xfc0)
- `movs r0,#0xc0; lsls r0,r0,#1` -> 0x180 SLOT_TYPE_A (verified: 0xc0<<1 = 0x180)
- `adds r0,#0x40` -> 0x1c0 SLOT_TYPE_B (verified: 0x180+0x40 = 0x1c0)

No existing constants in duel_field.inc with these values (grep confirmed). New:

| const_name | 值 | 语义 |
|------------|-----|------|
| SLOT_CARD_TYPE_MASK | 0x000000fc0 | bits[11:6] of card[+2] halfword = slot card type field |
| SLOT_CARD_TYPE_ELIGIBLE_A | 0x00000180 | eligible type value A (lsls r0,#0xc0<<1) |
| SLOT_CARD_TYPE_ELIGIBLE_B | 0x000001c0 | eligible type value B (= A + 0x40) |

Confidence: med (function plate describes "slot type field (0xfc0 & [r6+2]) must be 0x180 or 0x1c0"; no independent cross-function evidence for field name).

These constants only appear at single slots in this segment. No new .inc file needed; add to duel_field.inc.

#### 新建 CHAIN_NODE_CARD_ARR_OFF (ewram.inc)

`DAT_08051480 = 0x000004f4` used as `gDuelPhaseFlags + 0x4f4` = card pointer array offset in equip chain node list. Confirmed by Seg-9 comment (line 21592): `OFFSET_CARD_ARR=0x4f4`. Add to ewram.inc near existing LP_BAR_ANIM_STATE_OFF/SPRITE_ROW_ENTRY_DATA_OFF group.

#### fn-ptr REF slots (RENAME to fn+1 labels)

| 槽地址 | 标签 | 值 (THUMB) | target fn | 槽 label |
|--------|------|-----------|----------|---------|
| 0x08050ff4 | DAT_08050ff4 | 0x080502b1 | eval_equip_slot_score_by_card_state+1 | check_equip_slot_eligible_by_card_id_tree_fn_ptr_a |
| 0x08051020 | DAT_08051020 | 0x08050a55 | check_equip_slot_eligible_by_card_id_bst+1 | check_equip_slot_eligible_by_card_id_tree_fn_ptr_b |
| 0x08051058 | DAT_08051058 | 0x08052aa9 | check_equip_slot_eligible_by_card_id_dispatch_b+1 | check_equip_slot_eligible_by_card_id_tree_fn_ptr_c |
| 0x08051084 | DAT_08051084 | 0x08050995 | check_equip_slot_eligible_by_type_then_prereqs+1 | check_equip_slot_eligible_by_card_id_tree_fn_ptr_d |
| 0x080510a4 | DAT_080510a4 | 0x08051b21 | check_equip_slot_eligible_by_setcode_and_prereqs+1 | check_equip_slot_eligible_by_card_id_tree_fn_ptr_e |
| 0x080510cc | DAT_080510cc | 0x08051b21 | check_equip_slot_eligible_by_setcode_and_prereqs+1 | check_equip_slot_eligible_by_card_id_tree_fn_ptr_f |

All values are odd (THUMB), verified by python. GAS `.word <fn>+1` syntax required (fn-ptr +1 periodic fix applies to these slots as well after re-export). Confidence: high (addresses match function push instructions within Seg-8 and surrounding code).

---

### REF_SLOTS (USER-label + DATA-ref)

| 槽地址 | 标签 | target 符号 | 槽 label |
|--------|------|------------|---------|
| 0x08051304 | DWORD_08051304 | gP1LifePoints | check_equip_slot_eligible_by_lp_zone_and_type_lp_base |

(1 REF slot; gP1LifePoints already named symbol in ewram.inc; use `.word gP1LifePoints` instead of `.word 0x0201c4e0`)

---

### RENAME_SLOTS (纯改名 + EOL)

| 槽地址 | 标签 | 值 | 新 slot_label | EOL |
|--------|------|----|-------------|-----|
| 0x08051848 | DAT_08051848 | 0x00001250 | check_equip_slot_eligible_by_card_id_score_cid_1250 | "card_id=0x1250 (not in card-stats.s; equip BST leaf; distinct from GSETTINGS_TEXT_FIELD_A_OFF=0x1250)" |

(1 RENAME; value collision with existing GSETTINGS_TEXT_FIELD_A_OFF but different semantic domain -> RENAME only per C5 rule)

---

### PLATE (R5)

One stale FUN_ found in Seg-8 range (grep `FUN_[0-9a-f]{8}` on lines 17671..19858):

- Line 19638, function `check_equip_slot_eligible_by_setcode_and_prereqs` (0x08051b20):
  Plate contains `FUN_08053704` and `FUN_08054118`.

  - `FUN_08053704` -> `dispatch_equip_slot_eligible_by_card_id_tier` (asm/05, line 23735, confirmed)
  - `FUN_08054118` -> `dispatch_equip_slot_eligible_by_type_prereqs_or_setcode` (asm/06, line 1382, confirmed)

  Action: **substring replace** both stale FUN_ names with current names in the plate.

| fn addr | old substring | new substring |
|---------|--------------|---------------|
| 0x08051b20 | FUN_08053704 | dispatch_equip_slot_eligible_by_card_id_tier |
| 0x08051b20 | FUN_08054118 | dispatch_equip_slot_eligible_by_type_prereqs_or_setcode |

Additionally, plates for `check_equip_slot_eligible_by_opposite_side_with_guard` (0x080514b4) and `check_equip_slot_eligible_by_opposite_and_slot_guard` (0x0805153c) reference `gDuelTurnStruct = 0x0201bb90` in the Constants section. Fixer should update plate text to replace `gDuelTurnStruct` with `gEquipChainSlotRefs` (the authoritative ewram.inc name). This is a prose fix within plate, not a FUN_ stale name fix.

---

## carve 计划 (R7)

**无**。 ROM_INCBIN 0x51bfc/0x40 = §5.1 (0 真实代码引用)。无函数间 ROM_INCBIN 需 carve。

---

## disasm 计划 (R4)

**无**。无误标数据为代码的区域。ROM_INCBIN 0x51bfc/0x40 是孤立 THUMB 死代码, §5.1 登记。

---

## 新增 constants / 全局

### card_info.inc 新增 (N=12 CID + 1 threshold)

| const_name | 值 | 来源证据 |
|------------|-----|---------|
| DE_SPELL_GERM_WEAPON_CID | 0x000014ee | card-stats.s card_1054 slot=0x14EE pw=54591086 |
| TORPEDO_FISH_CID | 0x00001706 | card-stats.s card_1470 slot=0x1706 pw=90337190 |
| ORCA_MEGA_FORTRESS_OF_DARKNESS_CID | 0x00001708 | card-stats.s card_1472 slot=0x1708 pw=63120904 |
| ARCANE_ARCHER_OF_THE_FOREST_CID | 0x00001753 | card-stats.s card_1534 slot=0x1753 pw=55001420 |
| CHAIN_DESTRUCTION_CID | 0x000012cd | card-stats.s card_0654 slot=0x12CD pw=01248895 |
| TRAP_HOLE_CID | 0x000012e4 | card-stats.s card_0668 slot=0x12E4 pw=04206964 |
| ELEMENTAL_BURST_CID | 0x0000188d | card-stats.s card_1804 slot=0x188D pw=61411502 |
| SPIRITUAL_WATER_ART_AOI_CID | 0x00001928 | card-stats.s card_1925 slot=0x1928 pw=06540606 |
| SPIRITUAL_WIND_ART_MIYABI_CID | 0x0000192a | card-stats.s card_1927 slot=0x192A pw=79333300 |
| HYDROGEDDON_CID | 0x0000194f | card-stats.s card_1950 slot=0x194F pw=22587018 |
| OXYGEDDON_CID | 0x00001950 | card-stats.s card_1951 slot=0x1950 pw=58071123 |
| FIELD5_SCORE_THRESHOLD_1999 | 0x000007cf | check_equip_slot_eligible_by_card_id_tree cmp [sp+0x14] vs 0x7cf path |

C5 check: FIELD5_SCORE_THRESHOLD_1299=0x513 exists, 0x7cf != 0x513 (new OK). FIELD5_SCORE_THRESHOLD_999 (0x3e7) removed: reuse CARD_STAT_LP_THRESHOLD_999 from card_info.inc:83 (same value, C5 strict dedup). None of the 12 CIDs found in card_info.inc (grep confirmed). RARE_METALMORPH_CID/CRUSH_CARD_CID/BURST_BREATH_CID/GAIA_SOUL_CID/CANNONBALL_SPEAR_SHELLFISH_CID -> all REUSE (see EQ_SLOTS).

### ewram.inc 新增

| const_name | 值 | 语义 | 信心 |
|------------|-----|------|------|
| CHAIN_NODE_CARD_ARR_OFF | 0x000004f4 | [gDuelPhaseFlags+0x4f4] card pointer array for equip chain node list | high (Seg-9 comment confirms OFFSET_CARD_ARR=0x4f4) |

### duel_field.inc 新增

| const_name | 值 | 语义 | 信心 |
|------------|-----|------|------|
| SLOT_CARD_TYPE_MASK | 0x000000fc0 | bits[11:6] type field in card[+2] halfword (check_equip_slot_eligible_by_card_id_score filter) | med |
| SLOT_CARD_TYPE_ELIGIBLE_A | 0x00000180 | eligible slot type value A | med |
| SLOT_CARD_TYPE_ELIGIBLE_B | 0x000001c0 | eligible slot type value B | med |

---

## §5.1 登记 (Rule 3) — 0 引用块

| 地址 | 大小 | 初判内容 | 状态 |
|------|------|---------|------|
| 0x0805_1bfc | 0x40 (64B) | 孤立 THUMB dead code (orphan; gap 于 check_equip_slot_eligible_by_setcode_only 与 check_equip_slot_eligible_by_setcode_and_slot8 之间); 所有 4 个 THUMB 引用来自 0x09xxxxxx 压缩资源区 (偶合), 真实代码引用 = 0 (ref-scan 验证) | defer |

---

## 消费者证据 (R6)

1. **PLAYER_BLOCK_STRIDE = 0x868**: ewram.inc line 311 定义; 24 个函数的 slot 计算公式 `player_id*0x868 + slot_idx*0x14`, 全段一致。文件: ewram.inc:311, 置信度: high。

2. **gDuelFieldSlots = 0x0201c510**: ewram.inc line 311 定义; 24 个函数均通过 `gDuelFieldSlots + player_off + slot_off` 访问目标 slot。置信度: high。

3. **gEquipChainSlotRefs = 0x0201bb90**: ewram.inc line 313; used at `[base+0]=current_player` / `[base+0x1c]=current_slot_idx` in check_equip_slot_eligible_by_opposite_side_with_guard (0x080514b4) and check_equip_slot_eligible_by_opposite_and_slot_guard (0x0805153c). 置信度: high (address match confirmed).

4. **gDuelPhaseFlags = 0x0201b290 + offsets 0x4cc / 0x4d4 / 0x4f4**: ewram.inc lines 349/400/406; used in check_equip_slot_eligible_by_card_id_pair (0x080513d0) chain node traversal. 0x4f4 confirmed by Seg-9 comment line 21592. 置信度: high.

5. **Card IDs via card-stats.s**: All CIDs verified slot_id match in card-stats.s (confidence: high for all named cards). 0x1250 not in card-stats.s (confidence: low, kept neutral RENAME).

6. **SLOT_CARD_EMPTY = 0x0000ffff**: card_info.inc line 386; used in build_equip_chain_for_special_zone (0x08051a08) as pair-not-found sentinel compared against find_equip_chain_pair_across_field result. 置信度: high.

7. **gP1LifePoints = 0x0201c4e0**: ewram.inc (gP1LifePoints); used in check_equip_slot_eligible_by_lp_zone_and_type (0x080512c0) as `gP1LifePoints + P1LP_BLOCK2_OFF_1CE8` to read LP zone equip area. 置信度: high.

8. **Fn-ptr targets**: All 5 fn-ptr slots contain odd (THUMB) addresses pointing to named functions within asm/05 confirmed by push instruction addresses. `.word <fn>+1` syntax required (fn-ptr +1 rule applies). 置信度: high.

---

## 求助

1. **SLOT_CARD_TYPE_MASK / ELIGIBLE_A / ELIGIBLE_B (0xfc0 / 0x180 / 0x1c0)**: 仅在 check_equip_slot_eligible_by_card_id_score (0x080517b4) 内 bits[11:6] 过滤路径出现, 无其他函数交叉引用命名这些字段。置信度 med。命名合理但无法完全确认字段语义。

2. **0x1250 card_id**: 未在 card-stats.s 中找到对应 slot_id。与 GSETTINGS_TEXT_FIELD_A_OFF 值碰撞但不同域。暂标中性 RENAME。如有更多证据可升 CID。

---

## Executor Report: F05-Seg-8

- 槽: EQ=75 (25 stride + 24 gdfs + 2 gEquipChainSlotRefs + 4 gDuelPhaseFlags group + 1 P1LP_BLOCK2 + 7 reuse-CID + 1 reuse-CARD_STAT_LP_THRESHOLD_999 + 1 new-threshold + 3 type-mask + 1 SLOT_CARD_EMPTY + 6 fn-ptr) REF=1 RENAME=1 FUNC_RENAME=0 PLATE=1 fn (2 FUN_ subs + 2 gDuelTurnStruct->gEquipChainSlotRefs prose fixes)
- carve=0 disasm=0 §5.1=1 (0x051bfc/0x40)
- 新增 constants/全局: card_info.inc +12 CID + 1 threshold (FIELD5_SCORE_THRESHOLD_1999); ewram.inc +1 (CHAIN_NODE_CARD_ARR_OFF); duel_field.inc +3 (SLOT_CARD_TYPE_MASK/ELIGIBLE_A/ELIGIBLE_B); 复用 card_info.inc CARD_STAT_LP_THRESHOLD_999 for 0x3e7 slot (C5 dedup)
- 求助: SLOT_CARD_TYPE_MASK 0xfc0 语义 med-conf; 0x1250 card_id unallocated neutral
- proposal: doc/dev/refine/F05-Seg-8.proposal.md
