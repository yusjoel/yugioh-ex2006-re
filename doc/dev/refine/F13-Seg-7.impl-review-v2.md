# F13-Seg-7 Implementation Review v2

## 结论与前版失效说明

- 审查范围：`F13-Seg-7 [0x080a38fc,0x080a46a0)` 的 Mode B retry2 实现、失败恢复和最终落地门禁。
- 本文取代 `F13-Seg-7.impl-review.md` 的执行批准；前版保留为历史记录。real apply retry1 已经证实前版遗漏了两项实现缺陷：压缩写法 `throw'F13_SEG7_APPLY_GATE_FAIL'` 被 PowerShell 作为命令 `throwF13_SEG7_APPLY_GATE_FAIL` 执行，以及 apply gate 错把合法 Ghidra save 后的 `db.<generation>.gbf` 文件名轮换判为 DB 结构损坏。因此，前版 PASS 不再提供 real apply 授权。
- retry1 的 Ghidra transaction 曾正常 commit/save，随后 wrapper 触发 `CommandNotFoundException`。物理 restore 已完成：当前 DB 与冻结备份15/15逐项一致，source baseline 70/70一致，fresh `-noanalysis -readOnly` 语义前态通过，authority产物为0，暂存区为0。
- v2 修正后的 wrapper、validator、runtime/recovery checker、fresh dry 和 final-preapply checker 均由本 reviewer 重新执行或独立复算，未执行 additional real apply、export、build、stage 或 commit。

## 冻结输入与最终门禁

| 输入/门禁 | SHA256 | 结果 |
|---|---|---|
| proposal | `129f42778a7ed9da2ec4e082da91d71577532e56016d4f2cb394e797a8d63a99` | exact |
| TSV | `2bd2619525cf56f5a996a2c8eb4dd91161958b1e825906d91e680e690221a99f` | exact |
| semantic review PASS | `80fbd95458a16cb7faea369ff2051905b1b4cf6f8e5ebab9fb022ded0f60b926` | exact |
| plan | `772b89fab666c9ad09516aff6e3e8c3a3984db91d393cef99ede87e425edbe6b` | exact |
| Ghidra script | `3c446203ce84dabc92cb4cb5dbdabe422aa8ea497d7bb0a05db6269e0f368b28` | exact |
| source baseline | `3c0376f0bec32b47e6e0b4f96669069d38f69e967e620a8ecd6f1f272b0644b0` | exact，70 paths |
| final-preapply checker | `c66938171eeaf4ee1817a0f3ee039be61719eb36686cef1b235aa028de1e5e27` | exact |
| final-preapply gate | `bdf4a5b23feac2be36de991ba1bae6fbd71233d5130e15a76703c33759d4db21` | `F13_SEG7_FINAL_PREAPPLY_PASS_DRY_ONLY`, `FAIL=0` |

动作合同仍为 `EQ=73, REF=19, RENAME=4, EOL=96, FUNC_RENAME=9, PLATE=14, CARVE=2, FIXED_OLD_NAME_SCAN=9`，retry2未改变冻结语义。

## v2 独立核验

