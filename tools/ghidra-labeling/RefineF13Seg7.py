# -*- coding: ascii -*-
#@runtime Jython
#@category Ygo-ex2006.Refine
# F13-Seg-7 PASS materialization. Dry/check are read-only; apply is one transaction.

import hashlib
import json
import os
import re

from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import RefType, SourceType


MODE = list(getScriptArgs())[0].lower() if list(getScriptArgs()) else 'dry'
if MODE not in ('dry', 'apply', 'check'):
    raise RuntimeError('Expected dry, apply, or check')

ROOT = os.path.abspath(os.path.join(str(getSourceFile().getParentFile()), '..', '..'))
RUN = os.path.join(ROOT, 'output', 'refine-run-20260831-194634')
PLAN_NAME = 'f13-seg7-plan.json'
INPUT_HASHES = [
    ('doc/dev/refine/F13-Seg-7.proposal.md', '129f42778a7ed9da2ec4e082da91d71577532e56016d4f2cb394e797a8d63a99'),
    ('doc/dev/refine/F13-Seg-7.review.md', '80fbd95458a16cb7faea369ff2051905b1b4cf6f8e5ebab9fb022ded0f60b926'),
    ('doc/dev/refine/F13-Seg-7.slots.tsv', '2bd2619525cf56f5a996a2c8eb4dd91161958b1e825906d91e680e690221a99f'),
    ('output/refine-run-20260831-194634/f13-seg7-refscan.tsv', 'e98fe19aa98963f587f62ef05107aad86e1a2aa3292d4a7b54cb8472c276d52a'),
    ('output/refine-run-20260831-194634/f13-seg7-functions.tsv', '57e4d3cf6a5720d6ddf7d20074fdddd58a688489f6c125e3397de7c2940301c3'),
    ('output/refine-run-20260831-194634/f13-seg7-direct-edges.tsv', 'afc0106593069583a9ad418b6e4c5501bc6f277a3eac92d90208c1200632767e'),
    ('output/refine-run-20260831-194634/f13-seg7-literal-reads.tsv', '62c42d3f553e240641073f3b9ed41e11d5a5943b8f3ebb41e21f6f0e0d23d5d1'),
    ('output/refine-run-20260831-194634/f13-seg7-consumers.tsv', 'd81ef5de9411ffbf0eaf8a1e17da5f186b2a95e5c1c2bbc90886b142a61a4eb1'),
    ('output/refine-run-20260831-194634/f13-seg7-layout.json', 'c2487fa74d1ee2f348e0e8e07c0f8f816c131004c93a6b1a79ad98cec1a50798'),
    ('output/refine-run-20260831-194634/F13Seg7ProposalPrestate.py', '13d5032c70438ca67cd5ad8e8bdbc2089cb70cdee6606c0f2ea7f196f760d51f'),
    ('output/refine-run-20260831-194634/f13-seg7-ghidra-prestate.json', '54d59f1f9cdad65c034da875f92f367944adba41ab332a93b4a5e031ddf0a623'),
    ('output/refine-run-20260831-194634/f13-seg7-ghidra-prestate-gate.json', '57efed71e2db94267a220d69f0c07478371c117c2157742a363db9a03a2ccbab'),
    ('output/refine-run-20260831-194634/f13-seg7-modea2-selfcheck.json', 'e5ec57751e8531fbdd4dd92cfd6d7ad5d6039fdcde0d9c3f8a7dabb499834d6e'),
    ('output/refine-run-20260831-194634/f13-seg7-preapply-backup.json', '3f2b848200de1bd02c4e9c97d3b44c6c62264a0958b72b7a3b2649cc8f03aac6'),
    ('output/refine-run-20260831-194634/InspectF13Seg7FullPrestate.py', '4a8491751b9447771805a173133582e0797a65f461c11a93540b03231d564db1'),
    ('output/refine-run-20260831-194634/f13-seg7-full-prestate.json', 'df66e641ac7d66a1197a4a73ac1e24c75b4651af551f00c0f1eac2e4bd96ec3f'),
    ('output/refine-run-20260831-194634/f13-seg7-full-prestate-gate.json', '9f24e63bfd53a012b96c654845b2354d122677ec03a1cc48aaa7c5368cc85275'),
    ('output/refine-run-20260831-194634/f13-seg7-plan.json', '772b89fab666c9ad09516aff6e3e8c3a3984db91d393cef99ede87e425edbe6b'),
]

listing = currentProgram.getListing()
symbols = currentProgram.getSymbolTable()
references = currentProgram.getReferenceManager()
equates = currentProgram.getEquateTable()
memory = currentProgram.getMemory()
functions = currentProgram.getFunctionManager()
context = currentProgram.getProgramContext()
tmode = context.getRegister('TMode')
global_ns = currentProgram.getGlobalNamespace()
FAILS = []
EXPECTED_APPLY_COUNTS = {
    'EQ': 73, 'REF': 19, 'RENAME': 4, 'EOL': 96,
    'FUNC_RENAME': 9, 'PLATE': 14, 'CARVE': 2, 'FIXED_OLD_NAME_SCAN': 9,
}
COUNTS = dict((key, 0) for key in EXPECTED_APPLY_COUNTS)


