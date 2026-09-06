# -*- coding: ascii -*-
#@runtime Jython
#@category Ygo-ex2006
# F13-Seg-5 EXPANDED_PASS preflight/apply script.
# Exactly 249 slots, four R4 regions / 80 ranges, one dataization,
# three Function creates, one Function rename, ten PLATE comments and 250 EOL comments. No carve.

INPUT_HASHES = [('doc/dev/refine/F13-Seg-5.proposal.md', 'b045999088ac6e758eb236e9920d26a74941532b7ce208bd6322176244d67317'),
 ('doc/dev/refine/F13-Seg-5.review.md', '191048643145dffc834f8b6ed78330ba857886deddc9a26765bbf2fd678e7477'),
 ('doc/dev/refine/F13-Seg-5.slots.tsv', 'ff0425315b47c77c8576776d66abfe01d8415acdb1cda3c3f3bc7ab4d64d4664'),
 ('output/refine-run-20260831-194634/f13-seg5-expanded-plan.json',
  'b88304291a070a70b89da05eb4599b0a15bab32956487a3362726473c142387a'),
 ('output/refine-run-20260831-194634/f13-seg5-expanded-refscan.json',
  'a5677da287f2168237d108e6233ebeef240e0d9d798ee24796c9f7c90c429eac'),
 ('output/refine-run-20260831-194634/F13-Seg-5-expanded-direct-edges.tsv',
  '88ac58dc4bc0815933535bbd8252a84d959acb9e4955bc05936ed4563dbf182a'),
 ('output/refine-run-20260831-194634/f13-seg5-expanded-edge-check.json',
  '31160d4a37585e0b356b9cca41aa44faccc6e5c78ca88cabca8e8f4fe10b067b'),
 ('output/refine-run-20260831-194634/f13-seg5-expanded-backup.json',
  'c174454a034b751110a34611470f61d4168c842b1c0ed4a684d999ae7e265eff'),
 ('output/refine-run-20260831-194634/f13-seg5-slots-before.json',
  'abba68ffd8181462ed791bbb95a994e1ab2f9d9e2710441ff994a5869b29ad86'),
 ('output/refine-run-20260831-194634/f13-seg5-functions-before.json',
  '05319b1b60bb109b405b36e7d59fa0238c807934104ea1f6cb4f3fccb7162425'),
 ('output/refine-run-20260831-194634/f13-seg5-code-before.json',
  'a1e2e4e8f10226d3bdeac956f6d57d43f03809a770d7aca6c4bc2e7edca21988'),
 ('output/refine-run-20260831-194634/f13-seg4-block-code-before.json',
  '22d9497fb2e8b1fe1e486767734663943be8776a4db5cf0d7de32cdbc589b449'),
 ('output/refine-run-20260831-194634/f13-seg4-block-flow.json',
  'c66b84463ea2bc7d2d417c8eccae1f7db98f9ebb9e7228196d48a82b02920417')]

import copy
import hashlib
import json
import os
import re

from java.math import BigInteger
from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.address import AddressSet
from ghidra.program.model.data import DWordDataType, UnsignedIntegerDataType, UnsignedShortDataType
from ghidra.program.model.listing import CodeUnit, Function, ParameterImpl
from ghidra.program.model.symbol import RefType, SourceType, SymbolType


MODE = list(getScriptArgs())[0].lower() if list(getScriptArgs()) else 'dry'
if MODE not in ('dry', 'apply', 'check', 'probe', 'symbol_probe', 'expanded_probe'):
    raise RuntimeError('Expected dry, apply, check, probe, symbol_probe, or expanded_probe')
ROOT = os.path.abspath(os.path.join(str(getSourceFile().getParentFile()), '..', '..'))
RUN = os.path.join(ROOT, 'output', 'refine-run-20260831-194634')
listing = currentProgram.getListing()
symbols = currentProgram.getSymbolTable()
references = currentProgram.getReferenceManager()
memory = currentProgram.getMemory()
equates = currentProgram.getEquateTable()
context = currentProgram.getProgramContext()
tmode = context.getRegister('TMode')
functions = currentProgram.getFunctionManager()
FAILS = []
DISASM_SEEDS = []
COUNTS = dict((name, 0) for name in (
    'EQ', 'REF', 'RENAME', 'EOL', 'PLATE', 'R4_REGION', 'CODE_RANGE',
    'POOL_DATA', 'DATAIZATION', 'FUNC_CREATE', 'FUNC_RENAME'))


def read_json(name):
    with open(os.path.join(RUN, name), 'rb') as stream:
        return json.load(stream)


def write_json(name, value):
    with open(os.path.join(RUN, name), 'w') as stream:
        stream.write(json.dumps(value, ensure_ascii=True, sort_keys=True, indent=2) + '\n')


def file_hash(path):
    with open(path, 'rb') as stream:
        return hashlib.sha256(stream.read()).hexdigest()


def fail(message, actual=None, expected=None):
    FAILS.append(message)
    print('FAIL: ' + message)
    if actual is not None or expected is not None:
        print('DETAIL ' + json.dumps({'actual': actual, 'expected': expected}, ensure_ascii=True, sort_keys=True))


def require(condition, message):
    if not condition:
        fail(message)


def canonical(value):
    if isinstance(value, dict):
        value = dict((key, canonical(item)) for key, item in value.items() if key != 'input_label')
    elif isinstance(value, list):
        value = sorted((canonical(item) for item in value), key=lambda item: json.dumps(item, sort_keys=True))
    return value


def same(message, actual, expected):
    if canonical(actual) != canonical(expected):
        fail(message, actual, expected)


def basic_ref(ref, target_primary=False):
    result = {'from': str(ref.getFromAddress()), 'to': str(ref.getToAddress()),
              'operand': ref.getOperandIndex(), 'type': str(ref.getReferenceType()),
              'source': str(ref.getSource()), 'primary': bool(ref.isPrimary())}
    if target_primary:
        primary = symbols.getPrimarySymbol(ref.getToAddress())
        result['target_primary'] = None if primary is None else {
            'id': long(primary.getID()), 'name': unicode(primary.getName()),
            'qualified_name': unicode(primary.getName(True)),
            'type': str(primary.getSymbolType()), 'source': str(primary.getSource())}
    return result


def symbol_info(symbol):
    return {'id': long(symbol.getID()), 'name': unicode(symbol.getName()),
            'qualified_name': unicode(symbol.getName(True)),
            'type': str(symbol.getSymbolType()), 'source': str(symbol.getSource()),
            'primary': bool(symbol.isPrimary())}


def data_info(addr):
    data = listing.getDefinedDataAt(addr)
    return None if data is None else {
        'address': str(data.getAddress()), 'length': data.getLength(),
        'type': unicode(data.getDataType().getPathName()),
        'min': str(data.getMinAddress()), 'max': str(data.getMaxAddress())}


def describe(value):
    addr = toAddr(value)
    unit = listing.getCodeUnitContaining(addr)
    fn = getFunctionContaining(addr)
    result = {
        'address': value,
        'symbols': [symbol_info(symbol) for symbol in symbols.getSymbols(addr)],
        'defined_data': data_info(addr),
        'containing_code_unit': None if unit is None else {
            'address': str(unit.getAddress()), 'length': unit.getLength(),
            'class': str(unit.getClass().getSimpleName())},
        'instruction_at': None if getInstructionAt(addr) is None else str(getInstructionAt(addr)),
        'containing_function': None if fn is None else {
            'entry': str(fn.getEntryPoint()), 'name': str(fn.getName()), 'body': str(fn.getBody())},
        'equates': [{'name': str(eq.getName()), 'value': long(eq.getValue())}
                    for eq in equates.getEquates(addr)],
        'comments': {},
        'rom_word': None,
        'references_from': [basic_ref(ref, True) for ref in references.getReferencesFrom(addr)],
        'references_to': [basic_ref(ref, False) for ref in references.getReferencesTo(addr)],
    }
    for name, kind in (('EOL', CodeUnit.EOL_COMMENT), ('PLATE', CodeUnit.PLATE_COMMENT)):
        text = listing.getComment(kind, addr)
        result['comments'][name] = None if text is None else unicode(text)
    if 0x08000000 <= value <= 0x09fffffc:
        result['rom_word'] = memory.getInt(addr) & 0xffffffff
    return result


def function_state(value):
    fn = getFunctionAt(toAddr(value))
    if fn is None:
        return None
    symbol = fn.getSymbol()
    plate = listing.getComment(CodeUnit.PLATE_COMMENT, fn.getEntryPoint())
    values = []
    eols = []
    iterator = fn.getBody().getAddresses(True)
    while iterator.hasNext():
        addr = iterator.next()
        values.append(chr(memory.getByte(addr) & 255))
        eol = listing.getComment(CodeUnit.EOL_COMMENT, addr)
        if eol is not None:
            eols.append([str(addr), unicode(eol)])
    return {
        'addr': value, 'name': unicode(fn.getName()), 'symbol_id': long(symbol.getID()),
        'source': str(symbol.getSource()), 'symbol_type': str(symbol.getSymbolType()),
        'body': str(fn.getBody()), 'body_size': fn.getBody().getNumAddresses(),
        'body_sha256': hashlib.sha256(''.join(values)).hexdigest(),
        'plate': None if plate is None else unicode(plate),
        'plate_chars': None if plate is None else len(plate),
        'plate_sha256': None if plate is None else hashlib.sha256(unicode(plate).encode('utf8')).hexdigest(),
        'incoming': [basic_ref(ref, False) for ref in references.getReferencesTo(fn.getEntryPoint())],
        'eols': eols,
    }


