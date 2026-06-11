# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF03Seg7Slots.py -- file 03 Seg-7 (0x0803bba4..0x0803c774)
#   eval_equip_placement_full_check .. tick_equip_candidate_scan_with_display
#   EQ=27, REF=28, RENAME=1, FUNC_RENAME=0, PLATE=8
#   carve=0, disasm=0, §5.1=1 (0x0803be38/0x14 dead THUMB, 0 refs)
#
# Sections:
#   A. EQ_SLOTS   -- data-equate
#       reuse (9): AMAZONESS_TIGER_CID, EQUIP_CHAIN_PAIR_CARD_MAX, NECROVALLEY_CID,
#                  P1LP_BLOCK2_OFF_1CE8, P1LP_BLOCK2_OFF(x2), DUEL_FIELD_OAM_TILE_IDX_A,
#                  SCENE_SLOT_MASK_LO, PLAYER_BLOCK_STRIDE
#       new (18): DISPLAY_SEQ_STEP_LOCK_OFF(x8), DISPLAY_SEQ_SLOT_IDX_OFF(x4),
#                 DISPLAY_SEQ_ACTIVE_PLAYER_OFF(x1), ACTIVATION_STATE_C_OFF(x1),
#                 DISPATCH_ACTIVE_FLAG_OFF(x1), SPRITE_ATTR_FIELD1_OFF(x1),
#                 SPRITE_ATTR_FIELD3_OFF(x1), BALLISTA_OF_RAMPART_SMASHING_CID(x1)
#   B. REF_SLOTS  -- USER-label + DATA-ref (28 slots)
#   C. RENAME_SLOTS -- switch table ptr label (1 slot)
#   D. PLATE_FIXES -- 8 fixes (1 full CJK->ASCII rewrite + 7 substring replaces)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).

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
    tgt = _addr(target_addr)
    sm = currentProgram.getSymbolTable()
    sm.createLabel(tgt, gas_label, SourceType.USER_DEFINED)
    rm = currentProgram.getReferenceManager()
    src = _addr(slot_addr)
    rm.addMemoryReference(src, tgt, RefType.DATA, SourceType.USER_DEFINED, 0)
    ref_list = rm.getReferencesFrom(src)
    for r in ref_list:
        if r.getToAddress().equals(tgt):
            rm.setPrimary(r, True)
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

    # --- card_info.inc: AMAZONESS_TIGER_CID = 0x160f (reuse, 1 slot) ---
    (0x0803bbf0, 0x160f, 'AMAZONESS_TIGER_CID', 'equip_check_amazoness_tiger_cid',
     'Amazoness Tiger (card_1303 slot=0x160F); special equip placement path'),

    # --- card_info.inc: EQUIP_CHAIN_PAIR_CARD_MAX = 0x164f (reuse, 1 slot) ---
    (0x0803bc20, 0x164f, 'EQUIP_CHAIN_PAIR_CARD_MAX', 'equip_check_chain_pair_max_cid',
     'EQUIP_CHAIN_PAIR_CARD_MAX=0x164f; upper bound for equip chain pair card range'),

    # --- card_info.inc: NECROVALLEY_CID = 0x159d (reuse, 1 slot) ---
    (0x0803bc4c, 0x159d, 'NECROVALLEY_CID', 'spell_zone_necrovalley_cid',
     'Necrovalley (card_1185 slot=0x159D); blocks spell-zone placement'),

    # --- new: DISPLAY_SEQ_STEP_LOCK_OFF = 0x80c (8 slots in Seg-7) ---
    (0x0803bc7c, 0x80c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'play_cond_step_lock_off_a',
     '[gDuelDisplaySeqState+0x80c] step lock / state clear flag'),
    (0x0803c314, 0x80c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'anim_queue_step_lock_off_a',
     '[gDuelDisplaySeqState+0x80c] step lock cleared at dispatch_duel_anim_queue_step exit'),
    (0x0803c3ac, 0x80c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'anim_queue_step_lock_off_b',
     '[gDuelDisplaySeqState+0x80c] step lock check in tick_duel_anim_event_hub'),
    (0x0803c51c, 0x80c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'op09_step_lock_off_a',
     '[gDuelDisplaySeqState+0x80c] cleared at tick_display_op09_seq exit'),
    (0x0803c560, 0x80c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'chain_link_step_lock_off_a',
     '[gDuelDisplaySeqState+0x80c] cleared at tick_equip_chain_link_display_seq exit'),
    (0x0803c670, 0x80c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'equip_set_step_lock_off_a',
     '[gDuelDisplaySeqState+0x80c] cleared at tick_equip_set_display_sequence exit'),
    (0x0803c704, 0x80c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'cand_scan_step_lock_off_a',
     '[gDuelDisplaySeqState+0x80c] cleared at tick_equip_candidate_scan_with_display'),
    (0x0803c770, 0x80c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'cand_scan_step_lock_off_b',
     '[gDuelDisplaySeqState+0x80c] cleared at tick_equip_candidate_scan_with_display exit'),

    # --- new: DISPLAY_SEQ_SLOT_IDX_OFF = 0x808 (4 slots) ---
    (0x0803bc80, 0x808, 'DISPLAY_SEQ_SLOT_IDX_OFF', 'play_cond_slot_idx_off_a',
     '[gDuelDisplaySeqState+0x808] sprite write slot index'),
    (0x0803bd90, 0x808, 'DISPLAY_SEQ_SLOT_IDX_OFF', 'enq_sprite_slot_idx_off_a',
     '[gDuelDisplaySeqState+0x808] slot index in enqueue_sprite_attr_record'),
    (0x0803bde0, 0x808, 'DISPLAY_SEQ_SLOT_IDX_OFF', 'write_sprite_slot_idx_off_a',
     '[gDuelDisplaySeqState+0x808] slot index in write_sprite_attrs_to_seq_buf'),
    (0x0803c514, 0x808, 'DISPLAY_SEQ_SLOT_IDX_OFF', 'op09_slot_idx_off_a',
     '[gDuelDisplaySeqState+0x808] slot index in tick_display_op09_seq'),

    # --- ewram.inc: P1LP_BLOCK2_OFF_1CE8 = 0x1ce8 (reuse, 1 slot) ---
    (0x0803bcc4, 0x1ce8, 'P1LP_BLOCK2_OFF_1CE8', 'play_cond_lp_block2_1ce8_a',
     '[gP1LifePoints+0x1ce8] LP display block2 field'),

    # --- new: DISPLAY_SEQ_ACTIVE_PLAYER_OFF = 0x1d10 (1 slot) ---
    (0x0803bcc8, 0x1d10, 'DISPLAY_SEQ_ACTIVE_PLAYER_OFF', 'play_cond_active_player_off_a',
     '[gP1LifePoints+0x1d10] active player field in display seq'),

    # --- new: ACTIVATION_STATE_C_OFF = 0x1d4c (1 slot) ---
    (0x0803bd00, 0x1d4c, 'ACTIVATION_STATE_C_OFF', 'play_cond_activation_c_off_a',
     '[gP1LifePoints+0x1d4c] activation state C; checked ==0 before play_ui_effect(0x31/0x32)'),

    # --- new: SPRITE_ATTR_FIELD1_OFF = 0x306 (1 slot) ---
    (0x0803be30, 0x306, 'SPRITE_ATTR_FIELD1_OFF', 'write_attr_field1_off_a',
     '[gSpriteAttrBuf+0x306] sprite attr halfword 1'),

    # --- new: SPRITE_ATTR_FIELD3_OFF = 0x30a (1 slot) ---
    (0x0803be34, 0x30a, 'SPRITE_ATTR_FIELD3_OFF', 'write_attr_field3_off_a',
     '[gSpriteAttrBuf+0x30a] sprite attr halfword 3'),

    # --- new: DISPATCH_ACTIVE_FLAG_OFF = 0x1d38 (1 slot) ---
    (0x0803be78, 0x1d38, 'DISPATCH_ACTIVE_FLAG_OFF', 'dispatch_active_flag_off_a',
     '[gP1LifePoints+0x1d38] display dispatch in-progress flag; set :=1 at dispatch_duel_event_display_seq entry'),

    # --- duel_field.inc: SCENE_SLOT_MASK_LO = 0xfff (reuse, 1 slot) ---
    (0x0803be80, 0xfff, 'SCENE_SLOT_MASK_LO', 'dispatch_event_code_mask_a',
     'SCENE_SLOT_MASK_LO=0xfff; extracts event_code bits[11:0] from hword[0]'),

    # --- ewram.inc: P1LP_BLOCK2_OFF = 0x1d08 (reuse, 2 slots) ---
    (0x0803c3f0, 0x1d08, 'P1LP_BLOCK2_OFF', 'anim_event_lp_block2_a',
     '[gP1LifePoints+0x1d08] LP display block2 field'),
    (0x0803c524, 0x1d08, 'P1LP_BLOCK2_OFF', 'op09_lp_block2_a',
     '[gP1LifePoints+0x1d08] LP display block2 field'),

    # --- duel_field.inc: DUEL_FIELD_OAM_TILE_IDX_A = 0x814 (reuse, 1 slot) ---
    (0x0803c528, 0x814, 'DUEL_FIELD_OAM_TILE_IDX_A', 'op09_oam_tile_idx_a',
     'DUEL_FIELD_OAM_TILE_IDX_A=0x814; OAM tile index for duel field card sprite'),

    # --- new: BALLISTA_OF_RAMPART_SMASHING_CID = 0x1846 (1 slot) ---
    (0x0803c66c, 0x1846, 'BALLISTA_OF_RAMPART_SMASHING_CID', 'chain_link_ballista_cid',
     'Ballista of Rampart Smashing (pw=00242146; card_4305 slot=0x1846); chain pool index'),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x868 (reuse, 1 slot) ---
    (0x0803c6fc, 0x868, 'PLAYER_BLOCK_STRIDE', 'equip_set_player_stride_a',
     'PLAYER_BLOCK_STRIDE=0x868; player data block stride'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS
# ---------------------------------------------------------------------------
# (slot_addr, target_addr, gas_label, slot_label, eol_or_None)
REF_SLOTS = [
    # check_card_play_condition_eligible (0x0803bc58)
    (0x0803bc78, 0x0201bcc0, 'gDuelDisplaySeqState', 'play_cond_display_state_a', None),
    (0x0803bcbc, 0x0201e2a0, 'gDuelCardCtxBase',     'play_cond_card_ctx_a',      None),
    (0x0803bcc0, 0x0201c4e0, 'gP1LifePoints',        'play_cond_lp_base_a',       None),
    (0x0803bcfc, 0x0201c4e0, 'gP1LifePoints',        'play_cond_lp_base_b',       None),

    # enqueue_sprite_attr_record (0x0803bd2c)
    (0x0803bd28, 0x0201b870, 'gSpriteAttrBuf',       'sprite_record_buf_base_a',  None),
    (0x0803bd88, 0x0201e2a0, 'gDuelCardCtxBase',     'enq_sprite_ctx_base_a',     None),
    (0x0803bd8c, 0x0201bcc0, 'gDuelDisplaySeqState', 'enq_sprite_seq_state_a',    None),

    # write_sprite_attrs_to_seq_buf (0x0803bd94)
    (0x0803bddc, 0x0201bcc0, 'gDuelDisplaySeqState', 'write_sprite_seq_state_a',  None),

    # write_sprite_attr_record_entry (0x0803bde4)
    (0x0803be2c, 0x0201b870, 'gSpriteAttrBuf',       'write_attr_entry_buf_base_a', None),

    # dispatch_duel_event_display_seq (0x0803be4c)
    (0x0803be74, 0x0201c4e0, 'gP1LifePoints',        'dispatch_lp_base_a',        None),
    (0x0803be7c, 0x0201bcc0, 'gDuelDisplaySeqState', 'dispatch_seq_state_a',      None),

    # dispatch_duel_anim_queue_step (0x0803c318)
    (0x0803c334, 0x0201b870, 'gSpriteAttrBuf',       'anim_queue_sprite_buf_a',   None),
    (0x0803c3a8, 0x0201bcc0, 'gDuelDisplaySeqState', 'anim_queue_seq_state_a',    None),
    (0x0803c3b0, 0x0201b870, 'gSpriteAttrBuf',       'anim_queue_sprite_buf_b',   None),

    # tick_duel_anim_event_hub (0x0803c3b4)
    (0x0803c3ec, 0x0201c4e0, 'gP1LifePoints',        'anim_event_lp_base_a',      None),
    (0x0803c3f4, 0x0201b870, 'gSpriteAttrBuf',       'anim_event_sprite_buf_a',   None),

    # tick_display_op09_seq (0x0803c53c)
    (0x0803c510, 0x0201bcc0, 'gDuelDisplaySeqState', 'anim_event_seq_state_a',    None),
    (0x0803c518, 0x0201b870, 'gSpriteAttrBuf',       'anim_event_sprite_buf_b',   None),
    (0x0803c520, 0x0201c4e0, 'gP1LifePoints',        'anim_event_lp_base_b',      None),
    (0x0803c52c, 0x0201e2a0, 'gDuelCardCtxBase',     'anim_event_ctx_base_a',     None),
    (0x0803c55c, 0x0201bcc0, 'gDuelDisplaySeqState', 'op09_seq_state_a',          None),

    # tick_equip_chain_link_display_seq (0x0803c564)
    (0x0803c660, 0x0201bcc0, 'gDuelDisplaySeqState', 'chain_link_seq_state_a',    None),
    (0x0803c664, 0x0201bb90, 'gEquipChainSlotRefs',  'chain_link_slot_refs_a',    None),
    (0x0803c668, 0x0201c510, 'gDuelFieldSlots',      'chain_link_field_slots_a',  None),

    # tick_equip_set_display_sequence (0x0803c674)
    (0x0803c6f4, 0x0201bcc0, 'gDuelDisplaySeqState', 'equip_set_seq_state_a',     None),
    (0x0803c6f8, 0x0201bb90, 'gEquipChainSlotRefs',  'equip_set_slot_refs_a',     None),
    (0x0803c700, 0x0201c510, 'gDuelFieldSlots',      'equip_set_field_slots_a',   None),

    # tick_equip_candidate_scan_with_display (0x0803c708)
    (0x0803c76c, 0x0201bcc0, 'gDuelDisplaySeqState', 'cand_scan_seq_state_a',     None),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS
# ---------------------------------------------------------------------------
# (slot_addr, old_label, new_label, eol)
RENAME_SLOTS = [
    (0x0803be84, 'DAT_0803be84', 'dispatch_event_switch_table_ptr',
     'ptr to switchD_0803be70__switchdataD_0803be88; 115-entry dispatch table for event codes 0x1..0x73'),
]

# ---------------------------------------------------------------------------
# D. PLATE_FIXES
# ---------------------------------------------------------------------------

def _get_plate(addr_int):
    cu = currentProgram.getListing().getCodeUnitAt(_addr(addr_int))
    if cu is None:
        return None
    return cu.getComment(CodeUnit.PLATE_COMMENT)

def _set_plate(addr_int, text):
    cu = currentProgram.getListing().getCodeUnitAt(_addr(addr_int))
    if cu is None:
        print("WARN: no code unit at 0x%08x for plate" % addr_int)
        return False
    cu.setComment(CodeUnit.PLATE_COMMENT, text)
    return True

def apply_plate_fixes():
    # Fix 1: check_card_play_condition_eligible @ 0x0803bc58
    # Full setPlateComment rewrite: CJK->ASCII + FUN_080c9f50->render_card_view_scene_by_lp_time
    addr = 0x0803bc58
    ascii_plate = (
        "Checks if the card play / effect condition is satisfied. "
        "r0 = context index (value from ldr r0,[r0,#0x4] at call site in render_card_view_scene_by_lp_time). "
        "Phase 1: checks [gDuelDisplaySeqState+0x80c] and [+0x808] both ==0; if either nonzero returns 0 (blocked). "
        "Phase 2: reads [gDuelCardCtxBase+0x8] as entry_type; if entry_type==1: reads gP1LifePoints+0x1ce8 "
        "(player LP field), compares with r0; if match checks gP1LifePoints+0x1d10 nonzero, then "
        "gP1LifePoints+0x1d40 (0x1ce8+0x30+0x18) for value==3. Returns 1 only if all conditions pass. "
        "Phase 3 (fallthrough): checks gDuelDisplaySeqState[+0x4]==r0 (slot context match); if match: "
        "reads gP1LifePoints+0x1d4c; if 0 calls play_ui_effect(0x31) and play_ui_effect(0x32); sets result. "
        "Side path LAB_0803bd04: reads [gSpriteAttrBuf+0x300] byte bit7; if 0 calls check_player_side_condition. "
        "Returns 0 (blocked) or 1 (condition satisfied). Side effects: play_ui_effect(0x31)/(0x32) conditionally. "
        "Constants: gDuelDisplaySeqState=0x0201bcc0, gP1LifePoints=0x0201c4e0, gSpriteAttrBuf=0x0201b870, "
        "step_lock_off=0x80c, slot_idx_off=0x808, lp_field_off=0x1ce8, active_field_off=0x1d10, "
        "target_field_off=0x1d4c, ui_sfx_occupied=0x31, ui_sfx_blocked=0x32. indeg=1."
    )
    if DRY:
        print("DRY PLATE fix1: 0x%08x full CJK->ASCII rewrite (%d chars)" % (addr, len(ascii_plate)))
    else:
        _set_plate(addr, ascii_plate)
        print("PLATE fix1 ok: 0x%08x CJK->ASCII rewrite (check_card_play_condition_eligible)" % addr)

    # Fix 2: write_sprite_attrs_to_seq_buf @ 0x0803bd94
    # substring: FUN_08094c10 -> poll_sprite_seq_until_done
    addr = 0x0803bd94
    old_text = _get_plate(addr)
    if old_text is None:
        print("WARN: no plate at write_sprite_attrs_to_seq_buf (0x0803bd94)")
    elif "FUN_08094c10" in old_text:
        new_text = old_text.replace("FUN_08094c10", "poll_sprite_seq_until_done")
        if DRY:
            print("DRY PLATE fix2: 0x%08x FUN_08094c10->poll_sprite_seq_until_done" % addr)
        else:
            _set_plate(addr, new_text)
            print("PLATE fix2 ok: 0x%08x replaced FUN_08094c10" % addr)
    else:
        print("PLATE fix2: FUN_08094c10 not found in plate at 0x%08x (already fixed?)" % addr)

    # Fix 3: dispatch_duel_event_display_seq @ 0x0803be4c
    # substring x2: FUN_0803c318->dispatch_duel_anim_queue_step; FUN_0803c3b4->tick_duel_anim_event_hub
    addr = 0x0803be4c
    old_text = _get_plate(addr)
    if old_text is None:
        print("WARN: no plate at dispatch_duel_event_display_seq (0x0803be4c)")
    else:
        new_text = old_text
        changed = False
        if "FUN_0803c318" in new_text:
            new_text = new_text.replace("FUN_0803c318", "dispatch_duel_anim_queue_step")
            changed = True
        if "FUN_0803c3b4" in new_text:
            new_text = new_text.replace("FUN_0803c3b4", "tick_duel_anim_event_hub")
            changed = True
        if changed:
            if DRY:
                print("DRY PLATE fix3: 0x%08x FUN_0803c318->dispatch_duel_anim_queue_step; FUN_0803c3b4->tick_duel_anim_event_hub" % addr)
            else:
                _set_plate(addr, new_text)
                print("PLATE fix3 ok: 0x%08x replaced FUN_0803c318 and/or FUN_0803c3b4" % addr)
        else:
            print("PLATE fix3: no FUN_0803c318/FUN_0803c3b4 in plate at 0x%08x (already fixed?)" % addr)

    # Fix 4: tick_duel_anim_event_hub @ 0x0803c3b4
    # substring: FUN_0803c318 -> dispatch_duel_anim_queue_step
    addr = 0x0803c3b4
    old_text = _get_plate(addr)
    if old_text is None:
        print("WARN: no plate at tick_duel_anim_event_hub (0x0803c3b4)")
    elif "FUN_0803c318" in old_text:
        new_text = old_text.replace("FUN_0803c318", "dispatch_duel_anim_queue_step")
        if DRY:
            print("DRY PLATE fix4: 0x%08x FUN_0803c318->dispatch_duel_anim_queue_step" % addr)
        else:
            _set_plate(addr, new_text)
            print("PLATE fix4 ok: 0x%08x replaced FUN_0803c318" % addr)
    else:
        print("PLATE fix4: FUN_0803c318 not found in plate at 0x%08x (already fixed?)" % addr)

    # Fix 5: tick_display_op09_seq @ 0x0803c53c
    # substring: FUN_0803be4c -> dispatch_duel_event_display_seq
    addr = 0x0803c53c
    old_text = _get_plate(addr)
    if old_text is None:
        print("WARN: no plate at tick_display_op09_seq (0x0803c53c)")
    elif "FUN_0803be4c" in old_text:
        new_text = old_text.replace("FUN_0803be4c", "dispatch_duel_event_display_seq")
        if DRY:
            print("DRY PLATE fix5: 0x%08x FUN_0803be4c->dispatch_duel_event_display_seq" % addr)
        else:
            _set_plate(addr, new_text)
            print("PLATE fix5 ok: 0x%08x replaced FUN_0803be4c" % addr)
    else:
        print("PLATE fix5: FUN_0803be4c not found in plate at 0x%08x (already fixed?)" % addr)

    # Fix 6: tick_equip_chain_link_display_seq @ 0x0803c564
    # substring: FUN_0803be4c -> dispatch_duel_event_display_seq
    addr = 0x0803c564
    old_text = _get_plate(addr)
    if old_text is None:
        print("WARN: no plate at tick_equip_chain_link_display_seq (0x0803c564)")
    elif "FUN_0803be4c" in old_text:
        new_text = old_text.replace("FUN_0803be4c", "dispatch_duel_event_display_seq")
        if DRY:
            print("DRY PLATE fix6: 0x%08x FUN_0803be4c->dispatch_duel_event_display_seq" % addr)
        else:
            _set_plate(addr, new_text)
            print("PLATE fix6 ok: 0x%08x replaced FUN_0803be4c" % addr)
    else:
        print("PLATE fix6: FUN_0803be4c not found in plate at 0x%08x (already fixed?)" % addr)

    # Fix 7: tick_equip_set_display_sequence @ 0x0803c674
    # substring: FUN_0803be4c -> dispatch_duel_event_display_seq
    addr = 0x0803c674
    old_text = _get_plate(addr)
    if old_text is None:
        print("WARN: no plate at tick_equip_set_display_sequence (0x0803c674)")
    elif "FUN_0803be4c" in old_text:
        new_text = old_text.replace("FUN_0803be4c", "dispatch_duel_event_display_seq")
        if DRY:
            print("DRY PLATE fix7: 0x%08x FUN_0803be4c->dispatch_duel_event_display_seq" % addr)
        else:
            _set_plate(addr, new_text)
            print("PLATE fix7 ok: 0x%08x replaced FUN_0803be4c" % addr)
    else:
        print("PLATE fix7: FUN_0803be4c not found in plate at 0x%08x (already fixed?)" % addr)

    # Fix 8: tick_equip_candidate_scan_with_display @ 0x0803c708
    # substring: FUN_0803be4c -> dispatch_duel_event_display_seq
    addr = 0x0803c708
    old_text = _get_plate(addr)
    if old_text is None:
        print("WARN: no plate at tick_equip_candidate_scan_with_display (0x0803c708)")
    elif "FUN_0803be4c" in old_text:
        new_text = old_text.replace("FUN_0803be4c", "dispatch_duel_event_display_seq")
        if DRY:
            print("DRY PLATE fix8: 0x%08x FUN_0803be4c->dispatch_duel_event_display_seq" % addr)
        else:
            _set_plate(addr, new_text)
            print("PLATE fix8 ok: 0x%08x replaced FUN_0803be4c" % addr)
    else:
        print("PLATE fix8: FUN_0803be4c not found in plate at 0x%08x (already fixed?)" % addr)


# ---------------------------------------------------------------------------
# Execute
# ---------------------------------------------------------------------------

print("=== RefineF03Seg7Slots.py DRY=%s ===" % DRY)

for (sa, val, eqn, sl, eol) in EQ_SLOTS:
    _eq(sa, val, eqn, sl, eol)

print("EQ done: %d slots" % len(EQ_SLOTS))

for (sa, ta, gl, sl, eol) in REF_SLOTS:
    _ref(sa, ta, gl, sl, eol)

print("REF done: %d slots" % len(REF_SLOTS))

for (sa, ol, nl, eol) in RENAME_SLOTS:
    _rename(sa, ol, nl, eol)

print("RENAME done: %d slots" % len(RENAME_SLOTS))

apply_plate_fixes()
print("PLATE done: 8 fixes")

print("=== COMPLETE: EQ=%d REF=%d RENAME=%d PLATE=8 DRY=%s ===" % (
    len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), DRY))
