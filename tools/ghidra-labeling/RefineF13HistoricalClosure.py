# -*- coding: ascii -*-
#@runtime Jython
#@category Ygo-ex2006.Refine
# F13 Historical Closure: one approved ASCII PLATE rewrite.

import csv
import hashlib
import json
import os

from ghidra.program.model.listing import CodeUnit

ARGS = list(getScriptArgs())
MODE = ARGS[0].lower() if ARGS else 'dry'
if MODE not in ('dry', 'apply', 'check'):
    raise RuntimeError('Expected dry, apply, or check')

ROOT = os.path.abspath(os.path.join(str(getSourceFile().getParentFile()), '..', '..'))
RUN = os.path.join(ROOT, 'output', 'refine-run-20261028-105948')
PLAN_NAME = 'f13-closure-plan.json'
PRESTATE_NAME = 'f13-closure-fresh-full-prestate.json'
SOURCE_SNAPSHOT_NAME = 'f13-closure-source-snapshot-preapply.json'
PROPOSAL_MANIFEST_NAME = 'f13-closure-proposal-manifest.json'
DB_BACKUP_MANIFEST_NAME = 'root-f13-closure-db-backup.json'
PLATES_REL = 'doc/dev/refine/F13-Historical-Closure.plates.tsv'
SEGMENT_START = 0x0809d718
SEGMENT_END = 0x080a78dc
SEGMENT_SIZE = 41412
TARGET = 0x080a38fc
TARGET_ID = 3436
EXPECTED_FUNCTION_COUNT = 5213
EXPECTED_COUNTS = {
    'EQ': 0, 'REF': 0, 'RENAME': 0, 'EOL': 0,
    'FUNC_RENAME': 0, 'PLATE': 1, 'R4': 0,
    'CARVE': 0, 'NEW_CONSTANT': 0,
}
INPUT_HASHES = {
    'doc/dev/refine/F13-Historical-Closure.proposal.md': 'c941f0068bc8242f6a69bc28ddcbeadefbccf2430b7b7c2f5435bdd5a66cbb1a',
    'doc/dev/refine/F13-Historical-Closure.review.md': '1a95e28c1d373e9ad61eb778385971920444d54aadeb2aa25218364290fdb5e2',
    'doc/dev/refine/F13-Historical-Closure.plates.tsv': 'a98e77c26062726316b55cfdd1864058dea8792468109b753efe1a3cde5cc821',
    'output/refine-run-20261028-105948/f13-closure-proposal-manifest.json': '87ffbd4aad972395502e3f2c8d8854efcb02657976b0e6764a394fa1a6ed6c87',
    'output/refine-run-20261028-105948/reviewer-f13-closure-round2-audit.json': 'd621c1b1ae333f35ebf72a503c33eec9dd905417fa9737125ed4e0825f3e5d0d',
}

listing = currentProgram.getListing()
symbols = currentProgram.getSymbolTable()
references = currentProgram.getReferenceManager()
equates = currentProgram.getEquateTable()
memory = currentProgram.getMemory()
functions = currentProgram.getFunctionManager()
global_ns = currentProgram.getGlobalNamespace()
FAILS = []

def root_path(relative):
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

def text_hash(value):
    return hashlib.sha256(value.encode('utf-8')).hexdigest()

def raw_hash(lo, hi):
    raw = ''.join(chr(memory.getByte(toAddr(value)) & 255) for value in range(lo, hi))
    return hashlib.sha256(raw).hexdigest()

def safe(callable_value, default=None):
    try:
        return callable_value()
    except Exception:
        return default

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
        values = [canonical(item) for item in value]
        return sorted(values, key=lambda item: json.dumps(item, ensure_ascii=True, sort_keys=True))
    return value

def same(message, actual, expected):
    left = json.dumps(canonical(actual), ensure_ascii=True, sort_keys=True, separators=(',', ':'))
    right = json.dumps(canonical(expected), ensure_ascii=True, sort_keys=True, separators=(',', ':'))
    if left != right:
        fail(message, actual, expected)

def reject(phase):
    if FAILS:
        write_json('f13-closure-%s-failures.json' % MODE,
                   {'status': 'FAIL', 'phase': phase, 'FAIL': len(FAILS), 'failures': FAILS})
        raise RuntimeError('%s FAIL=%d' % (phase, len(FAILS)))

