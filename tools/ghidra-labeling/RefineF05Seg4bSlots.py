# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF05Seg4bSlots.py -- p5 file-05 Seg-4b (0x0804be38..0x0804c6e8)
#
#   Sections:
#     A. EQ_SLOTS      -- data-equate 89 slots
#                         A-class (reuse existing card_info.inc): 28 slots
#                         B-class (new card_info.inc CIDs): 61 slots
#     C. RENAME_SLOTS  -- 10 slots (8 gap CID + 2 structural constants)
#                         with ASCII EOL comments
#     P. PLATE         -- 1 function plate rewrite (FUN_ -> current name)
#
#   99 DAT_ slots total covered: EQ=89 + RENAME=10
#   FUNC_RENAME=0, REF=0, carve=0, disasm=0
#
#   All slot values verified ROM struct.unpack_from('<I', rom, addr-0x08000000).
#   Reviewer C4 spot-check: 25 slots independently verified -- all match.
#
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
# A. EQ_SLOTS: (slot_addr, value, const_name, slot_label)
#    const_name = existing or new card_info.inc .equ name
#    slot_label = <func_abbrev>_<cid_short> (unique per slot, != const_name)
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # --- get_card_effect_category (0x0804be38) ---
    # A-class reuse
    (0x0804be5c, 0x0000161a, 'ROYAL_MAGICAL_LIBRARY_CID',       'effect_cat_royal_mag_lib_a_cid'),
    # B-class new
    (0x0804be60, 0x0000128e, 'HANNIBAL_NECROMANCER_CID',        'effect_cat_hannibal_necro_cid'),
    (0x0804be64, 0x00001610, 'SKILLED_WHITE_MAGICIAN_CID',      'effect_cat_skilled_white_mag_cid'),
    # A-class reuse
    (0x0804be78, 0x00001615, 'MAGICAL_MARIONETTE_CID',          'effect_cat_magical_marionette_cid'),
    # A-class reuse
    (0x0804be90, 0x000016de, 'TOWER_OF_BABEL_CID',              'effect_cat_tower_of_babel_cid'),
    # B-class new
    (0x0804bea8, 0x0000186a, 'BLAST_MAGICIAN_CID',              'effect_cat_blast_magician_cid'),
    (0x0804beb4, 0x00001983, 'MYTHICAL_BEAST_CERBERUS_CID',     'effect_cat_mythical_beast_cerb_cid'),

    # --- check_card_id_is_equip_set_b (0x0804bf20) ---
    # B-class new
    (0x0804bf3c, 0x00001909, 'SPARK_BLASTER_CID',               'equip_set_b_spark_blaster_cid'),
    (0x0804bf44, 0x00001529, 'GREAT_DEZARD_CID',                'equip_set_b_great_dezard_cid'),
    # B-class new
    (0x0804bf54, 0x00001837, 'BIG_CORE_CID',                    'equip_set_b_big_core_cid'),
    # A-class reuse
    (0x0804bf6c, 0x00001962, 'BES_TETRAN_CID',                  'equip_set_b_bes_tetran_cid'),
    (0x0804bf80, 0x000019b2, 'ANCIENT_GEAR_CASTLE_CID',         'equip_set_b_anc_gear_castle_cid'),

    # --- check_card_id_is_equip_set_d (0x0804bf88) ---
    # B-class new
    (0x0804bfac, 0x000012ec, 'POT_OF_GREED_CID',                'equip_set_d_pot_of_greed_a_cid'),
    # B-class new
    (0x0804bfc8, 0x000012ce, 'MESMERIC_CONTROL_CID',            'equip_set_d_mesmeric_ctrl_cid'),
    (0x0804bfe8, 0x00001325, 'DELINQUENT_DUO_CID',              'equip_set_d_delinquent_duo_cid'),
    (0x0804bff4, 0x00001307, 'RESTRUCTER_REVOLUTION_CID',       'equip_set_d_restructer_rev_cid'),
    (0x0804c008, 0x0000132b, 'THE_FORCEFUL_SENTRY_CID',         'equip_set_d_forceful_sentry_cid'),
    (0x0804c00c, 0x00001804, 'CEMETARY_BOMB_CID',               'equip_set_d_cemetary_bomb_cid'),

    # --- check_card_is_equip_set_c (0x0804c014) ---
    # B-class new
    (0x0804c02c, 0x0000114f, 'THUNDER_DRAGON_CID',              'equip_set_c_thunder_dragon_cid'),
    (0x0804c044, 0x0000168f, 'DESROOK_ARCHFIEND_CID',           'equip_set_c_desrook_archfiend_cid'),
    # B-class new (2 slots for KING_OF_THE_SWAMP)
    (0x0804c054, 0x0000179c, 'KING_OF_THE_SWAMP_CID',           'equip_set_c_king_swamp_a_cid'),

    # --- check_card_id_is_equip_blocker (0x0804c05c) ---
    # B-class new
    (0x0804c070, 0x0000149c, 'FUSION_GATE_CID',                 'equip_blocker_fusion_gate_cid'),
    (0x0804c074, 0x00001232, 'MAGICAL_LABYRINTH_CID',           'equip_blocker_magical_lab_cid'),

    # --- check_card_id_is_equip_set_e (0x0804c08c) ---
    # B-class new
    (0x0804c0a8, 0x00001228, 'MYSTICAL_SHEEP_1_CID',            'equip_set_e_mystical_sheep1_cid'),
    (0x0804c0ac, 0x000010a8, 'BEASTKING_OF_THE_SWAMPS_CID',     'equip_set_e_beastking_swamps_cid'),
    (0x0804c0b8, 0x000010b3, 'VERSAGO_THE_DESTROYER_CID',       'equip_set_e_versago_destroyer_cid'),
    # B-class new (2nd slot for KING_OF_THE_SWAMP)
    (0x0804c0d8, 0x0000179c, 'KING_OF_THE_SWAMP_CID',           'equip_set_e_king_swamp_b_cid'),

    # --- check_card_id_is_equip_excluded_set_f (0x0804c0e0) ---
    # A-class reuse
    (0x0804c0fc, 0x000018fd, 'CYBER_END_DRAGON_CID',            'equip_excl_f_cyber_end_dragon_cid'),
    # A-class reuse
    (0x0804c100, 0x000014c7, 'RYU_SENSHI_CID',                  'equip_excl_f_ryu_senshi_a_cid'),
    # A-class reuse
    (0x0804c110, 0x000014da, 'FIEND_SKULL_DRAGON_CID',          'equip_excl_f_fiend_skull_cid'),
    # A-class reuse
    (0x0804c128, 0x00001955, 'CYBER_BLADER_CID',                'equip_excl_f_cyber_blader_cid'),
    # B-class new
    (0x0804c138, 0x000019d6, 'D3S_FROG_CID',                    'equip_excl_f_d3s_frog_cid'),

    # --- check_card_id_is_field_zone_special (0x0804c140) ---
    # B-class new
    (0x0804c154, 0x0000170a, 'MATAZA_THE_ZAPPER_CID',           'field_zone_spec_mataza_zapper_cid'),
    # A-class reuse
    (0x0804c164, 0x000017d2, 'HORUS_LV4_CID',                   'field_zone_spec_horus_lv4_cid'),

    # --- check_card_is_zone_pair_restricted (0x0804c16c) ---
    # A-class reuse
    (0x0804c180, 0x000012d3, 'AMPLIFIER_CID',                   'zone_pair_restr_amplifier_cid'),
    # B-class new
    (0x0804c184, 0x0000147e, 'SPIRITUALISM_CID',                'zone_pair_restr_spiritualism_cid'),

    # --- check_card_is_field_spell_type_b (0x0804c18c) ---
    # B-class new
    (0x0804c1ac, 0x00001497, 'SPIRIT_MESSAGE_I_CID',            'field_spell_b_spirit_msg_i_cid'),
    (0x0804c1b0, 0x000017ae, 'THE_SECOND_SARCOPHAGUS_CID',      'field_spell_b_2nd_sarcophagus_cid'),

    # --- get_card_effect_zone_check_sides (0x0804c1b8) ---
    # B-class new
    (0x0804c1f4, 0x000014e2, 'SUPER_REJUVENATION_CID',          'zone_sides_super_rejuv_cid'),
    (0x0804c1f8, 0x000012ec, 'POT_OF_GREED_CID',                'zone_sides_pot_of_greed_b_cid'),
    # B-class new
    (0x0804c20c, 0x0000131f, 'UPSTART_GOBLIN_CID',              'zone_sides_upstart_goblin_cid'),
    # B-class new
    (0x0804c214, 0x0000145a, 'JAR_OF_GREED_CID',                'zone_sides_jar_of_greed_a_cid'),
    # B-class new
    (0x0804c22c, 0x00001567, 'CARD_OF_SANCTITY_CID',            'zone_sides_card_of_sanctity_cid'),
    # B-class new
    (0x0804c240, 0x0000161a, 'ROYAL_MAGICAL_LIBRARY_CID',       'zone_sides_royal_mag_lib_b_cid'),
    # B-class new
    (0x0804c248, 0x0000162a, 'JAR_ROBBER_CID',                  'zone_sides_jar_robber_cid'),
    # B-class new
    (0x0804c26c, 0x000017a5, 'CARD_7_CID',                      'zone_sides_card7_cid'),
    # B-class new
    (0x0804c280, 0x00001776, 'CORPSE_OF_YATA_GARASU_CID',       'zone_sides_corpse_yata_cid'),
    # B-class new
    (0x0804c2a8, 0x00001888, 'GOOD_GOBLIN_HOUSEKEEPING_CID',    'zone_sides_good_goblin_hk_cid'),
    # B-class new
    (0x0804c2c0, 0x0000196f, 'POT_OF_AVARICE_CID',              'zone_sides_pot_of_avarice_cid'),
    # B-class new
    (0x0804c2d0, 0x0000198d, 'MAGICAL_MALLET_CID',              'zone_sides_magical_mallet_cid'),

    # --- check_card_id_is_equip_set_g (0x0804c2e0) ---
    # A-class reuse
    (0x0804c304, 0x0000159d, 'NECROVALLEY_CID',                 'equip_set_g_necrovalley_cid'),
    # A-class reuse
    (0x0804c308, 0x00001302, 'ROYAL_DECREE_CID',                'equip_set_g_royal_decree_cid'),
    # A-class reuse
    (0x0804c310, 0x000014c7, 'RYU_SENSHI_CID',                  'equip_set_g_ryu_senshi_b_cid'),
    # B-class new
    (0x0804c324, 0x000014de, 'THE_DRAGONS_BEAD_CID',            'equip_set_g_dragons_bead_cid'),
    # B-class new (2nd slot GREAT_DEZARD)
    (0x0804c334, 0x00001529, 'GREAT_DEZARD_CID',                'equip_set_g_great_dezard_cid'),
    # A-class reuse
    (0x0804c350, 0x000017c2, 'BLUE_EYES_SHINING_DRAGON_CID',    'equip_set_g_beshd_cid'),
    # B-class new
    (0x0804c358, 0x000017b9, 'THE_END_OF_ANUBIS_CID',           'equip_set_g_end_of_anubis_cid'),
    # A-class reuse
    (0x0804c370, 0x0000183a, 'A_TEAM_TRAP_DISPOSAL_UNIT_CID',   'equip_set_g_a_team_trap_cid'),
    # B-class new
    (0x0804c384, 0x00001936, 'ALKANA_KNIGHT_JOKER_CID',         'equip_set_g_alkana_joker_cid'),

    # --- classify_card_id_summon_category (0x0804c38c) ---
    # A-class reuse
    (0x0804c3d4, 0x00001631, 'MIRACLE_RESTORING_CID',           'summon_cat_miracle_restoring_cid'),
    (0x0804c3d8, 0x00001488, 'GILASAURUS_CID',                  'summon_cat_gilasaurus_cid'),
    # A-class reuse
    (0x0804c3dc, 0x00001366, 'PREMATURE_BURIAL_CID',            'summon_cat_premature_burial_cid'),
    # B-class new
    (0x0804c3e0, 0x0000106d, 'PENGUIN_KNIGHT_CID',              'summon_cat_penguin_knight_cid'),
    # B-class new
    (0x0804c3f0, 0x00001138, 'MONSTER_EYE_CID',                 'summon_cat_monster_eye_cid'),
    # B-class new
    (0x0804c404, 0x000012ea, 'MONSTER_REBORN_CID',              'summon_cat_monster_reborn_cid'),
    # B-class new
    (0x0804c414, 0x0000133b, 'SPEAR_CRETIN_CID',                'summon_cat_spear_cretin_cid'),
    # B-class new
    (0x0804c434, 0x000013fe, 'DE_FUSION_CID',                   'summon_cat_de_fusion_cid'),
    # A-class reuse
    (0x0804c444, 0x0000138a, 'VALKYRION_THE_MAGNA_WARRIOR_CID', 'summon_cat_valkyrion_cid'),
    # NOTE: 0x0804c45a annotation (=0x0804c214) in proposal table was misread;
    # ROM @ 0x0804c45a = 0x3034e134 (not 0x145a); the JAR_OF_GREED 2nd slot is c214 (already listed above).
    # B-class new
    (0x0804c4b0, 0x000014d2, 'THE_WARRIOR_RETURNING_ALIVE_CID', 'summon_cat_warrior_ret_alive_cid'),
    # A-class reuse
    (0x0804c4d4, 0x000014fb, 'FIBER_JAR_CID',                   'summon_cat_fiber_jar_cid'),
    # A-class reuse
    (0x0804c4dc, 0x00001534, 'FUSHIOH_RICHIE_CID',              'summon_cat_fushioh_richie_cid'),
    # A-class reuse
    (0x0804c4fc, 0x000015e6, 'AUTONOMOUS_ACTION_UNIT_CID',      'summon_cat_autonomous_unit_cid'),
    # B-class new
    (0x0804c50c, 0x0000158f, 'MYSTICAL_KNIGHT_OF_JACKAL_CID',   'summon_cat_mystical_kof_jackal_cid'),
    # B-class new
    (0x0804c524, 0x00001611, 'SKILLED_DARK_MAGICIAN_CID',       'summon_cat_skilled_dark_mag_cid'),
    # B-class new
    (0x0804c56c, 0x0000179a, 'NIGHT_ASSAILANT_CID',             'summon_cat_night_assailant_cid'),
    # B-class new
    (0x0804c57c, 0x0000164f, 'EQUIP_CHAIN_PAIR_CARD_MAX',        'summon_cat_equip_chain_max_cid'),
    # B-class new
    (0x0804c598, 0x000016a4, 'EQUIP_LOCK_A_CID',                'summon_cat_equip_lock_a_cid'),
    # B-class new
    (0x0804c5a8, 0x000016a8, 'RAY_OF_HOPE_CID',                 'summon_cat_ray_of_hope_cid'),
    # B-class new
    (0x0804c5c8, 0x00001745, 'THE_KICK_MAN_CID',                'summon_cat_the_kick_man_cid'),
    # B-class new
    (0x0804c5d8, 0x00001713, 'DEDICATION_THROUGH_LIGHT_DARK_CID','summon_cat_dedic_light_dark_cid'),
    # B-class new
    (0x0804c5f0, 0x0000178a, 'ASWAN_APPARITION_CID',            'summon_cat_aswan_apparition_cid'),
    # B-class new
    (0x0804c600, 0x0000178c, 'NUBIAN_GUARD_CID',                'summon_cat_nubian_guard_cid'),
    # A-class reuse
    (0x0804c628, 0x00001881, 'RE_FUSION_CID',                   'summon_cat_re_fusion_cid'),
    # B-class new
    (0x0804c638, 0x000017f1, 'DARK_FACTORY_MASS_PROD_CID',      'summon_cat_dark_factory_mprod_cid'),
    # A-class reuse
    (0x0804c650, 0x00001864, 'BEHEMOTH_KING_CID',               'summon_cat_behemoth_king_cid'),
    # B-class new
    (0x0804c664, 0x0000187a, 'A_FEATHER_OF_THE_PHOENIX_CID',    'summon_cat_feather_phoenix_cid'),
    # A-class reuse
    (0x0804c680, 0x00001951, 'WATER_DRAGON_CID',                'summon_cat_water_dragon_cid'),
    # B-class new
    (0x0804c690, 0x0000190a, 'DARK_RULER_VANDALGYON_CID',       'summon_cat_dark_ruler_vand_cid'),
    # B-class new
    (0x0804c6ac, 0x00001979, 'ROLL_OUT_CID',                    'summon_cat_roll_out_cid'),

    # --- get_paired_card_id_by_variant (0x0804c6cc) ---
    # B-class new (structural: equip base subtract operand)
    # NOTE: 0x0804c6e0 and 0x0804c6e4 are structural constants -- handled in RENAME_SLOTS
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, label, eol_ascii_or_None)
#    8 gap CID slots + 2 structural constant slots. Pure ASCII EOL.
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    # --- check_card_id_is_equip_blocker (0x0804c05c) ---
    (0x0804c084, 'check_equip_blocker_cid_1517',
     'gap cid 0x1517; between Disappear(0x1515) Bottomless_Trap_Hole(0x1518); conf low'),

    # --- check_card_id_is_equip_excluded_set_f (0x0804c0e0) ---
    # (no gap CIDs in this function -- all handled in EQ_SLOTS)

    # --- get_card_effect_zone_check_sides (0x0804c1b8) ---
    (0x0804c1f0, 'get_card_effect_zone_sides_cid_16c1',
     'gap cid 0x16c1; between Freed_the_Brave(0x16c0) Witch_Doctor(0x16c2); conf low'),

    # --- check_card_id_is_equip_set_b (0x0804bf20) ---
    (0x0804bf40, 'check_equip_set_b_cid_16fe',
     'gap cid 0x16fe; between Don_Turtle(0x16fd) Dark_Driceratops(0x16ff); conf low'),

    # --- check_card_id_is_equip_set_g (0x0804c2e0) ---
    (0x0804c28c, 'check_equip_set_g_cid_1790',
     'gap cid 0x1790; between Sand_Gambler(0x178f) Ghost_Knight(0x1791); conf low'),

    # --- classify_card_id_summon_category (0x0804c38c) ---
    (0x0804c4a0, 'classify_summon_cat_cid_1549',
     'gap cid 0x1549; between Reckless_Greed(0x1548) Toon_DMG(0x154a); conf low'),
    (0x0804c534, 'classify_summon_cat_cid_1616',
     'gap cid 0x1616; between Magical_Marionette(0x1615) Breaker(0x1617); conf low'),

    # --- get_card_effect_zone_check_sides (0x0804c1b8) ---
    (0x0804c460, 'get_card_effect_zone_sides_cid_144c',
     'gap cid 0x144c; between Amazon_Archer(0x144b) Fire_Princess(0x144d); conf low'),
    (0x0804c470, 'get_card_effect_zone_sides_cid_1452',
     'gap cid 0x1452; between Dancing_Fairy(0x1451) Empress_Mantis(0x1453); conf low'),

    # --- get_paired_card_id_by_variant (0x0804c6cc) structural constants ---
    (0x0804c6e0, 'get_paired_card_id_by_variant_base_sub',
     '= -0x164a (negate Guardian_Elma CID range base; r0 -= 0x164a to get variant index)'),
    (0x0804c6e4, 'get_paired_card_id_by_variant_table_ptr',
     '= &switchD_0804c6dc__switchdataD_0804c6e8; pointer to 6-entry jump table'),
]

