# 方法论：字面量池符号化（Ghidra ↔ asm 源同步）

**用途**：把 `asm/all.s` 里大量 `.word 0xXXXXXXXX` 裸地址替换成 `.word <symbol>`，让代码自解释，同时保持 byte-identical 构建。

本文是 [`asset-location.md`](asset-location.md) 之后的**符号化阶段**：资产已定位、`data/*.s` 已结构化，下一步把 Ghidra 里的 USER_DEFINED LABEL 双向同步进 asm 源。

---

## 一、三方分工

```
Ghidra symbol table              asm 源（rom.s/data/*.s/*.inc）
        │                                      │
        │ ExportRangeToGas.py 的                │ GAS 汇编 .word <name>
        │ resolve_word_symbol() 查 outgoing ref │ 通过 label: 或 .equ resolve
        ▼                                      ▼
  asm/all.s 里的 .word <name> ←─── 必须双向同名才闭环 ───→
```

**三方缺一处都失败**：
| 缺口 | 后果 |
|---|---|
| Ghidra 没 label | `resolve_word_symbol` 查不到 → asm/all.s 仍 `.word 0xXXXX` |
| asm 源没 label / `.equ` | GAS `undefined reference to <name>` → 构建失败 |
| 三处名字不一致 | `redefinition` 或 `undefined`，构建失败 |

**自动化分工**（项目已建好）：
- `tools/ghidra-labeling/LabelDataCrystalRomMap.py`：手工维护 Ghidra label 列表
- `tools/ghidra-labeling/MarkRamIoPointers.py`：扫代码区 4-byte data，自动 `createData(Pointer)` 让 Ghidra 建 outgoing reference
- `tools/ghidra-labeling/ExportRomLabelsToInc.py`：扫 Ghidra symbol table，自动写 `constants/rom_data.inc`（asm 源已有同名 label 时 exclude，避免 redefinition）
- `tools/asm-regen/ghidra/ExportRangeToGas.py::resolve_word_symbol()`：导出 asm/all.s 时，把 `.word 0xXXXXXXXX` 替换成 `.word <symbol>`（白名单 EWRAM/IWRAM/MMIO + ROM `LABEL` 类型）

---

## 二、决策树：什么场景做符号化

```
asm/all.s 残留裸 .word 0xXXXXXXXX
      │
      ├─ 0x02xxxxxx (EWRAM) / 0x03xxxxxx (IWRAM) → 加 .equ 到 ewram.inc / iwram.inc
      ├─ 0x04xxxxxx (MMIO)                       → 已在 gba_io.inc (96 个)
      ├─ 0x08xxxxxx / 0x09xxxxxx (ROM 数据段)
      │     ├─ asm 源已有 label:                 → LabelDataCrystalRomMap.py 加条目同步 Ghidra
      │     └─ asm 源无 label                    → 加 label: 到 asm/rom.s 或 data/*.s,
      │                                            或 ExportRomLabelsToInc 自动生成 .equ
      └─ THUMB 函数地址 (0x08xxxxxx 末位 1)        → 不符号化 (FUNCTION 缺 |1 位破坏 byte-identical)
```

**白名单策略**（`resolve_word_symbol` 与 `MarkRamIoPointers` 必须一致）：
- EWRAM/IWRAM/MMIO（`0x02..0x04xxxxxx`）：放行任意 `SourceType.USER_DEFINED`
- ROM 数据段（`0x08..0x09xxxxxx`）：仅放行 `SymbolType.LABEL`，排除 `FUNCTION`
- 排除 auto-gen 前缀：`DAT_/LAB_/FUN_/PTR_/SUB_/UNK_/SWITCH_`
- PALRAM/VRAM/OAM（`0x05..0x07xxxxxx`）：不处理（loader 未定义 symbol）

### 2.1 三种符号化机制（按数据类型选）

上面的决策树是 **① 地址指针** 路径。完整有三种机制：

