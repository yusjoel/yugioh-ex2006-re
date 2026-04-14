# 卡牌大卡图批量导出（P1-5）

**脚本**：`tools/rom-export/export_card_images.py`
**状态**：2026-04-15 最终确定，按 card_id **0..2097** 全量导出 2331 张 PNG，
独立 tile_block 完整覆盖 0..2330（无重复、无遗漏）。card_id 1..2097 是 yugipedia
的正本卡（含 2081..2097 共 17 张 Token），card_id=0 是象形文字纹理风格的
占位/未知卡图（用途暂未确认）。

## 快速使用

```bash
python tools/rom-export/export_card_images.py             # 默认 1..2097 全量
python tools/rom-export/export_card_images.py --gray      # 灰度
python tools/rom-export/export_card_images.py --only 672  # 单张调试
python tools/rom-export/export_card_images.py --start 2081 --end 2097  # 仅 token
```

### 命名规则

对每个 card_id 同时查 OCG (flag=0) 与 TCG (flag=1) 索引：

| 情况 | 输出文件 |
|------|---------|
| 两版 tile_block 相同 | `card_{cid:04d}.png` |
| 两版 tile_block 不同 | `card_{cid:04d}_ocg.png` + `card_{cid:04d}_tcg.png` |
| 仅一版有 tile_block | `card_{cid:04d}_ocg.png` 或 `card_{cid:04d}_tcg.png` |
| 两版都 0xFFFF | 跳过 |

输出目录 `graphics/card-images/`（已 .gitignore），清单 `manifest.csv` 字段：
`card_id,file_ocg,file_tcg,file_shared,slot_id_hex,tb_ocg,tb_tcg`。

## 数据结构要点（详见 p1-phase-b2-findings.md）

| 项 | 地址 / 值 |
|----|----------|
| 6bpp tile 数据基址 | ROM `0x00510640` |
| 每卡 stride | 4800 字节（10×10 tiles × 8×8） |
| 索引表 | ROM `0x015B5C00`，u16 LE |
| 索引表访问 | `byte_off = (card_id × 2 + flag) × 2` |
| 索引表有效范围 | card_id 0–3422 |
| **每卡独立调色板** | ROM `0x004C76C0 + tile_block × 128`，64 色 BGR555 |
| 调色板应用 | 离线：raw_6bit 直接索引；游戏内：VRAM palette[0x10..0x4F] |

## card_id 0..2097 导出统计（最终口径）

| 项 | 数量 |
|----|------|
| 两版相同（无后缀 PNG） | 1865 |
| 两版不同（_ocg + _tcg 双文件） | 233 |
| 仅单版存在 | 0 |
| 两版都 FFFF | 0 |
| 写入 PNG 总数 | **2331** |
| 覆盖独立 tile_block | **2331**（0..2330 完整连续，0 漏项） |

- card_id 1..2080：正式卡（slot 0x0FA7..0x19FE 升序）
- card_id 2081..2097：17 张 Token
- card_id 0：slot=0x0000 占位记录，对应 tb=0 象形文字纹理图（用途未知，可能是卡典未解锁默认图/UI 占位）

### card-stats.s 的两表并行结构（已证伪的"card_id 直接映射 slot"假说）

`data/card-stats.s` 总 5170 条，结构实际为：

- **表 A**：idx 1..2080，slot 升序 `0x0FA7..0x19FE`，共 2080 主卡 + 副本
- **表 B**：idx 2081..5169，再从 `0x13FB` 起重新升序——疑似另一批用途（仍需确认）

每 slot 在两表各有 1 条 copy=0，所以"每 slot 2 条主记录"。此前按 stats idx 做 card_id
导致 B 表 idx 3418（slot 0x14CF = The A. Forces）被错误关联到另一张图；换用
**card_id 1..2097 上限**后问题消失，因为 2097 恰好落在表 A 内部。

### 早期（前一版）的多余扫描

先前脚本扫描到 card_id 3422（表 B 尾端）共 3134 条有效条目，误将表 B 记录也当卡图
导出。当前规则明确后，应以 card_id 1..2097 为权威范围。

## 调色板调查过程

初读 findings §3.1 将 `0x084C76C0` 理解为"256 色 BG 共享调色板"——试用 512 字节共享后
DESPAIR 呈现错误的蓝灰色调。分析该地址前 512 字节，发现约半数 BGR555 项带 bit15=1，不符合 GBA
惯例，证明**这不是一个 256 色单一调色板**。改按 `base + tile_block × 128` 当 64 色/卡读取，
DESPAIR 立即呈现正确的暗红紫配色；多张抽样（card_0010=红龙、card_0500=蓝色昆虫、
card_3098=蓝龙等）颜色均合理。因此确认每卡独立 128 字节调色板区，紧贴在 tile 数据基址
`0x00510640` 之前占用 `0x4C76C0..0x510440`（~297 KB）。

## card_id ↔ slot_id 映射（已解决 2026-04-15）

**`card_id` 就是 `data/card-stats.s` 中的 0-indexed 记录序号**。ROM 偏移：
`0x018169B6 + card_id × 22`，读 +2 处 u16 即 slot_id。

实测对应关系：

| card_id | ROM record 偏移 | slot_id | 卡名 |
|---------|----------------|---------|------|
| 0 | 0x018169B6 | 0x0000 | (占位) |
| 1 | 0x018169CC | 0x0FA7 | Blue-Eyes White Dragon |
| 672 | 0x0181A606 | 0x12EA | Monster Reborn |
| 1323 | 0x0181C4E8 | 0x1653 | Despair from the Dark |

**多条 copy=0 主记录**：同一 slot_id 在 card-stats.s 中可能出现多次（如 Monster Reborn 在 card_id=672 与 2933 都是 copy=0），
推测为游戏不同场景使用的独立记录（预组 / 卡典 / 限制表等）。图像表通常只给**第一条**记录登记图像，
后续同 slot 的 copy=0 条目在图像索引表中为 `0xFFFF`。

因此脚本以 card_id 为主键导出，命名 `card_{card_id:04d}_tb{tile_block:04d}.png` 已足够；
如需 `{slot_id:04X}_{english_name}.png` 形式，可从 card-stats 反查 slot_id 再从 card-names.s 取卡名。

## 未解决 / 待改进

- **flag=0（日版）独立导出**：脚本支持 `--flag 0` 但未做视觉验证。日版卡图数据 tile_block
  范围实测 0–2330，与美版共享同一 tile 数据池，所以 flag 仅影响索引查找，不涉及数据路径。

- **索引表末尾 424 条 FFFF**：长度留有余量，未见被任何 card_id 访问。

## 与单卡验证脚本的关系

`tools/ad-hoc/decode_card_6bpp.py` 是 Phase B2 单卡验证脚本，产出 PGM 格式、仅 DESPAIR。
保留作为历史参考。生产使用请用 `tools/rom-export/export_card_images.py`。
