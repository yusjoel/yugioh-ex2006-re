---
name: analyze-function
description: Use this skill when the user asks to analyze a specific function in the GBA ROM disassembly, e.g. "分析FUN_080d6290", "分析 0x080d6290", "analyze FUN_xxxxxxxx", "深入分析 FUN_xxxxxxxx". Performs static analysis on the function in asm/all.s, proposes a name + plate comment + parameter signature + line-level annotations + related data labels, then walks the full Ghidra write-back pipeline (rename, label, refs, comments, asm regen, byte-identical verify, CSV sync). Skip for casual mentions or when only naming needed without deep analysis.
---

# 分析单函数 + 写入 Ghidra 标准流程

把对一个 `FUN_xxxxxxxx` 的深入分析沉淀到 Ghidra 工程，并保持 ROM byte-identical。完整覆盖 `doc/dev/methodology/build-pipeline.md` §三。

## 触发示例

- `分析FUN_080d6290`
- `分析 0x080dd53c`
- `analyze FUN_080f4e18`
- `深入分析 FUN_xxxxxxxx`

## 启动检查（每次必做）

1. 解析参数：从用户输入提取 `FUN_xxxxxxxx` 或 `0xXXXXXXXX` 形式的 8 位 hex 地址（小写）。
2. 验证地址在 ROM 主代码段：`0x080000c0 ≤ addr ≤ 0x084c7637`。否则停下问用户。
3. 在 `asm/all.s` 内 grep `^FUN_<addr>:` 或 `^<funcname>:` 确认存在。

---

## 阶段 A：分析（不写任何东西）

### A1. 读函数体

```bash
LINE=$(grep -n "^FUN_<addr>:\|^<known_name>:" asm/all.s | head -1 | cut -d: -f1)
sed -n "$((LINE-3)),$((LINE+80))p" asm/all.s
```

包含：函数 label / 完整指令 / 紧随的 literal pool（DAT_/PTR_）。

### A2. 提取关键信息

按以下要点逐个落实：

- **入参**：r0/r1/r2/r3 在函数早期被 `push` 保存还是直接用？识别参数语义（id / 指针 / flag / size）。
- **literal pool**：每个 `DAT_xxx: .word 0xNNNNNNNN`、`PTR_xxx_xxxxxxxx: .word <symbol>`。值是地址要分类：
  - `0x08000XXX..0x084C7637` → ROM code/data 指针
  - `0x09000000..0x09FFFFFF` → ROM data 指针（卡数据/字符串/调色板等）
  - `0x02000000..0x0203FFFF` → EWRAM
  - `0x03000000..0x03007FFF` → IWRAM
  - `0x04000000..0x040003FF` → IO MMIO
  - `0x05000000..0x07000400` → PALRAM/VRAM/OAM
  - 小整数 (< 0x10000) → 可能是 logical id / size / flag / coord
- **callees**：每个 `bl <target>`。已命名的（如 `bl game_str_id_to_row`）说明调用链已知；`bl FUN_xxx` 不要立刻标 `(TODO)`，先做下面的 callee tag 反推。
- **callee tag 反推**（重要：能在不深入 callee 函数体的情况下得到粗略业务方向）：

  对每个 `bl FUN_xxx` 的 callee，去 `doc/dev/naming-proposals.csv` 查 `(proposed_name, score, tags)` 四元组：

  ```bash
  for addr in <callee1> <callee2> <callee3> ...; do
    grep "^0x$addr," doc/dev/naming-proposals.csv
  done
  ```

  解读约定：
  - **proposed_name**（如 `hud_080cc904` / `game_str_080cbf0c` 带 module 前缀的占位名）→ callee 已被某个方法（label refs / FID / 状态表 / 字符串锚）锚定到具体模块。score=5 强证据 / 4-3 中证据 / 2 弱启发。
  - **tags** 单 module token → 业务专属；多 module → 跨模块 helper / dispatcher（4+ 个 module 几乎没业务信息）。
  - **IO family tag**（`vram` / `bg` / `palette` / `display` / `blend` / `window` / `sprite` / `dma` / `sio` / `timer`）是横切信号，看业务 module 才是关键。
  - **frame_counter / prng / settings** 几乎到处出现，弱信号。

  **叠加多个 callee 的 tag → 当前函数的业务推断**。例：6-state 顺序调度器，sub-handler tag 分别是 `frame_counter`(sync) / `bg;palette` / `fs` / `demo;fs` / `hud;duel_field;game_str` / `frame_counter`(sync) → 这是一个**决斗场景加载序列**（同步等待 → BG/调色板 → 资源加载 → 动画 → HUD/文本渲染 → 同步收尾）。

  caveat：
  - tag 是 `propagate_label_tags.py` 沿 callgraph 扩散来的，sync/util helper 容易被沾上调用方的 module tag → 单一 callee 的单一 tag 容易误导。
  - **多个 callee 的 tag 一致性高才是可信信号**。一个 sub-handler 的弱 tag 不要单独采信，要看整体 pattern。
  - score 列空白但 tags 非空：仅是 propagate 的扩散结果，比 score=2 还弱。

