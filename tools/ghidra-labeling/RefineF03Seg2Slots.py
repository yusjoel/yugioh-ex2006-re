# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF03Seg2Slots.py -- file 03 Seg-2 (0x08036a78..0x08037128)
#   equip chain cont: graveyard/hand/field array ops + effect entry search (13 fn, 37 slots)
#   sum_equip_slot_effect_values_for_player / check_slot_card_eligible_for_special_action /
#   find_effect_entry_by_player_zone / build_effect_zone_entry /
#   place_card_into_graveyard_slot / place_card_into_graveyard_slot_with_seq /
#   remove_equip_slot_by_index_from_array_a / erase_slot_from_equip_array_a_by_ptr /
#   insert_card_into_hand_list_by_zone_desc / insert_card_into_field_list_by_zone_desc /
#   find_deck_slot_by_card_pair_match / find_graveyard_entry_by_ptr /
#   count_extra_deck_cards_by_id
#
# Sections:
#   A. EQ_SLOTS   -- data-equate (37 slots; reuse existing + new inc constants)
#   B. RENAME_SLOTS -- (none in this segment)
#   C. PLATE_FULL -- full plate rewrite for all 13 functions (pure ASCII, no FUN_/CJK)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).
# NOTE: New constants: card_info.inc x3, ewram.inc x4 written separately (B2 pipeline).

from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

