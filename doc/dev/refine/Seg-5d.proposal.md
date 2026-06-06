# Refine Proposal: Seg-5d  [0x080171ec..0x0801794c)

## 段测绘

函数入口 (push-prologue, 按地址序):

| 地址 | 现名 | 行号 (asm/00_system_str_vija.s) |
|---|---|---|
| 0x080171ec | validate_complement_checksum | L8181 |
| 0x0801722c | decode_char_frame_to_vram | L8229 |
| 0x08017464 | compute_floor_log2 | L8497 |
| 0x08017478 | unpack_bits_to_byte_buf | L8517 |
| 0x080174e8 | pack_bytes_to_vram_bits | L8581 |
| 0x08017540 | init_scrollbar_oam_slot_settings | L8642 |
| 0x08017574 | name_input_page_init | L8670 |
| 0x080175f4 | dispatch_text_render_by_mode | L8730 |
| 0x080176c0 | apply_sprite_gfx_by_type | L8833 |
| 0x0801778c | apply_sprite_gfx_type_zero | L8937 |
| 0x08017798 | setup_font_jp_ctx_bg_vram_fixed | L8950 |
| 0x080177dc | setup_font_jp_ctx_obj_vram_row | L8986 |
| 0x08017830 | fill_bg0_tilemap_name_input | L9038 |
| 0x0801785c | pad_str_to_char_multiple | L9066 |
| 0x080178b4 | load_game_str_pair_1004_to_state | L9119 |
| 0x0801794c | load_game_str_1006_to_state | L9197 (= Seg-6 起点, 边界) |

总计: 15 函数 (含边界函数 load_game_str_1006_to_state 已 named, 仅作 REF_SLOT 消费者参考)

残留自动名槽 (DWORD_/DAT_):

decode_char_frame_to_vram 内部 (12 槽):
- DWORD_08017264 = 0xfffffa50  (neg stack frame size)
- DWORD_08017268 = 0x000005a4  (sp offset 1)
- DWORD_080172d4 = 0x01000168  (BIOS cpu_set ctrl)
- DWORD_080172d8 = 0x000005a4  (sp offset, duplicate)
- DWORD_080172dc = 0x09e3a790  (assert string ptr)
- DWORD_080172f8 = 0x09e3a7ac  (assert string ptr 2)
- DWORD_0801740c = 0x00000201  (field offset, BLOCKED -- see below)
- DWORD_08017410 = 0x09e3a660  (char_frame_decode_lut ptr)
- DWORD_08017414 = 0x000005a4  (sp offset, 3rd ref)
- DWORD_08017418 = 0x000005a2  (sp offset 2)
- DWORD_0801741c = 0x000005ac  (sp offset 3)
- DWORD_08017420 = 0x00003e9c  (vram step constant)

init_scrollbar_oam_slot_settings (1 槽):
- DAT_08017570  = 0x02029250   (gState)

name_input_page_init (7 槽):
- DAT_080175d8  = 0x02029250   (gState)
- DAT_080175dc  = 0x050000c9   (cpu_set fill ctrl)
- DAT_080175e0  = 0x00001c02   (BG0CNT init value)
- DAT_080175e4  = 0x00001d8c   (BG1CNT init value)
- DAT_080175e8  = 0x00001e8d   (BG2CNT init value)
- DAT_080175ec  = 0x00001f8f   (BG3CNT init value)
- DAT_080175f0  = 0x0202348c   (gTextEncodingOverride)

apply_sprite_gfx_by_type (5 槽):
- DAT_08017778  = 0x02029250   (gState)
- DAT_0801777c  = 0x09e3afc8   (sprite_gfx_type_meta ROM table)
- DAT_08017780  = 0x09e3afd8   (sprite_palette_type_table ROM table)
- DAT_08017784  = 0xffffc07f   (OAM attr2 palette clear mask)
- DAT_08017788  = 0x0000ffff   (OAM attr0 hidden init)

