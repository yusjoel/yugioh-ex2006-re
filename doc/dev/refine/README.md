# doc/dev/refine/

refine-loop 体系每段的留痕目录 (参照 `doc/dev/eval/` 之于 analysis-loop):

- `<Seg-N>.proposal.md` — refine-executor 产出 (段测绘 + 数据块分类 + 符号化/carve/disasm/§5.1 计划)
- `<Seg-N>.review.md`   — refine-reviewer 产出 (C1-C13 核验 + verdict + 修改清单)

落地结果 (Ghidra 改动 / byte-identical / commit) 由 refine-fixer 执行, 记录进活动 refine 文档
`doc/dev/p5-refine-<file>.md` 的 §四 (逐段记录) + §五 (路线图 ✅) + §5.1 (未引用登记)。

方法论: `doc/dev/methodology/refine-loop.md`; 驱动 skill: `.claude/skills/refine-loop/`。
