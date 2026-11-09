# Refine Review: F14-Seg-2（二轮）

## 复核输入

- 段范围：`asm/14_equip_ai_scoring.s [0x080a8c30,0x080aa120)`，长度`0x14f0 = 5360` bytes。
- proposal：`doc/dev/refine/F14-Seg-2.proposal.md`，SHA256 `de2dee2f06c1daa5fa2f558aa6d6e9fa19a05a1ff567590eb4c7fc5704c5b809`。
- slots：`doc/dev/refine/F14-Seg-2.slots.tsv`，SHA256 `32c3f4b9fb7ffeac283bd281859fc9bfc70c5eb5fa4aeb1a5b35ae53c91a5a71`，与首轮逐字节相等。
- plates：`doc/dev/refine/F14-Seg-2.plates.tsv`，SHA256 `239b1abec33838950e7d089e8fb89038bce57c0e796379aab6b7835762644325`。
- R4 map：`output/refine-run-20261028-105948/f14-seg2-r4-cfg-map.json`，SHA256 `8d30c1f7bc2ac86184317407a1da7b2591ea1ee9c09056d37a9b0e3f0d6fe98b`，与首轮逐字节相等。
- function plan：`output/refine-run-20261028-105948/f14-seg2-function-plan.json`，SHA256 `56bad146a04fbea3964720236d948010ed133fa63cde03f6f0add0dcb936cd64`。
- Mode A machine contract：`output/refine-run-20261028-105948/f14-seg2-mode-a-machine-contract.json`，SHA256 `e9d077cd245e2b23f7fed2793cd46b5aefcb0258c9de95d80aa73075d9fd1bcc`。
- freeze manifest：`output/refine-run-20261028-105948/f14-seg2-freeze-manifest.json`，SHA256 `9fd76592edb220c3f0c98bb03a45a4dff30293a36ed110fdb5fda236dec5f63c`；20个当前输入及2个review-basis引用逐项重新计算SHA256，0项漂移。
- Mode A checklist：`output/refine-run-20261028-105948/f14-seg2-mode-a-checklist-gate.json`，SHA256 `762b427f4980186489a72c8d0f76aaad3b785415146fbe4f80a1f867f3b110b5`。
- reviewer二轮独立审计：`output/refine-run-20261028-105948/f14-seg2-review-round2-audit.json`，SHA256 `b967598f78237a2826b257b86c91dacf5d99ca921a2da39c0fc305edbde2ed35`。

首轮正式review SHA256 `e2f03a83701232ebcd5288711e1526506a1d80855445692c7449452b3e396d95`及其21项输入/证据完整保存在`output/refine-run-20261028-105948/f14-seg2-review-round1/`；独立重算21个归档文件的size与SHA256，全部匹配`root-f14-seg2-round1-archive.json`。活动review未进入manifest hash环。

P0通过：当前proposal、slots、plates均非空，未出现中止标记。二轮未启动headless，未写proposal、TSV、正式源码、Ghidra工程、进度文档或脚本，未运行build、stage或commit。

## 五项修订独立复核

### #1 raw3 table sources / unique targets

直接从原ROM重读`9770..9798`的10个word，独立得到6个unique targets：`9798/9800/9b40/9ba4/9bac/9c2c`，其中`9ba4`由5个sources复用。与`9268..9278`的5源/5目标合计为15 sources/11 unique targets。`9134`只由`9ba6` direct BL抵达，不属于table targets。

proposal:42、proposal:48、machine contract和manifest现均使用10/6及总15/11口径，首轮#1关闭。

### #2 raw1本块扫描与跨块CFG闭包

二轮重新对三个raw块的每个偶地址扫描完整ROM。raw1 `[9132,9264)`有153个候选，仅`920e`在`09ee7069`出现一处资产raw偶合，真实raw/THUMB pointer命中为0；其live入口是`9ba6 -> 9134` BL。raw2的5个table sources位于`9268..9278`，目标全部在raw2。

按未改R4 map重新逐地址统计：raw1=`128 instructions/256B + 12 pools/48B + 1 pad/2B`；raw2=`528 instructions/1070B + 32 pools/128B + 5 pads/10B`；跨raw1+raw2的新Function cluster才是`656 instructions/1326B + 44 pools/176B + 6 pads/12B`。proposal:40-41已完整分离三个口径，首轮#2关闭。

### #3 `aa10c` Function entry与`aa10e` interior引用

独立从原ROM/R4 map派生新增边，并重读前态地址状态：

- Function entry `aa10c`最终2条incoming：既有`975a -> aa10c` CALL与新增`9bd6 -> aa10c` JUMP；两者精确target primary为USER Function ID 16954。
- Function interior `aa10e`最终5条incoming：`9b98/9baa/9c1c/9c36/aa106 -> aa10e` JUMP。其前态`primary_symbol=null`、`function_at=null`、`refs_to=[]`，但`function_containing=exit_equip_phase_oob_epilogue_wide`且InstructionDB已存在。
- 当前合同要求disasm派生单一DEFAULT code Label，后态从`getPrimarySymbol(aa10e)`读取动态ID/name，type/source必须是`Label/DEFAULT`且ID不得等于16954；原bytes、InstructionDB、owner、refs_from和EOL保持。Function body external incoming独立计数为7。

