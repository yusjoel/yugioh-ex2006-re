# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# LabelCardDescriptions.py  (Jython 2.7 / Ghidra script)
#
# Label card description data area:
#   - card_desc_table      @ 0x09800000 (39 cards x 6 langs description text)
#   - card_desc_data       @ 0x0980A50C (u32 data table)
#   - card_desc_ptr_table  @ 0x09816580 (269 file offset pointers)

from ghidra.program.model.symbol import SourceType

RUN_DRY = False
try:
    _args = list(getScriptArgs())
    if _args and _args[0].lower() in ("dry", "--dry", "1", "true"):
        RUN_DRY = True
except Exception:
    pass

LABELS = [
    (0x09800000, "card_desc_table"),
    (0x0980A50C, "card_desc_data"),
    (0x09816580, "card_desc_ptr_table"),
]


def set_label(gba_addr, name):
    st = currentProgram.getSymbolTable()
    addr = toAddr(gba_addr)

    existing = st.getSymbols(name)
    for s in existing:
        if s.getAddress().equals(addr):
            print("[skip] %s @ %s (already exists)" % (name, addr))
            return True

    if RUN_DRY:
        print("[dry] %s @ 0x%08X" % (name, gba_addr))
        return True

    try:
        st.createLabel(addr, name, SourceType.USER_DEFINED)
        print("[ok] %s @ 0x%08X" % (name, gba_addr))
        return True
    except Exception as e:
        print("[fail] %s @ 0x%08X: %s" % (name, gba_addr, e))
        return False


def main():
    ok = 0
    for gba_addr, name in LABELS:
        if set_label(gba_addr, name):
            ok += 1
    print("[done] LabelCardDescriptions: %d/%d" % (ok, len(LABELS)))


main()
