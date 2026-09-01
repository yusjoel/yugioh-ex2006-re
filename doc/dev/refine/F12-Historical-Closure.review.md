# Refine Review: F12-Historical-Closure

## 当前状态: PASS（第二轮正式复审）

2026-09-01，Sol + xhigh。首轮唯一问题 **#1 C6/C7的五个子项均已闭合**：08095554改为仅将既有global USER_DEFINED LABEL id31014设为primary；保留id4244的对象、scoped名字、namespace与ANALYSIS来源，仅取消其primary。无需重命名、创建或删除标签，原95550引用不重建。第二轮无新增修改项。

这是一份提案PASS，尚未落地。Mode B必须先通过完整dry守卫，再执行保存/重开只读检查、标准导出、byte-identical及模块验收；本review未调用Ghidra或build，未改正式源码/DB/进度，未stage/commit。第一轮原文保留在后半部分，旧NEEDS_FIX仅描述已修的旧输入。

## 第二轮输入hash

| 输入 | SHA256 |
|---|---|
| 当前proposal | `74f49b4e0cddffe0a66dd2c0a073fe28c555a6d60d89c979bb9796aa58a5ae11` |
| 当前closure-plan.json | `e1b40e449d4b18b396a2c7c549ad2cbf21aff5490659a96d73763d97f0f5d816` |
| closure-plates.json（未变） | `9022db01ec21fd82370e3d21c9f3544ca3a25e851fca968b025c7b82e264bf89` |
| 当前closure-selfcheck.json | `a0ee36521ac578f3d03f1eb913e46e103dfa6ff8b33d99d088f53b3b75324d20` |
| asm12基线（未变） | `ac38c3b9b8068ba46ad0b070a4f099c1aa66691bdcfca33af06455f43467ad8f` |
| 冻结首轮proposal | `8407798be1cb67e3aa8b6f31a2ed016411df8e7e49ba27e482cb6d34979881e8` |
| 冻结首轮review | `77c5b5e392dc8703ff71196ddade1a5407ad93a04501b4b3320595c291f3122f` |

当前ROM SHA1仍为`9689337d6aac1ce9699ab60aac73fc2cfdccad9b`。当前导出器SHA256仍为`a46f8efae54994e58f5b067a34f16f7fe751df46b155b67fd0449e6c53db9fdb`。独立重新计算50个正式文件hash（25模块、22constants、rom.s/includes/CSV）均与写前记录一致。未变ROM/asm/6002常量/消费者/卡表/覆盖结论沿用首轮真实核验，不宣称本轮重跑全量分支/ref-scan。

## 第二轮独立差异核查与#1闭合

本轮自行读取冻结首轮和当前文件，逐行、逐JSON键比较，没有采用Mode A自检布尔值作为证明。共 **10个文本修改块**（1行上下文合并显示为9个diff hunk），均属于95554目标动作、完整守卫、导出/复用/范围说明与修订记录。

计划的旧字段仅`slots[6].target_symbol_id`由4244变31014；新增`target_action`、`target_guard`。删除这两个新增键并还原该id后，**整个plan与首轮对象深度相等**。全部proposal代码块相等、19plates文件逐字节相等；8槽所有原字段（除目标id）、19PLATE原文和旧hash、8EOL、DISASM/Function body合同、4块§5.1及全部计数均未变化。selfcheck仅更换proposal/plan hash及新增mode_a_revision，明确先前静态投影未重跑。

