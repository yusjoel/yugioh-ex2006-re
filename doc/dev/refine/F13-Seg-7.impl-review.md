# F13-Seg-7 Implementation Review

## 结论

- 审查范围：`F13-Seg-7 [0x080a38fc,0x080a46a0)` 的 Mode B 实现及落地门禁。
- 语义输入保持冻结：proposal `129f42778a7ed9da2ec4e082da91d71577532e56016d4f2cb394e797a8d63a99`，TSV `2bd2619525cf56f5a996a2c8eb4dd91161958b1e825906d91e680e690221a99f`，semantic review PASS `80fbd95458a16cb7faea369ff2051905b1b4cf6f8e5ebab9fb022ded0f60b926`。
- 实现动作与冻结合同同构：`EQ=73, REF=19, RENAME=4, EOL=96, FUNC_RENAME=9, PLATE=14, CARVE=2, FIXED_OLD_NAME_SCAN=9`；Function create/delete、R4、§5.1 均为0。
- fresh read-only dry 已由本 reviewer 重新执行：exit=0，成功 marker 存在，`FAIL=0`，`semantic_actions_applied=false`，Ghidra DB 查询前后15/15文件逐项相等，当前 DB 与物理备份逐项相等。
- PowerShell validator 已由本 reviewer 实际执行：正常/逆序计数通过；额外、缺项、错值、错名、null、字符串、浮点、bool、UInt64 溢出全部拒绝；scalar 负测全部符合预期；所有 gate AST 错误数为0；旧 `return$false`/`return[...]` 压缩错误模式为0命中。
- real apply 产物均不存在，暂存区为空。本审查未执行 Ghidra 写入、export、build、stage 或 commit。

## 实现核验

| # | 检查 | 结果 | 独立核验 |
|---|---|---|---|
| I1 | plan/script 动作同构 | PASS | plan含96槽、8 targets、22段内Functions、9 renames、14 plates、65 body ranges、29 padding、305 edges；Jython逐项读取这些合同，dry/apply/check共用同一 `verify_frozen_plan`、prestate和poststate逻辑。三个odd callback保持EQ-only，不创建奇地址Symbol/Data/Function或DATA ref。 |
| I2 | 冻结输入 | PASS | Jython核 proposal/review/TSV/refscan/functions/edges/literal_reads/consumers/layout/prestate/backup/plan 共18项hash；apply wrapper再次核proposal/review/TSV/plan/script/source baseline。plan=`772b89fab666c9ad09516aff6e3e8c3a3984db91d393cef99ede87e425edbe6b`，script=`3c446203ce84dabc92cb4cb5dbdabe422aa8ea497d7bb0a05db6269e0f368b28`。 |
| I3 | 单事务与 rollback | PASS | real actions和完整postcheck位于同一Ghidra transaction；异常或断言失败以`commit=false`结束事务。apply/persisted/export-build/source-scope/landing gate的写后失败路径均调用物理restore。 |
| I4 | provisional receipt | PASS | apply前删除旧receipt/check；接受条件同时要求exit0、精确commit marker、receipt状态/FAIL/hash/八项count严格类型和值、DB内容确有变化、DB文件集合仍为15项。字符串、浮点、bool、null、溢出值均无法通过。 |
| I5 | fresh persisted | PASS | 单独的`-noanalysis -readOnly`进程先复核receipt/apply gate，再完整复算96槽、8 targets、Function ID/APCS/body、14 PLATE、odd callbacks、edges及残留自动名；结果必须含布尔 `PERSISTED_EXACT=true`，并与receipt的完整after capture相等。查询前后DB须15/15逐项相等。 |
| I6 | 物理DB备份/恢复 | PASS | preapply backup evidence冻结15文件relative path/size/SHA256，当前与备份一致。restore验证路径位于`ghidra`内，物理替换当前`.rep`、拒绝额外DB generation，并在恢复后再跑fresh read-only完整语义前态门禁。 |
| I7 | source baseline/恢复 | PASS | baseline为70条present路径、0 absent，含25 modules、全部现存`asm/*.s`、`all.s.raw`、`all.s.raw.nomode`、`output/2343.gba`、全部constants、CSV、registry、四inventory、活动/总进度及实现输入；每项有物理副本、size和SHA256。恢复按present逐字节覆盖并清理10项planned transient输出。 |
| I8 | export/mode/split/scope | PASS | export仅在persisted PASS后启动；全范围`080000c0..084c7637`，要求2个`.arm`+2个`.thumb`且只移除这4行，随后inject/split/split-check全为exit0、modules=25。source scope仅准modules02/04/12/13/23及批准的all/rom/constants/CSV/registry/inventory路径变化，Seg-8从`080a46a0`起后缀逐行不变，旧九名及`FUN_08094f58`为0。 |
| I9 | CSV/registry/inventory | PASS | source编辑器仅更新九个既有CSV地址行的name字段；registry更新八个既有tuple并新增唯一`FUN_08094f58` tuple，写后AST复核。fresh inventory要求total=5213、named=5123、auto=90，九个Function均为最终USER_DEFINED名。 |
| I10 | constants/aliases/carve | PASS | source编辑器精确新增11 constants、3 Thumb `+1` aliases及2个12-byte CID表；同名预检、原incbin唯一匹配及切割算术均为硬断言。source scope逐定义核值和唯一性，并核两table label及prefix/suffix incbin。 |
| I11 | export_all/build/ROM | PASS | pipeline要求`export_all.py` exit0且`完成: 49/49`、`build.bat` exit0；ROM gate同时要求两端size=33554432、Python逐字节相等、`fc /b` exit0、SHA1=`9689337d6aac1ce9699ab60aac73fc2cfdccad9b`。任一失败进入restore。 |
| I12 | landing与Git | PASS | landing wrapper用try/catch包围最终检查，任何失败调用restore；最终receipt只接受apply/persisted/pipeline/scope/inventory/ROM/进度全部通过且staged=0。当前real-apply/apply-gate/persisted/export/landing产物均不存在，`git diff --cached --name-only`为空。 |

