# F13-Seg-7 Implementation Review v8

## 结论与授权版本

- 审查范围：retry5 suffix scope 失败、恢复前态、Seg-8 BL 名称投影合同、22 字段事故链，以及 F13-Seg-7 Mode B 全流水线回归。
- **v1 至 v7 的 real apply 执行授权全部作废。** v7 的 PASS 已被 retry5 写后 scope 失败消耗；本文是当前唯一 implementation review 执行判定。
- 本 reviewer 仅执行只读检查和系统临时目录内的 fixture/runtime 测试，并将生成报告重定向到临时目录。没有执行 real apply、export、build、stage、commit，也没有改动 Ghidra DB、正式 source、冻结语义文件或生产实现。

## retry5 事故与完整恢复

| 阶段 | 结果 | 独立证据 |
|---|---|---|
| apply | PASS | `f13-seg7-apply-headless.log` 含 `STATUS: OK mode=apply FAIL=0 transaction=committed` 与 `Save succeeded`；SHA256=`311364c4edcb7cc9bc2a5b0e94654274cc3fa6a171a046b0efb540ab8a223f38`。 |
| persisted | PASS | fresh check 含 `STATUS: OK mode=check FAIL=0 PERSISTED_EXACT=true`；SHA256=`3af78d4b6f567460c6416c1ba64bc10e3e4d9c528463d78ae363b9d1c9232f68`。 |
| export/source edits/inventory | PASS | Ghidra export 正常结束；normalize/split/source edit 后 inventory exporter 给出 5213/5123/90。export wrapper 仅在 inventory checker exit=0 后进入 source scope，故到达 scope 失败证明 source edits 与 inventory checker 均已通过。 |
| 失败点 | 已确认 | 旧 scope checker SHA256=`81ab19ed027a26744c7dea75125d78e5db4abbd3982e04cc2b18c6515ddc00fc` 把 Seg-8 中因 Seg-7 函数 rename 必然产生的 7 条 BL 名称投影当成 suffix 内容变化，触发 `SEG8_SUFFIX_SCOPE_OVERSTRICT`。 |
| 后续阶段 | 未执行 | export_all、build、document updater、landing 均在 scope 之后，因此 retry5 未进入这些阶段。 |
| restore | PASS | 失败 catch 调用同一物理 restore；当前 DB 与 backup 均 15 文件且 path/size/SHA exact；source 70/70 mismatch=0，两正式文档 exact；fresh `-noanalysis -readOnly` 前态 PASS；authority=0、staged=0。 |

`check_f13_seg7_retry5_recovery.py` 与 `f13-seg7-retry5-recovery.json` 分别为
`05b861a06eacba76be0dc5f1f72c645127272407b41a30cacd3cfae758c97417`、
`3e088a9207647147becf3704de52080acde0ba7c87963cc1e15cef66e77161a5`，隔离重跑与上述事实一致。

## Seg-8 BL 投影独立推导

我没有采用 source-scope checker 的硬编码结论。独立读取冻结 plan 的 9 个 `renames[]`，遍历每个 `pre.incoming[]`，以正式 Seg-8 区间 `[0x080a46a0,0x080a585c)` 过滤 `UNCONDITIONAL_CALL`，再逐地址读取 baseline snapshot、当前 ROM 和 rename entry。结果恰好为以下 7 条：

| BL 地址 | baseline old | future export new | target/rename entry | mnemonic | opcode / ROM bytes |
|---|---|---|---|---|---|
| `0x080a49e4` | `check_equip_slot_has_field_spell_target` | `check_necroshade_normal_summon_available` | `0x080a4574` | `bl` | `fff7c6fd` |
| `0x080a504e` | `check_equip_set_activatable_for_player` | `check_gate_guardian_summon_allowed` | `0x080a3dac` | `bl` | `fef7adfe` |
| `0x080a5056` | `eval_equip_card_placeable_for_player` | `check_valkyrion_summon_allowed` | `0x080a3eb4` | `bl` | `fef72dff` |
| `0x080a5060` | `eval_spell_card_activation_placeable` | `check_special_summon_material_rule_satisfied` | `0x080a42b0` | `bl` | `fff726f9` |
| `0x080a50a0` | `check_banisher_of_light_activatable` | `check_banisher_sensitive_summon_allowed` | `0x080a3c2c` | `bl` | `fef7c4fd` |
| `0x080a50aa` | `check_banisher_pair_activation_allowed` | `check_neo_bubbleman_summon_allowed` | `0x080a3d74` | `bl` | `fef763fe` |
| `0x080a50d2` | `check_ritual_fusion_pairable_slots_exist` | `check_fusion_material_pair_slots_exist` | `0x080a4134` | `bl` | `fff72ff8` |

