# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixF05Seg3LiteralPoolLabels.py -- Fix missing literal pool labels in disasm blocks
#
# After DisassembleF05Seg3Blocks.py, the literal pool data for the 3 disasm blocks
# was exported as raw .byte blobs with only the first label of each group defined.
# The ldr instructions reference sub-labels (e.g. DAT_0804ae64, DAT_0804ae68)
# that are embedded inside the .byte blocks but not separately labeled.
#
# This script creates USER_DEFINED labels at those sub-locations so the GAS exporter
# emits separate labels within the .byte blob, allowing the assembler to resolve
# the ldr references.
#
# Addresses derived from the proposal EQ_SLOTS for disasm blocks.
# We apply both the equate (where data exists) and a plain label (for sub-labels).

from ghidra.program.model.symbol import SourceType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

# ---------------------------------------------------------------------------
# Sub-labels to create: (addr_int, label)
# These are literal pool addresses that are referenced by ldr but not labeled.
# ---------------------------------------------------------------------------
SUB_LABELS = [
    # Block A -- check_card_is_toon_type literal pool sub-labels
    (0x0804ae60, 'toon_type_beyd_cid'),       # BLUE_EYES_TOON_DRAGON_CID (first, may already exist)
    (0x0804ae64, 'toon_type_alligator_cid'),   # TOON_ALLIGATOR_CID (sub-label, referenced by ldr)
    (0x0804ae68, 'toon_type_summoned_skull_cid'), # TOON_SUMMONED_SKULL_CID
    (0x0804ae80, 'toon_type_dmg_cid'),         # TOON_DARK_MAGICIAN_GIRL_CID (may already exist as DAT_0804ae80)
    (0x0804ae84, 'toon_type_world_cid'),        # TOON_WORLD_CARD_ID
    (0x0804ae98, 'toon_type_goblin_af_cid'),    # TOON_GOBLIN_AF_CID (may already exist)
    # Block B -- check_card_is_guardian_type literal pool sub-labels
    (0x0804afa8, 'guardian_type_sphinx_cid'),   # GUARDIAN_SPHINX_CID (may already exist as DAT_0804afa8)
    (0x0804afac, 'guardian_type_throne_room_cid'), # GUARDIAN_OF_THRONE_ROOM_CID
    (0x0804afb0, 'guardian_type_metal_cid'),    # METAL_GUARDIAN_CID
    (0x0804afb4, 'guardian_type_gate_cid'),     # GATE_GUARDIAN_CID
    (0x0804afc8, 'guardian_type_skull_cid'),    # SKULL_GUARDIAN_CID (may already exist as DAT_0804afc8)
    (0x0804afcc, 'check_card_is_guardian_type_cid_1452'),  # unassigned 0x1452 (already done by RN)
    (0x0804afe8, 'guardian_type_angel_joan_cid'),  # GUARDIAN_ANGEL_JOAN_CID (may already exist as DAT_0804afe8)
    (0x0804affc, 'guardian_type_lost_cid'),     # LOST_GUARDIAN_CID (may already exist as DAT_0804affc)
    # Block B -- check_card_is_dark_scorpion_type literal pool sub-labels
    (0x0804b020, 'dark_scorpion_meanae_cid'),   # DARK_SCORPION_MEANAE_CID (may already exist as DAT_0804b020)
    (0x0804b02c, 'dark_scorpion_chick_cid'),    # DARK_SCORPION_CHICK_CID (may already exist as DAT_0804b02c)
    (0x0804b040, 'dark_scorpion_mustering_cid'), # MUSTERING_DARK_SCORPIONS_CID (may already exist as DAT_0804b040)
    # Block C -- check_card_is_batteryman_type literal pool sub-labels
    (0x0804b264, 'batteryman_type_aa_cid'),     # BATTERYMAN_AA_CID (may already exist as DAT_0804b264)
]

# ---------------------------------------------------------------------------
# EQ references to apply where data exists (equate + label)
# These are the same slots, equated to the correct constant names.
# ---------------------------------------------------------------------------
EQ_REFS = [
    # (addr, value, const_name)
    (0x0804ae60, 0x000012a5, 'BLUE_EYES_TOON_DRAGON_CID'),
    (0x0804ae64, 0x00001123, 'TOON_ALLIGATOR_CID'),
    (0x0804ae68, 0x0000127f, 'TOON_SUMMONED_SKULL_CID'),
    (0x0804ae80, 0x0000154a, 'TOON_DARK_MAGICIAN_GIRL_CID'),
    (0x0804ae84, 0x000012be, 'TOON_WORLD_CARD_ID'),
    (0x0804ae98, 0x00001566, 'TOON_GOBLIN_AF_CID'),
    (0x0804afa8, 0x0000152e, 'GUARDIAN_SPHINX_CID'),
    (0x0804afac, 0x000011a7, 'GUARDIAN_OF_THRONE_ROOM_CID'),
    (0x0804afb0, 0x00000ffe, 'METAL_GUARDIAN_CID'),
    (0x0804afb4, 0x0000111c, 'GATE_GUARDIAN_CID'),
    (0x0804afc8, 0x00001266, 'SKULL_GUARDIAN_CID'),
    (0x0804afe8, 0x0000170b, 'GUARDIAN_ANGEL_JOAN_CID'),
    (0x0804affc, 0x000018b0, 'LOST_GUARDIAN_CID'),
    (0x0804b020, 0x00001686, 'DARK_SCORPION_MEANAE_CID'),
    (0x0804b02c, 0x00001656, 'DARK_SCORPION_CHICK_CID'),
    (0x0804b040, 0x0000169e, 'MUSTERING_DARK_SCORPIONS_CID'),
    (0x0804b264, 0x000018c3, 'BATTERYMAN_AA_CID'),
]


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def main():
    print("=== FixF05Seg3LiteralPoolLabels (DRY=%s) ===" % DRY)
    et      = currentProgram.getEquateTable()
    listing = currentProgram.getListing()
    nLBL = nEQ = 0

    # 1. Create labels at sub-label addresses
    for addr_int, label in SUB_LABELS:
        a = _addr(addr_int)
        if DRY:
            print("[LBL dry] 0x%08x -> %s" % (addr_int, label)); nLBL += 1; continue
        try:
            currentProgram.getSymbolTable().createLabel(a, label, SourceType.USER_DEFINED)
            print("[LBL ok ] 0x%08x -> %s" % (addr_int, label)); nLBL += 1
        except Exception as e:
            print("[LBL warn] 0x%08x %s: %s" % (addr_int, label, e))

    # 2. Apply equate references where possible
    for addr_int, value, cname in EQ_REFS:
        a = _addr(addr_int)
        if DRY:
            print("[EQ dry] 0x%08x equate %s=0x%x" % (addr_int, cname, value)); nEQ += 1; continue
        # Try to get or create equate
        try:
            eq = et.getEquate(cname)
            if eq is None:
                eq = et.createEquate(cname, value)
            eq.addReference(a, 0)
            print("[EQ ok ] 0x%08x equate %s" % (addr_int, cname)); nEQ += 1
        except Exception as e:
            print("[EQ warn] 0x%08x %s: %s" % (addr_int, cname, e))

    print("[done] LBL=%d EQ=%d (DRY=%s)" % (nLBL, nEQ, DRY))


main()
