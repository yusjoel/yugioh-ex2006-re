# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineSeg10Slots.py -- p5 Seg-10 (0x0801b850..0x0801cb00)
#   vija/shuen scene tick (32 functions):
#   load_demo_shuen_sprite_gfx / load_shuen_sprite_gfx_guarded /
#   load_shuen_bg1_gfx_set / load_shuen_obj_resource_by_slot /
#   load_shuen_obj_resource_slot0 / write_shuen_bg3_scroll_regs /
#   tick_demo_shuen_bg3_hscroll / tick_shuen_bg3_vscroll_phase /
#   advance_shuen_cell_anim_frame / tick_shuen_anim_slots_batch /
#   apply_win0v_fadein_step / apply_win0v_fadeout_step /
#   demo_shuen_state_machine / tick_scene_step_by_step_table_a /
#   reset_gl_display_state / load_vija_bg_gfx_embedded /
#   load_vija_bg_gfx_from_fs / load_vija_bg_gfx_by_mode /
#   load_vija_obj_resource_by_region / load_vija_obj_resource_gated /
#   apply_bg3_scroll_masked / tick_vija_bg3_scroll_forward /
#   tick_vija_bg3_scroll_backward / drive_vija_obj_cell_anim /
#   apply_bg2_affine_fixed_angle / tick_bg2_affine_anim_frame /
#   tick_bg_scroll_anim_frame / get_vija_obj_slot_field8 /
#   advance_scene_phase_counter / update_dual_cell_anim_oam_pos /
#   tick_vija_obj_anim_slot / tick_all_vija_obj_anim_slots
#
# Sections:
#   A. EQ_SLOTS   -- data-equate (26 reuse + 6 new)
#   B. REF_SLOTS  -- USER label on target + DATA ref + slot rename
#   C. RENAME_SLOTS -- plain rename + optional EOL (pure ASCII)
#   D. PLATE_REWRITES -- FUN_ -> current name + IO address fixes
#   E. CJK_PLATE_REWRITE -- full rewrite of demo_shuen_state_machine plate (ASCII)
#   F. CJK_EOL_FIXES -- replace CJK inline EOL comments with ASCII
#
# REVIEW FIXES APPLIED:
#   #1 (C5): slot 0x0801c2a0 uses NAME_INPUT_PAGE_STATE_CLEAR (existing)
#             instead of new SCENE_STEP_IDX_CLEAR_MASK; 6 new EQ not 7.
#   #2 (C13): 9 additional RENAME slots added (6 gDemoState + gPrng + BG3HOFS + BG3VOFS)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).

from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.data import DWordDataType, DataTypeConflictHandler

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

