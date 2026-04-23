# 卡牌属性数据表

全部卡牌的属性数据（ATK / DEF / 星级 / 种族 / 属性 / 副类别等）的 ROM 布局。

---

## 位置与规模

| 项目 | 值 |
|------|-----|
| ROM 偏移起始 | `0x018169B6` |
| ROM 偏移结束 | `0x01832602` |
| 记录大小 | 22 字节（11 × uint16 LE） |
| 总记录数 | 5170 条 |
| 唯一槽位数 | 2054 个（copy=0 的主记录） |
| 槽位 ID 范围 | `0x0000 – 0x19FE` |

**索引公式**：`record_addr = 0x018169B6 + card_id × 22`

`card_id` 是 0-indexed 记录序号。同一 `slot_id` 可能出现多次（多条 `copy=0` 主记录用于不同场景：预组、卡典、限制表等）。从 card_id 取 slot_id：`rom[0x018169B6 + card_id × 22 + 2]` (u16 LE)。

---

## 字段布局

每条记录 22 字节，以 uint16 小端格式排列：

| 字节偏移 | 字段名 | 说明 |
|---------|--------|------|
| +00 | `zero0`   | 恒为 `0x0000`（首条哑元记录除外） |
| +02 | `slot_id` | 卡槽编号（与 `data.md` 中 Slot 列一致） |
| +04 | `copy`    | 異画索引（0=主图，1/2/3=异画） |
| +06 | `flags`   | 标志（通常 1；0=哑元；3=含义待定） |
| +08 | `atk`     | 攻击力；魔法/陷阱卡为 `0x0000` |
| +0A | `def`     | 守备力；魔法/陷阱卡为 `0x0000` |
| +0C | `level`   | 星数（怪兽卡；非怪兽为 0） |
| +0E | `race`    | 种族代码（`RACE_*`） |
| +10 | `attr`    | 属性代码（`ATTR_*`） |
| +12 | `subtype` | 卡种类（`SUBTYPE_NORMAL/EFFECT/FUSION/...`） |
| +14 | `spsub`   | 魔法/陷阱细分（`SPSUB_NORMAL/EQUIP/FIELD/...`；怪兽恒 0） |

枚举宏定义见 `include/macros.inc`。

---

## 属性编码

| 值 | 宏 | 属性 | 代表卡 |
|----|----|------|--------|
| 1 | `ATTR_LIGHT` | LIGHT（光） | Blue-Eyes White Dragon |
| 2 | `ATTR_DARK` | DARK（闇） | Ryu-Kishin / Kuriboh |
| 3 | `ATTR_WATER` | WATER（水） | Great White / Fiend Kraken |
| 4 | `ATTR_FIRE` | FIRE（炎） | Flame Swordsman |
| 5 | `ATTR_EARTH` | EARTH（地） | Hitotsu-Me Giant |
| 6 | `ATTR_WIND` | WIND（风） | Baby Dragon |
| 7 | `ATTR_DIVINE` | DIVINE（神） | **BY6E 中未使用** |
| 8 | `ATTR_SPELL` | SPELL（魔法卡） | Axe of Despair |
| 9 | `ATTR_TRAP` | TRAP（陷阱卡） | Dragon Capture Jar |

怪兽卡不会取 8/9；`attr=8/9` 仅用于魔法/陷阱卡，与 `race=22/23` 成对出现。

---

## 种族编码

| 值 | 宏 | 种族 | 代表卡 |
|----|----|------|--------|
| 1  | `RACE_DRAGON`        | Dragon（龙） | Blue-Eyes White Dragon |
| 2  | `RACE_ZOMBIE`        | Zombie（不死） | Skull Servant |
| 3  | `RACE_FIEND`         | Fiend（恶魔） | Kuriboh / Summoned Skull |
| 4  | `RACE_PYRO`          | Pyro（炎） | Charubin the Fire Knight |
| 5  | `RACE_SEA_SERPENT`   | Sea Serpent（海龙） | Takriminos |
| 6  | `RACE_ROCK`          | Rock（岩石） | Giant Soldier of Stone |
| 7  | `RACE_MACHINE`       | Machine（机械） | Cyber Soldier of Darkworld |
| 8  | `RACE_FISH`          | Fish（鱼） | Great White |
| 9  | `RACE_DINOSAUR`      | Dinosaur（恐龙） | Two-Headed King Rex |
| 10 | `RACE_INSECT`        | Insect（昆虫） | Basic Insect |
| 11 | `RACE_BEAST`         | Beast（兽） | Griffore |
| 12 | `RACE_BEAST_WARRIOR` | Beast-Warrior（兽战士） | Battle Ox |
| 13 | `RACE_PLANT`         | Plant（植物） | Mushroom Man |
| 14 | `RACE_AQUA`          | Aqua（水） | Jellyfish |
| 15 | `RACE_WARRIOR`       | Warrior（战士） | Flame Swordsman |
| 16 | `RACE_WINGED_BEAST`  | Winged Beast（鸟兽） | Harpie Lady |
| 17 | `RACE_FAIRY`         | Fairy（天使） | Gyakutenno Megami |
| 18 | `RACE_SPELLCASTER`   | Spellcaster（魔法使） | Mystical Elf |
| 19 | `RACE_THUNDER`       | Thunder（雷） | LaLa Li-oon |
| 20 | `RACE_REPTILE`       | Reptile（爬虫） | Armored Lizard |
| 21 | `RACE_DIVINE_BEAST`  | Divine-Beast（幻神兽） | **BY6E 中未使用** |
| 22 | `RACE_SPELL`         | Spell（魔法卡） | Axe of Despair（与 `attr=8` 成对） |
| 23 | `RACE_TRAP`          | Trap（陷阱卡） | Dragon Capture Jar（与 `attr=9` 成对） |

魔法/陷阱卡的 `race` 与 `attr` 是冗余配对：魔法恒 `(attr=8, race=22)`，陷阱恒 `(attr=9, race=23)`。

---

## 表结构（两表并列）

`data/card-stats.s` 总 5170 条实际为两段：

- **表 A**：idx 1–2080，slot 升序 `0x0FA7–0x19FE`，主卡 + 副本
- **表 B**：idx 2081–5169，从 `0x13FB` 起重新升序，另一批用途

每 `slot_id` 在两表各有 1 条 `copy=0` 主记录，因此"每 slot 2 条主记录"。

---

## 已验证示例（Blue-Eyes White Dragon）

```
ROM 偏移: 0x018169D4 (card_id=1)
Raw hex : 0000 A70F 0000 0100 B80B C409 0800 0100 0100 0000 0000

slot_id       = 0x0FA7 (= 4007)
copy          = 0x0000 (主记录)
flags         = 0x0001
atk           = 0x0BB8 (= 3000)
def           = 0x09C4 (= 2500)
level         = 0x0008 (= 8 星)
race          = 0x0001 (DRAGON)
attr          = 0x0001 (LIGHT)
subtype       = 0x0000 (NORMAL)
spsub         = 0x0000
```

---

## 相关文件

| 文件 | 内容 |
|------|------|
| `data/card-stats.s` | 结构化汇编（5170 条 `card_stat` 宏） |
| `include/macros.inc` | `card_stat_*` / `ATTR_*` / `RACE_*` / `SUBTYPE_*` / `SPSUB_*` 宏 |
| `tools/rom-export/export_card_data.py` | 从 ROM 重建 `card-stats.s` |
| `tools/ad-hoc/verify_card_enums.py` | 枚举值完整性验证 |