def mode_at(value):
    result = context.getValue(tmode, toAddr(value), False)
    return None if result is None else int(result)


def unit_state(value):
    addr = toAddr(value)
    unit = listing.getCodeUnitAt(addr)
    if unit is None:
        return None
    instruction = getInstructionAt(addr)
    data = listing.getDefinedDataAt(addr)
    fn = getFunctionContaining(addr)
    raw = ''.join('%02x' % (memory.getByte(addr.add(index)) & 255) for index in range(unit.getLength()))
    result = {
        'address': value, 'length': unit.getLength(), 'kind': str(unit.getClass().getSimpleName()),
        'bytes': raw, 'function': None if fn is None else str(fn.getEntryPoint()),
        'defined_data': None if data is None else unicode(data.getDataType().getPathName()),
        'references_from': [basic_ref(ref, False) for ref in references.getReferencesFrom(addr)],
        'references_to': [basic_ref(ref, False) for ref in references.getReferencesTo(addr)],
        'eol': listing.getComment(CodeUnit.EOL_COMMENT, addr),
        'plate': listing.getComment(CodeUnit.PLATE_COMMENT, addr),
        'tmode': mode_at(value), 'instruction': None,
    }
    if instruction is not None:
        result['instruction'] = {
            'mnemonic': str(instruction.getMnemonicString()), 'text': str(instruction),
            'flow_type': str(instruction.getFlowType()),
            'flows': [str(target) for target in instruction.getFlows()],
            'fallthrough': None if instruction.getFallThrough() is None else str(instruction.getFallThrough()),
            'operands': [str(instruction.getDefaultOperandRepresentation(index))
                         for index in range(instruction.getNumOperands())],
        }
    return result


def range_units(lo, hi):
    result = []
    cursor = lo
    while cursor < hi:
        state = unit_state(cursor)
        require(state is not None and state['length'] > 0 and cursor + state['length'] <= hi,
                'RANGE_UNIT %08x' % cursor)
        if state is None or state['length'] <= 0 or cursor + state['length'] > hi:
            break
        result.append(state)
        cursor += state['length']
    require(cursor == hi, 'RANGE_COVERAGE %08x_%08x' % (lo, hi))
    return result


def raw_hash(lo, hi):
    values = ''.join(chr(memory.getByte(toAddr(value)) & 255) for value in range(lo, hi))
    return hashlib.sha256(values).hexdigest()


def read_edge_ledger():
    path = os.path.join(RUN, 'F13-Seg-5-expanded-direct-edges.tsv')
    with open(path, 'rb') as stream:
        lines = [line.rstrip('\r\n') for line in stream]
    header = lines[0].split('\t')
    expected_header = ['source', 'op', 'target', 'source_group', 'classification',
                       'target_owner', 'rule3_crosscheck', 'rom_bytes']
    require(header == expected_header, 'EDGE_LEDGER_HEADER')
    result = []
    for line in lines[1:]:
        values = line.split('\t')
        row = dict(zip(header, values))
        row['source'] = int(row['source'], 16)
        row['target'] = int(row['target'], 16)
        result.append(row)
    return result


def sign_extend(value, bits):
    sign = 1 << (bits - 1)
    return (value ^ sign) - sign


def halfword(value):
    lo = memory.getByte(toAddr(value)) & 255
    hi = memory.getByte(toAddr(value + 1)) & 255
    return lo | (hi << 8)


def byte_hex(value, length):
    return ''.join('%02x' % (memory.getByte(toAddr(value + index)) & 255)
                   for index in range(length))


def decode_direct_edges():
    cond_names = ['beq.n', 'bne.n', 'bcs.n', 'bcc.n', 'bmi.n', 'bpl.n', 'bvs.n',
                  'bvc.n', 'bhi.n', 'bls.n', 'bge.n', 'blt.n', 'bgt.n', 'ble.n']
    rows = []
    for lo, hi in CODE_RANGES:
        cursor = lo
        while cursor < hi:
            first = halfword(cursor)
            if first & 0xf800 == 0xf000 and cursor + 4 <= hi:
                second = halfword(cursor + 2)
                if second & 0xf800 == 0xf800:
                    immediate = ((first & 0x7ff) << 12) | ((second & 0x7ff) << 1)
                    target = (cursor + 4 + sign_extend(immediate, 23)) & 0xffffffff
                    rows.append({'source': cursor, 'op': 'bl', 'target': target,
                                 'rom_bytes': byte_hex(cursor, 4)})
                    cursor += 4
                    continue
            if first & 0xf000 == 0xd000 and ((first >> 8) & 15) < 14:
                condition = (first >> 8) & 15
                target = (cursor + 4 + sign_extend(first & 255, 8) * 2) & 0xffffffff
                rows.append({'source': cursor, 'op': cond_names[condition], 'target': target,
                             'rom_bytes': byte_hex(cursor, 2)})
            elif first & 0xf800 == 0xe000:
                target = (cursor + 4 + sign_extend(first & 0x7ff, 11) * 2) & 0xffffffff
                rows.append({'source': cursor, 'op': 'b.n', 'target': target,
                             'rom_bytes': byte_hex(cursor, 2)})
            cursor += 2
    return rows


def verify_direct_edges(require_instructions):
    ledger = read_edge_ledger()
    expected_core = [dict((key, row[key]) for key in ('source', 'op', 'target', 'rom_bytes'))
                     for row in ledger]
    decoded = decode_direct_edges()
    require(decoded == expected_core, 'DIRECT_EDGE_ROWS_EXACT')
    require(len(ledger) == 375 and len(set(row['target'] for row in ledger)) == 226,
            'DIRECT_EDGE_COUNTS')
    require(sum(row['op'] == 'bl' for row in ledger) == 89 and
            sum(row['op'] != 'bl' for row in ledger) == 286, 'DIRECT_EDGE_OP_COUNTS')
    require(sum(row['source'] == 0x080a18ba and row['op'] == 'bl' and
                row['target'] == 0x080a0b20 and row['rom_bytes'] == 'fff731f9'
                for row in ledger) == 1, 'DIRECT_EDGE_18BA_0B20')
    external = [row for row in ledger if row['classification'] == 'EXTERNAL_EXISTING_STUB']
    require(len(external) == 1 and external[0]['source'] == 0x080a187a and
            external[0]['target'] == READONLY_PROJECTION, 'DIRECT_EDGE_EXTERNAL_ONLY')
    require(all(row['classification'] != 'UNAPPROVED' for row in ledger), 'DIRECT_EDGE_UNAPPROVED')
    for row in ledger:
        require(not overlaps_reserved(row['target'], row['target'] + 1),
                'DIRECT_EDGE_RESERVED_TARGET %08x' % row['source'])
        require(not any(lo <= row['target'] < hi for lo, hi in RULE3),
                'DIRECT_EDGE_RULE3_TARGET %08x' % row['source'])
        if require_instructions:
            instruction = getInstructionAt(toAddr(row['source']))
            require(instruction is not None and
                    toAddr(row['target']) in list(instruction.getFlows()),
                    'DIRECT_EDGE_GHIDRA_FLOW %08x' % row['source'])
    return ledger


def projection_state():
    value = READONLY_PROJECTION
    addr = toAddr(value)
    data = listing.getDefinedDataAt(addr)
    at_addr = list(symbols.getSymbols(addr))
    primary = symbols.getPrimarySymbol(addr)
    symbol_rows = []
    for symbol in at_addr:
        row = symbol_info(symbol)
        row['global'] = symbol.getParentNamespace() == currentProgram.getGlobalNamespace()
        symbol_rows.append(row)
    primary_row = None
    if primary is not None:
        primary_row = symbol_info(primary)
        primary_row['global'] = primary.getParentNamespace() == currentProgram.getGlobalNamespace()
    return {
        'address': value,
        'bytes': byte_hex(value, 4),
        'data': None if data is None else {
            'address': str(data.getAddress()), 'length': data.getLength(),
            'type': unicode(data.getDataType().getPathName())},
        'instruction': None if getInstructionAt(addr) is None else str(getInstructionAt(addr)),
        'function': None if getFunctionAt(addr) is None else unicode(getFunctionAt(addr).getName()),
        'eol': listing.getComment(CodeUnit.EOL_COMMENT, addr),
        'plate': listing.getComment(CodeUnit.PLATE_COMMENT, addr),
        'symbol_count': len(at_addr),
        'symbols': symbol_rows,
        'primary': primary_row,
    }


