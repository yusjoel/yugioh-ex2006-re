# Refine Proposal: Seg-10  [0x0801b850..0x0801cb00)

## 段测绘

- 函数入口: 32 个 (全部 < 0x0801cb00, 严守上界)

| addr       | name                          |
|------------|-------------------------------|
| 0x0801b850 | load_demo_shuen_sprite_gfx    |
| 0x0801b91c | load_shuen_sprite_gfx_guarded |
| 0x0801b93c | load_shuen_bg1_gfx_set        |
| 0x0801ba04 | load_shuen_obj_resource_by_slot |
| 0x0801ba4c | load_shuen_obj_resource_slot0 |
| 0x0801ba5c | write_shuen_bg3_scroll_regs   |
| 0x0801ba78 | tick_demo_shuen_bg3_hscroll   |
| 0x0801bad0 | tick_shuen_bg3_vscroll_phase  |
| 0x0801bb28 | advance_shuen_cell_anim_frame |
| 0x0801bbd4 | tick_shuen_anim_slots_batch   |
| 0x0801bc28 | apply_win0v_fadein_step       |
| 0x0801bcb8 | apply_win0v_fadeout_step      |
| 0x0801bd08 | demo_shuen_state_machine      |
| 0x0801c254 | tick_scene_step_by_step_table_a |
| 0x0801c2ac | reset_gl_display_state        |
| 0x0801c310 | load_vija_bg_gfx_embedded     |
| 0x0801c3f4 | load_vija_bg_gfx_from_fs      |
| 0x0801c484 | load_vija_bg_gfx_by_mode      |
| 0x0801c4c0 | load_vija_obj_resource_by_region |
| 0x0801c50c | load_vija_obj_resource_gated  |
| 0x0801c544 | apply_bg3_scroll_masked       |
| 0x0801c560 | tick_vija_bg3_scroll_forward  |
| 0x0801c59c | tick_vija_bg3_scroll_backward |
| 0x0801c5d8 | drive_vija_obj_cell_anim      |
| 0x0801c668 | apply_bg2_affine_fixed_angle  |
| 0x0801c694 | tick_bg2_affine_anim_frame    |
| 0x0801c6b0 | tick_bg_scroll_anim_frame     |
| 0x0801c710 | get_vija_obj_slot_field8      |
| 0x0801c728 | advance_scene_phase_counter   |
| 0x0801c74c | update_dual_cell_anim_oam_pos |
| 0x0801c794 | tick_vija_obj_anim_slot       |
| 0x0801cadc | tick_all_vija_obj_anim_slots  |

- 残留自动名槽: 65 个 DAT_/DWORD_/PTR_ 定义 (含 7 个 PTR_ 已正确符号化值; 纯改名目标)
- ROM_INCBIN / .byte 块: 0 (driver 扫描确认, awk 过 Seg-10 行范围无匹配)

file boundary: 0x0801cb00 = file 01 起点 (run_vija_scene_state_machine 首字节), 不纳入

---

## 数据块分类 (Rule 2/3)

无段内 ROM_INCBIN / .byte 块, 跳过此节。

---

## 符号化计划 (R1/R2/R3)

### 新增全局 gVijaState (0x02029eb0)

**消费者证据 (R6)**:
- asm/00_system_str_vija.s line 19382: `reset_gl_display_state` plate -- "bios_cpu_set fill-zero EWRAM 0x02029eb0 192 bytes"; code: `ldr r1, DAT_0801c2f8` = 0x02029eb0, bios_cpu_set ctrl 0x05000030 (= count=0x30 words * 4 = 0xc0 = 192 bytes). confidence=high
- asm/00_system_str_vija.s line 19708-19713: plate "VIJA_STATE=0x02029eb0; SCROLL_PHASE_OFF=0x8c" -- vija scroll tick; confidence=high
- asm/00_system_str_vija.s line 20367: plate "SLOT_BASE_OFFSET=0x98, SLOT_COUNT=5" -- vija OBJ anim slots at base+0x98; confidence=high
- asm/01_vija_scene_text.s line 4: plate "per-frame state machine driver. all state from IWRAM 0x02029eb0. VIJA_STATE=0x02029eb0"; run_vija_scene_state_machine plate; confidence=high