setup_font_jp_ctx_bg_vram_fixed (2 槽):
- DAT_080177d0  = 0x06000020   (BG VRAM base + 0x20)
- DAT_080177d4  = 0x02006ed0   (gFontJpCtx)

setup_font_jp_ctx_obj_vram_row (2 槽, PTR_ 已命名不计):
- DAT_08017824  = 0x06010000   (OBJ_TILE_VRAM_BASE, in gba_mem.inc)
- DAT_08017828  = 0x02006ed0   (gFontJpCtx)

load_game_str_pair_1004_to_state (4 槽, PTR_ 已命名不计):
- DAT_08017930  = 0x02029250   (gState)
- DAT_08017934  = 0x00001004   (string ID 0x1004)
- DAT_0801793c  = 0x02000000   (EWRAM base)
- DAT_08017940  = 0x00006c2c   (gSettings offset from EWRAM base)
- DAT_08017948  = 0x00001005   (string ID 0x1005)

load_game_str_1006_to_state (4 槽, PTR_ 已命名不计):
- DAT_08017990  = 0x02029250   (gState)
- DAT_08017994  = 0x00001006   (string ID 0x1006)
- DAT_0801799c  = 0x02000000   (EWRAM base)
- DAT_080179a0  = 0x00006c2c   (gSettings offset)

ROM_INCBIN / .byte 块:
- ROM_INCBIN 0x17424, 0x40  (64 B; L8490 in asm/00_system_str_vija.s)

---

## 数据块分类 (Rule 2/3) -- 每块给 ref-scan 证据

| 块 | ref-scan (raw / THUMB+1) | 判定 | 理由 |
|---|---|---|---|
| ROM_INCBIN 0x17424, 0x40 (64 B) | raw=0 thumb=0 (每 4B 对齐逐格扫描均 0) | §5.1 登记 | 0 外部引用; 块内含 2 个 THUMB 小函数 (bx lr at 0x17444 and 0x17462), 系 dead code; 见下节 |

ref-scan 详情 (python d.count(struct.pack('<I', addr)) for addr in block):
- 0x08017424 raw=0 thumb=0; 0x08017428 raw=0 thumb=0; ...全 16 项均 0
- 验证: `d.count(struct.pack('<I', 0x08017424)) == 0` and `d.count(struct.pack('<I', 0x08017425)) == 0`

块内容分析 (THUMB 反汇编):
- 0x17424..0x17444 (32 B): `adds r2,r1,#0; asrs r1,r2,#2; adds r0,r0,r1; ldrb r1,[r0,#0]; adds r0,r2,#0; cmp r2,#0; bge +2; adds r0,r2,#3; asrs r0,r0,#2; lsls r0,r0,#2; subs r0,r2,r0; lsls r0,r0,#1; asrs r1,r0; movs r0,#3; ands r1,r0; adds r0,r1,#0; bx lr; .zero 2` -- 孤儿 bitfield-index helper (dead code)
- 0x17448..0x17462 (26 B): `movs r2,#1; ands r2,r0; lsls r2,r2,#3; movs r1,#2; rsbs r1,r1,#0; ands r1,r0; ldrh r3,[r1,#2]; lsls r0,r3,#0x10; ldrh r1,[r1,#0]; orrs r0,r1; asrs r0,r2; lsls r0,r0,#0x10; lsrs r0,r0,#0x10; bx lr` -- 孤儿 halfword-pair extractor (dead code)

判定: §5.1 登记 (全 ROM 0 引用, dead code)

---

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate)

新建 constants (先确认现有 inc 无可复用):
- `gba_mem.inc` 无 EWRAM_BASE; `constants/` 无 gState; `oam_attr.inc` 无 palette mask
- `ewram.inc` 已有 gTextEncodingOverride=0x0202348c; gba_mem.inc 已有 OBJ_TILE_VRAM_BASE=0x06010000

