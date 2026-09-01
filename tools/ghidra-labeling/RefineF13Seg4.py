# -*- coding: ascii -*-
#@runtime Jython
#@category Ygo-ex2006
# F13-Seg-4 final PASS materialization. Dry/check must use direct -noanalysis -readOnly.
# No data creation, disassembly, memory writes, function creation, carve, or function rename.

EQ_SLOTS = [(134875260, 781, 'SPRITE_ROW_ENTRY_30D_OFF', 'sprite_row_entry_30d_off_080a087c'),
 (134875352, 1156, 'EQUIP_ACTIVE_CTX_OFF', 'equip_active_ctx_off_080a08d8'),
 (134875360, 781, 'SPRITE_ROW_ENTRY_30D_OFF', 'sprite_row_entry_30d_off_080a08e0'),
 (134875460, 782, 'SPRITE_ROW_ENTRY_30E_OFF', 'sprite_row_entry_30e_off_080a0944'),
 (134875552, 1204, 'EQUIP_ACTIVATION_AUX_OFF', 'equip_activation_aux_off_080a09a0'),
 (134875556, 1156, 'EQUIP_ACTIVE_CTX_OFF', 'equip_active_ctx_off_080a09a4'),
 (134875564, 782, 'SPRITE_ROW_ENTRY_30E_OFF', 'sprite_row_entry_30e_off_080a09ac'),
 (134875652, 783, 'SPRITE_ROW_ENTRY_30F_OFF', 'sprite_row_entry_30f_off_080a0a04'),
 (134875740, 1156, 'EQUIP_ACTIVE_CTX_OFF', 'equip_active_ctx_off_080a0a5c'),
 (134875748, 783, 'SPRITE_ROW_ENTRY_30F_OFF', 'sprite_row_entry_30f_off_080a0a64'),
 (134875828, 769, 'SPRITE_ROW_BUSY_BYTE_OFF', 'sprite_row_busy_byte_off_080a0ab4'),
 (134878076, 7564, 'EQUIP_CONTEXT_PLAYER_OFF', 'equip_context_player_off_080a137c'),
 (134878080, 7576, 'EQUIP_REROLL_SPRITE_PARAM_OFF', 'equip_reroll_sprite_param_off_080a1380'),
 (134878084, 7578, 'EQUIP_REROLL_COUNT_TARGET_OFF', 'equip_reroll_count_target_off_080a1384'),
 (134878212, 7592, 'LP_CARD_TRACK_BASE_OFF', 'lp_card_track_base_off_080a1404'),
 (134878216, 32859, 'OAM_COIN_REROLL_SPRITE_P2_5B', 'oam_coin_reroll_sprite_p2_5b_080a1408'),
 (134878224, 7572, 'EQUIP_PHASE_DISPLAY_STATE_OFF', 'equip_phase_display_state_off_080a1410'),
 (134878312, 5391, 'SECOND_COIN_TOSS_CID', 'second_coin_toss_cid_080a1468'),
 (134878320, 7594, 'LP_CARD_TRACK_NEXT_OFF', 'lp_card_track_next_off_080a1470'),
 (134878348, 287, 'GAME_STR_PERFORM_COIN_TOSS_AGAIN_ID', 'game_str_perform_coin_toss_again_id_080a148c'),
 (134878356, 7572, 'EQUIP_PHASE_DISPLAY_STATE_OFF', 'equip_phase_display_state_off_080a1494'),
 (134878400, 5391, 'SECOND_COIN_TOSS_CID', 'second_coin_toss_cid_080a14c0'),
 (134878468, 7594, 'LP_CARD_TRACK_NEXT_OFF', 'lp_card_track_next_off_080a1504'),
 (134878552, 7564, 'EQUIP_CONTEXT_PLAYER_OFF', 'equip_context_player_off_080a1558'),
 (134878556, 7576, 'EQUIP_REROLL_SPRITE_PARAM_OFF', 'equip_reroll_sprite_param_off_080a155c'),
 (134878560, 7578, 'EQUIP_REROLL_COUNT_TARGET_OFF', 'equip_reroll_count_target_off_080a1560'),
 (134878564, 7572, 'EQUIP_PHASE_DISPLAY_STATE_OFF', 'equip_phase_display_state_off_080a1564'),
 (134878624, 7592, 'LP_CARD_TRACK_BASE_OFF', 'lp_card_track_base_off_080a15a0'),
 (134878628, 32860, 'OAM_DICE_REROLL_SPRITE_P2_5C', 'oam_dice_reroll_sprite_p2_5c_080a15a4'),
 (134878636, 7572, 'EQUIP_PHASE_DISPLAY_STATE_OFF', 'equip_phase_display_state_off_080a15ac'),
 (134878712, 5797, 'DICE_RE_ROLL_CID', 'dice_re_roll_cid_080a15f8'),
 (134878720, 7592, 'LP_CARD_TRACK_BASE_OFF', 'lp_card_track_base_off_080a1600'),
 (134878752, 7572, 'EQUIP_PHASE_DISPLAY_STATE_OFF', 'equip_phase_display_state_off_080a1620'),
 (134878796, 5797, 'DICE_RE_ROLL_CID', 'dice_re_roll_cid_080a164c')]

REF_SLOTS = [(134875252, 33667184, 'gSpriteAttrBuf', 'sprite_attr_buf_ref_080a0874'),
 (134875256, 33666448, 'gEffectEntryArray', 'effect_entry_array_ref_080a0878'),
 (134875348, 33665680, 'gDuelPhaseFlags', 'duel_phase_flags_ref_080a08d4'),
 (134875356, 33667184, 'gSpriteAttrBuf', 'sprite_attr_buf_ref_080a08dc'),
 (134875452, 33667184, 'gSpriteAttrBuf', 'sprite_attr_buf_ref_080a093c'),
 (134875456, 33666448, 'gEffectEntryArray', 'effect_entry_array_ref_080a0940'),
 (134875548, 33665680, 'gDuelPhaseFlags', 'duel_phase_flags_ref_080a099c'),
 (134875560, 33667184, 'gSpriteAttrBuf', 'sprite_attr_buf_ref_080a09a8'),
 (134875644, 33667184, 'gSpriteAttrBuf', 'sprite_attr_buf_ref_080a09fc'),
 (134875648, 33666448, 'gEffectEntryArray', 'effect_entry_array_ref_080a0a00'),
 (134875736, 33665680, 'gDuelPhaseFlags', 'duel_phase_flags_ref_080a0a58'),
 (134875744, 33667184, 'gSpriteAttrBuf', 'sprite_attr_buf_ref_080a0a60'),
 (134875824, 33667184, 'gSpriteAttrBuf', 'sprite_attr_buf_ref_080a0ab0'),
 (134878316, 33677984, 'gDuelCardCtxBase', 'duel_card_ctx_ref_080a146c'),
 (134878460, 33677984, 'gDuelCardCtxBase', 'duel_card_ctx_ref_080a14fc'),
 (134878716, 33677984, 'gDuelCardCtxBase', 'duel_card_ctx_ref_080a15fc')]

