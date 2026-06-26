# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF11Seg10Slots.py -- f11 Seg-10 slot symbolization [0x08093598..0x080941c4)
#
# 9 named functions: play_card_ok_ui_effect / clear_duel_puzzle_wram_regions /
# init_duel_puzzle_field_and_hand_display / init_duel_puzzle_field_display_and_flags /
# init_duel_puzzle_hand_display_both_sides / init_duel_puzzle_scene_state /
# return_one_leaf__0809383c / copy_text_line_to_buf / write_lp_card_display_slot_entry /
# parse_duel_puzzle_text_token / render_duel_puzzle_text_to_sprite_queue
#
# EQ:     70 (all REUSE from constants/*.inc; 8 NEW already appended to ewram/oam_attr.inc)
# REF:    25 (25 ROM string pointer slots -> carved puzzle_token_strtab labels)
# RENAME:  9 (PTR_gP1LifePoints_* -> slot labels; code-side label relabels)
# CODE_PTR: 2 (jump-table .word slots that point to code labels within same fn)
# PLATE:   9 (replace plates: truncated over-500 + stale FUN_ substitutions)
#
# Carve: puzzle_token_strtab already added to rom.s (248 B, 25 strings at 0x09e47464)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK). Ghidra Jython mojibake prevention.
# NOTE: WARN=FAIL: any setComment FAIL or value mismatch = skip that item and report.

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
    """Create USER label at target + USER label at slot + DATA ref slot->target + setPrimary."""
    if not _check(slot_addr, target_val, gas_label):
        return False
    if DRY:
        print("[dry] REF 0x%08x  target=0x%08x  gas=%s  label=%s" % (
            slot_addr, target_val, gas_label, slot_label))
        return True
    a = _addr(slot_addr)
    t = _addr(target_val)
    sym_tbl = currentProgram.getSymbolTable()
    ref_mgr = currentProgram.getReferenceManager()
    # Create label at target (string label in ROM) if not present
    tgt_syms = list(sym_tbl.getSymbols(t))
    if not any(s.getName() == gas_label for s in tgt_syms):
        sym_tbl.createLabel(t, gas_label, SourceType.USER_DEFINED)
    # Create slot label
    names = [s.getName() for s in sym_tbl.getSymbols(a)]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)
    for s in sym_tbl.getSymbols(a):
        if s.getName() == slot_label:
            s.setPrimary()
            break
    # Add DATA reference from slot -> target
    ref_mgr.addMemoryReference(a, t, RefType.DATA, SourceType.USER_DEFINED, 0)
    for ref in ref_mgr.getReferencesFrom(a):
        if ref.getToAddress() == t:
            ref_mgr.setPrimary(ref, True)
            break
    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)
    print("[REF] 0x%08x  target=0x%08x  -> %s" % (slot_addr, target_val, slot_label))
    return True


