# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF08Seg3Slots.py -- F08 Seg-3 (0x08066448..0x08067160)
#   dispatch_equip_zone_sprite_by_slot_state + reserved-icid dispatch + lp-counter sprite
#   + equip zone render/enqueue cluster + effect-type dispatch + LP delta wrapper
#   EQ=51 (CIDs x5 new + globals x9 reuse + offsets x5 reuse + OAM x1 new + strides x14)
#   REF=4 (gP1LifePoints x2 raw-addr slots + dispatch table ptr x1 + switchD ptr x1)
#   RENAME=2 (placeholder slots to descriptive labels via EQ plan)
#   PLATE=2 (stale FUN_ substring replace in apply_lp_delta_for_slot_player)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK). Jython encodes CJK as
# double-UTF-8 mojibake -- any CJK here is a red-line error.
# Disasm block handled in DisassembleF08Seg3Blocks.py.
# New constants: card_info.inc +5 (DE_SPELL_CID/CYBER_STEIN_CID/ICID_RESERVED_A/B/C)
#                oam_attr.inc +1 (OAM_ATTR_P2_SPRITE)
#
# backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260617_215450-pre-F08Seg3

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
#    Creates equate (value->name) and references it from slot address.
#    Slot label MUST differ from eq_name to avoid GAS ldr/equate conflict.
# ---------------------------------------------------------------------------
EQ_SLOTS = [

    # ---- Group A: Card IDs -- dispatch_equip_zone_sprite_by_slot_state ----
    # ARMED_NINJA_CID = 0x117b (reuse card_info.inc)
    (0x080664b8, 0x0000117b, 'ARMED_NINJA_CID',
     'dispatch_equip_zone_by_slot_state_cid_a', None),
    # DE_SPELL_CID = 0x12eb (NEW card_info.inc)
    (0x080664bc, 0x000012eb, 'DE_SPELL_CID',
     'dispatch_equip_zone_by_slot_state_cid_b',
     'DE_SPELL_CID=0x12eb (pw=19159413; card_0673; second cmp in slot-state dispatch)'),

    # ---- Group B: Strides / field-slots ----
    # PLAYER_BLOCK_STRIDE = 0x868 (reuse ewram.inc x14)
    (0x080664c0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'dispatch_equip_zone_player_stride', None),
    # gDuelFieldSlots = 0x0201c510 (reuse ewram.inc)
    (0x080664c4, 0x0201c510, 'gDuelFieldSlots',
     'dispatch_equip_zone_field_slots', None),
    (0x08066594, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'enqueue_gyd_hand_slot_stride', None),
    (0x08066598, 0x0201c8f8, 'gP1HandSlotArray',
     'enqueue_gyd_hand_slots', None),

    # ---- Group C: dispatch_zone_state_for_reserved_icid_slot ----
    # ICID_RESERVED_A = 0x162c (NEW card_info.inc)
    (0x080665f0, 0x0000162c, 'ICID_RESERVED_A',
     'dispatch_reserved_icid_a',
     'ICID_RESERVED_A=0x162c (cid=0xFFFF reserved; no card-stats.s entry)'),
    # ICID_RESERVED_C = 0x1051 (NEW card_info.inc)
    (0x080665f4, 0x00001051, 'ICID_RESERVED_C',
     'dispatch_reserved_icid_c',
     'ICID_RESERVED_C=0x1051 (cid=0xFFFF reserved; no card-stats.s entry)'),
    # ICID_RESERVED_B = 0x184c (NEW card_info.inc)
    (0x08066600, 0x0000184c, 'ICID_RESERVED_B',
     'dispatch_reserved_icid_b',
     'ICID_RESERVED_B=0x184c (cid=0xFFFF reserved; no card-stats.s entry)'),
    # gDuelPhaseFlags = 0x0201b290 (reuse ewram.inc)
    (0x08066624, 0x0201b290, 'gDuelPhaseFlags',
     'dispatch_reserved_icid_phase_flags', None),
    # PLAYER_BLOCK_STRIDE (reuse)
    (0x08066664, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'dispatch_reserved_icid_state_stride', None),
    # gDuelCardCtxBase = 0x0201e2a0 (reuse ewram.inc)
    (0x08066668, 0x0201e2a0, 'gDuelCardCtxBase',
     'dispatch_reserved_icid_display_ctx', None),

    # ---- Group D: dispatch_lp_counter_or_sprite_by_zone_state ----
    # gDuelPhaseFlags (reuse)
    (0x080666b4, 0x0201b290, 'gDuelPhaseFlags',
     'dispatch_lp_ctr_phase_flags', None),
    # OAM_ATTR_P2_SPRITE = 0x8059 (NEW oam_attr.inc)
    (0x080666e0, 0x00008059, 'OAM_ATTR_P2_SPRITE',
     'dispatch_lp_ctr_p2_sprite_attr',
     'OAM_ATTR_P2_SPRITE=0x8059 (bit15=OBJ pal; 0x59=tile); P2 lp-counter sprite; sibling of OAM_ATTR_P1_SPRITE=0x8027'),

    # ---- Group E: render_equip_zone_sprites_both_players ----
    # P1LP_BLOCK2_OFF_1CE8 = 0x1ce8 (reuse ewram.inc)
    (0x08066734, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',
     'render_equip_zone_zone_state_off',
     'P1LP_BLOCK2_OFF_1CE8=0x1ce8: zone-15 sub-struct offset in gP1LifePoints block'),
    # gDuelEquipCtx = 0x0201bbbc (reuse ewram.inc)
    (0x08066738, 0x0201bbbc, 'gDuelEquipCtx',
     'render_equip_zone_equip_ctx', None),
    # PLAYER_BLOCK_STRIDE (reuse)
    (0x08066788, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'render_equip_zone_player_stride', None),

    # ---- Group F: enqueue_equip_zone_sprite_with_chain_check ----
    # PLAYER_BLOCK_STRIDE (reuse)
    (0x08066830, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'enqueue_equip_zone_chain_stride', None),
    # gDuelFieldSlots (reuse)
    (0x08066834, 0x0201c510, 'gDuelFieldSlots',
     'enqueue_equip_zone_chain_field_slots', None),
    # RAVIEL_LORD_CID = 0x19a5 (reuse card_info.inc)
    (0x08066838, 0x000019a5, 'RAVIEL_LORD_CID',
     'enqueue_equip_zone_chain_raviel_cid', None),

    # ---- Group G: dispatch_equip_zone_sprite_by_effect_type ----
    # gDuelPhaseFlags (reuse)
    (0x08066888, 0x0201b290, 'gDuelPhaseFlags',
     'dispatch_equip_zone_effect_type_phase_flags', None),

    # ---- Group H: apply_equip_activation_for_slot_with_chain_branch ----
    # PLAYER_BLOCK_STRIDE (reuse)
    (0x08066af0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'apply_equip_act_chain_stride', None),
    # gDuelFieldSlots (reuse)
    (0x08066af4, 0x0201c510, 'gDuelFieldSlots',
     'apply_equip_act_chain_field_slots', None),

    # ---- Group I: apply_equip_activation_across_slots ----
    # PLAYER_BLOCK_STRIDE (reuse)
    (0x08066be8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'apply_equip_act_slots_stride', None),
    # gDuelFieldSlots (reuse)
    (0x08066bec, 0x0201c510, 'gDuelFieldSlots',
     'apply_equip_act_slots_field_slots', None),

    # ---- Group J: apply_effect_node_sprites_all_zones ----
    # gEquipZoneCountTable = 0x0201e1c8 (reuse ewram.inc)
    (0x08066c3c, 0x0201e1c8, 'gEquipZoneCountTable',
     'apply_effect_node_zone_count_tbl', None),

    # ---- Group K: enqueue_equip_zone_sprite_with_spell_card_mode ----
    # PLAYER_BLOCK_STRIDE (reuse)
    (0x08066cbc, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'enqueue_equip_zone_spell_stride', None),
    # gDuelFieldSlots (reuse)
    (0x08066cc0, 0x0201c510, 'gDuelFieldSlots',
     'enqueue_equip_zone_spell_field_slots', None),
    # BATTLE_SCARRED_CID = 0x16a2 (reuse card_info.inc)
    (0x08066cc4, 0x000016a2, 'BATTLE_SCARRED_CID',
     'enqueue_equip_zone_spell_cid_a', None),
    # SHADOW_SPELL_CID = 0x1243 (reuse card_info.inc)
    (0x08066cc8, 0x00001243, 'SHADOW_SPELL_CID',
     'enqueue_equip_zone_spell_cid_b', None),
    # NINJITSU_ART_OF_DECOY_CID = 0x17ff (reuse card_info.inc)
    (0x08066d00, 0x000017ff, 'NINJITSU_ART_OF_DECOY_CID',
     'enqueue_equip_zone_spell_cid_c', None),

    # ---- Group L: enqueue_equip_zone_sprite_mode4_for_slot ----
    # PLAYER_BLOCK_STRIDE (reuse)
    (0x08066d5c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'enqueue_equip_zone_mode4_stride', None),
    # gDuelFieldSlots (reuse)
    (0x08066d60, 0x0201c510, 'gDuelFieldSlots',
     'enqueue_equip_zone_mode4_field_slots', None),
    # SANGA_OF_THUNDER_CID = 0x1119 (reuse card_info.inc)
    (0x08066d64, 0x00001119, 'SANGA_OF_THUNDER_CID',
     'enqueue_equip_zone_mode4_cid', None),

    # ---- Group M: enqueue_graveyard_sprite_for_polymerization_pair ----
    # POLYMERIZATION_CID = 0x12e5 (reuse card_info.inc)
    (0x08066da0, 0x000012e5, 'POLYMERIZATION_CID',
     'enqueue_gyd_poly_pair_cid', None),
    # PLAYER_BLOCK_STRIDE (reuse)
    (0x08066da4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'enqueue_gyd_poly_pair_stride', None),
    # gP1HandSlotArray (reuse)
    (0x08066da8, 0x0201c8f8, 'gP1HandSlotArray',
     'enqueue_gyd_poly_pair_hand_slots', None),

    # ---- Group N: dispatch_equip_oam_by_zone_state_with_cyberstein ----
    # gDuelPhaseFlags (reuse)
    (0x08066e2c, 0x0201b290, 'gDuelPhaseFlags',
     'dispatch_equip_oam_cyberstein_phase_flags', None),
    # CYBER_STEIN_CID = 0x114a (NEW card_info.inc)
    (0x08066ebc, 0x0000114a, 'CYBER_STEIN_CID',
     'dispatch_equip_oam_cyberstein_cid',
     'CYBER_STEIN_CID=0x114a (pw=69015963; card_0361; state=0x7e cmp in cyberstein dispatch)'),

    # ---- Group O: tick_equip_activation_display_seq ----
    # gDuelPhaseFlags (reuse)
    (0x08066f04, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_act_disp_seq_phase_flags', None),
    # TADPOLE_CID = 0x1919 (reuse card_info.inc)
    (0x08066f90, 0x00001919, 'TADPOLE_CID',
     'tick_equip_act_disp_seq_tadpole_cid', None),
    # EQUIP_PHASE_FRAME_OFF = 0x4a4 (reuse ewram.inc)
    (0x08066f94, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'tick_equip_act_disp_seq_frame_off_a',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: [gDuelPhaseFlags+0x4a4] equip effect frame counter'),
    (0x08066fa4, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'tick_equip_act_disp_seq_frame_off_b',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: [gDuelPhaseFlags+0x4a4] equip effect frame counter'),
    # PLAYER_BLOCK_STRIDE (reuse)
    (0x08066fec, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'tick_equip_act_disp_seq_stride', None),
    # gP1SlotSetCodeArray = 0x0201c740 (reuse ewram.inc)
    (0x08066ff0, 0x0201c740, 'gP1SlotSetCodeArray',
     'tick_equip_act_disp_seq_hand_slots', None),
    # gDuelPhaseFlags (reuse -- second slot in same fn)
    (0x08066ff4, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_act_disp_seq_phase_flags_b', None),
    # EQUIP_PHASE_FRAME_OFF (reuse -- third slot)
    (0x08066ff8, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'tick_equip_act_disp_seq_frame_off_c',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: [gDuelPhaseFlags+0x4a4] equip effect frame counter'),
    # gDuelCardCtxBase (reuse)
    (0x08067044, 0x0201e2a0, 'gDuelCardCtxBase',
     'tick_equip_act_disp_seq_card_ctx', None),

    # ---- Group P: tick_equip_activation_display_state ----
    # gDuelPhaseFlags (reuse)
    (0x080670c8, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_act_disp_state_phase_flags', None),
    # gDuelCardCtxBase (reuse)
    (0x080670f8, 0x0201e2a0, 'gDuelCardCtxBase',
     'tick_equip_act_disp_state_card_ctx', None),
    # LP_CARD_TRACK_NEXT_OFF = 0x1daa (reuse ewram.inc)
    (0x08067150, 0x00001daa, 'LP_CARD_TRACK_NEXT_OFF',
     'tick_equip_act_disp_state_lp_track_off',
     'LP_CARD_TRACK_NEXT_OFF=0x1daa: LP track next field offset in gP1LifePoints; sprite enqueue arg'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label, eol_ascii_or_None)
#    Adds a memory reference from slot to target, sets labels on both.
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # gP1LifePoints raw-addr slots (2)
    (0x08066660, 0x0201c4e0, 'gP1LifePoints',
     'dispatch_reserved_icid_lp_base',
     'gP1LifePoints=0x0201c4e0 raw addr; dispatch_zone_state_for_reserved_icid_slot state=0x80 path'),
    (0x08066730, 0x0201c4e0, 'gP1LifePoints',
     'render_equip_zone_lp_base',
     'gP1LifePoints=0x0201c4e0 raw addr; render_equip_zone_sprites_both_players ldr r0 -> mov r8'),
    # dispatch_equip_zone_by_effect_type jump table ptr
    (0x0806688c, 0x08066890, 'dispatch_equip_zone_by_effect_type_jump_table',
     'dispatch_equip_zone_effect_type_jump_tbl_ptr',
     'raw-addr jump table base at 0x08066890 (12 entries, states 0x75..0x80; MOV PC,r0 dispatch)'),
    # switchD table pointer
    (0x08066f08, 0x08066f0c, 'switchD_08066f02__switchdataD_08066f0c',
     'tick_equip_act_disp_seq_switch_tbl_ptr',
     'ptr to switchD_08066f02 data table at 0x08066f0c'),
]

# ---------------------------------------------------------------------------
# C. PLATE_REWRITES: (func_addr, old_text, new_text)
#    Replace stale FUN_ references in existing plate comments.
#    All text must be pure ASCII.
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    # apply_lp_delta_for_slot_player (0x080665a4):
    #   FUN_08073428 -> apply_lp_delta_for_slot_by_series_code
    (0x080665a4, 'FUN_08073428', 'apply_lp_delta_for_slot_by_series_code'),
    #   FUN_08074770 -> dispatch_dragon_summon_or_lp_delta_by_slot_type
    (0x080665a4, 'FUN_08074770', 'dispatch_dragon_summon_or_lp_delta_by_slot_type'),
]

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _check(slot_addr, expected_val, label):
    """Verify ROM dword at slot_addr == expected_val. Return True if OK."""
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
        print("[SKIP] EQ 0x%08x (%s) value mismatch -- WARN treated as FAIL" % (slot_addr, eq_name))
        return

    if DRY:
        print("[dry] EQ 0x%08x  %s=0x%x  label=%s" % (slot_addr, eq_name, value, slot_label))
        return

    # create/get equate
    eq = eq_tbl.getEquate(eq_name)
    if eq is None:
        eq = eq_tbl.createEquate(eq_name, value & 0xFFFFFFFFFFFFFFFFL)
    eq.addReference(a, 0)

    # create slot label
    existing = sym_tbl.getSymbols(a)
    names = [s.getName() for s in existing]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)

    # EOL comment (ASCII only)
    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            bad = any(ord(ch) > 127 for ch in eol)
            if bad:
                print("[WARN] non-ASCII in EOL @ 0x%08x -- skipping EOL" % slot_addr)
            else:
                cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[EQ ] 0x%08x  %s  -> %s" % (slot_addr, eq_name, slot_label))


def _apply_ref(slot_addr, target_addr, gas_label, slot_label, eol):
    """Add DATA reference from slot_addr to target_addr; set labels on both."""
    a_slot = _addr(slot_addr)
    a_target = _addr(target_addr)
    sym_tbl = currentProgram.getSymbolTable()
    ref_mgr = currentProgram.getReferenceManager()

    if DRY:
        print("[dry] REF 0x%08x -> 0x%08x  target=%s  slot=%s" % (
            slot_addr, target_addr, gas_label, slot_label))
        return

    # Label on target
    existing_t = sym_tbl.getSymbols(a_target)
    tnames = [s.getName() for s in existing_t]
    if gas_label not in tnames:
        sym_tbl.createLabel(a_target, gas_label, SourceType.USER_DEFINED)

    # DATA reference slot -> target
    ref_mgr.addMemoryReference(a_slot, a_target, RefType.DATA, SourceType.USER_DEFINED, 0)
    # Set primary for target label
    syms = list(sym_tbl.getSymbols(a_target))
    for s in syms:
        if s.getName() == gas_label:
            s.setPrimary()
            break

    # Slot label
    existing_s = sym_tbl.getSymbols(a_slot)
    snames = [s.getName() for s in existing_s]
    if slot_label not in snames:
        sym_tbl.createLabel(a_slot, slot_label, SourceType.USER_DEFINED)

    # EOL on slot
    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a_slot)
        if cu is not None:
            bad = any(ord(ch) > 127 for ch in eol)
            if bad:
                print("[WARN] non-ASCII in REF EOL @ 0x%08x -- skipping" % slot_addr)
            else:
                cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[REF] 0x%08x -> 0x%08x  %s  slot=%s" % (slot_addr, target_addr, gas_label, slot_label))


def _apply_plate_fix(func_addr, old_text, new_text):
    """Replace old_text with new_text in existing plate comment at func_addr."""
    for txt in [old_text, new_text]:
        if any(ord(ch) > 127 for ch in txt):
            print("[PLATE FAIL] non-ASCII in plate_fix text @ 0x%08x -- skipping" % func_addr)
            return

    a = _addr(func_addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[WARN] plate_fix 0x%08x: no code unit" % func_addr)
        return

    existing = cu.getComment(CodeUnit.PLATE_COMMENT)
    if existing is None:
        print("[WARN] plate_fix 0x%08x: no plate comment -- FAIL" % func_addr)
        return

    if old_text not in existing:
        print("[WARN] plate_fix 0x%08x: '%s' not found in plate -- FAIL" % (func_addr, old_text))
        return

    if DRY:
        print("[dry] PLATE_FIX 0x%08x: '%s' -> '%s'" % (func_addr, old_text, new_text))
        return

    new_plate = existing.replace(old_text, new_text)
    cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)
    print("[PFX] 0x%08x: '%s' -> '%s'" % (func_addr, old_text, new_text))


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF08Seg3Slots (DRY=%s) ===" % DRY)
    print("  Seg-3: 0x08066448..0x08067160")
    print("  EQ=%d  REF=%d  PLATE=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(PLATE_REWRITES)))

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    eq_ok = 0
    eq_fail = 0
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        mem = currentProgram.getMemory()
        a = _addr(slot_addr)
        try:
            actual = mem.getInt(a) & 0xFFFFFFFF
            if actual != (value & 0xFFFFFFFF):
                eq_fail += 1
                print("[FAIL] 0x%08x (%s): rom=0x%08x expect=0x%08x" % (
                    slot_addr, eq_name, actual, value & 0xFFFFFFFF))
                continue
        except Exception as e:
            eq_fail += 1
            print("[FAIL] 0x%08x (%s): read error %s" % (slot_addr, eq_name, e))
            continue
        _apply_eq(slot_addr, value, eq_name, slot_label, eol)
        eq_ok += 1
    print("  EQ done: %d ok, %d fail" % (eq_ok, eq_fail))
    if eq_fail > 0:
        print("  !!! %d EQ FAILURES -- check values before real run !!!" % eq_fail)

    # B. REF_SLOTS
    print("\n--- B. REF_SLOTS (%d) ---" % len(REF_SLOTS))
    ref_ok = 0
    for entry in REF_SLOTS:
        slot_addr, target_addr, gas_label, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        _apply_ref(slot_addr, target_addr, gas_label, slot_label, eol)
        ref_ok += 1
    print("  REF done: %d" % ref_ok)

    # C. PLATE_REWRITES
    print("\n--- C. PLATE_REWRITES (%d entries) ---" % len(PLATE_REWRITES))
    plate_ok = 0
    plate_fail = 0
    for func_addr, old_text, new_text in PLATE_REWRITES:
        a = _addr(func_addr)
        listing = currentProgram.getListing()
        cu = listing.getCodeUnitAt(a)
        if cu is None:
            print("[WARN] plate_fix 0x%08x: no code unit" % func_addr)
            plate_fail += 1
            continue
        existing = cu.getComment(CodeUnit.PLATE_COMMENT)
        if existing is None:
            print("[WARN] plate_fix 0x%08x: no plate comment" % func_addr)
            plate_fail += 1
            continue
        if old_text not in existing:
            print("[WARN] plate_fix 0x%08x: '%s' not found -- FAIL" % (func_addr, old_text))
            plate_fail += 1
            continue
        _apply_plate_fix(func_addr, old_text, new_text)
        plate_ok += 1
    print("  PLATE done: %d ok, %d fail" % (plate_ok, plate_fail))
    if plate_fail > 0:
        print("  !!! %d PLATE FAILURES -- check addresses !!!" % plate_fail)

    print("\n=== RefineF08Seg3Slots DONE ===")
    print("  EQ=%d/%d ok  REF=%d  PLATE=%d/%d ok" % (
        eq_ok, len(EQ_SLOTS), ref_ok, plate_ok, len(PLATE_REWRITES)))


main()
