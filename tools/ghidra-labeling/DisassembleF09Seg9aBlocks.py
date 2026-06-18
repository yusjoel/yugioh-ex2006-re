# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF09Seg9aBlocks.py -- p5 file09 Seg-9a R4 disasm (blocks B1..B5)
#
# B1: fn_eligible_spatial_collapse @ 0x0807757c (ROM_INCBIN 0x7757c/0x2c)
#   - THUMB+1 ref: 0x0807757d from FS table at GBA:0x09e41ca8 (CID=0x16df SPATIAL_COLLAPSE_CARD_ID)
#   - fn prologue: 0x0807757c = 0xb530 (push {r4,r5,lr}); valid THUMB prologue
#   - Literal pool at +0x24..+0x2b (2 DWords):
#       0x080775a0: 0x0201b290 (gDuelPhaseFlags)
#       0x080775a4: 0x000004a4 (EQUIP_PHASE_FRAME_OFF)
#   - Block range: [0x0807757c, 0x080775a7] (0x2c bytes)
#
# B2: spatial_collapse sub-stubs @ 0x080775d0..0x08077677 (ROM_INCBIN 0x775d0/0xa8)
#   - 9-entry raw dispatch table at PTR_DAT_080775ac (0x080775ac..0x080775cf)
#   - 6 unique sub-stub entry points:
#       sub_75d0 @ 0x080775d0  (entry[8] = table last)
#       sub_75ec @ 0x080775ec  (entry[?])
#       sub_7602 @ 0x08077602  (entry[?])
#       sub_762a @ 0x0807762a  (entry[?])
#       sub_7648 @ 0x08077648  (entry[0] = table first)
#       default_7670 @ 0x08077670  (entry[?], appears 4x in table)
#   - Literal pool DWords found in block (by ROM scan):
#       0x080775e4: 0x0201c4e0 (gP1LifePoints)
#       0x08077640: 0x0201c4e0 (gP1LifePoints)
#       0x08077664: 0x0201c4e0 (gP1LifePoints)
#   - Block range: [0x080775d0, 0x08077677]
#   - NOTE: 0x080775e0=0x000004a4 and 0x080775e8=0x00001ce8 are constants (not EWRAM addrs);
#     0x08077644=0x00001da8 and 0x08077668=0x00001ce8 similarly; no need to force_dword these
#
# B3: fn_eligible_dimension_fusion @ 0x080779e4 (ROM_INCBIN 0x779e4/0x30)
#   - THUMB+1 ref: 0x080779e5 from FS table at GBA:0x09e41d68 (CID=0x1712 DIMENSION_FUSION_CID)
#   - fn prologue: 0x080779e4 = 0xb570 (push {r4,r5,r6,lr}); valid THUMB prologue
#   - Literal pool at +0x28..+0x2f (2 DWords):
#       0x08077a0c: 0x0201b290 (gDuelPhaseFlags)
#       0x08077a10: 0x000004a4 (EQUIP_PHASE_FRAME_OFF)
#   - Block range: [0x080779e4, 0x08077a13] (0x30 bytes)
#
# B4: jade_insect dispatch sub-stubs + embedded fn_eligible @ 0x08077a3c..0x08077b57
#   - ROM_INCBIN 0x77a3c/0x120
#   - 9-entry raw dispatch table at PTR_DAT_08077a18 (0x08077a18..0x08077a3b)
#   - 6 unique sub-stub entry points:
#       sub_7a3c @ 0x08077a3c  (entry[8] = table last)
#       sub_7a70 @ 0x08077a70  (entry[7])
#       sub_7ab4 @ 0x08077ab4  (entry[6])
#       sub_7ac2 @ 0x08077ac2  (entry[5])
#       sub_7b00 @ 0x08077b00  (entry[0] = table first)
#       sub_7b2c @ 0x08077b2c  (entries[1..4])
#   - Embedded fn_eligible at B4+0xf8 = 0x08077b34:
#       THUMB+1 ref: 0x08077b35 from FS table @0x09e41de0 (CID=0x1717 JADE_INSECT_WHISTLE_CID)
#       fn prologue: 0x08077b34 = 0xb530 (push {r4,r5,lr}); valid THUMB prologue
#       Literal pool: 0x08077b54=0x0201b290, 0x08077b58=0x08077b5c (dispatch table ptr)
#       -> createFunction(0x08077b34, "fn_eligible_jade_insect_whistle")
#   - Literal pool DWords in B4 (by ROM scan):
#       0x08077a68: 0x0201c4e0 (gP1LifePoints)
#       0x08077af4: 0x0201c4e0 (gP1LifePoints)
#       0x08077b20: 0x0201c4e0 (gP1LifePoints)
#       0x08077b54: 0x0201b290 (gDuelPhaseFlags)   <- fn_eligible pool[0]
#       0x08077b58: 0x08077b5c (dispatch table ptr) <- fn_eligible pool[1]
#   - Block range: [0x08077a3c, 0x08077b57] (0x11c bytes)
#   - NOTE: 0x08077a64=0x4a4 / 0x08077a6c=0x1ce8 / 0x08077af8=0x1da8 /
#     0x08077b1c=0x4a4 / 0x08077b24=0x1ce8 are constants (not EWRAM); skip force_dword
#
# B5: dimension_fusion sub-stubs @ 0x08077b88..0x08077c4f (ROM_INCBIN 0x77b88/0xc8)
#   - 11-entry raw dispatch table at 0x08077b5c..0x08077b87 (B4-trailing)
#   - 6 unique sub-stub entry points:
#       sub_7b88 @ 0x08077b88  (entry[10] = table last)
#       sub_7bb6 @ 0x08077bb6  (entry[9])
#       sub_7c18 @ 0x08077c18  (entry[2])
#       sub_7c2c @ 0x08077c2c  (entry[1])
#       sub_7c3a @ 0x08077c3a  (entry[0] = table first)
#       default_7c48 @ 0x08077c48  (entries[3..8], appears 6x)
#   - Literal pool DWords found in block (by ROM scan):
#       0x08077c10: 0x0201c4e0 (gP1LifePoints)
#   - Block range: [0x08077b88, 0x08077c4f] (0xc8 bytes)
#   - NOTE: 0x08077c0c=0x00008056 is not an EWRAM/ROM addr; not a pool DWord
#          0x08077c14=0x00001daa is a constant offset (not EWRAM addr)
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

