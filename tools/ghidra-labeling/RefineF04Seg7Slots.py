# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF04Seg7Slots.py -- file 04 Seg-7 (0x08044674..0x08044e30)
#   19 functions:
#   enqueue_graveyard_spell_sprite_and_lp / enqueue_graveyard_spell_sprite_with_zone_ref /
#   enqueue_hand_card_sprite_alt_by_zone_slot / enqueue_graveyard_spell_sprite_with_player_xor /
#   enqueue_equip_zone_sprite_by_slot_ptr / enqueue_equip_zone_sprite_with_attr_u16 /
#   enqueue_equip_zone_sprite_attr_shape_a / enqueue_equip_zone_sprite_attr_shape_b /
#   enqueue_hand_sprite_with_flip_flag_set / enqueue_hand_sprite_by_zone_set_code /
#   enqueue_sprite_attr_for_zone_slot_packed / enqueue_equip_chain_sprite_attrs_for_slot /
#   enqueue_equip_slot_sprite_by_player / enqueue_sprite_attr_row_0x29_by_player /
#   enqueue_sprite_attr_row_0x29_with_flag2 / enqueue_equip_slot_sprite_with_display_code /
#   enqueue_equip_zone_sprite_for_player / enqueue_equip_multi_slot_marker_sprite /
#   enqueue_field_slot_sprite_with_state_update
#
# Sections:
#   A. EQ_SLOTS    -- 35 slots (25 reuse + 10 new constants)
#   B. REF_SLOTS   -- 0 slots
#   C. RENAME_SLOTS -- 0 slots
#   D. PLATE_REWRITES -- 14 functions (13 substr + 1 full ASCII rewrite)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).
# NOTE: Slot labels MUST differ from .equ constant names (GAS ldr/equate conflict).
# NOTE: FUNC_RENAME = 0 (no function renames in this segment).
# NOTE: All 35 slot addresses verified via python struct.unpack_from on roms/2343.gba.
# NOTE: New constants (7):
#   card_info.inc: WATAPON_CID=0x17cc / WATAPON_EQUIP_ACTIVATION_MASK=0x34500000 / DARK_MIMIC_LV1_CID=0x17d5
#   oam_attr.inc: OAM_EQUIP_SLOT_SPRITE_P2=0x8029 / OAM_MULTI_SLOT_MARKER_P2=0x8048 / OAM_FIELD_SLOT_SPRITE_P2=0x8043
#   duel_field.inc: EQUIP_MULTI_SLOT_CTL_OFF=0x1ce0

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
#    All values verified against roms/2343.gba (python struct.unpack_from).
# ---------------------------------------------------------------------------
EQ_SLOTS = [

    # === enqueue_graveyard_spell_sprite_and_lp (0x08044674) ===
    (0x08044704, 0x0201c4e0, 'gP1LifePoints',                  'gspy_andlp_lp_base',
     'gP1LifePoints=0x0201c4e0: reuse ewram.inc'),
    (0x08044708, 0x00000868, 'PLAYER_BLOCK_STRIDE',            'gspy_andlp_stride',
     'PLAYER_BLOCK_STRIDE=0x868: reuse ewram.inc'),

    # === enqueue_graveyard_spell_sprite_with_zone_ref (0x08044714) ===
    (0x080447c0, 0x0201c4e0, 'gP1LifePoints',                  'gspy_zref_lp_base',
     'gP1LifePoints=0x0201c4e0: reuse ewram.inc'),
    (0x080447c4, 0x00000868, 'PLAYER_BLOCK_STRIDE',            'gspy_zref_stride',
     'PLAYER_BLOCK_STRIDE=0x868: reuse ewram.inc'),

    # === enqueue_hand_card_sprite_alt_by_zone_slot (0x080447d4) ===
    (0x0804488c, 0x0201c4e0, 'gP1LifePoints',                  'hspy_alt_lp_base',
     'gP1LifePoints=0x0201c4e0: reuse ewram.inc'),
    (0x08044890, 0x00000868, 'PLAYER_BLOCK_STRIDE',            'hspy_alt_stride',
     'PLAYER_BLOCK_STRIDE=0x868: reuse ewram.inc'),

    # === enqueue_graveyard_spell_sprite_with_player_xor (0x080448a0) ===
    (0x08044958, 0x0201c4e0, 'gP1LifePoints',                  'gspy_pxor_lp_base',
     'gP1LifePoints=0x0201c4e0: reuse ewram.inc'),
    (0x0804495c, 0x00000868, 'PLAYER_BLOCK_STRIDE',            'gspy_pxor_stride',
     'PLAYER_BLOCK_STRIDE=0x868: reuse ewram.inc'),

    # === enqueue_equip_zone_sprite_by_slot_ptr (0x08044970) ===
    (0x080449a0, 0x00008033, 'OAM_EQUIP_ZONE_SPRITE_P1',       'ezsp_slotptr_p2_attr',
     'OAM_EQUIP_ZONE_SPRITE_P1=0x8033: reuse oam_attr.inc; equip zone sprite P1 attr0'),

    # === enqueue_equip_zone_sprite_with_attr_u16 (0x080449a4) ===
    (0x080449d0, 0x00008033, 'OAM_EQUIP_ZONE_SPRITE_P1',       'ezsp_u16_p2_attr',
     'OAM_EQUIP_ZONE_SPRITE_P1=0x8033: reuse oam_attr.inc'),

    # === enqueue_hand_sprite_by_zone_set_code (0x08044a34) ===
    (0x08044b24, 0x0201c4e0, 'gP1LifePoints',                  'hspy_zset_lp_base',
     'gP1LifePoints=0x0201c4e0: reuse ewram.inc'),
    (0x08044b28, 0x00000868, 'PLAYER_BLOCK_STRIDE',            'hspy_zset_stride',
     'PLAYER_BLOCK_STRIDE=0x868: reuse ewram.inc'),
    # OAM_ATTR1_X_MASK: value 0x1ff reuse (C5 dedup -- same value as X-mask; used here as 9-bit iteration mask)
    (0x08044b2c, 0x000001ff, 'OAM_ATTR1_X_MASK',              'hspy_zset_hand_iter_mask',
     'OAM_ATTR1_X_MASK=0x1ff: reuse oam_attr.inc; C5 value dedup (9-bit mask for hand-slot iter offset)'),
    (0x08044b30, 0xfffffdff, 'OAM_SPRITE_ATTR_CLR_BIT9',       'hspy_zset_clr_bit9',
     'OAM_SPRITE_ATTR_CLR_BIT9=0xfffffdff: reuse oam_attr.inc; AND mask clears bit9 (player_side)'),
    (0x08044b34, 0xfffffe00, 'OAM_ATTR1_X_CLEAR',              'hspy_zset_clr_low9',
     'OAM_ATTR1_X_CLEAR=0xfffffe00: reuse oam_attr.inc; AND mask clears attr1 bits[8:0]'),
    # NEW: WATAPON_CID=0x17cc (card-stats.s card_1626 slot=0x17CC; pw=87774234)
    (0x08044b38, 0x000017cc, 'WATAPON_CID',                    'hspy_zset_watapon_cid',
     'WATAPON_CID=0x17cc: new card_info.inc; pw=87774234; card_1626 (Watapon); Watapon-path branch'),
    # NEW: WATAPON_EQUIP_ACTIVATION_MASK=0x34500000 (OR-ed into attr2 arg on Watapon path)
    (0x08044b3c, 0x34500000, 'WATAPON_EQUIP_ACTIVATION_MASK',  'hspy_zset_watapon_mask',
     'WATAPON_EQUIP_ACTIVATION_MASK=0x34500000: new card_info.inc; activation flag mask ORed into attr2 arg for Watapon path'),

    # === enqueue_equip_chain_sprite_attrs_for_slot (0x08044bac) ===
    (0x08044c30, 0x00000868, 'PLAYER_BLOCK_STRIDE',            'ecsa_slot_stride',
     'PLAYER_BLOCK_STRIDE=0x868: reuse ewram.inc'),
    (0x08044c34, 0x0201c5ec, 'gDuelFieldSpellZoneBase',        'ecsa_chain_base',
     'gDuelFieldSpellZoneBase=0x0201c5ec: reuse ewram.inc'),
    (0x08044c38, 0x0201d9c0, 'gEquipNodePool',                 'ecsa_node_pool',
     'gEquipNodePool=0x0201d9c0: reuse ewram.inc'),
    # NEW: DARK_MIMIC_LV1_CID=0x17d5 (card-stats.s card_1635 slot=0x17D5; pw=74713516)
    (0x08044c3c, 0x000017d5, 'DARK_MIMIC_LV1_CID',            'ecsa_card_type_a',
     'DARK_MIMIC_LV1_CID=0x17d5: new card_info.inc; pw=74713516; card_1635 (Dark Mimic LV1); card_type filter A'),
    (0x08044c80, 0x00001814, 'SILENT_SWORDSMAN_LV5_CID',       'ecsa_card_type_c',
     'SILENT_SWORDSMAN_LV5_CID=0x1814: reuse card_info.inc; card_type filter C'),

    # === enqueue_equip_slot_sprite_by_player (0x08044c84) ===
    # NEW: OAM_EQUIP_SLOT_SPRITE_P2=0x8029 (P2 counterpart of OAM_EQUIP_SLOT_SPRITE_P1=0x8034)
    (0x08044ca0, 0x00008029, 'OAM_EQUIP_SLOT_SPRITE_P2',       'essp_p2_attr',
     'OAM_EQUIP_SLOT_SPRITE_P2=0x8029: new oam_attr.inc; P2 equip slot sprite attr0 (bit15+0x29)'),

    # === enqueue_sprite_attr_row_0x29_by_player (0x08044ca4) ===
    (0x08044cc0, 0x00008029, 'OAM_EQUIP_SLOT_SPRITE_P2',       'spar29_p2_attr',
     'OAM_EQUIP_SLOT_SPRITE_P2=0x8029: reuse oam_attr.inc'),

    # === enqueue_sprite_attr_row_0x29_with_flag2 (0x08044cc4) ===
    (0x08044ce0, 0x00008029, 'OAM_EQUIP_SLOT_SPRITE_P2',       'spar29f2_p2_attr',
     'OAM_EQUIP_SLOT_SPRITE_P2=0x8029: reuse oam_attr.inc'),

    # === enqueue_equip_slot_sprite_with_display_code (0x08044ce4) ===
    (0x08044d04, 0x00008029, 'OAM_EQUIP_SLOT_SPRITE_P2',       'esdc_p2_attr',
     'OAM_EQUIP_SLOT_SPRITE_P2=0x8029: reuse oam_attr.inc'),

    # === enqueue_equip_zone_sprite_for_player (0x08044d08) ===
    (0x08044d3c, 0x00008029, 'OAM_EQUIP_SLOT_SPRITE_P2',       'ezfp_p2_attr',
     'OAM_EQUIP_SLOT_SPRITE_P2=0x8029: reuse oam_attr.inc'),
    (0x08044d40, 0x00000868, 'PLAYER_BLOCK_STRIDE',            'ezfp_stride',
     'PLAYER_BLOCK_STRIDE=0x868: reuse ewram.inc'),
    (0x08044d44, 0x0201c740, 'gP1SlotSetCodeArray',            'ezfp_zone_base',
     'gP1SlotSetCodeArray=0x0201c740: reuse ewram.inc'),

    # === enqueue_equip_multi_slot_marker_sprite (0x08044d48) ===
    (0x08044d8c, 0x0201c4e0, 'gP1LifePoints',                  'emms_lp_base',
     'gP1LifePoints=0x0201c4e0: reuse ewram.inc'),
    (0x08044d90, 0x00000868, 'PLAYER_BLOCK_STRIDE',            'emms_stride',
     'PLAYER_BLOCK_STRIDE=0x868: reuse ewram.inc'),
    # NEW: OAM_MULTI_SLOT_MARKER_P2=0x8048 (P2 counterpart P1=0x48 inline movs)
    (0x08044dc8, 0x00008048, 'OAM_MULTI_SLOT_MARKER_P2',       'emms_p2_attr',
     'OAM_MULTI_SLOT_MARKER_P2=0x8048: new oam_attr.inc; P2 multi-slot selection marker sprite attr0 (bit15+0x48)'),

    # === enqueue_field_slot_sprite_with_state_update (0x08044dcc) ===
    (0x08044e24, 0x00000868, 'PLAYER_BLOCK_STRIDE',            'efss_stride',
     'PLAYER_BLOCK_STRIDE=0x868: reuse ewram.inc'),
    (0x08044e28, 0x0201c510, 'gDuelFieldSlots',                'efss_field_slots',
     'gDuelFieldSlots=0x0201c510: reuse ewram.inc'),
    # NEW: OAM_FIELD_SLOT_SPRITE_P2=0x8043 (P2 counterpart P1=0x43 inline movs)
    (0x08044e2c, 0x00008043, 'OAM_FIELD_SLOT_SPRITE_P2',       'efss_p2_attr',
     'OAM_FIELD_SLOT_SPRITE_P2=0x8043: new oam_attr.inc; P2 duel field slot sprite attr0 (bit15+0x43)'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: none in Seg-7
# ---------------------------------------------------------------------------
REF_SLOTS = []

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: none in Seg-7
#    (rezslp_cid_graverobber at 0x08044670 is already correctly named from Seg-6; no change needed)
# ---------------------------------------------------------------------------
RENAME_SLOTS = []

# ---------------------------------------------------------------------------
# D. PLATE_REWRITES: 14 functions (13 substr + 1 full ASCII rewrite)
#    Total FUN_ tokens: 1+1+1+1+1+2+7+2+3+1+1+2+1+2 = 26
# ---------------------------------------------------------------------------
PLATE_REWRITES = [

    # --- 1. enqueue_hand_card_sprite_alt_by_zone_slot (0x080447d4) ---
    # 1 FUN_ token: FUN_08077318 -> enqueue_hand_card_sprite_alt_with_zone_decrement
    (0x080447d4, 'substr', 'FUN_08077318', 'enqueue_hand_card_sprite_alt_with_zone_decrement'),

    # --- 2. enqueue_graveyard_spell_sprite_with_player_xor (0x080448a0) ---
    # 1 FUN_ token: FUN_0806c780 -> enqueue_graveyard_spell_sprite_from_hand
    (0x080448a0, 'substr', 'FUN_0806c780', 'enqueue_graveyard_spell_sprite_from_hand'),

    # --- 3. enqueue_equip_zone_sprite_with_attr_u16 (0x080449a4) ---
    # 1 FUN_ token: FUN_0807fde8 -> dispatch_equip_criteria_display_by_type_code
    (0x080449a4, 'substr', 'FUN_0807fde8', 'dispatch_equip_criteria_display_by_type_code'),

    # --- 4. enqueue_equip_zone_sprite_attr_shape_b (0x08044a00) ---
    # 1 FUN_ token: FUN_0807f458 -> dispatch_equip_zone_sprite_shape_b_by_state
    (0x08044a00, 'substr', 'FUN_0807f458', 'dispatch_equip_zone_sprite_shape_b_by_state'),

    # --- 5. enqueue_hand_sprite_with_flip_flag_set (0x08044a28) ---
    # 1 FUN_ token: FUN_0807cef0 -> apply_equip_activation_with_neo_daedalus_lp_output
    (0x08044a28, 'substr', 'FUN_0807cef0', 'apply_equip_activation_with_neo_daedalus_lp_output'),

    # --- 6. enqueue_hand_sprite_by_zone_set_code (0x08044a34) ---
    # 2 FUN_ tokens
    (0x08044a34, 'substr', 'FUN_08044a28', 'enqueue_hand_sprite_with_flip_flag_set'),
    (0x08044a34, 'substr', 'FUN_0807cef0', 'apply_equip_activation_with_neo_daedalus_lp_output'),

    # --- 7. enqueue_sprite_attr_for_zone_slot_packed (0x08044b5c) ---
    # FULL ASCII REWRITE (existing plate has CJK text)
    # 7 FUN_ stale refs resolved in the new ASCII plate below
    (0x08044b5c, 'full',
     'Called by update_equip_zone_sprite_by_state (case_3 at 0x0809bd9a), '
     'enqueue_pair_zone_sprite_attr_by_card_id, '
     'enqueue_zone_sprite_with_hand_and_monster_slot, '
     'enqueue_hand_to_monster_slot_equip_sprite, '
     'enqueue_equip_zone_sprite_with_slot_setup, '
     'tick_equip_activation_display_state_machine, '
     'tick_equip_oam_activation_text_display (indeg>=7). '
     'Entry: r0=player_side->r6; r1=slot_idx; r2=tile_id->r5; r3=extra_field->r8; '
     'sp[0x14]=sp5_field; sp[0x18]=y_byte0; sp[0x1c]=y_byte1. '
     'Builds OAM attr1: (tile_id&0xff)<<6|(slot_idx&0x1f)<<1|(player_side&1). '
     'Builds OAM attr2: (sp5&0x1f)<<1|(extra_field&0xff). '
     'Builds y coord: merge sp[0x18]/sp[0x1c] bytes as 16-bit y field. '
     'Fixed attr0=0x41 (Y=65, OBJ normal, square). '
     'Calls enqueue_sprite_attr_record(0x41, attr1, attr2, y_pack). '
     'Side effects: writes one attr0=0x41 record to OAM sprite queue. '
     'Constants: OAM_ATTR0_Y65=0x41, slot_bits=5, tile_mask=0xff.',
     None),

    # --- 8. enqueue_equip_chain_sprite_attrs_for_slot (0x08044bac) ---
    # 2 FUN_ tokens
    (0x08044bac, 'substr', 'FUN_0806e898', 'dispatch_equip_chain_state_sprite_by_slot'),
    (0x08044bac, 'substr', 'FUN_080744f8', 'dispatch_equip_zone_bitmap_or_neo_daedalus_sprite'),

    # --- 9. enqueue_equip_slot_sprite_by_player (0x08044c84) ---
    # 3 FUN_ tokens
    (0x08044c84, 'substr', 'FUN_08080c9c', 'enqueue_equip_slot_sprite_with_code_rotation'),
    (0x08044c84, 'substr', 'FUN_08044ca4', 'enqueue_sprite_attr_row_0x29_by_player'),
    (0x08044c84, 'substr', 'FUN_08044cc4', 'enqueue_sprite_attr_row_0x29_with_flag2'),

    # --- 10. enqueue_sprite_attr_row_0x29_by_player (0x08044ca4) ---
    # 1 FUN_ token
    (0x08044ca4, 'substr', 'FUN_0807c388', 'tick_equip_activation_display_state'),

    # --- 11. enqueue_sprite_attr_row_0x29_with_flag2 (0x08044cc4) ---
    # 1 FUN_ token
    (0x08044cc4, 'substr', 'FUN_08083ba0', 'tick_equip_activation_sprite_array_4state'),

    # --- 12. enqueue_equip_slot_sprite_with_display_code (0x08044ce4) ---
    # 2 FUN_ tokens
    (0x08044ce4, 'substr', 'FUN_08069d08', 'dispatch_zone_activation_display_by_confirm_state'),
    (0x08044ce4, 'substr', 'FUN_08080d40', 'pack_equip_slot_sprite_with_code_attr'),

    # --- 13. enqueue_equip_zone_sprite_for_player (0x08044d08) ---
    # 1 FUN_ token
    (0x08044d08, 'substr', 'FUN_0807512c', 'dispatch_equip_display_state_by_code'),

    # --- 14. enqueue_equip_multi_slot_marker_sprite (0x08044d48) ---
    # 2 FUN_ tokens
    (0x08044d48, 'substr', 'FUN_08072890', 'dispatch_equip_slot_sprite_by_activation_state'),
    (0x08044d48, 'substr', 'FUN_0807c158', 'enqueue_multi_slot_marker_sprite_for_node'),
]

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

def _check(slot_addr, expected_val, label):
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
        print("[dry] EQ 0x%08x  %s=0x%x  label=%s" % (slot_addr, eq_name, value, slot_label))
        return

    eq = eq_tbl.getEquate(eq_name)
    if eq is None:
        eq = eq_tbl.createEquate(eq_name, value & 0xFFFFFFFFFFFFFFFFL)
    eq.addReference(a, 0)

    existing = sym_tbl.getSymbols(a)
    names = [s.getName() for s in existing]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)

    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[EQ ] 0x%08x  %s  -> %s" % (slot_addr, eq_name, slot_label))

def _apply_ref(slot_addr, target_addr, gas_label, slot_label, eol):
    a_slot = _addr(slot_addr)
    a_target = _addr(target_addr)
    sym_tbl = currentProgram.getSymbolTable()
    ref_mgr = currentProgram.getReferenceManager()
    listing = currentProgram.getListing()

    if DRY:
        print("[dry] REF 0x%08x -> %s(0x%x) slot=%s" % (slot_addr, gas_label, target_addr, slot_label))
        return

    tgt_syms = sym_tbl.getSymbols(a_target)
    tgt_names = [s.getName() for s in tgt_syms]
    if gas_label not in tgt_names:
        sym_tbl.createLabel(a_target, gas_label, SourceType.USER_DEFINED)

    slot_syms = sym_tbl.getSymbols(a_slot)
    slot_names = [s.getName() for s in slot_syms]
    if slot_label not in slot_names:
        sym_tbl.createLabel(a_slot, slot_label, SourceType.USER_DEFINED)

    ref_mgr.addMemoryReference(a_slot, a_target, RefType.DATA, SourceType.USER_DEFINED, 0)
    for sym in sym_tbl.getSymbols(a_slot):
        if sym.getName() == slot_label:
            sym.setPrimary()
            break

    if eol:
        cu = listing.getCodeUnitAt(a_slot)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[REF] 0x%08x -> %s (gas=%s slot=%s)" % (slot_addr, hex(target_addr), gas_label, slot_label))

def _apply_plate_substr(func_addr, old_text, new_text):
    a = _addr(func_addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[WARN] plate_substr 0x%08x: no code unit" % func_addr)
        return

    existing = cu.getComment(CodeUnit.PLATE_COMMENT)
    if existing is None:
        print("[WARN] plate_substr 0x%08x: no plate comment" % func_addr)
        return

    if old_text not in existing:
        print("[WARN] plate_substr 0x%08x: '%s' not found in plate" % (func_addr, old_text))
        return

    if DRY:
        print("[dry] PLATE_SUBSTR 0x%08x: '%s' -> '%s'" % (func_addr, old_text, new_text))
        return

    new_plate = existing.replace(old_text, new_text)
    cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)
    print("[PFX] 0x%08x: '%s' -> '%s'" % (func_addr, old_text, new_text))

def _apply_plate_full(func_addr, new_text):
    a = _addr(func_addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[WARN] plate_full 0x%08x: no code unit" % func_addr)
        return

    if DRY:
        # Verify new_text is pure ASCII
        non_ascii = [c for c in new_text if ord(c) > 127]
        if non_ascii:
            print("[WARN] plate_full 0x%08x: non-ASCII chars in new text: %s" % (
                func_addr, repr(non_ascii[:5])))
        else:
            print("[dry] PLATE_FULL 0x%08x: ASCII OK, len=%d" % (func_addr, len(new_text)))
        return

    # Verify ASCII before writing
    non_ascii = [c for c in new_text if ord(c) > 127]
    if non_ascii:
        print("[SKIP] plate_full 0x%08x: non-ASCII chars detected, refusing to write" % func_addr)
        return

    cu.setComment(CodeUnit.PLATE_COMMENT, new_text)
    print("[FULL] 0x%08x: plate fully rewritten, len=%d" % (func_addr, len(new_text)))

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF04Seg7Slots (DRY=%s) ===" % DRY)
    print("  file 04 Seg-7: 0x08044674..0x08044e30, 19 fn, 35 slots")
    print("  EQ=%d  REF=%d  RENAME=%d  PLATE_entries=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATE_REWRITES)))

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    eq_ok = 0
    eq_skip = 0
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        _apply_eq(slot_addr, value, eq_name, slot_label, eol)
        eq_ok += 1
    print("  EQ done: %d" % eq_ok)

    # B. REF_SLOTS
    print("\n--- B. REF_SLOTS (%d) ---" % len(REF_SLOTS))
    print("  REF done: 0")

    # C. RENAME_SLOTS
    print("\n--- C. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    print("  RENAME done: 0")

    # D. PLATE_REWRITES
    print("\n--- D. PLATE_REWRITES (%d entries) ---" % len(PLATE_REWRITES))
    plate_ok = 0
    for entry in PLATE_REWRITES:
        func_addr, mode = entry[0], entry[1]
        if mode == 'substr':
            _apply_plate_substr(func_addr, entry[2], entry[3])
        elif mode == 'full':
            _apply_plate_full(func_addr, entry[2])
        else:
            print("[ERR] unknown mode '%s' for 0x%08x" % (mode, func_addr))
        plate_ok += 1
    print("  PLATE done: %d entries" % plate_ok)

    print("\n=== RefineF04Seg7Slots DONE ===")
    print("  EQ=%d  REF=%d  RENAME=%d  PLATE_entries=%d (DRY=%s)" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATE_REWRITES), DRY))

main()
