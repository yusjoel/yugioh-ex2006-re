# 卡包卡牌列表数据分析

**写作日期**：2026-04-16
**数据范围**：ROM `0x1E5ABFC ~ 0x1E5E618`（14,876 字节）
**产出**：`data/pack-card-lists.s`（3,829 行）

---

## 一、数据结构

### 卡包信息表 (Pack Info Table)

**地址**：`0x09E5E2E8`（ROM偏移 `0x1E5E2E8`）
**大小**：51 条 × 16 字节 = 816 字节

| 偏移 | 类型 | 字段 | 说明 |
|------|------|------|------|
| +0 | u16 | price | 开包价格 (DP)，范围 150~1500 |
| +2 | u16 | cards_per | 每次开包获得的卡数，3 或 5 |
| +4 | u16 | total | 本包可开出的卡牌总数 |
| +6 | u16 | name_id | 包名 string ID (7001~7063) |
| +8 | u16 | desc_id | 包描述 string ID (7101~7163) |
| +10 | u16 | padding | 恒为 0 |
| +12 | u32 | card_list_ptr | 卡牌列表 ROM 指针 (GBA地址)；pack 45-50 为 0 |

**已知引用**：`FUN_080dbbc0`（`pack_name_text_render`）从 `pack_id * 16 + offset 6` 读取 name_id。

### 卡牌列表 (Pack Card Lists)

**地址**：`0x09E5ABFC ~ 0x09E5E2E8`（紧接在信息表之前）
**大小**：3,515 条 × 4 字节 = 14,060 字节

每条 4 字节：

| 偏移 | 类型 | 字段 | 说明 |
|------|------|------|------|
| +0 | u16 | slot_id | 卡槽编号，与 `card-names.s` 标签 `card_name_XXXX` 一致 |
| +2 | u8 | rarity | 稀有度编码（见下表） |
| +3 | u8 | padding | 恒为 0 |

列表按 full u32 值升序排列（先按 rarity 分组，组内按 slot_id 升序）。

### 稀有度编码

| 值 | 含义 | 说明 |
|----|------|------|
| 0x00 | Common | 最常见 |
| 0x04 | Secret Rare | |
| 0x05 | Secret Rare (alt art) | 仅 Pack 0 的 Blue-Eyes White Dragon |
| 0x08 | Ultra Rare | |
| 0x0C | Super Rare | |
| 0x10 | Rare | |

rarity 0x05 在全 ROM 仅出现 1 次（Pack 0 Blue-Eyes White Dragon，slot_id 0x0FA7）。

---

## 二、数据分布

### 45 个有卡牌列表的 Pack

| Pack | 名称 | 价格 | 每包 | 总数 |
|------|------|------|------|------|
| 0 | LEGEND OF B.E.W.D. | 150 | 5 | 106 |
| 1 | METAL RAIDERS | 150 | 5 | 114 |
| 2 | PHARAOH'S SERVANT | 200 | 5 | 92 |
| 3 | PHARAONIC GUARDIAN | 300 | 5 | 91 |
| 4 | SPELL RULER | 200 | 5 | 88 |
| 5 | LABYRINTH OF NIGHTMARE | 250 | 5 | 96 |
| 6 | LEGACY OF DARKNESS | 250 | 5 | 92 |
| 7 | MAGICIAN'S FORCE | 300 | 5 | 92 |
| 8 | DARK CRISIS | 300 | 5 | 101 |
| 9 | INVASION OF CHAOS | 350 | 5 | 107 |
| 10 | ANCIENT SANCTUARY | 350 | 5 | 103 |
| 11 | SOUL OF THE DUELIST | 400 | 5 | 57 |
| 12 | RISE OF DESTINY | 400 | 5 | 59 |
| 13 | FLAMING ETERNITY | 450 | 5 | 58 |
| 14 | THE LOST MILLENIUM | 450 | 5 | 58 |
| 15 | CYBERNETIC REVOLUTION | 500 | 5 | 59 |
| 16 | ELEMENTAL ENERGY | 500 | 5 | 57 |
| 17 | SHADOW OF INFINITY | 500 | 5 | 58 |
| 18 | GAME GIFT COLLECTION | 1000 | 5 | 82 |
| 19 | Special Gift Collection | 1000 | 5 | 72 |
| 20 | Fairy Collection | 500 | 5 | 68 |
| 21 | Dragon Collection | 500 | 5 | 76 |
| 22 | Warrior Collection A | 400 | 5 | 82 |
| 23 | Warrior Collection B | 600 | 5 | 85 |
| 24 | Fiend Collection A | 400 | 5 | 67 |
| 25 | Fiend Collection B | 600 | 5 | 87 |
| 26 | Machine Collection A | 400 | 5 | 53 |
| 27 | Machine Collection B | 600 | 5 | 68 |
| 28 | Spellcaster Collection A | 400 | 5 | 63 |
| 29 | Spellcaster Collection B | 600 | 5 | 70 |
| 30 | Zombie Collection | 500 | 5 | 66 |
| 31 | Special Monsters A | 800 | 5 | 55 |
| 32 | Special Monsters B | 1000 | 5 | 62 |
| 33 | Reverse Collection | 450 | 3 | 71 |
| 34 | LP Recovery Collection | 300 | 5 | 56 |
| 35 | Special Summon Collection A | 600 | 3 | 86 |
| 36 | Special Summon Collection B | 800 | 3 | 85 |
| 37 | Special Summon Collection C | 1000 | 3 | 93 |
| 38 | Equipment Collection | 400 | 3 | 74 |
| 39 | Continuous Spell/Trap A | 300 | 3 | 74 |
| 40 | Continuous Spell/Trap B | 500 | 3 | 80 |
| 41 | Quick/Counter Collection | 800 | 5 | 66 |
| 42 | Direct Damage Collection | 600 | 5 | 107 |
| 43 | Direct Attack Collection | 500 | 5 | 49 |
| 44 | Monster Destroy Collection | 800 | 5 | 130 |

