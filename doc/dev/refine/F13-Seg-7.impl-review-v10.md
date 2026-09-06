# F13-Seg-7 Implementation Review v10

## 结论与授权版本

- 审查范围：retry7 写后 source-scope 失败及恢复、跨模块 BL/函数 label/plate 的结构合同、35 字段事故链，以及 F13-Seg-7 Mode B 全流水线回归。
- **v1 至 v9 的 real apply 执行授权全部作废。** v9 的 PASS 已被 retry7 写后 `MODULE04_EXPORT_PADDING_ASSERTION` 消耗；本文是当前唯一 implementation review 执行判定。
- 本 reviewer 仅执行只读检查及隔离 fixture/runtime 测试；测试和 final checker 的正式报告写入点均重定向到内存。没有执行 real apply、export、build、stage、commit，也没有改动 Ghidra DB、正式 source、冻结语义文件或生产实现。

## retry7 事故与完整恢复

| 阶段 | 结果 | 独立证据 |
|---|---|---|
| apply | PASS | `f13-seg7-apply-headless.log` 含 transaction committed 与 `Save succeeded`；SHA256=`5425477994e5177f32c288bd8075221cc26032d875ab4e41717ce6bff352bbe8`。 |
| persisted | PASS | fresh check 含 `PERSISTED_EXACT=true`；SHA256=`571a6a852bb0e927e743c1fc8f781110a9dadd659bbec0bebfc4c1bb150cc4b1`。 |
| export/source/inventory/Seg-8 suffix | PASS | export log SHA256=`ed709ec73bf47b7ae9ce40a7842176d910d230a74a6ea0fc5e8758eee350f1dd`；inventory log SHA256=`6073bf0d04ec1122aa9668f33bce32153e9e4ce43eac543f2f333268908d36ab`，总数 5213/5123/90。retry7 recovery 明确记录 source edits、inventory 和 Seg-8 suffix 均 SUCCESS。 |
| 失败点 | 已确认 | v9 checker SHA256=`59a75f69bb2f47a7de1366009c57399ea7bd74f53c8cac3f645c49e6acf83ead` 对 module04 `0x080415be` 保留固定 padding 文本断言。新 callee 的 instruction width=49，真实 Exporter 只产生 1 个分隔空格，旧断言要求 5 个空格，触发 `MODULE04_EXPORT_PADDING_ASSERTION`。 |
| 后续阶段 | 未执行 | export_all、build、document updater、landing 均位于失败点之后。 |
| restore | PASS | 当前 DB=backup 15/15 path/size/SHA exact；source 70 rows/70 unique、mismatch=0；两正式文档 exact；fresh `-noanalysis -readOnly` 前态 PASS；authority=0、staged=0。 |

retry7 recovery checker 与 evidence 的 SHA256 分别为
`97d36848a23ce0b1ac1ae1f3ae3c86a7b8ee511fdacdb7ec12afa7fec69c8460`、
`a78e7e24010096a7da3ffee026b1bb32f86f9dc5f7ecc7243390f9a0edfdf39c`；evidence 为 `F13_SEG7_RETRY7_RECOVERY_PASS`、`FAIL=0`，并记录 `retry10_additional_real_apply=false`。

## Exporter 结构 parser 独立核验

正式 Exporter 在 `tools/asm-regen/ghidra/ExportRangeToGas.py:911` 使用 `"    %-40s %s%s\n"`。含显式分隔空格后，其规则为：instruction width 39 产生 2 个空格，width 40 产生 1 个空格，width 大于 40 仍产生 1 个空格。独立生成并交给现行 `BL_LINE.fullmatch` 的 39/40/41 三个边界样本全部通过，padding 分别为 2/1/1。

现行 `f13-seg7-source-scope.py` SHA256=`621b43f2af1432cba1f295006c44a535137622a2268e72b2edcbdfed2c5bc90e`。parser 强制四个 ASCII 空格缩进、`bl`、callee、正数个 ASCII padding、`@`、八位小写地址和八位小写 opcode，且 fullmatch 禁止额外 token/comment；不再按 callee 长度硬编码 padding。

独立从冻结 plan 的 `renames[].pre.incoming`、baseline 25 模块及 ROM 字节重建 9 条 BL 合同，结果如下：

