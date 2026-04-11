@ =============================================================================
@ 汇编宏定义
@ 文件: include/macros.inc
@ =============================================================================

@ 预组条目宏
@ 参数:
@   so_code - 卡牌内部编号（十进制整数，如 4088 = 真红眼黑龙）
@   qty     - 副本数量（1、2 或 3）
@ 编码格式: [so_code * 4 | qty][0x0000]（共 4 字节，小端序）
@ 示例: deck_entry 4088, 1    @ Red-Eyes B. Dragon
.macro deck_entry so_code:req, qty:req
    .hword (\so_code * 4) | \qty, 0
.endm

@ 禁卡表条目宏
@ 参数:
@   so_code - 卡牌内部编号（十进制整数）
@   limit   - 限制数量（0 = 禁止，1 = 限制，2 = 准限制）
@ 编码格式: [so_code][limit]（各 2 字节，小端序）
@ 示例: banlist_entry 4088, 1    @ Red-Eyes B. Dragon 限制
.macro banlist_entry so_code:req, limit:req
    .hword \so_code, \limit
.endm

@ 对手/初始卡组条目宏
@ 参数:
@   so_code - 卡牌内部编号（十进制整数）
@ 编码格式: [so_code]（2 字节，小端序）
@ 重复多次表示多张副本
@ 示例: deck_card 4088    @ Red-Eyes B. Dragon
.macro deck_card so_code:req
    .hword \so_code
.endm
