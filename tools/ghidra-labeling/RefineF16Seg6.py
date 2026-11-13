# -*- coding: ascii -*-
#@runtime Jython
#@category Ygo-ex2006.Refine
# Seg6 reviewed symbols/comments only. Root controls every native invocation.
import csv,json,os,traceback,hashlib,re
from collections import Counter
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import RefType,SourceType
csv.field_size_limit(2**27)
ARGS=list(getScriptArgs());MODE=ARGS[0].lower() if ARGS else 'dry'
if MODE not in ('prestate','dry','fullrollback','apply','check'):raise RuntimeError('Unknown mode')
if MODE in ('apply','check'):
 if len(ARGS)!=2:raise RuntimeError('Explicit Root grant SHA256 required')
 SAVE_GRANT_SHA_ARG=ARGS[1]
else:
 if len(ARGS)>1:raise RuntimeError('Save grant forbidden in readonly phase')
 SAVE_GRANT_SHA_ARG=None
ROOT=os.path.abspath(os.path.join(str(getSourceFile().getParentFile()),'..','..'))
RUN=os.path.join(ROOT,'output','refine-run-20261028-105948')
EVIDENCE_VERSION='v1'
PLAN_NAME='f16-seg6-plan-v1.json'
PRESTATE_NAME='f16-seg6-fresh-full-prestate-v1.json'
SNAPSHOT_NAME='f16-seg6-source-snapshot-preapply-v2.json'
FRESH_PROOF_NAME='f16-seg6-fresh-canonical-proof-v1.json'
AUTH_CONTRACT_NAME='f16-seg6-once-save-contract-v3.json'
GRANT_NAME='root-f16-seg6-implementation-gate.json'
ROOT_ATTEMPT_NAME='f16-seg6-apply-once-v1.json'
SCRIPT_CLAIM_NAME='f16-seg6-script-apply-claim-v1.json'
APPLY_RECEIPT_NAME='f16-seg6-apply-v1.json'
PHASE1A_MANIFEST_NAME='f16-seg6-phase1a-manifest-v2.json'
PHASE1_MANIFEST_NAME='f16-seg6-phase1-manifest-v1.json'
PHASE1_AUDIT_NAME='f16-seg6-phase1-static-review-v1.json'
FAILS=[]
is_lower_hex64=lambda value:isinstance(value,basestring) and re.match(r'^[0-9a-f]{64}$',value) is not None

