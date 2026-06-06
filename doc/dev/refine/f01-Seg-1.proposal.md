# Refine Proposal: f01-Seg-1  [0x0801cb00..0x0801d448)

## 段测绘

- 函数入口 x8 (全 <0x1d448, boundary: 0x1d448 = Seg-2 起点):

| addr | name | push prologue addr |
|------|------|--------------------|
| 0x0801cb00 | run_vija_scene_state_machine | 0x0801cb00 |
| 0x0801cf74 | tick_scene_step_by_step_table_b | 0x0801cf74 |
| 0x0801cfcc | tick_scene_step_by_step_table_c | 0x0801cfcc |
| 0x0801d0cc | write_tile_attr_byte_to_vram | 0x0801d0cc |
| 0x0801d15c | copy_palette_bank_by_slot | 0x0801d15c |
| 0x0801d174 | write_tile_attr_strip_4wide | 0x0801d174 |
| 0x0801d208 | apply_palette_and_tile_attr_strips | 0x0801d208 |
| 0x0801d290 | decode_card_image_6bpp | 0x0801d290 |

- 残留自动名槽 (严格 <0x1d448):

| slot addr | name | value |
|-----------|------|-------|
| 0x0801cb1c | DAT_0801cb1c | 0x02029eb0 |
| 0x0801cb20 | DAT_0801cb20 | 0x0801cb24 |
| 0x0801cbf4 | DAT_0801cbf4 | 0x09e3da08 |
| 0x0801cbf8 | DAT_0801cbf8 | 0x080000ae |
| 0x0801cbfc | DAT_0801cbfc | 0x02000000 |
| 0x0801cc00 | DAT_0801cc00 | 0x00006c2c |
| 0x0801cc04 | DAT_0801cc04 | 0xffffe0ff |
| 0x0801cd9c | DAT_0801cd9c | 0xffffe0ff |
| 0x0801ce00 | DAT_0801ce00 | 0x09e3da10 |
| 0x0801ce3c | DAT_0801ce3c | 0xffffe0ff |
| 0x0801cf08 | DAT_0801cf08 | 0xffffe0ff |
| 0x0801cfb8 | DWORD_0801cfb8 | 0x09e589b4 |
| 0x0801cfbc | DWORD_0801cfbc | gPrng (already labeled) |
| 0x0801cfc0 | DWORD_0801cfc0 | 0xffc03fff |
| 0x0801d010 | DWORD_0801d010 | 0x09e589b4 |
| 0x0801d014 | DWORD_0801d014 | gPrng (already labeled) |
| 0x0801d018 | DWORD_0801d018 | 0xffc03fff |
| 0x0801d158 | DWORD_0801d158 | 0x06004000 |
| 0x0801d424 | DAT_0801d424 | 0x080000ae |
| 0x0801d428 | DAT_0801d428 | 0x02000000 |
| 0x0801d42c | DAT_0801d42c | 0x00006c2c |
| 0x0801d438 | DAT_0801d438 | 0x06004000 |
| 0x0801d43c | DAT_0801d43c | 0x0000031f |
| 0x0801d440 | DAT_0801d440 | 0x00003f3f |
| 0x0801d444 | DAT_0801d444 | 0x00000c7f |

- PTR_DAT_0801d044: .word 0x0801d044 at 0x1d040 + 30-entry jump table (0x1d044..0x1d0bb, already structured .word in asm, no residual DAT name)

- ROM_INCBIN 0x1d024, 0x1c (28B): see data block section below.

- DAT_0801d0bc (.byte 16B at 0x1d0bc..0x1d0cb): 3 THUMB stubs, see data block section below.

Seg-2 boundary: 0x1d448 = card_info_page_enter_with_card_id (push {lr} at 0x0801d448).

---

## 数据块分类 (Rule 2/3)

### Block A: ROM_INCBIN 0x1d024, 0x1c (28B) at 0x0801d024

ref-scan (python `d.count(struct.pack('<I', v))`):

