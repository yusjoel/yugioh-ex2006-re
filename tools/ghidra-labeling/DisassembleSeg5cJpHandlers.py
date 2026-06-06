# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleSeg5cJpHandlers.py — p5 Seg-5c-ii (R4)
#   反汇编 0x170d4..0x171d0 (252B = 74 个 SJIS code->idx handler stubs, 各 4B:
#   `movs r0,#N; b 0x171d2`)。这是被 jp_char_handler_jump_table (0x16b88) 引用的 live code,
#   Ghidra 误标为 ROM_INCBIN。disasm 后消除 incbin (Rule 2)。NOT createFunction (跳转表目标, 非 bl 函数)。
#   备份: .rep.bak-20260606-180000-pre-seg5c
from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.address import AddressSet
from java.math import BigInteger

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"): DRY = True
except Exception:
    pass

LO = 0x080170d4
HI = 0x080171cf  # 0x170d4 + 0xfc - 1


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def main():
    print("=== DisassembleSeg5cJpHandlers (DRY=%s) 0x%08x..0x%08x ===" % (DRY, LO, HI))
    lo = _addr(LO); hi = _addr(HI)
    listing = currentProgram.getListing()

    if DRY:
        print("[dry] would clearListing(whole) + setTMode=THUMB + per-stub DisassembleCommand"); return

    # 1) 先清整个 range (含已 disasm 的首 stub), 否则 setTMode 与现有指令冲突
    try:
        clearListing(lo, hi)
    except Exception as e:
        print("[warn] clearListing whole: %s" % e)

    # 2) 整 range 设 TMode=1 (现在全是 data, 无冲突)
    ctx = currentProgram.getProgramContext()
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        ctx.setValue(tmode, lo, hi, BigInteger.ONE)

    # 3) 每个 stub = 4B (movs r0,#N; b 0x171d2). 逐 stub disasm (跳转表目标, 非 fall-through)。
    a = LO
    while a <= HI:
        sa = _addr(a)
        cmd = DisassembleCommand(sa, AddressSet(sa, _addr(a + 3)), True)
        if not cmd.applyTo(currentProgram):
            print("[warn] disasm 0x%08x: %s" % (a, cmd.getStatusMsg()))
        a += 4

    # count
    n = 0
    inst = listing.getInstructionAt(lo)
    while inst is not None and inst.getAddress().compareTo(hi) <= 0:
        n += 1
        inst = listing.getInstructionAfter(inst.getAddress())
    print("[done] %d instructions in 0x%08x..0x%08x" % (n, LO, HI))


main()
