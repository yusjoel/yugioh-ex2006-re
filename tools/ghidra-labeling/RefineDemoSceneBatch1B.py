# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineDemoSceneBatch1B.py — p5 batch-1 Sub-phase B (R3 指针)
#   (1) 10 个 FS 资源区指针 (0x09e39xxx, 导出范围外) 经 data-equate 符号化 + 槽改名
#   (2) 15 个已符号化的指针槽 (gDemoState x8 + IO 寄存器 x7) 仅改槽标签
#   (3) cell_anim plate R5: 断言文件名 IG2D_Main.c -> Exodia/EXO_main.c (经 ROM 字节核实)
# Usage: tools\asm-regen\ghidra-run-script.bat RefineDemoSceneBatch1B.py [dry]
from ghidra.program.model.symbol import SourceType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry","--dry","1","true"): DRY = True
except Exception: pass

# (addr, value, const_name, slot_label) — data-equate + 改名
DATA_EQUATES = [
 (0x0801366c, 0x09e396b8, "DEMO_SPRITE_RESOURCE_DESC",     "setup_demo_sprite_entry_demo_sprite_resource_desc"),
 (0x08013734, 0x09e396c8, "DEMO_SPRITE_ALT_RESOURCE_DESC", "setup_demo_sprite_entry_alt_demo_sprite_alt_resource_desc"),
 (0x08013988, 0x09e397d4, "DEMO_OBJ_RESOURCE_PTR_TABLE",   "load_demo_obj_resource_by_slot_demo_obj_resource_ptr_table"),
 (0x08013ab4, 0x09e397f4, "DEMO_CELL_ANIM_ASSERT_FILE",    "setup_demo_cell_anim_slot_demo_cell_anim_assert_file"),
 (0x08013abc, 0x09e39808, "DEMO_CELL_ANIM_ASSERT_EXPR",    "setup_demo_cell_anim_slot_demo_cell_anim_assert_expr"),
 (0x08013c98, 0x09e39844, "PATH_DEMO_EXODIA00_1_BG",       "tick_demo_scene_state_machine_path_demo_exodia00_1_bg"),
 (0x08013c9c, 0x09e39864, "PATH_DEMO_EXODIA00_2_BG",       "tick_demo_scene_state_machine_path_demo_exodia00_2_bg"),
 (0x08013fd4, 0x09e39884, "PATH_DEMO_EXODIA01_BG",         "tick_demo_scene_state_machine_path_demo_exodia01_bg"),
 (0x08013fd8, 0x09e398a4, "PATH_DEMO_EXODIA01",            "tick_demo_scene_state_machine_path_demo_exodia01"),
 (0x08014130, 0x09e398c0, "PATH_DEMO_EXODIA02",            "tick_demo_scene_state_machine_path_demo_exodia02"),
]

# (addr, slot_label) — 仅改槽标签 (值已由现有 ref 符号化)
LABEL_ONLY = [
 (0x08013564, "reset_display_and_gl_state_ptr_gdemostate"),
 (0x08013668, "setup_demo_sprite_entry_ptr_gdemostate"),
 (0x08013738, "setup_demo_sprite_entry_alt_ptr_gdemostate"),
 (0x08013984, "load_demo_obj_resource_by_slot_ptr_gdemostate"),
 (0x08013a08, "tick_demo_bg3_hscroll_ptr_gdemostate"),
 (0x08013a60, "tick_demo_bg3_vscroll_ptr_gdemostate"),
 (0x08013ab0, "setup_demo_cell_anim_slot_ptr_gdemostate"),
 (0x08013bfc, "tick_demo_scene_state_machine_ptr_gdemostate"),
 (0x080139b0, "write_bg3_scroll_regs_ptr_bg3hofs"),
 (0x080139b4, "write_bg3_scroll_regs_ptr_bg3vofs"),
 (0x08013b74, "apply_demo_window_fade_in_step_ptr_winin"),
 (0x08013b78, "apply_demo_window_fade_in_step_ptr_winout"),
 (0x08013b80, "apply_demo_window_fade_in_step_ptr_win0v"),
 (0x08013bd0, "apply_demo_window_fade_out_step_ptr_win0v"),
 (0x08013fcc, "tick_demo_scene_state_machine_ptr_bg3cnt"),
]

PLATE_FIX = (0x08013a68,
    u"IG2D_Main.c:0x14b=331",
    u"Exodia/EXO_main.c:331; assert: anmID < IG2D_GetAnmSequencesCount")

def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

def main():
    print("=== RefineDemoSceneBatch1B (DRY=%s) ===" % DRY)
    et = currentProgram.getEquateTable()
    listing = currentProgram.getListing()
    nde=nlo=0
    # data-equates
    for addr_int, value, cname, label in DATA_EQUATES:
        a=_addr(addr_int); d=getDataAt(a)
        if d is None or d.getLength()!=4:
            print("[FAIL] no 4B data @ 0x%08x"%addr_int); continue
        try:
            dv=d.getValue(); iv=(int(dv.getValue())&0xffffffff) if hasattr(dv,"getValue") else (int(dv)&0xffffffff)
        except Exception: iv=None
        if iv is not None and iv!=(value&0xffffffff):
            print("[FAIL] val mismatch @ 0x%08x data=0x%x decl=0x%x"%(addr_int,iv,value)); continue
        if DRY:
            print("[dry] DE 0x%08x -> %s / %s=0x%x"%(addr_int,label,cname,value)); nde+=1; continue
        createLabel(a,label,True,SourceType.USER_DEFINED)
        eq=et.getEquate(cname)
        if eq is None: eq=et.createEquate(cname,value)
        eq.addReference(a,0); nde+=1
        print("[ok] DE 0x%08x %s"%(addr_int,cname))
    # label-only
    for addr_int,label in LABEL_ONLY:
        a=_addr(addr_int)
        if DRY:
            print("[dry] LO 0x%08x -> %s"%(addr_int,label)); nlo+=1; continue
        createLabel(a,label,True,SourceType.USER_DEFINED); nlo+=1
        print("[ok] LO 0x%08x %s"%(addr_int,label))
    # plate fix
    pa,old,new=PLATE_FIX
    cu=listing.getCodeUnitAt(_addr(pa))
    txt=cu.getComment(CodeUnit.PLATE_COMMENT) if cu else None
    if txt and old in txt:
        if DRY: print("[dry] plate 0x%08x fix"%pa)
        else: cu.setComment(CodeUnit.PLATE_COMMENT, txt.replace(old,new)); print("[ok] plate 0x%08x fixed"%pa)
    else:
        print("[FAIL] plate pattern not found @ 0x%08x"%pa)
    print("[done] DE=%d LO=%d (DRY=%s)"%(nde,nlo,DRY))

main()
