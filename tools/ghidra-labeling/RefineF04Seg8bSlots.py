# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF04Seg8bSlots.py -- file 04 Seg-8b (0x0804640c..0x08047990)
#   check_slot_equip_placement_valid / build_equip_placement_valid_bitmap /
#   check_slot_equip_target_eligibility / dispatch_card_effect_zone_action_by_card_id /
#   handle_card_effect_zone_eligibility_by_field6 / update_equip_target_bitmap_for_field /
#   query_equip_target_bitmap_default / prepare_slot_ctx_for_equip_bitmap /
#   enqueue_equip_slot_bitmap_update / test_equip_target_slot_in_bitmap
#
# Sections:
#   A. EQ_SLOTS  (117) -- equate + slot label + optional EOL
#   B. REF_SLOTS (6)   -- USER label on target + DATA ref + slot rename
#   C. RENAME_SLOTS (23) -- plain rename + EOL (composites / packed vals)
#   D. PLATE_REWRITES (4 fn, 15 FUN_ tokens) -- substr replace

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
# helpers
# ---------------------------------------------------------------------------
def _addr(x):
    return toAddr(x)

def _sym(nm):
    return currentProgram.getSymbolTable()

def _check(slot, expected):
    mem = currentProgram.getMemory()
    try:
        val = mem.getInt(_addr(slot)) & 0xffffffff
    except Exception as e:
        return False, "read-error: %s" % e
    if val == expected:
        return True, None
    return False, "ROM=0x%08x expected=0x%08x" % (val, expected)

def _eq(slot, eq_name, slot_label, eol=None):
    """Create equate + slot label + optional EOL."""
    addr = _addr(slot)
    listing = currentProgram.getListing()
    sym_table = currentProgram.getSymbolTable()
    eq_table = currentProgram.getEquateTable()
    ref_mgr = currentProgram.getReferenceManager()

    # read actual value for equate
    mem = currentProgram.getMemory()
    try:
        val = mem.getInt(addr) & 0xffffffff
    except Exception as e:
        print("  WARN EQ read-error @ 0x%08x: %s" % (slot, e))
        return

    if not DRY:
        try:
            eq = eq_table.getEquate(eq_name)
            if eq is None:
                eq = eq_table.createEquate(eq_name, val)
        except Exception as e:
            print("  WARN EQ create @ 0x%08x %s: %s" % (slot, eq_name, e))
            return
        try:
            eq.addReference(addr, 0)
        except Exception:
            pass
        try:
            sym_table.createLabel(addr, slot_label, SourceType.USER_DEFINED)
        except Exception:
            pass
        if eol:
            try:
                listing.setComment(addr, CodeUnit.EOL_COMMENT, eol)
            except Exception:
                pass
    else:
        print("  DRY EQ 0x%08x %s=%s label=%s" % (slot, eq_name, hex(val), slot_label))

def _ref(slot, target_val, gas_label, slot_label):
    """Create USER label on target + DATA memory ref + slot label."""
    slot_addr = _addr(slot)
    target_addr = _addr(target_val)
    sym_table = currentProgram.getSymbolTable()
    ref_mgr = currentProgram.getReferenceManager()

    if not DRY:
        try:
            sym_table.createLabel(target_addr, gas_label, SourceType.USER_DEFINED)
            # set primary
            for s in sym_table.getSymbols(target_addr):
                if s.getName() == gas_label:
                    s.setPrimary()
                    break
        except Exception as e:
            print("  WARN REF target-label @ 0x%08x %s: %s" % (target_val, gas_label, e))
        try:
            ref_mgr.addMemoryReference(slot_addr, target_addr, RefType.DATA, SourceType.USER_DEFINED, 0)
        except Exception as e:
            print("  WARN REF mem-ref @ 0x%08x: %s" % (slot, e))
        try:
            sym_table.createLabel(slot_addr, slot_label, SourceType.USER_DEFINED)
        except Exception as e:
            print("  WARN REF slot-label @ 0x%08x %s: %s" % (slot, slot_label, e))
    else:
        print("  DRY REF 0x%08x -> 0x%08x (%s) label=%s" % (slot, target_val, gas_label, slot_label))