INPUT_HASHES = {'output/refine-run-20261028-105948/f16-seg6-analysis-source-v3.json': '84ca5339f10f31c8757b94f7a88bc8351d7593099e963e6bf472756f115b8426', 'output/refine-run-20261028-105948/f16-seg6-inputs-v3.json': 'bfdfeb4b1c624a4643a7aa034eb420addb14d7e424ba6b2e8e5d37f000ef5886', 'output/refine-run-20261028-105948/f16-seg6-primitives-v3.json': '75f8f8994e682705d2bbba570c1625b6b35fd6877ddddb7216c519ac3a3970ca', 'output/refine-run-20261028-105948/f16-seg6-semantic-authoring-source-v3.json': 'f75f5a9d6c894bd87387ab2e0cd18baf9aeb8f4cf9139ecdcd1680a988bb6861', 'output/refine-run-20261028-105948/f16-seg6-mode-a-final-v3.json': '0ece707788a2f45e0c94bd37e8ec48abe1d63c48a5877d13988ea397e19319b4', 'output/refine-run-20261028-105948/f16-seg6-mode-a-evidence-v3.json': '4768b1ea8b7762def75c8815617edbd522303942896b8843299be40ca904ac7c', 'output/refine-run-20261028-105948/f16-seg6-mode-a-diff-v3.json': 'd88b853fd78e074c48f69d68af68ce8c0c00087c0cea036b6633477330d1a778', 'output/refine-run-20261028-105948/f16-seg6-modea-archive-mapping-v3.json': '5d783d6e70d121e4774f675db934296e369af2a7f8f022e8e5cf0d997166f83c', 'output/refine-run-20261028-105948/f16-seg6-executor-modea-proposal-archive-v3.md': '14734fc7d791ffe99a1b6e93c9971dc40737cbfde4be01c5c60e3c35e175020f', 'output/refine-run-20261028-105948/f16-seg6-semantic-review-final-v2.json': '8ffa2a280645e218c197e59b8e885b5c57202f7d88e7ae70e516144ddf0f87d6', 'output/refine-run-20261028-105948/root-f16-seg6-review-v2-archive-v1.json': 'ff9c86c1860b1c3fb140de578f8e9a076f060305196c81aaa2b469bf3b29ed8c', 'output/refine-run-20261028-105948/f16-seg6-final-manifest-v2.json': 'e52f9003a76d98667da1ab3c778522ecca57be4b850a3ce6aeb8b992917af5ed', 'output/refine-run-20261028-105948/f16-seg6-structural-only-final-v1.json': 'c67ca7f3d962d805bf92c35a1ed2e86664f149162e2d6eed7767cbff2a0677b7', 'output/refine-run-20261028-105948/f16-seg6-negative-suite-v1.json': 'f4f9f72a8068f75c1a953c2336d236c117968911e377f6d05e709ca6cd587d7e', 'output/refine-run-20261028-105948/f16-seg6-focused-patch-suite-v2.json': 'd9918ae5a428cc9745f3afe6649bd0bd8c3998de25ce27f865213021794f9819', 'output/refine-run-20261028-105948/f16-seg6-selfcheck-v3.json': '2de9cf68989fb845194566ff7410c9bc4282f532d773678010732cf28cdd82de', 'output/refine-run-20261028-105948/f16-seg6-focused-patch-suite-v3.json': 'bdadf1f8e330b28c24e82df42f512b510f73b8ae5fc3c8c4a150e0445a22a3f6', 'output/refine-run-20261028-105948/f16-seg6-formal3-CAS-v3.json': '64abeee92417765476b8329cc5c2aebb6208bcd1a984b9be3a7f03a58d07e25d', 'output/refine-run-20261028-105948/f16-seg6-decisions-v3.json': '921d6872f302e28298a10e3a48a497a4308277c13a0602a5eb915409b981d168', 'output/refine-run-20261028-105948/f16-seg6-slot-plan-v3.json': 'acc8c06a6f29b7b36b732d961b87c6896f919295784df297b724f082113189ba', 'output/refine-run-20261028-105948/f16-seg6-target-plan-v3.json': 'd23d46f6f688f038b8ba1fc8be5eecb28b0f6cceeac8b029e0c31b3a9b0a1453', 'output/refine-run-20261028-105948/f16-seg6-function-plan-v3.json': 'fef254a97a04a81869edd542b61491cc2b8528dbd20420198f1621eecc4efed8', 'output/refine-run-20261028-105948/f16-seg6-full-function-observation-plan-v3.json': 'ba9e34df39ca9b4d8e1fb037633025690f6d1ed81bd15a1f8cd25b319a2d2952', 'output/refine-run-20261028-105948/f16-seg6-fullstate-observation-plan-v3.json': '14d66c9e232478d31acc75e13fa41c5405a003a0ae08dce34df9363e0c6a18d2', 'output/refine-run-20261028-105948/f16-seg6-native-query-full-observation-plan-v3.json': '5b30f07c1e7d774b8d56fcd419047ac9e3b5e2c0cef41801d9b74412c3584ecd', 'output/refine-run-20261028-105948/f16-seg6-instruction-properties-plan-v3.json': 'c73f4ef3c17516d9165202e77c6adbcd57f4eaa94a6f47569ad0a71fcc401668', 'output/refine-run-20261028-105948/f16-seg6-label-closure-plan-v3.json': '7c09ebb57898a2eb6a46e5bc7a09f8f1472e163da520bece8efb46b1ffedb801', 'output/refine-run-20261028-105948/f16-seg6-global-equates-plan-v3.json': 'af6a5dd3bb126b05edf197d90470ee470923f3f329208b5c9dfcb29ddaaca1ac', 'output/refine-run-20261028-105948/f16-seg6-native-module-metadata-plan-v3.json': 'cf2d30aaa4f2bd87ee4f922660dd4616817087aa0e3f715426fe794ba8153003', 'output/refine-run-20261028-105948/f16-seg6-primary-symbol-plan-v3.json': '0d20a49f6d49be74d4e5ceb85f3107ba8bd3c0c4e95452f9e090d14db46a822b', 'output/refine-run-20261028-105948/f16-seg6-semantic-plan-v3.json': '7446882a97d30c3095af17a48ae18c7167e5778d0b66649aadc9b34a7da6c76c', 'output/refine-run-20261028-105948/f16-seg6-gas-projections-v3.json': 'ff1dabef4a29437a5ca015dd304f4542bc4f4dd559a81bb055b987940a425674', 'output/refine-run-20261028-105948/f16-seg6-native-resolver-execution-v3.json': '15633a11aeff97e952c9a2f35b0f685ac4b24851743c7574aec2d215c6c3d5bc', 'output/refine-run-20261028-105948/f16-seg6-registry-plan-v3.json': '0c26f9f9eb6efd94ed8a1fe9c344c9a06dbca118fda75b222f9e361d48bd7b48', 'output/refine-run-20261028-105948/f16-seg6-name-reference-baseline-v3.json': 'f5ff8de9ce92e0c1533000c1f7bb86d34d22e6065bc3db3cfd78be52930d08de', 'output/refine-run-20261028-105948/f16-seg6-source-scope-plan-v3.json': '92d94ac562155b38ba85ce9021017e6d31af0f3f1d5cf2cf6afa95103468db9b', 'output/refine-run-20261028-105948/f16-seg6-once-save-contract-v3.json': 'de41a946e1b52dc80d62a2d7d4b6346ef90cad40ed31c7677dc6e2ca3069a126', 'output/refine-run-20261028-105948/f16-seg6-slots-final-v3.tsv': 'ca041835e82bddea984e4d8f106be65c62a70aefd0afcf9fde9bc562cb66771f', 'output/refine-run-20261028-105948/f16-seg6-plates-final-v3.tsv': 'd7aff52dc9d687c325372b1bf1a42cea7ab8bca4103de7d92caf9a06b361c600', 'output/refine-run-20261028-105948/f16-seg6-proposal-final-v3.md': 'b2e7e21ad74dd4cdb32a17f8659eb5b55ffc6927eddf33d20745d25361a360d3', 'doc/dev/refine/F16-Seg-6.proposal.md': 'b2e7e21ad74dd4cdb32a17f8659eb5b55ffc6927eddf33d20745d25361a360d3', 'doc/dev/refine/F16-Seg-6.slots.tsv': 'ca041835e82bddea984e4d8f106be65c62a70aefd0afcf9fde9bc562cb66771f', 'doc/dev/refine/F16-Seg-6.plates.tsv': 'd7aff52dc9d687c325372b1bf1a42cea7ab8bca4103de7d92caf9a06b361c600', 'doc/dev/refine/F16-Seg-6.review.md': '74a90d54d830a26270ca30f39e4af934f2fbd03dd194d9d87de96ab358a30a07', 'output/refine-run-20261028-105948/f16-seg6-semantic-review-independent-r3-v3.json': '2a03f2e6314a2f84a49c40d33c8521acb5d01ed2db59506d9162200567d7aa90', 'output/refine-run-20261028-105948/f16-seg6-semantic-review-independent-r2-v2.json': 'd82065e894f5b24cdaf8a5a96ce09c11b4e6621392f311f6106ceced1d2f3dab', 'output/refine-run-20261028-105948/f16-seg6-semantic-review-r5-supplement-v1.json': 'da246993e72f73027a8d05db0564223f1b840cb67d141509fd642ff415d612fe', 'output/refine-run-20261028-105948/f16-seg6-semantic-review-independent-values-v1.json': 'de825f38b4f8acbf6bda3e8d9100e2bdf3ab5180165c8364f6b77d2184ea0570', 'output/refine-run-20261028-105948/f16-seg6-semantic-review-independent-refscan-v2.json': '477dbca7d7c921b31b366ee6408ff9c5ca93aef351df03e0b88f75f037ba91bd', 'output/refine-run-20261028-105948/f16-seg6-semantic-review-live-v1-archive.md': '1f0858c2656bcd1da45ed26fb70996de661bdfb6cfec26a37db28fa5541ae6bb', 'output/refine-run-20261028-105948/f16-seg6-semantic-review-live-v2-archive.md': '5c8b35511441408696cc8c6898d1c901f34260af5923bbfefad236b9b5003685', 'output/refine-run-20261028-105948/root-f16-seg6-complete-before-v1.json': 'c22545bc21e169cf6666a4b6186aaaded73836dbe7ac067df419728ecf6479a1', 'output/refine-run-20261028-105948/root-f16-seg6-native-before-v2.json': '943a2eaa94a5c2ba21f741a40b0e8021ac14f1645d5be339ba4b4f1d5d9ec3a3', 'output/refine-run-20261028-105948/root-f16-seg6-instruction-properties-before-v1.json': 'a39852d97be7feb3e9c5baa420a3b878b7148b0e02218a98b4a43ca52bf2114a', 'output/refine-run-20261028-105948/root-f16-seg6-typed-label-closure-before-v2.json': '7d031ed364e8e182c1d427789cbaff775393644f859cafd75764cd0ef0eb6bca', 'output/refine-run-20261028-105948/root-source-baseline-f16seg6.json': '10a9d92bda43f927b402453be3034b00f3cbececa8c4ea27c0d77f5154a2afdf', 'output/refine-run-20261028-105948/root-f16-seg6-db-backup.json': 'f86448815f04955689e2e9aea7257b649e7ee8cbba8e6a46b702d9bcdf3de162', 'output/refine-run-20261028-105948/root-f16-seg6-all-ID-before-gate-v1.json': 'b81c361bd73bc4620487cfeaca4e6a0c9402b369b08718eabb637908635bd7b5', 'output/refine-run-20261028-105948/root-f16-seg6-all-static-symbol-IDs-before-v1.json': 'cbfe0222273cc54fde4a68b7331f612677082ba1676d722b896117f9a7cd6e81', 'output/refine-run-20261028-105948/root-f16-seg6-all-dynamic-symbol-IDs-before-v1.json': 'ac1d47bf6495cc1acd0635c71eccac5f194baa12a27140d342199c9360f0e2ef', 'output/refine-run-20261028-105948/f16-seg6-firststage-manifest-v1.json': '61d9f230bc04e6750952aa6343863aa509c0be1f9734211f67042dcfcc44e787', 'output/refine-run-20261028-105948/f16-seg6-firststage-semantic-primitives-v1.json': '3fe1a7fcf3fedb30b2069cd433c20ee26d8c8e2801556e44e153f8b489913a59', 'output/refine-run-20261028-105948/f16-seg6-static-source-inventory-v1.json': '745b617b1b6bdfa46a2e522036ef07b681dfbb01ec71e32d613e8aeb46d0af80', 'output/refine-run-20261028-105948/f16-seg5-source-landing-pins-v1.json': 'dc72e4b32094cfa9f91e935547e582ac7bb017156b56f7c843138ab610b7f9b9', 'output/refine-run-20261028-105948/f16-seg1-analysis-validator-v2.py': '5472177d1856c01db0f2b1fd6cce08bd9e0fb69d289bdb725ad053b3b42da768', 'tools/asm-regen/ghidra/ExportRangeToGas.py': '4544a6a95f922f5a1779553555180ed2184955bc4fc1e92f96ad9b500ddaeb87', 'tools/ghidra-labeling/RenameKnownFunctions.py': 'cca3e9ad73f3252f9c04db404abfd1f70bd6ac23aa5b6fa4fe683afb3de18fd0', 'doc/dev/naming-proposals.csv': '4130fcf6f53ff0392d7983ad355e4b5386eb2a3fa032dc9b34506c6aefd153d8', 'temp/ghidra-functions.csv': '80267b164b0be2bcb1160a1c1e609dadca787f76dc098ebc1183ee99c79862ee', 'output/refine-run-20261028-105948/f16-seg6-mode-a-final-v2.json': '7f9a37941e74a46e6d583fede163636b3f9fa0516c50f35e83b7aca4ae0a94d5', 'output/refine-run-20261028-105948/f16-seg6-mode-a-evidence-v2.json': 'e9fcf6b93db0570908629e1725f5bbfe7afff5b346ef403379b894cb970becb4', 'output/refine-run-20261028-105948/f16-seg6-mode-a-diff-v2.json': '8a7886cb604599abb168a9cc623701ed70aca469bb38f9dcdc01082931840325', 'output/refine-run-20261028-105948/f16-seg6-semantic-review-final-v1.json': 'f6860ff04b0b488a851368a944035ca90cca76b6529ae7a63822bedab8481adb', 'output/refine-run-20261028-105948/f16-seg6-modea-archive-mapping-v2.json': '3aa94ef05c3aaf929140d6c12503991c07fe2ce99791a1b00ea3c49f4d425e52', 'output/refine-run-20261028-105948/f16-seg6-executor-modea-proposal-archive-v2.md': '89e8c2645691ac92b17b7a6d671e3488c388eb294c082648e0bbb7b5e82bbe47', 'output/refine-run-20261028-105948/f16-seg6-mode-a-authoring-diff-v3.patch': '31ed940c70b3004f64e35ee71d1421b83d681d16393e20439dfbda3c3224e650', 'output/refine-run-20261028-105948/f16-seg6-mode-a-proposal-diff-v3.patch': '6cea843ecf5b714c9071cfcac170b6bc234b7d4fc0d988b75359f63e47f0b268', 'output/refine-run-20261028-105948/f16-seg6-mode-a-proposal-intermediate-v3.md': '14734fc7d791ffe99a1b6e93c9971dc40737cbfde4be01c5c60e3c35e175020f', 'output/refine-run-20261028-105948/f16-seg6-mode-a-apply-v3.py': 'ce434e428af4cdee841d8e39781d7c0f5045ccf175cced2c5c46061148b3b80c', 'output/refine-run-20261028-105948/root-f16-seg6-resolved-functions-input-v1.json': '7f06c401e982d263ff1b052f6010d9b12bcc5af86f889d314c2a7abb2e1efc4f', 'output/refine-run-20261028-105948/root-f16-seg6-expanded-words-input-v1.json': '2d5ab282aee2df85ca9756be8734b2752a502f57c44cffdce123707f96e9d1d2', 'output/refine-run-20261028-105948/root-f16-seg6-expanded-slots-input-v1.json': '695d9f986055153c5ef7efdc2e18ded5afcf0ec31878a0196d3fed525e9ca3a6', 'output/refine-run-20261028-105948/root-f16-seg6-expanded-equates-input-v1.json': 'a5338d955b09046ec0b16f3a9625b7955c763aae07dc722e474e6078745f932f', 'output/refine-run-20261028-105948/root-f16-seg6-instruction-slots-input-v1.json': 'e3545723a3c9c627f487acf9e998a4463101d0b114ec830ca6c8b02e07a7d1fc', 'output/refine-run-20261028-105948/root-f16-seg6-empty-input-v1.json': '37517e5f3dc66819f61f5a7bb8ace1921282415f10551d2defa5c3eb0985b570', 'output/refine-run-20261028-105948/root-f16-seg6-label-closure-seeds-v1.json': 'f0c03c46ce7a0896bacbdb1eeb5bd61f71c7cfa0f6ec80c347fc845586df3e98', 'output/refine-run-20261028-105948/f16-seg6-final-manifest-v3.json': 'e8668649b96a1ab9de71fa49368a804c2c1acc0a739546acfef53847f23758b1'}
EXPECTED_COUNTS = {'EQ_ADD': 35, 'REF_ADD': 48, 'REF_PRESERVE': 15, 'CASE_VECTOR_PRESERVE_CORE': 78, 'SOURCE_LABEL': 98, 'SOURCE_EOL': 98, 'TARGET_LABEL': 5, 'DATA_REF_ADD': 48, 'FUNCTION_RENAME': 10, 'PLATE': 34, 'INSTRUCTION_EOL': 58}
COLLECTOR_INPUT_NAMES = ['root-f16-seg6-resolved-functions-input-v1.json', 'root-f16-seg6-expanded-words-input-v1.json', 'root-f16-seg6-expanded-slots-input-v1.json', 'root-f16-seg6-expanded-equates-input-v1.json', 'root-f16-seg6-instruction-slots-input-v1.json', 'root-f16-seg6-empty-input-v1.json', 'root-f16-seg6-label-closure-seeds-v1.json']
AUTH_CONTRACT_SHA256 = 'de41a946e1b52dc80d62a2d7d4b6346ef90cad40ed31c7677dc6e2ca3069a126'
ANALYSIS_FREEZE_SHA256 = 'e8668649b96a1ab9de71fa49368a804c2c1acc0a739546acfef53847f23758b1'
ANALYSIS_REVIEW_SHA256 = '74a90d54d830a26270ca30f39e4af934f2fbd03dd194d9d87de96ab358a30a07'

# -*- coding: ascii -*-
# Seg6 callable getter-only draft. No Script entry point, transaction or writer.
import hashlib
import re
try:
    long, unicode, basestring
