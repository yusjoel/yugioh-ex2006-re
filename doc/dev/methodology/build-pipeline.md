# 方法论：构建流水线与 asm/all.s 再生成

**用途**：把定位到的 ROM 资产结构化到 `data/*.s` / `graphics/bin/`，完成 byte-identical 构建，Ghidra 反向标注后再生成 `asm/all.s` 并再次验证。

本文覆盖 [`asset-location.md`](asset-location.md) 定位成功后的**所有后续流程**：结构化 → 构建 → 反向标注 → 再生成 → 二次构建。

---

## 一、完整端到端工作流（14 阶段，4 大 Phase）

```
┌─────────────────────────────────────────────────────────────┐
│  Phase 1: 定位  [详见 asset-location.md]                    │
│  ① 游戏截图 + VRAM/PALRAM/OAM 快照                          │
│  ② OAM / IO 分析 → sprite 尺寸/色深/tile 地址                │
│  ③ 三方向静态分析 (B=VRAM字面量 / C=IO指纹 / A=GDB动态)     │
│  ④ ROM 字节搜索验证 VRAM↔ROM 匹配                           │
│  ⑤ 调色板定位 (PALRAM dump → ROM 搜索)                      │
│  ⑥ 导出 PNG + 截图目视对比                                  │
├─────────────────────────────────────────────────────────────┤
│  Phase 2: 结构化                                            │
│  ⑦ 编写导出脚本 (ROM → bin + PNG + .s)                      │
│  ⑧ 修改 rom.s (拆分 incbin → .include data/*.s)             │
│  ⑨ 构建 + byte-identical 验证                               │
├─────────────────────────────────────────────────────────────┤
│  Phase 3: 反向标注                                          │
│  ⑩ Ghidra 函数重命名 (RenameKnownFunctions.py)              │
│  ⑪ Ghidra 数据 label (LabelPackBanners.py)                  │
│  ⑫ 重导出 asm/all.s + 构建验证                              │
├─────────────────────────────────────────────────────────────┤
│  Phase 4: 文档                                              │
│  ⑬ 分析报告 (doc/analysis/*.md 或 doc/dev/data-structure/)  │
│  ⑭ 方法论更新 (asset-location.md 视情况)                    │
└─────────────────────────────────────────────────────────────┘
```

### Phase 1: 定位（外链）

定位流程详见 [`asset-location.md`](asset-location.md) §二（动态路径六步）或 §三（静态路径四阶段）。以下示范以 pack banner 为实战案例：

| 方向 | 指纹 | 命中数 | 定位到 |
|------|------|--------|--------|
| B: VRAM 字面量 | `0x06016000` | 2 | `FUN_080bdfac`（状态机） |
| C: IO 指纹 | BG2CNT=`0x1E0D` | 1 | `FUN_080d8d84 → FUN_080d971c`（页面初始化） |
| A: GDB hbreak | 已知函数 + 按键注入 | 6 hits | 验证参数和调用链 |

**Phase 1 关键教训**：
- 方向 B 和 C 找到的是**互补的**函数群（运行时状态机 vs 一次性初始化）
- GDB VRAM watchpoint 因 DMA 未触发，改用 hbreak 在已知函数上成功
- `0x06014000` 有 52 处命中太多，改用 `0x06016000`（仅 2 处）作为强指纹
- 初次检查 ROM 数据时**必须看完整 block 不只看前几字节**（pack-banner 前 16 B 是零 padding，误判为"数据全零"）

### Phase 2: 结构化

#### ⑦ 编写导出脚本

模板：`tools/rom-export/export_<模块>.py`

**产出**：
- `graphics/bin/<模块>/*.bin` — tile 二进制（不入库，由导出脚本生成）
- `graphics/images/<模块>/*.png` — 彩色预览（不入库）
- `data/<模块>.s` — 结构化汇编（入库）

**设计要点**：
- **指针表用 `.word <label>` 形式**，不导出为 bin——汇编器会根据 label 位置自动计算指针值
- **tile 数据用 `.incbin`** 引用导出的 bin 文件
- **PNG 渲染必须按 GBA 8×8 tile 结构解码**，不能当线性像素处理
- **目视对比验证**：与 Phase 1 截图对比确认渲染正确（这一步拦截 tile 格式 / bpp / 行列序错误——这类错误在 byte-identical 构建中不会暴露）

