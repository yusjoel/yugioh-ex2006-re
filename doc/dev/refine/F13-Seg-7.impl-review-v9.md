# F13-Seg-7 Implementation Review v9

## 结论与授权版本

- 审查范围：retry6 写后 scope 失败及恢复、新版 source-scope 的真实 Exporter 行合同、28 字段事故链，以及 F13-Seg-7 Mode B 全流水线回归。
- **v1 至 v8 的 real apply 执行授权全部作废。** v8 的 PASS 已被 retry6 写后 `SUFFIX_NORMALIZATION_PADDING_MISMATCH` 消耗；本文是当前唯一 implementation review 执行判定。
- 本 reviewer 仅执行只读检查与隔离 fixture/runtime 测试，final checker 的报告写入被重定向到内存。没有执行 real apply、export、build、stage、commit，也没有改动 Ghidra DB、正式 source、冻结语义文件或生产实现。

## retry6 事故与完整恢复

| 阶段 | 结果 | 独立证据 |
|---|---|---|
| apply | PASS | `f13-seg7-apply-headless.log` 含 transaction committed 与 `Save succeeded`；SHA256=`1ef73b616d99d5549fe42c3a916ee2ff55762ca4ce5139d0eb2f6470fb012976`。 |
| persisted | PASS | fresh check 含 `PERSISTED_EXACT=true`；SHA256=`1ec16eaf39e66bd82b3e0f2d3004cb95a44bf0e481a99672313b56971fee262b`。 |
| export/source edits/inventory | PASS | Ghidra export log SHA256=`4a3a0040592c6ba301f56c9c54daadcd7f1f3fb0ad3030182d8395fbf30f32b9`；inventory export log SHA256=`273b823a720c28dbaddbccb5a61d27e894909139a8d8b69e8210712f4a706438`，总数为 5213/5123/90。export wrapper 仅在 inventory checker exit=0 后进入 source scope。 |
| 失败点 | 已确认 | 旧 checker SHA256=`dca38d440cb0e41af94c843453a40b9d796c0b060b7867977e8e1f6c8173bd75` 只反向替换 new symbol，保留了 rename 后由 `%-40s` 产生的 padding，故全文归一化比较触发 `SUFFIX_NORMALIZATION_PADDING_MISMATCH`。 |
| 后续阶段 | 未执行 | export_all、build、document updater、landing 均位于失败点之后。 |
| restore | PASS | `f13-seg7-retry6-recovery.json` 为 `F13_SEG7_RETRY6_RECOVERY_PASS`、`FAIL=0`；当前 DB=backup 15/15 path/size/SHA exact，source 70/70 mismatch=0，两正式文档 exact，fresh `-noanalysis -readOnly` 前态 PASS，authority=0、staged=0。 |

恢复 checker 与 evidence 的 SHA256 分别为
`001f984c05a3cbe46f8a4e9467b478039d3f5e45ac4f4f5c38479aec45c03559`、
`d0fb1a6e49859f35bd6c57d55e97316d28a42a27718776f284a7b2896e2e55b6`。
恢复记录还明确给出 `retry9_additional_real_apply=false`，没有遗留任何 authority 输出。

## 真实 Exporter 行合同与七条 BL 投影

审查者没有采用 checker 的硬编码结果。独立读取冻结 plan 的 9 个 `renames[]` 及每个 `pre.incoming[]`，以 `UNCONDITIONAL_CALL`、source 地址和 rename entry 重建投影，再逐地址核 baseline 与 ROM opcode。正式 Seg-8 区间为 `[0x080a46a0,0x080a585c)`，结果恰好为以下七条；`0x080a585c` 之后至模块末尾没有额外 incoming rename 投影。

Exporter 在 `tools/asm-regen/ghidra/ExportRangeToGas.py:911` 使用 `"    %-40s %s%s\n"`。retry6 的真实 export spacing 与该格式逐字一致：固定四个 ASCII 空格缩进、`bl`、callee、至少一个 ASCII padding、`@`、八位小写地址及八位小写 opcode，行尾没有额外 token/comment。

