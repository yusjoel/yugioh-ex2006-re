# T-THEME 研究笔记

**状态**：原 Sheet 仅列 1 对手（Exarion Universe），数据极不完整；实装待新来源
**来源**：`doc/um06-romhacking-resource/opponents-coinflip-screen.md` Sheet 1 第 80+ 行
**日期**：2026-04-15

---

## 原 Sheet 实际提供的数据

| 对手 | 位置 | Image ROM | Tilemap ROM | Palette ROM |
|------|------|-----------|-------------|-------------|
| Exarion Universe | Top | `0x01A1DFAC` | `0x01A85FAC` | `0x01A1A52C` |
| Exarion Universe | Bottom | `0x01A98DEC` | `0x01B00DEC` | `0x01A1A5AC` |

> 其他 26 个对手的 Theme Duel 大图**原表未填**。

## 观察到的结构规律

- Top image → Tilemap 偏移：`0x01A85FAC - 0x01A1DFAC = 0x68000` — 与 opponents T2 一致
- Bottom image → Tilemap 偏移：`0x01B00DEC - 0x01A98DEC = 0x68000` — 同上
- Top palette → Bottom palette：`0x01A1A5AC - 0x01A1A52C = 0x80`（128 B，标准 4bpp 16 色 × 8 行，或 16 subpal × 2×4？）
- Top image → Bottom image：`0x01A98DEC - 0x01A1DFAC = 0x7AE40`（可能跨段，含 Bottom image 之前的其他数据）

## 与 opponents T2 管线对比

已落地的 opponents 管线（`graphics/opponents/*.bin`）数据：

| 项 | 值 |
|---|---|
| image 区基址 | `0x01B1200C`（Top）/ `0x01B51CFC`（Bottom） |
| image stride | 8192 B（= 0x2000）每对手 |
| tilemap stride | 1200 B 每对手 |
| palette 块 | `0x01B101AC`（每对手 128 B） |

Theme Duel 的 Exarion Universe 地址不在这批 opponents 图形区内，且 stride
可能不同。需要**新出的 Sheet 或逆向**来补全其他 26 对手地址 + 实际尺寸。

## 下一步

1. 若有新版本 Sheet：一次性补全 27 对手 × Top/Bottom 的 image/tilemap/palette
2. 静态逆向：在 `asm/all.s` 搜 `.word 0x01A1DFAC` / `.word 0x01A1A52C` 等字面量，
   找加载函数 → 发现是否存在 27 项数组式 pointer table（如 opponents 那样）
3. mGBA 运行时：进一个 Theme Duel，dump BG VRAM/palette 对照 ROM

## 与 T-COINFLIP 的关联

Theme Duel 大图和 Coinflip 大图共享同一 Sheet，推测它们属于同一 UI 模块。
找到 coinflip 初始化函数可能顺带撞见 theme duel 的 pointer table。

## 参考

- `doc/dev/t-coinflip-research.md`
- `tools/rom-export/export_gfx.py`：opponents/HUD 管线模板
- `asm/rom.s` L126–260：opponents incbin 拆分示例
