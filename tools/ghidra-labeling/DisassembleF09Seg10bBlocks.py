# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF09Seg10bBlocks.py -- p5 file09 Seg-10b R4 disasm (blocks B6..B10)
#
# B6: fn_eligible shared by ORDER_TO_CHARGE (CID=0x179f) + ORDER_TO_SMASH (CID=0x17b8)
#     Range: [0x08079660, 0x080796ab) -- note: 0x7965c is 4-byte THUMB align pad before fn body
#     Wait -- proposal says entry @0x7965c, block [0x7965c..0x796ac), 0x50 bytes
#     ROM bytes: 0x0807965c: 0x1c04b5f0 => PUSH {r4,r5,r6,r7,lr}; mov r4,r0
#     So fn body starts directly at 0x7965c (no pad). Pools: 0x79670,0x7967c,0x796a4,0x796a8
#     (0x79670=0x0000179f ORDER_TO_CHARGE_CID; 0x7967c=fn ptr; 0x796a4=fn ptr; 0x796a8=gDuelPhaseFlags)
#
# B7: 5 sub-stubs for equip slot activation dispatch
#     Range: [0x080796c4, 0x080797cf)
#     Entry points (from PTR_DAT_080796b0 5-entry table):
#       0x080796c4  0x0807970e  0x08079734  0x08079760  0x080797c4
#     Pools scattered through B7 (see B7_POOL_DWORDS below)
#
# B8: fn_eligible for FAMILIAR_KNIGHT (CID=0x17c3)
#     Range: [0x08079a1c, 0x08079a63)
#     Entry point: 0x08079a1c
#     Pools: 0x79a54,0x79a58,0x79a5c,0x79a60
#
# B9: 6 sub-stubs + fn_eligible for INFERNO_TEMPEST (CID=0x17ca)
#     Range: [0x08079adc, 0x08079c17)
#     Entry points (address order): 0x79adc 0x79af8 0x79b62 0x79b80 0x79bb4 0x79bd0 0x79bdc
#     Pools scattered through B9 (see B9_POOL_DWORDS below)
#
# B10: 9 sub-stubs for Neo-Daedalus equip LP sequence
#     Range: [0x08079c9c, 0x08079e5f)
#     Entry points (from PTR_DAT_08079c1c 32-entry table):
#       0x79c9c  0x79cd4  0x79d24  0x79d74  0x79da4  0x79dc0  0x79dd8  0x79df0  0x79e4e
#     Pools scattered through B10 (see B10_POOL_DWORDS below)
#
# Pattern: clearListing -> setTMode -> force_dword pool words -> per-stub DisassembleCommand
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

# B6: fn_eligible_order_to_charge_or_smash
# THUMB ref @ 0x9e42098 (CID=0x179f ORDER_TO_CHARGE) + 0x9e42200 (CID=0x17b8 ORDER_TO_SMASH)
# Single fn body starts at 0x7965c; pool after code
B6_LO      = 0x08079660   # fn body start (skipping 4-byte incbin pad at 0x7965c/0x7965e?)
B6_HI      = 0x080796ab   # end of block (0x7965c + 0x50 - 1)
B6_FN_LO   = 0x08079660   # actual code start (0x7965c bytes check: 0xb5f0 = PUSH, then 0x1c04)
# Wait: ROM bytes at 0x7965c = 0x1c04b5f0 in little-endian 32-bit = half-words 0xb5f0, 0x1c04
# 0xb5f0 = PUSH {r4,r5,r6,r7,lr} => fn_eligible starts at 0x7965c
B6_FN_LO   = 0x0807965c   # fn body start
B6_HI      = 0x080796ab   # end of block (0x7965c + 0x50 - 1)
B6_FN_NAME = 'fn_eligible_order_to_charge_or_smash'
# Pool DWords in B6:
# 0x79670: 0x0000179f (ORDER_TO_CHARGE_CID)
# 0x7967c: 0x080507ad (fn ptr: check_equip_activation_eligible+1 or similar)
# 0x796a4: 0x08051e95 (fn ptr)
# 0x796a8: 0x0201b290 (gDuelPhaseFlags)
B6_POOL_DWORDS = [
    0x08079670,  # 0x0000179f ORDER_TO_CHARGE_CID (literal comparison)
    0x0807967c,  # 0x080507ad fn ptr
    0x080796a4,  # 0x08051e95 fn ptr
    0x080796a8,  # 0x0201b290 gDuelPhaseFlags
]

