# Refine Review: F13-Seg-5（第二轮）

审查范围固定为 `[0x080a1658,0x080a27a0)`，模块为 `asm/13_equip_placement.s`。本轮重新读取
Mode A 修订后的 proposal/TSV，并独立复核首轮八项修改；未进入 Seg-6 语义，未修改 Ghidra、
proposal、TSV、正式源码或常量，未执行 build/commit。

## P0 与输入固化

- proposal SHA256：`4f24859a66f2b7580c7599312488a961a55b6270f1d8aa0c3eb4b8612b3b9028`。
- TSV SHA256：`785063ff6264fcd036b96df641c397f031f9da0c42540df8702ddfd54b5ed1df`。
- proposal 非空，无中止标记或零容忍词；TSV 为179行，即1行表头加178行数据。
- 活动路线图确认 Seg-1至Seg-4已完成，下一段正是 Seg-5
  `[0x080a1658,0x080a27a0)`；边界、地址序和模块均一致。

## 独立数据块与 ref-scan 复核

当前段内原始来源确为五块：`1720..190a` ROM_INCBIN、`1950..1954` `.byte`、
`1dd8..1de8` `.byte`、`1f54..2000` ROM_INCBIN、`2018..2234` ROM_INCBIN。对每块内每个
2-byte 对齐候选地址重新搜索全 ROM little-endian raw 与 `address|1`；`1f54..2000`按最终归宿
拆成 Rule3 与 R4 两个子范围。结果为：

| range | raw / THUMB\|1 | 独立归因 | 结论 |
|---|---:|---|---|
| `080a1720..080a190a` | `29 / 2` | 19个真实even switch words；10 raw与2 thumb数据偶合 | R4 |
| `080a1950..080a1954` | `0 / 0` | `080a18fa: 0x4a15`的PC-relative LDR解析到`1950` | 4-byte dataization |
| `080a1dd8..080a1de8` | `0 / 0` | Ghidra refs=0；无branch/literal/word/fall-through | Rule3 / §5.1 |
| `080a1f54..080a1f68` | `0 / 0` | Ghidra refs=0；`1f52`属前Function且返回；`1f68`无fall-through | Rule3 / §5.1 |
| `080a1f68..080a2000` | `1 / 0` | packed命中仅`1fee -> 0814729f`数据偶合；另有真实BL `1732 -> 1f68` | R4 + Function create |
| `080a2018..080a2234` | `6 / 6` | 5个真实even switch words；1 raw与6 thumb数据偶合 | R4 |

首块漏项已闭合：`0x080a1900` raw 在ROM host `0x09e13b4f`命中，字节为
`00 19 0a 08`，属于 `asm/rom.s:783` 的raw host
`[0x09dff9e4,0x09e246d4)`；修订稿已将总数改为`29/2`并列出该项。19项row-type表的原值
依次为`1720,1720,1740,1764,1788,17ac,17c8,17d8,17fc,1820,183c,1858,1874,1884,
18a8,18cc,18e8,18ee,18f4`。五项phase表为`2018,203a,20a0,2140,217c`；六项既有
card-type表为`2608,2644,2652,26e8,272c,2770`。三表共30个word均保持even。

两个Rule3范围另经fresh PyGhidra只读查询，目的地址引用均为0；该次查询前后 `.rep` 的15个
数据库文件SHA256变化数为0。局部分支、literal、结构化word和前后Function归属均与Rule3结论
一致，没有有效入口进入这两个范围。

## R4、literal pool 与 Function body

依据ROM机器码独立重建并逐range调用Thumb objdump：

- `1720..190a`分成18个唯一code islands；row types 1和2共享`1720`，其余17个入口对应
  row types 3..19。前17个独立岛末尾均跳到`190a`，最后一路自然进入该共享尾。
- `1f68..2004`的pre-switch代码为`[1f68,1fba) [1fc4,1ff8)`；其余部分为proposal列明的
  padding/pool/table pointer。
- `2018..2234`分成11个code ranges，五个switch入口及内部branch均落入这些range，最后的
  `[21e8,2226)`包含共享返回尾`[2214,2226)`。
- 三个R4范围的code与pool/padding集合逐字节无空洞、无重叠；全部31个code range均从指定首
  地址正常解码，无undefined指令。
- R4代码共有71个PC-relative LDR及71个唯一literal target；去掉既有`080a194c`后，余下70个
  target与TSV的70个`new_pool`逐地址完全相等。

Function合同逐项成立：

1. 当前`080a1658`实测Function ID为16936，前态body恰为
   `[1658,166c) [1674,169e) [16b4,16cc) [190a,194a)`，唯一incoming reference为
   `08094d30 -> 080a1658`、operand 0、`UNCONDITIONAL_CALL/DEFAULT/primary`。修订稿的后态body
   加入18个case入口，排除全部pool/padding，并将相邻的`18e8..194a`规范化合并；入口和ID保持。
2. `080a1f68`由`080a1732`真实BL进入，入口为`b5f0`。后态body明确为2个pre-switch range加
   11个phase range；只在此地址createFunction，不给case另建Function。
3. `080a24cc`由`080a25a8 = 0x080a24cd`作为Thumb callback引用。机器码body精确为
   `[24cc,24e4) [24ec,24f0)`，两个pool words `24e4/24e8`排除，`24ee`为`bx lr`。

当前inventory为5209个Function；段内38个既有Function均以Thumb push开头。只新建上述两个
Function，故后态`5209 -> 5211`成立。新Function ID在事务receipt记录并由fresh只读进程复核，
没有凭空预设ID。

## TSV、ROM值与常量

- 178行分布为原槽108、R4/dataization新增池70；原槽类别精确为
  `DAT=52 / DWORD=36 / PTR=20`。两个裸块头`DAT_080a1720`、`DAT_080a2018`另计。
- 动作精确为`EQ=127 / REF=26 / RENAME=25`；178个地址和178个`slot_label`均唯一，全部符合
  `^[a-z][a-z0-9_]+$`，未与当前asm/data label碰撞。
- 108个非`new_pool`行逐地址、逐`old_name`均能在当前asm找到；段内额外结构化表头
  `switchD_080a25de__switchdataD_080a25f0`由switch规范化计划单独覆盖，不属于108个自动4-byte槽。
- 178/178个`original_value`均等于ROM对应地址的4-byte little-endian值；因此127/127个EQ值
  全部通过。
- 116个REUSE EQ行涉及18个唯一符号，均在当前constants/rom.s存在同值定义。新增集合精确为
  两个offset、两个RAM global和四个Thumb GAS alias；新增名称及四个新增数值未与现有定义冲突。
- `FENGSHENG_MIRROR_CID=0x1509`和`TRAP_DUSTSHOOT_CID=0x1546`均由
  `data/card-stats.s`结构化slot记录及`constants/card_info.inc:1438/1456`复核；`0x12a1`由
  `asm/13_equip_placement.s:8519`的zone-query调用复核为`zone_query_hand_tag_12a1`。

## Symbol/reference source 与 switch 唯一Symbol

fresh PyGhidra只读前态验证了七个REF target：

| target | 实测primary/source | 实测Data |
|---|---|---|
| `0201c4e0` | `gP1LifePoints / USER_DEFINED` | `/undefined4`, 4 |
| `0201e2a0` | `gDuelCardCtxBase / USER_DEFINED` | `/undefined4`, 4 |
| `0201c600` | `gP1FieldArrayCBase / USER_DEFINED` | `/undefined4`, 4 |
| `0201b870` | `gSpriteAttrBuf / USER_DEFINED` | `/undefined2`, 2 |
| `0201e274` | `DAT_0201e274 / DEFAULT` | `/undefined4`, 4 |
| `0201e28a` | `DAT_0201e28a / DEFAULT` | `/undefined2`, 2 |
| `080a2004` | `PTR_DAT_080a2004 / DEFAULT` | undefined pointer, 4 |

proposal的七行target合同与这些实测值一致，并明确RAM仅创建/规范USER_DEFINED primary LABEL、
不创建或重打Data。26行REF post-state表与TSV逐行集合完全相等，全部规定operand 0
`DATA/USER_DEFINED/primary`。25行RENAME表与Ghidra逐槽实测完全一致：24行各有且仅有列明的
`DATA/{DEFAULT|USER_DEFINED}/primary`，`080a25ec`确为无reference；其后态要求原样保留tuple。

switch修订也已闭合：

- `080a16d4`当前primary为`PTR_DAT_080a16d4/DEFAULT`；修订稿复用该同一Symbol对象作为唯一
  `equip_row_type_switch_table`，首元素target使用`equip_row_type_case_1_or_2@080a1720`，其后
  17个唯一target按case 3..19命名。
- `080a2004`当前primary为`PTR_DAT_080a2004/DEFAULT`；修订稿复用同一Symbol对象作为唯一
  `equip_target_select_phase_switch_table`，首元素target为case 0。
- `080a25f0`当前primary为scoped `switchdataD_080a25f0/ANALYSIS`；修订稿移动/重命名同一对象为
  global USER_DEFINED `equip_activation_card_type_switch_table`。
- 三处均明令不建同址alias。TSV中`16d4`与`2004`的`slot_label`就是各自唯一表名，没有第二个
  首元素槽名。

四个唯一Thumb callback值为`080a1e81/080a24cd/080a24f1/080a2541`，均等于对应偶地址
Function `+1`。ROM中有五个odd pointer slots，因为`080a1e81`在`20ec`和`2134`出现两次；TSV
覆盖全部五槽，proposal的四个GAS alias覆盖四个唯一值。此计数与30个even computed-switch words
相互独立。

## PLATE、函数改名与证据

- proposal完整列出9条PLATE，ASCII byte长度依次为
  `271/431/282/308/280/392/200/367/375`，最大431；均无`FUN_/DAT_/DWORD_/PTR_DAT_`
  旧自动名。
- 五条既有stale PLATE `1968/1b1c/1e0c/24f0/2540`均已纳入全文替换，新增的
  `1658/1bc0/1f68/24cc`亦给出全文；PLATE总数精确为9。
- TSV的178条`eol_ascii`全部非空且纯ASCII。
- `080a1bc0`机器码确认入口`r1`保存到r5并在fallback成为callee r2；入口`r2`保存到r3，既是
  active-path delta也是fallback callee r3；入口r3未读取。修订PLATE与此一致。
- `080a1f68`的`1f78..1fa6`逐项掩码为`01/02/08/10/20/80`，修订PLATE已将r2写为packed flag
  bits，不再写成slot value。
- `080a1950`证据已改为当前源码`:7563`的raw block与ROM `080a18fa (0x4a15)` literal解析，
  file:line及地址均正确。

完整R4后的`080a1658`无APCS参数，读取`+1d88`active flag及`+1d90`row type并调度row types
1..19；原名`check_equip_target_slot_state`与函数体冲突。修订名
`tick_equip_display_row_by_type`符合函数行为和命名形式，`FUNC_RENAME=1`。

同步合同精确：当前`doc/dev/naming-proposals.csv`仅有`0x080a1658`旧名行，新地址
`080a1f68/080a24cc`均无历史行；`RenameKnownFunctions.py`也无三地址tuple。落地只更改既有CSV行的
name cell，不新增两个历史评分行；inventory从`total/named/auto = 5209/5119/90`变为
`5211/5121/90`。正式asm的精确旧callee只存在于`asm/12_equip_activation_scan.s:1604`及asm13
定义，修订稿已把这两处纳入导出scope合同。

