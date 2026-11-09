# -*- coding: ascii -*-
#@runtime Jython
#@category Ygo-ex2006.Refine
# F14-Seg-3 PASS materialization. prestate/dry/check are read-only.

import csv
import hashlib
import json
import os
import re

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.address import AddressSet
from ghidra.program.model.data import ArrayDataType, Undefined4DataType, UnsignedShortDataType
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import RefType, SourceType
from java.math import BigInteger

ARGS = list(getScriptArgs())
MODE = ARGS[0].lower() if ARGS else 'dry'
if MODE not in ('prestate', 'dry', 'apply', 'check'):
    raise RuntimeError('Expected prestate, dry, apply, or check')

ROOT = os.path.abspath(os.path.join(str(getSourceFile().getParentFile()), '..', '..'))
RUN = os.path.join(ROOT, 'output', 'refine-run-20261028-105948')
PLAN_NAME = 'f14-seg3-plan-v3.json'
PRESTATE_NAME = 'f14-seg3-fresh-full-prestate-v4.json'
SOURCE_SNAPSHOT_NAME = 'f14-seg3-source-snapshot-preapply-v5.json'
FREEZE_MANIFEST_NAME = 'f14-seg3-freeze-manifest.json'
MAP_NAME = 'f14-seg3-r4-cfg-map.json'
MACHINE_CONTRACT_NAME = 'f14-seg3-mode-a-machine-contract.json'
FUNCTION_PLAN_NAME = 'f14-seg3-function-plan.json'
DB_BACKUP_MANIFEST_NAME = 'root-f14-seg3-db-backup.json'

INPUT_HASHES = {
    'doc/dev/refine/F14-Seg-3.proposal.md': 'de4aaf39ce3ab7f9540816a331f0df26f253451f99c7fea3455c0f2aa4bca018',
    'doc/dev/refine/F14-Seg-3.review.md': '095e91d5e076d651dc941476aacc6926fde83b168c8c97c9c38f16f75dbfd8a2',
    'doc/dev/refine/F14-Seg-3.slots.tsv': '370def5e0e4bb363827bb8c9f47eadf512a5ee63b70d3150586eb86556fdb20f',
    'doc/dev/refine/F14-Seg-3.plates.tsv': 'a9e41dd029dbb747f9378d17337e8026ed748387b8c6b3802acc8ea35b35bcfd',
    'output/refine-run-20261028-105948/f14-seg3-freeze-manifest.json': '95abbfdd0be71b85449af97518002c052ab92973ac46e404df04a09919e18319',
    'output/refine-run-20261028-105948/f14-seg3-mode-a-machine-contract.json': 'ecd6922ab4690225fc3c09cc1cacb25dc09589bcfc94914eb72e3494a987b989',
    'output/refine-run-20261028-105948/f14-seg3-even-function-equate-contract.json': 'cc60560d717af799e24da92304dd345ecd259b758ada89aa96995d57f3747776',
    'output/refine-run-20261028-105948/f14-seg3-final-export-amendment-audit.json': 'c3a77ed31d7369d237545ba00ebdcec1eaa23420f4941ef02c18f67a01bf916a',
    'output/refine-run-20261028-105948/root-f14-seg3-even-function-amendment-narrow-gate.json': 'ecdce263994afb97418a4f0886040b5604e0e94b4e69e622e00a8dd618291ec6',
    'output/refine-run-20261028-105948/root-f14-seg3-even-function-projection-scope-gate.json': '672d3ef3e15360eeb22656a0f08fd77ff493e863f1fb267e40f465bdf57accf1',
    'output/refine-run-20261028-105948/root-f14-seg3-even-function-equate-prestate.json': '2dd2701bddc804924638e9e3215a60784628726cf55ff81a37fa8f5bdb733a94',
    'output/refine-run-20261028-105948/root-f14-seg3-even-function-equate-prestate.json.db-gate.json': '35e4df505ff9074c300f7049760d7326d412cf124a4dc102bb28a49250f6c4d6',
    'output/refine-run-20261028-105948/f14-seg3-r4-cfg-map.json': '0ef41331aac5d2f562f123d5bf7013dbe94cfeb4a96c178a0d75183f91c5b66e',
    'output/refine-run-20261028-105948/f14-seg3-function-plan.json': '204006f29399e9f8c4b952e190154c5d6431c2cab6069d531c63cd41a81f3502',
    'output/refine-run-20261028-105948/f14-seg3-constant-plan.json': '1930920fa0b40f0a64487dcb9a1935e509acca2206ec6b524eec5bf46e88ca06',
    'output/refine-run-20261028-105948/root-f14-seg3-mode-a-narrow-gate.json': 'c671b8fc340ec22f741cd32557a696596b99f63a58c03c3e083e9de6160f54db',
    'output/refine-run-20261028-105948/root-f14-seg3-r4-static-gate.json': '05b760e67e73dab0cd0f4a838b02e0eb040356b601136775d14a850ba0036a31',
    'output/refine-run-20261028-105948/root-f14-seg2-independent-post-v2.json': 'dfb04dbeea6f14215f287437390eec0dc37f18827bf9e1f9faa1378b9cce1428',
    'output/refine-run-20261028-105948/root-f14-seg3-supplement-prestate.json': 'fcd04b3e0888a6cd414e05390d28292e7a5755eb2a4cae52049fd2feca14309d',
    'output/refine-run-20261028-105948/root-f14-seg3-db-backup.json': '4d903355734789ac26c61358cf723af7849115569d9bf3b269a470a8506acef8',
    'output/refine-run-20261028-105948/root-source-baseline-f14seg3.json': '4bb38f621ef6bd3465dd5346f831a4844e3e374d8ab32ced3ce7e076a072818f',
}
EXPECTED_COUNTS = {
    'EQ_ADD': 57, 'EQ_MATERIALIZE': 65,
    'REF_ADD': 30, 'REF_PRESERVE': 1, 'REF_MATERIALIZE': 25,
    'TABLE_ENTRY_MATERIALIZE': 23, 'TABLE_ENTRY_EQUATE_EVEN_FUNCTION': 5,
    'EOL': 206, 'SOURCE_LABEL': 181,
    'CASE_LABEL': 15, 'CASE_FUNCTION_PRESERVE': 1, 'TABLE_BASE_LABEL': 3,
    'REF_TARGET_MATERIALIZE': 1, 'FUNC_RENAME': 3, 'PLATE_WRITE': 5,
    'R4_CODE_RANGES': 40, 'R4_INITIAL_SEEDS': 24,
    'R4_INSTRUCTIONS': 1411, 'R4_POOL_WORDS': 90,
    'BODY_UPDATE': 4,
}
SEGMENT_START = 0x080aa120
SEGMENT_END = 0x080aba78
SEGMENT_SHA256 = '87ef2e4217d9adf8a3732cb8709060f86a16a327cdca184b420764c9379531d2'
FUNCTION_COUNT = 5214
FINAL_FUNCTION_COUNT = 5214
LP_COUNTER = 0x0201b754
PARTIAL_DATA = 0x080ab278

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

def path_in_root(relative):
    return os.path.join(ROOT, *relative.replace('\\', '/').split('/'))

def run_path(name):
    return os.path.join(RUN, name)

def read_json_path(path):
    with open(path, 'rb') as stream:
        return json.load(stream)

def read_json(name):
    return read_json_path(run_path(name))

def write_json(name, value):
    with open(run_path(name), 'w') as stream:
        stream.write(json.dumps(value, ensure_ascii=True, sort_keys=True, indent=2) + '\n')

def file_hash(path):
    with open(path, 'rb') as stream:
        return hashlib.sha256(stream.read()).hexdigest()

def read_tsv(relative):
    with open(path_in_root(relative), 'rb') as stream:
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

REF_CORE_KEYS = frozenset(('from', 'to', 'operand', 'type', 'source', 'primary'))

def is_reference_dict(value):
    return isinstance(value, dict) and REF_CORE_KEYS.issubset(set(value.keys()))

def canonical(value):
    if isinstance(value, dict):
        return dict((key, canonical(item)) for key, item in value.items())
    if isinstance(value, list):
        items = [canonical(item) for item in value]
        # Ghidra may enumerate reference collections in a different order after
        # materialization.  Only those unordered CORE6 reference dictionaries
        # are normalized.  Ordered vectors such as [source, target] flow edges
        # and [lo, hi] body ranges retain their direction and boundaries.
        if items and all(is_reference_dict(item) for item in items):
            return sorted(items, key=lambda item: json.dumps(item, sort_keys=True))
        return items
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
        write_json('f14-seg3-%s-failures-v2.json' % MODE,
                   {'status': 'FAIL', 'phase': phase, 'FAIL': len(FAILS),
                    'failures': FAILS})
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
        'id': long(symbol.getID()), 'name': unicode(symbol.getName()),
        'qualified_name': unicode(symbol.getName(True)),
        'type': str(symbol.getSymbolType()), 'source': str(symbol.getSource()),
        'primary': bool(symbol.isPrimary()),
        'namespace_name': None if parent is None else unicode(parent.getName()),
        'namespace_qualified': None if parent is None else unicode(parent.getName(True)),
        'namespace_id': None if parent is None else safe_value(lambda: long(parent.getID())),
        'global': parent == global_ns,
    }

def ref_row(ref):
    primary = symbols.getPrimarySymbol(ref.getToAddress())
    return {
        'from': str(ref.getFromAddress()), 'to': str(ref.getToAddress()),
        'operand': int(ref.getOperandIndex()), 'type': str(ref.getReferenceType()),
        'source': str(ref.getSource()), 'primary': bool(ref.isPrimary()),
        'target_primary_id': None if primary is None else long(primary.getID()),
        'target_primary_name': None if primary is None else unicode(primary.getName(True)),
        'target_primary_type': None if primary is None else str(primary.getSymbolType()),
        'target_primary_source': None if primary is None else str(primary.getSource()),
    }

def ref_core(row):
    return dict((key, row[key]) for key in
                ('from', 'to', 'operand', 'type', 'source', 'primary'))

