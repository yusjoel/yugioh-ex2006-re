# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineSeg1bTextPrng.py — p5 Seg-1b (0x14398..0x14600 gap, 7 fn)
#   tick_prng_step_sequence(0x14398) MISNOMER -> RENAME step_demo_scene_phase
#     + R7 carve demo_scene_phase_table(0x09e587d4, 3 fn ptr+NULL, rom.s 已切) ref/改名
#     + gPrng base / phase-field-clear mask 槽改名 + plate 全重写
#   banlist_password_enter_char/append/advance/count/measure (5 文字函数):
#     gSettings(0x02006c2c via base+offset) 槽改名 + gTextEncodingOverride(0x0202348c) 全局符号化
#   copy_str_unbounded: 0x05f5e0ff 无上限哨兵槽改名
# Usage: tools\asm-regen\ghidra-run-script.bat RefineSeg1bTextPrng.py [dry]
from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"): DRY = True
except Exception:
    pass

# A. function rename (addr, old, new)
FUNC_RENAME = [
 (0x08014398, 'tick_prng_step_sequence', 'step_demo_scene_phase'),
]

# B. global/carve label + DATA ref + slot rename (target_addr, gas_label, [(slot_addr, slot_label),...])
GLOBAL_REFS = [
 (0x09e587d4, 'demo_scene_phase_table', [
   (0x080143dc, 'step_demo_scene_phase_phase_table'),
 ]),
 (0x0202348c, 'gTextEncodingOverride', [
   (0x08014438, 'banlist_password_enter_char_ptr_text_encoding_override'),
   (0x080144bc, 'append_text_to_buf_charlen_ptr_text_encoding_override'),
   (0x08014528, 'advance_text_ptr_by_charlen_ptr_text_encoding_override'),
   (0x08014598, 'count_str_charlen_ptr_text_encoding_override'),
   (0x080145f0, 'measure_text_pixel_width_ptr_text_encoding_override'),
 ]),
]

# C. plain slot rename (slot_addr, slot_label, eol_or_None)
RENAME_SLOTS = [
 # tick_prng -> step_demo_scene_phase
 (0x080143e0, 'step_demo_scene_phase_ptr_gprng_base', '+0x204 = gDemoSceneInitPhase (0x03000244)'),
 (0x080143e4, 'step_demo_scene_phase_phase_field_clear_mask', 'clear bits[21:14] (phase idx)'),
 # copy_str_unbounded sentinel
 (0x0801447c, 'copy_str_unbounded_len_sentinel', '= 99,999,999 (0x5f5e0ff) 无上限哨兵'),
 # gSettings base(0x02000000)+offset(0x6c2c) per text fn
 (0x08014430, 'banlist_password_enter_char_ewram_base', None),
 (0x08014434, 'banlist_password_enter_char_gsettings_offset', '= gSettings(0x02006c2c) - EWRAM base'),
 (0x080144b4, 'append_text_to_buf_charlen_ewram_base', None),
 (0x080144b8, 'append_text_to_buf_charlen_gsettings_offset', '= gSettings(0x02006c2c) - EWRAM base'),
 (0x08014520, 'advance_text_ptr_by_charlen_ewram_base', None),
 (0x08014524, 'advance_text_ptr_by_charlen_gsettings_offset', '= gSettings(0x02006c2c) - EWRAM base'),
 (0x08014590, 'count_str_charlen_ewram_base', None),
 (0x08014594, 'count_str_charlen_gsettings_offset', '= gSettings(0x02006c2c) - EWRAM base'),
 (0x080145e8, 'measure_text_pixel_width_ewram_base', None),
 (0x080145ec, 'measure_text_pixel_width_gsettings_offset', '= gSettings(0x02006c2c) - EWRAM base'),
]

# D. full plate rewrite (addr -> text)
FULL_PLATE = {
 0x08014398: (
  u"Demo scene phase sequencer (was mis-named tick_prng_step_sequence; uses gPrng addr only as a base). "
  u"Reads gDemoSceneInitPhase (gPrng+0x204 = 0x03000244) bits[21:14] = current phase index, looks up "
  u"demo_scene_phase_table[index] and calls it via invoke_r0. Phase table: [0]=reset_display_and_gl_state, "
  u"[1]=load_demo_obj_resource_slot0, [2]=tick_demo_scene_state_machine, [3]=NULL (sequence-end sentinel). "
  u"If phase fn returns nonzero (phase done), increments index (mod 256) writing back bits[21:14]; if returns 0, "
  u"calls return_void_handler and returns 0; if table entry is NULL returns 1 (sequence complete). indeg=0 (driven indirectly).\n"
  u"\n"
  u"Params: none. Returns: r0=1 when sequence complete (NULL entry), else 0.\n"
  u"Side effects: updates [gDemoSceneInitPhase] bits[21:14] (+1 mod 256) when a phase completes.\n"
  u"Constants: gDemoSceneInitPhase=0x03000244 (gPrng+0x204) / demo_scene_phase_table=0x09e587d4 / "
  u"PHASE_SHIFT=14 (bits[21:14]) / PHASE_FIELD_CLEAR=0xffc03fff."
 ),
}

