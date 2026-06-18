# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF09Seg8Blocks.py -- p5 file09 Seg-8 R4 disasm (blocks B1..B4)
#
# B1: fn_eligible_mustering_dark_scorpions @ 0x080765b0 (ROM_INCBIN 0x765b0/0x2c)
#   - THUMB+1 ref: 0x080765b1 from FS table at GBA:0x09e41a68 (CID=0x169e MUSTERING_DARK_SCORPIONS_CID)
#   - No 2B pad; fn body starts at 0x080765b0 (ROM byte 0xf0b5 = push {r4-r7,lr})
#   - fn code: 0x080765b0..0x080765d3 (0x24 bytes)
#   - Literal pool: 2 DWords at 0x080765d4 and 0x080765d8
#       0x080765d4: 0x0201b290 (gDuelPhaseFlags)
#       0x080765d8: 0x080765dc (B2 dispatch table base)
#   - Block range: [0x080765b0, 0x080765db] (0x2c bytes)
#
# B2: 5 mustering_dark_scorpions dispatch sub-stubs @ 0x080765f0..0x0807678b
#   - ROM_INCBIN 0x765f0/0x19c
#   - Dispatch table: 5 raw entries at 0x765dc..0x765ef
#       0x080765dc: 0x08076780  (sub_6780, first = highest index)
#       0x080765e0: 0x080766d8  (sub_66d8)
#       0x080765e4: 0x080766a8  (sub_66a8)
#       0x080765e8: 0x08076616  (sub_6616)
#       0x080765ec: 0x080765f0  (sub_65f0, last = index 0 / default)
#   - 5 unique sub-stub entry points (ordered by address):
#       sub_65f0 @ 0x080765f0
#       sub_6616 @ 0x08076616
#       sub_66a8 @ 0x080766a8
#       sub_66d8 @ 0x080766d8
#       sub_6780 @ 0x08076780
#   - Block range: [0x080765f0, 0x0807678b]
#   - Literal pool DWords found in block (by address scan):
#       0x0807666c: 0x0201c4e0 (gP1LifePoints)
#       0x08076674: 0x0201e2a8 (gDuelCardCtxBase-like EWRAM)
#       0x08076678: 0x08076511 (ROM code ptr, check_effect_slot_card_type_flag_by_id+1)
#       0x08076688: 0x08076511 (same, duplicate)
#       0x080766c8: 0x0201b290 (gDuelPhaseFlags)
#       0x080766cc: 0x0201c4e0 (gP1LifePoints)
#       0x08076718: 0x0201c600 (gP1FieldArrayCBase)
#
# B3: fn_eligible_spell_vanishing @ 0x080767ac (ROM_INCBIN 0x767aa/0x32)
#   - 2B zero pad at 0x080767aa (0x0000); fn body starts at 0x080767ac
#   - THUMB+1 ref: 0x080767ad from FS table at GBA:0x09e41b28 (CID=0x16a6 SPELL_VANISHING_CID)
#   - fn code: 0x080767ac..0x080767d3 (0x28 bytes code + pool)
#   - Literal pool: 2 DWords
#       0x080767d4: 0x0201b290 (gDuelPhaseFlags)
#       0x080767d8: 0x080767dc (B4 dispatch table base)
#   - Block range: [0x080767aa, 0x080767db] (0x32 bytes)
#   - NOTE: do NOT clearListing the 2B pad at 0x080767aa; start clearListing at 0x080767ac
#   - NOTE: create DWord at pad addr 0x080767aa after setting TMode
#
# B4: 7 spell_vanishing dispatch sub-stubs @ 0x080767f8..0x08076907
#   - ROM_INCBIN 0x767f8/0x110
#   - Dispatch table: 7 raw entries at 0x767dc..0x767f7
#       0x080767dc: 0x080768cc  (sub_68cc, first = highest index)
#       0x080767e0: 0x080768b8  (sub_68b8)
#       0x080767e4: 0x080768aa  (sub_68aa)
#       0x080767e8: 0x08076890  (sub_6890)
#       0x080767ec: 0x08076818  (sub_6818)
#       0x080767f0: 0x08076804  (sub_6804)
#       0x080767f4: 0x080767f8  (sub_67f8, last = index 0 / default)
#   - 7 unique sub-stub entry points (ordered by address):
#       sub_67f8 @ 0x080767f8
#       sub_6804 @ 0x08076804
#       sub_6818 @ 0x08076818
#       sub_6890 @ 0x08076890
#       sub_68aa @ 0x080768aa
#       sub_68b8 @ 0x080768b8
#       sub_68cc @ 0x080768cc
#   - Block range: [0x080767f8, 0x08076907]
#   - Literal pool DWords found in block (by address scan):
#       0x08076884: 0x0201c4e0 (gP1LifePoints)
#   - NOTE: 272B block; patterns from Seg-7 B4 apply
#
# Pattern: clearListing -> setTMode -> per-stub DisassembleCommand -> force-DWord pool words
#
# NOTE: All labels are pure ASCII. No CJK in EOL/plate.

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