# ---------------------------------------------------------------------------
# A. EQ_SLOTS: (slot_addr, value, eq_name, slot_label, eol_ascii_or_None)
#    Creates equate (value -> name) and references it from slot address.
#    Slot label MUST differ from eq_name to avoid GAS ldr/equate conflict.
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # --- demo_state.inc: DEMO_CLEAR_BITS_13_7 = 0xffffc07f (4 slots) ---
    (0x0801b918, 0xffffc07f, 'DEMO_CLEAR_BITS_13_7',
     'load_demo_shuen_sprite_gfx_oam_palette_mask',
     'OAM palette field clear mask bits[13:7]'),
    (0x0801ba00, 0xffffc07f, 'DEMO_CLEAR_BITS_13_7',
     'load_shuen_bg1_gfx_set_oam_palette_mask', None),
    (0x0801c3f0, 0xffffc07f, 'DEMO_CLEAR_BITS_13_7',
     'load_vija_bg_gfx_embedded_oam_palette_mask', None),
    (0x0801c47c, 0xffffc07f, 'DEMO_CLEAR_BITS_13_7',
     'load_vija_bg_gfx_from_fs_oam_palette_mask', None),

    # --- demo_state.inc: DEMO_KEEP_BITS_8_0 = 0x000001ff (2 slots) ---
    (0x0801ba6c, 0x000001ff, 'DEMO_KEEP_BITS_8_0',
     'write_shuen_bg3_scroll_regs_scroll_mask',
     '9-bit scroll mask bits[8:0]'),
    (0x0801c554, 0x000001ff, 'DEMO_KEEP_BITS_8_0',
     'apply_bg3_scroll_masked_scroll_mask', None),

    # --- demo_state.inc: DEMO_CLEAR_BITS_8_1 = 0xfffffe01 (7 slots) ---
    (0x0801bacc, 0xfffffe01, 'DEMO_CLEAR_BITS_8_1',
     'tick_demo_shuen_bg3_hscroll_counter_clear_mask',
     'clear bits[8:1] of hscroll counter'),
    (0x0801bb24, 0xfffffe01, 'DEMO_CLEAR_BITS_8_1',
     'tick_shuen_bg3_vscroll_phase_counter_clear_mask', None),
    (0x0801be28, 0xfffffe01, 'DEMO_CLEAR_BITS_8_1',
     'demo_shuen_state_machine_substate_clear_mask_a', None),
    (0x0801bf94, 0xfffffe01, 'DEMO_CLEAR_BITS_8_1',
     'demo_shuen_state_machine_substate_clear_mask_b', None),
    (0x0801bfd0, 0xfffffe01, 'DEMO_CLEAR_BITS_8_1',
     'demo_shuen_state_machine_substate_clear_mask_c', None),
    (0x0801c0c0, 0xfffffe01, 'DEMO_CLEAR_BITS_8_1',
     'demo_shuen_state_machine_substate_clear_mask_d', None),
    (0x0801c160, 0xfffffe01, 'DEMO_CLEAR_BITS_8_1',
     'demo_shuen_state_machine_substate_clear_mask_e', None),

    # --- demo_state.inc: DEMO_CLEAR_BITS_16_9 = 0xfffe01ff (5 slots) ---
    (0x0801bdd8, 0xfffe01ff, 'DEMO_CLEAR_BITS_16_9',
     'demo_shuen_state_machine_state_clear_mask_a',
     'clear state bits[16:9] in gDemoState+0x8c'),
    (0x0801be2c, 0xfffe01ff, 'DEMO_CLEAR_BITS_16_9',
     'demo_shuen_state_machine_state_clear_mask_b', None),
    (0x0801bf98, 0xfffe01ff, 'DEMO_CLEAR_BITS_16_9',
     'demo_shuen_state_machine_state_clear_mask_c', None),
    (0x0801bfd4, 0xfffe01ff, 'DEMO_CLEAR_BITS_16_9',
     'demo_shuen_state_machine_state_clear_mask_d', None),
    (0x0801c0c4, 0xfffe01ff, 'DEMO_CLEAR_BITS_16_9',
     'demo_shuen_state_machine_state_clear_mask_e', None),

    # --- demo_state.inc: DEMO_CLEAR_BITS_14_13 = 0xffff9fff (1 slot) ---
    (0x0801bcb0, 0xffff9fff, 'DEMO_CLEAR_BITS_14_13',
     'apply_win0v_fadein_step_dispcnt_clear_mask',
     'DISPCNT clear bits[14:13] (WIN0/WIN1 display enable)'),

    # --- demo_state.inc: DEMO_CLEAR_BITS_12_8 = 0xffffe0ff (3 slots) ---
    (0x0801bdd4, 0xffffe0ff, 'DEMO_CLEAR_BITS_12_8',
     'demo_shuen_state_machine_dispcnt_clear_mask',
     'DISPCNT clear bits[12:8] (BG/OBJ enable field)'),
    (0x0801c0bc, 0xffffe0ff, 'DEMO_CLEAR_BITS_12_8',
     'demo_shuen_state_machine_dispcnt_clear_mask_b', None),
    (0x0801c1c0, 0xffffe0ff, 'DEMO_CLEAR_BITS_12_8',
     'demo_shuen_state_machine_dispcnt_clear_mask_c', None),

    # --- demo_state.inc: DEMO_CLEAR_BITS_8_1 already listed; one more ---
    (0x0801c204, 0xfffffe01, 'DEMO_CLEAR_BITS_8_1',
     'demo_shuen_state_machine_substate_clear_mask_f', None),

    # --- rom_region.inc: ROM_REGION_CODE_ADDR = 0x080000ae (1 slot) ---
    (0x0801c538, 0x080000ae, 'ROM_REGION_CODE_ADDR',
     'load_vija_obj_resource_by_region_rom_region_addr',
     'ROM header game-code region address (JP detect)'),

    # --- gba_mem.inc: EWRAM_BASE = 0x02000000 (1 slot) ---
    (0x0801c53c, 0x02000000, 'EWRAM_BASE',
     'load_vija_obj_resource_by_region_ewram_base', None),

    # --- name_input.inc: GSETTINGS_OFFSET = 0x00006c2c (1 slot) ---
    (0x0801c540, 0x00006c2c, 'GSETTINGS_OFFSET',
     'load_vija_obj_resource_by_region_gsettings_off',
     'gSettings offset from EWRAM_BASE'),

    # --- name_input.inc: NAME_INPUT_PAGE_STATE_CLEAR = 0xffc03fff (1 slot) ---
    # C5 fix: reuse existing constant instead of new SCENE_STEP_IDX_CLEAR_MASK
    (0x0801c2a0, 0xffc03fff, 'NAME_INPUT_PAGE_STATE_CLEAR',
     'tick_scene_step_by_step_table_a_step_idx_clear_mask',
     'bits[21:14] clear mask for step index field in gPrng+0x204'),

    # --- demo_state.inc NEW: VIJA_CPUSET_FILL_CTRL = 0x05000030 (1 slot) ---
    (0x0801c2fc, 0x05000030, 'VIJA_CPUSET_FILL_CTRL',
     'reset_gl_display_state_cpuset_ctrl',
     'bios_cpu_set fill+32bit: count=0x30 words (0xc0 bytes) to zero gVijaState'),

    # --- demo_state.inc NEW: VIJA_DISPCNT_INIT = 0x00001741 (1 slot) ---
    (0x0801c300, 0x00001741, 'VIJA_DISPCNT_INIT',
     'reset_gl_display_state_dispcnt_init',
     'DISPCNT init: mode1 + OBJ+BG0-1 + OBJ 1-D'),

    # --- demo_state.inc NEW: VIJA_BG0CNT_INIT = 0x00001d81 (1 slot) ---
    (0x0801c304, 0x00001d81, 'VIJA_BG0CNT_INIT',
     'reset_gl_display_state_bg0cnt_init', None),

    # --- demo_state.inc NEW: VIJA_BG1CNT_INIT = 0x00001e82 (1 slot) ---
    (0x0801c308, 0x00001e82, 'VIJA_BG1CNT_INIT',
     'reset_gl_display_state_bg1cnt_init', None),

    # --- demo_state.inc NEW: VIJA_BG2CNT_INIT = 0x00001f8b (1 slot) ---
    (0x0801c30c, 0x00001f8b, 'VIJA_BG2CNT_INIT',
     'reset_gl_display_state_bg2cnt_init', None),

    # --- demo_state.inc NEW: DEMO_CLEAR_BITS_16_14 = 0xfffe3fff (1 slot) ---
    (0x0801c480, 0xfffe3fff, 'DEMO_CLEAR_BITS_16_14',
     'load_vija_bg_gfx_from_fs_tile_shape_clear_mask',
     'clear bits[16:14]: OAM resource struct tile shape upper field'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_vaddr, gas_label, slot_label, eol_or_None)
