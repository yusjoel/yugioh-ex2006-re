# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF11Seg3bSlots.py -- f11 Seg-3b slot symbolization [0x080872e4..0x08087d58)
#
# 15 named functions: write_equip_zone_entries_by_lv_card_id,
#   populate_equip_zone_entries_substate_e_by_pair, scan_zone_equip_target_eligible_substate_c,
#   write_all_equip_zone_entries_substate_c, scan_zone_gadget_pair_check_substate_d,
#   scan_zone_equip_category_match_substate_e, scan_zone_field5_atk_bound_substate_d,
#   scan_zone_chimera_pair_check_substate_e, scan_zone_field6_eq_eval_placement_substate_b,
#   scan_zone_parasite_node_check_substate_d, scan_zone_labyrinth_pair_placement_substate_d,
#   scan_zone_field6_one_placement_substate_b, scan_player_zone_equip_criteria_substate_c,
#   scan_both_players_field5_eligible_substate_e, scan_zone_opponent_field5_substate_e
#
# EQ=82 (10 NEW CID in card_info.inc + 72 REUSE) + REF=10 + RENAME=13 = 105 slots (100% coverage)
# PLATE=14: 14 full rewrites (all ASCII, all <=490 chars)
# FUNC_RENAME=0, carve=0, disasm=0
#
# NOTE: All EOL/plate text is pure ASCII (no CJK). Ghidra Jython mojibake prevention.
# NOTE: PLATE WARN=FAIL: if setComment fails or pattern not found, report FAIL.
# NOTE: REF globals (gP1FieldArrayCBase/gP1SlotSetCodeArray/gP1HandSlotArray/gP1ChainZoneArray/
#       PLAYER_BLOCK_STRIDE) are defined in constants/ewram.inc.

from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _check(slot_addr, expected_val, name='?'):
    mem = currentProgram.getMemory()
    try:
        actual = mem.getInt(_addr(slot_addr)) & 0xFFFFFFFF
        if actual != (expected_val & 0xFFFFFFFF):
            print("FAIL value @0x%08x %s: expected=0x%08x actual=0x%08x" % (
                slot_addr, name, expected_val & 0xFFFFFFFF, actual))
            return False
    except Exception as e:
        print("FAIL read @0x%08x %s: %s" % (slot_addr, name, e))
        return False
    return True


def _apply_eq(slot_addr, value, eq_name, slot_label, eol=None):
    if not _check(slot_addr, value, eq_name):
        return False
    if DRY:
        print("[dry] EQ 0x%08x  %s=0x%x  label=%s" % (slot_addr, eq_name, value, slot_label))
        return True
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()
    eq_tbl = currentProgram.getEquateTable()
    eq = eq_tbl.getEquate(eq_name)
    if eq is None:
        eq = eq_tbl.createEquate(eq_name, value & 0xFFFFFFFFFFFFFFFFL)
    eq.addReference(a, 0)
    names = [s.getName() for s in sym_tbl.getSymbols(a)]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)
    for s in sym_tbl.getSymbols(a):
        if s.getName() == slot_label:
            s.setPrimary()
            break
    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)
    print("[EQ ] 0x%08x  %s  -> %s" % (slot_addr, eq_name, slot_label))
    return True


def _apply_ref(slot_addr, target_val, gas_label, slot_label, eol=None):
    """Apply USER label to slot + add memory reference to target."""
    if not _check(slot_addr, target_val, gas_label):
        return False
    if DRY:
        print("[dry] REF 0x%08x  target=0x%08x  gas_label=%s  slot_label=%s" % (
            slot_addr, target_val, gas_label, slot_label))
        return True
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()
    names = [s.getName() for s in sym_tbl.getSymbols(a)]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)
    for s in sym_tbl.getSymbols(a):
        if s.getName() == slot_label:
            s.setPrimary()
            break
    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)
    print("[REF] 0x%08x  target=0x%08x  -> %s" % (slot_addr, target_val, slot_label))
    return True


def _apply_rename(slot_addr, slot_label, eol=None):
    if DRY:
        print("[dry] RENAME 0x%08x -> %s" % (slot_addr, slot_label))
        return True
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()
    names = [s.getName() for s in sym_tbl.getSymbols(a)]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)
    for s in sym_tbl.getSymbols(a):
        if s.getName() == slot_label:
            s.setPrimary()
            break
    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)
    print("[REN] 0x%08x  -> %s" % (slot_addr, slot_label))
    return True


