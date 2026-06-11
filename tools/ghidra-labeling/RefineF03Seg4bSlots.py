# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF03Seg4bSlots.py -- file 03 Seg-4b (0x08037ec0..0x0803a7f0)
#   eval_slot_score_entry_full + dispatch_equip_node_by_type cluster + equip chain rule
#   EQ=~108, REF=~22, RENAME=~26, FUNC_RENAME=0, PLATE=15
#
# Sections:
#   A. EQ_SLOTS   -- data-equate (CID constants + numeric offsets)
#   B. REF_SLOTS  -- USER-label + DATA-ref (globals + fn-ptrs + carve labels)
#   C. RENAME_SLOTS -- pure rename + EOL
#   D. PLATE_FULL -- full plate rewrite (15 functions, pure ASCII, no FUN_/CJK)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).
# NOTE: DAT_080384d0 = 0x1755 = Goblin King (NOT Solar Flare Dragon 0x1756).
#   New constant GOBLIN_KING_CID added.

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
    # label the target
    tgt = _addr(target_addr)
    sm = currentProgram.getSymbolTable()
    sm.createLabel(tgt, gas_label, SourceType.USER_DEFINED)
    # DATA ref
    rm = currentProgram.getReferenceManager()
    src = _addr(slot_addr)
    rm.addMemoryReference(src, tgt, RefType.DATA, SourceType.USER_DEFINED, 0)
    ref_list = rm.getReferencesFrom(src)
    for r in ref_list:
        if r.getToAddress().equals(tgt):
            rm.setPrimary(r, True)
    # label the slot
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

def _plate(func_addr, text):
    """Set plate (pre) comment for function at func_addr (ASCII only)."""
    if DRY:
        print("DRY PLATE: 0x%08x len=%d" % (func_addr, len(text)))
        return
    addr = _addr(func_addr)
    cu = currentProgram.getListing().getCodeUnitAt(addr)
    if cu is None:
        print("WARN: no code unit at 0x%08x for plate" % func_addr)
        return
    cu.setComment(CodeUnit.PLATE_COMMENT, text)

