# F13-Seg-7 Implementation Review v7

## 结论与授权版本

- 审查范围：retry4 写前 SHA 拒绝、当前静态哈希合同、恢复前态，以及 F13-Seg-7 Mode B 全流水线回归。
- **v1 至 v6 的 real apply 执行授权全部作废。** v6 的 PASS 已被 retry4 写前哈希失败消耗；本文是当前唯一 implementation review 执行判定。
- 本 reviewer 只读取正式仓库，并把测试报告输出重定向到系统临时目录。没有执行 real apply、export、build、stage、commit，也没有改动 Ghidra DB、正式 source、冻结语义文件或生产实现。

## retry4 写前事故与恢复态

retry4 使用的旧 apply wrapper 把 proposal 期望值写成 65 字符：
`129f42778a7ed9da2ec4e082da91d71577532e56016d4f2cb394e797a8d63a99f`；proposal 实际 SHA256 是严格 64 位小写十六进制：
`129f42778a7ed9da2ec4e082da91d71577532e56016d4f2cb394e797a8d63a99`。

当前实现已修正：

| 检查 | 结果 | 独立证据 |
|---|---|---|
| apply 冻结声明 | PASS | `run_f13_seg7_apply_gate.ps1` 的 proposal 值为正确 64 位 SHA；wrapper SHA256=`90cdcca8572edcc1a9ceaabf2f350e5f2ffd2800771ae8d6a832b1998cf78c85`。 |
| landing 冻结声明 | PASS | `check_f13_seg7_landing.py` 的 proposal 值相同；checker SHA256=`4bb3d8d822bc9a09860e2fa135e80aed26ecc607662b59e9c1cb33122ecb0bc3`。 |
| 写前顺序 | PASS | `$frozen` 格式、目标唯一和实算校验在 authority 清理、DB/source 检查、`try`、headless 参数构造及 headless 调用之前。 |
| `FROZEN_HASH_FAIL` 路线 | PASS | 隔离运行 26-route harness：唯一对应路线为 `pre_write_reject`，`restore_calls=0`、`expected_restore_calls=0`、`command_not_found=false`；headless invocation=0。 |
| retry4 写入事实 | PASS | 没有新增 apply receipt/gate、persisted/pipeline/landing authority 输出；当前 DB/source 均保持冻结前态。因此 retry4 未进入 Ghidra 或 source 写阶段，restore 不需要执行。 |

`f13-seg7-hash-contract-test.json` 中的 `retry4_rejection.restore_completed=true` 按“当前恢复态已经完整”解读；它不表示执行过 restore。实际调用次数由 runtime route 的 `restore_calls=0` 和 prewrite evidence 的 `restore_required=false` 共同约束。

## 静态哈希合同复核

### 覆盖与计数

当前 `test_f13_seg7_hash_contract.py` SHA256 为
`c00aa3c41aafaa7622b08113fff264dfbfe5c26a8e4504626cff67793c47d501`。我独立重建其生产声明集合，并逐条读取目标字节复算 SHA256：

| 声明组 | 数量 |
|---|---:|
| apply wrapper | 6 |
| persisted wrapper | 2 |
| Ghidra `INPUT_HASHES` | 18 |
| landing checker | 11 |
| final checker inputs | 29 |
| final checker implementation artifacts | 25 |
| retry4 prewrite checker reviews | 4 |
| plan input hashes | 17 |
| plan ROM segment hash | 1 |
| source baseline present rows | 70 |
| **合计** | **183** |

上述声明来自 8 个声明载体并覆盖第 9 个生产目标 ROM segment；baseline 的 70 个物理 snapshot 也逐项复算。结果为：

- 183/183 的期望值均恰好 64 字符，且每个字符仅为 `0-9` 或小写 `a-f`；63、65、非十六进制和大写值均未进入生产合同。
- 每组 key 唯一、目标路径唯一；全部目标存在，183/183 的实算值与声明 exact。
- proposal/review/TSV/plan/script/baseline/snapshot 的静态声明没有陈旧值；proposal 在 apply、landing、final、plan和 Ghidra 输入合同中的值均指向同一正确 SHA。
- `Get-FileHash`、`sha256()`、receipt/output hash 等运行时计算结果没有被误当作静态期望声明。保留在 incident evidence/checker 中的 65 字符旧值只用于证明 retry4 事故，不参与可执行冻结集合。

### 隔离正负测试

把正式测试代码原样执行、仅把 JSON 输出重定向到临时目录：

- 正例 PASS；声明数 183，snapshot 70/70，临时输出 SHA256 精确为
  `6ea26388b33920a9ae566d6219a5a7f8d6ee64aca4f49275e172faca6e0b5a35`，与冻结 evidence 相同。
