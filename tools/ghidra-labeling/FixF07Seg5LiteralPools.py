# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixF07Seg5LiteralPools.py -- Fix literal pool DWORDs in disassembled blocks (F07 Seg-5)
#
# After clearListing+disasm, literal pool words within THUMB fn bodies are exported
# as raw .byte sequences, causing "invalid offset / value too big" GAS errors.
# Fix: createDWord at each 4-byte literal pool address to restore proper DWORD data.
#
# Literal pool addresses (from proposal disasm plan):
#
#   Block 1: check_equip_slot_eligible_by_lp_slot_for_cid_159a @ 0x0806008c
#     0x080600a8 = gP1LifePoints (0x0201c4e0)
#     0x080600ac = PLAYER_BLOCK_STRIDE (0x00000868)
#
#   Block 2: check_equip_slot_eligible_by_type_and_player_for_cid_15dc @ 0x08060388
#     No named DAT_ pool slots -- pool data within fn body (2 pool slots, no external named labels)
#     Pool slots auto-resolved by disasm; createDWord if needed for each 4B word in fn:
#     (Check asm post-disasm export; if .byte sequences appear, add here)
#
#   Block 3-F1: check_equip_slot_eligible_by_active_player_phase_for_cid_15f0 @ 0x08060588
#     0x080605a8 = gP1LifePoints (0x0201c4e0)
#     0x080605ac = P1LP_BLOCK2_OFF_1CE8 (0x00001ce8)
#     0x080605b0 = FIELD_STATE_OFF (0x00001cf4)
#
#   Block 3-F2: check_equip_slot_eligible_by_active_player_phase_for_cid_15f2 @ 0x080605b8
#     0x080605d0 = gP1LifePoints (0x0201c4e0)
#     0x080605d4 = P1LP_BLOCK2_OFF_1CE8 (0x00001ce8)
#     0x080605ec = FIELD_STATE_OFF (0x00001cf4)
#
#   Block 3-F3: check_equip_slot_eligible_by_monster_zone_type_for_cid_15f3 @ 0x080605f0
#     No dedicated pool slots in the [0x08060588..0x08060603] range for F3 prologue
#     (F3 body extends into named asm at 0x08060604; its pools are in named asm area)
#
#   Block 4: check_equip_slot_eligible_active_player_with_chain_and_node_count @ 0x08060800
#     0x08060834 = gP1LifePoints (0x0201c4e0)   [in named asm area, currently .byte fragment]
#     0x08060838 = P1LP_BLOCK2_OFF_1CE8 (0x00001ce8)  [already named DAT_08060838 in EQ_SLOTS]
#
# Backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260614-154713-pre-f07seg5

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

# (slot_addr, expected_value) -- for verification
DWORD_SLOTS = [
    # Block 1 literal pool (check_equip_slot_eligible_by_lp_slot_for_cid_159a)
    (0x080600a8, 0x0201c4e0),  # gP1LifePoints
    (0x080600ac, 0x00000868),  # PLAYER_BLOCK_STRIDE

    # Block 3-F1 literal pool (check_equip_slot_eligible_by_active_player_phase_for_cid_15f0)
    (0x080605a8, 0x0201c4e0),  # gP1LifePoints
    (0x080605ac, 0x00001ce8),  # P1LP_BLOCK2_OFF_1CE8
    (0x080605b0, 0x00001cf4),  # FIELD_STATE_OFF

    # Block 3-F2 literal pool (check_equip_slot_eligible_by_active_player_phase_for_cid_15f2)
    (0x080605d0, 0x0201c4e0),  # gP1LifePoints
    (0x080605d4, 0x00001ce8),  # P1LP_BLOCK2_OFF_1CE8
    (0x080605ec, 0x00001cf4),  # FIELD_STATE_OFF

    # Block 4 literal pool slot in named asm area
    (0x08060834, 0x0201c4e0),  # gP1LifePoints (in .byte 0xe0,0xc4,0x01,0x02 fragment)
    # 0x08060838 is DAT_08060838 (P1LP_BLOCK2_OFF_1CE8) -- handled by EQ_SLOTS in RefineF07Seg5Slots
]


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def main():
    print("=== FixF07Seg5LiteralPools (DRY=%s) ===" % DRY)
    listing = currentProgram.getListing()
    n_ok = n_fail = 0

    for slot_int, expected in DWORD_SLOTS:
        a = _addr(slot_int)
        d = getDataAt(a)
        val = None
        if d is not None and d.getLength() == 4:
            try:
                dv = d.getValue()
                val = (int(dv.getValue()) & 0xffffffff) if hasattr(dv, 'getValue') else (int(dv) & 0xffffffff)
            except Exception:
                pass
        if val == (expected & 0xffffffff):
            print("[skip] 0x%08x already DWORD=0x%08x" % (slot_int, expected))
            n_ok += 1; continue
        if DRY:
            print("[dry] createDWord @ 0x%08x (expected=0x%08x, current=%s)" % (
                slot_int, expected, ("0x%08x" % val) if val is not None else "unknown"))
            n_ok += 1; continue
        try:
            clearListing(a, _addr(slot_int + 3))
            createDWord(a)
            d2 = getDataAt(a)
            if d2 is not None and d2.getLength() == 4:
                try:
                    dv2 = d2.getValue()
                    got = (int(dv2.getValue()) & 0xffffffff) if hasattr(dv2, 'getValue') else (int(dv2) & 0xffffffff)
                except Exception:
                    got = None
                if got is not None and got != (expected & 0xffffffff):
                    print("[FAIL] 0x%08x: createDWord ok but value=0x%x != expected=0x%x" % (
                        slot_int, got, expected))
                    n_fail += 1; continue
            print("[ok ] createDWord @ 0x%08x (value=0x%08x)" % (slot_int, expected))
            n_ok += 1
        except Exception as e:
            print("[FAIL] createDWord @ 0x%08x: %s" % (slot_int, e))
            n_fail += 1

    print("[done] ok=%d fail=%d (expected %d ok, 0 fail)" % (n_ok, n_fail, len(DWORD_SLOTS)))


main()