def tsv_ref_row(row):
    return dict((key, row.get(key)) for key in
                ('from', 'to', 'operand', 'type', 'source', 'primary',
                 'target_primary_id', 'target_primary_name'))

def data_row(data):
    if data is None:
        return None
    return {
        'address': str(data.getAddress()), 'min': str(data.getMinAddress()),
        'max': str(data.getMaxAddress()), 'length': int(data.getLength()),
        'type': unicode(data.getDataType().getPathName()),
        'defined': bool(safe_value(lambda: data.isDefined(), False)),
    }

def address_state(value):
    addr = toAddr(value)
    primary = symbols.getPrimarySymbol(addr)
    symbol_list = [symbol_row(item) for item in symbols.getSymbols(addr)]
    raw = bytes_hex(value, 4)
    instruction = listing.getInstructionAt(addr)
    fn = functions.getFunctionAt(addr)
    owner = functions.getFunctionContaining(addr)
    return {
        'address': '0x%08x' % value, 'bytes': raw,
        'rom_word': None if raw is None else long(memory.getInt(addr) & 0xffffffff),
        'symbols': symbol_list, 'symbol_count': len(symbol_list),
        'primary_symbol': None if primary is None else symbol_row(primary),
        'data_at': data_row(listing.getDataAt(addr)),
        'defined_data_at': data_row(listing.getDefinedDataAt(addr)),
        'data_containing': data_row(listing.getDataContaining(addr)),
        'instruction': None if instruction is None else unicode(instruction.toString()),
        'function': None if fn is None else unicode(fn.getName()),
        'function_containing': None if owner is None else {
            'entry': str(owner.getEntryPoint()),
            'id': long(owner.getSymbol().getID()),
            'name': unicode(owner.getName())},
        'references_from': [ref_row(ref) for ref in references.getReferencesFrom(addr)],
        'references_to': [ref_row(ref) for ref in references.getReferencesTo(addr)],
        'equates': sorted([{'name': unicode(eq.getName()),
                            'value': long(eq.getValue()) & 0xffffffff}
                           for eq in equates.getEquates(addr)],
                          key=lambda row: (row['name'], row['value'])),
        'eol': listing.getComment(CodeUnit.EOL_COMMENT, addr),
        'plate': listing.getComment(CodeUnit.PLATE_COMMENT, addr),
    }

