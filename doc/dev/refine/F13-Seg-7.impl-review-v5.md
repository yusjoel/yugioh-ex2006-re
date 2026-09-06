# F13-Seg-7 Implementation Review v5

## 结论与授权状态

- 审查范围：v4 `NEEDS_FIX` 后的12字段 completion-record 合同、39个landing负例、生产文档投影路径，以及 F13-Seg-7 retry4 写前恢复状态。
- v4 review SHA256已核为 `6ac93da23900e6bcb85bf210211185ef92b4845d65302a0445ee91b3e917942f`。
- **v1、v2、v3、v4 的 real apply 执行授权全部作废。** v4本身是 `NEEDS_FIX`，没有提供执行授权。
- 本 reviewer 只运行系统临时目录内的checker、fixture、wrapper runtime和source-editor投影测试，并复算当前状态；临时目录已删除。没有执行 real apply、export、build、stage 或 commit。
- 修后的landing checker对合成文本已严格闭合，但正式生产路径不能生成该文本。v5 verdict为 **NEEDS_FIX**；当前final gate `126dc8c4e45f70c2041624a70a9f94103b0fe13b20c57a44912920935e385f31` 不构成retry4执行授权。

## v4缺陷修复本体复核

`check_f13_seg7_landing.py` 当前定义12个精确字段：

| field | exact value |
|---|---|
| `retry1_failure` | `POWERSHELL_WRAPPER_LEXICAL_FAILURE` |
| `retry1_restore` | `COMPLETE` |
| `retry2_apply` | `SUCCESS` |
| `retry2_persisted` | `SUCCESS` |
| `retry2_failure` | `INVENTORY_SCHEMA_KEYERROR` |
| `retry2_restore` | `COMPLETE` |
| `retry3_status` | `PREWRITE_REJECTED_BAD_SEG8_BOUNDARY` |
| `retry3_ghidra_write` | `NONE` |
| `retry3_source_write` | `NONE` |
| `retry3_restore` | `NOT_REQUIRED` |
| `retry4_status` | `FINAL_SUCCESS` |
| `retry4_landing` | `PASS` |

此外，完成记录必须各含一次 `§5.1=0` 和一次下一范围 `[0x080a46a0,0x080a585c)`。活动文档必须只有一个 `### 4.07 F13-Seg-7...` section；总进度必须只有一个 `> **file 13 Seg-7结果**:` 行。checker显式拒绝 `retry3成功`、`retry3=成功`、`retry3_status=SUCCESS` 和 `retry3_status=FINAL_SUCCESS`。

### 独立负测

- 隔离重跑正式test：正例failure为空，39个负例全部拒绝并含各自expected code；生成evidence SHA256与正式文件一致，为 `330086a902d452a6872004289ffc4101ee3facab9a71ad37640234189ff1e111`。
- 在正式39例之外，本 reviewer 对活动/进度两份记录的每个字段分别执行duplicate、key case-change、missing和tampered value，共96例；再加活动section重复、总进度结果行重复和显式插入`retry3成功`，合计99例，全部fail-closed。
- retry事实链与事故证据一致：retry1为PowerShell wrapper词法失败后恢复；retry2的apply和persisted成功，随后inventory读取错误schema触发`KeyError`并恢复；retry3因坏Seg-8边界在PREWRITE拒绝，Ghidra/source写入均为NONE且restore为NOT_REQUIRED；最终成功记录保留给retry4。

因此，v4指出的“checker接受retry3成功且不要求retry4成功”这一oracle缺陷，在checker及其合成fixture层已经修复。

## 确定缺陷：生产文档投影不存在

修复没有接入正式生产编辑路径：

1. 全部F13-Seg-7生产 `.py` / `.ps1` 静态扫描中，`retry3_status=PREWRITE_REJECTED_BAD_SEG8_BOUNDARY` 和 `retry4_status=FINAL_SUCCESS` 只存在于 `test_f13_seg7_landing_checker.py` 的合成fixture；没有生产editor包含这两段文本。
2. `apply_f13_seg7_source_edits.py` SHA仍为 `6f3def4a382e8b101c8876735f77ede31978ca39fbb3de6908a3d2506af6801c`。它只写 `constants/card_info.inc`、`constants/duel_field.inc`、`asm/rom.s`、`doc/dev/naming-proposals.csv` 和 `tools/ghidra-labeling/RenameKnownFunctions.py`，完全不读写活动文档或 `refine-progress.md`。
3. `run_f13_seg7_export_build_gate.ps1` 只调用上述source editor；`run_f13_seg7_landing_gate.ps1` 随后直接运行checker，也没有文档更新步骤。
4. 独立端到端投影测试复制真实写前文件到系统临时root并实际运行 `apply_f13_seg7_source_edits.py`。editor exit=0且报告11 constants、3 aliases、2 carves、9 CSV、9 registry；但活动文档与总进度SHA256均保持不变。将这两个真实editor输出交给当前checker，仍得到8项失败：`ACTIVITY_TOP_NEXT`、`ACTIVITY_SEG7_TABLE_STATUS`、`ACTIVITY_SEG7_ROUTE_STATUS`、`ACTIVITY_COMPLETION_RECORD`、`PROGRESS_TOP_NEXT`、`PROGRESS_TOP_COUNT`、`PROGRESS_FILE13_TABLE`、`PROGRESS_COMPLETION_RECORD`。

