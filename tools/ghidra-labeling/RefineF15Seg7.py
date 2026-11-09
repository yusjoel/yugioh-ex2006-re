# -*- coding: ascii -*-
#@runtime Jython
#@category Ygo-ex2006.Refine
# F15-Seg-7 approved materialization. Phase1 uses prestate/dry/fullrollback only.

import csv
from collections import defaultdict
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
EVIDENCE_VERSION = 'v2'
PLAN_NAME = 'f15-seg7-plan-v2.json'
PRESTATE_NAME = 'f15-seg7-fresh-full-prestate-v2.json'
SNAPSHOT_NAME = 'f15-seg7-source-snapshot-preapply-v2.json'
FRESH_PROOF_NAME = 'f15-seg7-fresh-canonical-proof-v2.json'
INPUT_HASHES = {
    'doc/dev/refine/F15-Seg-7.proposal.md': '4666d2134c0101d990c1ceff6747fef3deca55cf859ca2335a1c36fa0c731cf2',
    'doc/dev/refine/F15-Seg-7.review.md': '68c78aeed231623c0633433730d53483017ee89b1ac7a0e8682cdf0074ba8ffa',
    'doc/dev/refine/F15-Seg-7.slots.tsv': '459754ac49f6b4257588e84332937ab9ed1fe3a35a000cfbd193f1be953fe97d',
    'doc/dev/refine/F15-Seg-7.plates.tsv': '7eb2bc1ef9ed0ec3719bf0fdac7af93408e190ad529e0ece274130420d87e3c7',
    'output/refine-run-20261028-105948/f15-seg7-freeze-manifest.json': 'c3bdcbf6e59a1f6d8d95541417d398491ecdfd8f307c00b02531c586423da36d',
}
AUXILIARY_INPUTS = (
    'root-f15-seg7-composite-independent-prestate-v3.json',
    'root-f15-seg7-independent-functions-v3-input.json',
    'root-f15-seg7-independent-slots-v3-input.json',
    'root-f15-seg7-db-backup.json',
    'root-source-baseline-f15seg7.json',
    'f15-seg7-slot-plan.json',
    'f15-seg7-target-plan.json',
    'f15-seg7-function-plan.json',
    'f15-seg7-global-equates-plan.json',
    'f15-seg7-selfcheck.json',
    'f15-seg7-gas-projections.json',
    'f15-seg7-source-scope-plan.json',
    'f15-seg7-review-final-independent.json',
    'root-f15-seg7-reference-identity-mechanism.json',
    'root-f15-seg7-gas-scope-before.json',
    'root-f15-seg7-native-capability-execution.json',
    'root-f15-seg6-transaction-mechanism.json',
    'root_verify_f15_seg7_fresh.py',
    'f15-seg7-phase1-v2-offline-selfcheck.json',
    'f15-seg7-phase1-static-ready-v1.json',
    'root-f15-seg7-phase1a-v1-failure-archive.json',
)
EXPECTED_COUNTS = {
    'EQ_ADD': 45, 'REF_ADD': 62, 'REF_PRESERVE': 63, 'PRESERVE': 65,
    'SOURCE_LABEL': 170, 'SOURCE_EOL': 170, 'TARGET_LABEL': 29,
    'DATA_REF_ADD': 62, 'FUNCTION_RENAME': 5, 'PLATE': 31,
}
SEGMENT_START = 0x080bc71c
SEGMENT_END = 0x080bda7c
MODULE_START = 0x080b5348
MODULE_END = 0x080c1448

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
DYNAMIC_COUNTS = {'R4_MISSING_SEEDS': 0}


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
        write_json('f15-seg7-%s-failures-%s.json' % (MODE, EVIDENCE_VERSION), {
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


def all_equate_globals():
    result = {}
    iterator = equates.getEquates()
    if hasattr(iterator, 'hasNext'):
        while iterator.hasNext():
            eq = iterator.next()
            name = unicode(eq.getName())
            if name in result:
                raise RuntimeError('Duplicate global Equate name: ' + name)
            result[name] = equate_global_row(name)
    else:
        for eq in iterator:
            name = unicode(eq.getName())
            if name in result:
                raise RuntimeError('Duplicate global Equate name: ' + name)
            result[name] = equate_global_row(name)
    for name in ALL_EQUATE_NAMES:
        if name not in result:
            result[name] = None
    return result


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



SLOT_ROWS = read_tsv('doc/dev/refine/F15-Seg-7.slots.tsv')
PLATE_ROWS = read_tsv('doc/dev/refine/F15-Seg-7.plates.tsv')
SLOT_PLAN = read_json('f15-seg7-slot-plan.json')
TARGET_PLAN = read_json('f15-seg7-target-plan.json')
FUNCTION_PLAN = read_json('f15-seg7-function-plan.json')
GLOBAL_PLAN = read_json('f15-seg7-global-equates-plan.json')
ROOT_FULL_PRESTATE = read_json('root-f15-seg7-composite-independent-prestate-v3.json')

SLOTS = dict((int(row['address'], 16), row) for row in SLOT_ROWS)
SLOT_CONTRACTS = dict((int(row['address'], 16), row) for row in SLOT_PLAN['rows'])
PLATES = dict((int(row['entry'], 16), row) for row in PLATE_ROWS)
FUNCTION_CONTRACTS = dict((int(row['entry'], 16), row)
                          for row in FUNCTION_PLAN['functions'])
TARGET_CONTRACTS = dict((int(row['address'], 16), row)
                        for row in TARGET_PLAN['targets'])


def address_list(name):
    return [int(row['address'], 16) for row in read_json(name)]


OBSERVER_FUNCTIONS = address_list('root-f15-seg7-independent-functions-v3-input.json')
STATE_ADDRESSES = address_list('root-f15-seg7-independent-slots-v3-input.json')
WORD_ADDRESSES = [int(row['state']['address'], 16)
                  for row in ROOT_FULL_PRESTATE['words']]
TARGET_STATE_ADDRESSES = sorted(TARGET_CONTRACTS)
EXTERNAL_UNIT_ADDRESSES = [int(row['address'], 16)
                           for row in ROOT_FULL_PRESTATE['protected_external_units']['units']]
TARGETS = sorted(set(int(row['original_value'], 16) for row in SLOT_ROWS
                     if row['action'] in ('REF_ADD', 'REF_PRESERVE')))
TARGET_MATERIALIZATIONS = set(value for value, row in TARGET_CONTRACTS.items()
                              if row['before']['primary_symbol'] != row['after']['primary_symbol'])
RENAMED_FUNCTIONS = dict((value, row) for value, row in FUNCTION_CONTRACTS.items()
                         if row['before']['name'] != row['after']['name'])

ROOT_STATE_PRESTATE = {}
for _item in ROOT_FULL_PRESTATE['targets']:
    if _item.get('exact') is not None:
        ROOT_STATE_PRESTATE[int(_item['exact']['address'], 16)] = _item['exact']
for _group in ('words', 'slots'):
    for _item in ROOT_FULL_PRESTATE[_group]:
        _state = _item['state']
        _value = int(_state['address'], 16)
        if _value in ROOT_STATE_PRESTATE and ROOT_STATE_PRESTATE[_value] != _state:
            raise RuntimeError('Conflicting root state at %08x' % _value)
        ROOT_STATE_PRESTATE[_value] = _state

PLANNED_STATES = {}
PLANNED_BEFORE_STATES = {}
for _row in SLOT_PLAN['rows'] + TARGET_PLAN['targets']:
    _value = int(_row['before']['address'], 16)
    if _value in PLANNED_STATES and PLANNED_STATES[_value] != _row['after']:
        raise RuntimeError('Conflicting planned state at %08x' % _value)
    if _value in PLANNED_BEFORE_STATES and PLANNED_BEFORE_STATES[_value] != _row['before']:
        raise RuntimeError('Conflicting planned before state at %08x' % _value)
    PLANNED_STATES[_value] = _row['after']
    PLANNED_BEFORE_STATES[_value] = _row['before']

CHANGED_PRIMARY_FROZEN = {}
for _value, _after in PLANNED_STATES.items():
    _before = ROOT_STATE_PRESTATE[_value]
    if _after['primary_symbol'] != _before['primary_symbol']:
        CHANGED_PRIMARY_FROZEN[_value] = _after['primary_symbol']
for _value, _row in RENAMED_FUNCTIONS.items():
    CHANGED_PRIMARY_FROZEN[_value] = _row['after']['symbol']

FUNCTION_AFTER_CONTRACTS = dict((int(row['entry'], 16), row['after'])
                                for row in FUNCTION_PLAN['functions'])

ROOT_PRIMARY_BY_ADDRESS = {}
for _value, _state in ROOT_STATE_PRESTATE.items():
    if _state.get('primary_symbol') is not None:
        ROOT_PRIMARY_BY_ADDRESS[_value] = _state['primary_symbol']
for _fn in ROOT_FULL_PRESTATE['functions']:
    if _fn is not None:
        ROOT_PRIMARY_BY_ADDRESS[int(_fn['entry'], 16)] = _fn['symbol']


def register_reference_primary(row):
    try:
        value = int(row['to'], 16)
    except ValueError:
        return
    if row.get('target_primary_id') is None:
        return
    observed = {
        'id': row['target_primary_id'],
        'qualified_name': row['target_primary_name'],
        'type': row['target_primary_type'],
        'source': row['target_primary_source'],
    }
    existing = ROOT_PRIMARY_BY_ADDRESS.get(value)
    if existing is not None:
        expected = dict((key, existing[key]) for key in
                        ('id', 'qualified_name', 'type', 'source'))
        if expected != observed:
            raise RuntimeError('Conflicting reference primary at %08x' % value)
    else:
        ROOT_PRIMARY_BY_ADDRESS[value] = observed


for _state in ROOT_STATE_PRESTATE.values():
    for _ref in _state.get('references_from', []) + _state.get('references_to', []):
        register_reference_primary(_ref)
for _fn in ROOT_FULL_PRESTATE['functions']:
    if _fn is not None:
        for _ref in _fn.get('body_references', []) + _fn.get('incoming', []):
            register_reference_primary(_ref)

FROZEN_AFTER_RICH_ROWS = []
for _row in SLOT_PLAN['rows'] + TARGET_PLAN['targets']:
    _after = _row['after']
    FROZEN_AFTER_RICH_ROWS.extend(_after.get('references_from', []))
    FROZEN_AFTER_RICH_ROWS.extend(_after.get('references_to', []))
for _row in FUNCTION_PLAN['functions']:
    FROZEN_AFTER_RICH_ROWS.extend(_row['after'].get('body_references', []))
    FROZEN_AFTER_RICH_ROWS.extend(_row['after'].get('incoming', []))

COMMENT_TYPES = (
    ('EOL', CodeUnit.EOL_COMMENT),
    ('PLATE', CodeUnit.PLATE_COMMENT),
    ('PRE', CodeUnit.PRE_COMMENT),
    ('POST', CodeUnit.POST_COMMENT),
    ('REPEATABLE', CodeUnit.REPEATABLE_COMMENT),
)


def frozen_rich_errors(row):
    keys = ('from','to','operand','type','source','primary','target_primary_id',
            'target_primary_name','target_primary_type','target_primary_source')
    if sorted(row) != sorted(keys):
        return ['RICH10_KEYS']
    try:
        target = int(row['to'], 16)
    except ValueError:
        return [] if all(row[key] is None for key in
                         ('target_primary_id','target_primary_name','target_primary_type',
                          'target_primary_source')) else ['NONMEMORY_PRIMARY']
    changed_primary = CHANGED_PRIMARY_FROZEN.get(target)
    primary = changed_primary if changed_primary is not None else ROOT_PRIMARY_BY_ADDRESS.get(target)
    actual_id = row['target_primary_id']
    if changed_primary is None:
        # Stable targets are already frozen facts.  They must never acquire a
        # DYNAMIC token merely because a live Symbol happens to exist later.
        if isinstance(actual_id, basestring) and actual_id.startswith('DYNAMIC_'):
            return ['STABLE_TARGET_DYNAMIC_%08x' % target]
        if primary is None:
            if actual_id is None:
                return [] if all(row[key] is None for key in
                                 ('target_primary_name','target_primary_type',
                                  'target_primary_source')) else [
                                      'UNKNOWN_PRIMARY_PARTIAL_%08x' % target]
            return ['UNKNOWN_PRIMARY_%08x' % target]
    errors = []
    expected_id = primary['id']
    if isinstance(actual_id, basestring):
        if not (isinstance(expected_id, basestring) and actual_id == expected_id and
                dynamic_address(actual_id) == target):
            errors.append('UNAPPROVED_DYNAMIC_%08x' % target)
    elif isinstance(expected_id, basestring) or long(actual_id) != long(expected_id):
        errors.append('STATIC_ID_%08x' % target)
    if (row['target_primary_name'], row['target_primary_type'], row['target_primary_source']) != (
            primary['qualified_name'], primary['type'], primary['source']):
        errors.append('PRIMARY_META_%08x' % target)
    return errors

EQUATE_BINDINGS = []
for _value, _row in sorted(SLOT_CONTRACTS.items()):
    for _item in _row['after'].get('equate_references', []):
        EQUATE_BINDINGS.append((_item['name'], long(_item['value']) & 0xffffffff,
                                _value, int(_item['operand'])))
EQUATE_NAMES = sorted(set(item[0] for item in EQUATE_BINDINGS))
GLOBAL_EQ_PRESTATE = dict(ROOT_FULL_PRESTATE['global_equates'])
for _name in GLOBAL_PLAN['after']:
    if _name not in GLOBAL_EQ_PRESTATE:
        GLOBAL_EQ_PRESTATE[_name] = None
ALL_EQUATE_NAMES = sorted(GLOBAL_EQ_PRESTATE)


def normalized_frozen_state(row, before):
    result = json.loads(json.dumps(row))
    if 'instruction' in result:
        text = result.pop('instruction')
        frozen = before.get('instruction_at')
        if text is None:
            require(frozen is None, 'FROZEN_INSTRUCTION_NONE_' + result['address'])
            result['instruction_at'] = None
        else:
            require(frozen is not None and frozen['text'] == text,
                    'FROZEN_INSTRUCTION_TEXT_' + result['address'], frozen, text)
            result['instruction_at'] = json.loads(json.dumps(frozen))
    return result


def dynamic_address(token):
    if not isinstance(token, basestring) or not token.startswith('DYNAMIC_'):
        return None
    tail = token.rsplit('_', 1)[-1]
    try:
        return int(tail, 16)
    except ValueError:
        return None


def resolve_frozen_dynamic(value, token_ids):
    if isinstance(value, list):
        return [resolve_frozen_dynamic(item, token_ids) for item in value]
    if not isinstance(value, dict):
        return value
    result = dict((key, resolve_frozen_dynamic(item, token_ids)) for key, item in value.items())
    for id_key, name_key, type_key, source_key in (
            ('id', 'name', 'type', 'source'),
            ('target_primary_id', 'target_primary_name',
             'target_primary_type', 'target_primary_source')):
        token = result.get(id_key)
        target = dynamic_address(token)
        if target is None:
            continue
        require(token in token_ids, 'UNKNOWN_DYNAMIC_TOKEN_' + token)
        require(token_ids[token]['address'] == target,
                'DYNAMIC_TOKEN_ADDRESS_' + token)
        require((result.get(name_key), result.get(type_key), result.get(source_key)) ==
                (token_ids[token]['name'], token_ids[token]['type'], token_ids[token]['source']),
                'DYNAMIC_FROZEN_META_' + token)
        result[id_key] = long(token_ids[token]['id'])
    return result


def build_live_primary_graph():
    graph = {}
    tokens = {}
    for value, frozen in sorted(CHANGED_PRIMARY_FROZEN.items()):
        primary = symbols.getPrimarySymbol(toAddr(value))
        require(primary is not None, 'PRIMARY_GRAPH_MISSING_%08x' % value)
        actual = symbol_row(primary)
        expected = json.loads(json.dumps(frozen))
        token = expected.get('id')
        if isinstance(token, basestring):
            require(dynamic_address(token) == value, 'PRIMARY_TOKEN_ADDRESS_%08x' % value)
            if token in tokens:
                exact('PRIMARY_TOKEN_REUSE_' + token, tokens[token]['id'], actual['id'])
            tokens[token] = {'address': value, 'id': actual['id'],
                             'name': expected['qualified_name'],
                             'type': expected['type'], 'source': expected['source']}
            expected['id'] = actual['id']
        exact('PRIMARY_GRAPH_%08x' % value, actual, expected)
        graph['%08x' % value] = actual
    require(len(graph) == 204, 'LIVE_PRIMARY_GRAPH_COUNT', len(graph), 204)
    return graph, tokens


def project_old_ref(row, graph):
    result = json.loads(json.dumps(row))
    primary = graph.get(result.get('to'))
    if primary is not None:
        result['target_primary_id'] = primary['id']
        result['target_primary_name'] = primary['qualified_name']
        result['target_primary_type'] = primary['type']
        result['target_primary_source'] = primary['source']
    return result


def project_owner_name(row):
    if row is None:
        return None
    result = json.loads(json.dumps(row))
    entry = int(result['entry'], 16)
    contract = RENAMED_FUNCTIONS.get(entry)
    if contract is not None:
        require(long(result['id']) == long(contract['before']['symbol']['id']),
                'OWNER_STATIC_ID_%08x' % entry)
        result['name'] = contract['after']['name']
    return result


def project_state_identity(value, row, graph):
    result = json.loads(json.dumps(row))
    primary = graph.get('%08x' % value)
    if primary is not None:
        replaced = []
        for symbol in result['symbols']:
            replaced.append(json.loads(json.dumps(primary)) if symbol.get('primary') else symbol)
        if not any(symbol.get('primary') for symbol in result['symbols']):
            replaced.append(json.loads(json.dumps(primary)))
        result['symbols'] = replaced
        result['symbol_count'] = len(replaced)
        result['primary_symbol'] = json.loads(json.dumps(primary))
    result['function_at'] = project_owner_name(result.get('function_at'))
    result['function_containing'] = project_owner_name(result.get('function_containing'))
    return result


def multiset_additions(after, before):
    remaining = [json.dumps(item, sort_keys=True, separators=(',', ':')) for item in before]
    result = []
    for item in after:
        key = json.dumps(item, sort_keys=True, separators=(',', ':'))
        if key in remaining:
            remaining.remove(key)
        else:
            result.append(item)
    require(not remaining, 'EXPECTED_AFTER_DROPPED_OLD_ROWS', remaining, [])
    return result


def comment_rows():
    result = []
    for value in range(MODULE_START, MODULE_END):
        addr = toAddr(value)
        for kind, comment_type in COMMENT_TYPES:
            text = listing.getComment(comment_type, addr)
            if text is not None:
                result.append({'address': '0x%08x' % value, 'type': kind,
                               'text': unicode(text)})
    return result


def module_symbol_rows():
    result = []
    iterator = symbols.getAllSymbols(True)
    while iterator.hasNext():
        symbol = iterator.next()
        addr = symbol.getAddress()
        if addr is None or not addr.isMemoryAddress():
            continue
        value = long(addr.getOffset())
        if MODULE_START <= value < MODULE_END:
            row = symbol_row(symbol)
            row['address'] = '0x%08x' % value
            result.append(row)
    return result


def build_expected_post(pre):
    graph, tokens = build_live_primary_graph()
    before_states = {}
    for group in ('states', 'words', 'target_states'):
        for row in pre[group]:
            value = int(row['address'], 16)
            if value in before_states:
                exact('EXPECTED_BEFORE_DUPLICATE_%08x' % value, row, before_states[value])
            else:
                before_states[value] = row
    require(len(before_states) == 9831, 'EXPECTED_BEFORE_STATE_UNION_COUNT',
            len(before_states), 9831)
    final = {}
    for value, frozen in PLANNED_STATES.items():
        require(value in before_states, 'PLANNED_STATE_OBSERVED_%08x' % value)
        state = normalized_frozen_state(frozen, before_states[value])
        final[value] = resolve_frozen_dynamic(state, tokens)
    additions = []
    for value, state in sorted(final.items()):
        old_rows = [project_old_ref(row, graph)
                    for row in before_states[value]['references_from']]
        additions.extend(multiset_additions(state['references_from'], old_rows))
    require(len(additions) == 62, 'DATA_ADDITION_COUNT', len(additions), 62)
    incoming = defaultdict(list)
    for row in additions:
        require(sorted(row) == sorted(('from','to','operand','type','source','primary',
                                       'target_primary_id','target_primary_name',
                                       'target_primary_type','target_primary_source')),
                'DATA_ADDITION_RICH10', row)
        require(row['type'] == 'DATA' and row['source'] == 'USER_DEFINED',
                'DATA_ADDITION_CORE', row)
        incoming[int(row['to'], 16)].append(row)
    expected_states = {}
    for value, before in before_states.items():
        if value in final:
            expected = final[value]
        else:
            expected = project_state_identity(value, before, graph)
            expected['references_from'] = [project_old_ref(row, graph)
                                           for row in before['references_from']]
            expected['references_to'] = [project_old_ref(row, graph)
                                         for row in before['references_to']] + incoming[value]
            contract = FUNCTION_AFTER_CONTRACTS.get(value)
            if contract is not None:
                expected['plate'] = contract['plate']
        expected_states[value] = expected
    before_functions = dict((int(row['entry'], 16), row)
                            for row in pre['functions'] if row is not None)
    expected_functions = {}
    for value, before in before_functions.items():
        expected = json.loads(json.dumps(before))
        expected['body_references'] = [project_old_ref(row, graph)
                                       for row in before['body_references']]
        expected['incoming'] = [project_old_ref(row, graph)
                                for row in before['incoming']] + incoming[value]
        contract = FUNCTION_AFTER_CONTRACTS.get(value)
        if contract is not None:
            frozen = resolve_frozen_dynamic(contract, tokens)
            for key in expected:
                if key in ('body_references', 'incoming', 'eol_comments'):
                    same_set('FUNCTION_CONTRACT_%08x_%s' % (value, key),
                             expected[key], frozen[key])
                elif key in ('name', 'symbol', 'symbols', 'prototype', 'plate'):
                    pass
                else:
                    exact('FUNCTION_CONTRACT_%08x_%s' % (value, key),
                          expected[key], frozen[key])
            expected = frozen
        expected_functions[value] = expected
    require(len(expected_functions) == 411 and len(expected_states) == 9831,
            'EXPECTED_MODEL_COUNTS')
    expected_units = json.loads(json.dumps(pre['units']))
    rename_names = dict((value, row['after']['name'])
                        for value, row in RENAMED_FUNCTIONS.items())
    for row in expected_units:
        owner = row.get('function_owner')
        if owner is not None:
            entry = int(owner['entry'], 16)
            if entry in rename_names:
                owner['name'] = rename_names[entry]
    expected_symbols = []
    seen_primary = set()
    for row in pre['module_symbols']:
        value = int(row['address'], 16)
        if row.get('primary') and '%08x' % value in graph:
            projected = json.loads(json.dumps(graph['%08x' % value]))
            projected['address'] = row['address']
            expected_symbols.append(projected)
            seen_primary.add(value)
        else:
            expected_symbols.append(json.loads(json.dumps(row)))
    for key, symbol in graph.items():
        value = int(key, 16)
        if MODULE_START <= value < MODULE_END and value not in seen_primary:
            projected = json.loads(json.dumps(symbol))
            projected['address'] = '0x%08x' % value
            expected_symbols.append(projected)
    expected_comments = dict(((int(row['address'], 16), row['type']), row['text'])
                             for row in pre['module_comments'])
    for value, row in SLOT_CONTRACTS.items():
        if row['before'].get('eol') != row['after'].get('eol'):
            expected_comments[(value, 'EOL')] = row['after'].get('eol')
    for value, row in FUNCTION_CONTRACTS.items():
        if (MODULE_START <= value < MODULE_END and
                row['before'].get('plate') != row['after'].get('plate')):
            expected_comments[(value, 'PLATE')] = row['after'].get('plate')
    expected_comments = [
        {'address': '0x%08x' % value, 'type': kind, 'text': text}
        for (value, kind), text in sorted(expected_comments.items()) if text is not None]
    return (expected_states, expected_functions, expected_units, expected_symbols,
            expected_comments, graph, tokens, additions)


def compare_unordered_field(prefix, actual, expected, field):
    same_set(prefix + '_' + field.upper(), actual.get(field, []), expected.get(field, []))


def compare_state(prefix, actual, expected):
    unordered = ('symbols', 'references_from', 'references_to',
                 'equates', 'equate_references')
    exact(prefix + '_KEYS', sorted(actual), sorted(expected))
    for key in expected:
        if key in unordered:
            compare_unordered_field(prefix, actual, expected, key)
        else:
            exact(prefix + '_' + key.upper(), actual.get(key), expected.get(key))


def compare_function(prefix, actual, expected):
    exact(prefix + '_KEYS', sorted(actual), sorted(expected))
    for key in expected:
        if key in ('body_references', 'incoming', 'eol_comments'):
            same_set(prefix + '_' + key.upper(), actual.get(key, []), expected.get(key, []))
        else:
            exact(prefix + '_' + key.upper(), actual.get(key), expected.get(key))


def verify_global_equate_pre(actuals):
    exact('GLOBAL_EQ_PRE_NAMES', sorted(actuals), sorted(GLOBAL_EQ_PRESTATE))
    require(len(actuals) == 2446 and
            sum(row is not None for row in actuals.values()) == 2438 and
            sum(row is None for row in actuals.values()) == 8,
            'GLOBAL_EQ_PRE_COUNTS')
    for name in ALL_EQUATE_NAMES:
        actual = actuals.get(name)
        expected = GLOBAL_EQ_PRESTATE.get(name)
        if actual is None or expected is None:
            exact('GLOBAL_EQ_PRE_' + name, actual, expected)
        else:
            exact('GLOBAL_EQ_PRE_NAME_' + name, actual['name'], expected['name'])
            exact('GLOBAL_EQ_PRE_VALUE_' + name,
                  long(actual['value']) & 0xffffffff,
                  long(expected['value']) & 0xffffffff)
            same_set('GLOBAL_EQ_PRE_REFS_' + name,
                     actual.get('references', []), expected.get('references', []))


def verify_inputs():
    for relative, digest in sorted(INPUT_HASHES.items()):
        exact('INPUT_HASH_' + relative, file_hash(os.path.join(ROOT, relative)), digest)
    manifest = read_json('f15-seg7-freeze-manifest.json')
    frozen = manifest['formal'] + manifest['plans'] + manifest['evidence']
    require(len(frozen) == 38, 'FREEZE_INPUT_COUNT', len(frozen), 38)
    for item in frozen:
        path = os.path.join(ROOT, item['path'])
        exact('FREEZE_' + item['path'],
              [file_hash(path), os.path.getsize(path)],
              [item['sha256'], long(item.get('bytes', item.get('size')))])
    require(len(SLOT_ROWS) == len(SLOTS) == len(SLOT_CONTRACTS) == 235,
            'SLOT_COUNT')
    for action, count in (('EQ_ADD', 45), ('REF_ADD', 62),
                          ('REF_PRESERVE', 63), ('PRESERVE', 65)):
        require(sum(row['action'] == action for row in SLOT_ROWS) == count,
                action + '_COUNT')
    require(len(PLATES) == len(FUNCTION_CONTRACTS) == 31,
            'FUNCTION_COUNT')
    require(sum(row['action'] == 'PLATE_REWRITE' for row in PLATE_ROWS) == 26 and
            sum(row['action'] == 'FUNC_RENAME_PLATE_REWRITE' for row in PLATE_ROWS) == 5,
            'PLATE_ACTION_COUNTS')
    for value, formal in sorted(PLATES.items()):
        contract = FUNCTION_CONTRACTS.get(value)
        require(contract is not None, 'PLATE_FUNCTION_ENTRY_%08x' % value)
        expected_action = ('RENAME_PLATE' if
                           formal['action'] == 'FUNC_RENAME_PLATE_REWRITE'
                           else 'PLATE_REWRITE')
        exact('PLATE_FUNCTION_ACTION_%08x' % value,
              contract['action'], expected_action)
        renamed = contract['before']['name'] != contract['after']['name']
        exact('PLATE_FUNCTION_RENAME_%08x' % value, renamed,
              formal['action'] == 'FUNC_RENAME_PLATE_REWRITE')
        exact('PLATE_FUNCTION_NAMES_%08x' % value,
              [formal['current_name'], formal['final_name']],
              [contract['before']['name'], contract['after']['name']])
    require(len(OBSERVER_FUNCTIONS) == 412 and len(set(OBSERVER_FUNCTIONS)) == 412,
            'OBSERVER_FUNCTION_COUNT')
    require(len(STATE_ADDRESSES) == 9795 and len(set(STATE_ADDRESSES)) == 9795,
            'STATE_OBSERVER_COUNT')
    require(len(WORD_ADDRESSES) == 1446 and len(set(WORD_ADDRESSES)) == 1446,
            'WORD_OBSERVER_COUNT')
    require(len(TARGET_STATE_ADDRESSES) == 48 and len(EXTERNAL_UNIT_ADDRESSES) == 48,
            'TARGET_EXTERNAL_COUNTS')
    require(len(EQUATE_BINDINGS) == 45 and len(EQUATE_NAMES) == 16,
            'EQUATE_BINDING_COUNTS', [len(EQUATE_BINDINGS), len(EQUATE_NAMES)], [45, 16])
    require(len(GLOBAL_PLAN['before']) == 2438 and len(GLOBAL_PLAN['after']) == 2446 and
            sum(GLOBAL_EQ_PRESTATE[name] is None for name in ALL_EQUATE_NAMES) == 8,
            'GLOBAL_EQUATE_COUNTS')
    require(len(PLANNED_STATES) == len(PLANNED_BEFORE_STATES) == 275 and
            len(CHANGED_PRIMARY_FROZEN) == 204 and len(RENAMED_FUNCTIONS) == 5,
            'PLANNED_STATE_GRAPH_COUNTS')
    for value, before in sorted(PLANNED_BEFORE_STATES.items()):
        exact('PLANNED_BEFORE_%08x' % value, before, ROOT_STATE_PRESTATE[value])
    root_functions = dict((int(row['entry'], 16), row)
                          for row in ROOT_FULL_PRESTATE['functions'] if row is not None)
    function_rows = FUNCTION_PLAN['functions']
    require(len(function_rows) == 31 and len(FUNCTION_AFTER_CONTRACTS) == 31,
            'FUNCTION_PROJECTION_COUNTS')
    for row in function_rows:
        value = int(row['before']['entry'], 16)
        exact('FUNCTION_BEFORE_%08x' % value, row['before'], root_functions[value])
    rich_errors = []
    for index, row in enumerate(FROZEN_AFTER_RICH_ROWS):
        for error in frozen_rich_errors(row):
            rich_errors.append('%04d:%s' % (index, error))
    exact('FROZEN_AFTER_RICH_ERRORS', rich_errors, [])
    require(len(FROZEN_AFTER_RICH_ROWS) == 6777,
            'FROZEN_AFTER_RICH_COUNT', len(FROZEN_AFTER_RICH_ROWS), 6777)
    require(len(TARGET_MATERIALIZATIONS) == 29, 'TARGET_MATERIALIZATION_COUNT')
    for value in sorted(TARGET_MATERIALIZATIONS):
        require(TARGET_CONTRACTS[value]['after'].get('eol') ==
                TARGET_CONTRACTS[value]['before'].get('eol'),
                'TARGET_EOL_FORBIDDEN_%08x' % value)
    exact('GLOBAL_PLAN_BEFORE', GLOBAL_PLAN['before'],
          ROOT_FULL_PRESTATE['global_equates'])
    require(len(GLOBAL_PLAN['before']) == 2438 and len(GLOBAL_PLAN['after']) == 2446 and
            sum(len(row['references']) for row in GLOBAL_PLAN['before'].values()) == 12465 and
            sum(len(row['references']) for row in GLOBAL_PLAN['after'].values()) == 12510,
            'GLOBAL_PLAN_BINDING_COUNTS')
    require(len(ALL_EQUATE_NAMES) == 2446 and len(GLOBAL_EQ_PRESTATE) == 2446,
            'GLOBAL_COMPLETE_NAME_COUNTS')
    global_additions = []
    for name, after in sorted(GLOBAL_PLAN['after'].items()):
        before = GLOBAL_PLAN['before'].get(name)
        before_refs = [] if before is None else before['references']
        for item in multiset_additions(after['references'], before_refs):
            global_additions.append((name, long(after['value']) & 0xffffffff,
                                     int(item['address'], 16), int(item['operand'])))
    exact('GLOBAL_PLAN_ADDITIONS', sorted(global_additions), sorted(EQUATE_BINDINGS))
    for row in SLOT_ROWS:
        if row.get('new_eol_ascii'):
            require(all(ord(char) < 128 for char in row['new_eol_ascii']),
                    'EOL_ASCII_' + row['address'])
    for value, row in sorted(PLATES.items()):
        require(all(ord(char) < 128 for char in row['new_plate']) and
                len(row['new_plate']) == int(row['new_plate_chars']) and
                len(row['new_plate']) <= 500,
                'PLATE_ASCII_%08x' % value)
    snapshot = read_json(SNAPSHOT_NAME)
    require(snapshot.get('file_count') == 176 and
            snapshot.get('baseline_file_count') == 171 and
            snapshot.get('phase1_additions') == 5,
            'SOURCE_SNAPSHOT_COUNTS')
    exact('SOURCE_SNAPSHOT_BASELINE_NAME', snapshot.get('baseline_manifest'),
          'root-source-baseline-f15seg7.json')
    exact('SOURCE_SNAPSHOT_BASELINE_HASH', snapshot.get('baseline_manifest_sha256'),
          file_hash(os.path.join(RUN, 'root-source-baseline-f15seg7.json')))
    baseline = read_json('root-source-baseline-f15seg7.json')
    additions = set([
        'doc/dev/refine/F15-Seg-7.proposal.md',
        'doc/dev/refine/F15-Seg-7.review.md',
        'doc/dev/refine/F15-Seg-7.slots.tsv',
        'doc/dev/refine/F15-Seg-7.plates.tsv',
        'tools/ghidra-labeling/RefineF15Seg7.py',
    ])
    exact('SOURCE_SNAPSHOT_MEMBER_SET', sorted(snapshot['files']),
          sorted(set(baseline['files']) | additions))
    for relative, expected in sorted(baseline['files'].items()):
        exact('SOURCE_BASELINE_MEMBER_' + relative,
              snapshot['files'][relative]['sha256'], expected['sha256'])
    snapshot_root = os.path.join(ROOT, snapshot['snapshot_directory'])
    for relative, expected in sorted(snapshot['files'].items()):
        current_path = os.path.join(ROOT, relative)
        frozen_path = os.path.join(snapshot_root, relative)
        exact('SOURCE_CURRENT_' + relative,
              [os.path.getsize(current_path), file_hash(current_path)],
              [long(expected['size']), expected['sha256']])
        exact('SOURCE_SNAPSHOT_' + relative,
              file_hash(frozen_path), expected['snapshot_sha256'])
    reject('INPUTS')


def capture():
    return {
        'status': 'F15_SEG7_FRESH_FULL_PRESTATE',
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
        'states': [address_state(value) for value in STATE_ADDRESSES],
        'words': [address_state(value) for value in WORD_ADDRESSES],
        'target_states': [address_state(value) for value in TARGET_STATE_ADDRESSES],
        'units': [unit_row(value) for value in range(MODULE_START, MODULE_END)],
        'external_units': [unit_row(value) for value in EXTERNAL_UNIT_ADDRESSES],
        'module_symbols': module_symbol_rows(),
        'module_comments': comment_rows(),
        'equate_globals': all_equate_globals(),
    }


def verify_prestate(pre, recapture):
    require(pre['status'] == 'F15_SEG7_FRESH_FULL_PRESTATE', 'PRESTATE_STATUS')
    require(pre['function_count'] == 5414, 'FUNCTION_COUNT_PRE')
    require(len(pre['functions']) == 412 and len(pre['states']) == 9795 and
            len(pre['words']) == 1446 and len(pre['target_states']) == 48 and
            len(pre['units']) == 49408 and
            len(pre['external_units']) == 48,
            'PRESTATE_ARRAY_COUNTS')
    same_set('PRESTATE_MODULE_SYMBOLS_CANONICAL', pre['module_symbols'],
             ROOT_FULL_PRESTATE['module_symbols'])
    canonical_comments = [
        {'address': row['address'], 'type': row['type'], 'text': row['text']}
        for row in ROOT_FULL_PRESTATE['module_comments']]
    same_set('PRESTATE_MODULE_COMMENTS_CANONICAL', pre['module_comments'],
             canonical_comments)
    verify_global_equate_pre(pre['equate_globals'])
    if recapture:
        current = capture()
        exact('PRESTATE_RECAPTURE_MODULE', current['module'], pre['module'])
        exact('PRESTATE_RECAPTURE_SEGMENT', current['segment'], pre['segment'])
        exact('PRESTATE_RECAPTURE_FUNCTION_COUNT', current['function_count'], pre['function_count'])
        for index, (actual, expected) in enumerate(zip(current['functions'], pre['functions'])):
            if actual is None or expected is None:
                exact('PRESTATE_FUNCTION_%04d' % index, actual, expected)
            else:
                compare_function('PRESTATE_FUNCTION_%04d' % index, actual, expected)
        for index, (actual, expected) in enumerate(zip(current['states'], pre['states'])):
            compare_state('PRESTATE_STATE_%04d' % index, actual, expected)
        for index, (actual, expected) in enumerate(zip(current['words'], pre['words'])):
            compare_state('PRESTATE_WORD_%04d' % index, actual, expected)
        for index, (actual, expected) in enumerate(zip(current['target_states'],
                                                       pre['target_states'])):
            compare_state('PRESTATE_TARGET_%04d' % index, actual, expected)
        exact('PRESTATE_UNITS', current['units'], pre['units'])
        exact('PRESTATE_EXTERNAL_UNITS', current['external_units'], pre['external_units'])
        same_set('PRESTATE_MODULE_SYMBOLS', current['module_symbols'], pre['module_symbols'])
        same_set('PRESTATE_MODULE_COMMENTS', current['module_comments'], pre['module_comments'])
        verify_global_equate_pre(current['equate_globals'])
    reject('PRESTATE')


def verify_plan(plan, prestate_hash):
    require(plan.get('status') == 'F15_SEG7_PLAN_FROZEN', 'PLAN_STATUS')
    exact('PLAN_INPUT_HASHES', plan.get('input_hashes'), INPUT_HASHES)
    exact('PLAN_COUNTS', plan.get('counts'), EXPECTED_COUNTS)
    exact('PLAN_SCRIPT_HASH', plan.get('script_sha256'),
          file_hash(getSourceFile().getAbsolutePath()))
    exact('PLAN_PRESTATE_HASH', plan.get('prestate_sha256'), prestate_hash)
    require(plan.get('source_snapshot_manifest') == SNAPSHOT_NAME and
            plan.get('source_snapshot_sha256') == file_hash(os.path.join(RUN, SNAPSHOT_NAME)),
            'PLAN_SNAPSHOT_HASH')
    require(plan.get('segment') == [SEGMENT_START, SEGMENT_END] and
            plan.get('module') == [MODULE_START, MODULE_END] and
            plan.get('observer_function_count') == len(OBSERVER_FUNCTIONS) and
            plan.get('word_count') == len(WORD_ADDRESSES) and
            plan.get('state_count') == len(STATE_ADDRESSES) and
            plan.get('target_state_count') == len(TARGET_STATE_ADDRESSES) and
            plan.get('external_unit_count') == len(EXTERNAL_UNIT_ADDRESSES) and
            plan.get('slots') == sorted(SLOTS) and
            plan.get('targets') == TARGETS and
            plan.get('planned_equate_names') == EQUATE_NAMES and
            plan.get('all_equate_names') == ALL_EQUATE_NAMES,
            'PLAN_SCOPE')
    for name in AUXILIARY_INPUTS:
        exact('PLAN_AUX_' + name, plan.get('auxiliary_hashes', {}).get(name),
              file_hash(os.path.join(RUN, name)))
    offline_name = 'f15-seg7-phase1-%s-offline-selfcheck.json' % EVIDENCE_VERSION
    offline_status = 'F15_SEG7_PHASE1_%s_OFFLINE_SELFCHECK_PASS' % EVIDENCE_VERSION.upper()
    require(offline_name in AUXILIARY_INPUTS, 'OFFLINE_SELFCHECK_AUX')
    offline = read_json(offline_name)
    require(offline.get('status') == offline_status and
            offline.get('script_sha256') == file_hash(getSourceFile().getAbsolutePath()),
            'OFFLINE_SELFCHECK_BINDING')
    proof = read_json(FRESH_PROOF_NAME)
    require(proof.get('status') == 'PASS', 'FRESH_PROOF_STATUS')
    exact('FRESH_PROOF_HASH', plan.get('fresh_proof_sha256'),
          file_hash(os.path.join(RUN, FRESH_PROOF_NAME)))
    exact('FRESH_PROOF_FRESH', proof.get('freshSha256'), prestate_hash)
    exact('FRESH_PROOF_SCRIPT', proof.get('scriptSha256'),
          file_hash(getSourceFile().getAbsolutePath()))
    exact('FRESH_PROOF_SNAPSHOT', proof.get('snapshotSha256'),
          file_hash(os.path.join(RUN, SNAPSHOT_NAME)))
    exact('FRESH_PROOF_FREEZE', proof.get('freezeSha256'),
          INPUT_HASHES['output/refine-run-20261028-105948/f15-seg7-freeze-manifest.json'])
    exact('FRESH_PROOF_CANONICAL', proof.get('canonicalSha256'),
          file_hash(os.path.join(RUN, 'root-f15-seg7-composite-independent-prestate-v3.json')))
    exact('FRESH_PROOF_VERIFIER', proof.get('verifierSha256'),
          file_hash(os.path.join(RUN, 'root_verify_f15_seg7_fresh.py')))
    require(proof.get('functions') == 412 and proof.get('states') == 9795 and
            proof.get('words') == 1446 and proof.get('targetStates') == 48 and
            proof.get('units') == 49408 and
            proof.get('externalUnits') == 48 and proof.get('sourceFiles') == 176,
            'FRESH_PROOF_COUNTS')
    reject('PLAN')


def receipt_bindings():
    return {
        'script_sha256': file_hash(getSourceFile().getAbsolutePath()),
        'plan_sha256': file_hash(os.path.join(RUN, PLAN_NAME)),
        'fresh_sha256': file_hash(os.path.join(RUN, PRESTATE_NAME)),
        'fresh_proof_sha256': file_hash(os.path.join(RUN, FRESH_PROOF_NAME)),
        'source_snapshot_sha256': file_hash(os.path.join(RUN, SNAPSHOT_NAME)),
        'freeze_sha256': INPUT_HASHES['output/refine-run-20261028-105948/f15-seg7-freeze-manifest.json'],
        'review_sha256': INPUT_HASHES['doc/dev/refine/F15-Seg-7.review.md'],
    }


def ensure_user_label(value, name):
    addr = toAddr(value)
    current = symbols.getPrimarySymbol(addr)
    existing = list(symbols.getSymbols(addr))
    if current is None:
        if existing:
            raise RuntimeError('Symbols without primary at %08x' % value)
        current = symbols.createLabel(addr, name, global_ns, SourceType.USER_DEFINED)
    else:
        if not current.isPrimary() or len(existing) != 1:
            raise RuntimeError('Primary precondition at %08x' % value)
        if unicode(current.getName(True)) != name or str(current.getSource()) != 'USER_DEFINED':
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
        raise RuntimeError('USER label failed at %08x' % value)


def ensure_equate(name, value, address, operand):
    eq = equates.getEquate(name)
    if eq is None:
        eq = equates.createEquate(name, value)
    elif (long(eq.getValue()) & 0xffffffff) != value:
        raise RuntimeError('Equate conflict ' + name)
    matches = [ref for ref in eq.getReferences()
               if ref.getAddress() == toAddr(address) and ref.getOpIndex() == operand]
    if not matches:
        eq.addReference(toAddr(address), operand)
        return True
    elif len(matches) != 1:
        raise RuntimeError('Equate multiplicity at %08x' % address)
    return False


def exact_ref_cores(value):
    return [ref_core(ref_row(ref)) for ref in references.getReferencesFrom(toAddr(value))]


def add_data_ref(source, item):
    expected = ref_core(item)
    existing = exact_ref_cores(source)
    if expected in existing:
        if existing.count(expected) != 1:
            raise RuntimeError('DATA multiplicity at %08x' % source)
        return False
    if existing:
        raise RuntimeError('DATA source occupied at %08x' % source)
    ref = references.addMemoryReference(toAddr(source), toAddr(int(item['to'], 16)),
                                         RefType.DATA, SourceType.USER_DEFINED,
                                         int(item['operand']))
    references.setPrimary(ref, bool(item['primary']))
    return True


def apply_function_names():
    for value, row in sorted(RENAMED_FUNCTIONS.items()):
        fn = functions.getFunctionAt(toAddr(value))
        if (fn is None or long(fn.getSymbol().getID()) != long(row['before']['symbol']['id']) or
                unicode(fn.getName()) != row['before']['name']):
            raise RuntimeError('Function rename precondition at %08x' % value)
        fn.setName(row['after']['name'], SourceType.USER_DEFINED)
        COUNTS['FUNCTION_RENAME'] += 1


def apply_target_labels():
    for value in sorted(TARGET_MATERIALIZATIONS):
        row = TARGET_CONTRACTS[value]
        if row['before'].get('eol') != row['after'].get('eol'):
            raise RuntimeError('Target EOL mutation forbidden at %08x' % value)
        ensure_user_label(value, row['after']['primary_symbol']['name'])
        COUNTS['TARGET_LABEL'] += 1


def apply_slots():
    for value, formal in sorted(SLOTS.items()):
        contract = SLOT_CONTRACTS[value]
        addr = toAddr(value)
        if (memory.getInt(addr) & 0xffffffff) != int(formal['original_value'], 16):
            raise RuntimeError('ROM value changed at %08x' % value)
        data = listing.getDefinedDataAt(addr)
        if (data is None or data.getLength() != 4 or
                unicode(data.getDataType().getPathName()) != formal['final_data_type']):
            raise RuntimeError('Data contract at %08x' % value)
        action = formal['action']
        if action == 'EQ_ADD':
            items = contract['after']['equate_references']
            if len(items) != 1:
                raise RuntimeError('EQ malformed at %08x' % value)
            item = items[0]
            if not ensure_equate(item['name'], long(item['value']) & 0xffffffff,
                                  value, int(item['operand'])):
                raise RuntimeError('EQ binding unexpectedly existed at %08x' % value)
        elif action == 'REF_ADD':
            additions = contract['after']['references_from']
            before_cores = [ref_core(item) for item in contract['before']['references_from']]
            new = [item for item in additions if ref_core(item) not in before_cores]
            if len(new) != 1 or not add_data_ref(value, new[0]):
                raise RuntimeError('REF_ADD malformed/existing at %08x' % value)
            COUNTS['DATA_REF_ADD'] += 1
        elif action == 'REF_PRESERVE':
            before = [ref_core(item) for item in contract['before']['references_from']]
            if sorted_rows(exact_ref_cores(value)) != sorted_rows(before):
                raise RuntimeError('REF_PRESERVE drift at %08x' % value)
        elif action == 'PRESERVE':
            for key in contract['before']:
                if key != 'references_to' and contract['after'].get(key) != contract['before'].get(key):
                    raise RuntimeError('Pure PRESERVE local contract changed at %08x' % value)
        else:
            raise RuntimeError('Unknown action at %08x' % value)
        if action != 'PRESERVE':
            after_primary = contract['after']['primary_symbol']
            if after_primary is None or after_primary.get('source') != 'USER_DEFINED':
                raise RuntimeError('Source primary contract at %08x' % value)
            ensure_user_label(value, after_primary['name'])
            if contract['after'].get('eol') != formal['new_eol_ascii']:
                raise RuntimeError('Source EOL contract at %08x' % value)
            listing.setComment(addr, CodeUnit.EOL_COMMENT, contract['after'].get('eol'))
            COUNTS['SOURCE_LABEL'] += 1
            COUNTS['SOURCE_EOL'] += 1
        COUNTS[action] += 1


def apply_plates():
    for value, row in sorted(PLATES.items()):
        contract = FUNCTION_CONTRACTS.get(value)
        if contract is None:
            raise RuntimeError('Function contract missing at %08x' % value)
        expected_contract_action = (
            'RENAME_PLATE' if row['action'] == 'FUNC_RENAME_PLATE_REWRITE'
            else 'PLATE_REWRITE' if row['action'] == 'PLATE_REWRITE' else None)
        if (expected_contract_action is None or
                contract['action'] != expected_contract_action or
                ((contract['before']['name'] != contract['after']['name']) !=
                 (row['action'] == 'FUNC_RENAME_PLATE_REWRITE'))):
            raise RuntimeError('Function action pairing at %08x' % value)
        fn = functions.getFunctionAt(toAddr(value))
        if fn is None or unicode(fn.getName()) != row['final_name']:
            raise RuntimeError('Function precondition at %08x' % value)
        listing.setComment(toAddr(value), CodeUnit.PLATE_COMMENT, row['new_plate'])
        COUNTS['PLATE'] += 1


def apply_all():
    apply_function_names()
    apply_target_labels()
    apply_slots()
    apply_plates()


def verify_post(pre):
    current = capture()
    (expected_states, expected_functions, expected_units, expected_symbols,
     expected_comments, graph, tokens, additions) = build_expected_post(pre)
    exact('POST_FUNCTION_COUNT', current['function_count'], pre['function_count'])
    exact('POST_SEGMENT', current['segment'], pre['segment'])
    exact('POST_MODULE', current['module'], pre['module'])
    for index, value in enumerate(OBSERVER_FUNCTIONS):
        actual = current['functions'][index]
        before = pre['functions'][index]
        if actual is None or before is None:
            exact('POST_FUNCTION_%08x' % value, actual, before)
        else:
            compare_function('POST_FUNCTION_%08x' % value, actual,
                             expected_functions[value])
    for index, value in enumerate(STATE_ADDRESSES):
        compare_state('POST_STATE_%08x' % value, current['states'][index],
                      expected_states[value])
    for index, value in enumerate(WORD_ADDRESSES):
        compare_state('POST_WORD_%08x' % value, current['words'][index],
                      expected_states[value])
    for index, value in enumerate(TARGET_STATE_ADDRESSES):
        compare_state('POST_TARGET_%08x' % value, current['target_states'][index],
                      expected_states[value])
    exact('POST_UNITS', current['units'], expected_units)
    exact('POST_EXTERNAL_UNITS', current['external_units'], pre['external_units'])
    same_set('POST_MODULE_SYMBOLS', current['module_symbols'], expected_symbols)
    same_set('POST_MODULE_COMMENTS', current['module_comments'], expected_comments)
    expected_globals = dict(pre['equate_globals'])
    for name, row in GLOBAL_PLAN['after'].items():
        expected_globals[name] = row
    exact('POST_GLOBAL_NAMES', sorted(current['equate_globals']), sorted(expected_globals))
    for name in sorted(expected_globals):
        actual = current['equate_globals'][name]
        expected = expected_globals[name]
        if actual is None or expected is None:
            exact('POST_GLOBAL_' + name, actual, expected)
        else:
            exact('POST_GLOBAL_NAME_' + name, actual['name'], expected['name'])
            exact('POST_GLOBAL_VALUE_' + name,
                  long(actual['value']) & 0xffffffff,
                  long(expected['value']) & 0xffffffff)
            same_set('POST_GLOBAL_REFS_' + name,
                     actual.get('references', []), expected.get('references', []))
    require(len(current['equate_globals']) == 2446 and
            sum(len(row['references']) for row in current['equate_globals'].values()
                if row is not None) == 12510,
            'POST_GLOBAL_COUNTS')
    require(len(graph) == 204 and len(additions) == 62,
            'POST_GRAPH_ADDITION_COUNTS')
    if MODE in ('fullrollback', 'apply'):
        for key, expected in EXPECTED_COUNTS.items():
            exact('ACTION_COUNT_' + key, COUNTS[key], expected)
    reject('POST')


def transaction_info_row():
    info = currentProgram.getCurrentTransactionInfo()
    if info is None:
        return None
    return {
        'present': True,
        'class_name': unicode(info.getClass().getName()),
    }


def failure_payload(phase, error, progress=None):
    payload = {
        'status': 'FAIL', 'phase': phase, 'mode': MODE,
        'FAIL': len(FAILS), 'failures': FAILS,
        'error': unicode(error), 'traceback': traceback.format_exc(),
        'semantic_actions_applied': False,
        'post_verified': False,
    }
    if progress is not None:
        payload.update(progress)
    return payload


verify_inputs()
if MODE == 'prestate':
    result = capture()
    write_json(PRESTATE_NAME, result)
    print('STATUS: OK PRESTATE functions=%d states=%d words=%d targets=%d units=%d external=%d globals=%d' %
          (len(result['functions']), len(result['states']), len(result['words']),
           len(result['target_states']), len(result['units']), len(result['external_units']),
           len(result['equate_globals'])))
elif MODE == 'dry':
    pre = read_json(PRESTATE_NAME)
    verify_prestate(pre, True)
    verify_plan(read_json(PLAN_NAME), file_hash(os.path.join(RUN, PRESTATE_NAME)))
    payload = {
        'status': 'PASS', 'mode': MODE, 'FAIL': 0,
        'semantic_actions_applied': False, 'post_verified': False,
        'counts': EXPECTED_COUNTS, 'prestate_sha256': file_hash(os.path.join(RUN, PRESTATE_NAME)),
    }
    payload.update(receipt_bindings())
    write_json('f15-seg7-dry-%s.json' % EVIDENCE_VERSION, payload)
    print('STATUS: OK DRY FAIL=0')
elif MODE in ('fullrollback', 'apply'):
    pre = read_json(PRESTATE_NAME)
    verify_prestate(pre, True)
    verify_plan(read_json(PLAN_NAME), file_hash(os.path.join(RUN, PRESTATE_NAME)))
    tx = None
    owned_open = False
    committed = False
    stage = 'MANAGED_OUTER_PRECONDITION'
    progress = {
        'semantic_actions_applied': False,
        'post_verified': False,
        'post_pass': False,
        'rollback_after_capture_pass': False,
        'rollback_forced': MODE == 'fullrollback',
        'transaction_committed': False,
        'txn_before_managed_end': None,
        'txn_after_managed_end': None,
        'txn_before_own_start': None,
        'txn_after_own_start': None,
        'txn_before_own': None,
        'txn_before_own_end': None,
        'txn_after_own': None,
        'txn_after_own_end': None,
        'owned_transaction_id': None,
        'end_transaction_return': None,
    }
    try:
        progress['txn_before_managed_end'] = transaction_info_row()
        require(progress['txn_before_managed_end'] is not None,
                'MANAGED_OUTER_PRESENT')
        reject('MANAGED_OUTER_PRECONDITION')
        stage = 'MANAGED_OUTER_END'
        this.end(False)
        progress['txn_after_managed_end'] = transaction_info_row()
        exact('MANAGED_OUTER_ENDED', progress['txn_after_managed_end'], None)
        reject('MANAGED_OUTER_END')
        stage = 'MANAGED_OUTER_RESTORE'
        verify_prestate(pre, True)
        reject('MANAGED_OUTER_RESTORE')
        progress['txn_before_own_start'] = transaction_info_row()
        exact('OWNED_TRANSACTION_PRE_NONE', progress['txn_before_own_start'], None)
        reject('OWNED_TRANSACTION_PRE')
        stage = 'OWNED_TRANSACTION_START'
        tx = currentProgram.startTransaction('F15-Seg-7 approved materialization')
        owned_open = True
        progress['owned_transaction_id'] = long(tx)
        progress['txn_after_own_start'] = transaction_info_row()
        progress['txn_before_own'] = progress['txn_after_own_start']
        require(progress['txn_after_own_start'] is not None and
                progress['txn_after_own_start'].get('present') is True and
                long(progress['owned_transaction_id']) == long(tx),
                'OWNED_TRANSACTION_ACTIVE')
        reject('OWNED_TRANSACTION_START')
        stage = 'MUTATION'
        progress['semantic_actions_applied'] = True
        apply_all()
        stage = 'POST'
        verify_post(pre)
        progress['post_verified'] = True
        progress['post_pass'] = True
        progress['txn_before_own_end'] = transaction_info_row()
        exact('OWNED_TRANSACTION_BEFORE_END',
              progress['txn_before_own_end'], progress['txn_after_own_start'])
        reject('OWNED_TRANSACTION_BEFORE_END')
        stage = 'OWNED_TRANSACTION_END'
        progress['end_transaction_return'] = bool(
            currentProgram.endTransaction(tx, MODE == 'apply'))
        owned_open = False
        if MODE == 'apply':
            require(progress['end_transaction_return'] is True,
                    'OWNED_TRANSACTION_APPLY_COMMITTED')
        committed = MODE == 'apply' and progress['end_transaction_return'] is True
        progress['transaction_committed'] = committed
        progress['txn_after_own'] = transaction_info_row()
        progress['txn_after_own_end'] = progress['txn_after_own']
        exact('OWNED_TRANSACTION_ENDED', progress['txn_after_own'], None)
        reject('OWNED_TRANSACTION_END')
        if MODE == 'fullrollback':
            stage = 'ROLLBACK_RESTORE'
            verify_prestate(pre, True)
            reject('ROLLBACK_RESTORE')
            progress['rollback_after_capture_pass'] = True
        payload = {
            'status': 'PASS', 'mode': MODE, 'FAIL': 0,
            'counts': COUNTS,
            'prestate_sha256': file_hash(os.path.join(RUN, PRESTATE_NAME)),
        }
        payload.update(progress)
        payload.update(receipt_bindings())
        write_json('f15-seg7-%s-%s.json' % (MODE, EVIDENCE_VERSION), payload)
        print('STATUS: OK %s FAIL=0 committed=%s' % (MODE.upper(), committed))
    except Exception as error:
        if owned_open:
            try:
                currentProgram.endTransaction(tx, False)
                owned_open = False
                progress['txn_after_own'] = transaction_info_row()
                progress['txn_after_own_end'] = progress['txn_after_own']
            except Exception:
                pass
        write_json('f15-seg7-%s-failure-%s.json' % (MODE, EVIDENCE_VERSION),
                   failure_payload(stage, error, progress))
        print(traceback.format_exc())
        raise
elif MODE == 'check':
    pre = read_json(PRESTATE_NAME)
    plan = read_json(PLAN_NAME)
    verify_plan(plan, file_hash(os.path.join(RUN, PRESTATE_NAME)))
    apply_receipt = read_json('f15-seg7-apply-%s.json' % EVIDENCE_VERSION)
    require(apply_receipt.get('status') == 'PASS' and
            apply_receipt.get('transaction_committed') is True and
            apply_receipt.get('post_verified') is True,
            'CHECK_APPLY_RECEIPT')
    exact('CHECK_APPLY_BINDINGS',
          dict((key, apply_receipt.get(key)) for key in receipt_bindings()),
          receipt_bindings())
    reject('CHECK_BINDINGS')
    verify_post(pre)
    payload = {
        'status': 'PASS', 'mode': MODE, 'FAIL': 0,
        'semantic_actions_applied': False, 'post_verified': True,
    }
    payload.update(receipt_bindings())
    write_json('f15-seg7-persisted-check-%s.json' % EVIDENCE_VERSION, payload)
    print('STATUS: OK CHECK FAIL=0')
