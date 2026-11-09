# -*- coding: ascii -*-
#@runtime Jython
#@category Ygo-ex2006.Refine
# F13-Seg-8 PASS materialization. prestate/dry/check are read-only.

import csv
import hashlib
import json
import os
import re

from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import RefType, SourceType


ARGS = list(getScriptArgs())
MODE = ARGS[0].lower() if ARGS else 'dry'
if MODE not in ('prestate', 'dry', 'apply', 'check'):
    raise RuntimeError('Expected prestate, dry, apply, or check')

ROOT = os.path.abspath(os.path.join(str(getSourceFile().getParentFile()), '..', '..'))
RUN = os.path.join(ROOT, 'output', 'refine-run-20261011-103530')
PLAN_NAME = 'f13-seg8-plan.json'
PRESTATE_NAME = 'f13-seg8-fresh-full-prestate.json'
SOURCE_SNAPSHOT_MANIFEST_NAME = 'f13-seg8-source-snapshot-preapply-v3.json'
AUXILIARY_PLAN_HASHES = {
    'review_mode_a_gate_sha256': 'root-f13-seg8-mode-a-independent-gate.json',
    'baseline_v2_sha256': 'root-f13-seg8-baseline-v2.json',
    'db_backup_manifest_sha256': 'root-f13-seg8-db-backup.json',
}
INPUT_HASHES = {
    'doc/dev/refine/F13-Seg-8.proposal.md': '5835bdaaf66fe4269cbcc552db086f02e1dc63eee115f077a4686f50256fa731',
    'doc/dev/refine/F13-Seg-8.review.md': '232083904d5131c494fe00e4c20de0ace978c1855e49fdbfb2a0ec72e66d981a',
    'doc/dev/refine/F13-Seg-8.slots.tsv': 'c62a1ff6516fbfe9e51e1c584ce734d7a3d702975f1303f821f1a0e9e6842db6',
    'doc/dev/refine/F13-Seg-8.plates.tsv': 'a470fdbf187bb779d4fbbea8d0fd0b5a989ad276957beb0a3896ecd770083c76',
}
EXPECTED_COUNTS = {
    'EQ': 112, 'REF': 26, 'RENAME': 17, 'EOL': 155,
    'FUNC_RENAME': 4, 'PLATE': 14,
}
SEGMENT_START = 0x080a46a0
SEGMENT_END = 0x080a585c
ODDWORDS = [
    0x080a6434, 0x080a6474, 0x080a655c, 0x080a65d4,
    0x080a668c, 0x080a66d4, 0x080a67c0, 0x080a6800,
    0x080a6900, 0x080a6948, 0x080a6a74, 0x080a6abc,
]

