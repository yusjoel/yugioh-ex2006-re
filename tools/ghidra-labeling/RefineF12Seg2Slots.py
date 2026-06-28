# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF12Seg2Slots.py -- file 12 Seg-2 [0x08094f20, 0x08095ba8)
#   asm/12_equip_activation_scan.s slot symbolization
#   15 named functions, 2 ROM_INCBIN blocks (0x95274/0xc0 R4 disasm, 0x95b28/0x14 orphan)
#
# Sections:
#   A. EQ_SLOTS   -- data-equate (109 slots: 99 DAT_ + 10 DWORD_)
#   B. REF_SLOTS  -- USER label on target + DATA ref + slot rename (2 slots)
#   C. RENAME_SLOTS -- PTR_gP1LifePoints_* + DWORD_ -> snake_case (20 slots: 12 gP1LP + 7 DWORD_off)
#   D. PLATE_REWRITES -- 6 stale FUN_ plate repairs (substring replace, pure ASCII)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK -- Jython UTF-8 mojibake risk).
# Block1 (0x08095274) R4 disasm is handled in DisassembleF12Seg2Block1.py.
# Block2 (0x08095b28) is 0-ref orphan THUMB code -> section 5.1 only, NOT disassembled here.

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
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # --- gDuelCardCtxBase (ewram.inc:218, 0x0201e2a0) -- 7 slots ---
    (0x0809501c, 0x0201e2a0, 'gDuelCardCtxBase',
     'gduecardctx_9501c',
     'update_card_display_index_by_type_rules: ldr r5,[r1,#4]=player_id check'),
    (0x08095188, 0x0201e2a0, 'gDuelCardCtxBase',
     'gduecardctx_95188',
     'write_monster_zone_display_indices: ldr r2,[r7,#4]=player_id'),
    (0x0809560c, 0x0201e2a0, 'gDuelCardCtxBase',
     'gduecardctx_9560c',
     'step_prng_anim_frame caseD_2: [+4]=player_id for slot index lookup'),
    (0x0809577c, 0x0201e2a0, 'gDuelCardCtxBase',
     'gduecardctx_9577c',
     'step_prng_anim_frame caseD_e: ldr r0,[r0,#4]=current_player_id for XOR'),
    (0x08095870, 0x0201e2a0, 'gDuelCardCtxBase',
     'gduecardctx_95870',
     'step_prng_anim_frame caseD_11: [+4] player_id XOR'),
    (0x0809589c, 0x0201e2a0, 'gDuelCardCtxBase',
     'gduecardctx_9589c',
     'step_prng_anim_frame caseD_1e: [+4]=player_id arg to setup_lp_display_row_with_data'),
    (0x08095ba4, 0x0201e2a0, 'gDuelCardCtxBase',
     'gduecardctx_95ba4',
     'check_player_side_condition: [+4]=player_id for XOR'),

    # --- NEGATE_ATTACK_CID (card_info.inc NEW, 0x000012c4) -- 1 slot ---
    (0x08095020, 0x000012c4, 'NEGATE_ATTACK_CID',
     'negate_atk_cid_95020',
     'update_card_display_index_by_type_rules: cmp r2,r0 when card_id==0x12c4 (Negate Attack) XOR player_side'),

    # --- P1LP_BLOCK2_OFF_1CE8 (ewram.inc:276, 0x00001ce8) -- 3 slots ---
    (0x08095028, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',
     'p1lp_blk2_95028',
     'update_card_display_index_by_type_rules: [gP1LifePoints+0x1ce8] player_raw XOR for Negate Attack check'),
    (0x08095080, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',
     'p1lp_blk2_95080',
     'update_card_display_index_by_type_rules field6==0x16 path: player XOR check'),
    (0x08095ba0, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',
     'p1lp_blk2_95ba0',
     'check_player_side_condition: [gP1LifePoints+0x1ce8] player_id XOR check'),

    # --- PLAYER_BLOCK_STRIDE (ewram.inc:251, 0x00000868) -- 1 slot ---
    (0x0809518c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_9518c',
     'write_monster_zone_display_indices: muls r0,r1 player offset'),

    # --- gDuelFieldSlots (ewram.inc:314, 0x0201c510) -- 1 slot ---
    (0x08095190, 0x0201c510, 'gDuelFieldSlots',
     'gduelfieldslots_95190',
     'write_monster_zone_display_indices: ldr base for slot scan [+0]=slot_field5'),

    # --- ACTIVATION_STATE_C_OFF (duel_field.inc:220, 0x00001d4c) -- 1 slot ---
    (0x08095208, 0x00001d4c, 'ACTIVATION_STATE_C_OFF',
     'act_state_c_95208',
     'play_equip_ui_effect_3_with_state_gate: [gP1LifePoints+0x1d4c] equip slot status; ldr then cmp!=0'),

    # --- LP_EQUIP_STATE_B_OFF (ewram.inc NEW, 0x00001d50) -- 2 slots ---
    (0x0809520c, 0x00001d50, 'LP_EQUIP_STATE_B_OFF',
     'lp_equip_b_9520c',
     'play_equip_ui_effect_3_with_state_gate: [gP1LifePoints+0x1d50] secondary equip state; cmp==0 then set:=1'),
    (0x0809521c, 0x00001d50, 'LP_EQUIP_STATE_B_OFF',
     'lp_equip_b_9521c',
     'play_equip_ui_effect_3_with_state_gate LAB_08095210: str r1,[r0] r1=0 -> clear [+0x1d50]'),

    # --- ELIGIB_ACT_TYPE_OFF (ewram.inc:421, 0x00001d5c) -- 1 slot ---
    (0x08095244, 0x00001d5c, 'ELIGIB_ACT_TYPE_OFF',
     'eligib_act_type_95244',
     'dispatch_equip_confirm_phase_by_step: [gP1LifePoints+0x1d5c] step value; subs#1; cmp#9; bls dispatch'),

    # --- ELIGIB_STATE_CTRL_OFF (ewram.inc:419, 0x00001d54) -- 2 slots ---
    (0x08095344, 0x00001d54, 'ELIGIB_STATE_CTRL_OFF',
     'eligib_state_ctrl_95344',
     'dispatch_equip_confirm_phase_by_step LAB_08095334: str 0 to [+0x1d54] when step out of range'),
    (0x0809537c, 0x00001d54, 'ELIGIB_STATE_CTRL_OFF',
     'eligib_state_ctrl_9537c',
     'tick_equip_confirm_slot_by_step: [gP1LifePoints+0x1d54] check after step; if==0 clears [+0x1d58]'),

    # --- ELIGIB_ACT_COUNT_OFF (ewram.inc:420, 0x00001d58) -- 1 slot ---
    (0x08095360, 0x00001d58, 'ELIGIB_ACT_COUNT_OFF',
     'eligib_act_cnt_95360',
     'tick_equip_confirm_slot_by_step: [gP1LifePoints+0x1d58] confirm pending flag; cmp==0 -> return 0'),

    # --- SPRITE_HIGH_HALF_MASK (duel_field.inc NEW, 0xffff0000) -- 1 slot ---
    # Domain-distinct from EQUIP_CHAIN_SENTINEL=0xffff0000 (list terminator; different use)
    (0x080953bc, 0xffff0000, 'SPRITE_HIGH_HALF_MASK',
     'sprite_hi_mask_953bc',
     'pack_sprite_row_attr_words: ands r1,r4 clears low 16 bits of sprite attr word before OR y-coord'),

    # --- SPRITE_LOW_HALF_MASK (duel_field.inc NEW, 0x0000ffff) -- 1 slot ---
    # Domain-distinct from SLOT_CARD_EMPTY/UNINIT_GUARD_FFFF etc (6 existing hits, all different domain)
    (0x080953c0, 0x0000ffff, 'SPRITE_LOW_HALF_MASK',
     'sprite_lo_mask_953c0',
     'pack_sprite_row_attr_words: ands r1,r5 clears high 16 bits of sprite attr word'),

    # --- SPRITE_ROW_DISPATCH_TABLE (duel_field.inc NEW, 0x080953dc) -- 1 slot ---
    (0x080953d8, 0x080953dc, 'SPRITE_ROW_DISPATCH_TABLE',
     'sprite_row_tbl_953d8',
     'dispatch_sprite_row_write_by_type: 30-entry switch table (2 targets: 0x08095454/0x0809548e)'),

    # --- gSpriteAttrBuf (ewram.inc:378, 0x0201b870) -- 21 slots ---
    (0x0809546c, 0x0201b870, 'gSpriteAttrBuf',
     'gsprattrb_9546c',
     'dispatch_sprite_row_write_by_type caseD_2 r2!=0: adds r2,r2,r0 r0=0xc0<<2=0x300 stride'),
    (0x08095490, 0x0201b870, 'gSpriteAttrBuf',
     'gsprattrb_95490',
     'dispatch_sprite_row_write_by_type caseD_2 r2==0 path LAB_08095470'),
    (0x08095528, 0x0201b870, 'gSpriteAttrBuf',
     'gsprattrb_95528',
     'step_prng_anim_frame: base for busy_flag [+0xc0*4=0x300]'),
    (0x08095608, 0x0201b870, 'gSpriteAttrBuf',
     'gsprattrb_95608',
     'step_prng_anim_frame caseD_2: [gSpriteAttrBuf+0x300] busy byte ORed with 1'),
    (0x0809561c, 0x0201b870, 'gSpriteAttrBuf',
     'gsprattrb_9561c',
     'step_prng_anim_frame caseD_3: adds base+0xc0*4 then ORs bit0'),
    (0x08095674, 0x0201b870, 'gSpriteAttrBuf',
     'gsprattrb_95674',
     'step_prng_anim_frame caseD_9: ldrh r0[2]/r3[6]/r2[4] sprite row fields'),
    (0x0809568c, 0x0201b870, 'gSpriteAttrBuf',
     'gsprattrb_9568c',
     'step_prng_anim_frame caseD_a: ldrh r0,[r0,#2] sprite type field'),
    (0x08095714, 0x0201b870, 'gSpriteAttrBuf',
     'gsprattrb_95714',
     'step_prng_anim_frame caseD_c: ORs 0x10 into [gSpriteAttrBuf+0x300]'),
    (0x08095738, 0x0201b870, 'gSpriteAttrBuf',
     'gsprattrb_95738',
     'step_prng_anim_frame caseD_d: ORs 0x20 into [gSpriteAttrBuf+0x300]'),
    (0x080957a0, 0x0201b870, 'gSpriteAttrBuf',
     'gsprattrb_957a0',
     'step_prng_anim_frame caseD_12: ldrh r5,[r1,#2]; lsls r0,r5,#1; adds; lsls,#3 -> sprite offset'),
    (0x080957bc, 0x0201b870, 'gSpriteAttrBuf',
     'gsprattrb_957bc',
     'step_prng_anim_frame caseD_13: ldrh r1,[r1,#2]'),
    (0x080957dc, 0x0201b870, 'gSpriteAttrBuf',
     'gsprattrb_957dc',
     'step_prng_anim_frame caseD_14: ldrh fields for submit_slot_card_sprite_row_entry'),
    (0x08095818, 0x0201b870, 'gSpriteAttrBuf',
     'gsprattrb_95818',
     'step_prng_anim_frame caseD_f: ldrh r0,[r2,#2] source sprite_id'),
    (0x0809582c, 0x0201b870, 'gSpriteAttrBuf',
     'gsprattrb_9582c',
     'step_prng_anim_frame caseD_10: adds r1,r1,r5 r5=0x300; ORs 0x20'),
    (0x080958a0, 0x0201b870, 'gSpriteAttrBuf',
     'gsprattrb_958a0',
     'step_prng_anim_frame caseD_1e: ldrh r1,[r2,#2]; adds r2,#4 source for setup_lp_display_row_with_data'),
    (0x08095904, 0x0201b870, 'gSpriteAttrBuf',
     'gsprattrb_95904',
     'step_prng_anim_frame caseD_1c: base [+2] ldrh as sprite_id; [+0xc4*4] store; [+0x301] OR 0x10'),
    (0x08095938, 0x0201b870, 'gSpriteAttrBuf',
     'gsprattrb_95938',
     'step_prng_anim_frame caseD_1d: adds r2,r1,r3 r3=0x301 -> [+0x301] ORed 0x20'),
    (0x0809597c, 0x0201b870, 'gSpriteAttrBuf',
     'gsprattrb_9597c',
     'step_prng_anim_frame caseD_1a: [+2] ldrh; [+0xc4*4]=sprite_id; copy to gEffectEntryArray; [+0x30e] strb 0'),
    (0x080959bc, 0x0201b870, 'gSpriteAttrBuf',
     'gsprattrb_959bc',
     'step_prng_anim_frame caseD_1b: [+0x301] ORed 0x8; [gDuelPhaseFlags+0x494] stride'),
    (0x08095a38, 0x0201b870, 'gSpriteAttrBuf',
     'gsprattrb_95a38',
     'step_prng_anim_frame caseD_18: entry fields; [+0xc4*4]=sprite_id; copy to gEffectEntryArray+stride'),
    (0x08095a5c, 0x0201b870, 'gSpriteAttrBuf',
     'gsprattrb_95a5c',
     'step_prng_anim_frame LAB_08095a48: [+0x30f]:=0; [+0x301] ORed 0x40'),
    (0x08095aec, 0x0201b870, 'gSpriteAttrBuf',
     'gsprattrb_95aec',
     'step_prng_anim_frame caseD_8: adds r1,r1,r5 r5=0x300; ORs 0x8 into [+0x300]'),
    (0x08095ad4, 0x0201b870, 'gSpriteAttrBuf',
     'gsprattrb_95ad4',
     'step_prng_anim_frame caseD_7: ldrh r0[2]/r1[4]/r2[6]/r3[8] -> write_sprite_attr_record_entry args'),
    (0x08095b94, 0x0201b870, 'gSpriteAttrBuf',
     'gsprattrb_95b94',
     'check_player_side_condition: [+0xc0*4=0x300] ldr r0; lsls#0xd; asrs r3,r0,#0x1c -> bits[18:15]'),

    # --- gSpriteAttrBufData (ewram.inc NEW, 0x0201b872) -- 7 slots ---
    (0x08095638, 0x0201b872, 'gSpriteAttrBufData',
     'gsprattrb_p2_95638',
     'step_prng_anim_frame caseD_15: dst = gSpriteAttrBuf+2 for copy_bytes_by_halfword 0x18'),
    (0x08095648, 0x0201b872, 'gSpriteAttrBufData',
     'gsprattrb_p2_95648',
     'step_prng_anim_frame caseD_16: same copy dst LAB_080959b2'),
    (0x08095718, 0x0201b872, 'gSpriteAttrBufData',
     'gsprattrb_p2_95718',
     'step_prng_anim_frame caseD_b: ldrh r4,[r2,#0] source halfword'),
    (0x08095770, 0x0201b872, 'gSpriteAttrBufData',
     'gsprattrb_p2_95770',
     'step_prng_anim_frame caseD_e: ldrh r0[0]/r1[2]/r2[4] entry fields; r4=gSpriteAttrBuf+2'),
    (0x08095864, 0x0201b872, 'gSpriteAttrBufData',
     'gsprattrb_p2_95864',
     'step_prng_anim_frame caseD_11: ldrh r0[0]/r1[2]/r2[4] entry; init_duel_zone_target_slot_refs args'),
    (0x080958c8, 0x0201b872, 'gSpriteAttrBufData',
     'gsprattrb_p2_958c8',
     'step_prng_anim_frame caseD_1f: dst for copy_bytes_by_halfword(gEquipChainEntryBase, gSpriteAttrBuf+2, 0x10)'),
    (0x08095aa0, 0x0201b872, 'gSpriteAttrBufData',
     'gsprattrb_p2_95aa0',
     'step_prng_anim_frame caseD_19: copy dst for copy_bytes_by_halfword 0x30 bytes'),
    (0x08095ac0, 0x0201b872, 'gSpriteAttrBufData',
     'gsprattrb_p2_95ac0',
     'step_prng_anim_frame LAB_08095aa4: copy_bytes_by_halfword(gEffectEntryArray+idx*24, gSpriteAttrBuf+2, 0x18)'),

    # --- gEquipZoneRankState (ewram.inc:441, 0x0201e4d0) -- 2 slots ---
    (0x08095634, 0x0201e4d0, 'gEquipZoneRankState',
     'gequipzonerank_95634',
     'step_prng_anim_frame caseD_15: bl copy_bytes_by_halfword(gEquipZoneRankState, gSpriteAttrBuf+2, 0x18)'),
    (0x08095644, 0x0201e4d0, 'gEquipZoneRankState',
     'gequipzonerank_95644',
     'step_prng_anim_frame caseD_16 LAB_080959b2: same copy src'),

    # --- gDuelPhaseFlags (ewram.inc:353, 0x0201b290) -- 9 slots ---
    (0x08095708, 0x0201b290, 'gDuelPhaseFlags',
     'gphaseflag_95708',
     'step_prng_anim_frame caseD_c: clears [+0x594] [+0x58c] [+0x590]; ORs 0x10 into [gSpriteAttrBuf+0x300]'),
    (0x08095780, 0x0201b290, 'gDuelPhaseFlags',
     'gphaseflag_95780',
     'step_prng_anim_frame caseD_e: [+GPRNG_SCENE_CTX_DISPLAY_FLAG_OFF=0x584] := 1'),
    (0x08095810, 0x0201b290, 'gDuelPhaseFlags',
     'gphaseflag_95810',
     'step_prng_anim_frame caseD_f: ldr+adds -> [gDuelPhaseFlags+0x594]=sprite_id from gSpriteAttrBuf'),
    (0x080957b4, 0x0201b290, 'gDuelPhaseFlags',
     'gphaseflag_957b4',
     'step_prng_anim_frame caseD_13: adds r0,r1 r1=0x594 -> gDuelPhaseFlags+EFFECT_ENTRY_COUNT_OFF'),
    (0x08095874, 0x0201b290, 'gDuelPhaseFlags',
     'gphaseflag_95874',
     'step_prng_anim_frame caseD_11: [+0x584]:=1'),
    (0x08095940, 0x0201b290, 'gDuelPhaseFlags',
     'gphaseflag_95940',
     'step_prng_anim_frame caseD_1d: [+0x494]=count*24+gEffectEntryArray'),
    (0x08095a9c, 0x0201b290, 'gDuelPhaseFlags',
     'gphaseflag_95a9c',
     'step_prng_anim_frame caseD_19: [+0x94*8=0x4a0]:=0 clear state; [+0x90*8=0x480] count check'),
    (0x080959c4, 0x0201b290, 'gDuelPhaseFlags',
     'gphaseflag_959c4',
     'step_prng_anim_frame caseD_1b'),
    (0x08095a9c, 0x0201b290, 'gDuelPhaseFlags',
     'gphaseflag_95a9c_dup',
     None),  # dup entry handled gracefully

    # --- EFFECT_ENTRY_COUNT_OFF (ewram.inc:359, 0x00000594) -- 3 slots ---
    (0x0809570c, 0x00000594, 'EFFECT_ENTRY_COUNT_OFF',
     'effect_cnt_9570c',
     'step_prng_anim_frame caseD_c: [gDuelPhaseFlags+0x594]:=0'),
    (0x080957b8, 0x00000594, 'EFFECT_ENTRY_COUNT_OFF',
     'effect_cnt_957b8',
     'step_prng_anim_frame caseD_13: [gDuelPhaseFlags+0x594]=effect entry count'),
    (0x08095814, 0x00000594, 'EFFECT_ENTRY_COUNT_OFF',
     'effect_cnt_95814',
     'step_prng_anim_frame caseD_f'),

    # --- EQUIP_SLOT_SUBSTATE_OFF (ewram.inc:538, 0x0000058c) -- 2 slots ---
    (0x08095710, 0x0000058c, 'EQUIP_SLOT_SUBSTATE_OFF',
     'equip_substate_95710',
     'step_prng_anim_frame caseD_c: [gDuelPhaseFlags+0x58c]:=0'),
    (0x0809581c, 0x0000058c, 'EQUIP_SLOT_SUBSTATE_OFF',
     'equip_substate_9581c',
     'step_prng_anim_frame caseD_f: [gDuelPhaseFlags+0x58c]:=0'),

    # --- LP_BAR_ANIM_STATE_OFF (ewram.inc:405, 0x000004cc) -- 1 slot ---
    (0x0809571c, 0x000004cc, 'LP_BAR_ANIM_STATE_OFF',
     'lp_bar_anim_9571c',
     'step_prng_anim_frame caseD_b+c: [gDuelPhaseFlags+0x4cc] str r4'),

    # --- SPRITE_ROW_ENTRY_DATA_OFF (ewram.inc:411, 0x000004d4) -- 1 slot ---
    (0x08095720, 0x000004d4, 'SPRITE_ROW_ENTRY_DATA_OFF',
     'sprite_row_data_95720',
     'step_prng_anim_frame caseD_b: [gDuelPhaseFlags+0x4d4] byte array base'),

    # --- CHAIN_NODE_CARD_ARR_OFF (ewram.inc:447, 0x000004f4) -- 1 slot ---
    (0x08095724, 0x000004f4, 'CHAIN_NODE_CARD_ARR_OFF',
     'chain_node_arr_95724',
     'step_prng_anim_frame caseD_b: [gDuelPhaseFlags+0x4f4] card ptr array'),

    # --- GPRNG_SCENE_CTX_DISPLAY_FLAG_OFF (duel_field.inc:97, 0x00000584) -- 2 slots ---
    (0x08095784, 0x00000584, 'GPRNG_SCENE_CTX_DISPLAY_FLAG_OFF',
     'gprng_disp_flag_95784',
     'step_prng_anim_frame caseD_e: str 1 -> [gDuelPhaseFlags+0x584] display-ready'),
    (0x08095878, 0x00000584, 'GPRNG_SCENE_CTX_DISPLAY_FLAG_OFF',
     'gprng_disp_flag_95878',
     'step_prng_anim_frame caseD_11: [gDuelPhaseFlags+0x584]:=1'),

    # --- SPRITE_ATTR_BYTE_2FE_OFF (ewram.inc NEW, 0x000002fe) -- 2 slots ---
    (0x08095788, 0x000002fe, 'SPRITE_ATTR_BYTE_2FE_OFF',
     'sprite_byte_2fe_95788',
     'step_prng_anim_frame caseD_e/11: adds r4,r4,r2 r4=gSpriteAttrBuf+2 r2=0x2fe -> byte at +0x300'),
    (0x0809587c, 0x000002fe, 'SPRITE_ATTR_BYTE_2FE_OFF',
     'sprite_byte_2fe_9587c',
     'step_prng_anim_frame caseD_11: adds r4,r4,r2 r2=0x2fe -> byte at gSpriteAttrBuf+2+0x2fe'),

    # --- LP_PLAYER_SIDE_CACHE_OFF (ewram.inc NEW, 0x00001d64) -- 2 slots ---
    (0x08095778, 0x00001d64, 'LP_PLAYER_SIDE_CACHE_OFF',
     'lp_playerside_9578',
     'step_prng_anim_frame caseD_e: [gP1LifePoints+0x1d64]:=[gDuelCardCtxBase+4] XOR 1; player_side cache'),
    (0x0809586c, 0x00001d64, 'LP_PLAYER_SIDE_CACHE_OFF',
     'lp_playerside_9586c',
     'step_prng_anim_frame caseD_11: [+0x1d64]:=[gDuelCardCtxBase+4] XOR 1 (same pattern as caseD_e)'),

    # --- gEffectEntryArray (ewram.inc:358, 0x0201b590) -- 4 slots ---
    (0x080957a4, 0x0201b590, 'gEffectEntryArray',
     'geffectentry_957a4',
     'step_prng_anim_frame caseD_12: adds r0,r0,r2 r2=gEffectEntryArray -> base+entry_offset'),
    (0x08095908, 0x0201b590, 'gEffectEntryArray',
     'geffectentry_95908',
     'step_prng_anim_frame caseD_1c: adds r0,r0,r1 -> gEffectEntryArray+sprite_id*24'),
    (0x08095980, 0x0201b590, 'gEffectEntryArray',
     'geffectentry_95980',
     'step_prng_anim_frame caseD_1a: effect entry base'),
    (0x08095a3c, 0x0201b590, 'gEffectEntryArray',
     'geffectentry_95a3c',
     'step_prng_anim_frame caseD_18'),

    # --- LP_DISPLAY_STATE_OFF (ewram.inc NEW, 0x00001d0c) -- 3 slots ---
    (0x08095530, 0x00001d0c, 'LP_DISPLAY_STATE_OFF',
     'lp_disp_state_95530',
     'step_prng_anim_frame: [gP1LifePoints+0x1d0c] LP display state control; ldr then b LAB_08095b12'),
    (0x08095afc, 0x00001d0c, 'LP_DISPLAY_STATE_OFF',
     'lp_disp_state_95afc',
     'step_prng_anim_frame caseD_1: ldr r3=[0x1d0c]; adds r0,r0,r3; b LAB_08095b12 -> writes 1'),
    (0x08095b24, 0x00001d0c, 'LP_DISPLAY_STATE_OFF',
     'lp_disp_state_95b24',
     'step_prng_anim_frame caseD_4: after pack_sprite_row_attr_words, [gP1LifePoints+0x1d0c]:=1'),
    (0x08095b4c, 0x00001d0c, 'LP_DISPLAY_STATE_OFF',
     'lp_disp_state_95b4c',
     'get_lp_display_state_word: ldr r0,[r0+r1] returns [gP1LifePoints+0x1d0c]'),

    # --- LP_EQUIP_DISPLAY_FLAG_OFF (ewram.inc NEW, 0x00001d84) -- 1 slot ---
    (0x080958a8, 0x00001d84, 'LP_EQUIP_DISPLAY_FLAG_OFF',
     'lp_equip_disp_958a8',
     'step_prng_anim_frame caseD_1e: str 1 to [gP1LifePoints+0x1d84] after setup_lp_display_row_with_data'),

    # --- gEquipChainEntryBase (ewram.inc:391, 0x0201e288) -- 1 slot ---
    (0x080958c4, 0x0201e288, 'gEquipChainEntryBase',
     'gequipchain_958c4',
     'step_prng_anim_frame caseD_1f: bl copy_bytes_by_halfword(gEquipChainEntryBase, gSpriteAttrBuf+2, 0x10)'),

    # --- SPRITE_ATTR_BYTE_2FF_OFF (ewram.inc NEW, 0x000002ff) -- 1 slot ---
    (0x080958cc, 0x000002ff, 'SPRITE_ATTR_BYTE_2FF_OFF',
     'sprite_byte_2ff_958cc',
     'step_prng_anim_frame caseD_1f: adds r4,r4,r0 r0=0x2ff -> byte at gSpriteAttrBuf+2+0x2ff'),

    # --- SPRITE_ROW_ENTRY_30D_OFF (ewram.inc NEW, 0x0000030d) -- 1 slot ---
    (0x0809590c, 0x0000030d, 'SPRITE_ROW_ENTRY_30D_OFF',
     'sprite_entry_30d_9590c',
     'step_prng_anim_frame caseD_1c: strb r0,[r1,#0] -> [gSpriteAttrBuf+0x30d]:=0 (clear byte)'),

    # --- SPRITE_ROW_BUSY_BYTE_OFF (ewram.inc NEW, 0x00000301) -- 7 slots ---
    (0x08095910, 0x00000301, 'SPRITE_ROW_BUSY_BYTE_OFF',
     'sprite_busy_95910',
     'step_prng_anim_frame caseD_1c: adds r4,r4,r5; ldrb r1,[r4,#0]; ORs 0x10 -> [gSpriteAttrBuf+0x301]'),
    (0x0809593c, 0x00000301, 'SPRITE_ROW_BUSY_BYTE_OFF',
     'sprite_busy_9593c',
     'step_prng_anim_frame caseD_1d: [gSpriteAttrBuf+0x301] ORed 0x20'),
    (0x08095988, 0x00000301, 'SPRITE_ROW_BUSY_BYTE_OFF',
     'sprite_busy_95988',
     'step_prng_anim_frame caseD_1a: [gSpriteAttrBuf+0x301] ORed 0x4'),
    (0x080959c0, 0x00000301, 'SPRITE_ROW_BUSY_BYTE_OFF',
     'sprite_busy_959c0',
     'step_prng_anim_frame caseD_1b: [gSpriteAttrBuf+0x301] ORed 0x8'),
    (0x08095a64, 0x00000301, 'SPRITE_ROW_BUSY_BYTE_OFF',
     'sprite_busy_95a64',
     'step_prng_anim_frame LAB_08095a48: [gSpriteAttrBuf+0x301] ORed 0x40'),
    (0x08095a60, 0x0000030f, 'SPRITE_ROW_ENTRY_30F_OFF',
     'sprite_entry_30f_95a60',
     'step_prng_anim_frame LAB_08095a48: [gSpriteAttrBuf+0x30f]:=0 clear'),

    # --- SPRITE_ROW_ANIM_CTL_OFF (ewram.inc:435, 0x00000494) -- 2 slots ---
    (0x08095944, 0x00000494, 'SPRITE_ROW_ANIM_CTL_OFF',
     'sprite_anim_ctl_95944',
     'step_prng_anim_frame caseD_1d: [gDuelPhaseFlags+0x494] sprite type index'),
    (0x080959c8, 0x00000494, 'SPRITE_ROW_ANIM_CTL_OFF',
     'sprite_anim_ctl_959c8',
     'step_prng_anim_frame caseD_1b: [gDuelPhaseFlags+0x494] stride'),

    # --- SPRITE_ROW_ENTRY_30E_OFF (ewram.inc NEW, 0x0000030e) -- 1 slot ---
    (0x08095984, 0x0000030e, 'SPRITE_ROW_ENTRY_30E_OFF',
     'sprite_entry_30e_95984',
     'step_prng_anim_frame caseD_1a: strb 0 -> [gSpriteAttrBuf+0x30e] clear'),

    # --- LP_ACTIVATION_TYPE_ARRAY_BASE_OFF (ewram.inc NEW, 0x000010e1) -- 1 slot ---
    (0x08095a44, 0x000010e1, 'LP_ACTIVATION_TYPE_ARRAY_BASE_OFF',
     'lp_act_type_base_95a44',
     'step_prng_anim_frame caseD_18: r1=gP1LifePoints+field_slot*4+0x10e1 ORs bit7; per-slot activation type byte'),

    # --- SPRITE_ROW_BITS18_15_CLEAR_MASK (duel_field.inc NEW, 0xfff87fff) -- 1 slot ---
    (0x08095494, 0xfff87fff, 'SPRITE_ROW_BITS18_15_CLEAR_MASK',
     'sprite_bits1815_mask_95494',
     'dispatch_sprite_row_write_by_type: ands r0,r3 clears bits[18:15] before ORing new direction bits'),

    # --- P1LP_BLOCK2_OFF (ewram.inc:243, 0x00001d08) -- 1 slot ---
    (0x08095b9c, 0x00001d08, 'P1LP_BLOCK2_OFF',
     'p1lp_blk2_95b9c',
     'check_player_side_condition: [gP1LifePoints+0x1d08] flag check'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_vaddr, gas_label, slot_label, eol_ascii_or_None)
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # --- jump table ptr for dispatch_equip_confirm_phase_by_step ---
    (0x08095248, 0x0809524c, 'equip_confirm_case_jump_table',
     'eq_confirm_jumptbl_95248',
     'ptr to 10-entry raw-address jump table at 0x0809524c; dispatch via mov pc,r0 (0x4687)'),
    # --- second switchD dispatch table for step_prng_anim_frame ---
    (0x08095550, 0x08095554, 'switchD_0809554c__switchdataD_08095554',
     'sprite_row_tbl2_95550',
     'step_prng_anim_frame second switchD: 30-entry dispatch table base at 0x08095554; ldr r1,[DAT_08095550]; adds r0,r0,r1; ldr r0,[r0]; mov pc,r0'),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
