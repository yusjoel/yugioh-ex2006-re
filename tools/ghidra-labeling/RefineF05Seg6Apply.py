# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF05Seg6Apply.py -- file-05 Seg-6 (0x0804d124..0x0804ffba)
#   Seg-6a: 0x0804d124..0x0804f6c4 (sprite-row anim/queue dispatch cluster)
#   Seg-6b: 0x0804f6c4..0x0804ffba (check_slot_card_eligible_by_card_id BST hub)
#
# Sections:
#   A. EQ_SLOTS  -- data-equate (~129 slots)
#   B. REF_SLOTS -- 2 slots (jump table pointers)
#   C. RENAME_SLOTS -- 2 slots (scalar renames with EOL)
#   D. PLATE_SUBS -- update plate comments (9 stale FUN_ replacements, 13 occurrences)
#   E. DISASM -- 2 ROM_INCBIN blocks (handled by separate DisassembleSeg6*.py)
#
# All EOL/plate text is pure ASCII.
from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"): DRY = True
except Exception:
    pass

def _addr(offset):
    return toAddr(offset)

def _check(addr_int, expected_val, label):
    """Verify ROM word at addr matches expected value; return True if ok."""
    mem = currentProgram.getMemory()
    a = _addr(addr_int)
    try:
        actual = mem.getInt(a) & 0xffffffff
        if actual != (expected_val & 0xffffffff):
            print("FAIL value_check %s @0x%08x: expected=0x%08x actual=0x%08x" % (
                label, addr_int, expected_val & 0xffffffff, actual))
            return False
        return True
    except Exception as e:
        print("FAIL value_check %s @0x%08x: exception %s" % (label, addr_int, str(e)))
        return False

def apply_eq_slot(slot_addr, value, const_name, slot_label):
    """Create equate + label at slot_addr."""
    if not _check(slot_addr, value, const_name):
        return False
    if DRY:
        print("DRY EQ 0x%08x %s = %s" % (slot_addr, slot_label, const_name))
        return True
    try:
        eqtbl = currentProgram.getEquateTable()
        eq = eqtbl.getEquate(const_name)
        if eq is None:
            eq = eqtbl.createEquate(const_name, value & 0xffffffff)
        eq.addReference(_addr(slot_addr), 0)
        sm = currentProgram.getSymbolTable()
        sm.createLabel(_addr(slot_addr), slot_label, SourceType.USER_DEFINED)
        print("OK  EQ 0x%08x %s = %s" % (slot_addr, slot_label, const_name))
        return True
    except Exception as e:
        print("ERR EQ 0x%08x %s: %s" % (slot_addr, slot_label, str(e)))
        return False

def apply_ref_slot(slot_addr, target_addr, gas_label, slot_label):
    """Create USER label at target + DATA ref from slot, label slot."""
    if DRY:
        print("DRY REF 0x%08x -> 0x%08x (%s / %s)" % (slot_addr, target_addr, gas_label, slot_label))
        return True
    try:
        sm = currentProgram.getSymbolTable()
        sm.createLabel(_addr(target_addr), gas_label, SourceType.USER_DEFINED)
        rf = currentProgram.getReferenceManager()
        ref = rf.addMemoryReference(_addr(slot_addr), _addr(target_addr), RefType.DATA, SourceType.USER_DEFINED, 0)
        # setPrimary via symbol setPrimary (not reference)
        try:
            ref.setPrimary(True)
        except Exception:
            pass  # not all Ghidra versions support this on MemReferenceDB
        sm.createLabel(_addr(slot_addr), slot_label, SourceType.USER_DEFINED)
        print("OK  REF 0x%08x -> 0x%08x (%s)" % (slot_addr, target_addr, slot_label))
        return True
    except Exception as e:
        print("ERR REF 0x%08x: %s" % (slot_addr, str(e)))
        return False

def apply_rename_slot(slot_addr, label, eol_ascii):
    """Rename data slot and optionally set EOL comment (ASCII only)."""
    if DRY:
        print("DRY REN 0x%08x %s eol=%s" % (slot_addr, label, repr(eol_ascii)))
        return True
    try:
        sm = currentProgram.getSymbolTable()
        sm.createLabel(_addr(slot_addr), label, SourceType.USER_DEFINED)
        if eol_ascii:
            listing = currentProgram.getListing()
            cu = listing.getCodeUnitAt(_addr(slot_addr))
            if cu:
                cu.setComment(CodeUnit.EOL_COMMENT, eol_ascii)
        print("OK  REN 0x%08x %s" % (slot_addr, label))
        return True
    except Exception as e:
        print("ERR REN 0x%08x %s: %s" % (slot_addr, label, str(e)))
        return False

def apply_plate(func_addr, plate_text):
    """Set plate comment on function at func_addr (ASCII text only)."""
    if DRY:
        print("DRY PLATE 0x%08x [%d chars]" % (func_addr, len(plate_text)))
        return True
    try:
        listing = currentProgram.getListing()
        cu = listing.getCodeUnitAt(_addr(func_addr))
        if cu is None:
            print("WARN PLATE 0x%08x: no code unit" % func_addr)
            return False
        cu.setComment(CodeUnit.PLATE_COMMENT, plate_text)
        print("OK  PLATE 0x%08x" % func_addr)
        return True
    except Exception as e:
        print("ERR PLATE 0x%08x: %s" % (func_addr, str(e)))
        return False