#    Creates USER_DEFINED label at target, DATA ref from slot, renames slot.
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # --- gVijaState (ewram.inc NEW, 0x02029eb0) -- 10 slots ---
    (0x0801c2f8, 0x02029eb0, 'gVijaState',
     'reset_gl_display_state_gvija_state',
     'bios_cpu_set fill-zero: clear 0xc0 bytes from gVijaState'),
    (0x0801c3e4, 0x02029eb0, 'gVijaState',
     'load_vija_bg_gfx_embedded_gvija_state', None),
    (0x0801c504, 0x02029eb0, 'gVijaState',
     'load_vija_obj_resource_by_region_gvija_state', None),
    (0x0801c598, 0x02029eb0, 'gVijaState',
     'tick_vija_bg3_scroll_forward_gvija_state', None),
    (0x0801c5d4, 0x02029eb0, 'gVijaState',
     'tick_vija_bg3_scroll_backward_gvija_state', None),
    (0x0801c628, 0x02029eb0, 'gVijaState',
     'drive_vija_obj_cell_anim_gvija_state', None),
    (0x0801c6ac, 0x02029eb0, 'gVijaState',
     'tick_bg2_affine_anim_frame_gvija_state', None),
    (0x0801c704, 0x02029eb0, 'gVijaState',
     'tick_bg_scroll_anim_frame_gvija_state', None),
    (0x0801c724, 0x02029eb0, 'gVijaState',
     'get_vija_obj_slot_field8_gvija_state', None),
    (0x0801cafc, 0x02029eb0, 'gVijaState',
     'tick_all_vija_obj_anim_slots_gvija_state', None),

    # --- trig_table (rom.s carve, 0x09e399d0) -- 2 slots ---
    (0x0801c95c, 0x09e399d0, 'trig_table',
     'tick_vija_obj_anim_slot_trig_table_b',
     'sin/cos lookup table (512B, 256 s16 entries, amplitude 256=Q8.8)'),
    (0x0801caa0, 0x09e399d0, 'trig_table',
     'tick_vija_obj_anim_slot_trig_table_c', None),

    # --- gDemoState (ewram.inc, 0x02029ec0) -- 6 slots (C13 fix) ---
    (0x0801b910, 0x02029ec0, 'gDemoState',
     'load_demo_shuen_sprite_gfx_ptr_gdemostate', None),
    (0x0801ba44, 0x02029ec0, 'gDemoState',
     'load_shuen_obj_resource_by_slot_ptr_gdemostate', None),
    (0x0801bac8, 0x02029ec0, 'gDemoState',
     'tick_demo_shuen_bg3_hscroll_ptr_gdemostate', None),
    (0x0801bb20, 0x02029ec0, 'gDemoState',
     'tick_shuen_bg3_vscroll_phase_ptr_gdemostate', None),
    (0x0801bb94, 0x02029ec0, 'gDemoState',
     'advance_shuen_cell_anim_frame_ptr_gdemostate', None),
    (0x0801bd30, 0x02029ec0, 'gDemoState',
     'demo_shuen_state_machine_ptr_gdemostate', None),

    # --- gPrng (iwram.inc, 0x03000040) -- 1 slot (C13 fix) ---
    (0x0801c29c, 0x03000040, 'gPrng',
     'tick_scene_step_by_step_table_a_ptr_gprng', None),

    # --- BG3HOFS (IO, 0x0400001c) -- 1 slot (C13 fix) ---
    (0x0801c558, 0x0400001c, 'BG3HOFS',
     'apply_bg3_scroll_masked_ptr_bg3hofs', None),

    # --- BG3VOFS (IO, 0x0400001e) -- 1 slot (C13 fix) ---
    (0x0801c55c, 0x0400001e, 'BG3VOFS',
     'apply_bg3_scroll_masked_ptr_bg3vofs', None),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