RENAME_SLOTS = [(134878072, 'gp1lp_ptr_080a1378', 'gP1LifePoints base; preserve existing operand-0 DATA/USER_DEFINED reference.'),
 (134878220, 'gp1lp_ptr_080a140c', 'gP1LifePoints base; preserve existing operand-0 DATA/USER_DEFINED reference.'),
 (134878352, 'gp1lp_ptr_080a1490', 'gP1LifePoints base; preserve existing operand-0 DATA/USER_DEFINED reference.'),
 (134878464, 'gp1lp_ptr_080a1500', 'gP1LifePoints base; preserve existing operand-0 DATA/USER_DEFINED reference.'),
 (134878548, 'gp1lp_ptr_080a1554', 'gP1LifePoints base; preserve existing operand-0 DATA/USER_DEFINED reference.'),
 (134878632, 'gp1lp_ptr_080a15a8', 'gP1LifePoints base; preserve existing operand-0 DATA/USER_DEFINED reference.'),
 (134878748, 'gp1lp_ptr_080a161c', 'gP1LifePoints base; preserve existing operand-0 DATA/USER_DEFINED reference.')]

PLATES = [(134875200,
  'update_equip_sprite_state_by_slot_status',
  'No arguments. Uses gSpriteAttrBuf+0x310 as the effect-entry count and gEffectEntryArray stride 0x18. Control byte '
  '+0x30d selects initialization, handler, or sprite-row paths. The handler stores the current entry at '
  'gDuelPhaseFlags+EQUIP_ACTIVE_CTX_OFF, calls invoke_card_effect_node_handler(current, previous), records the '
  'result sign, and advances the control byte. Returns 0 only after the handler path; otherwise 1. Caller: '
  'route_equip_slot_tick_by_flag.'),
 (134875388,
  'dispatch_equip_effect_by_slot_state',
  'No arguments. Uses gSpriteAttrBuf+0x310 and gEffectEntryArray stride 0x18. Control byte +0x30e selects '
  'initialization, invoke_effect_node_action_if_found, or sprite-row 0x1b. Initialization clears two gDuelPhaseFlags '
  'fields. The handler stores the current entry at +EQUIP_ACTIVE_CTX_OFF, updates entry byte +4 bit 0, and advances '
  'the control byte. Returns 0 after the handler path; otherwise 1. Caller: route_equip_slot_tick_by_flag.'),
 (134875592,
  'dispatch_equip_lp_delta_by_slot_status',
  'No arguments. Uses gSpriteAttrBuf+0x310 and gEffectEntryArray stride 0x18. Control byte +0x30f selects '
  'initialization, LP-delta handling, or sprite-row 0x19. The handler stores the current entry at '
  'gDuelPhaseFlags+EQUIP_ACTIVE_CTX_OFF, calls apply_equip_lp_delta_by_node_flag(current, previous), stores the '
  'result at +0x4a0, and advances only when the result is zero. Returns 0 after the handler path; otherwise 1.'),
 (134875788,
  'route_equip_slot_tick_by_flag',
  'No arguments. Reads gSpriteAttrBuf+SPRITE_ROW_BUSY_BYTE_OFF. In order, it services flag 0x10 with '
  'update_equip_sprite_state_by_slot_status, flag 0x20 with dispatch_equip_effect_by_slot_state, '
  'gSpriteAttrBuf+0x300 flag 0x10 with dispatch_equip_slot_state_by_index, and flag 0x40 with '
  'dispatch_equip_lp_delta_by_slot_status. Completed handlers clear their flag. Returns 1 after a selected handler '
  'and 0 when no relevant flag is set.'),
 (134875924,
  'tick_equip_slot_activation_step',
  'No arguments. Calls route_equip_slot_tick_by_flag, discards its return value, and always returns 0. Called once '
  'from tick_equip_activation_main_sequence at 0x08094d96.'),
 (134878008,
  'tick_equip_zone_sprite_phase_a',
  'No APCS arguments; r8-r10 are inherited context. Drives the three-state Second Coin Toss reroll display at '
  'gP1LifePoints+0x1d94. State 0 builds coin sprite records from the packed parameters at +0x1d98/+0x1d9a. State 1 '
  'checks CID 0x150f, issues game string 287 when confirmation is needed, and advances. State 2 enqueues the zone '
  'sprite and resets the display phase state. Other states return 1. No incoming call or pointer reference is '
  'defined in the current image.'),
 (134878500,
  'tick_equip_zone_sprite_phase_b',
  'No APCS arguments; r8-r10 are inherited context. Drives the three-state Dice Re-Roll display at '
  'gP1LifePoints+0x1d94. State 0 builds die sprite records from +0x1d98/+0x1d9a. State 1 checks CID 0x16a5 in zone '
  '11 for modes 1 and 2, issues game string 288 when confirmation is needed, and advances. State 2 enqueues the '
  'equip-zone sprite and resets the display phase state. Other states return 1. No incoming call or pointer '
  'reference is defined in the current image.')]

