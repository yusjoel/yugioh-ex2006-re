# asm/all.s 重新生成工作流

日期：2026-04-14  
验证状态：✅ 端到端 byte-identical 通过（SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`）

本文档描述如何从 Ghidra 数据库重新导出并加工出可汇编的 `asm/all.s`，并保证 `build.bat` 产物与原始 ROM 逐字节一致。

---

## 流水线总览

```
Ghidra 数据库 (ghidra/Yu-Gi-Oh WCT 2006.gpr)
        │
        │  tools/asm-regen/ghidra-export-range.bat     （调 analyzeHeadless）
        │  tools/asm-regen/ghidra/ExportRangeToGas.py  （Jython，Ghidra 内执行）
        ▼
doc/temp/all.s.raw                 （约 20.5 MB，含 14088 行 .arm/.thumb）
        │
        │  grep -v '^\.(thumb|arm)\s*$'     （剥掉 Jython 的 mode 指令）
        ▼
doc/temp/all.s.raw.nomode
        │
        │  python tools/asm-regen/inject_modes.py <in> <out>
        │     - 注入 3 处 .arm/.thumb 切换（依据 hex 宽度和 BL/BLX 模式）
        │     - 补全 141015 处 Thumb 设标志指令的 s 后缀
        │     - 应用 2 处手动补丁
        ▼
doc/temp/all.s.v2  ──替换──►  asm/all.s
        │
        │  build.bat  (as → ld → objcopy)
        ▼
output/2343.gba   ✓ byte-identical
```

导出范围：`0x080000c0 – 0x08ffffff`（16 MB，跳过 ROM 头；ROM 头由 `asm/rom_header.s` 和 `asm/crt0.s` 维护）。

---

## 各脚本职责

### 1. `tools/asm-regen/ghidra-export-range.bat`

Windows 批处理包装，调用 Ghidra `support/analyzeHeadless.bat` 以无 GUI 方式执行 Jython 脚本。

**参数**：`<start_hex> <end_hex> <output_path> [xrefs 0|1]`

**读取**：
- `GHIDRA_HOME` 环境变量（Ghidra 安装根目录，见 `LOCAL.md`）
- 项目 `ghidra/Yu-Gi-Oh WCT 2006.gpr`（`.gitignore` 忽略）
- 处理目标 `2343.gba`（项目内已导入）

**固定参数**：`-noanalysis -readOnly`（不触发分析、只读打开，避免污染项目）

---

### 2. `tools/asm-regen/ghidra/ExportRangeToGas.py`（Jython）

出处：Ghidra 安装目录 `Ghidra/Features/GBA/ghidra_scripts/ExportRangeToGasS_Jython.py`（2026-03-09 版）  
本仓库副本额外加了 headless 参数支持（`getScriptArgs()` 分支）。

**职责**：遍历指定地址范围，按 listing 输出 GAS 风格 `.s`：

- **指令行**：`<mnemonic operands>  @ <address> <hex>`  
  同时做几项 GAS 语法修正（见下）。
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

**输出 `.arm` / `.thumb` 切换**：  
Jython 版试图"每条指令判定 Thumb/ARM，发生变化就输出 mode 指令"。判定顺序：
1. 地址对齐（`addr % 4 != 0` ⇒ Thumb）
2. `ProgramContext` 的 `TMode` / `ISAMode` 寄存器
3. 指令长度 == 2 ⇒ Thumb
4. 默认 ARM

#### ⚠️ 缺陷：自动 mode 切换不可用

实测 Jython 的 mode 切换结果汇编失败（5 处 `misaligned branch destination`），因此**必须在下游剥掉**。保留指令是因为 GUI 场景下它仍然是有用的提示；headless 流水线里由 `inject_modes.py` 重新注入。

根因推测：Ghidra 数据库中部分区段的 `TMode` 未被正确设置，或判定顺序在某些边界情况下给出错误答案。调试成本高，绕开更划算。

#### Headless 接口

- GUI 模式：走 `ask*` 交互（XREFS 开关、起止地址、输出文件、是否导出 structs）
- Headless 模式：通过 `getScriptArgs()` 读 `<start> <end> <out> [xrefs]` 四个位置参数，跳过所有 `ask*`

---

### 3. `tools/asm-regen/inject_modes.py`

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
| ~~`adr r10,0x810e204`~~ | ~~`sub r10,pc,#4`~~ | **已被 Jython 自动处理**（合成 `DAT__0810e204` 标签），该补丁可移除 |
| `adds r4,r4,#0x4  @ 0809fb20 241d` | `.hword 0x1d24` | Ghidra 输出 3-operand 形式，GAS 会编码成 2-operand，字节不一致；直接按原字节写死 |
| `bx r11  @ 087e0bc4 5e47` | `.hword 0x475e` | 原始编译器产生的 `bx r11` 编码未清零 SBZ 位（`5e47`），GAS 正确编码为 `5847`，byte 不一致；按原字节写死 |

这 3 条都是"无法通过汇编规则重现原始字节"的**编译器历史产物**，必须硬写。

---

## Diff 演进（验证过程记录）

| 阶段 | 脚本组合 | 与 `asm/all.s` diff 行数 |
|---|---|---:|
| 初版 v6（旧） | `ExportRangeToGas v6` + `inject_modes` | 194,180 |
| 换 Jython 版 | `ExportRangeToGas`(Jython) + `inject_modes` | 28,181 |
| 剥 mode 指令 | Jython + `grep -v` + `inject_modes` | 5（1 处真实差异） |
| 最终 | 同上（确认可 byte-identical 构建） | 1 处可接受差异 |

**最终唯一差异**（与现有 `asm/all.s` 相比）：

```diff
-    adr r10, DAT__0810e204                   @ 0810e200 04a04fe2
-DAT__0810e204:
+    sub r10,pc,#4   @                        @ 0810e200 04a04fe2
```

两种写法 GAS 都汇编成相同字节 `04a04fe2`。新方式（Jython 的 DAT_ 合成）更通用，旧方式是 `inject_modes.py` 的手动补丁遗留。

---

## 已知仍未解决的问题

1. **Jython 的 `.arm`/`.thumb` 自动输出不可用**：5 处错位导致 `misaligned branch destination`。当前绕开方案是下游 `grep -v` 剥掉。若未来有人用 Ghidra GUI 直接导出 `.s` 并尝试汇编，会踩这个坑。
2. **`inject_modes.py` 的两处 hword 补丁是硬编码字节**：`0x1d24` 和 `0x475e` 绑定具体地址（`0809fb20`、`087e0bc4`）。如果 Ghidra 重新分析后这些地址的指令形式变了，补丁会匹配失败。
3. **141015 处 `s` 后缀是大规模字符串改写**：规则覆盖绝大多数情况，但遇到新指令模式可能遗漏，需要通过汇编报错反馈。
4. **`sub r10,pc,#4` 补丁已过时**：Jython 合成了 `DAT__0810e204` 标签，原 `adr r10,0x810e204` 字串已不存在，该补丁永远不会触发。可以清理。

---

## 参考命令

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

完整流水线耗时：Ghidra headless 导出约 90 秒，`inject_modes.py` 约 20 秒，build 约 5 秒。
