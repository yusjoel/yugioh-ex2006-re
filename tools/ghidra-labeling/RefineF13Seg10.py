# -*- coding: ascii -*-
#@runtime Jython
#@category Ygo-ex2006.Refine
# F13-Seg-10 PASS materialization. prestate/dry/check are read-only.

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
PLAN_NAME = 'f13-seg10-plan.json'
PRESTATE_NAME = 'f13-seg10-fresh-full-prestate.json'
SOURCE_SNAPSHOT_MANIFEST_NAME = 'f13-seg10-source-snapshot-preapply.json'
MAP_NAME = 'f13-seg10-r4-map.json'
PROPOSAL_MANIFEST_NAME = 'f13-seg10-proposal-manifest.json'
DB_BACKUP_MANIFEST_NAME = 'root-f13-seg10-db-backup.json'
INPUT_HASHES = {
    'doc/dev/refine/F13-Seg-10.proposal.md': 'c239c4eecc95ad0d19062390cb8da40d20009bad2c8b002b71a627fa7c0cdc6d',
    'doc/dev/refine/F13-Seg-10.review.md': '53dd5204f5c8e4d2a7894294de310d1a144be45a42a53b2e58b0ae85b9db1bd3',
    'doc/dev/refine/F13-Seg-10.slots.tsv': 'e98972cc66d9e431e090ebaaec39877a5007a0564eb51c059c2f3e6c1a7f1186',
    'doc/dev/refine/F13-Seg-10.plates.tsv': '17c86fe57d3e9bda1c4ddb7228790eaafa44c220e6911ccb4c3132ed7c4ddf30',
    'output/refine-run-20261028-105948/f13-seg10-r4-map.json': '375f6e2a3187468d056280f36184a9cafdbb1aa0eb87a098cccac1dadaf1ed91',
    'output/refine-run-20261028-105948/f13-seg10-proposal-manifest.json': '5247b29c4cfc0c9b5f57ba2adf9ffec6d0c89abf7300e6a5c181839474f9289a',
    'output/refine-run-20261028-105948/f13-seg10-mode-a-round2-contract.json': '034af846f408386d749ddfdabd3205bc1f2d395d488217c28bcffabe6e217604',
    'output/refine-run-20261028-105948/root-f13-seg10-mode-a-narrow-gate.json': 'e100441e1d757bbb96f0e1187131d2e72aebfe8f79dd1cf02d0be5b7b3a76fce',
    'output/refine-run-20261028-105948/root-f13-seg10-r4-static-round2-gate.json': '6f9cf2626bcb925492261e34ae74b770b2c54b8cb134ff1400f85f4b6b9a02bc',
    'output/refine-run-20261028-105948/reviewer-f13-seg10-round2-delta-audit.json': '74bc56f7dc64e878b86805f231cb604012f83a3178c36f3dbce10b2e8f2c5f47',
}
EXPECTED_COUNTS = {
    'EQ': 47, 'REF': 66, 'RENAME': 1, 'EOL': 114,
    'FUNC_RENAME': 8, 'PLATE': 16, 'CASE_LABEL': 7,
    'TABLE_LABEL': 1, 'CARVE_LABEL': 1, 'CARVE_DATA': 3,
    'R4_CODE_RANGES': 19, 'R4_INSTRUCTIONS': 415,
    'R4_POOL_WORDS': 36, 'BODY_RESIZE': 1,
}
SEGMENT_START = 0x080a689c
SEGMENT_END = 0x080a78dc
SEGMENT_SHA256 = '45f349db8eaf1cce3846d79c0114257e2c6e5a747a5e83952ba3fc863ac5a369'
BODY_FUNCTION = 0x080a71e4
BODY_FUNCTION_ID = 16937
BODY_FINAL_SIZE = 930
BODY_FINAL_SHA256 = '1df69703ef58256188c43f6c38432617338052999ee87b15f31ce1a2d0abcdc8'
PRESERVE_FUNCTIONS = [0x08086cdc]
CALL_SITES = [0x080a8f66, 0x080a8f6c, 0x080a8f12, 0x080a8f2a,
              0x080a8f30, 0x080a8f36, 0x080a8f3c, 0x080a8f42]
CALL_TARGETS = {
    0x080a8f66: 0x080a689c, 0x080a8f6c: 0x080a6a20,
    0x080a8f12: 0x080a6b38, 0x080a8f2a: 0x080a6cc8,
    0x080a8f30: 0x080a6e74, 0x080a8f36: 0x080a71e4,
    0x080a8f3c: 0x080a7650, 0x080a8f42: 0x080a7788,
}
SWITCH_SOURCES = [0x080a7218 + index * 4 for index in range(7)]
CASE_NAMES = {
    0x080a7234: 'special_summon_banish_phase_case_0_prompt',
    0x080a73a8: 'special_summon_banish_phase_case_1_init_effect_slots',
    0x080a7438: 'special_summon_banish_phase_case_2_enqueue_effect_slot',
    0x080a74b6: 'special_summon_banish_phase_case_3_finalize_materials',
    0x080a7238: 'special_summon_banish_phase_case_4_repeat_prompt',
    0x080a7544: 'special_summon_banish_phase_case_5_select_target',
    0x080a759c: 'special_summon_banish_phase_case_6_confirm_target',
}
ODD_TARGETS = [0x080a57b9, 0x080a5d4d, 0x080a5afd]
PREEXISTING_EQ_SLOTS = [0x080a6b84, 0x080a6be8, 0x080a6d20,
                        0x080a6d88, 0x080a6edc, 0x080a6f50]
PREEXISTING_REF_SLOTS = [
    0x080a69f0, 0x080a6b1c, 0x080a6c74, 0x080a6dbc, 0x080a6fc0,
    0x080a7030, 0x080a71d0, 0x080a76d0, 0x080a76fc, 0x080a7740,
    0x080a7768, 0x080a7808, 0x080a7848, 0x080a788c, 0x080a78bc,
]
TABLE_BASE = 0x080a7218
TABLE_NAME = 'special_summon_banish_phase_jump_table'
CARVE_BASE = 0x09e478bc
CARVE_WORDS = [0x1288, 0x129b, 0x12b8]
CARVE_NAME = 'valkyrion_prompt_material_cids'
CARVE_BOOKEND_START = 0x09e478b0
CARVE_TAIL_START = 0x09e478c8
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

def path_in_root(relative):
    return os.path.join(ROOT, *relative.replace('\\', '/').split('/'))

def read_json_path(path):
    with open(path, 'rb') as stream:
        return json.load(stream)

