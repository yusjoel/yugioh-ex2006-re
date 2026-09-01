# Refine Review: F13-Seg-1

**当前结论：第二轮正式复审 PASS（2 / 3）。** 首轮两项已闭合；本文件保留首轮 NEEDS_FIX 原文作为历史记录，最新输入、复核证据与最终结论见文末“第二轮正式复审”。PASS仅批准本版提案进入后续落地流程，不代表已经写入或通过构建。

## 第一轮正式评审

- 日期：2026-09-01；reviewer：Sol / xhigh；正式轮次：1 / 3。
- 范围：`asm/13_equip_placement.s`，`[0x0809d718,0x0809e6f4)`，4060 B。
- 本轮结论：**NEEDS_FIX（2 项）**。两项均为 C12：一条直接消费者证据混入旧注释；一个新 PLATE 的返回条件写宽。其余核验项通过，但不据此批准落地。
- reviewer 仅写本 review 与运行目录中的 `f13-seg1-review-*`；未改提案、正式源码、constants、数据库或进度，未 build、stage、commit，未启动 headless，未分析 Seg-2。独立重读 ROM、实际汇编、消费者和工具实现；executor 自检没有作为判定依据。

## 输入锁定

| 输入 | SHA256 |
| --- | --- |
| `doc/dev/refine/F13-Seg-1.proposal.md` | `4892244b810fd5a76a809c9b3dfa219a6c41d89fca9a7613699bb4dd469e9006` |
| `asm/13_equip_placement.s` | `e473bd1db9d96114f78e5ea8cde07ee83c9003d7a4f6e920ad25887196190671` |
| `f13-seg1-plan.json` | `58c3045850b13a4cceffbc9210f1eaad63128c807b5ce34ae9a319ed4fb74471` |
| `f13-seg1-plates.json` | `ecd6512dd262f9a78d1287da32aec5db52d261bd899d71392490a6376acf5d8d` |
| `f13-seg1-selfcheck.json` | `7fcf1917cd6c635889736a3315bdab8cae790a614e24a26e136654375e6880b8` |
| `roms/2343.gba` | `f405c620da05a817a5d63f45a4707b914260fb5802fe519b1e31bf050ba8f524` |

以上运行文件的目录均为 `output/refine-run-20260831-194634/`。收尾时重新核对提案、asm、plan、plates、selfcheck 的实际 hash，均与本轮输入一致。

## P0

**PASS**。提案存在、非空、包含完整动作表、15 个全文 PLATE 和 142 条 EOL；禁用标记与零容忍用语扫描无命中。以下两个问题进入 NEEDS_FIX，不属于 P0_FAILED。

## 核验（C1-C13）