#    All PTR_gP1LifePoints_* and DWORD_gP1LifePoints/DWORD_other slots -> snake_case rename.
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    # PTR_gP1LifePoints_* -> gp1lp_ptr_* (12 slots -- 11 true PTR_gP1LP + Fix#1 0x0809552c)
    (0x08095024, 'gp1lp_ptr_95024', None),
    (0x0809507c, 'gp1lp_ptr_9507c', None),
    (0x0809552c, 'gp1lp_ptr_9552c', None),  # Fix #1: was missing
    (0x08095774, 'gp1lp_ptr_95774', None),
    (0x08095868, 'gp1lp_ptr_95868', None),
    (0x080958a4, 'gp1lp_ptr_958a4', None),
    (0x08095a40, 'gp1lp_ptr_95a40', None),
    (0x08095af8, 'gp1lp_ptr_95af8', None),
    (0x08095b20, 'gp1lp_ptr_95b20', None),
    (0x08095b48, 'gp1lp_ptr_95b48', None),
    (0x08095b98, 'gp1lp_ptr_95b98', None),
    # DWORD_gP1LifePoints (3 slots)
    (0x08095204, 'gp1lp_ptr_95204', None),
    (0x08095240, 'gp1lp_ptr_95240', None),
    (0x0809535c, 'gp1lp_ptr_9535c', None),
    # DWORD_ holding non-gP1LP values (7 slots -- already in EQ_SLOTS above as EQ targets,
    # rename here to remove DWORD_ prefix and apply slot_label)
    (0x08095208, 'act_state_c_95208', None),
    (0x0809520c, 'lp_equip_b_9520c', None),
    (0x0809521c, 'lp_equip_b_9521c', None),
    (0x08095244, 'eligib_act_type_95244', None),
    (0x08095344, 'eligib_state_ctrl_95344', None),
    (0x08095360, 'eligib_act_cnt_95360', None),
    (0x0809537c, 'eligib_state_ctrl_9537c', None),
]

