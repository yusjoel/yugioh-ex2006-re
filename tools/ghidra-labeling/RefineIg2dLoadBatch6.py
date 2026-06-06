# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineIg2dLoadBatch6.py — p5 batch-6 (NNS IG2D 资源加载管理器 globals + allocators)
#   R3: 6 个 IG2D 全局符号化 (iwram.inc/ewram.inc) + 9 槽 DATA ref + 槽改名
#       gIg2dUsedCellAnm(0x03000bf8) gIg2dUsedNceBuff(bfc) gIg2dUsedNanBuff(c00)
#       gIg2dNceBuffBase(c08) gIg2dCharPoolBase(0x03002c08) gIg2dCellAnmBank(0x02027d40)
#   rename: gl_clear_frame_callbacks(0x080156ac) -> reset_ig2d_load_counters
#           (误名: 实清 3 个 IG2D used-count 计数器, 非帧回调)
#   R5: 4 cluster plate (alloc_*) 地址->g名 + 自身 plate 重写 + 5 external plate 改名
# Usage: tools\asm-regen\ghidra-run-script.bat RefineIg2dLoadBatch6.py [dry]
from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"): DRY = True
except Exception:
    pass

# A. global label + ref + slot rename (slot_addr, global_addr, global_name, slot_label)
REF_SLOTS = [
 (0x08015664, 0x03000bfc, 'gIg2dUsedNceBuff',  'alloc_nce_buff_slot_ptr_used_nce_buff'),
 (0x080156c0, 0x03000bfc, 'gIg2dUsedNceBuff',  'reset_ig2d_load_counters_ptr_used_nce_buff'),
 (0x0801569c, 0x03000c00, 'gIg2dUsedNanBuff',  'alloc_char_data_slot_ptr_used_nan_buff'),
 (0x080156c4, 0x03000c00, 'gIg2dUsedNanBuff',  'reset_ig2d_load_counters_ptr_used_nan_buff'),
 (0x080156bc, 0x03000bf8, 'gIg2dUsedCellAnm',  'reset_ig2d_load_counters_ptr_used_cell_anm'),
 (0x08015af0, 0x03000bf8, 'gIg2dUsedCellAnm',  'alloc_cell_anim_slot_ptr_used_cell_anm'),
 (0x08015670, 0x03000c08, 'gIg2dNceBuffBase',  'alloc_nce_buff_slot_ptr_nce_buff_base'),
 (0x080156a8, 0x03002c08, 'gIg2dCharPoolBase', 'alloc_char_data_slot_ptr_char_pool_base'),
 (0x08015b00, 0x02027d40, 'gIg2dCellAnmBank',  'alloc_cell_anim_slot_ptr_cell_anm_bank'),
]

# B. function rename
FUNC_RENAME = [(0x080156ac, 'reset_ig2d_load_counters')]

# C1. full plate replace (own plate)
PLATE_FULL = {
 0x080156ac: (
  u"GL/IG2D: 复位 IG2D 资源加载计数器——把 gIg2dUsedCellAnm/gIg2dUsedNceBuff/gIg2dUsedNanBuff "
  u"(0x03000bf8/bfc/c00) 三个 used-count 写 0, 释放所有已加载 G2D 资源槽 (NCE/NAN/CellAnm 缓冲)。"
  u"无参 (void); 叶子。被 reset_display_and_gl_state 等 6 个场景重置入口调用 (indeg=6)。"
  u"注: 旧名 gl_clear_frame_callbacks 系误名 (清的是计数器, 非帧回调)。"
 ),
}

