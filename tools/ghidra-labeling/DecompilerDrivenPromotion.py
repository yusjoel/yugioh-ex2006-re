# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DecompilerDrivenPromotion.py
#
# 对每个已识别函数跑反编译, 收集 pcode 里所有 CALL op 的目标地址.
# 命中下列严格条件就 createFunction:
#   - 目标在 [0x080000C0, 0x084C7637] 主代码段
#   - 已被反汇编 (getInstructionAt != None)
#   - 还不是函数入口 (getFunctionAt == None)
#   - 不在既有函数体内 (getFunctionContaining == None)
#   - target 处必须是 prologue:
#       THUMB:  halfword 0xB5xx
#       ARM:    word 0xE92Dxxxx 且 bit 14 set
#
# 收益主要在: switch dispatch 的 case target / 函数指针经寄存器中转后调用 /
# 尾调用 b/bx 的目标. 静态分析器漏掉的、但 decompiler 通过常量传播能解析的.
#
# 用法:
#   tools\asm-regen\ghidra-run-script.bat DecompilerDrivenPromotion.py [dry] [limit=N]
#
#   limit=N  对全部函数做等距抽样 N 个 (用于 pilot)
#   dry      只 report 不 createFunction

from ghidra.app.decompiler import DecompInterface, DecompileOptions
from ghidra.util.task import ConsoleTaskMonitor
from ghidra.program.model.pcode import PcodeOp


CODE_LO = 0x080000C0
CODE_HI = 0x084C7637
DECOMP_TIMEOUT = 60  # 每函数最长 60 秒


def parse_args():
    dry = False
    limit = 0
    try:
        for a in list(getScriptArgs()):
            la = a.lower()
            if la in ("dry", "--dry"):
                dry = True
            elif la.startswith("limit="):
                limit = int(la.split("=", 1)[1])
            elif la.startswith("--limit="):
                limit = int(la.split("=", 1)[1])
            elif la.isdigit():
                limit = int(la)
    except Exception:
        pass
    return dry, limit


def is_thumb_prologue(mem, target):
    try:
        hw = mem.getShort(target) & 0xFFFF
        return (hw & 0xFF00) == 0xB500
    except Exception:
        return False


def is_arm_prologue(mem, target):
    try:
        w = mem.getInt(target) & 0xFFFFFFFF
        return (w & 0xFFFF0000) == 0xE92D0000 and (w & 0x4000) == 0x4000
    except Exception:
        return False


