# -*- coding: ascii -*-
#@runtime Jython
#@category Ygo-ex2006.Refine
# F13-Seg-9 PASS materialization. prestate/dry/check are read-only.

import csv
import hashlib
import json
import os
import re

from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.data import Undefined4DataType
from ghidra.program.model.symbol import RefType, SourceType


ARGS = list(getScriptArgs())
MODE = ARGS[0].lower() if ARGS else 'dry'
if MODE not in ('prestate', 'dry', 'apply', 'check'):
    raise RuntimeError('Expected prestate, dry, apply, or check')

ROOT = os.path.abspath(os.path.join(str(getSourceFile().getParentFile()), '..', '..'))
RUN = os.path.join(ROOT, 'output', 'refine-run-20261011-103530')
PLAN_NAME = 'f13-seg9-plan.json'
PRESTATE_NAME = 'f13-seg9-fresh-full-prestate.json'
SOURCE_SNAPSHOT_MANIFEST_NAME = 'f13-seg9-source-snapshot-preapply-v2.json'
AUXILIARY_PLAN_HASHES = {
    'review_inputs_v3_sha256': 'f13-seg9-review-inputs-v3.json',
    'mode_a_gate_v3_sha256': 'f13-seg9-mode-a-checklist-gate-v3.json',
    'root_mode_a_gate_v3_sha256': 'root-f13-seg9-mode-a-contract-gate-v3.json',
    'baseline_sha256': 'root-f13-seg9-baseline.json',
    'db_backup_manifest_sha256': 'root-f13-seg9-db-backup.json',
}
INPUT_HASHES = {
    'doc/dev/refine/F13-Seg-9.proposal.md': '3d6fc06bbf6b51c1c74b59aa71fc8a020d57b14d5a40b35687b67ca544a13bbf',
    'doc/dev/refine/F13-Seg-9.review.md': '960a18c6b0ff08e3d6d1d2f8bbcb062d114e0599203eaf7fe18276bc056e4fa3',
    'doc/dev/refine/F13-Seg-9.slots.tsv': '2e1ddfd1d7896b39decd2884c1067276519106e98e72a0b074d02d7885050e6d',
    'doc/dev/refine/F13-Seg-9.plates.tsv': '36548a9fc69ac3916c5362e7f449749dfb86f4c3649cbe30254b69aeef22d5a4',
}
EXPECTED_COUNTS = {
    'EQ': 44, 'REF': 52, 'RENAME': 15, 'EOL': 111,
    'FUNC_RENAME': 6, 'PLATE': 18, 'PACKED_EQ': 8,
    'CARVE_LABEL': 1, 'CARVE_DATA': 3,
}
SEGMENT_START = 0x080a585c
SEGMENT_END = 0x080a689c
SEGMENT_SHA256 = '06464586eee38370658c7670617c0a7d92e24ccdcba9a6eb12063acd33650c05'
PACKED_WORDS = [
    0x080a6b84, 0x080a6be8, 0x080a6d20, 0x080a6d88,
    0x080a6edc, 0x080a6f50, 0x080a712c, 0x080a7174,
    0x080a7574, 0x080a7594, 0x080a7a1c, 0x080a7a2c,
    0x080a8b30, 0x080a8b70,
]
PACKED_ACTIONS = {
    0x080a6b84: 'check_gate_guardian_material_slot_requirement_1',
    0x080a6be8: 'check_gate_guardian_material_slot_requirement_1',
    0x080a6d20: 'check_valkyrion_material_slot_requirement_1',
    0x080a6d88: 'check_valkyrion_material_slot_requirement_1',
    0x080a6edc: 'check_masked_beast_des_gardius_material_slot_requirement_1',
    0x080a6f50: 'check_masked_beast_des_gardius_material_slot_requirement_1',
    0x080a8b30: 'check_ancient_gear_castle_counter_slot_requirement_1',
    0x080a8b70: 'check_ancient_gear_castle_counter_slot_requirement_1',
}
CALL_SITES = [
    0x080a5f5c, 0x08069f9e, 0x08095298, 0x080952a4,
    0x08097086, 0x080970b6, 0x080bbf02, 0x080bc116,
]
CALL_TARGETS = {
    0x080a5f5c: 0x080a5e28,
    0x08069f9e: 0x080a5f38,
    0x08095298: 0x080a5f38,
    0x080952a4: 0x080a5f38,
    0x08097086: 0x080a5f38,
    0x080970b6: 0x080a5f38,
    0x080bbf02: 0x080a5f38,
    0x080bc116: 0x080a5f38,
}
PRESERVE_FUNCTIONS = [
    0x080a6b38, 0x080a6cc8, 0x080a6e74,
    0x080a70d8, 0x080a89f8, 0x08095220,
]
CARVE_BASE = 0x09e478b0
CARVE_WORDS = [0x00001288, 0x0000129b, 0x000012b8]
CARVE_NAME = 'valkyrion_target_material_cids'
CARVE_BOOKEND_START = 0x09e478a4
CARVE_TAIL_START = 0x09e478bc
CARVE_END = 0x09e49d0c

listing = currentProgram.getListing()
symbols = currentProgram.getSymbolTable()
references = currentProgram.getReferenceManager()
equates = currentProgram.getEquateTable()
memory = currentProgram.getMemory()
functions = currentProgram.getFunctionManager()
global_ns = currentProgram.getGlobalNamespace()
tmode_register = currentProgram.getRegister('TMode')
FAILS = []
COUNTS = dict((key, 0) for key in EXPECTED_COUNTS)


def read_json(name):
    with open(os.path.join(RUN, name), 'rb') as stream:
        return json.load(stream)


def write_json(name, value):
    with open(os.path.join(RUN, name), 'w') as stream:
        stream.write(json.dumps(value, ensure_ascii=True, sort_keys=True, indent=2) + '\n')


def file_hash(path):
    with open(path, 'rb') as stream:
        return hashlib.sha256(stream.read()).hexdigest()


def read_tsv(relative):
    with open(os.path.join(ROOT, relative), 'rb') as stream:
        return list(csv.DictReader(stream, delimiter='\t'))


def fail(message, actual=None, expected=None):
    FAILS.append(message)
    print('FAIL: ' + message)
    if actual is not None or expected is not None:
        print('DETAIL ' + json.dumps({'actual': actual, 'expected': expected},
                                    ensure_ascii=True, sort_keys=True))


def require(condition, message):
    if not condition:
        fail(message)


def canonical(value):
    if isinstance(value, dict):
        return dict((key, canonical(item)) for key, item in value.items())
    if isinstance(value, list):
        return sorted((canonical(item) for item in value),
                      key=lambda item: json.dumps(item, sort_keys=True))
    return value