## 首轮修改清单闭合

| 首轮项 | 结果 | 第二轮独立结论 |
|---|---|---|
| #1 ref-scan计数 | PASS | 独立复现`29/2`，补充host、字节、来源及守卫均完整 |
| #2 switch同址Symbol/case映射 | PASS | `16d4/2004/25f0`均为单一Symbol合同；`1720=case_1_or_2`，其后case 3..19 |
| #3 LABEL与reference source | PASS | 七target、26 REF、25 RENAME均完整，且与只读Ghidra/TSV实测相等 |
| #4 三个Function body | PASS | 1658 ID/前态、18/2/11代码range、1f68及24cc入口/边界均由ROM控制流复核 |
| #5 九个PLATE | PASS | 九条全文均给出，ASCII、最大431 bytes、无五组stale自动名 |
| #6 `080a1658`改名/CSV | PASS | 函数体支持新名；caller、inventory、CSV及registry边界均明确 |
| #7 参数与`1950`证据 | PASS | `1bc0`、`1f68`寄存器语义及`:7563/@18fa`证据均与机器码一致 |
| #8 R9门禁 | PASS | 物理备份、15/15 hash、source快照、dry/apply事务回滚、fresh只读、全流水线及失败恢复均可执行 |

## 核验 (C1-C13)

| # | 检查 | 结果 | 证据摘要 |
|---|---|---|---|
| C1 | Rule1范围与地址序 | PASS | 路线图范围一致，Seg-1至4已完成，本轮未进入Seg-6 |
| C2 | Rule2五块归宿 | PASS | 三R4、一dataization、两Rule3子范围完整；31个code range与pool/padding无空洞/重叠 |
| C3 | Rule3确为0引用 | PASS | 两范围packed scan `0/0`，Ghidra refs=0，无控制流或fall-through |
| C4 | EQ值 | PASS | 178/178 ROM words一致，127/127 EQ通过 |
| C5 | 复用/新增 | PASS | 116个REUSE EQ行全匹配；新增2 offset、2 global、4 alias无冲突；CID证据成立 |
| C6 | 槽名 | PASS | 178个slot label合法、唯一、无碰撞；共享case及后续编号正确 |
| C7 | LABEL/ref接通 | PASS | 七target、26 REF、25 RENAME source/primary合同完整；三表不建同址alias |
| C8 | PLATE现名 | PASS | 九条完整rewrite无旧自动名，首轮五条stale PLATE均覆盖 |
| C9 | ASCII/长度 | PASS | 9 PLATE与178 EOL全ASCII；PLATE最大431 bytes |
| C10 | Thumb/even | PASS | 五个odd槽对应四个`fn+1`唯一值；三表30项保持even且ROM值相等 |
| C11 | 函数误名 | PASS | `1658`改为row-type dispatcher名称；只create `1f68/24cc` |
| C12 | 消费者证据 | PASS | `1bc0/1f68/1950`修订与ROM机器码一致，关键语义均有file/address和high置信度 |
| C13 | 残留覆盖 | PASS | 原108与新增70完整；两个裸块头、25f0结构化表头及两Rule3范围均显式处理 |

## 实施门禁复核

proposal明确要求写入前递归物理备份 `.rep`，逐一核15个数据库文件size/SHA256，并建立正式
source存在性/size/SHA256快照；dry-run必须精确命中178槽、3个R4范围、1个dataization、2个
Function create、1个Function rename、9个PLATE、178个EOL、0 carve、0 FAIL。apply置于单一
Ghidra事务，事务内任一postcheck失败即rollback；save后以fresh `-noanalysis -readOnly`复核并要求
15个DB hash无变化。随后执行全范围导出、mode清理、`inject_modes.py`、`split_all_s.py`、
`export_all.py`与build，要求ROM大小33554432、逐字节相等及SHA1
`9689337d6aac1ce9699ab60aac73fc2cfdccad9b`。事务提交后或source编辑后的任何失败均从物理
`.rep`备份及source快照恢复并重验scope；Seg-6、stage和commit均被禁止。R9门禁完整且可执行。

## 状态: PASS

第二轮未发现C1-C13失败项；首轮八项修改均由独立证据闭合，可以进入Mode B落地。

## Reviewer Verdict: F13-Seg-5 = PASS

## Mode B retry-1 implementation review

本小节只审查 apply-1 失败后的retry-1窄修，不改变上文C1-C13与`PASS` verdict。审查输入为
`f13-seg5-apply1.log`、apply-1脚本快照、当前`RefineF13Seg5.py`、
`f13-seg5-apply1-to-retry1.diff`、retry-1 diagnosis/backup/prep/dry及DB hash证据。未运行apply、
build或commit。

### apply-1失败与ROM控制流

apply-1在完整preflight `FAIL=0`后停止于：

```text
Instruction coverage failed at 080a1fee in 080a1fc4..080a1ff8
```

ROM的独立Thumb objdump结果为：

```text
080a1fe8  2804       cmp  r0,#4
080a1fea  d900       bls  080a1fee
080a1fec  e112       b    080a2214
080a1fee  0080       lsls r0,r0,#2
080a1ff0  4903       ldr  r1,[pc,#12] -> 080a2000
080a1ff2  1840       adds r0,r0,r1
080a1ff4  6800       ldr  r0,[r0,#0]
080a1ff6  4687       mov  pc,r0
```

对应ROM字节为`042800d912e180000349401800688746`。`1fea`的条件分支确以`1fee`为目标；
从`1fc4`开始的单seed反汇编在`1fec`无条件跳往`2214`后不能覆盖`1fee..1ff8`，因此失败地址与
机器码一致。`1fee..1ff8`是五条完整Thumb指令，`1ff8`本身是后续pool起点，不属于该代码range。

### retry-1 diff与行为边界

独立对apply-1脚本快照和当前脚本执行diff，结果恰为两个hunk：

1. `INPUT_HASHES`新增retry-1物理备份与diagnosis两项冻结证据；这是输入门禁元数据。
2. `clear_and_disassemble`仍先清理并设置同一半开范围`[lo,hi)`，默认seed仍为`lo`；仅当
   `(lo,hi)==(080a1fc4,080a1ff8)`时追加seed `080a1fee`，随后对两个seed使用相同的
   `AddressSet(seed,080a1ff7)`和`enableCodeAnalysis(False)`。

唯一程序变换行为变化就是：清理原有`[1fc4,1ff8)`后，显式从`1fc4`和条件分支目标`1fee`
各启动一次Thumb反汇编。新增seed严格位于既有代码range内；清理下界、上界、TMode范围及覆盖
后检查均未改变，不触及`1fc0`或`1ff8`两个pool边界。

diff未改动`PLAN`、`CODE_GROUPS`、`CODE_RANGES`、`NEW_POOLS`、`BODY_RANGES`、槽动作、Function
动作、注释或source动作。`set_functions()`仍按冻结的精确body显式设置`080a1658/080a1f68/
080a24cc`，所以第二seed不会扩大或缩小Function body。保持不变的实施合同为：

- 178槽，`EQ=127 / REF=26 / RENAME=25`；
- R4代码range分组`18+2+11`，合计31；
- 70个pool、1个dataization、2个Function create、1个Function rename；
- 9个PLATE、178个EOL、2个Rule3范围。

### retry-1门禁证据

- 当前脚本SHA256为`3bae47f97ab6d07c252a7a4a1e7fbb81339b906fff29fdcf3b02772723ec8a1e`；
  apply-1脚本快照SHA256为`434cb5e8f2f3aaae78c4bc58ad8e16ced548ef5dc047ec8055f62631f8ccd86a`。
- 在本小节写入前，proposal/review/TSV/plan当前SHA256逐一等于冻结值：
  `4f24859a...b9028 / e5635e24...a477 / 785063ff...1df / 9dd26ff2...3a4f`。
- 独立重算当前 `.rep` 与
  `Yu-Gi-Oh WCT 2006.rep.bak-20260905-125951-pre-F13Seg5Retry1`：双方均为15个文件，
  相对路径、size与SHA256为15/15完全相同；retry backup JSON的15项也与实测current一致。
  原始pre-F13Seg5备份仍存在并在证据中标为preserved。
- source snapshot的40个原已存在路径逐一重算为40/40 size+SHA256不变；原先缺失的唯一路径
  `tools/ghidra-labeling/RefineF13Seg5.py`现为预定新增脚本，没有其他正式路径变化。
- retry-1 dry日志明确以`Processing read-only project file`启动，preflight为
  `slots=178 ... CODE_RANGES=18+2+11 ... FAIL=0`，最终为
  `STATUS: OK mode=dry FAIL=0`。`f13-seg5-retry1-dry1-db-before/after.json`经独立规范化比较为
  15/15完全相等，fresh read-only未改变数据库文件。
- 当前不存在`f13-seg5-apply-receipt.json`或`f13-seg5-persisted-check.json`；retry prep记录
  `realApplyExecuted=false`、`applyReceiptAbsent=true`、`stagedFiles=[]`。现有apply日志只有已失败的
  apply-1，没有retry-1 real apply。

apply-1的物理DB before/after清单并不相等；retry准备阶段已经恢复prestate，并以恢复后的current
重新建立15/15精确物理备份。随后rollback后dry与retry-1 dry的各自DB before/after均15/15相等，
当前脚本dry又完整校验5209 Function及全部冻结前态。因此retry-1放行基线是已恢复的current与新
物理备份，而不是apply-1失败后的物理文件集合。

### 结论: RETRY_PASS

retry-1准确补齐`080a1fee`这一真实条件分支入口；没有改变批准的range/body/pool/槽或其他动作。
备份、dry、fresh read-only、冻结输入与“未real apply”证据完整，可以由root在更新本次review
写入产生的新SHA256后，重新冻结hash链并重跑prep/dry/DB门禁；全部重门禁通过后方可放行real
apply。本结论本身不授权跳过root重门禁。

## Retry-2 probe2 implementation review

本小节只审查retry-1 real apply失败后的动态gap-fill及probe2证据，不改变上文C1-C13的`PASS`
verdict，也保留retry-1的历史审查记录。审查期间未运行apply/build、未修改Ghidra或正式源码、未
stage/commit。

### 两次real apply失败与修复范围

独立读取两次失败日志：apply-1在完整preflight `FAIL=0`后停于
`080a1fee in 080a1fc4..080a1ff8`；retry-1也在完整preflight `FAIL=0`后停于
`080a2020 in 080a2018..080a2056`。两者都发生在`clear_and_disassemble`的连续覆盖检查，尚未
到达pool、槽、Function或comment动作。retry2 diagnosis将根因限定为：Ghidra递归反汇编在批准的
纯Thumb半开区间内遇到控制流断点后停止，固定补一个`1fee`不能覆盖后续同类CFG gap。日志地址、
ROM控制流与该诊断一致。

### 31个range与独立ROM解码

从冻结plan重新取得31个批准range，以ROM `roms/2343.gba`为输入逐range执行Thumb objdump，
并按每行机器码半字数独立计算Instruction长度。31/31均满足：首条地址等于`lo`，相邻指令无
gap/overlap，末条指令终点恰等于`hi`，无undefined解码。各range指令数为：

