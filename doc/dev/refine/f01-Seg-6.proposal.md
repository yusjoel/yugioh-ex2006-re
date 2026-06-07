# Refine Proposal: f01-Seg-6  [0x0801f25c..0x08020fa8)

## 段测绘

- 范围: GBA ROM [0x0801f25c, 0x08020fa8) = 16 named functions + 4 ROM_INCBIN blocks
- Seg-7 边界: 0x08020fa8 = `render_lp_record_text_set_b:` push {r4,r5,r6,lr} @ 0x08020fa8

### 函数入口列表 (全 < 0x20fa8)

| 地址 | 函数名 | asm 行 |
|---|---|---|
| 0x0801f25c | append_game_text_if_raw | 5165 |
| 0x0801f280 | format_int_to_decimal_text | 5185 |
| 0x0801f2c4 | format_game_text_with_text_arg | 5220 |
| 0x0801f338 | format_game_text_with_int_arg | 5283 |
| 0x0801f398 | check_siocnt_link_ready | 5341 |
| 0x0801f3b0 | read_prng_entry_flag_clear | 5357 |
| 0x0801f3d4 | return_void_noop_stub | 5377 |
| 0x0801f3d8 | return_zero_leaf | 5383 |
| 0x0801f3dc | return_noop_leaf | 5389 |
| 0x0801f3e4 | return_one_leaf | 5398 |
| 0x0801f3e8 | find_deck_record_index_by_key | 5408 |
| 0x0801f40c | find_card_index_in_rom_table | 5437 |
| 0x0801f444 | tick_duel_puzzle_scene_step | 5478 |
| 0x0801fe92 | poll_fadein_exit_to_duel_state | 5555 |
| 0x0801fec0 | run_duel_puzzle_scene_state_machine | 5582 |
| 0x08020db4 | render_lp_record_text_set_a | 6152 |

- 4 ROM_INCBIN 块: 0x1f4d0/0x690, 0x1fb90/0x302, 0x202fe/0x36, 0x20370/0xa44
- 残留自动名槽: DAT_* x50+, DWORD_* x25+ (本提案逐函数处理)

---

## 数据块分类 (Rule 2/3) - 逐块 ref-scan 证据

### ref-scan 方法

```python
import struct
d = open("roms/2343.gba","rb").read()
gba_base = 0x08000000
# For block at GBA addr A, size S:
# scan all ROM words for values v where A <= (v & ~1) < A+S
# report (rom_offset, gba_addr, v, is_thumb=(v&1))
```

### Block 1: 0x1f4d0, 0x690 (1680 B)

ref-scan 结果:
- 块内地址有 ref 总计 **95 个** (含块外引用 87 个 + 段内 step-table 8 个)
- 块入口 raw=0 (0x801f4d0 raw=0), THUMB 0x801f4d1=0 (start addr 无直接外部函数调用)
- step-table PTR_DAT_0801f47c @ asm 5507 条目 0..7 全指向块内地址:
  - case 0: 0x0801f4d0 raw=1, thumb=0
  - case 1: 0x0801f5ec raw=2, thumb=1
  - case 2: 0x0801f60c raw=1, thumb=1
  - case 3: 0x0801f738 raw=1, thumb=0
  - case 4: 0x0801f9c4 raw=1, thumb=0
  - case 5: 0x0801f9e0 raw=1, thumb=0
  - case 6: 0x0801fb20 raw=1, thumb=0
  - case 7: 0x0801fb2c raw=1, thumb=0
- 外部 THUMB refs 示例: ROM[0x123d64]=0x801faf3 thumb=1, ROM[0x141a58]=0x801faf3 thumb=1, ROM[0x18f1c8]=0x801f611 thumb=1 ...
- 首字节 bytes: `0d f0 d0 fd 38 4e 39 4b ...` -> h0=0xf00d, h1=0xfdd0 -> **BL upper/lower pair = THUMB BL**

判定: **disasm R4**

理由: THUMB BL 指令开头; step-table PTR_DAT_0801f47c (tick_duel_puzzle_scene_step @ 0x1f444) 引用内部地址; 外部 87 ref 含大量 THUMB+1 函数调用. 块内为 tick_duel_puzzle_scene_step step cases 0..7 (state machine sub-handlers).

消费者: tick_duel_puzzle_scene_step @ 0x0801f444 (asm line 5478); step-table PTR_DAT_0801f47c @ asm line 5507. 置信度 high.

### Block 2: 0x1fb90, 0x302 (770 B)

ref-scan 结果:
- 块内地址有 ref 总计 **104 个** (外部 86 + 段内 18)
- PTR_DAT_0801fb64 @ asm 5532 (10-entry sub-dispatch table) 条目全指向块内:
  - 0x0801fb90 raw=1, 0x0801fb94 raw=1, 0x0801fb98 raw=1, 0x0801fb9c raw=1,
  - 0x0801fbb2 raw=1, 0x0801fbbe raw=6 (repeated), 0x0801fe7c raw=1
- step-table PTR_DAT_0801f47c cases 8..13,20 全指向块内:
  - case 8: 0x0801fbe4 raw=1, case 9: 0x0801fc18 raw=2 (thumb=0+1)
  - case 10: 0x0801fd48 raw=1, case 11: 0x0801fd80 raw=1
  - case 12: 0x0801fe14 raw=1 (thumb=1), case 13: 0x0801fe54 raw=1, case 20: 0x0801fe7c raw=1
