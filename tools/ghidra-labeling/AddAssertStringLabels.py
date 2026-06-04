# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# AddAssertStringLabels.py — 给 NNS/GL SDK 断言串建 USER_DEFINED label + 代码槽加 DATA ref
#   读 tools/ghidra-labeling/assert_labels.csv (slot_addr,string_addr,label,is_new):
#     is_new=1: createLabel(string_addr,label) [每串一次] + addMemoryReference(slot->string)
#     is_new=0: 已在 rom_data.inc, 跳过 (既有 label + ref 已解析)
#   随后 ExportRomLabelsToInc.py 把新 label 写入 constants/rom_data.inc; 重导出后代码
#   .word 经 resolve_word_symbol 显示 label 名 -> byte-identical (项目既定 ROM 数据符号模式)。
# Usage: tools\asm-regen\ghidra-run-script.bat AddAssertStringLabels.py [dry]
import os
from ghidra.program.model.symbol import SourceType, RefType

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
        p = os.path.join(d, "assert_labels.csv")
        if os.path.exists(p):
            return p
    except Exception:
        pass
    return "assert_labels.csv"


def main():
    path = csv_path()
    print("=== AddAssertStringLabels (DRY=%s) csv=%s ===" % (DRY, path))
    rows = []
    f = open(path, "r")
    try:
        for line in f:
            line = line.strip()
            if not line or line.startswith("slot_addr"):
                continue
            p = line.split(",")
            if len(p) != 4:
                continue
            rows.append((int(p[0], 16), int(p[1], 16), p[2], p[3] == "1"))
    finally:
        f.close()

    rm = currentProgram.getReferenceManager()
    new_strs = {}
    for slot, s, lab, isnew in rows:
        if isnew:
            new_strs[s] = lab
    nlbl = nref = 0
    # 1. 建 label (每个新串一次)
    for s, lab in sorted(new_strs.items()):
        if not DRY:
            createLabel(_addr(s), lab, True, SourceType.USER_DEFINED)
        nlbl += 1
    # 2. 代码槽加 DATA ref (仅 is_new)
    for slot, s, lab, isnew in rows:
        if not isnew:
            continue
        if not DRY:
            ref = rm.addMemoryReference(_addr(slot), _addr(s), RefType.DATA, SourceType.USER_DEFINED, 0)
            rm.setPrimary(ref, True)
        nref += 1
    print("[done] labels=%d refs=%d (DRY=%s)" % (nlbl, nref, DRY))


main()