| BL 地址 | baseline old | retry6/future new | target | padding | opcode / ROM bytes |
|---|---|---|---|---:|---|
| `0x080a49e4` | `check_equip_slot_has_field_spell_target` | `check_necroshade_normal_summon_available` | `0x080a4574` | 1 | `fff7c6fd` |
| `0x080a504e` | `check_equip_set_activatable_for_player` | `check_gate_guardian_summon_allowed` | `0x080a3dac` | 4 | `fef7adfe` |
| `0x080a5056` | `eval_equip_card_placeable_for_player` | `check_valkyrion_summon_allowed` | `0x080a3eb4` | 8 | `fef72dff` |
| `0x080a5060` | `eval_spell_card_activation_placeable` | `check_special_summon_material_rule_satisfied` | `0x080a42b0` | 1 | `fff726f9` |
| `0x080a50a0` | `check_banisher_of_light_activatable` | `check_banisher_sensitive_summon_allowed` | `0x080a3c2c` | 1 | `fef7c4fd` |
| `0x080a50aa` | `check_banisher_pair_activation_allowed` | `check_neo_bubbleman_summon_allowed` | `0x080a3d74` | 4 | `fef763fe` |
| `0x080a50d2` | `check_ritual_fusion_pairable_slots_exist` | `check_fusion_material_pair_slots_exist` | `0x080a4134` | 1 | `fff72ff8` |

七条均满足：plan edge target=`renames[].entry`；baseline old/current new、地址、mnemonic、opcode 各字段精确；opcode 与 ROM 对应四字节相等；地址唯一。没有第八条投影。

新版 `f13-seg7-source-scope.py` SHA256=`59a75f69bb2f47a7de1366009c57399ea7bd74f53c8cac3f645c49e6acf83ead`。其 `BL_LINE.fullmatch` 强制上述行结构；字段验证完成后以整条 `baseline_line` 替换 current projection 行，再比较从 `0x080a46a0` 到 `asm/13_equip_placement.s` 末尾的全文。因此符号长度引起的合法 padding 变化被完整归一化，同时任何投影外变化仍会失败。

测试源 `test_f13_seg7_source_scope.py` SHA256=`cf1960cb29503528aad71aa817c460f700b3f1d9693f20cf1987d3af220dbb68`。隔离重跑结果：

- 正例 1 使用 retry6 七条真实 Exporter 行；正例 2 使用等价 ASCII padding；两者均为 `projectionCount=7`、plan/baseline/opcode/normalized suffix exact。
- 15/15 负例按预期 code 拒绝：缺投影、错 new、错 baseline old、错地址、错 opcode、错 mnemonic、tab padding、额外 token、额外 comment、重复地址、额外 suffix comment、未批准 suffix 行变化、缺 plan edge、错 target、额外 plan edge。
- fixture-only、persistent writes=false、real apply=false；临时目录已清理。重跑 evidence 字节 SHA256=`5fc6264a8b30bd0c102cabbbfb084bdfe9b1376fb0e937132505b0e7f07508ef`。

## 28 字段事故链与文档接线

生产 document updater 与 landing checker 使用同一组 28 个唯一字段：

- retry1：PowerShell lexical failure，restore COMPLETE；
- retry2：apply/persisted SUCCESS，inventory schema `KeyError`，restore COMPLETE；
- retry3：坏 Seg-8 边界导致 PREWRITE 拒绝，Ghidra/source write 均 NONE，restore NOT_REQUIRED；
- retry4：65 字符 proposal SHA 导致 PREWRITE 拒绝，Ghidra/source write 均 NONE，恢复态 COMPLETE；
- retry5：apply/persisted/source edits/inventory SUCCESS，suffix scope overstrict，restore COMPLETE；
- retry6：apply/persisted/source edits/inventory SUCCESS，`SUFFIX_NORMALIZATION_PADDING_MISMATCH`，restore COMPLETE；
- retry7：`FINAL_SUCCESS`，landing `PASS`。

