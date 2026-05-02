# -*- coding: utf-8 -*-
"""
生成 doc/dev/eval/PROGRESS.md 初始版本
- 续接提示词
- 当前状态
- 进度
- 函数列表 (从 closure_topo_order.csv 取 class != A/B 的所有函数, 按 topo_idx 升序)
- 历史里程碑
- BLOCKED 追踪
"""

import csv
import datetime
import os

CLOSURE_CSV = "temp/closure_topo_order.csv"
OUT = "doc/dev/eval/PROGRESS.md"

ROOT_ADDR = 0x08108ac0
ROOT_NAME = "enter_deck_edit_page"


def main():
    rows = []
    with open(CLOSURE_CSV) as f:
        for r in csv.DictReader(f):
            rows.append(r)
    # 跳过 A/B 类
    todo = [r for r in rows if r["class"] not in ("A_named", "B_invoker", "B_runtime")]
    todo.sort(key=lambda r: int(r["topo_idx"]))
    total = len(todo)

    # 选下一个 (topo_idx 最小)
    nxt = todo[0] if todo else None

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    today = datetime.datetime.now().strftime("%Y-%m-%d")

    lines = []
    lines.append("# 反汇编命名 — 进度跟踪文档")
    lines.append("")
    lines.append('> 用途: 跨会话续接的项目状态镜像。新会话读完本文档即可继续工作。')
    lines.append('> **每次完成 1 个函数, fixer 必须更新本文档** (PROGRESS 字段 + 函数列表对应行)')
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 续接提示词 (新会话直接粘贴)")
    lines.append("")
    lines.append("```")
    lines.append('读 doc/dev/eval/PROGRESS.md 续接反汇编命名工作.')
    lines.append('')
    lines.append('按 下一步 字段开始:')
    lines.append('  Skill: analysis-loop <next_function_addr>')
    lines.append('')
    lines.append('每完成 1 个函数, 必须:')
    lines.append('  1. 更新进度百分比 + 已分析数')
    lines.append('  2. 更新函数列表对应行的 分析后函数名 + rev + eval 链接')
    lines.append('  3. 更新 当前步骤 + 下一步 字段')
    lines.append('  4. 不自动 commit, 等用户指令')
    lines.append("```")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 当前状态")
    lines.append("")
    lines.append("| 字段 | 值 |")
    lines.append("|------|----|")
    lines.append(f"| **根函数** | `{ROOT_NAME}` (0x{ROOT_ADDR:08x}) |")
    lines.append(f"| **当前步骤** | Step 3 — 装配完成, 准备 POC |")
    lines.append(f"| **下一步** | 开始分析 `{nxt['name']}` (topo={nxt['topo_idx']}, L{nxt['depth']}, indeg={nxt['indeg']}, {nxt['class']}) |")
    lines.append(f"| **上次更新** | {now} |")
    lines.append(f"| **上次 callgraph 刷新** | {today} 11:00 |")
    lines.append("")

    lines.append("## 进度")
    lines.append("")
    lines.append(f"**0 / {total} (0.00%) 已分析** (跳过 A 已命名 + B runtime/invoker)")
    lines.append("")
    lines.append("---")
    lines.append("")

    lines.append("## 函数列表 (按 topo_idx 升序, 跳过 A/B 类)")
    lines.append("")
    lines.append("> 列说明: # 序号 / topo 拓扑序 / depth BFS 深度 / indeg 全 ROM 入度 / class C 高 indeg / D 中 / E 低 / F orphan")
    lines.append("> rev = 本函数完成命名所需的 reviewer 轮数 (期望 ≤ 3)")
    lines.append("")
    lines.append("| # | topo | L | indeg | class | 位置 | 分析前 | 分析后 | rev | eval |")
    lines.append("|---|------|---|-------|-------|------|--------|--------|-----|------|")
    for i, r in enumerate(todo, start=1):
        addr = r["addr"]
        cls_short = {
            "C_util_high": "C",
            "D_shared_mid": "D",
            "E_specific_low": "E",
            "F_orphan": "F",
        }.get(r["class"], r["class"][:2])
        lines.append(f"| {i} | {r['topo_idx']} | L{r['depth']} | {r['indeg']} | {cls_short} | `{addr}` | {r['name']} | _(待分析)_ | — | — |")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 历史里程碑")
    lines.append("")
    lines.append(f"- {today} 10:30: Step 0 完成, 闭包从 2 → 308 函数 (commit ac61a1e)")
    lines.append(f"- {today} 11:00: Step 1+2 完成, 拓扑排序 + 分类 (commit 930cccd)")
    lines.append(f"- {today} 11:55: 装配 refactor-loop 4-agent 体系 (本次 commit)")
    lines.append("")

    lines.append("## BLOCKED 追踪")
    lines.append("")
    lines.append("无 BLOCKED 项。")
    lines.append("")
    lines.append("> 格式: `SB-<ADDR>-<N> | <YYYY-MM-DD> | <阻塞原因> | <解除前置条件>`")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    print(f"[done] -> {OUT} ({len(todo)} 函数)")


if __name__ == "__main__":
    main()