# ---------------------------------------------------------------------------
# D. PLATE_REWRITES: (func_addr, old_stale_fn, new_real_name)
#    Substring replace in existing plate comment. Pure ASCII only.
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    # write_spell_activation_type_display_bit (0x08094f58): FUN_0804154c -> tick_spell_equip_zone_display_seq
    (0x08094f58, 'FUN_0804154c', 'tick_spell_equip_zone_display_seq'),
    # update_card_display_index_by_type_rules (0x08094f70): FUN_080954e8 -> step_prng_anim_frame
    # Also note: FUN_08095a18 is a LAB_ label inside step_prng_anim_frame, not a function
    (0x08094f70, 'FUN_080954e8', 'step_prng_anim_frame'),
    # count_nonzero_results_in_zone_matrix (0x08095194): FUN_080a2ad0 -> tick_equip_target_selection_display_seq
    (0x08095194, 'FUN_080a2ad0', 'tick_equip_target_selection_display_seq'),
    # dispatch_sprite_row_write_by_type (0x080953c4): FUN_080954e8 -> step_prng_anim_frame
    (0x080953c4, 'FUN_080954e8', 'step_prng_anim_frame'),
    # step_prng_anim_frame (0x080954e8): FUN_08094dac -> advance_duel_turn_by_prng_anim
    (0x080954e8, 'FUN_08094dac', 'advance_duel_turn_by_prng_anim'),
    # get_lp_display_state_word (0x08095b3c): FUN_080954e8 -> step_prng_anim_frame
    (0x08095b3c, 'FUN_080954e8', 'step_prng_anim_frame'),
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
        print("[SKIP] EQ 0x%08x (%s) value mismatch" % (slot_addr, eq_name))
        return

    if DRY:
        print("[dry] EQ 0x%08x  %s=%s  label=%s" % (slot_addr, eq_name, hex(value), slot_label))
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

    # EOL comment
    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[EQ ] 0x%08x  %s  -> %s" % (slot_addr, eq_name, slot_label))

