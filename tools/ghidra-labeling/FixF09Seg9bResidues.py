# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixF09Seg9bResidues.py -- Fix residue ROM_INCBIN blocks in Seg-9b B6/B7
#
# After DisassembleF09Seg9bBlocks.py, 3 ROM_INCBIN residues remain in [0x77c50, 0x7850c):
#
#   ROM_INCBIN 0x77eec, 0x2c   @ LAB_08077eec  (B6 fn_eligible body: conditional branch target)
#   ROM_INCBIN 0x77fae, 0x1e   @ LAB_08077fae  (B7 sub-stubs: shared branch target)
#   ROM_INCBIN 0x77fd0, 0x20   @ LAB_08077fd0  (B7 sub-stubs: shared branch target)
#
# Root cause: DisassembleCommand(start, range, True) stops at unconditional branch.
# Shared sub-blocks reached by conditional branches are not auto-disassembled.
# These are valid THUMB code that Ghidra didn't follow because disasm started at
# each stub entry and stopped before reaching these conditional targets.
#
# Fix: DisassembleCommand at each residue block start (within already-set TMode range).
# No clearListing needed (those ranges are already clear from prior clearListing pass).
# No pool force_dword needed (pool words in these ranges were already handled).
#
# Residue details:
#   0x08077eec/0x2c: B6 fn body after literal pool word at 0x08077ee8:
#     0x08077eec: THUMB code (bgt target in fn_eligible body; jump-table-like dispatch)
#     End: 0x08077f17 (just before pool at 0x08077f18)
#   0x08077fae/0x1e: B7 sub body (beq target from sub_7f44/7f56 dispatches):
#     0x08077fae: THUMB code
#     End: 0x08077fcb (just before pool word at 0x08077fcc)
#   0x08077fd0/0x20: B7 sub body (beq target from sub_7f44/7f56 dispatches):
#     0x08077fd0: THUMB code
#     End: 0x08077fef (just before pool at 0x08077ff0)

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.address import AddressSet
from java.math import BigInteger

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

# (start_addr, end_addr, label_at_start, note)
RESIDUE_BLOCKS = [
    (0x08077eec, 0x08077f17, 'LAB_08077eec',
     'B6 fn_eligible body after pool[0] at 0x08077ee8; bgt target'),
    (0x08077fae, 0x08077fcb, 'LAB_08077fae',
     'B7 shared sub-block; beq target from sub_7f44/sub_7f56'),
    (0x08077fd0, 0x08077fef, 'LAB_08077fd0',
     'B7 shared sub-block; beq target from sub_7f44/sub_7f56'),
]

def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

def _set_tmode(lo_int, hi_int):
    lo = _addr(lo_int)
    hi = _addr(hi_int)
    ctx = currentProgram.getProgramContext()
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        ctx.setValue(tmode, lo, hi, BigInteger.ONE)
        print("[ok ] setTMode=1 for 0x%08x..0x%08x" % (lo_int, hi_int))
    else:
        print("[warn] TMode register not found")

def _disasm_at(sa, hi_int, label):
    stub_lo = _addr(sa)
    stub_hi = _addr(hi_int)
    cmd = DisassembleCommand(stub_lo, AddressSet(stub_lo, stub_hi), True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm %s @ 0x%08x: %s" % (label, sa, cmd.getStatusMsg()))
    else:
        print("[ok ] disasm %s @ 0x%08x" % (label, sa))

def main():
    print("=== FixF09Seg9bResidues (DRY=%s) ===" % DRY)
    print("Fixing %d residue ROM_INCBIN blocks in [0x77c50, 0x7850c)" % len(RESIDUE_BLOCKS))

    if DRY:
        for (sa, hi, label, note) in RESIDUE_BLOCKS:
            print("[dry] 0x%08x..0x%08x  %s  (%s)" % (sa, hi, label, note))
        return

    for (sa, hi, label, note) in RESIDUE_BLOCKS:
        print("\n--- Residue @ 0x%08x..0x%08x ---" % (sa, hi))
        print("    %s: %s" % (label, note))
        _set_tmode(sa, hi)
        _disasm_at(sa, hi, label)

    print("\n=== FixF09Seg9bResidues DONE ===")
    print("  Disassembled 3 residue blocks in B6/B7")

main()
