# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineDemoSceneBatch1LabelSwitch.py — p5 batch-1 R3 单一命名源
#   把 10 个 FS 资源指针从 data-equate (UPPER 常量) 切换为直接引用 data/demo-exodia-resources.s
#   的 GAS label (小写, 单一命名源):
#     (1) 在目标地址 (0x09e39xxx) createLabel = 导出脚本 label 名;
#     (2) 给代码槽 .word 加 DATA ref -> 目标 (resolve_word_symbol 据此导出 label);
#     (3) 删旧 data-equate (避免冗余/同名冲突)。
#   GAS 端 .word <label> 链接 data/demo-exodia-resources.s 定义 -> byte-identical。
# Usage: tools\asm-regen\ghidra-run-script.bat RefineDemoSceneBatch1LabelSwitch.py [dry]
from ghidra.program.model.symbol import SourceType, RefType

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry","--dry","1","true"): DRY = True
except Exception: pass

# (slot_addr, target_addr, gas_label, old_equate_name)
SWITCH = [
 (0x0801366c, 0x09e396b8, "demo_sprite_resource_desc",     "DEMO_SPRITE_RESOURCE_DESC"),
 (0x08013734, 0x09e396c8, "demo_sprite_alt_resource_desc", "DEMO_SPRITE_ALT_RESOURCE_DESC"),
 (0x08013988, 0x09e397d4, "demo_obj_resource_ptr_table",   "DEMO_OBJ_RESOURCE_PTR_TABLE"),
 (0x08013ab4, 0x09e397f4, "demo_cell_anim_assert_file",    "DEMO_CELL_ANIM_ASSERT_FILE"),
 (0x08013abc, 0x09e39808, "demo_cell_anim_assert_expr",    "DEMO_CELL_ANIM_ASSERT_EXPR"),
 (0x08013c98, 0x09e39844, "demo_path_exodia00_1_bg",       "PATH_DEMO_EXODIA00_1_BG"),
 (0x08013c9c, 0x09e39864, "demo_path_exodia00_2_bg",       "PATH_DEMO_EXODIA00_2_BG"),
 (0x08013fd4, 0x09e39884, "demo_path_exodia01_bg",         "PATH_DEMO_EXODIA01_BG"),
 (0x08013fd8, 0x09e398a4, "demo_path_exodia01",            "PATH_DEMO_EXODIA01"),
 (0x08014130, 0x09e398c0, "demo_path_exodia02",            "PATH_DEMO_EXODIA02"),
]

def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

def main():
    print("=== LabelSwitch (DRY=%s) n=%d ===" % (DRY, len(SWITCH)))
    et = currentProgram.getEquateTable()
    rm = currentProgram.getReferenceManager()
    n=0
    for slot_int, tgt_int, label, oldeq in SWITCH:
        slot=_addr(slot_int); tgt=_addr(tgt_int)
        d=getDataAt(slot)
        if d is None or d.getLength()!=4:
            print("[FAIL] no 4B data @ slot 0x%08x"%slot_int); continue
        if DRY:
            print("[dry] slot 0x%08x .word 0x%08x -> label %s (del eq %s)"%(slot_int,tgt_int,label,oldeq)); n+=1; continue
        # 1. 目标 label
        createLabel(tgt, label, True, SourceType.USER_DEFINED)
        # 2. 代码槽 DATA ref -> 目标 (primary)
        ref = rm.addMemoryReference(slot, tgt, RefType.DATA, SourceType.USER_DEFINED, 0)
        rm.setPrimary(ref, True)
        # 3. 删旧 equate
        eq = et.getEquate(oldeq)
        if eq is not None:
            try: eq.removeReference(slot, 0)
            except Exception as e: print("  [warn] removeReference %s: %s"%(oldeq,e))
            try:
                if eq.getReferenceCount()==0: et.removeEquate(oldeq)
            except Exception: pass
        print("[ok] 0x%08x -> %s"%(slot_int,label)); n+=1
    print("[done] %d (DRY=%s)"%(n,DRY))

main()