def read_json(name):
    with open(os.path.join(RUN, name), 'rb') as stream:
        return json.load(stream)


def write_json(name, value):
    with open(os.path.join(RUN, name), 'w') as stream:
        stream.write(json.dumps(value, ensure_ascii=True, sort_keys=True, indent=2) + '\n')


def file_hash(path):
    with open(path, 'rb') as stream:
        return hashlib.sha256(stream.read()).hexdigest()


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
    actual_text = json.dumps(canonical(actual), ensure_ascii=True, sort_keys=True, separators=(',', ':'))
    expected_text = json.dumps(canonical(expected), ensure_ascii=True, sort_keys=True, separators=(',', ':'))
    if actual_text != expected_text:
        fail(message, actual, expected)


def reject(phase):
    if FAILS:
        write_json('f13-seg7-%s-failures.json' % MODE,
                   {'status': 'FAIL', 'phase': phase, 'FAIL': len(FAILS), 'failures': FAILS})
        raise RuntimeError('%s FAIL=%d' % (phase, len(FAILS)))


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
        'id': long(symbol.getID()),
        'name': unicode(symbol.getName()),
        'qualified_name': unicode(symbol.getName(True)),
        'type': str(symbol.getSymbolType()),
        'source': str(symbol.getSource()),
        'primary': bool(symbol.isPrimary()),
        'namespace': None if parent is None else unicode(parent.getName()),
        'global': parent == global_ns,
    }


def ref_row(ref):
    target_primary = symbols.getPrimarySymbol(ref.getToAddress())
    return {
        'from': str(ref.getFromAddress()),
        'to': str(ref.getToAddress()),
        'operand': int(ref.getOperandIndex()),
        'type': str(ref.getReferenceType()),
        'source': str(ref.getSource()),
        'primary': bool(ref.isPrimary()),
        'target_primary_id': None if target_primary is None else long(target_primary.getID()),
        'target_primary_name': None if target_primary is None else unicode(target_primary.getName(True)),
    }


def ref_core(ref):
    return dict((key, ref[key]) for key in ('from', 'to', 'operand', 'type', 'source', 'primary'))


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


def address_state(value, byte_length=4):
    addr = toAddr(value)
    instruction = listing.getInstructionAt(addr)
    fn = functions.getFunctionAt(addr)
    symbol_list = [symbol_row(symbol) for symbol in symbols.getSymbols(addr)]
    primary = symbols.getPrimarySymbol(addr)
    return {
        'address': '0x%08x' % value,
        'bytes': bytes_hex(value, byte_length),
        'symbols': symbol_list,
        'symbol_count': len(symbol_list),
        'primary_symbol': None if primary is None else symbol_row(primary),
        'data_at': data_row(listing.getDefinedDataAt(addr)),
        'data_containing': data_row(listing.getDefinedDataContaining(addr)),
        'instruction': None if instruction is None else unicode(instruction.toString()),
        'function': None if fn is None else unicode(fn.getName()),
        'references_from': [ref_row(ref) for ref in references.getReferencesFrom(addr)],
        'references_to': [ref_row(ref) for ref in references.getReferencesTo(addr)],
        'equates': sorted([{'name': unicode(eq.getName()), 'value': long(eq.getValue())}
                           for eq in equates.getEquates(addr)], key=lambda row: (row['name'], row['value'])),
        'eol': listing.getComment(CodeUnit.EOL_COMMENT, addr),
        'plate': listing.getComment(CodeUnit.PLATE_COMMENT, addr),
    }


def body_ranges(fn):
    result = []
    iterator = fn.getBody().getAddressRanges()
    while iterator.hasNext():
        item = iterator.next()
        result.append([
            '0x%08x' % int(item.getMinAddress().getOffset()),
            '0x%08x' % (int(item.getMaxAddress().getOffset()) + 1),
        ])
    return result


def function_row(value):
    addr = toAddr(value)
    fn = functions.getFunctionAt(addr)
    if fn is None:
        return None
    symbol = fn.getSymbol()
    params = []
    for param in fn.getParameters():
        params.append({
            'ordinal': int(param.getOrdinal()),
            'name': unicode(param.getName()),
            'data_type': unicode(param.getDataType().getPathName()),
            'storage': unicode(param.getVariableStorage().toString()),
            'source': str(param.getSource()),
        })
    symbol_list = [symbol_row(item) for item in symbols.getSymbols(addr)]
    return {
        'entry': '0x%08x' % value,
        'name': unicode(fn.getName()),
        'symbol': symbol_row(symbol),
        'symbols': symbol_list,
        'symbol_count': len(symbol_list),
        'body_ranges': body_ranges(fn),
        'body_size': int(fn.getBody().getNumAddresses()),
        'calling_convention': unicode(fn.getCallingConventionName()),
        'return_type': unicode(fn.getReturnType().getPathName()),
        'parameters': params,
        'plate': listing.getComment(CodeUnit.PLATE_COMMENT, addr),
        'incoming': [ref_row(ref) for ref in references.getReferencesTo(addr)],
    }