def _apply_plate_full(fn_addr, plate_text):
    """Full plate overwrite."""
    if DRY:
        print("[dry] PLATE_FULL 0x%08x  len=%d" % (fn_addr, len(plate_text)))
        return True
    a = _addr(fn_addr)
    cu = currentProgram.getListing().getCodeUnitAt(a)
    if cu is None:
        print("FAIL PLATE_FULL 0x%08x: no code unit (WARN=FAIL)" % fn_addr)
        return False
    try:
        cu.setComment(CodeUnit.PLATE_COMMENT, plate_text)
        print("[PLT_FULL] 0x%08x OK  len=%d" % (fn_addr, len(plate_text)))
        return True
    except Exception as e:
        print("FAIL PLATE_FULL 0x%08x: %s (WARN=FAIL)" % (fn_addr, e))
        return False


# ---------------------------------------------------------------------------
# A. EQ_SLOTS: (slot_addr, value, const_name, slot_label, eol_or_None)
#    82 total EQ slots: 67 CID + 15 PLAYER_BLOCK_STRIDE
# ---------------------------------------------------------------------------

# ===== CID slots (67) =====

# write_equip_zone_entries_by_lv_card_id (0x080872e4)
# 44 CID slots in BST for LV-card pairs + Elegant Egotist

CID_SLOTS = [
    # -- write_equip_zone_entries_by_lv_card_id (0x080872e4) --
    (0x08087338, 0x000017d7, 'MYSTIC_SWORDSMAN_LV2_CID',     'lv_cid_87338'),
    (0x0808733c, 0x000010e4, 'ELEGANT_EGOTIST_CID',          'lv_cid_8733c'),
    (0x08087340, 0x00000fb6, 'TIME_WIZARD_CID',               'lv_cid_87340'),
    (0x08087350, 0x00001529, 'GREAT_DEZARD_CID',              'lv_cid_87350'),
    (0x0808736c, 0x0000165a, 'A_DEAL_WITH_DARK_RULER_CID',   'lv_cid_8736c'),
    (0x0808737c, 0x0000167e, 'SAGES_STONE_CID',              'lv_cid_8737c'),
    (0x080873a4, 0x000017d1, 'ULTIMATE_INSECT_LV1_CID',      'lv_cid_873a4'),
    (0x080873ac, 0x000017c9, 'THEINEN_THE_GREAT_SPHINX_CID', 'lv_cid_873ac'),
    (0x080873c8, 0x000017d3, 'HORUS_LV6_CID',                'lv_cid_873c8'),
    (0x080873fc, 0x00001822, 'ULTIMATE_INSECT_LV3_CID',      'lv_cid_873fc'),
    (0x08087418, 0x00001814, 'SILENT_SWORDSMAN_LV5_CID',     'lv_cid_87418'),
    (0x0808741c, 0x00001812, 'SILENT_SWORDSMAN_LV3_CID',     'lv_cid_8741c'),
    (0x0808742c, 0x00001817, 'SILENT_MAGICIAN_LV4_CID',      'lv_cid_8742c'),
    (0x08087450, 0x00001907, 'TRANSCENDENT_WINGS_CID',       'lv_cid_87450'),
    (0x08087460, 0x0000187e, 'RELEASE_RESTRAINT_CID',        'lv_cid_87460'),
    (0x0808747c, 0x000019b5, 'ATTACK_REFLECTOR_UNIT_CID',    'lv_cid_8747c'),
    (0x0808748c, 0x000019d8, 'TRIAL_OF_THE_PRINCESSES_CID',  'lv_cid_8748c'),
    (0x08087494, 0x0000146e, 'DARK_SAGE_CID',                'lv_cid_87494'),
    (0x080874a4, 0x00000fe4, 'HARPIE_LADY_CID',              'lv_cid_874a4'),
    (0x080874ac, 0x00001534, 'FUSHIOH_RICHIE_CID',           'lv_cid_874ac'),
    (0x080874b4, 0x00000fa7, 'BLUE_EYES_WHITE_DRAGON_CID',   'lv_cid_874b4'),
    (0x080874bc, 0x00001643, 'MIRAGE_KNIGHT_CID',            'lv_cid_874bc'),
    (0x080874c4, 0x00001644, 'BERSERK_DRAGON_CID',           'lv_cid_874c4'),
    (0x080874cc, 0x00000fc9, 'DARK_MAGICIAN_CID_0FC9',       'lv_cid_874cc'),
    (0x080874d4, 0x0000173d, 'MYSTICAL_SHINE_BALL_CID',      'lv_cid_874d4'),
    (0x080874dc, 0x00001788, 'SPIRIT_OF_PHARAOH_CID',        'lv_cid_874dc'),
    (0x080874e4, 0x00001822, 'ULTIMATE_INSECT_LV3_CID',      'lv_cid_874e4'),
    (0x080874ec, 0x0000185e, 'ULTIMATE_INSECT_LV5_CID',      'lv_cid_874ec'),
    (0x080874f4, 0x000018af, 'ULTIMATE_INSECT_LV7_CID',      'lv_cid_874f4'),
    (0x080874fc, 0x000017d4, 'HORUS_LV8_CID',                'lv_cid_874fc'),
    (0x08087504, 0x000017d6, 'DARK_MIMIC_LV3_CID',           'lv_cid_87504'),
    (0x0808750c, 0x000017d8, 'MYSTIC_SWORDSMAN_LV4_CID',     'lv_cid_8750c'),
    (0x08087514, 0x00001823, 'MYSTIC_SWORDSMAN_LV6_CID',     'lv_cid_87514'),
    (0x0808751c, 0x000017da, 'ARMED_DRAGON_LV5_CID',         'lv_cid_8751c'),
    (0x08087524, 0x000017db, 'ARMED_DRAGON_LV7_CID',         'lv_cid_87524'),
    (0x0808753c, 0x00001816, 'SILENT_SWORDSMAN_LV7_CID',     'lv_cid_8753c'),
    (0x08087544, 0x0000181a, 'SILENT_MAGICIAN_LV8_CID',      'lv_cid_87544'),
    (0x0808754c, 0x0000185c, 'SACRED_PHOENIX_CID',           'lv_cid_8754c'),
    (0x08087554, 0x0000186b, 'GEARFRIED_SWORDMASTER_CID',    'lv_cid_87554'),
    (0x0808755c, 0x00001906, 'WINGED_KURIBOH_LV10_CID',      'lv_cid_8755c'),
    (0x08087568, 0x000019a8, 'CYBER_BARRIER_DRAGON_CID',     'lv_cid_87568'),
    (0x0808757c, 0x00001757, 'WHITE_MAGICIAN_PIKERU_CID',    'lv_cid_8757c'),
    (0x08087580, 0x0000191d, 'EBON_MAGICIAN_CURRAN_CID',     'lv_cid_87580'),
    (0x08087588, 0x000019cd, 'PRINCESS_PIKERU_CID',          'lv_cid_87588'),

    # -- populate_equip_zone_entries_substate_e_by_pair (0x0808767c) --
    (0x080876d8, 0x000012e5, 'POLYMERIZATION_CID',           'poly_cid_876d8'),

    # -- scan_zone_gadget_pair_check_substate_d (0x08087794) --
    (0x080877b4, 0x0000139d, 'BIRDFACE_CID',                 'gadget_cid_877b4'),
    (0x080877b8, 0x00001293, 'BERFOMET_CID',                 'gadget_cid_877b8'),
    (0x080877d0, 0x0000180b, 'RED_GADGET_CID',               'gadget_cid_877d0'),
    (0x080877d4, 0x00001807, 'GREEN_GADGET_CID',             'gadget_cid_877d4'),
    (0x080877e0, 0x0000180c, 'YELLOW_GADGET_CID',            'gadget_cid_877e0'),
    (0x080877e8, 0x000012e5, 'POLYMERIZATION_CID',           'gadget_cid_877e8'),
    (0x080877f0, 0x00001291, 'GAZELLE_CID',                  'gadget_cid_877f0'),
    (0x080877f8, 0x00000fe4, 'HARPIE_LADY_CID',              'gadget_cid_877f8'),
    (0x08087804, 0x0000180c, 'YELLOW_GADGET_CID',            'gadget_cid_87804'),
    (0x0808780c, 0x00001807, 'GREEN_GADGET_CID',             'gadget_cid_8780c'),

    # -- scan_zone_field5_atk_bound_substate_d (0x080878c8) --
    (0x08087964, 0x000005dc, 'CARD_STAT_LP_THRESHOLD_1500',  'atk_thr_87964'),
    (0x08087968, 0x000012a1, 'zone_query_hand_tag_12a1',     'zone_qtag_87968'),

    # -- scan_zone_chimera_pair_check_substate_e (0x0808796c) --
    (0x08087988, 0x00001294, 'CHIMERA_FLYING_MYTHICAL_BEAST_CID', 'chimera_cid_87988'),
    (0x0808798c, 0x00001631, 'MIRACLE_RESTORING_CID',        'chimera_cid_8798c'),
    (0x08087998, 0x00001291, 'GAZELLE_CID',                  'chimera_cid_87998'),
    (0x080879c8, 0x00000fc9, 'DARK_MAGICIAN_CID_0FC9',       'chimera_cid_879c8'),
    (0x080879cc, 0x00001377, 'BUSTER_BLADER_CID',            'chimera_cid_879cc'),

    # -- scan_zone_parasite_node_check_substate_d (0x08087a80) --
    (0x08087afc, 0x000012a1, 'PARASITE_PARACIDE_CID',        'para_cid_87afc'),

    # -- scan_zone_labyrinth_pair_placement_substate_d (0x08087b00) --
    (0x08087b18, 0x00001232, 'MAGICAL_LABYRINTH_CID',        'lab_cid_87b18'),
    (0x08087b20, 0x00001117, 'WALL_SHADOW_CID',              'lab_cid_87b20'),
    (0x08087b98, 0x00000fc9, 'DARK_MAGICIAN_CID_0FC9',       'lab_cid_87b98'),

    # -- write_equip_zone_entries_by_lv_card_id (0x080872e4) -- (Princess Curran, far end of pool)
    (0x08087668, 0x000019ce, 'PRINCESS_CURRAN_CID',          'lv_cid_87668'),
]