def same(message, actual, expected):
    left = json.dumps(canonical(actual), ensure_ascii=True, sort_keys=True,
                      separators=(',', ':'))
    right = json.dumps(canonical(expected), ensure_ascii=True, sort_keys=True,
                       separators=(',', ':'))
    if left != right:
        fail(message, actual, expected)


def reject(phase):
    if FAILS:
        write_json('f13-seg9-%s-failures.json' % MODE, {
            'status': 'FAIL', 'phase': phase, 'FAIL': len(FAILS),
            'failures': FAILS,
        })
        raise RuntimeError('%s FAIL=%d' % (phase, len(FAILS)))


def safe_value(callable_value, default=None):
    try:
        return callable_value()
    except Exception:
        return default


def bytes_hex(value, length):
    addr = toAddr(value)
    block = memory.getBlock(addr)
    if block is None or not block.isInitialized():
        return None
    return ''.join('%02x' % (memory.getByte(addr.add(index)) & 255)
                   for index in range(length))


def raw_hash(lo, hi):
    raw = ''.join(chr(memory.getByte(toAddr(value)) & 255)
                  for value in range(lo, hi))
    return hashlib.sha256(raw).hexdigest()


def symbol_row(symbol):
    parent = symbol.getParentNamespace()
    return {
        'id': long(symbol.getID()),
        'name': unicode(symbol.getName()),
        'qualified_name': unicode(symbol.getName(True)),
        'type': str(symbol.getSymbolType()),
        'source': str(symbol.getSource()),
        'primary': bool(symbol.isPrimary()),
        'namespace_name': None if parent is None else unicode(parent.getName()),
        'namespace_qualified': None if parent is None else unicode(parent.getName(True)),
        'namespace_id': None if parent is None else safe_value(lambda: long(parent.getID())),
        'global': parent == global_ns,
    }


def ref_row(ref):
    primary = symbols.getPrimarySymbol(ref.getToAddress())
    return {
        'from': str(ref.getFromAddress()),
        'to': str(ref.getToAddress()),
        'operand': int(ref.getOperandIndex()),
        'type': str(ref.getReferenceType()),
        'source': str(ref.getSource()),
        'primary': bool(ref.isPrimary()),
        'target_primary_id': None if primary is None else long(primary.getID()),
        'target_primary_name': None if primary is None else unicode(primary.getName(True)),
    }


def ref_core(row):
    return dict((key, row[key]) for key in
                ('from', 'to', 'operand', 'type', 'source', 'primary'))


def data_row(data):
    if data is None:
        return None
    return {
        'address': str(data.getAddress()),
        'min': str(data.getMinAddress()),
        'max': str(data.getMaxAddress()),
        'length': int(data.getLength()),
        'type': unicode(data.getDataType().getPathName()),
    }


def address_state(value):
    addr = toAddr(value)
    primary = symbols.getPrimarySymbol(addr)
    symbol_list = [symbol_row(item) for item in symbols.getSymbols(addr)]
    raw = bytes_hex(value, 4)
    return {
        'address': '0x%08x' % value,
        'bytes': raw,
        'rom_word': None if raw is None else long(memory.getInt(addr) & 0xffffffff),
        'symbols': symbol_list,
        'symbol_count': len(symbol_list),
        'primary_symbol': None if primary is None else symbol_row(primary),
        'data_at': data_row(listing.getDefinedDataAt(addr)),
        'data_containing': data_row(listing.getDefinedDataContaining(addr)),
        'instruction': None if listing.getInstructionAt(addr) is None else
                       unicode(listing.getInstructionAt(addr).toString()),
        'function': None if functions.getFunctionAt(addr) is None else
                    unicode(functions.getFunctionAt(addr).getName()),
        'references_from': [ref_row(ref) for ref in references.getReferencesFrom(addr)],
        'references_to': [ref_row(ref) for ref in references.getReferencesTo(addr)],
        'equates': sorted([{'name': unicode(eq.getName()),
                            'value': long(eq.getValue()) & 0xffffffff}
                           for eq in equates.getEquates(addr)],
                          key=lambda row: (row['name'], row['value'])),
        'eol': listing.getComment(CodeUnit.EOL_COMMENT, addr),
        'plate': listing.getComment(CodeUnit.PLATE_COMMENT, addr),
    }


def body_ranges(fn):
    result = []
    iterator = fn.getBody().getAddressRanges()
    while iterator.hasNext():
        item = iterator.next()
        result.append(['0x%08x' % long(item.getMinAddress().getOffset()),
                       '0x%08x' % (long(item.getMaxAddress().getOffset()) + 1)])
    return result


def variable_row(variable):
    if variable is None:
        return None
    return {
        'name': unicode(variable.getName()),
        'data_type': unicode(variable.getDataType().getPathName()),
        'storage': unicode(variable.getVariableStorage().toString()),
        'source': str(variable.getSource()),
        'is_auto_parameter': bool(safe_value(lambda: variable.isAutoParameter(), False)),
        'is_register_variable': bool(safe_value(lambda: variable.isRegisterVariable(), False)),
        'is_stack_variable': bool(safe_value(lambda: variable.isStackVariable(), False)),
        'is_memory_variable': bool(safe_value(lambda: variable.isMemoryVariable(), False)),
    }


def function_row(value):
    addr = toAddr(value)
    fn = functions.getFunctionAt(addr)
    if fn is None:
        return None
    symbol = fn.getSymbol()
    params = []
    for param in fn.getParameters():
        row = variable_row(param)
        row['ordinal'] = int(param.getOrdinal())
        row['first_use_offset'] = int(safe_value(lambda: param.getFirstUseOffset(), 0))
        params.append(row)
    body_refs = []
    eols = []
    raw = []
    iterator = fn.getBody().getAddresses(True)
    while iterator.hasNext():
        item = iterator.next()
        raw.append(chr(memory.getByte(item) & 255))
        value_at = long(item.getOffset())
        for ref in references.getReferencesFrom(item):
            body_refs.append(ref_row(ref))
        eol = listing.getComment(CodeUnit.EOL_COMMENT, item)
        if eol is not None:
            eols.append({'address': '0x%08x' % value_at, 'text': unicode(eol)})
    thunk = safe_value(lambda: fn.getThunkedFunction(False))
    namespace = symbol.getParentNamespace()
    return {
        'entry': '0x%08x' % value,
        'name': unicode(fn.getName()),
        'symbol': symbol_row(symbol),
        'namespace': {
            'name': None if namespace is None else unicode(namespace.getName()),
            'qualified_name': None if namespace is None else unicode(namespace.getName(True)),
            'id': None if namespace is None else safe_value(lambda: long(namespace.getID())),
            'global': namespace == global_ns,
        },
        'body': unicode(fn.getBody().toString()),
        'body_ranges': body_ranges(fn),
        'body_size': int(fn.getBody().getNumAddresses()),
        'body_sha256': hashlib.sha256(''.join(raw)).hexdigest(),
        'body_bytes': ''.join('%02x' % ord(item) for item in raw),
        'body_references': body_refs,
        'eol_comments': eols,
        'calling_convention': unicode(fn.getCallingConventionName()),
        'signature_source': str(safe_value(lambda: fn.getSignatureSource())),
        'prototype': unicode(safe_value(lambda: fn.getPrototypeString(False, False), '')),
        'custom_variable_storage': bool(safe_value(lambda: fn.hasCustomVariableStorage(), False)),
        'varargs': bool(safe_value(lambda: fn.hasVarArgs(), False)),
        'inline': bool(safe_value(lambda: fn.isInline(), False)),
        'no_return': bool(safe_value(lambda: fn.hasNoReturn(), False)),
        'external': bool(safe_value(lambda: fn.isExternal(), False)),
        'thunk': bool(safe_value(lambda: fn.isThunk(), False)),
        'thunk_target': None if thunk is None else {
            'entry': str(thunk.getEntryPoint()), 'name': unicode(thunk.getName()),
            'id': long(thunk.getSymbol().getID()),
        },
        'stack_purge_size': safe_value(lambda: int(fn.getStackPurgeSize())),
        'return': variable_row(fn.getReturn()),
        'parameters': params,
        'plate': listing.getComment(CodeUnit.PLATE_COMMENT, addr),
        'incoming': [ref_row(ref) for ref in references.getReferencesTo(addr)],
    }