def equate_global_row(name):
    eq = equates.getEquate(name)
    if eq is None:
        return None
    return {
        'name': unicode(eq.getName()),
        'value': long(eq.getValue()) & 0xffffffff,
        'references': sorted([
            {'address': str(ref.getAddress()), 'operand': int(ref.getOpIndex())}
            for ref in eq.getReferences()],
            key=lambda row: (row['address'], row['operand'])),
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
    raw = []
    body_refs = []
    eols = []
    iterator = fn.getBody().getAddresses(True)
    while iterator.hasNext():
        item = iterator.next()
        raw.append(chr(memory.getByte(item) & 255))
        for ref in references.getReferencesFrom(item):
            body_refs.append(ref_row(ref))
        text = listing.getComment(CodeUnit.EOL_COMMENT, item)
        if text is not None:
            eols.append({'address': '0x%08x' % long(item.getOffset()),
                         'text': unicode(text)})
    thunk = safe_value(lambda: fn.getThunkedFunction(False))
    namespace = symbol.getParentNamespace()
    return {
        'entry': '0x%08x' % value, 'name': unicode(fn.getName()),
        'symbol': symbol_row(symbol),
        'namespace': {
            'name': None if namespace is None else unicode(namespace.getName()),
            'qualified_name': None if namespace is None else unicode(namespace.getName(True)),
            'id': None if namespace is None else safe_value(lambda: long(namespace.getID())),
            'global': namespace == global_ns,
        },
        'body': unicode(fn.getBody().toString()), 'body_ranges': body_ranges(fn),
        'body_size': int(fn.getBody().getNumAddresses()),
        'body_sha256': hashlib.sha256(''.join(raw)).hexdigest(),
        'body_bytes': ''.join('%02x' % ord(item) for item in raw),
        'body_references': body_refs, 'eol_comments': eols,
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
            'id': long(thunk.getSymbol().getID())},
        'stack_purge_size': safe_value(lambda: int(fn.getStackPurgeSize())),
        'return': variable_row(fn.getReturn()), 'parameters': params,
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
        data = listing.getDataAt(addr)
        defined = listing.getDefinedDataAt(addr)
        owner = functions.getFunctionContaining(addr)
        tmode = None
        if tmode_register is not None:
            raw_tmode = safe_value(lambda: context.getValue(tmode_register, addr, False))
            if raw_tmode is not None:
                tmode = int(raw_tmode)
        rows.append({
            'address': '0x%08x' % value, 'byte': memory.getByte(addr) & 255,
            'unit': None if unit is None else {
                'min': str(unit.getMinAddress()), 'max': str(unit.getMaxAddress()),
                'length': int(unit.getLength()),
                'class': unicode(unit.getClass().getSimpleName())},
            'instruction_at': None if instruction is None else unicode(instruction.toString()),
            'data_at': data_row(data), 'defined_data_at': data_row(defined),
            'function_owner': None if owner is None else {
                'entry': str(owner.getEntryPoint()),
                'id': long(owner.getSymbol().getID()), 'name': unicode(owner.getName())},
            'tmode': tmode,
        })
    return rows

SLOT_ROWS = read_tsv('doc/dev/refine/F14-Seg-3.slots.tsv')
PLATE_ROWS = read_tsv('doc/dev/refine/F14-Seg-3.plates.tsv')
R4_MAP = read_json(MAP_NAME)
MACHINE_CONTRACT = read_json(MACHINE_CONTRACT_NAME)
PROJECTION_CONTRACT = read_json('f14-seg3-even-function-equate-contract.json')
FUNCTION_PLAN = read_json(FUNCTION_PLAN_NAME)
MODULE_BASELINE = read_json('root-f14-seg2-independent-post-v2.json')
SUPPLEMENT_BASELINE = read_json('root-f14-seg3-supplement-prestate.json')
OBSERVER_FUNCTIONS = sorted(set(
    int(row['entry'], 16)
    for source in (MODULE_BASELINE, SUPPLEMENT_BASELINE)
    for row in source['functions'] if row is not None))
SLOTS = dict((int(row['address'], 16), row) for row in SLOT_ROWS)
PLATES = dict((int(row['entry'], 16), row) for row in PLATE_ROWS)
RENAMES = dict((value, row) for value, row in PLATES.items()
               if row['current_name'] != row['final_name'])
PLATE_WRITES = dict(PLATES)
FUNCTIONS = sorted(PLATES)
BODY_MUTATIONS = dict((value, row) for value, row in PLATES.items()
                      if row['body_ranges_json'] != row['final_body_ranges_json'])
TABLE_ROWS = [row for row in SLOT_ROWS if row['action'].startswith('TABLE_ENTRY_')]
PROJECTION_ROWS = [row for row in SLOT_ROWS
                   if row['action'] == 'TABLE_ENTRY_EQUATE_EVEN_FUNCTION']
PROJECTION_EQ_NAME = PROJECTION_CONTRACT['name']
PROJECTION_EQ_VALUE = int(PROJECTION_CONTRACT['value'], 16)
TABLE_SOURCES = sorted(int(row['address'], 16) for row in TABLE_ROWS)
CASE_NAMES = {}
for row in TABLE_ROWS:
    target = int(row['original_value'], 16)
    name = row['target_final_label']
    if target in CASE_NAMES and CASE_NAMES[target] != name:
        raise RuntimeError('Conflicting case label at %08x' % target)
    CASE_NAMES[target] = name
TABLE_BASES = dict((int(row['address'], 16), row['final_slot_label'])
                   for row in TABLE_ROWS if row['final_slot_label'] != 'none')
REF_ROWS = [row for row in SLOT_ROWS if row['action'].startswith('REF_')]
REF_TARGETS = sorted(set(int(row['original_value'], 16) for row in REF_ROWS))
RAM_TARGETS = sorted(value for value in REF_TARGETS if value < 0x08000000)
REF_TARGET_NAMES = {}
for row in REF_ROWS:
    target = int(row['original_value'], 16)
    name = row['target_final_label']
    if name != 'none':
        if target in REF_TARGET_NAMES and REF_TARGET_NAMES[target] != name:
            raise RuntimeError('Conflicting REF target label at %08x' % target)
        REF_TARGET_NAMES[target] = name
ODD_TARGETS = sorted(set(int(row['original_value'], 16) for row in SLOT_ROWS
                         if row['action'].startswith('EQ_') and
                         0x08000000 <= int(row['original_value'], 16) < 0x0a000000 and
                         int(row['original_value'], 16) & 1))
ODD_FUNCTIONS = sorted(set(value - 1 for value in ODD_TARGETS))
CODE_RANGES = []
INITIAL_SEEDS = []
POOL_ADDRESSES = []
PADDING_RANGES = []
INSTRUCTION_ROWS = []
FLOW_ROWS = []
FLOW_REF_ROWS = []
PC_READ_ROWS = []
FALLTHROUGH_ROWS = []
for cluster in R4_MAP['clusters']:
    INITIAL_SEEDS.extend(int(item, 16) for item in cluster['seeds'])
    CODE_RANGES.extend((int(item[0], 16), int(item[1], 16))
                       for item in cluster['code_ranges'])
    POOL_ADDRESSES.extend(int(row['address'], 16) for row in cluster['pool_words'])
    for row in cluster['padding_or_unclassified']:
        PADDING_RANGES.append((int(row['range'][0], 16), int(row['range'][1], 16)))
    for row in cluster['instructions']:
        INSTRUCTION_ROWS.append(row)
        for target in row['direct_flow_targets']:
            kind = 'CALL' if target in row['call_targets'] else 'JUMP'
            FLOW_ROWS.append({'from': row['address'], 'to': target, 'kind': kind})
            FLOW_REF_ROWS.append({
                'from': row['address'][2:], 'to': target[2:], 'operand': 0,
                'type': ('UNCONDITIONAL_CALL' if kind == 'CALL' else
                         ('CONDITIONAL_JUMP' if row['kind'] == 'conditional_branch'
                          else 'UNCONDITIONAL_JUMP')),
                'source': 'DEFAULT', 'primary': True})
        for target in row['pc_read_targets']:
            PC_READ_ROWS.append({'from': row['address'], 'to': target})
        if row['fallthrough'] is not None:
            FALLTHROUGH_ROWS.append({'from': row['address'], 'to': row['fallthrough']})
INSTRUCTION_ADDRESSES = sorted(int(row['address'], 16) for row in INSTRUCTION_ROWS)
POOL_ADDRESSES = sorted(POOL_ADDRESSES)
CODE_RANGES = sorted(CODE_RANGES)
PADDING_RANGES = sorted(PADDING_RANGES)
INITIAL_SEEDS = sorted(set(INITIAL_SEEDS))
DIRECT_CALLEE_TARGETS = sorted(set(int(row['to'], 16) for row in FLOW_ROWS
                                   if row['kind'] == 'CALL'))
FINAL_BODY_RANGES = dict((value, [(int(lo, 16), int(hi, 16))
                                  for lo, hi in json.loads(row['final_body_ranges_json'])])
                         for value, row in PLATES.items())
HOST_BY_INSTRUCTION = {}
for value in INSTRUCTION_ADDRESSES:
    owners = [entry for entry, ranges in FINAL_BODY_RANGES.items()
              if any(lo <= value < hi for lo, hi in ranges)]
    if len(owners) != 1:
        raise RuntimeError('R4 owner contract at %08x: %r' % (value, owners))
    HOST_BY_INSTRUCTION[value] = owners[0]

def freeze_manifest_path(relative):
    return path_in_root(relative)

def verify_inputs():
    for relative, digest in sorted(INPUT_HASHES.items()):
        same('INPUT_HASH_' + relative, file_hash(path_in_root(relative)), digest)
    manifest = read_json(FREEZE_MANIFEST_NAME)
    basis = manifest.get('review_basis', {})
    require(isinstance(basis, dict) and len(basis) == 25,
            'FREEZE_MANIFEST_REVIEW_BASIS_COUNT')
    for relative, digest in sorted(basis.items()):
        same('FREEZE_MANIFEST_HASH_' + relative,
             file_hash(path_in_root(relative)), digest)
    prior = manifest.get('prior_review', {})
    require(prior.get('immutable_archive') is True and
            file_hash(path_in_root(prior['path'])) == prior['sha256'],
            'IMMUTABLE_PRIOR_REVIEW')
    draft = manifest.get('prior_mode_a_draft1', {})
    require(draft.get('immutable_archive') is True and
            file_hash(path_in_root(draft['path'])) == draft['sha256'],
            'IMMUTABLE_MODE_A_DRAFT1')
    require(len(SLOTS) == 206 and len(SLOT_ROWS) == 206 and
            len(PLATES) == 5 and len(FUNCTIONS) == 5 and
            len(RENAMES) == 3 and len(PLATE_WRITES) == 5 and
            len(BODY_MUTATIONS) == 4,
            'PRIMARY_INPUT_COUNTS')
    require(len(OBSERVER_FUNCTIONS) == 190, 'OBSERVER_FUNCTION_COUNT')
    action_counts = {}
    for row in SLOT_ROWS:
        action_counts[row['action']] = action_counts.get(row['action'], 0) + 1
    same('SLOT_ACTION_COUNTS', action_counts,
         {'EQ_ADD': 57, 'EQ_MATERIALIZE': 65,
          'REF_ADD': 30, 'REF_PRESERVE': 1, 'REF_MATERIALIZE': 25,
          'TABLE_ENTRY_MATERIALIZE': 23,
          'TABLE_ENTRY_EQUATE_EVEN_FUNCTION': 5})
    require(len(TABLE_SOURCES) == 28 and len(CASE_NAMES) == 16 and
            len(TABLE_BASES) == 3 and len(REF_TARGETS) == 12 and
            len(RAM_TARGETS) == 9 and len(ODD_TARGETS) == 0,
            'REFERENCE_SCOPE_COUNTS')
    require(len(CODE_RANGES) == 40 and len(INITIAL_SEEDS) == 24 and
            len(INSTRUCTION_ADDRESSES) == 1411 and len(POOL_ADDRESSES) == 90 and
            len(PADDING_RANGES) == 18 and len(FLOW_ROWS) == 248 and
            sum(row['kind'] == 'CALL' for row in FLOW_ROWS) == 58 and
            len(PC_READ_ROWS) == 95 and len(FALLTHROUGH_ROWS) == 1338 and
            sum(hi - lo for lo, hi in CODE_RANGES) == 2938 and
            sum(hi - lo for lo, hi in PADDING_RANGES) == 36,
            'R4_SCOPE_COUNTS')
    require(all(value in INSTRUCTION_ADDRESSES for value in INITIAL_SEEDS),
            'R4_INITIAL_SEED_SCOPE')
    counts = R4_MAP['counts']
    require(counts['instructions'] == 1411 and counts['code_bytes'] == 2938 and
            counts['pool_words'] == 90 and counts['padding_halfwords'] == 18 and
            counts['direct_flows'] == 248 and counts['calls'] == 58 and
            counts['pc_reads'] == 95 and counts['fallthroughs'] == 1338,
            'R4_MAP_COUNTS')
    contract = MACHINE_CONTRACT['action_counts']
    require(contract['slot_total'] == 206 and contract['EQ_total'] == 122 and
            contract['REF_total'] == 56 and contract['TABLE_total'] == 28,
            'MACHINE_ACTION_COUNTS')
    require(len(PROJECTION_ROWS) == 5 and
            sorted(int(row['address'], 16) for row in PROJECTION_ROWS) ==
            [0x080aa7c0, 0x080aa7c4, 0x080aa7c8, 0x080aa7cc, 0x080aa7d0] and
            all(int(row['original_value'], 16) == 0x080aaf54 and
                row['target_final_label'] == PROJECTION_EQ_NAME and
                row['equates_json'] == '[]'
                for row in PROJECTION_ROWS),
            'PROJECTION_ROWS')
    require(PROJECTION_CONTRACT['operation_scope']['scope'] == 'projection_only' and
            PROJECTION_CONTRACT['operation_scope']['memory_incoming_reference_delta'] == 0 and
            PROJECTION_CONTRACT['operation_scope']['source_data_reference_delta'] == 0 and
            PROJECTION_CONTRACT['operation_scope']['target_function_mutations'] == [] and
            PROJECTION_EQ_NAME == 'exit_equip_phase_oob_epilogue' and
            PROJECTION_EQ_VALUE == 0x080aaf54 and
            PROJECTION_CONTRACT['before'] == {
                'exists': False, 'value': None, 'references': []},
            'PROJECTION_CONTRACT')
    preserve = MACHINE_CONTRACT['ref_preserve']
    require(preserve['source'] == '0x080ab6d0' and
            preserve['target'] == '0x0201c4e0' and
            preserve['target_symbol_id'] == 15545 and
            preserve['target_name'] == 'gP1LifePoints',
            'REF_PRESERVE_MACHINE_CONTRACT')
    counter = MACHINE_CONTRACT['lp_bar_display_counter']
    require(counter['address'] == '0x0201b754' and
            counter['exact_target_label'] == 'gLpBarDisplayCounter' and
            counter['definition_expression'] ==
            'gDuelPhaseFlags + LP_BAR_DISPLAY_CTR_OFF' and
            counter['native_slot_expression'] == 'gLpBarDisplayCounter' and
            counter['same_address_aliases'] == 0,
            'LP_COUNTER_MACHINE_CONTRACT')
    source_names = [row['final_slot_label'] for row in SLOT_ROWS
                    if row['final_slot_label'] != 'none']
    require(len(source_names) == 181 and len(set(source_names)) == 181,
            'SOURCE_LABEL_COUNT_UNIQUE')
    equated_slots = 0
    equate_values = {}
    for value, row in sorted(SLOTS.items()):
        if row['final_slot_label'] != 'none':
            require(re.match(r'^[a-z][a-z0-9_]+$', row['final_slot_label']) is not None,
                    'SOURCE_LABEL_SYNTAX_%08x' % value)
            collisions = [item for item in symbols.getGlobalSymbols(row['final_slot_label'])
                          if item.getAddress() != toAddr(value)]
            require(not collisions, 'SOURCE_LABEL_COLLISION_%08x' % value)
        require(row['new_eol_ascii'] != 'none' and
                all(ord(char) < 128 for char in row['new_eol_ascii']),
                'EOL_ASCII_%08x' % value)
        after = json.loads(row['after_equates_json'])
        if row['action'] in ('EQ_ADD', 'EQ_MATERIALIZE'):
            expected_after = [{'name': row['const_or_target'],
                               'value': row['original_value'], 'operand': 0}]
        elif row['action'] == 'TABLE_ENTRY_EQUATE_EVEN_FUNCTION':
            expected_after = [{'name': PROJECTION_EQ_NAME,
                               'value': '0x080aaf54', 'operand': 0}]
        else:
            expected_after = []
        same('AFTER_EQUATES_INPUT_%08x' % value, after, expected_after)
        if after:
            equated_slots += 1
            name = after[0]['name']
            scalar = int(after[0]['value'], 16)
            require(name not in equate_values or equate_values[name] == scalar,
                    'EQUATE_NAME_VALUE_CONFLICT_' + name)
            equate_values[name] = scalar
    require(equated_slots == 127 and len(equate_values) == 91,
            'AFTER_EQUATE_COUNTS')
    for value, name in sorted(CASE_NAMES.items()):
        require(re.match(r'^[a-z][a-z0-9_]+$', name) is not None,
                'CASE_LABEL_SYNTAX_%08x' % value)
        collisions = [item for item in symbols.getGlobalSymbols(name)
                      if item.getAddress() != toAddr(value)]
        require(not collisions, 'CASE_LABEL_COLLISION_%08x' % value)
    for value, name in sorted(REF_TARGET_NAMES.items()):
        require(re.match(r'^[A-Za-z][A-Za-z0-9_]+$', name) is not None,
                'REF_TARGET_LABEL_SYNTAX_%08x' % value)
        collisions = [item for item in symbols.getGlobalSymbols(name)
                      if item.getAddress() != toAddr(value)]
        require(not collisions, 'REF_TARGET_LABEL_COLLISION_%08x' % value)
    for value, row in sorted(PLATE_WRITES.items()):
        text = row['new_plate']
        require(all(ord(char) < 128 for char in text) and len(text) <= 500 and
                len(text) == int(row['new_plate_chars']),
                'PLATE_ASCII_%08x' % value)
    for value, row in sorted(RENAMES.items()):
        collisions = [item for item in symbols.getGlobalSymbols(row['final_name'])
                      if item.getAddress() != toAddr(value)]
        require(not collisions, 'FUNCTION_NAME_COLLISION_%08x' % value)
    target_fn = functions.getFunctionAt(toAddr(PROJECTION_EQ_VALUE))
    target_symbols = list(symbols.getSymbols(toAddr(PROJECTION_EQ_VALUE)))
    require(target_fn is not None and long(target_fn.getSymbol().getID()) == 16957 and
            unicode(target_fn.getName()) == PROJECTION_EQ_NAME and
            str(target_fn.getSymbol().getSource()) == 'USER_DEFINED' and
            str(target_fn.getSymbol().getSymbolType()) == 'Function' and
            len(target_symbols) == 1,
            'PROJECTION_TARGET_FUNCTION_STATIC')
    global_eq = equate_global_row(PROJECTION_EQ_NAME)
    if MODE == 'check':
        same('PROJECTION_EQ_POST_INPUT', global_eq, {
            'name': PROJECTION_EQ_NAME, 'value': PROJECTION_EQ_VALUE,
            'references': [{'address': '%08x' % value, 'operand': 0}
                           for value in [0x080aa7c0, 0x080aa7c4, 0x080aa7c8,
                                         0x080aa7cc, 0x080aa7d0]]})
    else:
        require(global_eq is None, 'PROJECTION_EQ_ABSENT_PRE')

def capture():
    target_addresses = sorted(set(REF_TARGETS + list(CASE_NAMES) + list(TABLE_BASES) +
                                  [PARTIAL_DATA]))
    direct_functions = sorted(set(value for value in DIRECT_CALLEE_TARGETS
                                  if functions.getFunctionAt(toAddr(value)) is not None))
    equate_names = sorted(set(row['const_or_target'] for row in SLOT_ROWS
                              if row['action'].startswith('EQ_')))
    equate_names = sorted(set(equate_names + [PROJECTION_EQ_NAME]))
    return {
        'status': 'F14_SEG3_FRESH_FULL_PRESTATE',
        'program_name': unicode(currentProgram.getName()),
        'function_count': int(functions.getFunctionCount()),
        'segment': {'start': '0x%08x' % SEGMENT_START,
                    'end': '0x%08x' % SEGMENT_END,
                    'size': SEGMENT_END - SEGMENT_START,
                    'sha256': raw_hash(SEGMENT_START, SEGMENT_END)},
        'functions': [function_row(value) for value in FUNCTIONS],
        'observer_functions': [function_row(value) for value in OBSERVER_FUNCTIONS],
        'slots': [address_state(value) for value in sorted(SLOTS)],
        'targets': [address_state(value) for value in target_addresses],
        'table_sources': [address_state(value) for value in TABLE_SOURCES],
        'case_targets': [address_state(value) for value in sorted(CASE_NAMES)],
        'table_bases': [address_state(value) for value in sorted(TABLE_BASES)],
        'ram_targets': [address_state(value) for value in RAM_TARGETS],
        'odd_targets': [address_state(value) for value in ODD_TARGETS],
        'odd_even_functions': [function_row(value) for value in ODD_FUNCTIONS],
        'direct_callee_targets': [address_state(value) for value in DIRECT_CALLEE_TARGETS],
        'direct_callee_functions': [function_row(value) for value in direct_functions],
        'equate_globals': [equate_global_row(name) for name in equate_names],
        'partial_data': address_state(PARTIAL_DATA),
        'segment_byte_units': segment_byte_units(),
    }

def bool_field(value):
    return value.lower() == 'true'

def verify_function_tsv(value, row, state):
    require(state is not None and state['name'] == row['current_name'] and
            state['symbol']['id'] == long(row['function_id']) and
            state['symbol']['source'] == row['function_source'] and
            state['symbol']['type'] == row['symbol_type'] and
            state['namespace']['name'] == row['namespace'] and
            state['namespace']['id'] == long(row['namespace_id']) and
            state['body'] == row['body'] and
            state['body_ranges'] == json.loads(row['body_ranges_json']) and
            state['body_size'] == int(row['body_size']) and
            state['body_sha256'] == row['body_sha256'] and
            state['calling_convention'] == row['calling_convention'] and
            state['signature_source'] == row['signature_source'] and
            state['prototype'] == row['prototype'] and
            state['custom_variable_storage'] == bool_field(row['custom_variable_storage']) and
            state['varargs'] == bool_field(row['varargs']) and
            state['inline'] == bool_field(row['inline']) and
            state['no_return'] == bool_field(row['no_return']) and
            state['external'] == bool_field(row['external']) and
            state['thunk'] == bool_field(row['thunk']) and
            state['thunk_target'] == (None if row['thunk_target'] == 'none' else
                                      json.loads(row['thunk_target'])) and
            state['stack_purge_size'] == int(row['stack_purge_size']),
            'FUNCTION_STATIC_%08x' % value)
    require(state['return'] == json.loads(row['return_json']) and
            state['parameters'] == json.loads(row['parameters_json']) and
            state['eol_comments'] == json.loads(row['eol_json']) and
            state['incoming'] == json.loads(row['incoming_json']),
            'FUNCTION_FULL_METADATA_%08x' % value)
    plate = state['plate']
    require(plate is not None and len(plate) == int(row['old_plate_chars']) and
            hashlib.sha256(plate.encode('utf-8')).hexdigest() == row['old_plate_sha256'],
            'FUNCTION_PLATE_PRE_%08x' % value)

def data_contract_from_tsv(state, row, value):
    old_type = row['old_data_type']
    if old_type == 'none':
        require(state['defined_data_at'] is None and state['instruction'] is None and
                (state['data_at'] is None or
                 (state['data_at']['type'] == '/undefined' and
                  state['data_at']['length'] == 1 and
                  state['data_at']['defined'] is False)),
                'SLOT_DATA_NONE_%08x' % value)
    else:
        require(state['data_at'] is not None and
                state['data_at']['type'] == old_type and
                state['data_at']['length'] == 4,
                'SLOT_DATA_TYPE_%08x' % value)

def verify_prestate(pre):
    same('FRESH_PRESTATE_EXACT', capture(), pre)
    require(pre['function_count'] == FUNCTION_COUNT, 'FUNCTION_COUNT_PRE')
    require(pre['segment']['sha256'] == SEGMENT_SHA256 and
            len(pre['segment_byte_units']) == SEGMENT_END - SEGMENT_START,
            'SEGMENT_PRE')
    pre_functions = dict(zip(FUNCTIONS, pre['functions']))
    for value, row in sorted(PLATES.items()):
        verify_function_tsv(value, row, pre_functions[value])
    pre_slots = dict((int(row['address'], 16), row) for row in pre['slots'])
    for value, row in sorted(SLOTS.items()):
        state = pre_slots[value]
        require(state['bytes'] == row['old_bytes'] and
                state['rom_word'] == int(row['original_value'], 16) and
                state['symbols'] == json.loads(row['old_symbols_json']) and
                state['primary_symbol'] == (None if row['old_primary_json'] == 'null'
                                             else json.loads(row['old_primary_json'])) and
                state['references_from'] == json.loads(row['refs_from_json']) and
                state['references_to'] == json.loads(row['refs_to_json']) and
                state['equates'] == json.loads(row['equates_json']) and
                state['eol'] == (None if row['old_eol_json'] == 'null'
                                 else json.loads(row['old_eol_json'])),
                'SLOT_PRE_%08x' % value)
        data_contract_from_tsv(state, row, value)
    preserve = pre_slots[0x080ab6d0]
    same('REF_PRESERVE_PRE_CORE6',
         [ref_core(item) for item in preserve['references_from']],
         [{'from': '080ab6d0', 'to': '0201c4e0', 'operand': 0,
           'type': 'DATA', 'source': 'USER_DEFINED', 'primary': True}])
    require(preserve['references_from'][0]['target_primary_id'] == 15545 and
            preserve['references_from'][0]['target_primary_name'] == 'gP1LifePoints',
            'REF_PRESERVE_PRE_TARGET')
    counter = dict((int(row['address'], 16), row) for row in pre['targets'])[LP_COUNTER]
    require(counter['primary_symbol'] is not None and
            counter['primary_symbol']['name'] == 'DAT_0201b754' and
            counter['primary_symbol']['source'] == 'DEFAULT',
            'LP_COUNTER_PRE_DEFAULT')
    equate_globals = dict((name, item) for name, item in zip(
        sorted(set(row['const_or_target'] for row in SLOT_ROWS
                   if row['action'].startswith('EQ_')) | set([PROJECTION_EQ_NAME])),
        pre['equate_globals']))
    require(equate_globals[PROJECTION_EQ_NAME] is None,
            'PROJECTION_EQ_PRE_ABSENT')
    partial = pre['partial_data']
    require(partial['bytes'] == 'd0e40102' and partial['rom_word'] == 0x0201e4d0 and
            partial['defined_data_at'] is not None and
            partial['defined_data_at']['length'] == 4 and
            partial['defined_data_at']['type'] == '/dword' and
            partial['function_containing'] is not None and
            partial['function_containing']['entry'] == '080ab200',
            'PARTIAL_DATA_PRE')
    for row in [item for cluster in R4_MAP['clusters']
                for item in cluster['instructions']]:
        value = int(row['address'], 16)
        require(bytes_hex(value, int(row['length'])) == row['raw_bytes'] and
                listing.getInstructionAt(toAddr(value)) is None,
                'R4_INSTRUCTION_PRE_%08x' % value)
    for row in [item for cluster in R4_MAP['clusters']
                for item in cluster['pool_words']]:
        value = int(row['address'], 16)
        require(bytes_hex(value, 4) == row['raw_bytes'] and
                listing.getDefinedDataAt(toAddr(value)) is None and
                listing.getInstructionAt(toAddr(value)) is None,
                'R4_POOL_PRE_%08x' % value)
    require(len(pre['observer_functions']) == 190 and
            all(item is not None for item in pre['observer_functions']),
            'OBSERVER_FUNCTIONS_PRE')

def verify_plan(plan, prestate_hash):
    require(plan.get('status') == 'F14_SEG3_PLAN_FROZEN', 'PLAN_STATUS')
    same('PLAN_INPUT_HASHES', plan.get('input_hashes'), INPUT_HASHES)
    same('PLAN_COUNTS', plan.get('counts'), EXPECTED_COUNTS)
    require(plan.get('script_sha256') == file_hash(getSourceFile().getAbsolutePath()),
            'PLAN_SCRIPT_HASH')
    require(plan.get('prestate_sha256') == prestate_hash, 'PLAN_PRESTATE_HASH')
    require(plan.get('source_snapshot_manifest') == SOURCE_SNAPSHOT_NAME and
            plan.get('source_snapshot_manifest_sha256') ==
            file_hash(run_path(SOURCE_SNAPSHOT_NAME)),
            'PLAN_SOURCE_SNAPSHOT_HASH')
    require(plan.get('freeze_manifest_sha256') ==
            file_hash(run_path(FREEZE_MANIFEST_NAME)) and
            plan.get('db_backup_manifest_sha256') ==
            file_hash(run_path(DB_BACKUP_MANIFEST_NAME)),
            'PLAN_MANIFEST_HASHES')
    require(plan.get('range') == [SEGMENT_START, SEGMENT_END] and
            plan.get('function_addresses') == FUNCTIONS and
            plan.get('observer_function_addresses') == OBSERVER_FUNCTIONS and
            plan.get('slot_addresses') == sorted(SLOTS) and
            plan.get('table_sources') == TABLE_SOURCES and
            plan.get('case_targets') == sorted(CASE_NAMES) and
            plan.get('table_bases') == sorted(TABLE_BASES) and
            plan.get('ref_targets') == REF_TARGETS and
            plan.get('odd_targets') == ODD_TARGETS,
            'PLAN_SCOPE')
    r4 = plan.get('r4', {})
    require(r4.get('code_ranges') == [[lo, hi] for lo, hi in CODE_RANGES] and
            r4.get('pool_addresses') == POOL_ADDRESSES and
            r4.get('padding_ranges') == [[lo, hi] for lo, hi in PADDING_RANGES] and
            r4.get('initial_seeds') == INITIAL_SEEDS and
            r4.get('missing_seed_algorithm') ==
            'iterate_sorted_expected_starts_missing_after_initial_seeds' and
            r4.get('instructions') == 1411 and r4.get('flows') == 248 and
            r4.get('calls') == 58 and r4.get('pc_reads') == 95 and
            r4.get('fallthroughs') == 1338,
            'PLAN_R4_SCOPE')
    require(plan.get('body_mutations') == sorted(BODY_MUTATIONS) and
            plan.get('partial_data_owner_release') == [PARTIAL_DATA, PARTIAL_DATA + 2] and
            plan.get('new_function_count') == 0 and
            plan.get('carve_count') == 0,
            'PLAN_BODY_SCOPE')
    require(plan.get('projection_equate') == {
                'name': PROJECTION_EQ_NAME,
                'value': PROJECTION_EQ_VALUE,
                'sources': [0x080aa7c0, 0x080aa7c4, 0x080aa7c8,
                            0x080aa7cc, 0x080aa7d0],
                'operand': 0, 'operation_scope': 'projection_only',
                'memory_incoming_reference_delta': 0,
                'source_data_reference_delta': 0,
                'target_function_id': 16957,
                'target_function_type': 'Function',
                'target_function_source': 'USER_DEFINED',
                'target_symbol_aliases_added': 0,
            }, 'PLAN_PROJECTION_EQUATE')
    sync = plan.get('sync_contract', {})
    require(sync.get('new_constants_globals') == 15 and
            sync.get('naming_proposals_name_cells') == 3 and
            sync.get('naming_proposals_new_rows') == 0 and
            sync.get('inventory_function_count') == 5214 and
            sync.get('inventory_named_count') == 5124 and
            sync.get('inventory_auto_count') == 90 and
            sync.get('inventory_name_changes') == sorted(RENAMES) and
            sync.get('inventory_length_changes') == [
                {'entry': 0x080aa120, 'before': 68, 'after': 1392},
                {'entry': 0x080aa77c, 'before': 46, 'after': 1196},
                {'entry': 0x080aaf64, 'before': 104, 'after': 568},
                {'entry': 0x080ab200, 'before': 2426, 'after': 2424}] and
            sync.get('inventory_paths') == [
                'temp/ghidra-functions.csv',
                'temp/ghidra-functions-renamed.txt',
                'temp/ghidra-functions-auto.txt',
                'temp/ghidra-functions-summary.md'] and
            sync.get('legacy_inventory_unchanged') is True and
            sync.get('no_carve') is True and sync.get('no_alias_write') is True,
            'PLAN_SYNC_CONTRACT')

def ensure_single_global_label(value, name):
    addr = toAddr(value)
    existing = list(symbols.getSymbols(addr))
    primary = symbols.getPrimarySymbol(addr)
    if primary is None:
        if existing:
            raise RuntimeError('Symbols without primary at %08x' % value)
        primary = symbols.createLabel(addr, name, global_ns, SourceType.USER_DEFINED)
    else:
        if len(existing) != 1:
            raise RuntimeError('Expected one pre-label at %08x' % value)
        if primary.getParentNamespace() != global_ns:
            primary.setNameAndNamespace(name, global_ns, SourceType.USER_DEFINED)
        else:
            primary.setName(name, SourceType.USER_DEFINED)
    post = symbols.getPrimarySymbol(addr)
    if (post is None or unicode(post.getName()) != name or
            str(post.getSource()) != 'USER_DEFINED' or
            post.getParentNamespace() != global_ns or
            len(list(symbols.getSymbols(addr))) != 1):
        raise RuntimeError('Label materialization failed at %08x' % value)
    return post

def exact_ref_cores(value):
    return [ref_core(ref_row(ref)) for ref in references.getReferencesFrom(toAddr(value))]

def instruction_starts_in_range(lo, hi):
    result = set()
    iterator = listing.getInstructions(AddressSet(toAddr(lo), toAddr(hi - 1)), True)
    while iterator.hasNext():
        result.add(long(iterator.next().getAddress().getOffset()))
    return result

def apply_all():
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
        after = instruction_starts_in_range(lo, hi)
        additions = after - before
        if value not in after or not additions or not additions.issubset(expected_set):
            raise RuntimeError('Missing-start seed result at %08x' % value)
        DYNAMIC_COUNTS['R4_MISSING_SEEDS'] += 1
    actual_range_starts = set()
    for lo, hi in CODE_RANGES:
        actual_range_starts.update(instruction_starts_in_range(lo, hi))
    if actual_range_starts != expected_set:
        raise RuntimeError('R4 instruction address set has extra/missing starts')
    COUNTS['R4_INSTRUCTIONS'] = len(actual_range_starts)
    for value in POOL_ADDRESSES:
        clearListing(toAddr(value), toAddr(value + 3))
        listing.createData(toAddr(value), Undefined4DataType.dataType)
        COUNTS['R4_POOL_WORDS'] += 1
    for value, name in sorted(CASE_NAMES.items()):
        if value == PROJECTION_EQ_VALUE:
            fn = functions.getFunctionAt(toAddr(value))
            primary = symbols.getPrimarySymbol(toAddr(value))
            if (fn is None or primary is None or long(primary.getID()) != 16957 or
                    unicode(primary.getName()) != PROJECTION_EQ_NAME or
                    str(primary.getSymbolType()) != 'Function' or
                    str(primary.getSource()) != 'USER_DEFINED' or
                    len(list(symbols.getSymbols(toAddr(value)))) != 1):
                raise RuntimeError('Projection Function target changed')
            COUNTS['CASE_FUNCTION_PRESERVE'] += 1
        else:
            ensure_single_global_label(value, name)
            COUNTS['CASE_LABEL'] += 1
    for value, name in sorted(TABLE_BASES.items()):
        ensure_single_global_label(value, name)
        COUNTS['TABLE_BASE_LABEL'] += 1
    for value, name in sorted(REF_TARGET_NAMES.items()):
        primary = symbols.getPrimarySymbol(toAddr(value))
        if value == LP_COUNTER:
            require(primary is not None and str(primary.getSource()) == 'DEFAULT',
                    'LP_COUNTER_EXPECT_DEFAULT_BEFORE')
            ensure_single_global_label(value, name)
            COUNTS['REF_TARGET_MATERIALIZE'] += 1
        else:
            if (primary is None or unicode(primary.getName()) != name or
                    str(primary.getSource()) != 'USER_DEFINED' or
                    primary.getParentNamespace() != global_ns):
                raise RuntimeError('Static REF target changed at %08x' % value)
    for value, row in sorted(SLOTS.items()):
        action = row['action']
        addr = toAddr(value)
        original = int(row['original_value'], 16)
        if (memory.getInt(addr) & 0xffffffff) != original:
            raise RuntimeError('ROM value changed at %08x' % value)
        if action.startswith('EQ_'):
            if exact_ref_cores(value):
                raise RuntimeError('EQ source has DATA ref at %08x' % value)
            eq = equates.getEquate(row['const_or_target'])
            if eq is None:
                eq = equates.createEquate(row['const_or_target'], original)
            elif (eq.getValue() & 0xffffffff) != original:
                raise RuntimeError('Equate conflict: ' + row['const_or_target'])
            matches = [ref for ref in eq.getReferences()
                       if ref.getAddress() == addr and ref.getOpIndex() == 0]
            if action in ('EQ_ADD', 'EQ_MATERIALIZE') and not matches:
                eq.addReference(addr, 0)
            elif len(matches) != 1:
                raise RuntimeError('Equate reference contract at %08x' % value)
        elif action.startswith('REF_'):
            existing = exact_ref_cores(value)
            if action == 'REF_PRESERVE':
                expected = [ref_core(item) for item in json.loads(row['refs_from_json'])]
                if existing != expected:
                    raise RuntimeError('Preserved REF changed at %08x' % value)
            else:
                if existing:
                    raise RuntimeError('New REF source occupied at %08x' % value)
                ref = references.addMemoryReference(addr, toAddr(original), RefType.DATA,
                                                     SourceType.USER_DEFINED, 0)
                references.setPrimary(ref, True)
        elif action in ('TABLE_ENTRY_MATERIALIZE',
                        'TABLE_ENTRY_EQUATE_EVEN_FUNCTION'):
            expected = [ref_core(item) for item in json.loads(row['refs_from_json'])]
            if exact_ref_cores(value) != expected:
                raise RuntimeError('Table source ref changed at %08x' % value)
            if action == 'TABLE_ENTRY_EQUATE_EVEN_FUNCTION':
                eq = equates.getEquate(PROJECTION_EQ_NAME)
                if eq is None:
                    eq = equates.createEquate(PROJECTION_EQ_NAME, PROJECTION_EQ_VALUE)
                elif (eq.getValue() & 0xffffffff) != PROJECTION_EQ_VALUE:
                    raise RuntimeError('Projection Equate value conflict')
                matches = [ref for ref in eq.getReferences()
                           if ref.getAddress() == addr and ref.getOpIndex() == 0]
                if not matches:
                    eq.addReference(addr, 0)
                elif len(matches) != 1:
                    raise RuntimeError('Projection Equate reference duplicate at %08x' % value)
        else:
            raise RuntimeError('Unknown action at %08x: %s' % (value, action))
        if row['final_slot_label'] != 'none':
            ensure_single_global_label(value, row['final_slot_label'])
            COUNTS['SOURCE_LABEL'] += 1
        listing.setComment(addr, CodeUnit.EOL_COMMENT, row['new_eol_ascii'])
        COUNTS['EOL'] += 1
        COUNTS[action] += 1
    for value, row in sorted(BODY_MUTATIONS.items()):
        fn = functions.getFunctionAt(toAddr(value))
        if fn is None or long(fn.getSymbol().getID()) != long(row['function_id']):
            raise RuntimeError('Body function identity changed at %08x' % value)
        body = AddressSet()
        for lo_text, hi_text in json.loads(row['final_body_ranges_json']):
            body.addRange(toAddr(int(lo_text, 16)), toAddr(int(hi_text, 16) - 1))
        fn.setBody(body)
        COUNTS['BODY_UPDATE'] += 1
    for value, row in sorted(RENAMES.items()):
        functions.getFunctionAt(toAddr(value)).setName(row['final_name'],
                                                        SourceType.USER_DEFINED)
        COUNTS['FUNC_RENAME'] += 1
    for value, row in sorted(PLATE_WRITES.items()):
        listing.setComment(toAddr(value), CodeUnit.PLATE_COMMENT, row['new_plate'])
        COUNTS['PLATE_WRITE'] += 1

def expected_refs(rows):
    result = json.loads(json.dumps(rows))
    approved_dynamic = set(SLOTS) | set(CASE_NAMES) | set(TABLE_BASES) | set([LP_COUNTER])
    for item in result:
        try:
            target = int(item['to'], 16)
        except Exception:
            continue
        if target in approved_dynamic:
            primary = symbols.getPrimarySymbol(toAddr(target))
            if primary is None:
                fail('APPROVED_DERIVED_TARGET_MISSING_%08x' % target)
            else:
                item['target_primary_id'] = long(primary.getID())
                item['target_primary_name'] = unicode(primary.getName(True))
                item['target_primary_type'] = str(primary.getSymbolType())
                item['target_primary_source'] = str(primary.getSource())
        if target in RENAMES and item.get('target_primary_name') == RENAMES[target]['current_name']:
            item['target_primary_name'] = RENAMES[target]['final_name']
    return result

def function_metadata_core(row):
    return dict((key, row[key]) for key in (
        'entry', 'symbol', 'namespace', 'body', 'body_ranges', 'body_size',
        'body_sha256', 'body_bytes', 'eol_comments', 'calling_convention',
        'signature_source', 'prototype', 'custom_variable_storage', 'varargs',
        'inline', 'no_return', 'external', 'thunk', 'thunk_target',
        'stack_purge_size', 'return', 'parameters'))

def unit_layout_core(row):
    owner = row['function_owner']
    return {
        'address': row['address'], 'byte': row['byte'], 'unit': row['unit'],
        'data_at': row['data_at'], 'defined_data_at': row['defined_data_at'],
        'tmode': row['tmode'],
        'function_owner': None if owner is None else {
            'entry': owner['entry'], 'id': owner['id']},
    }

def source_in_ranges(source, ranges):
    value = int(source, 16)
    return any(int(lo, 16) <= value < int(hi, 16) for lo, hi in ranges)

def expected_instruction_ref_cores(value):
    result = [dict(row) for row in FLOW_REF_ROWS
              if int(row['from'], 16) == value]
    result.extend({
        'from': row['from'][2:], 'to': row['to'][2:], 'operand': 1,
        'type': 'READ', 'source': 'DEFAULT', 'primary': True,
    } for row in PC_READ_ROWS if int(row['from'], 16) == value)
    return result

def expected_body_ref_cores(host, before):
    final_ranges = FINAL_BODY_RANGES[host]
    result = [ref_core(item) for item in before['body_references']
              if any(lo <= int(item['from'], 16) < hi for lo, hi in final_ranges)]
    for value in INSTRUCTION_ADDRESSES:
        if HOST_BY_INSTRUCTION[value] == host:
            result.extend(expected_instruction_ref_cores(value))
    return result

def verify_r4_post(pre):
    actual_instruction_addresses = []
    flow_pairs = []
    pc_pairs = []
    fallthroughs = []
    instruction_set = set(INSTRUCTION_ADDRESSES)
    for value in range(SEGMENT_START, SEGMENT_END):
        instruction = listing.getInstructionAt(toAddr(value))
        if instruction is None:
            continue
        actual_instruction_addresses.append(value)
        if value not in instruction_set:
            continue
        for target in instruction.getFlows():
            flow_pairs.append([value, long(target.getOffset())])
        for ref in references.getReferencesFrom(toAddr(value)):
            if str(ref.getReferenceType()) == 'READ' and int(ref.getOperandIndex()) == 1:
                pc_pairs.append([value, long(ref.getToAddress().getOffset())])
        fall = instruction.getFallThrough()
        if fall is not None:
            fallthroughs.append([value, long(fall.getOffset())])
            require(long(fall.getOffset()) == value + int(instruction.getLength()),
                    'R4_FALLTHROUGH_TARGET_%08x' % value)
    pre_addresses = [int(row['address'], 16) for row in pre['segment_byte_units']
                     if row['instruction_at'] is not None]
    same('R4_INSTRUCTION_ADDRESS_SET', actual_instruction_addresses,
         sorted(pre_addresses + INSTRUCTION_ADDRESSES))
    instruction_map = dict((int(row['address'], 16), row) for row in INSTRUCTION_ROWS)
    for value in INSTRUCTION_ADDRESSES:
        expected = instruction_map[value]
        instruction = listing.getInstructionAt(toAddr(value))
        require(instruction is not None and
                bytes_hex(value, int(expected['length'])) == expected['raw_bytes'] and
                int(instruction.getLength()) == int(expected['length']) and
                str(instruction.getFlowOverride()) == 'NONE',
                'R4_INSTRUCTION_%08x' % value)
        owner = functions.getFunctionContaining(toAddr(value))
        host = HOST_BY_INSTRUCTION[value]
        require(owner is not None and
                long(owner.getEntryPoint().getOffset()) == host and
                long(owner.getSymbol().getID()) == long(PLATES[host]['function_id']),
                'R4_OWNER_%08x' % value)
        context_value = currentProgram.getProgramContext().getValue(
            tmode_register, toAddr(value), False)
        require(context_value is not None and int(context_value) == 1,
                'R4_TMODE_%08x' % value)
        same('R4_SOURCE_REFS_%08x' % value, exact_ref_cores(value),
             expected_instruction_ref_cores(value))
    same('R4_FLOW_SET', sorted(flow_pairs),
         sorted([[int(row['from'], 16), int(row['to'], 16)] for row in FLOW_ROWS]))
    same('R4_PC_READ_SET', sorted(pc_pairs),
         sorted([[int(row['from'], 16), int(row['to'], 16)] for row in PC_READ_ROWS]))
    same('R4_FALLTHROUGH_SET', sorted(fallthroughs),
         sorted([[int(row['from'], 16), int(row['to'], 16)]
                 for row in FALLTHROUGH_ROWS]))
    require(len(flow_pairs) == 248 and len(pc_pairs) == 95 and
            len(fallthroughs) == 1338,
            'R4_DYNAMIC_COUNTS')
    for value in POOL_ADDRESSES:
        state = address_state(value)
        require(state['defined_data_at'] is not None and
                state['defined_data_at']['length'] == 4 and
                state['defined_data_at']['type'] == '/undefined4' and
                state['instruction'] is None,
                'R4_POOL_DATA_%08x' % value)
        owner = functions.getFunctionContaining(toAddr(value))
        hosts = [entry for entry, ranges in FINAL_BODY_RANGES.items()
                 if any(lo <= value < hi for lo, hi in ranges)]
        require(hosts == [] and owner is None,
                'R4_POOL_OWNER_%08x' % value)
    pre_units = dict((int(row['address'], 16), row) for row in pre['segment_byte_units'])
    units = segment_byte_units()
    units_by_address = dict((int(row['address'], 16), row) for row in units)
    for lo, hi in PADDING_RANGES:
        for value in range(lo, hi):
            actual = unit_layout_core(units_by_address[value])
            before = unit_layout_core(pre_units[value])
            actual.pop('function_owner', None)
            before.pop('function_owner', None)
            same('R4_PADDING_UNIT_%08x' % value, actual, before)
            owner = functions.getFunctionContaining(toAddr(value))
            hosts = [entry for entry, ranges in FINAL_BODY_RANGES.items()
                     if any(rlo <= value < rhi for rlo, rhi in ranges)]
            require(hosts == [] and owner is None,
                    'R4_PADDING_OWNER_%08x' % value)
    starts = [row for row in units if row['unit'] is not None and
              row['unit']['min'] == row['address'][2:]]
    same('R4_FINAL_UNIT_COUNTS', {
        'instruction_starts': sum(row['instruction_at'] is not None for row in starts),
        'defined_len4': sum(row['defined_data_at'] is not None and
                            row['defined_data_at']['length'] == 4 for row in starts),
    }, {'instruction_starts': 2696, 'defined_len4': 206})
    changed = set()
    for lo, hi in CODE_RANGES + PADDING_RANGES:
        changed.update(range(lo, hi))
    for base in POOL_ADDRESSES:
        changed.update(range(base, base + 4))
    changed.update([PARTIAL_DATA, PARTIAL_DATA + 1])
    for row in units:
        value = int(row['address'], 16)
        if value not in changed:
            same('UNIT_STATIC_POST_%08x' % value,
                 unit_layout_core(row), unit_layout_core(pre_units[value]))

def verify_function_post(pre):
    pre_functions = dict(zip(FUNCTIONS, pre['functions']))
    for value, row in sorted(PLATES.items()):
        actual = function_row(value)
        before = pre_functions[value]
        require(actual is not None and actual['name'] == row['final_name'] and
                actual['symbol']['id'] == before['symbol']['id'] and
                actual['symbol']['source'] == 'USER_DEFINED' and
                actual['symbol']['type'] == 'Function' and
                actual['symbol']['global'] and actual['symbol']['primary'] and
                actual['namespace']['global'],
                'FUNCTION_IDENTITY_POST_%08x' % value)
        require(actual['plate'] == row['new_plate'],
                'FUNCTION_PLATE_POST_%08x' % value)
        require(actual['body_ranges'] == json.loads(row['final_body_ranges_json']) and
                actual['body_size'] == int(row['final_body_size']) and
                actual['body_sha256'] == row['final_body_sha256'],
                'FUNCTION_BODY_CONTRACT_POST_%08x' % value)
        same('FUNCTION_INCOMING_POST_%08x' % value, actual['incoming'],
             expected_refs(json.loads(row['final_incoming_json'])))
        actual_core = function_metadata_core(actual)
        before_core = function_metadata_core(before)
        for core in (actual_core, before_core):
            core['symbol'] = dict(core['symbol'])
            core['symbol'].pop('name', None)
            core['symbol'].pop('qualified_name', None)
            for key in ('body', 'body_ranges', 'body_size', 'body_sha256', 'body_bytes'):
                core.pop(key, None)
        actual_prototype = actual_core.pop('prototype')
        before_prototype = before_core.pop('prototype')
        expected_prototype = before_prototype
        if value in RENAMES:
            expected_prototype = before_prototype.replace(
                RENAMES[value]['current_name'], RENAMES[value]['final_name'], 1)
        require(actual_prototype == expected_prototype,
                'FUNCTION_PROTOTYPE_POST_%08x' % value)
        same('FUNCTION_BODY_REF_CORE_POST_%08x' % value,
             [ref_core(item) for item in actual['body_references']],
             expected_body_ref_cores(value, before))
        same('FUNCTION_METADATA_POST_%08x' % value, actual_core, before_core)

def expected_word_incoming(value, before):
    result = [ref_core(item) for item in before['references_to']]
    result.extend({
        'from': '%08x' % int(row['from'], 16), 'to': '%08x' % value,
        'operand': 1, 'type': 'READ', 'source': 'DEFAULT', 'primary': True,
    } for row in PC_READ_ROWS if int(row['to'], 16) == value)
    result.extend({
        'from': '%08x' % int(row['address'], 16), 'to': '%08x' % value,
        'operand': 0, 'type': 'DATA', 'source': 'USER_DEFINED', 'primary': True,
    } for row in REF_ROWS if row['action'] in ('REF_ADD', 'REF_MATERIALIZE') and
        int(row['original_value'], 16) == value)
    return result

def verify_word_post(value, row, actual, before):
    action = row['action']
    require(actual['bytes'] == before['bytes'] and
            actual['rom_word'] == int(row['original_value'], 16),
            'WORD_BYTES_POST_%08x' % value)
    require(actual['defined_data_at'] is not None and
            actual['defined_data_at']['length'] == 4 and
            actual['instruction'] is None,
            'WORD_DATA_POST_%08x' % value)
    expected_label = row['final_slot_label']
    if expected_label == 'none':
        require(actual['symbol_count'] == 0, 'WORD_NO_LABEL_POST_%08x' % value)
    else:
        require(actual['symbol_count'] == 1 and
                actual['primary_symbol']['name'] == expected_label and
                actual['primary_symbol']['source'] == 'USER_DEFINED' and
                actual['primary_symbol']['primary'] and
                actual['primary_symbol']['global'],
                'WORD_LABEL_POST_%08x' % value)
        primary_id = actual['primary_symbol']['id']
        primary_name = actual['primary_symbol']['qualified_name']
        require(all(item['target_primary_id'] == primary_id and
                    item['target_primary_name'] == primary_name
                    for item in actual['references_to']),
                'WORD_READ_DERIVED_POST_%08x' % value)
    require(actual['eol'] == row['new_eol_ascii'], 'WORD_EOL_POST_%08x' % value)
    expected_equates = sorted([
        {'name': item['name'], 'value': int(item['value'], 16)}
        for item in json.loads(row['after_equates_json'])],
        key=lambda item: (item['name'], item['value']))
    same('WORD_EQUATE_SET_POST_%08x' % value,
         actual['equates'], expected_equates)
    same('WORD_READ_CORE_POST_%08x' % value,
         [ref_core(item) for item in actual['references_to']],
         expected_word_incoming(value, before))
    source_cores = [ref_core(item) for item in actual['references_from']]
    if action.startswith('EQ_'):
        same('EQ_SET_POST_%08x' % value, actual['equates'],
             [{'name': row['const_or_target'], 'value': int(row['original_value'], 16)}])
        require(source_cores == [], 'EQ_REF_POST_%08x' % value)
    elif action in ('REF_ADD', 'REF_MATERIALIZE'):
        require(actual['equates'] == [], 'REF_EQ_POST_%08x' % value)
        same('REF_NEW_POST_%08x' % value, source_cores,
             [{'from': '%08x' % value,
               'to': '%08x' % int(row['original_value'], 16),
               'operand': 0, 'type': 'DATA', 'source': 'USER_DEFINED',
               'primary': True}])
    elif action == 'REF_PRESERVE':
        require(actual['equates'] == [], 'REF_PRESERVE_EQ_POST_%08x' % value)
        same('REF_PRESERVE_POST_%08x' % value, source_cores,
             [ref_core(item) for item in before['references_from']])
        require(actual['references_from'][0]['target_primary_id'] == 15545 and
                actual['references_from'][0]['target_primary_name'] == 'gP1LifePoints' and
                actual['references_from'][0]['target_primary_source'] == 'USER_DEFINED',
                'REF_PRESERVE_TARGET_POST')
    elif action in ('TABLE_ENTRY_MATERIALIZE',
                    'TABLE_ENTRY_EQUATE_EVEN_FUNCTION'):
        same('TABLE_SOURCE_CORE_POST_%08x' % value, source_cores,
             [ref_core(item) for item in before['references_from']])
        primary = symbols.getPrimarySymbol(toAddr(int(row['original_value'], 16)))
        require(len(actual['references_from']) == 1 and primary is not None and
                actual['references_from'][0]['target_primary_id'] == long(primary.getID()) and
                actual['references_from'][0]['target_primary_name'] ==
                unicode(primary.getName(True)),
                'TABLE_DERIVED_POST_%08x' % value)

def verify_post(pre):
    require(int(pre['function_count']) == FUNCTION_COUNT and
            int(functions.getFunctionCount()) == FINAL_FUNCTION_COUNT,
            'FUNCTION_COUNT_POST')
    require(raw_hash(SEGMENT_START, SEGMENT_END) ==
            pre['segment']['sha256'] == SEGMENT_SHA256,
            'SEGMENT_RAW_HASH_POST')
    verify_r4_post(pre)
    verify_function_post(pre)
    pre_observers = dict((int(row['entry'], 16), row)
                         for row in pre['observer_functions'])
    for value, before in sorted(pre_observers.items()):
        if value in PLATES:
            continue
        expected = json.loads(json.dumps(before))
        expected['body_references'] = expected_refs(expected['body_references'])
        expected['incoming'] = expected_refs(expected['incoming'])
        for item in FLOW_REF_ROWS:
            if int(item['to'], 16) != value:
                continue
            enriched = dict(item)
            enriched['target_primary_id'] = before['symbol']['id']
            enriched['target_primary_name'] = before['symbol']['qualified_name']
            enriched['target_primary_type'] = before['symbol']['type']
            enriched['target_primary_source'] = before['symbol']['source']
            expected['incoming'].append(enriched)
        same('OBSERVER_FUNCTION_STATIC_POST_%08x' % value,
             function_row(value), expected)
    pre_slots = dict((int(row['address'], 16), row) for row in pre['slots'])
    for value, row in sorted(SLOTS.items()):
        verify_word_post(value, row, address_state(value), pre_slots[value])
    pre_cases = dict((int(row['address'], 16), row) for row in pre['case_targets'])
    for value, name in sorted(CASE_NAMES.items()):
        state = address_state(value)
        primary = state['primary_symbol']
        function = functions.getFunctionAt(toAddr(value))
        require(state['symbol_count'] == 1 and primary is not None and
                primary['name'] == name and primary['source'] == 'USER_DEFINED' and
                primary['type'] == ('Function' if function is not None else 'Label') and
                primary['global'] and primary['primary'],
                'CASE_LABEL_POST_%08x' % value)
        additions = [row for row in FLOW_REF_ROWS if int(row['to'], 16) == value]
        same('CASE_INCOMING_CORE_POST_%08x' % value,
             [ref_core(item) for item in state['references_to']],
             [ref_core(item) for item in pre_cases[value]['references_to']] + additions)
    for value, name in sorted(TABLE_BASES.items()):
        state = address_state(value)
        require(state['symbol_count'] == 1 and
                state['primary_symbol']['name'] == name and
                state['primary_symbol']['source'] == 'USER_DEFINED' and
                state['primary_symbol']['type'] == 'Label' and
                state['primary_symbol']['global'] and
                state['primary_symbol']['primary'],
                'TABLE_BASE_LABEL_POST_%08x' % value)
    same('PROJECTION_GLOBAL_EQUATE_POST',
         equate_global_row(PROJECTION_EQ_NAME), {
             'name': PROJECTION_EQ_NAME,
             'value': PROJECTION_EQ_VALUE,
             'references': [{'address': '%08x' % value, 'operand': 0}
                            for value in [0x080aa7c0, 0x080aa7c4, 0x080aa7c8,
                                          0x080aa7cc, 0x080aa7d0]],
         })
    projection_target = address_state(PROJECTION_EQ_VALUE)
    require(projection_target['symbol_count'] == 1 and
            projection_target['primary_symbol']['id'] == 16957 and
            projection_target['primary_symbol']['name'] == PROJECTION_EQ_NAME and
            projection_target['primary_symbol']['type'] == 'Function' and
            projection_target['primary_symbol']['source'] == 'USER_DEFINED',
            'PROJECTION_TARGET_FUNCTION_POST')
    pre_targets = dict((int(row['address'], 16), row) for row in pre['targets'])
    for value in REF_TARGETS:
        actual = address_state(value)
        before = pre_targets[value]
        additions = [{'from': '%08x' % int(row['address'], 16),
                      'to': '%08x' % value, 'operand': 0, 'type': 'DATA',
                      'source': 'USER_DEFINED', 'primary': True}
                     for row in REF_ROWS
                     if row['action'] in ('REF_ADD', 'REF_MATERIALIZE') and
                     int(row['original_value'], 16) == value]
        same('REF_TARGET_REFS_TO_POST_%08x' % value,
             [ref_core(item) for item in actual['references_to']],
             [ref_core(item) for item in before['references_to']] + additions)
        expected_name = REF_TARGET_NAMES[value]
        require(actual['symbol_count'] == 1 and
                actual['primary_symbol']['name'] == expected_name and
                actual['primary_symbol']['source'] == 'USER_DEFINED' and
                actual['primary_symbol']['global'] and actual['primary_symbol']['primary'],
                'REF_TARGET_PRIMARY_POST_%08x' % value)
        if value == LP_COUNTER:
            require(actual['primary_symbol']['name'] == 'gLpBarDisplayCounter' and
                    actual['primary_symbol']['type'] == 'Label' and
                    actual['bytes'] is None and before['bytes'] is None,
                    'LP_COUNTER_POST')
        elif value in TABLE_BASES:
            require(before['symbol_count'] == 0 and
                    before['primary_symbol'] is None and
                    actual['primary_symbol']['type'] == 'Label',
                    'REF_TARGET_TABLE_BASE_MATERIALIZE_POST_%08x' % value)
        else:
            require(before['primary_symbol'] is not None and
                    actual['primary_symbol']['id'] == before['primary_symbol']['id'] and
                    actual['primary_symbol']['type'] == before['primary_symbol']['type'] and
                    actual['primary_symbol']['source'] == before['primary_symbol']['source'],
                    'REF_TARGET_STATIC_ID_POST_%08x' % value)
    partial_before = pre['partial_data']
    partial = address_state(PARTIAL_DATA)
    # The word at 080ab278 is also an approved REF_ADD slot.  Its source
    # symbol, EOL, equate/ref projections, and rich incoming target metadata
    # are therefore verified by verify_word_post above.  This observer only
    # freezes the independent data/layout fields while releasing Fn ownership.
    for key in ('bytes', 'rom_word', 'data_at', 'defined_data_at',
                'data_containing', 'instruction', 'plate'):
        same('PARTIAL_DATA_LAYOUT_PRESERVE_' + key,
             partial[key], partial_before[key])
    require(partial['function_containing'] is None,
            'PARTIAL_DATA_OWNER_RELEASE_POST')
    pre_callees = dict((int(row['address'], 16), row)
                       for row in pre['direct_callee_targets'])
    for value, before in sorted(pre_callees.items()):
        actual = address_state(value)
        additions = [row for row in FLOW_REF_ROWS if int(row['to'], 16) == value]
        same('CALLEE_INCOMING_CORE_POST_%08x' % value,
             [ref_core(item) for item in actual['references_to']],
             [ref_core(item) for item in before['references_to']] + additions)
    if MODE == 'apply':
        same('APPLY_COUNTS', COUNTS, EXPECTED_COUNTS)

print('=== RefineF14Seg3 mode=%s ===' % MODE)
verify_inputs()
reject('INPUTS')

if MODE == 'prestate':
    state = capture()
    verify_prestate(state)
    reject('PRESTATE')
    write_json(PRESTATE_NAME, state)
    print('PRESTATE plate_functions=5 observer_functions=190 slots=206 targets=%d '
          'table_sources=28 cases=16 bases=3 odd=0 direct_callees=%d '
          'segment_bytes=6488 FAIL=0' %
          (len(state['targets']), len(DIRECT_CALLEE_TARGETS)))
    print('STATUS: OK mode=prestate read_only=true')
else:
    prestate_hash = file_hash(run_path(PRESTATE_NAME))
    prestate = read_json(PRESTATE_NAME)
    plan = read_json(PLAN_NAME)
    verify_plan(plan, prestate_hash)
    reject('PLAN')
    if MODE == 'dry':
        verify_prestate(prestate)
        reject('DRY')
        result = {
            'status': 'F14_SEG3_DRY_PREFLIGHT_OK', 'FAIL': 0,
            'script_sha256': file_hash(getSourceFile().getAbsolutePath()),
            'plan_sha256': file_hash(run_path(PLAN_NAME)),
            'prestate_sha256': prestate_hash,
            'source_snapshot_manifest_sha256': file_hash(run_path(SOURCE_SNAPSHOT_NAME)),
            'counts': EXPECTED_COUNTS,
            'preflight': {
                'plate_functions': 5, 'observer_functions': 190,
                'slots': 206, 'ref_targets': len(REF_TARGETS),
                'table_sources': 28, 'case_targets': 16, 'table_bases': 3,
                'odd_targets': 0, 'direct_callees': len(DIRECT_CALLEE_TARGETS),
                'segment_bytes': 6488, 'r4_instructions': 1411,
                'r4_pc_reads': 95, 'r4_flows': 248, 'r4_calls': 58,
                'r4_fallthroughs': 1338, 'body_mutations': 4,
                'new_functions': 0, 'carve': 0,
            },
            'semantic_actions_applied': False,
        }
        write_json('f14-seg3-dry-result-v3.json', result)
        print('PREFLIGHT slots=206 EQ=122 REF=56 TABLE=28 FUNC_RENAME=3 '
              'BODY_UPDATE=4 PLATE_WRITE=5 R4=1411 FAIL=0')
        print('STATUS: OK mode=dry FAIL=0 semantic_actions_applied=false')
    elif MODE == 'check':
        verify_post(prestate)
        reject('PERSISTED_CHECK')
        write_json('f14-seg3-persisted-check-v3.json', {
            'status': 'F14_SEG3_PERSISTED_CHECK_OK', 'FAIL': 0,
            'script_sha256': file_hash(getSourceFile().getAbsolutePath()),
            'plan_sha256': file_hash(run_path(PLAN_NAME)),
            'prestate_sha256': prestate_hash,
        })
        print('STATUS: OK mode=check FAIL=0 read_only=true')
    else:
        verify_prestate(prestate)
        reject('APPLY_PRESTATE')
        transaction = currentProgram.startTransaction('F14-Seg-3 approved materialization')
        commit = False
        error_text = None
        try:
            apply_all()
            verify_post(prestate)
            if FAILS:
                raise RuntimeError('Postcondition FAIL=%d' % len(FAILS))
            commit = True
        except Exception as error:
            error_text = unicode(error)
            if not FAILS:
                fail('APPLY_EXCEPTION', error_text, None)
        finally:
            currentProgram.endTransaction(transaction, commit)
        if not commit:
            write_json('f14-seg3-apply-failures-v2.json', {
                'status': 'FAIL_ROLLED_BACK', 'FAIL': len(FAILS),
                'error': error_text, 'failures': FAILS,
                'transaction_committed': False,
            })
            raise RuntimeError('F14-Seg-3 apply rolled back')
        write_json('f14-seg3-apply-receipt-v2.json', {
            'status': 'F14_SEG3_APPLY_OK', 'FAIL': 0,
            'script_sha256': file_hash(getSourceFile().getAbsolutePath()),
            'plan_sha256': file_hash(run_path(PLAN_NAME)),
            'prestate_sha256': prestate_hash, 'counts': COUNTS,
            'dynamic_counts': DYNAMIC_COUNTS,
            'transaction_committed': True,
        })
        print('STATUS: OK mode=apply FAIL=0 transaction_committed=true')

