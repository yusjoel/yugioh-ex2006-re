# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF11Seg7Slots.py -- f11 Seg-7 slot symbolization [0x0808f7c0..0x08090a78)
#
# 32 named functions (30 pre-existing + 1 FUNC_RENAME + 2 NEW stubs via DisassembleF11Seg7Stubs)
# 0 ROM_INCBIN; region C (all pre-existing named functions, 2 stubs)
#
# EQ: 109 total (98 REUSE + 11 NEW)
#   REUSE: PLAYER_BLOCK_STRIDE(0x868) x11, gDuelFieldSlots(0x0201c510) x11,
#          EQUIP_ZONE_COUNT_TABLE(0x0201e1c8) x9, gDuelPhaseFlags(0x0201b290) x12,
#          PHASE_LOCK_FLAG_OFF(0x4bc) x8, EQUIP_ACTIVE_CTX_OFF(0x484) x3,
#          P1LP_BLOCK2_OFF_1CE8(0x1ce8) x5, gDuelFieldSlotState(0x0201c520) x4,
#          gDuelCardCtxBase(0x0201e2a0) x1, P1LP_BLOCK2_OFF(0x1d08) x1,
#          DISPATCH_ACTIVE_FLAG_OFF(0x1d38) x2, P1LP_EQUIP_BITMAP_CTR_OFF(0x1d3c) x1,
#          EQUIP_SLOT_SCORE_CAP(0xffff) x2, CHAIN_LINK_COUNTER_OFF(0x1cbc) x1,
#          EFFECT_ZONE_BITMASK_OFF(0x10d0) x2, EQUIP_CHAIN_STEP_OFF(0x1d28) x1,
#          LP_BAR_ANIM_STATE_OFF(0x4cc) x1, SPRITE_ROW_ENTRY_DATA_OFF(0x4d4) x2,
#          CHAIN_NODE_CARD_ARR_OFF(0x4f4) x2, FIELD_STATE_OFF(0x1cf4) x1,
#          gDuelCardCtxBase(0x0201e2a0) x1, EQUIP_ZONE_COUNT_TABLE(0x0201e1c8) x9,
#          gEquipNodePool(0x0201d9c0) x1, gEquipChainSlotRefs(0x0201bb90) x1,
#          SPIRIT_REAPER_CID/DARK_ROOM_OF_NIGHTMARE_CID/CRIOSPHINX_CID/SOUL_ABSORPTION_CID/
#          SILENT_MAGICIAN_LV4_CID/ANDRO_SPHINX_CID/THEINEN_THE_GREAT_SPHINX_CID/
#          PITCH_BLACK_POWER_STONE_CID/EXODIA_NECROSS_CID/RIGHT_LEG_FORBIDDEN_ONE_CID/
#          LEFT_LEG_FORBIDDEN_ONE_CID/RIGHT_ARM_FORBIDDEN_ONE_CID/LEFT_ARM_FORBIDDEN_ONE_CID/
#          EXODIA_THE_FORBIDDEN_ONE_CID/BACKFIRE_CID/GEARFRIED_SWORDMASTER_CID/MAJI_GIRE_PANDA_CID/
#          FIREBIRD_CID
#   NEW: BERSERK_GORILLA_CID(0x16bf), FALLING_DOWN_CID_SHIFTED(0xb4d00000),
#        SOUL_ABSORBING_BONE_TOWER_CID_SHIFTED(0xba200000), THE_BLOCKMAN_CID_SHIFTED(0xc0800000),
#        THEINEN_ACTIVATION_PACKED(0x005017c9), SPHINX_ACTIVATION_INIT_TEMPLATE(0x09e3f18c),
#        EFFECT_NODE_TABLE_TYPE0_BASE(0x09e3f19c), EFFECT_NODE_TABLE_TYPE0_COUNT(0x2a3),
#        EFFECT_NODE_TABLE_TYPE1_BASE(0x09e430fc), EFFECT_NODE_TABLE_TYPE1_COUNT(0x187),
#        EFFECT_NODE_TABLE_TYPE2_BASE(0x09e455bc), EFFECT_NODE_TABLE_TYPE3_BASE(0x09e46324)
# RENAME: 10 (9 PTR_gP1LifePoints_ -> ptr_lp_xxxx + 1 DAT_0808f934 -> ptr_case_body_f934)
# REF: 0
# FUNC_RENAME: 1 (0x080905e8 set_equip_activation_state_by_mode_alt -> invoke_effect_node_handler_3arg)
# PLATE: 35 total (33 C8 stale-FUN_ substitutions + 2 CJK->ASCII rewrites)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK). Ghidra Jython mojibake prevention.
# NOTE: WARN=FAIL: any failed setComment or value mismatch = FAIL, skip that item.
# NOTE: Run DisassembleF11Seg7Stubs.py FIRST to create the 2 stub functions.

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


def _apply_func_rename(func_addr, old_name, new_name):
    a = _addr(func_addr)
    fn = currentProgram.getFunctionManager().getFunctionAt(a)
    if fn is None:
        print("[WARN] FUNC_RENAME 0x%08x: no function found (WARN=FAIL)" % func_addr)
        return False
    current = fn.getName()
    if DRY:
        print("[dry] FUNC_RENAME 0x%08x  %s -> %s" % (func_addr, current, new_name))
        return True
    if current == new_name:
        print("[FRN] 0x%08x  already named %s (skip)" % (func_addr, new_name))
        return True
    # Remove any conflicting non-function label with new_name at this address
    sym_tbl = currentProgram.getSymbolTable()
    existing = sym_tbl.getSymbols(a)
    for sym in existing:
        if sym.getName() == new_name and not sym.getSymbolType().toString() == "Function":
            print("[FRN] removing conflicting label %s at 0x%08x" % (new_name, func_addr))
            sym.delete()
    fn.setName(new_name, SourceType.USER_DEFINED)
    print("[FRN] 0x%08x  %s -> %s" % (func_addr, current, new_name))
    return True