| 首轮子项 | 结果 | 新提案/计划的独立闭合证据 |
|---|---|---|
| #1.1 精确复用两个既有对象 | ✅ | proposal:89、98-100、106；target_action唯一目标写调用为`symbol_id_31014.setPrimary()`，receiver=31014、arguments为空。禁止setName/setNamespace/setSource/createLabel/delete/merge；两ID保持。 |
| #1.2 完整前态/对象保留 | ✅ | proposal:95-104；target_expected_before与真实root-closure-switch-before.json完整对象相等；双LABEL恰2个，地址/namespace显式守卫。95550前态所有真实状态字段相等，32表项及30case对象逐项与真实快照相等。 |
| #1.3 最小后态/按名导出 | ✅ | target_expected_after由真实前态独立复制后仅反转两个primary即可完全复现。95550的后态仅原审定EOL与目标导航元数据变更；引用本体六字段全不变。要求正确完整GAS word，拒绝裸值/短名回退。 |
| #1.4 全文/派生同步 | ✅ | REF与导出段:89-106、来源:333/367、guard:386、范围:392均已去除旧id4244规范化执行要求，改为id31014提升；旧动作仅作为已被替代的错误记录。plan/selfcheck引用hash均与当前真实文件匹配。 |
| #1.5 不扩修改范围 | ✅ | 除前述三个JSON键差异，plan整体还原等于首轮；全部旧文本代码块/19plates/8EOL、8槽地址值与分类、DISASM和四块登记相等。NEW/REUSE等计数不变。 |

目标08095554的严格终态为：id31014仍是`switchD_0809554c__switchdataD_08095554`、global、LABEL/USER_DEFINED，primary=true；id4244仍是`switchdataD_08095554`、namespace `switchD_0809554c`、LABEL/ANALYSIS，primary=false。两者ID/name/qualified_name/namespace/type/source不变，仅两布尔值对调。该动作符合首轮已核本机`CodeSymbol.java:136-160`；不存在原重命名碰撞。

引用守卫正确区分 **引用本体** 与 **目标导航信息**：

- 95550→95554原operand0 DATA/USER_DEFINED/primary的from/to/operand/type/source/primary完全保留；快照`target_primary`随目标主标签从id4244变为id31014，是导航信息更新，不是重建引用。
- 9564c→9565c原operand1 READ/DEFAULT/primary六字段也保持。其target_primary按首轮已批准的9565c池改名操作成为`gsprattrb_9565c`/USER_DEFINED；新合同没有增加第二次改名或重建READ引用。动态DEFAULT池标签转成USER标签后的实际ID必须匹配该原定操作产生的主标签，不错误固定旧动态ID。
- 其余32表项/30case的target_primary导航也逐字保持；目标base两primary之外，不允许改case对象、namespace/source、数据定义或表值。32个ROM u32本轮再次读取，全部偶地址且仍为30个不同目标。

导出路径沿用首轮实际函数探针：`resolve_word_symbol`选新的primary USER LABEL后返回全名；定义端`_pick_best_symbol_name`的结果在primary切换前后相同，`emit_label_if_any_or_forced`按地址只输出一次。保存两个现存Symbol不会产生重复GAS定义。无新equate、无callback+1改写、无需改exporter。

## 第二轮 P0 / C1-C13 完整结论

P0 ✅：提案完整，无中止标记或禁用词。当前范围及计数为 **38228B；8槽=6RENAME+2REF+0EQ；19完整PLATE；8EOL；DISASM1块8B/3指令；NEW0/6REUSE；FUNC_RENAME0/carve0/新增§5.1=0**。

