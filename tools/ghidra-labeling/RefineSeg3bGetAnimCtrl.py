# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineSeg3bGetAnimCtrl.py — p5 Seg-3b (R5 plate stale-DWORD fix)
#   get_anim_ctrl_seq_id (0x156f4): plate 仍引旧 DWORD_08015710/14 (槽已改名), 订正为现名
from ghidra.program.model.listing import CodeUnit

PLATE_REPL = {
 0x080156f4: [
  (u"- DWORD_08015710 = 0x09e3a488 (source file string)",
   u"- get_anim_ctrl_seq_id_ig2d_main_c_filename = ig2d_main_c_filename (GL/IG2D_Main.c)"),
  (u"- DWORD_08015714 = 0x09e3a4d8 (condition string)",
   u"- get_anim_ctrl_seq_id_assert_psequence = assert_psequence (pSequence)"),
 ],
}


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def main():
    listing = currentProgram.getListing()
    n = 0
    for addr_int in sorted(PLATE_REPL.keys()):
        cu = listing.getCodeUnitAt(_addr(addr_int))
        txt = cu.getComment(CodeUnit.PLATE_COMMENT) if cu else None
        if txt is None:
            print("[FAIL] no plate @ 0x%08x" % addr_int); continue
        new = txt
        ok = True
        for old, rep in PLATE_REPL[addr_int]:
            if old not in new:
                print("[FAIL] 0x%08x pattern not found: %r" % (addr_int, old[:40])); ok = False; continue
            new = new.replace(old, rep)
        if not ok or new == txt: continue
        cu.setComment(CodeUnit.PLATE_COMMENT, new)
        print("[ok] 0x%08x plate repl" % addr_int); n += 1
    print("[done] %d" % n)


main()