def main():
    dry, limit = parse_args()

    fm = currentProgram.getFunctionManager()
    listing = currentProgram.getListing()
    mem = currentProgram.getMemory()

    all_funcs = []
    it = fm.getFunctions(True)
    while it.hasNext():
        all_funcs.append(it.next())
    n_total = len(all_funcs)

    if limit > 0 and limit < n_total:
        stride = n_total // limit
        sample = [all_funcs[i * stride] for i in range(limit)]
    else:
        sample = all_funcs
        limit = n_total

    print("== DecompilerDrivenPromotion ==")
    print("  total funcs       = %d" % n_total)
    print("  sample size       = %d  (stride=%d)" % (len(sample), n_total // limit if limit else 1))
    print("  dry               = %s" % dry)
    print("  decomp timeout    = %d s/func" % DECOMP_TIMEOUT)

    decomp = DecompInterface()
    decomp.setOptions(DecompileOptions())
    decomp.openProgram(currentProgram)
    monitor = ConsoleTaskMonitor()

    counts = {
        "decomp_ok": 0, "decomp_fail": 0,
        "call_ops": 0, "unique_targets": 0,
        "out_of_range": 0, "already_function": 0,
        "in_existing_func": 0, "no_instruction": 0,
        "mode_mismatch": 0, "no_prologue": 0,
        "created": 0, "create_failed": 0,
    }
    seen = set()
    samples_created = []
    samples_no_proto = []

    for idx, func in enumerate(sample):
        try:
            res = decomp.decompileFunction(func, DECOMP_TIMEOUT, monitor)
        except Exception:
            counts["decomp_fail"] += 1
            continue
        if res is None or not res.decompileCompleted():
            counts["decomp_fail"] += 1
            continue
        counts["decomp_ok"] += 1
        high = res.getHighFunction()
        if high is None:
            continue

        op_iter = high.getPcodeOps()
        while op_iter.hasNext():
            op = op_iter.next()
            if op.getOpcode() != PcodeOp.CALL:
                continue
            counts["call_ops"] += 1
            target_vn = op.getInput(0)
            if target_vn is None or not target_vn.isAddress():
                continue
            target_addr = target_vn.getAddress()
            target_int = target_addr.getOffset() & 0xFFFFFFFF

            if target_int in seen:
                continue
            seen.add(target_int)
            counts["unique_targets"] += 1

            if target_int < CODE_LO or target_int > CODE_HI:
                counts["out_of_range"] += 1
                continue
            if fm.getFunctionAt(target_addr) is not None:
                counts["already_function"] += 1
                continue
            if fm.getFunctionContaining(target_addr) is not None:
                counts["in_existing_func"] += 1
                continue
            ti = listing.getInstructionAt(target_addr)
            if ti is None:
                counts["no_instruction"] += 1
                continue

            ilen = ti.getLength()
            if ilen == 2:
                if not is_thumb_prologue(mem, target_addr):
                    counts["no_prologue"] += 1
                    if len(samples_no_proto) < 5:
                        samples_no_proto.append((target_int,
                                                 func.getEntryPoint().getOffset() & 0xFFFFFFFF,
                                                 ti.getMnemonicString()))
                    continue
            elif ilen == 4:
                if not is_arm_prologue(mem, target_addr):
                    counts["no_prologue"] += 1
                    if len(samples_no_proto) < 5:
                        samples_no_proto.append((target_int,
                                                 func.getEntryPoint().getOffset() & 0xFFFFFFFF,
                                                 ti.getMnemonicString()))
                    continue
            else:
                counts["mode_mismatch"] += 1
                continue

            if dry:
                counts["created"] += 1
                if len(samples_created) < 30:
                    samples_created.append((target_int,
                                            func.getEntryPoint().getOffset() & 0xFFFFFFFF))
                continue

            try:
                created_f = createFunction(target_addr, None)
                if created_f is not None:
                    counts["created"] += 1
                    if len(samples_created) < 30:
                        samples_created.append((target_int,
                                                func.getEntryPoint().getOffset() & 0xFFFFFFFF))
                else:
                    counts["create_failed"] += 1
            except Exception:
                counts["create_failed"] += 1

    decomp.dispose()

    print("\n[done] DecompilerDrivenPromotion (dry=%s)" % dry)
    print("  decomp ok / fail  = %d / %d" % (counts["decomp_ok"], counts["decomp_fail"]))
    print("  CALL ops          = %d" % counts["call_ops"])
    print("  unique targets    = %d" % counts["unique_targets"])
    print("  filter:")
    print("    out_of_range      = %d" % counts["out_of_range"])
    print("    already_function  = %d" % counts["already_function"])
    print("    in_existing_func  = %d" % counts["in_existing_func"])
    print("    no_instruction    = %d" % counts["no_instruction"])
    print("    mode_mismatch     = %d" % counts["mode_mismatch"])
    print("    no_prologue       = %d" % counts["no_prologue"])
    print("  ----")
    print("  CREATED           = %d" % counts["created"])
    print("  create_failed     = %d" % counts["create_failed"])
    if samples_created:
        print("  -- sample created (target  <--  caller) --")
        for t, c in samples_created[:15]:
            print("     0x%08x  <--  0x%08x" % (t, c))
    if samples_no_proto:
        print("  -- sample no_prologue (说明 decomp 看到了 call 但 target 没序言) --")
        for t, c, mn in samples_no_proto:
            print("     0x%08x  <--  0x%08x  (first instr: %s)" % (t, c, mn))


main()