| 槽 | value | const_name | slot_label | inc 文件 |
|---|---|---|---|---|
| DWORD_080172d4 | 0x01000168 | CHAR_FRAME_DECODE_CPUSET_CTRL | decode_char_frame_to_vram_cpuset_ctrl | 新建 name_input.inc |
| DAT_080175dc | 0x050000c9 | NAME_INPUT_STATE_CPUSET_CTRL | name_input_page_init_cpuset_ctrl | 新建 name_input.inc |
| DAT_080175e0 | 0x00001c02 | NAME_INPUT_BG0CNT_INIT | name_input_page_init_bg0cnt | 新建 name_input.inc |
| DAT_080175e4 | 0x00001d8c | NAME_INPUT_BG1CNT_INIT | name_input_page_init_bg1cnt | 新建 name_input.inc |
| DAT_080175e8 | 0x00001e8d | NAME_INPUT_BG2CNT_INIT | name_input_page_init_bg2cnt | 新建 name_input.inc |
| DAT_080175ec | 0x00001f8f | NAME_INPUT_BG3CNT_INIT | name_input_page_init_bg3cnt | 新建 name_input.inc |
| DAT_08017784 | 0xffffc07f | GFX_ATTR_CLEAR_BITS_13_7 | apply_sprite_gfx_by_type_oam_pal_mask | 复用 gfx_resource.inc (Seg-5b 已建, 同值 0xffffc07f; 不新建重名常量) |
| DAT_08017788 | 0x0000ffff | OAM_ATTR0_HIDDEN | apply_sprite_gfx_by_type_attr0_init | 追加 oam_attr.inc |

注: BGnCNT init 值仅 name_input_page_init 使用 (asm 00_system_str_vija.s L8684-L8696 各 1 次), 新建 name_input.inc 集中放置。

### REF_SLOTS (USER-label + DATA-ref; RAM/ROM 全局或 carve label)

RAM 全局 (需新增至 ewram.inc / gba_mem.inc):

| 槽 | target | gas_label | slot_label | 证据 |
|---|---|---|---|---|
| DAT_08017570 / DAT_080175d8 / DAT_08017778 / DAT_08017930 / DAT_08017990 | 0x02029250 | gState | (各函数前缀)_gstate | 37 ROM refs; name_input/banlist 场景主状态结构; plates for init_scrollbar_oam_slot_settings (L8634 `gState+0x304=0x02029554`) / name_input_page_init / apply_sprite_gfx_by_type / load_game_str_pair_1004_to_state -- 高置信度 gState 全局 |
| DAT_080177d4 / DAT_08017828 | 0x02006ed0 | gFontJpCtx | (各函数前缀)_font_jp_ctx | 202 ROM refs; setup_font_jp_ctx_bg_vram_fixed (L8948 `CTX_BASE=0x02006ed0`) / setup_font_jp_ctx_obj_vram_row (L8985) -- 高置信度 JP 字体渲染上下文全局 |
| DAT_080175f0 | 0x0202348c | gTextEncodingOverride | name_input_page_init_text_enc_override | 复用 ewram.inc (L18 gTextEncodingOverride=0x0202348C) -- 高置信度 |
| DAT_08017824 | 0x06010000 | OBJ_TILE_VRAM_BASE | setup_font_jp_ctx_obj_vram_row_vram_base | 复用 gba_mem.inc (OBJ_TILE_VRAM_BASE=0x06010000) -- 高置信度 |
| DAT_0801793c / DAT_0801799c | 0x02000000 | EWRAM_BASE | (各函数前缀)_ewram_base | base+offset 分离形态; gSettings = EWRAM_BASE+0x6c2c; 新增 EWRAM_BASE 到 gba_mem.inc (0x02000000 有 4295 ROM refs, 值得命名) |
| DAT_08017940 / DAT_080179a0 | 0x00006c2c | GSETTINGS_OFFSET | (各函数前缀)_gsettings_offset | 已有 gSettings=0x02006c2c (ewram.inc), 此处 base+offset 形态中的 offset 分量; 新建 equate GSETTINGS_OFFSET=0x6c2c 在 name_input.inc |

ROM 数据 carve labels (见 carve 计划节):

