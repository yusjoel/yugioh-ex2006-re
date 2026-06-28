# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF12Seg2Block1c.py -- file 12 Seg-2 Block1 sub-sub-stub fix
#
# After DisassembleF12Seg2Block1b.py ran, ROM_INCBIN 0x952ea/0x1a remains.
# Structure at 0x952ea:
#   0x952ea: .zero 2 (alignment pad)
#   0x952ec: .word 0x00001d44 (pool word DAT_080952ec, referenced by ldr r2,DAT_080952ec at 0x952d4)
#   0x952ee: .zero 2 (alignment pad)
#   0x952f0: THUMB code (LAB_080952f0 -> LAB_080952f2 -> LAB_080952fc target code)
#   ... ends at 0x95303 (inclusive), dispatch_case_9 starts 0x95304
#
# LAB_080952f2 and LAB_080952fc are inside this code block.
# They are referenced by branches in case[2] (0x080952b6, 0x080952ba) and
# by LAB_080952d4 code.
#
# Fix:
#   1. clearListing 0x952ea..0x95303
#   2. setTMode THUMB=1 for 0x952ea..0x95303
#   3. createDWord at 0x952ec (DAT_080952ec = 0x00001d44)
#      + equate for 0x1d44 (if exists: check ewram.inc / duel_field.inc;
#        not in constants yet -- leave as raw or check)
#   4. DisassembleCommand at 0x952f0 (THUMB code start)
#
# NOTE: All text is pure ASCII.

from ghidra.app.cmd.disassemble import DisassembleCommand
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


SUB_START = 0x080952ea
SUB_END   = 0x08095303  # inclusive

POOL_WORD_ADDR  = 0x080952ec
POOL_WORD_VALUE = 0x00001d44  # ELIGIB_CARD_ID_OFF (ewram.inc:418)

CODE_ENTRY = 0x080952f0  # THUMB code starts here (after pool word + pad)


def main():
    print("=== DisassembleF12Seg2Block1c (DRY=%s) ===" % DRY)
    print("  Sub-block: 0x080952ea..0x08095303 (0x1a bytes)")
    print("  Pool @ 0x952ec = 0x%08x; Code @ 0x952f0" % POOL_WORD_VALUE)

    listing = currentProgram.getListing()
    sym_tbl = currentProgram.getSymbolTable()
    eq_tbl  = currentProgram.getEquateTable()
    ctx     = currentProgram.getProgramContext()
    tmode   = ctx.getRegister("TMode")

    a_lo = _addr(SUB_START)
    a_hi = _addr(SUB_END)

    if DRY:
        print("[dry] clearListing 0x%08x..0x%08x" % (SUB_START, SUB_END))
        print("[dry] setTMode THUMB=1 for 0x%08x..0x%08x" % (SUB_START, SUB_END))
        print("[dry] createDWord @ 0x%08x = 0x%08x (DAT_080952ec)" % (POOL_WORD_ADDR, POOL_WORD_VALUE))
        print("[dry] DisassembleCommand @ 0x%08x" % CODE_ENTRY)
        print("[dry] done")
        return

    # Step 1: clearListing
    print("[1] clearListing 0x%08x..0x%08x" % (SUB_START, SUB_END))
    try:
        clearListing(a_lo, a_hi)
        print("    done")
    except Exception as e:
        print("[WARN] clearListing: %s" % e)

    # Step 2: setTMode THUMB=1
    print("[2] setTMode THUMB=1")
    if tmode is not None:
        ctx.setValue(tmode, a_lo, a_hi, BigInteger.ONE)
        print("    TMode set")
    else:
        print("[WARN] TMode register not found")

    # Step 3: createDWord at pool word
    print("[3] createDWord @ 0x%08x = 0x%08x" % (POOL_WORD_ADDR, POOL_WORD_VALUE))
    pa = _addr(POOL_WORD_ADDR)
    try:
        listing.createData(pa, ghidra.program.model.data.DWordDataType.dataType)
        print("    createDWord ok")
    except Exception as e:
        print("    [WARN] createDWord: %s" % e)
    # ELIGIB_CARD_ID_OFF = 0x1d44 (ewram.inc:418) -- create equate + slot label
    eq_name = 'ELIGIB_CARD_ID_OFF'
    slot_label = 'eligib_card_id_952ec'
    eq = eq_tbl.getEquate(eq_name)
    if eq is None:
        eq = eq_tbl.createEquate(eq_name, POOL_WORD_VALUE & 0xFFFFFFFFFFFFFFFFL)
        print("    equate created: %s" % eq_name)
    eq.addReference(pa, 0)
    existing = [s.getName() for s in sym_tbl.getSymbols(pa)]
    if slot_label not in existing:
        sym_tbl.createLabel(pa, slot_label, SourceType.USER_DEFINED)
    print("    equate+label set: %s -> %s" % (eq_name, slot_label))

    # Step 4: DisassembleCommand at code entry
    print("[4] DisassembleCommand @ 0x%08x (THUMB code)" % CODE_ENTRY)
    ea = _addr(CODE_ENTRY)
    cmd = DisassembleCommand(ea, None, False)
    if cmd.applyTo(currentProgram):
        print("    disasm ok")
    else:
        print("    [WARN] disasm: %s" % cmd.getStatusMsg())

    print("\n=== DisassembleF12Seg2Block1c DONE ===")
    print("  Pool @ 0x952ec + code @ 0x952f0..0x95303 handled")
    print("  POST-CHECK: grep ROM_INCBIN/.byte in [0x08095274, 0x08095334) must == 0")


main()