```text
11,11,11,11,8,5,11,11,8,8,8,5,11,11,8,2,2,10,
41,25,29,20,11,19,27,13,4,14,16,9,29
```

独立合计为`409 instructions / 886 bytes`，逐range与
`f13-seg5-retry2-probe2-coverage-before-rollback.json`的31行全部相等，mismatch为0。

又把每个R4区间按code/new pool/padding重新排序覆盖，三个半开区间均无空洞、重叠或越界：

| R4区间 | 总字节 | code | pool | padding |
|---|---:|---:|---:|---:|
| `[080a1720,080a190a)` | 490 | 340 | 140 | 10 |
| `[080a1f68,080a2000)` | 152 | 134 | 16 | 2 |
| `[080a2018,080a2234)` | 540 | 412 | 116 | 12 |

因此31个range边界只覆盖已批准代码；区间内68个pool与全部padding均被排除。另两个new pool
`080a1950`和`080a2000`位于这三个R4半开区间外，也不与code range相交。

### 五个动态gap seed

probe2记录的五个gap地址均由ROM机器码独立确认是偶地址Thumb指令边界，且是明确控制流目标：

| gap seed | 入边机器码 | seed处首条指令 | 结论 |
|---|---|---|---|
| `080a1fee` | `080a1fea d900 bls 080a1fee` | `0080 lsls r0,r0,#2` | 条件分支目标 |
| `080a2020` | `080a201a d101 bne 080a2020` | `f7a8 fba4 bl 0804a76c` | 条件分支目标 |
| `080a2076` | `080a206c d003 beq 080a2076` | `4644 mov r4,r8` | 条件分支目标 |
| `080a2084` | `080a207a d003 beq 080a2084` | `20eb movs r0,#235` | 条件分支目标 |
| `080a21f6` | `080a21ec d003 beq 080a21f6` | `1c28 adds r0,r5,#0` | 条件分支目标 |

这些地址全部严格落在各自批准range内部；没有seed落入pool/padding或半开上界。

### gap-fill实现与动作漂移

当前脚本SHA256为`506b5c50d3ca64ba977bc313237af57d91975852eb49c4ad6774a50caa12407e`。
独立读取脚本并对retry-1脚本快照作diff，实际apply路径的变化限定为：

1. `clear_and_disassemble(lo,hi)`仍只清理并设置TMode于原批准`[lo,hi)`，先从`lo`反汇编；随后
   从`lo`开始按Ghidra实际`Instruction.getLength()`顺扫。
2. cursor无Instruction时，先用`getInstructionContaining`拒绝中段重叠，再仅以当前cursor作为
   同一range内的新seed；seed后仍无Instruction即失败。
3. 每条Instruction均检查`length>0`、`cursor+length<=hi`及不与70个new pool/全部padding相交；
   最终cursor必须精确等于`hi`。`disassemble_seed`还拒绝奇地址、range外地址和reserved首半字。
4. `verify_probe_state`再次逐Instruction验证31个range，并逐字节确认pool/padding内不存在任何
   Instruction。以上守卫与独立ROM解码共同排除越界、重叠及pool/padding误吃。

retry-1到retry2的其他差异为冻结元数据、额外preflight reserved-overlap守卫和强制rollback的
probe模式；`apply_all`只是把原有三组range循环等价提取为`apply_probe_ranges()`，后续顺序仍是
padding、70 pools、target/case、178槽、Function、PLATE。合同保持
`EQ127/REF26/RENAME25`、31 ranges、70 pools、`FUNC_CREATE2/FUNC_RENAME1`、9 PLATE、178 EOL，
三个Function body仍完全取冻结`BODY_RANGES`。因此除通用gap-fill外没有实际apply动作漂移。

又独立比较probe1脚本快照与当前脚本，diff只新增coverage汇总及“rollback前落盘”证据，并删除
同一Ghidra session中rollback后的prestate断言；`overlaps_reserved`、`disassemble_seed`、
`clear_and_disassemble`、`apply_probe_ranges`、`verify_probe_state`和`apply_all`均未改变。

### probe2时序、恢复与冻结状态

probe1的coverage动作完成后，在同一session强制rollback后立即重查prestate得到104项listing/ref
差异；这是rollback后的同session视图不适合作持久态证明。probe2把coverage证据明确在事务仍待
rollback时写出，再由`finally`强制`endTransaction(...,False)`，随后用物理恢复和全新只读进程
证明prestate，时序闭合：

- `13:29:13`记录probe2 DB before；`13:29:25`写出rollback前coverage，状态为
  `PROBE2_COVERAGE_PASS_BEFORE_ROLLBACK`、`coverage_FAIL=0`、31 ranges、409 instructions、
  886 bytes、5 gap seeds，且语义动作计数全部为0；日志随后打印forced rollback返回。
- probe进程退出时Ghidra仍产生新generation物理文件，所以不把同session rollback当物理恢复
  证明。`13:29:29`从retry2物理备份恢复并删除额外generation；本审查重新计算当前`.rep`与
  `Yu-Gi-Oh WCT 2006.rep.bak-20260905-131746-pre-F13Seg5Retry2`，双方相对路径、size、SHA256
  为15/15完全相等。
- `13:29:56`后启动全新dry进程；日志明确为`Processing read-only project file`，完整preflight
  `FAIL=0`且最终`STATUS: OK mode=dry FAIL=0`。fresh DB before/after清单经独立规范化比较为
  15/15完全相等。
- source snapshot的40个原已存在路径经重新计算size/SHA256为40/40不变；当前不存在
  `f13-seg5-apply-receipt.json`或`f13-seg5-persisted-check.json`，没有retry2 real apply/build。
- 本小节写入前，proposal/TSV/plan SHA256仍分别为
  `4f24859a66f2b7580c7599312488a961a55b6270f1d8aa0c3eb4b8612b3b9028`、
  `785063ff6264fcd036b96df641c397f031f9da0c42540df8702ddfd54b5ed1df`、
  `9dd26ff219d5e5f6182fc66a65e1d27bdc38a4d6eedff49e68748073bd8c3a4f`；均与gate冻结值一致。

### 结论: RETRY2_PASS

动态gap-fill严格受31个批准半开code range、Instruction实际长度及pool/padding守卫约束；独立ROM
复核与probe2均得到31 ranges、409 instructions、886 bytes及同一组五个真实控制流gap seed。
除gap-fill外没有apply动作漂移，rollback前coverage、物理恢复15/15及fresh read-only前态证据
顺序完整。

root可以在重新冻结本次review写入产生的新SHA256、同步脚本输入hash并重跑最终dry/root门禁后
放行real apply；任何hash、dry、DB或动作计数不一致都必须停止。本结论不允许复用写入前的旧
review hash，也不授权跳过最终门禁。

## Retry3 symbol-order implementation review

本小节独立审查retry2 real apply的`PRIMARY_OBJECT_PRE 080a2004`失败、retry3操作顺序及
`symbol_probe`证据；不改变原C1-C13的`PASS`及retry1/retry2历史结论。审查中未运行apply/build，
未修改Ghidra、脚本、proposal、TSV或正式源码，未stage/commit。

### `080a2004`失败的精确根因

retry2日志显示完整preflight `FAIL=0`，随后在旧`apply_all()`已依次执行31-range disasm、padding
clear和70个pool dataization后，首次进入`normalize_targets_and_cases()`即失败于
`PRIMARY_OBJECT_PRE 080a2004`。冻结前态给出以下依赖链：

- `080a2000`是`/undefined *` DataDB，唯一operand-0 DEFAULT DATA reference为
  `080a2000 -> 080a2004`；
- `080a2004`的唯一primary `PTR_DAT_080a2004/DEFAULT`，动态ID为
  `4611686018562269188`，正由上述入边派生；
- `080a2000`又是本轮new pool，`create_pool(080a2000)`先执行
  `clearCodeUnits(080a2000..080a2003)`，再创建普通`/dword`；DATA/USER_DEFINED reference只会在
  后续`apply_slot(080a2000)`建立。

因此旧顺序在normalize消费冻结Symbol身份之前删除了`2000 -> 2004`这一唯一DEFAULT引用，使
`080a2004`的动态primary不再满足“同址唯一且ID等于冻结值”的前置条件。

disasm-only的retry2 probe1残留视图进一步排除了“R4本身替换ID”这一归因：其
`TARGET_PRE 080a2004`实际仍是同一个动态ID `4611686018562269188`、同址count 1和相同入边；只有
派生显示名从`PTR_DAT_080a2004`变为`PTR_LAB_080a2004`，而
`rename_primary_same_object()`的`PRIMARY_OBJECT_PRE`只核同址数量、primary存在及ID。因此当前
`f13-seg5-retry3-diagnosis.json`把直接原因写成“R4 disassembly ... replaced a DEFAULT-derived
primary object”与冻结前态、probe1及`create_pool`顺序不一致。正确的直接失效点是
`create_pool(080a2000)`清除了唯一派生引用；通用顺序约束则应表述为“在任何会重建listing/ref的
动作前先消费并规范化全部批准Symbol”。

### retry3操作顺序与幂等性

当前脚本SHA256为`b152aac47f66127cf9aac5ec795a814c7d9ce0f0ae13de3b9bc1c71c82139f11`。
独立比较retry2脚本快照与当前脚本，实际apply路径的变化符合预定窄修：

1. `normalize_targets_and_cases()`从R4/padding/pool之后前移到`apply_probe_ranges()`之前；原后置
   调用已删除，apply路径只调用一次。
2. `PRENORMALIZE_SWITCH_SLOTS`精确为`(080a16d4,)`。三个switch table中，`080a2004`已在
   `TARGET_CONTRACTS`，`080a25f0`已在`CASE_LABELS`，仅`080a16d4`原本只由slot动作命名，因此
   这一个补充地址集合完整且无扩大。
3. `080a16d4`的冻结动作是唯一一行`RENAME`。预规范化只把其唯一primary改为批准的
   `equip_row_type_switch_table/USER_DEFINED`，不增加动作计数；后续`apply_slot(080a16d4)`不改
   reference，只进入`ensure_slot_label`。由于name/source已相等，该函数不再rename，仅确认primary、
   count 1、写EOL并把`RENAME/EOL`各计数一次。因此同址无alias且动作不会重复计数。
4. 后续顺序仍为31-range disasm、padding、70 pools、178 slots、Function、PLATE；diff中的其余
   内容为冻结元数据、symbol_probe观测代码和preflight合同。`apply_slot`、gap-fill、pool、Function
   等实施函数未改变，合同仍是`EQ127/REF26/RENAME25`、31 ranges、70 pools、
   `FUNC_CREATE2/FUNC_RENAME1`、9 PLATE、178 EOL。

该前移顺序确实在`create_pool(2000)`清理派生引用前物化`080a2004`为USER_DEFINED Symbol，且
symbol_probe证明其随后可穿过全部R4 disasm而保持身份。所以实现修复本身覆盖了精确根因。

### 32地址三态与switch组

从冻结plan独立重建批准name映射：7个`TARGET_CONTRACTS`、24个`CASE_LABELS`及唯一补充槽
`080a16d4`，合计32个互异地址。逐项把probe的`before -> normalized -> post_disasm`与plan及
`f13-seg5-slots-before.json`交叉，结果如下：