# B1: fn_eligible_spatial_collapse
B1_LO   = 0x0807757c   # fn body start
B1_HI   = 0x080775a7   # end of incbin (0x7757c + 0x2c - 1)
B1_FN_NAME = 'fn_eligible_spatial_collapse'
B1_POOL_DWORDS = [0x080775a0, 0x080775a4]  # gDuelPhaseFlags + EQUIP_PHASE_FRAME_OFF

# B2: spatial_collapse sub-stubs
B2_LO = 0x080775d0
B2_HI = 0x08077677   # 0x775d0 + 0xa8 - 1
B2_STUBS = [
    (0x080775d0, 'spatial_collapse_sub_75d0'),
    (0x080775ec, 'spatial_collapse_sub_75ec'),
    (0x08077602, 'spatial_collapse_sub_7602'),
    (0x0807762a, 'spatial_collapse_sub_762a'),
    (0x08077648, 'spatial_collapse_sub_7648'),
    (0x08077670, 'spatial_collapse_default_7670'),
]
# Pool DWords in B2: only EWRAM/ROM address-like values need force_dword
B2_POOL_DWORDS = [
    0x080775e4,  # 0x0201c4e0 (gP1LifePoints)
    0x08077640,  # 0x0201c4e0 (gP1LifePoints)
    0x08077664,  # 0x0201c4e0 (gP1LifePoints)
]

