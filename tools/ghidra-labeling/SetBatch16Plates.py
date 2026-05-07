# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
from ghidra.program.model.symbol import SourceType
from ghidra.program.model.listing import CodeUnit

PLATES = [
    ("0801b91c", "load_shuen_sprite_gfx_guarded",
        "demo_shuen scene sprite GFX load dispatcher (guarded). "
        "Called twice by demo_shuen_state_machine (0x0801bd08) in caseD_0 (INIT step). "
        "r0=u8 skip_flag: if r0==0, shifts params (r1->r0, r2->r1, r3->r2, [sp+0xc]->r3, [sp+0x8]->stack) "
        "then calls load_demo_shuen_sprite_gfx; if r0!=0, skips. "
        "Both actual callsites pass r0=0 so the load path always executes. "
        "Params: r0=skip_flag {0=load, non-0=skip}, r1=tile_param_low [0..1], r2=tile_param_high [0..2], "
        "r3=sprite_config [1..2], [sp+0x8]=5th param, [sp+0xc]=6th param. "
        "Returns void (tail-call via pop {r0}; bx r0). "
        "Side-effects: OAM attr bytes [r8+0..35] zeroed then attr0/1/2 written; apply_gfx_resource_list triggered. "
        "Constants: none (all magic handled by callee)."),
    ("0801b93c", "load_shuen_bg1_gfx_set",
        "demo_shuen scene BG1 GFX resource loader. "
        "Called by demo_shuen_state_machine (0x0801bd08) caseD_0 with r0=0x09e3cfe8. "
        "Flow: (1) fs_load(r0, 0) decompresses shuen_bg1.LZ5bg; "
        "(2) zero_struct_36bytes clears first GFX descriptor; configures OAM attr bytes "
        "(attr0+0x14 bits[3:0]=0, attr2+0x18 bits[14:7] cleared via mask 0xffffc07f, priority=3); "
        "first apply_gfx_resource_list writes BG1 resource; "
        "(3) zero_struct_36bytes clears second descriptor; attr bits[3:0]=3, [+0x18]=0xa00 OBJ tile offset; "
        "second apply_gfx_resource_list; (4) strh to DISPCNT (0x04000000) enables display. "
        "Symmetric with load_demo_bg_gfx_set0 (0x0801379c). "
        "Param: r0=ptr file_path (ROM addr -> 'demo/shuen/shuen_bg1.LZ5bg'). Returns void. "
        "Constants: BG1_GFX_RESOURCE=0x09e3cfe8, OAM_PRIORITY_MASK=0xffffc07f, "
        "PRIORITY_3=0x3, OBJ_TILE_OFFSET=0xa0<<4, DISPCNT=0x04000000."),
    ("0801ba04", "load_shuen_obj_resource_by_slot",
        "demo_shuen scene OBJ GFX resource loader by slot index. "
        "Called by load_shuen_obj_resource_slot0 (0x0801ba4c) with r0=0. "
        "Symmetric with load_demo_obj_resource_by_slot (0x08013940): "
        "(1) copies 4 words from ROM resource table 0x09e3cf60 (ldmia+str) to stack struct; "
        "(2) builds load_g2d_obj_resource_set param struct; "
        "(3) lsls r0,r0,#4 multiplies slot_index by 16; (4) calls load_g2d_obj_resource_set. "
        "Param: r0=u32 slot_index [0..0]. Returns void. "
        "Side-effects: gDemoState anim ctrl + ImageProxy initialized; "
        "OBJ Tile VRAM + OBJ Palette VRAM written. "
        "Constants: GDEMOSTATE=0x02029ec0, SHUEN_OBJ_RESOURCE_TABLE=0x09e3cf60, "
        "OBJ_RESOURCE_STRIDE=0x10, VRAM_FLAGS=0x200."),
    ("0801ba4c", "load_shuen_obj_resource_slot0",
        "demo_shuen scene OBJ GFX resource slot0 fixed-param stub. "
        "Symmetric with load_demo_obj_resource_slot0 (0x0801398c): "
        "passes r0=0 to load_shuen_obj_resource_by_slot, then returns fixed r0=1. "
        "Called by play_demo_shuen (0x080bc880) and FUN_0801c254 (0x0801c254). "
        "Entry scan (5 instrs): push {lr} / movs r0,#0 / bl FUN_0801ba04 / movs r0,#1 / pop {r1}. "
        "r0 at entry clobbered -> no input parameter. "
        "Returns r0=u32 1 (load success/busy). "
        "Side-effects via load_shuen_obj_resource_by_slot(0): "
        "OBJ Tile VRAM + OBJ Palette VRAM written; gDemoState anim ctrl + ImageProxy initialized."),
    ("0801ba5c", "write_shuen_bg3_scroll_regs",
        "demo_shuen scene BG3 scroll register writer. "
        "Identical structure to write_bg3_scroll_regs (0x0801399c): "
        "r0=u16 hofs [0..511], r1=u16 vofs [0..511]; each ANDed with 0x1FF (9-bit mask), "
        "then strh written to BG3HOFS (0x04000018) and BG3VOFS (0x0400001e). "
        "Callers: tick_demo_shuen_bg3_hscroll (0x0801ba78) passes r0=0, r1=hofs; "
        "FUN_0801bad0 passes r0=vofs, r1=0. Leaf function (bx lr). "
        "Side-effects: [BG3HOFS 0x04000018] := r0 & 0x1FF; [BG3VOFS 0x0400001e] := r1 & 0x1FF. "
        "Constants: BG3_SCROLL_MASK=0x1FF, BG3HOFS=0x04000018, BG3VOFS=0x0400001e."),
    ("0801ba78", "tick_demo_shuen_bg3_hscroll",
        "Per-frame BG3 horizontal scroll updater for demo_shuen scene. "
        "Called by demo_shuen_state_machine (0x0801bd08) each frame. "
        "Reads gDemoState+0x8C bits[23:16] (8-bit scroll counter), computes hofs = counter % 0xA0, "
        "updates counter bits[8:1] (+= 2, wraps at 256), re-wraps if > 0xA0, "
        "writes back, then calls write_shuen_bg3_scroll_regs(0, new_hofs). "
        "Symmetric with tick_demo_bg3_hscroll (0x080139b8). "
        "No input params (r0 clobbered by ldr at entry). Returns void. "
        "Side-effects: [gDemoState+0x8C] bits[8:1] updated; [BG3HOFS 0x04000018] written. "
        "Constants: SCREEN_WIDTH=0xA0, COUNTER_MASK=0xFF, STEP=2."),
    ("0801bb28", "advance_shuen_cell_anim_frame",
        "Per-sprite demo cell animation frame advance for shuen scene (Shuen/SHU_main.c). "
        "Called by tick_shuen_anim_slots_batch (0x0801bbd4). "
        "r0=u8 anm_id [0..10], r1=s32 playback_step (-1=auto advance, >=0=explicit seq step), "
        "r2=s32 screen_x_fp12, r3=s32 screen_y_fp12. "
        "Validates anm_id via read_obj_id_field; out-of-range triggers suppress_assert_report "
        "(assert: anmID < IG2D_GetAnmSequencesCount, file=Shuen/SHU_main.c, line=0xEF). "
        "playback_step==-1: dispatch_cell_anim_frame_advance then dispatch_cell_anim_sequence_step; "
        "playback_step>=0: dispatch_cell_anim_sequence_step with r6 low 16 bits. "
        "Finally dispatch_isd_cell_anim_oam_setup commits OAM. Returns void. "
        "Side-effects: [gDemoState+0x8+anm_id*4] advanced; OAM attr0/1/2 + XY written. "
        "Constants: STEP_AUTO=-1, DEFAULT_STEP=1, FAST_STEP=2, SEQ_RANGE_MAX=0xA."),
    ("0801bbd4", "tick_shuen_anim_slots_batch",
        "Per-frame batch OBJ animation slot updater for demo_shuen scene. "
        "Called by demo_shuen_state_machine (0x0801bd08) each frame. "
        "r0=u32 total_count [0..209]: divided by 11 to get valid slot ceiling. "
        "Copies 40-byte ROM coord table (0x09e3cfbf, 20 pairs) to stack via memcpy. "
        "Loops slot r5 from 0 to min(total_count/11, 19), calls "
        "advance_shuen_cell_anim_frame(slot=r5, step=-1, x=table[r5*2], y=table[r5*2+1]). "
        "Returns void. "
        "Side-effects: OBJ VRAM/OAM updated for all active sprite slots. "
        "Constants: MAX_SLOTS=0x13, GROUP_SIZE=0xB, COORD_TABLE=0x09e3cfbf."),
    ("0801c2ac", "reset_gl_display_state",
        "Full GL display state reset called at scene transitions. "
        "Called by FUN_0801cf74, FUN_0801cfcc, and play_ui_effect_3b (0x080bc918). "
        "No input params (r0 clobbered at entry). Returns r0=1 (success). "
        "Sequence: (1) bios_cpu_set fill-zero EWRAM 0x02029eb0 192 bytes; "
        "(2) gl_clear_vram_palram_scroll; "
        "(3) DISPCNT(0x04000000)=0x1741, BG0CNT(0x04000008)=0x1D81, "
        "BG1CNT(0x0400000A)=0x1E82, BG2CNT(0x0400000C)=0x1F8B; "
        "(4) gl_set_brightness(0x3F,-16); (5) gl_state_init; (6) gl_clear_frame_callbacks. "
        "Side-effects: EWRAM cleared; IO regs written; GL state/callbacks reset. "
        "Constants: DISPCNT_VAL=0x1741, BG0CNT_VAL=0x1D81, BG1CNT_VAL=0x1E82, "
        "BG2CNT_VAL=0x1F8B, ZERO_FILL_CTRL=0x05000030."),
    ("0801c310", "load_vija_bg_gfx_embedded",
        "vija scene BG GFX loader - embedded ROM data variant. "
        "Called by load_vija_bg_gfx_by_mode (0x0801c484) when r0==0. "
        "Copies 16-byte BG resource header from 0x09e3d834 to stack (ldmia+str x4); "
        "memcpy 8-byte BG params from 0x09e3d844. "
        "Configures OAM: [r1+0x14] bits[3:0]=tile_shape, [r1+0x17] bit6=priority(0x40), "
        "[r1+0x18] bits[6:0]=tile_base_idx, bits[14:7]=palette_bank<<7. "
        "Calls apply_gfx_resource_list -> BG tile+palette VRAM write. "
        "Params: r0=u8 tile_group_index [0..12], r1=ptr oam_entry, "
        "r2=u8 tile_shape [0..15], r3=u8 tile_base_idx [0..127], [sp+0]=palette_bank [0..127]. "
        "Returns void. "
        "Constants: VIJA_STATE=0x02029eb0, VIJA_BG_RES_HEADER=0x09e3d834, "
        "VIJA_BG_PARAMS=0x09e3d844, OAM_PRIORITY_BIT=0x40, OAM_TILE_MASK=0xffffc07f."),
    ("0801c3f4", "load_vija_bg_gfx_from_fs",
        "vija scene BG GFX loader - file system variant. "
        "Called by load_vija_bg_gfx_by_mode (0x0801c484) when r0==1. "
        "Non-APCS input: r8=ptr oam_entry (entry .hword 0x4668 = mov r0,r8). "
        "zero_struct_36bytes(r8) clears OAM buffer; fs_load(0x09e3d84c, 0) loads vija BG/OBJ files. "
        "OAM attr: [r1+0x14] bits[3:0]=tile_shape, [r1+0x17] bits[5:0]=0 (clear priority+flip), "
        "[r1+0x18] tile_base_idx + palette_bank<<7, [r1+0x1b] bit2=1 (OBJ enable). "
        "apply_gfx_resource_list writes VRAM. "
        "Params: r8=ptr oam_entry (non-APCS), r2=tile_shape [0..15], "
        "r3=tile_base_idx [0..127], [sp+0x34]=palette_bank [0..127]. Returns void. "
        "Constants: VIJA_FS_PATH_LIST=0x09e3d84c, OAM_TILE_MASK=0xffffc07f, OBJ_ENABLE=0x4."),
    ("0801c484", "load_vija_bg_gfx_by_mode",
        "vija scene BG GFX load dispatcher by mode. "
        "Called by tick_bg_scroll_anim_frame (0x0801c6b0) and FUN_0801cb00. "
        "r0=u8 load_mode: 0=load_vija_bg_gfx_embedded, 1=load_vija_bg_gfx_from_fs, other=no-op. "
        "Forwards r1..r3 and two stack params unchanged. No direct VRAM side-effects. "
        "Params: r0=load_mode, r1=tile_group_index [0..3], r2=ptr oam_entry, "
        "r3=tile_base_idx [0..127], [sp+0x10]=palette_bank, [sp+0x14]=extra_param. "
        "Returns void."),
    ("0801c4c0", "load_vija_obj_resource_by_region",
        "vija scene OBJ resource loader selected by JP/US region variant. "
        "Called by load_vija_obj_resource_gated (0x0801c50c). "
        "r0=u8 use_us_variant [0..1]: 0=JP wija_obj_all, 1=US wija_obj_allUS. "
        "Copies 8 pointers from ROM table 0x09e3d964 (JP 4 + US 4) to stack. "
        "lsls r0,r0,#4 (stride=16) selects resource group ptr on stack. "
        "Calls load_g2d_obj_resource_set(VIJA_STATE, +4, +8, 0). Returns void. "
        "Constants: VIJA_STATE=0x02029eb0, VIJA_OBJ_RES_TABLE=0x09e3d964, "
        "OBJ_RESOURCE_STRIDE=0x10, OBJ_VRAM_FLAGS=0x200."),
    ("0801c50c", "load_vija_obj_resource_gated",
        "vija scene OBJ resource load entry with JP/US region gate. "
        "Called by FUN_0801cf74, FUN_0801cfcc, and play_ui_effect_3b (0x080bc918). "
        "No input params. Returns r0=1 (always). "
        "ROM header 0x080000ae u16 high byte: != 0x4a ('J') -> use_us_variant=1. "
        "If JP: [0x02006c2c] bits[2:0] != 0 -> use_us_variant=1. "
        "Calls load_vija_obj_resource_by_region(use_us_variant). "
        "Constants: ROM_REGION_CODE_ADDR=0x080000ae, REGION_CODE_JP=0x4a, "
        "REGION_FLAGS_OFFSET=0x6c2c, REGION_FLAGS_MASK=0x7."),
    ("0801c5d8", "drive_vija_obj_cell_anim",
        "vija scene NNS G2D CellAnimation driver (Vija/VIJ_main.c). "
        "Called by update_dual_cell_anim_oam_pos (0x0801c74c) and FUN_0801c794. "
        "r0=u8 obj_slot_idx [0..N-1]: read_obj_id_field validates; "
        "out-of-range -> suppress_assert_report (Vija/VIJ_main.c line=0xf2). "
        "r1=s16 anim_cmd: -2=OAM pos refresh only, -1=frame advance (rate 0x1000), >=0=seq step. "
        "r2=s16 x_pos, r3=s16 y_pos (lsls #0xc -> fp12). "
        "All paths end: dispatch_isd_cell_anim_oam_setup. Returns void. "
        "Side-effects: OAM updated; CellAnim state advanced. "
        "Constants: VIJA_STATE=0x02029eb0, ANIM_CMD_NO_UPDATE=-2, "
        "ANIM_CMD_FRAME_ADVANCE=-1, FRAME_ADVANCE_RATE=0x1000."),
    ("0801c668", "apply_bg2_affine_fixed_angle",
        "Apply BG2 rotation+scale affine transform at fixed scale with given angle. "
        "Called by tick_bg2_affine_anim_frame (0x0801c694). "
        "r0=u8 angle [0..255] (256 steps/revolution). "
        "Builds param block: bg_index=2, scale_x=0x40, scale_y=0x40 (1:1), "
        "pivot_x=0x40-0x78+0x28=-0x10. "
        "Calls apply_bg_affine_by_angle_scale (0x08015868). Returns void. "
        "Side-effects: BG2PA(0x04000020), BG2PB(0x04000022), BG2PC(0x04000024), "
        "BG2PD(0x04000026), BG2X(0x04000028), BG2Y(0x0400002c) written."),
    ("0801c694", "tick_bg2_affine_anim_frame",
        "Per-frame BG2 affine rotation tick for play_ui_effect_3b scene. "
        "Called by FUN_0801cb00 each frame. No input params. "
        "Reads IWRAM 0x02029eb0+0x90 frame counter byte, increments (u8 wrap), "
        "zero-extends old value -> angle, calls apply_bg2_affine_fixed_angle(angle). "
        "Returns void. "
        "Side-effects: [0x02029eb0+0x90] incremented; BG2 affine regs written via callee."),
    ("0801c6b0", "tick_bg_scroll_anim_frame",
        "Per-frame BG scroll and tile animation tick for play_ui_effect_3b scene. "
        "Called by FUN_0801cb00 each frame. r0=u32 tick_count. "
        "Updates only when tick_count mod 13 == 0. "
        "On trigger: memcpy 4-byte ROM params from 0x09e3d9cf; "
        "increments [0x02029eb0+0x91] AND 0x3 (4-frame cycle); "
        "calls load_vija_bg_gfx_by_mode(mode=0); writes BG0VOFS(0x04000012)=4. "
        "Returns void. "
        "Constants: MOD_PERIOD=13, SUB_FRAME_MASK=0x3, BG0VOFS=0x04000012."),
    ("0801c728", "advance_scene_phase_counter",
        "Scene internal 2-level phase counter advance. "
        "Called by FUN_0801c794; return value used for dispatch. "
        "r0=void* pSceneState: byte[2]=phase tick [0..7], byte[3]=phase index [0..3]. "
        "If byte[2]==7: byte[3]=(byte[3]+1)&0x3, byte[2]=0. Else: byte[2]++. "
        "Returns r0=u8 phase_index [0..3]. Leaf function. "
        "Side-effects: [r0+2] and [r0+3] updated."),
    ("0801c74c", "update_dual_cell_anim_oam_pos",
        "Update two ISD cell animation OAM entries simultaneously. "
        "Called by FUN_0801c794 (play_ui_effect_3b state machine). "
        "r0=u8 base_obj_index [0..7], r1=s16 sequence_idx [0..4], "
        "r2=s16 x_pos_px, r3=s16 y_pos_px. "
        "x -= 0x10, y -= 0x10 (center anchor). "
        "Calls drive_vija_obj_cell_anim(obj_index=2, seq_idx, x, y), "
        "then drive_vija_obj_cell_anim(obj_index=r0+3, seq_idx, x, y). "
        "[sp+0]=0, [sp+4]=0 for both. Returns void. "
        "Side-effects: OAM slots [2] and [r0+3] updated via dispatch_isd_cell_anim_oam_setup."),
]

listing = currentProgram.getListing()
ok = 0
for addr_str, func_name, plate_text in PLATES:
    addr = currentProgram.getAddressFactory().getAddress("0x0" + addr_str)
    func = getFunctionAt(addr)
    if func is None:
        print("[no_func] 0x%s %s" % (addr_str, func_name))
        continue
    cu = listing.getCodeUnitAt(func.getEntryPoint())
    if cu is None:
        print("[no_cu] 0x%s %s" % (addr_str, func_name))
        continue
    try:
        if isinstance(plate_text, str):
            plate_u = plate_text.decode("utf-8")
        else:
            plate_u = plate_text
        cu.setComment(CodeUnit.PLATE_COMMENT, plate_u)
        print("[ok] 0x%s %s" % (addr_str, func_name))
        ok += 1
    except Exception as e:
        print("[error] 0x%s %s: %s" % (addr_str, func_name, e))

print("[done] plate comments set: %d/%d" % (ok, len(PLATES)))
