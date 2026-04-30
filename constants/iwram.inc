@ =============================================================================
@ IWRAM 变量符号常量
@ 数据来源: refs/datacrystal-um2006/ram-map.md
@ =============================================================================

.equ gPrng,           0x03000040  @ 4 B  伪随机数发生器状态
.equ gFrameCounter,   0x03000240  @ 4 B  帧计数器
.equ pack_ui_state,   0x03005850  @ pack scene state struct; offset 0x10 = u16 state field