| 数据类型 | 机制 | GAS 端定义处 | 导出器函数 |
|---|---|---|---|
| **① 地址指针**（`.word` 指向 RAM/IO/ROM 某符号） | Ghidra USER_DEFINED label + DATA ref | `rom_data.inc`/`ewram.inc` 等 `.equ`（自动/手维护） | `resolve_word_symbol` |
| **② 纯数值常量**（位掩码 / IO 初值等，**无目标地址**） | Ghidra **data-equate**（`EquateTable.createEquate`+`addReference(数据地址,op0)`） | `constants/*.inc` 的 `.equ`/`.set`（手维护） | `resolve_word_equate` |
| **③ 需结构化的数据本体**（字符串 / 描述符 / 表） | carve 成 `<label>: .asciz/.byte/.word`，gap 用 `.incbin` | 数据本身即定义（`data/*.s` 或 `rom.s` carve 块） | `resolve_word_symbol`（指向 carve label） |

**B2 优先级陷阱**：导出器对 `.word` **先调 `resolve_word_symbol`、再兜底 `resolve_word_equate`**。
- 同一地址**若已有 USER_DEFINED label，data-equate 会失效（成死代码）**——给已 label 的地址别再设 equate。
- 反之**纯数值常量别建 Ghidra label**（GAS 端无该地址定义 → 链接失败），用 data-equate。

**B3 混合区不可整片自动 carve**：区域若是字符串 + 二进制 + 图形混合（如 SDK 调试串池夹 tile/指针表），
"可打印即字符串"的启发式分类会把图形数据（如 `0x21`=`!` 连串、SJIS 日文）误判成 `.asciz` → 产出脏假串。
正确做法：**只 carve 被代码引用的特定项**，其余 gap 用 `.incbin "roms/2343.gba", off, len` 原样保留。
（byte-identical 不在乎 `.asciz` vs `.byte` 分类，仅影响可读性——但脏分类反害可读性，故只 carve 确定项。）

**B4 整片 carve 只适用于干净连续数据块**（如 demo/exodia 资源块 = 描述符 + 路径池 + 指针表连续 548B，
可整体 carve 成 `data/*.s`）。

---

## 三、标准 pipeline（6 步）

每次新增/修改 label 后跑一遍：

```bat
:: 1. 同步 Ghidra symbol table
tools\asm-regen\ghidra-run-script.bat LabelDataCrystalRomMap.py

:: 2. 批量 pointer 化字面量池 (Ghidra outgoing reference 才能建立)
tools\asm-regen\ghidra-run-script.bat MarkRamIoPointers.py

:: 3. 重生成 constants/rom_data.inc (ROM 段 .equ, exclude asm 源已有 label)
tools\asm-regen\ghidra-run-script.bat ExportRomLabelsToInc.py

:: 4. 重导出 asm/all.s
tools\asm-regen\ghidra-export-range.bat 080000c0 084c7637 asm\all.s 0
python tools\asm-regen\inject_modes.py

:: 5. 构建
build.bat

:: 6. byte-identical 验证 (必须无差异)
fc /b roms\2343.gba output\2343.gba
```

完整步骤无差异即完成。如果 fc 报差异 → 立刻 git diff 查看 asm/all.s 看哪行变了，常见原因见 §五。

---

## 四、验证 ROM 数据段边界（拆 .bin 前必做）

**经验**：基于"静态分析推断"或"相邻 anchor 推算"的拆分边界**经常错**（HUD 错位 0xB40 字节、icon 错位 0xB40 字节都是案例）。任何拆分前用三连击验证：

### 4.1 asm/all.s 字面量池查
```bash
grep -c "\.word\s\+0x09[xx][xx][xx][xx][xx]" asm/all.s
```
若 ≥ 1 命中：该地址在代码字面量池被引用，是真 base。

### 4.2 ROM 全文 LE pattern 扫
```python
with open("roms/2343.gba", "rb") as f: rom = f.read()
pat = bytes([addr & 0xff, (addr >> 8) & 0xff, (addr >> 16) & 0xff, (addr >> 24) & 0xff])
positions = [p for p in range(0, len(rom)-3, 4) if rom[p:p+4] == pat]
```
4-byte 对齐命中数 ≥ 1：被某个指针表/数据结构引用。

