# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF09Seg10aBlocks.py -- p5 file09 Seg-10a R4 disasm (blocks B1..B5)
#
# B1: fn_eligible @ 0x08078a90 (ROM_INCBIN 0x78a90/0x44)
#   - THUMB+1 ref: 0x08078a91 from FS table @ GBA:0x09e45e78 (CID=0x1796 EMISSARY_OF_THE_AFTERLIFE_CID)
#   - fn prologue: 0x08078a90 = 0xb530 (PUSH {r4,r5,lr})
#   - Literal pool DWords in B1:
#       0x08078ac4: 0x0201c4e0 (gP1LifePoints)
#       0x08078ac8: 0x00001ce8 (P1LP_BLOCK2_OFF_1CE8)
#       0x08078acc: 0x0201b290 (gDuelPhaseFlags)
#       0x08078ad0: 0x000004a4 (EQUIP_PHASE_FRAME_OFF)
#   - Code ends at 0x08078ac0 (mov pc,r0 = 0x4687); pad 0x08078ac2 (0x0000)
#   - Block range: [0x08078a90, 0x08078ad4) = 0x44 bytes
#
# B2: sub-stubs for equip state dispatch @ 0x08078b24 (ROM_INCBIN 0x78b24/0xd4)
#   - 8 unique entry points from PTR_DAT_08078ad8 dispatch table (19 entries):
#       0x08078b24  0x08078b38  0x08078b58  0x08078b70
#       0x08078b7c  0x08078b9c  0x08078bd8  0x08078bec
#   - Known literal pool DWords in B2:
#       0x08078b34: 0x000004a4 (EQUIP_PHASE_FRAME_OFF)
#       0x08078b6c: 0x00001daa (LP_CARD_TRACK_NEXT_OFF)
#       0x08078b8c: 0x0000???? (alignment word = 0x00000000)
#       0x08078b90: 0x000004a4 (EQUIP_PHASE_FRAME_OFF)
#       0x08078bcc: 0x0201b290 (gDuelPhaseFlags)
#       0x08078bd0: 0x000004a4 (EQUIP_PHASE_FRAME_OFF)
#       0x08078bf4: 0x00001ce8 (P1LP_BLOCK2_OFF_1CE8)
#   - Block range: [0x08078b24, 0x08078bf8) = 0xd4 bytes
#
# B3: fn_eligible THE_FIRST_SARCOPHAGUS (CID=0x17af) + sub-stub @ 0x08078fde (ROM_INCBIN 0x78fde/0xf6)
#   - THUMB+1 ref: fn_eligible at 0x08078fe0 (THUMB+1=0x08078fe1 from 0x09e44b10)
#   - Sub-stub at 0x08079040 (raw ref from 0x084d6254 in asm/07)
#   - 2-byte alignment pad at 0x08078fde (0x0000) before fn_eligible
#   - Literal pool DWords in B3:
#       0x08079092: ??? (check below; might be code? No: 0x08680000 looks like code pair)
#       0x08079098: 0x0201c510 (gDuelFieldSlots - existing ewram.inc constant)
#       0x080790cc: 0x0201b290 (gDuelPhaseFlags)
#       0x080790d0: 0x080790d4 (ptr to B4 dispatch table start)
#   - Block range: [0x08078fde, 0x080790d4) = 0xf6 bytes
#   - Note: B3 ends at 0x080790d4 (excl); B4 dispatch table starts at 0x080790d4
#
# B4: sub-stubs + fn_eligible HUMAN_WAVE_TACTICS (CID=0x17b2) @ 0x08079148 (ROM_INCBIN 0x79148/0x1ec)
#   - B4 dispatch table at 0x080790d4..0x08079148 (29 entries raw-ptrs; outside B4 block)
#   - 10 unique entry points (address order):
#       0x08079148  0x08079188  0x0807919c  0x08079238
#       0x080792a8  0x080792b4  0x080792c0  0x080792cc
#       0x080792e4  0x080792f8  (fn_eligible = THUMB+1 ref from 0x09e44b28)
#   - 2-byte alignment pad at 0x080792f6 (0x0000) before fn_eligible at 0x080792f8
#   - Literal pool DWords in B4:
#       0x08079180: 0x0201b290 (gDuelPhaseFlags)
#       0x0807921c: 0x0201b290 (gDuelPhaseFlags)
#       0x080792a4: 0x0201c510 (gDuelFieldSlots)
#       0x0807932c: 0x0201b290 (gDuelPhaseFlags)
#       0x08079330: 0x08079334 (ptr; B5 dispatch table starts at 0x08079334)
#   - Block range: [0x08079148, 0x08079334) = 0x1ec bytes
#
# B5: sub-stubs for equip-zone-sprite sequence @ 0x080793ac (ROM_INCBIN 0x793ac/0x154)
#   - B5 dispatch table at 0x08079334..0x080793ab (30 entries raw-ptrs; outside B5 block)
#   - 7 unique entry points (address order):
#       0x080793ac  0x080793ec  0x0807940a  0x08079434
#       0x080794da  0x080794ec  0x080794f6  (default sub-stub, raw=24)
#   - Note: THUMB ref 0x080793cd from 0x09ef6c6e is NOT 0x09e4xxxx -> compressed data artifact
#     0x080793cc is mid-stub within 0x080793ac body (not a separate entry point)
#   - Literal pool DWords in B5:
#       0x08079428: 0x0201b290 (gDuelPhaseFlags)
#       0x08079430: 0x0201c4e0 (gP1LifePoints)
#       0x08079470: 0x0201b290 (gDuelPhaseFlags)
#       0x080794c4: 0x0201b290 (gDuelPhaseFlags)
#   - Block range: [0x080793ac, 0x08079500) = 0x154 bytes
#
# Pattern: clearListing -> setTMode -> force_dword pool words -> per-stub DisassembleCommand
#          -> createFunction for fn_eligible stubs
#
# NOTE: All labels are pure ASCII. No CJK in EOL/plate.
# NOTE: DRY mode skips all modifications.

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