# B7: 5 sub-stubs for equip slot activation dispatch
# PTR_DAT_080796b0 5-entry table has these raw targets:
B7_LO = 0x080796c4
B7_HI = 0x080797cf   # 0x796c4 + 0x10c - 1
B7_STUBS = [
    (0x080796c4, 'equip_act_sub_96c4'),
    (0x0807970e, 'equip_act_sub_970e'),
    (0x08079734, 'equip_act_sub_9734'),
    (0x08079760, 'equip_act_sub_9760'),
    (0x080797c4, 'equip_act_default_97c4'),
]
# Pool DWords in B7 (scattered across stubs):
B7_POOL_DWORDS = [
    0x0807972c,  # 0x0201b290 gDuelPhaseFlags (stub equip_act_sub_96c4)
    0x08079730,  # 0x000004a4 EQUIP_PHASE_FRAME_OFF
    0x0807975c,  # 0x000004a4 EQUIP_PHASE_FRAME_OFF (stub equip_act_sub_970e)
    0x08079798,  # 0x0201c4e0 gP1LifePoints (stub equip_act_sub_9760)
    0x0807979c,  # 0x00001d68 ELIGIB_SPRITE_CTRL_OFF
    0x080797a0,  # 0x00001d6c ELIGIB_ANIM_STATE_OFF
    0x080797a4,  # 0x0201b290 gDuelPhaseFlags
    0x080797a8,  # 0x000004a4 EQUIP_PHASE_FRAME_OFF
    0x080797bc,  # 0x0201b290 gDuelPhaseFlags (stub equip_act_sub_97c4)
    0x080797c0,  # 0x000004a4 EQUIP_PHASE_FRAME_OFF
]

# B8: fn_eligible for FAMILIAR_KNIGHT (CID=0x17c3)
# THUMB ref @ 0x9e45ef0; CID @ 0x9e45eec=0x17c3
B8_LO      = 0x08079a1c
B8_HI      = 0x08079a63   # 0x79a1c + 0x48 - 1
B8_FN_NAME = 'fn_eligible_familiar_knight'
# Pool DWords in B8:
B8_POOL_DWORDS = [
    0x08079a54,  # 0x0201c4e0 gP1LifePoints
    0x08079a58,  # 0x00001ce8 P1LP_BLOCK2_OFF_1CE8
    0x08079a5c,  # 0x0201b290 gDuelPhaseFlags
    0x08079a60,  # 0x000004a4 EQUIP_PHASE_FRAME_OFF
]

# B9: 6 sub-stubs + fn_eligible for INFERNO_TEMPEST (CID=0x17ca)
# Sub-stub raw refs from PTR_DAT_08079a68 29-entry table:
#   0x79adc 0x79af8 0x79b62 0x79b80 0x79bb4 0x79bd0 (default, raw=24)
# fn_eligible: THUMB+1 from 0x9e42230; CID @ 0x9e4222c = 0x17ca
#   0x79bdc (fn_eligible body)
B9_LO = 0x08079adc
B9_HI = 0x08079c17   # 0x79adc + 0x13c - 1
B9_FN_LO   = 0x08079bdc
B9_FN_NAME = 'fn_eligible_inferno_tempest'
B9_STUBS = [
    (0x08079adc, 'inferno_tempest_sub_9adc'),
    (0x08079af8, 'inferno_tempest_sub_9af8'),
    (0x08079b62, 'inferno_tempest_sub_9b62'),
    (0x08079b80, 'inferno_tempest_sub_9b80'),
    (0x08079bb4, 'inferno_tempest_sub_9bb4'),
    (0x08079bd0, 'inferno_tempest_default_9bd0'),
    (0x08079bdc, 'fn_eligible_inferno_tempest'),   # fn_eligible (same as B9_FN_NAME)
]
# Pool DWords in B9 (scattered):
B9_POOL_DWORDS = [
    0x08079af0,  # 0x0201b290 gDuelPhaseFlags (sub_9adc pool)
    0x08079af4,  # 0x000004a4 EQUIP_PHASE_FRAME_OFF
    0x08079b48,  # 0x0201e2a0 gDuelCardCtxBase (sub_9af8 pool)
    0x08079b4c,  # 0x0201c4e0 gP1LifePoints
    0x08079b50,  # 0x00001da8 (field offset)
    0x08079b7c,  # 0x00001da8 (field offset, sub_9b62 pool)
    0x08079bac,  # 0x00001da8 (field offset, sub_9b80 pool)
    0x08079bb0,  # 0x00000868 PLAYER_BLOCK_STRIDE
    0x08079bc8,  # 0x000004a4 EQUIP_PHASE_FRAME_OFF (sub_9bb4/9bd0 pool)
    0x08079c10,  # 0x0201b290 gDuelPhaseFlags (fn_eligible pool)
    0x08079c14,  # 0x000004a4 EQUIP_PHASE_FRAME_OFF
]

