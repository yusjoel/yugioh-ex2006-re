# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF09Seg4bDisasmFix.py -- Disasm missed code regions in B6 and fix related pools
#   Region 1: 0x72480..0x72489 (10 bytes, continuation of last_turn_sub_2444)
#     LAB_08072486 is at 0x72486 (movs r0,#0x7f then b ...)
#   Region 2: 0x7250c..0x7252f (0x24 bytes, continuation of last_turn_sub_24b4)
#     LAB_0807252a is at 0x7252a (movs r0,#0x7c then b ...)
#   Also fix: DAT_08072504 (0x72504, 4 bytes, pool word = 0x00001daa LP_CARD_TRACK_NEXT_OFF)

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import SourceType
from ghidra.program.model.data import DWordDataType
from ghidra.program.model.util import CodeUnitInsertionException
from java.math import BigInteger

def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

def force_dword(listing, sym_tbl, pool_addr, pool_label, pool_eol=None):
    pa = _addr(pool_addr)
    try:
        clearListing(pa, _addr(pool_addr + 7))
    except Exception as e:
        print("[WARN] clearListing @ 0x%08x: %s" % (pool_addr, e))
    try:
        d = listing.createData(pa, DWordDataType.dataType)
        if d is not None:
            print("[POOL] DWord @ 0x%08x (%s)" % (pool_addr, pool_label))
        else:
            print("[WARN] createData None @ 0x%08x" % pool_addr)
    except CodeUnitInsertionException as e:
        try:
            clearListing(pa, _addr(pool_addr + 11))
            d2 = listing.createData(pa, DWordDataType.dataType)
            if d2 is not None:
                print("[POOL] DWord @ 0x%08x (%s) [retry ok]" % (pool_addr, pool_label))
        except Exception as e2:
            print("[WARN] retry failed @ 0x%08x: %s" % (pool_addr, e2))
    except Exception as e:
        print("[WARN] unexpected @ 0x%08x: %s" % (pool_addr, e))
    existing_p = [s.getName() for s in sym_tbl.getSymbols(pa)]
    if pool_label not in existing_p:
        try:
            sym_tbl.createLabel(pa, pool_label, SourceType.USER_DEFINED)
        except Exception:
            pass
    if pool_eol:
        cu = listing.getCodeUnitAt(pa)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, pool_eol)

listing = currentProgram.getListing()
sym_tbl = currentProgram.getSymbolTable()
ctx = currentProgram.getProgramContext()
tmode = ctx.getRegister("TMode")

print("=== RefineF09Seg4bDisasmFix ===")

# --- Fix DAT_08072504: pool word = 0x00001daa (LP_CARD_TRACK_NEXT_OFF) ---
force_dword(listing, sym_tbl, 0x08072504, 'pool_b6_2504', 'LP_CARD_TRACK_NEXT_OFF=0x1daa; literal pool last_turn_sub_24b4')

# --- Region 1: 0x72480..0x72489 (10 bytes THUMB code) ---
print("\n--- Region1: 0x08072480..0x08072489 ---")
R1_START = 0x08072480
R1_END   = 0x08072489  # inclusive
a_r1_lo = _addr(R1_START)
a_r1_hi = _addr(R1_END)
try:
    clearListing(a_r1_lo, a_r1_hi)
    print("[R1] clearListing done")
except Exception as e:
    print("[WARN] clearListing R1: %s" % e)
if tmode is not None:
    ctx.setValue(tmode, a_r1_lo, a_r1_hi, BigInteger.ONE)
    print("[R1] TMode set")
cmd_r1 = DisassembleCommand(a_r1_lo, None, False)
if cmd_r1.applyTo(currentProgram):
    print("[R1] disasm ok")
else:
    print("[WARN] disasm R1: %s" % cmd_r1.getStatusMsg())
# Ensure LAB_08072486 is USER_DEFINED
for lbl_addr, lbl_name in [(0x08072486, 'LAB_08072486')]:
    la = _addr(lbl_addr)
    existing = [s.getName() for s in sym_tbl.getSymbols(la)]
    if lbl_name not in existing:
        try:
            sym_tbl.createLabel(la, lbl_name, SourceType.USER_DEFINED)
            print("[LABEL] %s @ 0x%08x created" % (lbl_name, lbl_addr))
        except Exception as e:
            print("[WARN] createLabel %s: %s" % (lbl_name, e))
    else:
        # Check if USER_DEFINED version exists
        ud_exists = any(s.getName() == lbl_name and str(s.getSource()) == 'USER_DEFINED'
                       for s in sym_tbl.getSymbols(la))
        if not ud_exists:
            try:
                sym_tbl.createLabel(la, lbl_name, SourceType.USER_DEFINED)
                print("[LABEL] %s USER_DEFINED copy created" % lbl_name)
            except Exception as e:
                print("[WARN] createLabel USER_DEFINED %s: %s" % (lbl_name, e))
        else:
            print("[LABEL] %s already USER_DEFINED" % lbl_name)

# --- Region 2: 0x7250c..0x7252f (0x24 bytes THUMB code) ---
print("\n--- Region2: 0x0807250c..0x0807252f ---")
R2_START = 0x0807250c
R2_END   = 0x0807252f  # inclusive
a_r2_lo = _addr(R2_START)
a_r2_hi = _addr(R2_END)
try:
    clearListing(a_r2_lo, a_r2_hi)
    print("[R2] clearListing done")
except Exception as e:
    print("[WARN] clearListing R2: %s" % e)
if tmode is not None:
    ctx.setValue(tmode, a_r2_lo, a_r2_hi, BigInteger.ONE)
    print("[R2] TMode set")
cmd_r2 = DisassembleCommand(a_r2_lo, None, False)
if cmd_r2.applyTo(currentProgram):
    print("[R2] disasm ok")
else:
    print("[WARN] disasm R2: %s" % cmd_r2.getStatusMsg())
# Ensure LAB_0807252a is USER_DEFINED
for lbl_addr, lbl_name in [(0x0807252a, 'LAB_0807252a')]:
    la = _addr(lbl_addr)
    existing = [s.getName() for s in sym_tbl.getSymbols(la)]
    if lbl_name not in existing:
        try:
            sym_tbl.createLabel(la, lbl_name, SourceType.USER_DEFINED)
            print("[LABEL] %s @ 0x%08x created" % (lbl_name, lbl_addr))
        except Exception as e:
            print("[WARN] createLabel %s: %s" % (lbl_name, e))
    else:
        ud_exists = any(s.getName() == lbl_name and str(s.getSource()) == 'USER_DEFINED'
                       for s in sym_tbl.getSymbols(la))
        if not ud_exists:
            try:
                sym_tbl.createLabel(la, lbl_name, SourceType.USER_DEFINED)
                print("[LABEL] %s USER_DEFINED copy created" % lbl_name)
            except Exception as e:
                print("[WARN] createLabel USER_DEFINED %s: %s" % (lbl_name, e))
        else:
            print("[LABEL] %s already USER_DEFINED" % lbl_name)

print("\n=== RefineF09Seg4bDisasmFix DONE ===")
