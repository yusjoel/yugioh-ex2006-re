@ =============================================================================
@ OAM attribute (硬件 OAM 项) 字段位掩码常量
@ 用于 cell-anim OAM 构建簇 (setup_isd_cell_anim_oam_entry 0x08015954) 对暂存缓冲
@ gOamAttrBuildBuf 内每个 OAM 项的 attr2 char-name 字段做 tile-base 重映射。
@ 经 ExportRangeToGas.resolve_word_equate 导出符号; GAS 用本表 .equ 解析回同值 -> byte-identical。
@
@ OAM attr2 格式: bits[9:0]=char name (tile index) / bits[11:10]=priority / bits[15:12]=palette。
@ =============================================================================

.equ OAM_ATTR2_CHARNAME_MASK,  0x000003ff  @ 保留 attr2 bits[9:0] (char name = tile index)
.equ OAM_ATTR2_CHARNAME_CLEAR, 0xfffffc00  @ 清 attr2 bits[9:0] (插入 tile-base 重映射前)
