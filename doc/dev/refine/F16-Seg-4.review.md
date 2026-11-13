# Refine Review: F16-Seg-4 — Round 3

## 状态: PASS

Mode A v3 已闭合最后一项 I2-R。此结论针对完整 proposal 与分析模型，允许进入后续受审实施准备；不是实际 Ghidra POST、完整回滚、保存或 ROM 构建验收，也不签发保存授权。

冻结绑定：manifest-v3 `09dda96f7b00f5d0117d4ecc32543b73e26c25b0136afffd302a49f53146cea5`；source-v3 `31d3493e031410a7af1a2ae1a2a9dc319d88fda5edf23e599c7de2f7e90cd0fd`；inputs-v4 `3ff67b50c6dc6785f2e337ab12432d4a287f42e78bfbe30d7d045d5043509b83`。

原完整审核与两轮缺陷证据封存在 RUN 的 `f16-seg4-review-round1.md` / `f16-seg4-review-round2.md`。本轮继承其中不变的语义和 C1-C13 核验，仅重放 I2-R 影响入口。24 语义产物共181453167B、producer/proposal/validator 原文、三份正式 proposal/TSV、原22输入均保持原字节；新增4个动态身份权威输入。

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|---|---|---|
| C1 | Rule1 地址顺序 | ✅ | 当前唯一下一段 `[080c4350,080c57c4)`，没有跳段或回头。 |
| C2 | Rule2 全数据块归宿 | ✅ | 四块2128B互斥完整覆盖：25 code spans/884 heads/1838B，64 undefined4/256B，17 zero-align/34B。 |
| C3 | Rule3 全 ROM 引用 | ✅ | 本人 Round1 非对齐全ROM1064候选逐位置复扫保持有效；raw/THUMB命中4/0、13/2、24/1、18/0。§5.1=0，没有把正引用块登记为零引用。 |
| C4 | R1 值 | ✅ | 本人直接原ROM核对203 word、其中27 EQ的结论保持；本轮全部24产物再次逐字节复放一致。 |
| C5 | R1 复用 | ✅ | 0x215/0x21e/0x868复用，6新EQ与4RAM全局的域和名字通过原独立检索。 |
| C6 | R2 名/碰撞 | ✅ | 193 USER唯一、3 rename；槽/表/代码小写命名、RAM全局约定及全asm/constants无冲突结论保持。 |
| C7 | R3 USER/DATA接通 | ✅ | 80 DATA add、13 preserve、83 even vectors、185 auto与193 USER闭合；21target/4876primary及同类固定集合唯一全集守卫保持通过。 |
| C8 | R5 现名 | ✅ | 8本段PLATE加6b04上下文PLATE均使用最终现名，无旧自动数据名。 |
| C9 | ASCII | ✅ | 9 PLATE、2 instruction EOL、120 slot EOL原ASCII文本不变。 |
| C10 | even/THUMB | ✅ | computed-PC表保even地址与既有DATA/DEFAULT引用，不加+1；无独立函数指针carve。 |
| C11 | 函数误名 | ✅ | 单卡渲染状态机、手牌计数阈值分类、配对请求初始化三改名与完整消费者一致。 |
| C12 | R6 消费者/置信度 | ✅ | caller flag0/1、packed字段、28/44-byte清零、chain mask、OAM attr2、共享saved-frame等原独立证据保持。 |
| C13 | 残留 | ✅ | 61自动名及四raw全部有归宿，无静默ROM_INCBIN/.byte。 |

R1-R9 的 proposal 静态质量检查通过。R4 采用原生 detached decode/factory，精确 DisassembleCommand restricted set、884个start head、followFlow=false及enableCodeAnalysis(false)；只扩parent4350 body56→1894B、局部CALL_RETURN437a/4424，不并4ca0 shared body、不新建/删除/合并Function。其它140完整Function、4876fullstates、22359指令属性、43716module units、48external、2618Tiny、508真实NULL even_function均保完整投影。实际执行效果仍由实施阶段独立验证。

## I1/I2 修复闭合