#### ⑧ 修改 rom.s

**操作**：将覆盖目标区域的大 `.incbin` 拆分为三段：

```
原: .incbin "roms/2343.gba", 0x1CCD290, 0xF1D8A    @ 一整段

改: .incbin "roms/2343.gba", 0x1CCD290, 0x16D0      @ 前部
    .include "data/pack-banners.s"                    @ 结构化数据
    .incbin "roms/2343.gba", 0x1CE822C, 0xD6DEE      @ 后部
```

**校验**：三段大小之和 = 原始大小（例：`0x16D0 + 0x198CC + 0xD6DEE = 0xF1D8A`）

#### ⑨ 构建 + byte-identical 验证

```bat
as.exe -mcpu=arm7tdmi -o output/rom.o asm/rom.s
ld.exe -T ld_script.txt -o output/2343.elf output/rom.o
objcopy.exe -O binary output/2343.elf output/2343.gba

fc /b roms\2343.gba output\2343.gba
@ 或
python -c "print(open('roms/2343.gba','rb').read()==open('output/2343.gba','rb').read())"
```

**必须零差异**。构建失败时优先检查：
- 三段大小之和是否等于原始 `.incbin` 的 size
- 新 `.include` 的 `.s` 是否有语法错误导致汇编失败
- `data/*.s` 中的宏展开字节数是否与原 ROM 吻合

### Phase 3: 反向标注

#### ⑩ Ghidra 函数重命名

**脚本**：`tools/ghidra-labeling/RenameKnownFunctions.py`

**流程**：
1. 追加本次定位的新函数名到脚本
2. headless 执行：`tools\asm-regen\ghidra-run-script.bat RenameKnownFunctions.py`
3. Ghidra 自动 `Save succeeded`

Ghidra 会把 `FUN_xxxxxxxx` 替换为语义名，并在 plate comment 里写一行简短说明。完整登记表与脚本用法见 `doc/dev/ghidra-function-names.md`。

#### ⑪ Ghidra 数据 label

**脚本**：`tools/ghidra-labeling/LabelPackBanners.py` / `LabelPackCardLists.py` 等，每类数据一个脚本

**特点**：从 ROM 指针表动态读取各地址，不硬编码——即使数据位置调整脚本也能自动跟随。

#### ⑫ 重导出 asm/all.s

```bat
tools\asm-regen\ghidra-export-range.bat 080000c0 084c7637 asm\all.s.raw 0
grep -v -E "^\.(thumb|arm)\s*$" asm/all.s.raw > asm/all.s.raw.nomode
python tools/asm-regen/inject_modes.py asm/all.s.raw.nomode asm/all.s
build.bat
```

导出后 `bl FUN_080db860` 会变为 `bl pack_banner_tile_copy`，代码可读性大幅提升。再次验证 byte-identical。

详细流水线见本文 §二。

### Phase 4: 文档

| 文档类型 | 位置 | 内容 |
|---------|------|------|
| Spec（最终数据结构） | `doc/dev/data-structure/<名>.md` | ROM 地址、字节布局、公式（**不写过程**） |
| Narrative（调研叙事） | `doc/analysis/<名>-location.md` | 按时间线展开，失败路径归档 |
| 方法论更新 | `doc/dev/methodology/` | 仅当发现新方法或修正旧结论 |
| README | `README.md` | 构建前置步骤、数据提取表、工具脚本表 |
| 函数名登记 | `doc/dev/ghidra-function-names.md` | 追加本轮 rename 条目 |

---

## 二、asm/all.s 再生成子流程（Phase 3 细节）

**验证状态**：✅ 端到端 byte-identical 通过

### 流水线总览