def verify_projection_contract(post):
    projection = projection_state()
    require(projection['bytes'] == '01207047' and projection['data'] is None and
            projection['instruction'] is None and projection['function'] is None and
            projection['eol'] is None and projection['plate'] is None,
            'READONLY_PROJECTION_LISTING_%s' % ('POST' if post else 'PRE'))
    if post:
        primary = projection['primary']
        require(projection['symbol_count'] == 1 and len(projection['symbols']) == 1 and
                primary is not None and primary['primary'] and
                primary['name'] == 'SUB_080a38f8' and
                primary['qualified_name'] == 'SUB_080a38f8' and
                primary['source'] == 'DEFAULT' and primary['type'] == 'Label' and
                primary['global'] and projection['symbols'][0] == primary,
                'READONLY_PROJECTION_SYMBOL_POST')
    else:
        require(projection['symbol_count'] == 0 and projection['symbols'] == [] and
                projection['primary'] is None, 'READONLY_PROJECTION_SYMBOL_PRE')
    return projection


PLAN = read_json('f13-seg5-expanded-plan.json')
SLOTS_BEFORE_DOC = read_json('f13-seg5-slots-before.json')
FUNCTIONS_BEFORE_DOC = read_json('f13-seg5-functions-before.json')
CODE_BEFORE_DOC = read_json('f13-seg5-code-before.json')
CLOSURE_BEFORE_DOC = read_json('f13-seg4-block-code-before.json')
EDGE_CHECK_DOC = read_json('f13-seg5-expanded-edge-check.json')
SCRIPT_HASH = file_hash(getSourceFile().getAbsolutePath())
SLOTS = dict((row['addr'], row) for row in PLAN['actions'])
SLOT_BEFORE = dict((row['address'], dict((key, item) for key, item in row.items() if key != 'input_label'))
                   for row in SLOTS_BEFORE_DOC['slots'])
TARGET_BEFORE = dict((row['address'], row) for row in SLOTS_BEFORE_DOC['extra_targets'])
FUNCTIONS_BEFORE = dict((row['addr'], row) for row in FUNCTIONS_BEFORE_DOC['functions'])
CODE_BEFORE = dict((row['address'], row) for row in CODE_BEFORE_DOC['units'])
CLOSURE_BEFORE = dict((row['address'], row) for row in CLOSURE_BEFORE_DOC['units'])
PLATES = dict((row['addr'], row['text']) for row in PLAN['plates'])
BODY_RANGES = dict((row['addr'], [tuple(pair) for pair in row['ranges']]) for row in PLAN['function_bodies'])
FUNCTION_NAMES = dict((int(addr), name) for addr, name in PLAN['function_names'].items())
CODE_GROUPS = [[tuple(pair) for pair in group] for group in PLAN['code_groups']]
CODE_RANGES = [tuple(pair) for pair in PLAN['code_ranges']]
PADDING = [tuple(pair) for pair in PLAN['padding']]
RULE3 = [tuple(pair) for pair in PLAN['rule3']]
CASE_LABELS = [(row[0], row[1]) for row in PLAN['case_labels']]
TARGET_CONTRACTS = [(row[0], row[1], row[2], row[3]) for row in PLAN['target_contracts']]
RENAME_CONTRACT = dict((int(addr), value) for addr, value in PLAN['rename_contract'].items())
NEW_POOLS = set(row['addr'] for row in PLAN['actions'] if row['new_pool'])
NEW_FUNCTIONS = (0x080a0b20, 0x080a1f68, 0x080a24cc)
OLD_NAME = 'check_equip_target_slot_state'
NEW_NAME = 'tick_equip_display_row_by_type'
PRENORMALIZE_SWITCH_SLOTS = (0x080a16d4,)
LOCAL_LABELS = [(row[0], row[1], row[2]) for row in PLAN['local_labels']]
READONLY_PROJECTION = PLAN['readonly_projection']
NORMALIZED_NAMES = {}
for value, name, data_type, length in TARGET_CONTRACTS:
    NORMALIZED_NAMES[value] = name
for value, name in CASE_LABELS:
    NORMALIZED_NAMES[value] = name
for value in PRENORMALIZE_SWITCH_SLOTS:
    NORMALIZED_NAMES[value] = SLOTS[value]['slot_label']
SWITCH_TARGET_GROUPS = [
    ('row_type', sorted(set(value for addr, value in PLAN['switch_entries'][:19]))),
    ('target_select_phase', sorted(set(value for addr, value in PLAN['switch_entries'][19:24]))),
    ('activation_card_type', sorted(set(value for addr, value in PLAN['switch_entries'][24:]))),
]
SWITCH_TABLES = (0x080a16d4, 0x080a2004, 0x080a25f0)


def verify_frozen_and_plan():
    for relative, digest in INPUT_HASHES:
        same('INPUT_HASH ' + relative, file_hash(os.path.join(ROOT, relative)), digest)
    require(PLAN['input_hashes'] == {
        'proposal': 'b045999088ac6e758eb236e9920d26a74941532b7ce208bd6322176244d67317',
        'review': '98e43b4f5a90576da66f75268a68497d6147565b62113fbc5d71d5b1336f7f76',
        'tsv': 'ff0425315b47c77c8576776d66abfe01d8415acdb1cda3c3f3bc7ab4d64d4664',
        'edge_ledger': '88ac58dc4bc0815933535bbd8252a84d959acb9e4955bc05936ed4563dbf182a'},
        'APPROVED_HASHES')
    require(len(SLOTS) == 249 and len(set(SLOTS)) == 249, 'SLOT_COUNT')
    require([sum(row['action'] == kind for row in PLAN['actions'])
             for kind in ('EQ', 'REF', 'RENAME')] == [190, 33, 26], 'ACTION_COUNTS')
    require(len(NEW_POOLS) == 141 and 0x080a1950 in NEW_POOLS, 'POOL_COUNT')
    require([len(group) for group in CODE_GROUPS] == [49, 18, 2, 11] and
            len(CODE_RANGES) == 80, 'R4_RANGE_COUNTS')
    require(sum(hi - lo for lo, hi in CODE_GROUPS[0]) == 1754 and
            sum(hi - lo for lo, hi in CODE_RANGES) == 2640, 'R4_CODE_BYTES')
    reserved = [(value, value + 4) for value in NEW_POOLS] + list(PADDING)
    for lo, hi in CODE_RANGES:
        require(lo < hi and lo % 2 == 0 and hi % 2 == 0, 'R4_RANGE_ALIGNMENT')
        require(not any(lo < reserved_hi and reserved_lo < hi
                        for reserved_lo, reserved_hi in reserved),
                'R4_RANGE_RESERVED_OVERLAP %08x..%08x' % (lo, hi))
    require(len(PLATES) == 10 and max(len(text) for text in PLATES.values()) == 456,
            'PLATE_COUNTS')
    for text in PLATES.values():
        require(len(text) < 500 and all(ord(char) < 128 for char in text), 'PLATE_ASCII')
    for row in PLAN['actions']:
        require(all(ord(char) < 128 for char in row['eol']), 'EOL_ASCII %08x' % row['addr'])
    require(len(PLAN['switch_entries']) == 30 and all(value % 2 == 0 for addr, value in PLAN['switch_entries']),
            'EVEN_SWITCH_ENTRIES')
    require(len(set(value for addr, value in PLAN['odd_callbacks'])) == 4 and
            all(value % 2 == 1 for addr, value in PLAN['odd_callbacks']), 'ODD_CALLBACKS')
    require(len(LOCAL_LABELS) == 1 and LOCAL_LABELS[0][0] == 0x080a131c and
            all(ord(char) < 128 for char in LOCAL_LABELS[0][2]), 'LOCAL_EPILOGUE_PLAN')
    require(len(RULE3) == 2 and PLAN['dataization'] == [0x080a1950, 0x080a1954], 'RULE3_DATAIZATION')
    require(PLAN['function_pre_count'] == 5209 and PLAN['function_post_count'] == 5212,
            'FUNCTION_COUNT_PLAN')
    require(len(BODY_RANGES[0x080a0b20]) == 49 and len(BODY_RANGES[0x080a1658]) == 19 and
            len(BODY_RANGES[0x080a1f68]) == 13 and
            len(BODY_RANGES[0x080a24cc]) == 2, 'FUNCTION_BODY_RANGE_COUNTS')
    require(PRENORMALIZE_SWITCH_SLOTS == (0x080a16d4,) and
            [len(values) for name, values in SWITCH_TARGET_GROUPS] == [18, 5, 6] and
            len(NORMALIZED_NAMES) == 32 and
            all(value in NORMALIZED_NAMES for value in SWITCH_TABLES),
            'SYMBOL_PROBE_CONTRACTS')
    require(PLAN['new_pool_count'] == 141 and len(PLAN['new_definitions']) == 7 and
            len(PLAN['gas_aliases']) == 4, 'SOURCE_COUNTS')
    refscan = read_json('f13-seg5-expanded-refscan.json')
    require(refscan['status'] == 'EXPANDED_REFSCAN_OK' and
            refscan['entry']['raw'] == 0 and refscan['entry']['thumb'] == 0 and
            refscan['entry']['direct_call'] == {
                'source': 0x080a18ba, 'target': 0x080a0b20, 'rom_bytes': 'fff731f9'} and
            refscan['nonzero_start_counts'] == {
                '080a0c0c': [26, 65], '080a0d18': [0, 1],
                '080a0f0c': [2, 3], '080a131c': [4, 1]} and
            refscan['original_counts'] == [[29, 2], [0, 0], [0, 0], [1, 0], [6, 6]],
            'REFSCAN_COUNTS')
    require(EDGE_CHECK_DOC['status'] == 'EXPANDED_DIRECT_EDGE_LEDGER_OK' and
            EDGE_CHECK_DOC['rows'] == 375 and EDGE_CHECK_DOC['bl'] == 89 and
            EDGE_CHECK_DOC['b'] == 286 and EDGE_CHECK_DOC['unique_targets'] == 226 and
            EDGE_CHECK_DOC['pool_padding_rule3_targets'] == 0 and
            EDGE_CHECK_DOC['unapproved'] == 0, 'EDGE_LEDGER_COUNTS')