except NameError:
    long, unicode, basestring = int, str, str


def configure_scope(function_requests, word_requests, slot_requests,
                    segment_equates, property_requests, nullable_property_heads,
                    closure_seeds, static_id_authority, all_id_authority):
    # Pure input binding. No Program getter, mutation or file access occurs here.
    global MODULE_START, MODULE_END, WORD_REQUESTS, SLOT_REQUESTS
    global OBSERVER_FUNCTIONS, PROPERTY_REQUEST_ADDRESSES, NULLABLE_PROPERTY_HEADS
    global CLOSURE_SEEDS, EXTERNAL_ALIAS_NAMES, PENALTY_EQUATE_NAMES
    global SEGMENT_EQUATE_NAMES, ALL_BEFORE_IDS
    def integer(value):
        return type(value) in (int, long) and 0 < value < 2**63
    def rows(value, count, label):
        if type(value) is not list or len(value) != count:
            raise RuntimeError(label + ': strict input list/count')
        seen = set()
        previous = -1
        for row in value:
            if type(row) is not dict or not isinstance(row.get('address'), basestring) or re.match(r'^0x[0-9a-f]{8}$', row['address']) is None:
                raise RuntimeError(label + ': address DTO')
            address = int(row['address'], 16)
            if address in seen or address <= previous:
                raise RuntimeError(label + ': unique ordered addresses')
            seen.add(address)
            previous = address
        return seen
    rows(function_requests, 183, 'Function requests')
    rows(word_requests, 1933, 'word requests')
    slots = rows(slot_requests, 2765, 'slot requests')
    rows(property_requests, 18596, 'property requests')
    nullable = rows(nullable_property_heads, 0, 'nullable property heads')
    rows(closure_seeds, 2765, 'Tiny seeds')
    if type(segment_equates) is not list or segment_equates:
        raise RuntimeError('Exact empty segment-equate input')
    if static_id_authority.get('iteration_finished') is not True or all_id_authority.get('iteration_finished') is not True or all_id_authority.get('dynamic_ID_public_getter_verified') is not True:
        raise RuntimeError('Complete native BEFORE identity enumeration required')
    statics = static_id_authority['rows']
    if type(statics) is not list or len(statics) != 36258:
        raise RuntimeError('Complete36258 static authority rows')
    static_ids = []
    previous = 0
    for row in statics:
        if type(row) is not dict or set(row) != set(('id','address','name','qualified_name','type','source','dynamic','namespace_id')) or row['dynamic'] is not False or not integer(row['id']) or row['id'] <= previous:
            raise RuntimeError('Static identity DTO/type/order')
        static_ids.append(row['id'])
        previous = row['id']
    observed_static = all_id_authority['static_ids']
    if type(observed_static) is not list or len(observed_static) != 36258 or any(not integer(value) for value in observed_static) or observed_static != static_ids:
        raise RuntimeError('Independent native static identity lists disagree')
    expected_counts = {'iterated':84196,'static':36258,'dynamic':47938,'function_symbols':5414}
    counts = all_id_authority['counts']
    if type(counts) is not dict or set(counts) != set(expected_counts) or any(type(counts[key]) not in (int, long) or counts[key] != expected_counts[key] for key in expected_counts):
        raise RuntimeError('Strict complete84196 native identity counts')
    dynamics = all_id_authority['dynamic_rows']
    if type(dynamics) is not list or len(dynamics) != 47938:
        raise RuntimeError('Complete47938 dynamic authority rows')
    identities = set(static_ids)
    previous = 0
    for row in dynamics:
        if type(row) is not dict or set(row) != set(('id','address','type','source','dynamic','namespace_id')) or row['dynamic'] is not True or not integer(row['id']) or row['id'] <= previous or row['id'] in identities:
            raise RuntimeError('Dynamic identity DTO/type/order/disjointness')
        if type(row['namespace_id']) not in (int, long) or not 0 <= row['namespace_id'] < 2**63 or any(not isinstance(row[key], basestring) for key in ('address','type','source')):
            raise RuntimeError('Dynamic identity complete field types')
        identities.add(row['id'])
        previous = row['id']
    if len(identities) != 84196:
        raise RuntimeError('Complete84196 BEFORE identities')
    MODULE_START, MODULE_END = 0x080c1448, 0x080cbf0c
    # Preserve full request rows as the Java getter's source holder objects.
    WORD_REQUESTS, SLOT_REQUESTS = word_requests, slot_requests
    OBSERVER_FUNCTIONS = [int(row['address'], 16) for row in function_requests]
    PROPERTY_REQUEST_ADDRESSES = [int(row['address'], 16) for row in property_requests]
    NULLABLE_PROPERTY_HEADS = nullable
    CLOSURE_SEEDS = closure_seeds
    EXTERNAL_ALIAS_NAMES = ('check_equip_target_slot_eligible_by_field6_eq17_1','check_uria_tribute_slot_eligible_1','check_equip_target_slot_eligible_by_field9_eq4_field6_eq16_1','check_hamon_tribute_slot_eligible_1','check_equip_target_slot_eligible_by_whitelist_or_special_1','check_anteatereatingant_tribute_slot_eligible_1','exit_equip_phase_oob_epilogue')
    PENALTY_EQUATE_NAMES = ('ZONE_EFFECT_ATK_PENALTY_500','ZONE_EFFECT_ATK_PENALTY_400')
    SEGMENT_EQUATE_NAMES = segment_equates
    ALL_BEFORE_IDS = identities


def bind_program(program, address_converter):
    # Read getters only. Root's future readOnly probe owns invocation.
    global currentProgram, toAddr, listing, symbols, references, equates
    global memory, functions, global_ns, tmode_register, CodeUnit
    from ghidra.program.model.listing import CodeUnit
    currentProgram, toAddr = program, address_converter
    listing = program.getListing()
    symbols = program.getSymbolTable()
    references = program.getReferenceManager()
    equates = program.getEquateTable()
    memory = program.getMemory()
    functions = program.getFunctionManager()
    global_ns = program.getGlobalNamespace()
    tmode_register = program.getRegister('TMode')


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
        'flow_targets': [str(item) for item in inst.getFlows()],
        'fallthrough': None if inst.getFallThrough() is None else str(inst.getFallThrough()),
        'flow_type': str(inst.getFlowType()),
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

def equate_global_row(name):
    eq = equates.getEquate(name)
    if eq is None:
        return None
    refs = []
    for ref in eq.getReferences():
        refs.append({'address': str(ref.getAddress()), 'operand': int(ref.getOpIndex())})
    return {'name': unicode(eq.getName()), 'value': long(eq.getValue()) & 0xffffffff,
            'references': sorted(refs, key=lambda row: (row['address'], row['operand']))}

def instruction_property_row(value):
    address = toAddr(value)
    instruction = instruction_row(listing.getInstructionAt(address))
    if instruction is not None:
        instruction['address'] = '0x' + instruction['address']
        instruction['flow_targets'] = ['0x' + target for target in instruction['flow_targets']]
        if instruction['fallthrough'] is not None:
            instruction['fallthrough'] = '0x' + instruction['fallthrough']
    owners = {}
    for key, fn in (('function_at', functions.getFunctionAt(address)),
                    ('function_containing', functions.getFunctionContaining(address))):
        owners[key] = None if fn is None else {
            'entry': '0x' + str(fn.getEntryPoint()), 'name': unicode(fn.getName()),
            'id': long(fn.getSymbol().getID()),
        }
    return {
        'address': '0x%08x' % value, 'bytes': bytes_hex(value, 4),
        'instruction': instruction, 'function_at': owners['function_at'],
        'function_containing': owners['function_containing'],
    }

# -*- coding: ascii -*-
# Same-Program getter adapter, preserving the complete native Java query schema.
def native_state(value):
    row = address_state(value)
    inst = row.pop('instruction_at')
    row['instruction'] = None if inst is None else inst['text']
    for field in ('function_at', 'function_containing'):
        owner = row[field]
        row[field] = None if owner is None else owner['name']
    return row


def native_units(lo, hi):
    result = []
    for value in range(lo, hi):
        at = toAddr(value)
        unit = listing.getCodeUnitContaining(at)
        inst = listing.getInstructionAt(at)
        data = listing.getDefinedDataAt(at)
        owner = functions.getFunctionContaining(at)
        result.append({
            'address': '%08x' % value, 'byte': int(memory.getByte(at) & 255),
            'unit': None if unit is None else [str(unit.getMinAddress()), int(unit.getLength()), str(unit.getClass().getSimpleName())],
            'instruction_at': None if inst is None else unicode(inst.toString()),
            'flow_targets': [] if inst is None else [str(item) for item in inst.getFlows()],
            'fall_through': None if inst is None or inst.getFallThrough() is None else str(inst.getFallThrough()),
            'function': None if owner is None else str(owner.getEntryPoint()),
            'defined_data': None if data is None else '%s %d %s' % (str(data.getAddress()), int(data.getLength()), unicode(data.getDataType().getPathName())),
            'tmode': tmode_at(at),
        })
    return result


def native_comments():
    result = []
    types = [(CodeUnit.PLATE_COMMENT, 'PLATE'), (CodeUnit.EOL_COMMENT, 'EOL'),
             (CodeUnit.PRE_COMMENT, 'PRE'), (CodeUnit.POST_COMMENT, 'POST'),
             (CodeUnit.REPEATABLE_COMMENT, 'REPEATABLE')]
    for value in range(MODULE_START, MODULE_END):
        at = toAddr(value)
        for kind, name in types:
            text = listing.getComment(kind, at)
            if text is None:
                continue
            text = unicode(text)
            fn = functions.getFunctionContaining(at)
            result.append({'address': '0x%08x' % value, 'type': name, 'text': text,
                           'characters': len(text), 'sha256': hashlib.sha256(text.encode('utf8')).hexdigest(),
                           'ascii': all(ord(char) < 128 for char in text),
                           'owner': None if fn is None else '0x' + str(fn.getEntryPoint())})
    return result


def native_module_symbols():
    result = []
    iterator = symbols.getAllSymbols(True)
    while iterator.hasNext():
        item = iterator.next()
        at = item.getAddress()
        if at.isMemoryAddress() and MODULE_START <= long(at.getOffset()) < MODULE_END:
            row = symbol_row(item)
            row['address'] = '0x' + str(at)
            result.append(row)
    return result


