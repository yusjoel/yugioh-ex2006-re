# F13-Seg-7 Implementation Review v6

## 结论与授权版本

- 审查范围：v5 `NEEDS_FIX` 后新增的生产文档updater、landing接线、两文档事务/rollback、70-path恢复合同，以及retry4最终写前门禁。
- v5 review SHA256精确为 `a253e8d322ea9c44f24d479b9b027f0b515b03dfecc71c06b748ca92b48eefc9`。
- **v1至v5的执行授权全部作废。** v4和v5均为`NEEDS_FIX`；本文是当前唯一implementation review执行判定。
- 本 reviewer只运行系统临时目录内的真实生产updater及其tests，并以输出重定向方式重跑final checker。没有执行real apply、export、build、stage或commit；正式活动文档、总进度、Ghidra DB与正式source均未被测试修改。

## v5判断订正

v5关于“70-path baseline不包含两份文档”的判断错误。原因是只用正斜杠字符串过滤JSON，而baseline内`paths[].path`使用反斜杠。按统一`\\ -> /`后独立复算：

- baseline `path_count=70`、`unique_path_count=70`、实际row=70、正规化唯一row=70；
- `doc/dev/p5-refine-13-equip-placement.md`与`doc/dev/refine-progress.md`各有且仅有一行，均为present；
- 两行在真实当前文件、baseline row和物理snapshot中的size/SHA256逐项相等；
- 活动文档当前/row/snapshot SHA256均为 `9b0d864c4577e1cbfc2da3559f29803c31069c77873fa71c997f269bc63d0fbb`；
- 总进度当前/row/snapshot SHA256均为 `001af9601fd56ca7615308d54b470aae26c2b2d48c68706b6c989facf0378acb`。

v5指出的生产文档updater缺失仍是有效缺陷，现已由 `apply_f13_seg7_document_updates.py` 与landing wrapper接线修复；baseline无需扩至72行。

## 真实生产updater独立执行

本 reviewer把正式当前两份文档按原字节复制到系统临时root，直接运行当前生产脚本 `apply_f13_seg7_document_updates.py`，不是调用手写activity/progress fixture。

### 正例与后态

| 检查 | 结果 | 证据 |
|---|---|---|
| 第一次运行 | PASS | exit=0，`F13_SEG7_DOCUMENT_UPDATE_PASS`，`changed=true`、`idempotent=false`、target_count=2。 |
| 真实landing合同 | PASS | updater产出的两份真实文档交给`document_contract_failures()`后failure为空；`poststate_extra_exact=true`。 |
| 活动文档 | PASS | 唯一`§4.07 F13-Seg-7`；Seg-7完成；Seg-8为`[0x080a46a0,0x080a585c)`；路线和§5.1状态exact；投影SHA256为`cc09a00f160dee8730e100629f0e07212a1b2e29591cd683bc09485a32454be9`。 |
| 总进度 | PASS | 唯一`file 13 Seg-7结果`行；顶部下一任务为Seg-8；file 13为7/10；总表为Seg-1..7完成；投影SHA256为`471f64ceb3cd3a73833ba7c8f7bfeb617544d3e20a2331c37564079ec37a2101`。 |
| 事故链 | PASS | 两文档均含12个精确字段：retry1词法失败/恢复；retry2 apply与persisted成功后inventory schema `KeyError`/恢复；retry3坏边界PREWRITE拒绝且Ghidra/source均NONE、restore为NOT_REQUIRED；retry4为FINAL_SUCCESS且landing为PASS。 |
| 二次运行 | PASS | exit=0，`changed=false`、`idempotent=true`，两目标hash与第一次完全一致。 |
| 正式文件不变 | PASS | 全部隔离用例结束后，正式两文档与测试前字节完全相同。 |

### fail-closed与双文件事务

| 用例 | 结果 | 原文件保持 | 临时残留 |
|---|---|---|---|
| 缺失锚点 | 非0拒绝 | exact | 0 |
| 重复锚点 | 非0拒绝 | exact | 0 |
| 状态漂移 | 非0拒绝 | exact | 0 |
| activity为后态而progress为前态的混合状态 | 非0拒绝 | exact | 0 |
| 写完第一个文件后注入第二文件失败 | 非0拒绝 | 两文件均rollback至原字节 | 0 |

所有失败均产生`DocumentContractError`且不产生report。真实生产输出再执行39个landing负例，39/39均以预期code拒绝。临时测试目录全部清理。

## landing生产顺序与恢复链

`run_f13_seg7_landing_gate.ps1` 在调用document updater之前读取并逐项验证：

1. apply gate与exact integer receipt counts；
2. persisted fresh read-only gate；
3. export/normalize/split/source/build gate及49/49；
4. source scope的5个changed modules与`0x080a46a0` suffix；
5. inventory 5213/5123/90、9个USER_DEFINED且`is_auto=0`的rename；
6. ROM size、SHA1和`fcExitCode=0`。

