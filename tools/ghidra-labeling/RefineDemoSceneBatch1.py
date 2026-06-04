# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineDemoSceneBatch1.py  — p5 batch-1 (demo scene 簇 0x13510..0x14398) 字面量池常量符号化
#   对 41 个高置信值槽: (1) 重命名池标签为 <func>_<const>(碰撞加地址尾号);
#   (2) 设 data-equate <CONST> 于该数据地址 op0 -> ExportRangeToGas.resolve_word_equate 导出符号。
#   GAS 端 constants/demo_state.inc 的 .equ 解析回同值 -> byte-identical。
# Usage: tools\asm-regen\ghidra-run-script.bat RefineDemoSceneBatch1.py [dry]
from ghidra.program.model.symbol import SourceType

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry","--dry","1","true"): DRY = True
except Exception: pass

# (addr, value, const_name, slot_label)
SLOTS = [
(0x08013568, 0x05000025, 'DEMO_CPUSET_FILL_CTRL', 'reset_display_and_gl_state_demo_cpuset_fill_ctrl'),
(0x0801356c, 0x00001e01, 'DEMO_BG1CNT_INIT', 'reset_display_and_gl_state_demo_bg1cnt_init'),
(0x08013570, 0x00001f02, 'DEMO_BG2CNT_INIT', 'reset_display_and_gl_state_demo_bg2cnt_init'),
(0x08013574, 0x00009b0b, 'DEMO_BG3CNT_INIT', 'reset_display_and_gl_state_demo_bg3cnt_init'),
(0x08013670, 0xffffc07f, 'DEMO_CLEAR_BITS_13_7', 'setup_demo_sprite_entry_demo_clear_bits_13_7'),
(0x0801373c, 0xffffc07f, 'DEMO_CLEAR_BITS_13_7', 'setup_demo_sprite_entry_alt_demo_clear_bits_13_7'),
(0x08013860, 0xffffc07f, 'DEMO_CLEAR_BITS_13_7', 'load_demo_bg_gfx_set0_demo_clear_bits_13_7'),
(0x08013938, 0xffffc07f, 'DEMO_CLEAR_BITS_13_7', 'load_demo_bg_gfx_set1_demo_clear_bits_13_7'),
(0x0801393c, 0x141e0000, 'DEMO_EXTRA_RESOURCE_DESC', 'load_demo_bg_gfx_set1_demo_extra_resource_desc'),
(0x080139ac, 0x000001ff, 'DEMO_KEEP_BITS_8_0', 'write_bg3_scroll_regs_demo_keep_bits_8_0'),
(0x08013a0c, 0xfffffe01, 'DEMO_CLEAR_BITS_8_1', 'tick_demo_bg3_hscroll_demo_clear_bits_8_1'),
(0x08013a64, 0xfffffe01, 'DEMO_CLEAR_BITS_8_1', 'tick_demo_bg3_vscroll_demo_clear_bits_8_1'),
(0x08013b7c, 0xffff9fff, 'DEMO_CLEAR_BITS_14_13', 'apply_demo_window_fade_in_step_demo_clear_bits_14_13'),
(0x08013ca0, 0xffffe0ff, 'DEMO_CLEAR_BITS_12_8', 'tick_demo_scene_state_machine_demo_clear_bits_12_8_ca0'),
(0x08013cf4, 0xfffe01ff, 'DEMO_CLEAR_BITS_16_9', 'tick_demo_scene_state_machine_demo_clear_bits_16_9_cf4'),
(0x08013d4c, 0xfffe01ff, 'DEMO_CLEAR_BITS_16_9', 'tick_demo_scene_state_machine_demo_clear_bits_16_9_d4c'),
(0x08013d50, 0xfffffe01, 'DEMO_CLEAR_BITS_8_1', 'tick_demo_scene_state_machine_demo_clear_bits_8_1_d50'),
(0x08013ddc, 0xfffffe01, 'DEMO_CLEAR_BITS_8_1', 'tick_demo_scene_state_machine_demo_clear_bits_8_1_ddc'),
(0x08013de0, 0xffffe0ff, 'DEMO_CLEAR_BITS_12_8', 'tick_demo_scene_state_machine_demo_clear_bits_12_8_de0'),
(0x08013e90, 0xffffe0ff, 'DEMO_CLEAR_BITS_12_8', 'tick_demo_scene_state_machine_demo_clear_bits_12_8_e90'),
(0x08013e94, 0xfffffe01, 'DEMO_CLEAR_BITS_8_1', 'tick_demo_scene_state_machine_demo_clear_bits_8_1_e94'),
(0x08013ed0, 0xffffe0ff, 'DEMO_CLEAR_BITS_12_8', 'tick_demo_scene_state_machine_demo_clear_bits_12_8_ed0'),
(0x08013ed4, 0xfffe01ff, 'DEMO_CLEAR_BITS_16_9', 'tick_demo_scene_state_machine_demo_clear_bits_16_9_ed4'),
(0x08013f20, 0xfffffe01, 'DEMO_CLEAR_BITS_8_1', 'tick_demo_scene_state_machine_demo_clear_bits_8_1_f20'),
(0x08013f24, 0xffffe0ff, 'DEMO_CLEAR_BITS_12_8', 'tick_demo_scene_state_machine_demo_clear_bits_12_8_f24'),
(0x08013fc8, 0xffffe0ff, 'DEMO_CLEAR_BITS_12_8', 'tick_demo_scene_state_machine_demo_clear_bits_12_8_fc8'),
(0x08013fd0, 0xffff3fff, 'DEMO_CLEAR_BITS_15_14', 'tick_demo_scene_state_machine_demo_clear_bits_15_14'),
(0x08013fdc, 0xfffffe01, 'DEMO_CLEAR_BITS_8_1', 'tick_demo_scene_state_machine_demo_clear_bits_8_1_fdc'),
(0x08013fe0, 0xfffe01ff, 'DEMO_CLEAR_BITS_16_9', 'tick_demo_scene_state_machine_demo_clear_bits_16_9_fe0'),
(0x0801405c, 0xffff9fff, 'DEMO_CLEAR_BITS_14_13', 'tick_demo_scene_state_machine_demo_clear_bits_14_13_05c'),
(0x08014060, 0xfffffe01, 'DEMO_CLEAR_BITS_8_1', 'tick_demo_scene_state_machine_demo_clear_bits_8_1_060'),
(0x08014064, 0xfffe01ff, 'DEMO_CLEAR_BITS_16_9', 'tick_demo_scene_state_machine_demo_clear_bits_16_9_064'),
(0x0801412c, 0xfffffe01, 'DEMO_CLEAR_BITS_8_1', 'tick_demo_scene_state_machine_demo_clear_bits_8_1_12c'),
(0x08014134, 0xfffe01ff, 'DEMO_CLEAR_BITS_16_9', 'tick_demo_scene_state_machine_demo_clear_bits_16_9_134'),
(0x080141f4, 0xffffe0ff, 'DEMO_CLEAR_BITS_12_8', 'tick_demo_scene_state_machine_demo_clear_bits_12_8_1f4'),
(0x0801424c, 0xffff9fff, 'DEMO_CLEAR_BITS_14_13', 'tick_demo_scene_state_machine_demo_clear_bits_14_13_24c'),
(0x08014250, 0xfffffe01, 'DEMO_CLEAR_BITS_8_1', 'tick_demo_scene_state_machine_demo_clear_bits_8_1_250'),
(0x08014254, 0xfffe01ff, 'DEMO_CLEAR_BITS_16_9', 'tick_demo_scene_state_machine_demo_clear_bits_16_9_254'),
(0x080142f8, 0xfffffe01, 'DEMO_CLEAR_BITS_8_1', 'tick_demo_scene_state_machine_demo_clear_bits_8_1_2f8'),
(0x080142fc, 0xffffe0ff, 'DEMO_CLEAR_BITS_12_8', 'tick_demo_scene_state_machine_demo_clear_bits_12_8_2fc'),
(0x08014300, 0xfffe01ff, 'DEMO_CLEAR_BITS_16_9', 'tick_demo_scene_state_machine_demo_clear_bits_16_9_300'),
]

