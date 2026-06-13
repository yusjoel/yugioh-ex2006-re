# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF05Seg4aSlots.py -- p5 file-05 Seg-4a (0x0804b4f4..0x0804be38)
#
#   Sections:
#     A. EQ_SLOTS      -- data-equate 95 slots (A-class 32 + B-class 63)
#     C. RENAME_SLOTS  -- 6 gap CID slots (plain rename + EOL ASCII)
#     S. SCALAR_EQ     -- 5 inline immediate scalar equates
#                         (3 movs CID + 2 cmp field6 type)
#
#   101 DAT_ slots total covered: EQ=95 (32 A-class + 63 B-class) + RENAME=6
#   FUNC_RENAME=0, REF=0, PLATE=0
#
#   All slot values verified ROM struct.unpack_from('<I', rom, addr-0x08000000).
#   All scalar immediates verified against ROM opcode bytes.
#
from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.scalar import Scalar

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
#    slot_label  = <func_abbrev>_<cid_short> (unique per slot)
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # --- get_card_field_summon_restriction (0x0804b4f4) ---
    # B-class new CIDs
    (0x0804b540, 0x00001227, 'INVADER_OF_THE_THRONE_CID',           'summon_restr_invader_throne_cid'),
    (0x0804b54c, 0x0000100c, 'MASK_OF_DARKNESS_CID',               'summon_restr_mask_darkness_cid'),
    (0x0804b560, 0x000010b0, 'PRINCESS_OF_TSURUGI_CID',            'summon_restr_princess_tsurugi_cid'),
    (0x0804b570, 0x00001152, 'MAGICIAN_OF_FAITH_CID',              'summon_restr_magician_faith_cid'),
    (0x0804b590, 0x000011d8, 'NEEDLE_WORM_CID',                    'summon_restr_needle_worm_cid'),
    (0x0804b5a0, 0x000011c3, 'HANE_HANE_CID',                     'summon_restr_hane_hane_cid'),
    (0x0804b5bc, 0x000011f5, 'MORPHING_JAR_CID',                   'summon_restr_morphing_jar_cid'),
    # A-class reuse
    (0x0804b5f8, 0x000013ad, 'SLATE_WARRIOR_CID',                  'summon_restr_slate_warrior_cid'),
    (0x0804b608, 0x000012a1, 'PARASITE_PARACIDE_CID',              'summon_restr_parasite_paracide_cid'),
    # B-class new CIDs
    (0x0804b628, 0x0000136a, 'BUBONIC_VERMIN_CID',                 'summon_restr_bubonic_vermin_cid'),
    # A-class reuse
    (0x0804b630, 0x000013ab, 'JOWLS_OF_DARK_DEMISE_CID',           'summon_restr_jowls_dark_demise_cid'),
    # B-class new CIDs
    (0x0804b654, 0x00001413, 'FOUR_STARRED_LADYBUG_OF_DOOM_CID',   'summon_restr_4star_ladybug_cid'),
    (0x0804b65c, 0x000013bd, 'SONIC_JAMMER_CID',                   'summon_restr_sonic_jammer_cid'),
    (0x0804b678, 0x00001481, 'SUMMONER_OF_ILLUSIONS_CID',          'summon_restr_summoner_illusions_cid'),
    (0x0804b688, 0x00001489, 'TORNADO_BIRD_CID',                   'summon_restr_tornado_bird_cid'),
    (0x0804b6cc, 0x0000161f, 'MAGICAL_MERCHANT_CID',               'summon_restr_magical_merchant_cid'),
    # A-class reuse
    (0x0804b6d4, 0x000014fb, 'FIBER_JAR_CID',                      'summon_restr_fiber_jar_cid'),
    (0x0804b6f4, 0x00001527, 'ROYAL_KEEPER_CID',                   'summon_restr_royal_keeper_cid'),
    # B-class new CIDs
    (0x0804b6fc, 0x00001530, 'DICE_JAR_CID',                       'summon_restr_dice_jar_cid'),
    # A-class reuse
    (0x0804b71c, 0x00001595, 'COBRA_JAR_CID',                      'summon_restr_cobra_jar_cid'),
    # B-class new CIDs
    (0x0804b72c, 0x00001590, 'A_CAT_OF_ILL_OMEN_CID',             'summon_restr_cat_ill_omen_cid'),
    (0x0804b740, 0x00001613, 'OLD_VINDICTIVE_MAGICIAN_CID',        'summon_restr_old_vindictive_mag_cid'),
    (0x0804b750, 0x00001618, 'MAGICAL_PLANT_MANDRAGOLA_CID',       'summon_restr_magical_plant_cid'),
    # A-class reuse
    (0x0804b778, 0x0000179a, 'NIGHT_ASSAILANT_CID',                'summon_restr_night_assailant_cid'),
    # B-class new CIDs
    (0x0804b78c, 0x00001689, 'IRON_BLACKSMITH_KOTETSU_CID',        'summon_restr_iron_blacksmith_cid'),
    (0x0804b7a4, 0x000016c2, 'WITCH_DOCTOR_OF_CHAOS_CID',          'summon_restr_witch_doctor_chaos_cid'),
    (0x0804b7b4, 0x0000178e, 'DESERTAPIR_CID',                     'summon_restr_desertapir_cid'),
    # A-class reuse
    (0x0804b7d0, 0x000017ee, 'OJAMA_KING_CARD_ID',                 'summon_restr_ojama_king_cid'),
    # B-class new CIDs
    (0x0804b7e0, 0x000017ea, 'NOBLEMAN_EATER_BUG_CID',             'summon_restr_nobleman_eater_cid'),
    # A-class reuse (DUMMY_GOLEM -- was listed in A with note "NEW B class"; actually new)
    (0x0804b7fc, 0x000018b5, 'DUMMY_GOLEM_CID',                    'summon_restr_dummy_golem_cid'),
    # A-class reuse
    (0x0804b810, 0x000018c2, 'CHARMER_RANGE_MAX_CID',              'summon_restr_charmer_range_max_cid'),

    # --- get_card_special_group_code (0x0804b81c) ---
    # B-class new CIDs
    (0x0804b85c, 0x00001758, 'ARCHLORD_ZERATO_CID',                'spec_grp_archlord_zerato_cid'),
    # A-class reuse
    (0x0804b860, 0x00001466, 'DARK_NECROFEAR_CID',                 'spec_grp_dark_necrofear_cid'),
    (0x0804b864, 0x0000112e, 'METALZOA_CID',                       'spec_grp_metalzoa_cid'),
    # B-class new CIDs (using existing A-class equates where noted in proposal)
    (0x0804b868, 0x00000fe5, 'HARPIE_LADY_SISTERS_CID',            'spec_grp_harpie_sisters_cid'),
    (0x0804b87c, 0x00001117, 'WALL_SHADOW_CID',                    'spec_grp_wall_shadow_cid'),
    (0x0804b880, 0x00000fe9, 'PERFECTLY_ULTIMATE_GREAT_MOTH_CID',  'spec_grp_perfect_ult_moth_cid'),
    # A-class reuse
    (0x0804b888, 0x0000111c, 'GATE_GUARDIAN_CID',                  'spec_grp_gate_guardian_cid'),
    # B-class
    (0x0804b8ac, 0x0000128c, 'RED_EYES_BLACK_METAL_DRAGON_CID',    'spec_grp_rebmd_cid'),
    (0x0804b8c0, 0x0000138a, 'VALKYRION_THE_MAGNA_WARRIOR_CID',    'spec_grp_valkyrion_cid'),
    # A-class reuse (upd_cid_13e9)
    (0x0804b8c8, 0x000013e9, 'upd_cid_13e9',                       'spec_grp_upd_13e9_cid'),
    # A-class reuse
    (0x0804b8ec, 0x00001578, 'LAVA_GOLEM_CID',                     'spec_grp_lava_golem_cid'),
    # B-class
    (0x0804b900, 0x00001534, 'FUSHIOH_RICHIE_CID',                 'spec_grp_fushioh_richie_cid'),
    # A-class reuse
    (0x0804b908, 0x0000154a, 'TOON_DARK_MAGICIAN_GIRL_CID',        'spec_grp_tdmg_cid'),
    # B-class
    (0x0804b930, 0x000016c9, 'CHAOS_SORCERER_CID',                 'spec_grp_chaos_sorcerer_cid'),
    (0x0804b948, 0x000016cb, 'BLACK_LUSTER_SOLDIER_ENVOY_CID',     'spec_grp_bls_envoy_cid'),
    (0x0804b978, 0x000018b9, 'MASTER_MONK_CID',                    'spec_grp_master_monk_cid'),
    # A-class reuse
    (0x0804b98c, 0x000017c9, 'THEINEN_THE_GREAT_SPHINX_CID',       'spec_grp_theinen_sphinx_cid'),
    (0x0804b994, 0x000017d4, 'HORUS_LV8_CID',                     'spec_grp_horus_lv8_cid'),
    # B-class
    (0x0804b9b4, 0x00001895, 'VAMPIRE_GENESIS_CID',                'spec_grp_vampire_genesis_cid'),
    # A-class reuse
    (0x0804b9bc, 0x0000186b, 'GEARFRIED_SWORDMASTER_CID',          'spec_grp_gearfried_swmaster_cid'),
    # B-class
    (0x0804b9f4, 0x000019a6, 'EHERO_NEO_BUBBLEMAN_CID',            'spec_grp_ehero_neo_bubbleman_cid'),
    (0x0804ba04, 0x00001982, 'DARK_ERADICATOR_WARLOCK_CID',        'spec_grp_dark_eradicator_cid'),
    # A-class reuse
    (0x0804ba24, 0x000019ca, 'DOOM_DOZER_CID',                     'spec_grp_doom_dozer_cid'),
    (0x0804ba3c, 0x000019cd, 'PRINCESS_PIKERU_CID',                'spec_grp_princess_pikeru_cid'),

    # --- check_card_not_equip_placement_type (0x0804ba90) ---
    (0x0804baa0, 0x000017c4, 'RARE_METAL_DRAGON_CID',              'not_equip_rare_metal_dragon_cid'),

    # --- check_card_id_is_special_tribute_group (0x0804bab8) ---
    (0x0804bae0, 0x000018f6, 'CYBER_DRAGON_CID',                   'sp_tribute_cyber_dragon_cid'),
    (0x0804bae4, 0x000015b4, 'XYZ_DRAGON_CANNON_CID',              'sp_tribute_xyz_cannon_cid'),
    (0x0804bae8, 0x00001488, 'GILASAURUS_CID',                     'sp_tribute_gilasaurus_cid'),
    (0x0804baec, 0x00001299, 'THE_FIEND_MEGACYBER_CID',            'sp_tribute_fiend_megacyber_cid'),
    (0x0804baf4, 0x000015b1, 'XY_DRAGON_CANNON_CID',               'sp_tribute_xy_cannon_cid'),
    (0x0804bb08, 0x0000164c, 'GUARDIAN_GRARL_CID',                 'sp_tribute_guardian_grarl_cid'),
    (0x0804bb14, 0x00001806, 'THE_TRICKY_CID',                     'sp_tribute_the_tricky_cid'),
    (0x0804bb34, 0x0000196e, 'FAMILIAR_POSSESSED_WYNN_CID',        'sp_tribute_familiar_wynn_cid'),
    (0x0804bb54, 0x000019aa, 'ANCIENT_GEAR_CID',                   'sp_tribute_ancient_gear_cid'),

    # --- check_card_is_equip_target_eligible (0x0804bb6c) ---
    # NOTE: 0x0804bb9c (gap 0x1729) is handled in RENAME_SLOTS only -- no .equ constant
    # A-class reuse
    (0x0804bba0, 0x000015fc, 'DARK_PALADIN_CID',                   'equip_tgt_dark_paladin_a_cid'),
    # B-class
    (0x0804bbb0, 0x000016ec, 'VICTORY_D_CID',                      'equip_tgt_victory_d_cid'),
    (0x0804bbcc, 0x000018ac, 'ANCIENT_GEAR_BEAST_CID',             'equip_tgt_ancient_gear_beast_cid'),
    (0x0804bbd0, 0x00001771, 'SKULL_DESCOVERY_KNIGHT_CID',         'equip_tgt_skull_descovery_cid'),
    (0x0804bbd8, 0x000018c9, 'ELEMENTAL_HERO_THUNDER_GIANT_CID',   'equip_tgt_ehero_thunder_giant_cid'),
    (0x0804bbfc, 0x00001987, 'ELEMENTAL_HERO_STEAM_HEALER_CID',    'equip_tgt_ehero_steam_healer_cid'),
    # A-class reuse
    (0x0804bc10, 0x00001956, 'EHERO_RAMPART_BLASTER_CARD_ID',      'equip_tgt_ehero_rampart_cid'),
    # B-class
    (0x0804bc30, 0x000019ce, 'PRINCESS_CURRAN_CID',                'equip_tgt_princess_curran_cid'),
    # A-class reuse
    (0x0804bc4c, 0x000019ef, 'EHERO_ERIKSHIELER_CID',              'equip_tgt_ehero_erikshieler_cid'),

    # --- check_card_id_is_equip_excluded_range (0x0804bc58) ---
    # A-class reuse
    (0x0804bc74, 0x000015fa, 'YZ_TANK_DRAGON_CID',                 'equip_excl_yz_tank_dragon_cid'),
    # A-class reuse
    (0x0804bc88, 0x00001954, 'VWXYZ_DRAGON_CATAPULT_CANNON_CID',   'equip_excl_vwxyz_cannon_cid'),

    # --- get_card_equip_zone_rank (0x0804bc90) ---
    # A-class reuse (DARK_PALADIN 2nd occurrence)
    (0x0804bcdc, 0x000015fc, 'DARK_PALADIN_CID',                   'equip_rank_dark_paladin_b_cid'),
    # B-class
    (0x0804bce0, 0x0000148c, 'MARYOKUTAI_CID',                     'equip_rank_maryokutai_cid'),
    # B-class
    (0x0804bce4, 0x0000111b, 'SUIJIN_CID',                         'equip_rank_suijin_cid'),
    # B-class
    (0x0804bcec, 0x000013a7, 'INJECTION_FAIRY_LILY_CID',           'equip_rank_injection_fairy_cid'),
    # A-class reuse
    (0x0804bd00, 0x000014c7, 'RYU_SENSHI_CID',                     'equip_rank_ryu_senshi_cid'),
    # B-class
    (0x0804bd2c, 0x000017c6, 'SORCERER_OF_DARK_MAGIC_CID',         'equip_rank_sorcerer_dark_magic_cid'),
    # A-class reuse
    (0x0804bd30, 0x000016b9, 'STRIKE_NINJA_CID',                   'equip_rank_strike_ninja_cid'),
    # NOTE: 0x0804bd40 (gap 0x1774) is handled in RENAME_SLOTS only -- no .equ constant
    # B-class
    (0x0804bd58, 0x0000183a, 'A_TEAM_TRAP_DISPOSAL_UNIT_CID',      'equip_rank_a_team_trap_cid'),
    # A-class reuse
    (0x0804bd6c, 0x00001906, 'WINGED_KURIBOH_LV10_CID',            'equip_rank_wk_lv10_cid'),

    # --- check_card_id_is_equip_set_a (0x0804bd78) ---
    # A-class reuse
    (0x0804bda0, 0x0000123b, 'CRUSH_CARD_CID',                     'equip_set_a_crush_card_cid'),
    (0x0804bda4, 0x00000ff9, 'CASTLE_OF_DARK_ILLUSIONS_CID',       'equip_set_a_castle_dark_ill_cid'),
    (0x0804bdb4, 0x00001009, 'PUMPKING_CID',                       'equip_set_a_pumpking_cid'),
    # B-class
    (0x0804bdc8, 0x0000130d, 'GERM_INFECTION_CID',                 'equip_set_a_germ_infection_cid'),
    (0x0804bdd8, 0x0000131a, 'STIM_PACK_CID',                      'equip_set_a_stim_pack_cid'),
    (0x0804bdf4, 0x0000169c, 'FINAL_COUNTDOWN_CID',                'equip_set_a_final_countdown_cid'),
    (0x0804bdf8, 0x0000159c, 'DIFFERENT_DIMENSION_CAPSULE_CID',    'equip_set_a_diff_dim_capsule_cid'),
    (0x0804be1c, 0x00001810, 'THE_BLOCKMAN_CID',                   'equip_set_a_the_blockman_cid'),
    # B-class
    (0x0804be30, 0x0000187c, 'SWORDS_OF_CONCEALING_LIGHT_CID',     'equip_set_a_swords_concealing_cid'),

    # --- check_card_id_is_equip_set_a (continued) ---
    # A-class reuse
    (0x0804bd9c, 0x0000149d, 'EKIBYO_DRAKMORD_CID',                'equip_set_a_ekibyo_drakmord_cid'),
]