def capture_native():
    word_rows = []
    target_sources = {}
    for source in WORD_REQUESTS:
        value = int(source['address'], 16)
        state = native_state(value)
        word_rows.append({'source': source, 'state': state})
        target = state['rom_word']
        if target is not None and 0x02000000 <= target < 0x0a000000:
            target_sources.setdefault(target, []).append('0x%08x' % value)
    targets = [{'value': '0x%08x' % value, 'sources': target_sources[value],
                'exact': native_state(value),
                'even_function': None if value & 1 == 0 else function_row(value - 1)}
               for value in sorted(target_sources)]
    globals_now = {}
    iterator = equates.getEquates()
    while iterator.hasNext():
        item = iterator.next()
        name = unicode(item.getName())
        if name in globals_now:
            raise RuntimeError('Duplicate global Equate ' + name)
        globals_now[name] = equate_global_row(name)
    return {
        'external_equate_aliases': dict((name, equate_global_row(name)) for name in EXTERNAL_ALIAS_NAMES),
        'penalty_equates': dict((name, equate_global_row(name)) for name in PENALTY_EQUATE_NAMES),
        'segment_equates': dict((name, equate_global_row(name)) for name in SEGMENT_EQUATE_NAMES),
        'global_equates': globals_now, 'module_symbols': native_module_symbols(),
        'module_comments': native_comments(), 'status': 'F14_MODULE_READONLY_PRESTATE_OK',
        'program_name': unicode(currentProgram.getName()), 'function_count': int(functions.getFunctionCount()),
        'segment': {'start': '0x%08x' % MODULE_START, 'end': '0x%08x' % MODULE_END,
                    'size': MODULE_END - MODULE_START, 'sha256': raw_hash(MODULE_START, MODULE_END)},
        'functions': [function_row(value) for value in OBSERVER_FUNCTIONS],
        'words': word_rows,
        'slots': [{'source': source, 'state': native_state(int(source['address'], 16))} for source in SLOT_REQUESTS],
        'targets': targets, 'extra_units': native_units(MODULE_START, MODULE_END),
        'protected_external_units': {'range': ['0x09e5ab58', '0x09e5ab88'], 'units': native_units(0x09e5ab58, 0x09e5ab88)},
        'counts': {'functions': len(OBSERVER_FUNCTIONS), 'words': len(word_rows), 'slots': len(SLOT_REQUESTS),
                   'targets': len(targets), 'extra_units': MODULE_END - MODULE_START},
    }


def capture_properties():
    addresses = set(PROPERTY_REQUEST_ADDRESSES)
    for value in OBSERVER_FUNCTIONS:
        fn = functions.getFunctionAt(toAddr(value))
        if fn is None:
            raise RuntimeError('Missing observed Function %08x' % value)
        iterator = listing.getInstructions(fn.getBody(), True)
        while iterator.hasNext():
            addresses.add(long(iterator.next().getAddress().getOffset()))
    rows = []
    for value in sorted(addresses):
        if listing.getInstructionAt(toAddr(value)) is None and value not in NULLABLE_PROPERTY_HEADS:
            raise RuntimeError('Missing existing property instruction %08x' % value)
        rows.append(instruction_property_row(value))
    return {'status': 'F14_MODULE_READONLY_PRESTATE_OK',
            'query_kind': 'ROOT_F16_SEG6_NATIVE_FUNCTION_UNION_INSTRUCTION_PROPERTIES_PRESTATE_V1',
            'program_name': unicode(currentProgram.getName()), 'function_count': int(functions.getFunctionCount()),
            'rows': rows, 'input_function_entries': ['0x%08x' % value for value in OBSERVER_FUNCTIONS],
            'input_instruction_slots': len(PROPERTY_REQUEST_ADDRESSES),
            'counts': {'instructions': len(rows)}}


def tiny_symbol(item):
    if item is None:
        return None
    result = symbol_row(item)
    result['address'] = str(item.getAddress())
    result['dynamic'] = bool(item.isDynamic())
    result['dynamic_api_available'] = True
    return result


def tiny_object(items):
    # The native Tiny Gson does not serialize null fields.
    result = {}
    for key, value in items.items():
        if value is None:
            continue
        if type(value) is dict:
            value = tiny_object(value)
        elif type(value) is list:
            value = [tiny_object(item) if type(item) is dict else item for item in value]
        result[key] = value
    return result


def capture_label_closure():
    from collections import deque
    from ghidra.program.model.data import Pointer
    from ghidra.program.model.address import Address
    discovered = set()
    pending = deque()
    def include(value):
        if not 0x02000000 <= value < 0x0a000000:
            raise RuntimeError('Tiny address range')
        if value not in discovered:
            if len(discovered) >= 262144:
                raise RuntimeError('Tiny bounded scope')
            discovered.add(value)
            pending.append(value)
    def span(data):
        if data.getLength() > 256:
            raise RuntimeError('Tiny typed unit exceeds 256 bytes')
        for value in range(long(data.getMinAddress().getOffset()), long(data.getMaxAddress().getOffset()) + 2):
            include(value)
    for request in CLOSURE_SEEDS:
        value = int(request['address'], 16)
        include(value)
        data = listing.getDefinedDataContaining(toAddr(value))
        if data is not None:
            span(data)
    edges = []
    edge_keys = set()
    while pending:
        value = pending.popleft()
        at = toAddr(value)
        for reference in references.getReferencesTo(at):
            data = listing.getDefinedDataContaining(reference.getFromAddress())
            if data is None or not isinstance(data.getDataType(), Pointer) or not isinstance(data.getValue(), Address):
                continue
            pointed = data.getValue()
            if pointed != at:
                continue
            key = str(data.getAddress()) + ':' + str(at)
            if key not in edge_keys:
                edge_keys.add(key)
                edges.append(tiny_object({'source_data': data_row(data), 'source_primary': tiny_symbol(symbols.getPrimarySymbol(data.getAddress())),
                                          'pointed_to': str(pointed), 'reference': ref_row(reference)}))
            span(data)
    rows = []
    count = 0
    for value in sorted(discovered):
        at = toAddr(value)
        incoming = []
        for reference in references.getReferencesTo(at):
            fn = functions.getFunctionContaining(reference.getFromAddress())
            owner = None if fn is None else {'entry': str(fn.getEntryPoint()), 'name': unicode(fn.getName()), 'id': long(fn.getSymbol().getID())}
            incoming.append(tiny_object({'reference': ref_row(reference), 'source_function': owner}))
        count += len(incoming)
        syms = [tiny_symbol(item) for item in symbols.getSymbols(at)]
        rows.append(tiny_object({'request': {'address': '0x%08x' % value}, 'address': '0x%08x' % value,
                                 'data_at': data_row(listing.getDefinedDataAt(at)), 'data_containing': data_row(listing.getDefinedDataContaining(at)),
                                 'primary_symbol': tiny_symbol(symbols.getPrimarySymbol(at)), 'symbols': syms, 'symbol_count': len(syms), 'incoming': incoming}))
    return {'status': 'F14_MODULE_READONLY_PRESTATE_OK', 'query_kind': 'ROOT_F16_SEG6_COMPLETE_CODE_AND_TYPED_LABEL_CLOSURE_GETTER_ONLY_V1',
            'program_name': unicode(currentProgram.getName()), 'function_count': int(functions.getFunctionCount()),
            'seed_requests': CLOSURE_SEEDS, 'pointer_edges': edges, 'rows': rows,
            'counts': {'slots': len(rows), 'incoming': count, 'seeds': len(CLOSURE_SEEDS), 'typed_pointer_edges': len(edges)}}


def capture_before_inventory():
    identities = set()
    iterator = symbols.getAllSymbols(True)
    while iterator.hasNext():
        item = iterator.next()
        identity = long(item.getID())
        if not 0 < identity < 2**63 or identity in identities:
            raise RuntimeError('Invalid or repeated native BEFORE identity')
        if item.isDynamic() and identity != long(symbols.getDynamicSymbolID(item.getAddress())):
            raise RuntimeError('Native dynamic public ID disagrees')
        identities.add(identity)
    if identities != ALL_BEFORE_IDS:
        raise RuntimeError('Native complete84196 BEFORE identities changed')
    return len(identities)


def capture():
    return {'status': 'F16_SEG6_READONLY_NATIVE_BUNDLE_DRAFT', 'program_name': unicode(currentProgram.getName()),
            'function_count': int(functions.getFunctionCount()), 'native': capture_native(),
            'instruction_properties': capture_properties(), 'label_closure': capture_label_closure()}

def read_json_path(path):
    with open(path, 'rb') as stream:
        return json.load(stream)

def read_json(name):
    return read_json_path(os.path.join(RUN, name))

def write_json(name, value):
    atomic_write_claim(name, value)

def file_hash(path):
    with open(path, 'rb') as stream:
        return hashlib.sha256(stream.read()).hexdigest()

def strict_bool(value, expected):
    return isinstance(value, bool) and value is expected

def strict_integer(value, expected=None, nonnegative=False):
    if not isinstance(value, (int, long)) or isinstance(value, bool):
        return False
    if expected is not None and value != expected:
        return False
    if nonnegative and value < 0:
        return False
    return True

def strict_integer_list(value, expected=None):
    if not isinstance(value, list) or any(not strict_integer(item) for item in value):
        return False
    return expected is None or value == expected

def strict_sized_hash_row(value):
    return (isinstance(value, dict) and
            set(value) == set(('size', 'sha256', 'snapshot_sha256')) and
            strict_integer(value.get('size'), nonnegative=True) and
            is_lower_hex64(value.get('sha256')) and
            is_lower_hex64(value.get('snapshot_sha256')) and
            value.get('sha256') == value.get('snapshot_sha256'))

def strict_evidence_version(value):
    return strict_integer(value, int(EVIDENCE_VERSION[1:]))

def require_file(name, message):
    path = os.path.join(RUN, name)
    if not os.path.isfile(path):
        raise RuntimeError(message + ': ' + name)
    return path

def atomic_write_claim(name, value):
    path = os.path.join(RUN, name)
    payload = json.dumps(value, ensure_ascii=True, sort_keys=True, indent=2) + '\n'
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    descriptor = os.open(path, flags)
    stream = None
    try:
        stream = os.fdopen(descriptor, 'w')
        descriptor = None
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
    finally:
        if stream is not None:
            stream.close()
        elif descriptor is not None:
            os.close(descriptor)
    return file_hash(path)

