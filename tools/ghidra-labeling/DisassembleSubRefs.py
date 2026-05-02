# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleSubRefs.py
#
# 反汇编那些被 bl 引用、但目标位置没有指令的地址 (linker 报 undefined SUB_xxxxxxxx)。
# 由 DisassembleHiddenFuncs.py 反汇编新函数后, 这些函数 bl 到的目标可能仍是 raw bytes。
# 本脚本对硬编码的 12 个 SUB_ 地址做 force-disassemble + createFunction。
#
# 目标地址来自构建错误 + grep 'SUB_' asm/all.s, 见仓库根 build.log 或运行:
#   grep -oE "SUB_[0-9a-f]{8}" asm/all.s | sort -u

from ghidra.app.cmd.disassemble import DisassembleCommand
from java.math import BigInteger


import re
import os

ASM_PATH = "asm/all.s"


def find_repo_root():
    cwd = os.getcwd()
    for cand in [cwd, os.path.dirname(cwd)]:
        if os.path.exists(os.path.join(cand, ASM_PATH)):
            return cand
    return cwd


def collect_sub_refs():
    """从 asm/all.s 收集所有 SUB_xxxxxxxx 引用 (linker undefined symbol)"""
    root = find_repo_root()
    path = os.path.join(root, ASM_PATH)
    refs = set()
    with open(path) as f:
        for line in f:
            for m in re.finditer(r"SUB_([0-9a-fA-F]{8})", line):
                refs.add(int(m.group(1), 16))
    return sorted(refs)


SUB_ADDRS = collect_sub_refs()


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def disasm_and_func(addr_int):
    addr = _addr(addr_int)
    listing = currentProgram.getListing()
    fm = currentProgram.getFunctionManager()

    if fm.getFunctionAt(addr) is not None:
        return "skip_already_func"

    cu = listing.getCodeUnitAt(addr)
    if cu is None or cu.getMnemonicString() == "??":
        prog_ctx = currentProgram.getProgramContext()
        tmode = prog_ctx.getRegister("TMode")
        if tmode is not None:
            try:
                prog_ctx.setValue(tmode, addr, addr, BigInteger.ONE)
            except Exception as e:
                return "fail_tmode_%s" % e
        cmd = DisassembleCommand(addr, None, True)  # 不限定 set, 让 Ghidra 跟随 flow
        if not cmd.applyTo(currentProgram):
            return "fail_disasm_%s" % cmd.getStatusMsg()

    f = createFunction(addr, None)
    if f is None:
        return "fail_create_function"
    return "ok"


def main():
    print("=== DisassembleSubRefs ===")
    stats = {}
    for addr in SUB_ADDRS:
        result = disasm_and_func(addr)
        print("  0x%08x: %s" % (addr, result))
        key = "ok" if result == "ok" else ("skip" if result.startswith("skip") else "fail")
        stats[key] = stats.get(key, 0) + 1
    print("\n[summary] %s" % stats)


main()
