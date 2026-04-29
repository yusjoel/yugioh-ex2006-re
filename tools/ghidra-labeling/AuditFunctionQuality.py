# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# AuditFunctionQuality.py
#
# 给每个函数打 "真实度" 标签:
#   prologue:  首指令是 push {...,lr}(THUMB) 或 stmfd sp!{...,lr}(ARM)
#   has_call:  有 RefType.isCall() 类型的 XREF (即被 bl/blx 调用)
#   has_data:  有非 call XREF (函数指针表 / vtable / 字面量)
#
# 桶:
#   solid          prologue=Y  has_call=Y     真函数, 有 BL caller
#   ptr_likely     prologue=Y  has_call=N has_data=Y    通过指针调用的真函数
#   no_proto_call  prologue=N  has_call=Y     被 bl 但无序言(尾调用 / 非常规)
#   no_proto_ptr   prologue=N  has_call=N has_data=Y    *最可疑*: 没序言, 仅数据引用
#                                                       (大概率原本是函数内 LAB_xxx
#                                                        被 pointer scan 误升)
#   orphan         prologue=?  无任何 XREF
#
# 输出:
#   - stdout 各桶计数
#   - temp/ghidra-funcs-suspicious.txt   no_proto_ptr 桶完整地址清单
#   - temp/ghidra-funcs-by-bucket.csv    每个函数一行 (addr,name,bucket,length,callers,data_refs)
#
# 用法:
#   tools\asm-regen\ghidra-run-script.bat AuditFunctionQuality.py

import os

from ghidra.program.model.symbol import RefType


CODE_LO = 0x080000C0
CODE_HI = 0x084C7637


def is_prologue(instr, mem):
    if instr is None:
        return False
    addr = instr.getAddress()
    ilen = instr.getLength()
    try:
        if ilen == 2:
            hw = mem.getShort(addr) & 0xFFFF
            return (hw & 0xFF00) == 0xB500
        elif ilen == 4:
            w = mem.getInt(addr) & 0xFFFFFFFF
            return (w & 0xFFFF4000) == 0xE92D4000
    except Exception:
        return False
    return False


def repo_root():
    try:
        src = getSourceFile().getAbsolutePath()
        return os.path.dirname(os.path.dirname(os.path.dirname(src)))
    except Exception:
        return os.getcwd()


def main():
    listing = currentProgram.getListing()
    fm = currentProgram.getFunctionManager()
    rm = currentProgram.getReferenceManager()
    mem = currentProgram.getMemory()

    counts = {
        "solid": 0,
        "ptr_likely": 0,
        "no_proto_call": 0,
        "no_proto_ptr": 0,
        "orphan": 0,
        "out_of_range": 0,
        "named_skipped": 0,
    }
    sus_list = []
    rows = []

    funcs = fm.getFunctions(True)
    for f in funcs:
        ep = f.getEntryPoint()
        addr_int = ep.getOffset() & 0xFFFFFFFF
        if addr_int < CODE_LO or addr_int > CODE_HI:
            counts["out_of_range"] += 1
            continue
        name = f.getName()

        instr = listing.getInstructionAt(ep)
        proto = is_prologue(instr, mem)

        has_call = False
        has_data = False
        n_callers = 0
        n_data = 0
        for ref in rm.getReferencesTo(ep):
            rt = ref.getReferenceType()
            if rt.isCall():
                has_call = True
                n_callers += 1
            else:
                has_data = True
                n_data += 1

        if proto and has_call:
            bucket = "solid"
        elif proto and has_data:
            bucket = "ptr_likely"
        elif (not proto) and has_call:
            bucket = "no_proto_call"
        elif (not proto) and has_data:
            bucket = "no_proto_ptr"
            sus_list.append((addr_int, name, n_callers, n_data, instr))
        else:
            bucket = "orphan"

        counts[bucket] += 1
        rows.append((addr_int, name, bucket, n_callers, n_data, proto))

    print("[done] AuditFunctionQuality")
    print("  range = [0x%08x, 0x%08x]" % (CODE_LO, CODE_HI))
    total = sum(counts.values()) - counts["out_of_range"]
    print("  total in range  = %d" % total)
    print("  out_of_range    = %d" % counts["out_of_range"])
    print("  ----")
    print("  solid           = %d  (prologue + BL caller)" % counts["solid"])
    print("  ptr_likely      = %d  (prologue + 仅数据 XREF, 函数指针调用)" % counts["ptr_likely"])
    print("  no_proto_call   = %d  (无 prologue 但有 BL caller, 尾调用/非常规)" % counts["no_proto_call"])
    print("  no_proto_ptr    = %d  *可疑*: 无 prologue, 仅数据 XREF" % counts["no_proto_ptr"])
    print("  orphan          = %d  (无任何 XREF)" % counts["orphan"])

    out_dir = os.path.join(repo_root(), "temp")
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    sus_path = os.path.join(out_dir, "ghidra-funcs-suspicious.txt")
    fsus = open(sus_path, "w")
    fsus.write("# no_proto_ptr  (无 prologue + 仅数据 XREF, 高度疑似 pointer-scan 误升)\n")
    fsus.write("# format: addr  name  callers  data_refs  first_instr\n")
    for addr_int, name, nc, nd, instr in sorted(sus_list):
        instr_repr = ""
        if instr is not None:
            instr_repr = "%s %s" % (instr.getMnemonicString(),
                                    instr.getDefaultOperandRepresentation(0) if instr.getNumOperands() > 0 else "")
        fsus.write("0x%08x  %-32s  callers=%d  data=%d  | %s\n" % (
            addr_int, name, nc, nd, instr_repr))
    fsus.close()
    print("  -> %s  (%d entries)" % (sus_path, len(sus_list)))

    csv_path = os.path.join(out_dir, "ghidra-funcs-by-bucket.csv")
    fcsv = open(csv_path, "w")
    fcsv.write("address,name,bucket,callers,data_refs,prologue\n")
    for addr_int, name, bucket, nc, nd, proto in rows:
        fcsv.write("0x%08x,%s,%s,%d,%d,%d\n" % (
            addr_int, name, bucket, nc, nd, 1 if proto else 0))
    fcsv.close()
    print("  -> %s" % csv_path)


main()
