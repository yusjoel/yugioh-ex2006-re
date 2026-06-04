# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RenameAssertPreexisting.py — 把 2 个 pre-existing 断言串 label 统一为 my-scheme 名,
#   使其与 rom.s carve 块的 label 一致 (code .word 经 resolve_word_symbol 用 carve label,
#   rom_data.inc 不再残留旧名)。
#   0x09e398ec: gl_bright_assert      -> assert_bright_16_bright_16
#   0x09e3b434: nns_g2d_assert_anmID  -> assert_anmid_ig2d_getanmsequencescoun
# Usage: tools\asm-regen\ghidra-run-script.bat RenameAssertPreexisting.py [dry]
from ghidra.program.model.symbol import SourceType

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

RENAMES = [
    (0x09e398ec, "assert_bright_16_bright_16"),
    (0x09e3b434, "assert_anmid_ig2d_getanmsequencescoun"),
]


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def main():
    print("=== RenameAssertPreexisting (DRY=%s) ===" % DRY)
    for addr_int, newname in RENAMES:
        a = _addr(addr_int)
        sym = getSymbolAt(a)
        if sym is None:
            print("[FAIL] no symbol @ 0x%08x" % addr_int)
            continue
        old = sym.getName()
        if old == newname:
            print("[skip] 0x%08x already %s" % (addr_int, newname))
            continue
        if DRY:
            print("[dry] 0x%08x %s -> %s" % (addr_int, old, newname))
            continue
        sym.setName(newname, SourceType.USER_DEFINED)
        print("[ok] 0x%08x %s -> %s" % (addr_int, old, newname))
    print("[done]")


main()