**命名**: `gVijaState` = 0x02029eb0
- 理由: vija scene (play_ui_effect_3b) per-frame state struct; 61 ROM refs (ref-scan: raw count=61, THUMB count=0); 结构大小 0xc0 bytes (reset_gl_display_state bios_cpu_set). 与 gDemoState (0x02029ec0) 相邻但独立 -- gDemoState 服务 shuen, gVijaState 服务 vija/play_ui_effect_3b (两场景共享同一 EWRAM 块地址)
- 新增到 `constants/ewram.inc`

**验证**: 0x02029eb0 raw ROM count=61 (python struct.pack('<I',0x02029eb0).count); 0x02029eb1 THUMB count=0; confidence=high.

---

### EQ_SLOTS (data-equate)

复用现有常量 (`constants/demo_state.inc`, `constants/gba_mem.inc`, `constants/rom_region.inc`, `constants/name_input.inc`, `constants/iwram.inc`):

| 槽 (addr) | value | const_name | slot_label |
|-----------|-------|------------|------------|
| 0x0801b918 | 0xffffc07f | DEMO_CLEAR_BITS_13_7 | load_demo_shuen_sprite_gfx_oam_palette_mask |
| 0x0801ba00 | 0xffffc07f | DEMO_CLEAR_BITS_13_7 | load_shuen_bg1_gfx_set_oam_palette_mask |
| 0x0801ba6c | 0x000001ff | DEMO_KEEP_BITS_8_0 | write_shuen_bg3_scroll_regs_scroll_mask |
| 0x0801bacc | 0xfffffe01 | DEMO_CLEAR_BITS_8_1 | tick_demo_shuen_bg3_hscroll_counter_clear_mask |
| 0x0801bb24 | 0xfffffe01 | DEMO_CLEAR_BITS_8_1 | tick_shuen_bg3_vscroll_phase_counter_clear_mask |
| 0x0801bcb0 | 0xffff9fff | DEMO_CLEAR_BITS_14_13 | apply_win0v_fadein_step_dispcnt_clear_mask |
| 0x0801bdd4 | 0xffffe0ff | DEMO_CLEAR_BITS_12_8 | demo_shuen_state_machine_dispcnt_clear_mask |
| 0x0801bdd8 | 0xfffe01ff | DEMO_CLEAR_BITS_16_9 | demo_shuen_state_machine_state_clear_mask_a |
| 0x0801be28 | 0xfffffe01 | DEMO_CLEAR_BITS_8_1 | demo_shuen_state_machine_substate_clear_mask_a |
| 0x0801be2c | 0xfffe01ff | DEMO_CLEAR_BITS_16_9 | demo_shuen_state_machine_state_clear_mask_b |
| 0x0801bf94 | 0xfffffe01 | DEMO_CLEAR_BITS_8_1 | demo_shuen_state_machine_substate_clear_mask_b |
| 0x0801bf98 | 0xfffe01ff | DEMO_CLEAR_BITS_16_9 | demo_shuen_state_machine_state_clear_mask_c |
| 0x0801bfd0 | 0xfffffe01 | DEMO_CLEAR_BITS_8_1 | demo_shuen_state_machine_substate_clear_mask_c |
| 0x0801bfd4 | 0xfffe01ff | DEMO_CLEAR_BITS_16_9 | demo_shuen_state_machine_state_clear_mask_d |
| 0x0801c0bc | 0xffffe0ff | DEMO_CLEAR_BITS_12_8 | demo_shuen_state_machine_dispcnt_clear_mask_b |
| 0x0801c0c0 | 0xfffffe01 | DEMO_CLEAR_BITS_8_1 | demo_shuen_state_machine_substate_clear_mask_d |
| 0x0801c0c4 | 0xfffe01ff | DEMO_CLEAR_BITS_16_9 | demo_shuen_state_machine_state_clear_mask_e |
| 0x0801c160 | 0xfffffe01 | DEMO_CLEAR_BITS_8_1 | demo_shuen_state_machine_substate_clear_mask_e |
| 0x0801c1c0 | 0xffffe0ff | DEMO_CLEAR_BITS_12_8 | demo_shuen_state_machine_dispcnt_clear_mask_c |
| 0x0801c204 | 0xfffffe01 | DEMO_CLEAR_BITS_8_1 | demo_shuen_state_machine_substate_clear_mask_f |
| 0x0801c3f0 | 0xffffc07f | DEMO_CLEAR_BITS_13_7 | load_vija_bg_gfx_embedded_oam_palette_mask |
| 0x0801c47c | 0xffffc07f | DEMO_CLEAR_BITS_13_7 | load_vija_bg_gfx_from_fs_oam_palette_mask |
| 0x0801c538 | 0x080000ae | ROM_REGION_CODE_ADDR | load_vija_obj_resource_by_region_rom_region_addr |
| 0x0801c53c | 0x02000000 | EWRAM_BASE | load_vija_obj_resource_by_region_ewram_base |
| 0x0801c540 | 0x00006c2c | GSETTINGS_OFFSET | load_vija_obj_resource_by_region_gsettings_off |
| 0x0801c554 | 0x000001ff | DEMO_KEEP_BITS_8_0 | apply_bg3_scroll_masked_scroll_mask |

