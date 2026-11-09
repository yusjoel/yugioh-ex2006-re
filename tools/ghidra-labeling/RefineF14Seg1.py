# -*- coding: ascii -*-
#@runtime Jython
#@category Ygo-ex2006.Refine
# F14-Seg-1 PASS materialization. prestate/dry/check are read-only.

import csv
import hashlib
import json
import os
import re

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.address import AddressSet
from ghidra.program.model.data import Undefined4DataType
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import RefType, SourceType
from java.math import BigInteger

ARGS = list(getScriptArgs())
MODE = ARGS[0].lower() if ARGS else 'dry'
if MODE not in ('prestate', 'dry', 'apply', 'check'):
    raise RuntimeError('Expected prestate, dry, apply, or check')

ROOT = os.path.abspath(os.path.join(str(getSourceFile().getParentFile()), '..', '..'))
RUN = os.path.join(ROOT, 'output', 'refine-run-20261028-105948')
PLAN_NAME = 'f14-seg1-plan-v4.json'
PRESTATE_NAME = 'f14-seg1-fresh-full-prestate-v4.json'
SOURCE_SNAPSHOT_NAME = 'f14-seg1-source-snapshot-preapply-v4.json'
FREEZE_MANIFEST_NAME = 'f14-seg1-freeze-manifest.json'
MAP_NAME = 'f14-seg1-r4-map.json'
MACHINE_CONTRACT_NAME = 'f14-seg1-mode-a-machine-contract.json'
BODY_CONTRACT_NAME = 'root-f14-seg1-body-contract.json'
DB_BACKUP_MANIFEST_NAME = 'root-f14-db-backup.json'

INPUT_HASHES = {
    'doc/dev/refine/F14-Seg-1.proposal.md': '3dbf8f8761d96475b7926453187077271fb84f801d85bfe2f62152cbb5ca98c4',
    'doc/dev/refine/F14-Seg-1.review.md': 'd2e3825448c959bac78b8b97fbdcc8a831c710475cb91d994b7892e5de72f528',
    'doc/dev/refine/F14-Seg-1.slots.tsv': '30f286050966b3c97edfd2e3d2df0fbe3279a5cef8b363b29e1dda93d9e98693',
    'doc/dev/refine/F14-Seg-1.plates.tsv': '7b12e7ae523ca9892f08ec23fbfc019f5672b199cfd15eafbfc740fb054325d3',
    'output/refine-run-20261028-105948/f14-seg1-freeze-manifest.json': '22e9c676efe950c1ecbc31d4c189950160464035d8c6f86635ff72faf769bf56',
    'output/refine-run-20261028-105948/f14-seg1-mode-a-machine-contract.json': 'ec45253613c2ed2f2ee524c40e5947bb3f515c8e49790a1dfe84d59708ed3057',
    'output/refine-run-20261028-105948/f14-seg1-review-round2-audit.json': '037207f3345b2e0cbbf95eee51d8ac1c5176c03ed26d1ab002bc2ec6c077fe9a',
    'output/refine-run-20261028-105948/f14-seg1-r4-map.json': '6f2ec82b4156dc7b4fb754b75ee986d30ddf806148ceb9d12584abb81021dad2',
    'output/refine-run-20261028-105948/root-f14-seg1-body-contract.json': '62cc7be116469adc3b8ec16702a7890459f44a7338b21a4cf9a97813bde2d89a',
    'output/refine-run-20261028-105948/root-f14-seg1-external-alias-baseline-v2.json': 'e4275f3865d2a157d62f3a23782b3f1a09dd4ad64f1035923bbade5ed2fd045c',
}
EXPECTED_COUNTS = {
    'EQ_ADD': 61, 'EQ_PRESERVE': 2,
    'REF_ADD': 64, 'REF_PRESERVE': 13,
    'RENAME': 1, 'TABLE_ENTRY_MATERIALIZE': 25,
    'DISASM_WORD_TO_CODE': 1, 'EOL': 166,
    'SOURCE_LABEL': 144, 'CASE_LABEL': 17, 'TABLE_BASE_LABEL': 3,
    'FUNC_RENAME': 10, 'PLATE_WRITE': 13,
    'EXTERNAL_ALIAS_EQ_RENAME': 3, 'EXTERNAL_ALIAS_EOL': 3,
    'R4_CODE_RANGES': 18, 'R4_INSTRUCTIONS': 482,
    'R4_SUPPLEMENTAL_SEEDS': 3,
    'R4_POOL_WORDS': 36, 'BODY_RESIZE': 3,
}
SEGMENT_START = 0x080a78dc
SEGMENT_END = 0x080a8c30
SEGMENT_SHA256 = '2bbb97bc594e282de434db73d11ce431952cd727e56d7fc88285e239b2927822'
FUNCTION_COUNT = 5213
BOGUS_WORD = 0x080a7928
BOGUS_TARGET = 0x08607cec
EXTERNAL_ALIAS_RENAMES = {
    0x080a3cb0: (
        'check_equip_target_slot_eligible_by_field6_eq17_1',
        'check_uria_tribute_slot_eligible_1'),
    0x080a3cbc: (
        'check_equip_target_slot_eligible_by_field9_eq4_field6_eq16_1',
        'check_hamon_tribute_slot_eligible_1'),
    0x080a3cfc: (
        'check_equip_target_slot_eligible_by_whitelist_or_special_1',
        'check_anteatereatingant_tribute_slot_eligible_1'),
}

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
        write_json('f14-seg1-%s-failures.json' % MODE,
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
    }