# ---------------------------------------------------------------------------
# A. EQ_SLOTS: (slot_addr, value, const_name, slot_label)
# ---------------------------------------------------------------------------
EQ_SLOTS = [

    # --- Seg-6a: dispatch_sprite_row_anim_by_state literal pool ---
    # ewram.inc EXISTS: gDuelPhaseFlags=0x0201b290
    (0x0804d218, 0x0201b290, 'gDuelPhaseFlags',        'dispatch_sprite_row_anim_phase_flags'),
    # ewram.inc NEW: SPRITE_ROW_ANIM_CTL_OFF=0x00000494
    (0x0804d21c, 0x00000494, 'SPRITE_ROW_ANIM_CTL_OFF','sprite_row_anim_ctl_off_s'),

    # --- Seg-6a: reset_sprite_row_queue_tail literal pool ---
    (0x0804db44, 0x0201b290, 'gDuelPhaseFlags',        'gDuelPhaseFlags_s_b'),
    # ewram.inc NEW: SPRITE_ROW_ANIM_STATE_OFF=0x0000048c
    (0x0804db48, 0x0000048c, 'SPRITE_ROW_ANIM_STATE_OFF', 'sprite_row_anim_state_off_s'),
    # ewram.inc NEW: SPRITE_ROW_QUEUE_STATE_OFF=0x0000049c
    (0x0804db4c, 0x0000049c, 'SPRITE_ROW_QUEUE_STATE_OFF', 'sprite_row_queue_state_off_s'),

    (0x0804db88, 0x0201b290, 'gDuelPhaseFlags',        'gDuelPhaseFlags_s_c'),
    (0x0804dbac, 0x0201b290, 'gDuelPhaseFlags',        'gDuelPhaseFlags_s_d'),
    (0x0804dbb0, 0x0000049c, 'SPRITE_ROW_QUEUE_STATE_OFF', 'sprite_row_queue_state_off_s_b'),

    # --- Seg-6a: flush_sprite_row_queue_partial literal pool ---
    (0x0804f0e0, 0x0201b290, 'gDuelPhaseFlags',        'gDuelPhaseFlags_s_e'),
    (0x0804f1cc, 0x0201b290, 'gDuelPhaseFlags',        'gDuelPhaseFlags_s_f'),
    (0x0804f1d4, 0x0000048c, 'SPRITE_ROW_ANIM_STATE_OFF', 'sprite_row_anim_state_off_s_b'),
    (0x0804f1d8, 0x00000494, 'SPRITE_ROW_ANIM_CTL_OFF', 'sprite_row_anim_ctl_off_s_b'),

    # --- Seg-6a: compact_equip_zone_rank3_entries literal pool ---
    (0x0804f288, 0x0201b290, 'gDuelPhaseFlags',        'gDuelPhaseFlags_s_g'),
    (0x0804f2d4, 0x0201b290, 'gDuelPhaseFlags',        'gDuelPhaseFlags_s_h'),
    (0x0804f2d8, 0x0000048c, 'SPRITE_ROW_ANIM_STATE_OFF', 'sprite_row_anim_state_off_s_c'),
    (0x0804f2dc, 0x00000494, 'SPRITE_ROW_ANIM_CTL_OFF', 'sprite_row_anim_ctl_off_s_c'),
    (0x0804f2f4, 0x0201b290, 'gDuelPhaseFlags',        'gDuelPhaseFlags_s_i'),
    (0x0804f2f8, 0x0000048c, 'SPRITE_ROW_ANIM_STATE_OFF', 'sprite_row_anim_state_off_s_d'),

    # --- Seg-6a: advance_equip_zone_rank_state literal pool ---
    (0x0804f3ac, 0x0201b290, 'gDuelPhaseFlags',        'gDuelPhaseFlags_s_j'),
    # demo_state.inc EXISTS: DEMO_CLEAR_BITS_8_1=0xfffffe01
    (0x0804f3b0, 0xfffffe01, 'DEMO_CLEAR_BITS_8_1',   'rank_field_mask_s'),
    (0x0804f3b4, 0x0000048c, 'SPRITE_ROW_ANIM_STATE_OFF', 'sprite_row_anim_state_off_s_e'),
    (0x0804f3e0, 0xfffffe01, 'DEMO_CLEAR_BITS_8_1',   'rank_field_mask_s_b'),
    (0x0804f3e4, 0x0201b290, 'gDuelPhaseFlags',        'gDuelPhaseFlags_s_k'),
    (0x0804f3e8, 0x0000048c, 'SPRITE_ROW_ANIM_STATE_OFF', 'sprite_row_anim_state_off_s_f'),
    (0x0804f418, 0xfffffe01, 'DEMO_CLEAR_BITS_8_1',   'rank_field_mask_s_c'),
    (0x0804f41c, 0x0201b290, 'gDuelPhaseFlags',        'gDuelPhaseFlags_s_l'),
    (0x0804f43c, 0xfffffe01, 'DEMO_CLEAR_BITS_8_1',   'rank_field_mask_s_d'),

    # --- Seg-6a: check_equip_slot_eligibility_with_whitelist literal pool ---
    # ewram.inc EXISTS: PLAYER_BLOCK_STRIDE=0x00000868
    (0x0804f49c, 0x00000868, 'PLAYER_BLOCK_STRIDE',   'player_block_stride_s'),
    # ewram.inc EXISTS: gDuelFieldSlots=0x0201c510
    (0x0804f4a0, 0x0201c510, 'gDuelFieldSlots',        'gduelfield_slots_s'),

    # --- Seg-6a: check_equip_slot_eligible_with_owner_and_type literal pool ---
    (0x0804f4cc, 0x00000868, 'PLAYER_BLOCK_STRIDE',   'player_block_stride_s_b'),
    (0x0804f4d0, 0x0201c510, 'gDuelFieldSlots',        'gduelfield_slots_s_b'),

    # --- Seg-6a: check_equip_slot_eligible_triple_predicate literal pool ---
    (0x0804f540, 0x00000868, 'PLAYER_BLOCK_STRIDE',   'player_block_stride_s_c'),
    (0x0804f544, 0x0201c510, 'gDuelFieldSlots',        'gduelfield_slots_s_c'),

    # --- Seg-6a: check_equip_slot_eligible_by_owner_and_prereqs literal pool ---
    (0x0804f5b4, 0x00000868, 'PLAYER_BLOCK_STRIDE',   'player_block_stride_s_d'),
    (0x0804f5b8, 0x0201c510, 'gDuelFieldSlots',        'gduelfield_slots_s_d'),

    # --- Seg-6a: check_equip_slot_eligible_with_whitelist_and_type literal pool ---
    (0x0804f608, 0x00000868, 'PLAYER_BLOCK_STRIDE',   'player_block_stride_s_e'),
    (0x0804f60c, 0x0201c510, 'gDuelFieldSlots',        'gduelfield_slots_s_e'),

    # --- Seg-6a: check_equip_target_matches_card_owner literal pool ---
    (0x0804f678, 0x00000868, 'PLAYER_BLOCK_STRIDE',   'player_block_stride_s_f'),
    (0x0804f67c, 0x0201c510, 'gDuelFieldSlots',        'gduelfield_slots_s_f'),

    # --- Seg-6a: check_equip_target_matches_card_owner sentinel ---
    # card_info.inc EXISTS: SLOT_CARD_EMPTY=0x0000ffff
    (0x0804f6c0, 0x0000ffff, 'SLOT_CARD_EMPTY',       'slot_card_empty_s'),

    # --- Seg-6a: advance_equip_zone_rank_state struct base ---
    # ewram.inc NEW: gEquipZoneRankState=0x0201e4d0
    (0x0804f368, 0x0201e4d0, 'gEquipZoneRankState',   'equip_zone_rank_state_base_s'),

    # --- Seg-6b: check_slot_card_eligible_by_card_id BST head ---
    (0x0804f71c, 0x00000868, 'PLAYER_BLOCK_STRIDE',   'player_block_stride_s_g'),
    (0x0804f720, 0x0201c510, 'gDuelFieldSlots',        'gduelfield_slots_s_g'),

    # --- Seg-6b: BST literal pool (CIDs) ---
    (0x0804f7c8, 0x00000868, 'PLAYER_BLOCK_STRIDE',   'player_block_stride_s_h'),
    (0x0804f7cc, 0x0201c510, 'gDuelFieldSlots',        'gduelfield_slots_s_h'),

    # card_info.inc NEW: CYCLON_LASER_CID=0x00001496
    (0x0804f7d0, 0x00001496, 'CYCLON_LASER_CID',      'check_slot_cid_cyclon_laser'),
    # card_info.inc EXISTS: MAGICAL_LABYRINTH_CID=0x00001232
    (0x0804f7d4, 0x00001232, 'MAGICAL_LABYRINTH_CID', 'check_slot_cid_magic_labyrinth'),

    # card_info.inc EXISTS: COCOON_OF_EVOLUTION_CID=0x00000fee
    (0x0804f7f0, 0x00000fee, 'COCOON_OF_EVOLUTION_CID','check_slot_cid_cocoon_evol'),
    # card_info.inc EXISTS: MAGICAL_LABYRINTH_CID reuse at f7d4 (already above)
    # DWORD_0804f80c=0x000010da -> cid_10da (NEW unallocated)
    (0x0804f80c, 0x000010da, 'cid_10da',              'check_slot_cid_10da'),

    # card_info.inc EXISTS: AMPLIFIER_CID=0x000012d3
    (0x0804f834, 0x000012d3, 'AMPLIFIER_CID',         'check_slot_cid_amplifier'),
    # cid_10e2 (NEW unallocated)
    (0x0804f84c, 0x000010e2, 'cid_10e2',              'check_slot_cid_10e2'),
    # cid_10ea (NEW unallocated)
    (0x0804f870, 0x000010ea, 'cid_10ea',              'check_slot_cid_10ea'),
    # cid_10eb (NEW unallocated)
    (0x0804f888, 0x000010eb, 'cid_10eb',              'check_slot_cid_10eb'),

    # cid_12ef (NEW unallocated)
    (0x0804f8bc, 0x000012ef, 'cid_12ef',              'check_slot_cid_12ef'),
    # cid_10ee (NEW unallocated)
    (0x0804f8c0, 0x000010ee, 'cid_10ee',              'check_slot_cid_10ee'),

    # card_info.inc EXISTS: MAGICAL_LABYRINTH_CID=0x1232; note: 0x1232 also at f8d0
    (0x0804f8d0, 0x00001232, 'MAGICAL_LABYRINTH_CID', 'check_slot_cid_magic_labyrinth_b'),
    # cid_12c6 (NEW unallocated)
    (0x0804f8ec, 0x000012c6, 'cid_12c6',              'check_slot_cid_12c6'),

    # card_info.inc EXISTS: AMPLIFIER_CID=0x12d3; note 0x12d3 also at f904
    (0x0804f904, 0x000012d3, 'AMPLIFIER_CID',         'check_slot_cid_amplifier_b'),
    # card_info.inc EXISTS: PREMATURE_BURIAL_CID=0x00001366
    (0x0804f938, 0x00001366, 'PREMATURE_BURIAL_CID',  'check_slot_cid_premature_burial'),
    # card_info.inc EXISTS: SNATCH_STEAL_CID=0x00001322
    (0x0804f948, 0x00001322, 'SNATCH_STEAL_CID',      'check_slot_cid_snatch_steal'),
    # card_info.inc EXISTS: LIGHTNING_BLADE_CID=0x000013f6
    (0x0804f964, 0x000013f6, 'LIGHTNING_BLADE_CID',   'check_slot_cid_lightning_blade'),
    # card_info.inc EXISTS: DARK_NECROFEAR_CID=0x00001466
    (0x0804f97c, 0x00001466, 'DARK_NECROFEAR_CID',    'check_slot_cid_dark_necrofear'),

    # card_info.inc EXISTS: OPTI_CAMO_ARMOR_CID=0x00001759
    (0x0804f9c0, 0x00001759, 'OPTI_CAMO_ARMOR_CID',  'check_slot_cid_opti_camo'),
    # card_info.inc EXISTS: KIRYU_CID=0x000015cf
    (0x0804f9c4, 0x000015cf, 'KIRYU_CID',             'check_slot_cid_kiryu'),

    # card_info.inc EXISTS: HEART_OF_CLEAR_WATER_CID=0x0000150a
    (0x0804f9d4, 0x0000150a, 'HEART_OF_CLEAR_WATER_CID','check_slot_cid_heart_clear_water'),
    # card_info.inc EXISTS: BUSTER_RANCHER_CID - NEW
    (0x0804f9f0, 0x0000159e, 'BUSTER_RANCHER_CID',   'check_slot_cid_buster_rancher'),

    # card_info.inc NEW: Y_DRAGON_HEAD_CID=0x000015b0
    (0x0804fa08, 0x000015b0, 'Y_DRAGON_HEAD_CID',    'check_slot_cid_y_dragon_head'),
    # card_info.inc NEW: Z_METAL_TANK_CID=0x000015b3
    (0x0804fa0c, 0x000015b3, 'Z_METAL_TANK_CID',     'check_slot_cid_z_metal_tank'),

    # card_info.inc NEW: FREEZING_BEAST_CID=0x000015d7 (already exists from earlier batch?)
    (0x0804fa34, 0x000015d7, 'FREEZING_BEAST_CID',   'check_slot_cid_freezing_beast'),
    # card_info.inc NEW: SECOND_GOBLIN_CID=0x000015d3
    (0x0804fa38, 0x000015d3, 'SECOND_GOBLIN_CID',    'check_slot_cid_second_goblin'),

    # card_info.inc NEW: DES_DENDLE_CID=0x000015d5
    (0x0804fa50, 0x000015d5, 'DES_DENDLE_CID',       'check_slot_cid_des_dendle'),

    # card_info.inc EXISTS: METALLIZING_PARASITE_CID=0x00001693
    (0x0804fa74, 0x00001693, 'METALLIZING_PARASITE_CID','check_slot_cid_metallizing_parasite'),
    # card_info.inc EXISTS: FALLING_DOWN_CID=0x0000169a
    (0x0804fa8c, 0x0000169a, 'FALLING_DOWN_CID',     'check_slot_cid_falling_down'),

    # card_info.inc NEW: SPARK_BLASTER_CID=0x00001909 (already exists)
    (0x0804fac0, 0x00001909, 'SPARK_BLASTER_CID',    'check_slot_cid_spark_blaster'),
    # card_info.inc NEW: RITUAL_WEAPON_CID=0x000017fb
    (0x0804fad8, 0x000017fb, 'RITUAL_WEAPON_CID',    'check_slot_cid_ritual_weapon'),

    # card_info.inc NEW: LEGENDARY_BLACK_BELT_CID=0x000018d0
    (0x0804fafc, 0x000018d0, 'LEGENDARY_BLACK_BELT_CID','check_slot_cid_legendary_black_belt'),
    # card_info.inc EXISTS: NITRO_UNIT_CID=0x000018d1
    (0x0804fb08, 0x000018d1, 'NITRO_UNIT_CID',       'check_slot_cid_nitro_unit'),

    # card_info.inc NEW: DIVINE_SWORD_PHOENIX_BLADE_CID=0x0000193a
    (0x0804fb44, 0x0000193a, 'DIVINE_SWORD_PHOENIX_BLADE_CID','check_slot_cid_div_sword_phoenix'),
    # card_info.inc NEW: ADHESIVE_EXPLOSIVE_CID=0x000019bd
    (0x0804fb68, 0x000019bd, 'ADHESIVE_EXPLOSIVE_CID','check_slot_cid_adhesive_explosive'),

    # card_info.inc EXISTS: SYMBOL_OF_HERITAGE_CID=0x000019d7
    (0x0804fb80, 0x000019d7, 'SYMBOL_OF_HERITAGE_CID','check_slot_cid_symbol_of_heritage'),

    # card_info.inc EXISTS: PETIT_MOTH_CID=0x000010bc (NEW to add)
    (0x0804fbfc, 0x000010bc, 'PETIT_MOTH_CID',       'check_slot_cid_petit_moth'),
    # card_info.inc EXISTS: COCOON_OF_EVOLUTION_CID=0x00000fee
    (0x0804fc00, 0x00000fee, 'COCOON_OF_EVOLUTION_CID','check_slot_cid_cocoon_evol_b'),

    # card_info.inc EXISTS: HARPIE_LADY_CID=0x00000fe4
    (0x0804fc1c, 0x00000fe4, 'HARPIE_LADY_CID',      'check_slot_cid_harpie_lady'),
    # card_info.inc EXISTS: HARPIE_LADY_SISTERS_CID=0x00000fe5
    (0x0804fc20, 0x00000fe5, 'HARPIE_LADY_SISTERS_CID','check_slot_cid_harpie_sisters'),

    # card_info.inc EXISTS: LABYRINTH_WALL_CID=0x00001114 (NEW to add)
    (0x0804fc2c, 0x00001114, 'LABYRINTH_WALL_CID',   'check_slot_cid_labyrinth_wall'),
    # card_info.inc EXISTS: JINZO_CID=0x00001296
    (0x0804fc38, 0x00001296, 'JINZO_CID',             'check_slot_cid_jinzo'),

    # card_info.inc EXISTS: DARK_MAGICIAN_GIRL_CID=0x0000129e
    (0x0804fc54, 0x0000129e, 'DARK_MAGICIAN_GIRL_CID','check_slot_cid_dark_mag_girl'),
    # card_info.inc EXISTS: DARK_MAGICIAN_CID_0FC9=0x00000fc9
    (0x0804fc58, 0x00000fc9, 'DARK_MAGICIAN_CID_0FC9','check_slot_cid_dark_mag_0fc9'),

    # card_info.inc EXISTS: DARK_MAGICIAN_CID_142D=0x0000142d
    (0x0804fc68, 0x0000142d, 'DARK_MAGICIAN_CID_142D','check_slot_cid_dark_mag_142d'),
    # card_info.inc EXISTS: GRADIUS_CID=0x00001414
    (0x0804fc74, 0x00001414, 'GRADIUS_CID',           'check_slot_cid_gradius'),

    # card_info.inc NEW: FIELD5_SCORE_THRESHOLD_1299=0x00000513
    (0x0804fc94, 0x00000513, 'FIELD5_SCORE_THRESHOLD_1299','check_slot_field5_score_thresh'),

    # card_info.inc NEW: CHU_SKE_MOUSE_FIGHTER_CID=0x0000185a
    (0x0804fd4c, 0x0000185a, 'CHU_SKE_MOUSE_FIGHTER_CID','check_slot_cid_chu_ske'),
    # card_info.inc NEW: EHERO_SPARKMAN_CID=0x000018a9
    (0x0804fd58, 0x000018a9, 'EHERO_SPARKMAN_CID',   'check_slot_cid_ehero_sparkman'),

    # card_info.inc EXISTS: CARD_STAT_LP_THRESHOLD_1500=0x000005dc
    (0x0804fd78, 0x000005dc, 'CARD_STAT_LP_THRESHOLD_1500','check_slot_lp_threshold_1500'),
    # card_info.inc EXISTS: EHERO_BUBBLEMAN_CID=0x000018f9
    (0x0804fd88, 0x000018f9, 'EHERO_BUBBLEMAN_CID',  'check_slot_cid_bubbleman'),

    # card_info.inc EXISTS: EHERO_WILDHEART_CID=0x0000194e
    (0x0804fd9c, 0x0000194e, 'EHERO_WILDHEART_CID',  'check_slot_cid_wildheart'),
    # card_info.inc NEW: WHITE_MAGICIAN_PIKERU_CID=0x00001757
    (0x0804fdb4, 0x00001757, 'WHITE_MAGICIAN_PIKERU_CID','check_slot_cid_wm_pikeru'),
    # card_info.inc NEW: EBON_MAGICIAN_CURRAN_CID=0x0000191d
    (0x0804fdb8, 0x0000191d, 'EBON_MAGICIAN_CURRAN_CID','check_slot_cid_ebon_curran'),

    # card_info.inc NEW: DARK_BLADE_CID=0x000015cd
    (0x0804fdfc, 0x000015cd, 'DARK_BLADE_CID',       'check_slot_cid_dark_blade'),
    # card_info.inc NEW: DECAYED_COMMANDER_CID=0x000015d0
    (0x0804fe10, 0x000015d0, 'DECAYED_COMMANDER_CID','check_slot_cid_decayed_commander'),
    # card_info.inc NEW: GIANT_ORC_CID=0x000015d2
    (0x0804fe24, 0x000015d2, 'GIANT_ORC_CID',        'check_slot_cid_giant_orc'),
    # card_info.inc NEW: SECOND_GOBLIN_CID reuse at 0x15d3
    (0x0804fe38, 0x000015d3, 'SECOND_GOBLIN_CID',    'check_slot_cid_second_goblin_b'),
    # card_info.inc NEW: BURNING_BEAST_CID=0x000015d6
    (0x0804fe5c, 0x000015d6, 'BURNING_BEAST_CID',    'check_slot_cid_burning_beast'),
    # card_info.inc NEW: AITSU_CID=0x0000160a
    (0x0804fe64, 0x0000160a, 'AITSU_CID',            'check_slot_cid_aitsu'),
    # card_info.inc NEW: SOITSU_CID=0x0000190b
    (0x0804fe6c, 0x0000190b, 'SOITSU_CID',           'check_slot_cid_soitsu'),

    # PLAYER_BLOCK_STRIDE/gDuelFieldSlots at tail of check_slot_card_eligible_by_card_id
    (0x0804fedc, 0x00000868, 'PLAYER_BLOCK_STRIDE',   'player_block_stride_s_i'),
    (0x0804fee0, 0x0201c510, 'gDuelFieldSlots',        'gduelfield_slots_s_i'),

    # card_info.inc NEW: INDOMITABLE_FIGHTER_LEI_LEI_CID=0x00001915
    (0x0804fef4, 0x00001915, 'INDOMITABLE_FIGHTER_LEI_LEI_CID','check_slot_cid_lei_lei'),
    # card_info.inc NEW: V_TIGER_JET_CID=0x00001947
    (0x0804ff14, 0x00001947, 'V_TIGER_JET_CID',      'check_slot_cid_v_tiger_jet'),

    # --- Seg-6b: unallocated CIDs ---
    # cid_10d4
    (0x0804f7f0, 0x00000fee, 'COCOON_OF_EVOLUTION_CID','check_slot_cid_cocoon_evol_c'),  # placeholder - already above
    # NOTE: 0x0804f7f0 appears twice (0x0fee) - handled above, skip duplicate

    # cid_10e5
    (0x0804f834, 0x000012d3, 'AMPLIFIER_CID',         'check_slot_cid_amplifier_c'),  # 0x12d3 f834 already above, skip
]

