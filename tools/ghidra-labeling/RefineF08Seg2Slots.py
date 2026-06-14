# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF08Seg2Slots.py -- F08 Seg-2 (0x0806544c..0x08066448)
#   write_equip_lp_delta_goblin_thief + LP delta + switchD_08065a44 cluster
#   EQ=65 (LP delta + PLAYER_BLOCK_STRIDE + globals + CIDs + offsets + OAM attr)
#   REF=13 (fn-ptr .word <fn>+1 + table pointers)
#   RENAME=10 (PTR_gP1LifePoints_* -> descriptive labels)
#   PLATE=11 (stale FUN_ replacements + gEquipEffectCtx fix)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK). Jython encodes CJK as
# double-UTF-8 mojibake -- any CJK here is a red-line error.
# Three disasm blocks handled in DisassembleF08Seg2Blocks.py.
# New constants: equip_lp_delta.inc +1 / ewram.inc +1 / oam_attr.inc +1 / card_info.inc +17

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

    # ---- Group A: LP delta equates (equip_lp_delta.inc) ----
    # LP_EQUIP_DELTA_NEG_500 = reuse (already in equip_lp_delta.inc)
    (0x08065464, 0xfffffe0c, 'LP_EQUIP_DELTA_NEG_500',
     'write_equip_lp_delta_goblin_thief_neg500',
     'LP_EQUIP_DELTA_NEG_500 = -500 (s32); Goblin Thief opponent LP penalty'),
    # LP_EQUIP_DELTA_NEG_2000 = reuse
    (0x08065480, 0xfffff830, 'LP_EQUIP_DELTA_NEG_2000',
     'write_equip_lp_delta_granadora_neg2000',
     'LP_EQUIP_DELTA_NEG_2000 = -2000 (s32); Granadora attack-pos penalty'),
    # LP_EQUIP_DELTA_NEG_1000 = NEW (equip_lp_delta.inc)
    (0x080654f4, 0xfffffc18, 'LP_EQUIP_DELTA_NEG_1000',
     'write_equip_lp_delta_atomic_firefly_neg1000',
     'LP_EQUIP_DELTA_NEG_1000 = -1000 (s32); Atomic Firefly / Mecha-Dog Marron LP penalty'),
    # LP_EQUIP_DELTA_NEG_1000 = reuse (second slot)
    (0x08065554, 0xfffffc18, 'LP_EQUIP_DELTA_NEG_1000',
     'write_equip_lp_delta_mecha_dog_marron_neg1000',
     'LP_EQUIP_DELTA_NEG_1000 = -1000 (s32); Mecha-Dog Marron conditional own-side penalty'),
    # LP_EQUIP_DELTA_NEG_800 = reuse
    (0x08065584, 0xfffffce0, 'LP_EQUIP_DELTA_NEG_800',
     'write_equip_lp_delta_twin_swords_neg800',
     'LP_EQUIP_DELTA_NEG_800 = -800 (s32); shared path penalty'),

    # ---- Group B: PLAYER_BLOCK_STRIDE = 0x868 (10 slots, reuse ewram.inc L250) ----
    (0x080654b4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'write_equip_lp_delta_saturn_stride', None),
    (0x080655e8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'restore_equip_effect_frame_stride', None),
    (0x0806586c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'dispatch_draw_ctr_helping_robo_stride', None),
    (0x0806588c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'dispatch_draw_ctr_royal_lib_stride', None),
    (0x08065940, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'dispatch_draw_ctr_bubbleman_stride', None),
    (0x08065cc4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'tick_dragon_summon_display_stride', None),
    (0x08065d64, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_slot_dark_magic_pair_stride', None),
    (0x0806616c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'drive_equip_slot_bitmap_stride', None),
    (0x080661dc, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'dispatch_equip_chain_state_stride', None),
    (0x08066440, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'enqueue_state2_sprites_stride', None),

    # ---- Group C: Global pointers (ewram.inc reuse) ----
    # gEquipChainSlotRefs = 0x0201bb90
    (0x080654e0, 0x0201bb90, 'gEquipChainSlotRefs',
     'write_equip_lp_delta_marshmallon_ctx_ptr',
     'gEquipChainSlotRefs[+0x0]=player_id via EQUIP_CTX_PLAYER_OFF'),
    # gDuelPhaseFlags = 0x0201b290 (7 slots)
    (0x080659d4, 0x0201b290, 'gDuelPhaseFlags',
     'check_equip_activation_at_slot11_phase_flags', None),
    (0x08065a48, 0x0201b290, 'gDuelPhaseFlags',
     'tick_dragon_summon_phase_flags_a', None),
    (0x08065ae4, 0x0201b290, 'gDuelPhaseFlags',
     'tick_dragon_summon_phase_flags_b', None),
    (0x08065b54, 0x0201b290, 'gDuelPhaseFlags',
     'tick_dragon_summon_phase_flags_c', None),
    (0x08065cc8, 0x0201b290, 'gDuelPhaseFlags',
     'tick_dragon_summon_display_phase_flags', None),
    (0x08066160, 0x0201b290, 'gDuelPhaseFlags',
     'drive_equip_slot_bitmap_phase_flags', None),
    (0x08066228, 0x0201b290, 'gDuelPhaseFlags',
     'dispatch_equip_chain_state_phase_flags', None),
    # gDuelFieldSlots = 0x0201c510 (4 slots)
    (0x08065d68, 0x0201c510, 'gDuelFieldSlots',
     'check_slot_dark_magic_pair_field_slots', None),
    (0x08066164, 0x0201c510, 'gDuelFieldSlots',
     'drive_equip_slot_bitmap_field_slots', None),
    (0x080661e4, 0x0201c510, 'gDuelFieldSlots',
     'dispatch_equip_chain_state_field_slots', None),
    (0x08066444, 0x0201c510, 'gDuelFieldSlots',
     'enqueue_state2_sprites_field_slots', None),
    # gDuelCardCtxBase = 0x0201e2a0 (2 slots)
    (0x08065b1c, 0x0201e2a0, 'gDuelCardCtxBase',
     'tick_dragon_summon_card_ctx_a', None),
    (0x08065c4c, 0x0201e2a0, 'gDuelCardCtxBase',
     'tick_dragon_summon_card_ctx_b', None),
    # gEquipZoneCountTable = 0x0201e1c8 (1 slot)
    (0x080661e0, 0x0201e1c8, 'gEquipZoneCountTable',
     'drive_equip_slot_bitmap_equip_zone_table', None),

    # ---- Group D: gDuelPhaseFlags offsets ----
    # EQUIP_ACTIVE_CTX_OFF = 0x484 (reuse duel_field.inc)
    (0x080659d8, 0x00000484, 'EQUIP_ACTIVE_CTX_OFF',
     'check_equip_activation_at_slot11_ctx_off',
     'EQUIP_ACTIVE_CTX_OFF = 0x484: equip active ctx slot ptr in gDuelPhaseFlags'),
    # EQUIP_PHASE_FRAME_OFF = 0x4a4 (NEW ewram.inc -- 3 slots)
    (0x08065ae8, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'tick_dragon_summon_frame_off_a',
     'EQUIP_PHASE_FRAME_OFF = 0x4a4: [gDuelPhaseFlags+0x4a4] effect frame counter'),
    (0x08065b58, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'tick_dragon_summon_frame_off_b',
     'EQUIP_PHASE_FRAME_OFF = 0x4a4: [gDuelPhaseFlags+0x4a4] effect frame counter'),
    (0x08065ccc, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'tick_dragon_summon_display_frame_off',
     'EQUIP_PHASE_FRAME_OFF = 0x4a4: [gDuelPhaseFlags+0x4a4] effect frame counter'),

    # ---- Group E: gP1LifePoints offsets ----
    # LP_BANISHER_CTX_OFF = 0x1d70 (reuse ewram.inc)
    (0x08065cbc, 0x00001d70, 'LP_BANISHER_CTX_OFF',
     'tick_dragon_summon_display_ctr_off',
     'LP_BANISHER_CTX_OFF = 0x1d70: display state counter field in gP1LifePoints'),

    # ---- Group F: Card IDs -- REUSE (21 from card_info.inc) ----
    # CID values reused from card_info.inc
    (0x08065d6c, 0x00000fc9, 'DARK_MAGICIAN_CID',
     'check_slot_dark_magic_pair_dm_cid', None),
    (0x08065738, 0x00001082, 'MASKED_SORCERER_CID',
     'dispatch_draw_ctr_masked_sorcerer_cid', None),
    (0x08065754, 0x00001353, 'APPROPRIATE_CID',
     'dispatch_draw_ctr_appropriate_cid', None),
    (0x08065784, 0x00001533, 'DES_LACOODA_CID',
     'dispatch_draw_ctr_des_lacooda_cid', None),
    (0x0806577c, 0x00001563, 'TOON_MASKED_SORCERER_CID',
     'dispatch_draw_ctr_toon_masked_sorc_cid', None),
    (0x0806579c, 0x000015dc, 'HELPING_ROBO_FOR_COMBAT_CID',
     'dispatch_draw_ctr_helping_robo_cid', None),
    (0x080657a4, 0x0000161a, 'ROYAL_MAGICAL_LIBRARY_CID',
     'dispatch_draw_ctr_royal_lib_cid', None),
    (0x080657d0, 0x000017d5, 'DARK_MIMIC_LV1_CID',
     'dispatch_draw_ctr_dark_mimic_lv1_cid', None),
    (0x080657ec, 0x00001748, 'AVATAR_OF_THE_POT_CID',
     'dispatch_draw_ctr_avatar_pot_cid', None),
    (0x080657f8, 0x00001776, 'CORPSE_OF_YATA_GARASU_CID',
     'dispatch_draw_ctr_yata_garasu_cid', None),
    (0x08065818, 0x00001911, 'CYBER_ARCHFIEND_CID',
     'dispatch_draw_ctr_cyber_archfiend_cid', None),
    (0x08065824, 0x000018f9, 'EHERO_BUBBLEMAN_CID',
     'dispatch_draw_ctr_bubbleman_cid', None),
    (0x0806583c, 0x00001966, 'BROWW_HUNTSMAN_OF_DARK_WORLD_CID',
     'dispatch_draw_ctr_broww_cid', None),
    (0x0806584c, 0x000019c7, 'CHAINSAW_INSECT_CID',
     'dispatch_draw_ctr_chainsaw_insect_cid', None),
    (0x08065cc0, 0x0000165b, 'CONTRACT_WITH_EXODIA_CID',
     'tick_dragon_summon_exodia_cid', None),
    (0x08065b5c, 0x00001572, 'HIDDEN_SOLDIER_CID',
     'tick_dragon_summon_hidden_soldier_cid', None),
    (0x08065b60, 0x000012ca, 'FLUTE_SUMMONING_DRAGON_CID',
     'tick_dragon_summon_flute_cid_a', None),
    (0x08065b6c, 0x0000153b, 'CALL_OF_THE_MUMMY_CID',
     'tick_dragon_summon_call_mummy_cid', None),
    (0x08065b84, 0x00001715, 'ULTRA_EVOLUTION_PILL_CID',
     'tick_dragon_summon_ultra_evol_cid', None),
    (0x08065b98, 0x00001879, 'KING_DRAGUN_CID',
     'tick_dragon_summon_king_dragun_cid', None),
    (0x08065b9c, 0x000019ac, 'MAGNET_CIRCLE_LV2_CID',
     'tick_dragon_summon_magnet_circle_cid', None),
    (0x08066168, 0x000010ef, 'DRAGON_CAPTURE_JAR_CID',
     'drive_equip_slot_bitmap_dcj_cid', None),

    # ---- Group F2: Card IDs -- NEW (17 from card_info.inc additions) ----
    # TIME_WIZARD_CID = 0x0fb6 -- used in Block1 disasm (dispatch table entry CID)
    # Also present as EQ slot in Seg-2 range: DAT_0806572c=0x1662 PRECIOUS_CARDS_FROM_BEYOND_CID
    (0x0806572c, 0x00001662, 'PRECIOUS_CARDS_FROM_BEYOND_CID',
     'dispatch_draw_ctr_precious_cards_cid',
     'PRECIOUS_CARDS_FROM_BEYOND_CID=0x1662; benign collision with CARD_STAT_LP_THRESHOLD_5730(L85)'),
    (0x08065730, 0x00001403, 'CARD_OF_SAFE_RETURN_CID',
     'dispatch_draw_ctr_card_safe_return_cid', None),
    (0x08065734, 0x000011c2, 'SKELENGEL_CID',
     'dispatch_draw_ctr_skelengel_cid', None),
    (0x0806575c, 0x0000139f, 'AIRKNIGHT_PARSHATH_CID',
     'dispatch_draw_ctr_airknight_cid', None),
    (0x080657d8, 0x000016f7, 'MOLTEN_ZOMBIE_CID',
     'dispatch_draw_ctr_molten_zombie_cid_b', None),
    (0x08065a18, 0x000012ca, 'FLUTE_SUMMONING_DRAGON_CID',
     'tick_dragon_summon_flute_cid_b', None),
    (0x08065a1c, 0x000016fd, 'DON_TURTLE_CID',
     'tick_dragon_summon_don_turtle_cid', None),
    (0x080659dc, 0x0000183e, 'SERIAL_SPELL_CID',
     'check_equip_activation_serial_spell_cid', None),

    # ---- Group G: OAM attribute (oam_attr.inc) ----
    (0x08066334, 0x00008027, 'OAM_ATTR_P1_SPRITE',
     'enqueue_slot_player_side_sprite_attr_p1',
     'OAM_ATTR_P1_SPRITE=0x8027: player 1 side sprite attr (0x8000=OBJ pal select; 0x27=tile region)'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label, eol_ascii_or_None)
#    Adds a memory reference from slot to target, sets labels on both.
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # PTR_gP1LifePoints_* x9 -> gP1LifePoints = 0x0201c4e0
    (0x080654b0, 0x0201c4e0, 'gP1LifePoints',
     'write_equip_lp_delta_saturn_lp_base',
     'gP1LifePoints ptr for write_equip_lp_delta_saturn LP base'),
    (0x080655e4, 0x0201c4e0, 'gP1LifePoints',
     'check_lp_side_for_twin_swords_lp_base',
     'gP1LifePoints ptr for check_lp_side_for_twin_swords LP base'),
    (0x08065868, 0x0201c4e0, 'gP1LifePoints',
     'dispatch_draw_ctr_helping_robo_lp_base',
     'gP1LifePoints ptr for dispatch_equip_draw_counter dispatch LP base'),
    (0x08065888, 0x0201c4e0, 'gP1LifePoints',
     'dispatch_draw_ctr_royal_lib_lp_base',
     'gP1LifePoints ptr for dispatch_draw_ctr_royal_lib LP base'),
    (0x0806593c, 0x0201c4e0, 'gP1LifePoints',
     'dispatch_draw_ctr_bubbleman_lp_base',
     'gP1LifePoints ptr for dispatch_draw_ctr_bubbleman LP base'),
    (0x08065b20, 0x0201c4e0, 'gP1LifePoints',
     'tick_dragon_summon_lp_bar_flag_base',
     'gP1LifePoints ptr for tick_dragon_summon LP bar flag path'),
    (0x08065c10, 0x0201c4e0, 'gP1LifePoints',
     'tick_dragon_summon_case7f_lp_base',
     'gP1LifePoints ptr for tick_dragon_summon state_0x7f LP base'),
    (0x08065c48, 0x0201c4e0, 'gP1LifePoints',
     'tick_dragon_summon_case7e_lp_base',
     'gP1LifePoints ptr for tick_dragon_summon state_0x7e LP base'),
    (0x08065cb8, 0x0201c4e0, 'gP1LifePoints',
     'tick_dragon_summon_case7d_lp_base',
     'gP1LifePoints ptr for tick_dragon_summon state_0x7d LP base'),
    # THUMB fn-ptr: check_equip_activation_at_slot11+1 (x2 slots)
    (0x08065c50, 0x08065991, 'check_equip_activation_at_slot11',
     'tick_dragon_summon_case7e_act_cb',
     'THUMB fn-ptr: check_equip_activation_at_slot11+1 = 0x08065991 as activation callback'),
    (0x08065c60, 0x08065991, 'check_equip_activation_at_slot11',
     'tick_dragon_summon_case7e_act_cb2',
     'THUMB fn-ptr: check_equip_activation_at_slot11+1 = 0x08065991 (second copy)'),
    # switchD table pointer
    (0x08065a4c, 0x08065a50, 'switchD_08065a44__switchdataD_08065a50',
     'tick_dragon_summon_state_table',
     'ptr to switchD_08065a44 data table at 0x08065a50 (29 entries, states 0x5f..0x80)'),
    # dispatch_equip_chain_state jump table ptr
    (0x0806622c, 0x08066230, 'dispatch_equip_chain_state_jump_table',
     'dispatch_equip_chain_state_table_ptr',
     'ptr to dispatch_equip_chain_state jump table at 0x08066230 (29 entries)'),
]

