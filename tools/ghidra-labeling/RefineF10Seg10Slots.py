# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF10Seg10Slots.py -- f10 Seg-10 slot symbolization [0x08084318..0x080850d8)
#
# FINAL SEGMENT of file 10 (equip_effect_dispatch).
# Seg-10: 19 named functions, 5 ROM_INCBIN blocks (handled in DisassembleF10Seg10Blocks.py)
# C13=56: EQ=52 + RENAME=4 = 56 total auto-name slots (REF=0)
# FUNC_RENAME=0; PLATE=7 (CJK mojibake -> ASCII); carve=0; disasm=5 blocks
#
# NEW constants added to constants/*.inc BEFORE running this script:
#   card_info.inc:  MOBIUS_THE_FROST_MONARCH_CID=0x17e2, HADE_HANE_CID=0x17ec
#   duel_field.inc: check_equip_slot_eligible_by_card_id_bst_special_cases_fn_ptr=0x080557e1,
#                   check_equip_slot_eligible_by_cross_player_and_field6_zero_fn_ptr=0x080554c5,
#                   check_equip_slot_eligible_by_same_side_and_prereqs_fn_ptr=0x08054899,
#                   check_equip_slot_target_not_blocked_fn_ptr=0x08084a99
#
# REUSE constants verified by value grep:
#   ewram.inc:    gDuelPhaseFlags=0x0201b290, gDuelCardCtxBase=0x0201e2a0,
#                 gEquipChainSlotRefs=0x0201bb90, gDuelFieldSlots=0x0201c510,
#                 gP1LifePoints=0x0201c4e0, PLAYER_BLOCK_STRIDE=0x868,
#                 ELIGIB_SPRITE_CTRL_OFF=0x1d68, ELIGIB_ANIM_STATE_OFF=0x1d6c,
#                 LP_CARD_TRACK_BASE_OFF=0x1da8, LP_CARD_TRACK_NEXT_OFF=0x1daa,
#                 gP1HandSlotArray=0x0201c8f8
#   duel_field.inc: DUAL_LABEL_RENDER_STATE_CLEAR=0xfffc7fff (duel_field.inc:134),
#                   set_equip_activation_state_by_mode_alt_fn_ptr=0x080905e9 (duel_field.inc:451),
#                   lookup_equip_score_mooyan_p1=0x199 (duel_field.inc:323)
#   card_info.inc:  DNA_TRANSPLANT_CID=0x171f (card_info.inc:395),
#                   DNA_SURGERY_CID=0x1357 (card_info.inc:391),
#                   SERIAL_SPELL_CID=0x183e (card_info.inc:997),
#                   POLYMERIZATION_CID=0x12e5 (card_info.inc:436),
#                   HYDROGEDDON_CID=0x194f (card_info.inc:943),
#                   OXYGEDDON_CID=0x1950 (card_info.inc:944),
#                   OJAMA_KING_CARD_ID=0x17ee (card_info.inc:120)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK). Ghidra Jython mojibake prevention.
# NOTE: PLATE WARN=FAIL: if setComment fails, report FAIL.
# NOTE: RENAME_SLOTS include 3 ROM_INCBIN base labels + 1 PTR_gP1LifePoints_ -- disasm script handles BLK labeling after clearListing

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
#    52 total EQ slots (all ROM values verified)
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # ===== REUSE: gDuelPhaseFlags=0x0201b290 (ewram.inc) x14 =====
    (0x08084334, 0x0201b290, 'gDuelPhaseFlags',
     'duel_phase_flags_08084334', None),
    (0x080843c4, 0x0201b290, 'gDuelPhaseFlags',
     'duel_phase_flags_080843c4', None),
    (0x08084498, 0x0201b290, 'gDuelPhaseFlags',
     'duel_phase_flags_08084498', None),
    (0x080845fc, 0x0201b290, 'gDuelPhaseFlags',
     'duel_phase_flags_080845fc', None),
    (0x0808469c, 0x0201b290, 'gDuelPhaseFlags',
     'duel_phase_flags_0808469c', None),
    (0x08084c5c, 0x0201b290, 'gDuelPhaseFlags',
     'duel_phase_flags_08084c5c', None),
    (0x08084d78, 0x0201b290, 'gDuelPhaseFlags',
     'duel_phase_flags_08084d78', None),
    (0x08084e08, 0x0201b290, 'gDuelPhaseFlags',
     'duel_phase_flags_08084e08', None),
    (0x08084e20, 0x0201b290, 'gDuelPhaseFlags',
     'duel_phase_flags_08084e20', None),
    (0x08084e90, 0x0201b290, 'gDuelPhaseFlags',
     'duel_phase_flags_08084e90', None),
    (0x08084f5c, 0x0201b290, 'gDuelPhaseFlags',
     'duel_phase_flags_08084f5c', None),
    (0x08085028, 0x0201b290, 'gDuelPhaseFlags',
     'duel_phase_flags_08085028', None),

    # ===== REUSE: gDuelCardCtxBase=0x0201e2a0 (ewram.inc) x2 =====
    (0x08084364, 0x0201e2a0, 'gDuelCardCtxBase',
     'duel_card_ctx_base_08084364', None),
    (0x080844d8, 0x0201e2a0, 'gDuelCardCtxBase',
     'duel_card_ctx_base_080844d8', None),

    # ===== REUSE: gEquipChainSlotRefs=0x0201bb90 (ewram.inc) x1 =====
    (0x08084368, 0x0201bb90, 'gEquipChainSlotRefs',
     'equip_chain_slot_refs_08084368', None),

    # ===== REUSE: gP1LifePoints=0x0201c4e0 (ewram.inc) x10 =====
    (0x0808436c, 0x0201c4e0, 'gP1LifePoints',
     'gp1_life_points_ptr_0808436c', None),
    (0x08084390, 0x0201c4e0, 'gP1LifePoints',
     'gp1_life_points_ptr_08084390', None),
    (0x080843f8, 0x0201c4e0, 'gP1LifePoints',
     'gp1_life_points_ptr_080843f8', None),
    (0x08084668, 0x0201c4e0, 'gP1LifePoints',
     'gp1_life_points_ptr_08084668', None),
    (0x08084c94, 0x0201c4e0, 'gP1LifePoints',
     'gp1_life_points_ptr_08084c94', None),
    (0x08084cd8, 0x0201c4e0, 'gP1LifePoints',
     'gp1_life_points_ptr_08084cd8', None),
    (0x08084e00, 0x0201c4e0, 'gP1LifePoints',
     'gp1_life_points_ptr_08084e00', None),
    (0x08084ff4, 0x0201c4e0, 'gP1LifePoints',
     'gp1_life_points_ptr_08084ff4', None),

    # ===== REUSE: PLAYER_BLOCK_STRIDE=0x868 (ewram.inc) x4 =====
    (0x08084394, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_08084394', None),
    (0x08084534, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_08084534', None),
    (0x08084730, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_08084730', None),
    (0x08084f38, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_08084f38', None),

    # ===== REUSE: gDuelFieldSlots=0x0201c510 (ewram.inc) x2 =====
    (0x08084538, 0x0201c510, 'gDuelFieldSlots',
     'duel_field_slots_08084538', None),
    (0x08084734, 0x0201c510, 'gDuelFieldSlots',
     'duel_field_slots_08084734', None),

    # ===== REUSE: lookup_equip_score_mooyan_p1=0x199 (duel_field.inc:323) x1 =====
    (0x080843c0, 0x00000199, 'lookup_equip_score_mooyan_p1',
     'lookup_equip_score_mooyan_p1_080843c0',
     'r2 arg to lookup_equip_score (Mooyan Curry P1 score mode 0x199)'),

    # ===== REUSE: set_equip_activation_state_by_mode_alt_fn_ptr=0x080905e9 (duel_field.inc:451) x1 =====
    (0x0808453c, 0x080905e9, 'set_equip_activation_state_by_mode_alt_fn_ptr',
     'set_equip_act_alt_fn_ptr_0808453c',
     'THUMB+1 fn-ptr to set_equip_activation_state_by_mode_alt (0x080905e8); REUSE duel_field.inc'),

    # ===== REUSE: ELIGIB_SPRITE_CTRL_OFF=0x1d68 (ewram.inc) x3 =====
    (0x0808456c, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF',
     'eligib_sprite_ctrl_off_0808456c', None),
    (0x08084e04, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF',
     'eligib_sprite_ctrl_off_08084e04', None),
    (0x08084ff8, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF',
     'eligib_sprite_ctrl_off_08084ff8', None),

    # ===== REUSE: ELIGIB_ANIM_STATE_OFF=0x1d6c (ewram.inc) x2 =====
    (0x08084570, 0x00001d6c, 'ELIGIB_ANIM_STATE_OFF',
     'eligib_anim_state_off_08084570', None),
    (0x08084ffc, 0x00001d6c, 'ELIGIB_ANIM_STATE_OFF',
     'eligib_anim_state_off_08084ffc', None),

    # ===== REUSE: DUAL_LABEL_RENDER_STATE_CLEAR=0xfffc7fff (duel_field.inc:134) x2 =====
    (0x08084624, 0xfffc7fff, 'DUAL_LABEL_RENDER_STATE_CLEAR',
     'dual_label_render_state_clear_08084624',
     'AND mask clears bits[17:15] of effect node attr (REUSE duel_field.inc:134)'),
    (0x08084f9c, 0xfffc7fff, 'DUAL_LABEL_RENDER_STATE_CLEAR',
     'dual_label_render_state_clear_08084f9c', None),

    # ===== REUSE: LP_CARD_TRACK_NEXT_OFF=0x1daa (ewram.inc) x2 =====
    (0x0808466c, 0x00001daa, 'LP_CARD_TRACK_NEXT_OFF',
     'lp_card_track_next_off_0808466c',
     'gP1LifePoints+LP_CARD_TRACK_NEXT_OFF: LP card-track next halfword'),
    (0x08084c98, 0x00001daa, 'LP_CARD_TRACK_NEXT_OFF',
     'lp_card_track_next_off_08084c98', None),

    # ===== REUSE: DNA_TRANSPLANT_CID=0x171f (card_info.inc:395) x2 =====
    (0x08084670, 0x0000171f, 'DNA_TRANSPLANT_CID',
     'dna_transplant_cid_08084670',
     'LP sentinel: DNA Transplant CID (value match; REUSE card_info.inc:395)'),
    (0x08084c9c, 0x0000171f, 'DNA_TRANSPLANT_CID',
     'dna_transplant_cid_08084c9c', None),

    # ===== REUSE: LP_CARD_TRACK_BASE_OFF=0x1da8 (ewram.inc) x1 =====
    (0x08084cdc, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF',
     'lp_card_track_base_off_08084cdc',
     'gP1LifePoints+LP_CARD_TRACK_BASE_OFF: LP card-ref tracking base'),

    # ===== REUSE: DNA_SURGERY_CID=0x1357 (card_info.inc:391) x1 =====
    (0x08084ce0, 0x00001357, 'DNA_SURGERY_CID',
     'dna_surgery_cid_08084ce0',
     'LP sentinel2 in advance_equip_lp_value_display_seq (DNA Surgery CID; card_info.inc:391)'),

    # ===== REUSE: SERIAL_SPELL_CID=0x183e (card_info.inc:997) x1 =====
    (0x08084d04, 0x0000183e, 'SERIAL_SPELL_CID',
     'serial_spell_cid_08084d04',
     'invoke_effect_action_with_temp_card_id: restores card_id to SERIAL_SPELL_CID after temp override'),

    # ===== NEW: check_equip_slot_eligible_by_card_id_bst_special_cases_fn_ptr=0x080557e1 (duel_field.inc) x1 =====
    (0x08084da0, 0x080557e1, 'check_equip_slot_eligible_by_card_id_bst_special_cases_fn_ptr',
     'eligib_card_id_bst_special_fn_ptr_08084da0',
     'THUMB+1 fn-ptr to check_equip_slot_eligible_by_card_id_bst_special_cases (0x080557e0); state=0 mode_a'),

    # ===== NEW: check_equip_slot_eligible_by_cross_player_and_field6_zero_fn_ptr=0x080554c5 (duel_field.inc) x1 =====
    (0x08084dc8, 0x080554c5, 'check_equip_slot_eligible_by_cross_player_and_field6_zero_fn_ptr',
     'eligib_cross_player_field6_zero_fn_ptr_08084dc8',
     'THUMB+1 fn-ptr to check_equip_slot_eligible_by_cross_player_and_field6_zero (0x080554c4); state=2 mode_b'),

    # ===== REUSE: POLYMERIZATION_CID=0x12e5 (card_info.inc:436) x1 =====
    (0x08084f34, 0x000012e5, 'POLYMERIZATION_CID',
     'polymerization_cid_08084f34',
     'tick_equip_polymerization_display_3state: finds deck slot by card pair match with Polymerization'),

    # ===== REUSE: gP1HandSlotArray=0x0201c8f8 (ewram.inc) x1 =====
    (0x08084f3c, 0x0201c8f8, 'gP1HandSlotArray',
     'gp1_hand_slot_array_08084f3c',
     'tick_equip_polymerization_display_3state state=2: reads monster slot entry from P1 hand array'),

    # ===== NEW: check_equip_slot_eligible_by_same_side_and_prereqs_fn_ptr=0x08054899 (duel_field.inc) x1 =====
    (0x08084fc8, 0x08054899, 'check_equip_slot_eligible_by_same_side_and_prereqs_fn_ptr',
     'eligib_same_side_prereqs_fn_ptr_08084fc8',
     'THUMB+1 fn-ptr to check_equip_slot_eligible_by_same_side_and_prereqs (0x08054898); state=2 dispatch'),

    # ===== REUSE: HYDROGEDDON_CID=0x194f (card_info.inc:943) x1 =====
    (0x080850d0, 0x0000194f, 'HYDROGEDDON_CID',
     'hydrogeddon_cid_080850d0',
     'dispatch_equip_effect_for_hydrogeddon_pair: first dispatch_effect_handler_by_card_id call'),

    # ===== REUSE: OXYGEDDON_CID=0x1950 (card_info.inc:944) x1 =====
    (0x080850d4, 0x00001950, 'OXYGEDDON_CID',
     'oxygeddon_cid_080850d4',
     'dispatch_equip_effect_for_hydrogeddon_pair: second dispatch_effect_handler_by_card_id call'),
]

# ---------------------------------------------------------------------------
# B. RENAME_SLOTS: (slot_addr, new_label, eol_ascii_or_None)
#    4 slots: 1 PTR_gP1LifePoints_ + 3 ROM_INCBIN base labels
#    NOTE: The 3 ROM_INCBIN base labels (0x08084790/0x08084918/0x08084b34) are renamed
#    here for USER labeling; disasm script will add createFunction at the actual fn entries.
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x08084568, 'gp1_lp_ptr_08084568',
     'gP1LifePoints pool (tick_equip_display_with_target_selection state=3)'),
    (0x08084790, 'mobius_dispatch_state_stubs',
     'Mobius the Frost Monarch (CID=0x17e2) state dispatch sub-stubs (BLK2)'),
    (0x08084918, 'hade_hane_dispatch_state_stubs',
     'Hade-Hane (CID=0x17ec) state dispatch sub-stubs (BLK3)'),
    (0x08084b34, 'ojama_king_dispatch_state_stubs',
     'Ojama King (CID=0x17ee) state dispatch sub-stubs (BLK5)'),
]

# ---------------------------------------------------------------------------
# C. PLATE_REWRITES: (func_addr, new_plate_text)
#    7 functions with CJK mojibake plates -> full ASCII rewrite
#    All plate text is pure ASCII. PLATE WARN=FAIL.
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    # 1. dispatch_equip_display_by_activity_if_slot_group_le4 (0x080843fc)
    (0x080843fc,
     "@ Equip display activity gate: reads card_slot[+2] bits[6:2] as slot_group (5-bit via lsls#0x1a;lsrs#0x1b);\n"
     "@ if slot_group > 4 returns 1 (skip); else calls dispatch_equip_display_by_type_flag_and_node_activity\n"
     "@ and passes through return value. Runtime fn-ptr dispatch (indeg=0 Sub-type A)."),

    # 2. tick_equip_display_with_target_selection (0x08084460)
    (0x08084460,
     "@ Equip confirm target selection display state machine. indeg=0, fn-ptr driven.\n"
     "@ Reads card_slot[+0xc] confirm_state: state==2 calls dispatch_equip_activation_display_by_confirm_state.\n"
     "@ state==1/3: reads gDuelCtx+0x4b0 sub-state; sub-state 0/1 sets [+0xc] and calls dispatch;\n"
     "@ if confirm_flag==1 calls select_equip_target_slot_by_effect_strategy;\n"
     "@ else card_name_lookup+format_text+trigger_op31+set_activation_mode;\n"
     "@ sub-state 2 confirms then select_equip_target_slot;\n"
     "@ sub-state 3 check_confirmed -> enqueue_equip_slot_sprite_with_code_rotation."),

    # 3. dispatch_equip_display_if_confirm_state_nonzero (0x08084594)
    (0x08084594,
     "@ Equip activation confirm nonzero gate dispatcher. Reads card_slot[+0xc] halfword;\n"
     "@ if 0 returns 1 (skip); else calls dispatch_equip_activation_display_by_confirm_state\n"
     "@ and passes through return value.\n"
     "@ Sibling of dispatch_equip_display_if_confirm_state_one/two (0x080833a8/0x0808416c);\n"
     "@ this variant triggers on any nonzero confirm state."),

    # 4. scan_equip_target_slots_for_sprites (0x08084674)
    (0x08084674,
     "@ Equip target slot sprite scan enqueue function. indeg=0, fn-ptr driven.\n"
     "@ Reads gDuelCtx+0x4b0: if !=0xa first calls dispatch_equip_display_by_type_flag_and_node_activity;\n"
     "@ on nonzero result writes state:=0xa.\n"
     "@ Sub-state 0xa: read_effect_slot_side_and_type gets type_nibble; loops slot 0..4 reading\n"
     "@ gDuelFieldSlots[slot*0x14+player*0x868] card_id; filters via check_card_field8_is_9\n"
     "@ /check_slot_card_is_monster_type/query_slot_card_type_eligibility;\n"
     "@ on pass calls submit_equip_sprite_if_slot_eligible, increments count.\n"
     "@ After loop calls enqueue_sprite_attr_with_xy_split(player,slot_group,count)."),

    # 5. dispatch_equip_display_if_monster_slot_and_activation (0x08084d08)
    (0x08084d08,
     "@ Equip activation display double-precondition gate dispatcher.\n"
     "@ Extracts player_id from card_slot[+2] bit0;\n"
     "@ calls find_first_available_monster_slot_for_player(player_id) -- returns -1 if none available.\n"
     "@ Then calls count_effect_node_zone_activations(card_slot) -- returns -1 if zero.\n"
     "@ Both preconditions satisfied: calls dispatch_equip_activation_display_by_confirm_state\n"
     "@ and passes through return value."),

    # 6. dispatch_equip_display_unless_type_code_80 (0x08084d3c)
    (0x08084d3c,
     "@ Equip display type-code 0x80 exclusion gate dispatcher.\n"
     "@ Reads card_slot[+2] bits[11:2] (mask 0xfc0); if ==0x80 returns 1 (skip;\n"
     "@ type_code 0x80 handled by separate path);\n"
     "@ else calls dispatch_equip_display_by_type_flag_and_node_activity\n"
     "@ and passes through return value."),

    # 7. dispatch_equip_display_by_ext_field6_type (0x08084e2c)
    (0x08084e2c,
     "@ Equip display routing by extended stat field6 type.\n"
     "@ Reads card_slot[+0x14] pointer; calls get_card_extended_stat_field6 for ext_field6 value.\n"
     "@ If ext_field6==0x16 returns 1 (skip; handled by other path).\n"
     "@ If ext_field6==0x17 calls dispatch_equip_activation_display_by_confirm_state and passes through.\n"
     "@ Else: calls dispatch_effect_for_neo_daedalus_eligible_slot;\n"
     "@ if returns 0 returns 1; else calls tick_equip_slot_display_by_card_id_3state and passes through."),
]