def _apply_ref(slot_addr, target_vaddr, gas_label, slot_label, eol):
    sa = _addr(slot_addr)
    ta = _addr(target_vaddr)
    sym_tbl = currentProgram.getSymbolTable()
    ref_mgr = currentProgram.getReferenceManager()

    if DRY:
        print("[dry] REF 0x%08x -> 0x%08x  %s  slot=%s" % (slot_addr, target_vaddr, gas_label, slot_label))
        return

    # create USER_DEFINED label at target if not already there
    tgt_syms = sym_tbl.getSymbols(ta)
    tgt_names = [s.getName() for s in tgt_syms]
    if gas_label not in tgt_names:
        sym_tbl.createLabel(ta, gas_label, SourceType.USER_DEFINED)

    # add DATA ref from slot to target
    ref_mgr.addMemoryReference(sa, ta, RefType.DATA, SourceType.USER_DEFINED, 0)
    # set primary
    for ref in ref_mgr.getReferencesFrom(sa):
        if ref.getToAddress().equals(ta):
            ref_mgr.setPrimary(ref, True)

    # create slot label
    s_syms = sym_tbl.getSymbols(sa)
    s_names = [s.getName() for s in s_syms]
    if slot_label not in s_names:
        sym_tbl.createLabel(sa, slot_label, SourceType.USER_DEFINED)

    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(sa)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[REF] 0x%08x -> 0x%08x  %s  slot=%s" % (slot_addr, target_vaddr, gas_label, slot_label))

