# -*- coding: ascii -*-
#@runtime Jython
#@category Ygo-ex2006
# Historical closure: reviewed slots/comments and exactly three instructions.
# Usage: RefineF12HistoricalClosure.py dry|apply|check
import copy
import hashlib
import json
import os
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import SourceType, RefType, SymbolType
from ghidra.program.model.address import AddressSet
from ghidra.app.cmd.disassemble import DisassembleCommand

# Proposal SHA256: 74f49b4e0cddffe0a66dd2c0a073fe28c555a6d60d89c979bb9796aa58a5ae11
EQ_SLOTS = []

REF_SLOTS = [(134829392, 134829396, 'switchD_0809554c__switchdataD_08095554', 'sprite_row_tbl2_95550'),
 (134829660, 33667184, 'gSpriteAttrBuf', 'gsprattrb_9565c')]

RENAME_SLOTS = [(134828672, 'eligib_act_type_95280', 'Byte offset from gP1LifePoints; steps8/9 load the activation type as u16.'),
 (134828748,
  'eligib_anim_state_952cc',
  'Byte offset from gP1LifePoints; step3 reads the animation state for the 11..15 split.'),
 (134828752,
  'eligib_sprite_ctrl_952d0',
  'Byte offset from gP1LifePoints; step3 states12..15 load the sprite-control argument.'),
 (134828840,
  'eligib_sprite_ctrl_95328',
  'Byte offset from gP1LifePoints; step1 reads sprite control for display-context initialization.'),
 (134828844,
  'eligib_anim_state_9532c',
  'Byte offset from gP1LifePoints; step1 passes animation state minus11 to context initialization.'),
 (134828848,
  'eligib_state_ctrl_95330',
  'Byte offset from gP1LifePoints; step1 clears state control through the shared store path.')]

EXTRA_EOL = [(134829392,
  '32-entry even-address type table at 0x08095554, indexed by type0..31; dispatch uses MOV pc,r0 and stays in Thumb '
  'state.'),
 (134829660, 'Sprite attribute buffer base; type0x17 sets bit1 of byte[base+0x300].')]

