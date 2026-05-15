# -*- coding: utf-8 -*-
"""
生成 doc/dev/eval/PROGRESS.md 初始版本 (新根函数 bootstrap 用)

骨架:
- 续接提示词
- 当前状态
- 进度 + class 分布
- 高 rev 异常 (rev >= 3, 初始空)
- BLOCKED 追踪 (初始空)
- 失败追踪 (auto-skip, pick_batch.py 数据源, 初始空)

已命名函数清单不再写入本文档, 改由 doc/dev/naming-proposals.csv 维护。
"""

import csv
import datetime
import os
from collections import Counter

CLOSURE_CSV = "temp/closure_topo_order.csv"
OUT = "doc/dev/eval/PROGRESS.md"

ROOT_ADDR = 0x08108ac0
ROOT_NAME = "enter_deck_edit_page"


CLASS_DESC = {
    "A_named": "已命名 (来自跨根池)",
    "B_invoker": "invoker thunks",
    "B_runtime": "runtime/libgcc",
    "C_util_high": "indeg >= 20 的高频工具",
    "D_shared_mid": "indeg 5-19 的共享函数",
    "E_specific_low": "indeg 1-4 的 feature-specific",
    "F_orphan": "indeg=0 的 root",
}
CLASS_SKIP = {"A_named", "B_invoker", "B_runtime"}