# E. plate targeted substring replace (addr -> [(old,new),...])  — text fn 0x0202348c 符号化
PLATE_REPL = {
 0x08014480: [(u"0x0202348c=TCG/OCG override flag", u"gTextEncodingOverride(0x0202348c)=TCG/OCG override flag")],
 0x080144e8: [(u"0x0202348c=TCG/OCG override flag", u"gTextEncodingOverride(0x0202348c)=TCG/OCG override flag")],
 0x0801455c: [(u"附加标志 [0x0202348c]", u"附加标志 [gTextEncodingOverride (0x0202348c)]")],
 0x080145bc: [(u"0x0202348c=TCG/OCG override", u"gTextEncodingOverride(0x0202348c)=TCG/OCG override")],
}


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def main():
    print("=== RefineSeg1bTextPrng (DRY=%s) ===" % DRY)
    rm = currentProgram.getReferenceManager()
    listing = currentProgram.getListing()
    fm = currentProgram.getFunctionManager()
    nF = nG = nC = nP = nE = 0

    for addr_int, old, new in FUNC_RENAME:
        fn = fm.getFunctionAt(_addr(addr_int))
        if fn is None:
            print("[F FAIL] no function @ 0x%08x" % addr_int); continue
        if fn.getName() != old:
            print("[F WARN] 0x%08x name is %r not %r" % (addr_int, fn.getName(), old))
        if DRY:
            print("[F dry] 0x%08x rename %s -> %s" % (addr_int, old, new)); nF += 1; continue
        fn.setName(new, SourceType.USER_DEFINED)
        print("[F ok] 0x%08x -> %s" % (addr_int, new)); nF += 1

    made = set()
    for tgt_int, gas_label, slots in GLOBAL_REFS:
        for slot_int, slot_label in slots:
            d = getDataAt(_addr(slot_int))
            if d is None or d.getLength() != 4:
                print("[G FAIL] no 4B data @ 0x%08x" % slot_int); continue
            if DRY:
                print("[G dry] 0x%08x ref->%s rename %s" % (slot_int, gas_label, slot_label)); nG += 1; continue
            if tgt_int not in made:
                createLabel(_addr(tgt_int), gas_label, True, SourceType.USER_DEFINED); made.add(tgt_int)
            ref = rm.addMemoryReference(_addr(slot_int), _addr(tgt_int), RefType.DATA, SourceType.USER_DEFINED, 0)
            rm.setPrimary(ref, True)
            createLabel(_addr(slot_int), slot_label, True, SourceType.USER_DEFINED)
            print("[G ok] 0x%08x -> %s (%s)" % (slot_int, slot_label, gas_label)); nG += 1

    for slot_int, label, eol in RENAME_SLOTS:
        d = getDataAt(_addr(slot_int))
        if d is None or d.getLength() != 4:
            print("[C FAIL] no 4B data @ 0x%08x" % slot_int); continue
        if DRY:
            print("[C dry] 0x%08x rename %s%s" % (slot_int, label, " +EOL" if eol else "")); nC += 1; continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        if eol:
            listing.getCodeUnitAt(_addr(slot_int)).setComment(CodeUnit.EOL_COMMENT, eol)
        print("[C ok] 0x%08x -> %s" % (slot_int, label)); nC += 1

    for addr_int in sorted(FULL_PLATE.keys()):
        cu = listing.getCodeUnitAt(_addr(addr_int))
        if cu is None:
            print("[P FAIL] no code unit @ 0x%08x" % addr_int); continue
        if DRY:
            print("[P dry] 0x%08x full plate rewrite" % addr_int); nP += 1; continue
        cu.setComment(CodeUnit.PLATE_COMMENT, FULL_PLATE[addr_int])
        print("[P ok] 0x%08x full plate" % addr_int); nP += 1

    for addr_int in sorted(PLATE_REPL.keys()):
        cu = listing.getCodeUnitAt(_addr(addr_int))
        txt = cu.getComment(CodeUnit.PLATE_COMMENT) if cu else None
        if txt is None:
            print("[E FAIL] no plate @ 0x%08x" % addr_int); continue
        new = txt; ok = True
        for old, rep in PLATE_REPL[addr_int]:
            if old not in new:
                print("[E FAIL] 0x%08x pattern not found: %r" % (addr_int, old[:30])); ok = False; continue
            new = new.replace(old, rep)
        if not ok or new == txt: continue
        if DRY:
            print("[E dry] 0x%08x plate repl" % addr_int); nE += 1; continue
        cu.setComment(CodeUnit.PLATE_COMMENT, new)
        print("[E ok] 0x%08x plate repl" % addr_int); nE += 1

    print("[done] F=%d G=%d C=%d P=%d E=%d (DRY=%s)" % (nF, nG, nC, nP, nE, DRY))


main()