- 三阶段均为32行/32个唯一地址；before逐项等于冻结Symbol前态，normalized及post-disasm逐项为
  批准name、global、USER_DEFINED、primary且同址symbol count 1，无alias。
- before来源分布为27 DEFAULT、1 ANALYSIS、4 USER_DEFINED。27个DEFAULT动态Symbol全部且仅在
  normalize时更换为实体USER Symbol ID；非DEFAULT地址无ID变化。normalized到post-disasm的
  额外ID变化为0/32。
- `080a2004`三态为
  `4611686018562269188/PTR_DAT_080a2004/DEFAULT ->
  32683/equip_target_select_phase_switch_table/USER_DEFINED -> 同一32683`，每阶段count 1。
- `080a25f0`三态均保持同一对象ID `4719`；只在normalize把scoped
  `switchdataD_080a25f0/ANALYSIS`移动/改名为global
  `equip_activation_card_type_switch_table/USER_DEFINED`，post-disasm仍为ID 4719。
- 从30个switch words重新分组去重，row type为18个目标、target-select phase为5个目标、
  activation card type为6个目标；三阶段probe地址集合与plan分别18/18、5/5、6/6完全相等。
  六个activation case目标`080a2608/2644/2652/26e8/272c/2770`均保持原ANALYSIS对象ID
  `4712..4717`，未被本轮规范化或R4改变。

symbol_probe动作计数只有`R4_REGION=3/CODE_RANGE=31`，EQ/REF/RENAME/pool/Function/PLATE/EOL
均为0，证明该probe未偷偷执行其余语义动作。

### R4覆盖、恢复与冻结门禁

重新对冻结31个range逐一执行ROM Thumb objdump，并以机器码半字数计算Instruction长度；31/31
均从`lo`连续覆盖至`hi`、无undefined或probe逐range差异。独立合计仍为31 ranges、409
instructions、886 bytes，gap seeds仍精确为
`080a1fee/080a2020/080a2076/080a2084/080a21f6`。

symbol evidence于`13:57:09`在事务仍待rollback时写出，`FAIL=0`后由`finally`强制rollback；
`13:57:12`从retry3物理备份恢复并删除额外generation。独立重算当前`.rep`与
`Yu-Gi-Oh WCT 2006.rep.bak-20260905-135103-pre-F13Seg5Retry3`为15/15相对路径、size、SHA256
完全相同。随后fresh dry日志明确为`Processing read-only project file`、preflight/final均
`FAIL=0`；fresh DB before/after独立规范化比较为15/15完全相同。正式source快照40个原已存在
路径为40/40 size/SHA256不变；不存在apply receipt或persisted check，也没有retry3 real
apply/build。

本小节写入前，proposal/review/TSV/plan SHA256分别为
`4f24859a66f2b7580c7599312488a961a55b6270f1d8aa0c3eb4b8612b3b9028`、
`7e1e205298a86438db2f8096c24a4073b0522495c6f01a25be49b01713b04fec`、
`785063ff6264fcd036b96df641c397f031f9da0c42540df8702ddfd54b5ed1df`、
`9dd26ff219d5e5f6182fc66a65e1d27bdc38a4d6eedff49e68748073bd8c3a4f`，与symbol-probe gate
冻结值一致。

### 结论: NEEDS_FIX

retry3代码顺序、32地址Symbol三态、18/5/6 switch组、R4覆盖和恢复门禁均通过；唯一失败项是
冻结diagnosis对`PRIMARY_OBJECT_PRE 080a2004`的直接触发操作归因错误。证据链不能以错误根因
进入real apply。

#### #1 — Retry3 diagnosis — 修正`080a2004`直接失效点并重冻结

1. 将`f13-seg5-retry3-diagnosis.json`的cause改为：旧顺序在normalize前执行
   `create_pool(080a2000)`，其`clearCodeUnits(080a2000..080a2003)`删除唯一DEFAULT DATA reference
   `080a2000 -> 080a2004`，从而使派生动态primary `PTR_DAT_080a2004`的冻结身份失效；不要再把
   “R4 disassembly替换该ID”写作直接原因。
2. 保留当前“normalize在任何R4/padding/pool动作前执行”、`PRENORMALIZE_SWITCH_SLOTS=(16d4,)`
   及全部实现逻辑，不需要扩大代码行为。
3. 更新diagnosis hash、脚本`INPUT_HASHES`及脚本hash，重新冻结本次review新SHA256；随后重跑
   symbol_probe、强制rollback、物理恢复15/15、fresh read-only dry/DB before-after和root最终
   门禁。所有计数、32地址三态、31/409/886/5 gaps及无receipt条件必须再次相等，才可申请real
   apply。

## Retry3 NEEDS_FIX修后复核

本小节复核上一节唯一修改项的闭合状态；上一节`NEEDS_FIX`作为历史保留，当前控制结论以本小节
为准。本轮未执行apply/build，未修改Ghidra、脚本、proposal、TSV或正式源码，未stage/commit。

### 根因修正与实现冻结

最新`f13-seg5-retry3-diagnosis.json`已把直接原因改为：旧顺序中的
`create_pool(080a2000)`在normalize前调用
`clearCodeUnits(080a2000..080a2003)`，删除唯一DEFAULT DATA reference
`080a2000 -> 080a2004`，从而使派生动态primary `PTR_DAT_080a2004`的冻结身份失效。该表述逐项
对应冻结前态：`080a2000`为带上述唯一出边的`/undefined *` DataDB，`080a2004`的唯一入边就是
该引用，且其primary ID属于DEFAULT动态ID。上一节#1的根因归因已精确修正。

当前脚本SHA256独立重算为
`3b7d3f8649c3939b1ff02d3fae77c20f3337984ec12e36e1c6a97b07b79926ea`。将修正前脚本快照
`b152aac4...9f11`与当前脚本直接diff，只有两个hunk：review冻结SHA256从`7e1e2052...fec`更新为
`7fb703f2...f79e`，retry3 diagnosis SHA256从`9bd9d6d5...9253`更新为
`05707e43...2521`；不存在行为代码变化。

因此已审定的唯一apply行为窄修保持原样：`normalize_targets_and_cases()`仅调用一次，并从
R4/padding/pool之后前移到`apply_probe_ranges()`之前；`PRENORMALIZE_SWITCH_SLOTS`仍精确为
`(080a16d4,)`，原后置normalize调用仍已删除。`080a16d4`仍是唯一`RENAME`槽，预规范化不增加
计数；后续`apply_slot`只幂等确认既有USER_DEFINED primary、写EOL，并将`RENAME/EOL`各计一次，
不会新建alias或重复slot动作。

### symbol probe与覆盖复核

修正后重新生成的`f13-seg5-retry3-symbol-probe-before-rollback.json`经独立重建plan映射并逐项
比较，结果为：

- before/normalized/post-disasm均覆盖同一32个互异批准地址，三阶段同址symbol count均为1；
  normalized与post-disasm均为批准name、global USER_DEFINED primary，无alias。
- normalize阶段ID变化精确为27，全部且仅来自before的DEFAULT动态Symbol；非DEFAULT对象无ID
  变化。normalized到post-disasm的额外ID变化为0。
- `080a2004`为
  `4611686018562269188/PTR_DAT_080a2004/DEFAULT ->
  32683/equip_target_select_phase_switch_table/USER_DEFINED -> 同一32683`，三态均唯一。
- `080a25f0`三态对象ID均为`4719`；18/5/6三个switch目标组的地址集合与plan完全相等。
- coverage保持31 ranges、409 instructions、886 bytes及5个gap seeds；probe动作计数仅为
  `R4_REGION=3/CODE_RANGE=31`，其余语义动作均为0。

### 恢复、dry与动作计数

symbol evidence在事务待rollback时写出并以`FAIL=0`结束，随后强制rollback和物理恢复。独立重算
当前`.rep`与`Yu-Gi-Oh WCT 2006.rep.bak-20260905-135103-pre-F13Seg5Retry3`，双方15个文件的
相对路径、size、SHA256为15/15完全相等。修后fresh prestate及final preapply dry均由全新
`-noanalysis -readOnly`进程运行；两组DB before/after分别都是15/15 byte-identical，日志均为
preflight/final `FAIL=0`。

final dry动作合同为`EQ=127/REF=26/RENAME=25`，三类slot动作相加精确为178；同时
`EOL=178`、`R4_REGION=3`、`CODE_RANGE=31`、`POOL_DATA=70`、`DATAIZATION=1`、
`FUNC_CREATE=2`、`FUNC_RENAME=1`、`PLATE=9`。当前`.rep`仍为前态，不存在apply receipt或
persisted check，gate明确`realApplyRun=false/buildRun=false`。

本小节写入前，proposal/review/TSV/plan/diagnosis SHA256独立重算分别为
`4f24859a66f2b7580c7599312488a961a55b6270f1d8aa0c3eb4b8612b3b9028`、
`7fb703f2a75a3b79be3886003a35581a933638a6d47b8965ac99d5edf2d2f79e`、
`785063ff6264fcd036b96df641c397f031f9da0c42540df8702ddfd54b5ed1df`、
`9dd26ff219d5e5f6182fc66a65e1d27bdc38a4d6eedff49e68748073bd8c3a4f`、
`05707e43e26a8cf1b44d6e1c9ea0ccbac6c22998973c38b36950ba6f852c2521`，均与修后gate一致。

### 结论: RETRY3_PASS

上一节唯一修改项已闭合；根因、脚本行为、32/27 Symbol合同、31/409/886/5覆盖、178槽动作、
物理恢复及只读DB门禁全部一致。root必须先把本小节写入产生的新review SHA256重新冻结到脚本，
并以更新后的脚本再跑final read-only dry/root门禁；全部通过后方可执行real apply，不得复用写入前
的`7fb703f2...f79e` review hash。

## Mode B real apply scope failure review

本小节只审查retry3 real apply后的production-export scope failure；原C1-C13 `PASS`和retry历史保留，
但在本小节修改项闭合前不构成继续落地授权。本轮未运行apply/build，未修改Ghidra、脚本、proposal、
TSV或正式汇编源码。

### `SUB_080a0b20`的来源

失败证据`f13-seg5-retry3-scope-failure.json`的SHA256为
`e326739efc9627b9159c99d990d7e761995234f50c200a3fa1e79f403854c4da`。该文件第4至12行记录：
transaction postcheck、persisted check和export/normalize/split均成功，production export scope在
`asm/13_equip_placement.s`的`080a0b20`发现新增`SUB_080a0b20:`，而批准范围只允许Seg-5
`[080a1658,080a27a0)`及`08094d30`单一caller operand。第13至14行还确认`export_all`和build均未运行。

独立读取ROM并强制Thumb反汇编得到：

```text
080a18b8: 8812       ldrh r2,[r2,#0]
080a18ba: f7ff f931  bl   0x080a0b20
080a18be: e024       b    0x080a190a
080a0b20: b5f0       push {r4,r5,r6,r7,lr}
```