| 地址 | 投影 | instruction width | padding | opcode / ROM bytes |
|---|---|---:|---:|---|
| `0x080415be` | `write_spell_activation_type_display_bit` → `write_special_summon_material_rule_display_bit` | 49 | 1 | `53f0cbfc` |
| `0x08094f5a` | `classify_spell_card_activation_type` → `get_special_summon_material_rule_by_card_id` | 46 | 1 | `0ff067f9` |
| `0x080a49e4` | `check_equip_slot_has_field_spell_target` → `check_necroshade_normal_summon_available` | 43 | 1 | `fff7c6fd` |
| `0x080a504e` | `check_equip_set_activatable_for_player` → `check_gate_guardian_summon_allowed` | 37 | 4 | `fef7adfe` |
| `0x080a5056` | `eval_equip_card_placeable_for_player` → `check_valkyrion_summon_allowed` | 33 | 8 | `fef72dff` |
| `0x080a5060` | `eval_spell_card_activation_placeable` → `check_special_summon_material_rule_satisfied` | 47 | 1 | `fff726f9` |
| `0x080a50a0` | `check_banisher_of_light_activatable` → `check_banisher_sensitive_summon_allowed` | 42 | 1 | `fef7c4fd` |
| `0x080a50aa` | `check_banisher_pair_activation_allowed` → `check_neo_bubbleman_summon_allowed` | 37 | 4 | `fef763fe` |
| `0x080a50d2` | `check_ritual_fusion_pairable_slots_exist` → `check_fusion_material_pair_slots_exist` | 41 | 1 | `fff72ff8` |

9/9 均满足 baseline old、plan target、ROM opcode、`%-40s` 生成行及 parser 字段 exact。Seg-8 suffix 仍恰好七条，逐字段验证后用完整 baseline 行归一化，suffix 全文 exact 且没有额外投影。

函数 metadata 也从固定文本升级为结构验证：9 个 post-name label 各唯一，label 后首条 addressed instruction 的地址必须等于对应 `renames[].entry`，该 entry 地址在全文也必须唯一；14 个 ASCII plate 文本各唯一，plate 后首条 addressed instruction 地址必须等于 plan 的 plate address。现行执行链中的 source checker 没有固定 padding assert；retry7 recovery 文件中引用旧断言的字符串仅用于冻结事故证据，不参与未来 source 合同判定。

测试源 `test_f13_seg7_source_scope.py` SHA256=`b8909d3b842a96979852b202b38c44b14d65bdd22648a196f405e0785748a7b2`。隔离重跑结果：

- 两个 suffix 正例、两个跨模块真实 Exporter 正例、39/40/41 width 正例、9 label 和 14 plate metadata 正例全部通过；
- 27/27 负例按预期 code 拒绝：suffix 15、跨模块 call 8、metadata 4；
- `production_checker_references=["f13-seg7-source-scope.py"]`，`fragile_padding_assertions=[]`，fixture-only、persistent writes=false、real apply=false；
- 内存捕获报告按 Windows `Path.write_text` 字节序列与冻结 evidence exact，SHA256=`e531e24d512ccf7c3773b7d14880dd15e1a3e1f288fc08bcd7069cccea4e2d94`。

## 35 字段事故链与文档接线

生产 updater 和 landing checker 使用同一组 35 个唯一字段：

- retry1：PowerShell lexical failure，restore COMPLETE；
- retry2：apply/persisted SUCCESS，inventory schema `KeyError`，restore COMPLETE；
- retry3：坏 Seg-8 边界导致 PREWRITE 拒绝，Ghidra/source write 均 NONE，restore NOT_REQUIRED；
- retry4：65 字符 proposal SHA 导致 PREWRITE 拒绝，Ghidra/source write 均 NONE，恢复态 COMPLETE；
- retry5：apply/persisted/source edits/inventory SUCCESS，suffix scope overstrict，restore COMPLETE；
- retry6：apply/persisted/source edits/inventory SUCCESS，`SUFFIX_NORMALIZATION_PADDING_MISMATCH`，restore COMPLETE；
- retry7：apply/persisted/source edits/inventory/Seg-8 suffix SUCCESS，`MODULE04_EXPORT_PADDING_ASSERTION`，restore COMPLETE；
- retry8：`FINAL_SUCCESS`，landing `PASS`。

记录还唯一包含 `§5.1=0` 和下一任务 `F13-Seg-8 [0x080a46a0,0x080a585c)`。parser 要求 key 唯一、大小写和值 exact，并拒绝 retry3 至 retry7 的旧成功记录，特别拒绝 retry7 `FINAL_SUCCESS`/landing `PASS`。

生产 updater SHA256=`cd0051bb6a304858520d411529d203fb86d9d2f2ea149d0d0fa9252a8545eba9`；landing checker SHA256=`bcc40349d17723cf24af9421bd3c5931ec99c5f6a0a998c45e963e9ed2507e23`。隔离重跑 landing 为 93/93 负例通过；以真实当前两文档副本运行生产 updater，第一次 changed 且 landing 合同 PASS，第二次幂等，93/93 文档合同负例和 5/5 双文件事务失败路线全部通过，正式文档不变且临时目录清理。

## v10 回归矩阵

