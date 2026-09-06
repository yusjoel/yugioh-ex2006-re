# -*- coding: ascii -*-
#@runtime Jython
#@category Ygo-ex2006.Refine
# F13-Seg-6 PASS materialization. Dry is read-only; apply is one transaction.

import hashlib
import json
import os
import re

from java.math import BigInteger
from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.address import AddressSet
from ghidra.program.model.data import UnsignedIntegerDataType
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import RefType, SourceType


MODE = list(getScriptArgs())[0].lower() if list(getScriptArgs()) else 'dry'
if MODE not in ('dry', 'apply', 'check'):
    raise RuntimeError('Expected dry, apply, or check')

ROOT = os.path.abspath(os.path.join(str(getSourceFile().getParentFile()), '..', '..'))
RUN = os.path.join(ROOT, 'output', 'refine-run-20260831-194634')
PLAN_NAME = 'f13-seg6-plan.json'
INPUT_HASHES = [
    ('doc/dev/refine/F13-Seg-6.proposal.md', 'e8b6d3846956140b66a09876873622bb7bb6b1f2de332cd36ef1de3779ceaeab'),
    ('doc/dev/refine/F13-Seg-6.review.md', 'abf6c5209a3f9138e7c247488575cea913f78c586ca03c0d57b1107a01e942d1'),
    ('doc/dev/refine/F13-Seg-6.slots.tsv', '2070db7653e739f32396fa55c7ca49c70575edb857f3523fb0e55416f983d1fe'),
    ('output/refine-run-20260831-194634/F13-Seg-6.refscan.tsv', '58d491e7bd73040b7873a0cf59ea6192f432f34be72f92587c2de66285829a52'),
    ('output/refine-run-20260831-194634/F13-Seg-6.direct-edges.tsv', 'bc0b2478cc1fe1d049645b5a52a32d87e5b777965cfd1d07758b8c719398484e'),
    ('output/refine-run-20260831-194634/F13-Seg-6.functions.tsv', 'cb4bee09f630de00cc798e00382f4894332a4df92eada169cc29a6465744d207'),
    ('output/refine-run-20260831-194634/F13-Seg-6.layout.tsv', 'b90c4b464a563583765093f2cffdf6a126fbfea28b7a9aa5b0171ad64b2aa506'),
    ('output/refine-run-20260831-194634/f13-seg6-ref-prestate.json', 'e85ecaf4fd4ce0c82376c17e9af8a3aedc17330fb17e7cd9242ade0da589e12c'),
    ('output/refine-run-20260831-194634/f13-seg6-ref-prestate-gate.json', 'e149bb3a46ef62a2b4f77e4a68c22f5681beebe9703044408f62428bfcb4c4b7'),
    ('output/refine-run-20260831-194634/f13-seg6-full-prestate.json', '4237671c74c2204f046107dcc0aea069d4d0ecd7d3c29adc2eb42b161ba5e0e5'),
    ('output/refine-run-20260831-194634/f13-seg6-full-prestate-gate.json', 'c86f44324f9b3136aede455ef4894568b162da4e00ba59b162c21d8a8d029536'),
    ('output/refine-run-20260831-194634/f13-seg6-preapply-backup.json', '98abe5100b4fefc2ea4373fb634014eef90825af46d74a4a3da7c89190892b86'),
    ('output/refine-run-20260831-194634/f13-seg6-tail-probe.json', '4eef1354130a8eeeeb405c5542d5c18623bb10097a98fa6d8f65d3235a865d85'),
    ('output/refine-run-20260831-194634/f13-seg6-tail-probe-restore-gate.json', 'aa13465e8a676bd1c28c55de58344b9eda7ad37c54d59ae12b3fba64e6c8786e'),
    ('output/refine-run-20260831-194634/f13-seg6-plan.json', '6e80777abf14d0e74436bd47ae1990f2efc63ae5c6a2db1839384ed5ba195d8a'),
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
    'EQ': 138, 'REF': 14, 'RENAME': 32, 'EOL': 184,
    'PLATE': 9, 'R4': 1, 'FUNC_CREATE': 1,
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
        write_json('f13-seg6-%s-failures.json' % MODE,
                   {'status': 'FAIL', 'phase': phase, 'FAIL': len(FAILS), 'failures': FAILS})
        raise RuntimeError('%s FAIL=%d' % (phase, len(FAILS)))


def byte_hex(value, length):
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
        'qualified_name': unicode(symbol.getName(True)),
        'type': str(symbol.getSymbolType()), 'source': str(symbol.getSource()),
        'primary': bool(symbol.isPrimary()),
        'namespace': None if parent is None else unicode(parent.getName()),
        'global': parent == global_ns,
    }