```
Ghidra 数据库 (ghidra/Yu-Gi-Oh WCT 2006.gpr)
        │
        │  tools/asm-regen/ghidra-export-range.bat     （调 analyzeHeadless）
        │  tools/asm-regen/ghidra/ExportRangeToGas.py  （Jython，Ghidra 内执行）
        ▼
asm/all.s.raw                       （约 20.5 MB，含 14088 行 .arm/.thumb）
        │
        │  grep -v '^\.(thumb|arm)\s*$'     （剥掉 Jython 的 mode 指令）
        ▼
asm/all.s.raw.nomode
        │
        │  python tools/asm-regen/inject_modes.py <in> <out>
        │     - 注入 3 处 .arm/.thumb 切换（依据 hex 宽度和 BL/BLX 模式）
        │     - 补全 141015 处 Thumb 设标志指令的 s 后缀
        │     - 应用 2 处手动补丁
        ▼
asm/all.s                           （更新完成）
        │
        │  build.bat  (as → ld → objcopy)
        ▼
output/2343.gba   ✓ byte-identical
```

**导出范围**：`0x080000c0 – 0x08ffffff`（16 MB，跳过 ROM 头；ROM 头由 `asm/rom_header.s` 和 `asm/crt0.s` 维护）。

**完整流水线耗时**：Ghidra headless 导出约 90 秒，`inject_modes.py` 约 20 秒，build 约 5 秒。

### 各脚本职责

#### 1. `tools/asm-regen/ghidra-export-range.bat`

Windows 批处理包装，调用 Ghidra `support/analyzeHeadless.bat` 以无 GUI 方式执行 Jython 脚本。

**参数**：`<start_hex> <end_hex> <output_path> [xrefs 0|1]`

**读取**：
- `GHIDRA_HOME` 环境变量（Ghidra 安装根目录，见 `LOCAL.md`）
- 项目 `ghidra/Yu-Gi-Oh WCT 2006.gpr`（`.gitignore` 忽略）
- 处理目标 `2343.gba`（项目内已导入）

**固定参数**：`-noanalysis -readOnly`（不触发分析、只读打开，避免污染项目）

#### 2. `tools/asm-regen/ghidra/ExportRangeToGas.py`（Jython）

出处：Ghidra 安装目录 `Ghidra/Features/GBA/ghidra_scripts/ExportRangeToGasS_Jython.py`（2026-03-09 版）。本仓库副本额外加了 headless 参数支持（`getScriptArgs()` 分支）。

**职责**：遍历指定地址范围，按 listing 输出 GAS 风格 `.s`：

- **指令行**：`<mnemonic operands>  @ <address> <hex>`，同时做几项 GAS 语法修正（见下）
- **已定义数据**：`.word / .hword / .byte`（Structure 字段展开为独立行）
- **UNDEF 连续区**：`> 16 字节` 用 `ROM_INCBIN` 宏（`.incbin` 原 ROM）；否则 `.byte`
- **label**：Ghidra 已有 symbol 直接输出；ADR 目标若范围内无 symbol 则合成 `DAT_<addr>`
- **label 全局去重**：避免 `switchD` 等同名符号在不同地址重复定义

**GAS 语法修正**：

| Ghidra 原文 | 改写为 | 说明 |
|---|---|---|
| `ldr rX,[0xADDR]` | `ldr rX, <label>` 或 `ldr rX, [pc, #imm]` | GAS 不支持 `[绝对地址]` 寻址 |
| `b / bl / cbz / cbnz 0xADDR` | `b <label>` 等 | 分支目标符号化 |
| `adr r0,0xADDR` | `adr r0, DAT_xxx`（必要时合成） | GAS 无法对绝对地址做 PC-relative |

**输出 `.arm` / `.thumb` 切换**：Jython 版试图"每条指令判定 Thumb/ARM，发生变化就输出 mode 指令"。判定顺序：
1. 地址对齐（`addr % 4 != 0` ⇒ Thumb）
2. `ProgramContext` 的 `TMode` / `ISAMode` 寄存器
3. 指令长度 == 2 ⇒ Thumb
4. 默认 ARM

⚠️ **缺陷：自动 mode 切换不可用**

实测 Jython 的 mode 切换结果汇编失败（5 处 `misaligned branch destination`），因此**必须在下游剥掉**。保留指令是因为 GUI 场景下它仍然是有用的提示；headless 流水线里由 `inject_modes.py` 重新注入。

