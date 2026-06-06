# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineGlBlendBatch2.py — p5 batch-2 (GL blend/brightness 簇 0x14600..0x14a10, 12 fn)
#   R2/R3: gGlBlendState(0x02023480) USER label + 8 槽 DATA ref + 槽改名 <func>_ptr_gl_blend_state
#   R1   : data-equate 4 常量 (GL_CLEAR_BITS_9_2 / _17_10 / GL_CLEAR_VRAM/PALRAM_FILL_CTRL)
#          经 ExportRangeToGas.resolve_word_equate 导出符号; constants/gl_blend.inc .equ 解析回值
#   R2   : assert-line 槽 (0x148bc=281) 改名
#   R5   : 1 plate 全改 (0x1469c 函数改名) + 6 plate targeted 修正 (gDemoState->gGlBlendState 等)
#   rename: 0x0801469c clear_demo_sprite_enable_bits -> reset_gl_blend_transition_state
#           (batch-1 误名: 实复位 gGlBlendState 而非 demo sprite)
# Usage: tools\asm-regen\ghidra-run-script.bat RefineGlBlendBatch2.py [dry]
from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"): DRY = True
except Exception:
    pass

GL_BLEND_STATE = 0x02023480

# --- A. gGlBlendState 指针槽 (slot_addr, slot_label) ---
PTR_SLOTS = [
 (0x080146c0, 'clear_demo_sprite_enable_bits_ptr_gl_blend_state'),   # 函数将改名, 但 setName 在标签创建后; 槽名用旧前缀避免歧义? -> 用新前缀
 (0x080146ec, 'update_brightness_fade_flag_ptr_gl_blend_state'),
 (0x08014740, 'gl_set_brightness_ptr_gl_blend_state'),
 (0x080147c0, 'init_blend_transition_params_ptr_gl_blend_state'),
 (0x08014824, 'gl_set_blend2_level_ptr_gl_blend_state'),
 (0x080148b4, 'init_blend_transition_params_ex_ptr_gl_blend_state'),
 (0x0801490c, 'check_blend_transition_done_ptr_gl_blend_state'),
 (0x08014954, 'tick_blend_transition_step_ptr_gl_blend_state'),
]
# 注: 0x146c0 槽属将被改名的函数; 槽前缀用 reset_gl_blend_transition_state_ 与新函数名一致
PTR_SLOTS[0] = (0x080146c0, 'reset_gl_blend_transition_state_ptr_gl_blend_state')

# --- B. data-equate 常量 (slot_addr, value, const_name, slot_label) ---
EQ_SLOTS = [
 (0x080146c4, 0xfffffc03, 'GL_CLEAR_BITS_9_2',   'reset_gl_blend_transition_state_gl_clear_bits_9_2'),
 (0x0801474c, 0xfffffc03, 'GL_CLEAR_BITS_9_2',   'gl_set_brightness_gl_clear_bits_9_2'),
 (0x080147d0, 0xfffffc03, 'GL_CLEAR_BITS_9_2',   'init_blend_transition_params_gl_clear_bits_9_2'),
 (0x08014830, 0xfffffc03, 'GL_CLEAR_BITS_9_2',   'gl_set_blend2_level_gl_clear_bits_9_2'),
 (0x080148c8, 0xfffffc03, 'GL_CLEAR_BITS_9_2',   'init_blend_transition_params_ex_gl_clear_bits_9_2'),
 (0x08014958, 0xfffffc03, 'GL_CLEAR_BITS_9_2',   'tick_blend_transition_step_gl_clear_bits_9_2'),
 (0x080146c8, 0xfffc03ff, 'GL_CLEAR_BITS_17_10', 'reset_gl_blend_transition_state_gl_clear_bits_17_10'),
 (0x08014750, 0xfffc03ff, 'GL_CLEAR_BITS_17_10', 'gl_set_brightness_gl_clear_bits_17_10'),
 (0x080147d4, 0xfffc03ff, 'GL_CLEAR_BITS_17_10', 'init_blend_transition_params_gl_clear_bits_17_10'),
 (0x08014834, 0xfffc03ff, 'GL_CLEAR_BITS_17_10', 'gl_set_blend2_level_gl_clear_bits_17_10'),
 (0x080148cc, 0xfffc03ff, 'GL_CLEAR_BITS_17_10', 'init_blend_transition_params_ex_gl_clear_bits_17_10'),
 (0x08014690, 0x01006000, 'GL_CLEAR_VRAM_FILL_CTRL',   'gl_clear_vram_palram_scroll_gl_clear_vram_fill_ctrl'),
 (0x08014694, 0x01000100, 'GL_CLEAR_PALRAM_FILL_CTRL', 'gl_clear_vram_palram_scroll_gl_clear_palram_fill_ctrl'),
]

