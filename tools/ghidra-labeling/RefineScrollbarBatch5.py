# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineScrollbarBatch5.py — p5 batch-5 (GL_Scrollbar 簇 0x15384..0x155f4, 11 fn)
#   R1/R2: data-equate 5 个字段位掩码/控制字 (新 constants/gl_scrollbar.inc) + 7 槽改名
#   R5   : 4 plate 的过时 FUN_ caller 引用改现名 + thumb mask 名对齐 equate
#   注: GL_Scrollbar* 由 r0 传入 (非全局, 无 ewram label)。0x1550a 处 .byte 小函数为
#        独立 R4 (误标数据), 本批 defer。
# Usage: tools\asm-regen\ghidra-run-script.bat RefineScrollbarBatch5.py [dry]
from ghidra.program.model.symbol import SourceType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"): DRY = True
except Exception:
    pass

# A. data-equate (slot_addr, value, const_name, slot_label)
EQ_SLOTS = [
 (0x08015410, 0x05000004, 'SCROLLBAR_INIT_FILL_CTRL',   'init_scrollbar_oam_entry_scrollbar_init_fill_ctrl'),
 (0x08015414, 0x000001ff, 'SCROLLBAR_KEEP_BITS_8_0',    'init_scrollbar_oam_entry_scrollbar_keep_bits_8_0'),
 (0x08015418, 0xffff803f, 'SCROLLBAR_CLEAR_BITS_14_6',  'init_scrollbar_oam_entry_scrollbar_clear_bits_14_6'),
 (0x0801541c, 0xff007fff, 'SCROLLBAR_CLEAR_BITS_23_15', 'init_scrollbar_oam_entry_scrollbar_clear_bits_23_15'),
 (0x08015420, 0xfffc01ff, 'SCROLLBAR_CLEAR_BITS_17_9',  'init_scrollbar_oam_entry_scrollbar_clear_bits_17_9'),
 (0x08015634, 0x000001ff, 'SCROLLBAR_KEEP_BITS_8_0',    'update_scrollbar_thumb_display_scrollbar_keep_bits_8_0'),
 (0x08015638, 0xfffc01ff, 'SCROLLBAR_CLEAR_BITS_17_9',  'update_scrollbar_thumb_display_scrollbar_clear_bits_17_9'),
]

# B. plate targeted (addr -> [(old, new), ...])
PLATE_REPL = {
 0x08015424: [
  (u"Callers FUN_08018d3c/banlist_080186f0 read this param",
   u"Callers tick_oam_palette_fade_settings/read_banlist_char_at_scroll_pos read this param"),
 ],
 0x0801544c: [
  (u"Caller FUN_080155f4 reads result for OAM Y update.",
   u"Caller update_scrollbar_thumb_display reads result for OAM Y update."),
 ],
 0x080154a4: [
  (u"Caller banlist_080186f0 reads current scroll position",
   u"Caller read_banlist_char_at_scroll_pos reads current scroll position"),
 ],
 0x080155f4: [
  (u"Called by FUN_08018434 (tags: [scrollbar,name_input]) and FUN_0801a794 (tags: [scrollbar,banlist])",
   u"Called by tick_name_input_scrollbar_and_anims and tick_banlist_scrollbar_and_slot_anim"),
  (u"THUMB_FIELD_MASK = 0xfffc01ff", u"SCROLLBAR_CLEAR_BITS_17_9 = 0xfffc01ff"),
  (u"THUMB_VAL_MASK = 0x000001ff", u"SCROLLBAR_KEEP_BITS_8_0 = 0x000001ff"),
 ],
}


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _check(slot_int, want):
    d = getDataAt(_addr(slot_int))
    if d is None or d.getLength() != 4:
        return False, "no 4B data"
    try:
        dv = d.getValue()
        iv = (int(dv.getValue()) & 0xffffffff) if hasattr(dv, "getValue") else (int(dv) & 0xffffffff)
    except Exception:
        iv = None
    if iv is not None and iv != (want & 0xffffffff):
        return False, "value mismatch got=0x%x want=0x%x" % (iv, want)
    return True, None


def main():
    print("=== RefineScrollbarBatch5 (DRY=%s) ===" % DRY)
    et = currentProgram.getEquateTable()
    listing = currentProgram.getListing()
    nA = nB = 0

    for slot_int, value, cname, label in EQ_SLOTS:
        ok, err = _check(slot_int, value)
        if not ok:
            print("[A FAIL] 0x%08x: %s" % (slot_int, err)); continue
        if DRY:
            print("[A dry] 0x%08x equate %s=0x%x rename %s" % (slot_int, cname, value, label)); nA += 1; continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        eq = et.getEquate(cname)
        if eq is None:
            eq = et.createEquate(cname, value)
        eq.addReference(_addr(slot_int), 0)
        print("[A ok] 0x%08x -> %s (%s)" % (slot_int, label, cname)); nA += 1

    for addr_int in sorted(PLATE_REPL.keys()):
        cu = listing.getCodeUnitAt(_addr(addr_int))
        txt = cu.getComment(CodeUnit.PLATE_COMMENT) if cu else None
        if txt is None:
            print("[B FAIL] no plate @ 0x%08x" % addr_int); continue
        new = txt
        ok = True
        for old, rep in PLATE_REPL[addr_int]:
            if old not in new:
                print("[B FAIL] 0x%08x pattern not found: %r" % (addr_int, old[:40])); ok = False; continue
            new = new.replace(old, rep)
        if not ok or new == txt:
            continue
        if DRY:
            print("[B dry] 0x%08x plate update (%d repl)" % (addr_int, len(PLATE_REPL[addr_int]))); nB += 1; continue
        cu.setComment(CodeUnit.PLATE_COMMENT, new)
        print("[B ok] 0x%08x plate updated" % addr_int); nB += 1

    print("[done] A=%d B=%d (DRY=%s)" % (nA, nB, DRY))


main()
