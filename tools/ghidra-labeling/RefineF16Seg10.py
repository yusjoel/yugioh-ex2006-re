# -*- coding: ascii -*-
#@runtime Jython
#@category Ygo-ex2006.Refine
# Seg10 approved symbols/comments only; no R4/R7/body/ABI/override. Root controls every native invocation.
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
PLAN_NAME='f16-seg10-plan-v1.json'
PRESTATE_NAME='f16-seg10-fresh-full-prestate-v1.json'
SNAPSHOT_NAME='f16-seg10-source-snapshot-preapply-v1.json'
FRESH_PROOF_NAME='f16-seg10-fresh-canonical-proof-v1.json'
AUTH_CONTRACT_NAME='f16-seg10-once-save-contract-v1.json'
GRANT_NAME='root-f16-seg10-implementation-gate.json'
ROOT_ATTEMPT_NAME='f16-seg10-apply-once-v1.json'
SCRIPT_CLAIM_NAME='f16-seg10-script-apply-claim-v1.json'
APPLY_RECEIPT_NAME='f16-seg10-apply-v1.json'
PHASE1A_MANIFEST_NAME='f16-seg10-phase1a-manifest-v1.json'
PHASE1_MANIFEST_NAME='f16-seg10-phase1-manifest-v1.json'
PHASE1_AUDIT_NAME='f16-seg10-phase1-static-review-v1.json'
FAILS=[]
is_lower_hex64=lambda value:isinstance(value,basestring) and re.match(r'^[0-9a-f]{64}$',value) is not None