PLATES = [(134824592,
  'get_clamped_tile_row_count',
  'No inputs. Read signed phase at gEquipEffectZoneBase+4. Return 0 if phase<=5. Otherwise start with n=1; phase 7..38 '
  'sets n=phase-6, and phase 40..71 sets n=phase-39. Return unsigned min(n,word[base+0xc]). Thus phase 6,39 and values '
  'above71 use n=1. Pure read; no bounds-state writes.'),
 (134824668,
  'get_monster_slot_entry_ptr',
  'No inputs. Read index=word[gEquipEffectZoneBase+8] and return gEquipEffectZoneBase+0x10+4*index. Does not '
  'dereference the selected entry, increment the index or check bounds. Pure address calculation.'),
 (134824684,
  'get_effect_slot_entry_ptr',
  'r0=slot index. Return gEquipLpZoneEntryBase+4*index using 32-bit address arithmetic. The selected entry is not '
  'dereferenced and the index is not range-checked. No memory writes.'),
 (134824724,
  'get_duel_activation_zone_id',
  'No inputs. Return the u32 at gEquipEffectZoneBase+0xc. Three-instruction leaf with no writes; the base comes from '
  'the existing gEquipEffectZoneBase literal. Used by activation-zone display callers.'),
 (134825316,
  'read_slot_palette_index',
  'r0=slot index. Return the high byte of the halfword at gEquipEffectZoneBase+0x410+2*index, as an unsigned value '
  '0..255. No bounds check or memory write. Used by reset_slots_above_palette_index and check_slot_palette_nonzero.'),
 (134825532,
  'advance_prng_state',
  'No inputs. Advance the u32 seed at gP1LifePoints+0x1ce0: seed=seed*LCG_MUL_343FD+LCG_INC_269EC3 modulo 2^32. Store '
  'the new seed and return (seed>>16)&0x7fff, in range0..32767. Modifies only the seed word. Direct callers are the '
  'scaling wrapper and two random-draw/display sequence functions.'),
 (134825572,
  'sample_prng_scaled',
  'r0=scale. Call advance_prng_state, multiply its 15-bit result by scale using a 32-bit product, then return '
  'product>>15. No input range check; multiplication can wrap for large scale. Advances the shared seed. For positive '
  'scale with no product overflow, result is below scale.'),
 (134825720,
  'enqueue_duel_phase_sprite_by_side',
  'No inputs. If gP1LifePoints+P1LP_BACKUP_DST_OFF is not 0xffff, return. Also return when check_player_side_condition '
  'is nonzero. Otherwise copy the timer at P1LP_TIMER_OFF to the backup word and enqueue sprite type 0xb or '
  'SPRITE_ATTR_DUEL_PHASE_P2 according to gDuelCardCtxBase+4 being zero or nonzero. The other three enqueue arguments '
  'are zero. Returns void.'),
 (134825808,
  'init_duel_phase_display_flag_with_sprite',
  'r0=player. Return if word[gP1LifePoints+LP_DISCARD_ZONE_OFF] is nonzero; otherwise set it to1. Store display '
  'variant2 if player equals word[gDuelCardCtxBase+4], else1. Enqueue type0x23 for player0 or '
  'SPRITE_ATTR_DUEL_PHASE_P2_B otherwise, with remaining arguments (0xb,0,0). Writes the guard and variant once; '
  'returns void.'),
 (134827024,
  'poll_sprite_seq_until_done',
  'r0 is saved as a loop-continuation flag. The first call is return_one_leaf, which returns1 in this ROM, so this '
  'entry immediately returns without reading a frame or writing the sprite sequence. The dormant loop would read four '
  'halfwords from return_zero_leaf, submit them, and test the saved flag only after that work. The supplied flag is '
  'not an initial null-pointer guard. Returns void.'),
 (134827104,
  'tick_equip_activation_dispatch_hub',
  'No inputs. Check Last Turn in current-player zone0xb; if present and the subphase dispatcher returns0, return0. '
  'Otherwise index EQUIP_PHASE_FN_TABLE_ROM by the shared main phase. A null function pointer returns1. Invoke a '
  'nonnull pointer; on nonzero result clear CARD_PLAY_PHASE_CTR_OFF and increment main phase. All nonnull-pointer '
  'paths return0. No player-stride multiplication precedes the chain query.'),
 (134827220,
  'tick_equip_activation_main_sequence',
  'No inputs. Return1 for context mode3, active sprite-busy gate or discard guard. Run six UI/target/confirm update '
  'checks until one returns nonzero; store (result==0) at gP1LifePoints+0x1d10. Nonzero returns0. On zero, a nonzero '
  'normal-summon check returns1; otherwise call tick_equip_slot_activation_step for player context2, or '
  'tick_equip_activation_dispatch_hub, and return0. Both final call results are ignored.'),
 (134827436,
  'advance_duel_turn_by_prng_anim',
  'No inputs. Index DUEL_TURN_FN_TABLE_ROM by shared turn state. A null entry copies display variant and the selected '
  'player word into duel context, then returns1. For a nonnull entry, a required PRNG-animation step returning0 '
  'returns1; a nonzero animation-event result returns0. Otherwise invoke the entry; a nonzero result advances turn '
  'state and clears the card-play counter. This dispatch path returns0.'),
 (134827888,
  'update_card_display_index_by_type_rules',
  'r0=24-byte card entry; r1=entry index (>0 enables the previous-entry test). Require entry side XOR its flip bit to '
  'equal current player. Field6=23 writes index0x3a, then0x21 if flags0x30 are clear; field9==1 plus '
  'prior-entry/CID/entity tests enable0x22. Field6=22 writes0x39, then0x1f when those flags are clear; opposite cached '
  'player and field9==5 enable0x20. All writes use value1. Returns void; caller supplies the index from '
  'gSpriteAttrBuf+0x310.'),
 (134828576,
  'dispatch_equip_confirm_phase_by_step',
  'No inputs. Read ELIGIB_ACT_TYPE_OFF from gP1LifePoints; steps1..10 select ten even-address cases via MOV pc,r0. '
  'Other steps clear ELIGIB_STATE_CTRL_OFF. Cases initialize/tick equip display using the shared entry frame. In '
  'step3, animation state outside11..15 calls init_equip_card_sprite_row_entry(0); state11 and12..15 use distinct '
  'paths. All cases return through the saved r4/lr epilogue at 0x0809533c; no extra callback frame.'),
 (134828928,
  'pack_sprite_row_attr_words',
  'r0-r3 supply four low16 fields. Build two local words: low16(r0)|(r1<<16) and low16(r2)|(r3<<16). Submit them with '
  'submit_sprite_row_data(low16(r0),-1,sp+2,6), then restore the local stack and forward its r0 result. The sp+4 '
  'intermediate is masked twice so no old stack bits survive. The pointer sp+2 is not an input stride or fifth '
  'argument.'),
 (134829288,
  'step_prng_anim_frame',
  'No inputs. If gSpriteAttrBuf+0x300 bit0 is set, return1. Otherwise dequeue a record; a nonzero result dispatches '
  'its type through32 even-address MOV pc cases. Cases update sprite/effect/LP state; most return1, while type1,4,5 or '
  'out-of-range type set LP_DISPLAY_STATE_OFF=1 and return0. With no record, return1 only when '
  'read_prng_entry_flag_clear is nonzero and LP display state is zero; otherwise set that state to1 and return0.'),
 (134836560,
  'dispatch_to_effect_handler_by_card_type',
  'r0=context; r1=type key; r2=sub-parameter. Scan18 records in EQUIP_ACTIVATION_HANDLER_TABLE, indices0..17 with '
  'stride0x10. Compare the full r1 word to record+0. On the first match invoke the function pointer at record+0xc with '
  'the original (context,type,sub-parameter), then return. No match returns without dispatch. No key truncation or '
  'handler-null check. Returns void.'),
 (134837628,
  'refresh_slot_activation_display_if_changed',
  'No inputs. Build a 0x44-byte slot-state image and compare with gEquipChainSlotRefs+0xec. A mismatch in either '
  'leading word clears cached mode/chain-active, sets chain step1 and returns1. Further state, eligibility and '
  'EARTHBOUND_INVITATION_CID checks detect changes. No change returns0. On change, clear mode/chain-active; guard '
  'returning0 enqueues the slot sprite and sets step1, otherwise set step2 and request card display/slot-bit updates. '
  'Return1; this is not a cache-pointer API.')]