def ref_core(row):
    return dict((key, row[key]) for key in
                ('from', 'to', 'operand', 'type', 'source', 'primary'))

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

SLOT_ROWS = read_tsv('doc/dev/refine/F14-Seg-1.slots.tsv')
PLATE_ROWS = read_tsv('doc/dev/refine/F14-Seg-1.plates.tsv')
R4_MAP = read_json(MAP_NAME)
MACHINE_CONTRACT = read_json(MACHINE_CONTRACT_NAME)
BODY_CONTRACT = read_json(BODY_CONTRACT_NAME)
SLOTS = dict((int(row['address'], 16), row) for row in SLOT_ROWS)
PLATES = dict((int(row['entry'], 16), row) for row in PLATE_ROWS)
RENAMES = dict((value, row) for value, row in PLATES.items()
               if row['current_name'] != row['final_name'])
PLATE_WRITES = dict((value, row) for value, row in PLATES.items()
                    if row['action'] != 'PRESERVE')
FUNCTIONS = sorted(PLATES)
TABLE_ROWS = [row for row in SLOT_ROWS if row['action'] == 'TABLE_ENTRY_MATERIALIZE']
TABLE_SOURCES = sorted(int(row['address'], 16) for row in TABLE_ROWS)
CASE_NAMES = dict((int(row['original_value'], 16), row['target_final_label'])
                  for row in TABLE_ROWS)
TABLE_BASES = dict((int(row['address'], 16), row['final_slot_label'])
                   for row in TABLE_ROWS if row['final_slot_label'] != 'none')
REF_ROWS = [row for row in SLOT_ROWS if row['action'].startswith('REF_')]
REF_TARGETS = sorted(set(int(row['original_value'], 16) for row in REF_ROWS))
RAM_TARGETS = sorted(value for value in REF_TARGETS if value < 0x08000000)
ODD_TARGETS = sorted(set(int(row['original_value'], 16) for row in SLOT_ROWS
                         if row['action'].startswith('EQ_') and
                         0x08000000 <= int(row['original_value'], 16) < 0x0a000000 and
                         int(row['original_value'], 16) & 1))
ODD_FUNCTIONS = sorted(set(value - 1 for value in ODD_TARGETS))
CODE_RANGES = []
SUPPLEMENTAL_SEEDS = [0x080a835e, 0x080a874a, 0x080a8750]
SUPPLEMENTAL_NEW_COUNTS = {0x080a835e: 18, 0x080a874a: 3, 0x080a8750: 66}
POOL_ADDRESSES = []
PADDING_RANGES = []
INSTRUCTION_ROWS = []
FLOW_ROWS = []
PC_READ_ROWS = []
HOST_BY_INSTRUCTION = {}
for layout in R4_MAP['layouts']:
    host = int(layout['host_function'], 16)
    for item in layout['code_ranges']:
        CODE_RANGES.append((int(item[0], 16), int(item[1], 16)))
    for row in layout['literal_words']:
        POOL_ADDRESSES.append(int(row['address'], 16))
    for row in layout['padding']:
        lo = int(row['address'], 16)
        PADDING_RANGES.append((lo, lo + int(row['length'])))
    for row in layout['instructions']:
        value = int(row['address'], 16)
        INSTRUCTION_ROWS.append(row)
        HOST_BY_INSTRUCTION[value] = host
    FLOW_ROWS.extend(layout['direct_flows'])
    PC_READ_ROWS.extend(layout['pc_literal_reads'])
