# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# ApplyNamingProposals.py
#
# 读 doc/dev/naming-proposals.csv 里 score=5 的提案, 把对应函数 rename 到
# proposed_name (SourceType.USER_DEFINED). 仅 rename, 不创建函数, 不动其它.
#
# 跳过条件 (各计独立桶):
#   skip_no_score5         score 不是 5
#   skip_no_proposed       proposed_name 为空
#   skip_not_function      地址处没有 Function (Ghidra 没识别成函数)
#   skip_already_named     当前 name 已不是 FUN_/SUB_/thunk_FUN_ 前缀
#   skip_same_name         current name 已经等于 proposed (重跑幂等)
#
# 用法:
#   tools\asm-regen\ghidra-run-script.bat ApplyNamingProposals.py [dry]

import csv
import os

from ghidra.program.model.symbol import SourceType


RUN_DRY = False
try:
    _args = list(getScriptArgs())
    if _args and _args[0].lower() in ("dry", "--dry", "1", "true"):
        RUN_DRY = True
except Exception:
    pass


def repo_root():
    try:
        src = getSourceFile().getAbsolutePath()
        return os.path.dirname(os.path.dirname(os.path.dirname(src)))
    except Exception:
        return os.getcwd()


def main():
    csv_path = os.path.join(repo_root(), "doc", "dev", "naming-proposals.csv")
    if not os.path.isfile(csv_path):
        print("ERROR: %s not found" % csv_path)
        return

    af = currentProgram.getAddressFactory()
    space = af.getDefaultAddressSpace()
    fm = currentProgram.getFunctionManager()

    proposals = []
    n_total_rows = 0
    skip_no_score5 = 0
    skip_no_proposed = 0
    f = open(csv_path, "r")
    try:
        reader = csv.DictReader(f)
        for row in reader:
            n_total_rows += 1
            score = (row.get("score") or "").strip()
            if score != "5":
                skip_no_score5 += 1
                continue
            proposed = (row.get("proposed_name") or "").strip()
            if not proposed:
                skip_no_proposed += 1
                continue
            try:
                addr_int = int(row["address"], 16)
            except (ValueError, TypeError):
                continue
            proposals.append((addr_int, row.get("name", ""), proposed))
    finally:
        f.close()

    print("[load   ] CSV total rows         = %d" % n_total_rows)
    print("[filter ] skip score!=5          = %d" % skip_no_score5)
    print("[filter ] skip empty proposed    = %d" % skip_no_proposed)
    print("[plan   ] candidates to apply    = %d" % len(proposals))
    print("[mode   ] dry = %s" % RUN_DRY)

    n_renamed = 0
    skip_not_function = 0
    skip_already_named = 0
    skip_same_name = 0
    n_fail = 0
    samples = []
    fails = []

    for addr_int, csv_name, proposed in proposals:
        addr = space.getAddress(addr_int)
        func = fm.getFunctionAt(addr)
        if func is None:
            skip_not_function += 1
            continue
        cur_name = func.getName()
        is_auto = (cur_name.startswith("FUN_") or cur_name.startswith("SUB_")
                   or cur_name.startswith("thunk_FUN_"))
        if cur_name == proposed:
            skip_same_name += 1
            continue
        if not is_auto:
            skip_already_named += 1
            continue
        if RUN_DRY:
            n_renamed += 1
            if len(samples) < 12:
                samples.append((addr_int, cur_name, proposed))
            continue
        try:
            func.getSymbol().setName(proposed, SourceType.USER_DEFINED)
            n_renamed += 1
            if len(samples) < 12:
                samples.append((addr_int, cur_name, proposed))
        except Exception as e:
            n_fail += 1
            if len(fails) < 8:
                fails.append((addr_int, cur_name, proposed, str(e)))

    print("\n[done   ] ApplyNamingProposals  (dry=%s)" % RUN_DRY)
    print("  renamed                = %d" % n_renamed)
    print("  skip not_function      = %d  (Ghidra 没把那个地址当函数)" % skip_not_function)
    print("  skip already_named     = %d  (有非 FUN_ 命名, 不覆盖)" % skip_already_named)
    print("  skip same_name         = %d  (幂等)" % skip_same_name)
    print("  fail                   = %d" % n_fail)
    if samples:
        print("  -- sample --")
        for a, old, new in samples:
            print("    0x%08x  %-30s  ->  %s" % (a, old, new))
    if fails:
        print("  -- fail --")
        for a, old, new, msg in fails:
            print("    0x%08x  %-30s  ->  %-30s  %s" % (a, old, new, msg))


main()