# ---------------------------------------------------------------------------
# A. EQ_SLOTS: (slot_addr, value, eq_name, slot_label, eol_ascii_or_None)
#    Creates equate (value->name) and references it from slot address.
#    Slot label MUST differ from eq_name to avoid GAS ldr/equate conflict.
# ---------------------------------------------------------------------------
EQ_SLOTS = [

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x868 (12 slots) ---
    (0x08036ab8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'sum_equip_slot_values_stride', None),
    (0x08036b0c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_special_action_elig_stride', None),
    (0x08036b78, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_special_action_elig_stride_b', None),
    (0x08036cfc, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'place_card_graveyard_stride', None),
    (0x08036d7c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'place_card_graveyard_seq_stride', None),
    (0x08036dd8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'remove_equip_slot_a_stride', None),
    (0x08036e2c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'erase_equip_array_a_stride', None),
    (0x08036ee4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'insert_hand_list_stride', None),
    (0x08037000, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'insert_field_list_stride', None),
    (0x0803706c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'find_deck_slot_stride', None),
    (0x080370c4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'find_graveyard_entry_stride', None),
    (0x08037124, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_extra_deck_stride', None),

    # --- ewram.inc: gDuelFieldSlots = 0x0201c510 (3 slots) ---
    (0x08036abc, 0x0201c510, 'gDuelFieldSlots',
     'sum_equip_slot_values_slots', None),
    (0x08036b10, 0x0201c510, 'gDuelFieldSlots',
     'check_special_action_elig_slots', None),
    (0x08036b7c, 0x0201c510, 'gDuelFieldSlots',
     'check_special_action_elig_slots_b', None),

    # --- card_info.inc: GAP_CID_13EA = 0x000013ea (new; gap slot) ---
    (0x08036b2c, 0x000013ea, 'GAP_CID_13EA',
     'check_special_action_elig_cid_13ea', None),

    # --- card_info.inc: KUNAI_WITH_CHAIN_CID = 0x00001231 (new) ---
    (0x08036b30, 0x00001231, 'KUNAI_WITH_CHAIN_CID',
     'check_special_action_elig_kunai_cid', None),

    # --- card_info.inc: BLAST_WITH_CHAIN_CID = 0x00001514 (new) ---
    (0x08036b74, 0x00001514, 'BLAST_WITH_CHAIN_CID',
     'check_special_action_elig_blast_cid', None),

    # --- ewram.inc: gDuelPhaseFlags = 0x0201b290 (1 slot; reuse) ---
    (0x08036bf8, 0x0201b290, 'gDuelPhaseFlags',
     'find_effect_entry_phase_flags', None),

    # --- ewram.inc: EFFECT_ENTRY_COUNT_OFF = 0x00000594 (new) ---
    (0x08036bfc, 0x00000594, 'EFFECT_ENTRY_COUNT_OFF',
     'find_effect_entry_count_off', None),

    # --- ewram.inc: gEffectEntryArray = 0x0201b590 (new) ---
    (0x08036c00, 0x0201b590, 'gEffectEntryArray',
     'find_effect_entry_array', None),

    # --- gl_scrollbar.inc: SCROLLBAR_CLEAR_BITS_14_6 = 0xffff803f (reuse; C5 same value) ---
    (0x08036cb4, 0xffff803f, 'SCROLLBAR_CLEAR_BITS_14_6',
     'build_effect_zone_entry_mask', None),

    # --- ewram.inc: gP1HandSlotArray = 0x0201c8f8 (3 slots; reuse) ---
    (0x08036d00, 0x0201c8f8, 'gP1HandSlotArray',
     'place_card_graveyard_gy_base', None),
    (0x08036ee8, 0x0201c8f8, 'gP1HandSlotArray',
     'insert_hand_list_gy_base', None),
    (0x08037070, 0x0201c8f8, 'gP1HandSlotArray',
     'find_deck_slot_hand_base', None),

    # --- ewram.inc: HAND_ARRAY_TO_COUNT_NEG_OFF = 0xfffffbfc (new; 2 slots) ---
    (0x08036d04, 0xfffffbfc, 'HAND_ARRAY_TO_COUNT_NEG_OFF',
     'place_card_graveyard_count_neg_off', None),
    (0x08036eec, 0xfffffbfc, 'HAND_ARRAY_TO_COUNT_NEG_OFF',
     'insert_hand_list_count_neg_off', None),

    # --- ewram.inc: gP1LifePoints = 0x0201c4e0 (8 PTR slots) ---
    (0x08036d78, 0x0201c4e0, 'gP1LifePoints',
     'place_card_graveyard_seq_lp_ptr', None),
    (0x08036dd4, 0x0201c4e0, 'gP1LifePoints',
     'remove_equip_slot_a_lp_ptr', None),
    (0x08036e28, 0x0201c4e0, 'gP1LifePoints',
     'erase_equip_array_a_lp_ptr', None),
    (0x08036ee0, 0x0201c4e0, 'gP1LifePoints',
     'insert_hand_list_lp_ptr', None),
    (0x08036ffc, 0x0201c4e0, 'gP1LifePoints',
     'insert_field_list_lp_ptr', None),
    (0x08037068, 0x0201c4e0, 'gP1LifePoints',
     'find_deck_slot_lp_ptr', None),
    (0x080370c0, 0x0201c4e0, 'gP1LifePoints',
     'find_graveyard_entry_lp_ptr', None),
    (0x08037120, 0x0201c4e0, 'gP1LifePoints',
     'count_extra_deck_lp_ptr', None),

    # --- ewram.inc: gP1AltHandSlotArray = 0x0201cab0 (1 slot; reuse) ---
    (0x08037004, 0x0201cab0, 'gP1AltHandSlotArray',
     'insert_field_list_althand_base', None),

    # --- ewram.inc: ALT_HAND_ARRAY_TO_COUNT_NEG_OFF = 0xfffffa4c (new) ---
    (0x08037008, 0xfffffa4c, 'ALT_HAND_ARRAY_TO_COUNT_NEG_OFF',
     'insert_field_list_count_neg_off', None),

]  # end EQ_SLOTS (37 entries)

# ---------------------------------------------------------------------------
# B. RENAME_SLOTS: (slot_addr, new_label, eol_ascii_or_None)
#    No rename slots in Seg-2.
# ---------------------------------------------------------------------------
RENAME_SLOTS = []

# ---------------------------------------------------------------------------
# C. PLATE_FULL: (func_addr, new_plate_ascii_text)
#    Full plate rewrite. Text must be pure ASCII.
# ---------------------------------------------------------------------------
PLATE_FULL = [

    # PLATE-1: sum_equip_slot_effect_values_for_player (0x08036a78)
    (0x08036a78,
     'sum_equip_slot_effect_values_for_player: Sums effect card values for all active equip slots of a player.'
     ' r0=player_id [0..1].'
     ' Iterates slots 0..10 (gDuelFieldSlots stride=PLAYER_BLOCK_STRIDE=0x868, slot_stride=0x14).'
     ' Per slot: tests bit19 of slot[0] (activation flag); if set, checks slot[+0x8] card_id nonzero;'
     ' on both: calls get_slot_effect_card_value(player, slot_idx) and accumulates.'
     ' Returns r7 = sum of effect values across all 11 active equip slots.'
     ' 5 callers (duel_field AI + effect dispatch).'
     ' Constants: gDuelFieldSlots=0x0201c510, PLAYER_BLOCK_STRIDE=0x868, activation_bit=19.'),

    # PLATE-2: check_slot_card_eligible_for_special_action (0x08036ac0)
    (0x08036ac0,
     'check_slot_card_eligible_for_special_action: Checks equip activation eligibility for 5 special card_ids.'
     ' r0=player_id [0..1]; r1=slot_idx [0..0xb]; r2=card_id [0..0x172f].'
     ' Steps: (1) card_id==0 -> return 0; (2) slot in [5..9] -> check_card_field5_is_nonzero, hit->1;'
     ' (3) get_card_extended_stat_field9==3 -> slot in [5..0xa] active_bit check at gDuelFieldSlots+8;'
     ' (4) field9!=3 -> match against 5 special CIDs:'
     '   GAP_CID_13EA(0x13ea,gap), KUNAI_WITH_CHAIN_CID(0x1231), KUNAI+7=Metalmorph(0x1238),'
     '   BLAST_WITH_CHAIN_CID(0x1514), 0xcc<<5=Hero_Heyro(0x1980);'
     '   on match: slot in [0..4] and active_bit nonzero and [slot+0x10].bit1==0 -> return 1.'
     ' Returns 1 if eligible, 0 if not. 5 callers (duel_field/effect). Read-only.'
     ' Constants: gDuelFieldSlots=0x0201c510, PLAYER_BLOCK_STRIDE=0x868.'),

    # PLATE-3: find_effect_entry_by_player_zone (0x08036b88)
    (0x08036b88,
     'find_effect_entry_by_player_zone: Reverse-scans effect entry array for an entry matching player_side and zone_type.'
     ' gEffectEntryArray=0x0201b590, stride=0x18.'
     ' count = [gDuelPhaseFlags + EFFECT_ENTRY_COUNT_OFF(0x594)].'
     ' Per candidate: [+2].bit0==r10(player_side) and [+2].bits[1..5]==r9(zone_type).'
     ' Inner loop: calls read_effect_slot_side_and_type(entry, sub_slot_idx) for each sub-slot,'
     ' compares packed result (slot_idx<<8|player_side) against key; returns 1 on first full match.'
     ' r0=u32 player_side [0..1], r1=u32 slot_idx [0..4] (stacked), r2=player_side->r10, r3=zone_type->r9.'
     ' Returns u32 bool (1=match found, 0=not found). Read-only.'),

    # PLATE-4: build_effect_zone_entry (0x08036c2c)
    (0x08036c2c,
     'build_effect_zone_entry: Builds and submits an effect zone entry for player_side(r0), zone_idx(r1 >=5).'
     ' zone_idx<=4 returns 0 immediately (monster zone ignored).'
     ' Steps: (1) get_zone_slot_ptr(player_side, zone_idx) -> slot_ptr r4;'
     ' (2) alloca 0x18 bytes stack, zero-fill via memset;'
     ' (3) write player_side&1 to buf[+2].bit0 and zone_idx&0x1f to buf[+2].bits[1..5];'
     ' (4) read card_id bits[12:0] from slot_ptr, write to buf[+0];'
     ' (5) pack extra fields into buf[+4] using mask SCROLLBAR_CLEAR_BITS_14_6(0xffff803f);'
     ' (6) clear buf[+3] bits 0x31;'
     ' (7) call check_card_placement_rules(buf) and return result.'
     ' Returns 0 on early exit, else check_card_placement_rules result.'),

    # PLATE-5: place_card_into_graveyard_slot (0x08036cb8)
    (0x08036cb8,
     'place_card_into_graveyard_slot: Places a card into the player graveyard array (gP1HandSlotArray+0x418 path).'
     ' r0=card_slot_ptr. Extracts player_id from card_slot_ptr[0].bit14.'
     ' Graveyard count: [gP1HandCountBase + player*PLAYER_BLOCK_STRIDE].'
     ' Graveyard array: gP1HandSlotArray + player*PLAYER_BLOCK_STRIDE.'
     ' (HAND_ARRAY_TO_COUNT_NEG_OFF=0xfffffbfc maps gP1HandSlotArray -> gP1HandCountBase.)'
     ' If card_type(bits[18:0])!=0 and check_card_field8_is_9==0:'
     '   calls write_word_from_deref_src to write; increments count.'
     ' Simpler variant (no sequence word); caller FUN_08032280 case 0xe (zone_type=14).'),

    # PLATE-6: place_card_into_graveyard_slot_with_seq (0x08036d08)
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
     ' Caller FUN_08032280 case 0xf (zone_type=15).'),

    # PLATE-7: remove_equip_slot_by_index_from_array_a (0x08036d80)
    (0x08036d80,
     'remove_equip_slot_by_index_from_array_a: Removes element by index from equip array A and left-shifts remainder.'
     ' r0=player_id [0..1], r1=slot_idx [0..count-1].'
     ' Array A base: gP1LifePoints + player*PLAYER_BLOCK_STRIDE + 0x83*8 (=0x418).'
     ' Count field: gP1LifePoints + player*PLAYER_BLOCK_STRIDE + 0x14.'
     ' If slot_idx>=count returns 0;'
     ' else: decrement count; if slot_idx<new_count shift elements [idx+1..new_count]'
     '   left via write_word_from_deref_src loop; return 1.'
     ' Called by erase_slot_from_equip_array_a_by_ptr after ptr match.'),

    # PLATE-8: erase_slot_from_equip_array_a_by_ptr (0x08036de8)
    (0x08036de8,
     'erase_slot_from_equip_array_a_by_ptr: Searches equip array A for element matching card_ptr; deletes it.'
     ' r0=player_id [0..1], r1=card_ptr (->r7).'
     ' Array A base: gP1LifePoints + player*PLAYER_BLOCK_STRIDE + 0x83*8 (=0x418).'
     ' Count field offset: 0x14.'
     ' Backward scan from count-1 to 0 via check_deref_words_equal.'
     ' On match: calls remove_equip_slot_by_index_from_array_a; returns 1.'
     ' Returns 0 if not found.'
     ' Caller FUN_08032194 (duel_field) cleans up equip array A when card leaves field.'),

    # PLATE-9: insert_card_into_hand_list_by_zone_desc (0x08036e40)
    (0x08036e40,
     'insert_card_into_hand_list_by_zone_desc: Searches player hand list for target card by zone_desc; shifts it to front.'
     ' r0=player_side (bit0), r1=target zone_desc (u16 [0..0xffff]).'
     ' Hand count: gP1LifePoints + player*PLAYER_BLOCK_STRIDE + 0x14.'
     ' Hand array A: gP1LifePoints + player*PLAYER_BLOCK_STRIDE + 0x83*8 (=0x418).'
     ' (HAND_ARRAY_TO_COUNT_NEG_OFF=0xfffffbfc maps gP1HandSlotArray -> gP1HandCountBase.)'
     ' Zone desc match: bits[23:16] and bit[13] of slot word.'
     ' On match: swap_deref_words then write_word_from_deref_src to shift subsequent slots.'
     ' Symmetric to insert_card_into_field_list_by_zone_desc (zone_type=0xe path).'),

    # PLATE-10: insert_card_into_field_list_by_zone_desc (0x08036f0c)
    (0x08036f0c,
     'insert_card_into_field_list_by_zone_desc: Searches player field slot list for target by zone_desc; inserts via dual array shift.'
     ' r0=player_side (bit0), r1=target zone_desc (u16 [0..0xffff]).'
     ' Alt-hand count: gP1LifePoints + player*PLAYER_BLOCK_STRIDE + 0x1c.'
     ' Array A: gP1AltHandSlotArray + player*PLAYER_BLOCK_STRIDE (0xba*8=0x5d0 offset base).'
     ' Array B: gP1LifePoints + player*PLAYER_BLOCK_STRIDE + 0xf1*8 (=0x788).'
     ' (ALT_HAND_ARRAY_TO_COUNT_NEG_OFF=0xfffffa4c maps gP1AltHandSlotArray -> gP1AltHandCountBase.)'
     ' Zone desc match same as insert_card_into_hand_list_by_zone_desc.'
     ' On match: dual array shift (write_word_from_deref_src + strh for arrays A and B).'
     ' Symmetric to insert_card_into_hand_list (zone_type=0xf path).'),

    # PLATE-11: find_deck_slot_by_card_pair_match (0x08037030)
    # This function had CJK in its plate (asm Line 2334) -- must be replaced with pure ASCII.
    (0x08037030,
     'find_deck_slot_by_card_pair_match: Searches extra-deck array for a card_id passing check_card_pair_allowed(card_id, filter).'
     ' r0=player_id, r1=card_id_filter (->r6, low 16 bits).'
     ' Extra-deck count: gP1LifePoints + player*PLAYER_BLOCK_STRIDE + 0x14.'
     ' Array: gP1HandSlotArray + player*PLAYER_BLOCK_STRIDE (0x83*8=0x418 offset).'
     ' Backward scan from count-1 to 0; extracts card_id bits[12:0] from each word;'
     ' calls check_card_pair_allowed(card_id, filter); on hit returns index.'
     ' Returns -1 if no match (movs r0,#1; rsbs r0,r0,#0).'
     ' indeg>=7; callers include FUN_080bb4c2 and duel_field at 0x080637a2/0x08063bd2/0x08066d74/0x0807ecbe/0x080833e0.'),

    # PLATE-12: find_graveyard_entry_by_ptr (0x08037088)
    (0x08037088,
     'find_graveyard_entry_by_ptr: Searches player graveyard array for entry matching target_ptr; returns 1-based index.'
     ' r0=player_id [0..1], r1=target_ptr (->r7).'
     ' Graveyard base: gP1LifePoints + player*PLAYER_BLOCK_STRIDE + 0x83*8 (=0x418).'
     ' Count: gP1LifePoints + player*PLAYER_BLOCK_STRIDE + 0x14.'
     ' Forward scan; calls check_deref_words_equal each step; on match returns index+1 (1-based).'
     ' Returns 0 if not found. Read-only.'
     ' 3 callers: 0x08044674, 0x08044714, 0x080448a0 (duel_field).'),

    # PLATE-13: count_extra_deck_cards_by_id (0x080370dc)
    (0x080370dc,
     'count_extra_deck_cards_by_id: Counts extra-deck entries matching target card_id.'
     ' r0=player_id, r1=card_id filter (low 16 bits extracted to r6 via lsls/lsrs #0x10; non-APCS).'
     ' Extra-deck count: gP1LifePoints + player*PLAYER_BLOCK_STRIDE + 0x14.'
     ' Array: gP1LifePoints + player*PLAYER_BLOCK_STRIDE + 0x83*8 (=0x418).'
     ' For i=0..count-1: extract card_id bits[12:0]; compare with r6; hit -> r4++.'
     ' Returns r4 = total matching count.'
     ' indeg=0; referenced by runtime fn-ptr or dead code.'),

]  # end PLATE_FULL

# ===========================================================================
# Helpers (match RefineF03Seg1Slots.py style)
# ===========================================================================

def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

def _check(slot_addr, expected_val, label):
    """Verify ROM dword at slot_addr == expected_val. Return True if OK."""
    mem = currentProgram.getMemory()
    a = _addr(slot_addr)
    try:
        actual = mem.getInt(a) & 0xFFFFFFFF
    except Exception as e:
        print("[FAIL] _check 0x%08x (%s): read error %s" % (slot_addr, label, e))
        return False
    if actual != (expected_val & 0xFFFFFFFF):
        print("[FAIL] _check 0x%08x (%s): got 0x%08x expected 0x%08x" % (
            slot_addr, label, actual, expected_val & 0xFFFFFFFF))
        return False
    return True

def _apply_eq(slot_addr, value, eq_name, slot_label, eol):
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()
    eq_tbl = currentProgram.getEquateTable()

    if not _check(slot_addr, value, eq_name):
        print("[SKIP] EQ 0x%08x (%s) value mismatch" % (slot_addr, eq_name))
        return

    if DRY:
        print("[dry] EQ 0x%08x  %s=%s  label=%s" % (slot_addr, eq_name, hex(value), slot_label))
        return

    # create/get equate
    eq = eq_tbl.getEquate(eq_name)
    if eq is None:
        eq = eq_tbl.createEquate(eq_name, value & 0xFFFFFFFFFFFFFFFFL)
    eq.addReference(a, 0)

    # create slot label
    existing = sym_tbl.getSymbols(a)
    names = [s.getName() for s in existing]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)

    # EOL comment
    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[EQ ] 0x%08x  %s  -> %s" % (slot_addr, eq_name, slot_label))

def _apply_rename(slot_addr, slot_label, eol):
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()

    if DRY:
        print("[dry] RENAME 0x%08x -> %s" % (slot_addr, slot_label))
        return

    existing = sym_tbl.getSymbols(a)
    names = [s.getName() for s in existing]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)

    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[REN] 0x%08x -> %s" % (slot_addr, slot_label))

