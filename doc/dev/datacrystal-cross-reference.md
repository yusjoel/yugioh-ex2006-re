# Data Crystal ROM/RAM map 交叉验证 + 数据区拆分

**写作日期**：2026-04-17
**前置依赖**：`refs/datacrystal-um2006/` (4 个 wiki 子页面抓取，2026-04-17)
**遵循流程**：`doc/dev/workflow-rom-asset-to-structured-asm.md`（仅 Phase 2-4 适用，无新 ROM 资产 Phase 1 定位）

---

## 一、动因

`refs/datacrystal-um2006/rom-map.md` 收录的 7 段反汇编（来自 TCRF Data Crystal wiki）揭示了三个数据区的精确语义，与项目当前结构有出入。本次任务把 wiki 结论转化为项目结构改动并 byte-identical 验证。

## 二、wiki 揭示的关键事实（已 ROM 字节验证）

### 2.1 `cards_ids_array` @ ROM 0x15B7CCC

依据 `0x080EE76C` 反汇编：

```
r1 = pointer_to_cards_ids_array + ((internal_card_id - 4007) << 1)
r1 = ldrh [r1]              ; r1 = card_id（0xFFFF 表示无对应）
```

- 范围：`internal_card_id` ∈ [0x0FA7, 0x1BA6] → 3072 条
- 每条 u16，总 6144 B = 0x1800
- 终止地址：0x15B7CCC + 0x1800 = **0x15B94CC**

ROM 字节验证（前 32 条）：

| internal_card_id | 偏移 | u16 值 | card_id |
|---|---|---|---|
| 0x0FA7 (4007) | 0x15B7CCC | 0x0001 | 1 (Blue-Eyes White Dragon) |
| 0x0FA8 (4008) | 0x15B7CCE | 0x0005 | 5 (Mystical Elf) |
| 0x0FAF (4015) | 0x15B7CDC | 0xFFFF | (无) |
| ... |

### 2.2 `card_name_pointer_table` @ ROM 0x15F3A5C

依据 `0x080EE968`：

```
r0 = ldr [card_name_pointer_table + ((card_id * 6 + language_id) << 2)]
name_addr = 0x15BB594 + r0
```

- 12,612 × u32 = 50,448 B = 0xC510
- = 2,102 张卡 × 6 语言（EN/DE/FR/IT/ES/XX）

ROM 字节验证（前 12 条）：

| 索引 | card_id | lang | u32 | abs name_addr |
|---|---|---|---|---|
| 0 | 0 | 0 (EN) | 0x00000000 | 0x15BB594 |
| 1 | 0 | 1 (DE) | 0x00000002 | 0x15BB596 |
| ... | ... | ... | ... | ... |
| 6 | 1 | 0 (EN) | 0x0000000C | 0x15BB5A0 |
| 7 | 1 | 1 (DE) | 0x00000018 | 0x15BB5AC ← 项目 card-names.s 起始 |

### 2.3 `card_names_pool` @ ROM 0x15BB594

cid=0 占据 24 字节占位槽（6 langs × 4 字节空字符串），cid=1 起始才到 0x15BB5AC。
项目当前 `data/card-names.s` 从 0x15BB5AC 开始，**漏了前 0x18 字节**——但这部分由
`asm/rom.s` 中的 `.incbin .. 0x15B94CC, 0x20E0` 兜底覆盖，byte-identical 不受影响。
**本次未修复**（涉及 `export_card_data.py` 重写）。

## 三、项目原有冲突

| 数据区 | 项目原状 | wiki 实际 |
|---|---|---|
| `data/card-image-index.s` | 0x15B5C00..0x15B94CB（7270 × u16，"2098+ 为未使用/表 B 数据"）| 真实索引仅到 card_id 2098；2099+ 实际是 `cards_ids_array` |
| `data/card-effect-text.s` | 0x15F3A5C..0x17FFFFF，含 "u32 数据表 12612 条 (用途待确认)" | 头部 50,448 B 是 `card_name_pointer_table`，非 effect text |

## 四、本次改动

### 4.1 新增数据文件

| 文件 | ROM 范围 | 大小 | 来源脚本 |
|---|---|---|---|
| `data/cards-ids-array.s` | 0x15B7CCC..0x15B94CB | 6,144 B | `export_card_images.py` 新增 `write_cards_ids_array_source()` |
| `data/card-name-pointer-table.s` | 0x15F3A5C..0x15FFF6B | 50,448 B | 新建 `export_card_name_pointer_table.py` |

### 4.2 现有文件调整

- `data/card-image-index.s` 截断到 0x15B5C00..0x15B7CCB（card_id 0..2098）。删除原 "card_id 2099+" 段（迁至 `cards-ids-array.s`）和 0xFFFF 填充段。
- `data/card-effect-text.s` 起始改为 0x15FFF6C，去掉头部 u32 表段。

### 4.3 `asm/rom.s` 拆分

