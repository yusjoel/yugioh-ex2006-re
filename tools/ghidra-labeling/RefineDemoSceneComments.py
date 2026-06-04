# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineDemoSceneComments.py — p5 batch-1 Sub-phase C (R5 注释订正)
#   (1) 过时 FUN_08013bd4 -> tick_demo_scene_state_machine (4 plate)
#   (2) Sub-phase A 改名后的 DAT_0801393c -> DEMO_EXTRA_RESOURCE_DESC (1 plate)
#   (3) caller 归属订正: reset_display(0x13510)+hub(0x13bd4) 的直接调用者仅 play_ui_effect_3a;
#       0x08014398(tick_prng_step_sequence) 实为 indirect_table (函数指针表成员, 非 direct bl)。
#   targeted 字符串替换, 逐条断言命中, 改完经 setPlateComment 写回 (重导出生效)。
# Usage: tools\asm-regen\ghidra-run-script.bat RefineDemoSceneComments.py [dry]

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry","--dry","1","true"): DRY = True
except Exception: pass

# addr -> [(old, new), ...]
REPL = {
    0x08013510: [
        (u"play_ui_effect_3a 及 FUN_08014398 在需要完全重置显示层时调用",
         u"play_ui_effect_3a (0x080bcbd4) 在需要完全重置显示层时调用 (直接调用者仅此一个; 其地址另登记于函数指针表, 可被间接分派)"),
    ],
    0x08013740: [(u"FUN_08013bd4", u"tick_demo_scene_state_machine")],
    0x0801379c: [(u"FUN_08013bd4", u"tick_demo_scene_state_machine")],
    0x08013864: [(u"FUN_08013bd4", u"tick_demo_scene_state_machine"),
                 (u"DAT_0801393c", u"DEMO_EXTRA_RESOURCE_DESC")],
    0x08013a68: [(u"FUN_08013bd4", u"tick_demo_scene_state_machine")],
    0x08013bd4: [
        (u"Called by FUN_08014398 and play_ui_effect_3a (0x080bcbd4); drives",
         u"Called by play_ui_effect_3a (0x080bcbd4) directly (its address also appears in a function-pointer table for indirect dispatch); drives"),
    ],
}

def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

def main():
    print("=== RefineDemoSceneComments (DRY=%s) ===" % DRY)
    listing = currentProgram.getListing()
    from ghidra.program.model.listing import CodeUnit
    nfix = 0
    for addr_int in sorted(REPL.keys()):
        a = _addr(addr_int)
        cu = listing.getCodeUnitAt(a)
        txt = cu.getComment(CodeUnit.PLATE_COMMENT) if cu else None
        if txt is None:
            print("[FAIL] no plate @ 0x%08x" % addr_int); continue
        new = txt
        ok = True
        for old, rep in REPL[addr_int]:
            if old not in new:
                print("[FAIL] 0x%08x: pattern not found: %r" % (addr_int, old[:40])); ok = False; continue
            new = new.replace(old, rep)
        if not ok:
            continue
        if new == txt:
            print("[skip] 0x%08x no change" % addr_int); continue
        if DRY:
            print("[dry]  0x%08x would update plate (%d repl)" % (addr_int, len(REPL[addr_int]))); nfix += 1; continue
        cu.setComment(CodeUnit.PLATE_COMMENT, new)
        print("[ok]   0x%08x plate updated" % addr_int); nfix += 1
    print("[done] %d plate(s) (DRY=%s)" % (nfix, DRY))

main()