def expected_save_bindings():
    return {
        'script_sha256': file_hash(getSourceFile().getAbsolutePath()),
        'runtime_plan_sha256': file_hash(require_file(PLAN_NAME, 'Missing runtime plan')),
        'fresh_sha256': file_hash(require_file(PRESTATE_NAME, 'Missing fresh prestate')),
        'fresh_proof_sha256': file_hash(require_file(FRESH_PROOF_NAME, 'Missing fresh proof')),
        'source_snapshot_sha256': file_hash(require_file(SNAPSHOT_NAME, 'Missing source snapshot')),
        'analysis_freeze_sha256': INPUT_HASHES[
            'output/refine-run-20261028-105948/f16-seg6-final-manifest-v3.json'],
        'analysis_review_sha256': INPUT_HASHES['doc/dev/refine/F16-Seg-6.review.md'],
        'canonical_sha256': file_hash(require_file(
            'root-f16-seg6-native-before-v2.json',
            'Missing canonical prestate')),
        'phase1a_manifest_sha256': file_hash(require_file(
            PHASE1A_MANIFEST_NAME, 'Missing Phase1a manifest')),
        'phase1_manifest_sha256': file_hash(require_file(
            PHASE1_MANIFEST_NAME, 'Missing final Phase1 manifest')),
        'phase1_audit_sha256': file_hash(require_file(
            PHASE1_AUDIT_NAME, 'Missing final Phase1 audit')),
        'root_contract_sha256': file_hash(require_file(
            AUTH_CONTRACT_NAME, 'Missing authorization contract')),
    }

def validate_grant_document(grant_sha_arg):
    if not is_lower_hex64(grant_sha_arg):
        raise RuntimeError('Grant SHA must be 64 lowercase hex characters')
    contract_path = require_file(AUTH_CONTRACT_NAME, 'Missing authorization contract')
    if file_hash(contract_path) != AUTH_CONTRACT_SHA256:
        raise RuntimeError('Authorization contract hash mismatch')
    grant_path = require_file(GRANT_NAME, 'Missing Root save grant')
    actual_grant_sha = file_hash(grant_path)
    if actual_grant_sha != grant_sha_arg:
        raise RuntimeError('Root save grant CLI hash mismatch')
    grant = read_json_path(grant_path)
    string_constants = {
        'schema': 'F16_SEG6_ROOT_ONCE_SAVE_GATE_V2',
        'status': 'ROOT_F16_SEG6_IMPLEMENTATION_GATE_PASS',
        'segment': 'F16-Seg-6',
        'authorized_mode': 'apply',
    }
    for key, expected in string_constants.items():
        if grant.get(key) != expected:
            raise RuntimeError('Root save grant constant mismatch: ' + key)
    if not strict_bool(grant.get('apply_authorized'), True):
        raise RuntimeError('Root save grant constant mismatch: apply_authorized')
    if not strict_integer(grant.get('max_saved_apply'), 1):
        raise RuntimeError('Root save grant constant mismatch: max_saved_apply')
    if not strict_integer(grant.get('already_saved_apply'), 0):
        raise RuntimeError('Root save grant constant mismatch: already_saved_apply')
    if not strict_evidence_version(grant.get('evidence_version')):
        raise RuntimeError('Root save grant evidence version mismatch')
    nonce = grant.get('gate_nonce')
    if not is_lower_hex64(nonce):
        raise RuntimeError('Root save grant nonce invalid')
    expected = expected_save_bindings()
    for key, value in expected.items():
        actual = grant.get(key)
        if not is_lower_hex64(actual) or actual != value:
            raise RuntimeError('Root save grant binding mismatch: ' + key)
    phase1_manifest = read_json(PHASE1_MANIFEST_NAME)
    if (phase1_manifest.get('status') !=
            'F16_SEG6_PHASE1_%s_COMPLETE' % EVIDENCE_VERSION.upper() or
            not strict_bool(phase1_manifest.get('persistent_apply_authorized'), False) or
            not strict_integer(phase1_manifest.get('saved_apply_count'), 0)):
        raise RuntimeError('Final Phase1 manifest is not a no-save complete proof')
    phase1_audit = read_json(PHASE1_AUDIT_NAME)
    if (phase1_audit.get('status') != 'PASS' or
            not strict_bool(phase1_audit.get('final_phase1_pass'), True) or
            not strict_bool(phase1_audit.get('persistent_apply_authorized'), False)):
        raise RuntimeError('Final Phase1 audit is not an independent no-save PASS')
    return {
        'grant': grant,
        'grant_sha256': actual_grant_sha,
        'gate_nonce': nonce,
        'bindings': expected,
    }

def validate_root_attempt(auth):
    attempt_path = require_file(ROOT_ATTEMPT_NAME, 'Missing Root apply attempt')
    attempt = read_json_path(attempt_path)
    expected = {
        'status': 'ROOT_APPLY_ATTEMPT_STARTED',
        'segment': 'F16-Seg-6',
        'evidence_version': int(EVIDENCE_VERSION[1:]),
        'grant_sha256': auth['grant_sha256'],
        'gate_nonce': auth['gate_nonce'],
        'script_sha256': auth['bindings']['script_sha256'],
        'runtime_plan_sha256': auth['bindings']['runtime_plan_sha256'],
    }
    if set(attempt) != set(expected):
        raise RuntimeError('Root apply attempt keyset mismatch')
    for key, value in expected.items():
        actual = attempt.get(key)
        if key == 'evidence_version':
            valid = strict_integer(actual, value)
        else:
            valid = actual == value
        if not valid:
            raise RuntimeError('Root apply attempt mismatch: ' + key)
    return attempt

def claim_payload(auth):
    return {
        'status': 'CLAIMED_BEFORE_MUTATION',
        'segment': 'F16-Seg-6',
        'evidence_version': int(EVIDENCE_VERSION[1:]),
        'grant_sha256': auth['grant_sha256'],
        'gate_nonce': auth['gate_nonce'],
        'script_sha256': auth['bindings']['script_sha256'],
        'runtime_plan_sha256': auth['bindings']['runtime_plan_sha256'],
    }

def validate_claim_document(claim, auth):
    expected = claim_payload(auth)
    if set(claim) != set(expected):
        raise RuntimeError('Persistent apply claim keyset mismatch')
    for key, value in expected.items():
        actual = claim.get(key)
        if key == 'evidence_version':
            valid = strict_integer(actual, value)
        else:
            valid = actual == value
        if not valid:
            raise RuntimeError('Persistent apply claim binding mismatch: ' + key)
    return claim

def validate_transaction_marker(value, field, owned_transaction_id=None):
    expected_keys = set(('present', 'class_name'))
    if owned_transaction_id is not None:
        expected_keys.add('owned_transaction_id')
    if (not isinstance(value, dict) or set(value) != expected_keys or
            not strict_bool(value.get('present'), True) or
            not isinstance(value.get('class_name'), basestring) or
            not value.get('class_name') or
            (owned_transaction_id is not None and
             not strict_integer(value.get('owned_transaction_id'),
                                owned_transaction_id))):
        raise RuntimeError('Persistent apply receipt transaction marker mismatch: ' + field)
    return value

def validate_successful_apply_receipt(receipt, auth, claim_sha):
    progress_keys = set((
        'semantic_actions_applied', 'post_verified', 'post_pass',
        'rollback_after_capture_pass', 'rollback_forced', 'transaction_committed',
        'txn_before_managed_end', 'txn_after_managed_end', 'txn_before_own_start',
        'txn_after_own_start', 'txn_before_own', 'txn_before_own_end',
        'txn_after_own', 'txn_after_own_end', 'owned_transaction_id',
        'end_transaction_return', 'grant_sha256', 'gate_nonce', 'claim_sha256'))
    binding_keys = set(receipt_bindings(auth))
    required_keys = set(('status', 'mode', 'FAIL', 'counts', 'prestate_sha256'))
    required_keys.update(progress_keys)
    required_keys.update(binding_keys)
    if set(receipt) != required_keys:
        raise RuntimeError('Persistent apply receipt keyset mismatch')
    if receipt.get('status') != 'PASS' or receipt.get('mode') != 'apply':
        raise RuntimeError('Persistent apply receipt status/mode mismatch')
    if not strict_integer(receipt.get('FAIL'), 0):
        raise RuntimeError('Persistent apply receipt FAIL mismatch')
    for field in ('semantic_actions_applied', 'post_verified', 'post_pass',
                  'end_transaction_return', 'transaction_committed'):
        if not strict_bool(receipt.get(field), True):
            raise RuntimeError('Persistent apply receipt true control mismatch: ' + field)
    for field in ('rollback_forced', 'rollback_after_capture_pass'):
        if not strict_bool(receipt.get(field), False):
            raise RuntimeError('Persistent apply receipt false control mismatch: ' + field)
    counts = receipt.get('counts')
    if not isinstance(counts, dict) or set(counts) != set(EXPECTED_COUNTS):
        raise RuntimeError('Persistent apply receipt counts keyset mismatch')
    for key, expected in EXPECTED_COUNTS.items():
        if not strict_integer(counts.get(key), expected):
            raise RuntimeError('Persistent apply receipt count mismatch: ' + key)
    if not strict_integer(receipt.get('owned_transaction_id'), nonnegative=True):
        raise RuntimeError('Persistent apply receipt owned transaction id mismatch')
    before_managed = validate_transaction_marker(
        receipt.get('txn_before_managed_end'), 'txn_before_managed_end')
    owned_transaction_id = receipt.get('owned_transaction_id')
    after_start = validate_transaction_marker(
        receipt.get('txn_after_own_start'), 'txn_after_own_start',
        owned_transaction_id)
    before_own = validate_transaction_marker(
        receipt.get('txn_before_own'), 'txn_before_own',
        owned_transaction_id)
    before_own_end = validate_transaction_marker(
        receipt.get('txn_before_own_end'), 'txn_before_own_end',
        owned_transaction_id)
    if receipt.get('txn_after_managed_end') is not None:
        raise RuntimeError('Persistent apply receipt managed transaction remained active')
    if receipt.get('txn_before_own_start') is not None:
        raise RuntimeError('Persistent apply receipt owned precondition mismatch')
    if before_own != after_start:
        raise RuntimeError('Persistent apply receipt owned start duplicate mismatch')
    if before_own_end != after_start:
        raise RuntimeError('Persistent apply receipt owned end duplicate mismatch')
    if receipt.get('txn_after_own') is not None or receipt.get('txn_after_own_end') is not None:
        raise RuntimeError('Persistent apply receipt owned transaction remained active')
    if not before_managed:
        raise RuntimeError('Persistent apply receipt managed boundary missing')
    expected_bindings = receipt_bindings(auth)
    for key, value in expected_bindings.items():
        if receipt.get(key) != value:
            raise RuntimeError('Persistent apply receipt binding mismatch: ' + key)
    if (receipt.get('grant_sha256') != auth['grant_sha256'] or
            receipt.get('gate_nonce') != auth['gate_nonce'] or
            receipt.get('claim_sha256') != claim_sha):
        raise RuntimeError('Persistent apply receipt authorization mismatch')
    if receipt.get('prestate_sha256') != receipt.get('fresh_sha256'):
        raise RuntimeError('Persistent apply receipt prestate/fresh mismatch')
    if receipt.get('plan_sha256') != receipt.get('runtime_plan_sha256'):
        raise RuntimeError('Persistent apply receipt plan/runtime-plan mismatch')
    if receipt.get('freeze_sha256') != receipt.get('analysis_freeze_sha256'):
        raise RuntimeError('Persistent apply receipt freeze provenance mismatch')
    if receipt.get('review_sha256') != receipt.get('analysis_review_sha256'):
        raise RuntimeError('Persistent apply receipt review provenance mismatch')
    return receipt

