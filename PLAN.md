# 游戏王 EX2006 ROM 数据汇编化计划

## 目标

将 ROM 中已知数据区从 `.incbin` 替换为带结构注释的可读汇编代码，
最终输出与原始 ROM **byte-identical**。

## 数据区总览

| 区块 | ROM 偏移范围 | 大小 | 状态 |
|------|------------|------|------|
| 对手卡值块（27条目×32字节）| `0x1E58D0E – 0x1E5906D` | 864 B | ⬜ 待做 |
| 禁卡表（8个版本共487条目）  | `0x1E5EF30 – 0x1E5F6CB` | 1948 B | ⬜ 待做 |
| 初始卡组（50张+终止符）    | `0x1E5F884 – 0x1E5F8E9` | 102 B | ⬜ 待做 |
| 结构卡组（6套+指针表）     | `0x1E5FA58 – 0x1E5FD83` | 812 B | ✅ 已完成，待重构格式 |
| 对手卡组（25套）           | `0x1E6468E – ~0x1E65A45` | ~5300 B | ⬜ 待做 |

## 数据编码格式

**结构卡组**：每条 4 字节 = `(so_code * 4 | qty)` LE16 + `0x0000` LE16

**禁卡表**：每条 4 字节 = `so_code` LE16 + `limit` LE16（limit: 0禁止/1限制/2准限制）

**初始/对手卡组**：每条 2 字节 = `so_code` LE16，以 `0x0000` 终止

**对手卡值块**：每条 32 字节 = `card_value`(2) + `unk`(2) + 文件路径字符串(20字节null-padded) + padding(8)

## 宏定义（include/macros.inc）

```asm
deck_entry so_code, qty    @ 结构卡组：(so_code * 4) | qty, 0
banlist_entry so_code, limit  @ 禁卡表：so_code, limit
deck_card so_code          @ 对手/初始卡组：so_code
```

**示例**（真红眼黑龙 SO=4088=0x0FF8）：
```asm
@ 旧格式：.hword 0x3FE1, 0x0000
@ 新格式：deck_entry 4088, 1    @ Red-Eyes B. Dragon (74677422)
```

## 实施步骤

- [x] Phase 0：建立宏系统（`include/macros.inc`）
- [x] Phase 1：重构结构卡组（`data/struct-decks.s`）使用 `deck_entry` + 十进制 so_code
- [x] Phase 2：禁卡表（`data/banlists.s`）8个版本，使用 `banlist_entry`
- [x] Phase 3：初始卡组（`data/starter-deck.s`）50张，使用 `deck_card`
- [x] Phase 4：对手卡值块（`data/opponent-card-values.s`）27条目×32字节
- [x] Phase 5：对手卡组（`data/opponent-decks.s`）25套

## rom.s 最终布局（按 ROM 偏移排序）

```
incbin [0x1000000, 0x1E58D0D]
data/opponent-card-values.s   @ 0x1E58D0E (+864 B)
incbin [0x1E5906E, 0x1E5EF2F]
data/banlists.s               @ 0x1E5EF30 (+1948 B)
incbin [0x1E5F6CC, 0x1E5F883]
data/starter-deck.s           @ 0x1E5F884 (+102 B)
incbin [0x1E5F8EA, 0x1E5FA57]
data/struct-decks.s           @ 0x1E5FA58 (+812 B)  ← 已完成
incbin [0x1E5FD84, 0x1E6468D]
data/opponent-decks.s         @ 0x1E6468E (~+5300 B)
incbin [end, 0x1FFFF00]
```

## 注意事项

- 每个 Phase 完成后必须 `build.bat` 验证 **byte-identical**
- `so_code` 统一用**十进制**整数写入 ASM 源码（如 `4088` 代替 `0x0FF8`）
- 卡牌数据来源：`doc/um06-deck-modification-tool/data.md`
- 对手卡值块中 `unk` 字段（0x1F40 起递增）原因未知，保留为 `.hword` 硬编码