def ref_row(ref):
    return {
        'from': str(ref.getFromAddress()), 'to': str(ref.getToAddress()),
        'operand': int(ref.getOperandIndex()), 'type': str(ref.getReferenceType()),
        'source': str(ref.getSource()), 'primary': bool(ref.isPrimary()),
    }


def data_row(addr):
    data = listing.getDefinedDataAt(addr)
    if data is None:
        return None
    return {
        'address': str(data.getAddress()), 'min': str(data.getMinAddress()),
        'max': str(data.getMaxAddress()), 'length': int(data.getLength()),
        'type': unicode(data.getDataType().getPathName()),
    }


def address_state(value):
    addr = toAddr(value)
    instruction = listing.getInstructionAt(addr)
    fn = functions.getFunctionAt(addr)
    return {
        'address': value, 'bytes': byte_hex(value, 4),
        'symbols': [symbol_row(symbol) for symbol in symbols.getSymbols(addr)],
        'data': data_row(addr),
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
        result.append([int(item.getMinAddress().getOffset()), int(item.getMaxAddress().getOffset()) + 1])
    return result


def function_row(value):
    fn = functions.getFunctionAt(toAddr(value))
    if fn is None:
        return None
    symbol = fn.getSymbol()
    params = []
    for param in fn.getParameters():
        params.append({
            'ordinal': int(param.getOrdinal()), 'name': unicode(param.getName()),
            'data_type': unicode(param.getDataType().getPathName()),
            'storage': unicode(param.getVariableStorage().toString()),
            'source': str(param.getSource()),
        })
    return {
        'entry': value, 'name': unicode(fn.getName()), 'symbol': symbol_row(symbol),
        'body_ranges': body_ranges(fn), 'body_size': int(fn.getBody().getNumAddresses()),
        'calling_convention': unicode(fn.getCallingConventionName()),
        'return_type': unicode(fn.getReturnType().getPathName()), 'parameters': params,
        'plate': listing.getComment(CodeUnit.PLATE_COMMENT, fn.getEntryPoint()),
        'incoming': [ref_row(ref) for ref in references.getReferencesTo(fn.getEntryPoint())],
    }


def tail_instruction_row(instruction):
    addr = instruction.getAddress()
    value = int(addr.getOffset())
    mode = context.getValue(tmode, addr, False)
    return {
        'address': value,
        'address_text': str(addr),
        'to_string': unicode(instruction.toString()),
        'mnemonic': unicode(instruction.getMnemonicString()),
        'length': int(instruction.getLength()),
        'bytes': byte_hex(value, instruction.getLength()),
        'tmode': None if mode is None else int(mode),
        'flow_type': str(instruction.getFlowType()),
        'flows': [str(target) for target in instruction.getFlows()],
        'fallthrough': None if instruction.getFallThrough() is None else str(instruction.getFallThrough()),
        'operands': [unicode(instruction.getDefaultOperandRepresentation(index))
                     for index in range(instruction.getNumOperands())],
    }


def exact_body(ranges):
    body = AddressSet()
    for lo, hi in ranges:
        body.addRange(toAddr(lo), toAddr(hi - 1))
    return body


def instruction_summary(ranges, require_thumb=True):
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
            if require_thumb:
                mode = context.getValue(tmode, toAddr(cursor), False)
                require(mode is not None and int(mode) == 1, 'TMODE_%08x' % cursor)
            cursor += length
            count += 1
            total += length
        require(cursor == hi, 'INSTRUCTION_COVERAGE_%08x_%08x' % (lo, hi))
    return {'ranges': len(ranges), 'instructions': count, 'bytes': total}


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
                    result.append({'source': cursor, 'op': 'BL', 'target': target,
                                   'rom_bytes': byte_hex(cursor, 4)})
                    cursor += 4
                    continue
            if first & 0xf000 == 0xd000 and ((first >> 8) & 15) < 14:
                target = (cursor + 4 + sign_extend(first & 255, 8) * 2) & 0xffffffff
                result.append({'source': cursor, 'op': 'Bcc', 'target': target,
                               'rom_bytes': byte_hex(cursor, 2)})
            elif first & 0xf800 == 0xe000:
                target = (cursor + 4 + sign_extend(first & 0x7ff, 11) * 2) & 0xffffffff
                result.append({'source': cursor, 'op': 'B', 'target': target,
                               'rom_bytes': byte_hex(cursor, 2)})
            cursor += 2
    return result


PLAN = read_json(PLAN_NAME)
PRE = read_json('f13-seg6-full-prestate.json')
SCRIPT_HASH = file_hash(getSourceFile().getAbsolutePath())
SLOTS = dict((row['addr'], row) for row in PLAN['actions'])
PRE_SLOTS = dict((row['address'], row) for row in PRE['slots'])
PRE_TARGETS = dict((row['address'], row) for row in PRE['targets'])
PRE_FUNCTIONS = dict((row['entry'], row) for row in PRE['functions'])
TARGETS = dict((row['address'], row) for row in PLAN['target_contracts'])
REF_DATA = dict((row['address'], row['pre_data']) for row in PLAN['ref_data_contracts'])
REF_DATA_FULL = {}
for _value, _row in REF_DATA.items():
    _copy = dict(_row)
    _copy['min'] = '%08x' % _value
    _copy['max'] = '%08x' % (_value + _row['length'] - 1)
    REF_DATA_FULL[_value] = _copy
PLATES = dict((row['addr'], row['text']) for row in PLAN['plates'])
EXISTING_RANGES = [tuple(pair) for pair in PLAN['existing_code_ranges']]
POST_RANGES = [tuple(pair) for pair in PLAN['post_code_ranges']]
PADDING = [tuple(pair) for pair in PLAN['padding']]
TAIL = PLAN['tail']
TAIL_LO, TAIL_HI = TAIL['range']


def verify_frozen_plan():
    for relative, digest in INPUT_HASHES:
        same('INPUT_HASH_' + relative, file_hash(os.path.join(ROOT, relative)), digest)
    expected_inputs = dict((key, value) for key, value in (
        ('proposal', INPUT_HASHES[0][1]), ('review', INPUT_HASHES[1][1]),
        ('tsv', INPUT_HASHES[2][1]), ('refscan', INPUT_HASHES[3][1]),
        ('edges', INPUT_HASHES[4][1]), ('functions', INPUT_HASHES[5][1]),
        ('layout', INPUT_HASHES[6][1]), ('c7_raw', INPUT_HASHES[7][1]),
        ('c7_gate', INPUT_HASHES[8][1]), ('full_prestate', INPUT_HASHES[9][1]),
        ('full_prestate_gate', INPUT_HASHES[10][1]), ('backup', INPUT_HASHES[11][1]),
        ('tail_probe', INPUT_HASHES[12][1]), ('tail_probe_restore', INPUT_HASHES[13][1])))
    same('PLAN_INPUT_HASHES', PLAN['input_hashes'], expected_inputs)
    require(PLAN['status'] == 'F13_SEG6_PLAN_OK', 'PLAN_STATUS')
    require(PLAN['range'] == [0x080a27a0, 0x080a38fc] and PLAN['range_size'] == 4444,
            'SEGMENT_RANGE')
    require(len(SLOTS) == 184 and len(PLAN['actions']) == 184, 'SLOT_COUNT')
    require([sum(row['action'] == kind for row in PLAN['actions'])
             for kind in ('EQ', 'REF', 'RENAME')] == [138, 14, 32], 'ACTION_COUNTS')
    require(len(TARGETS) == 5 and len(REF_DATA) == 14, 'REF_CONTRACT_COUNTS')
    require(len(PLAN['new_constants']) == 3 and len(PLAN['gas_aliases']) == 8,
            'SOURCE_SYMBOL_COUNTS')
    require(len(PADDING) == 47 and sum(hi - lo for lo, hi in PADDING) == 94,
            'PADDING_COUNTS')
    require(len(PLAN['switch_words']) == 5 and len(PLAN['layout']) == 236,
            'LAYOUT_COUNTS')
    require(len(EXISTING_RANGES) == 96 and len(POST_RANGES) == 97,
            'CODE_RANGE_COUNTS')
    require(sum(hi - lo for lo, hi in EXISTING_RANGES) == 3590 and
            sum(hi - lo for lo, hi in POST_RANGES) == 3594, 'CODE_BYTE_COUNTS')
    require(len(PLAN['functions']) == 17 and
            sum(row['action'] == 'preserve' for row in PLAN['functions']) == 16 and
            sum(row['action'] == 'create_and_name' for row in PLAN['functions']) == 1,
            'FUNCTION_PLAN_COUNTS')
    require(PLAN['function_pre_count'] == 5212 and PLAN['function_post_count'] == 5213,
            'FUNCTION_TOTAL_COUNTS')
    require(TAIL_LO == 0x080a38f8 and TAIL_HI == 0x080a38fc and
            TAIL['bytes'] == '01207047' and TAIL['return_type'] == 'uint' and
            TAIL['parameters'] == [] and TAIL['return_value'] == 1,
            'TAIL_CONTRACT')
    require(TAIL['encoding_semantics'] == ['movs_r0_imm8_1', 'bx_lr'] and
            [(row['address'], row['length'], row['bytes'], row['tmode'], row['mnemonic'])
             for row in TAIL['instruction_contract']] == [
                (0x080a38f8, 2, '0120', 1, 'mov'),
                (0x080a38fa, 2, '7047', 1, 'bx')],
            'TAIL_INSTRUCTION_PLAN')
    for value, contract in TARGETS.items():
        expected_data = contract['pre']['data']
        require(expected_data['address'] == '%08x' % value and
                expected_data['min'] == '%08x' % value and
                expected_data['max'] == '%08x' % (value + expected_data['length'] - 1) and
                expected_data['length'] == 4, 'TARGET_DATA_PLAN_%08x' % value)
    require(len(PLAN['edges']) == 379 and PLAN['edge_counts'] == {'B': 109, 'BL': 84, 'Bcc': 186},
            'EDGE_COUNTS')
    require(len(PLATES) == 9 and max(len(text) for text in PLATES.values()) < 500,
            'PLATE_COUNTS')
    for value, text in PLATES.items():
        require(all(ord(char) < 128 for char in text), 'PLATE_ASCII_%08x' % value)
    for value, row in SLOTS.items():
        require(row['addr'] == value and all(ord(char) < 128 for char in row['eol']),
                'EOL_ASCII_%08x' % value)
        require(re.match(r'^[a-z][a-z0-9_]+$', row['slot_label']) is not None,
                'SLOT_NAME_%08x' % value)
    require(TARGETS[0x080a2b00]['pre']['symbols'][0]['id'] == 5854 and
            TARGETS[0x080a2b00]['post_name'] == 'equip_target_selection_phase_jump_table',
            'SWITCH_TARGET_ID')
    require(raw_hash(0x080a27a0, 0x080a38fc) == PLAN['segment_sha256'], 'SEGMENT_ROM_SHA')


def verify_prestate():
    require(functions.getFunctionCount() == 5212, 'FUNCTION_COUNT_PRE')
    require(len(PRE_SLOTS) == 184 and len(PRE_TARGETS) == 6 and len(PRE_FUNCTIONS) == 16,
            'PRESTATE_DOCUMENT_COUNTS')
    for value in sorted(PRE_SLOTS):
        same('SLOT_PRE_%08x' % value, address_state(value), PRE_SLOTS[value])
        require(memory.getInt(toAddr(value)) & 0xffffffff == SLOTS[value]['value'],
                'SLOT_ROM_VALUE_%08x' % value)
    for value in sorted(PRE_TARGETS):
        same('TARGET_PRE_%08x' % value, address_state(value), PRE_TARGETS[value])
    for value in sorted(PRE_FUNCTIONS):
        same('FUNCTION_PRE_%08x' % value, function_row(value), PRE_FUNCTIONS[value])
    same('TAIL_PRE', address_state(TAIL_LO), PRE['tail'])
    code = instruction_summary(EXISTING_RANGES)
    same('EXISTING_CODE_SUMMARY', code, {'ranges': 96, 'instructions': 1712, 'bytes': 3590})
    for lo, hi in PADDING:
        require(byte_hex(lo, hi - lo) == '00' * (hi - lo), 'PADDING_BYTES_%08x' % lo)
        for value in range(lo, hi):
            require(listing.getInstructionContaining(toAddr(value)) is None and
                    listing.getDefinedDataContaining(toAddr(value)) is None,
                    'PADDING_LISTING_%08x' % value)
    for address, value in PLAN['switch_words']:
        require(memory.getInt(toAddr(address)) & 0xffffffff == value, 'SWITCH_WORD_%08x' % address)
    for value, expected in REF_DATA_FULL.items():
        same('REF_DATA_PRE_%08x' % value, data_row(toAddr(value)), expected)
        require(address_state(value)['bytes'] == PRE_SLOTS[value]['bytes'], 'REF_BYTES_PRE_%08x' % value)
    decoded = decode_edges(EXISTING_RANGES + [(0x080a187a, 0x080a187e)])
    expected = [dict((key, row[key]) for key in ('source', 'op', 'target', 'rom_bytes'))
                for row in PLAN['edges']]
    same('DIRECT_EDGES_PRE', decoded, expected)
    require(sum(row['target'] == TAIL_LO for row in PLAN['edges']) == 1 and
            [row for row in PLAN['edges'] if row['target'] == TAIL_LO][0]['source'] == 0x080a187a,
            'TAIL_INBOUND_EDGE')
    print('PREFLIGHT slots=184 EQ=138 REF=14 RENAME=32 TARGETS=5 RANGES=96 '
          'INSTRUCTIONS=1712 BYTES=3590 PADDING=47 FUNCTIONS=16 TAIL_CREATE=1 '
          'PLATE=9 EOL=184 EDGES=379 FAIL=%d' % len(FAILS))


def rename_same_symbol(value, name, expected):
    addr = toAddr(value)
    at_addr = list(symbols.getSymbols(addr))
    primary = symbols.getPrimarySymbol(addr)
    expected_symbol = expected['symbols'][0]
    if not (len(at_addr) == 1 and primary is not None and
            long(primary.getID()) == expected_symbol['id'] and primary.isPrimary()):
        raise RuntimeError('Target symbol identity precondition failed at %08x' % value)
    collisions = [symbol for symbol in symbols.getGlobalSymbols(name) if symbol.getAddress() != addr]
    if collisions:
        raise RuntimeError('Target name collision: ' + name)
    if primary.getParentNamespace() != global_ns:
        primary.setNameAndNamespace(name, global_ns, SourceType.USER_DEFINED)
    else:
        primary.setName(name, SourceType.USER_DEFINED)
    post = symbols.getPrimarySymbol(addr)
    if (post is None or long(post.getID()) != expected_symbol['id'] or
            unicode(post.getName()) != name or str(post.getSource()) != 'USER_DEFINED' or
            post.getParentNamespace() != global_ns or len(list(symbols.getSymbols(addr))) != 1):
        raise RuntimeError('Target normalization failed at %08x' % value)


def normalize_targets():
    # This runs before every listing/reference change. 080a2b00 keeps Symbol ID 5854.
    for value in sorted(TARGETS):
        rename_same_symbol(value, TARGETS[value]['post_name'], TARGETS[value]['pre'])


def ensure_slot_label(value, name):
    addr = toAddr(value)
    primary = symbols.getPrimarySymbol(addr)
    at_addr = list(symbols.getSymbols(addr))
    if len(at_addr) > 1:
        raise RuntimeError('Slot has aliases at %08x' % value)
    if primary is None:
        primary = symbols.createLabel(addr, name, SourceType.USER_DEFINED)
    elif primary.getParentNamespace() != global_ns:
        primary.setNameAndNamespace(name, global_ns, SourceType.USER_DEFINED)
    else:
        primary.setName(name, SourceType.USER_DEFINED)
    primary = symbols.getPrimarySymbol(addr)
    primary.setPrimary()
    if (primary is None or unicode(primary.getName()) != name or
            str(primary.getSource()) != 'USER_DEFINED' or len(list(symbols.getSymbols(addr))) != 1):
        raise RuntimeError('Slot label failed at %08x' % value)


def apply_slot(row):
    value = row['addr']
    addr = toAddr(value)
    if (memory.getInt(addr) & 0xffffffff) != row['value']:
        raise RuntimeError('ROM value changed at %08x' % value)
    if row['action'] == 'EQ':
        eq = equates.getEquate(row['target'])
        if eq is None:
            eq = equates.createEquate(row['target'], row['value'])
        elif (eq.getValue() & 0xffffffff) != row['value']:
            raise RuntimeError('Equate conflict: ' + row['target'])
        eq.addReference(addr, 0)
    elif row['action'] == 'REF':
        # The defined Data object is intentionally untouched.
        same('REF_DATA_BEFORE_APPLY_%08x' % value, data_row(addr), REF_DATA_FULL[value])
        if FAILS:
            raise RuntimeError('REF Data precondition failed at %08x' % value)
        existing = [ref for ref in references.getReferencesFrom(addr) if ref.getOperandIndex() == 0]
        if existing:
            raise RuntimeError('REF operand already populated at %08x' % value)
        ref = references.addMemoryReference(addr, toAddr(row['value']), RefType.DATA,
                                             SourceType.USER_DEFINED, 0)
        references.setPrimary(ref, True)
        same('REF_DATA_AFTER_APPLY_%08x' % value, data_row(addr), REF_DATA_FULL[value])
        if FAILS:
            raise RuntimeError('REF Data changed at %08x' % value)
    elif row['action'] != 'RENAME':
        raise RuntimeError('Unknown action at %08x' % value)
    ensure_slot_label(value, row['slot_label'])
    listing.setComment(addr, CodeUnit.EOL_COMMENT, row['eol'])
    COUNTS[row['action']] += 1
    COUNTS['EOL'] += 1


def create_tail_function():
    if getFunctionAt(toAddr(TAIL_LO)) is not None:
        raise RuntimeError('Tail Function already exists')
    listing.clearCodeUnits(toAddr(TAIL_LO), toAddr(TAIL_HI - 1), False)
    context.setValue(tmode, toAddr(TAIL_LO), toAddr(TAIL_HI - 1), BigInteger.ONE)
    command = DisassembleCommand(toAddr(TAIL_LO), AddressSet(toAddr(TAIL_LO), toAddr(TAIL_HI - 1)), True)
    if not command.applyTo(currentProgram):
        raise RuntimeError('Tail disassembly failed: ' + str(command.getStatusMsg()))
    summary = instruction_summary([(TAIL_LO, TAIL_HI)])
    if summary != {'ranges': 1, 'instructions': 2, 'bytes': 4}:
        raise RuntimeError('Tail instruction coverage mismatch')
    fn = functions.createFunction(TAIL['name'], toAddr(TAIL_LO),
                                  exact_body([(TAIL_LO, TAIL_HI)]), SourceType.USER_DEFINED)
    if fn is None:
        raise RuntimeError('Tail Function create failed')
    fn.setReturnType(UnsignedIntegerDataType.dataType, SourceType.USER_DEFINED)
    if len(list(fn.getParameters())) != 0:
        raise RuntimeError('Tail Function parameters are not empty')
    COUNTS['R4'] += 1
    COUNTS['FUNC_CREATE'] += 1


def apply_all():
    normalize_targets()
    for value in sorted(SLOTS):
        apply_slot(SLOTS[value])
    create_tail_function()
    for value, text in sorted(PLATES.items()):
        listing.setComment(toAddr(value), CodeUnit.PLATE_COMMENT, text)
        COUNTS['PLATE'] += 1


def operand_zero_refs(value):
    return [ref_row(ref) for ref in references.getReferencesFrom(toAddr(value))
            if ref.getOperandIndex() == 0]


def verify_post(receipt=None):
    require(functions.getFunctionCount() == 5213, 'FUNCTION_COUNT_POST')
    require(raw_hash(0x080a27a0, 0x080a38fc) == PLAN['segment_sha256'], 'SEGMENT_ROM_POST')
    summary = instruction_summary(POST_RANGES)
    same('POST_CODE_SUMMARY', summary, {'ranges': 97, 'instructions': 1714, 'bytes': 3594})
    for value, row in SLOTS.items():
        require(memory.getInt(toAddr(value)) & 0xffffffff == row['value'], 'SLOT_ROM_POST_%08x' % value)
        primary = symbols.getPrimarySymbol(toAddr(value))
        require(primary is not None and unicode(primary.getName()) == row['slot_label'] and
                str(primary.getSource()) == 'USER_DEFINED' and primary.isPrimary() and
                primary.getParentNamespace() == global_ns and
                len(list(symbols.getSymbols(toAddr(value)))) == 1, 'SLOT_SYMBOL_POST_%08x' % value)
        require(listing.getComment(CodeUnit.EOL_COMMENT, toAddr(value)) == row['eol'],
                'SLOT_EOL_POST_%08x' % value)
        if row['action'] == 'EQ':
            eq = equates.getEquate(row['target'])
            matches = [] if eq is None else [ref for ref in eq.getReferences()
                                              if ref.getAddress() == toAddr(value) and ref.getOpIndex() == 0]
            require(eq is not None and (eq.getValue() & 0xffffffff) == row['value'] and
                    len(matches) == 1, 'EQ_POST_%08x' % value)
        elif row['action'] == 'REF':
            same('REF_DATA_POST_%08x' % value, data_row(toAddr(value)), REF_DATA_FULL[value])
            same('REF_POST_%08x' % value, operand_zero_refs(value), [{
                'from': '%08x' % value, 'to': '%08x' % row['value'], 'operand': 0,
                'type': 'DATA', 'source': 'USER_DEFINED', 'primary': True}])
        else:
            same('RENAME_REFS_POST_%08x' % value,
                 [ref_row(ref) for ref in references.getReferencesFrom(toAddr(value))],
                 PRE_SLOTS[value]['references_from'])
    for value, contract in TARGETS.items():
        before = contract['pre']
        actual = address_state(value)
        primary = symbols.getPrimarySymbol(toAddr(value))
        require(primary is not None and long(primary.getID()) == before['symbols'][0]['id'] and
                unicode(primary.getName()) == contract['post_name'] and
                str(primary.getSource()) == 'USER_DEFINED' and primary.isPrimary() and
                primary.getParentNamespace() == global_ns and
                len(list(symbols.getSymbols(toAddr(value)))) == 1, 'TARGET_POST_%08x' % value)
        same('TARGET_DATA_POST_%08x' % value, actual['data'], before['data'])
    for value in sorted(PRE_FUNCTIONS):
        actual = function_row(value)
        old = PRE_FUNCTIONS[value]
        require(actual is not None and actual['symbol']['id'] == old['symbol']['id'] and
                actual['name'] == old['name'] and actual['body_ranges'] == old['body_ranges'] and
                actual['body_size'] == old['body_size'] and
                actual['calling_convention'] == old['calling_convention'] and
                actual['return_type'] == old['return_type'] and
                actual['parameters'] == old['parameters'] and actual['incoming'] == old['incoming'],
                'EXISTING_FUNCTION_POST_%08x' % value)
        require(actual['plate'] == PLATES.get(value, old['plate']),
                'EXISTING_FUNCTION_PLATE_POST_%08x' % value)
    fn = getFunctionAt(toAddr(TAIL_LO))
    require(fn is not None and unicode(fn.getName()) == TAIL['name'] and
            str(fn.getSymbol().getSource()) == 'USER_DEFINED' and
            body_ranges(fn) == [[TAIL_LO, TAIL_HI]] and
            unicode(fn.getReturnType().getName()) == 'uint' and len(list(fn.getParameters())) == 0,
            'TAIL_FUNCTION_POST')
    require(byte_hex(TAIL_LO, 4) == TAIL['bytes'], 'TAIL_ROM_BYTES_POST')
    tail_instructions = [getInstructionAt(toAddr(TAIL_LO)), getInstructionAt(toAddr(TAIL_LO + 2))]
    require(all(instruction is not None for instruction in tail_instructions),
            'TAIL_INSTRUCTIONS_PRESENT_POST')
    if all(instruction is not None for instruction in tail_instructions):
        same('TAIL_INSTRUCTIONS_POST',
             [tail_instruction_row(instruction) for instruction in tail_instructions],
             TAIL['instruction_contract'])
    same('TAIL_INCOMING_POST', [ref_row(ref) for ref in references.getReferencesTo(toAddr(TAIL_LO))],
         [{'from': '080a187a', 'to': '080a38f8', 'operand': 0,
           'type': 'UNCONDITIONAL_CALL', 'source': 'DEFAULT', 'primary': True}])
    for value, text in PLATES.items():
        actual = listing.getComment(CodeUnit.PLATE_COMMENT, toAddr(value))
        require(actual == text and len(actual) < 500 and all(ord(char) < 128 for char in actual),
                'PLATE_POST_%08x' % value)
    decoded = decode_edges(EXISTING_RANGES + [(0x080a187a, 0x080a187e)])
    expected = [dict((key, row[key]) for key in ('source', 'op', 'target', 'rom_bytes'))
                for row in PLAN['edges']]
    same('DIRECT_EDGES_POST', decoded, expected)
    for row in PLAN['edges']:
        instruction = listing.getInstructionAt(toAddr(row['source']))
        require(instruction is not None and toAddr(row['target']) in list(instruction.getFlows()),
                'GHIDRA_EDGE_POST_%08x' % row['source'])
    auto_hits = []
    iterator = symbols.getSymbolIterator(toAddr(0x080a27a0), True)
    while iterator.hasNext():
        symbol = iterator.next()
        value = int(symbol.getAddress().getOffset())
        if value >= 0x080a38fc:
            break
        name = unicode(symbol.getName())
        if re.match(r'^(?:DAT|DWORD|PTR|UNK|FUN|SUB)_[0-9a-fA-F]{8}$', name):
            auto_hits.append([value, name])
    require(auto_hits == [], 'RESIDUAL_AUTO_NAMES_' + repr(auto_hits))
    print('POSTCHECK slots=184 EQ=138 REF=14 RENAME=32 TARGETS=5 RANGES=97 '
          'INSTRUCTIONS=1714 BYTES=3594 PADDING=47 FUNC_CREATE=1 PLATE=9 EOL=184 '
          'EDGES=379 FAIL=%d' % len(FAILS))


def capture():
    return {
        'script_sha256': SCRIPT_HASH, 'plan_sha256': INPUT_HASHES[-1][1],
        'segment_sha256': raw_hash(0x080a27a0, 0x080a38fc),
        'function_count': int(functions.getFunctionCount()),
        'slots': [address_state(value) for value in sorted(SLOTS)],
        'targets': [address_state(value) for value in sorted(TARGETS)],
        'functions': [function_row(value) for value in sorted(PRE_FUNCTIONS) + [TAIL_LO]],
    }


print('=== RefineF13Seg6 mode=%s ===' % MODE)
verify_frozen_plan()
reject('FROZEN_PLAN')

if MODE == 'dry':
    verify_prestate()
    reject('DRY_PREFLIGHT')
    write_json('f13-seg6-dry-result.json', {
        'status': 'F13_SEG6_DRY_PREFLIGHT_OK', 'FAIL': 0,
        'script_sha256': SCRIPT_HASH, 'plan_sha256': INPUT_HASHES[-1][1],
        'counts': {'slots': 184, 'EQ': 138, 'REF': 14, 'RENAME': 32,
                   'targets': 5, 'ranges_pre': 96, 'instructions_pre': 1712,
                   'padding': 47, 'functions_preserve': 16, 'function_create': 1,
                   'PLATE': 9, 'EOL': 184, 'edges': 379},
        'semantic_actions_applied': False})
    print('STATUS: OK mode=dry FAIL=0 semantic_actions_applied=false')
elif MODE == 'check':
    receipt = read_json('f13-seg6-apply-receipt.json')
    require(receipt.get('status') == 'F13_SEG6_APPLIED_POSTCHECK_OK' and
            receipt.get('FAIL') == 0 and
            receipt.get('script_sha256') == SCRIPT_HASH and
            receipt.get('plan_sha256') == INPUT_HASHES[-1][1] and
            receipt.get('counts') == EXPECTED_APPLY_COUNTS,
            'RECEIPT_CONTRACT')
    reject('RECEIPT_CONTRACT')
    verify_post(receipt)
    reject('PERSISTED_POSTCHECK')
    same('PERSISTED_EXACT', capture(), receipt['after'])
    reject('PERSISTED_EXACT')
    write_json('f13-seg6-persisted-check.json', {
        'status': 'F13_SEG6_PERSISTED_CHECK_OK', 'FAIL': 0,
        'script_sha256': SCRIPT_HASH, 'plan_sha256': INPUT_HASHES[-1][1]})
    print('STATUS: OK mode=check FAIL=0')
else:
    verify_prestate()
    reject('APPLY_PREFLIGHT')
    transaction = currentProgram.startTransaction('Refine F13-Seg-6 approved transaction')
    commit = False
    try:
        apply_all()
        verify_post()
        same('APPLY_COUNTS', COUNTS, EXPECTED_APPLY_COUNTS)
        reject('APPLY_POSTCHECK')
        after = capture()
        receipt = {
            'status': 'F13_SEG6_APPLIED_POSTCHECK_OK', 'FAIL': 0,
            'script_sha256': SCRIPT_HASH, 'plan_sha256': INPUT_HASHES[-1][1],
            'counts': dict(EXPECTED_APPLY_COUNTS), 'after': after}
        write_json('f13-seg6-apply-receipt.json', receipt)
        commit = True
    finally:
        currentProgram.endTransaction(transaction, commit)
    if not commit:
        raise RuntimeError('F13-Seg-6 transaction rolled back')
    print('STATUS: OK mode=apply FAIL=0 transaction=committed')