| # | 检查 | 结果 | 独立证据 |
|---|---|---|---|
| V1 | source scope | PASS | 2 个 suffix 正例、2 个跨模块 call、39/40/41 width、9 label、14 plate；27/27 负例；现行 checker 固定 padding assert=0。 |
| V2 | landing | PASS | 正例 failures=[]；93/93 负例；35 字段事故链、`§5.1=0` 与 next range exact。 |
| V3 | document updater | PASS | 真实两文档投影、二次幂等、93/93 合同负例、5/5 事务失败路线；正式文档不变。 |
| V4 | wrapper 词法/AST/receipt/layout/wiring | PASS | 9 个 run wrapper compressed/collision/AST 均 0；receipt exact integer、DB generation layout、scope selftest、document/landing/restore wiring 全部通过。 |
| V5 | runtime 失败路线 | PASS | 28/28；3 个 prewrite restore=0，25 个 postwrite restore=1；CommandNotFound=0，real apply=false。 |
| V6 | inventory | PASS | 5213/5123/90、9 rename；15/15 负例；错误 schema access=0，fixture 已清理。 |
| V7 | static hash contract | PASS | 198 条生产声明均为恰好 64 个小写十六进制字符，目标唯一且实算 exact；70 snapshot exact；7/7 负例。 |
| V8 | fresh dry/prestate | PASS | 冻结 dry 为 semantic actions=false、动作计数 exact、readOnly/noanalysis、DB before/after exact；retry7 后 fresh prestate 与当前 final checker 再验 DB/source/docs exact。 |
| V9 | retry7 恢复态 | PASS | DB=backup 15/15 exact；source 70/70、mismatch=0；docs exact；authority=0；staged=0。 |
| V10 | final checker | PASS | 报告写入重定向到内存后读取真实 repo 重跑：exit=0、`FAIL=0`、37 frozen input 和 29 production artifact 全 exact；Windows CRLF 字节与正式 gate exact，SHA256=`af73de78b3f9fdcfbb280aa23e5972aec7cb98a23b1eb2f7d8dc6dfbd12ecd22`。 |

## v10 冻结 hash

### 语义与核心输入

| artifact | SHA256 |
|---|---|
| `F13-Seg-7.proposal.md` | `129f42778a7ed9da2ec4e082da91d71577532e56016d4f2cb394e797a8d63a99` |
| `F13-Seg-7.review.md` | `80fbd95458a16cb7faea369ff2051905b1b4cf6f8e5ebab9fb022ded0f60b926` |
| `F13-Seg-7.slots.tsv` | `2bd2619525cf56f5a996a2c8eb4dd91161958b1e825906d91e680e690221a99f` |
| `F13-Seg-7.impl-review-v9.md` | `fd6acff0ffce16e31c10a03fed3ddd44b341a09ff281aebdd51578e487b38f27` |
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
| `run_f13_seg7_landing_gate.ps1` | `625d435515cf785548b8c98926c9968f829b356b7241495da6da2821d43ec982` |
| `run_f13_seg7_full_prestate_gate.ps1` | `193c4365b5fca823a5bc2cd44490d0c573f223b61a292e8a6318ec1849685191` |
| `run_f13_seg7_modea_prestate.ps1` | `3e2f418912d0bf40eb62f4f25f5e70ed4a87332bf4de27cd858442224adb6e28` |
| `test_f13_seg7_wrapper_validators.ps1` | `0c432a5b2a5e64714bdcf809fca439e5047c032d8cf51f4fc9488d0e84f4e316` |
| `test_f13_seg7_runtime_failure_paths.ps1` | `387c394b77e76513ebe6342c5b96490e913374cb3bb29277abbea64b66ee9f16` |
| `test_f13_seg7_hash_contract.py` | `c00aa3c41aafaa7622b08113fff264dfbfe5c26a8e4504626cff67793c47d501` |
| `test_f13_seg7_inventory_checker.py` | `7f09c911ef89cadfdfea3b825e3d4c61ec88b87f9c8f1011ab146ca21300420a` |
| `test_f13_seg7_source_scope.py` | `b8909d3b842a96979852b202b38c44b14d65bdd22648a196f405e0785748a7b2` |
| `test_f13_seg7_landing_checker.py` | `e5b11ef0a1d2c4a78998e13a2cbc8339f39187543624fa4d938df6ff846e5596` |
| `test_f13_seg7_document_editor.py` | `ea1fbd002ff36288860d010892a3c44fdbd11c5d8718c3e906391cc7888533c0` |
| `check_f13_seg7_retry2_recovery.py` | `23b10e7c1541b6e9fb1645f32d3c4e95f4ca489b4bfe199e6b1927b2d4afa714` |
| `check_f13_seg7_retry3_recovery.py` | `cd0c0f293b86afc7b10a1ff02811000f2b115824cb9e7e09436e4679a9327951` |
| `check_f13_seg7_retry4_prewrite.py` | `e3b6e583ce58c67315e516ac070fc5268987292cf5ab7b8446a54b6bf8d909d7` |
| `check_f13_seg7_retry5_recovery.py` | `05b861a06eacba76be0dc5f1f72c645127272407b41a30cacd3cfae758c97417` |
| `check_f13_seg7_retry6_recovery.py` | `001f984c05a3cbe46f8a4e9467b478039d3f5e45ac4f4f5c38479aec45c03559` |
| `check_f13_seg7_retry7_recovery.py` | `97d36848a23ce0b1ac1ae1f3ae3c86a7b8ee511fdacdb7ec12afa7fec69c8460` |
| `apply_f13_seg7_document_updates.py` | `cd0051bb6a304858520d411529d203fb86d9d2f2ea149d0d0fa9252a8545eba9` |
| `apply_f13_seg7_source_edits.py` | `6f3def4a382e8b101c8876735f77ede31978ca39fbb3de6908a3d2506af6801c` |
| `f13-seg7-normalize-split.py` | `3950581c7cad1f2499fd3267a3916912b65c906a2c2e39a50afae4ab85c3fd9f` |
| `f13-seg7-source-scope.py` | `621b43f2af1432cba1f295006c44a535137622a2268e72b2edcbdfed2c5bc90e` |
| `f13-seg7-inventory-check.py` | `f44bbe33ddafce19b1cc48425c8d52c39db34b631c05c66407837a6f72098b0b` |
| `f13-seg7-verify-rom.py` | `e4818ab261bd06ec322d393947319dcb88e3d267cfe965fa051d7c1fa5215449` |
| `check_f13_seg7_landing.py` | `bcc40349d17723cf24af9421bd3c5931ec99c5f6a0a998c45e963e9ed2507e23` |