ROM的`080a18ba..080a18bd`原字节为`ff f7 31 f9`。失败导出的
`asm/all.s.raw`（SHA256
`9ef50c518c357bc916c590e51fe4543a6cb6660b6560714fe68b550e549c9a23`）在316984行将其导出为
`bl SUB_080a0b20`，316271行定义该label，316272行才是原
`ROM_INCBIN 0xa0b20,0x818`。去mode中间件`asm/all.s.raw.nomode`（SHA256
`0e613c050402b5d9841ceef693af4a12addf28ca73787164b4a2842f994850a1`）仍在316982行保留同一call、
316269行保留同一label。`f13-seg5-export-normalize-split.json`（SHA256
`32228b72a2d6de5641b39a5883878b08c486465adab716cf20eaf33a439ef57d`）第9、15、18至20行分别固定
上述raw/nomode hash且三个生成步骤返回0。因此label不是mode清理或split产生的孤立文本。

`SUB_080a0b20`这个**名字**属于exporter/Ghidra为未命名flow target选择的自动名；其**存在**则由
`080a18ba -> 080a0b20`真实直接CALL引用触发，不能作为无语义导出噪声删除。目标首条指令同时是
标准保存寄存器的函数序言，与直接BL目标一致。

### 对既有Rule 3与Seg-5扫描的复核

全ROM重新搜索地址字面量仍得到`0x080a0b20` raw=0、`0x080a0b21` THUMB|1=0。这不否定上述CALL：
raw/THUMB扫描查找的是小端`.word`值`20 0b 0a 08`/`21 0b 0a 08`，而Thumb BL使用
PC-relative半字`ff f7 31 f9`编码。必须通过机器指令解码才能取得目标。

Seg-4 proposal SHA256
`2dba3097eafc80290faa35c4a8d7e02541b3a7cd7f08676c5d7f1cdcda2d4eba`在46行以地址字面量扫描和
“当前asm真实机器行”过滤得出verified refs=0；Seg-4 review SHA256
`21438e4af40d6d1b6f3678b4b92544728ef7e2f6d76d8fc60aa652c294de1985`第14行同样只确认当时当前asm
中的直接B/BL入边为0。当时`080a18ba`仍埋在未反汇编块中，所以该过滤源集合没有这条机器行。
这两个结论是当时状态下的暂存Rule 3证据，不是发现新flow edge后的永久豁免。

活动文档`doc/dev/p5-refine-13-equip-placement.md`（SHA256
`6854bc7033832bc72bd63120b1835536e9b4a166e1a5438e46a5cec725fe1633`）第203行已明确约定
`[080a0b20,080a1338)`“仅在后续发现真实外部入口引用时重新进入R4”。方法论第24至28行要求被引用
代码进入R4，§5.1唯一例外是全ROM无引用且“引用到时再处理”。本次真实BL正好触发该约定；
因此这是§5.1的受控重开，不是违反地址序的任意回头。

Seg-5 proposal SHA256
`4f24859a66f2b7580c7599312488a961a55b6270f1d8aa0c3eb4b8612b3b9028`遗漏了这条边：第399行的
“no referenced block enters §5.1”已被ROM机器码反证；第415行只冻结五块raw/THUMB及局部引用归因，
没有把新反汇编code ranges的全部直接B/BL目标与§5.1登记表交叉；第420行据此错误地禁止
`080a0b20`投影变化。前一轮review也未补做该跨表控制流检查。本次不是29/2等地址字面量计数错误，
而是ref-scan维度缺少PC-relative控制流边。

### 三条闭环路线判定

| 路线 | 结论 | 依据 |
|---|---|---|
| (a) 导出后删除label并保持所有越界源码不变 | ❌ | 保留`bl SUB_080a0b20`会产生未定义符号；把operand机械改成数值也只会隐藏真实CALL，仍违反“被引用代码进入R4”。 |
| (b) 在Ghidra预先移除/抑制target Symbol | ❌ | flow reference仍由真实BL产生，exporter可重新物化target label；连同flow ref一起抑制则损坏正确控制流并维持失真的Rule 3登记。 |
| (c) 扩大proposal scope并重开该§5.1块 | ✅ | 与ROM、export、方法论及活动文档的“引用到时再处理”合同一致，是最窄正确路线。 |

该问题不需要外部运行态或用户语义输入才能继续，故不是`BLOCKED`。

### 恢复状态与是否需要重新apply

历史receipt证明旧范围动作曾保存成功：`f13-seg5-persisted-check.json`（SHA256
`bf30b22362ca8f4568746c6c4abdadc77b63b7717a63739a39dca8b1cb14dd81`）第2至22行记录`FAIL=0`、
31 ranges、178槽动作、2 Function creates、1 Function rename及`PERSISTED_CHECK_OK`。但scope redline后
该落地状态已全部恢复，不能继续沿用：

- `f13-seg5-retry3-scope-failure-db-restore.log`（SHA256
  `6bdc732747e3708ccf238d6d6a429cc8fb42160286141f011c5615178604cd4a`）第2至7行记录物理恢复、15个
  DB文件size/SHA256完全相等及额外generation清除；本审查再次枚举当前`.rep`与
  `.rep.bak-20260905-135103-pre-F13Seg5Retry3`，相对路径集合15/15、size/SHA256差异0。
- `f13-seg5-retry3-scope-failure-source-restore.json`（SHA256
  `acbf8f35fa2394b20c0ea9bb0ae50771d088dbc79e0785575a7bb62f12027b6b`）第2至17行记录11个正式文件
  已恢复；当前`asm/all.s`和`asm/13_equip_placement.s` SHA256分别为
  `94040577804bdb5814cfcb4ecf1b7d1e9351c1e1a014a0373af851c56984560`、
  `aaa2b403112747ba06a0994ca7688044542adc935c807f8a95edb3d54a7b9044`，与pre-source snapshot相同。
  `pre-f13-seg-5-formal/asm/all.s:316270`只有原incbin，不含新增target label。

所以修订后必须从恢复的prestate重新备份、dry、real apply及persisted/export/build；现存receipt和
失败导出的raw文件只能作诊断证据，不能作当前落地凭据。

### 结论: NEEDS_FIX

#### #1 — C3/Rule 3 — 撤销`080a0b20..080a1338`的整块0-ref结论

在Seg-5 proposal中登记精确边`080a18ba CALL -> 080a0b20`及ROM半字，修正第399、409、415、420行
相关结论和scope合同；同步把活动文档该整块§5.1记录改为“被引用、待R4闭合”，但正式进度文档只在
新一轮全部门禁通过后落地更新。

#### #2 — C2/R4 — 为目标块提交精确可实施的reachable closure

以`080a0b20`直接BL目标和函数序言为入口，自主重做递归Thumb控制流、fall-through、全部直接
B/BL、literal pool和padding边界归因；为`080a0b20`建立明确Function create、语义名、参数、精确
body与ASCII PLATE/EOL合同。旧证据中的822 instructions/1754 code bytes、71 literal words/284
bytes、17 padding/34 bytes只能作为交叉基线，不能直接替代新proposal。若递归closure没有覆盖原
2072B整块，剩余每个半开子区间必须分别重跑raw/THUMB与机器控制流入边扫描，只有再次证实0有效
引用的子区间才能重新登记§5.1；不得继续把整块保留为一个incbin。

#### #3 — C1/C11/C13 — 重冻结扩大后的范围、Function及动作合同

更新plan/TSV/script的批准地址、R4 ranges、pool/padding、Function count/ID/body、自动名残留及导出
投影合同。当前prestate在`080a0b20`无Function；若新闭包只新增这一入口，则与原Seg-5两个create
合计应从5209到5212；若控制流证明额外真实入口，必须逐一列地址与证据并相应冻结计数。不能仅将
`SUB_080a0b20:`加入scope白名单，也不能让该自动名成为最终语义名。

#### #4 — C3 landing guard — 增加PC-relative控制流全覆盖门禁

对原31个及新增的每个批准code range解码全部直接B/BL，按指令地址计算目标，并与Function范围、
pool/padding、proposal scope及活动§5.1区间交叉。门禁必须显式命中
`080a18ba -> 080a0b20`，且任何其他落入§5.1或未批准范围的目标都在写入前停止。保留原raw/THUMB
地址字面量扫描；两类扫描互补，不能互相替代。

#### #5 — R9 — 从已恢复prestate完整重走落地

在proposal、TSV、plan、script和本review重新冻结并通过独立review后，创建新的物理15/15备份，
重跑fresh read-only dry、real apply、persisted check、全量export/normalize/split、production scope、
`export_all.py`、build及byte-identical SHA1门禁。任一失败按新备份和source snapshot恢复；不得复用
本次历史receipt或假定已恢复DB仍含Seg-5动作。

## Scope Reviewer Verdict: F13-Seg-5 = NEEDS_FIX(5 items)

## Expanded-scope full re-review

本小节对scope failure后扩大的proposal重新执行完整C1-C13审查；前一节`NEEDS_FIX(5 items)`保留为
历史，五项修改的当前闭合结论以本小节为准。本轮只读取ROM、proposal、TSV、edge ledger、正式源码
和冻结前态证据；未修改proposal/TSV/Ghidra/脚本/正式源码，未运行apply/build，未stage/commit。

冻结输入经独立重算为：

- proposal SHA256
  `b045999088ac6e758eb236e9920d26a74941532b7ce208bd6322176244d67317`；
- TSV SHA256
  `ff0425315b47c77c8576776d66abfe01d8415acdb1cda3c3f3bc7ab4d64d4664`，250行含249行数据；
- edge ledger SHA256
  `88ac58dc4bc0815933535bbd8252a84d959acb9e4955bc05936ed4563dbf182a`，376行含375行数据；
- 本小节写入前review SHA256
  `2c6f7cdca625718c7e0a8c57e739b35d659254fc00c8fda94ce4a5fdfaf1fa8c`；
- ROM为33554432 bytes，SHA1
  `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`。

proposal/TSV 的禁用措辞扫描结果为 0。

### 历史块递归closure

审查没有采用executor给出的range集合驱动解码，而是从ROM入口`080a0b20`重新执行Thumb递归流：
普通指令跟随fall-through，条件B同时加入target/fall-through，无条件B只加入target，BL加入callee及返回点，
BX/POP-pc/MOV-pc终止当前路径；每条PC-relative LDR独立解析word地址并在下一轮排除literal Data。
两轮达到固定点，结果精确为：

- 49个互异半开code ranges，822条有效Thumb指令，1754 bytes；
- 71个互异且4-byte对齐的literal words，284 bytes；地址集合与TSV中小于`080a1658`的71行逐项相等；
- 17个互异2-byte剩余区间，34 bytes，每处ROM字节均为`00 00`；
- code/pool/padding两两不交，合计`1754+284+34=2072`，完整覆盖
  `[080a0b20,080a1338)`，无洞、无残余子区间；
- 逐range再次调用GNU objdump强制Thumb，49/49起止精确，无undefined、跨pool或跨padding指令。

`080a0b58: f000 fbe0`独立解码为`bl 080a131c`。`080a131c..132e`没有prologue，执行
`0xc4<<2=0x310`恢复sp、恢复r8/r9/sl和r4-r7，随后从原保存栈恢复返回地址并`bx`；它与入口
`080a0b2a..0b2c`加载`0xfffffcf0`并分配0x310-byte frame严格配对。全ROM对`080a131c`的packed
raw/thumb命中为4/1，但五个host均不在当前asm机器行或结构化`.word`地址；递归closure内唯一指向它
的真实边来自`080a0b58`。冻结Function前态也没有`080a131c`入口。因此它是
`tick_equip_card_message_by_id`的共享local epilogue，不是第二个Function。

