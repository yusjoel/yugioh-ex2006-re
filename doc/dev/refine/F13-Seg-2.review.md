# Refine Review: F13-Seg-2

**当前结论：第一轮正式评审 NEEDS_FIX（1项，1 / 3）。** 424 B 裸块分类、158个槽、常量、CID、引用与59个全文 PLATE 均已独立闭合；唯一问题是通用 callee 的“card array”语义已订正，但两个固定CID wrapper仍保留与其真实委托路径矛盾的 `monster_zone_chain` 正式名。本轮不批准进入ModeB。

## 输入锁定

| 输入 | SHA256 |
| --- | --- |
| `doc/dev/refine/F13-Seg-2.proposal.md` | `9528df517e41f9041e8b4df5e9719ec7ec352c5f8b3dd2e10d7f56cb4bbd1d8a` |
| `asm/13_equip_placement.s` | `3218ebbbd6743fab7ebf47d96c7ad61c08fd64972dbd9fc5ea8fa62371681bd7` |
| `f13-seg2-plan.json` | `fb039f6e5d2b33deddbbc1ca33fb657d6e2934bd5a91514edcc1c11292b99e66` |
| `f13-seg2-plates.json` | `a5d6e97c89c0599bbe509714bdc42d9be98099293f70c3ce8e9fd0648da36bf7` |
| `f13-seg2-selfcheck.json` | `9eb95f175847ddbcb7c2a9d641443f518509b3e26612cc08a54838c02983685d` |
| `roms/2343.gba` | `f405c620da05a817a5d63f45a4707b914260fb5802fe519b1e31bf050ba8f524` |

日期：2026-09-01；reviewer：Sol / xhigh；正式轮次：1 / 3。reviewer仅写本review及运行目录中的 `f13-seg2-review-*` 证据；未改proposal、plan、正式源码、constants、Ghidra、进度或全局文档，未build、stage、commit，也未分析Seg-3。executor与root的自检仅用于定位输入，结论来自实际asm、ROM、constants、消费者和导出器的独立复核。

## P0

**PASS。** 提案存在且非空，含完整动作、反汇编、引用、函数改名、PLATE和落地守卫；`[降级]`、`[跳过]`、`[待补全]`及零容忍用语扫描无命中。下述正式名遗漏属于NEEDS_FIX，不是P0_FAILED。

## 核验（C1-C13）