Note: ROM_REGION_CODE_ADDR from `constants/rom_region.inc` (confirmed line 2 of rom_region.inc); EWRAM_BASE from `constants/gba_mem.inc`; GSETTINGS_OFFSET from `constants/name_input.inc`.

新建常量 (先确认 constants/ 无可复用):

| 槽 (addr) | value | new const_name | inc 文件 | slot_label |
|-----------|-------|----------------|---------|------------|
| 0x0801c2a0 | 0xffc03fff | SCENE_STEP_IDX_CLEAR_MASK | demo_state.inc | tick_scene_step_by_step_table_a_step_idx_clear_mask |
| 0x0801c2fc | 0x05000030 | VIJA_CPUSET_FILL_CTRL | demo_state.inc | reset_gl_display_state_cpuset_ctrl |
| 0x0801c300 | 0x00001741 | VIJA_DISPCNT_INIT | demo_state.inc | reset_gl_display_state_dispcnt_init |
| 0x0801c304 | 0x00001d81 | VIJA_BG0CNT_INIT | demo_state.inc | reset_gl_display_state_bg0cnt_init |
| 0x0801c308 | 0x00001e82 | VIJA_BG1CNT_INIT | demo_state.inc | reset_gl_display_state_bg1cnt_init |
| 0x0801c30c | 0x00001f8b | VIJA_BG2CNT_INIT | demo_state.inc | reset_gl_display_state_bg2cnt_init |
| 0x0801c480 | 0xfffe3fff | DEMO_CLEAR_BITS_16_14 | demo_state.inc | load_vija_bg_gfx_from_fs_tile_shape_clear_mask |

说明:
- SCENE_STEP_IDX_CLEAR_MASK=0xffc03fff: ~0x003fc000 = clears bits[21:14] (8-bit step index field in gPrng+0x204 packed word); used by tick_scene_step_by_step_table_a. Confirmed by `tick_scene_step_by_step_table_a` plate: "STEP_ADVANCE_MASK = 0xffc03fff (step field clear mask)" (asm/00_system_str_vija.s line 19298).
- VIJA_CPUSET_FILL_CTRL=0x05000030: bios_cpu_set fill-mode control word; count=0x30 (48 words = 192 bytes), bit24=fill, bit26=32bit; clears gVijaState region 0x02029eb0..+0xc0; confidence=high (asm/00_system_str_vija.s line 19382 plate).
- VIJA_DISPCNT_INIT/BGxCNT_INIT: four display register init values written to DISPCNT/BG0-2CNT at scene reset; confirmed by asm/00_system_str_vija.s lines 19386-19392 `.word` values cross-checked via ROM bytes (ROM off 0x1c300=0x1741, 0x1c304=0x1d81, 0x1c308=0x1e82, 0x1c30c=0x1f8b).
- DEMO_CLEAR_BITS_16_14=0xfffe3fff: ~0x0001c000 = clears bits[16:14]; used in load_vija_bg_gfx_from_fs to clear OAM resource struct tile shape upper field; not present in demo_state.inc.

