# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FindFunctionPrologues.py
#
# 在 ROM main code 范围 [0x080000C0, 0x084C7637] 内扫描"已反汇编但尚未归属
# 函数"的指令, 命中下列序言模式即提升为函数:
#
#   THUMB push {..., lr}        halfword pattern  0xB5xx
#   ARM   stmfd sp!, {..., lr}  word     pattern  0xE92Dxxxx 且 (xxxx & 0x4000)==0x4000
#
# 候选必须:
#   - 已被反汇编 (getInstructionAt != None)
#   - 不在任何已有函数体内 (含入口) (getFunctionContaining == None)
#   - 长度 / 对齐与模式一致 (THUMB len=2 偶对齐, ARM len=4 4字节对齐)
#
# 纯增量, 不改既有函数. 不去碰未反汇编的字节 (避免在数据区瞎插函数).
#
# 用法:
#   tools\asm-regen\ghidra-run-script.bat FindFunctionPrologues.py [dry]

from ghidra.program.model.address import AddressSet


RANGE_LO = 0x080000C0
RANGE_HI = 0x084C7637


RUN_DRY = False
try:
    _args = list(getScriptArgs())
    if _args and _args[0].lower() in ("dry", "--dry", "1", "true"):
        RUN_DRY = True
except Exception:
    pass


def main():
    af = currentProgram.getAddressFactory()
    listing = currentProgram.getListing()
    fm = currentProgram.getFunctionManager()
    mem = currentProgram.getMemory()

    addr_lo = af.getAddress("0x%08x" % RANGE_LO)
    addr_hi = af.getAddress("0x%08x" % RANGE_HI)
    aset = AddressSet(addr_lo, addr_hi)

    thumb_created = 0
    arm_created = 0
    skipped_in_func = 0
    skipped_align = 0
    failed = 0
    sample_thumb = []
    sample_arm = []

    instr_iter = listing.getInstructions(aset, True)
    for instr in instr_iter:
        addr = instr.getAddress()
        addr_int = addr.getOffset()
        ilen = instr.getLength()

        if fm.getFunctionContaining(addr) is not None:
            skipped_in_func += 1
            continue

        try:
            if ilen == 2:
                if (addr_int & 1) != 0:
                    skipped_align += 1
                    continue
                hw = mem.getShort(addr) & 0xFFFF
                if (hw & 0xFF00) != 0xB500:
                    continue
                if RUN_DRY:
                    thumb_created += 1
                    if len(sample_thumb) < 15:
                        sample_thumb.append(addr_int)
                    continue
                f = createFunction(addr, None)
                if f is not None:
                    thumb_created += 1
                    if len(sample_thumb) < 15:
                        sample_thumb.append(addr_int)
                else:
                    failed += 1
            elif ilen == 4:
                if (addr_int & 3) != 0:
                    skipped_align += 1
                    continue
                w = mem.getInt(addr) & 0xFFFFFFFF
                if (w & 0xFFFF0000) != 0xE92D0000:
                    continue
                if (w & 0x00004000) == 0:
                    continue
                if RUN_DRY:
                    arm_created += 1
                    if len(sample_arm) < 15:
                        sample_arm.append(addr_int)
                    continue
                f = createFunction(addr, None)
                if f is not None:
                    arm_created += 1
                    if len(sample_arm) < 15:
                        sample_arm.append(addr_int)
                else:
                    failed += 1
        except Exception as e:
            failed += 1

    total_created = thumb_created + arm_created
    print("[done] FindFunctionPrologues  (dry=%s)" % RUN_DRY)
    print("  THUMB push{...,lr} = %d" % thumb_created)
    print("  ARM   stmfd!{,lr}  = %d" % arm_created)
    print("  total created      = %d" % total_created)
    print("  skipped in_func    = %d" % skipped_in_func)
    print("  skipped align      = %d" % skipped_align)
    print("  failed             = %d" % failed)
    if sample_thumb:
        print("  -- sample THUMB --")
        for a in sample_thumb:
            print("     0x%08x" % a)
    if sample_arm:
        print("  -- sample ARM --")
        for a in sample_arm:
            print("     0x%08x" % a)


main()
