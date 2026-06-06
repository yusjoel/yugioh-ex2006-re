# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineCellAnimOamBatch10.py — p5 batch-10 (ISD cell-anim OAM 簇 0x15954..0x15ac4, 2 fn)
#   setup_isd_cell_anim_oam_entry (0x15954) + dispatch_isd_cell_anim_oam_setup (0x15a8c)
#   R3: gOamAttrBuildBuf=0x030007f8 (iwram.inc) OAM 属性构建暂存缓冲 (128×8B=0x400B);
#       slot 0x15a80 加 USER label+DATA ref+改名
#   R1: OAM attr2 char-name 字段掩码 2 个 (新 constants/oam_attr.inc):
#       OAM_ATTR2_CHARNAME_MASK(0x3ff)/OAM_ATTR2_CHARNAME_CLEAR(0xfffffc00)
#   R2: 0x15a74(0x1ff scale-shift 阈值) + 0x15af8(alloc_cell_anim_slot assert line 0x127) 槽改名
#   R5: 3 plate 的 0x030007f8 散文引用 → gOamAttrBuildBuf (setup / setup_decimal_digit_oam_batch /
#       build_oam_attrs_from_cell_with_affine 消费者)
# Usage: tools\asm-regen\ghidra-run-script.bat RefineCellAnimOamBatch10.py [dry]
from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"): DRY = True
except Exception:
    pass

# A. carve/global ref + slot rename (slot_addr, target_addr, gas_label, slot_label)
REF_SLOTS = [
 (0x08015a80, 0x030007f8, 'gOamAttrBuildBuf',
  'setup_isd_cell_anim_oam_entry_ptr_oam_attr_build_buf'),
]

# B. data-equate (slot_addr, value, const_name, slot_label)
EQ_SLOTS = [
 (0x08015a84, 0x000003ff, 'OAM_ATTR2_CHARNAME_MASK',
  'setup_isd_cell_anim_oam_entry_oam_attr2_charname_mask'),
 (0x08015a88, 0xfffffc00, 'OAM_ATTR2_CHARNAME_CLEAR',
  'setup_isd_cell_anim_oam_entry_oam_attr2_charname_clear'),
]

# C. plain slot rename (slot_addr, slot_label) — 无 equate/无 ref 变化
RENAME_SLOTS = [
 (0x08015a74, 'setup_isd_cell_anim_oam_entry_scale_shift_threshold'),  # 0x1ff: cmp r5 阈值, 选 >>5/>>9
 (0x08015af8, 'alloc_cell_anim_slot_assert_line'),                     # 0x127=295 (assert 行号)
]

# D. plate targeted (addr -> [(old, new), ...])
PLATE_REPL = {
 0x08015954: [
  (u"build_oam_attrs_from_cell_with_affine(0x030007f8, max=128",
   u"build_oam_attrs_from_cell_with_affine(gOamAttrBuildBuf, max=128"),
  (u"OAM buffer [0x030007f8+...] written.",
   u"OAM buffer [gOamAttrBuildBuf (0x030007f8)+...] written."),
 ],
 0x08015ea4: [
  (u"[0x030007f8+offset]: OAM attrs written",
   u"[gOamAttrBuildBuf (0x030007f8)+offset]: OAM attrs written"),
  (u"OAM_BUF=0x030007f8",
   u"OAM_BUF=gOamAttrBuildBuf (0x030007f8)"),
 ],
 0x080e969c: [
  (u"[0x030007f8 at callsite]",
   u"[gOamAttrBuildBuf (0x030007f8) at callsite]"),
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
    print("=== RefineCellAnimOamBatch10 (DRY=%s) ===" % DRY)
    rm = currentProgram.getReferenceManager()
    et = currentProgram.getEquateTable()
    listing = currentProgram.getListing()
    nA = nB = nC = nD = 0
    made = set()

    for slot_int, tgt_int, gas_label, slot_label in REF_SLOTS:
        d = getDataAt(_addr(slot_int))
        if d is None or d.getLength() != 4:
            print("[A FAIL] no 4B data @ 0x%08x" % slot_int); continue
        if DRY:
            print("[A dry] 0x%08x ref->%s rename %s" % (slot_int, gas_label, slot_label)); nA += 1; continue
        if tgt_int not in made:
            createLabel(_addr(tgt_int), gas_label, True, SourceType.USER_DEFINED)
            made.add(tgt_int)
        ref = rm.addMemoryReference(_addr(slot_int), _addr(tgt_int), RefType.DATA, SourceType.USER_DEFINED, 0)
        rm.setPrimary(ref, True)
        createLabel(_addr(slot_int), slot_label, True, SourceType.USER_DEFINED)
        print("[A ok] 0x%08x -> %s (%s)" % (slot_int, slot_label, gas_label)); nA += 1

    for slot_int, value, cname, label in EQ_SLOTS:
        ok, err = _check(slot_int, value)
        if not ok:
            print("[B FAIL] 0x%08x: %s" % (slot_int, err)); continue
        if DRY:
            print("[B dry] 0x%08x equate %s=0x%x rename %s" % (slot_int, cname, value, label)); nB += 1; continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        eq = et.getEquate(cname)
        if eq is None:
            eq = et.createEquate(cname, value)
        eq.addReference(_addr(slot_int), 0)
        print("[B ok] 0x%08x -> %s (%s)" % (slot_int, label, cname)); nB += 1

    for slot_int, label in RENAME_SLOTS:
        d = getDataAt(_addr(slot_int))
        if d is None or d.getLength() != 4:
            print("[C FAIL] no 4B data @ 0x%08x" % slot_int); continue
        if DRY:
            print("[C dry] 0x%08x rename %s" % (slot_int, label)); nC += 1; continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        print("[C ok] 0x%08x -> %s" % (slot_int, label)); nC += 1

    for addr_int in sorted(PLATE_REPL.keys()):
        cu = listing.getCodeUnitAt(_addr(addr_int))
        txt = cu.getComment(CodeUnit.PLATE_COMMENT) if cu else None
        if txt is None:
            print("[D FAIL] no plate @ 0x%08x" % addr_int); continue
        new = txt
        ok = True
        for old, rep in PLATE_REPL[addr_int]:
            if old not in new:
                print("[D FAIL] 0x%08x pattern not found: %r" % (addr_int, old[:40])); ok = False; continue
            new = new.replace(old, rep)
        if not ok or new == txt:
            continue
        if DRY:
            print("[D dry] 0x%08x plate update (%d repl)" % (addr_int, len(PLATE_REPL[addr_int]))); nD += 1; continue
        cu.setComment(CodeUnit.PLATE_COMMENT, new)
        print("[D ok] 0x%08x plate updated" % addr_int); nD += 1

    print("[done] A=%d B=%d C=%d D=%d (DRY=%s)" % (nA, nB, nC, nD, DRY))


main()