| # | 检查 | 结果 | 独立证据与结论 |
| --- | --- | --- | --- |
| C1 | Rule1：地址序与路线图 | ✅ | 活动文档§五的Seg-2恰为 `[0x0809e6f4,0x0809f744)`、4176 B；Seg-1已闭合，下一段从`0x0809f744`开始。本评审没有预析Seg-3。音频payload与段外函数指针只用于判定本段raw/rename依赖，不扩展后段函数范围。 |
| C2 | Rule2：裸块归宿 | ✅ | 段内唯一裸块 `[0x0809e74c,0x0809e8f4)` 共424 B，独立分成145条指令/316 B、25个literal word/100 B、4处2 B零对齐/8 B，合计424 B。proposal全部归入R4 disasm并保留同一dispatcher Function；没有静默保留的 `ROM_INCBIN/.byte`。 |
| C3 | Rule3：ref-scan | ✅ | 本段§5.1=0。reviewer对块内212个halfword候选逐个在整ROM搜索raw及THUMB\|1：raw=9、odd=0；8项是e72c表的真实偶地址case，额外`0809e812`仅在`081feb5e`出现。该位置落在音频表index37 payload `[081fb9dc,081ff400)` 内，窗口为有符号样本字节且非4 B对齐，不是代码指针。 |
| C4 | R1：槽值 | ✅ | 158动作=119 EQ+20 REF+19 RENAME。每个槽均从ROM读取小端u32并与proposal/plan比较；126个原自动word、7个匿名table word、25个新pool word完整对应。全段154条真实Thumb literal LDR均按PC对齐公式解码，动作uses无额外或漏项。 |
| C5 | R1：常量复用 | ✅ | 独立解析22个constants文件的5998条 `.equ`，5998个名称均唯一。48个REUSE的名称/值/文件/行全对；24个NEW均无同名。仅两个NEW值有既有同值：`0x1cf8`的旧定义以`gDuelFieldSlots`为基址，本项以LP为基址；`0xffff`的8个旧定义均不是pair-missing返回哨兵，域分离有消费者支撑。 |
| C6 | R2：槽名、目标对象与碰撞 | ✅ | 158槽名均匹配 `^[a-z][a-z0-9_]+$` 且唯一；合并table/case目标后166个静态ROM label名唯一，当前asm/data无同名定义。8个case前态均为单个DEFAULT动态label，不存在F12 closure式双对象冲突；新建USER primary label的计划可执行。两个已列新函数名也无全局碰撞。 |
| C7 | R3：引用与导出接通 | ✅ | e728及8项table word的既有DATA/DEFAULT引用按同operand/target精确重建为USER_DEFINED；其他引用保留。19个RENAME中e71c引用为USER_DEFINED，其余18个为DEFAULT，均明确原样保留。另11个无outgoing的RAM指针槽新增DATA/USER_DEFINED。25个新pool前态为逐字节undefined、无Instruction/Data/symbol/outgoing，计划建`/dword`并由新LDR生成READ。`ExportRangeToGas.py:508-584`可经USER ROM LABEL/RAM LABEL或equate fallback输出全部表达式；本段没有依赖ROM FUNCTION或`+1`的REF槽。 |
| C8 | R5：PLATE使用现名 | ✅ | 59个新PLATE正文无 `FUN_/DAT_/DWORD_/PTR_DAT_/UNK_`，且f158的两个wrapper PLATE都引用新callee名 `scan_player_card_array_for_equip_activation_by_cid`。正式Function名遗漏单列C11，不把正文检查混作命名通过。 |
| C9 | ASCII与长度 | ✅ | 独立检查59 PLATE、158槽EOL、8 case EOL、24新constant EOL，共249段拟写Ghidra文本，全部纯ASCII。PLATE最大469字符，均不超过500。 |
| C10 | carve / Thumb指针 | ✅ | 本段carve=0；8个MOV-pc table word均保持偶地址，不加1。两项原计划FUNC_RENAME的整ROM依赖正确：ec34仅odd值`0809ec35`命中`09e477c0`，f158无raw/odd，均保留原字节。额外wrapper遗漏带来的两项odd依赖列入修改清单，不改值、不carve。 |
| C11 | 函数误名与身份 | ❌ | f158真实扫描 `gP1HandSlotArray + player*0x868 + index*4`，proposal将其改为card-array名称正确；但f1fc/f20c只是加载固定CID并BL到f158，正式名仍写 `scan_monster_zone_chain_*`。这两个12 B wrapper没有任何monster-zone遍历，名称与直接callee及新PLATE矛盾。详见修改清单#1。 |
| C12 | R6：消费者、CID与rename依赖 | ❌ | 59个函数的输入/返回、145条新指令、13个BL、21个非call branch和26个块内literal READ均已从机器码复核；其余语义通过。59个唯一CID按data.md逻辑CID列、ROM逆表、passcode解密和全部5170条stats记录交叉验证：56映射、11cf/1338/1367三项无映射；后两项NEW保持中性名。失败点仅为上述直接消费者结论没有传播到两个wrapper正式名及其依赖集合。 |
| C13 | 全覆盖与残留 | ✅ | 原自动槽126=103 DAT+3 DWORD+20 PTR；加7个匿名table word和25个新pool后恰为158动作，地址唯一。静态投影含1668条指令、158个word、1826单元，重建4176 B并逐字节等于ROM，SHA256=`46e20aba25cfd3417fcd388f095b0eb9fcd79b028c2786c6c72be69798bde64d`。预计段内自动word残留0、裸块0。wrapper改名遗漏不改变槽覆盖。 |

## R1-R9

| 项 | 结果 | 结论 |
| --- | --- | --- |
| R1 常量符号化 | ✅ | 119 EQ逐值正确，24 NEW/48 REUSE全量查重闭合。 |
| R2 标签可读化 | ✅ | 166个ROM label名合法、唯一、无碰撞；槽语义与消费者一致。 |
| R3 按名引用 | ✅ | 20 REF的目标label、DATA ref source/operand/primary和exporter路径完整。 |
| R4 误标数据反汇编 | ✅ | 424 B精确分区、控制流、pool、padding和Function body union完整。 |
| R5 注释订正 | ✅ | 59个全文PLATE和全部EOL的事实、现名、ASCII与长度通过。 |
| R6 先读消费者再命名 | ❌ | f158消费者结论正确，但两个直接wrapper的正式名未同步。 |
| R7 数据carve | ✅ | 无需carve；偶地址switch与段外保值项边界明确。 |
| R8 目视核对 | ✅ | 本段没有新增图形资产；音频假命中由真实表、header、payload边界及signed-byte消费者闭合。 |
| R9 byte-identical合同 | ✅ | 提案包含备份、dry、精确前后态、export/build/SHA1/持久化守卫；本轮没有声称已执行落地或build。 |

