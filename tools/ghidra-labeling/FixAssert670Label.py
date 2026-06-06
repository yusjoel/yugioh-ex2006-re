# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixAssert670Label.py — 修正 assert-carve 遗留 2 字节 byte-identical 回归
#   0x09e3c670 的 Ghidra 符号被遗留为裸 base 名 (无 _670 后缀), 导致 .word @0x0801a4f8
#   导出为 base 名 -> GAS 解析到 0x09e3b434 (base 串) 而非 0x09e3c670 (_670 串)。
#   assert_labels.csv / carve block 均意图 _670; 此处把 Ghidra 符号补回 _670 后缀。
#   仅 1 个符号改名; 恢复 byte-identical (SHA1 9689337d)。与 batch-2 无关 (独立 pre-existing bug)。
# Usage: tools\asm-regen\ghidra-run-script.bat FixAssert670Label.py [dry]
from ghidra.program.model.symbol import SourceType

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"): DRY = True
except Exception:
    pass

TARGET = 0x09e3c670
WRONG = "assert_anmid_ig2d_getanmsequencescoun"
RIGHT = "assert_anmid_ig2d_getanmsequencescoun_670"


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def main():
    st = currentProgram.getSymbolTable()
    a = _addr(TARGET)
    syms = list(st.getSymbols(a))
    print("=== FixAssert670Label (DRY=%s) @0x%08x ===" % (DRY, TARGET))
    target_sym = None
    for s in syms:
        print("  found: %s (primary=%s)" % (s.getName(), s.isPrimary()))
        if s.getName() == WRONG:
            target_sym = s
        elif s.getName() == RIGHT:
            print("  [already correct] %s present" % RIGHT)
    if target_sym is None:
        print("[FAIL] no symbol named %s @ target" % WRONG); return
    if DRY:
        print("[dry] would rename %s -> %s" % (WRONG, RIGHT)); return
    target_sym.setName(RIGHT, SourceType.USER_DEFINED)
    print("[ok] renamed -> %s" % RIGHT)


main()
