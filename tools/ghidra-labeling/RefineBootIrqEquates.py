# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineBootIrqEquates.py  (Jython 2.7 / Ghidra 12.x)
#
# p5 boot/IRQ 细化: 给 IntrMain 区的立即数设 equate (REG_BASE / INTR_FLAG_* /
# INTR_NESTED_ENABLE_MASK / PSR_MODE_FIQ_IRQ_MASK / PSR_IRQ_MODE_IRQ_OFF), 使
# ExportRangeToGas.apply_equates 把裸立即数导出为符号; GAS 端靠 constants/gba_intr.inc
# + constants/arm_psr.inc 的 .equ/.set 解析回同值 -> byte-identical。
# 另: 修正 dispatch_thumb_isr_from_arm (0x080001f0) plate 的 Side-effects 归属错误
# (IO 寄存器恢复/cpsr 切换实际发生在 IntrMain_RetAddr, 不在本 bridge 的 3 条指令内)。
#
# Usage: tools\asm-regen\ghidra-run-script.bat RefineBootIrqEquates.py [dry]

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
    (0x080000fc, "REG_BASE",                0x04000000),  # mov r3,#0x4000000
    (0x08000124, "INTR_FLAG_SERIAL_TIMER3", 0x000000c0),  # ands r0,r1,#0xc0  (slot0)
    (0x08000130, "INTR_FLAG_HBLANK",        0x00000002),  # ands r0,r1,#0x2
    (0x0800013c, "INTR_FLAG_VBLANK",        0x00000001),  # ands r0,r1,#0x1
    (0x08000148, "INTR_FLAG_VCOUNT",        0x00000004),  # ands r0,r1,#0x4
    (0x08000154, "INTR_FLAG_TIMER0",        0x00000008),  # ands r0,r1,#0x8
    (0x08000160, "INTR_FLAG_TIMER1",        0x00000010),  # ands r0,r1,#0x10
    (0x0800016c, "INTR_FLAG_TIMER2",        0x00000020),  # ands r0,r1,#0x20
    (0x08000178, "INTR_FLAG_DMA0",          0x00000100),  # ands r0,r1,#0x100
    (0x08000184, "INTR_FLAG_DMA1",          0x00000200),  # ands r0,r1,#0x200
    (0x08000190, "INTR_FLAG_DMA2",          0x00000400),  # ands r0,r1,#0x400
    (0x0800019c, "INTR_FLAG_DMA3",          0x00000800),  # ands r0,r1,#0x800
    (0x080001a8, "INTR_FLAG_KEYPAD",        0x00001000),  # ands r0,r1,#0x1000
    (0x080001b4, "INTR_FLAG_GAMEPAK",       0x00002000),  # ands r0,r1,#0x2000
    (0x080001c4, "INTR_NESTED_ENABLE_MASK", 0x000026c0),  # mov r1,#0x26c0
    (0x080001d8, "PSR_MODE_FIQ_IRQ_MASK",   0x000000df),  # bic r3,r3,#0xdf (IntrMain)
    (0x08000204, "PSR_MODE_FIQ_IRQ_MASK",   0x000000df),  # bic r3,r3,#0xdf (RetAddr)
    (0x08000208, "PSR_IRQ_MODE_IRQ_OFF",    0x00000092),  # orr r3,r3,#0x92 (RetAddr)
]

# (addr, plate_text)  —  dispatch_thumb_isr_from_arm Side-effects 归属修正
DISPATCH_PLATE = (
    0x080001f0,
    "ARM-mode bridge invoked by IntrMain (0x080000fc) on every IRQ. Pushes lr, "
    "sets lr=IntrMain_RetAddr (0x080001fc), then bx r0 to the Thumb ISR. When the "
    "ISR returns it lands in the IntrMain_RetAddr stub (NOT in this bridge), which "
    "restores IRQ mode via cpsr manipulation and rewrites the IE/IF/IME IO "
    "registers. No game-layer callers (indeg=0); activated by the hardware IRQ "
    "mechanism only.\n"
    "\n"
    "Params: r0=Thumb ISR func_ptr (loaded by IntrMain before the call)\n"
    "Returns: void (Thumb ISR returns through lr=IntrMain_RetAddr)\n"
    "Side effects (this bridge only): pushes lr onto the IRQ stack; sets "
    "lr=IntrMain_RetAddr. The IE/IF/IME restore and cpsr mode-switch happen in "
    "IntrMain_RetAddr (0x080001fc), not in these three instructions.\n"
    "Constants: 0x92=IRQ mode (bits[4:0]=0b10010) | IRQ-disable (bit7); "
    "0xdf=BIC mask clearing bits[7:6:4:3:2:1:0] (preserves Thumb bit5)"
)


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def find_scalar_op(ins, value):
    for i in range(ins.getNumOperands()):
        for obj in ins.getOpObjects(i):
            if isinstance(obj, Scalar):
                if (obj.getValue() & 0xffffffff) == (value & 0xffffffff):
                    return i
    return -1


def do_equates():
    print("=== equates (DRY=%s) ===" % DRY)
    et = currentProgram.getEquateTable()
    nok = 0
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
            nok += 1
            continue
        eq = et.getEquate(name)
        if eq is None:
            eq = et.createEquate(name, value)
        eq.addReference(a, opi)
        print("[ok]   equate %-26s=0x%-8x @ 0x%08x op%d" % (name, value, addr_int, opi))
        nok += 1
    print("[equates] %d/%d ok" % (nok, len(EQUATES)))


def do_plate():
    print("=== dispatch plate fix (DRY=%s) ===" % DRY)
    addr_int, text = DISPATCH_PLATE
    a = _addr(addr_int)
    cur = getPlateComment(a)
    if DRY:
        print("[dry]  would set plate @ 0x%08x (cur len=%s)" % (addr_int, len(cur) if cur else 0))
        return
    setPlateComment(a, text)
    print("[ok]   plate set @ 0x%08x" % addr_int)


def main():
    print("=== RefineBootIrqEquates (DRY=%s) ===" % DRY)
    do_equates()
    do_plate()
    print("[done] RefineBootIrqEquates (DRY=%s)" % DRY)


main()