def exact_body(ranges):
    body = AddressSet()
    for lo, hi in ranges:
        body.addRange(toAddr(lo), toAddr(hi - 1))
    return body


def operand_zero_refs(value):
    return [basic_ref(ref, False) for ref in references.getReferencesFrom(toAddr(value))
            if ref.getOperandIndex() == 0]


def expected_rename_refs(value):
    contract = RENAME_CONTRACT[value]
    if contract is None:
        return []
    target, ref_type, source, primary = contract
    return [{'from': '%08x' % value, 'to': '%08x' % target, 'operand': 0,
             'type': ref_type, 'source': source, 'primary': primary}]


def verify_prestate():
    require(functions.getFunctionCount() == 5209, 'FUNCTION_COUNT_PRE')
    require(raw_hash(0x080a0b20, 0x080a1338) == PLAN['closure_sha256'], 'CLOSURE_BYTES_PRE')
    require(raw_hash(0x080a1658, 0x080a27a0) == PLAN['segment_sha256'], 'SEGMENT_BYTES_PRE')
    require(getFunctionAt(toAddr(0x080a1658)) is not None and
            long(getFunctionAt(toAddr(0x080a1658)).getSymbol().getID()) == 16936 and
            unicode(getFunctionAt(toAddr(0x080a1658)).getName()) == OLD_NAME, 'FUNCTION_1658_PRE')
    require(getFunctionAt(toAddr(0x080a0b20)) is None and
            getFunctionAt(toAddr(0x080a131c)) is None and
            getFunctionAt(toAddr(0x080a1f68)) is None and
            getFunctionAt(toAddr(0x080a24cc)) is None and
            getFunctionAt(toAddr(READONLY_PROJECTION)) is None,
            'NEW_FUNCTIONS_ABSENT_PRE')
    closure_actual = [unit_state(value) for value in sorted(CLOSURE_BEFORE)]
    closure_expected = [CLOSURE_BEFORE[value] for value in sorted(CLOSURE_BEFORE)]
    same('CLOSURE_LISTING_PRE', closure_actual, closure_expected)
    for value, expected in SLOT_BEFORE.items():
        same('SLOT_PRE %08x' % value, describe(value), expected)
    for value, row in SLOTS.items():
        require(memory.getInt(toAddr(value)) & 0xffffffff == row['value'], 'SLOT_ROM_PRE %08x' % value)
    for value, expected in TARGET_BEFORE.items():
        same('TARGET_PRE %08x' % value, describe(value), expected)
    for value, expected in FUNCTIONS_BEFORE.items():
        same('FUNCTION_PRE %08x' % value, function_state(value), expected)
    for value in RENAME_CONTRACT:
        same('RENAME_REF_PRE %08x' % value, operand_zero_refs(value), expected_rename_refs(value))
    for value, name, data_type, length in TARGET_CONTRACTS:
        expected = TARGET_BEFORE[value]
        require(expected['defined_data'] is not None and
                expected['defined_data']['type'] == data_type and
                expected['defined_data']['length'] == length, 'TARGET_DATA_CONTRACT_PRE %08x' % value)
    for lo, hi in RULE3:
        expected = []
        cursor = lo
        while cursor < hi:
            row = CODE_BEFORE[cursor]
            expected.append(row)
            cursor += row['length']
        same('RULE3_PRE %08x' % lo, range_units(lo, hi), expected)
    incoming = [basic_ref(ref, False) for ref in references.getReferencesTo(toAddr(0x080a1658))]
    same('FUNCTION_1658_INCOMING_PRE', incoming, [{
        'from': '08094d30', 'to': '080a1658', 'operand': 0,
        'type': 'UNCONDITIONAL_CALL', 'source': 'DEFAULT', 'primary': True}])
    require(list(symbols.getSymbols(toAddr(0x080a131c))) == [], 'LOCAL_EPILOGUE_SYMBOL_PRE')
    verify_projection_contract(False)
    verify_direct_edges(False)
    print('PREFLIGHT slots=249 EQ=190 REF=33 RENAME=26 R4=4 CODE_RANGES=49+18+2+11 '
          'POOL=141 DATAIZATION=1 FUNC_CREATE=3 FUNC_RENAME=1 PLATE=10 EOL=250 RULE3=2 '
          'EDGES=375 TARGETS=226 FAIL=%d' % len(FAILS))


def verify_name_available(name, value, post=False):
    matches = list(symbols.getGlobalSymbols(name))
    require(all(symbol.getAddress() == toAddr(value) for symbol in matches), 'NAME_COLLISION ' + name)
    if post:
        require(len(matches) == 1, 'NAME_COUNT ' + name)


def rename_primary_same_object(value, name, expected=None):
    addr = toAddr(value)
    verify_name_available(name, value, False)
    primary = symbols.getPrimarySymbol(addr)
    at_addr = list(symbols.getSymbols(addr))
    if expected is not None:
        expected_symbols = expected['symbols']
        require(len(expected_symbols) == 1 and len(at_addr) == 1 and primary is not None and
                long(primary.getID()) == expected_symbols[0]['id'], 'PRIMARY_OBJECT_PRE %08x' % value)
    if FAILS:
        raise RuntimeError('Primary object precondition failed at %08x' % value)
    if primary is None:
        primary = symbols.createLabel(addr, name, SourceType.USER_DEFINED)
    else:
        if primary.getParentNamespace() != currentProgram.getGlobalNamespace():
            primary.setNameAndNamespace(name, currentProgram.getGlobalNamespace(), SourceType.USER_DEFINED)
        else:
            primary.setName(name, SourceType.USER_DEFINED)
    primary = symbols.getPrimarySymbol(addr)
    if primary is None or unicode(primary.getName()) != name:
        raise RuntimeError('Primary rename failed at %08x' % value)
    primary.setPrimary()
    if len(list(symbols.getSymbols(addr))) != 1:
        raise RuntimeError('Same-address alias at %08x' % value)
    return primary


def normalize_targets_and_cases():
    for value in PRENORMALIZE_SWITCH_SLOTS:
        rename_primary_same_object(value, SLOTS[value]['slot_label'], TARGET_BEFORE[value])
    for value, name, data_type, length in TARGET_CONTRACTS:
        rename_primary_same_object(value, name, TARGET_BEFORE[value])
    for value, name in CASE_LABELS:
        # 080a2004 was already normalized as a REF target; other targets are independent.
        if value == 0x080a2004:
            continue
        rename_primary_same_object(value, name, TARGET_BEFORE[value])


def normalize_local_labels():
    for value, name, text in LOCAL_LABELS:
        verify_name_available(name, value, False)
        at_addr = list(symbols.getSymbols(toAddr(value)))
        require(len(at_addr) <= 1, 'LOCAL_LABEL_ALIAS_PRE %08x' % value)
        if at_addr:
            primary = at_addr[0]
            if primary.getParentNamespace() != currentProgram.getGlobalNamespace():
                primary.setNameAndNamespace(name, currentProgram.getGlobalNamespace(), SourceType.USER_DEFINED)
            else:
                primary.setName(name, SourceType.USER_DEFINED)
            primary.setPrimary()
        else:
            primary = symbols.createLabel(toAddr(value), name, SourceType.USER_DEFINED)
            primary.setPrimary()
        require(len(list(symbols.getSymbols(toAddr(value)))) == 1 and
                unicode(symbols.getPrimarySymbol(toAddr(value)).getName()) == name and
                str(symbols.getPrimarySymbol(toAddr(value)).getSource()) == 'USER_DEFINED',
                'LOCAL_LABEL_NORMALIZE %08x' % value)


def probe_symbol_state(value):
    addr = toAddr(value)
    at_addr = list(symbols.getSymbols(addr))
    primary = symbols.getPrimarySymbol(addr)
    return {
        'address': value,
        'symbol_count': len(at_addr),
        'primary': None if primary is None else symbol_info(primary),
        'symbols': [symbol_info(symbol) for symbol in at_addr],
    }


