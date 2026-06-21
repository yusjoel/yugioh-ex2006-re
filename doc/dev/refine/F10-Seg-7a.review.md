# Refine Review: F10-Seg-7a [0x08080ba0..0x08081900)

Reviewer: independent re-scan (iteration 2)
Date: 2026-06-21
Proposal: `doc/dev/refine/F10-Seg-7a.proposal.md`

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 范围与 §五 路线图一致 | OK | refine-progress.md 确认 Seg-6 终于 0x08080ba0; 7a 从 0x08080ba0 起到 0x08081900; 无跳号回头 |
| C2 Rule2 | ROM_INCBIN/.byte 全有归宿 | OK | 段内 0 个 ROM_INCBIN, N/A |
| C3 Rule3 | §5.1 块确 0 引用 | OK | 无 §5.1 块, N/A |
| C4 R1 值 | EQ value == ROM 4B LE | OK | 独立 python 复核 28 个代表性槽 (含 c30/c94/c38/c98/d14/d68/f14/fb4/fd0/1008/1058/142c/17bc/1880/18a0/18d4/10b4 + 27 个 NEW CID 槽) 全部匹配 |
| C5 R1 复用 | 新建 constants 前无可复用 | OK | 31 个 NEW 卡 CID 全部 0-hit in ALL constants/*.inc; 0xfffffe00 在 oam_attr.inc 存在为 OAM_ATTR1_X_CLEAR 但语义不同 (stack 负值 vs OAM 位掩码) 已由 iter-1 审核裁定允许新建; 0x00000119 在 gba_mem.inc 存在为 RESULT_SCREEN_FONT_CTX_OFF 但语义不同 (op sub-id vs struct offset) 同裁定允许新建; 3 个非 CID 新常量 (EFFECT_SLOT_TYPE_CLEAR_MASK/STACK_ALLOC_NEG_512/EQUIP_DISP_OP_ID_0x119) 均通过全 constants 扫描 |
| C6 R2 名 | 槽名合法, 无碰撞 | OK | 所有新名 format ^[a-z][a-z0-9_]+$ 合规; 中性名 cid_128a/cid_1326/cid_127/cid_125 合规; 无重名 |
| C7 R3 接通 | 无需 carve/全局槽 | OK | 无 ROM_INCBIN, 无 REF_SLOTS, N/A |
| C8 R5 现名 | plate 无残留 FUN_ | WARN | ASM 段内 26 处 FUN_ 残留需修复: FUN_08080ea0→dispatch_equip_card_display_op_by_card_id (25x); FUN_08080d28→pack_equip_slot_sprite_with_code_attr (1x); FUN_08081de4 是 Seg-7b 函数留 7b 处理; 提案已列出所有 C8 替换计划 |
| C9 ASCII | plate/EOL 纯 ASCII | OK | 提案 PLATE 节及 setPlateComment 文本中无 CJK; 提案本身 doc/ 中文标题不计 |
| C10 carve | 无指针表 | OK | 无 ROM_INCBIN, N/A |
| C11 误名 | 无 FUNC_RENAME 漏项 | OK | 9 个主函数名与函数体操作一致, 无新发现误名 |
| C12 R6 | 关键槽消费者证据 | OK | 5 个关键常量有 file:line + 置信度证据 (EFFECT_SLOT_TYPE_CLEAR_MASK/DEMO_CLEAR_BITS_15_14/DUAL_LABEL_RENDER_STATE_CLEAR/STACK_ALLOC_NEG_512/HANE_HANE_INTERNAL_ID_0x1f5); HANE_HANE_INTERNAL_ID_0x1f5 确认为 icid 参数不是 CID (asm L16519/16523 证实) |
| C13 残留 | 段内所有自动名槽全覆盖 | OK | 独立 python 扫描: 段内 DAT_/DWORD_ 共 101 个; 提案 EQ 表 93 primary + 8 secondary = 101, 无缺漏; DAT_08081948 已正确排除在 7a 外 |

---

## 各项独立核验结果

### 1. 57 项 iter-1 修正已全部落地 (验证)

- 4 个中性名 (cid_128a/cid_1326/cid_127/cid_125): 提案正确列出, ROM 字节核对 OK
- 43 个 REUSE 名称: 全部改为 card_info.inc 中的正确现有常量名; 逐一 python 对照核对 33 项全部 OK
- DISPLAY_CODE_CLEAR_MASK -> DUAL_LABEL_RENDER_STATE_CLEAR: 提案已正确改写
- DWORD_08081008 -> EQ COPYCAT_CID (不做 RENAME): 提案正确
- #A1/A2/A3 三个缺漏槽补入: DAT_08080c94/c98/080818a0 均已在 EQ 表中
- #A4 DAT_08081948 移出: 提案已移除, RENAME_SLOTS 为空

### 2. NEW 常量独立核验 (不信提案结论)

**31 个 NEW 卡 CID:**

全部通过以下双重验证:
(a) grep constants/*.inc 按值 -> 0-hit 确认无可复用
(b) grep data/card-stats.s slot=0x{val:04x} -> 找到对应条目, 卡名与提案常量名匹配

| 常量名 | 值 | card-stats.s 槽行 | 卡名 | 核验 |
|--------|------|---------------------|------|------|
| SPIRIT_REAPER_CID | 0x1596 | card_1178 | Spirit Reaper | OK |
| RAIGEKI_BREAK_CID | 0x15a8 | card_1195 | Raigeki Break | OK |
| TRAP_MASTER_CID | 0x1086 | card_0211 | Trap Master | OK |
| MAN_EATER_BUG_CID | 0x119b | card_0418 | Man-Eater Bug | OK |
| THE_RELIABLE_GUARDIAN_CID | 0x132a | card_0721 | The Reliable Guardian | OK |
| REINFORCEMENTS_CID | 0x12f1 | card_0676 | Reinforcements | OK |
| DUST_TORNADO_CID | 0x137c | card_0792 | Dust Tornado | OK |
| KRYUEL_CID | 0x139e | card_0815 | Kryuel | OK |
| MASK_OF_DISPEL_CID | 0x13f0 | card_0862 | Mask of Dispel | OK |
| THOUSAND_KNIVES_CID | 0x142e | card_0912 | Thousand Knives | OK |
| COLLECTED_POWER_CID | 0x148d | card_0971 | Collected Power | OK |
| VISER_DES_CID | 0x14ac | card_0996 | Viser Des | OK |
| RYU_KISHIN_CLOWN_CID | 0x14bb | card_1006 | Ryu-Kishin Clown | OK |
| DOUBLE_SNARE_CID | 0x14c3 | card_1012 | Double Snare | OK |
| COLLAPSE_CID | 0x14eb | card_1051 | Collapse | OK |
| BOOK_OF_MOON_CID | 0x1538 | card_1117 | Book of Moon | OK |
| MONSTER_RELIEF_CID | 0x1579 | card_1153 | Monster Relief | OK |
| A_MAN_WITH_WDJAT_CID | 0x158e | card_1170 | A Man with Wdjat | OK |
| SOUL_TAKER_CID | 0x166f | card_1348 | Soul Taker | OK |
| GUARDIAN_CEAL_CID | 0x164b | card_1316 | Guardian Ceal | OK |
| GALE_LIZARD_CID | 0x16ba | card_1406 | Gale Lizard | OK |
| COMPULSORY_EVACUATION_DEVICE_CID | 0x171a | card_1490 | Compulsory Evacuation Device | OK |
| SHIELD_CRASH_CID | 0x1773 | card_1559 | Shield Crash | OK |
| GRANMARG_THE_ROCK_MONARCH_CID | 0x185f | card_1760 | Granmarg the Rock Monarch | OK |
| CATNIPPED_KITTY_CID | 0x1863 | card_1764 | Catnipped Kitty | OK |
| ASSAULT_ON_GHQ_CID | 0x188a | card_1801 | Assault on GHQ | OK |
| PATROID_CID | 0x18f0 | card_1874 | Patroid | OK |
| VW_TIGER_CATAPULT_CID | 0x1953 | card_1954 | VW-Tiger Catapult | OK |
| KARMA_CUT_CID | 0x19db | card_2062 | Karma Cut | OK |
| GENERATION_SHIFT_CID | 0x19dd | card_2064 | Generation Shift | OK |

注: GENERATION_SHIFT_CID 提案中 pw=34460219 与 card-stats.s pw=34460239 有一位数字差异,
但 slot=0x19dd 与常量名均正确; 此为 doc comment 中密码数值的笔误, 不影响 EQ 值正确性.

**4 个中性 CID (不在 card-stats.s 中):**

cid_128a (0x128a) / cid_1326 (0x1326) / cid_127 (0x0127) / cid_125 (0x0125)
全部 grep card-stats.s slot= 0-hit, 确认不在 card-stats.s 中. 中性名正确.

**HANE_HANE_INTERNAL_ID_0x1f5 (0x1f5):**

grep card-stats.s slot=0x01f5 -> 0-hit. 这不是一个 card CID, 而是 trigger_card_display_op_with_card_name_0x6c
中传给 card_name_lookup_by_internal_id 的内部查找 ID (asm L16519/16523 确认 icid=0x1f5). 名称准确.
grep constants/*.inc 0x000001f5 -> 0-hit. 正确新建.

**3 个非 CID 新常量:**

- EFFECT_SLOT_TYPE_CLEAR_MASK = 0xffffc01f: grep constants/*.inc -> 0-hit. 新建于 duel_field.inc. OK
- STACK_ALLOC_NEG_512 = 0xfffffe00: 在 oam_attr.inc 有 OAM_ATTR1_X_CLEAR 但语义不同
  (stack frame -0x200 负值 vs OAM attr1 x-pos 清零掩码). 允许新建 (iter-1 裁定维持).
- EQUIP_DISP_OP_ID_0x119 = 0x00000119: 在 gba_mem.inc 有 RESULT_SCREEN_FONT_CTX_OFF 但语义不同
  (display op sub-id vs struct offset). 允许新建 (iter-1 裁定维持).

### 3. C4 ROM 字节核对 (独立 python)

28 个代表性槽: 全部 OK. 关键摘要:
- 0x08080c30/c94 = 0xffffc01f (EFFECT_SLOT_TYPE_CLEAR_MASK) OK
- 0x08080c38/c98 = 0xffff3fff (DEMO_CLEAR_BITS_15_14) OK
- 0x08080d14/d68 = 0xfffc7fff (DUAL_LABEL_RENDER_STATE_CLEAR) OK
- 0x08080f14 = 0xfffffe00 (STACK_ALLOC_NEG_512) OK
- 0x08081008 = 0x000012bb (COPYCAT_CID) OK
- 0x08081058 = 0x0000132a (THE_RELIABLE_GUARDIAN_CID) OK
- 0x0808142c = 0x0000164b (GUARDIAN_CEAL_CID) OK
- 0x08081788/18c4 = 0x00000119 (EQUIP_DISP_OP_ID_0x119) OK
- 0x080817bc = 0x000001f5 (HANE_HANE_INTERNAL_ID_0x1f5) OK
- 0x08081880/18a0 = 0x00000127 (cid_127) OK
- 0x080818d4 = 0x00000125 (cid_125) OK

### 4. C13 槽覆盖 (独立计数)

python 扫描 asm/10_equip_effect_dispatch.s 行 14662-16793:
- 唯一 DAT_/DWORD_ 地址在 [0x08080ba0, 0x08081900) 范围内: **101 个**
- 提案 EQ 表 (93 primary + 8 secondary): **101 个**
- 差集: 空. 全覆盖确认.

---

## 状态: PASS

---

## 执行备注 (给 fixer)

1. GENERATION_SHIFT_CID 新常量 comment 中 pw 应为 34460239 (card-stats.s 实值), 非 34460219. 可在 fixer 写 card_info.inc 时直接使用正确值.
2. C8: FUN_08081de4 出现于 asm L15054 (find_effect_slot_by_side_and_type 的 plate), 该函数是 Seg-7b 函数尚未命名, 留待 Seg-7b 处理时一并修复.
3. STACK_ALLOC_NEG_512 放入 duel_field.inc (不是 oam_attr.inc, 语义不同).
4. EQUIP_DISP_OP_ID_0x119 放入 duel_field.inc (不是 gba_mem.inc, 语义不同).
5. EFFECT_SLOT_TYPE_CLEAR_MASK 放入 duel_field.inc (新建, 非 oam_attr.inc).
6. 所有 31 个新 CID 常量放入 card_info.inc.
7. 4 个中性名 (cid_128a/cid_1326/cid_127/cid_125) 放入 card_info.inc, EOL: "equip BST unassigned slot".