# NOTE: remove exact duplicates from the list
# 0x0804f7f0 handled already as COCOON_OF_EVOLUTION_CID
# The list above may have inadvertent duplicates - Ghidra will handle gracefully

# Clean approach: separate out the remaining CID slots that map to unallocated IDs
EQ_SLOTS_UNK = [
    # cid_10d4 - NOT in list above since we need correct addr. Let me check proposal again
    # DAT_0804f7f0=0x000010d4 - wait, proposal says DAT_0804f7f0=0x000010d4
    # but I see cocoon_of_evolution at 0x0804f7f0=0x000010d4? Re-check proposal:
    # "DAT_0804f7f0=0x000010d4" -- so 0x0804f7f0=0x10d4, NOT 0x0fee
    # But I wrote 0x0fee above. Need to fix. This will be caught by _check().
]

# ---------------------------------------------------------------------------
# CORRECTION: Build final EQ list properly based on proposal table
# ---------------------------------------------------------------------------
# Re-read proposal carefully for Seg-6b CID values
# The proposal shows:
#   DAT_0804f7d0=0x00001496 CYCLON_LASER_CID
#   DAT_0804f7d4=0x000010ed cid_10ed  (NOT MAGICAL_LABYRINTH 0x1232!)
# Wait - let me re-check the proposal table for Seg-6b
# From proposal lines 77-113:
#   DAT_0804f7d0=0x00001496, DAT_0804f7d4=0x000010ed
#   DAT_0804f7f0=0x000010d4, DWORD_0804f80c=0x000010da
#   DAT_0804f834=0x000010e5, DAT_0804f84c=0x000010e2
#   DAT_0804f870=0x000010ea, DAT_0804f888=0x000010eb
#   DAT_0804f8bc=0x000012ef, DAT_0804f8c0=0x000010ee
#   DAT_0804f8d0=0x00001232, DAT_0804f8ec=0x000012c6
#   DAT_0804f904=0x000012d3, DAT_0804f938=0x00001366
# So I need to REBUILD the Seg-6b EQ_SLOTS correctly.