# B1: fn_eligible_emissary_of_the_afterlife
B1_LO      = 0x08078a90   # fn body start
B1_HI      = 0x08078ad3   # end of incbin (0x78a90 + 0x44 - 1)
B1_FN_NAME = 'fn_eligible_emissary_of_the_afterlife'
# Pool DWords in B1 (after code ends at 0x78ac0; pad 0x78ac2; pools 0x78ac4..)
B1_POOL_DWORDS = [
    0x08078ac4,  # 0x0201c4e0 gP1LifePoints
    0x08078ac8,  # 0x00001ce8 P1LP_BLOCK2_OFF_1CE8
    0x08078acc,  # 0x0201b290 gDuelPhaseFlags
    0x08078ad0,  # 0x000004a4 EQUIP_PHASE_FRAME_OFF
]

# B2: equip_state_dispatch_sub_stubs
B2_LO = 0x08078b24
B2_HI = 0x08078bf7   # 0x78b24 + 0xd4 - 1
B2_STUBS = [
    (0x08078b24, 'equip_state_sub_b24'),
    (0x08078b38, 'equip_state_sub_b38'),
    (0x08078b58, 'equip_state_sub_b58'),
    (0x08078b70, 'equip_state_sub_b70'),
    (0x08078b7c, 'equip_state_sub_b7c'),
    (0x08078b9c, 'equip_state_sub_b9c'),
    (0x08078bd8, 'equip_state_sub_bd8'),
    (0x08078bec, 'equip_state_default_bec'),
]
# Known pool DWords in B2 (EQUIP_PHASE_FRAME_OFF, LP_CARD_TRACK_NEXT_OFF, gDuelPhaseFlags, P1LP_BLOCK2_OFF_1CE8)
B2_POOL_DWORDS = [
    0x08078b34,  # 0x000004a4 EQUIP_PHASE_FRAME_OFF
    0x08078b6c,  # 0x00001daa LP_CARD_TRACK_NEXT_OFF
    0x08078b8c,  # 0x00000000 alignment word (force split)
    0x08078b90,  # 0x000004a4 EQUIP_PHASE_FRAME_OFF
    0x08078bcc,  # 0x0201b290 gDuelPhaseFlags
    0x08078bd0,  # 0x000004a4 EQUIP_PHASE_FRAME_OFF
    0x08078bf4,  # 0x00001ce8 P1LP_BLOCK2_OFF_1CE8
]