# C2. targeted plate replace (addr -> [(old, new), ...])
PLATE_REPL = {
 # cluster: alloc_nce_buff_slot
 0x0801563c: [
  (u"[0x03000BFC]", u"gIg2dUsedNceBuff"),
  (u"[0x03000C08]", u"gIg2dNceBuffBase"),
 ],
 # cluster: alloc_char_data_slot
 0x08015674: [
  (u"[0x03000c00]", u"gIg2dUsedNanBuff"),
  (u"[0x03002c08]", u"gIg2dCharPoolBase"),
 ],
 # cluster: alloc_cell_anim_slot
 0x08015ac4: [
  (u"[0x03000BF8]", u"gIg2dUsedCellAnm"),
  (u"CellAnmBank + counter*0x54", u"gIg2dCellAnmBank + counter*0x54"),
  (u"CellAnmBank=0x02027D40", u"CellAnmBank=gIg2dCellAnmBank"),
 ],
 # cluster: load_nanr_anim_bank_from_file
 0x08015b70: [
  (u"([0x03000c00] +1)", u"(gIg2dUsedNanBuff +1)"),
 ],
 # external callers: rename token + phrase fixes
 0x08013510: [
  (u"gl_clear_frame_callbacks 清空帧回调队列", u"reset_ig2d_load_counters 复位 IG2D 资源加载计数器"),
 ],
 0x08019660: [
  (u"gl_clear_frame_callbacks", u"reset_ig2d_load_counters"),
 ],
 0x0801b7e8: [
  (u"gl_clear_frame_callbacks", u"reset_ig2d_load_counters"),
 ],
 0x0801c2ac: [
  (u"gl_clear_frame_callbacks", u"reset_ig2d_load_counters"),
  (u"GL state/callbacks reset", u"GL state reset + IG2D load counters reset"),
 ],
 0x080fd2f0: [
  (u"gl_clear_frame_callbacks to clear frame callback list", u"reset_ig2d_load_counters to reset IG2D load counters"),
 ],
}


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _check(slot_int, want):
    d = getDataAt(_addr(slot_int))
    if d is None or d.getLength() != 4:
        return False, "no 4B data"
    return True, None


def main():
    print("=== RefineIg2dLoadBatch6 (DRY=%s) ===" % DRY)
    rm = currentProgram.getReferenceManager()
    listing = currentProgram.getListing()
    nA = nB = nC = 0
    made = set()

    for slot_int, gaddr, gname, label in REF_SLOTS:
        ok, err = _check(slot_int, gaddr)
        if not ok:
            print("[A FAIL] 0x%08x: %s" % (slot_int, err)); continue
        if DRY:
            print("[A dry] 0x%08x ref->%s rename %s" % (slot_int, gname, label)); nA += 1; continue
        if gaddr not in made:
            createLabel(_addr(gaddr), gname, True, SourceType.USER_DEFINED)
            made.add(gaddr)
        ref = rm.addMemoryReference(_addr(slot_int), _addr(gaddr), RefType.DATA, SourceType.USER_DEFINED, 0)
        rm.setPrimary(ref, True)
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        print("[A ok] 0x%08x -> %s (%s)" % (slot_int, label, gname)); nA += 1

    for fn_int, newname in FUNC_RENAME:
        fn = getFunctionAt(_addr(fn_int))
        if fn is None:
            print("[B FAIL] no function @ 0x%08x" % fn_int); continue
        old = fn.getName()
        if DRY:
            print("[B dry] 0x%08x %s -> %s" % (fn_int, old, newname)); nB += 1; continue
        fn.setName(newname, SourceType.USER_DEFINED)
        print("[B ok] 0x%08x %s -> %s" % (fn_int, old, newname)); nB += 1

    for addr_int, newtxt in sorted(PLATE_FULL.items()):
        cu = listing.getCodeUnitAt(_addr(addr_int))
        if cu is None:
            print("[C FAIL] no code unit @ 0x%08x" % addr_int); continue
        if DRY:
            print("[C dry] 0x%08x full plate" % addr_int); nC += 1; continue
        cu.setComment(CodeUnit.PLATE_COMMENT, newtxt)
        print("[C ok] 0x%08x full plate" % addr_int); nC += 1

    for addr_int in sorted(PLATE_REPL.keys()):
        cu = listing.getCodeUnitAt(_addr(addr_int))
        txt = cu.getComment(CodeUnit.PLATE_COMMENT) if cu else None
        if txt is None:
            print("[C FAIL] no plate @ 0x%08x" % addr_int); continue
        new = txt
        ok = True
        for old, rep in PLATE_REPL[addr_int]:
            if old not in new:
                print("[C FAIL] 0x%08x pattern not found: %r" % (addr_int, old[:36])); ok = False; continue
            new = new.replace(old, rep)
        if not ok or new == txt:
            continue
        if DRY:
            print("[C dry] 0x%08x plate update (%d repl)" % (addr_int, len(PLATE_REPL[addr_int]))); nC += 1; continue
        cu.setComment(CodeUnit.PLATE_COMMENT, new)
        print("[C ok] 0x%08x plate updated" % addr_int); nC += 1

    print("[done] A=%d B=%d C=%d (DRY=%s)" % (nA, nB, nC, DRY))


main()
