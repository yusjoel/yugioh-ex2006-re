# -*- coding: ascii -*-
#@runtime Jython
#@category Ygo-ex2006.Refine
# F15-Seg-5 approved materialization. Phase1 uses prestate/dry/fullrollback only.

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
EVIDENCE_VERSION = 'v5'
PLAN_NAME = 'f15-seg5-plan-v5.json'
PRESTATE_NAME = 'f15-seg5-fresh-full-prestate-v5.json'
SNAPSHOT_NAME = 'f15-seg5-source-snapshot-preapply-v5.json'
INPUT_HASHES = {
    'doc/dev/refine/F15-Seg-5.proposal.md': '770dc2329c60a2b898388e415a0e15e2a408ec4fcc00e437445db4feee75d257',
    'doc/dev/refine/F15-Seg-5.review.md': 'c13ad1641206d06cc66a27dc04736ab544e9bfe895f1fab84335c17948c68aec',
    'doc/dev/refine/F15-Seg-5.slots.tsv': '2a1ecac7afdb3ce776d0ad81748d72e94f4fe6906fa883c90cefb7722fe14b9a',
    'doc/dev/refine/F15-Seg-5.plates.tsv': '349ccf9651196cdf9dba8ba0678d7441e00e679e1e102fe7ce9890687c53309a',
    'output/refine-run-20261028-105948/f15-seg5-freeze-manifest.json': '1a3f3ef7255c81b1f15906cbb77222e2089bf28682ed1fb019bf34b3f5dbeb29',
}
AUXILIARY_INPUTS = (
    'root-f15-seg5-independent-full-prestate.json',
    'root-f15-seg5-independent-full-prestate.json.db-gate.json',
    'root-f15-seg5-independent-functions-input.json',
    'root-f15-seg5-independent-slots-input.json',
    'root-f15-seg5-pre-words-input.json',
    'root-f15-seg5-db-backup.json',
    'root-source-baseline-f15seg5.json',
    'f15-seg5-semantic-plan.json',
    'f15-seg5-slot-plan.json',
    'f15-seg5-function-plan.json',
    'f15-seg5-r4-cfg-map.json',
    'f15-seg5-r4-plan.json',
    'f15-seg5-external-table-carve-plan.json',
    'f15-seg5-callback-source-plan.json',
    'f15-seg5-odd-holder-projection.json',
    'f15-seg5-external-rename-rich-projection.json',
    'f15-seg5-name-reference-baseline.json',
    'f15-seg5-function-pointer-holds.json',
    'f15-seg5-selfcheck.json',
    'f15-seg5-global-equates-plan.json',
)
EXPECTED_COUNTS = {
    'EQ_ADD': 28, 'REF_ADD': 15, 'REF_PRESERVE': 7,
    'SOURCE_LABEL': 50, 'EOL': 50,
    'R4_CODE_RANGES': 1, 'R4_INITIAL_SEEDS': 1,
    'R4_INSTRUCTIONS': 20, 'R4_POOL_WORDS': 2,
    'FUNC_CREATE': 1, 'FUNC_RENAME': 2, 'PLATE': 14,
    'CARVE_WORDS': 6, 'CARVE_DATA_CREATE': 4, 'CARVE_DATA_REF': 3,
    'CALLBACK_EQ_REBIND': 1, 'CALLBACK_DATA_REF': 1,
    'GLOBAL_EQ_REMOVE': 1,
}
SEGMENT_START = 0x080babd4
SEGMENT_END = 0x080bb3dc
MODULE_START = 0x080b5348
MODULE_END = 0x080c1448
DYNAMIC_TARGETS = set([0x09e488d8])
CALLBACK_SOURCE = 0x09e48e9c
HOLDER_SOURCE = 0x09e5ab5c
HOLDER_ODD_TARGET = 0x080bb2d5
EXTERNAL_DERIVED_FUNCTION = 0x080bc71c

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
        write_json('f15-seg5-%s-failures-%s.json' % (MODE, EVIDENCE_VERSION), {
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


SLOT_ROWS = read_tsv('doc/dev/refine/F15-Seg-5.slots.tsv')
PLATE_ROWS = read_tsv('doc/dev/refine/F15-Seg-5.plates.tsv')
R4_MAP = read_json('f15-seg5-r4-cfg-map.json')
R4_PLAN = read_json('f15-seg5-r4-plan.json')
FUNCTION_PLAN = read_json('f15-seg5-function-plan.json')
CARVE_PLAN = read_json('f15-seg5-external-table-carve-plan.json')
CALLBACK_PLAN = read_json('f15-seg5-callback-source-plan.json')
HOLDER_PLAN = read_json('f15-seg5-odd-holder-projection.json')
EXTERNAL_DERIVED_PLAN = read_json('f15-seg5-external-rename-rich-projection.json')
GLOBAL_PLAN = read_json('f15-seg5-global-equates-plan.json')
ROOT_FULL_PRESTATE = read_json('root-f15-seg5-independent-full-prestate.json')
ROOT_STATE_PRESTATE = {}
for _collection in (ROOT_FULL_PRESTATE['slots'], ROOT_FULL_PRESTATE['words']):
    for _item in _collection:
        ROOT_STATE_PRESTATE[int(_item['state']['address'], 16)] = _item['state']
for _item in ROOT_FULL_PRESTATE['targets']:
    ROOT_STATE_PRESTATE[int(_item['value'], 16)] = _item['exact']
SLOTS = dict((int(row['address'], 16), row) for row in SLOT_ROWS)
PLATES = dict((int(row['entry'], 16), row) for row in PLATE_ROWS)
NEW_FUNCTION_ROWS = dict((int(row['entry'], 16), row) for row in PLATE_ROWS
                         if row['action'] == 'CREATE')
RENAME_ROWS = dict((int(row['entry'], 16), row) for row in PLATE_ROWS
                   if row['action'] != 'CREATE' and row['current_name'] != row['final_name'])
PLATE_WRITES = dict(PLATES)


def address_list(name):
    return [int(row['address'], 16) for row in read_json(name)]


OBSERVER_FUNCTIONS = address_list('root-f15-seg5-independent-functions-input.json')
WORD_ADDRESSES = address_list('root-f15-seg5-pre-words-input.json')
STATE_ADDRESSES = address_list('root-f15-seg5-independent-slots-input.json')
TARGETS = sorted(set(int(row['original_value'], 16) for row in SLOT_ROWS
                     if row['action'] in ('REF_ADD', 'REF_PRESERVE')))
CARVE_ROWS = dict((int(row['address'], 16), row) for row in CARVE_PLAN['rows'])
CARVE_BOOKENDS = dict((int(row['address'], 16), row)
                      for row in CARVE_PLAN['bookends'].values())

CODE_RANGES = sorted((int(lo, 16), int(hi, 16))
                     for row in R4_PLAN['functions']
                     for lo, hi in row['ranges'])
INSTRUCTION_ROWS = dict((int(row['address'], 16), row)
                        for row in R4_PLAN['instructions'])
INSTRUCTION_ADDRESSES = sorted(INSTRUCTION_ROWS)
INSTRUCTION_OWNER = {}
for _value in INSTRUCTION_ADDRESSES:
    _owners = [int(row['entry'], 16) for row in R4_PLAN['functions']
               if any(int(lo, 16) <= _value < int(hi, 16) for lo, hi in row['ranges'])]
    if len(_owners) != 1:
        raise RuntimeError('Instruction owner contract at %08x' % _value)
    INSTRUCTION_OWNER[_value] = _owners[0]
POOL_ROWS = dict((int(row['address'], 16), row) for row in R4_PLAN['pools'])
POOL_ADDRESSES = sorted(POOL_ROWS)
PADDING_RANGES = [(int(row['start'], 16), int(row['end'], 16))
                  for row in R4_PLAN['zero_padding']]
INITIAL_SEEDS = sorted(int(row['entry'], 16) for row in R4_PLAN['functions'])
FLOW_ROWS = []
for _row in R4_PLAN['instructions']:
    _source = int(_row['address'], 16)
    for _target_text in ([] if _row['directTarget'] is None else [_row['directTarget']]):
        _target = int(_target_text, 16)
        FLOW_ROWS.append({
            'from': '%08x' % _source, 'to': '%08x' % _target, 'operand': 0,
            'type': ('UNCONDITIONAL_CALL' if _row['kind'] == 'CALL' else
                     ('CONDITIONAL_JUMP' if _row['kind'] == 'CONDITIONAL'
                      else 'UNCONDITIONAL_JUMP')),
            'source': 'DEFAULT', 'primary': True,
        })
PC_ROWS = []
for _row in R4_PLAN['pools']:
    for _ref in json.loads(_row['refs_to_json']):
        PC_ROWS.append(dict((key, _ref[key]) for key in
                            ('from', 'to', 'operand', 'type', 'source', 'primary')))
FALLTHROUGH_PAIRS = sorted((int(row['address'], 16), int(row['fallthrough'], 16))
                           for row in R4_PLAN['instructions']
                           if row['fallthrough'] is not None)
CODE_BYTES = set(value for lo, hi in CODE_RANGES for value in range(lo, hi))
POOL_BYTES = set(value for base in POOL_ADDRESSES for value in range(base, base + 4))
APPROVED_CODE_SET = AddressSet()
for _lo, _hi in CODE_RANGES:
    APPROVED_CODE_SET.addRange(toAddr(_lo), toAddr(_hi - 1))
NEW_FUNCTION_BODY_BYTES = set()
for _row in NEW_FUNCTION_ROWS.values():
    for _lo, _hi in json_ranges_field(_row, 'final_body_ranges_json'):
        NEW_FUNCTION_BODY_BYTES.update(range(int(_lo, 16), int(_hi, 16)))

EQUATE_BINDINGS = []
for _value, _row in sorted(SLOTS.items()):
    for _item in json_list_field(_row, 'after_equates_json'):
        _eq_value = (long(_item['value']) if isinstance(_item['value'], (int, long))
                     else long(_item['value'], 16)) & 0xffffffff
        EQUATE_BINDINGS.append((_item['name'], _eq_value,
                                _value, int(_item['operand'])))
for _value, _row in sorted(CARVE_ROWS.items()):
    for _item in _row['equates']:
        EQUATE_BINDINGS.append((_item['name'], long(_item['value']) & 0xffffffff,
                                _value, int(_item['operand'])))
for _item in CALLBACK_PLAN['after']['equates']:
    EQUATE_BINDINGS.append((_item['name'], long(_item['value']) & 0xffffffff,
                            CALLBACK_SOURCE, int(_item['operand'])))
EQUATE_NAMES = sorted(set(item[0] for item in EQUATE_BINDINGS))
ROOT_GLOBAL_EQUATE_NAMES = sorted(ROOT_FULL_PRESTATE['global_equates'])
GLOBAL_EQ_PRESTATE = dict(ROOT_FULL_PRESTATE['global_equates'])
for _planned_name in GLOBAL_PLAN['new']:
    if _planned_name not in GLOBAL_EQ_PRESTATE:
        GLOBAL_EQ_PRESTATE[_planned_name] = None
ALL_EQUATE_NAMES = sorted(GLOBAL_EQ_PRESTATE)
FINAL_EQUATE_NAMES = sorted(GLOBAL_PLAN['after'])
RETIRED_EQUATE_NAMES = sorted(GLOBAL_PLAN['retired'])
PROTECTED_EQUATE_NAMES = sorted(set(ROOT_GLOBAL_EQUATE_NAMES) -
                                 set(GLOBAL_PLAN['changed']) -
                                 set(RETIRED_EQUATE_NAMES))


def frozen_projection(name, symbol_type, source, symbol_id):
    return {'name': name, 'type': symbol_type, 'source': source, 'id': symbol_id}


APPROVED_PRIMARY_PROJECTIONS = {}
for _value, _row in sorted(SLOTS.items()):
    _old = json_value_field(_row, 'old_primary_json')
    _id = (_old['id'] if _old is not None and _old['source'] == 'USER_DEFINED'
           else None)
    APPROVED_PRIMARY_PROJECTIONS[_value] = frozen_projection(
        _row['final_slot_label'], 'Label', 'USER_DEFINED', _id)
for _value, _row in sorted(CARVE_ROWS.items()):
    _old = _row['old_state']['primary_symbol']
    _id = (_old['id'] if _old is not None and _old['source'] == 'USER_DEFINED'
           else None)
    APPROVED_PRIMARY_PROJECTIONS[_value] = frozen_projection(
        _row['final_label'], 'Label', 'USER_DEFINED', _id)
for _value, _row in sorted(RENAME_ROWS.items()):
    APPROVED_PRIMARY_PROJECTIONS[_value] = frozen_projection(
        _row['final_name'], 'Function', 'USER_DEFINED', long(_row['function_id']))
for _value, _row in sorted(NEW_FUNCTION_ROWS.items()):
    APPROVED_PRIMARY_PROJECTIONS[_value] = frozen_projection(
        _row['final_name'], 'Function', 'USER_DEFINED', None)
APPROVED_PRIMARY_PROJECTIONS[0x080bacf0] = frozen_projection(
    'LAB_080bacf0', 'Label', 'DEFAULT', None)
_holder_primary = HOLDER_PLAN['after']['primary_symbol']
APPROVED_PRIMARY_PROJECTIONS[HOLDER_SOURCE] = frozen_projection(
    _holder_primary['name'], _holder_primary['type'],
    _holder_primary['source'], long(_holder_primary['id']))
_holder_odd = HOLDER_PLAN['after']['references_from'][0]
APPROVED_PRIMARY_PROJECTIONS[HOLDER_ODD_TARGET] = frozen_projection(
    _holder_odd['target_primary_name'], _holder_odd['target_primary_type'],
    _holder_odd['target_primary_source'], long(_holder_odd['target_primary_id']))

_new_function_entry = sorted(NEW_FUNCTION_ROWS)[0]
NEW_FUNCTION_FINAL_REFS = json_list_field(
    NEW_FUNCTION_ROWS[_new_function_entry], 'final_body_refs_json')
FROZEN_ADDITION_REFS = list(NEW_FUNCTION_FINAL_REFS)
for _row in SLOT_ROWS:
    if _row['action'] == 'REF_ADD':
        FROZEN_ADDITION_REFS.extend(json_list_field(_row, 'after_refs_from_json'))
for _row in CARVE_ROWS.values():
    FROZEN_ADDITION_REFS.extend(_row['refs_from'])
FROZEN_ADDITION_REFS.extend(CALLBACK_PLAN['after']['refs_from'])

FROZEN_AFTER_RICH_ROWS = []
for _row in PLATE_ROWS:
    FROZEN_AFTER_RICH_ROWS.extend(json_list_field(_row, 'final_body_refs_json'))
    FROZEN_AFTER_RICH_ROWS.extend(json_list_field(_row, 'final_incoming_json'))
for _row in SLOT_ROWS:
    FROZEN_AFTER_RICH_ROWS.extend(json_list_field(_row, 'after_refs_from_json'))
for _row in CARVE_ROWS.values():
    FROZEN_AFTER_RICH_ROWS.extend(_row['refs_from'])
FROZEN_AFTER_RICH_ROWS.extend(CALLBACK_PLAN['after']['refs_from'])
FROZEN_AFTER_RICH_ROWS.extend(HOLDER_PLAN['after']['references_from'])
FROZEN_AFTER_RICH_ROWS.extend(HOLDER_PLAN['after']['references_to'])
FROZEN_AFTER_RICH_ROWS.extend(EXTERNAL_DERIVED_PLAN['after_body_refs'])


def parse_number(value):
    if isinstance(value, (int, long)):
        return long(value) & 0xffffffff
    return long(value, 16) & 0xffffffff


def bool_field(value):
    return value.lower() == 'true'


def verify_inputs():
    for relative, digest in sorted(INPUT_HASHES.items()):
        exact('INPUT_HASH_' + relative, file_hash(os.path.join(ROOT, relative)), digest)
    manifest = read_json('f15-seg5-freeze-manifest.json')
    frozen = manifest['formal'] + manifest['plans'] + manifest['evidence']
    require(len(frozen) == 28, 'FREEZE_INPUT_COUNT')
    for item in frozen:
        path = os.path.join(ROOT, item['path'])
        exact('FREEZE_' + item['path'],
              [file_hash(path), os.path.getsize(path)],
              [item['sha256'], long(item.get('bytes', item.get('size')))])
    prior = manifest['prior_review']
    exact('PRIOR_REVIEW', file_hash(os.path.join(ROOT, prior['path'])),
          prior['sha256'])
    require(len(SLOTS) == 50 and len(SLOT_ROWS) == 50, 'SLOT_COUNT')
    for action in ('EQ_ADD', 'REF_ADD', 'REF_PRESERVE'):
        require(sum(row['action'] == action for row in SLOT_ROWS) == EXPECTED_COUNTS[action],
                action + '_COUNT')
    require(len(PLATES) == 14 and len(PLATE_WRITES) == 14 and
            len(NEW_FUNCTION_ROWS) == 1 and len(RENAME_ROWS) == 2,
            'FUNCTION_PLATE_COUNTS')
    require(len(OBSERVER_FUNCTIONS) == 340 and len(set(OBSERVER_FUNCTIONS)) == 340,
            'OBSERVER_FUNCTION_COUNT')
    require(len(WORD_ADDRESSES) == 1444 and len(set(WORD_ADDRESSES)) == 1444,
            'WORD_OBSERVER_COUNT')
    require(len(STATE_ADDRESSES) == 9497 and len(set(STATE_ADDRESSES)) == 9497,
            'STATE_OBSERVER_COUNT')
    require(len(TARGETS) == 10 and DYNAMIC_TARGETS == set([0x09e488d8]),
            'TARGET_COUNTS')
    require(len(CODE_RANGES) == 1 and len(INITIAL_SEEDS) == 1 and
            len(INSTRUCTION_ADDRESSES) == 20 and len(POOL_ADDRESSES) == 2 and
            len(PADDING_RANGES) == 0 and len(FLOW_ROWS) == 1 and
            len(PC_ROWS) == 2 and len(FALLTHROUGH_PAIRS) == 19,
            'R4_COUNTS')
    require(len(CARVE_ROWS) == 6 and len(CARVE_BOOKENDS) == 2 and
            CARVE_PLAN['counts']['create_dwords'] == 4 and
            CARVE_PLAN['counts']['aux_even_function_refs'] == 3,
            'CARVE_COUNTS')
    require(len(EQUATE_BINDINGS) == 35 and len(EQUATE_NAMES) == 24 and
            len(ROOT_GLOBAL_EQUATE_NAMES) == 2425 and
            len(ALL_EQUATE_NAMES) == 2430 and
            len(FINAL_EQUATE_NAMES) == 2429 and
            len(RETIRED_EQUATE_NAMES) == 1 and
            GLOBAL_PLAN['before_bindings'] == 12325 and
            GLOBAL_PLAN['after_bindings'] == 12359,
            'GLOBAL_EQUATE_COUNTS')
    require(sum(GLOBAL_EQ_PRESTATE[name] is None for name in ALL_EQUATE_NAMES) == 5,
            'PLANNED_GLOBAL_EQUATE_NULL_COUNT')
    require(len(APPROVED_PRIMARY_PROJECTIONS) == 62,
            'APPROVED_PRIMARY_PROJECTION_COUNT')
    require(len(FROZEN_ADDITION_REFS) == 22 and
            len(NEW_FUNCTION_FINAL_REFS) == 3 and
            len(FROZEN_AFTER_RICH_ROWS) == 397,
            'FROZEN_RICH_ADDITION_COUNTS')
    require(0x09e48e9c not in APPROVED_PRIMARY_PROJECTIONS and
            APPROVED_PRIMARY_PROJECTIONS.get(0x080bacf0) == {
                'name': 'LAB_080bacf0', 'type': 'Label',
                'source': 'DEFAULT', 'id': None},
            'PRIMARY_GRAPH_CALLBACK_EXCLUDED_BACF0_INCLUDED')
    for index, item in enumerate(FROZEN_AFTER_RICH_ROWS):
        errors = frozen_after_contract_errors(item)
        require(not errors, 'FROZEN_AFTER_RICH_%04d' % index,
                errors, item)
    dynamic_targets = set(int(item['to'], 16) for item in FROZEN_AFTER_RICH_ROWS
                          if isinstance(item.get('target_primary_id'), basestring))
    require(all(target in APPROVED_PRIMARY_PROJECTIONS and
                APPROVED_PRIMARY_PROJECTIONS[target]['id'] is None
                for target in dynamic_targets),
            'FROZEN_DYNAMIC_TARGET_COVERAGE', sorted(dynamic_targets))
    require(len(dynamic_targets) == 54,
            'FROZEN_DYNAMIC_TARGET_COUNT', len(dynamic_targets), 54)
    for row in SLOT_ROWS:
        require(row['final_symbol_source'] == 'USER_DEFINED',
                'SLOT_SOURCE_CONTRACT_' + row['address'])
        require(all(ord(char) < 128 for char in row['new_eol_ascii']),
                'EOL_ASCII_' + row['address'])
    source_names = [row['final_slot_label'] for row in SLOT_ROWS]
    require(len(source_names) == len(set(source_names)), 'SOURCE_LABEL_UNIQUENESS')
    for value, row in sorted(PLATE_WRITES.items()):
        text = row['new_plate']
        require(all(ord(char) < 128 for char in text) and len(text) <= 500 and
                len(text) == int(row['new_plate_chars']), 'PLATE_ASCII_%08x' % value)
    require(max(int(row['new_plate_chars']) for row in PLATE_WRITES.values()) == 485,
            'PLATE_MAX_WRITTEN_485')
    for value, row in sorted(NEW_FUNCTION_ROWS.items()):
        collisions = [item for item in symbols.getGlobalSymbols(row['final_name'])
                      if item.getAddress() != toAddr(value)]
        require(not collisions, 'FUNCTION_NAME_COLLISION_%08x' % value)
    reject('INPUTS')


def capture():
    return {
        'status': 'F15_SEG5_FRESH_FULL_PRESTATE',
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
        'targets': [address_state(value) for value in TARGETS],
        'equate_globals': dict((name, equate_global_row(name))
                                for name in ALL_EQUATE_NAMES),
        'units': [unit_row(value) for value in range(MODULE_START, MODULE_END)],
    }


def require_external_state(value, actual, expected, prefix):
    for key in ('address', 'bytes', 'rom_word', 'symbols', 'symbol_count',
                'primary_symbol', 'data_at', 'data_containing',
                'references_from', 'references_to',
                'equates', 'equate_references', 'eol', 'pre', 'post',
                'repeatable', 'plate', 'tmode'):
        if key in expected:
            if key in ('references_from', 'references_to'):
                same_set('%s_%s_%08x' % (prefix, key.upper(), value),
                         actual[key], expected[key])
            else:
                exact('%s_%s_%08x' % (prefix, key.upper(), value),
                      actual[key], expected[key])
    for key in ('function_at', 'function_containing'):
        if key not in expected:
            continue
        wanted = expected[key]
        observed = actual[key]
        if wanted is None:
            exact('%s_%s_%08x' % (prefix, key.upper(), value), observed, None)
        elif isinstance(wanted, basestring):
            require(observed is not None and observed['name'] == wanted,
                    '%s_%s_%08x' % (prefix, key.upper(), value), observed, wanted)
        else:
            exact('%s_%s_%08x' % (prefix, key.upper(), value), observed, wanted)
    if 'instruction' in expected:
        wanted = expected['instruction']
        observed = actual['instruction_at']
        if wanted is None:
            exact('%s_INSTRUCTION_%08x' % (prefix, value), observed, None)
        else:
            require(observed is not None and observed['text'] == wanted,
                    '%s_INSTRUCTION_%08x' % (prefix, value), observed, wanted)


def require_slot_pre(value, row, state):
    require(state['rom_word'] == int(row['original_value'], 16) and
            state['bytes'] == row['old_bytes'], 'SLOT_VALUE_%08x' % value)
    exact('SLOT_SYMBOLS_%08x' % value, state['symbols'],
          json_list_field(row, 'old_symbols_json'))
    exact('SLOT_PRIMARY_%08x' % value, state['primary_symbol'],
          json_value_field(row, 'old_primary_json'))
    same_set('SLOT_REFS_FROM_%08x' % value, state['references_from'],
             json_list_field(row, 'refs_from_json'))
    expected_refs_to = ([] if row.get('origin') == 'R4_NEW_POOL'
                        else json_list_field(row, 'refs_to_json'))
    same_set('SLOT_REFS_TO_%08x' % value, state['references_to'], expected_refs_to)
    exact('SLOT_EQUATES_%08x' % value, state['equates'],
          json_list_field(row, 'equates_json'))
    expected_eq_refs = []
    for item in json_list_field(row, 'equates_json'):
        expected_eq_refs.append({'name': item['name'], 'value': parse_number(item['value']),
                                 'operand': int(item.get('operand', 0))})
    exact('SLOT_EQ_REFS_PRE_%08x' % value,
          state['equate_references'], expected_eq_refs)
    exact('SLOT_EOL_%08x' % value, state['eol'], json_value_field(row, 'old_eol_json'))
    if row['old_data_type'] not in ('', 'NONE'):
        require(state['data_at'] is not None and state['data_at']['length'] == 4 and
                state['data_at']['type'] == row['old_data_type'], 'SLOT_DATA_%08x' % value)
    else:
        require(state['data_at'] is None and state['data_containing'] is None and
                state['instruction_at'] is None,
                'SLOT_UNTYPED_%08x' % value)
    owner = None if state['function_containing'] is None else state['function_containing']['name']
    expected_owner = (None if row['old_function_owner'] in ('', 'null')
                      else row['old_function_owner'])
    require(owner == expected_owner, 'SLOT_OWNER_%08x' % value, owner, expected_owner)


def require_plate_pre(value, row, actual):
    if value in NEW_FUNCTION_ROWS:
        require(actual is None and row['current_name'] == 'ABSENT' and
                row['function_id'] == 'NEW_USER_FUNCTION_ID' and row['body_size'] == '0' and
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
    same_set('FUNCTION_BODY_REFS_%08x' % value, actual['body_references'],
             json_list_field(row, 'body_refs_json'))


def require_carve_pre(value, row, state):
    require_external_state(value, state, row['old_state'], 'CARVE_PRE')
    data = state['data_at']
    if row['old_state']['data_at'] is None:
        require(data is None and state['data_containing'] is None and
                state['instruction_at'] is None, 'CARVE_UNTYPED_PRE_%08x' % value)
    else:
        require(data is not None and data['type'] == '/dword' and
                data['length'] == 4 and state['instruction_at'] is None,
                'CARVE_DATA_PRE_%08x' % value)


def verify_prestate(pre, recapture):
    if recapture:
        exact('FRESH_PRESTATE_EXACT', capture(), pre)
    require(pre['function_count'] == 5413, 'FUNCTION_COUNT_PRE')
    require(pre['segment']['size'] == (SEGMENT_END - SEGMENT_START) and
            pre['module']['size'] == 49408,
            'RANGE_SIZE_PRE')
    require(len(pre['functions']) == 340 and len(pre['words']) == 1444 and
            len(pre['states']) == 9497 and len(pre['units']) == 49408 and
            len(pre['targets']) == 10 and len(pre['equate_globals']) == 2430,
            'PRESTATE_COUNTS')
    function_map = dict(zip(OBSERVER_FUNCTIONS, pre['functions']))
    state_map = dict((int(row['address'], 16), row) for row in pre['states'])
    target_map = dict((int(row['address'], 16), row) for row in pre['targets'])
    require(sum(row is None for row in pre['functions']) == 2,
            'ABSENT_FUNCTION_COUNT')
    for value, row in sorted(SLOTS.items()):
        require_slot_pre(value, row, state_map[value])
        collisions = [symbol for symbol in symbols.getGlobalSymbols(row['final_slot_label'])
                      if symbol.getAddress() != toAddr(value)]
        require(not collisions, 'SLOT_NAME_COLLISION_%08x' % value)
    for value, row in sorted(PLATES.items()):
        require_plate_pre(value, row, function_map[value])
    for value, row in sorted(CARVE_ROWS.items()):
        require_carve_pre(value, row, state_map[value])
    require_external_state(CALLBACK_SOURCE, state_map[CALLBACK_SOURCE],
                           CALLBACK_PLAN['old_state'], 'CALLBACK_PRE')
    require_external_state(HOLDER_SOURCE, state_map[HOLDER_SOURCE],
                           HOLDER_PLAN['before'], 'HOLDER_PRE')
    holder_ref = HOLDER_PLAN['before']['references_from'][0]
    holder_odd_primary = symbols.getPrimarySymbol(toAddr(HOLDER_ODD_TARGET))
    require(holder_odd_primary is not None and
            long(holder_odd_primary.getID()) == long(holder_ref['target_primary_id']) and
            unicode(holder_odd_primary.getName(True)) == holder_ref['target_primary_name'] and
            str(holder_odd_primary.getSymbolType()) == holder_ref['target_primary_type'] and
            str(holder_odd_primary.getSource()) == holder_ref['target_primary_source'],
            'HOLDER_ODD_PRIMARY_PRE')
    for value, row in sorted(CARVE_BOOKENDS.items()):
        require_external_state(value, state_map[value], row, 'CARVE_BOOKEND_PRE')
    for target in TARGETS:
        rows = [row for row in SLOT_ROWS if row['action'].startswith('REF_') and
                int(row['original_value'], 16) == target]
        expected = json_value_field(rows[0], 'target_prestate_json')
        if expected is None:
            expected = ROOT_STATE_PRESTATE[target]
        require_external_state(target, target_map[target], expected, 'TARGET_PRE')
        for row in rows[1:]:
            duplicate = json_value_field(row, 'target_prestate_json')
            if duplicate is not None:
                exact('TARGET_DUPLICATE_%08x' % target, duplicate, expected)
    verify_global_equate_pre(pre['equate_globals'])
    reject('PRESTATE_VERIFY')


def verify_plan(plan, prestate_hash):
    require(plan.get('status') == 'F15_SEG5_PLAN_FROZEN', 'PLAN_STATUS')
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
            plan.get('observer_function_count') == len(OBSERVER_FUNCTIONS) and
            plan.get('word_count') == len(WORD_ADDRESSES) and
            plan.get('state_count') == len(STATE_ADDRESSES) and
            plan.get('slots') == sorted(SLOTS) and plan.get('targets') == TARGETS and
            plan.get('carve_words') == sorted(CARVE_ROWS) and
            plan.get('callback_source') == CALLBACK_SOURCE and
            plan.get('holder_source') == HOLDER_SOURCE and
            plan.get('new_functions') == sorted(NEW_FUNCTION_ROWS) and
            plan.get('r4_instruction_count') == len(INSTRUCTION_ADDRESSES) and
            plan.get('planned_equate_names') == EQUATE_NAMES and
            plan.get('protected_equate_names') == PROTECTED_EQUATE_NAMES and
            plan.get('all_equate_names') == ALL_EQUATE_NAMES and
            plan.get('final_equate_names') == FINAL_EQUATE_NAMES,
            'PLAN_SCOPE')
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


def remove_equate_binding(name, address, operand):
    eq = equates.getEquate(name)
    if eq is None:
        raise RuntimeError('Old Equate missing: ' + name)
    matches = [ref for ref in eq.getReferences()
               if ref.getAddress() == toAddr(address) and ref.getOpIndex() == operand]
    if len(matches) != 1:
        raise RuntimeError('Old Equate binding multiplicity at %08x' % address)
    eq.removeReference(toAddr(address), operand)


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
        command = DisassembleCommand(toAddr(value), APPROVED_CODE_SET, True)
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
        command = DisassembleCommand(toAddr(value), APPROVED_CODE_SET, True)
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
        if (listing.getInstructionContaining(toAddr(value)) is not None or
                listing.getInstructionContaining(toAddr(value + 3)) is not None or
                listing.getDefinedDataContaining(toAddr(value)) is not None or
                listing.getDefinedDataContaining(toAddr(value + 3)) is not None):
            raise RuntimeError('R4 pool occupied at %08x' % value)
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


def rename_functions():
    for value, row in sorted(RENAME_ROWS.items()):
        fn = functions.getFunctionAt(toAddr(value))
        if fn is None or unicode(fn.getName()) != row['current_name']:
            raise RuntimeError('Rename precondition at %08x' % value)
        fn.setName(row['final_name'], SourceType.USER_DEFINED)
        COUNTS['FUNC_RENAME'] += 1


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


def apply_carve():
    for value, row in sorted(CARVE_ROWS.items()):
        old = row['old_state']
        if bytes_hex(value, 4) != old['bytes']:
            raise RuntimeError('Carve bytes changed at %08x' % value)
        data = listing.getDefinedDataAt(toAddr(value))
        if old['data_at'] is None:
            if data is not None or listing.getInstructionContaining(toAddr(value)) is not None:
                raise RuntimeError('Carve new dword occupied at %08x' % value)
            listing.createData(toAddr(value), DWordDataType.dataType)
            COUNTS['CARVE_DATA_CREATE'] += 1
        elif (data is None or data.getLength() != 4 or
              unicode(data.getDataType().getPathName()) != '/dword'):
            raise RuntimeError('Carve preserved dword drift at %08x' % value)
        ensure_slot_label(value, row['final_label'])
        for item in row['equates']:
            ensure_equate(item['name'], long(item['value']) & 0xffffffff,
                           value, int(item['operand']))
        for item in row['refs_from']:
            if not add_approved_data_ref(value, item):
                raise RuntimeError('Carve DATA ref unexpectedly existed at %08x' % value)
            COUNTS['CARVE_DATA_REF'] += 1
        COUNTS['CARVE_WORDS'] += 1


def apply_callback_source():
    old_item = CALLBACK_PLAN['old_state']['equate_references'][0]
    remove_equate_binding(old_item['name'], CALLBACK_SOURCE, int(old_item['operand']))
    item = CALLBACK_PLAN['after']['equates'][0]
    ensure_equate(item['name'], long(item['value']) & 0xffffffff,
                   CALLBACK_SOURCE, int(item['operand']))
    ref_item = CALLBACK_PLAN['after']['refs_from'][0]
    if not add_approved_data_ref(CALLBACK_SOURCE, ref_item):
        raise RuntimeError('Callback DATA ref unexpectedly existed')
    COUNTS['CALLBACK_EQ_REBIND'] += 1
    COUNTS['CALLBACK_DATA_REF'] += 1
    for name in RETIRED_EQUATE_NAMES:
        eq = equates.getEquate(name)
        if eq is None or int(eq.getReferenceCount()) != 0:
            raise RuntimeError('Retired Equate still bound: ' + name)
        equates.removeEquate(name)
        COUNTS['GLOBAL_EQ_REMOVE'] += 1


def apply_all():
    apply_r4()
    create_functions()
    apply_carve()
    apply_callback_source()
    apply_slots()
    rename_functions()
    for value, row in sorted(PLATE_WRITES.items()):
        listing.setComment(toAddr(value), CodeUnit.PLATE_COMMENT, row['new_plate'])
        COUNTS['PLATE'] += 1


def strip_ref_derivatives(rows):
    return [ref_core(item) for item in rows]


RICH_REF_KEYS = ('from', 'to', 'operand', 'type', 'source', 'primary',
                 'target_primary_id', 'target_primary_name',
                 'target_primary_type', 'target_primary_source')


def frozen_after_contract_errors(row):
    errors = []
    if sorted(row) != sorted(RICH_REF_KEYS):
        return ['RICH10_KEYS']
    try:
        target = int(row['to'], 16)
    except ValueError:
        target = None
    projection = APPROVED_PRIMARY_PROJECTIONS.get(target)
    dynamic = isinstance(row['target_primary_id'], basestring)
    if dynamic:
        if not (row['target_primary_id'].startswith('DYNAMIC_') and
                projection is not None and projection['id'] is None):
            errors.append('DYNAMIC_TARGET_%08x' % target)
    elif projection is not None:
        if not (projection['id'] is not None and
                long(row['target_primary_id']) == long(projection['id'])):
            errors.append('STATIC_ID_%08x' % target)
    if projection is not None:
        if not (row['target_primary_name'] == projection['name'] and
                row['target_primary_type'] == projection['type'] and
                row['target_primary_source'] == projection['source']):
            errors.append('PRIMARY_META_%08x' % target)
    return errors


def validate_frozen_after_ref(row, prefix):
    errors = frozen_after_contract_errors(row)
    require(not errors, prefix + '_CONTRACT', errors, row)
    return not errors


def strict_frozen_after_ref_expected(row):
    result = json.loads(json.dumps(row))
    if not validate_frozen_after_ref(result, 'STRICT_AFTER'):
        return result
    try:
        target = int(result['to'], 16)
    except ValueError:
        return result
    projection = APPROVED_PRIMARY_PROJECTIONS.get(target)
    if isinstance(result['target_primary_id'], basestring):
        primary = symbols.getPrimarySymbol(toAddr(target))
        require(primary is not None and unicode(primary.getName(True)) == projection['name'] and
                str(primary.getSymbolType()) == projection['type'] and
                str(primary.getSource()) == projection['source'],
                'DYNAMIC_PRIMARY_CONTRACT_%08x' % target)
        result['target_primary_id'] = None if primary is None else long(primary.getID())
    return result


def strict_frozen_after_refs(rows):
    return [strict_frozen_after_ref_expected(row) for row in rows]


def project_old_pre_ref_expected(row):
    result = json.loads(json.dumps(row))
    try:
        target = int(result['to'], 16)
    except ValueError:
        return result
    projection = APPROVED_PRIMARY_PROJECTIONS.get(target)
    if projection is None:
        return result
    result['target_primary_name'] = projection['name']
    result['target_primary_type'] = projection['type']
    result['target_primary_source'] = projection['source']
    if projection['id'] is None:
        primary = symbols.getPrimarySymbol(toAddr(target))
        require(primary is not None and unicode(primary.getName(True)) == projection['name'] and
                str(primary.getSymbolType()) == projection['type'] and
                str(primary.getSource()) == projection['source'],
                'OLD_PRE_DYNAMIC_PRIMARY_%08x' % target)
        result['target_primary_id'] = None if primary is None else long(primary.getID())
    else:
        result['target_primary_id'] = long(projection['id'])
    return result


def project_old_pre_refs(rows):
    return [project_old_pre_ref_expected(row) for row in rows]


def ranges_contain(ranges, value):
    return any(int(lo, 16) <= value < int(hi, 16) for lo, hi in ranges)


def expected_additions_to(value):
    return [json.loads(json.dumps(item)) for item in FROZEN_ADDITION_REFS
            if int(item['to'], 16) == value]


def verify_strict_frozen_after_refs(prefix, rows):
    for item in rows:
        exact(prefix + '_' + item['from'] + '_' + item['to'],
              item, strict_frozen_after_ref_expected(item))


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
             strict_frozen_after_refs(json_list_field(row, 'after_refs_from_json')))
    if row.get('origin') == 'R4_NEW_POOL':
        expected_refs_to = strict_frozen_after_refs(expected_additions_to(value))
    else:
        expected_refs_to = project_old_pre_refs(json_list_field(row, 'refs_to_json'))
        expected_refs_to.extend(strict_frozen_after_refs(expected_additions_to(value)))
    same_set('SLOT_REFS_TO_POST_%08x' % value, actual['references_to'],
             expected_refs_to)
    expected_eq = [{'name': item['name'], 'value': parse_number(item['value'])}
                   for item in json_list_field(row, 'after_equates_json')]
    expected_eq_refs = [{'name': item['name'], 'value': parse_number(item['value']),
                         'operand': int(item['operand'])}
                        for item in json_list_field(row, 'after_equates_json')]
    exact('SLOT_EQ_POST_%08x' % value, actual['equates'], expected_eq)
    exact('SLOT_EQ_REF_POST_%08x' % value, actual['equate_references'], expected_eq_refs)
    exact('SLOT_OWNER_POST_%08x' % value, actual['function_containing'], None)


def verify_carve_post(value, row, before):
    actual = address_state(value)
    old = row['old_state']
    require(actual['bytes'] == old['bytes'] and actual['data_at'] is not None and
            actual['data_at']['length'] == 4 and actual['data_at']['type'] == '/dword' and
            actual['instruction_at'] is None and actual['function_containing'] is None,
            'CARVE_DATA_POST_%08x' % value)
    primary = actual['primary_symbol']
    require(actual['symbol_count'] == 1 and primary is not None and
            primary['name'] == row['final_label'] and primary['type'] == 'Label' and
            primary['source'] == 'USER_DEFINED' and primary['primary'] and primary['global'],
            'CARVE_LABEL_POST_%08x' % value)
    same_set('CARVE_REFS_FROM_POST_%08x' % value, actual['references_from'],
             strict_frozen_after_refs(row['refs_from']))
    expected_refs_to = project_old_pre_refs(old['references_to'])
    expected_refs_to.extend(strict_frozen_after_refs(expected_additions_to(value)))
    same_set('CARVE_REFS_TO_POST_%08x' % value, actual['references_to'],
             expected_refs_to)
    expected_eq = [{'name': item['name'], 'value': long(item['value']) & 0xffffffff}
                   for item in row['equates']]
    expected_eq_refs = [{'name': item['name'], 'value': long(item['value']) & 0xffffffff,
                         'operand': int(item['operand'])} for item in row['equates']]
    exact('CARVE_EQ_POST_%08x' % value, actual['equates'], expected_eq)
    exact('CARVE_EQ_REFS_POST_%08x' % value, actual['equate_references'], expected_eq_refs)
    for key in ('pre', 'post', 'repeatable', 'plate', 'tmode'):
        exact('CARVE_%s_POST_%08x' % (key.upper(), value), actual[key], old[key])


def verify_callback_post(before):
    actual = address_state(CALLBACK_SOURCE)
    old = CALLBACK_PLAN['old_state']
    after = CALLBACK_PLAN['after']
    require(actual['bytes'] == old['bytes'] and actual['rom_word'] == old['rom_word'] and
            actual['data_at'] is not None and actual['data_at']['length'] == 4 and
            actual['data_at']['type'] == after['data_type'] and
            actual['instruction_at'] is None and actual['function_containing'] is None,
            'CALLBACK_DATA_POST')
    exact('CALLBACK_SYMBOLS_POST', actual['symbols'], after['symbols'])
    exact('CALLBACK_PRIMARY_POST', actual['primary_symbol'], after['primary_symbol'])
    same_set('CALLBACK_REFS_FROM_POST', actual['references_from'],
             strict_frozen_after_refs(after['refs_from']))
    same_set('CALLBACK_REFS_TO_POST', actual['references_to'],
             strict_frozen_after_refs(after['refs_to']))
    expected_eq = [{'name': item['name'], 'value': long(item['value']) & 0xffffffff}
                   for item in after['equates']]
    expected_eq_refs = [{'name': item['name'], 'value': long(item['value']) & 0xffffffff,
                         'operand': int(item['operand'])} for item in after['equates']]
    exact('CALLBACK_EQ_POST', actual['equates'], expected_eq)
    exact('CALLBACK_EQ_REFS_POST', actual['equate_references'], expected_eq_refs)
    for key in ('eol', 'pre', 'post', 'repeatable', 'plate', 'tmode'):
        expected = after['eol'] if key == 'eol' else old[key]
        exact('CALLBACK_%s_POST' % key.upper(), actual[key], expected)


def verify_holder_post():
    require_external_state(HOLDER_SOURCE, address_state(HOLDER_SOURCE),
                           HOLDER_PLAN['after'], 'HOLDER_POST')
    expected = HOLDER_PLAN['after']['references_from'][0]
    primary = symbols.getPrimarySymbol(toAddr(HOLDER_ODD_TARGET))
    require(primary is not None and long(primary.getID()) == long(expected['target_primary_id']) and
            unicode(primary.getName(True)) == expected['target_primary_name'] and
            str(primary.getSymbolType()) == expected['target_primary_type'] and
            str(primary.getSource()) == expected['target_primary_source'],
            'HOLDER_ODD_PRIMARY_POST')


def verify_bookend_post(value, before):
    expected = json.loads(json.dumps(before))
    if value == 0x09e488f0:
        expected['references_to'] = project_old_pre_refs(expected['references_to'])
        expected['references_to'].extend(
            strict_frozen_after_refs(expected_additions_to(value)))
    require_external_state(value, address_state(value), expected, 'CARVE_BOOKEND_POST')


def verify_external_derived_post():
    fn = function_row(EXTERNAL_DERIVED_FUNCTION)
    require(fn is not None, 'EXTERNAL_DERIVED_FUNCTION_PRESENT')
    same_set('EXTERNAL_DERIVED_BODY_REFS', fn['body_references'],
             strict_frozen_after_refs(EXTERNAL_DERIVED_PLAN['after_body_refs']))


def verify_preserved_target_post(value, before):
    actual = address_state(value)
    same_set('TARGET_REFS_TO_CORE_%08x' % value,
             strip_ref_derivatives(actual['references_to']),
             strip_ref_derivatives(before['references_to']) +
             strip_ref_derivatives(expected_additions_to(value)))
    expected_refs = project_old_pre_refs(before['references_to'])
    expected_refs.extend(strict_frozen_after_refs(expected_additions_to(value)))
    same_set('TARGET_REFS_TO_RICH_%08x' % value, actual['references_to'], expected_refs)
    for key in ('symbols', 'symbol_count', 'primary_symbol', 'bytes', 'rom_word',
                'data_at', 'data_containing', 'instruction_at', 'function_at',
                'function_containing', 'references_from', 'equates',
                'equate_references', 'eol', 'pre', 'post', 'repeatable', 'plate', 'tmode'):
        exact('TARGET_PRESERVE_%s_%08x' % (key.upper(), value), actual[key], before[key])


def verify_target_post(value, before):
    if value in CARVE_ROWS:
        return
    verify_preserved_target_post(value, before)


def expected_instruction_refs(value):
    return [ref_core(item) for item in NEW_FUNCTION_FINAL_REFS
            if int(item['from'], 16) == value]


def verify_r4_post(pre):
    actual_starts = set()
    flow_pairs = []
    pc_pairs = []
    fallthrough_pairs = []
    for lo, hi in CODE_RANGES:
        actual_starts.update(instruction_starts_in_range(lo, hi))
    exact('R4_START_SET', sorted(actual_starts), INSTRUCTION_ADDRESSES)
    for value in INSTRUCTION_ADDRESSES:
        row = INSTRUCTION_ROWS[value]
        inst = listing.getInstructionAt(toAddr(value))
        require(inst is not None and int(inst.getLength()) == int(row['length']) and
                bytes_hex(value, int(row['length'])) == row['bytes'] and
                str(inst.getFlowOverride()) == 'NONE', 'R4_INSTRUCTION_%08x' % value)
        context = currentProgram.getProgramContext().getValue(
            tmode_register, toAddr(value), False)
        require(context is not None and int(context) == 1, 'R4_TMODE_%08x' % value)
        owner = functions.getFunctionContaining(toAddr(value))
        host = INSTRUCTION_OWNER[value]
        require(owner is not None and long(owner.getEntryPoint().getOffset()) == host and
                unicode(owner.getName()) == NEW_FUNCTION_ROWS[host]['final_name'],
                'R4_OWNER_%08x' % value)
        same_set('R4_REFS_%08x' % value, exact_ref_cores(value),
                 expected_instruction_refs(value))
        for target in inst.getFlows():
            flow_pairs.append((value, long(target.getOffset())))
        for ref in references.getReferencesFrom(toAddr(value)):
            if str(ref.getReferenceType()) == 'READ' and int(ref.getOperandIndex()) == 1:
                pc_pairs.append((value, long(ref.getToAddress().getOffset())))
        target = inst.getFallThrough()
        if target is not None:
            fallthrough_pairs.append((value, long(target.getOffset())))
    exact('R4_FLOW_SET', sorted(flow_pairs),
          sorted((int(item['from'], 16), int(item['to'], 16)) for item in FLOW_ROWS))
    exact('R4_PC_SET', sorted(pc_pairs),
          sorted((int(item['from'], 16), int(item['to'], 16)) for item in PC_ROWS))
    exact('R4_FALLTHROUGH_SET', sorted(fallthrough_pairs), FALLTHROUGH_PAIRS)
    for value in POOL_ADDRESSES:
        state = address_state(value)
        require(state['data_at'] is not None and state['data_at']['length'] == 4 and
                state['data_at']['type'] == '/undefined4' and
                state['instruction_at'] is None and state['function_containing'] is None,
                'R4_POOL_%08x' % value)


def function_static_core(row):
    return dict((key, row[key]) for key in (
        'entry', 'name', 'symbol', 'symbols', 'symbol_count', 'namespace',
        'body', 'body_ranges', 'body_size',
        'body_sha256', 'eol_comments', 'calling_convention', 'signature_source',
        'prototype', 'custom_variable_storage', 'varargs', 'inline', 'no_return',
        'external', 'thunk', 'thunk_target', 'stack_purge_size', 'return',
        'parameters', 'plate'))


def projected_function(before, value):
    if before is None:
        return None
    result = json.loads(json.dumps(before))
    if value in RENAME_ROWS:
        old_name = RENAME_ROWS[value]['current_name']
        new_name = RENAME_ROWS[value]['final_name']
        result['name'] = new_name
        result['symbol']['name'] = new_name
        result['symbol']['qualified_name'] = new_name
        for item in result['symbols']:
            if item['type'] == 'Function' and item['name'] == old_name:
                item['name'] = new_name
                item['qualified_name'] = new_name
        result['prototype'] = result['prototype'].replace(old_name, new_name, 1)
    if value in PLATE_WRITES:
        result['plate'] = PLATE_WRITES[value]['new_plate']
    if value in PLATES:
        result['body_references'] = strict_frozen_after_refs(
            json_list_field(PLATES[value], 'final_body_refs_json'))
        result['incoming'] = strict_frozen_after_refs(
            json_list_field(PLATES[value], 'final_incoming_json'))
    else:
        result['body_references'] = project_old_pre_refs(result['body_references'])
        result['incoming'] = project_old_pre_refs(result['incoming'])
        result['incoming'].extend(strict_frozen_after_refs(expected_additions_to(value)))
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
        }
    for key in ('is_auto_parameter', 'is_register_variable',
                'is_stack_variable', 'is_memory_variable'):
        expected_return.setdefault(key, False)
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
             strict_frozen_after_refs(json_list_field(row, 'final_incoming_json')))
    same_set('NEW_FUNCTION_BODY_REFS_%08x' % value,
             actual['body_references'],
             strict_frozen_after_refs(json_list_field(row, 'final_body_refs_json')))