# B3: fn_eligible_first_sarcophagus + sub-stub
# Block has 2-byte pad at 0x78fde, then fn at 0x78fe0
B3_LO      = 0x08078fde   # block start (pad + fn_eligible body)
B3_HI      = 0x080790d3   # end of incbin (0x78fde + 0xf6 - 1)
B3_FN_LO   = 0x08078fe0   # fn_eligible body start (after 2-byte pad)
B3_FN_NAME = 'fn_eligible_first_sarcophagus'
B3_SUB_LO  = 0x08079040   # sub-stub (raw ref from 0x084d6254)
# Pool DWords in B3
B3_POOL_DWORDS = [
    0x08079098,  # 0x0201c510 gDuelFieldSlots
    0x080790cc,  # 0x0201b290 gDuelPhaseFlags
    0x080790d0,  # 0x080790d4 ptr to B4 dispatch table
]

# B4: 9 sub-stubs + fn_eligible_human_wave_tactics
# B4 dispatch table [0x080790d4..0x08079148) is OUTSIDE B4 block (already structured in asm)
B4_LO      = 0x08079148   # block start
B4_HI      = 0x08079333   # end of incbin (0x79148 + 0x1ec - 1)
B4_FN_LO   = 0x080792f8   # fn_eligible body start
B4_FN_NAME = 'fn_eligible_human_wave_tactics'
# 2-byte pad at 0x080792f6 (0x0000) before fn_eligible
# 10 entry points in address order
B4_STUBS = [
    (0x08079148, 'human_wave_sub_9148'),
    (0x08079188, 'human_wave_sub_9188'),
    (0x0807919c, 'human_wave_sub_919c'),
    (0x08079238, 'human_wave_sub_9238'),
    (0x080792a8, 'human_wave_sub_92a8'),
    (0x080792b4, 'human_wave_sub_92b4'),
    (0x080792c0, 'human_wave_sub_92c0'),
    (0x080792cc, 'human_wave_sub_92cc'),
    (0x080792e4, 'human_wave_default_92e4'),
    (0x080792f8, 'fn_eligible_human_wave_tactics'),   # fn_eligible (same as B4_FN_NAME)
]
# Pool DWords in B4
B4_POOL_DWORDS = [
    0x08079180,  # 0x0201b290 gDuelPhaseFlags
    0x0807921c,  # 0x0201b290 gDuelPhaseFlags
    0x080792a4,  # 0x0201c510 gDuelFieldSlots
    0x0807932c,  # 0x0201b290 gDuelPhaseFlags
    0x08079330,  # 0x08079334 ptr to B5 dispatch table
]

