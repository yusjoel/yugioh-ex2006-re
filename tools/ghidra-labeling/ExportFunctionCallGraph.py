# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# ExportFunctionCallGraph.py  (Jython 2.7 / Ghidra script)
#
# 导出 Ghidra 工程的函数调用图, 一边一行, 给后续 Python 脚本做扩散用
# (e.g. tools/ad-hoc/propagate_label_tags.py).
#
# 输出: temp/ghidra-funcs-callgraph.csv
#   columns: caller_addr, callee_addr
#   - caller / callee 都是 0x08xxxxxx GBA 地址
#   - 同一对 (caller, callee) 不去重以保留多次调用计数 (但当前消费者去重)
#   - thunks 不特殊处理 (Ghidra 的 getCalledFunctions 已包含 thunk-resolved targets)
#
# 此脚本 *只读*: 不 createFunction / 不 setName.
#
# 用法:
#   tools\asm-regen\ghidra-run-script.bat ExportFunctionCallGraph.py

import os

from ghidra.util.task import ConsoleTaskMonitor


def repo_root():
    try:
        src = getSourceFile().getAbsolutePath()
        return os.path.dirname(os.path.dirname(os.path.dirname(src)))
    except Exception:
        return os.getcwd()


def main():
    fm = currentProgram.getFunctionManager()
    monitor = ConsoleTaskMonitor()

    # 收集函数 + ep set (用于过滤 callee 必须在工程中)
    funcs = []
    func_eps = set()
    it = fm.getFunctions(True)
    while it.hasNext():
        f = it.next()
        funcs.append(f)
        func_eps.add(f.getEntryPoint().getOffset() & 0xFFFFFFFF)
    print("[scan] functions = %d" % len(funcs))

    out_dir = os.path.join(repo_root(), "temp")
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    csv_path = os.path.join(out_dir, "ghidra-funcs-callgraph.csv")
    f_csv = open(csv_path, "w")
    f_csv.write("caller_addr,callee_addr\n")

    n_edges = 0
    n_self_edges = 0
    n_callers_with_callees = 0
    n_callees_unknown = 0  # callee ep 不在工程函数集 (理论上不会, sanity)
    for f in funcs:
        caller_ep = f.getEntryPoint().getOffset() & 0xFFFFFFFF
        callees = f.getCalledFunctions(monitor)
        wrote_any = False
        # 同 caller -> callee 多次 ref 只输出一次 (去重)
        seen = set()
        for c in callees:
            c_ep = c.getEntryPoint().getOffset() & 0xFFFFFFFF
            if c_ep in seen:
                continue
            seen.add(c_ep)
            if c_ep == caller_ep:
                n_self_edges += 1
                continue
            if c_ep not in func_eps:
                n_callees_unknown += 1
                continue
            f_csv.write("0x%08x,0x%08x\n" % (caller_ep, c_ep))
            n_edges += 1
            wrote_any = True
        if wrote_any:
            n_callers_with_callees += 1
    f_csv.close()

    print("[done] ExportFunctionCallGraph")
    print("  edges (deduped)         = %d" % n_edges)
    print("  callers with >=1 edge   = %d" % n_callers_with_callees)
    print("  self edges (skipped)    = %d" % n_self_edges)
    print("  unknown callees skipped = %d" % n_callees_unknown)
    print("  -> %s" % csv_path)


main()