逐项结果：

- 7/7 的 edge target 与对应 `renames[].entry` 精确相等；`0x080a585c` 至模块末尾没有额外 incoming rename 投影。
- baseline 每个地址均唯一，行形态是 exporter 的 `bl <symbol> @ <address> <opcode>`；opcode 字符串与 ROM 对应 4 个原始字节逐项相等。
- 只把上述 7 行的 old name 换成 new name，即得到真实未来 export 的可接受行形态；地址、mnemonic、opcode、缩进和注释结构均不变。
- 对 future projection 反向替换 new→old 后，从 `0x080a46a0` 到 `asm/13_equip_placement.s` 末尾与 baseline 全文 exact；原始差异行恰好 7 行。

当前 `f13-seg7-source-scope.py` SHA256 为
`dca38d440cb0e41af94c843453a40b9d796c0b060b7867977e8e1f6c8173bd75`。它先要求 plan incoming 精确映射到上述投影，再逐行验证 baseline old/current new、地址唯一、`bl` 形态、opcode 和缩进，最后要求反向规范化 suffix 全文 exact。因此缺失、额外、错地址、错 old/new、错 target、错 opcode、错 mnemonic、重复地址和额外 comment 均 fail-closed。

`test_f13_seg7_source_scope.py` SHA256 为
`e069077dc091349886a093cc446b515dc5c9413a338df649246903ac67426e7e`。隔离复跑正例 PASS、11/11 负例按预期 code 拒绝，临时 evidence SHA256 精确为
`2053feaba583c9ab8da33b01df51772b9e2ce88be98404375b3b0d34c2204e58`。

## 22 字段事故链与正式文档投影

生产 updater 与 landing checker 使用相同的 22 个唯一 retry 字段：

- retry1：PowerShell wrapper lexical failure，restore COMPLETE；
- retry2：apply/persisted SUCCESS，inventory schema `KeyError`，restore COMPLETE；
- retry3：坏 Seg-8 边界导致 PREWRITE 拒绝，Ghidra/source write 均 NONE，restore NOT_REQUIRED；
- retry4：proposal SHA256 长度 65 导致 PREWRITE 拒绝，Ghidra/source write 均 NONE，恢复态 COMPLETE；
- retry5：apply/persisted/source edits/inventory SUCCESS，suffix scope overstrict，restore COMPLETE；
- retry6：FINAL_SUCCESS，landing PASS。

记录还唯一包含 `§5.1=0` 和下一任务 `F13-Seg-8 [0x080a46a0,0x080a585c)`。parser 要求 key 无重复、大小写和值 exact，并显式拒绝 retry3/retry4/retry5 的旧成功表述，其中 `retry4_status=FINAL_SUCCESS` 和 `retry4_landing=PASS` 都不能通过。

生产 updater SHA256=`bbbb5d515a20bd4e25f8ee3ce8fed6ba9a212371e78a4768c1a976819bfd28c2`；landing checker SHA256=`639f122272ada15ac77d03307b97dbc7bd6fe9e63ef0f5138d71030918da4574`。以真实当前两份文档的临时副本执行生产 updater：第一次 changed、landing 文档合同无失败；第二次幂等；63/63 合同负例与 5 个编辑/事务失败类全部拒绝并保持两文件 exact；正式两文档字节未变。

## v8 回归矩阵

