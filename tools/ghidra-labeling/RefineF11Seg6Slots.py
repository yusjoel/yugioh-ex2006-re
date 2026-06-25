# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF11Seg6Slots.py -- f11 Seg-6 slot symbolization [0x0808ea28..0x0808f7c0)
#
# 19 named functions (equip field scan / sprite enqueue cluster)
# 0 ROM_INCBIN; region C (all pre-existing named functions)
#
# EQ: 86 total (73 REUSE + 13 NEW)
#   REUSE: PLAYER_BLOCK_STRIDE(0x868)x13, gDuelFieldSlots(0x0201c510)x12,
#          gEquipZoneCountTable(0x0201e1c8)x7, P1LP_BLOCK2_OFF_1CE8(0x1ce8)x5,
#          gDuelFieldSlotState(0x0201c520)x3, EMBODIMENT_OF_APOPHIS_CID(0x1472)x3,
#          FIRE_PRINCESS_CID(0x144d)x2, gDuelFieldSpellZoneBase(0x0201c5ec)x2,
#          gEquipNodePool(0x0201d9c0)x2, SLOT_CARD_EMPTY(0xffff)x2,
#          EQUIP_NODE_TAG_MASK(0x000fffff)x2, FATAL_ABACUS_CID_SHIFTED(0xa5f80000)x2,
#          SOLEMN_WISHES_CID_SHIFTED(0xa0280000)x2, + singletons
#   NEW: THUNDER_NYAN_NYAN_CID(0x13a4), FIRE_PRINCESS_CID(0x144d),
#        MYSTICAL_BEAST_SERKET_CID(0x147a), CONVULSION_OF_NATURE_CID(0x1510),
#        KOZAKY_CID(0x1784), SOLEMN_WISHES_CID_SHIFTED(0xa0280000),
#        FIRE_PRINCESS_CID_SHIFTED(0xa2680000), FATAL_ABACUS_CID_SHIFTED(0xa5f80000),
#        AMAZONESS_TIGER_CID_SHIFTED(0xb0780000), SPELL_ZONE_TARGET_CID_PACKED(0x13680000),
#        CRUSH_CARD_ZONE11_TAG(0x0002123b), DECK_DEV_VIRUS_ZONE11_TAG(0x0002188c),
#        EQUIP_NODE_TAG_MASK(0x000fffff)
# RENAME: 7x PTR_gP1LifePoints_xxxx -> ptr_lp_xxxx + 5 raw label renames
# REF: 0
# PLATE: 13 functions C8 stale-FUN_ substitution (ASCII only)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK). Ghidra Jython mojibake prevention.
# NOTE: WARN=FAIL: any failed setComment or value mismatch = FAIL, skip that item.

from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.address import AddressSet

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


def _rename_label(slot_addr, old_prefix, new_label, eol=None):
    """Rename a label (e.g. PTR_gP1LifePoints_xxxx -> ptr_lp_xxxx or DAT_ -> semantic)."""
    if DRY:
        print("[dry] RENAME 0x%08x  -> %s" % (slot_addr, new_label))
        return True
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()
    renamed = False
    for s in sym_tbl.getSymbols(a):
        if s.getName().startswith(old_prefix):
            try:
                s.setName(new_label, SourceType.USER_DEFINED)
                s.setPrimary()
                renamed = True
                print("[REN] 0x%08x  %s... -> %s" % (slot_addr, old_prefix, new_label))
            except Exception as e:
                print("FAIL RENAME 0x%08x %s: %s (WARN=FAIL)" % (slot_addr, new_label, e))
                return False
            break
    if not renamed:
        try:
            sym_tbl.createLabel(a, new_label, SourceType.USER_DEFINED)
            for s in sym_tbl.getSymbols(a):
                if s.getName() == new_label:
                    s.setPrimary()
                    break
            print("[REN_NEW] 0x%08x  -> %s" % (slot_addr, new_label))
        except Exception as e:
            print("FAIL RENAME_NEW 0x%08x %s: %s (WARN=FAIL)" % (slot_addr, new_label, e))
            return False
    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)
    return True


def _apply_plate(fn_addr, plate_text):
    if DRY:
        print("[dry] PLATE 0x%08x  len=%d" % (fn_addr, len(plate_text)))
        return True
    a = _addr(fn_addr)
    cu = currentProgram.getListing().getCodeUnitAt(a)
    if cu is None:
        print("FAIL PLATE 0x%08x: no code unit (WARN=FAIL)" % fn_addr)
        return False
    try:
        cu.setComment(CodeUnit.PLATE_COMMENT, plate_text)
        print("[PLT] 0x%08x OK  len=%d" % (fn_addr, len(plate_text)))
        return True
    except Exception as e:
        print("FAIL PLATE 0x%08x: %s (WARN=FAIL)" % (fn_addr, e))
        return False


