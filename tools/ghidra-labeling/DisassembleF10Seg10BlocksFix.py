# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF10Seg10BlocksFix.py -- Fix: disasm check_equip_slot_target_not_blocked
#
# check_equip_slot_target_not_blocked at 0x08084a98 (0x5c bytes) was inadvertently
# cleared by BLK3 clearListing (0x08084918..0x08084af2). It's a regular named function
# (19th fn in Seg-10), not a ROM_INCBIN block. Needs THUMB disassembly.
#
# ROM bytes confirmed: 0x08084a98 = 0xb570 = push{r4,r5,r6,lr}; ends at 0x08084af4-2 = 0x08084af2
# (2B padding 0x08084af0=0x4708 bx r1, 0x08084af2=0x0000 pad... wait fn ends at 0x08084af4-2)
# Actually end is 0x08084af2 (ROM_INCBIN ends at 0x84a98+0x5c=0x84af4, so fn is 0x5c bytes minus 2B pad
# at 0x84af2..0x84af3 = 0x0000).

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.data import DWordDataType
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import SourceType
from java.math import BigInteger

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _clear_and_tmode(lo_int, hi_int):
    lo = _addr(lo_int)
    hi = _addr(hi_int)
    try:
        clearListing(lo, hi)
    except Exception as e:
        print("[warn] clearListing 0x%08x..0x%08x: %s" % (lo_int, hi_int, e))
    ctx = currentProgram.getProgramContext()
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        ctx.setValue(tmode, lo, hi, BigInteger.ONE)
    print("[tmode] set THUMB 0x%08x..0x%08x" % (lo_int, hi_int))


def _disasm_stub(entry_int):
    a = _addr(entry_int)
    cmd = DisassembleCommand(a, None, True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm 0x%08x: %s" % (entry_int, cmd.getStatusMsg()))
    else:
        print("[disasm ok] 0x%08x" % entry_int)


def main():
    if DRY:
        print("DRY: disasm check_equip_slot_target_not_blocked @ 0x08084a98 (0x5c bytes)")
        return

    print("=== Fix: check_equip_slot_target_not_blocked @ 0x08084a98 ===")
    # Function body: 0x08084a98..0x08084af1 (0x5a bytes code + 0x2 pad at 0x84af2..0x84af3)
    # Clear and disasm the function body (stop before BLK4 zero-pad at 0x84af2)
    _clear_and_tmode(0x08084a98, 0x08084af2)
    _disasm_stub(0x08084a98)

    # Ensure the function exists with the correct name
    fn = getFunctionAt(_addr(0x08084a98))
    if fn is None:
        fn = createFunction(_addr(0x08084a98), 'check_equip_slot_target_not_blocked')
        if fn:
            print("[func] created check_equip_slot_target_not_blocked @ 0x08084a98")
        else:
            print("[FAIL] createFunction 0x08084a98")
    else:
        print("[func] already exists: %s @ 0x08084a98" % fn.getName())

    print("=== DisassembleF10Seg10BlocksFix DONE ===")


main()