| 槽 | target | gas_label | slot_label | 证据 |
|---|---|---|---|---|
| DWORD_08017410 | 0x09e3a660 | char_frame_decode_lut | decode_char_frame_to_vram_lut_ptr | 1 ROM ref; 68-entry×4B halfword-pair decode LUT; 消费者 decode_char_frame_to_vram L8349 ldrh [r6]; 高置信度 |
| DAT_0801777c | 0x09e3afc8 | sprite_gfx_type_meta | apply_sprite_gfx_by_type_meta_ptr | 1 ROM ref; 4-entry×4B GFX descriptor table for sprite types 0..3; 消费者 apply_sprite_gfx_by_type L8848 ldmia r0!; 高置信度 |
| DAT_08017780 | 0x09e3afd8 | sprite_palette_type_table | apply_sprite_gfx_by_type_pal_table_ptr | 1 ROM ref; 4-byte palette index table [1,1,16,16]; 消费者 apply_sprite_gfx_by_type L8853; 高置信度 |

assert string slots (points into existing incbin blob assert_pdst_nameid):

| 槽 | target | gas_label | slot_label | 证据 |
|---|---|---|---|---|
| DWORD_080172dc | 0x09e3a790 | (inside assert_pdst_nameid blob) | decode_char_frame_to_vram_assert_str_prohibit_cs | 1 ref; string = "Prohibit CheckSum Error\n"; inside .incbin 0x1E3A78D,0xB2B (rom.s L920); 高置信度 |
| DWORD_080172f8 | 0x09e3a7ac | (inside assert_pdst_nameid blob) | decode_char_frame_to_vram_assert_str_password_size | 1 ref; string = "PassWord Size Error\n"; same blob; 高置信度 |

注: 这两个槽指向 assert_pdst_nameid 大 incbin 内部, 目前该 blob 无拆分计划 (assert 串是第一步 carve, 数据表是另类 carve). 暂作 RENAME_SLOT 加 EOL 注明字符串内容; 若后续 carve assert blob 再升为 REF_SLOT.

### RENAME_SLOTS (纯改名 + EOL)

decode_char_frame_to_vram 内部帧偏移槽 (不是 global constants, 是函数内部 sp 偏移值):

| 槽 | slot_label | eol_ascii |
|---|---|---|
| DWORD_08017264 | decode_char_frame_to_vram_neg_frame_size | neg stack frame alloc: sp -= 0x5b0 |
| DWORD_08017268 | decode_char_frame_to_vram_sp_state_ptr_off | sp+0x5a4: ptr to r1(state) |
| DWORD_080172d8 | decode_char_frame_to_vram_sp_state_ptr_off_b | sp+0x5a4 2nd ref (same value) |
| DWORD_08017414 | decode_char_frame_to_vram_sp_state_ptr_off_c | sp+0x5a4 3rd ref (same value) |
| DWORD_08017418 | decode_char_frame_to_vram_sp_packed_cnt_off | sp+0x5a2: packed char count |
| DWORD_0801741c | decode_char_frame_to_vram_sp_state_holder_off | sp+0x5ac: state ptr holder |
| DWORD_08017420 | decode_char_frame_to_vram_vram_step | 0x3e9c: VRAM bit-field step; med-conf |

assert string ptr slots (points into blob, rename + EOL):

| 槽 | slot_label | eol_ascii |
|---|---|---|
| DWORD_080172dc | decode_char_frame_to_vram_assert_prohibit_cs_ptr | ptr to "Prohibit CheckSum Error\n" in ROM blob |
| DWORD_080172f8 | decode_char_frame_to_vram_assert_password_sz_ptr | ptr to "PassWord Size Error\n" in ROM blob |

decode_char_frame_to_vram store-base slot (resolved, see 求助 section):

| 槽 | slot_label | eol_ascii |
|---|---|---|
| DWORD_0801740c | decode_char_frame_to_vram_store_base_201 | byte store base: dst=0x201+r10 (r10=param r2 from prologue mov r10,r2 @0x0801723a); sibling base 0x200 at 0x080173ee |

BG VRAM fixed base slot:

