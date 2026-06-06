# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineGlStateBatch4.py — p5 batch-4 (GL palette/OAM manager 簇 0x1510c..0x1522c, 7 fn)
#   R2/R3: gGlState(0x02023490) USER label + 7 槽 DATA ref + 槽改名 <func>_ptr_gl_state
#   R1   : data-equate GL_STATE_INIT_FILL_CTRL / GL_PALRAM_FILL_CTRL / GL_PALENTRY_ZERO_CTRL
#          (constants/gl_state.inc .equ 解析回值)
#   R5   : 7 plate targeted (0x02023490->gGlState; alloc 计数器 0x02024330->0x02023d30 订正;
#          gl_state_init 0x22B B->0x8ac B; fill_gl_palram 0x200->0x400 字节单位订正)
# Usage: tools\asm-regen\ghidra-run-script.bat RefineGlStateBatch4.py [dry]
from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"): DRY = True
except Exception:
    pass

GL_STATE = 0x02023490

# A. gGlState 指针槽 (slot_addr, slot_label)
PTR_SLOTS = [
 (0x0801512c, 'get_gl_oam_entry_ptr_ptr_gl_state'),
 (0x08015154, 'gl_state_init_ptr_gl_state'),
 (0x08015190, 'init_gl_palette_slot_flags_ptr_gl_state'),
 (0x080151ac, 'fill_gl_palram_buf_0xf0_ptr_gl_state'),
 (0x080151d4, 'assign_palette_slot_entry_ptr_gl_state'),
 (0x080151f4, 'alloc_palette_entry_slot_ptr_gl_state'),
 (0x080152ac, 'copy_sprite_attr_table_to_oam_ptr_gl_state'),
]

# B. data-equate (slot_addr, value, const_name, slot_label)
EQ_SLOTS = [
 (0x08015158, 0x0500022b, 'GL_STATE_INIT_FILL_CTRL', 'gl_state_init_gl_state_init_fill_ctrl'),
 (0x080151b0, 0x05000100, 'GL_PALRAM_FILL_CTRL',     'fill_gl_palram_buf_0xf0_gl_palram_fill_ctrl'),
 (0x08015228, 0x05000002, 'GL_PALENTRY_ZERO_CTRL',   'alloc_palette_entry_slot_gl_palentry_zero_ctrl'),
]

# C. plate targeted (addr -> [(old, new), ...])
PLATE_REPL = {
 0x0801510c: [
  (u"base 0x02023490 + r0*0x20", u"base gGlState + r0*0x20"),
  (u"Returns: r0=u8* ptr (0x02023490 + slot_idx*0x20)", u"Returns: r0=u8* ptr (gGlState + slot_idx*0x20)"),
  (u"Constants: 0x02023490=GL state EWRAM base;", u"Constants: gGlState=0x02023490 GL state EWRAM base;"),
 ],
 0x08015138: [
  (u"state struct @ EWRAM 0x02023490 (0x22B B)", u"gGlState 结构 @ EWRAM 0x02023490 (0x8ac B = 0x22b 字)"),
 ],
 0x08015160: [
  (u"GL 调色板槽位标记区域 (EWRAM 0x02023490+0x880, 共 32 字节)", u"gGlState+0x880 调色板槽位标记区 (palette_map, 共 32 字节)"),
 ],
 0x08015194: [
  (u"bios_cpu_set fill 写入 EWRAM 0x02023490 起始 0x100 halfword (0x200 字节)",
   u"bios_cpu_set fill 写入 gGlState 起始 0x100 字 (0x400 字节)"),
  (u"Constants: 0x05000100 = bios_cpu_set 控制字 (bit24=1 fill, len=0x100 halfwords=0x200 bytes).",
   u"Constants: GL_PALRAM_FILL_CTRL=0x05000100 (bit24=fill, bit26=32-bit, len=0x100 字=0x400 字节)."),
 ],
 0x080151b4: [
  (u"Base 0x02023490: slot_record array at +0x800", u"Base gGlState (0x02023490): slot_record array at +0x800"),
 ],
 0x080151d8: [
  (u"Checks [0x02024330] signed byte (slot counter)", u"Checks [gGlState+0x8a0] (=0x02023d30) signed byte (slot counter)"),
  (u"[0x02024330] += 1", u"[gGlState+0x8a0] += 1"),
  (u"(CPUSET_CTRL=0x05000002)", u"(GL_PALENTRY_ZERO_CTRL=0x05000002)"),
 ],
 0x0801522c: [
  (u"from EWRAM sprite-attr array (0x02023490+0x880) to EWRAM OAM buffer (0x02023490+slot*8)",
   u"from gGlState+0x880 (palette_map sentinel list) to EWRAM OAM buffer (gGlState+slot*8)"),
  (u"all addresses computed internally from DAT_080152ac=0x02023490",
   u"all addresses computed internally from gGlState (0x02023490)"),
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
    print("=== RefineGlStateBatch4 (DRY=%s) ===" % DRY)
    et = currentProgram.getEquateTable()
    rm = currentProgram.getReferenceManager()
    listing = currentProgram.getListing()
    nA = nB = nC = 0

    if not DRY:
        createLabel(_addr(GL_STATE), "gGlState", True, SourceType.USER_DEFINED)
    for slot_int, label in PTR_SLOTS:
        ok, err = _check(slot_int, GL_STATE)
        if not ok:
            print("[A FAIL] 0x%08x: %s" % (slot_int, err)); continue
        if DRY:
            print("[A dry] 0x%08x ref->gGlState rename %s" % (slot_int, label)); nA += 1; continue
        ref = rm.addMemoryReference(_addr(slot_int), _addr(GL_STATE), RefType.DATA, SourceType.USER_DEFINED, 0)
        rm.setPrimary(ref, True)
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        print("[A ok] 0x%08x -> %s" % (slot_int, label)); nA += 1

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