def probe_approved_phase(phase, require_user):
    rows = []
    for value in sorted(NORMALIZED_NAMES):
        state = probe_symbol_state(value)
        primary = symbols.getPrimarySymbol(toAddr(value))
        if require_user:
            require(state['symbol_count'] == 1 and primary is not None and
                    bool(primary.isPrimary()) and
                    unicode(primary.getName()) == NORMALIZED_NAMES[value] and
                    str(primary.getSource()) == 'USER_DEFINED' and
                    primary.getParentNamespace() == currentProgram.getGlobalNamespace(),
                    'SYMBOL_PROBE_%s %08x' % (phase.upper(), value))
        else:
            expected = TARGET_BEFORE[value]['symbols']
            same('SYMBOL_PROBE_BEFORE %08x' % value, state['symbols'], expected)
            require(len(expected) == 1 and state['symbol_count'] == 1 and
                    state['primary'] is not None and state['primary']['primary'],
                    'SYMBOL_PROBE_BEFORE_UNIQUE %08x' % value)
        rows.append({'address': value, 'approved_name': NORMALIZED_NAMES[value],
                     'phase': phase, 'state': state})
    return rows


def probe_switch_target_groups(phase):
    return [{'name': name, 'count': len(values),
             'targets': [probe_symbol_state(value) for value in values]}
            for name, values in SWITCH_TARGET_GROUPS]


def probe_id_changes(before, after):
    before_map = dict((row['address'], row['state']['primary']) for row in before)
    after_map = dict((row['address'], row['state']['primary']) for row in after)
    changes = []
    for value in sorted(before_map):
        old = before_map[value]
        new = after_map[value]
        if old is None or new is None or old['id'] != new['id']:
            changes.append({'address': value, 'before': old, 'after': new})
    return changes


def overlaps_reserved(lo, hi):
    for value in NEW_POOLS:
        if lo < value + 4 and value < hi:
            return True
    for reserved_lo, reserved_hi in PADDING:
        if lo < reserved_hi and reserved_lo < hi:
            return True
    return False


def disassemble_seed(seed, lo, hi):
    if seed % 2 != 0 or seed < lo or seed >= hi or overlaps_reserved(seed, seed + 2):
        raise RuntimeError('Invalid disassembly seed=%08x range=%08x..%08x' % (seed, lo, hi))
    command = DisassembleCommand(toAddr(seed), AddressSet(toAddr(seed), toAddr(hi - 1)), False)
    command.enableCodeAnalysis(False)
    if not command.applyTo(currentProgram, monitor):
        raise RuntimeError('DisassembleCommand failed seed=%08x range=%08x..%08x: %s' %
                           (seed, lo, hi, command.getStatusMsg()))


def clear_and_disassemble(lo, hi):
    if overlaps_reserved(lo, hi):
        raise RuntimeError('Approved code range overlaps pool/padding %08x..%08x' % (lo, hi))
    listing.clearCodeUnits(toAddr(lo), toAddr(hi - 1), False)
    context.setValue(tmode, toAddr(lo), toAddr(hi - 1), BigInteger.ONE)
    seeds = [lo]
    gap_seeds = []
    disassemble_seed(lo, lo, hi)
    cursor = lo
    while cursor < hi:
        instruction = getInstructionAt(toAddr(cursor))
        if instruction is None:
            containing = listing.getInstructionContaining(toAddr(cursor))
            if containing is not None:
                raise RuntimeError('Instruction overlap at %08x from %s' %
                                   (cursor, containing.getAddress()))
            gap_seeds.append(cursor)
            seeds.append(cursor)
            disassemble_seed(cursor, lo, hi)
            instruction = getInstructionAt(toAddr(cursor))
        if instruction is None:
            raise RuntimeError('Instruction gap remains at %08x in %08x..%08x' % (cursor, lo, hi))
        length = instruction.getLength()
        instruction_hi = cursor + length
        if length <= 0 or instruction_hi > hi or overlaps_reserved(cursor, instruction_hi):
            raise RuntimeError('Instruction bounds failed at %08x len=%d range=%08x..%08x' %
                               (cursor, length, lo, hi))
        cursor = instruction_hi
    if cursor != hi:
        raise RuntimeError('Instruction range end failed %08x..%08x' % (lo, hi))
    DISASM_SEEDS.append({'lo': lo, 'hi': hi, 'initial_seed': lo,
                         'gap_seeds': gap_seeds, 'seeds': seeds})
    COUNTS['CODE_RANGE'] += 1


def apply_probe_ranges():
    for group in CODE_GROUPS:
        for lo, hi in group:
            clear_and_disassemble(lo, hi)
        COUNTS['R4_REGION'] += 1


def verify_probe_state():
    require(len(DISASM_SEEDS) == 80 and
            [(row['lo'], row['hi']) for row in DISASM_SEEDS] == CODE_RANGES,
            'PROBE_RANGE_RECORDS')
    for lo, hi in CODE_RANGES:
        cursor = lo
        while cursor < hi:
            instruction = getInstructionAt(toAddr(cursor))
            require(instruction is not None, 'PROBE_INSTRUCTION_AT %08x' % cursor)
            if instruction is None:
                break
            length = instruction.getLength()
            instruction_hi = cursor + length
            require(length > 0 and instruction_hi <= hi,
                    'PROBE_INSTRUCTION_BOUNDS %08x' % cursor)
            require(not overlaps_reserved(cursor, instruction_hi),
                    'PROBE_INSTRUCTION_RESERVED %08x' % cursor)
            if length <= 0 or instruction_hi > hi:
                break
            cursor = instruction_hi
        require(cursor == hi, 'PROBE_RANGE_END %08x..%08x' % (lo, hi))
    reserved = [(value, value + 4) for value in NEW_POOLS] + list(PADDING)
    for lo, hi in reserved:
        cursor = lo
        while cursor < hi:
            require(getInstructionAt(toAddr(cursor)) is None and
                    listing.getInstructionContaining(toAddr(cursor)) is None,
                    'PROBE_RESERVED_INSTRUCTION %08x' % cursor)
            cursor += 1
    require(raw_hash(0x080a0b20, 0x080a1338) == PLAN['closure_sha256'],
            'PROBE_CLOSURE_BYTES')
    require(raw_hash(0x080a1658, 0x080a27a0) == PLAN['segment_sha256'],
            'PROBE_SEGMENT_BYTES')
    coverage = probe_coverage_summary()
    require(sum(row['instruction_count'] for row in coverage) == 1231 and
            sum(row['instruction_bytes'] for row in coverage) == 2640,
            'PROBE_INSTRUCTION_TOTALS')
    verify_direct_edges(True)
    verify_projection_contract(True)


def probe_coverage_summary():
    summaries = []
    for row in DISASM_SEEDS:
        lo = row['lo']
        hi = row['hi']
        cursor = lo
        instruction_count = 0
        instruction_bytes = 0
        while cursor < hi:
            instruction = getInstructionAt(toAddr(cursor))
            if instruction is None:
                raise RuntimeError('Probe summary gap at %08x' % cursor)
            length = instruction.getLength()
            instruction_count += 1
            instruction_bytes += length
            cursor += length
        summaries.append({
            'lo': lo, 'hi': hi, 'initial_seed': row['initial_seed'],
            'gap_seeds': list(row['gap_seeds']), 'seeds': list(row['seeds']),
            'instruction_count': instruction_count,
            'instruction_bytes': instruction_bytes,
            'full_half_open_coverage': cursor == hi and instruction_bytes == hi - lo})
    return summaries


def create_pool(value):
    addr = toAddr(value)
    listing.clearCodeUnits(addr, toAddr(value + 3), False)
    context.setValue(tmode, addr, toAddr(value + 3), BigInteger.ZERO)
    data = listing.createData(addr, DWordDataType.dataType)
    if data is None or data.getLength() != 4 or unicode(data.getDataType().getPathName()) != '/dword':
        raise RuntimeError('DWord dataization failed at %08x' % value)
    COUNTS['POOL_DATA'] += 1
    if value == 0x080a1950:
        COUNTS['DATAIZATION'] += 1


def clear_padding(lo, hi):
    listing.clearCodeUnits(toAddr(lo), toAddr(hi - 1), False)
    context.setValue(tmode, toAddr(lo), toAddr(hi - 1), BigInteger.ZERO)


def ensure_slot_label(value, name):
    addr = toAddr(value)
    existing = symbols.getPrimarySymbol(addr)
    if existing is None:
        existing = symbols.createLabel(addr, name, SourceType.USER_DEFINED)
    elif unicode(existing.getName()) != name or str(existing.getSource()) != 'USER_DEFINED':
        if existing.getParentNamespace() != currentProgram.getGlobalNamespace():
            existing.setNameAndNamespace(name, currentProgram.getGlobalNamespace(), SourceType.USER_DEFINED)
        else:
            existing.setName(name, SourceType.USER_DEFINED)
    existing = symbols.getPrimarySymbol(addr)
    if existing is None or unicode(existing.getName()) != name:
        raise RuntimeError('Slot label failure at %08x' % value)
    existing.setPrimary()
    if len(list(symbols.getSymbols(addr))) != 1:
        raise RuntimeError('Slot alias at %08x' % value)