def read_json(name):
    return read_json_path(os.path.join(RUN, name))

def write_json(name, value):
    with open(os.path.join(RUN, name), 'w') as stream:
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
        print('DETAIL ' + json.dumps({'actual': actual, 'expected': expected}, ensure_ascii=True, sort_keys=True))

def require(condition, message):
    if not condition:
        fail(message)

def canonical(value):
    if isinstance(value, dict):
        return dict((key, canonical(item)) for key, item in value.items())
    if isinstance(value, list):
        return sorted((canonical(item) for item in value), key=lambda item: json.dumps(item, sort_keys=True))
    return value

def same(message, actual, expected):
    left = json.dumps(canonical(actual), ensure_ascii=True, sort_keys=True, separators=(',', ':'))
    right = json.dumps(canonical(expected), ensure_ascii=True, sort_keys=True, separators=(',', ':'))
    if left != right:
        fail(message, actual, expected)

def reject(phase):
    if FAILS:
        write_json('f13-seg10-%s-failures.json' % MODE,
                   {'status': 'FAIL', 'phase': phase, 'FAIL': len(FAILS), 'failures': FAILS})
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
    return ''.join('%02x' % (memory.getByte(addr.add(index)) & 255) for index in range(length))

def raw_hash(lo, hi):
    raw = ''.join(chr(memory.getByte(toAddr(value)) & 255) for value in range(lo, hi))
    return hashlib.sha256(raw).hexdigest()

def symbol_row(symbol):
    parent = symbol.getParentNamespace()
    return {
        'id': long(symbol.getID()), 'name': unicode(symbol.getName()),
        'qualified_name': unicode(symbol.getName(True)), 'type': str(symbol.getSymbolType()),
        'source': str(symbol.getSource()), 'primary': bool(symbol.isPrimary()),
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
    return dict((key, row[key]) for key in ('from', 'to', 'operand', 'type', 'source', 'primary'))

def data_row(data):
    if data is None:
        return None
    return {'address': str(data.getAddress()), 'min': str(data.getMinAddress()),
            'max': str(data.getMaxAddress()), 'length': int(data.getLength()),
            'type': unicode(data.getDataType().getPathName()),
            'defined': bool(safe_value(lambda: data.isDefined(), False))}

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
        'data_at': data_row(listing.getDataAt(addr)),
        'defined_data_at': data_row(listing.getDefinedDataAt(addr)),
        'data_containing': data_row(listing.getDataContaining(addr)),
        'instruction': None if listing.getInstructionAt(addr) is None else unicode(listing.getInstructionAt(addr).toString()),
        'function': None if functions.getFunctionAt(addr) is None else unicode(functions.getFunctionAt(addr).getName()),
        'references_from': [ref_row(ref) for ref in references.getReferencesFrom(addr)],
        'references_to': [ref_row(ref) for ref in references.getReferencesTo(addr)],
        'equates': sorted([{'name': unicode(eq.getName()), 'value': long(eq.getValue()) & 0xffffffff}
                           for eq in equates.getEquates(addr)], key=lambda row: (row['name'], row['value'])),
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
                'length': int(unit.getLength()), 'class': unicode(unit.getClass().getSimpleName())},
            'instruction_at': None if instruction is None else unicode(instruction.toString()),
            'data_at': data_row(data), 'defined_data_at': data_row(defined),
            'function_owner': None if owner is None else {
                'entry': str(owner.getEntryPoint()), 'id': long(owner.getSymbol().getID()),
                'name': unicode(owner.getName())},
            'tmode': tmode,
        })
    return rows

SLOT_ROWS = read_tsv('doc/dev/refine/F13-Seg-10.slots.tsv')
PLATE_ROWS = read_tsv('doc/dev/refine/F13-Seg-10.plates.tsv')
R4_MAP = read_json(MAP_NAME)
SLOTS = dict((int(row['address'], 16), row) for row in SLOT_ROWS)
PLATES = dict((int(row['entry'], 16), row) for row in PLATE_ROWS)
RENAMES = dict((value, row) for value, row in PLATES.items() if row['current_name'] != row['final_name'])
FUNCTIONS = sorted(set(PLATES) | set(PRESERVE_FUNCTIONS))
REF_TARGETS = sorted(set(int(row['original_value'], 16) for row in SLOT_ROWS if row['action'] == 'REF'))
CODE_RANGES = [(int(item[0], 16), int(item[1], 16)) for item in R4_MAP['code_ranges']]
POOL_RANGES = [(int(item[0], 16), int(item[1], 16)) for item in R4_MAP['pool_ranges']]
PADDING_RANGES = [(int(item[0], 16), int(item[1], 16)) for item in R4_MAP['padding_ranges']]
FINAL_BODY_RANGES = [(int(item[0], 16), int(item[1], 16)) for item in R4_MAP['final_function_body_ranges']]
LITERAL_ADDRESSES = sorted(int(row['address'], 16) for row in R4_MAP['literal_slots'])
INSTRUCTION_ADDRESSES = sorted(int(row['address'], 16) for row in R4_MAP['instructions'])

def manifest_input_path(relative):
    if relative == 'doc/dev/refine/F13-Seg-10.review.md':
        return os.path.join(RUN, 'seg10-review-round1', *relative.split('/'))
    return path_in_root(relative)