记录还唯一包含 `§5.1=0` 和下一任务 `F13-Seg-8 [0x080a46a0,0x080a585c)`。parser 要求 key 唯一、大小写和值 exact，并拒绝 retry3/retry4/retry5/retry6 的旧成功记录，尤其拒绝 retry6 `FINAL_SUCCESS`/landing `PASS`。

生产 updater SHA256=`dbc76c0c284370772cd659ffb04ce98b014704c1ef193a65200f5c5d8007984d`；landing checker SHA256=`3fb6a8d0e9cb4170511a7ffa710980b780a8dbf0005f2c05c775052cacfdb086`。以真实当前两文档的隔离副本运行生产 updater：第一次 changed 且 landing 合同 PASS，第二次幂等；77/77 文档合同负例和 5/5 双文件事务失败路线全部通过，正式文档字节未变。

## v9 回归矩阵

| # | 检查 | 结果 | 独立证据 |
|---|---|---|---|
| V1 | source scope | PASS | 两个正例；15/15 负例；真实 retry6 spacing、七行字段、ROM opcode、整行 baseline 归一化与 suffix 全文均 exact。 |
| V2 | landing | PASS | 正例 failures=[]；77/77 负例；28 字段事故链、`§5.1=0` 与 next=`[0x080a46a0,0x080a585c)` exact。 |
| V3 | document updater | PASS | 真实两文档投影、二次幂等、77/77 合同负例、5/5 事务失败路线；正式文档不变。 |
| V4 | wrapper 词法/AST/receipt/layout/wiring | PASS | 9 个 run wrapper compressed/collision/AST 均 0；receipt exact integer、DB generation layout、scope selftest、document 与 landing wiring、restore route 均通过。 |
| V5 | runtime 失败路线 | PASS | 28/28；3 个 prewrite restore=0，25 个 postwrite restore=1；CommandNotFound=0，real apply=false。 |
| V6 | inventory | PASS | 5213/5123/90、9 rename；15/15 负例；错误 schema access=0，fixture 已清理。 |
| V7 | static hash contract | PASS | 194 条生产声明均为恰好 64 个字符，且每字符仅为 `0-9` 或 `a-f`；目标唯一、实算 exact；70 snapshot exact；7/7 负例。 |
| V8 | fresh dry | PASS | `semantic_actions_applied=false`，动作计数 exact；readOnly/noanalysis，DB before/after exact，source 70/70，两文档 baseline exact。 |
| V9 | retry6 恢复前态 | PASS | DB=backup 15/15 exact；source 70 rows/70 unique、mismatch=0；docs exact；authority=0；staged=0。 |
| V10 | final checker | PASS | 生产报告写入重定向到内存后读取真实 repo 重跑：exit=0、`FAIL=0`；按 Windows `Path.write_text` 的 CRLF 字节序列与正式 gate exact，SHA256=`eca9e42570527e8bd1048f223577cb2b15ce6687d6ae3691a62e1dd84b5f445d`。 |

## v9 冻结 hash

### 语义与核心输入

| artifact | SHA256 |
|---|---|
| `F13-Seg-7.proposal.md` | `129f42778a7ed9da2ec4e082da91d71577532e56016d4f2cb394e797a8d63a99` |
| `F13-Seg-7.review.md` | `80fbd95458a16cb7faea369ff2051905b1b4cf6f8e5ebab9fb022ded0f60b926` |
| `F13-Seg-7.slots.tsv` | `2bd2619525cf56f5a996a2c8eb4dd91161958b1e825906d91e680e690221a99f` |
| `F13-Seg-7.impl-review-v8.md` | `122dd84ca75b29417287daecf6bd2e5938ae068033375bafa72ae39264f8f950` |
| `f13-seg7-plan.json` | `772b89fab666c9ad09516aff6e3e8c3a3984db91d393cef99ede87e425edbe6b` |
| `RefineF13Seg7.py` | `3c446203ce84dabc92cb4cb5dbdabe422aa8ea497d7bb0a05db6269e0f368b28` |
| `f13-seg7-source-baseline.json` | `a8e6419d64ba52bdbf70aff62f750303091e6298daa6a24af33db24301c90fd3` |
| `f13-seg7-preapply-backup.json` | `3f2b848200de1bd02c4e9c97d3b44c6c62264a0958b72b7a3b2649cc8f03aac6` |

