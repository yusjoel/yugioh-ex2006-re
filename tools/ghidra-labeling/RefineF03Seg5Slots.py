# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF03Seg5Slots.py -- file 03 Seg-5 (0x0803a7f0..0x0803b3a8)
#   build_equip_target_eligibility_table .. get_zone_slot_ptr
#   EQ=45, REF=31, RENAME=3, FUNC_RENAME=0, PLATE=0
#
# Sections:
#   A. EQ_SLOTS   -- data-equate (PLAYER_BLOCK_STRIDE reuse x21, NODE_POOL_NEG_OFFSET x4,
#                                  card CID reuse x12, new card CIDs x8)
#   B. REF_SLOTS  -- USER-label + DATA-ref (globals + fn-ptr + ROM table)
#   C. RENAME_SLOTS -- pure rename + EOL (3 slots)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).
# NOTE: DAT_0803aa74 = 0x0803777d (THUMB fn-ptr, odd addr = check_level_conv_lab_node_match+1).
#   Known issue: Ghidra DATA ref will target even addr; after export asm must have +1 manually.

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
# Helpers
# ---------------------------------------------------------------------------

def _addr(val):
    return toAddr(val)

def _check(slot_addr, expected):
    """Verify ROM dword at slot_addr matches expected. Return True if OK."""
    addr = _addr(slot_addr)
    mem = currentProgram.getMemory()
    try:
        actual = mem.getInt(addr) & 0xffffffff
        if actual != (expected & 0xffffffff):
            print("WARN: slot 0x%08x expected 0x%08x got 0x%08x -- SKIP" % (slot_addr, expected & 0xffffffff, actual))
            return False
        return True
    except Exception as e:
        print("WARN: slot 0x%08x read error: %s" % (slot_addr, e))
        return False

def _eq(slot_addr, value, eq_name, slot_label, eol=None):
    """Create equate eq_name=value, reference from slot, label slot."""
    if not _check(slot_addr, value):
        return
    if DRY:
        print("DRY EQ: 0x%08x %s=%s sl=%s" % (slot_addr, eq_name, hex(value & 0xffffffff), slot_label))
        return
    addr = _addr(slot_addr)
    et = currentProgram.getEquateTable()
    eq = et.getEquate(eq_name)
    if eq is None:
        eq = et.createEquate(eq_name, value & 0xffffffff)
    eq.addReference(addr, 0)
    sm = currentProgram.getSymbolTable()
    sm.createLabel(addr, slot_label, SourceType.USER_DEFINED)
    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(addr)
        if cu:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

def _ref(slot_addr, target_addr, gas_label, slot_label, eol=None):
    """Create USER label at target, DATA ref from slot, label slot."""
    if DRY:
        print("DRY REF: 0x%08x -> 0x%08x gas=%s sl=%s" % (slot_addr, target_addr, gas_label, slot_label))
        return
    # label the target
    tgt = _addr(target_addr)
    sm = currentProgram.getSymbolTable()
    sm.createLabel(tgt, gas_label, SourceType.USER_DEFINED)
    # DATA ref
    rm = currentProgram.getReferenceManager()
    src = _addr(slot_addr)
    rm.addMemoryReference(src, tgt, RefType.DATA, SourceType.USER_DEFINED, 0)
    ref_list = rm.getReferencesFrom(src)
    for r in ref_list:
        if r.getToAddress().equals(tgt):
            rm.setPrimary(r, True)
    # label the slot
    sm.createLabel(src, slot_label, SourceType.USER_DEFINED)
    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(src)
        if cu:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

def _rename(slot_addr, old_label, new_label, eol=None):
    """Rename existing label (or create new) at slot_addr."""
    if DRY:
        print("DRY RENAME: 0x%08x %s->%s" % (slot_addr, old_label, new_label))
        return
    addr = _addr(slot_addr)
    sm = currentProgram.getSymbolTable()
    syms = list(sm.getSymbols(addr))
    renamed = False
    for sym in syms:
        if sym.getName() == old_label:
            sym.setName(new_label, SourceType.USER_DEFINED)
            renamed = True
            break
    if not renamed:
        sm.createLabel(addr, new_label, SourceType.USER_DEFINED)
    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(addr)
        if cu:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