上述二进制门禁全部通过后，wrapper才运行document updater，验证2-target receipt与12字段，再运行landing checker。`DOCUMENT_INPUT_MISSING`、`DOCUMENT_PRECONDITION_FAIL`、`DOCUMENT_EDIT_FAIL`、`DOCUMENT_PROJECTION_FAIL`或`LANDING_FAIL`任一出现都进入同一catch并调用物理restore。

restore当前显式要求baseline 70/70唯一、两文档声明2/2、row唯一、snapshot size/hash exact；恢复后再次核两份正式文档size/hash，并执行fresh `-noanalysis -readOnly`语义前态。document update与landing gate均在planned transient paths中，失败恢复会清除。

## v6回归核验

| # | 检查 | 结果 | 独立证据 |
|---|---|---|---|
| V1 | 生产document updater | PASS | 正例真实文档投影合同为空，二次幂等；5个editor失败用例全部拒绝、双文档exact、temp=0。 |
| V2 | landing checker | PASS | 正确Seg-8 `[0x080a46a0,0x080a585c)`正例通过；39/39负例拒绝；旧完整范围生产命中0；suffix gate exact。 |
| V3 | baseline与正式文档 | PASS | 70 rows/70 unique；两文档各唯一且current/row/snapshot三方SHA exact；正式文档测试前后不变。 |
| V4 | restore接线 | PASS | DB物理15-file恢复、70-path present/absent恢复、两文档显式复核及fresh semantic prestate均在同一restore实现。 |
| V5 | PowerShell词法/AST | PASS | 9个run wrapper compressed control flow=0、control-flow command collision=0、AST error=0。 |
| V6 | 26条runtime失败路线 | PASS | 3条apply写前失败restore=0；23条写后失败restore=1，含4个新增document失败marker；`CommandNotFoundException=0`，静态/运行时路线exact。 |
| V7 | inventory | PASS | 5213/5123/90正例、9 rename、15个负例、fixture cleanup全部通过。 |
| V8 | fresh dry | PASS | `semantic_actions=false`、动作计数exact、DB before/after exact、source70/70与document baseline exact。 |
| V9 | 当前恢复前态 | PASS | DB=backup15/current15/exact；source70/70 mismatch=0；authority output=0；staged=0。 |
| V10 | final checker | PASS | 只重定向最终JSON、读取真实repo重跑，exit=0、`FAIL=0`；输出SHA256精确为`a9a4e6350400b9f26150b02d6f2cdd50d176f95744a7084c7d502bf68df9bd71`。 |

## 冻结语义与v6实现hash

### 语义输入

| artifact | SHA256 |
|---|---|
| `F13-Seg-7.proposal.md` | `129f42778a7ed9da2ec4e082da91d71577532e56016d4f2cb394e797a8d63a99` |
| `F13-Seg-7.slots.tsv` | `2bd2619525cf56f5a996a2c8eb4dd91161958b1e825906d91e680e690221a99f` |
| `F13-Seg-7.review.md` | `80fbd95458a16cb7faea369ff2051905b1b4cf6f8e5ebab9fb022ded0f60b926` |
| `f13-seg7-plan.json` | `772b89fab666c9ad09516aff6e3e8c3a3984db91d393cef99ede87e425edbe6b` |
| `RefineF13Seg7.py` | `3c446203ce84dabc92cb4cb5dbdabe422aa8ea497d7bb0a05db6269e0f368b28` |

### 生产实现