FUNC_RENAME = []

DISASM_INSTRUCTIONS = [(134828796, 2, '0020', 'mov', None),
 (134828798, 4, '00f053fc', 'bl', 134831016),
 (134828802, 2, '1be0', 'b', 134828860)]

FROZEN_INPUTS = [('doc/dev/refine/F12-Historical-Closure.proposal.md',
  '74f49b4e0cddffe0a66dd2c0a073fe28c555a6d60d89c979bb9796aa58a5ae11'),
 ('doc/dev/refine/F12-Historical-Closure.review.md',
  '3f90388db91a3f52d6596b19f78d9ae9b6130a176f228cab0d3b038cd2397248'),
 ('output/refine-run-20260831-194634/closure-plan.json',
  'e1b40e449d4b18b396a2c7c549ad2cbf21aff5490659a96d73763d97f0f5d816'),
 ('output/refine-run-20260831-194634/closure-plates.json',
  '9022db01ec21fd82370e3d21c9f3544ca3a25e851fca968b025c7b82e264bf89'),
 ('output/refine-run-20260831-194634/root-closure-switch-before.json',
  'fb144f2034138b36f565af79fe7008c7658cc371443d3e759945981c9b083291'),
 ('output/refine-run-20260831-194634/root-closure-functions-before.json',
  'a47351b5f6dd60b68538a66491183d0df9a1fded7698181b6e282d166e0608f0')]

MODE = list(getScriptArgs())[0].lower() if list(getScriptArgs()) else 'dry'
if MODE not in ('dry', 'apply', 'check'):
    raise RuntimeError('Expected dry|apply|check')
ROOT = os.path.abspath(os.path.join(str(getSourceFile().getParentFile()), '..', '..'))
RUN = os.path.join(ROOT, 'output', 'refine-run-20260831-194634')
listing = currentProgram.getListing()
symbols = currentProgram.getSymbolTable()
references = currentProgram.getReferenceManager()
memory = currentProgram.getMemory()
FAILS = []
COUNTS = dict((key, 0) for key in ('EQ', 'REF', 'RENAME', 'PLATE', 'EOL', 'DISASM', 'FUNC_RENAME'))


def read_json(name):
    with open(os.path.join(RUN, name), 'rb') as stream:
        return json.load(stream)


def write_json(name, data):
    with open(os.path.join(RUN, name), 'w') as stream:
        stream.write(json.dumps(data, ensure_ascii=True, sort_keys=True, indent=2) + '\n')


def fail(message, actual=None, expected=None):
    FAILS.append(message)
    print('FAIL: ' + message)
    if actual is not None or expected is not None:
        print('DETAIL ' + json.dumps({'actual': actual, 'expected': expected}, ensure_ascii=True, sort_keys=True))


def canonical(value):
    if isinstance(value, dict):
        return dict((k, canonical(v)) for k, v in value.items())
    if isinstance(value, list):
        return sorted((canonical(v) for v in value), key=lambda v: json.dumps(v, sort_keys=True))
    return value


def same(where, actual, expected):
    if canonical(actual) != canonical(expected):
        fail(where, actual, expected)


def ref_info(ref, navigation=False):
    result = {'from': str(ref.getFromAddress()), 'to': str(ref.getToAddress()),
              'operand': ref.getOperandIndex(), 'type': str(ref.getReferenceType()),
              'source': str(ref.getSource()), 'primary': bool(ref.isPrimary())}
    if navigation:
        sym = symbols.getPrimarySymbol(ref.getToAddress())
        result['target_primary'] = None if sym is None else {
            'id': long(sym.getID()), 'name': unicode(sym.getName()),
            'qualified_name': unicode(sym.getName(True)),
            'type': str(sym.getSymbolType()), 'source': str(sym.getSource())}
    return result