def _apply_rename(slot_addr, slot_label, eol):
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()

    if DRY:
        print("[dry] RENAME 0x%08x -> %s" % (slot_addr, slot_label))
        return

    existing = sym_tbl.getSymbols(a)
    names = [s.getName() for s in existing]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)

    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[REN] 0x%08x -> %s" % (slot_addr, slot_label))

def _apply_plate_fix(func_addr, old_sub, new_sub):
    """Substring replace in plate comment. WARN if not found (treat as FAIL)."""
    a = _addr(func_addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[FAIL] plate_fix 0x%08x: no code unit" % func_addr)
        return False

    current = cu.getComment(CodeUnit.PLATE_COMMENT)
    if current is None:
        print("[FAIL] plate_fix 0x%08x: no plate comment" % func_addr)
        return False

    if old_sub not in current:
        print("[FAIL] plate_fix 0x%08x: '%s' not found in plate" % (func_addr, old_sub))
        return False

    if DRY:
        print("[dry] PLATE 0x%08x: '%s' -> '%s'" % (func_addr, old_sub, new_sub))
        return True

    new_plate = current.replace(old_sub, new_sub)
    cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)
    print("[PLT] 0x%08x: replaced '%s' -> '%s'" % (func_addr, old_sub, new_sub))
    return True

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF12Seg2Slots (DRY=%s) ===" % DRY)
    print("  Seg-2: 0x08094f20..0x08095ba8, file 12 equip_activation_scan")
    print("  EQ=%d  REF=%d  RENAME=%d  PLATE=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATE_REWRITES)))

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    eq_ok = 0
    eq_skip = 0
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        # skip dup entries gracefully
        if slot_label.endswith('_dup'):
            continue
        _apply_eq(slot_addr, value, eq_name, slot_label, eol)
        eq_ok += 1
    print("  EQ done: %d" % eq_ok)

    # B. REF_SLOTS
    print("\n--- B. REF_SLOTS (%d) ---" % len(REF_SLOTS))
    for entry in REF_SLOTS:
        slot_addr, target_vaddr, gas_label, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        _apply_ref(slot_addr, target_vaddr, gas_label, slot_label, eol)
    print("  REF done: %d" % len(REF_SLOTS))

    # C. RENAME_SLOTS
    print("\n--- C. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    for entry in RENAME_SLOTS:
        slot_addr, slot_label = entry[0], entry[1]
        eol = entry[2] if len(entry) > 2 else None
        _apply_rename(slot_addr, slot_label, eol)
    print("  RENAME done: %d" % len(RENAME_SLOTS))

    # D. PLATE_REWRITES
    print("\n--- D. PLATE_REWRITES (%d) ---" % len(PLATE_REWRITES))
    plate_ok = 0
    plate_fail = 0
    for func_addr, old_sub, new_sub in PLATE_REWRITES:
        if _apply_plate_fix(func_addr, old_sub, new_sub):
            plate_ok += 1
        else:
            plate_fail += 1
    print("  PLATE done: ok=%d fail=%d" % (plate_ok, plate_fail))
    if plate_fail > 0:
        print("[WARN] %d PLATE replacements failed -- check stale FUN_ coverage" % plate_fail)

    print("\n=== RefineF12Seg2Slots DONE ===")
    print("  EQ=%d  REF=%d  RENAME=%d  PLATE_ok=%d PLATE_fail=%d" % (
        eq_ok, len(REF_SLOTS), len(RENAME_SLOTS), plate_ok, plate_fail))

main()
