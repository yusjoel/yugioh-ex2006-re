# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# PromoteCallTargetsToFunctions.py
#
# 扫所有指令, 把 bl/blx 调用目标里"已反汇编但还不是 Function 入口"的地址
# 提升为函数 (createFunction). 纯增量, 不删/不改既有函数.
#
# 跳过情况:
#   - 目标已经是某函数入口             (already_at_entry)
#   - 目标落在某个既有函数的 body 内    (inside_existing, 多半是 tail-merge / 嵌入跳转)
#   - 目标地址处没有指令               (no_instruction, 多半是数据)
#   - createFunction 抛异常 / 返 None  (failed)
#
# 用法:
#   tools\asm-regen\ghidra-run-script.bat PromoteCallTargetsToFunctions.py [dry]

from ghidra.program.model.symbol import SourceType


RUN_DRY = False
try:
    _args = list(getScriptArgs())
    if _args and _args[0].lower() in ("dry", "--dry", "1", "true"):
        RUN_DRY = True
except Exception:
    pass


def main():
    listing = currentProgram.getListing()
    fm = currentProgram.getFunctionManager()

    created = 0
    already_at_entry = 0
    inside_existing = 0
    no_instruction = 0
    failed = 0
    seen = set()
    samples_created = []
    samples_failed = []

    instr_iter = listing.getInstructions(True)
    for instr in instr_iter:
        mn = instr.getMnemonicString().lower()
        if mn not in ("bl", "blx"):
            continue
        for ref in instr.getReferencesFrom():
            rt = ref.getReferenceType()
            if not rt.isCall():
                continue
            target = ref.getToAddress()
            if target is None:
                continue
            key = target.getOffset()
            if key in seen:
                continue
            seen.add(key)

            if fm.getFunctionAt(target) is not None:
                already_at_entry += 1
                continue
            if fm.getFunctionContaining(target) is not None:
                inside_existing += 1
                continue
            if listing.getInstructionAt(target) is None:
                no_instruction += 1
                continue

            if RUN_DRY:
                created += 1
                if len(samples_created) < 20:
                    samples_created.append((target, instr.getAddress()))
                continue

            try:
                f = createFunction(target, None)
                if f is not None:
                    created += 1
                    if len(samples_created) < 20:
                        samples_created.append((target, instr.getAddress()))
                else:
                    failed += 1
                    if len(samples_failed) < 10:
                        samples_failed.append((target, instr.getAddress(), "None"))
            except Exception as e:
                failed += 1
                if len(samples_failed) < 10:
                    samples_failed.append((target, instr.getAddress(), str(e)))

    print("[done] PromoteCallTargetsToFunctions  (dry=%s)" % RUN_DRY)
    print("  unique BL targets = %d" % len(seen))
    print("  created           = %d" % created)
    print("  already at entry  = %d" % already_at_entry)
    print("  inside existing   = %d" % inside_existing)
    print("  no instruction    = %d" % no_instruction)
    print("  failed            = %d" % failed)
    if samples_created:
        print("  -- sample created (target  <-- caller) --")
        for t, c in samples_created[:10]:
            print("     %s  <--  %s" % (t, c))
    if samples_failed:
        print("  -- sample failed --")
        for t, c, msg in samples_failed:
            print("     %s  <--  %s  (%s)" % (t, c, msg))


main()