def sign_extend(value, bits):
    sign = 1 << (bits - 1)
    return (value ^ sign) - sign


def halfword(value):
    return (memory.getByte(toAddr(value)) & 255) | ((memory.getByte(toAddr(value + 1)) & 255) << 8)


def decode_edges(ranges):
    result = []
    for lo, hi in ranges:
        cursor = lo
        while cursor < hi:
            first = halfword(cursor)
            if first & 0xf800 == 0xf000 and cursor + 4 <= hi:
                second = halfword(cursor + 2)
                if second & 0xf800 == 0xf800:
                    immediate = ((first & 0x7ff) << 12) | ((second & 0x7ff) << 1)
                    target = (cursor + 4 + sign_extend(immediate, 23)) & 0xffffffff
                    result.append({'source': cursor, 'kind': 'BL', 'target': target,
                                   'rom_bytes': bytes_hex(cursor, 4)})
                    cursor += 4
                    continue
            if first & 0xf000 == 0xd000 and ((first >> 8) & 15) < 14:
                target = (cursor + 4 + sign_extend(first & 255, 8) * 2) & 0xffffffff
                result.append({'source': cursor, 'kind': 'Bcc', 'target': target,
                               'rom_bytes': bytes_hex(cursor, 2)})
            elif first & 0xf800 == 0xe000:
                target = (cursor + 4 + sign_extend(first & 0x7ff, 11) * 2) & 0xffffffff
                result.append({'source': cursor, 'kind': 'B', 'target': target,
                               'rom_bytes': bytes_hex(cursor, 2)})
            cursor += 2
    return result


def instruction_summary(ranges):
    count = 0
    total = 0
    for lo, hi in ranges:
        cursor = lo
        while cursor < hi:
            instruction = listing.getInstructionAt(toAddr(cursor))
            require(instruction is not None, 'INSTRUCTION_MISSING_%08x' % cursor)
            if instruction is None:
                break
            length = int(instruction.getLength())
            require(length > 0 and cursor + length <= hi, 'INSTRUCTION_RANGE_%08x' % cursor)
            mode = context.getValue(tmode, toAddr(cursor), False)
            require(mode is not None and int(mode) == 1, 'TMODE_%08x' % cursor)
            cursor += length
            count += 1
            total += length
        require(cursor == hi, 'INSTRUCTION_COVERAGE_%08x_%08x' % (lo, hi))
    return {'ranges': len(ranges), 'instructions': count, 'bytes': total}


PLAN = read_json(PLAN_NAME)
SCRIPT_HASH = file_hash(getSourceFile().getAbsolutePath())
SLOTS = dict((row['address'], row) for row in PLAN['slots'])
TARGETS = dict((row['address'], row) for row in PLAN['targets'])
SEGMENT_FUNCTIONS = dict((row['entry'], row) for row in PLAN['segment_functions'])
RENAMES = dict((row['entry'], row) for row in PLAN['renames'])
PLATES = dict((row['address'], row['text']) for row in PLAN['plates'])
PLATE_PRE = dict((int(row['entry'], 16), row) for row in PLAN['plate_prestate'])
CODE_RANGES = [tuple(pair) for pair in PLAN['code_ranges']]
PADDING = [tuple(pair) for pair in PLAN['padding']]
OLD_NAMES = list(PLAN['old_name_scan'])