# ---------------------------------------------------------------------------
# Helper: verify slot value against ROM
# ---------------------------------------------------------------------------
def _check(addr, expected_val):
    mem = currentProgram.getMemory()
    try:
        actual = mem.getInt(toAddr(addr)) & 0xFFFFFFFF
        if actual != (expected_val & 0xFFFFFFFF):
            print("FAIL value check @0x{:08x}: expected=0x{:08x} actual=0x{:08x}".format(
                addr, expected_val & 0xFFFFFFFF, actual))
            return False
    except Exception as e:
        print("FAIL read @0x{:08x}: {}".format(addr, e))
        return False
    return True

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    sym_table = currentProgram.getSymbolTable()
    eq_table = currentProgram.getEquateTable()
    listing = currentProgram.getListing()

    ok_eq = 0; fail_eq = 0
    ok_rename = 0; fail_rename = 0
    ok_plate = 0; fail_plate = 0

    # ---- A. EQ_SLOTS ----
    seen_addrs = set()
    for (slot_addr, val, eq_name, slot_label, eol) in EQ_SLOTS:
        if slot_addr in seen_addrs:
            print("SKIP dup EQ addr 0x{:08x}".format(slot_addr))
            continue
        seen_addrs.add(slot_addr)
        if not _check(slot_addr, val):
            fail_eq += 1
            continue
        if DRY:
            print("DRY EQ 0x{:08x} = {} ({})".format(slot_addr, eq_name, slot_label))
            ok_eq += 1
            continue
        try:
            # create/get equate
            eq = eq_table.getEquate(eq_name)
            if eq is None:
                eq = eq_table.createEquate(eq_name, val & 0xFFFFFFFF)
            eq.addReference(toAddr(slot_addr), 0)
            # create USER label at slot
            sym_table.createLabel(toAddr(slot_addr), slot_label, SourceType.USER_DEFINED)
            # set primary
            for s in sym_table.getSymbols(toAddr(slot_addr)):
                if s.getName() == slot_label:
                    s.setPrimary()
                    break
            # set EOL comment
            if eol:
                cu = listing.getCodeUnitAt(toAddr(slot_addr))
                if cu:
                    cu.setComment(CodeUnit.EOL_COMMENT, eol)
            ok_eq += 1
        except Exception as e:
            print("FAIL EQ 0x{:08x} {}: {}".format(slot_addr, eq_name, e))
            fail_eq += 1

    # ---- B. RENAME_SLOTS ----
    for (slot_addr, new_label, eol) in RENAME_SLOTS:
        if DRY:
            print("DRY RENAME 0x{:08x} -> {}".format(slot_addr, new_label))
            ok_rename += 1
            continue
        try:
            sym_table.createLabel(toAddr(slot_addr), new_label, SourceType.USER_DEFINED)
            for s in sym_table.getSymbols(toAddr(slot_addr)):
                if s.getName() == new_label:
                    s.setPrimary()
                    break
            if eol:
                cu = listing.getCodeUnitAt(toAddr(slot_addr))
                if cu:
                    cu.setComment(CodeUnit.EOL_COMMENT, eol)
            ok_rename += 1
        except Exception as e:
            print("FAIL RENAME 0x{:08x}: {}".format(slot_addr, e))
            fail_rename += 1

    # ---- C. PLATE_REWRITES ----
    for (fn_addr, plate_text) in PLATE_REWRITES:
        if DRY:
            print("DRY PLATE 0x{:08x}".format(fn_addr))
            ok_plate += 1
            continue
        try:
            cu = listing.getCodeUnitAt(toAddr(fn_addr))
            if cu is None:
                print("FAIL PLATE 0x{:08x}: no code unit (WARN=FAIL)".format(fn_addr))
                fail_plate += 1
                continue
            cu.setComment(CodeUnit.PLATE_COMMENT, plate_text)
            ok_plate += 1
        except Exception as e:
            print("FAIL PLATE 0x{:08x}: {} (WARN=FAIL)".format(fn_addr, e))
            fail_plate += 1

    print("")
    print("=== RefineF10Seg10Slots DONE ===")
    print("EQ: {}/{} OK  RENAME: {}/{} OK  PLATE: {}/{} OK".format(
        ok_eq, ok_eq + fail_eq,
        ok_rename, ok_rename + fail_rename,
        ok_plate, ok_plate + fail_plate))
    print("FAIL total: {}".format(fail_eq + fail_rename + fail_plate))

main()
