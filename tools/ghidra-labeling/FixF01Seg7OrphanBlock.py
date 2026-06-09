# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixF01Seg7OrphanBlock.py -- Fix orphan block (0x0802108e..0x0802114b)
#
# Discovery: FUN_08023614 (in block4) calls SUB_08021090 via bl.
# So 0x08021090 has a real caller and must be disassembled + createFunction.
#
# Layout of 0x0802108e..0x0802114b:
#   0x0802108e..0x0802108f: 2B align pad (0x0000)
#   0x08021090..0x080210f7: SUB_08021090 code body
#   0x080210f8..0x08021113: Literal pool 1 (7 DWORDs):
#     0x080210f8: 0xfffffb00  (stack frame size: sp += 0xfffffb00 = -0x500)
#     0x080210fc: 0x0201e2a0  gDuelCardCtxBase
#     0x08021100: 0x02023360  gDuelSceneBase
#     0x08021104: 0x09e5e9cc  ROM step table ptr (duel scene card select)
#     0x08021108: 0x02029590  gMenuState
#     0x0802110c: 0x03000040  gPrng (IWRAM base)
#     0x08021110: 0x00000213  gPrng+0x213 field offset
#   0x08021114..0x0802113b: More SUB_08021090 code (second body part)
#   0x0802113c..0x0802114b: Literal pool 2 (4 DWORDs):
#     0x0802113c: 0x0201c4e0  gP1LifePoints
#     0x08021140: 0x00001cec  P1LP_TIMER_OFF
#     0x08021144: 0x03000040  gPrng
#     0x08021148: 0xffffd8d5  large negative constant (step table dispatch bit mask)
#
# Fix strategy:
#   1. clearListing entire range
#   2. setTMode THUMB
#   3. createDWord for both literal pools
#   4. DisassembleCommand for entry 0x08021090 (let flow handle code around literal pools)
#   5. createFunction SUB_08021090

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.app.cmd.function import CreateFunctionCmd
from ghidra.program.model.address import AddressSet
from ghidra.program.model.symbol import SourceType
from java.math import BigInteger

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"): DRY = True
except Exception:
    pass


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


# Literal pool 1: 0x080210f8..0x08021113 (7 DWORDs)
# These are known EWRAM/IWRAM addresses that we can directly recognize
LITPOOL1 = [
    (0x080210f8, 0xfffffb00),
    (0x080210fc, 0x0201e2a0),
    (0x08021100, 0x02023360),
    (0x08021104, 0x09e5e9cc),
    (0x08021108, 0x02029590),
    (0x0802110c, 0x03000040),
    (0x08021110, 0x00000213),
]

# Literal pool 2: 0x0802113c..0x0802114b (4 DWORDs)
LITPOOL2 = [
    (0x0802113c, 0x0201c4e0),
    (0x08021140, 0x00001cec),
    (0x08021144, 0x03000040),
    (0x08021148, 0xffffd8d5),
]


def main():
    print("=== FixF01Seg7OrphanBlock (DRY=%s) ===" % DRY)

    ORPHAN_LO = 0x0802108e
    ORPHAN_HI = 0x0802114b
    CODE_ENTRY = 0x08021090

    if DRY:
        print("[dry] would clearListing + setTMode + createDWord litpool1/2 + disasm + createFunction")
        return

    lo = _addr(ORPHAN_LO)
    hi = _addr(ORPHAN_HI)

    # 1. Clear listing
    try:
        clearListing(lo, hi)
        print("[ok] clearListing 0x%08x..0x%08x" % (ORPHAN_LO, ORPHAN_HI))
    except Exception as e:
        print("[warn] clearListing: %s" % e)

    # 2. Set THUMB mode for entire range
    ctx = currentProgram.getProgramContext()
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        ctx.setValue(tmode, lo, hi, BigInteger.ONE)
        print("[ok] setTMode=THUMB")
    else:
        print("[warn] TMode register not found")

    # 3. Create DWORDs for literal pool 1
    print("[LP1] Creating DWORDs for literal pool 1...")
    for addr_int, val in LITPOOL1:
        try:
            createDWord(_addr(addr_int))
            print("[LP1] createDWord @ 0x%08x (0x%08x)" % (addr_int, val))
        except Exception as e:
            print("[warn] createDWord LP1 @ 0x%08x: %s" % (addr_int, e))

    # 4. Disassemble from entry point (flow will handle code body + second literal pool)
    print("[disasm] DisassembleCommand from 0x%08x..." % CODE_ENTRY)
    entry_addr = _addr(CODE_ENTRY)
    cmd = DisassembleCommand(entry_addr, None, True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm: %s" % cmd.getStatusMsg())
    else:
        print("[ok] disasm from 0x%08x" % CODE_ENTRY)

    # 5. Create DWORDs for literal pool 2 (flow may have decoded them as instructions)
    print("[LP2] Creating DWORDs for literal pool 2...")
    for addr_int, val in LITPOOL2:
        try:
            clearListing(_addr(addr_int), _addr(addr_int + 3))
            createDWord(_addr(addr_int))
            print("[LP2] createDWord @ 0x%08x (0x%08x)" % (addr_int, val))
        except Exception as e:
            print("[warn] createDWord LP2 @ 0x%08x: %s" % (addr_int, e))

    # 6. Create function
    fn_mgr = currentProgram.getFunctionManager()
    sym_tbl = currentProgram.getSymbolTable()
    existing = fn_mgr.getFunctionAt(_addr(CODE_ENTRY))
    if existing is not None:
        print("[FN] function already exists: %s @ 0x%08x" % (existing.getName(), CODE_ENTRY))
    else:
        cmd2 = CreateFunctionCmd("SUB_08021090", _addr(CODE_ENTRY), None, SourceType.USER_DEFINED)
        if cmd2.applyTo(currentProgram):
            print("[FN] created SUB_08021090 @ 0x%08x" % CODE_ENTRY)
        else:
            print("[warn] createFunction: %s" % cmd2.getStatusMsg())
            sym_tbl.createLabel(_addr(CODE_ENTRY), "SUB_08021090", SourceType.USER_DEFINED)

    print("=== FixF01Seg7OrphanBlock DONE ===")


main()
