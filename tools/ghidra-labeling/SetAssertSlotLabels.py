# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# SetAssertSlotLabels.py — 给断言串指针槽改名 + 加断言文本 EOL 注释
#   读 tools/ghidra-labeling/assert_slots.csv (slot_addr,slot_label,eol_text):
#     (1) createLabel(slot_addr, slot_label)  把 DAT_xxx -> ptr_<assertlabel>_<addrtail>
#     (2) setEOLComment(slot_addr, eol_text)  .word 行追加断言原文
#   (label 目标 + ref 已由 AddAssertStringLabels.py 建; 本脚本只处理槽侧。)
# Usage: tools\asm-regen\ghidra-run-script.bat SetAssertSlotLabels.py [dry]
import os
from ghidra.program.model.symbol import SourceType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def csv_path():
    try:
        d = os.path.dirname(str(getSourceFile().getAbsolutePath()))
        p = os.path.join(d, "assert_slots.csv")
        if os.path.exists(p):
            return p
    except Exception:
        pass
    return "assert_slots.csv"


def main():
    path = csv_path()
    print("=== SetAssertSlotLabels (DRY=%s) csv=%s ===" % (DRY, path))
    listing = currentProgram.getListing()
    rows = []
    f = open(path, "r")
    try:
        for line in f:
            line = line.rstrip("\n").rstrip("\r")
            if not line or line.startswith("slot_addr"):
                continue
            p = line.split(",", 2)
            if len(p) != 3:
                continue
            rows.append((int(p[0], 16), p[1], p[2]))
    finally:
        f.close()
    nl = ne = 0
    for slot_int, slot_label, eol in rows:
        a = _addr(slot_int)
        d = getDataAt(a)
        if d is None or d.getLength() != 4:
            print("[FAIL] no 4B data @ 0x%08x" % slot_int)
            continue
        if not DRY:
            # 重命名现有 user label (如旧 ptr_*) 为新 <func>_<assertlabel>; 无则新建
            sym = getSymbolAt(a)
            if sym is not None and sym.getSource() == SourceType.USER_DEFINED and not sym.isDynamic():
                if sym.getName() != slot_label:
                    sym.setName(slot_label, SourceType.USER_DEFINED)
            else:
                createLabel(a, slot_label, True, SourceType.USER_DEFINED)
            cu = listing.getCodeUnitAt(a)
            if cu is not None:
                cu.setComment(CodeUnit.EOL_COMMENT, eol)
        nl += 1
        ne += 1
    print("[done] renamed=%d eol=%d (DRY=%s)" % (nl, ne, DRY))


main()