# B10: 9 sub-stubs for Neo-Daedalus equip LP sequence
# PTR_DAT_08079c1c 32-entry table; 9 unique entry points:
#   0x79c9c 0x79cd4 0x79d24 0x79d74 0x79da4 0x79dc0 0x79dd8 0x79df0 0x79e4e(default)
# Note: THUMB refs 0x79e02|1 (from 0x98355b1) and 0x79e1c|1 (from 0x874a8df)
#       are NOT 0x09e4xxxx -> compressed-data artifacts; both within stub[7] 0x79df0..0x79e4d
B10_LO = 0x08079c9c
B10_HI = 0x08079e5f   # 0x79c9c + 0x1c4 - 1
B10_STUBS = [
    (0x08079c9c, 'neo_daedalus_lp_sub_9c9c'),
    (0x08079cd4, 'neo_daedalus_lp_sub_9cd4'),
    (0x08079d24, 'neo_daedalus_lp_sub_9d24'),
    (0x08079d74, 'neo_daedalus_lp_sub_9d74'),
    (0x08079da4, 'neo_daedalus_lp_sub_9da4'),
    (0x08079dc0, 'neo_daedalus_lp_sub_9dc0'),
    (0x08079dd8, 'neo_daedalus_lp_sub_9dd8'),
    (0x08079df0, 'neo_daedalus_lp_sub_9df0'),
    (0x08079e4e, 'neo_daedalus_lp_default_9e4e'),
]
# Pool DWords in B10 (scattered):
B10_POOL_DWORDS = [
    0x08079cc4,  # 0x0201b290 gDuelPhaseFlags (sub_9c9c pool)
    0x08079cc8,  # 0x000004a4 EQUIP_PHASE_FRAME_OFF
    0x08079ccc,  # 0x0201c4e0 gP1LifePoints
    0x08079cd0,  # 0x00001ce8 P1LP_BLOCK2_OFF_1CE8
    0x08079d1c,  # 0x0201c4e0 gP1LifePoints (sub_9cd4 pool)
    0x08079d20,  # 0x00000868 PLAYER_BLOCK_STRIDE
    0x08079d6c,  # 0x0201c4e0 gP1LifePoints (sub_9d24 pool)
    0x08079d70,  # 0x00000868 PLAYER_BLOCK_STRIDE
    0x08079d90,  # 0x000004a4 EQUIP_PHASE_FRAME_OFF (sub_9d74 pool)
    0x08079d94,  # 0x0201c4e0 gP1LifePoints
    0x08079d98,  # 0x00001ce8 P1LP_BLOCK2_OFF_1CE8
    0x08079db8,  # 0x0201c4e0 gP1LifePoints (sub_9da4 pool)
    0x08079dbc,  # 0x00001ce8 P1LP_BLOCK2_OFF_1CE8
    0x08079dd0,  # 0x0201c4e0 gP1LifePoints (sub_9dc0 pool)
    0x08079dd4,  # 0x00001ce8 P1LP_BLOCK2_OFF_1CE8
    0x08079de8,  # 0x0201c4e0 gP1LifePoints (sub_9dd8 pool)
    0x08079dec,  # 0x00001ce8 P1LP_BLOCK2_OFF_1CE8
    0x08079e04,  # 0x0201c4e0 gP1LifePoints (sub_9df0 pool)
    0x08079e08,  # 0x00001ce8 P1LP_BLOCK2_OFF_1CE8
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
    print("=== DisassembleF09Seg10bBlocks (DRY=%s) ===" % DRY)
    print("  B6: fn_eligible_order_to_charge_or_smash @ 0x0807965c (0x50B)")
    print("  B7: equip_act dispatch sub-stubs @ 0x080796c4 (0x10cB, 5 stubs)")
    print("  B8: fn_eligible_familiar_knight @ 0x08079a1c (0x48B)")
    print("  B9: inferno_tempest sub-stubs + fn_eligible @ 0x08079adc (0x13cB, 7 entries)")
    print("  B10: neo_daedalus_lp sub-stubs @ 0x08079c9c (0x1c4B, 9 stubs)")

    if DRY:
        print("[dry] B6: clearListing(0x0807965c..0x080796ab) + setTMode + pool x4 + disasm + createFn")
        print("[dry] B7: clearListing(0x080796c4..0x080797cf) + setTMode + pool x10 + 5x disasm + labels")
        print("[dry] B8: clearListing(0x08079a1c..0x08079a63) + setTMode + pool x4 + disasm + createFn")
        print("[dry] B9: clearListing(0x08079adc..0x08079c17) + setTMode + pool x11 + 7x disasm + createFn")
        print("[dry] B10: clearListing(0x08079c9c..0x08079e5f) + setTMode + pool x19 + 9x disasm + labels")
        return

    listing = currentProgram.getListing()

    # -----------------------------------------------------------------------
    # Block6: fn_eligible_order_to_charge_or_smash @ 0x0807965c
    # -----------------------------------------------------------------------
    print("\n--- Block6: fn_eligible_order_to_charge_or_smash @ 0x0807965c ---")
    print("    CID=0x179f ORDER_TO_CHARGE_CID + CID=0x17b8 ORDER_TO_SMASH_CID (shared fn_eligible)")
    print("    FS THUMB+1 @ 0x09e42098 (CID=0x179f) + 0x09e42200 (CID=0x17b8)")
    print("    Range: 0x%08x..0x%08x (0x50 bytes)" % (B6_LO, B6_HI))

    _clear_listing(B6_LO, B6_HI)
    _set_tmode(B6_LO, B6_HI)

    # Force DWords for literal pool BEFORE disasm
    for dw_addr in B6_POOL_DWORDS:
        _force_dword(dw_addr)

    # Disassemble fn body (single fn_eligible covering the block)
    _disasm_at(B6_LO, B6_HI, B6_FN_NAME)

    _create_function(B6_LO, B6_FN_NAME, B6_HI)
    _add_label(B6_LO, B6_FN_NAME)

    # -----------------------------------------------------------------------
    # Block7: equip_act dispatch sub-stubs @ 0x080796c4
    # -----------------------------------------------------------------------
    print("\n--- Block7: equip_act dispatch sub-stubs @ 0x080796c4 ---")
    print("    ROM_INCBIN 0x796c4/0x10c; PTR_DAT_080796b0 5-entry table")
    print("    5 unique sub-stub entry points")

    _clear_listing(B7_LO, B7_HI)
    _set_tmode(B7_LO, B7_HI)

    # Force DWords for known literal pool words BEFORE disasm
    for dw_addr in B7_POOL_DWORDS:
        _force_dword(dw_addr)

    # Disassemble each sub-stub
    _disasm_stubs(B7_STUBS, B7_HI, "B7")

    # -----------------------------------------------------------------------
    # Block8: fn_eligible_familiar_knight @ 0x08079a1c
    # -----------------------------------------------------------------------
    print("\n--- Block8: fn_eligible_familiar_knight @ 0x08079a1c ---")
    print("    CID=0x17c3 FAMILIAR_KNIGHT_CID; FS THUMB+1 @ 0x09e45ef0")
    print("    Range: 0x%08x..0x%08x (0x48 bytes)" % (B8_LO, B8_HI))

    _clear_listing(B8_LO, B8_HI)
    _set_tmode(B8_LO, B8_HI)

    # Force DWords for literal pool BEFORE disasm
    for dw_addr in B8_POOL_DWORDS:
        _force_dword(dw_addr)

    # Disassemble fn body
    _disasm_at(B8_LO, B8_HI, B8_FN_NAME)

    _create_function(B8_LO, B8_FN_NAME, B8_HI)
    _add_label(B8_LO, B8_FN_NAME)

    # -----------------------------------------------------------------------
    # Block9: inferno_tempest sub-stubs + fn_eligible @ 0x08079adc
    # -----------------------------------------------------------------------
    print("\n--- Block9: inferno_tempest sub-stubs + fn_eligible @ 0x08079adc ---")
    print("    ROM_INCBIN 0x79adc/0x13c; PTR_DAT_08079a68 29-entry table -> 6 sub-stubs")
    print("    CID=0x17ca INFERNO_TEMPEST_CID; fn_eligible @ 0x08079bdc (THUMB+1 @ 0x9e42230)")
    print("    7 entry points total (6 stubs + 1 fn_eligible)")

    _clear_listing(B9_LO, B9_HI)
    _set_tmode(B9_LO, B9_HI)

    # Force DWords for known literal pool words BEFORE disasm
    for dw_addr in B9_POOL_DWORDS:
        _force_dword(dw_addr)

    # Disassemble each sub-stub and fn_eligible in address order
    _disasm_stubs(B9_STUBS, B9_HI, "B9")

    # Create function for fn_eligible
    _create_function(B9_FN_LO, B9_FN_NAME, B9_HI)

    # -----------------------------------------------------------------------
    # Block10: neo_daedalus_lp sub-stubs @ 0x08079c9c
    # -----------------------------------------------------------------------
    print("\n--- Block10: neo_daedalus_lp sub-stubs @ 0x08079c9c ---")
    print("    ROM_INCBIN 0x79c9c/0x1c4; PTR_DAT_08079c1c 32-entry table -> 9 unique stubs")
    print("    NOTE: THUMB refs 0x79e02|1 (0x98355b1) + 0x79e1c|1 (0x874a8df) are compressed-data artifacts")
    print("    Both 0x79e02 and 0x79e1c fall within stub[7] 0x79df0..0x79e4d -> disasm covers them")

    _clear_listing(B10_LO, B10_HI)
    _set_tmode(B10_LO, B10_HI)

    # Force DWords for known literal pool words BEFORE disasm
    for dw_addr in B10_POOL_DWORDS:
        _force_dword(dw_addr)

    # Disassemble each sub-stub
    _disasm_stubs(B10_STUBS, B10_HI, "B10")

    # -----------------------------------------------------------------------
    # Summary: instruction counts
    # -----------------------------------------------------------------------
    print("\n--- Instruction counts ---")
    for lo_int, hi_int, name in [
        (B6_LO, B6_HI, "B6"),
        (B7_LO, B7_HI, "B7"),
        (B8_LO, B8_HI, "B8"),
        (B9_LO, B9_HI, "B9"),
        (B10_LO, B10_HI, "B10"),
    ]:
        lo_a = _addr(lo_int)
        hi_a = _addr(hi_int)
        n = 0
        inst = listing.getInstructionAt(lo_a)
        while inst is not None and inst.getAddress().compareTo(hi_a) <= 0:
            n += 1
            inst = listing.getInstructionAfter(inst.getAddress())
        print("  %s: %d instructions in 0x%08x..0x%08x" % (name, n, lo_int, hi_int))

    print("\n=== DisassembleF09Seg10bBlocks DONE ===")
    print("  New functions: fn_eligible_order_to_charge_or_smash @ 0x0807965c")
    print("                 fn_eligible_familiar_knight @ 0x08079a1c")
    print("                 fn_eligible_inferno_tempest @ 0x08079bdc")
    print("  Sub-stub labels: B7=5 + B9=6 + B10=9 = 20 total")

main()