def verify_frozen_plan():
    for relative, digest in INPUT_HASHES:
        same('INPUT_HASH_' + relative, file_hash(os.path.join(ROOT, relative)), digest)
    expected_inputs = dict((relative_key, digest) for relative_key, digest in (
        ('proposal', INPUT_HASHES[0][1]), ('review', INPUT_HASHES[1][1]),
        ('tsv', INPUT_HASHES[2][1]), ('refscan', INPUT_HASHES[3][1]),
        ('functions', INPUT_HASHES[4][1]), ('edges', INPUT_HASHES[5][1]),
        ('literal_reads', INPUT_HASHES[6][1]), ('consumers', INPUT_HASHES[7][1]),
        ('layout', INPUT_HASHES[8][1]), ('proposal_query', INPUT_HASHES[9][1]),
        ('proposal_prestate', INPUT_HASHES[10][1]),
        ('proposal_prestate_gate', INPUT_HASHES[11][1]),
        ('modea2_selfcheck', INPUT_HASHES[12][1]), ('backup', INPUT_HASHES[13][1]),
        ('full_query', INPUT_HASHES[14][1]), ('full_prestate', INPUT_HASHES[15][1]),
        ('full_prestate_gate', INPUT_HASHES[16][1])))
    same('PLAN_INPUT_HASHES', PLAN['input_hashes'], expected_inputs)
    require(PLAN['status'] == 'F13_SEG7_PLAN_OK', 'PLAN_STATUS')
    require(PLAN['range'] == [0x080a38fc, 0x080a46a0] and PLAN['range_size'] == 3492,
            'SEGMENT_RANGE')
    same('EXPECTED_APPLY_COUNTS', PLAN['expected_counts'], EXPECTED_APPLY_COUNTS)
    require(len(SLOTS) == 96 and len(PLAN['slots']) == 96, 'SLOT_COUNT')
    require([sum(row['action'] == kind for row in PLAN['slots'])
             for kind in ('EQ', 'REF', 'RENAME')] == [73, 19, 4], 'ACTION_COUNTS')
    require(len(TARGETS) == 8 and len(SEGMENT_FUNCTIONS) == 22 and len(RENAMES) == 9,
            'OBJECT_COUNTS')
    require(len(PLATES) == 14 and len(PLATE_PRE) == 14, 'PLATE_COUNTS')
    require(len(CODE_RANGES) == 65 and sum(hi - lo for lo, hi in CODE_RANGES) == 3050,
            'CODE_RANGE_COUNTS')
    require(len(PADDING) == 29 and sum(hi - lo for lo, hi in PADDING) == 58,
            'PADDING_COUNTS')
    require(len(PLAN['edges']) == 305 and
            PLAN['edge_counts'] == {'B': 60, 'BL': 82, 'Bcc': 163}, 'EDGE_COUNTS')
    require(len(PLAN['new_constants']) == 11 and len(PLAN['gas_aliases']) == 3 and
            len(PLAN['carves']) == 2, 'SOURCE_SYMBOL_COUNTS')
    require(PLAN['function_pre_count'] == PLAN['function_post_count'] == 5213,
            'FUNCTION_TOTAL')
    require(len(OLD_NAMES) == len(set(OLD_NAMES)) == 9, 'OLD_NAME_SCAN_COUNT')
    require(PLAN['extra_auto_name_scan'] == 'FUN_08094f58', 'AUTO_NAME_SCAN')
    require(raw_hash(0x080a38fc, 0x080a46a0) == PLAN['segment_sha256'], 'SEGMENT_ROM_SHA')
    for value, row in SLOTS.items():
        require(row['address'] == value and re.match(r'^[a-z][a-z0-9_]+$', row['slot_label']) is not None,
                'SLOT_NAME_%08x' % value)
        require(all(ord(char) < 128 for char in row['eol']), 'EOL_ASCII_%08x' % value)
    for value, text in PLATES.items():
        require(all(ord(char) < 128 for char in text) and len(text) < 500,
                'PLATE_ASCII_%08x' % value)
    for row in PLAN['odd_callbacks']:
        require(row['slot'] in SLOTS and SLOTS[row['slot']]['action'] == 'EQ' and
                row['stored_value'] == row['odd_target'] == row['even_entry'] + 1 and
                row['alias'] == SLOTS[row['slot']]['target'], 'ODD_CALLBACK_PLAN_%08x' % row['slot'])


def verify_prestate():
    require(functions.getFunctionCount() == 5213, 'FUNCTION_COUNT_PRE')
    require(raw_hash(0x080a38fc, 0x080a46a0) == PLAN['segment_sha256'], 'SEGMENT_ROM_PRE')
    for value, row in sorted(SLOTS.items()):
        same('SLOT_PRE_%08x' % value, address_state(value), row['pre'])
        require(memory.getInt(toAddr(value)) & 0xffffffff == row['value'],
                'SLOT_ROM_%08x' % value)
        eq = equates.getEquate(row['target']) if row['action'] == 'EQ' else None
        if row['action'] == 'EQ' and row['reuse_status'] == 'REUSE':
            # REUSE is the source-constant contract, not a claim that this
            # prestate already contains a Ghidra Equate object.
            require(eq is None or (eq.getValue() & 0xffffffff) == row['value'],
                    'REUSE_EQUATE_VALUE_%08x' % value)
        if row['action'] == 'EQ' and row['reuse_status'] == 'NEW':
            require(eq is None, 'NEW_EQUATE_ABSENT_%08x' % value)
    for value, contract in sorted(TARGETS.items()):
        length = 12 if value in (0x09e47898, 0x09e478a4) else 4
        same('TARGET_PRE_%08x' % value, address_state(value, length), contract['pre'])
        collisions = [symbol for symbol in symbols.getGlobalSymbols(contract['post_name'])
                      if symbol.getAddress() != toAddr(value)]
        require(not collisions, 'TARGET_NAME_COLLISION_%08x' % value)
    for value, contract in sorted(SEGMENT_FUNCTIONS.items()):
        same('SEGMENT_FUNCTION_PRE_%08x' % value, function_row(value), contract['pre'])
    for value, contract in sorted(PLATE_PRE.items()):
        same('PLATE_FUNCTION_PRE_%08x' % value, function_row(value), contract)
    for value, contract in sorted(RENAMES.items()):
        same('RENAME_FUNCTION_PRE_%08x' % value, function_row(value), contract['pre'])
        collisions = [symbol for symbol in symbols.getGlobalSymbols(contract['post_name'])
                      if symbol.getAddress() != toAddr(value)]
        require(not collisions, 'FUNCTION_NAME_COLLISION_%08x' % value)
    for row in PLAN['odd_callbacks']:
        same('ODD_SLOT_PRE_%08x' % row['slot'], address_state(row['slot']), row['pre']['slot'])
        same('ODD_TARGET_PRE_%08x' % row['odd_target'], address_state(row['odd_target']), row['pre']['odd_target'])
        same('ODD_EVEN_FUNCTION_PRE_%08x' % row['even_entry'], function_row(row['even_entry']), row['pre']['even_function'])
    same('CODE_SUMMARY_PRE', instruction_summary(CODE_RANGES),
         {'ranges': 65, 'instructions': 1443, 'bytes': 3050})
    for lo, hi in PADDING:
        require(bytes_hex(lo, hi - lo) == '00' * (hi - lo), 'PADDING_BYTES_%08x' % lo)
        for value in range(lo, hi):
            require(listing.getInstructionContaining(toAddr(value)) is None and
                    listing.getDefinedDataContaining(toAddr(value)) is None,
                    'PADDING_LISTING_%08x' % value)
    decoded = decode_edges(CODE_RANGES)
    expected = [dict((key, row[key]) for key in ('source', 'kind', 'target', 'rom_bytes'))
                for row in PLAN['edges']]
    same('DIRECT_EDGES_PRE', decoded, expected)
    print('PREFLIGHT slots=96 EQ=73 REF=19 RENAME=4 TARGETS=8 RANGES=65 '
          'INSTRUCTIONS=1443 BYTES=3050 PADDING=29 FUNCTIONS=22 FUNC_RENAME=9 '
          'PLATE=14 EOL=96 CARVE=2 EDGES=305 FAIL=%d' % len(FAILS))