| probe value | count |
|-------------|-------|
| 0x0801d024 (raw) | 0 |
| 0x0801d025 (THUMB+1) | 0 |
| 0x0001d024 (raw offset) | 1 (at ROM 0x8bbe3d5, compressed asset region -- coincidental, not a code ref) |

THUMB opcode evidence (LE halfwords):
- +0x00: 0xb510 = `push {r4,lr}` -- THUMB function prologue
- +0x02: 0x1c1c = `adds r4,r3,#0` (save r3=slot)
- +0x04: 0x232c = `movs r3,#0x2c` (stride 44)
- +0x06: 0x4359 = `muls r1,r3`
- +0x08: 0x3120 = `adds r1,#0x20`
- +0x0a: 0x6011 = `str r1,[r2,#0]`
- +0x0c: 0x3801 = `subs r0,#1`
- +0x0e: 0x281d = `cmp r0,#0x1d` (30-entry dispatch)
- +0x10: 0xd846 = `bhi` -> branches to 0x0801d0c4 (OOB epilogue)
- +0x12: 0x0080 = `lsls r0,r0,#2` (index * 4)
- +0x14: 0x4901 = `ldr r1,[pc,#4]` -> loads 0x0801d044 from 0x1d040
- +0x16: 0x1840 = `adds r0,r0,r1`
- +0x18: 0x6800 = `ldr r0,[r0]` (load fn ptr from table)
- +0x1a: 0x4687 = `mov pc,r0` (jump to dispatch target)