def verify_inputs():
    for relative, digest in sorted(INPUT_HASHES.items()):
        same('INPUT_HASH_' + relative, file_hash(path_in_root(relative)), digest)
    proposal_manifest = read_json(PROPOSAL_MANIFEST_NAME)
    require(len(proposal_manifest.get('sha256', {})) == 14, 'PROPOSAL_MANIFEST_ENTRY_COUNT')
    for relative, digest in sorted(proposal_manifest.get('sha256', {}).items()):
        same('PROPOSAL_MANIFEST_HASH_' + relative,
             file_hash(manifest_input_path(relative)), digest)
    require(len(SLOTS) == 114 and len(SLOT_ROWS) == 114, 'SLOT_COUNT')
    require(sum(row['action'] == 'EQ' for row in SLOT_ROWS) == 47, 'EQ_COUNT')
    require(sum(row['action'] == 'REF' for row in SLOT_ROWS) == 66, 'REF_COUNT')
    require(sum(row['action'] == 'RENAME' for row in SLOT_ROWS) == 1, 'RENAME_COUNT')
    require(sum(row['old_name'] != 'none' for row in SLOT_ROWS) == 78 and
            sum(row['old_name'] == 'none' for row in SLOT_ROWS) == 36, 'OLD_NEW_SLOT_COUNTS')
    require(len(PLATES) == 16 and len(RENAMES) == 8 and len(FUNCTIONS) == 17,
            'FUNCTION_PLATE_COUNTS')
    require(len(REF_TARGETS) == 5 and len(CALL_SITES) == 8 and len(ODD_TARGETS) == 3,
            'EXTERNAL_ENTITY_COUNTS')
    require(len(PREEXISTING_EQ_SLOTS) == 6 and len(PREEXISTING_REF_SLOTS) == 15 and
            all(SLOTS[value]['action'] == 'EQ' for value in PREEXISTING_EQ_SLOTS) and
            all(SLOTS[value]['action'] == 'REF' for value in PREEXISTING_REF_SLOTS),
            'PREEXISTING_ACTION_COUNTS')
    require(len(CODE_RANGES) == 19 and len(POOL_RANGES) == 18 and
            len(PADDING_RANGES) == 9 and len(FINAL_BODY_RANGES) == 19,
            'R4_RANGE_COUNTS')
    require(len(LITERAL_ADDRESSES) == 36 and len(INSTRUCTION_ADDRESSES) == 415 and
            len(R4_MAP['explicit_flow_targets']) == 67 and
            sum(len(row['pc_consumers']) for row in R4_MAP['literal_slots']) == 37,
            'R4_MACHINE_COUNTS')
    require([int(item, 16) for item in R4_MAP['case_entries']] ==
            [0x080a7234, 0x080a73a8, 0x080a7438, 0x080a74b6,
             0x080a7238, 0x080a7544, 0x080a759c], 'CASE_ENTRY_ORDER')
    require(sum(hi - lo for lo, hi in CODE_RANGES) == 876 and
            sum(hi - lo for lo, hi in POOL_RANGES) == 144 and
            sum(hi - lo for lo, hi in PADDING_RANGES) == 18 and
            sum(hi - lo for lo, hi in FINAL_BODY_RANGES) == BODY_FINAL_SIZE,
            'R4_BYTE_COUNTS')
    require(sorted(LITERAL_ADDRESSES) == sorted(value for lo, hi in POOL_RANGES
                                                for value in range(lo, hi, 4)),
            'R4_LITERAL_RANGE_SET')
    require(len(set(row['final_slot_label'] for row in SLOT_ROWS)) == 114,
            'SLOT_LABEL_UNIQUE')
    for value, row in sorted(SLOTS.items()):
        require(re.match(r'^[a-z][a-z0-9_]+$', row['final_slot_label']) is not None,
                'SLOT_NAME_%08x' % value)
        require(all(ord(char) < 128 for char in row['eol_ascii']),
                'EOL_ASCII_%08x' % value)
        collisions = [symbol for symbol in symbols.getGlobalSymbols(row['final_slot_label'])
                      if symbol.getAddress() != toAddr(value)]
        require(not collisions, 'SLOT_NAME_COLLISION_%08x' % value)
    for value, row in sorted(PLATES.items()):
        text = row['new_plate']
        require(all(ord(char) < 128 for char in text) and len(text) <= 500 and
                len(text) == int(row['new_plate_chars']), 'PLATE_ASCII_%08x' % value)
        collisions = [symbol for symbol in symbols.getGlobalSymbols(row['final_name'])
                      if symbol.getAddress() != toAddr(value)]
        require(not collisions, 'FUNCTION_NAME_COLLISION_%08x' % value)
    for value, name in sorted(CASE_NAMES.items()):
        collisions = [symbol for symbol in symbols.getGlobalSymbols(name)
                      if symbol.getAddress() != toAddr(value)]
        require(not collisions, 'CASE_NAME_COLLISION_%08x' % value)
    require(not [symbol for symbol in symbols.getGlobalSymbols(TABLE_NAME)
                 if symbol.getAddress() != toAddr(TABLE_BASE)], 'TABLE_NAME_COLLISION')
    require(not [symbol for symbol in symbols.getGlobalSymbols(CARVE_NAME)
                 if symbol.getAddress() != toAddr(CARVE_BASE)], 'CARVE_NAME_COLLISION')

def capture():
    carve_addresses = [CARVE_BOOKEND_START, CARVE_BOOKEND_START + 4,
                       CARVE_BOOKEND_START + 8, CARVE_BASE, CARVE_BASE + 4,
                       CARVE_BASE + 8, CARVE_TAIL_START, CARVE_END]
    return {
        'status': 'F13_SEG10_FRESH_FULL_PRESTATE',
        'program_name': unicode(currentProgram.getName()),
        'function_count': int(functions.getFunctionCount()),
        'segment': {'start': '0x%08x' % SEGMENT_START,
                    'end': '0x%08x' % SEGMENT_END,
                    'size': SEGMENT_END - SEGMENT_START,
                    'sha256': raw_hash(SEGMENT_START, SEGMENT_END)},
        'functions': [function_row(value) for value in FUNCTIONS],
        'slots': [address_state(value) for value in sorted(SLOTS)],
        'ref_targets': [address_state(value) for value in REF_TARGETS],
        'switch_sources': [address_state(value) for value in SWITCH_SOURCES],
        'case_targets': [address_state(value) for value in sorted(CASE_NAMES)],
        'odd_targets': [address_state(value) for value in ODD_TARGETS],
        'odd_target_functions': [function_row(value - 1) for value in ODD_TARGETS],
        'call_sites': [address_state(value) for value in CALL_SITES],
        'carve': {
            'addresses': [address_state(value) for value in carve_addresses],
            'bookend_and_carve_bytes': bytes_hex(CARVE_BOOKEND_START, 24),
            'bookend_to_tail_end_size': CARVE_END - CARVE_BOOKEND_START,
            'bookend_to_tail_end_sha256': raw_hash(CARVE_BOOKEND_START, CARVE_END),
        },
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
            state['body'] == row['body'] and state['body_size'] == int(row['body_size']) and
            state['body_sha256'] == row['body_sha256'] and
            state['calling_convention'] == row['calling_convention'] and
            state['signature_source'] == row['signature_source'] and
            state['prototype'] == row['prototype'] and
            state['custom_variable_storage'] == bool_field(row['custom_variable_storage']) and
            state['varargs'] == bool_field(row['varargs']) and
            state['inline'] == bool_field(row['inline']) and
            state['no_return'] == bool_field(row['no_return']) and
            state['external'] == bool_field(row['external']) and
            state['thunk'] == bool_field(row['thunk']), 'FUNCTION_STATIC_%08x' % value)
    require(state['return'] is not None and
            state['return']['name'] == row['return_name'] and
            state['return']['data_type'] == row['return_data_type'] and
            state['return']['storage'] == row['return_storage'] and
            state['return']['source'] == row['return_source'] and
            state['parameters'] == json.loads(row['parameters_json']) and
            state['incoming'] == json.loads(row['incoming_json']) and
            len(state['eol_comments']) == int(row['eol_count']),
            'FUNCTION_FULL_METADATA_%08x' % value)
    plate = state['plate']
    require(plate is not None and len(plate) == int(row['old_plate_chars']) and
            hashlib.sha256(plate.encode('utf-8')).hexdigest() == row['old_plate_sha256'],
            'FUNCTION_PLATE_PRE_%08x' % value)