| # | 检查 | 结果 | 独立证据与结论 |
| --- | --- | --- | --- |
| C1 | Rule1：地址序与路线图 | ✅ | 活动文档 `doc/dev/p5-refine-13-equip-placement.md` §五的 Seg-1 为本范围。F12 closure 已闭合后进入模块13；不包含 `0x0809e6f4` 的下一入口。三张段外 ROM 表是本段 literal 直接引用的必要 carve 依赖，并非后段函数分析。 |
| C2 | Rule2：裸块归宿 | ✅ | 按真实汇编地址重建 4060 B，段内 `ROM_INCBIN/.byte/UNK` 裸块均为0。39 个 `.hword` 是既有 Thumb 指令；32 个 `.zero 2` 是64 B对齐。段外三表共252 B全部 carve；无静默保留的被引用块。 |
| C3 | Rule3：raw/THUMB 扫描 | ✅ | reviewer 对三表每个2 B候选地址、两个 switch base、24个去重 case 目标及两个改名入口独立做全 ROM 原始字节搜索。三表 base 各 raw=1、odd=0，内部候选均0；无 §5.1 项。`0x0809e3e1` 的1次 raw 命中保留，并以两条字符串指针的跨 word 窗口和真实对齐读取排除有效 Thumb 引用。 |
| C4 | R1：槽值 | ✅ | 142个实际自动槽逐一从 ROM 读小端 u32：93 EQ、19 REF、30 RENAME 全部与提案相符。另52个 switch word 均为偶地址；共194 word。提案元组、统一 EOL 表和 plan 的地址/值/分类/输出符号一致。 |
| C5 | R1：常量复用 | ✅ | 独立解析当前22个 constants 文件的5989条 `.equ`，5989个唯一名、无解析错误。35个 REUSE 的名称/值/来源正确；9个 NEW 无同名碰撞。8个 NEW 值无既有同值定义；`0x8002` 仅有文本层标志定义，与本段 sprite selector 不同域。 |
| C6 | R2：命名及对象 | ✅ | 142个新槽名均匹配小写格式且唯一；连同9个 NEW、2个新函数名和3个新表头共156个名字，未与正式 asm/data 定义或既有函数名碰撞。两个 switch 完整 symbols 集合各只有1个 ANALYSIS LABEL：id6770/id7145，可复用同对象规范全局 GAS 名；没有 F12 closure 的双对象冲突。 |
| C7 | R3：真实引用与导出接通 | ✅ | 独立比较142槽、12个 REF 目标、63表项、边界及76项 switch/case 前态，plan 与 root 只读原始记录逐字段一致。30个 LP 槽保留 DATA/DEFAULT/operand0/primary；17个空引用 REF 新建 USER DATA，两个 switch 槽精确替换既有 DEFAULT。同值 RAM equate 与目标 USER LABEL 分别落实；两个 Data=None 的 RAM 目标保持 None。现有 exporter 路径可输出计划表达式。 |
| C8 | R5：PLATE 使用现名 | ✅ | 15个拟写 PLATE 均无 `FUN_/SUB_/DAT_/DWORD_/UNK_/PTR_` 自动名，也无两个废弃函数名；三 wrapper 引用新 callee 名。d914 的条件失真单列 C12 #2，不把名称检查当作语义通过。 |
| C9 | ASCII / 长度 | ✅ | 从提案独立抽取142条 EOL，与 plan 全文逐字相等，均 ASCII。15个新 PLATE 均 ASCII，长度依次为230/216/263/391/252/234/231/344/388/458/414/472/387/306/334，最大472。15个旧全文与实际 asm 连续注释、只读快照及旧 hash 一致。 |
| C10 | carve / Thumb 指针 | ✅ | 63个 `.word fn + 1` 逐项以当前 asm 符号地址及 inventory 偶 Function 入口核对，均等于 ROM odd 值。3表没有 NULL 项。两个 MOV-pc switch 保持52个偶地址 word，不能加1。原10160 B host 的前340 B + carve252 B + 后9568 B重建与 ROM逐字节一致。 |
| C11 | 误名与函数身份 | ✅ | d7ec 的 r2 实为 counter_base，node 类型固定1；e5e0 比较 CID1954，实际卡名为 VWXYZ-Dragon Catapult Cannon。两处 FUNC_RENAME 必要且准确。全25模块共20695条真实 BL解码，调用点分别3/2，与 incoming 相符；两入口全 ROM raw/odd均0。15原 Function ID/body/incoming/EOL 与 ROM body hash匹配；两个局部共享尾不能成为新函数。 |
| C12 | R6：消费者及语义证据 | ❌ | #1：d7b4 的“直接 literal-load 消费者”含旧 PLATE 行72，实际只有行76。独立解码170条 literal LDR，plan uses 共171项，仅此1项多余。#2：d914 的新 PLATE 把 `count_field_copies_of_card` 非零写成单纯场上存在，遗漏实际有效性过滤。17个 CID/35条卡表记录、其余数据流及常量域核对通过。 |
| C13 | 全覆盖 / 残留 | ✅ | 实际142自动槽=110 DAT+32 PTR；与提案和 plan 一一对应，无漏槽。静态投影保留1751个单元、全部指令字节、64 B对齐及52个 switch word，4060 B与 ROM一致；预计自动槽定义0、裸块0。没有把旧 PLATE 行当新槽，#1仅污染消费者证据。 |

## 独立测绘、ref-scan 与投影

独立测绘得到1751个连续单元：1486条常规指令、39个既有 Thumb `.hword`、194个 word、32处2 B对齐。实际 literal-load 解码采用 Thumb PC 对齐公式，得到170条；直接分支/调用284条，包括129条 conditional、70条 B、85条 BL。该测绘由真实 asm 注释地址和 ROM 机器码建立，不读取 executor map 作为结果。

三个 carve 表的真实基址引用分别为：

| 表 | 字节数 / word数 | base raw 命中 | base odd / 内部候选 |
| --- | --- | --- | --- |
| `0x09e476b0..0x09e47738` | 136 / 34 | `0x0809df88` | 全0 |
| `0x09e47738..0x09e4779c` | 100 / 25 | `0x0809dfe0` | 全0 |
| `0x09e4779c..0x09e477ac` | 16 / 4 | `0x0809e044` | 全0 |