def apply_ref(row):
    addr = toAddr(row['addr'])
    for ref in list(references.getReferencesFrom(addr)):
        if ref.getOperandIndex() == 0:
            references.delete(ref)
    ref = references.addMemoryReference(addr, toAddr(row['value']), RefType.DATA,
                                        SourceType.USER_DEFINED, 0)
    references.setPrimary(ref, True)


def apply_slot(row):
    value = row['addr']
    if row['action'] == 'EQ':
        eq = equates.getEquate(row['target'])
        if eq is None:
            eq = equates.createEquate(row['target'], row['value'])
        elif (eq.getValue() & 0xffffffff) != row['value']:
            raise RuntimeError('Equate value conflict: ' + row['target'])
        eq.addReference(toAddr(value), 0)
    elif row['action'] == 'REF':
        apply_ref(row)
    elif row['action'] != 'RENAME':
        raise RuntimeError('Unknown action at %08x' % value)
    ensure_slot_label(value, row['slot_label'])
    listing.setComment(toAddr(value), CodeUnit.EOL_COMMENT, row['eol'])
    COUNTS[row['action']] += 1
    COUNTS['EOL'] += 1


def set_card_message_signature(fn):
    uint_type = UnsignedIntegerDataType.dataType
    ushort_type = UnsignedShortDataType.dataType
    params = [
        ParameterImpl('player_id', uint_type, currentProgram, SourceType.USER_DEFINED),
        ParameterImpl('card_id', ushort_type, currentProgram, SourceType.USER_DEFINED),
        ParameterImpl('unused_row_value', ushort_type, currentProgram, SourceType.USER_DEFINED),
    ]
    fn.replaceParameters(Function.FunctionUpdateType.DYNAMIC_STORAGE_FORMAL_PARAMS,
                         True, SourceType.USER_DEFINED, *params)
    fn.setReturnType(uint_type, SourceType.USER_DEFINED)


def verify_card_message_signature(fn):
    params = list(fn.getParameters())
    require(len(params) == 3 and
            [unicode(param.getName()) for param in params] ==
            ['player_id', 'card_id', 'unused_row_value'] and
            [unicode(param.getDataType().getName()) for param in params] ==
            ['uint', 'ushort', 'ushort'] and
            unicode(fn.getReturnType().getName()) == 'uint', 'FUNCTION_0B20_APCS_SIGNATURE')


def set_functions():
    local_entry = toAddr(0x080a131c)
    provisional = getFunctionAt(local_entry)
    if provisional is not None:
        if provisional.getEntryPoint() != local_entry:
            raise RuntimeError('Local epilogue belongs to a non-local Function before body creation')
        if not functions.removeFunction(local_entry):
            raise RuntimeError('Failed to remove provisional local epilogue Function')
    if getFunctionAt(local_entry) is not None:
        raise RuntimeError('Local epilogue Function remains')
    existing = getFunctionAt(toAddr(0x080a1658))
    if existing is None or long(existing.getSymbol().getID()) != 16936:
        raise RuntimeError('Existing Function identity changed')
    existing.setBody(exact_body(BODY_RANGES[0x080a1658]))
    existing.setName(NEW_NAME, SourceType.USER_DEFINED)
    COUNTS['FUNC_RENAME'] += 1
    for value in NEW_FUNCTIONS:
        if getFunctionAt(toAddr(value)) is not None:
            raise RuntimeError('New Function preexists at %08x' % value)
        created = functions.createFunction(FUNCTION_NAMES[value], toAddr(value),
                                           exact_body(BODY_RANGES[value]), SourceType.USER_DEFINED)
        if created is None:
            raise RuntimeError('Function create failed at %08x' % value)
        if value == 0x080a0b20:
            set_card_message_signature(created)
        COUNTS['FUNC_CREATE'] += 1


def apply_after_normalization():
    apply_probe_ranges()
    for lo, hi in PADDING:
        clear_padding(lo, hi)
    for value in sorted(NEW_POOLS):
        create_pool(value)
    for value in sorted(SLOTS):
        apply_slot(SLOTS[value])
    for value, name, text in LOCAL_LABELS:
        listing.setComment(toAddr(value), CodeUnit.EOL_COMMENT, text)
        COUNTS['EOL'] += 1
    set_functions()
    for value, text in sorted(PLATES.items()):
        listing.setComment(toAddr(value), CodeUnit.PLATE_COMMENT, text)
        COUNTS['PLATE'] += 1


def apply_all():
    normalize_targets_and_cases()
    normalize_local_labels()
    apply_after_normalization()


def refs_core(value):
    return [basic_ref(ref, False) for ref in references.getReferencesFrom(toAddr(value))]