## 独立反汇编、ref-scan与Function身份

从8个真实case根沿Thumb控制流遍历得到145条不重叠指令、316 B。25个literal目标均唯一，合计100 B；四个padding为`e75e/e7ae/e7d2/e8ae`各`00 00`。Ghidra前态中25个pool的每个基址均为undefined1、无DefinedData/Instruction/symbol/outgoing；8个padding字节也均为undefined1、值0、无引用。不能把padding建成Data2。

dispatcher `0809e6f4` 保持Function ID16934。原body是`[[0809e6f4,0809e71b] [0809e8f4,0809e901]]`、54 B、27条指令；新body为proposal所列12个half-open range、370 B，只并入case代码，不包含pool/padding。`mov pc,r0@0809e71a`原 `flows=[]`、`references_from=[]`、`fallthrough=None`，保持空，不人工造computed flow。13个BL均从双halfword编码求得真实callee，21个branch目标均落在同一共享frame或原返回尾；不建立case Function，Function总数仍5209。

raw额外命中`081feb5e`的上下文由ROM真实音频表闭合：`081d7ea0[37]=081fb9d0`、下一项`[38]=081ff400`，header为`0x0c2d,0x3a24,0xffffffff`，payload从base+12开始。命中偏移`0x3182`，四字节解释为signed samples `[18,-24,9,8]`；实际混音消费者使用`LDRSB`。因此保留音频字节，不建ref/label/function。

## 值、CID与语义

全段154条literal LDR中，块外128条与块内26条全部以`((PC+4)&~3)+imm8*4`重新解码。158个word的ROM值、用途、拟导出表达式均一一对应。59个PLATE的旧全文/hash/Function ID/body/incoming/EOL前态与真实快照相符；新正文覆盖所有59入口，只有dispatcher body变化。

常量全量扫描确认两个同值域例外：

- `EQUIP_ACTIVATION_SAVED_PHASE_OFF=0x1cf8` 从`gP1LifePoints`取保存phase；现有`EQUIP_CHAIN_STEP_FROM_FIELD_OFF`从`gDuelFieldSlots`表达另一个字段，不能复用旧名。
- `EQUIP_CHAIN_PAIR_MISSING=0xffff`是`find_equip_chain_pair_across_field`返回的player/slot pair缺失哨兵；现有8个同值常量分别属于empty card、mask、cap、guard、OAM或score域。

CID复核没有按反序列行号或SO列匹配。59个值逐一读取data.md第4列逻辑CID、`cards-ids-array.s`与ROM逆表、`card-passcodes.s`及ROM LCG解密、`card-stats.s`和ROM全部5170条22 B记录。56个mapped CID的名称/password/主副记录一致；`11cf/1338/1367`逆表均为`ffff`且5170条记录零命中。24个NEW中的两个未分配CID使用 `EQUIP_ACTIVATION_UNMAPPED_CID_*`，没有附会卡名。

两个已列改名入口本身准确：

- `0809ec34`用LP+0x14计数，按4 B读取player card-word array，以`0x00201fff`比较Marie CID，逐匹配调用activation；不是20 B monster-slot遍历。
- `0809f158`先做zone11 chain CID guard，随后同样按4 B扫描player card array，以low13 CID和bit21过滤；命中后调用activation。正式名突出它实际循环的数据结构。

这也直接证明遗漏的两个wrapper必须同步：

| 地址 / ID | 当前正式名 | 真实body与依赖 |
| --- | --- | --- |
| `0809f1fc` / 6864 | `scan_monster_zone_chain_for_equip_activation_sinister_serpent` | 12 B：加载CID`0x1181`并BL到f158；整ROMeven=0，odd=`0809f1fd`仅命中`09e4788c`。 |
| `0809f20c` / 6865 | `scan_monster_zone_chain_for_equip_activation_treeborn_frog` | 12 B：加载CID`0x19cb`并BL到f158；整ROMeven=0，odd=`0809f20d`仅命中`09e47890`。 |

