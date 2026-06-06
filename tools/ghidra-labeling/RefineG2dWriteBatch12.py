# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineG2dWriteBatch12.py — p5 batch-12 (NNS G2D 写族前 2 fn 0x1626c..0x16342)
#   write_palt_block_to_vram (0x1626c) + dispatch_bg_screen_map_write (0x162dc)
#   R1/R3: OBJ_PALRAM_BASE=0x05000200 (gba_mem.inc, batch-11 已建) for 0x162bc slot
#   R2   : 0x162fc (0xfff00000 raw-addr 判别掩码) 槽改名
#   R5   : write_palt plate 的 0x05000000/0x05000200 散文 → GBA_PALRAM_BASE/OBJ_PALRAM_BASE
#   注: write_tile_region_to_bg_screen (0x16344, med-conf, struct 字段待 runtime) defer。
#        BG palette base 0x05000000 由 movs+lsls 内联 (0xa0<<0x13) 无 pool 槽不符号化。
# Usage: tools\asm-regen\ghidra-run-script.bat RefineG2dWriteBatch12.py [dry]
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
 (0x080162bc, 0x05000200, 'OBJ_PALRAM_BASE', 'write_palt_block_to_vram_obj_palram_base'),
]

# B. plain slot rename (slot_addr, slot_label)
RENAME_SLOTS = [
 (0x080162fc, 'dispatch_bg_screen_map_write_raw_addr_mask'),  # 0xfff00000: 测 dst 高位判 raw-addr/offset
]

# C. plate targeted (addr -> [(old, new), ...])
PLATE_REPL = {
 0x0801626c: [
  (u"type: 0-3 -> BG palette 0x05000000; type 4 -> OBJ palette 0x05000200",
   u"type: 0-3 -> BG palette GBA_PALRAM_BASE (0x05000000); type 4 -> OBJ palette OBJ_PALRAM_BASE (0x05000200)"),
  (u"Constants: 0x05000000 = BG palette VRAM base; 0x05000200 = OBJ palette VRAM base.",
   u"Constants: GBA_PALRAM_BASE (0x05000000) = BG palette VRAM base; OBJ_PALRAM_BASE (0x05000200) = OBJ palette VRAM base."),
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
    print("=== RefineG2dWriteBatch12 (DRY=%s) ===" % DRY)
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