def describe_address(value):
    address = toAddr(value)
    data = listing.getDefinedDataAt(address)
    result = {'address': value, 'symbols': []}
    for sym in symbols.getSymbols(address):
        result['symbols'].append({'id': long(sym.getID()), 'name': unicode(sym.getName()),
            'qualified_name': unicode(sym.getName(True)), 'type': str(sym.getSymbolType()),
            'source': str(sym.getSource()), 'primary': bool(sym.isPrimary())})
    result['defined_data'] = None if data is None else {
        'address': str(data.getAddress()), 'length': data.getLength(),
        'type': unicode(data.getDataType().getPathName()),
        'min': str(data.getMinAddress()), 'max': str(data.getMaxAddress())}
    unit = listing.getCodeUnitContaining(address)
    result['containing_code_unit'] = None if unit is None else {
        'address': str(unit.getAddress()), 'length': unit.getLength(),
        'class': str(unit.getClass().getSimpleName())}
    ins = getInstructionAt(address)
    result['instruction_at'] = None if ins is None else str(ins)
    fn = getFunctionContaining(address)
    result['containing_function'] = None if fn is None else {
        'entry': str(fn.getEntryPoint()), 'name': str(fn.getName()), 'body': str(fn.getBody())}
    result['equates'] = [{'name': str(eq.getName()), 'value': long(eq.getValue())}
                        for eq in currentProgram.getEquateTable().getEquates(address)]
    result['comments'] = {}
    for key, kind in [('EOL', CodeUnit.EOL_COMMENT), ('PLATE', CodeUnit.PLATE_COMMENT)]:
        text = listing.getComment(kind, address)
        result['comments'][key] = None if text is None else unicode(text)
    result['rom_word'] = None
    if 0x08000000 <= value <= 0x09fffffc:
        result['rom_word'] = memory.getInt(address) & 0xffffffff
    result['references_from'] = [ref_info(ref, True) for ref in references.getReferencesFrom(address)]
    result['references_to'] = [ref_info(ref) for ref in references.getReferencesTo(address)]
    return result


def function_state(value):
    fn = getFunctionAt(toAddr(value))
    if fn is None:
        fail('FUNCTION_MISSING %08x' % value)
        return {}
    sym = fn.getSymbol()
    plate = listing.getComment(CodeUnit.PLATE_COMMENT, toAddr(value))
    plate = unicode(plate) if plate is not None else None
    raw, eols, body_refs = [], [], []
    iterator = fn.getBody().getAddresses(True)
    while iterator.hasNext():
        pos = iterator.next()
        raw.append(chr(memory.getByte(pos) & 255))
        eol = listing.getComment(CodeUnit.EOL_COMMENT, pos)
        if eol is not None:
            eols.append([str(pos), unicode(eol)])
        body_refs.extend(ref_info(ref) for ref in references.getReferencesFrom(pos))
    return {'addr': value, 'name': str(fn.getName()), 'symbol_id': long(sym.getID()),
            'source': str(sym.getSource()), 'symbol_type': str(sym.getSymbolType()),
            'body': str(fn.getBody()), 'body_size': fn.getBody().getNumAddresses(),
            'body_sha256': hashlib.sha256(''.join(raw)).hexdigest(),
            'plate': plate, 'plate_chars': len(plate) if plate is not None else None,
            'plate_sha256': hashlib.sha256(plate.encode('utf-8')).hexdigest() if plate is not None else None,
            'incoming': [ref_info(ref) for ref in references.getReferencesTo(toAddr(value))],
            'eols': eols, 'body_refs': body_refs}


def mode_at(value):
    mode = currentProgram.getProgramContext().getValue(currentProgram.getRegister('TMode'), toAddr(value), False)
    return None if mode is None else int(mode)


def capture():
    comments = {}
    for value in range(0x080941c4, 0x0809d718):
        for key, kind in [('EOL', CodeUnit.EOL_COMMENT), ('PLATE', CodeUnit.PLATE_COMMENT)]:
            text = listing.getComment(kind, toAddr(value))
            if text is not None:
                comments['%08x:%s' % (value, key)] = unicode(text)
    addresses = set(x['address'] for x in SOURCE_SLOTS['slots'] + SOURCE_SLOTS['extra_targets'])
    addresses.update(range(0x080952f0, 0x08095344))
    return {'function_count': currentProgram.getFunctionManager().getFunctionCount(),
            'addresses': [describe_address(value) for value in sorted(addresses)],
            'functions': [function_state(value) for value in sorted(set([p[0] for p in PLATES] + [0x08095ba8]))],
            'comments': comments,
            'module_sha256': hashlib.sha256(''.join(chr(memory.getByte(toAddr(v)) & 255)
                for v in range(0x080941c4, 0x0809d718))).hexdigest(),
            'tmode': [[v, mode_at(v)] for v in range(0x080952fc, 0x08095304)]}