INPUT_HASHES = {'output/refine-run-20261028-105948/f16-seg10-semantic-firststage-final-v2.json': 'ec2ea49b91b5bfdbbecbae33ce09d6160ff64435bb818620c382f2c8aa5ad14a', 'output/refine-run-20261028-105948/f16-seg10-mode-a-materialize-v2.py': 'a22979449f276990210e5fe51e41e1a5b944399b415d9283456a831c6602179b', 'output/refine-run-20261028-105948/f16-seg10-semantic-authoring-source-v2.json': '45548e591321f4925af32bda0e01cc1453b6d923d65b981bf66ef555f915ba84', 'output/refine-run-20261028-105948/f16-seg10-static-producer-source-v2.json': '6fe9e27687daa9d3fc03b0606f62b4746ea6bb8a45db16681b9e98a5405d77a7', 'output/refine-run-20261028-105948/f16-seg10-static-selfcheck-source-v2.json': '11638be9cf3d4daa8b02cd881a81c9c69e614098113fca1195186f2f99729f60', 'output/refine-run-20261028-105948/f16-seg10-semantic-primitives-v2.json': '42997527936d6dc1625b08c905fc364a2e2f55fb6ea6032b15341a8cbebf30d9', 'output/refine-run-20261028-105948/f16-seg10-static-selfcheck-v2.json': '99a760bc0a3169b7c82ba33a7d22c0f765b842bbcc69a0f50c80df72c0f5d60e', 'output/refine-run-20261028-105948/f16-seg10-deterministic-replay-v2.json': 'bcf87a148cf41998ed26d4ce43e9dbe2ab631e311e4493d033633c57a60d7f84', 'output/refine-run-20261028-105948/f16-seg10-mode-a-cas-v2.json': '1bc9a6054a0ed61b8b8c8c0c8aa91b134fce8808d44aec7798e50567cbc8c77d', 'output/refine-run-20261028-105948/f16-seg10-mode-a-minimal-diff-v2.json': 'd750e5eb8a8152dbe9b2f3ac8a3e6e1b45385ee760793602c21e1866edd0ec2e', 'output/refine-run-20261028-105948/f16-seg10-mode-a-future-registry-after-v2.json': '61e6dd116af4c62be9b0465624a7891276fc66f0a69a5f4178d26096bcc0ca81', 'doc/dev/refine/F16-Seg-10.proposal.md': '6f2baf4aca1fb5261145cb97bd560147179519eb957c650995ae605756e1ca1d', 'doc/dev/refine/F16-Seg-10.slots.tsv': 'e2c1ad1cf974f00af5007d405e5a334cab3c9853111fb9a531283084b23a1a61', 'doc/dev/refine/F16-Seg-10.plates.tsv': 'c1e8349c592d7a659b8773feb1c8570b9f99bd2a3cf26652756a8404d01b8a3b', 'output/refine-run-20261028-105948/f16-seg10-inventory-v1.json': '07b448a6ac0c71fd4253a8cde7dee144aa860de458ee018ada6976a6a4275c86', 'output/refine-run-20261028-105948/f16-seg10-static-call-edges-v1.json': 'c7d8c2001b0a178e9627a6f9c09cf111132a218d4dd322801c318c2b9a406052', 'output/refine-run-20261028-105948/f16-seg10-firststage-native-requests-v1.json': 'ebb5c48ad80719e61c39a529e8cde5e70300e9c13710a33417e26133ce23732f', 'output/refine-run-20261028-105948/f16-seg10-highreg-decode-v1.json': 'ba8a506bfcbb673476bf7d2292279d3e9a529c156fc0b104c31e9392f25461cd', 'output/refine-run-20261028-105948/f16-seg10-icon-source-view-v1.png': '30d50d35c35bea869c743a4ea12a6bb3e5f01764d25c9d1e76898585047b071d', 'output/refine-run-20261028-105948/f16-seg10-graphics-render-source-v1.json': '3509339f1763459f3fda2d56fd6de59ee557a5e15e0c4a9b838f0983c011b3e2', 'output/refine-run-20261028-105948/f16-seg10-consumer-evidence-v1.json': '9e0435651a23e389c2a39b32557d1ca43cc8dbd459e9c22d19072ee06d39afc0', 'output/refine-run-20261028-105948/f16-seg10-graphics-evidence-v1.json': 'dc90a5c8d32137d89592970754d64f929b57b4fcf13684d542c739e85740e014', 'output/refine-run-20261028-105948/f16-seg10-caller-callee-source-evidence-v1.json': '6aa07fc62492938a061656da25c82c10643ab37523d0fb6d091b7d6ca82c7b71', 'output/refine-run-20261028-105948/root-f16-seg10-semantic-v1-cas-archive-v1.json': '1dc3dbe1b1580b52d90b36ee8ef429f9cdda96339d6fa67a0c493bf0cd0fc3b7', 'output/refine-run-20261028-105948/f16-seg10-semantic-firststage-final-v1.json': 'bb11e4af0fa86a7ce0c4829c96dd5f96b1b0d7101fe00a8ad1c0eaab87f87a5d', 'output/refine-run-20261028-105948/f16-seg10-semantic-review-final-v1.json': 'c00bf9a936028b7db6da407feda3507e00f1efdf6e130b9c688724638f9c1c72', 'output/refine-run-20261028-105948/f16-seg10-semantic-review-final-v2.json': 'd8aa4a1a5490ba2e8f2da6394303a6b2ac3fe9314debbb724c22be591e16c810', 'output/refine-run-20261028-105948/f16-seg10-semantic-rereview-evidence-v2.json': '89684707caf569d4c5c74881fb9ce22b2802d9013b460b97238bced7c6160bcf', 'doc/dev/refine/F16-Seg-10.review.md': 'f516c0f70440c8da82a771aa7bdde606d9b6392aa187c422a41c34cb34c797ae', 'output/refine-run-20261028-105948/root-f16-seg10-semantic-v1-archive/output/refine-run-20261028-105948/f16-seg10-inventory-v1.json': '07b448a6ac0c71fd4253a8cde7dee144aa860de458ee018ada6976a6a4275c86', 'output/refine-run-20261028-105948/root-f16-seg10-semantic-v1-archive/output/refine-run-20261028-105948/f16-seg10-static-call-edges-v1.json': 'c7d8c2001b0a178e9627a6f9c09cf111132a218d4dd322801c318c2b9a406052', 'output/refine-run-20261028-105948/root-f16-seg10-semantic-v1-archive/output/refine-run-20261028-105948/f16-seg10-firststage-native-requests-v1.json': 'ebb5c48ad80719e61c39a529e8cde5e70300e9c13710a33417e26133ce23732f', 'output/refine-run-20261028-105948/root-f16-seg10-semantic-v1-archive/output/refine-run-20261028-105948/f16-seg10-highreg-decode-v1.json': 'ba8a506bfcbb673476bf7d2292279d3e9a529c156fc0b104c31e9392f25461cd', 'output/refine-run-20261028-105948/root-f16-seg10-semantic-v1-archive/output/refine-run-20261028-105948/f16-seg10-icon-source-view-v1.png': '30d50d35c35bea869c743a4ea12a6bb3e5f01764d25c9d1e76898585047b071d', 'output/refine-run-20261028-105948/root-f16-seg10-semantic-v1-archive/output/refine-run-20261028-105948/f16-seg10-graphics-render-source-v1.json': '3509339f1763459f3fda2d56fd6de59ee557a5e15e0c4a9b838f0983c011b3e2', 'output/refine-run-20261028-105948/root-f16-seg10-semantic-v1-archive/output/refine-run-20261028-105948/f16-seg10-consumer-evidence-v1.json': '9e0435651a23e389c2a39b32557d1ca43cc8dbd459e9c22d19072ee06d39afc0', 'output/refine-run-20261028-105948/root-f16-seg10-semantic-v1-archive/output/refine-run-20261028-105948/f16-seg10-graphics-evidence-v1.json': 'dc90a5c8d32137d89592970754d64f929b57b4fcf13684d542c739e85740e014', 'output/refine-run-20261028-105948/root-f16-seg10-semantic-v1-archive/output/refine-run-20261028-105948/f16-seg10-caller-callee-source-evidence-v1.json': '6aa07fc62492938a061656da25c82c10643ab37523d0fb6d091b7d6ca82c7b71', 'output/refine-run-20261028-105948/root-f16-seg10-semantic-v1-archive/output/refine-run-20261028-105948/f16-seg10-semantic-authoring-source-v1.json': '4473dcbeb44b1ff3146d466294d0c3d222c7558036d5e7a8cf3531dcf7367f44', 'output/refine-run-20261028-105948/root-f16-seg10-semantic-v1-archive/output/refine-run-20261028-105948/f16-seg10-static-producer-source-v1.json': 'c650a86e8ad1003e8f070053c85260724ba7b5e4858a6c19e09c2a505c3eb466', 'output/refine-run-20261028-105948/root-f16-seg10-semantic-v1-archive/output/refine-run-20261028-105948/f16-seg10-static-selfcheck-source-v1.json': '348c4cec1d20ee7f41a36ee5a3d43f4f7cd8103129f80aca723242373a78e224', 'output/refine-run-20261028-105948/root-f16-seg10-semantic-v1-archive/output/refine-run-20261028-105948/f16-seg10-semantic-primitives-v1.json': '7a417324d2bf1dfe1133232cda4f0b16ea4f31c3e0be81d3efac5609be8eafcf', 'output/refine-run-20261028-105948/root-f16-seg10-semantic-v1-archive/output/refine-run-20261028-105948/f16-seg10-static-selfcheck-v1.json': 'ce175f5fe86f8d8d3c3d5396becec4fee3ac737af7cdde0bb2e476d6adb9ce62', 'output/refine-run-20261028-105948/root-f16-seg10-semantic-v1-archive/output/refine-run-20261028-105948/f16-seg10-deterministic-replay-v1.json': 'e164d2c2caa44d68a97014873d3e190827e40fbc860e7289bf6e7b5618ac6978', 'output/refine-run-20261028-105948/root-f16-seg10-semantic-v1-archive/doc/dev/refine/F16-Seg-10.proposal.md': '559c8f4427c6228d09c256d9a650c120aff17f6a68cc22a8b1937b3ff341e2ee', 'output/refine-run-20261028-105948/root-f16-seg10-semantic-v1-archive/doc/dev/refine/F16-Seg-10.slots.tsv': 'e2c1ad1cf974f00af5007d405e5a334cab3c9853111fb9a531283084b23a1a61', 'output/refine-run-20261028-105948/root-f16-seg10-semantic-v1-archive/doc/dev/refine/F16-Seg-10.plates.tsv': '2c1eb3ba05ac109153106fe19d19383a387ad71c832f5c71134118b70a9232f7', 'output/refine-run-20261028-105948/root-f16-seg10-semantic-v1-archive/output/refine-run-20261028-105948/f16-seg10-semantic-firststage-final-v1.json': 'bb11e4af0fa86a7ce0c4829c96dd5f96b1b0d7101fe00a8ad1c0eaab87f87a5d', 'output/refine-run-20261028-105948/root-f16-seg10-semantic-v1-archive/doc/dev/refine/F16-Seg-10.review.md': 'b02ed29f39f2e78d9dd3bbfe86015aaad4d3700d8e2ee7d335f11e2e51ee8f36', 'output/refine-run-20261028-105948/root-f16-seg10-semantic-v1-archive/output/refine-run-20261028-105948/f16-seg10-semantic-review-structural-v1.json': '1fc96ebcffe802a70cc0bdc5404964db7c915473f0831c571ff0e180f950efe8', 'output/refine-run-20261028-105948/root-f16-seg10-semantic-v1-archive/output/refine-run-20261028-105948/f16-seg10-semantic-review-r8-v1.json': 'be0882bc56bb60463c30b11461ef912273c053c5ef1cd3b3cfadf03de52f4809', 'output/refine-run-20261028-105948/root-f16-seg10-semantic-v1-archive/output/refine-run-20261028-105948/f16-seg10-semantic-review-consumers-v1.json': '1dca70bbfdb0c6f40008aa15a6bab99e95305bf9e81918cf599f09a3e1fd5781', 'output/refine-run-20261028-105948/root-f16-seg10-semantic-v1-archive/output/refine-run-20261028-105948/root-f16-seg10-complete-before-v1.json': 'c0733eec160d3a453af5f55d8e332bb6321c6a69f00080778001fae0671e8628', 'output/refine-run-20261028-105948/root-f16-seg10-semantic-v1-archive/output/refine-run-20261028-105948/root-f16-seg10-instruction-eol-before-gate-v1.json': '251f0ffa602cc6b446221e54ffeeb81508a2e218b1cee9c0e1ccf9ca647ff4d4', 'output/refine-run-20261028-105948/root-f16-seg10-semantic-v1-archive/output/refine-run-20261028-105948/root-f16-seg10-native-collector-interop-gate-v1.json': 'c76d2345d8a8c8aeb42b2184a0012205442c42676a959b1eb00d032ebbca7c06', 'output/refine-run-20261028-105948/root-f16-seg10-semantic-v1-archive/roms/2343.gba': 'f405c620da05a817a5d63f45a4707b914260fb5802fe519b1e31bf050ba8f524', 'output/refine-run-20261028-105948/root-f16-seg10-semantic-v1-archive/asm/16_duelfield_zone.s': '62fbadb94b199188cc00d81dd8e69122c9d30ee3339d34931615110cc6f2366d', 'output/refine-run-20261028-105948/root-f16-seg10-semantic-v1-archive/asm/17_duelfield_pack_frame.s': '854585fd84c8419ca9217c40c21684cfd0942d869f46a13ef645787a6830656e', 'output/refine-run-20261028-105948/root-f16-seg10-semantic-v1-archive/asm/20_anim_jp_tileblit.s': '3b7d2be71c4ce0e174e0747c24ced3fe6b31e9adda89cc65aeddbdfc7d67729e', 'output/refine-run-20261028-105948/root-f16-seg10-semantic-v1-archive/asm/21_font_title_scene.s': 'b9d45c06729f0a85e30d96b2a9ba732a9ee92cb6ed8755caa373b4808dda2f97', 'output/refine-run-20261028-105948/root-f16-seg10-semantic-v1-archive/asm/rom.s': '9ccd4029a050da2345f748b89fdaeccb902ebb4520eabca832fa06dc3faebab2', 'output/refine-run-20261028-105948/root-f16-seg10-semantic-v1-archive/constants/gba_mem.inc': '82a778a0936b4dfd31da770897f4b4feda8b18f4b124216e13914e1be6978a47', 'output/refine-run-20261028-105948/root-f16-seg10-semantic-v1-archive/constants/card_info.inc': '86ca274f922e551cc65d8ebb8d9a2dcb7e282c7691110104c065adc7c9a0d274', 'output/refine-run-20261028-105948/root-f16-seg10-semantic-v1-archive/constants/duel_field.inc': 'f5a422133220f9f05a142d0e4d60fcdec894ae46bec1f753e60995376c873814', 'output/refine-run-20261028-105948/root-f16-seg10-semantic-v1-archive/constants/ewram.inc': 'c7b912afb99c7eea9a1d037770ec4214556a3f6d9147bd73d624ac60dadb3116', 'output/refine-run-20261028-105948/root-f16-seg10-semantic-v1-archive/constants/name_input.inc': '8fbd4ce3b8525c41d1ccca7b7551f99153fc1f7abf4a330bc77e61a2eee65142', 'output/refine-run-20261028-105948/root-f16-seg10-semantic-v1-archive/tools/ghidra-labeling/RenameKnownFunctions.py': '151f9ccaa016793f5b0e4b30d155ea4654d1696a9444c20071ac4b71657c0a9f', 'output/refine-run-20261028-105948/root-f16-seg10-semantic-v1-archive/tools/rom-export/export_card_data.py': 'f481e826773e79a10279588b4cf96b23934de8dfb8b0e55f04bc7e32b700c739', 'output/refine-run-20261028-105948/root-f16-seg10-complete-before-v1.json': 'c0733eec160d3a453af5f55d8e332bb6321c6a69f00080778001fae0671e8628', 'output/refine-run-20261028-105948/root-f16-seg10-native-before-v1.json': '09b397a9fedc1e1da2da7558ba50f28d4e409ca3ab8c54ed49510ee475f69686', 'output/refine-run-20261028-105948/root-f16-seg10-instruction-properties-before-v1.json': '6b6f4a8c68dbb6d91716fac9d33a010d9915dd822284b3eee854841701ff083d', 'output/refine-run-20261028-105948/root-f16-seg10-typed-label-closure-before-v1.json': 'de19e73210e2add62fb10ea8f43f37d32882b41823fa6653c58154bd051826f2', 'output/refine-run-20261028-105948/root-f16-seg10-native-before-v1.json.db-gate.json': '3f2b47a35e38a231a64340e9f4d70309d96ba52cbd7a864c63389e16c0ec3ad0', 'output/refine-run-20261028-105948/root-f16-seg10-instruction-properties-before-v1.json.db-gate.json': '3f2b47a35e38a231a64340e9f4d70309d96ba52cbd7a864c63389e16c0ec3ad0', 'output/refine-run-20261028-105948/root-f16-seg10-typed-label-closure-before-v1.json.db-gate.json': '3f2b47a35e38a231a64340e9f4d70309d96ba52cbd7a864c63389e16c0ec3ad0', 'output/refine-run-20261028-105948/root-f16-seg10-functions-input-v1.json': 'abf43fdf757113a14b8b36499cc27b127de87e9493d43bddf15edf3c3d29fc93', 'output/refine-run-20261028-105948/root-f16-seg10-words-input-v1.json': 'b33212bbcdb30e504368c862f1981f13dd4a5a2e6038d305864cdb5359360b42', 'output/refine-run-20261028-105948/root-f16-seg10-slots-input-v1.json': '2d52af94da3deca26a4b69bed2c7689e3a86f453e554a0d981894a14fd331f31', 'output/refine-run-20261028-105948/root-f16-seg10-equates-input-v1.json': '37517e5f3dc66819f61f5a7bb8ace1921282415f10551d2defa5c3eb0985b570', 'output/refine-run-20261028-105948/root-f16-seg10-property-instruction-seeds-v1.json': 'd77b752ddf52612f661d91deff941cfd2fb6c6d295723d587ad1027781752e74', 'output/refine-run-20261028-105948/root-f16-seg10-label-closure-seeds-v1.json': '8509a3200d7325260306a5917899025f3be0605d286739618eb1cb2baeb04ab4', 'output/refine-run-20261028-105948/root-source-baseline-f16seg10.json': '58b26a802dce9230f8de468b94b0bdc375cc5bed94b7921ff25b5a43092d1ead', 'output/refine-run-20261028-105948/root-f16-seg10-db-backup.json': 'fc4351891341a275356183491112b84a706b39f326673d0afec9d1d38cd32fc7', 'output/refine-run-20261028-105948/root-f16-seg10-all-ID-before-gate-v1.json': '37bd6269233332b9f483fd5a50d8d6af55a080bc57d8a2a86ad517a98328d5c9', 'output/refine-run-20261028-105948/root-f16-seg10-static-symbol-IDs-before-v1.json': '2e1057a33faf7307e3e2d42cabf6b286998fe08d4de00a4e56798671d0170895', 'output/refine-run-20261028-105948/root-f16-seg10-dynamic-symbol-IDs-before-v1.json': 'f21a6546165a42410847ba04ea5c3b955e5b1608b93088e6327b4d9aa99ea276', 'output/refine-run-20261028-105948/root-f16-seg10-resolved-scope-preparation-v1.json': '70061f5dadbaa0a6a32a583f78d53b1f576a6de2238d5ad3fd5b1c5b6b760834', 'output/refine-run-20261028-105948/root-f16-seg10-fresh-scope-and-defaults-v1.json': '28108cd32a425546022b1654de6d816cb4e1cc9cccad6e10499ff54fa48e6809', 'output/refine-run-20261028-105948/root-f16-seg10-preexisting-newlines-and-inventories-v1.json': '6736074a3fab1f10a77078e06f487470c54708f156955d39e79b6c958deb6bc6', 'output/refine-run-20261028-105948/root-f16-seg10-native-context-final-v1.json': '6bade24dcc758ef8efebb448638f3dee8859665d99c62e132227b17adcca4d55', 'output/refine-run-20261028-105948/root-f16-seg10-owner-expansion-v2.json': 'c44a09e54bbafea8c69fcb06601016851f8c77ee6ac13adac065ae7790474bec', 'output/refine-run-20261028-105948/root-f16-seg10-owner-expansion-v2.json.db-gate.json': '3f2b47a35e38a231a64340e9f4d70309d96ba52cbd7a864c63389e16c0ec3ad0', 'output/refine-run-20261028-105948/f16-seg6-readonly-scripts/F16ModuleIndependentQuery.java': '042c3c176a03341d0c7b6ae775086ae4308b27b6c3c0218daa917832b1951011', 'output/refine-run-20261028-105948/f16-seg6-readonly-scripts/F16Seg6InstructionPropertiesQuery.java': '2e0d45dd2903f63dd6a80ef85940aa0ffc9c2a2f9263e0724b6c35675c990765', 'output/refine-run-20261028-105948/f16-seg6-readonly-scripts/F16Seg6CompleteTypedLabelClosureQueryV3.java': 'fba276e02a2059d04fe0ac5c2009031acdd38fdf3898bc428dc301aafc418bb1', 'output/refine-run-20261028-105948/root-f16-seg10-native-collector-interop-gate-v1.json': 'c76d2345d8a8c8aeb42b2184a0012205442c42676a959b1eb00d032ebbca7c06', 'output/refine-run-20261028-105948/root-f16-seg10-native-collector-probe-v1.json': 'c7b06bd5efec754f3a25f64f79156d7ecc08c8a9dfafba2c104f4283089c309e', 'output/refine-run-20261028-105948/root-f16-seg10-native-collector-probe-v1.json.db-gate.json': '3f2b47a35e38a231a64340e9f4d70309d96ba52cbd7a864c63389e16c0ec3ad0', 'output/refine-run-20261028-105948/root-f16-seg10-collector-preparation-v1.json': 'd94730fd8fa5f5ea85c991afeb30428f611c54974db11fc0be8f418474376643', 'output/refine-run-20261028-105948/root_f16_seg10_native_collector_v1.py': 'cca0f681bf01693c768f3a8cebd42bf219483e93e6d8e5f2a3fe858b4e2868ee', 'output/refine-run-20261028-105948/root-f16-seg10-instruction-eol-before-gate-v1.json': '251f0ffa602cc6b446221e54ffeeb81508a2e218b1cee9c0e1ccf9ca647ff4d4', 'output/refine-run-20261028-105948/f16-seg10-semantic-primitives-v1.json': '7a417324d2bf1dfe1133232cda4f0b16ea4f31c3e0be81d3efac5609be8eafcf', 'output/refine-run-20261028-105948/f16-seg10-prospective-odd-symbols-v1.json': 'f41ef8ca8916ab670a14b26a19b38b51a94c24cf640126099243c950f0fb5a18', 'output/refine-run-20261028-105948/f16-seg10-empty-property-nullable-v1.json': '37517e5f3dc66819f61f5a7bb8ace1921282415f10551d2defa5c3eb0985b570', 'roms/2343.gba': 'f405c620da05a817a5d63f45a4707b914260fb5802fe519b1e31bf050ba8f524', 'output/refine-run-20261028-105948/f16-seg10-prepare-model-source-v1.py': 'dcbe890c701b870bbb333ce4e1adde2b3106ad22e3f69683786360c930d7c943', 'output/refine-run-20261028-105948/f16-seg10-post-model-v1.py': '1317cf83986bb8de616f97a4fa6a9d69f5611b0ea757853e6af0373fa012f9a1', 'output/refine-run-20261028-105948/f16-seg10-prepare-model-v1.py': 'd27c6ec671ffeb77bbd5f85d86151542c1e7a92f45a98a9700f81e22565d25eb', 'output/refine-run-20261028-105948/f16-seg10-mode-b-inputs-v1.json': '90a75ddda35e995e538ca9d50f028a1d0b140bb61446746ba0ba2441f9c69f18', 'output/refine-run-20261028-105948/f16-seg10-native-query-full-observation-plan-v1.json': 'c5dfcedf8c3fce73c07884dc2dc2750c3dc3efb61760618aa24fea8d8f45e8b3', 'output/refine-run-20261028-105948/f16-seg10-instruction-properties-plan-v1.json': 'db0cf06a76eca038e46c472cb9684e6531ac73c5713d988a1321baf8a8af008c', 'output/refine-run-20261028-105948/f16-seg10-label-closure-plan-v1.json': '48cf6e5cc0b2d418fb3407702581bd1c251104d5496189a6e7f0c7bd7ff070c8', 'output/refine-run-20261028-105948/f16-seg10-slot-plan-v1.json': '69fa771eccf99419a8ef480704221bfbacf29af3ff73f109a55624468bf0ee39', 'output/refine-run-20261028-105948/f16-seg10-function-plan-v1.json': '39075af656301d68d65d2e9c07f5d0c9ad40883a8902d5b1b9fb856390a63e28', 'output/refine-run-20261028-105948/f16-seg10-target-plan-v1.json': '91377d98b15fa1b42aba25f9f9367addb2dbcb44523f56c6df692a447f3cfc66', 'output/refine-run-20261028-105948/f16-seg10-model-static-generation-v1.json': '7c2c1b46f9b654c2f1bd92cd6d813a2ed050b250d0e77a5e32baf9ce716b2547', 'output/refine-run-20261028-105948/f16-seg10-model-fixtures-v1.py': 'ada714ce1ff425a5acd4e9c96e81e6b98974a24088ee1aaef837ca568d467e20', 'output/refine-run-20261028-105948/f16-seg10-model-fixtures-report-v1.json': '9e5aa0a3b7e48aed48efa557ad020b9ef3d753b5cbd0512a04dd8e1bc5ba82a1', 'output/refine-run-20261028-105948/f16-seg10-gas-projections-v1.json': '0a64a71051360c3436558442f306f6acae757b26bfcca1e547b130d04385418e', 'output/refine-run-20261028-105948/f16-seg10-registry-plan-v1.json': 'b3cc6ed545f9d66804664b0b2b9717d3bdc62f72eddabc76f92346ce7e4a2f2a', 'output/refine-run-20261028-105948/f16-seg10-source-scope-plan-v1.json': 'b5ed30d12b8d7c95be7905e5b1d3fff5ea0a2ad1b94c6d02304b79fa665d5bb5', 'output/refine-run-20261028-105948/f16-seg10-prepare-source-plan-source-v1.json': 'fecab90556c31af5ae0d86a0f55fa43c8ab4d833806917515613bf68c3065f6d', 'output/refine-run-20261028-105948/f16-seg10-source-plan-preparation-v1.json': '41a3ecc696b8b0a928783db80d17514888d00c8bc4ccd0af2a926d6bfa834041', 'output/refine-run-20261028-105948/f16-seg10-source-plan-selfcheck-source-v1.json': 'c2b4f3bfd27aafc429dc12f113ead1c03da6ff7c7eb3702b72073505b0a7b625', 'output/refine-run-20261028-105948/f16-seg10-source-plan-selfcheck-v1.json': 'ab18f78ea40e5ca09ed7d66306a2be05b8be283e4543a8d12575754607a13ae0', 'output/refine-run-20261028-105948/f16-seg10-model-partial-final-v1.json': '8a6fc2bcf6d409b5e8c1bf4af248b6823db40163469521a711c2751d8a64abaa', 'output/refine-run-20261028-105948/f16-seg10-source-plan-partial-final-v1.json': 'fae277c3f3ee7147c451fa998c1b7e76eeee60c38b0d63fac31c1a64d1d7cf3c', 'output/refine-run-20261028-105948/f16-seg10-once-save-contract-v1.json': '9148814e3be9f97b72045e90c98df3a7ce7cb89ac6f3a569f642cd609390ca74', 'output/refine-run-20261028-105948/f16-seg10-prepare-production-v1.py': '0801662d9277790f76a00437e5cbfc5b7407d4d995312215da77016b0b2fb64c'}
EXPECTED_COUNTS = {'EQ_ADD': 35, 'REF_ADD': 83, 'REF_PRESERVE': 26, 'CASE_VECTOR_PRESERVE_CORE': 29, 'SOURCE_LABEL': 144, 'SOURCE_EOL': 144, 'TARGET_LABEL': 11, 'DATA_REF_ADD': 83, 'FUNCTION_RENAME': 4, 'PLATE': 9, 'INSTRUCTION_EOL': 60}
COLLECTOR_INPUT_NAMES = ['root-f16-seg10-functions-input-v1.json', 'root-f16-seg10-words-input-v1.json', 'root-f16-seg10-slots-input-v1.json', 'root-f16-seg10-equates-input-v1.json', 'root-f16-seg10-property-instruction-seeds-v1.json', 'f16-seg10-empty-property-nullable-v1.json', 'root-f16-seg10-label-closure-seeds-v1.json']
AUTH_CONTRACT_SHA256 = '9148814e3be9f97b72045e90c98df3a7ce7cb89ac6f3a569f642cd609390ca74'
ANALYSIS_FREEZE_SHA256 = 'ec2ea49b91b5bfdbbecbae33ce09d6160ff64435bb818620c382f2c8aa5ad14a'
ANALYSIS_REVIEW_SHA256 = 'f516c0f70440c8da82a771aa7bdde606d9b6392aa187c422a41c34cb34c797ae'