---

### REF_SLOTS (USER-label + DATA-ref; RAM/ROM global or carve label)

| 槽 (addr) | target | gas_label | slot_label |
|-----------|--------|-----------|------------|
| 0x0801c2f8 | 0x02029eb0 | gVijaState | reset_gl_display_state_gvija_state |
| 0x0801c3e4 | 0x02029eb0 | gVijaState | load_vija_bg_gfx_embedded_gvija_state |
| 0x0801c504 | 0x02029eb0 | gVijaState | load_vija_obj_resource_by_region_gvija_state |
| 0x0801c598 | 0x02029eb0 | gVijaState | tick_vija_bg3_scroll_forward_gvija_state |
| 0x0801c5d4 | 0x02029eb0 | gVijaState | tick_vija_bg3_scroll_backward_gvija_state |
| 0x0801c628 | 0x02029eb0 | gVijaState | drive_vija_obj_cell_anim_gvija_state |
| 0x0801c6ac | 0x02029eb0 | gVijaState | tick_bg2_affine_anim_frame_gvija_state |
| 0x0801c704 | 0x02029eb0 | gVijaState | tick_bg_scroll_anim_frame_gvija_state |
| 0x0801c724 | 0x02029eb0 | gVijaState | get_vija_obj_slot_field8_gvija_state |
| 0x0801cafc | 0x02029eb0 | gVijaState | tick_all_vija_obj_anim_slots_gvija_state |
| 0x0801c95c | 0x09e399d0 | trig_table | tick_vija_obj_anim_slot_trig_table_b |
| 0x0801caa0 | 0x09e399d0 | trig_table | tick_vija_obj_anim_slot_trig_table_c |

Note: trig_table label is already carved in rom.s at line 829 (confirmed grep `trig_table:` in asm/rom.s). 0x09e399d0 ROM ref-scan = 7 (all code literal pool refs, no false positives).

---

### RENAME_SLOTS (纯改名 + EOL)

改名规则: 取值类型 + 函数前缀 + 语义后缀, 避碰撞用 `_b/_c` 或 `_hex` 后缀。

**ROM 地址槽** (raw ROM address, 无 equate 可用; 保留 raw value, 只改 label):

| 槽 (addr) | value | new slot_label | 语义 |
|-----------|-------|----------------|------|
| 0x0801b914 | 0x09e3cee8 | load_demo_shuen_sprite_gfx_gfx_resource_desc | shuen sprite GFX resource descriptor ptr |
| 0x0801ba48 | 0x09e3cf60 | load_shuen_obj_resource_by_slot_obj_resource_table | shuen OBJ resource table base |
| 0x0801bc24 | 0x09e3cfbf | tick_shuen_anim_slots_batch_coord_table | shuen 20-pair s8 screen coord table |
| 0x0801bdcc | 0x09e3cfe8 | demo_shuen_state_machine_bg1_resource_path | shuen BG1 file path ptr (shuen_bg1.LZ5bg) |
| 0x0801bdd0 | 0x09e3d004 | demo_shuen_state_machine_bg2_path | shuen BG2 file path ptr (shuen_bg2.LZ5bg) |
| 0x0801be98 | 0x09e3d01f | demo_shuen_state_machine_keyframe_phase_a | shuen phase A 3-byte keyframe table ptr |
| 0x0801c0b4 | 0x09e3d022 | demo_shuen_state_machine_keyframe_phase_b_a | shuen phase B keyframe A (loop start) |
| 0x0801c0b8 | 0x09e3d028 | demo_shuen_state_machine_keyframe_phase_b_b | shuen phase B keyframe B (loop end) |
| 0x0801c298 | 0x09e589a4 | tick_scene_step_by_step_table_a_step_table | ROM step table A base (scene step fn ptrs) |
| 0x0801c3e8 | 0x09e3d834 | load_vija_bg_gfx_embedded_bg_res_header | vija BG embedded resource header (16B) |
| 0x0801c3ec | 0x09e3d844 | load_vija_bg_gfx_embedded_bg_params | vija BG embedded params (8B coord table) |
| 0x0801c478 | 0x09e3d84c | load_vija_bg_gfx_from_fs_bg_fs_params | vija BG fs path ptr (wija_bg.LZ5bg variant) |
| 0x0801c508 | 0x09e3d964 | load_vija_obj_resource_by_region_obj_res_table | vija OBJ resource table (JP/US 8-ptr array) |
| 0x0801c708 | 0x09e3d9cf | tick_bg_scroll_anim_frame_bg_frame_params | vija BG frame cycle param table (4B) |