# Let me rebuild entire EQ list from scratch with correct proposal values:
EQ_SLOTS = [

    # =====================================================================
    # Seg-6a EQ_SLOTS
    # =====================================================================

    # dispatch_sprite_row_anim_by_state
    (0x0804d218, 0x0201b290, 'gDuelPhaseFlags',           'dispatch_sprite_row_anim_phase_flags'),
    (0x0804d21c, 0x00000494, 'SPRITE_ROW_ANIM_CTL_OFF',   'sprite_row_anim_ctl_off_s'),

    # reset_sprite_row_queue_tail
    (0x0804db44, 0x0201b290, 'gDuelPhaseFlags',           'gDuelPhaseFlags_s_b'),
    (0x0804db48, 0x0000048c, 'SPRITE_ROW_ANIM_STATE_OFF', 'sprite_row_anim_state_off_s'),
    (0x0804db4c, 0x0000049c, 'SPRITE_ROW_QUEUE_STATE_OFF','sprite_row_queue_state_off_s'),
    (0x0804db88, 0x0201b290, 'gDuelPhaseFlags',           'gDuelPhaseFlags_s_c'),
    (0x0804dbac, 0x0201b290, 'gDuelPhaseFlags',           'gDuelPhaseFlags_s_d'),
    (0x0804dbb0, 0x0000049c, 'SPRITE_ROW_QUEUE_STATE_OFF','sprite_row_queue_state_off_s_b'),

    # flush_sprite_row_queue_partial
    (0x0804f0e0, 0x0201b290, 'gDuelPhaseFlags',           'gDuelPhaseFlags_s_e'),

    # compact_equip_zone_rank3_entries / flush
    (0x0804f1cc, 0x0201b290, 'gDuelPhaseFlags',           'gDuelPhaseFlags_s_f'),
    (0x0804f1d4, 0x0000048c, 'SPRITE_ROW_ANIM_STATE_OFF', 'sprite_row_anim_state_off_s_b'),
    (0x0804f1d8, 0x00000494, 'SPRITE_ROW_ANIM_CTL_OFF',   'sprite_row_anim_ctl_off_s_b'),

    (0x0804f288, 0x0201b290, 'gDuelPhaseFlags',           'gDuelPhaseFlags_s_g'),
    (0x0804f2d4, 0x0201b290, 'gDuelPhaseFlags',           'gDuelPhaseFlags_s_h'),
    (0x0804f2d8, 0x0000048c, 'SPRITE_ROW_ANIM_STATE_OFF', 'sprite_row_anim_state_off_s_c'),
    (0x0804f2dc, 0x00000494, 'SPRITE_ROW_ANIM_CTL_OFF',   'sprite_row_anim_ctl_off_s_c'),
    (0x0804f2f4, 0x0201b290, 'gDuelPhaseFlags',           'gDuelPhaseFlags_s_i'),
    (0x0804f2f8, 0x0000048c, 'SPRITE_ROW_ANIM_STATE_OFF', 'sprite_row_anim_state_off_s_d'),

    # advance_equip_zone_rank_state
    (0x0804f368, 0x0201e4d0, 'gEquipZoneRankState',       'equip_zone_rank_state_base_s'),
    (0x0804f3ac, 0x0201b290, 'gDuelPhaseFlags',           'gDuelPhaseFlags_s_j'),
    (0x0804f3b0, 0xfffffe01, 'DEMO_CLEAR_BITS_8_1',       'rank_field_mask_s'),
    (0x0804f3b4, 0x0000048c, 'SPRITE_ROW_ANIM_STATE_OFF', 'sprite_row_anim_state_off_s_e'),
    (0x0804f3e0, 0xfffffe01, 'DEMO_CLEAR_BITS_8_1',       'rank_field_mask_s_b'),
    (0x0804f3e4, 0x0201b290, 'gDuelPhaseFlags',           'gDuelPhaseFlags_s_k'),
    (0x0804f3e8, 0x0000048c, 'SPRITE_ROW_ANIM_STATE_OFF', 'sprite_row_anim_state_off_s_f'),
    (0x0804f418, 0xfffffe01, 'DEMO_CLEAR_BITS_8_1',       'rank_field_mask_s_c'),
    (0x0804f41c, 0x0201b290, 'gDuelPhaseFlags',           'gDuelPhaseFlags_s_l'),
    (0x0804f43c, 0xfffffe01, 'DEMO_CLEAR_BITS_8_1',       'rank_field_mask_s_d'),

    # eligibility predicates
    (0x0804f49c, 0x00000868, 'PLAYER_BLOCK_STRIDE',       'player_block_stride_s'),
    (0x0804f4a0, 0x0201c510, 'gDuelFieldSlots',           'gduelfield_slots_s'),
    (0x0804f4cc, 0x00000868, 'PLAYER_BLOCK_STRIDE',       'player_block_stride_s_b'),
    (0x0804f4d0, 0x0201c510, 'gDuelFieldSlots',           'gduelfield_slots_s_b'),
    (0x0804f540, 0x00000868, 'PLAYER_BLOCK_STRIDE',       'player_block_stride_s_c'),
    (0x0804f544, 0x0201c510, 'gDuelFieldSlots',           'gduelfield_slots_s_c'),
    (0x0804f5b4, 0x00000868, 'PLAYER_BLOCK_STRIDE',       'player_block_stride_s_d'),
    (0x0804f5b8, 0x0201c510, 'gDuelFieldSlots',           'gduelfield_slots_s_d'),
    (0x0804f608, 0x00000868, 'PLAYER_BLOCK_STRIDE',       'player_block_stride_s_e'),
    (0x0804f60c, 0x0201c510, 'gDuelFieldSlots',           'gduelfield_slots_s_e'),
    (0x0804f678, 0x00000868, 'PLAYER_BLOCK_STRIDE',       'player_block_stride_s_f'),
    (0x0804f67c, 0x0201c510, 'gDuelFieldSlots',           'gduelfield_slots_s_f'),

    # SLOT_CARD_EMPTY sentinel
    (0x0804f6c0, 0x0000ffff, 'SLOT_CARD_EMPTY',           'slot_card_empty_s'),

    # =====================================================================
    # Seg-6b EQ_SLOTS (check_slot_card_eligible_by_card_id BST)
    # =====================================================================

    # head function literal pool
    (0x0804f71c, 0x00000868, 'PLAYER_BLOCK_STRIDE',       'player_block_stride_s_g'),
    (0x0804f720, 0x0201c510, 'gDuelFieldSlots',           'gduelfield_slots_s_g'),

    (0x0804f7c8, 0x00000868, 'PLAYER_BLOCK_STRIDE',       'player_block_stride_s_h'),
    (0x0804f7cc, 0x0201c510, 'gDuelFieldSlots',           'gduelfield_slots_s_h'),

    # BST CID nodes from proposal lines 77-113 (exact values)
    (0x0804f7d0, 0x00001496, 'CYCLON_LASER_CID',          'check_slot_cid_cyclon_laser'),
    (0x0804f7d4, 0x000010ed, 'cid_10ed',                  'check_slot_cid_10ed'),
    (0x0804f7f0, 0x000010d4, 'cid_10d4',                  'check_slot_cid_10d4'),
    (0x0804f80c, 0x000010da, 'cid_10da',                  'check_slot_cid_10da'),
    (0x0804f834, 0x000010e5, 'cid_10e5',                  'check_slot_cid_10e5'),
    (0x0804f84c, 0x000010e2, 'cid_10e2',                  'check_slot_cid_10e2'),
    (0x0804f870, 0x000010ea, 'cid_10ea',                  'check_slot_cid_10ea'),
    (0x0804f888, 0x000010eb, 'cid_10eb',                  'check_slot_cid_10eb'),
    (0x0804f8bc, 0x000012ef, 'cid_12ef',                  'check_slot_cid_12ef'),
    (0x0804f8c0, 0x000010ee, 'cid_10ee',                  'check_slot_cid_10ee'),
    (0x0804f8d0, 0x00001232, 'MAGICAL_LABYRINTH_CID',     'check_slot_cid_magic_labyrinth'),
    (0x0804f8ec, 0x000012c6, 'cid_12c6',                  'check_slot_cid_12c6'),
    (0x0804f904, 0x000012d3, 'AMPLIFIER_CID',             'check_slot_cid_amplifier'),
    (0x0804f938, 0x00001366, 'PREMATURE_BURIAL_CID',      'check_slot_cid_premature_burial'),
    (0x0804f948, 0x00001322, 'SNATCH_STEAL_CID',          'check_slot_cid_snatch_steal'),
    (0x0804f964, 0x000013f6, 'LIGHTNING_BLADE_CID',       'check_slot_cid_lightning_blade'),
    (0x0804f97c, 0x00001466, 'DARK_NECROFEAR_CID',        'check_slot_cid_dark_necrofear'),
    (0x0804f9c0, 0x00001759, 'OPTI_CAMO_ARMOR_CID',      'check_slot_cid_opti_camo'),
    (0x0804f9c4, 0x000015cf, 'KIRYU_CID',                 'check_slot_cid_kiryu'),
    (0x0804f9d4, 0x0000150a, 'HEART_OF_CLEAR_WATER_CID', 'check_slot_cid_heart_clear_water'),
    (0x0804f9f0, 0x0000159e, 'BUSTER_RANCHER_CID',        'check_slot_cid_buster_rancher'),
    (0x0804fa08, 0x000015b0, 'Y_DRAGON_HEAD_CID',         'check_slot_cid_y_dragon_head'),
    (0x0804fa0c, 0x000015b3, 'Z_METAL_TANK_CID',          'check_slot_cid_z_metal_tank'),
    (0x0804fa34, 0x000015d7, 'FREEZING_BEAST_CID',        'check_slot_cid_freezing_beast'),
    (0x0804fa38, 0x000015d3, 'SECOND_GOBLIN_CID',         'check_slot_cid_second_goblin'),
    (0x0804fa50, 0x000015d5, 'DES_DENDLE_CID',            'check_slot_cid_des_dendle'),
    (0x0804fa74, 0x00001693, 'METALLIZING_PARASITE_CID',  'check_slot_cid_metallizing_parasite'),
    (0x0804fa8c, 0x0000169a, 'FALLING_DOWN_CID',          'check_slot_cid_falling_down'),
    (0x0804fac0, 0x00001909, 'SPARK_BLASTER_CID',         'check_slot_cid_spark_blaster'),
    (0x0804fad8, 0x000017fb, 'RITUAL_WEAPON_CID',         'check_slot_cid_ritual_weapon'),
    (0x0804fafc, 0x000018d0, 'LEGENDARY_BLACK_BELT_CID',  'check_slot_cid_legendary_black_belt'),
    (0x0804fb08, 0x000018d1, 'NITRO_UNIT_CID',            'check_slot_cid_nitro_unit'),
    (0x0804fb44, 0x0000193a, 'DIVINE_SWORD_PHOENIX_BLADE_CID','check_slot_cid_div_sword_phoenix'),
    (0x0804fb68, 0x000019bd, 'ADHESIVE_EXPLOSIVE_CID',    'check_slot_cid_adhesive_explosive'),
    (0x0804fb80, 0x000019d7, 'SYMBOL_OF_HERITAGE_CID',    'check_slot_cid_symbol_of_heritage'),
    (0x0804fbfc, 0x000010bc, 'PETIT_MOTH_CID',            'check_slot_cid_petit_moth'),
    (0x0804fc00, 0x00000fee, 'COCOON_OF_EVOLUTION_CID',   'check_slot_cid_cocoon_evol'),
    (0x0804fc1c, 0x00000fe4, 'HARPIE_LADY_CID',           'check_slot_cid_harpie_lady'),
    (0x0804fc20, 0x00000fe5, 'HARPIE_LADY_SISTERS_CID',   'check_slot_cid_harpie_sisters'),
    (0x0804fc2c, 0x00001114, 'LABYRINTH_WALL_CID',        'check_slot_cid_labyrinth_wall'),
    (0x0804fc38, 0x00001296, 'JINZO_CID',                 'check_slot_cid_jinzo'),
    (0x0804fc54, 0x0000129e, 'DARK_MAGICIAN_GIRL_CID',    'check_slot_cid_dark_mag_girl'),
    (0x0804fc58, 0x00000fc9, 'DARK_MAGICIAN_CID_0FC9',    'check_slot_cid_dark_mag_0fc9'),
    (0x0804fc68, 0x0000142d, 'DARK_MAGICIAN_CID_142D',    'check_slot_cid_dark_mag_142d'),
    (0x0804fc74, 0x00001414, 'GRADIUS_CID',               'check_slot_cid_gradius'),
    (0x0804fc94, 0x00000513, 'FIELD5_SCORE_THRESHOLD_1299','check_slot_field5_score_thresh'),
    (0x0804fd4c, 0x0000185a, 'CHU_SKE_MOUSE_FIGHTER_CID', 'check_slot_cid_chu_ske'),
    (0x0804fd58, 0x000018a9, 'EHERO_SPARKMAN_CID',        'check_slot_cid_ehero_sparkman'),
    (0x0804fd78, 0x000005dc, 'CARD_STAT_LP_THRESHOLD_1500','check_slot_lp_threshold_1500'),
    (0x0804fd88, 0x000018f9, 'EHERO_BUBBLEMAN_CID',       'check_slot_cid_bubbleman'),
    (0x0804fd9c, 0x0000194e, 'EHERO_WILDHEART_CID',       'check_slot_cid_wildheart'),
    (0x0804fdb4, 0x00001757, 'WHITE_MAGICIAN_PIKERU_CID', 'check_slot_cid_wm_pikeru'),
    (0x0804fdb8, 0x0000191d, 'EBON_MAGICIAN_CURRAN_CID',  'check_slot_cid_ebon_curran'),
    (0x0804fdfc, 0x000015cd, 'DARK_BLADE_CID',            'check_slot_cid_dark_blade'),
    (0x0804fe10, 0x000015d0, 'DECAYED_COMMANDER_CID',     'check_slot_cid_decayed_commander'),
    (0x0804fe24, 0x000015d2, 'GIANT_ORC_CID',             'check_slot_cid_giant_orc'),
    (0x0804fe38, 0x000015d4, 'VAMPIRE_ORCHIS_CID',         'check_slot_cid_vampire_orchis'),
    (0x0804fe5c, 0x000015d6, 'BURNING_BEAST_CID',         'check_slot_cid_burning_beast'),
    (0x0804fe64, 0x0000160a, 'AITSU_CID',                 'check_slot_cid_aitsu'),
    (0x0804fe6c, 0x0000190b, 'SOITSU_CID',                'check_slot_cid_soitsu'),
    (0x0804fedc, 0x00000868, 'PLAYER_BLOCK_STRIDE',       'player_block_stride_s_i'),
    (0x0804fee0, 0x0201c510, 'gDuelFieldSlots',           'gduelfield_slots_s_i'),
    (0x0804fef4, 0x00001915, 'INDOMITABLE_FIGHTER_LEI_LEI_CID','check_slot_cid_lei_lei'),
    (0x0804ff14, 0x00001947, 'V_TIGER_JET_CID',           'check_slot_cid_v_tiger_jet'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label)
# ---------------------------------------------------------------------------
REF_SLOTS = [
    (0x0804d254, 0x0804d258, 'sprite_row_anim_jump_table',  'sprite_row_anim_jt_ptr_s'),
    (0x0804dbb4, 0x0804dbb8, 'sprite_row_queue_jump_table', 'sprite_row_queue_jt_ptr_s'),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, label, eol_ascii_or_None)
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x0804f1d0, 'compact_rank3_stride_delta_s',
     'stride delta -0x300; compact_equip_zone_rank3_entries write_ptr adjustment'),
    (0x0804f28c, 'compact_rank3_delta_b_s',
     '-0x480 stride adjustment in phase 2 of compact_equip_zone_rank3_entries'),
]

