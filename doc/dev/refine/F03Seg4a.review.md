# Refine Review: F03Seg4a

## 段范围
`[0x08037904, 0x08037ec0)` — `asm/03_equip_chain_hand.s` Seg-4 前半  
前置 Seg: Seg-3 (commit b90b81f) ✅

---

## 核验矩阵 (C1-C13) — 第 2 轮

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致 | ✅ | refine-progress.md: 下一任务 file 03 Seg-4 (0x37904..0x3a7f0)；Seg-4a [0x37904..0x37ec0) 拆分正确续接 Seg-3 |
| C2 Rule2 | 段内所有 ROM_INCBIN/.byte 块有归宿 | ✅ | Seg-4a 内无 ROM_INCBIN；Seg-4b incbin @0x39350/0x10ce ref-scan 前置报告完整 (R4 disasm 留 Seg-4b) |
| C3 Rule3 | §5.1 块确 0 引用 | N/A | Seg-4a 无 §5.1 登记块 |
| C4 R1 值 | 每个 EQ value == ROM 4 字节小端 | ✅ | 独立 python 核对全部 43 个槽 (32 EQ + 11 REF), 43/43 匹配；详见下方字节核对记录 |
| C5 R1 复用 | 新建 constants 前无现有同值 | ✅ | 扫描全部 19 个 constants/*.inc：9 个新 CID 值 (0x137b/0x17e7/0x135e/0x1346/0x10f5/0x1344/0x1349/0x159d/0x183f) + 0xffffef10 + 0xfffffe70 均无重复（rom_data.inc 中 card_137B=0x09831648 是 ROM 指针，非 CID，无碰撞）|
| C6 R2 名 | 槽名格式 + 无碰撞 | ✅ | 全 43 个槽名符合 `^[a-z][a-z0-9_]+$`；独立验证无重复（compute_zone_effect_atk_delta_table_base 仅出现于 DAT_08037ddc 一个槽，RENAME+REF 共享同名属同一槽不构成碰撞）|
| C7 R3 接通 | REF 槽有 USER-label + DATA-ref 计划 | ✅ | 10 个 PTR_gP1LifePoints_* 槽均有 `<func>_lp_ptr` 命名计划指向 gP1LifePoints；DAT_08037ddc 有 createLabel field_spell_atk_bonus_table @0x09e3ef74 USER + addMemoryReference from 0x08037ddc 计划 |
| C8 R5 现名 | plate 无残留 FUN_ | ✅ | 2 处 STALE_FUN 均给出替换 plate 文本 (FUN_080ae050→find_empty_slot_for_card_id_dispatch / FUN_08037c20→shuffle_hand_by_player_deck_flag)；新 plate 文本块无 FUN_ |
| C9 ASCII | plate/EOL 文本纯 ASCII | ✅ | 3 个 plate 文本代码块 (count_field_zone_cards_by_field6 / count_monster_slots_field5_ge_threshold / get_player_deck_flag_bit1) 全部纯 ASCII；doc/ prose 中的 CJK 是分析说明，不进 Ghidra |
| C10 carve | 指针表 +1 核对 | N/A | field_spell_atk_bonus_table 是数据表非 fn-ptr，正确不 +1；Seg-4a 无其他 carve |
| C11 误名 | 函数体 vs 函数名矛盾已标 FUNC_RENAME | ✅ | **#2 已修正**：FUNC_RENAME 节已添加 count_gy_cards_by_field6→count_field_zone_cards_by_field6；函数体读 gP1LP+0x120 (field_zone array C) 非墓地 (+0x5d0)；lp_ptr 槽 label 同步改为 count_field_zone_cards_by_field6_lp_ptr；plate 文本更新为 "field zone array C"；落地说明含 ExportFunctionInventory+CSV sync |
| C12 R6 | 关键槽语义有 file:line + 置信度证据 | ✅ | **#3 已修正**：4 处 card_XXXX 引用全部订正 (EYE_OF_TRUTH→card_0791/RESPECT_PLAY→card_0766/NECROVALLEY→card_1185/HARPIES_HUNTING_GROUND→card_1731)；独立 card-stats.s grep 验证；EQ 表 + card_info.inc comment + R6 表三处均已更正 |
| C13 残留 | 段内所有残留自动名槽被覆盖 | ✅ | asm/03 grep 确认段内恰好 43 个 DAT_/PTR_ label 定义；EQ=32 + REF=11 = 43，一一对应；RENAME=33 (43 - 10 PTR_gP1LifePoints_* = 33，覆盖全部 EQ 槽) |

### carve 专项核验

| 项 | 结果 | 备注 |
|----|------|------|
| C-carve #1 rom.s 接入点 | ✅ | rom.s line 1236: `.incbin "roms/2343.gba", 0x1E3EF74, 0xAD98` 存在且与计划一致；available_slot_order_table 末尾 (0x09e3ef60+0x14=0x09e3ef74) 紧接无间隙 |
| C-carve #1 拆分等式 | ✅ | 0x120 + 0xAC78 = 0xAD98 ✓；0x1E3EF74 + 0x120 = 0x1E3F094 ✓ |
| C-carve #1 ref-scan | ✅ | 独立 python: raw=1 (来自 0x08037ddc), THUMB\|1=0；GBA 0x09e3ef74 = file 0x1e3ef74 映射正确 |
| C-carve #1 表内容 | ✅ | 6 rows × 24 s16; row 5 (Yami): col3=+200, col17=-200, col18=+200；stride=0x30 = 6×0x30=0x120 ✓ |
| C-carve #1 DAT_08037ddc 改 REF | ✅ | proposal 中 DAT_08037ddc 已在 REF_SLOTS (not EQ_SLOTS)；slot_label=compute_zone_effect_atk_delta_table_base |
| C-carve #1 field_spell_bonus.inc | ✅ | 新建 inc 仅含 FIELD_SPELL_TABLE_IDX_BIAS + ZONE_EFFECT_ATK_PENALTY_500 两项；无 FIELD_SPELL_ATK_BONUS_TABLE .equ（改 carve label）|

---

## 自主复核记录 (第 2 轮)

### EQ 值字节核对 (python 独立验证)

全部 43 槽 (`struct.unpack_from('<I', d, addr-0x08000000)`) 核对结果 43/43 匹配:
- 32 EQ 槽：15×PLAYER_BLOCK_STRIDE(0x868), 4×gDuelFieldSlots/gP1FieldArrayCBase, 1×P1LP_BLOCK2_OFF_1CE8, 9 CID, 2 field_spell constants, 4×ZONE_EFFECT_ATK_PENALTY_500
- 11 REF 槽：10×gP1LifePoints(0x0201c4e0), 1×field_spell_atk_bonus_table(0x09e3ef74)

### C13 残留计数

asm/03 段内 [0x37904..0x37ec0) grep 统计:
- `^DAT_08037` 定义 labels: 33 个
- `^PTR_.*08037` 定义 labels: 10 个
- 合计: 43 个，与 EQ=32 + REF=11 = 43 一致 ✓

### card-stats.s 卡牌 ID 独立验证 (第 2 轮)

| CID 值 | 正确 card 标号 | proposal 引用 | 一致 |
|--------|--------------|---------------|------|
| 0x137b | card_0791 slot=0x137B line 10298 | card_0791 | ✅ |
| 0x17e7 | card_1652 slot=0x17E7 line 21491 | card_1652 | ✅ |
| 0x135e | card_0766 slot=0x135E line 9973 | card_0766 | ✅ |
| 0x1346 | card_0747 slot=0x1346 | card_0747 | ✅ |
| 0x10f5 | card_0297 slot=0x10F5 | card_0297 | ✅ |
| 0x1344 | card_0745 slot=0x1344 | card_0745 | ✅ |
| 0x1349 | card_0750 slot=0x1349 | card_0750 | ✅ |
| 0x159d | card_1185 slot=0x159D line 15420 | card_1185 | ✅ |
| 0x183f | card_1731 slot=0x183F line 22518 | card_1731 | ✅ |

### FUNC_RENAME 体验证 (第 2 轮)

asm/03 lines 3596-3643 (count_gy_cards_by_field6):
- `movs r4,#0x90; lsls r4,#0x1` → r4=0x120 = gP1FieldArrayCBase offset
- count 来自 `adds r0,r3,#0; adds r0,#0xc` → gP1LP+player*0x868+0x0c
- graveyard 在 +0x5d0 (count +0x1c), 两套 offset 确实不同
- "gy" 名与函数体矛盾已标 FUNC_RENAME ✓

---

## 附加说明

### 轻微文档不一致 (不影响 PASS 判定)

carve 计划 line 378: "同步删除 field_spell_bonus.inc 中的 FIELD_SPELL_ATK_BONUS_TABLE .equ 行" — 该 inc 是新建文件，无需删除操作。fixer 落地时直接创建仅含 FIELD_SPELL_TABLE_IDX_BIAS + ZONE_EFFECT_ATK_PENALTY_500 的 inc 文件即可，无需理会此删除指令。

---

## 状态: PASS

全部 C1-C13 及 C-carve 专项通过。三项 round-1 修正均已正确落实到 proposal:
- #1 carve: DAT_08037ddc 由 EQ 改 REF carve；field_spell_bonus.inc 仅含 2 纯数值常量；rom.s 拆分方案数学正确
- #2 FUNC_RENAME: count_gy_cards_by_field6→count_field_zone_cards_by_field6 节完整；lp_ptr 槽同步；落地步骤完整
- #3 evidence: 4 处 card_XXXX 全部订正为正确序号

---

## Reviewer Verdict: F03Seg4a = PASS
