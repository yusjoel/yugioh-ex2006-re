# -*- coding: utf-8 -*-
"""
Step 0: 解析所有 fn_ptr 派发表, 输出完整 callgraph (含间接边)

策略:
  1. 找出所有 invoker thunk (FUN_0810e5c8 ~ FUN_0810e5f0, "bx r0..r10")
  2. 扫 asm/all.s 函数体, 找含 `bl <invoker>` 的 caller
  3. 在 caller 函数体内收集所有 `.word 0x0XXXXXXX` (ROM 地址) 引用
  4. 验证每个 ROM 地址处是否是合法 fn_ptr 表 (首项 LSB=1, 在 code range, 0 终止)
  5. 把表里所有 entries 加为 caller 的 indirect callee

输出:
  - temp/complete_callgraph.csv  (caller_addr, callee_addr, kind=direct|indirect_table)
  - temp/fnptr_tables.csv         (table_addr, length, caller_func, entries)
  - temp/enter_deck_edit_page_closure.txt  (示例闭包)
"""

import csv
import os
import re
import struct
import sys
from collections import defaultdict


ROM_PATH = "roms/2343.gba"
ASM_PATH = "asm/all.s"
DIRECT_CG = "temp/ghidra-funcs-callgraph.csv"
PROPOSALS = "doc/dev/naming-proposals.csv"

OUT_COMPLETE = "temp/complete_callgraph.csv"
OUT_TABLES = "temp/fnptr_tables.csv"
OUT_CLOSURE = "temp/enter_deck_edit_page_closure.txt"

ROM_BASE = 0x08000000
CODE_LO = 0x080000C0
CODE_HI = 0x084C7637
ROM_HI = 0x09FFFFFF

# 11 个 invoker thunks: bx r0..r10
INVOKERS = {
    0x0810e5c8: "bx_r0",
    0x0810e5cc: "bx_r1",
    0x0810e5d0: "bx_r2",
    0x0810e5d4: "bx_r3",
    0x0810e5d8: "bx_r4",
    0x0810e5dc: "bx_r5",
    0x0810e5e0: "bx_r6",
    0x0810e5e4: "bx_r7",
    0x0810e5e8: "bx_r8",
    0x0810e5ec: "bx_r9",
    0x0810e5f0: "bx_r10",
}


# ----- pass 1: parse asm/all.s -----

LABEL_RE = re.compile(r'^([A-Za-z_][A-Za-z_0-9]*):\s*$')
WORD_RE = re.compile(r'^\s*\.word\s+(?:0x([0-9a-fA-F]+)|([A-Za-z_][A-Za-z_0-9]*))(?:\s|$)')
ROM_ADDR_COMMENT_RE = re.compile(r'@\s+([0-9a-f]{8})\s')
BL_RE = re.compile(r'^\s*bl\s+([A-Za-z_][A-Za-z_0-9]*)\s')
LDR_DAT_RE = re.compile(r'^\s*ldr\s+r\d+,\s*([A-Za-z_][A-Za-z_0-9]*)\s')


def parse_asm(asm_path):
    """返回:
      funcs: list of dict (name, addr, start_line, end_line)
      labels: {label_name: addr or None}  (label 行号映射用 line_of_label)
      label_addr: {label_name: addr}      (从 ROM 地址注释推断)
      word_at_label: {label_name: int_value} (.word 紧跟 label, 解析后续 .word)
    """
    funcs = []
    label_addr = {}
    word_at_label = {}
    line_of_label = {}

    cur_func = None
    last_label = None

    with open(asm_path, encoding="utf-8") as f:
        lines = f.readlines()

    for i, line in enumerate(lines, start=1):
        # label?
        m = LABEL_RE.match(line)
        if m:
            label = m.group(1)
            last_label = label
            line_of_label[label] = i
            # 函数开始?
            if label.startswith(("FUN_", "SUB_")) or any(label.startswith(p) for p in
                ("LAB_", "DAT_", "PTR_", "DWORD_", "switchD_")) is False:
                # 任何非 LAB_/DAT_/PTR_/DWORD_/switchD_ 的标签都视为函数入口
                # 但要排除内部 LAB
                if not (label.startswith("LAB_") or label.startswith("DAT_") or
                        label.startswith("PTR_") or label.startswith("DWORD_") or
                        label.startswith("switchD_")):
                    if cur_func is not None:
                        cur_func["end_line"] = i - 1
                    addr = parse_addr_from_label(label)
                    cur_func = {"name": label, "addr": addr, "start_line": i, "end_line": None}
                    funcs.append(cur_func)
            continue
        # ROM 地址注释 (推断 label addr)
        if last_label is not None and last_label not in label_addr:
            cm = ROM_ADDR_COMMENT_RE.search(line)
            if cm:
                label_addr[last_label] = int(cm.group(1), 16)
        # .word 紧跟 last_label?
        wm = WORD_RE.match(line)
        if wm and last_label is not None and last_label not in word_at_label:
            if wm.group(1):
                word_at_label[last_label] = int(wm.group(1), 16)
            elif wm.group(2):
                # symbolic .word, 如 .word gPrng — 跳过 (resolved by .equ)
                pass

    if cur_func is not None:
        cur_func["end_line"] = len(lines)

    # 用 label_addr 回填函数地址 (语义命名的函数 parse_addr_from_label 解不出)
    for f in funcs:
        if f["addr"] is None and f["name"] in label_addr:
            f["addr"] = label_addr[f["name"]]

    return funcs, label_addr, word_at_label, lines


