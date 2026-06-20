# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixF09Seg9bPools2.py -- Fix more missing pool DWord definitions in Seg-9b B6
#
# After FixF09Seg9bResidues.py, the extended B6 body (LAB_08077eec) was disassembled.
# This revealed 2 more pool references without labels:
#
#   asm/09 L21597: ldr r2, DAT_08077f24  -- 0x08077f24 = 0x00001da8 (LP_CARD_TRACK_BASE_OFF)
#   (DAT_08077f20 label exists, but 8-byte .byte block so DAT_08077f24 undefined)
#
# The root cause: DisassembleF09Seg9bBlocks.py forced dword at 0x08077f18 and 0x08077f1c
# (which turned out to be CODE bytes 0x18404903 and 0x46876800 inside the extended B6 body),
# but the actual pool words for the extended body are at 0x08077f20 and 0x08077f24.
#
# Fix: force_dword at 0x08077f20 (gP1LifePoints) and 0x08077f24 (LP_CARD_TRACK_BASE_OFF).
# Then re-disassemble the extended B6 body to pick up the correct instruction decode
# for 0x08077f18/0x08077f1c (they should be THUMB instructions, not DWords).

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

def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

def _check(addr_int, expected):
    mem = currentProgram.getMemory()
    a = _addr(addr_int)
    try:
        actual = mem.getInt(a) & 0xFFFFFFFF
    except Exception as e:
        print("[FAIL] read 0x%08x: %s" % (addr_int, e))
        return False
    if actual != (expected & 0xFFFFFFFF):
        print("[FAIL] 0x%08x: got 0x%08x expected 0x%08x" % (addr_int, actual, expected & 0xFFFFFFFF))
        return False
    return True

def _force_dword(addr_int, expected, note):
    print("  Pool @ 0x%08x (expected 0x%08x): %s" % (addr_int, expected & 0xFFFFFFFF, note))
    if not _check(addr_int, expected):
        print("  [SKIP] value mismatch")
        return

    if DRY:
        print("  [dry] force_dword @ 0x%08x" % addr_int)
        return

    a = _addr(addr_int)
    a_end = _addr(addr_int + 3)
    listing = currentProgram.getListing()
    try:
        clearListing(a, a_end)
        print("  [ok ] clearListing @ 0x%08x" % addr_int)
    except Exception as e:
        print("  [warn] clearListing @ 0x%08x: %s" % (addr_int, e))
    try:
        listing.createData(a, ghidra.program.model.data.DWordDataType.dataType)
        print("  [ok ] force_dword @ 0x%08x" % addr_int)
    except Exception as e:
        print("  [warn] createData @ 0x%08x: %s" % (addr_int, e))

def _undo_wrong_dword(addr_int, note):
    """Undo incorrectly forced DWords (at CODE addresses) by clearListing + re-disasm."""
    print("  Undo wrong dword @ 0x%08x: %s" % (addr_int, note))
    if DRY:
        print("  [dry] clearListing + re-disasm @ 0x%08x" % addr_int)
        return

    a = _addr(addr_int)
    a_end = _addr(addr_int + 3)
    try:
        clearListing(a, a_end)
        print("  [ok ] clearListing @ 0x%08x" % addr_int)
    except Exception as e:
        print("  [warn] clearListing @ 0x%08x: %s" % (addr_int, e))

def _set_tmode(lo_int, hi_int):
    lo = _addr(lo_int)
    hi = _addr(hi_int)
    ctx = currentProgram.getProgramContext()
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        ctx.setValue(tmode, lo, hi, BigInteger.ONE)
        print("  [ok ] setTMode=1 for 0x%08x..0x%08x" % (lo_int, hi_int))
    else:
        print("  [warn] TMode register not found")

def _disasm_at(sa, hi_int, label):
    stub_lo = _addr(sa)
    stub_hi = _addr(hi_int)
    cmd = DisassembleCommand(stub_lo, AddressSet(stub_lo, stub_hi), True)
    if not cmd.applyTo(currentProgram):
        print("  [warn] disasm %s @ 0x%08x: %s" % (label, sa, cmd.getStatusMsg()))
    else:
        print("  [ok ] disasm %s @ 0x%08x" % (label, sa))

def main():
    print("=== FixF09Seg9bPools2 (DRY=%s) ===" % DRY)

    # Step 1: Undo incorrect DWords at 0x08077f18 and 0x08077f1c (these are CODE)
    # These were forced in DisassembleF09Seg9bBlocks.py but are actually THUMB instructions
    print("\n--- Step 1: Undo incorrect DWords at 0x08077f18/0x08077f1c (CODE) ---")
    _undo_wrong_dword(0x08077f18, "0x18404903 = THUMB: adds r0,r0,r0; adds r4,r0,#0x1 (CODE)")
    _undo_wrong_dword(0x08077f1c, "0x46876800 = THUMB: movs r0,r0; mov pc,r0 (CODE)")

    # Step 2: Force correct DWords for actual pool at 0x08077f20/0x08077f24
    print("\n--- Step 2: Force correct pool DWords at 0x08077f20/0x08077f24 ---")
    _force_dword(0x08077f20, 0x0201c4e0, "gP1LifePoints (B6 fn_eligible extended body pool[0])")
    _force_dword(0x08077f24, 0x00001da8, "LP_CARD_TRACK_BASE_OFF (B6 fn_eligible extended body pool[1])")

    # Step 3: Re-disassemble B6 extended body (clearListing of CODE area + re-disasm)
    # The range 0x08077eec..0x08077f1f needs fresh disasm
    print("\n--- Step 3: Re-disassemble B6 extended body 0x08077eec..0x08077f1f ---")
    if not DRY:
        lo = _addr(0x08077eec)
        hi = _addr(0x08077f1f)  # just before the pool at 0x08077f20
        try:
            clearListing(lo, hi)
            print("  [ok ] clearListing 0x08077eec..0x08077f1f")
        except Exception as e:
            print("  [warn] clearListing: %s" % e)
        _set_tmode(0x08077eec, 0x08077f1f)
        _disasm_at(0x08077eec, 0x08077f1f, "LAB_08077eec_re")
    else:
        print("  [dry] clearListing + setTMode + disasm 0x08077eec..0x08077f1f")

    print("\n=== FixF09Seg9bPools2 DONE ===")

main()