INSTRUCTION_ADDRESSES = sorted(int(row['address'], 16) for row in INSTRUCTION_ROWS)
POOL_ADDRESSES = sorted(POOL_ADDRESSES)
DIRECT_CALLEE_TARGETS = sorted(set(int(row['to'], 16) for row in FLOW_ROWS
                                   if row['kind'] == 'CALL'))
BODY_ROWS = dict((int(row['entry'], 16), row) for row in BODY_CONTRACT['functions'])

def freeze_manifest_path(relative):
    return path_in_root(relative)

def verify_inputs():
    for relative, digest in sorted(INPUT_HASHES.items()):
        same('INPUT_HASH_' + relative, file_hash(path_in_root(relative)), digest)
    manifest = read_json(FREEZE_MANIFEST_NAME)
    require(len(manifest.get('files', {})) == 17, 'FREEZE_MANIFEST_ENTRY_COUNT')
    for relative, digest in sorted(manifest.get('files', {}).items()):
        same('FREEZE_MANIFEST_HASH_' + relative,
             file_hash(freeze_manifest_path(relative)), digest)
    basis = manifest.get('review_basis', {})
    require(basis.get('active_review_in_hash_inputs') is False and
            file_hash(path_in_root(basis['path'])) == basis['sha256'],
            'ARCHIVED_REVIEW_BASIS')
    require(len(SLOTS) == 167 and len(SLOT_ROWS) == 167 and
            len(PLATES) == 14 and len(FUNCTIONS) == 14 and
            len(RENAMES) == 10 and len(PLATE_WRITES) == 13,
            'PRIMARY_INPUT_COUNTS')
    action_counts = {}
    for row in SLOT_ROWS:
        action_counts[row['action']] = action_counts.get(row['action'], 0) + 1
    same('SLOT_ACTION_COUNTS', action_counts,
         {'EQ_ADD': 61, 'EQ_PRESERVE': 2, 'REF_ADD': 64,
          'REF_PRESERVE': 13, 'RENAME': 1,
          'TABLE_ENTRY_MATERIALIZE': 25, 'DISASM_WORD_TO_CODE': 1})
    require(len(TABLE_SOURCES) == 25 and len(CASE_NAMES) == 17 and
            len(TABLE_BASES) == 3 and len(REF_TARGETS) == 9,
            'REFERENCE_SCOPE_COUNTS')
    require(len(CODE_RANGES) == 18 and len(INSTRUCTION_ADDRESSES) == 482 and
            len(POOL_ADDRESSES) == 36 and len(PADDING_RANGES) == 9 and
            len(FLOW_ROWS) == 54 and len(PC_READ_ROWS) == 39 and
            sum(hi - lo for lo, hi in CODE_RANGES) == 1006,
            'R4_SCOPE_COUNTS')
    require(SUPPLEMENTAL_SEEDS == [0x080a835e, 0x080a874a, 0x080a8750] and
            SUPPLEMENTAL_NEW_COUNTS == {
                0x080a835e: 18, 0x080a874a: 3, 0x080a8750: 66} and
            all(value in INSTRUCTION_ADDRESSES for value in SUPPLEMENTAL_SEEDS) and
            [(lo, hi) for value in SUPPLEMENTAL_SEEDS for lo, hi in CODE_RANGES
             if lo <= value < hi] == [
                (0x080a8358, 0x080a838a),
                (0x080a8718, 0x080a87d8),
                (0x080a8718, 0x080a87d8)],
            'R4_SUPPLEMENTAL_SEED_SCOPE')
    require(MACHINE_CONTRACT['switch_contract']['source_entries'] == 25 and
            MACHINE_CONTRACT['switch_contract']['total_unique_targets'] == 17 and
            MACHINE_CONTRACT['switch_contract']['new_r4_targets'] == 16 and
            MACHINE_CONTRACT['switch_contract']['existing_tail'] == '0x080a87e0',
            'SWITCH_MACHINE_CONTRACT')
    require(len(BODY_ROWS) == 3 and sorted(BODY_ROWS) ==
            [0x080a78dc, 0x080a81fc, 0x080a85d0], 'BODY_CONTRACT_COUNT')
    require(len(EXTERNAL_ALIAS_RENAMES) == 3, 'EXTERNAL_ALIAS_COUNT')
    source_names = [row['final_slot_label'] for row in SLOT_ROWS
                    if row['final_slot_label'] != 'none']
    require(len(source_names) == 144 and len(set(source_names)) == 144,
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
    for value, row in sorted(PLATE_WRITES.items()):
        text = row['new_plate']
        require(all(ord(char) < 128 for char in text) and len(text) <= 500 and
                len(text) == int(row['new_plate_chars']),
                'PLATE_ASCII_%08x' % value)
    for value, names in sorted(EXTERNAL_ALIAS_RENAMES.items()):
        old_name, new_name = names
        old_eq = equates.getEquate(old_name)
        new_eq = equates.getEquate(new_name)
        if MODE == 'check':
            expected_value = long(memory.getInt(toAddr(value))) & 0xffffffff
            expected_refs = [{'address': '%08x' % value, 'operand': 0}]
            new_contract = equate_global_row(new_name)
            require(old_eq is None and new_eq is not None and
                    new_contract is not None and
                    new_contract['value'] == expected_value and
                    new_contract['references'] == expected_refs,
                    'EXTERNAL_ALIAS_POST_INPUT_%08x' % value)
        else:
            require(old_eq is not None and new_eq is None,
                    'EXTERNAL_ALIAS_PRE_%08x' % value)
    for value, row in sorted(RENAMES.items()):
        collisions = [item for item in symbols.getGlobalSymbols(row['final_name'])
                      if item.getAddress() != toAddr(value)]
        require(not collisions, 'FUNCTION_NAME_COLLISION_%08x' % value)

def capture():
    target_addresses = sorted(set(REF_TARGETS + list(CASE_NAMES) + list(TABLE_BASES)))
    direct_functions = sorted(set(value for value in DIRECT_CALLEE_TARGETS
                                  if functions.getFunctionAt(toAddr(value)) is not None))
    return {
        'status': 'F14_SEG1_FRESH_FULL_PRESTATE',
        'program_name': unicode(currentProgram.getName()),
        'function_count': int(functions.getFunctionCount()),
        'segment': {'start': '0x%08x' % SEGMENT_START,
                    'end': '0x%08x' % SEGMENT_END,
                    'size': SEGMENT_END - SEGMENT_START,
                    'sha256': raw_hash(SEGMENT_START, SEGMENT_END)},
        'functions': [function_row(value) for value in FUNCTIONS],
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
        'external_alias_sources': [address_state(value)
                                   for value in sorted(EXTERNAL_ALIAS_RENAMES)],
        'external_alias_equates': [equate_global_row(EXTERNAL_ALIAS_RENAMES[value][0])
                                   for value in sorted(EXTERNAL_ALIAS_RENAMES)],
        'bogus_target': address_state(BOGUS_TARGET),
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
    }, {'instruction_starts': 1540, 'data_starts': 1347,
        'defined_data_starts': 131, 'bytes': 4948})
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
        same('SLOT_REFS_FROM_%08x' % value, state['references_from'],
             json.loads(row['refs_from_json']))
        same('SLOT_REFS_TO_%08x' % value, state['references_to'],
             json.loads(row['refs_to_json']))
        same('SLOT_EQUATES_%08x' % value, state['equates'],
             json.loads(row['equates_json']))
        same('SLOT_EOL_%08x' % value, state['eol'],
             json.loads(row['old_eol_json']))
        data_contract_from_tsv(state, row, value)
    pre_functions = dict((int(row['entry'], 16), row) for row in pre['functions'])
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
                state['primary_symbol']['primary'],
                'CASE_DYNAMIC_PRE_%08x' % value)
    for state in pre['ram_targets']:
        require(state['bytes'] is None and state['primary_symbol'] is not None and
                state['primary_symbol']['source'] == 'USER_DEFINED',
                'RAM_TARGET_PRE_' + state['address'])
    for state in pre['odd_targets']:
        require(state['defined_data_at'] is None and state['references_from'] == [],
                'ODD_TARGET_PRE_' + state['address'])
    alias_states = dict((int(row['address'], 16), row)
                        for row in pre['external_alias_sources'])
    alias_equates = dict((row['name'], row) for row in pre['external_alias_equates'])
    for value, names in sorted(EXTERNAL_ALIAS_RENAMES.items()):
        old_name, new_name = names
        state = alias_states[value]
        eq = alias_equates[old_name]
        require(state['defined_data_at'] is not None and
                state['defined_data_at']['length'] == 4 and
                state['equates'] == [{'name': old_name, 'value': state['rom_word']}] and
                old_name in state['eol'] and new_name not in state['eol'] and
                eq['value'] == state['rom_word'] and
                eq['references'] == [{'address': '%08x' % value, 'operand': 0}],
                'EXTERNAL_ALIAS_COMPLETE_PRE_%08x' % value)
    bogus = pre_slots[BOGUS_WORD]
    same('BOGUS_REF_PRE', [ref_core(item) for item in bogus['references_from']],
         [{'from': '080a7928', 'to': '08607cec', 'operand': 0,
           'type': 'DATA', 'source': 'DEFAULT', 'primary': True}])
    for row in INSTRUCTION_ROWS:
        value = int(row['address'], 16)
        require(bytes_hex(value, int(row['length'])) == row['raw_bytes'],
                'R4_ROM_BYTES_PRE_%08x' % value)
    for row in [item for layout in R4_MAP['layouts'] for item in layout['literal_words']]:
        value = int(row['address'], 16)
        require(bytes_hex(value, 4) == row['raw_bytes'],
                'R4_POOL_BYTES_PRE_%08x' % value)