# ---------------------------------------------------------------------------
# D. PLATE_SUBS: Update plate comments to replace stale FUN_ strings
#    Format: (func_addr, old_plate_fragment, new_plate_fragment)
#    We use full plate text replacement for each affected function.
# ---------------------------------------------------------------------------

# New plate texts with all FUN_ replaced. Read existing plate via listing.getCodeUnitAt.
# Strategy: get existing plate comment, do substring substitution, set new plate.

PLATE_SUBS = [
    # Item 2: FUN_0804d1e4 -> dispatch_sprite_row_anim_by_state (L9128, reset_sprite_row_queue_tail)
    (0x0804daf6, 'FUN_0804d1e4', 'dispatch_sprite_row_anim_by_state'),
    # Item 3: FUN_0804f2e0 -> dispatch_equip_field_update_by_anim_state (L9047 + L9360)
    (0x0804d1e4, 'FUN_0804f2e0', 'dispatch_equip_field_update_by_anim_state'),
    (0x0804f0e4, 'FUN_0804f2e0', 'dispatch_equip_field_update_by_anim_state'),
    # Item 4: FUN_0804f34c -> advance_equip_zone_rank_state (L9047)
    (0x0804d1e4, 'FUN_0804f34c', 'advance_equip_zone_rank_state'),
    # Item 5: FUN_0804f6c4 -> check_slot_card_eligible_by_card_id (L11597/L11605/L11619/L11633)
    (0x0804ff9a, 'FUN_0804f6c4', 'check_slot_card_eligible_by_card_id'),
    (0x0804ffa4, 'FUN_0804f6c4', 'check_slot_card_eligible_by_card_id'),
    (0x0804ffba, 'FUN_0804f6c4', 'check_slot_card_eligible_by_card_id'),
    (0x0804ffd2, 'FUN_0804f6c4', 'check_slot_card_eligible_by_card_id'),
    # Item 6: FUN_0804f2ee / FUN_0804f3da -> call-site references (L9047, dispatch_sprite_row_anim_by_state plate)
    # The pattern "FUN_0804f2ee/FUN_0804f3da" appears both standalone and in "Both known callers FUN_..."
    # One sub handles both occurrences since the FUN_ fragment appears literally in the text.
    (0x0804d1e4, 'FUN_0804f2ee/FUN_0804f3da',
     'dispatch_equip_field_update_by_anim_state (bl at 0x0804f2ee) and advance_equip_zone_rank_state (bl at 0x0804f3da)'),
    # Item 7: FUN_08094cd4 -> tick_equip_activation_main_sequence (L9629)
    (0x0804f2e0, 'FUN_08094cd4', 'tick_equip_activation_main_sequence'),
    # Item 8: FUN_08053d88 -> check_equip_slot_eligible_by_opposite_side_zone_chain (L10029)
    (0x0804f550, 'FUN_08053d88', 'check_equip_slot_eligible_by_opposite_side_zone_chain'),
    # Item 9: FUN_08054d08 -> check_equip_slot_eligible_by_whitelist_field7_and_zone_bit (L10166)
    (0x0804f618, 'FUN_08054d08', 'check_equip_slot_eligible_by_whitelist_field7_and_zone_bit'),
]