**内部跳转表指针槽** (switch jump table addr; 自指; 保留 raw value, 只改 label):

| 槽 (addr) | value | new slot_label |
|-----------|-------|----------------|
| 0x0801bd34 | 0x0801bd38 | demo_shuen_state_machine_switch_table_ptr |
| 0x0801c7bc | 0x0801c7c0 | tick_vija_obj_anim_slot_switch_table_ptr |
| 0x0801c880 | 0x0801c884 | tick_vija_obj_anim_slot_inner_switch_table_ptr_b |
| 0x0801c988 | 0x0801c98c | tick_vija_obj_anim_slot_inner_switch_table_ptr_c |

**PTR_ 槽** (已有正确 IO 寄存器 symbol value, 仅改 label):

| 槽 (addr) | value | current_label | new slot_label |
|-----------|-------|---------------|----------------|
| 0x0801ba70 | BG3HOFS | PTR_BG3HOFS_0801ba70 | write_shuen_bg3_scroll_regs_bg3hofs |
| 0x0801ba74 | BG3VOFS | PTR_BG3VOFS_0801ba74 | write_shuen_bg3_scroll_regs_bg3vofs |
| 0x0801bca8 | WININ | PTR_WININ_0801bca8 | apply_win0v_fadein_step_winin |
| 0x0801bcac | WINOUT | PTR_WINOUT_0801bcac | apply_win0v_fadein_step_winout |
| 0x0801bcb4 | WIN0V | PTR_WIN0V_0801bcb4 | apply_win0v_fadein_step_win0v |
| 0x0801bd04 | WIN0V | PTR_WIN0V_0801bd04 | apply_win0v_fadeout_step_win0v |
| 0x0801c70c | BG0VOFS | PTR_BG0VOFS_0801c70c | tick_bg_scroll_anim_frame_bg0vofs |

---

### FUNC_RENAME (误名订正)

无。Seg-10 所有 32 个函数名经 naming-proposals.csv 核实，名称与函数体语义一致，无误名信号。

---

### PLATE (R5)

#### PLATE-1: demo_shuen_state_machine (0x0801bd08) -- CJK plate 转 ASCII

**现 plate** (asm/00_system_str_vija.s line 18618, 含 CJK 终焉/过场等字符):
```
@ demo 'shuen' (終焉) 过场动画状态机 (7-state on [gDemoState+0x8c] bits 9..16). step 0 INIT: 加载 BG1 (FUN_0801b93c 'demo/shuen/shuen_bg1.LZ5bg') + BG2 (fs_load 'demo/shuen/shuen_bg2.LZ5bg' 缓存到 [gDemoState+0x88]) + OAM/window + 启 fade-in. step 1=wait init (poll FUN_080148f4). step 2=phase A (keyframe 0x09e3d01f, sub-state 按 0x3c/0x96/0x4b/0xa5/0xe6 分支). step 3=wait A. step 4=phase B (双 keyframe 0x09e3d022/0x09e3d028, 6帧循环, sub-state==0x78 推进). step 5=fadeout (3 种 brightness/blend 模式). step 6=wait fadeout. default 路径 cleanup (FUN_0801522c sprite + FUN_08015160 + FUN_080148f4 final poll). 返回 1=busy / 0=done. 唯一 caller: FUN_080bc880 case 3 (scene loader).
```