| # | 检查 | 结果 | 本轮依据 |
|---|---|---|---|
| C1 | 地址序/授权范围 | ✅ | 用户授权历史补漏不变；操作顺序/地址和路线图合同未变，无模块13分析。 |
| C2 | 所有裸数据处理 | ✅ | 原唯一8B.byte仍DISASM；原4个134B ROM_INCBIN仍列既有§5.1，无新块/遗漏。 |
| C3 | 自主ref-scan | ✅ | ROM/asm和块分类未变，复用首轮逐半字目标raw/THUMB及真实分支证据；96eec保留raw1/像素巧合/effective0，952fc两真实分支仍DISASM。 |
| C4 | 值/单位 | ✅ | 原8槽字段/表达式完全不变，复用首轮全部ROM值和8 LDR核验；32表值本轮再次读取一致。 |
| C5 | 现有符号复用 | ✅ | 22constants内容hash全不变、6002定义结论有效；NEW0。switch明确复用现存id31014，不新建别名。 |
| C6 | 名称/对象/碰撞 | ✅ | 首轮#1已修：两个现有LABEL只交换primary，不rename/namespace变更，无同址同名操作。8池名及其他标签命名计划均未变化。 |
| C7 | DATA-ref和实际导出 | ✅ | 95550既有USER ref不重建，id31014成为primary USER LABEL；9565c原定新增RAM DATA-ref与RAM2B目标合同未变；六RENAME仍原equate+空refs。两种导航元数据变化已准确限定。 |
| C8 | 新注释使用现名 | ✅ | 所有PLATE/EOL原文不变，首轮当前正式名核验有效；本轮只修改doc层对象说明。 |
| C9 | ASCII/长度 | ✅ | 本轮重新提取19PLATE：全部ASCII，长度177..485；8EOL均ASCII，逐字与首轮相等。 |
| C10 | Thumb/表与DISASM | ✅ | 32偶地址表本轮核对一致；10项原表及3条新指令/目标原合同不变，不添加Thumb+1到MOV pc表。 |
| C11 | 函数名与语义 | ✅ | 全19函数/plate/调用/全局证据输入未变，原无新增FUNC_RENAME结论继续有效。 |
| C12 | 消费者/来源 | ✅ | 原19完整消费者与3CID六记录的正确列/ROM/密码证据未变；95554完整双对象及引用新合同逐字段对照真实快照，本轮没有证据来源错误。 |
| C13 | 全覆盖 | ✅ | 首轮16709项/38228B、1518word、7原自动定义/20旧注释行/唯一8B裸块结论对应未变asm；原计划全覆盖不变。8槽19plate计数未扩缩。 |

未完成的工作仅是PASS后的Mode B落地与验收，不属于提案缺项；不能将本轮PASS描述为ROM构建或Ghidra写入已经成功。

## 第二轮新增证据

- `output/refine-run-20260831-194634/closure-review-round2-diff.json`：自行生成的proposal全文diff及递归plan差异。
- `output/refine-run-20260831-194634/closure-review-round2-checks.json`：31项独立断言全部通过，错误数组为空；包含10个修改块、50文件hash比对、完整双对象终态、32表项/30case快照相等及ASCII长度。slot比较仅不将只读查询参数`input_label`当Ghidra状态字段；所有真实状态字段均已比对。

## 修改清单（第二轮）

无。首轮#1的五子项全部解决；允许主线程按本版提案进入Mode B，保持禁止stage/commit和完整dry/保存重开/byte-identical门禁。

---

## 第一轮历史记录（原文保留，旧结论已由第二轮替代）

# Refine Review: F12-Historical-Closure

## 状态: NEEDS_FIX

第一轮独立正式评审，2026-09-01，Sol + xhigh。共 **1 项修改清单（#1，C6/C7）**：`08095554` 已有两个 LABEL 对象，提案遗漏现存全局 USER_DEFINED 标签 id31014，要求将 id4244 改成被它占用的同址同名。该步骤违反本机 Ghidra 重名检查，不能按原计划落地。其余 P0/C1-C5/C8-C13 均完成独立核验。

本结论只评提案。未运行 Ghidra 写入、build、stage 或 commit；未改变 proposal、正式源码、constants、进度。未预析模块13。下面的静态投影不代表落地完成或模块12已清零。

## 输入与复核方法