#    Plain rename + optional EOL comment (pure ASCII, no CJK).
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    # ROM address slots (raw ROM address, no equate)
    (0x0801b914, 'load_demo_shuen_sprite_gfx_gfx_resource_desc',
     'shuen sprite GFX resource descriptor ptr (0x09e3cee8)'),
    (0x0801ba48, 'load_shuen_obj_resource_by_slot_obj_resource_table',
     'shuen OBJ resource table base (0x09e3cf60)'),
    (0x0801bc24, 'tick_shuen_anim_slots_batch_coord_table',
     'shuen 20-pair s8 screen coord table (0x09e3cfbf)'),
    (0x0801bdcc, 'demo_shuen_state_machine_bg1_resource_path',
     'shuen BG1 file path ptr (demo/shuen/shuen_bg1.LZ5bg)'),
    (0x0801bdd0, 'demo_shuen_state_machine_bg2_path',
     'shuen BG2 file path ptr (demo/shuen/shuen_bg2.LZ5bg)'),
    (0x0801be98, 'demo_shuen_state_machine_keyframe_phase_a',
     'shuen phase A 3-byte keyframe table ptr (0x09e3d01f)'),
    (0x0801c0b4, 'demo_shuen_state_machine_keyframe_phase_b_a',
     'shuen phase B keyframe A - loop start (0x09e3d022)'),
    (0x0801c0b8, 'demo_shuen_state_machine_keyframe_phase_b_b',
     'shuen phase B keyframe B - loop end (0x09e3d028)'),
    (0x0801c298, 'tick_scene_step_by_step_table_a_step_table',
     'ROM step table A base - scene step fn ptrs (0x09e589a4)'),
    (0x0801c3e8, 'load_vija_bg_gfx_embedded_bg_res_header',
     'vija BG embedded resource header 16B (0x09e3d834)'),
    (0x0801c3ec, 'load_vija_bg_gfx_embedded_bg_params',
     'vija BG embedded params 8B coord table (0x09e3d844)'),
    (0x0801c478, 'load_vija_bg_gfx_from_fs_bg_fs_params',
     'vija BG fs path ptr (wija_bg.LZ5bg variant, 0x09e3d84c)'),
    (0x0801c508, 'load_vija_obj_resource_by_region_obj_res_table',
     'vija OBJ resource table JP/US 8-ptr array (0x09e3d964)'),
    (0x0801c708, 'tick_bg_scroll_anim_frame_bg_frame_params',
     'vija BG frame cycle param table 4B (0x09e3d9cf)'),

    # Internal jump table pointer slots
    (0x0801bd34, 'demo_shuen_state_machine_switch_table_ptr',
     'ptr to 7-entry switch jump table at 0x0801bd38'),
    (0x0801c7bc, 'tick_vija_obj_anim_slot_switch_table_ptr',
     'ptr to switch jump table at 0x0801c7c0'),
    (0x0801c880, 'tick_vija_obj_anim_slot_inner_switch_table_ptr_b',
     'ptr to inner switch jump table at 0x0801c884'),
    (0x0801c988, 'tick_vija_obj_anim_slot_inner_switch_table_ptr_c',
     'ptr to inner switch jump table at 0x0801c98c'),

    # NOTE: 0x0801ad40/ad80/adc0/adfc/ae00 are handled in DWORD_SLOTS below.
    # They need createDWord to be recognized as .word entries by the exporter.

    # PTR_ slots -- already have correct IO register symbol values, rename label only
    (0x0801ba70, 'write_shuen_bg3_scroll_regs_bg3hofs',
     'BG3HOFS (0x0400001c) horizontal scroll register'),
    (0x0801ba74, 'write_shuen_bg3_scroll_regs_bg3vofs',
     'BG3VOFS (0x0400001e) vertical scroll register'),
    (0x0801bca8, 'apply_win0v_fadein_step_winin',
     'WININ window inside control'),
    (0x0801bcac, 'apply_win0v_fadein_step_winout',
     'WINOUT window outside control'),
    (0x0801bcb4, 'apply_win0v_fadein_step_win0v',
     'WIN0V window 0 vertical bounds'),
    (0x0801bd04, 'apply_win0v_fadeout_step_win0v',
     'WIN0V window 0 vertical bounds'),
    (0x0801c70c, 'tick_bg_scroll_anim_frame_bg0vofs',
     'BG0VOFS vertical scroll register'),
]