### `tick_equip_card_message_by_id`语义与APCS

独立ROM反汇编确认`080a18a8..18ba`依次从`gP1LifePoints+1d8c/1d98/1d9a`加载r0 word、r1/r2
halfword，再以`ff f7 31 f9`调用`080a0b20`。现有常量与消费者把`1d8c`定为
`EQUIP_CONTEXT_PLAYER_OFF`；callee在入口把r0保存到r7、把r1零扩展到r6，entry r2在任何读取前由
`080a0b50`的literal LDR覆盖。因此签名
`u32 tick_equip_card_message_by_id(u32 player_id, u16 card_id, u16 unused_row_value)`成立。

入口从`gP1LifePoints+EQUIP_PHASE_DISPLAY_STATE_OFF`读取状态：0进入card-id分派和field/hand/zone/
stat/score/PRNG路径，1进入card-name/game-text格式化与display-op-31路径，其他值复制共享display word；
`080a130e..1318`递增同一phase word，所有退出通过共享epilogue返回0或1。对49 ranges的BL重新按ROM
解码并用`temp/ghidra-functions.csv`映射，得到18个callee target：copy/append text、两个format、
zone count、card field/stat/score、三类display-op、PRNG、hand-field check、card name和两类game-text
lookup；逐callee出现次数与proposal §3.0完全相等。

closure的CID槽还独立与`constants/card_info.inc`及`data/card-stats.s`交叉：28个命名CID均按同值
命中结构化`slot=0x....`记录；`cid_12c6/cid_135b/cid_16d3/cid_1803`均为已有明确未分配常量且
结构化记录为0；`0x1368`按现有`SPELL_ZONE_TARGET_CARD_ID`的非card-stats消费者复用。函数名、参数、
返回值和proposal第411行456-byte PLATE均有caller/callee/global/CID四类证据，置信度为high。

### 合并R4与直接边账本

原Seg-5的31个code ranges与旧`f13-seg5-plan.json`逐项相同。对49+31共80 ranges重新按ROM
Instruction长度顺扫并另用GNU objdump交叉，得到1231 instructions/2640 bytes，80/80边界精确。
其中原31 ranges仍为409 instructions/886 bytes，扩大closure贡献822/1754。

独立解码80 ranges中的每一条直接B/BL，按`source/op/target/ROM bytes`排序后与edge ledger逐行比较，
375/375完全相等：89 BL、286 B、226个unique targets。再以独立递归ranges、Seg-5 ranges、冻结
Function entry/body和pool/padding/§5.1集合分类，结果为：

| target class | count |
|---|---:|
| REOPENED_R4_CODE | 234 |
| REOPENED_LOCAL_EPILOGUE | 1 |
| REOPENED_FUNCTION_ENTRY | 1 |
| SEG5_R4_CODE | 35 |
| SEG5_NEW_FUNCTION_ENTRY | 1 |
| EXISTING_FUNCTION | 85 |
| EXISTING_FUNCTION_BODY | 17 |
| EXTERNAL_EXISTING_STUB | 1 |

分类与ledger逐行相等；pool、padding、两个当前Rule-3范围和UNAPPROVED的target均为0。
`080a18ba -> 080a0b20`精确出现一次，原scope failure的控制流漏项已闭合。

### `080a187a -> 080a38f8`边界裁定

该唯一边独立解码为`080a187a: f002 f83d bl 080a38f8`，目标ROM四字节为`01 20 70 47`，即
`movs r0,#1; bx lr`。全ROMpacked raw/thumb地址命中仍为0/0，但直接BL是真实引用。活动路线图明确
Seg-6为`[080a27a0,080a38fc)`，且其唯一裸块正是末尾`[080a38f8,080a38fc)`；所以本轮抢先对该
stub执行R4/Function/语义命名会越过尚未处理的Seg-6低地址内容，违反严格地址序。

允许本轮只接受自动target projection，理由和边界均已具备：

1. 失败轮生成证据`asm/all.s.raw:316952`已经把caller导出为`bl SUB_080a38f8`，
   `asm/all.s.raw:321663`定义同名Symbol，下一行仍是原四字节`.byte`；因此GAS有定义可解析，
   不是静默未定义自动名。
2. proposal第3、438、488、506、517、520行把这一行列为唯一越界projection，要求四字节和listing
   type不变，禁止R4、Function、语义名、comment及任何第二项Seg-6 delta。第514行的“不得mutate
   Seg-6 Symbol”按同一合同解释为不得**显式**创建/重命名USER/ANALYSIS Symbol；source disasm产生的
   单一DEFAULT `SUB_080a38f8`是已冻结的唯一自动副作用。
3. Rule 2要求该被引用代码在其所属段处理；严格地址序要求下一任务仍是完整F13-Seg-6
   `[080a27a0,080a38fc)`从低到高，而不是跳到末尾stub。Seg-6不得在关闭`38f8..38fc`前标记完成，
   且到达该末尾块时必须R4、建立Function/语义名并消除`SUB_080a38f8`。proposal中的pending记录
   不得解释为先行跳址。

在以上冻结解释下，当前轮接受该唯一projection不违反Rule 1/2；任何额外Seg-6输出变化或把自动名
当成最终结果都使landing gate失败。

### 槽、常量、Symbol与文本

- TSV精确249行，地址和`slot_label`各自249/249唯一，全部slot label符合
  `^[a-z][a-z0-9_]+$`。action为EQ190/REF33/RENAME26；closure为63/7/1共71，原Seg-5为
  127/26/25共178。expanded TSV中这178行与旧plan按address、old_name、value、action、target、
  slot label、reuse、evidence、EOL逐字段完全相等；原合同没有漂移。
- 249/249 `original_value`均等于对应ROM四字节小端word。190个EQ target及33个REF target全部可解析
  到同值；30个switch words为19/5/6三组且全部偶地址，五个callback槽对应四个Function并全部是
  精确`entry+1`奇地址。
- TSV reuse为224 REUSE/25 NEW。proposal真正新增的七个numeric/global定义对当前6051个`.equ`
  进行表达式求值后，同值命中均为0；四个GAS alias名称也不存在。所有REUSE target均已存在且值
  与ROM相等。新Function名、local epilogue名及新增constant/global名在正式符号源中无碰撞。
- 七个REF target的前态name/source/Data与`f13-seg5-slots-before.json`逐项相等；33个REF行明确冻结
  operand-0 `DATA/USER_DEFINED/primary`。26个RENAME行包含完整pre-reference tuple，新增closure行
  `080a12f4`保持none，原25行与旧plan完全相等。
- 十个PLATE逐项ASCII byte长度为456/271/431/282/308/280/392/200/367/375，max456；249个slot
  EOL与`080a131c`的72-byte EOL全部ASCII、非空，PLATE/EOL均无`FUN_/SUB_/DAT_/DWORD_/PTR_DAT_/
  UNK_`自动名残留。
- 冻结前态Function总数5209、named5119、auto90；Seg-5既有38个Function，`080a0b20/131c/1f68/
  24cc/38f8`均无Function。只创建`0b20/1f68/24cc`并保留`131c`为local、`38f8`待下一段后，精确
  为total5212/named5122/auto90。`080a1658`现有ID16936及`08094d30`唯一incoming合同保持。

两个当前§5.1范围另行逐halfword执行全ROMpacked扫描：`1dd8..1de8`八个候选和
`1f54..1f68`十个候选的raw/thumb总计各为0/0；解析当前asm全部真实机器行并合并新80 ranges后，
没有直接B/BL落入任一区间。前函数分别在`1dd6`、`1f52`返回，后续Function分别从`1de8`、`1f68`
开始，无fall-through。历史`0b20..1338`整块不再符合§5.1，并由无洞R4 partition完整取代。

### C1-C13复核

| # | 检查 | 结果 | 独立证据 |
|---|---|---|---|
| C1 Rule1 | 扩大范围与地址序 | ✅ | 只重开有新引用的历史§5.1块；Seg-5仍为原范围。38f8只允许冻结projection，R4留给下一完整Seg-6按低到高执行。 |
| C2 Rule2 | 每块有归宿 | ✅ | 历史2072B全量R4无残余；原五块分别R4/dataization/两段§5.1，无静默保留；38f8明确成为下一Seg-6必处理项。 |
| C3 Rule3 | 保留块0有效引用 | ✅ | 两范围逐halfword packed与现有+新增direct-edge均0；0b20历史登记撤销。 |
| C4 R1值 | slot值等于ROM | ✅ | 249/249 little-endian word相等；switch/callback另行30/30、5/5相等。 |
| C5 R1复用 | NEW前无可复用 | ✅ | 七个新值对全部现有可求值`.equ`无同值；REUSE符号和值全匹配。 |
| C6 R2名 | 形式、唯一、碰撞 | ✅ | 249 slot labels通过regex且唯一；新Function/local/constant/global无正式源碰撞。 |
| C7 R3接通 | LABEL与DATA-ref | ✅ | 七target前态独立核对；33 REF post tuple与26 RENAME pre tuple完整。 |
| C8 R5现名 | PLATE使用现名 | ✅ | 十个完整PLATE及全部EOL无自动旧名；38f8自动名不进入PLATE/EOL。 |
| C9 ASCII | PLATE/EOL纯ASCII | ✅ | 10/10 PLATE、249/249 slot EOL及131c EOL全ASCII；max PLATE=456。 |
| C10 carve/pointer | even/odd值 | ✅ | carve=0；30个mov-pc表word全偶，五槽/四种callback均为Function+1。 |
| C11误名/Function | name与body一致 | ✅ | 0b20语义/APCS、131c local及四个Function body闭合；只3 create+1 rename，5209→5212。 |
| C12 R6证据 | 消费者与置信度 | ✅ | 0b20 caller/callee/global/CID及其他关键槽均给ROM或file:line证据并标high。 |
| C13残留 | 全覆盖与边界 | ✅ | 249槽=原178+closure71；80 ranges/1231/2640、375 edges全覆盖，唯一越界38f8显式冻结并列下一段义务。 |

### 结论: EXPANDED_PASS

前一节五项修改均已闭合：历史Rule-3行已在proposal中撤销并获得无洞R4计划；Function/槽/动作合同
重冻结；PC-relative direct-edge门禁覆盖375条；38f8边界projection具备唯一scope、可解析定义、
不变四字节/listing守卫和下一完整Seg-6义务；恢复prestate后的完整重落地顺序仍受物理备份、fresh
dry/persisted/full-export/export_all/build/byte-identical及失败恢复门禁约束。

本结论只授权root以本小节写入后的新review SHA重新冻结expanded plan/script并重跑独立final dry/root
门禁；不授权复用scope-failure历史receipt，不授权本轮在38f8执行R4/Function/语义命名，也不授权
跳过下一Seg-6低地址内容直接处理尾stub。

## Expanded Reviewer Verdict: F13-Seg-5 = EXPANDED_PASS

## Expanded materialized implementation + dry/probe/restore review