def read_plate_row():
    with open(root_path(PLATES_REL), 'rb') as stream:
        rows = list(csv.DictReader(stream, delimiter='\t'))
    require(len(rows) == 1, 'PLATE_ROW_COUNT')
    return rows[0] if rows else {}

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
        'namespace_id': None if parent is None else safe(lambda: long(parent.getID())),
        'global': parent == global_ns,
    }

def ref_row(reference):
    target = symbols.getPrimarySymbol(reference.getToAddress())
    return {
        'from': str(reference.getFromAddress()),
        'to': str(reference.getToAddress()),
        'operand': int(reference.getOperandIndex()),
        'type': str(reference.getReferenceType()),
        'source': str(reference.getSource()),
        'primary': bool(reference.isPrimary()),
        'target_primary_id': None if target is None else long(target.getID()),
        'target_primary_name': None if target is None else unicode(target.getName(True)),
    }

def refs_from(address):
    return [ref_row(item) for item in references.getReferencesFrom(address)]

def refs_to(address):
    return [ref_row(item) for item in references.getReferencesTo(address)]

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

def bytes_hex(value, length):
    addr = toAddr(value)
    block = memory.getBlock(addr)
    if block is None or not block.isInitialized():
        return None
    return ''.join('%02x' % (memory.getByte(addr.add(index)) & 255) for index in range(length))

def address_state(value):
    addr = toAddr(value)
    primary = symbols.getPrimarySymbol(addr)
    symbol_rows = [symbol_row(item) for item in symbols.getSymbols(addr)]
    equate_rows = sorted([
        {'name': unicode(item.getName()), 'value': long(item.getValue()) & 0xffffffff}
        for item in equates.getEquates(addr)
    ], key=lambda item: item['name'])
    raw = bytes_hex(value, 4)
    at = functions.getFunctionAt(addr)
    containing = functions.getFunctionContaining(addr)
    instruction = listing.getInstructionAt(addr)
    return {
        'address': '0x%08x' % value,
        'bytes': raw,
        'rom_word': None if raw is None else long(memory.getInt(addr) & 0xffffffff),
        'symbols': symbol_rows,
        'symbol_count': len(symbol_rows),
        'primary_symbol': None if primary is None else symbol_row(primary),
        'data_at': data_row(listing.getDefinedDataAt(addr)),
        'data_containing': data_row(listing.getDefinedDataContaining(addr)),
        'instruction': None if instruction is None else unicode(instruction.toString()),
        'function_at': None if at is None else unicode(at.getName()),
        'function_containing': None if containing is None else unicode(containing.getName()),
        'references_from': refs_from(addr),
        'references_to': refs_to(addr),
        'equates': equate_rows,
        'eol': listing.getComment(CodeUnit.EOL_COMMENT, addr),
        'plate': listing.getComment(CodeUnit.PLATE_COMMENT, addr),
    }

def variable_row(variable):
    if variable is None:
        return None
    return {
        'name': unicode(variable.getName()),
        'data_type': unicode(variable.getDataType().getPathName()),
        'storage': unicode(variable.getVariableStorage().toString()),
        'source': str(variable.getSource()),
        'is_auto_parameter': bool(safe(lambda: variable.isAutoParameter(), False)),
        'is_register_variable': bool(variable.isRegisterVariable()),
        'is_stack_variable': bool(variable.isStackVariable()),
        'is_memory_variable': bool(variable.isMemoryVariable()),
    }

def body_ranges(function):
    rows = []
    iterator = function.getBody().getAddressRanges()
    while iterator.hasNext():
        item = iterator.next()
        rows.append(['0x%08x' % long(item.getMinAddress().getOffset()),
                     '0x%08x' % (long(item.getMaxAddress().getOffset()) + 1)])
    return rows

