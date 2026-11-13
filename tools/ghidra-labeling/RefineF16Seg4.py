# -*- coding: ascii -*-
#@runtime Jython
#@category Ygo-ex2006.Refine
# F16-Seg-4 approved materialization. Phase1 uses prestate/dry/fullrollback only.

import csv
from collections import defaultdict, Counter
import hashlib
import json
import os
import traceback
import re
from java.math import BigInteger
from ghidra.program.model.address import AddressSet
from ghidra.program.model.data import Undefined4DataType
from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.listing import FlowOverride

from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import RefType, SourceType


csv.field_size_limit(2**27)


ARGS = list(getScriptArgs())
MODE = ARGS[0].lower() if ARGS else 'dry'
if MODE not in ('prestate', 'dry', 'fullrollback', 'apply', 'check'):
    raise RuntimeError('Expected prestate, dry, fullrollback, apply, or check')
if MODE in ('apply', 'check'):
    if len(ARGS) != 2:
        raise RuntimeError('Apply/check require explicit Root grant SHA256 argument')
    SAVE_GRANT_SHA_ARG = ARGS[1]
else:
    if len(ARGS) > 1:
        raise RuntimeError('Save grant is forbidden outside apply/check')
    SAVE_GRANT_SHA_ARG = None

ROOT = os.path.abspath(os.path.join(str(getSourceFile().getParentFile()), '..', '..'))
RUN = os.path.join(ROOT, 'output', 'refine-run-20261028-105948')
EVIDENCE_VERSION = 'v1'
PLAN_NAME = 'f16-seg4-plan-v1.json'
PRESTATE_NAME = 'f16-seg4-fresh-full-prestate-v1.json'
SNAPSHOT_NAME = 'f16-seg4-source-snapshot-preapply-v1.json'
FRESH_PROOF_NAME = 'f16-seg4-fresh-canonical-proof-v1.json'
AUTH_CONTRACT_NAME = 'f16-seg4-once-save-contract-v1.json'
AUTH_CONTRACT_SHA256 = '95fd8e4ea547bd719ae318122a103f7a90a1fd6dfa5673128098a35e35568065'
GRANT_NAME = 'root-f16-seg4-implementation-gate.json'
ROOT_ATTEMPT_NAME = 'f16-seg4-apply-once-v1.json'
SCRIPT_CLAIM_NAME = 'f16-seg4-script-apply-claim-v1.json'
APPLY_RECEIPT_NAME = 'f16-seg4-apply-v1.json'
PHASE1A_MANIFEST_NAME = 'f16-seg4-phase1a-manifest-v1.json'
PHASE1_MANIFEST_NAME = 'f16-seg4-phase1-manifest-v1.json'
PHASE1_AUDIT_NAME = 'f16-seg4-phase1-static-review-v1.json'
INPUT_HASHES = {'doc/dev/refine/F16-Seg-4.plates.tsv': '8daaa420bf56dfde2ecd5879988a82f38619a3b15663aebbd15de9807c2da982', 'doc/dev/refine/F16-Seg-4.proposal.md': 'cfdf43e9a2c60502834470cbe91a5232e4635cf78f1f60361a8b78286114afe2', 'doc/dev/refine/F16-Seg-4.review.md': '13d7c73647ecf9ae435b6836d69bbacc6c4f556298db7f46721ea9d7f3d16060', 'doc/dev/refine/F16-Seg-4.slots.tsv': 'bf738dae36ca542cb078b1bd1a8bb91131fd70ee036aaf7e304a07c6269abbcc', 'output/refine-run-20261028-105948/f15-readonly-scripts/F16Seg4GlobalDynamicSymbolIdsQuery.java': '0c6cdd7ea2681c1a891d5a490ad7eef23c2bd3914032421c324aa31c729b7f04', 'output/refine-run-20261028-105948/f15-readonly-scripts/F16Seg4GlobalStaticSymbolIdsQuery.java': 'f958b9ff172fb7fba5374916c2ddd23c9db349a203debd08d109b8c80c4f44a8', 'output/refine-run-20261028-105948/f16-seg1-analysis-validator-v2.py': '5472177d1856c01db0f2b1fd6cce08bd9e0fb69d289bdb725ad053b3b42da768', 'output/refine-run-20261028-105948/f16-seg3-source-landing-pins-v2.json': '8ca88f1e34a89bfa52f1f3a71f8b97696abc2606ea200dabf3cc6e776108c0f7', 'output/refine-run-20261028-105948/f16-seg4-all-id-validator-v3.py': '9913dcef8a3d2c90d52d99a6a5c6313ab42b08418589e0f091b99c253c2da301', 'output/refine-run-20261028-105948/f16-seg4-analysis-manifest-v2.json': '6c318fb55436d6fab3bc89d12e2d7c9eb3d099114b8df8a07abbc5e5b375dc21', 'output/refine-run-20261028-105948/f16-seg4-analysis-manifest-v3.json': '09dda96f7b00f5d0117d4ecc32543b73e26c25b0136afffd302a49f53146cea5', 'output/refine-run-20261028-105948/f16-seg4-analysis-source-v2.json': '549f061903717124d2a8a9d7210d39e6de8c6adb5ed526da63c5c8cef441e7e6', 'output/refine-run-20261028-105948/f16-seg4-analysis-source-v3.json': '31d3493e031410a7af1a2ae1a2a9dc319d88fda5edf23e599c7de2f7e90cd0fd', 'output/refine-run-20261028-105948/f16-seg4-auto-reference-source-audit-v1.json': '939b4c5c90c9c3a3b6c93d23047777dc8154bcefab0a54f22f424a16a633f938', 'output/refine-run-20261028-105948/f16-seg4-automatic-reference-rules-review-v1.json': '8d168a2a4219a0965d699e86cf334cedb23e90c56be99c171fb912e179152347', 'output/refine-run-20261028-105948/f16-seg4-decisions-v1.json': 'f002f0abe1c2182f61fc739a22719b49ecc74463ddf8f48eb0ea5643482dfb48', 'output/refine-run-20261028-105948/f16-seg4-execute-mode-a-v3.py': 'da9307776a2b2ebdd1c9bebed73dd7a7197f95a6bb35e01223ac12c1fdb439c6', 'output/refine-run-20261028-105948/f16-seg4-existing-gnu-value-scan-v1.json': '2d51a523b190de40b6b68120666fb5a0aa8b550fc4b04a86bf056bdae08f46f9', 'output/refine-run-20261028-105948/f16-seg4-full-function-observation-plan-v1.json': 'db60281eca1852ac6787e93449ad2fa96cc598b433202b98116477fedf334ffe', 'output/refine-run-20261028-105948/f16-seg4-full-raw-thumb-refscan-v2.json': '9dd3610069c6931e6ba977418e616d3dd975c5abe3f6af54a61f503565812544', 'output/refine-run-20261028-105948/f16-seg4-full-rom-refscan-v1.json': 'dff4f3f34b6f054742f1e27ce640ebc7c4069c26a172bb7e334f157ed2752d05', 'output/refine-run-20261028-105948/f16-seg4-fullstate-observation-plan-v1.json': 'e61be63180c86812463dc1181c747aab326210c27c6b45384a38bfbf9d2754b8', 'output/refine-run-20261028-105948/f16-seg4-function-plan-v1.json': '5383b6b0366255a9e81d4dda141ea96fbb511f4dba54834ddffd14b2c33499cd', 'output/refine-run-20261028-105948/f16-seg4-gas-projections-v1.json': 'd316a8e15252efc38288dfe045c1b1f730177f75bbf2e512246914b003dd1b92', 'output/refine-run-20261028-105948/f16-seg4-global-equates-plan-v1.json': '9a6a8bb2be8baffe799ba1519eaadd0a3fe859489f9dfa52e1dca2e374e6ddc3', 'output/refine-run-20261028-105948/f16-seg4-initial-raw-refscan-disasm-v1.json': 'e07af7ebfd6b1a25f729bfeadcc12b593c3b6f274d5f803ed4002ef825f277be', 'output/refine-run-20261028-105948/f16-seg4-inputs-v3.json': '123b68bf21951905985c22a57a59a31978a8317c17215b287aab9348a33ffe3c', 'output/refine-run-20261028-105948/f16-seg4-inputs-v4.json': '3ff67b50c6dc6785f2e337ab12432d4a287f42e78bfbe30d7d045d5043509b83', 'output/refine-run-20261028-105948/f16-seg4-instruction-properties-plan-v1.json': '1a9458fc098e13508b683a00d1818d133f3fad98149b17d82dc1083bdf68cd11', 'output/refine-run-20261028-105948/f16-seg4-label-closure-plan-v1.json': '934399fc6370edcb609aa8c501e6f1b0e9e86aa68bc1dbcf27c424e8a5387611', 'output/refine-run-20261028-105948/f16-seg4-mode-a-build-v3.py': '914915e03acb1fdb296b3fda97d746cd2553f6ac244370e8498d8239b6c22dc5', 'output/refine-run-20261028-105948/f16-seg4-mode-a-execution-v3.log': 'ee976ea62135f4478ccfaf50a730ecb2141944b062fc4641f192c0ecaeed9639', 'output/refine-run-20261028-105948/f16-seg4-mode-a-freeze-v3.py': 'e32f613be9376854f37ba515141d10588f51dc03b0e279359a5efa3a8af693b1', 'output/refine-run-20261028-105948/f16-seg4-mode-a-original-review-v2.md': '679c84c53d258b499cf060369e7eab33c2572ed55be54f5f92d637531c4633d9', 'output/refine-run-20261028-105948/f16-seg4-mode-a-proposal-binding-v3.json': '82e9abc3dcd827736a1e7f6d813edce05ef049e70a78a5d8b2728722173baa1b', 'output/refine-run-20261028-105948/f16-seg4-name-reference-baseline-v1.json': 'c19cb34cfbf893d41c03dba4fe63d5ba58e9dd9599d67d0f50516fdf65e9c069', 'output/refine-run-20261028-105948/f16-seg4-native-instruction-projection-v1.json': 'acc9686377a2574743b7ddbcdc0ec85ca8f85795257d7e3ddfadf93cf16825ce', 'output/refine-run-20261028-105948/f16-seg4-native-module-metadata-plan-v1.json': '60689e170a7a79a3e1384480d1d92d87fbc8a2af70f6db6b62afa05c1ba3a1cd', 'output/refine-run-20261028-105948/f16-seg4-native-query-full-observation-plan-v1.json': '48745aa13cfc7efc285897fc05fcb231bce91fe1e459e35d12f4312eb0b40fd8', 'output/refine-run-20261028-105948/f16-seg4-native-resolver-execution-v1.json': 'a9d65ca535e98c8c92a230b516629b47a923cd42df7cec576ddacabb0851045e', 'output/refine-run-20261028-105948/f16-seg4-negative-execution-v1.json': '2c89ab514e0f0c7e4b31395df950d5fb6dc9d0950a01cc9e911c9b3923a8f555', 'output/refine-run-20261028-105948/f16-seg4-negative-execution-v2.json': '8125f07266ab09ea4dbb2cdf1d619800f8e9d3393194d3f630bc355d4d1bb3bd', 'output/refine-run-20261028-105948/f16-seg4-negative-execution-v3.json': 'daccd7d3436c28e3f2ac0b122b1fa6a552c83dbf9707f9f96b188b48fc618049', 'output/refine-run-20261028-105948/f16-seg4-negative-suite-v3.py': '4328e23ee93df5f0ebdc440cc36910394b09990391374f51272fd6426dfd7e8b', 'output/refine-run-20261028-105948/f16-seg4-plates-draft-v1.tsv': '8daaa420bf56dfde2ecd5879988a82f38619a3b15663aebbd15de9807c2da982', 'output/refine-run-20261028-105948/f16-seg4-primary-symbol-plan-v1.json': 'ec7a1c65a430a13c2b82bbe8c2510b8e08868d42bb287e28f07b1413270a5e61', 'output/refine-run-20261028-105948/f16-seg4-primitives-draft-v1.json': '77d4ed8c9700c12b00e7b45153db095f7df8ca9ea35d67dbe44c1c3720f5bcaa', 'output/refine-run-20261028-105948/f16-seg4-proposal-draft-v1.md': 'cfdf43e9a2c60502834470cbe91a5232e4635cf78f1f60361a8b78286114afe2', 'output/refine-run-20261028-105948/f16-seg4-r4-plan-v1.json': 'ecd3cd4f6f9193aec4aecd94ab028c2eadc90d7b5198855084c5c315495a961f', 'output/refine-run-20261028-105948/f16-seg4-registry-plan-v1.json': 'beaa2523a9ab53336b57a51d03d92f326a82e359b78244c78ffc0990e4b44f20', 'output/refine-run-20261028-105948/f16-seg4-replay-execution-v3.json': '80b392caf528950ec67e7faaead0ad4db3d8f3848cbb99085e9fe41b69eb1392', 'output/refine-run-20261028-105948/f16-seg4-reviewer-R2-virtual-boundary-v1.json': '553c40fe079e60dbe275cbba1280b6817ebf484ba487075d87b820281b768c75', 'output/refine-run-20261028-105948/f16-seg4-reviewer-audit-v2.json': '9a6a376c1cb409ca960d14af78d411095114d955067dbcdfa64dba0fba63d5d5', 'output/refine-run-20261028-105948/f16-seg4-reviewer-audit-v3.json': '69f0b5d24b77be646485d9056823175fc6dbad49e9ff3305a544bf20c12266ac', 'output/refine-run-20261028-105948/f16-seg4-runner-source-v3.py': 'cfeaba067ee8c7fd258e7c5977e78efcfe12bfa5f13037eb97124d88142f8376', 'output/refine-run-20261028-105948/f16-seg4-semantic-plan-v1.json': 'c09a3850afba74b7c30c68a25304e1c4c7ab0ad8ae6b0f0a019968650bcc92f7', 'output/refine-run-20261028-105948/f16-seg4-slot-plan-v1.json': '454085ad87ac9bcef573ba7101535a4ddd20c10c7cb216b17e5c85bbd9e65959', 'output/refine-run-20261028-105948/f16-seg4-slots-draft-v1.tsv': 'bf738dae36ca542cb078b1bd1a8bb91131fd70ee036aaf7e304a07c6269abbcc', 'output/refine-run-20261028-105948/f16-seg4-source-cfg-map-v2.json': '93b4c9395b5fba1ea91afcaecf56908f08b65e2a9fd6bdc73d255c654a36b164', 'output/refine-run-20261028-105948/f16-seg4-source-scope-plan-v1.json': 'ce9ff5496ed173c51188c396c585dfe520b739ad0efd26e1079bb4def9c6e8bb', 'output/refine-run-20261028-105948/f16-seg4-target-plan-v1.json': '3859f3a43c11143f21122aa5cf334d4b3808917d802e2e54a2c84c92562fa09f', 'output/refine-run-20261028-105948/root-f15-seg6-transaction-mechanism.json': '908138c1819efa2dc2df669a76926d4d8d9934f479829801b01d9d7038356480', 'output/refine-run-20261028-105948/root-f16-seg4-all-ID-before-gate-v1.json': '172821f6cf32676dafaf1cb3cf58260f9fd0fda6e83e0f8fd8c7caeae531b5d9', 'output/refine-run-20261028-105948/root-f16-seg4-all-dynamic-symbol-IDs-before-v1.json': '14d298e21ffbcb7bce635795623d93ddb9b3caeaa77167bc1b65b3e021f14981', 'output/refine-run-20261028-105948/root-f16-seg4-all-dynamic-symbol-IDs-before-v1.json.db-gate.json': '94612dac4b3a24e0781f2e59feb8958960f3b163ce3b3dd7742267d5a2275d5c', 'output/refine-run-20261028-105948/root-f16-seg4-all-static-symbol-IDs-before-v1.json': 'c2f09acc1e65d680d90dd855c28df54cd8da528d3d6eaf8ae609962b9199ea73', 'output/refine-run-20261028-105948/root-f16-seg4-all-static-symbol-IDs-before-v1.json.db-gate.json': '94612dac4b3a24e0781f2e59feb8958960f3b163ce3b3dd7742267d5a2275d5c', 'output/refine-run-20261028-105948/root-f16-seg4-db-backup.json': '1b6f73e2a53f23f5f5419c712009c4616dfac6a3616bcc87cfc93171efd12ffe', 'output/refine-run-20261028-105948/root-f16-seg4-independent-prestate-v5.json': 'a09a962479de938b7d49c8c38e530c628b950aa81101f9a81e6d511cf23e8471', 'output/refine-run-20261028-105948/root-f16-seg4-instruction-properties-before-v2.json': 'b25464fb336821b5fd6337cb1268b23f446c5a2866b4803606ca017668d84714', 'output/refine-run-20261028-105948/root-f16-seg4-instruction-slot-input-v1.json': '53ea1a8e073fa7b00dddc7637527324ab98e09e96c4afe8de7d6ce413342eca2', 'output/refine-run-20261028-105948/root-f16-seg4-native-before-complete-v1.json': '09f599499634aa33212a8d6e3cdde0c278b7ab9db739b9c510a865f6cbdac201', 'output/refine-run-20261028-105948/root-f16-seg4-prospective-target-IDs-before-v1.json': 'f4118070dae3eb207a0b239d375955c247decc8ff7468e175ac09c00d75bf358', 'output/refine-run-20261028-105948/root-f16-seg4-pseudo-decode-v3.json': 'd7452233514fc70e588947690db58cca6c2ded8a39d87003a8945d5ae1c87ee0', 'output/refine-run-20261028-105948/root-f16-seg4-static-ID-before-gate-v1.json': 'b309f9399bfc2ef4b39091d7c4a8d7c70f6766f3a5cec2a2ce27bb1bb65dd5f9', 'output/refine-run-20261028-105948/root-f16-seg4-typed-label-closure-before-v3.json': '9fa2c3c8d868c6530b37f237f922ea9efcbbf4de14d2fea8785df787c5bc9683', 'output/refine-run-20261028-105948/root-source-baseline-f16seg4.json': '9c5bb82e1e206bc50b04bd3f864d4436c4c3d86ce94fc24301e8b80019c24f03', 'tools/asm-regen/ghidra/ExportRangeToGas.py': '4544a6a95f922f5a1779553555180ed2184955bc4fc1e92f96ad9b500ddaeb87'}
AUXILIARY_INPUTS = ('f15-readonly-scripts/F16Seg4GlobalDynamicSymbolIdsQuery.java', 'f15-readonly-scripts/F16Seg4GlobalStaticSymbolIdsQuery.java', 'f16-seg1-analysis-validator-v2.py', 'f16-seg3-source-landing-pins-v2.json', 'f16-seg4-all-id-validator-v3.py', 'f16-seg4-analysis-manifest-v2.json', 'f16-seg4-analysis-manifest-v3.json', 'f16-seg4-analysis-source-v2.json', 'f16-seg4-analysis-source-v3.json', 'f16-seg4-auto-reference-source-audit-v1.json', 'f16-seg4-automatic-reference-rules-review-v1.json', 'f16-seg4-decisions-v1.json', 'f16-seg4-execute-mode-a-v3.py', 'f16-seg4-existing-gnu-value-scan-v1.json', 'f16-seg4-full-function-observation-plan-v1.json', 'f16-seg4-full-raw-thumb-refscan-v2.json', 'f16-seg4-full-rom-refscan-v1.json', 'f16-seg4-fullstate-observation-plan-v1.json', 'f16-seg4-function-plan-v1.json', 'f16-seg4-gas-projections-v1.json', 'f16-seg4-global-equates-plan-v1.json', 'f16-seg4-initial-raw-refscan-disasm-v1.json', 'f16-seg4-inputs-v3.json', 'f16-seg4-inputs-v4.json', 'f16-seg4-instruction-properties-plan-v1.json', 'f16-seg4-label-closure-plan-v1.json', 'f16-seg4-mode-a-build-v3.py', 'f16-seg4-mode-a-execution-v3.log', 'f16-seg4-mode-a-freeze-v3.py', 'f16-seg4-mode-a-original-review-v2.md', 'f16-seg4-mode-a-proposal-binding-v3.json', 'f16-seg4-name-reference-baseline-v1.json', 'f16-seg4-native-instruction-projection-v1.json', 'f16-seg4-native-module-metadata-plan-v1.json', 'f16-seg4-native-query-full-observation-plan-v1.json', 'f16-seg4-native-resolver-execution-v1.json', 'f16-seg4-negative-execution-v1.json', 'f16-seg4-negative-execution-v2.json', 'f16-seg4-negative-execution-v3.json', 'f16-seg4-negative-suite-v3.py', 'f16-seg4-plates-draft-v1.tsv', 'f16-seg4-primary-symbol-plan-v1.json', 'f16-seg4-primitives-draft-v1.json', 'f16-seg4-proposal-draft-v1.md', 'f16-seg4-r4-plan-v1.json', 'f16-seg4-registry-plan-v1.json', 'f16-seg4-replay-execution-v3.json', 'f16-seg4-reviewer-R2-virtual-boundary-v1.json', 'f16-seg4-reviewer-audit-v2.json', 'f16-seg4-reviewer-audit-v3.json', 'f16-seg4-runner-source-v3.py', 'f16-seg4-semantic-plan-v1.json', 'f16-seg4-slot-plan-v1.json', 'f16-seg4-slots-draft-v1.tsv', 'f16-seg4-source-cfg-map-v2.json', 'f16-seg4-source-scope-plan-v1.json', 'f16-seg4-target-plan-v1.json', 'root-f15-seg6-transaction-mechanism.json', 'root-f16-seg4-all-ID-before-gate-v1.json', 'root-f16-seg4-all-dynamic-symbol-IDs-before-v1.json', 'root-f16-seg4-all-dynamic-symbol-IDs-before-v1.json.db-gate.json', 'root-f16-seg4-all-static-symbol-IDs-before-v1.json', 'root-f16-seg4-all-static-symbol-IDs-before-v1.json.db-gate.json', 'root-f16-seg4-db-backup.json', 'root-f16-seg4-independent-prestate-v5.json', 'root-f16-seg4-instruction-properties-before-v2.json', 'root-f16-seg4-instruction-slot-input-v1.json', 'root-f16-seg4-native-before-complete-v1.json', 'root-f16-seg4-prospective-target-IDs-before-v1.json', 'root-f16-seg4-pseudo-decode-v3.json', 'root-f16-seg4-static-ID-before-gate-v1.json', 'root-f16-seg4-typed-label-closure-before-v3.json', 'root-source-baseline-f16seg4.json')
EXPECTED_COUNTS = {'EQ_ADD': 27, 'REF_ADD': 80, 'REF_PRESERVE': 13, 'CASE_VECTOR_PRESERVE_CORE': 83, 'SOURCE_LABEL': 120, 'SOURCE_EOL': 122, 'TARGET_LABEL': 73, 'DATA_REF_ADD': 80, 'FUNCTION_RENAME': 3, 'PLATE': 9, 'R4_TMODE_BYTES': 1838, 'R4_DATA': 64, 'R4_CODE': 884, 'R4_BODY': 1, 'R4_CALL_RETURN': 2}
SEGMENT_START = 135021392
SEGMENT_END = 135026628
MODULE_START = 0x080c1448
MODULE_END = 0x080cbf0c

