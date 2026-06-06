# 方法论：地址序逐段细化循环 (refine-loop)

> 用途：在**已 100% 命名**的基础上，对一个反汇编模块文件 (`asm/NN_*.s`) 做**内部细化**——
> 立即数符号化 / 消灭自动名 label / 误标数据反汇编 / 函数间数据 carve / 注释订正，
> 全程保持 **byte-identical**。与 [`analysis-loop.md`](analysis-loop.md) (命名) 互补：命名给函数起名，
> 细化把函数**体内**与**函数之间**的一切打磨到可读、无 `DAT_`/`ROM_INCBIN` 残留。
> 单函数零散细化见 [`symbolization.md`](symbolization.md)；本文讲如何把整个文件包装成可跨会话运行的逐段 loop。

---

## 何时用

- 一个文件已全部命名，要系统性消灭 `DAT_/DWORD_/UNK_/PTR_DAT_` 自动名 + `ROM_INCBIN`/`.byte` 未分化块。
- 跨会话推进，需地址序进度跟踪 + 逐段 commit。
- 实战范例：`doc/dev/p5-refine-00-system-str-vija.md` (00_system_str_vija.s 全程记录)。

---

## 三条硬规则 (用户定, 2026-06-06)

1. **严格地址序**。整个代码区按地址均分 **~10 段 (Seg-1..Seg-10)**，每段 ~28 fn，
   **段边界 = 某函数结束处**（绝不切断函数）。按 Seg 序号执行，段内低→高，**不回头不跳号**。
   — 旧"子系统聚类"方式 (跳地址) 已废弃。
2. **函数间数据也要细化**。段内出现的 `ROM_INCBIN <off>, <size>` / `.byte` 未分化块**不允许保留**：
   - **被引用的代码** → R4 反汇编 (disasm)；
   - **被引用的数据** → R7 carve 进 `rom.s` (label + 结构化 `.byte`/`.word`/`.asciz`)。
3. **唯一例外**：该块**全 ROM 无任何引用** (ref-scan 见下) → 允许暂不处理，登记进活动 refine 文档的
   **§5.1 未引用数据登记表** (注地址/大小/所在 Seg/初判内容)，引用到时再处理。

---

## R1-R9 细化清单 (每函数 / 每数据块逐项过)

| | 项 | 要点 |
|--|----|------|
| R1 | 常量符号化 | 立即数已知常量 → Ghidra **data-equate** (`EquateTable.createEquate`+`addReference`)，GAS 端靠 `constants/*.inc` 的 `.equ` 解析回同值。**先查现有 inc 复用** (gSettings/OBJ_PALRAM_BASE/FourCC tag…)，勿重复造。 |
| R2 | 标签可读化 | `DAT_/LAB_/DWORD_/UNK_/PTR_DAT_` → `^[a-z][a-z0-9_]+$` 语义名。槽用 `<func>_<role>`；多个同类用后缀 (`_assert_line_<hexlineno>` 避碰撞)。RAM/IO 全局加 USER label + 写 `constants/*.inc` `.equ`。 |
| R3 | 符号被「按名引用」 | 仅在 .inc 定义不够：Ghidra 给目标地址加 USER label + 给字面量池 `.word` 加 **DATA ref**，`resolve_word_symbol` 才导出 `.word <name>`。验证：`grep <name>` 同时命中定义+引用。 |
| R4 | 误标数据反汇编 | Ghidra 错标成 `ROM_INCBIN`/`.byte` 的**代码** → disasm + 必要时 createFunction (见下「R4 技法」)。 |
| R5 | 注释订正 | plate/EOL 用**现名**：过时 `FUN_/DAT_/DWORD_` 引用改现名；错误描述改正 (误名是细化最常发现的系统性问题)。零容忍词 (似乎/可能/大概) 禁用，给 file:line + 置信度。 |
| R6 | 先读消费者再命名 | 命名数据/参数前先读**使用它的代码**搞清格式语义，不靠猜。 |
| R7 | 数据区结构化 carve | 裸 `ROM_INCBIN` 按类型抽成可读 `rom.s` 结构 (见下「carve 技法」)。 |
| R8 | 目视核对 (图形) | 图形提取后渲 PNG 确认；无法静态确认调色板/消费者 → 诚实标注 + 走 mGBA 动态路径，不臆造。 |
| R9 | 红线 byte-identical + 备份 | 每步 build 验 `SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b`；Ghidra 写入前必备份 `.rep`；失败回滚 + 二分。 |