def normalize_target(value, contract):
    addr = toAddr(value)
    primary = symbols.getPrimarySymbol(addr)
    at_addr = list(symbols.getSymbols(addr))
    pre_symbol = contract['pre']['primary_symbol']
    if not (len(at_addr) == 1 and primary is not None and primary.isPrimary() and
            long(primary.getID()) == pre_symbol['id'] and
            unicode(primary.getName()) == pre_symbol['name'] and
            str(primary.getSource()) == pre_symbol['source']):
        raise RuntimeError('Target symbol precondition failed at %08x' % value)
    collisions = [symbol for symbol in symbols.getGlobalSymbols(contract['post_name'])
                  if symbol.getAddress() != addr]
    if collisions:
        raise RuntimeError('Target name collision: ' + contract['post_name'])
    if primary.getParentNamespace() != global_ns:
        primary.setNameAndNamespace(contract['post_name'], global_ns, SourceType.USER_DEFINED)
    else:
        primary.setName(contract['post_name'], SourceType.USER_DEFINED)
    post = symbols.getPrimarySymbol(addr)
    if (post is None or unicode(post.getName()) != contract['post_name'] or
            str(post.getSource()) != 'USER_DEFINED' or not post.isPrimary() or
            post.getParentNamespace() != global_ns or len(list(symbols.getSymbols(addr))) != 1):
        raise RuntimeError('Target normalization failed at %08x' % value)
    if contract['preserve_id'] and long(post.getID()) != pre_symbol['id']:
        raise RuntimeError('Target identity changed at %08x' % value)


def ensure_slot_label(value, name):
    addr = toAddr(value)
    primary = symbols.getPrimarySymbol(addr)
    at_addr = list(symbols.getSymbols(addr))
    if len(at_addr) != 1 or primary is None or not primary.isPrimary():
        raise RuntimeError('Slot Symbol precondition failed at %08x' % value)
    collisions = [symbol for symbol in symbols.getGlobalSymbols(name) if symbol.getAddress() != addr]
    if collisions:
        raise RuntimeError('Slot label collision: ' + name)
    if primary.getParentNamespace() != global_ns:
        primary.setNameAndNamespace(name, global_ns, SourceType.USER_DEFINED)
    else:
        primary.setName(name, SourceType.USER_DEFINED)
    post = symbols.getPrimarySymbol(addr)
    if (post is None or unicode(post.getName()) != name or str(post.getSource()) != 'USER_DEFINED' or
            not post.isPrimary() or post.getParentNamespace() != global_ns or
            len(list(symbols.getSymbols(addr))) != 1):
        raise RuntimeError('Slot label failed at %08x' % value)