CONTRACT_COUNTS = {'analysis_input_records': 26, 'producer_outputs': 24, 'functions': 141, 'states': 4876, 'slot_holders': 4440, 'module_words': 1644, 'target_states': 508, 'units': 43716, 'external_units': 48, 'instruction_properties': 22359, 'label_closure_rows': 2618, 'closure_seeds': 2190, 'label_closure_incoming_before': 270, 'label_closure_incoming_after': 443, 'baseline_files': 207, 'snapshot_files': 212, 'before_static_ids': 35732, 'before_dynamic_ids': 48116, 'before_all_ids': 83848, 'new_USER_ids': 193, 'global_before': 2488, 'global_after': 2494, 'bindings_before': 12739, 'bindings_after': 12766}

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
    atomic_write_claim(name, value)

def file_hash(path):
    with open(path, 'rb') as stream:
        return hashlib.sha256(stream.read()).hexdigest()

def is_lower_hex64(value):
    return (isinstance(value, basestring) and len(value) == 64 and
            all(char in '0123456789abcdef' for char in value))

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
            'output/refine-run-20261028-105948/f16-seg4-analysis-manifest-v3.json'],
        'analysis_review_sha256': INPUT_HASHES['doc/dev/refine/F16-Seg-4.review.md'],
        'canonical_sha256': file_hash(require_file(
            'root-f16-seg4-independent-prestate-v5.json',
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
        'schema': 'F16_SEG4_ROOT_ONCE_SAVE_GATE_V2',
        'status': 'ROOT_F16_SEG4_IMPLEMENTATION_GATE_PASS',
        'segment': 'F16-Seg-4',
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
            'F16_SEG4_PHASE1_%s_COMPLETE' % EVIDENCE_VERSION.upper() or
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
        'segment': 'F16-Seg-4',
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
        'segment': 'F16-Seg-4',
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
        write_json('f16-seg4-%s-failures-%s.json' % (MODE, EVIDENCE_VERSION), {
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
# Pure plan initializers end at typed_atom; no native getter is called here.
RAW_SLOT_ROWS = read_tsv('doc/dev/refine/F16-Seg-4.slots.tsv')
RAW_PLATE_ROWS = read_tsv('doc/dev/refine/F16-Seg-4.plates.tsv')
SLOT_PLAN = read_json('f16-seg4-slot-plan-v1.json')
FUNCTION_PLAN = read_json('f16-seg4-function-plan-v1.json')
FULL_NATIVE_PLAN = read_json('f16-seg4-native-query-full-observation-plan-v1.json')
ROOT_FULL_PRESTATE = FULL_NATIVE_PLAN['before']
NATIVE_AFTER = FULL_NATIVE_PLAN['after']
PROPERTIES_BEFORE = read_json('root-f16-seg4-instruction-properties-before-v2.json')
PROPERTY_PLAN = read_json('f16-seg4-instruction-properties-plan-v1.json')
LABEL_CLOSURE_PLAN = read_json('f16-seg4-label-closure-plan-v1.json')
LABEL_CLOSURE_BEFORE = LABEL_CLOSURE_PLAN['before']
R4_PLAN = read_json('f16-seg4-r4-plan-v1.json')
PRIMITIVES = read_json('f16-seg4-primitives-draft-v1.json')
STATIC_ID_BEFORE = read_json('root-f16-seg4-all-static-symbol-IDs-before-v1.json')
ALL_ID_BEFORE = read_json('root-f16-seg4-all-dynamic-symbol-IDs-before-v1.json')
ALL_BEFORE_IDS = set(ALL_ID_BEFORE['static_ids']) | set(row['id'] for row in ALL_ID_BEFORE['dynamic_rows'])
WORD_REQUESTS = [row['source'] for row in ROOT_FULL_PRESTATE['words']]
SLOT_REQUESTS = [row['source'] for row in ROOT_FULL_PRESTATE['slots']]
OBSERVER_FUNCTIONS = [int(row['entry'], 16) for row in ROOT_FULL_PRESTATE['functions']]
PROPERTY_REQUEST_ADDRESSES = [int(row['address'], 16) for row in read_json('root-f16-seg4-instruction-slot-input-v1.json')]
CLOSURE_SEEDS = LABEL_CLOSURE_BEFORE['seed_requests']
EXTERNAL_ALIAS_NAMES = sorted(ROOT_FULL_PRESTATE['external_equate_aliases'])
PENALTY_EQUATE_NAMES = sorted(ROOT_FULL_PRESTATE['penalty_equates'])
SEGMENT_EQUATE_NAMES = sorted(ROOT_FULL_PRESTATE['segment_equates'])
R4_HEADS = set(int(row['after']['address'], 16) for row in R4_PLAN['new_instruction_rows'])
CODE_RANGES = [pair for block in R4_PLAN['raw_blocks'] for pair in block['code_ranges']]
CODE_BYTES = set(value for lo, hi in CODE_RANGES for value in range(int(lo, 16), int(hi, 16)))
STATE_CONTRACTS = dict((int(row['address'], 16), row) for row in read_json('f16-seg4-fullstate-observation-plan-v1.json')['rows'])
SLOT_ROWS = [{'address': row['address'], 'action': row['action'], 'old_value': row['value'],
              'final_data_type': row['after']['data_at']['type'], 'final_eol': row['after']['eol']} for row in SLOT_PLAN['rows']]
SLOTS = dict((int(row['address'], 16), row) for row in SLOT_ROWS)
SLOT_CONTRACTS = dict((int(row['address'], 16), row) for row in SLOT_PLAN['rows'])
SOURCE_LABEL_ADDRESSES = set(value for value, row in SLOT_CONTRACTS.items() if row['action'] != 'CASE_VECTOR_PRESERVE_CORE')
TARGET_MATERIALIZATIONS = set(int(address, 16) for address in PRIMITIVES['labels']) - SOURCE_LABEL_ADDRESSES
TARGET_CONTRACTS = dict((value, STATE_CONTRACTS[value]) for value in TARGET_MATERIALIZATIONS)
RENAMED_FUNCTIONS = dict((int(row['entry'], 16), row) for row in FUNCTION_PLAN['rows'] if row['before']['name'] != row['after']['name'])
FUNCTION_CONTRACTS = dict((int(row['entry'], 16), dict(row, action='RENAME_PLATE' if row['before']['name'] != row['after']['name'] else 'PLATE')) for row in FUNCTION_PLAN['rows'])
PLATES = dict((value, {'address': row['entry'], 'old_name': row['before']['name'], 'new_name': row['after']['name'],
                       'old_plate': row['before']['plate'], 'new_plate': row['after']['plate'], 'action': 'FULL_REWRITE'}) for value, row in FUNCTION_CONTRACTS.items())
INSTRUCTION_EOLS = dict((int(address, 16), text) for address, text in PRIMITIVES['instruction_eol'].items())
ALL_EQUATE_NAMES = sorted(set(ROOT_FULL_PRESTATE['global_equates']) | set(NATIVE_AFTER['global_equates']))
EQUATE_NAMES = sorted(set(row['after']['equate_references'][0]['name'] for row in SLOT_PLAN['rows'] if row['action'] == 'EQ_ADD'))


PLAN_STATIC = {'input_hashes': {'doc/dev/refine/F16-Seg-4.plates.tsv': '8daaa420bf56dfde2ecd5879988a82f38619a3b15663aebbd15de9807c2da982', 'doc/dev/refine/F16-Seg-4.proposal.md': 'cfdf43e9a2c60502834470cbe91a5232e4635cf78f1f60361a8b78286114afe2', 'doc/dev/refine/F16-Seg-4.review.md': '13d7c73647ecf9ae435b6836d69bbacc6c4f556298db7f46721ea9d7f3d16060', 'doc/dev/refine/F16-Seg-4.slots.tsv': 'bf738dae36ca542cb078b1bd1a8bb91131fd70ee036aaf7e304a07c6269abbcc', 'output/refine-run-20261028-105948/f15-readonly-scripts/F16Seg4GlobalDynamicSymbolIdsQuery.java': '0c6cdd7ea2681c1a891d5a490ad7eef23c2bd3914032421c324aa31c729b7f04', 'output/refine-run-20261028-105948/f15-readonly-scripts/F16Seg4GlobalStaticSymbolIdsQuery.java': 'f958b9ff172fb7fba5374916c2ddd23c9db349a203debd08d109b8c80c4f44a8', 'output/refine-run-20261028-105948/f16-seg1-analysis-validator-v2.py': '5472177d1856c01db0f2b1fd6cce08bd9e0fb69d289bdb725ad053b3b42da768', 'output/refine-run-20261028-105948/f16-seg3-source-landing-pins-v2.json': '8ca88f1e34a89bfa52f1f3a71f8b97696abc2606ea200dabf3cc6e776108c0f7', 'output/refine-run-20261028-105948/f16-seg4-all-id-validator-v3.py': '9913dcef8a3d2c90d52d99a6a5c6313ab42b08418589e0f091b99c253c2da301', 'output/refine-run-20261028-105948/f16-seg4-analysis-manifest-v2.json': '6c318fb55436d6fab3bc89d12e2d7c9eb3d099114b8df8a07abbc5e5b375dc21', 'output/refine-run-20261028-105948/f16-seg4-analysis-manifest-v3.json': '09dda96f7b00f5d0117d4ecc32543b73e26c25b0136afffd302a49f53146cea5', 'output/refine-run-20261028-105948/f16-seg4-analysis-source-v2.json': '549f061903717124d2a8a9d7210d39e6de8c6adb5ed526da63c5c8cef441e7e6', 'output/refine-run-20261028-105948/f16-seg4-analysis-source-v3.json': '31d3493e031410a7af1a2ae1a2a9dc319d88fda5edf23e599c7de2f7e90cd0fd', 'output/refine-run-20261028-105948/f16-seg4-auto-reference-source-audit-v1.json': '939b4c5c90c9c3a3b6c93d23047777dc8154bcefab0a54f22f424a16a633f938', 'output/refine-run-20261028-105948/f16-seg4-automatic-reference-rules-review-v1.json': '8d168a2a4219a0965d699e86cf334cedb23e90c56be99c171fb912e179152347', 'output/refine-run-20261028-105948/f16-seg4-decisions-v1.json': 'f002f0abe1c2182f61fc739a22719b49ecc74463ddf8f48eb0ea5643482dfb48', 'output/refine-run-20261028-105948/f16-seg4-execute-mode-a-v3.py': 'da9307776a2b2ebdd1c9bebed73dd7a7197f95a6bb35e01223ac12c1fdb439c6', 'output/refine-run-20261028-105948/f16-seg4-existing-gnu-value-scan-v1.json': '2d51a523b190de40b6b68120666fb5a0aa8b550fc4b04a86bf056bdae08f46f9', 'output/refine-run-20261028-105948/f16-seg4-full-function-observation-plan-v1.json': 'db60281eca1852ac6787e93449ad2fa96cc598b433202b98116477fedf334ffe', 'output/refine-run-20261028-105948/f16-seg4-full-raw-thumb-refscan-v2.json': '9dd3610069c6931e6ba977418e616d3dd975c5abe3f6af54a61f503565812544', 'output/refine-run-20261028-105948/f16-seg4-full-rom-refscan-v1.json': 'dff4f3f34b6f054742f1e27ce640ebc7c4069c26a172bb7e334f157ed2752d05', 'output/refine-run-20261028-105948/f16-seg4-fullstate-observation-plan-v1.json': 'e61be63180c86812463dc1181c747aab326210c27c6b45384a38bfbf9d2754b8', 'output/refine-run-20261028-105948/f16-seg4-function-plan-v1.json': '5383b6b0366255a9e81d4dda141ea96fbb511f4dba54834ddffd14b2c33499cd', 'output/refine-run-20261028-105948/f16-seg4-gas-projections-v1.json': 'd316a8e15252efc38288dfe045c1b1f730177f75bbf2e512246914b003dd1b92', 'output/refine-run-20261028-105948/f16-seg4-global-equates-plan-v1.json': '9a6a8bb2be8baffe799ba1519eaadd0a3fe859489f9dfa52e1dca2e374e6ddc3', 'output/refine-run-20261028-105948/f16-seg4-initial-raw-refscan-disasm-v1.json': 'e07af7ebfd6b1a25f729bfeadcc12b593c3b6f274d5f803ed4002ef825f277be', 'output/refine-run-20261028-105948/f16-seg4-inputs-v3.json': '123b68bf21951905985c22a57a59a31978a8317c17215b287aab9348a33ffe3c', 'output/refine-run-20261028-105948/f16-seg4-inputs-v4.json': '3ff67b50c6dc6785f2e337ab12432d4a287f42e78bfbe30d7d045d5043509b83', 'output/refine-run-20261028-105948/f16-seg4-instruction-properties-plan-v1.json': '1a9458fc098e13508b683a00d1818d133f3fad98149b17d82dc1083bdf68cd11', 'output/refine-run-20261028-105948/f16-seg4-label-closure-plan-v1.json': '934399fc6370edcb609aa8c501e6f1b0e9e86aa68bc1dbcf27c424e8a5387611', 'output/refine-run-20261028-105948/f16-seg4-mode-a-build-v3.py': '914915e03acb1fdb296b3fda97d746cd2553f6ac244370e8498d8239b6c22dc5', 'output/refine-run-20261028-105948/f16-seg4-mode-a-execution-v3.log': 'ee976ea62135f4478ccfaf50a730ecb2141944b062fc4641f192c0ecaeed9639', 'output/refine-run-20261028-105948/f16-seg4-mode-a-freeze-v3.py': 'e32f613be9376854f37ba515141d10588f51dc03b0e279359a5efa3a8af693b1', 'output/refine-run-20261028-105948/f16-seg4-mode-a-original-review-v2.md': '679c84c53d258b499cf060369e7eab33c2572ed55be54f5f92d637531c4633d9', 'output/refine-run-20261028-105948/f16-seg4-mode-a-proposal-binding-v3.json': '82e9abc3dcd827736a1e7f6d813edce05ef049e70a78a5d8b2728722173baa1b', 'output/refine-run-20261028-105948/f16-seg4-name-reference-baseline-v1.json': 'c19cb34cfbf893d41c03dba4fe63d5ba58e9dd9599d67d0f50516fdf65e9c069', 'output/refine-run-20261028-105948/f16-seg4-native-instruction-projection-v1.json': 'acc9686377a2574743b7ddbcdc0ec85ca8f85795257d7e3ddfadf93cf16825ce', 'output/refine-run-20261028-105948/f16-seg4-native-module-metadata-plan-v1.json': '60689e170a7a79a3e1384480d1d92d87fbc8a2af70f6db6b62afa05c1ba3a1cd', 'output/refine-run-20261028-105948/f16-seg4-native-query-full-observation-plan-v1.json': '48745aa13cfc7efc285897fc05fcb231bce91fe1e459e35d12f4312eb0b40fd8', 'output/refine-run-20261028-105948/f16-seg4-native-resolver-execution-v1.json': 'a9d65ca535e98c8c92a230b516629b47a923cd42df7cec576ddacabb0851045e', 'output/refine-run-20261028-105948/f16-seg4-negative-execution-v1.json': '2c89ab514e0f0c7e4b31395df950d5fb6dc9d0950a01cc9e911c9b3923a8f555', 'output/refine-run-20261028-105948/f16-seg4-negative-execution-v2.json': '8125f07266ab09ea4dbb2cdf1d619800f8e9d3393194d3f630bc355d4d1bb3bd', 'output/refine-run-20261028-105948/f16-seg4-negative-execution-v3.json': 'daccd7d3436c28e3f2ac0b122b1fa6a552c83dbf9707f9f96b188b48fc618049', 'output/refine-run-20261028-105948/f16-seg4-negative-suite-v3.py': '4328e23ee93df5f0ebdc440cc36910394b09990391374f51272fd6426dfd7e8b', 'output/refine-run-20261028-105948/f16-seg4-plates-draft-v1.tsv': '8daaa420bf56dfde2ecd5879988a82f38619a3b15663aebbd15de9807c2da982', 'output/refine-run-20261028-105948/f16-seg4-primary-symbol-plan-v1.json': 'ec7a1c65a430a13c2b82bbe8c2510b8e08868d42bb287e28f07b1413270a5e61', 'output/refine-run-20261028-105948/f16-seg4-primitives-draft-v1.json': '77d4ed8c9700c12b00e7b45153db095f7df8ca9ea35d67dbe44c1c3720f5bcaa', 'output/refine-run-20261028-105948/f16-seg4-proposal-draft-v1.md': 'cfdf43e9a2c60502834470cbe91a5232e4635cf78f1f60361a8b78286114afe2', 'output/refine-run-20261028-105948/f16-seg4-r4-plan-v1.json': 'ecd3cd4f6f9193aec4aecd94ab028c2eadc90d7b5198855084c5c315495a961f', 'output/refine-run-20261028-105948/f16-seg4-registry-plan-v1.json': 'beaa2523a9ab53336b57a51d03d92f326a82e359b78244c78ffc0990e4b44f20', 'output/refine-run-20261028-105948/f16-seg4-replay-execution-v3.json': '80b392caf528950ec67e7faaead0ad4db3d8f3848cbb99085e9fe41b69eb1392', 'output/refine-run-20261028-105948/f16-seg4-reviewer-R2-virtual-boundary-v1.json': '553c40fe079e60dbe275cbba1280b6817ebf484ba487075d87b820281b768c75', 'output/refine-run-20261028-105948/f16-seg4-reviewer-audit-v2.json': '9a6a376c1cb409ca960d14af78d411095114d955067dbcdfa64dba0fba63d5d5', 'output/refine-run-20261028-105948/f16-seg4-reviewer-audit-v3.json': '69f0b5d24b77be646485d9056823175fc6dbad49e9ff3305a544bf20c12266ac', 'output/refine-run-20261028-105948/f16-seg4-runner-source-v3.py': 'cfeaba067ee8c7fd258e7c5977e78efcfe12bfa5f13037eb97124d88142f8376', 'output/refine-run-20261028-105948/f16-seg4-semantic-plan-v1.json': 'c09a3850afba74b7c30c68a25304e1c4c7ab0ad8ae6b0f0a019968650bcc92f7', 'output/refine-run-20261028-105948/f16-seg4-slot-plan-v1.json': '454085ad87ac9bcef573ba7101535a4ddd20c10c7cb216b17e5c85bbd9e65959', 'output/refine-run-20261028-105948/f16-seg4-slots-draft-v1.tsv': 'bf738dae36ca542cb078b1bd1a8bb91131fd70ee036aaf7e304a07c6269abbcc', 'output/refine-run-20261028-105948/f16-seg4-source-cfg-map-v2.json': '93b4c9395b5fba1ea91afcaecf56908f08b65e2a9fd6bdc73d255c654a36b164', 'output/refine-run-20261028-105948/f16-seg4-source-scope-plan-v1.json': 'ce9ff5496ed173c51188c396c585dfe520b739ad0efd26e1079bb4def9c6e8bb', 'output/refine-run-20261028-105948/f16-seg4-target-plan-v1.json': '3859f3a43c11143f21122aa5cf334d4b3808917d802e2e54a2c84c92562fa09f', 'output/refine-run-20261028-105948/root-f15-seg6-transaction-mechanism.json': '908138c1819efa2dc2df669a76926d4d8d9934f479829801b01d9d7038356480', 'output/refine-run-20261028-105948/root-f16-seg4-all-ID-before-gate-v1.json': '172821f6cf32676dafaf1cb3cf58260f9fd0fda6e83e0f8fd8c7caeae531b5d9', 'output/refine-run-20261028-105948/root-f16-seg4-all-dynamic-symbol-IDs-before-v1.json': '14d298e21ffbcb7bce635795623d93ddb9b3caeaa77167bc1b65b3e021f14981', 'output/refine-run-20261028-105948/root-f16-seg4-all-dynamic-symbol-IDs-before-v1.json.db-gate.json': '94612dac4b3a24e0781f2e59feb8958960f3b163ce3b3dd7742267d5a2275d5c', 'output/refine-run-20261028-105948/root-f16-seg4-all-static-symbol-IDs-before-v1.json': 'c2f09acc1e65d680d90dd855c28df54cd8da528d3d6eaf8ae609962b9199ea73', 'output/refine-run-20261028-105948/root-f16-seg4-all-static-symbol-IDs-before-v1.json.db-gate.json': '94612dac4b3a24e0781f2e59feb8958960f3b163ce3b3dd7742267d5a2275d5c', 'output/refine-run-20261028-105948/root-f16-seg4-db-backup.json': '1b6f73e2a53f23f5f5419c712009c4616dfac6a3616bcc87cfc93171efd12ffe', 'output/refine-run-20261028-105948/root-f16-seg4-independent-prestate-v5.json': 'a09a962479de938b7d49c8c38e530c628b950aa81101f9a81e6d511cf23e8471', 'output/refine-run-20261028-105948/root-f16-seg4-instruction-properties-before-v2.json': 'b25464fb336821b5fd6337cb1268b23f446c5a2866b4803606ca017668d84714', 'output/refine-run-20261028-105948/root-f16-seg4-instruction-slot-input-v1.json': '53ea1a8e073fa7b00dddc7637527324ab98e09e96c4afe8de7d6ce413342eca2', 'output/refine-run-20261028-105948/root-f16-seg4-native-before-complete-v1.json': '09f599499634aa33212a8d6e3cdde0c278b7ab9db739b9c510a865f6cbdac201', 'output/refine-run-20261028-105948/root-f16-seg4-prospective-target-IDs-before-v1.json': 'f4118070dae3eb207a0b239d375955c247decc8ff7468e175ac09c00d75bf358', 'output/refine-run-20261028-105948/root-f16-seg4-pseudo-decode-v3.json': 'd7452233514fc70e588947690db58cca6c2ded8a39d87003a8945d5ae1c87ee0', 'output/refine-run-20261028-105948/root-f16-seg4-static-ID-before-gate-v1.json': 'b309f9399bfc2ef4b39091d7c4a8d7c70f6766f3a5cec2a2ce27bb1bb65dd5f9', 'output/refine-run-20261028-105948/root-f16-seg4-typed-label-closure-before-v3.json': '9fa2c3c8d868c6530b37f237f922ea9efcbbf4de14d2fea8785df787c5bc9683', 'output/refine-run-20261028-105948/root-source-baseline-f16seg4.json': '9c5bb82e1e206bc50b04bd3f864d4436c4c3d86ce94fc24301e8b80019c24f03', 'tools/asm-regen/ghidra/ExportRangeToGas.py': '4544a6a95f922f5a1779553555180ed2184955bc4fc1e92f96ad9b500ddaeb87'}, 'counts': {'EQ_ADD': 27, 'REF_ADD': 80, 'REF_PRESERVE': 13, 'CASE_VECTOR_PRESERVE_CORE': 83, 'SOURCE_LABEL': 120, 'SOURCE_EOL': 122, 'TARGET_LABEL': 73, 'DATA_REF_ADD': 80, 'FUNCTION_RENAME': 3, 'PLATE': 9, 'R4_TMODE_BYTES': 1838, 'R4_DATA': 64, 'R4_CODE': 884, 'R4_BODY': 1, 'R4_CALL_RETURN': 2}, 'contract_counts': {'analysis_input_records': 26, 'producer_outputs': 24, 'functions': 141, 'states': 4876, 'slot_holders': 4440, 'module_words': 1644, 'target_states': 508, 'units': 43716, 'external_units': 48, 'instruction_properties': 22359, 'label_closure_rows': 2618, 'closure_seeds': 2190, 'label_closure_incoming_before': 270, 'label_closure_incoming_after': 443, 'baseline_files': 207, 'snapshot_files': 212, 'before_static_ids': 35732, 'before_dynamic_ids': 48116, 'before_all_ids': 83848, 'new_USER_ids': 193, 'global_before': 2488, 'global_after': 2494, 'bindings_before': 12739, 'bindings_after': 12766}, 'segment': [135021392, 135026628], 'module': [135009352, 135053068], 'observer_function_count': 141, 'word_count': 1644, 'state_count': 4876, 'target_state_count': 508, 'external_unit_count': 48, 'bundle_fields': ['status', 'program_name', 'function_count', 'native', 'instruction_properties', 'label_closure'], 'evidence_version': 1, 'analysis_version': 3}
PROOF_COUNTS = {'functions': 141, 'states': 4876, 'words': 1644, 'targetStates': 508, 'units': 43716, 'externalUnits': 48, 'sourceFiles': 212, 'instructionProperties': 22359, 'labelClosureRows': 2618, 'labelClosureIncomingBefore': 270, 'labelClosureExpectedIncomingAfter': 443, 'beforeStaticIdentities': 35732, 'beforeDynamicIdentities': 48116, 'beforeAllIdentities': 83848, 'r4InstructionHeads': 884, 'r4CodeBytes': 1838, 'r4DataWords': 64, 'r4PaddingHalfwords': 17, 'r4ParentBodyBytes': 1894, 'r4CallReturn': 2}


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
    bag_fields = set(('references_from', 'references_to', 'body_references', 'references', 'incoming',
                      'added_source_refs', 'eol_comments', 'module_symbols', 'module_comments'))
    if type(expected) is dict:
        if type(actual) is not dict or set(actual) != set(expected):
            raise RuntimeError(label + ': exact dict schema')
        for key in expected:
            metadata_assert(label + '.' + key, actual[key], expected[key], key)
    elif type(expected) is list:
        if type(actual) is not list:
            raise RuntimeError(label + ': strict list')
        if field in bag_fields:
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


def expected_before_bundle():
    return {'status': 'F16_SEG4_FRESH_FULL_PRESTATE', 'program_name': ROOT_FULL_PRESTATE['program_name'],
            'function_count': ROOT_FULL_PRESTATE['function_count'], 'native': ROOT_FULL_PRESTATE,
            'instruction_properties': PROPERTIES_BEFORE, 'label_closure': LABEL_CLOSURE_BEFORE}


def expected_post_bundle(current):
    states = dict((int(row['state']['address'], 16), row['state']) for row in current['native']['slots'])
    planned = dict((int(row['state']['address'], 16), row['state']) for row in NATIVE_AFTER['slots'])
    bindings = {}
    for address, spec in PRIMITIVES['labels'].items():
        value = int(address, 16)
        actual = states[value]['primary_symbol']
        identity = actual['id']
        if not strict_integer(identity) or not 0 < identity < 2**63 or identity in ALL_BEFORE_IDS:
            raise RuntimeError('New USER ID aliases complete BEFORE identity at ' + address)
        token = 'DYNAMIC_USER_ID:' + spec['name']
        bindings[token] = identity
        metadata_assert('new USER ' + address, actual, bind_dynamic(planned[value]['primary_symbol'], {token: identity}))
    if len(bindings) != 193 or len(set(bindings.values())) != 193:
        raise RuntimeError('193 new USER identities must be distinct')
    properties = dict(PROPERTIES_BEFORE)
    properties['rows'] = [row['after'] for row in PROPERTY_PLAN['rows']]
    expected = {'status': 'F16_SEG4_FRESH_FULL_PRESTATE', 'program_name': ROOT_FULL_PRESTATE['program_name'],
                'function_count': ROOT_FULL_PRESTATE['function_count'], 'native': NATIVE_AFTER,
                'instruction_properties': properties, 'label_closure': LABEL_CLOSURE_PLAN['after']}
    return bind_dynamic(expected, bindings)


def verify_id_authorities():
    expected_static_keys = set(('id', 'address', 'name', 'qualified_name', 'type', 'source', 'dynamic', 'namespace_id'))
    previous = 0
    static_ids = []
    for row in STATIC_ID_BEFORE['rows']:
        if type(row) is not dict or set(row) != expected_static_keys or row['dynamic'] is not False:
            raise RuntimeError('Static BEFORE row schema')
        identity = row['id']
        if not strict_integer(identity) or not previous < identity < 2**63:
            raise RuntimeError('Static BEFORE ID order/type')
        static_ids.append(identity)
        previous = identity
    metadata_assert('full static authority', ALL_ID_BEFORE['static_ids'], static_ids)
    metadata_assert('all identity counts', ALL_ID_BEFORE['counts'], {'iterated': 83848, 'function_symbols': 5414, 'static': 35732, 'dynamic': 48116})
    if ALL_ID_BEFORE['iteration_finished'] is not True or ALL_ID_BEFORE['dynamic_ID_public_getter_verified'] is not True:
        raise RuntimeError('Incomplete public native identity enumeration')
    previous = 0
    rows = ALL_ID_BEFORE['dynamic_rows']
    if type(rows) is not list or len(rows) != 48116 or len(static_ids) != 35732:
        raise RuntimeError('Complete native identity list scope')
    static_set = set(static_ids)
    for row in rows:
        if type(row) is not dict or set(row) != set(('id', 'address', 'type', 'source', 'dynamic', 'namespace_id')):
            raise RuntimeError('Dynamic BEFORE row schema')
        identity = row['id']
        if not strict_integer(identity) or not previous < identity < 2**63 or identity in static_set or row['dynamic'] is not True:
            raise RuntimeError('Dynamic BEFORE identity/type/order/disjoint')
        if not strict_integer(row['namespace_id'], nonnegative=True):
            raise RuntimeError('Dynamic namespace type')
        for field in ('address', 'type', 'source'):
            if not isinstance(row[field], basestring):
                raise RuntimeError('Dynamic BEFORE DTO field type')
        previous = identity
    if len(ALL_BEFORE_IDS) != 83848:
        raise RuntimeError('Complete native identity union')


def verify_prestate(pre, recapture):
    metadata_assert('complete BEFORE bundle', pre, expected_before_bundle())
    if recapture:
        capture_before_inventory()
        metadata_assert('complete same-Program BEFORE recapture', capture(), pre)


def verify_post(pre):
    current = capture()
    metadata_assert('complete native POST bundle', current, expected_post_bundle(current))
    if MODE in ('fullrollback', 'apply'):
        metadata_assert('actual action counts', COUNTS, EXPECTED_COUNTS)
    return current


def make_address_set(ranges):
    result = AddressSet()
    for lo, hi in ranges:
        result.add(toAddr(int(lo, 16)), toAddr(int(hi, 16) - 1))
    return result


def address_set_values(value):
    result = set()
    iterator = value.getAddresses(True)
    while iterator.hasNext():
        result.add(long(iterator.next().getOffset()))
    return result


def apply_r4():
    if len(CODE_RANGES) != 25 or len(CODE_BYTES) != 1838 or len(R4_HEADS) != 884:
        raise RuntimeError('R4 exact code mask')
    before_units = dict((int(row['address'], 16), row) for row in ROOT_FULL_PRESTATE['extra_units'])
    raw_values = set(value for block in R4_PLAN['raw_blocks'] for value in range(int(block['lo'], 16), int(block['hi'], 16)))
    for value in sorted(raw_values):
        at = toAddr(value)
        if listing.getInstructionContaining(at) is not None or listing.getDefinedDataContaining(at) is not None or tmode_at(at) != 0 or (memory.getByte(at) & 255) != before_units[value]['byte']:
            raise RuntimeError('R4 raw NULL/bytes/context precondition %08x' % value)
    for lo, hi in CODE_RANGES:
        currentProgram.getProgramContext().setValue(tmode_register, toAddr(int(lo, 16)), toAddr(int(hi, 16) - 1), BigInteger.ONE)
    COUNTS['R4_TMODE_BYTES'] += len(CODE_BYTES)
    for row in R4_PLAN['new_data_words']:
        value = int(row['address'], 16)
        data = listing.createData(toAddr(value), Undefined4DataType.dataType, 4)
        if data is None or int(data.getLength()) != 4 or unicode(data.getDataType().getPathName()) != '/undefined4':
            raise RuntimeError('R4 Undefined4DataType contract')
        COUNTS['R4_DATA'] += 1
    heads = AddressSet()
    for value in sorted(R4_HEADS):
        heads.add(toAddr(value))
    restricted = make_address_set(CODE_RANGES)
    command = DisassembleCommand(heads, restricted, False)
    command.enableCodeAnalysis(False)
    if not command.applyTo(currentProgram, monitor):
        raise RuntimeError('R4 disassembly rejected: ' + str(command.getStatusMsg()))
    if address_set_values(command.getDisassembledAddressSet()) != CODE_BYTES:
        raise RuntimeError('R4 actual DisassembledAddressSet differs from1838 mask')
    for row in R4_PLAN['new_instruction_rows']:
        value = int(row['after']['address'], 16)
        actual = instruction_property_row(value)['instruction']
        desired = row['after']['instruction']
        if actual is None or actual['length'] != desired['length']:
            raise RuntimeError('R4 incomplete instruction length %08x' % value)
        if any(pc not in CODE_BYTES for pc in range(value, value + actual['length'])):
            raise RuntimeError('R4 instruction crosses restricted code boundary')
        COUNTS['R4_CODE'] += 1
    fn = functions.getFunctionAt(toAddr(0x080c4350))
    metadata_assert('R4 parent original body', body_ranges(fn), R4_PLAN['parent_body_before']['body_ranges'])
    body = AddressSet(fn.getBody())
    body.add(restricted)
    if body.getNumAddresses() != 1894 or body.contains(toAddr(0x080c4ca0)):
        raise RuntimeError('R4 parent additive body contract')
    fn.setBody(body)
    COUNTS['R4_BODY'] += 1
    for row in R4_PLAN['flow_override_projections']:
        value = int(row['address'], 16)
        instruction = listing.getInstructionAt(toAddr(value))
        if instruction is None or instruction.getLength() != 4 or str(instruction.getFlowOverride()) != 'NONE':
            raise RuntimeError('CALL_RETURN precondition')
        instruction.setFlowOverride(FlowOverride.CALL_RETURN)
        COUNTS['R4_CALL_RETURN'] += 1
    for value in R4_PLAN['padding_addresses']:
        at = toAddr(int(value, 16))
        if listing.getInstructionAt(at) is not None or listing.getDefinedDataContaining(at) is not None or tmode_at(at) != 0:
            raise RuntimeError('R4 zero padding must remain NULL/context0')


def apply_instruction_eols():
    if len(INSTRUCTION_EOLS) != 2:
        raise RuntimeError('Two approved instruction EOLs')
    for value, text in sorted(INSTRUCTION_EOLS.items()):
        row = STATE_CONTRACTS[value]
        if listing.getInstructionAt(toAddr(value)) is None or listing.getComment(CodeUnit.EOL_COMMENT, toAddr(value)) != row['before']['eol'] or not all(ord(char) < 128 for char in text):
            raise RuntimeError('Instruction EOL exact precondition')
        listing.setComment(toAddr(value), CodeUnit.EOL_COMMENT, text)
        COUNTS['SOURCE_EOL'] += 1

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
        if listing.getInstructionAt(toAddr(value)) is None and value not in R4_HEADS:
            raise RuntimeError('Missing existing property instruction %08x' % value)
        rows.append(instruction_property_row(value))
    return {'status': 'F14_MODULE_READONLY_PRESTATE_OK',
            'query_kind': 'ROOT_F16_SEG4_NATIVE_EXPANDED141_AND_RAW_INSTRUCTION_PROPERTIES_PRESTATE_V2',
            'program_name': unicode(currentProgram.getName()), 'function_count': int(functions.getFunctionCount()),
            'rows': rows, 'input_function_entries': ['0x%08x' % value for value in OBSERVER_FUNCTIONS],
            'input_instruction_slots': len(PROPERTY_REQUEST_ADDRESSES), 'input_nullable_raw_heads': len(R4_HEADS),
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
            if len(discovered) >= 8192:
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
    return {'status': 'F14_MODULE_READONLY_PRESTATE_OK', 'query_kind': 'ROOT_F16_SEG4_COMPLETE_CODE_AND_TYPED_LABEL_CLOSURE_GETTER_ONLY_V3',
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
        raise RuntimeError('Native complete83848 BEFORE identities changed')
    return len(identities)


def capture():
    return {'status': 'F16_SEG4_FRESH_FULL_PRESTATE', 'program_name': unicode(currentProgram.getName()),
            'function_count': int(functions.getFunctionCount()), 'native': capture_native(),
            'instruction_properties': capture_properties(), 'label_closure': capture_label_closure()}

# -*- coding: ascii -*-
def verify_inputs():
    for relative, digest in sorted(INPUT_HASHES.items()):
        path = os.path.join(ROOT, relative)
        if file_hash(path) != digest:
            raise RuntimeError('Frozen input SHA changed: ' + relative)
    review = open(os.path.join(ROOT, 'doc/dev/refine/F16-Seg-4.review.md'), 'rb').read().decode('utf8')
    if re.findall(r'(?m)^## Reviewer Verdict: F16-Seg-4 = (.+)$', review) != ['PASS']:
        raise RuntimeError('Final independent analysis verdict must be exactly PASS')
    if len(RAW_SLOT_ROWS) != 203 or len(SLOT_ROWS) != 203 or len(SLOTS) != 203:
        raise RuntimeError('203 exact slot addresses')
    for formal, row in zip(RAW_SLOT_ROWS, SLOT_PLAN['rows']):
        for column, expected in (('address', row['address']), ('action', row['action']), ('value', row['value']), ('gas_expression_after', row['gas_expression_after'])):
            metadata_assert('formal slot ' + column, formal[column], expected)
        for prefix, stage in (('old', 'before'), ('final', 'after')):
            for field, expected in row[stage].items():
                metadata_assert('formal slot ' + prefix + '_' + field, json.loads(formal[prefix + '_' + field + '_json']), expected)
    if len(RAW_PLATE_ROWS) != 9:
        raise RuntimeError('9 formal Function contracts')
    for formal, row in zip(RAW_PLATE_ROWS, FUNCTION_PLAN['rows']):
        metadata_assert('formal Function entry', formal['entry'], row['entry'])
        metadata_assert('formal Function before', json.loads(formal['before_function_json']), row['before'])
        metadata_assert('formal Function after', json.loads(formal['after_function_json']), row['after'])
    verify_id_authorities()
    if len(OBSERVER_FUNCTIONS) != 141 or len(set(OBSERVER_FUNCTIONS)) != 141 or len(STATE_CONTRACTS) != 4876 or len(WORD_REQUESTS) != 1644 or len(SLOT_REQUESTS) != 4440 or len(CLOSURE_SEEDS) != 2190:
        raise RuntimeError('Native exact observer scopes')
    if len(SOURCE_LABEL_ADDRESSES) != 120 or len(TARGET_MATERIALIZATIONS) != 73 or len(RENAMED_FUNCTIONS) != 3 or len(PLATES) != 9:
        raise RuntimeError('Approved identity/comment action scopes')
    for row in SLOT_PLAN['rows']:
        text = row['after']['eol']
        if row['action'] != 'CASE_VECTOR_PRESERVE_CORE' and (not isinstance(text, basestring) or not all(ord(char) < 128 for char in text)):
            raise RuntimeError('Slot EOL ASCII')
    for row in PLATES.values():
        if not isinstance(row['new_plate'], basestring) or not all(ord(char) < 128 for char in row['new_plate']):
            raise RuntimeError('Function PLATE ASCII')
    metadata_assert('Full holder BEFORE authority', ROOT_FULL_PRESTATE, read_json('root-f16-seg4-independent-prestate-v5.json'))
    metadata_assert('Tiny BEFORE authority', LABEL_CLOSURE_BEFORE, read_json('root-f16-seg4-typed-label-closure-before-v3.json'))
    snapshot = read_json(SNAPSHOT_NAME)
    if not strict_integer(snapshot.get('file_count'), 212) or not strict_integer(snapshot.get('baseline_file_count'), 207) or not strict_integer(snapshot.get('phase1_additions'), 5):
        raise RuntimeError('Source snapshot212 schema/count')
    baseline = read_json('root-source-baseline-f16seg4.json')
    additions = set(['tools/ghidra-labeling/RefineF16Seg4.py'] + ['doc/dev/refine/F16-Seg-4.' + suffix for suffix in ('proposal.md', 'review.md', 'slots.tsv', 'plates.tsv')])
    if len(baseline['files']) != 207 or set(snapshot['files']) != set(baseline['files']) | additions or snapshot['baseline_manifest'] != 'root-source-baseline-f16seg4.json' or snapshot['baseline_manifest_sha256'] != file_hash(os.path.join(RUN, 'root-source-baseline-f16seg4.json')):
        raise RuntimeError('Source snapshot212 membership/baseline')
    for relative, row in snapshot['files'].items():
        if not strict_sized_hash_row(row):
            raise RuntimeError('Source snapshot212 row schema')
        if relative in baseline['files']:
            metadata_assert('baseline source row', [row['size'], row['sha256']], [baseline['files'][relative]['size'], baseline['files'][relative]['sha256']])
        for base, expected in ((ROOT, row['sha256']), (os.path.join(ROOT, snapshot['snapshot_directory']), row['snapshot_sha256'])):
            path = os.path.join(base, relative)
            if os.path.getsize(path) != row['size'] or file_hash(path) != expected:
                raise RuntimeError('Source current/copy changed: ' + relative)


def proof_expected_values(fresh_hash):
    result = {'freshSha256': fresh_hash, 'scriptSha256': file_hash(getSourceFile().getAbsolutePath()),
              'snapshotSha256': file_hash(os.path.join(RUN, SNAPSHOT_NAME)),
              'freezeSha256': file_hash(os.path.join(RUN, 'f16-seg4-analysis-manifest-v3.json')),
              'canonicalSha256': file_hash(os.path.join(RUN, 'root-f16-seg4-independent-prestate-v5.json')),
              'verifierSha256': file_hash(os.path.join(RUN, 'f16-seg4-fresh-canonical-verifier-v1.py')),
              'instructionPropertiesSha256': file_hash(os.path.join(RUN, 'root-f16-seg4-instruction-properties-before-v2.json')),
              'labelClosurePlanSha256': file_hash(os.path.join(RUN, 'f16-seg4-label-closure-plan-v1.json')),
              'labelClosureBeforeSha256': file_hash(os.path.join(RUN, 'root-f16-seg4-typed-label-closure-before-v3.json')),
              'staticSymbolIdsBeforeSha256': file_hash(os.path.join(RUN, 'root-f16-seg4-all-static-symbol-IDs-before-v1.json')),
              'dynamicSymbolIdsBeforeSha256': file_hash(os.path.join(RUN, 'root-f16-seg4-all-dynamic-symbol-IDs-before-v1.json')),
              'allSymbolIdsCustodySha256': file_hash(os.path.join(RUN, 'root-f16-seg4-all-ID-before-gate-v1.json'))}
    result.update(PROOF_COUNTS)
    return result


def verify_plan(plan, prestate_hash):
    if plan.get('status') != 'F16_SEG4_PLAN_FROZEN':
        raise RuntimeError('Root frozen runtime plan required')
    for key, expected in PLAN_STATIC.items():
        metadata_assert('Root plan static ' + key, plan.get(key), expected)
    required = {'script_sha256': file_hash(getSourceFile().getAbsolutePath()),
                'prestate_sha256': prestate_hash, 'source_snapshot_manifest': SNAPSHOT_NAME,
                'source_snapshot_sha256': file_hash(os.path.join(RUN, SNAPSHOT_NAME)),
                'fresh_proof_sha256': file_hash(os.path.join(RUN, FRESH_PROOF_NAME)),
                'offline_selfcheck_sha256': file_hash(os.path.join(RUN, 'f16-seg4-phase1-v1-offline-selfcheck.json'))}
    for key, expected in required.items():
        metadata_assert('Root plan current ' + key, plan.get(key), expected)
    offline = read_json('f16-seg4-phase1-v1-offline-selfcheck.json')
    if offline.get('status') != 'F16_SEG4_PHASE1_V1_OFFLINE_SELFCHECK_PASS' or offline.get('script_sha256') != required['script_sha256']:
        raise RuntimeError('Current Script offline selfcheck required')
    proof = read_json(FRESH_PROOF_NAME)
    if proof.get('status') != 'PASS':
        raise RuntimeError('Independent complete native fresh proof required')
    for key, expected in proof_expected_values(prestate_hash).items():
        metadata_assert('independent fresh proof ' + key, proof.get(key), expected)

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

def exact_ref_cores(value):
    return [ref_core(ref_row(ref)) for ref in references.getReferencesFrom(toAddr(value))]

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

def apply_slots():
    for value, formal in sorted(SLOTS.items()):
        contract = SLOT_CONTRACTS[value]
        addr = toAddr(value)
        if (memory.getInt(addr) & 0xffffffff) != int(formal['old_value'], 16):
            raise RuntimeError('ROM value changed at %08x' % value)
        data = listing.getDefinedDataAt(addr)
        if (data is None or data.getLength() != 4 or
                unicode(data.getDataType().getPathName()) != formal['final_data_type']):
            raise RuntimeError('Data contract at %08x' % value)
        action = formal['action']
        if action == 'EQ_ADD':
            items = contract['after']['equate_references']
            if len(items) != 1:
                raise RuntimeError('EQ malformed at %08x' % value)
            item = items[0]
            if not ensure_equate(item['name'], long(item['value']) & 0xffffffff,
                                  value, int(item['operand'])):
                raise RuntimeError('EQ binding unexpectedly existed at %08x' % value)
        elif action == 'REF_ADD':
            additions = contract['after']['references_from']
            before_cores = [ref_core(item) for item in contract['before']['references_from']]
            new = [item for item in additions if ref_core(item) not in before_cores]
            if len(new) != 1 or not add_data_ref(value, new[0]):
                raise RuntimeError('REF_ADD malformed/existing at %08x' % value)
            COUNTS['DATA_REF_ADD'] += 1
        elif action == 'REF_PRESERVE':
            before = [ref_core(item) for item in contract['before']['references_from']]
            if sorted_rows(exact_ref_cores(value)) != sorted_rows(before):
                raise RuntimeError('REF_PRESERVE drift at %08x' % value)
        elif action == 'CASE_VECTOR_PRESERVE_CORE':
            before = [ref_core(item) for item in contract['before']['references_from']]
            if sorted_rows(exact_ref_cores(value)) != sorted_rows(before):
                raise RuntimeError('CASE_VECTOR core drift at %08x' % value)
        else:
            raise RuntimeError('Unknown action at %08x' % value)
        if action != 'CASE_VECTOR_PRESERVE_CORE':
            after_primary = contract['after']['primary_symbol']
            if after_primary is None or after_primary.get('source') != 'USER_DEFINED':
                raise RuntimeError('Source primary contract at %08x' % value)
            ensure_user_label(value, after_primary['name'])
            if contract['after'].get('eol') != formal['final_eol']:
                raise RuntimeError('Source EOL contract at %08x' % value)
            listing.setComment(addr, CodeUnit.EOL_COMMENT, contract['after'].get('eol'))
            COUNTS['SOURCE_LABEL'] += 1
            COUNTS['SOURCE_EOL'] += 1
        COUNTS[action] += 1

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

def receipt_bindings(save_authorization=None):
    result = {
        'script_sha256': file_hash(getSourceFile().getAbsolutePath()),
        'plan_sha256': file_hash(os.path.join(RUN, PLAN_NAME)),
        'fresh_sha256': file_hash(os.path.join(RUN, PRESTATE_NAME)),
        'fresh_proof_sha256': file_hash(os.path.join(RUN, FRESH_PROOF_NAME)),
        'source_snapshot_sha256': file_hash(os.path.join(RUN, SNAPSHOT_NAME)),
        'freeze_sha256': INPUT_HASHES['output/refine-run-20261028-105948/f16-seg4-analysis-manifest-v3.json'],
        'review_sha256': INPUT_HASHES['doc/dev/refine/F16-Seg-4.review.md'],
    }
    if save_authorization is not None:
        result.update(save_authorization['bindings'])
        result.update({
            'grant_sha256': save_authorization['grant_sha256'],
            'gate_nonce': save_authorization['gate_nonce'],
            'claim_sha256': save_authorization['claim_sha256'],
        })
    return result

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


verify_inputs()
if MODE == 'prestate':
    capture_before_inventory()
    result = capture()
    verify_prestate(result, False)
    write_json(PRESTATE_NAME, result)
    print('STATUS: OK PRESTATE native141 states4876 props22359 Tiny2618')
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
    write_json('f16-seg4-dry-%s.json' % EVIDENCE_VERSION, payload)
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
        tx = currentProgram.startTransaction('F16-Seg-4 approved materialization')
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
        apply_r4()
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
        write_json('f16-seg4-%s-%s.json' % (MODE, EVIDENCE_VERSION), payload)
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
        write_json('f16-seg4-%s-failure-%s.json' % (MODE, EVIDENCE_VERSION),
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
    write_json('f16-seg4-persisted-check-%s.json' % EVIDENCE_VERSION, payload)
    print('STATUS: OK CHECK FAIL=0')