| 槽 | slot_label | eol_ascii |
|---|---|---|
| DAT_080177d0 | setup_font_jp_ctx_bg_vram_fixed_vram_base | 0x06000020 = BG VRAM base + 0x20 (tile 1 start) |

String ID equate slots (small constant values, rename + EOL):

| 槽 | slot_label | eol_ascii |
|---|---|---|
| DAT_08017934 | load_game_str_pair_1004_to_state_str_id_a | str ID 0x1004 name-input str A |
| DAT_08017948 | load_game_str_pair_1004_to_state_str_id_b | str ID 0x1005 name-input str B |
| DAT_08017994 | load_game_str_1006_to_state_str_id | str ID 0x1006 name-input str C |

### FUNC_RENAME (误名订正, 如有)

本段 15 函数名称经目视检查均与函数体操作一致, 无误名信号. 跳过 FUNC_RENAME.

Evidence:
- init_scrollbar_oam_slot_settings: 体内调用 init_scrollbar_oam_entry + ldr gState+0xc1<<2 -- 与名称一致 (asm L8642-L8667)
- name_input_page_init: 体内写 DISPCNT/BGnCNT/gl_set_brightness/gl_state_init/reset_ig2d_load_counters/write_name_input_mode_flag -- 与名称一致 (asm L8670-L8727)
- dispatch_text_render_by_mode: 体内 cmp #0x20/#0x80 + 多路 text_render_wrapper -- 与名称一致 (asm L8730)
- apply_sprite_gfx_by_type: 体内 apply_gfx_resource_list -- 与名称一致 (asm L8833)

### PLATE (R5; full 重写 或 substring 替换)

以下函数 plate 含 FUN_ 过时引用需更新 (substring 替换):

1. validate_complement_checksum (L8175):
   plate 当前引用 "FUN_0801722c" -> 替换为 "decode_char_frame_to_vram"
   Evidence: asm L8175 "Called by FUN_0801722c after XOR decode"

2. compute_floor_log2 (L8492):
   plate 当前引用 "FUN_08017478 and FUN_080174e8" -> 替换为 "unpack_bits_to_byte_buf and pack_bytes_to_vram_bits"
   Evidence: asm L8492 "Callers FUN_08017478 and FUN_080174e8"

3. unpack_bits_to_byte_buf (L8511):
   plate 当前引用 "FUN_0801722c" -> 替换为 "decode_char_frame_to_vram"
   Evidence: asm L8512 "Called by FUN_0801722c"

4. pack_bytes_to_vram_bits (L8574):
   plate 当前引用 "FUN_0801722c" -> 替换为 "decode_char_frame_to_vram"
   Evidence: asm L8575 "Called by FUN_0801722c"

其余函数 plate 无 FUN_ 引用, 无需改动.

---

## carve 计划 (R7) -- rom.s incbin 切割

### Carve 1: char_frame_decode_lut @ 0x09e3a660 (272 B)

当前覆盖: `.incbin "roms/2343.gba", 0x1E3A65E, 0x112` (rom.s L914 行 assert_expr_zero_65c 后缀)

拆分为:
```
    .incbin "roms/2343.gba", 0x1E3A65E, 0x2     @ 2B align pad after assert_expr_zero_65c
char_frame_decode_lut:                            @ 0x09e3a660
    .incbin "roms/2343.gba", 0x1E3A660, 0x110   @ 272B: 68 entries x 4B halfword-pair decode LUT
                                                  @ LUT[2*char_idx + encode_mode] -> VRAM halfword
                                                  @ Consumed by: decode_char_frame_to_vram DWORD_08017410
```
Coverage check: 0x2 + 0x110 = 0x112 == original size. Byte-identical preserved.

代码侧 R3 ref: DWORD_08017410 slot_label -> `decode_char_frame_to_vram_lut_ptr` pointing to `char_frame_decode_lut`

### Carve 2: sprite_gfx_type_meta + sprite_palette_type_table @ 0x09e3afc8 (20 B)

