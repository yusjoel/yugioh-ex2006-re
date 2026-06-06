# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineIg2dLoadBatch11.py — p5 batch-11 (NNS IG2D 资源加载族 0x15b04..0x15e72, 7 fn)
#   load_nce_cell_bank/load_nanr_anim_bank/load_ncgr_char_data/load_nclr_pltt_data_from_file
#   + copy_pltt_data_to_vram_proxy + load_g2d_obj_resource_set (invoke_fs_load 已干净)
#   R1/R3: OBJ_PALRAM_BASE=0x05000200 (gba_mem.inc) for copy_pltt slot 0x15ce4
#   R2   : 16 个 assert-line DAT_ 槽 → <func>_assert_line_<hexlineno> (避碰撞)
#   R5   : copy_pltt_data_to_vram_proxy plate 的 0x05000200 散文 → OBJ_PALRAM_BASE
# Usage: tools\asm-regen\ghidra-run-script.bat RefineIg2dLoadBatch11.py [dry]
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
 (0x08015ce4, 0x05000200, 'OBJ_PALRAM_BASE',
  'copy_pltt_data_to_vram_proxy_obj_palram_base'),
]

# B. plain slot rename — assert line-number 槽 (slot_addr, slot_label)
RENAME_SLOTS = [
 (0x08015b60, 'load_nce_cell_bank_from_file_assert_line_199'),   # 0x199=409 pFname
 (0x08015bbc, 'load_nanr_anim_bank_from_file_assert_line_1c1'),  # 0x1c1=449 ppAnimBank
 (0x08015c18, 'load_ncgr_char_data_from_file_assert_line_23e'),  # 0x23e=574 ppCharData
 (0x08015c20, 'load_ncgr_char_data_from_file_assert_line_23f'),  # 0x23f=575 pFname
 (0x08015c78, 'load_nclr_pltt_data_from_file_assert_line_266'),  # 0x266=614 ppPltData
 (0x08015c80, 'load_nclr_pltt_data_from_file_assert_line_267'),  # 0x267=615 pFname
 (0x08015cd4, 'copy_pltt_data_to_vram_proxy_assert_line_2d9'),   # 0x2d9=729 pSrcData
 (0x08015cdc, 'copy_pltt_data_to_vram_proxy_assert_line_2da'),   # 0x2da=730 pPltProxt
 (0x08015d10, 'copy_pltt_data_to_vram_proxy_assert_line_2e3'),   # 0x2e3=739 FALSE
 (0x08015e78, 'load_g2d_obj_resource_set_assert_line_32d'),      # 0x32d=813 pBuf (nce)
 (0x08015e80, 'load_g2d_obj_resource_set_assert_line_331'),      # 0x331=817 pBuf (nanr)
 (0x08015e84, 'load_g2d_obj_resource_set_assert_line_33a'),      # 0x33a=826 numSequences!=0
 (0x08015e8c, 'load_g2d_obj_resource_set_assert_line_33f'),      # 0x33f=831 *ppCellAnim
 (0x08015e94, 'load_g2d_obj_resource_set_assert_line_341'),      # 0x341=833 pSequenceArrayHead
 (0x08015e9c, 'load_g2d_obj_resource_set_assert_line_355'),      # 0x355=853 pBuf (ncgr)
 (0x08015ea0, 'load_g2d_obj_resource_set_assert_line_36a'),      # 0x36a=874 pBuf (nclr)
]

# C. plate targeted (addr -> [(old, new), ...])
PLATE_REPL = {
 0x08015c90: [
  (u"added to OBJ palette base 0x05000200",
   u"added to OBJ palette base OBJ_PALRAM_BASE (0x05000200)"),
  (u"OBJ VRAM at 0x05000200+offset",
   u"OBJ VRAM at OBJ_PALRAM_BASE (0x05000200)+offset"),
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
    print("=== RefineIg2dLoadBatch11 (DRY=%s) ===" % DRY)
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

    for slot_int, label in RENAME_SLOTS:
        d = getDataAt(_addr(slot_int))
        if d is None or d.getLength() != 4:
            print("[B FAIL] no 4B data @ 0x%08x" % slot_int); continue
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
            print("[C dry] 0x%08x plate update (%d repl)" % (addr_int, len(PLATE_REPL[addr_int]))); nC += 1; continue
        cu.setComment(CodeUnit.PLATE_COMMENT, new)
        print("[C ok] 0x%08x plate updated" % addr_int); nC += 1

    print("[done] A=%d B=%d C=%d (DRY=%s)" % (nA, nB, nC, DRY))


main()