- 提案：`doc/dev/refine/F12-Historical-Closure.proposal.md`，SHA256 `8407798be1cb67e3aa8b6f31a2ed016411df8e7e49ba27e482cb6d34979881e8`。
- 当前模块：`asm/12_equip_activation_scan.s`，SHA256 `ac38c3b9b8068ba46ad0b070a4f099c1aa66691bdcfca33af06455f43467ad8f`。
- ROM：`roms/2343.gba`，SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`。
- 派生计划：`closure-plan.json`，SHA256 `52b484d57a6106cbfa549cddf8389a50e2fd0e8f992ee60ba70805f0e9a9ace8`；仅用于与提案/实物逐项比较，不作为扫描结论来源。
- 导出器：`tools/asm-regen/ghidra/ExportRangeToGas.py`，SHA256 `a46f8efae54994e58f5b067a34f16f7fe751df46b155b67fd0449e6c53db9fdb`。
- 独立从 asm 建立全模块地址图，读原 ROM 对照每项字节；重扫全 ROM raw/THUMB 值及所有25个现有 asm 模块的真实分支编码；逐条读取19函数完整消费者、两个 switch、DISASM 调用目标和共享 epilogue；全6002常量求值/查重；按逻辑 CID 列重新核对卡表。Ghidra 对象前态使用主线程成功只读导出的完整记录，并逐字段审查；没有另开 headless 或尝试重命名。

## P0 与精确范围

P0 ✅：提案存在且完整，无中止标记。模块范围 `[080941c4,0809d718)`，共38228B。本批 **8槽=6 RENAME+2 REF+0 EQ；19完整PLATE；8 EOL；1个8B DISASM（3指令）；NEW0/6 REUSE；FUNC_RENAME0；carve0；新增§5.1=0**。

7个实际自动定义为 `95280/952cc/952d0/95328/9532c/95330/9565c`。`95550` 是既有具名槽，为同址 EOL 与按名导出的必要依赖，已显式纳入8槽；不能算成第8个原自动槽。独立扫描得到20行旧自动名注释，落在19个完整 PLATE 及相关 EOL 的计划范围。

## 核验（C1-C13）

| # | 检查 | 结果 | 独立证据与边界 |
|---|---|---|---|
| C1 | Rule1 地址/路线图 | ✅ | 用户2026-09-01明确授权历史补漏；活动文档:320、总进度:12-14已登记本批。历史“等待授权”记录描述此前阶段，不覆盖后续授权。操作28项按地址递增；未借此处理模块13。 |
| C2 | Rule2 每块有归宿 | ✅ | 实际4个 ROM_INCBIN 共134B均保留原§5.1登记；唯一 `.byte` 8B在952fc，有真实条件分支入口，已按DISASM处理。没有遗漏块。 |
| C3 | Rule3 自主 ref-scan | ✅ | 全ROM对5块每个半字候选地址扫描 raw/THUMB 值。前三§5.1块均0/0；96eec raw1/Thumb0，唯一命中经真实固定长6bpp像素来源排除，有效引用0。实际分支仅952b6/952ba进入952fc，不能列§5.1。详见下表。 |
| C4 | R1 值/单位 | ✅ | EQ=0；仍逐槽核对全部8个原ROM u32，六既有equate和两地址值完全一致。8条PC-relative LDR按真实半字解码均指向指定池。 |
| C5 | R1 复用 | ✅ | 全6002定义求值成功，NEW0。四个ELIGIB byte offset及gSpriteAttrBuf各有唯一同值定义；消费者基址/访问单位吻合；switch直接复用既有LABEL，无ROM equate。 |
| C6 | R2 名/对象/碰撞 | ❌ | 8个池名满足格式，asm跨25模块无新名冲突；但真实08095554已存在同址全局全名 id31014，原计划对id4244的重命名会抛DuplicateNameException。需执行#1。 |
| C7 | R3 实际导出可执行性 | ❌ | 六RENAME保留空refs及原equate，9565c的既有RAM主LABEL+新DATA/USER ref方案正确；95550保留既有USER ref正确，但其target重命名步骤不可执行。按#1仅提升id31014即可满足原导出器primary USER LABEL路径。 |
| C8 | R5 现名 | ✅ | 19个新PLATE及8个EOL引用当前正式名，无旧FUN_/DAT_/DWORD_/PTR_/UNK_残留；95a18保留内部LABEL事实，未虚构Function。 |
| C9 | ASCII/长度 | ✅ | 19完整PLATE纯ASCII、长度177..485；8个EOL纯ASCII。19旧全文/hash与源码及真实Ghidra记录一致，明确整体替换而非截断旧文。 |
| C10 | THUMB/carve/表 | ✅ | carve0；两个MOV pc表分别10/32项，全部偶地址，必须原值保持，不加1。952fe为真正BL指令，ROM解码目标95ba8；95302为B至9533c。无callback literal +1新表达式。 |
| C11 | 函数现名与本体 | ✅ | 完整读19个函数及必要直接上下文，修正旧输入/返回/全局描述后没有新的全局基址与函数名硬矛盾；FUNC_RENAME0成立。poll函数首调用固定return_one_leaf并跳过循环的事实已明确披露。 |
| C12 | R6 消费者/来源 | ✅ | 下列19项均有真实asm:line与high证据；DISASM r0=0/保存帧/共享pop路径闭合；3CID六条卡表记录与ROM和正确CID列、密码一致。仅双Symbol前态合同遗漏由#1修正。 |
| C13 | 全部残留覆盖 | ✅ | 全模块16709项精确覆盖38228B，1518word/834hword/298对齐项，无缺口/重叠/字节差。7自动定义/20旧注释行/1裸8B均有处理项；静态应用文字与解码计划后自动定义/旧名注释/.byte均0，仅4个原§5.1块134B。投影不能证明#1的Ghidra操作成功。 |

## ROM、数据块与控制流证据

| 原块 | 长度 | raw / THUMB 命中 | 实际控制流与归宿 |
|---|---:|---|---|
| 0809437c | 0x1c | 0 / 0 | 前指令9437a为BX r1，无fall-through；原§5.1。 |
| 08094c3e | 0x22 | 0 / 0 | 前指令94c3c为BX r0，无fall-through；原§5.1。 |
| 080952fc | 8 | 0 / 0 | 952b6/952ba两条已解码条件分支进入起点，必须DISASM。 |
| 08095b28 | 0x14 | 0 / 0 | 95b1c为BX r1，随后对齐/池，无fall-through；原§5.1。 |
| 08096eec | 0x34 | 1 / 0 | 唯一raw在08b16c2f，已确认像素数据巧合；96edc为BX lr，随后对齐/池，无fall-through；原§5.1。 |

`08b16c2f` 位于 `graphics/bin/card-images/tiles/tb1316.bin` 的 `+0x2ef`，该4800B文件逐字节等于ROM `[08b16940,08b17c00)`。`data/card-image-tiles.s:1322` 和 `tools/rom-export/export_card_images.py:226-232` 给出直接incbin/原ROM切片关系。命中四字节为 `ec 6e 09 08`；包含它的6B位打包组 `30 ec 6e 09 08 82` 解出8个6bpp像素索引 `48,48,46,27,9,32,32,32`。这是固定长像素位打包，不是指针表，不称压缩资产，也不把四字节误称四像素；登记必须保留 raw=1/effective=0。

952fc原字节 `00 20 00 f0 53 fc 1b e0` 独立解码为 `movs r0,#0; bl init_equip_card_sprite_row_entry; b LAB_0809533c`。8个原单元均DataDB/undefined1、TMode=1、没有Instruction或Function归属。95ba8本体保存r8及自己的栈，使用r0零值分流并正常恢复；9533c/3e/40的pop{r4}/pop{r0}/bx r0闭合5220的原栈帧。禁止在952fc建独立函数或扩大5220既有44B Function body。95ba8既有776字符plate不属于本批写入范围，保持原文。