**新 plate** (全 ASCII):
```
@ demo 'shuen' (shuen/Syu-en) cinematic 7-state machine on [gDemoState+0x8c] bits[16:9]. State 0 INIT: load_shuen_bg1_gfx_set('demo/shuen/shuen_bg1.LZ5bg') + fs_load('demo/shuen/shuen_bg2.LZ5bg') cached to [gDemoState+0x88] + load_shuen_sprite_gfx_guarded x2 (OAM/window setup) + tick_demo_shuen_bg3_hscroll + gl_set_blend2_level(0x28,0,0x3c) fade-in + DISPCNT|=0x1800 (BG3+OBJ). State 1 WAIT_INIT: check_blend_transition_done; on done: clear [+0x8e] field bits. State 2 PHASE_A: memcpy 3-byte keyframe table from 0x09e3d01f; dispatch sub-state by sub_state bits (0x3c/0x96/0x4b/0xa5/0xe6 branches). State 3 WAIT_A. State 4 PHASE_B: dual keyframe 0x09e3d022/0x09e3d028; 6-frame sub-loop; tick_shuen_anim_slots_batch + tick_demo_shuen_bg3_hscroll. State 5 FADEOUT: 3-variant brightness/blend sequence. State 6 WAIT_FADEOUT: check_blend_transition_done. Default: copy_sprite_attr_table_to_oam + init_gl_palette_slot_flags + check_blend_transition_done final. Returns r0: 1=busy / 0=done. Caller: play_demo_shuen (0x080bc880) case 3.
```

**EOL corrections** (within body): existing EOL comments use CJK -- all 19 non-ASCII inline comments to be replaced with ASCII equivalents, e.g.:
- line 18632: `-- state > 6 -> default (cleanup)` (was: `-- state > 6 -> default (cleanup, 检查 done flag)`)
- line 18655: `-- case 0 INIT: load resources + start fade-in` (was: CJK)
- line 18662: `-- gDemoState[+0x88] = fs_load return (decompressed data ptr)` (was: CJK)
- etc. (all 19 non-ASCII inline comment lines identified by grep; full list in Phase 4 self-check)

#### PLATE-2: write_shuen_bg3_scroll_regs (0x0801ba5c) -- wrong IO addresses

**现 plate** (line 18251): says "BG3HOFS (0x04000018) and BG3VOFS (0x0400001e)" -- BG3HOFS value is wrong.

**Evidence**: ROM bytes at PTR_BG3HOFS_0801ba70 = 0x0400001c (verified python ROM read off=0x01ba70); GBA register map: BG3HOFS=0x0400001C, BG3VOFS=0x0400001E; gba_io.inc confirms BG3HOFS=0x0400001C (line 25). confidence=high.

**新 plate substring fix**: replace `BG3HOFS (0x04000018)` -> `BG3HOFS (0x0400001c)` in plate.

#### PLATE-3: apply_bg3_scroll_masked (0x0801c544) -- wrong IO addresses in plate + constants block

**现 plate** (lines 19685-19691): says "BG3HOFS (0x04000016)" and "BG3VOFS (0x04000018)" -- both wrong.

**Evidence**: ROM bytes DWORD_0801c558=0x0400001c (BG3HOFS), DWORD_0801c55c=0x0400001e (BG3VOFS); verified python read off 0x01c558/0x01c55c. confidence=high.

**新 plate** (全 ASCII, substring fix):
```
@ Called by tick_vija_bg3_scroll_forward (0x0801c560) and tick_vija_bg3_scroll_backward (0x0801c59c) during background scroll frame updates. r0 = horizontal offset (BG3HOFS), r1 = vertical offset (BG3VOFS); both are ANDed with mask 0x1ff (9-bit width) then written to the corresponding IO registers. Side effects: BG3HOFS (0x0400001c) := r0 & 0x1ff, BG3VOFS (0x0400001e) := r1 & 0x1ff. Leaf tool function for 9-bit precision write to background layer 3 scroll registers.
@
@ Constants:
@ SCROLL_MASK = 0x1ff (BG scroll register valid bit width 9 bits, [0..511])
@ BG3HOFS = 0x0400001c (background layer 3 horizontal scroll offset register)
@ BG3VOFS = 0x0400001e (background layer 3 vertical scroll offset register)
```