# ---------------------------------------------------------------------------
# A. EQ_SLOTS
# ---------------------------------------------------------------------------
# (slot_addr, value, eq_name, slot_label, eol_or_None)
EQ_SLOTS = [

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x868 ---
    (0x08038034, 0x868, 'PLAYER_BLOCK_STRIDE', 'eval_slot_score_entry_full_stride_a', None),
    (0x08038190, 0x868, 'PLAYER_BLOCK_STRIDE', 'eval_slot_lp_cost_stride_a', None),
    (0x080382ac, 0x868, 'PLAYER_BLOCK_STRIDE', 'eval_slot_lp_cost_stride_b', None),
    (0x08038754, 0x868, 'PLAYER_BLOCK_STRIDE', 'eval_hand_magicians_stride', None),
    (0x080387bc, 0x868, 'PLAYER_BLOCK_STRIDE', 'eval_slot_bonus_stride_a', None),
    (0x08038898, 0x868, 'PLAYER_BLOCK_STRIDE', 'eval_lp_cost_zone_stride_a', None),
    (0x080388fc, 0x868, 'PLAYER_BLOCK_STRIDE', 'eval_lp_cost_zone_stride_b', None),
    (0x08038a40, 0x868, 'PLAYER_BLOCK_STRIDE', 'eval_monster_zone_stride_a', None),
    (0x08038aac, 0x868, 'PLAYER_BLOCK_STRIDE', 'eval_sanctuary_stride', None),
    (0x08038c7c, 0x868, 'PLAYER_BLOCK_STRIDE', 'eval_hand_field6_stride', None),
    (0x08038dd0, 0x868, 'PLAYER_BLOCK_STRIDE', 'eval_extra_deck_stride', None),
    (0x08039124, 0x868, 'PLAYER_BLOCK_STRIDE', 'eval_bonus_state_stride_a', None),
    (0x08039260, 0x868, 'PLAYER_BLOCK_STRIDE', 'adjust_score_chain_stride', None),
    (0x0803930c, 0x868, 'PLAYER_BLOCK_STRIDE', 'dispatch_equip_node_stride', None),
    (0x0803a59c, 0x868, 'PLAYER_BLOCK_STRIDE', 'check_equip_chain_stride_a', None),
    (0x0803a64c, 0x868, 'PLAYER_BLOCK_STRIDE', 'classify_equip_stride_a', None),
    (0x0803a6c4, 0x868, 'PLAYER_BLOCK_STRIDE', 'classify_equip_stride_b', None),
    (0x0803a704, 0x868, 'PLAYER_BLOCK_STRIDE', 'classify_equip_stride_c', None),
    (0x0803a74c, 0x868, 'PLAYER_BLOCK_STRIDE', 'build_elig_table_stride', None),
    (0x0803a7bc, 0x868, 'PLAYER_BLOCK_STRIDE', 'build_elig_table_stride_b', None),

    # --- duel_field.inc: EQUIP_NODE_BASE_OFFSET = 0x14b0 ---
    (0x080382b4, 0x14b0, 'EQUIP_NODE_BASE_OFFSET', 'eval_equip_pool_base_off', None),
    (0x0803a6cc, 0x14b0, 'EQUIP_NODE_BASE_OFFSET', 'classify_equip_node_base_off', None),

    # --- duel_field.inc: DUEL_ACTIVE_PLAYER_OFF = 0x1cb8 ---
    (0x08038968, 0x1cb8, 'DUEL_ACTIVE_PLAYER_OFF', 'eval_active_player_off_a', None),
    (0x08039194, 0x1cb8, 'DUEL_ACTIVE_PLAYER_OFF', 'eval_active_player_off_b', None),

    # --- duel_field.inc: PUZZLE_LP_STEP_1000 = 0xfffffc18 ---
    (0x0803884c, 0xfffffc18, 'PUZZLE_LP_STEP_1000', 'eval_lp_step_neg1000', None),

    # --- ewram.inc: P1LP_BLOCK2_OFF_1CE8 = 0x1ce8 ---
    (0x0803893c, 0x1ce8, 'P1LP_BLOCK2_OFF_1CE8', 'eval_p1lp_block2_off_a', None),
    (0x08039140, 0x1ce8, 'P1LP_BLOCK2_OFF_1CE8', 'eval_p1lp_block2_off_b', None),

    # --- card_info.inc: GRADIUS_OPTION_CID = 0x14fc (reuse) ---
    (0x080383a0, 0x14fc, 'GRADIUS_OPTION_CID', 'eval_gradius_option_cid', None),

    # --- card_info.inc: AMAZONESS_TIGER_CID = 0x160f (reuse) ---
    (0x08038434, 0x160f, 'AMAZONESS_TIGER_CID', 'eval_amazoness_tiger_cid', None),

    # --- card_info.inc: SOLAR_FLARE_DRAGON_CID = 0x1756 (reuse) ---
    # NOTE: 0x1755 = GOBLIN_KING_CID (new), NOT Solar Flare Dragon
    (0x080384d0, 0x1755, 'GOBLIN_KING_CID', 'eval_goblin_king_cid', None),

    # --- duel_field.inc: new --- LP_COST_3000 = 0x0bb8 ---
    (0x080380d8, 0x0bb8, 'LP_COST_3000', 'eval_lp_cost_3000_a', None),
    (0x08038bf4, 0x0bb8, 'LP_COST_3000', 'eval_lp_cost_3000_b', None),
    (0x08038e6c, 0x0bb8, 'LP_COST_3000', 'eval_lp_cost_3000_c', None),

    # --- duel_field.inc: new LP_COST_1500 = 0x05dc ---
    (0x08038b38, 0x05dc, 'LP_COST_1500', 'eval_lp_cost_1500', None),

    # --- duel_field.inc: new SCORE_DELTA_NEG_300 = 0xfffffed4 ---
    (0x0803919c, 0xfffffed4, 'SCORE_DELTA_NEG_300', 'eval_score_delta_neg300_a', None),
    (0x080391b8, 0xfffffed4, 'SCORE_DELTA_NEG_300', 'eval_score_delta_neg300_b', None),

    # --- duel_field.inc: new SCORE_DELTA_NEG_500 = 0xfffffe0c ---
    (0x080391d4, 0xfffffe0c, 'SCORE_DELTA_NEG_500', 'eval_score_delta_neg500', None),

    # --- duel_field.inc: new SCORE_DELTA_NEG_700 = 0xfffffd44 ---
    (0x08039258, 0xfffffd44, 'SCORE_DELTA_NEG_700', 'eval_score_delta_neg700', None),

    # --- ewram.inc: new HAND_COUNT_TO_SLOT_OFF = 0x0404 ---
    (0x08038760, 0x0404, 'HAND_COUNT_TO_SLOT_OFF', 'eval_hand_count_to_slot_off',
     '0x404: gP1HandCountBase to gP1HandSlotArray offset'),

    # --- card_info.inc: new SLOT_CARD_EMPTY = 0xffff ---
    (0x080389a8, 0xffff, 'SLOT_CARD_EMPTY', 'eval_slot_empty_sentinel',
     '0xffff: no-card sentinel'),

    # --- duel_field.inc: new FIELD_STATE_OFF = 0x1cf4 ---
    (0x08038940, 0x1cf4, 'FIELD_STATE_OFF', 'eval_field_state_off_a', None),
    (0x08039144, 0x1cf4, 'FIELD_STATE_OFF', 'eval_field_state_off_b', None),

    # --- duel_field.inc: new CHAIN_LINK_COUNTER_OFF = 0x1cbc ---
    (0x080386f0, 0x1cbc, 'CHAIN_LINK_COUNTER_OFF', 'eval_chain_link_counter_off', None),

    # --- duel_field.inc: new EQUIP_PHASE_STATE_OFF = 0x1cc4 ---
    (0x0803896c, 0x1cc4, 'EQUIP_PHASE_STATE_OFF', 'eval_equip_phase_state_off', None),

    # -------------------------------------------------------------------------
    # card_info.inc: CID slots (new constants)
    # -------------------------------------------------------------------------

    # MACHINE_KING_CID = 0x113d
    (0x080382f8, 0x113d, 'MACHINE_KING_CID', 'eval_machine_king_cid', None),

    # MAHA_VAILO_CID = 0x1193
    (0x08038308, 0x1193, 'MAHA_VAILO_CID', 'eval_maha_vailo_cid', None),

    # MUKA_MUKA_CID = 0x11aa
    (0x080382c8, 0x11aa, 'MUKA_MUKA_CID', 'eval_muka_muka_cid', None),

    # REVERSE_TRAP_CID = 0x1257
    (0x08038044, 0x1257, 'REVERSE_TRAP_CID', 'eval_reverse_trap_cid', None),

    # MAGICIAN_OF_BLACK_CHAOS_CID = 0x1278
    (0x0803875c, 0x1278, 'MAGICIAN_OF_BLACK_CHAOS_CID', 'eval_magician_black_chaos_cid', None),

    # DARK_MAGICIAN_GIRL_CID = 0x129e
    (0x08038338, 0x129e, 'DARK_MAGICIAN_GIRL_CID', 'eval_dark_magician_girl_cid', None),

    # SHIELD_AND_SWORD_CID = 0x12cb
    (0x080382b8, 0x12cb, 'SHIELD_AND_SWORD_CID', 'eval_shield_and_sword_cid', None),

    # FLASH_ASSAILANT_CID = 0x1336
    (0x08038354, 0x1336, 'FLASH_ASSAILANT_CID', 'eval_flash_assailant_cid', None),

    # SLATE_WARRIOR_CID = 0x13ad
    (0x080383b4, 0x13ad, 'SLATE_WARRIOR_CID', 'eval_slate_warrior_cid', None),

    # NUVIA_THE_WICKED_CID = 0x13e8
    (0x080383a4, 0x13e8, 'NUVIA_THE_WICKED_CID', 'eval_nuvia_the_wicked_cid', None),

    # LIGHTNING_BLADE_CID = 0x13f6
    (0x08039130, 0x13f6, 'LIGHTNING_BLADE_CID', 'eval_lightning_blade_cid', None),

    # YELLOW_LUSTER_SHIELD_CID = 0x1429
    (0x08039138, 0x1429, 'YELLOW_LUSTER_SHIELD_CID', 'eval_yellow_luster_shield_cid', None),

    # DARK_MAGICIAN_CID_142D = 0x142d
    (0x08038784, 0x142d, 'DARK_MAGICIAN_CID_142D', 'eval_dark_magician_142d_cid', None),

    # EMBODIMENT_OF_APOPHIS_CID = 0x1472 (two slots)
    (0x08038050, 0x1472, 'EMBODIMENT_OF_APOPHIS_CID', 'eval_embodiment_apophis_cid_a', None),
    (0x08038be4, 0x1472, 'EMBODIMENT_OF_APOPHIS_CID', 'eval_embodiment_apophis_cid_b', None),

    # SOUL_OF_PURITY_CID = 0x1483
    (0x08039158, 0x1483, 'SOUL_OF_PURITY_CID', 'eval_soul_of_purity_cid', None),

    # ROCK_SPIRIT_CID = 0x1486
    (0x080383d0, 0x1486, 'ROCK_SPIRIT_CID', 'eval_rock_spirit_cid', None),

    # THE_A_FORCES_CID = 0x14cf
    (0x08038f10, 0x14cf, 'THE_A_FORCES_CID', 'eval_the_a_forces_cid', None),

    # MUDORA_CID = 0x14ec
    (0x080383e0, 0x14ec, 'MUDORA_CID', 'eval_mudora_cid', None),

    # MASTER_OF_DRAGON_SOLDIER_CID = 0x157d
    (0x08038418, 0x157d, 'MASTER_OF_DRAGON_SOLDIER_CID', 'eval_master_dragon_soldier_cid', None),

    # BANNER_OF_COURAGE_CID = 0x15a2
    (0x08039148, 0x15a2, 'BANNER_OF_COURAGE_CID', 'eval_banner_of_courage_cid', None),

    # DARK_PALADIN_CID = 0x15fc
    (0x08038408, 0x15fc, 'DARK_PALADIN_CID', 'eval_dark_paladin_cid', None),

    # MAGICAL_MARIONETTE_CID = 0x1615
    (0x0803844c, 0x1615, 'MAGICAL_MARIONETTE_CID', 'eval_magical_marionette_cid', None),

    # METAL_REFLECT_SLIME_CID = 0x1636
    (0x08038054, 0x1636, 'METAL_REFLECT_SLIME_CID', 'eval_metal_reflect_slime_cid', None),

    # GYAKU_GIRE_PANDA_CID = 0x1651
    (0x080382c0, 0x1651, 'GYAKU_GIRE_PANDA_CID', 'eval_gyaku_gire_panda_cid', None),

    # NIGHTMARE_PENGUIN_CID = 0x16ab
    (0x08039134, 0x16ab, 'NIGHTMARE_PENGUIN_CID', 'eval_nightmare_penguin_cid', None),

    # PERFECT_MACHINE_KING_CID = 0x16ac
    (0x080384a4, 0x16ac, 'PERFECT_MACHINE_KING_CID', 'eval_perfect_machine_king_cid', None),

    # SKULL_ZOMA_CID = 0x172f
    (0x0803804c, 0x172f, 'SKULL_ZOMA_CID', 'eval_skull_zoma_cid', None),

    # AGENT_OF_FORCE_MARS_CID = 0x1742
    (0x080384c0, 0x1742, 'AGENT_OF_FORCE_MARS_CID', 'eval_agent_force_mars_cid', None),

    # UNHAPPY_GIRL_CID = 0x1743
    (0x0803a724, 0x1743, 'UNHAPPY_GIRL_CID', 'classify_unhappy_girl_cid', None),

    # MOKEY_MOKEY_CID = 0x1782
    (0x08038e64, 0x1782, 'MOKEY_MOKEY_CID', 'eval_mokey_mokey_cid', None),

    # THEBAN_NIGHTMARE_CID = 0x1789
    (0x08038494, 0x1789, 'THEBAN_NIGHTMARE_CID', 'eval_theban_nightmare_cid', None),

    # ELEMENT_DRAGON_CID = 0x17e3
    (0x08038500, 0x17e3, 'ELEMENT_DRAGON_CID', 'eval_element_dragon_cid', None),

    # ENRAGED_MUKA_MUKA_CID = 0x17eb
    (0x080384f8, 0x17eb, 'ENRAGED_MUKA_MUKA_CID', 'eval_enraged_muka_muka_cid', None),

    # GREEN_GADGET_CID = 0x1807
    (0x08038be8, 0x1807, 'GREEN_GADGET_CID', 'eval_green_gadget_cid', None),

    # STRONGHOLD_CID = 0x1809
    (0x08038068, 0x1809, 'STRONGHOLD_CID', 'eval_stronghold_cid', None),

    # RED_GADGET_CID = 0x180b
    (0x08038bec, 0x180b, 'RED_GADGET_CID', 'eval_red_gadget_cid', None),

    # YELLOW_GADGET_CID = 0x180c
    (0x08038bf0, 0x180c, 'YELLOW_GADGET_CID', 'eval_yellow_gadget_cid', None),

    # SILENT_MAGICIAN_LV4_CID = 0x1817
    (0x0803851c, 0x1817, 'SILENT_MAGICIAN_LV4_CID', 'eval_silent_magician_lv4_cid', None),

    # ULTIMATE_INSECT_LV3_CID = 0x1822
    (0x08039154, 0x1822, 'ULTIMATE_INSECT_LV3_CID', 'eval_ultimate_insect_lv3_cid', None),

    # ELEMENT_SAURUS_CID = 0x1827
    (0x08038534, 0x1827, 'ELEMENT_SAURUS_CID', 'eval_element_saurus_cid', None),

    # MOKEY_MOKEY_SMACKDOWN_CID = 0x1843
    (0x08038e68, 0x1843, 'MOKEY_MOKEY_SMACKDOWN_CID', 'eval_mokey_mokey_smackdown_cid', None),

    # BEHEMOTH_KING_CID = 0x1864
    (0x08038048, 0x1864, 'BEHEMOTH_KING_CID', 'eval_behemoth_king_cid', None),

    # ULTIMATE_INSECT_LV5_CID = 0x185e
    (0x0803916c, 0x185e, 'ULTIMATE_INSECT_LV5_CID', 'eval_ultimate_insect_lv5_cid', None),

    # RED_EYES_DARKNESS_DRAGON_CID = 0x1894
    (0x08038490, 0x1894, 'RED_EYES_DARKNESS_DRAGON_CID', 'eval_red_eyes_darkness_dragon_cid', None),

    # KING_OF_SKULL_SERVANTS_CID = 0x18c5
    (0x08038080, 0x18c5, 'KING_OF_SKULL_SERVANTS_CID', 'eval_king_skull_servants_cid', None),

    # DORIADO_CID = 0x18c7 (Elemental Mistress Doriado)
    (0x0803803c, 0x18c7, 'DORIADO_CID', 'eval_doriado_cid', None),

    # BATTERYMAN_AA_CID = 0x18c3
    # (used via shifted sentinel DAT_08038c84, raw CID not a separate slot here)

    # DARK_DREADROUTE_CID = 0x1905
    (0x0803a53c, 0x1905, 'DARK_DREADROUTE_CID', 'check_equip_chain_dark_dreadroute_cid', None),

    # TADPOLE_CID = 0x1919
    (0x08038d18, 0x1919, 'TADPOLE_CID', 'eval_tadpole_cid', None),

    # TYRANNO_INFINITY_CID = 0x191b
    (0x08038098, 0x191b, 'TYRANNO_INFINITY_CID', 'eval_tyranno_infinity_cid', None),

    # BATTERYMAN_C_CID = 0x191c (raw CID -- shifted sentinel is separate RENAME slot)
    # No raw slot for 0x191c -- it appears only as shifted

    # EHERO_SHINING_FLARE_WINGMAN_CID = 0x1943
    (0x0803857c, 0x1943, 'EHERO_SHINING_FLARE_WINGMAN_CID', 'eval_ehero_shining_flare_wingman_cid', None),

    # WATER_DRAGON_CID = 0x1951
    (0x0803a530, 0x1951, 'WATER_DRAGON_CID', 'check_equip_chain_water_dragon_cid', None),

    # CYBER_BLADER_CID = 0x1955
    (0x0803a534, 0x1955, 'CYBER_BLADER_CID', 'check_equip_chain_cyber_blader_cid', None),

    # MACHINE_KING_PROTOTYPE_CID = 0x19be
    (0x08038598, 0x19be, 'MACHINE_KING_PROTOTYPE_CID', 'eval_machine_king_prototype_cid', None),

    # ANCIENT_GEAR_CASTLE_CID = 0x19b2
    (0x08039150, 0x19b2, 'ANCIENT_GEAR_CASTLE_CID', 'eval_ancient_gear_castle_cid', None),

    # PARASITIC_TICKY_CID = 0x19c4
    (0x080385a8, 0x19c4, 'PARASITIC_TICKY_CID', 'eval_parasitic_ticky_cid', None),

    # TREEBORN_FROG_CID = 0x19cb
    (0x08038d48, 0x19cb, 'TREEBORN_FROG_CID', 'eval_treeborn_frog_cid', None),

    # BEELZE_FROG_CID = 0x19cc
    (0x0803856c, 0x19cc, 'BEELZE_FROG_CID', 'eval_beelze_frog_cid', None),

    # SAND_MOTH_CID = 0x19d2
    (0x080380a8, 0x19d2, 'SAND_MOTH_CID', 'eval_sand_moth_cid', None),

    # D3S_FROG_CID = 0x19d6
    (0x080385e0, 0x19d6, 'D3S_FROG_CID', 'eval_d3s_frog_cid', None),

    # EHERO_ERIKSHIELER_CID = 0x19ef (two slots)
    (0x08038040, 0x19ef, 'EHERO_ERIKSHIELER_CID', 'eval_ehero_erikshieler_cid_a', None),
    (0x080385d0, 0x19ef, 'EHERO_ERIKSHIELER_CID', 'eval_ehero_erikshieler_cid_b', None),

    # GREAT_SPIRIT_CID = 0x19f1
    (0x080382bc, 0x19f1, 'GREAT_SPIRIT_CID', 'eval_great_spirit_cid', None),

    # HELIOS_CID = 0x19f6 (The Ancient Sun Helios)
    (0x08038600, 0x19f6, 'HELIOS_CID', 'eval_helios_cid', None),

    # HELIOS_DUO_MEGISTE_CID = 0x19f7
    (0x0803861c, 0x19f7, 'HELIOS_DUO_MEGISTE_CID', 'eval_helios_duo_megiste_cid', None),

    # MIRROR_WALL_CID = 0x1381
    (0x0803a538, 0x1381, 'MIRROR_WALL_CID', 'check_equip_chain_mirror_wall_cid', None),

    # AQUA_CHORUS_CID = 0x138e
    (0x0803914c, 0x138e, 'AQUA_CHORUS_CID', 'eval_aqua_chorus_cid', None),

    # COMMAND_KNIGHT_CID = 0x1399 (two slots)
    (0x08038f0c, 0x1399, 'COMMAND_KNIGHT_CID', 'eval_command_knight_cid_a', None),
    (0x0803a5bc, 0x1399, 'COMMAND_KNIGHT_CID', 'check_equip_chain_command_knight_cid', None),

    # SKULL_SERVANT_CID = 0x0fbe
    (0x08038168, 0x0fbe, 'SKULL_SERVANT_CID', 'eval_skull_servant_cid', None),

    # DARK_MAGICIAN_CID_0FC9 = 0x0fc9
    (0x08038764, 0x0fc9, 'DARK_MAGICIAN_CID_0FC9', 'eval_dark_magician_0fc9_cid', None),

    # HARPIE_LADY_CID = 0x0fe4
    (0x08038684, 0x0fe4, 'HARPIE_LADY_CID', 'eval_harpie_lady_cid', None),

    # CASTLE_OF_DARK_ILLUSIONS_CID = 0x0ff9
    (0x0803a70c, 0x0ff9, 'CASTLE_OF_DARK_ILLUSIONS_CID', 'classify_castle_dark_illusions_cid', None),

    # PUMPKING_CID = 0x1009
    (0x080382cc, 0x1009, 'PUMPKING_CID', 'eval_pumpking_cid', None),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label, eol_or_None)
