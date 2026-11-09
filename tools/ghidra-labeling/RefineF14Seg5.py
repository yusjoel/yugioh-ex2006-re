# -*- coding: ascii -*-
#@runtime Jython
#@category Ygo-ex2006.Refine
# F14-Seg-5 approved materialization. Phase1 uses prestate/dry/fullrollback only.

import csv
import hashlib
import json
import os
import traceback

from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import RefType, SourceType


csv.field_size_limit(2**27)


ARGS = list(getScriptArgs())
MODE = ARGS[0].lower() if ARGS else 'dry'
if MODE not in ('prestate', 'dry', 'fullrollback', 'apply', 'check'):
    raise RuntimeError('Expected prestate, dry, fullrollback, apply, or check')

ROOT = os.path.abspath(os.path.join(str(getSourceFile().getParentFile()), '..', '..'))
RUN = os.path.join(ROOT, 'output', 'refine-run-20261028-105948')
PLAN_NAME = 'f14-seg5-plan-v5.json'
PRESTATE_NAME = 'f14-seg5-fresh-full-prestate-v5.json'
SNAPSHOT_NAME = 'f14-seg5-source-snapshot-preapply-v5.json'
INPUT_HASHES = {
    'doc/dev/refine/F14-Seg-5.proposal.md': 'e580007963a9f48a70143bd147037115cde75acd55084e22d6ebd359bd9aee76',
    'doc/dev/refine/F14-Seg-5.review.md': '8ca04f453ff22a42a4df375630f767dc6cbe03239f924426b6a0d02a674245da',
    'doc/dev/refine/F14-Seg-5.slots.tsv': '0fe6bd46a8d93421f0ef6f5bc2b6e609ba48c4fae5ccbbf424e7b5acd8e5e5bb',
    'doc/dev/refine/F14-Seg-5.plates.tsv': '756195365a799c3b5c2981777dbc2fbe2f44a01800a52fda228810e24ac23145',
    'output/refine-run-20261028-105948/f14-seg5-freeze-manifest.json': '86fb68f23debb1f4e2b1082c62f04ef749ca1b3c0ba68b3fb8e4fe85b8dc4e7a',
    'output/refine-run-20261028-105948/f14-seg5-review-round2-audit.json': '8b6ab40d78c28268b9740cb2ef6969f3ab43976bac7c5259b95807e7577c3c37',
    'output/refine-run-20261028-105948/root-f14-seg5-input-contract-gate-v2.json': 'bb23a166c386e015e017bb1a3162cf5a8e01a845772e9467f459e32165345f09',
    'output/refine-run-20261028-105948/root-f14-seg5-mode-a-narrow-gate.json': 'a6910705915dbe32614e15532e910cb01a8300673138f5fb1cbaf0a44e664584',
}
AUXILIARY_INPUTS = (
    'root-f14-seg4-independent-post.json',
    'root-f14-seg5-supplement-prestate.json',
    'root-f14-seg5-caller-owner-correction-prestate.json',
    'root-f14-seg5-penalty-equate-prestate.json',
    'root-f14-seg5-penalty-equate-prestate.json.db-gate.json',
    'root-f14-seg5-db-backup.json',
    'root-source-baseline-f14seg5.json',
)
EXPECTED_COUNTS = {
    'EQ_ADD': 132, 'REF_ADD': 10, 'REF_PRESERVE': 8,
    'EOL': 150, 'FUNC_RENAME': 2, 'PLATE': 20,
}
SEGMENT_START = 0x080acc30
SEGMENT_END = 0x080ade8c

listing = currentProgram.getListing()
symbols = currentProgram.getSymbolTable()
references = currentProgram.getReferenceManager()
equates = currentProgram.getEquateTable()
memory = currentProgram.getMemory()
functions = currentProgram.getFunctionManager()
global_ns = currentProgram.getGlobalNamespace()
FAILS = []
COUNTS = dict((key, 0) for key in EXPECTED_COUNTS)


def read_json_path(path):
    with open(path, 'rb') as stream:
        return json.load(stream)


def read_json(name):
    return read_json_path(os.path.join(RUN, name))


def write_json(name, value):
    path = os.path.join(RUN, name)
    with open(path, 'w') as stream:
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


def require(condition, message, actual=None, expected=None):
    if not condition:
        fail(message, actual, expected)


def exact(message, actual, expected):
    left = json.dumps(actual, ensure_ascii=True, sort_keys=True, separators=(',', ':'))
    right = json.dumps(expected, ensure_ascii=True, sort_keys=True, separators=(',', ':'))
    if left != right:
        fail(message, actual, expected)


def sorted_rows(rows):
    return sorted(rows, key=lambda item: json.dumps(item, ensure_ascii=True,
                                                   sort_keys=True, separators=(',', ':')))


def same_set(message, actual, expected):
    exact(message, sorted_rows(actual), sorted_rows(expected))