def verify_plan(plan, prestate_hash):
    require(plan.get('status') == 'F14_SEG1_PLAN_FROZEN', 'PLAN_STATUS')
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
            plan.get('r4')['supplemental_seeds'] == SUPPLEMENTAL_SEEDS,
            'PLAN_SCOPE')
    sync = plan.get('sync_contract', {})
    require(sync.get('naming_proposals_name_cells') == 10 and
            sync.get('registry_add') == 11 and sync.get('registry_update') == 3 and
            sync.get('inventory_function_count') == 5213 and
            sync.get('inventory_named_count') == 5123 and
            sync.get('inventory_auto_count') == 90 and
            sync.get('inventory_length_changes') == [
                {'entry': 0x080a78dc, 'before': 48, 'after': 386},
                {'entry': 0x080a81fc, 'before': 58, 'after': 336},
                {'entry': 0x080a85d0, 'before': 46, 'after': 436}],
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
    pre_bogus = exact_ref_cores(BOGUS_WORD)
    expected_bogus = [{'from': '080a7928', 'to': '08607cec', 'operand': 0,
                       'type': 'DATA', 'source': 'DEFAULT', 'primary': True}]
    if pre_bogus != expected_bogus:
        raise RuntimeError('Bogus source reference contract changed')
    for lo, hi in CODE_RANGES:
        clearListing(toAddr(lo), toAddr(hi - 1))
        context.setValue(tmode_register, toAddr(lo), toAddr(hi - 1), BigInteger.ONE)
        command = DisassembleCommand(toAddr(lo), AddressSet(toAddr(lo), toAddr(hi - 1)), True)
        if not command.applyTo(currentProgram):
            raise RuntimeError('Disassembly failed [%08x,%08x)' % (lo, hi))
        COUNTS['R4_CODE_RANGES'] += 1
    for value in SUPPLEMENTAL_SEEDS:
        ranges = [(lo, hi) for lo, hi in CODE_RANGES if lo <= value < hi]
        if len(ranges) != 1 or listing.getInstructionAt(toAddr(value)) is not None:
            raise RuntimeError('Supplemental seed precondition at %08x' % value)
        lo, hi = ranges[0]
        before = instruction_starts_in_range(lo, hi)
        command = DisassembleCommand(toAddr(value),
                                     AddressSet(toAddr(lo), toAddr(hi - 1)), True)
        if not command.applyTo(currentProgram):
            raise RuntimeError('Supplemental disassembly failed at %08x' % value)
        after = instruction_starts_in_range(lo, hi)
        additions = after - before
        if (value not in after or len(additions) != SUPPLEMENTAL_NEW_COUNTS[value] or
                not additions.issubset(set(INSTRUCTION_ADDRESSES))):
            raise RuntimeError('Supplemental seed result at %08x' % value)
        COUNTS['R4_SUPPLEMENTAL_SEEDS'] += 1
    actual_instructions = [value for value in INSTRUCTION_ADDRESSES
                           if listing.getInstructionAt(toAddr(value)) is not None]
    if actual_instructions != INSTRUCTION_ADDRESSES:
        raise RuntimeError('R4 instruction address set incomplete')
    COUNTS['R4_INSTRUCTIONS'] = len(actual_instructions)
    if exact_ref_cores(BOGUS_WORD):
        raise RuntimeError('Bogus DATA reference survived code disassembly')
    for value in POOL_ADDRESSES:
        clearListing(toAddr(value), toAddr(value + 3))
        listing.createData(toAddr(value), Undefined4DataType.dataType)
        COUNTS['R4_POOL_WORDS'] += 1
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
        if action == 'DISASM_WORD_TO_CODE':
            COUNTS[action] += 1
            continue
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
            if action == 'EQ_ADD' and not matches:
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
        elif action == 'RENAME':
            if exact_ref_cores(value) or list(equates.getEquates(addr)):
                raise RuntimeError('RENAME slot has semantic object at %08x' % value)
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
    for value, contract in sorted(BODY_ROWS.items()):
        fn = functions.getFunctionAt(toAddr(value))
        if fn is None or long(fn.getSymbol().getID()) != long(PLATES[value]['function_id']):
            raise RuntimeError('Body function identity changed at %08x' % value)
        body = AddressSet()
        for lo_text, hi_text in contract['canonical_ranges']:
            body.addRange(toAddr(int(lo_text, 16)), toAddr(int(hi_text, 16) - 1))
        fn.setBody(body)
        COUNTS['BODY_RESIZE'] += 1
    for value, row in sorted(RENAMES.items()):
        functions.getFunctionAt(toAddr(value)).setName(row['final_name'],
                                                        SourceType.USER_DEFINED)
        COUNTS['FUNC_RENAME'] += 1
    for value, row in sorted(PLATE_WRITES.items()):
        listing.setComment(toAddr(value), CodeUnit.PLATE_COMMENT, row['new_plate'])
        COUNTS['PLATE_WRITE'] += 1
    for value, names in sorted(EXTERNAL_ALIAS_RENAMES.items()):
        old_name, new_name = names
        old_eq = equates.getEquate(old_name)
        if old_eq is None or equates.getEquate(new_name) is not None:
            raise RuntimeError('External alias equate precondition at %08x' % value)
        old_refs = list(old_eq.getReferences())
        if (len(old_refs) != 1 or old_refs[0].getAddress() != toAddr(value) or
                int(old_refs[0].getOpIndex()) != 0):
            raise RuntimeError('External alias equate reference scope at %08x' % value)
        old_value = long(old_eq.getValue()) & 0xffffffff
        new_eq = equates.createEquate(new_name, old_value)
        new_eq.addReference(toAddr(value), 0)
        old_eq.removeReference(toAddr(value), 0)
        equates.removeEquate(old_name)
        COUNTS['EXTERNAL_ALIAS_EQ_RENAME'] += 1
        old_eol = listing.getComment(CodeUnit.EOL_COMMENT, toAddr(value))
        if old_eol is None or old_eol.count(old_name) != 1 or new_name in old_eol:
            raise RuntimeError('External alias EOL precondition at %08x' % value)
        listing.setComment(toAddr(value), CodeUnit.EOL_COMMENT,
                           old_eol.replace(old_name, new_name))
        COUNTS['EXTERNAL_ALIAS_EOL'] += 1

def expected_refs(rows):
    result = json.loads(json.dumps(rows))
    approved_dynamic = set(SLOTS) | set(CASE_NAMES) | set(TABLE_BASES)
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
        require(owner is not None and long(owner.getEntryPoint().getOffset()) == host and
                long(owner.getSymbol().getID()) == long(PLATES[host]['function_id']),
                'R4_OWNER_%08x' % value)
        context_value = currentProgram.getProgramContext().getValue(
            tmode_register, toAddr(value), False)
        require(context_value is not None and int(context_value) == 1,
                'R4_TMODE_%08x' % value)
    expected_flows = sorted([[int(row['from'], 16), int(row['to'], 16)]
                             for row in FLOW_ROWS])
    expected_pc = sorted([[int(row['from'], 16), int(row['to'], 16)]
                          for row in PC_READ_ROWS])
    same('R4_FLOW_SET', sorted(flow_pairs), expected_flows)
    same('R4_PC_READ_SET', sorted(pc_pairs), expected_pc)
    require(len(fallthroughs) == 461, 'R4_FALLTHROUGH_COUNT')
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
    }, {'instruction_starts': 2022, 'data_starts': 236,
        'defined_data_starts': 166, 'defined_len4': 166})
    changed = set(value for lo, hi in CODE_RANGES for value in range(lo, hi))
    changed.update(value for base in POOL_ADDRESSES for value in range(base, base + 4))
    for row in units:
        value = int(row['address'], 16)
        if value not in changed:
            same('UNIT_STATIC_POST_%08x' % value,
                 unit_layout_core(row), unit_layout_core(pre_units[value]))