### 4.3 反查整段被引用的 base 集合
```python
# 范围内每个 4-byte 对齐位置, 看是否落在 [seg_lo, seg_hi]
for pos in range(0, len(rom)-3, 4):
    v = int.from_bytes(rom[pos:pos+4], "little")
    if seg_lo <= v <= seg_hi:
        found.setdefault(v, []).append(pos)
```
高频 base（≥ 5 引用 + 4-byte 对齐）= 真数据段起点。

### 4.4 视觉验证（tile 数据）
导出 4bpp tile → PNG（可用临时 Python + PIL）。**用对应 palette 渲染彩色图比统计签名可靠**——本会话因迷信"palette high bit 应 < 5%" 误判 palette 位置，被实际渲染的彩色 icon 打脸。

---

## 五、byte-identical 重构 pattern

只要 ROM 字节流不变，asm 源**怎么切分都可以**：

| 操作 | 示例 |
|---|---|
| `.incbin "roms/2343.gba", off, size` → 拆 .bin + label | `unused_inner_image:` + 新 .bin |
| `.incbin "table.bin"` → `.word <label>` 列表 | `duel_field_outer_tile_pointers` 7 × `.word` |
| 裸 `.word 0xXXXX` → `.word <symbol>` | 走 §三 pipeline |

**关键约束**：
1. **linker VMA 必须 = ROM 基址 0x08000000**（`ld_script.txt` 已是）—— `.word campaign_outer_image` 解析为 `0x0985504C`，等于原 ROM 字节
2. **THUMB 函数 label 不能 `.word`**：缺 `|1` 位，字节差 1 → byte-identical 失败
   - 防御：白名单只接受 `SymbolType.LABEL`，FUNCTION 排除（`ExportRangeToGas.resolve_word_symbol` + `MarkRamIoPointers`）
3. **同名 symbol 唯一**：GAS 不允许 `name:` 和 `.equ name, ...` 并存 → `ExportRomLabelsToInc.py` 必须 exclude asm 源已定义的名字

---

## 六、GBA 地址映射陷阱

```
ROM 32MB 挂载: GBA 0x08000000 .. 0x09FFFFFF (连续, 不是镜像!)

ROM offset 范围              GBA 地址前缀
──────────────────────────────────────────
0x0000000 .. 0x0FFFFFF       0x08xxxxxx
0x1000000 .. 0x1FFFFFF       0x09xxxxxx     ← bit 24 自然进位
```

**别混淆**：
- `0x08510640` 和 `0x09510640` 是**完全不同**的 ROM 字节（ROM offset 0x510640 vs 0x1510640）
- `0x09xxxxxx` **不是** WS1 镜像。真正的 WS1/WS2 镜像在 `0x0Axxxxxx / 0x0Cxxxxxx`，本游戏不用
- 搜代码引用时 `0x08` 和 `0x09` 形式都要扫——同段 ROM 数据起点 < 0x01000000 用 0x08，> 用 0x09

---

## 七、命名一致性

`LabelDataCrystalRomMap.py` 提供 `RENAMES` 和 `REMOVALS` 机制实现幂等迁移：

```python
RENAMES = [
    # 旧名 → 新名 (data/*.s 注释里的正式名优先)
    ("card_names_pool", "card_names_table"),
    ("card_desc_text_pool", "card_descs_table"),
    # 命名细化 (与 _palette_pointers / _tilemap_pointers 并列)
    ("duel_field_outer_pointer_table", "duel_field_outer_tile_pointers"),
]

REMOVALS = [
    # 地址错的旧 label (例: 抄 wiki 时偏 0x60 字节)
    (0x095FFF6C, "card_effect_text_pool"),
]
```

每次跑 `LabelDataCrystalRomMap.py` 都执行 rename + remove，幂等。

