# F13-Seg-7 Implementation Review v3

## 结论与授权版本

- 审查范围：`F13-Seg-7 [0x080a38fc,0x080a46a0)` 的 Mode B retry3 实现、库存导出合同、失败恢复和最终落地门禁。
- 本文取代 `F13-Seg-7.impl-review-v2.md` 的执行批准；v1、v2均保留为历史记录。retry2 已证实 v2 未发现库存 checker 对 plan schema 的错误读取，因此 v2 PASS 不再提供 real apply 授权。
- 冻结语义保持不变：proposal `129f42778a7ed9da2ec4e082da91d71577532e56016d4f2cb394e797a8d63a99f`，TSV `2bd2619525cf56f5a996a2c8eb4dd91161958b1e825906d91e680e690221a99f`，semantic review PASS `80fbd95458a16cb7faea369ff2051905b1b4cf6f8e5ebab9fb022ded0f60b926`，plan `772b89fab666c9ad09516aff6e3e8c3a3984db91d393cef99ede87e425edbe6b`，Ghidra script `3c446203ce84dabc92cb4cb5dbdabe422aa8ea497d7bb0a05db6269e0f368b28`。
- 本reviewer只执行隔离临时目录中的fixture/runtime检查、fresh `-noanalysis -readOnly` dry和只读状态复算。所有临时目录均已删除；未执行 additional real apply、export、build、stage 或 commit。

## retry2 事故独立复核

| 阶段 | 结果 | 证据 |
|---|---|---|
| real apply retry2 | PASS | apply log含`STATUS: OK mode=apply FAIL=0 transaction=committed`和`Save succeeded`。 |
| persisted fresh check | PASS | persisted log含`STATUS: OK mode=check FAIL=0 PERSISTED_EXACT=true`。 |
| Function inventory export | PASS | exporter正常结束并输出`total=5213, named=5123, auto=90`。 |
| inventory checker | FAIL | 旧checker把`plan.renames[]`当作含`address`字段的对象，执行`contract['address']`时触发`KeyError`；export wrapper进入`INVENTORY_CHECK_FAIL`。真实schema的地址字段是整数`entry`。 |
| recovery | PASS | catch调用物理restore；当前DB与冻结备份15/15逐项一致，source baseline 70/70一致，fresh read-only语义前态PASS，authority outputs=0，staged=0。 |

retry2 的apply、persisted成功不构成落地成功；库存检查失败后已经完整撤销DB和source变化。retry3开始前仍处于冻结前态。

## plan、source contract与Exporter真实schema

### 三层地址表示

| 层 | 地址字段 | 精确类型/格式 | v3处理 |
|---|---|---|---|
| `plan.renames[]` | `entry` | JSON integer；Python要求`type(value) is int`，范围`0..0xffffffff` | 格式化为canonical `0x%08x` |
| `plan.source_contract.csv[]` | `address` | lowercase canonical string，`^0x[0-9a-f]{8}$` | 与由`entry`生成的地址、pre/post name逐项交叉匹配 |
| `ExportFunctionInventory.py` CSV | `address` | lowercase canonical string | 作为7列CSV的首列，按Function entry升序 |

`plan.renames[]`的精确字段集合是`entry, plate, post_name, pre, pre_name`；`source_contract.csv[]`的精确字段集合是`address, post_name, pre_name, pre_row`。Exporter真实CSV schema为：

`address,name,source,is_auto,is_thunk,length,namespace`

v3 checker先把9个整数`entry`正规化为canonical字符串，再与`source_contract.csv`逐项连接；库存CSV不再直接读取`renames[].address`。

### 九个rename目标

