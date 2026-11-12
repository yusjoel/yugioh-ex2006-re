# Refine Review · F16-Seg-2 · 第二轮

## 状态 PASS

本轮只复核首轮I1/I2关闭及完整正常回归。范围 `[0x080c2544,0x080c36a8)`，4452B。17份语义产物、proposal、producer与批准原语保持原字节，首轮已通过的语义和机器动作继承。当前manifest `d1a38ca32b9c91584383195a16c36a5034ade3436ac0e0af610aa716081f20fe`，source JSON `30f7d560d135585a573e2b041a5e2e9549a757af92cc6cdfecae62507ae3ee13`。首轮原件完整保存在 `f16-seg2-review1-final-archive/`，原analysis26件保存在 `f16-seg2-analysis-before-review1-fix-archive/`。

## C1-C13 复核

| 项 | 结论 | 证据 |
|---|---|---|
| C1 地址序 | PASS | Seg-2紧接已完成Seg-1，15入口，4452B范围不变。 |
| C2 raw归宿 | PASS | 1751 mnemonic与100真实InstructionDB `.hword`、145word、25处2B padding连续覆盖，raw0。 |
| C3 独立引用扫描 | PASS | 首轮独立raw/THUMB扫描与本轮完整validator重跑一致，8个改名函数、25引用目标；C3081两命中逐字节对应4800B像素record，§5.1为0。 |
| C4 数值/字节 | PASS | 145word小端值、39EQ及整段指令/字节/DataType/TMode保护不变。 |
| C5 常量域/复用 | PASS | 新EQ8/新target12/GNU20保持；AOB高16 tilebase、低4 palette-base事实不变；0x404消费者为OBJ tiled目标偏移。 |
| C6 名称/静态身份 | PASS | 118自动槽全覆盖，source lower_snake；12新target原DEFAULT或无symbol；64位静态ID和ANALYSIS switch aliases保持。 |
| C7 全图/引用 | PASS | 119完整Fn/3097state/16452指令属性，57新DATA/22旧引用保持；全图、ABI/body、bytes、owner投影合同保持。 |
| C8 现名/范围 | PASS | 八rename、14段内PLATE+1保留、两必要C8、七dispatcher BL、registry16既有tuple及CSV八name cell保持。 |
| C9 ASCII | PASS | 新PLATE/EOL均ASCII，PLATE<=500。 |
| C10 GAS/native | PASS | 实际producer两遍各17输出；完整独立validator执行真实resolver AST各145次。137native/8新pins/115继承pins及20GNU闭包精确。 |
| C11 误名 | PASS | reset/init/setter及UI效果、decimal非零marker八命名消费者证据不变。 |
| C12 语义 | PASS | FFFFF807清3..10、AOB palette域、每次scatter576B和1152B双半记录、count0 tag与OAM公式维持已审事实。 |
| C13 严格验证 | PASS | 完整96反例均拒绝，17严格int正例、34float/bool拒绝、typed引用重排及空list正例、真实tuple解码边界均通过；原四个误接受逐项原样拒绝。 |

三硬规则满足，carve/disasm/§5.1均0。R1-R9分析层核验通过。本结论为分析质量通过，实际Ghidra演练、保存、源码重导、构建和整ROM逐字节验证由后续实施门禁完成。

## I1 关闭证明

`typed_references` 在Counter之前要求actual与独立expected均为严格list，每行严格dict且key集合精确为address/operand。address必须为八位小写hex字符串，operand必须严格int，bool/float拒绝。随后按完整JSON字段的无序多重集比较并保留重复数。

原零引用Eq的 `references=[]` 改为 `{}` 已在完整validate入口拒绝。空list与引用排列正例正常，增删/重复替换/额外字段/缺operand/地址类型与格式反例拒绝。独立辅助测试另核11个坏形状/类型及重复数可区分。

tuple测试在真实validate的JSON解码边界精确匹配原global文本，定点将 `set_equip_activation_state_by_mode.references` 改为tuple后进入原validator。实际拒绝来自 `global.actual.set_equip_activation_state_by_mode: reference list required`，decoder命中1次、实际类型tuple、code object保持，finally恢复原json。tuple未经过JSON重新序列化。

## I2 关闭证明

17个计数/大小字段全部先要求 `type(value) is int`，再比独立canonical、批准集合或真实AST结果派生值。AST有13处literal调用加global四项循环，覆盖首轮审计全部17字段。GAS expression_assertion_count及native native_exact/fallbacks已接通真实145/137/8结果。

完整负例套件逐字段执行17个int正例与34个float/bool反例。原fullstate `3097.0`、global after_count `2487.0`、registry new_tuple_count `false` 均在实际完整validate入口以AssertionError拒绝。decisions.counts、actual_ast_calls及scope内原严格计数保护保持。

## 实际重放与保管链

读取并执行固定JSON内 `runner_source` 的全部顶层语句，直到最终manifest打印。producer调用两遍，各17输出逐字节一致；完整独立validator正常通过；全部96负例、17int正例、typed引用重排/空list及tuple边界均真实执行。

reviewer仅在内存捕获 `Path.write_bytes/write_text` 输出，正确采用Windows默认CRLF转换。最终22个捕获输出，包括17语义件、proposal和四份运行元数据，全部与冻结包逐字节相等。首轮捕获器换行问题在本轮完整重放中已消除。

独立保管链核24 records、13 inputs、旧26件archive和review1 archive，source197 current/copies及正确DB15 current/backup均精确，共493个唯一实际文件。四个原元数据文件变化与ModeA许可一致，其余17语义件、proposal、producer和原语保持。

