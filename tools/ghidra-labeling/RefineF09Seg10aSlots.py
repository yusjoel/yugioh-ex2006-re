# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF09Seg10aSlots.py -- p5 file09 Seg-10a (0x0807850c..0x08079500)
#   invoke_effect_node_with_active_flag_if_player_mismatch
#   dispatch_equip_target_slot_select_by_lp_state
#   route_equip_zone_sprite_by_activation_state
#   dispatch_equip_graveyard_sprite_by_lp_state
#   apply_lp_delta_for_specific_equip_card_type
#   decrement_zone_entry_slot_count
#   dispatch_neo_daedalus_hand_equip_oam_by_lp_state
#   enqueue_hand_spell_sprite_for_recycle_zone
#   dispatch_lp_row_and_bitmap_by_equip_state
#   invoke_setup_equip_oam_for_neo_daedalus_zone_e
#   enqueue_graveyard_spell_sprite_for_hand_slot
#   dispatch_equip_lp_bar_or_paired_zone_sprite
#   dispatch_equip_zone_sprite_seq_by_lp_state
#   (13 named functions; B1-B5 are ROM_INCBIN handled by DisassembleF09Seg10aBlocks.py)
#
# Sections:
#   A. EQ_SLOTS   -- 60 slots (58 REUSE + 2 NEW: CARD_TYPE_FIELD8_MASK, RECYCLE_CID)
#   B. REF_SLOTS  -- 3 slots
#   C. RENAME_SLOTS -- 0 slots
#   D. PLATE_REWRITES -- 0 updates
#
# New constants added to constants/card_info.inc BEFORE this script:
#   CARD_TYPE_FIELD8_MASK = 0xb4f80000  (apply_lp_delta_for_specific_equip_card_type)
#   RECYCLE_CID           = 0x000016d5  (enqueue_hand_spell_sprite_for_recycle_zone)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).
# NOTE: carve=0; disasm handled by DisassembleF09Seg10aBlocks.py

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
#    60 slots -- 58 REUSE + 2 NEW
# ---------------------------------------------------------------------------
EQ_SLOTS = [

    # =========================================================================
    # invoke_effect_node_with_active_flag_if_player_mismatch (0x0807850c)
    # =========================================================================

    # --- duel_field.inc: EQUIP_ACTIVE_CTX_OFF = 0x00000484 ---
    (0x08078540, 0x0201b290, 'gDuelPhaseFlags',
     'gduel_phase_pool_8540',
     'gDuelPhaseFlags: duel phase flags global (EWRAM)'),

    (0x08078544, 0x00000484, 'EQUIP_ACTIVE_CTX_OFF',
     'equip_active_ctx_pool_8544',
     'EQUIP_ACTIVE_CTX_OFF: equip activation context offset [gDuelPhaseFlags+0x484]'),

    # =========================================================================
    # dispatch_equip_target_slot_select_by_lp_state (0x08078550)
    # =========================================================================

    (0x080785ac, 0x0201b290, 'gDuelPhaseFlags',
     'gduel_phase_pool_85ac', None),

    (0x080785b0, 0x0201c4e0, 'gP1LifePoints',
     'gp1lp_pool_85b0',
     'gP1LifePoints: P1 LP tracking block base (EWRAM)'),

    (0x080785b4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_85b4',
     'PLAYER_BLOCK_STRIDE: byte stride per player data block (0x868)'),

    (0x080785b8, 0x0201e2a0, 'gDuelCardCtxBase',
     'gduel_card_ctx_pool_85b8',
     'gDuelCardCtxBase: duel card activation context base (EWRAM)'),

    # =========================================================================
    # route_equip_zone_sprite_by_activation_state (0x08078658)
    # =========================================================================

    (0x0807861c, 0x0201c4e0, 'gP1LifePoints',
     'gp1lp_pool_861c', None),

    (0x08078620, 0x00001d6c, 'ELIGIB_ANIM_STATE_OFF',
     'eligib_anim_state_pool_8620',
     'ELIGIB_ANIM_STATE_OFF: animation state index [gP1LifePoints+0x1d6c]'),

    (0x08078624, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_8624', None),

    (0x08078628, 0x00001d70, 'LP_BANISHER_CTX_OFF',
     'lp_banisher_ctx_pool_8628',
     'LP_BANISHER_CTX_OFF: banisher zone LP context [gP1LifePoints+0x1d70]'),

    (0x08078644, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF',
     'eligib_sprite_ctrl_pool_8644',
     'ELIGIB_SPRITE_CTRL_OFF: sprite display control [gP1LifePoints+0x1d68]'),

    (0x08078648, 0x00001d70, 'LP_BANISHER_CTX_OFF',
     'lp_banisher_ctx_pool_8648', None),

    # =========================================================================
    # dispatch_equip_graveyard_sprite_by_lp_state (0x080786a8)
    # =========================================================================

    (0x08078690, 0x0201b290, 'gDuelPhaseFlags',
     'gduel_phase_pool_8690', None),

    (0x08078694, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frame_pool_8694',
     'EQUIP_PHASE_FRAME_OFF: equip phase frame counter [gDuelPhaseFlags+0x4a4]'),

    (0x080786c4, 0x0201b290, 'gDuelPhaseFlags',
     'gduel_phase_pool_86c4', None),

    (0x080786ec, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frame_pool_86ec', None),

    (0x080786f0, 0x0201c4e0, 'gP1LifePoints',
     'gp1lp_pool_86f0', None),

    (0x080786f4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_86f4', None),

    (0x0807871c, 0x0201c4e0, 'gP1LifePoints',
     'gp1lp_pool_871c', None),

    (0x08078720, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_8720', None),

    (0x0807874c, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frame_pool_874c', None),

    (0x08078784, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frame_pool_8784', None),

    (0x08078788, 0x0201c4e0, 'gP1LifePoints',
     'gp1lp_pool_8788', None),

    # =========================================================================
    # apply_lp_delta_for_specific_equip_card_type (0x08078794)
    # =========================================================================

    (0x080787d4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_87d4', None),

    (0x080787d8, 0x0201c5d8, 'gDuelFieldSlots_p2_base',
     'gduel_slots_p2_pool_87d8',
     'gDuelFieldSlots_p2_base: P2 duel field slot array base (EWRAM)'),

    # --- NEW: CARD_TYPE_FIELD8_MASK = 0xb4f80000 ---
    (0x080787dc, 0xb4f80000, 'CARD_TYPE_FIELD8_MASK',
     'card_type_field8_mask_pool_87dc',
     'CARD_TYPE_FIELD8_MASK: (slot.field8<<0x13)==0xb4f80000 identifies specific equip type'),

    # =========================================================================
    # dispatch_neo_daedalus_hand_equip_oam_by_lp_state (0x08078808)
    # =========================================================================

    (0x08078828, 0x0201b290, 'gDuelPhaseFlags',
     'gduel_phase_pool_8828', None),

    (0x080788b0, 0x00001951, 'WATER_DRAGON_CID',
     'water_dragon_cid_pool_88b0',
     'WATER_DRAGON_CID: Water Dragon special path in Neo Daedalus OAM dispatch'),

    (0x080788b4, 0x0201b290, 'gDuelPhaseFlags',
     'gduel_phase_pool_88b4', None),

    (0x080788b8, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frame_pool_88b8', None),

    # =========================================================================
    # enqueue_hand_spell_sprite_for_recycle_zone (0x08078954)
    # =========================================================================

    (0x08078934, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frame_pool_8934', None),

    (0x08078938, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_8938', None),

    (0x0807893c, 0x0201c8f8, 'gP1HandSlotArray',
     'gp1_hand_slot_pool_893c',
     'gP1HandSlotArray: P1 hand slot data array base (EWRAM)'),

    (0x08078940, 0x0201b290, 'gDuelPhaseFlags',
     'gduel_phase_pool_8940', None),

    # --- NEW: RECYCLE_CID = 0x000016d5 ---
    (0x08078994, 0x000016d5, 'RECYCLE_CID',
     'recycle_cid_pool_8994',
     'RECYCLE_CID: card ID for Recycle (pw=96316857); differentiates Recycle zone from other hand spells'),

    # =========================================================================
    # dispatch_lp_row_and_bitmap_by_equip_state (0x080789b0)
    # =========================================================================

    (0x080789dc, 0x0201b290, 'gDuelPhaseFlags',
     'gduel_phase_pool_89dc', None),

    (0x080789fc, 0x0201c4e0, 'gP1LifePoints',
     'gp1lp_pool_89fc', None),

    (0x08078a00, 0x00001daa, 'LP_CARD_TRACK_NEXT_OFF',
     'lp_card_track_next_pool_8a00',
     'LP_CARD_TRACK_NEXT_OFF: LP card track next field [gP1LifePoints+0x1daa]'),

    # =========================================================================
    # invoke_setup_equip_oam_for_neo_daedalus_zone_e (0x08078a24)
    # =========================================================================

    (0x08078a88, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_8a88', None),

    (0x08078a8c, 0x0201c8f8, 'gP1HandSlotArray',
     'gp1_hand_slot_pool_8a8c', None),

    # =========================================================================
    # enqueue_graveyard_spell_sprite_for_hand_slot (0x08078bf8)
    # =========================================================================

    (0x08078c34, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_8c34', None),

    (0x08078c38, 0x0201c8f8, 'gP1HandSlotArray',
     'gp1_hand_slot_pool_8c38', None),

    # =========================================================================
    # dispatch_equip_lp_bar_or_paired_zone_sprite (0x08078c3c)
    # =========================================================================

    (0x08078cbc, 0x0201b290, 'gDuelPhaseFlags',
     'gduel_phase_pool_8cbc', None),

    # =========================================================================
    # dispatch_equip_zone_sprite_seq_by_lp_state (0x08078c94)
    # =========================================================================

    (0x08078d64, 0x0201c4e0, 'gP1LifePoints',
     'gp1lp_pool_8d64', None),

    (0x08078d68, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_8d68', None),

    (0x08078d6c, 0x0201b290, 'gDuelPhaseFlags',
     'gduel_phase_pool_8d6c', None),

    (0x08078d70, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frame_pool_8d70', None),

    (0x08078d9c, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frame_pool_8d9c', None),

    (0x08078da0, 0x0201c4e0, 'gP1LifePoints',
     'gp1lp_pool_8da0', None),

    (0x08078da4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_8da4', None),

    (0x08078dcc, 0x00008056, 'OAM_EFFECT_SLOT_TILE_P1',
     'oam_effect_slot_tile_p1_pool_8dcc',
     'OAM_EFFECT_SLOT_TILE_P1: effect-slot sprite tile OAM attr0 (0x56|OBJ_DIS bit15)'),

    (0x08078e60, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_8e60', None),

    (0x08078e64, 0x0201c740, 'gP1SlotSetCodeArray',
     'gp1_slot_set_code_pool_8e64',
     'gP1SlotSetCodeArray: P1 slot set_code data array base (EWRAM)'),

    (0x08078ea4, 0x0201b290, 'gDuelPhaseFlags',
     'gduel_phase_pool_8ea4', None),

    (0x08078ea8, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frame_pool_8ea8', None),

    (0x08078ee4, 0x0201b290, 'gDuelPhaseFlags',
     'gduel_phase_pool_8ee4', None),

    (0x08078f10, 0x0201c4e0, 'gP1LifePoints',
     'gp1lp_pool_8f10', None),

    (0x08078f14, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_8f14', None),

    (0x08078f44, 0x0201c4e0, 'gP1LifePoints',
     'gp1lp_pool_8f44', None),

    (0x08078f48, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_8f48', None),

]  # end EQ_SLOTS (60 slots)

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label, eol_ascii_or_None)
#    3 slots -- 2 self-ref fn-ptrs + 1 cross-module fn-ptr
# ---------------------------------------------------------------------------
REF_SLOTS = [

    # DWORD_080785bc -> invoke_effect_node_with_active_flag_if_player_mismatch+1
    # Self-ref fn-ptr: dispatch_equip_target_slot_select_by_lp_state calls
    # select_equip_target_slot_by_card_id(player, card_id, callback=0x0807850d)
    (0x080785bc, 0x0807850d,
     'invoke_effect_node_with_active_flag_if_player_mismatch',
     'REF_self_fn_ptr_bc',
     'fn-ptr: invoke_effect_node_with_active_flag_if_player_mismatch+1 (THUMB); callback to select_equip_target_slot_by_card_id'),

    # DWORD_080785d4 -> invoke_effect_node_with_active_flag_if_player_mismatch+1
    # Same self-ref fn-ptr used in init_zone_activation_display_fields(callback) call
    (0x080785d4, 0x0807850d,
     'invoke_effect_node_with_active_flag_if_player_mismatch',
     'REF_self_fn_ptr_d4',
     'fn-ptr: invoke_effect_node_with_active_flag_if_player_mismatch+1 (THUMB); callback to init_zone_activation_display_fields'),

    # DWORD_08078a20 -> check_equip_slot_eligible_by_side_match_and_type+1
    # fn-ptr to asm/06 check_equip_slot_eligible_by_side_match_and_type (0x08053f10+1)
    # used in dispatch_lp_row_and_bitmap_by_equip_state as r1=fn_ptr arg to build_equip_zone_bitmap_for_player
    (0x08078a20, 0x08053f11,
     'check_equip_slot_eligible_by_side_match_and_type',
     'REF_check_equip_slot_elig_fn_ptr',
     'fn-ptr: check_equip_slot_eligible_by_side_match_and_type+1 (THUMB); r1 callback to build_equip_zone_bitmap_for_player'),

]  # end REF_SLOTS (3 slots)

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: 0 slots
# ---------------------------------------------------------------------------
RENAME_SLOTS = []

# ---------------------------------------------------------------------------
# D. PLATE_REWRITES: 0 updates
# ---------------------------------------------------------------------------
PLATE_REWRITES = []

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
        print("[SKIP] EQ 0x%08x (%s) value mismatch" % (slot_addr, eq_name))
        return

    if DRY:
        print("[dry] EQ 0x%08x  %s=%s  label=%s" % (slot_addr, eq_name, hex(value), slot_label))
        return

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
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[EQ ] 0x%08x  %s  -> %s" % (slot_addr, eq_name, slot_label))

def _apply_ref(slot_addr, target_addr, gas_label, slot_label, eol):
    a_slot   = _addr(slot_addr)
    a_target = _addr(target_addr)
    sym_tbl  = currentProgram.getSymbolTable()

    if DRY:
        print("[dry] REF 0x%08x -> 0x%08x  gas=%s  slot=%s" % (
            slot_addr, target_addr, gas_label, slot_label))
        return

    # create USER label at target (fn body, not +1)
    tgt_body_addr = target_addr - 1  # target_addr is fn+1 (THUMB ptr)
    a_body = _addr(tgt_body_addr)
    tgt_syms = sym_tbl.getSymbols(a_body)
    tgt_names = [s.getName() for s in tgt_syms]
    if gas_label not in tgt_names:
        sym_tbl.createLabel(a_body, gas_label, SourceType.USER_DEFINED)

    # add DATA reference slot -> target (the +1 THUMB ptr value)
    refMgr = currentProgram.getReferenceManager()
    refMgr.addMemoryReference(a_slot, a_target, RefType.DATA, SourceType.USER_DEFINED, 0)

    # set primary on target label at body address
    for sym in sym_tbl.getSymbols(a_body):
        if sym.getName() == gas_label:
            sym.setPrimary()
            break

    # USER label at slot
    slot_syms = sym_tbl.getSymbols(a_slot)
    slot_names = [s.getName() for s in slot_syms]
    if slot_label not in slot_names:
        sym_tbl.createLabel(a_slot, slot_label, SourceType.USER_DEFINED)

    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a_slot)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[REF] 0x%08x -> 0x%08x  %s" % (slot_addr, target_addr, slot_label))

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF09Seg10aSlots (DRY=%s) ===" % DRY)
    print("  EQ=%d  REF=%d  RENAME=%d" % (len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS)))

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS ---")
    for (sa, val, eq_name, slot_label, eol) in EQ_SLOTS:
        _apply_eq(sa, val, eq_name, slot_label, eol)

    # B. REF_SLOTS
    print("\n--- B. REF_SLOTS ---")
    for (sa, ta, gas_label, slot_label, eol) in REF_SLOTS:
        _apply_ref(sa, ta, gas_label, slot_label, eol)

    # C. RENAME_SLOTS (none)
    print("\n--- C. RENAME_SLOTS (0 slots) ---")

    # D. PLATE_REWRITES (none)
    print("\n--- D. PLATE_REWRITES (0 updates) ---")

    print("\n=== RefineF09Seg10aSlots DONE ===")
    print("  EQ_SLOTS: %d" % len(EQ_SLOTS))
    print("  REF_SLOTS: %d" % len(REF_SLOTS))
    print("  NOTE: Run DisassembleF09Seg10aBlocks.py for B1-B5 disasm")

main()
