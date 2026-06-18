# Refine Review: F08-Seg-9

## 核验矩阵 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | ✅ | Seg-9 = 0x0806cbe8..0x0806d960, 接 Seg-8c (0x6c0cc..0x6cbe8 ✅), 符合 §五 路线图 |
| C2 Rule2 | ✅ | python 扫 Seg-9 lines 19718..21595: ROM_INCBIN=0, .byte=0, 与 proposal 一致 |
| C3 Rule3 | ✅ | 无 ROM_INCBIN 块, ref-scan 不适用 |
| C4 R1 值 | ✅ | 27 个抽查槽全部匹配 ROM 小端字节; 见下方核对表 |
| C5 R1 复用 | ✅ | 4 NEW 按值 grep constants/*.inc 全部 0 命中; 14 reuse 精确名值双向核通过 |
| C6 R2 名 | ✅ | 12 个 RENAME label 全部符合 ^[a-z][a-z0-9_]+$, 无重复 |
| C7 R3 接通 | ✅ | REF=0, carve=0; 无需 USER-label/DATA-ref 连通检查 |
| C8 R5 现名 | ✅ | Seg-9 内 FUN_ 恰好 2 处 (L20975/L21181), 均在 proposal PLATE 计划中; 已确认现名 |
| C9 ASCII | ✅ | Seg-9 仅 L20806 含非 ASCII (318 字节 UTF-8 CJK), 在 proposal PLATE#3 计划 ASCII 重写; 12 RENAME EOL 无非 ASCII |
| C10 carve | ✅ | carve=0 (无指针表条目需核对) |
| C11 误名 | ✅ PASS (见注) | dispatch_neo_space_placement_by_card_id_and_state 保留: neo_space 为 file 08 既成非正式域标签, 不触发 FUNC_RENAME |
| C12 R6 | ✅ | 7 关键槽均有 asm/08 file:line 引用 + high 置信度; 无零容忍词 |
| C13 残留 | ✅ | python 精确清点: Seg-9 内 DAT_/DWORD_/PTR_/UNK_ = 63 个, EQ(51)+RENAME(12)=63, 无遗漏无越界无重复 |

---

## 独立复核细节

### C4: ROM 字节抽查 (27 槽)

| slot | addr | proposal value | ROM 实读 |
|------|------|----------------|----------|
| DAT_0806cc1c | 0x0806cc1c | 0x0201b290 | 0x0201b290 ✅ |
| DAT_0806cc60 | 0x0806cc60 | 0x00001da8 | 0x00001da8 ✅ |
| DAT_0806cc94 | 0x0806cc94 | 0x00001daa | 0x00001daa ✅ |
| DAT_0806ccb8 | 0x0806ccb8 | 0x00001daa | 0x00001daa ✅ |
| DAT_0806cd38 | 0x0806cd38 | 0x00000868 | 0x00000868 ✅ |
| DAT_0806cd3c | 0x0806cd3c | 0x0201c510 | 0x0201c510 ✅ |
| DAT_0806cdb4 | 0x0806cdb4 | 0x000010d0 | 0x000010d0 ✅ |
| DAT_0806cdbc | 0x0806cdbc | 0x00001404 | 0x00001404 ✅ |
| DAT_0806cdc8 | 0x0806cdc8 | 0x0000176a | 0x0000176a ✅ |
| DAT_0806ce1c | 0x0806ce1c | 0x00008020 | 0x00008020 ✅ |
| DAT_0806ce64 | 0x0806ce64 | 0x00008020 | 0x00008020 ✅ |
| DAT_0806cf34 | 0x0806cf34 | 0x0201bb90 | 0x0201bb90 ✅ |
| DAT_0806d120 | 0x0806d120 | 0x0201e1c8 | 0x0201e1c8 ✅ |
| DAT_0806d138 | 0x0806d138 | 0x0000138a | 0x0000138a ✅ |
| DAT_0806d13c | 0x0806d13c | 0x0000156a | 0x0000156a ✅ |
| DAT_0806d28c | 0x0806d28c | 0x0000138d | 0x0000138d ✅ |
| DAT_0806d1d8 | 0x0806d1d8 | 0x000004a4 | 0x000004a4 ✅ |
| DAT_0806d44c | 0x0806d44c | 0x0201e2a0 | 0x0201e2a0 ✅ |
| DAT_0806d510 | 0x0806d510 | 0x0201c8f8 | 0x0201c8f8 ✅ |
| DWORD_0806d67c | 0x0806d67c | 0x00001ce8 | 0x00001ce8 ✅ |
| DWORD_0806d678 | 0x0806d678 | gP1LifePoints | ROM=0x0201c4e0 = gP1LifePoints ✅ |
| DAT_0806d76c | 0x0806d76c | 0x00001cb8 | 0x00001cb8 ✅ |
| DWORD_0806d610 | 0x0806d610 | 0x00000868 | 0x00000868 ✅ |
| DWORD_0806d614 | 0x0806d614 | 0x0201c510 | 0x0201c510 ✅ |
| DAT_0806d6bc | 0x0806d6bc | 0x00001ce8 | 0x00001ce8 ✅ |
| DAT_0806d850 | 0x0806d850 | 0x00001ce8 | 0x00001ce8 ✅ |
| DAT_0806d8bc | 0x0806d8bc | 0x0201c8f8 | 0x0201c8f8 ✅ |

### C5 NEW 4 个常量独立复核

使用 `grep -n "0x0000xxxx" constants/*.inc` 精确按值核查:

| 常量名 | 值 | 扫结果 | CID passcode (card-stats.s) |
|--------|-----|--------|------------------------------|
| MAGIC_CYLINDER_CID | 0x1404 | 0 命中 ✅ NEW | card_0879 @ L11442 slot=0x1404 pw=62279055 Magic Cylinder ✅ |
| DRAINING_SHIELD_CID | 0x176a | 0 命中 ✅ NEW | card_1554 @ L20217 slot=0x176A pw=43250041 Draining Shield ✅ |
| RING_OF_DESTRUCTION_CID | 0x138d | 0 命中 ✅ NEW | card_0802 @ L10441 slot=0x138D pw=83555666 Ring of Destruction ✅ |
| SPRITE_RECORD_P2_SIDE | 0x8020 | 0 命中 ✅ NEW | N/A (sprite attr, oam_attr.inc; OAM_SPRITE_COUNT_P2=0x8025 不同值) ✅ |

### C5 reuse 关键抽查

| 常量名 | 值 | 确认来源 |
|--------|-----|----------|
| PLAYER_BLOCK_STRIDE | 0x868 | ewram.inc:250 ✅ |
| gDuelFieldSlots | 0x0201c510 | ewram.inc:313 ✅ |
| gDuelPhaseFlags | 0x0201b290 | ewram.inc:352 ✅ |
| LP_CARD_TRACK_BASE_OFF | 0x1da8 | ewram.inc:247 ✅ |
| LP_CARD_TRACK_NEXT_OFF | 0x1daa | ewram.inc:248 ✅ |
| LP_ACTIVATION_LINK_FLAG_OFF | 0x10d0 | ewram.inc:481 ✅ |
| gEquipChainSlotRefs | 0x0201bb90 | ewram.inc:316 ✅ |
| gEquipZoneCountTable | 0x0201e1c8 | ewram.inc:396 ✅ |
| VALKYRION_THE_MAGNA_WARRIOR_CID | 0x138a | card_info.inc:726 ✅ |
| PUPPET_MASTER_CID | 0x156a | card_info.inc:1021 ✅ |
| EQUIP_PHASE_FRAME_OFF | 0x4a4 | ewram.inc:435 ✅ |
| gDuelCardCtxBase | 0x0201e2a0 | ewram.inc:218 ✅ |
| gP1HandSlotArray | 0x0201c8f8 | ewram.inc:333 ✅ |
| P1LP_BLOCK2_OFF_1CE8 | 0x1ce8 | ewram.inc:275 ✅ |
| EQUIP_ZONE_COUNT_TABLE_OFF | 0x1cb8 | duel_field.inc:156 (base=gDuelFieldSlots, 域例外已确立 Seg-7) ✅ |
| gP1LifePoints | 0x0201c4e0 | ewram.inc:79 ✅ |

### C11: dispatch_neo_space_placement_by_card_id_and_state 误名独立裁定

**函数体 (0x0806d124) 关键事实**:
1. ldrh r1,[r6,#0x0] 读 effect_node card_id; BST dispatch: CID==0x138a (Valkyrion the Magna Warrior) -> r7=3; CID==0x156a (Puppet Master) -> r7=2; else r7=0  
2. state==0x80 路径: bl count_available_monster_slots (与 r7 比较) → bl check_field_spell_neo_daedalus_group_placeable (0x0803bb7c) → bl invoke_setup_equip_oam_with_attr2  
3. state==0x7f/0x7e 路径: find_hand_slot_idx_by_set_code + check_zone_slot_equip_eligible

**file 08 neo_space 用法调查**:
- `tick_equip_neo_daedalus_sprite_state_machine` (0x08067b5c): plate 写 "Handles Neo Space/Neo-Spacian equip zone sprite state machine", 同样调用 check_field_spell_neo_daedalus_group_placeable, 同样 dispatch 非 Neo Space 卡牌 (Magical Labyrinth/Wall Shadow)
- `tick_neo_space_oam_seq_by_card_id` (0x0806e308): dispatch Multiplication of Ants/Blockman/Phantasmal Martyrs/Dandylion, 同样调用 check_field_spell_neo_daedalus_group_placeable

**结论**: file 08 已建立非正式惯例: "neo_space" 用作 Neo Daedalus group 放置门控域标签, 与 TCG 卡牌 "Neo Space" 无直接对应。card-stats.s 中不存在名为 "Neo Space" 的卡牌。Valkyrion/Puppet Master 与 Neo Space 卡牌无任何 lore 关联, 但与 neo_daedalus group 放置机制关联一致 (共享 check_field_spell_neo_daedalus_group_placeable 门控)。

**裁定**: executor 保守不改 (FUNC_RENAME=0, med confidence) 成立。file 08 内 neo_space 是已确立的域名约定, 不属于函数体矛盾式误名。**不要求 FUNC_RENAME**。

注: plate 中写 "Neo-Space card placement" 而非 "Neo Daedalus group placement" 存在轻微表述张力, 但这是 naming phase 已定的约定, refine 阶段无充分证据推翻 (无 card 名直接矛盾, 同 file 三函数同一惯例)。

### C8: stale FUN_ 确认

L20975: `FUN_08071404` → `enqueue_equip_sprite_guarded_by_zone_type13`  
确认: asm/09_equip_lp_display.s:L5724: `enqueue_equip_sprite_guarded_by_zone_type13:` @ 0x08071404 ✅

L21181: `FUN_08071d64` → `dispatch_spirit_monster_zone_sprite_by_card_id`  
确认: asm/09_equip_lp_display.s:L6819: `dispatch_spirit_monster_zone_sprite_by_card_id:` @ 0x08071d64 ✅

无其他 stale FUN_ (全段扫描精确 2 处)。

### C9: ASCII 核查

- L20806: 318 字节非 ASCII (UTF-8 CJK), 唯一非 ASCII 行, proposal PLATE#3 计划 ASCII 重写 741 字符 ✅
- 741 字符替换文本: 独立核查 0 非 ASCII chars ✅; 语义关键词全部命中 (check_effect_slot_matches_zone_entry / read_effect_slot_side_and_type / invoke_effect_node_with_active_flag_3arg / sample_prng_scaled / 0x1d40 / invoke_card_display_op_0x31_sub8(0x38) / enqueue_lp_display_row_type17 / 0x1daa / invoke_equip_slot_eligibility_via_effect_node_bitmap) ✅
- 12 RENAME EOL: 无非 ASCII (python 扫描确认) ✅

### C13: 残留 100% 覆盖

python 精确清点: Seg-9 lines 19718..21595 内 DAT_/DWORD_/PTR_gP1LifePoints_/UNK_ (addr in [0x0806cbe8, 0x0806d960)) = **63 个**。  
EQ 表 = 51 个; RENAME 表 = 12 个; 并集 = 63 个。无遗漏, 无越界, 无重复。

---

## 状态: PASS

所有 C1-C13 检查通过。无需修改。

---

## 修改清单

无 (PASS 状态)。

---

## Fixer 落地备注 (供参考)

- PLATE#3 L20806: ASCII 重写 741 字符替换 CJK mojibake; Ghidra setPlateComment 时须用 proposal 中的 ASCII 文本
- PLATE#1 L20975: FUN_08071404 → enqueue_equip_sprite_guarded_by_zone_type13
- PLATE#2 L21181: FUN_08071d64 → dispatch_spirit_monster_zone_sprite_by_card_id
- card_info.inc 新增 3 CID (MAGIC_CYLINDER_CID/DRAINING_SHIELD_CID/RING_OF_DESTRUCTION_CID)
- oam_attr.inc 新增 1 (SPRITE_RECORD_P2_SIDE=0x8020)
- EQ 51 槽, RENAME 12 槽 (gp1lifepoints_0806xxxx 命名格式)
- FUNC_RENAME=0 (dispatch_neo_space_placement_by_card_id_and_state 保持现名)