def verify_units_post(pre):
    pre_units = dict((int(row['address'], 16), row) for row in pre['units'])
    for value in range(MODULE_START, MODULE_END):
        if value in CODE_BYTES or value in POOL_BYTES:
            continue
        actual = unit_row(value)
        expected = json.loads(json.dumps(pre_units[value]))
        owner = expected['function_owner']
        if owner is not None:
            entry = int(owner['entry'], 16)
            if entry in RENAME_ROWS:
                owner['name'] = RENAME_ROWS[entry]['final_name']
        exact('UNIT_STATIC_%08x' % value, actual, expected)
    for value in INSTRUCTION_ADDRESSES:
        actual = unit_row(value)
        row = INSTRUCTION_ROWS[value]
        require(actual['unit_class'] == 'InstructionDB' and
                actual['unit_length'] == int(row['length']) and
                actual['unit_min'] == '%08x' % value and actual['tmode'] == 1 and
                actual['function_owner'] is not None and
                int(actual['function_owner']['entry'], 16) == INSTRUCTION_OWNER[value],
                'UNIT_CODE_%08x' % value)
    for value in POOL_ADDRESSES:
        actual = unit_row(value)
        require(actual['unit_class'] == 'DataDB' and actual['unit_length'] == 4 and
                actual['unit_min'] == '%08x' % value and
                actual['defined_data_at']['type'] == '/undefined4' and
                actual['function_owner'] is None,
                'UNIT_POOL_%08x' % value)