SLOT_EOLS = [(134875252, 'gSpriteAttrBuf: sprite attribute buffer base; add operand-0 DATA/USER_DEFINED reference.'),
 (134875256, 'gEffectEntryArray: 0x18-byte effect entry array base; add operand-0 DATA/USER_DEFINED reference.'),
 (134875260, 'SPRITE_ROW_ENTRY_30D_OFF: gSpriteAttrBuf control byte for status path A.'),
 (134875348,
  'gDuelPhaseFlags: duel phase and equip activation state base; add operand-0 DATA/USER_DEFINED reference.'),
 (134875352, 'EQUIP_ACTIVE_CTX_OFF: gDuelPhaseFlags current effect-entry pointer.'),
 (134875356, 'gSpriteAttrBuf: sprite attribute buffer base; add operand-0 DATA/USER_DEFINED reference.'),
 (134875360, 'SPRITE_ROW_ENTRY_30D_OFF: gSpriteAttrBuf control byte for status path A.'),
 (134875452, 'gSpriteAttrBuf: sprite attribute buffer base; add operand-0 DATA/USER_DEFINED reference.'),
 (134875456, 'gEffectEntryArray: 0x18-byte effect entry array base; add operand-0 DATA/USER_DEFINED reference.'),
 (134875460, 'SPRITE_ROW_ENTRY_30E_OFF: gSpriteAttrBuf control byte for status path B.'),
 (134875548,
  'gDuelPhaseFlags: duel phase and equip activation state base; add operand-0 DATA/USER_DEFINED reference.'),
 (134875552, 'EQUIP_ACTIVATION_AUX_OFF: gDuelPhaseFlags equip activation auxiliary field.'),
 (134875556, 'EQUIP_ACTIVE_CTX_OFF: gDuelPhaseFlags current effect-entry pointer.'),
 (134875560, 'gSpriteAttrBuf: sprite attribute buffer base; add operand-0 DATA/USER_DEFINED reference.'),
 (134875564, 'SPRITE_ROW_ENTRY_30E_OFF: gSpriteAttrBuf control byte for status path B.'),
 (134875644, 'gSpriteAttrBuf: sprite attribute buffer base; add operand-0 DATA/USER_DEFINED reference.'),
 (134875648, 'gEffectEntryArray: 0x18-byte effect entry array base; add operand-0 DATA/USER_DEFINED reference.'),
 (134875652, 'SPRITE_ROW_ENTRY_30F_OFF: gSpriteAttrBuf control byte for LP-delta path.'),
 (134875736,
  'gDuelPhaseFlags: duel phase and equip activation state base; add operand-0 DATA/USER_DEFINED reference.'),
 (134875740, 'EQUIP_ACTIVE_CTX_OFF: gDuelPhaseFlags current effect-entry pointer.'),
 (134875744, 'gSpriteAttrBuf: sprite attribute buffer base; add operand-0 DATA/USER_DEFINED reference.'),
 (134875748, 'SPRITE_ROW_ENTRY_30F_OFF: gSpriteAttrBuf control byte for LP-delta path.'),
 (134875824, 'gSpriteAttrBuf: sprite attribute buffer base; add operand-0 DATA/USER_DEFINED reference.'),
 (134875828, 'SPRITE_ROW_BUSY_BYTE_OFF: gSpriteAttrBuf busy and route flag byte.'),
 (134878072, 'gP1LifePoints base; preserve existing operand-0 DATA/USER_DEFINED reference.'),
 (134878076, 'EQUIP_CONTEXT_PLAYER_OFF: gP1LifePoints-relative equip context player field.'),
 (134878080, 'EQUIP_REROLL_SPRITE_PARAM_OFF: gP1LifePoints-relative coin/dice sprite parameter hword.'),
 (134878084, 'EQUIP_REROLL_COUNT_TARGET_OFF: gP1LifePoints-relative packed reroll count/target hword.'),
 (134878212, 'LP_CARD_TRACK_BASE_OFF: gP1LifePoints scratch hword base reused by reroll animation.'),
 (134878216, 'OAM_COIN_REROLL_SPRITE_P2_5B: P2-side coin-reroll sprite code; P1 uses inline 0x5b.'),
 (134878220, 'gP1LifePoints base; preserve existing operand-0 DATA/USER_DEFINED reference.'),
 (134878224, 'EQUIP_PHASE_DISPLAY_STATE_OFF: gP1LifePoints equip display phase state word.'),
 (134878312, 'SECOND_COIN_TOSS_CID: Second Coin Toss internal CID.'),
 (134878316, 'gDuelCardCtxBase: duel card activation context base; add operand-0 DATA/USER_DEFINED reference.'),
 (134878320, 'LP_CARD_TRACK_NEXT_OFF: adjacent gP1LifePoints scratch hword.'),
 (134878348, 'GAME_STR_PERFORM_COIN_TOSS_AGAIN_ID: game string 287: Perform coin toss again?.'),
 (134878352, 'gP1LifePoints base; preserve existing operand-0 DATA/USER_DEFINED reference.'),
 (134878356, 'EQUIP_PHASE_DISPLAY_STATE_OFF: gP1LifePoints equip display phase state word.'),
 (134878400, 'SECOND_COIN_TOSS_CID: Second Coin Toss internal CID.'),
 (134878460, 'gDuelCardCtxBase: duel card activation context base; add operand-0 DATA/USER_DEFINED reference.'),
 (134878464, 'gP1LifePoints base; preserve existing operand-0 DATA/USER_DEFINED reference.'),
 (134878468, 'LP_CARD_TRACK_NEXT_OFF: adjacent gP1LifePoints scratch hword.'),
 (134878548, 'gP1LifePoints base; preserve existing operand-0 DATA/USER_DEFINED reference.'),
 (134878552, 'EQUIP_CONTEXT_PLAYER_OFF: gP1LifePoints-relative equip context player field.'),
 (134878556, 'EQUIP_REROLL_SPRITE_PARAM_OFF: gP1LifePoints-relative coin/dice sprite parameter hword.'),
 (134878560, 'EQUIP_REROLL_COUNT_TARGET_OFF: gP1LifePoints-relative packed reroll count/target hword.'),
 (134878564, 'EQUIP_PHASE_DISPLAY_STATE_OFF: gP1LifePoints equip display phase state word.'),
 (134878624, 'LP_CARD_TRACK_BASE_OFF: gP1LifePoints scratch hword base reused by reroll animation.'),
 (134878628, 'OAM_DICE_REROLL_SPRITE_P2_5C: P2-side dice-reroll sprite code; P1 uses inline 0x5c.'),
 (134878632, 'gP1LifePoints base; preserve existing operand-0 DATA/USER_DEFINED reference.'),
 (134878636, 'EQUIP_PHASE_DISPLAY_STATE_OFF: gP1LifePoints equip display phase state word.'),
 (134878712, 'DICE_RE_ROLL_CID: Dice Re-Roll internal CID.'),
 (134878716, 'gDuelCardCtxBase: duel card activation context base; add operand-0 DATA/USER_DEFINED reference.'),
 (134878720, 'LP_CARD_TRACK_BASE_OFF: gP1LifePoints scratch hword base reused by reroll animation.'),
 (134878748, 'gP1LifePoints base; preserve existing operand-0 DATA/USER_DEFINED reference.'),
 (134878752, 'EQUIP_PHASE_DISPLAY_STATE_OFF: gP1LifePoints equip display phase state word.'),
 (134878796, 'DICE_RE_ROLL_CID: Dice Re-Roll internal CID.')]

FUNC_RENAME = []

NEW_DEFINITIONS = [('GAME_STR_PERFORM_COIN_TOSS_AGAIN_ID', 287, 'constants/duel_field.inc'),
 ('SECOND_COIN_TOSS_CID', 5391, 'constants/card_info.inc'),
 ('DICE_RE_ROLL_CID', 5797, 'constants/card_info.inc'),
 ('EQUIP_CONTEXT_PLAYER_OFF', 7564, 'constants/duel_field.inc'),
 ('EQUIP_REROLL_SPRITE_PARAM_OFF', 7576, 'constants/duel_field.inc'),
 ('EQUIP_REROLL_COUNT_TARGET_OFF', 7578, 'constants/duel_field.inc'),
 ('OAM_COIN_REROLL_SPRITE_P2_5B', 32859, 'constants/oam_attr.inc'),
 ('OAM_DICE_REROLL_SPRITE_P2_5C', 32860, 'constants/oam_attr.inc')]

BLOCK_GUARD = (134875936, 134878008, 'a528dc1219fac0f18ea7765732cbb678ec14e6320c5322817f06403f1153941b', 'section_5_1')

