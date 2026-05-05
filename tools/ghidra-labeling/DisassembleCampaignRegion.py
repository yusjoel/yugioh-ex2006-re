# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleCampaignRegion.py  (Jython 2.7 / Ghidra 12.x)
#
# Force-disassemble the campaign-feature code region currently held in three
# .incbin chunks of asm/all.s:
#   ROM_INCBIN 0x25d58, 0x1f20  (state-handler bodies for FUN_08025c94 dispatch)
#   ROM_INCBIN 0x27e50, 0x06c   (small chunk, content TBD)
#   ROM_INCBIN 0x27f00, 0x518   (state-handler bodies for PTR_DAT_08027ec0 dispatch)
#
# Two state-machine dispatch tables drive 41 handlers (26 unique + 16 unique = 42 - 1 overlap):
#   - PTR_DAT_08025ccc @ 0x08025ccc (35 entries, 26 unique) — driven by FUN_08025c94
#       dispatch via `ldr r0,[tbl+state*4]; mov pc, r0`  (.hword 0x4687)
#   - PTR_DAT_08027ec0 @ 0x08027ec0 (16 entries) — driven by some sub-dispatcher
#       (.hword 0x4687 / 0x46xx pattern in containing function)
#
# These handlers are CPS-style continuation entries (not standard APCS functions):
#   - First instruction is typically BL/LDR/MOV (not push {...,lr})
#   - They share the dispatcher's stack frame (saved r4-r10+lr)
#   - They unwind the frame themselves via `add sp; pop; bx r0` or equivalent
# Ghidra accepts createFunction at non-prologue entries — we just need to set
# TMode=THUMB and let DisassembleCommand walk forward from each entry until it
# hits an unconditional terminator.
#
# Pipeline (after this script runs):
#   1. PromoteCallTargetsToFunctions.py        # pick up bl-target sub-routines
#   2. ghidra-export-range.bat → asm/all.s     # regen
#   3. inject_modes.py                          # mode + s-suffix patching
#   4. build.bat                                # produce output/2343.gba
#   5. sha1sum verify byte-identical            # MUST match 9689337d6aac...
#
# Usage:
#   tools\asm-regen\ghidra-run-script.bat DisassembleCampaignRegion.py
#   tools\asm-regen\ghidra-run-script.bat DisassembleCampaignRegion.py dry

from ghidra.program.model.address import Address
from ghidra.program.model.symbol import SourceType
from ghidra.program.model.listing import CodeUnit
from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.lang import RegisterValue
from ghidra.program.model.lang import Register
from ghidra.program.model.data import DWordDataType
from ghidra.program.model.util import CodeUnitInsertionException
from java.lang import Exception as JavaException
from java.math import BigInteger

RUN_DRY = False
try:
    _args = list(getScriptArgs())
    if _args and _args[0].lower() in ("dry", "--dry", "1", "true"):
        RUN_DRY = True
except Exception:
    pass


# Dispatch table 1: PTR_DAT_08025ccc, 26 unique state handlers.
# 0x08027c78 is already disassembled (FUN_08027c78 = default/error handler) -> excluded.
CAMPAIGN_STATE1_HANDLERS = [
    (0x08025d58, "FUN_08025d58"),
    (0x08025ec0, "FUN_08025ec0"),
    (0x08025f14, "FUN_08025f14"),
    (0x080266bc, "FUN_080266bc"),
    (0x080266d0, "FUN_080266d0"),
    (0x08026748, "FUN_08026748"),
    (0x080267ca, "FUN_080267ca"),
    (0x08026858, "FUN_08026858"),
    (0x08026a2c, "FUN_08026a2c"),
    (0x08026af2, "FUN_08026af2"),
    (0x08026bc8, "FUN_08026bc8"),
    (0x08026c88, "FUN_08026c88"),
    (0x08026e68, "FUN_08026e68"),
    (0x08026e9c, "FUN_08026e9c"),
    (0x08026fe4, "FUN_08026fe4"),
    (0x0802727c, "FUN_0802727c"),
    (0x080274f4, "FUN_080274f4"),
    (0x0802752c, "FUN_0802752c"),
    (0x080276dc, "FUN_080276dc"),
    (0x08027714, "FUN_08027714"),
    (0x0802774c, "FUN_0802774c"),
    (0x080277a4, "FUN_080277a4"),
    (0x08027834, "FUN_08027834"),
    (0x08027888, "FUN_08027888"),
    (0x080278c0, "FUN_080278c0"),
    (0x08027a0c, "FUN_08027a0c"),
]

# Dispatch table 2: PTR_DAT_08027ec0, 16 entries (all in incbin 0x27f00..0x28418).
CAMPAIGN_STATE2_HANDLERS = [
    (0x08027f00, "FUN_08027f00"),
    (0x08027f48, "FUN_08027f48"),
    (0x08027fcc, "FUN_08027fcc"),
    (0x080280bc, "FUN_080280bc"),
    (0x0802803c, "FUN_0802803c"),
    (0x080280d0, "FUN_080280d0"),
    (0x08028118, "FUN_08028118"),
    (0x08028194, "FUN_08028194"),
    (0x08028402, "FUN_08028402"),
    (0x080281d8, "FUN_080281d8"),
    (0x0802826e, "FUN_0802826e"),
    (0x080282a0, "FUN_080282a0"),
    (0x080282ac, "FUN_080282ac"),
    (0x080282c2, "FUN_080282c2"),
    (0x080282f0, "FUN_080282f0"),
    (0x080283e8, "FUN_080283e8"),
]

