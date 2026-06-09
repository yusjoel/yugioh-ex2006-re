# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF01Seg10Block.py -- f01 Seg-10 R4 disasm
#   Block: 0x08029170..0x0802b460 (0x22f0 = 8944 bytes)
#   Dispatch: dispatch_campaign_scene_by_prng_state via mov pc,r0 (.hword 0x4687)
#   -> raw THUMB addresses (no +1), 254-entry table at 0x08028d78
#   35 unique entry points, 207 default entries -> load_campaign_state_post_sio
#
# Strategy:
#   1. clearListing + setTMode(THUMB=1) for entire block
#   2. Per-entry DisassembleCommand (35 stubs, flow-based)
#   3. createFunction for each unique entry
#   4. Literal pool guard pass: scan for embedded .word pools via
#      reference-manager PC-relative ldr targets, create DWORDs
#      (prevents GAS "invalid offset" on literal pool re-export)
#
# NOTE: largest stub idx=10 @ 0x080295cc (estimated ~1572B) may contain
#       multiple interleaved literal pools. The guard pass runs AFTER all
#       disasm is complete to catch all pool locations.

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.app.cmd.function import CreateFunctionCmd
from ghidra.program.model.address import AddressSet
from ghidra.program.model.symbol import SourceType
from ghidra.program.model.listing import CodeUnit
from java.math import BigInteger

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"): DRY = True
except Exception:
    pass

BLOCK_LO      = 0x08029170
BLOCK_HI_EXCL = 0x0802b460  # exclusive (load_campaign_state_post_sio starts here)

# 35 unique entry points from dispatch table at 0x08028d78
# (254 entries; idx 0..253; default=0x0802b460 for 207 entries)
ENTRIES = [
    0x08029170,  # idx=0
    0x080292b4,  # idx=1
    0x08029304,  # idx=2
    0x08029398,  # idx=3
    0x080294bc,  # idx=4
    0x0802952c,  # idx=5
    0x0802957c,  # idx=7
    0x080295cc,  # idx=10  (largest stub ~1572B)
    0x08029bf0,  # idx=12
    0x08029e38,  # idx=20
    0x08029fac,  # idx=21
    0x0802a00c,  # idx=22
    0x0802a1cc,  # idx=23
    0x0802a3e4,  # idx=24
    0x0802a43c,  # idx=26
    0x0802a4c8,  # idx=27
    0x0802a4f4,  # idx=30
    0x0802a57c,  # idx=31
    0x0802a5b4,  # idx=32
    0x0802a640,  # idx=33
    0x0802a784,  # idx=50
    0x0802a83c,  # idx=51
    0x0802a89c,  # idx=52
    0x0802a9f8,  # idx=53
    0x0802aa64,  # idx=54
    0x0802aac4,  # idx=70
    0x0802ac54,  # idx=72
    0x0802ae40,  # idx=100
    0x0802aeac,  # idx=101
    0x0802b148,  # idx=102
    0x0802b1a0,  # idx=103
    0x0802b1d8,  # idx=104
    0x0802b220,  # idx=250
    0x0802b3a4,  # idx=252
    0x0802b434,  # idx=253
]


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _clear_and_set_thumb(lo_int, hi_int):
    lo = _addr(lo_int)
    hi = _addr(hi_int)
    try:
        clearListing(lo, hi)
        print("[ok ] clearListing(0x%08x..0x%08x)" % (lo_int, hi_int))
    except Exception as e:
        print("[warn] clearListing 0x%08x..0x%08x: %s" % (lo_int, hi_int, e))
    ctx = currentProgram.getProgramContext()
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        ctx.setValue(tmode, lo, hi, BigInteger.ONE)
        print("[ok ] setTMode=THUMB 0x%08x..0x%08x" % (lo_int, hi_int))
    else:
        print("[warn] TMode register not found")


