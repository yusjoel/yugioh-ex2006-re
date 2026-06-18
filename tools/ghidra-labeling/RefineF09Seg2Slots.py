# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF09Seg2Slots.py -- F09 Seg-2 (0x0806ff50..0x0807104c)
#   tick_equip_partner_lp_indicator_state_machine + invoke_equip_oam_setup +
#   dispatch_equip_lp_or_hand_sprite cluster (22 fn)
#   EQ=64  (61 REUSE + 10 NEW: 10 new CIDs in card_info.inc)
#         NOTE: DAT_08070754 = OAM_SPRITE_CODE_P1_ACTIVATION (0x8019, REUSE oam_attr.inc)
#   REF=3  (PTR_gP1LifePoints x2 + gEquipChainSlotRefs x1)
#   RENAME=3  (fn-ptr DWORD slots, THUMB+1 values)
#   FUNC_RENAME=1  (0x08070900 -> check_zone_tile_count_and_set_summon_restriction_flag)
#   PLATE=0
#
# NEW constants added to constants/card_info.inc before running:
#   GUARDIAN_BAOU_CID=0x164d, LEGENDARY_FIEND_CID=0x154d, INSECT_PRINCESS_CID=0x1704
#   AQUA_SPIRIT_CID=0x1485, THUNDER_CRASH_CID=0x16d7, ENCHANTED_ARROW_CID=0x14aa
#   TOKEN_THANKSGIVING_CID=0x1665, TOKEN_FEASTEVIL_CID=0x18dc
#   GRYPHONS_FEATHER_DUSTER_CID=0x170f, CYCLONE_BOOMERANG_CID=0x19b0
#   BAZOO_THE_SOUL_EATER_CID=0x1482  (EOL only, not a data-slot equate)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK). Jython encodes CJK as
# double-UTF-8 mojibake -- CJK in plate/EOL is a red-line error.
#
# backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260618_205456-pre-F09Seg2

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
#    64 slots total (61 REUSE + 10 NEW [by value])
# ---------------------------------------------------------------------------
EQ_SLOTS = [

    # ---- tick_equip_partner_lp_indicator_state_machine (0x6ff50..0x6ffff) ----
    # gDuelCardCtxBase = 0x0201e2a0 (reuse ewram.inc)
    (0x0806ffb4, 0x0201e2a0, 'gDuelCardCtxBase', 'gduel_card_ctx_ffb4', None),
    # DWORD_0806ffb8 = gP1LifePoints (reuse ewram.inc)
    (0x0806ffb8, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ffb8', None),

    # ---- invoke_equip_oam_setup_if_tile_count_match_and_neo_daedalus (0x08070000..0x080700ff) ----
    # gP1LifePoints x3
    (0x08070044, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_0044', None),
    (0x0806ffe8, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ffe8', None),
    # ELIGIB_SPRITE_CTRL_OFF = 0x1d68 (reuse ewram.inc)
    (0x08070048, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF', 'eligib_sprite_ctrl_0048', None),
    # gDuelPhaseFlags x1
    (0x0806ff6c, 0x0201b290, 'gDuelPhaseFlags', 'gduel_phase_ff6c', None),
    # PLAYER_BLOCK_STRIDE x1
    (0x080700ec, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_00ec', None),
    # gDuelFieldSlots x1
    (0x080700f0, 0x0201c510, 'gDuelFieldSlots', 'gduel_slots_00f0', None),

    # ---- (check_equip_slot_active_gate / tick_equip_partner_display_phase) (0x08070100..0x080701af) ----
    # gDuelPhaseFlags x1
    (0x08070110, 0x0201b290, 'gDuelPhaseFlags', 'gduel_phase_0110', None),

    # ---- enqueue_zone_sprite_by_special_monster_card_id (0x080701b0..0x08070305) ----
    # PLAYER_BLOCK_STRIDE x2
    (0x0807026c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_026c', None),
    (0x08070304, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_0304', None),
    # gDuelFieldSlots x2
    (0x08070270, 0x0201c510, 'gDuelFieldSlots', 'gduel_slots_0270', None),
    (0x08070308, 0x0201c510, 'gDuelFieldSlots', 'gduel_slots_0308', None),
    # RAGING_FLAME_SPRITE_CID = 0x182d (reuse card_info.inc)
    (0x0807030c, 0x0000182d, 'RAGING_FLAME_SPRITE_CID', 'raging_flame_cid_030c',
     'RAGING_FLAME_SPRITE_CID=0x182d: Raging Flame Sprite; enqueue_zone_sprite_by_special_monster_card_id dispatch'),
    # GUARDIAN_BAOU_CID = 0x164d (NEW card_info.inc)
    (0x08070310, 0x0000164d, 'GUARDIAN_BAOU_CID', 'guardian_baou_cid_0310',
     'GUARDIAN_BAOU_CID=0x164d: Guardian Baou (pw=73544866); enqueue_zone_sprite_by_special_monster_card_id dispatch'),
    # LEGENDARY_FIEND_CID = 0x154d (NEW card_info.inc)
    (0x08070314, 0x0000154d, 'LEGENDARY_FIEND_CID', 'legendary_fiend_cid_0314',
     'LEGENDARY_FIEND_CID=0x154d: Legendary Fiend (pw=99747800); enqueue_zone_sprite_by_special_monster_card_id dispatch'),
    # MAJI_GIRE_PANDA_CID = 0x1862 (reuse card_info.inc)
    (0x08070340, 0x00001862, 'MAJI_GIRE_PANDA_CID', 'maji_gire_panda_cid_0340',
     'MAJI_GIRE_PANDA_CID=0x1862: Maji-Gire Panda; enqueue_zone_sprite_by_special_monster_card_id dispatch'),
    # INSECT_PRINCESS_CID = 0x1704 (NEW card_info.inc)
    (0x08070328, 0x00001704, 'INSECT_PRINCESS_CID', 'insect_princess_cid_0328',
     'INSECT_PRINCESS_CID=0x1704: Insect Princess (pw=37957847); enqueue_zone_sprite_by_special_monster_card_id dispatch'),
    # FIREBIRD_CID = 0x1875 (reuse card_info.inc)
    (0x08070358, 0x00001875, 'FIREBIRD_CID', 'firebird_cid_0358',
     'FIREBIRD_CID=0x1875: Firebird; enqueue_zone_sprite_by_special_monster_card_id dispatch'),
    # gDuelPhaseFlags x1
    (0x080703b8, 0x0201b290, 'gDuelPhaseFlags', 'gduel_phase_03b8', None),

    # ---- (function containing SUMMONER_OF_ILLUSIONS_CID) (0x08070306..0x0807047f area) ----
    # SUMMONER_OF_ILLUSIONS_CID = 0x1481 (reuse card_info.inc)
    (0x08070420, 0x00001481, 'SUMMONER_OF_ILLUSIONS_CID', 'summoner_of_illusions_cid_0420',
     'SUMMONER_OF_ILLUSIONS_CID=0x1481: Summoner of Illusions; dispatch branch'),

    # ---- dispatch_equip_lp_row_or_oam_by_state_and_hand_slot (0x0807051c area) ----
    # AQUA_SPIRIT_CID = 0x1485 (NEW card_info.inc)
    (0x0807057c, 0x00001485, 'AQUA_SPIRIT_CID', 'aqua_spirit_cid_057c',
     'AQUA_SPIRIT_CID=0x1485: Aqua Spirit (pw=40916023); dispatch_equip_lp_row_or_oam_by_state_and_hand_slot CID compare'),
    # gDuelPhaseFlags x1
    (0x080705a8, 0x0201b290, 'gDuelPhaseFlags', 'gduel_phase_05a8', None),

    # ---- dispatch (LP card track / LP row) ----
    # LP_CARD_TRACK_BASE_OFF x3
    (0x08070620, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF', 'lp_card_track_off_0620', None),
    (0x0807066c, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF', 'lp_card_track_off_066c', None),
    (0x08070b10, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF', 'lp_card_track_off_0b10', None),
    # PLAYER_BLOCK_STRIDE x1
    (0x08070670, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_0670', None),

    # ---- dispatch_equip_zone_sprite_or_lp_row_type16 (0x08070700 area) ----
    # gDuelPhaseFlags x1
    (0x08070750, 0x0201b290, 'gDuelPhaseFlags', 'gduel_phase_0750', None),
    # OAM_SPRITE_CODE_P1_ACTIVATION = 0x8019 (reuse oam_attr.inc) -- C4/C5 corrected
    (0x08070754, 0x00008019, 'OAM_SPRITE_CODE_P1_ACTIVATION', 'oam_sprite_p1_act_0754',
     'OAM_SPRITE_CODE_P1_ACTIVATION=0x8019: P1 activation sprite code; dispatch_equip_zone_sprite_or_lp_row_type16'),
    # gDuelPhaseFlags x1
    (0x080707d0, 0x0201b290, 'gDuelPhaseFlags', 'gduel_phase_07d0', None),

    # ---- build_equip_chain_entries_from_zone_slots (0x08070800 area) ----
    # gP1LifePoints x2
    (0x08070880, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_0880', None),
    (0x08070b0c, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_0b0c', None),
    # PLAYER_BLOCK_STRIDE x4
    (0x08070888, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_0888', None),
    (0x08070974, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_0974', None),
    (0x08070a38, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_0a38', None),
    (0x08070c08, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_0c08', None),
    # gDuelFieldSlots x6
    (0x0807088c, 0x0201c510, 'gDuelFieldSlots', 'gduel_slots_088c', None),
    (0x08070978, 0x0201c510, 'gDuelFieldSlots', 'gduel_slots_0978', None),
    (0x08070a3c, 0x0201c510, 'gDuelFieldSlots', 'gduel_slots_0a3c', None),
    (0x08070c0c, 0x0201c510, 'gDuelFieldSlots', 'gduel_slots_0c0c', None),
    (0x08070ca0, 0x0201c510, 'gDuelFieldSlots', 'gduel_slots_0ca0', None),
    (0x08070da8, 0x0201c510, 'gDuelFieldSlots', 'gduel_slots_0da8', None),
    # gDuelFieldSlotState = 0x0201c520 (reuse ewram.inc)
    (0x08070890, 0x0201c520, 'gDuelFieldSlotState', 'gduel_slot_state_0890', None),
    # P1LP_BLOCK2_OFF_1CE8 = 0x1ce8 (reuse ewram.inc)
    (0x08070884, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'p1lp_block2_off_0884', None),
    # gDuelPhaseFlags x3
    (0x08070ae8, 0x0201b290, 'gDuelPhaseFlags', 'gduel_phase_0ae8', None),
    (0x08070b38, 0x0201b290, 'gDuelPhaseFlags', 'gduel_phase_0b38', None),
    (0x08070a40, 0x0201b290, 'gDuelPhaseFlags', 'gduel_phase_0a40', None),
    # gDuelCardCtxBase = 0x0201e2a0 (reuse ewram.inc)
    (0x08070a44, 0x0201e2a0, 'gDuelCardCtxBase', 'gduel_card_ctx_0a44', None),
    # DISPATCH_ACTIVE_FLAG_OFF = 0x1d38 (reuse duel_field.inc)
    (0x08070a88, 0x00001d38, 'DISPATCH_ACTIVE_FLAG_OFF', 'dispatch_active_flag_0a88', None),
    # PLAYER_BLOCK_STRIDE x2 more
    (0x08070c9c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_0c9c', None),
    (0x08070da4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_0da4', None),
    # SUPER_REJUVENATION_CID = 0x14e2 (reuse card_info.inc)
    (0x08070d28, 0x000014e2, 'SUPER_REJUVENATION_CID', 'super_rejuvenation_cid_0d28',
     'SUPER_REJUVENATION_CID=0x14e2: Super Rejuvenation; tick_equip_target_count_or_lp_sprite_by_card_id BST node'),

    # ---- tick_equip_target_count_or_lp_sprite_by_card_id ----
    # gDuelPhaseFlags x4
    (0x08070e34, 0x0201b290, 'gDuelPhaseFlags', 'gduel_phase_0e34', None),
    (0x08070ee0, 0x0201b290, 'gDuelPhaseFlags', 'gduel_phase_0ee0', None),
    (0x08070f3c, 0x0201b290, 'gDuelPhaseFlags', 'gduel_phase_0f3c', None),
    # PLAYER_BLOCK_STRIDE x1
    (0x08070ed8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_0ed8', None),
    # gP1HandSlotArray = 0x0201c8f8 (reuse ewram.inc) -- C13 fix: this is gP1HandSlotArray not gDuelFieldSlots
    (0x08070edc, 0x0201c8f8, 'gP1HandSlotArray', 'gp1hand_0edc', None),

    # EQUIP_PHASE_FRAME_OFF = 0x4a4 (reuse ewram.inc) x8
    (0x08070e54, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'equip_phase_frame_0e54', None),
    (0x08070ed4, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'equip_phase_frame_0ed4', None),
    (0x08070f40, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'equip_phase_frame_0f40', None),
    (0x08070fb0, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'equip_phase_frame_0fb0', None),
    (0x08070fd0, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'equip_phase_frame_0fd0', None),
    (0x08070ff0, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'equip_phase_frame_0ff0', None),
    (0x08071018, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'equip_phase_frame_1018', None),
    (0x08071048, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'equip_phase_frame_1048', None),
    # NEW CIDs for dispatch table
    # THUNDER_CRASH_CID = 0x16d7 (NEW card_info.inc)
    (0x08070f60, 0x000016d7, 'THUNDER_CRASH_CID', 'thunder_crash_cid_0f60',
     'THUNDER_CRASH_CID=0x16d7: Thunder Crash (pw=69196160); tick_equip_target_count_or_lp_sprite_by_card_id dispatch table'),
    # ENCHANTED_ARROW_CID = 0x14aa (NEW card_info.inc)
    (0x08070f64, 0x000014aa, 'ENCHANTED_ARROW_CID', 'enchanted_arrow_cid_0f64',
     'ENCHANTED_ARROW_CID=0x14aa: Enchanted Arrow (pw=93260132); tick_equip_target_count_or_lp_sprite_by_card_id dispatch table'),
    # TOKEN_THANKSGIVING_CID = 0x1665 (NEW card_info.inc)
    (0x08070f68, 0x00001665, 'TOKEN_THANKSGIVING_CID', 'token_thanksgiving_cid_0f68',
     'TOKEN_THANKSGIVING_CID=0x1665: Token Thanksgiving (pw=57182235); tick_equip_target_count_or_lp_sprite_by_card_id dispatch table'),
    # TOKEN_FEASTEVIL_CID = 0x18dc (NEW card_info.inc)
    (0x08070f80, 0x000018dc, 'TOKEN_FEASTEVIL_CID', 'token_feastevil_cid_0f80',
     'TOKEN_FEASTEVIL_CID=0x18dc: Token Feastevil (pw=83675475); tick_equip_target_count_or_lp_sprite_by_card_id dispatch table'),
    # GRYPHONS_FEATHER_DUSTER_CID = 0x170f (NEW card_info.inc)
    (0x08070f84, 0x0000170f, 'GRYPHONS_FEATHER_DUSTER_CID', 'gryphons_feather_duster_cid_0f84',
     "GRYPHONS_FEATHER_DUSTER_CID=0x170f: Gryphon's Feather Duster (pw=34370473); tick_equip_target_count_or_lp_sprite_by_card_id dispatch table"),
    # CYCLONE_BOOMERANG_CID = 0x19b0 (NEW card_info.inc)
    (0x08070f90, 0x000019b0, 'CYCLONE_BOOMERANG_CID', 'cyclone_boomerang_cid_0f90',
     'CYCLONE_BOOMERANG_CID=0x19b0: Cyclone Boomerang (pw=29612557); tick_equip_target_count_or_lp_sprite_by_card_id dispatch table'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label)
#    3 entries
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # PTR_gP1LifePoints_0807061c (PTR slot -> gP1LifePoints)
    (0x0807061c, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_061c'),
    # PTR_gP1LifePoints_08070668 (PTR slot -> gP1LifePoints)
    (0x08070668, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_0668'),
    # DAT_08070758 -> gEquipChainSlotRefs
    (0x08070758, 0x0201bb90, 'gEquipChainSlotRefs', 'gequip_chain_refs_0758'),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS (fn-ptr +1): (slot_addr, slot_label, eol_ascii)
#    3 entries -- raw THUMB fn-ptr values; slot gets descriptive label + EOL
# ---------------------------------------------------------------------------
FNPTR_SLOTS = [
    # DWORD_0806ffb0 = 0x08051f05 = check_equip_slot_eligible_by_side_and_type_query+1
    (0x0806ffb0, 0x08051f05, 'check_equip_slot_eligible_by_side_and_type_query_ptr_ffb0',
     'check_equip_slot_eligible_by_side_and_type_query+1 (THUMB fn-ptr)'),
    # DWORD_0806ffec = 0x08051f05 same fn
    (0x0806ffec, 0x08051f05, 'check_equip_slot_eligible_by_side_and_type_query_ptr_ffec',
     'check_equip_slot_eligible_by_side_and_type_query+1 (THUMB fn-ptr)'),
    # DAT_08070a64 = 0x08090625 = invoke_effect_node_with_active_flag_3arg+1
    (0x08070a64, 0x08090625, 'invoke_effect_node_with_active_flag_3arg_ptr_0a64',
     'invoke_effect_node_with_active_flag_3arg+1 (THUMB fn-ptr)'),
]

# ---------------------------------------------------------------------------
# D. FUNC_RENAME: (addr, new_name)
# ---------------------------------------------------------------------------
FUNC_RENAMES = [
    (0x08070900, 'check_zone_tile_count_and_set_summon_restriction_flag'),
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
        print("[SKIP] EQ 0x%08x (%s) value mismatch -- FAIL" % (slot_addr, eq_name))
        return False

    if DRY:
        print("[dry] EQ 0x%08x  %s=0x%x  label=%s" % (slot_addr, eq_name, value, slot_label))
        return True

    eq = eq_tbl.getEquate(eq_name)
    if eq is None:
        eq = eq_tbl.createEquate(eq_name, value & 0xFFFFFFFFFFFFFFFFL)
    eq.addReference(a, 0)

    existing = sym_tbl.getSymbols(a)
    names = [s.getName() for s in existing]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)

    if eol:
        bad = any(ord(ch) > 127 for ch in eol)
        if bad:
            print("[WARN] non-ASCII in EOL @ 0x%08x -- skipping EOL" % slot_addr)
        else:
            cu = currentProgram.getListing().getCodeUnitAt(a)
            if cu is not None:
                cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[EQ ] 0x%08x  %s  -> %s" % (slot_addr, eq_name, slot_label))
    return True


def _apply_ref(slot_addr, target_addr, gas_label, slot_label, made):
    if DRY:
        print("[dry] REF 0x%08x ref->0x%08x (%s) rename %s" % (
            slot_addr, target_addr, gas_label, slot_label))
        return True
    rm = currentProgram.getReferenceManager()
    sym_tbl = currentProgram.getSymbolTable()

    tgt_a = _addr(target_addr)
    if target_addr not in made:
        existing = [s.getName() for s in sym_tbl.getSymbols(tgt_a)]
        if gas_label not in existing:
            sym_tbl.createLabel(tgt_a, gas_label, SourceType.USER_DEFINED)
        made.add(target_addr)

    slot_a = _addr(slot_addr)
    ref = rm.addMemoryReference(slot_a, tgt_a, RefType.DATA, SourceType.USER_DEFINED, 0)
    rm.setPrimary(ref, True)

    existing_slot = [s.getName() for s in sym_tbl.getSymbols(slot_a)]
    if slot_label not in existing_slot:
        sym_tbl.createLabel(slot_a, slot_label, SourceType.USER_DEFINED)

    print("[REF] 0x%08x -> 0x%08x (%s) label=%s" % (slot_addr, target_addr, gas_label, slot_label))
    return True


def _apply_fnptr(slot_addr, value, slot_label, eol):
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()

    if not _check(slot_addr, value, slot_label):
        print("[SKIP] FNPTR 0x%08x value mismatch -- FAIL" % slot_addr)
        return False

    if DRY:
        print("[dry] FNPTR 0x%08x  0x%08x  label=%s" % (slot_addr, value, slot_label))
        return True

    existing = [s.getName() for s in sym_tbl.getSymbols(a)]
    if slot_label not in existing:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)

    if eol:
        bad = any(ord(ch) > 127 for ch in eol)
        if bad:
            print("[WARN] non-ASCII in EOL @ 0x%08x -- skipping EOL" % slot_addr)
        else:
            cu = currentProgram.getListing().getCodeUnitAt(a)
            if cu is not None:
                cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[FNPTR] 0x%08x  0x%08x  -> %s" % (slot_addr, value, slot_label))
    return True


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF09Seg2Slots (DRY=%s) ===" % DRY)
    print("  Seg-2: 0x0806ff50..0x0807104c")
    print("  EQ=%d  REF=%d  FNPTR=%d  FUNC_RENAME=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(FNPTR_SLOTS), len(FUNC_RENAMES)))

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    eq_ok = eq_fail = 0
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        if _apply_eq(slot_addr, value, eq_name, slot_label, eol):
            eq_ok += 1
        else:
            eq_fail += 1
    print("  EQ done: %d ok, %d fail" % (eq_ok, eq_fail))
    if eq_fail > 0:
        print("  !!! %d EQ FAILURES !!!" % eq_fail)

    # B. REF_SLOTS
    print("\n--- B. REF_SLOTS (%d) ---" % len(REF_SLOTS))
    ref_ok = ref_fail = 0
    made = set()
    for entry in REF_SLOTS:
        slot_addr, target_addr, gas_label, slot_label = entry
        if _apply_ref(slot_addr, target_addr, gas_label, slot_label, made):
            ref_ok += 1
        else:
            ref_fail += 1
    print("  REF done: %d ok, %d fail" % (ref_ok, ref_fail))

    # C. FNPTR_SLOTS
    print("\n--- C. FNPTR_SLOTS (%d) ---" % len(FNPTR_SLOTS))
    fnptr_ok = fnptr_fail = 0
    for slot_addr, value, slot_label, eol in FNPTR_SLOTS:
        if _apply_fnptr(slot_addr, value, slot_label, eol):
            fnptr_ok += 1
        else:
            fnptr_fail += 1
    print("  FNPTR done: %d ok, %d fail" % (fnptr_ok, fnptr_fail))
    if fnptr_fail > 0:
        print("  !!! %d FNPTR FAILURES !!!" % fnptr_fail)

    # D. FUNC_RENAME
    print("\n--- D. FUNC_RENAME (%d) ---" % len(FUNC_RENAMES))
    fn_ok = fn_fail = 0
    fm = currentProgram.getFunctionManager()
    sym_tbl_d = currentProgram.getSymbolTable()
    for addr_int, new_name in FUNC_RENAMES:
        a = _addr(addr_int)
        fn = fm.getFunctionAt(a)
        if DRY:
            fn_desc = fn.getName() if fn is not None else "(no fn -- will createLabel)"
            print("[dry] FUNC_RENAME 0x%08x: %s -> %s" % (addr_int, fn_desc, new_name))
            fn_ok += 1
            continue
        if fn is None:
            # Function not recognized at this address; create a USER label instead
            # (Ghidra export will pick up the label as a function entry)
            existing = [s.getName() for s in sym_tbl_d.getSymbols(a)]
            if new_name not in existing:
                sym_tbl_d.createLabel(a, new_name, SourceType.USER_DEFINED)
            print("[FUNC_RENAME] 0x%08x: no fn object; created label %s" % (addr_int, new_name))
            fn_ok += 1
            continue
        old_name = fn.getName()
        fn.setName(new_name, SourceType.USER_DEFINED)
        print("[FUNC_RENAME] 0x%08x: %s -> %s" % (addr_int, old_name, new_name))
        fn_ok += 1
    print("  FUNC_RENAME done: %d ok, %d fail" % (fn_ok, fn_fail))
    if fn_fail > 0:
        print("  !!! %d FUNC_RENAME FAILURES !!!" % fn_fail)

    print("\n=== RefineF09Seg2Slots DONE ===")
    print("  EQ=%d/%d ok  REF=%d/%d ok  FNPTR=%d/%d ok  FUNC_RENAME=%d/%d ok" % (
        eq_ok, len(EQ_SLOTS),
        ref_ok, len(REF_SLOTS),
        fnptr_ok, len(FNPTR_SLOTS),
        fn_ok, len(FUNC_RENAMES)))


main()