- **callers**：`grep -n "bl FUN_<addr>" asm/all.s | wc -l` 看调用频率，`head` 看几个 caller 的地址。
- **state writes**：`strh/strb/str rN, [rM, #imm]` 写到 EWRAM/IWRAM 地址 → 全局状态机变量。
- **返回值**：函数末尾 `movs r0, #N; pop {pc}` 模式 → 返回值。

### A3. 输出分析报告（给 user 看）

报告格式（控制台输出）：

```
## FUN_<addr> 功能分析

**反汇编**（asm/all.s:<line>+）：
<关键代码段, 多行带注释解释>

**语义**：
| 阶段 | 动作 |
|---|---|
| 1 | <step 1 说明> |
| 2 | <step 2 说明> |
...

**触发场景**：<什么时候被调用>

**建议命名**：
- `FUN_<addr>` → **`<proposed_name>`**（命名理由）
- 数据 label：`<addr>` → **`<label_name>`**（如有）
- 参数（如有特定 calling convention）：`<func>(arg1: type1, arg2: type2, ...)`

要写入 Ghidra 吗？或先验证 caller 行为再批量命名？
```

**关键：在 user 确认前不写任何东西。** user 可能会调整命名 / 否决整体或者要补充验证。

---

## 阶段 B：user 确认后写入

### B0. 备份 .rep（必做，先备份再写）

```bash
TS=$(date +%Y%m%d-%H%M%S)
cp -r "ghidra/Yu-Gi-Oh WCT 2006.rep" "ghidra/Yu-Gi-Oh WCT 2006.rep.bak-${TS}-pre-<funcname>"
```

`<funcname>` 用本次新命名（如 `pack-ui-dialog`、`game-str-id-to-row`），简短 kebab-case。

### B1. 编辑中央 Ghidra 脚本（添加条目，不重写）

#### B1a. `tools/ghidra-labeling/RenameKnownFunctions.py`

在 `RENAMES = [...]` 列表末尾追加：

```python
("FUN_<addr>", "<proposed_name>",
    "<plate comment - 简明扼要的功能 / 入参 / 关键数据 / 返回值>"),
```

中文注释直接写（`do_rename` 自动 `.decode("utf-8")` 转 unicode 进 Java API）。

#### B1b. `tools/ghidra-labeling/LabelDataCrystalRomMap.py`（如有新数据 label）

在合适的段（按地址区域 ROM/EWRAM/IWRAM）追加：

```python
(0x<addr>, "<label_name>"),  # <说明>
```

如果是 IWRAM/EWRAM label，**还需手工**在 `constants/iwram.inc` 或 `constants/ewram.inc` 加一行 `.equ`：

```
.equ <label_name>,    0x<addr>  @ <说明>
```

（IWRAM/EWRAM label 不归 ROM 段的 rom_data.inc 管，需要手工同步）

### B2. 写专属 Annotate 脚本（参数签名 + 行级注释）

文件：`tools/ghidra-labeling/Annotate<Module>.py`

每个深入分析的函数（或一组相关函数）一个脚本。模板见 `AnnotatePackUIDialog.py`（实战范例）。

