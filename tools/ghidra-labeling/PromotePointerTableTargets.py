# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# PromotePointerTableTargets.py  (strict prologue-required version)
#
# 扫整个 ROM [0x08000000, 0x09FFFFFF] 的 4 字节对齐 word, 把"看起来像
# 函数指针, 且 target 同时满足下列所有条件"的地址提升为函数:
#
#   1) target 落在 [0x080000C0, 0x084C7637] 主代码段
#   2) target 已被反汇编 (getInstructionAt != None)
#   3) target 不在既有函数体内 (getFunctionContaining == None)
#   4) target 处指令长度与指针模式一致 (THUMB=2 / ARM=4)
#   5) ★ target 处必须是 prologue:
#         THUMB:  halfword 模式 0xB5xx       (push {..., lr})
#         ARM:    word     模式 0xE92Dxxxx   且 bit 14 set (stmfd sp! {..., lr})
#
# 加 (5) 是为了规避 v1 的核心坑: target 在某段已反汇编但未归属函数的
# orphan 代码里 (典型: IRQ handler 尾段), 仅靠 (3) 不能确认 target 真是
# 函数入口. 加上 prologue 检查后, 8 个 ARM IRQ handler 的中段误升不再发生.
#
# 用法:
#   tools\asm-regen\ghidra-run-script.bat PromotePointerTableTargets.py [dry]

import jarray


ROM_LO = 0x08000000
ROM_HI = 0x09FFFFFF
CODE_LO = 0x080000C0
CODE_HI = 0x084C7637

CHUNK = 0x40000


RUN_DRY = False
try:
    _args = list(getScriptArgs())
    if _args and _args[0].lower() in ("dry", "--dry", "1", "true"):
        RUN_DRY = True
except Exception:
    pass


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
    af = currentProgram.getAddressFactory()
    space = af.getDefaultAddressSpace()
    listing = currentProgram.getListing()
    fm = currentProgram.getFunctionManager()
    mem = currentProgram.getMemory()

    thumb_created = 0
    arm_created   = 0
    candidate_thumb = 0
    candidate_arm   = 0
    target_out_of_code = 0
    target_no_instr = 0
    target_in_func  = 0
    target_at_entry = 0
    mode_mismatch   = 0
    not_prologue    = 0
    failed = 0

    seen_targets = set()
    sample_thumb = []
    sample_arm = []

    for block in mem.getBlocks():
        if not block.isInitialized():
            continue
        bstart = block.getStart().getOffset() & 0xFFFFFFFF
        bend   = block.getEnd().getOffset() & 0xFFFFFFFF
        if bend < ROM_LO or bstart > ROM_HI:
            continue
        scan_lo = max(bstart, ROM_LO)
        scan_hi = min(bend, ROM_HI)
        if scan_lo & 3:
            scan_lo = (scan_lo + 3) & ~3

        cur = scan_lo
        while cur < scan_hi:
            sz = min(CHUNK, (scan_hi + 1) - cur)
            sz &= ~3
            if sz == 0:
                break
            addr = space.getAddress(cur)
            buf = jarray.zeros(sz, 'b')
            try:
                n = mem.getBytes(addr, buf)
            except Exception:
                cur += sz
                continue
            n &= ~3
            for i in range(0, n, 4):
                b3 = buf[i + 3] & 0xFF
                if b3 != 0x08:
                    continue
                b0 = buf[i] & 0xFF
                b1 = buf[i + 1] & 0xFF
                b2 = buf[i + 2] & 0xFF
                w = b0 | (b1 << 8) | (b2 << 16) | (b3 << 24)

                is_thumb = (w & 1) == 1
                target_int = w & ~1
                if not is_thumb and (target_int & 3) != 0:
                    continue
                if target_int < CODE_LO or target_int > CODE_HI:
                    target_out_of_code += 1
                    continue
                if target_int in seen_targets:
                    continue

                if is_thumb:
                    candidate_thumb += 1
                else:
                    candidate_arm += 1

                target = space.getAddress(target_int)
                if fm.getFunctionAt(target) is not None:
                    target_at_entry += 1
                    seen_targets.add(target_int)
                    continue
                if fm.getFunctionContaining(target) is not None:
                    target_in_func += 1
                    seen_targets.add(target_int)
                    continue
                ti = listing.getInstructionAt(target)
                if ti is None:
                    target_no_instr += 1
                    seen_targets.add(target_int)
                    continue

                if is_thumb and ti.getLength() != 2:
                    mode_mismatch += 1
                    seen_targets.add(target_int)
                    continue
                if (not is_thumb) and ti.getLength() != 4:
                    mode_mismatch += 1
                    seen_targets.add(target_int)
                    continue

                # ★ 新增: target 必须是 prologue
                if is_thumb:
                    if not is_thumb_prologue(mem, target):
                        not_prologue += 1
                        seen_targets.add(target_int)
                        continue
                else:
                    if not is_arm_prologue(mem, target):
                        not_prologue += 1
                        seen_targets.add(target_int)
                        continue

                seen_targets.add(target_int)

                if RUN_DRY:
                    if is_thumb:
                        thumb_created += 1
                        if len(sample_thumb) < 15:
                            sample_thumb.append((target_int, cur + i))
                    else:
                        arm_created += 1
                        if len(sample_arm) < 15:
                            sample_arm.append((target_int, cur + i))
                    continue

                try:
                    f = createFunction(target, None)
                    if f is not None:
                        if is_thumb:
                            thumb_created += 1
                            if len(sample_thumb) < 15:
                                sample_thumb.append((target_int, cur + i))
                        else:
                            arm_created += 1
                            if len(sample_arm) < 15:
                                sample_arm.append((target_int, cur + i))
                    else:
                        failed += 1
                except Exception:
                    failed += 1

            cur += n if n > 0 else sz

    print("[done] PromotePointerTableTargets (strict prologue)  (dry=%s)" % RUN_DRY)
    print("  candidates Thumb / ARM      = %d / %d" % (candidate_thumb, candidate_arm))
    print("  created    Thumb / ARM      = %d / %d  (total %d)" % (
        thumb_created, arm_created, thumb_created + arm_created))
    print("  skipped:")
    print("    target_out_of_code        = %d" % target_out_of_code)
    print("    target_at_entry (already) = %d" % target_at_entry)
    print("    target_in_func            = %d" % target_in_func)
    print("    target_no_instruction     = %d" % target_no_instr)
    print("    mode_mismatch             = %d" % mode_mismatch)
    print("    not_prologue (NEW filter) = %d  <- v1 在这步全部漏过" % not_prologue)
    print("    failed                    = %d" % failed)
    if sample_thumb:
        print("  -- sample THUMB target  <--  pointer source --")
        for t, src in sample_thumb:
            print("     0x%08x  <--  0x%08x" % (t, src))
    if sample_arm:
        print("  -- sample ARM target  <--  pointer source --")
        for t, src in sample_arm:
            print("     0x%08x  <--  0x%08x" % (t, src))


main()