def parse_addr_from_label(label):
    """从 'FUN_080fbad0' 等抽出地址"""
    m = re.search(r"_([0-9a-fA-F]{8})$", label)
    if m:
        return int(m.group(1), 16)
    return None


# ----- pass 2: 找间接调用的 caller -----

def find_indirect_callers(funcs, lines):
    """对每个 caller, 列出 (line, invoker_name) 列表"""
    invoker_names_by_addr = {}
    # 反查 invoker 标签名
    for f in funcs:
        if f["addr"] in INVOKERS:
            invoker_names_by_addr[f["name"]] = f["addr"]

    if not invoker_names_by_addr:
        print("[warn] 未找到任何 invoker thunk, 检查 asm/all.s")
        return {}

    invoker_set = set(invoker_names_by_addr.keys())
    print(f"[scan] {len(invoker_set)} invoker thunks: {sorted(invoker_set)}")

    callers = {}  # caller_addr -> [(line, invoker_name)]
    for f in funcs:
        if f["addr"] is None:
            continue
        for ln in range(f["start_line"], f["end_line"] + 1):
            line = lines[ln - 1]
            m = BL_RE.match(line)
            if m and m.group(1) in invoker_set:
                callers.setdefault(f["addr"], []).append((ln, m.group(1)))
    return callers


def collect_word_refs(funcs, label_addr, word_at_label, lines):
    """对每个函数, 收集函数体内所有 ldr rN, DAT_xxx 引用的 .word 值"""
    refs = {}  # caller_addr -> set(rom_addr)
    for f in funcs:
        if f["addr"] is None:
            continue
        seen = set()
        for ln in range(f["start_line"], f["end_line"] + 1):
            line = lines[ln - 1]
            m = LDR_DAT_RE.match(line)
            if m:
                lbl = m.group(1)
                if lbl in word_at_label:
                    val = word_at_label[lbl]
                    seen.add(val)
        if seen:
            refs[f["addr"]] = seen
    return refs


# ----- pass 3: 验证 fn_ptr 表 -----

def validate_fnptr_table(rom, table_addr, max_entries=128):
    """读 ROM 在 table_addr, 返回 entries 列表 (Thumb fn_ptr, LSB=1, 在 code range)
    遇到 0 或非法 entry 停止"""
    if table_addr < ROM_BASE or table_addr > ROM_HI:
        return None
    off = table_addr - ROM_BASE
    if off + 4 > len(rom):
        return None
    # 读首项验证
    first = struct.unpack_from("<I", rom, off)[0]
    if (first & 1) != 1:
        return None
    if first < CODE_LO or first > CODE_HI:
        return None
    entries = [first]
    for i in range(1, max_entries):
        if off + 4 * (i + 1) > len(rom):
            break
        w = struct.unpack_from("<I", rom, off + 4 * i)[0]
        if w == 0:
            entries.append(0)
            break
        # 允许 0 entry (state 无 handler) — 不终止
        if (w & 1) == 1 and CODE_LO <= w <= CODE_HI:
            entries.append(w)
        elif w == 0:
            entries.append(0)
            break
        else:
            # 非法 entry, 停止 (含 0 终止前的非法)
            break
    # 至少 1 个有效 fn_ptr
    valid = [e for e in entries if e != 0]
    if len(valid) < 1:
        return None
    return entries


# ----- main -----

