# -*- coding: ascii -*-
#@runtime Jython
#@category Ygo-ex2006.Refine
# F16-Seg-5 approved materialization. Phase1 uses prestate/dry/fullrollback only.

import csv
from collections import defaultdict, Counter
import hashlib
import json
import os
import traceback
import re
from java.math import BigInteger
from ghidra.program.model.address import AddressSet
from ghidra.program.model.data import Undefined4DataType, DWordDataType
from ghidra.app.cmd.disassemble import DisassembleCommand

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
PLAN_NAME = 'f16-seg5-plan-v1.json'
PRESTATE_NAME = 'f16-seg5-fresh-full-prestate-v1.json'
SNAPSHOT_NAME = 'f16-seg5-source-snapshot-preapply-v1.json'
FRESH_PROOF_NAME = 'f16-seg5-fresh-canonical-proof-v1.json'
AUTH_CONTRACT_NAME = 'f16-seg5-once-save-contract-v1.json'
AUTH_CONTRACT_SHA256 = '5e0684b0bc4fdc8e1fb7b95973981cc4b15413cb714c274eb7caa99b52773676'
GRANT_NAME = 'root-f16-seg5-implementation-gate.json'
ROOT_ATTEMPT_NAME = 'f16-seg5-apply-once-v1.json'
SCRIPT_CLAIM_NAME = 'f16-seg5-script-apply-claim-v1.json'
APPLY_RECEIPT_NAME = 'f16-seg5-apply-v1.json'
PHASE1A_MANIFEST_NAME = 'f16-seg5-phase1a-manifest-v1.json'
PHASE1_MANIFEST_NAME = 'f16-seg5-phase1-manifest-v1.json'
PHASE1_AUDIT_NAME = 'f16-seg5-phase1-static-review-v1.json'
INPUT_HASHES = {'doc/dev/refine/F16-Seg-5.plates.tsv': '061ba7037fbd3ea89df085a478eb7fc25403f56c48493d84afbe66672a6b10f2', 'doc/dev/refine/F16-Seg-5.proposal.md': '4f069a7d05817e6154459cb39c9be1a1ebd31ae60ba22a6b31a9bd39f4ccd29a', 'doc/dev/refine/F16-Seg-5.review.md': '6678f15ecd21443c0e2d53039be904d7f91308851343dc987ea61e81995b6e50', 'doc/dev/refine/F16-Seg-5.slots.tsv': 'a597aac9c1692a731dca32db4fa4342af8a3e15ed3c8c61b6b27667a8a7ef752', 'output/refine-run-20261028-105948/f15-readonly-scripts/F16ModuleIndependentQuery.java': '042c3c176a03341d0c7b6ae775086ae4308b27b6c3c0218daa917832b1951011', 'output/refine-run-20261028-105948/f15-readonly-scripts/F16Seg5CompleteTypedLabelClosureQueryV1.java': '651a69f1e87617596d249293b4361000a77a66ebe0f9199436f4625f7cc41af8', 'output/refine-run-20261028-105948/f15-readonly-scripts/F16Seg5ExpandedInstructionPropertiesQueryV2.java': '0af472743e1e5998d0d4c3e0c2f3960d1911ec6aaa45dbd2b9830184a65617e2', 'output/refine-run-20261028-105948/f15-readonly-scripts/F16Seg5PseudoDecodeQueryV1.java': 'e98684c6ef336e8c127fd42c7eace269ae3fe3645760c2c4099fdd86127b267b', 'output/refine-run-20261028-105948/f16-seg1-analysis-validator-v2.py': '5472177d1856c01db0f2b1fd6cce08bd9e0fb69d289bdb725ad053b3b42da768', 'output/refine-run-20261028-105948/f16-seg4-source-landing-pins-v1.json': 'e73dcebd0157c65d9ac9ce5f109199deb9d54f387375c224b82547c32ec09b80', 'output/refine-run-20261028-105948/f16-seg5-action-bases-draft-v1.json': '30ebe07c13cc92895056ce45e52d36ddeea0b66932b5f53681952d34230a0fe8', 'output/refine-run-20261028-105948/f16-seg5-analysis-source-v1.json': '8239a98d4a3d85f1b9e9d9933d8659865752df984060f48185057260ca405030', 'output/refine-run-20261028-105948/f16-seg5-before-ID-and-binding-contract-v1.json': '5272a6e2d231b111eec7464563d6d637f3b52213f9c32e85c9036e68112e0346', 'output/refine-run-20261028-105948/f16-seg5-decisions-v1.json': 'cb0d1baaa2edf5094e3eaf6a9d71ade20cd400891b695360aa18fe7c199f6633', 'output/refine-run-20261028-105948/f16-seg5-final-manifest-v1.json': 'cbf9e2591a0af6bed6a45fbc82747e0008b4a752a22e2ac9cd78ce050d20bb4f', 'output/refine-run-20261028-105948/f16-seg5-firststage-manifest-v1.json': '9b21b01b46a05d94e5a82ade09dfede839771646c116ce87a20564e672fdf69b', 'output/refine-run-20261028-105948/f16-seg5-fresh-canonical-verifier-v1.py': '71092a166513dd4946780f97b9e5d155b19e964e0129c83015d1df88bb2507f5', 'output/refine-run-20261028-105948/f16-seg5-full-function-observation-plan-v1.json': 'ff2e2167942388ec911d77e4325c33567fa519e651d42037eb060842d499a0f5', 'output/refine-run-20261028-105948/f16-seg5-full-rom-refscan-v1.json': '39fdbddc4eaa139afb7e5c7e7f23c347aeec8f9443cf411712ebec8199285722', 'output/refine-run-20261028-105948/f16-seg5-fullstate-observation-plan-v1.json': 'b87633702fd1458d50c38391b4c45e975162d0c3f911a820928990be1ed7ccb4', 'output/refine-run-20261028-105948/f16-seg5-function-plan-v1.json': 'e6cc8b2a7c0990ab8d6662eeaed07a62c7ff45580c6682e4fd3c659eaf8a8ea7', 'output/refine-run-20261028-105948/f16-seg5-gas-projections-v1.json': 'df3e91e480852ff95e182c05f043746fc1fdfc4cfd8476d6523fbd44a7f0a711', 'output/refine-run-20261028-105948/f16-seg5-global-equates-plan-v1.json': 'c50c41416fd90b06b00edf9f5a15c8402f7bb3e908b941d95d13c5eabc6a5688', 'output/refine-run-20261028-105948/f16-seg5-initial-cfg-v1.json': '259be8c05041c9f42120c45b731f2bdd7f73a0e81817a1f4660b87a5d7eb5c3e', 'output/refine-run-20261028-105948/f16-seg5-initial-full-rom-refscan-v1.json': 'ea4e937cc7540962209411810501a7957327eed4e7a9417b3e2fd6a342dc58c8', 'output/refine-run-20261028-105948/f16-seg5-inputs-v3.json': '5914ffbdbf9c3e739813dab76fc6b9ad8fec29b68fa956b3c1eccdb980ca285f', 'output/refine-run-20261028-105948/f16-seg5-instruction-properties-plan-v1.json': 'c7146ce723f9816daea186bd79fba3387534dad4c757bbf17eba7af34790497a', 'output/refine-run-20261028-105948/f16-seg5-label-closure-plan-v1.json': '3da758112a2815089efe47305a2c7833a12f495ad260d8a05461b6c364ace8ce', 'output/refine-run-20261028-105948/f16-seg5-name-reference-baseline-v1.json': 'be9c6abf29819f97893e289719314a70cbc1064b2633fd73e21ffa5154e25659', 'output/refine-run-20261028-105948/f16-seg5-native-collector-draft-v1.py': 'dce47471728601342ebc9361533987bef09fd76d17793b1ebdcde0518e11b379', 'output/refine-run-20261028-105948/f16-seg5-native-collector-fixtures-v1.py': 'd912b325b318ff87bc00797ede5c945f75dcc92538f9c1913e24b720acf6d734', 'output/refine-run-20261028-105948/f16-seg5-native-collector-preparation-v1.json': 'c7eda554500868ed7d6c57c42b15237c3fa21001ee0b5d32042fb9e7abce1c1e', 'output/refine-run-20261028-105948/f16-seg5-native-instruction-projection-v1.json': 'a8392723e62fc8354afa6126591720becd8d0af36a10e6035e0e7b85ae8b1e6b', 'output/refine-run-20261028-105948/f16-seg5-native-module-metadata-plan-v1.json': '8bb285735b107e8b77245d20b062b775cfec7211fefb09c3992a04bab9f58cb0', 'output/refine-run-20261028-105948/f16-seg5-native-query-full-observation-plan-v1.json': 'e770fbcb0e8bdea1c0bba8ff99ef2e1b4f2c7e8af7ceaae21b76da48877d65bb', 'output/refine-run-20261028-105948/f16-seg5-native-resolver-execution-v1.json': 'f22311625dea3aec658b9fd1cb6b3577a557e89fe48cb4909b059dde5d95192c', 'output/refine-run-20261028-105948/f16-seg5-negative-suite-v1.json': 'ed851ea2331e76052d15b2ba5d665c5a3da36e5d9f56e68ab39070172e56d245', 'output/refine-run-20261028-105948/f16-seg5-once-save-contract-v1.json': '5e0684b0bc4fdc8e1fb7b95973981cc4b15413cb714c274eb7caa99b52773676', 'output/refine-run-20261028-105948/f16-seg5-phase-table-boundary-correction-draft-v1.json': 'a408647b6ecc05d793dd34d444747d698fc41a915df9359f345c2be4d0ac3a06', 'output/refine-run-20261028-105948/f16-seg5-plates-final-v1.tsv': '061ba7037fbd3ea89df085a478eb7fc25403f56c48493d84afbe66672a6b10f2', 'output/refine-run-20261028-105948/f16-seg5-primary-symbol-plan-v1.json': '87a14ccb5e0245af80ff4fce134b18e4db475523422a141f757e103ef565b265', 'output/refine-run-20261028-105948/f16-seg5-primitives-v3.json': '40bc44a805f5f5c74dca2f97dbf29f7457ebb349d1ecb6d56d1d5f4ff438ea94', 'output/refine-run-20261028-105948/f16-seg5-proposal-final-v1.md': '4f069a7d05817e6154459cb39c9be1a1ebd31ae60ba22a6b31a9bd39f4ccd29a', 'output/refine-run-20261028-105948/f16-seg5-r4-plan-v1.json': '1c2813e31474b2d22a3d4da848c3f83b7f3ec3c2804b7b2968e74fe5d3695562', 'output/refine-run-20261028-105948/f16-seg5-r7-plan-v1.json': 'f46167d4167e0ae64226a73ba0dcd1762f2ce7d69447c7b922ef794878958c31', 'output/refine-run-20261028-105948/f16-seg5-registry-plan-v1.json': '5af1fbcd31568d40f8b479d4f22fd4b7f90c77d8cbc80cf6f47e25f4a4a11da2', 'output/refine-run-20261028-105948/f16-seg5-reviewer-audit-v1.json': 'ea38c31745c757dae28a5697704929c89f0ec6b9986f9b62b55ece5c3d62b2a8', 'output/refine-run-20261028-105948/f16-seg5-root-pure-preparation-review-v1.json': '183ba85a6363dbced8be73bcbefc730043e92ae967b3e59f5d0b7406887e8a5e', 'output/refine-run-20261028-105948/f16-seg5-selfcheck-v1.json': '1fde88604b5e631ffc345be47da33995089e4c9c8c36cdfda2a3363ec769103c', 'output/refine-run-20261028-105948/f16-seg5-semantic-plan-v1.json': '34201c528f2c27612257d91e1a80996197d937e70411c6bdeb8c181dd02dc8e9', 'output/refine-run-20261028-105948/f16-seg5-slot-plan-v1.json': 'fde2964d731576b7e5531ed07ac82e084242460c9daab35b7e6b4b86e4c8b73f', 'output/refine-run-20261028-105948/f16-seg5-slots-final-v1.tsv': 'a597aac9c1692a731dca32db4fa4342af8a3e15ed3c8c61b6b27667a8a7ef752', 'output/refine-run-20261028-105948/f16-seg5-source-scope-plan-v1.json': '70eab24032ea23d06c01e1c2208efb4c36b95497bd2be888f46e87b7c9f867f2', 'output/refine-run-20261028-105948/f16-seg5-stage2-manifest-draft-v1.json': '66a826ec20ea2e74cfc1a2e72998cef46d8b6eea93bde7637a212416938eac3f', 'output/refine-run-20261028-105948/f16-seg5-target-plan-v1.json': 'f9d49c5b43debb40e1364b97ebc2d8cc18df88c4c858ee706d3290367df4c8d0', 'output/refine-run-20261028-105948/root-f15-seg6-transaction-mechanism.json': '908138c1819efa2dc2df669a76926d4d8d9934f479829801b01d9d7038356480', 'output/refine-run-20261028-105948/root-f16-seg5-all-ID-before-gate-v1.json': 'abfe5dfd0647bc63f95e3fb19e53ffa15a47a7b5ebe49c2a32d06cc674685d76', 'output/refine-run-20261028-105948/root-f16-seg5-all-dynamic-symbol-IDs-before-v1.json': 'b071bd76650fd84d59f0ded5a62ce202ffa7c537c7253499d6c4092b3f2d9e03', 'output/refine-run-20261028-105948/root-f16-seg5-all-static-symbol-IDs-before-v1.json': 'b227b8ed7c9b76706765218c35bb6e6decf59e56ee18d981bfd178a144d7fe55', 'output/refine-run-20261028-105948/root-f16-seg5-collector-cross-schema-gate-v2.json': '3686f83a2b2dc0f67526bada7301bff214ed36a697344b06122e39428430f0c9', 'output/refine-run-20261028-105948/root-f16-seg5-db-backup.json': '3b6bd8a45ab3eb754c796693fb951f0031ab1d28501c96d70a06186f8ae1b71d', 'output/refine-run-20261028-105948/root-f16-seg5-expanded-equates-input-v4.json': '37517e5f3dc66819f61f5a7bb8ace1921282415f10551d2defa5c3eb0985b570', 'output/refine-run-20261028-105948/root-f16-seg5-expanded-functions-input-v4.json': 'fe8aaa51d9f3babc29b05ba10358660dcbcee03e0f24120f5d7358b180c4b603', 'output/refine-run-20261028-105948/root-f16-seg5-expanded-query-inputs-v4.json': 'af34a66ae5cf8cab85cccbc7856c87fd38517e9bd298f1f5e57f026fd2b2f822', 'output/refine-run-20261028-105948/root-f16-seg5-expanded-slots-input-v4.json': 'a707ff8c91229dee05422d138d96b68c6bb574788a7030c2c1f89b11679dc413', 'output/refine-run-20261028-105948/root-f16-seg5-expanded-words-input-v4.json': '2229cf77b9a96273a252b2e24608ef6e9704974e3a3918b13f70070984280933', 'output/refine-run-20261028-105948/root-f16-seg5-independent-prestate-v5.json': '6aab066769000c66e19de104496544d5e87319841df2085d09216af60183ff53', 'output/refine-run-20261028-105948/root-f16-seg5-independent-prestate-v5.json.db-gate.json': 'ae958ad9d22279d39ce20c370a3f151e40e89194849a11ec1b282dee459e96fb', 'output/refine-run-20261028-105948/root-f16-seg5-instruction-properties-before-v2.json': 'fa06848756a158b2ddef8f3ff79575bcebcb3e5c55b5118c06ab515e08a2b548', 'output/refine-run-20261028-105948/root-f16-seg5-instruction-properties-before-v2.json.db-gate.json': 'ae958ad9d22279d39ce20c370a3f151e40e89194849a11ec1b282dee459e96fb', 'output/refine-run-20261028-105948/root-f16-seg5-instruction-slot-input-v1.json': 'ddca3dc52444f1ed88061b767653d226edda7f96df00815fcc31f0b8680eea78', 'output/refine-run-20261028-105948/root-f16-seg5-label-closure-getter-preparation-v1.json': '16e80f021f942b0271ecf02346e0087fbe5fe28a85bda3366e85c5ba2702ce5e', 'output/refine-run-20261028-105948/root-f16-seg5-label-closure-seeds-v1.json': '165ba1c489b0264fa1e921905774f1144f442a4f28174440004383ede29cd793', 'output/refine-run-20261028-105948/root-f16-seg5-native-before-complete-v1.json': '6e1fbaf952604ff65efd9a418f4225fc6dabe589a4469fd69bfc4b43c57792c2', 'output/refine-run-20261028-105948/root-f16-seg5-native-supplement-preparation-v1.json': 'b9599a0bea15c8e1de17d59d94bf8f1655c474cf5a52fe8226f60bb222117317', 'output/refine-run-20261028-105948/root-f16-seg5-pseudo-decode-v1.json': '41bd895d1291fef6567b8ad04c0d1ac7f6eea46ca838a797f8cc88ca6391bbc1', 'output/refine-run-20261028-105948/root-f16-seg5-pseudo-decode-v1.json.db-gate.json': 'ae958ad9d22279d39ce20c370a3f151e40e89194849a11ec1b282dee459e96fb', 'output/refine-run-20261028-105948/root-f16-seg5-raw-instruction-heads-input-v1.json': '360470526efee8a9b0a3c53d18002f8bf786c87cfd9720a7b7c94f03759473f5', 'output/refine-run-20261028-105948/root-f16-seg5-typed-label-closure-before-v1.json': '26daa891d9d62de99c741b9909f73534f79abc7ee7496304a0178b6140f65766', 'output/refine-run-20261028-105948/root-f16-seg5-typed-label-closure-before-v1.json.db-gate.json': 'ae958ad9d22279d39ce20c370a3f151e40e89194849a11ec1b282dee459e96fb', 'output/refine-run-20261028-105948/root-source-baseline-f16seg5.json': '25c8767f34ac1f6a50f0e529f3e02affdc45d1a6eb55d418ca61a3e23c4c5695', 'output/refine-run-20261028-105948/root_query_f15_module_8g.ps1': '0913ef217a84e98edc8d1cd4cbc51acf5d909d551bbb82ae73d6d532f7c97b88', 'tools/asm-regen/ghidra/ExportRangeToGas.py': '4544a6a95f922f5a1779553555180ed2184955bc4fc1e92f96ad9b500ddaeb87'}
AUXILIARY_INPUTS = ('f15-readonly-scripts/F16ModuleIndependentQuery.java', 'f15-readonly-scripts/F16Seg5CompleteTypedLabelClosureQueryV1.java', 'f15-readonly-scripts/F16Seg5ExpandedInstructionPropertiesQueryV2.java', 'f15-readonly-scripts/F16Seg5PseudoDecodeQueryV1.java', 'f16-seg1-analysis-validator-v2.py', 'f16-seg4-source-landing-pins-v1.json', 'f16-seg5-action-bases-draft-v1.json', 'f16-seg5-analysis-source-v1.json', 'f16-seg5-before-ID-and-binding-contract-v1.json', 'f16-seg5-decisions-v1.json', 'f16-seg5-final-manifest-v1.json', 'f16-seg5-firststage-manifest-v1.json', 'f16-seg5-fresh-canonical-verifier-v1.py', 'f16-seg5-full-function-observation-plan-v1.json', 'f16-seg5-full-rom-refscan-v1.json', 'f16-seg5-fullstate-observation-plan-v1.json', 'f16-seg5-function-plan-v1.json', 'f16-seg5-gas-projections-v1.json', 'f16-seg5-global-equates-plan-v1.json', 'f16-seg5-initial-cfg-v1.json', 'f16-seg5-initial-full-rom-refscan-v1.json', 'f16-seg5-inputs-v3.json', 'f16-seg5-instruction-properties-plan-v1.json', 'f16-seg5-label-closure-plan-v1.json', 'f16-seg5-name-reference-baseline-v1.json', 'f16-seg5-native-collector-draft-v1.py', 'f16-seg5-native-collector-fixtures-v1.py', 'f16-seg5-native-collector-preparation-v1.json', 'f16-seg5-native-instruction-projection-v1.json', 'f16-seg5-native-module-metadata-plan-v1.json', 'f16-seg5-native-query-full-observation-plan-v1.json', 'f16-seg5-native-resolver-execution-v1.json', 'f16-seg5-negative-suite-v1.json', 'f16-seg5-once-save-contract-v1.json', 'f16-seg5-phase-table-boundary-correction-draft-v1.json', 'f16-seg5-plates-final-v1.tsv', 'f16-seg5-primary-symbol-plan-v1.json', 'f16-seg5-primitives-v3.json', 'f16-seg5-proposal-final-v1.md', 'f16-seg5-r4-plan-v1.json', 'f16-seg5-r7-plan-v1.json', 'f16-seg5-registry-plan-v1.json', 'f16-seg5-reviewer-audit-v1.json', 'f16-seg5-root-pure-preparation-review-v1.json', 'f16-seg5-selfcheck-v1.json', 'f16-seg5-semantic-plan-v1.json', 'f16-seg5-slot-plan-v1.json', 'f16-seg5-slots-final-v1.tsv', 'f16-seg5-source-scope-plan-v1.json', 'f16-seg5-stage2-manifest-draft-v1.json', 'f16-seg5-target-plan-v1.json', 'root-f15-seg6-transaction-mechanism.json', 'root-f16-seg5-all-ID-before-gate-v1.json', 'root-f16-seg5-all-dynamic-symbol-IDs-before-v1.json', 'root-f16-seg5-all-static-symbol-IDs-before-v1.json', 'root-f16-seg5-collector-cross-schema-gate-v2.json', 'root-f16-seg5-db-backup.json', 'root-f16-seg5-expanded-equates-input-v4.json', 'root-f16-seg5-expanded-functions-input-v4.json', 'root-f16-seg5-expanded-query-inputs-v4.json', 'root-f16-seg5-expanded-slots-input-v4.json', 'root-f16-seg5-expanded-words-input-v4.json', 'root-f16-seg5-independent-prestate-v5.json', 'root-f16-seg5-independent-prestate-v5.json.db-gate.json', 'root-f16-seg5-instruction-properties-before-v2.json', 'root-f16-seg5-instruction-properties-before-v2.json.db-gate.json', 'root-f16-seg5-instruction-slot-input-v1.json', 'root-f16-seg5-label-closure-getter-preparation-v1.json', 'root-f16-seg5-label-closure-seeds-v1.json', 'root-f16-seg5-native-before-complete-v1.json', 'root-f16-seg5-native-supplement-preparation-v1.json', 'root-f16-seg5-pseudo-decode-v1.json', 'root-f16-seg5-pseudo-decode-v1.json.db-gate.json', 'root-f16-seg5-raw-instruction-heads-input-v1.json', 'root-f16-seg5-typed-label-closure-before-v1.json', 'root-f16-seg5-typed-label-closure-before-v1.json.db-gate.json', 'root-source-baseline-f16seg5.json', 'root_query_f15_module_8g.ps1')
EXPECTED_COUNTS = {'EQ_ADD': 37, 'REF_ADD': 139, 'REF_PRESERVE': 4, 'CASE_VECTOR_PRESERVE_CORE': 62, 'R7_DATA_DEFINE': 7, 'R7_TYPE_PRESERVE': 1, 'SOURCE_LABEL': 181, 'SOURCE_EOL': 188, 'TARGET_LABEL': 152, 'DATA_REF_ADD': 139, 'FUNCTION_RENAME': 9, 'PLATE': 11, 'R4_TMODE_BYTES': 794, 'R4_DATA': 103, 'R4_CODE': 395, 'R4_BODY': 2, 'R4_CALL_RETURN': 0, 'R7_DWORD': 7}
SEGMENT_START = 135026628
SEGMENT_END = 135031196
MODULE_START = 0x080c1448
MODULE_END = 0x080cbf0c