**命名规范**：
- 数据池（实际 byte 数据）：`<scope>_table`（如 `card_names_table`、`card_stats_table`）
- 索引/指针表：`<scope>_pointer_table` 或 `<scope>_pointers`（如 `card_name_pointer_table`、`duel_field_outer_tile_pointers`）
- base + offset 访问的数组：base 用单一 label（如 `campaign_inner_image`，其他 mode 由 `base + idx * stride` 访问，不需各自 label）
- **字面量池槽 label**（函数内 `<label>: .word <目标>` 的槽**自身**）：用 **`<函数名>_<目标>`** 前缀，
  靠函数名避免"多函数引用同一目标"时 label 重复（如 `init_blend_transition_params_assert_blend1_0_blend1_16`、
  `gl_set_brightness_gl_common_c_filename`；同函数引用同目标两次才追加地址尾 `_<低3位>`）。
  ⚠ **不要用全局 `ptr_<目标>`** 给可被多处引用的目标——会跨函数碰撞；`ptr_<目标>` 仅适合全局唯一、单次引用的槽（如 crt0 的 `ptr_intr_vector`）。

---

## 八、实战案例：131 icon 修正

**初始假设错误**：
```
27 × opponent_icon_tiles @ 0x188DA70, 0x1E60 B
↓ 中间 0x6B00 B "未知数据"
27 × opponent_icon_palettes @ 0x18963D0, 0x360 B
```

**反查发现**（用 §四 三连击）：
1. `0x09888DA70` 在整个 32MB ROM 0 引用 → **不是真 base**
2. `0x0988CF30` 被代码 11 次引用 → 真 base（错位 0xB40 B）
3. `0x09896290` 被代码 8 次引用 + 4-byte 对齐 → 真 palette base
4. `(0x09896290 - 0x0988CF30) / 0x120 = 131` 整除 → **N = 131**（不是 27）
5. 用 N=131 + palette 紧跟 tiles 渲染彩色 PNG → 玩家头像 + 27 对手 + 其他角色全部清晰

**修正**：
- `export_gfx.py` ICONS list 改为 `[(f'icon_{i:03d}', tile_base+i*0x120, pal_base+i*0x20) for i in range(131)]`
- `asm/rom.s` 重切：前段 incbin `0x26510 → 0x259D0`、新 131 icon tile + 131 palette、后段起点 `0x1896730 → 0x18972F0`
- `LabelDataCrystalRomMap.py` 加 `icon_tiles_base / icon_palettes_base`
- 跑 §三 pipeline → byte-identical ✓

**教训**：
- 相邻 `.incbin` 注释推断的边界 ≠ 真 base
- 灰度渲染容易误判，**用对应 palette 渲染彩色才能定边界**
- 数量假设也要验证（不要默认"27 对手所以是 27 个"——可能含玩家头像）

---

## 九、相关文件清单

| 文件 | 用途 |
|---|---|
| `tools/ghidra-labeling/LabelDataCrystalRomMap.py` | Ghidra label 主表 + RENAMES + REMOVALS |
| `tools/ghidra-labeling/MarkRamIoPointers.py` | 扫代码区批量 pointer 化字面量 |
| `tools/ghidra-labeling/ExportRomLabelsToInc.py` | Ghidra → constants/rom_data.inc 自动同步 |
| `tools/asm-regen/ghidra/ExportRangeToGas.py` | 符号化核心：`resolve_word_symbol()`（地址指针）+ `resolve_word_equate()`（纯数值常量 data-equate）；`emit_defined_data` 还支持数据行 EOL 注释 |
| `tools/asm-regen/inject_modes.py` | 重导出后修 ARM/Thumb mode + s 后缀 |
| `tools/gen_gba_io_inc.py` | 从 refs/gba-ghidra-loader 生成 96 条 MMIO `.equ` |
| `constants/ewram.inc` | EWRAM 变量 `.equ`（手维护） |
| `constants/iwram.inc` | IWRAM 变量 `.equ`（手维护） |
| `constants/gba_io.inc` | MMIO 寄存器 `.equ`（自动生成） |
| `constants/rom_data.inc` | ROM 数据段 symbol `.equ`（自动生成） |
