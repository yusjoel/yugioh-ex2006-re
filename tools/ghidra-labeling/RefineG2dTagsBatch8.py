# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineG2dTagsBatch8.py — p5 batch-8 (NNS G2D GFX entry accessor 簇 0x16140..0x16268, 10 fn)
#   R1/R2: data-equate 3 个 FourCC tag (BGDT/OBJD/PALT, 新 g2d_tags.inc) + 9 槽改名
#   R5: 9 accessor plate 去掉过时 DAT_/DWORD_ 槽引用 + find_gfx plate tag_* -> *_TAG
# Usage: tools\asm-regen\ghidra-run-script.bat RefineG2dTagsBatch8.py [dry]
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
 (0x08016184, 0x54444742, 'BGDT_TAG', 'get_bgdt_entry_char_base_bgdt_tag'),
 (0x080161a0, 0x54444742, 'BGDT_TAG', 'get_bgdt_entry_field0x18_bgdt_tag'),
 (0x080161bc, 0x444a424f, 'OBJD_TAG', 'get_objd_entry_field0x1c_objd_tag'),
 (0x080161d4, 0x544c4150, 'PALT_TAG', 'get_palt_entry_byte_size_palt_tag'),
 (0x08016200, 0x54444742, 'BGDT_TAG', 'get_bgdt_entry_pixel_dimensions_bgdt_tag'),
 (0x08016214, 0x54444742, 'BGDT_TAG', 'get_bgdt_inline_data_ptr_bgdt_tag'),
 (0x08016234, 0x54444742, 'BGDT_TAG', 'get_bgdt_second_blob_ptr_bgdt_tag'),
 (0x08016254, 0x444a424f, 'OBJD_TAG', 'get_objd_second_blob_ptr_objd_tag'),
 (0x08016268, 0x444a424f, 'OBJD_TAG', 'get_objd_inline_data_ptr_objd_tag'),
]

# B. plate targeted (addr -> [(old, new), ...])
PLATE_REPL = {
 0x08016140: [
  (u"tag_BGDT=0x54444742 / tag_OBJD=0x444a424f / tag_PALT=0x544c4150",
   u"BGDT_TAG=0x54444742 / OBJD_TAG=0x444a424f / PALT_TAG=0x544c4150"),
 ],
 0x0801616c: [(u", DAT_08016184)", u")")],
 0x08016188: [(u", DAT_080161a0)", u")")],
 0x080161a4: [(u", DAT_080161bc)", u")")],
 0x080161c0: [(u", DAT_080161d4)", u")")],
 0x080161e0: [(u", DWORD_08016200)", u")")],
 0x08016204: [(u", DWORD_08016214)", u")")],
 0x08016218: [(u", DWORD_08016234)", u")")],
 0x08016238: [(u", DWORD_08016254)", u")")],
 0x08016258: [(u", DWORD_08016268)", u")")],
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
    print("=== RefineG2dTagsBatch8 (DRY=%s) ===" % DRY)
    et = currentProgram.getEquateTable()
    listing = currentProgram.getListing()
    nA = nB = 0

    for slot_int, value, cname, label in EQ_SLOTS:
        ok, err = _check(slot_int, value)
        if not ok:
            print("[A FAIL] 0x%08x: %s" % (slot_int, err)); continue
        if DRY:
            print("[A dry] 0x%08x equate %s rename %s" % (slot_int, cname, label)); nA += 1; continue
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
                print("[B FAIL] 0x%08x pattern not found: %r" % (addr_int, old)); ok = False; continue
            new = new.replace(old, rep)
        if not ok or new == txt:
            continue
        if DRY:
            print("[B dry] 0x%08x plate update" % addr_int); nB += 1; continue
        cu.setComment(CodeUnit.PLATE_COMMENT, new)
        print("[B ok] 0x%08x plate updated" % addr_int); nB += 1

    print("[done] A=%d B=%d (DRY=%s)" % (nA, nB, DRY))


main()