def _apply_rename(slot_addr, old_label, new_label, eol=None):
    """Rename existing label at slot_addr to new_label, set EOL."""
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()
    if DRY:
        print("[dry] RENAME 0x%08x  %s -> %s" % (slot_addr, old_label, new_label))
        return True
    renamed = False
    for s in sym_tbl.getSymbols(a):
        if s.getName() == old_label:
            try:
                s.setName(new_label, SourceType.USER_DEFINED)
                s.setPrimary()
                renamed = True
            except Exception as e:
                print("FAIL RENAME 0x%08x %s->%s: %s" % (slot_addr, old_label, new_label, e))
                return False
            break
    if not renamed:
        names = [s.getName() for s in sym_tbl.getSymbols(a)]
        if new_label in names:
            for s in sym_tbl.getSymbols(a):
                if s.getName() == new_label:
                    s.setPrimary()
                    break
            renamed = True
        else:
            print("WARN RENAME 0x%08x: old label %s not found (names=%s)" % (slot_addr, old_label, names))
            sym_tbl.createLabel(a, new_label, SourceType.USER_DEFINED)
            for s in sym_tbl.getSymbols(a):
                if s.getName() == new_label:
                    s.setPrimary()
                    break
            renamed = True
    if eol and renamed:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)
    print("[REN] 0x%08x  %s -> %s" % (slot_addr, old_label, new_label))
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
# EQ_SLOTS: 70 total (all REUSE; NEW constants already added to *.inc files)
# Addresses verified against proposal EQ table.
# Note: 0x08093c08 and 0x08093c64 are REF slots (fmt_d), NOT EQ slots.
#       0x08093c0c is the PTR_gP1LifePoints EQ slot.
# Format: (slot_addr, value, eq_name, slot_label, eol_or_None)
# =============================================================================
EQ_SLOTS = [
    # --- clear_duel_puzzle_wram_regions (0x080935a4) ---
    (0x08093628, 0x0201c4e0, 'gP1LifePoints',               'ptr_gP1LifePoints_3628',            None),
    (0x0809362c, 0x00001db8, 'PUZZLE_CLEAR_HALF_COUNT_1DB8', 'puzzle_clear_half_count_1db8',     'PUZZLE_CLEAR_HALF_COUNT_1DB8'),
    (0x08093630, 0x0201e4f0, 'gEquipEffectZoneBase',         'ptr_gEquipEffectZoneBase_3630',     None),
    (0x08093634, 0x0201bcc0, 'gDuelDisplaySeqState',         'ptr_gDuelDisplaySeqState_3634',     None),
    (0x08093638, 0x0000081c, 'PUZZLE_CLEAR_HALF_COUNT_081C', 'puzzle_clear_half_count_081c',     'PUZZLE_CLEAR_HALF_COUNT_081C'),
    (0x0809363c, 0x0201e4d0, 'gEquipZoneRankState',          'ptr_gEquipZoneRankState_363c',      None),
    (0x08093640, 0x0201b290, 'gDuelPhaseFlags',              'ptr_gDuelPhaseFlags_3640',          None),
    (0x08093644, 0x000005d4, 'PUZZLE_CLEAR_HALF_COUNT_05D4', 'puzzle_clear_half_count_05d4',     'PUZZLE_CLEAR_HALF_COUNT_05D4'),
    (0x08093648, 0x0201bb90, 'gEquipChainSlotRefs',          'ptr_gEquipChainSlotRefs_3648',      None),
    (0x0809364c, 0x0201b1b0, 'gPuzzleCardAnimBuf',           'gPuzzleCardAnimBuf_364c',           'gPuzzleCardAnimBuf'),
    (0x08093650, 0x0201afe0, 'gEquipLpScoreBase',            'ptr_gEquipLpScoreBase_3650',        None),
    (0x08093654, 0x0201b870, 'gSpriteAttrBuf',               'ptr_gSpriteAttrBuf_3654',           None),
    (0x08093658, 0x0201e2a0, 'gDuelCardCtxBase',             'ptr_gDuelCardCtxBase_3658',         None),
    (0x0809365c, 0x00001d08, 'P1LP_BLOCK2_OFF',              'ptr_p1lp_block2_off_365c',          None),
    # --- init_duel_puzzle_field_and_hand_display (0x08093660) ---
    (0x0809370c, 0x0201c4e0, 'gP1LifePoints',               'ptr_gP1LifePoints_370c',            None),
    (0x08093710, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'ptr_player_block_stride_3710',      None),
    (0x08093714, 0x0201e2b4, 'gCardFsDataBlock',             'ptr_gCardFsDataBlock_3714',         None),
    (0x08093718, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',         'ptr_p1lp_block2_off_1ce8_3718',     None),
    (0x0809371c, 0x00001cf0, 'P1LP_BACKUP_DST_OFF',          'ptr_p1lp_backup_dst_off_371c',      None),
    (0x08093720, 0x0000ffff, 'SLOT_CARD_EMPTY',              'ptr_slot_card_empty_3720',          None),
    (0x08093778, 0x00001d08, 'P1LP_BLOCK2_OFF',              'ptr_p1lp_block2_off_3778',          None),
    (0x0809377c, 0x00008054, 'OAM_ZONE_UPDATE_SPRITE_P1',    'ptr_oam_zone_upd_spr_p1_377c',      None),
    # --- init_duel_puzzle_field_display_and_flags (0x08093780) ---
    (0x0809379c, 0x0201c4e0, 'gP1LifePoints',               'ptr_gP1LifePoints_379c',            None),
    (0x080937a0, 0x00001cf0, 'P1LP_BACKUP_DST_OFF',          'ptr_p1lp_backup_dst_off_37a0',      None),
    (0x080937a4, 0x00001d04, 'PUZZLE_READY_FLAG_OFF',        'puzzle_ready_flag_off',             'PUZZLE_READY_FLAG_OFF'),
    # --- init_duel_puzzle_scene_state (0x080937d4) ---
    (0x080937d0, 0x0201e2a0, 'gDuelCardCtxBase',             'ptr_gDuelCardCtxBase_37d0',         None),
    # --- write_lp_card_display_slot_entry (0x0809387c) ---
    (0x08093824, 0x0201c4e0, 'gP1LifePoints',               'ptr_gP1LifePoints_3824',            None),
    (0x08093828, 0x0201e2a0, 'gDuelCardCtxBase',             'ptr_gDuelCardCtxBase_3828',         None),
    (0x0809382c, 0x00001cec, 'P1LP_TIMER_OFF',               'ptr_p1lp_timer_off_382c',           None),
    (0x08093830, 0x00001cf0, 'P1LP_BACKUP_DST_OFF',          'ptr_p1lp_backup_dst_off_3830',      None),
    (0x08093834, 0x0000ffff, 'SLOT_CARD_EMPTY',              'ptr_slot_card_empty_3834',          None),
    (0x08093838, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',         'ptr_p1lp_block2_off_1ce8_3838',     None),
    # --- parse_duel_puzzle_text_token (0x080938d4) ---
    (0x080938c4, 0x0201c4e0, 'gP1LifePoints',               'ptr_gP1LifePoints_38c4',            None),
    (0x080938c8, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'ptr_player_block_stride_38c8',      None),
    (0x080938cc, 0x00001fff, 'SLOT_CARD_SET_CODE_MASK',      'ptr_slot_set_code_mask_38cc',       None),
    (0x080938d0, 0xffffe000, 'OAM_ATTR2_TILE_CLEAR',         'ptr_oam_attr2_tile_clear_38d0',     None),
    (0x08093948, 0x0201c4e0, 'gP1LifePoints',               'ptr_gP1LifePoints_3948',            None),
    (0x0809394c, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'ptr_player_block_stride_394c',      None),
    (0x080939d0, 0x0201c4e0, 'gP1LifePoints',               'ptr_gP1LifePoints_39d0',            None),
    (0x080939d4, 0x00001d18, 'EQUIP_MAIN_PHASE_OFF',         'ptr_equip_main_phase_off_39d4',     None),
    (0x080939e4, 0x0201c4e0, 'gP1LifePoints',               'ptr_gP1LifePoints_39e4',            None),
    (0x080939e8, 0x00001d18, 'EQUIP_MAIN_PHASE_OFF',         'ptr_equip_main_phase_off_39e8',     None),
    (0x080939f8, 0x0201c4e0, 'gP1LifePoints',               'ptr_gP1LifePoints_39f8',            None),
    (0x080939fc, 0x00001d18, 'EQUIP_MAIN_PHASE_OFF',         'ptr_equip_main_phase_off_39fc',     None),
    (0x08093a0c, 0x0201c4e0, 'gP1LifePoints',               'ptr_gP1LifePoints_3a0c',            None),
    (0x08093a10, 0x00001d18, 'EQUIP_MAIN_PHASE_OFF',         'ptr_equip_main_phase_off_3a10',     None),
    (0x08093a20, 0x0201c4e0, 'gP1LifePoints',               'ptr_gP1LifePoints_3a20',            None),
    (0x08093a24, 0x00001d18, 'EQUIP_MAIN_PHASE_OFF',         'ptr_equip_main_phase_off_3a24',     None),
    (0x08093ac4, 0x0201c4e0, 'gP1LifePoints',               'ptr_gP1LifePoints_3ac4',            None),
    (0x08093ac8, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'ptr_player_block_stride_3ac8',      None),
    (0x08093b10, 0x0201c4e0, 'gP1LifePoints',               'ptr_gP1LifePoints_3b10',            None),
    (0x08093b14, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'ptr_player_block_stride_3b14',      None),
    (0x08093b68, 0x0201c4e0, 'gP1LifePoints',               'ptr_gP1LifePoints_3b68',            None),
    (0x08093b6c, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'ptr_player_block_stride_3b6c',      None),
    (0x08093bb0, 0x0201c4e0, 'gP1LifePoints',               'ptr_gP1LifePoints_3bb0',            None),
    (0x08093bb4, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'ptr_player_block_stride_3bb4',      None),
    # NOTE: 0x08093c08 and 0x08093c64 are REF slots (puzzle_token_fmt_d), handled below
    (0x08093c0c, 0x0201c4e0, 'gP1LifePoints',               'ptr_gP1LifePoints_3c0c',            None),
    (0x08093c10, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'ptr_player_block_stride_3c10',      None),
    (0x08093c6c, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'ptr_player_block_stride_3c6c',      None),
    (0x08093c70, 0x0201c510, 'gDuelFieldSlots',              'ptr_gDuelFieldSlots_3c70',          None),
    (0x08093c74, 0x00001fff, 'SLOT_CARD_SET_CODE_MASK',      'ptr_slot_set_code_mask_3c74',       None),
    (0x08093c78, 0xffffe000, 'OAM_ATTR2_TILE_CLEAR',         'ptr_oam_attr2_tile_clear_3c78',     None),
    (0x08093cb4, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'ptr_player_block_stride_3cb4',      None),
    (0x08093cb8, 0x0201c510, 'gDuelFieldSlots',              'ptr_gDuelFieldSlots_3cb8',          None),
    (0x08093cf4, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'ptr_player_block_stride_3cf4',      None),
    (0x08093cf8, 0x0201c510, 'gDuelFieldSlots',              'ptr_gDuelFieldSlots_3cf8',          None),
    (0x08093d38, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'ptr_player_block_stride_3d38',      None),
    (0x08093d3c, 0x0201c510, 'gDuelFieldSlots',              'ptr_gDuelFieldSlots_3d3c',          None),
    (0x08093db0, 0x0201d9c8, 'gEquipNodePool_data',          'gEquipNodePool_data_db0',           'gEquipNodePool_data'),
    (0x08093db4, 0x0201e4f0, 'gEquipEffectZoneBase',         'ptr_gEquipEffectZoneBase_3db4',     None),
    # --- render_duel_puzzle_text_to_sprite_queue (0x08093fa8) ---
    (0x08094098, 0x0201c4e0, 'gP1LifePoints',               'ptr_gP1LifePoints_4098',            None),
    (0x0809409c, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'ptr_player_block_stride_409c',      None),
    (0x080940a0, 0x0000086c, 'PUZZLE_P2LP_SLOT_OFF',         'puzzle_p2lp_slot_off',              'PUZZLE_P2LP_SLOT_OFF'),
    (0x080940a4, 0x0201c510, 'gDuelFieldSlots',              'ptr_gDuelFieldSlots_40a4',          None),
    (0x080940a8, 0xffffe000, 'OAM_ATTR2_TILE_CLEAR',         'ptr_oam_attr2_tile_clear_40a8',     None),
    (0x080940ac, 0x00008073, 'PUZZLE_LP_SPRITE_P2_ATTR',     'puzzle_lp_sprite_p2_attr',          'PUZZLE_LP_SPRITE_P2_ATTR'),
    (0x080940b0, 0x0000803a, 'OAM_XY_SPLIT_SPRITE_P2',      'ptr_oam_xy_split_spr_p2_40b0',      None),
    (0x080941a8, 0x0201d9c8, 'gEquipNodePool_data',          'gEquipNodePool_data_1a8',           'gEquipNodePool_data'),
    (0x080941ac, 0x00008036, 'OAM_SPRITE_PAL_P1',            'ptr_oam_sprite_pal_p1_41ac',        None),
    (0x080941b0, 0x0201e4f0, 'gEquipEffectZoneBase',         'ptr_gEquipEffectZoneBase_41b0',     None),
    (0x080941b4, 0x0201c4e0, 'gP1LifePoints',               'ptr_gP1LifePoints_41b4',            None),
    (0x080941b8, 0x00008054, 'OAM_ZONE_UPDATE_SPRITE_P1',    'ptr_oam_zone_upd_spr_p1_41b8',      None),
    (0x080941bc, 0x00000874, 'LP_P2_LOOP_CEIL_OFF',          'ptr_lp_p2_loop_ceil_off_41bc',      None),
    (0x080941c0, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'ptr_player_block_stride_41c0',      None),
]

# =============================================================================
# REF_SLOTS: 25 string pointer slots (parse_duel_puzzle_text_token pool)
# puzzle_token_fmt_d (0x09e47478) is shared across 8 slots.
# Format: (slot_addr, target_addr, gas_label, slot_label)
# =============================================================================
REF_SLOTS = [
    (0x0809390c, 0x09e47464, 'puzzle_token_str_end',             'ptr_str_end_390c'),
    (0x08093940, 0x09e4746c, 'puzzle_token_str_player_lp',       'ptr_str_player_lp_3940'),
    # puzzle_token_fmt_d shared x8: 3944, 3ac0, 3b0c, 3b64, 3bac, 3c08, 3c64, 3dac
    (0x08093944, 0x09e47478, 'puzzle_token_fmt_d',               'ptr_fmt_d_3944'),
    (0x08093ac0, 0x09e47478, 'puzzle_token_fmt_d',               'ptr_fmt_d_3ac0'),
    (0x08093b0c, 0x09e47478, 'puzzle_token_fmt_d',               'ptr_fmt_d_3b0c'),
    (0x08093b64, 0x09e47478, 'puzzle_token_fmt_d',               'ptr_fmt_d_3b64'),
    (0x08093bac, 0x09e47478, 'puzzle_token_fmt_d',               'ptr_fmt_d_3bac'),
    (0x08093c08, 0x09e47478, 'puzzle_token_fmt_d',               'ptr_fmt_d_3c08'),
    (0x08093c64, 0x09e47478, 'puzzle_token_fmt_d',               'ptr_fmt_d_3c64'),
    (0x08093dac, 0x09e47478, 'puzzle_token_fmt_d',               'ptr_fmt_d_3dac'),
    (0x08093974, 0x09e4747c, 'puzzle_token_str_phase',           'ptr_str_phase_3974'),
    (0x08093a50, 0x09e47484, 'puzzle_token_str_card_in',         'ptr_str_card_in_3a50'),
    (0x08093c68, 0x09e4748c, 'puzzle_token_str_eq',              'ptr_str_eq_3c68'),
    (0x08093cb0, 0x09e47490, 'puzzle_token_str_face',            'ptr_str_face_3cb0'),
    (0x08093cf0, 0x09e47498, 'puzzle_token_str_turn',            'ptr_str_turn_3cf0'),
    (0x08093d34, 0x09e474a0, 'puzzle_token_str_param',           'ptr_str_param_3d34'),
    (0x08093da8, 0x09e474a8, 'puzzle_token_str_equip_act',       'ptr_str_equip_act_3da8'),
    (0x08093db8, 0x09e474b4, 'puzzle_token_str_src_player',      'ptr_str_src_player_3db8'),
    (0x08093de4, 0x09e474c0, 'puzzle_token_str_src_locate',      'ptr_str_src_locate_3de4'),
    (0x08093e08, 0x09e474cc, 'puzzle_token_str_src_card_id',     'ptr_str_src_card_id_3e08'),
    (0x08093e38, 0x09e474d8, 'puzzle_token_str_dst_player',      'ptr_str_dst_player_3e38'),
    (0x08093e64, 0x09e474e4, 'puzzle_token_str_dst_locate',      'ptr_str_dst_locate_3e64'),
    (0x08093e94, 0x09e474f0, 'puzzle_token_str_type',            'ptr_str_type_3e94'),
    (0x08093e98, 0x09e474f8, 'puzzle_token_str_only_in_turn',    'ptr_str_only_in_turn_3e98'),
    (0x08093eb8, 0x09e47504, 'puzzle_token_str_only_face_turn',  'ptr_str_only_face_turn_3eb8'),
    (0x08093ed8, 0x09e47514, 'puzzle_token_str_only_face',       'ptr_str_only_face_3ed8'),
    (0x08093ef8, 0x09e47520, 'puzzle_token_str_forever',         'ptr_str_forever_3ef8'),
    (0x08093f18, 0x09e47528, 'puzzle_token_str_permanent',       'ptr_str_permanent_3f18'),
    (0x08093f38, 0x09e47534, 'puzzle_token_str_during_face',     'ptr_str_during_face_3f38'),
    (0x08093f58, 0x09e47540, 'puzzle_token_str_equipment',       'ptr_str_equipment_3f58'),
    (0x08093f78, 0x09e4754c, 'puzzle_token_str_union',           'ptr_str_union_3f78'),
    (0x08093fa4, 0x09e47554, 'puzzle_token_str_captured',        'ptr_str_captured_3fa4'),
]

# =============================================================================
# RENAME_SLOTS: rename existing Ghidra auto-names (PTR_gP1LifePoints_* etc)
# Format: (slot_addr, old_label, new_label, eol_or_None)
# =============================================================================
RENAME_SLOTS = [
    (0x08093628, 'PTR_gP1LifePoints_08093628', 'ptr_gP1LifePoints_3628',  None),
    (0x08093824, 'PTR_gP1LifePoints_08093824', 'ptr_gP1LifePoints_3824',  None),
    (0x080938c4, 'PTR_gP1LifePoints_080938c4', 'ptr_gP1LifePoints_38c4',  None),
    (0x08093948, 'PTR_gP1LifePoints_08093948', 'ptr_gP1LifePoints_3948',  None),
    (0x080939d0, 'PTR_gP1LifePoints_080939d0', 'ptr_gP1LifePoints_39d0',  None),
    (0x080939e4, 'PTR_gP1LifePoints_080939e4', 'ptr_gP1LifePoints_39e4',  None),
    (0x080939f8, 'PTR_gP1LifePoints_080939f8', 'ptr_gP1LifePoints_39f8',  None),
    (0x08093a0c, 'PTR_gP1LifePoints_08093a0c', 'ptr_gP1LifePoints_3a0c',  None),
    (0x08093a20, 'PTR_gP1LifePoints_08093a20', 'ptr_gP1LifePoints_3a20',  None),
    (0x08093ac4, 'PTR_gP1LifePoints_08093ac4', 'ptr_gP1LifePoints_3ac4',  None),
    (0x08093b10, 'PTR_gP1LifePoints_08093b10', 'ptr_gP1LifePoints_3b10',  None),
    (0x08093b68, 'PTR_gP1LifePoints_08093b68', 'ptr_gP1LifePoints_3b68',  None),
    (0x08093bb0, 'PTR_gP1LifePoints_08093bb0', 'ptr_gP1LifePoints_3bb0',  None),
    (0x08093c0c, 'PTR_gP1LifePoints_08093c0c', 'ptr_gP1LifePoints_3c0c',  None),
    (0x08094098, 'PTR_gP1LifePoints_08094098', 'ptr_gP1LifePoints_4098',  None),
    (0x080941b4, 'PTR_gP1LifePoints_080941b4', 'ptr_gP1LifePoints_41b4',  None),
]

# =============================================================================
# CODE_PTR_SLOTS: 2 (jump-table .word entries pointing to code within same fn)
# These point to code, not to string table. Handled as pure rename.
# =============================================================================
CODE_PTR_SLOTS = [
    (0x08093978, 'DAT_08093978', 'switchD_08093972__switchdataD_0809397c', None),
    (0x08093a54, 'DAT_08093a54', 'switchD_08093a4c__switchdataD_08093a58',  None),
]

# =============================================================================
# PLATE_REWRITES: 9 function plates (all pure ASCII, all <= 500 chars)
# =============================================================================
PLATE_REWRITES = [
    # 0. play_card_ok_ui_effect (0x08093598): replace 2 stale FUN_
    (0x08093598,
     "Plays UI sound effect for card confirm/OK action. Called by process_card_play_ok_sequence (card/duel_field/prng scene dispatcher) and tick_equip_activation_main_sequence after card confirm/select operation. Body: push {lr}; movs r0,#0x31=49 (UI effect ID); bl play_ui_effect; pop {r1}; bx r1. Thin wrapper around play_ui_effect with fixed effect_id=0x31=49. Side effects: triggers sound effect ID 49 via play_ui_effect (indirect). Constants: CARD_OK_EFFECT_ID=0x31=49."),
    # 1. clear_duel_puzzle_wram_regions (0x080935a4): truncate + replace 2 stale FUN_
    (0x080935a4,
     "Clear EWRAM/display regions for duel_puzzle scene. init_duel_puzzle_field_and_hand_display and init_duel_puzzle_scene_state call this first. zero_fill_by_halfword x9: gP1LifePoints(0x1db8 hw), gEquipEffectZoneBase(0xc2*8 hw), gDuelDisplaySeqState(0x81c hw), gEquipZoneRankState(0x18 hw), gDuelPhaseFlags(0x5d4 hw), gEquipChainSlotRefs(0x98*2 hw), gPuzzleCardAnimBuf(0xd8 hw), gEquipLpScoreBase(0xe6*2 hw), gSpriteAttrBuf(0xc5*4 hw). If [ctx+8]==2 sets gP1LP[0x1d08]:=1. Clears ctx[0x224/0x228]:=0."),
    # 2. init_duel_puzzle_field_and_hand_display (0x08093660): truncate over-500
    (0x08093660,
     "Full field/hand OAM init hub for duel_puzzle scene entry. Seq: (1) clear_duel_puzzle_wram_regions; (2) set gP1LifePoints[0]/[0x868] to 0x1f40 (8000 initial LP); (3) init_player_hand_display_slots x2 for both players; (4) shuffle_player_hand_list x2; (5) 6x dispatch_card_display_op(0xd/0x14); (6) if scene_ctx+8==3 poll_sprite_seq_until_done(0). Callers: run_campaign_step26_init_duel_puzzle_scene + 2 others."),
    # 3. init_duel_puzzle_scene_state (0x080937d4): truncate over-500
    (0x080937d4,
     "Init duel puzzle scene state. Calls clear_duel_puzzle_wram_regions, then writes gP1LifePoints: [+0x1d00]:=1 (puzzle_mode_active), [+0x1cec]:=9 (stage counter), [+0x1cf0]:=0xffff (LP sentinel), [+0x1ce0]:=0, [+0x1ce8]:=0. Also inits gDuelCardCtxBase[+0/4/8]:=0, [+0xc]:=1, [+0x10]:=0. Finally calls render_duel_puzzle_text_to_sprite_queue(r4). Returns fixed 1. indeg=1, caller: addr 0x0801fec0 (duel scene switch dispatcher)."),
    # 4. init_duel_puzzle_hand_display_both_sides (0x080937a8): factual fix
    (0x080937a8,
     "Init duel_puzzle both-sides hand display. Calls init_duel_puzzle_field_and_hand_display, then build_hand_zone_display_slots_shuffled(player_id, r5) for local player (gDuelCardCtxBase[+0x10]) and opponent (1-player_id). Returns fixed 1. indeg=0, called via function pointer by scene state machine. r5=hand_ctx_param passed through to both build calls."),
    # 5. copy_text_line_to_buf (0x08093840): truncate over-500
    (0x08093840,
     "Copy one text line to buf byte-by-byte. r0=dst_buf, r1=max_len-1 (loop bound), r2=src_ptr_ptr. Reads *src_ptr_ptr; stops at null or newline (0x0a) or overflow. Writes null terminator; updates *src_ptr_ptr to next byte. Returns bytes written, or 0 on overflow. Called by render_duel_puzzle_text_to_sprite_queue in text-parse loop. NEWLINE=0x0a."),
    # 6. write_lp_card_display_slot_entry (0x0809387c): truncate over-500
    (0x0809387c,
     "Write LP card display slot entry for duel puzzle. r0=player (0/1), r1=lp_value. Writes lp_value into gP1LifePoints[player*PLAYER_BLOCK_STRIDE+4+count*4] and increments slot count. Updates VRAM halfword bits[12:0] at [gP1LP+player*PLAYER_BLOCK_STRIDE+0x1080]. Called by parse_duel_puzzle_text_token H-subcase after sscanf extracts LP value. MASK_LOW13=SLOT_CARD_SET_CODE_MASK(0x1fff), MASK_HIGH=OAM_ATTR2_TILE_CLEAR(0xffffe000)."),
    # 7. parse_duel_puzzle_text_token (0x080938d4): truncate over-500 + fix stale FUN_
    (0x080938d4,
     "Duel puzzle text script token parser. r0=line_buf_ptr. Dispatches on first byte: 0x45(E)->[END]->return 1; 0x43(C)->CardIn init; 0x50(P)->PlayerLP LP parse via sscanf; 0x5b([)->return 1; 0x53(S)->Phase sub-table (18-entry switch for scene state fields at gP1LP+EQUIP_MAIN_PHASE_OFF). Returns 0=continue, 1=done. Called by render_duel_puzzle_text_to_sprite_queue in loop."),
    # 8. render_duel_puzzle_text_to_sprite_queue (0x08093fa8): truncate over-500 + fix stale FUN_
    (0x08093fa8,
     "Render duel puzzle text to sprite queue. Called by init_duel_puzzle_scene_state. Inits gP1LP[0]/[0x868] to 0x1f40, gP1LP[4]:=1, gP1LP[PUZZLE_P2LP_SLOT_OFF]:=1. Loops: copy_text_line_to_buf + parse_duel_puzzle_text_token until done. Then iterates gEquipNodePool entries, calls enqueue_sprite_attr_record for each active LP sprite row, then 10x dispatch_card_display_op for field+hand ops. Returns void (Pattern B)."),
]


# =============================================================================
# MAIN
# =============================================================================
def main():
    eq_ok = eq_fail = 0
    ref_ok = ref_fail = 0
    ren_ok = ren_fail = 0
    plt_ok = plt_fail = 0

    print("=== RefineF11Seg10Slots  DRY=%s ===" % DRY)

    # -- EQ pass --
    print("\n--- EQ (%d slots) ---" % len(EQ_SLOTS))
    for (sa, v, eq_n, sl, eol) in EQ_SLOTS:
        if _apply_eq(sa, v, eq_n, sl, eol):
            eq_ok += 1
        else:
            eq_fail += 1

    # -- REF pass (string table pointers) --
    print("\n--- REF (%d slots) ---" % len(REF_SLOTS))
    for (sa, tv, gl, sl) in REF_SLOTS:
        if _apply_ref(sa, tv, gl, sl):
            ref_ok += 1
        else:
            ref_fail += 1

    # -- RENAME pass (PTR_ -> slot labels) --
    print("\n--- RENAME (%d slots) ---" % len(RENAME_SLOTS))
    for (sa, old, new, eol) in RENAME_SLOTS:
        if _apply_rename(sa, old, new, eol):
            ren_ok += 1
        else:
            ren_fail += 1

    # -- CODE_PTR pass (jump-table .word entries) --
    print("\n--- CODE_PTR (%d slots) ---" % len(CODE_PTR_SLOTS))
    for (sa, old, new, eol) in CODE_PTR_SLOTS:
        if _apply_rename(sa, old, new, eol):
            ren_ok += 1
        else:
            ren_fail += 1

    # -- PLATE pass --
    print("\n--- PLATE (%d rewrites) ---" % len(PLATE_REWRITES))
    for (fa, txt) in PLATE_REWRITES:
        if _apply_plate(fa, txt):
            plt_ok += 1
        else:
            plt_fail += 1

    print("\n=== SUMMARY ===")
    print("EQ  : %d OK  %d FAIL  (total=%d)" % (eq_ok,  eq_fail,  len(EQ_SLOTS)))
    print("REF : %d OK  %d FAIL  (total=%d)" % (ref_ok, ref_fail, len(REF_SLOTS)))
    print("REN : %d OK  %d FAIL  (total=%d / incl %d CODE_PTR)" % (
        ren_ok, ren_fail, len(RENAME_SLOTS)+len(CODE_PTR_SLOTS), len(CODE_PTR_SLOTS)))
    print("PLT : %d OK  %d FAIL  (total=%d)" % (plt_ok, plt_fail, len(PLATE_REWRITES)))
    total_fail = eq_fail + ref_fail + ren_fail + plt_fail
    if total_fail == 0:
        print("ALL PASS -- ready for export")
    else:
        print("FAILURES: %d -- investigate before export" % total_fail)


main()