INPUT_HASHES = [('doc/dev/refine/F13-Seg-4.proposal.md', '2dba3097eafc80290faa35c4a8d7e02541b3a7cd7f08676c5d7f1cdcda2d4eba'),
 ('doc/dev/refine/F13-Seg-4.review.md', '21438e4af40d6d1b6f3678b4b92544728ef7e2f6d76d8fc60aa652c294de1985'),
 ('output/refine-run-20260831-194634/f13-seg4-plan.json',
  '66e0dfd362db5f82670dd3cbcaa5c878e25e5c8ed9fd91ad32bbdef819c823fa'),
 ('output/refine-run-20260831-194634/f13-seg4-plates.json',
  'fcec02ae28a66336c86b107016ca99c0ea9c519f0c755d71b7dff42cadd9364e'),
 ('output/refine-run-20260831-194634/f13-seg4-selfcheck.json',
  'c419a576bc51416717dffac556dd827734789e47fd71cc51be620b326fc4c9a5'),
 ('output/refine-run-20260831-194634/f13-seg4-map.json',
  'b82ac3d6f4d830f1414b4c4dd3bfa92e2d7a93998ec33ee2ba98a737d275effe'),
 ('output/refine-run-20260831-194634/f13-seg4-slots-before.json',
  '47b4fa998f898c2981df427af23b82cf04eb734dc3d1af5d57c91b1630e19efb'),
 ('output/refine-run-20260831-194634/f13-seg4-functions-before.json',
  '1e2e1207f168d2f79b98046b31531bca18ed8c3fba0c09f9ab282ac04462fa40'),
 ('output/refine-run-20260831-194634/f13-seg4-block-code-before.json',
  '22d9497fb2e8b1fe1e486767734663943be8776a4db5cf0d7de32cdbc589b449'),
 ('output/refine-run-20260831-194634/f13-seg4-review-slots.json',
  '35a354f277992a60d6e6f82926038ae90c75d4c60ef0422dbb72958f52f3960e'),
 ('output/refine-run-20260831-194634/f13-seg4-review-constants-names.json',
  'a478dd1e2811ad8495cf486a47d4c5171dc49524e07ba97a32ed9a5264b1af0d'),
 ('output/refine-run-20260831-194634/f13-seg4-review-block.json',
  '859702b21e7067cedad9dad3a82f6a2153fdee27018961aa42d9420c88c2ae3f'),
 ('output/refine-run-20260831-194634/f13-seg4-review-fresh-summary.json',
  'c64ed6c4afdf04844b8850b57db6d5152edfd8897dcdb1d1fad9a9de97b8dfe4'),
 ('output/refine-run-20260831-194634/f13-seg-4-backup.json',
  '1edbc3dc03c9f824af04ae8c96362a83e9ccd6141255d301af3a4b9ac38afa13'),
 ('asm/13_equip_placement.s', '121004fdbfcc154d2677d5e04263e6f2e6039c9e59f56e31a07f9242923fd42b')]

SEGMENT_RANGE_SHA256 = 'b7a5d8fe2f12f0265aa6fb52655690df3d8ef6da3b3f99449acf7f97d79d30aa'

import copy
import hashlib
import json
import os

from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import SourceType, RefType, SymbolType

MODE = list(getScriptArgs())[0].lower() if list(getScriptArgs()) else 'dry'
if MODE not in ('dry', 'apply', 'check'):
    raise RuntimeError('Expected dry, apply, or check')
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(getSourceFile().getAbsolutePath())))
RUN = os.path.join(ROOT, 'output', 'refine-run-20260831-194634')
listing = currentProgram.getListing()
symbols = currentProgram.getSymbolTable()
references = currentProgram.getReferenceManager()
memory = currentProgram.getMemory()
equates = currentProgram.getEquateTable()
context = currentProgram.getProgramContext()
tmode = context.getRegister('TMode')
FAILS = []
COUNTS = dict((key, 0) for key in ('EQ', 'REF', 'RENAME', 'PLATE', 'EOL', 'FUNC_RENAME'))
SEGMENT_START = 0x080a0840
SEGMENT_END = 0x080a1658
EFFECT_ENTRY_ARRAY = 0x0201b590


def fail(message):
    FAILS.append(message)
    print('FAIL: ' + message)


def require(condition, message):
    if not condition:
        fail(message)


def canonical(value):
    if isinstance(value, dict):
        result = dict((key, canonical(item)) for key, item in value.items() if key != 'input_label')
        return result
    if isinstance(value, list):
        result = [canonical(item) for item in value]
        if all(isinstance(item, dict) for item in result):
            result = sorted(result, key=lambda item: json.dumps(item, sort_keys=True))
        return result
    return copy.deepcopy(value)


def same(message, actual, expected):
    if canonical(actual) != canonical(expected):
        fail(message)


def file_hash(path):
    with open(path, 'rb') as stream:
        return hashlib.sha256(stream.read()).hexdigest()


def read_json(name):
    with open(os.path.join(RUN, name), 'r') as stream:
        return json.load(stream)


def write_json(name, value):
    with open(os.path.join(RUN, name), 'w') as stream:
        stream.write(json.dumps(value, ensure_ascii=True, sort_keys=True, indent=2) + '\n')


def basic_ref(ref):
    return {'from': str(ref.getFromAddress()), 'to': str(ref.getToAddress()),
            'operand': ref.getOperandIndex(), 'type': str(ref.getReferenceType()),
            'source': str(ref.getSource()), 'primary': bool(ref.isPrimary())}


def symbol_info(symbol, with_primary=True):
    if symbol is None:
        return None
    result = {'id': long(symbol.getID()), 'name': unicode(symbol.getName()),
              'qualified_name': unicode(symbol.getName(True)),
              'type': str(symbol.getSymbolType()), 'source': str(symbol.getSource())}
    if with_primary:
        result['primary'] = bool(symbol.isPrimary())
    return result


def describe(value):
    addr = toAddr(value)
    data = listing.getDefinedDataAt(addr)
    unit = listing.getCodeUnitContaining(addr)
    fn = getFunctionContaining(addr)
    result = {'address': value, 'symbols': [symbol_info(item) for item in symbols.getSymbols(addr)],
              'defined_data': None if data is None else {
                  'address': str(data.getAddress()), 'length': data.getLength(),
                  'type': unicode(data.getDataType().getPathName()),
                  'min': str(data.getMinAddress()), 'max': str(data.getMaxAddress())},
              'containing_code_unit': None if unit is None else {
                  'address': str(unit.getAddress()), 'length': unit.getLength(),
                  'class': str(unit.getClass().getSimpleName())},
              'instruction_at': None if getInstructionAt(addr) is None else str(getInstructionAt(addr)),
              'containing_function': None if fn is None else {
                  'entry': str(fn.getEntryPoint()), 'name': str(fn.getName()), 'body': str(fn.getBody())},
              'equates': [{'name': str(eq.getName()), 'value': long(eq.getValue())}
                          for eq in equates.getEquates(addr)],
              'comments': {}, 'rom_word': None, 'references_from': [], 'references_to': []}
    for key, kind in [('EOL', CodeUnit.EOL_COMMENT), ('PLATE', CodeUnit.PLATE_COMMENT)]:
        text = listing.getComment(kind, addr)
        result['comments'][key] = None if text is None else unicode(text)
    if 0x08000000 <= value <= 0x09fffffc:
        result['rom_word'] = memory.getInt(addr) & 0xffffffff
    for ref in references.getReferencesFrom(addr):
        item = basic_ref(ref)
        item['target_primary'] = symbol_info(symbols.getPrimarySymbol(ref.getToAddress()), False)
        result['references_from'].append(item)
    result['references_to'] = [basic_ref(ref) for ref in references.getReferencesTo(addr)]
    return result


