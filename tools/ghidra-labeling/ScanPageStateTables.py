# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# ScanPageStateTables.py  (Jython 2.7 / Ghidra script)
#
# 方法 5 - 状态机表反推 (function-naming.md §七).
#
# GBA 游戏 UI / page 用 C 风格 vtable 实现状态机:
#   struct { void(*init)(); void(*load)(); void(*tick)(); void(*exit)(); };
# ROM 表现为连续 N x 4B 合法 Thumb 函数指针 (高位 0x08/0x09, 低位 |1).
#
# 算法:
#   1. 扫 ROM [0x08000000, 0x09FFFFFF] 4-byte 对齐窗口
#   2. 每窗口验证是否合法 Thumb 函数指针:
#      - 值 in [0x08000001, 0x084C7637] 且 (val & 1) == 1
#      - target = val & ~1, 首 hword 是 push {..., lr} (0xB500-0xB5FF)
#      - target 必须在 prologue-able 地址 (4 字节对齐 || 2 字节对齐合法 THUMB)
#   3. 累积连续匹配, 长度 >= MIN_TABLE_SIZE (默认 3) 即候选表
#      (经典 4-entry vtable, 但有些表是 3 个或 5 个; 取 3 减少漏掉小表)
#   4. 对每个候选表:
#      - 找 ldr ref 指向表起点的 caller (= page dispatcher)
#      - 标记 entry 是否已命名
#      - 输出 CSV 行
#
# 输出: temp/ghidra-state-tables.csv
#   columns: table_addr, n_entries, n_callers, entry_0_addr, entry_0_name,
#            entry_1_addr, entry_1_name, ...,  caller_0_addr, caller_0_name, ...
#
# 用法: tools\asm-regen\ghidra-run-script.bat ScanPageStateTables.py

import os

CODE_LO = 0x080000C0
CODE_HI = 0x084C7637

ROM_LO = 0x08000000
ROM_HI = 0x09FFFFFF

MIN_TABLE_SIZE = 3   # 至少 3 个连续 Thumb fn ptr 才算候选
MAX_TABLE_SIZE = 32  # 上限 (避免奇怪长链)

# 跳过已知非状态表区 (asm/all.s 范围内的 LITERAL POOL 等高密度指针区)
# all.s 范围 [0x080000C0, 0x084C7637]; 这区里的连续指针多是 .word 字面量池
# 状态表通常在 0x09xxxxxx 数据区
SKIP_CODE_REGION = True


def repo_root():
    try:
        src = getSourceFile().getAbsolutePath()
        return os.path.dirname(os.path.dirname(os.path.dirname(src)))
    except Exception:
        return os.getcwd()


def is_thumb_func_ptr(val, mem, af):
    """合法 Thumb 函数指针: 值在 ROM, 低位 1, target 首指令是 push {...,lr}."""
    if (val & 1) == 0:
        return False
    target = val & ~1
    if not (CODE_LO <= target <= CODE_HI):
        return False
    # target 必须 2 字节对齐 (THUMB)
    if target & 1:
        return False
    # 读首 hword 看是不是 push {..., lr}: 0xB500-0xB5FF
    try:
        hw = mem.getShort(af.getAddress("0x%08x" % target)) & 0xFFFF
    except Exception:
        return False
    if 0xB500 <= hw <= 0xB5FF:
        return True
    # 也允许 STMFD sp!{...,lr} (ARM 32-bit, 较少在 GBA THUMB code), 跳过
    return False


def safe_csv(s):
    if s is None:
        return ""
    s = str(s)
    if "," in s or '"' in s or "\n" in s:
        return '"' + s.replace('"', '""') + '"'
    return s