def _rename(slot, slot_label, eol=None):
    """Rename slot label + optional EOL."""
    addr = _addr(slot)
    sym_table = currentProgram.getSymbolTable()
    listing = currentProgram.getListing()
    if not DRY:
        try:
            sym_table.createLabel(addr, slot_label, SourceType.USER_DEFINED)
        except Exception as e:
            print("  WARN RENAME @ 0x%08x %s: %s" % (slot, slot_label, e))
        if eol:
            try:
                listing.setComment(addr, CodeUnit.EOL_COMMENT, eol)
            except Exception:
                pass
    else:
        print("  DRY RENAME 0x%08x label=%s" % (slot, slot_label))

def _plate(fn_addr, fn_name, replacements):
    """Substring-replace FUN_ tokens in plate comment."""
    listing = currentProgram.getListing()
    addr = _addr(fn_addr)
    cu = listing.getCodeUnitAt(addr)
    if cu is None:
        print("  WARN PLATE no code unit @ 0x%08x (%s)" % (fn_addr, fn_name))
        return
    old = cu.getComment(CodeUnit.PLATE_COMMENT)
    if old is None:
        old = ""
    new = old
    for old_tok, new_tok in replacements:
        new = new.replace(old_tok, new_tok)
    if new == old:
        print("  WARN PLATE no-change @ 0x%08x (%s) -- check tokens" % (fn_addr, fn_name))
        return
    if not DRY:
        try:
            listing.setComment(addr, CodeUnit.PLATE_COMMENT, new)
            print("  PLATE OK 0x%08x (%s) -- %d tokens replaced" % (fn_addr, fn_name, len(replacements)))
        except Exception as e:
            print("  WARN PLATE set @ 0x%08x: %s" % (fn_addr, e))
    else:
        print("  DRY PLATE 0x%08x (%s) -- %d tokens" % (fn_addr, fn_name, len(replacements)))