def reject_if_failed(phase):
    if FAILS:
        write_json('closure-%s-failure.json' % MODE, {'phase': phase, 'fails': FAILS})
        raise RuntimeError('%s FAIL=%d' % (phase, len(FAILS)))


def verify_frozen_inputs():
    for relative, digest in FROZEN_INPUTS:
        with open(os.path.join(ROOT, relative), 'rb') as stream:
            actual = hashlib.sha256(stream.read()).hexdigest()
        same('INPUT_SHA256 ' + relative, actual, digest)
    same('COUNT_EQ', len(EQ_SLOTS), 0)
    same('COUNT_REF', len(REF_SLOTS), 2)
    same('COUNT_RENAME', len(RENAME_SLOTS), 6)
    same('COUNT_PLATE', len(PLATES), 19)
    same('COUNT_EOL', len(RENAME_SLOTS) + len(EXTRA_EOL), 8)
    same('COUNT_DISASM', len(DISASM_INSTRUCTIONS), 3)
    for addr, name, text in PLATES:
        if not text or len(text) > 500 or any(ord(ch) > 127 for ch in text):
            fail('PLATE_ASCII_LENGTH %08x' % addr)
    for addr, text in EOLS.items():
        if any(ord(ch) > 127 for ch in text):
            fail('EOL_ASCII %08x' % addr)
    for slot in PLAN['slots']:
        if slot['kind'] == 'RENAME':
            same('RENAME_TABLE %08x' % slot['addr'],
                 [slot['addr'], slot['slot_label'], slot['eol']],
                 list(next(row for row in RENAME_SLOTS if row[0] == slot['addr'])))
        else:
            same('REF_TABLE %08x' % slot['addr'],
                 [slot['addr'], slot['value'], slot['symbol'], slot['slot_label']],
                 list(next(row for row in REF_SLOTS if row[0] == slot['addr'])))
    same('PLATE_TABLE', [list(row) for row in PLATES],
         [[row['addr'], row['name'], row['text']] for row in PLAN['plates']])


def switch_namespaces(post):
    for identity, namespace, global_namespace in [(4244, 'switchD_0809554c', False), (31014, None, True)]:
        sym = symbols.getSymbol(identity)
        if sym is None:
            fail('SWITCH_EXACT_ID %d' % identity)
            continue
        same('SWITCH_ADDRESS %d' % identity, str(sym.getAddress()), '08095554')
        ns = sym.getParentNamespace()
        same('SWITCH_GLOBAL_NAMESPACE %d' % identity, bool(ns.isGlobal()), global_namespace)
        if not global_namespace:
            same('SWITCH_SCOPED_NAMESPACE %d' % identity, str(ns.getName(True)), namespace)
    expected = SWITCH_GUARD['target_expected_after' if post else 'target_expected_before']
    same('SWITCH_COMPLETE_DUAL_SYMBOLS', describe_address(0x08095554)['symbols'], expected['symbols'])


def verify_switch_words(post):
    for table in PLAN['switches']:
        same('SWITCH_MOV_PC %08x' % table['mov_pc'], memory.getShort(toAddr(table['mov_pc'])) & 0xffff, 0x4687)
        for index, value in enumerate(table['values']):
            at = table['addr'] + 4 * index
            same('SWITCH_WORD %08x' % at, memory.getInt(toAddr(at)) & 0xffffffff, value)
            same('SWITCH_EVEN %08x' % value, value & 1, 0)
            same('SWITCH_TMODE %08x' % value, mode_at(value), 1)
            if getInstructionAt(toAddr(value)) is None:
                fail('SWITCH_CASE_INSTRUCTION %08x' % value)
    switch_namespaces(post)