def verify_global_equates(pre):
    for name, expected in sorted(GLOBAL_PLAN['after'].items()):
        actual = equate_global_row(name)
        require(actual is not None and actual['value'] == long(expected['value']),
                'GLOBAL_EQ_VALUE_' + name)
        same_set('GLOBAL_EQ_REFS_' + name, actual['references'], expected['references'])
    for name in RETIRED_EQUATE_NAMES:
        exact('RETIRED_GLOBAL_EQ_' + name, equate_global_row(name), None)


def verify_generic_state_post(value, before):
    actual = address_state(value)
    expected = json.loads(json.dumps(before))
    for key in ('function_at', 'function_containing'):
        owner = expected.get(key)
        if owner is not None:
            entry = int(owner['entry'], 16)
            if entry in RENAME_ROWS:
                owner['name'] = RENAME_ROWS[entry]['final_name']
    if value in RENAME_ROWS:
        old_name = RENAME_ROWS[value]['current_name']
        new_name = RENAME_ROWS[value]['final_name']
        for item in expected['symbols']:
            if item['type'] == 'Function' and item['name'] == old_name:
                item['name'] = new_name
                item['qualified_name'] = new_name
        primary = expected['primary_symbol']
        if primary is not None and primary['type'] == 'Function' and primary['name'] == old_name:
            primary['name'] = new_name
            primary['qualified_name'] = new_name
    expected['references_from'] = project_old_pre_refs(expected['references_from'])
    expected['references_to'] = project_old_pre_refs(expected['references_to'])
    expected['references_to'].extend(
        strict_frozen_after_refs(expected_additions_to(value)))
    if value in PLATE_WRITES:
        expected['plate'] = PLATE_WRITES[value]['new_plate']
    for key in sorted(expected):
        if key in ('references_from', 'references_to'):
            same_set('STATE_%s_POST_%08x' % (key.upper(), value),
                     actual[key], expected[key])
        else:
            exact('STATE_%s_POST_%08x' % (key.upper(), value),
                  actual[key], expected[key])


