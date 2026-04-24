@ =============================================================================
@ GBA MMIO 寄存器符号常量
@ 数据来源: refs/gba-ghidra-loader/src/main/java/gba/GBALoader.java (mapIO)
@ 生成脚本: tools/gen_gba_io_inc.py (据 GBALoader.java 自动提取)
@
@ 用法: 代码里 .word <名字> / ldr rN, =<名字>,GAS 会 .equ 替换成对应 MMIO 地址
@ =============================================================================

@ -----------------------------------------------------------------------------
@ LCD I/O
@ -----------------------------------------------------------------------------
.equ DISPCNT,     0x04000000  @ LCD Control
.equ DISPSTAT,    0x04000004  @ General LCD Status (STAT,LYC)
.equ VCOUNT,      0x04000006  @ Vertical Counter (LY)
.equ BG0CNT,      0x04000008  @ BG0 Control
.equ BG1CNT,      0x0400000A  @ BG1 Control
.equ BG2CNT,      0x0400000C  @ BG2 Control
.equ BG3CNT,      0x0400000E  @ BG3 Control
.equ BG0HOFS,     0x04000010  @ BG0 X-Offset
.equ BG0VOFS,     0x04000012  @ BG0 Y-Offset
.equ BG1HOFS,     0x04000014  @ BG1 X-Offset
.equ BG1VOFS,     0x04000016  @ BG1 Y-Offset
.equ BG2HOFS,     0x04000018  @ BG2 X-Offset
.equ BG2VOFS,     0x0400001A  @ BG2 Y-Offset
.equ BG3HOFS,     0x0400001C  @ BG3 X-Offset
.equ BG3VOFS,     0x0400001E  @ BG3 Y-Offset
.equ BG2PA,       0x04000020  @ BG2 Rotation/Scaling Parameter A (dx)
.equ BG2PB,       0x04000022  @ BG2 Rotation/Scaling Parameter B (dmx)
.equ BG2PC,       0x04000024  @ BG2 Rotation/Scaling Parameter C (dy)
.equ BG2PD,       0x04000026  @ BG2 Rotation/Scaling Parameter D (dmy)
.equ BG2X,        0x04000028  @ BG2 Reference Point X-Coordinate
.equ BG2Y,        0x0400002C  @ BG2 Reference Point Y-Coordinate
.equ BG3PA,       0x04000030  @ BG3 Rotation/Scaling Parameter A (dx)
.equ BG3PB,       0x04000032  @ BG3 Rotation/Scaling Parameter B (dmx)
.equ BG3PC,       0x04000034  @ BG3 Rotation/Scaling Parameter C (dy)
.equ BG3PD,       0x04000036  @ BG3 Rotation/Scaling Parameter D (dmy)
.equ BG3X,        0x04000038  @ BG3 Reference Point X-Coordinate
.equ BG3Y,        0x0400003C  @ BG3 Reference Point Y-Coordinate
.equ WIN0H,       0x04000040  @ Window 0 Horizontal Dimensions
.equ WIN1H,       0x04000042  @ Window 1 Horizontal Dimensions
.equ WIN0V,       0x04000044  @ Window 0 Vertical Dimensions
.equ WIN1V,       0x04000046  @ Window 1 Vertical Dimensions
.equ WININ,       0x04000048  @ Inside of Window 0 and 1
.equ WINOUT,      0x0400004A  @ Inside of OBJ Window & Outside of Windows
.equ MOSAIC,      0x0400004C  @ Mosaic Size
.equ BLDCNT,      0x04000050  @ Color Special Effects Selection
.equ BLDALPHA,    0x04000052  @ Alpha Blending Coefficients
.equ BLDY,        0x04000054  @ Brightness (Fade-In/Out) Coefficient

@ -----------------------------------------------------------------------------
@ Sound
@ -----------------------------------------------------------------------------
.equ SOUND1CNT_L, 0x04000060  @ Sweep register (NR10)
.equ SOUND1CNT_H, 0x04000062  @ Duty/Length/Envelope (NR11, NR12)
.equ SOUND1CNT_X, 0x04000064  @ Frequency/Control (NR13, NR14)
.equ SOUND2CNT_L, 0x04000068  @ Duty/Length/Envelope (NR21, NR22)
.equ SOUND2CNT_H, 0x0400006C  @ Frequency/Control (NR23, NR24)
.equ SOUND3CNT_L, 0x04000070  @ Stop/Wave RAM select (NR30)
.equ SOUND3CNT_H, 0x04000072  @ Length/Volume (NR31, NR32)
.equ SOUND3CNT_X, 0x04000074  @ Frequency/Control (NR33, NR34)
.equ SOUND4CNT_L, 0x04000078  @ Length/Envelope (NR41, NR42)
.equ SOUND4CNT_H, 0x0400007C  @ Frequency/Control (NR43, NR44)
.equ SOUNDCNT_L,  0x04000080  @ Control Stereo/Volume/Enable (NR50, NR51)
.equ SOUNDCNT_H,  0x04000082  @ Control Mixing/DMA Control
.equ SOUNDCNT_X,  0x04000084  @ Control Sound on/off (NR52)
.equ SOUNDBIAS,   0x04000088  @ Sound PWM Control
.equ WAVE_RAM,    0x04000090  @ Channel 3 Wave Pattern RAM (2 banks!!)
.equ FIFO_A,      0x040000A0  @ Channel A FIFO, Data 0-3
.equ FIFO_B,      0x040000A4  @ Channel B FIFO, Data 0-3