Judgment: **disasm (R4)**. This is a THUMB tile-attr-op dispatcher: r0=op (1-based, subs r0,#1 -> 0-based), r1/r2/r3=params, dispatches 30 entries (indices 0..29). OOB (r0>29) falls to epilogue at 0x0801d0c4. No ROM pointer to entry address (0 refs) -- entered indirectly (struct field or runtime-computed pointer). The surrounding already-structured data (0x1d040 .word + 0x1d044..0x1d0bb jump table) is internally part of this function.

### Block B: DAT_0801d0bc (.byte 16B at 0x0801d0bc..0x0801d0cb)

ref-scan: dispatch table entries point to 0x0801d0bc, 0x0801d0c0, 0x0801d0c4 (raw, no +1). These addresses are used as `mov pc,r0` targets from the THUMB dispatcher above.

Content as THUMB halfwords:
- 0x0801d0bc: 0x2030 `movs r0,#0x30`; 0xe000 `b +4` -> falls to next
- 0x0801d0c0: 0x2050 `movs r0,#0x50`; 0x6020 `str r0,[r4,#0]`
- 0x0801d0c4: 0xbc10 `pop {r4}`; 0xbc01 `pop {r0}`; 0x4700 `bx r0` (epilogue)

Judgment: **disasm (R4)** -- internal stubs/epilogue of the unnamed dispatcher at 0x1d024. Three dispatch targets: [0x1d0bc] sets r0=0x30 then falls through to store; [0x1d0c0] sets r0=0x50 then stores r0 to [r4]; [0x1d0c4] is OOB epilogue (pop+return). These are internal code reachable from the jump table -- NOT standalone functions (no push prologue, no THUMB fn-ptr ref with +1).

### Data block summary

| Block | addr | size | ref-scan | judgment |
|-------|------|------|----------|----------|
| A | 0x0801d024 | 28B | raw=0, thumb+1=0 (entry 0-ref) | **§5.1 (driver 订正)**: orphan dispatcher cluster, 0 external entry ref |
| B | 0x0801d0bc | 16B | only internal jump-table raw-addr refs | **§5.1 (driver 订正)**: handlers of the orphan cluster |

**driver 订正 (Rule 3 + file 00 precedent)**: 块 A 入口 0x1d024 raw+thumb 全 0 引用, 且前一函数
0x1d022 `bx r1` 返回 (非 fall-through 可达) → **orphan dead-code dispatcher 簇** (入口 + 内部
jump table 0x1d044 + handlers 0x1d0bc/0c0/0c4, 簇内互引但 0 外部入口引用)。与 file 00 Seg-4
(0x1604c jump-table dispatcher) / Seg-5b (0x169d6 orphan objd dispatcher) **完全同模式** → 按
**Rule 3 §5.1 登记** (留 ROM_INCBIN/.byte 原样, 不 disasm 不 createFunction), 引用到时再 R4。
executor 原判 disasm R4 与 Rule 3 + file 00 precedent 冲突, 改 §5.1。**BLOCKED-f01S1-1 随之消解**
(§5.1 无需命名)。

---

## 符号化计划

All EQ values verified against ROM (python `struct.unpack_from('<I', d, slot_offset)[0]` == expected). All correct.

### EQ_SLOTS

| slot | value | const_name | source | slot_label |
|------|-------|------------|--------|------------|
| DAT_0801cb1c | 0x02029eb0 | gVijaState | 复用 ewram.inc | run_vija_scene_state_machine_gvija_state |
| DAT_0801cbf8 | 0x080000ae | ROM_REGION_CODE_ADDR | 复用 rom_region.inc | run_vija_scene_state_machine_rom_region_code_addr |
| DAT_0801cbfc | 0x02000000 | EWRAM_BASE | 复用 gba_mem.inc | run_vija_scene_state_machine_ewram_base |
| DAT_0801cc00 | 0x00006c2c | GSETTINGS_OFFSET | 复用 name_input.inc | run_vija_scene_state_machine_gsettings_offset |
| DAT_0801cc04 | 0xffffe0ff | DEMO_CLEAR_BITS_12_8 | 复用 demo_state.inc | run_vija_scene_state_machine_dispcnt_obj_en_mask_a |
| DAT_0801cd9c | 0xffffe0ff | DEMO_CLEAR_BITS_12_8 | 复用 demo_state.inc | run_vija_scene_state_machine_dispcnt_obj_en_mask_b |
| DAT_0801ce3c | 0xffffe0ff | DEMO_CLEAR_BITS_12_8 | 复用 demo_state.inc | run_vija_scene_state_machine_dispcnt_obj_en_mask_c |
| DAT_0801cf08 | 0xffffe0ff | DEMO_CLEAR_BITS_12_8 | 复用 demo_state.inc | run_vija_scene_state_machine_dispcnt_obj_en_mask_d |
| DWORD_0801cfc0 | 0xffc03fff | NAME_INPUT_PAGE_STATE_CLEAR | 复用 name_input.inc:28 | tick_scene_step_by_step_table_b_step_advance_mask |
| DWORD_0801d018 | 0xffc03fff | NAME_INPUT_PAGE_STATE_CLEAR | 复用 name_input.inc:28 | tick_scene_step_by_step_table_c_step_advance_mask |
| DWORD_0801d158 | 0x06004000 | BG_CHAR_VRAM_CB2 | 新建 gba_mem.inc | write_tile_attr_byte_to_vram_vram_char_base |
| DAT_0801d424 | 0x080000ae | ROM_REGION_CODE_ADDR | 复用 rom_region.inc | decode_card_image_6bpp_rom_region_code_addr |
| DAT_0801d428 | 0x02000000 | EWRAM_BASE | 复用 gba_mem.inc | decode_card_image_6bpp_ewram_base |
| DAT_0801d42c | 0x00006c2c | GSETTINGS_OFFSET | 复用 name_input.inc | decode_card_image_6bpp_gsettings_offset |
| DAT_0801d438 | 0x06004000 | BG_CHAR_VRAM_CB2 | 复用同新建 | decode_card_image_6bpp_vram_char_base |

Evidence sources:
- gVijaState: ewram.inc line 179. Confirmed: run_vija_scene_state_machine ldr r5, DAT_0801cb1c then adds r0,r5,#0; adds r0,#0x8d -> gVijaState+0x8d = phase byte. Confidence: high.
- ROM_REGION_CODE_ADDR: rom_region.inc line 10. Confirmed: DAT_0801cbf8 used as `ldrh r0,[r0,#0]; lsrs r0,r0,#8; cmp r0,#0x4a` (region check). Confidence: high.
- EWRAM_BASE: gba_mem.inc line 7. Value 0x02000000 used as base for gSettings offset. Confidence: high.
- GSETTINGS_OFFSET: name_input.inc line 18. Pattern `ldr r1,DAT_..fcfc; ldr r0,DAT_..cc00; adds r1,r1,r0` -> EWRAM_BASE + GSETTINGS_OFFSET = gSettings. Confidence: high.
- DEMO_CLEAR_BITS_12_8: demo_state.inc line 16. Value 0xffffe0ff = ~0x00001f00 = clear DISPCNT bits[12:8] (BG/OBJ enable). Same mask used at 4 sites in run_vija_scene_state_machine for `ands r0,r1; orrs r0,r3; strh r0,[r2,#0]` on DISPCNT (0x04000000). Confidence: high.
- STEP_ADVANCE_MASK 0xffc03fff: comment in plate explicitly states this value. Used as `ands r0,r2 (field word); orrs r0,r1 (new idx shifted); str r0,[r4]` to update gPrng+0x204 step-index bitfield (bits[21:14]). 0xffc03fff = ~(0xff<<14) = clear bits [21:14]. Confidence: high.
- BG_CHAR_VRAM_CB2 0x06004000: GBA VRAM charblock 2 base (= GBA_VRAM_BASE + 0x4000). Confirmed: write_tile_attr_byte_to_vram plate states "VRAM_CHAR_BASE = 0x06004000 (BG char data VRAM base)". 43 ROM refs (shared constant). Not yet in gba_mem.inc. Confidence: high.

### REF_SLOTS

| slot | target | gas_label | slot_label |
|------|--------|-----------|------------|
| DAT_0801cb20 | 0x0801cb24 | switchD_0801cb1a__switchdataD_0801cb24 | run_vija_scene_state_machine_switch_table_base |
| DAT_0801cbf4 | 0x09e3da08 | vija_bg_fs_path_pair | run_vija_scene_state_machine_vija_bg_path_pair |
| DAT_0801ce00 | 0x09e3da10 | vija_obj_slot_seq | run_vija_scene_state_machine_vija_obj_slot_seq |

Evidence:
- DAT_0801cb20 = 0x0801cb24: switchdataD label exists at asm line 26 (switchD_0801cb1a__switchdataD_0801cb24). This is the jump table base loaded for the 10-case dispatch. Confidence: high.
- DAT_0801cbf4 = 0x09e3da08: code reads [+0] (JP path ptr) and [+4] (US path ptr) from struct at this address, stores on stack, then calls fs_load with selected path. Content: {ptr->'demo/vija/BG1_all.LZ5bg', ptr->'demo/vija/BG1_all_US.LZ5bg'}. 1 ROM ref. Must be carved into rom.s. Confidence: high.
- DAT_0801ce00 = 0x09e3da10: caseD_5 code: `ldr r1, DAT_0801ce00; add r0,sp,#8; movs r2,#5; bl memcpy` -> copies 5 bytes from 0x09e3da10 to stack. Content: {0x01, 0x03, 0x00, 0x02, 0x04} = OBJ slot selection sequence indexed by (tick_counter/10). 1 ROM ref. Adjacent to vija_bg_fs_path_pair (at offset +8). Must be carved. Confidence: high (memcpy r2=#5 is explicit size).

### RENAME_SLOTS

| slot | slot_label | eol_note |
|------|------------|---------|
| DWORD_0801cfb8 | tick_scene_step_by_step_table_b_step_table | ROM step table B base (0x09e589b4); 3 entries [0]=0x0801c2ad [1]=0x0801c50d [2]=0x0801cb01+1 |
| DWORD_0801d010 | tick_scene_step_by_step_table_c_step_table | same ROM step table B (0x09e589b4) shared with table_b |
| DAT_0801d43c | decode_card_image_6bpp_tile_x_low_mask | 0x31f tile index low-9-bit mask for BG char addr compute |
| DAT_0801d440 | decode_card_image_6bpp_tile_xy_6bit_mask | 0x3f3f dual-6-bit mask for tile grid x/y coords |
| DAT_0801d444 | decode_card_image_6bpp_attr_packed_mask | 0xc7f packed tile attribute field mask |

Evidence:
- DWORD_0801cfb8 = 0x09e589b4: plate comment states "STEP_TABLE_BASE_B = 0x09e589b4". Verified: ROM at offset 0x1e589b4 has 3 THUMB fn-ptrs (0x0801c2ad, 0x0801c50d, 0x0801cb01) then NULL. tick_scene_step_by_step_table_b reads this, multiplies step index by 4, and calls the fn. Confidence: high.
- DWORD_0801d010: same value 0x09e589b4 in tick_scene_step_by_step_table_c. Identical plate note states shared table. Confidence: high.
- DAT_0801d43c = 0x0000031f: used in decode_card_image_6bpp inner loop (0x1d3ee: `ldr r3, DAT_0801d440; ldr r2,[sp,#0]`). The 0x31f mask operates on tile coordinate computation alongside 0x3f3f and 0xc7f masks. Together these perform bit-field extraction for BG tile attribute encoding. 17 ROM refs (common bit mask). Local slot names per function. Confidence: med (exact bit semantics require deeper decode analysis; the masking role is clear from context).
- DAT_0801d440 = 0x00003f3f: 85 ROM refs. Used for dual 6-bit field select. Confidence: med.
- DAT_0801d444 = 0x00000c7f: 4 ROM refs. Confidence: med.

### FUNC_RENAME

None identified. All 8 function names match observed behavior:
- run_vija_scene_state_machine: body reads gVijaState+0x8d phase byte, dispatches 10 cases (phase 0..9). Name matches. Confidence: high.
- tick_scene_step_by_step_table_b/c: bodies read step table B (0x09e589b4), call via invoke_r0, advance step index. Names match. Confidence: high.
- write_tile_attr_byte_to_vram / copy_palette_bank_by_slot / write_tile_attr_strip_4wide / apply_palette_and_tile_attr_strips / decode_card_image_6bpp: names match observed operations. Confidence: high.

### PLATE (R5)

One CJK plate line found in Seg-1 scope:

- **decode_card_image_6bpp** (asm line 963): `@ p1: 6bpp -> BG0 VRAM, 每6 ROM bytes -> 8 像素`
  - Contains CJK: 每 (U+6BCF), 像素 (U+50CF U+7D20)
  - ASCII replacement: `@ p1: 6bpp source -> BG char VRAM tile layout. 6 input bytes -> 8 output pixels (3 src halfwords -> 4 dst halfwords).`
  - Evidence: function operates on 6bpp card image data (plate line 963 + structure: ldrh r2,[r6]; ldrh r3,[r6,#2]; ldrh r4,[r6,#4] = 6 bytes src; strh..strh..strh..strh = 4 halfwords dst). Confidence: high.
  - Action: rewrite asm line 963 in-place (before or after Ghidra export).

Other 7 function plates: checked -- all ASCII (no CJK). Confirmed by grep `[^\x00-\x7F]` on lines 1..1192 of 01_vija_scene_text.s: only lines 2 (file header), 963, 1193 (Seg-2) have non-ASCII. Lines 2 and 1193 are outside scope.

- **write_tile_attr_byte_to_vram** (asm line 708): `FUN_0801d174` -> `write_tile_attr_strip_4wide`
  Full: `@ Called by write_tile_attr_strip_4wide in inner loop for each of 4 sub-elements ...`
  Evidence: FUN_0801d174 = write_tile_attr_strip_4wide (asm line 812, push @ 0x0801d174, Seg-1 named fn). C8 fix.

- **copy_palette_bank_by_slot** (asm line 787): `FUN_0801d208` -> `apply_palette_and_tile_attr_strips`
  Full: `@ Called by apply_palette_and_tile_attr_strips (tile map update function). ...`
  Evidence: FUN_0801d208 = apply_palette_and_tile_attr_strips (asm line 898, push @ 0x0801d208, Seg-1 named fn). C8 fix.

---

## carve 计划 (R7)

### carve-1: vija BG/OBJ resource data

Host incbin (rom.s line 1142):
```
.incbin "roms/2343.gba", 0x1E3D9CF, 0xC33D
```

Replace with (coverage equation: 5 + 24 + 28 + 8 + 8 + 0xC2F4 = 0xC33D = verified):

```asm
    .incbin "roms/2343.gba", 0x1E3D9CF, 0x5        @ 5B pad (NUL+data after assert string)
vija_bg_jp_path:                                    @ 0x09e3d9d4
    .asciz "demo/vija/BG1_all.LZ5bg"               @ 24B (incl NUL, already 4-byte aligned)
vija_bg_us_path:                                    @ 0x09e3d9ec
    .asciz "demo/vija/BG1_all_US.LZ5bg"            @ 27B + 1B NUL pad = 28B
    .byte 0x0                                       @ alignment pad
vija_bg_fs_path_pair:                               @ 0x09e3da08 (DAT_0801cbf4 target)
    .word vija_bg_jp_path                           @ [0] JP FS path ptr
    .word vija_bg_us_path                           @ [4] US FS path ptr
vija_obj_slot_seq:                                  @ 0x09e3da10 (DAT_0801ce00 target)
    .byte 0x01, 0x03, 0x00, 0x02, 0x04             @ OBJ slot index sequence [phase 0..4]
    .byte 0x0, 0x0, 0x0                             @ 3B pad
    .incbin "roms/2343.gba", 0x1E3DA18, 0xC2F4     @ remainder
```

Byte-identical verification:
- `vija_bg_jp_path` resolves to GBA addr via linker. The `.word vija_bg_jp_path` at vija_bg_fs_path_pair[0] must equal 0x09e3d9d4. Confirmed: string starts at ROM 0x1e3d9d4, GBA 0x09e3d9d4.
- `vija_bg_us_path` must equal 0x09e3d9ec. Confirmed: previous string 24B + 0x09e3d9d4 = 0x09e3d9ec.
- 5-byte pre-pad content: ROM bytes at 0x1e3d9cf = `0x00 0x01 0x02 0x01 0x00` -- these are raw binary (NOT pure NUL). The `.incbin` sub-slice preserves them exactly.
- vija_obj_slot_seq bytes: ROM at 0x1e3da10 = `01 03 00 02 04` + `00 00 00`. Verified.

Code-side changes:
- DAT_0801cbf4 -> `run_vija_scene_state_machine_vija_bg_path_pair: .word vija_bg_fs_path_pair`
- DAT_0801ce00 -> `run_vija_scene_state_machine_vija_obj_slot_seq: .word vija_obj_slot_seq`

---

## disasm 计划 (R4)

### disasm-1: unnamed THUMB tile-attr dispatcher at 0x0801d024

Range: 0x0801d024..0x0801d0cb (includes ROM_INCBIN 28B + adjacent .word + jump table + stubs)

Current asm structure:
- ROM_INCBIN 0x1d024, 0x1c (28B) -- THUMB fn prefix
- .word 0x0801d044 @ 0x1d040 -- ldr pc literal target
- PTR_DAT_0801d044: 30 .word entries @ 0x1d044..0x1d0bb
- DAT_0801d0bc: .byte 16B @ 0x1d0bc..0x1d0cb -- 3 THUMB stubs

Disasm plan: Ghidra must disassemble 0x0801d024 as THUMB. The bhi at +0x10 targets 0x0801d0c4 (OOB epilogue). Jump table entries at 0x1d044..0x1d0bb are RAW addresses (no +1); they're written to pc via `mov pc,r0` so the target code is entered in ARM mode OR the targets are THUMB code entered via mode switch -- in either case Ghidra must disassemble the stub targets.

Function naming: 0 ROM pointer refs (no THUMB fn-ptr found). Name TBD -- propose `dispatch_tile_attr_op_by_index` (tile-attr op dispatch by op index 1..30; r0=op, r1/r2/r3=tile params, r4=slot saved). Low confidence on semantics without caller analysis. Caller is not statically visible -> mark BLOCKED for naming, propose leaving as unnamed until Seg-2+ analysis reveals caller.

Disasm stub details:
- `dispatch_tile_attr_op_case_r0_0x30`: at 0x1d0bc: `movs r0,#0x30; b 0x1d0c0`
- `dispatch_tile_attr_op_case_r0_0x50`: at 0x1d0c0: `movs r0,#0x50; str r0,[r4,#0]`
- `dispatch_tile_attr_op_epilogue`: at 0x1d0c4: `pop {r4}; pop {r0}; bx r0` (OOB epilogue + normal return)

Note: The `.word 0x0801d044 @ 0x1d040` at ROM offset 0x1d040 is NOT a code instruction -- it is the literal pool value loaded by `ldr r1,[pc,#4]` at 0x1d038 inside the THUMB fn. Ghidra should mark it as a data word within the function body.

### disasm-2: DAT_0801d0bc stubs (covered under disasm-1 above)

Already described. These 16 bytes at 0x1d0bc..0x1d0cb are the 3 dispatch stubs + OOB epilogue. Part of the same disasm range.

---

## 新增 constants / 全局

### BG_CHAR_VRAM_CB2 = 0x06004000

- Location: gba_mem.inc (add after GBA_VRAM_BASE = 0x06000000 line 12).
- Evidence: used in write_tile_attr_byte_to_vram (DWORD_0801d158) and decode_card_image_6bpp (DAT_0801d438). Plate of write_tile_attr_byte_to_vram (asm line 711): "VRAM_CHAR_BASE = 0x06004000 (BG char data VRAM base)". Value = GBA_VRAM_BASE + 0x4000 (charblock 2). 43 ROM refs. Confidence: high.
- Existing scan: grep of constants/*.inc for 0x06004000 -> no match. New equate confirmed needed.

---

## §5.1 登記 (Rule 3) -- 0 引用块

| 地址 | 大小 | 所在 Seg | 初判内容 | 状态 |
|---|---|---|---|---|
| 0x0801d024 (+ jump table 0x1d044 + handlers 0x1d0bc) | 28B (ROM_INCBIN 0x1d024,0x1c) + 16B (.byte 0x1d0bc) | f01 Seg-1 | **orphan THUMB tile-attr dispatcher 簇**: 入口 0x1d024 (push{r4,lr} + subs r0,#1 + bhi OOB + 30-entry jump-table dispatch via mov pc,r0) + jump table 0x1d044 (30×4B raw-addr, 已 .word 结构化) + handlers 0x1d0bc(r0=0x30)/0x1d0c0(r0=0x50, str)/0x1d0c4(OOB epilogue)。**入口 0 外部引用** (raw+thumb 全 0; 前函数 0x1d022 bx r1 返回, 非 fall-through), 簇内互引。与 file 00 Seg-4 0x1604c / Seg-5b 0x169d6 orphan dispatcher 同模式。**留待**: 引用到时 R4 disasm + createFunction (caller 暴露后命名)。byte-identical: 保持 ROM_INCBIN/.byte 原样 |

注: 该簇是本段唯一数据块, 判 §5.1 (Rule 3)。本段无 carve 以外的 disasm。

---

## 消費者証據 (R6)

| 槽/全局 | consumer | file:line | confidence |
|---------|----------|-----------|------------|
| gVijaState | run_vija_scene_state_machine: `adds r0,r5,#0; adds r0,#0x8d; ldrb r0,[r0]` reads phase byte | asm/01_vija_scene_text.s:8,9,11 | high |
| ROM_REGION_CODE_ADDR | run_vija_scene_state_machine caseD_0: `ldrh r0,[r0,#0]; lsrs r0,r0,#8; cmp r0,#0x4a` region check | asm/01_vija_scene_text.s:53-55 | high |
| GSETTINGS_OFFSET | caseD_0: `ldr r1,DAT_cbfc (EWRAM_BASE); ldr r0,DAT_cc00 (GSETTINGS_OFFSET); adds r1,r1,r0` -> gSettings | asm/01_vija_scene_text.s:57-59 | high |
| DEMO_CLEAR_BITS_12_8 | caseD_0: `ands r0,r1; orrs r0,r3; strh r0,[r2,#0]` on DISPCNT at 0x04000000 | asm/01_vija_scene_text.s:106-108 | high |
| vija_bg_fs_path_pair | caseD_0: `ldr r0,[struct]; ldr r1,[struct+4]` -> jp/us path ptrs passed for fs_load | asm/01_vija_scene_text.s:47-50 | high |
| vija_obj_slot_seq | caseD_5: `bl memcpy(sp+8, 0x09e3da10, 5)` -> 5-byte slot seq copied to stack | asm/01_vija_scene_text.s:337-340 | high |
| gPrng (DWORD_cfbc/d014) | tick_scene_step_by_step_table_b/c: `ldr r0, gPrng; movs r2,#0x81; lsls r2,r2,#2; adds r4,r0,r2; ldr r0,[r4]` | asm/01_vija_scene_text.s:609,629 | high |
| BG_CHAR_VRAM_CB2 | write_tile_attr_byte_to_vram: `ldr r3, DWORD_0801d158; adds r5,r5,r3` -> VRAM base for tile write | asm/01_vija_scene_text.s:739-740 | high |

---

## 求助 (BLOCKED) — RESOLVED by driver

### BLOCKED-f01S1-1: RESOLVED → §5.1 (无需命名)
driver 裁定: 0x1d024 dispatcher 簇入口 0 外部引用 → orphan dead-code → **§5.1 登记** (Rule 3 +
file 00 Seg-4/5b precedent), 不 disasm 不命名。caller 未知正是 0-ref 的体现, 引用到时再 R4+命名。
以下原 BLOCKED 分析保留作背景参考:

### (原) BLOCKED-f01S1-1: dispatch_tile_attr_op_by_index caller unknown

- Function at 0x0801d024 (THUMB tile-attr dispatcher): 0 ROM pointer refs (no THUMB fn-ptr 0x0801d025 found).
- Cannot identify caller statically. Cannot confirm semantic name.
- Action: disasm R4 proceeds (THUMB code clear); leave function unnamed (FUN_ or temp name) until Seg-2+ analysis exposes caller context, then revisit naming.
- Confidence on disasm-R4: high. Confidence on naming: blocked.

---

## Executor Report: f01-Seg-1

- 函数: 8 fn, 全 <0x1d448 (boundary confirmed: card_info_page_enter_with_card_id at 0x0801d448)
- 槽: EQ=15 REF=3 RENAME=5 FUNC_RENAME=0 PLATE=3 (decode_card_image_6bpp CJK->ASCII + 2x FUN_->现名 C8)
- carve=1 (vija_bg_fs_path_pair + vija_obj_slot_seq, host incbin rom.s line 1142)
- disasm=0 (orphan dispatcher 簇 §5.1, 不 disasm)
- §5.1=1 cluster (0x1d024 orphan dispatcher + jump table 0x1d044 + handlers 0x1d0bc)
- 新增 constants: BG_CHAR_VRAM_CB2=0x06004000 (gba_mem.inc); NAME_INPUT_PAGE_STATE_CLEAR 复用 name_input.inc:28
- 新增 carve labels: vija_bg_jp_path, vija_bg_us_path, vija_bg_fs_path_pair, vija_obj_slot_seq (all in rom.s host incbin 0x1E3D9CF)
- 求助: BLOCKED-f01S1-1 (dispatch_tile_attr_op_by_index at 0x0801d024 -- 0 caller refs, naming deferred)
- 越界检查: 无. 所有槽地址 <0x1d448. DAT_0801d458 (line 1202, addr 0x1d458 >= 0x1d448) 不在 Seg-1 范围内, 未纳入.
- proposal: doc/dev/refine/f01-Seg-1.proposal.md
