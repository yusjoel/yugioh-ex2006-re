# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixF07Seg3LiteralPools.py -- Fix literal pool DWORDs in disassembled blocks (F07 Seg-3)
#
# After clearListing+disasm, literal pool words within THUMB fn bodies are exported
# as raw .byte sequences, causing "invalid offset / value too big" GAS errors.
# Fix: createDWord at each 4-byte literal pool address to restore proper DWORD data.
#
# Literal pool addresses (verified from asm/07_equip_effect_chain.s after export):
#
#   Block1 fn1 (check_equip_type480_cross_player_for_cid_13f9):
#     0x0805e770 = gEquipChainSlotRefs (0x0201bb90)
#     Note: preceded by 2B pad at 0x0805e76e (handled by clearListing, no createDWord needed)
#
#   Block2 fn1 (check_slot_count_exceeds_2_for_cid_144e):
#     0x0805ed68 = gP1LifePoints (0x0201c4e0)
#     0x0805ed6c = PLAYER_BLOCK_STRIDE (0x00000868)
#     Note: preceded by 2B pad at 0x0805ed66
#
#   Block3 fn1 (check_zone_field6_hw_zero_for_cid_1450):
#     0x0805edb4 = PLAYER_BLOCK_STRIDE (0x00000868)
#     0x0805edb8 = gDuelFieldSlots (0x0201c510)
#
#   Block3 fn2 (check_zone_field6_hw_nonzero_for_cid_1451):
#     0x0805ede4 = PLAYER_BLOCK_STRIDE (0x00000868)
#     0x0805ede8 = gDuelFieldSlots (0x0201c510)
#
#   Block3 fn3 (check_opponent_lp_above_3000_for_cid_1460):
#     0x0805ee14 = gP1LifePoints (0x0201c4e0)
#     0x0805ee18 = PLAYER_BLOCK_STRIDE (0x00000868)
#     0x0805ee1c = 0x00000BB8 (3000 LP threshold)
#     Note: preceded by 2B pad at 0x0805ee12
#
#   Block4 fn2 (check_neo_daedalus_no_banisher_for_cid_146f):
#     0x0805eed8 = BANISHER_OF_THE_LIGHT_CID (0x00001332)
#     Note: preceded by 2B pad at 0x0805eed6
#
#   Block4 fn3 (check_field_state24_neo_daedalus_for_cid_1472):
#     0x0805eefc = gP1LifePoints (0x0201c4e0)
#     0x0805ef00 = FIELD_STATE_OFF (0x00001cf4)
#
#   Block4 fn4 (check_chain_match_opponent_for_cid_1475):
#     0x0805ef24 = gP1LifePoints (0x0201c4e0)
#     0x0805ef28 = FIELD_STATE_OFF (0x00001cf4)
#
#   Block4 fn5 (check_field_0c_nonzero_no_banisher_for_cid_147f):
#     0x0805ef74 = gP1LifePoints (0x0201c4e0)
#     0x0805ef78 = PLAYER_BLOCK_STRIDE (0x00000868)
#     0x0805ef7c = BANISHER_OF_THE_LIGHT_CID (0x00001332)
#     Note: preceded by 2B pad at 0x0805ef72
#
# Backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260614-130344-pre-f07seg3

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

DWORD_SLOTS = [
    # Block1 fn1 literal pool
    0x0805e770,  # gEquipChainSlotRefs (0x0201bb90)

    # Block2 fn1 literal pool
    0x0805ed68,  # gP1LifePoints (0x0201c4e0)
    0x0805ed6c,  # PLAYER_BLOCK_STRIDE (0x00000868)

    # Block3 fn1 literal pool
    0x0805edb4,  # PLAYER_BLOCK_STRIDE (0x00000868)
    0x0805edb8,  # gDuelFieldSlots (0x0201c510)

    # Block3 fn2 literal pool
    0x0805ede4,  # PLAYER_BLOCK_STRIDE (0x00000868)
    0x0805ede8,  # gDuelFieldSlots (0x0201c510)

    # Block3 fn3 literal pool
    0x0805ee14,  # gP1LifePoints (0x0201c4e0)
    0x0805ee18,  # PLAYER_BLOCK_STRIDE (0x00000868)
    0x0805ee1c,  # 0x00000BB8 (3000 LP threshold, raw literal)

    # Block4 fn2 literal pool
    0x0805eed8,  # BANISHER_OF_THE_LIGHT_CID (0x00001332)

    # Block4 fn3 literal pool
    0x0805eefc,  # gP1LifePoints (0x0201c4e0)
    0x0805ef00,  # FIELD_STATE_OFF (0x00001cf4)

    # Block4 fn4 literal pool
    0x0805ef24,  # gP1LifePoints (0x0201c4e0)
    0x0805ef28,  # FIELD_STATE_OFF (0x00001cf4)

    # Block4 fn5 literal pool
    0x0805ef74,  # gP1LifePoints (0x0201c4e0)
    0x0805ef78,  # PLAYER_BLOCK_STRIDE (0x00000868)
    0x0805ef7c,  # BANISHER_OF_THE_LIGHT_CID (0x00001332)
]


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def main():
    print("=== FixF07Seg3LiteralPools (DRY=%s) ===" % DRY)
    listing = currentProgram.getListing()
    n_ok = n_fail = 0

    for slot_int in DWORD_SLOTS:
        a = _addr(slot_int)
        if DRY:
            print("[dry] createDWord @ 0x%08x" % slot_int)
            n_ok += 1
            continue
        try:
            clearListing(a, _addr(slot_int + 3))
            listing.createData(a, ghidra.program.model.data.DWordDataType.dataType)
            d = getDataAt(a)
            val = None
            if d is not None and d.getLength() == 4:
                try:
                    dv = d.getValue()
                    val = (int(dv.getValue()) & 0xffffffff) if hasattr(dv, 'getValue') else (int(dv) & 0xffffffff)
                except Exception:
                    pass
            if val is not None:
                print("[ok ] createDWord @ 0x%08x = 0x%08x" % (slot_int, val))
            else:
                print("[ok ] createDWord @ 0x%08x (value unreadable)" % slot_int)
            n_ok += 1
        except Exception as e:
            print("[FAIL] createDWord @ 0x%08x: %s" % (slot_int, e))
            n_fail += 1

    print("[done] ok=%d fail=%d (DRY=%s)" % (n_ok, n_fail, DRY))
    print("  Total DWORD slots: %d (expected 18)" % len(DWORD_SLOTS))


main()