---

## 段划分 (一次性, 每文件)

按 push-prologue 检测函数入口，地址序均分 ~10 段，边界落在函数起点：

```python
# 抽函数入口 (label 行 + 下一行 push + @地址) + ROM_INCBIN 列表, 均分 N=10
# 见 p5-refine doc §五 表: Seg | 地址范围 | ~fn | 内含 ROM_INCBIN | 旧覆盖 | 剩余工作
```

产出写入活动 refine 文档的 **§五 路线图表** (每段地址范围 + 该段内 `ROM_INCBIN` 列表 + 状态)。

---

## 每段工作流 (Seg-N)

```
0. 备份 .rep → .rep.bak-<ts>-pre-seg<N>
1. 测绘段: 扫该段 [start,end) 内 (a) 残留自动名 label (b) ROM_INCBIN/.byte 块 (c) 函数入口
2. 数据块分类 (对每个 incbin/.byte, 见「分类决策树」)
3. 读函数体: 理解 pool 槽语义 (R6); 误名信号 = 函数体操作的全局与函数名矛盾
4. 写 Ghidra 脚本 RefineSeg<N>*.py: equate / carve-label-ref / 槽改名 / plate (+ rom.s carve / disasm 脚本)
5. dry-run 校验 (DRY=True, 全 patterns/values 命中 0 FAIL) → 实跑
6. 重导出: ghidra-export-range.bat 080000c0 084c7637 → inject_modes → split_all_s → build → SHA1 校验
7. (改了函数名) ExportFunctionInventory + sync_ghidra_names_to_proposals + 手改 naming-proposals.csv 那行
8. 更新活动 refine 文档: §四 完成记录 + §三 进度表 + §5.1 登记 (如有) + §五 标 ✅
9. commit (用户指令后; 段内可多次 commit, 地址序不回头)
10. 更新 MEMORY 续接指针 (下一段)
```

段大时可拆 Seg-Na/Nb/... 子段 (地址序仍连续)。已被旧批次细化干净的函数 → 跳过, 只补 gap + carve + 清残留。

---

## 数据块分类决策树 (Rule 2/3 落地)

```
遇 ROM_INCBIN <off>,<sz>  或  .byte 块
  │
  ├─ ref-scan: 全 ROM 搜 raw 值 (addr) 与 THUMB 值 (addr|1) 的小端 .word
  │    python: d.count(struct.pack("<I", addr))  对 addr 与 addr|1, 以及块内各候选入口
  │
  ├─ 有引用 + 内容是代码 (THUMB opcode 形态)  → R4 disasm (见下)
  ├─ 有引用 + 内容是数据 (指针表/字符串/掩码) → R7 carve (见下)
  └─ 0 引用 (raw+THUMB+1 均空, 排除压缩资产里的偶合值) → §5.1 登记, 留待
```

> 孤儿 dead-code 常见来源：编译器对同一函数的**另一翻译变体** (如 jump-table 版 vs cmp/beq 版同时存在)，
> 一个 live 一个 0 引用。登记时注明"与 named `<fn>` 功能重叠的编译变体 dead code"。

---

## carve 技法 (R7)

把 `rom.s` 的 `.incbin "roms/2343.gba", <off>, <sz>` 切成 label + 结构化：

- **切割**：缩短 incbin 到目标块前 (`<off>, <sz-cut>`)，加 `<label>:` + 结构化指令，剩余 incbin 续接。
- **指针表 (THUMB 函数指针)**：ROM 存 `addr|1`，故 carve 必用 `.word <fn> + 1` (否则 GAS 输出偶地址 → 字节失配)。
- **字符串/魔数**：`.asciz "..."` 或 `.ascii "x\0\0\0"` (含对齐填充)。
- **代码侧接通 (R3)**：Ghidra 给 carve 目标地址加 USER label (= carve 的 GAS label 名) + 字面量池槽加 DATA ref
  → `resolve_word_symbol` 导出 `.word <carve_label>`，GAS 解析回同址 → byte-identical。