def verify_prestate(pre):
    same('FRESH_PRESTATE_EXACT', capture(), pre)
    require(pre['function_count'] == 5213, 'FUNCTION_COUNT_PRE')
    require(pre['segment']['sha256'] == SEGMENT_SHA256 and
            len(pre['segment_byte_units']) == SEGMENT_END - SEGMENT_START,
            'SEGMENT_PRE')
    unit_starts = [row for row in pre['segment_byte_units']
                   if row['unit'] is not None and row['unit']['min'] == row['address'][2:]]
    unit_counts = {
        'instruction_starts': sum(row['instruction_at'] is not None for row in unit_starts),
        'data_starts': sum(row['unit']['class'] == 'DataDB' for row in unit_starts),
        'defined_data_starts': sum(row['defined_data_at'] is not None for row in unit_starts),
        'bytes': len(pre['segment_byte_units']),
    }
    same('SEGMENT_UNIT_COUNTS_PRE', unit_counts,
         {'instruction_starts': 1302, 'data_starts': 1171,
          'defined_data_starts': 85, 'bytes': 4160})
    pre_slots = dict((int(row['address'], 16), row) for row in pre['slots'])
    for value, row in sorted(SLOTS.items()):
        state = pre_slots[value]
        require(state['rom_word'] == int(row['original_value'], 16) and
                state['eol'] is None, 'SLOT_VALUE_EOL_%08x' % value)
        expected_source_refs = []
        expected_equates = []
        if value in PREEXISTING_REF_SLOTS:
            expected_source_refs = [{
                'from': '%08x' % value,
                'to': '%08x' % int(row['original_value'], 16),
                'operand': 0, 'type': 'DATA', 'source': 'USER_DEFINED',
                'primary': True,
            }]
        if value in PREEXISTING_EQ_SLOTS:
            expected_equates = [{
                'name': row['target_symbol'],
                'value': int(row['original_value'], 16),
            }]
        same('SLOT_SOURCE_REFS_PRE_%08x' % value,
             [ref_core(item) for item in state['references_from']], expected_source_refs)
        same('SLOT_EQUATES_PRE_%08x' % value, state['equates'], expected_equates)
        if row['old_name'] == 'none':
            require(state['symbol_count'] == 0 and state['primary_symbol'] is None and
                    state['defined_data_at'] is None and state['instruction'] is None,
                    'NEW_POOL_EMPTY_%08x' % value)
        else:
            require(state['symbol_count'] == 1 and
                    state['primary_symbol']['id'] == long(row['slot_symbol_id']) and
                    state['primary_symbol']['name'] == row['old_name'] and
                    state['primary_symbol']['source'] == row['slot_symbol_source'] and
                    state['primary_symbol']['type'] == row['slot_symbol_type'] and
                    state['defined_data_at'] is not None and
                    state['defined_data_at']['type'] == row['defined_data'].rsplit(':', 1)[0] and
                    state['defined_data_at']['length'] == 4,
                    'OLD_SLOT_STATIC_%08x' % value)
    pre_functions = dict((int(row['entry'], 16), row) for row in pre['functions'])
    for value, row in sorted(PLATES.items()):
        verify_function_tsv(value, row, pre_functions[value])
    preserve = pre_functions[0x08086cdc]
    require(preserve is not None and preserve['return'] is not None and
            preserve['namespace']['id'] is not None and preserve['symbol']['id'] is not None,
            'PRESERVE_FUNCTION_COMPLETE_METADATA')
    pre_switches = dict((int(row['address'], 16), row) for row in pre['switch_sources'])
    for index, value in enumerate(SWITCH_SOURCES):
        state = pre_switches[value]
        target = int(R4_MAP['case_entries'][index], 16)
        same('SWITCH_REF_PRE_%08x' % value,
             [ref_core(item) for item in state['references_from']],
             [{'from': '%08x' % value, 'to': '%08x' % target, 'operand': 0,
               'type': 'DATA', 'source': 'DEFAULT', 'primary': True}])
        require(state['rom_word'] == target and state['symbol_count'] == 0 and
                state['defined_data_at'] is not None and
                state['defined_data_at']['length'] == 4, 'SWITCH_SOURCE_PRE_%08x' % value)
    pre_cases = dict((int(row['address'], 16), row) for row in pre['case_targets'])
    for value in CASE_NAMES:
        state = pre_cases[value]
        require(state['symbol_count'] == 1 and state['primary_symbol']['source'] == 'DEFAULT' and
                state['primary_symbol']['primary'], 'CASE_DYNAMIC_PRE_%08x' % value)
    for state in pre['odd_targets']:
        require(state['defined_data_at'] is None and state['references_from'] == [] and
                state['symbol_count'] <= 1, 'ODD_TARGET_PRE_' + state['address'])
    pre_calls = dict((int(row['address'], 16), row) for row in pre['call_sites'])
    for value in CALL_SITES:
        same('CALL_REF_PRE_%08x' % value,
             [ref_core(item) for item in pre_calls[value]['references_from']],
             [{'from': '%08x' % value, 'to': '%08x' % CALL_TARGETS[value],
               'operand': 0, 'type': 'UNCONDITIONAL_CALL',
               'source': 'DEFAULT', 'primary': True}])
    require(bytes_hex(CARVE_BASE, 12) == '881200009b120000b8120000', 'CARVE_BYTES_PRE')
    for value in [CARVE_BASE, CARVE_BASE + 4, CARVE_BASE + 8]:
        state = address_state(value)
        require(state['symbol_count'] == 0 and state['defined_data_at'] is None and
                state['references_from'] == [] and state['references_to'] == [],
                'CARVE_EMPTY_PRE_%08x' % value)