# -*- coding: ascii -*-
# Seg8 callable getter-only scope. No Script entry point, transaction or writer.
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
    rows(function_requests, 274, 'Function requests')
    rows(word_requests, 1962, 'word requests')
    slots = rows(slot_requests, 4296, 'slot requests')
    rows(property_requests, 273, 'property requests')
    nullable = rows(nullable_property_heads, 0, 'nullable property heads')
    rows(closure_seeds, 4303, 'Tiny seeds')
    if type(segment_equates) is not list or segment_equates:
        raise RuntimeError('Exact empty segment-equate input')
    if static_id_authority.get('iteration_finished') is not True or all_id_authority.get('iteration_finished') is not True or all_id_authority.get('dynamic_ID_public_getter_verified') is not True:
        raise RuntimeError('Complete native BEFORE identity enumeration required')
    statics = static_id_authority['rows']
    if type(statics) is not list or len(statics) != 36851:
        raise RuntimeError('Complete36851 static authority rows')
    static_ids = []
    previous = 0
    for row in statics:
        if type(row) is not dict or set(row) != set(('id','address','name','qualified_name','type','source','dynamic','namespace_id')) or row['dynamic'] is not False or not integer(row['id']) or row['id'] <= previous:
            raise RuntimeError('Static identity DTO/type/order')
        static_ids.append(row['id'])
        previous = row['id']
    observed_static = all_id_authority['static_ids']
    if type(observed_static) is not list or len(observed_static) != 36851 or any(not integer(value) for value in observed_static) or observed_static != static_ids:
        raise RuntimeError('Independent native static identity lists disagree')
    expected_counts = {'iterated':84210,'static':36851,'dynamic':47359,'function_symbols':5414}
    counts = all_id_authority['counts']
    if type(counts) is not dict or set(counts) != set(expected_counts) or any(type(counts[key]) not in (int, long) or counts[key] != expected_counts[key] for key in expected_counts):
        raise RuntimeError('Strict complete84210 native identity counts')
    dynamics = all_id_authority['dynamic_rows']
    if type(dynamics) is not list or len(dynamics) != 47359:
        raise RuntimeError('Complete47359 dynamic authority rows')
    identities = set(static_ids)
    previous = 0
    for row in dynamics:
        if type(row) is not dict or set(row) != set(('id','address','type','source','dynamic','namespace_id')) or row['dynamic'] is not True or not integer(row['id']) or row['id'] <= previous or row['id'] in identities:
            raise RuntimeError('Dynamic identity DTO/type/order/disjointness')
        if type(row['namespace_id']) not in (int, long) or not 0 <= row['namespace_id'] < 2**63 or any(not isinstance(row[key], basestring) for key in ('address','type','source')):
            raise RuntimeError('Dynamic identity complete field types')
        identities.add(row['id'])
        previous = row['id']
    if len(identities) != 84210:
        raise RuntimeError('Complete84210 BEFORE identities')
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
        raise RuntimeError('Native complete84210 BEFORE identities changed')
    return len(identities)