`asm/13_equip_placement.s` 的 phase11/phase20 保存 `gP1LifePoints+0x1d20` 的索引，分别循环34/4项；phase12每次从局部索引0重新执行25项。三处经 `invoke_r1` 的 `bx r1` 使用 odd Thumb 目标；callback返回0时本 tick 返回0。边界不是从下一个符号猜得，而由循环上界和实际4 B步长闭合。

两个 switch 的 `0x0809d9f2/0x0809e1aa` 原字节均 `87 46`，即 Thumb `mov pc,r0`。21/31项表内偶地址直接保留当前 Thumb 状态。52个 word 指向24个去重目标，均落在本段真实代码。唯一额外 odd 值命中：ROM `0x09e58b99` 的4字节为 `0x0809e3e1`；窗口 `0x09e58b98` 为 `1c e1 e3 09 08 e1 e3 09`，实际两个 word 是 `0x09e3e11c` 和 `0x09e3e108`，字符串分别为 `deck/theme_010.ydc`、`deck/theme_011.ydc`。`asm/01_vija_scene_text.s:3853-3857` 以 index<<2读取 `card_deck_fs_path_table`；非对齐窗口不是该读取路径的指针项。保留 raw=1，不删除或改写该段外数据。

独立对静态投影的每条指令只允许槽名/函数名替换，重新求值194个 word，并复原4060 B，SHA256为 `9bbbcf2be55647a14c49ca25eb401c33c4e53fd5bdd1c8cc36423943adaf6460`。carve host为 `asm/rom.s:1371` 的 offset `0x1e4755c`、size `0x27b0`；拆为 `.incbin ... 0x1e4755c,0x154`、63 word、`.incbin ... 0x1e477ac,0x2560`，10160 B重建 hash为 `c24f85a4569f51e786b13508802437653e856b2ce41794c307537acaced6d2b4`，与原切片相同。此项是静态字节核对，不声称已经 build。

## 消费者、常量与函数语义

已逐体读取本段15个函数，以及判断输入/返回、计数过滤、间接调用、字节长度所需的直接 callee。没有用旧 PLATE 反推新语义。

| 入口 | 独立确认的输入、返回和关键行为 |
| --- | --- |
| `0x0809d718` | r0=player；Last Turn chain slot11存在、本方 occupied count非零、对方为0时提交sprite并返回0，否则1。 |
| `0x0809d764` | 只测试 Last Turn chain；不测试双方怪兽数量；命中提交后0，未命中1。 |
| `0x0809d79c` | Power Bond chain/entity用于卡图、LP indicator和slot sprite；命中0，未命中1。池值0x18fe正确；消费者证据须修 #1。 |
| `0x0809d7ec` | r2保存在高寄存器作 counter_base；`byte[node+2]&15==1`为固定类型过滤，`counter_base-(byte[node+2]>>5)`低16位传sprite；沿node+6逐个提交，始终1。 |
| `0x0809d86c/0x0809d880/0x0809d894` | 三个真实 push/BL/pop wrapper，传Crush Card/Deck Devastation/Pikeru与3/3/2计数基数；不是tail-call或zone参数。 |
| `0x0809d8a8` | 先starting player再player^1；entity非负时用timer-entity+1，signed结果>19才追加type11；两方完成后1。timer地址与LPbase+0x1cec一致。 |
| `0x0809d914` | 由有效 Infinite Cards计数决定提前返回；hand limit依次6、Hieroglyph命中7、对方有效Enervating Mist命中覆盖5；读取LPbase+0xc+player stride的hand count，超限提交count-limit并返回0。新 PLATE须修 #2。 |
| `0x0809d984` | 无参数；LPbase+0x1ce8给player，+0x1d1c给phase，+0x1d20为持久callback索引，+0x1d24为slot/callback cursor；default/unused返回1；已核三callback循环、slot20 B步长与共享0x120 B栈帧。 |
| `0x0809e078` | phase0按ctx word清0x1cc字节，非halfword数量；phase1 Gamble命中设flag0x17；+0x1d04仅抑制backup+1通知，不抑制backup+4；phase0为0，其他1。 |
| `0x0809e168` | 无参数；Timeater/flag/phase分派；unused/default返回0；phase30在field phase2/4扫描CID1954并调用 `apply_equip_activation_with_id_lookup`；flag/cancel出口或完成返回1。 |
| `0x0809e5e0` | r0=player，5个20 Bfield entry；低13位CID1954且u16+8非零才调用 `apply_equip_activation_via_packed_attr`；该调用非零才返回0，否则继续，最终1。与e168所调callee不同。 |
| `0x0809e654/0x0809e6a4` | r0是player，不是slot指针；5个slot低13 CID非零后分别测试Last Turn entity==1/0；首次命中返回index，否则-1。getter缺失节点返回-1，不满足==0。 |