# ---------------------------------------------------------------------------
# A. EQ_SLOTS: (slot_addr, expected_value, eq_name, slot_label, eol_or_None)
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # --- check_slot_equip_placement_valid (0x0804640c) ---
    (0x0804650c, 0x00000868, 'PLAYER_BLOCK_STRIDE',       'check_slot_equip_placement_valid_stride',           None),
    (0x08046510, 0x0201c510, 'gDuelFieldSlots',            'check_slot_equip_placement_valid_slots',            None),
    (0x08046514, 0x000010a4, 'EFFECT_ZONE_PARTITION_OFF',  'check_slot_equip_placement_valid_zone_off',         None),
    (0x08046518, 0x0000169f, 'PANDEMONIUM_CID',            'check_slot_equip_placement_valid_cid_pandemonium',  None),
    (0x0804651c, 0x00001683, 'PANDEMONIUM_WATCHBEAR_CID',  'check_slot_equip_placement_valid_cid_watchbear',    None),

    # --- check_slot_equip_target_eligibility (0x0804659c) ---
    (0x0804663c, 0x00001825, 'HEAVY_MECH_SUPPORT_PLATFORM_CID', 'check_slot_equip_target_elig_cid_1825',       None),
    (0x08046698, 0x000010d4, 'EQUIP_BITMAP_CTRL_OFF',      'check_slot_equip_target_elig_ctrl_off',            None),
    (0x0804669c, 0x000015e6, 'AUTONOMOUS_ACTION_UNIT_CID', 'check_slot_equip_target_elig_cid_15e6',            None),
    (0x080466a0, 0x0000137d, 'CALL_OF_THE_HAUNTED_CID',    'check_slot_equip_target_elig_cid_137d',            None),
    (0x080466a8, 0x00001366, 'PREMATURE_BURIAL_CID',        'check_slot_equip_target_elig_cid_1366_b',         None),
    (0x080466c4, 0x0000149a, 'SPIRIT_MESSAGE_L_CID',        'check_slot_equip_target_elig_cid_149a',           None),
    (0x080466d4, 0x0000150e, 'SPIRITUAL_ENERGY_SETTLE_CID', 'check_slot_equip_target_elig_cid_150e',           None),
    (0x080466fc, 0x000017af, 'THE_FIRST_SARCOPHAGUS_CID',   'check_slot_equip_target_elig_cid_17af',           None),
    (0x08046700, 0x000017ad, 'THE_THIRD_SARCOPHAGUS_CID',   'check_slot_equip_target_elig_cid_17ad',           None),
    (0x08046704, 0x000016a2, 'BATTLE_SCARRED_CID',          'check_slot_equip_target_elig_cid_16a2',           None),
    (0x08046718, 0x00001768, 'NINJITSU_ART_OF_TRANSFORMATION_CID', 'check_slot_equip_target_elig_cid_1768',    None),
    (0x08046738, 0x00001881, 'RE_FUSION_CID',               'check_slot_equip_target_elig_cid_1881',           None),
    (0x0804674c, 0x000019d7, 'SYMBOL_OF_HERITAGE_CID',      'check_slot_equip_target_elig_cid_19d7',           None),
    (0x080467e4, 0x00000868, 'PLAYER_BLOCK_STRIDE',         'check_slot_equip_target_elig_stride_b',           None),
    (0x080467e8, 0x0201c510, 'gDuelFieldSlots',             'check_slot_equip_target_elig_slots_b',            None),
    (0x0804688c, 0x00000868, 'PLAYER_BLOCK_STRIDE',         'check_slot_equip_target_elig_stride_c',           None),
    (0x08046890, 0x0201c510, 'gDuelFieldSlots',             'check_slot_equip_target_elig_slots_c',            None),
    (0x08046894, 0x0000ffff, 'OAM_ATTR0_HIDDEN',            'check_slot_equip_target_elig_no_pair_a',          None),
    (0x08046954, 0x00000868, 'PLAYER_BLOCK_STRIDE',         'check_slot_equip_target_elig_stride_d',           None),
    (0x08046958, 0x0201c510, 'gDuelFieldSlots',             'check_slot_equip_target_elig_slots_d',            None),
    (0x0804695c, 0x0000ffff, 'OAM_ATTR0_HIDDEN',            'check_slot_equip_target_elig_no_pair_b',          None),
    (0x08046960, 0x00001625, 'BIG_BANG_SHOT_CID',           'check_slot_equip_target_elig_cid_1625',           None),
    (0x08046964, 0x00001881, 'RE_FUSION_CID',               'check_slot_equip_target_elig_cid_1881_b',         None),
    (0x08046a28, 0x00000868, 'PLAYER_BLOCK_STRIDE',         'check_slot_equip_target_elig_stride_e',           None),
    (0x08046a2c, 0x0201c510, 'gDuelFieldSlots',             'check_slot_equip_target_elig_slots_e',            None),
    (0x08046a30, 0x00001468, 'DESTINY_BOARD_CID',           'check_slot_equip_target_elig_cid_1468',           None),
    (0x08046a34, 0x0000149a, 'SPIRIT_MESSAGE_L_CID',        'check_slot_equip_target_elig_cid_149a_b',         None),
    (0x08046ab4, 0x00000868, 'PLAYER_BLOCK_STRIDE',         'check_slot_equip_target_elig_stride_f',           None),
    (0x08046ab8, 0x0201c510, 'gDuelFieldSlots',             'check_slot_equip_target_elig_slots_f',            None),
    (0x08046abc, 0x000017af, 'THE_FIRST_SARCOPHAGUS_CID',   'check_slot_equip_target_elig_cid_17af_b',         None),
    (0x08046ac0, 0x000017ad, 'THE_THIRD_SARCOPHAGUS_CID',   'check_slot_equip_target_elig_cid_17ad_b',         None),
    (0x08046bc0, 0x00000868, 'PLAYER_BLOCK_STRIDE',         'check_slot_equip_target_elig_stride_g',           None),
    (0x08046bc4, 0x0201c510, 'gDuelFieldSlots',             'check_slot_equip_target_elig_slots_g',            None),
    (0x08046bc8, 0x0000150e, 'SPIRITUAL_ENERGY_SETTLE_CID', 'check_slot_equip_target_elig_cid_150e_b',         None),
    (0x08046bcc, 0x0201d9c0, 'gEquipNodePool',              'check_slot_equip_target_elig_node_pool',          None),

    # --- dispatch_card_effect_zone_action_by_card_id (0x08046bd0) ---
    (0x08046c38, 0x00001625, 'BIG_BANG_SHOT_CID',           'disp_zone_action_cid_1625',                       None),
    (0x08046c3c, 0x00001468, 'DESTINY_BOARD_CID',           'disp_zone_action_cid_1468',                       None),
    (0x08046c40, 0x000012d3, 'AMPLIFIER_CID',               'disp_zone_action_cid_12d3',                       None),
    (0x08046c50, 0x00001366, 'PREMATURE_BURIAL_CID',        'disp_zone_action_cid_1366',                       None),
    (0x08046c74, 0x0000150e, 'SPIRITUAL_ENERGY_SETTLE_CID', 'disp_zone_action_cid_150e',                       None),
    (0x08046c84, 0x000015e6, 'AUTONOMOUS_ACTION_UNIT_CID',  'disp_zone_action_cid_15e6',                       None),
    (0x08046cac, 0x000017b7, 'SOUL_RESURRECTION_CID',       'disp_zone_action_cid_17b7',                       None),
    (0x08046ce4, 0x000017af, 'THE_FIRST_SARCOPHAGUS_CID',   'disp_zone_action_cid_17af',                       None),
    (0x08046ce8, 0x00000868, 'PLAYER_BLOCK_STRIDE',         'disp_zone_action_stride_a',                       None),
    (0x08046cec, 0x0201c510, 'gDuelFieldSlots',             'disp_zone_action_slots_a',                        None),
    (0x08046d08, 0x00001881, 'RE_FUSION_CID',               'disp_zone_action_cid_1881',                       None),
    (0x08046d18, 0x000019d7, 'SYMBOL_OF_HERITAGE_CID',      'disp_zone_action_cid_19d7',                       None),
    (0x08046da8, 0x0201e1c8, 'gEquipZoneCountTable',        'disp_zone_action_equip_zone_tbl',                 None),
    (0x08046dac, 0x00000868, 'PLAYER_BLOCK_STRIDE',         'disp_zone_action_stride_b',                       None),
    (0x08046db0, 0x0201c510, 'gDuelFieldSlots',             'disp_zone_action_slots_b',                        None),
    (0x08046db4, 0x0201c520, 'gDuelFieldSlotState',         'disp_zone_action_slot_state',                     None),
    (0x08046e68, 0x00000868, 'PLAYER_BLOCK_STRIDE',         'disp_zone_action_stride_c',                       None),
    (0x08046e6c, 0x0201c510, 'gDuelFieldSlots',             'disp_zone_action_slots_c',                        None),
    (0x08046e70, 0x0000ffff, 'OAM_ATTR0_HIDDEN',            'disp_zone_action_no_pair_a',                      None),
    (0x08046ef4, 0x00000868, 'PLAYER_BLOCK_STRIDE',         'disp_zone_action_stride_d',                       None),
    (0x08046ef8, 0x0201c510, 'gDuelFieldSlots',             'disp_zone_action_slots_d',                        None),
    (0x08046efc, 0x000017c8, 'SPHINX_TELEIA_CID',           'disp_zone_action_cid_17c8',                       None),
    (0x08046fc4, 0x00000868, 'PLAYER_BLOCK_STRIDE',         'disp_zone_action_stride_e',                       None),
    (0x08046fc8, 0x0201c510, 'gDuelFieldSlots',             'disp_zone_action_slots_e',                        None),
    (0x08046fcc, 0x0000ffff, 'OAM_ATTR0_HIDDEN',            'disp_zone_action_no_pair_b',                      None),
    (0x08046fd0, 0x00001625, 'BIG_BANG_SHOT_CID',           'disp_zone_action_cid_1625_b',                     None),
    (0x08046fd4, 0x00001881, 'RE_FUSION_CID',               'disp_zone_action_cid_1881_b',                     None),
    (0x08047094, 0x00000868, 'PLAYER_BLOCK_STRIDE',         'disp_zone_action_stride_f',                       None),
    (0x08047098, 0x0201c510, 'gDuelFieldSlots',             'disp_zone_action_slots_f',                        None),
    (0x0804709c, 0x00001468, 'DESTINY_BOARD_CID',           'disp_zone_action_cid_1468_b',                     None),
    (0x080470a0, 0x0000149a, 'SPIRIT_MESSAGE_L_CID',        'disp_zone_action_cid_149a',                       None),
    (0x08047104, 0x000017af, 'THE_FIRST_SARCOPHAGUS_CID',   'disp_zone_action_cid_17af_b',                     None),
    (0x08047108, 0x00000868, 'PLAYER_BLOCK_STRIDE',         'disp_zone_action_stride_g',                       None),
    (0x0804710c, 0x0201c510, 'gDuelFieldSlots',             'disp_zone_action_slots_g',                        None),
    (0x08047110, 0x000017ad, 'THE_THIRD_SARCOPHAGUS_CID',   'disp_zone_action_cid_17ad',                       None),
    (0x08047204, 0x00000868, 'PLAYER_BLOCK_STRIDE',         'disp_zone_action_stride_h',                       None),
    (0x08047208, 0x0201c510, 'gDuelFieldSlots',             'disp_zone_action_slots_h',                        None),
    (0x0804720c, 0x0201e1c8, 'gEquipZoneCountTable',        'disp_zone_action_equip_zone_tbl_b',               None),
    (0x08047210, 0x0000150e, 'SPIRITUAL_ENERGY_SETTLE_CID', 'disp_zone_action_cid_150e_b',                     None),
    (0x08047214, 0x0201d9c0, 'gEquipNodePool',              'disp_zone_action_node_pool_b',                    None),

    # --- handle_card_effect_zone_eligibility_by_field6 (0x08047218) ---
    (0x08047270, 0x00000868, 'PLAYER_BLOCK_STRIDE',         'handle_zone_elig_stride',                         None),
    (0x08047274, 0x0201c510, 'gDuelFieldSlots',             'handle_zone_elig_slots',                          None),
    (0x080472e4, 0x00001825, 'HEAVY_MECH_SUPPORT_PLATFORM_CID', 'handle_zone_elig_cid_1825',                   None),
    (0x080474ac, 0x00000868, 'PLAYER_BLOCK_STRIDE',         'handle_zone_elig_stride_b',                       None),
    (0x080474b0, 0x000014fb, 'FIBER_JAR_CID',               'handle_zone_elig_cid_14fb',                       None),
    (0x080474b4, 0x000019e1, 'GOBLIN_OUT_OF_FRYING_PAN_CID', 'handle_zone_elig_cid_19e1',                      None),
    (0x080474b8, 0x000010d4, 'EQUIP_BITMAP_CTRL_OFF',       'handle_zone_elig_ctrl_off_b',                     None),
    (0x080474bc, 0x000016f8, 'DARK_MAGICIAN_OF_CHAOS_CID',  'handle_zone_elig_cid_16f8',                       None),
    (0x080474c0, 0x0201c510, 'gDuelFieldSlots',             'handle_zone_elig_slots_b',                        None),
    (0x080474c4, 0xfffffe00, 'OAM_ATTR1_X_CLEAR',           'handle_zone_elig_x_clr',                         None),
    (0x080474c8, 0xfffffdff, 'OAM_SPRITE_ATTR_CLR_BIT9',    'handle_zone_elig_clr_bit9',                       None),
    (0x080474cc, 0xffffc3ff, 'OAM_SPRITE_ATTR_CLR_BITS13_10', 'handle_zone_elig_clr_bits13_10',               None),
    (0x080474d0, 0xffffbfff, 'SLOT_ACTIVE_BIT14_CLR',       'handle_zone_elig_clr_bit14',                      None),
    (0x080474d4, 0xfffdffff, 'OAM_SPRITE_ATTR_CLR_BIT17',   'handle_zone_elig_clr_bit17',                      None),
    (0x080474d8, 0xfffbffff, 'OAM_SPRITE_ATTR_CLR_BIT18',   'handle_zone_elig_clr_bit18',                      None),
    (0x080474dc, 0xffff7fff, 'SLOT_ACTIVE_BIT15_CLR',       'handle_zone_elig_clr_bit15',                      None),
    (0x080474e0, 0xff7fffff, 'SLOT_ACTIVE_BIT23_CLR',       'handle_zone_elig_clr_bit23',                      None),
    (0x080474e4, 0xff87ffff, 'OAM_SPRITE_ATTR_CLR_BITS22_19', 'handle_zone_elig_clr_bits22_19',               None),
    (0x080474e8, 0x000010a4, 'EFFECT_ZONE_PARTITION_OFF',   'handle_zone_elig_zone_off',                       None),
    (0x080474ec, 0x00008045, 'OAM_ZONE_EQUIP_SPRITE_P1',    'handle_zone_elig_oam_zone_equip',                 None),
    (0x08047528, 0x00008031, 'OAM_EFFECT_ZONE_SPRITE_P1',   'handle_zone_elig_oam_effect_zone_p1',
     'OAM attr0 P1 zone effect card sprite (bit15+0x31); field8==9 P1 path'),
    (0x08047574, 0x0000803d, 'OAM_EQUIP_CHAIN_PAIR_SPRITE_P1', 'handle_zone_elig_oam_pair_p1',                None),
    (0x080475a0, 0x00008031, 'OAM_EFFECT_ZONE_SPRITE_P1',   'handle_zone_elig_oam_effect_zone_p1_b',          None),
    (0x080475cc, 0x00008033, 'OAM_EQUIP_ZONE_SPRITE_P1',    'handle_zone_elig_oam_equip_zone',                None),
    (0x08047618, 0x00000868, 'PLAYER_BLOCK_STRIDE',         'handle_zone_elig_stride_c',                       None),
    (0x0804761c, 0x0201c510, 'gDuelFieldSlots',             'handle_zone_elig_slots_c',                        None),
    (0x08047708, 0x00000868, 'PLAYER_BLOCK_STRIDE',         'handle_zone_elig_stride_d',                       None),
    (0x0804770c, 0x0201c510, 'gDuelFieldSlots',             'handle_zone_elig_slots_d',                        None),

    # --- update_equip_target_bitmap_for_field (0x08047724) ---
    (0x0804786c, 0x000010d4, 'EQUIP_BITMAP_CTRL_OFF',       'upd_equip_bitmap_ctrl_off',                       None),
    (0x08047870, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',        'upd_equip_bitmap_block2_off',                     None),
    (0x08047874, 0x00001825, 'HEAVY_MECH_SUPPORT_PLATFORM_CID', 'upd_equip_bitmap_cid_1825',                   None),
    (0x08047878, 0x0201e1c8, 'gEquipZoneCountTable',        'upd_equip_bitmap_equip_zone_tbl_c',               None),
    (0x0804787c, 0x00001332, 'BANISHER_OF_THE_LIGHT_CID',   'upd_equip_bitmap_cid_banisher',                   None),
    (0x08047880, 0x00000868, 'PLAYER_BLOCK_STRIDE',         'upd_equip_bitmap_stride',                         None),
    (0x08047884, 0x0201c510, 'gDuelFieldSlots',             'upd_equip_bitmap_slots',                          None),

    # --- query_equip_target_bitmap_default / prepare_slot_ctx / enqueue / test (0x080478fc..) ---
    (0x080478f8, 0x000010d4, 'EQUIP_BITMAP_CTRL_OFF',       'upd_equip_bitmap_ctrl_off_b',                     None),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_val, gas_label, slot_label)
