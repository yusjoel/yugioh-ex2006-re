# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF09Seg9bBlocks.py -- p5 file09 Seg-9b R4 disasm (blocks B6..B9)
#
# B6: fn_eligible_dangerous_machine_type6 @ 0x08077ecc (ROM_INCBIN 0x77ecc/0x5c)
#   - THUMB+1 ref: 0x08077ecd from FS table at GBA:0x09e448d0 (CID=0x1738 DANGEROUS_MACHINE_TYPE6_CID)
#   - fn prologue: 0x08077ecc = 0x1c04b510 => push{r4,lr}; adds r4,r0,#0 (valid THUMB prologue)
#   - Literal pool DWords:
#       0x08077ee8: 0x0201b290 (gDuelPhaseFlags)
#       0x08077f18: 0x0201c4e0 (gP1LifePoints)
#       0x08077f1c: 0x00001da8 (LP_CARD_TRACK_BASE_OFF)
#   - Block range: [0x08077ecc, 0x08077f27] (0x5c bytes)
#
# B7: dangerous_machine sub-stubs @ 0x08077f44..0x08078003 (ROM_INCBIN 0x77f44/0xc0)
#   - 6-entry raw dispatch table at 0x08077f2c..0x08077f43 (outside B7, already structured)
#   - 6 unique sub-stub entry points:
#       sub_7f44 @ 0x08077f44  (entry[0])
#       sub_7f56 @ 0x08077f56  (entry[1])
#       sub_7f6c @ 0x08077f6c  (entry[2])
#       sub_7f7a @ 0x08077f7a  (entry[3])
#       sub_7f86 @ 0x08077f86  (entry[4])
#       sub_7f9c @ 0x08077f9c  (entry[5])
#   - Literal pool DWords in B7:
#       0x08077fcc: 0x080507ad (fn_ptr OUTSIDE segment; force_dword OK)
#       0x08077ff0: 0x0201c4e0 (gP1LifePoints)
#       0x08077ff4: 0x00001d68 (offset constant)
#       0x08077ff8: 0x00001d6c (offset constant)
#   - GUARD: 0x08077f94 (B7+0x50) = 0xe033 (CODE: `b` branch inside sub_7f86 body)
#            DO NOT force_dword(0x08077f94) -- that would corrupt code
#   - Block range: [0x08077f44, 0x08078003] (0xc0 bytes)
#
# B8: fn_eligible_monster_gate @ 0x080782c0 (ROM_INCBIN 0x782c0/0x2c)
#   - THUMB+1 ref: 0x080782c1 from FS table at GBA:0x09e41f18 (CID=0x175c MONSTER_GATE_CID)
#   - fn prologue: 0x080782c0 = 0x4647b5f0 => push{r4..r7,lr}; mov r7,r8 (valid THUMB prologue)
#   - Literal pool DWords:
#       0x080782e4: 0x0201b290 (gDuelPhaseFlags)
#       0x080782e8: 0x080782ec (dispatch table ptr -> 31-entry table)
#   - Block range: [0x080782c0, 0x080782eb] (0x2c bytes)
#
# B9: monster_gate sub-stubs @ 0x08078368..0x080784b3 (ROM_INCBIN 0x78368/0x14c)
#   - 31-entry raw dispatch table at 0x080782ec..0x08078367 (already structured in asm)
#   - 8 unique sub-stub entry points:
#       sub_8368 @ 0x08078368  (entry[30])
#       sub_83a0 @ 0x080783a0  (entry[28])
#       sub_83a8 @ 0x080783a8  (entry[27])
#       sub_8476 @ 0x08078476  (entry[26]; BL 0x0804a870; b 0x080784a8, 6 bytes)
#       sub_847c @ 0x0807847c  (entry[2])
#       sub_848c @ 0x0807848c  (entry[1])
#       sub_849e @ 0x0807849e  (entry[0])
#       default_84a8 @ 0x080784a8  (entries[3-25,29], default)
#   - NOTE: 0x0807841c (B9+0xb4) is mid-BL (0x0807841a=f7bb BL-hi; 0x0807841c=f8cd BL-lo)
#           NOT a valid THUMB entry. DisassembleCommand(0x0807841c) would corrupt sub_83a8.
#           EXCLUDED from disasm targets.
#   - Block range: [0x08078368, 0x080784b3] (0x14c bytes)
#
# Pattern: clearListing -> setTMode -> force_dword pool words BEFORE disasm
#          -> per-stub DisassembleCommand -> createFunction for fn_eligible stubs
#
# NOTE: All labels are pure ASCII. No CJK in EOL/plate.
# NOTE: DRY mode skips all modifications; check console output for plan.

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.address import AddressSet
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

