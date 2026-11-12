# Refine Review: F16-Seg-1（第四轮）

## 状态: PASS

本轮只复核review3唯一GNU primitive闭包及正常全量回归。已通过的语义、机器动作和物化合同不再扩展；全部残项关闭。此PASS仅为**分析质量通过**，不代表Phase1实施、Ghidra保存、源码重导或ROM构建获准。

冻结依据：

- manifest-v4 SHA256 **730d93f6856303a06a4cc7124d38951e890357324f73a5862d90b368fd7378ed**
- validator-v4 SHA256 **203992f88ff484b1e8256f3a2d5cfcfd91e72256402cd1a34a6a507baa41bee7**
- producer-v4 SHA256 **0aa282106c79bea2393845eab9285bfa18599c804557274b95acaf3619ab7a35**
- canonical v2 SHA256 **a434a23cb683de9e27fad9a9f7bcbfbe855fa8171d278bb07811d29846f60aeb**

## 核验 (C1-C13)

| # | 检查 | 结果 | 最终证据 |
|---|---|---|---|
| C1 | 地址序/路线图 | ✅ | 文件16首段[080c1448,080c2544)，4348B；无跳段。 |
| C2 | 全raw归宿/布局 | ✅ | 1648指令3444B+210word840B+32处padding64B，ROM字节连续覆盖4348B；raw0，155自动源名全覆盖。 |
| C3 | 独立raw+Thumb扫描 | ✅ | 正常回归重扫5rename/34target，与冻结结果相同；相同ROM/地址集合继承首轮7Fn/210源扫描。无本段§5.1/carve/disasm。 |
| C4 | 值/小端/GNU表达式 | ✅ | 210 ROM字与完整布局重核；formal3/plans13对v3/v2逐字节相同，继承22新GNU及304表达式真值证明。 |
| C5 | 复用/常量域 | ✅ | 7fff为DISPCNT_OBJWIN_CLEAR_MASK@gba_io；BGR555_WHITE旧对象不动；SPARK_BLASTER_CID<<19=C8480000，44c0的OAM域正确。 |
| C6 | 标签/碰撞 | ✅ | 155源+19新目标+5稳定ID Function形成179变化primary节点；lower_snake、静态身份与命名空间约束保持。 |
| C7 | 按名连接/完整after | ✅ | reviewer从canonical独立重派生210slot/34target/117Fn/2181state，after差异0；58新DATA无重复、109旧边CORE6、7overlap、126qualified副本保持。 |
| C8 | 现名/registry/scope | ✅ | 7既存tuple=5name+PLATE+2comment-only、15path/34引用文本合同严格保持，无历史材料泛替换。 |
| C9 | ASCII | ✅ | 7新PLATE/155新EOL全ASCII；新PLATE<=500；两pack PLATE及外部context写入边界保持。 |
| C10 | GAS/native/carve | ✅ | 真实symbol/equate各210调用；189native/21真正fallback、94继承/115有效pins。无新增段外typed-DATA表达式范围；无carve。 |
| C11 | 函数名 | ✅ | 两个count-domain修订及另三名称的消费者证明继承v2通过；五rename不扩。 |
| C12 | 阶段/状态/返回语义 | ✅ | count动画、按arg3-1存储、9/33/9 OAM时长、AND0xfb只清field bit2等已审事实与全部副本不变。 |
| C13 | 独立来源/严格验证 | ✅ | GNU22先独立派生并严格核再进入model；真实54negative全拒绝，reviewer原样三GNU反例及三schema/order/type反例全部在model前拒绝；两遍16输出byte-exact，历史仅绑定不可变归档。 |

三硬规则均满足：严格首段地址序；本段无未处理函数间raw；未将正引用块登记§5.1。历史正引用backlog未宣称在本段关闭。

R1-R9最终结论：常量域/值、标签、按名连接、注释/消费者语义、无raw的R4/R7及资源功能命名已通过；R8没有新增无证据的像素/glyph身份。R9已核正确saved-S15-Seg10的source192/DB15备份双份，本轮未运行build；实际实施仍须独立审批、备份和整ROM逐字节验证。

## review3 唯一项关闭实证

1. **expected独立来源**：expected_gnu_definitions仅读取批准EQ/REF最小primitive表，按顺序构造3个new Eq+19个new Label；未读取pending或归档完整GNU DTO作为expected。
2. **完整严格比较**：name/value/expression/file/kind、完整key集合、类型、数量、顺序、唯一性均由strict_equal及基数检查约束。SPARK表达式保持(SPARK_BLASTER_CID << 19)，mask/OAM的gba_io/oam_attr文件域正确。
3. **消费顺序**：validate_documents先执行validate_gnu_primitives，再调用已审v3的正常模型。故继承BASE.approved_model读取new_target_values之前，pending列表已被证明与批准定义完全相等。
4. **四方接通**：所有22项与source-scope相应inc名称清单、globalEq数值、target状态/地址/file、EQ/REF decision值一致；后续v3完整canonical派生继续严格核这些合同。
5. **真实旧反例**：原样将mask value改1、file改rom_data、name改UNAPPROVED_MASK_NAME，均由真实validate_documents拒绝。坏value用custody=True/native=True调用，在任何model进入前直接失败；无需继续跑本应被阻止的native或事务路径。
6. **模型前拒绝证据**：仅给原approved_model套一个记录后原样转发的观察器，不改变expected、返回值或拒绝逻辑。三个旧反例及额外字段、列表倒序、int替hex-string三个窄反例，观察到model调用数全部0。
7. **完整正常回归**：实际validate()返回PASS，结果与冻结validation-v4逐对象一致；旧46+新增8 GNU共54真实入口negative全部拒绝。正常native两函数各210次均真实执行，不以字符串PASS代替。
8. **无动作变更**：正式三件及13plans对v3归档byte-exact，当前117Fn/2181state独立模型0差异，43EQ/58ADD/54REFP/55PRES、5rename/7PLATE、2479对象/12686bindings、22GNU、189/21、115pins均不变。

## 保管链与复跑

- 本轮40冻结record逐size/SHA核对；source192当前/副本、正确DB15当前/备份均精确。
- v1/v2/v3归档48/63/46文件全部保持；manifest/basis/result没有活动review历史绑定。更新本正式review后，40记录仍应全部精确。
- 真producer-v4.write_evidence执行：底层真实generator在内存capture两遍，16个输出每个都等当前冻结字节；三个归档review按真实SHA检查。
- 真validator-v4.validate执行：固定证据写入仅在进程内捕获；native读回采用刚生成的实际内存内容，未以旧expected冒充actual，未覆盖fixer任何文件。
- review3的三GNU反例另行独立重放；正常完整typed/model、字节、Eq和历史回归执行，已通过语义仅按相同物化文件继承，不重新扩分析范围。

## 独立证据

RUN=output/refine-run-20261028-105948/：

- f16-seg1-reviewer-mechanical-v4.json：40记录/source192/DB15、完整canonical前后态、ROM/refscan/Eq正常回归。
- f16-seg1-reviewer-delta-history-v4.json：formal3+plans13字节不变、三版归档与来源历史。
- f16-seg1-reviewer-provenance-v4.json：真实producer/validate、54拒绝、正常420native、三旧反例及schema/order/type观察；附实际执行源码及SHA。
- f16-seg1-reviewer-audit-v4.json：本review及所有独立证据实际path/size/SHA和最终保管链。

## 修改清单

无残项。实施质量与保存授权仍由后续独立流程决定。

FINAL FROZEN + STOP。

## Reviewer Verdict: F16-Seg-1 = PASS