# =============================================================================
# EQ_SLOTS: all 86 slots
# Format: (slot_addr, value, eq_name, slot_label, eol_or_None)
# =============================================================================
EQ_SLOTS = [
    # --- enqueue_paired_slot_sprite_attrs_for_player [0x0808ea28] pool ---
    (0x0808eb48, 0x00000868, 'PLAYER_BLOCK_STRIDE',         'seg6_pool_stride_eb48',     None),
    (0x0808eb4c, 0x0201c510, 'gDuelFieldSlots',             'seg6_pool_field_eb4c',      None),
    (0x0808eb50, 0x00001368, 'SPELL_ZONE_TARGET_CARD_ID',   'seg6_pool_cid_sztar_eb50',  None),
    (0x0808eb54, 0x13680000, 'SPELL_ZONE_TARGET_CID_PACKED','seg6_pool_cidpk_eb54',      'SPELL_ZONE_TARGET_CARD_ID(0x1368) in high 16 bits; lsrs #0x10 -> r2=0x1368 for enqueue arg'),
    (0x0808eb58, 0x000012a1, 'zone_query_hand_tag_12a1',    'seg6_pool_tag_eb58',        None),
    (0x0808eb5c, 0x0201c4f0, 'gP1SlotCountBase',            'seg6_pool_slotcnt_eb5c',    None),
    (0x0808eb60, 0x0201c740, 'gP1SlotSetCodeArray',         'seg6_pool_setcode_eb60',    None),
    # --- find_first_eligible_zone_slot_for_player [0x0808ebb8] pool ---
    (0x0808eba0, 0x00000868, 'PLAYER_BLOCK_STRIDE',         'seg6_pool_stride_eba0',     None),
    (0x0808eba4, 0x0201c510, 'gDuelFieldSlots',             'seg6_pool_field_eba4',      None),
    # --- scan_field_slots_for_zone_equip_bitmap_update [0x0808ebb8] pool ---
    (0x0808ebec, 0x0201e1c8, 'gEquipZoneCountTable',        'seg6_pool_eqzcnt_ebec',     None),
    (0x0808ebf0, 0x000013a4, 'THUNDER_NYAN_NYAN_CID',       'seg6_pool_cid_tnn_ebf0',   'Thunder Nyan Nyan CID; test_slot_has_active_card filter'),
    # --- scan_field_slots_for_graveyard_equip_activation [0x0808ec08] pool ---
    (0x0808ed0c, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',        'seg6_pool_lp2off_ed0c',     None),
    (0x0808ed10, 0x00000868, 'PLAYER_BLOCK_STRIDE',         'seg6_pool_stride_ed10',     None),
    (0x0808ed14, 0x0201c510, 'gDuelFieldSlots',             'seg6_pool_field_ed14',      None),
    (0x0808ed18, 0x00001403, 'CARD_OF_SAFE_RETURN_CID',     'seg6_pool_cid_csr_ed18',    None),
    (0x0808ed1c, 0x0201c520, 'gDuelFieldSlotState',         'seg6_pool_slotst_ed1c',     None),
    (0x0808ed20, 0xfffffdff, 'OAM_SPRITE_ATTR_CLR_BIT9',    'seg6_pool_oam_clrb9_ed20',  None),
    (0x0808ed24, 0x000001ff, 'OAM_ATTR1_X_MASK',            'seg6_pool_oam_xmsk_ed24',   None),
    (0x0808ed28, 0xfffffe00, 'OAM_ATTR1_X_CLEAR',           'seg6_pool_oam_xclr_ed28',   None),
    # --- enqueue_zone_sprite_by_activation_flags [0x0808ed2c] pool ---
    (0x0808ed8c, 0x0201c510, 'gDuelFieldSlots',             'seg6_pool_field_ed8c',      None),
    (0x0808ed90, 0x00000868, 'PLAYER_BLOCK_STRIDE',         'seg6_pool_stride_ed90',     None),
    (0x0808ed94, 0xa0280000, 'SOLEMN_WISHES_CID_SHIFTED',   'seg6_pool_cidsh_swish_ed94','Solemn Wishes CID(0x1405)<<19; slot state filter post lsls #0x13'),
    # --- scan_field_slots_for_card_pair_sprite_update [0x0808ed98] pool ---
    (0x0808ee70, 0x0201e1c8, 'gEquipZoneCountTable',        'seg6_pool_eqzcnt_ee70',     None),
    (0x0808ee74, 0x00000868, 'PLAYER_BLOCK_STRIDE',         'seg6_pool_stride_ee74',     None),
    (0x0808ee78, 0x0201c510, 'gDuelFieldSlots',             'seg6_pool_field_ee78',      None),
    (0x0808ee7c, 0xa0280000, 'SOLEMN_WISHES_CID_SHIFTED',   'seg6_pool_cidsh_swish_ee7c','Solemn Wishes CID(0x1405)<<19; second occurrence'),
    # --- enqueue_active_card_shape_sprites_in_zone [0x0808ee80] pool ---
    (0x0808eeac, 0x0000144d, 'FIRE_PRINCESS_CID',           'seg6_pool_cid_fp_eeac',     'Fire Princess CID; test_slot_has_active_card filter'),
    # --- scan_field_slots_for_chain_sprite_enqueue [0x0808eeb0] pool ---
    (0x0808ef90, 0x0201e1c8, 'gEquipZoneCountTable',        'seg6_pool_eqzcnt_ef90',     None),
    (0x0808ef94, 0x00000868, 'PLAYER_BLOCK_STRIDE',         'seg6_pool_stride_ef94',     None),
    (0x0808ef98, 0x0201c510, 'gDuelFieldSlots',             'seg6_pool_field_ef98',      None),
    (0x0808efa0, 0x0201c520, 'gDuelFieldSlotState',         'seg6_pool_slotst_efa0',     None),
    (0x0808efa4, 0x0000144d, 'FIRE_PRINCESS_CID',           'seg6_pool_cid_fp_efa4',     'Fire Princess CID; second occurrence'),
    (0x0808ef9c, 0xa2680000, 'FIRE_PRINCESS_CID_SHIFTED',   'seg6_pool_cidsh_fp_ef9c',   'Fire Princess CID(0x144d)<<19; slot state CHAIN_NODE_MAGIC'),
    # --- scan_field_for_whitelist_equip_sprite_and_lp [0x0808efa8] pool ---
    (0x0808f09c, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',        'seg6_pool_lp2off_f09c',     None),
    (0x0808f0a0, 0x00000868, 'PLAYER_BLOCK_STRIDE',         'seg6_pool_stride_f0a0',     None),
    (0x0808f0a4, 0x0201c510, 'gDuelFieldSlots',             'seg6_pool_field_f0a4',      None),
    (0x0808f0a8, 0x00001472, 'EMBODIMENT_OF_APOPHIS_CID',   'seg6_pool_cid_eoa_f0a8',    None),
    (0x0808f0ac, 0xffff803f, 'slot_field_mask_ffff803f',    'seg6_pool_fldmsk_f0ac',     None),
    (0x0808f130, 0x00001472, 'EMBODIMENT_OF_APOPHIS_CID',   'seg6_pool_cid_eoa_f130',    None),
    (0x0808f170, 0x00001472, 'EMBODIMENT_OF_APOPHIS_CID',   'seg6_pool_cid_eoa_f170',    None),
    # --- scan_field_for_paired_equip_slot_bitmap_update [0x0808f174] pool ---
    (0x0808f1ac, 0x0201e1c8, 'gEquipZoneCountTable',        'seg6_pool_eqzcnt_f1ac',     None),
    (0x0808f1b0, 0x0000147a, 'MYSTICAL_BEAST_SERKET_CID',   'seg6_pool_cid_mbs_f1b0',   'Mystical Beast Serket CID; test_slot_has_active_card filter'),
    (0x0808f1b4, 0x0000146f, 'CATHEDRAL_OF_NOBLES_CID',     'seg6_pool_cid_con_f1b4',    None),
    # --- scan_field_for_unpaired_equip_slot_update [0x0808f1cc] pool ---
    (0x0808f210, 0x0201e1c8, 'gEquipZoneCountTable',        'seg6_pool_eqzcnt_f210',     None),
    (0x0808f214, 0x00001914, 'GIANT_KOZAKY_CID',            'seg6_pool_cid_gk_f214',     None),
    (0x0808f218, 0x00001784, 'KOZAKY_CID',                  'seg6_pool_cid_kzk_f218',   'Kozaky CID; count_equipped_paired_slots_for_player arg'),
    # --- scan_field_for_equip_priority_slot_update [0x0808f230] pool ---
    (0x0808f29c, 0x0201e1c8, 'gEquipZoneCountTable',        'seg6_pool_eqzcnt_f29c',     None),
    (0x0808f2a0, 0x0000160f, 'AMAZONESS_TIGER_CID',         'seg6_pool_cid_amtgr_f2a0',  None),
    (0x0808f2a4, 0x00000868, 'PLAYER_BLOCK_STRIDE',         'seg6_pool_stride_f2a4',     None),
    (0x0808f2a8, 0x0201c510, 'gDuelFieldSlots',             'seg6_pool_field_f2a8',      None),
    (0x0808f2ac, 0xb0780000, 'AMAZONESS_TIGER_CID_SHIFTED', 'seg6_pool_cidsh_amtgr_f2ac','Amazoness Tiger CID(0x160f)<<19; slot state filter post lsls #0x13'),
    # --- enqueue_exchange_slot_sprite_attrs [0x0808f2f0] pool ---
    (0x0808f3a4, 0x0000ffff, 'SLOT_CARD_EMPTY',             'seg6_pool_empty_f3a4',      'no-pair sentinel from find_equip_chain_pair_across_field'),
    (0x0808f3ac, 0x00000868, 'PLAYER_BLOCK_STRIDE',         'seg6_pool_stride_f3ac',     None),
    # --- scan_field_slots_for_attached_sprite_by_id [0x0808f3b0] pool ---
    (0x0808f440, 0x00000868, 'PLAYER_BLOCK_STRIDE',         'seg6_pool_stride_f440',     None),
    (0x0808f444, 0x0201c520, 'gDuelFieldSlotState',         'seg6_pool_slotst_f444',     None),
    (0x0808f448, 0x0201c510, 'gDuelFieldSlots',             'seg6_pool_field_f448',      None),
    (0x0808f44c, 0xa5f80000, 'FATAL_ABACUS_CID_SHIFTED',    'seg6_pool_cidsh_fab_f44c',  'Fatal Abacus CID(0x14bf)<<19; slot state filter'),
    # --- scan_field_slots_for_lp_change_sprite_update [0x0808f450] pool ---
    (0x0808f564, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',        'seg6_pool_lp2off_f564',     None),
    (0x0808f568, 0x00000868, 'PLAYER_BLOCK_STRIDE',         'seg6_pool_stride_f568',     None),
    (0x0808f56c, 0x0201c510, 'gDuelFieldSlots',             'seg6_pool_field_f56c',      None),
    (0x0808f570, 0xa5f80000, 'FATAL_ABACUS_CID_SHIFTED',    'seg6_pool_cidsh_fab_f570',  'Fatal Abacus CID(0x14bf)<<19; second occurrence'),
    (0x0808f574, 0x0201e1c8, 'gEquipZoneCountTable',        'seg6_pool_eqzcnt_f574',     None),
    (0x0808f578, 0x00001717, 'JADE_INSECT_WHISTLE_CID',     'seg6_pool_cid_jiw_f578',    None),
    # --- scan_equip_chain_slots_for_bitmap_update [0x0808f57c] pool ---
    (0x0808f5e0, 0x0201e1c8, 'gEquipZoneCountTable',        'seg6_pool_eqzcnt_f5e0',     None),
    (0x0808f5e4, 0x000014fc, 'GRADIUS_OPTION_CID',          'seg6_pool_cid_gopt_f5e4',   None),
    (0x0808f5e8, 0x0000ffff, 'SLOT_CARD_EMPTY',             'seg6_pool_empty_f5e8',      'no-pair sentinel 0xffff'),
    (0x0808f5ec, 0x00000868, 'PLAYER_BLOCK_STRIDE',         'seg6_pool_stride_f5ec',     None),
    (0x0808f5f0, 0x0201c510, 'gDuelFieldSlots',             'seg6_pool_field_f5f0',      None),
    # --- scan_chain_nodes_for_equip_zone_sprite [0x0808f608] pool ---
    (0x0808f6c4, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',        'seg6_pool_lp2off_f6c4',     None),
    (0x0808f6c8, 0x0000123b, 'CRUSH_CARD_CID',              'seg6_pool_cid_cc_f6c8',     None),
    (0x0808f6cc, 0x00000868, 'PLAYER_BLOCK_STRIDE',         'seg6_pool_stride_f6cc',     None),
    (0x0808f6d0, 0x0201c5ec, 'gDuelFieldSpellZoneBase',     'seg6_pool_spellz_f6d0',     None),
    (0x0808f6d8, 0x0201d9c0, 'gEquipNodePool',              'seg6_pool_eqnpool_f6d8',    None),
    (0x0808f6dc, 0x000fffff, 'EQUIP_NODE_TAG_MASK',         'seg6_pool_eqtmask_f6dc',    'chain node [+0] low-20-bit tag mask'),
    (0x0808f6e0, 0x0002123b, 'CRUSH_CARD_ZONE11_TAG',       'seg6_pool_z11tag_cc_f6e0',  'Crush Card zone11 node tag = CID|(2<<16)'),
    # --- scan_chain_nodes_for_equip_zone11_sprite [0x0808f6e4] pool ---
    (0x0808f7a0, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',        'seg6_pool_lp2off_f7a0',     None),
    (0x0808f7a4, 0x0000188c, 'DECK_DEVASTATION_VIRUS_CID',  'seg6_pool_cid_ddv_f7a4',    None),
    (0x0808f7a8, 0x00000868, 'PLAYER_BLOCK_STRIDE',         'seg6_pool_stride_f7a8',     None),
    (0x0808f7ac, 0x0201c5ec, 'gDuelFieldSpellZoneBase',     'seg6_pool_spellz_f7ac',     None),
    (0x0808f7b4, 0x0201d9c0, 'gEquipNodePool',              'seg6_pool_eqnpool_f7b4',    None),
    (0x0808f7b8, 0x000fffff, 'EQUIP_NODE_TAG_MASK',         'seg6_pool_eqtmask_f7b8',    'chain node [+0] low-20-bit tag mask; second occurrence'),
    (0x0808f7bc, 0x0002188c, 'DECK_DEV_VIRUS_ZONE11_TAG',   'seg6_pool_z11tag_ddv_f7bc', 'Deck Dev Virus zone11 node tag = CID|(2<<16)'),
    # --- enqueue_sprite_by_field_copy_count [0x0808f7c0] pool ---
    (0x0808f7e8, 0x00001510, 'CONVULSION_OF_NATURE_CID',    'seg6_pool_cid_con_f7e8',    'Convulsion of Nature CID; count_field_copies_of_card arg'),
    (0x0808f7f0, 0x000010d0, 'LP_ACTIVATION_LINK_FLAG_OFF', 'seg6_pool_lpflag_f7f0',     None),
    (0x0808f854, 0x00001598, 'REAPER_ON_NIGHTMARE_CID',     'seg6_pool_cid_ron_f854',    None),
]

# =============================================================================
# RENAME_SLOTS: 7x PTR_gP1LifePoints_ -> ptr_lp_* + 5 raw label renames
# Format: (slot_addr, old_prefix, new_label, eol_or_None)
# =============================================================================
RENAME_SLOTS = [
    # PTR_gP1LifePoints_ -> ptr_lp_*
    (0x0808ed08, 'PTR_gP1LifePoints_', 'ptr_lp_ed08', None),
    (0x0808f098, 'PTR_gP1LifePoints_', 'ptr_lp_f098', None),
    (0x0808f3a8, 'PTR_gP1LifePoints_', 'ptr_lp_f3a8', None),
    (0x0808f560, 'PTR_gP1LifePoints_', 'ptr_lp_f560', None),
    (0x0808f6c0, 'PTR_gP1LifePoints_', 'ptr_lp_f6c0', None),
    (0x0808f79c, 'PTR_gP1LifePoints_', 'ptr_lp_f79c', None),
    (0x0808f7ec, 'PTR_gP1LifePoints_', 'ptr_lp_f7ec', None),
    # Raw neg-offset / internal labels
    (0x0808eb64, 'DAT_', 'slot_set_code_array_neg_off_eb64',
        '-0x250 neg offset from gP1SlotSetCodeArray to card array'),
    (0x0808ee6c, 'DAT_', 'equip_zone_to_slot_state_neg_off_ee6c',
        'gEquipZoneCountTable-gDuelFieldSlotState = -0x1ca8'),
    (0x0808f6d4, 'DAT_', 'lp_block2_to_zone_chain_neg_off_f6d4',
        '[gP1LP+1ce8]+0xffffe438 -> gDuelFieldSpellZoneBase+0x14'),
    (0x0808f7b0, 'DAT_', 'lp_block2_to_zone_chain_neg_off_f7b0',
        'same offset as f6d4 (distinct slot)'),
    (0x0808f818, 'DAT_', 'switchd_base_f818',
        'switch(bits[3:0]-2) 10-case table for enqueue_sprite_by_field_copy_count'),
]

# =============================================================================
# PLATE: C8 stale FUN_ substitution for 13 functions
# Plate text is the existing plate with FUN_<addr> replaced by current name.
# All text is ASCII.
# =============================================================================
PLATES = [
    # 01 enqueue_paired_slot_sprite_attrs_for_player @ 0x0808ea28
    (0x0808ea28,
     "Iterates all slot pairs for a player (player*2 rows, up to 11 slots per row). For each pair, calls check_slot_card_pair_allowed; if non-zero, reads slot attrs and calls enqueue_sprite_attr_with_mode (mode=3) to write OAM. Also calls enqueue_equip_slot_sprite_attr for equip chain slots. r0=u32 player_data_ptr; r1=u8 player_id [0..1]; r2=u8 col_idx [0..10]; r3=u8 row_count [0..1]. Returns void. Callers: update_duel_field_slot_sprite_state (duel_field), enqueue_paired_zone_sprite_if_slot_matches. Constants: player_stride=0x868, gDuelFieldSlots=0x0201c510, mode=3."
    ),
    # 02 find_first_eligible_zone_slot_for_player @ 0x0808ebb8
    (0x0808ebb8,
     "Iterates 5 field slots (slot 0..4, stride 0x14) for given player side (r0=player_id). Checks each slot: (1) bit12 activation flag; (2) [slot+0x8] nonzero (has card); (3) check_slot_zone_bit_eligible (r2=1). Returns 1 immediately on first match, 0 if none found. Called by scan_field_slots_for_zone_equip_bitmap_update and eval_equip_slot_pair_eligibility. Params: r0=u8 player_id [0..1]. Constants: PLAYER_STRIDE=0x868, BASE_ADDR=0x0201c510, ZONE_FLAG=1."
    ),
    # 03 scan_field_slots_for_zone_equip_bitmap_update @ 0x0808ebb8... wait, label at 0x0808ebd8? Let me check
    # Actually from grep: scan_field_slots_for_zone_equip_bitmap_update L20836 -> addr 0x0808ebb8 is find_first..
    # scan_field_slots_for_zone_equip_bitmap_update starts right after; let me check the asm addresses
    # From grep L20836: scan_field_slots_for_zone_equip_bitmap_update label, addr = 0x0808ebb8 + body follows
    # Actually need to get the actual addresses from asm
    # From the raw asm: find_first_eligible_zone_slot_for_player at L20791, and the body starts there
    # scan_field_slots_for_zone_equip_bitmap_update at L20836
    # The addresses: fn02 = 0x0808ebb8 (find_first...), fn03 = need to look at the asm
]

# Let me re-derive function addresses from the proposal table directly:
# fn01 = 0x0808ea28, fn02 = 0x0808eb68, fn03 = 0x0808ebb8, fn04 = 0x0808ec08,
# fn05 = 0x0808ed2c, fn06 = 0x0808ed98, fn07 = 0x0808ee80, fn08 = 0x0808eeb0,
# fn09 = 0x0808efa8, fn10 = 0x0808f174, fn11 = 0x0808f1cc, fn12 = 0x0808f230,
# fn13 = 0x0808f2f0, fn14 = 0x0808f3b0, fn15 = 0x0808f450, fn16 = 0x0808f57c,
# fn17 = 0x0808f608, fn18 = 0x0808f6e4, fn19 = 0x0808f7c0

PLATES = [
    # 01 enqueue_paired_slot_sprite_attrs_for_player @ 0x0808ea28
    (0x0808ea28,
     "Iterates all slot pairs for a player (player*2 rows, up to 11 slots per row). For each pair, calls check_slot_card_pair_allowed; if non-zero, reads slot attrs and calls enqueue_sprite_attr_with_mode (mode=3) to write OAM. Also calls enqueue_equip_slot_sprite_attr for equip chain slots. r0=u32 player_data_ptr; r1=u8 player_id [0..1]; r2=u8 col_idx [0..10]; r3=u8 row_count [0..1]. Returns void. Callers: update_duel_field_slot_sprite_state (duel_field), enqueue_paired_zone_sprite_if_slot_matches. Constants: player_stride=0x868, gDuelFieldSlots=0x0201c510, mode=3."
    ),
    # 02 find_first_eligible_zone_slot_for_player @ 0x0808eb68
    (0x0808eb68,
     "Iterates 5 field slots (slot 0..4, stride 0x14) for given player side (r0=player_id). Checks each slot: (1) bit12 activation flag; (2) [slot+0x8] nonzero (has card); (3) check_slot_zone_bit_eligible (r2=1). Returns 1 immediately on first match, 0 if none found. Called by scan_field_slots_for_zone_equip_bitmap_update and eval_equip_slot_pair_eligibility. Params: r0=u8 player_id [0..1]. Constants: PLAYER_STRIDE=0x868, BASE_ADDR=0x0201c510, ZONE_FLAG=1."
    ),
    # 03 scan_field_slots_for_zone_equip_bitmap_update @ 0x0808ebb8
    (0x0808ebb8,
     "Iterates 2 sides x 5 slots; calls test_slot_has_active_card (card_id=0x13a4) to confirm active; if active, calls find_first_eligible_zone_slot_for_player to confirm that side has eligible zone slot; if eligible, calls enqueue_equip_slot_bitmap_update to enqueue equip bitmap update. Returns 1=processed, 0=none. Single caller dispatch_equip_field_scan_sequence (duel_field master). Params: r0=void (entry movs r6,#0 overwrites). Constants: CARD_ID_TARGET=0x13a4, BASE_ADDR=0x0201e1c8."
    ),
    # 04 scan_field_slots_for_graveyard_equip_activation @ 0x0808ec08
    (0x0808ec08,
     "Called by dispatch_equip_field_scan_sequence (duel_field main control) as one step in equip-chain activation scanner sequence. Iterates 2 players x 10 slots (player 0..1, slot 0..9), reads card_id (bits[12:0]) from each slot, compares with constant 0x1403 (Graveyard zone card ID); also checks [slot+0xc] chain pointer is non-zero. When conditions met, constructs OAM attr (flip/priority/coord fields) then calls apply_equip_activation_with_id_lookup to attempt equip effect activation. Sets flag and returns 1 if any slot activates, else 0. Side effect: injects activation record into equip chain. r0=void (entry movs r0,#0 confirms no APCS input). Returns u32 found_flag (0=no activation, 1=at least one triggered). Constants: base=gP1LifePoints+0x1ce8, card_id=0x1403 (Graveyard zone). Callers: dispatch_equip_field_scan_sequence."
    ),
    # 05 enqueue_zone_sprite_by_activation_flags @ 0x0808ed2c
    (0x0808ed2c,
     "Called exclusively by tick_duel_field_zone_sprite_update_pipeline (duel_field, indeg=3). r0=player_id [0..1]. Prologue: push {r4,r5,r6,r7,lr}; sub sp,#4; r7=player_id; movs r6,#5 (initial loop counter); r3=1. Computes player base: r0 = player_id & 1; *0x868 -> player offset; r5 = gDuelFieldSlots+player*0x868+0x74 (effect zone head); r4 = gDuelFieldSlots+player*0x868+0x64. Loop r6=[5..8] (ble #9, zone slot indices). Per iteration: reads [r4,#0] with lsls #0x13 then compares against SOLEMN_WISHES_CID_SHIFTED=0xa0280000 (skip if not equal); reads [r5,#0] extracts bit5/bit1 with double ~mask combination; if nonzero calls enqueue_sprite_attr_with_shape(player_id, slot_index, 1, r3=1). Step: r5+=0x14; r4+=0x14; slot_index++. Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, zone_offset_r4=0x64, zone_offset_r5=0x74, slot_stride=0x14, activation_mask=SOLEMN_WISHES_CID_SHIFTED (after lsls #0x13), slot_limit=9 (ble), bit5_invert_mask=bit5, bit1_invert_mask=bit1."
    ),
    # 06 scan_field_slots_for_card_pair_sprite_update @ 0x0808ed98
    (0x0808ed98,
     "Called by dispatch_equip_field_scan_sequence (duel_field main control); large field sprite scanner. Iterates 2 players x 10 slots (player 0..1, slot 0..9), base gP1LifePoints+0xffffe358. For each slot: reads word[0], extracts bits[19:0] and compares with constant 0x28a0 (card_id/type check), checks [slot+0xc] chain pointer. If conditions met: calls enqueue_sprite_attr_with_xy_split for XY-split sprite; checks [slot+0x8] bit5/bit1 inverted logic combination; if inner condition met: calls enqueue_sprite_attr_for_zone_card_id_lookup, then submit_effect_zone_lp_and_shape_sprites. r0=void (entry movs r0,#0; str r0,[sp,#0]; movs r1,#1; mov r10,r1 confirms no APCS input). Returns u32 found_flag (0=not triggered, 1=at least one slot matched). Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, cmp_val=0x28a0. Callers: dispatch_equip_field_scan_sequence."
    ),
    # 07 enqueue_active_card_shape_sprites_in_zone @ 0x0808ee80
    (0x0808ee80,
     "Called by submit_effect_zone_lp_and_shape_sprites (duel_field) as last step in effect-zone sprite combined submission. Receives player_side (r0), iterates slots 0..4 (counter r4=0..4). For each slot calls test_slot_has_active_card(card_id=0x144d, player=r0, slot=r4). If active card found: calls enqueue_sprite_attr_with_shape(player=r0, slot=r4, mode=1) to write shape sprite to attribute buffer. Pure side-effect function, no return value. r0=u8 player_side [0..1]. Returns void. Constants: card_id=0x144d, slot_range=0..4, shape_mode=1. Callers: submit_effect_zone_lp_and_shape_sprites."
    ),
    # 08 scan_field_slots_for_chain_sprite_enqueue @ 0x0808eeb0
    (0x0808eeb0,
     "Iterates 2 sides x 5 slots; checks each slot bit12 activation flag and [slot+0xc] field value against chain node constant FIRE_PRINCESS_CID_SHIFTED=0xa2680000. For matching slots calls enqueue_sprite_attr_with_xy_split to enqueue split-XY sprite attr. Inner loop slot 0..4, outer loop player 0..1. Base addr 0x0201e1c8. Single caller dispatch_equip_field_scan_sequence (duel_field master). Params: r0=void (entry ldr r0,DAT overwrites). Constants: BASE_ADDR=0x0201e1c8, CHAIN_NODE_MAGIC=FIRE_PRINCESS_CID_SHIFTED=0xa2680000, PLAYER_STRIDE=0x868."
    ),
    # 12 scan_field_for_equip_priority_slot_update @ 0x0808f230
    (0x0808f230,
     "Iterates 2 sides x 5 slots; calls test_slot_has_active_card (card_id=0x160f) per slot; among active slots compares [slot+0x4] values (priority/ATK), selects slot with smaller value; calls enqueue_equip_slot_bitmap_update to update equip bitmap. Returns 1=found and updated, 0=not processed. Single caller dispatch_equip_field_scan_sequence. Params: r0=void (entry movs r0,#0 + mov r10,r0 overwrites). Constants: CARD_ID_TARGET=0x160f, BASE_ADDR=0x0201e1c8, PLAYER_STRIDE=0x868."
    ),
    # 14 scan_field_slots_for_attached_sprite_by_id @ 0x0808f3b0
    (0x0808f3b0,
     "Double-loop field scanner for card 0x14bf (FATAL_ABACUS_CID_SHIFTED=0xa5f80000=0x14bf<<19): outer i=[0..1] (player side), inner j=[5..9] (monster + spell zone). When [slot+0]>>19 == 0x14bf AND [slot+0x40] bit5+bit1 both 0, calls enqueue_sprite_attr_with_shape to submit decorative sprite. r0=u32 card_field_bit13 [0..1] -> r10 (callee-save alias for enqueue 1st arg); r1=u32 sprite_kind_id [=1, fixed across 4 callers] -> r9. Returns void. All 4 callers (handle_card_effect_zone_eligibility_by_field6/render_slot_card_sprite_from_descriptor/render_slot_card_sprite_and_effects/render_slot_card_sprite_with_chaos_equip_check, duel_field) build r0 via lsls#0x12+lsrs#0x1f and r1=#1. Constants: TARGET_CARD_ID=0x14bf, slot_base=gDuelFieldSlots, stride_player=0x868, stride_slot=0x14, slot_attr_offset=0x40."
    ),
    # 15 scan_field_slots_for_lp_change_sprite_update @ 0x0808f450
    (0x0808f450,
     "Called exclusively by dispatch_equip_field_scan_sequence (duel_field main controller, indeg=1). Double loop 2x9 (player [0..1] x zone_slot [0..8]). Per slot: reads gP1LifePoints+0x1ce8+player_offset, checks state mask (FATAL_ABACUS_CID_SHIFTED=0xa5f80000); if match: calls enqueue_sprite_attr_with_xy_split; builds equip bitmap from bit5/bit1; if equip bitmap nonzero: calls enqueue_sprite_attr_for_zone_card_id_lookup; then calls submit_lp_change_indicator_with_chain_check twice (both player sides). Returns r0=u32 hit_flag (1=at least one slot processed, 0=none). Constants: gP1LifePoints+0x1ce8=player_offset, slot_stride=0x14, state_mask=FATAL_ABACUS_CID_SHIFTED=0xa5f80000."
    ),
    # 16 scan_equip_chain_slots_for_bitmap_update @ 0x0808f57c
    (0x0808f57c,
     "Called by dispatch_equip_field_scan_sequence (duel_field main control); equip-chain bitmap sprite update scanner. Iterates 2 players (r6=0..1) x 5 slots (r5=0..4), base 0x0201e1c8. For each (player, slot): calls test_slot_has_active_card(card_id=0x14fc, player=r4=player_xor_6, slot=r5). If active card found: calls find_equip_chain_pair_across_field(player, slot) to find cross-field pair. If valid pair returned (!=0xffff): extracts player-side/slot-index from result, calls enqueue_equip_slot_bitmap_update to write equip-slot bitmap sprite. r0=void (entry movs r6,#0 / ldr r7,DAT confirms no APCS input). Returns u32 found_flag (0=no pair, 1=at least one pair updated). Constants: card_id=0x14fc, state_base=0x0201e1c8, slot_range=0..4, no_pair=0xffff. Callers: dispatch_equip_field_scan_sequence."
    ),
    # 17 scan_chain_nodes_for_equip_zone_sprite @ 0x0808f608
    (0x0808f608,
     "Called by dispatch_equip_field_scan_sequence (duel_field main control) as one phase in equip-chain activation scan. Iterates 2 players x 11 slots (player=r9, slot 0..10), calls check_node_in_slot_chain(card_id=0x123b, zone=0xb, type=2) for each slot. If node found, reads [slot_entry+0xa] availability; if valid, calls find_slot_idx_by_card_id_in_player_zones to locate equip target slot. When target valid: calls enqueue_equip_zone_sprite_by_side for flip sprite, then submit_equip_slot_sprite_zone11 for equip-zone sprite. Finally calls enqueue_sprite_attr_for_chain_node_match for match-marker sprite. r0=void (entry movs r0,#0 / mov r9,r0 confirms no APCS input). Returns u32 activation_flag (0=none, non-zero=at least one node matched). Constants: card_id=0x123b, zone=0xb, type=2, base=0x0201c5ec. Callers: dispatch_equip_field_scan_sequence."
    ),
    # 18 scan_chain_nodes_for_equip_zone11_sprite @ 0x0808f6e4
    (0x0808f6e4,
     "Called exclusively by dispatch_equip_field_scan_sequence (duel_field main controller, indeg=1). Outer loop 2x (player [0..1]); per player: calls check_node_in_slot_chain(player XOR r4, zone=0xb=0x188c, card_type=2); if node exists: traverses chain node list (base=0x0201d9c0, stride=8), checks [node+0x0] AND EQUIP_NODE_TAG_MASK == DECK_DEV_VIRUS_ZONE11_TAG (zone11 marker); if match: calls find_slot_idx_by_card_id_in_player_zones; if slot>=0 and player_xor==0: calls enqueue_equip_zone_sprite_by_side; calls submit_equip_slot_sprite_zone11 + enqueue_sprite_attr_for_chain_node_match. Returns r0=u32 hit_count (zone11 sprite processing count, 0=no match). Constants: zone_id=0xb (zone11), chain_base=0x0201d9c0, zone11_marker=DECK_DEV_VIRUS_ZONE11_TAG=0x0002188c."
    ),
    # 19 enqueue_sprite_by_field_copy_count @ 0x0808f7c0
    (0x0808f7c0,
     "Called exclusively by duel_field master dispatch_equip_field_scan_sequence. Calls count_field_copies_of_card(card_id=0x1510): count>0 sets flag=1, else flag=0. Reads [gP1LifePoints+0x10d0] lsrs #2 ands #1 (bit2). If flag != stored bit2: calls enqueue_sprite_attr_for_card_slot to enqueue update. Returns 1=processed, 0=not queued. Constants: CARD_ID=CONVULSION_OF_NATURE_CID=0x1510, STATE_OFFSET=LP_ACTIVATION_LINK_FLAG_OFF=0x10d0."
    ),
]

# Also: scan_field_for_paired_equip_slot_bitmap_update @ 0x0808f174 (has FUN_08090218)
# scan_field_for_unpaired_equip_slot_update @ 0x0808f1cc (has FUN_08090218)
# these were missed in first PLATES list; add them:
PLATES += [
    (0x0808f174,
     "Called exclusively by dispatch_equip_field_scan_sequence (duel_field main controller). No APCS input (movs r6,#0 at entry; loads global base from gEquipZoneCountTable=0x0201e1c8). Double loop player [0..1] x slot [0..4]: calls test_slot_has_active_card(card_id=MYSTICAL_BEAST_SERKET_CID=0x147a) to confirm active; calls count_paired_slots_with_field5_default(card_id=CATHEDRAL_OF_NOBLES_CID=0x146f) for pair count; if both pass: calls enqueue_equip_slot_bitmap_update(player,slot,0,0). Returns r0=u32 hit_flag (1=at least one group processed, 0=none). Constants: BASE_ADDR=0x0201e1c8, CARD_ID_ACTIVE=0x147a, CARD_ID_PAIR=0x146f."
    ),
    (0x0808f1cc,
     "Called exclusively by duel_field master dispatch_equip_field_scan_sequence. Double loop player [0..1] x slot [0..4]; base 0x0201e1c8. Per slot: test_slot_has_active_card(card_id=GIANT_KOZAKY_CID=0x1914). If active: count_equipped_paired_slots_for_player(0) and (1) - both must be 0. If both zero: calls enqueue_equip_slot_bitmap_update, returns 1. Used to trigger equip priority slot refresh when both sides have no pairs. Returns 1=updated, 0=not processed. Constants: CARD_ID=GIANT_KOZAKY_CID=0x1914, BASE_ADDR=0x0201e1c8, KOZAKY_CID=0x1784 (for count call)."
    ),
]


# =============================================================================
# MAIN
# =============================================================================
def run():
    fail_count = 0
    ok_count = 0

    print("=" * 60)
    print("RefineF11Seg6Slots.py  DRY=%s" % DRY)
    print("=" * 60)

    # EQ pass
    print("\n--- EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    for item in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = item[0], item[1], item[2], item[3]
        eol = item[4] if len(item) > 4 else None
        if _apply_eq(slot_addr, value, eq_name, slot_label, eol):
            ok_count += 1
        else:
            fail_count += 1

    # RENAME pass
    print("\n--- RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    for item in RENAME_SLOTS:
        slot_addr, old_prefix, new_label = item[0], item[1], item[2]
        eol = item[3] if len(item) > 3 else None
        if _rename_label(slot_addr, old_prefix, new_label, eol):
            ok_count += 1
        else:
            fail_count += 1

    # PLATE pass
    print("\n--- PLATES (%d) ---" % len(PLATES))
    for fn_addr, plate_text in PLATES:
        if _apply_plate(fn_addr, plate_text):
            ok_count += 1
        else:
            fail_count += 1

    print("\n" + "=" * 60)
    print("DONE: ok=%d  fail=%d" % (ok_count, fail_count))
    if fail_count > 0:
        print("RESULT: FAIL (%d errors)" % fail_count)
    else:
        print("RESULT: PASS")
    print("=" * 60)


run()