def verify_post(receipt=None):
    require(functions.getFunctionCount() == 5212, 'FUNCTION_COUNT_POST')
    require(raw_hash(0x080a0b20, 0x080a1338) == PLAN['closure_sha256'], 'CLOSURE_BYTES_POST')
    require(raw_hash(0x080a1658, 0x080a27a0) == PLAN['segment_sha256'], 'SEGMENT_BYTES_POST')
    for lo, hi in CODE_RANGES:
        cursor = lo
        while cursor < hi:
            instruction = getInstructionAt(toAddr(cursor))
            require(instruction is not None and cursor + instruction.getLength() <= hi,
                    'CODE_POST %08x' % cursor)
            if instruction is None:
                break
            require(mode_at(cursor) == 1, 'TMODE_CODE_POST %08x' % cursor)
            cursor += instruction.getLength()
        require(cursor == hi, 'CODE_END_POST %08x' % lo)
    for value in NEW_POOLS:
        data = listing.getDefinedDataAt(toAddr(value))
        require(data is not None and data.getLength() == 4 and
                unicode(data.getDataType().getPathName()) == '/dword' and
                getInstructionAt(toAddr(value)) is None and getFunctionContaining(toAddr(value)) is None,
                'POOL_POST %08x' % value)
    for lo, hi in PADDING:
        for value in range(lo, hi):
            require(getInstructionAt(toAddr(value)) is None and
                    listing.getDefinedDataAt(toAddr(value)) is None and
                    getFunctionContaining(toAddr(value)) is None,
                    'PADDING_POST %08x' % value)
    for value, row in SLOTS.items():
        require(memory.getInt(toAddr(value)) & 0xffffffff == row['value'], 'SLOT_VALUE_POST %08x' % value)
        primary = symbols.getPrimarySymbol(toAddr(value))
        require(primary is not None and unicode(primary.getName()) == row['slot_label'] and
                str(primary.getSource()) == 'USER_DEFINED' and primary.isPrimary() and
                len(list(symbols.getSymbols(toAddr(value)))) == 1, 'SLOT_LABEL_POST %08x' % value)
        require(listing.getComment(CodeUnit.EOL_COMMENT, toAddr(value)) == row['eol'],
                'SLOT_EOL_POST %08x' % value)
        if row['action'] == 'EQ':
            eq = equates.getEquate(row['target'])
            refs = [] if eq is None else [ref for ref in eq.getReferences()
                                          if ref.getAddress() == toAddr(value) and ref.getOpIndex() == 0]
            require(eq is not None and (eq.getValue() & 0xffffffff) == row['value'] and len(refs) == 1,
                    'EQ_POST %08x' % value)
        elif row['action'] == 'REF':
            same('REF_POST %08x' % value, operand_zero_refs(value), [{
                'from': '%08x' % value, 'to': '%08x' % row['value'], 'operand': 0,
                'type': 'DATA', 'source': 'USER_DEFINED', 'primary': True}])
        else:
            same('RENAME_REF_POST %08x' % value, operand_zero_refs(value), expected_rename_refs(value))
    for value, name, data_type, length in TARGET_CONTRACTS:
        primary = symbols.getPrimarySymbol(toAddr(value))
        data = listing.getDefinedDataAt(toAddr(value))
        require(primary is not None and unicode(primary.getName()) == name and
                str(primary.getSource()) == 'USER_DEFINED' and primary.isPrimary() and
                len(list(symbols.getSymbols(toAddr(value)))) == 1, 'TARGET_SYMBOL_POST %08x' % value)
        require(data is not None and unicode(data.getDataType().getPathName()) == data_type and
                data.getLength() == length, 'TARGET_DATA_POST %08x' % value)
    for value, name in CASE_LABELS:
        primary = symbols.getPrimarySymbol(toAddr(value))
        require(primary is not None and unicode(primary.getName()) == name and
                str(primary.getSource()) == 'USER_DEFINED' and primary.isPrimary() and
                len(list(symbols.getSymbols(toAddr(value)))) == 1, 'CASE_LABEL_POST %08x' % value)
    for value, name, text in LOCAL_LABELS:
        primary = symbols.getPrimarySymbol(toAddr(value))
        owner = getFunctionContaining(toAddr(value))
        require(primary is not None and unicode(primary.getName()) == name and
                str(primary.getSource()) == 'USER_DEFINED' and primary.isPrimary() and
                len(list(symbols.getSymbols(toAddr(value)))) == 1 and
                getFunctionAt(toAddr(value)) is None and
                owner is not None and owner.getEntryPoint() == toAddr(0x080a0b20) and
                listing.getComment(CodeUnit.EOL_COMMENT, toAddr(value)) == text,
                'LOCAL_EPILOGUE_POST %08x' % value)
    for value, ranges in BODY_RANGES.items():
        fn = getFunctionAt(toAddr(value))
        require(fn is not None and unicode(fn.getName()) == FUNCTION_NAMES[value] and
                str(fn.getBody()) == str(exact_body(ranges)), 'FUNCTION_BODY_POST %08x' % value)
        if value == 0x080a1658:
            require(long(fn.getSymbol().getID()) == 16936, 'FUNCTION_ID_1658_POST')
        elif receipt is not None:
            require(long(fn.getSymbol().getID()) == receipt['function_ids']['%08x' % value],
                    'NEW_FUNCTION_ID_POST %08x' % value)
        if value == 0x080a0b20:
            verify_card_message_signature(fn)
    same('FUNCTION_0B20_INCOMING_POST',
         [basic_ref(ref, False) for ref in references.getReferencesTo(toAddr(0x080a0b20))], [{
             'from': '080a18ba', 'to': '080a0b20', 'operand': 0,
             'type': 'UNCONDITIONAL_CALL', 'source': 'DEFAULT', 'primary': True}])
    same('FUNCTION_1658_INCOMING_POST',
         [basic_ref(ref, False) for ref in references.getReferencesTo(toAddr(0x080a1658))], [{
             'from': '08094d30', 'to': '080a1658', 'operand': 0,
             'type': 'UNCONDITIONAL_CALL', 'source': 'DEFAULT', 'primary': True}])
    same('FUNCTION_1F68_INCOMING_POST',
         [basic_ref(ref, False) for ref in references.getReferencesTo(toAddr(0x080a1f68))], [{
             'from': '080a1732', 'to': '080a1f68', 'operand': 0,
             'type': 'UNCONDITIONAL_CALL', 'source': 'DEFAULT', 'primary': True}])
    require(list(references.getReferencesTo(toAddr(0x080a24cc))) == [], 'FUNCTION_24CC_NO_INCOMING')
    verify_direct_edges(True)
    verify_projection_contract(True)
    for addr, value in PLAN['switch_entries']:
        require(memory.getInt(toAddr(addr)) & 0xffffffff == value and value % 2 == 0,
                'SWITCH_VALUE_POST %08x' % addr)
    for addr, value in PLAN['odd_callbacks']:
        require(memory.getInt(toAddr(addr)) & 0xffffffff == value and value % 2 == 1,
                'CALLBACK_VALUE_POST %08x' % addr)
    for value, text in PLATES.items():
        actual = listing.getComment(CodeUnit.PLATE_COMMENT, toAddr(value))
        require(actual == text and len(actual) < 500 and all(ord(char) < 128 for char in actual),
                'PLATE_POST %08x' % value)
    for lo, hi in RULE3:
        expected = []
        cursor = lo
        while cursor < hi:
            expected.append(CODE_BEFORE[cursor])
            cursor += CODE_BEFORE[cursor]['length']
        same('RULE3_POST %08x' % lo, range_units(lo, hi), expected)
    # All original Functions other than the approved body/name retain identity and body bytes;
    # only the nine approved PLATE payloads may differ.
    for value, old in FUNCTIONS_BEFORE.items():
        actual = function_state(value)
        require(actual is not None and actual['symbol_id'] == old['symbol_id'] and
                actual['source'] == old['source'] and actual['symbol_type'] == old['symbol_type'],
                'EXISTING_FUNCTION_ID_POST %08x' % value)
        if value == 0x080a1658:
            require(actual['name'] == NEW_NAME, 'FUNCTION_RENAME_POST')
        else:
            require(actual['name'] == old['name'] and actual['body'] == old['body'] and
                    actual['body_size'] == old['body_size'] and actual['body_sha256'] == old['body_sha256'],
                    'EXISTING_FUNCTION_BODY_POST %08x' % value)
        expected_plate = PLATES.get(value, old['plate'])
        require(actual['plate'] == expected_plate, 'EXISTING_FUNCTION_PLATE_POST %08x' % value)
    auto_hits = []
    for scan_lo, scan_hi in ((0x080a0b20, 0x080a1338), (0x080a1658, 0x080a27a0)):
        iterator = symbols.getSymbolIterator(toAddr(scan_lo), True)
        while iterator.hasNext():
            symbol = iterator.next()
            offset = symbol.getAddress().getOffset()
            if offset >= scan_hi:
                break
            name = unicode(symbol.getName())
            if re.match(r'^(?:DAT|DWORD|PTR|UNK|FUN|SUB)_[0-9a-fA-F]{8}$', name):
                auto_hits.append([str(symbol.getAddress()), name])
    require(auto_hits == [], 'RESIDUAL_AUTO_NAMES ' + repr(auto_hits))
    print('POSTCHECK slots=249 EQ=190 REF=33 RENAME=26 R4=4 CODE_RANGES=80 POOL=141 '
          'DATAIZATION=1 FUNC_CREATE=3 FUNC_RENAME=1 PLATE=10 EOL=250 RULE3=2 '
          'EDGES=375 TARGETS=226 FAIL=%d' % len(FAILS))


def capture():
    addresses = set(SLOTS)
    addresses.update(value for value, name, data_type, length in TARGET_CONTRACTS)
    addresses.update(value for value, name in CASE_LABELS)
    addresses.update(value for value, name, text in LOCAL_LABELS)
    addresses.add(READONLY_PROJECTION)
    addresses.update(lo for lo, hi in PADDING)
    rule3_state = []
    for lo, hi in RULE3:
        rule3_state.append({'lo': lo, 'hi': hi, 'units': range_units(lo, hi)})
    function_values = sorted(set(PLAN['existing_functions']) | set(NEW_FUNCTIONS))
    return {
        'script_sha256': SCRIPT_HASH,
        'function_count': functions.getFunctionCount(),
        'closure_sha256': raw_hash(0x080a0b20, 0x080a1338),
        'segment_sha256': raw_hash(0x080a1658, 0x080a27a0),
        'addresses': [describe(value) for value in sorted(addresses)],
        'functions': [function_state(value) for value in function_values],
        'rule3': rule3_state,
    }


def reject(phase):
    if FAILS:
        write_json('f13-seg5-%s-failures.json' % MODE,
                   {'phase': phase, 'FAIL': len(FAILS), 'failures': FAILS})
        raise RuntimeError('%s FAIL=%d' % (phase, len(FAILS)))


print('=== RefineF13Seg5 mode=%s ===' % MODE)
verify_frozen_and_plan()
reject('FROZEN_PLAN')
if MODE == 'check':
    receipt = read_json('f13-seg5-expanded-apply-receipt.json')
    require(receipt['status'] == 'APPLIED_TRANSACTION_POSTCHECK_OK' and
            receipt['script_sha256'] == SCRIPT_HASH, 'PERSISTED_RECEIPT')
    verify_post(receipt)
    reject('PERSISTED_CHECK')
    state = capture()
    same('PERSISTED_EXACT_STATE', state, receipt['after'])
    reject('PERSISTED_EXACT_STATE')
    COUNTS = receipt['counts']
    write_json('f13-seg5-expanded-persisted-check.json', {
        'status': 'PERSISTED_CHECK_OK', 'FAIL': 0, 'script_sha256': SCRIPT_HASH,
        'counts': COUNTS, 'function_ids': receipt['function_ids'], 'exact_saved_state': True})
elif MODE == 'probe':
    verify_prestate()
    reject('PROBE_PREFLIGHT')
    transaction = currentProgram.startTransaction('Refine F13-Seg-5 expanded disassembly probe')
    probe_ok = False
    try:
        apply_probe_ranges()
        verify_probe_state()
        reject('PROBE_COVERAGE')
        coverage = probe_coverage_summary()
        write_json('f13-seg5-expanded-coverage-before-rollback.json', {
            'status': 'EXPANDED_COVERAGE_PASS_BEFORE_ROLLBACK',
            'coverage_FAIL': 0, 'script_sha256': SCRIPT_HASH,
            'plan_sha256': dict(INPUT_HASHES)['output/refine-run-20260831-194634/f13-seg5-expanded-plan.json'],
            'transaction_rollback_pending': True,
            'semantic_actions_applied': False,
            'counts': COUNTS, 'ranges': coverage,
            'range_count': len(coverage),
            'instruction_count': sum(row['instruction_count'] for row in coverage),
            'instruction_bytes': sum(row['instruction_bytes'] for row in coverage),
            'gap_seed_count': sum(len(row['gap_seeds']) for row in coverage)})
        probe_ok = True
    finally:
        currentProgram.endTransaction(transaction, False)
    if not probe_ok:
        raise RuntimeError('PROBE_COVERAGE transaction rolled back')
    print('EXPANDED coverage evidence flushed before forced transaction rollback')
