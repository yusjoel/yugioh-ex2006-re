# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# PromotePointerTableTargets.py
#
# 扫整个 ROM [0x08000000, 0x09FFFFFF] 的 4 字节对齐 word, 把"看起来像函数
# 指针 (Thumb/ARM) 且 target 已在 ROM 主代码段反汇编但未归属函数"的地址
# 提升为函数. 用于挖出函数指针表 (vtable / 状态表 / 回调) 里被间接调用、
# 没有 BL XREF 的函数.
#
# 函数指针判定 (target 必须落在 [0x080000C0, 0x084C7637]):
#   THUMB: 顶字节 0x08, bit0 = 1
#          target = (w & ~1), 偶对齐, 处指令长度 == 2
#   ARM:   顶字节 0x08, bit0 = 0, 4 字节对齐
#          target 处指令长度 == 4
#
# 候选必须:
#   - listing.getInstructionAt(target) != None     (已反汇编, 不在数据区)
#   - fm.getFunctionAt(target) == None              (还不是函数入口)
#   - fm.getFunctionContaining(target) == None      (不在既有函数体内)
#
# 命中即 createFunction(target, None). 纯增量, 不改既有函数, 不动未反汇编字节.
#
# 用法:
#   tools\asm-regen\ghidra-run-script.bat PromotePointerTableTargets.py [dry]

import jarray


ROM_LO = 0x08000000
ROM_HI = 0x09FFFFFF
CODE_LO = 0x080000C0
CODE_HI = 0x084C7637

CHUNK = 0x40000  # 256 KB / 块


RUN_DRY = False
try:
    _args = list(getScriptArgs())
    if _args and _args[0].lower() in ("dry", "--dry", "1", "true"):
        RUN_DRY = True
except Exception:
    pass


def main():
    af = currentProgram.getAddressFactory()
    space = af.getDefaultAddressSpace()
    listing = currentProgram.getListing()
    fm = currentProgram.getFunctionManager()
    mem = currentProgram.getMemory()

    thumb_created = 0
    arm_created   = 0
    candidate_thumb = 0   # word 模式匹配 Thumb 指针
    candidate_arm   = 0
    target_out_of_code = 0
    target_no_instr = 0
    target_in_func  = 0
    target_at_entry = 0
    mode_mismatch   = 0
    failed = 0

    # 已尝试过的 target, 防止同一个 target 被多张表多次 createFunction
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
        # 4-byte align
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
                # target 必须 落在 主代码段
                if target_int < CODE_LO or target_int > CODE_HI:
                    target_out_of_code += 1
                    continue
                # 同 target 去重
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

                # 模式 vs 指令长度
                if is_thumb and ti.getLength() != 2:
                    mode_mismatch += 1
                    seen_targets.add(target_int)
                    continue
                if (not is_thumb) and ti.getLength() != 4:
                    mode_mismatch += 1
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

    print("[done] PromotePointerTableTargets  (dry=%s)" % RUN_DRY)
    print("  candidates Thumb / ARM      = %d / %d" % (candidate_thumb, candidate_arm))
    print("  created    Thumb / ARM      = %d / %d  (total %d)" % (
        thumb_created, arm_created, thumb_created + arm_created))
    print("  skipped:")
    print("    target_out_of_code        = %d" % target_out_of_code)
    print("    target_at_entry (already) = %d" % target_at_entry)
    print("    target_in_func            = %d" % target_in_func)
    print("    target_no_instruction     = %d" % target_no_instr)
    print("    mode_mismatch             = %d" % mode_mismatch)
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
