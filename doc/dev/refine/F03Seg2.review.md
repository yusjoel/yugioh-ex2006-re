# Review: F03Seg2  [0x08036a78..0x08037128)

**Iteration**: 1  
**Verdict**: PASS

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
