@ =============================================================================
@ GFX 资源应用 (BGDT/OBJD → BG/sprite state struct) 字段位掩码
@ apply_bgdt_entry_to_bg / apply_objd_entry_to_sprite 把资源条目字段打包进目标
@ state 结构的 attr halfword ([+0x14]/[+0x16]/[+0x18]); 这些 AND 掩码先清旧字段位再 OR 新值。
@ 经 ExportRangeToGas.resolve_word_equate 导出; GAS 用本表 .equ 解析回同值 -> byte-identical。
@
@ 命名: GFX_ATTR_CLEAR_BITS_<hi>_<lo> = AND 掩码清 bits[hi:lo]。
@ =============================================================================

.equ GFX_ATTR_CLEAR_BITS_8_7,  0xfffffe7f  @ 清 attr bits[8:7] (palette 2-bit 字段)
.equ GFX_ATTR_CLEAR_BITS_13_7, 0xffffc07f  @ 清 attr bits[13:7] (tile/screen-map 字段)