# ---------------------------------------------------------------------------
REF_SLOTS = [

    # gDuelFieldSlots = 0x0201c510
    (0x08038038, 0x0201c510, 'gDuelFieldSlots', 'eval_slot_score_entry_full_field_slots', None),
    (0x08038194, 0x0201c510, 'gDuelFieldSlots', 'eval_slot_lp_cost_field_slots_a', None),
    (0x080382b0, 0x0201c510, 'gDuelFieldSlots', 'eval_slot_lp_cost_field_slots_b', None),
    (0x08038c80, 0x0201c510, 'gDuelFieldSlots', 'eval_hand_field6_slots', None),
    (0x08038da4, 0x0201c510, 'gDuelFieldSlots', 'eval_extra_deck_slots', None),
    (0x08039120, 0x0201c510, 'gDuelFieldSlots', 'eval_bonus_state_slots_a', None),
    (0x08039190, 0x0201c510, 'gDuelFieldSlots', 'eval_bonus_state_slots_b', None),
    (0x08039310, 0x0201c510, 'gDuelFieldSlots', 'dispatch_equip_node_slots', None),
    (0x0803a5a0, 0x0201c510, 'gDuelFieldSlots', 'check_equip_chain_slots_a', None),
    (0x0803a650, 0x0201c510, 'gDuelFieldSlots', 'classify_equip_slots_a', None),
    (0x0803a6c8, 0x0201c510, 'gDuelFieldSlots', 'classify_equip_slots_b', None),
    (0x0803a708, 0x0201c510, 'gDuelFieldSlots', 'classify_equip_slots_c', None),

    # gDuelFieldSlots_p2_base = 0x0201c5d8
    (0x0803925c, 0x0201c5d8, 'gDuelFieldSlots_p2_base', 'adjust_score_p2_slots', None),

    # gEquipNodePool = 0x0201d9c0
    (0x08039314, 0x0201d9c0, 'gEquipNodePool', 'dispatch_equip_node_pool', None),

    # gP1HandCountBase = 0x0201c4f4
    (0x08038758, 0x0201c4f4, 'gP1HandCountBase', 'eval_hand_magicians_count_base', None),

    # gP1FieldState = 0x0201e1d4 (new global label: gP1LifePoints + FIELD_STATE_OFF)
    (0x08039198, 0x0201e1d4, 'gP1FieldState', 'eval_p1_field_state_direct', None),

    # zone_monster_field_bonus_table = 0x09e3f094 (carve label)
    (0x0803912c, 0x09e3f094, 'zone_monster_field_bonus_table', 'eval_bonus_state_table_ref_a', None),
    (0x0803a654, 0x09e3f094, 'zone_monster_field_bonus_table', 'classify_equip_table_ref_b', None),

    # check_card_is_amazoness_type+1 = 0x0804b049 (THUMB fn-ptr)
    (0x080389dc, 0x0804b049, 'check_card_is_amazoness_type', 'eval_amazoness_fnptr_a', None),
    (0x080389f8, 0x0804b049, 'check_card_is_amazoness_type', 'eval_amazoness_fnptr_b', None),

    # dispatch_equip_node_jump_table = 0x0803931c (jump table base)
    (0x08039318, 0x0803931c, 'dispatch_equip_node_jump_table', 'dispatch_equip_jump_table_base', None),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, old_label, new_label, eol_or_None)
