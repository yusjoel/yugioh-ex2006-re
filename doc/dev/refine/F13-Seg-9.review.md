# Refine Review: F13-Seg-9（三轮）

## 复核输入

- 段范围：`[0x080a585c,0x080a689c)`，长度`0x1040 = 4160` bytes。
- proposal：`doc/dev/refine/F13-Seg-9.proposal.md`，SHA256 `3d6fc06bbf6b51c1c74b59aa71fc8a020d57b14d5a40b35687b67ca544a13bbf`。
- slots：`doc/dev/refine/F13-Seg-9.slots.tsv`，SHA256 `2e1ddfd1d7896b39decd2884c1067276519106e98e72a0b074d02d7885050e6d`。
- plates：`doc/dev/refine/F13-Seg-9.plates.tsv`，SHA256 `36548a9fc69ac3916c5362e7f449749dfb86f4c3649cbe30254b69aeef22d5a4`。
- 三轮输入清单：`output/refine-run-20261011-103530/f13-seg9-review-inputs-v3.json`，SHA256 `3a729d39cc5b9b0cb3e56ed9bf7845a7bd74b8e0fa0ddbcaee0ad7e9f3476467`。
- fixer窄修门禁：`output/refine-run-20261011-103530/f13-seg9-mode-a-checklist-gate-v3.json`，SHA256 `fd93bf7ef3ba346fd49bbcb0593440a72b324d07fe0370194bb8832601aa7477`。
- root不变量门禁：`output/refine-run-20261011-103530/root-f13-seg9-mode-a-contract-gate-v3.json`，SHA256 `3a3cec96d176c9653a213bbefe96b60dda066ae93cf6a00395d319d72e10588c`。
- 二轮正式输入完整保存在`output/refine-run-20261011-103530/seg9-review-round2/`；manifest SHA256为`73d9f2490b8ad5e6e0bb683362c36b09fc2963bc6e2793fcb06bce7c8dee6891`，二轮review SHA256为`3ae6f7d6d1f1fdb032c79dc35e4a36179b96e715ab907edbacec95ba374c8372`。

proposal非空，P0标记与禁用措辞扫描为空。本轮只写本review；未写proposal、TSV、正式源码、Ghidra工程或进度文档，未运行build、stage或commit。

## 二轮C5修订复核

当前proposal与二轮归档逐行比较只有第356行变化。新句将44个EQ槽精确拆成36个既有定义复用和8个新Thumb alias使用；slots、plates及全部只读证据hash不变。

独立按`slots.tsv reuse_status/target_contract`重算结果如下：

| 类别 | 数量 | 精确分布 |
|---|---:|---|
| REUSE | 36 | `constants/ewram.inc` 19；`constants/card_info.inc` 12；`constants/duel_field.inc` 3；`constants/demo_state.inc` 2 |
| NEW | 8 | `check_equip_sub_entry_slot_pair_eligible_1` 2；`check_moth_evolution_slot_requirement_1` 2；`check_special_summon_slot_requirement_with_pair_exclusions_1` 4 |

3个段内alias与4个范围外callee alias共同构成proposal §9的7个新GAS Thumb aliases。8个NEW槽的`target_contract`均为`gas=asm/rom.s:NEW`；36个REUSE槽均指向上表四份constants文件。proposal:356、§9 alias表、slots附件及§15自检现在互相一致，新增常量数为0。

## 独立证据连续性

- ROM、ASM和只读DB输入未变化。`root-f13-seg9-baseline.json` SHA256仍为`4a44841594b0b90891f639fdbb3331e2f2e63ff74e77d31a1592ca6dd49af16d`，覆盖1689个InstructionDB（1654条助记符、35条`.hword`）、145个4-byte words和29段共58B padding，合计4160B，无空洞或重叠。
- 145个word由111个自动名槽和34个既有switch words组成。111槽动作精确为`44 EQ + 52 REF + 15 RENAME`；111个ROM小端值、旧Symbol/Data/ref/equate/EOL前态均与附件冻结字段相等。34个switch words继续逐项PRESERVE。
- 主范围裸块数为0，carve=0、disasm=0、§5.1=0。范围外12B表`[0x09e478b0,0x09e478bc)`原字节为`881200009b120000b8120000`，三个word为`0x1288,0x129b,0x12b8`，前后bookend闭合。
- 首轮独立raw与`THUMB|1`扫描证据hash连续。111个槽地址只有`0x080a5bf4`出现一个Thumb命中，位于`graphics/bin/card-images/tiles/tb0891.bin+0x0ec1`，原字节`f55b0a08`，宿主`data/card-image-tiles.s:897`。13个Function入口共有14个`entry+1` word命中，精确等于`f13-seg9-packed-thumb-prestate.tsv`：8个EQ-only源和6个PRESERVE源。外表只有表首地址raw=1，命中`0x080a5a38`，其余raw/Thumb计数为0。
- 六个FUNC_RENAME、13条段内PLATE及5条必要范围外caller PLATE的body、caller与返回值证据不变。`0x08069e40`旧DB PLATE继续保持CRLF 2186字符、导出LF 2163字符的合同。
- 当前18条PLATE和111条EOL全部ASCII，PLATE最长437字符，无`FUN_/DAT_/DWORD_/PTR_DAT_/UNK_`残留；111个final slot label均符合`^[a-z][a-z0-9_]+$`且唯一。

