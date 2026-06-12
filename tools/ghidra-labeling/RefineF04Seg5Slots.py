# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF04Seg5Slots.py -- file 04 Seg-5 (0x0804308c..0x0804394c)
#   19 functions:
#   enqueue_slot_card_sprite_if_eligible / enqueue_equip_zone_sprite_attr_with_select /
#   enqueue_equip_chain_slot_sprite_attr / enqueue_sprite_attr_for_chain_node_check /
#   enqueue_equip_chain_all_slots_for_pair / enqueue_sprite_attr_for_chain_node_match /
#   enqueue_equip_chain_sprite_by_side / enqueue_zone_slot_sprite_attr_by_card_type /
#   enqueue_equip_set_slot_sprite_by_zone_col / enqueue_equip_slot_sprite_attr_by_state /
#   scan_equip_chain_list_for_sprite_update / enqueue_equip_chain_attrs_for_slot_range /
#   scan_equip_chain_list_by_player_slot / scan_equip_chain_by_slot_for_update /
#   enqueue_sprite_attrs_for_card_chain_list / enqueue_slot_bitmap_type_d_for_equip /
#   enqueue_slot_sprite_by_state_and_type / enqueue_slot_sprite_attr_by_card_type_and_state /
#   enqueue_zone_slot_sprite_attr_if_occupied
#
# Sections:
#   A. EQ_SLOTS    -- 45 slots (31 reuse + 14 new constants)
#   B. REF_SLOTS   -- 0 slots
#   C. RENAME_SLOTS -- 3 slots
#   D. PLATE_REWRITES -- 9 functions (2 full ASCII rewrite + 7 substring replace)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).
# NOTE: Slot labels MUST differ from .equ constant names (GAS ldr/equate conflict).
# NOTE: FUNC_RENAME = 0 (no function renames in this segment).

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
    # === enqueue_slot_card_sprite_if_eligible (0x0804308c) ===
    (0x080430e0, 0x00008036, 'OAM_SPRITE_PAL_P1',           'enqueue_slot_card_pal_p1',
     'OAM_SPRITE_PAL_P1=0x8036: P1 OAM attr0 (bit15=1, group 0x36); P0 uses bare 0x36'),

    # === enqueue_equip_zone_sprite_attr_with_select (0x08043100) ===
    (0x08043124, 0x00008036, 'OAM_SPRITE_PAL_P1',           'enqueue_equip_zone_pal_p1',
     'OAM_SPRITE_PAL_P1=0x8036: P1 OAM attr0; enqueue_equip_zone_sprite_attr_with_select'),

    # === enqueue_equip_chain_slot_sprite_attr (0x08043128) ===
    (0x08043178, 0x00008037, 'OAM_EQUIP_CHAIN_SPRITE_P1',   'enqueue_equip_chain_slot_pal_p1',
     'OAM_EQUIP_CHAIN_SPRITE_P1=0x8037: equip chain node OAM attr0 P1 (bit15+0x37); 11 ROM refs'),

    # === enqueue_sprite_attr_for_chain_node_check (0x080431f4) ===
    (0x080431f0, 0x00008037, 'OAM_EQUIP_CHAIN_SPRITE_P1',   'enqueue_equip_slot_pal_p1',
     'OAM_EQUIP_CHAIN_SPRITE_P1=0x8037: reuse; enqueue_sprite_attr_for_chain_node_check P1 path'),

    # === enqueue_sprite_attr_for_chain_node_match (0x08043240) ===
    (0x0804323c, 0x00008037, 'OAM_EQUIP_CHAIN_SPRITE_P1',   'enqueue_sprite_for_chain_node_pal_p1',
     'OAM_EQUIP_CHAIN_SPRITE_P1=0x8037: reuse; enqueue_sprite_attr_for_chain_node_match P1 path'),

    # === enqueue_equip_chain_sprite_by_side (0x08043274) ===
    (0x08043270, 0x00008038, 'OAM_CHAIN_MATCH_SPRITE_P1',   'enqueue_sprite_chain_match_pal_p1',
     'OAM_CHAIN_MATCH_SPRITE_P1=0x8038: chain match OAM attr0 P1 (bit15+0x38); 82 ROM refs'),

    # === enqueue_zone_slot_sprite_attr_by_card_type (0x080432bc) ===
    (0x080432a4, 0x00008038, 'OAM_CHAIN_MATCH_SPRITE_P1',   'enqueue_equip_chain_by_side_pal_p1',
     'OAM_CHAIN_MATCH_SPRITE_P1=0x8038: reuse; enqueue_equip_chain_sprite_by_side P1 path'),

    # === enqueue_zone_slot_type_sprite_attr (0x08043340) -- via enqueue_zone_slot_sprite_attr_by_card_type ===
    (0x0804338c, 0x00008042, 'OAM_ZONE_TYPE_SPRITE_P1',     'enqueue_zone_slot_type_pal_p1',
     'OAM_ZONE_TYPE_SPRITE_P1=0x8042: zone card-type OAM attr0 P1 (bit15+0x42); 48 ROM refs'),

    # === Player stride / duel field pointers -- enqueue_zone_slot_sprite_attr_by_card_type ===
    (0x08043380, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'enqueue_zone_slot_type_stride',  None),
    (0x08043384, 0x0201c510, 'gDuelFieldSlots',              'enqueue_zone_slot_type_slots',   None),

    # === Card IDs -- enqueue_zone_slot_sprite_attr_by_card_type ===
    (0x08043390, 0x000013c3, 'GEARFRIED_IRON_KNIGHT_CID',   'enqueue_zone_slot_type_cid_iron_knight',
     'GEARFRIED_IRON_KNIGHT_CID=0x13c3: BST dispatch card_id in enqueue_zone_slot_sprite_attr_by_card_type'),
    (0x08043394, 0x0000186b, 'GEARFRIED_SWORDMASTER_CID',   'enqueue_zone_slot_type_cid_swordmaster',
     'GEARFRIED_SWORDMASTER_CID=0x186b: BST dispatch card_id; Gearfried Swordmaster path'),

    # === enqueue_zone_slot_sprite_attr_by_card_type -- player stride set ===
    (0x08043530, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'scan_equip_chain_list_stride',   None),
    (0x08043534, 0x0201c510, 'gDuelFieldSlots',              'scan_equip_chain_list_slots',    None),
    (0x08043538, 0x0201d9c0, 'gEquipNodePool',               'scan_equip_chain_list_nodepool', None),
    (0x0804353c, 0xffffeb50, 'NODE_POOL_NEG_OFFSET',         'scan_equip_chain_list_neg_off',  None),
    (0x08043540, 0x0201c520, 'gDuelFieldSlotState',          'scan_equip_chain_list_slotstate',None),

    # === scan_equip_chain_list_for_sprite_update (0x0804348c) card IDs ===
    (0x08043544, 0x0000169a, 'FALLING_DOWN_CID',             'scan_equip_chain_cid_falling_down',
     'FALLING_DOWN_CID=0x169a: BST branch node in scan_equip_chain_list_for_sprite_update'),
    (0x08043554, 0x00001466, 'DARK_NECROFEAR_CID',           'scan_equip_chain_cid_dark_necrofear',
     'DARK_NECROFEAR_CID=0x1466: BST branch node; Dark Necrofear equip spell path'),
    (0x0804358c, 0x00001877, 'BRAIN_JACKER_CID',             'scan_equip_chain_cid_brain_jacker',
     'BRAIN_JACKER_CID=0x1877: BST branch node; Brain Jacker equip spell path'),

    # === Sentinel values ===
    (0x0804343c, 0x0000ffff, 'SLOT_CARD_EMPTY',              'enqueue_equip_chain_pair_no_pair',
     'SLOT_CARD_EMPTY=0xffff: NO_PAIR sentinel (chain pair not found); same encoding as empty slot'),
    (0x080436dc, 0x0000ffff, 'SLOT_CARD_EMPTY',              'enqueue_equip_bitmap_type_d_no_node',
     'SLOT_CARD_EMPTY=0xffff: NO_NODE sentinel (chain node not found); same encoding as empty slot'),

    # === scan_equip_chain_list_by_player_slot (0x080435c4) ===
    (0x08043638, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'scan_equip_chain_by_slot_stride',None),
    (0x0804363c, 0x0201c510, 'gDuelFieldSlots',              'scan_equip_chain_by_slot_slots', None),
    (0x08043640, 0x0201d9c0, 'gEquipNodePool',               'scan_equip_chain_by_slot_pool',  None),

    # === enqueue_sprite_attrs_for_card_chain_list (0x08043644) ===
    (0x08043690, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'enqueue_sprite_attrs_chain_stride',None),
    (0x08043694, 0x0201c510, 'gDuelFieldSlots',              'enqueue_sprite_attrs_chain_slots', None),
    (0x08043698, 0x0201d9c0, 'gEquipNodePool',               'enqueue_sprite_attrs_chain_pool',  None),

    # === enqueue_slot_bitmap_type_d_for_equip (0x08043700) ===
    (0x080436e0, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'enqueue_slot_bitmap_type_d_stride',None),
    (0x080436e4, 0x0201c510, 'gDuelFieldSlots',              'enqueue_slot_bitmap_type_d_slots', None),

    # === enqueue_slot_sprite_by_state_and_type (0x08043714) ===
    (0x08043768, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'enqueue_slot_sprite_by_state_stride',None),
    (0x0804376c, 0x0201c510, 'gDuelFieldSlots',              'enqueue_slot_sprite_by_state_slots', None),
    (0x080438e4, 0x00008035, 'OAM_ZONE_CARD_SPRITE_P1',      'enqueue_slot_sprite_by_state_pal_p1',
     'OAM_ZONE_CARD_SPRITE_P1=0x8035: zone occupied card OAM attr0 P1 (bit15+0x35); 8 ROM refs'),

    # === enqueue_slot_sprite_attr_by_card_type_and_state (0x08043864) ===
    (0x080438c0, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'enqueue_slot_sprite_attr_stride', None),
    (0x080438c4, 0x0201c510, 'gDuelFieldSlots',              'enqueue_slot_sprite_attr_slots',  None),
    (0x080438c8, 0xfffffdff, 'OAM_SPRITE_ATTR_CLR_BIT9',     'enqueue_slot_sprite_attr_clr_bit9',
     'OAM_SPRITE_ATTR_CLR_BIT9=0xfffffdff: AND mask clears bit9 (player_side) of OAM sprite attr word; 480 ROM refs'),
    (0x080438cc, 0xffffc3ff, 'OAM_SPRITE_ATTR_CLR_BITS13_10','enqueue_slot_sprite_attr_clr_bits13_10',
     'OAM_SPRITE_ATTR_CLR_BITS13_10=0xffffc3ff: AND mask clears bits[13:10] (slot_idx field); 27 ROM refs'),
    (0x080438d0, 0xffffbfff, 'SLOT_ACTIVE_BIT14_CLR',        'enqueue_slot_sprite_attr_clr_bit14',
     'SLOT_ACTIVE_BIT14_CLR=0xffffbfff: AND mask clears bit14 (equip_head flag) of OAM sprite attr'),
    (0x080438d4, 0xffff7fff, 'SLOT_ACTIVE_BIT15_CLR',        'enqueue_slot_sprite_attr_clr_bit15',
     'SLOT_ACTIVE_BIT15_CLR=0xffff7fff: AND mask clears bit15 (extra_flag) of OAM sprite attr'),
    (0x080438d8, 0xfffffe00, 'OAM_ATTR1_X_CLEAR',            'enqueue_slot_sprite_attr_clr_bits8_0',
     'OAM_ATTR1_X_CLEAR=0xfffffe00: AND mask clears attr1 bits[8:0] (x-coordinate); oam_attr.inc:19'),
    (0x080438dc, 0xfffeffff, 'OAM_SPRITE_ATTR_CLR_BIT16',    'enqueue_slot_sprite_attr_clr_bit16',
     'OAM_SPRITE_ATTR_CLR_BIT16=0xfffeffff: AND mask clears bit16 (flip flag) of OAM sprite attr; 1475 ROM refs'),
    (0x080438e0, 0xfffdffff, 'OAM_SPRITE_ATTR_CLR_BIT17',    'enqueue_slot_sprite_attr_clr_bit17',
     'OAM_SPRITE_ATTR_CLR_BIT17=0xfffdffff: AND mask clears bit17 (composite sprite flag); 448 ROM refs'),

    # === enqueue_zone_slot_sprite_attr_if_occupied (0x08043900) ===
    (0x08043940, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'enqueue_zone_slot_if_occ_stride',None),
    (0x08043944, 0x0201c510, 'gDuelFieldSlots',              'enqueue_zone_slot_if_occ_slots', None),
    (0x08043948, 0x00008035, 'OAM_ZONE_CARD_SPRITE_P1',      'enqueue_zone_slot_if_occ_pal_p1',
     'OAM_ZONE_CARD_SPRITE_P1=0x8035: reuse; enqueue_zone_slot_sprite_attr_if_occupied P1 path'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: none in Seg-5
# ---------------------------------------------------------------------------
REF_SLOTS = []

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
#    Pure label rename (no equate needed)
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x08043388, 'enqueue_zone_slot_sprite_mask_cid_13ea',
     'slot_word<<19 test for card_id=0x13ea (unassigned slot gap); enqueue_zone_slot_sprite_attr_by_card_type'),
    (0x080433c0, 'enqueue_zone_slot_sprite_flags_gearfried',
     'bits[29,28,21] activation flags; ORed into apply_equip_activation_with_id_lookup arg2 for Gearfried(0x13c3)'),
    (0x08043548, 'scan_equip_chain_cid_13ea',
     'unassigned slot_id 0x13ea (gap between 0x13e8 Nuvia and 0x13eb Soul Exchange); BST branch only; med-conf'),
]