# ---------------------------------------------------------------------------
# D. PLATE_REWRITES: (func_addr, old_text, new_text)
#    Replaces FUN_ references and wrong IO addresses in existing plate comments.
#    All text must be pure ASCII.
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    # load_shuen_obj_resource_slot0 plate: FUN_ -> current names
    (0x0801ba4c, 'FUN_0801ba04', 'load_shuen_obj_resource_by_slot'),
    (0x0801ba4c, 'FUN_0801c254', 'tick_scene_step_by_step_table_a'),

    # write_shuen_bg3_scroll_regs plate: wrong IO address fix (C5/PLATE-2)
    # BG3HOFS was written as 0x04000018 (which is BG2HOFS), correct is 0x0400001c
    (0x0801ba5c, 'BG3HOFS (0x04000018)', 'BG3HOFS (0x0400001c)'),

    # reset_gl_display_state plate: FUN_ -> current names
    (0x0801c2ac, 'FUN_0801cf74', 'tick_scene_step_by_step_table_b'),
    (0x0801c2ac, 'FUN_0801cfcc', 'tick_scene_step_by_step_table_c'),

    # load_vija_bg_gfx_by_mode plate: FUN_ -> current name
    (0x0801c484, 'FUN_0801cb00', 'run_vija_scene_state_machine'),

    # load_vija_obj_resource_gated plate: FUN_ -> current names
    (0x0801c50c, 'FUN_0801cf74', 'tick_scene_step_by_step_table_b'),
    (0x0801c50c, 'FUN_0801cfcc', 'tick_scene_step_by_step_table_c'),

    # drive_vija_obj_cell_anim plate: FUN_ -> current name
    (0x0801c5d8, 'FUN_0801c794', 'tick_vija_obj_anim_slot'),

    # tick_bg2_affine_anim_frame plate: FUN_ -> current name
    (0x0801c694, 'FUN_0801cb00', 'run_vija_scene_state_machine'),

    # tick_bg_scroll_anim_frame plate: FUN_ -> current name
    (0x0801c6b0, 'FUN_0801cb00', 'run_vija_scene_state_machine'),

    # advance_scene_phase_counter plate: FUN_ -> current name
    (0x0801c728, 'FUN_0801c794', 'tick_vija_obj_anim_slot'),

    # update_dual_cell_anim_oam_pos plate: FUN_ -> current name
    (0x0801c74c, 'FUN_0801c794', 'tick_vija_obj_anim_slot'),

    # tick_vija_obj_anim_slot plate: FUN_ -> current name
    (0x0801c794, 'FUN_0801cadc', 'tick_all_vija_obj_anim_slots'),

    # tick_all_vija_obj_anim_slots plate: FUN_ -> current name
    (0x0801cadc, 'FUN_0801cb00', 'run_vija_scene_state_machine'),

    # load_demo_shuen_sprite_gfx plate: FUN_ -> current name
    (0x0801b850, 'FUN_0801b91c', 'load_shuen_sprite_gfx_guarded'),

    # write_shuen_bg3_scroll_regs plate: FUN_ -> current name
    (0x0801ba5c, 'FUN_0801bad0', 'tick_shuen_bg3_vscroll_phase'),
]

# ---------------------------------------------------------------------------
# E. CJK_PLATE_REWRITE: full plate replacement for demo_shuen_state_machine
#    All text pure ASCII.
# ---------------------------------------------------------------------------
CJK_PLATE_REWRITES = [
    (0x0801bd08,
     "@ demo 'shuen' (shuen/Syu-en) cinematic 7-state machine on [gDemoState+0x8c] bits[16:9].\n"
     "@ State 0 INIT: load_shuen_bg1_gfx_set('demo/shuen/shuen_bg1.LZ5bg') +\n"
     "@   fs_load('demo/shuen/shuen_bg2.LZ5bg') cached to [gDemoState+0x88] +\n"
     "@   load_shuen_sprite_gfx_guarded x2 (OAM/window setup) +\n"
     "@   tick_demo_shuen_bg3_hscroll + gl_set_blend2_level(0x28,0,0x3c) fade-in +\n"
     "@   DISPCNT|=0x1800 (BG3+OBJ enabled).\n"
     "@ State 1 WAIT_INIT: check_blend_transition_done; on done: clear [gDemoState+0x8e] field bits.\n"
     "@ State 2 PHASE_A: memcpy 3-byte keyframe table from 0x09e3d01f;\n"
     "@   dispatch sub-state by sub_state bits (0x3c/0x96/0x4b/0xa5/0xe6 branches).\n"
     "@ State 3 WAIT_A: check_blend_transition_done.\n"
     "@ State 4 PHASE_B: dual keyframe 0x09e3d022/0x09e3d028; 6-frame sub-loop;\n"
     "@   tick_shuen_anim_slots_batch + tick_demo_shuen_bg3_hscroll.\n"
     "@ State 5 FADEOUT: 3-variant brightness/blend sequence.\n"
     "@ State 6 WAIT_FADEOUT: check_blend_transition_done.\n"
     "@ Default (state>6): copy_sprite_attr_table_to_oam + init_gl_palette_slot_flags +\n"
     "@   check_blend_transition_done final.\n"
     "@ Returns r0: 1=busy / 0=done.\n"
     "@ Caller: play_demo_shuen (0x080bc880) case 3."),
]