def function_state(value, extended=False):
    fn = getFunctionAt(toAddr(value))
    if fn is None:
        return None
    symbol = fn.getSymbol()
    values, eols, body_refs = [], [], []
    iterator = fn.getBody().getAddresses(True)
    while iterator.hasNext():
        pos = iterator.next()
        values.append(chr(memory.getByte(pos) & 255))
        eol = listing.getComment(CodeUnit.EOL_COMMENT, pos)
        if eol is not None:
            eols.append([str(pos), unicode(eol)])
        body_refs.extend(basic_ref(ref) for ref in references.getReferencesFrom(pos))
    text = listing.getComment(CodeUnit.PLATE_COMMENT, fn.getEntryPoint())
    result = {'plate_chars': 0 if text is None else len(text),
              'incoming': [basic_ref(ref) for ref in references.getReferencesTo(fn.getEntryPoint())],
              'plate_sha256': None if text is None else hashlib.sha256(unicode(text).encode('utf8')).hexdigest(),
              'body_sha256': hashlib.sha256(''.join(values)).hexdigest(),
              'plate': None if text is None else unicode(text),
              'source': str(symbol.getSource()), 'body': str(fn.getBody()),
              'body_size': fn.getBody().getNumAddresses(), 'name': unicode(fn.getName()),
              'symbol_type': str(symbol.getSymbolType()), 'addr': value,
              'symbol_id': long(symbol.getID()), 'eols': eols}
    if extended:
        result['body_refs'] = body_refs
        result['prototype'] = unicode(fn.getPrototypeString(True, True))
    return result


def mode_at(value):
    mode = context.getValue(tmode, toAddr(value), False)
    return None if mode is None else int(mode)


def instruction_state(value):
    addr = toAddr(value)
    unit = listing.getCodeUnitAt(addr)
    ins = getInstructionAt(addr)
    fn = getFunctionContaining(addr)
    data = listing.getDefinedDataAt(addr)
    if unit is None:
        return None
    raw = ''.join('%02x' % (memory.getByte(addr.add(index)) & 255) for index in range(unit.getLength()))
    state = {'tmode': mode_at(value), 'address': value,
             'eol': None if listing.getComment(CodeUnit.EOL_COMMENT, addr) is None else unicode(listing.getComment(CodeUnit.EOL_COMMENT, addr)),
             'kind': str(unit.getClass().getSimpleName()), 'length': unit.getLength(),
             'references_to': [basic_ref(ref) for ref in references.getReferencesTo(addr)],
             'references_from': [basic_ref(ref) for ref in references.getReferencesFrom(addr)],
             'plate': None if listing.getComment(CodeUnit.PLATE_COMMENT, addr) is None else unicode(listing.getComment(CodeUnit.PLATE_COMMENT, addr)),
             'bytes': raw, 'instruction': None,
             'function': None if fn is None else str(fn.getEntryPoint()),
             'defined_data': None if data is None else unicode(data.getDataType().getPathName())}
    if ins is not None:
        state['instruction'] = {'operands': [unicode(ins.getDefaultOperandRepresentation(index)) for index in range(ins.getNumOperands())],
                                'flow_type': str(ins.getFlowType()),
                                'flows': [str(target) for target in ins.getFlows()],
                                'mnemonic': unicode(ins.getMnemonicString()),
                                'text': unicode(str(ins)),
                                'fallthrough': None if ins.getFallThrough() is None else str(ins.getFallThrough())}
    return state


def raw_hash(start, end):
    raw = ''.join(chr(memory.getByte(toAddr(value)) & 255) for value in range(start, end))
    return hashlib.sha256(raw).hexdigest()


def range_hash():
    return raw_hash(SEGMENT_START, SEGMENT_END)


def block_state():
    start, end, expected_hash, classification = BLOCK_GUARD
    return {'status': 'READ_ONLY_CODE_OBSERVATION_COMPLETE', 'start': start, 'end': end,
            'byte_count': end - start, 'sha256': raw_hash(start, end),
            'function_count': currentProgram.getFunctionManager().getFunctionCount(),
            'units': [instruction_state(item['address']) for item in ROOT_BLOCK['units']]}


PLAN = read_json('f13-seg4-plan.json')
ROOT_SLOTS = read_json('f13-seg4-slots-before.json')
ROOT_FUNCTIONS = read_json('f13-seg4-functions-before.json')
ROOT_BLOCK = read_json('f13-seg4-block-code-before.json')
SCRIPT_HASH = file_hash(getSourceFile().getAbsolutePath())
SLOTS = dict((row['slot'], row) for row in PLAN['actions'])
PLATE_MAP = dict((addr, text) for addr, name, text in PLATES)
EOL_MAP = dict(SLOT_EOLS)
REF_TARGETS = dict((slot, (target, name)) for slot, target, name, label in REF_SLOTS)
NEW_NAMES = set(name for name, value, path in NEW_DEFINITIONS)
TARGET_ADDRESSES = sorted(set([target for slot, target, name, label in REF_SLOTS] +
                              [row['value'] for row in PLAN['actions'] if row['action'] == 'RENAME']))

SLOT_BASE = dict((item['address'], canonical(item)) for item in ROOT_SLOTS['slots'])
TARGET_BASE = dict((item['address'], canonical(item)) for item in ROOT_SLOTS['extra_targets']
                   if item['address'] in TARGET_ADDRESSES)
require(set(SLOT_BASE) == set(SLOTS), 'ROOT_SLOT_SET')
require(set(TARGET_BASE) == set(TARGET_ADDRESSES), 'ROOT_TARGET_SET')

TARGET_LABEL_AFTER = {}
EFFECT_ENTRY_USER_ID = None
for target in TARGET_ADDRESSES:
    old_symbols = TARGET_BASE[target]['symbols']
    desired_names = set(row['target'] for row in PLAN['actions']
                        if row.get('value') == target and row['action'] in ('REF', 'RENAME'))
    require(len(desired_names) == 1, 'TARGET_NAME_SET %08x' % target)
    desired = list(desired_names)[0]
    if target == EFFECT_ENTRY_ARRAY:
        require(len(old_symbols) == 1 and old_symbols[0]['primary'] and old_symbols[0]['source'] == 'DEFAULT' and
                old_symbols[0]['name'] == 'DAT_0201b590', 'EFFECT_ENTRY_SYMBOL_PRE')
        item = copy.deepcopy(old_symbols[0])
        item['name'] = desired
        item['qualified_name'] = desired
        item['source'] = 'USER_DEFINED'
        item['id'] = 0
        TARGET_LABEL_AFTER[target] = item
    else:
        matches = [item for item in old_symbols if item['name'] == desired and item['source'] == 'USER_DEFINED' and item['primary']]
        require(len(matches) == 1, 'TARGET_USER_SYMBOL %08x' % target)
        TARGET_LABEL_AFTER[target] = copy.deepcopy(matches[0])

NEW_SLOT_IDS = set(SLOTS)


def memory_target(ref):
    try:
        return int(ref['to'], 16)
    except (ValueError, TypeError):
        return None


def planned_ref(source, target, navigation=False):
    result = {'from': '%08x' % source, 'to': '%08x' % target, 'operand': 0,
              'type': 'DATA', 'source': 'USER_DEFINED', 'primary': True}
    if navigation:
        item = copy.deepcopy(TARGET_LABEL_AFTER[target])
        item.pop('primary', None)
        result['target_primary'] = item
    return result