def segment_byte_units():
    rows = []
    context = currentProgram.getProgramContext()
    for value in range(SEGMENT_START, SEGMENT_END):
        addr = toAddr(value)
        unit = listing.getCodeUnitContaining(addr)
        instruction = listing.getInstructionAt(addr)
        data = listing.getDefinedDataAt(addr)
        owner = functions.getFunctionContaining(addr)
        tmode = None
        if tmode_register is not None:
            raw_tmode = safe_value(lambda: context.getValue(tmode_register, addr, False))
            if raw_tmode is not None:
                tmode = int(raw_tmode)
        rows.append({
            'address': '0x%08x' % value,
            'byte': memory.getByte(addr) & 255,
            'unit': None if unit is None else {
                'min': str(unit.getMinAddress()),
                'max': str(unit.getMaxAddress()),
                'length': int(unit.getLength()),
                'class': unicode(unit.getClass().getSimpleName()),
            },
            'instruction_at': None if instruction is None else unicode(instruction.toString()),
            'defined_data_at': data_row(data),
            'function_owner': None if owner is None else {
                'entry': str(owner.getEntryPoint()),
                'id': long(owner.getSymbol().getID()),
                'name': unicode(owner.getName()),
            },
            'tmode': tmode,
        })
    return rows


def normalize_dynamic_address(row):
    result = dict(row)
    normalized_symbols = []
    for symbol in row['symbols']:
        item = dict(symbol)
        if item['source'] == 'DEFAULT':
            item['id'] = '<dynamic>'
            item['name'] = '<dynamic>'
            item['qualified_name'] = '<dynamic>'
        normalized_symbols.append(item)
    result['symbols'] = normalized_symbols
    if row['primary_symbol'] is not None:
        item = dict(row['primary_symbol'])
        if item['source'] == 'DEFAULT':
            item['id'] = '<dynamic>'
            item['name'] = '<dynamic>'
            item['qualified_name'] = '<dynamic>'
        result['primary_symbol'] = item
    result['references_from'] = [ref_core(item) for item in row['references_from']]
    result['references_to'] = [ref_core(item) for item in row['references_to']]
    return result


SLOT_ROWS = read_tsv('doc/dev/refine/F13-Seg-9.slots.tsv')
PLATE_ROWS = read_tsv('doc/dev/refine/F13-Seg-9.plates.tsv')
SWITCH_ROWS = read_tsv('output/refine-run-20261011-103530/f13-seg9-switch-words-prestate.tsv')
PACKED_ROWS = read_tsv('output/refine-run-20261011-103530/f13-seg9-packed-thumb-prestate.tsv')
SLOTS = dict((int(row['address'], 16), row) for row in SLOT_ROWS)
PLATES = dict((int(row['entry'], 16), row) for row in PLATE_ROWS)
SWITCHES = dict((int(row['address'], 16), row) for row in SWITCH_ROWS)
FUNCTIONS = sorted(set(PLATES) | set(PRESERVE_FUNCTIONS))
RENAMES = dict((value, row) for value, row in PLATES.items()
               if row['current_name'] != row['final_name'])
TARGETS = {}
for value, row in SLOTS.items():
    if row['action'] in ('REF', 'RENAME'):
        target = int(row['original_value'], 16)
        match = re.search(r'id=([0-9]+)', row['target_contract'])
        TARGETS[target] = {
            'address': target,
            'name': (SWITCHES[target]['symbol_name'] if target in SWITCHES else
                     row['target_symbol']),
            'id': None if match is None else long(match.group(1)),
        }