def verify_preflight(state):
    same('FUNCTION_COUNT', state['function_count'], 5209)
    actual_addresses = dict((x['address'], x) for x in state['addresses'])
    for old in SOURCE_SLOTS['slots'] + SOURCE_SLOTS['extra_targets']:
        expected = copy.deepcopy(old)
        expected.pop('input_label', None)
        same('PRE_ADDRESS %08x' % expected['address'], actual_addresses[expected['address']], expected)
    same('EPILOGUE_PRE', actual_addresses[0x0809533c], PLAN['disasm']['expected_epilogue'])
    by_function = dict((x['addr'], x) for x in state['functions'])
    for old in SOURCE_FUNCTIONS['functions'] + [PLAN['disasm']['expected_callee']]:
        actual = copy.deepcopy(by_function[old['addr']])
        actual.pop('body_refs', None)
        same('FUNCTION_PRE %08x' % old['addr'], actual, old)
    for at, size, raw, mnemonic, target in DISASM_INSTRUCTIONS:
        same('DISASM_RAW %08x' % at, ''.join('%02x' % (memory.getByte(toAddr(v)) & 255) for v in range(at, at + size)), raw)
    for value in range(0x080952fc, 0x08095304):
        actual = actual_addresses[value]
        same('UNDEFINED_UNIT %08x' % value, actual['containing_code_unit'],
             {'address': '%08x' % value, 'length': 1, 'class': 'DataDB'})
        same('NO_DEFINED_DATA %08x' % value, actual['defined_data'], None)
        same('NO_INSTRUCTION %08x' % value, actual['instruction_at'], None)
        same('NO_FUNCTION %08x' % value, actual['containing_function'], None)
        same('THUMB_PRE %08x' % value, mode_at(value), 1)
    for row in PLAN['slots']:
        actual = actual_addresses[row['addr']]
        same('SLOT_VALUE %08x' % row['addr'], actual['rom_word'], row['value'])
        if row['addr'] != 0x08095550:
            for sym in symbols.getGlobalSymbols(row['slot_label']):
                fail('NEW_POOL_NAME_ALREADY_EXISTS ' + row['slot_label'])
    verify_switch_words(False)
    print('PREFLIGHT_COUNTS slots=8 plates=19 eols=8 disasm_bytes=8 functions=19 table_words=42 FAIL=%d' % len(FAILS))


def new_pool_primary(value, name):
    sym = symbols.getPrimarySymbol(toAddr(value))
    if sym is None:
        fail('NEW_POOL_MISSING %08x' % value)
        return None
    actual = {'id': long(sym.getID()), 'name': unicode(sym.getName()),
              'qualified_name': unicode(sym.getName(True)), 'type': str(sym.getSymbolType()),
              'source': str(sym.getSource()), 'primary': bool(sym.isPrimary())}
    same('NEW_POOL_PROPERTIES %08x' % value, dict((k, v) for k, v in actual.items() if k != 'id'),
         {'name': name, 'qualified_name': name, 'type': 'Label', 'source': 'USER_DEFINED', 'primary': True})
    same('NEW_POOL_GLOBAL %08x' % value, bool(sym.getParentNamespace().isGlobal()), True)
    return actual


def navigation(sym):
    return None if sym is None else dict((k, v) for k, v in sym.items() if k != 'primary')