def _disasm_stub(addr_int):
    lo = _addr(addr_int)
    cmd = DisassembleCommand(lo, None, True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm 0x%08x: %s" % (addr_int, cmd.getStatusMsg()))
        return False
    return True


def _create_fn(addr_int):
    a = _addr(addr_int)
    fn_mgr = currentProgram.getFunctionManager()
    sym_tbl = currentProgram.getSymbolTable()
    existing = fn_mgr.getFunctionAt(a)
    if existing is not None:
        print("[FN ] exists @ 0x%08x: %s" % (addr_int, existing.getName()))
        return
    fn_name = "campaign_scene_handler_%08x" % addr_int
    cmd = CreateFunctionCmd(fn_name, a, None, SourceType.USER_DEFINED)
    if cmd.applyTo(currentProgram):
        print("[FN ] created %s @ 0x%08x" % (fn_name, addr_int))
    else:
        print("[warn] createFunction @ 0x%08x: %s" % (addr_int, cmd.getStatusMsg()))
        sym_tbl.createLabel(a, fn_name, SourceType.USER_DEFINED)
        print("[FN ] label fallback %s @ 0x%08x" % (fn_name, addr_int))


def _guard_literal_pools_in_block():
    """
    Scan instructions in block for PC-relative LDR targets that fall within
    [BLOCK_LO, BLOCK_HI_EXCL). For each such target, create a DWORD to
    prevent GAS from misinterpreting the pool word as code.
    """
    rm = currentProgram.getReferenceManager()
    listing = currentProgram.getListing()
    lo = _addr(BLOCK_LO)
    hi = _addr(BLOCK_HI_EXCL - 1)
    guarded = set()
    n_guarded = 0
    # Walk instructions in block
    instr_iter = listing.getInstructions(lo, True)
    while instr_iter.hasNext():
        instr = instr_iter.next()
        if instr.getAddress().compareTo(hi) > 0:
            break
        # Check each memory reference from this instruction
        refs = rm.getReferencesFrom(instr.getAddress())
        for ref in refs:
            tgt = ref.getToAddress()
            tgt_int = tgt.getOffset() & 0xffffffff
            if BLOCK_LO <= tgt_int < BLOCK_HI_EXCL:
                if tgt_int not in guarded:
                    # Check if it looks like a literal pool (not instruction start)
                    existing_instr = listing.getInstructionAt(tgt)
                    if existing_instr is None:
                        try:
                            clearListing(_addr(tgt_int), _addr(tgt_int + 3))
                            createDWord(tgt)
                            guarded.add(tgt_int)
                            n_guarded += 1
                            print("[LP ] guard dword @ 0x%08x" % tgt_int)
                        except Exception as e:
                            print("[warn] guard dword @ 0x%08x: %s" % (tgt_int, e))
    print("[LP ] total %d literal pool DWORDs guarded" % n_guarded)


def main():
    print("=== DisassembleF01Seg10Block (DRY=%s) ===" % DRY)
    print("Block: 0x%08x..0x%08x (0x%x bytes, %d entries)" % (
        BLOCK_LO, BLOCK_HI_EXCL, BLOCK_HI_EXCL - BLOCK_LO, len(ENTRIES)))

    if DRY:
        print("[dry] would: clearListing 0x%08x..0x%08x" % (BLOCK_LO, BLOCK_HI_EXCL - 1))
        print("[dry] would: setTMode=THUMB 0x%08x..0x%08x" % (BLOCK_LO, BLOCK_HI_EXCL - 1))
        for e in ENTRIES:
            print("[dry] would: DisassembleCommand @ 0x%08x" % e)
        print("[dry] would: createFunction x%d" % len(ENTRIES))
        print("[dry] would: guard literal pools in block (PC-relative ldr targets)")
        print("[done] DRY complete (%d entries)" % len(ENTRIES))
        return

    # 1. Clear entire block and set THUMB mode
    _clear_and_set_thumb(BLOCK_LO, BLOCK_HI_EXCL - 1)

    # 2. Per-entry disasm (flow-based; 35 stubs)
    n_ok = 0
    for e in ENTRIES:
        if _disasm_stub(e):
            n_ok += 1
    print("[disasm] %d/%d stubs disassembled" % (n_ok, len(ENTRIES)))

    # 3. Create functions for each unique entry
    for e in ENTRIES:
        _create_fn(e)

    # 4. Guard literal pools AFTER all disasm
    _guard_literal_pools_in_block()

    print("=== DisassembleF01Seg10Block COMPLETE ===")


main()