| # | 检查 | 结果 | 独立证据 |
|---|---|---|---|
| V1 | source scope | PASS | 独立推导 7 条；test 正例 PASS，11/11 负例拒绝，未来 export/反向规范化 exact。 |
| V2 | landing | PASS | 正例 failures=[]；63/63 负例按预期 code 拒绝；正确 next=`[0x080a46a0,0x080a585c)`；旧范围生产命中=0。 |
| V3 | document updater | PASS | 真实两文档投影合同 PASS、二次幂等；63/63 合同负例与 5/5 事务失败类通过；正式文档不变、临时目录清理。 |
| V4 | wrapper 词法/AST/receipt/layout/wiring | PASS | 9 个 run wrapper compressed/collision/AST 均 0；exact integer receipt、DB generation layout、source-scope selftest 和 restore wiring 通过。 |
| V5 | runtime 失败路线 | PASS | 28/28；3 个 prewrite restore=0，25 个 postwrite restore=1；新增 `SOURCE_SCOPE_SELFTEST_FAIL` 与 scope wrapper route 均恢复；CommandNotFound=0。 |
| V6 | inventory | PASS | 5213/5123/90、9 rename；15/15 负例拒绝；错误 `renames[].address` 访问=0，fixture 已清理。 |
| V7 | static hash contract | PASS | 189 条生产声明全部为 64 位小写十六进制、目标唯一且实算 exact；70 snapshot exact；7/7 hash 负例拒绝。 |
| V8 | fresh dry | PASS | `semantic_actions_applied=false`，动作计数 exact；`readOnly=true`、`noanalysis=true`、DB before/after exact、source 70/70、document baseline exact。 |
| V9 | 当前恢复前态 | PASS | DB=backup 15/15 exact；source 70 rows/70 unique、mismatch=0；两文档 snapshot/current exact；authority=0；staged=0。 |
| V10 | final checker | PASS | 输出重定向读取真实 repo 重跑：exit=0、`FAIL=0`、failures=[]；输出 SHA256=`40134494371f990e3f87f1ab0bac72113b084cefeda3aa9f0a19ea3cd3c45d61`。 |

## v8 冻结 hash

### 语义与核心输入

| artifact | SHA256 |
|---|---|
| `F13-Seg-7.proposal.md` | `129f42778a7ed9da2ec4e082da91d71577532e56016d4f2cb394e797a8d63a99` |
| `F13-Seg-7.review.md` | `80fbd95458a16cb7faea369ff2051905b1b4cf6f8e5ebab9fb022ded0f60b926` |
| `F13-Seg-7.slots.tsv` | `2bd2619525cf56f5a996a2c8eb4dd91161958b1e825906d91e680e690221a99f` |
| `F13-Seg-7.impl-review-v7.md` | `9f6784f02a5c9adec660e5b6793d1b462ecb2d7dde0f424ec1701bb793f8597a` |
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
| `run_f13_seg7_landing_gate.ps1` | `cc1418916d8cb84c58562d674b3cd8b393bcdc56e34b472502165a1d4dbb5af8` |
| `run_f13_seg7_full_prestate_gate.ps1` | `193c4365b5fca823a5bc2cd44490d0c573f223b61a292e8a6318ec1849685191` |
| `run_f13_seg7_modea_prestate.ps1` | `3e2f418912d0bf40eb62f4f25f5e70ed4a87332bf4de27cd858442224adb6e28` |
| `test_f13_seg7_wrapper_validators.ps1` | `5cc483266d153fccb3bfcb4471a5789fea421cc9c8a2cfd6fd905671075defd1` |
| `test_f13_seg7_runtime_failure_paths.ps1` | `387c394b77e76513ebe6342c5b96490e913374cb3bb29277abbea64b66ee9f16` |
| `test_f13_seg7_hash_contract.py` | `c00aa3c41aafaa7622b08113fff264dfbfe5c26a8e4504626cff67793c47d501` |
| `test_f13_seg7_inventory_checker.py` | `7f09c911ef89cadfdfea3b825e3d4c61ec88b87f9c8f1011ab146ca21300420a` |
| `test_f13_seg7_source_scope.py` | `e069077dc091349886a093cc446b515dc5c9413a338df649246903ac67426e7e` |
| `test_f13_seg7_landing_checker.py` | `1ddd410849c3ceec9c1a1c55a66071e0fcf17821544de09219b7fd840262c9d0` |
| `test_f13_seg7_document_editor.py` | `ab1c4d07d8c84d076f844c52d8b16cf13a5dcf3307fdc21fd3d7b51ea3e72307` |
| `check_f13_seg7_retry2_recovery.py` | `23b10e7c1541b6e9fb1645f32d3c4e95f4ca489b4bfe199e6b1927b2d4afa714` |
| `check_f13_seg7_retry3_recovery.py` | `cd0c0f293b86afc7b10a1ff02811000f2b115824cb9e7e09436e4679a9327951` |
| `check_f13_seg7_retry4_prewrite.py` | `e3b6e583ce58c67315e516ac070fc5268987292cf5ab7b8446a54b6bf8d909d7` |
| `check_f13_seg7_retry5_recovery.py` | `05b861a06eacba76be0dc5f1f72c645127272407b41a30cacd3cfae758c97417` |
| `apply_f13_seg7_document_updates.py` | `bbbb5d515a20bd4e25f8ee3ce8fed6ba9a212371e78a4768c1a976819bfd28c2` |
| `apply_f13_seg7_source_edits.py` | `6f3def4a382e8b101c8876735f77ede31978ca39fbb3de6908a3d2506af6801c` |
| `f13-seg7-normalize-split.py` | `3950581c7cad1f2499fd3267a3916912b65c906a2c2e39a50afae4ab85c3fd9f` |
| `f13-seg7-source-scope.py` | `dca38d440cb0e41af94c843453a40b9d796c0b060b7867977e8e1f6c8173bd75` |
| `f13-seg7-inventory-check.py` | `f44bbe33ddafce19b1cc48425c8d52c39db34b631c05c66407837a6f72098b0b` |
| `f13-seg7-verify-rom.py` | `e4818ab261bd06ec322d393947319dcb88e3d267cfe965fa051d7c1fa5215449` |
| `check_f13_seg7_landing.py` | `639f122272ada15ac77d03307b97dbc7bd6fe9e63ef0f5138d71030918da4574` |
| `check_f13_seg7_final_preapply.py` | `fb440acb70a23eae3f99af5abf27cff6e9c15e37667b06556d6c7e9c85566ad5` |