当前覆盖: `.incbin "roms/2343.gba", 0x1E3A78D, 0xB2B` (rom.s L920, assert_pdst_nameid 后缀)

拆分为:
```
    .incbin "roms/2343.gba", 0x1E3A78D, 0x83B   @ 2107B: up to sprite_gfx_type_meta
sprite_gfx_type_meta:                             @ 0x09e3afc8
    .word 0x031e0000                              @ type0: [tile_start=0x00, tile_count=0x1e, screen_page=0x03, ...]
    .word 0x061e0300                              @ type1
    .word 0x081e0600                              @ type2
    .word 0x0a1e0800                              @ type3 (4 entries x 4B = 16B)
sprite_palette_type_table:                        @ 0x09e3afd8
    .byte 1, 1, 16, 16                            @ palette indices for sprite types 0..3 (4B)
    .incbin "roms/2343.gba", 0x1E3AFDC, 0x2DC   @ 732B: remainder of blob to 0x1E3B2B8
```
Coverage check: 0x83B + 16 + 4 + 0x2DC = 0x83B + 0x14 + 0x2DC = 0xB2B == original size. Byte-identical preserved.

代码侧 R3 ref:
- DAT_0801777c slot -> `apply_sprite_gfx_by_type_meta_ptr` pointing to `sprite_gfx_type_meta`
- DAT_08017780 slot -> `apply_sprite_gfx_by_type_pal_table_ptr` pointing to `sprite_palette_type_table`

---

## disasm 计划 (R4, 如有)

无. ROM_INCBIN 0x17424/0x40 全 ROM 0 引用, 判定 §5.1 登记, 不做 disasm.

---

## 新增 constants / 全局

### 新建 constants/name_input.inc

```
@ =============================================================================
@ Name-input / banlist page constants (NameInput/Name_main.c, PassInput/Pass_main.c)
@ =============================================================================

@ bios_cpu_set fill-zero control words
.equ CHAR_FRAME_DECODE_CPUSET_CTRL, 0x01000168  @ fill 0x168 halfwords (360 x 2B = 720B)
                                                 @ used by decode_char_frame_to_vram to zero stack buf
.equ NAME_INPUT_STATE_CPUSET_CTRL,  0x050000c9  @ fill+32bit 0xc9 words (201 x 4B = 804B)
                                                 @ used by name_input_page_init to zero gState

@ BG layer control register init values for name-input page
.equ NAME_INPUT_BG0CNT_INIT, 0x00001c02  @ BG0: pri=2 scrbase=28 charbase=0 16col 32x32
.equ NAME_INPUT_BG1CNT_INIT, 0x00001d8c  @ BG1: pri=0 scrbase=29 charbase=3 256col 32x32
.equ NAME_INPUT_BG2CNT_INIT, 0x00001e8d  @ BG2: pri=1 scrbase=30 charbase=3 256col 32x32
.equ NAME_INPUT_BG3CNT_INIT, 0x00001f8f  @ BG3: pri=3 scrbase=31 charbase=3 256col 32x32

@ gSettings base+offset split (used in load_game_str_*_to_state funcs)
.equ GSETTINGS_OFFSET, 0x00006c2c        @ offset of gSettings from EWRAM_BASE
```

### 追加至 constants/ewram.inc

```
.equ gState,    0x02029250  @ name-input / banlist page state struct (804B cleared by NAME_INPUT_STATE_CPUSET_CTRL)
                             @ +0x8d = name display buffer (14B); +0x304 = scrollbar OAM slot;
                             @ +0x6c2c = gSettings language byte (bits[2:0])
                             @ 37 ROM refs; consumers: init_scrollbar_oam_slot_settings,
                             @   name_input_page_init, apply_sprite_gfx_by_type,
                             @   load_game_str_pair_1004_to_state, load_game_str_1006_to_state, ...

.equ gFontJpCtx, 0x02006ed0 @ JP font render context struct (~0x68B based on stride)
                              @ +0x4  = fn_ptr (indexed from font_jp_base_table by mode bits)
                              @ +0x8  = mode_flags (bit1=double-byte, bit2=? used by setup_font_jp_ctx_*)
                              @ +0x15 = active_flag (bit5=0x20 = glyph active)
                              @ 202 ROM refs; consumers: setup_font_jp_ctx_bg_vram_fixed,
                              @   setup_font_jp_ctx_obj_vram_row
```

