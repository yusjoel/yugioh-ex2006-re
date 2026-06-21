# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# PoolFixF10Seg9.py -- Fix pool word DAT_0808430c and label LAB_08084310
#
# Problem identified after DisassembleF10Seg9Blocks:
#   DAT_0808430c was exported as .byte [0x90,0xb2,0x01,0x02,0x01,0x20] (6 bytes)
#   but ROM[0x0808430c] = 0x0201b290 (gDuelPhaseFlags pool word, 4 bytes)
#   and ROM[0x08084310] = 0x2001 (movs r0,#1 THUMB code, 2 bytes)
#   bhi LAB_08084310 at 0x08084220 branches to 0x08084310 (state>5 returns 1 path)
#
# Fix:
#   1. createDWord at 0x0808430c (= gDuelPhaseFlags pool word)
#   2. Apply EQ gDuelPhaseFlags + label duel_phase_flags_0808430c
#   3. Disassemble THUMB code at 0x08084310 (movs r0,#1; pop; bx r1 epilogue)
#   4. The label LAB_08084310 should be created by the disassembly (Ghidra auto-names it)
#      OR we explicitly create label LAB_08084310 at 0x08084310
#
# NOTE: All EOL/plate text is pure ASCII (no CJK). Ghidra Jython mojibake prevention.

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


def _check_mem_word(addr_int, expected):
    mem = currentProgram.getMemory()
    a = _addr(addr_int)
    try:
        actual = mem.getInt(a) & 0xFFFFFFFF
        match = (actual == (expected & 0xFFFFFFFF))
        status = 'OK' if match else 'MISMATCH'
        print("[check] 0x%08x: got=0x%08x exp=0x%08x %s" % (
            addr_int, actual, expected & 0xFFFFFFFF, status))
        return match
    except Exception as e:
        print("[check err] 0x%08x: %s" % (addr_int, e))
        return False


def _create_dword(addr_int, label=None, eol=None):
    a = _addr(addr_int)
    listing = currentProgram.getListing()
    dt = DWordDataType.dataType
    try:
        listing.clearCodeUnits(a, _addr(addr_int + 3), False)
        listing.createData(a, dt)
        print("[dword ok] 0x%08x" % addr_int)
    except Exception as e:
        print("[warn] createDWord 0x%08x: %s" % (addr_int, e))
    if label:
        sm = currentProgram.getSymbolTable()
        sm.createLabel(a, label, SourceType.USER_DEFINED)
    if eol:
        cu = listing.getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)


def _apply_eq_pool(addr_int, value, eq_name, slot_label, eol=None):
    a = _addr(addr_int)
    sym_tbl = currentProgram.getSymbolTable()
    eq_tbl = currentProgram.getEquateTable()

    eq = eq_tbl.getEquate(eq_name)
    if eq is None:
        eq = eq_tbl.createEquate(eq_name, value & 0xFFFFFFFFFFFFFFFFL)
    eq.addReference(a, 0)

    existing = sym_tbl.getSymbols(a)
    names = [s.getName() for s in existing]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)

    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[EQ pool] 0x%08x  %s -> %s" % (addr_int, eq_name, slot_label))


def _create_label(addr_int, label):
    a = _addr(addr_int)
    sm = currentProgram.getSymbolTable()
    sm.createLabel(a, label, SourceType.USER_DEFINED)
    print("[label ok] 0x%08x %s" % (addr_int, label))


def _set_tmode_and_disasm(lo_int, hi_int, entry_int):
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
    a = _addr(entry_int)
    cmd = DisassembleCommand(a, None, True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm 0x%08x: %s" % (entry_int, cmd.getStatusMsg()))
    else:
        print("[disasm ok] 0x%08x" % entry_int)


def main():
    print("=== PoolFixF10Seg9 (DRY=%s) ===" % DRY)

    if DRY:
        print("[DRY] Fix DAT_0808430c -> createDWord gDuelPhaseFlags pool word")
        print("[DRY] Fix LAB_08084310 -> disasm movs r0,#1 epilogue THUMB code")
        return

    # Step 1: Verify ROM values
    _check_mem_word(0x0808430c, 0x0201b290)  # gDuelPhaseFlags pool word

    # Step 2: createDWord at 0x0808430c (was incorrectly exported as .byte)
    _create_dword(0x0808430c, 'bol_state0_phase_flags_0c',
                  'gDuelPhaseFlags=0x0201b290: pool word in book_of_life_eligible_state0')
    _apply_eq_pool(0x0808430c, 0x0201b290, 'gDuelPhaseFlags',
                   'duel_phase_flags_0808430c',
                   'gDuelPhaseFlags pool word in book_of_life_eligible_state0')

    # Step 3: Disassemble THUMB code at 0x08084310
    # Code: 0x2001=movs r0,#1; 0xbc70=pop{r4,r5,r6}; 0xbc02=pop{r1}; 0x4708=bx r1
    # This is the bhi target (state > 5 -> return 1)
    _set_tmode_and_disasm(0x08084310, 0x08084316, 0x08084310)

    # Step 4: Ensure label LAB_08084310 exists at 0x08084310
    _create_label(0x08084310, 'LAB_08084310')

    print("=== PoolFixF10Seg9 DONE ===")


main()