两者Ghidra incoming当前均为空；实际调度通过段外odd函数指针表。改名只改变目标primary Function导航名，不能改`09e4788c/90`的raw值、Data/ref本体或host incbin，也不在本段追加carve。

## C6/C7落地条件

1. 9个table相关既有DEFAULT引用必须先精确删除同operand0/target引用，再重建USER_DEFINED；`addMemoryReference`合并同目标不会自动提升source。8个case均新建唯一USER primary LABEL，不新增同址alias。
2. 19个RENAME引用保持本体不变：e71c为DATA/USER_DEFINED，其他18个为DATA/DEFAULT，全部operand0/primary。不能由目标`gP1LifePoints`的USER source推断引用source。
3. 25个新pool建`/dword` length4；对应新READ由反汇编产生。四处padding仍导出`.zero 2`并保持undefined1，不建Data/label/ref。
4. RAM只复用既有USER labels `gP1LifePoints`、`gDuelFieldSlots`、`gP1HandSlotArray`，保留原Data4与incoming/outgoing，不读取未初始化RAM。
5. e72c及8项case目标是ROM LABEL而非FUNCTION，符合exporter的ROM限制；EQ走equate fallback。表项保持偶地址，MOV-pc沿当前Thumb状态执行。
6. 原proposal的两个rename需按现有合同保留Function ID/body/prototype/incoming/EOL。新增两个wrapper rename也须采用同样的对象身份守卫，并保留两项段外odd raw依赖。
7. 当前CSV四个相关行都已是旧正式名，`proposed_name/score`为空；`sync_ghidra_names_to_proposals.py`对已具名分歧只warn。落地须真实导出4个inventory文件，用`--dry-run`审计后按address仅修改四个CSV `name`单元格，不能依赖全量sync自动写入。

## 修改清单

### #1 — C11/C12/R6 — 两个固定CID wrapper也必须改为card-array正式名

**正确名称：**

| 地址 | 旧名 | 新名 |
| --- | --- | --- |
| `0x0809f1fc` | `scan_monster_zone_chain_for_equip_activation_sinister_serpent` | `scan_player_card_array_for_equip_activation_sinister_serpent` |
| `0x0809f20c` | `scan_monster_zone_chain_for_equip_activation_treeborn_frog` | `scan_player_card_array_for_equip_activation_treeborn_frog` |

两个新名均无当前asm/data/Function碰撞，并与已审核PLATE及直接callee一致。ModeA须完成以下五组同步，且不得改变158槽、424 B disasm或59个PLATE正文语义：

1. proposal的段测绘、FUNC_RENAME表、rename依赖、生产命中清单、C11/C13与最终计数改为**4 FUNC_RENAME**。f1fc/f20c原“registry plate-only”合同改成“name+plate”；四个相关registry tuple均为name+plate。
2. 同步当前派生文件 `f13-seg2-plan.json`、`f13-seg2-plates.json`、`f13-seg2-map.json`、`f13-module-map.json`、`f13-seg2-rename-dependencies.json`、`f13-seg2-static-projection.s`及selfcheck中所有计划输出名称、计数和hash。plate JSON的`name`改为新正式名，`expected_old_name`及真实旧全文/body/hash守卫保留。不得修改`*-round1`、`f13-seg2-round1-evidence/`、baseline或备份。
3. ModeB的asm动作增加两个Function定义名替换，并更新本批受控PLATE/同族文本中的旧wrapper名；两条BL仍只从f1fc/f20c指向f158，新名字不改变机器码。`RenameKnownFunctions.py`中这两个tuple从plate-only变为name+plate；其他tuple不动。
4. `doc/dev/naming-proposals.csv`按`0809f1fc/0809f20c`再修改两个`name`单元格，连同原ec34/f158共4行；保留`proposed_name/score/tags`。真实运行`ExportFunctionInventory.py`刷新4个inventory文件，再用sync dry-run审计限定差异。
5. 增加段外保值守卫：`09e4788c`必须仍为`0809f1fd`，`09e47890`仍为`0809f20d`；不carve、不重建其引用、不改DataType或host切割。后态只允许target primary的Function名字随改名导航变化。保持ID6864/6865、各12 B body、prototype、原incoming/EOL/PLATE前态和全局Function总数5209。

