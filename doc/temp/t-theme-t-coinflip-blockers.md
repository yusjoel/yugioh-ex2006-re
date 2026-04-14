# T-THEME / T-COINFLIP 卡点记录（2026-04-15）

## T-THEME（27 对手 Theme Duel 大图）

### 卡点

`doc/um06-romhacking-resource/opponents-coinflip-screen.md` Theme Duel 段
（L91 之后）仅包含 **Exarion Universe Top/Bottom 两行** 数据：

| 字段 | Top | Bottom |
|------|------|--------|
| Image | `0x01A1DFAC` | `0x01A98DEC` |
| Tilemap | `0x01A85FAC` | `0x01B00DEC` |
| Palette | `0x1A1A52C` | `0x1A1A5AC` |

后续 26 个对手的地址在原始 Google Sheets（Sheet 1）中，但 md 转换**未保留**。
无法推定区段结构：

- Top image ↔ Top tilemap 差 `0x68000`，不是 `27 × 0x2000` 或 `27 × 0x4B0`
- Palette Top/Bottom 差仅 `0x80`（对手调色板 stride 为 `0x120`）

### 推进需求

任一即可解开：

1. 重新导出 Sheet 1 完整 Theme Duel 段（需 Google Sheets 访问）
2. 从 ROM 结构中反向扫描：以 Exarion Top tilemap (0x01A85FAC) 处 `0x4B0` 字节
   为参考模板，在后续区间找 27 段同构 tilemap 定位块边界
3. Ghidra 中追 Theme Duel 加载函数（`0x0802D200` 附近曾被 md 提及 L61）的
   字面量池

### 现状

保持 `asm/rom.s` 现有对 Theme Duel 区段的大段 `.incbin "roms/2343.gba", ...` 引用。

---

## T-COINFLIP（抛硬币界面 4 类资源）

### 卡点

同源 md 第 9 行 header 行有以下条目但**字段对齐混乱**：

| 资源 | Image in Tile Mole | Tilemap | Palette | 备注 |
|------|---------------------|---------|---------|------|
| Coinflip Top Bar | `0x0194F83C` | ? | `0x01A1A62C` | 单行 |
| Coin & Box | `0x0194D71C` | `0x0195383C` | `0x0194D6FC` | "Limited to 14 Tiles" |
| Flipping Animation | `0x018977F8` | - | - | 多帧？格式未知 |
| "Coin Toss Selection" Text | ? | - | - | 无图像地址 |

具体 **每项字节长度**、**Flipping Animation 帧数/格式**、**Tilemap 尺寸**
均无法从 md 推定。Text 条目可能仅是字符串而非图形。

### 推进需求

- 需要 Google Sheets 完整 Sheet 1 原始数据确认字段对齐
- 或 mGBA 动态追踪：硬币翻转界面的 VRAM 写入时机 + DMA 源地址

### 现状

`asm/rom.s` 现有 `0x1896730 + 0x279A7C` 大段 `.incbin` 保持不变（覆盖
`0x18977F8` / `0x194D71C` / `0x194F83C`），未拆分。

---

## 建议

- 优先让用户补全 Google Sheets Sheet 1 的 md 再回头做
- 或并入 P2（卡牌列表小图）调查时一起走 mGBA 动态路线
