# Refine Review: F15-Seg-6 — Round 3

## 最终冻结基线

最终manifest SHA256：c15a620a547d7b93195b2b486a78d26cfccdc9650205c91f8ab7a95f6e6092be。
正式proposal/slots/plates SHA256：

- d2ec956a2589e6e855c3a8c05c346f2215818f887948c472dba0550e06b51288
- bd736c3cd58d26bc0efddc2046ca8edc0df12c82501462a85e7894081fc8cc79
- fb74216d7ceeb29e7c1e7e0237ee0d130952cf141cd9365cd288b6c32af678fd

本轮为第二轮四组剩余项的最终窄复核。完整28项round2归档hash/size独立核对；此前机械扫描、ROM值、全局map、typed/formal/9odd/引用闭包及source/DB核验通过的证据保持，机器动作不扩大。首轮E238同址校准继续有效：LP+1d58与FieldArray+1c38均为0201e238，四处直接提交STR32写1。

## 窄差异与四组闭合

| 项 | 独立核验 | 结果 |
|---|---|---|
| #1 B414 | 新403字PLATE逐字采用review候选；顺序为207表→三路真正handler调用返回1→SkillDrain非零0→slots0..4内部提交/耗尽0。共享E244/E238及type9/5/8保持。 | ✅ |
| #2 B9B8 | 新462字候选逐字一致；phase1 commit0/失败和其他phase1写清。详细条款完整列6槽low13/+8/bit20计数、四早期检查极性、owner/type/CID override、最后post-gate fallback及STR32提交。 | ✅ |
| #3 C648 | 新402字候选逐字一致；display-advance0不读cancel、保持2/返回0；advance非零后cancel非零保持2/1、cancel0推进3/0。其他phase原真细节保持。 | ✅ |
| #4 文档合同/C168 | proposal明确旧incoming保留及两条新DATA。C168详细条款补齐LP+1cec、bit17、Chain Energy、strict/group、opponent effect-zone count及实际callee/返回表；424字PLATE逐字保持。 | ✅ |

实际递归差异仅为Function-plan三处after.plate、semantic三处text/长度、registry两处final_plate及外表state8 target_function_after.plate；正式TSV仅B414/B9B8/C648的new_plate/new_plate_chars六个单元变化。其余九条PLATE逐字不变。slot-plan、target-plan、19个段外owner、完整global map、18pins、pointer扫描和167-symbol图均与已验收v2字节完全相同。

全部formal/Function/semantic/registry及外表目标Function文本投影相等。缺席registry项继续缺席；无新的Function name、body、ABI、Data、Symbol或reference动作。

## 核验 (C1-C13)

| # | 检查 | 结果 | 证据/边界 |
|---|---|---|---|
| C1 | 地址序与范围 | ✅ | [080bb3dc,080bc71c)，Seg-5后按序，4928B。 |
| C2 | raw分类 | ✅ | 无段内raw；既有1982ins/160words/39零区不变；段外40B表carve。 |
| C3 | 全ROM扫描 | ✅ | 独立首/二轮raw+Thumb扫描证据保留，ROM/扫描合同字节不变，无5.1。 |
| C4 | 精确ROM值 | ✅ | 160槽与指令、97scalar、9odd callback及零项已核；slots和布局不变。 |
| C5 | 常量复用/GAS | ✅ | 57scalar复用+2新增；完整2429→2438/106绑定计划不变。 |
| C6 | 标签规范 | ✅ | 155源label及167主标签图不变，唯一无冲突。 |
| C7 | 类型/引用闭包 | ✅ | typed数组和真实Equate双schema、44DATA完整入站、qualified名及9odd补证保持；incoming文档矛盾消除。 |
| C8 | 现名/持久来源 | ✅ | 7既有registry PLATE-only、1原样、4真实缺席；新文本投影一致。 |
| C9 | ASCII/长度 | ✅ | 全12最终文本ASCII≤500；三候选403/462/402，C168保持424；全部新EOL保持。 |
| C10 | Thumb/host边界 | ✅ | 9callback+0、旧7odd refs、2even refs、2+40+120 host与state9终止不变。 |
| C11 | Function名/ABI | ✅ | 全部名称、ID、body/ABI保持。 |
| C12 | 真实分支与状态 | ✅ | 四组修正按实际指令闭合；BBBF8及C388/P1/P2前轮已核真细节保持。 |
| C13 | 残留与段外保护 | ✅ | 155auto+5switch覆盖；BC71C/BC784、18pins及历史04BECC84B保护保持。 |

## 状态: PASS

源码166个当前文件及其副本、正确pre-Seg6数据库15个当前文件及备份再次逐文件核hash/size相同；最终39条formal/plans/evidence记录及4条附加完整性记录和ModeA final摘要全部核对通过。复核仅写review与ignored审计，没有运行headless/build，也未改proposal、plans、正式源码、DB、进度、stage或commit。

本PASS批准的是本段proposal的C1-C13质量，后续ModeB Phase1仍需单独冻结实现、fresh/dry/强制回滚与独立实施审查。

## Reviewer Verdict: F15-Seg-6 = PASS