# ---------------------------------------------------------------------------
# Block definitions
# ---------------------------------------------------------------------------

# B6: fn_eligible_dangerous_machine_type6
B6_LO       = 0x08077ecc   # fn body start
B6_HI       = 0x08077f27   # end of incbin (0x77ecc + 0x5c - 1)
B6_FN_NAME  = 'fn_eligible_dangerous_machine_type6'
# Pool DWords (EWRAM/ROM addresses) in B6 -- force before disasm
# 0x08077ee8: 0x0201b290 gDuelPhaseFlags
# 0x08077f18: 0x0201c4e0 gP1LifePoints
# 0x08077f1c: 0x00001da8 LP_CARD_TRACK_BASE_OFF (constant offset, but force anyway)
B6_POOL_DWORDS = [0x08077ee8, 0x08077f18, 0x08077f1c]

# B7: dangerous_machine sub-stubs
B7_LO = 0x08077f44
B7_HI = 0x08078003   # 0x77f44 + 0xc0 - 1
B7_STUBS = [
    (0x08077f44, 'dangerous_machine_sub_7f44'),
    (0x08077f56, 'dangerous_machine_sub_7f56'),
    (0x08077f6c, 'dangerous_machine_sub_7f6c'),
    (0x08077f7a, 'dangerous_machine_sub_7f7a'),
    (0x08077f86, 'dangerous_machine_sub_7f86'),
    (0x08077f9c, 'dangerous_machine_sub_7f9c'),
]
# Pool DWords in B7: only EWRAM/ROM-like addresses and fn_ptrs
# GUARD: 0x08077f94 is CODE (b branch 0xe033 inside sub_7f86) -- NOT force_dword
B7_POOL_DWORDS = [
    0x08077fcc,  # 0x080507ad fn_ptr (outside segment; force_dword to create DWord)
    0x08077ff0,  # 0x0201c4e0 gP1LifePoints
    0x08077ff4,  # 0x00001d68 offset constant
    0x08077ff8,  # 0x00001d6c offset constant
]

# B8: fn_eligible_monster_gate
B8_LO       = 0x080782c0   # fn body start
B8_HI       = 0x080782eb   # end of incbin (0x782c0 + 0x2c - 1)
B8_FN_NAME  = 'fn_eligible_monster_gate'
# Pool DWords in B8
# 0x080782e4: 0x0201b290 gDuelPhaseFlags
# 0x080782e8: 0x080782ec dispatch table ptr
B8_POOL_DWORDS = [0x080782e4, 0x080782e8]

# B9: monster_gate sub-stubs
B9_LO = 0x08078368
B9_HI = 0x080784b3   # 0x78368 + 0x14c - 1
B9_STUBS = [
    (0x08078368, 'monster_gate_sub_8368'),
    (0x080783a0, 'monster_gate_sub_83a0'),
    (0x080783a8, 'monster_gate_sub_83a8'),
    # NOTE: skip 0x0807841c (mid-BL, NOT a valid entry)
    (0x08078476, 'monster_gate_sub_8476'),   # entry[26]: BL decrement_lp_bar; b default
    (0x0807847c, 'monster_gate_sub_847c'),
    (0x0807848c, 'monster_gate_sub_848c'),
    (0x0807849e, 'monster_gate_sub_849e'),
    (0x080784a8, 'monster_gate_default_84a8'),
]
# B9 does NOT have a simple sorted pool list -- let disasm auto-detect within block
# We only force_dword for values Ghidra might misidentify as instructions
# The sub-stubs themselves are short; their pool words are inline within the stubs
B9_POOL_DWORDS = []  # disasm handles pool words in each stub body automatically

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
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

def _clear_listing(lo_int, hi_int):
    lo = _addr(lo_int)
    hi = _addr(hi_int)
    try:
        clearListing(lo, hi)
        print("[ok ] clearListing 0x%08x..0x%08x" % (lo_int, hi_int))
    except Exception as e:
        print("[warn] clearListing 0x%08x..0x%08x: %s" % (lo_int, hi_int, e))

