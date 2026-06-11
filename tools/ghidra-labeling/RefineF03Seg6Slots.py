# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF03Seg6Slots.py -- file 03 Seg-6 (0x0803b3a8..0x0803bba4)
#   get_zone_slot_entity_ref_by_type .. check_field_spell_neo_daedalus_group_placeable
#   EQ=54, REF=37, RENAME=4, FUNC_RENAME=0, PLATE=5
#
# Sections:
#   A. EQ_SLOTS   -- data-equate
#       reuse: PLAYER_BLOCK_STRIDE(x29), EFFECT_ZONE_BITMASK_OFF(x2), PARASITE_PARACIDE_CID(x1)
#       new: 9 card CIDs in card_info.inc
#   B. REF_SLOTS  -- USER-label + DATA-ref (37 slots)
#   C. RENAME_SLOTS -- switch-table ptr labels (4 slots)
#   D. PLATE_FIXES -- 3 substring replacements + 2 full setPlateComment rewrites
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).

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
# Helpers
# ---------------------------------------------------------------------------

def _addr(val):
    return toAddr(val)

def _check(slot_addr, expected):
    """Verify ROM dword at slot_addr matches expected. Return True if OK."""
    addr = _addr(slot_addr)
    mem = currentProgram.getMemory()
    try:
        actual = mem.getInt(addr) & 0xffffffff
        if actual != (expected & 0xffffffff):
            print("WARN: slot 0x%08x expected 0x%08x got 0x%08x -- SKIP" % (slot_addr, expected & 0xffffffff, actual))
            return False
        return True
    except Exception as e:
        print("WARN: slot 0x%08x read error: %s" % (slot_addr, e))
        return False

def _eq(slot_addr, value, eq_name, slot_label, eol=None):
    """Create equate eq_name=value, reference from slot, label slot."""
    if not _check(slot_addr, value):
        return
    if DRY:
        print("DRY EQ: 0x%08x %s=%s sl=%s" % (slot_addr, eq_name, hex(value & 0xffffffff), slot_label))
        return
    addr = _addr(slot_addr)
    et = currentProgram.getEquateTable()
    eq = et.getEquate(eq_name)
    if eq is None:
        eq = et.createEquate(eq_name, value & 0xffffffff)
    eq.addReference(addr, 0)
    sm = currentProgram.getSymbolTable()
    sm.createLabel(addr, slot_label, SourceType.USER_DEFINED)
    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(addr)
        if cu:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

def _ref(slot_addr, target_addr, gas_label, slot_label, eol=None):
    """Create USER label at target, DATA ref from slot, label slot."""
    if DRY:
        print("DRY REF: 0x%08x -> 0x%08x gas=%s sl=%s" % (slot_addr, target_addr, gas_label, slot_label))
        return
    tgt = _addr(target_addr)
    sm = currentProgram.getSymbolTable()
    sm.createLabel(tgt, gas_label, SourceType.USER_DEFINED)
    rm = currentProgram.getReferenceManager()
    src = _addr(slot_addr)
    rm.addMemoryReference(src, tgt, RefType.DATA, SourceType.USER_DEFINED, 0)
    ref_list = rm.getReferencesFrom(src)
    for r in ref_list:
        if r.getToAddress().equals(tgt):
            rm.setPrimary(r, True)
    sm.createLabel(src, slot_label, SourceType.USER_DEFINED)
    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(src)
        if cu:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

def _rename(slot_addr, old_label, new_label, eol=None):
    """Rename existing label (or create new) at slot_addr."""
    if DRY:
        print("DRY RENAME: 0x%08x %s->%s" % (slot_addr, old_label, new_label))
        return
    addr = _addr(slot_addr)
    sm = currentProgram.getSymbolTable()
    syms = list(sm.getSymbols(addr))
    renamed = False
    for sym in syms:
        if sym.getName() == old_label:
            sym.setName(new_label, SourceType.USER_DEFINED)
            renamed = True
            break
    if not renamed:
        sm.createLabel(addr, new_label, SourceType.USER_DEFINED)
    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(addr)
        if cu:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

