# F13-Seg-7 Implementation Review v4

## 结论与授权状态

- 审查范围：`F13-Seg-7 [0x080a38fc,0x080a46a0)` 的 Mode B retry4 写前实现、retry3 事故前态、正式 Seg-8 边界、landing 文档合同以及完整失败恢复链。
- **v1、v2、v3 的 real apply 执行授权全部作废。** v3 保留为历史记录；retry3 在写入前因 v3 冻结的错误 Seg-8 边界 `[0x080a46a0,0x080a549c)` 被拒绝，没有发生 Ghidra DB 或 source 写入，也不需要 restore。
- 本 reviewer 仅执行只读检查、系统临时目录中的 fixture/runtime 测试和 fresh `-noanalysis -readOnly` dry。没有执行 real apply、export、build、stage 或 commit；隔离目录均已清理。
- 当前实现多数门禁通过，但 landing completion-record oracle 接受与真实 retry 序列矛盾的记录，因此 v4 verdict 为 **NEEDS_FIX**。当前 final gate `69b2dabb3cc860db6d5716f6d99d32488fe32174c1ac7aaa09fac5d7d350098d` 不构成 retry4 执行授权。

## retry3 事故与当前前态

| 检查 | 结果 | 独立证据 |
|---|---|---|
| retry3 是否写入 | PASS | `check_f13_seg7_retry4_prewrite.py` 报告 `v3_execution_rejected_before_write=true`、`additional_real_apply_in_retry4=false`、`restore_required=false`。 |
| Ghidra DB | PASS | 当前工程与冻结 backup 的物理 manifest 均为15个文件，path/size/SHA256逐项相等。 |
| source baseline | PASS | 70个 present/absent 合同逐项复算，mismatch=0；范围含 `asm/all.s.raw`、`asm/all.s.raw.nomode`、`asm/all.s` 与 output ROM。 |
| fresh semantic prestate | PASS | 真实 Ghidra 工程 `-noanalysis -readOnly` 查询 exit=0、成功标记存在、DB before/after exact；fresh gate为 `F13_SEG7_FULL_PRESTATE_GATE_PASS`。 |
| authority / staged | PASS | apply receipt、persisted、pipeline、scope、inventory、ROM、landing等11个 authority output均不存在；`git diff --cached --name-only`为空。 |

因此当前状态仍是合法写前前态，不需要因 retry3 再执行一次 restore。

## 正式 Seg-8 边界复核

正式下一段只能是 `[0x080a46a0,0x080a585c)`：

- `0x080a46a0` 是 `eval_card_placement_flags_for_ai` 的函数入口。
- 该区间依次包含7个函数入口：`0x080a46a0`、`0x080a4af4`、`0x080a5188`、`0x080a533c`、`0x080a5498`、`0x080a5714`、`0x080a57b8`。
- 下一函数 `check_equip_sub_entry_slot_pair_with_field_scan` 从 `0x080a585c` 开始；区间长度为4540字节。
- 旧终点 `0x080a549c` 位于 `check_equip_slot_pair_can_activate_full` 的 `0x080a5498` prologue 之后，会切断函数，不能作为段边界。
- 活动文档的拆段基线为 Seg-8 `[0x080a46a0,0x080a585c)`、Seg-9 `[0x080a585c,0x080a689c)`；`f13-seg7-source-scope.py` 仍强制 `0x080a46a0` 至 `asm/13_equip_placement.s` 末尾 suffix exact。

隔离重跑 landing checker test：正确 `0x080a585c` 正例通过，旧 `0x080a549c` 与其余8个负例共9项全部以预期code拒绝；41个生产合同文件中旧完整范围命中0，正确范围命中6。旧完整范围只保留在 `f13-seg7-landing-checker-test.json` 的 `wrong_range` 和 `f13-seg7-retry4-prewrite.json` 的 `wrong_next_range` 历史事故字段，不参与生产合同。

## v4 回归核验