# --- C. 其它槽改名 (无 equate, 仅 R2 改名) ---
RENAME_ONLY = [
 (0x080148bc, 'init_blend_transition_params_ex_assert_line_blend1'),  # .word 0x119=281 (GL_Common.c 行号)
]

# --- D. 函数改名 ---
FUNC_RENAME = [
 (0x0801469c, 'reset_gl_blend_transition_state'),
]

# --- E. plate 全替换 ---
PLATE_FULL = {
 0x0801469c: (
  u"由 tick_demo_scene_state_machine (0x08013bd4) caseD_4 在 blend 完成检测后调用, "
  u"复位 gGlBlendState (0x02023480) 的 +0x8 打包控制字: "
  u"(1) ldrb/strb 清 bits[1:0] (active/fade 标志, AND 0xfc); "
  u"(2) ldrh/strh 清 bits[9:2] (blend1 step, GL_CLEAR_BITS_9_2); "
  u"(3) ldr/str 清 bits[17:10] (blend2 step, GL_CLEAR_BITS_17_10) 后置 bit10 (0x400). "
  u"无参 (void); 叶子函数. 副作用: [gGlBlendState+0x8] 字节/半字/字写入."
 ),
}

# --- E. plate targeted 替换 (addr -> [(old, new), ...]) ---
PLATE_REPL = {
 0x080146cc: [
  (u"亮度状态结构体 (EWRAM 0x02023480)", u"gGlBlendState 亮度状态结构体 (0x02023480)"),
  (u"副作用: [0x02023480+8]", u"副作用: [gGlBlendState+8]"),
 ],
 0x08014754: [
  (u"Initializes gDemoState blend-transition param struct", u"Initializes gGlBlendState blend-transition param struct"),
 ],
 0x080147d8: [
  (u"Writes blend2_level to [gl_state+0x8] bits[11:2] (mask 0xFFFFFC03, shift 10); saves blend1_level to [gl_state+0x1]; old [gl_state+0x1] -> [gl_state+0x0]; writes blend_target to [gl_state+0x2]",
   u"Clears blend1 step bits[9:2] of [gGlBlendState+0x8] (GL_CLEAR_BITS_9_2); inserts blend2_level into bits[17:10] (GL_CLEAR_BITS_17_10, shift 10); saves blend1_level to [gGlBlendState+0x1]; old [gGlBlendState+0x1] -> [gGlBlendState+0x0]; writes blend_target to [gGlBlendState+0x2]"),
  (u"Constants: GL_STATE_BASE=0x02023480 / BLEND2_MASK=0xFFFFFC03 / BLEND2_SHIFT=10.",
   u"Constants: gGlBlendState=0x02023480 / GL_CLEAR_BITS_9_2=0xFFFFFC03 / GL_CLEAR_BITS_17_10=0xFFFC03FF / BLEND2_SHIFT=10."),
 ],
 0x08014838: [
  (u"writes r0/r1/r2/r3/r5 to gDemoState+0x0", u"writes r0/r1/r2/r3/r5 to gGlBlendState+0x0"),
 ],
 0x080148f4: [
  (u"Reads gDemoState+0x8", u"Reads gGlBlendState+0x8"),
 ],
 0x08014914: [
  (u"reads gDemoState+0x8 bits[9:2]", u"reads gGlBlendState+0x8 bits[9:2]"),
  (u"Side-effects: gDemoState+0x8 step field", u"Side-effects: gGlBlendState+0x8 step field"),
 ],
}


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _check_value(slot_int, want):
    d = getDataAt(_addr(slot_int))
    if d is None or d.getLength() != 4:
        return None, "no 4B data"
    try:
        dv = d.getValue()
        iv = (int(dv.getValue()) & 0xffffffff) if hasattr(dv, "getValue") else (int(dv) & 0xffffffff)
    except Exception:
        iv = None
    if iv is not None and want is not None and iv != (want & 0xffffffff):
        return iv, "value mismatch decl=0x%x" % want
    return iv, None