def apply_plate_sub(func_addr, old_frag, new_frag):
    """Read existing plate comment, replace old_frag with new_frag, write back."""
    if DRY:
        print("DRY PLATE_SUB 0x%08x [%s] -> [%s]" % (func_addr, old_frag[:30], new_frag[:30]))
        return True
    try:
        listing = currentProgram.getListing()
        cu = listing.getCodeUnitAt(_addr(func_addr))
        if cu is None:
            print("WARN PLATE_SUB 0x%08x: no code unit" % func_addr)
            return False
        existing = cu.getComment(CodeUnit.PLATE_COMMENT)
        if existing is None:
            existing = ""
        if old_frag not in existing:
            print("WARN PLATE_SUB 0x%08x: pattern not found [%s]" % (func_addr, old_frag[:40]))
            return False
        new_plate = existing.replace(old_frag, new_frag)
        cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)
        print("OK  PLATE_SUB 0x%08x replaced [%s]" % (func_addr, old_frag[:40]))
        return True
    except Exception as e:
        print("ERR PLATE_SUB 0x%08x: %s" % (func_addr, str(e)))
        return False


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def run():
    fail_count = 0
    ok_count = 0

    print("=== RefineF05Seg6Apply: DRY=%s ===" % DRY)

    # A. EQ_SLOTS
    print("--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    for slot_addr, value, const_name, slot_label in EQ_SLOTS:
        if apply_eq_slot(slot_addr, value, const_name, slot_label):
            ok_count += 1
        else:
            fail_count += 1

    # B. REF_SLOTS
    print("--- B. REF_SLOTS (%d) ---" % len(REF_SLOTS))
    for slot_addr, target_addr, gas_label, slot_label in REF_SLOTS:
        if apply_ref_slot(slot_addr, target_addr, gas_label, slot_label):
            ok_count += 1
        else:
            fail_count += 1

    # C. RENAME_SLOTS
    print("--- C. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    for slot_addr, label, eol in RENAME_SLOTS:
        if apply_rename_slot(slot_addr, label, eol):
            ok_count += 1
        else:
            fail_count += 1

    # D. PLATE_SUBS
    print("--- D. PLATE_SUBS (%d) ---" % len(PLATE_SUBS))
    for args in PLATE_SUBS:
        if apply_plate_sub(args[0], args[1], args[2]):
            ok_count += 1
        else:
            fail_count += 1

    print("=== DONE: ok=%d fail=%d ===" % (ok_count, fail_count))
    if fail_count > 0:
        print("*** FAILURES DETECTED - review FAIL/WARN lines above ***")

run()