# ---------------------------------------------------------------------------
# F. CJK_EOL_FIXES: (addr, new_eol_ascii)
#    Replace CJK inline EOL comments with pure ASCII equivalents.
#    Addresses are from the 19 non-ASCII EOL lines identified in the asm.
# ---------------------------------------------------------------------------
CJK_EOL_FIXES = [
    # 0x0801bd20: state > 6 -> default cleanup
    (0x0801bd20, 'state > 6 -> default cleanup path'),
    # 0x0801bd2c: switch dispatch
    (0x0801bd2c, 'switch dispatch: load jump_table entry, mov pc'),
    # 0x0801bd54: case 0 INIT: load resources + start fade-in
    (0x0801bd54, 'case 0 INIT: load resources + start fade-in'),
    # 0x0801bd5e: fs_load call
    (0x0801bd5e, "fs_load('demo/shuen/shuen_bg2.LZ5bg', 0)"),
    # 0x0801bd66: gDemoState[+0x88] = fs_load return value
    (0x0801bd66, 'gDemoState[+0x88] = fs_load return (decompressed data ptr)'),
    # 0x0801bd76: FUN_0801b91c(0,0,1,1) call
    (0x0801bd76, 'load_shuen_sprite_gfx_guarded(0,0,1,1) -- OAM/window setup #1'),
    # 0x0801bd86: FUN_0801b91c(0,1,0,2) call
    (0x0801bd86, 'load_shuen_sprite_gfx_guarded(0,1,0,2) -- OAM/window setup #2'),
    # 0x0801bd94: gl_set_blend2_level call -- start fade-in
    (0x0801bd94, 'gl_set_blend2_level(0x28, 0, 0x3c) -- start fade-in'),
    # 0x0801bda8: DISPCNT |= 0x1800 -- enable BG3 + OBJ
    (0x0801bda8, 'DISPCNT |= 0x1800: enable BG3 + OBJ display'),
    # 0x0801bdac: FUN_080f9adc(3) sound
    (0x0801bdac, 'set_channel_if_changed(3) -- sound channel trigger'),
    # 0x0801bdc8: gDemoState[+0x8c]: state++
    (0x0801bdc8, 'gDemoState[+0x8c]: state++ packed into bits[16:9]'),
    # 0x0801bddc: case 1 WAIT_INIT
    (0x0801bddc, 'case 1 WAIT_INIT: check_blend_transition_done'),
    # 0x0801bde2: r0 != 0 (still busy)
    (0x0801bde2, 'r0 != 0 (still busy) -> skip state advance'),
    # 0x0801be30: case 2 PHASE_A: keyframe
    (0x0801be30, 'case 2 PHASE_A: copy keyframe table from 0x09e3d01f'),
    # 0x0801be36: memcpy call
    (0x0801be36, 'memcpy(stack+0x8, 0x09e3d01f, 3) -- copy 3-byte keyframe table'),
    # 0x0801bf9c: case 3 WAIT_A
    (0x0801bf9c, 'case 3 WAIT_A: check_blend_transition_done for phase A'),
    # 0x0801bfd8: case 4 PHASE_B
    (0x0801bfd8, 'case 4 PHASE_B: dual keyframe 6-frame sub-loop'),
    # 0x0801c0c8: case 5 FADEOUT
    (0x0801c0c8, 'case 5 FADEOUT: 3-variant brightness/blend sequence'),
    # 0x0801c208: case 6 WAIT_FADEOUT
    (0x0801c208, 'case 6 WAIT_FADEOUT: check_blend_transition_done'),
    # 0x0801c22a: r0 != 0 (gl busy)
    (0x0801c22a, 'r0 != 0 (gl busy) -> skip cleanup return 0 path'),
    # 0x0801c230: check done flag
    (0x0801c230, 'read gDemoState[+0x8c] bit0 (done flag)'),
    # 0x0801c238: bit0 set + gl ready
    (0x0801c238, 'bit0 set + gl ready -> r0=1 (busy, one more frame)'),
    # 0x0801c242: epilogue
    (0x0801c242, 'epilogue: return r0 (1=busy / 0=done)'),
]

# ---------------------------------------------------------------------------
# G. DWORD_SLOTS: (slot_addr, expected_val, slot_label, eol_or_None)
#    Force-create DWord data type at addr + rename label.
#    Used to restore literal-pool entries that lost their label after re-analysis.
# ---------------------------------------------------------------------------
DWORD_SLOTS = [
    # Restore labels in dispatch_banlist_cursor_action (Seg-9 area, 0x0801ad00-0x0801ae10)
    # These slots had DAT_ labels that disappeared after headless re-analysis.
    (0x0801ad40, 0x0000064c,
     'dispatch_banlist_cursor_action_scroll_cursor_hw_off_a',
     'cursor halfword offset in gBanlistPasswordBuffer (0x64c)'),
    (0x0801ad80, 0x0000064c,
     'dispatch_banlist_cursor_action_scroll_cursor_hw_off_b',
     'cursor halfword offset in gBanlistPasswordBuffer (0x64c)'),
    (0x0801adc0, 0x0000065c,
     'dispatch_banlist_cursor_action_scroll_row_byte_off',
     'row height byte offset (0x65c)'),
    (0x0801adfc, 0x03000040,
     'dispatch_banlist_cursor_action_ptr_gprng_b',
     'gPrng second ref in cursor action handler (0x03000040)'),
    (0x0801ae00, 0x0000023a,
     'dispatch_banlist_cursor_action_cursor_px_base',
     'cursor pixel pos base offset (0x023a=570 into EWRAM)'),
]

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