def verify_function_post(pre):
    pre_functions = dict((int(row['entry'], 16), row) for row in pre['functions'])
    for value, row in sorted(PLATES.items()):
        actual = function_row(value)
        before = pre_functions[value]
        require(actual['name'] == row['final_name'] and
                actual['symbol']['id'] == before['symbol']['id'] and
                actual['symbol']['source'] == 'USER_DEFINED',
                'FUNCTION_NAME_ID_POST_%08x' % value)
        expected_plate = row['new_plate'] if value in PLATE_WRITES else before['plate']
        require(actual['plate'] == expected_plate, 'FUNCTION_PLATE_POST_%08x' % value)
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
        if value in BODY_ROWS:
            for key in ('body', 'body_ranges', 'body_size', 'body_sha256', 'body_bytes'):
                actual_core.pop(key, None)
                before_core.pop(key, None)
            contract = BODY_ROWS[value]
            require(actual['body_ranges'] == contract['canonical_ranges'] and
                    actual['body_size'] == int(contract['expected_size']) and
                    actual['body_sha256'] == contract['body_sha256'],
                    'BODY_RESIZE_POST_%08x' % value)
            old_ranges = json.loads(row['body_ranges_json'])
            actual_old_refs = [item for item in actual['body_references']
                               if source_in_ranges(item['from'], old_ranges)]
            same('OLD_BODY_REFS_POST_%08x' % value, actual_old_refs,
                 expected_refs(before['body_references']))
        else:
            same('FUNCTION_BODY_REFS_POST_%08x' % value,
                 actual['body_references'], expected_refs(before['body_references']))
        same('FUNCTION_METADATA_POST_%08x' % value, actual_core, before_core)
        same('FUNCTION_INCOMING_POST_%08x' % value,
             actual['incoming'], expected_refs(before['incoming']))

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
    require(int(functions.getFunctionCount()) == int(pre['function_count']) == FUNCTION_COUNT,
            'FUNCTION_COUNT_POST')
    require(raw_hash(SEGMENT_START, SEGMENT_END) == pre['segment']['sha256'] == SEGMENT_SHA256,
            'SEGMENT_RAW_HASH_POST')
    verify_r4_post(pre)
    expected_bogus_target = json.loads(json.dumps(pre['bogus_target']))
    expected_bogus_target['symbols'] = []
    expected_bogus_target['symbol_count'] = 0
    expected_bogus_target['primary_symbol'] = None
    expected_bogus_target['references_to'] = []
    same('BOGUS_TARGET_DERIVED_POST', address_state(BOGUS_TARGET),
         expected_bogus_target)
    verify_function_post(pre)
    pre_slots = dict((int(row['address'], 16), row) for row in pre['slots'])
    for value, row in sorted(SLOTS.items()):
        verify_word_post(value, row, address_state(value), pre_slots[value])
    for value, name in sorted(CASE_NAMES.items()):
        state = address_state(value)
        require(state['symbol_count'] == 1 and state['primary_symbol']['name'] == name and
                state['primary_symbol']['source'] == 'USER_DEFINED' and
                state['primary_symbol']['global'] and state['primary_symbol']['primary'],
                'CASE_LABEL_POST_%08x' % value)
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
    pre_odds = dict((int(row['address'], 16), row) for row in pre['odd_targets'])
    for value in ODD_TARGETS:
        same('ODD_TARGET_POST_%08x' % value, address_state(value), pre_odds[value])
    pre_alias_states = dict((int(row['address'], 16), row)
                            for row in pre['external_alias_sources'])
    pre_alias_equates = dict((row['name'], row)
                             for row in pre['external_alias_equates'])
    for value, names in sorted(EXTERNAL_ALIAS_RENAMES.items()):
        old_name, new_name = names
        before = pre_alias_states[value]
        actual = address_state(value)
        expected_eol = before['eol'].replace(old_name, new_name)
        require(actual['bytes'] == before['bytes'] and
                actual['data_at'] == before['data_at'] and
                actual['defined_data_at'] == before['defined_data_at'] and
                actual['symbols'] == before['symbols'] and
                actual['references_from'] == before['references_from'] and
                actual['references_to'] == before['references_to'] and
                actual['eol'] == expected_eol and
                actual['equates'] == [{'name': new_name,
                                       'value': before['rom_word']}],
                'EXTERNAL_ALIAS_SOURCE_POST_%08x' % value)
        old_contract = pre_alias_equates[old_name]
        new_contract = equate_global_row(new_name)
        require(equates.getEquate(old_name) is None and new_contract is not None and
                new_contract['value'] == old_contract['value'] and
                new_contract['references'] == old_contract['references'],
                'EXTERNAL_ALIAS_EQUATE_POST_%08x' % value)
    if MODE == 'apply':
        same('APPLY_COUNTS', COUNTS, EXPECTED_COUNTS)