## Fresh dry 与 validator 证据

- `f13-seg7-dry-result.json`: SHA256 `8d80f6f3605fe39c58eb65ee7e5b9d5dc4536ce81de5dd519224b0e0e3379d76`。
- `f13-seg7-dry-gate.json`: SHA256 `bd0fa603a1e970580a74654d56f6070c6261c95c35b24e104d3ffb12c792087f`。
- `f13-seg7-wrapper-validator-test.json`: SHA256 `e10223342ec722543d6ba8e6c7edac0fb6a13fbc072accedfcb3b40bde30fb5a`。
- `f13-seg7-final-preapply-gate.json`: `status=F13_SEG7_FINAL_PREAPPLY_PASS_DRY_ONLY, FAIL=0`，SHA256 `d53079a1601ed27edbb6e767bf3860bf6452d388b6b2475c704bd7512d2f3c27`。
- source baseline：SHA256 `3c0376f0bec32b47e6e0b4f96669069d38f69e967e620a8ecd6f1f272b0644b0`，70/70当前匹配。
- DB backup evidence：SHA256 `3f2b848200de1bd02c4e9c97d3b44c6c62264a0958b72b7a3b2649cc8f03aac6`，当前/backup均15项且逐项相等。

## 冻结的 implementation artifacts

| artifact | SHA256 |
|---|---|
| `tools/ghidra-labeling/RefineF13Seg7.py` | `3c446203ce84dabc92cb4cb5dbdabe422aa8ea497d7bb0a05db6269e0f368b28` |
| `f13-seg7-plan.json` | `772b89fab666c9ad09516aff6e3e8c3a3984db91d393cef99ede87e425edbe6b` |
| `run_f13_seg7_restore.ps1` | `a7dd126ead9afba1805bd10bf91bb51bd358a47e44ee0df24880db768075862f` |
| `run_f13_seg7_dry_gate.ps1` | `c4f80ca7d4c1599728669babb6c72242b175376b29aec7c90b9af1b9be923eac` |
| `run_f13_seg7_apply_gate.ps1` | `c2abe7047a59caf940fb981f024bb35c0af5bb10734b461c0514677a7ab40e7e` |
| `run_f13_seg7_persisted_gate.ps1` | `1d6a7b4fe8fef341cfff17d82c34a4a1a91f08909dfa4821a2373088be00b343` |
| `run_f13_seg7_export_build_gate.ps1` | `e9c51eeff7a4035289a58e9e7cb120d5a51342c51ede312000d202e1d2d0a4b2` |
| `run_f13_seg7_source_scope_gate.ps1` | `4b76f5bfbbb2a91cd5064b91161514046245ac1380a55135f5755ea33ee6935b` |
| `run_f13_seg7_landing_gate.ps1` | `47ae36c8669c2d9dcedf64f88430b5961416c6391c093c0daab1cc8e970ce4b6` |
| `test_f13_seg7_wrapper_validators.ps1` | `5c5c44cf3c50a25ebbdb379efe477627f2153eec0c83b0ddf9225ce0fa4071a1` |
| `apply_f13_seg7_source_edits.py` | `6f3def4a382e8b101c8876735f77ede31978ca39fbb3de6908a3d2506af6801c` |
| `f13-seg7-normalize-split.py` | `3950581c7cad1f2499fd3267a3916912b65c906a2c2e39a50afae4ab85c3fd9f` |
| `f13-seg7-source-scope.py` | `81ab19ed027a26744c7dea75125d78e5db4abbd3982e04cc2b18c6515ddc00fc` |
| `f13-seg7-inventory-check.py` | `a5ff45de7c057dfaed702e86d9b72e847d67dbdb33487c82e9a93282b151642a` |
| `f13-seg7-verify-rom.py` | `e4818ab261bd06ec322d393947319dcb88e3d267cfe965fa051d7c1fa5215449` |
| `check_f13_seg7_landing.py` | `7660c4db5372c7acb76bc0bb7441e301b4aa9d8b8a1baeff68d51de1b26d4abd` |

以上hash在real apply前不得变化。implementation review文档本身不进入Ghidra script的语义输入hash链。

## 状态：PASS

批准root在核对上述hash与 final-preapply gate 后执行 real apply；随后必须按 persisted fresh read-only → export/mode/split → source edits/scope → inventory → export_all/build/fc/SHA → progress/landing 的顺序完成。任何写后门禁失败必须物理恢复DB与70-path source baseline，且不得提交失败态。

## Implementation Reviewer Verdict: F13-Seg-7 = PASS