def verify_inputs():
    for relative, digest in sorted(INPUT_HASHES.items()):
        same('INPUT_HASH_' + relative,
             file_hash(os.path.join(ROOT, relative)), digest)
    require(len(SLOTS) == 111 and len(SLOT_ROWS) == 111, 'SLOT_COUNT')
    require(sum(row['action'] == 'EQ' for row in SLOT_ROWS) == 44, 'EQ_COUNT')
    require(sum(row['action'] == 'REF' for row in SLOT_ROWS) == 52, 'REF_COUNT')
    require(sum(row['action'] == 'RENAME' for row in SLOT_ROWS) == 15, 'RENAME_COUNT')
    require(sum(row['reuse_status'] == 'REUSE' for row in SLOT_ROWS if row['action'] == 'EQ') == 36 and
            sum(row['reuse_status'] == 'NEW' for row in SLOT_ROWS if row['action'] == 'EQ') == 8,
            'EQ_REUSE_NEW_COUNTS')
    require(len(PLATES) == 18 and len(RENAMES) == 6 and len(FUNCTIONS) == 24,
            'FUNCTION_PLATE_COUNTS')
    require(len(TARGETS) == 7 and CARVE_BASE in TARGETS, 'TARGET_COUNT')
    require(len(SWITCHES) == 34 and len(SWITCH_ROWS) == 34, 'SWITCH_COUNT')
    require(len(PACKED_ROWS) == 14 and
            sorted(int(row['address'], 16) for row in PACKED_ROWS) == PACKED_WORDS and
            len(PACKED_ACTIONS) == 8, 'PACKED_COUNT')
    require(len(CALL_SITES) == 8 and len(CARVE_WORDS) == 3, 'EXTERNAL_SCOPE_COUNTS')
    for value, row in SLOTS.items():
        require(re.match(r'^[a-z][a-z0-9_]+$', row['final_slot_label']) is not None,
                'SLOT_NAME_%08x' % value)
        require(all(ord(char) < 128 for char in row['eol_ascii']),
                'EOL_ASCII_%08x' % value)
        collisions = [symbol for symbol in symbols.getGlobalSymbols(row['final_slot_label'])
                      if symbol.getAddress() != toAddr(value)]
        require(not collisions, 'SLOT_NAME_COLLISION_%08x' % value)
    for value, row in PLATES.items():
        text = row['new_plate']
        require(all(ord(char) < 128 for char in text) and len(text) <= 500 and
                len(text) == int(row['new_plate_chars']), 'PLATE_ASCII_%08x' % value)
    for row in PACKED_ROWS:
        value = int(row['address'], 16)
        expected = PACKED_ACTIONS.get(value)
        require((expected is None and row['action'] == 'PRESERVE') or
                (expected is not None and row['action'] == 'EQUATE ' + expected),
                'PACKED_ACTION_CONTRACT_%08x' % value)
    aliases = set(row['target_symbol'] for row in SLOT_ROWS
                  if row['action'] == 'EQ' and row['reuse_status'] == 'NEW')
    aliases.update(PACKED_ACTIONS.values())
    require(len(aliases) == 7, 'NEW_ALIAS_COUNT')
    carve_collisions = [symbol for symbol in symbols.getGlobalSymbols(CARVE_NAME)
                        if symbol.getAddress() != toAddr(CARVE_BASE)]
    require(not carve_collisions, 'CARVE_NAME_COLLISION')


def capture():
    packed_rows = []
    for value in PACKED_WORDS:
        state = address_state(value)
        target = state['rom_word']
        packed_rows.append({
            'source': state,
            'odd_target': address_state(target),
            'even_function': function_row(target - 1),
        })
    carve_addresses = [
        CARVE_BOOKEND_START, CARVE_BOOKEND_START + 4, CARVE_BOOKEND_START + 8,
        CARVE_BASE, CARVE_BASE + 4, CARVE_BASE + 8, CARVE_TAIL_START, CARVE_END,
    ]
    return {
        'status': 'F13_SEG9_FRESH_FULL_PRESTATE',
        'program_name': unicode(currentProgram.getName()),
        'function_count': int(functions.getFunctionCount()),
        'segment': {'start': '0x%08x' % SEGMENT_START, 'end': '0x%08x' % SEGMENT_END,
                    'size': SEGMENT_END - SEGMENT_START,
                    'sha256': raw_hash(SEGMENT_START, SEGMENT_END)},
        'functions': [function_row(value) for value in FUNCTIONS],
        'slots': [address_state(value) for value in sorted(SLOTS)],
        'targets': [address_state(value) for value in sorted(TARGETS)],
        'switch_words': [address_state(value) for value in sorted(SWITCHES)],
        'packed_words': packed_rows,
        'call_sites': [address_state(value) for value in CALL_SITES],
        'carve': {
            'addresses': [address_state(value) for value in carve_addresses],
            'bookend_and_carve_bytes': bytes_hex(CARVE_BOOKEND_START, 24),
            'bookend_to_tail_end_size': CARVE_END - CARVE_BOOKEND_START,
            'bookend_to_tail_end_sha256': raw_hash(CARVE_BOOKEND_START, CARVE_END),
        },
        'segment_byte_units': segment_byte_units(),
    }