print('=== RefineF14Seg1 mode=%s ===' % MODE)
verify_inputs()
reject('INPUTS')

if MODE == 'prestate':
    state = capture()
    verify_prestate(state)
    reject('PRESTATE')
    write_json(PRESTATE_NAME, state)
    print('PRESTATE functions=14 slots=167 targets=26 table_sources=25 cases=17 '
          'bases=3 odd=%d direct_callees=%d segment_bytes=4948 FAIL=0' %
          (len(ODD_TARGETS), len(DIRECT_CALLEE_TARGETS)))
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
            'status': 'F14_SEG1_DRY_PREFLIGHT_OK', 'FAIL': 0,
            'script_sha256': file_hash(getSourceFile().getAbsolutePath()),
            'plan_sha256': file_hash(run_path(PLAN_NAME)),
            'prestate_sha256': prestate_hash,
            'source_snapshot_manifest_sha256': file_hash(run_path(SOURCE_SNAPSHOT_NAME)),
            'counts': EXPECTED_COUNTS,
            'preflight': {
                'functions': 14, 'slots': 167, 'ref_targets': len(REF_TARGETS),
                'table_sources': 25, 'case_targets': 17, 'table_bases': 3,
                'odd_targets': len(ODD_TARGETS),
                'direct_callees': len(DIRECT_CALLEE_TARGETS),
                'segment_bytes': 4948, 'r4_instructions': 482,
                'r4_pc_reads': 39, 'r4_flows': 54,
                'r4_fallthroughs_final': 461,
            },
            'semantic_actions_applied': False,
        }
        write_json('f14-seg1-dry-result-v4.json', result)
        print('PREFLIGHT slots=167 EQ=63 REF=77 TABLE=25 RENAME=1 '
              'DISASM_WORD=1 FUNC_RENAME=10 PLATE_WRITE=13 R4=482 FAIL=0')
        print('STATUS: OK mode=dry FAIL=0 semantic_actions_applied=false')
    elif MODE == 'check':
        verify_post(prestate)
        reject('PERSISTED_CHECK')
        write_json('f14-seg1-persisted-check-v4.json', {
            'status': 'F14_SEG1_PERSISTED_CHECK_OK', 'FAIL': 0,
            'script_sha256': file_hash(getSourceFile().getAbsolutePath()),
            'plan_sha256': file_hash(run_path(PLAN_NAME)),
            'prestate_sha256': prestate_hash,
        })
        print('STATUS: OK mode=check FAIL=0 read_only=true')
    else:
        verify_prestate(prestate)
        reject('APPLY_PRESTATE')
        transaction = currentProgram.startTransaction('F14-Seg-1 approved materialization')
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
            write_json('f14-seg1-apply-failures.json', {
                'status': 'FAIL_ROLLED_BACK', 'FAIL': len(FAILS),
                'error': error_text, 'failures': FAILS,
                'transaction_committed': False,
            })
            raise RuntimeError('F14-Seg-1 apply rolled back')
        write_json('f14-seg1-apply-receipt.json', {
            'status': 'F14_SEG1_APPLY_OK', 'FAIL': 0,
            'script_sha256': file_hash(getSourceFile().getAbsolutePath()),
            'plan_sha256': file_hash(run_path(PLAN_NAME)),
            'prestate_sha256': prestate_hash, 'counts': COUNTS,
            'transaction_committed': True,
        })
        print('STATUS: OK mode=apply FAIL=0 transaction_committed=true')