# =============================================================================
# EQ_SLOTS: all 109 slots
# Format: (slot_addr, value, eq_name, slot_label, eol_or_None)
# =============================================================================
EQ_SLOTS = [
    # --- scan_field_slots_for_equip_chain_node_bitmap_update [0x0808f86c] pool ---
    (0x0808f898, 0x000010d0, 'EFFECT_ZONE_BITMASK_OFF',      'seg7_pool_efzmsk_f898',      None),
    (0x0808f89c, 0x00001d28, 'EQUIP_CHAIN_STEP_OFF',         'seg7_pool_chstep_f89c',      None),
    (0x0808f924, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'seg7_pool_stride_f924',      None),
    (0x0808f928, 0x0201e1c8, 'EQUIP_ZONE_COUNT_TABLE',   'seg7_pool_eqzcnt_f928',      None),
    (0x0808f92c, 0x0201c510, 'gDuelFieldSlots',              'seg7_pool_field_f92c',       None),
    (0x0808f930, 0x00001596, 'SPIRIT_REAPER_CID',            'seg7_pool_cid_sr_f930',      None),
    # --- refresh_opponent_field_slots_for_card_attached [0x0808f938] pool ---
    (0x0808f9cc, 0x0000159b, 'DARK_ROOM_OF_NIGHTMARE_CID',   'seg7_pool_cid_drn_f9cc',     None),
    (0x0808f9d4, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'seg7_pool_stride_f9d4',      None),
    # --- scan_field_slots_for_equip_bitmap_update [0x0808f9f8] pool ---
    (0x0808fa30, 0x0201e1c8, 'EQUIP_ZONE_COUNT_TABLE',   'seg7_pool_eqzcnt_fa30',      None),
    (0x0808fa34, 0x00001624, 'PITCH_BLACK_POWER_STONE_CID',  'seg7_pool_cid_pbps_fa34',    None),
    # --- scan_field_for_extra_deck_equip_slot_update [0x0808fa4c] pool ---
    (0x0808fab4, 0x0201e1c8, 'EQUIP_ZONE_COUNT_TABLE',   'seg7_pool_eqzcnt_fab4',      None),
    (0x0808fab8, 0x00001645, 'EXODIA_NECROSS_CID',           'seg7_pool_cid_en_fab8',      None),
    (0x0808fabc, 0x00000fb7, 'RIGHT_LEG_FORBIDDEN_ONE_CID',  'seg7_pool_cid_rl_fabc',      None),
    (0x0808fac0, 0x00000fb8, 'LEFT_LEG_FORBIDDEN_ONE_CID',   'seg7_pool_cid_ll_fac0',      None),
    (0x0808fac4, 0x00000fb9, 'RIGHT_ARM_FORBIDDEN_ONE_CID',  'seg7_pool_cid_ra_fac4',      None),
    (0x0808fac8, 0x00000fba, 'LEFT_ARM_FORBIDDEN_ONE_CID',   'seg7_pool_cid_la_fac8',      None),
    (0x0808facc, 0x00000fbb, 'EXODIA_THE_FORBIDDEN_ONE_CID', 'seg7_pool_cid_fo_facc',      None),
    # --- scan_field_slots_for_inactive_equip_bitmap_clear [0x0808fae4] pool ---
    (0x0808fb90, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',         'seg7_pool_lp2off_fb90',      None),
    (0x0808fb94, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'seg7_pool_stride_fb94',      None),
    (0x0808fb98, 0x0201c510, 'gDuelFieldSlots',              'seg7_pool_field_fb98',       None),
    (0x0808fb9c, 0xb4d00000, 'FALLING_DOWN_CID_SHIFTED',     'seg7_pool_cidsh_fd_fb9c',    'FALLING_DOWN_CID(0x169a)<<19; lsls #0x13 compare in scan_field_slots_for_inactive_equip_bitmap_clear'),
    (0x0808fba0, 0x0201c520, 'gDuelFieldSlotState',          'seg7_pool_slotst_fba0',      None),
    # --- scan_field_slots_for_archfiend_equip_bitmap_update [0x0808fbd0] pool ---
    (0x0808fc48, 0x0201e1c8, 'EQUIP_ZONE_COUNT_TABLE',   'seg7_pool_eqzcnt_fc48',      None),
    (0x0808fc4c, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'seg7_pool_stride_fc4c',      None),
    (0x0808fc50, 0x000016bf, 'BERSERK_GORILLA_CID',          'seg7_pool_cid_bg_fc50',      'Berserk Gorilla CID; test_slot_has_active_card filter in scan_field_slots_for_archfiend_equip_bitmap_update'),
    (0x0808fc54, 0x0201c510, 'gDuelFieldSlots',              'seg7_pool_field_fc54',       None),
    # --- scan_card_placement_for_activation [0x0808fc78] pool ---
    (0x0808fce0, 0x0201b290, 'gDuelPhaseFlags',              'seg7_pool_phaseflag_fce0',   None),
    (0x0808fce4, 0x000004cc, 'LP_BAR_ANIM_STATE_OFF',        'seg7_pool_lp_anim_fce4',     None),
    (0x0808fce8, 0x000004d4, 'SPRITE_ROW_ENTRY_DATA_OFF',    'seg7_pool_sprent_fce8',      None),
    # 0x0808fcec is PTR_gP1LifePoints_ -> RENAME (ptr_lp_fcec)
    (0x0808fcf0, 0x000004f4, 'CHAIN_NODE_CARD_ARR_OFF',      'seg7_pool_cnarr_fcf0',       None),
    (0x0808fcdc, 0x09e3f18c, 'SPHINX_ACTIVATION_INIT_TEMPLATE', 'seg7_pool_sphinx_tmpl_fcdc', '4-word init template for scan_card_placement_for_activation sp work area'),
    (0x0808fcf4, 0x000017c7, 'ANDRO_SPHINX_CID',              'seg7_pool_cid_as_fcf4',      None),
    # --- scan_effect_zone_slots_for_equip_activation [0x0808fdc0] pool ---
    (0x0808fd94, 0x0201b290, 'gDuelPhaseFlags',              'seg7_pool_phaseflag_fd94',   None),
    (0x0808fd98, 0x000004f4, 'CHAIN_NODE_CARD_ARR_OFF',      'seg7_pool_cnarr_fd98',       None),
    (0x0808fd9c, 0x000017c9, 'THEINEN_THE_GREAT_SPHINX_CID', 'seg7_pool_cid_tgs_fd9c',     None),
    (0x0808fda4, 0x005017c9, 'THEINEN_ACTIVATION_PACKED',    'seg7_pool_theipack_fda4',    'THEINEN_THE_GREAT_SPHINX_CID(0x17c9)|0x00500000 flag bits; orrs r0,r1 at 0x0808fd7c'),
    (0x0808fda0, 0x000004d4, 'SPRITE_ROW_ENTRY_DATA_OFF',    'seg7_pool_sprent_fda0',      None),
    # --- apply_equip_activation_from_zone_scan [0x0808fe84] pool ---
    (0x0808fe50, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',         'seg7_pool_lp2off_fe50',      None),
    (0x0808fe54, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'seg7_pool_stride_fe54',      None),
    (0x0808fe58, 0x0201c510, 'gDuelFieldSlots',              'seg7_pool_field_fe58',       None),
    (0x0808fe5c, 0x000016da, 'SOUL_ABSORPTION_CID',          'seg7_pool_cid_sa_fe5c',      None),
    # --- scan_slots_for_field_bit4_sprite_update [0x0808ff44] pool ---
    (0x0808ff10, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',         'seg7_pool_lp2off_ff10',      None),
    (0x0808ff14, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'seg7_pool_stride_ff14',      None),
    (0x0808ff18, 0x0201c510, 'gDuelFieldSlots',              'seg7_pool_field_ff18',       None),
    (0x0808ff1c, 0x000018b2, 'CRIOSPHINX_CID',               'seg7_pool_cid_crs_ff1c',     None),
    (0x0808ffa4, 0x0201e1c8, 'EQUIP_ZONE_COUNT_TABLE',   'seg7_pool_eqzcnt_ffa4',      None),
    (0x0808ffa8, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'seg7_pool_stride_ffa8',      None),
    (0x0808ffac, 0x0201c510, 'gDuelFieldSlots',              'seg7_pool_field_ffac',       None),
    (0x0808ffb0, 0xba200000, 'SOUL_ABSORBING_BONE_TOWER_CID_SHIFTED', 'seg7_pool_cidsh_sabt_ffb0', 'SOUL_ABSORBING_BONE_TOWER_CID(0x1744)<<19; scan_slots_for_field_bit4_sprite_update'),
    # --- scan_field_slots_for_equip_sprite_by_chain [0x0808ffb4] pool ---
    (0x08090040, 0x0201e1c8, 'EQUIP_ZONE_COUNT_TABLE',   'seg7_pool_eqzcnt_0040',      None),
    (0x08090044, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'seg7_pool_stride_0044',      None),
    (0x08090048, 0x0201c520, 'gDuelFieldSlotState',          'seg7_pool_slotst_0048',      None),
    (0x0809004c, 0x0201c510, 'gDuelFieldSlots',              'seg7_pool_field_004c',       None),
    (0x08090050, 0x00001817, 'SILENT_MAGICIAN_LV4_CID',      'seg7_pool_cid_smlv4_0050',   None),
    # --- scan_equip_set_slot_sprite_by_counter [0x0809007c] pool ---
    (0x08090090, 0x00001cf4, 'FIELD_STATE_OFF',              'seg7_pool_fldst_0090',       None),
    # 0x0809008c is PTR_gP1LifePoints_ -> RENAME (ptr_lp_008c)
    (0x08090114, 0xc0800000, 'THE_BLOCKMAN_CID_SHIFTED',     'seg7_pool_cidsh_tb_0114',    'THE_BLOCKMAN_CID(0x1810)<<19; scan_equip_set_slot_sprite_by_counter'),
    # --- scan_slots_for_equip_activation_by_field5 [0x0809011c] pool ---
    (0x0809010c, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',         'seg7_pool_lp2off_010c',      None),
    (0x08090110, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'seg7_pool_stride_0110',      None),
    (0x08090118, 0x00001cbc, 'CHAIN_LINK_COUNTER_OFF',       'seg7_pool_chlnk_0118',       None),
    # --- dispatch_equip_field_scan_sequence [0x08090218] pool ---
    (0x08090204, 0x0201e1c8, 'EQUIP_ZONE_COUNT_TABLE',   'seg7_pool_eqzcnt_0204',      None),
    (0x08090208, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'seg7_pool_stride_0208',      None),
    (0x0809020c, 0x0201c510, 'gDuelFieldSlots',              'seg7_pool_field_020c',       None),
    (0x08090210, 0x0201c520, 'gDuelFieldSlotState',          'seg7_pool_slotst_0210',      None),
    # 0x08090214 = EQUIP_SLOT_SCORE_CAP (0xffff) -- 2nd occurrence
    (0x08090214, 0x0000ffff, 'EQUIP_SLOT_SCORE_CAP',         'seg7_pool_scrcap_0214',      None),
    # --- find_card_effect_node_entry [0x080904f4] pool ---
    (0x08090520, 0x09e3f19c, 'EFFECT_NODE_TABLE_TYPE0_BASE', 'seg7_pool_efnt0base_0520',   'effect node BST table type=0; 0x2a3 entries x 0xc stride'),
    (0x08090524, 0x000002a3, 'EFFECT_NODE_TABLE_TYPE0_COUNT','seg7_pool_efnt0cnt_0524',    None),
    (0x08090530, 0x09e430fc, 'EFFECT_NODE_TABLE_TYPE1_BASE', 'seg7_pool_efnt1base_0530',   'effect node BST table type=1; 0x187 entries'),
    (0x08090534, 0x00000187, 'EFFECT_NODE_TABLE_TYPE1_COUNT','seg7_pool_efnt1cnt_0534',    None),
    (0x08090540, 0x09e455bc, 'EFFECT_NODE_TABLE_TYPE2_BASE', 'seg7_pool_efnt2base_0540',   'effect node BST table type=2; 0x8e entries'),
    (0x0809054c, 0x09e46324, 'EFFECT_NODE_TABLE_TYPE3_BASE', 'seg7_pool_efnt3base_054c',   'effect node BST table type=3; 0xb7 entries'),
    # --- invoke_effect_node_handler_3arg (was set_equip_activation_state_by_mode_alt) [0x080905e8] pool ---
    (0x08090614, 0x0201b290, 'gDuelPhaseFlags',              'seg7_pool_phaseflag_0614',   None),
    (0x08090618, 0x000004bc, 'PHASE_LOCK_FLAG_OFF',          'seg7_pool_phlk_0618',        None),
    # --- invoke_effect_node_with_active_flag_3arg [0x08090624] pool ---
    (0x08090664, 0x0201b290, 'gDuelPhaseFlags',              'seg7_pool_phaseflag_0664',   None),
    (0x08090668, 0x000004bc, 'PHASE_LOCK_FLAG_OFF',          'seg7_pool_phlk_0668',        None),
    # --- query_equip_zone_bitmap_with_effect_guard [0x0809066c] pool --- (no new pool)
    # --- query_equip_zone_bitmap_with_active_flag [0x08090690] pool ---
    (0x080906b8, 0x0201b290, 'gDuelPhaseFlags',              'seg7_pool_phaseflag_06b8',   None),
    (0x080906bc, 0x000004bc, 'PHASE_LOCK_FLAG_OFF',          'seg7_pool_phlk_06bc',        None),
    # --- count_effect_node_zone_activations [0x08090714] pool ---
    # 0x080903cc is PTR_gP1LifePoints_ -> RENAME (ptr_lp_03cc)
    (0x080903d0, 0x00001d38, 'DISPATCH_ACTIVE_FLAG_OFF',     'seg7_pool_dspact_03d0',      None),
    (0x080903d4, 0x00001d08, 'P1LP_BLOCK2_OFF',              'seg7_pool_lp2off2_03d4',     None),
    (0x080903d8, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',         'seg7_pool_lp2off_03d8',      None),
    (0x080903dc, 0x0201e2a0, 'gDuelCardCtxBase',             'seg7_pool_cardctx_03dc',     None),
    (0x080903e0, 0x000010d0, 'EFFECT_ZONE_BITMASK_OFF',      'seg7_pool_efzmsk_03e0',      None),
    # 0x080904cc is PTR_gP1LifePoints_ -> RENAME (ptr_lp_04cc)
    (0x080904b0, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'seg7_pool_stride_04b0',      None),
    (0x080904b4, 0x0201e1c8, 'EQUIP_ZONE_COUNT_TABLE',   'seg7_pool_eqzcnt_04b4',      None),
    (0x080904b8, 0x0201c510, 'gDuelFieldSlots',              'seg7_pool_field_04b8',       None),
    (0x080904bc, 0x00001762, 'BACKFIRE_CID',                 'seg7_pool_cid_bf_04bc',      None),
    (0x080904c0, 0x0000186b, 'GEARFRIED_SWORDMASTER_CID',    'seg7_pool_cid_gsm_04c0',     None),
    (0x080904c4, 0x00001862, 'MAJI_GIRE_PANDA_CID',          'seg7_pool_cid_mgp_04c4',     None),
    (0x080904c8, 0x00001875, 'FIREBIRD_CID',                 'seg7_pool_cid_fb_04c8',      None),
    (0x080904d0, 0x00001d38, 'DISPATCH_ACTIVE_FLAG_OFF',     'seg7_pool_dspact_04d0',      None),
    (0x080904d4, 0x00001d3c, 'P1LP_EQUIP_BITMAP_CTR_OFF',    'seg7_pool_eqbitctr_04d4',    None),
    # --- invoke_count_zone_pair_hits_full_range [0x0809077c] pool ---
    (0x08090774, 0x0201b290, 'gDuelPhaseFlags',              'seg7_pool_phaseflag_0774',   None),
    (0x08090778, 0x000004bc, 'PHASE_LOCK_FLAG_OFF',          'seg7_pool_phlk_0778',        None),
    # --- count_zone_pair_hits_with_fn_ptr [0x0809078c] pool ---
    (0x080907ec, 0x0201b290, 'gDuelPhaseFlags',              'seg7_pool_phaseflag_07ec',   None),
    (0x080907f0, 0x000004bc, 'PHASE_LOCK_FLAG_OFF',          'seg7_pool_phlk_07f0',        None),
    # --- count_effect_node_activations_by_zone [0x080907f4] pool ---
    # (no pool -- uses immediate or shared pools)
    # --- dispatch_card_effect_activation [0x08090848] pool ---
    (0x08090840, 0x0201b290, 'gDuelPhaseFlags',              'seg7_pool_phaseflag_0840',   None),
    (0x08090844, 0x000004bc, 'PHASE_LOCK_FLAG_OFF',          'seg7_pool_phlk_0844',        None),
    # --- invoke_card_effect_node_handler [0x08090900] pool ---
    (0x08090884, 0x0201b290, 'gDuelPhaseFlags',              'seg7_pool_phaseflag_0884',   None),
    (0x08090888, 0x00000484, 'EQUIP_ACTIVE_CTX_OFF',         'seg7_pool_eqactctx_0888',    None),
    # --- invoke_effect_node_action_if_found [0x08090944] pool --- (no new pool)
    # --- check_card_effect_node_has_callback [0x0809096c] pool --- (no pool)
    # --- apply_equip_lp_delta_by_node_flag [0x08090988] pool ---
    (0x080908d4, 0x0201b290, 'gDuelPhaseFlags',              'seg7_pool_phaseflag_08d4',   None),
    (0x080908d8, 0x000004bc, 'PHASE_LOCK_FLAG_OFF',          'seg7_pool_phlk_08d8',        None),
    (0x080908dc, 0x00000484, 'EQUIP_ACTIVE_CTX_OFF',         'seg7_pool_eqactctx_08dc',    None),
    # --- check_card_effect_node_active [0x080909e0] pool ---
    (0x080908f8, 0x0201b290, 'gDuelPhaseFlags',              'seg7_pool_phaseflag_08f8',   None),
    (0x080908fc, 0x00000484, 'EQUIP_ACTIVE_CTX_OFF',         'seg7_pool_eqactctx_08fc',    None),
    # --- scan_equip_chain_nodes_for_bitmap_update [0x080909fc] pool ---
    (0x08090a58, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'seg7_pool_stride_0a58',      None),
    (0x08090a5c, 0x0201c510, 'gDuelFieldSlots',              'seg7_pool_field_0a5c',       None),
    (0x08090a60, 0x0201d9c0, 'gEquipNodePool',               'seg7_pool_nodepool_0a60',    None),
    (0x08090af0, 0x0201bb90, 'gEquipChainSlotRefs',          'seg7_pool_chainrefs_0af0',   None),
    # --- EQUIP_SLOT_SCORE_CAP first occurrence in scan_slots_for_equip_activation_by_field5 ---
    (0x080900c0, 0x0000ffff, 'EQUIP_SLOT_SCORE_CAP',         'seg7_pool_scrcap_00c0',      None),
]

# =============================================================================
# RENAME_SLOTS: 10 total (9 PTR_ + 1 DAT_ fn-ptr)
# Format: (slot_addr, old_prefix, new_label, eol_or_None)
# =============================================================================
RENAME_SLOTS = [
    (0x0808f894, 'PTR_gP1LifePoints_', 'ptr_lp_f894',   'gP1LifePoints ptr'),
    (0x0808f9d0, 'PTR_gP1LifePoints_', 'ptr_lp_f9d0',   'gP1LifePoints ptr'),
    (0x0808fb8c, 'PTR_gP1LifePoints_', 'ptr_lp_fb8c',   'gP1LifePoints ptr'),
    (0x0808fcec, 'PTR_gP1LifePoints_', 'ptr_lp_fcec',   'gP1LifePoints ptr'),
    (0x0808fe4c, 'PTR_gP1LifePoints_', 'ptr_lp_fe4c',   'gP1LifePoints ptr'),
    (0x0808ff0c, 'PTR_gP1LifePoints_', 'ptr_lp_ff0c',   'gP1LifePoints ptr'),
    (0x0809008c, 'PTR_gP1LifePoints_', 'ptr_lp_008c',   'gP1LifePoints ptr'),
    (0x080903cc, 'PTR_gP1LifePoints_', 'ptr_lp_03cc',   'gP1LifePoints ptr'),
    (0x080904cc, 'PTR_gP1LifePoints_', 'ptr_lp_04cc',   'gP1LifePoints ptr'),
    # DAT_0808f934: raw THUMB+1 fn-ptr to switch-case body at 0x0808f800
    (0x0808f934, 'DAT_',               'ptr_case_body_f934',
     'switch case body fn-ptr for find_equip_chain_node_by_pred callback'),
]

# =============================================================================
# FUNC_RENAME: 1
# =============================================================================
FUNC_RENAME = [
    (0x080905e8, 'set_equip_activation_state_by_mode_alt', 'invoke_effect_node_handler_3arg'),
]

# =============================================================================
# PLATES: 35 total
# - 33 C8 stale-FUN_ substitution plates
# - 2 CJK->ASCII rewrites
# All text is pure ASCII.
# =============================================================================
PLATES = [
    # 1. scan_field_slots_for_equip_chain_node_bitmap_update @ 0x0808f86c
    # Stale: FUN_08090218 -> dispatch_equip_field_scan_sequence, FUN_08099e0c -> run_equip_spell_display_state_machine
    (0x0808f86c,
     "Called by dispatch_equip_field_scan_sequence and run_equip_spell_display_state_machine (indeg=2). Entry gate: reads gP1LifePoints+0x10d0 [+0x0] bit0 (equip active flag); if bit0==0: returns 0 immediately. Also gates on gP1LifePoints+0x1d28 value >8 (phase threshold). Double loop 2x5 (player [0..1] x slot [0..4]); per slot: reads equip_chain_base (0x0201e1c8)+player+slot, compares card_id with 0x1596 or 0x1598; if match and chain head [+0x8] nonzero: calls find_equip_chain_node_by_pred; if found: calls enqueue_equip_slot_bitmap_update(player, slot, 0, 0). Returns r0=u32 updated_flag (1=updated, 0=none). Constants: equip_flag_offset=0x10d0, equip_chain_base=0x0201e1c8, card_id_A=0x1596, card_id_B=0x1598."
    ),
    # 2. refresh_opponent_field_slots_for_card_attached @ 0x0808f938
    # Stale: FUN_080487dc -> submit_lp_change_indicator_with_chain_check
    (0x0808f938,
     "Opponent-side field scanner: r0=player_id, opp_side=1-r0. Scans opponent 5 monster slots (j=[5..9]). For each: test_slot_has_active_card filter; reads [slot+0x40] >>4 & opp_side. ==0 simple path: enqueue_sprite_attr_with_shape. !=0: parses attr bits (lsls #0x2/#0x12) + apply_equip_activation_via_packed_attr (batch); on hit calls set_field_slot_bit_with_sprite_update(side,slot,4,1) + enqueue. r0=u32 player_id [0..1]. Returns void. Single caller submit_lp_change_indicator_with_chain_check (duel_field, batch). Side effects: enqueue_sprite_attr_with_shape, set_field_slot_bit_with_sprite_update, apply_equip_activation_via_packed_attr. Constants: PRE_TEST_CARD=0x159b, slot_attr_offset=0x40, BIT5_OPP_SHIFT=4."
    ),
    # 3. scan_field_slots_for_equip_bitmap_update @ 0x0808f9f8
    # Stale: FUN_08090218 -> dispatch_equip_field_scan_sequence
    (0x0808f9f8,
     "Iterates 2 sides (player 0..1) x monster zone slots (slot 5..9). For each slot calls test_slot_has_active_card (card_id=0x1624); if active and get_slot_effect_card_value returns 0 (no extra effect value), calls enqueue_equip_slot_bitmap_update to enqueue bitmap update. Returns 1=found and processed, 0=none. Single caller dispatch_equip_field_scan_sequence (duel_field master). Params: r0=void (entry movs r6,#0 overwrites). Constants: BASE_ADDR=0x0201e1c8, CARD_ID_FILTER=0x1624."
    ),
    # 4. scan_field_for_extra_deck_equip_slot_update @ 0x0808fa4c
    # Stale: FUN_08090218 -> dispatch_equip_field_scan_sequence
    (0x0808fa4c,
     "Called exclusively by duel_field master dispatch_equip_field_scan_sequence. Symmetric to scan_field_for_unpaired_equip_slot_update; double loop player x slot. Per active slot (card_id=0x1645): calls count_extra_deck_cards_by_id for 5 card IDs (0x0fb7/0x0fb8/0x0fb9/0x0fba/0x0fbb). If any count==0: calls enqueue_equip_slot_bitmap_update, returns 1. Triggers equip slot refresh when field has fusion material card but extra deck is missing at least one required material. Constants: CARD_ID_FIELD=0x1645, EXTRA_IDS=0x0fb7..0x0fbb, BASE_ADDR=0x0201e1c8."
    ),
    # 5. scan_field_slots_for_inactive_equip_bitmap_clear @ 0x0808fae4
    # Stale: FUN_08090218 -> dispatch_equip_field_scan_sequence
    (0x0808fae4,
     "Called exclusively by dispatch_equip_field_scan_sequence (duel_field main controller, indeg=1). Symmetric to scan_field_slots_for_archfiend_equip_bitmap_update (0x0808fbd0); adds bit5 inactive equip filter. Double loop 2x5 (player [0..1] x slot [0..4]); per slot: calls test_slot_has_active_card; if active: reads gDuelFieldSlots2 (0x0201c520) field, checks bit5==0 (equip inactive); if inactive: traverses 10 sub-slots calling check_card_is_archfiend_type; if no archfiend (r7==0): calls enqueue_equip_slot_bitmap_update. Returns r0=u32 updated_flag (1=at least one updated, 0=none). Constants: gDuelFieldSlots2=0x0201c520, player_stride=0x868, sub_slot_count=10."
    ),
    # 6. scan_field_slots_for_archfiend_equip_bitmap_update @ 0x0808fbd0
    # Stale: FUN_08090218 -> dispatch_equip_field_scan_sequence
    (0x0808fbd0,
     "Called exclusively by dispatch_equip_field_scan_sequence (duel_field main controller, indeg=1). Symmetric to scan_equip_chain_slots_for_bitmap_update (0x0808f57c). Double loop 2x5 (player [0..1] x slot [0..4]); per slot: calls test_slot_has_active_card (card_id=0x16bf); if active: traverses 10 sub-slots calling check_card_is_archfiend_type, counts archfiend cards (r7). If r7==0 (no archfiend): calls enqueue_equip_slot_bitmap_update(player, slot, 0, 0). Returns r0=u32 updated_flag (1=at least one bitmap updated, 0=none). Constants: CARD_ID=0x16bf, gDuelFieldSlots=0x0201c510, archfiend_slot_count=10."
    ),
    # 7. scan_card_placement_for_activation @ 0x0808fc78
    # Stale: FUN_0808daf0 -> find_matching_slot_by_player_zone_card, FUN_08090218 -> dispatch_equip_field_scan_sequence
    (0x0808fc78,
     "Called exclusively by duel_field master dispatch_equip_field_scan_sequence. Initializes sp work area (4 words from SPHINX_ACTIVATION_INIT_TEMPLATE=0x09e3f18c). Iterates 2 players; per slot checks byte[+0]==0x1b (card_type filter), bit15 of [slot+4] (activation flag), bits[14:8] sub-type to branch: ANDRO_SPHINX_CID=0x17c7=type_A / SPHINX_TELEIA_CID=0x17c8=type_B, stores player_id in sp+0 or sp+4+bit*8. Then calls find_zone_slot_idx_allowed_for_card, find_card_pair_in_player_deck_list, find_slot_idx_in_dual_list_by_id, find_matching_slot_by_player_zone_card, apply_equip_activation_with_id_lookup. Returns 1=activated at least once, 0=none. Constants: SPHINX_ACTIVATION_INIT_TEMPLATE=0x09e3f18c, ANDRO_SPHINX_CID=0x17c7, gDuelPhaseFlags=0x0201b290."
    ),
    # 8. scan_effect_zone_slots_for_equip_activation @ 0x0808fdc0
    # Stale: FUN_08090218 -> dispatch_equip_field_scan_sequence
    (0x0808fdc0,
     "Called exclusively by duel_field master dispatch_equip_field_scan_sequence. Double loop player [0..1] x slot [0..4]; base 0x0201c510+player*0x868+slot*0x14. Per slot: extracts bits[19:13] (7-bit card type field) and bit31 (activation flag). Filters card type SOUL_ABSORPTION_CID=0x16da via cmp. On match: checks [slot+0x8] / [slot+0xc] nonzero. Constructs OAM attr (bits[22:19] + bit13), calls apply_equip_activation_with_id_lookup then enqueue_sprite_attr_with_xy_split. Accumulates hit count in r12. Returns 0=no hit, 1=at least one activation. Constants: EFFECT_ZONE_OFFSET=0x1ce8, player_stride=0x868, CARD_TYPE_FILTER=0x16da."
    ),
    # 9. apply_equip_activation_from_zone_scan @ 0x0808fe84
    # (No stale FUN_ in this plate -- leave as new ASCII plate with current content)
    # Actually check: the current plate already has no FUN_, so just rewrite to confirm
    (0x0808fe84,
     "Called by scan_effect_zone_slots_for_equip_activation (equip zone activation dispatch). r0=player_id, r1=slot_idx. Reads slot attr from gDuelFieldSlots+player*0x868+slot*0x14; filters card_id bits[12:0] against CRIOSPHINX_CID=0x18b2. On match: checks [slot+0x8] and [slot+0xc] availability; constructs packed OAM attr; calls apply_equip_activation_with_id_lookup; if successful calls enqueue_sprite_attr_with_xy_split. Returns 1=activated, 0=none. Constants: CRIOSPHINX_CID=0x18b2, gDuelFieldSlots=0x0201c510, player_stride=0x868, slot_stride=0x14."
    ),
    # 10. scan_slots_for_field_bit4_sprite_update @ 0x0808ff44
    # Stale: FUN_08090218 -> dispatch_equip_field_scan_sequence
    (0x0808ff44,
     "Called exclusively by duel_field master dispatch_equip_field_scan_sequence. Double loop player [0..1] x slot [0..4]; reads slot word low 13 bits (card_type). Filters via mask SOUL_ABSORBING_BONE_TOWER_CID_SHIFTED=0xba200000 (lsls then cmp). On match calls set_field_slot_bit_with_sprite_update(player, slot, r2=4, r3=0) to set bit4 and trigger sprite refresh. Returns 0 always. Constants: gDuelFieldSlots=0x0201c510, EXTRA_TABLE=0x0201e1c8, CARD_TYPE_MASK=SOUL_ABSORBING_BONE_TOWER_CID_SHIFTED=0xba200000."
    ),
    # 11. scan_field_slots_for_equip_sprite_by_chain @ 0x0808ffb4
    # Stale: FUN_08090218 -> dispatch_equip_field_scan_sequence
    (0x0808ffb4,
     "Iterates 2 sides x 5 slots; for each active slot checks card_id=SILENT_MAGICIAN_LV4_CID=0x1817; calls count_slot_chain_nodes_by_card_id; if nonzero, checks bit5: bit5=0 calls enqueue_effect_card_slot_sprite_attr (with count param), then calls enqueue_equip_slot_sprite_attr (r3=1). Returns 1=processed at least one slot, 0=none. Single caller dispatch_equip_field_scan_sequence. Params: r0=void (entry movs r0,#0 + mov r8,r0 overwrites). Constants: CARD_ID_TARGET=SILENT_MAGICIAN_LV4_CID=0x1817, BASE_ADDR=0x0201e1c8."
    ),
    # 12. scan_equip_set_slot_sprite_by_counter @ 0x0809007c
    # Stale: FUN_08090218 -> dispatch_equip_field_scan_sequence
    (0x0809007c,
     "Called exclusively by dispatch_equip_field_scan_sequence (duel_field main controller). No APCS input; loads from PTR_gP1LifePoints. Reads [gP1LifePoints+0x1cf4] counter; if != 7: returns 0 immediately. If == 7: loads slot base from [gP1LifePoints+0x1ce8], iterates 4 slots (0..3); per slot: checks [slot+0xc] bits[12:0] vs passed card_id, [slot+0x8] nonzero, and [slot+0x10] bit4 (equip-activation bit); if match: calls enqueue_equip_set_slot_sprite_by_zone_col and enqueue_sprite_attr_with_xy_split. Returns r0=u32 hit_flag (1=at least one slot processed, 0=none or counter != 7). Constants: counter_val_trigger=7, counter_offset=0x1cf4, slot_base_offset=0x1ce8, slot_stride=0x14, equip_bit=bit4."
    ),
    # 13. scan_slots_for_equip_activation_by_field5 @ 0x0809011c
    # Stale: FUN_08090218 -> dispatch_equip_field_scan_sequence
    (0x0809011c,
     "Called by dispatch_equip_field_scan_sequence (duel_field main control) as one phase of equip activation scanner chain. Entry saves r0 to r9 (.hword 0x4681=mov r9,r0 -- card_id or global ptr). Calls check_card_field5_is_nonzero(r9): if non-zero scans monster zone (slot 0..4); else scans trap zone (slot 5..9). For each (player 0..1, slot): reads slot card_id (bits[12:0]), compares with r9; checks [slot+0x8] availability; checks [slot+0x10] bit4 (equip-activation bit). If conditions met: constructs OAM attr, calls apply_equip_activation_with_id_lookup; on success calls set_field_slot_bit_with_sprite_update. r0=u16 card_id [0..0xffff] (saved to r9; callsite 0x08090470 loads BACKFIRE_CID=0x1762). Returns u32 activation_done (0=no activation, 1=activated). Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, bit4=equip_activation_bit. Callers: dispatch_equip_field_scan_sequence."
    ),
    # 14. dispatch_equip_field_scan_sequence @ 0x08090218
    # Stale: FUN_0804f2e0 -> dispatch_equip_field_update_by_anim_state
    (0x08090218,
     "Called exclusively by dispatch_equip_field_update_by_anim_state (duel_field frame dispatcher). No APCS input; loads from PTR_gP1LifePoints. Entry: checks [gP1LifePoints+offset_0]; if 0: returns 0 immediately. Sequential chain of ~30 equip-zone scan functions; each returns 0=continue / nonzero=stop (jumps to LAB_080904d8, returns 1). Chain order (partial): write_monster_zone_display_indices -> increment_lp_bar_counter_no_player -> scan_equip_zone_candidates_with_snapshot -> dispatch_equip_pair_sprites_by_state -> scan_all_slots_for_max_equip_match -> scan_field_for_equip_set_slot_sprite_update -> scan_chain_nodes_for_equip_zone_sprite -> ... -> scan_all_zone_slots_for_lp_change_indicator -> scan_equip_set_slot_sprite_by_counter -> LP bar state update. Returns r0=u32 (1=some scanner processed a slot, 0=all passed or entry condition unmet). Constants: chain members ~30, all named in asm/all.s."
    ),
    # 15. find_card_effect_node_entry @ 0x080904f4 -- no FUN_ to replace, but need to add plate
    (0x080904f4,
     "Binary search over 4 effect node BST tables (TYPE0..TYPE3) indexed by card_type bits. r0=card_info_ptr, r1=param (card_type/key). Dispatches by type field to appropriate table (EFFECT_NODE_TABLE_TYPE0_BASE..TYPE3_BASE); searches 0x2a3/0x187/0x8e/0xb7 entries respectively. On match returns pointer to effect_node entry; on miss returns 0. Used by invoke_effect_node_handler_3arg, count_effect_node_activations_by_zone, dispatch_card_effect_activation, and ~12 others. indeg=28 per callgraph. Constants: TYPE0_BASE=0x09e3f19c(cnt=0x2a3), TYPE1_BASE=0x09e430fc(cnt=0x187), TYPE2_BASE=0x09e455bc(cnt=0x8e), TYPE3_BASE=0x09e46324(cnt=0xb7); entry_size=0xc."
    ),
    # 16. check_card_has_activatable_effect_node @ 0x0809058c -- simple plate, confirm no FUN_
    (0x0809058c,
     "Query wrapper: r0=card_info_ptr, r1=node_type. Calls find_card_effect_node_entry(r0, r1); if result==0 returns 0; if [node+0x8]==0 returns 0; else returns 1 (effect node exists with valid handler). Thin bool wrapper for find_card_effect_node_entry. indeg from eligibility checkers across multiple segs."
    ),
    # 17. invoke_effect_node_handler_2arg @ 0x080905c0 -- was previously clean
    (0x080905c0,
     "Effect node 2-arg invoke: r0=card_info_ptr(r4), r1=param(r5). Calls find_card_effect_node_entry(r4, r5); if node==0 returns 1. Reads node[+0xc] (2-arg handler ptr); if 0 returns 1. Clears [gDuelPhaseFlags+PHASE_LOCK_FLAG_OFF]; calls invoke_r2(card_info_ptr, param). Returns invoke_r2 result. Sibling of invoke_effect_node_handler_3arg (node[+0x8]) and invoke_effect_node_with_active_flag_3arg. indeg=7."
    ),
    # 18. invoke_effect_node_handler_3arg @ 0x080905e8 (renamed from set_equip_activation_state_by_mode_alt)
    # New plate to reflect rename
    (0x080905e8,
     "Effect node 3-arg invoke: r0=card_info_ptr(r4), r1=param1(r5), r2=param2(r6). Calls find_card_effect_node_entry(r4); if node==0 returns 1. Reads node[+0x8] (3-arg handler ptr); if 0 returns 1. Clears [gDuelPhaseFlags+PHASE_LOCK_FLAG_OFF]=0; calls invoke_r3(card_info_ptr, param1, param2). Returns invoke_r3 result. Old name set_equip_activation_state_by_mode_alt was wrong (no state write, no mode param). Sibling: invoke_effect_node_handler_2arg (node[+0xc]) and invoke_effect_node_with_active_flag_3arg (node[+0x8] with flag-set fence). indeg=18."
    ),
    # 19. invoke_effect_node_with_active_flag_3arg @ 0x08090624 -- no FUN_ stale
    (0x08090624,
     "Effect node 3-arg invoke with symmetric active-flag fence: r0=card_info_ptr(r4), r1=param1(r5), r2=param2(r6). Calls find_card_effect_node_entry(r4); if node==0 returns 1. Reads node[+0x8]; if 0 returns 1. Sets [gDuelPhaseFlags+PHASE_LOCK_FLAG_OFF]=1 (flag-set before invoke), calls invoke_r3(r4, r5, r6), then clears flag=0 on both paths (symmetric fence). Returns invoke_r3 result. Contrasted to invoke_effect_node_handler_3arg which only clears (no set). indeg=78."
    ),
    # 20. query_equip_zone_bitmap_with_effect_guard @ 0x0809066c -- no FUN_ stale
    (0x0809066c,
     "Equip zone bitmap query without active flag (passive mode): r0=slot_info_ptr. Calls find_card_effect_node_entry(r0); if node null or [node+8]==0 returns -1. Otherwise calls build_equip_zone_bitmap_for_player(r0) directly (no flag write). Compared to query_equip_zone_bitmap_with_active_flag (0x08090690): does NOT set/clear [gDuelPhaseFlags+0x4bc]. Used for eligibility checks in passive (non-activating) context. Returns 32-bit zone bitmap."
    ),
    # 21. query_equip_zone_bitmap_with_active_flag @ 0x08090690
    # Stale: FUN_0810e5e8 -> invoke_r8
    (0x08090690,
     "Equip zone bitmap query with active flag guard: r0=slot_info_ptr (r5). Calls find_card_effect_node_entry(r5); if node is null or [node+8]==0 returns -1. When node is valid: sets [gDuelPhaseFlags+PHASE_LOCK_FLAG_OFF] (global active flag) to 1, calls build_equip_zone_bitmap_for_player(r0=r5), then clears active flag to 0. Compared to query_equip_zone_bitmap_with_effect_guard (0x0809066c), this function additionally maintains the +0x4bc active flag around build_equip_zone_bitmap_for_player, ensuring invoke_r8 inside the builder can recognize the actively activating context vs passive query. Called by ~20 duel_field functions."
    ),
    # 22. build_equip_zone_bitmap_for_player @ 0x080906cc
    # Stale: FUN_0810e5e8 -> invoke_r8
    (0x080906cc,
     "Builds 2x11 equip zone bitmap (bitmask) for a given player. Nested double loop: outer r5 in {0,1} (player_side), inner r4 in {0..10} (slot_idx). Each (side, slot): calls invoke_r8 invoker thunk (r0=player_id from r9, r1=side, r2=slot); if non-zero result, ORs bit=1<<(side*16+slot) into result r6. Returns 32-bit bitmap: high 16 bits = side=1, low 16 bits = side=0. Called by query_equip_zone_bitmap_with_effect_guard and multiple duel_field callers. Constants: SIDE_COUNT=2, SLOT_COUNT=11, BITMAP_FORMULA=1<<(side*16+slot)."
    ),
    # 23. count_effect_node_zone_activations @ 0x08090714 -- no FUN_ stale
    (0x08090714,
     "Counts effect node activations across 2x11 zones. r0=card_info_ptr, r1=node_type. Clears [gDuelCardCtxBase+DISPATCH_ACTIVE_FLAG_OFF] first. Calls find_card_effect_node_entry; if node==0 or [node+0x8]==0 returns 0. Double loop outer r10={0,1} (player_side), inner r4={0..0xa} (zone_idx); calls invoke_effect_node_handler_3arg(card_info, node_type, packed_zone); on non-zero increments counter r7. Returns r7=activation count. Side-effects via invoke_effect_node_handler_3arg. indeg=11."
    ),
    # 24. invoke_count_zone_pair_hits_full_range @ 0x0809077c
    # Stale: FUN_08050eac -> set_equip_activation_state_by_mode, FUN_0809077c is in-seg -- but this IS the function
    # The plate cites FUN_08050eac -> set_equip_activation_state_by_mode and FUN_0809077c (self-ref, this function)
    (0x0809077c,
     "Wrapper calling count_zone_pair_hits_with_fn_ptr with r2=-1 (skip_pair=all). r0=card_ptr, r1=fn_ptr passed through; r2 forced to -1 (movs r2,#0xff; lsls r2,#1 -> 0x1fe? -- actually r2=0xffffffff per movs/mvn). Returns count_zone_pair_hits_with_fn_ptr result. Callers such as set_equip_activation_state_by_mode pass fn_ptr for equip placement enumeration. indeg from asm/05/09/11."
    ),
    # 25. count_zone_pair_hits_with_fn_ptr @ 0x0809078c
    # Stale: FUN_08050eac -> set_equip_activation_state_by_mode, FUN_0809077c -> invoke_count_zone_pair_hits_full_range
    (0x0809078c,
     "Zone pair scan counter accepting a function pointer parameter. Entry r0=card_ptr (sp[0] spill), r1=fn_ptr (r10 via .hword 0x468a=mov r10,r1), r2=skip_pair [0..0x1ff] (r9 via .hword 0x4691=mov r9,r2). Clears [gDuelPhaseFlags+PHASE_LOCK_FLAG_OFF] first. Double loop r5 in {0,1} (player_side) x r4 in {0..0xa} (zone_idx): builds packed_pair=r5<<8|r4; compares with r9 (skip_pair) to skip self-pair; calls invoke_r10(card_ptr, player_side, zone_idx); non-zero -> count r7++. Returns r7 = hit count. Callers such as set_equip_activation_state_by_mode pass scan_zone_* callbacks (e.g. 080876dc cluster) via fn_ptr for equip placement enumeration. indeg=4 (including invoke_count_zone_pair_hits_full_range wrapper)."
    ),
    # 26. count_effect_node_activations_by_zone @ 0x080907f4 -- CJK -> ASCII rewrite
    (0x080907f4,
     "Called by multiple equip/field effect paths (indeg=16). r0=card_info_ptr (r6), r1=effect_param (r8 via mov). Calls find_card_effect_node_entry; clears [gDuelPhaseFlags+PHASE_LOCK_FLAG_OFF]. If node=0 or node[+0x8]=0: return 0. Else loop r4=0..0xa (11 zones): invoke_r3(card_info_ptr, effect_param, r4); non-zero -> r7++. Returns r7=activation zone count. Sibling: dispatch_card_effect_activation (0x08090848) adds unicast path. Side effects: [gDuelPhaseFlags+0x4bc]:=0; via invoke_r3: zone effect node activation state. Constants: ZONE_MAX=0xa."
    ),
    # 27. dispatch_card_effect_activation @ 0x08090848
    # Stale: FUN_0810e5d0 -> invoke_r2, FUN_0810e5d4 -> invoke_r3
    (0x08090848,
     "Lookup effect node then dispatch card effect activation via unicast or broadcast handler. Calls find_card_effect_node_entry; if node==0 returns 1 (no handler). If node[+0xc] (unicast handler ptr) non-0: saves card_ptr to global slot 0x0201b714, calls invoke_r2 unicast handler, restores slot. If node[+0x8] non-0: calls invoke_r3 broadcast over 2 players x 11 zones. r0=ptr card_info, r1=u32 override_param. Returns u32 (0=success, 1=blocked/no-handler). Side-effects: [0x0201b714] temp card_ptr; [gDuelPhaseFlags+0x4bc] zeroed on broadcast path. Constants: global_card_slot=0x0201b714, player_count=2, zone_count=11."
    ),
    # 28. invoke_card_effect_node_handler @ 0x08090900
    # Stale: FUN_0810e5d0 -> invoke_r2
    (0x08090900,
     "Effect node handler invoke (node[+0x10]). r0=card_info_ptr, r1=param. Calls find_card_effect_node_entry(r0); if node==0: return 1. If [node+0x10]==0: return 1. If non-NULL -> bl invoke_r2(card_id, slot_index) (invoke effect action at node[+0x10]). Returns invoke_r2 result. indeg from check_effect_node_handler_present callers."
    ),
    # 29. check_effect_node_handler_present @ 0x08090928 -- no FUN_ stale
    (0x08090928,
     "Bool test: checks if effect node [+0x10] handler exists. r0=card_info_ptr. Calls find_card_effect_node_entry(r0); if node==0 or [node+0x10]==0 returns 0; else returns 1. Thin wrapper for invoke_card_effect_node_handler eligibility gate."
    ),
    # 30. invoke_effect_node_action_if_found @ 0x08090944
    # Stale: FUN_08084cec -> invoke_effect_action_with_temp_card_id, FUN_080a08fc -> dispatch_equip_effect_by_slot_state, FUN_0810e5d0 -> invoke_r2
    (0x08090944,
     "Conditional effect node action executor called by invoke_effect_action_with_temp_card_id and dispatch_equip_effect_by_slot_state. Calls find_card_effect_node_entry(card_ptr) to look up associated effect node. If not found (r0=0) or found but [node+0x14]=0 (no callback), returns 1 (skip-success; movs r0,#1 @ 0x08090962). If found with callback, calls invoke_r2 (effect node action executor) with r0=card_ptr, r1=r1. Returns 0 on action failure, or invoke_r2 return value on execution."
    ),
    # 31. check_card_effect_node_has_callback @ 0x0809096c -- no FUN_ stale
    (0x0809096c,
     "Bool test: checks if effect node [+0x14] callback exists. r0=card_info_ptr. Calls find_card_effect_node_entry(r0); if node==0 or [node+0x14]==0 returns 0; else returns 1. Thin wrapper for invoke_effect_node_action_if_found eligibility gate."
    ),
    # 32. apply_equip_lp_delta_by_node_flag @ 0x08090988
    # Stale: FUN_0807ae84 -> commit_serial_spell_effect_node, FUN_080a09c8 -> dispatch_equip_lp_delta_by_slot_status, FUN_080a1bc0 -> apply_lp_delta_if_slot_active
    (0x08090988,
     "Equip LP delta commit function called by commit_serial_spell_effect_node and dispatch_equip_lp_delta_by_slot_status. Accepts effect_node pointer (r0) and LP delta (r1). Checks bit5 (0x20) of [r0+4]: if 0 jumps to find_card_effect_node_entry path; if 1 checks bit2 (0x4): if 0 reads player bit from [r0+2], inverts (1-bit0), calls apply_lp_delta_if_slot_active with r0=flipped_player, r1=1, r2=1. Both paths set bit3 (0x8) in [r0+4] to mark node as committed."
    ),
    # 33. check_card_effect_node_active @ 0x080909e0 -- no FUN_ stale
    (0x080909e0,
     "Bool test: checks [node+0x4] activation count. r0=effect_node_ptr. Reads [r0+0x4]; if nonzero returns 1 (node active); else returns 0. Used by LP delta and activation state checks."
    ),
    # 34. scan_equip_chain_nodes_for_bitmap_update @ 0x080909fc -- CJK -> ASCII rewrite
    # Stale: FUN_08090a78 -> build_equip_candidate_score_table
    (0x080909fc,
     "Called by build_equip_candidate_score_table (0x08090a78, equip activation main loop, indeg=6). r0=packed_player_slot (bit0=player_side, upper=slot_idx encoded), r1=slot_idx, r3=callback_flag. Reads gDuelFieldSlots+player*PLAYER_BLOCK_STRIDE+slot*0x14; loads chain_head at slot[+0xa]; if 0 returns. Traverses gEquipNodePool (stride=8) linked list: checks node[+2].bits[3:0]==0xa (equip node type). If match: extracts player/slot from node[+0], calls test_slot_has_active_card; if r3!=0: calls enqueue_equip_slot_bitmap_update; if r3==0: sets internal flag r7=1. Constants: PLAYER_BLOCK_STRIDE=0x868, node_type_equip=0xa, node_stride=8."
    ),
    # 35. return_effect_node_result_0 @ 0x080904ec (NEW stub, set by disasm script)
    # Plate already set by DisassembleF11Seg7Stubs.py but set here too for completeness/idempotency
    (0x080904ec,
     "Effect-node callback stub: returns 0. Stored as fn_activate/fn_eligible pointer in effect node descriptor tables (TYPE0/1/2/3 at 0x09e40xxx-0x09e42c58); 10 THUMB+1 refs."
    ),
    # 36. return_effect_node_result_2 @ 0x080904f0 (NEW stub)
    (0x080904f0,
     "Effect-node callback stub: returns 2. Stored as fn_activate/fn_eligible pointer in effect node descriptor tables (TYPE0/1/2/3 at 0x09e3f6xx-0x09e452xx); 9 THUMB+1 refs."
    ),
]


# =============================================================================
# MAIN
# =============================================================================
def run():
    fail_count = 0
    ok_count = 0

    print("=" * 60)
    print("RefineF11Seg7Slots.py  DRY=%s" % DRY)
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

    # FUNC_RENAME pass
    print("\n--- FUNC_RENAME (%d) ---" % len(FUNC_RENAME))
    for func_addr, old_name, new_name in FUNC_RENAME:
        if _apply_func_rename(func_addr, old_name, new_name):
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