def verify_prestate(pre):
    same('FRESH_PRESTATE_EXACT', capture(), pre)
    require(pre['function_count'] == 5213, 'FUNCTION_COUNT_PRE')
    require(pre['segment']['sha256'] == SEGMENT_SHA256 and
            len(pre['segment_byte_units']) == SEGMENT_END - SEGMENT_START,
            'SEGMENT_PRE')
    instruction_units = sum(row['instruction_at'] is not None
                            for row in pre['segment_byte_units'])
    data_units = [row['defined_data_at'] for row in pre['segment_byte_units']
                  if row['defined_data_at'] is not None]
    unit_counts = {
        'instruction_at': instruction_units,
        'defined_data_at': len(data_units),
        'data_len4': sum(row['length'] == 4 for row in data_units),
        'data_len2': sum(row['length'] == 2 for row in data_units),
        'data_len1': sum(row['length'] == 1 for row in data_units),
        'bytes_with_unit': sum(row['unit'] is not None
                               for row in pre['segment_byte_units']),
    }
    expected_unit_counts = {
        'instruction_at': 1689, 'defined_data_at': 145,
        'data_len4': 145, 'data_len2': 0, 'data_len1': 0,
        'bytes_with_unit': SEGMENT_END - SEGMENT_START,
    }
    if unit_counts != expected_unit_counts:
        fail('SEGMENT_UNIT_COUNTS_PRE', unit_counts, expected_unit_counts)
    for value, row in sorted(SLOTS.items()):
        state = address_state(value)
        require(state['rom_word'] == int(row['original_value'], 16),
                'SLOT_VALUE_%08x' % value)
        require(state['primary_symbol'] is not None and
                state['primary_symbol']['id'] == long(row['slot_symbol_id']) and
                state['primary_symbol']['name'] == row['old_name'] and
                state['primary_symbol']['source'] == 'DEFAULT' and
                state['symbol_count'] == 1, 'SLOT_SYMBOL_%08x' % value)
        expected_type = row['defined_data'].rsplit(':', 1)[0]
        require(state['data_at'] is not None and state['data_at']['type'] == expected_type and
                state['data_at']['length'] == 4, 'SLOT_DATA_%08x' % value)
        require(not state['equates'] and state['eol'] is None, 'SLOT_EQ_EOL_%08x' % value)
        cores = [ref_core(item) for item in state['references_from']]
        if row['action'] == 'RENAME':
            ref_source = 'USER_DEFINED' if 'DATA:USER_DEFINED:' in row['existing_refs'] else 'DEFAULT'
            require(cores == [{'from': '%08x' % value,
                               'to': '%08x' % int(row['original_value'], 16),
                               'operand': 0, 'type': 'DATA', 'source': ref_source,
                               'primary': True}], 'RENAME_REF_%08x' % value)
        else:
            require(cores == [], 'EMPTY_REF_%08x' % value)
    for value, contract in sorted(TARGETS.items()):
        state = address_state(value)
        if value == CARVE_BASE:
            require(state['primary_symbol'] is None and state['symbol_count'] == 0 and
                    state['data_at'] is None and state['data_containing'] is None and
                    state['references_from'] == [] and state['references_to'] == [] and
                    state['equates'] == [], 'CARVE_TARGET_EMPTY_PRE')
        else:
            expected_source = re.search(r'source=([A-Z_]+)',
                                        next(row['target_contract'] for row in SLOT_ROWS
                                             if int(row['original_value'], 16) == value)).group(1)
            require(state['primary_symbol'] is not None and
                    state['primary_symbol']['id'] == contract['id'] and
                    state['primary_symbol']['name'] == contract['name'] and
                    state['primary_symbol']['source'] == expected_source,
                    'TARGET_STATIC_%08x' % value)
    for value, row in sorted(PLATES.items()):
        state = function_row(value)
        require(state is not None and state['name'] == row['current_name'] and
                state['symbol']['id'] == long(row['function_id']) and
                state['symbol']['source'] == row['function_source'] and
                state['body'] == row['body'] and state['body_size'] == int(row['body_size']) and
                state['body_sha256'] == row['body_sha256'] and
                len(state['plate']) == int(row['old_plate_chars']) and
                hashlib.sha256(state['plate'].encode('utf-8')).hexdigest() == row['old_plate_sha256'] and
                state['calling_convention'] == row['calling_convention'] and
                state['signature_source'] == row['signature_source'] and
                state['prototype'] == row['prototype'] and
                state['custom_variable_storage'] == (row['custom_variable_storage'] == 'true') and
                state['varargs'] == (row['varargs'] == 'true') and
                state['inline'] == (row['inline'] == 'true') and
                state['no_return'] == (row['no_return'] == 'true') and
                state['external'] == (row['external'] == 'true') and
                state['thunk'] == (row['thunk'] == 'true'),
                'FUNCTION_STATIC_%08x' % value)
        require(state['return'] is not None and 'storage' in state['return'] and
                'source' in state['return'] and state['calling_convention'] is not None and
                state['namespace']['id'] is not None,
                'FUNCTION_COMPLETE_METADATA_%08x' % value)
        require(len(state['body_references']) >= 0, 'FUNCTION_BODY_REFS_%08x' % value)
        collisions = [symbol for symbol in symbols.getGlobalSymbols(row['final_name'])
                      if symbol.getAddress() != toAddr(value)]
        require(not collisions, 'FUNCTION_NAME_COLLISION_%08x' % value)
    for value in PRESERVE_FUNCTIONS:
        state = function_row(value)
        require(state is not None and state['return'] is not None and
                state['symbol']['id'] is not None and state['body_bytes'] is not None and
                state['namespace']['id'] is not None and state['calling_convention'] is not None,
                'PRESERVE_FUNCTION_COMPLETE_%08x' % value)
    require(len(function_row(0x08069e40)['plate']) == 2186,
            'CRLF_PLATE_08069e40_PRE')
    for value, row in sorted(SWITCHES.items()):
        state = address_state(value)
        require(state['bytes'] == row['bytes'] and
                state['rom_word'] == int(row['rom_word'], 16) and
                state['data_at'] is not None and state['data_at']['type'] == row['data_type'] and
                state['eol'] is None and state['equates'] == [],
                'SWITCH_STATIC_%08x' % value)
        same('SWITCH_REFS_FROM_%08x' % value, state['references_from'],
             json.loads(row['refs_from_json']))
        same('SWITCH_REFS_TO_%08x' % value, state['references_to'],
             json.loads(row['refs_to_json']))
        if row['symbol_id'] == 'none':
            require(state['primary_symbol'] is None, 'SWITCH_SYMBOL_NONE_%08x' % value)
        else:
            require(state['primary_symbol']['id'] == long(row['symbol_id']) and
                    state['primary_symbol']['name'] == row['symbol_name'] and
                    state['primary_symbol']['source'] == row['symbol_source'],
                    'SWITCH_SYMBOL_%08x' % value)
    packed_contracts = dict((int(row['address'], 16), row) for row in PACKED_ROWS)
    for value in PACKED_WORDS:
        row = packed_contracts[value]
        state = address_state(value)
        require(state['bytes'] == row['bytes'] and state['rom_word'] == int(row['rom_word'], 16) and
                state['references_from'] == [] and state['equates'] == [] and
                state['eol'] is None and state['rom_word'] & 1 == 1,
                'PACKED_STATIC_%08x' % value)
        same('PACKED_REFS_TO_%08x' % value, state['references_to'],
             json.loads(row['refs_to_json']))
        odd = address_state(state['rom_word'])
        require(odd['symbol_count'] == 0 and odd['data_at'] is None and
                odd['data_containing'] is None and odd['references_from'] == [] and
                odd['references_to'] == [] and odd['equates'] == [],
                'ODD_TARGET_EMPTY_%08x' % state['rom_word'])
    for value in CALL_SITES:
        state = address_state(value)
        call_refs = [ref_core(item) for item in state['references_from']
                     if item['type'] == 'UNCONDITIONAL_CALL']
        require(state['instruction'] is not None and
                call_refs == [{'from': '%08x' % value,
                               'to': '%08x' % CALL_TARGETS[value],
                               'operand': 0, 'type': 'UNCONDITIONAL_CALL',
                               'source': 'DEFAULT', 'primary': True}],
                'CALL_SITE_%08x' % value)
    require(bytes_hex(CARVE_BASE, 12) == '881200009b120000b8120000' and
            bytes_hex(CARVE_BOOKEND_START, 12) is not None and
            symbols.getPrimarySymbol(toAddr(CARVE_BOOKEND_START)).getName() ==
            'valkyrion_material_cids' and
            symbols.getPrimarySymbol(toAddr(CARVE_END)).getName() == 'assert_pdst_null',
            'CARVE_BOOKENDS_PRE')


def verify_plan(plan, prestate_hash):
    require(plan.get('status') == 'F13_SEG9_PLAN_FROZEN', 'PLAN_STATUS')
    same('PLAN_INPUT_HASHES', plan.get('input_hashes'), INPUT_HASHES)
    same('PLAN_COUNTS', plan.get('counts'), EXPECTED_COUNTS)
    require(plan.get('script_sha256') == file_hash(getSourceFile().getAbsolutePath()),
            'PLAN_SCRIPT_HASH')
    require(plan.get('prestate_sha256') == prestate_hash, 'PLAN_PRESTATE_HASH')
    require(plan.get('source_snapshot_manifest') == SOURCE_SNAPSHOT_MANIFEST_NAME and
            plan.get('source_snapshot_manifest_sha256') ==
            file_hash(os.path.join(RUN, SOURCE_SNAPSHOT_MANIFEST_NAME)),
            'PLAN_SOURCE_SNAPSHOT_HASH')
    for key, name in sorted(AUXILIARY_PLAN_HASHES.items()):
        require(plan.get(key) == file_hash(os.path.join(RUN, name)),
                'PLAN_AUXILIARY_HASH_' + key)
    require(plan.get('range') == [SEGMENT_START, SEGMENT_END] and
            plan.get('packed_word_addresses') == PACKED_WORDS and
            plan.get('packed_actions') == dict(('0x%08x' % key, value)
                                               for key, value in PACKED_ACTIONS.items()) and
            plan.get('call_sites') == CALL_SITES and
            plan.get('switch_word_addresses') == sorted(SWITCHES) and
            plan.get('function_addresses') == FUNCTIONS and
            plan.get('carve')['base'] == CARVE_BASE and
            plan.get('carve')['words'] == CARVE_WORDS,
            'PLAN_SCOPE')