def apply_slot(row):
    value = row['address']
    addr = toAddr(value)
    if (memory.getInt(addr) & 0xffffffff) != row['value']:
        raise RuntimeError('ROM value changed at %08x' % value)
    same('SLOT_DATA_BEFORE_%08x' % value, data_row(listing.getDefinedDataAt(addr)), row['pre']['data_at'])
    if FAILS:
        raise RuntimeError('Slot Data precondition failed at %08x' % value)
    if row['action'] == 'EQ':
        eq = equates.getEquate(row['target'])
        if eq is None:
            eq = equates.createEquate(row['target'], row['value'])
        elif (eq.getValue() & 0xffffffff) != row['value']:
            raise RuntimeError('Equate conflict: ' + row['target'])
        eq.addReference(addr, 0)
    elif row['action'] == 'REF':
        existing = [ref for ref in references.getReferencesFrom(addr) if ref.getOperandIndex() == 0]
        if existing:
            raise RuntimeError('REF operand already populated at %08x' % value)
        ref = references.addMemoryReference(addr, toAddr(row['value']), RefType.DATA,
                                             SourceType.USER_DEFINED, 0)
        references.setPrimary(ref, True)
    elif row['action'] != 'RENAME':
        raise RuntimeError('Unknown action at %08x' % value)
    ensure_slot_label(value, row['slot_label'])
    listing.setComment(addr, CodeUnit.EOL_COMMENT, row['eol'])
    same('SLOT_DATA_AFTER_%08x' % value, data_row(listing.getDefinedDataAt(addr)), row['pre']['data_at'])
    if FAILS:
        raise RuntimeError('Slot Data changed at %08x' % value)
    COUNTS[row['action']] += 1
    COUNTS['EOL'] += 1


def rename_function(value, contract):
    fn = functions.getFunctionAt(toAddr(value))
    if fn is None or long(fn.getSymbol().getID()) != contract['pre']['symbol']['id']:
        raise RuntimeError('Function identity precondition failed at %08x' % value)
    fn.setName(contract['post_name'], SourceType.USER_DEFINED)
    post = functions.getFunctionAt(toAddr(value))
    if (post is None or long(post.getSymbol().getID()) != contract['pre']['symbol']['id'] or
            unicode(post.getName()) != contract['post_name'] or
            str(post.getSymbol().getSource()) != 'USER_DEFINED'):
        raise RuntimeError('Function rename failed at %08x' % value)
    COUNTS['FUNC_RENAME'] += 1


def apply_all():
    # Target Symbols are normalized before any reference action.
    for value, contract in sorted(TARGETS.items()):
        normalize_target(value, contract)
    COUNTS['CARVE'] = len(PLAN['carves'])
    for value, row in sorted(SLOTS.items()):
        apply_slot(row)
    for value, contract in sorted(RENAMES.items()):
        rename_function(value, contract)
    for value, text in sorted(PLATES.items()):
        listing.setComment(toAddr(value), CodeUnit.PLATE_COMMENT, text)
        COUNTS['PLATE'] += 1
    for old_name in OLD_NAMES:
        if list(symbols.getGlobalSymbols(old_name)):
            raise RuntimeError('Old Function name remains: ' + old_name)
    if list(symbols.getGlobalSymbols(PLAN['extra_auto_name_scan'])):
        raise RuntimeError('Legacy auto name remains: ' + PLAN['extra_auto_name_scan'])
    COUNTS['FIXED_OLD_NAME_SCAN'] = len(OLD_NAMES)


def function_invariant(value, pre, expected_name, expected_plate):
    actual = function_row(value)
    require(actual is not None, 'FUNCTION_MISSING_%08x' % value)
    if actual is None:
        return
    require(actual['symbol']['id'] == pre['symbol']['id'] and
            actual['symbol_count'] == 1 and actual['symbol']['type'] == 'Function' and
            actual['symbol']['source'] == 'USER_DEFINED' and actual['symbol']['primary'] and
            actual['symbol']['global'], 'FUNCTION_SYMBOL_POST_%08x' % value)
    require(actual['name'] == expected_name and actual['body_ranges'] == pre['body_ranges'] and
            actual['body_size'] == pre['body_size'] and
            actual['calling_convention'] == pre['calling_convention'] and
            actual['return_type'] == pre['return_type'] and actual['parameters'] == pre['parameters'],
            'FUNCTION_BODY_APCS_POST_%08x' % value)
    same('FUNCTION_INCOMING_POST_%08x' % value,
         [ref_core(row) for row in actual['incoming']],
         [ref_core(row) for row in pre['incoming']])
    require(actual['plate'] == expected_plate, 'FUNCTION_PLATE_POST_%08x' % value)