def expected_after(addr):
    if addr in SLOT_BASE:
        result = copy.deepcopy(SLOT_BASE[addr])
        row = SLOTS[addr]
        result['symbols'] = [{'id': 0, 'name': row['slot_label'], 'qualified_name': row['slot_label'],
                              'source': 'USER_DEFINED', 'type': 'Label', 'primary': True}]
        result['comments']['EOL'] = row['eol']
        if row['action'] == 'EQ':
            result['equates'] = [{'name': row['constant'], 'value': row['value']}]
        elif row['action'] == 'REF':
            result['references_from'].append(planned_ref(addr, row['value'], True))
        elif row['action'] != 'RENAME':
            fail('UNKNOWN_ACTION %08x' % addr)
        for ref in result['references_from']:
            target = memory_target(ref)
            if target in TARGET_LABEL_AFTER:
                item = copy.deepcopy(TARGET_LABEL_AFTER[target])
                item.pop('primary', None)
                ref['target_primary'] = item
        return canonical(result)
    result = copy.deepcopy(TARGET_BASE[addr])
    result['symbols'] = [copy.deepcopy(TARGET_LABEL_AFTER[addr])]
    for slot, (target, name) in REF_TARGETS.items():
        if target == addr:
            result['references_to'].append(planned_ref(slot, target, False))
    return canonical(result)


def normalize_new_ids(state):
    global EFFECT_ENTRY_USER_ID
    result = copy.deepcopy(state)
    addr = result['address']
    if addr in NEW_SLOT_IDS:
        for symbol in result['symbols']:
            if symbol['name'] == SLOTS[addr]['slot_label']:
                require(symbol['id'] > 0, 'NEW_SLOT_ID %08x' % addr)
                symbol['id'] = 0
    if addr == EFFECT_ENTRY_ARRAY:
        require(EFFECT_ENTRY_USER_ID is not None, 'EFFECT_ENTRY_ID_NOT_CAPTURED')
        require(len(result['symbols']) == 1 and result['symbols'][0]['id'] == EFFECT_ENTRY_USER_ID,
                'EFFECT_ENTRY_NORMALIZE_SYMBOL')
        if len(result['symbols']) == 1:
            result['symbols'][0]['id'] = 0
    for ref in result.get('references_from', []):
        if memory_target(ref) == EFFECT_ENTRY_ARRAY and ref.get('target_primary') is not None:
            require(EFFECT_ENTRY_USER_ID is not None and
                    ref['target_primary']['id'] == EFFECT_ENTRY_USER_ID,
                    'EFFECT_ENTRY_NORMALIZE_NAV %08x' % addr)
            ref['target_primary']['id'] = 0
    return canonical(result)


def require_final_effect_symbol():
    global EFFECT_ENTRY_USER_ID
    addr = toAddr(EFFECT_ENTRY_ARRAY)
    frozen_id = TARGET_BASE[EFFECT_ENTRY_ARRAY]['symbols'][0]['id']
    at_addr = list(symbols.getSymbols(addr))
    primary = symbols.getPrimarySymbol(addr)
    require(len(at_addr) == 1 and primary is not None and at_addr[0].isPrimary() and
            long(at_addr[0].getID()) == long(primary.getID()), 'EFFECT_ENTRY_UNIQUE_PRIMARY')
    if len(at_addr) != 1 or primary is None:
        return None
    symbol = at_addr[0]
    actual_id = long(symbol.getID())
    require(symbol.getAddress() == addr and symbol.getSymbolType() == SymbolType.LABEL and
            not symbol.isDynamic() and unicode(symbol.getName()) == 'gEffectEntryArray' and
            str(symbol.getSource()) == 'USER_DEFINED' and actual_id > 0 and actual_id != frozen_id,
            'EFFECT_ENTRY_FINAL_SYMBOL')
    if EFFECT_ENTRY_USER_ID is None:
        EFFECT_ENTRY_USER_ID = actual_id
    else:
        require(actual_id == EFFECT_ENTRY_USER_ID, 'EFFECT_ENTRY_FINAL_ID_STABLE')
    return symbol


def verify_literal_tables():
    expected_eq = [(row['slot'], row['value'], row['constant'], row['slot_label'])
                   for row in PLAN['actions'] if row['action'] == 'EQ']
    expected_ref = [(row['slot'], row['value'], row['target'], row['slot_label'])
                    for row in PLAN['actions'] if row['action'] == 'REF']
    expected_rename = [(row['slot'], row['slot_label'], row['eol'])
                       for row in PLAN['actions'] if row['action'] == 'RENAME']
    expected_plates = [(row['addr'], row['name'], row['new_plate']) for row in PLAN['functions']]
    expected_eols = [(row['slot'], row['eol']) for row in PLAN['actions']]
    expected_new = [(row['name'], row['value'], row['file']) for row in PLAN['new_constants']]
    expected_block = (PLAN['block']['range'][0], PLAN['block']['range'][1],
                      PLAN['block']['sha256'], PLAN['block']['classification'])
    same('TABLE_EQ', EQ_SLOTS, expected_eq)
    same('TABLE_REF', REF_SLOTS, expected_ref)
    same('TABLE_RENAME', RENAME_SLOTS, expected_rename)
    same('TABLE_PLATE', PLATES, expected_plates)
    same('TABLE_EOL', SLOT_EOLS, expected_eols)
    same('TABLE_FUNC_RENAME', FUNC_RENAME, PLAN['function_renames'])
    same('TABLE_NEW', NEW_DEFINITIONS, expected_new)
    same('TABLE_BLOCK', BLOCK_GUARD, expected_block)
    require((len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATES), len(SLOT_EOLS),
             len(FUNC_RENAME), len(NEW_DEFINITIONS)) == (34, 16, 7, 7, 57, 0, 8), 'COUNTS')
    require(len(SLOTS) == 57 and set(EOL_MAP) == set(SLOTS), 'SLOT_UNION')
    require(BLOCK_GUARD[0:2] == (0x080a0b20, 0x080a1338) and
            BLOCK_GUARD[1] - BLOCK_GUARD[0] == 2072 and BLOCK_GUARD[3] == 'section_5_1', 'BLOCK_BOUND')
    for addr, name, text in PLATES:
        require(all(ord(char) < 128 for char in text) and len(text) <= 500, 'ASCII_PLATE %08x' % addr)
    for addr, text in SLOT_EOLS:
        require(all(ord(char) < 128 for char in text), 'ASCII_EOL %08x' % addr)
    for row in PLAN['actions']:
        base = SLOT_BASE[row['slot']]
        for key, value in row['before'].items():
            same('PLAN_BEFORE_%s %08x' % (key, row['slot']), base.get(key), value)


def require_name(name, addr, post=False):
    matches = list(symbols.getGlobalSymbols(name))
    require(all(item.getAddress() == toAddr(addr) for item in matches), 'NAME_COLLISION ' + name)
    if post:
        require(len(matches) == 1, 'NAME_COUNT ' + name)
    else:
        require(len(matches) == 0, 'NEW_NAME_PREEXISTS ' + name)