def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

def main():
    print("=== RefineDemoSceneBatch1 (DRY=%s) n=%d ===" % (DRY, len(SLOTS)))
    et = currentProgram.getEquateTable()
    nl = ne = 0
    for addr_int, value, cname, label in SLOTS:
        a = _addr(addr_int)
        d = getDataAt(a)
        if d is None or d.getLength() != 4:
            print("[FAIL] no 4-byte data @ 0x%08x (%s)" % (addr_int, d)); continue
        # 校验数据值与声明一致
        try:
            dv = d.getValue()
            iv = (int(dv.getValue()) & 0xffffffff) if hasattr(dv,"getValue") else (int(dv) & 0xffffffff)
        except Exception:
            iv = None
        if iv is not None and iv != (value & 0xffffffff):
            print("[FAIL] value mismatch @ 0x%08x: data=0x%x decl=0x%x" % (addr_int, iv, value)); continue
        if DRY:
            print("[dry] 0x%08x -> %s / equate %s=0x%x" % (addr_int, label, cname, value)); nl+=1; ne+=1; continue
        createLabel(a, label, True, SourceType.USER_DEFINED); nl += 1
        eq = et.getEquate(cname)
        if eq is None: eq = et.createEquate(cname, value)
        eq.addReference(a, 0); ne += 1
    print("[done] labels=%d equates=%d (DRY=%s)" % (nl, ne, DRY))

main()
