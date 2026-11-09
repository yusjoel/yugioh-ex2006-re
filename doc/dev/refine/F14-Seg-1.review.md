# Refine Review: F14-Seg-1（二轮）

## 复核输入

- 段范围：`asm/14_equip_ai_scoring.s [0x080a78dc,0x080a8c30)`，长度`0x1354 = 4948` bytes。
- proposal：`doc/dev/refine/F14-Seg-1.proposal.md`，SHA256 `3dbf8f8761d96475b7926453187077271fb84f801d85bfe2f62152cbb5ca98c4`。
- slots：`doc/dev/refine/F14-Seg-1.slots.tsv`，SHA256 `30f286050966b3c97edfd2e3d2df0fbe3279a5cef8b363b29e1dda93d9e98693`。
- plates：`doc/dev/refine/F14-Seg-1.plates.tsv`，SHA256 `7b12e7ae523ca9892f08ec23fbfc019f5672b199cfd15eafbfc740fb054325d3`，与首轮逐字节相等。
- freeze manifest：`output/refine-run-20261028-105948/f14-seg1-freeze-manifest.json`，SHA256 `22e9c676efe950c1ecbc31d4c189950160464035d8c6f86635ff72faf769bf56`；17个输入逐项重新计算SHA256，0项漂移。活动review不在hash输入中。
- Mode A machine contract：`output/refine-run-20261028-105948/f14-seg1-mode-a-machine-contract.json`，SHA256 `ec45253613c2ed2f2ee524c40e5947bb3f515c8e49790a1dfe84d59708ed3057`。
- reviewer二轮独立审计：`output/refine-run-20261028-105948/f14-seg1-review-round2-audit.json`，SHA256 `037207f3345b2e0cbbf95eee51d8ac1c5176c03ed26d1ab002bc2ec6c077fe9a`。

首轮正式review SHA256 `3d0ce2dd37e9f4f6946983cda521e2deab53961644256d6f4e7e9be01eb5d3ae`及其20项输入/证据完整保存在`output/refine-run-20261028-105948/f14-seg1-review-round1/`；独立重算20个归档文件hash均与`root-f14-seg1-round1-archive.json`相等。二轮未启动headless，未写proposal、TSV、正式源码、Ghidra工程、进度文档或脚本，未运行build、stage或commit。

## 三项修订独立复核

### #1 `0x080a8234`引用守恒

独立比较首轮与当前167行slots，只有`0x080a8234`的`action`及`id_contract`两字段变化，其余166行及该行其他字段相等。当前动作是`REF_PRESERVE`；前态仍有且只有一条`080a8234 -> 080a8238`、operand 0、DATA、DEFAULT、primary引用，source仍是4-byte Data。合同明确禁止duplicate add和source reference升级，仅允许动态DEFAULT table-base target物化USER primary时派生的`target_primary_id/name`改变。

重新按当前TSV统计为：`REF_ADD=64`、`REF_PRESERVE=13`，总REF=77；其余动作仍为`61 EQ_ADD + 2 EQ_PRESERVE + 1 RENAME + 25 TABLE_ENTRY_MATERIALIZE + 1 DISASM_WORD_TO_CODE`。proposal:132,171与slots完全一致，首轮#1关闭。

### #2 B3来源范围口径

直接从ROM读取表`[0x080a85fc,0x080a862c)`的12个word并与完整ROM raw扫描复核：

- 5个sources分别命中`[0x080a862c,0x080a87e0)`内5个unique targets；
- 另7个sources重复命中既有范围外tail `0x080a87e0`；
- 全表共12个sources、6个unique targets。

proposal:50现完整区分“全表来源”“R4半开区间内命中”和“范围外既有tail”，未改原始refscan逐项命中数据，首轮#2关闭。

### #3 全表17个unique targets

不采用machine contract的汇总值，直接从当前25个`TABLE_ENTRY_MATERIALIZE`行的ROM原值与既有DATA refs重新派生：25个source entries对应17个unique target地址，其中16个是新R4代码入口，1个是既有tail `0x080a87e0`。25行ROM值全部匹配，每行source reference CORE6均为冻结的`DATA/DEFAULT/op0/primary`，无错误。