# B1: fn_eligible_mustering_dark_scorpions
B1_LO   = 0x080765b0   # fn body start (no pad)
B1_HI   = 0x080765db   # end of incbin (0x2c bytes from 0x765b0; 0x765b0+0x2c-1=0x765db)
B1_POOL_DWORDS = [0x080765d4, 0x080765d8]  # gDuelPhaseFlags + B2 dispatch table ptr

# B2: mustering_dark_scorpions sub-stubs
B2_LO = 0x080765f0
B2_HI = 0x0807678b   # 0x765f0 + 0x19c - 1
B2_STUBS = [
    (0x080765f0, 'mustering_dark_scorpions_sub_65f0'),
    (0x08076616, 'mustering_dark_scorpions_sub_6616'),
    (0x080766a8, 'mustering_dark_scorpions_sub_66a8'),
    (0x080766d8, 'mustering_dark_scorpions_sub_66d8'),
    (0x08076780, 'mustering_dark_scorpions_sub_6780'),
]
# Pool DWords in B2: pre-force known address-like words to avoid GAS "value too big"
B2_POOL_DWORDS = [
    0x0807666c,  # 0x0201c4e0 (gP1LifePoints)
    0x08076674,  # 0x0201e2a8 (EWRAM addr)
    0x08076678,  # 0x08076511 (ROM code ptr THUMB+1)
    0x08076688,  # 0x08076511 (duplicate)
    0x080766c8,  # 0x0201b290 (gDuelPhaseFlags)
    0x080766cc,  # 0x0201c4e0 (gP1LifePoints)
    0x08076718,  # 0x0201c600 (gP1FieldArrayCBase)
]

# B3: fn_eligible_spell_vanishing (2B pad at 0x080767aa, fn starts at 0x080767ac)
B3_PAD   = 0x080767aa  # 2B alignment pad (0x0000)
B3_LO    = 0x080767ac  # fn body start
B3_HI    = 0x080767db  # end of incbin (0x767aa + 0x32 - 1 = 0x767db)
B3_POOL_DWORDS = [0x080767d4, 0x080767d8]  # gDuelPhaseFlags + B4 dispatch table ptr

# B4: spell_vanishing sub-stubs
B4_LO = 0x080767f8
B4_HI = 0x08076907   # 0x767f8 + 0x110 - 1
B4_STUBS = [
    (0x080767f8, 'spell_vanishing_sub_67f8'),
    (0x08076804, 'spell_vanishing_sub_6804'),
    (0x08076818, 'spell_vanishing_sub_6818'),
    (0x08076890, 'spell_vanishing_sub_6890'),
    (0x080768aa, 'spell_vanishing_sub_68aa'),
    (0x080768b8, 'spell_vanishing_sub_68b8'),
    (0x080768cc, 'spell_vanishing_sub_68cc'),
]
# Pool DWords in B4: pre-force known address-like words
B4_POOL_DWORDS = [
    0x08076884,  # 0x0201c4e0 (gP1LifePoints)
]

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

