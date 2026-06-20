# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF09Seg8RBlocks.py -- p5 file09 Seg-8 REMEDIATION
#
# Eliminates the last partial-disasm residuals in Seg-8 range [0x7629c, 0x7738c):
#
# Block B (simpler): .byte 0x10,0x20 at LAB_08076750 (2 bytes = movs r0,#0x10)
#   - Containing fn: fn_eligible_mustering_dark_scorpions @ 0x080765b0
#   - Reaching branch: beq LAB_08076750 @ 0x0807672e (hw=0xd00f)
#   - Fix: clearListing(0x08076750, 0x08076751) + setTMode + DisassembleCommand
#
# Block A: ROM_INCBIN 0x768dc/0x1e (30 bytes = 15 THUMB instrs)
#   - Containing fn: spell_vanishing_sub_6818 (intra-fn beq-taken path)
#   - Reaching branch: beq LAB_080768dc @ 0x08076866 (hw=0xd039)
#   - BL target: dispatch_equip_zone_sprite_banisher_by_field_count @ 0x080445a4 (asm/04)
#   - Fix: clearListing(0x080768dc, 0x080768f9) + setTMode + DisassembleCommand
#
# Block C: DAT_08076720 -- Ghidra literal-pool split artifact (4 bytes total)
#   - Ghidra split: 2B DAT_ (0x31,0x15) + 2B fake movs r0,r0 at 0x08076722
#   - True value: ROM[0x76720..23] = 0x00001531 = DARK_SCORPION_BURGLARS_CID
#   - Consumer: ldr r0,DAT_08076720 @ 0x08076704; cmp r2,r0 @ 0x08076706
#   - Fix: clearListing(0x08076720, 0x08076723) + createDWord + equate + EOL
#
# Block D: DAT_0807677c -- literal pool 4-byte .byte (4 bytes)
#   - Value: ROM[0x7677c..7f] = 0x00000868 = PLAYER_BLOCK_STRIDE
#   - Consumer: ldr r2,DAT_0807677c @ 0x0807675e; muls r1,r2 @ 0x08076760
#   - Fix: clearListing(0x0807677c, 0x0807677f) + createDWord + equate + EOL
#
# EQ: 2 (all REUSE -- DARK_SCORPION_BURGLARS_CID from card_info.inc, PLAYER_BLOCK_STRIDE from ewram.inc)
# Disasm: 2 (Block A=15 instrs, Block B=1 instr)
# Carve: 0 | REF: 0 | RENAME: 0 | PLATE: 0
#
# NOTE: All EOL text is pure ASCII (no CJK). Ghidra EOL/plate RED LINE = ASCII only.

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

