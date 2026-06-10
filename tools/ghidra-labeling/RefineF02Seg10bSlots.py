# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF02Seg10bSlots.py -- file 02 Seg-10b (0x08035280..0x08035f54)
#   field activation eligibility / field-spell activation check cluster (7 functions):
#   exit_slot_activation_with_state_write / eval_slot_activation_eligibility_full /
#   count_activatable_slots_for_player / check_slot_field_spell_chain_eligible /
#   check_field_spell_trap_chain_eligible / check_player_field_spell_chain_eligible /
#   eval_slot_fieldspell_activation_full
#
# Also rewrites 1 Seg-10a CJK plate:
#   eval_slot_activation_guard_full (0x0803495c) -- CJK -> ASCII
#
# Sections:
#   A. EQ_SLOTS   -- 28 REUSE + 51 NEW  total=79
#   B. REF_SLOTS  -- 1 (gDuelCardCtxBase)
#   C. RENAME_SLOTS -- 3
#   D. PLATE_FULL -- 3 (2 Seg-10b + 1 Seg-10a CJK cleanup)
#
# New constants (already appended to constants/*.inc before running this script):
#   card_info.inc:   51 CID equates + HAMON_LORD_CID_SHIFTED
#   duel_field.inc:  FIELD5_SCORE_ACTIVATION_THRESHOLD, FIELD5_SCORE_FIELDSPELL_THRESHOLD
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).

from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.data import DWordDataType, DataTypeConflictHandler

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