| artifact | SHA256 |
|---|---|
| `apply_f13_seg7_document_updates.py` | `892deaec08bb50ae57e8c3af6d7e13eac6c469350147651a7e06d13e54f75756` |
| `check_f13_seg7_landing.py` | `add2057c5c62827cfde7e1d52d1546ad6956464ada71d13c426afdda05132d4a` |
| `run_f13_seg7_landing_gate.ps1` | `f7f986f34ce7a3a4e1c810ba4c1e2284d79e43a7acad502a00290e7f30a18c1b` |
| `run_f13_seg7_restore.ps1` | `6ff3cb2866373f57d10d2b51259bbc854aea05216ca22cf38943a6423bb23da6` |
| `f13-seg7-source-baseline.json` | `a8e6419d64ba52bdbf70aff62f750303091e6298daa6a24af33db24301c90fd3` |
| `run_f13_seg7_dry_gate.ps1` | `6bece91563fd3b70004c56cf89f8b460c05672feb84e8ff826d858e49f7e10ce` |
| `run_f13_seg7_apply_gate.ps1` | `a4b55966a0c34f53d96c0c530fa7d73780096d1dbaea4dd4d544e94a236b7624` |
| `run_f13_seg7_persisted_gate.ps1` | `0086fcf0184214f459352e55fddd87a2a99f9e6018cb03811aac1b9c057838ad` |
| `run_f13_seg7_export_build_gate.ps1` | `9dda753bad1b2803677b6bc2ec8e9ea3e426c657b2c18535232faec939aa9cbd` |
| `run_f13_seg7_source_scope_gate.ps1` | `9f93d00ed1f1e96351f154d530de3716f2b726994f93a84692efa24cc6ec2507` |
| `run_f13_seg7_full_prestate_gate.ps1` | `193c4365b5fca823a5bc2cd44490d0c573f223b61a292e8a6318ec1849685191` |
| `run_f13_seg7_modea_prestate.ps1` | `3e2f418912d0bf40eb62f4f25f5e70ed4a87332bf4de27cd858442224adb6e28` |
| `test_f13_seg7_wrapper_validators.ps1` | `3ec768858117429c07f99749fb5a1e2efeeb78c81f11e05b54987b8db36da66e` |
| `test_f13_seg7_runtime_failure_paths.ps1` | `be0c70f5a3cda70be4a052461b868100c08fdc2c4d1e15c1b44d8c4f79a8f13b` |
| `test_f13_seg7_inventory_checker.py` | `7f09c911ef89cadfdfea3b825e3d4c61ec88b87f9c8f1011ab146ca21300420a` |
| `test_f13_seg7_landing_checker.py` | `d3ad94235f82d7a20ad2ba08d819064e50bb673d310812b55304bf8608aef66e` |
| `test_f13_seg7_document_editor.py` | `38e5a93616b7f582d26147fdb764ebd50778514c1d606ff9176fcea219b6d259` |
| `check_f13_seg7_retry4_prewrite.py` | `a779773b45c7b2f16125f32deb1e4f58431e8909c1cf4b5607938410066e18fe` |
| `apply_f13_seg7_source_edits.py` | `6f3def4a382e8b101c8876735f77ede31978ca39fbb3de6908a3d2506af6801c` |
| `f13-seg7-normalize-split.py` | `3950581c7cad1f2499fd3267a3916912b65c906a2c2e39a50afae4ab85c3fd9f` |
| `f13-seg7-source-scope.py` | `81ab19ed027a26744c7dea75125d78e5db4abbd3982e04cc2b18c6515ddc00fc` |
| `f13-seg7-inventory-check.py` | `f44bbe33ddafce19b1cc48425c8d52c39db34b631c05c66407837a6f72098b0b` |
| `f13-seg7-verify-rom.py` | `e4818ab261bd06ec322d393947319dcb88e3d267cfe965fa051d7c1fa5215449` |
| `check_f13_seg7_final_preapply.py` | `6552fd8768119f76729edc55d209fc5fe21e34817884c5f4cad2ba4d0c6c14dd` |

### v6证据

| evidence | SHA256 |
|---|---|
| `f13-seg7-document-editor-test.json` | `e71ccbf5dc5baa3a5052b44daa6c9c53e6143bb82f65c22bec1ac434d72df60f` |
| `f13-seg7-landing-checker-test.json` | `5d5706c675bf5c80e2d416b6d1e76dce0e743d7032c6872639ff4868fb8ed2b6` |
| `f13-seg7-wrapper-validator-test.json` | `826e0cfb859c751d7fd8ca73d0aa00170e7d1f04568696b925b1646638f61937` |
| `f13-seg7-runtime-failure-path-test.json` | `a16600edfab9861ee917ab8c9512df5e1c923b58188bfa3ae2748c348da35b23` |
| `f13-seg7-inventory-checker-test.json` | `b91e520432323563a603b86685aea4b63fcef6418f414493c1d674edc6513608` |
| `f13-seg7-dry-gate.json` | `6b3eb85674e47bc674c1efcc4dcf70b07102075c9e5531ff956648e0336afde8` |
| `f13-seg7-retry4-prewrite.json` | `10ade1bab6a910f7a653c063296563adf44d65c3c44633940b6e6530268cf07f` |
| `f13-seg7-final-preapply-gate.json` | `a9a4e6350400b9f26150b02d6f2cdd50d176f95744a7084c7d502bf68df9bd71` |

以上implementation/evidence hashes构成v6执行冻结。root在real apply前还必须记录本文SHA256并确认本表、DB=backup15/15、source=70/70、authority=0、staged=0未变化。

## 状态：PASS

批准root执行一次real apply retry4。执行顺序必须保持apply → persisted fresh read-only → export/mode/split/source/inventory → source scope → export_all/build/fc/SHA → production document updater → landing。任一写后门禁或任一文档门禁失败必须物理恢复DB、70-path source及两份文档；失败态不得提交。

## Implementation Reviewer Verdict: F13-Seg-7 = PASS