elif MODE == 'symbol_probe':
    verify_prestate()
    reject('SYMBOL_PROBE_PREFLIGHT')
    transaction = currentProgram.startTransaction('Refine F13-Seg-5 retry3 symbol order probe')
    symbol_probe_ok = False
    try:
        before_symbols = probe_approved_phase('before', False)
        before_switch_targets = probe_switch_target_groups('before')
        normalize_targets_and_cases()
        normalize_local_labels()
        normalized_symbols = probe_approved_phase('normalized', True)
        normalized_switch_targets = probe_switch_target_groups('normalized')
        reject('SYMBOL_PROBE_NORMALIZE')
        apply_probe_ranges()
        verify_probe_state()
        post_disasm_symbols = probe_approved_phase('post_disasm', True)
        post_disasm_switch_targets = probe_switch_target_groups('post_disasm')
        reject('SYMBOL_PROBE_POST_DISASM')
        coverage = probe_coverage_summary()
        write_json('f13-seg5-expanded-symbol-probe-before-rollback.json', {
            'status': 'EXPANDED_SYMBOL_PROBE_PASS_BEFORE_ROLLBACK',
            'FAIL': 0, 'script_sha256': SCRIPT_HASH,
            'plan_sha256': dict(INPUT_HASHES)['output/refine-run-20260831-194634/f13-seg5-expanded-plan.json'],
            'transaction_rollback_pending': True,
            'persistent_semantic_actions': False,
            'prenormalize_switch_slots': list(PRENORMALIZE_SWITCH_SLOTS),
            'switch_tables': list(SWITCH_TABLES),
            'before': before_symbols,
            'normalized': normalized_symbols,
            'post_disasm': post_disasm_symbols,
            'id_changes_after_normalize': probe_id_changes(before_symbols, normalized_symbols),
            'id_changes_after_disasm': probe_id_changes(normalized_symbols, post_disasm_symbols),
            'switch_target_groups': {
                'before': before_switch_targets,
                'normalized': normalized_switch_targets,
                'post_disasm': post_disasm_switch_targets},
            'counts': COUNTS, 'coverage': coverage,
            'coverage_range_count': len(coverage),
            'coverage_instruction_count': sum(row['instruction_count'] for row in coverage),
            'coverage_instruction_bytes': sum(row['instruction_bytes'] for row in coverage),
            'coverage_gap_seed_count': sum(len(row['gap_seeds']) for row in coverage)})
        symbol_probe_ok = True
    finally:
        currentProgram.endTransaction(transaction, False)
    if not symbol_probe_ok:
        raise RuntimeError('SYMBOL_PROBE transaction rolled back after failure')
    print('EXPANDED symbol evidence flushed before forced transaction rollback')
elif MODE == 'expanded_probe':
    verify_prestate()
    reject('EXPANDED_PROBE_PREFLIGHT')
    before_capture = capture()
    before_symbols = probe_approved_phase('before', False)
    before_switch_targets = probe_switch_target_groups('before')
    before_local = [probe_symbol_state(value) for value, name, text in LOCAL_LABELS]
    before_projection = projection_state()
    transaction = currentProgram.startTransaction('Refine F13-Seg-5 EXPANDED_PASS full probe')
    expanded_probe_ok = False
    try:
        normalize_targets_and_cases()
        normalize_local_labels()
        normalized_symbols = probe_approved_phase('normalized', True)
        normalized_switch_targets = probe_switch_target_groups('normalized')
        normalized_local = [probe_symbol_state(value) for value, name, text in LOCAL_LABELS]
        require(len(probe_id_changes(before_symbols, normalized_symbols)) == 27,
                'EXPANDED_PROBE_RETRY3_ID_CHANGE_COUNT')
        reject('EXPANDED_PROBE_NORMALIZE')
        apply_after_normalization()
        verify_probe_state()
        post_symbols = probe_approved_phase('post_apply', True)
        post_switch_targets = probe_switch_target_groups('post_apply')
        post_local = [probe_symbol_state(value) for value, name, text in LOCAL_LABELS]
        verify_post(None)
        reject('EXPANDED_PROBE_POSTCHECK')
        coverage = probe_coverage_summary()
        function_rows = [function_state(value) for value in NEW_FUNCTIONS]
        edge_rows = verify_direct_edges(True)
        write_json('f13-seg5-expanded-probe-before-rollback.json', {
            'status': 'EXPANDED_PROBE_PASS_BEFORE_ROLLBACK',
            'FAIL': 0,
            'script_sha256': SCRIPT_HASH,
            'plan_sha256': dict(INPUT_HASHES)['output/refine-run-20260831-194634/f13-seg5-expanded-plan.json'],
            'edge_ledger_sha256': dict(INPUT_HASHES)['output/refine-run-20260831-194634/F13-Seg-5-expanded-direct-edges.tsv'],
            'transaction_rollback_pending': True,
            'persistent_semantic_actions': False,
            'counts': COUNTS,
            'coverage': coverage,
            'coverage_range_count': len(coverage),
            'coverage_instruction_count': sum(row['instruction_count'] for row in coverage),
            'coverage_instruction_bytes': sum(row['instruction_bytes'] for row in coverage),
            'coverage_gap_seed_count': sum(len(row['gap_seeds']) for row in coverage),
            'coverage_gap_seeds': [seed for row in coverage for seed in row['gap_seeds']],
            'direct_edge_count': len(edge_rows),
            'direct_edge_target_count': len(set(row['target'] for row in edge_rows)),
            'symbols': {
                'before': before_symbols,
                'normalized': normalized_symbols,
                'post_apply': post_symbols,
                'id_changes_after_normalize': probe_id_changes(before_symbols, normalized_symbols),
                'id_changes_after_apply': probe_id_changes(normalized_symbols, post_symbols),
                'switch_target_groups': {
                    'before': before_switch_targets,
                    'normalized': normalized_switch_targets,
                    'post_apply': post_switch_targets}},
            'local_epilogue': {
                'before': before_local, 'normalized': normalized_local,
                'post_apply': post_local, 'function_at_entry': None,
                'owner_function': '080a0b20'},
            'functions': function_rows,
            'projection_before': before_projection,
            'projection_post': projection_state(),
            'before_capture': before_capture,
            'post_capture': capture(),
        })
        expanded_probe_ok = True
    finally:
        currentProgram.endTransaction(transaction, False)
    if not expanded_probe_ok:
        raise RuntimeError('EXPANDED_PROBE transaction rolled back after failure')
    print('EXPANDED full probe evidence flushed before forced transaction rollback')
else:
    verify_prestate()
    reject('PREFLIGHT')
    before = capture()
    if MODE == 'dry':
        COUNTS.update({'EQ': 190, 'REF': 33, 'RENAME': 26, 'EOL': 250, 'PLATE': 10,
                       'R4_REGION': 4, 'CODE_RANGE': 80, 'POOL_DATA': 141,
                       'DATAIZATION': 1, 'FUNC_CREATE': 3, 'FUNC_RENAME': 1})
        write_json('f13-seg5-expanded-dry-state.json', before)
        write_json('f13-seg5-expanded-dry-check.json', {
            'status': 'EXPANDED_DRY_PREFLIGHT_OK', 'FAIL': 0, 'script_sha256': SCRIPT_HASH,
            'input_hashes': INPUT_HASHES, 'counts': COUNTS,
            'slots': 249, 'code_group_ranges': [49, 18, 2, 11],
            'function_pre_count': 5209, 'rule3_ranges': 2,
            'direct_edges': 375, 'direct_edge_targets': 226,
            'complete_state': 'f13-seg5-expanded-dry-state.json'})
    else:
        write_json('f13-seg5-expanded-apply-before.json', before)
        transaction = currentProgram.startTransaction('Refine F13-Seg-5 EXPANDED_PASS actions')
        success = False
        after = None
        function_ids = None
        try:
            apply_all()
            verify_post(None)
            reject('POSTCHECK')
            function_ids = dict(('%08x' % value, long(getFunctionAt(toAddr(value)).getSymbol().getID()))
                                for value in NEW_FUNCTIONS)
            after = capture()
            success = True
        finally:
            currentProgram.endTransaction(transaction, success)
        write_json('f13-seg5-expanded-apply-receipt.json', {
            'status': 'APPLIED_TRANSACTION_POSTCHECK_OK', 'FAIL': 0,
            'script_sha256': SCRIPT_HASH, 'input_hashes': INPUT_HASHES,
            'counts': COUNTS, 'function_ids': function_ids, 'before': before, 'after': after})
reject('FINAL')
print('COUNTS ' + ' '.join('%s=%d' % (name, COUNTS[name]) for name in (
    'EQ', 'REF', 'RENAME', 'R4_REGION', 'CODE_RANGE', 'POOL_DATA', 'DATAIZATION',
    'FUNC_CREATE', 'FUNC_RENAME', 'PLATE', 'EOL')))
print('STATUS: OK mode=%s FAIL=0' % MODE)