| # | 检查 | 结果 | 独立证据 |
|---|---|---|---|
| V1 | landing 正确边界与9负例 | PASS | 正例 failure为空；9个负例全部拒绝且包含各自 expected code；旧范围生产命中0；source suffix gate为true。 |
| V2 | 当前活动/进度写前状态 | PASS | 当前真实文档仍为 Seg-7下一任务、Seg-7未开始、file 13为6/10，符合尚未获准执行 retry4 的前态。landing fixture已覆盖预期后态的 Seg-7完成、Seg-8表/路线、顶部下一任务和file 13 7/10行。 |
| V3 | 9个生产 wrapper 词法/AST | PASS | `throw'`、`return$`等压缩控制流碰撞为0，控制流命令碰撞为0，PowerShell AST parse errors为0。 |
| V4 | 22条 synthetic runtime 失败路线 | PASS | 3条apply写前失败restore=0；19条写后失败restore=1；`CommandNotFoundException=0`，runtime keyword probes exact。landing失败位于写后恢复路径。 |
| V5 | receipt、scalar与DB layout | PASS | count receipt接受exact及逆序，拒绝额外/缺项/错值/错名/null/字符串/浮点/bool/UInt64溢出；scalar要求exact integer。DB layout允许合法generation轮换，拒绝丢失、额外、fixed path变化和结构异常；成功apply仍要求`dbChanged=true`与15-file layout exact。 |
| V6 | inventory正例与15负例 | PASS | 5213行7列CSV正例得到`total=5213, named=5123, auto=90`；9个rename均为预期name、`USER_DEFINED`、`is_auto=0`；地址唯一、canonical、升序，projection与summary exact。15个负例全部拒绝，fixture已清理。 |
| V7 | fresh readonly dry | PASS | 真实工程 `-noanalysis -readOnly` dry exit=0、`FAIL=0`、`semantic_actions_applied=false`，73 EQ/19 REF/4 RENAME/96 EOL/9 FUNC_RENAME/14 PLATE/2 CARVE/9 old-name scan计数exact，DB 15/15 before/after exact。 |
| V8 | persisted与landing恢复链 | PASS | apply、persisted、export/mode/split、source edit、inventory、scope、export_all/build/fc/SHA、landing均处于统一写后restore链；诊断写失败不阻断restore。 |
| V9 | final checker重跑 | PASS | 将输出重定向至系统临时目录后读取真实repo重跑，得到 `F13_SEG7_FINAL_PREAPPLY_PASS_DRY_ONLY`、`FAIL=0`，生成输出SHA256仍为 `69b2dabb3cc860db6d5716f6d99d32488fe32174c1ac7aaa09fac5d7d350098d`。 |
| V10 | completion record事实合同 | **FAIL** | 当前checker只要求记录中出现字符串`retry1`、`retry2`、`retry3`、`§5.1=0`与下一范围；test正例明确写成`retry3成功`且没有`retry4成功`，与已确认的retry3写前拒绝事实矛盾。 |

## 确定缺陷

`output/refine-run-20260831-194634/check_f13_seg7_landing.py:64-67` 与 `:82-85` 仅用token存在性验证活动文档和总进度完成记录。`output/refine-run-20260831-194634/test_f13_seg7_landing_checker.py:20-40` 的两个正例分别写入：

`retry1 ...恢复；retry2 ...恢复；retry3成功；§5.1=0...`

这套oracle会接受“retry3成功、完全不记录retry4”的错误历史。实际事实是 retry3 在写前因旧 `0x080a549c` 边界被拒绝且零写入；只有未来通过本轮修复与重新审查后执行的 retry4 才能记为成功。completion record 是 landing 所要求的正式活动/进度事实，不是显示文本偏好；当前正例与事故证据互相矛盾，V10失败。

## 修改清单

### #1 — completion-record oracle 必须与 retry3/retry4 事实一致