# B3: fn_eligible_dimension_fusion
B3_LO   = 0x080779e4   # fn body start
B3_HI   = 0x08077a13   # end of incbin (0x779e4 + 0x30 - 1)
B3_FN_NAME = 'fn_eligible_dimension_fusion'
B3_POOL_DWORDS = [0x08077a0c, 0x08077a10]  # gDuelPhaseFlags + EQUIP_PHASE_FRAME_OFF

# B4: jade_insect sub-stubs + embedded fn_eligible
B4_LO = 0x08077a3c
B4_HI = 0x08077b57   # 0x77a3c + 0x120 - 4 - 1 = 0x77b57
# NOTE: B4 range is 0x77a3c..0x77b5b (0x120 bytes); the trailing dispatch table for B5
# is at 0x77b5c..0x77b87 (outside B4 ROM_INCBIN but contiguous); we handle B4 as
# ROM_INCBIN range 0x77a3c/0x120 = [0x77a3c, 0x77b5b]
# Correction: 0x77a3c + 0x120 = 0x77b5c; so B4 ROM_INCBIN is [0x77a3c, 0x77b5b]
# But 0x77b5c..0x77b87 is the B5 dispatch table (already structured .word entries in asm)
# So disasm B4 as [0x77a3c..0x77b57] which contains sub-stubs + fn_eligible_jade_insect
B4_STUBS = [
    (0x08077a3c, 'jade_insect_sub_7a3c'),
    (0x08077a70, 'jade_insect_sub_7a70'),
    (0x08077ab4, 'jade_insect_sub_7ab4'),
    (0x08077ac2, 'jade_insect_sub_7ac2'),
    (0x08077b00, 'jade_insect_sub_7b00'),
    (0x08077b2c, 'jade_insect_sub_7b2c'),
    # Note: 0x08077b34 is fn_eligible_jade_insect_whistle (handled separately below)
]
B4_FN_ELIGIBLE_ADDR = 0x08077b34
B4_FN_ELIGIBLE_NAME = 'fn_eligible_jade_insect_whistle'
# Pool DWords in B4 sub-stubs + fn_eligible
B4_POOL_DWORDS = [
    0x08077a68,  # 0x0201c4e0 (gP1LifePoints) in sub_7a3c
    0x08077af4,  # 0x0201c4e0 (gP1LifePoints) in sub_7ac2
    0x08077b20,  # 0x0201c4e0 (gP1LifePoints) in sub_7b00
    0x08077b54,  # 0x0201b290 (gDuelPhaseFlags) in fn_eligible pool[0]
    0x08077b58,  # 0x08077b5c (dispatch table ptr) in fn_eligible pool[1]
]