# ---------------------------------------------------------------------------
REF_SLOTS = [
    (0x08046524, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_08046524'),
    (0x08046694, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_08046694'),
    (0x080474a8, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_080474a8'),
    (0x08047868, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_08047868'),
    (0x080478f4, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_080478f4'),
    # compound: gDuelFieldSlots+EFFECT_ZONE_PARTITION_OFF = 0x0201c510+0x10a4 = 0x0201d5b4
    (0x080478f0, 0x0201d5b4, 'gDuelFieldSlots', 'upd_equip_bitmap_effect_zone'),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x08046520, 'check_slot_equip_placement_valid_cid_1258',
     'card_id 0x1258: gap in card-stats.s (no name); eligibility check gP1LifePoints+off bit2 [low-conf]'),
    (0x08046c38, 'disp_zone_action_cid_1625',
     'BIG_BANG_SHOT_CID -- see card_info.inc'),
    (0x08046c3c, 'disp_zone_action_cid_1468',
     'DESTINY_BOARD_CID -- see card_info.inc'),
    (0x08046c40, 'disp_zone_action_cid_12d3',
     'AMPLIFIER_CID -- see card_info.inc'),
    (0x08046c50, 'disp_zone_action_cid_1366',
     'PREMATURE_BURIAL_CID -- see card_info.inc'),
    (0x08046c74, 'disp_zone_action_cid_150e',
     'SPIRITUAL_ENERGY_SETTLE_CID -- see card_info.inc'),
    (0x08046c84, 'disp_zone_action_cid_15e6',
     'AUTONOMOUS_ACTION_UNIT_CID -- see card_info.inc'),
    (0x08046cac, 'disp_zone_action_cid_17b7',
     'SOUL_RESURRECTION_CID -- see card_info.inc'),
    (0x08046ce4, 'disp_zone_action_cid_17af',
     'THE_FIRST_SARCOPHAGUS_CID -- see card_info.inc'),
    (0x08046d08, 'disp_zone_action_cid_1881',
     'RE_FUSION_CID -- see card_info.inc'),
    (0x08046d18, 'disp_zone_action_cid_19d7',
     'SYMBOL_OF_HERITAGE_CID -- see card_info.inc'),
    (0x08046efc, 'disp_zone_action_cid_17c8',
     'SPHINX_TELEIA_CID (range upper bound [0x17c7..0x17c8]) -- card_info.inc'),
    (0x08046fd0, 'disp_zone_action_cid_1625_b',
     'BIG_BANG_SHOT_CID -- see card_info.inc'),
    (0x08046fd4, 'disp_zone_action_cid_1881_b',
     'RE_FUSION_CID -- see card_info.inc'),
    (0x0804709c, 'disp_zone_action_cid_1468_b',
     'DESTINY_BOARD_CID'),
    (0x080470a0, 'disp_zone_action_cid_149a',
     'SPIRIT_MESSAGE_L_CID'),
    (0x08047104, 'disp_zone_action_cid_17af_b',
     'THE_FIRST_SARCOPHAGUS_CID'),
    (0x08047110, 'disp_zone_action_cid_17ad',
     'THE_THIRD_SARCOPHAGUS_CID'),
    (0x08047210, 'disp_zone_action_cid_150e_b',
     'SPIRITUAL_ENERGY_SETTLE_CID'),
    (0x080474b0, 'handle_zone_elig_cid_14fb',
     'FIBER_JAR_CID -- see card_info.inc'),
    (0x080474b4, 'handle_zone_elig_cid_19e1',
     'GOBLIN_OUT_OF_FRYING_PAN_CID -- see card_info.inc'),
    (0x080474bc, 'handle_zone_elig_cid_16f8',
     'DARK_MAGICIAN_OF_CHAOS_CID -- see card_info.inc'),
    (0x0804787c, 'upd_equip_bitmap_cid_banisher',
     'BANISHER_OF_THE_LIGHT_CID -- see card_info.inc'),
]

# ---------------------------------------------------------------------------
# D. PLATE_REWRITES: (fn_addr, fn_name, [(old_token, new_token), ...])
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    (0x0804659c, 'check_slot_equip_target_eligibility', [
        ('FUN_08047724', 'update_equip_target_bitmap_for_field'),
        ('FUN_08046538', 'build_equip_placement_valid_bitmap'),
    ]),
    (0x08046bd0, 'dispatch_card_effect_zone_action_by_card_id', [
        ('FUN_08047114', 'dispatch_card_effect_zone_action_by_card_id'),
        ('FUN_080470a4', 'dispatch_card_effect_zone_action_by_card_id'),
        ('FUN_08047218', 'handle_card_effect_zone_eligibility_by_field6'),
        ('FUN_08047f50', 'render_slot_card_sprite_from_descriptor'),
        ('FUN_08048020', 'render_slot_card_sprite_and_effects'),
        ('FUN_08048268', 'render_zone_sprite_with_effect_dispatch_by_slot'),
        ('FUN_08048364', 'render_slot_card_sprite_with_chaos_equip_check'),
        ('FUN_0804559c', 'dispatch_card_effect_sprite_render_by_card_id'),
    ]),
    (0x08047218, 'handle_card_effect_zone_eligibility_by_field6', [
        ('FUN_0804559c', 'dispatch_card_effect_sprite_render_by_card_id'),
        ('FUN_08046bd0', 'dispatch_card_effect_zone_action_by_card_id'),
        ('FUN_08047724', 'update_equip_target_bitmap_for_field'),
        ('FUN_0804adf0', 'check_card_field8_is_9'),
    ]),
    (0x08047970, 'test_equip_target_slot_in_bitmap', [
        ('FUN_080478fc', 'query_equip_target_bitmap_default'),
    ]),
]

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
print("=== RefineF04Seg8bSlots DRY=%s ===" % DRY)

# --- A. EQ_SLOTS ---
print("--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
eq_ok = 0
eq_fail = 0
for (slot, expected, eq_name, slot_label, eol) in EQ_SLOTS:
    ok, msg = _check(slot, expected)
    if not ok:
        print("  FAIL EQ value check 0x%08x %s: %s" % (slot, eq_name, msg))
        eq_fail += 1
        continue
    eq_ok += 1
    _eq(slot, eq_name, slot_label, eol)

print("  EQ: %d OK, %d FAIL" % (eq_ok, eq_fail))

# --- B. REF_SLOTS ---
print("--- B. REF_SLOTS (%d) ---" % len(REF_SLOTS))
for (slot, target_val, gas_label, slot_label) in REF_SLOTS:
    ok, msg = _check(slot, target_val)
    if not ok:
        print("  FAIL REF value check 0x%08x: %s" % (slot, msg))
        continue
    _ref(slot, target_val, gas_label, slot_label)

# --- C. RENAME_SLOTS ---
print("--- C. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
for (slot, slot_label, eol) in RENAME_SLOTS:
    _rename(slot, slot_label, eol)

# --- D. PLATE_REWRITES ---
print("--- D. PLATE_REWRITES (%d fn) ---" % len(PLATE_REWRITES))
for (fn_addr, fn_name, replacements) in PLATE_REWRITES:
    _plate(fn_addr, fn_name, replacements)

print("=== DONE DRY=%s ===" % DRY)