| # | 检查 | 结果 | 独立证据 |
|---|---|---|---|
| V1 | 9个 `run_f13_seg7_*.ps1` 词法与AST | PASS | 独立扫描9个wrapper：压缩控制流命中0，`throw'`/`return$`及控制流命令碰撞0，PowerShell AST parse error=0。旧 `return$false` 与 retry1 的压缩 `throw` 均已消失。 |
| V2 | 21条失败分支实际运行 | PASS | synthetic runtime共21 cases；3条apply写前拒绝均restore=0，18条写后失败均restore=1；捕获的异常均为目标marker，`CommandNotFoundException=0`。关键字探针覆盖return/throw/if-else/foreach/continue/try-catch等实际PowerShell执行路径。 |
| V3 | receipt严格类型与完整性 | PASS | exact和字段逆序接受；额外、缺项、错值、错名、null、字符串、浮点、bool、UInt64溢出均拒绝。scalar仅接受整数0；字符串0、浮点0、false、null和溢出均拒绝。 |
| V4 | apply DB layout与`dbChanged` | PASS | 固定路径集合必须exact；每个DB generation目录的文件数量与结构必须exact，`db.<generation>.gbf`编号允许合法轮换。独立负测结果：exact=true、generation rotation=true；丢失文件=false、额外文件=false、畸形generation名=false、generation移组=false。成功合同另行强制`dbChanged=true`、before/after均15文件。 |
| V5 | apply诊断与恢复顺序 | PASS | 冻结hash、DB前态、source前态在写前拒绝，不调用restore。写后异常进入catch；failure diagnostic写入位于嵌套best-effort try内，即使诊断写失败仍继续物理restore，然后重抛原异常。 |
| V6 | persisted fresh语义链 | PASS | 必须先严格复核receipt与apply gate，包含`db_changed=true`、`db_file_count_exact=true`、`db_layout_exact=true`及完整hash/count合同；随后以独立`-noanalysis -readOnly`进程复算完整after capture。仅接受布尔`PERSISTED_EXACT=true`、精确success marker、15/15 DB查询前后逐项相等。任一失败均restore。 |
| V7 | 物理DB恢复 | PASS | backup evidence冻结15个relative path/size/SHA256；restore先校验备份，再物理替换当前`.rep`，拒绝丢失、额外或结构异常，最后重新执行fresh read-only完整语义前态。当前DB与物理备份15/15一致。 |
| V8 | source baseline与恢复 | PASS | 70-path baseline同时表达present/absent状态；覆盖全部25 modules、`asm/all.s.raw`、`asm/all.s.raw.nomode`、`output/2343.gba`、constants、CSV、registry、inventories、progress及实现输入。restore恢复present内容并删除baseline absent/transient authority路径。当前mismatch=0。 |
| V9 | downstream失败恢复 | PASS | persisted、export/mode/split/source edits/inventory/source scope/export_all/build/ROM、standalone source-scope和landing的每条写后失败路径均进入restore。landing最终检查任一失败也执行物理DB与70-path source restore。 |
| V10 | export/split/mode/scope合同 | PASS | persisted PASS是export前置；全范围export后仅规范2个`.arm`和2个`.thumb`行，再执行inject_modes、split与split-check，要求25 modules。变化范围仅允许modules02/04/12/13/23和批准的all/rom/constants/CSV/registry/inventory/progress路径，Seg-8从`0x080a46a0`起后缀保持一致。 |
| V11 | build与byte identity合同 | PASS | pipeline要求inventory、`export_all.py` 49/49、`build.bat`、Python byte compare、`fc /b`全部成功，ROM size=33554432且SHA1=`9689337d6aac1ce9699ab60aac73fc2cfdccad9b`；任一失败restore。此项仅审查合同，v2 review未运行真实export/build。 |
| V12 | fresh dry、retry1恢复与authority | PASS | 本reviewer重跑fresh dry：exit0、success marker、result exact、`semantic_actions_applied=false`、DB before/after exact，source mismatch=0。retry2 recovery checker与final-preapply checker均`FAIL=0`；additional real apply=false，authority outputs present=0，staged=0。 |

## v2 运行证据冻结

| evidence | SHA256 |
|---|---|
| `f13-seg7-preapply-backup.json` | `3f2b848200de1bd02c4e9c97d3b44c6c62264a0958b72b7a3b2649cc8f03aac6` |
| `InspectF13Seg7FullPrestate.py` | `4a8491751b9447771805a173133582e0797a65f461c11a93540b03231d564db1` |
| `f13-seg7-full-prestate.json` | `df66e641ac7d66a1197a4a73ac1e24c75b4651af551f00c0f1eac2e4bd96ec3f` |
| `f13-seg7-full-prestate-gate.json` | `9f24e63bfd53a012b96c654845b2354d122677ec03a1cc48aaa7c5368cc85275` |
| `f13-seg7-dry-result.json` | `8d80f6f3605fe39c58eb65ee7e5b9d5dc4536ce81de5dd519224b0e0e3379d76` |
| `f13-seg7-dry-gate.json` | `bd0fa603a1e970580a74654d56f6070c6261c95c35b24e104d3ffb12c792087f` |
| `f13-seg7-wrapper-validator-test.json` | `510983e394d4713790bed8bc2f5b06b990d979d2deedfaf8dd2d0e7c065466c3` |
| `f13-seg7-runtime-failure-path-test.json` | `ce8cd8ba111d06d8f031e378807dd80ee20f081ed921e7b3dfa1f403b7b2d8b2` |
| `f13-seg7-retry2-recovery.json` | `fef36bbe3777ecc42fff9be018c167c9653c204e0d614dfa9814db1f029e64b3` |
| retry1 `f13-seg7-apply-headless.log` | `cbde87ef765282a241f9d855df5c8e483ea87e40f7114649919003aba55839ab` |
| `f13-seg7-restore.json` | `a504883d262f0c21c68cb32241a84e991389647e0e5802500cf6ed7b60b1980b` |
| `f13-seg7-final-preapply-gate.json` | `bdf4a5b23feac2be36de991ba1bae6fbd71233d5130e15a76703c33759d4db21` |