根因推测：Ghidra 数据库中部分区段的 `TMode` 未被正确设置，或判定顺序在某些边界情况下给出错误答案。调试成本高，绕开更划算。

**Headless 接口**：
- GUI 模式：走 `ask*` 交互（XREFS 开关、起止地址、输出文件、是否导出 structs）
- Headless 模式：通过 `getScriptArgs()` 读 `<start> <end> <out> [xrefs]` 四个位置参数，跳过所有 `ask*`

#### 3. `tools/asm-regen/inject_modes.py`

Python 3 后处理脚本。**强烈依赖 Jython 导出每行末尾注释中的 hex bytes**（`@ <addr> <hex>`）。

**输入 / 输出**：
- `inject_modes.py`（无参）→ 原地处理 `asm/all.s`
- `inject_modes.py <in>` → 原地处理指定文件
- `inject_modes.py <in> <out>` → 从 `<in>` 读，写到 `<out>`（验证管线时用，避免污染 `asm/all.s`）

**职责 1：注入 `.arm` / `.thumb` 模式切换**

规则：
- 4 个 hex 字符（2 字节）→ THUMB
- 8 个 hex 字符（4 字节），首 halfword `0xF000–0xF7FF` 且次 halfword `0xE800`/`0xF800` → THUMB BL/BLX（ARMv4T）
- 其余 8 个 hex 字符 → ARM

仅在模式**真正发生改变**时输出切换指令。本 ROM 全量实际只需 3 处（`.thumb` @181, `.arm` @359725, `.thumb` @360074）。这就是为什么 Jython 的 14088 处 mode 切换是"过度输出"。

**职责 2：补全 Thumb 设标志指令的 `s` 后缀**

`.syntax unified` 要求设标志的 Thumb-1 指令显式写 `s`。脚本按规则识别并改写：

- `ALWAYS_S = {adc, and, asr, bic, eor, lsl, lsr, mul, mvn, orr, ror, sbc}`：Thumb-1 只有设标志编码，必须加 `s`
- `add` / `sub`：SP/PC 相关不设标志；含高寄存器（r8-r15）不设；其余加 `s`
- `rsb`：Thumb-1 为 `rsbs rd, rs, #0`，无立即数时自动补齐操作数

**实测**：全量跑一次补 141015 处。

**职责 3：手动补丁（hardcoded）**

通用规则无法覆盖的少数特殊指令，按文本精确匹配替换：

| 原文 | 替换为 | 原因 |
|---|---|---|
| `adds r4,r4,#0x4  @ 0809fb20 241d` | `.hword 0x1d24` | Ghidra 输出 3-operand 形式，GAS 编码成 2-operand，字节不一致；直接按原字节写死 |
| `bx r11  @ 087e0bc4 5e47` | `.hword 0x475e` | 原始编译器产生的 `bx r11` 编码未清零 SBZ 位（`5e47`），GAS 正确编码为 `5847`，byte 不一致；按原字节写死 |

这 2 条都是"无法通过汇编规则重现原始字节"的**编译器历史产物**，必须硬写。

### 已知仍未解决的问题

1. **Jython 的 `.arm`/`.thumb` 自动输出不可用**：5 处错位导致 `misaligned branch destination`。当前绕开方案是下游 `grep -v` 剥掉。若未来有人用 Ghidra GUI 直接导出 `.s` 并尝试汇编，会踩这个坑。
2. **`inject_modes.py` 的两处 hword 补丁是硬编码字节**：`0x1d24` 和 `0x475e` 绑定具体地址（`0809fb20`、`087e0bc4`）。如果 Ghidra 重新分析后这些地址的指令形式变了，补丁会匹配失败。
3. **141015 处 `s` 后缀是大规模字符串改写**：规则覆盖绝大多数情况，但遇到新指令模式可能遗漏，需要通过汇编报错反馈。

### 参考命令