def main():
    rows = []
    with open(CLOSURE_CSV) as f:
        for r in csv.DictReader(f):
            rows.append(r)
    todo = [r for r in rows if r["class"] not in CLASS_SKIP]
    todo.sort(key=lambda r: int(r["topo_idx"]))
    total = len(todo)
    nxt = todo[0] if todo else None

    class_counts = Counter(r["class"] for r in rows)

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    today = datetime.datetime.now().strftime("%Y-%m-%d")

    lines = []
    lines.append("# 反汇编命名 — 进度跟踪文档")
    lines.append("")
    lines.append("> 用途: 跨会话续接的项目状态镜像。新会话读完本文档即可继续工作。")
    lines.append("> 已命名函数清单见 `doc/dev/naming-proposals.csv` (pick_batch.py 数据源, 不在本文档维护)。")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 续接提示词 (新会话直接粘贴)")
    lines.append("")
    lines.append("```")
    lines.append("读 doc/dev/eval/PROGRESS.md 续接反汇编命名工作, batch=20 全自动模式。")
    lines.append("")
    lines.append("python tools/ad-hoc/pick_batch.py --max 20 --out temp/batch.json")
    lines.append("")
    lines.append("启动 4-agent loop (executor → reviewer → fixer → lesson-keeper) 处理 batch.json 中的全部函数,")
    lines.append("单 Ghidra session + 单 build + 单 sha1 verify, byte-identical 通过后自动 commit, 进入下一 batch。")
    lines.append("")
    lines.append("**强制单 call 模式 (token 经济优先, 不在意 wall-clock)**:")
    lines.append("  - executor: 1 个 sub-agent 一次性产出 batch 全部 20 份 proposal (禁止拆分 4×5 并行)")
    lines.append("  - reviewer: 1 个 sub-agent 一次性评 20 份 (禁止拆分)")
    lines.append("  - fixer iter (NEEDS_FIX): 1 个 sub-agent 处理本批所有 NEEDS_FIX")
    lines.append("  - 拆分并行会导致 skill/feedback/asm 上下文重复加载, 实测 ~3× token 浪费, 收益仅 wall-clock")
    lines.append("")
    lines.append("任何函数失败 (byte-identical ❌ / MAX_ITER / agent 求助 / 无法命名) → 不停下询问:")
    lines.append("  1. 在 PROGRESS.md \"失败追踪\" 段记录 (ADDR, reason, date)")
    lines.append("  2. pick_batch.py 自动把\"含失败 callee\"的函数标 SKIP, 不进入下一 batch")
    lines.append("  3. 继续下一批")
    lines.append("")
    lines.append("仅 BLOCKED 但有命名的函数仍走落地 (BLOCKED 是 SB tracking 不阻塞 rename)。")
    lines.append("```")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 当前状态")
    lines.append("")
    lines.append("| 字段 | 值 |")
    lines.append("|------|----|")
    lines.append(f"| **根函数** | `{ROOT_NAME}` (0x{ROOT_ADDR:08x}) |")
    lines.append("| **当前步骤** | Step 0 — 装配完成, 准备开第一批 |")
    if nxt:
        lines.append(f"| **下一步** | `python tools/ad-hoc/pick_batch.py --max 20 --out temp/batch.json` → 启动 4-agent loop (下一候选: topo={nxt['topo_idx']}) |")
    else:
        lines.append("| **下一步** | 闭包内无待命名函数 |")
    lines.append(f"| **上次更新** | {now} |")
    lines.append(f"| **上次 callgraph 刷新** | {today} |")
    lines.append("| **callgraph_locked** | `true` (后续 rename 不动拓扑, 整任务期间不需再 refresh) |")
    lines.append("")

    lines.append("## 进度")
    lines.append("")
    lines.append(f"**0 / {total} = 0.00% 已分析** (跳过 A/B 类 = {sum(class_counts[c] for c in CLASS_SKIP)} 函数)")
    lines.append("")
    lines.append("### 闭包 class 分布")
    lines.append("")
    lines.append("| class | 数量 | 含义 | 处理 |")
    lines.append("|-------|-----:|------|------|")
    for cls in ["A_named", "B_invoker", "B_runtime", "C_util_high", "D_shared_mid", "E_specific_low", "F_orphan"]:
        n = class_counts.get(cls, 0)
        if n == 0:
            continue
        act = "跳过" if cls in CLASS_SKIP else "命名"
        lines.append(f"| {cls} | {n} | {CLASS_DESC[cls]} | {act} |")
    lines.append("")
    lines.append("---")
    lines.append("")

    lines.append("## 高 rev 异常 (rev >= 3)")
    lines.append("")
    lines.append("> fixer 落地 phase 在 rev >= 3 时追加一行。低 rev 函数不入表 (静默 PASSED)。")
    lines.append("> 用途: 观察哪类函数语义反复扣分, 反推 methodology 缺口。")
    lines.append("")
    lines.append("| ADDR | rev | 函数名 | 备注 |")
    lines.append("|------|-----|--------|------|")
    lines.append("| _(空)_ | — | — | — |")
    lines.append("")
    lines.append("---")
    lines.append("")

    lines.append("## BLOCKED 追踪")
    lines.append("")
    lines.append("| SB 编号 | 日期 | 阻塞原因 | 解除前置条件 |")
    lines.append("|---------|------|----------|-------------|")
    lines.append("| _(空)_ | — | — | — |")
    lines.append("")
    lines.append("> 格式: `SB-<ADDR>-<N> | <YYYY-MM-DD> | <阻塞原因> | <解除前置条件>`")
    lines.append("")

    lines.append("## 失败追踪 (auto-skip)")
    lines.append("")
    lines.append("> fixer 在 byte-identical ❌ / MAX_ITER / agent 求助 / 完全无法命名 时追加。")
    lines.append("> pick_batch.py 自动:")
    lines.append(">   - 排除 ADDR 在本表的函数 (本身失败)")
    lines.append(">   - 排除直接 callee 含本表 ADDR 的函数 (cascade SKIP, 因 R7 无法满足)")
    lines.append("")
    lines.append("| ADDR | 日期 | 失败原因 | 备注 |")
    lines.append("|------|------|----------|------|")
    lines.append("| _(空)_ | — | — | — |")
    lines.append("")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    print(f"[done] -> {OUT} ({total} 待命名函数)")


if __name__ == "__main__":
    main()