@ -----------------------------------------------------------------------------
@ DMA
@ -----------------------------------------------------------------------------
.equ DMA0SAD,     0x040000B0  @ DMA 0 Source Address
.equ DMA0DAD,     0x040000B4  @ DMA 0 Destination Address
.equ DMA0CNT_L,   0x040000B8  @ DMA 0 Word Count
.equ DMA0CNT_H,   0x040000BA  @ DMA 0 Control
.equ DMA1SAD,     0x040000BC  @ DMA 1 Source Address
.equ DMA1DAD,     0x040000C0  @ DMA 1 Destination Address
.equ DMA1CNT_L,   0x040000C4  @ DMA 1 Word Count
.equ DMA1CNT_H,   0x040000C6  @ DMA 1 Control
.equ DMA2SAD,     0x040000C8  @ DMA 2 Source Address
.equ DMA2DAD,     0x040000CC  @ DMA 2 Destination Address
.equ DMA2CNT_L,   0x040000D0  @ DMA 2 Word Count
.equ DMA2CNT_H,   0x040000D2  @ DMA 2 Control
.equ DMA3SAD,     0x040000D4  @ DMA 3 Source Address
.equ DMA3DAD,     0x040000D8  @ DMA 3 Destination Address
.equ DMA3CNT_L,   0x040000DC  @ DMA 3 Word Count
.equ DMA3CNT_H,   0x040000DE  @ DMA 3 Control

@ -----------------------------------------------------------------------------
@ Timer
@ -----------------------------------------------------------------------------
.equ TM0CNT_L,    0x04000100  @ Timer 0 Counter/Reload
.equ TM0CNT_H,    0x04000102  @ Timer 0 Control
.equ TM1CNT_L,    0x04000104  @ Timer 1 Counter/Reload
.equ TM1CNT_H,    0x04000106  @ Timer 1 Control
.equ TM2CNT_L,    0x04000108  @ Timer 2 Counter/Reload
.equ TM2CNT_H,    0x0400010A  @ Timer 2 Control
.equ TM3CNT_L,    0x0400010C  @ Timer 3 Counter/Reload
.equ TM3CNT_H,    0x0400010E  @ Timer 3 Control

@ -----------------------------------------------------------------------------
@ Serial / Keypad / JOY Bus
@ -----------------------------------------------------------------------------
.equ SIODATA32,   0x04000120  @ SIO Data (Normal-32bit Mode; shared with below)
.equ SIOCNT,      0x04000128  @ SIO Control Register
.equ SIOMLT_SEND, 0x0400012A  @ SIO Data (Local of MultiPlayer; shared below)
.equ SIODATA8,    0x0400012A  @ SIO Data (Normal-8bit and UART Mode)
.equ KEYINPUT,    0x04000130  @ Key Status
.equ KEYCNT,      0x04000132  @ Key Interrupt Control
.equ RCNT,        0x04000134  @ SIO Mode Select/General Purpose Data
.equ IR,          0x04000136  @ Ancient - Infrared Register (Prototypes only)
.equ JOYCNT,      0x04000140  @ SIO JOY Bus Control
.equ JOY_RECV,    0x04000150  @ SIO JOY Bus Receive Data
.equ JOY_TRANS,   0x04000154  @ SIO JOY Bus Transmit Data
.equ JOYSTAT,     0x04000158  @ SIO JOY Bus Receive Status

@ -----------------------------------------------------------------------------
@ Interrupt / Waitstate / Power-Down
@ -----------------------------------------------------------------------------
.equ IE,          0x04000200  @ Interrupt Enable Register
.equ IF,          0x04000202  @ Interrupt Request Flags / IRQ Acknowledge
.equ WAITCNT,     0x04000204  @ Game Pak Waitstate Control
.equ IME,         0x04000208  @ Interrupt Master Enable Register
.equ POSTFLG,     0x04000300  @ Undocumented - Post Boot Flag
.equ HALTCNT,     0x04000301  @ Undocumented - Power Down Control