def _disasm_at(lo_int, hi_int, label):
    lo = _addr(lo_int)
    hi = _addr(hi_int)
    cmd = DisassembleCommand(lo, AddressSet(lo, hi), True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm %s @ 0x%08x: %s" % (label, lo_int, cmd.getStatusMsg()))
    else:
        print("[ok ] disasm %s @ 0x%08x" % (label, lo_int))

def _force_dword(addr_int):
    a = _addr(addr_int)
    a_end = _addr(addr_int + 3)
    listing = currentProgram.getListing()
    try:
        clearListing(a, a_end)
        print("[ok ] clearListing for dword @ 0x%08x" % addr_int)
    except Exception as e:
        print("[warn] clearListing dword @ 0x%08x: %s" % (addr_int, e))
    try:
        listing.createData(a, ghidra.program.model.data.DWordDataType.dataType)
        print("[ok ] createDWord @ 0x%08x" % addr_int)
    except Exception as e:
        print("[warn] createDWord @ 0x%08x: %s" % (addr_int, e))

def _apply_eq(slot_int, value, eq_name, slot_label, eol_ascii):
    """Apply equate to a dword slot. Slot label must differ from eq_name."""
    a = _addr(slot_int)
    # Value check via memory read
    mem = currentProgram.getMemory()
    try:
        actual = mem.getInt(a) & 0xFFFFFFFF
    except Exception as ex:
        print("[FAIL] EQ _check 0x%08x: read error %s" % (slot_int, ex))
        return
    if actual != (value & 0xFFFFFFFF):
        print("[FAIL] EQ 0x%08x (%s): got 0x%08x want 0x%08x" % (
              slot_int, eq_name, actual, value & 0xFFFFFFFF))
        return

    if DRY:
        print("[dry] EQ 0x%08x  %s=0x%x  label=%s" % (slot_int, eq_name, value, slot_label))
        return

    eq_tbl = currentProgram.getEquateTable()
    eq = eq_tbl.getEquate(eq_name)
    if eq is None:
        eq = eq_tbl.createEquate(eq_name, value & 0xFFFFFFFFFFFFFFFFL)
    eq.addReference(a, 0)

    sym_tbl = currentProgram.getSymbolTable()
    existing = sym_tbl.getSymbols(a)
    names = [s.getName() for s in existing]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)

    if eol_ascii:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol_ascii)

    print("[EQ ] 0x%08x  %s  -> %s" % (slot_int, eq_name, slot_label))

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF09Seg8RBlocks (DRY=%s) ===" % DRY)
    print("  Seg-8 REMEDIATION: Block B + Block A (disasm) + Block C + Block D (createDWord+EQ)")

    if DRY:
        print("[dry] Block B: clearListing(0x08076750,0x08076751) + setTMode + disasm -> movs r0,#0x10")
        print("[dry] Block A: clearListing(0x080768dc,0x080768f9) + setTMode + disasm -> 15 THUMB instrs")
        print("[dry] Block C: clearListing(0x08076720,0x08076723) + createDWord + EQ DARK_SCORPION_BURGLARS_CID")
        print("[dry] Block D: clearListing(0x0807677c,0x0807677f) + createDWord + EQ PLAYER_BLOCK_STRIDE")
        return

    listing = currentProgram.getListing()

    # -----------------------------------------------------------------------
    # Block B: .byte 0x10,0x20 at LAB_08076750 (2 bytes = movs r0,#0x10)
    # Simpler first: single instruction, no pool.
    # -----------------------------------------------------------------------
    print("\n--- Block B: .byte 0x10,0x20 at LAB_08076750 ---")
    print("    beq target from fn_eligible_mustering_dark_scorpions")
    print("    hw=0x2010 = movs r0,#0x10; fall-through to LAB_08076752 (already decoded)")

    # clearListing: 2 bytes only (0x08076750..0x08076751)
    # LAB_08076752 is already decoded; stop before it.
    _clear_listing(0x08076750, 0x08076751)
    _set_tmode(0x08076750, 0x08076751)
    _disasm_at(0x08076750, 0x08076751, "BlockB_movs_r0_0x10")

    # -----------------------------------------------------------------------
    # Block A: ROM_INCBIN 0x768dc/0x1e (30 bytes = 15 THUMB instructions)
    # beq-taken path of spell_vanishing_sub_6818 inner loop.
    # -----------------------------------------------------------------------
    print("\n--- Block A: ROM_INCBIN 0x768dc/0x1e (30B = 15 THUMB instrs) ---")
    print("    beq target from spell_vanishing_sub_6818 @ 0x08076866 (hw=0xd039)")
    print("    BL target: dispatch_equip_zone_sprite_banisher_by_field_count @ 0x080445a4 (asm/04)")
    print("    No internal literal pool. Fall-through: b LAB_080768fc (already decoded)")

    # clearListing: 0x1e bytes (0x080768dc..0x080768f9)
    # LAB_080768fa is at 0x080768fa (already decoded); stop 1 before it.
    _clear_listing(0x080768dc, 0x080768f9)
    _set_tmode(0x080768dc, 0x080768f9)
    _disasm_at(0x080768dc, 0x080768f9, "BlockA_spell_vanishing_sub_stub")

    # -----------------------------------------------------------------------
    # Block C: DAT_08076720 -- Ghidra split artifact
    # True 4-byte word: 0x00001531 = DARK_SCORPION_BURGLARS_CID (card_info.inc:1476 REUSE)
    # Ghidra created: 2B DAT_(0x31,0x15) + 2B fake movs r0,r0 at 0x08076722.
    # clearListing covers all 4 bytes to absorb both halves.
    # -----------------------------------------------------------------------
    print("\n--- Block C: DAT_08076720 (split artifact) -> DARK_SCORPION_BURGLARS_CID ---")
    print("    ldr r0,DAT_08076720 @ 0x08076704; ROM[0x76720..23]=0x00001531")
    print("    REUSE: DARK_SCORPION_BURGLARS_CID from card_info.inc:1476")
    print("    Pool label: DWORD_08076720 (differs from equate name, no GAS collision)")

    _force_dword(0x08076720)
    _apply_eq(
        0x08076720,
        0x00001531,
        'DARK_SCORPION_BURGLARS_CID',
        'DWORD_08076720',
        'DARK_SCORPION_BURGLARS_CID=0x1531: Dark Scorpion Burglars (pw=40933924); card_info.inc:1476'
    )

    # -----------------------------------------------------------------------
    # Block D: DAT_0807677c -- literal pool 4-byte .byte
    # Value: 0x00000868 = PLAYER_BLOCK_STRIDE (ewram.inc:250 REUSE)
    # -----------------------------------------------------------------------
    print("\n--- Block D: DAT_0807677c (4B .byte) -> PLAYER_BLOCK_STRIDE ---")
    print("    ldr r2,DAT_0807677c @ 0x0807675e; ROM[0x7677c..7f]=0x00000868")
    print("    REUSE: PLAYER_BLOCK_STRIDE from ewram.inc:250")
    print("    Pool label: DWORD_0807677c (differs from equate name, no GAS collision)")

    _force_dword(0x0807677c)
    _apply_eq(
        0x0807677c,
        0x00000868,
        'PLAYER_BLOCK_STRIDE',
        'DWORD_0807677c',
        'PLAYER_BLOCK_STRIDE=0x868: player data block stride (2152B); ewram.inc:250'
    )

    # -----------------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------------
    print("\n--- Instruction count check ---")
    # Block B: expect 1 instruction at 0x08076750
    inst = listing.getInstructionAt(_addr(0x08076750))
    print("  Block B @ 0x08076750: %s" % (("instr: " + str(inst)) if inst else "NO INSTRUCTION"))

    # Block A: expect 15 instructions from 0x080768dc to 0x080768f9
    n_a = 0
    inst = listing.getInstructionAt(_addr(0x080768dc))
    end_a = _addr(0x080768f9)
    while inst is not None and inst.getAddress().compareTo(end_a) <= 0:
        n_a += 1
        inst = listing.getInstructionAfter(inst.getAddress())
    print("  Block A @ 0x080768dc: %d instructions (expect 15)" % n_a)

    # Block C/D: check createDWord succeeded
    d_c = listing.getDataAt(_addr(0x08076720))
    d_d = listing.getDataAt(_addr(0x0807677c))
    print("  Block C @ 0x08076720: %s (expect DWord, length=4)" % (
          ("len=%d" % d_c.getLength()) if d_c else "NO DATA"))
    print("  Block D @ 0x0807677c: %s (expect DWord, length=4)" % (
          ("len=%d" % d_d.getLength()) if d_d else "NO DATA"))

    print("\n=== RefineF09Seg8RBlocks DONE ===")
    print("  Disasm: Block A=15 instrs @ 0x080768dc, Block B=1 instr @ 0x08076750")
    print("  EQ: DARK_SCORPION_BURGLARS_CID @ DWORD_08076720 + PLAYER_BLOCK_STRIDE @ DWORD_0807677c")
    print("  Carve=0 | REF=0 | RENAME=0 | PLATE=0 | NO new constants")


main()
