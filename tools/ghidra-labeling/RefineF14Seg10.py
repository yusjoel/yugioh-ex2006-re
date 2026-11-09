# -*- coding: ascii -*-
#@runtime Jython
#@category Ygo-ex2006.Refine
# F14-Seg-10 approved materialization. Phase1 uses prestate/dry/fullrollback only.

import csv
import hashlib
import json
import os
import traceback

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.address import AddressSet
from ghidra.program.model.data import DWordDataType, Undefined4DataType
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import RefType, SourceType
from java.math import BigInteger


csv.field_size_limit(2**27)


ARGS = list(getScriptArgs())
MODE = ARGS[0].lower() if ARGS else 'dry'
if MODE not in ('prestate', 'dry', 'fullrollback', 'apply', 'check'):
    raise RuntimeError('Expected prestate, dry, fullrollback, apply, or check')

ROOT = os.path.abspath(os.path.join(str(getSourceFile().getParentFile()), '..', '..'))
RUN = os.path.join(ROOT, 'output', 'refine-run-20261028-105948')
EVIDENCE_VERSION = 'v4'
PLAN_NAME = 'f14-seg10-plan-phase1-v4.json'
PRESTATE_NAME = 'f14-seg10-fresh-full-prestate-v4.json'
SNAPSHOT_NAME = 'f14-seg10-source-snapshot-preapply-v4.json'
INPUT_HASHES = {
    'doc/dev/refine/F14-Seg-10.proposal.md': '101061c0817bc299a463ffc9f03f12aeebd71dc905195df773329c47ef79cfe1',
    'doc/dev/refine/F14-Seg-10.review.md': '3c0ea99b96feb128024fb5da85625dc05f976a17ac86e7e33245897705d83972',
    'doc/dev/refine/F14-Seg-10.slots.tsv': 'b8e6c5101b9cabd3188d34858ce23be4caf1c61b09ed5c9d119e38332f51f072',
    'doc/dev/refine/F14-Seg-10.plates.tsv': '7f7c37670197ed96143feddf5558187e48c8e1687d054433aab474bf4d917002',
    'output/refine-run-20261028-105948/f14-seg10-freeze-manifest.json': '141e6b68268be1dba79afda0c9d57d82c8a100d29d4e8e84e717b8d3a390bd64',
    'output/refine-run-20261028-105948/root-f14-seg10-round3-freeze-gate.json': '7cf1307d78046e242e729d0b5fa99d3e1654a3a7c4f7bcfad0c50008e2c90371',
}
AUXILIARY_INPUTS = (
    'root-f14-seg10-independent-full-prestate.json',
    'root-f14-seg10-independent-full-prestate-gate.json',
    'root-f14-seg10-independent-full-prestate.json.db-gate.json',
    'root-f14-seg10-independent-functions-input.json',
    'root-f14-seg10-independent-words-input.json',
    'root-f14-seg10-independent-slots-input.json',
    'root-f14-seg10-independent-equates-input.json',
    'root-f14-seg10-db-backup.json',
    'root-source-baseline-f14seg10.json',
    'f14-seg10-r4-cfg-map.json',
    'f14-seg10-table-transition-plan.json',
    'f14-seg10-plan.json',
    'f14-seg10-name-reference-baseline.json',
    'f14-seg10-b4464-rename-evidence.json',
)
EXPECTED_COUNTS = {
    'EQ_ADD': 37, 'REF_ADD': 20, 'REF_PRESERVE': 9,
    'SOURCE_LABEL': 66, 'EOL': 66,
    'R4_CODE_RANGES': 6, 'R4_INITIAL_SEEDS': 5,
    'R4_INSTRUCTIONS': 194, 'R4_POOL_WORDS': 3,
    'FUNC_CREATE': 5, 'FUNC_RENAME': 2, 'PLATE': 35,
    'TABLE_BINDING_TRANSITION': 17, 'TABLE_DATA_REF': 17,
    'B4464_EQUATE_TRANSITION': 2,
}
SEGMENT_START = 0x080b40b8
SEGMENT_END = 0x080b5348
MODULE_START = 0x080a78dc
MODULE_END = 0x080b5348
TABLE_START = 0x09e478d0
TABLE_END = 0x09e481e8
DYNAMIC_TARGETS = set()

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
        write_json('f14-seg10-%s-failures-%s.json' % (MODE, EVIDENCE_VERSION), {
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


SLOT_ROWS = read_tsv('doc/dev/refine/F14-Seg-10.slots.tsv')
PLATE_ROWS = read_tsv('doc/dev/refine/F14-Seg-10.plates.tsv')
R4_MAP = read_json('f14-seg10-r4-cfg-map.json')
TABLE_PLAN = read_json('f14-seg10-table-transition-plan.json')
ROOT_FULL_PRESTATE = read_json('root-f14-seg10-independent-full-prestate.json')
ROOT_STATE_PRESTATE = dict((int(item['state']['address'], 16), item['state'])
                           for item in ROOT_FULL_PRESTATE['slots'])
SLOTS = dict((int(row['address'], 16), row) for row in SLOT_ROWS)
PLATES = dict((int(row['entry'], 16), row) for row in PLATE_ROWS)
NEW_FUNCTION_ROWS = dict((int(row['entry'], 16), row) for row in PLATE_ROWS
                         if row['action'] == 'FUNCTION_CREATE_PLATE')
PLATE_WRITES = dict((value, row) for value, row in PLATES.items()
                    if row['action'] != 'PRESERVE')
RENAMES = dict((value, row) for value, row in PLATES.items()
               if row['current_name'] and row['current_name'] != row['final_name'])

def address_list(name):
    return [int(row['address'], 16) for row in read_json(name)]

OBSERVER_FUNCTIONS = address_list('root-f14-seg10-independent-functions-input.json')
WORD_ADDRESSES = address_list('root-f14-seg10-independent-words-input.json')
STATE_ADDRESSES = address_list('root-f14-seg10-independent-slots-input.json')
TARGETS = sorted(set(int(row['original_value'], 16) for row in SLOT_ROWS
                     if row['action'].startswith('REF_')))
TABLE_ROWS = dict((int(row['source'], 16), row)
                  for row in TABLE_PLAN['source_rows'])
B4464_PROJECTION = TABLE_PLAN['function_rename_projection']
B4464_SOURCES = [int(value, 16) for value in B4464_PROJECTION['source_words']]
TABLE_STATE_ADDRESSES = sorted(set(TABLE_ROWS) | set(B4464_SOURCES))

CODE_RANGES = sorted(set((int(lo, 16), int(hi, 16))
                         for row in R4_MAP['function_candidates']
                         for lo, hi in row['body_ranges']))
INSTRUCTION_ROWS = dict((int(row['address'], 16), row) for row in R4_MAP['instructions'])
INSTRUCTION_ADDRESSES = sorted(INSTRUCTION_ROWS)
INSTRUCTION_OWNER = {}
for _value in INSTRUCTION_ADDRESSES:
    _owners = [int(row['entry'], 16) for row in R4_MAP['function_candidates']
               if any(int(lo, 16) <= _value < int(hi, 16)
                      for lo, hi in row['body_ranges'])]
    if len(_owners) != 1:
        raise RuntimeError('R4 owner ambiguity at %08x' % _value)
    INSTRUCTION_OWNER[_value] = _owners[0]
POOL_ROWS = dict((int(row['address'], 16), row) for row in R4_MAP['pools'])
POOL_ADDRESSES = sorted(POOL_ROWS)
PADDING_RANGES = [(int(row['start'], 16), int(row['end'], 16))
                  for row in R4_MAP['padding']]
INITIAL_SEEDS = sorted(int(value, 16) for value in R4_MAP['roots'])
FLOW_ROWS = []
for _row in R4_MAP['instructions']:
    _source = int(_row['address'], 16)
    for _target_text in _row['targets']:
        _kind = _row['kind']
        FLOW_ROWS.append({
            'from': '%08x' % _source, 'to': '%08x' % int(_target_text, 16),
            'operand': 0,
            'type': ('UNCONDITIONAL_CALL' if _kind == 'CALL' else
                     ('CONDITIONAL_JUMP' if _kind == 'CONDITIONAL'
                      else 'UNCONDITIONAL_JUMP')),
            'source': 'DEFAULT', 'primary': True,
        })
PC_ROWS = []
for _pool in R4_MAP['pools']:
    for _source_text in _pool['sources']:
        PC_ROWS.append({'from': '%08x' % int(_source_text, 16),
                        'to': '%08x' % int(_pool['address'], 16),
                        'operand': 1, 'type': 'READ',
                        'source': 'DEFAULT', 'primary': True})
FALLTHROUGH_PAIRS = sorted((int(row['address'], 16),
                            int(row['architectural_fallthrough'], 16))
                           for row in R4_MAP['instructions']
                           if row['architectural_fallthrough'] is not None)
CODE_BYTES = set(value for lo, hi in CODE_RANGES for value in range(lo, hi))
POOL_BYTES = set(value for base in POOL_ADDRESSES for value in range(base, base + 4))

EQUATE_BINDINGS = []
for _value, _row in sorted(SLOTS.items()):
    for _item in json_list_field(_row, 'after_equates_json'):
        _eq_value = (long(_item['value']) if isinstance(_item['value'], (int, long))
                     else long(_item['value'], 16)) & 0xffffffff
        EQUATE_BINDINGS.append((_item['name'], _eq_value, _value, int(_item['operand'])))
TABLE_TRANSITIONS = []
for _value, _row in sorted(TABLE_ROWS.items()):
    _old = _row['equate_transition']['remove_binding']
    _new = _row['equate_transition']['add_binding']
    TABLE_TRANSITIONS.append((_value, _old, _new, _row['aux_even_data_ref']))
for _value in B4464_SOURCES:
    TABLE_TRANSITIONS.append((_value,
        {'name': B4464_PROJECTION['old_odd_equate'],
         'value': int(B4464_PROJECTION['odd_value'], 16),
         'address': '%08x' % _value, 'operand': 0},
        {'name': B4464_PROJECTION['new_odd_equate'],
         'value': int(B4464_PROJECTION['odd_value'], 16),
         'address': '%08x' % _value, 'operand': 0}, None))
ROOT_GLOBAL_EQUATE_NAMES = sorted(ROOT_FULL_PRESTATE['global_equates'])
GLOBAL_EQ_PRESTATE = dict(ROOT_FULL_PRESTATE['global_equates'])
PLANNED_EQUATE_NAMES = set(item[0] for item in EQUATE_BINDINGS)
for _value, _old, _new, _ref in TABLE_TRANSITIONS:
    PLANNED_EQUATE_NAMES.add(_new['name'])
    PLANNED_EQUATE_NAMES.add(_old['name'])
for _name in PLANNED_EQUATE_NAMES:
    if _name not in GLOBAL_EQ_PRESTATE:
        GLOBAL_EQ_PRESTATE[_name] = None
ALL_EQUATE_NAMES = sorted(GLOBAL_EQ_PRESTATE)

def parse_number(value):
    if isinstance(value, (int, long)):
        return long(value) & 0xffffffff
    return long(value, 16) & 0xffffffff


def bool_field(value):
    return value.lower() == 'true'


def verify_inputs():
    for relative, digest in sorted(INPUT_HASHES.items()):
        exact('INPUT_HASH_' + relative, file_hash(os.path.join(ROOT, relative)), digest)
    manifest = read_json('f14-seg10-freeze-manifest.json')
    for group in manifest['groups'].values():
        if not isinstance(group, list):
            continue
        for item in group:
            path = os.path.join(ROOT, item['path'])
            exact('FREEZE_' + item['path'],
                  [file_hash(path), os.path.getsize(path)],
                  [item['sha256'], long(item['size'])])
    prior = manifest['prior_review']
    prior_path = os.path.join(ROOT, prior['path'])
    exact('PRIOR_REVIEW', file_hash(prior_path), prior['sha256'])
    require(len(SLOTS) == 66 and len(SLOT_ROWS) == 66, 'SLOT_COUNT')
    for action in ('EQ_ADD', 'REF_ADD', 'REF_PRESERVE'):
        require(sum(row['action'] == action for row in SLOT_ROWS) == EXPECTED_COUNTS[action], action + '_COUNT')
    require(len(PLATES) == 35 and len(PLATE_WRITES) == 35 and
            len(NEW_FUNCTION_ROWS) == 5 and len(RENAMES) == 2,
            'FUNCTION_PLATE_COUNTS')
    require(len(OBSERVER_FUNCTIONS) == 377 and len(set(OBSERVER_FUNCTIONS)) == 377,
            'OBSERVER_FUNCTION_COUNT')
    require(len(WORD_ADDRESSES) == 1502 and len(set(WORD_ADDRESSES)) == 1502,
            'WORD_OBSERVER_COUNT')
    require(len(STATE_ADDRESSES) == 5944 and len(set(STATE_ADDRESSES)) == 5944,
            'STATE_OBSERVER_COUNT')
    require(len(CODE_RANGES) == 6 and len(INSTRUCTION_ADDRESSES) == 194 and
            len(POOL_ADDRESSES) == 3 and len(PADDING_RANGES) == 1 and
            len(FLOW_ROWS) == 42 and len(PC_ROWS) == 5 and
            len(FALLTHROUGH_PAIRS) == 183, 'R4_COUNTS')
    require(len(TABLE_ROWS) == 17 and len(B4464_SOURCES) == 2 and
            len(TABLE_TRANSITIONS) == 19, 'TABLE_COUNTS')
    require(len(ROOT_GLOBAL_EQUATE_NAMES) == 2229, 'GLOBAL_EQUATE_ROOT_COUNT')
    for row in SLOT_ROWS:
        require(row['final_symbol_source'] == 'USER_DEFINED', 'SLOT_SOURCE_' + row['address'])
        require(all(ord(char) < 128 for char in row['new_eol_ascii']), 'EOL_ASCII_' + row['address'])
    require(len(set(row['final_slot_label'] for row in SLOT_ROWS)) == 66,
            'SOURCE_LABEL_UNIQUENESS')
    for value, row in sorted(PLATE_WRITES.items()):
        require(all(ord(char) < 128 for char in row['new_plate']) and len(row['new_plate']) <= 500 and
                len(row['new_plate']) == int(row['new_plate_chars']),
                'PLATE_ASCII_%08x' % value)
    require(max(int(row['new_plate_chars']) for row in PLATE_ROWS) == 393,
            'PLATE_MAX_393')
    for value, row in sorted(NEW_FUNCTION_ROWS.items()):
        collisions = [item for item in symbols.getGlobalSymbols(row['final_name'])
                      if item.getAddress() != toAddr(value)]
        require(not collisions, 'FUNCTION_NAME_COLLISION_%08x' % value)
    reject('INPUTS')


def capture():
    return {
        'status': 'F14_SEG10_FRESH_FULL_PRESTATE',
        'program_name': unicode(currentProgram.getName()),
        'function_count': int(functions.getFunctionCount()),
        'segment': {'start': '0x%08x' % SEGMENT_START, 'end': '0x%08x' % SEGMENT_END,
                    'size': SEGMENT_END - SEGMENT_START,
                    'sha256': raw_hash(SEGMENT_START, SEGMENT_END)},
        'module': {'start': '0x%08x' % MODULE_START, 'end': '0x%08x' % MODULE_END,
                   'size': MODULE_END - MODULE_START,
                   'sha256': raw_hash(MODULE_START, MODULE_END)},
        'table': {'start': '0x%08x' % TABLE_START, 'end': '0x%08x' % TABLE_END,
                  'size': TABLE_END - TABLE_START,
                  'sha256': raw_hash(TABLE_START, TABLE_END)},
        'functions': [function_row(value) for value in OBSERVER_FUNCTIONS],
        'words': [address_state(value) for value in WORD_ADDRESSES],
        'states': [address_state(value) for value in STATE_ADDRESSES],
        'equate_globals': dict((name, equate_global_row(name)) for name in ALL_EQUATE_NAMES),
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
    expected_eq_refs = []
    for item in json_list_field(row, 'equates_json'):
        expected_eq_refs.append({'name': item['name'], 'value': parse_number(item['value']),
                                 'operand': int(item.get('operand', 0))})
    exact('SLOT_EQ_REFS_PRE_%08x' % value,
          state['equate_references'], expected_eq_refs)
    exact('SLOT_EOL_%08x' % value, state['eol'], json_value_field(row, 'old_eol_json'))
    if row['old_data_type']:
        require(state['data_at'] is not None and state['data_at']['length'] == 4 and
                state['data_at']['type'] == row['old_data_type'], 'SLOT_DATA_%08x' % value)
    else:
        require(state['data_at'] is None and state['instruction_at'] is None,
                'SLOT_UNTYPED_%08x' % value)
    owner = None if state['function_containing'] is None else state['function_containing']['name']
    expected_owner = row['old_function_owner'] or None
    require(owner == expected_owner, 'SLOT_OWNER_%08x' % value, owner, expected_owner)


def require_plate_pre(value, row, actual):
    if value in NEW_FUNCTION_ROWS:
        require(actual is None and row['current_name'] == '' and
                row['function_id'] == '' and row['body_size'] == '0' and
                json_ranges_field(row, 'body_ranges_json') == [] and
                json_list_field(row, 'incoming_json') == [],
                'NEW_FUNCTION_ABSENT_%08x' % value)
        return
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


def require_table_pre(value, row, state):
    exact('TABLE_BYTES_PRE_%08x' % value, state['bytes'], row['bytes'])
    exact('TABLE_SYMBOLS_PRE_%08x' % value, state['symbols'], row['old_symbols'])
    exact('TABLE_PRIMARY_PRE_%08x' % value, state['primary_symbol'], row['old_primary'])
    same_set('TABLE_REFS_FROM_PRE_%08x' % value,
             state['references_from'], row['old_refs_from'])
    same_set('TABLE_REFS_TO_PRE_%08x' % value,
             state['references_to'], row['old_refs_to'])
    exact('TABLE_EQ_PRE_%08x' % value, state['equates'], row['old_equates'])
    exact('TABLE_EOL_PRE_%08x' % value, state['eol'], row['old_eol'])
    if row['old_data_type'] is None:
        require(state['data_at'] is None and state['instruction_at'] is None,
                'TABLE_UNTYPED_PRE_%08x' % value)
    else:
        require(state['data_at'] is not None and
                state['data_at']['type'] == row['old_data_type'] and
                state['data_at']['length'] == 4,
                'TABLE_DATA_PRE_%08x' % value)


def verify_prestate(pre, recapture):
    if recapture:
        exact('FRESH_PRESTATE_EXACT', capture(), pre)
    require(pre['function_count'] == 5274, 'FUNCTION_COUNT_PRE')
    require(pre['segment']['size'] == 4752 and pre['module']['size'] == 55916 and
            pre['table']['size'] == 2328, 'RANGE_SIZE_PRE')
    require(len(pre['functions']) == 377 and len(pre['words']) == 1502 and
            len(pre['states']) == 5944 and len(pre['units']) == 55916,
            'PRESTATE_COUNTS')
    function_map = dict(zip(OBSERVER_FUNCTIONS, pre['functions']))
    state_map = dict((int(row['address'], 16), row) for row in pre['states'])
    require(sum(row is None for row in pre['functions']) == 6,
            'ABSENT_FUNCTION_COUNT')
    for value, row in sorted(SLOTS.items()):
        require_slot_pre(value, row, state_map[value])
        collisions = [symbol for symbol in symbols.getGlobalSymbols(row['final_slot_label'])
                      if symbol.getAddress() != toAddr(value)]
        require(not collisions, 'SLOT_NAME_COLLISION_%08x' % value)
    for value, row in sorted(PLATES.items()):
        require_plate_pre(value, row, function_map[value])
    for value in TABLE_STATE_ADDRESSES:
        require_external_state(value, state_map[value], ROOT_STATE_PRESTATE[value],
                               'TABLE_ROOT_PRE')
    for target in TARGETS:
        rows = [row for row in SLOT_ROWS if row['action'].startswith('REF_') and
                int(row['original_value'], 16) == target]
        expected = json_value_field(rows[0], 'target_prestate_json')
        if expected is None:
            expected = ROOT_STATE_PRESTATE[target]
        require_external_state(target, state_map[target], expected, 'TARGET_PRE')
    verify_global_equate_pre(pre['equate_globals'])
    reject('PRESTATE_VERIFY')


def verify_plan(plan, prestate_hash):
    require(plan.get('status') == 'F14_SEG10_PLAN_PHASE1_FROZEN', 'PLAN_STATUS')
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
            plan.get('table') == [TABLE_START, TABLE_END] and
            plan.get('observer_function_count') == len(OBSERVER_FUNCTIONS) and
            plan.get('word_count') == len(WORD_ADDRESSES) and
            plan.get('state_count') == len(STATE_ADDRESSES) and
            plan.get('slots') == sorted(SLOTS) and plan.get('targets') == TARGETS and
            plan.get('new_functions') == sorted(NEW_FUNCTION_ROWS) and
            plan.get('renames') == sorted(RENAMES) and
            plan.get('r4_instruction_count') == len(INSTRUCTION_ADDRESSES) and
            plan.get('table_sources') == TABLE_STATE_ADDRESSES and
            plan.get('all_equate_names') == ALL_EQUATE_NAMES, 'PLAN_SCOPE')
    for name in AUXILIARY_INPUTS:
        require(plan.get('auxiliary_hashes', {}).get(name) == file_hash(os.path.join(RUN, name)),
                'PLAN_AUX_' + name)
    reject('PLAN_VERIFY')


def ensure_slot_label(value, name):
    addr = toAddr(value)
    current = symbols.getPrimarySymbol(addr)
    existing = list(symbols.getSymbols(addr))
    if current is None:
        if existing:
            raise RuntimeError('Source symbols without primary at %08x' % value)
        current = symbols.createLabel(addr, name, global_ns, SourceType.USER_DEFINED)
    else:
        if not current.isPrimary() or len(existing) != 1:
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
    expected_name = row['target_final_label']
    if value in DYNAMIC_TARGETS:
        if current is None:
            if list(symbols.getSymbols(addr)):
                raise RuntimeError('Target symbols without primary at %08x' % value)
            current = symbols.createLabel(addr, expected_name, global_ns,
                                          SourceType.USER_DEFINED)
        elif not current.isPrimary() or len(list(symbols.getSymbols(addr))) != 1:
            raise RuntimeError('Target primary precondition failed at %08x' % value)
        elif str(current.getSource()) == 'DEFAULT':
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
        frozen_state = json_value_field(row, 'target_prestate_json')
        if frozen_state is None:
            frozen_state = ROOT_STATE_PRESTATE[value]
        frozen = frozen_state['primary_symbol']
        if (current is None or frozen is None or
                long(current.getID()) != long(frozen['id']) or
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
    return post


def ensure_equate(name, value, address, operand):
    eq = equates.getEquate(name)
    if eq is None:
        eq = equates.createEquate(name, value)
    elif (long(eq.getValue()) & 0xffffffff) != value:
        raise RuntimeError('Equate value conflict: ' + name)
    matches = [ref for ref in eq.getReferences()
               if ref.getAddress() == toAddr(address) and ref.getOpIndex() == operand]
    if not matches:
        eq.addReference(toAddr(address), operand)
    elif len(matches) != 1:
        raise RuntimeError('Equate binding multiplicity at %08x' % address)


def exact_ref_cores(value):
    return [ref_core(ref_row(ref)) for ref in references.getReferencesFrom(toAddr(value))]


def add_approved_data_ref(source, item):
    expected = ref_core(item)
    existing = exact_ref_cores(source)
    if expected in existing:
        if existing.count(expected) != 1:
            raise RuntimeError('DATA ref multiplicity at %08x' % source)
        return False
    if existing:
        raise RuntimeError('DATA ref source occupied at %08x' % source)
    ref = references.addMemoryReference(
        toAddr(source), toAddr(int(item['to'], 16)), RefType.DATA,
        SourceType.USER_DEFINED, int(item['operand']))
    references.setPrimary(ref, bool(item['primary']))
    return True


def instruction_starts_in_range(lo, hi):
    result = set()
    iterator = listing.getInstructions(AddressSet(toAddr(lo), toAddr(hi - 1)), True)
    while iterator.hasNext():
        result.add(long(iterator.next().getAddress().getOffset()))
    return result


def apply_r4():
    context = currentProgram.getProgramContext()
    for lo, hi in CODE_RANGES:
        clearListing(toAddr(lo), toAddr(hi - 1))
        context.setValue(tmode_register, toAddr(lo), toAddr(hi - 1), BigInteger.ONE)
        COUNTS['R4_CODE_RANGES'] += 1
    for value in INITIAL_SEEDS:
        ranges = [(lo, hi) for lo, hi in CODE_RANGES if lo <= value < hi]
        if len(ranges) != 1:
            raise RuntimeError('Initial seed range at %08x' % value)
        lo, hi = ranges[0]
        command = DisassembleCommand(toAddr(value),
                                     AddressSet(toAddr(lo), toAddr(hi - 1)), True)
        if not command.applyTo(currentProgram):
            raise RuntimeError('Initial disassembly failed at %08x' % value)
        COUNTS['R4_INITIAL_SEEDS'] += 1
    expected_set = set(INSTRUCTION_ADDRESSES)
    for value in INSTRUCTION_ADDRESSES:
        if listing.getInstructionAt(toAddr(value)) is not None:
            continue
        ranges = [(lo, hi) for lo, hi in CODE_RANGES if lo <= value < hi]
        if len(ranges) != 1:
            raise RuntimeError('Missing seed range at %08x' % value)
        lo, hi = ranges[0]
        before = instruction_starts_in_range(lo, hi)
        command = DisassembleCommand(toAddr(value),
                                     AddressSet(toAddr(lo), toAddr(hi - 1)), True)
        if not command.applyTo(currentProgram):
            raise RuntimeError('Missing-start disassembly failed at %08x' % value)
        additions = instruction_starts_in_range(lo, hi) - before
        if value not in additions or not additions.issubset(expected_set):
            raise RuntimeError('Missing-start seed result at %08x' % value)
        DYNAMIC_COUNTS['R4_MISSING_SEEDS'] += 1
    actual_set = set()
    for lo, hi in CODE_RANGES:
        actual_set.update(instruction_starts_in_range(lo, hi))
    if actual_set != expected_set:
        raise RuntimeError('R4 instruction address set has extra/missing starts')
    COUNTS['R4_INSTRUCTIONS'] = len(actual_set)
    for value in POOL_ADDRESSES:
        clearListing(toAddr(value), toAddr(value + 3))
        listing.createData(toAddr(value), Undefined4DataType.dataType)
        COUNTS['R4_POOL_WORDS'] += 1


def create_functions():
    for value, row in sorted(NEW_FUNCTION_ROWS.items()):
        if functions.getFunctionAt(toAddr(value)) is not None:
            raise RuntimeError('New Function already exists at %08x' % value)
        body = AddressSet()
        for lo_text, hi_text in json_ranges_field(row, 'final_body_ranges_json'):
            body.addRange(toAddr(int(lo_text, 16)), toAddr(int(hi_text, 16) - 1))
        fn = functions.createFunction(row['final_name'], toAddr(value), body,
                                      SourceType.USER_DEFINED)
        if fn is None:
            raise RuntimeError('New Function creation failed at %08x' % value)
        COUNTS['FUNC_CREATE'] += 1


def apply_slots():
    target_done = set()
    for value, row in sorted(SLOTS.items()):
        addr = toAddr(value)
        if (memory.getInt(addr) & 0xffffffff) != int(row['original_value'], 16):
            raise RuntimeError('ROM value changed at %08x' % value)
        data = listing.getDefinedDataAt(addr)
        if (data is None or data.getLength() != 4 or
                unicode(data.getDataType().getPathName()) != row['final_data_type']):
            raise RuntimeError('Slot Data contract at %08x' % value)
        action = row['action']
        if action == 'EQ_ADD':
            items = json_list_field(row, 'after_equates_json')
            if len(items) != 1:
                raise RuntimeError('EQ contract malformed at %08x' % value)
            item = items[0]
            ensure_equate(item['name'], parse_number(item['value']), value,
                          int(item['operand']))
            for ref_item in json_list_field(row, 'after_refs_from_json'):
                add_approved_data_ref(value, ref_item)
        elif action == 'REF_ADD':
            target = int(row['original_value'], 16)
            if target not in target_done:
                ensure_ref_target(row)
                target_done.add(target)
                if target in DYNAMIC_TARGETS:
                    COUNTS['REF_TARGET_LABEL'] += 1
            items = json_list_field(row, 'after_refs_from_json')
            if len(items) != 1:
                raise RuntimeError('REF_ADD contract malformed at %08x' % value)
            add_approved_data_ref(value, items[0])
        elif action == 'REF_PRESERVE':
            before = [ref_core(item) for item in json_list_field(row, 'refs_from_json')]
            if sorted_rows(exact_ref_cores(value)) != sorted_rows(before):
                raise RuntimeError('REF_PRESERVE drift at %08x' % value)
        else:
            raise RuntimeError('Unknown action at %08x' % value)
        ensure_slot_label(value, row['final_slot_label'])
        listing.setComment(addr, CodeUnit.EOL_COMMENT, row['new_eol_ascii'])
        COUNTS[action] += 1
        COUNTS['SOURCE_LABEL'] += 1
        COUNTS['EOL'] += 1


def remove_equate_binding(name, value, address, operand):
    eq = equates.getEquate(name)
    if eq is None or (long(eq.getValue()) & 0xffffffff) != (long(value) & 0xffffffff):
        raise RuntimeError('Old Equate missing/value drift: ' + name)
    matches = [ref for ref in eq.getReferences()
               if ref.getAddress() == toAddr(address) and ref.getOpIndex() == operand]
    if len(matches) != 1:
        raise RuntimeError('Old Equate binding multiplicity: ' + name)
    eq.removeReference(toAddr(address), operand)
    if eq.getReferenceCount() == 0:
        equates.removeEquate(name)


def apply_table_transitions():
    for value, old, new, ref_item in TABLE_TRANSITIONS:
        if bytes_hex(value, 4) is None:
            raise RuntimeError('Table source unavailable at %08x' % value)
        remove_equate_binding(old['name'], parse_number(old['value']), value,
                               int(old['operand']))
        ensure_equate(new['name'], parse_number(new['value']), value,
                       int(new['operand']))
        if ref_item is not None:
            add_approved_data_ref(value, ref_item)
            COUNTS['TABLE_BINDING_TRANSITION'] += 1
            COUNTS['TABLE_DATA_REF'] += 1
        else:
            COUNTS['B4464_EQUATE_TRANSITION'] += 1


def apply_all():
    apply_r4()
    create_functions()
    apply_slots()
    for value, row in sorted(RENAMES.items()):
        fn = functions.getFunctionAt(toAddr(value))
        if fn is None or unicode(fn.getName()) != row['current_name']:
            raise RuntimeError('Rename precondition at %08x' % value)
        fn.setName(row['final_name'], SourceType.USER_DEFINED)
        COUNTS['FUNC_RENAME'] += 1
    apply_table_transitions()
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


def expected_additions_to(value):
    rows = [item for item in FLOW_ROWS + PC_ROWS if int(item['to'], 16) == value]
    for source, row in sorted(SLOTS.items()):
        before = [ref_core(item) for item in json_list_field(row, 'refs_from_json')]
        for item in json_list_field(row, 'after_refs_from_json'):
            if int(item['to'], 16) == value and ref_core(item) not in before:
                rows.append(ref_core(item))
    for source, row in sorted(TABLE_ROWS.items()):
        item = row['aux_even_data_ref']
        if int(item['to'], 16) == value:
            rows.append(ref_core(item))
    return rows


def verify_live_refs(prefix, rows):
    for item in rows:
        exact(prefix + '_' + item['from'] + '_' + item['to'], item, live_ref_expected(item))


def verify_slot_post(value, row, before):
    actual = address_state(value)
    require(actual['bytes'] == row['old_bytes'] and
            actual['rom_word'] == int(row['original_value'], 16) and
            actual['instruction_at'] is None and actual['data_at'] is not None and
            actual['data_at']['length'] == 4 and
            actual['data_at']['type'] == row['final_data_type'],
            'SLOT_DATA_POST_%08x' % value)
    primary = actual['primary_symbol']
    require(actual['symbol_count'] == 1 and primary is not None and
            primary['name'] == row['final_slot_label'] and primary['type'] == 'Label' and
            primary['source'] == 'USER_DEFINED' and primary['primary'] and primary['global'],
            'SLOT_LABEL_POST_%08x' % value)
    exact('SLOT_EOL_POST_%08x' % value, actual['eol'], row['new_eol_ascii'])
    same_set('SLOT_REFS_FROM_POST_%08x' % value, actual['references_from'],
             live_refs(json_list_field(row, 'after_refs_from_json')))
    expected_refs_to = json_list_field(row, 'refs_to_json')
    expected_refs_to += [item for item in PC_ROWS if int(item['to'], 16) == value]
    same_set('SLOT_REFS_TO_POST_%08x' % value, actual['references_to'],
             live_refs(expected_refs_to))
    expected_eq = [{'name': item['name'], 'value': parse_number(item['value'])}
                   for item in json_list_field(row, 'after_equates_json')]
    expected_eq_refs = [{'name': item['name'], 'value': parse_number(item['value']),
                         'operand': int(item['operand'])}
                        for item in json_list_field(row, 'after_equates_json')]
    exact('SLOT_EQ_POST_%08x' % value, actual['equates'], expected_eq)
    exact('SLOT_EQ_REF_POST_%08x' % value, actual['equate_references'], expected_eq_refs)
    exact('SLOT_OWNER_POST_%08x' % value, actual['function_containing'], None)


def expected_table_state(value, before):
    expected = json.loads(json.dumps(before))
    transition = next((item for item in TABLE_TRANSITIONS if item[0] == value), None)
    if transition is None:
        return expected
    source, old, new, ref_item = transition
    expected['equates'] = [{'name': new['name'], 'value': parse_number(new['value'])}]
    expected['equate_references'] = [{'name': new['name'],
                                      'value': parse_number(new['value']),
                                      'operand': int(new['operand'])}]
    refs = list(expected['references_from'])
    if ref_item is not None:
        refs.append(ref_item)
    expected['references_from'] = live_refs(refs)
    expected['references_to'] = live_refs(expected['references_to'])
    return expected


def verify_table_post(value, before):
    actual = address_state(value)
    expected = expected_table_state(value, before)
    for key in sorted(expected):
        if key in ('references_from', 'references_to'):
            same_set('TABLE_%s_POST_%08x' % (key.upper(), value), actual[key], expected[key])
        else:
            exact('TABLE_%s_POST_%08x' % (key.upper(), value), actual[key], expected[key])


def verify_target_post(value, before):
    actual = address_state(value)
    expected_name = next(row['target_final_label'] for row in SLOT_ROWS
                         if row['action'].startswith('REF_') and
                         int(row['original_value'], 16) == value)
    primary = actual['primary_symbol']
    if value in DYNAMIC_TARGETS:
        require(actual['symbol_count'] == 1 and primary is not None and
                primary['name'] == expected_name and primary['type'] == 'Label' and
                primary['source'] == 'USER_DEFINED' and primary['primary'] and primary['global'],
                'DYNAMIC_TARGET_POST_%08x' % value)
    else:
        exact('STATIC_TARGET_PRIMARY_POST_%08x' % value,
              primary, before['primary_symbol'])
    same_set('TARGET_REFS_TO_CORE_%08x' % value,
             strip_ref_derivatives(actual['references_to']),
             strip_ref_derivatives(before['references_to']) + expected_additions_to(value))
    verify_live_refs('TARGET_REFS_TO_LIVE_%08x' % value, actual['references_to'])
    for key in ('bytes', 'rom_word', 'data_at', 'data_containing', 'instruction_at',
                'function_at', 'function_containing', 'references_from', 'equates',
                'equate_references', 'eol', 'pre', 'post', 'repeatable', 'plate', 'tmode'):
        exact('TARGET_PRESERVE_%s_%08x' % (key.upper(), value), actual[key], before[key])


def expected_instruction_refs(value):
    return [item for item in FLOW_ROWS + PC_ROWS if int(item['from'], 16) == value]


def verify_r4_post(pre):
    actual_starts=set();flow_pairs=[];pc_pairs=[];fallthrough_pairs=[]
    for lo,hi in CODE_RANGES:
        actual_starts.update(instruction_starts_in_range(lo,hi))
    exact('R4_START_SET',sorted(actual_starts),INSTRUCTION_ADDRESSES)
    for value in INSTRUCTION_ADDRESSES:
        row=INSTRUCTION_ROWS[value];inst=listing.getInstructionAt(toAddr(value))
        require(inst is not None and int(inst.getLength())==int(row['length']) and
                bytes_hex(value,int(row['length']))==row['raw_bytes'] and
                str(inst.getFlowOverride())=='NONE','R4_INSTRUCTION_%08x'%value)
        context=currentProgram.getProgramContext().getValue(tmode_register,toAddr(value),False)
        require(context is not None and int(context)==1,'R4_TMODE_%08x'%value)
        owner=functions.getFunctionContaining(toAddr(value));host=INSTRUCTION_OWNER[value]
        require(owner is not None and long(owner.getEntryPoint().getOffset())==host and
                unicode(owner.getName())==NEW_FUNCTION_ROWS[host]['final_name'],
                'R4_OWNER_%08x'%value)
        same_set('R4_REFS_%08x'%value,exact_ref_cores(value),expected_instruction_refs(value))
        for target in inst.getFlows():flow_pairs.append((value,long(target.getOffset())))
        for ref in references.getReferencesFrom(toAddr(value)):
            if str(ref.getReferenceType())=='READ' and int(ref.getOperandIndex())==1:
                pc_pairs.append((value,long(ref.getToAddress().getOffset())))
        target=inst.getFallThrough()
        if target is not None:fallthrough_pairs.append((value,long(target.getOffset())))
    exact('R4_FLOW_SET',sorted(flow_pairs),sorted((int(x['from'],16),int(x['to'],16)) for x in FLOW_ROWS))
    exact('R4_PC_SET',sorted(pc_pairs),sorted((int(x['from'],16),int(x['to'],16)) for x in PC_ROWS))
    exact('R4_FALLTHROUGH_SET',sorted(fallthrough_pairs),FALLTHROUGH_PAIRS)
    for value in POOL_ADDRESSES:
        state=address_state(value)
        require(state['data_at'] is not None and state['data_at']['length']==4 and
                state['data_at']['type']=='/undefined4' and state['instruction_at'] is None and
                state['function_containing'] is None,'R4_POOL_%08x'%value)


def function_static_core(row):
    return dict((key,row[key]) for key in (
        'entry','name','symbol','symbols','symbol_count','namespace','body','body_ranges',
        'body_size','body_sha256','eol_comments','calling_convention','signature_source',
        'prototype','custom_variable_storage','varargs','inline','no_return','external',
        'thunk','thunk_target','stack_purge_size','return','parameters','plate'))


def projected_function(before,value):
    if before is None:return None
    result=json.loads(json.dumps(before))
    if value in RENAMES:
        old=RENAMES[value]['current_name'];new=RENAMES[value]['final_name']
        result['name']=new
        for item in result['symbols']:
            if item['name']==old:item['name']=new;item['qualified_name']=new
        if result['symbol']['name']==old:
            result['symbol']['name']=new;result['symbol']['qualified_name']=new
        result['prototype']=result['prototype'].replace(old,new,1)
    if value in PLATE_WRITES:result['plate']=PLATE_WRITES[value]['new_plate']
    result['body_references']=live_refs(result['body_references'])
    result['incoming']=live_refs(result['incoming']+expected_additions_to(value))
    return result


def verify_new_function(value, row):
    actual = function_row(value)
    require(actual is not None and actual['name'] == row['final_name'] and
            actual['symbol']['type'] == 'Function' and
            actual['symbol']['source'] == 'USER_DEFINED' and
            actual['symbol']['primary'] and actual['symbol']['global'] and
            actual['symbol_count'] == 1 and actual['namespace']['global'],
            'NEW_FUNCTION_IDENTITY_%08x' % value)
    expected_return = json_value_field(row, 'return_json')
    if expected_return is None:
        expected_return = {
            'name': '<RETURN>', 'data_type': '/undefined',
            'storage': '<UNASSIGNED>', 'source': 'DEFAULT',
            'is_auto_parameter': False, 'is_register_variable': False,
            'is_stack_variable': False, 'is_memory_variable': False,
        }
    metadata = {
        'body_ranges': json_ranges_field(row, 'final_body_ranges_json'),
        'body_size': int(row['final_body_size']),
        'body_sha256': row['final_body_sha256'],
        'calling_convention': row['calling_convention'],
        'signature_source': row['signature_source'],
        'prototype': row['prototype'],
        'custom_variable_storage': bool_field(row['custom_variable_storage']),
        'varargs': bool_field(row['varargs']), 'inline': bool_field(row['inline']),
        'no_return': bool_field(row['no_return']), 'external': bool_field(row['external']),
        'thunk': bool_field(row['thunk']), 'thunk_target': None,
        'stack_purge_size': int(row['stack_purge_size']), 'return': expected_return,
        'parameters': json_list_field(row, 'parameters_json'),
        'eol_comments': json_list_field(row, 'eol_json'), 'plate': row['new_plate'],
    }
    for key, expected in sorted(metadata.items()):
        exact('NEW_FUNCTION_%s_%08x' % (key.upper(), value), actual[key], expected)
    same_set('NEW_FUNCTION_INCOMING_%08x' % value, actual['incoming'],
             live_refs(json_list_field(row, 'final_incoming_json')))
    same_set('NEW_FUNCTION_BODY_REFS_%08x' % value,
             strip_ref_derivatives(actual['body_references']),
             [item for item in FLOW_ROWS + PC_ROWS
              if INSTRUCTION_OWNER[int(item['from'], 16)] == value])
    verify_live_refs('NEW_FUNCTION_BODY_REFS_LIVE_%08x' % value,
                     actual['body_references'])


def rename_for_owner(name):
    for value,row in RENAMES.items():
        if name==row['current_name']:return row['final_name']
    return name


def verify_units_post(pre):
    pre_units=dict((int(row['address'],16),row) for row in pre['units'])
    for value in range(MODULE_START,MODULE_END):
        if value in CODE_BYTES or value in POOL_BYTES:continue
        expected=json.loads(json.dumps(pre_units[value]))
        if expected.get('function_owner') is not None:
            expected['function_owner']['name']=rename_for_owner(expected['function_owner']['name'])
        exact('UNIT_STATIC_%08x'%value,unit_row(value),expected)
    for value in INSTRUCTION_ADDRESSES:
        actual=unit_row(value);row=INSTRUCTION_ROWS[value]
        require(actual['unit_class']=='InstructionDB' and actual['unit_length']==int(row['length']) and
                actual['unit_min']=='%08x'%value and actual['tmode']==1 and
                actual['function_owner'] is not None and
                int(actual['function_owner']['entry'],16)==INSTRUCTION_OWNER[value],
                'UNIT_CODE_%08x'%value)
    for value in POOL_ADDRESSES:
        actual=unit_row(value)
        require(actual['unit_class']=='DataDB' and actual['unit_length']==4 and
                actual['unit_min']=='%08x'%value and actual['defined_data_at']['type']=='/undefined4' and
                actual['function_owner'] is None,'UNIT_POOL_%08x'%value)


def expected_global_equates(pre):
    result=json.loads(json.dumps(pre['equate_globals']))
    def add(name,value,address,operand):
        row=result.get(name)
        if row is None:row={'name':name,'value':value,'references':[]};result[name]=row
        require((long(row['value'])&0xffffffff)==(long(value)&0xffffffff),'EQ_EXPECTED_VALUE_'+name)
        ref={'address':'%08x'%address,'operand':operand}
        if ref not in row['references']:row['references'].append(ref)
    def remove(name,address,operand):
        row=result.get(name);require(row is not None,'EQ_EXPECTED_OLD_'+name)
        ref={'address':'%08x'%address,'operand':operand}
        require(row['references'].count(ref)==1,'EQ_EXPECTED_OLD_REF_'+name)
        row['references'].remove(ref)
        if not row['references']:result[name]=None
    for name,value,address,operand in EQUATE_BINDINGS:add(name,value,address,operand)
    for address,old,new,ref_item in TABLE_TRANSITIONS:
        remove(old['name'],address,int(old['operand']))
        add(new['name'],parse_number(new['value']),address,int(new['operand']))
    return result


def verify_global_equates(pre):
    expected=expected_global_equates(pre)
    exact('GLOBAL_EQ_NAME_SET',sorted(ALL_EQUATE_NAMES),sorted(expected))
    for name in ALL_EQUATE_NAMES:
        actual=equate_global_row(name);wanted=expected[name]
        if actual is None or wanted is None:
            exact('GLOBAL_EQ_%s'%name,actual,wanted);continue
        exact('GLOBAL_EQ_NAME_%s'%name,actual['name'],wanted['name'])
        exact('GLOBAL_EQ_VALUE_%s'%name,long(actual['value'])&0xffffffff,long(wanted['value'])&0xffffffff)
        same_set('GLOBAL_EQ_REFS_%s'%name,actual['references'],wanted['references'])


def project_function_view(item):
    if item is None:return None
    result=json.loads(json.dumps(item))
    if 'entry' in result:
        value=int(result['entry'],16)
        if value in RENAMES:result['name']=RENAMES[value]['final_name']
    return result


def verify_generic_state_post(value,before):
    actual=address_state(value);expected=json.loads(json.dumps(before))
    expected['references_from']=live_refs(expected['references_from'])
    expected['references_to']=live_refs(expected['references_to']+expected_additions_to(value))
    if value in RENAMES:
        old=RENAMES[value]['current_name'];new=RENAMES[value]['final_name']
        for item in expected['symbols']:
            if item['name']==old:item['name']=new;item['qualified_name']=new
        if expected['primary_symbol'] is not None and expected['primary_symbol']['name']==old:
            expected['primary_symbol']['name']=new;expected['primary_symbol']['qualified_name']=new
    expected['function_at']=project_function_view(expected['function_at'])
    expected['function_containing']=project_function_view(expected['function_containing'])
    if value in PLATE_WRITES:expected['plate']=PLATE_WRITES[value]['new_plate']
    for key in sorted(expected):
        if key in ('references_from','references_to'):
            same_set('STATE_%s_POST_%08x'%(key.upper(),value),actual[key],expected[key])
        else:exact('STATE_%s_POST_%08x'%(key.upper(),value),actual[key],expected[key])


def verify_states_post(pre):
    state_map=dict((int(row['address'],16),row) for row in pre['states']);handled=set()
    for value,row in sorted(SLOTS.items()):
        verify_slot_post(value,row,state_map[value]);handled.add(value)
    for value in TABLE_STATE_ADDRESSES:
        verify_table_post(value,state_map[value]);handled.add(value)
    for value in TARGETS:
        if value in state_map:
            verify_target_post(value,state_map[value]);handled.add(value)
    for value in STATE_ADDRESSES:
        if value in handled or value in CODE_BYTES or value in POOL_BYTES or value in NEW_FUNCTION_ROWS:continue
        verify_generic_state_post(value,state_map[value])


def verify_post(pre):
    require(pre['function_count']==5274 and int(functions.getFunctionCount())==5279,'FUNCTION_COUNT_POST')
    require(raw_hash(SEGMENT_START,SEGMENT_END)==pre['segment']['sha256'] and
            raw_hash(MODULE_START,MODULE_END)==pre['module']['sha256'] and
            raw_hash(TABLE_START,TABLE_END)==pre['table']['sha256'],'RAW_HASH_POST')
    verify_r4_post(pre);verify_states_post(pre)
    word_map=dict((int(row['address'],16),row) for row in pre['words'])
    for value in WORD_ADDRESSES:
        if value in SLOTS or value in TABLE_STATE_ADDRESSES or value in CODE_BYTES or value in POOL_BYTES:continue
        verify_generic_state_post(value,word_map[value])
    verify_units_post(pre)
    function_map=dict(zip(OBSERVER_FUNCTIONS,pre['functions']))
    for value in OBSERVER_FUNCTIONS:
        before=function_map[value]
        if value in NEW_FUNCTION_ROWS:
            exact('NEW_FUNCTION_PRE_NULL_%08x'%value,before,None);verify_new_function(value,NEW_FUNCTION_ROWS[value]);continue
        actual=function_row(value)
        if before is None:
            exact('FUTURE_FUNCTION_STAYS_NULL_%08x'%value,actual,None);continue
        expected=projected_function(before,value)
        exact('FUNCTION_STATIC_POST_%08x'%value,function_static_core(actual),function_static_core(expected))
        same_set('FUNCTION_BODY_REFS_POST_%08x'%value,actual['body_references'],expected['body_references'])
        same_set('FUNCTION_INCOMING_POST_%08x'%value,actual['incoming'],expected['incoming'])
    verify_global_equates(pre)
    if MODE!='check':exact('APPLY_COUNTS',COUNTS,EXPECTED_COUNTS)
    reject('POST_VERIFY')


def failure_payload(phase, error):
    return {
        'status': 'FAIL', 'phase': phase, 'mode': MODE, 'FAIL': len(FAILS),
        'failures': FAILS, 'error': unicode(error), 'traceback': traceback.format_exc(),
        'counts': COUNTS,
    }


print('=== RefineF14Seg10 mode=%s ===' % MODE)
verify_inputs()

if MODE == 'prestate':
    state=capture();verify_prestate(state,False);write_json(PRESTATE_NAME,state)
    print('PRESTATE functions=377 words=1502 states=5944 globals=%d units=55916 FAIL=0' % len(ALL_EQUATE_NAMES))
    print('STATUS: OK mode=prestate read_only=true')
else:
    prestate_path=os.path.join(RUN,PRESTATE_NAME);prestate_hash=file_hash(prestate_path)
    prestate=read_json(PRESTATE_NAME);plan=read_json(PLAN_NAME);verify_plan(plan,prestate_hash)
    if MODE=='dry':
        verify_prestate(prestate,True)
        result={'status':'F14_SEG10_DRY_PREFLIGHT_OK','FAIL':0,
                'script_sha256':file_hash(getSourceFile().getAbsolutePath()),
                'plan_sha256':file_hash(os.path.join(RUN,PLAN_NAME)),
                'prestate_sha256':prestate_hash,'counts':EXPECTED_COUNTS,
                'preflight':{'functions':377,'words':1502,'states':5944,'slots':66,
                             'targets':len(TARGETS),'r4_instructions':194,'r4_flows':42,
                             'pc_read_consumers':5,'table_binding_transitions':19,
                             'global_equates':len(ALL_EQUATE_NAMES),'units':55916},
                'semantic_actions_applied':False}
        write_json('f14-seg10-dry-result-%s.json'%EVIDENCE_VERSION,result)
        print('STATUS: OK mode=dry FAIL=0 semantic_actions_applied=false')
    elif MODE=='fullrollback':
        verify_prestate(prestate,True)
        transaction=currentProgram.startTransaction('F14-Seg-10 Phase1 full rollback validation')
        post_verified=False;error=None
        try:
            apply_all();verify_post(prestate);post_verified=True
        except Exception as caught:
            error=caught;write_json('f14-seg10-full-rollback-failure-%s.json'%EVIDENCE_VERSION,
                                    failure_payload('FULLROLLBACK',caught));traceback.print_exc()
        finally:currentProgram.endTransaction(transaction,False)
        if not post_verified:raise RuntimeError('F14-Seg-10 full rollback validation failed: %s'%unicode(error))
        result={'status':'F14_SEG10_FULL_ROLLBACK_VALIDATION_OK','FAIL':0,
                'script_sha256':file_hash(getSourceFile().getAbsolutePath()),
                'plan_sha256':file_hash(os.path.join(RUN,PLAN_NAME)),
                'prestate_sha256':prestate_hash,'counts':EXPECTED_COUNTS,
                'post_verified':True,'semantic_actions_applied':True,
                'transaction_committed':False,'rollback_forced':True,
                'dynamic_counts':DYNAMIC_COUNTS}
        write_json('f14-seg10-full-rollback-validation-%s.json'%EVIDENCE_VERSION,result)
        print('STATUS: OK mode=fullrollback FAIL=0 transaction=rolled_back')
    elif MODE=='check':
        receipt=read_json('f14-seg10-apply-receipt-%s.json'%EVIDENCE_VERSION)
        require(receipt.get('status')=='F14_SEG10_APPLIED_POSTCHECK_OK' and
                receipt.get('counts')==EXPECTED_COUNTS and
                receipt.get('script_sha256')==file_hash(getSourceFile().getAbsolutePath()) and
                receipt.get('plan_sha256')==file_hash(os.path.join(RUN,PLAN_NAME)),
                'RECEIPT_CONTRACT');reject('RECEIPT');verify_post(prestate)
        write_json('f14-seg10-persisted-check-%s.json'%EVIDENCE_VERSION,
                   {'status':'F14_SEG10_PERSISTED_CHECK_OK','FAIL':0,
                    'script_sha256':receipt['script_sha256'],'plan_sha256':receipt['plan_sha256'],
                    'counts':EXPECTED_COUNTS})
        print('STATUS: OK mode=check FAIL=0')
    else:
        verify_prestate(prestate,True)
        transaction=currentProgram.startTransaction('F14-Seg-10 approved transaction')
        commit=False;error=None
        try:apply_all();verify_post(prestate);commit=True
        except Exception as caught:
            error=caught;write_json('f14-seg10-apply-failure-%s.json'%EVIDENCE_VERSION,
                                    failure_payload('APPLY',caught));traceback.print_exc()
        finally:currentProgram.endTransaction(transaction,commit)
        if not commit:raise RuntimeError('F14-Seg-10 transaction rolled back: %s'%unicode(error))
        receipt={'status':'F14_SEG10_APPLIED_POSTCHECK_OK','FAIL':0,
                 'script_sha256':file_hash(getSourceFile().getAbsolutePath()),
                 'plan_sha256':file_hash(os.path.join(RUN,PLAN_NAME)),
                 'prestate_sha256':prestate_hash,'counts':EXPECTED_COUNTS}
        write_json('f14-seg10-apply-receipt-%s.json'%EVIDENCE_VERSION,receipt)
        print('STATUS: OK mode=apply FAIL=0 transaction=committed')