# 0x27e50, 0x6c chunk: tail-end of FUN_08027c98 region. Ghidra likely needs the
# function prior to it disassembled fully; we don't add explicit entries here —
# scan_region_define_data + PromoteCallTargetsToFunctions should pick up any
# bl-targets. If post-build there are still SUB_ refs in this range, add them
# here as entries.
ALL_HANDLERS = CAMPAIGN_STATE1_HANDLERS + CAMPAIGN_STATE2_HANDLERS


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def force_disassemble_thumb(addr_int):
    addr = _addr(addr_int)
    cu = currentProgram.getListing().getCodeUnitAt(addr)
    if cu is not None and cu.getMnemonicString() != "??":
        return True  # already done
    if RUN_DRY:
        print("[dry] would disassemble THUMB @ 0x%08X" % addr_int)
        return True
    prog_ctx = currentProgram.getProgramContext()
    tmode = prog_ctx.getRegister("TMode")
    if tmode is not None:
        try:
            prog_ctx.setValue(tmode, addr, addr, BigInteger.ONE)
        except Exception as e:
            print("[warn] setValue TMode @ 0x%08X failed: %s" % (addr_int, e))
    cmd = DisassembleCommand(addr, None, True)
    ok = cmd.applyTo(currentProgram)
    if not ok:
        print("[fail] disassemble @ 0x%08X: %s" % (addr_int, cmd.getStatusMsg()))
        return False
    print("[ok]   disassembled THUMB @ 0x%08X" % addr_int)
    return True


def create_function(addr_int, name):
    addr = _addr(addr_int)
    fm = currentProgram.getFunctionManager()
    func = fm.getFunctionAt(addr)
    if func is None:
        if RUN_DRY:
            print("[dry] would create function %s @ 0x%08X" % (name, addr_int))
            return True
        func = createFunction(addr, name)
        if func is None:
            print("[fail] createFunction @ 0x%08X (%s)" % (addr_int, name))
            return False
        print("[ok]   created function %s @ 0x%08X" % (name, addr_int))
        return True
    else:
        if func.getName() == name or func.getName().startswith(name):
            return True
        if RUN_DRY:
            print("[dry] would rename %s -> %s @ 0x%08X" % (func.getName(), name, addr_int))
            return True
        try:
            func.setName(name, SourceType.USER_DEFINED)
            print("[ok]   renamed -> %s @ 0x%08X" % (name, addr_int))
        except Exception as e:
            print("[fail] rename @ 0x%08X: %s" % (addr_int, e))
            return False
        return True


def scan_region_define_data(start_int, end_int):
    """Walk all instructions in [start, end), collect data refs, define Dword at each
    target that isn't yet a defined data item.  Mirrors DisassembleNameInputRegion.py."""
    start = _addr(start_int)
    end = _addr(end_int)
    listing = currentProgram.getListing()
    targets = set()
    inst = listing.getInstructionAt(start)
    if inst is None:
        inst = listing.getInstructionAfter(start)
    scanned = 0
    while inst is not None and inst.getAddress().compareTo(end) < 0:
        for ref in inst.getReferencesFrom():
            rt = ref.getReferenceType()
            if rt.isData() or rt.isRead() or rt.isWrite():
                to_addr = ref.getToAddress()
                if to_addr.getOffset() < 0x08000000:
                    continue
                if to_addr.getOffset() >= 0x0A000000:
                    continue
                targets.add(to_addr)
        scanned += 1
        inst = listing.getInstructionAfter(inst.getAddress())
    print("[ok]   scanned %d instructions, collected %d unique data targets" % (scanned, len(targets)))

    defined = 0
    skipped_aligned = 0
    skipped_conflict = 0
    for t in targets:
        if (t.getOffset() & 3) != 0:
            skipped_aligned += 1
            continue
        data_at = listing.getDataAt(t)
        if data_at is not None and data_at.isDefined():
            if data_at.getLength() == 4:
                continue
            skipped_conflict += 1
            continue
        if RUN_DRY:
            defined += 1
            continue
        ok = False
        try:
            createData(t, DWordDataType())
            ok = True
        except (JavaException, Exception):
            pass
        if not ok:
            try:
                clearListing(t, t.add(3))
                createData(t, DWordDataType())
                ok = True
            except (JavaException, Exception):
                pass
        if ok:
            defined += 1
        else:
            skipped_conflict += 1
    print("[ok]   defined %d new Dword targets (%d skipped misaligned, %d skipped conflict)"
          % (defined, skipped_aligned, skipped_conflict))
    return defined


def main():
    print("=== DisassembleCampaignRegion ===  RUN_DRY=%s" % RUN_DRY)

    # Phase 1: Force-disassemble the 42 dispatch handlers.
    print("\n[Phase 1] Force-disassemble campaign state handlers (table1=26 + table2=16)")
    for addr_int, name in ALL_HANDLERS:
        force_disassemble_thumb(addr_int)
        create_function(addr_int, name)

    # Phase 1.5: sweep full code range to define any new PC-rel data targets that
    # propagation may have surfaced. Same range as DisassembleNameInputRegion.py.
    print("\n[Phase 1.5] Scan full code range 0x080000C0..0x084C7637 for PC-rel data targets")
    scan_region_define_data(0x080000C0, 0x084C7637)

    print("\n[done] DisassembleCampaignRegion")
    print("Next: tools\\asm-regen\\ghidra-run-script.bat PromoteCallTargetsToFunctions.py")


main()