# ===== PLAYER_BLOCK_STRIDE slots (15) =====

STRIDE_SLOTS = [
    (0x08087670, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_87670'),
    (0x080876d4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_876d4'),
    (0x08087750, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_87750'),
    (0x08087790, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_87790'),
    (0x0808786c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8786c'),
    (0x080878c4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_878c4'),
    (0x0808795c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8795c'),
    (0x080879d4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_879d4'),
    (0x08087a78, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_87a78'),
    (0x08087af4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_87af4'),
    (0x08087ba0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_87ba0'),
    (0x08087bec, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_87bec'),
    (0x08087c48, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_87c48'),
    (0x08087ce8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_87ce8'),
    (0x08087d54, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_87d54'),
]

EQ_SLOTS = CID_SLOTS + STRIDE_SLOTS

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_val, gas_label, slot_label, eol_or_None)
#    10 slots: RAM addr references (all in ewram.inc)
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # gP1FieldArrayCBase = 0x0201c600 (ewram.inc)
    (0x08087674, 0x0201c600, 'gP1FieldArrayCBase', 'ref_87674', None),
    (0x08087a7c, 0x0201c600, 'gP1FieldArrayCBase', 'ref_87a7c', None),
    (0x08087bf0, 0x0201c600, 'gP1FieldArrayCBase', 'ref_87bf0', None),
    # gP1SlotSetCodeArray = 0x0201c740 (ewram.inc)
    (0x08087678, 0x0201c740, 'gP1SlotSetCodeArray', 'ref_87678', None),
    (0x08087960, 0x0201c740, 'gP1SlotSetCodeArray', 'ref_87960', None),
    (0x08087af8, 0x0201c740, 'gP1SlotSetCodeArray', 'ref_87af8', None),
    (0x08087ba4, 0x0201c740, 'gP1SlotSetCodeArray', 'ref_87ba4', None),
    # gP1ChainZoneArray = 0x0201c880 (ewram.inc)
    (0x08087754, 0x0201c880, 'gP1ChainZoneArray', 'ref_87754', None),
    # gP1HandSlotArray = 0x0201c8f8 (ewram.inc)
    (0x08087a1c, 0x0201c8f8, 'gP1HandSlotArray', 'ref_87a1c', None),
    (0x08087cec, 0x0201c8f8, 'gP1HandSlotArray', 'ref_87cec', None),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: PTR_gP1LifePoints_xxxx -> ptr_lp_xxxx
#    13 slots (all hold value 0x0201c4e0 = gP1LifePoints)
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x0808766c, 'ptr_lp_8766c', 'gP1LifePoints'),
    (0x080876d0, 'ptr_lp_876d0', 'gP1LifePoints'),
    (0x0808774c, 'ptr_lp_8774c', 'gP1LifePoints'),
    (0x0808778c, 'ptr_lp_8778c', 'gP1LifePoints'),
    (0x08087868, 'ptr_lp_87868', 'gP1LifePoints'),
    (0x080878c0, 'ptr_lp_878c0', 'gP1LifePoints'),
    (0x08087958, 'ptr_lp_87958', 'gP1LifePoints'),
    (0x080879d0, 'ptr_lp_879d0', 'gP1LifePoints'),
    (0x08087af0, 'ptr_lp_87af0', 'gP1LifePoints'),
    (0x08087b9c, 'ptr_lp_87b9c', 'gP1LifePoints'),
    (0x08087c44, 'ptr_lp_87c44', 'gP1LifePoints'),
    (0x08087ce4, 'ptr_lp_87ce4', 'gP1LifePoints'),
    (0x08087d50, 'ptr_lp_87d50', 'gP1LifePoints'),
]

# ---------------------------------------------------------------------------
# D. PLATE operations: 14 full rewrites (all ASCII, all <=490 chars)
#    WARN=FAIL policy: any setComment failure = FAIL
# ---------------------------------------------------------------------------

PLATE_OPS = [
    # 1. write_equip_zone_entries_by_lv_card_id (0x080872e4) -- 490 chars
    (0x080872e4,
     "Equip zone entry writer for LV-card pairs. r0=player_id, r1=target_card_id. "
     "BST on r1 maps LV-pair cards (Mystic Swordsman LV2/4/6, Ultimate Insect LV1/3/5/7, "
     "Horus LV6/8, Armed Dragon LV5/7, Silent Swordsman LV3/5/7, Silent Magician LV4/8, "
     "others) to sp[0]=base_cid sp[4]=evo_cid. Elegant Egotist: calls "
     "get_card_evolution_target_ids. Phase 2: scans player gP1FieldArrayCBase slots, "
     "check_card_pair_allowed(sp[0/4], slot_card), writes substate=0xb. "
     "Phase 3: opponent slots, substate=0xd."),

    # 2. populate_equip_zone_entries_substate_e_by_pair (0x0808767c) -- CORRECTED, 339 chars
    (0x0808767c,
     "Equip zone writer for Polymerization pair. r0=player_id. Reads "
     "[gP1LifePoints+player*PLAYER_BLOCK_STRIDE+0x14] alt_slot_count. Loops "
     "gP1HandSlotArray+player*stride, extracts card_id bits[18:0], calls "
     "check_card_pair_allowed(card_id, POLYMERIZATION_CID). Pass -> "
     "write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Returns void."),

    # 3. scan_zone_equip_target_eligible_substate_c (0x080876dc) -- 412 chars
    (0x080876dc,
     "Equip activation scan callback, substate=0xc. r0=player_id, r8=zone count ptr "
     "(fn-ptr frame). Iterates [gP1LifePoints+player*PLAYER_BLOCK_STRIDE+0x18] zone list; "
     "extracts card_id bits[18:0]; gate 1: check_card_is_equip_target_eligible, gate 2: "
     "check_card_id_is_equip_excluded_range. Both pass -> "
     "write_equip_zone_entry_by_substate(player_id, 0xc, slot_idx). Used as fn-ptr via "
     "count_zone_pair_hits_with_fn_ptr."),

    # 4. write_all_equip_zone_entries_substate_c (0x08087758) -- 340 chars
    (0x08087758,
     "Equip write callback, substate=0xc, unconditional path. r0=player_id. Reads "
     "[gP1LifePoints+player*PLAYER_BLOCK_STRIDE+0x18] zone count. Loops: "
     "write_equip_zone_entry_by_substate(player_id, 0xc, slot_idx) for every slot, no "
     "eligibility check. Sibling of scan_zone_equip_target_eligible_substate_c (0x080876dc) "
     "which filters by eligibility."),

    # 5. scan_zone_gadget_pair_check_substate_d (0x08087794) -- 432 chars
    (0x08087794,
     "Equip scan callback, substate=0xd, card-pair dispatch. r1=input_card_id selects pair "
     "target r6: Green Gadget->Red Gadget; Red Gadget->Green/Yellow Gadget; Yellow Gadget->itself; "
     "Polymerization->input; Berfomet->Gazelle; Birdface->Harpie Lady. Iterates "
     "[gP1LifePoints+player*PLAYER_BLOCK_STRIDE+0x10] monster zone; "
     "check_card_pair_allowed(slot_card, r6). Pass -> "
     "write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx)."),

    # 6. scan_zone_equip_category_match_substate_e (0x08087870) -- CORRECTED, 339 chars
    (0x08087870,
     "Equip scan callback, substate=0xe, field6 category filter. r0=player_id. Iterates "
     "gP1HandSlotArray+player*PLAYER_BLOCK_STRIDE (offset 0x14 for zone count). Extracts "
     "card_id bits[18:0]; calls get_card_extended_stat_field6(card_id); if == "
     "CARD_FIELD6_EQUIP_CONTINUOUS (0x16) -> "
     "write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx)."),

    # 7. scan_zone_field5_atk_bound_substate_d (0x080878c8) -- 417 chars
    (0x080878c8,
     "Equip scan callback, substate=0xd, triple gate: field5 nonzero + ATK<=1500 + no Parasite "
     "node. r0=player_id, r8=fn-ptr frame. Iterates gP1SlotSetCodeArray+player*stride. Gates: "
     "check_card_field5_is_nonzero; get_card_extended_stat_field4_raw<=CARD_STAT_LP_THRESHOLD_1500; "
     "find_effect_node_in_zone(player_id, 0xb, zone_query_hand_tag_12a1)==0. All pass -> "
     "write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx)."),

    # 8. scan_zone_chimera_pair_check_substate_e (0x0808796c) -- 439 chars
    (0x0808796c,
     "Equip scan callback, substate=0xe, Chimera/Miracle Restoring pair check. r0=player_id, "
     "r1=input_card_id. Dispatch: CHIMERA_FLYING_MYTHICAL_BEAST_CID->sp[0]=GAZELLE_CID, "
     "sp[4]=BERFOMET_CID; MIRACLE_RESTORING_CID->sp[0]=DARK_MAGICIAN_CID_0FC9, "
     "sp[4]=BUSTER_BLADER_CID. Iterates gP1HandSlotArray+player*stride; dual-pass (r4 in 0..1): "
     "check_card_pair_allowed(slot_card, sp[r4*4]). Pass -> "
     "write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx)."),

    # 9. scan_zone_field6_eq_eval_placement_substate_b (0x08087a20) -- 402 chars
    (0x08087a20,
     "Equip scan callback, substate=0xb. r0=player_id, r1=target_card_id, r2=zone_slot_idx "
     "(saved to r8). Reads gP1FieldArrayCBase+player*stride+slot*4; extracts card_id. Gate 1: "
     "get_card_extended_stat_field6(zone_card)==get_card_extended_stat_field6(r1_card). Gate 2: "
     "eval_equip_placement_full_check(player_id, zone_card, 0). Both pass -> "
     "write_equip_zone_entry_by_substate(player_id, 0xb, zone_slot_idx)."),

    # 10. scan_zone_parasite_node_check_substate_d (0x08087a80) -- 353 chars
    (0x08087a80,
     "Equip scan callback, substate=0xd, Parasite Paracide node check. r0=player_id. Iterates "
     "gP1SlotSetCodeArray+player*stride+0x10. Per slot: card_id==PARASITE_PARACIDE_CID? If so, "
     "extracts zone_type, builds zone_key; find_effect_node_in_zone(player_id, 0xb, "
     "zone_key)==0 (no existing node) -> "
     "write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx)."),

    # 11. scan_zone_labyrinth_pair_placement_substate_d (0x08087b00) -- 451 chars
    (0x08087b00,
     "Equip scan callback, substate=0xd, Labyrinth/Dark Magic Curtain pair + placement. "
     "r0=player_id, r1=input_card_id. Dispatch: MAGICAL_LABYRINTH_CID->WALL_SHADOW_CID (r8); "
     "DARK_MAGIC_CURTAIN_CID->DARK_MAGICIAN_CID_0FC9 (r8). Iterates "
     "gP1SlotSetCodeArray+player*stride+0x10; check_card_pair_allowed(slot_card, r8). Pass: "
     "eval_equip_placement_full_check(player_id, zone_card, 1). Both pass -> "
     "write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx)."),

    # 12. scan_zone_field6_one_placement_substate_b (0x08087ba8) -- 407 chars
    (0x08087ba8,
     "Equip scan callback, substate=0xb. r0=player_id, r2=zone_slot_idx. Reads "
     "gP1FieldArrayCBase+player*stride+slot*4. Gate 1: "
     "get_card_extended_stat_field6(zone_card)==1. Gate 2: "
     "eval_equip_placement_full_check(player_id, zone_card, 0). Both pass -> "
     "write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Sibling of "
     "scan_zone_field6_eq_eval_placement_substate_b: uses constant 1 not target card field6."),

    # 13. scan_both_players_field5_eligible_substate_e (0x08087c4c) -- 390 chars
    (0x08087c4c,
     "Equip scan callback, substate=0xe, dual-player loop. r8=player_id (write target). Outer "
     "loop r2 in 0..1 (both player sides via eors r5,r2); inner loop r4=0..zone_count-1. Reads "
     "gP1HandSlotArray+player*stride+0x14 zone count. Gates: check_card_field5_is_nonzero; "
     "check_zone_slot_equip_eligible(r8, player_side, slot_idx). Both pass -> "
     "write_equip_zone_entry_by_substate(r8, 0xe, slot_idx)."),

    # 14. scan_zone_opponent_field5_substate_e (0x08087cf0) -- 464 chars
    (0x08087cf0,
     "Equip scan callback, substate=0xe, opponent-side field5 scan. r0=player_id; "
     "opponent=1-player_id. Iterates gP1LifePoints+opponent*PLAYER_BLOCK_STRIDE+0x14 zone count; "
     "reads gP1LifePoints+opponent*stride+0x418 (gP1HandSlotArray offset); extracts card_id; "
     "check_card_field5_is_nonzero. Pass -> "
     "write_equip_zone_entry_by_substate(opponent_id, 0xe, slot_idx). Contrast: "
     "scan_both_players_field5_eligible_substate_e (0x08087c4c) scans both sides + checks "
     "eligibility."),
]


def main():
    print("=== RefineF11Seg3bSlots (DRY=%s) ===" % DRY)
    nEQ = nREF = nREN = nPLT = 0
    fails = []

    print("--- EQ_SLOTS (%d total: %d CID + %d STRIDE) ---" % (
        len(EQ_SLOTS), len(CID_SLOTS), len(STRIDE_SLOTS)))
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        if _apply_eq(slot_addr, value, eq_name, slot_label, eol):
            nEQ += 1
        else:
            fails.append("EQ 0x%08x" % slot_addr)

    print("--- REF_SLOTS (%d) ---" % len(REF_SLOTS))
    for entry in REF_SLOTS:
        slot_addr, target_val, gas_label, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        if _apply_ref(slot_addr, target_val, gas_label, slot_label, eol):
            nREF += 1
        else:
            fails.append("REF 0x%08x" % slot_addr)

    print("--- RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    for slot_addr, slot_label, eol in RENAME_SLOTS:
        if _apply_rename(slot_addr, slot_label, eol):
            nREN += 1
        else:
            fails.append("REN 0x%08x" % slot_addr)

    print("--- PLATE ops (%d full rewrites) ---" % len(PLATE_OPS))
    for fn_addr, plate_text in PLATE_OPS:
        if len(plate_text) > 500:
            print("FAIL PLATE 0x%08x: text too long (%d chars > 500)" % (fn_addr, len(plate_text)))
            fails.append("PLT_LEN 0x%08x" % fn_addr)
        elif _apply_plate_full(fn_addr, plate_text):
            nPLT += 1
        else:
            fails.append("PLT_FULL 0x%08x" % fn_addr)

    print("")
    print("=== SUMMARY ===")
    print("EQ=%d/%d  REF=%d/%d  REN=%d/%d  PLT=%d/%d" % (
        nEQ, len(EQ_SLOTS), nREF, len(REF_SLOTS),
        nREN, len(RENAME_SLOTS), nPLT, len(PLATE_OPS)))
    if fails:
        print("FAILURES (%d): %s" % (len(fails), ", ".join(fails)))
    else:
        print("ALL PASS (0 failures)")


main()
