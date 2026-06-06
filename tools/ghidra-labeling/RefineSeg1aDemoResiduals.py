# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineSeg1aDemoResiduals.py — p5 Seg-1a (b1 残留 3 defer 槽, demo scene)
#   #1 setup_demo_sprite_entry (0x13578) ROM 区域/语言检测 3 槽:
#      0x13674(0x080000ae)->ROM_REGION_CODE_ADDR equate / 0x13678(0x02000000)+0x1367c(0x6c2c) 改名
#      + plate R5 订正 (误称 "JP BIOS" -> ROM game-code 区域 + gSettings language_id)
#   #2 setup_demo_cell_anim_slot (0x13a6c) assert 行号槽 0x13ab8(0x14b) 改名
#   #3 tick_demo_scene_state_machine (0x13bd4) 状态机跳转表基址槽 0x13c00 改名 + DATA ref->表 0x13c04
# Usage: tools\asm-regen\ghidra-run-script.bat RefineSeg1aDemoResiduals.py [dry]
from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"): DRY = True
except Exception:
    pass

# A. data-equate (slot_addr, value, const_name, slot_label)
EQ_SLOTS = [
 (0x08013674, 0x080000ae, 'ROM_REGION_CODE_ADDR', 'setup_demo_sprite_entry_rom_region_code_addr'),
]

# B. plain slot rename (slot_addr, slot_label, eol_or_None)
RENAME_SLOTS = [
 (0x08013678, 'setup_demo_sprite_entry_ewram_base', None),
 (0x0801367c, 'setup_demo_sprite_entry_gsettings_offset', '= gSettings(0x02006c2c) - EWRAM base; bits[2:0]=language_id'),
 (0x08013ab8, 'setup_demo_cell_anim_slot_assert_line_14b', None),
 (0x08013c00, 'tick_demo_scene_state_machine_state_jump_table_ptr', '-> 10-case state dispatch table @0x08013c04'),
]

# C. DATA ref (slot_addr, target_addr) — resolve jump-table base ptr to the switch table label
REF_TO = [
 (0x08013c00, 0x08013c04),
]

# D. plate targeted (addr -> [(old, new), ...])
PLATE_REPL = {
 0x08013578: [
  (u"Detects JP BIOS version byte [0x080000ae]>>8 == 0x4a and adjusts tile offset +0x38.",
   u"Region/language gate: game-code byte [ROM_REGION_CODE_ADDR (0x080000ae)]>>8 == 0x4a ('J') = JP build; if JP and gSettings (0x02006c2c) language_id (bits[2:0]) == 0, skip; otherwise for slot in {0,1,3} adjust 2 OAM char codes by +0x38."),
  (u"Constants: OAM_BIOS_JP_MASK=0x4a / ATTR1_X_MASK=0x7f / ATTR0_PAL_MASK=0xf.",
   u"Constants: ROM_REGION_CODE_ADDR=0x080000ae / REGION_CODE_JP=0x4a / gSettings=0x02006c2c (bits[2:0]=language_id) / CHAR_CODE_ADJUST=0x38 / ATTR1_X_MASK=0x7f / ATTR0_PAL_MASK=0xf."),
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
    print("=== RefineSeg1aDemoResiduals (DRY=%s) ===" % DRY)
    rm = currentProgram.getReferenceManager()
    et = currentProgram.getEquateTable()
    listing = currentProgram.getListing()
    nA = nB = nC = nD = 0

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
            print("[B dry] 0x%08x rename %s%s" % (slot_int, label, " +EOL" if eol else "")); nB += 1; continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        if eol:
            listing.getCodeUnitAt(_addr(slot_int)).setComment(CodeUnit.EOL_COMMENT, eol)
        print("[B ok] 0x%08x -> %s" % (slot_int, label)); nB += 1

    for slot_int, tgt_int in REF_TO:
        if DRY:
            print("[C dry] 0x%08x DATA ref -> 0x%08x" % (slot_int, tgt_int)); nC += 1; continue
        ref = rm.addMemoryReference(_addr(slot_int), _addr(tgt_int), RefType.DATA, SourceType.USER_DEFINED, 0)
        rm.setPrimary(ref, True)
        print("[C ok] 0x%08x DATA ref -> 0x%08x" % (slot_int, tgt_int)); nC += 1

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