Note: FUN_ references in existing plates:
- load_demo_shuen_sprite_gfx plate: "FUN_0801b91c" -> load_shuen_sprite_gfx_guarded (fix); "FUN_0801bad0" -> tick_shuen_bg3_vscroll_phase (fix)
- load_shuen_obj_resource_slot0 plate: "FUN_0801ba04" -> load_shuen_obj_resource_by_slot (fix); "FUN_0801c254" -> tick_scene_step_by_step_table_a (fix)
- demo_shuen_state_machine plate: covered in PLATE-1 rewrite
- reset_gl_display_state plate: "FUN_0801cf74" -> tick_scene_step_by_step_table_b (fix); "FUN_0801cfcc" -> tick_scene_step_by_step_table_c (fix)
- load_vija_bg_gfx_by_mode plate: "FUN_0801cb00" -> run_vija_scene_state_machine (fix)
- load_vija_obj_resource_gated plate: "FUN_0801cf74"/"FUN_0801cfcc" -> same fixes
- drive_vija_obj_cell_anim plate: "FUN_0801c794" -> tick_vija_obj_anim_slot (fix)
- tick_bg2_affine_anim_frame plate: "FUN_0801cb00" -> run_vija_scene_state_machine (fix)
- tick_bg_scroll_anim_frame plate: "FUN_0801cb00" -> run_vija_scene_state_machine (fix)
- advance_scene_phase_counter plate: "FUN_0801c794" -> tick_vija_obj_anim_slot (fix)
- update_dual_cell_anim_oam_pos plate: "FUN_0801c794" -> tick_vija_obj_anim_slot (fix)
- tick_vija_obj_anim_slot plate: "FUN_0801cadc" -> tick_all_vija_obj_anim_slots (fix)
- tick_all_vija_obj_anim_slots plate: "FUN_0801cb00" -> run_vija_scene_state_machine (fix)

Total PLATE updates: 3 full/partial rewrites + ~14 FUN_ in-place fixes across multiple plates.

---

## carve 計劃 (R7)

無。段内無 ROM_INCBIN，不需要 carve。

---

## disasm 計劃 (R4)

無。段内無誤標代碼塊。

---

## 新增 constants / 全局

### constants/ewram.inc (新增)
```
.equ gVijaState, 0x02029eb0   @ vija scene (play_ui_effect_3b) per-frame state struct (0xc0 bytes)
                               @ +0x8c = u8  scroll_phase (vija BG3 horizontal scroll counter)
                               @ +0x8d = u8  scene_main_state (10-phase state, run_vija_scene_state_machine)
                               @ +0x90 = u8  bg2_affine_angle_counter (tick_bg2_affine_anim_frame)
                               @ +0x91 = u8  bg_frame_cycle (mod 4, tick_bg_scroll_anim_frame)
                               @ +0x98 = u8[5*8] slot_ctrl (5 OBJ anim slots * 8B each, tick_vija_obj_anim_slot)
                               @ Consumers: reset_gl_display_state, load_vija_bg_gfx_embedded,
                               @   load_vija_obj_resource_by_region, tick_vija_bg3_scroll_forward,
                               @   tick_vija_bg3_scroll_backward, drive_vija_obj_cell_anim,
                               @   tick_bg2_affine_anim_frame, tick_bg_scroll_anim_frame,
                               @   get_vija_obj_slot_field8, tick_all_vija_obj_anim_slots,
                               @   run_vija_scene_state_machine (file 01)
```

### constants/demo_state.inc (新增)
```
@ Vija scene display reset constants (reset_gl_display_state)
.equ VIJA_CPUSET_FILL_CTRL, 0x05000030  @ bios_cpu_set fill ctrl: count=0x30 words (=0xc0 bytes), fill+32bit
.equ VIJA_DISPCNT_INIT,     0x00001741  @ DISPCNT init val: BG mode 1, OBJ+BG0-1, OBJ 1-D mapping
.equ VIJA_BG0CNT_INIT,      0x00001d81  @ BG0CNT init val (scrbase=29, charbase=2, 256col, 32x32)
.equ VIJA_BG1CNT_INIT,      0x00001e82  @ BG1CNT init val
.equ VIJA_BG2CNT_INIT,      0x00001f8b  @ BG2CNT init val

@ Bitfield clear mask for step index field (tick_scene_step_by_step_table_a)
.equ SCENE_STEP_IDX_CLEAR_MASK, 0xffc03fff  @ clears bits[21:14] (8-bit step index in gPrng+0x204)

@ Additional bitfield mask
.equ DEMO_CLEAR_BITS_16_14, 0xfffe3fff  @ clears bits[16:14] (~0x0001c000); OAM resource struct tile shape field
```