# NOTE: The following 2 slots have gap CIDs -- they are handled in RENAME_SLOTS with RENAME only,
# NOT EQ (no .equ constant for gap CIDs).
# 0x0804bb9c = 0x00001729 check_card_is_equip_target_eligible_cid_1729
# 0x0804bd40 = 0x00001774 get_card_equip_zone_rank_cid_1774
# These entries above in EQ_SLOTS incorrectly include gap CIDs as const_name = label name
# -> Remove duplicates: gap slots appear in RENAME_SLOTS only, not EQ_SLOTS.

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, label, eol_ascii_or_None)
#    6 gap CID slots. Pure ASCII EOL.
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x0804b53c, 'get_card_field_summon_restriction_cid_14c9',
     'unassigned card slot between Warrior_Dai_Grepher(0x14c8) and Frontier_Wiseman(0x14ca)'),
    (0x0804b544, 'get_card_field_summon_restriction_cid_1051',
     'unassigned card slot between Spirit_of_the_Harp(0x1050) and Armaill(0x1052)'),
    (0x0804b9cc, 'get_card_special_group_code_cid_18a4',
     'unassigned card slot between Kaibaman(0x189a) and EHERO_Avian(0x18a6)'),
    (0x0804bb9c, 'check_card_is_equip_target_eligible_cid_1729',
     'unassigned card slot between Abyss_Soldier(0x1727) and Inferno_Hammer(0x172a)'),
    (0x0804bd10, 'get_card_equip_zone_rank_cid_158a',
     'unassigned card slot between Gravekeeper_Spear_Soldier(0x1588) and Gravekeeper_Cannonholder(0x158c)'),
    (0x0804bd40, 'get_card_equip_zone_rank_cid_1774',
     'unassigned card slot between Shield_Crash(0x1773) and Return_Zombie(0x1775)'),
]