# B5: 7 sub-stubs for equip-zone-sprite sequence
# B5 dispatch table [0x08079334..0x080793ab) is OUTSIDE B5 block (structured in asm)
B5_LO = 0x080793ac
B5_HI = 0x080794ff   # 0x793ac + 0x154 - 1
B5_STUBS = [
    (0x080793ac, 'equip_zone_seq_sub_93ac'),
    (0x080793ec, 'equip_zone_seq_sub_93ec'),
    (0x0807940a, 'equip_zone_seq_sub_940a'),
    (0x08079434, 'equip_zone_seq_sub_9434'),
    (0x080794da, 'equip_zone_seq_sub_94da'),
    (0x080794ec, 'equip_zone_seq_sub_94ec'),
    (0x080794f6, 'equip_zone_seq_default_94f6'),
]
# Pool DWords in B5
B5_POOL_DWORDS = [
    0x08079428,  # 0x0201b290 gDuelPhaseFlags
    0x08079430,  # 0x0201c4e0 gP1LifePoints
    0x08079470,  # 0x0201b290 gDuelPhaseFlags
    0x080794c4,  # 0x0201b290 gDuelPhaseFlags
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
        print("[ok ] label 0x%08x -> %s (exists)" % (addr_int, label))

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
    print("=== DisassembleF09Seg10aBlocks (DRY=%s) ===" % DRY)
    print("  B1: fn_eligible_emissary_of_the_afterlife @ 0x08078a90 (0x44B)")
    print("  B2: equip_state_dispatch sub-stubs @ 0x08078b24 (0xd4B, 8 stubs)")
    print("  B3: fn_eligible_first_sarcophagus @ 0x08078fe0 + sub-stub @ 0x08079040 (range 0x78fde/0xf6)")
    print("  B4: human_wave_tactics sub-stubs + fn_eligible @ 0x08079148 (0x1ecB, 10 entries)")
    print("  B5: equip_zone_seq sub-stubs @ 0x080793ac (0x154B, 7 stubs)")

    if DRY:
        print("[dry] B1: clearListing(0x08078a90..0x08078ad3) + setTMode + pool x4 + disasm + createFn")
        print("[dry] B2: clearListing(0x08078b24..0x08078bf7) + setTMode + pool x7 + 8x disasm + labels")
        print("[dry] B3: clearListing(0x08078fde..0x080790d3) + setTMode + pad@0x78fde + pool x3 + 2x disasm + createFn")
        print("[dry] B4: clearListing(0x08079148..0x08079333) + setTMode + pool x5 + 10x disasm + createFn")
        print("[dry] B5: clearListing(0x080793ac..0x080794ff) + setTMode + pool x4 + 7x disasm + labels")
        return

    listing = currentProgram.getListing()

    # -----------------------------------------------------------------------
    # Block1: fn_eligible_emissary_of_the_afterlife @ 0x08078a90
    # -----------------------------------------------------------------------
    print("\n--- Block1: fn_eligible_emissary_of_the_afterlife @ 0x08078a90 ---")
    print("    CID=0x1796 EMISSARY_OF_THE_AFTERLIFE_CID; FS THUMB+1 @ 0x09e45e78")
    print("    Range: 0x%08x..0x%08x (0x44 bytes)" % (B1_LO, B1_HI))

    _clear_listing(B1_LO, B1_HI)
    _set_tmode(B1_LO, B1_HI)

    # Force DWords for literal pool BEFORE disasm
    for dw_addr in B1_POOL_DWORDS:
        _force_dword(dw_addr)

    # Disassemble fn body (code ends at 0x78ac0; pad 0x78ac2 = .zero 2)
    # DisassembleCommand will stop at mov pc,r0 (0x4687) naturally
    b1_code_hi = 0x08078ac1  # inclusive end of code (0x78ac0..0x78ac1 = 0x4687)
    _disasm_at(B1_LO, b1_code_hi, B1_FN_NAME)

    _create_function(B1_LO, B1_FN_NAME, B1_HI)
    _add_label(B1_LO, B1_FN_NAME)

    # -----------------------------------------------------------------------
    # Block2: equip_state_dispatch sub-stubs @ 0x08078b24
    # -----------------------------------------------------------------------
    print("\n--- Block2: equip_state_dispatch sub-stubs @ 0x08078b24 ---")
    print("    ROM_INCBIN 0x78b24/0xd4; 19-entry dispatch table @PTR_DAT_08078ad8")
    print("    8 unique sub-stub entry points")

    _clear_listing(B2_LO, B2_HI)
    _set_tmode(B2_LO, B2_HI)

    # Force DWords for known literal pool words BEFORE disasm
    for dw_addr in B2_POOL_DWORDS:
        _force_dword(dw_addr)

    # Disassemble each sub-stub
    _disasm_stubs(B2_STUBS, B2_HI, "B2")

    # -----------------------------------------------------------------------
    # Block3: fn_eligible_first_sarcophagus @ 0x08078fe0 + sub @ 0x08079040
    # -----------------------------------------------------------------------
    print("\n--- Block3: fn_eligible_first_sarcophagus @ 0x08078fe0 ---")
    print("    CID=0x17af THE_FIRST_SARCOPHAGUS_CID; FS THUMB+1 @ 0x09e44b10")
    print("    2-byte pad at 0x08078fde; fn body start 0x08078fe0")
    print("    Sub-stub @ 0x08079040 (raw ref from 0x084d6254)")
    print("    Range: 0x%08x..0x%08x (0xf6 bytes)" % (B3_LO, B3_HI))

    _clear_listing(B3_LO, B3_HI)
    _set_tmode(B3_FN_LO, B3_HI)  # set TMode starting from fn body (skip 2-byte pad)

    # Force DWords for known literal pool words BEFORE disasm
    for dw_addr in B3_POOL_DWORDS:
        _force_dword(dw_addr)

    # Disassemble fn body (starts at 0x78fe0, not 0x78fde)
    # DisassembleCommand on fn_eligible
    _disasm_at(B3_FN_LO, B3_SUB_LO - 1, B3_FN_NAME)
    _create_function(B3_FN_LO, B3_FN_NAME, B3_HI)
    _add_label(B3_FN_LO, B3_FN_NAME)

    # Disassemble sub-stub at 0x79040
    _disasm_at(B3_SUB_LO, B3_HI, 'first_sarcophagus_sub_9040')
    _add_label(B3_SUB_LO, 'first_sarcophagus_sub_9040')

    # -----------------------------------------------------------------------
    # Block4: human_wave_tactics sub-stubs + fn_eligible @ 0x08079148
    # -----------------------------------------------------------------------
    print("\n--- Block4: human_wave_tactics sub-stubs + fn_eligible @ 0x08079148 ---")
    print("    ROM_INCBIN 0x79148/0x1ec; 29-entry dispatch table @0x080790d4..0x08079148")
    print("    CID=0x17b2 HUMAN_WAVE_TACTICS_CID; fn_eligible @ 0x080792f8 (FS THUMB+1 @ 0x09e44b28)")
    print("    2-byte pad at 0x080792f6; 10 unique entry points total")

    _clear_listing(B4_LO, B4_HI)
    _set_tmode(B4_LO, B4_HI)

    # Force DWords for known literal pool words BEFORE disasm
    for dw_addr in B4_POOL_DWORDS:
        _force_dword(dw_addr)

    # Disassemble each sub-stub and fn_eligible in address order
    _disasm_stubs(B4_STUBS, B4_HI, "B4")

    # Create function for fn_eligible
    _create_function(B4_FN_LO, B4_FN_NAME, B4_HI)

    # -----------------------------------------------------------------------
    # Block5: equip_zone_seq sub-stubs @ 0x080793ac
    # -----------------------------------------------------------------------
    print("\n--- Block5: equip_zone_seq sub-stubs @ 0x080793ac ---")
    print("    ROM_INCBIN 0x793ac/0x154; 30-entry dispatch table @0x08079334..0x080793ab")
    print("    7 unique sub-stub entry points")
    print("    NOTE: THUMB ref 0x793cd from 0x09ef6c6e is compressed-data artifact (NOT 0x09e4xxxx)")
    print("    0x793cc is mid-stub within 0x793ac body, NOT a separate entry point")

    _clear_listing(B5_LO, B5_HI)
    _set_tmode(B5_LO, B5_HI)

    # Force DWords for known literal pool words BEFORE disasm
    for dw_addr in B5_POOL_DWORDS:
        _force_dword(dw_addr)

    # Disassemble each sub-stub
    _disasm_stubs(B5_STUBS, B5_HI, "B5")

    # -----------------------------------------------------------------------
    # Summary: instruction counts
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

    print("\n=== DisassembleF09Seg10aBlocks DONE ===")
    print("  New functions: fn_eligible_emissary_of_the_afterlife @ 0x08078a90")
    print("                 fn_eligible_first_sarcophagus @ 0x08078fe0")
    print("                 fn_eligible_human_wave_tactics @ 0x080792f8")
    print("  Sub-stub labels: B2=8 + B3-sub=1 + B4=9 + B5=7 = 25 total")

main()
