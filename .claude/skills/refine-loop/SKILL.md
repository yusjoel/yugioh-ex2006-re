---
name: refine-loop
description: Drive the address-ordered per-segment refinement loop for an already-named disassembly module (asm/NN_*.s). Symbolizes constants/labels/data, carves inter-function ROM_INCBIN, disassembles mislabeled code, fixes comments — all byte-identical. Use when the user says "继续细化" / "细化 Seg-N" / "/refine-loop" / wants to refine a code segment to eliminate DAT_/ROM_INCBIN residue.
---

# Refine Loop Driver Skill (slim)

驱动**已命名**模块的逐段内部细化循环。本 skill 仅给主线程调度纲领；完整方法论在
`doc/dev/methodology/refine-loop.md`，活动文件的进度+路线图在 `doc/dev/p5-refine-<file>.md`。
与 `analysis-loop` 互补：命名给函数起名，细化打磨函数体内与函数之间的一切。

## 入口

```
/refine-loop                 # 自动选下一段 (活动 refine 文档 §五 第一个未 ✅ 的 Seg)
/refine-loop Seg-6           # 显式段号
/refine-loop 0x16344         # 显式起始地址 (落在某 Seg 内)
```

无活动 refine 文档时：先按方法论「段划分」把目标文件均分 ~10 段 (Seg-1..Seg-10, 边界=函数结束处)，
写入新 `doc/dev/p5-refine-<file>.md` 的 §五 路线图。

## 三条硬规则 (违反即停)

1. **严格地址序**：按 Seg 序号执行，段内低→高，**不回头不跳号**。不按子系统/难度。
2. **函数间数据必处理**：段内 `ROM_INCBIN`/`.byte` 块**不留**——被引用代码 → R4 disasm；被引用数据 → R7 carve 进 rom.s。
3. **唯一例外**：全 ROM 0 引用 (ref-scan raw + THUMB+1) → §5.1 登记留待。

## 每段工作流 (Seg-N)

```
0. 备份 .rep → .rep.bak-<ts>-pre-seg<N>
1. 测绘段: 扫 [start,end) 内 残留自动名 label + ROM_INCBIN/.byte 块 + 函数入口
2. 数据块分类 (ref-scan → disasm / carve / §5.1, 见方法论决策树)
3. 读消费者理解槽语义 (R6); 留意误名信号 (函数体全局 vs 函数名矛盾)
4. 写 RefineSeg<N>*.py: equate / carve-label-ref / 槽改名 / plate (+ rom.s carve, + disasm 脚本)
5. DRY-run (0 FAIL) → 实跑
6. ghidra-export-range 080000c0 084c7637 → inject_modes → split_all_s → build → SHA1 校验
7. (改函数名才) ExportFunctionInventory + sync + 手改 naming-proposals.csv
8. 更新 refine 文档: §四 记录 + §三 进度 + §5.1 (如有) + §五 标 ✅
9. commit (用户指令后)
10. 更新 MEMORY 续接指针
```

## R1-R9 细化清单 (逐项过, 详见方法论)

R1 常量 equate (先查现有 inc 复用) · R2 自动名→语义名 · R3 USER-label+DATA-ref 接通 ·
R4 误标代码 disasm · R5 注释用现名+订正误名 · R6 先读消费者 · R7 数据 carve 进 rom.s ·
R8 图形目视核对 · R9 byte-identical + 备份。

## 红线 (任一触发 → abort 求助用户)

1. byte-identical SHA1 != `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`
2. Ghidra EOL/plate 写入含 **CJK** (Jython 双重 UTF-8 mojibake) —— Ghidra 注释一律 ASCII, 中文走 doc/
3. 数据块臆造语义 (无 file:line 证据 + 置信度) / 出现"似乎/可能/大概"
4. ROM_INCBIN 被引用却 §5.1 登记 (规则 2/3 误判)

## 关键技法 (一次性参考)

- **carve THUMB 指针表**: `.word <fn> + 1` (ROM 存 addr|1, 漏 +1 → 字节失配)。
- **R4 跳转表目标块**: 逐 stub `DisassembleCommand` (单次整 range 只 disasm 首 stub); 重跑前先 `clearListing` 整 range 再 `setTMode` (否则 ContextChangeException)。
- **R3 接通**: `createLabel(target,USER)` + `addMemoryReference(slot,target,DATA)` + 槽改名 → `resolve_word_symbol` 导出 `.word <name>`。
- **ref-scan 孤儿判定**: `d.count(struct.pack("<I", addr))` 对 addr 与 addr|1; 压缩资产里的偶合 raw 值不算真引用。
- **per-slot 安全**: equate/ref 只作用该槽, 同值字面量别处不受影响 → 跨段安全。

## 关键路径

| 文件 | 用途 |
|------|------|
| `doc/dev/methodology/refine-loop.md` | 完整方法论 (按需读) |
| `doc/dev/p5-refine-<file>.md` | 活动文件进度 + §五 Seg 路线图 + §5.1 登记 |
| `.claude/skills/symbolization` 或 `doc/dev/methodology/symbolization.md` | 字面量池符号化细节 |
| `tools/asm-regen/{ghidra-run-script,ghidra-export-range}.bat` | Ghidra 脚本 / 重导出 |
| `tools/ghidra-labeling/RefineSeg*.py` + `DisassembleSeg5cJpHandlers.py` | 逐段脚本 + R4 disasm 范例 |
| `tools/ghidra-labeling/DisassembleHiddenFuncs.py` | R4 disasm 参考实现 |