只增加952fe→95ba8 CALL与95302→9533c JUMP；952b6/952ba的原条件引用及9533c原8条JUMP均保留。两表的MOV pc半字均为0x4687；9524c有10项、95554有32项（30个不同case目标）。raw扫描结果和所有表值已保存；不因表目标为Thumb代码而改成奇地址。

## 8槽核验

| slot | ROM u32 / 表达式 | 分类与消费者 |
|---|---|---|
| 08095280 | 0x1d5c / ELIGIB_ACT_TYPE_OFF | RENAME；95274 LDR，steps8/9以LP基址读取u16 activation type。 |
| 080952cc | 0x1d6c / ELIGIB_ANIM_STATE_OFF | RENAME；952aa LDR，step3读动画状态并区分11、12..15及范围外。 |
| 080952d0 | 0x1d68 / ELIGIB_SPRITE_CTRL_OFF | RENAME；952bc LDR，step3读取sprite-control参数。 |
| 08095328 | 0x1d68 / ELIGIB_SPRITE_CTRL_OFF | RENAME；9530a LDR，step1初始化display context。 |
| 0809532c | 0x1d6c / ELIGIB_ANIM_STATE_OFF | RENAME；95310 LDR，step1传动画状态减11。 |
| 08095330 | 0x1d54 / ELIGIB_STATE_CTRL_OFF | RENAME；95322 LDR，经共享store清state。 |
| 08095550 | 0x08095554 / switchD_0809554c__switchdataD_08095554 | REF；95546 LDR后经32项MOV pc表分派；slot id31015、名称/source/primary及既有operand0 DATA/USER_DEFINED主ref全部保留。目标合同见#1。 |
| 0809565c | 0x0201b870 / gSpriteAttrBuf | REF；9564c LDR，case0x17将base+0x300的bit1置位；原空refs新增唯一operand0 DATA/USER_DEFINED主ref。 |

