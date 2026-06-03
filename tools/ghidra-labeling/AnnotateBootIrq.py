# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# AnnotateBootIrq.py  (Jython 2.7 / Ghidra 12.x)
#
# 细化 boot/IRQ 区 (0x080000c0 init_cpu_stacks_and_irq_vector + 0x080000fc IntrMain).
#
# 里程碑 1 (本脚本当前范围):
#   1) 反汇编 0x080000fc..0x080001ec 为 ARM (Ghidra 原误标为 data DWORD_080000fc + UNDEF)
#   2) createFunction IntrMain @ 0x080000fc (ARM 中断主处理器; 尾段落到 0x1f0 dispatch)
#   3) rename DAT_080000f4 -> sp_sys_init (System 模式栈顶 0x03007800)
#      rename DAT_080000f8 -> sp_irq_init (IRQ 模式栈顶 0x03007e00)
#   4) 修正 init_cpu_stacks_and_irq_vector plate (原注释把 IntrMain 误称 dispatch_thumb_isr_from_arm)
#   5) 给 IntrMain 加 plate
#   6) 在 0x08000234 定义 Dword (IntrMain 的 ldr r1,[pc,#72] 目标 = gIntrTable 指针)
#
# 备份: 调用前已 cp .rep 到 .bak-<ts>-pre-boot-irq-refine
# Usage:
#   tools\asm-regen\ghidra-run-script.bat AnnotateBootIrq.py        (写入)
#   tools\asm-regen\ghidra-run-script.bat AnnotateBootIrq.py dry    (只打印, 不写)

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.address import AddressSet
from ghidra.program.model.data import DWordDataType
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import SourceType, SymbolType
from java.lang import Exception as JavaException
from java.math import BigInteger

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

IRQ_LO = 0x080000fc
IRQ_HI = 0x080001ef   # 末条 ldr r0,[r1] @ 0x1ec 占 0x1ec..0x1ef

PLATE_INIT = (
    u"GBA ROM 启动入口 (crt0/Init). 复位后 BIOS 跳转至此. "
    u"依次: 进 IRQ 模式设 IRQ 栈顶 sp_irq_init=0x03007e00; 进 System "
    u"模式设主栈 sp_sys_init=0x03007800; 将 IntrMain (本游戏 ARM "
    u"中断处理器, @0x080000fc) 地址写入 BIOS IRQ 向量 "
    u"[0x03007ffc]; bx 跳到 run_game_main (AgbMain, 0x080f4d91 thumb) 启动游戏, "
    u"不返回. 末尾 b 为不可达死循环."
)
PLATE_INTRMAIN = (
    u"ARM 模式中断主处理器 (AGB IntrMain). 被 crt0 注册进 "
    u"BIOS IRQ 向量 [0x03007ffc], 每次硬件 IRQ 由 BIOS 跳入. "
    u"流程: 读 REG_IE/IF(0x4000200)/REG_IME(0x4000208)+SPSR 入栈; 按优先"
    u"级扫描挂起中断求 gIntrTable(@0x03000000) 槽偏移; "
    u"写 REG_IF 应答; 设 REG_IE=允许嵌套子集(0x26c0); 切 "
    u"System 模式开嵌套; 取 gIntrTable[槽] 的 Thumb ISR 指针; "
    u"尾段 (dispatch_thumb_isr_from_arm @0x1f0) 调用之并恢复现场"
    u"返回. GamePak(卡带拔出)中断 → 关声音"
    u"(SOUNDCNT_X)后死循环."
)


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def rename_symbol(addr_int, new_name):
    a = _addr(addr_int)
    st = currentProgram.getSymbolTable()
    sym = st.getPrimarySymbol(a)
    if sym is None:
        print("[warn] no symbol @ 0x%08x to rename -> %s" % (addr_int, new_name))
        return
    old = sym.getName()
    if old == new_name:
        print("[skip] 0x%08x already %s" % (addr_int, new_name))
        return
    if DRY:
        print("[dry]  rename 0x%08x %s -> %s" % (addr_int, old, new_name))
        return
    sym.setName(new_name, SourceType.USER_DEFINED)
    print("[ok]   rename 0x%08x %s -> %s" % (addr_int, old, new_name))


def set_plate(addr_int, text):
    a = _addr(addr_int)
    cu = currentProgram.getListing().getCodeUnitAt(a)
    if cu is None:
        print("[warn] no code unit @ 0x%08x for plate" % addr_int)
        return
    if DRY:
        print("[dry]  set plate @ 0x%08x (%d chars)" % (addr_int, len(text)))
        return
    cu.setComment(CodeUnit.PLATE_COMMENT, text)
    print("[ok]   set plate @ 0x%08x" % addr_int)


def main():
    print("=== AnnotateBootIrq (DRY=%s) ===" % DRY)
    lo = _addr(IRQ_LO)
    hi = _addr(IRQ_HI)
    st = currentProgram.getSymbolTable()
    ctx = currentProgram.getProgramContext()

    # 1) 清掉 [0x0fc, 0x1ef] 现有 data/UNDEF, 删除 0x0fc 处的 DWORD_ label
    if not DRY:
        for s in list(st.getSymbols(lo)):
            if s.getSymbolType() == SymbolType.LABEL:
                print("[ok]   remove label %s @ 0x080000fc" % s.getName())
                st.removeSymbolSpecial(s)
        try:
            clearListing(lo, hi)
        except (JavaException, Exception) as e:
            print("[warn] clearListing: %s" % e)

    # 2) 设 ARM (TMode=0) 并反汇编
    tmode = ctx.getRegister("TMode")
    if tmode is not None and not DRY:
        try:
            ctx.setValue(tmode, lo, hi, BigInteger.ZERO)
        except (JavaException, Exception) as e:
            print("[warn] setTMode: %s" % e)
    if not DRY:
        cmd = DisassembleCommand(lo, AddressSet(lo, hi), True)
        if cmd.applyTo(currentProgram):
            print("[ok]   disassembled ARM 0x080000fc..0x080001ec")
        else:
            print("[FAIL] disasm: %s" % cmd.getStatusMsg())
            return

    # 3) createFunction IntrMain @ 0x0fc
    if not DRY:
        f = getFunctionAt(lo)
        if f is None:
            f = createFunction(lo, "IntrMain")
        if f is None:
            print("[FAIL] createFunction IntrMain")
            return
        if f.getName() != "IntrMain":
            f.setName("IntrMain", SourceType.USER_DEFINED)
        print("[ok]   function IntrMain @ 0x080000fc body=%s" % f.getBody())

    # 4) 定义 0x08000234 Dword (IntrMain ldr r1,[pc,#72] -> gIntrTable 指针)
    if not DRY:
        t = _addr(0x08000234)
        d = currentProgram.getListing().getDataAt(t)
        if d is None or not d.isDefined() or d.getLength() != 4:
            try:
                clearListing(t, t.add(3))
                createData(t, DWordDataType())
                print("[ok]   defined Dword @ 0x08000234")
            except (JavaException, Exception) as e:
                print("[warn] define dword 0x234: %s" % e)

    # 5) rename 栈 label
    rename_symbol(0x080000f4, "sp_sys_init")
    rename_symbol(0x080000f8, "sp_irq_init")

    # 6) plate 注释
    set_plate(0x080000c0, PLATE_INIT)
    set_plate(0x080000fc, PLATE_INTRMAIN)

    print("[done] AnnotateBootIrq (DRY=%s)" % DRY)


main()