def verify_states_post(pre):
    state_map = dict((int(row['address'], 16), row) for row in pre['states'])
    target_map = dict((int(row['address'], 16), row) for row in pre['targets'])
    handled = set()
    for value, row in sorted(SLOTS.items()):
        if value in state_map:
            verify_slot_post(value, row, state_map[value])
            handled.add(value)
    for value, row in sorted(CARVE_ROWS.items()):
        if value in state_map:
            verify_carve_post(value, row, state_map[value])
            handled.add(value)
    verify_callback_post(state_map[CALLBACK_SOURCE])
    handled.add(CALLBACK_SOURCE)
    verify_holder_post()
    handled.add(HOLDER_SOURCE)
    for value, row in sorted(CARVE_BOOKENDS.items()):
        verify_bookend_post(value, row)
        handled.add(value)
    for value in TARGETS:
        verify_target_post(value, target_map[value])
        if value in state_map:
            handled.add(value)
    for value in STATE_ADDRESSES:
        if (value in handled or value in CODE_BYTES or value in POOL_BYTES or
                value in NEW_FUNCTION_BODY_BYTES):
            continue
        if value in NEW_FUNCTION_ROWS:
            continue
        verify_generic_state_post(value, state_map[value])


def verify_post(pre):
    require(pre['function_count'] == 5413 and
            int(functions.getFunctionCount()) == 5414,
            'FUNCTION_COUNT_POST')
    require(raw_hash(SEGMENT_START, SEGMENT_END) == pre['segment']['sha256'] and
            raw_hash(MODULE_START, MODULE_END) == pre['module']['sha256'],
            'RAW_HASH_POST')
    verify_r4_post(pre)
    verify_states_post(pre)

    word_map = dict((int(row['address'], 16), row) for row in pre['words'])
    for value in WORD_ADDRESSES:
        if (value in SLOTS or value in CARVE_ROWS or value in CODE_BYTES or
                value in POOL_BYTES or value in NEW_FUNCTION_BODY_BYTES):
            continue
        verify_generic_state_post(value, word_map[value])
    verify_units_post(pre)

    function_map = dict(zip(OBSERVER_FUNCTIONS, pre['functions']))
    for value in OBSERVER_FUNCTIONS:
        before = function_map[value]
        if value in NEW_FUNCTION_ROWS:
            exact('NEW_FUNCTION_PRE_NULL_%08x' % value, before, None)
            verify_new_function(value, NEW_FUNCTION_ROWS[value])
            continue
        actual = function_row(value)
        if before is None:
            exact('FUTURE_FUNCTION_STAYS_NULL_%08x' % value, actual, None)
            continue
        expected = projected_function(before, value)
        exact('FUNCTION_STATIC_POST_%08x' % value,
              function_static_core(actual), function_static_core(expected))
        same_set('FUNCTION_BODY_REFS_POST_%08x' % value,
                 actual['body_references'], expected['body_references'])
        same_set('FUNCTION_INCOMING_POST_%08x' % value,
                 actual['incoming'], expected['incoming'])

    verify_external_derived_post()
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


