# 方法论：构建流水线与 asm/all.s 再生成

**用途**：把定位到的 ROM 资产结构化到 `data/*.s` / `graphics/bin/`，完成 byte-identical 构建，Ghidra 反向标注后再生成 `asm/all.s` 并再次验证。

本文覆盖 [`asset-location.md`](asset-location.md) 定位成功后的**所有后续流程**：结构化 → 构建 → 反向标注 → 再生成 → 二次构建。

---

## 一、完整端到端工作流（17 阶段，4 大 Phase）

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
│  ⑩ 备份 .rep                                                 │
│  ⑪ Ghidra 函数重命名 (RenameKnownFunctions.py)              │
│  ⑫ Ghidra 数据 label (LabelDataCrystalRomMap.py)            │
│  ⑬ 重导出 asm/all.s + 构建验证 (含字面量池三连击)            │
│  ⑭ Ghidra → CSV 函数名同步 (sync_ghidra_names_to_proposals) │
│  ⑮ (可选) ExportComments 注释纳入 git                        │
├─────────────────────────────────────────────────────────────┤
│  Phase 4: 文档                                              │
│  ⑯ 分析报告 (doc/analysis/*.md 或 doc/dev/data-structure/)  │
│  ⑰ 方法论更新 (asset-location.md 视情况)                    │
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

#### ⑩ 备份 Ghidra 工程（写入前必做）

```bash
TS=$(date +%Y%m%d-%H%M%S)
cp -r "ghidra/Yu-Gi-Oh WCT 2006.rep" "ghidra/Yu-Gi-Oh WCT 2006.rep.bak-${TS}-pre-<task>"
```

任何 Ghidra script 写入前必备份。Ghidra 工程是 source of truth，写坏只能从 .rep 备份恢复。

#### ⑪ Ghidra 函数重命名

**脚本**：`tools/ghidra-labeling/RenameKnownFunctions.py`

**流程**：
1. 追加本次定位的新函数名到脚本（`(orig, new, plate_comment)` 三元组）
2. headless 执行：`tools\asm-regen\ghidra-run-script.bat RenameKnownFunctions.py`
3. Ghidra 自动 `Save succeeded`

Ghidra 会把 `FUN_xxxxxxxx` 替换为语义名，并在 plate comment 里写一行简短说明。完整登记表与脚本用法见 `doc/dev/ghidra-function-names.md`。

⚠️ **mojibake 坑（2026-04-30 修过历史 110 条）**：中文注释字符串必须 `.decode("utf-8")` 转成 unicode 再传给 Java API（如 `cu.setComment`），否则 Java 把 utf-8 字节当 Latin-1 收成 String，存进 .rep 全是乱码。`RenameKnownFunctions.do_rename` 已修。如发现历史 mojibake，跑 `tools/ghidra-labeling/FixCommentEncoding.py` 一次性修（latin-1↔utf-8 round-trip 检测，幂等）。

#### ⑫ Ghidra 数据 label

**脚本**：`tools/ghidra-labeling/LabelDataCrystalRomMap.py`（共享中央表）/ `LabelPackBanners.py` / `LabelPackCardLists.py` 等，每类数据一个脚本。

**特点**：从 ROM 指针表动态读取各地址，不硬编码——即使数据位置调整脚本也能自动跟随。

加新 label **三连击**（缺一漏一就 build fail "undefined reference"）：

```bash
# 1. 加 USER_DEFINED label
tools/asm-regen/ghidra-run-script.bat LabelDataCrystalRomMap.py
# 2. 给字面量池 .word <addr> 加 DATA reference, 让 .word 自动符号化为 .word <label_name>
tools/asm-regen/ghidra-run-script.bat AddLiteralPoolReferences.py
# 3. 把 INCBIN 内部 label (如 game_str_id_remap_table @ 0x250) 写成 .equ 给 GAS 链接器
tools/asm-regen/ghidra-run-script.bat ExportRomLabelsToInc.py
```

`ExportRomLabelsToInc.py` 范围 = `[0x080000C0, 0x09FFFFFF]`，但已在 asm/*.s 中以 `name:` 形式 disasm 出的会自动跳过（`scan_existing_asm_labels`），不重复 .equ。

#### ⑬ 重导出 asm/all.s + 校验

```bash
tools/asm-regen/ghidra-export-range.bat 080000c0 084c7637 asm/all.s 0
python tools/asm-regen/inject_modes.py    # 无参 = 原地改 asm/all.s
python tools/asm-regen/split_all_s.py     # all.s → asm/*.s 拆分模块 (见 §七)
rm -f asm/all.s asm/all.s.raw asm/all.s.raw.nomode   # 拆分后中间产物即可删
NOPAUSE=1 ./build.bat                       # bash harness 下必须 NOPAUSE=1
sha1sum roms/2343.gba output/2343.gba       # 必须一致
```

⚠️ 自 2026-06-03 起 `asm/all.s` 不再被 `rom.s` 直接 `.include`，而是经 `split_all_s.py`
拆成 `asm/NN_*.s` 多模块 (rom.s 改 `.include "asm/includes.inc"`)。**Ghidra 再生成后必须
补跑 `split_all_s.py`**，否则 build 用的是旧的拆分文件。`all.s` 及 `.raw`/`.raw.nomode`
都是中间产物，拆分完即可删除（已入库的是 `asm/NN_*.s`）。详见 §七。

导出后 `bl FUN_080db860` 变 `bl pack_banner_tile_copy`，`.word 0x08000240` 变 `.word game_str_id_remap_count`。再次 byte-identical 验证。

详细底层流水线（ExportRangeToGas 输出格式 / inject_modes 规则 / 已知问题）见本文 §二。

#### ⑭ 同步 Ghidra 函数名回 CSV（rename 后必跑）

```bash
# 1. 重导 Ghidra inventory 拿最新函数名
tools/asm-regen/ghidra-run-script.bat ExportFunctionInventory.py
# 2. 单向 Ghidra -> CSV 同步: name 列更新 + proposed/score 清空
python tools/ad-hoc/sync_ghidra_names_to_proposals.py
```

**作用**：把 Ghidra 已 USER_DEFINED 命名的函数名拷回 `doc/dev/naming-proposals.csv` 的 name 列；`proposed_name` + `score` 一律清空（提案已落地为现实，不再是 todo）。幂等可重跑。

**何时漏跑会出问题**：CSV name 列停在 `FUN_xxxxxxxx`，但 Ghidra 已是 `pack_ui_show_all_opened_done` —— 后续基于 CSV name 做分析（如 propagate / cluster）会用旧名，分析结论与 Ghidra 不一致。

#### ⑮ 注释备份导出（可选，每次深入分析后做）

```bash
tools/asm-regen/ghidra-run-script.bat ExportComments.py
```

导出全部 plate / pre / post / eol / repeatable / func_repeatable 注释到 `temp/ghidra-comments.csv`。用途：
- 把 Ghidra 内人工注释从 .rep 二进制工程导成纯文本，纳入 git 跟踪
- 不在 Ghidra 内的 reviewer 也能看到分析成果
- 作为分析备份，避免 .rep 损坏丢失

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
- **equate 符号化**（`apply_equates`，2026-06-03 加）：若某指令操作数在 Ghidra EquateTable 设了 equate，把立即数 `#0x..` 替换为 equate 名（如 `#PSR_IRQ_MODE`）。仅对有 equate 的操作数生效，其余指令零影响 → 全 ROM byte-identical 不受扰。GAS 端靠 `constants/*.inc` 的 `.set`/`.equ` 解析回同值。设 equate 用 `tools/ghidra-labeling/SetBootEquates.py` 式脚本（`EquateTable.createEquate` + `addReference(addr, opIndex)`）。⚠ `ins.toString()` 本身不应用 equate，故必须由本步替换。

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
python tools/asm-regen/split_all_s.py            # 拆成 asm/NN_*.s (见 §七)
rm -f asm/all.s asm/all.s.raw asm/all.s.raw.nomode

# 验证 byte-identical
rm -rf output && mkdir -p output
as.exe -mcpu=arm7tdmi -o output/rom.o asm/rom.s
ld.exe -T ld_script.txt -o output/2343.elf output/rom.o
objcopy.exe -O binary output/2343.elf output/2343.gba
cmp roms/2343.gba output/2343.gba && echo OK
```

---

## 七、asm/*.s 模块拆分

**背景**：`asm/all.s` 是 49.5 万行 / 25 MB 的 Ghidra 单体导出，编辑、git diff、检索都吃力。
4641 函数全部命名完成后（2026-06-03），按子系统拆成 `asm/NN_*.s` 多文件，**入库的是这些
拆分文件**；`asm/all.s` 及其 `.raw`/`.raw.nomode` 全部降级为可删的中间产物。

**核心约束**：
1. 拆分流（all.s）是**生成产物**（§二管线），拆分规则必须能在再生成后重新套用 →
   用 **manifest（以地址为 key）** 驱动，不手切。
2. byte-identical 要求**按地址顺序连续 emit**。`.include` = 纯文本拼接，所以"切在函数
   边界 + 按地址序 include" ⇒ 拼接等价 ⇒ 必然 byte-identical。
3. 因此**每个模块文件只能是一段连续 `[start, next_start)` 地址区间**，不能把散落各处的
   同子系统函数收进一个文件（会打乱地址序）。好在原编译单元本就连续排布，子系统天然成簇。
4. 全 ROM **无 local label**（无 `1:`/`.L`），切分零作用域风险。
5. mode（`.thumb`/`.arm`）状态在同一汇编单元内跨 `.include` 自然延续；split 脚本另在每个
   非首文件开头注入 3 行 header（`@ ==== 名 ====` / `@ 描述` / 当前 mode），零字节，纯为
   可读 + 可独立汇编。

**组件**：
| 文件 | 作用 |
|------|------|
| `tools/asm-regen/split_manifest.tsv` | 边界定义（`start_addr<TAB>filename<TAB>desc`），唯一手维护 |
| `tools/asm-regen/split_all_s.py` | 拆分器：规范流 + manifest → `asm/NN_*.s` + `asm/includes.inc` |
| `tools/asm-regen/generate_split_manifest.py` | 按行数均衡 + 子系统转变吸附，生成 manifest 初稿 |
| `asm/includes.inc` | 自动生成的有序 `.include` 清单，被 `rom.s` 引用 |

**规范流（canonical stream）来源**，`split_all_s.py` 自动按优先级选：
1. `asm/all.s` 存在（Ghidra 再生成 + inject_modes 刚产出）→ 直接用；
2. 否则从已入库的 `asm/NN_*.s` **反向合并**（剥掉注入 header）重建。

⇒ 所以 `asm/all.s` 删除后，阶段 B「改 manifest 重切」仍可工作，**无需保留 all.s**。
需要单体 all.s（如做 Ghidra round-trip / 整体 diff）时：`split_all_s.py --merge asm/all.s`。

**入库策略**：`asm/all.s` / `.raw` / `.raw.nomode` 都 `.gitignore`；git 跟踪 `asm/NN_*.s`
+ `asm/includes.inc`。`rom.s` 用 `.include "asm/includes.inc"`。**build.bat 保持纯汇编**
（直接 as/ld/objcopy 入库的拆分文件，不跑 split）。

**日常构建**：拆分文件已入库，`./build.bat` 直接用，无需任何额外步骤。

**阶段 B 调边界 / 再细分**：只改 `split_manifest.tsv`（增删行、改文件名/边界地址），然后：
```bash
python tools/asm-regen/split_all_s.py --check     # 校验全部边界命中
python tools/asm-regen/split_all_s.py             # 重切 (all.s 缺失时自动反向合并)
NOPAUSE=1 ./build.bat && sha1sum roms/2343.gba output/2343.gba   # 验证 byte-identical
```
风险隔离在 manifest 一处；改完务必 build 验证。

**已验证**：2026-06-03 阶段 A 25 段拆分（含删 all.s 后反向合并往返）byte-identical 通过，
SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`。

---

## 三、深入分析单个函数：标准 Ghidra 写入流程

**适用场景**：分析了一个之前不理解的函数（如 `FUN_080f4e18` → `game_str_id_to_row`），要把语义沉淀到 Ghidra（rename + plate comment + 关联数据 label），并保持 byte-identical。

**用本流程的判定**：函数已读懂用途、入参、返回值、关键数据；不是猜测性命名。猜测性的留 CSV 提案，不写 Ghidra。

### 完整步骤（实战记录: 2026-04-30 game_str_id_to_row 落地）

```bash
# === 0. 备份 ===
TS=$(date +%Y%m%d-%H%M%S)
cp -r "ghidra/Yu-Gi-Oh WCT 2006.rep" \
      "ghidra/Yu-Gi-Oh WCT 2006.rep.bak-${TS}-pre-<funcname>"

# === 1. 加 USER_DEFINED label 给关联数据 ===
# 编辑 tools/ghidra-labeling/LabelDataCrystalRomMap.py 加条目:
#   (0x08000240, "game_str_id_remap_count"),   # u16, count
#   (0x08000250, "game_str_id_remap_table"),   # 1651 × u16 sorted
tools/asm-regen/ghidra-run-script.bat LabelDataCrystalRomMap.py
# 已 exists 的 label 会 [skip], 幂等

# === 2. 函数 rename + plate comment ===
# 编辑 tools/ghidra-labeling/RenameKnownFunctions.py 加条目:
#   ("FUN_080f4e18", "game_str_id_to_row",
#       "二分查找 game_str_id_remap_table @ 0x08000250 ... ")
# ⚠ 中文必须 utf-8: do_rename 已自动 .decode("utf-8")
tools/asm-regen/ghidra-run-script.bat RenameKnownFunctions.py

# === 3. 字面量池符号化三连击 ===
tools/asm-regen/ghidra-run-script.bat AddLiteralPoolReferences.py
# .word 0x08000240 -> .word game_str_id_remap_count (加 DATA ref)
tools/asm-regen/ghidra-run-script.bat ExportRomLabelsToInc.py
# 把 INCBIN 内部 label 写成 .equ 给 GAS 链接器 (asm/*.s 已有 name: 的自动 skip)

# === 4. 重导 asm + 校验 ===
tools/asm-regen/ghidra-export-range.bat 080000c0 084c7637 asm/all.s 0
python tools/asm-regen/inject_modes.py
NOPAUSE=1 ./build.bat
sha1sum roms/2343.gba output/2343.gba
# 必须一致: 9689337d6aac1ce9699ab60aac73fc2cfdccad9b

# === 5. 同步 Ghidra 函数名回 CSV (rename 后必跑) ===
tools/asm-regen/ghidra-run-script.bat ExportFunctionInventory.py
python tools/ad-hoc/sync_ghidra_names_to_proposals.py
# CSV name 列更新为 Ghidra 真名, proposed/score 清空 (proposal 已落地)

# === 6. 注释备份导出 (可选但推荐) ===
tools/asm-regen/ghidra-run-script.bat ExportComments.py
# 输出 temp/ghidra-comments.csv
# git add temp/ghidra-comments.csv  # 如要纳入 git
```

### 失败模式与排查

| 现象 | 根因 | 修复 |
|---|---|---|
| `bl FUN_080f4e18` 在 asm/all.s 中**没**变成新名字 | rename 没生效 / 没 save | 看 RenameKnownFunctions 输出有 `[ok] FUN_xxx -> new_name`；重跑确认 `[miss] (already renamed)` |
| `.word 0x08000240` 没符号化 | 缺 DATA reference | 跑 `AddLiteralPoolReferences.py`，查 dry 输出有该地址 |
| build 报 `undefined reference to game_str_id_remap_table` | label 在 INCBIN 内部，没 .equ | 跑 `ExportRomLabelsToInc.py` 重生 `constants/rom_data.inc`，确认含 `.equ <name>, 0xNNNNNNNN` |
| build 报 `use of r13 is deprecated` | inject_modes 没跑 | 在 `./build.bat` 前加 `python tools/asm-regen/inject_modes.py` |
| sha1 不一致 | 改动外溢 / disasm 边界变化 / inject_modes 补丁失效 | 回滚 .rep 备份，二分定位哪步引入差异 |
| 中文 plate comment 显示 mojibake (`äºåæ¥æ¾`) | 老脚本写入时没 .decode("utf-8") | 跑 `tools/ghidra-labeling/FixCommentEncoding.py` 全工程批量修 |

### 工具职责矩阵

| 工具 | 作用域 | 写入 .rep | 改 asm/all.s | 改其它入库文件 |
|---|---|:---:|:---:|---|
| `LabelDataCrystalRomMap.py` | 加 USER_DEFINED label | ✓ | 间接 (下次 export) | — |
| `RenameKnownFunctions.py` | 函数 rename + plate comment | ✓ | 间接 | — |
| `Annotate*.py`（per-function） | 参数签名 + 行级 EOL/PRE/POST 注释 | ✓ | 间接 | — |
| `AddLiteralPoolReferences.py` | 给 4-byte data 加 DATA ref | ✓ | 间接 (符号化生效) | — |
| `ExportRomLabelsToInc.py` | 扫 USER_DEFINED label → .equ | — | — | `constants/rom_data.inc` |
| `ExportFunctionInventory.py` | 全函数清单导出 | — | — | `temp/ghidra-functions.csv` |
| `sync_ghidra_names_to_proposals.py` | 单向 Ghidra → CSV 名字同步 | — | — | `doc/dev/naming-proposals.csv` |
| `ExportRangeToGas.py`（包装在 `ghidra-export-range.bat`）| 反汇编 → asm/all.s | — | ✓ 全文重写 | — |
| `inject_modes.py` | mode 切换 + s 后缀 + 硬补丁 | — | ✓ 原地改 | — |
| `ExportComments.py` | 导出所有注释 | — | — | `temp/ghidra-comments.csv` |
| `FixCommentEncoding.py` | 修历史 mojibake 注释 | ✓ | 间接 | — |
| `build.bat` | as → ld → objcopy | — | — | `output/2343.gba` |

### 何时 *不* 用此流程

- **猜测性命名**：函数大致用途清楚但不确定细节 → 写 `doc/dev/naming-proposals.csv`（5 列 schema），等证据更强再 apply 到 Ghidra
- **跨多函数批量分析**：用 `tools/ghidra-labeling/ApplyNamingProposals.py`（只 apply score=5）
- **数据 label 不属任何模块**：可以只标 label 不命名，留 `DAT_xxx` 自动名

---

## 四、可复用 checklist

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
- [ ] **备份 .rep**（写入前必做：`cp -r ghidra/*.rep ghidra/*.rep.bak-<ts>-pre-<task>`）
- [ ] Ghidra 函数重命名（追加 `RenameKnownFunctions.py`，中文注释 `.decode("utf-8")`）
- [ ] Ghidra 数据 label（`LabelDataCrystalRomMap.py` 或新建 `Label<模块>.py`）
- [ ] （深入分析）参数签名 + 行级注释：写 `Annotate<Module>.py`
- [ ] 加新 label 后三连击：`AddLiteralPoolReferences.py` + `ExportRomLabelsToInc.py`
- [ ] 重导出 `asm/all.s` + `inject_modes.py` + `NOPAUSE=1 ./build.bat`
- [ ] sha1sum byte-identical 校验
- [ ] **同步 Ghidra 名字回 CSV**：`ExportFunctionInventory.py` + `sync_ghidra_names_to_proposals.py`
- [ ] （可选）`ExportComments.py` 导出注释纳入 git

**Phase 4 文档**：
- [ ] Spec 写入 `doc/dev/data-structure/<名>.md`
- [ ] Narrative 写入 `doc/analysis/<名>-location.md`
- [ ] 函数名登记表 (`ghidra-function-names.md`) 追加
- [ ] README + data-analysis-coverage.md 更新

---

## 五、产出清单模板

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

## 六、相关文档

| 文件 | 关系 |
|------|------|
| [`asset-location.md`](asset-location.md) | Phase 1 定位方法论（动态 + 静态路径） |
| [`../tools/gdb-debugging.md`](../tools/gdb-debugging.md) | GDB batch 脚本、断点矩阵、12 个坑 |
| [`../tools/mgba-mcp.md`](../tools/mgba-mcp.md) | mGBA MCP 15 个工具 + Lua 教程 |
| `doc/dev/ghidra-function-names.md` | Ghidra 重命名登记表（Phase 3 产出） |
| `data-analysis-coverage.md` | ROM 分析覆盖率总览（每次结构化后更新） |