def function_row(value):
    addr = toAddr(value)
    function = functions.getFunctionAt(addr)
    if function is None:
        return None
    symbol = function.getSymbol()
    namespace = symbol.getParentNamespace()
    symbol_rows = [symbol_row(item) for item in symbols.getSymbols(addr)]
    params = []
    for parameter in function.getParameters():
        row = variable_row(parameter)
        row['ordinal'] = int(parameter.getOrdinal())
        row['first_use_offset'] = int(parameter.getFirstUseOffset())
        params.append(row)
    body_refs = []
    eols = []
    raw = []
    iterator = function.getBody().getAddresses(True)
    while iterator.hasNext():
        item = iterator.next()
        raw.append(chr(memory.getByte(item) & 255))
        body_refs.extend(refs_from(item))
        eol = listing.getComment(CodeUnit.EOL_COMMENT, item)
        if eol is not None:
            eols.append({'address': '0x%08x' % long(item.getOffset()), 'text': unicode(eol)})
    thunk = function.getThunkedFunction(False)
    thunk_row = None
    if thunk is not None:
        thunk_row = {'entry': str(thunk.getEntryPoint()), 'name': unicode(thunk.getName()),
                     'id': long(thunk.getSymbol().getID())}
    return {
        'entry': '0x%08x' % value,
        'name': unicode(function.getName()),
        'symbol': symbol_row(symbol),
        'symbols': symbol_rows,
        'symbol_count': len(symbol_rows),
        'namespace': {
            'name': None if namespace is None else unicode(namespace.getName()),
            'qualified_name': None if namespace is None else unicode(namespace.getName(True)),
            'id': None if namespace is None else safe(lambda: long(namespace.getID())),
            'global': namespace == global_ns,
        },
        'body': unicode(function.getBody().toString()),
        'body_ranges': body_ranges(function),
        'body_size': int(function.getBody().getNumAddresses()),
        'body_sha256': hashlib.sha256(''.join(raw)).hexdigest(),
        'body_references': body_refs,
        'eol_comments': eols,
        'calling_convention': unicode(function.getCallingConventionName()),
        'signature_source': str(function.getSignatureSource()),
        'prototype': unicode(function.getPrototypeString(False, False)),
        'custom_variable_storage': bool(function.hasCustomVariableStorage()),
        'varargs': bool(function.hasVarArgs()),
        'inline': bool(function.isInline()),
        'no_return': bool(function.hasNoReturn()),
        'external': bool(function.isExternal()),
        'thunk': bool(function.isThunk()),
        'thunk_target': thunk_row,
        'stack_purge_size': int(function.getStackPurgeSize()),
        'return': variable_row(function.getReturn()),
        'parameters': params,
        'plate': listing.getComment(CodeUnit.PLATE_COMMENT, addr),
        'incoming': refs_to(addr),
    }

def module_symbols():
    rows = []
    iterator = symbols.getAllSymbols(True)
    while iterator.hasNext():
        item = iterator.next()
        address = item.getAddress()
        if address.isMemoryAddress() and SEGMENT_START <= long(address.getOffset()) < SEGMENT_END:
            row = symbol_row(item)
            row['address'] = '0x%08x' % long(address.getOffset())
            rows.append(row)
    return rows

def module_comments():
    rows = []
    types = [CodeUnit.PLATE_COMMENT, CodeUnit.EOL_COMMENT, CodeUnit.PRE_COMMENT,
             CodeUnit.POST_COMMENT, CodeUnit.REPEATABLE_COMMENT]
    names = ['PLATE', 'EOL', 'PRE', 'POST', 'REPEATABLE']
    for value in range(SEGMENT_START, SEGMENT_END):
        addr = toAddr(value)
        for index in range(len(types)):
            comment = listing.getComment(types[index], addr)
            if comment is None:
                continue
            owner = functions.getFunctionContaining(addr)
            rows.append({
                'address': '0x%08x' % value,
                'type': names[index],
                'text': unicode(comment),
                'characters': len(comment),
                'sha256': text_hash(unicode(comment)),
                'ascii': all(ord(ch) < 128 for ch in comment),
                'owner': None if owner is None else '0x%08x' % long(owner.getEntryPoint().getOffset()),
            })
    return rows

def expected_function(prestate, new_plate=None):
    rows = [item for item in prestate['functions'] if item['entry'].lower() == '0x080a38fc']
    require(len(rows) == 1, 'PRESTATE_TARGET_FUNCTION_COUNT')
    if not rows:
        return None
    result = json.loads(json.dumps(rows[0]))
    if new_plate is not None:
        result['plate'] = new_plate
    return result

def expected_slots(prestate, new_plate=None):
    rows = json.loads(json.dumps(prestate['slots']))
    if new_plate is not None:
        for item in rows:
            if item['state']['address'].lower() == '0x080a38fc':
                item['state']['plate'] = new_plate
    return rows

def live_slots(prestate):
    return [{'source': item['source'], 'state': address_state(int(item['source']['address'], 16))}
            for item in prestate['slots']]