# ---------------------------------------------------------------------------
RENAME_SLOTS = [

    # jump table itself
    (0x0803931c, 'PTR_DAT_0803931c', 'dispatch_equip_node_jump_table',
     '13-entry PC-dispatch table for equip node types 1..13'),

    # first entry of the table (will be overwritten by disasm, but label the raw slot too)
    (0x08039350, 'DAT_08039350', 'eval_equip_type_1_to_4_stub',
     'type 1..4 -> same code path: card-ID chain'),

    # shifted sentinel slots
    (0x08038ae4, 'DAT_08038ae4', 'eval_sanctuary_cid_shifted',
     'SANCTUARY_IN_THE_SKY_CID<<19; mov pc dispatch sentinel'),
    (0x08039128, 'DAT_08039128', 'eval_batteryman_c_cid_shifted',
     'BATTERYMAN_C_CID<<19'),
    (0x08038c84, 'DAT_08038c84', 'eval_batteryman_aa_cid_shifted',
     'BATTERYMAN_AA_CID<<19; mov pc dispatch sentinel'),

    # LP thresholds
    (0x08038b38, 'DAT_08038b38', 'eval_lp_cost_1500', 'LP threshold 1500'),
    (0x080380d8, 'DAT_080380d8', 'eval_lp_cost_3000_a', '3000 LP threshold slot a'),
    (0x08038bf4, 'DAT_08038bf4', 'eval_lp_cost_3000_b', '3000 LP threshold slot b'),
    (0x08038e6c, 'DAT_08038e6c', 'eval_lp_cost_3000_c', '3000 LP threshold slot c'),

    # sentinel
    (0x080389a8, 'DAT_080389a8', 'eval_slot_empty_sentinel', '0xffff: no-card sentinel'),

    # score deltas
    (0x0803919c, 'DAT_0803919c', 'eval_score_delta_neg300_a', '-300 score delta'),
    (0x080391b8, 'DAT_080391b8', 'eval_score_delta_neg300_b', '-300 score delta'),
    (0x080391d4, 'DAT_080391d4', 'eval_score_delta_neg500', '-500 score delta'),
    (0x08039258, 'DAT_08039258', 'eval_score_delta_neg700', '-700 score delta'),

    # hand count offset
    (0x08038760, 'DAT_08038760', 'eval_hand_count_to_slot_off',
     '0x404: gP1HandCountBase to gP1HandSlotArray offset'),

    # gap CIDs
    (0x080382dc, 'DAT_080382dc', 'eval_gap_cid_1091', 'gap CID 0x1091; not in card-stats.s'),
    (0x0803836c, 'DAT_0803836c', 'eval_gap_cid_133d', 'gap CID 0x133d; not in card-stats.s'),
    (0x0803862c, 'DAT_0803862c', 'eval_gap_cid_11d0', 'gap CID 0x11d0; passed to count_paired_slots'),
    (0x080386c4, 'DAT_080386c4', 'eval_gap_cid_0fb2', 'gap CID 0x0fb2; passed to count_paired_slots'),
    (0x080382c4, 'DAT_080382c4', 'eval_gap_cid_1387', 'gap CID 0x1387; zone_id sentinel per asm/14'),
    (0x0803a720, 'DAT_0803a720', 'classify_gap_cid_128a', 'gap CID 0x128a; also in asm/02 chain_128a'),
]

