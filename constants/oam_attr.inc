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

.equ OAM_ATTR0_HIDDEN,         0x0000ffff  @ attr0 all-bits-set: OBJ disabled/hidden mode
                                             @ used by apply_sprite_gfx_by_type for initial hide

.equ OAM_HFLIP_VFLIP_PACKED_PATTERN, 0x40004000  @ bit14 set in both attr0 and attr1 halfwords (packed as 32-bit word)
                                                   @ ORed into 32-bit OAM entry to toggle hflip+vflip
.equ OAM_ATTR1_X_MASK,  0x000001ff  @ attr1 bits[8:0] = x coordinate (9-bit x-pos field)
.equ OAM_ATTR1_X_CLEAR, 0xfffffe00  @ clear attr1 bits[8:0] before inserting x-pos

@ =============================================================================
@ file 02 Seg-6 additions: OAM attr2 tile-field clear mask
@ =============================================================================
.equ OAM_ATTR2_TILE_CLEAR, 0xffffe000  @ AND mask clearing OAM attr2 bits[12:0] before inserting new tile/set_code; 31 raw refs; 3 Seg-6 slots