## 独立证据

RUN为 `output/refine-run-20261028-105948/`。

- `f16-seg2-reviewer-R2-fullrunner-execution-v1.json`，完整顶层执行、96反例、22输出byte-exact和原始stdout。
- `f16-seg2-reviewer-R2-residual-closure-v1.json`，原四反例、17字段逐项正/负与tuple实际入口对应。
- `f16-seg2-reviewer-R2-private-component-cases-v1.json`，typed集合/行类型、重复数与17int/34坏类型辅助实测。
- `f16-seg2-reviewer-R2-static-component-preaudit-v1.json`，原AST窄差异、17字段调用、producer与17语义件保持。
- `f16-seg2-reviewer-R2-custody-v1.json`，493文件实际size/SHA。
- 首轮独立layout/refscan与fullmodel证据按相同字节继承，旧review/audit原件均在不可变review1 archive。

## 修改清单

无残项。实施阶段仍须实际演练、独立保存后检查、源码/ROM验收和本段提交。

## R5 checkpoint1：派生显示模型独立复核

状态：PASS，仅限模型材料化 checkpoint1。当前 analysis manifest 为 `9467beced2a452515cc4a02546484acf28bcec546fd37d8d0ec875305eb5ce53`，source JSON 为 `301dcaaec43002c335ad593ec636832bc5337640b788407df85ef932d840d2f1`。

独立逐字节核实：原17产物中14件保持原字节；另外3件仅有批准的8处 after 引用名称变化，全部 before 保持。新增辅助计划采用实际原生 getter 的 standard_c2、tiny_c2、tiny_c4 完整结构；主 canonical 仍为3097状态，既有动作、119函数、16452指令属性、GAS及源码范围不变。

实际执行 producer 两遍，各18输出均与当前材料逐字节一致；完整 normal validator 正例及7个受本增量影响的反例通过。原96反例源码保持字节一致，封存正常 runner 日志5289记录96项真实拒绝；本轮继承该回归，不重复运行无关旧项。独立重放当前 derived152完整入口，最终证据与封存a88c逐字节一致。

Root独立辅助模块只从原生 before getter 与 canonical owner 派生期望。发现的引用顺序误拒已修复：当前模块 `50badc7bf35f73d890b27cf33adf22676bc4faae12759d04364c02bfa88a273d` 在三个阶段的重排正例及重复、ID、owner、namespace反例共18项通过。saved verifier v3 `105023bab0879e38ff3a8b4bdf6eb0ad08b3084973e8f0221407336f2eeee1fb` 保留原主比较，仅新增精确4引用投影与完整辅助/DB链；其完整 main 纯内存夹具通过，磁盘 FREEZE 仍明确 PENDING。

独立报告：`output/refine-run-20261028-105948/checkpoint1-review-r5.json`。证据包括同RUN的 `f16-seg2-derived-checkpoint1-reviewer-{delta-custody,normal-entry,152-replay,root-aux-fixed,saved-main}-r5.json`。

本节不代表 Script 已实施、保存后验证或完整回滚通过。Script043a与历史快照03c保持原字节；下一步仍须准备新 Script、替换202快照、冻结准确新绑定，并重新完成真实只读与保存/源码/ROM门禁。当前不授权保存。

## Reviewer Verdict: F16-Seg-2 = PASS


## Root 最终落地验收（2026-11-13）

结论：**COMPLETED_BYTE_IDENTICAL**。执行前冻结的 review SHA256 为 `31ffd7220733e58880cd14f19eaa34bf9529da66098f1f43376aa084479e710a`，其原件保存在新 202 文件执行快照中；本节为执行后的验收追加。

- R5 真实 prestate、dry、完整 owned fullrollback 均通过，transaction 1242 的 post 及同 Program 核心/辅助前态恢复均 0 FAIL；三模式 DB15/source202 逐字节不变。最终独审 `0d18ac3059f1f25b367e2517d498729c231dc3fc2a781beb2bd676474a09115b`。
- 唯一保存成功（`60cdea828622405d0fdbfbdd82e0b96b0e85fe822079ab62ae23b51610d26c6f`），新进程 check 成功（`7ece3c3c4807a2cf7fe88d76354330afb01e8cc4bf9169e3f27f1a93d8bd725b`），不重复 apply。
- 独立原生后验覆盖 119 Function、3097 核心状态、130 新标签、138 primary 节点、2487 全局 Equate/12725 绑定及 c2/c4 完整辅助状态；4 条派生引用和另外 27 条 DEFAULT `+` 引用精确。数据库门禁 `de1563b3b4a554b44a1d6a6339193503d31507b697fdfad5277bae8cadac2967`。
- 16452 个指令位置仅投影 1086 个批准 owner 名字段，flow type 和 override 精确；指令门禁 `37555c0a596e75ca262940b9a3cde1b1301007bd6c9fba0d44d237e143ff6b99`。
- 137 native、123 有效 pins、145 表达式断言、20 GNU 定义、16 registry tuple、8 CSV name cell 和源码 15 项许可内精确 13 路径变更均通过。49/49 资产、构建及 33554432B 整 ROM 逐字节相等；ROM SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`。流水线门禁 `7c8a2c9612f3712778e34825bc50f83b561285ff27aad6ceb3268b9dd63df8ad`。

总进度已更新为 2/10。单段提交后立即按地址序进入 F16-Seg-3 `[0x080c36a8,0x080c4350)`。