# ---------------------------------------------------------------------------
# P. PLATE: (func_addr, new_plate_ascii)
#    1 function: classify_card_id_summon_category (0x0804c38c)
#    FUN_0803088c -> check_effect_slot_summon_path_eligible
# ---------------------------------------------------------------------------
PLATES = [
    (0x0804c38c,
     "Large BST: classifies card_id r0 into 3 summon/effect categories. "
     "Returns 0=no category, 1=category-1 (primary range up to 0x1631=MIRACLE_RESTORING_CID), "
     "2=category-2 (special subset). "
     "Used by check_effect_slot_summon_path_eligible (0x0803088c) to decide activation path. "
     "r0=u16 card_id. Returns u32 category [0..2]."),
]

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _check(slot_int, want):
    d = getDataAt(_addr(slot_int))
    if d is None or d.getLength() != 4:
        return False, "no 4B data"
    try:
        dv = d.getValue()
        iv = (int(dv.getValue()) & 0xffffffff) if hasattr(dv, 'getValue') else (int(dv) & 0xffffffff)
    except Exception:
        iv = None
    if iv is not None and iv != (want & 0xffffffff):
        return False, "value mismatch got=0x%x want=0x%x" % (iv, want)
    return True, None


def main():
    print("=== RefineF05Seg4bSlots (DRY=%s) ===" % DRY)
    rm      = currentProgram.getReferenceManager()
    et      = currentProgram.getEquateTable()
    listing = currentProgram.getListing()
    fm      = currentProgram.getFunctionManager()
    nA = nC = nP = 0

    # --- A. EQ_SLOTS ---
    for slot_int, value, cname, label in EQ_SLOTS:
        ok, err = _check(slot_int, value)
        if not ok:
            print("[A FAIL] 0x%08x: %s" % (slot_int, err)); continue
        if DRY:
            print("[A dry] 0x%08x equate %s=0x%x rename %s" % (slot_int, cname, value, label))
            nA += 1; continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        eq = et.getEquate(cname)
        if eq is None:
            eq = et.createEquate(cname, value)
        eq.addReference(_addr(slot_int), 0)
        print("[A ok] 0x%08x -> %s (%s)" % (slot_int, label, cname)); nA += 1

    # --- C. RENAME_SLOTS ---
    for slot_int, label, eol in RENAME_SLOTS:
        d = getDataAt(_addr(slot_int))
        if d is None or d.getLength() != 4:
            print("[C FAIL] no 4B data @ 0x%08x" % slot_int); continue
        if DRY:
            print("[C dry] 0x%08x rename %s" % (slot_int, label)); nC += 1; continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        if eol:
            cu = listing.getCodeUnitAt(_addr(slot_int))
            if cu is None:
                cu = getDataAt(_addr(slot_int))
            if cu is not None:
                try:
                    cu.setComment(CodeUnit.EOL_COMMENT, eol)
                except Exception as ex:
                    print("[C WARN] setComment EOL @ 0x%08x: %s" % (slot_int, ex))
        print("[C ok] 0x%08x -> %s" % (slot_int, label)); nC += 1

    # --- P. PLATE ---
    for func_int, plate_text in PLATES:
        fn = fm.getFunctionAt(_addr(func_int))
        if fn is None:
            print("[P FAIL] no function @ 0x%08x" % func_int); continue
        if DRY:
            print("[P dry] 0x%08x plate rewrite (%d chars)" % (func_int, len(plate_text)))
            nP += 1; continue
        cu = listing.getCodeUnitAt(_addr(func_int))
        if cu is not None:
            try:
                cu.setComment(CodeUnit.PLATE_COMMENT, plate_text)
                print("[P ok] 0x%08x plate set (%d chars)" % (func_int, len(plate_text))); nP += 1
            except Exception as ex:
                print("[P FAIL] 0x%08x: %s" % (func_int, ex))
        else:
            print("[P FAIL] no CodeUnit @ 0x%08x" % func_int)

    print("=== DONE: EQ=%d RENAME=%d PLATE=%d ===" % (nA, nC, nP))


main()