print('=== RefineF15Seg5 mode=%s ===' % MODE)
verify_inputs()

if MODE == 'prestate':
    state = capture()
    verify_prestate(state, False)
    write_json(PRESTATE_NAME, state)
    print('PRESTATE functions=340 words=1444 states=9497 globals=2430 units=49408 FAIL=0')
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
            'status': 'F15_SEG5_DRY_PREFLIGHT_OK', 'FAIL': 0,
            'script_sha256': file_hash(getSourceFile().getAbsolutePath()),
            'plan_sha256': file_hash(os.path.join(RUN, PLAN_NAME)),
            'prestate_sha256': prestate_hash, 'counts': EXPECTED_COUNTS,
            'preflight': {'functions': 340, 'words': 1444, 'states': 9497,
                          'slots': 50, 'targets': 10,
                          'r4_instructions': 20, 'r4_flows': 1,
                          'pc_read_consumers': 2,
                          'carve_words': 6, 'carve_data_refs': 3,
                          'global_equates': 2430, 'global_existing': 2425,
                          'global_absent_planned': 5, 'units': 49408},
            'semantic_actions_applied': False,
        }
        write_json('f15-seg5-dry-result-%s.json' % EVIDENCE_VERSION, result)
        print('STATUS: OK mode=dry FAIL=0 semantic_actions_applied=false')
    elif MODE == 'fullrollback':
        verify_prestate(prestate, True)
        transaction = currentProgram.startTransaction('F15-Seg-5 Phase1 full rollback validation')
        post_verified = False
        rollback_forced = False
        error = None
        try:
            apply_all()
            verify_post(prestate)
            post_verified = True
            raise RuntimeError('F15_SEG5_EXPECTED_FORCED_ROLLBACK')
        except Exception as caught:
            if post_verified and unicode(caught) == 'F15_SEG5_EXPECTED_FORCED_ROLLBACK':
                rollback_forced = True
            else:
                error = caught
                write_json('f15-seg5-full-rollback-failure-%s.json' % EVIDENCE_VERSION,
                           failure_payload('FULLROLLBACK', caught))
                traceback.print_exc()
        finally:
            currentProgram.endTransaction(transaction, False)
        if not post_verified or not rollback_forced:
            raise RuntimeError('F15-Seg-5 full rollback validation failed: %s' % unicode(error))
        result = {
            'status': 'F15_SEG5_FULL_ROLLBACK_VALIDATION_OK', 'FAIL': 0,
            'script_sha256': file_hash(getSourceFile().getAbsolutePath()),
            'plan_sha256': file_hash(os.path.join(RUN, PLAN_NAME)),
            'prestate_sha256': prestate_hash, 'counts': EXPECTED_COUNTS,
            'post_verified': True, 'semantic_actions_applied': True,
            'transaction_committed': False, 'rollback_forced': rollback_forced,
            'dynamic_counts': DYNAMIC_COUNTS,
        }
        write_json('f15-seg5-full-rollback-validation-%s.json' % EVIDENCE_VERSION, result)
        print('STATUS: OK mode=fullrollback FAIL=0 transaction=rolled_back')
    elif MODE == 'check':
        receipt = read_json('f15-seg5-apply-receipt-%s.json' % EVIDENCE_VERSION)
        require(receipt.get('status') == 'F15_SEG5_APPLIED_POSTCHECK_OK' and
                receipt.get('counts') == EXPECTED_COUNTS and
                receipt.get('script_sha256') == file_hash(getSourceFile().getAbsolutePath()) and
                receipt.get('plan_sha256') == file_hash(os.path.join(RUN, PLAN_NAME)),
                'RECEIPT_CONTRACT')
        reject('RECEIPT')
        verify_post(prestate)
        write_json('f15-seg5-persisted-check-%s.json' % EVIDENCE_VERSION, {
            'status': 'F15_SEG5_PERSISTED_CHECK_OK', 'FAIL': 0,
            'script_sha256': receipt['script_sha256'],
            'plan_sha256': receipt['plan_sha256'], 'counts': EXPECTED_COUNTS,
        })
        print('STATUS: OK mode=check FAIL=0')
    else:
        verify_prestate(prestate, True)
        transaction = currentProgram.startTransaction('F15-Seg-5 approved transaction')
        commit = False
        error = None
        try:
            apply_all()
            verify_post(prestate)
            commit = True
        except Exception as caught:
            error = caught
            write_json('f15-seg5-apply-failure-%s.json' % EVIDENCE_VERSION,
                       failure_payload('APPLY', caught))
            traceback.print_exc()
        finally:
            currentProgram.endTransaction(transaction, commit)
        if not commit:
            raise RuntimeError('F15-Seg-5 transaction rolled back: %s' % unicode(error))
        receipt = {
            'status': 'F15_SEG5_APPLIED_POSTCHECK_OK', 'FAIL': 0,
            'script_sha256': file_hash(getSourceFile().getAbsolutePath()),
            'plan_sha256': file_hash(os.path.join(RUN, PLAN_NAME)),
            'prestate_sha256': prestate_hash, 'counts': EXPECTED_COUNTS,
        }
        write_json('f15-seg5-apply-receipt-%s.json' % EVIDENCE_VERSION, receipt)
        print('STATUS: OK mode=apply FAIL=0 transaction=committed')