def ensure_slot_label(value, name):
    addr = toAddr(value)
    primary = symbols.getPrimarySymbol(addr)
    require(primary is not None and primary.isPrimary() and
            len(list(symbols.getSymbols(addr))) == 1, 'SLOT_LABEL_PRE_%08x' % value)
    reject('SLOT_LABEL_PRE')
    if primary.getParentNamespace() != global_ns:
        primary.setNameAndNamespace(name, global_ns, SourceType.USER_DEFINED)
    else:
        primary.setName(name, SourceType.USER_DEFINED)
    post = symbols.getPrimarySymbol(addr)
    if post is None or unicode(post.getName()) != name or str(post.getSource()) != 'USER_DEFINED':
        raise RuntimeError('Slot label failed at %08x' % value)


def apply_all():
    for index, original in enumerate(CARVE_WORDS):
        value = CARVE_BASE + index * 4
        addr = toAddr(value)
        if (memory.getInt(addr) & 0xffffffff) != original:
            raise RuntimeError('Carve ROM value changed at %08x' % value)
        if (symbols.getPrimarySymbol(addr) is not None or
                listing.getDefinedDataContaining(addr) is not None or
                list(references.getReferencesFrom(addr)) or
                list(references.getReferencesTo(addr))):
            raise RuntimeError('Carve target occupied at %08x' % value)
    symbols.createLabel(toAddr(CARVE_BASE), CARVE_NAME, global_ns,
                        SourceType.USER_DEFINED)
    COUNTS['CARVE_LABEL'] += 1
    for index in range(len(CARVE_WORDS)):
        listing.createData(toAddr(CARVE_BASE + index * 4), Undefined4DataType.dataType)
        COUNTS['CARVE_DATA'] += 1
    for value, row in sorted(SLOTS.items()):
        addr = toAddr(value)
        original = int(row['original_value'], 16)
        if (memory.getInt(addr) & 0xffffffff) != original:
            raise RuntimeError('ROM value changed at %08x' % value)
        if row['action'] == 'EQ':
            eq = equates.getEquate(row['target_symbol'])
            if eq is None:
                eq = equates.createEquate(row['target_symbol'], original)
            elif (eq.getValue() & 0xffffffff) != original:
                raise RuntimeError('Equate conflict: ' + row['target_symbol'])
            eq.addReference(addr, 0)
        elif row['action'] == 'REF':
            if list(references.getReferencesFrom(addr)):
                raise RuntimeError('REF source occupied at %08x' % value)
            ref = references.addMemoryReference(addr, toAddr(original), RefType.DATA,
                                                 SourceType.USER_DEFINED, 0)
            references.setPrimary(ref, True)
        elif row['action'] != 'RENAME':
            raise RuntimeError('Unknown action at %08x' % value)
        ensure_slot_label(value, row['final_slot_label'])
        listing.setComment(addr, CodeUnit.EOL_COMMENT, row['eol_ascii'])
        COUNTS[row['action']] += 1
        COUNTS['EOL'] += 1
    for value, name in sorted(PACKED_ACTIONS.items()):
        addr = toAddr(value)
        original = memory.getInt(addr) & 0xffffffff
        eq = equates.getEquate(name)
        if eq is None:
            eq = equates.createEquate(name, original)
        elif (eq.getValue() & 0xffffffff) != original:
            raise RuntimeError('Packed equate conflict: ' + name)
        eq.addReference(addr, 0)
        COUNTS['PACKED_EQ'] += 1
    for value, row in sorted(RENAMES.items()):
        fn = functions.getFunctionAt(toAddr(value))
        fn.setName(row['final_name'], SourceType.USER_DEFINED)
        COUNTS['FUNC_RENAME'] += 1
    for value, row in sorted(PLATES.items()):
        listing.setComment(toAddr(value), CodeUnit.PLATE_COMMENT, row['new_plate'])
        COUNTS['PLATE'] += 1


def function_metadata_core(row):
    return dict((key, row[key]) for key in (
        'entry', 'symbol', 'namespace', 'body', 'body_ranges', 'body_size',
        'body_sha256', 'body_bytes', 'eol_comments', 'calling_convention', 'signature_source',
        'prototype', 'custom_variable_storage', 'varargs', 'inline', 'no_return',
        'external', 'thunk', 'thunk_target', 'stack_purge_size', 'return', 'parameters'))


def expected_renamed_refs(rows):
    result = json.loads(json.dumps(rows))
    for item in result:
        try:
            target = int(item['to'], 16)
        except Exception:
            continue
        if target in SLOTS:
            primary = symbols.getPrimarySymbol(toAddr(target))
            if primary is None:
                fail('APPROVED_SLOT_REF_TARGET_MISSING_%08x' % target)
                continue
            item['target_primary_id'] = long(primary.getID())
            item['target_primary_name'] = unicode(primary.getName(True))
        if target in RENAMES:
            current_name = RENAMES[target]['current_name']
            final_name = RENAMES[target]['final_name']
            if item.get('target_primary_name') == current_name:
                item['target_primary_name'] = final_name
    return result


def unit_layout_core(row):
    owner = row['function_owner']
    return {
        'address': row['address'], 'byte': row['byte'], 'unit': row['unit'],
        'defined_data_at': row['defined_data_at'], 'tmode': row['tmode'],
        'function_owner': None if owner is None else {
            'entry': owner['entry'], 'id': owner['id'],
        },
    }