- 7/7 负例按预期 code 拒绝：63 位、65 位、非十六进制、大写、错误值、错误目标、重复 key。
- 临时目录已删除；`persistent_writes=false`、`real_apply_executed=false`。

## v7 回归矩阵

| # | 检查 | 结果 | 独立证据 |
|---|---|---|---|
| V1 | wrapper 词法/AST | PASS | 9 个 run wrapper：compressed control flow=0、control-flow command collision=0、AST error=0。 |
| V2 | receipt/DB layout/wiring | PASS | exact integer、8 项 receipt counts、合法 generation 轮换、错误 layout、restore 与 landing wiring 全部通过。 |
| V3 | runtime 失败路线 | PASS | 26/26；3 个 prewrite 路线 restore=0，23 个 postwrite 路线 restore=1，CommandNotFound=0；`FROZEN_HASH_FAIL` 明确 restore=0/headless=0。 |
| V4 | inventory | PASS | 5213/5123/90；9 个 rename；真实字段 `renames[].entry`；15/15 负例拒绝；错误 `renames[].address` 访问=0；fixture 已清理。 |
| V5 | document updater | PASS | 真实两文档投影第一次 changed、第二次幂等；39/39 landing 合同负例及 5 个事务失败类全部拒绝并恢复；正式两文档字节不变。 |
| V6 | landing checker | PASS | Seg-8 仅接受 `[0x080a46a0,0x080a585c)`；39/39 负例拒绝；旧 `0x080a549c` 生产命中=0；source suffix gate exact。 |
| V7 | fresh dry evidence | PASS | `semantic_actions_applied=false`，动作计数 exact；`readOnly=true`、`noanalysis=true`、DB before/after exact、source 70/70、两文档 baseline exact。 |
| V8 | 当前恢复前态 | PASS | Ghidra DB=backup 15/15 且 path/size/SHA exact；source baseline 70 rows/70 unique、mismatch=0；authority output=0；staged=0。 |
| V9 | final checker | PASS | 将最终 JSON 重定向后读取真实 repo 重跑：exit=0、`FAIL=0`、failures=[]；输出 SHA256=`b4399daf09807e6400d1981ce3c4aad488b6179928a43ecf3ccc25ab95f65188`。 |

## v7 冻结 hash

### 语义与核心输入

| artifact | SHA256 |
|---|---|
| `F13-Seg-7.proposal.md` | `129f42778a7ed9da2ec4e082da91d71577532e56016d4f2cb394e797a8d63a99` |
| `F13-Seg-7.review.md` | `80fbd95458a16cb7faea369ff2051905b1b4cf6f8e5ebab9fb022ded0f60b926` |
| `F13-Seg-7.slots.tsv` | `2bd2619525cf56f5a996a2c8eb4dd91161958b1e825906d91e680e690221a99f` |
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
| `run_f13_seg7_export_build_gate.ps1` | `9dda753bad1b2803677b6bc2ec8e9ea3e426c657b2c18535232faec939aa9cbd` |
| `run_f13_seg7_source_scope_gate.ps1` | `9f93d00ed1f1e96351f154d530de3716f2b726994f93a84692efa24cc6ec2507` |
| `run_f13_seg7_landing_gate.ps1` | `f7f986f34ce7a3a4e1c810ba4c1e2284d79e43a7acad502a00290e7f30a18c1b` |
| `run_f13_seg7_full_prestate_gate.ps1` | `193c4365b5fca823a5bc2cd44490d0c573f223b61a292e8a6318ec1849685191` |
| `run_f13_seg7_modea_prestate.ps1` | `3e2f418912d0bf40eb62f4f25f5e70ed4a87332bf4de27cd858442224adb6e28` |
| `test_f13_seg7_wrapper_validators.ps1` | `a359b7587284016bc54f4ce34667f77f2aaee9f51332e4d5f09018f3075dac4a` |
| `test_f13_seg7_runtime_failure_paths.ps1` | `9d74aff7859ffc9db7cf44bb9517cac170ae01161d19329f7319c565838ea5cb` |
| `test_f13_seg7_hash_contract.py` | `c00aa3c41aafaa7622b08113fff264dfbfe5c26a8e4504626cff67793c47d501` |
| `test_f13_seg7_inventory_checker.py` | `7f09c911ef89cadfdfea3b825e3d4c61ec88b87f9c8f1011ab146ca21300420a` |
| `test_f13_seg7_landing_checker.py` | `d3ad94235f82d7a20ad2ba08d819064e50bb673d310812b55304bf8608aef66e` |
| `test_f13_seg7_document_editor.py` | `38e5a93616b7f582d26147fdb764ebd50778514c1d606ff9176fcea219b6d259` |
| `check_f13_seg7_retry2_recovery.py` | `23b10e7c1541b6e9fb1645f32d3c4e95f4ca489b4bfe199e6b1927b2d4afa714` |
| `check_f13_seg7_retry3_recovery.py` | `cd0c0f293b86afc7b10a1ff02811000f2b115824cb9e7e09436e4679a9327951` |
| `check_f13_seg7_retry4_prewrite.py` | `e3b6e583ce58c67315e516ac070fc5268987292cf5ab7b8446a54b6bf8d909d7` |
| `apply_f13_seg7_document_updates.py` | `892deaec08bb50ae57e8c3af6d7e13eac6c469350147651a7e06d13e54f75756` |
| `apply_f13_seg7_source_edits.py` | `6f3def4a382e8b101c8876735f77ede31978ca39fbb3de6908a3d2506af6801c` |
| `f13-seg7-normalize-split.py` | `3950581c7cad1f2499fd3267a3916912b65c906a2c2e39a50afae4ab85c3fd9f` |
| `f13-seg7-source-scope.py` | `81ab19ed027a26744c7dea75125d78e5db4abbd3982e04cc2b18c6515ddc00fc` |
| `f13-seg7-inventory-check.py` | `f44bbe33ddafce19b1cc48425c8d52c39db34b631c05c66407837a6f72098b0b` |
| `f13-seg7-verify-rom.py` | `e4818ab261bd06ec322d393947319dcb88e3d267cfe965fa051d7c1fa5215449` |
| `check_f13_seg7_landing.py` | `4bb3d8d822bc9a09860e2fa135e80aed26ecc607662b59e9c1cb33122ecb0bc3` |
| `check_f13_seg7_final_preapply.py` | `ae8a566c1fe250d9b1186012218949cc12db45cffd8fcd7c08d484c78a405c7a` |

