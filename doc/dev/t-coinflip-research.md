# T-COINFLIP 研究笔记

**状态**：资产 ROM 地址已提取，**大小待定**，incbin 拆分待实装
**来源**：`doc/um06-romhacking-resource/opponents-coinflip-screen.md` Sheet 1
**日期**：2026-04-15

---

## 资产地址表

Coinflip 界面共 4 类资产，其中 3 类为图像，1 类为字符串。

| # | 资产 | Image ROM | Tilemap ROM | Palette ROM | 备注 |
|---|------|-----------|-------------|-------------|------|
| 1 | Coinflip Top Bar | `0x018977F8` | — | `0x01A1A62C` | ≤ 14 tiles (0x0D) |
| 2 | Coinflip Coin & Box | `0x0194D71C` | — | `0x0194D6FC` | palette 在 image 前 32 B |
| 3 | Coinflip Flipping Animation | `0x0194F83C` | `0x0195383C` | 未列（可能复用 #2） | 动画帧序列 |
| 4 | "Coin Toss Selection" Text | — | — | — | 字符串 @ `0x01DC53D6`, `0x01DC882A`（已覆盖于 `data/game-strings-*.s`）|

## 关键未知：尺寸

原表只给起始地址，**没给任何 asset 的字节长度**。要做 byte-identical incbin 拆分需要先解决：

### 方案 A：边界推断

- #2 Coin & Box image `0x0194D71C` 到 #3 Flipping Anim image `0x0194F83C` 相距 `0x2120 = 8480` 字节
- #3 Flipping Anim image `0x0194F83C` 到其 tilemap `0x0195383C` 相距 `0x4000 = 16384` 字节
- #3 tilemap `0x0195383C` 到某个下一个已知资产？

可以把相邻已知起点之差作为尺寸上界。但必须验证尾部是否留有 padding/其他数据。

### 方案 B：逆向 load 函数

找 Coinflip 屏幕初始化函数，看它 LZ77/memcpy 参数里的 `len`。这是 opponents
图形管线（T2）已经成功跑通的方式：`tools/rom-export/export_gfx.py` 里硬编码
了尺寸，很可能也是从逆向得来。

### 方案 C：mGBA 运行时 dump VRAM

进游戏 coinflip 界面，dump VRAM + palette 对照 ROM 定位。

---

## 下一步（下一轮 session）

1. **定位 coinflip 屏幕初始化函数**：在 `asm/all.s` 里搜 `.word 0x018977F8` /
   `.word 0x0194D71C` / `.word 0x0194F83C` 字面量，看调用该字面量的 bl 上下文
   （LZ77 unpack / DMA / memcpy 调用会露出长度参数）
2. 记 3 张图的实际字节数，写进 `tools/rom-export/export_gfx.py`，仿 opponents 管线导出 `.bin`
3. 在 `asm/rom.s` 加 `.incbin` 引用；build verify byte-identical

## 相关地址（ROM 布局上下文）

- `0x018977F8` 在对手小图标区后（`0x0188DA70..0x018977F?`），可能是 coinflip 特有的 top bar UI
- `0x0194D71C` / `0x0194F83C` / `0x0195383C` 簇在同一 MB 内，应为同一 coinflip 资源块
- `0x01A1A62C` (Top Bar palette) 远离 image，独立存放

## 参考

- `tools/rom-export/export_gfx.py`：opponents/HUD 管线模板
- `asm/rom.s` L126–260：opponents incbin 拆分示例
- `doc/um06-romhacking-resource/opponents-coinflip-screen.md`：原始 Sheet（表头被 Google Sheets 压扁，col 标签里可恢复原 3 地址+1 tilemap+2 palette）
