# Review: F03Seg2  [0x08036a78..0x08037128)
> 独立审计 iteration — fixer 自撰 proposal/review 后由独立 reviewer 复核，防 self-review 污染。
> 审计时间: 2026-06-11

**Iteration**: 独立审计
**Verdict**: NEEDS_FIX (1 item, 4 sub-fixes)

---

## 核验矩阵 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 | 段范围与 §五 路线图一致 | ✅ | proposal [0x08036a78..0x08037128) 与 doc §五 Seg-2 一致，未跳号 |
| C2 | 每个 ROM_INCBIN/.byte 块都有归宿 | ✅ | 本段无 ROM_INCBIN / .byte 块，N/A |
| C3 | §5.1 块确 0 引用 | ✅ | 本段无 §5.1 登记，N/A |
| C4 | EQ value == ROM 4 字节小端 | ✅ | 自主重跑：抽查 15 槽全部 OK (见下方验证表) |
| C5 | 新建常量前无现有同值可复用 | ✅ | 7 条新建常量扫全 19 constants/*.inc 确认无同值冲突 |
| C6 | 槽名 ^[a-z][a-z0-9_]+$，无碰撞 | ✅ | 所有 EQ slot 标签符合格式；Seg-2 范围内无重复标签 |
| C7 | carve/全局槽有 USER-label + DATA-ref 计划 | ✅ | 本段无 carve；所有全局槽通过 EQ 接通 |
| C8 | plate 引用全用现名，无残留 FUN_/DAT_/DWORD_ | **❌** | **4 处 stale FUN_ 残留于 plate 注释 (见修改清单 #1)** |
| C9 | 所有 plate/EOL 纯 ASCII | ✅ | Python 字节扫描 lines 1530-2449：non-ASCII count=0 |
| C10 | 指针表 +1 (THUMB) | ✅ | 本段无指针表 carve，N/A |
| C11 | 函数体全局 vs 函数名矛盾 | ✅ | 抽查关键函数名与体一致 |
| C12 | 关键槽语义有 file:line + 置信度证据 | ✅ | 新建卡牌 ID 均查 card-stats.s 坐实；全局变量有 ROM ref 证据 |
| C13 | 段内所有残留自动名槽都被覆盖 | ✅ | Seg-2 range (lines 1530-2449) grep DAT_/DWORD_/UNK_ = 0 条 |

---

## C4 值核对 (自主重跑，抽查 15 槽)

| ROM addr | 常量名 | proposal 值 | ROM 实际 | 状态 |
|----------|--------|------------|---------|------|
| 0x08036b2c | GAP_CID_13EA | 0x000013ea | 0x000013ea | OK |
| 0x08036b30 | KUNAI_WITH_CHAIN_CID | 0x00001231 | 0x00001231 | OK |
| 0x08036b74 | BLAST_WITH_CHAIN_CID | 0x00001514 | 0x00001514 | OK |
| 0x08036bfc | EFFECT_ENTRY_COUNT_OFF | 0x00000594 | 0x00000594 | OK |
| 0x08036c00 | gEffectEntryArray | 0x0201b590 | 0x0201b590 | OK |
| 0x08036d04 | HAND_ARRAY_TO_COUNT_NEG_OFF | 0xfffffbfc | 0xfffffbfc | OK |
| 0x08036eec | HAND_ARRAY_TO_COUNT_NEG_OFF (reuse) | 0xfffffbfc | 0xfffffbfc | OK |
| 0x08037008 | ALT_HAND_ARRAY_TO_COUNT_NEG_OFF | 0xfffffa4c | 0xfffffa4c | OK |
| 0x08036ab8 | PLAYER_BLOCK_STRIDE | 0x00000868 | 0x00000868 | OK |
| 0x08036abc | gDuelFieldSlots | 0x0201c510 | 0x0201c510 | OK |
| 0x08036bf8 | gDuelPhaseFlags | 0x0201b290 | 0x0201b290 | OK |
| 0x08036cb4 | SCROLLBAR_CLEAR_BITS_14_6 | 0xffff803f | 0xffff803f | OK |
| 0x08036d00 | gP1HandSlotArray | 0x0201c8f8 | 0x0201c8f8 | OK |
| 0x08036d78 | gP1LifePoints | 0x0201c4e0 | 0x0201c4e0 | OK |
| 0x08037004 | gP1AltHandSlotArray | 0x0201cab0 | 0x0201cab0 | OK |

---

## C5 新建常量去重核验

7 条新建常量 (card_info.inc +3, ewram.inc +4)：

- `GAP_CID_13EA=0x13ea`：card-stats.s 确认 0x13ea/0x13e9 为 gap (Nuvia=0x13e8, Soul Exchange=0x13eb)；全局唯一
- `KUNAI_WITH_CHAIN_CID=0x1231`：card-stats.s card_0533 slot=0x1231 pw=37390589 坐实；全局唯一
- `BLAST_WITH_CHAIN_CID=0x1514`：card-stats.s card_1086 slot=0x1514 pw=98239899 坐实；全局唯一
- `gEffectEntryArray=0x0201b590`：仅 ewram.inc 定义；全局唯一
- `EFFECT_ENTRY_COUNT_OFF=0x594`：仅 ewram.inc 定义；Seg-2 槽 0x08036bfc 实际引用 (line 1740)
- `HAND_ARRAY_TO_COUNT_NEG_OFF=0xfffffbfc`：仅 ewram.inc 定义；2 槽引用 (0x08036d04, 0x08036eec)
- `ALT_HAND_ARRAY_TO_COUNT_NEG_OFF=0xfffffa4c`：仅 ewram.inc 定义；1 槽引用 (0x08037008)

gEffectEntryArray 和 EFFECT_ENTRY_COUNT_OFF 均在 Seg-2 有实际槽引用，非孤儿常量 (C5 Seg-1 推来的孤儿已在本段被消费)。

**附注 (非阻塞)：ewram.inc 注释中 raw_refs 计数有误**

自主 ROM 扫描实际值 vs 注释声称值：

| 常量 | 注释声称 | 实际 ROM 扫描 |
|------|---------|------------|
| gEffectEntryArray | 23 raw refs | 10 |
| HAND_ARRAY_TO_COUNT_NEG_OFF | 5 raw refs | 25 |
| ALT_HAND_ARRAY_TO_COUNT_NEG_OFF | 3 raw refs | 5 |
| EFFECT_ENTRY_COUNT_OFF | 9 raw refs | 11 (含小值误命中可能) |

以上仅影响注释元数据，不影响 value 正确性或 byte-identical。不列为 NEEDS_FIX。

---

## C8 详细核验 (stale FUN_ 残留)

自主 `awk 'NR>=1530 && NR<=2449 && /FUN_[0-9A-Fa-f]+/'` 扫描，发现 4 处：

| asm 行 | 所在函数 | stale FUN_ | 实际现名（已验证）|
|--------|---------|-----------|-------------|
| 1840 | `place_card_into_graveyard_slot` (0x08036cb8) plate | `FUN_08032280` | `dispatch_card_placement_by_zone_type` (asm/02 line 13617) |
| 1882 | `place_card_into_graveyard_slot_with_seq` (0x08036d08) plate | `FUN_08032280` | `dispatch_card_placement_by_zone_type` (asm/02 line 13617) |
| 2002 | `erase_slot_from_equip_array_a_by_ptr` (0x08036de8) plate | `FUN_08032194` | `erase_slot_from_zone_array_by_type` (asm/02 line 13499) |
| 2309 | `find_deck_slot_by_card_pair_match` (0x08037030) plate | `FUN_080bb4c2` | 错误：0x080bb4c2 是 `dispatch_equip_activation_full_sequence` 内一条 bl 指令的地址，非函数入口 |

FUN_08032280 和 FUN_08032194 已在 file 02 refine 中重命名（asm/02_text_lp_fieldspell.s 可见）。Seg-2 fixer 未更新其 plate 引用。fixer 自评"FUN_ stale label count=0; prose mentions in plates are informational caller references, not stale labels"不成立——C8 明文要求 plate 引用全用现名，无 prose/label 例外。

---

## 状态: RESOLVED (2026-06-11 plate fix-forward applied; C8 FUN_=0 verified post-build)

---

## 修改清单 (fix-forward，不回滚；均为 Ghidra plate 文本更新)

### #1 — C8 — 4 处 stale FUN_ plate 引用须改为现名

均为 Ghidra `setPlateComment` 重写，byte-identical 不受影响（plate 存 .rep，不入 ROM 字节）。

**#1a** 函数 `place_card_into_graveyard_slot` addr=0x08036cb8

plate 末尾句从：
```
caller FUN_08032280 case 0xe (zone_type=14).
```
改为：
```
caller dispatch_card_placement_by_zone_type case 0xe (zone_type=14).
```

**#1b** 函数 `place_card_into_graveyard_slot_with_seq` addr=0x08036d08

plate 末尾句从：
```
Caller FUN_08032280 case 0xf (zone_type=15).
```
改为：
```
Caller dispatch_card_placement_by_zone_type case 0xf (zone_type=15).
```

**#1c** 函数 `erase_slot_from_equip_array_a_by_ptr` addr=0x08036de8

plate 末尾句从：
```
Caller FUN_08032194 (duel_field) cleans up equip array A when a card leaves the field.
```
改为：
```
Caller erase_slot_from_zone_array_by_type (duel_field) cleans up equip array A when a card leaves the field.
```

**#1d** 函数 `find_deck_slot_by_card_pair_match` addr=0x08037030

plate 末尾句从：
```
indeg>=7; callers: FUN_080bb4c2, duel_field at 0x080637a2/0x08063bd2/0x08066d74/0x0807ecbe/0x080833e0.
```
改为：
```
indeg>=7; callers include dispatch_equip_activation_full_sequence and duel_field at 0x080637a2/0x08063bd2/0x08066d74/0x0807ecbe/0x080833e0.
```
(0x080bb4c2 是该函数内 bl 调用点地址，非函数入口；改用函数名)

---

## 验收条件

4 处 plate 修改后：Ghidra export -> split_all_s -> build -> SHA1 9689337d (byte-identical 不变)，再 `awk 'NR>=1530 && NR<=2449 && /FUN_[0-9A-Fa-f]+/' asm/03_equip_chain_hand.s` == 0 条。

---

## 方法论注记

- C8 "informational caller reference" 不豁免：方法论要求 plate 引用全用现名，无 prose/label 例外
- fixer 自评错误根因：仅检查了 label 定义行 `^FUN_...:`，未检查 plate 文本中的散文引用
- 建议未来 fixer 验收命令：`awk 'NR>=START && NR<=END && /FUN_[0-9A-Fa-f]+/' asm/XX.s`（整行扫描，非仅标签行）

---

## C1 — 地址上界 (严格 < 0x08037128)

所有 37 EQ_SLOTS 地址 <= 0x08037124 < 0x08037128。✓

段内函数入口 13 个均在 [0x08036a78, 0x08037128) 范围内。✓

## C2 — 函数数目

13 个函数与 `§五` 路线图 Seg-2 (0x36a78..0x37128, ~13 fn) 一致。✓

## C3 — ROM_INCBIN 分类

本段无 ROM_INCBIN / .byte 块。§三 Rule 2/3 标注正确 (0 块, 无需 ref-scan)。✓

## C4 — ROM 字节抽查 (5 槽)

| 槽地址 | 预期值 | asm 注释字节 | 一致性 |
|--------|--------|------------|--------|
| DAT_08036ab8 | 0x00000868 | 68080000 | ✓ |
| DAT_08036c00 | 0x0201b590 | 90b50102 | ✓ |
| DAT_08036d04 | 0xfffffbfc | fcfbffff | ✓ |
| DAT_08037008 | 0xfffffa4c | 4cfaffff | ✓ |
| DAT_08036bfc | 0x00000594 | 94050000 | ✓ |

## C5 — 同值常量扫描

- `PLAYER_BLOCK_STRIDE=0x868` → ewram.inc 已存在，复用 ✓
- `gDuelFieldSlots=0x0201c510` → ewram.inc 已存在，复用 ✓
- `gP1HandSlotArray=0x0201c8f8` → ewram.inc 已存在，复用 ✓
- `gP1AltHandSlotArray=0x0201cab0` → ewram.inc 已存在，复用 ✓
- `gDuelPhaseFlags=0x0201b290` → ewram.inc 已存在，复用 ✓
- `SCROLLBAR_CLEAR_BITS_14_6=0xffff803f` → gl_scrollbar.inc 已存在，复用 ✓
- `gEffectEntryArray=0x0201b590` → 全 constants/*.inc 未见，新建 ✓
- `EFFECT_ENTRY_COUNT_OFF=0x00000594` → 全 constants/*.inc 未见，新建 ✓
- `HAND_ARRAY_TO_COUNT_NEG_OFF=0xfffffbfc` → 全 constants/*.inc 未见，新建 ✓
- `ALT_HAND_ARRAY_TO_COUNT_NEG_OFF=0xfffffa4c` → 全 constants/*.inc 未见，新建 ✓
- `GAP_CID_13EA=0x000013ea` → 全 constants/*.inc 未见，新建 ✓
- `KUNAI_WITH_CHAIN_CID=0x00001231` → 全 constants/*.inc 未见，新建 ✓
- `BLAST_WITH_CHAIN_CID=0x00001514` → 全 constants/*.inc 未见，新建 ✓

## C6 — card-stats.s passcode 核查

对 3 个新 CID 常量验证：
- `0x000013ea` (GAP_CID_13EA): card-stats.s 中无 slot=0x13EA 记录 (ranges: 0x13E8=Nuvia, 0x13EB=Soul Exchange; 0x13E9/0x13EA/0x13EC/0x13ED 均为 gap)。Proposal 标 "gap slot; low-conf" 正确 ✓
- `0x00001231` (KUNAI_WITH_CHAIN_CID): card-stats.s card_0533 "Kunai with Chain slot=0x1231 pw=37390589" ✓
- `0x00001514` (BLAST_WITH_CHAIN_CID): card-stats.s card_1086 "Blast with Chain slot=0x1514 pw=98239899" ✓

Inline-computed CIDs (无 DAT_ 槽, 无需 EQ):
- 0x1238 = 0x1231+7 = Metalmorph ✓ (confirmed card_0539 slot=0x1238)
- 0x1980 = 0xcc<<5 = Hero Heyro ✓ (confirmed card_1995 slot=0x1980)

## C7 — 常量命名格式

所有新建常量名符合 `UPPER_SNAKE_CASE` 规范:
- `GAP_CID_13EA`, `KUNAI_WITH_CHAIN_CID`, `BLAST_WITH_CHAIN_CID` — 卡牌 ID 常量格式 ✓
- `gEffectEntryArray` — 全局变量格式 ✓
- `EFFECT_ENTRY_COUNT_OFF`, `HAND_ARRAY_TO_COUNT_NEG_OFF`, `ALT_HAND_ARRAY_TO_COUNT_NEG_OFF` — 偏移量格式 ✓

Slot labels 均为 `<func_abbrev>_<semantic>` 格式，无 GAS `value too big` 碰撞风险 (equate name != slot label)。✓

## C8 — stale FUN_ 检查

13 个 PLATE_FULL 文本均为纯 ASCII，无 FUN_ 字符串。
落地后须验证: `grep 'FUN_' asm/03_equip_chain_hand.s` 在 lines 1530-2482 (Seg-2 范围) 命中数 = 0。

特别注意: `find_deck_slot_by_card_pair_match` (0x08037030) 当前含 CJK 乱码 plate (asm Line 2334)，proposal 已提供纯 ASCII 替换文本。落地后 Non-ASCII grep 须确认该行清洁。

## C9 — ASCII only

所有 PLATE_FULL 文本和 EQ_SLOTS EOL=None。无 CJK 字符。✓

## C10 — FUNC_RENAME

无函数改名 (FUNC_RENAME=0)。✓

## C11 — carve / disasm

无 ROM_INCBIN，无 carve / disasm 计划。✓

## C12 — §5.1 登记

无全 ROM 0-引用数据块。✓

## C13 — 残留 100% 覆盖

段内自动名统计:
- PTR_gP1LifePoints_* 槽: 8 个
- DAT_ 槽: 29 个
- 合计: 37 个

EQ_SLOTS = 37 (含 8 PTR_ + 29 DAT_)，RENAME = 0，覆盖 = 37/37 = 100%。✓

---

## 补充说明

1. **SCROLLBAR_CLEAR_BITS_14_6 复用**: C5 按值去重原则，0xffff803f 虽在 build_effect_zone_entry 中语义为 "effect buf[+4] 字段掩码"，但值与 gl_scrollbar.inc 中已有常量相同，正确复用。

2. **gP1HandSlotArray 多语义复用**: gP1HandSlotArray=0x0201c8f8 在本段用于：手牌数组基址、墓地数组基址、额外 Deck 数组基址——均为 gP1LP+0x418 同一物理地址，不同语境下的不同数组。C5 规则下复用同一常量名是正确的，已有 ewram.inc 注释说明。

3. **HAND_ARRAY_TO_COUNT_NEG_OFF 两个槽**: DAT_08036d04 和 DAT_08036eec 均为 0xfffffbfc，proposal 正确对两个槽应用同一 equate。

---

**PASS** — 可进入 Mode B 落地。
