# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixF08Seg10AndF09Seg1LiteralPools.py
#   Force-create DWORD data items at all PC-relative ldr targets inside
#   the disasm blocks of asm/08 Seg-10 (0x0806de00..0x0806e63f) and
#   asm/09 Seg-1 Block2/Block4/Block6 (dispatch sub-stubs).
#
#   Without this, Ghidra exports these as raw .byte sequences with no label,
#   and the GNU assembler cannot resolve the PC-relative references.
#
#   asm/08 Seg-10 pools: 22 addresses (cid_13ed + de_fusion state stubs)
#   asm/09 Block2 pools: 10 addresses (0x0806f09c..0x0806f1c4)
#   asm/09 Block4 pools:  8 addresses (0x0806fa40..0x0806fb48)
#   asm/09 Block6 pools:  3 addresses (0x0806fed4..0x0806ff4c)
#
# NOTE: This script was needed because DisassembleCommand(sa, {sa}, True)
# only disassembles from the entry point; stub bodies with interior ldr
# targets remain ROM_INCBIN in the export unless we force-split them here.

from ghidra.program.model.data import DWordDataType

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

def _addr(val):
    return toAddr(val)

# -------------------------------------------------------------------------
# asm/08 Seg-10: cid_13ed + de_fusion state stubs literal pools
# Range: 0x0806de00..0x0806e63f
# -------------------------------------------------------------------------
ASM08_POOLS = [
    0x0806de34,  # gP1LifePoints = 0x0201c4e0
    0x0806de38,  # LP_BANISHER_CTX_OFF = 0x1d70
    0x0806de3c,  # PLAYER_BLOCK_STRIDE = 0x868
    0x0806defc,  # gP1LifePoints = 0x0201c4e0
    0x0806df00,  # LP_CARD_TRACK_BASE_OFF = 0x1da8
    0x0806df04,  # gDuelPhaseFlags = 0x0201b290
    0x0806df08,  # EQUIP_PHASE_FRAME_OFF = 0x4a4
    0x0806df0c,  # PLAYER_BLOCK_STRIDE = 0x868
    0x0806df10,  # gP1FieldArrayCBase = 0x0201c600
    0x0806dfe8,  # EQUIP_PHASE_FRAME_OFF = 0x4a4
    0x0806e508,  # PLAYER_BLOCK_STRIDE = 0x868
    0x0806e50c,  # gDuelFieldSlots = 0x0201c510
    0x0806e510,  # gEquipLpZoneEntryBase = 0x0201e500
    0x0806e514,  # 0x159d
    0x0806e598,  # gEquipLpZoneEntryBase = 0x0201e500
    0x0806e59c,  # gDuelCardCtxBase = 0x0201e2a0
    0x0806e5a0,  # gP1LifePoints = 0x0201c4e0
    0x0806e5cc,  # gP1LifePoints = 0x0201c4e0
    0x0806e5d0,  # EQUIP_PHASE_FRAME_OFF = 0x4a4
    0x0806e608,  # gDuelPhaseFlags = 0x0201b290
    0x0806e60c,  # EQUIP_PHASE_FRAME_OFF = 0x4a4
    0x0806e610,  # gEquipLpZoneEntryBase = 0x0201e500
]

# -------------------------------------------------------------------------
# asm/09 Seg-1 Block2 dispatch sub-stubs literal pools
# Range: 0x0806f054..0x0806f1c7
# -------------------------------------------------------------------------
ASM09_BLOCK2_POOLS = [
    0x0806f09c,  # 0xe08c
    0x0806f0a0,  # EQUIP_PHASE_FRAME_OFF = 0x4a4
    0x0806f0a4,  # gP1LifePoints = 0x0201c4e0
    0x0806f0a8,  # LP_CARD_TRACK_BASE_OFF = 0x1da8
    0x0806f0c0,  # 0xe07a
    0x0806f0c4,  # gP1LifePoints = 0x0201c4e0
    0x0806f0c8,  # LP_CARD_TRACK_BASE_OFF = 0x1da8
    0x0806f180,  # 0xe01a
    0x0806f184,  # EQUIP_PHASE_FRAME_OFF = 0x4a4
    0x0806f1c4,  # EQUIP_PHASE_FRAME_OFF = 0x4a4
]

# -------------------------------------------------------------------------
# asm/09 Seg-1 Block4 dispatch sub-stubs literal pools
# Range: 0x0806fa08..0x0806fb87
# -------------------------------------------------------------------------
ASM09_BLOCK4_POOLS = [
    0x0806fa40,  # 0xe09a
    0x0806fa44,  # gDuelPhaseFlags = 0x0201b290
    0x0806fa48,  # EQUIP_PHASE_FRAME_OFF = 0x4a4
    0x0806fb04,  # 0x805e
    0x0806fb08,  # 0x1379
    0x0806fb0c,  # gDuelPhaseFlags = 0x0201b290
    0x0806fb10,  # EQUIP_PHASE_FRAME_OFF = 0x4a4
    0x0806fb48,  # 0x805e
]

# -------------------------------------------------------------------------
# asm/09 Seg-1 Block6 dispatch sub-stubs literal pools
# Range: 0x0806fe88..0x0806ff4f
# -------------------------------------------------------------------------
ASM09_BLOCK6_POOLS = [
    0x0806fed4,  # 0xe038
    0x0806fed8,  # 0x11d
    0x0806ff4c,  # 0x4708
]

ALL_POOLS = ASM08_POOLS + ASM09_BLOCK2_POOLS + ASM09_BLOCK4_POOLS + ASM09_BLOCK6_POOLS

print("=== FixF08Seg10AndF09Seg1LiteralPools.py DRY=%s ===" % DRY)
print("Processing %d literal pool addresses..." % len(ALL_POOLS))
print("  asm/08 Seg-10: %d" % len(ASM08_POOLS))
print("  asm/09 Block2: %d" % len(ASM09_BLOCK2_POOLS))
print("  asm/09 Block4: %d" % len(ASM09_BLOCK4_POOLS))
print("  asm/09 Block6: %d" % len(ASM09_BLOCK6_POOLS))

applied = 0
skipped = 0
for addr_val in ALL_POOLS:
    addr = _addr(addr_val)
    if DRY:
        print("DRY: createDWord at 0x%08x" % addr_val)
        applied += 1
        continue
    try:
        # Clear listing at just this 4-byte slot to remove conflicting code unit
        clearListing(addr, toAddr(addr_val + 3))
        # Force a DWORD data type so the exporter emits a labeled .word
        dt = DWordDataType()
        currentProgram.getListing().createData(addr, dt)
        applied += 1
        print("[OK] createDWord 0x%08x" % addr_val)
    except Exception as e:
        print("[WARN] 0x%08x createDWord failed: %s" % (addr_val, str(e)))
        skipped += 1

print("=== DONE: applied=%d skipped=%d ===" % (applied, skipped))