def verify_names_and_equates(post=False):
    for addr, value, name, label in EQ_SLOTS:
        eq = equates.getEquate(name)
        require(eq is None or (eq.getValue() & 0xffffffff) == value, 'EQUATE_VALUE ' + name)
        if name in NEW_NAMES and not post:
            require(eq is None, 'NEW_EQUATE_PREEXISTS ' + name)
        if post:
            refs = [ref for ref in eq.getReferences()
                    if ref.getAddress() == toAddr(addr) and ref.getOpIndex() == 0] if eq is not None else []
            require(eq is not None and len(refs) == 1, 'EQUATE_REFERENCE %08x' % addr)
    for row in PLAN['actions']:
        require_name(row['slot_label'], row['slot'], post)
    for target in TARGET_ADDRESSES:
        desired = TARGET_LABEL_AFTER[target]
        matches = list(symbols.getGlobalSymbols(desired['name']))
        if post:
            require(len(matches) == 1 and matches[0].getAddress() == toAddr(target), 'TARGET_NAME_POST %08x' % target)
            if target == EFFECT_ENTRY_ARRAY:
                effect_symbol = require_final_effect_symbol()
                require(effect_symbol is not None and len(matches) == 1 and
                        long(matches[0].getID()) == EFFECT_ENTRY_USER_ID,
                        'EFFECT_ENTRY_GLOBAL_POST')
            else:
                require(long(matches[0].getID()) == desired['id'], 'TARGET_ID_POST %08x' % target)
        elif target == EFFECT_ENTRY_ARRAY:
            require(len(matches) == 0, 'EFFECT_ENTRY_NAME_PREEXISTS')
        else:
            require(len(matches) == 1 and long(matches[0].getID()) == desired['id'], 'TARGET_ID_PRE %08x' % target)


def verify_addresses(post=False):
    result = []
    for addr in sorted(list(SLOT_BASE) + list(TARGET_BASE)):
        actual = describe(addr)
        expected = expected_after(addr) if post else (SLOT_BASE.get(addr) or TARGET_BASE[addr])
        normalized = normalize_new_ids(actual) if post else canonical(actual)
        if normalized != canonical(expected):
            keys = [key for key in expected if canonical(expected[key]) != canonical(normalized.get(key))]
            fail('%s_ADDRESS %08x fields=%s' % ('POST' if post else 'PRE', addr, ','.join(keys)))
            write_json('f13-seg4-mismatch-%s-%08x.json' % (MODE, addr),
                       {'expected': expected, 'actual': actual, 'normalized': normalized})
        result.append(actual)
    return result


def verify_functions(post=False, before=None):
    require(currentProgram.getFunctionManager().getFunctionCount() == 5209, 'FUNCTION_COUNT_5209')
    old_by_addr = dict((item['addr'], item) for item in ROOT_FUNCTIONS['functions'])
    plan_by_addr = dict((item['addr'], item) for item in PLAN['functions'])
    result = []
    for addr in sorted(old_by_addr):
        old = old_by_addr[addr]
        actual = function_state(addr, True)
        require(actual is not None, 'FUNCTION_MISSING %08x' % addr)
        if actual is None:
            continue
        for key in ('symbol_id', 'source', 'symbol_type', 'body', 'body_size', 'body_sha256', 'name', 'incoming', 'eols'):
            same('FUNCTION_%s %08x' % (key, addr), actual[key], old[key])
        expected_plate = plan_by_addr[addr]['new_plate'] if post else old['plate']
        same('FUNCTION_PLATE %08x' % addr, actual['plate'], expected_plate)
        if not post:
            require(actual['plate_sha256'] == plan_by_addr[addr]['old_plate_sha256'], 'OLD_PLATE_HASH %08x' % addr)
        if post and before is not None:
            frozen = before[addr]
            same('FUNCTION_BODY_REFS %08x' % addr, actual['body_refs'], frozen['body_refs'])
            same('FUNCTION_PROTOTYPE %08x' % addr, actual['prototype'], frozen['prototype'])
        result.append(actual)
    return result


def verify_block():
    state = block_state()
    same('BLOCK_FULL_STATE', state, ROOT_BLOCK)
    require(state['byte_count'] == 2072 and state['sha256'] == BLOCK_GUARD[2] and
            len(state['units']) == 2072, 'BLOCK_SIZE_HASH')
    for row in state['units']:
        require(row['kind'] == 'DataDB' and row['length'] == 1 and row['tmode'] == 0 and
                row['instruction'] is None and row['function'] is None and row['defined_data'] is None and
                row['references_from'] == [] and row['references_to'] == [] and
                row['eol'] is None and row['plate'] is None, 'BLOCK_DATAB1 %08x' % row['address'])
    return state


def verify_prestate():
    same('SEGMENT_RANGE_SHA_PRE', range_hash(), SEGMENT_RANGE_SHA256)
    verify_names_and_equates(False)
    addresses = verify_addresses(False)
    functions = verify_functions(False)
    block = verify_block()
    print('PREFLIGHT addresses=%d functions=%d block_bytes=%d slots=57 EQ=34 REF=16 RENAME=7 PLATE=7 EOL=57 NEW=8 FAIL=%d' %
          (len(addresses), len(functions), block['byte_count'], len(FAILS)))


def ensure_target_label(target, name):
    addr = toAddr(target)
    expected = TARGET_LABEL_AFTER[target]
    if target == EFFECT_ENTRY_ARRAY:
        frozen = TARGET_BASE[target]['symbols'][0]
        primary = symbols.getPrimarySymbol(addr)
        at_addr = list(symbols.getSymbols(addr))
        old_state = (len(at_addr) == 1 and primary is not None and primary.isPrimary() and
                     at_addr[0].isPrimary() and long(at_addr[0].getID()) == frozen['id'] and
                     long(primary.getID()) == frozen['id'] and primary.getAddress() == addr and
                     primary.getSymbolType() == SymbolType.LABEL and primary.isDynamic() and
                     unicode(primary.getName()) == frozen['name'] and
                     str(primary.getSource()) == frozen['source'])
        final_state = (len(at_addr) == 1 and primary is not None and primary.isPrimary() and
                       at_addr[0].isPrimary() and long(at_addr[0].getID()) == long(primary.getID()) and
                       primary.getAddress() == addr and primary.getSymbolType() == SymbolType.LABEL and
                       not primary.isDynamic() and unicode(primary.getName()) == name and
                       str(primary.getSource()) == 'USER_DEFINED' and long(primary.getID()) > 0 and
                       long(primary.getID()) != frozen['id'])
        require(old_state or final_state, 'EFFECT_ENTRY_STATE')
        if FAILS:
            raise RuntimeError('Effect-entry object precondition failed')
        if old_state:
            primary.setName(name, SourceType.USER_DEFINED)
        symbol = require_final_effect_symbol()
        if FAILS or symbol is None:
            raise RuntimeError('Effect-entry final symbol check failed')
    else:
        symbol = symbols.getGlobalSymbol(name, addr)
        require(symbol is not None and long(symbol.getID()) == expected['id'] and symbol.isPrimary(),
                'TARGET_EXISTING_OBJECT %08x' % target)
        if FAILS:
            raise RuntimeError('Target object precondition failed')
    require(len(list(symbols.getSymbols(addr))) == 1, 'TARGET_NO_ALIAS %08x' % target)
    return symbol