### I1：固定地址行全集与唯一性 — 已关闭

Round2 已实际证明21target、4876primary与20类同型固定集合守卫拒绝缺失/重复/类型/schema坏例。`validator_source` 本轮完全原字节，公共完整validate再次通过；31项I1与旧12项不变矩阵按封存证据继承，没有重跑。

### I2/I2-R：完整原生 BEFORE ID 排他 — 已关闭

- 本轮 AST 对比证明原 `_seg4_static_before_ids` 不变，`verify_actual_native` 除 `old_ids` 赋值RHS调用新权威外全部语法不变。严格正int64、非bool/float、193新ID互异、完整DTO比较和POST只绑定193新USER ID的边界没有放宽。
- 新权威来自真实 `SymbolTable.getAllSymbols(true)` 的35732静态+48116动态=83848完整既有身份。已读Java getter：迭代至结束，按 `isDynamic()` 分组；每个动态项以公开 `getDynamicSymbolID(Address)` 核对真实ID，重复/组间碰撞即拒绝，没有手算ID公式。
- 接收器严格校验新增4输入的固定path/size/SHA与唯一membership、文档/行schema、strict list、正int64/顺序/唯一、namespace类型、dynamic=true、枚举完成/公开getter标志、精确计数。完整静态ID序列与上一原生静态witness逐项一致，静态/动态互斥，union83848；已观测完整symbol DTO的既有ID均在该集合。
- dynamic gate与static gate完整同值，并与正确DB15 backup逐路径hash相同；custody records精确唯一绑定。原22输入、73个递归记录、当前source207+snapshot207、DB15+backup15均实际size/SHA通过。
- 实际完整 `_seg4_all_before_ids` 返回83848，含2991、23352的虚拟ID4611686018461086546及core之外00000043的真实虚拟ID4611686018427387971。193个私有互异新ID的whole canonical、full properties header/rows与Tiny正例PASS。
- 冻结 `run_negatives` 的21个完整native入口反例由本reviewer独立实际执行，全部拒绝：静态2991别名、原23352一致全图别名、另一个不在canonical/module的全局动态别名、旧offcut自身ID破坏，以及17项新authority decoded-boundary反例。17个hook均精确命中一次且计数字段为strict int；原始字节/hash与validator源码未改，finally恢复JSON代理。

## 本轮实际复放与范围

独立公共只读入口执行一遍producer+proposal、完整validate(custody=True)、新全ID权威入口及21项受影响native反例。24产物181453167B全部与冻结文件逐字节相同。未调用会覆写冻结报告的runner；既有fixer两遍生产结果只作封存记录，不代替独立复放。

原生静态/动态witness均为BEFORE getter证据；正常193 ID是私有观测夹具，未生成真正POST/proof/grant。源scope保持asm01两处BL和asm16本段/6b04，200native/3fallback、129→132pins、GNU10、registry9/CSV3、temp parent length56→1894合同保持。

## 修改清单

无。进入实施准备后，仍须独立审Script与控制链，再实际prestate/dry/owned rollback、唯一保存、fresh saved观察、源码范围和完整ROM逐字节验证；本报告不提前认定这些步骤通过。

## 独立证据

RUN=`output/refine-run-20261028-105948`：

- `f16-seg4-reviewer-R3-replay-v1.json`：实际公共入口、完整83848权威、21反例与私有正例，SHA `cef90584e3be65e831960060003190c8eba5b3c815e6eedfb867ab5e682e05fd`。
- `f16-seg4-reviewer-R3-custody-delta-v1.json`：73真实记录、old22/新4输入、AST/源码差分、source/DB双份、getter原文，SHA `ce605e203036423850ca8e9f7e3a509869d4e4687232fe7c932f6a76c573c16f`。
- `f16-seg4-reviewer-audit-v3.json`：最终绑定；`f16-seg4-review-round3.md`为本报告精确副本。

FINAL FROZEN STOP。没有Ghidra写入、实际POST/回滚/保存、源码流水线、构建或Git操作。

## Reviewer Verdict: F16-Seg-4 = PASS