def _check(slot_addr, expected_val, label):
    """Verify ROM dword at slot_addr == expected_val. Return True if OK."""
    mem = currentProgram.getMemory()
    a = _addr(slot_addr)
    try:
        actual = mem.getInt(a) & 0xFFFFFFFF
    except Exception as e:
        print("[FAIL] _check 0x%08x (%s): read error %s" % (slot_addr, label, e))
        return False
    if actual != (expected_val & 0xFFFFFFFF):
        print("[FAIL] _check 0x%08x (%s): got 0x%08x expected 0x%08x" % (
            slot_addr, label, actual, expected_val & 0xFFFFFFFF))
        return False
    return True

def _apply_eq(slot_addr, value, eq_name, slot_label, eol):
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()
    eq_tbl = currentProgram.getEquateTable()

    if not _check(slot_addr, value, eq_name):
        print("[SKIP] EQ 0x%08x (%s) value mismatch" % (slot_addr, eq_name))
        return

    if DRY:
        print("[dry] EQ 0x%08x  %s=%s  label=%s" % (slot_addr, eq_name, hex(value), slot_label))
        return

    # create/get equate
    eq = eq_tbl.getEquate(eq_name)
    if eq is None:
        eq = eq_tbl.createEquate(eq_name, value & 0xFFFFFFFFFFFFFFFFL)
    eq.addReference(a, 0)

    # create slot label
    existing = sym_tbl.getSymbols(a)
    names = [s.getName() for s in existing]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)

    # EOL comment
    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[EQ ] 0x%08x  %s  -> %s" % (slot_addr, eq_name, slot_label))

def _apply_ref(slot_addr, target_vaddr, gas_label, slot_label, eol):
    sa = _addr(slot_addr)
    ta = _addr(target_vaddr)
    sym_tbl = currentProgram.getSymbolTable()
    ref_mgr = currentProgram.getReferenceManager()

    if DRY:
        print("[dry] REF 0x%08x -> 0x%08x  %s  slot=%s" % (slot_addr, target_vaddr, gas_label, slot_label))
        return

    # create USER_DEFINED label at target if not already there
    tgt_syms = sym_tbl.getSymbols(ta)
    tgt_names = [s.getName() for s in tgt_syms]
    if gas_label not in tgt_names:
        sym_tbl.createLabel(ta, gas_label, SourceType.USER_DEFINED)

    # add DATA ref from slot to target
    ref_mgr.addMemoryReference(sa, ta, RefType.DATA, SourceType.USER_DEFINED, 0)
    # set primary
    for ref in ref_mgr.getReferencesFrom(sa):
        if ref.getToAddress().equals(ta):
            ref_mgr.setPrimary(ref, True)

    # create slot label
    s_syms = sym_tbl.getSymbols(sa)
    s_names = [s.getName() for s in s_syms]
    if slot_label not in s_names:
        sym_tbl.createLabel(sa, slot_label, SourceType.USER_DEFINED)

    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(sa)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[REF] 0x%08x -> 0x%08x  %s  slot=%s" % (slot_addr, target_vaddr, gas_label, slot_label))

def _apply_rename(slot_addr, slot_label, eol):
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()

    if DRY:
        print("[dry] RENAME 0x%08x -> %s" % (slot_addr, slot_label))
        return

    existing = sym_tbl.getSymbols(a)
    names = [s.getName() for s in existing]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)

    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[REN] 0x%08x -> %s" % (slot_addr, slot_label))

def _apply_plate_fix(func_addr, old_text, new_text):
    """Replace old_text with new_text in existing plate comment at func_addr."""
    a = _addr(func_addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[WARN] plate_fix 0x%08x: no code unit" % func_addr)
        return

    existing = cu.getComment(CodeUnit.PLATE_COMMENT)
    if existing is None:
        print("[WARN] plate_fix 0x%08x: no plate comment" % func_addr)
        return

    if old_text not in existing:
        print("[WARN] plate_fix 0x%08x: '%s' not found in plate" % (func_addr, old_text))
        return

    if DRY:
        print("[dry] PLATE_FIX 0x%08x: '%s' -> '%s'" % (func_addr, old_text, new_text))
        return

    new_plate = existing.replace(old_text, new_text)
    cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)
    print("[PFX] 0x%08x: '%s' -> '%s'" % (func_addr, old_text, new_text))