六DWORD原数据均/dword长4，恰一个正确equate，refs_from为空；不能套用上一段LP指针RENAME引用合同。9565c池为/undefined4长4；目标gSpriteAttrBuf id21747是现存USER_DEFINED主LABEL，而目标数据实际/undefined2长2，不改数据类型、不读未初始化RAM。引用SourceType与目标LABEL SourceType已分别核对。

导出器:506起先选目标primary Symbol，再要求USER_DEFINED及ROM LABEL，:557读取`getName()`；没有因已有secondary USER标签而自行选择它的路径。六RENAME通过现存equate fallback，9565c通过RAM LABEL+DATA ref。 `_pick_best_symbol_name`:143-160使用primary的qualified name，定义端:259-276按地址去重；独立调用原函数确认primary切换前后定义名相同，保留两对象不会导出两个重复定义。已调用原导出函数的独立最小探针确认所有8个预期表达式，但探针只证明满足终态时能导出，不能绕过真实Symbol重名规则。

## 19完整PLATE语义核验（置信度均high）

| 入口 / 当前函数 | asm12证据行 | 独立核验重点 |
|---|---|---|
| 94290 get_clamped_tile_row_count | 110-139 | signed phase<=5返0；7..38与40..71两个区间分别减6/39，其余为1；unsigned min上限。 |
| 942dc get_monster_slot_entry_ptr | 163-170 | 无输入；base+8读index，返回base+0x10+4*index，非条目解引用。 |
| 942ec get_effect_slot_entry_ptr | 178-183 | r0=index；返回gEquipLpZoneEntryBase+4*index，32位运算。 |
| 94314 get_duel_activation_zone_id | 209-214 | 无输入；返回base+0xc的u32。 |
| 94564 read_slot_palette_index | 525-536 | 返回base+0x410+2*index半字的高8位。 |
| 9463c advance_prng_state | 668-687 | seed位于LP+0x1ce0；LCG乘0x343fd加0x269ec3，返回新seed[30:16]。三个声称caller均由实际BL编码确认。 |
| 94664 sample_prng_scaled | 691-698 | r0 scale；乘积32位截断后>>15，注明正scale且无溢出的范围前提。 |
| 946f8 enqueue_duel_phase_sprite_by_side | 786-829 | 无输入；backup sentinel与实际side判定；type0xb/0x800b，其余实参0，返回值不定义。 |
| 94750 init_duel_phase_display_flag_with_sprite | 834-875 | r0 player；discard guard；variant1/2与type0x23/0x8023分路正确。 |
| 94c10 poll_sprite_seq_until_done | 1489-1510 | 原r0仅保存为循环续行标志；首次return_one_leaf实际固定1，直接结束；旧循环与return_zero_leaf路径客观说明。 |
| 94c60 tick_equip_activation_dispatch_hub | 1516-1574 | current-player zone0xb检查Last Turn；null handler返1；所有nonnull路径返0，handler非零才推进phase/清counter。 |
| 94cd4 tick_equip_activation_main_sequence | 1595-1701 | mode3/busy/discard前置返1；六调用短路链；LP+1d10写最后结果为0的bool；后续两个被调函数返回值被丢弃，最终0。 |
| 94dac advance_duel_turn_by_prng_anim | 1712-1815 | null callback写variant/selected-player word并返1；非空路径按PRNG/anim gate及callback推进共享state，返回合同正确。 |
| 94f70 update_card_display_index_by_type_rules | 1973-2106 | 24B entry/r1 index；type0x23/0x22、flags、field9及前项/Negate Attack条件对应显示索引；95a18实际从gSpriteAttrBuf+0x310加载r1。 |
| 95220 dispatch_equip_confirm_phase_by_step | 2352-2495 | 10项step表、step3动画状态分路和共享stack；入口step以word读取，而steps8/9后续读取u16。新8B路径r0=0闭合。 |
| 95380 pack_sprite_row_attr_words | 2539-2571 | 四低16字段构造两个word；实际r2=SP+2、长度6；r0返回透传。 |
| 954e8 step_prng_anim_frame | 2702-3497 | 完整32case及no-entry状态分路；busy返1；type1、4/5与超范围路径可返0，其余case及bit1写入准确。 |
| 97150 dispatch_to_effect_handler_by_card_type | 6520-6552 | 18条16B记录，word key比较，entry+0xc函数指针；r0/r1/r2透传，无pointer null guard；void。 |
| 9757c refresh_slot_activation_display_if_changed | 7080-7246 | 无输入；0x44B局部state与gEquipChainSlotRefs+0xec缓存；首两word早退、changed检测和guard的step1/2副作用正确。 |