1. 修改 `check_f13_seg7_landing.py` 的 `ACTIVITY_COMPLETION_RECORD` 和 `PROGRESS_COMPLETION_RECORD` 合同，要求两份记录都含有可区分的精确事实：retry1失败并恢复；retry2在inventory schema检查失败并恢复；retry3因旧Seg-8边界在写前被拒绝、没有DB/source写入且无需restore；retry4成功并通过landing；`§5.1=0`；下一任务 `[0x080a46a0,0x080a585c)`。旧`retry3成功`或缺失retry4成功必须拒绝。
2. 修改 `test_f13_seg7_landing_checker.py` 的 activity/progress正例fixture，删除`retry3成功`，改为retry3写前拒绝/零写入/无需restore以及retry4成功。对应两个completion-record负例必须分别删除或篡改这些新事实并命中指定failure code；保留正式 `0x080a585c` 正例、旧 `0x080a549c` 负例和完整负例覆盖。
3. 重跑 landing checker test，并冻结新checker、test、test evidence hashes。随后重生成 retry4 prewrite evidence，重跑wrapper validator及22-route runtime，更新 final checker 中所有受影响的expected hashes并重生成 final gate。
4. final checker必须纳入本v4 `NEEDS_FIX`，不能继续把 v3 PASS 当作执行授权。修复后必须由新的独立implementation review给出PASS；在此之前不得执行 real apply retry4。

## 当前已审查hash（不授予执行冻结）

### 冻结语义与核心实现

| artifact | SHA256 |
|---|---|
| `F13-Seg-7.proposal.md` | `129f42778a7ed9da2ec4e082da91d71577532e56016d4f2cb394e797a8d63a99` |
| `F13-Seg-7.review.md` | `80fbd95458a16cb7faea369ff2051905b1b4cf6f8e5ebab9fb022ded0f60b926` |
| `F13-Seg-7.slots.tsv` | `2bd2619525cf56f5a996a2c8eb4dd91161958b1e825906d91e680e690221a99f` |
| `f13-seg7-plan.json` | `772b89fab666c9ad09516aff6e3e8c3a3984db91d393cef99ede87e425edbe6b` |
| `RefineF13Seg7.py` | `3c446203ce84dabc92cb4cb5dbdabe422aa8ea497d7bb0a05db6269e0f368b28` |
| `f13-seg7-source-baseline.json` | `3c0376f0bec32b47e6e0b4f96669069d38f69e967e620a8ecd6f1f272b0644b0` |

### v4生产门禁实现