| address | post name | inventory source | is_auto |
|---|---|---|---|
| `0x08094f58` | `write_special_summon_material_rule_display_bit` | `USER_DEFINED` | `0` |
| `0x080a3c2c` | `check_banisher_sensitive_summon_allowed` | `USER_DEFINED` | `0` |
| `0x080a3d74` | `check_neo_bubbleman_summon_allowed` | `USER_DEFINED` | `0` |
| `0x080a3dac` | `check_gate_guardian_summon_allowed` | `USER_DEFINED` | `0` |
| `0x080a3eb4` | `check_valkyrion_summon_allowed` | `USER_DEFINED` | `0` |
| `0x080a4134` | `check_fusion_material_pair_slots_exist` | `USER_DEFINED` | `0` |
| `0x080a422c` | `get_special_summon_material_rule_by_card_id` | `USER_DEFINED` | `0` |
| `0x080a42b0` | `check_special_summon_material_rule_satisfied` | `USER_DEFINED` | `0` |
| `0x080a4574` | `check_necroshade_normal_summon_available` | `USER_DEFINED` | `0` |

九个`entry`均为exact integer，地址唯一且canonical排序后与source contract地址集合完全相等；九个pre/post name逐项一致。positive fixture要求上述九行name exact、`source=USER_DEFINED`、`is_auto=0`。

## v3 独立核验

| # | 检查 | 结果 | 独立证据 |
|---|---|---|---|
| V1 | inventory checker正例 | PASS | 在系统临时目录复制当前checker/test/plan后实际运行。构造5213行唯一、canonical、严格升序的7列CSV；结果`total=5213, named=5123, auto=90`，九个rename目标全部验证，renamed/auto projections逐行等于CSV投影，summary三项总数exact。 |
| V2 | inventory checker 15个负例 | PASS | contract缺字段、额外字段、entry字符串类型、重复entry、source-contract错误地址、count字符串类型，以及CSV缺列、额外列、地址格式错误、目标名错误、source错误、is_auto错误、总数错误、重复地址、字段非字符串，共15项全部拒绝。 |
| V3 | fixture清理 | PASS | `TemporaryDirectory`退出后`fixture_removed=true`；test报告`persistent_fixture_written=false`。本reviewer的隔离测试目录及fresh-dry目录也均已删除。 |
| V4 | 其他schema访问 | PASS | 独立扫描当前F13-Seg-7 pipeline：Jython `RefineF13Seg7.py`使用`renames[].entry`；source editor使用`source_contract.csv[].address`；source-scope对`plan.renames[]`只读`post_name`并对CSV合同读`address`；final checker只核renames cardinality。当前inventory checker中`contract["address"]`仅指`load_contracts()`返回的正规化对象。未发现同pipeline仍把原始`plan.renames[]`读取为`address`的路径。 |
| V5 | export wrapper自测位置与恢复 | PASS | wrapper在任何export、normalize、source edit和inventory export之前运行`test_f13_seg7_inventory_checker.py`；该步骤位于写后总`try/catch`中。自测非0时抛`INVENTORY_CHECKER_SELFTEST_FAIL`并调用restore。22-route测试已包含此新增失败分支且restore=1。 |
| V6 | 9个PowerShell wrapper词法与AST | PASS | 隔离运行当前validator：9个`run_f13_seg7_*.ps1`的compressed control flow=0、控制流命令碰撞=0、AST parse errors=0。 |
| V7 | 22条失败路线实际运行 | PASS | 3条apply写前拒绝restore=0；apply写后、persisted、inventory checker selftest、export/source/build/ROM、standalone source-scope及landing共19条写后失败均restore=1；`CommandNotFoundException=0`，runtime keyword probes全部通过。 |
| V8 | receipt和DB layout | PASS | count receipt接受exact/逆序，拒绝额外、缺项、错值、错名、null、字符串、浮点、bool及UInt64溢出；scalar只接受exact integer。DB layout允许合法generation轮换，拒绝fixed path变化；apply成功仍强制`dbChanged=true`、15/15及layout exact。 |
| V9 | fresh read-only dry | PASS | 使用只改写ROOT/RUN到临时目录的脚本副本，针对当前真实Ghidra工程执行`-noanalysis -readOnly` dry：exit0、success marker、`FAIL=0`、`semantic_actions_applied=false`、八项动作count exact，DB before/after 15/15逐项一致。临时结果已删除。 |
| V10 | retry2恢复状态 | PASS | 独立重算物理DB manifest、70-path source baseline、restore evidence、fresh prestate、authority集合和Git staged集合：DB=backup15/current15/exact，source mismatch=0，fresh prestate exit0/readOnly/noanalysis/db exact，authority=0，staged=0。 |
| V11 | final-preapply checker | PASS | 用只把输出重定向到系统临时目录的checker副本重新执行，读取真实repo状态；结果`F13_SEG7_FINAL_PREAPPLY_PASS_DRY_ONLY, FAIL=0`，输出SHA256仍为`9759baac83ead439e81269c01e44932b203feb4dacd7a8797035decd700c275e`，临时结果已删除。 |
| V12 | downstream落地合同 | PASS | persisted fresh read-only、export/mode/split、source scope、inventory、export_all、build、Python byte compare、`fc /b`、ROM SHA1和landing仍在统一restore保护下；ROM目标SHA1为`9689337d6aac1ce9699ab60aac73fc2cfdccad9b`。本review未运行这些真实落地步骤。 |

