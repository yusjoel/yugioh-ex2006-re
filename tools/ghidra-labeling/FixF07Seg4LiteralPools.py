# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixF07Seg4LiteralPools.py -- Fix literal pool DWORDs in disassembled blocks (F07 Seg-4)
#
# After clearListing+disasm, literal pool words within THUMB fn bodies are exported
# as raw .byte sequences, causing "invalid offset / value too big" GAS errors.
# Fix: createDWord at each 4-byte literal pool address to restore proper DWORD data.
#
# Literal pool addresses (from proposal disasm plan):
#
#   Block 1: check_field_state_leq3_for_cid_14d4 @ 0x0805f480
#     0x0805f494 = gP1LifePoints (0x0201c4e0)
#     0x0805f498 = FIELD_STATE_OFF (0x00001cf4)
#     NOTE: 0x5f492 is bx lr instruction (0x4770), not a data slot; skip it.
#
#   Block 2: check_zone640_opponent_turn_bit10_for_cid_151c @ 0x0805f8b4
#     0x0805f8e8 = gP1LifePoints (0x0201c4e0)
#     0x0805f8ec = P1LP_BLOCK2_OFF_1CE8 (0x00001ce8)
#
#   Block 3: check_opp_turn_lp_leq1000_return2_for_cid_151e @ 0x0805f930
#     0x0805f958 = gP1LifePoints (0x0201c4e0)
#     0x0805f95c = PLAYER_BLOCK_STRIDE (0x00000868)
#     0x0805f960 = P1LP_BLOCK2_OFF_1CE8 (0x00001ce8)
#
#   Block 4: check_player_lp_state_off10_nonzero @ 0x0805fa5c
#     0x0805fa7c = gP1LifePoints (0x0201c4e0)
#     0x0805fa80 = PLAYER_BLOCK_STRIDE (0x00000868)
#
#   Block 5: check_player_zone_count_above3_for_cid_1546 @ 0x0805fc10
#     0x0805fc34 = gP1LifePoints (0x0201c4e0)
#     0x0805fc38 = PLAYER_BLOCK_STRIDE (0x00000868)
#
# Backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260614-141354-pre-f07seg4

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

DWORD_SLOTS = [
    # Block 1 literal pool (check_field_state_leq3_for_cid_14d4)
    0x0805f494,  # gP1LifePoints (0x0201c4e0)
    0x0805f498,  # FIELD_STATE_OFF (0x00001cf4)

    # Block 2 literal pool (check_zone640_opponent_turn_bit10_for_cid_151c)
    0x0805f8e8,  # gP1LifePoints (0x0201c4e0)
    0x0805f8ec,  # P1LP_BLOCK2_OFF_1CE8 (0x00001ce8)

    # Block 3 literal pool (check_opp_turn_lp_leq1000_return2_for_cid_151e)
    0x0805f958,  # gP1LifePoints (0x0201c4e0)
    0x0805f95c,  # PLAYER_BLOCK_STRIDE (0x00000868)
    0x0805f960,  # P1LP_BLOCK2_OFF_1CE8 (0x00001ce8)

    # Block 4 literal pool (check_player_lp_state_off10_nonzero)
    0x0805fa7c,  # gP1LifePoints (0x0201c4e0)
    0x0805fa80,  # PLAYER_BLOCK_STRIDE (0x00000868)

    # Block 5 literal pool (check_player_zone_count_above3_for_cid_1546)
    0x0805fc34,  # gP1LifePoints (0x0201c4e0)
    0x0805fc38,  # PLAYER_BLOCK_STRIDE (0x00000868)
]


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def main():
    print("=== FixF07Seg4LiteralPools (DRY=%s) ===" % DRY)
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
    print("  Total DWORD slots: %d (expected 11)" % len(DWORD_SLOTS))


main()