# ---------------------------------------------------------------------------
# C. PLATE_REWRITES: (func_addr, old_text, new_text)
#    Replace stale FUN_ references in existing plate comments.
#    All text must be pure ASCII.
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    # 8x FUN_08064880 -> dispatch_equip_lp_delta_by_card_id
    # Note: write_equip_lp_delta_dark_rabbit at 0x08065458 has FUN_08064880
    (0x08065458, 'FUN_08064880', 'dispatch_equip_lp_delta_by_card_id'),
    # write_equip_lp_delta_granadora at 0x08065468
    (0x08065468, 'FUN_08064880', 'dispatch_equip_lp_delta_by_card_id'),
    # write_equip_lp_delta_solar_ray at 0x080654b8
    (0x080654b8, 'FUN_08064880', 'dispatch_equip_lp_delta_by_card_id'),
    # write_equip_lp_delta_marshmallon at 0x080654d8
    (0x080654d8, 'FUN_08064880', 'dispatch_equip_lp_delta_by_card_id'),
    # write_equip_lp_delta_marshmallon: also fix gEquipEffectCtx -> gEquipChainSlotRefs
    (0x080654d8, 'gEquipEffectCtx', 'gEquipChainSlotRefs'),
    # write_equip_lp_delta_atomic_firefly at 0x080654e4
    (0x080654e4, 'FUN_08064880', 'dispatch_equip_lp_delta_by_card_id'),
    # write_equip_lp_delta_greed at 0x080654f8
    (0x080654f8, 'FUN_08064880', 'dispatch_equip_lp_delta_by_card_id'),
    # write_equip_lp_delta_mecha_dog_marron at 0x0806552e
    (0x0806552e, 'FUN_08064880', 'dispatch_equip_lp_delta_by_card_id'),
    # restore_equip_effect_frame at 0x080655da (contains both FUN_08064880 + FUN_080655da)
    (0x080655da, 'FUN_08064880', 'dispatch_equip_lp_delta_by_card_id'),
    (0x080655da, 'FUN_080655da', 'restore_equip_effect_frame'),
    # dispatch_equip_chain_state_by_slot_ownership at 0x080661fc: FUN_080712a0
    (0x080661fc, 'FUN_080712a0', 'dispatch_equip_chain_state_if_tile_count_valid'),
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
    print("=== RefineF08Seg2Slots (DRY=%s) ===" % DRY)
    print("  Seg-2: 0x0806544c..0x08066448")
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

    print("\n=== RefineF08Seg2Slots DONE ===")
    print("  EQ=%d/%d ok  REF=%d  PLATE=%d/%d ok" % (
        eq_ok, len(EQ_SLOTS), ref_ok, plate_ok, len(PLATE_REWRITES)))


main()
