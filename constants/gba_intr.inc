@ =============================================================================
@ GBA 中断 (IRQ) 相关符号常量
@ 用于 IntrMain (ARM 模式中断主处理器) 的优先级扫描与嵌套掩码。
@ 数据来源: GBATEK (IE/IF/IME 位布局) + AGB IntrMain 标准实现。
@ 在 Ghidra 给对应立即数设 equate (同名) -> ExportRangeToGas.apply_equates 导出为符号;
@ GAS 用本表 .equ 解析回同值 -> byte-identical。
@ =============================================================================

@ MMIO 基址 (IntrMain 用作 r3 基址, +0x200 抵达 IE)
.equ REG_BASE,                0x04000000

@ -----------------------------------------------------------------------------
@ IRQ flag 位 (IE/IF 位布局) — IntrMain 按优先级逐位扫描挂起中断
@ -----------------------------------------------------------------------------
.equ INTR_FLAG_VBLANK,        0x0001  @ bit0  VBlank
.equ INTR_FLAG_HBLANK,        0x0002  @ bit1  HBlank
.equ INTR_FLAG_VCOUNT,        0x0004  @ bit2  VCount
.equ INTR_FLAG_TIMER0,        0x0008  @ bit3  Timer0
.equ INTR_FLAG_TIMER1,        0x0010  @ bit4  Timer1
.equ INTR_FLAG_TIMER2,        0x0020  @ bit5  Timer2
.equ INTR_FLAG_TIMER3,        0x0040  @ bit6  Timer3
.equ INTR_FLAG_SERIAL,        0x0080  @ bit7  Serial (SIO)
.equ INTR_FLAG_DMA0,          0x0100  @ bit8  DMA0
.equ INTR_FLAG_DMA1,          0x0200  @ bit9  DMA1
.equ INTR_FLAG_DMA2,          0x0400  @ bit10 DMA2
.equ INTR_FLAG_DMA3,          0x0800  @ bit11 DMA3
.equ INTR_FLAG_KEYPAD,        0x1000  @ bit12 Keypad
.equ INTR_FLAG_GAMEPAK,       0x2000  @ bit13 GamePak (卡带拔出)

@ -----------------------------------------------------------------------------
@ IntrMain 复合掩码
@ -----------------------------------------------------------------------------
@ 优先级扫描槽0: Serial|Timer3 合并检测 (0x80|0x40)
.equ INTR_FLAG_SERIAL_TIMER3, 0x00c0
@ 嵌套窗口允许的 IE 子集: GamePak|DMA2|DMA1|Serial|Timer3 (0x2000|0x400|0x200|0x80|0x40)
.equ INTR_NESTED_ENABLE_MASK, 0x26c0