以上 29 个 production artifact 的实算 hash 均与 final checker 冻结值一致。final checker 自身 SHA256=`2c16d50c2590034d366b594454400b7dd1b8f12173c2d3f7385f2e6f6bbf781a`。

### v10 关键证据

| evidence | SHA256 |
|---|---|
| `f13-seg7-retry7-recovery.json` | `a78e7e24010096a7da3ffee026b1bb32f86f9dc5f7ecc7243390f9a0edfdf39c` |
| `f13-seg7-source-scope-test.json` | `e531e24d512ccf7c3773b7d14880dd15e1a3e1f288fc08bcd7069cccea4e2d94` |
| `f13-seg7-landing-checker-test.json` | `db53efb7bd7dd39289cc8662635483022a8050120396b65f0b45117371ad7bb9` |
| `f13-seg7-document-editor-test.json` | `5c0f0f6f8d96848937991a771625d97589302515dcb6f5c54fd5cfbefaa7dc60` |
| `f13-seg7-wrapper-validator-test.json` | `55a79e14f86a6d682c8c05784478a04c373504e32a1d128d307800e259e3027a` |
| `f13-seg7-runtime-failure-path-test.json` | `f5ce42f7dff20100517df0333792a0a9ec0505388223603f98bf3e09ea5e5321` |
| `f13-seg7-inventory-checker-test.json` | `b91e520432323563a603b86685aea4b63fcef6418f414493c1d674edc6513608` |
| `f13-seg7-hash-contract-test.json` | `f3b7a03c4ae1bba2a84180f86c1ab4fb1e063fff6507e896dea7130e59777ced` |
| `f13-seg7-dry-gate.json` | `6b3eb85674e47bc674c1efcc4dcf70b07102075c9e5531ff956648e0336afde8` |
| `f13-seg7-dry-result.json` | `8d80f6f3605fe39c58eb65ee7e5b9d5dc4536ce81de5dd519224b0e0e3379d76` |
| `f13-seg7-full-prestate-gate.json` | `9f24e63bfd53a012b96c654845b2354d122677ec03a1cc48aaa7c5368cc85275` |
| `f13-seg7-full-prestate.json` | `df66e641ac7d66a1197a4a73ac1e24c75b4651af551f00c0f1eac2e4bd96ec3f` |
| `f13-seg7-final-preapply-gate.json` | `af73de78b3f9fdcfbb280aa23e5972aec7cb98a23b1eb2f7d8dc6dfbd12ecd22` |

上述 implementation/evidence hashes 构成 v10 执行冻结。real apply 前必须再次确认本文 SHA、这些冻结值、DB=backup 15/15、source=70/70、两正式文档 exact、authority=0、staged=0 不变。

## 状态：PASS

批准 root 执行一次 real apply retry8。执行顺序保持 apply → persisted fresh read-only → export/mode/split/source/inventory → source scope → export_all/build/fc/SHA → production document updater → landing。任一写后门禁失败必须物理恢复 DB、70-path source 及两份文档；失败态不得提交。

## Implementation Reviewer Verdict: F13-Seg-7 = PASS