### 生产实现

| artifact | SHA256 |
|---|---|
| `run_f13_seg7_restore.ps1` | `6ff3cb2866373f57d10d2b51259bbc854aea05216ca22cf38943a6423bb23da6` |
| `run_f13_seg7_dry_gate.ps1` | `6bece91563fd3b70004c56cf89f8b460c05672feb84e8ff826d858e49f7e10ce` |
| `run_f13_seg7_apply_gate.ps1` | `90cdcca8572edcc1a9ceaabf2f350e5f2ffd2800771ae8d6a832b1998cf78c85` |
| `run_f13_seg7_persisted_gate.ps1` | `0086fcf0184214f459352e55fddd87a2a99f9e6018cb03811aac1b9c057838ad` |
| `run_f13_seg7_export_build_gate.ps1` | `23bca74035ef216cbf71dc9b9f84304ee9390bc8d83bdd04a2e51d3d61ad52e4` |
| `run_f13_seg7_source_scope_gate.ps1` | `706fd515c9b5108235224dd5896b042fbaaa5607581215b000d3d2d5ffe591b0` |
| `run_f13_seg7_landing_gate.ps1` | `4738ad05a737baa5a6e8d1b4173b4a82bcb70dd71195152561d92656a47e852e` |
| `run_f13_seg7_full_prestate_gate.ps1` | `193c4365b5fca823a5bc2cd44490d0c573f223b61a292e8a6318ec1849685191` |
| `run_f13_seg7_modea_prestate.ps1` | `3e2f418912d0bf40eb62f4f25f5e70ed4a87332bf4de27cd858442224adb6e28` |
| `test_f13_seg7_wrapper_validators.ps1` | `24727885ba536d435d69906797f98201d2a4527fa89717ac6e0baef9d3f78c04` |
| `test_f13_seg7_runtime_failure_paths.ps1` | `387c394b77e76513ebe6342c5b96490e913374cb3bb29277abbea64b66ee9f16` |
| `test_f13_seg7_hash_contract.py` | `c00aa3c41aafaa7622b08113fff264dfbfe5c26a8e4504626cff67793c47d501` |
| `test_f13_seg7_inventory_checker.py` | `7f09c911ef89cadfdfea3b825e3d4c61ec88b87f9c8f1011ab146ca21300420a` |
| `test_f13_seg7_source_scope.py` | `cf1960cb29503528aad71aa817c460f700b3f1d9693f20cf1987d3af220dbb68` |
| `test_f13_seg7_landing_checker.py` | `21647d8c43fe9008c29a5ce84e808002c66fb5d426198ce1cbe028412257c3de` |
| `test_f13_seg7_document_editor.py` | `ff058fac9304762107f2b641f126717f6ce0d80493b3e5ccaa4cc347de99fc1e` |
| `check_f13_seg7_retry2_recovery.py` | `23b10e7c1541b6e9fb1645f32d3c4e95f4ca489b4bfe199e6b1927b2d4afa714` |
| `check_f13_seg7_retry3_recovery.py` | `cd0c0f293b86afc7b10a1ff02811000f2b115824cb9e7e09436e4679a9327951` |
| `check_f13_seg7_retry4_prewrite.py` | `e3b6e583ce58c67315e516ac070fc5268987292cf5ab7b8446a54b6bf8d909d7` |
| `check_f13_seg7_retry5_recovery.py` | `05b861a06eacba76be0dc5f1f72c645127272407b41a30cacd3cfae758c97417` |
| `check_f13_seg7_retry6_recovery.py` | `001f984c05a3cbe46f8a4e9467b478039d3f5e45ac4f4f5c38479aec45c03559` |
| `apply_f13_seg7_document_updates.py` | `dbc76c0c284370772cd659ffb04ce98b014704c1ef193a65200f5c5d8007984d` |
| `apply_f13_seg7_source_edits.py` | `6f3def4a382e8b101c8876735f77ede31978ca39fbb3de6908a3d2506af6801c` |
| `f13-seg7-normalize-split.py` | `3950581c7cad1f2499fd3267a3916912b65c906a2c2e39a50afae4ab85c3fd9f` |
| `f13-seg7-source-scope.py` | `59a75f69bb2f47a7de1366009c57399ea7bd74f53c8cac3f645c49e6acf83ead` |
| `f13-seg7-inventory-check.py` | `f44bbe33ddafce19b1cc48425c8d52c39db34b631c05c66407837a6f72098b0b` |
| `f13-seg7-verify-rom.py` | `e4818ab261bd06ec322d393947319dcb88e3d267cfe965fa051d7c1fa5215449` |
| `check_f13_seg7_landing.py` | `3fb6a8d0e9cb4170511a7ffa710980b780a8dbf0005f2c05c775052cacfdb086` |