def capture():
    return {'status': 'F16_SEG10_READONLY_NATIVE_BUNDLE_DRAFT', 'program_name': unicode(currentProgram.getName()),
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
            'output/refine-run-20261028-105948/f16-seg10-semantic-firststage-final-v2.json'],
        'analysis_review_sha256': INPUT_HASHES['doc/dev/refine/F16-Seg-10.review.md'],
        'canonical_sha256': file_hash(require_file(
            'root-f16-seg10-native-before-v1.json',
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
        'schema': 'F16_SEG10_ROOT_ONCE_SAVE_GATE_V2',
        'status': 'ROOT_F16_SEG10_IMPLEMENTATION_GATE_PASS',
        'segment': 'F16-Seg-10',
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
            'F16_SEG10_PHASE1_%s_COMPLETE' % EVIDENCE_VERSION.upper() or
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
        'segment': 'F16-Seg-10',
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
        'segment': 'F16-Seg-10',
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
        write_json('f16-seg10-%s-failures-%s.json' % (MODE, EVIDENCE_VERSION), {
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
ROOT_FULL_PRESTATE=artifact('root-f16-seg10-native-before-v1.json')
PROPERTIES_BEFORE=artifact('root-f16-seg10-instruction-properties-before-v1.json')
LABEL_CLOSURE_BEFORE=artifact('root-f16-seg10-typed-label-closure-before-v1.json')
PRIMITIVES=artifact('f16-seg10-semantic-primitives-v2.json')
SLOT_PLAN=artifact('f16-seg10-slot-plan-v1.json')
FUNCTION_PLAN=artifact('f16-seg10-function-plan-v1.json')
TARGET_PLAN=artifact('f16-seg10-target-plan-v1.json')
NATIVE_AFTER=artifact('f16-seg10-native-query-full-observation-plan-v1.json')['after']
PROPERTY_AFTER=artifact('f16-seg10-instruction-properties-plan-v1.json')['after']
LABEL_CLOSURE_AFTER=artifact('f16-seg10-label-closure-plan-v1.json')['after']
BINDING=artifact('f16-seg10-mode-b-inputs-v1.json')
EOL_BEFORE=artifact('root-f16-seg10-instruction-eol-before-gate-v1.json')
COLLECTOR_INPUTS=[artifact(name) for name in COLLECTOR_INPUT_NAMES]
STATIC_ID_BEFORE=artifact('root-f16-seg10-static-symbol-IDs-before-v1.json')
ALL_ID_BEFORE=artifact('root-f16-seg10-dynamic-symbol-IDs-before-v1.json')
ODD_BEFORE=artifact('f16-seg10-prospective-odd-symbols-v1.json')
FROZEN_ODD_IDS=set(long(x['prospective_dynamic_id']) for x in ODD_BEFORE['rows'])
functions=currentProgram.getFunctionManager();listing=currentProgram.getListing()
memory=currentProgram.getMemory();symbols=currentProgram.getSymbolTable()
references=currentProgram.getReferenceManager();equates=currentProgram.getEquateTable()
global_ns=currentProgram.getGlobalNamespace();tmode_register=currentProgram.getRegister('TMode')
bind_program(currentProgram,toAddr)
configure_scope(*(COLLECTOR_INPUTS+[STATIC_ID_BEFORE,ALL_ID_BEFORE]))
RAW_SLOT_ROWS=read_tsv(os.path.join(ROOT,'doc/dev/refine/F16-Seg-10.slots.tsv'))
RAW_PLATE_ROWS=read_tsv(os.path.join(ROOT,'doc/dev/refine/F16-Seg-10.plates.tsv'))
SLOT_CONTRACTS=dict((int(x['address'],16),x) for x in SLOT_PLAN['rows'])
SLOTS={}
for formal in RAW_SLOT_ROWS:
    value=int(formal['address'],16);contract=SLOT_CONTRACTS[value]
    row=dict(formal);row.update(action=contract['action'],old_value=contract['value'],final_data_type=contract['before']['data_at']['type'],final_eol=contract['after']['eol'])
    SLOTS[value]=row
SOURCE_LABEL_ADDRESSES=set(int(x['address'],16) for x in PRIMITIVES['words'] if x['slot_label'])
NEW_USER_LABELS=dict((x['address'],x['name']) for x in PRIMITIVES['primary_changes'] if x['role']!='Function')
# All11 approved targets have the mature no-target-EOL contract.
TARGET_MATERIALIZATIONS=set(int(x['address'],16) for x in PRIMITIVES['new_targets'])
TARGET_CONTRACTS=dict((int(x['address'],16),x) for x in TARGET_PLAN['rows'])
FUNCTION_CONTRACTS={};PLATES={};RENAMED_FUNCTIONS={}
for row in FUNCTION_PLAN['rows']:
    value=int(row['entry'],16);before=row['before'];after=row['after'];renamed=before['name']!=after['name']
    contract=dict(row);contract['action']='RENAME_PLATE' if renamed else 'PLATE';FUNCTION_CONTRACTS[value]=contract
    PLATES[value]=dict(action='FULL_REWRITE',old_name=before['name'],new_name=after['name'],old_plate=before['plate'],new_plate=after['plate'])
    if renamed:RENAMED_FUNCTIONS[value]=contract
INSTRUCTION_EOLS=dict((int(row['PC'],16),row['eol_after']) for row in PRIMITIVES['instruction_eol'])
COUNTS=dict((key,0) for key in EXPECTED_COUNTS)

def verify_inputs():
    for relative,digest in INPUT_HASHES.items():
        if file_hash(os.path.join(ROOT,relative))!=digest:raise RuntimeError('Frozen input '+relative)
    review=artifact('f16-seg10-semantic-review-final-v2.json')
    if review['status']!='PASS' or not strict_integer(review['finding_count'],0) or review['C1_C13']!=dict(('C'+str(i),'PASS') for i in range(1,14)):raise RuntimeError('Independent semantic PASS required')
    if (len(SLOTS),len(RAW_SLOT_ROWS),len(PLATES),len(RAW_PLATE_ROWS),len(NEW_USER_LABELS))!=(173,173,9,9,155):raise RuntimeError('Exact formal scope')
    for formal,row,primitive in zip(RAW_SLOT_ROWS,SLOT_PLAN['rows'],PRIMITIVES['words']):
        metadata_assert('formal slot address',formal['address'],row['address'])
        metadata_assert('formal slot value',int(formal['value'],0),primitive['value'])
        metadata_assert('formal slot kind',formal['kind'],primitive['kind'])
        metadata_assert('formal slot BEFORE',json.loads(formal['before_json']),row['before'])
    for formal,row in zip(RAW_PLATE_ROWS,FUNCTION_PLAN['rows']):
        metadata_assert('formal plate entry',formal['entry'],row['entry'])
        metadata_assert('formal plate BEFORE',json.loads(formal['before_full_Function_json']),row['before'])
        metadata_assert('formal plate setter',formal['plate_ASCII'],row['after']['plate'])
    if (len(RENAMED_FUNCTIONS),len(SOURCE_LABEL_ADDRESSES),len(TARGET_MATERIALIZATIONS),len(INSTRUCTION_EOLS))!=(4,144,11,60):raise RuntimeError('Action scopes')
    if EOL_BEFORE['status']!='ROOT_F16_SEG10_ACTUAL_INSTRUCTION_EOL_BEFORE_AUTHORITY_PASS' or EOL_BEFORE['null_is_not_inferred_from_missing_state'] is not True or EOL_BEFORE['actual_public_getter_full_Function_body_comment_coverage'] is not True:raise RuntimeError('Actual60 EOL authority required')
    metadata_assert('60 actual EOL before counts',EOL_BEFORE['counts'],dict(total=60,fullstate_crosscheck=15,complete_Function_comments_only=45,nonnull_rewrites=32,null_additions=28))
    if ODD_BEFORE['rows'] or ODD_BEFORE['count']!=0 or FROZEN_ODD_IDS or PRIMITIVES['DEFAULT_derivations']:raise RuntimeError('Seg10 has no odd/DEFAULT derivation actions')
    proofs=dict((int(x['PC'],16),x) for x in EOL_BEFORE['rows'])
    if set(proofs)!=set(INSTRUCTION_EOLS):raise RuntimeError('Exact60 instruction PC authority')
    bf=dict((int(f['entry'],16),f) for f in ROOT_FULL_PRESTATE['functions']);states={}
    for table,key in [('slots','state'),('words','state'),('targets','exact')]:
        for row in ROOT_FULL_PRESTATE[table]:states[int(row[key]['address'],16)]=row[key]
    fullstates=nonnull=0
    for x in PRIMITIVES['instruction_eol']:
        pc=int(x['PC'],16);f=bf[int(x['source_fn'],16)];proof=proofs[pc]
        if x['before_EOL_authority']!='complete Function-body non-null eol_comments traversal' or proof['source_fn']!=x['source_fn'] or proof['body_sha256']!=f['body_sha256'] or proof['instruction_property_present'] is not True or proof['after_ASCII']!=x['eol_after']:raise RuntimeError('Native60 EOL owner proof')
        if not any(int(lo,16)<=pc<int(hi,16) for lo,hi in f['body_ranges']):raise RuntimeError('EOL actual owner body')
        comments=dict((int(c['address'],16),c['text']) for c in f['eol_comments'])
        metadata_assert('actual original EOL',comments.get(pc),x['before_native_EOL']);metadata_assert('actual EOL gate',proof['before_native_EOL'],x['before_native_EOL'])
        present=pc in states
        if x['before_native_fullstate_present'] is not present or proof['fullstate_present'] is not present:raise RuntimeError('EOL state coverage proof')
        if present:metadata_assert('EOL fullstate before',states[pc]['eol'],x['before_native_EOL']);fullstates+=1
        if x['before_native_EOL'] is not None:nonnull+=1
    if fullstates!=15 or nonnull!=32 or len(PRIMITIVES['instruction_eol'])!=60:raise RuntimeError('Exact60 EOL:32rewrites28additions15states45Function-only')
    for text in list(INSTRUCTION_EOLS.values())+[x['new_plate'] for x in PLATES.values()]:
        if not isinstance(text,basestring) or not all(ord(x)<128 for x in text):raise RuntimeError('ASCII setter')
    if any(len(x['new_plate'])>500 for x in PLATES.values()):raise RuntimeError('PLATE length')
    snapshot=read_json(SNAPSHOT_NAME);baseline=artifact('root-source-baseline-f16seg10.json')
    additions=set(['tools/ghidra-labeling/RefineF16Seg10.py']+['doc/dev/refine/F16-Seg-10.'+suffix for suffix in ('proposal.md','review.md','slots.tsv','plates.tsv')])
    if snapshot['file_count']!=242 or set(snapshot['files'])!=set(baseline['files'])|additions:raise RuntimeError('source242 exact membership')
    for relative,row in snapshot['files'].items():
        for base,digest in [(ROOT,row['sha256']),(os.path.join(ROOT,snapshot['snapshot_directory']),row['snapshot_sha256'])]:
            path=os.path.join(base,relative)
            if os.path.getsize(path)!=row['size'] or file_hash(path)!=digest:raise RuntimeError('source242 live/copy drift '+relative)

def runtime_capture():return capture()
def expected_before_bundle():
    return dict(status='F16_SEG10_READONLY_NATIVE_BUNDLE_DRAFT',program_name=ROOT_FULL_PRESTATE['program_name'],function_count=ROOT_FULL_PRESTATE['function_count'],native=ROOT_FULL_PRESTATE,instruction_properties=PROPERTIES_BEFORE,label_closure=LABEL_CLOSURE_BEFORE)
def verify_prestate(pre,recapture):
    metadata_assert('complete BEFORE',pre,expected_before_bundle())
    if recapture:
        capture_before_inventory();metadata_assert('same Program BEFORE',runtime_capture(),pre)
def expected_post_bundle(current):
    observed={};planned={}
    for table,key in [('slots','state'),('words','state'),('targets','exact')]:
        for row in current['native'][table]:observed[int(row[key]['address'],16)]=row[key]
        for row in NATIVE_AFTER[table]:planned[int(row[key]['address'],16)]=row[key]
    bindings={}
    for address,name in NEW_USER_LABELS.items():
        value=int(address,16);symbol=observed[value]['primary_symbol'];identity=symbol['id']
        if not strict_integer(identity) or not 0<identity<2**63 or identity in ALL_BEFORE_IDS or identity in FROZEN_ODD_IDS:raise RuntimeError('New USER identity '+address)
        token='DYNAMIC_USER_ID:'+name;bindings[token]=identity
        metadata_assert('whole new USER '+address,symbol,bind_dynamic(planned[value]['primary_symbol'],{token:identity}))
    if len(bindings)!=155 or len(set(bindings.values()))!=155:raise RuntimeError('Distinct155 USER identities')
    result=expected_before_bundle();result.update(native=NATIVE_AFTER,instruction_properties=PROPERTY_AFTER,label_closure=LABEL_CLOSURE_AFTER)
    return bind_dynamic(result,bindings)
def verify_post(pre):
    current=runtime_capture();metadata_assert('complete POST',current,expected_post_bundle(current))
    if MODE in ('apply','fullrollback'):metadata_assert('exact action counts',COUNTS,EXPECTED_COUNTS)
    write_json('f16-seg10-'+MODE+'-complete-post-v1.json',current)
    return current
def apply_instruction_eols():
    for value,text in sorted(INSTRUCTION_EOLS.items()):
        if listing.getInstructionAt(toAddr(value)) is None:raise RuntimeError('Instruction EOL owner')
        listing.setComment(toAddr(value),CodeUnit.EOL_COMMENT,text);COUNTS['INSTRUCTION_EOL']+=1
def verify_plan(plan,prestate_hash):
    if plan.get('status')!='F16_SEG10_PLAN_FROZEN':raise RuntimeError('Frozen runtime plan required')
    required=dict(static_generation=1,runtime_evidence_version=EVIDENCE_VERSION,script_sha256=file_hash(getSourceFile().getAbsolutePath()),prestate_sha256=prestate_hash,source_snapshot_manifest=SNAPSHOT_NAME,source_snapshot_sha256=file_hash(os.path.join(RUN,SNAPSHOT_NAME)),fresh_proof_sha256=file_hash(os.path.join(RUN,FRESH_PROOF_NAME)),counts=EXPECTED_COUNTS,analysis_freeze_sha256=ANALYSIS_FREEZE_SHA256,analysis_review_sha256=ANALYSIS_REVIEW_SHA256)
    metadata_assert('exact runtime plan',plan,dict(required,status='F16_SEG10_PLAN_FROZEN'))
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
        if value in SOURCE_LABEL_ADDRESSES:
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
        'freeze_sha256': INPUT_HASHES['output/refine-run-20261028-105948/f16-seg10-semantic-firststage-final-v2.json'],
        'review_sha256': INPUT_HASHES['doc/dev/refine/F16-Seg-10.review.md'],
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
    print('STATUS: OK PRESTATE native274 states4650 props39103 Tiny19409')
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
    write_json('f16-seg10-dry-%s.json' % EVIDENCE_VERSION, payload)
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
        tx = currentProgram.startTransaction('F16-Seg-10 approved materialization')
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
        write_json('f16-seg10-%s-%s.json' % (MODE, EVIDENCE_VERSION), payload)
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
        write_json('f16-seg10-%s-failure-%s.json' % (MODE, EVIDENCE_VERSION),
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
    write_json('f16-seg10-persisted-check-%s.json' % EVIDENCE_VERSION, payload)
    print('STATUS: OK CHECK FAIL=0')