def consume_apply_authorization(grant_sha_arg):
    auth = validate_grant_document(grant_sha_arg)
    validate_root_attempt(auth)
    if os.path.exists(os.path.join(RUN, SCRIPT_CLAIM_NAME)):
        raise RuntimeError('Persistent apply claim already exists')
    if os.path.exists(os.path.join(RUN, APPLY_RECEIPT_NAME)):
        raise RuntimeError('Persistent apply receipt already exists')
    payload = claim_payload(auth)
    try:
        claim_sha = atomic_write_claim(SCRIPT_CLAIM_NAME, payload)
    except OSError as error:
        raise RuntimeError('Atomic persistent apply claim failed: %s' % error)
    auth['claim'] = payload
    auth['claim_sha256'] = claim_sha
    return auth

def validate_check_authorization(grant_sha_arg):
    auth = validate_grant_document(grant_sha_arg)
    validate_root_attempt(auth)
    claim_path = require_file(SCRIPT_CLAIM_NAME, 'Missing persistent apply claim')
    receipt_path = require_file(APPLY_RECEIPT_NAME, 'Missing persistent apply receipt')
    claim = validate_claim_document(read_json_path(claim_path), auth)
    claim_sha = file_hash(claim_path)
    auth['claim'] = claim
    auth['claim_sha256'] = claim_sha
    receipt = read_json_path(receipt_path)
    validate_successful_apply_receipt(receipt, auth, claim_sha)
    auth['apply_receipt'] = receipt
    return auth

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
    if not isinstance(actual, list) or not isinstance(expected, list):
        fail(message + '_LIST_SHAPE', actual, expected)
        return
    exact(message, sorted_rows(actual), sorted_rows(expected))

def reject(phase):
    if FAILS:
        write_json('f16-seg6-%s-failures-%s.json' % (MODE, EVIDENCE_VERSION), {
            'status': 'FAIL', 'phase': phase, 'FAIL': len(FAILS),
            'failures': FAILS,
        })
        raise RuntimeError('%s FAIL=%d' % (phase, len(FAILS)))

def typed_atom(value):
    if type(value) is dict:
        return ('dict', tuple((key, typed_atom(child)) for key, child in sorted(value.items())))
    if type(value) is list:
        return ('list', tuple(typed_atom(child) for child in value))
    if isinstance(value, bool):
        return ('bool', value)
    if isinstance(value, (int, long)):
        return ('integer', value)
    if isinstance(value, basestring):
        return ('string', value)
    return (type(value).__name__, value)

def metadata_assert(label, actual, expected, field=None):
    bags = set(('references_from', 'references_to', 'body_references', 'references', 'incoming',
                'added_source_refs', 'eol_comments', 'module_symbols', 'module_comments'))
    if type(expected) is dict:
        if type(actual) is not dict or set(actual) != set(expected):
            raise RuntimeError(label + ': exact dict schema')
        for key in expected:
            metadata_assert(label + '.' + key, actual[key], expected[key], key)
    elif type(expected) is list:
        if type(actual) is not list:
            raise RuntimeError(label + ': strict list')
        if field in bags:
            if Counter(typed_atom(row) for row in actual) != Counter(typed_atom(row) for row in expected):
                raise RuntimeError(label + ': typed complete multiset')
        else:
            if len(actual) != len(expected):
                raise RuntimeError(label + ': list length')
            for index in range(len(expected)):
                metadata_assert(label + '[%d]' % index, actual[index], expected[index])
    elif typed_atom(actual) != typed_atom(expected):
        raise RuntimeError(label + ': exact typed scalar ' + repr(actual) + ' != ' + repr(expected))

def bind_dynamic(value, bindings):
    if isinstance(value, basestring) and value.startswith('DYNAMIC_USER_ID:'):
        if value not in bindings:
            raise RuntimeError('Unbound approved USER identity ' + value)
        return bindings[value]
    if type(value) is dict:
        return dict((key, bind_dynamic(child, bindings)) for key, child in value.items())
    if type(value) is list:
        return [bind_dynamic(child, bindings) for child in value]
    return value

def exact_ref_cores(value):
    return [ref_core(ref_row(ref)) for ref in references.getReferencesFrom(toAddr(value))]

def ensure_user_label(value, name):
    addr = toAddr(value)
    current = symbols.getPrimarySymbol(addr)
    existing = list(symbols.getSymbols(addr))
    if current is None:
        if existing:
            raise RuntimeError('Symbols without primary at %08x' % value)
        current = symbols.createLabel(addr, name, global_ns, SourceType.USER_DEFINED)
    else:
        if not current.isPrimary() or len(existing) != 1:
            raise RuntimeError('Primary precondition at %08x' % value)
        if unicode(current.getName(True)) != name or str(current.getSource()) != 'USER_DEFINED':
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
        raise RuntimeError('USER label failed at %08x' % value)

def ensure_equate(name, value, address, operand):
    eq = equates.getEquate(name)
    if eq is None:
        eq = equates.createEquate(name, value)
    elif (long(eq.getValue()) & 0xffffffff) != value:
        raise RuntimeError('Equate conflict ' + name)
    matches = [ref for ref in eq.getReferences()
               if ref.getAddress() == toAddr(address) and ref.getOpIndex() == operand]
    if not matches:
        eq.addReference(toAddr(address), operand)
        return True
    elif len(matches) != 1:
        raise RuntimeError('Equate multiplicity at %08x' % address)
    return False

def add_data_ref(source, item):
    expected = ref_core(item)
    existing = exact_ref_cores(source)
    if expected in existing:
        if existing.count(expected) != 1:
            raise RuntimeError('DATA multiplicity at %08x' % source)
        return False
    if existing:
        raise RuntimeError('DATA source occupied at %08x' % source)
    ref = references.addMemoryReference(toAddr(source), toAddr(int(item['to'], 16)),
                                         RefType.DATA, SourceType.USER_DEFINED,
                                         int(item['operand']))
    references.setPrimary(ref, bool(item['primary']))
    return True

def apply_function_names():
    for value, row in sorted(RENAMED_FUNCTIONS.items()):
        fn = functions.getFunctionAt(toAddr(value))
        if (fn is None or long(fn.getSymbol().getID()) != long(row['before']['symbol']['id']) or
                unicode(fn.getName()) != row['before']['name']):
            raise RuntimeError('Function rename precondition at %08x' % value)
        fn.setName(row['after']['name'], SourceType.USER_DEFINED)
        COUNTS['FUNCTION_RENAME'] += 1

def apply_target_labels():
    for value in sorted(TARGET_MATERIALIZATIONS):
        row = TARGET_CONTRACTS[value]
        if row['before'].get('eol') != row['after'].get('eol'):
            raise RuntimeError('Target EOL mutation forbidden at %08x' % value)
        ensure_user_label(value, row['after']['primary_symbol']['name'])
        COUNTS['TARGET_LABEL'] += 1

def apply_plates():
    for value, row in sorted(PLATES.items()):
        contract = FUNCTION_CONTRACTS.get(value)
        if contract is None:
            raise RuntimeError('Function contract missing at %08x' % value)
        fn = functions.getFunctionAt(toAddr(value))
        if fn is None or unicode(fn.getName()) != row['new_name']:
            raise RuntimeError('Function precondition at %08x' % value)
        if row['action'] == 'PRESERVE':
            if contract['action'] != 'PRESERVE':
                raise RuntimeError('Preserved PLATE contract action at %08x' % value)
            if listing.getComment(CodeUnit.PLATE_COMMENT, toAddr(value)) != row['old_plate']:
                raise RuntimeError('Preserved PLATE drift at %08x' % value)
            continue
        if row['action'] != 'FULL_REWRITE':
            raise RuntimeError('Unknown PLATE action at %08x' % value)
        expected_action = 'RENAME_PLATE' if row['old_name'] != row['new_name'] else 'PLATE'
        if contract['action'] != expected_action:
            raise RuntimeError('PLATE contract action at %08x' % value)
        listing.setComment(toAddr(value), CodeUnit.PLATE_COMMENT, row['new_plate'])
        COUNTS['PLATE'] += 1

def apply_all():
    apply_function_names()
    apply_target_labels()
    apply_slots()
    apply_plates()

def transaction_info_row(owned_transaction_id=None):
    info = currentProgram.getCurrentTransactionInfo()
    if info is None:
        return None
    result = {
        'present': True,
        'class_name': unicode(info.getClass().getName()),
    }
    if owned_transaction_id is not None:
        result['owned_transaction_id'] = long(owned_transaction_id)
    return result

def failure_payload(phase, error, progress=None):
    payload = {
        'status': 'FAIL', 'phase': phase, 'mode': MODE,
        'FAIL': len(FAILS), 'failures': FAILS,
        'error': unicode(error), 'traceback': traceback.format_exc(),
        'semantic_actions_applied': False,
        'post_verified': False,
    }
    if progress is not None:
        payload.update(progress)
    return payload


def read_bound(relative):
    path=os.path.join(ROOT,relative)
    if file_hash(path)!=INPUT_HASHES[relative]:raise RuntimeError('Frozen input drift '+relative)
    return read_json_path(path)