listing = currentProgram.getListing()
symbols = currentProgram.getSymbolTable()
references = currentProgram.getReferenceManager()
equates = currentProgram.getEquateTable()
memory = currentProgram.getMemory()
functions = currentProgram.getFunctionManager()
global_ns = currentProgram.getGlobalNamespace()
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
        write_json('f13-seg8-%s-failures.json' % MODE, {
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


SLOT_ROWS = read_tsv('doc/dev/refine/F13-Seg-8.slots.tsv')
PLATE_ROWS = read_tsv('doc/dev/refine/F13-Seg-8.plates.tsv')
SLOTS = dict((int(row['address'], 16), row) for row in SLOT_ROWS)
PLATES = dict((int(row['entry'], 16), row) for row in PLATE_ROWS)
FUNCTIONS = sorted(PLATES)
RENAMES = dict((value, row) for value, row in PLATES.items()
               if row['current_name'] != row['final_name'])
TARGETS = {}
for value, row in SLOTS.items():
    if row['action'] in ('REF', 'RENAME'):
        target = int(row['original_value'], 16)
        match = re.search(r'id=([0-9]+)', row['target_contract'])
        TARGETS[target] = {
            'address': target, 'name': row['target_symbol'],
            'id': None if match is None else long(match.group(1)),
        }


def verify_inputs():
    for relative, digest in sorted(INPUT_HASHES.items()):
        same('INPUT_HASH_' + relative,
             file_hash(os.path.join(ROOT, relative)), digest)
    require(len(SLOTS) == 155 and len(SLOT_ROWS) == 155, 'SLOT_COUNT')
    require(sum(row['action'] == 'EQ' for row in SLOT_ROWS) == 112, 'EQ_COUNT')
    require(sum(row['action'] == 'REF' for row in SLOT_ROWS) == 26, 'REF_COUNT')
    require(sum(row['action'] == 'RENAME' for row in SLOT_ROWS) == 17, 'RENAME_COUNT')
    require(len(PLATES) == 14 and len(RENAMES) == 4, 'FUNCTION_PLATE_COUNTS')
    require(len(TARGETS) == 4, 'TARGET_COUNT')
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


def capture():
    odd_rows = []
    for value in ODDWORDS:
        state = address_state(value)
        target = state['rom_word']
        odd_rows.append({
            'source': state,
            'odd_target': address_state(target),
            'even_function': function_row(target - 1),
        })
    return {
        'status': 'F13_SEG8_FRESH_FULL_PRESTATE',
        'program_name': unicode(currentProgram.getName()),
        'function_count': int(functions.getFunctionCount()),
        'segment': {'start': '0x%08x' % SEGMENT_START, 'end': '0x%08x' % SEGMENT_END,
                    'size': SEGMENT_END - SEGMENT_START,
                    'sha256': raw_hash(SEGMENT_START, SEGMENT_END)},
        'functions': [function_row(value) for value in FUNCTIONS],
        'slots': [address_state(value) for value in sorted(SLOTS)],
        'targets': [address_state(value) for value in sorted(TARGETS)],
        'oddwords': odd_rows,
    }


def verify_prestate(pre):
    same('FRESH_PRESTATE_EXACT', capture(), pre)
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
            require(cores == [{'from': '%08x' % value,
                               'to': '%08x' % int(row['original_value'], 16),
                               'operand': 0, 'type': 'DATA', 'source': 'DEFAULT',
                               'primary': True}], 'RENAME_REF_%08x' % value)
        else:
            require(cores == [], 'EMPTY_REF_%08x' % value)
    for value, contract in sorted(TARGETS.items()):
        state = address_state(value)
        require(state['primary_symbol'] is not None and
                state['primary_symbol']['id'] == contract['id'] and
                state['primary_symbol']['name'] == contract['name'] and
                state['primary_symbol']['source'] == 'USER_DEFINED',
                'TARGET_STATIC_%08x' % value)
    for value, row in sorted(PLATES.items()):
        state = function_row(value)
        require(state is not None and state['name'] == row['current_name'] and
                state['symbol']['id'] == long(row['function_id']) and
                state['symbol']['source'] == row['function_source'] and
                state['body'] == row['body'] and state['body_size'] == int(row['body_size']) and
                len(state['plate']) == int(row['old_plate_chars']),
                'FUNCTION_STATIC_%08x' % value)
        require(state['return'] is not None and 'storage' in state['return'] and
                'source' in state['return'] and state['calling_convention'] is not None and
                state['namespace']['id'] is not None,
                'FUNCTION_COMPLETE_METADATA_%08x' % value)
        require(len(state['body_references']) >= 0, 'FUNCTION_BODY_REFS_%08x' % value)
        collisions = [symbol for symbol in symbols.getGlobalSymbols(row['final_name'])
                      if symbol.getAddress() != toAddr(value)]
        require(not collisions, 'FUNCTION_NAME_COLLISION_%08x' % value)
    expected_types = ['/undefined4'] * 6 + ['/dword'] * 6
    for index, value in enumerate(ODDWORDS):
        state = address_state(value)
        require(state['data_at'] is not None and state['data_at']['type'] == expected_types[index] and
                state['references_from'] == [] and state['equates'] == [] and
                len(state['references_to']) == 1 and state['rom_word'] & 1 == 1,
                'ODDWORD_STATIC_%08x' % value)


def verify_plan(plan, prestate_hash):
    require(plan.get('status') == 'F13_SEG8_PLAN_FROZEN', 'PLAN_STATUS')
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
            plan.get('oddword_addresses') == ODDWORDS and
            plan.get('function_addresses') == FUNCTIONS,
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
        'body_sha256', 'eol_comments', 'calling_convention', 'signature_source',
        'prototype', 'custom_variable_storage', 'varargs', 'inline', 'no_return',
        'external', 'thunk', 'thunk_target', 'stack_purge_size', 'return', 'parameters'))