# ---------------------------------------------------------------------------
# S. SCALAR_EQ: (instr_addr, operand_index, const_name, value)
#    Scalar equates on instruction operands (inline immediates).
#    3 movs r0,#imm CID calculations + 2 cmp r5,#imm field6 type.
#    operand_index=1 for "movs r0, #imm" (operand 0=r0, 1=#imm)
#    operand_index=1 for "cmp r5, #imm" (operand 0=r5, 1=#imm)
# ---------------------------------------------------------------------------
SCALAR_EQ = [
    # get_card_field_summon_restriction: movs r0,#0x90; lsls r0,r0,#5 => 0x1200=PENGUIN_SOLDIER
    (0x0804b5c0, 1, 'PENGUIN_SOLDIER_CID',         0x00001200),
    # get_card_equip_zone_rank: movs r0,#0xfe; lsls r0,r0,#4 => 0x0fe0=KURIBOH
    (0x0804bcd6, 1, 'KURIBOH_CID',                 0x00000fe0),
    # check_card_id_is_equip_set_a: movs r0,#0xad; lsls r0,r0,#5 => 0x15a0=DARK_SNAKE_SYNDROME
    (0x0804bdfc, 1, 'DARK_SNAKE_SYNDROME_CID',     0x000015a0),
    # check_card_id_is_equip_excluded_range: cmp r5,#0x16 => CARD_FIELD6_EQUIP_CONTINUOUS
    (0x0804bca0, 1, 'CARD_FIELD6_EQUIP_CONTINUOUS', 0x00000016),
    # check_card_id_is_equip_excluded_range: cmp r5,#0x17 => CARD_FIELD6_EQUIP_RITUAL
    (0x0804bca4, 1, 'CARD_FIELD6_EQUIP_RITUAL',    0x00000017),
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
    print("=== RefineF05Seg4aSlots (DRY=%s) ===" % DRY)
    rm      = currentProgram.getReferenceManager()
    et      = currentProgram.getEquateTable()
    listing = currentProgram.getListing()
    fm      = currentProgram.getFunctionManager()
    nA = nC = nS = 0

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

    # --- S. SCALAR_EQ ---
    for instr_addr_int, op_idx, cname, value in SCALAR_EQ:
        instr = getInstructionAt(_addr(instr_addr_int))
        if instr is None:
            print("[S FAIL] no instruction @ 0x%08x" % instr_addr_int); continue
        if DRY:
            print("[S dry] 0x%08x op[%d] scalar equate %s=0x%x" % (instr_addr_int, op_idx, cname, value))
            nS += 1; continue
        eq = et.getEquate(cname)
        if eq is None:
            eq = et.createEquate(cname, value)
        try:
            eq.addReference(_addr(instr_addr_int), op_idx)
            print("[S ok] 0x%08x op[%d] -> %s (0x%x)" % (instr_addr_int, op_idx, cname, value)); nS += 1
        except Exception as ex:
            print("[S FAIL] 0x%08x: %s" % (instr_addr_int, ex))

    print("=== DONE: EQ=%d RENAME=%d SCALAR=%d ===" % (nA, nC, nS))


main()