def main():
    print("=== RefineGlBlendBatch2 (DRY=%s) ===" % DRY)
    et = currentProgram.getEquateTable()
    rm = currentProgram.getReferenceManager()
    listing = currentProgram.getListing()
    nA = nB = nC = nD = nE = 0

    # A. gGlBlendState label + refs + slot rename
    if not DRY:
        createLabel(_addr(GL_BLEND_STATE), "gGlBlendState", True, SourceType.USER_DEFINED)
    for slot_int, label in PTR_SLOTS:
        iv, err = _check_value(slot_int, GL_BLEND_STATE)
        if err:
            print("[A FAIL] 0x%08x: %s (got 0x%x)" % (slot_int, err, iv or 0)); continue
        if DRY:
            print("[A dry] 0x%08x ref->gGlBlendState rename %s" % (slot_int, label)); nA += 1; continue
        ref = rm.addMemoryReference(_addr(slot_int), _addr(GL_BLEND_STATE), RefType.DATA, SourceType.USER_DEFINED, 0)
        rm.setPrimary(ref, True)
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        print("[A ok] 0x%08x -> %s" % (slot_int, label)); nA += 1

    # B. data-equate + slot rename
    for slot_int, value, cname, label in EQ_SLOTS:
        iv, err = _check_value(slot_int, value)
        if err:
            print("[B FAIL] 0x%08x: %s (got 0x%x)" % (slot_int, err, iv or 0)); continue
        if DRY:
            print("[B dry] 0x%08x equate %s=0x%x rename %s" % (slot_int, cname, value, label)); nB += 1; continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        eq = et.getEquate(cname)
        if eq is None:
            eq = et.createEquate(cname, value)
        eq.addReference(_addr(slot_int), 0)
        print("[B ok] 0x%08x -> %s (%s)" % (slot_int, label, cname)); nB += 1

    # C. rename-only slots
    for slot_int, label in RENAME_ONLY:
        iv, err = _check_value(slot_int, None)
        if err:
            print("[C FAIL] 0x%08x: %s" % (slot_int, err)); continue
        if DRY:
            print("[C dry] 0x%08x rename %s" % (slot_int, label)); nC += 1; continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        print("[C ok] 0x%08x -> %s" % (slot_int, label)); nC += 1

    # D. function rename
    for fn_int, newname in FUNC_RENAME:
        fn = getFunctionAt(_addr(fn_int))
        if fn is None:
            print("[D FAIL] no function @ 0x%08x" % fn_int); continue
        old = fn.getName()
        if DRY:
            print("[D dry] 0x%08x %s -> %s" % (fn_int, old, newname)); nD += 1; continue
        fn.setName(newname, SourceType.USER_DEFINED)
        print("[D ok] 0x%08x %s -> %s" % (fn_int, old, newname)); nD += 1

    # E1. full plate replace
    for addr_int, newtxt in sorted(PLATE_FULL.items()):
        cu = listing.getCodeUnitAt(_addr(addr_int))
        if cu is None:
            print("[E FAIL] no code unit @ 0x%08x" % addr_int); continue
        if DRY:
            print("[E dry] 0x%08x full plate set (%d chars)" % (addr_int, len(newtxt))); nE += 1; continue
        cu.setComment(CodeUnit.PLATE_COMMENT, newtxt)
        print("[E ok] 0x%08x full plate set" % addr_int); nE += 1

    # E2. targeted plate replace
    for addr_int in sorted(PLATE_REPL.keys()):
        cu = listing.getCodeUnitAt(_addr(addr_int))
        txt = cu.getComment(CodeUnit.PLATE_COMMENT) if cu else None
        if txt is None:
            print("[E FAIL] no plate @ 0x%08x" % addr_int); continue
        new = txt
        ok = True
        for old, rep in PLATE_REPL[addr_int]:
            if old not in new:
                print("[E FAIL] 0x%08x pattern not found: %r" % (addr_int, old[:36])); ok = False; continue
            new = new.replace(old, rep)
        if not ok or new == txt:
            if ok:
                print("[E skip] 0x%08x no change" % addr_int)
            continue
        if DRY:
            print("[E dry] 0x%08x plate update (%d repl)" % (addr_int, len(PLATE_REPL[addr_int]))); nE += 1; continue
        cu.setComment(CodeUnit.PLATE_COMMENT, new)
        print("[E ok] 0x%08x plate updated" % addr_int); nE += 1

    print("[done] A=%d B=%d C=%d D=%d E=%d (DRY=%s)" % (nA, nB, nC, nD, nE, DRY))


main()