以上 28 个 production artifact 的实算 hash 均与 final checker 冻结值一致。final checker 自身 SHA256=`0cec861c6ce8ab4983f683f12963977833b5540a592600c449ee79367a48ac7d`。

### v9 关键证据

| evidence | SHA256 |
|---|---|
| `f13-seg7-retry6-recovery.json` | `d0fb1a6e49859f35bd6c57d55e97316d28a42a27718776f284a7b2896e2e55b6` |
| `f13-seg7-source-scope-test.json` | `5fc6264a8b30bd0c102cabbbfb084bdfe9b1376fb0e937132505b0e7f07508ef` |
| `f13-seg7-landing-checker-test.json` | `f5cd071ec63e47e9497f4e138f10d8a66f40b8db5cf527fc53ea7b07b9d03784` |
| `f13-seg7-document-editor-test.json` | `fbf302e993371a0ccd694563b621188f23b33bb34671dd95f9b5f299fd47071b` |
| `f13-seg7-wrapper-validator-test.json` | `55a79e14f86a6d682c8c05784478a04c373504e32a1d128d307800e259e3027a` |
| `f13-seg7-runtime-failure-path-test.json` | `f5ce42f7dff20100517df0333792a0a9ec0505388223603f98bf3e09ea5e5321` |
| `f13-seg7-inventory-checker-test.json` | `b91e520432323563a603b86685aea4b63fcef6418f414493c1d674edc6513608` |
| `f13-seg7-hash-contract-test.json` | `4b8736a4493228b488437a1cba79f5bb790664b9d984e06c8c497f1f81f725cf` |
| `f13-seg7-dry-gate.json` | `6b3eb85674e47bc674c1efcc4dcf70b07102075c9e5531ff956648e0336afde8` |
| `f13-seg7-dry-result.json` | `8d80f6f3605fe39c58eb65ee7e5b9d5dc4536ce81de5dd519224b0e0e3379d76` |
| `f13-seg7-full-prestate-gate.json` | `9f24e63bfd53a012b96c654845b2354d122677ec03a1cc48aaa7c5368cc85275` |
| `f13-seg7-full-prestate.json` | `df66e641ac7d66a1197a4a73ac1e24c75b4651af551f00c0f1eac2e4bd96ec3f` |
| `f13-seg7-final-preapply-gate.json` | `eca9e42570527e8bd1048f223577cb2b15ce6687d6ae3691a62e1dd84b5f445d` |

上述 implementation/evidence hashes 构成 v9 执行冻结。real apply 前必须再次确认本文 SHA、这些冻结值、DB=backup 15/15、source=70/70、两正式文档 exact、authority=0、staged=0 不变。

## 状态：PASS

批准 root 执行一次 real apply retry7。执行顺序保持 apply → persisted fresh read-only → export/mode/split/source/inventory → source scope → export_all/build/fc/SHA → production document updater → landing。任一写后门禁失败必须物理恢复 DB、70-path source 及两份文档；失败态不得提交。

## Implementation Reviewer Verdict: F13-Seg-7 = PASS
