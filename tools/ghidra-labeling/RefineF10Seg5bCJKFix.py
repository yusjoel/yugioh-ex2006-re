# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF10Seg5bCJKFix.py -- fix remaining CJK plate @ tick_equip_zone15_bitmap_with_sprite_output
# tick_equip_zone15_bitmap_with_sprite_output @ 0x0807ec10 has a CJK plate.
# Replace with ASCII-only content preserving semantic.
# All plate text is pure ASCII (no CJK). Ghidra Jython mojibake prevention.

from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


# New ASCII plate for tick_equip_zone15_bitmap_with_sprite_output (0x0807ec10)
PLATE_NEW = (
    '@ 4-step frame state machine for zone15 equip target bitmap update and sprite enumeration.\n'
    '@ Routes on [IWRAM_BASE+0x4a0]: 0x80 -> check_effect_slot_matches_zone_entry(0,0) +\n'
    '@ read_effect_slot_side_and_type(side/slot_type); invoke_effect_node_with_active_flag_3arg;\n'
    '@ update_equip_target_bitmap_zone15; on success read gDuelFieldSlots[player*0x868+slot_type*20]\n'
    '@ card_id -> write to [slot+0xc]; return 0x7f.\n'
    '@ 0x7f -> check_spell_zone_slot_placeable; success -> increment_lp_bar_display_counter return 0x7e;\n'
    '@ fail -> return 0x0.\n'
    '@ 0x7e -> find_deck_slot_by_card_pair_match(opponent, [slot+0xc]); found ->\n'
    '@ enqueue_equip_zone_sprite_by_slot_ptr return 0x7e (loop); not found -> return 0x7d.\n'
    '@ 0x7d -> decrement_lp_bar_display_counter; return 0x0.\n'
    '@ \n'
    '@ Constants:\n'
    '@ - IWRAM_BASE = 0x0201b290\n'
    '@ - STATE_OFFSET = 0x94*8 = 0x4a0\n'
    '@ - PLAYER_STRIDE = 0x868\n'
    '@ - gDuelFieldSlots = 0x0201c510\n'
    '@ - ZONE_TABLE_2 = 0x0201c8f8 (enqueue_equip_zone_sprite_by_slot_ptr base)'
)


def main():
    print("=== RefineF10Seg5bCJKFix (DRY=%s) ===" % DRY)
    listing = currentProgram.getListing()

    func_int = 0x0807ec10
    cu = listing.getCodeUnitAt(_addr(func_int))
    if cu is None:
        print("[FAIL] no CodeUnit @ 0x%08x" % func_int); return
    plate = cu.getComment(CodeUnit.PLATE_COMMENT)
    if plate is None:
        print("[SKIP] no plate @ 0x%08x" % func_int); return
    # Check if CJK present
    has_cjk = any(ord(c) > 0x7f for c in plate)
    print("[info] plate has CJK: %s (len=%d)" % (has_cjk, len(plate)))
    if not has_cjk:
        print("[SKIP] no CJK in plate @ 0x%08x -- already ASCII" % func_int); return
    if DRY:
        print("[dry] would replace CJK plate @ 0x%08x with %d-char ASCII text" % (func_int, len(PLATE_NEW)))
        return
    cu.setComment(CodeUnit.PLATE_COMMENT, PLATE_NEW)
    # Verify after set
    plate2 = cu.getComment(CodeUnit.PLATE_COMMENT)
    has_cjk2 = any(ord(c) > 0x7f for c in (plate2 or ''))
    print("[ok] plate replaced @ 0x%08x (new len=%d, CJK=%s)" % (func_int, len(plate2 or ''), has_cjk2))
    print("[done]")


main()