# ---------------------------------------------------------------------------
# A. EQ_SLOTS
# ---------------------------------------------------------------------------
# (slot_addr, value, eq_name, slot_label, eol_or_None)
EQ_SLOTS = [

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x868 (29 slots) ---
    (0x0803b3ec, 0x868, 'PLAYER_BLOCK_STRIDE', 'entity_ref_stride_a', None),
    (0x0803b408, 0x868, 'PLAYER_BLOCK_STRIDE', 'entity_ref_stride_b', None),
    (0x0803b424, 0x868, 'PLAYER_BLOCK_STRIDE', 'entity_ref_stride_c', None),
    (0x0803b440, 0x868, 'PLAYER_BLOCK_STRIDE', 'entity_ref_stride_d', None),
    (0x0803b45c, 0x868, 'PLAYER_BLOCK_STRIDE', 'entity_ref_stride_e', None),
    (0x0803b4a8, 0x868, 'PLAYER_BLOCK_STRIDE', 'entity_ref_stride_f', None),
    (0x0803b4f4, 0x868, 'PLAYER_BLOCK_STRIDE', 'card_ref_stride_a', None),
    (0x0803b510, 0x868, 'PLAYER_BLOCK_STRIDE', 'card_ref_stride_b', None),
    (0x0803b52c, 0x868, 'PLAYER_BLOCK_STRIDE', 'card_ref_stride_c', None),
    (0x0803b548, 0x868, 'PLAYER_BLOCK_STRIDE', 'card_ref_stride_d', None),
    (0x0803b564, 0x868, 'PLAYER_BLOCK_STRIDE', 'card_ref_stride_e', None),
    (0x0803b5b8, 0x868, 'PLAYER_BLOCK_STRIDE', 'card_ref_stride_f', None),
    (0x0803b610, 0x868, 'PLAYER_BLOCK_STRIDE', 'field6_stride_a', None),
    (0x0803b68c, 0x868, 'PLAYER_BLOCK_STRIDE', 'zone_attr_stride_a', None),
    (0x0803b6c0, 0x868, 'PLAYER_BLOCK_STRIDE', 'zone_attr_stride_b', None),
    (0x0803b730, 0x868, 'PLAYER_BLOCK_STRIDE', 'zone_attr_stride_c', None),
    (0x0803b77c, 0x868, 'PLAYER_BLOCK_STRIDE', 'field_word_stride_a', None),
    (0x0803b798, 0x868, 'PLAYER_BLOCK_STRIDE', 'field_word_stride_b', None),
    (0x0803b7b4, 0x868, 'PLAYER_BLOCK_STRIDE', 'field_word_stride_c', None),
    (0x0803b7d0, 0x868, 'PLAYER_BLOCK_STRIDE', 'field_word_stride_d', None),
    (0x0803b7ec, 0x868, 'PLAYER_BLOCK_STRIDE', 'field_word_stride_e', None),
    (0x0803b814, 0x868, 'PLAYER_BLOCK_STRIDE', 'field_word_stride_f', None),
    (0x0803b880, 0x868, 'PLAYER_BLOCK_STRIDE', 'player_state_bit_stride_a', None),
    (0x0803b8ac, 0x868, 'PLAYER_BLOCK_STRIDE', 'player_state_bit_stride_b', None),
    (0x0803b8e0, 0x868, 'PLAYER_BLOCK_STRIDE', 'field_slot_bit_stride_a', None),
    (0x0803b90c, 0x868, 'PLAYER_BLOCK_STRIDE', 'field_slot_bit_stride_b', None),
    (0x0803b95c, 0x868, 'PLAYER_BLOCK_STRIDE', 'lp_spell_threshold_stride_a', None),
    (0x0803ba74, 0x868, 'PLAYER_BLOCK_STRIDE', 'strict_placeable_stride_a', None),
    (0x0803baec, 0x868, 'PLAYER_BLOCK_STRIDE', 'last_warrior_stride_a', None),
    (0x0803bb60, 0x868, 'PLAYER_BLOCK_STRIDE', 'neo_daedalus_stride_a', None),

    # --- duel_field.inc: EFFECT_ZONE_BITMASK_OFF = 0x10d0 (2 slots) ---
    (0x0803b834, 0x10d0, 'EFFECT_ZONE_BITMASK_OFF', 'occupy_flag_bitmask_off_a', None),
    (0x0803b850, 0x10d0, 'EFFECT_ZONE_BITMASK_OFF', 'occupy_flag_bitmask_off_b', None),

    # --- card_info.inc: PARASITE_PARACIDE_CID = 0x12a1 (reuse, 1 slot) ---
    (0x0803b688, 0x12a1, 'PARASITE_PARACIDE_CID', 'zone_attr_paracide_cid',
     'Parasite Paracide (pw=27911549; card_0625 slot=0x12A1); zone case_f attr-select block'),

    # --- card_info.inc: NEW CID constants (9 new, multiple slots each) ---
    # CHAIN_ENERGY_CID = 0x132c (1 slot)
    (0x0803b954, 0x132c, 'CHAIN_ENERGY_CID', 'lp_spell_threshold_chain_energy_cid',
     'Chain Energy (pw=79323590; card_0723 slot=0x132C); LP-threshold gate'),

    # JUDGEMENT_OF_PHARAOH_CID = 0x1679 (5 slots)
    (0x0803b974, 0x1679, 'JUDGEMENT_OF_PHARAOH_CID', 'zone_no_field_spell_pharaoh_cid',
     'Judgement of Pharaoh (pw=55948544; card_1350 slot=0x1679); zone-b effect node check'),
    (0x0803b9e0, 0x1679, 'JUDGEMENT_OF_PHARAOH_CID', 'field_spell_group_pharaoh_cid_b',
     'Judgement of Pharaoh; field-spell group placement gate'),
    (0x0803ba84, 0x1679, 'JUDGEMENT_OF_PHARAOH_CID', 'field_spell_strict_pharaoh_cid',
     'Judgement of Pharaoh; strict placement gate'),
    (0x0803baf8, 0x1679, 'JUDGEMENT_OF_PHARAOH_CID', 'last_warrior_pharaoh_cid',
     'Judgement of Pharaoh; last warrior gate'),
    (0x0803bb70, 0x1679, 'JUDGEMENT_OF_PHARAOH_CID', 'neo_daedalus_pharaoh_cid',
     'Judgement of Pharaoh; neo daedalus gate'),

    # LIGHT_OF_INTERVENTION_CID = 0x135d (1 slot)
    (0x0803b9d8, 0x135d, 'LIGHT_OF_INTERVENTION_CID', 'field_spell_group_intervention_cid',
     'Light of Intervention (pw=62867251; card_0765 slot=0x135D); field-spell group gate'),

    # NON_AGGRESSION_AREA_CID = 0x15ad (3 slots)
    (0x0803b9dc, 0x15ad, 'NON_AGGRESSION_AREA_CID', 'field_spell_group_non_aggression_cid_a',
     'Non Aggression Area (pw=76848240; card_1198 slot=0x15AD); zone-b node block check'),
    (0x0803ba80, 0x15ad, 'NON_AGGRESSION_AREA_CID', 'field_spell_strict_non_aggression_cid',
     'Non Aggression Area; strict placement gate'),
    (0x0803bb6c, 0x15ad, 'NON_AGGRESSION_AREA_CID', 'neo_daedalus_non_aggression_cid',
     'Non Aggression Area; neo daedalus gate'),

    # LAVA_GOLEM_CID = 0x1578 (2 slots)
    (0x0803b9e4, 0x1578, 'LAVA_GOLEM_CID', 'field_spell_group_lava_golem_cid',
     'Lava Golem (pw=00102380; card_1152 slot=0x1578); slot-chain value check'),
    (0x0803ba88, 0x1578, 'LAVA_GOLEM_CID', 'field_spell_strict_lava_golem_cid',
     'Lava Golem; strict placement block'),

    # BOSS_RUSH_CID = 0x1972 (2 slots)
    (0x0803b9e8, 0x1972, 'BOSS_RUSH_CID', 'field_spell_group_boss_rush_cid',
     'Boss Rush (pw=66947414; card_1983 slot=0x1972); effect zone count gate'),
    (0x0803ba8c, 0x1972, 'BOSS_RUSH_CID', 'field_spell_strict_boss_rush_cid',
     'Boss Rush; strict placement block'),

    # JAM_BREEDING_MACHINE_CID = 0x13ff (3 slots)
    (0x0803ba78, 0x13ff, 'JAM_BREEDING_MACHINE_CID', 'field_spell_strict_jam_breeding_cid',
     'Jam Breeding Machine (pw=21770260; card_0874 slot=0x13FF); effect zone count gate'),
    (0x0803baf0, 0x13ff, 'JAM_BREEDING_MACHINE_CID', 'last_warrior_jam_breeding_cid',
     'Jam Breeding Machine; last warrior gate'),
    (0x0803bb98, 0x13ff, 'JAM_BREEDING_MACHINE_CID', 'neo_daedalus_group_jam_breeding_cid',
     'Jam Breeding Machine; neo daedalus group gate'),

    # LAST_WARRIOR_FROM_ANOTHER_PLANET_CID = 0x12b1 (3 slots)
    (0x0803ba7c, 0x12b1, 'LAST_WARRIOR_FROM_ANOTHER_PLANET_CID', 'field_spell_strict_last_warrior_cid',
     'The Last Warrior from Another Planet (pw=86099788; card_0634 slot=0x12B1); copy presence check'),
    (0x0803baf4, 0x12b1, 'LAST_WARRIOR_FROM_ANOTHER_PLANET_CID', 'last_warrior_self_cid',
     'Last Warrior from Another Planet; self-check copy count'),
    (0x0803bb68, 0x12b1, 'LAST_WARRIOR_FROM_ANOTHER_PLANET_CID', 'neo_daedalus_last_warrior_cid',
     'Last Warrior from Another Planet; neo daedalus gate'),

    # JOWGEN_THE_SPIRITUALIST_CID = 0x147f (1 slot)
    (0x0803bb64, 0x147f, 'JOWGEN_THE_SPIRITUALIST_CID', 'neo_daedalus_jowgen_cid',
     'Jowgen the Spiritualist (pw=41855169; card_0957 slot=0x147F); Neo Daedalus placement gate'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS
# ---------------------------------------------------------------------------
# (slot_addr, target_addr, gas_label, slot_label, eol_or_None)
REF_SLOTS = [
    # get_zone_slot_entity_ref_by_type (0x0803b3a8)
    (0x0803b3f0, 0x0201c880, 'gP1ChainZoneArray',       'entity_ref_chain_zone_base_a', None),
    (0x0803b40c, 0x0201c740, 'gP1SlotSetCodeArray',     'entity_ref_slot_code_base_a', None),
    (0x0803b428, 0x0201c8f8, 'gP1HandSlotArray',        'entity_ref_hand_slot_base_a', None),
    (0x0803b444, 0x0201cab0, 'gP1AltHandSlotArray',     'entity_ref_alt_hand_base_a', None),
    (0x0803b460, 0x0201c600, 'gP1FieldArrayCBase',      'entity_ref_field_c_base_a', None),
    (0x0803b484, 0x0201bc54, 'gDuelEffectChainSlots',   'entity_ref_effect_chain_base_a', None),
    (0x0803b4ac, 0x0201c510, 'gDuelFieldSlots',         'entity_ref_field_slots_a', None),

    # get_zone_slot_card_ref_by_type (0x0803b4b0)
    (0x0803b4f8, 0x0201c880, 'gP1ChainZoneArray',       'card_ref_chain_zone_base_a', None),
    (0x0803b514, 0x0201c740, 'gP1SlotSetCodeArray',     'card_ref_slot_code_base_a', None),
    (0x0803b530, 0x0201c8f8, 'gP1HandSlotArray',        'card_ref_hand_slot_base_a', None),
    (0x0803b54c, 0x0201cab0, 'gP1AltHandSlotArray',     'card_ref_alt_hand_base_a', None),
    (0x0803b568, 0x0201c600, 'gP1FieldArrayCBase',      'card_ref_field_c_base_a', None),
    (0x0803b58c, 0x0201bc54, 'gDuelEffectChainSlots',   'card_ref_effect_chain_base_a', None),
    (0x0803b5bc, 0x0201c510, 'gDuelFieldSlots',         'card_ref_field_slots_a', None),

    # get_zone_slot_field6_by_type (0x0803b5c0)
    (0x0803b5f0, 0x0201bc54, 'gDuelEffectChainSlots',   'field6_effect_chain_base_a', None),
    (0x0803b614, 0x0201c510, 'gDuelFieldSlots',         'field6_field_slots_a', None),

    # get_zone_card_attribute_by_type (0x0803b618)
    (0x0803b690, 0x0201c740, 'gP1SlotSetCodeArray',     'zone_attr_slot_code_base_a', None),
    (0x0803b6bc, 0x0201c4e0, 'gP1LifePoints',           'zone_attr_lp_base_a', None),
    (0x0803b6ec, 0x0201e2a0, 'gDuelCardCtxBase',        'zone_attr_card_ctx_a', None),
    (0x0803b710, 0x0201bc54, 'gDuelEffectChainSlots',   'zone_attr_effect_chain_a', None),
    (0x0803b734, 0x0201c510, 'gDuelFieldSlots',         'zone_attr_field_slots_a', None),

    # read_player_field_slot_word_by_zone (0x0803b738)
    (0x0803b778, 0x0201c4e0, 'gP1LifePoints',           'field_word_lp_base_c', None),
    (0x0803b794, 0x0201c4e0, 'gP1LifePoints',           'field_word_lp_base_d', None),
    (0x0803b7b0, 0x0201c4e0, 'gP1LifePoints',           'field_word_lp_base_e', None),
    (0x0803b7cc, 0x0201c4e0, 'gP1LifePoints',           'field_word_lp_base_f', None),
    (0x0803b7e8, 0x0201c4e0, 'gP1LifePoints',           'field_word_lp_base_b', None),
    (0x0803b818, 0x0201c510, 'gDuelFieldSlots',         'field_word_field_slots_a', None),

    # write_slot_occupy_flag_bit (0x0803b81c)
    (0x0803b830, 0x0201c4e0, 'gP1LifePoints',           'occupy_flag_lp_base_a', None),
    (0x0803b84c, 0x0201c4e0, 'gP1LifePoints',           'occupy_flag_lp_base_b', None),

    # set_player_state_bit (0x0803b854)
    (0x0803b87c, 0x0201c4e0, 'gP1LifePoints',           'player_state_bit_lp_a', None),
    (0x0803b8a8, 0x0201c4e0, 'gP1LifePoints',           'player_state_bit_lp_b', None),

    # write_field_slot_bit_by_player (0x0803b8b0)
    (0x0803b8dc, 0x0201c4e0, 'gP1LifePoints',           'field_slot_bit_lp_a', None),
    (0x0803b908, 0x0201c4e0, 'gP1LifePoints',           'field_slot_bit_lp_b', None),

    # check_lp_exceeds_spell_copy_threshold (0x0803b910)
    (0x0803b958, 0x0201c4e0, 'gP1LifePoints',           'lp_spell_threshold_lp_a', None),

    # check_field_spell_card_placeable_strict (0x0803b9f4)
    (0x0803ba70, 0x0201c4e0, 'gP1LifePoints',           'strict_placeable_lp_a', None),

    # check_field_spell_last_warrior_placeable (0x0803ba98)
    (0x0803bae8, 0x0201c4e0, 'gP1LifePoints',           'last_warrior_lp_a', None),

    # check_field_spell_neo_daedalus_placeable (0x0803bb04)
    (0x0803bb5c, 0x0201c4e0, 'gP1LifePoints',           'neo_daedalus_lp_a', None),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS
# ---------------------------------------------------------------------------
# (slot_addr, old_label, new_label, eol)
RENAME_SLOTS = [
    (0x0803b3c0, 'DAT_0803b3c0', 'entity_ref_switch_table_ptr',
     'switch base ptr for get_zone_slot_entity_ref_by_type; points to 0x0803b3c4'),
    (0x0803b4c8, 'DAT_0803b4c8', 'card_ref_switch_table_ptr',
     'switch base ptr for get_zone_slot_card_ref_by_type; points to 0x0803b4cc'),
    (0x0803b634, 'DAT_0803b634', 'zone_attr_switch_table_ptr',
     'switch base ptr for get_zone_card_attribute_by_type; points to 0x0803b638'),
    (0x0803b74c, 'DAT_0803b74c', 'field_word_switch_table_ptr',
     'switch base ptr for read_player_field_slot_word_by_zone; points to 0x0803b750'),
]

# ---------------------------------------------------------------------------
# D. PLATE_FIXES
# ---------------------------------------------------------------------------

def _get_plate(addr_int):
    cu = currentProgram.getListing().getCodeUnitAt(_addr(addr_int))
    if cu is None:
        return None
    return cu.getComment(CodeUnit.PLATE_COMMENT)

def _set_plate(addr_int, text):
    cu = currentProgram.getListing().getCodeUnitAt(_addr(addr_int))
    if cu is None:
        print("WARN: no code unit at 0x%08x for plate" % addr_int)
        return False
    cu.setComment(CodeUnit.PLATE_COMMENT, text)
    return True

def apply_plate_fixes():
    # Fix 1: get_zone_slot_card_ref_by_type @ 0x0803b4b0
    # substring: "FUN_0803b5c0" -> "get_zone_slot_field6_by_type"
    addr = 0x0803b4b0
    old_text = _get_plate(addr)
    if old_text is None:
        print("WARN: no plate at get_zone_slot_card_ref_by_type (0x0803b4b0)")
    elif "FUN_0803b5c0" in old_text:
        new_text = old_text.replace("FUN_0803b5c0", "get_zone_slot_field6_by_type")
        if DRY:
            print("DRY PLATE fix1: 0x%08x FUN_0803b5c0->get_zone_slot_field6_by_type" % addr)
        else:
            _set_plate(addr, new_text)
            print("PLATE fix1 ok: 0x%08x replaced FUN_0803b5c0" % addr)
    else:
        print("PLATE fix1: FUN_0803b5c0 not found in plate at 0x%08x (already fixed?)" % addr)

    # Fix 2: write_slot_occupy_flag_bit @ 0x0803b81c
    # substring: "FUN_08040144" -> "tick_hand_sort_display_init_seq"
    addr = 0x0803b81c
    old_text = _get_plate(addr)
    if old_text is None:
        print("WARN: no plate at write_slot_occupy_flag_bit (0x0803b81c)")
    elif "FUN_08040144" in old_text:
        new_text = old_text.replace("FUN_08040144", "tick_hand_sort_display_init_seq")
        if DRY:
            print("DRY PLATE fix2: 0x%08x FUN_08040144->tick_hand_sort_display_init_seq" % addr)
        else:
            _set_plate(addr, new_text)
            print("PLATE fix2 ok: 0x%08x replaced FUN_08040144" % addr)
    else:
        print("PLATE fix2: FUN_08040144 not found in plate at 0x%08x (already fixed?)" % addr)

    # Fix 3: check_lp_exceeds_spell_copy_threshold @ 0x0803b910
    # substring: "scale=132" -> "scale=500"
    addr = 0x0803b910
    old_text = _get_plate(addr)
    if old_text is None:
        print("WARN: no plate at check_lp_exceeds_spell_copy_threshold (0x0803b910)")
    elif "scale=132" in old_text:
        new_text = old_text.replace("scale=132", "scale=500")
        if DRY:
            print("DRY PLATE fix3: 0x%08x scale=132->scale=500" % addr)
        else:
            _set_plate(addr, new_text)
            print("PLATE fix3 ok: 0x%08x replaced scale=132->scale=500" % addr)
    else:
        print("PLATE fix3: scale=132 not found in plate at 0x%08x (already fixed?)" % addr)

    # Fix 4: get_zone_slot_entity_ref_by_type @ 0x0803b3a8
    # Full setPlateComment rewrite (CJK->ASCII)
    addr = 0x0803b3a8
    ascii_plate = (
        "Reads the entity_ref field from a zone slot selected by zone_type_code (r1) via switch-dispatch. "
        "Switch covers type_code 0xb..0xf (5 cases) plus default (two paths: r1+r2<=10 / >10). "
        "Symmetric sibling of get_zone_slot_card_ref_by_type (0x0803b4b0): both return [slot+0], "
        "but this function extracts bits[22..16]<<1 | bit[13] (entity/player reference bits) via lsls/lsrs. "
        "Params: r0=zone_idx, r1=zone_type_code, r2=slot_idx, r3=player_id (bit0). "
        "Bases: gDuelFieldSlots(0x0201c510)/gP1FieldArrayCBase(0x0201c600)/gP1ChainZoneArray(0x0201c880)/ "
        "       gP1SlotSetCodeArray(0x0201c740)/gP1HandSlotArray(0x0201c8f8)/gP1AltHandSlotArray(0x0201cab0)/ "
        "       gDuelEffectChainSlots(0x0201bc54). indeg=11. Constants: player_stride=0x868."
    )
    if DRY:
        print("DRY PLATE fix4: 0x%08x full rewrite CJK->ASCII (%d chars)" % (addr, len(ascii_plate)))
    else:
        _set_plate(addr, ascii_plate)
        print("PLATE fix4 ok: 0x%08x CJK->ASCII rewrite" % addr)

    # Fix 5: set_player_state_bit @ 0x0803b854
    # Full setPlateComment rewrite (CJK->ASCII)
    addr = 0x0803b854
    ascii_plate = (
        "Single-bit OR (set) or BIC (clear) on [gP1LifePoints + player&1 * 0x868 + 0x11c]. "
        "Params: r0=player_id, r1=bit_pos [0..31], r2=set_flag (0=clear, nonzero=set). "
        "r2!=0: computes 1<<bit_pos then OR to target word; r2==0: BIC clears bit. "
        "Returns void. Sibling of write_field_slot_bit_by_player (0x0803b8b0, operates on slot-level +0x40). "
        "indeg=4; called by set_player_state_bit_with_sprite_update and equip activation path. "
        "Side effects: [gP1LifePoints + player&1 * 0x868 + 0x11c] bit_pos OR/BIC. "
        "Constants: flags_offset=0x11c (0x8e*2), player_stride=0x868."
    )
    if DRY:
        print("DRY PLATE fix5: 0x%08x full rewrite CJK->ASCII (%d chars)" % (addr, len(ascii_plate)))
    else:
        _set_plate(addr, ascii_plate)
        print("PLATE fix5 ok: 0x%08x CJK->ASCII rewrite" % addr)


# ---------------------------------------------------------------------------
# Execute
# ---------------------------------------------------------------------------

print("=== RefineF03Seg6Slots.py DRY=%s ===" % DRY)

for (sa, val, eqn, sl, eol) in EQ_SLOTS:
    _eq(sa, val, eqn, sl, eol)

print("EQ done: %d slots" % len(EQ_SLOTS))

for (sa, ta, gl, sl, eol) in REF_SLOTS:
    _ref(sa, ta, gl, sl, eol)

print("REF done: %d slots" % len(REF_SLOTS))

for (sa, ol, nl, eol) in RENAME_SLOTS:
    _rename(sa, ol, nl, eol)

print("RENAME done: %d slots" % len(RENAME_SLOTS))

apply_plate_fixes()
print("PLATE done: 5 fixes")

print("=== COMPLETE: EQ=%d REF=%d RENAME=%d PLATE=5 DRY=%s ===" % (
    len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), DRY))