- 外部 THUMB refs 示例: ROM[0x11e58c]=0x801fc04 thumb=0, ROM[0x13218c]=0x801fd07 thumb=1, ROM[0x14fe2c]=0x801fdff thumb=1 ...
- 首字节 bytes: `19 20 09 e0 ...` -> h0=0x2019 (movs r1,#0x19), h1=0xe009 (b +0x14) -> **THUMB instructions**

判定: **disasm R4**

理由: THUMB movs/branch 指令开头; step-table PTR_DAT_0801f47c cases 8..13,20 全引用块内地址; sub-dispatch table PTR_DAT_0801fb64 (step 7 内部) 也指向块内. 块内为 tick_duel_puzzle_scene_step step cases 8..13,20 + sub-handler cluster.

消费者: tick_duel_puzzle_scene_step @ 0x0801f444 (asm line 5478); PTR_DAT_0801fb64 sub-dispatch (owned by step 7 body in block 1). 置信度 high.

### Block 3: 0x202fe, 0x36 (54 B)

ref-scan 结果:
- 块内地址有 ref 总计 **19 个**
- 外部 THUMB refs (来自段外): ROM[0xe2f40]=0x8020301 thumb=1, ROM[0x13e280]=0x8020301 thumb=1, ROM[0x17dbac]=0x8020303 thumb=1, ROM[0x474eec]=0x8020309 thumb=1, ROM[0x495290]=0x8020307 thumb=1 ...
- 内容解码:
  - byte +0..+1 (@ 0x202fe): `00 00` = 2-byte alignment pad
  - byte +2 (@ 0x20300): `f0 b5` = push {r4,r5,r6,r7,lr} -> **THUMB function prologue**
  - bytes: `57 46 4e 46 45 46 e0 b4 a2 b0` = mov r7,r10; mov r6,r9; mov r5,r8; push {r5,r6,r7}; sub sp,#0x28
  - ldr r0,[pc+28] -> literal 0x03000040 (gPrng); ldr r1,[pc+32] -> 0x00000202
  - adds r0,r0,r1; ldrh r0,[r0,#0] -> reads gPrng+0x202 halfword
  - lsls r0,r0,#0x12; lsrs r0,r0,#0x18 -> extract bits[13:6] = step index
  - cmp r0,#0x0d; bls +6 -> if >13 call overflow handler (at bl target 0x20324+offset)
  - else: ldr r1,[pc,#0x10] -> literal at 0x20336 = 0x08020338 (step table base)
  - ldr r0,[r0,#0]; .hword 0x4687 (mov r15,r0) -> tail-call dispatch
  - 14 cases (cmp r0,#0x0d = compare 0..13)
- External THUMB+1 ref at ROM[0xe2f40] (GBA=0x80e2f40) = gMenuState+0x234 fn-ptr table entry

判定: **disasm R4**

理由: 2 pad bytes + full THUMB function at 0x08020300; 19 external refs including THUMB+1 fn-ptr refs; identical dispatch pattern to tick_duel_puzzle_scene_step; 14-case step machine reading gPrng+0x202. Context at fn-ptr table (ROM[0xe2f3c]=0x02029590=gMenuState, ROM[0xe2f40]=0x8020301 THUMB ref): this is a gMenuState step function assigned to +0x234 slot.

消费者: gMenuState+0x234 fn-ptr slot (ROM[0xe2f40]=0x8020301+1 THUMB ref); step table at 0x08020338 dispatches cases 0..13 to block 4. 置信度 high.

### Block 4: 0x20370, 0xa44 (2628 B)

ref-scan 结果:
- 块内地址有 ref 总计 **110 个** (外部 96 + 段内 14 step-table refs)
- step-table PTR_DAT_08020338 @ asm 6126 (14 entries) 全指向块内:
  - case 0: 0x8020370, case 1: 0x8020524, case 2: 0x8020544, case 3: 0x8020670
  - case 4: 0x80209f4, case 5: 0x8020a10, case 6: 0x8020b50, case 7: 0x8020b6c
  - case 8: 0x8020b88, case 9: 0x8020ba4, case 10: 0x8020d00, case 11: 0x8020d34
  - case 12: 0x8020d94, case 13: 0x8020d4c
- 外部 THUMB refs 示例: ROM[0x1da4ac]=0x8020503 thumb=1, ROM[0x20cb68]=0x802040b thumb=1, ROM[0x262230]=0x8020403 thumb=1, ROM[0x263c14]=0x8020ceb thumb=1 ...
- 首字节 bytes: `0c f0 80 fe ...` -> h0=0xf00c, h1=0xfe80 -> **THUMB BL pair**
- 块尾 16 bytes: `a146 aa46 f0bc 02bc 0847 0000 a0e2 0102` -> pop+bx r1 epilogue + .word 0x0201e2a0

判定: **disasm R4**

理由: THUMB BL instruction at block start; PTR_DAT_08020338 (from dispatcher at 0x08020300) 14-entry step table all points within block; 110 refs total; block ends exactly at render_lp_record_text_set_a (0x08020db4); each sub-function is a step handler for the 14-case scene state machine.

消费者: dispatcher function at 0x08020300 (block 3) + PTR_DAT_08020338 @ asm line 6126. 置信度 high.

---

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate)

以下各函数的字面量池槽可符号化为已有 .equ 常量。EQ_SLOT label 名 = `<func>_<const_suffix>` 以避免 GAS PC-relative 冲突。

#### append_game_text_if_raw (0x0801f25c)

| 槽 | ROM off | 值 | const | 复用/新建 |
|---|---|---|---|---|
| DAT_0801f27c | 0x1f27c | 0xfffe0000 | GAME_STR_RAW_ID_MASK | 复用 ewram.inc |

Rename: `DAT_0801f27c` -> `append_game_text_if_raw_raw_id_mask`

#### format_game_text_with_text_arg (0x0801f2c4)

| 槽 | ROM off | 值 | const | 复用/新建 |
|---|---|---|---|---|
| DAT_0801f2f8 | 0x1f2f8 | 0xfffe0000 | GAME_STR_RAW_ID_MASK | 复用 ewram.inc |

Rename: `DAT_0801f2f8` -> `format_game_text_with_text_arg_raw_id_mask`

#### format_game_text_with_int_arg (0x0801f338)

| 槽 | ROM off | 值 | const | 复用/新建 |
|---|---|---|---|---|
| DAT_0801f358 | 0x1f358 | 0xfffe0000 | GAME_STR_RAW_ID_MASK | 复用 ewram.inc |

Rename: `DAT_0801f358` -> `format_game_text_with_int_arg_raw_id_mask`

#### check_siocnt_link_ready (0x0801f398)

| 槽 | ROM off | 值 | const | 复用/新建 |
|---|---|---|---|---|
| DWORD_0801f3ac | 0x1f3ac | 0x04000128 | SIOCNT | 复用 gba_io.inc |

Rename: `DWORD_0801f3ac` -> `check_siocnt_link_ready_siocnt`

EOL on renamed slot: `@ SIOCNT SIO Control Register`

#### read_prng_entry_flag_clear (0x0801f3b0)

| 槽 | ROM off | 值 | const | 复用/新建 |
|---|---|---|---|---|
| PTR_gPrng_0801f3c8 | 0x1f3c8 | 0x03000040 | gPrng | 复用 iwram.inc (already PTR_ prefixed - keep) |
| DAT_0801f3cc | 0x1f3cc | 0x00000584 | (raw offset, no existing const) | RENAME only |

PTR_gPrng_0801f3c8 已以 PTR_ 前缀命名 gPrng - 跳过 (no EQ needed).
DAT_0801f3cc rename -> `read_prng_entry_flag_clear_entry_offset` (value 0x584, no existing const; keep raw).

#### tick_duel_puzzle_scene_step (0x0801f444)

| 槽 | ROM off | 值 | const | 复用/新建 |
|---|---|---|---|---|
| PTR_gPrng_0801f470 | 0x1f470 | 0x03000040 | gPrng | 复用 (already PTR_) |
| DAT_0801f474 | 0x1f474 | 0x00000202 | (raw gPrng step offset) | RENAME only |
| DAT_0801f478 | 0x1f478 | 0x0801f47c | step table base ptr | RENAME only |
| PTR_DAT_0801f47c | 0x1f47c | ptr table | step table | keep as PTR_DAT_ |

DAT_0801f474 rename -> `tick_duel_puzzle_scene_step_step_idx_off`
DAT_0801f478 rename -> `tick_duel_puzzle_scene_step_table_base`

#### poll_fadein_exit_to_duel_state (0x0801fe92)

| 槽 | ROM off | 値 | const | 复用/新建 |
|---|---|---|---|---|
| DAT_0801fea8 | 0x1fea8 | 0x0201e2a0 | gDuelCardCtxBase | 复用 ewram.inc |

Rename: `DAT_0801fea8` -> `poll_fadein_exit_to_duel_state_duel_card_ctx_base`

消费者证据: asm line 5566-5567; plate说"reads [0x0201e2a0+0x224] (gDuelState+0x89*4)"; ewram.inc `.equ gDuelCardCtxBase, 0x0201e2a0`. 置信度 high.

#### run_duel_puzzle_scene_state_machine (0x0801fec0)

主状态机含多个 case handler 内联代码。各 case 共享数据槽:

| 槽 | ROM off | 值 | const | 复用/新建 |
|---|---|---|---|---|
| PTR_gPrng_0801feec | 0x1feec | 0x03000040 | gPrng | 复用 (PTR_) |
| DAT_0801fef0 | 0x1fef0 | 0x00000202 | step_idx_off | RENAME |
| DAT_0801fef4 | 0x1fef4 | 0x0801fef8 | step table base | RENAME |
| DAT_0801ffec | 0x1ffec | 0x02029e90 | (puzzle init area) | RENAME |
| PTR_gPrng_0801fff0 | 0x1fff0 | 0x03000040 | gPrng | 复用 (PTR_) |
| DAT_0801fff4 | 0x1fff4 | 0x0000023f | GPRNG_BANNER_FLAG_OFF | 复用 ewram.inc |
| DAT_0801fff8 | 0x1fff8 | 0x02023130 | gDuelFieldState | 复用 ewram.inc |
| DAT_0801fffc | 0x1fffc | 0xfffc03ff | GL_CLEAR_BITS_17_10 | 复用 gl_blend.inc |
| DAT_08020000 | 0x20000 | 0x00007530 | (puzzle card id 30000) | RENAME |
| DAT_08020004 | 0x20004 | 0x00000213 | (gDuelFieldState+0x213 offset) | RENAME |
| DAT_08020008 | 0x20008 | 0x0201e2a0 | gDuelCardCtxBase | 复用 ewram.inc |
| DAT_0802000c | 0x2000c | 0x09e59c2c | (puzzle_scenario_table ROM ptr) | RENAME |
| DAT_08020010 | 0x20010 | 0xfffffc03 | GL_CLEAR_BITS_9_2 | 复用 gl_blend.inc |
| DAT_08020014 | 0x20014 | 0x00000202 | step_idx_off | RENAME (dup) |
| DAT_08020018 | 0x20018 | 0xffffc03f | NAME_INPUT_PAGE_STATE_CLEAR? | verify |
| PTR_gPrng_0802003c | 0x2003c | 0x03000040 | gPrng | 复用 (PTR_) |
| DAT_08020040 | 0x20040 | 0x00000202 | step_idx_off | RENAME (dup) |
| PTR_gPrng_08020074 | 0x20074 | 0x03000040 | gPrng | 复用 (PTR_) |
| DAT_08020078 | 0x20078 | 0x00000203 | (gPrng+0x203 fade flag offset) | RENAME |
| DAT_08020134 | 0x20134 | 0x0201e2a0 | gDuelCardCtxBase | 复用 ewram.inc |
| DAT_08020138 | 0x20138 | 0x02000000 | EWRAM_BASE | 复用 gba_mem.inc |
| DAT_0802013c | 0x2013c | 0x00006c3c | (gDuelPuzzleProgress offset) | RENAME -> GSETTINGS_OFFSET+0x10? No - it's DuelPuzzle offset |
| DAT_08020140 | 0x20140 | 0x00001662 | (puzzle bonus DP = 5730) | RENAME |
| DAT_08020148 | 0x20148 | 0x00006c2c | GSETTINGS_OFFSET | 复用 name_input.inc |
| PTR_game_str_pointer_table_08020144 | 0x20144 | game_str_pointer_table | already REF | keep |
| PTR_game_str_ja_0802014c | 0x2014c | game_str_ja | already REF | keep |
| DAT_08020150 | 0x20150 | 0x00004b4e | (str JP offset) | RENAME (raw) |
| DAT_08020154 | 0x20154 | 0x0003f66a | (str offset) | RENAME (raw) |
| DAT_08020160 | 0x20160 | 0x000339ce | (str offset) | RENAME (raw) |
| DAT_0802016c | 0x2016c | 0x00027532 | (str offset) | RENAME (raw) |
| DAT_08020178 | 0x20178 | 0x0001b2a0 | (str offset) | RENAME (raw) |
| DAT_0802018c | 0x2018c | 0x0000fc06 | (str offset) | RENAME (raw) |
| DAT_0802019c | 0x2019c | 0x0201e2a0 | gDuelCardCtxBase | 复用 ewram.inc |
| PTR_gPrng_080201d0 | 0x201d0 | 0x03000040 | gPrng | 复用 (PTR_) |
| DAT_080201d4 | 0x201d4 | 0x00000203 | (gPrng+0x203 flag off) | RENAME (dup) |
| DAT_0802020c | 0x2020c | 0x02000000 | EWRAM_BASE | 复用 gba_mem.inc |
| DAT_08020210 | 0x20210 | 0x00006c2c | GSETTINGS_OFFSET | 复用 name_input.inc |
| DAT_08020214 | 0x20214 | 0x09dc01d8 | (lp_record str JP base) | RENAME (raw ROM ptr) |
| DAT_08020218 | 0x20218 | 0x0003ab80 | (lp_record str EN offset) | RENAME (raw) |
| DAT_08020220 | 0x20220 | 0x09def19a | (lp_record str DE addr) | RENAME (raw) |
| DAT_08020228 | 0x20228 | 0x09de2d00 | (lp_record str FR addr) | RENAME (raw) |
| DAT_08020230 | 0x20230 | 0x09dd6982 | (lp_record str IT addr) | RENAME (raw) |
| DAT_0802025c | 0x2025c | 0x09dcafac | (lp_record str ES addr) | RENAME (raw) |
| PTR_gPrng_08020260 | 0x20260 | 0x03000040 | gPrng | 复用 (PTR_) |
| DAT_08020264 | 0x20264 | 0x00000202 | step_idx_off | RENAME (dup) |
| DAT_08020268 | 0x20268 | 0xffffc03f | (step field clear mask) | RENAME |
| PTR_gPrng_080202a0 | 0x202a0 | 0x03000040 | gPrng | 复用 (PTR_) |
| DAT_080202a4 | 0x202a4 | 0x00000202 | step_idx_off | RENAME (dup) |
| DAT_080202a8 | 0x202a8 | 0xffffc03f | (step field clear mask) | RENAME (dup) |
| DAT_080202cc | 0x202cc | 0x02023360 | gDuelSceneBase | 复用 ewram.inc |
| DAT_080202d0 | 0x202d0 | 0x0201e2a0 | gDuelCardCtxBase | 复用 ewram.inc |
| DAT_080202e8 | 0x202e8 | 0x0201e2a0 | gDuelCardCtxBase | 复用 ewram.inc |

#### render_lp_record_text_set_a (0x08020db4)

| 槽 | ROM off | 值 | const | 复用/新建 |
|---|---|---|---|---|
| DWORD_08020f50 | 0x20f50 | 0x02000000 | EWRAM_BASE | 复用 gba_mem.inc |
| DWORD_08020f54 | 0x20f54 | 0x00006c2c | GSETTINGS_OFFSET | 复用 name_input.inc |
| DWORD_08020f58 | 0x20f58 | 0x09dc2e62 | (lp_str JP base) | RENAME (raw) |
| DWORD_08020f5c | 0x20f5c | 0x0003ae88 | (lp_str EN offset) | RENAME (raw) |
| DWORD_08020f64 | 0x20f64 | 0x09df2086 | (lp_str DE addr) | RENAME (raw) |
| DWORD_08020f6c | 0x20f6c | 0x09de5d9c | (lp_str FR addr) | RENAME (raw) |
| DWORD_08020f74 | 0x20f74 | 0x09dd9a36 | (lp_str IT addr) | RENAME (raw) |
| DWORD_08020f98 | 0x20f98 | 0x09dcda66 | (lp_str ES addr) | RENAME (raw) |
| DWORD_08020df0..ef0 (card ID comparison keys) | various | 0x1788,0x146e,0x112e,0xfe9,0x111c,0x1388,0x138a,0x15fa,0x15b1,0x1643,0x1954,0x183d,0x17c9,0x1905,0x1936,0x19a5,0x19d6,0x19ef | card IDs (binary search pivots) | RENAME as `_cid_<hex>` |

---

### REF_SLOTS (USER-label + DATA-ref)

以下槽需 createLabel (Ghidra) + 代码侧接通引用:

| 槽 | 目标 | gas label | 理由 |
|---|---|---|---|
| DAT_0801f428 | 0x098973f6 | find_card_index_in_rom_table_count_ptr | ROM table count halfword (no existing carve label) |
| DAT_0801f42c | 0x098972f0 | find_card_index_in_rom_table_data_ptr | ROM table data base (no existing carve label) |

注: 这两个 ROM 地址 (0x098973f6 / 0x098972f0) 均在远端数据区, 非本段 ROM_INCBIN 块。只做 RENAME_SLOT (槽名 label), 不 carve (不知道表大小边界)。

PTR_deck_record_table_0801f3f8 已引用 `deck_record_table` label (已 carve) - 跳过。
PTR_game_str_pointer_table_08020144 已引用 `game_str_pointer_table` - 跳过。
PTR_game_str_ja_0802014c 已引用 `game_str_ja` - 跳过。

---

### RENAME_SLOTS (纯改名 + EOL)

全量 RENAME 清单 (排除已 EQ / 已 PTR_ 正确命名的):

| 原槽名 | 新槽名 | EOL |
|---|---|---|
| DAT_0801f27c | append_game_text_if_raw_raw_id_mask | GAME_STR_RAW_ID_MASK |
| DAT_0801f2f8 | format_game_text_with_text_arg_raw_id_mask | GAME_STR_RAW_ID_MASK |
| DAT_0801f358 | format_game_text_with_int_arg_raw_id_mask | GAME_STR_RAW_ID_MASK |
| DWORD_0801f3ac | check_siocnt_link_ready_siocnt | SIOCNT |
| DAT_0801f3cc | read_prng_entry_flag_clear_entry_offset | offset 0x584 |
| DAT_0801f474 | tick_duel_puzzle_scene_step_step_idx_off | gPrng+0x202 step index offset |
| DAT_0801f478 | tick_duel_puzzle_scene_step_table_base | step fn-ptr table base |
| DAT_0801fea8 | poll_fadein_exit_to_duel_state_duel_card_ctx_base | gDuelCardCtxBase |
| DAT_0801fef0 | run_duel_puzzle_scene_step_idx_off | gPrng+0x202 step index offset |
| DAT_0801fef4 | run_duel_puzzle_scene_table_base | step fn-ptr table base |
| DAT_0801ffec | run_duel_puzzle_scene_puzzle_init_area | 0x02029e90 puzzle display area |
| DAT_0801fff4 | run_duel_puzzle_scene_banner_flag_off | GPRNG_BANNER_FLAG_OFF |
| DAT_0801fff8 | run_duel_puzzle_scene_duel_field_state | gDuelFieldState |
| DAT_0801fffc | run_duel_puzzle_scene_oam_char_clear | GL_CLEAR_BITS_17_10 |
| DAT_08020000 | run_duel_puzzle_scene_puzzle_card_id | 0x7530=30000 puzzle starting card ID |
| DAT_08020004 | run_duel_puzzle_scene_puzzle_card_slot_off | gDuelFieldState+0x213 puzzle card index field |
| DAT_08020008 | run_duel_puzzle_scene_duel_card_ctx | gDuelCardCtxBase |
| DAT_0802000c | run_duel_puzzle_scene_scenario_table | 0x09e59c2c puzzle scenario ROM pointer table |
| DAT_08020010 | run_duel_puzzle_scene_blend_clear_a | GL_CLEAR_BITS_9_2 |
| DAT_08020014 | run_duel_puzzle_scene_step_idx_off_b | gPrng+0x202 (dup) |
| DAT_08020018 | run_duel_puzzle_scene_step_field_clear | 0xffffc03f step index clear mask (bits[13:6]) |
| DAT_08020040 | run_duel_puzzle_case2_step_idx_off | gPrng+0x202 (dup case 2) |
| DAT_08020078 | run_duel_puzzle_case3_fadein_flag_off | gPrng+0x203 fadein flag offset |
| DAT_08020134 | run_duel_puzzle_case4_duel_card_ctx | gDuelCardCtxBase |
| DAT_08020138 | run_duel_puzzle_case4_ewram_base | EWRAM_BASE |
| DAT_0802013c | run_duel_puzzle_case4_puzzle_progress_off | 0x6c3c=gDuelPuzzleProgress offset from EWRAM_BASE |
| DAT_08020140 | run_duel_puzzle_case4_bonus_dp | 0x1662=5730 DP puzzle bonus |
| DAT_08020148 | run_duel_puzzle_case4_gsettings_off | GSETTINGS_OFFSET |
| DAT_08020150 | run_duel_puzzle_case4_str_off_jp | 0x4b4e str offset into game_str_ja |
| DAT_08020154 | run_duel_puzzle_case4_str_off_en | 0x3f66a str offset |
| DAT_08020160 | run_duel_puzzle_case4_str_off_de | 0x339ce str offset |
| DAT_0802016c | run_duel_puzzle_case4_str_off_fr | 0x27532 str offset |
| DAT_08020178 | run_duel_puzzle_case4_str_off_it | 0x1b2a0 str offset |
| DAT_0802018c | run_duel_puzzle_case4_str_off_es | 0xfc06 str offset |
| DAT_0802019c | run_duel_puzzle_case4_duel_card_ctx_b | gDuelCardCtxBase |
| DAT_080201d4 | run_duel_puzzle_case5_fadein_flag_off | gPrng+0x203 fadein flag offset |
| DAT_0802020c | run_duel_puzzle_case6_ewram_base | EWRAM_BASE |
| DAT_08020210 | run_duel_puzzle_case6_gsettings_off | GSETTINGS_OFFSET |
| DAT_08020214 | run_duel_puzzle_case6_str_jp_base | 0x09dc01d8 lp_record str JP base |
| DAT_08020218 | run_duel_puzzle_case6_str_en_off | 0x3ab80 EN offset |
| DAT_08020220 | run_duel_puzzle_case6_str_de | 0x09def19a |
| DAT_08020228 | run_duel_puzzle_case6_str_fr | 0x09de2d00 |
| DAT_08020230 | run_duel_puzzle_case6_str_it | 0x09dd6982 |
| DAT_0802025c | run_duel_puzzle_case6_str_es | 0x09dcafac |
| DAT_08020264 | run_duel_puzzle_case6_step_idx_off | gPrng+0x202 (dup case 6) |
| DAT_08020268 | run_duel_puzzle_case6_step_clear | 0xffffc03f (dup) |
| DAT_080202a4 | run_duel_puzzle_case7_step_idx_off | gPrng+0x202 (dup case 7) |
| DAT_080202a8 | run_duel_puzzle_case7_step_clear | 0xffffc03f (dup) |
| DAT_080202cc | run_duel_puzzle_case8_duel_scene | gDuelSceneBase |
| DAT_080202d0 | run_duel_puzzle_case8_duel_card_ctx | gDuelCardCtxBase |
| DAT_080202e8 | run_duel_puzzle_fadein_duel_card_ctx | gDuelCardCtxBase |
| DWORD_08020f50 | render_lp_record_set_a_ewram_base | EWRAM_BASE |
| DWORD_08020f54 | render_lp_record_set_a_gsettings_off | GSETTINGS_OFFSET |
| DWORD_08020f58 | render_lp_record_set_a_str_jp_base | 0x09dc2e62 lp str JP base |
| DWORD_08020f5c | render_lp_record_set_a_str_en_off | 0x3ae88 EN offset |
| DWORD_08020f64 | render_lp_record_set_a_str_de | 0x09df2086 |
| DWORD_08020f6c | render_lp_record_set_a_str_fr | 0x09de5d9c |
| DWORD_08020f74 | render_lp_record_set_a_str_it | 0x09dd9a36 |
| DWORD_08020f98 | render_lp_record_set_a_str_es | 0x09dcda66 |
| DWORD_08020df0 | render_lp_record_set_a_cid_1788 | card ID 0x1788 pivot |
| DWORD_08020df4 | render_lp_record_set_a_cid_146e | card ID 0x146e pivot |
| DWORD_08020df8 | render_lp_record_set_a_cid_112e | card ID 0x112e pivot |
| DWORD_08020dfc | render_lp_record_set_a_cid_0fe9 | card ID 0x0fe9 pivot |
| DWORD_08020e0c | render_lp_record_set_a_cid_111c | card ID 0x111c pivot |
| DWORD_08020e24 | render_lp_record_set_a_cid_1388 | card ID 0x1388 pivot |
| DWORD_08020e2c | render_lp_record_set_a_cid_138a | card ID 0x138a pivot |
| DWORD_08020e4c | render_lp_record_set_a_cid_15fa | card ID 0x15fa pivot |
| DWORD_08020e5c | render_lp_record_set_a_cid_15b1 | card ID 0x15b1 pivot |
| DWORD_08020e74 | render_lp_record_set_a_cid_1643 | card ID 0x1643 pivot |
| DWORD_08020e9c | render_lp_record_set_a_cid_1954 | card ID 0x1954 pivot |
| DWORD_08020ea0 | render_lp_record_set_a_cid_183d | card ID 0x183d pivot |
| DWORD_08020eb0 | render_lp_record_set_a_cid_17c9 | card ID 0x17c9 pivot |
| DWORD_08020ec4 | render_lp_record_set_a_cid_1905 | card ID 0x1905 pivot |
| DWORD_08020ed4 | render_lp_record_set_a_cid_1936 | card ID 0x1936 pivot |
| DWORD_08020ef0 | render_lp_record_set_a_cid_19a5 | card ID 0x19a5 pivot |
| DWORD_08020f0c | render_lp_record_set_a_cid_19d6 | card ID 0x19d6 pivot |
| DWORD_08020f4c | render_lp_record_set_a_cid_19ef | card ID 0x19ef pivot |

---

### FUNC_RENAME (误名订正)

- **run_duel_puzzle_scene_state_machine**: 检查函数体 - 9 case dispatch reading gPrng+0x202 bits[13:6]. 函数名准确描述了其行为. indeg: fn-ptr table entry (ROM[0xe1c88]=0x0801fec1 THUMB+1). 无误名. 不 FUNC_RENAME.
- 其余 15 函数: 名称与函数体操作一致. 无 FUNC_RENAME 候选.

---

### PLATE (R5)

需要修正的 CJK plate:

1. **run_duel_puzzle_scene_state_machine** @ asm line 5581:
   - 现有 plate 含大量 CJK 字符 (如"场景主状态机入口","初始化","主对局帧" 等)
   - 必须替换为纯 ASCII
   - ASCII 版本 (plate 全文替换):

```
@ Entry: gMenuState+0x234 fn-ptr (ROM[0x080e1c88]=0x0801fec1 THUMB+1), called each frame
@ by scene dispatcher. Reads gPrng+0x202 halfword bits[13:6] (9-case step index [0..8]):
@ case 0: init (zero_duel_scene_display_buffers, fs_load puzzle deck, init_duel_puzzle_scene_state,
@          init_duel_field_vram_layout, set LP flags in gPrng);
@ case 1: tick_duel_field_fadeout_step;
@ case 2: tick_duel_field_main_frame (main duel frame);
@ case 3: tick_duel_field_fadein_step, write gPrng+0x23f flags;
@ case 4: render_puzzle_lp_digit_sprites, count_cleared_puzzle_stages, accrue_money_with_cap,
@         find_expert_challenge_slot_by_id, render_card_name_centered_to_sprite_vram,
@         dispatch_puzzle_display_mode;
@ case 5: tick_lp_display_and_blend_step;
@ case 6: dispatch_puzzle_display_mode (render card name text by encoding mode);
@ case 7: render_puzzle_lp_digit_sprites, update step field in gPrng+0x202;
@ case 8: tick_lp_display_and_fadein_check, accrue_money_with_cap, init_puzzle_wram_then_copy.
@ All cases share exit LAB_080202ec (movs r0,#0x80; lsls r0,#1 = 0x100) or
@ LAB_080202d4 (movs r0,#0). Step table: switchD_0801fee8__switchdataD_0801fef8.
@ Constants: gPrng=0x03000040; STEP_IDX_OFF=0x202; MAX_STEP=8; STEP_TABLE=0x0801fef8.
```

2. **tick_duel_puzzle_scene_step** @ asm line 5471:
   - 现有 plate 全 ASCII (英文). 无需修改.

3. 其余函数: 需逐行检查 asm 文件确认无 CJK.
   - append_game_text_if_raw (line 5164): ASCII plate. OK.
   - format_int_to_decimal_text (line 5184): ASCII plate. OK.
   - format_game_text_with_text_arg (line 5219): ASCII plate. OK.
   - format_game_text_with_int_arg (line 5282): ASCII plate. OK.
   - check_siocnt_link_ready (line 5334): ASCII plate. OK.
   - read_prng_entry_flag_clear (line 5356): ASCII plate. OK.
   - return_void_noop_stub (line 5376): ASCII plate. OK.
   - return_zero_leaf (line 5381): ASCII plate. OK.
   - return_noop_leaf (line 5387): ASCII plate. OK.
   - return_one_leaf (line 5393): ASCII plate. OK.
   - find_deck_record_index_by_key (line 5402): ASCII plate. OK.
   - find_card_index_in_rom_table (line 5431): ASCII plate. OK.
   - poll_fadein_exit_to_duel_state (line 5547): ASCII plate. OK.
   - render_lp_record_text_set_a (line 6144): ASCII plate. OK.

PLATE count = **1** (run_duel_puzzle_scene_state_machine CJK->ASCII).

---

## carve 计划 (R7)

无新 carve 计划。

- Block 1/2: 均在段内 ROM_INCBIN - disasm R4 处理, 不 carve (整块代码, 无嵌入数据表需单独 carve)
- Block 3/4: 同上
- 远端数据: find_card_index_in_rom_table 使用 0x098973f6/0x098972f0 为 ROM table, 但边界未知; 只 RENAME_SLOT 不 carve。

---

## disasm 计划 (R4)

全部 4 个 ROM_INCBIN 块必须 disasm:

### disasm A: Block 1 (0x1f4d0, 0x690)

- Range: 0x0801f4d0..0x0801fb60 THUMB
- Entry points (step functions): 0x0801f4d0 (case 0), 0x0801f5ec, 0x0801f60c, 0x0801f738, 0x0801f9c4, 0x0801f9e0, 0x0801fb20, 0x0801fb2c
- 注意: 0x1fb60 (.word 0x0801fb64) 和 PTR_DAT_0801fb64 (0x1fb64..0x1fb90) 是数据, 不在 ROM_INCBIN 中, 不需 disasm
- R4 disasm 流程: clearListing 0x0801f4d0..0x0801fb60, setTMode, 逐 stub DisassembleCommand

### disasm B: Block 2 (0x1fb90, 0x302)

- Range: 0x0801fb90..0x0801fe92 THUMB
- Entry points: 0x0801fb90, 0x0801fb94, 0x0801fb98, 0x0801fb9c, 0x0801fbb2, 0x0801fbbe, 0x0801fbe4, 0x0801fc18, 0x0801fd48, 0x0801fd80, 0x0801fe14, 0x0801fe54, 0x0801fe7c
- 注意: 0x0801fe92 是 named fn poll_fadein_exit_to_duel_state, block 2 在 0x0801fe92 前结束 (exclusive)

### disasm C: Block 3 (0x202fe, 0x36)

- Range: 0x080202fe..0x08020334 THUMB
- Entry points: 0x08020300 (main dispatcher, 2-byte pad at 0x202fe)
- Note: 0x202fe bytes 0x00 0x00 = alignment pad; function at 0x08020300
- Function name candidate: `tick_campaign_scene_step` (14-case state machine, gMenuState+0x234 fn-ptr, reads gPrng+0x202 bits[13:6])
- BLOCKED (confidence med): exact scene name TBD - callers from ROM[0xe2f40] suggest gMenuState context but exact scene identity requires tracing caller chain

### disasm D: Block 4 (0x20370, 0xa44)

- Range: 0x08020370..0x08020db4 THUMB
- Entry points (14 cases): 0x08020370, 0x08020524, 0x08020544, 0x08020670, 0x080209f4, 0x8020a10, 0x8020b50, 0x8020b6c, 0x8020b88, 0x8020ba4, 0x8020d00, 0x8020d34, 0x8020d94, 0x8020d4c
- 注意: block 4 ends at 0x08020db4 = render_lp_record_text_set_a start (exclusive)

disasm 执行注意:
- 重跑前先 clearListing 整 range 再 setTMode (避免 ContextChangeException)
- 跳转表目标块逐 stub per-4B DisassembleCommand (不整 range 一次性 disasm)

---

## 新增 constants / 全局

无新 constants 或全局变量。所有值均可复用现有 ewram.inc / gba_io.inc / gba_mem.inc / gl_blend.inc / name_input.inc / iwram.inc 中的常量。

新增 EQ 建议 (非强制, 可在实施时考虑):
- `DUEL_PUZZLE_CARD_SLOT_OFF = 0x213` (gDuelFieldState+0x213 puzzle card index field) - 仅本函数用, 不新建 global

---

## §5.1 登记 (Rule 3) - 0 引用块

无。本段全部 4 个 ROM_INCBIN 块均有实质引用 (86-110 refs), 不符合 §5.1 条件。

---

## 消费者证据 (R6) - 关键槽语义

| 槽 | 证据 file:line | 置信度 |
|---|---|---|
| DAT_0801fff8=0x02023130 | ewram.inc `.equ gDuelFieldState, 0x02023130`; asm/01 line 5728 | high |
| DAT_0801fff4=0x0000023f | ewram.inc `.equ GPRNG_BANNER_FLAG_OFF, 0x23f` | high |
| DAT_0801fffc=0xfffc03ff | constants/gl_blend.inc `.equ GL_CLEAR_BITS_17_10, 0xfffc03ff` | high |
| DAT_08020010=0xfffffc03 | constants/gl_blend.inc `.equ GL_CLEAR_BITS_9_2, 0xfffffc03` | high |
| DAT_08020138=0x02000000 | EWRAM_BASE; gba_mem.inc | high |
| DAT_08020148=0x6c2c | name_input.inc `.equ GSETTINGS_OFFSET, 0x6c2c`; confirmed from Seg-3 et al | high |
| DAT_0802013c=0x6c3c | ewram.inc `.equ gDuelPuzzleProgress, 0x02006C3C`; EWRAM_BASE+0x6c3c=0x02006c3c | high |
| DAT_080202cc=0x02023360 | ewram.inc `.equ gDuelSceneBase, 0x02023360`; 192 raw refs | high |
| DWORD_08020f50=0x02000000 | EWRAM_BASE | high |
| DWORD_08020f54=0x6c2c | GSETTINGS_OFFSET | high |
| DAT_0801f27c/f2f8/f358=0xfffe0000 | ewram.inc `.equ GAME_STR_RAW_ID_MASK, 0xfffe0000` | high |
| DWORD_0801f3ac=0x4000128 | gba_io.inc `.equ SIOCNT, 0x04000128` | high |
| Block 3 entry 0x08020300 = gMenuState fn-ptr | ROM[0xe2f40]=0x8020301 THUMB+1; context ROM[0xe2f3c]=0x02029590=gMenuState | high |
| Block 1/2 = step fns of tick_duel_puzzle_scene_step | PTR_DAT_0801f47c step table @ asm 5507-5528 | high |
| Block 4 = step fns of 0x08020300 dispatcher | PTR_DAT_08020338 step table @ asm 6126-6140 | high |

---

## 求助

1. **Block 3 function name (low confidence)**: Function at 0x08020300 is a gMenuState+0x234 step function (14-case dispatcher reading gPrng+0x202). The exact scene name is not determined statically. Candidate: `tick_campaign_scene_step` or `tick_lp_record_scene_step` (given block 4 contains lp_record display step fns). Tracing ROM[0xe2f40] caller context needed. Marking as BLOCKED pending disasm of block 3/4.

2. **DAT_08020018=0xffffc03f**: This mask clears bits[13:6] (8-bit step index field in gPrng+0x202). NAME_INPUT_PAGE_STATE_CLEAR=0xffc03fff is different (clears different bits). The 0xffffc03f mask is new; needs new constant name or stays raw. Proposed: `PRNG_STEP_IDX_CLEAR = 0xffffc03f` (new constant). Not adding to avoid proliferation unless reviewer approves.