修订后应以第一轮冻结输入做exact diff：除上述名称、依赖合同、计数、派生hash与受控文本外，119EQ/20REF/19RENAME、24NEW/48REUSE、59PLATE正文、158槽EOL、8 case EOL、145指令/25pool/4padding、全部refs/Function前态及无carve/无§5.1结论必须保持。

## reviewer证据文件

均位于 `output/refine-run-20260831-194634/`：

| 文件 | SHA256 | 内容 |
| --- | --- | --- |
| `f13-seg2-review-block-refscan.json` | `91f4c0cb7ab909ef12877d6795eebddd0cb5dbccbc442b10696a1fd0f0207eb1` | 145指令、25pool、4padding、13CALL/21branch、整ROM raw/odd扫描及音频命中闭合。 |
| `f13-seg2-review-actions-plates.json` | `cb8f2b3a0b18483a3c9a176635dd0bbacd973a7c1f61c07c27d48cbbbfd4d0ac` | 158动作/154 literal LDR、59Function/PLATE前态、dispatcher、4176 B静态投影。 |
| `f13-seg2-review-constants.json` | `2e79e74878b9aa575195c5e91461ab45c9f2b592491ec8522a643b52c7d8a977` | 22文件/5998 equates、24NEW/48REUSE及全部同值集合。 |
| `f13-seg2-review-cids.json` | `f08e8d0488d94c5666808b45cd26504cb0930ca4b2b70b18f6d7ba3eec50f4f1` | 59CID的逻辑表、逆表、passcode、stats主副记录与ROM实读。 |
| `f13-seg2-review-cardstats-full.json` | `ea956139659f7ae9001241488faba776e2ae80dac91060bf42eccb6d26902842` | 5170条ROM stats对59CID的完整索引扫描，三项unmapped均零命中。 |
| `f13-seg2-review-ghidra-block-prestate.json` | `ece1db81f423360285dce44433593aae948e4a99cb1c177ba6fad2c37f988042` | 25pool和8padding字节的DefinedData/Instruction/ref前态。 |
| `f13-seg2-review-names-comments.json` | `7cb874fbf89a242de84c3948d76384118da1c5ea6f2c1ee243e85d5435a63123` | 166标签碰撞、249段ASCII文本、59PLATE长度/自动名扫描。 |
| `f13-seg2-review-wrapper-misnames.json` | `fec912f8b66ed2b73417f1c9ae2a00598afe3c5db394e722d71b98bea3812717` | 两个遗漏wrapper的ID/body、建议名碰撞、生产命中及odd raw依赖。 |

## 状态: NEEDS_FIX

完整修订清单为1项。除两个wrapper正式名及其精确同步合同外，没有其他修订项；当前锁定输入不得进入ModeB。修订后进行第二轮正式复审并保留本轮原文和证据。

## Reviewer Verdict: F13-Seg-2 = NEEDS_FIX(1 item)

## 第二轮正式复审

- 日期：2026-09-01；reviewer：Sol / xhigh；正式轮次：2 / 3。
- **结论：PASS。** 首轮唯一#1已按限定范围完整修正，无新增修订项。
- 首轮review冻结为`f13-seg2-review-round1.md`，SHA256=`b9c749abf464db7d71c38d2389c553f54cc743ea0943b75334894537d8b92f10`；上文首轮问题与NEEDS_FIX结论保持原文。
- 本轮仅追加当前review并写`f13-seg2-review-round2-diff.json`。未执行ModeA脚本、headless、Ghidra写入、正式源码修改、build、stage或commit，也未分析Seg-3。

### 第二轮输入锁定

| 输入 | SHA256 |
| --- | --- |
| `doc/dev/refine/F13-Seg-2.proposal.md` | `60370c445976ffe021413cdea6410e9bce8e9ab134613e4a91dd193bfb03b8b4` |
| `f13-seg2-plan.json` | `b54987a1ad0cc564e5e6bfa3693b8e435d5700ace3e38f4d1facb7f5b1b4fd0a` |
| `f13-seg2-plates.json` | `2b1709da950ac59407c9e407869202f74e1825af130619ab50d7747299ca1d44` |
| `f13-seg2-selfcheck.json` | `aea62c60ee87219d8ff1bdaa9cdcbcf21ee086893791cec2925cf955e123531a` |
| `asm/13_equip_placement.s` | `3218ebbbd6743fab7ebf47d96c7ad61c08fd64972dbd9fc5ea8fa62371681bd7`（未变） |

