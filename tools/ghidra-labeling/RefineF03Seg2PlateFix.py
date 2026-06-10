# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF03Seg2PlateFix.py -- file 03 Seg-2 plate fix-forward (C8 audit fix)
#
# Independent audit found 4 stale FUN_ references in plate comments that
# were written by the original RefineF03Seg2Slots.py run.
# This script rewrites only those 4 plates with corrected current names.
#
# Changes (all pure ASCII, no CJK):
#   PLATE-5  0x08036cb8  FUN_08032280 -> dispatch_card_placement_by_zone_type
#   PLATE-6  0x08036d08  FUN_08032280 -> dispatch_card_placement_by_zone_type
#   PLATE-8  0x08036de8  FUN_08032194 -> erase_slot_from_zone_array_by_type
#   PLATE-11 0x08037030  FUN_080bb4c2 -> dispatch_equip_activation_full_sequence
#             (0x080bb4c2 is a bl-site inside dispatch_equip_activation_full_sequence,
#              not a function entry; callers list now uses function name)
#
# No EQ/RENAME/carve changes. byte-identical: plates are .rep-only, no ROM bytes.

from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

# ---------------------------------------------------------------------------
# 4 plate rewrites: (func_addr_int, new_plate_ascii)
# All text must be pure ASCII (Jython double-UTF-8 issue with CJK).
# ---------------------------------------------------------------------------
PLATE_FIX = [

    # PLATE-5: place_card_into_graveyard_slot (0x08036cb8)
    # Fix: FUN_08032280 -> dispatch_card_placement_by_zone_type
    (0x08036cb8,
     'place_card_into_graveyard_slot: Places a card into the player graveyard array (gP1HandSlotArray+0x418 path).'
     ' r0=card_slot_ptr. Extracts player_id from card_slot_ptr[0].bit14.'
     ' Graveyard count: [gP1HandCountBase + player*PLAYER_BLOCK_STRIDE].'
     ' Graveyard array: gP1HandSlotArray + player*PLAYER_BLOCK_STRIDE.'
     ' (HAND_ARRAY_TO_COUNT_NEG_OFF=0xfffffbfc maps gP1HandSlotArray -> gP1HandCountBase.)'
     ' If card_type(bits[18:0])!=0 and check_card_field8_is_9==0:'
     '   calls write_word_from_deref_src to write; increments count.'
     ' Simpler variant (no sequence word);'
     ' caller dispatch_card_placement_by_zone_type case 0xe (zone_type=14).'),

    # PLATE-6: place_card_into_graveyard_slot_with_seq (0x08036d08)
    # Fix: FUN_08032280 -> dispatch_card_placement_by_zone_type
    (0x08036d08,
     'place_card_into_graveyard_slot_with_seq: Places a card into the player graveyard array with a sequence word.'
     ' r0=card_slot_ptr (->r9 via 0x4681), r1=sequence_word (->r10 via 0x468a).'
     ' Extracts player_id from card_slot_ptr[0].bit14.'
     ' Count field: [gP1LifePoints + player*PLAYER_BLOCK_STRIDE + 0x1c].'
     ' Array base: gP1LifePoints + player*PLAYER_BLOCK_STRIDE + 0xba*8 (=0x5d0).'
     ' If card_type!=0 and check_card_field8_is_9==0:'
     '   write_word_from_deref_src(slot_ptr),'
     '   store sequence halfword at array+count*2+gP1LP+0xf1*8,'
     '   increment count.'
     ' Caller dispatch_card_placement_by_zone_type case 0xf (zone_type=15).'),

    # PLATE-8: erase_slot_from_equip_array_a_by_ptr (0x08036de8)
    # Fix: FUN_08032194 -> erase_slot_from_zone_array_by_type
    (0x08036de8,
     'erase_slot_from_equip_array_a_by_ptr: Searches equip array A for element matching card_ptr; deletes it.'
     ' r0=player_id [0..1], r1=card_ptr (->r7).'
     ' Array A base: gP1LifePoints + player*PLAYER_BLOCK_STRIDE + 0x83*8 (=0x418).'
     ' Count field offset: 0x14.'
     ' Backward scan from count-1 to 0 via check_deref_words_equal.'
     ' On match: calls remove_equip_slot_by_index_from_array_a; returns 1.'
     ' Returns 0 if not found.'
     ' Caller erase_slot_from_zone_array_by_type (duel_field) cleans up equip array A when a card leaves the field.'),

    # PLATE-11: find_deck_slot_by_card_pair_match (0x08037030)
    # Fix: FUN_080bb4c2 is a bl-site inside dispatch_equip_activation_full_sequence,
    #      not a function entry point; replace with function name in caller list.
    (0x08037030,
     'find_deck_slot_by_card_pair_match: Searches extra-deck array for a card_id passing check_card_pair_allowed(card_id, filter).'
     ' r0=player_id, r1=card_id_filter (->r6, low 16 bits).'
     ' Extra-deck count: gP1LifePoints + player*PLAYER_BLOCK_STRIDE + 0x14.'
     ' Array: gP1HandSlotArray + player*PLAYER_BLOCK_STRIDE (0x83*8=0x418 offset).'
     ' Backward scan from count-1 to 0; extracts card_id bits[12:0] from each word;'
     ' calls check_card_pair_allowed(card_id, filter); on hit returns index.'
     ' Returns -1 if no match (movs r0,#1; rsbs r0,r0,#0).'
     ' indeg>=7; callers include dispatch_equip_activation_full_sequence'
     ' and duel_field at 0x080637a2/0x08063bd2/0x08066d74/0x0807ecbe/0x080833e0.'),

]  # end PLATE_FIX


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _apply_plate(func_addr, new_plate):
    """Overwrite the plate comment at func_addr with new_plate (pure ASCII)."""
    a = _addr(func_addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[WARN] plate_fix 0x%08x: no code unit -- skipping" % func_addr)
        return False

    if DRY:
        old = cu.getComment(CodeUnit.PLATE_COMMENT) or ""
        print("[dry] PLATE_FIX 0x%08x  old_len=%d new_len=%d" % (func_addr, len(old), len(new_plate)))
        # Show first occurrence of FUN_ in old text for verification
        idx = old.find("FUN_")
        if idx >= 0:
            print("  old snippet: ...%s..." % old[max(0, idx-10):idx+20])
        return True

    cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)

    # Readback check: confirm no FUN_ remains in the new plate
    readback = cu.getComment(CodeUnit.PLATE_COMMENT) or ""
    if "FUN_" in readback:
        print("[FAIL] PLATE_FIX 0x%08x: FUN_ still present after write!" % func_addr)
        return False
    print("[PLT] 0x%08x plate rewritten OK (len=%d, FUN_=0)" % (func_addr, len(readback)))
    return True


def main():
    print("=== RefineF03Seg2PlateFix (DRY=%s) ===" % DRY)
    print("  Fix 4 stale FUN_ plate refs in Seg-2 (0x08036a78..0x08037128)")

    ok = 0
    fail = 0
    for func_addr, new_plate in PLATE_FIX:
        # Sanity: verify new_plate is ASCII-only
        try:
            new_plate.encode("ascii")
        except (UnicodeEncodeError, UnicodeDecodeError):
            print("[ABORT] 0x%08x: new_plate contains non-ASCII! Fix the script." % func_addr)
            fail += 1
            continue

        if _apply_plate(func_addr, new_plate):
            ok += 1
        else:
            fail += 1

    print("\n=== RefineF03Seg2PlateFix DONE ===")
    print("  ok=%d  fail=%d  DRY=%s" % (ok, fail, DRY))
    if fail > 0:
        print("  WARNING: %d plate(s) failed -- inspect output above" % fail)


main()