**两类内容**：

**(1) 参数签名**（仅当函数对外接口已定型）：

```python
from ghidra.program.model.listing import ParameterImpl, Function
from ghidra.program.model.data import (
    UnsignedIntegerDataType, PointerDataType, CharDataType
)
from ghidra.program.model.symbol import SourceType

func = getFunctionAt(toAddr(0x<addr>))
uint_dt = UnsignedIntegerDataType.dataType
char_ptr = PointerDataType(CharDataType.dataType)

params = [
    ParameterImpl("<param1_name>", uint_dt, currentProgram, SourceType.USER_DEFINED),
    ParameterImpl("<param2_name>", char_ptr, currentProgram, SourceType.USER_DEFINED),
    ...
]
func.replaceParameters(
    Function.FunctionUpdateType.DYNAMIC_STORAGE_FORMAL_PARAMS,
    True, SourceType.USER_DEFINED, *params)
```

**(2) 行级 EOL 注释**（关键指令，不每条都注释）：

```python
def u(s):
    if isinstance(s, str): return s.decode("utf-8")
    return s

EOL_COMMENTS = [
    (0x<addr+offset>, "r0 = <语义>"),
    (0x<addr+offset>, "<callee_name>(<param 描述>)"),
    (0x<addr+offset>, "<state>[+0xN] = <value> (含义)"),
    (0x<addr+offset>, "return <value> (含义)"),
]

listing = currentProgram.getListing()
from ghidra.program.model.listing import CodeUnit
for addr, txt in EOL_COMMENTS:
    cu = listing.getCodeUnitAt(toAddr(addr))
    if cu: cu.setComment(CodeUnit.EOL_COMMENT, u(txt))
```

**注释选址原则**：
- 入口 / 出口 / 参数加载 / 关键 callee 调用 / 状态切换 / 返回值
- **不要**注释 game_str lookup chain 内部 12 条 ldr/lsl/add（写一条 marker 标记进入即可）
- 中文 + 简短，每行 < 80 字符

### B3. 跑写入 Ghidra 的脚本链（按顺序）

```bash
# 1. 加 USER_DEFINED label (如有 B1b 改动)
tools/asm-regen/ghidra-run-script.bat LabelDataCrystalRomMap.py

# 2. 函数 rename + plate comment
tools/asm-regen/ghidra-run-script.bat RenameKnownFunctions.py

# 3. 参数 + 行注释
tools/asm-regen/ghidra-run-script.bat Annotate<Module>.py

# 4. 字面量池符号化三连击
tools/asm-regen/ghidra-run-script.bat AddLiteralPoolReferences.py
tools/asm-regen/ghidra-run-script.bat ExportRomLabelsToInc.py
```

每步看输出确认有 `[ok] FUN_xxx -> new_name` / `[ok] <label> @ <addr>` / `refs added: N`。

### B4. 重导 asm + build + sha1 校验

```bash
tools/asm-regen/ghidra-export-range.bat 080000c0 084c7637 asm/all.s 0
python tools/asm-regen/inject_modes.py
NOPAUSE=1 ./build.bat
sha1sum roms/2343.gba output/2343.gba
```

**必须 SHA1 一致**：`9689337d6aac1ce9699ab60aac73fc2cfdccad9b`。不一致就回滚 .rep 备份，二分定位。

#### B4 失败排查

| 现象 | 根因 | 修复 |
|---|---|---|
| `bl FUN_<addr>` 在 asm/all.s 没变成新名 | rename 没生效 | 看 RenameKnownFunctions 输出 `[ok]` |
| `.word 0x<addr>` 没符号化为 label | 缺 DATA reference | 跑 AddLiteralPoolReferences 看是否覆盖 |
| build 报 `undefined reference to <label>` | INCBIN 内部 label 没 .equ | 跑 ExportRomLabelsToInc 重生 rom_data.inc; IWRAM/EWRAM label 还要手工加 iwram.inc/ewram.inc |
| build 报 `cannot honor width suffix` | inject_modes 没补 s 后缀 | 检查行末是否被 EOL 注释打断 inject_modes regex |
| sha1 不一致 | 改动外溢 | 回滚 .rep 备份，二分定位 |