四份round2冻结文件与当前输入逐字节一致。proposal、plan、plates、selfcheck和asm在复审结束前重新计算hash，均为上表值。

### 首轮修订项闭合

**#1已解决。** proposal现为4个FUNC_RENAME，新增：

| 地址 / ID | 新正式名 | 保留身份 |
| --- | --- | --- |
| `0809f1fc` / 6864 | `scan_player_card_array_for_equip_activation_sinister_serpent` | body `[[0809f1fc,0809f207]]`、12 B、SHA256 `48bb12e69322b3c84dee494d32dfb0902cd52a367f04f7c8571662ad796c26b5`、incoming空 |
| `0809f20c` / 6865 | `scan_player_card_array_for_equip_activation_treeborn_frog` | body `[[0809f20c,0809f217]]`、12 B、SHA256 `17a843da7e94c17f11ad2c106a87ed9b0b071a5a7bed6decdd7a76b177c03cdb`、incoming空 |

两个新名均符合形式、无全局asm/data碰撞，并与各自“固定CID后普通BL到f158”的真实body、新PLATE及callee语义一致。原ec34/f158两条rename对象逐字段不变；四个Function的ID、body、body size、incoming和ROM body hash均与只读前态相符。

三处段外odd word已分别按真实状态写入合同并独立复核：

| 地址 | ROM word / 全ROM命中 | 前态与后态合同 |
| --- | --- | --- |
| `09e477c0` | `0809ec35`；even=0、odd=1 | 已有`/undefined *` length4及operand0 DATA/DEFAULT/primary引用；完整保留引用本体，只允许target-primary显示名随ec34改名。 |
| `09e4788c` | `0809f1fd`；even=0、odd=1 | 当前DataDB length1、DefinedData=None、symbol/ref均空；后态仍保持无Data/symbol/ref。 |
| `09e47890` | `0809f20d`；even=0、odd=1 | 当前DataDB length1、DefinedData=None、symbol/ref均空；后态仍保持无Data/symbol/ref。 |

三项均明确不carve、不改raw值或host边界。新版没有把`09e4788c/90`误写成“保留既有ref”。

### 独立exact diff

reviewer未采用ModeA报告的PASS字段。以首轮冻结输入独立递归比较后得到：

- plan差异只有14条路径：新增`function_rename_count=4`、`function_renames`追加两项、两个plate owner name、三项odd-pointer guard及相应rename source policy。首轮前两个rename对象完整相等。
- `actions/counts/new_constants/reused_constants/new_globals/case_labels/extra_eols/disasm/carve/section_5_1/raw_reference_summary/control_evidence`均深度相等。因此158 actions、119EQ/20REF/19RENAME、24NEW/48REUSE、424 B R4、无carve/无§5.1完全未变。
- plates JSON仅`[40].name`与`[41].name`改变；59个`new_text`逐字相等，全部旧全文、hash、body、incoming和EOL守卫保留。
- seg2 map与module map各仅两个Function name及其两个label name改变；rename-dependencies保持原两项为前缀并仅追加两个wrapper。
- static projection逆替换两个新定义label后与首轮文件逐字节相等；当前投影四个旧正式Function定义名均为0，不改变4176 B字节投影。
- proposal文本的10组差异均属于首轮#1：计数、两rename行、四函数/odd合同、生产依赖、PLATE标题及落地守卫，没有夹带槽、常量、正文语义或后段修改。

当前CSV恰有四个address对应旧正式名，四行`proposed_name/score`均空；当前registry的1515个FUN tuple中四个目标key各恰1项且旧name/plate齐全。`temp/ghidra-functions.csv`共有5209行，四函数当前name正确匹配旧前态，dispatcher当前length=54；其余三个真实inventory文件存在，summary为5209 total / 5119 named / 90 auto。proposal正确要求ModeB保存后真实导出四个inventory文件，dispatcher length/body元数据改54→370，registry仅四个tuple name+plate，CSV仅四个name单元格；sync对已具名分歧只warn，不能代替按address限定更新。