本小节只审查`EXPANDED_PASS` proposal的物化脚本和写前门禁；不改变上一节C1-C13的
`EXPANDED_PASS`。审查中未运行apply/build，未修改Ghidra、proposal、TSV、脚本或正式源码，未
stage/commit。

### 冻结输入与逐字段物化

独立重算得到以下SHA256，均与脚本`INPUT_HASHES`及写前门禁相同：

- `RefineF13Seg5.py`：
  `c33ff11594a2d44e8d46ed2f31aad19d0c8d65184f8774bcab47e45f84a1861f`；
- expanded plan：
  `b88304291a070a70b89da05eb4599b0a15bab32956487a3362726473c142387a`；
- expanded ref-scan：
  `a5677da287f2168237d108e6233ebeef240e0d9d798ee24796c9f7c90c429eac`；
- proposal/review/TSV/edge ledger分别为
  `b045999088ac6e758eb236e9920d26a74941532b7ce208bd6322176244d67317`、
  `98e43b4f5a90576da66f75268a68497d6147565b62113fbc5d71d5b1336f7f76`、
  `ff0425315b47c77c8576776d66abfe01d8415acdb1cda3c3f3bc7ab4d64d4664`、
  `88ac58dc4bc0815933535bbd8252a84d959acb9e4955bc05936ed4563dbf182a`；
- expanded backup manifest：
  `c174454a034b751110a34611470f61d4168c842b1c0ed4a684d999ae7e265eff`。

plan的249个action与TSV按地址、旧名、ROM值、action、target、slot label、reuse、evidence、EOL
逐字段比较为249/249相等；249个ROM little-endian word也逐项相等。物化计数为
EQ190/REF33/RENAME26、141个new pool（含`1950` dataization与`2000`表指针槽）、29个padding
ranges、四组R4 ranges=`49/18/2/11`、三个Function create、一个Function rename、十个PLATE和
250个EOL。proposal中的四个Function body、十个PLATE原文、七个target合同、七个新增定义、四个
GAS alias、一个`131c` local label/EOL均与plan逐项相等；PLATE最大456 bytes，脚本、PLATE和EOL
payload均为ASCII。

### Retry3顺序、R4覆盖和Function状态

对Retry3 PASS脚本快照与当前脚本执行AST逐函数比较，`rename_primary_same_object`、
`normalize_targets_and_cases`、`clear_and_disassemble`、`apply_probe_ranges`、gap-fill、pool、slot、
REF等核心实现均未漂移。当前real apply路径仍精确为：

1. `normalize_targets_and_cases()`，其中`PRENORMALIZE_SWITCH_SLOTS=(080a16d4,)`；
2. `normalize_local_labels()`；
3. `apply_probe_ranges()`；
4. padding、141 pool、249 slots、local EOL、Function和PLATE。

因此`080a2000`被重新dataize前，`080a2004`的派生DEFAULT primary已经转换为批准的USER Symbol；
expanded probe的32地址三态仍为27个DEFAULT ID只在normalize阶段变化，normalize到post-apply的
额外ID变化为0。

没有采用probe自报的Instruction总数：重新以ROM和GNU objdump逐一反汇编80个批准range，80/80
都从`lo`连续走到`hi`，没有undefined、跨界、pool/padding重叠或地址断裂；独立合计为1231
instructions/2640 bytes。四个顶层块的code/pool/padding分区分别为：

| block | code | pool | padding | total | gaps/overlap |
|---|---:|---:|---:|---:|---:|
| 0b20..1338 | 1754 | 284 | 34 | 2072 | 0 |
| 1720..190a | 340 | 140 | 10 | 490 | 0 |
| 1f68..2000 | 134 | 16 | 2 | 152 | 0 |
| 2018..2234 | 412 | 116 | 12 | 540 | 0 |

probe记录的81个动态gap seeds为81/81唯一；逐项均在上述objdump连续Instruction地址集合中，所以
每个seed都是批准range内的真实Thumb指令边界，且没有seed落入pool/padding或越出range。

full expanded probe在事务内实际得到Function总数5212。`080a0b20`精确拥有49-range/1754-byte
body；脚本在创建后设置并复核
`uint tick_equip_card_message_by_id(uint player_id, ushort card_id, ushort unused_row_value)`。
`080a131c`实际为唯一USER_DEFINED local label、没有Function，owner为`080a0b20`，且只有批准的
ASCII EOL。`080a1f68`和`080a24cc`的body size分别为546和28。既有`080a1658`保持Function ID
16936，名称从`check_equip_target_slot_state`改为`tick_equip_display_row_by_type`，body从150扩为
批准的490 bytes。39个冻结既有Function的EOL集合在probe前后没有差异；七个既有PLATE加三个新
Function PLATE组成批准的十个PLATE动作。

### 直接边、rollback和只读证据

重新从ROM半字独立解码全部80 ranges并与edge ledger按`source/op/target/rom_bytes`逐行比较，
375/375相等：89 BL、286 B、226个unique targets；分类计数也与上一节相同。
`080a18ba -> 080a0b20`和`080a187a -> 080a38f8`各精确一行。实际probe中的`080a38f8`前态为
四字节`01207047`、0 Symbol、无Data/Instruction/Function/EOL/PLATE；post态为同四字节、恰一个
primary DEFAULT Label `SUB_080a38f8`，仍无Data/Instruction/Function/EOL/PLATE。该实际观测符合
上一节批准的唯一boundary projection。

证据时序为backup `15:46:06`，首次fresh dry DB before/after `15:56:17/15:56:32`，probe DB
before `15:56:52`，事务内证据 `15:57:06`，probe进程after `15:57:08`，物理restore
`15:57:28`，恢复后fresh read-only dry DB before/after `15:57:35/15:57:50`，最终写前门禁
`16:00:45`。脚本的`expanded_probe`路径在`finally`中无条件
`endTransaction(transaction, False)`；事务内证据明确标记rollback pending且不存在real receipt。

独立重新枚举并哈希当前`.rep`与
`Yu-Gi-Oh WCT 2006.rep.bak-20260905-154603-pre-F13Seg5Expanded`，两边均为15个文件，relative
path/size/SHA256为15/15完全相同。两次fresh dry的DB before/after JSON分别byte-identical；恢复后
当前DB也与backup一致。pre-source snapshot的40个既有正式路径当前为40/40 size/SHA256相同；唯一
存在性变化是该snapshot当时尚不存在、现在按本任务物化的`RefineF13Seg5.py`。不存在expanded
apply receipt、apply-before或persisted-check，staging为空，`output/2343.gba`时间仍为本轮开始前；
因此没有real apply、build或正式source变化。

### 唯一失败项：`080a38f8`合同没有完整固化为脚本门禁

实际probe状态正确不等于脚本已逐字段实现批准合同。当前`projection_state()`已经返回`data`，但
以下三处断言都没有检查`projection['data'] is None`：

- `RefineF13Seg5.py:536-539`的prestate；
- `RefineF13Seg5.py:766-770`的R4 probe post-state；
- `RefineF13Seg5.py:1035-1039`的real/persisted postcheck。

post断言还只核primary的name/source，没有核同址Symbol count恰为1、该Symbol确为primary、类型为
Label且qualified name仍在global namespace。`check_f13_seg5_expanded_preapply.py:77-80`重复了同一
缺口：它没有断言probe中的`data/eol/plate`为空，也没有从`post_capture`核同址唯一Symbol。

因此当前脚本能记录实际probe的正确完整状态，但不能在real apply及fresh persisted check中拒绝
“同址另有alias”或“38f8被定义为Data”的状态。这与proposal第3、488、514、517、520行及上一节
`EXPANDED_PASS`冻结的“仅一个DEFAULT projection，四字节和listing type不变”合同不完全一致。

### 结论: NEEDS_FIX

除`080a38f8`的精确门禁缺口外，expanded物化表、Retry3操作顺序、80/1231/2640/81覆盖、
249/190-33-26动作、四个Function body、APCS、131c local、375条边、probe rollback、15/15物理恢复、
fresh read-only及正式source不变均通过。

#### #1 — boundary projection — 补全listing与唯一Symbol断言

1. 扩展`projection_state()`以返回同址完整Symbol集合或至少`symbol_count`；不得以primary存在替代
   同址唯一性检查。
2. prestate要求`data/instruction/function/eol/plate`全部为`None`、`symbol_count=0`且primary为空。
3. probe、real postcheck和persisted check要求`data/instruction/function/eol/plate`全部为`None`、
   bytes仍为`01207047`、`symbol_count=1`，唯一Symbol必须为global primary DEFAULT Label
   `SUB_080a38f8`；不得在该地址创建USER Symbol、Data或Function。
4. 同步加强`check_f13_seg5_expanded_preapply.py`对事务内probe证据的上述完整断言。保留当前只由
   `080a187a`反汇编产生自动projection的行为，不扩大R4或Seg-6范围。
5. 更新script/gate hashes并冻结本review的新SHA256；随后重新执行expanded full probe、强制rollback、
   当前/backup 15/15物理恢复、fresh read-only dry/DB不变及root最终门禁。仍不得生成real receipt或
   运行build，直至下一轮独立实现复核通过。

## Expanded Implementation Reviewer Verdict: F13-Seg-5 = NEEDS_FIX(1 item)

## Expanded 38f8 projection gate fix review

本小节仅复核上一节唯一失败项的窄修；保留前文C1-C13的`EXPANDED_PASS`及各次retry历史。
审查中未运行apply/build，未修改Ghidra、proposal、TSV、脚本或正式源码，未stage/commit。

### 冻结输入与精确差异

独立重算SHA256如下：修前脚本
`c33ff11594a2d44e8d46ed2f31aad19d0c8d65184f8774bcab47e45f84a1861f`，修后脚本
`199616e18b82931f0303e6b4ac7426a4d0ba1d067f9f420015130f01845dfea3`，修前冻结review
`40e208a843be51236f339879643845a851958fd17a58d5b871ea9298133853c1`，保存的脚本diff
`ef82bd06b9be25606298d40ff6265aa51a4d13c67c4b7a895356a0667643a506`，最终dry/probe-only gate
`93add71d9e6144769dbfc2a3be9e4b02962554f7293eb931adb9892e08585bb9`。proposal、TSV、plan、
ref-scan及edge ledger仍分别为`b045999088ac6e758eb236e9920d26a74941532b7ce208bd6322176244d67317`、
`ff0425315b47c77c8576776d66abfe01d8415acdb1cda3c3f3bc7ab4d64d4664`、
`b88304291a070a70b89da05eb4599b0a15bab32956487a3362726473c142387a`、
`a5677da287f2168237d108e6233ebeef240e0d9d798ee24796c9f7c90c429eac`、
`88ac58dc4bc0815933535bbd8252a84d959acb9e4955bc05936ed4563dbf182a`。

现场重新生成`git diff --no-index`得到5853 bytes，与
`f13-seg5-expanded-projection-fix-script.diff`逐字节相等。AST逐函数比较得到修前/修后56/57个
函数：只新增`verify_projection_contract`，共同函数中只改变`projection_state`、
`verify_prestate`、`verify_probe_state`、`verify_post`；后三者的改变仅为用共享强合同替换原弱断言。
模块级数据唯一实质变化是`INPUT_HASHES`中的review SHA更新。所有normalize、R4/gap-fill、pool、
slot、REF、Function、comment及apply顺序函数均未改变，因此本窄修没有新增Ghidra写动作，也没有
改变38f8以外的行为。