plates TSV的`aa10c final_incoming_json`现只收录两条entry refs；function-plan、proposal:96,107,183,242及machine contract另有五条interior地址级合同。首轮#3关闭。

### #4 `9134`返回0/1的PLATE语义

独立重读ROM指令：`94ba`是`movs r0,#0`，`94bc`跳到`9722`，形成返回0路径；`9228/92cc`跳到`9720`，`9720`执行`movs r0,#1`，形成返回1路径。

当前`9134` PLATE逐址记录两类路径，实际长度与声明均为471 chars，纯ASCII且不超过500。plates TSV、function-plan及proposal:174使用同一文本/语义，首轮#4关闭。

### #5 canonical Function inventories

独立读取当前正式输出与导出脚本：`temp/ghidra-functions.csv`前态为5213 Function、5123 named、90 auto；`tools/ghidra-labeling/ExportFunctionInventory.py:7-10,62,69-72`将四份正式输出固定在`temp/`。当前proposal、function-plan及machine contract只列：

- `temp/ghidra-functions.csv`
- `temp/ghidra-functions-renamed.txt`
- `temp/ghidra-functions-auto.txt`
- `temp/ghidra-functions-summary.md`

后态合同为新`9134/process_equip_mode1_phase_3_to_7/1326B`、既有`9734/dispatch_equip_mode1_phase_by_combined_index/2210B`，总数5214/5124/90；正式naming CSV仅1个既有name cell变化并新增1行。proposal:194,246已禁止另一路inventory替代，首轮#5关闭。

## 未改合同连续性

- slots、R4 map、full-ROM refscan、card evidence、slot-value plan及source-format prediction与首轮逐字节相等；首轮独立机械证据hash连续。
- 二轮full-ROM扫描仍为1967 candidates、14个非零candidate地址；三项资产偶合位置/原字节不变，Section 5.1仍为0。
- R4仍为1699 InstructionDB/3484B、102 pools/408B、21 pads/42B、248 direct flows、43 BL、126 PC reads、1616 API fallthroughs；12 seed闭包覆盖全部1699条指令。
- 156槽仍精确覆盖54个当前word与102个新pool；动作仍为31 EQ_ADD、73 EQ_MATERIALIZE、36 REF_ADD、1 REF_PRESERVE、15 TABLE_ENTRY_MATERIALIZE。所有ROM值、前态Data/ref/equate/EOL及标签唯一性连续有效。
- carve `[09e478c8,09e478ce)`、三卡结构化身份、7个Function body ranges/SHA、1 rename+1 new Function及其余5条PLATE语义未改。6条写入PLATE全部ASCII，当前最长471。
- 15个物理DB文件当前hash全部等于Seg-2前态。源基线93项中91项当前精确相等；另两项是root在Mode A门禁后授权推进的`refine-progress.md`与活动文档“第二轮review中”状态，不属于Seg-2语义delta。

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|---|---|---|
| C1 | Rule 1：范围与路线图 | ✅ | 活动文档§五Seg-2仍精确为`[080a8c30,080aa120)`，紧接已完成Seg-1。 |
| C2 | Rule 2：每个裸块有归宿 | ✅ | 三块3934B全部进入R4；当前逐块计数为raw1 128/12/1、raw2 528/32/5、raw3 1043/58/15，跨块656/44/6口径已单列。 |
| C3 | Rule 3：§5.1块确为0引用 | ✅ | 二轮独立重扫1967个偶地址候选；三块均有live CFG，额外三项命中均是有具体文件/offset/原字节的资产偶合，Section 5.1=0。 |
| C4 | R1：EQ值等于ROM | ✅ | 未改104个EQ、15个table words及102个pool bytes继续逐项等于原ROM。 |
| C5 | R1：常量复用 | ✅ | 68个现有equate names与13个新增定义的复用审计未变；无新增常量delta。 |
| C6 | R2：槽名合法且唯一 | ✅ | 156槽及target/global labels合法；跨地址重名0，重复table rows仅共享同一target。 |
| C7 | R3：label/ref接通及前态守恒 | ✅ | word REF/carve合同未变；`aa10c` entry2与`aa10e` interior5现分离，后者要求动态DEFAULT Label且不借用Function ID 16954。 |
| C8 | R5：现名与PLATE引用 | ✅ | 所有PLATE使用现名且无自动名；`9134`现同时记录真实return0和return1路径。 |
| C9 | ASCII | ✅ | slots/plates TSV无非ASCII；6条写入PLATE最长471，均不超过500。 |
| C10 | carve与Thumb `+1` | ✅ | carve是3个u16 CID；`09e478c9`全ROM命中0，无odd label/Data/ref计划，switch targets保持偶地址。 |
| C11 | 函数误名 | ✅ | `9734` rename与真实combined-index body/caller一致；`9134`新Function名与阶段3..7表及caller一致。 |
| C12 | R6：消费者与计数证据 | ✅ | raw1/raw2/raw3、15/11 table、entry2/interior5、return0/1均有独立ROM/map/前态证据及明确后态门禁。 |
| C13 | 残留、布局与最终门禁 | ✅ | 54旧word、102 pools、11 unique table targets及自动名覆盖完整；四份inventory现只指向canonical `temp/`，并冻结5214/5124/90及两条关键row。 |

## 状态: PASS

## 修改清单

无。

## Reviewer Verdict: F14-Seg-2 = PASS