- **当场 carve, 不留待办** (用户标准)；同前缀串靠地址尾号后缀避碰撞 (`assert_expr_zero_65c`)。

---

## R4 反汇编技法

```python
from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.address import AddressSet
from java.math import BigInteger
# 1) clearListing(lo, hi)            ← 重跑时必须先清, 否则 setTMode ContextChangeException
# 2) ctx.setValue(ctx.getRegister("TMode"), lo, hi, BigInteger.ONE)   ← THUMB=1 / ARM=0
# 3) DisassembleCommand(lo, AddressSet(lo, hi), True).applyTo(currentProgram)
# 4) (函数才) createFunction(lo, None)
```

- **跳转表目标块**：单次 `DisassembleCommand(整 range)` 只 disasm 首 stub (flow 在首个 `b`/`bx` 处离开 range)，
  其余 stub 是跳转表目标非 fall-through → 须**逐目标 per-stub** `DisassembleCommand(addr, [addr,addr+len], thumb)`。
- 字节不变 → byte-identical 必然保持 (disasm 只改 listing 表示)。

---

## 符号化技法 (R1/R2/R3)

- **数值常量** (掩码/控制字/FourCC)：`EquateTable.createEquate(name,val)` + `eq.addReference(slot,0)` + 槽改名。
  GAS 端 `constants/<topic>.inc` 写 `.equ name, val` (复用现有文件优先, 否则新建并 `.include` 进 rom.s)。
- **RAM/ROM 全局** (地址)：`createLabel(target, name, USER)` + `addMemoryReference(slot, target, DATA)` + setPrimary
  + 槽改名。GAS 端 `constants/{ewram,iwram,gba_mem}.inc` 写 `.equ name, addr`。
- **base+offset 形态** (如 `gSettings = 0x02000000 + 0x6c2c`)：两槽无法合成单 `.word`，做 R2 槽改名
  (`_ewram_base` / `_<global>_offset`) + EOL 注明 = `<global> - base`。
- **per-slot 安全**：equate/ref 只作用于该槽，同值字面量在别处不受影响 → 跨段安全。

---

## 红线 / 踩坑 (零容忍)

1. **byte-identical** = 唯一红线。build SHA1 != 9689337d → 立即 abort + 回滚 `.rep`。
2. **Ghidra Jython 设的 EOL/plate 一律纯 ASCII**。含 CJK (`。、（）此值…`) → Jython 双重 UTF-8 编码 mojibake
   (memory `feedback_jython_unicode_plate_comment.md`)。中文解释一律走 `doc/dev/`，不进 Ghidra 注释。
3. **DRY-run 先行**：脚本先 `dry` 跑，确认 equate value `_check` 全过、plate pattern 全命中、0 FAIL，再实跑。
4. **改函数名才需 CSV sync** (ExportFunctionInventory + sync + 手改 naming-proposals.csv)；纯数据/标签/注释改动不需要。
5. **assert-carve 同前缀串**：靠地址尾号后缀去碰撞；改动后必 build 复验 (`_verify_carve` 不覆盖 .word 符号解析)。

---

## 关键路径

| 文件 | 用途 |
|------|------|
| `doc/dev/p5-refine-<file>.md` | 活动 refine 文档：§一 R1-R9 / §二 pipeline / §三 进度表 / §四 逐段记录 / §五 Seg 路线图 / §5.1 未引用登记 |
| `tools/asm-regen/ghidra-run-script.bat` | 跑 Ghidra Jython 脚本 (headless) |
| `tools/asm-regen/ghidra-export-range.bat 080000c0 084c7637` | 重导出 asm/all.s |
| `tools/asm-regen/{inject_modes,split_all_s}.py` | mode 注入 + 按模块拆分 |
| `tools/ghidra-labeling/RefineSeg<N>*.py` | 逐段细化脚本 (本会话产出) |
| `tools/ghidra-labeling/DisassembleHiddenFuncs.py` | R4 disasm 参考实现 |
| `build.bat` + `fc /b` / sha1sum | byte-identical 验证 |
| `doc/dev/methodology/{symbolization,build-pipeline}.md` | 字面量池符号化 / 导出器 equate 细节 |
