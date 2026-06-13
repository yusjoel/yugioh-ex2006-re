# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF05Seg6PoolLabels.py -- fix literal pool labels in Seg-6 disassembled blocks
#
# After disassembling the two ROM_INCBIN blocks (0x4d294 and 0x4dd58),
# Ghidra groups some literal pool words into .byte blocks without individual labels.
# The exported asm references e.g. DAT_0804d2e8 but that label doesn't appear in output.
# Fix: clearListing + createData(DWordDataType) at each pool address so the exporter
# emits separate labeled .word lines.
#
# NOTE: createLabel alone is NOT sufficient -- Ghidra's exporter follows data type
# definitions, not just labels. We must also define each word as a DWORD data item.
from ghidra.program.model.symbol import SourceType
from ghidra.program.model.data import DWordDataType

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"): DRY = True
except Exception:
    pass


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


MISSING_POOL_LABELS = [
    (0x0804d2e8, 'DAT_0804d2e8'),
    (0x0804d2ec, 'DAT_0804d2ec'),
    (0x0804d360, 'DAT_0804d360'),
    (0x0804d3ac, 'DAT_0804d3ac'),
    (0x0804d444, 'DAT_0804d444'),
    (0x0804d448, 'DAT_0804d448'),
    (0x0804d44c, 'DAT_0804d44c'),
    (0x0804d450, 'DAT_0804d450'),
    (0x0804d454, 'DAT_0804d454'),
    (0x0804d520, 'DAT_0804d520'),
    (0x0804d524, 'DAT_0804d524'),
    (0x0804d528, 'DAT_0804d528'),
    (0x0804d52c, 'DAT_0804d52c'),
    (0x0804d530, 'DAT_0804d530'),
    (0x0804d544, 'DAT_0804d544'),
    (0x0804d60c, 'DAT_0804d60c'),
    (0x0804d610, 'DAT_0804d610'),
    (0x0804d614, 'DAT_0804d614'),
    (0x0804d618, 'DAT_0804d618'),
    (0x0804d61c, 'DAT_0804d61c'),
    (0x0804d630, 'DAT_0804d630'),
    (0x0804d680, 'DAT_0804d680'),
    (0x0804d684, 'DAT_0804d684'),
    (0x0804d688, 'DAT_0804d688'),
    (0x0804d68c, 'DAT_0804d68c'),
    (0x0804d690, 'DAT_0804d690'),
    (0x0804d720, 'DAT_0804d720'),
    (0x0804d724, 'DAT_0804d724'),
    (0x0804d728, 'DAT_0804d728'),
    (0x0804d72c, 'DAT_0804d72c'),
    (0x0804d730, 'DAT_0804d730'),
    (0x0804d734, 'DAT_0804d734'),
    (0x0804d798, 'DAT_0804d798'),
    (0x0804d79c, 'DAT_0804d79c'),
    (0x0804d7dc, 'DAT_0804d7dc'),
    (0x0804d858, 'DAT_0804d858'),
    (0x0804d85c, 'DAT_0804d85c'),
    (0x0804d860, 'DAT_0804d860'),
    (0x0804d864, 'DAT_0804d864'),
    (0x0804da18, 'DAT_0804da18'),
    (0x0804da1c, 'DAT_0804da1c'),
    (0x0804da20, 'DAT_0804da20'),
    (0x0804da24, 'DAT_0804da24'),
    (0x0804da28, 'DAT_0804da28'),
    (0x0804da2c, 'DAT_0804da2c'),
    (0x0804da30, 'DAT_0804da30'),
    (0x0804da34, 'DAT_0804da34'),
    (0x0804da80, 'DAT_0804da80'),
    (0x0804da84, 'DAT_0804da84'),
    (0x0804da88, 'DAT_0804da88'),
    (0x0804dae0, 'DAT_0804dae0'),
    (0x0804dae4, 'DAT_0804dae4'),
    (0x0804dd88, 'DAT_0804dd88'),
    (0x0804dd8c, 'DAT_0804dd8c'),
    (0x0804dda8, 'DAT_0804dda8'),
    (0x0804ddf4, 'DAT_0804ddf4'),
    (0x0804ddf8, 'DAT_0804ddf8'),
    (0x0804ddfc, 'DAT_0804ddfc'),
    (0x0804dea8, 'DAT_0804dea8'),
    (0x0804deac, 'DAT_0804deac'),
    (0x0804deb0, 'DAT_0804deb0'),
    (0x0804deb4, 'DAT_0804deb4'),
    (0x0804df30, 'DAT_0804df30'),
    (0x0804e074, 'DAT_0804e074'),
    (0x0804e078, 'DAT_0804e078'),
    (0x0804e07c, 'DAT_0804e07c'),
    (0x0804e1ec, 'DAT_0804e1ec'),
    (0x0804e1f0, 'DAT_0804e1f0'),
    (0x0804e1f4, 'DAT_0804e1f4'),
    (0x0804e1f8, 'DAT_0804e1f8'),
    (0x0804e1fc, 'DAT_0804e1fc'),
    (0x0804e200, 'DAT_0804e200'),
    (0x0804e204, 'DAT_0804e204'),
    (0x0804e220, 'DAT_0804e220'),
    (0x0804e230, 'DAT_0804e230'),
    (0x0804e264, 'DAT_0804e264'),
    (0x0804e6c8, 'DAT_0804e6c8'),
    (0x0804e6cc, 'DAT_0804e6cc'),
    (0x0804e8f8, 'DAT_0804e8f8'),
    (0x0804e8fc, 'DAT_0804e8fc'),
    (0x0804e944, 'DAT_0804e944'),
    (0x0804e948, 'DAT_0804e948'),
    (0x0804e94c, 'DAT_0804e94c'),
    (0x0804e9b0, 'DAT_0804e9b0'),
    (0x0804e9b4, 'DAT_0804e9b4'),
    (0x0804e9b8, 'DAT_0804e9b8'),
    (0x0804e9cc, 'DAT_0804e9cc'),
    (0x0804ea08, 'DAT_0804ea08'),
    (0x0804ea0c, 'DAT_0804ea0c'),
    (0x0804eb10, 'DAT_0804eb10'),
    (0x0804eb14, 'DAT_0804eb14'),
    (0x0804eb18, 'DAT_0804eb18'),
    (0x0804eb1c, 'DAT_0804eb1c'),
    (0x0804eb20, 'DAT_0804eb20'),
    (0x0804eb48, 'DAT_0804eb48'),
    (0x0804eb60, 'DAT_0804eb60'),
    (0x0804eb64, 'DAT_0804eb64'),
    (0x0804ee44, 'DAT_0804ee44'),
    (0x0804ee48, 'DAT_0804ee48'),
    (0x0804ee4c, 'DAT_0804ee4c'),
    (0x0804ee50, 'DAT_0804ee50'),
    (0x0804ee54, 'DAT_0804ee54'),
    (0x0804ee58, 'DAT_0804ee58'),
    (0x0804ee5c, 'DAT_0804ee5c'),
    (0x0804ee60, 'DAT_0804ee60'),
    (0x0804ee64, 'DAT_0804ee64'),
    (0x0804ee68, 'DAT_0804ee68'),
    (0x0804ee6c, 'DAT_0804ee6c'),
    (0x0804ee70, 'DAT_0804ee70'),
    (0x0804eebc, 'DAT_0804eebc'),
    (0x0804eec0, 'DAT_0804eec0'),
    (0x0804eedc, 'DAT_0804eedc'),
    (0x0804eee0, 'DAT_0804eee0'),
    (0x0804ef08, 'DAT_0804ef08'),
    (0x0804ef0c, 'DAT_0804ef0c'),
    (0x0804efbc, 'DAT_0804efbc'),
    (0x0804efc0, 'DAT_0804efc0'),
    (0x0804efc4, 'DAT_0804efc4'),
    (0x0804efc8, 'DAT_0804efc8'),
    (0x0804efcc, 'DAT_0804efcc'),
    (0x0804efd0, 'DAT_0804efd0'),
    (0x0804f030, 'DAT_0804f030'),
    (0x0804f034, 'DAT_0804f034'),
    (0x0804f038, 'DAT_0804f038'),
    (0x0804f064, 'DAT_0804f064'),
    (0x0804f068, 'DAT_0804f068'),
    (0x0804f06c, 'DAT_0804f06c'),
    (0x0804f094, 'DAT_0804f094'),
    # Region A secondary disasm literal pools (SUB_0804cca4/cd00/cd74 range)
    (0x0804ccc4, 'DAT_0804ccc4'),
    (0x0804ccc8, 'DAT_0804ccc8'),
    (0x0804ccdc, 'DAT_0804ccdc'),
    (0x0804cce0, 'DAT_0804cce0'),
    (0x0804cd4c, 'DAT_0804cd4c'),
    (0x0804cd6c, 'DAT_0804cd6c'),
    # Block 2 literal pools that decoded as THUMB (all = 0x0201c520, gDuelFieldSlots+0x10)
    (0x0804e41c, 'DAT_0804e41c'),
    (0x0804e4d0, 'DAT_0804e4d0'),
    (0x0804e604, 'DAT_0804e604'),
    (0x0804e77c, 'DAT_0804e77c'),
]


def main():
    print("=== RefineF05Seg6PoolLabels v2 (DRY=%s): %d entries ===" % (DRY, len(MISSING_POOL_LABELS)))
    listing = currentProgram.getListing()
    sm = currentProgram.getSymbolTable()
    dt = DWordDataType()
    ok = 0
    err = 0
    for addr_int, label in MISSING_POOL_LABELS:
        if DRY:
            print("[dry] clearListing+DWord+label 0x%08x %s" % (addr_int, label))
            ok += 1
            continue
        try:
            a = _addr(addr_int)
            a_end = _addr(addr_int + 3)
            # 1) clear the 4-byte range (breaks enclosing .byte block)
            clearListing(a, a_end)
            # 2) define as DWORD so exporter emits .word
            du = listing.createData(a, dt)
            if du is None:
                print("[warn] createData returned None @ 0x%08x" % addr_int)
            # 3) apply the label
            sm.createLabel(a, label, SourceType.USER_DEFINED)
            ok += 1
        except Exception as e:
            print("[err] 0x%08x %s: %s" % (addr_int, label, str(e)))
            err += 1
    print("=== DONE: ok=%d err=%d ===" % (ok, err))


main()