# ---------------------------------------------------------------------------
# A. EQ_SLOTS: (slot_addr, value, eq_name, slot_label, eol_ascii_or_None)
#    Creates equate (value -> name) and references it from slot address.
#    Slot label MUST differ from eq_name to avoid GAS ldr/equate conflict.
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # --- Group A: REUSE existing constants ---

    # ACTIVATION_STATE_B_OFF = 0x00001d78 (duel_field.inc)
    (0x080352ac, 0x00001d78, 'ACTIVATION_STATE_B_OFF',
     'exit_slot_act_state_b_off',
     'gP1LifePoints+side*0x868+0x1d78: activation state field B'),

    # PLAYER_BLOCK_STRIDE = 0x00000868 (ewram.inc)
    (0x0803539c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'eval_slot_act_elig_stride_a', None),
    (0x08035478, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'eval_slot_act_elig_stride_b', None),
    (0x08035544, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'eval_slot_act_elig_stride_c', None),
    (0x080356c0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'eval_slot_act_elig_stride_d', None),
    (0x0803575c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'eval_slot_act_elig_stride_e', None),
    (0x080357dc, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'eval_slot_act_elig_stride_f', None),
    (0x08035934, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'eval_slot_act_elig_stride_g', None),
    (0x080359f4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_act_slots_stride', None),
    (0x08035af8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_sfsc_stride_a', None),
    (0x08035b70, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_fstc_stride', None),
    (0x08035c9c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'eval_fsact_stride_a', None),
    (0x08035e44, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'eval_fsact_stride_b', None),
    (0x08035eac, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'eval_fsact_stride_c', None),

    # gDuelFieldSlots = 0x0201c510 (ewram.inc)
    (0x080353a0, 0x0201c510, 'gDuelFieldSlots',
     'eval_slot_act_elig_gdf_a', None),
    (0x0803553c, 0x0201c510, 'gDuelFieldSlots',
     'eval_slot_act_elig_gdf_b', None),
    (0x080356bc, 0x0201c510, 'gDuelFieldSlots',
     'eval_slot_act_elig_gdf_d', None),
    (0x08035760, 0x0201c510, 'gDuelFieldSlots',
     'eval_slot_act_elig_gdf_e', None),
    (0x080357e0, 0x0201c510, 'gDuelFieldSlots',
     'eval_slot_act_elig_gdf_f', None),
    (0x08035938, 0x0201c510, 'gDuelFieldSlots',
     'eval_slot_act_elig_gdf_g', None),
    (0x080359f8, 0x0201c510, 'gDuelFieldSlots',
     'count_act_slots_gdf', None),
    (0x08035afc, 0x0201c510, 'gDuelFieldSlots',
     'check_sfsc_gdf_a', None),
    (0x08035b6c, 0x0201c510, 'gDuelFieldSlots',
     'check_fstc_gdf', None),
    (0x08035ca0, 0x0201c510, 'gDuelFieldSlots',
     'eval_fsact_gdf_a', None),
    (0x08035e48, 0x0201c510, 'gDuelFieldSlots',
     'eval_fsact_gdf_b', None),

    # UMI_CARD_ID = 0x000010f4 (card_info.inc -- already defined in Seg-10a)
    (0x08035794, 0x000010f4, 'UMI_CARD_ID',
     'eval_slot_act_elig_umi_cid',
     'Umi field spell CID; special activation check'),
    (0x08035b8c, 0x000010f4, 'UMI_CARD_ID',
     'check_fstc_umi_cid', None),
    (0x08035e58, 0x000010f4, 'UMI_CARD_ID',
     'eval_fsact_umi_cid', None),

    # --- Group B: NEW card_info.inc equates ---

    (0x08035cc0, 0x0000114c, 'JINZO_7_CID',
     'eval_fsact_jinzo7_cid',
     'Jinzo #7 CID 0x114c; fieldspell eligibility BST'),
    (0x08035454, 0x00001318, 'RING_OF_MAGNETISM_CID',
     'eval_slot_act_elig_rom_cid',
     'Ring of Magnetism CID 0x1318; activation elig'),
    (0x08035f24, 0x000013ab, 'JOWLS_OF_DARK_DEMISE_CID',
     'eval_fsact_jdd_cid',
     'Jowls of Dark Demise CID 0x13ab; fieldspell chain'),
    (0x08035ca4, 0x000013b3, 'SERVANT_OF_CATABOLISM_CID',
     'eval_fsact_soc_cid',
     'Servant of Catabolism CID 0x13b3; fieldspell BST'),
    (0x08035764, 0x000013cd, 'LEGENDARY_FISHERMAN_CID',
     'eval_slot_act_elig_lf_cid',
     'The Legendary Fisherman CID 0x13cd; chain check'),
    (0x08035b74, 0x000013cd, 'LEGENDARY_FISHERMAN_CID',
     'check_fstc_lf_cid', None),
    (0x08035928, 0x000014c6, 'MARAUDING_CAPTAIN_CID',
     'eval_slot_act_elig_mc_cid',
     'Marauding Captain CID 0x14c6; activation elig'),
    (0x08035948, 0x000014d4, 'A_FEINT_PLAN_CID',
     'eval_slot_act_elig_afp_cid',
     'A Feint Plan CID 0x14d4; activation elig'),
    (0x080359fc, 0x0000147d, 'ZOMBYRA_THE_DARK_CID',
     'eval_fsact_zombyra_cid',
     'Zombyra the Dark CID 0x147d; fieldspell chain'),
    (0x080353a4, 0x00001505, 'ASURA_PRIEST_CID',
     'eval_slot_act_elig_ap_cid',
     'Asura Priest CID 0x1505; activation elig BST'),
    (0x08035a14, 0x0000154a, 'TOON_DARK_MAGICIAN_GIRL_CID',
     'eval_fsact_tdmg_cid',
     'Toon Dark Magician Girl CID 0x154a'),
    (0x08035758, 0x0000154a, 'TOON_DARK_MAGICIAN_GIRL_CID',
     'eval_slot_act_elig_tdmg_cid', None),
    (0x08035d3c, 0x00001566, 'TOON_GOBLIN_AF_CID',
     'eval_fsact_tgaf_cid',
     'Toon Goblin Attack Force CID 0x1566; fieldspell BST'),
    (0x08035c90, 0x00001561, 'TOON_DEFENSE_CID',
     'eval_fsact_td_cid',
     'Toon Defense CID 0x1561; zone chain filter'),
    (0x08035d18, 0x00001598, 'REAPER_ON_NIGHTMARE_CID',
     'eval_fsact_ron_cid',
     'Reaper on the Nightmare CID 0x1598; fieldspell BST'),
    (0x08035d5c, 0x000015ba, 'DRILLAGO_CID',
     'eval_fsact_drillago_cid',
     'Drillago CID 0x15ba; fieldspell BST'),
    (0x08035f28, 0x000015cf, 'KIRYU_CID',
     'eval_fsact_kiryu_cid',
     'Kiryu CID 0x15cf; fieldspell chain filter'),
    (0x080353a8, 0x000015ea, 'RAREGOLD_ARMOR_CID',
     'eval_slot_act_elig_rga_cid',
     'Raregold Armor CID 0x15ea; activation elig'),
    (0x08035af4, 0x000015ff, 'DIFFUSION_WAVE_MOTION_CID',
     'eval_slot_act_elig_dwm_cid',
     'Diffusion Wave-Motion CID 0x15ff; activation elig'),
    (0x080356c4, 0x00001703, 'PRICKLE_FAIRY_CID',
     'eval_slot_act_elig_pf_cid',
     'Prickle Fairy CID 0x1703; activation elig BST'),
    (0x080356c8, 0x0000160f, 'AMAZONESS_TIGER_CID',
     'eval_slot_act_elig_at_cid',
     'Amazoness Tiger CID 0x160f; activation elig BST'),
    (0x08035b04, 0x00001619, 'MAGICAL_SCIENTIST_CID',
     'eval_slot_act_elig_ms_cid',
     'Magical Scientist CID 0x1619; fieldspell chain'),
    (0x08035418, 0x00001644, 'BERSERK_DRAGON_CID',
     'eval_slot_act_elig_bd_cid',
     'Berserk Dragon CID 0x1644; activation elig BST'),
    (0x08035a38, 0x00001644, 'BERSERK_DRAGON_CID',
     'eval_fsact_bd_cid', None),
    (0x08035778, 0x0000164e, 'GUARDIAN_KAYEST_CID',
     'eval_slot_act_elig_gk_cid',
     'Guardian Kay\'est CID 0x164e; activation/trap chain'),
    (0x08035b78, 0x0000164e, 'GUARDIAN_KAYEST_CID',
     'check_fstc_gk_cid', None),
    (0x08035f40, 0x0000165d, 'SHOOTING_STAR_BOW_CID',
     'eval_fsact_ssb_cid',
     'Shooting Star Bow - Ceal CID 0x165d; fieldspell chain'),
    (0x08035424, 0x00001561, 'TOON_DEFENSE_CID',
     'eval_slot_act_elig_td_cid',
     'Toon Defense CID 0x1561; activation elig'),
    (0x0803542c, 0x00001669, 'STAUNCH_DEFENDER_CID',
     'eval_slot_act_elig_sd_cid',
     'Staunch Defender CID 0x1669; activation elig'),
    (0x08035b0c, 0x00001669, 'STAUNCH_DEFENDER_CID',
     'eval_slot_act_elig_sd_cid_b', None),
    (0x080356cc, 0x0000168c, 'VILEPAWN_ARCHFIEND_CID',
     'eval_slot_act_elig_va_cid',
     'Vilepawn Archfiend CID 0x168c; activation elig BST'),
    (0x08035f2c, 0x0000169b, 'CHECKMATE_CID',
     'eval_fsact_checkmate_cid',
     'Checkmate CID 0x169b; fieldspell chain filter'),
    (0x08035f30, 0x000016a3, 'DARK_SCORPION_COMBO_CID',
     'eval_fsact_dsc_cid',
     'Dark Scorpion Combination CID 0x16a3; fieldspell chain'),
    (0x080357e4, 0x000016ed, 'MAGICIANS_VALKYRIE_CID',
     'eval_slot_act_elig_mv_cid',
     "Magician's Valkyrie CID 0x16ed; activation elig BST"),
    (0x08035d60, 0x00001701, 'BLACK_TYRANNO_CID',
     'eval_fsact_bt_cid',
     'Black Tyranno CID 0x1701; fieldspell BST'),
    (0x08035d58, 0x00001705, 'AMPHIBIOUS_BUGROTH_MK3_CID',
     'eval_fsact_abm3_cid',
     'Amphibious Bugroth MK-3 CID 0x1705; fieldspell BST'),
    (0x0803554c, 0x00001756, 'SOLAR_FLARE_DRAGON_CID',
     'eval_slot_act_elig_sfd_cid',
     'Solar Flare Dragon CID 0x1756; activation elig BST'),
    (0x08035f3c, 0x00001759, 'OPTI_CAMO_ARMOR_CID',
     'eval_fsact_oca_cid',
     'Opti-Camouflage Armor CID 0x1759; fieldspell chain'),
    (0x08035930, 0x00001770, 'MARSHMALLON_CID',
     'eval_slot_act_elig_marsh_cid',
     'Marshmallon CID 0x1770; activation elig BST'),
    (0x0803592c, 0x00001777, 'MARSHMALLON_GLASSES_CID',
     'eval_slot_act_elig_mg_cid',
     'Marshmallon glasses CID 0x1777; activation elig'),
    (0x08035560, 0x0000179d, 'EMISSARY_OF_OASIS_CID',
     'eval_slot_act_elig_eo_cid',
     'Emissary of the Oasis CID 0x179d; activation elig BST'),
    (0x08035f34, 0x000017aa, 'DELTA_ATTACKER_CID',
     'eval_fsact_da_cid',
     'Delta Attacker CID 0x17aa; fieldspell chain'),
    (0x08035540, 0x000017fc, 'TAUNT_CID',
     'eval_slot_act_elig_taunt_cid',
     'Taunt CID 0x17fc; activation elig BST'),
    (0x08035548, 0x000015ea, 'RAREGOLD_ARMOR_CID',
     'eval_slot_act_elig_rga_cid_b', None),
    (0x08035b00, 0x000017fc, 'TAUNT_CID',
     'eval_slot_act_elig_taunt_cid_b', None),
    (0x08035c94, 0x00001852, 'ASTRAL_BARRIER_CID',
     'eval_fsact_ab_cid',
     'Astral Barrier CID 0x1852; zone chain filter'),
    (0x08035428, 0x00001852, 'ASTRAL_BARRIER_CID',
     'eval_slot_act_elig_ab_cid',
     'Astral Barrier CID 0x1852; activation elig'),
    (0x08035d88, 0x0000186d, 'SHADOWSLAYER_CID',
     'eval_fsact_shadowslayer_cid',
     'Shadowslayer CID 0x186d; fieldspell BST'),
    (0x08035b08, 0x00001890, 'UNION_ATTACK_CID',
     'eval_slot_act_elig_ua_cid',
     'Union Attack CID 0x1890; fieldspell chain'),
    (0x08035f38, 0x00001893, 'OVERPOWERING_EYE_CID',
     'eval_fsact_oe_cid',
     'Overpowering Eye CID 0x1893; fieldspell chain filter'),
    (0x0803593c, 0x000017fd, 'ABSOLUTE_END_CID',
     'eval_slot_act_elig_ae_cid',
     'Absolute End CID 0x17fd; activation elig'),
    (0x08035c98, 0x000017fd, 'ABSOLUTE_END_CID',
     'eval_fsact_ae_cid', None),
    (0x08035940, 0x000018b1, 'HIERACOSPHINX_CID',
     'eval_slot_act_elig_hs_cid',
     'Hieracosphinx CID 0x18b1; activation elig BST'),
    (0x0803577c, 0x000018b6, 'GRAVE_OHJA_CID',
     'eval_slot_act_elig_go_cid',
     'Grave Ohja CID 0x18b6; activation elig'),
    (0x0803541c, 0x00001958, 'EHERO_WILDEDGE_CID',
     'eval_slot_act_elig_ew_cid',
     'EHERO Wildedge CID 0x1958; activation elig BST'),
    (0x08035420, 0x00001505, 'ASURA_PRIEST_CID',
     'eval_slot_act_elig_ap_cid_b', None),
    (0x08035a3c, 0x00001958, 'EHERO_WILDEDGE_CID',
     'eval_fsact_ew_cid', None),
    (0x08035a40, 0x00001505, 'ASURA_PRIEST_CID',
     'eval_fsact_ap_cid',
     'Asura Priest CID 0x1505; fieldspell BST'),
    (0x08035b10, 0x0000195b, 'FEATHER_SHOT_CID',
     'eval_slot_act_elig_fs_cid',
     'Feather Shot CID 0x195b; fieldspell chain'),
    (0x08035d78, 0x0000182d, 'RAGING_FLAME_SPRITE_CID',
     'eval_fsact_rfs_cid',
     'Raging Flame Sprite CID 0x182d; fieldspell BST'),
    (0x08035ce0, 0x00001295, 'GEAR_GOLEM_CID',
     'eval_fsact_gg_cid',
     'Gear Golem the Moving Fortress CID 0x1295; fieldspell BST'),
    (0x08035cf4, 0x000012a5, 'BLUE_EYES_TOON_DRAGON_CID',
     'eval_slot_act_elig_betd_cid',
     'Blue-Eyes Toon Dragon CID 0x12a5; activation elig'),
    (0x080356d4, 0x000012a5, 'BLUE_EYES_TOON_DRAGON_CID',
     'eval_slot_act_elig_betd_cid_b', None),
    (0x08035a00, 0x0000127d, 'MANGA_RYU_RAN_CID',
     'eval_fsact_mrr_cid',
     'Manga Ryu-Ran CID 0x127d; fieldspell chain'),

    # --- Group C: NEW duel_field.inc equates ---

    (0x080356d0, 0x0000076b, 'FIELD5_SCORE_ACTIVATION_THRESHOLD',
     'eval_slot_act_elig_field5_thresh',
     'get_slot_field5_score > this -> not activatable; 8 raw refs'),
    (0x08035e4c, 0x0000063f, 'FIELD5_SCORE_FIELDSPELL_THRESHOLD',
     'eval_fsact_field5_thresh',
     'get_slot_field5_score <= this -> not activatable; 3 raw refs'),

    # --- Group D: NEW HAMON_LORD_CID_SHIFTED sentinel ---

    (0x08035944, 0xcd200000, 'HAMON_LORD_CID_SHIFTED',
     'eval_slot_act_elig_hamon_shifted',
     'HAMON_LORD_CID<<19; slot_word<<19 sentinel check'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_vaddr, gas_label, slot_label, eol_or_None)
#    Creates USER_DEFINED label at target, DATA ref from slot, renames slot.
# ---------------------------------------------------------------------------
REF_SLOTS = [
    (0x080352a4, 0x0201e2a0, 'gDuelCardCtxBase',
     'exit_slot_act_dctxbase',
     'gDuelCardCtxBase[+4]=player_activation_idx; read in exit_slot_activation_with_state_write'),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
#    Plain rename + optional EOL comment (pure ASCII, no CJK).
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x080352a8, 'exit_slot_act_gp1lp', None),
    (0x08035ca8, 'eval_fsact_unknown_cid_1221',
     'unknown field-spell eligibility CID 0x1221; no card-stats entry between Night Lizard(0x1220) and Blue-Winged Crown(0x1222)'),
]

# ---------------------------------------------------------------------------
# D. PLATE_FULL: (func_addr, new_plate_ascii_str)
#    Full plate comment replacement (pure ASCII only, no CJK).
# ---------------------------------------------------------------------------
PLATE_FULL = [
    # PLATE-1: eval_slot_activation_eligibility_full (0x080352b0)
    # Replaces CJK plate. Trimmed to <= 500 chars.
    (0x080352b0,
     "Comprehensive field activation eligibility check for slot (player_side=r0, slot_idx=r1). Evaluates"
     " effect/fieldspell eligibility masks; checks zone 0xb chain; branches by opponent slot card_id testing"
     " ~28 specific card IDs (Diffusion Wave-Motion/Asura Priest/Berserk Dragon/EHERO Wildedge/Toon"
     " Defense/Astral Barrier/Staunch Defender/Ring of Magnetism/Taunt/Raregold Armor/Solar Flare Dragon/"
     "Emissary of Oasis/Prickle Fairy/Amazoness Tiger/Vilepawn Archfiend/Blue-Eyes Toon/Toon DM Girl/"
     "Marauding Captain/Marshmallon glasses/Marshmallon/Hieracosphinx/A Feint Plan/Zombyra/Manga Ryu-Ran/"
     "Magical Scientist/Union Attack/Feather Shot/Magician's Valkyrie). Hamon check via lsls#19 sentinel"
     " 0xcd200000==HAMON_LORD_CID<<19. field5_score threshold 0x76b. indeg=2. Returns 0/1."
    ),

    # PLATE-2: eval_slot_fieldspell_activation_full (0x08035bc8)
    # Replaces CJK plate. Trimmed to <= 500 chars.
    (0x08035bc8,
     "Full field-spell activation check for slot (player_side=r0, slot_idx via r8 caller-save). Calls"
     " check_slot_card_fieldspell_eligibility + check_slot_field_spell_chain_eligible; queries zone chains"
     " for Toon Defense(0x1561)/Astral Barrier(0x1852)/Absolute End(0x17fd)/Taunt(0x17fc); branches by"
     " opponent slot card_id (~21 specific cards incl. Jinzo#7/Gear Golem/Reaper on Nightmare/Toon Goblin"
     " AF/Drillago/Black Tyranno/Raging Flame Sprite/Shadowslayer/Jowls of Dark Demise/Kiryu/Checkmate/Dark"
     " Scorpion Combo/Delta Attacker/Overpowering Eye/Opti-Camo Armor/Shooting Star Bow-Ceal). Calls"
     " get_slot_field5_score (threshold 0x63f). Returns 0/1/2. indeg=1. Constants: PLAYER_BLOCK_STRIDE=0x868."
    ),

    # PLATE-3: eval_slot_activation_guard_full (0x0803495c) -- Seg-10a CJK cleanup
    # Current plate contains CJK. Rewrite to ASCII preserving semantics.
    (0x0803495c,
     "Hub for zone activation evaluation (indeg=9): checks if slot (player_side=r0, slot_idx=r1) can"
     " activate an effect. Calls check_slot_card_activatable first; returns 0 on fail. Then tries"
     " check_player_field_spell_chain_eligible and eval_slot_fieldspell_activation_full; returns 1 if"
     " either passes. If both fail, iterates 5 slots calling eval_slot_activation_eligibility_full for"
     " full effect eligibility. Returns 0 if all fail. Constants: gDuelFieldSlots=0x0201c510,"
     " player_stride=0x868, slot_count=[0..4]."
    ),
]

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
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

def _apply_ref(slot_addr, target_vaddr, gas_label, slot_label, eol):
    sa = _addr(slot_addr)
    ta = _addr(target_vaddr)
    sym_tbl = currentProgram.getSymbolTable()
    ref_mgr = currentProgram.getReferenceManager()

    if DRY:
        print("[dry] REF 0x%08x -> 0x%08x  %s  slot=%s" % (slot_addr, target_vaddr, gas_label, slot_label))
        return

    # create USER_DEFINED label at target if not already there
    tgt_syms = sym_tbl.getSymbols(ta)
    tgt_names = [s.getName() for s in tgt_syms]
    if gas_label not in tgt_names:
        sym_tbl.createLabel(ta, gas_label, SourceType.USER_DEFINED)

    # add DATA ref from slot to target
    ref_mgr.addMemoryReference(sa, ta, RefType.DATA, SourceType.USER_DEFINED, 0)
    # set primary
    for ref in ref_mgr.getReferencesFrom(sa):
        if ref.getToAddress().equals(ta):
            ref_mgr.setPrimary(ref, True)

    # create slot label
    s_syms = sym_tbl.getSymbols(sa)
    s_names = [s.getName() for s in s_syms]
    if slot_label not in s_names:
        sym_tbl.createLabel(sa, slot_label, SourceType.USER_DEFINED)

    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(sa)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[REF] 0x%08x -> 0x%08x  %s  slot=%s" % (slot_addr, target_vaddr, gas_label, slot_label))

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
    """Replace entire plate comment at func_addr with new_plate (pure ASCII).
    After setting, reads back and verifies no FUN_[0-9a-f]{8} remains.
    Also verifies no non-ASCII characters.
    """
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

    # Readback verification
    readback = cu.getComment(CodeUnit.PLATE_COMMENT)
    if readback is None:
        print("[WARN] plate_full 0x%08x: readback returned None" % func_addr)
        return

    import re
    stale = re.findall(r'FUN_[0-9a-fA-F]{8}', readback)
    if stale:
        print("[FAIL] plate_full 0x%08x: stale FUN_ still present: %s" % (func_addr, stale))
    else:
        # Check for non-ASCII
        non_ascii = [c for c in readback if ord(c) > 127]
        if non_ascii:
            print("[FAIL] plate_full 0x%08x: non-ASCII chars in plate: %s" % (
                func_addr, [hex(ord(c)) for c in non_ascii[:5]]))
        else:
            print("[PLF] 0x%08x: plate replaced OK, no stale FUN_, no non-ASCII (len=%d)" % (
                func_addr, len(new_plate)))

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF02Seg10bSlots (DRY=%s) ===" % DRY)
    print("  Seg-10b: 0x08035280..0x08035f54, 7 fn, 98 residual slots")
    print("  +1 Seg-10a CJK plate cleanup: eval_slot_activation_guard_full (0x0803495c)")
    print("  EQ=%d REF=%d RENAME=%d PLATE_FULL=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATE_FULL)))

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    eq_ok = 0
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        _apply_eq(slot_addr, value, eq_name, slot_label, eol)
        eq_ok += 1
    print("  EQ done: %d" % eq_ok)

    # B. REF_SLOTS
    print("\n--- B. REF_SLOTS (%d) ---" % len(REF_SLOTS))
    ref_ok = 0
    for entry in REF_SLOTS:
        slot_addr, target_vaddr, gas_label, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        _apply_ref(slot_addr, target_vaddr, gas_label, slot_label, eol)
        ref_ok += 1
    print("  REF done: %d" % ref_ok)

    # C. RENAME_SLOTS
    print("\n--- C. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    ren_ok = 0
    for entry in RENAME_SLOTS:
        slot_addr, slot_label = entry[0], entry[1]
        eol = entry[2] if len(entry) > 2 else None
        _apply_rename(slot_addr, slot_label, eol)
        ren_ok += 1
    print("  RENAME done: %d" % ren_ok)

    # D. PLATE_FULL
    print("\n--- D. PLATE_FULL (%d) ---" % len(PLATE_FULL))
    for func_addr, new_plate in PLATE_FULL:
        _apply_plate_full(func_addr, new_plate)

    print("\n=== RefineF02Seg10bSlots DONE ===")
    print("  EQ=%d  REF=%d  RENAME=%d  PLATE_FULL=%d  carve=0  disasm=0" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATE_FULL)))

main()