def verify_post(before, after):
    same('FUNCTION_COUNT_POST', after['function_count'], 5209)
    same('MODULE_BYTES_POST', after['module_sha256'], before['module_sha256'])
    same('TMODE_PRESERVED', after['tmode'], before['tmode'])
    expected_comments = copy.deepcopy(before['comments'])
    for addr, name, text in PLATES:
        expected_comments['%08x:PLATE' % addr] = text
    for addr, text in EOLS.items():
        expected_comments['%08x:EOL' % addr] = text
    same('ALL_MODULE_COMMENTS', after['comments'], expected_comments)
    pools = dict((row['addr'], new_pool_primary(row['addr'], row['slot_label']))
                 for row in PLAN['slots'] if row['addr'] != 0x08095550)
    primary_31014 = next(x for x in SWITCH_GUARD['target_expected_after']['symbols'] if x['id'] == 31014)
    after_addresses = dict((x['address'], x) for x in after['addresses'])
    for old in before['addresses']:
        addr = old['address']
        expected = copy.deepcopy(old)
        if addr in pools:
            expected['symbols'] = [pools[addr]]
        if addr == 0x08095554:
            expected['symbols'] = copy.deepcopy(SWITCH_GUARD['target_expected_after']['symbols'])
        if addr in EOLS:
            expected['comments']['EOL'] = EOLS[addr]
        if addr == 0x0809565c:
            expected['references_from'] = [{'from': '0809565c', 'to': '0201b870', 'operand': 0,
                'type': 'DATA', 'source': 'USER_DEFINED', 'primary': True,
                'target_primary': {'id': 21747, 'name': 'gSpriteAttrBuf', 'qualified_name': 'gSpriteAttrBuf',
                                   'source': 'USER_DEFINED', 'type': 'Label'}}]
        if addr == 0x0201b870:
            expected['references_to'].append({'from': '0809565c', 'to': '0201b870', 'operand': 0,
                'type': 'DATA', 'source': 'USER_DEFINED', 'primary': True})
        if addr == 0x0809533c:
            expected['references_to'].append(copy.deepcopy(PLAN['disasm']['allowed_new_references'][1]))
        for ref in expected['references_from']:
            target = int(ref['to'], 16)
            if target in pools:
                # Reference identity is unchanged; the planned pool label changes navigation only.
                ref['target_primary'] = navigation(pools[target])
            if ref['from'] == '08095550' and target == 0x08095554:
                ref['target_primary'] = navigation(primary_31014)
        if 0x080952fc <= addr < 0x08095304:
            entry = next(row for row in DISASM_INSTRUCTIONS if row[0] <= addr < row[0] + row[1])
            expected['containing_code_unit'] = {'address': '%08x' % entry[0], 'length': entry[1], 'class': 'InstructionDB'}
            if addr == entry[0]:
                # Bytes, operand/target, length and flow references are checked independently below.
                expected['instruction_at'] = after_addresses[addr]['instruction_at']
                if entry[4] is not None:
                    ref = copy.deepcopy(next(r for r in PLAN['disasm']['allowed_new_references'] if int(r['from'], 16) == addr))
                    target_sym = symbols.getPrimarySymbol(toAddr(entry[4]))
                    ref['target_primary'] = {'id': long(target_sym.getID()), 'name': unicode(target_sym.getName()),
                        'qualified_name': unicode(target_sym.getName(True)), 'source': str(target_sym.getSource()),
                        'type': str(target_sym.getSymbolType())}
                    expected['references_from'] = [ref]
        same('ADDRESS_POST %08x' % addr, after_addresses[addr], expected)
    after_functions = dict((x['addr'], x) for x in after['functions'])
    plate_map = dict((addr, text) for addr, name, text in PLATES)
    for old in before['functions']:
        expected = copy.deepcopy(old)
        if old['addr'] in plate_map:
            text = plate_map[old['addr']]
            expected['plate'] = text
            expected['plate_chars'] = len(text)
            expected['plate_sha256'] = hashlib.sha256(text.encode('ascii')).hexdigest()
        if old['addr'] == 0x08095ba8:
            expected['incoming'].append(copy.deepcopy(PLAN['disasm']['allowed_new_references'][0]))
        same('FUNCTION_POST %08x' % old['addr'], after_functions[old['addr']], expected)
    for at, size, raw, mnemonic, target in DISASM_INSTRUCTIONS:
        ins = getInstructionAt(toAddr(at))
        if ins is None:
            fail('DISASM_MISSING %08x' % at)
            continue
        same('DISASM_LENGTH %08x' % at, ins.getLength(), size)
        same('DISASM_BYTES %08x' % at, ''.join('%02x' % (memory.getByte(toAddr(v)) & 255) for v in range(at, at + size)), raw)
        got = str(ins.getMnemonicString()).lower()
        if target is None:
            if got not in ('mov', 'movs') or str(ins.getDefaultOperandRepresentation(0)) != 'r0':
                fail('DISASM_MOV_R0 %08x' % at)
            scalar = ins.getScalar(1)
            if scalar is None or long(scalar.getUnsignedValue()) != 0:
                fail('DISASM_MOV_ZERO %08x' % at)
            same('DISASM_MOV_REFS', [ref_info(ref) for ref in references.getReferencesFrom(toAddr(at))], [])
        else:
            same('DISASM_MNEMONIC %08x' % at, got, mnemonic)
            same('DISASM_FLOW %08x' % at, [str(a) for a in ins.getFlows()], ['%08x' % target])
            same('DISASM_FLOW_REF %08x' % at,
                 [ref_info(ref) for ref in references.getReferencesFrom(toAddr(at))],
                 [r for r in PLAN['disasm']['allowed_new_references'] if int(r['from'], 16) == at])
        same('DISASM_FUNCTION_STILL_NONE %08x' % at, getFunctionContaining(toAddr(at)), None)
    verify_switch_words(True)
    print('POSTCHECK_COUNTS slots=8 plates=19 eols=8 instructions=3 functions=19 callee=1 switch_words=42 FAIL=%d' % len(FAILS))


def set_pool_label(addr, name):
    # The seven old pool symbols are dynamic DEFAULT labels. No references are edited here.
    label = symbols.createLabel(toAddr(addr), name, SourceType.USER_DEFINED)
    label.setPrimary()


def disassemble_eight_bytes():
    for addr, size, raw, mnemonic, target in DISASM_INSTRUCTIONS:
        # Existing bytes are undefined and TMode=1. No clearListing or context mutation is needed.
        command = DisassembleCommand(toAddr(addr), AddressSet(toAddr(addr), toAddr(addr + size - 1)), False)
        command.enableCodeAnalysis(False)
        if not command.applyTo(currentProgram, monitor):
            raise RuntimeError('DISASM_COMMAND %08x %s' % (addr, command.getStatusMsg()))
        actual_set = command.getDisassembledAddressSet()
        if actual_set.getNumAddresses() != size or str(actual_set.getMinAddress()) != '%08x' % addr or str(actual_set.getMaxAddress()) != '%08x' % (addr + size - 1):
            raise RuntimeError('DISASM_RANGE %08x %s' % (addr, actual_set))
        COUNTS['DISASM'] += 1