### v7 关键证据

| evidence | SHA256 |
|---|---|
| `f13-seg7-hash-contract-test.json` | `6ea26388b33920a9ae566d6219a5a7f8d6ee64aca4f49275e172faca6e0b5a35` |
| `f13-seg7-wrapper-validator-test.json` | `9cd8e04490977c96aa1a1e0aecb39a71cb24ff06a059105ce413a73891f0eb91` |
| `f13-seg7-runtime-failure-path-test.json` | `f4e3b3041d1a88da0877895f3a4511ec454c41a890d5c688b9ad6d69163791c7` |
| `f13-seg7-inventory-checker-test.json` | `b91e520432323563a603b86685aea4b63fcef6418f414493c1d674edc6513608` |
| `f13-seg7-landing-checker-test.json` | `9099218377ea04eba2dad89e2b63c4d1326ecf5410ae60520f7cc25fe0159705` |
| `f13-seg7-document-editor-test.json` | `e71ccbf5dc5baa3a5052b44daa6c9c53e6143bb82f65c22bec1ac434d72df60f` |
| `f13-seg7-retry4-prewrite.json` | `866cb0f8844406062ba1780fed17ed4251470a954e1527744909c9a0504fb4c8` |
| `f13-seg7-dry-gate.json` | `6b3eb85674e47bc674c1efcc4dcf70b07102075c9e5531ff956648e0336afde8` |
| `f13-seg7-dry-result.json` | `8d80f6f3605fe39c58eb65ee7e5b9d5dc4536ce81de5dd519224b0e0e3379d76` |
| `f13-seg7-full-prestate-gate.json` | `9f24e63bfd53a012b96c654845b2354d122677ec03a1cc48aaa7c5368cc85275` |
| `f13-seg7-full-prestate.json` | `df66e641ac7d66a1197a4a73ac1e24c75b4651af551f00c0f1eac2e4bd96ec3f` |
| `f13-seg7-final-preapply-gate.json` | `b4399daf09807e6400d1981ce3c4aad488b6179928a43ecf3ccc25ab95f65188` |

以上 implementation/evidence hashes 构成 v7 执行冻结。real apply 前必须再次确认本文 SHA、上述冻结值、DB=backup 15/15、source=70/70、authority=0、staged=0 不变。

## 状态：PASS

批准 root 执行一次 real apply retry5。执行顺序保持 apply → persisted fresh read-only → export/mode/split/source/inventory → source scope → export_all/build/fc/SHA → production document updater → landing。任一写后门禁失败必须物理恢复 DB、70-path source 及两份文档；失败态不得提交。

## Implementation Reviewer Verdict: F13-Seg-7 = PASS