def _apply_plate_full(func_addr, new_plate):
    """Replace entire plate comment at func_addr with new_plate (pure ASCII)."""
    a = _addr(func_addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[WARN] plate_full 0x%08x: no code unit" % func_addr)
        return

    if DRY:
        print("[dry] PLATE_FULL 0x%08x (len=%d)" % (func_addr, len(new_plate)))
        return

    cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)
    print("[PLT] 0x%08x plate set (len=%d)" % (func_addr, len(new_plate)))

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF03Seg2Slots (DRY=%s) ===" % DRY)
    print("  Seg-2: 0x08036a78..0x08037128, 13 fn, graveyard/hand/field array ops")

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    eq_ok = 0
    eq_fail = 0
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        _apply_eq(slot_addr, value, eq_name, slot_label, eol)
        eq_ok += 1
    print("  EQ done: %d" % eq_ok)

    # B. RENAME_SLOTS
    print("\n--- B. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    for entry in RENAME_SLOTS:
        slot_addr, slot_label = entry[0], entry[1]
        eol = entry[2] if len(entry) > 2 else None
        _apply_rename(slot_addr, slot_label, eol)
    print("  RENAME done: %d" % len(RENAME_SLOTS))

    # C. PLATE_FULL
    print("\n--- C. PLATE_FULL (%d) ---" % len(PLATE_FULL))
    for func_addr, new_plate in PLATE_FULL:
        _apply_plate_full(func_addr, new_plate)
    print("  PLATE_FULL done: %d" % len(PLATE_FULL))

    print("\n=== RefineF03Seg2Slots DONE ===")
    print("  EQ=%d  RENAME=%d  PLATE_FULL=%d" % (
        len(EQ_SLOTS), len(RENAME_SLOTS), len(PLATE_FULL)))

main()
