@ =============================================================================
@ ARM CPSR/SPSR 处理器状态寄存器位常量
@ 用于 crt0 (init_cpu_stacks_and_irq_vector) 与 IntrMain 的模式切换。
@ 数据来源: ARM ARM (CPSR mode 字段 bits[4:0]) + refs/pokeruby constants/gba_constants.inc
@ 在 Ghidra 给对应立即数设 equate (同名) -> ExportRangeToGas.apply_equates 导出为符号;
@ GAS 用本表 .set 解析回同值 -> byte-identical。
@ =============================================================================

.set PSR_USR_MODE,  0x00000010  @ User 模式
.set PSR_FIQ_MODE,  0x00000011  @ FIQ 模式
.set PSR_IRQ_MODE,  0x00000012  @ IRQ 模式
.set PSR_SVC_MODE,  0x00000013  @ Supervisor 模式
.set PSR_ABT_MODE,  0x00000017  @ Abort 模式
.set PSR_UND_MODE,  0x0000001b  @ Undefined 模式
.set PSR_SYS_MODE,  0x0000001f  @ System 模式
.set PSR_MODE_MASK, 0x0000001f  @ 模式位掩码 bits[4:0]
.set PSR_T_BIT,     0x00000020  @ Thumb 状态位
.set PSR_F_BIT,     0x00000040  @ FIQ 禁用
.set PSR_I_BIT,     0x00000080  @ IRQ 禁用