| artifact | SHA256 |
|---|---|
| `check_f13_seg7_landing.py` | `e220cb2073c049dc4e44249ffa7a78f653bad54a4105cb6ad2155bf736a84b28` |
| `test_f13_seg7_landing_checker.py` | `e45c7a9f6e03e09674dd1b83742a6a789f061acce5d04e19870bbc11df6cfdf9` |
| `check_f13_seg7_final_preapply.py` | `e2b2cdad9e169328c4698e27ff0a7a0da3b86bd4fc4c9a50abb9ea409684858e` |
| `check_f13_seg7_retry4_prewrite.py` | `756bc112f69efc6649e56ff97acad1e1ab6b0634422231d491a0104af8ac02cd` |
| `test_f13_seg7_wrapper_validators.ps1` | `6a97465d2c414c7d316d00765dd8c5fdf525a5238cda1854ec87f34537204138` |
| `test_f13_seg7_runtime_failure_paths.ps1` | `a088444fc417d74425c9846f7b557389716695c1263b1f39f09d929dcab6c983` |
| `f13-seg7-inventory-check.py` | `f44bbe33ddafce19b1cc48425c8d52c39db34b631c05c66407837a6f72098b0b` |
| `test_f13_seg7_inventory_checker.py` | `7f09c911ef89cadfdfea3b825e3d4c61ec88b87f9c8f1011ab146ca21300420a` |
| `run_f13_seg7_restore.ps1` | `a7dd126ead9afba1805bd10bf91bb51bd358a47e44ee0df24880db768075862f` |
| `run_f13_seg7_dry_gate.ps1` | `c4f80ca7d4c1599728669babb6c72242b175376b29aec7c90b9af1b9be923eac` |
| `run_f13_seg7_apply_gate.ps1` | `9a99a178edf8d17aacb0228d9b0d1e81998fb0c81fe2a54dfd74a5df04b80c6f` |
| `run_f13_seg7_persisted_gate.ps1` | `0086fcf0184214f459352e55fddd87a2a99f9e6018cb03811aac1b9c057838ad` |
| `run_f13_seg7_export_build_gate.ps1` | `9dda753bad1b2803677b6bc2ec8e9ea3e426c657b2c18535232faec939aa9cbd` |
| `run_f13_seg7_source_scope_gate.ps1` | `9f93d00ed1f1e96351f154d530de3716f2b726994f93a84692efa24cc6ec2507` |
| `run_f13_seg7_landing_gate.ps1` | `bb4aeff22bf199de10f65778c7b9e19f0650f72799cd8ec8290355c6d27497ed` |
| `run_f13_seg7_full_prestate_gate.ps1` | `193c4365b5fca823a5bc2cd44490d0c573f223b61a292e8a6318ec1849685191` |
| `run_f13_seg7_modea_prestate.ps1` | `3e2f418912d0bf40eb62f4f25f5e70ed4a87332bf4de27cd858442224adb6e28` |
| `apply_f13_seg7_source_edits.py` | `6f3def4a382e8b101c8876735f77ede31978ca39fbb3de6908a3d2506af6801c` |
| `f13-seg7-normalize-split.py` | `3950581c7cad1f2499fd3267a3916912b65c906a2c2e39a50afae4ab85c3fd9f` |
| `f13-seg7-source-scope.py` | `81ab19ed027a26744c7dea75125d78e5db4abbd3982e04cc2b18c6515ddc00fc` |
| `f13-seg7-verify-rom.py` | `e4818ab261bd06ec322d393947319dcb88e3d267cfe965fa051d7c1fa5215449` |

### v4证据

| evidence | SHA256 |
|---|---|
| `f13-seg7-landing-checker-test.json` | `faa6cab89223af2919c009339fe221eb631cde9a9f0ac5c0cc033a9549c97223` |
| `f13-seg7-retry4-prewrite.json` | `991e3a67257bc9feb5dbe96f77b4fb32cfdc2d3bb85f65c755aa1dc495e95461` |
| `f13-seg7-wrapper-validator-test.json` | `96ff2c4960cbf396d3c9bc996c840a69a4cb893927094a2a2e017f8bed9d1731` |
| `f13-seg7-runtime-failure-path-test.json` | `108d4d7f725bea3d58c1b245fca10134bcade23027264332aade0d248f00d60d` |
| `f13-seg7-inventory-checker-test.json` | `b91e520432323563a603b86685aea4b63fcef6418f414493c1d674edc6513608` |
| `f13-seg7-full-prestate-gate.json` | `9f24e63bfd53a012b96c654845b2354d122677ec03a1cc48aaa7c5368cc85275` |
| `f13-seg7-dry-gate.json` | `bd0fa603a1e970580a74654d56f6070c6261c95c35b24e104d3ffb12c792087f` |
| `f13-seg7-final-preapply-gate.json` | `69b2dabb3cc860db6d5716f6d99d32488fe32174c1ac7aaa09fac5d7d350098d` |

以上hash仅记录本次审查输入。由于V10失败，landing checker/test、retry4 prewrite evidence、final checker/final gate必须在修复后变化并接受新一轮独立审查；不得把本表解释为执行冻结。

## 状态：NEEDS_FIX

当前没有 real apply retry4 授权。完成修改清单、重新生成全部受影响证据并通过新的独立implementation review前，必须保持DB=backup15/15、source baseline=70/70、authority=0、staged=0。

## Implementation Reviewer Verdict: F13-Seg-7 = NEEDS_FIX(1 item)