def apply_all():
    for operation in PLAN['operation_order']:
        addr, kind = operation['addr'], operation['kind']
        if kind == 'PLATE':
            text = next(text for value, name, text in PLATES if value == addr)
            listing.getCodeUnitAt(toAddr(addr)).setComment(CodeUnit.PLATE_COMMENT, text)
            COUNTS['PLATE'] += 1
        elif kind == 'DISASM':
            disassemble_eight_bytes()
        elif kind == 'RENAME':
            row = next(row for row in PLAN['slots'] if row['addr'] == addr)
            set_pool_label(addr, row['slot_label'])
            listing.getCodeUnitAt(toAddr(addr)).setComment(CodeUnit.EOL_COMMENT, EOLS[addr])
            COUNTS['RENAME'] += 1
            COUNTS['EOL'] += 1
        elif kind == 'REF':
            if addr == 0x08095550:
                # Exact existing receiver only. Do not rename/source-change/create/delete either switch label.
                symbols.getSymbol(31014).setPrimary()
                # The slot label and its existing DATA/USER_DEFINED reference are untouched.
            elif addr == 0x0809565c:
                set_pool_label(addr, 'gsprattrb_9565c')
                ref = references.addMemoryReference(toAddr(addr), toAddr(0x0201b870), RefType.DATA, SourceType.USER_DEFINED, 0)
                references.setPrimary(ref, True)
            else:
                raise RuntimeError('Unexpected REF address')
            listing.getCodeUnitAt(toAddr(addr)).setComment(CodeUnit.EOL_COMMENT, EOLS[addr])
            COUNTS['REF'] += 1
            COUNTS['EOL'] += 1
        else:
            raise RuntimeError('Unexpected operation kind')


PLAN = read_json('closure-plan.json')
SOURCE_SLOTS = read_json('root-closure-switch-before.json')
SOURCE_FUNCTIONS = read_json('root-closure-functions-before.json')
SWITCH_GUARD = next(row for row in PLAN['slots'] if row['addr'] == 0x08095550)['target_guard']
EOLS = dict([(addr, text) for addr, name, text in RENAME_SLOTS] + EXTRA_EOL)
print('BEGIN RefineF12HistoricalClosure mode=' + MODE)
verify_frozen_inputs()
reject_if_failed('FROZEN_INPUTS')
state = capture()
if MODE == 'check':
    before = read_json('closure-runtime-before.json')
    verify_post(before, state)
    reject_if_failed('PERSISTED_CHECK')
    COUNTS.update({'EQ': 0, 'REF': 2, 'RENAME': 6, 'PLATE': 19, 'EOL': 8, 'DISASM': 3, 'FUNC_RENAME': 0})
    write_json('closure-persisted-check.json', {'status': 'OK', 'FAIL': 0, 'counts': COUNTS, 'after': state})
else:
    verify_preflight(state)
    reject_if_failed('PREFLIGHT')
    baseline_path = os.path.join(RUN, 'closure-runtime-before.json')
    if os.path.exists(baseline_path):
        same('EXACT_READONLY_BASELINE', state, read_json('closure-runtime-before.json'))
        reject_if_failed('BASELINE')
    elif MODE == 'dry':
        write_json('closure-runtime-before.json', state)
    else:
        raise RuntimeError('Missing prior read-only dry baseline')
    if MODE == 'apply':
        transaction = currentProgram.startTransaction('F12 Historical Closure')
        success = False
        try:
            apply_all()
            after = capture()
            verify_post(state, after)
            reject_if_failed('POSTCHECK')
            success = True
        finally:
            currentProgram.endTransaction(transaction, success)
        write_json('closure-apply-result.json', {'status': 'OK', 'FAIL': 0, 'counts': COUNTS, 'after': after})
    else:
        COUNTS.update({'EQ': 0, 'REF': 2, 'RENAME': 6, 'PLATE': 19, 'EOL': 8, 'DISASM': 3, 'FUNC_RENAME': 0})
        write_json('closure-dry-result.json', {'status': 'OK', 'FAIL': 0, 'planned_counts': COUNTS})
print('COUNTS ' + ' '.join('%s=%d' % (key, COUNTS[key]) for key in ('EQ', 'REF', 'RENAME', 'PLATE', 'EOL', 'DISASM', 'FUNC_RENAME')))
print('STATUS: OK mode=%s FAIL=0' % MODE)