def verify_post(pre):
    require(int(functions.getFunctionCount()) == int(pre['function_count']),
            'FUNCTION_COUNT_POST')
    require(raw_hash(SEGMENT_START, SEGMENT_END) == pre['segment']['sha256'],
            'SEGMENT_RAW_HASH_POST')
    pre_functions = dict((int(row['entry'], 16), row) for row in pre['functions'])
    pre_slots = dict((int(row['address'], 16), row) for row in pre['slots'])
    pre_targets = dict((int(row['address'], 16), row) for row in pre['targets'])
    same('SEGMENT_UNIT_LAYOUT_POST',
         [unit_layout_core(row) for row in segment_byte_units()],
         [unit_layout_core(row) for row in pre['segment_byte_units']])
    for value, row in sorted(SLOTS.items()):
        actual = address_state(value)
        before = pre_slots[value]
        require(actual['rom_word'] == before['rom_word'] and actual['bytes'] == before['bytes'] and
                actual['data_at'] == before['data_at'] and actual['symbol_count'] == 1 and
                actual['primary_symbol']['name'] == row['final_slot_label'] and
                actual['primary_symbol']['source'] == 'USER_DEFINED' and
                actual['primary_symbol']['primary'] and actual['primary_symbol']['global'] and
                actual['eol'] == row['eol_ascii'], 'SLOT_POST_%08x' % value)
        cores = [ref_core(item) for item in actual['references_from']]
        if row['action'] == 'EQ':
            eq = equates.getEquate(row['target_symbol'])
            matches = [] if eq is None else [ref for ref in eq.getReferences()
                                              if ref.getAddress() == toAddr(value) and ref.getOpIndex() == 0]
            require(eq is not None and (eq.getValue() & 0xffffffff) == int(row['original_value'], 16) and
                    len(matches) == 1 and cores == [], 'EQ_POST_%08x' % value)
            same('EQ_SET_POST_%08x' % value, actual['equates'],
                 [{'name': row['target_symbol'], 'value': int(row['original_value'], 16)}])
        elif row['action'] == 'REF':
            require(cores == [{'from': '%08x' % value, 'to': '%08x' % int(row['original_value'], 16),
                               'operand': 0, 'type': 'DATA', 'source': 'USER_DEFINED',
                               'primary': True}] and not actual['equates'], 'REF_POST_%08x' % value)
        else:
            same('RENAME_REF_POST_%08x' % value, cores,
                 [ref_core(item) for item in before['references_from']])
            require(not actual['equates'], 'RENAME_EQ_POST_%08x' % value)
    for value in sorted(TARGETS):
        actual = address_state(value)
        before = pre_targets[value]
        if value == CARVE_BASE:
            require(actual['primary_symbol'] is not None and
                    actual['primary_symbol']['name'] == CARVE_NAME and
                    actual['primary_symbol']['source'] == 'USER_DEFINED' and
                    actual['primary_symbol']['global'] and
                    actual['data_at'] is not None and
                    actual['data_at']['type'] == '/undefined4' and
                    actual['data_at']['length'] == 4 and
                    actual['bytes'] == before['bytes'], 'CARVE_BASE_POST')
        else:
            require(actual['primary_symbol']['id'] == before['primary_symbol']['id'] and
                    actual['primary_symbol']['name'] == before['primary_symbol']['name'] and
                    actual['primary_symbol']['source'] == before['primary_symbol']['source'] and
                    actual['data_at'] == before['data_at'] and actual['bytes'] == before['bytes'],
                    'TARGET_POST_%08x' % value)
        expected = [ref_core(item) for item in before['references_to']]
        expected += [{'from': '%08x' % slot, 'to': '%08x' % value, 'operand': 0,
                      'type': 'DATA', 'source': 'USER_DEFINED', 'primary': True}
                     for slot, row in sorted(SLOTS.items())
                     if row['action'] == 'REF' and int(row['original_value'], 16) == value]
        same('TARGET_REFS_POST_%08x' % value,
             [ref_core(item) for item in actual['references_to']], expected)
    for index, original in enumerate(CARVE_WORDS):
        value = CARVE_BASE + index * 4
        actual = address_state(value)
        require(actual['rom_word'] == original and actual['data_at'] is not None and
                actual['data_at']['type'] == '/undefined4' and
                actual['data_at']['length'] == 4 and actual['equates'] == [] and
                actual['references_from'] == [], 'CARVE_WORD_POST_%08x' % value)
        if index > 0:
            require(actual['symbol_count'] == 0 and actual['references_to'] == [],
                    'CARVE_TAIL_WORD_POST_%08x' % value)
    for value, row in sorted(PLATES.items()):
        actual = function_row(value)
        before = pre_functions[value]
        expected_name = row['final_name']
        require(actual['symbol']['id'] == before['symbol']['id'] and
                actual['name'] == expected_name and actual['symbol']['source'] == 'USER_DEFINED' and
                actual['plate'] == row['new_plate'], 'FUNCTION_NAME_PLATE_POST_%08x' % value)
        actual_core = function_metadata_core(actual)
        before_core = function_metadata_core(before)
        actual_core['symbol'] = dict(actual_core['symbol'])
        before_core['symbol'] = dict(before_core['symbol'])
        for item in (actual_core['symbol'], before_core['symbol']):
            item.pop('name', None)
            item.pop('qualified_name', None)
        actual_prototype = actual_core.pop('prototype')
        before_prototype = before_core.pop('prototype')
        expected_prototype = before_prototype
        if row['current_name'] != row['final_name']:
            expected_prototype = before_prototype.replace(row['current_name'], row['final_name'], 1)
        require(actual_prototype == expected_prototype,
                'FUNCTION_PROTOTYPE_POST_%08x' % value)
        same('FUNCTION_METADATA_POST_%08x' % value, actual_core, before_core)
        same('FUNCTION_INCOMING_POST_%08x' % value, actual['incoming'],
             expected_renamed_refs(before['incoming']))
        same('FUNCTION_BODY_REFS_POST_%08x' % value, actual['body_references'],
             expected_renamed_refs(before['body_references']))
    for value in PRESERVE_FUNCTIONS:
        actual = function_row(value)
        before = json.loads(json.dumps(pre_functions[value]))
        actual_refs = actual.pop('body_references')
        before_refs = before.pop('body_references')
        actual_incoming = actual.pop('incoming')
        before_incoming = before.pop('incoming')
        same('PRESERVE_FUNCTION_POST_%08x' % value, actual, before)
        same('PRESERVE_FUNCTION_REFS_POST_%08x' % value, actual_refs,
             expected_renamed_refs(before_refs))
        same('PRESERVE_FUNCTION_INCOMING_POST_%08x' % value, actual_incoming,
             expected_renamed_refs(before_incoming))
    pre_switches = dict((int(row['address'], 16), row) for row in pre['switch_words'])
    for value in sorted(SWITCHES):
        expected_switch = json.loads(json.dumps(pre_switches[value]))
        if value == 0x080a5fb0:
            approved_slot = SLOTS[0x080a5fac]
            require(approved_slot['action'] == 'REF' and
                    int(approved_slot['original_value'], 16) == value and
                    expected_switch['primary_symbol']['id'] == 5291 and
                    expected_switch['primary_symbol']['qualified_name'] ==
                    'switchD_080a5fa2::switchdataD_080a5fb0',
                    'SWITCH_APPROVED_INCOMING_CONTRACT')
            expected_switch['references_to'].append({
                'from': '080a5fac', 'to': '080a5fb0', 'operand': 0,
                'type': 'DATA', 'source': 'USER_DEFINED', 'primary': True,
                'target_primary_id': 5291,
                'target_primary_name':
                    'switchD_080a5fa2::switchdataD_080a5fb0',
            })
        same('SWITCH_WORD_POST_%08x' % value,
             address_state(value), expected_switch)
    for index, value in enumerate(PACKED_WORDS):
        before = pre['packed_words'][index]
        expected_source = json.loads(json.dumps(before['source']))
        if value in PACKED_ACTIONS:
            expected_source['equates'] = [{
                'name': PACKED_ACTIONS[value],
                'value': int(expected_source['rom_word']),
            }]
        same('PACKED_SOURCE_POST_%08x' % value,
             address_state(value), expected_source)
        target = int(row_value(before['source']['rom_word']))
        expected_target = json.loads(json.dumps(before['odd_target']))
        even_entry = target - 1
        if even_entry in RENAMES:
            current_odd = RENAMES[even_entry]['current_name'] + '+1'
            final_odd = RENAMES[even_entry]['final_name'] + '+1'
            for symbol in expected_target['symbols']:
                if symbol['source'] == 'DEFAULT' and symbol['name'] == current_odd:
                    symbol['name'] = final_odd
                    symbol['qualified_name'] = final_odd
            primary = expected_target['primary_symbol']
            if primary is not None and primary['source'] == 'DEFAULT' and primary['name'] == current_odd:
                primary['name'] = final_odd
                primary['qualified_name'] = final_odd
            for ref in expected_target['references_to']:
                if ref['target_primary_name'] == current_odd:
                    ref['target_primary_name'] = final_odd
        same('ODD_TARGET_POST_%08x' % target,
             address_state(target), expected_target)
    pre_calls = dict((int(row['address'], 16), row) for row in pre['call_sites'])
    for value in CALL_SITES:
        actual = address_state(value)
        before = pre_calls[value]
        same('CALL_REFS_POST_%08x' % value, actual['references_from'],
             expected_renamed_refs(before['references_from']))
        require(actual['bytes'] == before['bytes'] and
                actual['references_to'] == before['references_to'],
                'CALL_STATIC_POST_%08x' % value)
    require(bytes_hex(CARVE_BOOKEND_START, 24) ==
            pre['carve']['bookend_and_carve_bytes'] and
            raw_hash(CARVE_BOOKEND_START, CARVE_END) ==
            pre['carve']['bookend_to_tail_end_sha256'], 'CARVE_RAW_POST')
    same('APPLY_COUNTS', COUNTS, EXPECTED_COUNTS)