def _disasm_at(sa, hi, label):
    stub_lo = _addr(sa)
    stub_hi = _addr(hi)
    cmd = DisassembleCommand(stub_lo, AddressSet(stub_lo, stub_hi), True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm %s @ 0x%08x: %s" % (label, sa, cmd.getStatusMsg()))
    else:
        print("[ok ] disasm %s @ 0x%08x" % (label, sa))

def _disasm_stubs(stubs, block_hi, block_name):
    """Disassemble a list of (start_addr, label) sub-stubs up to block_hi."""
    for i, (sa, label) in enumerate(stubs):
        # end address: next stub start - 1, or block_hi for last stub
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
    # 4B clearListing only (avoid clobbering adjacent code)
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
    print("=== DisassembleF09Seg8Blocks (DRY=%s) ===" % DRY)
    print("  B1: fn_eligible_mustering_dark_scorpions @ 0x080765b0 (0x2cB, no pad)")
    print("  B2: mustering_dark_scorpions sub-stubs @ 0x080765f0 (0x19cB, 5 stubs)")
    print("  B3: fn_eligible_spell_vanishing @ 0x080767ac (2B pad @0x767aa, 0x32B total)")
    print("  B4: spell_vanishing sub-stubs @ 0x080767f8 (0x110B, 7 stubs)")

    if DRY:
        print("[dry] B1: clearListing(0x080765b0..0x080765db) + setTMode + disasm + pool x2 + createFn")
        print("[dry] B2: clearListing(0x080765f0..0x0807678b) + setTMode + pool x7 + 5x disasm + labels")
        print("[dry] B3: clearListing(0x080767ac..0x080767db) [NOT 0x767aa pad] + setTMode + createDWord pad + disasm + pool x2 + createFn")
        print("[dry] B4: clearListing(0x080767f8..0x08076907) + setTMode + pool x1 + 7x disasm + labels")
        return

    listing = currentProgram.getListing()

    # -----------------------------------------------------------------------
    # Block1: fn_eligible_mustering_dark_scorpions @ 0x080765b0
    # -----------------------------------------------------------------------
    print("\n--- Block1: fn_eligible_mustering_dark_scorpions @ 0x080765b0 ---")
    print("    CID=0x169e MUSTERING_DARK_SCORPIONS_CID; FS THUMB+1 @ 0x09e41a68")
    print("    Range: 0x%08x..0x%08x (0x2c bytes, no pad)" % (B1_LO, B1_HI))

    _clear_listing(B1_LO, B1_HI)
    _set_tmode(B1_LO, B1_HI)

    # Disassemble fn body (code ends before literal pool at 0x080765d4)
    b1_code_hi = B1_POOL_DWORDS[0] - 1  # 0x080765d3
    _disasm_at(B1_LO, b1_code_hi, 'fn_eligible_mustering_dark_scorpions')

    # Force DWords for literal pool (2 DWords: gDuelPhaseFlags + B2 dispatch table ptr)
    for dw_addr in B1_POOL_DWORDS:
        _force_dword(dw_addr)

    # createFunction
    _create_function(B1_LO, 'fn_eligible_mustering_dark_scorpions', B1_HI)
    _add_label(B1_LO, 'fn_eligible_mustering_dark_scorpions')

    # -----------------------------------------------------------------------
    # Block2: mustering_dark_scorpions sub-stubs @ 0x080765f0
    # -----------------------------------------------------------------------
    print("\n--- Block2: mustering_dark_scorpions_sub_stubs @ 0x080765f0 ---")
    print("    ROM_INCBIN 0x765f0/0x19c; 5 sub-stubs via 5-entry dispatch table")
    print("    Pool words: 0x666c/0x6674/0x6678/0x6688/0x66c8/0x66cc/0x6718")

    _clear_listing(B2_LO, B2_HI)
    _set_tmode(B2_LO, B2_HI)

    # Force DWords for known literal pool words BEFORE disasm
    # (avoids GAS "value too big" on EWRAM/ROM address operands)
    for dw_addr in B2_POOL_DWORDS:
        _force_dword(dw_addr)

    # Disassemble each sub-stub
    _disasm_stubs(B2_STUBS, B2_HI, "B2")

    # -----------------------------------------------------------------------
    # Block3: fn_eligible_spell_vanishing @ 0x080767ac (2B pad at 0x080767aa)
    # -----------------------------------------------------------------------
    print("\n--- Block3: fn_eligible_spell_vanishing @ 0x080767ac ---")
    print("    CID=0x16a6 SPELL_VANISHING_CID; FS THUMB+1 @ 0x09e41b28")
    print("    2B zero pad at 0x080767aa (NOT cleared); fn code at 0x080767ac")
    print("    fn code range: 0x%08x..0x%08x" % (B3_LO, B3_HI))

    # NOTE: Do NOT clearListing the 2B pad at 0x080767aa
    _clear_listing(B3_LO, B3_HI)
    _set_tmode(B3_LO, B3_HI)

    # Create DWord at pad addr to make Ghidra not interpret it as code
    # (2B pad, but we create a Word, not DWord, since it's only 2 bytes)
    # Actually pad is only 2B = we leave it as-is (Ghidra already has it as data
    # from the ROM_INCBIN); just ensure fn body is correct
    # Force DWords for literal pool (2 DWords: gDuelPhaseFlags + B4 dispatch table ptr)
    b3_code_hi = B3_POOL_DWORDS[0] - 1  # 0x080767d3
    _disasm_at(B3_LO, b3_code_hi, 'fn_eligible_spell_vanishing')

    for dw_addr in B3_POOL_DWORDS:
        _force_dword(dw_addr)

    # createFunction at 0x080767ac (not the pad address)
    _create_function(B3_LO, 'fn_eligible_spell_vanishing', B3_HI)
    _add_label(B3_LO, 'fn_eligible_spell_vanishing')

    # -----------------------------------------------------------------------
    # Block4: spell_vanishing sub-stubs @ 0x080767f8
    # -----------------------------------------------------------------------
    print("\n--- Block4: spell_vanishing_sub_stubs @ 0x080767f8 ---")
    print("    ROM_INCBIN 0x767f8/0x110; 7 sub-stubs via 7-entry dispatch table")
    print("    Pool word: 0x6884 (0x0201c4e0 gP1LifePoints)")

    _clear_listing(B4_LO, B4_HI)
    _set_tmode(B4_LO, B4_HI)

    # Force DWords for known literal pool words BEFORE disasm
    for dw_addr in B4_POOL_DWORDS:
        _force_dword(dw_addr)

    # Disassemble each sub-stub
    _disasm_stubs(B4_STUBS, B4_HI, "B4")

    # -----------------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------------
    print("\n--- Instruction counts ---")
    for lo_int, hi_int, name in [
        (B1_LO, B1_HI, "B1"),
        (B2_LO, B2_HI, "B2"),
        (B3_LO, B3_HI, "B3"),
        (B4_LO, B4_HI, "B4"),
    ]:
        lo_a = _addr(lo_int)
        hi_a = _addr(hi_int)
        n = 0
        inst = listing.getInstructionAt(lo_a)
        while inst is not None and inst.getAddress().compareTo(hi_a) <= 0:
            n += 1
            inst = listing.getInstructionAfter(inst.getAddress())
        print("  %s: %d instructions in 0x%08x..0x%08x" % (name, n, lo_int, hi_int))

    print("\n=== DisassembleF09Seg8Blocks DONE ===")
    print("  New functions: fn_eligible_mustering_dark_scorpions @ 0x080765b0")
    print("                 fn_eligible_spell_vanishing @ 0x080767ac")
    print("  Sub-stub labels: B2=5 + B4=7 = 12 total")


main()
