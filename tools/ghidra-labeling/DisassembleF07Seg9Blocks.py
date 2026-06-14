# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF07Seg9Blocks.py -- F07 Seg-9 R4 disasm (3 blocks, 3 new functions)
#
# Block A: 0x08062ebe..0x08062efb (0x3e B)
#   2B alignment pad at 0x08062ebe
#   fn entry @ 0x08062ec0: check_opp_active_player_duel_phase_leq3
#   Shared fn_eligible for CIDs: 0x17fd (Absolute End), 0x1886 (Threatening Roar), 0x195f (Hero Barrier)
#   THUMB+1 refs at: 0x09e42358(CID=0x17fd), 0x09e426e8(CID=0x1886), 0x09e42ce8(CID=0x195f)
#   Code segs: 0xec0..0xed9 (0x1a B), 0xee4..0xef5 (0x12 B)
#   Lit pool: 0xedc(gP1LifePoints=0x0201c4e0), 0xee0(P1LP_BLOCK2_OFF_1CE8=0x1ce8), 0xef8(FIELD_STATE_OFF=0x1cf4)
#   Zero pad: 0xeda..0xedb(2B), 0xef6..0xef7(2B)
#   bx lr @ 0x08062ef4; end @ 0x08062efb
#   Semantics: returns 1 if opp is active player AND duel_phase <= 3; else 0
#
# Block B: 0x08062f38..0x08062f5f (0x28 B)
#   fn entry @ 0x08062f38: check_opp_alt_hand_count_nonzero_for_cid_188b
#   fn_eligible for CID 0x188b (D.D. Dynamite)
#   THUMB+1 ref at: 0x09e42760(CID=0x188b)
#   Code: 0xf38..0xf55 (0x1e B); zero pad: 0xf56..0xf57(2B); lit pool: 0xf58-0xf5f
#   Lit pool: 0xf58(gP1LifePoints=0x0201c4e0), 0xf5c(PLAYER_BLOCK_STRIDE=0x868)
#   bx lr @ 0x08062f54; end @ 0x08062f5f
#   Semantics: eors player_id to get opp; reads [gP1LP+opp*0x868+0x1c] (opp banished count)
#              returns 1 if nonzero (opp has banished cards), 0 if none
#   0x4048 = EOR (not AND -- verified: ALU op bits[9:6]=0001=EOR)
#
# Block C: 0x080636f8..0x0806372f (0x38 B)
#   fn entry @ 0x080636f8: check_zone_non_field_type_or_has_monsters_for_cid_1911
#   fn_eligible for CID 0x1911 (Cyber Archfiend)
#   THUMB+1 ref at: 0x09e45268(CID=0x1911)
#   Code: 0x36f8..0x3723 (0x2c B), lit pool: 0x3724-0x372b(8B), code: 0x372c-0x372f(4B)
#   Lit pool: 0x3724(gP1LifePoints=0x0201c4e0), 0x3728(PLAYER_BLOCK_STRIDE=0x868)
#   bx lr @ 0x0806372e; end @ 0x0806372f
#   Semantics: if slot[+2]&0xfc0 != 0x140 (FIELD_ZONE_TYPE=0xa0<<1): return 1
#              if field zone: check [gP1LP+player*0x868+0x0c] (monster_count); nonzero->1, zero->0
#   0x8859=ldrh r1,[r3,#2] (imm5=1; offset=imm5*2=2 bytes, NOT 4)
#
# backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260614_194352-pre-F07Seg9

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.app.cmd.function import CreateFunctionCmd
from ghidra.program.model.address import AddressSet
from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.data import DWordDataType
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


def _clear_and_set_thumb(lo_addr, hi_addr):
    lo = _addr(lo_addr)
    hi = _addr(hi_addr)
    try:
        clearListing(lo, hi)
        print("[ok ] clearListing(0x%08x..0x%08x)" % (lo_addr, hi_addr))
    except Exception as e:
        print("[warn] clearListing(0x%08x..0x%08x): %s" % (lo_addr, hi_addr, e))
    ctx = currentProgram.getProgramContext()
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        ctx.setValue(tmode, lo, hi, BigInteger.ONE)
        print("[ok ] setTMode=THUMB 0x%08x..0x%08x" % (lo_addr, hi_addr))
    else:
        print("[warn] TMode register not found")


