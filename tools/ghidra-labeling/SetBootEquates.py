# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# SetBootEquates.py  (Jython 2.7 / Ghidra 12.x)
#
# 给 boot/IRQ 区的 CPSR 模式立即数设 equate, 使 ExportRangeToGas.apply_equates
# 把 #0x12/#0x1f 导出为 #PSR_IRQ_MODE/#PSR_SYS_MODE。
# GAS 端靠 constants/arm_psr.inc 的 .set 解析回同值 -> byte-identical。
#
# Usage: tools\asm-regen\ghidra-run-script.bat SetBootEquates.py [dry]

from ghidra.program.model.scalar import Scalar

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

# (addr, equate_name, value)
EQUATES = [
    (0x080000c0, "PSR_IRQ_MODE", 0x12),   # init_cpu: mov r0,#0x12
    (0x080000cc, "PSR_SYS_MODE", 0x1f),   # init_cpu: mov r0,#0x1f
    (0x080001dc, "PSR_SYS_MODE", 0x1f),   # IntrMain: orr r3,r3,#0x1f (切 System 模式)
]


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def find_scalar_op(ins, value):
    for i in range(ins.getNumOperands()):
        for obj in ins.getOpObjects(i):
            if isinstance(obj, Scalar):
                if (obj.getValue() & 0xffffffff) == (value & 0xffffffff):
                    return i
    return -1


def main():
    print("=== SetBootEquates (DRY=%s) ===" % DRY)
    et = currentProgram.getEquateTable()
    for addr_int, name, value in EQUATES:
        a = _addr(addr_int)
        ins = getInstructionAt(a)
        if ins is None:
            print("[FAIL] no instruction @ 0x%08x" % addr_int)
            continue
        opi = find_scalar_op(ins, value)
        if opi < 0:
            print("[FAIL] 0x%08x has no scalar 0x%x (text=%s)" % (addr_int, value, ins.toString()))
            continue
        if DRY:
            print("[dry]  equate %s=0x%x @ 0x%08x op%d (%s)" % (name, value, addr_int, opi, ins.toString()))
            continue
        eq = et.getEquate(name)
        if eq is None:
            eq = et.createEquate(name, value)
        eq.addReference(a, opi)
        print("[ok]   equate %s=0x%x @ 0x%08x op%d" % (name, value, addr_int, opi))
    print("[done] SetBootEquates (DRY=%s)" % DRY)


main()
