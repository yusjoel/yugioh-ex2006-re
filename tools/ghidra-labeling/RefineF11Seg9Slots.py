# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF11Seg9Slots.py -- f11 Seg-9 slot symbolization [0x08091888..0x08093598)
#
# ~20 named functions including eval_field_equip_activation_candidates (~0x1afc B, 187-pool BST)
# + flush_field_spell_equip_slot_sprites + 16 invoke_card_display_op_0x31_* stubs
#
# EQ:   176 total (141 REUSE + 35 NEW)
# REF:  2 (createLabel + addMemoryReference for 2 new RAM globals)
# RENAME: 11 (4 DWORD_ -> slot labels + 7 PTR_gP1LifePoints_ -> ptr_lp_*)
# PLATE: 2 (CJK->ASCII rewrite for flush_field_spell_equip_slot_sprites and invoke_..._sub1)
#
# NEW constants (added to constants/*.inc before this script):
#   card_info.inc: 35 new CID equates (Seg-9 BST nodes)
#   ewram.inc: gEquipActivationSlotBase=0x0201bc2c, gDuelFieldSlotState_ec=0x0201c5fc
#   duel_field.inc: EQUIP_ACTIVATION_CNT_CAP=0x0000ffff
#
# NOTE: All EOL/plate text is pure ASCII (no CJK). Ghidra Jython mojibake prevention.
# NOTE: WARN=FAIL: any failed setComment or value mismatch = FAIL, skip that item.

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
    # Create label at target (global) if not present
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
    # Set primary on new ref
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
    """Rename existing label (old_label) at slot_addr to new_label, set EOL."""
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
        # Label may already have been renamed, just ensure new name exists
        names = [s.getName() for s in sym_tbl.getSymbols(a)]
        if new_label in names:
            for s in sym_tbl.getSymbols(a):
                if s.getName() == new_label:
                    s.setPrimary()
                    break
            renamed = True
        else:
            print("WARN RENAME 0x%08x: old label %s not found (names=%s)" % (slot_addr, old_label, names))
            # Create new label anyway
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
# EQ_SLOTS: 176 total
# Format: (slot_addr, value, eq_name, slot_label, eol_or_None)
# =============================================================================
EQ_SLOTS = [
    # --- Group A: RAM-global addresses (REUSE gEquipChainSlotRefs = 0x0201bb90) ---
    (0x08091904, 0x0201bb90, 'gEquipChainSlotRefs', 'ptr_gEquipChainSlotRefs_1904', None),
    (0x08091954, 0x0201bb90, 'gEquipChainSlotRefs', 'ptr_gEquipChainSlotRefs_1954', None),
    (0x08091a90, 0x0201bb90, 'gEquipChainSlotRefs', 'ptr_gEquipChainSlotRefs_1a90', None),
    (0x08091b60, 0x0201bb90, 'gEquipChainSlotRefs', 'ptr_gEquipChainSlotRefs_1b60', None),
    (0x08091bec, 0x0201bb90, 'gEquipChainSlotRefs', 'ptr_gEquipChainSlotRefs_1bec', None),
    (0x08091d88, 0x0201bb90, 'gEquipChainSlotRefs', 'ptr_gEquipChainSlotRefs_1d88', None),
    (0x08091e44, 0x0201bb90, 'gEquipChainSlotRefs', 'ptr_gEquipChainSlotRefs_1e44', None),
    (0x08091ef4, 0x0201bb90, 'gEquipChainSlotRefs', 'ptr_gEquipChainSlotRefs_1ef4', None),
    (0x08091f94, 0x0201bb90, 'gEquipChainSlotRefs', 'ptr_gEquipChainSlotRefs_1f94', None),
    (0x0809229c, 0x0201bb90, 'gEquipChainSlotRefs', 'ptr_gEquipChainSlotRefs_229c', None),
    (0x08092308, 0x0201bb90, 'gEquipChainSlotRefs', 'ptr_gEquipChainSlotRefs_2308', None),
    (0x080923cc, 0x0201bb90, 'gEquipChainSlotRefs', 'ptr_gEquipChainSlotRefs_23cc', None),
    (0x080924c4, 0x0201bb90, 'gEquipChainSlotRefs', 'ptr_gEquipChainSlotRefs_24c4', None),
    (0x080924fc, 0x0201bb90, 'gEquipChainSlotRefs', 'ptr_gEquipChainSlotRefs_24fc', None),
    (0x0809286c, 0x0201bb90, 'gEquipChainSlotRefs', 'ptr_gEquipChainSlotRefs_286c', None),
    (0x08092ac4, 0x0201bb90, 'gEquipChainSlotRefs', 'ptr_gEquipChainSlotRefs_2ac4', None),
    (0x08092af8, 0x0201bb90, 'gEquipChainSlotRefs', 'ptr_gEquipChainSlotRefs_2af8', None),
    (0x08092b40, 0x0201bb90, 'gEquipChainSlotRefs', 'ptr_gEquipChainSlotRefs_2b40', None),
    (0x08092b78, 0x0201bb90, 'gEquipChainSlotRefs', 'ptr_gEquipChainSlotRefs_2b78', None),
    (0x08092bc4, 0x0201bb90, 'gEquipChainSlotRefs', 'ptr_gEquipChainSlotRefs_2bc4', None),
    (0x08092c20, 0x0201bb90, 'gEquipChainSlotRefs', 'ptr_gEquipChainSlotRefs_2c20', None),
    (0x08092c78, 0x0201bb90, 'gEquipChainSlotRefs', 'ptr_gEquipChainSlotRefs_2c78', None),
    (0x08092cb8, 0x0201bb90, 'gEquipChainSlotRefs', 'ptr_gEquipChainSlotRefs_2cb8', None),
    (0x08092ce4, 0x0201bb90, 'gEquipChainSlotRefs', 'ptr_gEquipChainSlotRefs_2ce4', None),
    (0x08092de0, 0x0201bb90, 'gEquipChainSlotRefs', 'ptr_gEquipChainSlotRefs_2de0', None),
    (0x08092e18, 0x0201bb90, 'gEquipChainSlotRefs', 'ptr_gEquipChainSlotRefs_2e18', None),
    (0x08093188, 0x0201bb90, 'gEquipChainSlotRefs', 'ptr_gEquipChainSlotRefs_3188', None),
    (0x08093248, 0x0201bb90, 'gEquipChainSlotRefs', 'ptr_gEquipChainSlotRefs_3248', None),
    (0x080932cc, 0x0201bb90, 'gEquipChainSlotRefs', 'ptr_gEquipChainSlotRefs_32cc', None),
    (0x0809337c, 0x0201bb90, 'gEquipChainSlotRefs', 'ptr_gEquipChainSlotRefs_337c', None),
    # Other RAM globals (REUSE)
    (0x080933b0, 0x0201e2a0, 'gDuelCardCtxBase',    'ptr_gDuelCardCtxBase_33b0',  None),
    (0x08092898, 0x0201c510, 'gDuelFieldSlots',     'ptr_gDuelFieldSlots_2898',   None),
    (0x08092360, 0x0201c510, 'gDuelFieldSlots',     'ptr_gDuelFieldSlots_2360',   None),
    (0x08092c80, 0x0201c510, 'gDuelFieldSlots',     'ptr_gDuelFieldSlots_2c80',   None),
    (0x0809289c, 0x0201d9c0, 'gEquipNodePool',      'ptr_gEquipNodePool_289c',    None),
    (0x080931b8, 0x0201d9c0, 'gEquipNodePool',      'ptr_gEquipNodePool_31b8',    None),
    (0x080928a0, 0x0201c520, 'gDuelFieldSlotState', 'ptr_gDuelFieldSlotState_28a0', None),
    (0x080931bc, 0x0201c520, 'gDuelFieldSlotState', 'ptr_gDuelFieldSlotState_31bc', None),
    (0x08093470, 0x0201e4f0, 'gEquipEffectZoneBase','ptr_gEquipEffectZoneBase_3470', None),
    # flush_field_spell_equip_slot_sprites duel slots dup
    (0x080931b4, 0x0201c510, 'gDuelFieldSlots',     'ptr_duel_slots_31b4',        None),

    # --- Group B: PLAYER_BLOCK_STRIDE (REUSE 0x00000868) ---
    (0x0809190c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'equip_player_stride_190c',   None),
    (0x08091d9c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'equip_player_stride_1d9c',   None),
    (0x0809287c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'equip_player_stride_287c',   None),
    (0x08092c7c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'equip_player_stride_2c7c',   None),
    (0x08092d14, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'equip_player_stride_2d14',   None),
    (0x0809235c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'equip_player_stride_235c',   None),
    (0x080923f8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'equip_player_stride_23f8',   None),
    (0x08093198, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'equip_player_stride_3198',   None),

    # --- Group C: Known score/mask constants (REUSE) ---
    (0x08091f98, 0x000016a3, 'DARK_SCORPION_COMBO_CID',           'cid_dark_scorpion_1f98',  'DARK_SCORPION_COMBO_CID'),
    (0x08091f9c, 0x00001663, 'ROD_OF_THE_MINDS_EYE_CID',          'cid_rod_minds_eye_1f9c',  'ROD_OF_THE_MINDS_EYE_CID'),
    (0x08091fa0, 0x00001890, 'UNION_ATTACK_CID',                   'cid_union_attack_1fa0',   'UNION_ATTACK_CID'),
    (0x080921c8, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',               'lp_block2_off_21c8',      None),
    (0x080921cc, 0x00001cf4, 'P2LP_BLOCK2_OFF_1CF4',               'lp_block2_off_21cc',      None),
    (0x080921e4, 0x0000076b, 'FIELD5_SCORE_ACTIVATION_THRESHOLD',  'score_thresh_21e4',       None),
    (0x080921fc, 0xffff0000, 'EQUIP_CHAIN_SENTINEL',               'chain_sentinel_21fc',     None),
    (0x08092afc, 0xffff0000, 'EQUIP_CHAIN_SENTINEL',               'chain_sentinel_2afc',     None),
    (0x08093380, 0x0000ffff, 'EQUIP_ACTIVATION_CNT_CAP',           'act_cnt_cap_3380',        None),
    (0x08093474, 0xffffe000, 'OAM_ATTR2_TILE_CLEAR',               'attr2_tile_clr_3474',     None),
    (0x08093478, 0x00001fff, 'SLOT_CARD_SET_CODE_MASK',            'set_code_mask_3478',      None),
    # LP score offsets dup pass
    (0x08092abc, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',               'lp_block2_off_2abc',      None),
    (0x08092ac0, 0x00001cf4, 'P2LP_BLOCK2_OFF_1CF4',               'lp_block2_off_2ac0',      None),
    (0x08092adc, 0x0000076b, 'FIELD5_SCORE_ACTIVATION_THRESHOLD',  'score_thresh_2adc',       None),

    # --- Group D: CID BST first pass [0x08091888..0x08091bff] ---
    (0x080919d0, 0x000016ff, 'DARK_DRICERATOPS_CID',               'cid_dark_drice_19d0',     None),
    (0x080919d4, 0x0000154c, 'EXARION_UNIVERSE_CID',               'cid_exarion_19d4',        None),
    (0x080919d8, 0x00001416, 'MAD_SWORD_BEAST_CID',                'cid_mad_sword_19d8',      None),
    (0x080919e0, 0x000014d6, 'SPEAR_DRAGON_CID',                   'cid_spear_dragon_19e0',   None),
    (0x080919f4, 0x00001651, 'GYAKU_GIRE_PANDA_CID',               'cid_gyaku_panda_19f4',    None),
    (0x080919fc, 0x0000168b, 'MEFIST_THE_INFERNAL_GENERAL_CID',    'cid_mefist_19fc',         None),
    (0x08091a18, 0x0000194d, 'ELEMENTAL_HERO_BLADEDGE_CID',        'cid_bladedge_1a18',       None),
    (0x08091a24, 0x000018fd, 'CYBER_END_DRAGON_CID',               'cid_cyber_end_1a24',      None),
    (0x08091a40, 0x00001991, 'RANCER_DRAGONUTE_CID',               'cid_rancer_1a40',         None),
    (0x08091a50, 0x000019c9, 'SABER_BEETLE_CID',                   'cid_saber_beetle_1a50',   None),
    (0x08091a94, 0x000015f2, 'METEORAIN_CID',                      'cid_meteorain_1a94',      None),
    (0x08091aa0, 0x000016fc, 'ENRAGED_BATTLE_OX_CID',              'cid_enraged_ox_1aa0',     None),
    (0x08091b50, 0x000014e3, 'DRAGONS_RAGE_CID',                   'cid_dragons_rage_1b50',   None),
    (0x08091b54, 0x00000fcb, 'GAIA_THE_DRAGON_CHAMPION_CID',       'cid_gaia_dragon_1b54',    None),
    (0x08091b58, 0x0000147b, 'SWIFT_GAIA_THE_FIERCE_KNIGHT_CID',   'cid_swift_gaia_1b58',     None),
    (0x08091b5c, 0x0000187d, 'SPIRAL_SPEAR_STRIKE_CID',            'cid_spiral_spear_1b5c',   None),
    (0x08091b64, 0x00001408, 'FAIRY_METEOR_CRUSH_CID',             'cid_fairy_meteor_1b64',   None),
    (0x08091b68, 0x00001625, 'BIG_BANG_SHOT_CID',                  'cid_big_bang_1b68',       None),
    (0x08091b6c, 0x00001496, 'CYCLON_LASER_CID',                   'cid_cyclon_laser_1b6c',   None),
    (0x08091b70, 0x000015ce, 'PITCH_DARK_DRAGON_CID',              'cid_pitch_dark_1b70',     None),
    (0x08091bf0, 0x00001408, 'FAIRY_METEOR_CRUSH_CID',             'cid_fairy_meteor_1bf0',   None),
    (0x08091bf4, 0x00001625, 'BIG_BANG_SHOT_CID',                  'cid_big_bang_1bf4',       None),
    (0x08091bf8, 0x00001496, 'CYCLON_LASER_CID',                   'cid_cyclon_laser_1bf8',   None),
    (0x08091bfc, 0x000015ce, 'PITCH_DARK_DRAGON_CID',              'cid_pitch_dark_1bfc',     None),
    (0x08091c20, 0x00001883, 'CROSS_COUNTER_CID',                  'cid_cross_counter_1c20',  None),
    (0x08091c5c, 0x000019f2, 'FAULT_ZONE_CID',                     'cid_fault_zone_1c5c',     None),

    # --- Group E: CID BST second pass first block [0x08091d84..0x08091f93] ---
    (0x08091d84, 0x00001493, 'DESTRUCTION_PUNCH_CID',              'cid_dest_punch_1d84',     None),
    (0x08091d8c, 0x00001883, 'CROSS_COUNTER_CID',                  'cid_cross_counter_1d8c',  None),
    (0x08091d90, 0x0000162e, 'CONTINUOUS_DESTRUCTION_PUNCH_CID',   'cid_cont_dest_punch_1d90',None),
    (0x08091d94, 0x0000151e, 'LAST_TURN_CID',                      'cid_last_turn_1d94',      None),
    (0x08091da4, 0x000010f4, 'UMI_CARD_ID',                        'cid_umi_1da4',            None),
    (0x08091da8, 0x000013f7, 'TORNADO_WALL_CID',                   'cid_tornado_wall_1da8',   None),
    (0x08091dac, 0x0000175e, 'SANCTUARY_IN_THE_SKY_CID',           'cid_sanctuary_1dac',      None),
    (0x08091e40, 0x0000179d, 'EMISSARY_OF_OASIS_CID',              'cid_emissary_1e40',       None),
    (0x08091e48, 0x000018aa, 'WINGED_KURIBOH_CID',                 'cid_winged_kuri_1e48',    None),
    (0x08091e4c, 0x000017fe, 'SPIRIT_BARRIER_CID',                 'cid_spirit_barrier_1e4c', None),
    (0x08091e50, 0x00001989, 'BUBBLE_BLASTER_CID',                 'cid_bubble_blast_1e50',   None),
    (0x08091ef8, 0x00001989, 'BUBBLE_BLASTER_CID',                 'cid_bubble_blast_1ef8',   None),
    (0x08091efc, 0x00001805, 'HALLOWED_LIFE_BARRIER_CID',          'cid_hallow_life_1efc',    None),
    (0x08091f00, 0x000015ec, 'KISHIDO_SPIRIT_CID',                 'cid_kishido_1f00',        None),
    (0x08091f04, 0x0000168d, 'SHADOWKNIGHT_ARCHFIEND_CID',         'cid_shadowknight_1f04',   None),
    (0x08091f10, 0x00001750, 'PIRANHA_ARMY_CID',                   'cid_piranha_army_1f10',   None),

    # --- Group F: CID BST second large pass [0x08091fec..0x08092500] ---
    (0x08091fec, 0x0000164d, 'GUARDIAN_BAOU_CID',                  'cid_guardian_baou_1fec',  None),
    (0x08091ff0, 0x000014e9, 'KAISER_GLIDER_CID',                  'cid_kaiser_glider_1ff0',  None),
    (0x08091ff4, 0x000012ac, 'SATELLITE_CANNON_CID',               'cid_satellite_1ff4',      None),
    (0x08092004, 0x000013cb, 'ROCKET_WARRIOR_CID',                 'cid_rocket_warrior_2004', None),
    (0x08092020, 0x000014af, 'AMAZONESS_FIGHTER_CID',              'cid_amazoness_ftr_2020',  None),
    (0x08092038, 0x000014b6, 'DARK_BALTER_THE_TERRIBLE_CID',       'cid_dark_balter_2038',    None),
    (0x08092058, 0x00001596, 'SPIRIT_REAPER_CID',                  'cid_spirit_reaper_2058',  None),
    (0x08092068, 0x0000157e, 'FGD_CID',                            'cid_fgd_2068',            None),
    (0x0809207c, 0x00001622, 'ULTIMATE_OBEDIENT_FIEND_CID',        'cid_ult_obedient_207c',   None),
    (0x08092094, 0x00001642, 'DARK_FLARE_KNIGHT_CID',              'cid_dark_flare_2094',     None),
    (0x080920c8, 0x00001855, 'CASTLE_GATE_CID',                    'cid_castle_gate_20c8',    None),
    (0x080920d8, 0x00001743, 'UNHAPPY_GIRL_CID',                   'cid_unhappy_girl_20d8',   None),
    (0x080920ec, 0x00001827, 'ELEMENT_SAURUS_CID',                 'cid_element_saurus_20ec', None),
    (0x080920fc, 0x0000182b, 'HARPIE_LADY_2_CID',                  'cid_harpie_lady2_20fc',   None),
    (0x08092124, 0x00001913, 'BES_CRYSTAL_CORE_CID',               'cid_bes_crystal_2124',    None),
    (0x08092134, 0x000018b8, 'MONK_FIGHTER_CID',                   'cid_monk_fighter_2134',   None),
    (0x08092150, 0x00001955, 'CYBER_BLADER_CID',                   'cid_cyber_blader_2150',   None),
    (0x08092164, 0x00001962, 'BES_TETRAN_CID',                     'cid_bes_tetran_2164',     None),
    (0x08092438, 0x0000170d, 'GETSU_FUHMA_CID',                    'cid_getsu_fuhma_2438',    None),
    (0x0809242c, 0x0000170e, 'RYU_KOKKI_CID',                      'cid_ryu_kokki_242c',      None),
    (0x08092450, 0x00001866, 'KANGAROO_CHAMP_CID',                 'cid_kangaroo_2450',       None),
    (0x08092464, 0x00001950, 'OXYGEDDON_CID',                      'cid_oxygeddon_2464',      None),
    (0x08092500, 0x000017d5, 'DARK_MIMIC_LV1_CID',                 'cid_dark_mimic_2500',     None),

    # --- Group G: CID BST third large pass [0x08092870..0x08092e1c] ---
    (0x08092870, 0x00001663, 'ROD_OF_THE_MINDS_EYE_CID',           'cid_rod_minds_eye_2870',  None),
    (0x08092874, 0x00001890, 'UNION_ATTACK_CID',                   'cid_union_attack_2874',   None),
    (0x08092880, 0x00001594, 'CHARM_OF_SHABTI_CID',                'cid_charm_shabti_2880',   None),
    (0x08092884, 0x00001805, 'HALLOWED_LIFE_BARRIER_CID',          'cid_hallow_life_2884',    None),
    (0x08092888, 0x0000150a, 'HEART_OF_CLEAR_WATER_CID',           'cid_heart_clear_2888',    None),
    (0x0809288c, 0x000017ff, 'NINJITSU_ART_OF_DECOY_CID',          'cid_ninjitsu_288c',       None),
    (0x08092890, 0x00001992, 'MISTOBODY_CID',                      'cid_mistobody_2890',      None),
    (0x08092894, 0x00001957, 'ELEMENTAL_HERO_TEMPEST_CID',         'cid_eh_tempest_2894',     None),
    (0x080928a4, 0x00001989, 'BUBBLE_BLASTER_CID',                 'cid_bubble_blast_28a4',   None),
    (0x080928a8, 0x000015b3, 'Z_METAL_TANK_CID',                   'cid_z_metal_28a8',        None),
    (0x080928ac, 0x000015ff, 'DIFFUSION_WAVE_MOTION_CID',          'cid_diffusion_28ac',      None),
    (0x080928b0, 0x0000165f, 'WICKED_BREAKING_FLAMBERGE_BAOU_CID', 'cid_wicked_flamberge_28b0', None),
    (0x080928b4, 0x000014b5, 'DARK_RULER_HA_DES_CID',              'cid_dark_ruler_28b4',     None),
    (0x080928b8, 0x000018cd, 'KAMINOTE_BLOW_CID',                  'cid_kaminote_28b8',       None),
    (0x080928bc, 0x0000164d, 'GUARDIAN_BAOU_CID',                  'cid_guardian_baou_28bc',  None),
    (0x080928c0, 0x000014e9, 'KAISER_GLIDER_CID',                  'cid_kaiser_glider_28c0',  None),
    (0x080928e8, 0x000012ac, 'SATELLITE_CANNON_CID',               'cid_satellite_28e8',      None),
    (0x080928f8, 0x000013cb, 'ROCKET_WARRIOR_CID',                 'cid_rocket_warrior_28f8', None),
    (0x08092914, 0x000014af, 'AMAZONESS_FIGHTER_CID',              'cid_amazoness_ftr_2914',  None),
    (0x08092924, 0x000014b6, 'DARK_BALTER_THE_TERRIBLE_CID',       'cid_dark_balter_2924',    None),
    (0x08092944, 0x00001596, 'SPIRIT_REAPER_CID',                  'cid_spirit_reaper_2944',  None),
    (0x08092954, 0x0000157e, 'FGD_CID',                            'cid_fgd_2954',            None),
    (0x08092968, 0x00001622, 'ULTIMATE_OBEDIENT_FIEND_CID',        'cid_ult_obedient_2968',   None),
    (0x08092980, 0x00001642, 'DARK_FLARE_KNIGHT_CID',              'cid_dark_flare_2980',     None),
    (0x080929b4, 0x00001855, 'CASTLE_GATE_CID',                    'cid_castle_gate_29b4',    None),
    (0x080929c4, 0x00001743, 'UNHAPPY_GIRL_CID',                   'cid_unhappy_girl_29c4',   None),
    (0x080929d8, 0x00001827, 'ELEMENT_SAURUS_CID',                 'cid_element_saurus_29d8', None),
    (0x080929e8, 0x0000182b, 'HARPIE_LADY_2_CID',                  'cid_harpie_lady2_29e8',   None),
    (0x08092a10, 0x00001913, 'BES_CRYSTAL_CORE_CID',               'cid_bes_crystal_2a10',    None),
    (0x08092a20, 0x000018b8, 'MONK_FIGHTER_CID',                   'cid_monk_fighter_2a20',   None),
    (0x08092a3c, 0x00001955, 'CYBER_BLADER_CID',                   'cid_cyber_blader_2a3c',   None),
    (0x08092a54, 0x00001962, 'BES_TETRAN_CID',                     'cid_bes_tetran_2a54',     None),
    (0x08092d48, 0x0000170e, 'RYU_KOKKI_CID',                      'cid_ryu_kokki_2d48',      None),
    (0x08092d54, 0x0000170d, 'GETSU_FUHMA_CID',                    'cid_getsu_fuhma_2d54',    None),
    (0x08092d6c, 0x00001866, 'KANGAROO_CHAMP_CID',                 'cid_kangaroo_2d6c',       None),
    (0x08092d80, 0x00001950, 'OXYGEDDON_CID',                      'cid_oxygeddon_2d80',      None),
    (0x08092e1c, 0x000017d5, 'DARK_MIMIC_LV1_CID',                 'cid_dark_mimic_2e1c',     None),

    # --- Group H: CID BST fourth pass [0x08093188..0x080931d4] (flush_field sub-dispatch) ---
    (0x0809318c, 0x00001663, 'ROD_OF_THE_MINDS_EYE_CID',           'cid_rod_minds_eye_318c',  None),
    (0x08093190, 0x00001890, 'UNION_ATTACK_CID',                   'cid_union_attack_3190',   None),
    (0x0809319c, 0x00001594, 'CHARM_OF_SHABTI_CID',                'cid_charm_shabti_319c',   None),
    (0x080931a0, 0x00001805, 'HALLOWED_LIFE_BARRIER_CID',          'cid_hallow_life_31a0',    None),
    (0x080931a4, 0x0000150a, 'HEART_OF_CLEAR_WATER_CID',           'cid_heart_clear_31a4',    None),
    (0x080931a8, 0x000017ff, 'NINJITSU_ART_OF_DECOY_CID',          'cid_ninjitsu_31a8',       None),
    (0x080931ac, 0x00001992, 'MISTOBODY_CID',                      'cid_mistobody_31ac',      None),
    (0x080931b0, 0x00001957, 'ELEMENTAL_HERO_TEMPEST_CID',         'cid_eh_tempest_31b0',     None),
    (0x080931c0, 0x00001989, 'BUBBLE_BLASTER_CID',                 'cid_bubble_blast_31c0',   None),
    (0x080931c4, 0x000015b3, 'Z_METAL_TANK_CID',                   'cid_z_metal_31c4',        None),
    (0x080931c8, 0x0000165f, 'WICKED_BREAKING_FLAMBERGE_BAOU_CID', 'cid_wicked_flamberge_31c8', None),
    (0x080931cc, 0x000014b5, 'DARK_RULER_HA_DES_CID',              'cid_dark_ruler_31cc',     None),
    (0x080931d0, 0x000018cd, 'KAMINOTE_BLOW_CID',                  'cid_kaminote_31d0',       None),
    (0x080931d4, 0x00001392, 'SWORD_OF_DRAGONS_SOUL_CID',          'cid_sword_dragon_31d4',   None),
    (0x0809324c, 0x000018f1, 'GYROID_CID',                         'cid_gyroid_324c',         None),
    (0x08093250, 0x00000fb6, 'TIME_WIZARD_CID',                    'cid_time_wizard_3250',    None),
    (0x080932c8, 0x000018f1, 'GYROID_CID',                         'cid_gyroid_32c8',         None),
    (0x080932d0, 0x00000fb6, 'TIME_WIZARD_CID',                    'cid_time_wizard_32d0',    None),
]

# =============================================================================
# REF_SLOTS: 2
# Format: (slot_addr, target_addr, gas_label, slot_label, eol_or_None)
# =============================================================================
REF_SLOTS = [
    (0x08091d98, 0x0201bc2c, 'gEquipActivationSlotBase', 'ptr_equip_act_slot_base_1d98',
     'gEquipActivationSlotBase = gEquipChainSlotRefs+0x9c; 2-entry is_activated array'),
    (0x08091da0, 0x0201c5fc, 'gDuelFieldSlotState_ec',   'ptr_duel_field_state_ec_1da0',
     'gDuelFieldSlots+0xec; bits[23:22] 2-bit state field; player*0x868 offset at runtime'),
]

# =============================================================================
# RENAME_SLOTS: 11
# Format: (slot_addr, old_label, new_label, eol_or_None)
# =============================================================================
RENAME_SLOTS = [
    # 4 DWORD_ -> slot labels
    (0x08091f94, 'DWORD_08091f94', 'ptr_gEquipChainSlotRefs_1f94', None),
    (0x08091f98, 'DWORD_08091f98', 'cid_dark_scorpion_1f98',       'DARK_SCORPION_COMBO_CID'),
    (0x08091f9c, 'DWORD_08091f9c', 'cid_rod_minds_eye_1f9c',       'ROD_OF_THE_MINDS_EYE_CID'),
    (0x08091fa0, 'DWORD_08091fa0', 'cid_union_attack_1fa0',        'UNION_ATTACK_CID'),
    # 7 PTR_gP1LifePoints_ -> ptr_lp_*
    (0x08091908, 'PTR_gP1LifePoints_08091908', 'ptr_lp_91908', 'gP1LifePoints (0x0201c4e0)'),
    (0x080921c4, 'PTR_gP1LifePoints_080921c4', 'ptr_lp_921c4', 'gP1LifePoints (0x0201c4e0)'),
    (0x080923f4, 'PTR_gP1LifePoints_080923f4', 'ptr_lp_923f4', 'gP1LifePoints (0x0201c4e0)'),
    (0x08092878, 'PTR_gP1LifePoints_08092878', 'ptr_lp_92878', 'gP1LifePoints (0x0201c4e0)'),
    (0x08092ab8, 'PTR_gP1LifePoints_08092ab8', 'ptr_lp_92ab8', 'gP1LifePoints (0x0201c4e0)'),
    (0x08092d10, 'PTR_gP1LifePoints_08092d10', 'ptr_lp_92d10', 'gP1LifePoints (0x0201c4e0)'),
    (0x08093194, 'PTR_gP1LifePoints_08093194', 'ptr_lp_93194', 'gP1LifePoints (0x0201c4e0)'),
]

# =============================================================================
# PLATE_SLOTS: 2 (CJK->ASCII rewrites; stale FUN_ already substituted in text)
# =============================================================================
PLATE_SLOTS = [
    (0x080931de,
     "Callee of eval_field_equip_activation_candidates (indeg=6+). Guards: gEquipChainSlotRefs[+0x8] (busy) or sp[0x8] (ctx_flag) nonzero -> return. If [r4+0x2c] (activation_pending) set and r7==0: tests [r4+0x10] via check_value_in_slot_chain(chain=TIME_WIZARD_CID,5); on miss: clears [r4+0x2c], enqueues up to 3 OAM calls; on hit: 1 OAM call. P2 mirror at sp[0x10]. Side effects: [r4+0x2c]=0; up to 3 enqueue_sprite_attr calls."),
    (0x080933b4,
     "3-instruction thunk (indeg=36). Fixed params op=0x31, sub=0x1; remaps entry r0 as dispatch_card_display_op 3rd arg (r2), r3=0. Call form: dispatch_card_display_op(0x31, 0x1, r0_in, 0). op=0x31 = copy_game_text_to_card_name_vram cluster; sub=0x1 vs sub=0x2 variant (invoke_card_display_op_0x31_with_params at 0x080933c8). Called by duel_field/card_frame/card_stats/game_str/font_jp modules. Side effects: via dispatch_card_display_op op=0x31: card-name VRAM buffer write. Constants: OP=0x31, SUB=0x1."),
]


# =============================================================================
# MAIN
# =============================================================================
def main():
    eq_ok = eq_fail = 0
    ref_ok = ref_fail = 0
    ren_ok = ren_fail = 0
    plt_ok = plt_fail = 0

    print("=== RefineF11Seg9Slots %s ===" % ("DRY" if DRY else "REAL"))

    print("--- EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    for slot_addr, value, eq_name, slot_label, eol in EQ_SLOTS:
        if _apply_eq(slot_addr, value, eq_name, slot_label, eol):
            eq_ok += 1
        else:
            eq_fail += 1

    print("--- REF_SLOTS (%d) ---" % len(REF_SLOTS))
    for slot_addr, target_val, gas_label, slot_label, eol in REF_SLOTS:
        if _apply_ref(slot_addr, target_val, gas_label, slot_label, eol):
            ref_ok += 1
        else:
            ref_fail += 1

    print("--- RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    for slot_addr, old_label, new_label, eol in RENAME_SLOTS:
        if _apply_rename(slot_addr, old_label, new_label, eol):
            ren_ok += 1
        else:
            ren_fail += 1

    print("--- PLATE_SLOTS (%d) ---" % len(PLATE_SLOTS))
    for fn_addr, plate_text in PLATE_SLOTS:
        if _apply_plate(fn_addr, plate_text):
            plt_ok += 1
        else:
            plt_fail += 1

    print("=== SUMMARY: EQ %d/%d  REF %d/%d  RENAME %d/%d  PLATE %d/%d  FAIL=%d ===" % (
        eq_ok, eq_ok + eq_fail,
        ref_ok, ref_ok + ref_fail,
        ren_ok, ren_ok + ren_fail,
        plt_ok, plt_ok + plt_fail,
        eq_fail + ref_fail + ren_fail + plt_fail))


main()