def verify_plan(plan, prestate_hash):
    require(plan.get('status') == 'F13_SEG10_PLAN_FROZEN', 'PLAN_STATUS')
    same('PLAN_INPUT_HASHES', plan.get('input_hashes'), INPUT_HASHES)
    same('PLAN_COUNTS', plan.get('counts'), EXPECTED_COUNTS)
    require(plan.get('script_sha256') == file_hash(getSourceFile().getAbsolutePath()),
            'PLAN_SCRIPT_HASH')
    require(plan.get('prestate_sha256') == prestate_hash, 'PLAN_PRESTATE_HASH')
    require(plan.get('source_snapshot_manifest') == SOURCE_SNAPSHOT_MANIFEST_NAME and
            plan.get('source_snapshot_manifest_sha256') ==
            file_hash(os.path.join(RUN, SOURCE_SNAPSHOT_MANIFEST_NAME)),
            'PLAN_SOURCE_SNAPSHOT_HASH')
    require(plan.get('proposal_manifest_sha256') ==
            file_hash(os.path.join(RUN, PROPOSAL_MANIFEST_NAME)),
            'PLAN_PROPOSAL_MANIFEST_HASH')
    require(plan.get('db_backup_manifest_sha256') ==
            file_hash(os.path.join(RUN, DB_BACKUP_MANIFEST_NAME)),
            'PLAN_DB_BACKUP_HASH')
    require(plan.get('range') == [SEGMENT_START, SEGMENT_END] and
            plan.get('function_addresses') == FUNCTIONS and
            plan.get('slot_addresses') == sorted(SLOTS) and
            plan.get('switch_sources') == SWITCH_SOURCES and
            plan.get('case_targets') == sorted(CASE_NAMES) and
            plan.get('odd_targets') == ODD_TARGETS and
            plan.get('call_sites') == CALL_SITES and
            plan.get('r4')['code_ranges'] == [[lo, hi] for lo, hi in CODE_RANGES] and
            plan.get('r4')['pool_addresses'] == LITERAL_ADDRESSES and
            plan.get('r4')['padding_ranges'] == [[lo, hi] for lo, hi in PADDING_RANGES] and
            plan.get('r4')['final_body_ranges'] == [[lo, hi] for lo, hi in FINAL_BODY_RANGES] and
            plan.get('carve')['base'] == CARVE_BASE and
            plan.get('carve')['words'] == CARVE_WORDS, 'PLAN_SCOPE')
    require(plan.get('sync_contract', {}).get('naming_proposals_name_cells') == 8 and
            plan.get('sync_contract', {}).get('inventory_function_count') == 5213 and
            plan.get('sync_contract', {}).get('inventory_named_count') == 5123 and
            plan.get('sync_contract', {}).get('inventory_auto_count') == 90 and
            plan.get('sync_contract', {}).get('inventory_length_change') ==
            {'entry': 0x080a71e4, 'before': 54, 'after': 930},
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

def apply_all():
    context = currentProgram.getProgramContext()
    for lo, hi in CODE_RANGES:
        clearListing(toAddr(lo), toAddr(hi - 1))
        context.setValue(tmode_register, toAddr(lo), toAddr(hi - 1), BigInteger.ONE)
        command = DisassembleCommand(toAddr(lo), AddressSet(toAddr(lo), toAddr(hi - 1)), True)
        if not command.applyTo(currentProgram):
            raise RuntimeError('Disassembly failed [%08x,%08x)' % (lo, hi))
        COUNTS['R4_CODE_RANGES'] += 1
    actual_instructions = [value for value in INSTRUCTION_ADDRESSES
                           if listing.getInstructionAt(toAddr(value)) is not None]
    if actual_instructions != INSTRUCTION_ADDRESSES:
        raise RuntimeError('R4 instruction address set incomplete')
    COUNTS['R4_INSTRUCTIONS'] = len(actual_instructions)
    for value in LITERAL_ADDRESSES:
        clearListing(toAddr(value), toAddr(value + 3))
        listing.createData(toAddr(value), Undefined4DataType.dataType)
        COUNTS['R4_POOL_WORDS'] += 1
    for value, name in sorted(CASE_NAMES.items()):
        ensure_single_global_label(value, name)
        COUNTS['CASE_LABEL'] += 1
    ensure_single_global_label(TABLE_BASE, TABLE_NAME)
    COUNTS['TABLE_LABEL'] += 1
    for index, original in enumerate(CARVE_WORDS):
        value = CARVE_BASE + index * 4
        if (memory.getInt(toAddr(value)) & 0xffffffff) != original:
            raise RuntimeError('Carve ROM value changed at %08x' % value)
        if (symbols.getPrimarySymbol(toAddr(value)) is not None or
                listing.getDefinedDataAt(toAddr(value)) is not None or
                list(references.getReferencesFrom(toAddr(value))) or
                list(references.getReferencesTo(toAddr(value)))):
            raise RuntimeError('Carve target occupied at %08x' % value)
    ensure_single_global_label(CARVE_BASE, CARVE_NAME)
    COUNTS['CARVE_LABEL'] += 1
    for index in range(3):
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
            matches = [ref for ref in eq.getReferences()
                       if ref.getAddress() == addr and ref.getOpIndex() == 0]
            if not matches:
                eq.addReference(addr, 0)
            elif len(matches) != 1:
                raise RuntimeError('Duplicate equate references at %08x' % value)
        elif row['action'] == 'REF':
            existing_refs = list(references.getReferencesFrom(addr))
            if existing_refs:
                cores = [ref_core(ref_row(ref)) for ref in existing_refs]
                expected = [{'from': '%08x' % value, 'to': '%08x' % original,
                             'operand': 0, 'type': 'DATA',
                             'source': 'USER_DEFINED', 'primary': True}]
                if cores != expected:
                    raise RuntimeError('REF source conflict at %08x' % value)
            else:
                ref = references.addMemoryReference(addr, toAddr(original), RefType.DATA,
                                                     SourceType.USER_DEFINED, 0)
                references.setPrimary(ref, True)
        elif row['action'] != 'RENAME':
            raise RuntimeError('Unknown slot action at %08x' % value)
        ensure_single_global_label(value, row['final_slot_label'])
        listing.setComment(addr, CodeUnit.EOL_COMMENT, row['eol_ascii'])
        COUNTS[row['action']] += 1
        COUNTS['EOL'] += 1
    body_set = AddressSet()
    for lo, hi in FINAL_BODY_RANGES:
        body_set.addRange(toAddr(lo), toAddr(hi - 1))
    body_fn = functions.getFunctionAt(toAddr(BODY_FUNCTION))
    if body_fn is None or long(body_fn.getSymbol().getID()) != BODY_FUNCTION_ID:
        raise RuntimeError('Body function identity changed')
    body_fn.setBody(body_set)
    COUNTS['BODY_RESIZE'] += 1
    for value, row in sorted(RENAMES.items()):
        functions.getFunctionAt(toAddr(value)).setName(row['final_name'], SourceType.USER_DEFINED)
        COUNTS['FUNC_RENAME'] += 1
    for value, row in sorted(PLATES.items()):
        listing.setComment(toAddr(value), CodeUnit.PLATE_COMMENT, row['new_plate'])
        COUNTS['PLATE'] += 1

def expected_refs(rows):
    result = json.loads(json.dumps(rows))
    for item in result:
        try:
            target = int(item['to'], 16)
        except Exception:
            continue
        if target in SLOTS or target in CASE_NAMES:
            primary = symbols.getPrimarySymbol(toAddr(target))
            if primary is None:
                fail('APPROVED_DERIVED_TARGET_MISSING_%08x' % target)
            else:
                item['target_primary_id'] = long(primary.getID())
                item['target_primary_name'] = unicode(primary.getName(True))
        if target in RENAMES:
            current_name = RENAMES[target]['current_name']
            final_name = RENAMES[target]['final_name']
            if item.get('target_primary_name') == current_name:
                item['target_primary_name'] = final_name
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

def slot_read_cores(value, row):
    consumers = [int(item, 16) for item in row['pc_relative_consumers'].split(',')]
    return [{'from': '%08x' % source, 'to': '%08x' % value, 'operand': 1,
             'type': 'READ', 'source': 'DEFAULT', 'primary': True}
            for source in consumers]

def verify_r4_post(pre):
    actual_instruction_addresses = []
    actual_flow_pairs = []
    fallthroughs = []
    for value in range(SEGMENT_START, SEGMENT_END):
        instruction = listing.getInstructionAt(toAddr(value))
        if instruction is None:
            continue
        actual_instruction_addresses.append(value)
        if value in INSTRUCTION_ADDRESSES:
            for ref in references.getReferencesFrom(toAddr(value)):
                if ref.getReferenceType().isFlow():
                    actual_flow_pairs.append([value, long(ref.getToAddress().getOffset())])
            target = instruction.getFallThrough()
            if target is not None:
                fallthroughs.append([value, long(target.getOffset())])
                require(long(target.getOffset()) == value + int(instruction.getLength()),
                        'R4_FALLTHROUGH_TARGET_%08x' % value)
    pre_instruction_addresses = [int(row['address'], 16) for row in pre['segment_byte_units']
                                 if row['instruction_at'] is not None]
    same('R4_INSTRUCTION_ADDRESS_SET', actual_instruction_addresses,
         sorted(pre_instruction_addresses + INSTRUCTION_ADDRESSES))
    instruction_map = dict((int(row['address'], 16), row) for row in R4_MAP['instructions'])
    for value in INSTRUCTION_ADDRESSES:
        expected = instruction_map[value]
        require(bytes_hex(value, len(expected['raw_bytes']) // 2) == expected['raw_bytes'],
                'R4_INSTRUCTION_BYTES_%08x' % value)
        require(listing.getInstructionAt(toAddr(value)) is not None,
                'R4_INSTRUCTION_AT_%08x' % value)
        owner = functions.getFunctionContaining(toAddr(value))
        require(owner is not None and long(owner.getSymbol().getID()) == BODY_FUNCTION_ID,
                'R4_FUNCTION_OWNER_%08x' % value)
        context_value = currentProgram.getProgramContext().getValue(tmode_register, toAddr(value), False)
        require(context_value is not None and int(context_value) == 1,
                'R4_TMODE_%08x' % value)
    expected_flow_pairs = sorted([[int(row['from'], 16), int(row['to'], 16)]
                                  for row in R4_MAP['explicit_flow_targets']])
    same('R4_EXPLICIT_FLOW_SET', sorted(actual_flow_pairs), expected_flow_pairs)
    require(len(fallthroughs) == 395, 'R4_FALLTHROUGH_COUNT')
    require([0x080a763c, 0x080a763e] in fallthroughs,
            'R4_FINAL_FALLTHROUGH')
    for value in LITERAL_ADDRESSES:
        state = address_state(value)
        require(state['defined_data_at'] is not None and
                state['defined_data_at']['length'] == 4 and
                state['defined_data_at']['type'] == '/undefined4' and
                state['instruction'] is None, 'R4_POOL_DATA_%08x' % value)
    for lo, hi in PADDING_RANGES:
        for value in range(lo, hi):
            state = address_state(value)
            require(state['instruction'] is None and state['defined_data_at'] is None and
                    state['symbol_count'] == 0 and state['eol'] is None,
                    'R4_PADDING_%08x' % value)
    units = segment_byte_units()
    unit_starts = [row for row in units
                   if row['unit'] is not None and row['unit']['min'] == row['address'][2:]]
    counts = {
        'instruction_starts': sum(row['instruction_at'] is not None for row in unit_starts),
        'data_starts': sum(row['unit']['class'] == 'DataDB' for row in unit_starts),
        'defined_data_starts': sum(row['defined_data_at'] is not None for row in unit_starts),
        'data_len4': sum(row['defined_data_at'] is not None and
                         row['defined_data_at']['length'] == 4 for row in unit_starts),
    }
    same('R4_FINAL_UNIT_COUNTS', counts,
         {'instruction_starts': 1717, 'data_starts': 187,
          'defined_data_starts': 121, 'data_len4': 121})
    pre_units = dict((int(row['address'], 16), row) for row in pre['segment_byte_units'])
    changed = set(value for lo, hi in CODE_RANGES + POOL_RANGES for value in range(lo, hi))
    for row in units:
        value = int(row['address'], 16)
        if value not in changed:
            same('UNIT_STATIC_POST_%08x' % value,
                 unit_layout_core(row), unit_layout_core(pre_units[value]))

def verify_function_post(pre):
    pre_functions = dict((int(row['entry'], 16), row) for row in pre['functions'])
    for value in FUNCTIONS:
        actual = function_row(value)
        before = pre_functions[value]
        if value in PLATES:
            row = PLATES[value]
            require(actual['name'] == row['final_name'] and
                    actual['symbol']['id'] == before['symbol']['id'] and
                    actual['symbol']['source'] == 'USER_DEFINED' and
                    actual['plate'] == row['new_plate'],
                    'FUNCTION_NAME_PLATE_POST_%08x' % value)
        else:
            require(actual['name'] == before['name'] and actual['plate'] == before['plate'],
                    'PRESERVE_FUNCTION_NAME_PLATE_%08x' % value)
        actual_core = function_metadata_core(actual)
        before_core = function_metadata_core(before)
        actual_symbol = dict(actual_core['symbol'])
        before_symbol = dict(before_core['symbol'])
        actual_core['symbol'] = actual_symbol
        before_core['symbol'] = before_symbol
        for item in (actual_symbol, before_symbol):
            item.pop('name', None)
            item.pop('qualified_name', None)
        actual_prototype = actual_core.pop('prototype')
        before_prototype = before_core.pop('prototype')
        expected_prototype = before_prototype
        if value in RENAMES:
            expected_prototype = before_prototype.replace(
                RENAMES[value]['current_name'], RENAMES[value]['final_name'], 1)
        require(actual_prototype == expected_prototype,
                'FUNCTION_PROTOTYPE_POST_%08x' % value)
        if value == BODY_FUNCTION:
            for key in ('body', 'body_ranges', 'body_size', 'body_sha256', 'body_bytes'):
                actual_core.pop(key, None)
                before_core.pop(key, None)
            require(actual['body_ranges'] == [['0x%08x' % lo, '0x%08x' % hi]
                                              for lo, hi in FINAL_BODY_RANGES] and
                    actual['body_size'] == BODY_FINAL_SIZE and
                    actual['body_sha256'] == BODY_FINAL_SHA256,
                    'BODY_RESIZE_POST')
        same('FUNCTION_METADATA_POST_%08x' % value, actual_core, before_core)
        same('FUNCTION_INCOMING_POST_%08x' % value,
             actual['incoming'], expected_refs(before['incoming']))
        if value != BODY_FUNCTION:
            same('FUNCTION_BODY_REFS_POST_%08x' % value,
                 actual['body_references'], expected_refs(before['body_references']))

def verify_post(pre):
    require(int(functions.getFunctionCount()) == int(pre['function_count']) == 5213,
            'FUNCTION_COUNT_POST')
    require(raw_hash(SEGMENT_START, SEGMENT_END) == pre['segment']['sha256'] == SEGMENT_SHA256,
            'SEGMENT_RAW_HASH_POST')
    verify_r4_post(pre)
    verify_function_post(pre)
    pre_slots = dict((int(row['address'], 16), row) for row in pre['slots'])
    for value, row in sorted(SLOTS.items()):
        actual = address_state(value)
        before = pre_slots[value]
        require(actual['bytes'] == before['bytes'] and
                actual['rom_word'] == int(row['original_value'], 16) and
                actual['defined_data_at'] is not None and
                actual['defined_data_at']['length'] == 4 and
                actual['symbol_count'] == 1 and
                actual['primary_symbol']['name'] == row['final_slot_label'] and
                actual['primary_symbol']['source'] == 'USER_DEFINED' and
                actual['primary_symbol']['primary'] and
                actual['primary_symbol']['global'] and
                actual['eol'] == row['eol_ascii'], 'SLOT_POST_%08x' % value)
        read_cores = [ref_core(item) for item in actual['references_to']]
        same('SLOT_READ_REFS_POST_%08x' % value, read_cores, slot_read_cores(value, row))
        primary_id = actual['primary_symbol']['id']
        primary_name = actual['primary_symbol']['qualified_name']
        require(all(item['target_primary_id'] == primary_id and
                    item['target_primary_name'] == primary_name
                    for item in actual['references_to']),
                'SLOT_DERIVED_TARGET_POST_%08x' % value)
        source_cores = [ref_core(item) for item in actual['references_from']]
        if row['action'] == 'EQ':
            same('EQ_SET_POST_%08x' % value, actual['equates'],
                 [{'name': row['target_symbol'], 'value': int(row['original_value'], 16)}])
            require(source_cores == [], 'EQ_REF_POST_%08x' % value)
        elif row['action'] == 'REF':
            require(actual['equates'] == [], 'REF_EQ_POST_%08x' % value)
            same('REF_SOURCE_POST_%08x' % value, source_cores,
                 [{'from': '%08x' % value,
                   'to': '%08x' % int(row['original_value'], 16),
                   'operand': 0, 'type': 'DATA', 'source': 'USER_DEFINED',
                   'primary': True}])
        else:
            require(actual['equates'] == [] and source_cores ==
                    [ref_core(item) for item in before['references_from']],
                    'RENAME_SLOT_POST_%08x' % value)
    pre_targets = dict((int(row['address'], 16), row) for row in pre['ref_targets'])
    for value in REF_TARGETS:
        actual = address_state(value)
        before = pre_targets[value]
        additions = [{'from': '%08x' % slot, 'to': '%08x' % value,
                      'operand': 0, 'type': 'DATA', 'source': 'USER_DEFINED',
                      'primary': True}
                     for slot, row in sorted(SLOTS.items())
                     if row['action'] == 'REF' and
                     int(row['original_value'], 16) == value and
                     slot not in PREEXISTING_REF_SLOTS]
        same('TARGET_REFS_TO_POST_%08x' % value,
             [ref_core(item) for item in actual['references_to']],
             [ref_core(item) for item in before['references_to']] + additions)
        same('TARGET_REFS_FROM_POST_%08x' % value,
             [ref_core(item) for item in actual['references_from']],
             [ref_core(item) for item in before['references_from']])
        if value in (TABLE_BASE, CARVE_BASE):
            expected_name = TABLE_NAME if value == TABLE_BASE else CARVE_NAME
            require(actual['primary_symbol'] is not None and
                    actual['primary_symbol']['name'] == expected_name and
                    actual['primary_symbol']['source'] == 'USER_DEFINED' and
                    actual['primary_symbol']['global'], 'NEW_TARGET_LABEL_%08x' % value)
        else:
            require(actual['primary_symbol']['id'] == before['primary_symbol']['id'] and
                    actual['primary_symbol']['name'] == before['primary_symbol']['name'] and
                    actual['primary_symbol']['source'] == before['primary_symbol']['source'] and
                    actual['data_at'] == before['data_at'], 'STATIC_TARGET_POST_%08x' % value)
    pre_switches = dict((int(row['address'], 16), row) for row in pre['switch_sources'])
    for index, value in enumerate(SWITCH_SOURCES):
        actual = address_state(value)
        before = pre_switches[value]
        target = int(R4_MAP['case_entries'][index], 16)
        require(actual['bytes'] == before['bytes'] and actual['rom_word'] == target and
                actual['data_at'] == before['data_at'] and
                actual['defined_data_at'] == before['defined_data_at'] and
                actual['equates'] == before['equates'] and actual['eol'] == before['eol'],
                'SWITCH_STATIC_POST_%08x' % value)
        same('SWITCH_REF_POST_%08x' % value,
             [ref_core(item) for item in actual['references_from']],
             [ref_core(item) for item in before['references_from']])
        target_primary = symbols.getPrimarySymbol(toAddr(target))
        require(len(actual['references_from']) == 1 and
                actual['references_from'][0]['target_primary_id'] == long(target_primary.getID()) and
                actual['references_from'][0]['target_primary_name'] == unicode(target_primary.getName(True)),
                'SWITCH_DERIVED_TARGET_%08x' % value)
        if value == TABLE_BASE:
            require(actual['symbol_count'] == 1 and
                    actual['primary_symbol']['name'] == TABLE_NAME,
                    'TABLE_BASE_SOURCE_LABEL')
        else:
            require(actual['symbol_count'] == 0, 'SWITCH_SOURCE_NO_LABEL_%08x' % value)
    for value, name in sorted(CASE_NAMES.items()):
        state = address_state(value)
        require(state['symbol_count'] == 1 and state['primary_symbol']['name'] == name and
                state['primary_symbol']['source'] == 'USER_DEFINED' and
                state['primary_symbol']['global'] and state['primary_symbol']['primary'],
                'CASE_LABEL_POST_%08x' % value)
    pre_odds = dict((int(row['address'], 16), row) for row in pre['odd_targets'])
    for value in ODD_TARGETS:
        same('ODD_TARGET_POST_%08x' % value, address_state(value), pre_odds[value])
    pre_calls = dict((int(row['address'], 16), row) for row in pre['call_sites'])
    for value in CALL_SITES:
        actual = address_state(value)
        before = pre_calls[value]
        require(actual['bytes'] == before['bytes'] and
                actual['references_to'] == before['references_to'],
                'CALL_STATIC_POST_%08x' % value)
        same('CALL_REF_POST_%08x' % value,
             actual['references_from'], expected_refs(before['references_from']))
    for index, original in enumerate(CARVE_WORDS):
        value = CARVE_BASE + index * 4
        state = address_state(value)
        require(state['rom_word'] == original and state['defined_data_at'] is not None and
                state['defined_data_at']['type'] == '/undefined4' and
                state['defined_data_at']['length'] == 4 and
                state['equates'] == [] and state['references_from'] == [],
                'CARVE_WORD_POST_%08x' % value)
        if index == 0:
            require(state['symbol_count'] == 1 and
                    state['primary_symbol']['name'] == CARVE_NAME,
                    'CARVE_BASE_LABEL_POST')
        else:
            require(state['symbol_count'] == 0 and state['references_to'] == [],
                    'CARVE_TAIL_WORD_POST_%08x' % value)
    require(bytes_hex(CARVE_BOOKEND_START, 24) == pre['carve']['bookend_and_carve_bytes'] and
            raw_hash(CARVE_BOOKEND_START, CARVE_END) ==
            pre['carve']['bookend_to_tail_end_sha256'], 'CARVE_RAW_POST')
    if MODE == 'apply':
        same('APPLY_COUNTS', COUNTS, EXPECTED_COUNTS)

print('=== RefineF13Seg10 mode=%s ===' % MODE)
verify_inputs()
reject('INPUTS')

if MODE == 'prestate':
    state = capture()
    verify_prestate(state)
    reject('PRESTATE')
    write_json(PRESTATE_NAME, state)
    print('PRESTATE functions=17 slots=114 targets=5 switches=7 cases=7 '
          'odd=3 calls=8 segment_bytes=4160 FAIL=0')
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
        result = {
            'status': 'F13_SEG10_DRY_PREFLIGHT_OK', 'FAIL': 0,
            'script_sha256': file_hash(getSourceFile().getAbsolutePath()),
            'plan_sha256': file_hash(os.path.join(RUN, PLAN_NAME)),
            'prestate_sha256': prestate_hash,
            'source_snapshot_manifest_sha256':
                file_hash(os.path.join(RUN, SOURCE_SNAPSHOT_MANIFEST_NAME)),
            'counts': EXPECTED_COUNTS,
            'preflight': {'functions': 17, 'slots': 114, 'ref_targets': 5,
                          'switch_sources': 7, 'case_targets': 7,
                          'odd_targets': 3, 'call_sites': 8,
                          'segment_bytes': 4160, 'r4_instructions': 415,
                          'r4_pc_reads': 37, 'r4_flows': 67,
                          'r4_fallthroughs_final': 395},
            'semantic_actions_applied': False,
        }
        write_json('f13-seg10-dry-result.json', result)
        print('PREFLIGHT slots=114 EQ=47 REF=66 RENAME=1 EOL=114 '
              'FUNC_RENAME=8 PLATE=16 R4_INSTRUCTIONS=415 FUNCTIONS=17 FAIL=0')
        print('STATUS: OK mode=dry FAIL=0 semantic_actions_applied=false')
    elif MODE == 'check':
        verify_post(prestate)
        reject('PERSISTED_CHECK')
        write_json('f13-seg10-persisted-check.json', {
            'status': 'F13_SEG10_PERSISTED_CHECK_OK', 'FAIL': 0,
            'script_sha256': file_hash(getSourceFile().getAbsolutePath()),
            'plan_sha256': file_hash(os.path.join(RUN, PLAN_NAME)),
            'prestate_sha256': prestate_hash,
        })
        print('STATUS: OK mode=check FAIL=0 read_only=true')
    else:
        verify_prestate(prestate)
        reject('APPLY_PRESTATE')
        transaction = currentProgram.startTransaction('F13-Seg-10 approved materialization')
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
            write_json('f13-seg10-apply-failures.json', {
                'status': 'FAIL_ROLLED_BACK', 'FAIL': len(FAILS),
                'error': error_text, 'failures': FAILS,
                'transaction_committed': False,
            })
            raise RuntimeError('F13-Seg-10 apply rolled back')
        write_json('f13-seg10-apply-receipt.json', {
            'status': 'F13_SEG10_APPLY_OK', 'FAIL': 0,
            'script_sha256': file_hash(getSourceFile().getAbsolutePath()),
            'plan_sha256': file_hash(os.path.join(RUN, PLAN_NAME)),
            'prestate_sha256': prestate_hash, 'counts': COUNTS,
            'transaction_committed': True,
        })
        print('STATUS: OK mode=apply FAIL=0 transaction_committed=true')





