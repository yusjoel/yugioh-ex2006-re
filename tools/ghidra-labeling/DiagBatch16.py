# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
from ghidra.program.model.symbol import SourceType
from ghidra.program.model.listing import CodeUnit

# Check and rename batch16 functions by address
addrs_and_names = [
    ("0801b91c", "load_shuen_sprite_gfx_guarded"),
    ("0801b93c", "load_shuen_bg1_gfx_set"),
    ("0801ba04", "load_shuen_obj_resource_by_slot"),
    ("0801ba4c", "load_shuen_obj_resource_slot0"),
    ("0801ba5c", "write_shuen_bg3_scroll_regs"),
    ("0801ba78", "tick_demo_shuen_bg3_hscroll"),
    ("0801bb28", "advance_shuen_cell_anim_frame"),
    ("0801bbd4", "tick_shuen_anim_slots_batch"),
    ("0801c2ac", "reset_gl_display_state"),
    ("0801c310", "load_vija_bg_gfx_embedded"),
    ("0801c3f4", "load_vija_bg_gfx_from_fs"),
    ("0801c484", "load_vija_bg_gfx_by_mode"),
    ("0801c4c0", "load_vija_obj_resource_by_region"),
    ("0801c50c", "load_vija_obj_resource_gated"),
    ("0801c5d8", "drive_vija_obj_cell_anim"),
    ("0801c668", "apply_bg2_affine_fixed_angle"),
    ("0801c694", "tick_bg2_affine_anim_frame"),
    ("0801c6b0", "tick_bg_scroll_anim_frame"),
    ("0801c728", "advance_scene_phase_counter"),
    ("0801c74c", "update_dual_cell_anim_oam_pos"),
]

renamed = 0
already = 0
for addr_str, new_name in addrs_and_names:
    addr = currentProgram.getAddressFactory().getAddress("0x0" + addr_str)
    func = getFunctionAt(addr)
    if func is None:
        print("[no_func] 0x%s" % addr_str)
        continue
    current_name = func.getName()
    if current_name == new_name:
        print("[already] 0x%s -> %s" % (addr_str, new_name))
        already += 1
        continue
    print("[current] 0x%s = %s" % (addr_str, current_name))
    # Rename via function symbol
    func_sym = func.getSymbol()
    if func_sym is not None:
        try:
            func_sym.setName(new_name, SourceType.USER_DEFINED)
            print("[ok] 0x%s: %s -> %s" % (addr_str, current_name, new_name))
            renamed += 1
        except Exception as e:
            print("[error] 0x%s rename: %s" % (addr_str, e))
    else:
        print("[no_sym] 0x%s" % addr_str)

print("[done] already=%d renamed=%d" % (already, renamed))