def artifact(name):return read_bound('output/refine-run-20261028-105948/'+name)
ROOT_FULL_PRESTATE=artifact('root-f16-seg6-native-before-v2.json')
PROPERTIES_BEFORE=artifact('root-f16-seg6-instruction-properties-before-v1.json')
LABEL_CLOSURE_BEFORE=artifact('root-f16-seg6-typed-label-closure-before-v2.json')
PRIMITIVES=artifact('f16-seg6-primitives-v3.json')
SLOT_PLAN=artifact('f16-seg6-slot-plan-v3.json')
FUNCTION_PLAN=artifact('f16-seg6-function-plan-v3.json')
TARGET_PLAN=artifact('f16-seg6-target-plan-v3.json')
NATIVE_AFTER=artifact('f16-seg6-native-query-full-observation-plan-v3.json')['after']
PROPERTY_PLAN=artifact('f16-seg6-instruction-properties-plan-v3.json')
LABEL_CLOSURE_PLAN=artifact('f16-seg6-label-closure-plan-v3.json')
BINDING=artifact('f16-seg6-inputs-v3.json')
COLLECTOR_INPUTS=[artifact(name) for name in COLLECTOR_INPUT_NAMES]
STATIC_ID_BEFORE=artifact('root-f16-seg6-all-static-symbol-IDs-before-v1.json')
ALL_ID_BEFORE=artifact('root-f16-seg6-all-dynamic-symbol-IDs-before-v1.json')
functions=currentProgram.getFunctionManager();listing=currentProgram.getListing()
memory=currentProgram.getMemory();symbols=currentProgram.getSymbolTable()
references=currentProgram.getReferenceManager();equates=currentProgram.getEquateTable()
global_ns=currentProgram.getGlobalNamespace();tmode_register=currentProgram.getRegister('TMode')
bind_program(currentProgram,toAddr)
configure_scope(*(COLLECTOR_INPUTS+[STATIC_ID_BEFORE,ALL_ID_BEFORE]))
RAW_SLOT_ROWS=read_tsv(os.path.join(ROOT,'doc/dev/refine/F16-Seg-6.slots.tsv'))
RAW_PLATE_ROWS=read_tsv(os.path.join(ROOT,'doc/dev/refine/F16-Seg-6.plates.tsv'))
SLOT_CONTRACTS=dict((int(x['address'],16),x) for x in SLOT_PLAN['rows'])
SLOTS={}
for row in RAW_SLOT_ROWS:
    value=int(row['address'],16);contract=SLOT_CONTRACTS[value]
    formal=dict(row);formal.update(old_value=row['value'],final_data_type=contract['before']['data_at']['type'],final_eol=contract['after']['eol'])
    SLOTS[value]=formal
SOURCE_LABEL_ADDRESSES=set(int(a,16) for a,x in PRIMITIVES['labels'].items() if x['kind']=='SOURCE_LABEL')
TARGET_MATERIALIZATIONS=set(int(a,16) for a,x in PRIMITIVES['labels'].items() if x['kind']=='TARGET_LABEL')
TARGET_CONTRACTS=dict((int(x['address'],16),x) for x in TARGET_PLAN['rows'])
FUNCTION_CONTRACTS={};PLATES={};RENAMED_FUNCTIONS={}
for row in FUNCTION_PLAN['rows']:
    value=int(row['entry'],16);before=row['before'];after=row['after'];renamed=before['name']!=after['name']
    contract=dict(row);contract['action']='RENAME_PLATE' if renamed else 'PLATE';FUNCTION_CONTRACTS[value]=contract
    PLATES[value]=dict(action='FULL_REWRITE',old_name=before['name'],new_name=after['name'],old_plate=before['plate'],new_plate=after['plate'])
    if renamed:RENAMED_FUNCTIONS[value]=contract
INSTRUCTION_EOLS=dict((int(a,16),t) for a,t in PRIMITIVES['instruction_eol'].items())
COUNTS=dict((key,0) for key in EXPECTED_COUNTS)

def verify_inputs():
    for relative,digest in INPUT_HASHES.items():
        if file_hash(os.path.join(ROOT,relative))!=digest:raise RuntimeError('Frozen input '+relative)
    review=open(os.path.join(ROOT,'doc/dev/refine/F16-Seg-6.review.md'),'rb').read().decode('utf8')
    if re.findall(r'(?m)^## Reviewer Verdict: F16-Seg-6 = ([^\r\n]+)\r?$',review)!=['PASS']:raise RuntimeError('Independent R3 PASS required')
    if len(SLOTS)!=176 or len(RAW_SLOT_ROWS)!=176 or len(PLATES)!=34 or len(RAW_PLATE_ROWS)!=34:raise RuntimeError('Exact formal scopes')
    for formal,row in zip(RAW_SLOT_ROWS,SLOT_PLAN['rows']):
        for key,target in [('address','address'),('value','value'),('action','action'),('GAS','gas_expression_after')]:metadata_assert('formal '+key,formal[key],row[target])
        metadata_assert('formal before',json.loads(formal['before_json']),row['before']);metadata_assert('formal after',json.loads(formal['after_json']),row['after'])
    for formal,row in zip(RAW_PLATE_ROWS,FUNCTION_PLAN['rows']):
        metadata_assert('plate entry',formal['entry'],row['entry']);metadata_assert('plate before',json.loads(formal['before_json']),row['before']);metadata_assert('plate after',json.loads(formal['after_json']),row['after'])
    if (len(RENAMED_FUNCTIONS),len(SOURCE_LABEL_ADDRESSES),len(TARGET_MATERIALIZATIONS),len(INSTRUCTION_EOLS))!=(10,98,5,58):raise RuntimeError('Action scopes')
    if PRIMITIVES['R4'] or PRIMITIVES['R7'] or PRIMITIVES['ABI_change'] or PRIMITIVES['body_change']:raise RuntimeError('No raw/body/ABI actions')
    for text in list(INSTRUCTION_EOLS.values())+[x['new_plate'] for x in PLATES.values()]:
        if not isinstance(text,basestring) or not all(ord(x)<128 for x in text):raise RuntimeError('ASCII setter')
    if any(len(x['new_plate'])>500 for x in PLATES.values()):raise RuntimeError('PLATE length')
    snapshot=read_json(SNAPSHOT_NAME);baseline=artifact('root-source-baseline-f16seg6.json')
    additions=set(['tools/ghidra-labeling/RefineF16Seg6.py']+['doc/dev/refine/F16-Seg-6.'+suffix for suffix in ('proposal.md','review.md','slots.tsv','plates.tsv')])
    if snapshot['file_count']!=222 or set(snapshot['files'])!=set(baseline['files'])|additions:raise RuntimeError('source222 exact membership')
    for relative,row in snapshot['files'].items():
        for base,digest in [(ROOT,row['sha256']),(os.path.join(ROOT,snapshot['snapshot_directory']),row['snapshot_sha256'])]:
            path=os.path.join(base,relative)
            if os.path.getsize(path)!=row['size'] or file_hash(path)!=digest:raise RuntimeError('source222 live/copy drift '+relative)

def runtime_capture():
    return capture()
def expected_before_bundle():
    return dict(status='F16_SEG6_READONLY_NATIVE_BUNDLE_DRAFT',program_name=ROOT_FULL_PRESTATE['program_name'],function_count=ROOT_FULL_PRESTATE['function_count'],native=ROOT_FULL_PRESTATE,instruction_properties=PROPERTIES_BEFORE,label_closure=LABEL_CLOSURE_BEFORE)
def verify_prestate(pre,recapture):
    metadata_assert('complete BEFORE',pre,expected_before_bundle())
    if recapture:
        capture_before_inventory();metadata_assert('same Program BEFORE',runtime_capture(),pre)
def expected_post_bundle(current):
    observed=dict((int(x['state']['address'],16),x['state']) for x in current['native']['slots'])
    planned=dict((int(x['state']['address'],16),x['state']) for x in NATIVE_AFTER['slots']);bindings={}
    for address,spec in PRIMITIVES['labels'].items():
        value=int(address,16);symbol=observed[value]['primary_symbol'];identity=symbol['id']
        if not strict_integer(identity) or not 0<identity<2**63 or identity in ALL_BEFORE_IDS:raise RuntimeError('New USER identity '+address)
        token='DYNAMIC_USER_ID:'+spec['name'];bindings[token]=identity
        metadata_assert('whole new USER '+address,symbol,bind_dynamic(planned[value]['primary_symbol'],{token:identity}))
    if len(bindings)!=103 or len(set(bindings.values()))!=103:raise RuntimeError('Distinct103 USER identities')
    result=expected_before_bundle();result.update(native=NATIVE_AFTER,instruction_properties=PROPERTY_PLAN['after_document'],label_closure=LABEL_CLOSURE_PLAN['after'])
    return bind_dynamic(result,bindings)
def verify_post(pre):
    current=runtime_capture();metadata_assert('complete POST',current,expected_post_bundle(current))
    if MODE in ('apply','fullrollback'):metadata_assert('exact action counts',COUNTS,EXPECTED_COUNTS)
    write_json('f16-seg6-'+MODE+'-complete-post-v1.json',current)
    return current
def apply_instruction_eols():
    for value,text in sorted(INSTRUCTION_EOLS.items()):
        if listing.getInstructionAt(toAddr(value)) is None:raise RuntimeError('Instruction EOL owner')
        listing.setComment(toAddr(value),CodeUnit.EOL_COMMENT,text);COUNTS['INSTRUCTION_EOL']+=1
def verify_plan(plan,prestate_hash):
    if plan.get('status')!='F16_SEG6_PLAN_FROZEN':raise RuntimeError('Frozen runtime plan required')
    required=dict(static_generation=2,runtime_evidence_version=EVIDENCE_VERSION,script_sha256=file_hash(getSourceFile().getAbsolutePath()),prestate_sha256=prestate_hash,source_snapshot_manifest=SNAPSHOT_NAME,source_snapshot_sha256=file_hash(os.path.join(RUN,SNAPSHOT_NAME)),fresh_proof_sha256=file_hash(os.path.join(RUN,FRESH_PROOF_NAME)),counts=EXPECTED_COUNTS,analysis_freeze_sha256=ANALYSIS_FREEZE_SHA256,analysis_review_sha256=ANALYSIS_REVIEW_SHA256)
    metadata_assert('exact runtime plan',plan,dict(required,status='F16_SEG6_PLAN_FROZEN'))
    proof=read_json(FRESH_PROOF_NAME)
    if proof.get('status')!='PASS' or proof.get('fresh_sha256')!=prestate_hash or proof.get('script_sha256')!=required['script_sha256']:raise RuntimeError('Fresh proof binding')