`PLAYER_BLOCK_STRIDE=0x868` 为字节步长；field entry为20 B，chain node为8 B，`gEquipNodePool`不加player stride。`gDuelFieldSpellZoneBase=gDuelFieldSlots+11*20`，`gDuelFieldSlotState=gDuelFieldSlots+0x10`；ctx选择word为base+8+4*player。`0x1cf4`以LPbase访问，复用 `P2LP_BLOCK2_OFF_1CF4`，不选以field base定义的同值 `FIELD_STATE_OFF`。`0xfee`选择CID而非动画sentinel。`0xffffe000`复用已有低13位clear mask，EOL把对象限定为slot CID保存/清除/恢复，不声称访问OAM attr2。

9个 NEW 为3个CID、4个非零player sprite selector、`CARD_DISPLAY_OP31_PARAM_0135`、`gP1LpTimer`。`0x135`由r1传给 `trigger_card_display_op31_if_not_active`，该callee传给op0x31参数，不推定为卡号或字符串。`0x8002`的已有 `TEXT_RENDER_FLAG_LAYER2` 定义及消费属于文本渲染域，本段是 `enqueue_sprite_attr_record` 的r0选择器；另三个同类值的玩家分支同样闭合。

独立按 `data.md` 第四列逻辑CID查表，未按任意数字或记录序号匹配。17个CID及全部35条 `data/card-stats.s` 主/副记录的卡名、password、ROM记录CID均一致：0fee/1102/123b/1356/13b1/1400/1401/149d/150e/151e/159f/169c/1800/188c/18d5/18fe/1954。`0xa0<<5=0x1400`和`0xc0<<5=0x1800`为即时构造，未虚增池槽。CID1954的逻辑行1933、record1955、ROM CID地址098211ba、password84243274共同支持VWXYZ更名。详细35条记录及源hash保存在 reviewer CID证据中。

## C6/C7 实现条件与段外依赖

1. 142槽前态均为4 B DefinedData、equates为空；93 EQ原无outgoing，17普通REF原无outgoing。30 RENAME原引用都是operand0 DATA/DEFAULT/primary→0201c4e0；USER_DEFINED的是目标 `gP1LifePoints` LABEL id15545，不能混称引用来源。不得重建或升级这30条引用。
2. 两 switch base的完整 symbols 清单各只有一个对象：0809da00/id6770、0809e1c4/id7145。允许该对象规范namespace/name/source/primary，保持ID；不新增alias、不改24个case对象或52个word。两个代码池的既有同目标 DEFAULT ref须精确替换为 USER_DEFINED，不能依赖 `addMemoryReference` 合并自动提升来源；其他operand/其他目标引用保留。
3. RAM C5EC原只有DEFAULT动态名、DefinedData=None；新建USER主label但不建Data。D9C0原USER id20380、Data=None，两者都保留。E1CC原DEFAULT动态名、undefined4，保留22条原ANALYSIS READ/WRITE incoming，只增加D90C的USER DATA；不读未初始化RAM初值。其余5个既有USER RAM目标按原ID/source/type复用。
4. 三个新表头LABEL仅为代码侧REF提供 USER主符号。63原指针Data `/undefined *`、长度4和operand0 DATA/DEFAULT/primary→odd动态LABEL全部保留；不可重定向偶Function、升级来源或createData。两改名Function不在63项中，故表项target_primary导航名也不应变化。范围外477ac整个前态保留。
5. `ExportRangeToGas.py:527-562`选择primary outgoing后检查目标USER symbol；不要求既有引用本身为USER，故30 RENAME可原样导出。ROM目标必须LABEL，并由`:557`读取短名 `getName()`，所以两个 scoped switch需上述同对象规范名。数值EQ走`:565-584`的equate fallback。63个`fn+1`由 `rom.s`显式生成，不依赖exporter转换odd动态标签；不改exporter。
6. 全部1518个registry三元组（1515个FUN键、3个既有具名键）中，旧名相关集合恰为提案限定6条：d7ec/e5e0更新name+PLATE，三个wrapper只更新PLATE，97828仅替换一个旧Toon callee子串。当前asm12的97828 PLATE既无旧名也无新名，不能把registry旧全文写回Ghidra。
7. 当前CSV两行 `name`均为旧正式名，`proposed_name/score`均空。`sync_ghidra_names_to_proposals.py:94-98`对已具名分歧只warn；落地必须按方法论真实运行 `ExportFunctionInventory.py` 刷新4文件，再用sync的`--dry-run`审计并仅按两个address改CSV `name`，其余列/行不动。不得以全量sync意外同步无关历史差异。asm12严格只改97ac2/97b48两个BL目标拼写。
8. `0x0809e066`属于d984共享栈恢复；`0x0809e5da`属于e168共享返回。不得createFunction、覆盖PLATE、扩body或运行分析改变flow。保留5209个Function总数、15个既有身份及body/incoming/原指令EOL。

