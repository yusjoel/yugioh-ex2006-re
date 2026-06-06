# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineAffineBatch7.py — p5 batch-7 (BG affine matrix 簇 0x15728..0x15924, 4 fn)
#   R3: data-equate TRIG_TABLE(0x09e399d0) -> resolve_word_equate (constants/ig2d_data.inc)
#   R2: 3 个 auto-name 槽改名 (muldi3 round 对 + assert-expr "0")
#   R5: 3 plate 过时 FUN_ caller 改现名
#   注: trig_table 表体 carve (从 .incbin 0x1E399CD+0x283 切出) 留专项 R7。
# Usage: tools\asm-regen\ghidra-run-script.bat RefineAffineBatch7.py [dry]
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
 (0x08015814, 0x09e399d0, 'TRIG_TABLE', 'compute_bg_affine_matrix_scaled_trig_table'),
]

# B. rename-only 槽 (slot_addr, slot_label)
RENAME_ONLY = [
 (0x08015818, 'compute_bg_affine_matrix_scaled_fix12_round_lo'),   # 0x800 = 64-bit 舍入加数低字
 (0x0801581c, 'compute_bg_affine_matrix_scaled_fix12_round_hi'),   # 0x0   = 高字
 (0x08015944, 'resolve_bg_affine_param_offset_assert_expr_zero'),  # -> "0" assert(0) 表达式串
]

# C. plate targeted (addr -> [(old, new), ...])
PLATE_REPL = {
 0x08015728: [
  (u"Called by FUN_08015820 and apply_bg_affine_by_angle_scale",
   u"Called by setup_oam_affine_matrix_from_scale and apply_bg_affine_by_angle_scale"),
 ],
 0x08015820: [
  (u"Called by FUN_080ee654", u"Called by alloc_affine_oam_entry_with_defaults"),
 ],
 0x08015868: [
  (u"Called by FUN_0801c668 (BG affine animation driver, indeg=1)",
   u"Called by apply_bg2_affine_fixed_angle (BG affine animation driver, indeg=1)"),
 ],
}


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _check(slot_int, want):
    d = getDataAt(_addr(slot_int))
    if d is None or d.getLength() != 4:
        return False, "no 4B data"
    if want is not None:
        try:
            dv = d.getValue()
            iv = (int(dv.getValue()) & 0xffffffff) if hasattr(dv, "getValue") else (int(dv) & 0xffffffff)
        except Exception:
            iv = None
        if iv is not None and iv != (want & 0xffffffff):
            return False, "value mismatch got=0x%x want=0x%x" % (iv, want)
    return True, None


def main():
    print("=== RefineAffineBatch7 (DRY=%s) ===" % DRY)
    et = currentProgram.getEquateTable()
    listing = currentProgram.getListing()
    nA = nB = nC = 0

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

    for slot_int, label in RENAME_ONLY:
        ok, err = _check(slot_int, None)
        if not ok:
            print("[B FAIL] 0x%08x: %s" % (slot_int, err)); continue
        if DRY:
            print("[B dry] 0x%08x rename %s" % (slot_int, label)); nB += 1; continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        print("[B ok] 0x%08x -> %s" % (slot_int, label)); nB += 1

    for addr_int in sorted(PLATE_REPL.keys()):
        cu = listing.getCodeUnitAt(_addr(addr_int))
        txt = cu.getComment(CodeUnit.PLATE_COMMENT) if cu else None
        if txt is None:
            print("[C FAIL] no plate @ 0x%08x" % addr_int); continue
        new = txt
        ok = True
        for old, rep in PLATE_REPL[addr_int]:
            if old not in new:
                print("[C FAIL] 0x%08x pattern not found: %r" % (addr_int, old[:40])); ok = False; continue
            new = new.replace(old, rep)
        if not ok or new == txt:
            continue
        if DRY:
            print("[C dry] 0x%08x plate update" % addr_int); nC += 1; continue
        cu.setComment(CodeUnit.PLATE_COMMENT, new)
        print("[C ok] 0x%08x plate updated" % addr_int); nC += 1

    print("[done] A=%d B=%d C=%d (DRY=%s)" % (nA, nB, nC, DRY))


main()