# ---------------------------------------------------------------------------
# D. PLATE_REWRITES:
#    Two modes:
#      'full'   -- full ASCII setComment (for functions with CJK plates)
#      'substr' -- substring replace (for functions with ASCII plates)
#
# Format: (func_addr, mode, old_or_none, new_text)
#   mode='full':   old_or_none=None, new_text=full ASCII plate
#   mode='substr': old_or_none=old_substring, new_text=replacement substring
# ---------------------------------------------------------------------------
PLATE_REWRITES = [

    # --- enqueue_sprite_attr_for_chain_node_check (0x080431f4) ---
    # CJK plate (asm:6885): full ASCII rewrite
    (0x080431f4, 'full', None,
     "Called by scan_equip_zone_for_super_rejuvenation_activation after confirming equip activation eligibility.\n"
     "Params: r0=player_id->r4, r1=slot_idx->r5, r2=chain_idx->r7, r3=type_flag->r6.\n"
     "Calls check_node_in_slot_chain(r4,r5,r7,r6). On hit: selects OAM attr0 by player_id\n"
     "(r4==0 -> 0x37, r4!=0 -> 0x8037=OAM_EQUIP_CHAIN_SPRITE_P1), packs r5/r6 bit-fields into\n"
     "r1/r2/r3, calls enqueue_sprite_attr_record to write sprite attr to OAM buffer.\n"
     "On miss: skips enqueue.\n"
     "Side effects: OAM sprite queue write via enqueue_sprite_attr_record.\n"
     "Constants: OAM_P0=0x37, OAM_P1=0x8037."),

    # --- enqueue_equip_zone_sprite_attr_by_player (0x080430e4) ---
    # substring replace: FUN_0806d4a4 -> setup_equip_slot_oam_if_hand_slot_eligible
    # (function entry 0x080430e4; proposal listed 0x08043100 which is a LAB_ branch target inside fn)
    (0x080430e4, 'substr', 'FUN_0806d4a4', 'setup_equip_slot_oam_if_hand_slot_eligible'),

    # --- enqueue_equip_chain_all_slots_for_pair (0x0804317c) ---
    # substring replace: FUN_08044e30 -> update_duel_field_slot_sprite_state
    # (function entry 0x0804317c; proposal listed 0x08043190 which is mid-code)
    (0x0804317c, 'substr', 'FUN_08044e30', 'update_duel_field_slot_sprite_state'),

    # --- enqueue_sprite_attr_for_chain_node_match (0x08043240) ---
    # 5 FUN_ tokens: do 5 separate passes
    (0x08043240, 'substr', 'FUN_08044e30',  'update_duel_field_slot_sprite_state'),
    (0x08043240, 'substr', 'FUN_080490b4',  'tick_duel_field_zone_sprite_update_pipeline'),
    (0x08043240, 'substr', 'FUN_08057138',  'enqueue_chain_node_sprite_for_equip_entry'),
    (0x08043240, 'substr', 'FUN_08067750',  'tick_equip_chain_banisher_sprite_state'),
    (0x08043240, 'substr', 'FUN_08076b1c',  'enqueue_equip_zone_sprite_with_neo_daedalus_and_chain'),

    # --- enqueue_equip_chain_sprite_by_side (0x08043274) ---
    # substring replace: FUN_0804348c -> scan_equip_chain_list_for_sprite_update
    (0x08043274, 'substr', 'FUN_0804348c', 'scan_equip_chain_list_for_sprite_update'),

    # --- enqueue_zone_slot_sprite_attr_by_card_type (0x080432bc) ---
    # CJK plate (asm:7001): full ASCII rewrite correcting 3 FUN_ references
    (0x080432bc, 'full', None,
     "Called by invoke_zone_slot_sprite_attr_for_equip_type (wrapper, fixed r3=0xa),\n"
     "enqueue_equip_chain_slot_sprite_with_pair_lookup, and update_equip_zone_sprite_by_state\n"
     "(case_3, r3=0xc); indeg>=8.\n"
     "Entry: unpacks r0=player_side->sp[0]; r1 packed(byte1=zone_row, byte0=player_bit);\n"
     "r2 packed(byte1=col, byte0=y_offset); r3=card_type->r10.\n"
     "card_type==0xa path: reads gDuelFieldSlots[zone_row][player_bit] slot word; tests\n"
     "lsls#0x13 vs 0x9f500000; on hit calls enqueue_sprite_attr_with_xy_split;\n"
     "always calls enqueue_equip_set_slot_sprite_by_zone_col(player,zone_row,0).\n"
     "After card_type==0xa: selects attr0=0x42/0x8042 by sp[0]; calls enqueue_sprite_attr_record.\n"
     "Reads second slot word lsrs#5/lsrs#1 for bit-filter; on hit BST dispatch card_id:\n"
     "0x13c3(Gearfried Iron Knight)->apply_equip_activation_with_id_lookup;\n"
     "0x186b(Gearfried Swordmaster)->set_field_slot_bit_with_sprite_update(r6,r7,4,1).\n"
     "Final: always calls submit_lp_bar_sprite_row_by_type(0x18,slot_packed).\n"
     "Side effects: OAM queue, equip set slot sprite, lp bar sprite row.\n"
     "Constants: gDuelFieldSlots=0x0201c510, OAM_DEFAULT=0x42, OAM_ALT=0x8042,\n"
     "card_type_equip_special=0xa, mask=0x9f500000, iron_knight=0x13c3, swordmaster=0x186b."),

    # --- scan_equip_chain_list_for_sprite_update (0x0804348c) ---
    # 2 FUN_ tokens
    (0x0804348c, 'substr', 'FUN_08043274', 'enqueue_equip_chain_sprite_by_side'),
    (0x0804348c, 'substr', 'FUN_08090218', 'dispatch_equip_field_scan_sequence'),

    # --- enqueue_equip_chain_attrs_for_slot_range (0x0804345c) ---
    # 2 FUN_ tokens
    (0x0804345c, 'substr', 'FUN_080435c4', 'scan_equip_chain_list_by_player_slot'),
    (0x0804345c, 'substr', 'FUN_0809bdfc', 'scan_equip_chain_slots_for_attr_enqueue'),

    # --- enqueue_sprite_attrs_for_card_chain_list (0x08043644) ---
    # substring replace: FUN_08044e30 -> update_duel_field_slot_sprite_state
    (0x08043644, 'substr', 'FUN_08044e30', 'update_duel_field_slot_sprite_state'),

    # --- scan_equip_chain_list_by_player_slot (0x080435c4) ---
    # substring replace: FUN_08042bd0 -> dispatch_equip_chain_slot_scan_by_player
    (0x080435c4, 'substr', 'FUN_08042bd0', 'dispatch_equip_chain_slot_scan_by_player'),
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

def _apply_plate_substr(func_addr, old_text, new_text):
    """Substring replacement in existing plate (for ASCII plates with stale FUN_ tokens)."""
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
    """Full plate replacement with pure ASCII text (for CJK plate rewrites)."""
    a = _addr(func_addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[WARN] plate_full 0x%08x: no code unit" % func_addr)
        return

    if DRY:
        preview = new_text[:60].replace('\n', ' ')
        print("[dry] PLATE_FULL 0x%08x: set new ASCII plate (%d chars): %s..." % (
            func_addr, len(new_text), preview))
        return

    cu.setComment(CodeUnit.PLATE_COMMENT, new_text)
    print("[PWR] 0x%08x: plate fully rewritten (%d chars)" % (func_addr, len(new_text)))

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF04Seg5Slots (DRY=%s) ===" % DRY)
    print("  file 04 Seg-5: 0x0804308c..0x0804394c, 19 fn, 48 slots")
    print("  EQ=%d  REF=%d  RENAME=%d  PLATE_entries=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATE_REWRITES)))

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    eq_ok = 0
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        _apply_eq(slot_addr, value, eq_name, slot_label, eol)
        eq_ok += 1
    print("  EQ done: %d" % eq_ok)

    # B. REF_SLOTS (none)
    print("\n--- B. REF_SLOTS (%d) ---" % len(REF_SLOTS))
    print("  REF done: 0")

    # C. RENAME_SLOTS
    print("\n--- C. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    ren_ok = 0
    for entry in RENAME_SLOTS:
        slot_addr, slot_label = entry[0], entry[1]
        eol = entry[2] if len(entry) > 2 else None
        _apply_rename(slot_addr, slot_label, eol)
        ren_ok += 1
    print("  RENAME done: %d" % ren_ok)

    # D. PLATE_REWRITES
    print("\n--- D. PLATE_REWRITES (%d entries) ---" % len(PLATE_REWRITES))
    plate_ok = 0
    for entry in PLATE_REWRITES:
        func_addr, mode = entry[0], entry[1]
        if mode == 'full':
            _apply_plate_full(func_addr, entry[3])
        elif mode == 'substr':
            _apply_plate_substr(func_addr, entry[2], entry[3])
        else:
            print("[ERR] unknown mode '%s' for 0x%08x" % (mode, func_addr))
        plate_ok += 1
    print("  PLATE done: %d entries" % plate_ok)

    print("\n=== RefineF04Seg5Slots DONE ===")
    print("  EQ=%d  REF=%d  RENAME=%d  PLATE_entries=%d (DRY=%s)" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATE_REWRITES), DRY))

main()