def main():
    af = currentProgram.getAddressFactory()
    mem = currentProgram.getMemory()
    rm = currentProgram.getReferenceManager()
    fm = currentProgram.getFunctionManager()

    print("[scan] range = [0x%08x, 0x%08x]" % (ROM_LO, ROM_HI))
    print("[scan] MIN_TABLE_SIZE = %d  MAX_TABLE_SIZE = %d" %
          (MIN_TABLE_SIZE, MAX_TABLE_SIZE))

    # 用 ROM 数据区起点 + 4 字节步进
    # 跳过 asm/all.s 代码段 (CODE_LO..CODE_HI), 避开字面量池
    candidates = []  # list of (table_start, [entry_addrs])
    n_words_scanned = 0
    n_total_thumb_ptrs = 0

    addr = ROM_LO
    while addr < ROM_HI:
        if SKIP_CODE_REGION and CODE_LO <= addr <= CODE_HI:
            addr = (CODE_HI + 1) & ~3  # 跳到代码段后, 4 字节对齐
            continue
        try:
            val = mem.getInt(af.getAddress("0x%08x" % addr)) & 0xFFFFFFFF
        except Exception:
            addr += 4
            continue
        n_words_scanned += 1
        if is_thumb_func_ptr(val, mem, af):
            n_total_thumb_ptrs += 1
            # 累积连续
            entries = [val & ~1]
            scan = addr + 4
            while scan < ROM_HI and len(entries) < MAX_TABLE_SIZE:
                try:
                    v2 = mem.getInt(af.getAddress("0x%08x" % scan)) & 0xFFFFFFFF
                except Exception:
                    break
                if not is_thumb_func_ptr(v2, mem, af):
                    break
                entries.append(v2 & ~1)
                scan += 4
            if len(entries) >= MIN_TABLE_SIZE:
                candidates.append((addr, entries))
                addr = scan  # 跳过整张表
                continue
        addr += 4

    print("[scan] words scanned : %d" % n_words_scanned)
    print("[scan] thumb ptrs    : %d" % n_total_thumb_ptrs)
    print("[scan] table candidates (n>=%d): %d" %
          (MIN_TABLE_SIZE, len(candidates)))

    # 长度分布
    by_size = {}
    for _, ents in candidates:
        n = len(ents)
        by_size[n] = by_size.get(n, 0) + 1
    print("[scan] by size:")
    for n in sorted(by_size.keys()):
        print("  size=%2d : %4d 张表" % (n, by_size[n]))

    # 对每张表, 找 caller (有 ldr ref 指向表起点)
    out_dir = os.path.join(repo_root(), "temp")
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    csv_path = os.path.join(out_dir, "ghidra-state-tables.csv")
    f = open(csv_path, "w")
    f.write("table_addr,n_entries,n_callers,entries,callers\n")

    n_with_callers = 0
    n_all_named = 0
    n_some_named = 0
    n_none_named = 0

    for table_start, entries in candidates:
        ta = af.getAddress("0x%08x" % table_start)
        callers_set = set()
        for ref in rm.getReferencesTo(ta):
            from_addr = ref.getFromAddress()
            f_obj = fm.getFunctionContaining(from_addr)
            if f_obj is not None:
                callers_set.add((f_obj.getEntryPoint().getOffset() & 0xFFFFFFFF,
                                  f_obj.getName()))
        if callers_set:
            n_with_callers += 1

        # entry 命名状态
        entry_pairs = []
        named_count = 0
        for ep in entries:
            ep_addr = af.getAddress("0x%08x" % ep)
            f_obj = fm.getFunctionAt(ep_addr)
            if f_obj is None:
                # 也许是函数体内但没创建 Function
                f_obj = fm.getFunctionContaining(ep_addr)
            if f_obj is not None:
                nm = f_obj.getName()
            else:
                nm = "?"
            if nm and not (nm.startswith("FUN_") or nm.startswith("SUB_")
                           or nm.startswith("thunk_FUN_") or nm == "?"):
                named_count += 1
            entry_pairs.append((ep, nm))

        if named_count == len(entries):
            n_all_named += 1
        elif named_count > 0:
            n_some_named += 1
        else:
            n_none_named += 1

        # CSV 输出: entries 字段用 | 分隔, callers 字段同
        entries_str = "|".join("0x%08x:%s" % (a, n) for a, n in entry_pairs)
        callers_str = "|".join("0x%08x:%s" % (a, n) for a, n in sorted(callers_set))
        f.write("0x%08x,%d,%d,%s,%s\n" % (
            table_start, len(entries), len(callers_set),
            safe_csv(entries_str), safe_csv(callers_str)))
    f.close()

    print("[scan] tables with caller (有 ldr ref): %d / %d" %
          (n_with_callers, len(candidates)))
    print("[scan] entry naming status:")
    print("  all entries named   : %d" % n_all_named)
    print("  some entries named  : %d" % n_some_named)
    print("  no entries named    : %d" % n_none_named)
    print("  -> %s" % csv_path)


main()