## 冻结的 v2 implementation artifacts

| artifact | SHA256 |
|---|---|
| `tools/ghidra-labeling/RefineF13Seg7.py` | `3c446203ce84dabc92cb4cb5dbdabe422aa8ea497d7bb0a05db6269e0f368b28` |
| `f13-seg7-plan.json` | `772b89fab666c9ad09516aff6e3e8c3a3984db91d393cef99ede87e425edbe6b` |
| `f13-seg7-source-baseline.json` | `3c0376f0bec32b47e6e0b4f96669069d38f69e967e620a8ecd6f1f272b0644b0` |
| `check_f13_seg7_final_preapply.py` | `c66938171eeaf4ee1817a0f3ee039be61719eb36686cef1b235aa028de1e5e27` |
| `run_f13_seg7_restore.ps1` | `a7dd126ead9afba1805bd10bf91bb51bd358a47e44ee0df24880db768075862f` |
| `run_f13_seg7_dry_gate.ps1` | `c4f80ca7d4c1599728669babb6c72242b175376b29aec7c90b9af1b9be923eac` |
| `run_f13_seg7_apply_gate.ps1` | `9a99a178edf8d17aacb0228d9b0d1e81998fb0c81fe2a54dfd74a5df04b80c6f` |
| `run_f13_seg7_persisted_gate.ps1` | `0086fcf0184214f459352e55fddd87a2a99f9e6018cb03811aac1b9c057838ad` |
| `run_f13_seg7_export_build_gate.ps1` | `1abd0e6b34aa7b666946970faa7d72ebb02065e6bef48946e46fdeb59b1f415f` |
| `run_f13_seg7_source_scope_gate.ps1` | `9f93d00ed1f1e96351f154d530de3716f2b726994f93a84692efa24cc6ec2507` |
| `run_f13_seg7_landing_gate.ps1` | `bb4aeff22bf199de10f65778c7b9e19f0650f72799cd8ec8290355c6d27497ed` |
| `run_f13_seg7_full_prestate_gate.ps1` | `193c4365b5fca823a5bc2cd44490d0c573f223b61a292e8a6318ec1849685191` |
| `run_f13_seg7_modea_prestate.ps1` | `3e2f418912d0bf40eb62f4f25f5e70ed4a87332bf4de27cd858442224adb6e28` |
| `test_f13_seg7_wrapper_validators.ps1` | `65c77d90e475a7498978557fca177864cbe6a9d2e65aadbc6e95bf84d787a6e4` |
| `test_f13_seg7_runtime_failure_paths.ps1` | `762e1218844c5e351710efe9a2779d5e00ed2e42a1c78bf4c6d69f61abec8bbe` |
| `check_f13_seg7_retry2_recovery.py` | `23b10e7c1541b6e9fb1645f32d3c4e95f4ca489b4bfe199e6b1927b2d4afa714` |
| `apply_f13_seg7_source_edits.py` | `6f3def4a382e8b101c8876735f77ede31978ca39fbb3de6908a3d2506af6801c` |
| `f13-seg7-normalize-split.py` | `3950581c7cad1f2499fd3267a3916912b65c906a2c2e39a50afae4ab85c3fd9f` |
| `f13-seg7-source-scope.py` | `81ab19ed027a26744c7dea75125d78e5db4abbd3982e04cc2b18c6515ddc00fc` |
| `f13-seg7-inventory-check.py` | `a5ff45de7c057dfaed702e86d9b72e847d67dbdb33487c82e9a93282b151642a` |
| `f13-seg7-verify-rom.py` | `e4818ab261bd06ec322d393947319dcb88e3d267cfe965fa051d7c1fa5215449` |
| `check_f13_seg7_landing.py` | `7660c4db5372c7acb76bc0bb7441e301b4aa9d8b8a1baeff68d51de1b26d4abd` |

以上hash在real apply retry2前不得变化。本文不进入冻结语义hash链，也不修改前版implementation review、proposal、semantic review或TSV。

## 状态：PASS

批准root在重新核对上述implementation hashes与final-preapply gate SHA后执行一次real apply retry2。之后必须按 persisted fresh read-only → export/mode/split → source edits/scope → inventory → export_all/build/fc/SHA → progress/landing 顺序完成；任一写后失败必须物理恢复DB与70-path source baseline，失败态不得提交。

## Implementation Reviewer Verdict: F13-Seg-7 = PASS