def reject(phase):
    if FAILS:
        write_json('f14-seg5-%s-failures.json' % MODE, {
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
        'target_primary_type': None if primary is None else str(primary.getSymbolType()),
        'target_primary_source': None if primary is None else str(primary.getSource()),
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


def instruction_row(inst):
    if inst is None:
        return None
    return {
        'address': str(inst.getAddress()),
        'length': int(inst.getLength()),
        'text': unicode(inst.toString()),
        'flow_type': str(inst.getFlowType()),
        'fallthrough': None if inst.getFallThrough() is None else str(inst.getFallThrough()),
        'flow_override': str(inst.getFlowOverride()),
    }


def tmode_at(addr):
    register = currentProgram.getRegister('TMode')
    if register is None:
        return None
    value = currentProgram.getProgramContext().getValue(register, addr, False)
    if value is None:
        return None
    return int(safe_value(lambda: value.longValue(), value))


def address_state(value):
    addr = toAddr(value)
    primary = symbols.getPrimarySymbol(addr)
    symbol_list = [symbol_row(item) for item in symbols.getSymbols(addr)]
    raw = bytes_hex(value, 4)
    fn_at = functions.getFunctionAt(addr)
    fn_containing = functions.getFunctionContaining(addr)
    return {
        'address': '0x%08x' % value,
        'bytes': raw,
        'rom_word': None if raw is None else long(memory.getInt(addr) & 0xffffffff),
        'symbols': symbol_list,
        'symbol_count': len(symbol_list),
        'primary_symbol': None if primary is None else symbol_row(primary),
        'data_at': data_row(listing.getDefinedDataAt(addr)),
        'data_containing': data_row(listing.getDefinedDataContaining(addr)),
        'instruction_at': instruction_row(listing.getInstructionAt(addr)),
        'function_at': None if fn_at is None else {
            'entry': str(fn_at.getEntryPoint()), 'name': unicode(fn_at.getName()),
            'id': long(fn_at.getSymbol().getID()),
        },
        'function_containing': None if fn_containing is None else {
            'entry': str(fn_containing.getEntryPoint()), 'name': unicode(fn_containing.getName()),
            'id': long(fn_containing.getSymbol().getID()),
        },
        'references_from': [ref_row(ref) for ref in references.getReferencesFrom(addr)],
        'references_to': [ref_row(ref) for ref in references.getReferencesTo(addr)],
        'equates': sorted([{'name': unicode(eq.getName()),
                            'value': long(eq.getValue()) & 0xffffffff}
                           for eq in equates.getEquates(addr)],
                          key=lambda row: (row['name'], row['value'])),
        'eol': listing.getComment(CodeUnit.EOL_COMMENT, addr),
        'plate': listing.getComment(CodeUnit.PLATE_COMMENT, addr),
        'tmode': tmode_at(addr),
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
        for ref in references.getReferencesFrom(item):
            body_refs.append(ref_row(ref))
        eol = listing.getComment(CodeUnit.EOL_COMMENT, item)
        if eol is not None:
            eols.append({'address': '0x%08x' % long(item.getOffset()), 'text': unicode(eol)})
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


def unit_row(value):
    addr = toAddr(value)
    unit = listing.getCodeUnitContaining(addr)
    fn = functions.getFunctionContaining(addr)
    return {
        'address': '0x%08x' % value,
        'byte': '%02x' % (memory.getByte(addr) & 255),
        'unit_min': None if unit is None else str(unit.getMinAddress()),
        'unit_max': None if unit is None else str(unit.getMaxAddress()),
        'unit_length': None if unit is None else int(unit.getLength()),
        'unit_class': None if unit is None else unit.getClass().getSimpleName(),
        'instruction_at': instruction_row(listing.getInstructionAt(addr)),
        'defined_data_at': data_row(listing.getDefinedDataAt(addr)),
        'function_owner': None if fn is None else {
            'entry': str(fn.getEntryPoint()), 'name': unicode(fn.getName()),
            'id': long(fn.getSymbol().getID()),
        },
        'tmode': tmode_at(addr),
    }


def equate_global_row(name):
    eq = equates.getEquate(name)
    if eq is None:
        return None
    refs = []
    for ref in eq.getReferences():
        refs.append({'address': str(ref.getAddress()), 'operand': int(ref.getOpIndex())})
    return {'name': unicode(eq.getName()), 'value': long(eq.getValue()) & 0xffffffff,
            'references': sorted(refs, key=lambda row: (row['address'], row['operand']))}


SLOT_ROWS = read_tsv('doc/dev/refine/F14-Seg-5.slots.tsv')
PLATE_ROWS = read_tsv('doc/dev/refine/F14-Seg-5.plates.tsv')
SLOTS = dict((int(row['address'], 16), row) for row in SLOT_ROWS)
PLATES = dict((int(row['entry'], 16), row) for row in PLATE_ROWS)
RENAMES = dict((value, row) for value, row in PLATES.items()
               if row['current_name'] != row['final_name'])


def load_observer_functions():
    first = read_json('root-f14-seg4-independent-post.json')['functions']
    second = read_json('root-f14-seg5-supplement-prestate.json')['functions']
    third = read_json('root-f14-seg5-caller-owner-correction-prestate.json')['functions']
    rows = {}
    for row in first + second + third:
        if row is not None:
            rows[int(row['entry'], 16)] = row
    return sorted(rows)


OBSERVER_FUNCTIONS = load_observer_functions()
TARGETS = sorted(set(int(row['original_value'], 16) for row in SLOT_ROWS
                     if row['action'].startswith('REF_')))
CONSUMERS = set()
for row in SLOT_ROWS:
    for ref in json.loads(row['refs_to_json']):
        CONSUMERS.add(int(ref['from'], 16))
for row in PLATE_ROWS:
    if row['current_name'] != row['final_name']:
        for ref in json.loads(row['incoming_json']):
            CONSUMERS.add(int(ref['from'], 16))
CONSUMERS = sorted(CONSUMERS)
EQUATE_NAMES = sorted(set(item['name'] for row in SLOT_ROWS
                           for item in json.loads(row['after_equates_json'])))
EXTERNAL_EQUATE_NAMES = sorted(
    read_json('root-f14-seg4-independent-post.json')['external_equate_aliases'].keys())
PROTECTED_EQUATE_NAMES = sorted(EXTERNAL_EQUATE_NAMES + ['ZONE_EFFECT_ATK_PENALTY_500'])
ALL_EQUATE_NAMES = sorted(set(EQUATE_NAMES + PROTECTED_EQUATE_NAMES))
PENALTY_SOURCE_ADDRESSES = [0x08037e14, 0x08037e2c, 0x08037e44,
                            0x08037e5c, 0x080650ec]


def verify_inputs():
    for relative, digest in sorted(INPUT_HASHES.items()):
        exact('INPUT_HASH_' + relative, file_hash(os.path.join(ROOT, relative)), digest)
    manifest = read_json_path(os.path.join(ROOT,
        'output/refine-run-20261028-105948/f14-seg5-freeze-manifest.json'))
    require(len(manifest['review_basis']) == 21, 'REVIEW_BASIS_COUNT')
    for item in manifest['review_basis']:
        exact('REVIEW_BASIS_' + item['path'],
              [file_hash(os.path.join(ROOT, item['path'])),
               os.path.getsize(os.path.join(ROOT, item['path']))],
              [item['sha256'], long(item['size'])])
    require(len(SLOTS) == 150 and len(SLOT_ROWS) == 150, 'SLOT_COUNT')
    for action in ('EQ_ADD', 'REF_ADD', 'REF_PRESERVE'):
        require(sum(row['action'] == action for row in SLOT_ROWS) == EXPECTED_COUNTS[action],
                action + '_COUNT')
    require(len(PLATES) == 20 and len(RENAMES) == 2, 'FUNCTION_PLATE_COUNTS')
    require(len(TARGETS) == 7, 'TARGET_COUNT')
    require(len(OBSERVER_FUNCTIONS) == 202, 'OBSERVER_FUNCTION_COUNT')
    require(len(CONSUMERS) == 153, 'CONSUMER_COUNT', len(CONSUMERS), 153)
    require(len(EXTERNAL_EQUATE_NAMES) == 7, 'EXTERNAL_GLOBAL_EQUATE_COUNT')
    require(len(PROTECTED_EQUATE_NAMES) == 8, 'PROTECTED_GLOBAL_EQUATE_COUNT')
    require(len(EQUATE_NAMES) == 109, 'PLANNED_GLOBAL_EQUATE_COUNT')
    require(len(ALL_EQUATE_NAMES) == 117, 'ALL_GLOBAL_EQUATE_COUNT')
    type_counts = {}
    for row in SLOT_ROWS:
        type_counts[row['final_data_type']] = type_counts.get(row['final_data_type'], 0) + 1
        require(all(ord(char) < 128 for char in row['new_eol_ascii']),
                'EOL_ASCII_' + row['address'])
        require(row['final_symbol_source'] == 'USER_DEFINED',
                'SOURCE_LABEL_SOURCE_' + row['address'])
    exact('SOURCE_DATA_TYPES', type_counts, {'/undefined4': 138, '/pointer': 6, '/dword': 6})
    for value, row in sorted(PLATES.items()):
        text = row['new_plate']
        require(all(ord(char) < 128 for char in text) and len(text) <= 500 and
                len(text) == int(row['new_plate_chars']), 'PLATE_ASCII_%08x' % value)
    reject('INPUTS')


def capture():
    return {
        'status': 'F14_SEG5_FRESH_FULL_PRESTATE',
        'program_name': unicode(currentProgram.getName()),
        'function_count': int(functions.getFunctionCount()),
        'segment': {'start': '0x%08x' % SEGMENT_START,
                    'end': '0x%08x' % SEGMENT_END,
                    'size': SEGMENT_END - SEGMENT_START,
                    'sha256': raw_hash(SEGMENT_START, SEGMENT_END)},
        'functions': [function_row(value) for value in OBSERVER_FUNCTIONS],
        'slots': [address_state(value) for value in sorted(SLOTS)],
        'targets': [address_state(value) for value in TARGETS],
        'consumers': [address_state(value) for value in CONSUMERS],
        'protected_penalty_slots': [address_state(value) for value in PENALTY_SOURCE_ADDRESSES],
        'equate_globals': dict((name, equate_global_row(name)) for name in ALL_EQUATE_NAMES),
        'units': [unit_row(value) for value in range(SEGMENT_START, SEGMENT_END)],
    }


def json_field(row, field):
    value = row[field]
    return json.loads(value) if value else None


def require_slot_pre(value, row, state):
    require(state['rom_word'] == int(row['original_value'], 16) and
            state['bytes'] == row['old_bytes'], 'SLOT_VALUE_%08x' % value)
    exact('SLOT_SYMBOLS_%08x' % value, state['symbols'], json.loads(row['old_symbols_json']))
    exact('SLOT_PRIMARY_%08x' % value, state['primary_symbol'], json.loads(row['old_primary_json']))
    same_set('SLOT_REFS_FROM_%08x' % value, state['references_from'],
             json.loads(row['refs_from_json']))
    same_set('SLOT_REFS_TO_%08x' % value, state['references_to'],
             json.loads(row['refs_to_json']))
    exact('SLOT_EQUATES_%08x' % value, state['equates'], json.loads(row['equates_json']))
    exact('SLOT_EOL_%08x' % value, state['eol'], json.loads(row['old_eol_json']))
    require(state['data_at'] is not None and
            state['data_at']['type'] == row['old_data_type'] and
            state['data_at']['length'] == 4, 'SLOT_DATA_%08x' % value)
    owner = None if state['function_containing'] is None else state['function_containing']['name']
    expected_owner = json.loads(row['old_function_owner'])
    require(owner == expected_owner, 'SLOT_OWNER_%08x' % value)


def require_external_state(value, actual, expected, prefix):
    for key in ('address', 'bytes', 'rom_word', 'symbols', 'symbol_count',
                'primary_symbol', 'data_at', 'data_containing', 'function_at',
                'function_containing', 'references_from', 'references_to',
                'equates', 'eol', 'plate', 'tmode'):
        if key in expected:
            if key in ('references_from', 'references_to'):
                same_set('%s_%s_%08x' % (prefix, key.upper(), value),
                         actual[key], expected[key])
            else:
                exact('%s_%s_%08x' % (prefix, key.upper(), value),
                      actual[key], expected[key])
    if 'instruction' in expected:
        exact('%s_INSTRUCTION_%08x' % (prefix, value),
              actual['instruction_at'], expected['instruction'])


def bool_field(value):
    return value.lower() == 'true'


def require_function_pre(value, row, actual):
    require(actual is not None, 'FUNCTION_PRESENT_%08x' % value)
    require(actual['name'] == row['current_name'] and
            actual['symbol']['id'] == long(row['function_id']) and
            actual['symbol']['source'] == row['function_source'] and
            actual['symbol']['type'] == row['symbol_type'] and
            actual['namespace']['name'] == row['namespace'] and
            actual['namespace']['id'] == long(row['namespace_id']),
            'FUNCTION_IDENTITY_%08x' % value)
    require(actual['body'] == row['body'] and
            actual['body_ranges'] == json.loads(row['body_ranges_json']) and
            actual['body_size'] == int(row['body_size']) and
            actual['body_sha256'] == row['body_sha256'],
            'FUNCTION_BODY_%08x' % value)
    exact('FUNCTION_INTERFACE_%08x' % value, {
        'calling_convention': actual['calling_convention'],
        'signature_source': actual['signature_source'],
        'prototype': actual['prototype'],
        'custom_variable_storage': actual['custom_variable_storage'],
        'varargs': actual['varargs'], 'inline': actual['inline'],
        'no_return': actual['no_return'], 'external': actual['external'],
        'thunk': actual['thunk'], 'thunk_target': actual['thunk_target'],
        'stack_purge_size': actual['stack_purge_size'],
        'return': actual['return'], 'parameters': actual['parameters'],
        'eol_comments': actual['eol_comments'],
    }, {
        'calling_convention': row['calling_convention'],
        'signature_source': row['signature_source'],
        'prototype': row['prototype'],
        'custom_variable_storage': bool_field(row['custom_variable_storage']),
        'varargs': bool_field(row['varargs']), 'inline': bool_field(row['inline']),
        'no_return': bool_field(row['no_return']), 'external': bool_field(row['external']),
        'thunk': bool_field(row['thunk']), 'thunk_target': json.loads(row['thunk_target']),
        'stack_purge_size': int(row['stack_purge_size']),
        'return': json.loads(row['return_json']),
        'parameters': json.loads(row['parameters_json']),
        'eol_comments': json.loads(row['eol_json']),
    })
    exact('FUNCTION_PLATE_%08x' % value, actual['plate'], json.loads(row['old_plate_json']))
    same_set('FUNCTION_INCOMING_%08x' % value, actual['incoming'],
             json.loads(row['incoming_json']))


def verify_prestate(pre):
    exact('FRESH_PRESTATE_EXACT', capture(), pre)
    require(pre['function_count'] == 5214, 'FUNCTION_COUNT_PRE')
    require(pre['segment']['size'] == 4700, 'SEGMENT_SIZE_PRE')
    for value, row in sorted(SLOTS.items()):
        require_slot_pre(value, row, address_state(value))
        collisions = [symbol for symbol in symbols.getGlobalSymbols(row['final_slot_label'])
                      if symbol.getAddress() != toAddr(value)]
        require(not collisions, 'SLOT_NAME_COLLISION_%08x' % value)
    for value, row in sorted(PLATES.items()):
        actual = function_row(value)
        require_function_pre(value, row, actual)
    for target in TARGETS:
        rows = [row for row in SLOT_ROWS if row['action'].startswith('REF_') and
                int(row['original_value'], 16) == target]
        expected = json.loads(rows[0]['target_prestate_json'])
        require_external_state(target, address_state(target), expected, 'TARGET_PRE')
        for row in rows[1:]:
            exact('TARGET_CONTRACT_DUPLICATE_%08x' % target,
                  json.loads(row['target_prestate_json']), expected)
    penalty = read_json('root-f14-seg5-penalty-equate-prestate.json')
    penalty_rows = dict((int(row['source']['address'], 16), row['state'])
                        for row in penalty['words'])
    for value in PENALTY_SOURCE_ADDRESSES:
        require_external_state(value, address_state(value), penalty_rows[value],
                               'PENALTY_PRE')
    exact('PENALTY_OLD500_GLOBAL_PRE', equate_global_row('ZONE_EFFECT_ATK_PENALTY_500'),
          penalty['penalty_equates']['ZONE_EFFECT_ATK_PENALTY_500'])
    exact('PENALTY_NEW400_GLOBAL_PRE', equate_global_row('ZONE_EFFECT_ATK_PENALTY_400'),
          penalty['penalty_equates']['ZONE_EFFECT_ATK_PENALTY_400'])
    reject('PRESTATE_VERIFY')


def verify_plan(plan, prestate_hash):
    require(plan.get('status') == 'F14_SEG5_PLAN_FROZEN', 'PLAN_STATUS')
    exact('PLAN_INPUT_HASHES', plan.get('input_hashes'), INPUT_HASHES)
    exact('PLAN_COUNTS', plan.get('counts'), EXPECTED_COUNTS)
    require(plan.get('script_sha256') == file_hash(getSourceFile().getAbsolutePath()),
            'PLAN_SCRIPT_HASH')
    require(plan.get('prestate_sha256') == prestate_hash, 'PLAN_PRESTATE_HASH')
    require(plan.get('source_snapshot_manifest') == SNAPSHOT_NAME and
            plan.get('source_snapshot_sha256') == file_hash(os.path.join(RUN, SNAPSHOT_NAME)),
            'PLAN_SNAPSHOT_HASH')
    require(plan.get('segment') == [SEGMENT_START, SEGMENT_END] and
            plan.get('observer_functions') == OBSERVER_FUNCTIONS and
            plan.get('slots') == sorted(SLOTS) and plan.get('targets') == TARGETS and
            plan.get('consumers') == CONSUMERS and
            plan.get('penalty_source_addresses') == PENALTY_SOURCE_ADDRESSES and
            plan.get('planned_equate_names') == EQUATE_NAMES and
            plan.get('protected_equate_names') == PROTECTED_EQUATE_NAMES and
            plan.get('all_equate_names') == ALL_EQUATE_NAMES, 'PLAN_SCOPE')
    for name in AUXILIARY_INPUTS:
        require(plan.get('auxiliary_hashes', {}).get(name) == file_hash(os.path.join(RUN, name)),
                'PLAN_AUX_' + name)
    reject('PLAN_VERIFY')


def ensure_slot_label(value, name):
    addr = toAddr(value)
    current = symbols.getPrimarySymbol(addr)
    if current is None or not current.isPrimary() or len(list(symbols.getSymbols(addr))) != 1:
        raise RuntimeError('Source label precondition failed at %08x' % value)
    if current.getParentNamespace() != global_ns:
        current.setNameAndNamespace(name, global_ns, SourceType.USER_DEFINED)
    else:
        current.setName(name, SourceType.USER_DEFINED)
    post = symbols.getPrimarySymbol(addr)
    if post is None or unicode(post.getName()) != name or str(post.getSource()) != 'USER_DEFINED':
        raise RuntimeError('Source label materialization failed at %08x' % value)


def ensure_ref_target(row):
    value = int(row['original_value'], 16)
    addr = toAddr(value)
    current = symbols.getPrimarySymbol(addr)
    all_symbols = list(symbols.getSymbols(addr))
    if current is None or not current.isPrimary() or len(all_symbols) != 1:
        raise RuntimeError('Target primary precondition failed at %08x' % value)
    expected_name = row['target_final_label']
    if 'dynamic DEFAULT target materialized USER' in row['const_status']:
        if str(current.getSource()) != 'DEFAULT':
            raise RuntimeError('Dynamic target source changed at %08x' % value)
        if current.getParentNamespace() != global_ns:
            current.setNameAndNamespace(expected_name, global_ns, SourceType.USER_DEFINED)
        else:
            current.setName(expected_name, SourceType.USER_DEFINED)
    else:
        frozen = json.loads(row['target_prestate_json'])['primary_symbol']
        if (long(current.getID()) != long(frozen['id']) or
                unicode(current.getName(True)) != expected_name or
                str(current.getSource()) != 'USER_DEFINED' or
                str(current.getSymbolType()) != frozen['type']):
            raise RuntimeError('Static target identity changed at %08x' % value)
    post = symbols.getPrimarySymbol(addr)
    if (post is None or unicode(post.getName(True)) != expected_name or
            str(post.getSource()) != 'USER_DEFINED' or
            str(post.getSymbolType()) != 'Label' or
            post.getParentNamespace() != global_ns or
            len(list(symbols.getSymbols(addr))) != 1):
        raise RuntimeError('Target materialization failed at %08x' % value)


def apply_all():
    for value, row in sorted(SLOTS.items()):
        addr = toAddr(value)
        if (memory.getInt(addr) & 0xffffffff) != int(row['original_value'], 16):
            raise RuntimeError('ROM value changed at %08x' % value)
        action = row['action']
        if action == 'EQ_ADD':
            expected = json.loads(row['after_equates_json'])
            if len(expected) != 1:
                raise RuntimeError('EQ contract malformed at %08x' % value)
            item = expected[0]
            eq = equates.getEquate(item['name'])
            eq_value = int(item['value'], 16)
            if eq is None:
                eq = equates.createEquate(item['name'], eq_value)
            elif (eq.getValue() & 0xffffffff) != eq_value:
                raise RuntimeError('Equate value conflict: ' + item['name'])
            refs = [ref for ref in eq.getReferences()
                    if ref.getAddress() == addr and ref.getOpIndex() == 0]
            if not refs:
                eq.addReference(addr, 0)
            elif len(refs) != 1:
                raise RuntimeError('Equate binding multiplicity at %08x' % value)
        elif action == 'REF_ADD':
            if list(references.getReferencesFrom(addr)):
                raise RuntimeError('REF_ADD source occupied at %08x' % value)
            ensure_ref_target(row)
            target = toAddr(int(row['original_value'], 16))
            ref = references.addMemoryReference(addr, target, RefType.DATA,
                                                 SourceType.USER_DEFINED, 0)
            references.setPrimary(ref, True)
        elif action == 'REF_PRESERVE':
            before = [ref_core(item) for item in json.loads(row['refs_from_json'])]
            actual = [ref_core(ref_row(ref)) for ref in references.getReferencesFrom(addr)]
            if sorted_rows(actual) != sorted_rows(before):
                raise RuntimeError('REF_PRESERVE drift at %08x' % value)
        else:
            raise RuntimeError('Unknown action at %08x' % value)
        ensure_slot_label(value, row['final_slot_label'])
        listing.setComment(addr, CodeUnit.EOL_COMMENT, row['new_eol_ascii'])
        COUNTS[action] += 1
        COUNTS['EOL'] += 1
    for value, row in sorted(RENAMES.items()):
        fn = functions.getFunctionAt(toAddr(value))
        fn.setName(row['final_name'], SourceType.USER_DEFINED)
        COUNTS['FUNC_RENAME'] += 1
    for value, row in sorted(PLATES.items()):
        listing.setComment(toAddr(value), CodeUnit.PLATE_COMMENT, row['new_plate'])
        COUNTS['PLATE'] += 1


def strip_ref_derivatives(rows):
    return [ref_core(item) for item in rows]


def function_static_core(row):
    result = dict((key, row[key]) for key in (
        'entry', 'symbol', 'namespace', 'body', 'body_ranges', 'body_size',
        'body_sha256', 'eol_comments', 'calling_convention', 'signature_source',
        'prototype', 'custom_variable_storage', 'varargs', 'inline', 'no_return',
        'external', 'thunk', 'thunk_target', 'stack_purge_size', 'return', 'parameters'))
    return result


def live_ref_expected(row):
    result = json.loads(json.dumps(row))
    target = int(result['to'], 16)
    primary = symbols.getPrimarySymbol(toAddr(target))
    result['target_primary_id'] = None if primary is None else long(primary.getID())
    result['target_primary_name'] = None if primary is None else unicode(primary.getName(True))
    result['target_primary_type'] = None if primary is None else str(primary.getSymbolType())
    result['target_primary_source'] = None if primary is None else str(primary.getSource())
    return result


def verify_refs_live(prefix, rows):
    for ref in rows:
        exact(prefix + '_%s_%s' % (ref['from'], ref['to']), ref, live_ref_expected(ref))


def verify_slot_post(value, row, before):
    actual = address_state(value)
    require(actual['bytes'] == before['bytes'] and actual['rom_word'] == before['rom_word'] and
            actual['data_at'] == before['data_at'] and
            actual['data_containing'] == before['data_containing'] and
            actual['instruction_at'] == before['instruction_at'] and
            actual['function_at'] == before['function_at'] and
            actual['function_containing'] == before['function_containing'] and
            actual['plate'] == before['plate'] and actual['tmode'] == before['tmode'],
            'SLOT_STATIC_POST_%08x' % value)
    primary = actual['primary_symbol']
    require(actual['symbol_count'] == 1 and primary is not None and
            primary['name'] == row['final_slot_label'] and primary['source'] == 'USER_DEFINED' and
            primary['type'] == 'Label' and primary['primary'] and primary['global'] and
            actual['eol'] == row['new_eol_ascii'], 'SLOT_LABEL_EOL_POST_%08x' % value)
    same_set('SLOT_REFS_TO_POST_%08x' % value,
             strip_ref_derivatives(actual['references_to']),
             strip_ref_derivatives(before['references_to']))
    verify_refs_live('SLOT_REFS_TO_DERIVED_%08x' % value, actual['references_to'])
    after_refs = [live_ref_expected(item)
                  for item in json.loads(row['after_refs_from_json'])]
    same_set('SLOT_REFS_FROM_POST_%08x' % value, actual['references_from'], after_refs)
    expected_eq = [{'name': item['name'], 'value': int(item['value'], 16)}
                   for item in json.loads(row['after_equates_json'])]
    exact('SLOT_EQUATES_POST_%08x' % value, actual['equates'], expected_eq)


def expected_function(before, value):
    result = json.loads(json.dumps(before))
    if value in PLATES:
        result['plate'] = PLATES[value]['new_plate']
    if value in RENAMES:
        old_name = RENAMES[value]['current_name']
        new_name = RENAMES[value]['final_name']
        result['name'] = new_name
        result['symbol']['name'] = new_name
        result['symbol']['qualified_name'] = new_name
        result['prototype'] = result['prototype'].replace(old_name, new_name, 1)
    return result


def verify_post(pre):
    require(int(functions.getFunctionCount()) == pre['function_count'] == 5214,
            'FUNCTION_COUNT_POST')
    require(raw_hash(SEGMENT_START, SEGMENT_END) == pre['segment']['sha256'],
            'SEGMENT_HASH_POST')
    expected_units = json.loads(json.dumps(pre['units']))
    for item in expected_units:
        owner = item['function_owner']
        if owner is not None:
            entry = int(owner['entry'], 16)
            if entry in RENAMES:
                owner['name'] = RENAMES[entry]['final_name']
    exact('UNITS_POST', [unit_row(value) for value in range(SEGMENT_START, SEGMENT_END)],
          expected_units)
    pre_slots = dict((int(row['address'], 16), row) for row in pre['slots'])
    pre_targets = dict((int(row['address'], 16), row) for row in pre['targets'])
    pre_consumers = dict((int(row['address'], 16), row) for row in pre['consumers'])
    pre_functions = dict((int(row['entry'], 16), row) for row in pre['functions'])
    for value, row in sorted(SLOTS.items()):
        verify_slot_post(value, row, pre_slots[value])
    for target in TARGETS:
        actual = address_state(target)
        before = pre_targets[target]
        dynamic = target == 0x0201e500
        for key in ('bytes', 'rom_word',
                    'data_at', 'data_containing', 'instruction_at', 'function_at',
                    'function_containing', 'references_from', 'equates', 'eol', 'plate', 'tmode'):
            exact('TARGET_%s_POST_%08x' % (key.upper(), target), actual[key], before[key])
        if dynamic:
            primary = actual['primary_symbol']
            require(actual['symbol_count'] == 1 and primary is not None and
                    primary['name'] == 'gEquipLpZoneEntryBase' and
                    primary['qualified_name'] == 'gEquipLpZoneEntryBase' and
                    primary['type'] == 'Label' and primary['source'] == 'USER_DEFINED' and
                    primary['primary'] and primary['global'], 'DYNAMIC_TARGET_POST')
            exact('DYNAMIC_TARGET_SYMBOL_LIST', actual['symbols'], [primary])
        else:
            exact('TARGET_SYMBOLS_POST_%08x' % target, actual['symbols'], before['symbols'])
            exact('TARGET_SYMBOL_COUNT_POST_%08x' % target,
                  actual['symbol_count'], before['symbol_count'])
            exact('TARGET_PRIMARY_POST_%08x' % target,
                  actual['primary_symbol'], before['primary_symbol'])
        expected_to = [ref_core(item) for item in before['references_to']]
        for value, row in sorted(SLOTS.items()):
            if row['action'] == 'REF_ADD' and int(row['original_value'], 16) == target:
                expected_to.append(ref_core(json.loads(row['after_refs_from_json'])[0]))
        same_set('TARGET_REFS_TO_POST_%08x' % target,
                 strip_ref_derivatives(actual['references_to']), expected_to)
        verify_refs_live('TARGET_REFS_TO_DERIVED_%08x' % target,
                         actual['references_to'])
    for name in EQUATE_NAMES:
        before = pre['equate_globals'][name]
        actual = equate_global_row(name)
        planned = []
        value = None
        for slot, row in sorted(SLOTS.items()):
            for item in json.loads(row['after_equates_json']):
                if item['name'] == name:
                    value = int(item['value'], 16)
                    planned.append({'address': '%08x' % slot, 'operand': int(item['operand'])})
        before_refs = [] if before is None else list(before['references'])
        require(actual is not None and actual['value'] == value, 'GLOBAL_EQ_VALUE_' + name)
        same_set('GLOBAL_EQ_REFS_' + name, actual['references'], before_refs + planned)
    for name in PROTECTED_EQUATE_NAMES:
        exact('PROTECTED_GLOBAL_EQ_' + name,
              equate_global_row(name), pre['equate_globals'][name])
    pre_penalty = dict((int(row['address'], 16), row)
                       for row in pre['protected_penalty_slots'])
    for value in PENALTY_SOURCE_ADDRESSES:
        exact('PROTECTED_PENALTY_SLOT_%08x' % value,
              address_state(value), pre_penalty[value])
    for value in CONSUMERS:
        actual = address_state(value)
        before = pre_consumers[value]
        same_set('CONSUMER_REF_CORE_%08x' % value,
                 strip_ref_derivatives(actual['references_from']),
                 strip_ref_derivatives(before['references_from']))
        for ref in actual['references_from']:
            target = int(ref['to'], 16)
            primary = symbols.getPrimarySymbol(toAddr(target))
            expected_primary = {
                'target_primary_id': None if primary is None else long(primary.getID()),
                'target_primary_name': None if primary is None else unicode(primary.getName(True)),
                'target_primary_type': None if primary is None else str(primary.getSymbolType()),
                'target_primary_source': None if primary is None else str(primary.getSource()),
            }
            exact('CONSUMER_DERIVED_PRIMARY_%08x_%08x' % (value, target),
                  dict((key, ref[key]) for key in expected_primary), expected_primary)
            if target in SLOTS:
                require(primary is not None and
                        ref['target_primary_name'] == SLOTS[target]['final_slot_label'] and
                        ref['target_primary_type'] == 'Label' and
                        ref['target_primary_source'] == 'USER_DEFINED',
                        'CONSUMER_SLOT_DERIVED_%08x_%08x' % (value, target))
            if target in RENAMES:
                require(primary is not None and
                        ref['target_primary_name'] == RENAMES[target]['final_name'] and
                        ref['target_primary_id'] == long(RENAMES[target]['function_id']) and
                        ref['target_primary_type'] == 'Function' and
                        ref['target_primary_source'] == 'USER_DEFINED',
                        'CONSUMER_FUNCTION_DERIVED_%08x_%08x' % (value, target))
    for value in OBSERVER_FUNCTIONS:
        actual = function_row(value)
        before = pre_functions[value]
        expected = expected_function(before, value)
        actual_core = function_static_core(actual)
        expected_core = function_static_core(expected)
        exact('FUNCTION_STATIC_POST_%08x' % value, actual_core, expected_core)
        exact('FUNCTION_PLATE_POST_%08x' % value, actual['plate'], expected['plate'])
        same_set('FUNCTION_INCOMING_CORE_POST_%08x' % value,
                 strip_ref_derivatives(actual['incoming']),
                 strip_ref_derivatives(expected['incoming']))
        same_set('FUNCTION_BODY_REF_CORE_POST_%08x' % value,
                 strip_ref_derivatives(actual['body_references']),
                 strip_ref_derivatives(expected['body_references']))
    if MODE != 'check':
        exact('APPLY_COUNTS', COUNTS, EXPECTED_COUNTS)
    reject('POST_VERIFY')


def failure_payload(phase, error):
    return {
        'status': 'FAIL', 'phase': phase, 'mode': MODE, 'FAIL': len(FAILS),
        'failures': FAILS, 'error': unicode(error), 'traceback': traceback.format_exc(),
        'counts': COUNTS,
    }


print('=== RefineF14Seg5 mode=%s ===' % MODE)
verify_inputs()

if MODE == 'prestate':
    state = capture()
    verify_prestate(state)
    write_json(PRESTATE_NAME, state)
    print('PRESTATE functions=202 slots=150 targets=7 consumers=153 penalty=5 units=4700 FAIL=0')
    print('STATUS: OK mode=prestate read_only=true')
else:
    prestate_path = os.path.join(RUN, PRESTATE_NAME)
    prestate_hash = file_hash(prestate_path)
    prestate = read_json(PRESTATE_NAME)
    plan = read_json(PLAN_NAME)
    verify_plan(plan, prestate_hash)
    if MODE == 'dry':
        verify_prestate(prestate)
        result = {
            'status': 'F14_SEG5_DRY_PREFLIGHT_OK', 'FAIL': 0,
            'script_sha256': file_hash(getSourceFile().getAbsolutePath()),
            'plan_sha256': file_hash(os.path.join(RUN, PLAN_NAME)),
            'prestate_sha256': prestate_hash, 'counts': EXPECTED_COUNTS,
            'preflight': {'functions': 202, 'slots': 150, 'targets': 7,
                          'consumers': 153, 'pc_read_consumers': 152,
                          'rename_call_consumers': 1,
                          'penalty_slots': 5, 'units': 4700,
                          'global_equates': 117},
            'semantic_actions_applied': False,
        }
        write_json('f14-seg5-dry-result-v5.json', result)
        print('STATUS: OK mode=dry FAIL=0 semantic_actions_applied=false')
    elif MODE == 'fullrollback':
        verify_prestate(prestate)
        transaction = currentProgram.startTransaction('F14-Seg-5 Phase1 full rollback validation')
        post_verified = False
        error = None
        try:
            apply_all()
            verify_post(prestate)
            post_verified = True
        except Exception as caught:
            error = caught
            write_json('f14-seg5-full-rollback-failure-v5.json', failure_payload('FULLROLLBACK', caught))
            traceback.print_exc()
        finally:
            currentProgram.endTransaction(transaction, False)
        if not post_verified:
            raise RuntimeError('F14-Seg-5 full rollback validation failed: %s' % unicode(error))
        result = {
            'status': 'F14_SEG5_FULL_ROLLBACK_VALIDATION_OK', 'FAIL': 0,
            'script_sha256': file_hash(getSourceFile().getAbsolutePath()),
            'plan_sha256': file_hash(os.path.join(RUN, PLAN_NAME)),
            'prestate_sha256': prestate_hash, 'counts': EXPECTED_COUNTS,
            'post_verified': True, 'semantic_actions_applied': True,
            'transaction_committed': False,
            'rollback_forced': True,
        }
        write_json('f14-seg5-full-rollback-validation-v5.json', result)
        print('STATUS: OK mode=fullrollback FAIL=0 transaction=rolled_back')
    elif MODE == 'check':
        receipt = read_json('f14-seg5-apply-receipt.json')
        require(receipt.get('status') == 'F14_SEG5_APPLIED_POSTCHECK_OK' and
                receipt.get('counts') == EXPECTED_COUNTS and
                receipt.get('script_sha256') == file_hash(getSourceFile().getAbsolutePath()) and
                receipt.get('plan_sha256') == file_hash(os.path.join(RUN, PLAN_NAME)),
                'RECEIPT_CONTRACT')
        reject('RECEIPT')
        verify_post(prestate)
        write_json('f14-seg5-persisted-check.json', {
            'status': 'F14_SEG5_PERSISTED_CHECK_OK', 'FAIL': 0,
            'script_sha256': receipt['script_sha256'],
            'plan_sha256': receipt['plan_sha256'], 'counts': EXPECTED_COUNTS,
        })
        print('STATUS: OK mode=check FAIL=0')
    else:
        verify_prestate(prestate)
        transaction = currentProgram.startTransaction('F14-Seg-5 approved transaction')
        commit = False
        error = None
        try:
            apply_all()
            verify_post(prestate)
            commit = True
        except Exception as caught:
            error = caught
            write_json('f14-seg5-apply-failure.json', failure_payload('APPLY', caught))
            traceback.print_exc()
        finally:
            currentProgram.endTransaction(transaction, commit)
        if not commit:
            raise RuntimeError('F14-Seg-5 transaction rolled back: %s' % unicode(error))
        receipt = {
            'status': 'F14_SEG5_APPLIED_POSTCHECK_OK', 'FAIL': 0,
            'script_sha256': file_hash(getSourceFile().getAbsolutePath()),
            'plan_sha256': file_hash(os.path.join(RUN, PLAN_NAME)),
            'prestate_sha256': prestate_hash, 'counts': EXPECTED_COUNTS,
        }
        write_json('f14-seg5-apply-receipt.json', receipt)
        print('STATUS: OK mode=apply FAIL=0 transaction=committed')
