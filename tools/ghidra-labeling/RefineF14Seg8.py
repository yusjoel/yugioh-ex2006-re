# -*- coding: ascii -*-
#@runtime Jython
#@category Ygo-ex2006.Refine
# F14-Seg-8 approved materialization. Phase1 uses prestate/dry/fullrollback only.

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
EVIDENCE_VERSION = 'v4'
PLAN_NAME = 'f14-seg8-plan-v4.json'
PRESTATE_NAME = 'f14-seg8-fresh-full-prestate-v4.json'
SNAPSHOT_NAME = 'f14-seg8-source-snapshot-preapply-v4.json'
INPUT_HASHES = {
    'doc/dev/refine/F14-Seg-8.proposal.md': 'bea333dc5e3a10a29a4e249ae3377fe879976f33aeb2bd0112e3d89f98f3f373',
    'doc/dev/refine/F14-Seg-8.review.md': 'e7900e08f834cebb81ff42883e21bbb87eee0a4b3e124e6182d4c9b3e04849b4',
    'doc/dev/refine/F14-Seg-8.slots.tsv': '9624c1b6e7d82b72dfe518a1c62f53eb6f7605b685d2d0f71a44fc68d3bac8d7',
    'doc/dev/refine/F14-Seg-8.plates.tsv': '021a51cc30f68179a8d3417a2a3fe1a0027dc7efe9955fde03c8b35e8ddcb539',
    'output/refine-run-20261028-105948/f14-seg8-freeze-manifest.json': 'fa023e29fa8ba9b64a65f9c04c680f9ba2d6cc0f7e3348c4a46febd5aa6f355e',
    'output/refine-run-20261028-105948/f14-seg8-semantic-review-round2.json': 'b95eed332596357c9edf421e54da8a14715fa3caef9234708cf66292542bf220',
    'output/refine-run-20261028-105948/root-f14-seg8-input-contract-gate-v2.json': '8f1e8788f933ac8f0fc3db753fcbf3a152554e36fd339375d4c5b08cfcee544f',
    'output/refine-run-20261028-105948/f14-seg8-mode-a-narrow-gate.json': '81b8e77a89846b8d630724ac62b5cdceb762a18ee030c2f6f7717f671815ed11',
}
AUXILIARY_INPUTS = (
    'root-f14-seg8-independent-full-prestate.json',
    'root-f14-seg8-independent-full-prestate-gate.json',
    'root-f14-seg8-independent-full-prestate.json.db-gate.json',
    'root-f14-seg8-prepost-functions-input.json',
    'root-f14-seg8-prepost-words-input.json',
    'root-f14-seg8-prepost-slots-input.json',
    'root-f14-seg8-prepost-equates-input.json',
    'root-f14-seg8-prepost-preparation.json',
    'root-f14-seg8-db-backup.json',
    'root-source-baseline-f14seg8.json',
    'f14-seg8-function-projection-plan.json',
    'f14-seg8-target-contract.json',
)
EXPECTED_COUNTS = {
    'EQ_ADD': 61, 'REF_ADD': 35, 'REF_PRESERVE': 5,
    'EOL': 101, 'FUNC_RENAME': 4, 'PLATE': 14,
}
SEGMENT_START = 0x080b04a8
SEGMENT_END = 0x080b153c
MODULE_START = 0x080a78dc
MODULE_END = 0x080b5348
DYNAMIC_TARGETS = set([0x0201aff8, 0x0201b010, 0x0201b16c, 0x0201b18c])

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
        write_json('f14-seg8-%s-failures-%s.json' % (MODE, EVIDENCE_VERSION), {
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
    equate_references = []
    for eq in equates.getEquates(addr):
        for ref in eq.getReferences():
            if ref.getAddress() == addr:
                equate_references.append({
                    'name': unicode(eq.getName()),
                    'value': long(eq.getValue()) & 0xffffffff,
                    'operand': int(ref.getOpIndex()),
                })
    equate_references = sorted(equate_references,
                               key=lambda row: (row['name'], row['value'], row['operand']))
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
        'equate_references': equate_references,
        'eol': listing.getComment(CodeUnit.EOL_COMMENT, addr),
        'pre': listing.getComment(CodeUnit.PRE_COMMENT, addr),
        'post': listing.getComment(CodeUnit.POST_COMMENT, addr),
        'repeatable': listing.getComment(CodeUnit.REPEATABLE_COMMENT, addr),
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
        'symbols': [symbol_row(item) for item in symbols.getSymbols(addr)],
        'symbol_count': len(list(symbols.getSymbols(addr))),
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


def verify_global_equate_pre(actuals):
    """Compare every frozen Equate exactly, treating its reference list as a set.

    EquateTable.getReferences() does not promise iteration order.  The frozen Java
    observation and Jython observation contain the same complete address/operand
    multiset, so only that outer ordering is normalized here.
    """
    exact('GLOBAL_EQ_PRE_NAMES', sorted(actuals), sorted(GLOBAL_EQ_PRESTATE))
    for name in ALL_EQUATE_NAMES:
        actual = actuals.get(name)
        expected = GLOBAL_EQ_PRESTATE.get(name)
        if actual is None or expected is None:
            exact('GLOBAL_EQ_PRE_%s' % name, actual, expected)
            continue
        exact('GLOBAL_EQ_PRE_%s_NAME' % name, actual.get('name'), expected.get('name'))
        exact('GLOBAL_EQ_PRE_%s_VALUE' % name,
              long(actual.get('value')) & 0xffffffff,
              long(expected.get('value')) & 0xffffffff)
        same_set('GLOBAL_EQ_PRE_%s_REFS' % name,
                 actual.get('references', []), expected.get('references', []))

def json_list_field(row, field):
    raw = row.get(field, '')
    if raw is None or raw == '':
        return []
    value = json.loads(raw)
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def json_value_field(row, field):
    raw = row.get(field, '')
    if raw is None or raw == '':
        return None
    return json.loads(raw)


def json_ranges_field(row, field):
    value = json_list_field(row, field)
    if len(value) == 2 and isinstance(value[0], basestring):
        return [value]
    return value


SLOT_ROWS = read_tsv('doc/dev/refine/F14-Seg-8.slots.tsv')
PLATE_ROWS = read_tsv('doc/dev/refine/F14-Seg-8.plates.tsv')
SLOTS = dict((int(row['address'], 16), row) for row in SLOT_ROWS)
PLATES = dict((int(row['entry'], 16), row) for row in PLATE_ROWS)
RENAMES = dict((value, row) for value, row in PLATES.items()
               if row['current_name'] != row['final_name'])
PLATE_WRITES = dict((value, row) for value, row in PLATES.items()
                    if row['action'] != 'PRESERVE')


def address_list(name):
    return [int(row['address'], 16) for row in read_json(name)]


OBSERVER_FUNCTIONS = address_list('root-f14-seg8-prepost-functions-input.json')
WORD_ADDRESSES = address_list('root-f14-seg8-prepost-words-input.json')
STATE_ADDRESSES = address_list('root-f14-seg8-prepost-slots-input.json')
TARGETS = sorted(set(int(row['original_value'], 16) for row in SLOT_ROWS
                     if row['action'].startswith('REF_')))
PC_CONSUMERS = sorted(set(int(ref['from'], 16) for row in SLOT_ROWS
                          for ref in json_list_field(row, 'refs_to_json')))
RENAME_CONSUMERS = sorted(set(int(ref['from'], 16) for value, row in RENAMES.items()
                              for ref in json_list_field(row, 'incoming_json')))
CONSUMERS = sorted(set(PC_CONSUMERS + RENAME_CONSUMERS))
EQUATE_NAMES = sorted(set(item['name'] for row in SLOT_ROWS
                           for item in json_list_field(row, 'after_equates_json')))
ROOT_FULL_PRESTATE = read_json('root-f14-seg8-independent-full-prestate.json')
ROOT_GLOBAL_EQUATE_NAMES = sorted(ROOT_FULL_PRESTATE['global_equates'])
GLOBAL_EQ_PRESTATE = dict(ROOT_FULL_PRESTATE['global_equates'])
for _planned_name in EQUATE_NAMES:
    if _planned_name not in GLOBAL_EQ_PRESTATE:
        GLOBAL_EQ_PRESTATE[_planned_name] = None
ALL_EQUATE_NAMES = sorted(GLOBAL_EQ_PRESTATE)
PROTECTED_EQUATE_NAMES = sorted(set(ALL_EQUATE_NAMES) - set(EQUATE_NAMES))


def parse_number(value):
    if isinstance(value, (int, long)):
        return long(value) & 0xffffffff
    return long(value, 16) & 0xffffffff


def bool_field(value):
    return value.lower() == 'true'


def verify_inputs():
    for relative, digest in sorted(INPUT_HASHES.items()):
        exact('INPUT_HASH_' + relative, file_hash(os.path.join(ROOT, relative)), digest)
    manifest = read_json('f14-seg8-freeze-manifest.json')
    frozen = manifest['artifacts'] + manifest['evidence'] + manifest['history']
    require(len(frozen) == 35, 'FREEZE_INPUT_COUNT')
    for item in frozen:
        path = os.path.join(ROOT, item['path'])
        exact('FREEZE_' + item['path'],
              [file_hash(path), os.path.getsize(path)],
              [item['sha256'], long(item['size'])])
    require(len(SLOTS) == 101 and len(SLOT_ROWS) == 101, 'SLOT_COUNT')
    for action in ('EQ_ADD', 'REF_ADD', 'REF_PRESERVE'):
        require(sum(row['action'] == action for row in SLOT_ROWS) == EXPECTED_COUNTS[action],
                action + '_COUNT')
    require(len(PLATES) == 15 and len(PLATE_WRITES) == 14 and len(RENAMES) == 4,
            'FUNCTION_PLATE_COUNTS')
    require(len(OBSERVER_FUNCTIONS) == 280 and len(set(OBSERVER_FUNCTIONS)) == 280,
            'OBSERVER_FUNCTION_COUNT')
    require(len(WORD_ADDRESSES) == 1271 and len(set(WORD_ADDRESSES)) == 1271,
            'WORD_OBSERVER_COUNT')
    require(len(STATE_ADDRESSES) == 2978 and len(set(STATE_ADDRESSES)) == 2978,
            'STATE_OBSERVER_COUNT')
    require(len(PC_CONSUMERS) == 114 and len(RENAME_CONSUMERS) == 9 and
            len(CONSUMERS) == 123, 'CONSUMER_COUNTS')
    require(len(TARGETS) == 11 and set(DYNAMIC_TARGETS).issubset(set(TARGETS)),
            'TARGET_COUNTS')
    require(len(ROOT_GLOBAL_EQUATE_NAMES) == 2124 and len(EQUATE_NAMES) == 44 and
            len(PROTECTED_EQUATE_NAMES) == 2085 and
            len(ALL_EQUATE_NAMES) == 2129, 'GLOBAL_EQUATE_COUNTS')
    require(not set(EQUATE_NAMES).intersection(PROTECTED_EQUATE_NAMES),
            'GLOBAL_EQUATE_DISJOINT')
    require(sum(GLOBAL_EQ_PRESTATE[name] is None for name in EQUATE_NAMES) == 5,
            'PLANNED_GLOBAL_EQUATE_NULL_COUNT')
    type_counts = {}
    for row in SLOT_ROWS:
        type_counts[row['old_data_type']] = type_counts.get(row['old_data_type'], 0) + 1
        require(row['final_data_type'] == row['old_data_type'],
                'SLOT_DATA_TYPE_CONTRACT_' + row['address'])
        require(row['final_symbol_source'] == 'USER_DEFINED',
                'SLOT_SOURCE_CONTRACT_' + row['address'])
        require(all(ord(char) < 128 for char in row['new_eol_ascii']),
                'EOL_ASCII_' + row['address'])
    exact('SOURCE_DATA_TYPES', type_counts,
          {'/undefined4': 95, '/dword': 1, '/pointer': 5})
    for value, row in sorted(PLATES.items()):
        text = row['new_plate']
        require(all(ord(char) < 128 for char in text) and len(text) <= 500 and
                len(text) == int(row['new_plate_chars']), 'PLATE_ASCII_%08x' % value)
    require(max(int(row['new_plate_chars']) for row in PLATE_ROWS) == 497,
            'PLATE_MAX_497')
    b0c60 = PLATES[0x080b0c60]
    require(b0c60['prototype'] ==
            'undefined prepare_first_placeable_monster_slot()',
            'B0C60_PROJECTED_PROTOTYPE_INPUT')
    reject('INPUTS')


def capture():
    return {
        'status': 'F14_SEG8_FRESH_FULL_PRESTATE',
        'program_name': unicode(currentProgram.getName()),
        'function_count': int(functions.getFunctionCount()),
        'segment': {'start': '0x%08x' % SEGMENT_START,
                    'end': '0x%08x' % SEGMENT_END,
                    'size': SEGMENT_END - SEGMENT_START,
                    'sha256': raw_hash(SEGMENT_START, SEGMENT_END)},
        'module': {'start': '0x%08x' % MODULE_START,
                   'end': '0x%08x' % MODULE_END,
                   'size': MODULE_END - MODULE_START,
                   'sha256': raw_hash(MODULE_START, MODULE_END)},
        'functions': [function_row(value) for value in OBSERVER_FUNCTIONS],
        'words': [address_state(value) for value in WORD_ADDRESSES],
        'states': [address_state(value) for value in STATE_ADDRESSES],
        'equate_globals': dict((name, equate_global_row(name))
                                for name in ALL_EQUATE_NAMES),
        'units': [unit_row(value) for value in range(MODULE_START, MODULE_END)],
    }


def require_external_state(value, actual, expected, prefix):
    for key in ('address', 'bytes', 'rom_word', 'symbols', 'symbol_count',
                'primary_symbol', 'data_at', 'data_containing', 'function_at',
                'function_containing', 'references_from', 'references_to',
                'equates', 'equate_references', 'eol', 'pre', 'post',
                'repeatable', 'plate', 'tmode'):
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


def require_slot_pre(value, row, state):
    require(state['rom_word'] == int(row['original_value'], 16) and
            state['bytes'] == row['old_bytes'], 'SLOT_VALUE_%08x' % value)
    exact('SLOT_SYMBOLS_%08x' % value, state['symbols'],
          json_list_field(row, 'old_symbols_json'))
    exact('SLOT_PRIMARY_%08x' % value, state['primary_symbol'],
          json_value_field(row, 'old_primary_json'))
    same_set('SLOT_REFS_FROM_%08x' % value, state['references_from'],
             json_list_field(row, 'refs_from_json'))
    same_set('SLOT_REFS_TO_%08x' % value, state['references_to'],
             json_list_field(row, 'refs_to_json'))
    exact('SLOT_EQUATES_%08x' % value, state['equates'],
          json_list_field(row, 'equates_json'))
    require(state['equate_references'] == [], 'SLOT_EQ_REFS_PRE_%08x' % value)
    exact('SLOT_EOL_%08x' % value, state['eol'], json_value_field(row, 'old_eol_json'))
    require(state['data_at'] is not None and state['data_at']['length'] == 4 and
            state['data_at']['type'] == row['old_data_type'], 'SLOT_DATA_%08x' % value)
    owner = None if state['function_containing'] is None else state['function_containing']['name']
    expected_owner = row['old_function_owner'] or None
    require(owner == expected_owner, 'SLOT_OWNER_%08x' % value, owner, expected_owner)


def require_plate_pre(value, row, actual):
    require(actual is not None and actual['name'] == row['current_name'] and
            actual['symbol']['id'] == long(row['function_id']) and
            actual['symbol']['source'] == row['function_source'] and
            actual['symbol']['type'] == row['symbol_type'] and
            actual['namespace']['name'] == row['namespace'] and
            actual['namespace']['id'] == long(row['namespace_id']),
            'FUNCTION_IDENTITY_%08x' % value)
    require(actual['body'] == row['body'] and
            actual['body_ranges'] == json_ranges_field(row, 'body_ranges_json') and
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
        'prototype': (row['prototype'].replace(row['final_name'], row['current_name'], 1)
                      if row['current_name'] != row['final_name'] and
                      row['final_name'] in row['prototype'] else row['prototype']),
        'custom_variable_storage': bool_field(row['custom_variable_storage']),
        'varargs': bool_field(row['varargs']), 'inline': bool_field(row['inline']),
        'no_return': bool_field(row['no_return']), 'external': bool_field(row['external']),
        'thunk': bool_field(row['thunk']),
        'thunk_target': json_value_field(row, 'thunk_target'),
        'stack_purge_size': int(row['stack_purge_size']),
        'return': json_value_field(row, 'return_json'),
        'parameters': json_list_field(row, 'parameters_json'),
        'eol_comments': json_list_field(row, 'eol_json'),
    })
    exact('FUNCTION_PLATE_%08x' % value, actual['plate'],
          json_value_field(row, 'old_plate_json'))
    same_set('FUNCTION_INCOMING_%08x' % value, actual['incoming'],
             json_list_field(row, 'incoming_json'))


def verify_prestate(pre, recapture):
    if recapture:
        exact('FRESH_PRESTATE_EXACT', capture(), pre)
    require(pre['function_count'] == 5215, 'FUNCTION_COUNT_PRE')
    require(pre['segment']['size'] == 4244 and pre['module']['size'] == 55916,
            'RANGE_SIZE_PRE')
    require(len(pre['functions']) == 280 and len(pre['words']) == 1271 and
            len(pre['states']) == 2978 and len(pre['units']) == 55916 and
            len(pre['equate_globals']) == 2129, 'PRESTATE_COUNTS')
    function_map = dict(zip(OBSERVER_FUNCTIONS, pre['functions']))
    state_map = dict((int(row['address'], 16), row) for row in pre['states'])
    require(all(row is not None for row in pre['functions']), 'ALL_FUNCTIONS_PRESENT')
    exact('ROOT_FULL_FUNCTIONS_PRE', pre['functions'], ROOT_FULL_PRESTATE['functions'])
    for value, row in sorted(SLOTS.items()):
        require_slot_pre(value, row, state_map[value])
        collisions = [symbol for symbol in symbols.getGlobalSymbols(row['final_slot_label'])
                      if symbol.getAddress() != toAddr(value)]
        require(not collisions, 'SLOT_NAME_COLLISION_%08x' % value)
    for value, row in sorted(PLATES.items()):
        require_plate_pre(value, row, function_map[value])
    for target in TARGETS:
        rows = [row for row in SLOT_ROWS if row['action'].startswith('REF_') and
                int(row['original_value'], 16) == target]
        expected = json_value_field(rows[0], 'target_prestate_json')
        require_external_state(target, state_map[target], expected, 'TARGET_PRE')
        for row in rows[1:]:
            exact('TARGET_DUPLICATE_%08x' % target,
                  json_value_field(row, 'target_prestate_json'), expected)
    verify_global_equate_pre(pre['equate_globals'])
    reject('PRESTATE_VERIFY')


def verify_plan(plan, prestate_hash):
    require(plan.get('status') == 'F14_SEG8_PLAN_FROZEN', 'PLAN_STATUS')
    exact('PLAN_INPUT_HASHES', plan.get('input_hashes'), INPUT_HASHES)
    exact('PLAN_COUNTS', plan.get('counts'), EXPECTED_COUNTS)
    require(plan.get('script_sha256') == file_hash(getSourceFile().getAbsolutePath()),
            'PLAN_SCRIPT_HASH')
    require(plan.get('prestate_sha256') == prestate_hash, 'PLAN_PRESTATE_HASH')
    require(plan.get('source_snapshot_manifest') == SNAPSHOT_NAME and
            plan.get('source_snapshot_sha256') == file_hash(os.path.join(RUN, SNAPSHOT_NAME)),
            'PLAN_SNAPSHOT_HASH')
    require(plan.get('segment') == [SEGMENT_START, SEGMENT_END] and
            plan.get('module') == [MODULE_START, MODULE_END] and
            plan.get('observer_functions') == OBSERVER_FUNCTIONS and
            plan.get('word_addresses') == WORD_ADDRESSES and
            plan.get('state_addresses') == STATE_ADDRESSES and
            plan.get('slots') == sorted(SLOTS) and plan.get('targets') == TARGETS and
            plan.get('consumers') == CONSUMERS and
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
    if (post is None or unicode(post.getName(True)) != name or
            str(post.getSource()) != 'USER_DEFINED' or
            str(post.getSymbolType()) != 'Label' or not post.isPrimary() or
            post.getParentNamespace() != global_ns or
            len(list(symbols.getSymbols(addr))) != 1):
        raise RuntimeError('Source label materialization failed at %08x' % value)


def ensure_ref_target(row):
    value = int(row['original_value'], 16)
    addr = toAddr(value)
    current = symbols.getPrimarySymbol(addr)
    if current is None or not current.isPrimary() or len(list(symbols.getSymbols(addr))) != 1:
        raise RuntimeError('Target primary precondition failed at %08x' % value)
    expected_name = row['target_final_label']
    if value in DYNAMIC_TARGETS:
        if str(current.getSource()) == 'DEFAULT':
            if current.getParentNamespace() != global_ns:
                current.setNameAndNamespace(expected_name, global_ns, SourceType.USER_DEFINED)
            else:
                current.setName(expected_name, SourceType.USER_DEFINED)
        elif not (str(current.getSource()) == 'USER_DEFINED' and
                  unicode(current.getName(True)) == expected_name and
                  str(current.getSymbolType()) == 'Label' and
                  current.getParentNamespace() == global_ns):
            raise RuntimeError('Dynamic target source changed at %08x' % value)
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
            str(post.getSymbolType()) != 'Label' or not post.isPrimary() or
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
            expected = json_list_field(row, 'after_equates_json')
            if len(expected) != 1:
                raise RuntimeError('EQ contract malformed at %08x' % value)
            item = expected[0]
            eq_value = parse_number(item['value'])
            eq = equates.getEquate(item['name'])
            if eq is None:
                eq = equates.createEquate(item['name'], eq_value)
            elif (eq.getValue() & 0xffffffff) != eq_value:
                raise RuntimeError('Equate value conflict: ' + item['name'])
            matches = [ref for ref in eq.getReferences()
                       if ref.getAddress() == addr and ref.getOpIndex() == int(item['operand'])]
            if not matches:
                eq.addReference(addr, int(item['operand']))
            elif len(matches) != 1:
                raise RuntimeError('Equate binding multiplicity at %08x' % value)
        elif action == 'REF_ADD':
            if list(references.getReferencesFrom(addr)):
                raise RuntimeError('REF_ADD source occupied at %08x' % value)
            ensure_ref_target(row)
            ref = references.addMemoryReference(
                addr, toAddr(int(row['original_value'], 16)), RefType.DATA,
                SourceType.USER_DEFINED, 0)
            references.setPrimary(ref, True)
        elif action == 'REF_PRESERVE':
            before = [ref_core(item) for item in json_list_field(row, 'refs_from_json')]
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
        functions.getFunctionAt(toAddr(value)).setName(
            row['final_name'], SourceType.USER_DEFINED)
        COUNTS['FUNC_RENAME'] += 1
    for value, row in sorted(PLATE_WRITES.items()):
        listing.setComment(toAddr(value), CodeUnit.PLATE_COMMENT, row['new_plate'])
        COUNTS['PLATE'] += 1


def strip_ref_derivatives(rows):
    return [ref_core(item) for item in rows]


def live_ref_expected(row):
    result = json.loads(json.dumps(row))
    try:
        primary = symbols.getPrimarySymbol(toAddr(int(result['to'], 16)))
    except Exception:
        primary = None
    result['target_primary_id'] = None if primary is None else long(primary.getID())
    result['target_primary_name'] = None if primary is None else unicode(primary.getName(True))
    result['target_primary_type'] = None if primary is None else str(primary.getSymbolType())
    result['target_primary_source'] = None if primary is None else str(primary.getSource())
    return result


def live_refs(rows):
    return [live_ref_expected(row) for row in rows]


def ranges_contain(ranges, value):
    return any(int(lo, 16) <= value < int(hi, 16) for lo, hi in ranges)


def projected_identity(before):
    if before is None:
        return None
    result = json.loads(json.dumps(before))
    entry = int(result['entry'], 16)
    if entry in RENAMES:
        result['name'] = RENAMES[entry]['final_name']
    return result


def expected_ref_core_from(before, value):
    rows = [ref_core(item) for item in before]
    if value in SLOTS and SLOTS[value]['action'] == 'REF_ADD':
        rows.extend(ref_core(item) for item in
                    json_list_field(SLOTS[value], 'after_refs_from_json'))
    return rows


def expected_ref_core_to(before, value):
    rows = [ref_core(item) for item in before]
    for source, row in sorted(SLOTS.items()):
        if row['action'] == 'REF_ADD' and int(row['original_value'], 16) == value:
            rows.extend(ref_core(item) for item in
                        json_list_field(row, 'after_refs_from_json'))
    return rows


def verify_live_refs(prefix, rows):
    for item in rows:
        exact(prefix + '_' + item['from'] + '_' + item['to'], item, live_ref_expected(item))


def verify_state_post(value, before):
    actual = address_state(value)
    require(actual['bytes'] == before['bytes'] and actual['rom_word'] == before['rom_word'] and
            actual['instruction_at'] == before['instruction_at'] and
            actual['pre'] == before['pre'] and actual['post'] == before['post'] and
            actual['repeatable'] == before['repeatable'] and actual['tmode'] == before['tmode'],
            'STATE_STATIC_%08x' % value)
    exact('STATE_DATA_AT_%08x' % value, actual['data_at'], before['data_at'])
    exact('STATE_DATA_CONTAINING_%08x' % value,
          actual['data_containing'], before['data_containing'])
    expected_eol = SLOTS[value]['new_eol_ascii'] if value in SLOTS else before['eol']
    expected_plate = (PLATE_WRITES[value]['new_plate']
                      if value in PLATE_WRITES else before['plate'])
    exact('STATE_EOL_%08x' % value, actual['eol'], expected_eol)
    exact('STATE_PLATE_%08x' % value, actual['plate'], expected_plate)
    exact('STATE_FUNCTION_AT_%08x' % value,
          actual['function_at'], projected_identity(before['function_at']))
    exact('STATE_FUNCTION_CONTAINING_%08x' % value,
          actual['function_containing'], projected_identity(before['function_containing']))

    primary = actual['primary_symbol']
    if value in SLOTS:
        require(actual['symbol_count'] == 1 and primary is not None and
                primary['name'] == SLOTS[value]['final_slot_label'] and
                primary['type'] == 'Label' and primary['source'] == 'USER_DEFINED' and
                primary['primary'] and primary['global'], 'STATE_SLOT_SYMBOL_%08x' % value)
    elif value in DYNAMIC_TARGETS:
        expected_name = next(row['target_final_label'] for row in SLOT_ROWS
                             if int(row['original_value'], 16) == value)
        require(actual['symbol_count'] == 1 and primary is not None and
                primary['name'] == expected_name and primary['type'] == 'Label' and
                primary['source'] == 'USER_DEFINED' and primary['primary'] and
                primary['global'], 'STATE_DYNAMIC_TARGET_%08x' % value)
    elif value in RENAMES:
        expected_symbols = json.loads(json.dumps(before['symbols']))
        for item in expected_symbols:
            if item['type'] == 'Function' and item['id'] == long(RENAMES[value]['function_id']):
                item['name'] = RENAMES[value]['final_name']
                item['qualified_name'] = RENAMES[value]['final_name']
        expected_primary = json.loads(json.dumps(before['primary_symbol']))
        expected_primary['name'] = RENAMES[value]['final_name']
        expected_primary['qualified_name'] = RENAMES[value]['final_name']
        exact('STATE_RENAME_SYMBOLS_%08x' % value, actual['symbols'], expected_symbols)
        exact('STATE_RENAME_PRIMARY_%08x' % value, actual['primary_symbol'], expected_primary)
    else:
        exact('STATE_SYMBOLS_%08x' % value, actual['symbols'], before['symbols'])
        exact('STATE_PRIMARY_%08x' % value, actual['primary_symbol'], before['primary_symbol'])

    same_set('STATE_REFS_FROM_CORE_%08x' % value,
             strip_ref_derivatives(actual['references_from']),
             expected_ref_core_from(before['references_from'], value))
    same_set('STATE_REFS_TO_CORE_%08x' % value,
             strip_ref_derivatives(actual['references_to']),
             expected_ref_core_to(before['references_to'], value))
    verify_live_refs('STATE_REFS_FROM_LIVE_%08x' % value, actual['references_from'])
    verify_live_refs('STATE_REFS_TO_LIVE_%08x' % value, actual['references_to'])

    if value in SLOTS:
        expected_eq = [{'name': item['name'], 'value': parse_number(item['value'])}
                       for item in json_list_field(SLOTS[value], 'after_equates_json')]
        expected_eq_refs = [{'name': item['name'], 'value': parse_number(item['value']),
                             'operand': int(item['operand'])}
                            for item in json_list_field(SLOTS[value], 'after_equates_json')]
        exact('STATE_EQUATES_%08x' % value, actual['equates'], expected_eq)
        exact('STATE_EQ_REFS_%08x' % value, actual['equate_references'], expected_eq_refs)
    else:
        exact('STATE_EQUATES_%08x' % value, actual['equates'], before['equates'])
        exact('STATE_EQ_REFS_%08x' % value,
              actual['equate_references'], before['equate_references'])


def function_static_core(row):
    return dict((key, row[key]) for key in (
        'entry', 'name', 'symbol', 'symbols', 'symbol_count', 'namespace',
        'body', 'body_ranges', 'body_size',
        'body_sha256', 'eol_comments', 'calling_convention', 'signature_source',
        'prototype', 'custom_variable_storage', 'varargs', 'inline', 'no_return',
        'external', 'thunk', 'thunk_target', 'stack_purge_size', 'return',
        'parameters', 'plate'))


def projected_function(before, value):
    result = json.loads(json.dumps(before))
    if value in RENAMES:
        old_name = RENAMES[value]['current_name']
        new_name = RENAMES[value]['final_name']
        result['name'] = new_name
        result['symbol']['name'] = new_name
        result['symbol']['qualified_name'] = new_name
        for item in result['symbols']:
            if item['id'] == result['symbol']['id'] and item['type'] == 'Function':
                item['name'] = new_name
                item['qualified_name'] = new_name
        result['prototype'] = result['prototype'].replace(old_name, new_name, 1)
    if value in PLATE_WRITES:
        result['plate'] = PLATE_WRITES[value]['new_plate']
    eols = dict((int(item['address'], 16), item['text']) for item in before['eol_comments'])
    for slot, row in SLOTS.items():
        if ranges_contain(before['body_ranges'], slot):
            eols[slot] = row['new_eol_ascii']
    result['eol_comments'] = [{'address': '0x%08x' % address, 'text': eols[address]}
                              for address in sorted(eols)]
    refs = list(before['body_references'])
    for slot, row in SLOTS.items():
        if row['action'] == 'REF_ADD' and ranges_contain(before['body_ranges'], slot):
            refs.extend(json_list_field(row, 'after_refs_from_json'))
    result['body_references'] = live_refs(refs)
    result['incoming'] = live_refs(before['incoming'])
    return result


def verify_units_post(pre):
    for before in pre['units']:
        value = int(before['address'], 16)
        actual = unit_row(value)
        for key in ('address', 'byte', 'unit_min', 'unit_max', 'unit_length',
                    'unit_class', 'instruction_at', 'defined_data_at', 'tmode'):
            exact('UNIT_%s_%08x' % (key.upper(), value), actual[key], before[key])
        expected = projected_identity(before['function_owner'])
        exact('UNIT_OWNER_%08x' % value, actual['function_owner'], expected)


def verify_global_equates(pre):
    for name in EQUATE_NAMES:
        before = pre['equate_globals'][name]
        refs = [] if before is None else list(before['references'])
        value = None
        for slot, row in sorted(SLOTS.items()):
            for item in json_list_field(row, 'after_equates_json'):
                if item['name'] == name:
                    item_value = parse_number(item['value'])
                    if value is None:
                        value = item_value
                    require(value == item_value, 'GLOBAL_EQ_PLANNED_VALUE_' + name)
                    refs.append({'address': '%08x' % slot, 'operand': int(item['operand'])})
        actual = equate_global_row(name)
        require(actual is not None and actual['value'] == value, 'GLOBAL_EQ_VALUE_' + name)
        same_set('GLOBAL_EQ_REFS_' + name, actual['references'], refs)
    for name in PROTECTED_EQUATE_NAMES:
        exact('PROTECTED_GLOBAL_EQ_' + name,
              equate_global_row(name), pre['equate_globals'][name])


def verify_post(pre):
    require(int(functions.getFunctionCount()) == pre['function_count'] == 5215,
            'FUNCTION_COUNT_POST')
    require(raw_hash(SEGMENT_START, SEGMENT_END) == pre['segment']['sha256'] and
            raw_hash(MODULE_START, MODULE_END) == pre['module']['sha256'],
            'RAW_HASH_POST')
    state_map = dict((int(row['address'], 16), row) for row in pre['states'])
    for value in STATE_ADDRESSES:
        verify_state_post(value, state_map[value])
    word_map = dict((int(row['address'], 16), row) for row in pre['words'])
    for value in WORD_ADDRESSES:
        verify_state_post(value, word_map[value])
    verify_units_post(pre)

    function_map = dict(zip(OBSERVER_FUNCTIONS, pre['functions']))
    for value in OBSERVER_FUNCTIONS:
        actual = function_row(value)
        before = function_map[value]
        expected = projected_function(before, value)
        exact('FUNCTION_STATIC_POST_%08x' % value,
              function_static_core(actual), function_static_core(expected))
        same_set('FUNCTION_BODY_REFS_POST_%08x' % value,
                 actual['body_references'], expected['body_references'])
        same_set('FUNCTION_INCOMING_POST_%08x' % value,
                 actual['incoming'], expected['incoming'])

    verify_global_equates(pre)
    if MODE != 'check':
        exact('APPLY_COUNTS', COUNTS, EXPECTED_COUNTS)
    reject('POST_VERIFY')


def failure_payload(phase, error):
    return {
        'status': 'FAIL', 'phase': phase, 'mode': MODE, 'FAIL': len(FAILS),
        'failures': FAILS, 'error': unicode(error), 'traceback': traceback.format_exc(),
        'counts': COUNTS,
    }


print('=== RefineF14Seg8 mode=%s ===' % MODE)
verify_inputs()

if MODE == 'prestate':
    state = capture()
    verify_prestate(state, False)
    write_json(PRESTATE_NAME, state)
    print('PRESTATE functions=280 words=1271 states=2978 globals=2129(2124+5null) units=55916 FAIL=0')
    print('STATUS: OK mode=prestate read_only=true')
else:
    prestate_path = os.path.join(RUN, PRESTATE_NAME)
    prestate_hash = file_hash(prestate_path)
    prestate = read_json(PRESTATE_NAME)
    plan = read_json(PLAN_NAME)
    verify_plan(plan, prestate_hash)
    if MODE == 'dry':
        verify_prestate(prestate, True)
        result = {
            'status': 'F14_SEG8_DRY_PREFLIGHT_OK', 'FAIL': 0,
            'script_sha256': file_hash(getSourceFile().getAbsolutePath()),
            'plan_sha256': file_hash(os.path.join(RUN, PLAN_NAME)),
            'prestate_sha256': prestate_hash, 'counts': EXPECTED_COUNTS,
            'preflight': {'functions': 280, 'words': 1271, 'states': 2978,
                          'slots': 101, 'targets': 11, 'consumers': 123,
                          'pc_read_consumers': 114, 'rename_call_consumers': 9,
                          'global_equates': 2129, 'global_existing': 2124,
                          'global_absent_planned': 5, 'units': 55916},
            'semantic_actions_applied': False,
        }
        write_json('f14-seg8-dry-result-%s.json' % EVIDENCE_VERSION, result)
        print('STATUS: OK mode=dry FAIL=0 semantic_actions_applied=false')
    elif MODE == 'fullrollback':
        verify_prestate(prestate, True)
        transaction = currentProgram.startTransaction('F14-Seg-8 Phase1 full rollback validation')
        post_verified = False
        error = None
        try:
            apply_all()
            verify_post(prestate)
            post_verified = True
        except Exception as caught:
            error = caught
            write_json('f14-seg8-full-rollback-failure-%s.json' % EVIDENCE_VERSION,
                       failure_payload('FULLROLLBACK', caught))
            traceback.print_exc()
        finally:
            currentProgram.endTransaction(transaction, False)
        if not post_verified:
            raise RuntimeError('F14-Seg-8 full rollback validation failed: %s' % unicode(error))
        result = {
            'status': 'F14_SEG8_FULL_ROLLBACK_VALIDATION_OK', 'FAIL': 0,
            'script_sha256': file_hash(getSourceFile().getAbsolutePath()),
            'plan_sha256': file_hash(os.path.join(RUN, PLAN_NAME)),
            'prestate_sha256': prestate_hash, 'counts': EXPECTED_COUNTS,
            'post_verified': True, 'semantic_actions_applied': True,
            'transaction_committed': False, 'rollback_forced': True,
        }
        write_json('f14-seg8-full-rollback-validation-%s.json' % EVIDENCE_VERSION, result)
        print('STATUS: OK mode=fullrollback FAIL=0 transaction=rolled_back')
    elif MODE == 'check':
        receipt = read_json('f14-seg8-apply-receipt-%s.json' % EVIDENCE_VERSION)
        require(receipt.get('status') == 'F14_SEG8_APPLIED_POSTCHECK_OK' and
                receipt.get('counts') == EXPECTED_COUNTS and
                receipt.get('script_sha256') == file_hash(getSourceFile().getAbsolutePath()) and
                receipt.get('plan_sha256') == file_hash(os.path.join(RUN, PLAN_NAME)),
                'RECEIPT_CONTRACT')
        reject('RECEIPT')
        verify_post(prestate)
        write_json('f14-seg8-persisted-check-%s.json' % EVIDENCE_VERSION, {
            'status': 'F14_SEG8_PERSISTED_CHECK_OK', 'FAIL': 0,
            'script_sha256': receipt['script_sha256'],
            'plan_sha256': receipt['plan_sha256'], 'counts': EXPECTED_COUNTS,
        })
        print('STATUS: OK mode=check FAIL=0')
    else:
        verify_prestate(prestate, True)
        transaction = currentProgram.startTransaction('F14-Seg-8 approved transaction')
        commit = False
        error = None
        try:
            apply_all()
            verify_post(prestate)
            commit = True
        except Exception as caught:
            error = caught
            write_json('f14-seg8-apply-failure-%s.json' % EVIDENCE_VERSION,
                       failure_payload('APPLY', caught))
            traceback.print_exc()
        finally:
            currentProgram.endTransaction(transaction, commit)
        if not commit:
            raise RuntimeError('F14-Seg-8 transaction rolled back: %s' % unicode(error))
        receipt = {
            'status': 'F14_SEG8_APPLIED_POSTCHECK_OK', 'FAIL': 0,
            'script_sha256': file_hash(getSourceFile().getAbsolutePath()),
            'plan_sha256': file_hash(os.path.join(RUN, PLAN_NAME)),
            'prestate_sha256': prestate_hash, 'counts': EXPECTED_COUNTS,
        }
        write_json('f14-seg8-apply-receipt-%s.json' % EVIDENCE_VERSION, receipt)
        print('STATUS: OK mode=apply FAIL=0 transaction=committed')
