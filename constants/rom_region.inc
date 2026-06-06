@ =============================================================================
@ ROM 区域 (region) / 语言检测常量
@ 游戏代码 "BY6E" 在 ROM 头 offset 0xAC; 第 4 字符 (offset 0xAF) 区分区域:
@   'E'(0x45)=US/English, 'J'(0x4a)=JP。代码读 [0x080000ae] (game-code 高 u16) >>8 取该字符。
@ 多处函数 (demo sprite / vija scene / text 渲染 / equip 模块) 据此分支选 US/JP 资源与字库。
@ 常配合 gSettings(0x02006c2c) bits[2:0]=language_id (0=JP) 二次判定。
@ 经 ExportRangeToGas.resolve_word_equate 导出; GAS 用本表 .equ 解析回同值 -> byte-identical。
@ =============================================================================

.equ ROM_REGION_CODE_ADDR, 0x080000ae  @ ROM 头 game-code 高 u16 (>>8 = 区域字符)
.equ REGION_CODE_JP,       0x4a        @ 'J' = 日版 (immediate, 仅参考/plate)
.equ REGION_LANG_ID_MASK,  0x7         @ gSettings bits[2:0]=language_id 掩码 (immediate, 仅参考/plate)