### 6 个特殊 Pack（无卡牌列表）

| Pack | 名称 | 价格 | 每包 | total 字段 |
|------|------|------|------|------------|
| 45 | All Normal Monsters | 300 | 5 | 521 |
| 46 | All Effect Monsters | 800 | 3 | 783 |
| 47 | All Fusion Monsters | 800 | 3 | 90 |
| 48 | All Traps | 1200 | 3 | 297 |
| 49 | All Spells | 1200 | 3 | 406 |
| 50 | All at Random | 1500 | 5 | 2071 |

这些 pack 的 card_list_ptr 为 0，total 字段存储的是该类别的卡牌总数。
游戏运行时应通过卡牌属性表动态筛选而非查表。

---

## 三、ROM 布局

```
0x1E5ABFC  ┌─ pack_00_card_list (106 × 4B = 424B)
           ├─ pack_01_card_list (114 × 4B = 456B)
           ├─ ...（45 个 pack 紧密排列，无间隙）
0x1E5E2E8  ├─ pack_info_table (51 × 16B = 816B)
0x1E5E618  └─ 结束
```

总数据区 14,876 字节，落在 rom.s 原 incbin `0x1E5906E, 0x5EC2` 内。
拆分为三段：`0x1B8E` + `0x3A1C`（.include） + `0x918` = `0x5EC2`。

---

## 四、定位过程

### 切入点

`doc/temp/pack-card-list-investigation-prompt.md` 中记录的线索：

1. **ROM 0x09E5E2E8** — 16 字节 pack 记录表，已知 offset+6 = string ID
2. **FUN_080dc098** — pack 卡牌信息加载函数（本次未深入分析，已由数据层面解决）

### 步骤

1. Dump `0x09E5E2E8` 前 10 条记录，识别 u16/u32 字段：
   - offset 0 = price（与游戏 UI 价格一致）
   - offset 2 = 5（每包获得的卡数）
   - offset 4 = 卡牌总数
   - offset 12 = ROM 指针（`0x09E5xxxx` 范围）

2. 跟踪 Pack 0 指针 `0x09E5ABFC`，dump u32 数组：
   - 前 78 条值在 `0x0FA7~0x12ED`（与 card-names.s slot_id 匹配）
   - 后 28 条高位非零 → 发现 u8 rarity 字段

3. 交叉验证：用 card-names.s 反查每个 slot_id 的卡名，与 Yugipedia Pack 01 "Legend of B.E.W.D." 的卡牌列表逐张比对：
   - Secret: Raigeki (0x10F7) + Blue-Eyes White Dragon (0x0FA7) ✓
   - Ultra: Blue-Eyes (0x0FA7) + Dark Magician (0x0FC9) + Dark Hole (0x10F6) + Monster Reborn (0x12EA) ✓
   - Super: 5 Exodia 部件 + Red-Eyes B. Dragon + Swords of Revealing Light ✓
   - Rare: 15 张 ✓
   - Common: 78 张 ✓

4. 验证全部 45 个 pack 的卡牌列表连续且无间隙，最后一个列表结束地址恰好是信息表起始地址。

### 注意事项

- slot_id 与 SO code 是不同的编号体系：
  - slot_id 用于 card-names.s / card-stats.s 标签
  - SO code 用于 deck_entry / banlist_entry / deck_card 宏
  - 例：Blue-Eyes White Dragon 的 slot_id = 0x0FA7，SO code = 4088 (0x0FF8)
- 卡牌列表使用的是 **slot_id**，不是 SO code

---

## 五、相关文件

| 文件 | 内容 |
|------|------|
| `data/pack-card-lists.s` | 结构化汇编（入库） |
| `tools/rom-export/export_pack_card_lists.py` | 导出脚本 |
| `tools/ghidra-labeling/LabelPackCardLists.py` | 46 个 Ghidra 数据标签 |
| `include/macros.inc` | `pack_card_entry` 宏定义 |
| `doc/temp/pack-card-list-investigation-prompt.md` | 调查起始线索 |
