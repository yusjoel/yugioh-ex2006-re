# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineSeg5c-i: apply_gfx_resource_list(0x16a7c) + resolve_prhlist_entry_name_ptr(0x16afc)
#   + dispatch_jp_char_handler(0x16b68) 槽符号化 (不含 R4 disasm, 留 Seg-5c-ii)
from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"): DRY = True
except Exception:
    pass

# A. equate (reuse g2d_tags.inc FourCC)
EQ_SLOTS = [
 (0x08016aac, 0x54444742, 'BGDT_TAG', 'apply_gfx_resource_list_bgdt_tag'),
 (0x08016ab0, 0x444a424f, 'OBJD_TAG', 'apply_gfx_resource_list_objd_tag'),
 (0x08016acc, 0x544c4150, 'PALT_TAG', 'apply_gfx_resource_list_palt_tag'),
]

# B. carve/global ref (slot, target, gas_label, slot_label)  — jump table base ptr
REF_SLOTS = [
 (0x08016b84, 0x08016b88, 'jp_char_handler_jump_table', 'dispatch_jp_char_handler_ptr_jump_table'),
]

# C. plain rename (slot, label, eol)
RENAME_SLOTS = [
 (0x08016b48, 'resolve_prhlist_entry_name_ptr_nameid_offset',     '= 0x201; pDst[+0x201] u8 nameID'),
 (0x08016b54, 'resolve_prhlist_entry_name_ptr_game_str_id_base',  '= 0x1072; nameID + 0x1072 -> game_str id for game_str_id_to_row'),
 (0x08016b5c, 'resolve_prhlist_entry_name_ptr_ewram_base',        None),
 (0x08016b60, 'resolve_prhlist_entry_name_ptr_gsettings_offset',  '= gSettings(0x02006c2c) - EWRAM base; bits[2:0]=language_id selects str slot'),
 (0x08016b80, 'dispatch_jp_char_handler_neg_char_base',           '= -0x8148 (two-complement); r1 = sjis_code - 0x8148 (zone-2 base)'),
 (0x08016b88, 'jp_char_handler_jump_table',                       '339-entry (0x153) SJIS code->handler dispatch table; targets 0x170d4..0x171d0 stubs (each movs r0,#idx; b ret)'),
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
    print("=== RefineSeg5cSlots (DRY=%s) ===" % DRY)
    rm = currentProgram.getReferenceManager()
    et = currentProgram.getEquateTable()
    listing = currentProgram.getListing()
    nA = nB = nC = 0
    made = set()

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

    for slot_int, tgt_int, gas_label, slot_label in REF_SLOTS:
        d = getDataAt(_addr(slot_int))
        if d is None or d.getLength() != 4:
            print("[B FAIL] no 4B data @ 0x%08x" % slot_int); continue
        if DRY:
            print("[B dry] 0x%08x ref->%s rename %s" % (slot_int, gas_label, slot_label)); nB += 1; continue
        if tgt_int not in made:
            createLabel(_addr(tgt_int), gas_label, True, SourceType.USER_DEFINED); made.add(tgt_int)
        ref = rm.addMemoryReference(_addr(slot_int), _addr(tgt_int), RefType.DATA, SourceType.USER_DEFINED, 0)
        rm.setPrimary(ref, True)
        createLabel(_addr(slot_int), slot_label, True, SourceType.USER_DEFINED)
        print("[B ok] 0x%08x -> %s" % (slot_int, slot_label)); nB += 1

    for slot_int, label, eol in RENAME_SLOTS:
        d = getDataAt(_addr(slot_int))
        if d is None or d.getLength() != 4:
            print("[C FAIL] no 4B data @ 0x%08x" % slot_int); continue
        if DRY:
            print("[C dry] 0x%08x rename %s" % (slot_int, label)); nC += 1; continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        if eol:
            listing.getCodeUnitAt(_addr(slot_int)).setComment(CodeUnit.EOL_COMMENT, eol)
        print("[C ok] 0x%08x -> %s" % (slot_int, label)); nC += 1

    print("[done] A=%d B=%d C=%d (DRY=%s)" % (nA, nB, nC, DRY))


main()