## 首轮四项修订保持关闭

| 首轮项 | 结果 | 三轮复核 |
|---|---|---|
| #1 两个mask重复定义 | ✅ | `0x080a5f30/0x080a5f34`复用`DEMO_CLEAR_BITS_8_1/16_9`；TSV、`0x080a5e28` PLATE及新增常量计数一致。 |
| #2 15个RENAME概括错误 | ✅ | 前14槽保持`/pointer:4`、DEFAULT DATA ref；`0x080a6874`保持`/dword:4`、USER_DEFINED DATA ref；target均为USER_DEFINED `gP1LifePoints` Symbol ID15545。 |
| #3 `0x080a5f38` PLATE语义错误 | ✅ | PLATE与`asm/13_equip_placement.s:18942-18961`一致，清零目标为`ELIGIB_STATE_CTRL_OFF`，参数来源、mode分支和返回1均准确。 |
| #4 三张卡证据与Gamma密码 | ✅ | 三条`slot/icid -> cid -> card name -> logical CID -> password`证据闭合；明确排除`set_code`与任意首字符串命中；Mode B只允许`constants/card_info.inc:1152`的密码注释订正。 |

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|---|---|---|
| C1 | Rule 1：范围与路线图 | ✅ | `doc/dev/p5-refine-13-equip-placement.md`与`doc/dev/refine-progress.md`指定同一半开区间；承接已完成Seg-8，未跳号或回头。 |
| C2 | Rule 2：每个裸块有归宿 | ✅ | 主范围`ROM_INCBIN/.byte`裸块数为0；必要范围外12B表已有精确carve、原字节、宿主和bookend合同。 |
| C3 | Rule 3：§5.1块确为0引用 | ✅ | §5.1=0；raw/Thumb重扫把有引用的范围外表纳入carve，并以具体资产文件、偏移、原字节和命中数证明唯一槽地址命中为资产偶合。 |
| C4 | R1：EQ值等于ROM | ✅ | 44个EQ槽逐项等于ROM四字节小端值；7个新Thumb alias均等于对应偶地址Function入口`+1`。 |
| C5 | R1：常量复用 | ✅ | 36个REUSE精确分布为19+12+3+2；8个NEW精确分布为3个段内alias的2+2+4。proposal、TSV及§9表一致；新增常量=0。 |
| C6 | R2：槽名合法且唯一 | ✅ | 111个final label全部合法、唯一，当前实现面没有同名占用。 |
| C7 | R3：label/ref接通及前态守恒 | ✅ | 52个REF、15个RENAME、外表carve及8个packed EQ-only源的USER-label/Data/ref/equate计划完整；reference source与target Symbol source分别冻结，`0x080a6874`类型差异明确。 |
| C8 | R5：现名与PLATE引用 | ✅ | 六个final Function name与body/caller相符；18条PLATE均使用现名，5条范围外caller投影限定在实际host，没有扩展后段语义。 |
| C9 | ASCII | ✅ | 18条PLATE与111条EOL均为纯ASCII，声明长度与实测字符数相等。 |
| C10 | carve与Thumb `+1` | ✅ | 12B carve的三个CID word逐值等于ROM；14个packed words满足冻结合同，8个EQ-only与6个PRESERVE保持其余Symbol/Data/ref/EOL前态。 |
| C11 | 函数误名 | ✅ | 六个body/全局访问与旧名矛盾的函数均列入FUNC_RENAME；其余七个段内函数保留名与控制流一致。 |
| C12 | R6/R8：消费者、PLATE与卡数据证据 | ✅ | 消费者证据均给出file:line与置信度；两条修订PLATE与控制流一致。三张卡的CID列、卡名、逻辑CID和密码由四类结构化文件交叉证明，Gamma注释订正scope精确。 |
| C13 | 完整残留与布局 | ✅ | 111个自动名槽与附件地址/旧名集合精确相等；34个switch words全部冻结。1689 InstructionDB、145 words、58B padding闭合4160B，0 carve遗漏、0 disasm遗漏。 |

## 状态: PASS

## 修改清单

无。

## Reviewer Verdict: F13-Seg-9 = PASS