### v8 关键证据

| evidence | SHA256 |
|---|---|
| `f13-seg7-retry5-recovery.json` | `3e088a9207647147becf3704de52080acde0ba7c87963cc1e15cef66e77161a5` |
| `f13-seg7-source-scope-test.json` | `2053feaba583c9ab8da33b01df51772b9e2ce88be98404375b3b0d34c2204e58` |
| `f13-seg7-landing-checker-test.json` | `b7c74bae0868f755f17b07771760969d7b399be7632689ba553e5fff1351d160` |
| `f13-seg7-document-editor-test.json` | `5f62ada0afffa9adac850c6a2985be551ce9d8e5977806d074a5ac32f307e976` |
| `f13-seg7-wrapper-validator-test.json` | `55a79e14f86a6d682c8c05784478a04c373504e32a1d128d307800e259e3027a` |
| `f13-seg7-runtime-failure-path-test.json` | `f5ce42f7dff20100517df0333792a0a9ec0505388223603f98bf3e09ea5e5321` |
| `f13-seg7-inventory-checker-test.json` | `b91e520432323563a603b86685aea4b63fcef6418f414493c1d674edc6513608` |
| `f13-seg7-hash-contract-test.json` | `5f888e1beb9bab8edd30f4d64ed21ecaabeb39bde3f880a37cd9500707d45708` |
| `f13-seg7-dry-gate.json` | `6b3eb85674e47bc674c1efcc4dcf70b07102075c9e5531ff956648e0336afde8` |
| `f13-seg7-dry-result.json` | `8d80f6f3605fe39c58eb65ee7e5b9d5dc4536ce81de5dd519224b0e0e3379d76` |
| `f13-seg7-full-prestate-gate.json` | `9f24e63bfd53a012b96c654845b2354d122677ec03a1cc48aaa7c5368cc85275` |
| `f13-seg7-full-prestate.json` | `df66e641ac7d66a1197a4a73ac1e24c75b4651af551f00c0f1eac2e4bd96ec3f` |
| `f13-seg7-final-preapply-gate.json` | `40134494371f990e3f87f1ab0bac72113b084cefeda3aa9f0a19ea3cd3c45d61` |

以上 implementation/evidence hashes 构成 v8 执行冻结。real apply 前必须再次确认本文 SHA、上述冻结值、DB=backup 15/15、source=70/70、两正式文档 exact、authority=0、staged=0 不变。

## 状态：PASS

批准 root 执行一次 real apply retry6。执行顺序保持 apply → persisted fresh read-only → export/mode/split/source/inventory → source scope → export_all/build/fc/SHA → production document updater → landing。任一写后门禁失败必须物理恢复 DB、70-path source 及两份文档；失败态不得提交。

## Implementation Reviewer Verdict: F13-Seg-7 = PASS