machine contract逐行列出的25个source/target/label与上述独立派生完全相等，并列出17个唯一target、每址一个USER Global primary、0个同址alias。proposal:121,281及manifest的后态数量均为17，首轮#3关闭。

## 未改合同连续性

- 首轮proposal到当前proposal仅5行删除、5行加入，均对应三项修订；无其他文本变化。plates、R4 map、refscan、card-routing、plate-plan和Function body合同hash连续。
- 独立首轮ROM核验继续适用：三块1168B=`482 instructions/1006B + 36 pools/144B + 9 pads/18B`，54 direct flows、21 calls、39 PC reads；三条扩展Function body ranges及SHA256未变。
- 167槽仍精确覆盖131个当前word与36个新池，63个EQ等于ROM；final labels合法且唯一；6个新数值常量无可复用冲突；4个新和3个改名Thumb aliases保持偶地址Function`+1`，odd target不增label/Data/ref。
- 10个FUNC_RENAME、13条写入PLATE、1条保留PLATE及外部`4058` caller闭包均未变。13条写入PLATE全部ASCII、最长449字符；卡ID路由、真实caller/body/返回语义与四类结构化卡证据沿用首轮独立核验。
- 15个物理DB文件当前hash全部等于pre-F14前态。Mode A时冻结的88文件中，86个当前仍精确相等；其余两项是root在窄修门禁完成后授权更新的`refine-progress.md`与活动文档“第二轮review中”状态，只属于进度元数据，不进入本段语义delta，亦未回退。

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|---|---|---|
| C1 | Rule 1：范围与路线图 | ✅ | 活动文档§五仍精确指定Seg-1 `[0x080a78dc,0x080a8c30)`，地址序正确。 |
| C2 | Rule 2：每个裸块有归宿 | ✅ | 三块1168B全部进入R4的18 code ranges、36 pools、9 pads；`7928` word转code，无静默保留。 |
| C3 | Rule 3：§5.1块确为0引用 | ✅ | Section 5.1=0；首轮独立全ROM raw/Thumb扫描连续有效，三块均有真实jump-table入口，资产偶合已按原字节位置保留证据。 |
| C4 | R1：EQ值等于ROM | ✅ | 63个EQ逐项与ROM一致，callback odd words严格等于对应偶地址Function`+1`。 |
| C5 | R1：常量复用 | ✅ | 6个新数值常量、4个新aliases和3个改名aliases的复用审计未变，无同名或同值冲突。 |
| C6 | R2：槽名合法且唯一 | ✅ | 167行final labels合法；source labels及17个case target labels唯一，无同址多alias计划。 |
| C7 | R3：label/ref接通及前态守恒 | ✅ | `8234`现为REF_PRESERVE，source Data与CORE6冻结，计数64 ADD+13 PRESERVE；25个table source refs与17个target label计划完整。 |
| C8 | R5：现名与PLATE引用 | ✅ | 10个final Function names、13条写入PLATE及外部`4058`闭包均使用现名，无自动名残留。 |
| C9 | ASCII | ✅ | 全部新EOL和13条写入PLATE为ASCII；保留PLATE亦为ASCII。 |
| C10 | carve与Thumb `+1` | ✅ | carve=0；全部新旧callback词保持`Function+1`原值，未创建odd地址label/Data/ref。 |
| C11 | 函数误名 | ✅ | 10个旧泛化名均列入FUNC_RENAME；其余3个段内Function名与body/caller一致。 |
| C12 | R6：消费者与计数证据 | ✅ | B3现明确12源=`5内块+7外tail`；关键语义均有file:line和high confidence，无禁用措辞。 |
| C13 | 残留、布局与最终门禁 | ✅ | 167槽、482指令、36 pools、9 pads、25 refs完整；全表17 targets=`16新R4+1既有tail`已进入proposal、manifest及机器后态合同。 |

## 状态: PASS

## 修改清单

无。

## Reviewer Verdict: F14-Seg-1 = PASS