```asm
@ 改前：
  .include "data/card-image-index.s"             @ 0x15B5C00..0x15B94CB
  .incbin  "roms/2343.gba", 0x15B94CC, 0x20E0    @ gap
  .include "data/card-names.s"
  .include "data/card-effect-text.s"             @ 0x15F3A5C..0x17FFFFF

@ 改后：
  .include "data/card-image-index.s"             @ 0x15B5C00..0x15B7CCB (truncated)
  .include "data/cards-ids-array.s"              @ 0x15B7CCC..0x15B94CB (NEW)
  .incbin  "roms/2343.gba", 0x15B94CC, 0x20E0
  .include "data/card-names.s"
  .include "data/card-name-pointer-table.s"      @ 0x15F3A5C..0x15FFF6B (NEW)
  .include "data/card-effect-text.s"             @ 0x15FFF6C..0x17FFFFF (shrunk)
```

### 4.4 新增常量符号

`constants/ewram.inc`、`constants/iwram.inc`：依据 `refs/datacrystal-um2006/ram-map.md`
共 22 条 `.equ`（gSettings, gMoneyDp, gPlayerName, gP1LifePoints, gPrng, gFrameCounter…）。
通过 `asm/rom.s` 顶部 `.include` 加载，未做 sed 全量替换 `.word 0x02029810` → 符号——
留给后续重导出 `all.s` 时自然吸收。

### 4.5 Ghidra 标签 + 函数名

- 新建 `tools/ghidra-labeling/LabelDataCrystalRomMap.py`：21 条标签
  - 6 个 ROM 数据标签（`cards_ids_array`、`card_name_pointer_table`、`card_effect_text_pool`、`card_names_pool`、`deck_id_and_data_array`、已存在的 `card_image_index`）
  - 15 个 EWRAM/IWRAM 变量标签（`gSettings`、`gMoneyDp`、`gPlayerName`、`gP1LifePoints`、`gBanlistPasswordBuffer`、`gPrng` 等）
- `RenameKnownFunctions.py` 追加 5 个函数名：
  - `banlist_password_enter_char` (`FUN_080143f0`)
  - `draw_decimal_with_offset` (`FUN_0802387c`)
  - `internal_card_id_to_card_id` (`FUN_080ee76c`)
  - `select_charset_then_load_name` (`FUN_080ee7ac`)
  - `card_name_lookup_by_internal_id` (`FUN_080eebfc`)
  - 注：wiki 给的 `0x080242c8` / `0x080ee968` 是已有函数内的 LAB，不是函数入口（Ghidra 已识别），未单独命名。

### 4.6 Ghidra 落地 + asm/all.s 重导出

```
tools\asm-regen\ghidra-run-script.bat LabelDataCrystalRomMap.py
tools\asm-regen\ghidra-run-script.bat RenameKnownFunctions.py
tools\asm-regen\ghidra-export-range.bat 080000c0 084c7637 asm\all.s.raw 0
python tools/asm-regen/inject_modes.py asm/all.s.raw asm/all.s
build.bat        # byte-identical 9689337d6aac1ce9699ab60aac73fc2cfdccad9b
```

执行结果：`asm/all.s` 内 71 处出现新符号（如 `bl internal_card_id_to_card_id`、`bl select_charset_then_load_name`、`ldr rN, =cards_ids_array` 等），可读性显著提升。

## 五、byte-identical 验证

```
roms/2343.gba:    9689337d6aac1ce9699ab60aac73fc2cfdccad9b
output/2343.gba:  9689337d6aac1ce9699ab60aac73fc2cfdccad9b
```

build.bat 全程通过，唯一警告是预存在的 `r13 is deprecated`（与本次改动无关）。

## 六、未尽事项

1. **`card-names.s` 起始未修复**：应早 0x18 字节（含 cid=0 6 langs 占位槽）。需要重写 `export_card_data.py` 处理 cid=0 的空槽 + 调整 `rom.s` 的 .incbin 兜底大小。Byte-identical 不受影响，但语义不准。
2. ~~**`0x9E58D0C` `deck_id_and_data_array` 未结构化**~~：核实后是项目 `data/opponent-card-values.s` (ROM `0x1E58D0E`, 27×32B) 的同一段，仅起点差 2B。Ghidra label 已打。

   - Wiki 反汇编 `lsr r1,r4,0x16`（`r4 >> 22`），不是 `<< 16`；27 × 0x10000 = 1.7 MB 也放不下 ROM 剩余空间。
   - 实际 stride 32 B（已在 `data/opponent-card-values.s` 描述）。

---

## 附：可复用流程模板（仅 Phase 2-4，无 ROM 资产定位）

| Phase | 步骤 | 本次状态 |
|------|------|---------|
| Phase 2 ⑦ | 编写导出脚本 | ✓ 1 新 + 2 改 |
| Phase 2 ⑧ | 修改 rom.s 拆分 incbin | ✓ |
| Phase 2 ⑨ | 构建 + byte-identical | ✓ |
| Phase 3 ⑩ | Ghidra 函数重命名 | n/a（无新函数） |
| Phase 3 ⑩ | Ghidra 函数重命名 | ✓ (5 个新名) |
| Phase 3 ⑪ | Ghidra 数据 label | ✓ (21 条新标签) |
| Phase 3 ⑫ | 重导出 all.s + byte-identical | ✓ (71 处新符号引用) |
| Phase 4 ⑬ | 分析报告 | ✓（本文档） |
| Phase 4 ⑭ | 方法论更新 | n/a（流程未变） |
| Phase 4 ⑮ | README 更新 | ✓（根 + refs） |