def expected_comments(prestate, new_plate=None):
    rows = json.loads(json.dumps(prestate['module_comments']))
    if new_plate is not None:
        matches = [item for item in rows if item['address'].lower() == '0x080a38fc' and item['type'] == 'PLATE']
        require(len(matches) == 1, 'PRESTATE_TARGET_PLATE_COMMENT_COUNT')
        if matches:
            matches[0]['text'] = new_plate
            matches[0]['characters'] = len(new_plate)
            matches[0]['sha256'] = text_hash(new_plate)
            matches[0]['ascii'] = True
    return rows

def verify_inputs(row):
    for relative, digest in sorted(INPUT_HASHES.items()):
        same('INPUT_HASH_' + relative, file_hash(root_path(relative)), digest)
    manifest = read_json(PROPOSAL_MANIFEST_NAME)
    require(len(manifest.get('files', [])) == 11, 'PROPOSAL_MANIFEST_FILE_COUNT')
    for item in manifest.get('files', []):
        same('PROPOSAL_MANIFEST_' + item['path'], file_hash(root_path(item['path'])), item['sha256'])
    review_basis = manifest.get('review_basis', {})
    require(review_basis.get('active_review_in_hash_inputs') is False, 'MANIFEST_ACTIVE_REVIEW_POLICY')
    same('MANIFEST_ARCHIVED_REVIEW', file_hash(root_path(review_basis['path'])), review_basis['sha256'])
    require(row.get('entry', '').lower() == '0x080a38fc', 'PLATE_ENTRY')
    require(row.get('current_name') == 'tick_equip_score_display_phase' and
            row.get('final_name') == row.get('current_name'), 'PLATE_FUNCTION_NAME')
    require(row.get('action') == 'PLATE_FULL_REWRITE', 'PLATE_ACTION')
    plate = row.get('new_plate', '')
    require(len(plate) == 490 and row.get('new_plate_chars') == '490', 'PLATE_LENGTH')
    require(all(ord(ch) < 128 for ch in plate) and row.get('ascii') == 'true', 'PLATE_ASCII')
    same('PLATE_HASH', text_hash(plate), 'a30952b1a94a5e28be7fc202eae44bf8709bbc31acf3dd538ab7f0ecb5357985')

def verify_plan(plan):
    require(plan.get('status') == 'F13_HISTORICAL_CLOSURE_PLAN_FROZEN', 'PLAN_STATUS')
    same('PLAN_INPUT_HASHES', plan.get('input_hashes'), INPUT_HASHES)
    same('PLAN_COUNTS', plan.get('counts'), EXPECTED_COUNTS)
    same('PLAN_SCRIPT_HASH', plan.get('script_sha256'), file_hash(root_path('tools/ghidra-labeling/RefineF13HistoricalClosure.py')))
    same('PLAN_PRESTATE_HASH', plan.get('prestate_sha256'), file_hash(run_path(PRESTATE_NAME)))
    same('PLAN_SOURCE_SNAPSHOT_HASH', plan.get('source_snapshot_sha256'), file_hash(run_path(SOURCE_SNAPSHOT_NAME)))
    same('PLAN_PROPOSAL_MANIFEST_HASH', plan.get('proposal_manifest_sha256'), file_hash(run_path(PROPOSAL_MANIFEST_NAME)))
    same('PLAN_DB_BACKUP_HASH', plan.get('db_backup_manifest_sha256'), file_hash(run_path(DB_BACKUP_MANIFEST_NAME)))
    require(plan.get('source_snapshot_file_count') == 87, 'PLAN_SOURCE_SNAPSHOT_COUNT')
    same('PLAN_SEGMENT', plan.get('segment'), {
        'start': '0x0809d718', 'end': '0x080a78dc', 'size': 41412,
        'sha256': '14088b711a72b6d2e30aa5b97824816604c5b30c3bf4bae74f42a3f2d6150286'})

def verify_common(prestate):
    same('PROGRAM_FUNCTION_COUNT', int(functions.getFunctionCount()), EXPECTED_FUNCTION_COUNT)
    same('SEGMENT_RAW_HASH', raw_hash(SEGMENT_START, SEGMENT_END), prestate['segment']['sha256'])
    same('SEGMENT_SIZE', prestate['segment']['size'], SEGMENT_SIZE)
    same('MODULE_SYMBOLS', module_symbols(), prestate['module_symbols'])
    require(len(prestate['functions']) == 214 and len(prestate['words']) == 1530 and
            len(prestate['targets']) == 152 and len(prestate['slots']) == 44 and
            len(prestate['extra_units']) == 41412, 'PRESTATE_COMPLETE_COUNTS')