## v3 证据冻结

| evidence | SHA256 |
|---|---|
| `f13-seg7-preapply-backup.json` | `3f2b848200de1bd02c4e9c97d3b44c6c62264a0958b72b7a3b2649cc8f03aac6` |
| `InspectF13Seg7FullPrestate.py` | `4a8491751b9447771805a173133582e0797a65f461c11a93540b03231d564db1` |
| `f13-seg7-full-prestate.json` | `df66e641ac7d66a1197a4a73ac1e24c75b4651af551f00c0f1eac2e4bd96ec3f` |
| `f13-seg7-full-prestate-gate.json` | `9f24e63bfd53a012b96c654845b2354d122677ec03a1cc48aaa7c5368cc85275` |
| `f13-seg7-dry-result.json` | `8d80f6f3605fe39c58eb65ee7e5b9d5dc4536ce81de5dd519224b0e0e3379d76` |
| `f13-seg7-dry-gate.json` | `bd0fa603a1e970580a74654d56f6070c6261c95c35b24e104d3ffb12c792087f` |
| `f13-seg7-wrapper-validator-test.json` | `510983e394d4713790bed8bc2f5b06b990d979d2deedfaf8dd2d0e7c065466c3` |
| `f13-seg7-runtime-failure-path-test.json` | `108d4d7f725bea3d58c1b245fca10134bcade23027264332aade0d248f00d60d` |
| `f13-seg7-inventory-checker-test.json` | `b91e520432323563a603b86685aea4b63fcef6418f414493c1d674edc6513608` |
| `f13-seg7-retry3-recovery.json` | `dc3ed55e22b24960da36a2d8c159a13b349306ce9d5cd88c0f43112674c3ccad` |
| retry2 `f13-seg7-apply-headless.log` | `938e24aa01bf30746017ffc7464870adcea588bf54740bcfa097ade527273da2` |
| retry2 `f13-seg7-persisted-headless.log` | `b5c71d5d8440143e620442670db2da6e14cf75ffd3645b096d2c4109ee4c0514` |
| retry2 `f13-seg7-inventory-export.log` | `296362a3bf9628706e61c1613a900b1f9d5d0b9e46b35523eba1323d73972d63` |
| `f13-seg7-restore.json` | `a504883d262f0c21c68cb32241a84e991389647e0e5802500cf6ed7b60b1980b` |
| `f13-seg7-final-preapply-gate.json` | `9759baac83ead439e81269c01e44932b203feb4dacd7a8797035decd700c275e` |

## 冻结的 v3 implementation artifacts