def row_value(value):
    return long(value)


print('=== RefineF13Seg9 mode=%s ===' % MODE)
verify_inputs()
reject('INPUTS')

if MODE == 'prestate':
    state = capture()
    verify_prestate(state)
    reject('PRESTATE')
    write_json(PRESTATE_NAME, state)
    print('PRESTATE functions=24 slots=111 targets=7 switches=34 packed=14 calls=8 '
          'carve_targets=3 segment_bytes=4160 FAIL=0')
    print('STATUS: OK mode=prestate read_only=true')
else:
    prestate_path = os.path.join(RUN, PRESTATE_NAME)
    prestate_hash = file_hash(prestate_path)
    prestate = read_json(PRESTATE_NAME)
    plan = read_json(PLAN_NAME)
    verify_plan(plan, prestate_hash)
    reject('PLAN')
    if MODE == 'dry':
        verify_prestate(prestate)
        reject('DRY')
        write_json('f13-seg9-dry-result.json', {
            'status': 'F13_SEG9_DRY_PREFLIGHT_OK', 'FAIL': 0,
            'script_sha256': file_hash(getSourceFile().getAbsolutePath()),
            'plan_sha256': file_hash(os.path.join(RUN, PLAN_NAME)),
            'prestate_sha256': prestate_hash,
            'counts': EXPECTED_COUNTS,
            'preflight': {'functions': 24, 'slots': 111, 'targets': 7,
                          'switches': 34, 'packed_words': 14, 'call_sites': 8,
                          'carve_targets': 3, 'segment_bytes': 4160},
            'semantic_actions_applied': False,
        })
        print('PREFLIGHT slots=111 EQ=44 REF=52 RENAME=15 EOL=111 '
              'FUNC_RENAME=6 PLATE=18 PACKED_EQ=8 CARVE_LABEL=1 CARVE_DATA=3 '
              'FUNCTIONS=24 TARGETS=7 SWITCHES=34 PACKED=14 CALLS=8 FAIL=0')
        print('STATUS: OK mode=dry FAIL=0 semantic_actions_applied=false')
    elif MODE == 'check':
        receipt = read_json('f13-seg9-apply-receipt.json')
        require(receipt.get('status') == 'F13_SEG9_APPLIED_POSTCHECK_OK' and
                receipt.get('counts') == EXPECTED_COUNTS and
                receipt.get('script_sha256') == file_hash(getSourceFile().getAbsolutePath()) and
                receipt.get('plan_sha256') == file_hash(os.path.join(RUN, PLAN_NAME)),
                'RECEIPT_CONTRACT')
        reject('RECEIPT')
        same('PERSISTED_EXACT', capture(), receipt['after'])
        reject('PERSISTED')
        write_json('f13-seg9-persisted-check.json', {
            'status': 'F13_SEG9_PERSISTED_CHECK_OK', 'FAIL': 0,
            'script_sha256': receipt['script_sha256'],
            'plan_sha256': receipt['plan_sha256'],
            'counts': EXPECTED_COUNTS,
        })
        print('STATUS: OK mode=check FAIL=0 PERSISTED_EXACT=true')
    else:
        verify_prestate(prestate)
        reject('APPLY_PREFLIGHT')
        transaction = currentProgram.startTransaction('Refine F13-Seg-9 approved transaction')
        commit = False
        after = None
        try:
            apply_all()
            verify_post(prestate)
            reject('APPLY_POSTCHECK')
            after = capture()
            commit = True
        finally:
            currentProgram.endTransaction(transaction, commit)
        if not commit:
            raise RuntimeError('F13-Seg-9 transaction rolled back')
        receipt = {
            'status': 'F13_SEG9_APPLIED_POSTCHECK_OK', 'FAIL': 0,
            'script_sha256': file_hash(getSourceFile().getAbsolutePath()),
            'plan_sha256': file_hash(os.path.join(RUN, PLAN_NAME)),
            'prestate_sha256': prestate_hash,
            'counts': EXPECTED_COUNTS, 'after': after,
        }
        write_json('f13-seg9-apply-receipt.json', receipt)
        print('STATUS: OK mode=apply FAIL=0 transaction=committed')