这证明当前test只验证了手写fixture，不验证retry4实际流水线能够产生landing所要求的文档。若按现实现执行，前置写入与构建通过后，landing必因真实文档仍是Seg-7未开始/6/10而失败并触发restore。

另有恢复覆盖缺口：当前70-path `f13-seg7-source-baseline.json` 不包含 `doc/dev/p5-refine-13-equip-placement.md` 或 `doc/dev/refine-progress.md`。直接加入生产文档写入后，现有restore不会恢复这两个文件；landing失败会留下不真实的完成记录。

## 其余回归结果

| # | 检查 | 结果 | 独立证据 |
|---|---|---|---|
| V1 | landing合成正例/39负例 | PASS | 正例通过；39/39负例按expected code拒绝；错误边界生产命中0；正式范围为`[0x080a46a0,0x080a585c)`。 |
| V2 | 唯一性与字段fail-closed | PASS | 额外99例覆盖12字段duplicate/case/missing/tamper、重复section/结果行及`retry3成功`，全部拒绝。 |
| V3 | 正式source editor输出 | **FAIL** | 实际运行后两份文档均不变，checker返回8项文档合同失败。 |
| V4 | wrapper词法/AST | PASS | 9个run wrapper的compressed control flow=0、control-flow command collision=0、AST error=0。 |
| V5 | 22条runtime失败路线 | PASS | 3条写前失败restore=0；其余19条写后失败restore=1；`CommandNotFoundException=0`，静态与运行时路线exact。 |
| V6 | inventory | PASS | 5213/5123/90正例、9个USER_DEFINED且`is_auto=0`的rename、15个负例及fixture cleanup全部通过。 |
| V7 | fresh dry | PASS | 当前final gate复核dry为`semantic_actions=false`、DB exact、source mismatch=0；冻结dry evidence与脚本hash均exact。 |
| V8 | retry4写前状态 | PASS | DB=backup15/current15/exact，source baseline=70且mismatch=0，authority output=0，staged=0。 |
| V9 | 旧边界残留 | PASS | 生产合同中旧完整范围`[0x080a46a0,0x080a549c)`命中0；事故JSON与历史review中的记录不参与生产边界。 |
| V10 | final checker | PASS但不充分 | checker exit=0、`FAIL=0`、final gate hash exact；它只核合成landing test，没有执行生产source editor→真实文档→landing checker的闭环，因此没有覆盖V3。 |

## 修改清单

### #1 — 建立可恢复的生产文档投影闭环

1. 新建专用生产文档editor，或为现有流水线增加等价的独立document mode。它必须从写前真实活动文档和总进度的唯一锚点生成完整后态，不得复制test fixture作为运行时输入。至少要原子更新：活动文档顶部下一任务、Seg-7状态行、Seg-8边界行、Seg-7路线状态、唯一`§4.07`完成记录；总进度顶部下一任务、7/10统计、file 13总表行、唯一Seg-7结果行。两份完成记录必须逐字产生上述12字段、`§5.1=0`及`[0x080a46a0,0x080a585c)`。
2. 将document editor接入写后restore保护路径，并且只在apply、persisted、inventory、source scope、export_all、build和ROM验证均通过后运行；随后立即运行landing checker。为document-edit与document-projection失败分别设置明确marker，二者均必须走restore=1。
3. 扩展可恢复基线，使 `doc/dev/p5-refine-13-equip-placement.md` 和 `doc/dev/refine-progress.md` 有物理snapshot、present/hash合同并由 `run_f13_seg7_restore.ps1` 逐项恢复。若并入现有baseline，则path_count从70调整为72，并同步apply precheck、recovery、prewrite、final checker及所有exact-count断言；不得只扩大editor而保留70-path恢复盲区。
4. 增加独立集成测试：在完整写前fixture root运行生产document editor，再把其真实输出交给 `document_contract_failures()`，要求failure为空、两份目标各唯一、12字段逐项exact。随后对生产输出执行当前39项负测。该测试必须确认失败fixture和临时目录清理，不得仅调用 `activity_fixture()` / `progress_fixture()`。
5. 更新landing wrapper、wrapper validator和runtime failure-path test；新增的两个写后失败分支必须实际运行且restore=1。同步所有受影响implementation/evidence hashes，包括document editor、baseline/snapshot合同、restore、prewrite、source/full-prestate、landing test、final checker与final gate。
6. 修复完成后保持无authority output和staged=0，由新的独立implementation review复核真实editor闭环。取得新的PASS前不得执行real apply retry4。