19新PLATE长度依次为283/200/177/197/224/291/276/359/323/388/405/413/404/451/429/342/430/372/485。旧全文、hash、Function id/name/body范围、incoming及EOL守卫与真实记录逐字段一致；19个body的ROM字节hash独立复算一致。这里没有要求对未写的段外callee plate做附带订正。

CID来源按`data.md`逻辑CID列（第4列）匹配，绝不使用整行首次命中：

| CID | 名称 / password | card-stats主记录行 / ROM CID地址 | data.md行 | 全部卡表记录 |
|---|---|---|---:|---:|
| 12c4 | Negate Attack / 14315573 | 8439 / 0981a168 | 635 | 2 |
| 151e | Last Turn / 28566710 | 14224 / 0981c7a6 | 1078 | 2 |
| 177a | Earthbound Spirit's Invitation / 65743242 | 20334 / 0981f00a | 1543 | 2 |

另外三记录在card-stats:35800/42086/48618，ROM CID地址09826282/0982963e/0982ca26；六记录的逻辑CID、name、password全一致。`card_####`记录序号使用十进制，ROM CID地址为098169b8+22*index。

## 修改清单

### #1 — C6/C7 — 修正08095554既有双LABEL的复用合同

**实际前态**（`root-closure-switch-before.json`，extra_targets地址08095554）：

| id | name / qualified_name | source | primary |
|---:|---|---|---|
| 4244 | switchdataD_08095554 / switchD_0809554c::switchdataD_08095554 | ANALYSIS | true |
| 31014 | switchD_0809554c__switchdataD_08095554 / 同名全局 | USER_DEFINED | false |

目标数据已是/pointer长4。引用包括来自95550的operand0 DATA/USER_DEFINED/primary，以及95546的PARAM/ANALYSIS、9554a的DATA/ANALYSIS。两个LABEL都不是FUNCTION。既有95550槽Symbol id31015和它的USER ref均正确，不需要重建引用。