def main():
    print("[load] asm/all.s")
    funcs, label_addr, word_at_label, lines = parse_asm(ASM_PATH)
    print(f"  {len(funcs)} functions, {len(word_at_label)} .word labels")

    print("[load] roms/2343.gba")
    rom = open(ROM_PATH, "rb").read()

    print("[load] direct callgraph")
    direct_edges = set()
    with open(DIRECT_CG) as f:
        for r in csv.DictReader(f):
            direct_edges.add((int(r["caller_addr"], 16), int(r["callee_addr"], 16)))
    print(f"  {len(direct_edges)} direct edges")

    print("[step 1] 找间接 caller")
    callers = find_indirect_callers(funcs, lines)
    print(f"  {len(callers)} caller 含 invoker bl")

    print("[step 2] 收集每个 caller 的 .word ROM refs")
    refs = collect_word_refs(funcs, label_addr, word_at_label, lines)

    print("[step 3] 验证 fn_ptr 表")
    indirect_edges = set()
    tables = []  # (caller_addr, table_addr, entries)
    for caller_addr, _ in callers.items():
        rom_refs = refs.get(caller_addr, set())
        for rom_addr in rom_refs:
            entries = validate_fnptr_table(rom, rom_addr)
            if entries is None:
                continue
            valid_entries = [e for e in entries if e != 0]
            tables.append((caller_addr, rom_addr, valid_entries, len(entries)))
            for ep in valid_entries:
                # entry 是 Thumb addr (LSB=1), 函数实际入口 = ep & ~1
                callee = ep & ~1
                indirect_edges.add((caller_addr, callee))

    print(f"  发现 {len(tables)} 个 fn_ptr 表, {len(indirect_edges)} 个间接边")

    # 输出 tables CSV
    os.makedirs("temp", exist_ok=True)
    with open(OUT_TABLES, "w", encoding="utf-8") as f:
        f.write("caller_addr,table_rom_addr,n_entries,n_total,entries\n")
        for ca, ta, eps, nt in sorted(tables):
            f.write(f"0x{ca:08x},0x{ta:08x},{len(eps)},{nt},"
                    f"{';'.join(f'0x{e&~1:08x}' for e in eps)}\n")
    print(f"  -> {OUT_TABLES}")

    # 合并完整 callgraph
    all_edges = set()
    for e in direct_edges:
        all_edges.add((e[0], e[1], "direct"))
    for ca, ce in indirect_edges:
        all_edges.add((ca, ce, "indirect_table"))
    with open(OUT_COMPLETE, "w", encoding="utf-8") as f:
        f.write("caller_addr,callee_addr,kind\n")
        for ca, ce, k in sorted(all_edges):
            f.write(f"0x{ca:08x},0x{ce:08x},{k}\n")
    print(f"  -> {OUT_COMPLETE}  ({len(all_edges)} edges total)")

    # 计算 enter_deck_edit_page 闭包
    calls = defaultdict(set)
    for ca, ce, k in all_edges:
        calls[ca].add((ce, k))

    root = 0x08108ac0
    visited = {root: 0}
    queue = [root]
    edge_kind = {}  # callee -> kind
    while queue:
        nxt = []
        for f in queue:
            for callee, k in calls.get(f, []):
                if callee not in visited:
                    visited[callee] = visited[f] + 1
                    edge_kind[callee] = k
                    nxt.append(callee)
        queue = nxt

    # 加载已命名
    known = {}
    with open(PROPOSALS) as f:
        for r in csv.DictReader(f):
            known[int(r["address"], 16)] = r["name"]

    with open(OUT_CLOSURE, "w", encoding="utf-8") as f:
        f.write(f"# enter_deck_edit_page (0x08108ac0) 完整闭包 (含间接派发)\n")
        f.write(f"# 总计 {len(visited)} 函数\n")
        f.write(f"# level=BFS 深度, kind=direct/indirect_table, name=已命名/FUN_/SUB_/-\n\n")
        # 按 (level, addr) 排序
        for addr, lv in sorted(visited.items(), key=lambda x: (x[1], x[0])):
            n = known.get(addr, "")
            if not n:
                n = "-"
            tag = ""
            if n.startswith("FUN_") or n.startswith("SUB_") or n == "-":
                tag = "[需分析]"
            else:
                tag = "[已命名]"
            k = edge_kind.get(addr, "ROOT")
            f.write(f"  L{lv}  0x{addr:08x}  {k:16s}  {n:40s}  {tag}\n")
    print(f"  -> {OUT_CLOSURE}")

    # 简报
    print()
    print("=== enter_deck_edit_page 闭包 ===")
    print(f"  总函数: {len(visited)}")
    from collections import Counter
    by_level = Counter(visited.values())
    for lv in sorted(by_level):
        print(f"    L{lv}: {by_level[lv]}")
    named = sum(1 for a in visited if known.get(a, "FUN_").startswith("FUN_") is False
                and known.get(a, "SUB_").startswith("SUB_") is False
                and known.get(a, "") != "")
    print(f"  已命名: {named}")
    print(f"  未命名: {len(visited) - named}")


if __name__ == "__main__":
    main()