def ensure_slot_label(value, name):
    addr = toAddr(value)
    existing = symbols.getGlobalSymbol(name, addr)
    if existing is None:
        existing = symbols.createLabel(addr, name, SourceType.USER_DEFINED)
    require(existing.getSymbolType() == SymbolType.LABEL and existing.getAddress() == addr,
            'SLOT_LABEL_TYPE %08x' % value)
    expected_ids = set(item['id'] for item in SLOT_BASE[value]['symbols'])
    for old in list(symbols.getSymbols(addr)):
        if old.getID() == existing.getID():
            continue
        if old.getID() in expected_ids and str(old.getSource()) == 'DEFAULT' and old.getSymbolType() == SymbolType.LABEL:
            old.delete()
        else:
            raise RuntimeError('Unexpected slot alias at %08x' % value)
    existing.setPrimary()
    return existing


def apply_ref(row):
    addr, target = toAddr(row['slot']), toAddr(row['value'])
    ensure_target_label(row['value'], row['target'])
    old_refs = list(references.getReferencesFrom(addr))
    if old_refs:
        raise RuntimeError('REF prestate not empty at %08x' % row['slot'])
    ref = references.addMemoryReference(addr, target, RefType.DATA, SourceType.USER_DEFINED, 0)
    references.setPrimary(ref, True)


def apply_slot(row):
    addr = row['slot']
    if row['action'] == 'EQ':
        eq = equates.getEquate(row['constant'])
        if eq is None:
            eq = equates.createEquate(row['constant'], row['value'])
        eq.addReference(toAddr(addr), 0)
    elif row['action'] == 'REF':
        apply_ref(row)
    elif row['action'] != 'RENAME':
        raise RuntimeError('Unknown slot action %08x' % addr)
    ensure_slot_label(addr, row['slot_label'])
    listing.setComment(toAddr(addr), CodeUnit.EOL_COMMENT, row['eol'])
    COUNTS[row['action']] += 1
    COUNTS['EOL'] += 1


def apply_all():
    events = [(addr, 0, 'PLATE') for addr, name, text in PLATES]
    events.extend((addr, 1, 'SLOT') for addr in SLOTS)
    for addr, order, kind in sorted(events):
        if kind == 'PLATE':
            listing.setComment(toAddr(addr), CodeUnit.PLATE_COMMENT, PLATE_MAP[addr])
            COUNTS['PLATE'] += 1
        else:
            apply_slot(SLOTS[addr])


def verify_post(before):
    same('SEGMENT_RANGE_SHA_POST', range_hash(), SEGMENT_RANGE_SHA256)
    verify_names_and_equates(True)
    verify_addresses(True)
    frozen_functions = dict((item['addr'], item) for item in before['functions'])
    verify_functions(True, frozen_functions)
    verify_block()
    require(currentProgram.getFunctionManager().getFunctionCount() == 5209, 'FUNCTION_COUNT_POST')
    print('POSTCHECK slots=57 EQ=34 REF=16 RENAME=7 PLATE=7 EOL=57 FUNC_RENAME=0 BLOCK_PRESERVED=2072 NEW=8 FAIL=%d' % len(FAILS))


def capture():
    return {'script_sha256': SCRIPT_HASH, 'input_hashes': [list(row) for row in INPUT_HASHES],
            'function_count': currentProgram.getFunctionManager().getFunctionCount(),
            'range_sha256': range_hash(),
            'addresses': [describe(addr) for addr in sorted(list(SLOT_BASE) + list(TARGET_BASE))],
            'functions': [function_state(item['addr'], True) for item in ROOT_FUNCTIONS['functions']],
            'block': block_state()}


def reject(phase):
    if FAILS:
        write_json('f13-seg4-%s-failures.json' % MODE, {'phase': phase, 'FAIL': len(FAILS), 'failures': FAILS})
        raise RuntimeError('%s FAIL=%d' % (phase, len(FAILS)))


print('=== RefineF13Seg4 mode=%s ===' % MODE)
for relative, expected_hash in INPUT_HASHES:
    require(file_hash(os.path.join(ROOT, relative)) == expected_hash, 'INPUT_HASH ' + relative)
verify_literal_tables()
reject('FROZEN_TABLES')
if MODE == 'check':
    receipt = read_json('f13-seg4-apply-receipt.json')
    require(receipt['script_sha256'] == SCRIPT_HASH, 'PERSISTED_SCRIPT_HASH')
    require(receipt['input_hashes'] == [list(row) for row in INPUT_HASHES], 'PERSISTED_INPUT_HASHES')
    state = capture()
    verify_post(receipt['before'])
    require(canonical(state) == canonical(receipt['after']), 'PERSISTED_EXACT_POST_STATE')
    reject('PERSISTED_CHECK')
    COUNTS = receipt['counts']
    write_json('f13-seg4-persisted-check.json', {'status': 'PERSISTED_CHECK_OK', 'FAIL': 0,
               'script_sha256': SCRIPT_HASH, 'counts': COUNTS, 'exact_saved_state': True,
               'block_preserved_bytes': 2072})
else:
    verify_prestate()
    reject('PREFLIGHT')
    before = capture()
    if MODE == 'dry':
        write_json('f13-seg4-dry-state.json', before)
        COUNTS.update({'EQ': 34, 'REF': 16, 'RENAME': 7, 'PLATE': 7, 'EOL': 57, 'FUNC_RENAME': 0})
        write_json('f13-seg4-dry-check.json', {'status': 'DRY_PREFLIGHT_OK', 'FAIL': 0,
                   'script_sha256': SCRIPT_HASH, 'input_hashes': [list(row) for row in INPUT_HASHES],
                   'counts': COUNTS, 'address_count': len(before['addresses']),
                   'function_count': len(before['functions']), 'new_definitions': 8,
                   'block_preserved_bytes': 2072, 'complete_state': 'f13-seg4-dry-state.json'})
    else:
        write_json('f13-seg4-apply-before.json', before)
        transaction = currentProgram.startTransaction('Refine F13-Seg-4 final PASS actions')
        success = False
        after = None
        try:
            apply_all()
            verify_post(before)
            reject('POSTCHECK')
            after = capture()
            success = True
        finally:
            currentProgram.endTransaction(transaction, success)
        write_json('f13-seg4-apply-receipt.json', {'status': 'APPLIED_TRANSACTION_POSTCHECK_OK',
                   'FAIL': 0, 'script_sha256': SCRIPT_HASH, 'input_hashes': [list(row) for row in INPUT_HASHES],
                   'counts': COUNTS, 'before': before, 'after': after})
reject('FINAL')
print('COUNTS ' + ' '.join('%s=%d' % (key, COUNTS[key]) for key in ('EQ', 'REF', 'RENAME', 'PLATE', 'EOL', 'FUNC_RENAME')))
print('STATUS: OK mode=%s FAIL=0' % MODE)