### ModeA selfcheck声明审计

新版selfcheck保留原80项并明确分为13项本轮实际重跑、67项按未变输入hash复用；两组不重叠且并集为80，`errors=[]`。reviewer逐项核对其`verification`标记和`executed/reused_evidence`清单：

- 13项确为本轮可从当前proposal/plan/plates/projection/ROM重新执行的rename与字节检查，包括四rename、raw/call证据、新名碰撞、投影旧名清零和完整计数。
- 67项均属于首轮已通过且输入未变的机械测绘、158槽、常量、CID、R4、引用、59旧PLATE与投影检查。selfcheck记录的16份复用源文件与round1冻结manifest三方hash完全一致。
- selfcheck明确`headless/build/stage/commit=false`，没有把未执行操作写成重跑通过。

该声明与实际执行边界一致。reviewer另行重算上述四Function body、三odd word、CSV/registry/inventory、plan/plates/maps/dependencies/projection差异，结论相同。

### 第二轮P0与C1-C13

**P0：PASS。** 本版提案存在、完整，无禁用标记或零容忍用语。

| # | 结果 | 第二轮依据 |
| --- | --- | --- |
| C1 | ✅ | 范围、地址序及Seg-3边界未变；改名依赖仅为本段Function的段外raw保值。 |
| C2 | ✅ | 唯一424 B裸块分类及完整disasm计划深度相等，无静默保留。 |
| C3 | ✅ | ROM及refscan输入hash未变，复用首轮自主212候选raw/odd扫描；§5.1仍0。新增三odd项属于rename保值证据，不改块分类。 |
| C4 | ✅ | 158动作完整相等；当前ROM/asm hash未变，119个EQ值与全部word投影仍逐字节正确。 |
| C5 | ✅ | 24NEW/48REUSE对象及22个constants源hash未变，复用首轮5998定义全量查重。 |
| C6 | ✅ | 两个新增Function名无碰撞；166个槽/目标label对象与命名不变。 |
| C7 | ✅ | 20REF、19RENAME及全部目标/引用计划未变；三odd word按各自真实Data/ref前态精确区分。 |
| C8 | ✅ | 59 PLATE正文完全不变；两个owner改为card-array新名，正文内部callee引用一致，无旧自动名。 |
| C9 | ✅ | 59正文不变，仍全ASCII、最大469；全部EOL不变。 |
| C10 | ✅ | 8个switch偶地址合同不变；三rename odd word均保持THUMB\|1原值且不carve。 |
| C11 | ✅ | 首轮遗漏的两个wrapper现已纳入FUNC_RENAME；四个新名均与真实body/global/callee一致。 |
| C12 | ✅ | wrapper消费者结论已传播到proposal、plan、plates owner、maps、projection和生产同步合同；CID与其余语义输入未变。 |
| C13 | ✅ | 158槽/R4/投影覆盖不变，四个旧正式名的计划生产范围清零合同完整；expected-old与冻结历史明确保留。 |

R1-R9全部通过：本轮补齐R6的wrapper正式名传播；R1-R5、R7-R9经首轮自主证据hash和本轮不变字段审计继续成立。精确计数为**59 Function、158槽=119EQ+20REF+19RENAME、4FUNC_RENAME、59PLATE、158槽EOL+8case EOL、24NEW/48REUSE、1个424 B disasm块=145指令/25pool/4padding、0carve/0§5.1**。

### 第二轮reviewer证据

`output/refine-run-20260831-194634/f13-seg2-review-round2-diff.json`，SHA256=`f08eb251c16b9e0133e61bd2aa9de2105ecb7f08efb6ea927595e953de29e145`。文件记录输入hash、14条plan差异路径、两条plate差异、map/dependency/projection逆变换、四Function ROM body、三odd前态、CSV/registry/inventory、selfcheck 13/67分组及零错误。

本次PASS仅批准锁定hash的proposal进入ModeB。落地仍须执行首轮和本轮全部C6/C7/R9守卫、真实inventory/export/build、byte-identical、持久化和正式生产范围旧名清零检查；不得据此省略三处odd word的不同前态合同。

## 状态: PASS

第二轮修订清单为空；首轮唯一问题已解决，无新增阻塞。

## Reviewer Verdict: F13-Seg-2 = PASS