def verify_post(pre):
    require(int(functions.getFunctionCount()) == int(pre['function_count']),
            'FUNCTION_COUNT_POST')
    require(raw_hash(SEGMENT_START, SEGMENT_END) == pre['segment']['sha256'],
            'SEGMENT_RAW_HASH_POST')
    pre_functions = dict((int(row['entry'], 16), row) for row in pre['functions'])
    pre_slots = dict((int(row['address'], 16), row) for row in pre['slots'])
    pre_targets = dict((int(row['address'], 16), row) for row in pre['targets'])
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
        require(actual['primary_symbol']['id'] == before['primary_symbol']['id'] and
                actual['primary_symbol']['name'] == before['primary_symbol']['name'] and
                actual['primary_symbol']['source'] == 'USER_DEFINED' and
                actual['data_at'] == before['data_at'] and actual['bytes'] == before['bytes'],
                'TARGET_POST_%08x' % value)
        expected = [ref_core(item) for item in before['references_to']]
        expected += [{'from': '%08x' % slot, 'to': '%08x' % value, 'operand': 0,
                      'type': 'DATA', 'source': 'USER_DEFINED', 'primary': True}
                     for slot, row in sorted(SLOTS.items())
                     if row['action'] == 'REF' and int(row['original_value'], 16) == value]
        same('TARGET_REFS_POST_%08x' % value,
             [ref_core(item) for item in actual['references_to']], expected)
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
        same('FUNCTION_INCOMING_POST_%08x' % value,
             [ref_core(item) for item in actual['incoming']],
             [ref_core(item) for item in before['incoming']])
        same('FUNCTION_BODY_REFS_POST_%08x' % value,
             [ref_core(item) for item in actual['body_references']],
             [ref_core(item) for item in before['body_references']])
    for index, value in enumerate(ODDWORDS):
        before = pre['oddwords'][index]
        same('ODDWORD_SOURCE_POST_%08x' % value,
             address_state(value), before['source'])
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
        same('ODDWORD_TARGET_POST_%08x' % target,
             address_state(target), expected_target)
    same('APPLY_COUNTS', COUNTS, EXPECTED_COUNTS)


def row_value(value):
    return long(value)


print('=== RefineF13Seg8 mode=%s ===' % MODE)
verify_inputs()
reject('INPUTS')

if MODE == 'prestate':
    state = capture()
    verify_prestate(state)
    reject('PRESTATE')
    write_json(PRESTATE_NAME, state)
    print('PRESTATE functions=14 slots=155 targets=4 oddwords=12 FAIL=0')
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
        write_json('f13-seg8-dry-result.json', {
            'status': 'F13_SEG8_DRY_PREFLIGHT_OK', 'FAIL': 0,
            'script_sha256': file_hash(getSourceFile().getAbsolutePath()),
            'plan_sha256': file_hash(os.path.join(RUN, PLAN_NAME)),
            'prestate_sha256': prestate_hash,
            'counts': EXPECTED_COUNTS,
            'preflight': {'functions': 14, 'slots': 155, 'targets': 4, 'oddwords': 12},
            'semantic_actions_applied': False,
        })
        print('PREFLIGHT slots=155 EQ=112 REF=26 RENAME=17 EOL=155 '
              'FUNC_RENAME=4 PLATE=14 FUNCTIONS=14 TARGETS=4 ODDWORDS=12 FAIL=0')
        print('STATUS: OK mode=dry FAIL=0 semantic_actions_applied=false')
    elif MODE == 'check':
        receipt = read_json('f13-seg8-apply-receipt.json')
        require(receipt.get('status') == 'F13_SEG8_APPLIED_POSTCHECK_OK' and
                receipt.get('counts') == EXPECTED_COUNTS and
                receipt.get('script_sha256') == file_hash(getSourceFile().getAbsolutePath()) and
                receipt.get('plan_sha256') == file_hash(os.path.join(RUN, PLAN_NAME)),
                'RECEIPT_CONTRACT')
        reject('RECEIPT')
        same('PERSISTED_EXACT', capture(), receipt['after'])
        reject('PERSISTED')
        write_json('f13-seg8-persisted-check.json', {
            'status': 'F13_SEG8_PERSISTED_CHECK_OK', 'FAIL': 0,
            'script_sha256': receipt['script_sha256'],
            'plan_sha256': receipt['plan_sha256'],
            'counts': EXPECTED_COUNTS,
        })
        print('STATUS: OK mode=check FAIL=0 PERSISTED_EXACT=true')
    else:
        verify_prestate(prestate)
        reject('APPLY_PREFLIGHT')
        transaction = currentProgram.startTransaction('Refine F13-Seg-8 approved transaction')
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
            raise RuntimeError('F13-Seg-8 transaction rolled back')
        receipt = {
            'status': 'F13_SEG8_APPLIED_POSTCHECK_OK', 'FAIL': 0,
            'script_sha256': file_hash(getSourceFile().getAbsolutePath()),
            'plan_sha256': file_hash(os.path.join(RUN, PLAN_NAME)),
            'prestate_sha256': prestate_hash,
            'counts': EXPECTED_COUNTS, 'after': after,
        }
        write_json('f13-seg8-apply-receipt.json', receipt)
        print('STATUS: OK mode=apply FAIL=0 transaction=committed')