### 38f8完整合同

`RefineF13Seg5.py:341-390`现在采集同址完整Symbol集合、count、primary及global属性，并统一断言
四字节为`01207047`，Data/Instruction/Function/EOL/PLATE均为空：

- pre调用位于`:569`，要求`symbol_count=0`、空集合且primary为空；
- R4/full probe调用位于`:796`，要求同址恰一个global primary DEFAULT Label，name与qualified name
  均为`SUB_080a38f8`，类型为Label，且集合唯一元素与primary逐字段相等；
- real及persisted共同的`verify_post`调用位于`:1061`，使用同一post合同；`check`模式在
  `:1143-1151`读取receipt后调用该函数并再做完整saved-state比较。

辅助门禁`check_f13_seg5_expanded_preapply.py:77-101`也分别核了pre/post的全部空listing/comment字段、
0/1 Symbol、global/primary/DEFAULT/Label/name/qualified-name，以及post capture中同址唯一Symbol。
因此上一节列出的Data、alias、非global Symbol及错误primary漏检路径全部关闭。

没有接受脚本自报：直接解析新的事务内probe JSON，前态为`bytes=01207047`、0 Symbol、上述五类
listing/comment全空；post态四字节及上述空状态不变，恰一个global primary DEFAULT Label
`SUB_080a38f8`。对完整capture逐字段比较，ROM word仍为`0x47702001`，containing code unit、
defined data、instruction、Function、comments、equates及references-from均不变；唯一新增状态是该
Symbol以及`080a187a -> 080a38f8`的DEFAULT unconditional-call reference。probe因而没有把38f8
反汇编、dataize、建Function、加注释或赋USER名。

### dry、rollback、恢复及未漂移计数

证据顺序为首次fresh dry DB before/after `16:19:14/16:19:29`，probe DB before及事务内证据
`16:19:44/16:19:58`，probe进程after `16:20:00`，物理恢复 `16:20:17`，恢复后fresh read-only
dry DB before/after `16:20:24/16:20:39`，final gate `16:20:53`。两次dry日志均为
`STATUS: OK mode=dry FAIL=0`，probe日志为`STATUS: OK mode=expanded_probe FAIL=0`；脚本
`expanded_probe`仍在`finally`中强制`endTransaction(..., False)`。

两组fresh dry的DB before/after JSON分别逐字节相等且共同SHA256为
`9fe61e553033a358f04f96ae050eb0b84cfa2d039448ac3dd6695956d39d9fe9`。独立重枚举当前`.rep`与
`Yu-Gi-Oh WCT 2006.rep.bak-20260905-154603-pre-F13Seg5Expanded`，两边均15文件，relative
path/size/SHA256为15/15完全相同；备份本身也与15行manifest逐项相等。pre-source snapshot中的
40个既存正式路径仍40/40 size/SHA256相等；snapshot当时缺失而现在存在的唯一文件是本任务脚本。
不存在expanded apply receipt、apply-before或persisted-check，staging为空，未发生real apply或
build。

新probe维持249 actions=`EQ190/REF33/RENAME26`、80 ranges、1231 instructions/2640 bytes、
81 gap seeds、375 edges/226 targets、事务内Function总数5212；Retry3 normalize阶段仍只有27个
批准的DEFAULT Symbol ID变化，normalize到post-apply额外变化为0。141 pool、29 padding、
3 Function create、1 Function rename、10 PLATE及250 EOL亦由fresh dry/probe门禁原计数通过。

### 结论: EXPANDED_IMPLEMENTATION_PASS

上一节唯一`080a38f8`门禁缺口已按精确合同闭合，且窄修没有动作漂移；fresh dry、完整probe、强制
rollback、15/15物理恢复和恢复后fresh read-only检查均通过。由于追加本小节会改变review SHA，
现有`93add71d...` gate只能作为本次审查的输入证据；root须冻结下方新review SHA并更新脚本/门禁
哈希，再跑final fresh dry与root门禁后，方可放行real apply。

## Expanded Projection Fix Reviewer Verdict: F13-Seg-5 = EXPANDED_IMPLEMENTATION_PASS

## EXPANDED_IMPLEMENTATION_PASS 正式落地证据 (2026-09-05)

本节记录root明确授权后的Mode B落地，不改变前述review判定、proposal或TSV。落地期间没有stage或commit。

### 冻结输入、备份与source前态

- real apply前重新核对script/proposal/review/TSV/plan/ref-scan/direct-edge ledger SHA256，分别为`32f868a41634f1854da60be8a8e50224497e5d57a12a71a7c9f4ec50b625e154`、`b045999088ac6e758eb236e9920d26a74941532b7ce208bd6322176244d67317`、`191048643145dffc834f8b6ed78330ba857886deddc9a26765bbf2fd678e7477`、`ff0425315b47c77c8576776d66abfe01d8415acdb1cda3c3f3bc7ab4d64d4664`、`b88304291a070a70b89da05eb4599b0a15bab32956487a3362726473c142387a`、`a5677da287f2168237d108e6233ebeef240e0d9d798ee24796c9f7c90c429eac`、`88ac58dc4bc0815933535bbd8252a84d959acb9e4955bc05936ed4563dbf182a`，与授权逐项相同。
- 物理备份`Yu-Gi-Oh WCT 2006.rep.bak-20260905-154603-pre-F13Seg5Expanded`为15文件，source与backup的relative path、size和SHA256为15/15完全相同；此前四份pre-F13Seg5/Retry1/Retry2/Retry3备份均保留。`f13-seg5-expanded-backup.json`状态为`PHYSICAL_EXPANDED_BACKUP_VERIFIED`。
- 正式source snapshot含41个合同路径，其中40个既存路径在写源码前与`pre-f13-seg-5-formal`逐文件size/SHA256相同；唯一基线缺失路径为本次新建的`RefineF13Seg5.py`。恢复脚本的允许集合包含asm12/asm13/asm14、rom.s、两常量文件、CSV及四份inventory；没有放宽到其他正式文件。

### 单事务apply与fresh持久化

- `f13-seg5-expanded-real-apply.log`的PREFLIGHT为249槽=`EQ190/REF33/RENAME26`、R4=4、code ranges=`49+18+2+11`、pool=141、dataization=1、Function create=3、rename=1、PLATE=10、EOL=250、Rule-3=2、edges=375/targets=226、FAIL=0。POSTCHECK为80 ranges且其余计数相同，`STATUS: OK mode=apply FAIL=0`，Ghidra Save成功。
- `f13-seg5-expanded-apply-receipt.json`状态为`APPLIED_TRANSACTION_POSTCHECK_OK`、FAIL=0，Function总数5209 -> 5212；新Function ID分别为`080a0b20=32955`、`080a1f68=32959`、`080a24cc=32960`。本次expanded real apply一次成功，未触发事务rollback或物理恢复；此前coverage/Symbol顺序重试历史及其恢复证据继续保留。
- fresh `-noanalysis -readOnly`的`check`模式再次得到249槽、80 ranges、141 pools、1 dataization、3 create+1 rename、10 PLATE、250 EOL、2 Rule-3、375 edges/226 targets及FAIL=0；receipt完整saved-state逐字段相等。32个target/case/table Symbol身份、四个Function精确body/APCS/incoming、`0x080a131c`local shared epilogue非Function状态均通过。
- `0x080a38f8`保存后仍为bytes `01207047`，同址无Data/Instruction/Function/EOL/PLATE，只有一个global primary DEFAULT Label `SUB_080a38f8`且无alias；其唯一新入口为`0x080a187a`的DEFAULT unconditional-call reference。check前后15DB fingerprint JSON逐字节相同，SHA256均为`6ccab81678200d740982cf85693897946ce33048340c6dc059bcbd1f399573b2`。

### 全量导出、scope和命名同步

- Ghidra完整导出`080000c0..084c7637`成功；从raw中仅移除4条独立mode（ARM=2、THUMB=2），`inject_modes.py`、`split_all_s.py`及`split_all_s.py --check`均exit 0，25个manifest边界全部命中。生成的`asm/all.s` SHA256为`1a55b68ec594468a3e463921177e6ce0ecba146caa86e22b47bd6ba5d9566152`。
- 与source snapshot逐行/逐文件比较，25个模块仅asm12和asm13变化。asm12严格只有`0x08094d30`一行caller从旧1658名变为`tick_equip_display_row_by_type`；asm13仅`[080a0b20,080a1338)`历史闭包、原Seg-5投影及一个`SUB_080a38f8:`边界label变化。`[080a1338,080a1658)`、`[080a27a0,080a38f8)`及38f8原`.byte`起至EOF逐行相同；38f8下一行仍精确为`.byte 0x01, 0x20, 0x70, 0x47`。asm13 SHA256为`29bc339007301208e3877dc7ce5722580a87f5b21a932227083fc0438102abf3`。
- constants仅新增proposal批准的5个`duel_field.inc`定义和2个`ewram.inc`全局，`rom.s`仅新增4个批准Thumb `fn+1` alias；其他23模块及registry与snapshot字节相同。段内仅保留`ROM_INCBIN 0xa1f54, 0x14`与16B Rule-3块；历史2072B incbin、1720/2018块头和其他未批准auto槽均不再残留。
- fresh read-only `ExportFunctionInventory.py`输出total=5212、named=5122、auto=90；DB查询前后15文件完全相同。三项新Function只新增到真实inventory，既有1658仅name及body length `150 -> 490`变化，auto inventory字节不变。通用sync落地前dry只报告1658一项既有非auto分歧；CSV精确只改该行name cell后，apply为noop且post-dry为0 warn。未为0b20/1f68/24cc建立历史评分行，`RenameKnownFunctions.py`无四地址tuple并保持原hash。

### export_all、构建与文档门禁

- `python tools/rom-export/export_all.py`完成49/49；`NOPAUSE=1 build.bat` exit 0，仅输出既有r13 deprecated警告。`output/2343.gba`与`roms/2343.gba`均为33554432B，SHA1均为`9689337d6aac1ce9699ab60aac73fc2cfdccad9b`，Windows `fc /b`报告no differences。
- 活动文档已新增§4.05，把历史`[080a0b20,080a1338)`从§5.1撤销并记录`080a18ba -> 080a0b20`触发R4闭包；Seg-5残余§5.1仅`[080a1dd8,080a1de8)`16B和`[080a1f54,080a1f68)`20B。`0x080a38f8`记录为下一完整Seg-6必须处理的边界stub，Seg-6仍未开始且须低地址向高地址推进。总进度更新为file13 5/10，下一任务Seg-6 `[080a27a0,080a38fc)`。
- 核心落地证据为`f13-seg5-expanded-apply-receipt.json`、`f13-seg5-expanded-persisted-check.json`、`f13-seg5-expanded-production-scope.json`、`f13-seg5-expanded-inventory-check.json`、`f13-seg5-expanded-rom-verify.json`和最终`f13-seg5-expanded-landing-gates.json`。落地结束时没有BLOCKED，没有源码或ROM红线失败，没有stage或commit。

## Expanded Landing Verdict: F13-Seg-5 = LANDED_BYTE_IDENTICAL