**原计划为何不能执行**：proposal:95及98、REUSE表:351、guard:371把id4244规范到全局完整GAS名。该名字已被id31014占用。本机Ghidra12.0.3的`SoftwareModeling-src.zip`中，`SymbolDB.java:292-306`的两个setter均调用`setNameAndNamespace`，:367-368和:427-430执行重复检查；`SymbolManager.java:489-495`对同一memory address/name/namespace的现存符号直接抛`DuplicateNameException`，在LABEL允许跨地址重名的检查之前已经拒绝。同对象改namespace后再改名也无法避开此冲突。没有在真实DB上试改。

**Mode A必须一次性完成以下五项**：

1. 将95554目标动作明确改为：精确复用 **id31014** 现有global USER_DEFINED全名LABEL，仅调用其`setPrimary()`；id4244保留原对象、地址、scoped namespace、短名、source=ANALYSIS，仅primary从true变false。两个id都保留；不setName、不setNamespace、不setSource、不createLabel、不delete/合并任何同址标签。本机`CodeSymbol.java:136-160`证明该primary切换会解除旧主标签并设新主标签，不改两者名字/source/ID。
2. 前态dry守卫必须枚举95554的完整symbols集合并精确确认上述两个对象、name、qualified_name、type、source、primary；确认目标/pointer长4及既有refs。不得只看primary，或以同址任意USER标签替代指定id31014；不符时停写报告。保持95550 id31015、原u32、数据类型/长度、equate、原引用集合及所有operand/source/primary，保持32个table words/30个case目标及其symbols/data/refs。
3. 后态守卫只允许两对象primary对调：id31014为唯一primary USER_DEFINED全名LABEL，id4244为原scoped ANALYSIS非primary LABEL；两个id/name/qualified_name/source/type仍与前态相同，不新增/删除对象。95550原USER DATA ref不增删重建；表/case对象与全部值不变。原导出器据新的primary选中正确GAS全名，95550必须输出`.word switchD_0809554c__switchdataD_08095554`，不接受裸值或短名回退。
4. 同步提案所有相关文字及派生`closure-plan.json`的switch target action/完整前后态、`closure-selfcheck.json`与hash/证据说明。至少修正REF段、导出路径解释、REUSE来源id、落地guard及全模块范围“label表示改变”的表述。明确原id4244规范化步骤已被既有id31014 primary提升替代。不得将此修复说成实际Ghidra验证或落地成功。
5. 修订保持8槽地址/值/池名/分类、6RENAME的equate与空ref、两REF的池引用合同、19PLATE完整文本/旧hash、8EOL文本、DISASM三指令和函数body合同、4块§5.1分类及NEW0/6REUSE/FUNC_RENAME0/carve0全部不变。只有95554目标对象动作及其解释/守卫/计数未变的派生同步需要修改；不扩范围。

修订后进行下一轮正式review；原版本不可进入Mode B。下一轮可按输入hash复用未变ROM/asm/constants/消费者证据，但必须独立核对exact diff、双对象完整前态和新动作、引用不变及导出路径。

## 独立证据文件

均位于`output/refine-run-20260831-194634/`，由reviewer独立生成：

- `closure-review-map-refscan.json`：16709项完整ROM字节图、原7自动定义/20注释行、5块全ROM raw/THUMB搜索、全25模块真实分支解码、两switch与新BL/B。
- `closure-review-constants-asset.json`：6002常量求值/同值复用、8槽ROM值、96eec像素命中来源及6bpp解包。
- `closure-review-guards-projection.json`：19旧全文/hash/body守卫、8槽前态、文字与DISASM静态投影；其asm名字碰撞检查不代替完整Ghidra对象集合检查。
- `closure-review-exporter-disasm.json`：原导出函数探针、95554完整双Symbol前态、RAM2B元数据、8undefined单元及8 LDR解码。
- `closure-review-symbol-api.json`：本机Ghidra源码中重名拒绝和primary切换的准确文件/行证据。
- `closure-review-cid.json`：3个正确CID列匹配、六条卡表记录及ROM CID/密码闭合。

## Reviewer Verdict: F12-Historical-Closure = NEEDS_FIX(1 items)


---

## Reviewer Verdict: F12-Historical-Closure = PASS