def _apply_cjk_plate(func_addr, new_plate_text):
    """Full plate rewrite (for CJK->ASCII conversion)."""
    a = _addr(func_addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[WARN] cjk_plate 0x%08x: no code unit" % func_addr)
        return

    if DRY:
        print("[dry] CJK_PLATE 0x%08x: rewrite to ASCII" % func_addr)
        return

    cu.setComment(CodeUnit.PLATE_COMMENT, new_plate_text)
    print("[PLT] 0x%08x: CJK plate replaced with ASCII" % func_addr)

def _apply_dword(slot_addr, expected_val, slot_label, eol):
    """Force DWord data type at slot_addr and set label + EOL."""
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()
    listing = currentProgram.getListing()

    if not _check(slot_addr, expected_val, slot_label):
        print("[SKIP] DWORD 0x%08x (%s) value mismatch" % (slot_addr, slot_label))
        return

    if DRY:
        print("[dry] DWORD 0x%08x  value=0x%08x  label=%s" % (slot_addr, expected_val, slot_label))
        return

    # Clear existing data at this address and re-define as DWord
    try:
        listing.clearCodeUnits(a, a.add(3), False)
    except Exception as e:
        print("[WARN] DWORD clearCodeUnits 0x%08x: %s" % (slot_addr, e))

    try:
        dt = DWordDataType.dataType
        listing.createData(a, dt)
    except Exception as e:
        print("[WARN] DWORD createData 0x%08x: %s" % (slot_addr, e))

    # Create label
    existing = sym_tbl.getSymbols(a)
    names = [s.getName() for s in existing]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)

    if eol:
        cu = listing.getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[DWD] 0x%08x  0x%08x  -> %s" % (slot_addr, expected_val, slot_label))

def _apply_eol_fix(addr, new_eol):
    """Replace EOL comment at addr with new pure-ASCII text."""
    a = _addr(addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[WARN] eol_fix 0x%08x: no code unit" % addr)
        return

    if DRY:
        print("[dry] EOL_FIX 0x%08x: -> '%s'" % (addr, new_eol))
        return

    cu.setComment(CodeUnit.EOL_COMMENT, new_eol)
    print("[EOL] 0x%08x: set '%s'" % (addr, new_eol))

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineSeg10Slots (DRY=%s) ===" % DRY)
    print("  Seg-10: 0x0801b850..0x0801cb00, 32 fn, vija/shuen scene tick")

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    eq_ok = 0
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        _apply_eq(slot_addr, value, eq_name, slot_label, eol)
        eq_ok += 1
    print("  EQ done: %d" % eq_ok)

    # B. REF_SLOTS
    print("\n--- B. REF_SLOTS (%d) ---" % len(REF_SLOTS))
    ref_ok = 0
    for entry in REF_SLOTS:
        slot_addr, target_vaddr, gas_label, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        _apply_ref(slot_addr, target_vaddr, gas_label, slot_label, eol)
        ref_ok += 1
    print("  REF done: %d" % ref_ok)

    # C. RENAME_SLOTS
    print("\n--- C. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    ren_ok = 0
    for entry in RENAME_SLOTS:
        slot_addr, slot_label = entry[0], entry[1]
        eol = entry[2] if len(entry) > 2 else None
        _apply_rename(slot_addr, slot_label, eol)
        ren_ok += 1
    print("  RENAME done: %d" % ren_ok)

    # D. PLATE_REWRITES (FUN_ substitutions + IO address fixes in existing plates)
    print("\n--- D. PLATE_REWRITES: FUN_/address fixes (%d) ---" % len(PLATE_REWRITES))
    for func_addr, old_text, new_text in PLATE_REWRITES:
        _apply_plate_fix(func_addr, old_text, new_text)

    # E. CJK plate full rewrites
    print("\n--- E. CJK_PLATE_REWRITES (%d) ---" % len(CJK_PLATE_REWRITES))
    for func_addr, new_plate in CJK_PLATE_REWRITES:
        _apply_cjk_plate(func_addr, new_plate)

    # G. DWORD_SLOTS (restore lost literal-pool labels)
    print("\n--- G. DWORD_SLOTS (%d) ---" % len(DWORD_SLOTS))
    for entry in DWORD_SLOTS:
        slot_addr, expected_val, slot_label = entry[0], entry[1], entry[2]
        eol = entry[3] if len(entry) > 3 else None
        _apply_dword(slot_addr, expected_val, slot_label, eol)

    # F. CJK EOL fixes
    print("\n--- F. CJK_EOL_FIXES (%d) ---" % len(CJK_EOL_FIXES))
    for addr, new_eol in CJK_EOL_FIXES:
        _apply_eol_fix(addr, new_eol)

    print("\n=== RefineSeg10Slots DONE ===")
    print("  EQ=%d  REF=%d  RENAME=%d  DWORD=%d  PLATE_FIX=%d  CJK_PLATE=%d  EOL_FIX=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(DWORD_SLOTS),
        len(PLATE_REWRITES), len(CJK_PLATE_REWRITES), len(CJK_EOL_FIXES)))

main()
