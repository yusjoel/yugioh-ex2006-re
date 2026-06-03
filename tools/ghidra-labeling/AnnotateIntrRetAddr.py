# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# AnnotateIntrRetAddr.py  (Jython 2.7 / Ghidra 12.x)
#
# 修正 IntrMain 返回尾段:
#   1) 反汇编 0x080001fc (Ghidra 误标为 .word 0xe8bd4000, 实为 ldmia sp!,{lr})
#      —— 它是 Thumb ISR 经 dispatch_thumb_isr_from_arm(adr lr) 返回的入口,
#      与已有的 0x200..0x220 恢复代码相连
#   2) 反汇编 0x08000224/0x08000228 两条对齐填充 nop (mov r0,r0 / e1a00000)
#   3) rename LAB_080001fc -> IntrMain_RetAddr (pokeruby 同名)
#   4) 加 plate 注释
#
# 备份: 调用前已 cp .rep 到 .bak-<ts>-pre-intr-retaddr
# Usage: tools\asm-regen\ghidra-run-script.bat AnnotateIntrRetAddr.py [dry]

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.address import AddressSet
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import SourceType
from java.lang import Exception as JavaException
from java.math import BigInteger

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

PLATE = (
    u"IntrMain 返回入口. Thumb ISR (经 dispatch_thumb_isr_from_arm 的 "
    u"adr lr) 执行完返回到此: ldmia 弹出 lr; 恢复 CPSR 回 IRQ 模式"
    u"(0x92=I_BIT|IRQ_MODE); ldmia 还原 r0-r3/lr; 写回 REG_IE/REG_IME; "
    u"恢复 SPSR; bx lr 返回 BIOS. 其后 0x224 两条 mov r0,r0 为对齐填充, "
    u"再后为 init_cpu/IntrMain 的字面量池 (ptr_intr_vector/ptr_run_game_main/ptr_gIntrTable)."
)


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def disasm_arm(lo_int, hi_int, label):
    lo = _addr(lo_int)
    hi = _addr(hi_int)
    ctx = currentProgram.getProgramContext()
    tmode = ctx.getRegister("TMode")
    if not DRY:
        try:
            clearListing(lo, hi)
        except (JavaException, Exception) as e:
            print("[warn] clearListing %s: %s" % (label, e))
        if tmode is not None:
            try:
                ctx.setValue(tmode, lo, hi, BigInteger.ZERO)
            except (JavaException, Exception) as e:
                print("[warn] setTMode %s: %s" % (label, e))
        cmd = DisassembleCommand(lo, AddressSet(lo, hi), True)
        if cmd.applyTo(currentProgram):
            print("[ok]   disasm ARM %s (0x%08x..0x%08x)" % (label, lo_int, hi_int))
        else:
            print("[FAIL] disasm %s: %s" % (label, cmd.getStatusMsg()))
    else:
        print("[dry]  disasm ARM %s (0x%08x..0x%08x)" % (label, lo_int, hi_int))


def main():
    print("=== AnnotateIntrRetAddr (DRY=%s) ===" % DRY)

    # 1) 反汇编 0x1fc (单条 ldmia sp!,{lr}); 与已有 0x200 代码相连
    disasm_arm(0x080001fc, 0x080001ff, "IntrMain_RetAddr@0x1fc")
    # 2) 反汇编 0x224/0x228 两条 nop
    disasm_arm(0x08000224, 0x0800022b, "align nops @0x224")

    # 3) rename label
    a = _addr(0x080001fc)
    st = currentProgram.getSymbolTable()
    sym = st.getPrimarySymbol(a)
    if sym is None:
        if not DRY:
            createLabel(a, "IntrMain_RetAddr", True, SourceType.USER_DEFINED)
            print("[ok]   create label IntrMain_RetAddr @ 0x080001fc")
        else:
            print("[dry]  create label IntrMain_RetAddr @ 0x080001fc")
    elif sym.getName() != "IntrMain_RetAddr":
        if not DRY:
            sym.setName("IntrMain_RetAddr", SourceType.USER_DEFINED)
        print("[ok]   rename %s -> IntrMain_RetAddr" % sym.getName())
    else:
        print("[skip] already IntrMain_RetAddr")

    # 4) plate
    cu = currentProgram.getListing().getCodeUnitAt(a)
    if cu is not None and not DRY:
        cu.setComment(CodeUnit.PLATE_COMMENT, PLATE)
        print("[ok]   set plate @ 0x080001fc")

    print("[done] AnnotateIntrRetAddr (DRY=%s)" % DRY)


main()
