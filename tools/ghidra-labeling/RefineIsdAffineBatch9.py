# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineIsdAffineBatch9.py — p5 batch-9 (ISD affine matrix 指针簇 0x16098..0x1613c, 3 fn)
#   R3/R7: 3 个 ROM 数据 carve (rom.s 已切): isd_affine_matrix_ptr_type4(0x09e587e4=NULL)/
#          type9(0x09e587e8=NULL)/assert_expr_zero_65c(0x09e3a65c="0"); 9 槽加 DATA ref+改名
#   R5: set/get/resolve_isd plate 的 DWORD_/DAT_ 槽引用改 carve label
# Usage: tools\asm-regen\ghidra-run-script.bat RefineIsdAffineBatch9.py [dry]
from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"): DRY = True
except Exception:
    pass

# A. carve-label ref + slot rename (slot_addr, target_addr, gas_label, slot_label)
REF_SLOTS = [
 (0x080160bc, 0x09e587e4, 'isd_affine_matrix_ptr_type4', 'set_isd_affine_matrix_ptr_by_type_ptr_type4'),
 (0x080160c8, 0x09e587e8, 'isd_affine_matrix_ptr_type9', 'set_isd_affine_matrix_ptr_by_type_ptr_type9'),
 (0x080160b4, 0x09e3a65c, 'assert_expr_zero_65c',        'set_isd_affine_matrix_ptr_by_type_assert_expr_zero'),
 (0x080160f8, 0x09e587e4, 'isd_affine_matrix_ptr_type4', 'get_isd_affine_matrix_ptr_from_obj_ptr_type4'),
 (0x08016104, 0x09e587e8, 'isd_affine_matrix_ptr_type9', 'get_isd_affine_matrix_ptr_from_obj_ptr_type9'),
 (0x080160f0, 0x09e3a65c, 'assert_expr_zero_65c',        'get_isd_affine_matrix_ptr_from_obj_assert_expr_zero'),
 (0x08016130, 0x09e587e4, 'isd_affine_matrix_ptr_type4', 'resolve_isd_affine_matrix_ptr_ptr_type4'),
 (0x0801613c, 0x09e587e8, 'isd_affine_matrix_ptr_type9', 'resolve_isd_affine_matrix_ptr_ptr_type9'),
 (0x08016128, 0x09e3a65c, 'assert_expr_zero_65c',        'resolve_isd_affine_matrix_ptr_assert_expr_zero'),
]

# B. plate targeted (addr -> [(old, new), ...])
PLATE_REPL = {
 0x08016098: [
  (u"DWORD_080160bc = 0x09e587e4 (type-4 matrix pointer global slot)",
   u"isd_affine_matrix_ptr_type4 = 0x09e587e4 (type-4 矩阵指针槽; ROM 内 NULL)"),
  (u"DWORD_080160c8 = 0x09e587e8 (type-9 matrix pointer global slot)",
   u"isd_affine_matrix_ptr_type9 = 0x09e587e8 (type-9 矩阵指针槽; ROM 内 NULL)"),
 ],
 0x080160cc: [
  (u"DWORD_080160ec = 0x09e3a64c (source file string)",
   u"isd_draw_c_filename = 0x09e3a64c (源文件串)"),
  (u"DWORD_080160f0 = 0x09e3a65c (condition string)",
   u"assert_expr_zero_65c = 0x09e3a65c (条件串 \"0\")"),
  (u"DWORD_080160f8 = 0x09e587e4 (type-4 matrix pointer slot)",
   u"isd_affine_matrix_ptr_type4 = 0x09e587e4 (type-4 矩阵指针槽)"),
  (u"DWORD_08016104 = 0x09e587e8 (type-9 matrix pointer slot)",
   u"isd_affine_matrix_ptr_type9 = 0x09e587e8 (type-9 矩阵指针槽)"),
 ],
 0x08016108: [
  (u"ldr DAT_08016130 (=0x09e587e4) content", u"ldr isd_affine_matrix_ptr_type4 (=0x09e587e4) content"),
  (u"ldr DAT_0801613c (=0x09e587e8) content", u"ldr isd_affine_matrix_ptr_type9 (=0x09e587e8) content"),
 ],
}


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def main():
    print("=== RefineIsdAffineBatch9 (DRY=%s) ===" % DRY)
    rm = currentProgram.getReferenceManager()
    listing = currentProgram.getListing()
    nA = nB = 0
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