### B5. Ghidra 名字同步回 CSV（必跑）

```bash
tools/asm-regen/ghidra-run-script.bat ExportFunctionInventory.py
python tools/ad-hoc/sync_ghidra_names_to_proposals.py
```

把 Ghidra 真名拷回 `doc/dev/naming-proposals.csv` 的 name 列，proposed/score 一律清空。

### B6. 注释备份导出（推荐）

```bash
tools/asm-regen/ghidra-run-script.bat ExportComments.py
```

输出 `temp/ghidra-comments.csv`（plate / pre / post / eol / func_repeatable 全部）。

---

## 阶段 C：完成报告 + commit 提议

向 user 报告：

```
## 完成

**Ghidra 改动**（byte-identical SHA1 ✓）：
- 函数 rename: FUN_<addr> -> <proposed_name>
- plate comment: <一句话语义>
- 参数签名: <func>(arg1: type1, ...)  (如有)
- 行级 EOL 注释: N 条覆盖关键指令
- 数据 label: <addr> -> <label_name>  (如有)

**文件改动**：
- ghidra/<rep>.bak-<ts>-pre-<task>     (新)
- tools/ghidra-labeling/RenameKnownFunctions.py     (+1 entry)
- tools/ghidra-labeling/LabelDataCrystalRomMap.py   (+N entries)  (如有)
- tools/ghidra-labeling/Annotate<Module>.py         (新)
- constants/iwram.inc 或 ewram.inc                   (+N .equ)  (如有 IWRAM/EWRAM)
- asm/all.s                                          (重生)
- constants/rom_data.inc                             (重生, 可能没动)
- doc/dev/naming-proposals.csv                       (sync, name 列更新)
- temp/ghidra-comments.csv                           (注释备份)

要 git commit 吗？(按 CLAUDE.md 我不主动 commit)
```

---

## 关键约束（CLAUDE.md）

- **byte-identical 是硬门槛** —— sha1 不一致就回滚
- **mojibake** —— Ghidra 写中文必须 `.decode("utf-8")` 转 unicode
- **Don't auto-commit** —— `git add` OK，但必须 user 明确要求才 `git commit`
- **NOPAUSE=1** —— bash harness 下 build 必须设
- **inject_modes 必跑** —— GAS 不接受 raw Ghidra 反汇编
- **scope 围栏** —— 本流程只动当前分析的函数，不顺手做其它

## 何时**不**用此 skill

- **猜测性命名**：函数大致用途清楚但细节不确定 → 写 `naming-proposals.csv` 提案，不写 Ghidra
- **批量 FID match**：用 `tools/ghidra-labeling/ApplyNamingProposals.py` 走 score=5 通道
- **数据 label 不属任何模块**：只标 label 不命名，留 `DAT_xxx` 自动名

## 工具职责矩阵速查

| 工具 | 作用 | 写 .rep | 改 asm/all.s | 改其它 |
|---|---|:---:|:---:|---|
| LabelDataCrystalRomMap.py | USER_DEFINED label | ✓ | 间接 | — |
| RenameKnownFunctions.py | 函数 rename + plate | ✓ | 间接 | — |
| Annotate<Module>.py | 参数签名 + 行级 EOL | ✓ | 间接 | — |
| AddLiteralPoolReferences.py | 字面量池 DATA ref | ✓ | 间接 | — |
| ExportRomLabelsToInc.py | label → .equ | — | — | constants/rom_data.inc |
| ghidra-export-range.bat (ExportRangeToGas.py) | 反汇编导出 | — | ✓ 全文 | — |
| inject_modes.py | mode + s 后缀补 | — | ✓ 原地 | — |
| ExportFunctionInventory.py | 函数清单 | — | — | temp/ghidra-functions.csv |
| sync_ghidra_names_to_proposals.py | Ghidra → CSV name | — | — | doc/dev/naming-proposals.csv |
| ExportComments.py | 注释导出 | — | — | temp/ghidra-comments.csv |
| build.bat | 汇编链接 | — | — | output/2343.gba |