def _disasm_at(sa, hi_int, label):
    stub_lo = _addr(sa)
    stub_hi = _addr(hi_int)
    cmd = DisassembleCommand(stub_lo, AddressSet(stub_lo, stub_hi), True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm %s @ 0x%08x: %s" % (label, sa, cmd.getStatusMsg()))
    else:
        print("[ok ] disasm %s @ 0x%08x" % (label, sa))

def _disasm_stubs(stubs, block_hi, block_name):
    """Disassemble a list of (start_addr, label) sub-stubs, each to its own range."""
    for i, (sa, label) in enumerate(stubs):
        if i + 1 < len(stubs):
            hi = stubs[i + 1][0] - 1
        else:
            hi = block_hi
        _disasm_at(sa, hi, label)
        _add_label(sa, label)

def _force_dword(addr_int):
    a = _addr(addr_int)
    a_end = _addr(addr_int + 3)
    listing = currentProgram.getListing()
    try:
        clearListing(a, a_end)
    except Exception as e:
        print("[warn] force_dword clearListing @ 0x%08x: %s" % (addr_int, e))
    try:
        listing.createData(a, ghidra.program.model.data.DWordDataType.dataType)
        print("[ok ] force_dword @ 0x%08x" % addr_int)
    except Exception as e:
        print("[warn] force_dword createData @ 0x%08x: %s" % (addr_int, e))

def _add_label(addr_int, label):
    sym_tbl = currentProgram.getSymbolTable()
    a = _addr(addr_int)
    existing = sym_tbl.getSymbols(a)
    names = [s.getName() for s in existing]
    if label not in names:
        sym_tbl.createLabel(a, label, SourceType.USER_DEFINED)
        print("[ok ] label 0x%08x -> %s" % (addr_int, label))
    else:
        print("[ok ] label 0x%08x -> %s (already exists)" % (addr_int, label))

def _create_function(addr_int, name, body_hi):
    a = _addr(addr_int)
    fm = currentProgram.getFunctionManager()
    fn = fm.getFunctionAt(a)
    if fn is not None:
        if fn.getName() != name:
            fn.setName(name, SourceType.USER_DEFINED)
            print("[ok ] function renamed 0x%08x -> %s" % (addr_int, name))
        else:
            print("[ok ] function 0x%08x already named %s" % (addr_int, name))
    else:
        try:
            fm.createFunction(name, a,
                              AddressSet(_addr(addr_int), _addr(body_hi)),
                              SourceType.USER_DEFINED)
            print("[ok ] createFunction %s @ 0x%08x" % (name, addr_int))
        except Exception as e:
            print("[warn] createFunction %s @ 0x%08x: %s" % (name, addr_int, e))

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== DisassembleF09Seg9bBlocks (DRY=%s) ===" % DRY)
    print("  B6: fn_eligible_dangerous_machine_type6 @ 0x08077ecc (0x5cB)")
    print("  B7: dangerous_machine sub-stubs @ 0x08077f44 (0xc0B, 6 stubs)")
    print("  B8: fn_eligible_monster_gate @ 0x080782c0 (0x2cB)")
    print("  B9: monster_gate sub-stubs @ 0x08078368 (0x14cB, 8 stubs)")

    if DRY:
        print("[dry] B6: clearListing(0x08077ecc..0x08077f27) + setTMode + pool x3 + disasm + createFn")
        print("[dry] B7: clearListing(0x08077f44..0x08078003) + setTMode + pool x4 + 6x disasm + labels")
        print("[dry] B7 GUARD: force_dword(0x08077fcc) YES; force_dword(0x08077f94) NO (CODE)")
        print("[dry] B8: clearListing(0x080782c0..0x080782eb) + setTMode + pool x2 + disasm + createFn")
        print("[dry] B9: clearListing(0x08078368..0x080784b3) + setTMode + 8x disasm + labels")
        print("[dry] B9 GUARD: 0x0807841c (mid-BL) excluded from disasm targets")
        return

    listing = currentProgram.getListing()

    # -----------------------------------------------------------------------
    # Block6: fn_eligible_dangerous_machine_type6 @ 0x08077ecc
    # -----------------------------------------------------------------------
    print("\n--- Block6: fn_eligible_dangerous_machine_type6 @ 0x08077ecc ---")
    print("    CID=0x1738 DANGEROUS_MACHINE_TYPE6_CID; FS THUMB+1 @ 0x09e448d0")
    print("    Range: 0x%08x..0x%08x (0x5c bytes)" % (B6_LO, B6_HI))

    _clear_listing(B6_LO, B6_HI)
    _set_tmode(B6_LO, B6_HI)

    # Force DWords for literal pool BEFORE disasm
    for dw_addr in B6_POOL_DWORDS:
        _force_dword(dw_addr)

    # Disassemble fn body (code ends before first pool word)
    b6_code_hi = B6_POOL_DWORDS[0] - 1  # 0x08077ee7
    _disasm_at(B6_LO, b6_code_hi, B6_FN_NAME)

    _create_function(B6_LO, B6_FN_NAME, B6_HI)
    _add_label(B6_LO, B6_FN_NAME)

    # -----------------------------------------------------------------------
    # Block7: dangerous_machine sub-stubs @ 0x08077f44
    # -----------------------------------------------------------------------
    print("\n--- Block7: dangerous_machine_sub_stubs @ 0x08077f44 ---")
    print("    ROM_INCBIN 0x77f44/0xc0; 6-entry dispatch table @0x08077f2c..0x08077f43")
    print("    6 unique sub-stub entry points; Pool DWords: 0x7fcc/0x7ff0/0x7ff4/0x7ff8")
    print("    GUARD: 0x08077f94 is CODE (b branch 0xe033) -- NOT force_dword")

    _clear_listing(B7_LO, B7_HI)
    _set_tmode(B7_LO, B7_HI)

    # Force DWords for known literal pool words BEFORE disasm
    # EXPLICITLY: 0x08077fcc (fn_ptr 0x080507ad), 0x7ff0/0x7ff4/0x7ff8 (offsets)
    # GUARD: 0x08077f94 NOT in B7_POOL_DWORDS -- never called
    for dw_addr in B7_POOL_DWORDS:
        _force_dword(dw_addr)

    # Disassemble each sub-stub
    _disasm_stubs(B7_STUBS, B7_HI, "B7")

    # -----------------------------------------------------------------------
    # Block8: fn_eligible_monster_gate @ 0x080782c0
    # -----------------------------------------------------------------------
    print("\n--- Block8: fn_eligible_monster_gate @ 0x080782c0 ---")
    print("    CID=0x175c MONSTER_GATE_CID; FS THUMB+1 @ 0x09e41f18")
    print("    Range: 0x%08x..0x%08x (0x2c bytes)" % (B8_LO, B8_HI))

    _clear_listing(B8_LO, B8_HI)
    _set_tmode(B8_LO, B8_HI)

    # Force DWords for literal pool BEFORE disasm
    for dw_addr in B8_POOL_DWORDS:
        _force_dword(dw_addr)

    # Disassemble fn body (code ends before first pool word)
    b8_code_hi = B8_POOL_DWORDS[0] - 1  # 0x080782e3
    _disasm_at(B8_LO, b8_code_hi, B8_FN_NAME)

    _create_function(B8_LO, B8_FN_NAME, B8_HI)
    _add_label(B8_LO, B8_FN_NAME)

    # -----------------------------------------------------------------------
    # Block9: monster_gate sub-stubs @ 0x08078368
    # -----------------------------------------------------------------------
    print("\n--- Block9: monster_gate_sub_stubs @ 0x08078368 ---")
    print("    ROM_INCBIN 0x78368/0x14c; 31-entry dispatch table @0x080782ec..0x08078367")
    print("    8 unique sub-stub entry points (sub_8476 = entry[26]: BL+b, 6 bytes)")
    print("    GUARD: 0x0807841c is mid-BL instruction -- NOT a valid disasm entry")

    _clear_listing(B9_LO, B9_HI)
    _set_tmode(B9_LO, B9_HI)

    # Force DWords for known pool words BEFORE disasm (if any)
    for dw_addr in B9_POOL_DWORDS:
        _force_dword(dw_addr)

    # Disassemble each sub-stub per-target
    # Each DisassembleCommand stops at unconditional branch (b/bx/pop-pc)
    # sub_8476 is only 6 bytes (BL; b) -- DC will naturally stop at the `b`
    _disasm_stubs(B9_STUBS, B9_HI, "B9")

    # -----------------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------------
    print("\n--- Instruction counts ---")
    for lo_int, hi_int, name in [
        (B6_LO, B6_HI, "B6"),
        (B7_LO, B7_HI, "B7"),
        (B8_LO, B8_HI, "B8"),
        (B9_LO, B9_HI, "B9"),
    ]:
        lo_a = _addr(lo_int)
        hi_a = _addr(hi_int)
        n = 0
        inst = listing.getInstructionAt(lo_a)
        while inst is not None and inst.getAddress().compareTo(hi_a) <= 0:
            n += 1
            inst = listing.getInstructionAfter(inst.getAddress())
        print("  %s: %d instructions in 0x%08x..0x%08x" % (name, n, lo_int, hi_int))

    print("\n=== DisassembleF09Seg9bBlocks DONE ===")
    print("  New functions: fn_eligible_dangerous_machine_type6 @ 0x08077ecc")
    print("                 fn_eligible_monster_gate @ 0x080782c0")
    print("  Sub-stub labels: B7=6 + B9=8 = 14 total")
    print("  B7 GUARD confirmed: 0x08077f94 NOT force_dword'd (CODE)")
    print("  B9 GUARD confirmed: 0x0807841c NOT disasm'd (mid-BL)")

main()