R1/R2/R3/R4/R7的值、命名、接通、无新增disasm、carve计划已闭合；R5/R6须完成以下两项修订。R8没有新图形/调色板资产，sprite含义来自寄存器和玩家分支。R9仅核对备份、精确守卫和byte-identical实施合同；本轮没有落地或build，PASS之后仍须dry、真实导出/构建、SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`、逐字节和持久化复核。

## 修改清单

### #1 — C12 — 删除0809d7b4的伪消费者，验证所有uses都是实际literal LDR

**证据**：提案`:584`定义该列为“全部直接literal-load消费者”，`:590`却列`72,76`。`asm/13_equip_placement.s:72`是包含旧自动名的旧PLATE，不是指令；`:76`才是`ldr r6,DAT_0809d7b4`，机器地址0809d7a0，原字节`04 4e`（halfword0x4e04）。解码为：

```text
((0x0809d7a0 + 4) & ~3) + 4 * 4 = 0x0809d7b4
```

**执行范围**：

1. 提案`:590`直接消费者行从`72,76`改为`76`；槽动作、值0x18fe、常量名、槽名、EOL均不变。
2. 同步当前 `f13-module-map.json` 的 `$.slots[2].uses`、`f13-seg1-slots.json` 的 `$[2].uses`、`f13-seg1-plan.json` 的 `$.slots[2].uses`，仅删除line72的注释项，保留line76实际LDR。按slot addr定位并断言旧内容，不能依赖索引盲改。模块map的 `stale_auto_comment_lines[0]`、`nonascii_comment_lines[1]`是正确的历史注释发现，必须保留；d79c旧PLATE全文/hash守卫同样保留。
3. 加强并真实执行当前自检：每一uses必须对应baseline中真实指令地址/机器码，拒绝以`@`开头的纯注释；按Thumb literal LDR掩码及PC对齐公式解码目标，逐槽对比完整集合。验收为142个槽集合全相等、170条真实LDR（不是171个文本命中），无漏项或额外项。可写run目录审计，不改正式工具源码。
4. 更新 `f13-seg1-plan.json.input_hashes` 中受影响map/slots哈希及 `f13-seg1-selfcheck.json` 的实际重跑结果、artifact哈希/修订说明。既有冻结`*-round1`及本轮review证据不改。仅删除可见表格中的72不足以关闭本项。

### #2 — C12/R5 — 0809d914的提前返回必须绑定有效计数，不写成单纯场上存在

**证据**：`asm/13_equip_placement.s:278-281`把INFINITE_CARDS_CID传给 `count_field_copies_of_card`，仅在返回非零时提前返回1。被调函数 `asm/02_text_lp_fieldspell.s:14438-14462`（08032862..0803288c）在CID匹配后还组合u16[slot+8]与slot+0x10的状态位，再决定递增计数；其他card分类路径也有有效性检查。给一个仍含该CID、但u16[slot+8]==0的槽，计数不会因该槽增加，故“present on the field”不能表达调用条件。

**替换全文**（ASCII，403字符）：

```text
r0=player. Return1 if count_field_copies_of_card(INFINITE_CARDS_CID) is nonzero. Otherwise limit=6, raised to7 by HIEROGLYPH_LITHOGRAPH_CID in chain slot11 and overridden to5 by available Enervating Mist(0x1800) zones for 1-player. Read count at gP1ZoneHandCount+(player&1)*PLAYER_BLOCK_STRIDE. If unsigned count>limit, submit set_lp_display_row_if_nonzero(player,count-limit) and return0; else return1.
```

**执行范围**：

1. 提案d914 PLATE条目`:355-358`采用上述全文，长度388→403；保留旧全文SHA256 `2f2f71710944e6bf95e4b9489e3184dfa27cca1f9fb85b755cc08e683bf41b0d`及全部真实前态守卫。
2. 同步 `f13-seg1-plates.json` 的d914 `text/length`、`f13-seg1-plan.json.plates` 同一条目，以及 `f13-seg1-projected-segment.s.txt` 对应新PLATE；只改这1个新PLATE，其他14个新PLATE原文不变。该函数不在六条registry依赖动作中，不扩展registry更改集。
3. 重核15个新PLATE ASCII/<=500、提案/plan/plates/projection文本一致、投影机器码/word不变；最大PLATE仍472。同步selfcheck的真实结果和受影响hash，并写ModeA exact-diff审计。不要声称修改了未重跑的检查。

两项合并修订后，142槽地址/值/新名/分类、93EQ/19REF/30RENAME、9NEW/35REUSE、142EOL、两FUNC_RENAME、三carve/63word、switch/REF/函数守卫与正式修改范围必须保持。无需扩展到后续段或修改源码/DB。下一轮应独立对比本轮冻结输入和修订版本，并凭未变源hash复用本轮ROM/常量/消费者/引用证据。

## reviewer证据文件

均位于 `output/refine-run-20260831-194634/`：

| 文件 | 内容 |
| --- | --- |
| `f13-seg1-review-map-refscan.json` | 自主地址测绘、1751单元、142槽、170literal LDR、284分支、三表/switch/改名入口全ROM扫描。 |
| `f13-seg1-review-constants.json` | 22文件hash、5989定义全量数值解析、9NEW/35REUSE与同值列表。 |
| `f13-seg1-review-cids.json` | 正确逻辑CID列、17CID/35记录、卡名/password/ROM实读与来源hash。 |
| `f13-seg1-review-consumer-lines.json` | 142槽真实LDR行集合对比；仅d7b4多出旧PLATE行72。 |
| `f13-seg1-review-callers-carves.json` | 全25模块20695 BL解码、3/2真实callers、63个fn+1求值。完整新增名称碰撞结论以dependencies证据为准。 |
| `f13-seg1-review-prestate-plates.json` | 142槽原态、15Function/旧PLATE全文/body ROMhash、142EOL、63Data/ref、边界、76项switch/case元数据逐项一致。 |
| `f13-seg1-review-dependencies.json` | 完整156新增名字检查、1518registry、限定6tuple、CSV/inventory两行、97828现有plate、伪uses出现位置与输入hash。 |
| `f13-seg1-review-projection-targets.json` | 12个REF目标真实前态、4060B投影、10160B host复原、跨word偶合窗口/字符串、消费者与工具源hash。 |
| `f13-seg1-review-issues.json` | 两修订项的机器码/实际条件证据及403字符替换全文。 |

## 状态: NEEDS_FIX

本轮完整修订清单为2项。当前输入尚未通过；不得进入ModeB。修订后进行第二轮正式复审，保留第一轮证据和历史结论。

## Reviewer Verdict: F13-Seg-1 = NEEDS_FIX(2 items)

## 第二轮正式复审

- 日期：2026-09-01；reviewer：Sol / xhigh；正式轮次：2 / 3。
- **结论：PASS。** 首轮 #1、#2 均按限定范围修正，无新增修订项。
- 首轮 review 冻结为 `f13-seg1-review-round1.md`，实际SHA256仍为 `89ae6a38eb1186bcfe5f83f0e743f48f307b384d981547f20c1871374db7ef7c`。上文首轮状态和问题保留，不回写成已通过。
- 本轮仅写当前review和 `f13-seg1-review-round2-*` 独立证据。没有执行ModeA脚本、headless、Ghidra写入、build、stage、commit或后段分析；采用自己的差异、hash与机器码核验。

### 第二轮输入锁定

| 输入 | SHA256 |
| --- | --- |
| `doc/dev/refine/F13-Seg-1.proposal.md` | `fd84b9c4fcffb99261851465d7f1bf2033fd0133009e4b0b070b1f06e6bdb1a7` |
| `f13-seg1-plan.json` | `6eb02a8e5b14f900f14119eac9c648589c5abc8d14a7cdd850dc8cca9c47f75f` |
| `f13-seg1-plates.json` | `478ce86a54ba46ff7d370ef6a36454c25001f39e40b1c0ae0f8d3750457e244e` |
| `f13-seg1-selfcheck.json` | `f2717b90b2cfc350a122f325bc5a86ba085132b4f78f442b622432f3a701fb4f` |
| `f13-module-map.json` | `95e93f2fba5a65dc19a6bde1c7a252697c5ad6bc2986fd0ad6cf87423b13552e` |
| `asm/13_equip_placement.s` | `e473bd1db9d96114f78e5ea8cde07ee83c9003d7a4f6e920ad25887196190671`（未变） |

### 修订范围与证据复用审计

独立以冻结第一轮文本/JSON建立差异，并把允许修改逆变换后与旧输入比较；没有采用fixer或root的PASS字段作为证明。提案和投影还执行了原始字节逆变换，确认未混入换行或其他文本修改。

| 文件 | 实际差异 | 结果 |
| --- | --- | --- |
| proposal | d914全文与388→403长度；d7b4直接消费者72,76→76；增加真实Thumb literal LDR校验合同一行 | 仅首轮#1/#2 |
| module-map | `slots[2].uses`仅删除line72项 | 其他完整对象相等；两个历史comment数组保留 |
| seg1-slots | `[2].uses`仅删除line72项 | 其余141槽及本槽动作数据相等 |
| plan | `slots[2].uses`；`plates[8].text/length`；map和slots两项input hash | 其他全部字段相等，包括全部REF/函数/表/case前态守卫 |
| plates | d914的`text/length` | 其他14条完整对象相等，所有旧全文/hash守卫保留 |
| projected-segment | 仅d914一个PLATE行 | 非注释行、194个word表达式和机器码注释相等 |
| module-selfcheck | map hash及明确的ModeA修订/复用说明 | 没有声称重跑全模块测绘；历史activity-doc hash明确标明历史状态 |
| carve投影 | 无差异 | 与首轮冻结文件逐字节相等 |

重新核对76个ModeA受保护文件hash、首轮9份review证据hash、首轮记录的相关asm/ROM/exporter/registry/CSV/inventory hash，均吻合；另外独立逐一核对22个constants文件hash与CID来源文件hash，均未变。由此复用首轮已实际完成的5989定义解析、17CID/35记录、完整消费者语义、三表/switch全ROM扫描和真实前态核验。此处复用的是带输入hash的首轮自主证据，不是executor旧布尔值。

已读 `f13-seg1-mode-a-check.py` 实现与结果：其当前LDR检查拒绝纯注释，验证机器码与ROM相等，解码 `(halfword & 0xf800)==0x4800` 和 `((addr+4)&~3)+((halfword&255)<<2)`，再逐槽比较完整集合。reviewer另行从真实asm/ROM重做同一事实核验，170条地址/源行/寄存器/目标/halfword全部与ModeA报告一致。未执行该脚本，以免写入非reviewer所有的派生文件。

新selfcheck保留原54项，`mode_a_revision`明确列出11项实跑、43项按未变输入复用，两组不重叠且并集恰为54项；另有3项新增检查。原54个值没有被悄悄重分类为全部重跑，`refscan_recheck`明确说明本次未重跑首轮全ROM扫描。全部当前artifact hash均匹配实文件；`all_input_hashes_unchanged`针对修订后plan，两个已审查的map/slots hash变动已单独说明。自检呈现与真实执行范围相符。

### 首轮问题闭合

**#1 已解决。** 当前提案`:590`、module-map、seg1-slots、plan均只保留d7b4的真实LDR行76。独立从实际ROM重新解码170条literal LDR；142个实际自动槽的全部uses集合、每条文本和源行均相等，缺项0、多项0、纯注释0。d7a0字节`04 4e`仍解码到d7b4，line72不再属于直接消费者。历史旧注释发现、d79c旧PLATE全文/hash及其余动作保持。

**#2 已解决。** 当前d914全文恰为首轮给定的403字符ASCII替换，提案/plan/plates/projection四方逐字一致；提前返回条件明确为 `count_field_copies_of_card(INFINITE_CARDS_CID)` 非零，不再写成单纯场上存在。旧全文hash仍为 `2f2f71710944e6bf95e4b9489e3184dfa27cca1f9fb85b755cc08e683bf41b0d`，未增加registry动作。其他14个PLATE完整对象不变，15个PLATE最大长度仍472。

### 第二轮 P0 / C1-C13

**P0：PASS。** 本版提案存在、完整，禁用标记和零容忍用语无命中。

| # | 结果 | 本轮依据 |
| --- | --- | --- |
| C1 | ✅ | 范围/15入口/路线图合同未变，仍为模块13首段，无后段分析。 |
| C2 | ✅ | 段内裸块0、disasm0；全部carve动作和原指令/对齐清单未变。 |
| C3 | ✅ | ROM、三表/switch地址集合及carve定义未变，复用首轮自主raw/odd扫描；跨word raw命中记录保留，§5.1仍0。 |
| C4 | ✅ | 本轮再次从ROM读142槽值，全等；194个word表达式未改，93EQ/19REF/30RENAME不变。 |
| C5 | ✅ | 22个constants源hash不变、9NEW/35REUSE动作不变；首轮5989定义与域语义证据仍成立。 |
| C6 | ✅ | 全部新槽名/函数名/目标动作及完整symbols前态不变；两switch同ID规范化合同保留，无新增alias动作。 |
| C7 | ✅ | 全部slot/target/ref/data前态守卫和正式依赖集合逐字段未变，exporter源hash不变；沿用首轮精确引用、RAM None和63odd引用保留条件。 |
| C8 | ✅ | 14个PLATE未变；唯一新全文使用现名 `count_field_copies_of_card`，无自动名或旧callee名。 |
| C9 | ✅ | 本轮重验142EOL ASCII、15PLATE ASCII/<=500及四方文本一致；d914=403、最大472。 |
| C10 | ✅ | 3表63个fn+1表达式和host切割投影逐字节未变；52个MOV-pc偶地址word未改，复用首轮实际ROM/Function验证。 |
| C11 | ✅ | 两FUNC_RENAME、六registry tuple合同、两个CSV name动作、真实caller/函数身份和共享尾合同未变，原body及直接消费者源hash相同。 |
| C12 | ✅ | 两项均闭合：142槽/170个真实LDR集合一致；d914改为有效计数非零条件。其余语义与CID证据输入未变。 |
| C13 | ✅ | 本轮独立重数110DAT+32PTR=142槽；1751单元/4060 B投影再次逐字节匹配ROM，无动作/覆盖扩展。 |

R1-R9本版提案均通过：R5/R6的两项修订已闭合，其余沿用本轮hash确认后的首轮独立证据。精确计数仍为 **142槽=93EQ+19REF+30RENAME，15Function/15PLATE/142EOL，2FUNC_RENAME，9NEW/35REUSE，3carve/63word/252 B，0disasm/0裸块/0§5.1**。第二轮再次重建4060 B投影，SHA256仍为 `9bbbcf2be55647a14c49ca25eb401c33c4e53fd5bdd1c8cc36423943adaf6460`。

### 第二轮独立证据与落地条件

- `f13-seg1-review-round2-diff.json`：精确JSON/文本差异、76受保护文件与首轮review证据hash、完整不变字段断言。
- `f13-seg1-review-round2-machine.json`：实际142槽/170 LDR解码、逐槽集合、15PLATE四方一致、1751单元/4060 B重建、22个constants源hash复核。文件原始SHA256与换行规范化文本SHA256分开记录。
- `f13-seg1-review-round2-selfcheck.json`：54项实跑/复用分组、3项新增检查、所有artifact hash、CID来源hash、ModeA结果的独立复现与原始字节逆变换。

本次PASS仅针对锁定hash的提案。ModeB必须保留首轮“C6/C7 实现条件与段外依赖”全部合同，先验证备份和真实前态、dry无失败，再执行精确写入；之后仍须真实inventory/export/build、byte-identical与持久化/范围验收。不得因本次PASS省略30条DEFAULT引用保留、63条odd引用保留、两个Data=None RAM目标、原switch对象身份或段外修改边界。reviewer未启动落地。

## 状态: PASS

第二轮完整修订清单为空；首轮两项均已解决，无新增阻塞。

## Reviewer Verdict: F13-Seg-1 = PASS