# ---------------------------------------------------------------------------
# A. EQ_SLOTS
# ---------------------------------------------------------------------------
# (slot_addr, value, eq_name, slot_label, eol_or_None)
EQ_SLOTS = [

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x868 (21 slots) ---
    (0x0803a888, 0x868, 'PLAYER_BLOCK_STRIDE', 'build_elig_table_stride_c', None),
    (0x0803a950, 0x868, 'PLAYER_BLOCK_STRIDE', 'build_elig_table_stride_d', None),
    (0x0803a9f4, 0x868, 'PLAYER_BLOCK_STRIDE', 'eval_slot_score_full_stride_a', None),
    (0x0803ab18, 0x868, 'PLAYER_BLOCK_STRIDE', 'eval_equip_chain_stride_a', None),
    (0x0803aba4, 0x868, 'PLAYER_BLOCK_STRIDE', 'eval_equip_chain_stride_b', None),
    (0x0803ac58, 0x868, 'PLAYER_BLOCK_STRIDE', 'get_state_code_stride_a', None),
    (0x0803acdc, 0x868, 'PLAYER_BLOCK_STRIDE', 'query_state_code_stride_a', None),
    (0x0803ad84, 0x868, 'PLAYER_BLOCK_STRIDE', 'query_state_code_stride_b', None),
    (0x0803ae60, 0x868, 'PLAYER_BLOCK_STRIDE', 'query_state_code_stride_c', None),
    (0x0803aec8, 0x868, 'PLAYER_BLOCK_STRIDE', 'resolve_chain_target_stride_a', None),
    (0x0803af38, 0x868, 'PLAYER_BLOCK_STRIDE', 'resolve_chain_target_stride_b', None),
    (0x0803b02c, 0x868, 'PLAYER_BLOCK_STRIDE', 'resolve_chain_target_stride_c', None),
    (0x0803b120, 0x868, 'PLAYER_BLOCK_STRIDE', 'resolve_chain_target_stride_d', None),
    (0x0803b19c, 0x868, 'PLAYER_BLOCK_STRIDE', 'resolve_best_target_stride_a', None),
    (0x0803b214, 0x868, 'PLAYER_BLOCK_STRIDE', 'compute_zone_mask_stride_a', None),
    (0x0803b2f4, 0x868, 'PLAYER_BLOCK_STRIDE', 'get_zone_slot_ptr_stride_a', None),
    (0x0803b30c, 0x868, 'PLAYER_BLOCK_STRIDE', 'get_zone_slot_ptr_stride_b', None),
    (0x0803b324, 0x868, 'PLAYER_BLOCK_STRIDE', 'get_zone_slot_ptr_stride_c', None),
    (0x0803b33c, 0x868, 'PLAYER_BLOCK_STRIDE', 'get_zone_slot_ptr_stride_d', None),
    (0x0803b354, 0x868, 'PLAYER_BLOCK_STRIDE', 'get_zone_slot_ptr_stride_e', None),
    (0x0803b3a0, 0x868, 'PLAYER_BLOCK_STRIDE', 'get_zone_slot_ptr_stride_f', None),

    # --- duel_field.inc: NODE_POOL_NEG_OFFSET = 0xffffeb50 (4 slots) ---
    (0x0803ab20, 0xffffeb50, 'NODE_POOL_NEG_OFFSET', 'eval_equip_chain_pool_neg_off_a', None),
    (0x0803ae68, 0xffffeb50, 'NODE_POOL_NEG_OFFSET', 'query_state_code_pool_neg_off_a', None),
    (0x0803b074, 0xffffeb50, 'NODE_POOL_NEG_OFFSET', 'resolve_chain_target_pool_neg_off_a', None),
    (0x0803b128, 0xffffeb50, 'NODE_POOL_NEG_OFFSET', 'resolve_chain_target_pool_neg_off_b', None),

    # --- card_info.inc: reuse existing CID constants ---
    (0x0803aa90, 0x15c7, 'COST_DOWN_CID',             'eval_equip_chain_cost_down_cid', None),
    (0x0803aaac, 0x1472, 'EMBODIMENT_OF_APOPHIS_CID',  'eval_equip_chain_apophis_cid_a', None),
    (0x0803adcc, 0x1472, 'EMBODIMENT_OF_APOPHIS_CID',  'query_state_apophis_cid_a', None),
    (0x0803b094, 0x1472, 'EMBODIMENT_OF_APOPHIS_CID',  'resolve_chain_apophis_cid_a', None),
    (0x0803aab0, 0x1636, 'METAL_REFLECT_SLIME_CID',    'eval_equip_chain_slime_cid_a', None),
    (0x0803add0, 0x1636, 'METAL_REFLECT_SLIME_CID',    'query_state_slime_cid_a', None),
    (0x0803b098, 0x1636, 'METAL_REFLECT_SLIME_CID',    'resolve_chain_slime_cid_a', None),
    (0x0803aac4, 0x172f, 'SKULL_ZOMA_CID',             'eval_equip_chain_skull_zoma_cid_a', None),
    (0x0803ade4, 0x172f, 'SKULL_ZOMA_CID',             'query_state_skull_zoma_cid_a', None),
    (0x0803b0b0, 0x172f, 'SKULL_ZOMA_CID',             'resolve_chain_skull_zoma_cid_a', None),
    (0x0803abec, 0x150b, 'A_LEGENDARY_OCEAN_CARD_ID',  'get_state_code_ocean_cid', None),
    (0x0803b21c, 0x18c7, 'DORIADO_CID',                'compute_zone_mask_doriado_cid', None),
    (0x0803b220, 0x19ef, 'EHERO_ERIKSHIELER_CID',      'compute_zone_mask_erikshieler_cid', None),

    # --- card_info.inc: NEW CID constants (8) ---
    (0x0803aba0, 0x15e3, 'DEMOTION_CID',               'eval_equip_chain_demotion_cid',
     'Demotion (pw=72575145; card_1236 slot=0x15E3)'),
    (0x0803ace0, 0x12a1, 'PARASITE_PARACIDE_CID',      'query_state_paracide_cid',
     'Parasite Paracide (pw=27911549; card_0625 slot=0x12A1)'),
    (0x0803ad7c, 0x1357, 'DNA_SURGERY_CID',            'query_state_dna_surgery_cid',
     'DNA Surgery (pw=74701381; card_0760 slot=0x1357)'),
    (0x0803ada8, 0x15ae, 'D_TRIBE_CID',               'query_state_d_tribe_cid',
     'D. Tribe (pw=02833249; card_1199 slot=0x15AE)'),
    (0x0803b06c, 0x183b, 'HOMUNCULUS_CID',             'resolve_chain_homunculus_cid',
     'Homunculus the Alchemic Being (pw=40410110; card_1727 slot=0x183B)'),
    (0x0803b198, 0x145b, 'SCROLL_OF_BEWITCHMENT_CID',  'resolve_chain_bewitch_cid',
     'Scroll of Bewitchment (pw=10352095; card_0927 slot=0x145B)'),
    # DNA_TRANSPLANT_CID: base value only (not directly loaded; shifted form is the actual slot)
    # DNA_TRANSPLANT_CID_SHIFTED = 0xb8f80000 = 0x171f<<19
    (0x0803b030, 0xb8f80000, 'DNA_TRANSPLANT_CID_SHIFTED', 'resolve_chain_dna_transplant_shifted',
     'DNA_TRANSPLANT_CID(0x171f)<<19; lsls r0,#0x13 then cmp with this sentinel'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS
# ---------------------------------------------------------------------------
# (slot_addr, target_addr, gas_label, slot_label, eol_or_None)
REF_SLOTS = [
    # build_equip_target_eligibility_table
    (0x0803a88c, 0x0201c510, 'gDuelFieldSlots',         'build_elig_table_field_slots_a', None),
    (0x0803a94c, 0x0201e2a0, 'gDuelCardCtxBase',         'build_elig_table_ctx_base', None),
    (0x0803a954, 0x0201c510, 'gDuelFieldSlots',         'build_elig_table_field_slots_b', None),

    # eval_slot_score_entry_full_with_sp_result
    (0x0803a9f8, 0x0201c510, 'gDuelFieldSlots',         'eval_slot_score_full_field_slots_a', None),

    # eval_equip_chain_score_for_slot
    (0x0803aa74, 0x0803777c, 'check_level_conv_lab_node_match', 'eval_equip_chain_pred_fnptr',
     'THUMB fn-ptr: check_level_conv_lab_node_match+1 (odd addr); asm must have +1 after re-export'),
    (0x0803aa78, 0x0201d9c0, 'gEquipNodePool',          'eval_equip_chain_node_pool_a', None),
    (0x0803ab1c, 0x0201d9c0, 'gEquipNodePool',          'eval_equip_chain_node_pool_b', None),
    (0x0803ab24, 0x0201c520, 'gDuelFieldSlotState',     'eval_equip_chain_slot_state_a', None),
    (0x0803aba8, 0x0201c5d8, 'gDuelFieldSlots_p2_base', 'eval_equip_chain_p2_slots_base', None),

    # get_slot_card_state_code
    (0x0803ac5c, 0x0201c510, 'gDuelFieldSlots',         'get_state_code_field_slots_a', None),

    # query_slot_card_state_code
    (0x0803ace4, 0x0201c510, 'gDuelFieldSlots',         'query_state_code_field_slots_a', None),
    (0x0803ad88, 0x0201c510, 'gDuelFieldSlots',         'query_state_code_field_slots_b', None),
    (0x0803ad8c, 0x0201d9c0, 'gEquipNodePool',          'query_state_code_node_pool_a', None),
    (0x0803ae64, 0x0201d9c0, 'gEquipNodePool',          'query_state_code_node_pool_b', None),
    (0x0803ae6c, 0x0201c520, 'gDuelFieldSlotState',     'query_state_code_slot_state_a', None),

    # resolve_slot_chain_best_target
    (0x0803aecc, 0x0201c510, 'gDuelFieldSlots',         'resolve_chain_target_field_slots_a', None),
    (0x0803af3c, 0x0201c510, 'gDuelFieldSlots',         'resolve_chain_target_field_slots_b', None),
    (0x0803b034, 0x0201d9c0, 'gEquipNodePool',          'resolve_chain_target_node_pool_a', None),
    (0x0803b070, 0x0201d9c0, 'gEquipNodePool',          'resolve_chain_target_node_pool_b', None),
    (0x0803b12c, 0x0201c520, 'gDuelFieldSlotState',     'resolve_chain_target_slot_state_a', None),

    # resolve_best_target_slot_for_equip
    (0x0803b1a0, 0x0201c510, 'gDuelFieldSlots',         'resolve_best_target_field_slots_a', None),

    # resolve_slot_chain_best_target (cont - 3rd node_pool slot)
    (0x0803b124, 0x0201d9c0, 'gEquipNodePool',          'resolve_chain_target_node_pool_c', None),

    # compute_slot_zone_eligibility_mask
    (0x0803b218, 0x0201c510, 'gDuelFieldSlots',         'compute_zone_mask_field_slots_a', None),

    # get_zone_slot_ptr
    (0x0803b2cc, 0x0803b2d0, 'get_zone_slot_ptr_switchD_table', 'get_zone_slot_ptr_switch_table_ptr', None),
    (0x0803b2f8, 0x0201c880, 'gP1ChainZoneArray',       'get_zone_slot_ptr_chain_zone_base', None),
    (0x0803b310, 0x0201c740, 'gP1SlotSetCodeArray',     'get_zone_slot_ptr_slot_set_code_base', None),
    (0x0803b328, 0x0201c8f8, 'gP1HandSlotArray',        'get_zone_slot_ptr_hand_slot_base', None),
    (0x0803b340, 0x0201cab0, 'gP1AltHandSlotArray',     'get_zone_slot_ptr_alt_hand_base', None),
    (0x0803b358, 0x0201c600, 'gP1FieldArrayCBase',      'get_zone_slot_ptr_field_c_base', None),
    (0x0803b380, 0x0201bc54, 'gDuelEffectChainSlots',   'get_zone_slot_ptr_effect_chain_base', None),
    (0x0803b3a4, 0x0201c510, 'gDuelFieldSlots',         'get_zone_slot_ptr_field_slots_a', None),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS
# ---------------------------------------------------------------------------
# (slot_addr, old_label, new_label, eol)
RENAME_SLOTS = [
    (0x0803aec4, 'DAT_0803aec4', 'resolve_gap_cid_149f',
     'gap CID 0x149f; not in card-stats.s (between Miracle Dig 0x149e and Vengeful Bog Spirit 0x14a1)'),
    (0x0803abac, 'DAT_0803abac', 'eval_equip_chain_p2_equip_word_base',
     '0x0201c5e8 = gDuelFieldSlots_p2_base+0x10; equip_word field in P2 slot entry; 1 ref'),
    (0x0803ad80, 'DAT_0803ad80', 'query_state_code_magic_zone_p0_base',
     '0x0201c574 = gDuelFieldSlots+5*20; P0 magic/trap zone slot[5] base; 1 ref'),
]

# ---------------------------------------------------------------------------
# Execute
# ---------------------------------------------------------------------------

print("=== RefineF03Seg5Slots.py DRY=%s ===" % DRY)

eq_ok = 0; eq_skip = 0
for (sa, val, eqn, sl, eol) in EQ_SLOTS:
    before = eq_ok
    _eq(sa, val, eqn, sl, eol)
    if not DRY:
        eq_ok += 1
    else:
        eq_ok += 1

print("EQ done: %d slots" % len(EQ_SLOTS))

for (sa, ta, gl, sl, eol) in REF_SLOTS:
    _ref(sa, ta, gl, sl, eol)

print("REF done: %d slots" % len(REF_SLOTS))

for (sa, ol, nl, eol) in RENAME_SLOTS:
    _rename(sa, ol, nl, eol)

print("RENAME done: %d slots" % len(RENAME_SLOTS))

print("=== COMPLETE: EQ=%d REF=%d RENAME=%d ===" % (len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS)))