# ---------------------------------------------------------------------------
# D. PLATE_FULL: (func_addr, plate_text)
# All text is pure ASCII. FUN_ references replaced with current names.
# ---------------------------------------------------------------------------
PLATES = [

    (0x08037ec0,
     "eval_slot_score_entry_full [0x08037ec0]\n"
     "Computes score entry for a duel field slot (equip chain evaluation).\n"
     "Walks monster zones (stride PLAYER_BLOCK_STRIDE=0x868), evaluates LP cost paths,\n"
     "field-spell bonuses, and equip-node dispatch.\n"
     "Calls: compute_lp_cost_by_occupied_monster_zones, compute_lp_cost_by_hand_field6,\n"
     "       compute_lp_cost_by_extra_deck_card_id, compute_lp_cost_by_zone_field5_x100,\n"
     "       compute_lp_cost_by_zone_field5_x200, compute_lp_cost_by_zone_field5_both_players,\n"
     "       apply_slot_score_bonus_by_state, dispatch_equip_node_by_type.\n"
     "Caller(s): AI equip scoring engine."),

    (0x08038a1a,
     "compute_lp_cost_by_occupied_monster_zones [0x08038a1a]\n"
     "Counts occupied monster zone slots for current player using Amazoness fn-ptr check.\n"
     "Calls count_monster_slots_by_fnptr with check_card_is_amazoness_type.\n"
     "Returns LP cost contribution based on zone occupancy count.\n"
     "Called from eval_slot_score_entry_full."),

    (0x08038c60,
     "compute_lp_cost_by_hand_field6 [0x08038c60]\n"
     "Computes LP cost based on hand cards with field6 attribute and Batteryman AA check.\n"
     "Uses gP1HandCountBase (0x0201c4f4) + HAND_COUNT_TO_SLOT_OFF (0x404).\n"
     "Shifted sentinel BATTERYMAN_AA_CID_SHIFTED (0xc6180000 = 0x18c3<<19) for fast CID compare.\n"
     "Called from eval_slot_score_entry_full."),

    (0x08038d34,
     "compute_lp_cost_by_extra_deck_card_id [0x08038d34]\n"
     "Evaluates LP cost from extra-deck card IDs: Tadpole (0x1919) / Treeborn Frog (0x19cb).\n"
     "Uses gDuelFieldSlots (0x0201c510) and PLAYER_BLOCK_STRIDE (0x868).\n"
     "Called from eval_slot_score_entry_full."),

    (0x08038e84,
     "compute_lp_cost_by_zone_field5_x100 [0x08038e84]\n"
     "Returns LP cost x100 based on field5 zone count.\n"
     "Sibling of compute_lp_cost_by_zone_field5_x200 (0x08038e90).\n"
     "Called from eval_slot_score_entry_full."),

    (0x08038e90,
     "compute_lp_cost_by_zone_field5_x200 [0x08038e90]\n"
     "Returns LP cost x200 based on field5 zone count.\n"
     "Sibling of compute_lp_cost_by_zone_field5_x100 (0x08038e84).\n"
     "Called from eval_slot_score_entry_full."),

    (0x08038e9c,
     "compute_lp_cost_by_zone_field5_both_players [0x08038e9c]\n"
     "Returns LP cost contribution from field5 zones for both players.\n"
     "Uses PLAYER_BLOCK_STRIDE (0x868) to step P1->P2.\n"
     "Called from eval_slot_score_entry_full."),

    (0x08038e34,
     "apply_slot_score_bonus_by_state [0x08038e34]\n"
     "Applies field-spell ATK bonus from zone_monster_field_bonus_table (0x09e3f094).\n"
     "Table: 13 valid entries x 16B; fields [0..6]=ATK bonuses [7..12]=CID-encoded associations.\n"
     "Uses DUEL_ACTIVE_PLAYER_OFF (0x1cb8) for active player index.\n"
     "Score deltas: SCORE_DELTA_NEG_300/NEG_500/NEG_700.\n"
     "Called from eval_slot_score_entry_full."),

    (0x080392da,
     "dispatch_equip_node_by_type [0x080392da]\n"
     "Dispatches equip node processing via 13-entry jump table (mov pc,r0).\n"
     "Table at dispatch_equip_node_jump_table (0x0803931c).\n"
     "Types 1..4 -> eval_equip_node_type_1_to_4 (0x08039350)\n"
     "Type 5     -> eval_equip_node_type_5 (0x08039a62)\n"
     "Types 6..9 -> eval_equip_node_type_6_to_9 (0x08039a7c)\n"
     "Types 10..11 -> eval_equip_node_type_10_to_11 (0x08039c1c)\n"
     "Type 12    -> eval_equip_node_type_12 (0x0803a3c4)\n"
     "Type 13    -> eval_equip_node_type_13 (0x0803a2fc)\n"
     "ARMv4T: mov pc,r0 in THUMB maintains CPSR.T; even-addr stubs execute as THUMB.\n"
     "Called from eval_slot_score_entry_full."),

    (0x0803a41e,
     "advance_equip_node_chain_step [0x0803a41e]\n"
     "Advances the equip node chain iterator by one step.\n"
     "Uses gEquipNodePool (0x0201d9c0) and PLAYER_BLOCK_STRIDE.\n"
     "Called from eval_equip_node_type_* stubs."),

    (0x0803a428,
     "adjust_slot_score_by_chain_and_zone [0x0803a428]\n"
     "Adjusts slot score based on equip chain state and zone configuration.\n"
     "Uses gDuelFieldSlots_p2_base (0x0201c5d8), DUEL_ACTIVE_PLAYER_OFF (0x1cb8),\n"
     "SCORE_DELTA_NEG_300, SCORE_DELTA_NEG_700.\n"
     "Called from eval_slot_score_entry_full."),

    (0x0803a520,
     "cleanup_slot_score_entry_epilogue [0x0803a520]\n"
     "Epilogue: restores caller state and returns slot score result.\n"
     "Called from eval_slot_score_entry_full via bx r0."),

    (0x0803a540,
     "check_slot_equip_chain_rule [0x0803a540]\n"
     "Checks whether an equip chain rule applies to the current slot.\n"
     "Tests card IDs: Water Dragon (0x1951), Cyber Blader (0x1955), Mirror Wall (0x1381),\n"
     "Dark Dreadroute (0x1905), Command Knight (0x1399).\n"
     "Uses EQUIP_NODE_BASE_OFFSET (0x14b0), PLAYER_BLOCK_STRIDE, gDuelFieldSlots.\n"
     "Returns: 0=rule not applicable, 1=rule applies."),

    (0x0803a658,
     "classify_equip_target_eligibility [0x0803a658]\n"
     "Classifies whether a target slot is eligible for equip placement.\n"
     "Evaluates zone_monster_field_bonus_table (0x09e3f094) for field-spell bonuses.\n"
     "Checks: compute_zone_effect_atk_delta (0x08037c9c), find_effect_entry_by_player_zone (0x08036b88).\n"
     "Tests gap CID 0x128a range (per asm/10 plate), Unhappy Girl (0x1743),\n"
     "Castle of Dark Illusions (0x0ff9).\n"
     "Returns eligibility category code."),

]