def _disasm_flow(addr):
    """Disassemble at addr using flow continuation."""
    lo = _addr(addr)
    cmd = DisassembleCommand(lo, None, True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm_flow 0x%08x: %s" % (addr, cmd.getStatusMsg()))
        return False
    return True


def _create_function(addr, name):
    """Create a named function at addr."""
    a = _addr(addr)
    fn_mgr = currentProgram.getFunctionManager()
    sym_tbl = currentProgram.getSymbolTable()
    existing = fn_mgr.getFunctionAt(a)
    if existing is not None:
        if existing.getName() != name:
            existing.setName(name, SourceType.USER_DEFINED)
            print("[FN ] renamed existing function at 0x%08x -> %s" % (addr, name))
        else:
            print("[FN ] function already exists at 0x%08x: %s" % (addr, name))
        return
    cmd = CreateFunctionCmd(name, a, None, SourceType.USER_DEFINED)
    if cmd.applyTo(currentProgram):
        print("[FN ] created %s @ 0x%08x" % (name, addr))
    else:
        print("[warn] createFunction %s @ 0x%08x: %s" % (name, addr, cmd.getStatusMsg()))
        sym_tbl.createLabel(a, name, SourceType.USER_DEFINED)
        print("[FN ] created label (fallback) %s @ 0x%08x" % (name, addr))


def _set_plate(addr, text):
    """Set PLATE_COMMENT. text must be pure ASCII."""
    bad = any(ord(ch) > 127 for ch in text)
    if bad:
        print("[PLATE FAIL] non-ASCII in plate @ 0x%08x -- skipping" % addr)
        return
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(_addr(addr))
    if cu is None:
        print("[PLATE FAIL] no CodeUnit at 0x%08x" % addr)
        return
    cu.setComment(CodeUnit.PLATE_COMMENT, text)
    print("[PLATE ok] 0x%08x (%d chars)" % (addr, len(text)))


def _create_dword_eq(slot_addr, label_name, const_name, value):
    """Force a DWORD at slot_addr, set label, add equate."""
    a = _addr(slot_addr)
    listing = currentProgram.getListing()
    et = currentProgram.getEquateTable()
    try:
        clearListing(a, a.add(3))
    except Exception:
        pass
    listing.createData(a, DWordDataType.dataType)
    createLabel(a, label_name, True, SourceType.USER_DEFINED)
    eq = et.getEquate(const_name)
    if eq is None:
        eq = et.createEquate(const_name, value)
    eq.addReference(a, 0)
    print("[DW+EQ] 0x%08x -> %s (%s=0x%x)" % (slot_addr, label_name, const_name, value))


# ---------------------------------------------------------------------------
# BLOCK A: 0x08062ebe..0x08062efb (0x3e B)
#   1 function (fn @ 0x08062ec0), 2B pad at 0x08062ebe
# ---------------------------------------------------------------------------
BLOCK_A_LO  = 0x08062ebe
BLOCK_A_HI  = 0x08062efb
BLOCK_A_FN  = (0x08062ec0, 'check_opp_active_player_duel_phase_leq3')
BLOCK_A_POOL = [
    # Embedded lit pool between two code segments
    (0x08062edc, 'gp1lp_ref_08062edc',         'gP1LifePoints',        0x0201c4e0),
    (0x08062ee0, 'p1lp_block2_off_08062ee0',    'P1LP_BLOCK2_OFF_1CE8', 0x00001ce8),
    # Tail lit pool after second code segment
    (0x08062ef8, 'field_state_off_08062ef8',    'FIELD_STATE_OFF',      0x00001cf4),
]
BLOCK_A_PLATE = (
    'fn_eligible shared by 3 CIDs: ABSOLUTE_END (0x17fd), THREATENING_ROAR (0x1886), HERO_BARRIER (0x195f). '
    'Reached via card effect handler dispatch table 0x09e4xxxx. '
    '2B alignment pad at 0x08062ebe; fn entry at 0x08062ec0. '
    'Reads gP1LifePoints[P1LP_BLOCK2_OFF_1CE8=0x1ce8] (active player id); '
    'subs r1,r1,r0 -> opp_player_id (1 - player_id). '
    'If active_player != opp_player: return 0 (b 0x08062ef4). '
    'If opp is active player: reads gP1LP[FIELD_STATE_OFF=0x1cf4] (duel_phase); '
    'bhi #3 (phase>3 -> return 0); phase<=3 -> return 1. '
    'bx lr exit @ 0x08062ef4. '
    'Embedded lit pool @ 0x08062edc: gP1LifePoints/P1LP_BLOCK2_OFF_1CE8; '
    'tail lit pool @ 0x08062ef8: FIELD_STATE_OFF.'
)

# ---------------------------------------------------------------------------
# BLOCK B: 0x08062f38..0x08062f5f (0x28 B)
#   1 function (fn @ 0x08062f38), no leading pad
# ---------------------------------------------------------------------------
BLOCK_B_LO  = 0x08062f38
BLOCK_B_HI  = 0x08062f5f
BLOCK_B_FN  = (0x08062f38, 'check_opp_alt_hand_count_nonzero_for_cid_188b')
BLOCK_B_POOL = [
    (0x08062f58, 'gp1lp_ref_08062f58',     'gP1LifePoints',        0x0201c4e0),
    (0x08062f5c, 'player_stride_08062f5c', 'PLAYER_BLOCK_STRIDE',  0x00000868),
]
BLOCK_B_PLATE = (
    'fn_eligible for D.D. Dynamite CID 0x188b (pw=08628798). '
    'Reached via card effect handler dispatch table at ROM 0x09e42754. '
    '0x4048=EOR r0,r1 (ALU op bits[9:6]=0001=EOR, NOT AND): r0 = player_id XOR 1 = opp_player. '
    'Reads [gP1LP+opp_player*PLAYER_BLOCK_STRIDE+0x1c] (opp alt-hand/banished card count). '
    'If count==0: return 0 (beq 0x08062f54); else: movs r0,#1; bx lr -> return 1. '
    'bx lr exit @ 0x08062f54. '
    'Lit pool @ 0x08062f58: gP1LifePoints(0x0201c4e0)/PLAYER_BLOCK_STRIDE(0x868).'
)

# ---------------------------------------------------------------------------
# BLOCK C: 0x080636f8..0x0806372f (0x38 B)
#   1 function (fn @ 0x080636f8), no leading pad
# ---------------------------------------------------------------------------
BLOCK_C_LO  = 0x080636f8
BLOCK_C_HI  = 0x0806372f
BLOCK_C_FN  = (0x080636f8, 'check_zone_non_field_type_or_has_monsters_for_cid_1911')
BLOCK_C_POOL = [
    (0x08063724, 'gp1lp_ref_08063724',     'gP1LifePoints',        0x0201c4e0),
    (0x08063728, 'player_stride_08063728', 'PLAYER_BLOCK_STRIDE',  0x00000868),
]
BLOCK_C_PLATE = (
    'fn_eligible for Cyber Archfiend CID 0x1911 (pw=REUSE). '
    'Reached via card effect handler dispatch table at ROM 0x09e45268. '
    '0x8859=ldrh r1,[r3,#2]: slot[+2] halfword (imm5=1; offset=imm5*2=2 bytes). '
    'ZONE_TYPE_MASK=0xfc0 (movs r0,#0xfc; lsls r0,r0,#4). '
    'FIELD_ZONE_TYPE=0x140 (movs r1,#0xa0; lsls r1,r1,#1 -> 0xa0<<1=0x140). '
    'bne @ 0x08063708: if slot[+2]&0xfc0 != 0x140 (not a field zone): return 1. '
    'If field zone (zone_type==0x140): reads [gP1LP+player*PLAYER_BLOCK_STRIDE+0x0c] (monster_count). '
    'beq @ 0x0806371e: monster_count==0 -> return 0; nonzero -> return 1. '
    'bx lr exit @ 0x0806372e. '
    'Lit pool @ 0x08063724: gP1LifePoints(0x0201c4e0)/PLAYER_BLOCK_STRIDE(0x868).'
)


def main():
    print("=== DisassembleF07Seg9Blocks (DRY=%s) ===" % DRY)

    if DRY:
        print("[dry] Would process 3 blocks, 3 functions:")
        print("  Block A 0x%08x..0x%08x fn@0x%08x (2B pad at 0x08062ebe)" % (
            BLOCK_A_LO, BLOCK_A_HI, BLOCK_A_FN[0]))
        print("  Block B 0x%08x..0x%08x fn@0x%08x" % (BLOCK_B_LO, BLOCK_B_HI, BLOCK_B_FN[0]))
        print("  Block C 0x%08x..0x%08x fn@0x%08x" % (BLOCK_C_LO, BLOCK_C_HI, BLOCK_C_FN[0]))
        print("[dry] 7 literal pool slots (3 blocks): all EQ")
        return

    # =========================================================================
    # Block A: 0x08062ebe..0x08062efb (1 fn, 2B pad at 0x08062ebe)
    # =========================================================================
    print("\n--- Block A: 0x%08x..0x%08x (1 fn; 2B pad) ---" % (BLOCK_A_LO, BLOCK_A_HI))
    _clear_and_set_thumb(BLOCK_A_LO, BLOCK_A_HI)
    # fn entry at 0x08062ec0 (2B pad at 0x08062ebe skipped by disasm flow)
    _disasm_flow(BLOCK_A_FN[0])
    # Literal pool slots: clearListing+createDWord to force DWORD split for export label
    for sp, ln, cn, val in BLOCK_A_POOL:
        _create_dword_eq(sp, ln, cn, val)
    _create_function(BLOCK_A_FN[0], BLOCK_A_FN[1])
    _set_plate(BLOCK_A_FN[0], BLOCK_A_PLATE)

    # =========================================================================
    # Block B: 0x08062f38..0x08062f5f (1 fn, no leading pad)
    # =========================================================================
    print("\n--- Block B: 0x%08x..0x%08x (1 fn) ---" % (BLOCK_B_LO, BLOCK_B_HI))
    _clear_and_set_thumb(BLOCK_B_LO, BLOCK_B_HI)
    _disasm_flow(BLOCK_B_FN[0])
    for sp, ln, cn, val in BLOCK_B_POOL:
        _create_dword_eq(sp, ln, cn, val)
    _create_function(BLOCK_B_FN[0], BLOCK_B_FN[1])
    _set_plate(BLOCK_B_FN[0], BLOCK_B_PLATE)

    # =========================================================================
    # Block C: 0x080636f8..0x0806372f (1 fn, no leading pad)
    # =========================================================================
    print("\n--- Block C: 0x%08x..0x%08x (1 fn) ---" % (BLOCK_C_LO, BLOCK_C_HI))
    _clear_and_set_thumb(BLOCK_C_LO, BLOCK_C_HI)
    _disasm_flow(BLOCK_C_FN[0])
    for sp, ln, cn, val in BLOCK_C_POOL:
        _create_dword_eq(sp, ln, cn, val)
    _create_function(BLOCK_C_FN[0], BLOCK_C_FN[1])
    _set_plate(BLOCK_C_FN[0], BLOCK_C_PLATE)

    print("\n=== DisassembleF07Seg9Blocks DONE ===")
    print("  3 functions created across 3 blocks")
    print("  7 literal pool slots (all EQ)")
    print("  All blocks cleared + THUMB mode set before disassembly")


main()