def apply_slots():
    for value, formal in sorted(SLOTS.items()):
        contract = SLOT_CONTRACTS[value]
        addr = toAddr(value)
        if (memory.getInt(addr) & 0xffffffff) != int(formal['old_value'], 16):
            raise RuntimeError('ROM value changed at %08x' % value)
        data = listing.getDefinedDataAt(addr)
        if data is None or data.getLength() != 4 or unicode(data.getDataType().getPathName()) != formal['final_data_type']:
            raise RuntimeError('Data contract at %08x' % value)
        action = formal['action']
        if action == 'EQ_ADD':
            items = contract['after']['equate_references']
            if len(items) != 1:
                raise RuntimeError('EQ malformed at %08x' % value)
            item = items[0]
            if not ensure_equate(item['name'], long(item['value']) & 0xffffffff, value, int(item['operand'])):
                raise RuntimeError('EQ binding unexpectedly existed at %08x' % value)
        elif action == 'REF_ADD':
            before_cores = [ref_core(item) for item in contract['before']['references_from']]
            new = [item for item in contract['after']['references_from'] if ref_core(item) not in before_cores]
            if len(new) != 1 or not add_data_ref(value, new[0]):
                raise RuntimeError('REF_ADD malformed/existing at %08x' % value)
            COUNTS['DATA_REF_ADD'] += 1
        elif action in ('REF_PRESERVE', 'CASE_VECTOR_PRESERVE_CORE'):
            before = [ref_core(item) for item in contract['before']['references_from']]
            if sorted_rows(exact_ref_cores(value)) != sorted_rows(before):
                raise RuntimeError('Preserved reference core drift at %08x' % value)
        else:
            raise RuntimeError('Unknown slot action at %08x' % value)
        if value in SOURCE_LABEL_ADDRESSES:
            after_primary = contract['after']['primary_symbol']
            if after_primary is None or after_primary.get('source') != 'USER_DEFINED':
                raise RuntimeError('Source primary contract at %08x' % value)
            ensure_user_label(value, after_primary['name'])
            COUNTS['SOURCE_LABEL'] += 1
        if action != 'CASE_VECTOR_PRESERVE_CORE':
            text = contract['after']['eol']
            if text != formal['final_eol'] or not isinstance(text, basestring) or not all(ord(char) < 128 for char in text):
                raise RuntimeError('Source EOL ASCII contract at %08x' % value)
            listing.setComment(addr, CodeUnit.EOL_COMMENT, text)
            COUNTS['SOURCE_EOL'] += 1
        COUNTS[action] += 1

def receipt_bindings(save_authorization=None):
    result = {
        'script_sha256': file_hash(getSourceFile().getAbsolutePath()),
        'plan_sha256': file_hash(os.path.join(RUN, PLAN_NAME)),
        'fresh_sha256': file_hash(os.path.join(RUN, PRESTATE_NAME)),
        'fresh_proof_sha256': file_hash(os.path.join(RUN, FRESH_PROOF_NAME)),
        'source_snapshot_sha256': file_hash(os.path.join(RUN, SNAPSHOT_NAME)),
        'freeze_sha256': INPUT_HASHES['output/refine-run-20261028-105948/f16-seg6-final-manifest-v3.json'],
        'review_sha256': INPUT_HASHES['doc/dev/refine/F16-Seg-6.review.md'],
    }
    if save_authorization is not None:
        result.update(save_authorization['bindings'])
        result.update({
            'grant_sha256': save_authorization['grant_sha256'],
            'gate_nonce': save_authorization['gate_nonce'],
            'claim_sha256': save_authorization['claim_sha256'],
        })
    return result

verify_inputs()
if MODE == 'prestate':
    capture_before_inventory()
    result = runtime_capture()
    verify_prestate(result, False)
    write_json(PRESTATE_NAME, result)
    print('STATUS: OK PRESTATE native183 states3262 props26385 Tiny14980')
elif MODE == 'dry':
    pre = read_json(PRESTATE_NAME)
    verify_prestate(pre, True)
    verify_plan(read_json(PLAN_NAME), file_hash(os.path.join(RUN, PRESTATE_NAME)))
    payload = {
        'status': 'PASS', 'mode': MODE, 'FAIL': 0,
        'semantic_actions_applied': False, 'post_verified': False,
        'post_pass': False, 'rollback_forced': False,
        'rollback_after_capture_pass': False,
        'transaction_committed': False,
        'counts': EXPECTED_COUNTS, 'prestate_sha256': file_hash(os.path.join(RUN, PRESTATE_NAME)),
    }
    payload.update(receipt_bindings())
    write_json('f16-seg6-dry-%s.json' % EVIDENCE_VERSION, payload)
    print('STATUS: OK DRY FAIL=0')
elif MODE in ('fullrollback', 'apply'):
    pre = read_json(PRESTATE_NAME)
    verify_prestate(pre, True)
    verify_plan(read_json(PLAN_NAME), file_hash(os.path.join(RUN, PRESTATE_NAME)))
    tx = None
    owned_open = False
    committed = False
    save_authorization = None
    stage = 'SAVE_AUTHORIZATION' if MODE == 'apply' else 'MANAGED_OUTER_PRECONDITION'
    progress = {
        'semantic_actions_applied': False,
        'post_verified': False,
        'post_pass': False,
        'rollback_after_capture_pass': False,
        'rollback_forced': MODE == 'fullrollback',
        'transaction_committed': False,
        'txn_before_managed_end': None,
        'txn_after_managed_end': None,
        'txn_before_own_start': None,
        'txn_after_own_start': None,
        'txn_before_own': None,
        'txn_before_own_end': None,
        'txn_after_own': None,
        'txn_after_own_end': None,
        'owned_transaction_id': None,
        'end_transaction_return': None,
        'grant_sha256': None,
        'gate_nonce': None,
        'claim_sha256': None,
    }
    try:
        if MODE == 'apply':
            save_authorization = consume_apply_authorization(SAVE_GRANT_SHA_ARG)
            progress['grant_sha256'] = save_authorization['grant_sha256']
            progress['gate_nonce'] = save_authorization['gate_nonce']
            progress['claim_sha256'] = save_authorization['claim_sha256']
        stage = 'MANAGED_OUTER_PRECONDITION'
        progress['txn_before_managed_end'] = transaction_info_row()
        require(progress['txn_before_managed_end'] is not None,
                'MANAGED_OUTER_PRESENT')
        reject('MANAGED_OUTER_PRECONDITION')
        stage = 'MANAGED_OUTER_END'
        this.end(False)
        progress['txn_after_managed_end'] = transaction_info_row()
        exact('MANAGED_OUTER_ENDED', progress['txn_after_managed_end'], None)
        reject('MANAGED_OUTER_END')
        stage = 'MANAGED_OUTER_RESTORE'
        verify_prestate(pre, True)
        reject('MANAGED_OUTER_RESTORE')
        progress['txn_before_own_start'] = transaction_info_row()
        exact('OWNED_TRANSACTION_PRE_NONE', progress['txn_before_own_start'], None)
        reject('OWNED_TRANSACTION_PRE')
        stage = 'OWNED_TRANSACTION_START'
        tx = currentProgram.startTransaction('F16-Seg-6 approved materialization')
        owned_open = True
        progress['owned_transaction_id'] = long(tx)
        progress['txn_after_own_start'] = transaction_info_row(tx)
        progress['txn_before_own'] = progress['txn_after_own_start']
        require(progress['txn_after_own_start'] is not None and
                progress['txn_after_own_start'].get('present') is True and
                long(progress['owned_transaction_id']) == long(tx),
                'OWNED_TRANSACTION_ACTIVE')
        reject('OWNED_TRANSACTION_START')
        stage = 'MUTATION'
        progress['semantic_actions_applied'] = True
        apply_all()
        apply_instruction_eols()
        stage = 'POST'
        verify_post(pre)
        progress['post_verified'] = True
        progress['post_pass'] = True
        progress['txn_before_own_end'] = transaction_info_row(tx)
        exact('OWNED_TRANSACTION_BEFORE_END',
              progress['txn_before_own_end'], progress['txn_after_own_start'])
        reject('OWNED_TRANSACTION_BEFORE_END')
        stage = 'OWNED_TRANSACTION_END'
        progress['end_transaction_return'] = bool(
            currentProgram.endTransaction(tx, MODE == 'apply'))
        owned_open = False
        if MODE == 'apply':
            require(progress['end_transaction_return'] is True,
                    'OWNED_TRANSACTION_APPLY_COMMITTED')
        committed = MODE == 'apply' and progress['end_transaction_return'] is True
        progress['transaction_committed'] = committed
        progress['txn_after_own'] = transaction_info_row()
        progress['txn_after_own_end'] = progress['txn_after_own']
        exact('OWNED_TRANSACTION_ENDED', progress['txn_after_own'], None)
        reject('OWNED_TRANSACTION_END')
        if MODE == 'fullrollback':
            stage = 'ROLLBACK_RESTORE'
            verify_prestate(pre, True)
            reject('ROLLBACK_RESTORE')
            progress['rollback_after_capture_pass'] = True
        payload = {
            'status': 'PASS', 'mode': MODE, 'FAIL': 0,
            'counts': COUNTS,
            'prestate_sha256': file_hash(os.path.join(RUN, PRESTATE_NAME)),
        }
        payload.update(progress)
        payload.update(receipt_bindings(save_authorization))
        write_json('f16-seg6-%s-%s.json' % (MODE, EVIDENCE_VERSION), payload)
        print('STATUS: OK %s FAIL=0 committed=%s' % (MODE.upper(), committed))
    except Exception as error:
        if owned_open:
            try:
                currentProgram.endTransaction(tx, False)
                owned_open = False
                progress['txn_after_own'] = transaction_info_row()
                progress['txn_after_own_end'] = progress['txn_after_own']
                verify_prestate(pre, True)
                progress['rollback_after_capture_pass'] = True
            except Exception:
                progress['rollback_after_capture_pass'] = False
                progress['rollback_restore_error'] = traceback.format_exc()
        write_json('f16-seg6-%s-failure-%s.json' % (MODE, EVIDENCE_VERSION),
                   failure_payload(stage, error, progress))
        print(traceback.format_exc())
        raise
elif MODE == 'check':
    pre = read_json(PRESTATE_NAME)
    plan = read_json(PLAN_NAME)
    verify_plan(plan, file_hash(os.path.join(RUN, PRESTATE_NAME)))
    save_authorization = validate_check_authorization(SAVE_GRANT_SHA_ARG)
    apply_receipt = save_authorization['apply_receipt']
    require(apply_receipt.get('status') == 'PASS' and
            apply_receipt.get('transaction_committed') is True and
            apply_receipt.get('post_verified') is True,
            'CHECK_APPLY_RECEIPT')
    exact('CHECK_APPLY_BINDINGS',
          dict((key, apply_receipt.get(key))
               for key in receipt_bindings(save_authorization)),
          receipt_bindings(save_authorization))
    reject('CHECK_BINDINGS')
    verify_post(pre)
    payload = {
        'status': 'PASS', 'mode': MODE, 'FAIL': 0,
        'semantic_actions_applied': False, 'post_verified': True,
    }
    payload.update(receipt_bindings(save_authorization))
    write_json('f16-seg6-persisted-check-%s.json' % EVIDENCE_VERSION, payload)
    print('STATUS: OK CHECK FAIL=0')