# ---------------------------------------------------------------------------
# Apply
# ---------------------------------------------------------------------------
print("=== RefineF03Seg4bSlots.py DRY=%s ===" % DRY)

fail_count = 0
applied_eq = 0
applied_ref = 0
applied_rename = 0
applied_plate = 0

print("--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
for (sa, val, eq_nm, sl_nm, eol) in EQ_SLOTS:
    if not DRY and not _check(sa, val):
        fail_count += 1
        continue
    _eq(sa, val, eq_nm, sl_nm, eol)
    applied_eq += 1

print("--- B. REF_SLOTS (%d) ---" % len(REF_SLOTS))
for (sa, ta, gas, sl, eol) in REF_SLOTS:
    _ref(sa, ta, gas, sl, eol)
    applied_ref += 1

print("--- C. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
for (sa, old_nm, new_nm, eol) in RENAME_SLOTS:
    _rename(sa, old_nm, new_nm, eol)
    applied_rename += 1

print("--- D. PLATE_FULL (%d) ---" % len(PLATES))
for (fa, text) in PLATES:
    _plate(fa, text)
    applied_plate += 1

print("=== DONE: EQ=%d REF=%d RENAME=%d PLATE=%d FAIL=%d ===" % (
    applied_eq, applied_ref, applied_rename, applied_plate, fail_count))
