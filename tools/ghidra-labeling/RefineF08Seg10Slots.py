# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF08Seg10Slots.py -- F08 Seg-10 (0x0806d960..0x0806e76c)
#   dispatch_field_spell_placement_display_by_state cluster (11 fn)
#   EQ=40 (all reuse except 7 NEW: GAP_CID_13ED / MULTIPLICATION_OF_ANTS_CID /
#           NEO_SPACE_SPAWN_CAT_1422/1813/19BA / LP_DISPLAY_SEQ_PROGRESS_OFF /
#           EQUIP_BITMAP_QUERY_KEY)
#   REF=0
#   RENAME=2 (DWORD_0806e144/DWORD_0806e6d0 -> gp1lifepoints_<addr>)
#   FUNC_RENAME=0
#   PLATE=0 (no stale FUN_ in Seg-10; no CJK mojibake)
#
# NEW constants added to constants/*.inc before running:
#   card_info.inc: GAP_CID_13ED=0x13ed, MULTIPLICATION_OF_ANTS_CID=0x13fc,
#                  NEO_SPACE_SPAWN_CAT_1422=0x1422, NEO_SPACE_SPAWN_CAT_1813=0x1813,
#                  NEO_SPACE_SPAWN_CAT_19BA=0x19ba
#   duel_field.inc: LP_DISPLAY_SEQ_PROGRESS_OFF=0x1d7a,
#                   EQUIP_BITMAP_QUERY_KEY=0x04000400
#
# NOTE: All EOL/plate text is pure ASCII (no CJK). Jython encodes CJK as
# double-UTF-8 mojibake -- CJK in plate/EOL is a red-line error.
#
# backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260618_091902-pre-F08Seg10

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
#    40 slots total
# ---------------------------------------------------------------------------
EQ_SLOTS = [

    # ---- dispatch_field_spell_placement_display_by_state (0x6d960..0x6dbca) ----

    # gDuelPhaseFlags = 0x0201b290 (reuse ewram.inc)
    (0x0806d988, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflags_0806d988', None),

    # GAP_CID_13EA = 0x13ea (reuse card_info.inc)
    (0x0806d9f0, 0x000013ea, 'GAP_CID_13EA', 'gap_cid_13ea_0806d9f0',
     'GAP_CID_13EA=0x13ea: unallocated slot; dispatch_field_spell_placement_display_by_state default CID arg'),

    # EQUIP_PHASE_FRAME_OFF = 0x4a4 (reuse ewram.inc)
    (0x0806da2c, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'equip_phase_frame_off_0806da2c', None),

    # GAP_CID_13EA = 0x13ea (reuse card_info.inc) second slot
    (0x0806da30, 0x000013ea, 'GAP_CID_13EA', 'gap_cid_13ea_0806da30',
     'GAP_CID_13EA=0x13ea: second slot in dispatch_field_spell_placement_display_by_state'),

    # EQUIP_PHASE_FRAME_OFF = 0x4a4 (reuse ewram.inc) second slot
    (0x0806da54, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'equip_phase_frame_off_0806da54', None),

    # ---- evaluate_equip_placement_by_type_and_field5 (0x6db10..0x6dbca) ----

    # gDuelPhaseFlags = 0x0201b290 (reuse ewram.inc)
    (0x0806db60, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflags_0806db60', None),

    # EQUIP_ACTIVE_CTX_OFF = 0x484 (reuse duel_field.inc)
    (0x0806db64, 0x00000484, 'EQUIP_ACTIVE_CTX_OFF', 'equip_active_ctx_off_0806db64', None),

    # PLAYER_BLOCK_STRIDE = 0x868 (reuse ewram.inc)
    (0x0806db68, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806db68', None),

    # gP1FieldArrayCBase = 0x0201c600 (reuse ewram.inc)
    (0x0806db6c, 0x0201c600, 'gP1FieldArrayCBase', 'gp1fieldarraycbase_0806db6c', None),

    # ---- enqueue_zone_slot_sprite_with_lp_delta (0x6e00c..0x6e06e) ----

    # PLAYER_BLOCK_STRIDE = 0x868 (reuse ewram.inc)
    (0x0806e068, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806e068', None),

    # gDuelFieldSlots = 0x0201c510 (reuse ewram.inc)
    (0x0806e06c, 0x0201c510, 'gDuelFieldSlots', 'gduelfieldslotsbase_0806e06c', None),

    # ---- enqueue_zone_sprite_if_col_sum_and_effect_active_mode6 (0x6e070..0x6e116) ----

    # PLAYER_BLOCK_STRIDE = 0x868 (reuse ewram.inc)
    (0x0806e110, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806e110', None),

    # gDuelFieldSlots = 0x0201c510 (reuse ewram.inc)
    (0x0806e114, 0x0201c510, 'gDuelFieldSlots', 'gduelfieldslotsbase_0806e114', None),

    # ---- dispatch_spirit_zone_sprite_by_state_with_lp_gate (0x6e118..0x6e1c2) ----

    # P2LP_BLOCK2_OFF_1CF4 = 0x1cf4 (reuse ewram.inc)
    (0x0806e148, 0x00001cf4, 'P2LP_BLOCK2_OFF_1CF4', 'p2lp_block2_off_1cf4_0806e148', None),

    # gDuelPhaseFlags = 0x0201b290 (reuse ewram.inc)
    (0x0806e164, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflags_0806e164', None),

    # ---- tick_equip_lp_display_seq_with_prng (0x6e1c4..0x6e306) ----

    # PLAYER_BLOCK_STRIDE = 0x868 (reuse ewram.inc)
    (0x0806e244, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806e244', None),

    # gDuelFieldSlots = 0x0201c510 (reuse ewram.inc)
    (0x0806e248, 0x0201c510, 'gDuelFieldSlots', 'gduelfieldslotsbase_0806e248', None),

    # gDuelPhaseFlags = 0x0201b290 (reuse ewram.inc)
    (0x0806e24c, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflags_0806e24c', None),

    # gEquipChainSlotRefs = 0x0201bb90 (reuse ewram.inc)
    (0x0806e294, 0x0201bb90, 'gEquipChainSlotRefs', 'gequipchainslots_0806e294', None),

    # gDuelCardCtxBase = 0x0201e2a0 (reuse ewram.inc)
    (0x0806e298, 0x0201e2a0, 'gDuelCardCtxBase', 'gduecardctxbase_0806e298', None),

    # DISPLAY_SEQ_ACTIVE_PLAYER_OFF = 0x1d10 (reuse duel_field.inc)
    (0x0806e29c, 0x00001d10, 'DISPLAY_SEQ_ACTIVE_PLAYER_OFF', 'display_seq_active_player_off_0806e29c', None),

    # DISPLAY_SEQ_ACTIVE_PLAYER_OFF = 0x1d10 (reuse duel_field.inc) second slot
    (0x0806e2c0, 0x00001d10, 'DISPLAY_SEQ_ACTIVE_PLAYER_OFF', 'display_seq_active_player_off_0806e2c0', None),

    # LP_DISPLAY_SEQ_PROGRESS_OFF = 0x1d7a (NEW duel_field.inc)
    (0x0806e2f0, 0x00001d7a, 'LP_DISPLAY_SEQ_PROGRESS_OFF', 'lp_display_seq_progress_off_0806e2f0',
     'LP_DISPLAY_SEQ_PROGRESS_OFF=0x1d7a: [gDuelFieldSlots+player*0x868+0x1d7a] LP sequence progress halfword; '
     'state=0x7e: ldrh->cmp #0->beq exit; adjacent ACTIVATION_STATE_B_OFF=0x1d78; conf: high'),

    # gEquipChainSlotRefs = 0x0201bb90 (reuse ewram.inc) second slot
    (0x0806e2f4, 0x0201bb90, 'gEquipChainSlotRefs', 'gequipchainslots_0806e2f4', None),

    # ---- tick_neo_space_oam_seq_by_card_id (0x6e308..0x6e3f8) ----

    # THE_BLOCKMAN_CID = 0x1810 (reuse card_info.inc)
    (0x0806e328, 0x00001810, 'THE_BLOCKMAN_CID', 'the_blockman_cid_0806e328',
     'THE_BLOCKMAN_CID=0x1810: tick_neo_space_oam_seq_by_card_id BST branch'),

    # MULTIPLICATION_OF_ANTS_CID = 0x13fc (NEW card_info.inc)
    (0x0806e32c, 0x000013fc, 'MULTIPLICATION_OF_ANTS_CID', 'multiplication_of_ants_cid_0806e32c',
     'MULTIPLICATION_OF_ANTS_CID=0x13fc: card_stat_zero slot; plate L22365 CARD_ID_Multiplication_of_Ants=0x13fc; '
     'tick_neo_space_oam_seq_by_card_id BST case-match; conf: high (plate authority)'),

    # PHANTASMAL_MARTYRS_CID = 0x19af (reuse card_info.inc)
    (0x0806e340, 0x000019af, 'PHANTASMAL_MARTYRS_CID', 'phantasmal_martyrs_cid_0806e340',
     'PHANTASMAL_MARTYRS_CID=0x19af: tick_neo_space_oam_seq_by_card_id BST branch'),

    # NEO_SPACE_SPAWN_CAT_1422 = 0x1422 (NEW card_info.inc)
    (0x0806e34c, 0x00001422, 'NEO_SPACE_SPAWN_CAT_1422', 'neo_space_spawn_cat_1422_0806e34c',
     'NEO_SPACE_SPAWN_CAT_1422=0x1422: category code for Multiplication of Ants spawn group; '
     'card_5154=card_stat_zero; tick_neo_space_oam_seq_by_card_id; conf: high'),

    # NEO_SPACE_SPAWN_CAT_1813 = 0x1813 (NEW card_info.inc)
    (0x0806e358, 0x00001813, 'NEO_SPACE_SPAWN_CAT_1813', 'neo_space_spawn_cat_1813_0806e358',
     'NEO_SPACE_SPAWN_CAT_1813=0x1813: category code for The Blockman effect group; '
     'CID 6163 > max card range (5169); tick_neo_space_oam_seq_by_card_id; conf: high'),

    # NEO_SPACE_SPAWN_CAT_19BA = 0x19ba (NEW card_info.inc)
    (0x0806e364, 0x000019ba, 'NEO_SPACE_SPAWN_CAT_19BA', 'neo_space_spawn_cat_19ba_0806e364',
     'NEO_SPACE_SPAWN_CAT_19BA=0x19ba: category code for Phantasmal Martyrs group; '
     'CID 6586 > max card range; tick_neo_space_oam_seq_by_card_id; conf: high'),

    # EQUIP_ELIG_EXCL_D = 0x19ee (reuse card_info.inc)
    (0x0806e3ac, 0x000019ee, 'EQUIP_ELIG_EXCL_D', 'equip_elig_excl_d_0806e3ac',
     'EQUIP_ELIG_EXCL_D=0x19ee: eligibility exclusion domain; tick_neo_space_oam_seq_by_card_id 4th BST path'),

    # gDuelPhaseFlags = 0x0201b290 (reuse ewram.inc)
    (0x0806e3b0, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflags_0806e3b0', None),

    # EQUIP_PHASE_FRAME_OFF = 0x4a4 (reuse ewram.inc)
    (0x0806e3b4, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'equip_phase_frame_off_0806e3b4', None),

    # EQUIP_PHASE_FRAME_OFF = 0x4a4 (reuse ewram.inc) second slot
    (0x0806e3e8, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'equip_phase_frame_off_0806e3e8', None),

    # ---- dispatch_equip_node_sprite_by_state_with_lp_bit_gate (0x6e62c..0x6e6f6) ----

    # gDuelPhaseFlags = 0x0201b290 (reuse ewram.inc)
    (0x0806e6cc, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflags_0806e6cc', None),

    # LP_ACTIVATION_LINK_FLAG_OFF = 0x10d0 (reuse ewram.inc)
    (0x0806e6d4, 0x000010d0, 'LP_ACTIVATION_LINK_FLAG_OFF', 'lp_activation_link_flag_off_0806e6d4',
     'LP_ACTIVATION_LINK_FLAG_OFF=0x10d0: base=gP1LifePoints (ewram.inc); Seg-6 domain confirmed'),

    # gEquipChainSlotRefs = 0x0201bb90 (reuse ewram.inc)
    (0x0806e6d8, 0x0201bb90, 'gEquipChainSlotRefs', 'gequipchainslots_0806e6d8', None),

    # PLAYER_BLOCK_STRIDE = 0x868 (reuse ewram.inc)
    (0x0806e6dc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806e6dc', None),

    # OAM_SPRITE_CODE_P1_ACTIVATION = 0x8019 (reuse oam_attr.inc)
    (0x0806e6e0, 0x00008019, 'OAM_SPRITE_CODE_P1_ACTIVATION', 'oam_sprite_code_p1_act_0806e6e0', None),

    # ---- check_zone_tile_count_for_equip_bitmap_refresh (0x6e6f8..0x6e76c) ----

    # PLAYER_BLOCK_STRIDE = 0x868 (reuse ewram.inc)
    (0x0806e760, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806e760', None),

    # gDuelFieldSlots = 0x0201c510 (reuse ewram.inc)
    (0x0806e764, 0x0201c510, 'gDuelFieldSlots', 'gduelfieldslotsbase_0806e764', None),

    # EQUIP_BITMAP_QUERY_KEY = 0x04000400 (NEW duel_field.inc)
    (0x0806e768, 0x04000400, 'EQUIP_BITMAP_QUERY_KEY', 'equip_bitmap_query_key_0806e768',
     'equip bitmap query key 0x04000400; passed to bitmap update fn; not a HW register'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: none
# ---------------------------------------------------------------------------
REF_SLOTS = []

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: DWORD_ -> gp1lifepoints_<addr>
#    2 entries (already symbolized .word gP1LifePoints)
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x0806e144, 'DWORD_0806e144', 'gp1lifepoints_0806e144'),
    (0x0806e6d0, 'DWORD_0806e6d0', 'gp1lifepoints_0806e6d0'),
]

# ---------------------------------------------------------------------------
# D. FUNC_RENAMES: none
# ---------------------------------------------------------------------------
FUNC_RENAMES = []


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
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            bad = any(ord(ch) > 127 for ch in eol)
            if bad:
                print("[WARN] non-ASCII in EOL @ 0x%08x -- skipping EOL" % slot_addr)
            else:
                cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[EQ ] 0x%08x  %s  -> %s" % (slot_addr, eq_name, slot_label))
    return True


def _apply_rename_slot(slot_addr, old_label, new_label):
    if DRY:
        print("[dry] RENAME 0x%08x  %s -> %s" % (slot_addr, old_label, new_label))
        return
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()
    syms = list(sym_tbl.getSymbols(a))
    for s in syms:
        if s.getName() == old_label:
            s.setName(new_label, SourceType.USER_DEFINED)
            print("[REN] 0x%08x  %s -> %s" % (slot_addr, old_label, new_label))
            return
    # old label not found; create new label if not present
    names = [s.getName() for s in list(sym_tbl.getSymbols(a))]
    if new_label not in names:
        sym_tbl.createLabel(a, new_label, SourceType.USER_DEFINED)
        print("[REN] 0x%08x  old='%s' not found; created new label %s" % (
            slot_addr, old_label, new_label))
    else:
        print("[REN] 0x%08x  %s already present" % (slot_addr, new_label))


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF08Seg10Slots (DRY=%s) ===" % DRY)
    print("  Seg-10: 0x0806d960..0x0806e76c")
    print("  EQ=%d  REF=%d  RENAME=%d  FUNC_RENAME=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(FUNC_RENAMES)))

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

    # B. REF_SLOTS (none)
    print("\n--- B. REF_SLOTS (%d) ---" % len(REF_SLOTS))

    # C. RENAME_SLOTS
    print("\n--- C. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    for slot_addr, old_label, new_label in RENAME_SLOTS:
        _apply_rename_slot(slot_addr, old_label, new_label)

    # D. FUNC_RENAME (none)
    print("\n--- D. FUNC_RENAME (%d) ---" % len(FUNC_RENAMES))

    print("\n=== RefineF08Seg10Slots DONE ===")
    print("  EQ=%d/%d ok  REF=%d  RENAME=%d  FUNC_RENAME=%d" % (
        eq_ok, len(EQ_SLOTS),
        len(REF_SLOTS),
        len(RENAME_SLOTS),
        len(FUNC_RENAMES)))


main()
