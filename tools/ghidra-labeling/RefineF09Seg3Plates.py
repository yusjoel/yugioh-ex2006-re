# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF09Seg3Plates.py -- F09 Seg-3 plate fixes (PLATE-1 CJK rewrite + PLATE-2 stale FUN_)
#
# PLATE-1: dispatch_equip_lp_bar_or_bitmap_by_zone_type @ 0x0807158c
#   Current plate (line 6141) contains CJK characters (Jython UTF-8 mojibake).
#   Replace with pure ASCII description.
#
# PLATE-2: tick_zone_sprite_pipeline_with_chain_counter @ 0x08071604
#   Current plate (line 6209) contains stale FUN_ references:
#     FUN_08090714 -> count_effect_node_zone_activations
#     FUN_08096a4c -> set_equip_activation_state_by_mode__08096a4c
#
# IMPORTANT: setPlateComment WARN/not-found treated as FAIL.
# NOTE: All text is pure ASCII (no CJK). Jython encodes CJK as double-UTF-8 mojibake.
# backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260618_220254-pre-F09Seg3

from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

# ---------------------------------------------------------------------------
# PLATE_FIX: (func_addr_int, plate_ascii_text)
# All text must be pure ASCII.
# ---------------------------------------------------------------------------
PLATE_FIX = [

    # PLATE-1: dispatch_equip_lp_bar_or_bitmap_by_zone_type (0x0807158c)
    # Fix: CJK mojibake -> pure ASCII
    (0x0807158c,
     'dispatch_equip_lp_bar_or_bitmap_by_zone_type: Routes equip LP bar / bitmap dispatch by zone_type_code.'
     ' Reads [r0+0xc] halfword as zone_type_code.'
     ' type==1 -> submit_equip_lp_indicators_with_bar;'
     ' type==2 -> invoke_equip_slot_eligibility_via_effect_node_bitmap;'
     ' other type returns 0. Passthrough return value.'
     ' Short fn, 5 effective instructions, indeg=0.'),

    # PLATE-2: tick_zone_sprite_pipeline_with_chain_counter (0x08071604)
    # Fix: stale FUN_08090714 -> count_effect_node_zone_activations
    #      stale FUN_08096a4c -> set_equip_activation_state_by_mode__08096a4c
    (0x08071604,
     'tick_zone_sprite_pipeline_with_chain_counter: Accepts slot_ptr (r0). Reads gP1LifePoints+0x4a0 (scene state code). Supports two states:'
     ' State 0x80: calls count_effect_node_zone_activations (external check);'
     ' if nonzero calls trigger_card_display_op31_if_not_active(player_id, 0x6e)'
     ' and set_equip_activation_state_by_mode__08096a4c; returns 0x7f.'
     ' State 0x7f: checks gP1LP+0x4a4 (chain counter field) is nonzero;'
     ' if nonzero calls tick_zone_sprite_pipeline_with_update_flag with player_id and update_flag=1,'
     ' decrements counter field by 1; returns 0x7f.'
     ' Other states: returns 0.'
     ' Drives sprite pipeline updates and manages chain counter during equip chain activation.'
     ' Side effects: decrements [gP1LP+0x4a4]; updates sprite state via tick_zone_sprite_pipeline_with_update_flag.'
     ' Constants:'
     ' SCENE_STATE_OFFSET = 0x4a0 (gP1LP+0x4a0 = 0x201b730);'
     ' CHAIN_COUNT_OFFSET = 0x4a4 (gP1LP+0x4a4 = 0x201b734);'
     ' STATE_ACTIVATE = 0x80; STATE_TICK_PIPELINE = 0x7f'),

]


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _apply_plate(func_addr, plate_text):
    # ASCII guard
    bad = any(ord(ch) > 127 for ch in plate_text)
    if bad:
        print("[FAIL] non-ASCII char in plate text @ 0x%08x -- abort this plate" % func_addr)
        return False

    if DRY:
        print("[dry] PLATE 0x%08x  len=%d" % (func_addr, len(plate_text)))
        print("      text[:80]: %s" % plate_text[:80])
        return True

    a = _addr(func_addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[FAIL] PLATE 0x%08x: no CodeUnit at address" % func_addr)
        return False

    cu.setComment(CodeUnit.PLATE_COMMENT, plate_text)

    # Verify the plate was actually set (treat setPlateComment WARN as FAIL)
    actual = cu.getComment(CodeUnit.PLATE_COMMENT)
    if actual is None or len(actual.strip()) == 0:
        print("[FAIL] PLATE 0x%08x: setComment returned but plate is empty/None (WARN->FAIL)" % func_addr)
        return False

    # Verify no non-ASCII leaked in
    bad2 = any(ord(ch) > 127 for ch in actual)
    if bad2:
        print("[FAIL] PLATE 0x%08x: non-ASCII present in plate after write (mojibake)" % func_addr)
        return False

    print("[PLATE] 0x%08x  len=%d  OK" % (func_addr, len(actual)))
    return True


def main():
    print("=== RefineF09Seg3Plates (DRY=%s) ===" % DRY)
    print("  PLATE-1: CJK rewrite @ 0x0807158c")
    print("  PLATE-2: stale FUN_ fix @ 0x08071604")

    ok = fail = 0
    for func_addr, plate_text in PLATE_FIX:
        if _apply_plate(func_addr, plate_text):
            ok += 1
        else:
            fail += 1

    print("\n  PLATE done: %d ok, %d fail" % (ok, fail))
    if fail > 0:
        print("  !!! %d PLATE FAILURES !!!" % fail)
    print("=== RefineF09Seg3Plates DONE ===")


main()
