@ =============================================================================
@ GBA 内存区基址常量 (硬件固定地址, 非 MMIO 寄存器)
@ 字面量池里的区基址常量经 ExportRangeToGas.resolve_word_equate 导出为符号;
@ GAS 用本表 .equ 解析回同值 -> byte-identical。
@ 仅被引用 (data-equate) 的常量才会出现在导出 .word; 其余为参考文档。
@ =============================================================================

.equ EWRAM_BASE,          0x02000000  @ External Work RAM base (256KB, 0x02000000..0x0203FFFF)
                                      @ 4295 ROM refs; used in base+offset form for gSettings etc.
.equ GBA_PALRAM_BASE,     0x05000000  @ 调色板 RAM (BG+OBJ, 各 0x200 字节)
.equ OBJ_PALRAM_BASE,     0x05000200  @ OBJ/sprite 调色板 RAM (PALRAM+0x200, 16 调色板 ×16 色)
.equ GBA_VRAM_BASE,       0x06000000  @ VRAM 基址 (BG char/screen map; 0xc0<<0x13 内联值)
.equ OBJ_TILE_VRAM_BASE,  0x06010000  @ OBJ/sprite tile 数据基址 (mode 0-2, VRAM+0x10000)
.equ GBA_OAM_BASE,        0x07000000  @ OAM (sprite 属性, 0x400 字节)
.equ BG_CHAR_VRAM_CB2,    0x06004000  @ BG charblock 2 base (GBA_VRAM_BASE + 0x4000); 43 ROM refs; BG char data start for card image tile writes
.equ BG_VRAM_TEXT_BASE,   0x06000020  @ BG text VRAM base+0x20 (tile slot 1); used by font/text render init
.equ BG_SCREEN_TILE_OFF_1,0x06000002  @ BG screen map entry 1 (tile row 0 col 1 = map base+2)
.equ BG_SCREEN_ROW1_OFF,  0x06000040  @ BG screen map row 1 base (32 tiles * 2B = 0x40 per row)
.equ BG_SCREEN_ROW1_TILE1,0x06000042  @ BG screen map row 1 col 1 (0x06000040+2)
.equ OBJ_TILE_VRAM_BASE_PAGE2,0x06010200  @ OBJ_TILE_VRAM_BASE+0x200; 16 ROM refs; icon tile base+0x200 (f01 Seg-7)

@ Seg-8 additions: Campaign VRAM BG tile bases
.equ CAMPAIGN_VRAM_BG_TILE_BASE,  0x06001100  @ campaign BG tile region base (pack display); 18 ROM refs
.equ CAMPAIGN_VRAM_BG_TILE_BASE_B,0x06001780  @ VRAM BG tile base variant B (step2/22); 2 ROM refs
.equ CAMPAIGN_VRAM_BG_TILE_BASE_C,0x06000f80  @ VRAM BG tile base variant C (step2/22); 2 ROM refs
.equ CAMPAIGN_VRAM_BG_TILE_BASE_D,0x06000d80  @ VRAM BG tile base variant D (step11); 1 ROM ref
.equ CAMPAIGN_VRAM_BG_TILE_BASE_E,0x06000900  @ VRAM BG tile base variant E (step11); 1 ROM ref
.equ CAMPAIGN_VRAM_BG_TILE_BASE_F,0x06001180  @ VRAM BG tile region F (campaign display); 5 ROM refs

@ =============================================================================
@ Seg-10 additions: pack info screen / puzzle display VRAM + palette addresses
@ =============================================================================

@ Pack info screen init values
.equ PACK_INFO_DISPCNT_SHADOW_INIT,  0x00000401  @ DISPCNT shadow init: BG0+OBJ 1D-map; 188 ROM refs
.equ PACK_INFO_BG2CNT_INIT,          0x0000820a  @ BG2CNT for pack info screen: charbase=2 scrbase=2; 5 ROM refs
.equ PACK_CARD_INFO_SPRITE_VRAM,     0x060053c0  @ OBJ VRAM commit target for card-name sprite (centered); 1 ROM ref
.equ PACK_CARD_INFO_TILEMAP_ADDR,    0x06000812  @ BG tilemap addr for card-name tile-index row; 1 ROM ref
.equ PACK_INFO_NAME_SPRITE_VRAM_B,   0x06004c40  @ OBJ VRAM commit target (wide/narrow font path); 1 ROM ref

@ Puzzle display VRAM addresses
.equ PUZZLE_NAME_SPRITE_VRAM,        0x06008020  @ Puzzle card-name sprite VRAM base; 8 ROM refs
.equ PUZZLE_TILEMAP_SCRATCH,         0x06001440  @ Puzzle tilemap scratch area; 1 ROM ref

@ BG palette address
.equ BG_PALRAM_SLOT15_BASE,          0x050001e0  @ BG PALRAM last 32 bytes (OBJ_PALRAM_BASE-0x20); 10 ROM refs
