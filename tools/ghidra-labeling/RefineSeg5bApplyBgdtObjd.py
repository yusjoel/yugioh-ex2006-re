# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineSeg5bApplyBgdtObjd.py — p5 Seg-5b (0x165bc..0x16a7c)
#   apply_bgdt_entry_to_bg(0x165bc) / fill_vram_screen_rect_zero(0x16908) /
#   apply_objd_entry_to_sprite(0x1695c) + orphan dispatcher cluster (§5.1)
#   - 4 attr 掩码 equate (新 gfx_resource.inc): GFX_ATTR_CLEAR_BITS_8_7 / _13_7
#   - fill_vram cpuset word-count mask 槽改名
#   - orphan jump table PTR_DAT_080169f0 改名 (handlers 区进 §5.1)
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
 (0x08016634, 0xfffffe7f, 'GFX_ATTR_CLEAR_BITS_8_7',  'apply_bgdt_entry_to_bg_attr_clear_bits_8_7'),
 (0x08016638, 0xffffc07f, 'GFX_ATTR_CLEAR_BITS_13_7', 'apply_bgdt_entry_to_bg_attr_clear_bits_13_7'),
 (0x0801682c, 0xffffc07f, 'GFX_ATTR_CLEAR_BITS_13_7', 'apply_bgdt_entry_to_bg_attr_clear_bits_13_7_b'),
 (0x080168c8, 0xffffc07f, 'GFX_ATTR_CLEAR_BITS_13_7', 'apply_bgdt_entry_to_bg_attr_clear_bits_13_7_c'),
]

# B. plain slot rename (slot_addr, slot_label, eol)
RENAME_SLOTS = [
 (0x08016958, 'fill_vram_screen_rect_zero_cpuset_wordcount_mask',
  '= 0x001fffff; bios_cpu_set length field (bits[20:0]) mask'),
 (0x080169f0, 'orphan_objd_type_dispatch_jump_table',
  '12-entry; targets 0x16a20..70 (orphan handlers @0x16a20 ROM_INCBIN, dead code, 0 ext refs)'),
]


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
    print("=== RefineSeg5bApplyBgdtObjd (DRY=%s) ===" % DRY)
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

    for slot_int, label, eol in RENAME_SLOTS:
        d = getDataAt(_addr(slot_int))
        if d is None or d.getLength() != 4:
            print("[B FAIL] no 4B data @ 0x%08x" % slot_int); continue
        if DRY:
            print("[B dry] 0x%08x rename %s" % (slot_int, label)); nB += 1; continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        if eol:
            listing.getCodeUnitAt(_addr(slot_int)).setComment(CodeUnit.EOL_COMMENT, eol)
        print("[B ok] 0x%08x -> %s" % (slot_int, label)); nB += 1

    print("[done] A=%d B=%d (DRY=%s)" % (nA, nB, DRY))


main()