### 追加至 constants/oam_attr.inc

```
.equ OAM_ATTR0_HIDDEN,             0x0000ffff  @ attr0 all-bits-set: OBJ disabled/hidden mode
                                                 @ used by apply_sprite_gfx_by_type for initial hide
```

注 (reviewer C5): 0xffffc07f (clear attr2 bits[13:7] palette field) **复用** gfx_resource.inc 已有的
`GFX_ATTR_CLEAR_BITS_13_7` (Seg-5b 建, 同值), 不在 oam_attr.inc 新建 OAM_ATTR2_PALETTE_CLEAR_MASK。

### 追加至 constants/gba_mem.inc

```
.equ EWRAM_BASE, 0x02000000  @ External Work RAM base (256KB, 0x02000000..0x0203FFFF)
                              @ 4295 ROM refs; used in base+offset form for gSettings etc.
```

先证明现有 inc 无可复用:
- gState=0x02029250: grep constants/ 未找到. 新建.
- gFontJpCtx=0x02006ed0: grep constants/ 未找到. 新建.
- 0xffffc07f (palette clear mask): **复用** gfx_resource.inc 的 GFX_ATTR_CLEAR_BITS_13_7 (Seg-5b 已建, 同值). 不新建.
- OAM_ATTR0_HIDDEN=0xffff: oam_attr.inc 无. 新建.
- EWRAM_BASE=0x02000000: gba_mem.inc 仅有 GBA_PALRAM_BASE/OBJ_PALRAM_BASE/GBA_VRAM_BASE/OBJ_TILE_VRAM_BASE/GBA_OAM_BASE. 无 EWRAM_BASE. 新建.

---

## §5.1 登记 (Rule 3) -- 0 引用块

| 地址 | 大小 | 所在 Seg | 初判内容 | 状态 |
|---|---|---|---|---|
| 0x08017424 | 64 B (ROM_INCBIN 0x17424, 0x40) | Seg-5d | 2 个 THUMB 孤儿小函数: (1) 0x17424..0x17444 = bitfield-index helper (r2 mod 4 类操作); (2) 0x17448..0x17462 = halfword-pair extractor (从 r0 addr 读 2 halfwords 按 shift 合并); 均 dead code, 0 外部 ROM 引用 (raw+THUMB 全扫均 0). **留待**: 引用到时 R4 disasm + createFunction |

---

## 消费者证据 (R6) -- 关键槽语义的 file:line + 置信度