def verify_post(receipt=None):
    require(functions.getFunctionCount() == 5213, 'FUNCTION_COUNT_POST')
    require(raw_hash(0x080a38fc, 0x080a46a0) == PLAN['segment_sha256'], 'SEGMENT_ROM_POST')
    same('CODE_SUMMARY_POST', instruction_summary(CODE_RANGES),
         {'ranges': 65, 'instructions': 1443, 'bytes': 3050})
    for value, row in sorted(SLOTS.items()):
        require(memory.getInt(toAddr(value)) & 0xffffffff == row['value'],
                'SLOT_ROM_POST_%08x' % value)
        actual = address_state(value)
        primary = symbols.getPrimarySymbol(toAddr(value))
        require(primary is not None and unicode(primary.getName()) == row['slot_label'] and
                str(primary.getSource()) == 'USER_DEFINED' and primary.isPrimary() and
                primary.getParentNamespace() == global_ns and actual['symbol_count'] == 1,
                'SLOT_SYMBOL_POST_%08x' % value)
        same('SLOT_DATA_POST_%08x' % value, actual['data_at'], row['pre']['data_at'])
        require(actual['bytes'] == row['pre']['bytes'] and actual['instruction'] is None and
                actual['function'] is None and actual['eol'] == row['eol'],
                'SLOT_LISTING_POST_%08x' % value)
        if row['action'] == 'EQ':
            eq = equates.getEquate(row['target'])
            matches = [] if eq is None else [ref for ref in eq.getReferences()
                                              if ref.getAddress() == toAddr(value) and ref.getOpIndex() == 0]
            require(eq is not None and (eq.getValue() & 0xffffffff) == row['value'] and
                    len(matches) == 1 and not actual['references_from'],
                    'EQ_POST_%08x' % value)
        elif row['action'] == 'REF':
            same('REF_POST_%08x' % value,
                 [ref_core(ref) for ref in actual['references_from']],
                 [{'from': '%08x' % value, 'to': '%08x' % row['value'], 'operand': 0,
                   'type': 'DATA', 'source': 'USER_DEFINED', 'primary': True}])
            require(not actual['equates'], 'REF_EQUATE_EMPTY_%08x' % value)
        else:
            same('RENAME_REFS_POST_%08x' % value, actual['references_from'], row['pre']['references_from'])
            require(not actual['equates'], 'RENAME_EQUATE_EMPTY_%08x' % value)
    for value, contract in sorted(TARGETS.items()):
        length = 12 if value in (0x09e47898, 0x09e478a4) else 4
        actual = address_state(value, length)
        primary = symbols.getPrimarySymbol(toAddr(value))
        require(primary is not None and unicode(primary.getName()) == contract['post_name'] and
                str(primary.getSource()) == 'USER_DEFINED' and primary.isPrimary() and
                primary.getParentNamespace() == global_ns and actual['symbol_count'] == 1,
                'TARGET_SYMBOL_POST_%08x' % value)
        if contract['preserve_id']:
            require(long(primary.getID()) == contract['pre']['primary_symbol']['id'],
                    'TARGET_ID_POST_%08x' % value)
        if receipt is not None:
            receipt_targets = dict((int(row['address'], 16), row) for row in receipt['after']['targets'])
            require(actual['primary_symbol']['id'] == receipt_targets[value]['primary_symbol']['id'],
                    'TARGET_PERSISTED_ID_%08x' % value)
        same('TARGET_DATA_POST_%08x' % value, actual['data_at'], contract['pre']['data_at'])
        require(actual['bytes'] == contract['pre']['bytes'] and actual['instruction'] is None and
                actual['function'] is None and actual['eol'] == contract['pre']['eol'] and
                actual['plate'] == contract['pre']['plate'], 'TARGET_LISTING_POST_%08x' % value)
        expected_added = []
        for row in PLAN['slots']:
            if row['action'] == 'REF' and row['value'] == value:
                expected_added.append({'from': '%08x' % row['address'], 'to': '%08x' % value,
                                       'operand': 0, 'type': 'DATA',
                                       'source': 'USER_DEFINED', 'primary': True})
        same('TARGET_REFS_TO_POST_%08x' % value,
             [ref_core(ref) for ref in actual['references_to']],
             [ref_core(ref) for ref in contract['pre']['references_to']] + expected_added)
    for value, contract in sorted(SEGMENT_FUNCTIONS.items()):
        expected_name = RENAMES[value]['post_name'] if value in RENAMES else contract['pre']['name']
        expected_plate = PLATES[value] if value in PLATES else contract['pre']['plate']
        function_invariant(value, contract['pre'], expected_name, expected_plate)
    for value, pre in sorted(PLATE_PRE.items()):
        expected_name = RENAMES[value]['post_name'] if value in RENAMES else pre['name']
        function_invariant(value, pre, expected_name, PLATES[value])
    for row in PLAN['odd_callbacks']:
        same('ODD_TARGET_POST_%08x' % row['odd_target'],
             address_state(row['odd_target']), row['pre']['odd_target'])
        same('ODD_EVEN_FUNCTION_POST_%08x' % row['even_entry'],
             function_row(row['even_entry']), row['pre']['even_function'])
    for value, text in sorted(PLATES.items()):
        actual = listing.getComment(CodeUnit.PLATE_COMMENT, toAddr(value))
        require(actual == text and len(actual) < 500 and all(ord(char) < 128 for char in actual),
                'PLATE_POST_%08x' % value)
    decoded = decode_edges(CODE_RANGES)
    expected = [dict((key, row[key]) for key in ('source', 'kind', 'target', 'rom_bytes'))
                for row in PLAN['edges']]
    same('DIRECT_EDGES_POST', decoded, expected)
    for row in PLAN['edges']:
        instruction = listing.getInstructionAt(toAddr(row['source']))
        require(instruction is not None and toAddr(row['target']) in list(instruction.getFlows()),
                'GHIDRA_EDGE_POST_%08x' % row['source'])
    auto_hits = []
    iterator = symbols.getSymbolIterator(toAddr(0x080a38fc), True)
    while iterator.hasNext():
        symbol = iterator.next()
        value = int(symbol.getAddress().getOffset())
        if value >= 0x080a46a0:
            break
        name = unicode(symbol.getName())
        if re.match(r'^(?:DAT|DWORD|PTR|UNK|FUN|SUB)_[0-9a-fA-F]{8}$', name):
            auto_hits.append([value, name])
    require(auto_hits == [], 'RESIDUAL_AUTO_NAMES_' + repr(auto_hits))
    for old_name in OLD_NAMES:
        require(not list(symbols.getGlobalSymbols(old_name)), 'OLD_FUNCTION_NAME_POST_' + old_name)
    require(not list(symbols.getGlobalSymbols(PLAN['extra_auto_name_scan'])), 'OLD_AUTO_NAME_POST')
    print('POSTCHECK slots=96 EQ=73 REF=19 RENAME=4 TARGETS=8 RANGES=65 '
          'INSTRUCTIONS=1443 BYTES=3050 PADDING=29 FUNCTIONS=22 FUNC_RENAME=9 '
          'PLATE=14 EOL=96 CARVE=2 EDGES=305 FAIL=%d' % len(FAILS))


