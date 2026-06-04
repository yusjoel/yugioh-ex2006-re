# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# PocDataEquate.py  — 验证字面量池数值常量 data-equate 机制 (单槽 POC)
#   slot 0x08014060 (.word 0xfffffe01):
#     (1) 重命名符号 DAT_08014060 -> tick_demo_scene_state_machine_demo_clear_bits_8_1
#     (2) 设 equate DEMO_CLEAR_BITS_8_1=0xfffffe01 于该数据地址 op0
#   预期重导出: ldr r1, tick_..._demo_clear_bits_8_1 / .word DEMO_CLEAR_BITS_8_1
# Usage: tools\asm-regen\ghidra-run-script.bat PocDataEquate.py [dry]

from ghidra.program.model.symbol import SourceType

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

ADDR = 0x08014060
NEW_LABEL = "tick_demo_scene_state_machine_demo_clear_bits_8_1"
EQ_NAME = "DEMO_CLEAR_BITS_8_1"
EQ_VALUE = 0xfffffe01


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def main():
    print("=== PocDataEquate (DRY=%s) ===" % DRY)
    a = _addr(ADDR)
    d = getDataAt(a)
    print("data @ 0x%08x = %s (len=%s)" % (ADDR, d, d.getLength() if d else None))
    if DRY:
        print("[dry] would rename -> %s + equate %s=0x%x" % (NEW_LABEL, EQ_NAME, EQ_VALUE))
        return
    # (1) label rename
    createLabel(a, NEW_LABEL, True, SourceType.USER_DEFINED)
    print("[ok] label @ 0x%08x -> %s" % (ADDR, NEW_LABEL))
    # (2) data equate
    et = currentProgram.getEquateTable()
    eq = et.getEquate(EQ_NAME)
    if eq is None:
        eq = et.createEquate(EQ_NAME, EQ_VALUE)
    eq.addReference(a, 0)
    print("[ok] equate %s=0x%x @ 0x%08x op0" % (EQ_NAME, EQ_VALUE, ADDR))
    print("[done] PocDataEquate")


main()
