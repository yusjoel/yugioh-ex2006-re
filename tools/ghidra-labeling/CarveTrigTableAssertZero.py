# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# CarveTrigTableAssertZero.py — batch-7 续: 把 2 个 ROM 数据 carve 出来并切换为 GAS label 引用
#   (1) trig_table @0x09e399d0: 槽 0x08015814 从 data-equate TRIG_TABLE 切换为 label ref
#       (rom.s 已 carve 256 .hword + trig_table 标签); 删 TRIG_TABLE equate -> 单一命名源
#   (2) assert_expr_zero @0x09e3a4f8 ("0"): 槽 0x08015944 加 label + DATA ref
#       (rom.s 已 carve .asciz "0")
# Usage: tools\asm-regen\ghidra-run-script.bat CarveTrigTableAssertZero.py [dry]
from ghidra.program.model.symbol import SourceType, RefType

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"): DRY = True
except Exception:
    pass

# (slot_addr, target_addr, gas_label, old_equate_name_or_None)
SWITCH = [
 (0x08015814, 0x09e399d0, 'trig_table',       'TRIG_TABLE'),
 (0x08015944, 0x09e3a4f8, 'assert_expr_zero', None),
]


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def main():
    print("=== CarveTrigTableAssertZero (DRY=%s) ===" % DRY)
    et = currentProgram.getEquateTable()
    rm = currentProgram.getReferenceManager()
    n = 0
    for slot_int, tgt_int, label, oldeq in SWITCH:
        d = getDataAt(_addr(slot_int))
        if d is None or d.getLength() != 4:
            print("[FAIL] no 4B data @ slot 0x%08x" % slot_int); continue
        if DRY:
            print("[dry] slot 0x%08x .word -> label %s @0x%08x (del eq %s)" % (slot_int, label, tgt_int, oldeq)); n += 1; continue
        # 1. 目标 label
        createLabel(_addr(tgt_int), label, True, SourceType.USER_DEFINED)
        # 2. 代码槽 DATA ref -> 目标 (primary)
        ref = rm.addMemoryReference(_addr(slot_int), _addr(tgt_int), RefType.DATA, SourceType.USER_DEFINED, 0)
        rm.setPrimary(ref, True)
        # 3. 删旧 equate (若有)
        if oldeq is not None:
            eq = et.getEquate(oldeq)
            if eq is not None:
                try: eq.removeReference(_addr(slot_int), 0)
                except Exception as e: print("  [warn] removeReference %s: %s" % (oldeq, e))
                try:
                    if eq.getReferenceCount() == 0: et.removeEquate(oldeq)
                except Exception: pass
        print("[ok] 0x%08x -> %s" % (slot_int, label)); n += 1
    print("[done] %d (DRY=%s)" % (n, DRY))


main()