def capture():
    return {
        'script_sha256': SCRIPT_HASH,
        'plan_sha256': INPUT_HASHES[-1][1],
        'segment_sha256': raw_hash(0x080a38fc, 0x080a46a0),
        'function_count': int(functions.getFunctionCount()),
        'slots': [address_state(value) for value in sorted(SLOTS)],
        'targets': [address_state(value, 12 if value in (0x09e47898, 0x09e478a4) else 4)
                    for value in sorted(TARGETS)],
        'segment_functions': [function_row(value) for value in sorted(SEGMENT_FUNCTIONS)],
        'plate_functions': [function_row(value) for value in sorted(PLATE_PRE)],
        'odd_targets': [address_state(row['odd_target']) for row in PLAN['odd_callbacks']],
        'odd_even_functions': [function_row(row['even_entry']) for row in PLAN['odd_callbacks']],
    }


print('=== RefineF13Seg7 mode=%s ===' % MODE)
verify_frozen_plan()
reject('FROZEN_PLAN')

if MODE == 'dry':
    verify_prestate()
    reject('DRY_PREFLIGHT')
    write_json('f13-seg7-dry-result.json', {
        'status': 'F13_SEG7_DRY_PREFLIGHT_OK',
        'FAIL': 0,
        'script_sha256': SCRIPT_HASH,
        'plan_sha256': INPUT_HASHES[-1][1],
        'counts': dict(EXPECTED_APPLY_COUNTS),
        'preflight': {
            'slots': 96, 'targets': 8, 'segment_functions': 22, 'code_ranges': 65,
            'instructions': 1443, 'code_bytes': 3050, 'padding': 29, 'edges': 305,
            'odd_callbacks': 3,
        },
        'semantic_actions_applied': False,
    })
    print('STATUS: OK mode=dry FAIL=0 semantic_actions_applied=false')
elif MODE == 'check':
    receipt = read_json('f13-seg7-apply-receipt.json')
    require(receipt.get('status') == 'F13_SEG7_APPLIED_POSTCHECK_OK' and
            receipt.get('FAIL') == 0 and receipt.get('script_sha256') == SCRIPT_HASH and
            receipt.get('plan_sha256') == INPUT_HASHES[-1][1] and
            receipt.get('counts') == EXPECTED_APPLY_COUNTS,
            'RECEIPT_CONTRACT')
    reject('RECEIPT_CONTRACT')
    verify_post(receipt)
    reject('PERSISTED_POSTCHECK')
    same('PERSISTED_EXACT', capture(), receipt['after'])
    reject('PERSISTED_EXACT')
    write_json('f13-seg7-persisted-check.json', {
        'status': 'F13_SEG7_PERSISTED_CHECK_OK', 'FAIL': 0,
        'PERSISTED_EXACT': True,
        'script_sha256': SCRIPT_HASH, 'plan_sha256': INPUT_HASHES[-1][1],
        'receipt_counts': dict(EXPECTED_APPLY_COUNTS),
    })
    print('STATUS: OK mode=check FAIL=0 PERSISTED_EXACT=true')
else:
    verify_prestate()
    reject('APPLY_PREFLIGHT')
    transaction = currentProgram.startTransaction('Refine F13-Seg-7 approved transaction')
    commit = False
    try:
        apply_all()
        verify_post()
        same('APPLY_COUNTS', COUNTS, EXPECTED_APPLY_COUNTS)
        reject('APPLY_POSTCHECK')
        receipt = {
            'status': 'F13_SEG7_APPLIED_POSTCHECK_OK', 'FAIL': 0,
            'script_sha256': SCRIPT_HASH, 'plan_sha256': INPUT_HASHES[-1][1],
            'counts': dict(EXPECTED_APPLY_COUNTS), 'after': capture(),
        }
        write_json('f13-seg7-apply-receipt.json', receipt)
        commit = True
    finally:
        currentProgram.endTransaction(transaction, commit)
    if not commit:
        raise RuntimeError('F13-Seg-7 transaction rolled back')
    print('STATUS: OK mode=apply FAIL=0 transaction=committed')