# B5: dimension_fusion sub-stubs
B5_LO = 0x08077b88
B5_HI = 0x08077c4f   # 0x77b88 + 0xc8 - 1
B5_STUBS = [
    (0x08077b88, 'dimension_fusion_sub_7b88'),
    (0x08077bb6, 'dimension_fusion_sub_7bb6'),
    (0x08077c18, 'dimension_fusion_sub_7c18'),
    (0x08077c2c, 'dimension_fusion_sub_7c2c'),
    (0x08077c3a, 'dimension_fusion_sub_7c3a'),
    (0x08077c48, 'dimension_fusion_default_7c48'),
]
# Pool DWords in B5
B5_POOL_DWORDS = [
    0x08077c10,  # 0x0201c4e0 (gP1LifePoints)
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
    """Disassemble a list of (start_addr, label) sub-stubs."""
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
    print("=== DisassembleF09Seg9aBlocks (DRY=%s) ===" % DRY)
    print("  B1: fn_eligible_spatial_collapse @ 0x0807757c (0x2cB)")
    print("  B2: spatial_collapse sub-stubs @ 0x080775d0 (0xa8B, 6 stubs)")
    print("  B3: fn_eligible_dimension_fusion @ 0x080779e4 (0x30B)")
    print("  B4: jade_insect sub-stubs + fn_eligible_jade_insect_whistle @ 0x08077a3c (0x120B)")
    print("  B5: dimension_fusion sub-stubs @ 0x08077b88 (0xc8B, 6 stubs)")

    if DRY:
        print("[dry] B1: clearListing(0x0807757c..0x080775a7) + setTMode + pool x2 + disasm + createFn")
        print("[dry] B2: clearListing(0x080775d0..0x08077677) + setTMode + pool x3 + 6x disasm + labels")
        print("[dry] B3: clearListing(0x080779e4..0x08077a13) + setTMode + pool x2 + disasm + createFn")
        print("[dry] B4: clearListing(0x08077a3c..0x08077b57) + setTMode + pool x5 + 6x sub disasm + disasm fn_elig + createFn")
        print("[dry] B5: clearListing(0x08077b88..0x08077c4f) + setTMode + pool x1 + 6x disasm + labels")
        return

    listing = currentProgram.getListing()

    # -----------------------------------------------------------------------
    # Block1: fn_eligible_spatial_collapse @ 0x0807757c
    # -----------------------------------------------------------------------
    print("\n--- Block1: fn_eligible_spatial_collapse @ 0x0807757c ---")
    print("    CID=0x16df SPATIAL_COLLAPSE_CARD_ID; FS THUMB+1 @ 0x09e41ca8")
    print("    Range: 0x%08x..0x%08x (0x2c bytes)" % (B1_LO, B1_HI))

    _clear_listing(B1_LO, B1_HI)
    _set_tmode(B1_LO, B1_HI)

    # Force DWords for literal pool BEFORE disasm
    for dw_addr in B1_POOL_DWORDS:
        _force_dword(dw_addr)

    # Disassemble fn body (code ends before literal pool at B1_POOL_DWORDS[0])
    b1_code_hi = B1_POOL_DWORDS[0] - 1  # 0x0807759f
    _disasm_at(B1_LO, b1_code_hi, B1_FN_NAME)

    _create_function(B1_LO, B1_FN_NAME, B1_HI)
    _add_label(B1_LO, B1_FN_NAME)

    # -----------------------------------------------------------------------
    # Block2: spatial_collapse sub-stubs @ 0x080775d0
    # -----------------------------------------------------------------------
    print("\n--- Block2: spatial_collapse_sub_stubs @ 0x080775d0 ---")
    print("    ROM_INCBIN 0x775d0/0xa8; 9-entry dispatch table @0x080775ac..0x080775cf")
    print("    6 unique sub-stub entry points; Pool DWords: 0x75e4/0x7640/0x7664")

    _clear_listing(B2_LO, B2_HI)
    _set_tmode(B2_LO, B2_HI)

    # Force DWords for known literal pool words BEFORE disasm
    for dw_addr in B2_POOL_DWORDS:
        _force_dword(dw_addr)

    # Disassemble each sub-stub
    _disasm_stubs(B2_STUBS, B2_HI, "B2")

    # -----------------------------------------------------------------------
    # Block3: fn_eligible_dimension_fusion @ 0x080779e4
    # -----------------------------------------------------------------------
    print("\n--- Block3: fn_eligible_dimension_fusion @ 0x080779e4 ---")
    print("    CID=0x1712 DIMENSION_FUSION_CID; FS THUMB+1 @ 0x09e41d68")
    print("    Range: 0x%08x..0x%08x (0x30 bytes)" % (B3_LO, B3_HI))

    _clear_listing(B3_LO, B3_HI)
    _set_tmode(B3_LO, B3_HI)

    # Force DWords for literal pool BEFORE disasm
    for dw_addr in B3_POOL_DWORDS:
        _force_dword(dw_addr)

    # Disassemble fn body (code ends before literal pool at B3_POOL_DWORDS[0])
    b3_code_hi = B3_POOL_DWORDS[0] - 1  # 0x08077a0b
    _disasm_at(B3_LO, b3_code_hi, B3_FN_NAME)

    _create_function(B3_LO, B3_FN_NAME, B3_HI)
    _add_label(B3_LO, B3_FN_NAME)

    # -----------------------------------------------------------------------
    # Block4: jade_insect sub-stubs + embedded fn_eligible @ 0x08077a3c
    # -----------------------------------------------------------------------
    print("\n--- Block4: jade_insect_sub_stubs + fn_eligible @ 0x08077a3c ---")
    print("    ROM_INCBIN 0x77a3c/0x120; 9-entry dispatch table @0x08077a18..0x08077a3b")
    print("    6 unique sub-stub entry points + embedded fn_eligible_jade_insect_whistle @0x08077b34")
    print("    Pool DWords: 0x7a68/0x7af4/0x7b20/0x7b54/0x7b58")

    _clear_listing(B4_LO, B4_HI)
    _set_tmode(B4_LO, B4_HI)

    # Force DWords for known literal pool words BEFORE disasm
    for dw_addr in B4_POOL_DWORDS:
        _force_dword(dw_addr)

    # Disassemble sub-stubs (up to fn_eligible_jade_insect_whistle start - 1)
    # stubs end at 0x08077b33 (just before fn_eligible at 0x08077b34)
    stubs_hi = B4_FN_ELIGIBLE_ADDR - 1  # 0x08077b33
    _disasm_stubs(B4_STUBS, stubs_hi, "B4_stubs")

    # Disassemble embedded fn_eligible_jade_insect_whistle @ 0x08077b34
    # fn code before pool: pool[0] at 0x08077b54; code hi = 0x08077b53
    fn_elig_code_hi = B4_POOL_DWORDS[3] - 1  # 0x08077b53 (B4_POOL_DWORDS[3]=0x08077b54)
    _disasm_at(B4_FN_ELIGIBLE_ADDR, fn_elig_code_hi, B4_FN_ELIGIBLE_NAME)

    _create_function(B4_FN_ELIGIBLE_ADDR, B4_FN_ELIGIBLE_NAME, B4_HI)
    _add_label(B4_FN_ELIGIBLE_ADDR, B4_FN_ELIGIBLE_NAME)

    # -----------------------------------------------------------------------
    # Block5: dimension_fusion sub-stubs @ 0x08077b88
    # -----------------------------------------------------------------------
    print("\n--- Block5: dimension_fusion_sub_stubs @ 0x08077b88 ---")
    print("    ROM_INCBIN 0x77b88/0xc8; 11-entry dispatch table @0x08077b5c..0x08077b87")
    print("    6 unique sub-stub entry points; Pool DWord: 0x7c10")

    _clear_listing(B5_LO, B5_HI)
    _set_tmode(B5_LO, B5_HI)

    # Force DWords for known literal pool words BEFORE disasm
    for dw_addr in B5_POOL_DWORDS:
        _force_dword(dw_addr)

    # Disassemble each sub-stub
    _disasm_stubs(B5_STUBS, B5_HI, "B5")

    # -----------------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------------
    print("\n--- Instruction counts ---")
    for lo_int, hi_int, name in [
        (B1_LO, B1_HI, "B1"),
        (B2_LO, B2_HI, "B2"),
        (B3_LO, B3_HI, "B3"),
        (B4_LO, B4_HI, "B4"),
        (B5_LO, B5_HI, "B5"),
    ]:
        lo_a = _addr(lo_int)
        hi_a = _addr(hi_int)
        n = 0
        inst = listing.getInstructionAt(lo_a)
        while inst is not None and inst.getAddress().compareTo(hi_a) <= 0:
            n += 1
            inst = listing.getInstructionAfter(inst.getAddress())
        print("  %s: %d instructions in 0x%08x..0x%08x" % (name, n, lo_int, hi_int))

    print("\n=== DisassembleF09Seg9aBlocks DONE ===")
    print("  New functions: fn_eligible_spatial_collapse @ 0x0807757c")
    print("                 fn_eligible_dimension_fusion @ 0x080779e4")
    print("                 fn_eligible_jade_insect_whistle @ 0x08077b34")
    print("  Sub-stub labels: B2=6 + B4_stubs=6 + B5=6 = 18 total")


main()