| artifact | SHA256 |
|---|---|
| `tools/ghidra-labeling/RefineF13Seg7.py` | `3c446203ce84dabc92cb4cb5dbdabe422aa8ea497d7bb0a05db6269e0f368b28` |
| `f13-seg7-plan.json` | `772b89fab666c9ad09516aff6e3e8c3a3984db91d393cef99ede87e425edbe6b` |
| `f13-seg7-source-baseline.json` | `3c0376f0bec32b47e6e0b4f96669069d38f69e967e620a8ecd6f1f272b0644b0` |
| `check_f13_seg7_final_preapply.py` | `a95ce627893d3f99430f508ddf299dd7e07027a6933630da4baf154f5ef42fcb` |
| `run_f13_seg7_restore.ps1` | `a7dd126ead9afba1805bd10bf91bb51bd358a47e44ee0df24880db768075862f` |
| `run_f13_seg7_dry_gate.ps1` | `c4f80ca7d4c1599728669babb6c72242b175376b29aec7c90b9af1b9be923eac` |
| `run_f13_seg7_apply_gate.ps1` | `9a99a178edf8d17aacb0228d9b0d1e81998fb0c81fe2a54dfd74a5df04b80c6f` |
| `run_f13_seg7_persisted_gate.ps1` | `0086fcf0184214f459352e55fddd87a2a99f9e6018cb03811aac1b9c057838ad` |
| `run_f13_seg7_export_build_gate.ps1` | `9dda753bad1b2803677b6bc2ec8e9ea3e426c657b2c18535232faec939aa9cbd` |
| `run_f13_seg7_source_scope_gate.ps1` | `9f93d00ed1f1e96351f154d530de3716f2b726994f93a84692efa24cc6ec2507` |
| `run_f13_seg7_landing_gate.ps1` | `bb4aeff22bf199de10f65778c7b9e19f0650f72799cd8ec8290355c6d27497ed` |
| `run_f13_seg7_full_prestate_gate.ps1` | `193c4365b5fca823a5bc2cd44490d0c573f223b61a292e8a6318ec1849685191` |
| `run_f13_seg7_modea_prestate.ps1` | `3e2f418912d0bf40eb62f4f25f5e70ed4a87332bf4de27cd858442224adb6e28` |
| `test_f13_seg7_wrapper_validators.ps1` | `d6f9a32d9cda0d311ab78c22a17ee57f4037bda51b2ad4928a38a1c8288a5ed5` |
| `test_f13_seg7_runtime_failure_paths.ps1` | `a088444fc417d74425c9846f7b557389716695c1263b1f39f09d929dcab6c983` |
| `test_f13_seg7_inventory_checker.py` | `7f09c911ef89cadfdfea3b825e3d4c61ec88b87f9c8f1011ab146ca21300420a` |
| `check_f13_seg7_retry2_recovery.py` | `23b10e7c1541b6e9fb1645f32d3c4e95f4ca489b4bfe199e6b1927b2d4afa714` |
| `check_f13_seg7_retry3_recovery.py` | `cd0c0f293b86afc7b10a1ff02811000f2b115824cb9e7e09436e4679a9327951` |
| `apply_f13_seg7_source_edits.py` | `6f3def4a382e8b101c8876735f77ede31978ca39fbb3de6908a3d2506af6801c` |
| `f13-seg7-normalize-split.py` | `3950581c7cad1f2499fd3267a3916912b65c906a2c2e39a50afae4ab85c3fd9f` |
| `f13-seg7-source-scope.py` | `81ab19ed027a26744c7dea75125d78e5db4abbd3982e04cc2b18c6515ddc00fc` |
| `f13-seg7-inventory-check.py` | `f44bbe33ddafce19b1cc48425c8d52c39db34b631c05c66407837a6f72098b0b` |
| `f13-seg7-verify-rom.py` | `e4818ab261bd06ec322d393947319dcb88e3d267cfe965fa051d7c1fa5215449` |
| `check_f13_seg7_landing.py` | `7660c4db5372c7acb76bc0bb7441e301b4aa9d8b8a1baeff68d51de1b26d4abd` |

以上hash在real apply retry3前不得变化。本文不进入冻结语义hash链；root应在retry3前单独记录本文SHA256并重新核对final-preapply gate。

## 状态：PASS

批准root在重新核对上述v3 implementation/evidence hashes与final-preapply gate SHA后执行一次real apply retry3。之后必须按 persisted fresh read-only → inventory-checker selftest → export/mode/split → source edits → inventory export/check → source scope → export_all/build/fc/SHA → progress/landing 的顺序完成。任一写后门禁失败必须物理恢复DB与70-path source baseline，失败态不得提交。

## Implementation Reviewer Verdict: F13-Seg-7 = PASS
