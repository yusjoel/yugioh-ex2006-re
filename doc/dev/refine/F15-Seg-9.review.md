# Refine Review: F15-Seg-9

## 状态: PASS（第三轮最终窄复审）

唯一冻结 manifest SHA256 `3fadc43df3ab93a30b7cc9cb43df609f1d3807bd4bd3a0f0305c00d58f56c4e3`；proposal `a27871eb2ea4dbdb2d0cd2e104f319b92a081fd31e16bf908b3448cab02dabd2`，slots `0bc908dcff13251505bb86930d2357e30c780560b1f149cfae0777d11ab1e2b2`，plates `45a51c8b317ecdd03ed7f9a02500f021585ff2c6c7ef28f90e2df8cb41ca6733`。canonical仍为 `79c57dad1cd67e82143762ff78064b7b85b075b5242685d6b2c87521ab2d0aac`。

本轮只复核第二轮四项、全部副本/摘要及必要回归，继承已完成的完整C1-C13调查。首/二轮review、audit和所有ignored证据均保持原字节；未更改方案、生产源、DB、进度或任何实施输入，未启动headless/Ghidra、Computer Use、build、stage或commit。

## 核验 (C1-C13)

| # | 结果 | 结论/继承证据 |
|---|---|---|
| C1 | ✅ | 下一段 `[080bede4,080c00f0)`、4876B，严格地址序。 |
| C2 | ✅ | 已独立证实3854B指令+960B word+62B padding，1849指令/240word/31pad/raw0；布局与源码本轮不变。 |
| C3 | ✅ | 已独立重跑raw/odd全ROM扫描，六入口even/odd均0；冻结refscan本轮逐字节不变，无§5.1。 |
| C4 | ✅ | 240槽ROM/45EQ值正确；全局2461对象/12596绑定与完整canonical派生通过；本轮无改。 |
| C5 | ✅ | 15新GNU定义与复用域已核；中性LP_DELTA_PREFIX_TILE_MODE0仅BF390 operand0，值0x202；本轮无改。 |
| C6 | ✅ | 181源名唯一且符合正则；59switch既有namespace/static ID保留；本轮无改。 |
| C7 | ✅ | 198图、104新增入站/49目标、五重合after，10079 states/416 Fn独立推导通过；91旧DATA不升级。当前fullstate/slot/target原字节不变，Function只四PLATE叶改变。 |
| C8 | ✅ | 六函数名/所有现名引用闭合；12现存registry tuple按名/地址实查，BEDE4缺席保持；三现存tuple只改必要注释副本。 |
| C9 | ✅ | 13个PLATE写入全部ASCII<=500；四候选417/463/499/316字逐字相同，其他九条不变。 |
| C10 | ✅ | 81GAS=61继承+20fallback，native实际246次执行/零段外新增.word闭包已核；本轮GAS/scope路径及机器字段无改。 |
| C11 | ✅ | BF228最终play_zone_info_palette_cycle_effect与真实attr2消费一致；其余五拟名已核，本轮名称/ABI/prototype/引用无改。 |
| C12 | ✅ | 第二轮四项均由精确ASCII候选闭合，见下表；无新事实矛盾。 |
| C13 | ✅ | 240槽覆盖保持；producer/validator及transitive immutable base显式SHA绑定。实跑43928/0+104负例；实际producer由归档v2输入在内存复现15输出byteexact。 |

R1-R9细化清单已闭合；本结论仅为分析质量PASS。R9后续实施备份、真实事务回滚、保存门禁、native导出和ROM逐字节验证属于独立落地阶段，本轮未执行或授权。

## 四项修正闭合

| 第二轮项 | 当前精确事实 | 副本与语义依据 |
|---|---|---|
| R1 BEDE4 | real N与cached C分开；仅u32(N-C)<=7且N>7时store C-1，不写real N | 417字候选；`asm/15_equip_target_summon_zoom.s:21065-21094`；N10/C8写7而非9。 |
| R2 BF394 | progress字段位于banner+0x18，增加所选十进制step并clip；不存在固定+18 | 463字候选；`asm/15_equip_target_summon_zoom.s:21835-21964`；mode1 LP+progress、mode0 max(LP-progress,0)。 |
| R3 BF7F8 | phase0 ptnsect初始化/strings另走line buffer；phase2 nonzero tick latches active，latch0才每ctx写两结果OAM，all-zero-tick才增加hold | 499字候选；`asm/15_equip_target_summon_zoom.s:22353-22424,22425-22853,22914-23078`；保留后续fade/restore/default返回区别。 |
| R4 BFF34 | 从a&0x0f0f开始OR；lower adjusted nibble carry可设置bits11:8，不称其原值不变 | 316字候选；`asm/15_equip_target_summon_zoom.s:23272-23296`；0x00f0+1→0x1100等真实ROM例子保持。 |

四条均逐字采用第二轮review给出的候选，逐条字符数、ASCII与全文SHA对齐。13正式TSV中仅这四行的new_plate/new_plate_chars变化，所有BEFORE列及其余九行原字节不变。五个派生计划仅允许的四条PLATE/字符数/semantic evidence叶变化：Function（包括内嵌416观察）、full-Function、semantic、registry、source-scope内嵌registry。其他九个计划、240槽TSV、全10079state图、全Equate/GAS/refscan/rename/source路径完全不变。

## 独立来源执行与最终保管链

- 自主窄差异检查906项全部PASS，严格构造只允许四PLATE叶的预期对象并与完整前/后对象比较，未用fixer的delta自述代替。
- 实跑真实v3 validator wrapper及其immutable v2 base，43,928项/0失败，104逐边删除负例；捕获SystemExit后正确生成v3结果，结果与冻结validation逐字节相同。仅在本进程重定向唯一结果路径的读写到reviewer文件，未覆盖冻结输出。
- 实跑真实v3 producer generate AST与SHA锁定的v2 base，以归档v2为输入，使用内存存储overlay/实际Windows序列化规则；15个输出全部逐字节一致，含proposal/两个TSV/12个JSON。未运行实际--freeze或写任何producer输出。
- 30个冻结manifest声明、source181 current+copies、正确SavedSeg8 DB15 current+backup均精确；v1/v2独立证据未变。ROM SHA1仍为 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`。本轮不重开已通过且byteexact的全段调查。

ignored审计总表：`output/refine-run-20261028-105948/f15-seg9-reviewer-independent-v3.json`；其列全部新证据path/size/SHA和继承证据绑定。

## 修改清单

无。允许Root继续独立实施审核；本PASS不等于headless、生产写入或持久保存许可。

FINAL FROZEN + STOP。

## Reviewer Verdict: F15-Seg-9 = PASS