CONTRACT_COUNTS = {'analysis_records': 34, 'analysis_input_records': 17, 'producer_outputs': 26, 'functions': 137, 'states': 7295, 'slot_holders': 7218, 'module_words': 1755, 'target_states': 578, 'even_function_holders': 5, 'units': 43716, 'external_units': 48, 'instruction_properties': 20264, 'nullable_properties_before': 395, 'label_closure_rows': 2441, 'closure_seeds': 2119, 'label_closure_incoming_before': 211, 'label_closure_incoming_after': 532, 'baseline_files': 212, 'snapshot_files': 217, 'before_static_ids': 35925, 'before_dynamic_ids': 48035, 'before_all_ids': 83960, 'new_USER_ids': 333, 'global_before': 2494, 'global_after': 2503, 'bindings_before': 12766, 'bindings_after': 12803, 'new_raw_data': 103, 'new_r7_dwords': 7, 'R4_parents': 2}

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
            'output/refine-run-20261028-105948/f16-seg5-final-manifest-v1.json'],
        'analysis_review_sha256': INPUT_HASHES['doc/dev/refine/F16-Seg-5.review.md'],
        'canonical_sha256': file_hash(require_file(
            'root-f16-seg5-independent-prestate-v5.json',
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
        'schema': 'F16_SEG5_ROOT_ONCE_SAVE_GATE_V2',
        'status': 'ROOT_F16_SEG5_IMPLEMENTATION_GATE_PASS',
        'segment': 'F16-Seg-5',
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
            'F16_SEG5_PHASE1_%s_COMPLETE' % EVIDENCE_VERSION.upper() or
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
        'segment': 'F16-Seg-5',
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
        'segment': 'F16-Seg-5',
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
        write_json('f16-seg5-%s-failures-%s.json' % (MODE, EVIDENCE_VERSION), {
            'status': 'FAIL', 'phase': phase, 'FAIL': len(FAILS),
            'failures': FAILS,
        })
        raise RuntimeError('%s FAIL=%d' % (phase, len(FAILS)))

# -*- coding: ascii -*-
# Seg5 callable getter-only draft. No Script entry point, transaction or writer.
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
    rows(function_requests, 137, 'Function requests')
    rows(word_requests, 1755, 'word requests')
    slots = rows(slot_requests, 7218, 'slot requests')
    rows(property_requests, 17445, 'property requests')
    nullable = rows(nullable_property_heads, 395, 'nullable property heads')
    rows(closure_seeds, 2119, 'Tiny seeds')
    if not set(range(0x09e5ab84, 0x09e5aba4)).issubset(slots):
        raise RuntimeError('Complete32 R7 bytes must remain inside native slot scope')
    if any(address & 1 or not (0x080c5c3c <= address < 0x080c608a or 0x080c63e0 <= address < 0x080c6456) for address in nullable):
        raise RuntimeError('Nullable property head scope')
    if type(segment_equates) is not list or segment_equates:
        raise RuntimeError('Exact empty segment-equate input')
    if static_id_authority.get('iteration_finished') is not True or all_id_authority.get('iteration_finished') is not True or all_id_authority.get('dynamic_ID_public_getter_verified') is not True:
        raise RuntimeError('Complete native BEFORE identity enumeration required')
    statics = static_id_authority['rows']
    if type(statics) is not list or len(statics) != 35925:
        raise RuntimeError('Complete35925 static authority rows')
    static_ids = []
    previous = 0
    for row in statics:
        if type(row) is not dict or set(row) != set(('id','address','name','qualified_name','type','source','dynamic','namespace_id')) or row['dynamic'] is not False or not integer(row['id']) or row['id'] <= previous:
            raise RuntimeError('Static identity DTO/type/order')
        static_ids.append(row['id'])
        previous = row['id']
    observed_static = all_id_authority['static_ids']
    if type(observed_static) is not list or len(observed_static) != 35925 or any(not integer(value) for value in observed_static) or observed_static != static_ids:
        raise RuntimeError('Independent native static identity lists disagree')
    expected_counts = {'iterated':83960,'static':35925,'dynamic':48035,'function_symbols':5414}
    counts = all_id_authority['counts']
    if type(counts) is not dict or set(counts) != set(expected_counts) or any(type(counts[key]) not in (int, long) or counts[key] != expected_counts[key] for key in expected_counts):
        raise RuntimeError('Strict complete83960 native identity counts')
    dynamics = all_id_authority['dynamic_rows']
    if type(dynamics) is not list or len(dynamics) != 48035:
        raise RuntimeError('Complete48035 dynamic authority rows')
    identities = set(static_ids)
    previous = 0
    for row in dynamics:
        if type(row) is not dict or set(row) != set(('id','address','type','source','dynamic','namespace_id')) or row['dynamic'] is not True or not integer(row['id']) or row['id'] <= previous or row['id'] in identities:
            raise RuntimeError('Dynamic identity DTO/type/order/disjointness')
        if type(row['namespace_id']) not in (int, long) or not 0 <= row['namespace_id'] < 2**63 or any(not isinstance(row[key], basestring) for key in ('address','type','source')):
            raise RuntimeError('Dynamic identity complete field types')
        identities.add(row['id'])
        previous = row['id']
    if len(identities) != 83960:
        raise RuntimeError('Complete83960 BEFORE identities')
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
            'query_kind': 'ROOT_F16_SEG5_NATIVE_EXPANDED137_AND_RAW_INSTRUCTION_PROPERTIES_PRESTATE_V2',
            'program_name': unicode(currentProgram.getName()), 'function_count': int(functions.getFunctionCount()),
            'rows': rows, 'input_function_entries': ['0x%08x' % value for value in OBSERVER_FUNCTIONS],
            'input_instruction_slots': len(PROPERTY_REQUEST_ADDRESSES), 'input_nullable_raw_heads': len(NULLABLE_PROPERTY_HEADS),
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
    return {'status': 'F14_MODULE_READONLY_PRESTATE_OK', 'query_kind': 'ROOT_F16_SEG5_COMPLETE_CODE_AND_TYPED_LABEL_CLOSURE_GETTER_ONLY_V1',
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
        raise RuntimeError('Native complete83960 BEFORE identities changed')
    return len(identities)


def capture():
    return {'status': 'F16_SEG5_READONLY_NATIVE_BUNDLE_DRAFT', 'program_name': unicode(currentProgram.getName()),
            'function_count': int(functions.getFunctionCount()), 'native': capture_native(),
            'instruction_properties': capture_properties(), 'label_closure': capture_label_closure()}

# -*- coding: ascii -*-
# Pure model bindings; native getters are invoked only by capture paths below.
RAW_SLOT_ROWS = read_tsv('doc/dev/refine/F16-Seg-5.slots.tsv')
RAW_PLATE_ROWS = read_tsv('doc/dev/refine/F16-Seg-5.plates.tsv')
SLOT_PLAN = read_json('f16-seg5-slot-plan-v1.json')
FUNCTION_PLAN = read_json('f16-seg5-function-plan-v1.json')
FULL_NATIVE_PLAN = read_json('f16-seg5-native-query-full-observation-plan-v1.json')
ROOT_FULL_PRESTATE = FULL_NATIVE_PLAN['before']
NATIVE_AFTER = FULL_NATIVE_PLAN['after']
PROPERTIES_BEFORE = read_json('root-f16-seg5-instruction-properties-before-v2.json')
PROPERTY_PLAN = read_json('f16-seg5-instruction-properties-plan-v1.json')
LABEL_CLOSURE_PLAN = read_json('f16-seg5-label-closure-plan-v1.json')
LABEL_CLOSURE_BEFORE = LABEL_CLOSURE_PLAN['before']
R4_PLAN = read_json('f16-seg5-r4-plan-v1.json')
R7_PLAN = read_json('f16-seg5-r7-plan-v1.json')
PRIMITIVES = read_json('f16-seg5-primitives-v3.json')
STATIC_ID_BEFORE = read_json('root-f16-seg5-all-static-symbol-IDs-before-v1.json')
ALL_ID_BEFORE = read_json('root-f16-seg5-all-dynamic-symbol-IDs-before-v1.json')
COLLECTOR_INPUTS = [read_json(name) for name in ('root-f16-seg5-expanded-functions-input-v4.json',
    'root-f16-seg5-expanded-words-input-v4.json', 'root-f16-seg5-expanded-slots-input-v4.json',
    'root-f16-seg5-expanded-equates-input-v4.json', 'root-f16-seg5-instruction-slot-input-v1.json',
    'root-f16-seg5-raw-instruction-heads-input-v1.json', 'root-f16-seg5-label-closure-seeds-v1.json')]
configure_scope(*(COLLECTOR_INPUTS + [STATIC_ID_BEFORE, ALL_ID_BEFORE]))
R4_HEADS = set(int(row['after']['address'], 16) for row in R4_PLAN['new_instruction_rows'])
CODE_RANGES = [pair for block in R4_PLAN['raw_blocks'] for pair in block['code_ranges']]
CODE_BYTES = set(value for lo, hi in CODE_RANGES for value in range(int(lo, 16), int(hi, 16)))
STATE_CONTRACTS = dict((int(row['address'], 16), row) for row in read_json('f16-seg5-fullstate-observation-plan-v1.json')['rows'])
SLOT_ROWS = [{'address': row['address'], 'action': row['action'], 'old_value': row['value'],
              'final_data_type': row['after']['data_at']['type'], 'final_eol': row['after']['eol']} for row in SLOT_PLAN['rows']]
SLOTS = dict((int(row['address'], 16), row) for row in SLOT_ROWS)
SLOT_CONTRACTS = dict((int(row['address'], 16), row) for row in SLOT_PLAN['rows'])
SOURCE_LABEL_ADDRESSES = set(value for value, row in SLOT_CONTRACTS.items()
    if row['action'] in ('REF_ADD', 'REF_PRESERVE', 'EQ_ADD') or value == int(R7_PLAN['base'], 16))
TARGET_MATERIALIZATIONS = set(int(address, 16) for address in PRIMITIVES['labels']) - SOURCE_LABEL_ADDRESSES
TARGET_CONTRACTS = dict((value, STATE_CONTRACTS[value]) for value in TARGET_MATERIALIZATIONS)
RENAMED_FUNCTIONS = dict((int(row['entry'], 16), row) for row in FUNCTION_PLAN['rows'] if row['before']['name'] != row['after']['name'])
FUNCTION_CONTRACTS = dict((int(row['entry'], 16), dict(row, action='RENAME_PLATE' if row['before']['name'] != row['after']['name'] else 'PLATE')) for row in FUNCTION_PLAN['rows'])
PLATES = dict((value, {'address': row['entry'], 'old_name': row['before']['name'], 'new_name': row['after']['name'],
    'old_plate': row['before']['plate'], 'new_plate': row['after']['plate'], 'action': 'FULL_REWRITE'}) for value, row in FUNCTION_CONTRACTS.items())
INSTRUCTION_EOLS = dict((int(address, 16), text) for address, text in PRIMITIVES['instruction_eol'].items())
ALL_EQUATE_NAMES = sorted(set(ROOT_FULL_PRESTATE['global_equates']) | set(NATIVE_AFTER['global_equates']))
EQUATE_NAMES = sorted(set(row['after']['equate_references'][0]['name'] for row in SLOT_PLAN['rows'] if row['action'] == 'EQ_ADD'))


PLAN_STATIC = {'input_hashes': {'doc/dev/refine/F16-Seg-5.plates.tsv': '061ba7037fbd3ea89df085a478eb7fc25403f56c48493d84afbe66672a6b10f2', 'doc/dev/refine/F16-Seg-5.proposal.md': '4f069a7d05817e6154459cb39c9be1a1ebd31ae60ba22a6b31a9bd39f4ccd29a', 'doc/dev/refine/F16-Seg-5.review.md': '6678f15ecd21443c0e2d53039be904d7f91308851343dc987ea61e81995b6e50', 'doc/dev/refine/F16-Seg-5.slots.tsv': 'a597aac9c1692a731dca32db4fa4342af8a3e15ed3c8c61b6b27667a8a7ef752', 'output/refine-run-20261028-105948/f15-readonly-scripts/F16ModuleIndependentQuery.java': '042c3c176a03341d0c7b6ae775086ae4308b27b6c3c0218daa917832b1951011', 'output/refine-run-20261028-105948/f15-readonly-scripts/F16Seg5CompleteTypedLabelClosureQueryV1.java': '651a69f1e87617596d249293b4361000a77a66ebe0f9199436f4625f7cc41af8', 'output/refine-run-20261028-105948/f15-readonly-scripts/F16Seg5ExpandedInstructionPropertiesQueryV2.java': '0af472743e1e5998d0d4c3e0c2f3960d1911ec6aaa45dbd2b9830184a65617e2', 'output/refine-run-20261028-105948/f15-readonly-scripts/F16Seg5PseudoDecodeQueryV1.java': 'e98684c6ef336e8c127fd42c7eace269ae3fe3645760c2c4099fdd86127b267b', 'output/refine-run-20261028-105948/f16-seg1-analysis-validator-v2.py': '5472177d1856c01db0f2b1fd6cce08bd9e0fb69d289bdb725ad053b3b42da768', 'output/refine-run-20261028-105948/f16-seg4-source-landing-pins-v1.json': 'e73dcebd0157c65d9ac9ce5f109199deb9d54f387375c224b82547c32ec09b80', 'output/refine-run-20261028-105948/f16-seg5-action-bases-draft-v1.json': '30ebe07c13cc92895056ce45e52d36ddeea0b66932b5f53681952d34230a0fe8', 'output/refine-run-20261028-105948/f16-seg5-analysis-source-v1.json': '8239a98d4a3d85f1b9e9d9933d8659865752df984060f48185057260ca405030', 'output/refine-run-20261028-105948/f16-seg5-before-ID-and-binding-contract-v1.json': '5272a6e2d231b111eec7464563d6d637f3b52213f9c32e85c9036e68112e0346', 'output/refine-run-20261028-105948/f16-seg5-decisions-v1.json': 'cb0d1baaa2edf5094e3eaf6a9d71ade20cd400891b695360aa18fe7c199f6633', 'output/refine-run-20261028-105948/f16-seg5-final-manifest-v1.json': 'cbf9e2591a0af6bed6a45fbc82747e0008b4a752a22e2ac9cd78ce050d20bb4f', 'output/refine-run-20261028-105948/f16-seg5-firststage-manifest-v1.json': '9b21b01b46a05d94e5a82ade09dfede839771646c116ce87a20564e672fdf69b', 'output/refine-run-20261028-105948/f16-seg5-fresh-canonical-verifier-v1.py': '71092a166513dd4946780f97b9e5d155b19e964e0129c83015d1df88bb2507f5', 'output/refine-run-20261028-105948/f16-seg5-full-function-observation-plan-v1.json': 'ff2e2167942388ec911d77e4325c33567fa519e651d42037eb060842d499a0f5', 'output/refine-run-20261028-105948/f16-seg5-full-rom-refscan-v1.json': '39fdbddc4eaa139afb7e5c7e7f23c347aeec8f9443cf411712ebec8199285722', 'output/refine-run-20261028-105948/f16-seg5-fullstate-observation-plan-v1.json': 'b87633702fd1458d50c38391b4c45e975162d0c3f911a820928990be1ed7ccb4', 'output/refine-run-20261028-105948/f16-seg5-function-plan-v1.json': 'e6cc8b2a7c0990ab8d6662eeaed07a62c7ff45580c6682e4fd3c659eaf8a8ea7', 'output/refine-run-20261028-105948/f16-seg5-gas-projections-v1.json': 'df3e91e480852ff95e182c05f043746fc1fdfc4cfd8476d6523fbd44a7f0a711', 'output/refine-run-20261028-105948/f16-seg5-global-equates-plan-v1.json': 'c50c41416fd90b06b00edf9f5a15c8402f7bb3e908b941d95d13c5eabc6a5688', 'output/refine-run-20261028-105948/f16-seg5-initial-cfg-v1.json': '259be8c05041c9f42120c45b731f2bdd7f73a0e81817a1f4660b87a5d7eb5c3e', 'output/refine-run-20261028-105948/f16-seg5-initial-full-rom-refscan-v1.json': 'ea4e937cc7540962209411810501a7957327eed4e7a9417b3e2fd6a342dc58c8', 'output/refine-run-20261028-105948/f16-seg5-inputs-v3.json': '5914ffbdbf9c3e739813dab76fc6b9ad8fec29b68fa956b3c1eccdb980ca285f', 'output/refine-run-20261028-105948/f16-seg5-instruction-properties-plan-v1.json': 'c7146ce723f9816daea186bd79fba3387534dad4c757bbf17eba7af34790497a', 'output/refine-run-20261028-105948/f16-seg5-label-closure-plan-v1.json': '3da758112a2815089efe47305a2c7833a12f495ad260d8a05461b6c364ace8ce', 'output/refine-run-20261028-105948/f16-seg5-name-reference-baseline-v1.json': 'be9c6abf29819f97893e289719314a70cbc1064b2633fd73e21ffa5154e25659', 'output/refine-run-20261028-105948/f16-seg5-native-collector-draft-v1.py': 'dce47471728601342ebc9361533987bef09fd76d17793b1ebdcde0518e11b379', 'output/refine-run-20261028-105948/f16-seg5-native-collector-fixtures-v1.py': 'd912b325b318ff87bc00797ede5c945f75dcc92538f9c1913e24b720acf6d734', 'output/refine-run-20261028-105948/f16-seg5-native-collector-preparation-v1.json': 'c7eda554500868ed7d6c57c42b15237c3fa21001ee0b5d32042fb9e7abce1c1e', 'output/refine-run-20261028-105948/f16-seg5-native-instruction-projection-v1.json': 'a8392723e62fc8354afa6126591720becd8d0af36a10e6035e0e7b85ae8b1e6b', 'output/refine-run-20261028-105948/f16-seg5-native-module-metadata-plan-v1.json': '8bb285735b107e8b77245d20b062b775cfec7211fefb09c3992a04bab9f58cb0', 'output/refine-run-20261028-105948/f16-seg5-native-query-full-observation-plan-v1.json': 'e770fbcb0e8bdea1c0bba8ff99ef2e1b4f2c7e8af7ceaae21b76da48877d65bb', 'output/refine-run-20261028-105948/f16-seg5-native-resolver-execution-v1.json': 'f22311625dea3aec658b9fd1cb6b3577a557e89fe48cb4909b059dde5d95192c', 'output/refine-run-20261028-105948/f16-seg5-negative-suite-v1.json': 'ed851ea2331e76052d15b2ba5d665c5a3da36e5d9f56e68ab39070172e56d245', 'output/refine-run-20261028-105948/f16-seg5-once-save-contract-v1.json': '5e0684b0bc4fdc8e1fb7b95973981cc4b15413cb714c274eb7caa99b52773676', 'output/refine-run-20261028-105948/f16-seg5-phase-table-boundary-correction-draft-v1.json': 'a408647b6ecc05d793dd34d444747d698fc41a915df9359f345c2be4d0ac3a06', 'output/refine-run-20261028-105948/f16-seg5-plates-final-v1.tsv': '061ba7037fbd3ea89df085a478eb7fc25403f56c48493d84afbe66672a6b10f2', 'output/refine-run-20261028-105948/f16-seg5-primary-symbol-plan-v1.json': '87a14ccb5e0245af80ff4fce134b18e4db475523422a141f757e103ef565b265', 'output/refine-run-20261028-105948/f16-seg5-primitives-v3.json': '40bc44a805f5f5c74dca2f97dbf29f7457ebb349d1ecb6d56d1d5f4ff438ea94', 'output/refine-run-20261028-105948/f16-seg5-proposal-final-v1.md': '4f069a7d05817e6154459cb39c9be1a1ebd31ae60ba22a6b31a9bd39f4ccd29a', 'output/refine-run-20261028-105948/f16-seg5-r4-plan-v1.json': '1c2813e31474b2d22a3d4da848c3f83b7f3ec3c2804b7b2968e74fe5d3695562', 'output/refine-run-20261028-105948/f16-seg5-r7-plan-v1.json': 'f46167d4167e0ae64226a73ba0dcd1762f2ce7d69447c7b922ef794878958c31', 'output/refine-run-20261028-105948/f16-seg5-registry-plan-v1.json': '5af1fbcd31568d40f8b479d4f22fd4b7f90c77d8cbc80cf6f47e25f4a4a11da2', 'output/refine-run-20261028-105948/f16-seg5-reviewer-audit-v1.json': 'ea38c31745c757dae28a5697704929c89f0ec6b9986f9b62b55ece5c3d62b2a8', 'output/refine-run-20261028-105948/f16-seg5-root-pure-preparation-review-v1.json': '183ba85a6363dbced8be73bcbefc730043e92ae967b3e59f5d0b7406887e8a5e', 'output/refine-run-20261028-105948/f16-seg5-selfcheck-v1.json': '1fde88604b5e631ffc345be47da33995089e4c9c8c36cdfda2a3363ec769103c', 'output/refine-run-20261028-105948/f16-seg5-semantic-plan-v1.json': '34201c528f2c27612257d91e1a80996197d937e70411c6bdeb8c181dd02dc8e9', 'output/refine-run-20261028-105948/f16-seg5-slot-plan-v1.json': 'fde2964d731576b7e5531ed07ac82e084242460c9daab35b7e6b4b86e4c8b73f', 'output/refine-run-20261028-105948/f16-seg5-slots-final-v1.tsv': 'a597aac9c1692a731dca32db4fa4342af8a3e15ed3c8c61b6b27667a8a7ef752', 'output/refine-run-20261028-105948/f16-seg5-source-scope-plan-v1.json': '70eab24032ea23d06c01e1c2208efb4c36b95497bd2be888f46e87b7c9f867f2', 'output/refine-run-20261028-105948/f16-seg5-stage2-manifest-draft-v1.json': '66a826ec20ea2e74cfc1a2e72998cef46d8b6eea93bde7637a212416938eac3f', 'output/refine-run-20261028-105948/f16-seg5-target-plan-v1.json': 'f9d49c5b43debb40e1364b97ebc2d8cc18df88c4c858ee706d3290367df4c8d0', 'output/refine-run-20261028-105948/root-f15-seg6-transaction-mechanism.json': '908138c1819efa2dc2df669a76926d4d8d9934f479829801b01d9d7038356480', 'output/refine-run-20261028-105948/root-f16-seg5-all-ID-before-gate-v1.json': 'abfe5dfd0647bc63f95e3fb19e53ffa15a47a7b5ebe49c2a32d06cc674685d76', 'output/refine-run-20261028-105948/root-f16-seg5-all-dynamic-symbol-IDs-before-v1.json': 'b071bd76650fd84d59f0ded5a62ce202ffa7c537c7253499d6c4092b3f2d9e03', 'output/refine-run-20261028-105948/root-f16-seg5-all-static-symbol-IDs-before-v1.json': 'b227b8ed7c9b76706765218c35bb6e6decf59e56ee18d981bfd178a144d7fe55', 'output/refine-run-20261028-105948/root-f16-seg5-collector-cross-schema-gate-v2.json': '3686f83a2b2dc0f67526bada7301bff214ed36a697344b06122e39428430f0c9', 'output/refine-run-20261028-105948/root-f16-seg5-db-backup.json': '3b6bd8a45ab3eb754c796693fb951f0031ab1d28501c96d70a06186f8ae1b71d', 'output/refine-run-20261028-105948/root-f16-seg5-expanded-equates-input-v4.json': '37517e5f3dc66819f61f5a7bb8ace1921282415f10551d2defa5c3eb0985b570', 'output/refine-run-20261028-105948/root-f16-seg5-expanded-functions-input-v4.json': 'fe8aaa51d9f3babc29b05ba10358660dcbcee03e0f24120f5d7358b180c4b603', 'output/refine-run-20261028-105948/root-f16-seg5-expanded-query-inputs-v4.json': 'af34a66ae5cf8cab85cccbc7856c87fd38517e9bd298f1f5e57f026fd2b2f822', 'output/refine-run-20261028-105948/root-f16-seg5-expanded-slots-input-v4.json': 'a707ff8c91229dee05422d138d96b68c6bb574788a7030c2c1f89b11679dc413', 'output/refine-run-20261028-105948/root-f16-seg5-expanded-words-input-v4.json': '2229cf77b9a96273a252b2e24608ef6e9704974e3a3918b13f70070984280933', 'output/refine-run-20261028-105948/root-f16-seg5-independent-prestate-v5.json': '6aab066769000c66e19de104496544d5e87319841df2085d09216af60183ff53', 'output/refine-run-20261028-105948/root-f16-seg5-independent-prestate-v5.json.db-gate.json': 'ae958ad9d22279d39ce20c370a3f151e40e89194849a11ec1b282dee459e96fb', 'output/refine-run-20261028-105948/root-f16-seg5-instruction-properties-before-v2.json': 'fa06848756a158b2ddef8f3ff79575bcebcb3e5c55b5118c06ab515e08a2b548', 'output/refine-run-20261028-105948/root-f16-seg5-instruction-properties-before-v2.json.db-gate.json': 'ae958ad9d22279d39ce20c370a3f151e40e89194849a11ec1b282dee459e96fb', 'output/refine-run-20261028-105948/root-f16-seg5-instruction-slot-input-v1.json': 'ddca3dc52444f1ed88061b767653d226edda7f96df00815fcc31f0b8680eea78', 'output/refine-run-20261028-105948/root-f16-seg5-label-closure-getter-preparation-v1.json': '16e80f021f942b0271ecf02346e0087fbe5fe28a85bda3366e85c5ba2702ce5e', 'output/refine-run-20261028-105948/root-f16-seg5-label-closure-seeds-v1.json': '165ba1c489b0264fa1e921905774f1144f442a4f28174440004383ede29cd793', 'output/refine-run-20261028-105948/root-f16-seg5-native-before-complete-v1.json': '6e1fbaf952604ff65efd9a418f4225fc6dabe589a4469fd69bfc4b43c57792c2', 'output/refine-run-20261028-105948/root-f16-seg5-native-supplement-preparation-v1.json': 'b9599a0bea15c8e1de17d59d94bf8f1655c474cf5a52fe8226f60bb222117317', 'output/refine-run-20261028-105948/root-f16-seg5-pseudo-decode-v1.json': '41bd895d1291fef6567b8ad04c0d1ac7f6eea46ca838a797f8cc88ca6391bbc1', 'output/refine-run-20261028-105948/root-f16-seg5-pseudo-decode-v1.json.db-gate.json': 'ae958ad9d22279d39ce20c370a3f151e40e89194849a11ec1b282dee459e96fb', 'output/refine-run-20261028-105948/root-f16-seg5-raw-instruction-heads-input-v1.json': '360470526efee8a9b0a3c53d18002f8bf786c87cfd9720a7b7c94f03759473f5', 'output/refine-run-20261028-105948/root-f16-seg5-typed-label-closure-before-v1.json': '26daa891d9d62de99c741b9909f73534f79abc7ee7496304a0178b6140f65766', 'output/refine-run-20261028-105948/root-f16-seg5-typed-label-closure-before-v1.json.db-gate.json': 'ae958ad9d22279d39ce20c370a3f151e40e89194849a11ec1b282dee459e96fb', 'output/refine-run-20261028-105948/root-source-baseline-f16seg5.json': '25c8767f34ac1f6a50f0e529f3e02affdc45d1a6eb55d418ca61a3e23c4c5695', 'output/refine-run-20261028-105948/root_query_f15_module_8g.ps1': '0913ef217a84e98edc8d1cd4cbc51acf5d909d551bbb82ae73d6d532f7c97b88', 'tools/asm-regen/ghidra/ExportRangeToGas.py': '4544a6a95f922f5a1779553555180ed2184955bc4fc1e92f96ad9b500ddaeb87'}, 'counts': {'EQ_ADD': 37, 'REF_ADD': 139, 'REF_PRESERVE': 4, 'CASE_VECTOR_PRESERVE_CORE': 62, 'R7_DATA_DEFINE': 7, 'R7_TYPE_PRESERVE': 1, 'SOURCE_LABEL': 181, 'SOURCE_EOL': 188, 'TARGET_LABEL': 152, 'DATA_REF_ADD': 139, 'FUNCTION_RENAME': 9, 'PLATE': 11, 'R4_TMODE_BYTES': 794, 'R4_DATA': 103, 'R4_CODE': 395, 'R4_BODY': 2, 'R4_CALL_RETURN': 0, 'R7_DWORD': 7}, 'contract_counts': {'analysis_records': 34, 'analysis_input_records': 17, 'producer_outputs': 26, 'functions': 137, 'states': 7295, 'slot_holders': 7218, 'module_words': 1755, 'target_states': 578, 'even_function_holders': 5, 'units': 43716, 'external_units': 48, 'instruction_properties': 20264, 'nullable_properties_before': 395, 'label_closure_rows': 2441, 'closure_seeds': 2119, 'label_closure_incoming_before': 211, 'label_closure_incoming_after': 532, 'baseline_files': 212, 'snapshot_files': 217, 'before_static_ids': 35925, 'before_dynamic_ids': 48035, 'before_all_ids': 83960, 'new_USER_ids': 333, 'global_before': 2494, 'global_after': 2503, 'bindings_before': 12766, 'bindings_after': 12803, 'new_raw_data': 103, 'new_r7_dwords': 7, 'R4_parents': 2}, 'segment': [135026628, 135031196], 'module': [135009352, 135053068], 'observer_function_count': 137, 'word_count': 1755, 'state_count': 7295, 'target_state_count': 578, 'external_unit_count': 48, 'bundle_fields': ['status', 'program_name', 'function_count', 'native', 'instruction_properties', 'label_closure'], 'evidence_version': 1, 'analysis_version': 1, 'analysis_manifest_name': 'f16-seg5-final-manifest-v1.json'}
PROOF_COUNTS = {'functions': 137, 'states': 7295, 'words': 1755, 'targetStates': 578, 'units': 43716, 'externalUnits': 48, 'sourceFiles': 217, 'instructionProperties': 20264, 'nullableInstructionPropertiesBefore': 395, 'labelClosureRows': 2441, 'labelClosureIncomingBefore': 211, 'labelClosureExpectedIncomingAfter': 532, 'beforeStaticIdentities': 35925, 'beforeDynamicIdentities': 48035, 'beforeAllIdentities': 83960, 'evenFunctionHolders': 5, 'r4InstructionHeads': 395, 'r4CodeBytes': 794, 'r4DataWords': 103, 'r4PaddingHalfwords': 9, 'r4ParentBodies': 2, 'r4Parent1BodyBytes': 1028, 'r4Parent2BodyBytes': 430, 'r4Parent1BodyRanges': 67, 'r4Parent2BodyRanges': 8, 'r4CallReturn': 0, 'r7NewDwords': 7}


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


def runtime_capture():
    result = capture()
    if result['status'] != 'F16_SEG5_READONLY_NATIVE_BUNDLE_DRAFT':
        raise RuntimeError('Frozen collector outer status')
    result['status'] = 'F16_SEG5_FRESH_FULL_PRESTATE'
    return result


def expected_before_bundle():
    return {'status': 'F16_SEG5_FRESH_FULL_PRESTATE', 'program_name': ROOT_FULL_PRESTATE['program_name'],
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
    if len(bindings) != 333 or len(set(bindings.values())) != 333:
        raise RuntimeError('333 new USER identities must be distinct')
    expected = {'status': 'F16_SEG5_FRESH_FULL_PRESTATE', 'program_name': ROOT_FULL_PRESTATE['program_name'],
                'function_count': ROOT_FULL_PRESTATE['function_count'], 'native': NATIVE_AFTER,
                'instruction_properties': PROPERTY_PLAN['after_document'], 'label_closure': LABEL_CLOSURE_PLAN['after']}
    return bind_dynamic(expected, bindings)


def verify_id_authorities():
    configure_scope(*(COLLECTOR_INPUTS + [STATIC_ID_BEFORE, ALL_ID_BEFORE]))


def verify_prestate(pre, recapture):
    metadata_assert('complete BEFORE bundle', pre, expected_before_bundle())
    if recapture:
        capture_before_inventory()
        metadata_assert('complete same-Program BEFORE recapture', runtime_capture(), pre)


def verify_post(pre):
    current = runtime_capture()
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
    if len(CODE_RANGES) != 69 or len(CODE_BYTES) != 794 or len(R4_HEADS) != 395 or R4_PLAN['flow_override_projections']:
        raise RuntimeError('R4 exact code mask/zero overrides')
    before_units = dict((int(row['address'], 16), row) for row in ROOT_FULL_PRESTATE['extra_units'])
    raw_values = set(value for block in R4_PLAN['raw_blocks'] for value in range(int(block['start'], 16), int(block['end'], 16)))
    if len(raw_values) != 1224:
        raise RuntimeError('R4 exact raw1224 bytes')
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
    command = DisassembleCommand(heads, make_address_set(CODE_RANGES), False)
    command.enableCodeAnalysis(False)
    if not command.applyTo(currentProgram, monitor):
        raise RuntimeError('R4 disassembly rejected: ' + str(command.getStatusMsg()))
    if address_set_values(command.getDisassembledAddressSet()) != CODE_BYTES:
        raise RuntimeError('R4 actual DisassembledAddressSet differs from794 mask')
    for row in R4_PLAN['new_instruction_rows']:
        value = int(row['after']['address'], 16)
        actual = instruction_property_row(value)['instruction']
        desired = row['after']['instruction']
        if actual is None or actual['length'] != desired['length']:
            raise RuntimeError('R4 incomplete instruction length %08x' % value)
        if any(pc not in CODE_BYTES for pc in range(value, value + actual['length'])):
            raise RuntimeError('R4 instruction crosses restricted code boundary')
        COUNTS['R4_CODE'] += 1
    consumed = set()
    for parent in R4_PLAN['parent_bodies']:
        entry = int(parent['entry'], 16)
        fn = functions.getFunctionAt(toAddr(entry))
        if fn is None:
            raise RuntimeError('R4 existing parent required')
        metadata_assert('R4 parent original body', body_ranges(fn), parent['before']['body_ranges'])
        body = AddressSet(fn.getBody())
        added = set()
        for row in R4_PLAN['new_instruction_rows']:
            owner = row['after']['function_containing']
            if owner is not None and int(owner['entry'], 16) == entry:
                head = int(row['after']['address'], 16)
                length = row['after']['instruction']['length']
                body.add(toAddr(head), toAddr(head + length - 1))
                added.update(range(head, head + length))
        approved = make_address_set(parent['after']['body_ranges'])
        if consumed & added or not added or address_set_values(body) != address_set_values(approved) or body.getNumAddresses() != parent['after']['body_size']:
            raise RuntimeError('R4 additive normalized parent body')
        consumed.update(added)
        fn.setBody(body)
        metadata_assert('R4 normalized parent ranges', body_ranges(fn), parent['after']['body_ranges'])
        COUNTS['R4_BODY'] += 1
    if consumed != CODE_BYTES:
        raise RuntimeError('Every new code byte must belong to exactly one approved parent')
    for value in R4_PLAN['padding_addresses']:
        at = toAddr(int(value, 16))
        if listing.getInstructionContaining(at) is not None or listing.getDefinedDataContaining(at) is not None or tmode_at(at) != 0:
            raise RuntimeError('R4 zero padding must remain NULL/context0')


def apply_r7():
    if len(R7_PLAN['rows']) != 8 or R7_PLAN['entry_refs_preserve_empty'] is not True:
        raise RuntimeError('R7 exact eight-cell contract')
    for row in R7_PLAN['rows']:
        value = int(row['address'], 16)
        at = toAddr(value)
        metadata_assert('R7 exact local BEFORE', native_state(value), row['before'])
        if list(references.getReferencesFrom(at)):
            raise RuntimeError('R7 entries must preserve exact empty refs')
        if value == int(R7_PLAN['base'], 16):
            if row['before']['data_at']['type'] != '/dword':
                raise RuntimeError('R7 base type preserve')
        else:
            if listing.getDefinedDataContaining(at) is not None:
                raise RuntimeError('R7 new dword requires NULL')
            data = listing.createData(at, DWordDataType.dataType, 4)
            if data is None or int(data.getLength()) != 4 or unicode(data.getDataType().getPathName()) != '/dword':
                raise RuntimeError('R7 DWordDataType contract')
            COUNTS['R7_DWORD'] += 1


def apply_instruction_eols():
    if INSTRUCTION_EOLS:
        raise RuntimeError('Seg5 has zero instruction EOL writes')


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
        elif action in ('R7_DATA_DEFINE', 'R7_TYPE_PRESERVE'):
            if exact_ref_cores(value):
                raise RuntimeError('R7 entries must retain zero references')
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

# -*- coding: ascii -*-
def verify_inputs():
    for relative, digest in sorted(INPUT_HASHES.items()):
        path = os.path.join(ROOT, relative)
        if file_hash(path) != digest:
            raise RuntimeError('Frozen input SHA changed: ' + relative)
    review = open(os.path.join(ROOT, 'doc/dev/refine/F16-Seg-5.review.md'), 'rb').read().decode('utf8')
    if re.findall(r'(?m)^## Reviewer Verdict: F16-Seg-5 = (.+)$', review) != ['PASS']:
        raise RuntimeError('Final independent analysis verdict must be exactly PASS')
    if len(RAW_SLOT_ROWS) != 250 or len(SLOT_ROWS) != 250 or len(SLOTS) != 250:
        raise RuntimeError('250 exact unique slot addresses')
    for formal, row in zip(RAW_SLOT_ROWS, SLOT_PLAN['rows']):
        for column, expected in (('address', row['address']), ('action', row['action']), ('value', row['value']), ('GAS', row['gas_expression_after'])):
            metadata_assert('formal slot ' + column, formal[column], expected)
        metadata_assert('formal slot before', json.loads(formal['before_json']), row['before'])
        metadata_assert('formal slot after', json.loads(formal['after_json']), row['after'])
    if len(RAW_PLATE_ROWS) != 11:
        raise RuntimeError('11 formal Function contracts')
    for formal, row in zip(RAW_PLATE_ROWS, FUNCTION_PLAN['rows']):
        metadata_assert('formal Function entry', formal['entry'], row['entry'])
        metadata_assert('formal Function before', json.loads(formal['before_function_json']), row['before'])
        metadata_assert('formal Function after', json.loads(formal['after_function_json']), row['after'])
    verify_id_authorities()
    if len(OBSERVER_FUNCTIONS) != 137 or len(set(OBSERVER_FUNCTIONS)) != 137 or len(STATE_CONTRACTS) != 7295 or len(WORD_REQUESTS) != 1755 or len(SLOT_REQUESTS) != 7218 or len(CLOSURE_SEEDS) != 2119:
        raise RuntimeError('Native exact observer scopes')
    if sum(row['even_function'] is not None for row in ROOT_FULL_PRESTATE['targets']) != 5:
        raise RuntimeError('Five complete even Function holders required')
    if len(SOURCE_LABEL_ADDRESSES) != 181 or len(TARGET_MATERIALIZATIONS) != 152 or len(RENAMED_FUNCTIONS) != 9 or len(PLATES) != 11:
        raise RuntimeError('Approved identity/comment action scopes')
    metadata_assert('complete property plan BEFORE', PROPERTY_PLAN['before_document'], PROPERTIES_BEFORE)
    for row in SLOT_PLAN['rows']:
        text = row['after']['eol']
        if row['action'] != 'CASE_VECTOR_PRESERVE_CORE' and (not isinstance(text, basestring) or not all(ord(char) < 128 for char in text)):
            raise RuntimeError('Slot EOL ASCII')
    for row in PLATES.values():
        if not isinstance(row['new_plate'], basestring) or not all(ord(char) < 128 for char in row['new_plate']):
            raise RuntimeError('Function PLATE ASCII')
    metadata_assert('Full holder BEFORE authority', ROOT_FULL_PRESTATE, read_json('root-f16-seg5-independent-prestate-v5.json'))
    metadata_assert('Tiny BEFORE authority', LABEL_CLOSURE_BEFORE, read_json('root-f16-seg5-typed-label-closure-before-v1.json'))
    snapshot = read_json(SNAPSHOT_NAME)
    if not strict_integer(snapshot.get('file_count'), 217) or not strict_integer(snapshot.get('baseline_file_count'), 212) or not strict_integer(snapshot.get('phase1_additions'), 5):
        raise RuntimeError('Source snapshot217 schema/count')
    baseline = read_json('root-source-baseline-f16seg5.json')
    additions = set(['tools/ghidra-labeling/RefineF16Seg5.py'] + ['doc/dev/refine/F16-Seg-5.' + suffix for suffix in ('proposal.md', 'review.md', 'slots.tsv', 'plates.tsv')])
    if len(baseline['files']) != 212 or set(snapshot['files']) != set(baseline['files']) | additions or snapshot['baseline_manifest'] != 'root-source-baseline-f16seg5.json' or snapshot['baseline_manifest_sha256'] != file_hash(os.path.join(RUN, 'root-source-baseline-f16seg5.json')):
        raise RuntimeError('Source snapshot217 membership/baseline')
    for relative, row in snapshot['files'].items():
        if not strict_sized_hash_row(row):
            raise RuntimeError('Source snapshot217 row schema')
        if relative in baseline['files']:
            metadata_assert('baseline source row', [row['size'], row['sha256']], [baseline['files'][relative]['size'], baseline['files'][relative]['sha256']])
        for base, expected in ((ROOT, row['sha256']), (os.path.join(ROOT, snapshot['snapshot_directory']), row['snapshot_sha256'])):
            path = os.path.join(base, relative)
            if os.path.getsize(path) != row['size'] or file_hash(path) != expected:
                raise RuntimeError('Source current/copy changed: ' + relative)


def proof_expected_values(fresh_hash):
    result = {'freshSha256': fresh_hash, 'scriptSha256': file_hash(getSourceFile().getAbsolutePath()),
              'snapshotSha256': file_hash(os.path.join(RUN, SNAPSHOT_NAME)),
              'freezeSha256': file_hash(os.path.join(RUN, 'f16-seg5-final-manifest-v1.json')),
              'canonicalSha256': file_hash(os.path.join(RUN, 'root-f16-seg5-independent-prestate-v5.json')),
              'verifierSha256': file_hash(os.path.join(RUN, 'f16-seg5-fresh-canonical-verifier-v1.py')),
              'instructionPropertiesSha256': file_hash(os.path.join(RUN, 'root-f16-seg5-instruction-properties-before-v2.json')),
              'labelClosurePlanSha256': file_hash(os.path.join(RUN, 'f16-seg5-label-closure-plan-v1.json')),
              'labelClosureBeforeSha256': file_hash(os.path.join(RUN, 'root-f16-seg5-typed-label-closure-before-v1.json')),
              'staticSymbolIdsBeforeSha256': file_hash(os.path.join(RUN, 'root-f16-seg5-all-static-symbol-IDs-before-v1.json')),
              'dynamicSymbolIdsBeforeSha256': file_hash(os.path.join(RUN, 'root-f16-seg5-all-dynamic-symbol-IDs-before-v1.json')),
              'allSymbolIdsCustodySha256': file_hash(os.path.join(RUN, 'root-f16-seg5-all-ID-before-gate-v1.json'))}
    result.update(PROOF_COUNTS)
    return result


def verify_plan(plan, prestate_hash):
    if plan.get('status') != 'F16_SEG5_PLAN_FROZEN':
        raise RuntimeError('Root frozen runtime plan required')
    for key, expected in PLAN_STATIC.items():
        metadata_assert('Root plan static ' + key, plan.get(key), expected)
    required = {'script_sha256': file_hash(getSourceFile().getAbsolutePath()),
                'prestate_sha256': prestate_hash, 'source_snapshot_manifest': SNAPSHOT_NAME,
                'source_snapshot_sha256': file_hash(os.path.join(RUN, SNAPSHOT_NAME)),
                'fresh_proof_sha256': file_hash(os.path.join(RUN, FRESH_PROOF_NAME)),
                'offline_selfcheck_sha256': file_hash(os.path.join(RUN, 'f16-seg5-phase1-v1-offline-selfcheck.json'))}
    for key, expected in required.items():
        metadata_assert('Root plan current ' + key, plan.get(key), expected)
    offline = read_json('f16-seg5-phase1-v1-offline-selfcheck.json')
    if offline.get('status') != 'F16_SEG5_PHASE1_V1_OFFLINE_SELFCHECK_PASS' or offline.get('script_sha256') != required['script_sha256']:
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
        'freeze_sha256': INPUT_HASHES['output/refine-run-20261028-105948/f16-seg5-final-manifest-v1.json'],
        'review_sha256': INPUT_HASHES['doc/dev/refine/F16-Seg-5.review.md'],
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
    result = runtime_capture()
    verify_prestate(result, False)
    write_json(PRESTATE_NAME, result)
    print('STATUS: OK PRESTATE native137 states7295 props20264 Tiny2441')
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
    write_json('f16-seg5-dry-%s.json' % EVIDENCE_VERSION, payload)
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
        tx = currentProgram.startTransaction('F16-Seg-5 approved materialization')
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
        apply_r7()
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
        write_json('f16-seg5-%s-%s.json' % (MODE, EVIDENCE_VERSION), payload)
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
        write_json('f16-seg5-%s-failure-%s.json' % (MODE, EVIDENCE_VERSION),
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
    write_json('f16-seg5-persisted-check-%s.json' % EVIDENCE_VERSION, payload)
    print('STATUS: OK CHECK FAIL=0')