def verify_prestate(prestate, row):
    verify_common(prestate)
    same('TARGET_FUNCTION_PRE', function_row(TARGET), expected_function(prestate))
    same('RAW_AND_BOOKEND_STATES_PRE', live_slots(prestate), expected_slots(prestate))
    same('MODULE_COMMENTS_PRE', module_comments(), prestate['module_comments'])
    fn = functions.getFunctionAt(toAddr(TARGET))
    require(fn is not None and long(fn.getSymbol().getID()) == TARGET_ID, 'TARGET_FUNCTION_ID')
    same('OLD_PLATE_LENGTH', len(function_row(TARGET)['plate']), 1458)
    same('OLD_PLATE_HASH', text_hash(function_row(TARGET)['plate']), row['old_plate_sha256'])

def verify_post(prestate, row):
    plate = row['new_plate']
    verify_common(prestate)
    same('TARGET_FUNCTION_POST', function_row(TARGET), expected_function(prestate, plate))
    same('RAW_AND_BOOKEND_STATES_POST', live_slots(prestate), expected_slots(prestate, plate))
    same('MODULE_COMMENTS_POST', module_comments(), expected_comments(prestate, plate))
    same('NEW_PLATE_LENGTH', len(function_row(TARGET)['plate']), 490)
    same('NEW_PLATE_HASH', text_hash(function_row(TARGET)['plate']),
         'a30952b1a94a5e28be7fc202eae44bf8709bbc31acf3dd538ab7f0ecb5357985')

row = read_plate_row()
verify_inputs(row)
prestate = read_json(PRESTATE_NAME)
plan = read_json(PLAN_NAME)
verify_plan(plan)

if MODE == 'dry':
    verify_prestate(prestate, row)
    reject('DRY')
    result = {
        'status': 'F13_HISTORICAL_CLOSURE_DRY_OK', 'FAIL': 0,
        'counts': EXPECTED_COUNTS, 'function_count': int(functions.getFunctionCount()),
        'module_functions': len(prestate['functions']), 'module_words': len(prestate['words']),
        'module_targets': len(prestate['targets']), 'module_slots': len(prestate['slots']),
        'module_units': len(prestate['extra_units']),
        'script_sha256': file_hash(root_path('tools/ghidra-labeling/RefineF13HistoricalClosure.py')),
        'plan_sha256': file_hash(run_path(PLAN_NAME)),
        'prestate_sha256': file_hash(run_path(PRESTATE_NAME)),
        'source_snapshot_sha256': file_hash(run_path(SOURCE_SNAPSHOT_NAME)),
    }
    write_json('f13-closure-dry-result.json', result)
    print('STATUS: OK mode=dry PLATE=1 FUNCTIONS=214 WORDS=1530 UNITS=41412 FAIL=0')
elif MODE == 'check':
    verify_post(prestate, row)
    reject('CHECK')
    result = {
        'status': 'F13_HISTORICAL_CLOSURE_PERSISTED_CHECK_OK', 'FAIL': 0,
        'counts': EXPECTED_COUNTS,
        'script_sha256': file_hash(root_path('tools/ghidra-labeling/RefineF13HistoricalClosure.py')),
        'plan_sha256': file_hash(run_path(PLAN_NAME)),
        'prestate_sha256': file_hash(run_path(PRESTATE_NAME)),
    }
    write_json('f13-closure-persisted-check.json', result)
    print('STATUS: OK mode=check PLATE=1 FAIL=0')
else:
    verify_prestate(prestate, row)
    reject('APPLY_PRESTATE')
    transaction = currentProgram.startTransaction('F13 Historical Closure approved PLATE rewrite')
    commit = False
    try:
        listing.setComment(toAddr(TARGET), CodeUnit.PLATE_COMMENT, row['new_plate'])
        verify_post(prestate, row)
        reject('APPLY_POST')
        commit = True
    finally:
        currentProgram.endTransaction(transaction, commit)
    result = {
        'status': 'F13_HISTORICAL_CLOSURE_APPLY_OK', 'FAIL': 0,
        'counts': EXPECTED_COUNTS, 'transaction_committed': True,
        'script_sha256': file_hash(root_path('tools/ghidra-labeling/RefineF13HistoricalClosure.py')),
        'plan_sha256': file_hash(run_path(PLAN_NAME)),
        'prestate_sha256': file_hash(run_path(PRESTATE_NAME)),
    }
    write_json('f13-closure-apply-receipt.json', result)
    print('STATUS: OK mode=apply PLATE=1 FAIL=0 transaction_committed=true')