---

## §5.1 登記

無 (段内無 ROM_INCBIN 塊，無未引用數據區)。

---

## 消費者證據 (R6) -- 關鍵槽語義

1. **gVijaState=0x02029eb0**: asm/00_system_str_vija.s line 19382 plate (reset_gl_display_state bios_cpu_set 0xc0 bytes from this addr); line 19708-19713 plate (tick_vija_bg3_scroll_forward "VIJA_STATE=0x02029eb0; SCROLL_PHASE_OFF=0x8c"); asm/01_vija_scene_text.s line 4 (run_vija_scene_state_machine "all state from IWRAM 0x02029eb0"). confidence=high.

2. **VIJA_CPUSET_FILL_CTRL=0x05000030**: reset_gl_display_state body: `ldr r1, DAT_0801c2f8` (gVijaState=0x02029eb0), `ldr r2, DAT_0801c2fc` (0x05000030), `bl bios_cpu_set` (asm line 19354-19355). 0x05000030: bit26=1(32-bit), bit24=1(fill), count=0x30(48 words=192B). confidence=high.

3. **VIJA_DISPCNT_INIT=0x1741**: reset_gl_display_state: `movs r1,#0x80; lsls r1,r1,#0x13` -> r1=DISPCNT(0x04000000), `ldr r0, DAT_0801c300`=0x1741, `strh r0,[r1,#0x0]` (asm line 19357-19360). ROM byte verify: off 0x01c300 -> `41 17 00 00` = 0x00001741. confidence=high.

4. **SCENE_STEP_IDX_CLEAR_MASK=0xffc03fff**: tick_scene_step_by_step_table_a plate (asm line 19298): "STEP_ADVANCE_MASK = 0xffc03fff (step field clear mask)". ROM byte verify: off 0x01c2a0 -> `ff 3f c0 ff` = 0xffc03fff. ~0xffc03fff=0x003fc000=bits[21:14]. confidence=high.

5. **trig_table=0x09e399d0**: already carved in asm/rom.s line 829 (`trig_table:`); confirmed by trig_table[0]=0x0000 (sin 0), trig_table[1]=0x0006 (sin 1 ~Q8.8). confidence=high.

6. **BG3HOFS/VOFS wrong plate**: PTR_BG3HOFS_0801ba70 ROM bytes (off 0x01ba70) = 0x0400001c = BG3HOFS (gba_io.inc line 25); PTR_BG3VOFS_0801ba74 ROM bytes (off 0x01ba74) = 0x0400001e = BG3VOFS (gba_io.inc line 26). Plate says 0x04000018 which is BG2HOFS (GBA reg map error). confidence=high.

---

## 求助

無低置信度語義，無 BLOCKED 項。

---

## Executor Report: Seg-10

- 槽: EQ=33 (26 reuse existing consts + 7 new) REF=12 (10 gVijaState + 2 trig_table) RENAME=18 (14 ROM addr + 4 switch ptr) PTR_label_fix=7 FUNC_RENAME=0 PLATE=3 (1 CJK full-rewrite + 14 FUN_ fixes across plates + 2 wrong-IO-addr substring fixes)
- carve=0 disasm=0 §5.1=0
- 新增 constants/全局: gVijaState (ewram.inc) + 7 new EQ in demo_state.inc (VIJA_CPUSET_FILL_CTRL / VIJA_DISPCNT_INIT / VIJA_BG0CNT_INIT / VIJA_BG1CNT_INIT / VIJA_BG2CNT_INIT / SCENE_STEP_IDX_CLEAR_MASK / DEMO_CLEAR_BITS_16_14)
- 求助: none
- 有無越界: 無 (全部 32 fn 均 < 0x0801cb00; DAT_0801cafc=0x0801cafc < 0x0801cb00; file 01 首函數 run_vija_scene_state_machine @0x0801cb00 不納入)
- proposal: doc/dev/refine/Seg-10.proposal.md
