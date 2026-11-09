# -*- coding: ascii -*-
#@runtime Jython
#@category Ygo-ex2006.Refine
# F14-Seg-2 PASS materialization. prestate/dry/check are read-only.

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
PLAN_NAME = 'f14-seg2-plan-v2.json'
PRESTATE_NAME = 'f14-seg2-fresh-full-prestate-v2.json'
SOURCE_SNAPSHOT_NAME = 'f14-seg2-source-snapshot-preapply-v2.json'
FREEZE_MANIFEST_NAME = 'f14-seg2-freeze-manifest.json'
MAP_NAME = 'f14-seg2-r4-cfg-map.json'
MACHINE_CONTRACT_NAME = 'f14-seg2-mode-a-machine-contract.json'
DB_BACKUP_MANIFEST_NAME = 'root-f14-seg2-db-backup.json'

INPUT_HASHES = {
    'doc/dev/refine/F14-Seg-2.proposal.md': 'de2dee2f06c1daa5fa2f558aa6d6e9fa19a05a1ff567590eb4c7fc5704c5b809',
    'doc/dev/refine/F14-Seg-2.review.md': '6a925e4fd27f711e680772dcbf6f8c0111fd6320a849f28e0a4e5646177bb2db',
    'doc/dev/refine/F14-Seg-2.slots.tsv': '32c3f4b9fb7ffeac283bd281859fc9bfc70c5eb5fa4aeb1a5b35ae53c91a5a71',
    'doc/dev/refine/F14-Seg-2.plates.tsv': '239b1abec33838950e7d089e8fb89038bce57c0e796379aab6b7835762644325',
    'output/refine-run-20261028-105948/f14-seg2-freeze-manifest.json': '9fd76592edb220c3f0c98bb03a45a4dff30293a36ed110fdb5fda236dec5f63c',
    'output/refine-run-20261028-105948/f14-seg2-mode-a-machine-contract.json': 'e9d077cd245e2b23f7fed2793cd46b5aefcb0258c9de95d80aa73075d9fd1bcc',
    'output/refine-run-20261028-105948/f14-seg2-review-round2-audit.json': 'b967598f78237a2826b257b86c91dacf5d99ca921a2da39c0fc305edbde2ed35',
    'output/refine-run-20261028-105948/f14-seg2-r4-cfg-map.json': '8d30c1f7bc2ac86184317407a1da7b2591ea1ee9c09056d37a9b0e3f0d6fe98b',
    'output/refine-run-20261028-105948/root-f14-seg2-r4-static-gate.json': '5edd64197f8d992b16c2075df73f62c46b6ecdf1c2b30498b22a56eecd360741',
    'output/refine-run-20261028-105948/root-f14-seg2-mode-a-narrow-gate.json': 'c6291d883d2d2c22eb4d8781fb5016274c18cf53f066093c4cf7a62f2cd0c6cb',
    'output/refine-run-20261028-105948/root-f14-seg2-seed-cfg-closure.json': 'cd15e922666a67a343693ec5434546be39cda4274870954fb655db9d03b1384a',
    'output/refine-run-20261028-105948/root-f14-seg1-independent-post.json': 'cfc6200c79d83bdcba134c8c4bf1f210765e3c1680527b2ae2343c4da9c22ef0',
    'output/refine-run-20261028-105948/root-f14-seg2-supplement-prestate.json': '1e6af504513f856b743e882721270321d91aa2ac9b7ae4e4e801087045c61b1f',
    'output/refine-run-20261028-105948/root-f14-seg2-failed-apply-v1-audit.json': 'adbb27bc9e1d6b058efb96842042a3179e2b43ab504ae648b081e70631cf303a',
    'output/refine-run-20261028-105948/root-f14-seg2-db-restore-after-v1.json': 'baeb4e9e4f494cf26aad173c709db0bce4d304f7453e4d12d61a4d7213c4e0d2',
}
EXPECTED_COUNTS = {
    'EQ_ADD': 31, 'EQ_MATERIALIZE': 73,
    'REF_ADD': 36, 'REF_PRESERVE': 1,
    'TABLE_ENTRY_MATERIALIZE': 15, 'EOL': 156,
    'SOURCE_LABEL': 143, 'CASE_LABEL': 11, 'TABLE_BASE_LABEL': 2,
    'REF_TARGET_LABEL': 1, 'FUNC_RENAME': 1, 'PLATE_WRITE': 6,
    'R4_CODE_RANGES': 36, 'R4_INITIAL_SEEDS': 12,
    'R4_INSTRUCTIONS': 1699, 'R4_POOL_WORDS': 102,
    'BODY_CREATE': 1, 'BODY_EXTEND': 1, 'CARVE_DATA': 1,
}
SEGMENT_START = 0x080a8c30
SEGMENT_END = 0x080aa120
SEGMENT_SHA256 = 'f62c1a4e80b6b8b84b3705f5383e3f45aa2a3bd106d84f5288c831e3c5993c49'
FUNCTION_COUNT = 5213
FINAL_FUNCTION_COUNT = 5214
NEW_FUNCTION = 0x080a9134
EXTENDED_FUNCTION = 0x080a9734
SHARED_ENTRY = 0x080aa10c
SHARED_INTERIOR = 0x080aa10e
CARVE_START = 0x09e478c8
CARVE_END = 0x09e478ce
CARVE_RAW = '0013fd123219'

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
        write_json('f14-seg2-%s-failures-v2.json' % MODE,
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

SLOT_ROWS = read_tsv('doc/dev/refine/F14-Seg-2.slots.tsv')
PLATE_ROWS = read_tsv('doc/dev/refine/F14-Seg-2.plates.tsv')
R4_MAP = read_json(MAP_NAME)
MACHINE_CONTRACT = read_json(MACHINE_CONTRACT_NAME)
MODULE_BASELINE = read_json('root-f14-seg1-independent-post.json')
SUPPLEMENT_BASELINE = read_json('root-f14-seg2-supplement-prestate.json')
OBSERVER_FUNCTIONS = sorted(set(
    int(row['entry'], 16)
    for source in (MODULE_BASELINE, SUPPLEMENT_BASELINE)
    for row in source['functions'] if row is not None))
SLOTS = dict((int(row['address'], 16), row) for row in SLOT_ROWS)
PLATES = dict((int(row['entry'], 16), row) for row in PLATE_ROWS)
RENAMES = dict((value, row) for value, row in PLATES.items()
               if row['current_name'] != 'none' and
               row['current_name'] != row['final_name'])
PLATE_WRITES = dict((value, row) for value, row in PLATES.items()
                    if row['action'] != 'PRESERVE')
FUNCTIONS = sorted(PLATES)
NEW_FUNCTIONS = dict((value, row) for value, row in PLATES.items()
                     if row['body_action'] == 'R4_CREATE_FUNCTION')
EXTENDED_FUNCTIONS = dict((value, row) for value, row in PLATES.items()
                          if row['body_action'] == 'R4_EXTEND')
TABLE_ROWS = [row for row in SLOT_ROWS if row['action'] == 'TABLE_ENTRY_MATERIALIZE']
TABLE_SOURCES = sorted(int(row['address'], 16) for row in TABLE_ROWS)
CASE_NAMES = dict((int(row['original_value'], 16), row['target_final_label'])
                  for row in TABLE_ROWS)
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
        REF_TARGET_NAMES.setdefault(target, name)
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
HOST_BY_INSTRUCTION = {}
HOST_BY_CLUSTER = {
    'process_equip_mode1_phase_3_to_7': NEW_FUNCTION,
    'live_switch_c': EXTENDED_FUNCTION,
}
for cluster in R4_MAP['clusters']:
    host = HOST_BY_CLUSTER[cluster['id']]
    INITIAL_SEEDS.extend(int(item, 16) for item in cluster['seeds'])
    for item in cluster['code_ranges']:
        CODE_RANGES.append((int(item[0], 16), int(item[1], 16)))
    for row in cluster['pool_words']:
        POOL_ADDRESSES.append(int(row['address'], 16))
    for row in cluster['padding_or_unclassified']:
        lo = int(row['range'][0], 16)
        hi = int(row['range'][1], 16)
        PADDING_RANGES.append((lo, hi))
    for row in cluster['instructions']:
        value = int(row['address'], 16)
        INSTRUCTION_ROWS.append(row)
        HOST_BY_INSTRUCTION[value] = host
        for target in row['direct_flow_targets']:
            kind = 'CALL' if target in row['call_targets'] else 'JUMP'
            FLOW_ROWS.append({'from': row['address'], 'to': target, 'kind': kind})
            ref_type = ('UNCONDITIONAL_CALL' if kind == 'CALL' else
                        ('CONDITIONAL_JUMP' if row['kind'] == 'conditional_branch'
                         else 'UNCONDITIONAL_JUMP'))
            FLOW_REF_ROWS.append({
                'from': row['address'][2:], 'to': target[2:], 'operand': 0,
                'type': ref_type, 'source': 'DEFAULT', 'primary': True})
        for target in row['pc_read_targets']:
            PC_READ_ROWS.append({'from': row['address'], 'to': target})
        if row['fallthrough'] is not None:
            FALLTHROUGH_ROWS.append({'from': row['address'],
                                     'to': row['fallthrough']})
INSTRUCTION_ADDRESSES = sorted(int(row['address'], 16) for row in INSTRUCTION_ROWS)
POOL_ADDRESSES = sorted(POOL_ADDRESSES)
CODE_RANGES = sorted(CODE_RANGES)
PADDING_RANGES = sorted(PADDING_RANGES)
INITIAL_SEEDS = sorted(set(INITIAL_SEEDS))
DIRECT_CALLEE_TARGETS = sorted(set(int(row['to'], 16) for row in FLOW_ROWS
                                   if row['kind'] == 'CALL'))
BODY_ROWS = dict(NEW_FUNCTIONS.items() + EXTENDED_FUNCTIONS.items())
SHARED_INTERIOR_CONTRACT = MACHINE_CONTRACT['shared_tail_contract']['function_interior']

def freeze_manifest_path(relative):
    return path_in_root(relative)

def verify_inputs():
    for relative, digest in sorted(INPUT_HASHES.items()):
        same('INPUT_HASH_' + relative, file_hash(path_in_root(relative)), digest)
    manifest = read_json(FREEZE_MANIFEST_NAME)
    require(len(manifest.get('files', {})) == 20, 'FREEZE_MANIFEST_ENTRY_COUNT')
    for relative, digest in sorted(manifest.get('files', {}).items()):
        same('FREEZE_MANIFEST_HASH_' + relative,
             file_hash(freeze_manifest_path(relative)), digest)
    basis = manifest.get('review_basis', {})
    require(basis.get('path', '').endswith(
                'f14-seg2-review-round1/F14-Seg-2.review.md') and
            file_hash(path_in_root(basis['path'])) == basis['sha256'],
            'ARCHIVED_REVIEW_BASIS')
    require(len(SLOTS) == 156 and len(SLOT_ROWS) == 156 and
            len(PLATES) == 7 and len(FUNCTIONS) == 7 and
            len(RENAMES) == 1 and len(PLATE_WRITES) == 6 and
            sorted(NEW_FUNCTIONS) == [NEW_FUNCTION] and
            sorted(EXTENDED_FUNCTIONS) == [EXTENDED_FUNCTION],
            'PRIMARY_INPUT_COUNTS')
    require(len(OBSERVER_FUNCTIONS) == 173, 'OBSERVER_FUNCTION_COUNT')
    action_counts = {}
    for row in SLOT_ROWS:
        action_counts[row['action']] = action_counts.get(row['action'], 0) + 1
    same('SLOT_ACTION_COUNTS', action_counts,
         {'EQ_ADD': 31, 'EQ_MATERIALIZE': 73,
          'REF_ADD': 36, 'REF_PRESERVE': 1,
          'TABLE_ENTRY_MATERIALIZE': 15})
    require(len(TABLE_SOURCES) == 15 and len(CASE_NAMES) == 11 and
            len(TABLE_BASES) == 2 and len(REF_TARGETS) == 9 and
            len(RAM_TARGETS) == 6 and len(ODD_TARGETS) == 0,
            'REFERENCE_SCOPE_COUNTS')
    require(len(CODE_RANGES) == 36 and len(INSTRUCTION_ADDRESSES) == 1699 and
            len(POOL_ADDRESSES) == 102 and len(PADDING_RANGES) == 21 and
            len(FLOW_ROWS) == 248 and
            sum(row['kind'] == 'CALL' for row in FLOW_ROWS) == 43 and
            len(PC_READ_ROWS) == 126 and len(FALLTHROUGH_ROWS) == 1616 and
            sum(hi - lo for lo, hi in CODE_RANGES) == 3484 and
            sum(hi - lo for lo, hi in PADDING_RANGES) == 42,
            'R4_SCOPE_COUNTS')
    require(INITIAL_SEEDS == [
                0x080a9134, 0x080a927c, 0x080a932c, 0x080a9558,
                0x080a9668, 0x080a96f8, 0x080a9798, 0x080a9800,
                0x080a9b40, 0x080a9ba4, 0x080a9bac, 0x080a9c2c] and
            all(value in INSTRUCTION_ADDRESSES for value in INITIAL_SEEDS),
            'R4_INITIAL_SEED_SCOPE')
    table_contract = MACHINE_CONTRACT['table_contract']
    require(table_contract['source_count'] == 15 and
            table_contract['unique_target_count'] == 11 and
            table_contract['case_target_count'] == 11 and
            len(table_contract['entries']) == 15,
            'TABLE_MACHINE_CONTRACT')
    shared = MACHINE_CONTRACT['shared_tail_contract']
    require(shared['function_entry']['incoming_count'] == 2 and
            shared['function_entry']['function_id'] == 16954 and
            shared['function_interior']['incoming_count'] == 5 and
            shared['function_interior']['final_primary']['type'] == 'Label' and
            shared['function_interior']['final_primary']['source'] == 'DEFAULT' and
            shared['body_external_incoming_count'] == 7,
            'SHARED_TAIL_MACHINE_CONTRACT')
    require(len(BODY_ROWS) == 2 and sorted(BODY_ROWS) ==
            [NEW_FUNCTION, EXTENDED_FUNCTION], 'BODY_CONTRACT_COUNT')
    source_names = [row['final_slot_label'] for row in SLOT_ROWS
                    if row['final_slot_label'] != 'none']
    require(len(source_names) == 143 and len(set(source_names)) == 143,
            'SOURCE_LABEL_COUNT_UNIQUE')
    for value, row in sorted(SLOTS.items()):
        if row['final_slot_label'] != 'none':
            require(re.match(r'^[a-z][a-z0-9_]+$', row['final_slot_label']) is not None,
                    'SOURCE_LABEL_SYNTAX_%08x' % value)
            collisions = [item for item in symbols.getGlobalSymbols(row['final_slot_label'])
                          if item.getAddress() != toAddr(value)]
            require(not collisions, 'SOURCE_LABEL_COLLISION_%08x' % value)
        if row['new_eol_ascii'] != 'none':
            require(all(ord(char) < 128 for char in row['new_eol_ascii']),
                    'EOL_ASCII_%08x' % value)
    for value, name in sorted(CASE_NAMES.items()):
        require(re.match(r'^[a-z][a-z0-9_]+$', name) is not None,
                'CASE_LABEL_SYNTAX_%08x' % value)
        collisions = [item for item in symbols.getGlobalSymbols(name)
                      if item.getAddress() != toAddr(value)]
        require(not collisions, 'CASE_LABEL_COLLISION_%08x' % value)
    require(REF_TARGET_NAMES.get(CARVE_START) == 'equip_mode1_counter_trap_cids',
            'CARVE_TARGET_LABEL')
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
    new_fn = functions.getFunctionAt(toAddr(NEW_FUNCTION))
    if MODE == 'check':
        require(new_fn is not None and unicode(new_fn.getName()) ==
                PLATES[NEW_FUNCTION]['final_name'], 'NEW_FUNCTION_POST_INPUT')
    else:
        require(new_fn is None, 'NEW_FUNCTION_ABSENT_PRE')

def capture():
    target_addresses = sorted(set(REF_TARGETS + list(CASE_NAMES) + list(TABLE_BASES)))
    direct_functions = sorted(set(value for value in DIRECT_CALLEE_TARGETS
                                  if functions.getFunctionAt(toAddr(value)) is not None))
    equate_names = sorted(set(row['const_or_target'] for row in SLOT_ROWS
                              if row['action'].startswith('EQ_')))
    return {
        'status': 'F14_SEG2_FRESH_FULL_PRESTATE',
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
        'shared_entry': address_state(SHARED_ENTRY),
        'shared_interior': address_state(SHARED_INTERIOR),
        'carve': {
            'range': ['0x%08x' % CARVE_START, '0x%08x' % CARVE_END],
            'raw': bytes_hex(CARVE_START, CARVE_END - CARVE_START),
            'window_start': '0x09e478c0', 'window_end': '0x09e478d4',
            'window_raw': bytes_hex(0x09e478c0, 0x14),
            'states': [address_state(value) for value in
                       [0x09e478c0, 0x09e478c4, 0x09e478c8,
                        0x09e478cc, 0x09e478ce, 0x09e478d0]],
        },
        'segment_byte_units': segment_byte_units(),
    }

def bool_field(value):
    return value.lower() == 'true'

def verify_function_tsv(value, row, state):
    if value in NEW_FUNCTIONS:
        require(state is None and row['current_name'] == 'none' and
                row['function_id'] == 'dynamic' and row['function_source'] == 'none' and
                row['body_size'] == '0' and row['body_ranges_json'] == '[]' and
                row['incoming_json'] == '[]' and row['old_plate_chars'] == '0',
                'NEW_FUNCTION_ABSENT_%08x' % value)
        return
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
        path, length = old_type.rsplit(':', 1)
        require(state['data_at'] is not None and state['data_at']['type'] == path and
                state['data_at']['length'] == int(length),
                'SLOT_DATA_TYPE_%08x' % value)

def verify_prestate(pre):
    same('FRESH_PRESTATE_EXACT', capture(), pre)
    require(pre['function_count'] == FUNCTION_COUNT, 'FUNCTION_COUNT_PRE')
    require(pre['segment']['sha256'] == SEGMENT_SHA256 and
            len(pre['segment_byte_units']) == SEGMENT_END - SEGMENT_START,
            'SEGMENT_PRE')
    unit_starts = [row for row in pre['segment_byte_units']
                   if row['unit'] is not None and row['unit']['min'] == row['address'][2:]]
    same('SEGMENT_UNIT_COUNTS_PRE', {
        'instruction_starts': sum(row['instruction_at'] is not None for row in unit_starts),
        'data_starts': sum(row['unit']['class'] == 'DataDB' for row in unit_starts),
        'defined_data_starts': sum(row['defined_data_at'] is not None for row in unit_starts),
        'bytes': len(pre['segment_byte_units']),
    }, {'instruction_starts': 551, 'data_starts': 4020,
        'defined_data_starts': 54, 'bytes': 5360})
    pre_slots = dict((int(row['address'], 16), row) for row in pre['slots'])
    for value, row in sorted(SLOTS.items()):
        state = pre_slots[value]
        require(state['bytes'] == row['old_bytes'] and
                state['rom_word'] == int(row['original_value'], 16),
                'SLOT_BYTES_%08x' % value)
        same('SLOT_SYMBOLS_%08x' % value, state['symbols'],
             json.loads(row['old_symbols_json']))
        same('SLOT_PRIMARY_%08x' % value, state['primary_symbol'],
             None if row['old_primary_json'] == 'null' else json.loads(row['old_primary_json']))
        same('SLOT_REFS_FROM_%08x' % value,
             [tsv_ref_row(item) for item in state['references_from']],
             json.loads(row['refs_from_json']))
        same('SLOT_REFS_TO_%08x' % value,
             [tsv_ref_row(item) for item in state['references_to']],
             json.loads(row['refs_to_json']))
        same('SLOT_EQUATES_%08x' % value, state['equates'],
             json.loads(row['equates_json']))
        same('SLOT_EOL_%08x' % value, state['eol'],
             json.loads(row['old_eol_json']))
        data_contract_from_tsv(state, row, value)
    pre_functions = dict(zip(FUNCTIONS, pre['functions']))
    for value, row in sorted(PLATES.items()):
        verify_function_tsv(value, row, pre_functions[value])
    pre_tables = dict((int(row['address'], 16), row) for row in pre['table_sources'])
    for row in TABLE_ROWS:
        value = int(row['address'], 16)
        same('TABLE_REF_CORE_PRE_%08x' % value,
             [ref_core(item) for item in pre_tables[value]['references_from']],
             [ref_core(item) for item in json.loads(row['refs_from_json'])])
    pre_cases = dict((int(row['address'], 16), row) for row in pre['case_targets'])
    for value in CASE_NAMES:
        state = pre_cases[value]
        require(state['primary_symbol'] is not None and
                state['primary_symbol']['source'] == 'DEFAULT' and
                state['primary_symbol']['primary'] and
                state['instruction'] is None and state['function'] is None,
                'CASE_DYNAMIC_PRE_%08x' % value)
    for state in pre['ram_targets']:
        require(state['bytes'] is None and state['primary_symbol'] is not None and
                state['primary_symbol']['source'] == 'USER_DEFINED',
                'RAM_TARGET_PRE_' + state['address'])
    require(pre['odd_targets'] == [] and pre['odd_even_functions'] == [],
            'NO_ODD_ALIAS_PRE')
    shared = pre['shared_interior']
    require(shared['primary_symbol'] is None and shared['function'] is None and
            shared['references_to'] == [] and shared['instruction'] is not None and
            shared['function_containing'] is not None and
            shared['function_containing']['id'] == 16954 and
            shared['function_containing']['entry'] == '080aa10c',
            'SHARED_INTERIOR_PRE')
    carve = pre['carve']
    require(carve['raw'] == CARVE_RAW and
            carve['window_raw'] == '9b120000b81200000013fd1232190000a7160000',
            'CARVE_ROM_PRE')
    carve_state = [row for row in carve['states']
                   if row['address'] == '0x09e478c8'][0]
    require(carve_state['primary_symbol'] is None and
            carve_state['defined_data_at'] is None and
            carve_state['references_from'] == [] and
            carve_state['references_to'] == [], 'CARVE_STATE_PRE')
    for row in INSTRUCTION_ROWS:
        value = int(row['address'], 16)
        require(bytes_hex(value, int(row['length'])) == row['raw_bytes'] and
                listing.getInstructionAt(toAddr(value)) is None,
                'R4_ROM_BYTES_PRE_%08x' % value)
    for row in [item for cluster in R4_MAP['clusters']
                for item in cluster['pool_words']]:
        value = int(row['address'], 16)
        require(bytes_hex(value, 4) == row['raw_bytes'] and
                listing.getDefinedDataAt(toAddr(value)) is None and
                listing.getInstructionAt(toAddr(value)) is None,
                'R4_POOL_BYTES_PRE_%08x' % value)

def verify_plan(plan, prestate_hash):
    require(plan.get('status') == 'F14_SEG2_PLAN_FROZEN', 'PLAN_STATUS')
    same('PLAN_INPUT_HASHES', plan.get('input_hashes'), INPUT_HASHES)
    same('PLAN_COUNTS', plan.get('counts'), EXPECTED_COUNTS)
    require(plan.get('script_sha256') == file_hash(getSourceFile().getAbsolutePath()),
            'PLAN_SCRIPT_HASH')
    require(plan.get('prestate_sha256') == prestate_hash, 'PLAN_PRESTATE_HASH')
    require(plan.get('source_snapshot_manifest') == SOURCE_SNAPSHOT_NAME and
            plan.get('source_snapshot_manifest_sha256') == file_hash(run_path(SOURCE_SNAPSHOT_NAME)),
            'PLAN_SOURCE_SNAPSHOT_HASH')
    require(plan.get('freeze_manifest_sha256') == file_hash(run_path(FREEZE_MANIFEST_NAME)) and
            plan.get('db_backup_manifest_sha256') == file_hash(run_path(DB_BACKUP_MANIFEST_NAME)),
            'PLAN_MANIFEST_HASHES')
    require(plan.get('range') == [SEGMENT_START, SEGMENT_END] and
            plan.get('function_addresses') == FUNCTIONS and
            plan.get('slot_addresses') == sorted(SLOTS) and
            plan.get('table_sources') == TABLE_SOURCES and
            plan.get('case_targets') == sorted(CASE_NAMES) and
            plan.get('table_bases') == sorted(TABLE_BASES) and
            plan.get('odd_targets') == ODD_TARGETS and
            plan.get('r4')['code_ranges'] == [[lo, hi] for lo, hi in CODE_RANGES] and
            plan.get('r4')['pool_addresses'] == POOL_ADDRESSES and
            plan.get('r4')['padding_ranges'] == [[lo, hi] for lo, hi in PADDING_RANGES] and
            plan.get('r4')['initial_seeds'] == INITIAL_SEEDS and
            plan.get('r4')['missing_seed_algorithm'] ==
            'iterate_sorted_expected_starts_missing_after_initial_seeds',
            'PLAN_SCOPE')
    require(plan.get('new_function') == NEW_FUNCTION and
            plan.get('extended_function') == EXTENDED_FUNCTION and
            plan.get('shared_entry') == SHARED_ENTRY and
            plan.get('shared_interior') == SHARED_INTERIOR and
            plan.get('carve') == {
                'start': CARVE_START, 'end': CARVE_END,
                'raw': CARVE_RAW, 'data_type': 'ushort[3]'},
            'PLAN_FUNCTION_CARVE_SCOPE')
    sync = plan.get('sync_contract', {})
    require(sync.get('constants_card_info') == 5 and
            sync.get('constants_duel_field') == 2 and
            sync.get('constants_oam_attr') == 6 and
            sync.get('naming_proposals_name_cells') == 1 and
            sync.get('naming_proposals_new_rows') == 1 and
            sync.get('registry_add') == 6 and sync.get('registry_noop') == 1 and
            sync.get('inventory_function_count') == 5214 and
            sync.get('inventory_named_count') == 5124 and
            sync.get('inventory_auto_count') == 90 and
            sync.get('inventory_length_changes') == [
                {'entry': NEW_FUNCTION, 'before': 0, 'after': 1326},
                {'entry': EXTENDED_FUNCTION, 'before': 52, 'after': 2210}] and
            sync.get('inventory_paths') == [
                'temp/ghidra-functions.csv',
                'temp/ghidra-functions-renamed.txt',
                'temp/ghidra-functions-auto.txt',
                'temp/ghidra-functions-summary.md'] and
            sync.get('native_projection') == {
                'mnemonic': 2144, 'hword': 106, 'instruction_db': 2250},
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
    actual_instructions = [value for value in INSTRUCTION_ADDRESSES
                           if listing.getInstructionAt(toAddr(value)) is not None]
    if actual_instructions != INSTRUCTION_ADDRESSES:
        raise RuntimeError('R4 instruction address set incomplete')
    actual_range_starts = set()
    for lo, hi in CODE_RANGES:
        actual_range_starts.update(instruction_starts_in_range(lo, hi))
    if actual_range_starts != expected_set:
        raise RuntimeError('R4 instruction address set has extra/missing starts')
    COUNTS['R4_INSTRUCTIONS'] = len(actual_instructions)
    for value in POOL_ADDRESSES:
        clearListing(toAddr(value), toAddr(value + 3))
        listing.createData(toAddr(value), Undefined4DataType.dataType)
        COUNTS['R4_POOL_WORDS'] += 1
    clearListing(toAddr(CARVE_START), toAddr(CARVE_END - 1))
    carve_type = ArrayDataType(UnsignedShortDataType.dataType, 3, 2)
    listing.createData(toAddr(CARVE_START), carve_type)
    ensure_single_global_label(CARVE_START, REF_TARGET_NAMES[CARVE_START])
    COUNTS['CARVE_DATA'] += 1
    COUNTS['REF_TARGET_LABEL'] += 1
    for value, name in sorted(CASE_NAMES.items()):
        ensure_single_global_label(value, name)
        COUNTS['CASE_LABEL'] += 1
    for value, name in sorted(TABLE_BASES.items()):
        ensure_single_global_label(value, name)
        COUNTS['TABLE_BASE_LABEL'] += 1
    for value, row in sorted(SLOTS.items()):
        action = row['action']
        addr = toAddr(value)
        original = int(row['original_value'], 16)
        if (memory.getInt(addr) & 0xffffffff) != original:
            raise RuntimeError('ROM value changed at %08x' % value)
        if action.startswith('EQ_'):
            before = [ref_core(ref_row(ref)) for ref in references.getReferencesFrom(addr)]
            if before:
                raise RuntimeError('EQ source gained reference at %08x' % value)
            eq = equates.getEquate(row['const_or_target'])
            if eq is None:
                if action == 'EQ_PRESERVE':
                    raise RuntimeError('Preserved equate missing: ' + row['const_or_target'])
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
        elif action == 'TABLE_ENTRY_MATERIALIZE':
            expected = [ref_core(item) for item in json.loads(row['refs_from_json'])]
            if exact_ref_cores(value) != expected:
                raise RuntimeError('Table source ref changed at %08x' % value)
        else:
            raise RuntimeError('Unknown action at %08x: %s' % (value, action))
        if row['final_slot_label'] != 'none':
            ensure_single_global_label(value, row['final_slot_label'])
            COUNTS['SOURCE_LABEL'] += 1
        if row['new_eol_ascii'] != 'none':
            listing.setComment(addr, CodeUnit.EOL_COMMENT, row['new_eol_ascii'])
            COUNTS['EOL'] += 1
        COUNTS[action] += 1
    for value, row in sorted(NEW_FUNCTIONS.items()):
        body = AddressSet()
        for lo_text, hi_text in json.loads(row['final_body_ranges_json']):
            body.addRange(toAddr(int(lo_text, 16)), toAddr(int(hi_text, 16) - 1))
        fn = functions.createFunction(row['final_name'], toAddr(value), body,
                                      SourceType.USER_DEFINED)
        if fn is None:
            raise RuntimeError('New Function creation failed at %08x' % value)
        COUNTS['BODY_CREATE'] += 1
    for value, row in sorted(EXTENDED_FUNCTIONS.items()):
        fn = functions.getFunctionAt(toAddr(value))
        if fn is None or long(fn.getSymbol().getID()) != long(row['function_id']):
            raise RuntimeError('Body function identity changed at %08x' % value)
        body = AddressSet()
        for lo_text, hi_text in json.loads(row['final_body_ranges_json']):
            body.addRange(toAddr(int(lo_text, 16)), toAddr(int(hi_text, 16) - 1))
        fn.setBody(body)
        COUNTS['BODY_EXTEND'] += 1
    for value, row in sorted(RENAMES.items()):
        functions.getFunctionAt(toAddr(value)).setName(row['final_name'],
                                                        SourceType.USER_DEFINED)
        COUNTS['FUNC_RENAME'] += 1
    for value, row in sorted(PLATE_WRITES.items()):
        listing.setComment(toAddr(value), CodeUnit.PLATE_COMMENT, row['new_plate'])
        COUNTS['PLATE_WRITE'] += 1

def expected_refs(rows):
    result = json.loads(json.dumps(rows))
    approved_dynamic = (set(SLOTS) | set(CASE_NAMES) | set(TABLE_BASES) |
                        set([CARVE_START, NEW_FUNCTION, SHARED_INTERIOR]))
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

def expected_body_ref_cores(host, before=None):
    result = [] if before is None else [ref_core(item)
                                        for item in before['body_references']]
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
            if (str(ref.getReferenceType()) == 'READ' and int(ref.getOperandIndex()) == 1):
                pc_pairs.append([value, long(ref.getToAddress().getOffset())])
        target = instruction.getFallThrough()
        if target is not None:
            fallthroughs.append([value, long(target.getOffset())])
            require(long(target.getOffset()) == value + int(instruction.getLength()),
                    'R4_FALLTHROUGH_TARGET_%08x' % value)
    pre_addresses = [int(row['address'], 16) for row in pre['segment_byte_units']
                     if row['instruction_at'] is not None]
    same('R4_INSTRUCTION_ADDRESS_SET', actual_instruction_addresses,
         sorted(pre_addresses + INSTRUCTION_ADDRESSES))
    instruction_map = dict((int(row['address'], 16), row) for row in INSTRUCTION_ROWS)
    for value in INSTRUCTION_ADDRESSES:
        expected = instruction_map[value]
        require(bytes_hex(value, int(expected['length'])) == expected['raw_bytes'] and
                listing.getInstructionAt(toAddr(value)) is not None,
                'R4_INSTRUCTION_%08x' % value)
        owner = functions.getFunctionContaining(toAddr(value))
        host = HOST_BY_INSTRUCTION[value]
        owner_ok = owner is not None and long(owner.getEntryPoint().getOffset()) == host
        if host == NEW_FUNCTION:
            owner_ok = (owner_ok and unicode(owner.getName()) ==
                        PLATES[host]['final_name'] and
                        str(owner.getSymbol().getSource()) == 'USER_DEFINED')
        else:
            owner_ok = (owner_ok and long(owner.getSymbol().getID()) ==
                        long(PLATES[host]['function_id']))
        require(owner_ok, 'R4_OWNER_%08x' % value)
        context_value = currentProgram.getProgramContext().getValue(
            tmode_register, toAddr(value), False)
        require(context_value is not None and int(context_value) == 1,
                'R4_TMODE_%08x' % value)
        same('R4_SOURCE_REFS_%08x' % value, exact_ref_cores(value),
             expected_instruction_ref_cores(value))
    expected_flows = sorted([[int(row['from'], 16), int(row['to'], 16)]
                             for row in FLOW_ROWS])
    expected_pc = sorted([[int(row['from'], 16), int(row['to'], 16)]
                          for row in PC_READ_ROWS])
    same('R4_FLOW_SET', sorted(flow_pairs), expected_flows)
    same('R4_PC_READ_SET', sorted(pc_pairs), expected_pc)
    expected_fallthroughs = sorted([
        [int(row['from'], 16), int(row['to'], 16)]
        for row in FALLTHROUGH_ROWS])
    same('R4_FALLTHROUGH_SET', sorted(fallthroughs), expected_fallthroughs)
    require(len(fallthroughs) == 1616, 'R4_FALLTHROUGH_COUNT')
    for value in POOL_ADDRESSES:
        state = address_state(value)
        require(state['defined_data_at'] is not None and
                state['defined_data_at']['length'] == 4 and
                state['defined_data_at']['type'] == '/undefined4' and
                state['instruction'] is None,
                'R4_POOL_DATA_%08x' % value)
    pre_units = dict((int(row['address'], 16), row) for row in pre['segment_byte_units'])
    units = segment_byte_units()
    units_by_address = dict((int(row['address'], 16), row) for row in units)
    for lo, hi in PADDING_RANGES:
        for value in range(lo, hi):
            same('R4_PADDING_%08x' % value,
                 unit_layout_core(units_by_address[value]),
                 unit_layout_core(pre_units[value]))
    starts = [row for row in units
              if row['unit'] is not None and row['unit']['min'] == row['address'][2:]]
    same('R4_FINAL_UNIT_COUNTS', {
        'instruction_starts': sum(row['instruction_at'] is not None for row in starts),
        'data_starts': sum(row['unit']['class'] == 'DataDB' for row in starts),
        'defined_data_starts': sum(row['defined_data_at'] is not None for row in starts),
        'defined_len4': sum(row['defined_data_at'] is not None and
                            row['defined_data_at']['length'] == 4 for row in starts),
    }, {'instruction_starts': 2250, 'data_starts': 230,
        'defined_data_starts': 156, 'defined_len4': 156})
    changed = set(value for lo, hi in CODE_RANGES for value in range(lo, hi))
    changed.update(value for base in POOL_ADDRESSES for value in range(base, base + 4))
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
                actual['symbol']['source'] == 'USER_DEFINED' and
                actual['symbol']['type'] == 'Function' and
                actual['symbol']['global'] and actual['symbol']['primary'] and
                actual['namespace']['global'],
                'FUNCTION_IDENTITY_POST_%08x' % value)
        expected_plate = row['new_plate'] if value in PLATE_WRITES else before['plate']
        require(actual['plate'] == expected_plate, 'FUNCTION_PLATE_POST_%08x' % value)
        require(actual['body_ranges'] == json.loads(row['final_body_ranges_json']) and
                actual['body_size'] == int(row['final_body_size']) and
                actual['body_sha256'] == row['final_body_sha256'],
                'FUNCTION_BODY_CONTRACT_POST_%08x' % value)
        final_incoming = expected_refs(json.loads(row['final_incoming_json']))
        same('FUNCTION_INCOMING_POST_%08x' % value,
             actual['incoming'], final_incoming)
        if value == NEW_FUNCTION:
            require(actual['calling_convention'] == row['calling_convention'] and
                    actual['signature_source'] == row['signature_source'] and
                    actual['prototype'] == row['prototype'] and
                    actual['custom_variable_storage'] == bool_field(row['custom_variable_storage']) and
                    actual['varargs'] == bool_field(row['varargs']) and
                    actual['inline'] == bool_field(row['inline']) and
                    actual['no_return'] == bool_field(row['no_return']) and
                    actual['external'] == bool_field(row['external']) and
                    actual['thunk'] == bool_field(row['thunk']) and
                    actual['thunk_target'] is None and
                    actual['stack_purge_size'] == int(row['stack_purge_size']) and
                    actual['return'] == json.loads(row['return_json']) and
                    actual['parameters'] == json.loads(row['parameters_json']) and
                    actual['eol_comments'] == json.loads(row['eol_json']),
                    'NEW_FUNCTION_METADATA_POST')
            same('NEW_FUNCTION_BODY_REFS_POST',
                 [ref_core(item) for item in actual['body_references']],
                 expected_body_ref_cores(value))
            continue
        require(actual['symbol']['id'] == before['symbol']['id'],
                'FUNCTION_STATIC_ID_POST_%08x' % value)
        actual_core = function_metadata_core(actual)
        before_core = function_metadata_core(before)
        for core in (actual_core, before_core):
            core['symbol'] = dict(core['symbol'])
            core['symbol'].pop('name', None)
            core['symbol'].pop('qualified_name', None)
        actual_prototype = actual_core.pop('prototype')
        before_prototype = before_core.pop('prototype')
        expected_prototype = before_prototype
        if value in RENAMES:
            expected_prototype = before_prototype.replace(
                RENAMES[value]['current_name'], RENAMES[value]['final_name'], 1)
        require(actual_prototype == expected_prototype,
                'FUNCTION_PROTOTYPE_POST_%08x' % value)
        if value in EXTENDED_FUNCTIONS:
            for key in ('body', 'body_ranges', 'body_size', 'body_sha256', 'body_bytes'):
                actual_core.pop(key, None)
                before_core.pop(key, None)
            old_ranges = json.loads(row['body_ranges_json'])
            actual_old_refs = [item for item in actual['body_references']
                               if source_in_ranges(item['from'], old_ranges)]
            same('OLD_BODY_REFS_POST_%08x' % value, actual_old_refs,
                 expected_refs(before['body_references']))
            same('FULL_BODY_REF_CORE_POST_%08x' % value,
                 [ref_core(item) for item in actual['body_references']],
                 expected_body_ref_cores(value, before))
        else:
            same('FUNCTION_BODY_REFS_POST_%08x' % value,
                 actual['body_references'], expected_refs(before['body_references']))
        same('FUNCTION_METADATA_POST_%08x' % value, actual_core, before_core)

def expected_word_incoming(value, before):
    result = [ref_core(item) for item in before['references_to']]
    result.extend({
        'from': '%08x' % int(row['from'], 16),
        'to': '%08x' % value,
        'operand': 1,
        'type': 'READ',
        'source': 'DEFAULT',
        'primary': True,
    } for row in PC_READ_ROWS if int(row['to'], 16) == value)
    result.extend({
        'from': '%08x' % int(row['address'], 16),
        'to': '%08x' % value,
        'operand': 0,
        'type': 'DATA',
        'source': 'USER_DEFINED',
        'primary': True,
    } for row in REF_ROWS if row['action'] == 'REF_ADD' and
        int(row['original_value'], 16) == value)
    return result

def verify_word_post(value, row, actual, before):
    action = row['action']
    require(actual['bytes'] == before['bytes'] and
            actual['rom_word'] == int(row['original_value'], 16),
            'WORD_BYTES_POST_%08x' % value)
    if action == 'DISASM_WORD_TO_CODE':
        require(actual['instruction'] is not None and actual['defined_data_at'] is None and
                actual['primary_symbol']['name'] == CASE_NAMES[value] and
                not [item for item in actual['references_from'] if item['to'] == '08607cec'],
                'DISASM_WORD_POST_%08x' % value)
        return
    require(actual['defined_data_at'] is not None and
            actual['defined_data_at']['length'] == 4,
            'WORD_DATA_POST_%08x' % value)
    expected_label = row['final_slot_label']
    if expected_label == 'none':
        require(actual['symbol_count'] == 0, 'WORD_NO_LABEL_POST_%08x' % value)
    else:
        require(actual['symbol_count'] == 1 and actual['primary_symbol']['name'] == expected_label and
                actual['primary_symbol']['source'] == 'USER_DEFINED' and
                actual['primary_symbol']['primary'] and actual['primary_symbol']['global'],
                'WORD_LABEL_POST_%08x' % value)
        primary_id = actual['primary_symbol']['id']
        primary_name = actual['primary_symbol']['qualified_name']
        require(all(item['target_primary_id'] == primary_id and
                    item['target_primary_name'] == primary_name
                    for item in actual['references_to']),
                'WORD_READ_DERIVED_POST_%08x' % value)
    require(actual['eol'] == row['new_eol_ascii'], 'WORD_EOL_POST_%08x' % value)
    same('WORD_READ_CORE_POST_%08x' % value,
         [ref_core(item) for item in actual['references_to']],
         expected_word_incoming(value, before))
    source_cores = [ref_core(item) for item in actual['references_from']]
    if action.startswith('EQ_'):
        same('EQ_SET_POST_%08x' % value, actual['equates'],
             [{'name': row['const_or_target'],
               'value': int(row['original_value'], 16)}])
        require(source_cores == [], 'EQ_REF_POST_%08x' % value)
    elif action == 'REF_ADD':
        require(actual['equates'] == [], 'REF_EQ_POST_%08x' % value)
        same('REF_ADD_POST_%08x' % value, source_cores,
             [{'from': '%08x' % value, 'to': '%08x' % int(row['original_value'], 16),
               'operand': 0, 'type': 'DATA', 'source': 'USER_DEFINED',
               'primary': True}])
    elif action == 'REF_PRESERVE':
        require(actual['equates'] == [], 'REF_PRESERVE_EQ_POST_%08x' % value)
        same('REF_PRESERVE_POST_%08x' % value, source_cores,
             [ref_core(item) for item in before['references_from']])
    elif action == 'TABLE_ENTRY_MATERIALIZE':
        require(actual['equates'] == [], 'TABLE_EQ_POST_%08x' % value)
        same('TABLE_SOURCE_CORE_POST_%08x' % value, source_cores,
             [ref_core(item) for item in before['references_from']])
        primary = symbols.getPrimarySymbol(toAddr(int(row['original_value'], 16)))
        require(len(actual['references_from']) == 1 and primary is not None and
                actual['references_from'][0]['target_primary_id'] == long(primary.getID()) and
                actual['references_from'][0]['target_primary_name'] == unicode(primary.getName(True)),
                'TABLE_DERIVED_POST_%08x' % value)
    elif action == 'RENAME':
        require(actual['equates'] == [] and source_cores ==
                [ref_core(item) for item in before['references_from']],
                'RENAME_POST_%08x' % value)

def verify_post(pre):
    require(int(pre['function_count']) == FUNCTION_COUNT and
            int(functions.getFunctionCount()) == FINAL_FUNCTION_COUNT,
            'FUNCTION_COUNT_POST')
    require(raw_hash(SEGMENT_START, SEGMENT_END) == pre['segment']['sha256'] == SEGMENT_SHA256,
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
    pre_cases = dict((int(row['address'], 16), row)
                     for row in pre['case_targets'])
    for value, name in sorted(CASE_NAMES.items()):
        state = address_state(value)
        require(state['symbol_count'] == 1 and state['primary_symbol']['name'] == name and
                state['primary_symbol']['source'] == 'USER_DEFINED' and
                state['primary_symbol']['type'] == 'Label' and
                state['primary_symbol']['global'] and state['primary_symbol']['primary'],
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
    pre_targets = dict((int(row['address'], 16), row) for row in pre['targets'])
    for value in RAM_TARGETS:
        actual = address_state(value)
        before = pre_targets[value]
        additions = [{'from': '%08x' % int(row['address'], 16),
                      'to': '%08x' % value, 'operand': 0, 'type': 'DATA',
                      'source': 'USER_DEFINED', 'primary': True}
                     for row in REF_ROWS if row['action'] == 'REF_ADD' and
                     int(row['original_value'], 16) == value]
        same('RAM_REFS_TO_POST_%08x' % value,
             [ref_core(item) for item in actual['references_to']],
             [ref_core(item) for item in before['references_to']] + additions)
        require(actual['primary_symbol']['id'] == before['primary_symbol']['id'] and
                actual['primary_symbol']['name'] == before['primary_symbol']['name'] and
                actual['primary_symbol']['source'] == before['primary_symbol']['source'] and
                actual['bytes'] is None and before['bytes'] is None,
                'RAM_STATIC_POST_%08x' % value)
    shared_before = pre['shared_interior']
    shared = address_state(SHARED_INTERIOR)
    primary = shared['primary_symbol']
    expected_interior = SHARED_INTERIOR_CONTRACT
    require(shared['symbol_count'] == 1 and primary is not None and
            primary['name'] == expected_interior['final_primary']['expected_name'] and
            primary['type'] == 'Label' and primary['source'] == 'DEFAULT' and
            primary['primary'] and primary['global'] and primary['id'] != 16954 and
            shared['function'] is None and
            shared['function_containing']['id'] == 16954 and
            shared['function_containing']['entry'] == '080aa10c',
            'SHARED_INTERIOR_PRIMARY_POST')
    same('SHARED_INTERIOR_INCOMING_POST',
         [ref_core(item) for item in shared['references_to']],
         [dict(item, **{
             'from': item['from'][2:], 'to': item['to'][2:]})
          for item in expected_interior['incoming']])
    for key in ('bytes', 'rom_word', 'data_at', 'defined_data_at',
                'data_containing', 'instruction', 'function',
                'function_containing', 'references_from', 'equates', 'eol', 'plate'):
        same('SHARED_INTERIOR_PRESERVE_' + key,
             shared[key], shared_before[key])
    pre_callees = dict((int(row['address'], 16), row)
                       for row in pre['direct_callee_targets'])
    for value, before in sorted(pre_callees.items()):
        actual = address_state(value)
        additions = [row for row in FLOW_REF_ROWS if int(row['to'], 16) == value]
        same('CALLEE_INCOMING_CORE_POST_%08x' % value,
             [ref_core(item) for item in actual['references_to']],
             [ref_core(item) for item in before['references_to']] + additions)
    carve_before = dict((int(row['address'], 16), row)
                        for row in pre['carve']['states'])
    for value in (0x09e478c0, 0x09e478c4, 0x09e478ce, 0x09e478d0):
        same('CARVE_BOOKEND_POST_%08x' % value,
             address_state(value), carve_before[value])
    carve = address_state(CARVE_START)
    carve_additions = [{
        'from': '%08x' % int(row['address'], 16),
        'to': '%08x' % CARVE_START, 'operand': 0, 'type': 'DATA',
        'source': 'USER_DEFINED', 'primary': True,
    } for row in REF_ROWS if row['action'] == 'REF_ADD' and
        int(row['original_value'], 16) == CARVE_START]
    require(carve['bytes'] == CARVE_RAW[:8] and carve['symbol_count'] == 1 and
            carve['primary_symbol']['name'] == REF_TARGET_NAMES[CARVE_START] and
            carve['primary_symbol']['source'] == 'USER_DEFINED' and
            carve['primary_symbol']['global'] and carve['primary_symbol']['primary'] and
            carve['defined_data_at'] is not None and
            carve['defined_data_at']['length'] == 6 and
            carve['defined_data_at']['type'].endswith('ushort[3]') and
            carve['instruction'] is None and carve['references_from'] == [],
            'CARVE_DATA_POST')
    same('CARVE_INCOMING_POST',
         [ref_core(item) for item in carve['references_to']], carve_additions)
    if MODE == 'apply':
        same('APPLY_COUNTS', COUNTS, EXPECTED_COUNTS)

print('=== RefineF14Seg2 mode=%s ===' % MODE)
verify_inputs()
reject('INPUTS')

if MODE == 'prestate':
    state = capture()
    verify_prestate(state)
    reject('PRESTATE')
    write_json(PRESTATE_NAME, state)
    print('PRESTATE plate_functions=7 observer_functions=173 slots=156 targets=%d '
          'table_sources=15 cases=11 bases=2 odd=%d direct_callees=%d '
          'segment_bytes=5360 FAIL=0' %
          (len(state['targets']), len(ODD_TARGETS), len(DIRECT_CALLEE_TARGETS)))
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
            'status': 'F14_SEG2_DRY_PREFLIGHT_OK', 'FAIL': 0,
            'script_sha256': file_hash(getSourceFile().getAbsolutePath()),
            'plan_sha256': file_hash(run_path(PLAN_NAME)),
            'prestate_sha256': prestate_hash,
            'source_snapshot_manifest_sha256': file_hash(run_path(SOURCE_SNAPSHOT_NAME)),
            'counts': EXPECTED_COUNTS,
            'preflight': {
                'plate_functions': 7, 'observer_functions': 173,
                'slots': 156, 'ref_targets': len(REF_TARGETS),
                'table_sources': 15, 'case_targets': 11, 'table_bases': 2,
                'odd_targets': len(ODD_TARGETS),
                'direct_callees': len(DIRECT_CALLEE_TARGETS),
                'segment_bytes': 5360, 'r4_instructions': 1699,
                'r4_pc_reads': 126, 'r4_flows': 248,
                'r4_calls': 43, 'r4_fallthroughs_final': 1616,
                'new_function': NEW_FUNCTION,
                'extended_function': EXTENDED_FUNCTION,
            },
            'semantic_actions_applied': False,
        }
        write_json('f14-seg2-dry-result-v2.json', result)
        print('PREFLIGHT slots=156 EQ=104 REF=37 TABLE=15 FUNC_RENAME=1 '
              'FUNC_CREATE=1 FUNC_EXTEND=1 PLATE_WRITE=6 R4=1699 FAIL=0')
        print('STATUS: OK mode=dry FAIL=0 semantic_actions_applied=false')
    elif MODE == 'check':
        verify_post(prestate)
        reject('PERSISTED_CHECK')
        write_json('f14-seg2-persisted-check-v2.json', {
            'status': 'F14_SEG2_PERSISTED_CHECK_OK', 'FAIL': 0,
            'script_sha256': file_hash(getSourceFile().getAbsolutePath()),
            'plan_sha256': file_hash(run_path(PLAN_NAME)),
            'prestate_sha256': prestate_hash,
        })
        print('STATUS: OK mode=check FAIL=0 read_only=true')
    else:
        verify_prestate(prestate)
        reject('APPLY_PRESTATE')
        transaction = currentProgram.startTransaction('F14-Seg-2 approved materialization')
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
            write_json('f14-seg2-apply-failures-v2.json', {
                'status': 'FAIL_ROLLED_BACK', 'FAIL': len(FAILS),
                'error': error_text, 'failures': FAILS,
                'transaction_committed': False,
            })
            raise RuntimeError('F14-Seg-2 apply rolled back')
        write_json('f14-seg2-apply-receipt-v2.json', {
            'status': 'F14_SEG2_APPLY_OK', 'FAIL': 0,
            'script_sha256': file_hash(getSourceFile().getAbsolutePath()),
            'plan_sha256': file_hash(run_path(PLAN_NAME)),
            'prestate_sha256': prestate_hash, 'counts': COUNTS,
            'dynamic_counts': DYNAMIC_COUNTS,
            'transaction_committed': True,
        })
        print('STATUS: OK mode=apply FAIL=0 transaction_committed=true')