## 当前已审查hash（不授予执行冻结）

| artifact / evidence | SHA256 |
|---|---|
| `F13-Seg-7.impl-review-v4.md` | `6ac93da23900e6bcb85bf210211185ef92b4845d65302a0445ee91b3e917942f` |
| `check_f13_seg7_landing.py` | `22578afbcf4071be1faec1c318f94af7992f9dbd85657ed3cf8de211c7f96e04` |
| `test_f13_seg7_landing_checker.py` | `d3ad94235f82d7a20ad2ba08d819064e50bb673d310812b55304bf8608aef66e` |
| `f13-seg7-landing-checker-test.json` | `330086a902d452a6872004289ffc4101ee3facab9a71ad37640234189ff1e111` |
| `apply_f13_seg7_source_edits.py` | `6f3def4a382e8b101c8876735f77ede31978ca39fbb3de6908a3d2506af6801c` |
| `f13-seg7-source-baseline.json` | `3c0376f0bec32b47e6e0b4f96669069d38f69e967e620a8ecd6f1f272b0644b0` |
| `f13-seg7-source-scope.py` | `81ab19ed027a26744c7dea75125d78e5db4abbd3982e04cc2b18c6515ddc00fc` |
| `run_f13_seg7_restore.ps1` | `a7dd126ead9afba1805bd10bf91bb51bd358a47e44ee0df24880db768075862f` |
| `run_f13_seg7_export_build_gate.ps1` | `9dda753bad1b2803677b6bc2ec8e9ea3e426c657b2c18535232faec939aa9cbd` |
| `run_f13_seg7_landing_gate.ps1` | `bb4aeff22bf199de10f65778c7b9e19f0650f72799cd8ec8290355c6d27497ed` |
| `test_f13_seg7_wrapper_validators.ps1` | `6a97465d2c414c7d316d00765dd8c5fdf525a5238cda1854ec87f34537204138` |
| `test_f13_seg7_runtime_failure_paths.ps1` | `a088444fc417d74425c9846f7b557389716695c1263b1f39f09d929dcab6c983` |
| `f13-seg7-wrapper-validator-test.json` | `96ff2c4960cbf396d3c9bc996c840a69a4cb893927094a2a2e017f8bed9d1731` |
| `f13-seg7-runtime-failure-path-test.json` | `108d4d7f725bea3d58c1b245fca10134bcade23027264332aade0d248f00d60d` |
| `f13-seg7-inventory-checker-test.json` | `b91e520432323563a603b86685aea4b63fcef6418f414493c1d674edc6513608` |
| `check_f13_seg7_retry4_prewrite.py` | `add9dc7e96220cc59a19a487d2c367b4604557d9585eb4bae51a25b1bd2e6354` |
| `f13-seg7-retry4-prewrite.json` | `a7b97a5135ec5ff153096fb6ab5fd7341cb6bf9d4d927b38105794158411dc46` |
| `check_f13_seg7_final_preapply.py` | `0cd9601601207fa1f38558752f3fa18b5de5bb61ae46d5deee79025184135a2d` |
| `f13-seg7-final-preapply-gate.json` | `126dc8c4e45f70c2041624a70a9f94103b0fe13b20c57a44912920935e385f31` |

以上hash只记录本次审查输入。由于生产文档投影闭环缺失，它们不得解释为retry4执行冻结。

## 状态：NEEDS_FIX

当前没有real apply retry4授权。retry4仍应在最终完成记录中写作`retry4_status=FINAL_SUCCESS`与`retry4_landing=PASS`，但只有实际流水线成功且landing通过后，该记录才可保留在正式文档中。

## Implementation Reviewer Verdict: F13-Seg-7 = NEEDS_FIX(1 item)