| 槽/全局 | 消费者 file:line | 置信度 |
|---|---|---|
| gState=0x02029250 | asm/00_system_str_vija.s L8634 plate `gState+0x304=0x02029554` scrollbar slot; L8715 DAT_080175d8 in name_input_page_init zero-fill; L9177 DAT_08017930 in load_game_str_pair_1004_to_state `adds r5,#0x8d` offset | high |
| gFontJpCtx=0x02006ed0 | asm/00_system_str_vija.s L8948 plate `CTX_BASE=0x02006ed0`; L8958 `ldrb r1,[r2,#0x15]` -> bit5 flag; L8962 `ldrb r0,[r2,#0x8]` -> mode_flags | high |
| char_frame_decode_lut=0x09e3a660 | asm/00_system_str_vija.s L8349 `ldr r6, DWORD_08017410`; L8373 `ldrh r2,[r6,#0]` decode loop | high |
| sprite_gfx_type_meta=0x09e3afc8 | asm/00_system_str_vija.s L8833 plate `ROM_GFX_META=0x09e3afc8`; L8848 `ldmia r0!,{r2,r3,r6}` loads 3 words | high |
| sprite_palette_type_table=0x09e3afd8 | asm/00_system_str_vija.s L8833 plate `PALETTE_TABLE=0x09e3afd8 ([1,1,16,16])` | high |
| OAM_ATTR2_PALETTE_CLEAR_MASK | asm/00_system_str_vija.s L8930 `ldrh r3,[r1,#0x18]; ands r0,r3` clear palette bits | high |
| OAM_ATTR0_HIDDEN | asm/00_system_str_vija.s L8912 `strh r0,[r1,#0x10]` write 0xffff to attr0 | high |
| NAME_INPUT_BGnCNT_INIT values | asm/00_system_str_vija.s L8685-L8696: 4 sequential `ldr r0, DAT_; strh r0,[r1,#0]` to BG0-3CNT mmio | high |
| CHAR_FRAME_DECODE_CPUSET_CTRL | asm/00_system_str_vija.s L8219 plate `BIOS_CPUSET_CTRL=0x01000168`; L8315 `.word 0x01000168` slot used in bios_cpu_set call | high |
| DWORD_08017420=0x3e9c | asm/00_system_str_vija.s L8443-L8444 `ldr r0,DWORD_08017420; adds r2,r2,r0` -- vram_step accumulator in bitfield write loop | med |
| assert strings 0x09e3a790/0x09e3a7ac | asm/00_system_str_vija.s L8219 plate `Prohibit CheckSum Error\n` / `PassWord Size Error\n`; confirmed by ROM content at 0x1e3a790/0x1e3a7ac | high |

---

## 求助 (BLOCKED 项) — RESOLVED by driver (static, no mGBA)

### DWORD_0801740c = 0x00000201 — resolved as factual RENAME_SLOT (not blocked)

Context (asm/00_system_str_vija.s L8338-8340):
```
    ldr r0, DWORD_0801740c   @ 0x201
    add r0,r10               @ r10 = param r2 (mov r10,r2 @0x0801723a, sole r10 def in body)
    strb r1,[r0,#0]          @ [0x201+r10].b = byte
```

Driver investigation (verified static facts):
1. r10 is defined ONLY at 0x0801723a (`mov r10,r2`); within body 0x0801722c..0x08017462 it is used at 0x08017302 and 0x080173ee and restored from r5 only in the epilogue (0x08017402 `mov r10,r5`). So r10 == param r2 throughout the body. (grep: only 2 high-reg movs target r10; only 2 `add r0,r10` uses.)
2. **decode_char_frame_to_vram (0x0801722c) has 0 references in the entire ROM**: 0 `bl`, raw `d.count(struct.pack('<I',0x0801722c))`=0, THUMB+1 `0x0801722d`=0. It is an orphan/dead function — never reached at runtime, so r10's runtime value is unobservable and the store target is moot.

Decision: NOT a runtime block (function never executes). Symbolize the slot with a factual name + ASCII EOL stating only verified static facts; no semantic claim about dead-write/BIOS, no `可能/似乎`. See RENAME_SLOTS table.

Open item recorded for the NAMING phase (doc/ only, not Ghidra): the existing plate (L8219) calls param r2 "encode mode (0/1)", but r2 (via r10) is used as a STORE BASE for `[0x200/0x201 + r2].b` — tension between "mode" and "pointer/offset-base" interpretation. Combined with the 0-ref orphan status, this is a naming-phase plate-review candidate (R5), not a refine action; left unchanged here to avoid fabricating the opposite interpretation.

---

## 自检结果

1. EQ values vs ROM: all 38 slot values verified via python `struct.unpack_from('<I', d, off)[0]` match expected. (no mismatches)
2. carve ptr THUMB check: char_frame_decode_lut and sprite_gfx_type_meta/sprite_palette_type_table are DATA tables (not fn pointers), no +1 needed.
3. Plate/EOL ASCII: all proposed texts are pure ASCII (no CJK).
4. §5.1 block 0x17424/0x40: ref-scan confirmed 0 raw + 0 THUMB refs across all 16 aligned sub-addresses.
5. Slot name format: all labels use `^[a-z][a-z0-9_]+$`; duplicate sp-offset slots use `_b/_c` suffix.