```bash
# 全量重新生成 asm/all.s（验证过的最短路径）
cmd //c "tools\asm-regen\ghidra-export-range.bat 080000c0 08ffffff doc\temp\all.s.raw"
grep -v -E '^\.(thumb|arm)\s*$' doc/temp/all.s.raw > doc/temp/all.s.raw.nomode
python tools/asm-regen/inject_modes.py doc/temp/all.s.raw.nomode asm/all.s

# 验证 byte-identical
rm -rf output && mkdir -p output
as.exe -mcpu=arm7tdmi -o output/rom.o asm/rom.s
ld.exe -T ld_script.txt -o output/2343.elf output/rom.o
objcopy.exe -O binary output/2343.elf output/2343.gba
cmp roms/2343.gba output/2343.gba && echo OK
```

---

## 三、可复用 checklist

后续定位新资产时，按以下清单逐项打勾：

**Phase 1 定位**（详见 `asset-location.md`）：
- [ ] 游戏截图 + VRAM/PALRAM/OAM dump
- [ ] OAM 解析（sprite 尺寸/色深/tile/mapping 模式）
- [ ] 方向 B/C 静态分析（选最强指纹，grep 密度 < 5）
- [ ] 方向 A 动态验证（hbreak 优先于 watchpoint，DMA 绕过问题）
- [ ] ROM 字节搜索（VRAM tile → ROM 匹配，**检查完整 block 不只看前几字节**）
- [ ] 调色板搜索（PALRAM sub-palette → ROM 匹配）
- [ ] 渲染 PNG + 截图目视对比（**拦截 tile 格式/bpp/行列序错误**）

**Phase 2 结构化**：
- [ ] 导出脚本（bin + PNG + .s，指针表用 label 不用 bin）
- [ ] rom.s 拆分（前部 incbin + .include + 后部 incbin，大小校验）
- [ ] 构建 byte-identical

**Phase 3 反向标注**：
- [ ] Ghidra 函数重命名（追加 `RenameKnownFunctions.py`）
- [ ] Ghidra 数据 label（新建 `Label<模块>.py`）
- [ ] 重导出 asm/all.s + 再次构建验证

**Phase 4 文档**：
- [ ] Spec 写入 `doc/dev/data-structure/<名>.md`
- [ ] Narrative 写入 `doc/analysis/<名>-location.md`
- [ ] 函数名登记表 (`ghidra-function-names.md`) 追加
- [ ] README + data-analysis-coverage.md 更新

---

## 四、产出清单模板

单次资产定位 + 结构化的典型产出：

| 类型 | 文件 | 入库 |
|------|------|------|
| 导出脚本 | `tools/rom-export/export_<模块>.py` | ✓ |
| 结构化汇编 | `data/<模块>.s` | ✓ |
| ROM 引用 | `asm/rom.s`（拆分 incbin + .include） | ✓ |
| 反汇编代码 | `asm/all.s`（函数名更新） | ✓ |
| Ghidra 脚本 | `tools/ghidra-labeling/RenameKnownFunctions.py`（追加条目） | ✓ |
| Ghidra 脚本 | `tools/ghidra-labeling/Label<模块>.py`（新数据 label） | ✓ |
| GDB 脚本 | `doc/dev/scripts/gdb_<场景>.gdb`（可选） | ✓ |
| Spec 文档 | `doc/dev/data-structure/<模块>.md` | ✓ |
| Narrative 文档 | `doc/analysis/<模块>-location.md`（若是从零定位） | ✓ |
| 函数名登记 | `doc/dev/ghidra-function-names.md`（追加） | ✓ |
| README | `README.md` | ✓ |
| tile 二进制 | `graphics/bin/<模块>/*.bin` | ✗（导出生成） |
| 彩色预览 | `graphics/images/<模块>/*.png` | ✗（导出生成） |

---

## 五、相关文档

| 文件 | 关系 |
|------|------|
| [`asset-location.md`](asset-location.md) | Phase 1 定位方法论（动态 + 静态路径） |
| [`../tools/gdb-debugging.md`](../tools/gdb-debugging.md) | GDB batch 脚本、断点矩阵、12 个坑 |
| [`../tools/mgba-mcp.md`](../tools/mgba-mcp.md) | mGBA MCP 15 个工具 + Lua 教程 |
| `doc/dev/ghidra-function-names.md` | Ghidra 重命名登记表（Phase 3 产出） |
| `data-analysis-coverage.md` | ROM 分析覆盖率总览（每次结构化后更新） |
