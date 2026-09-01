# Refine Review: F12-Seg-9

## 状态: PASS

第三轮（最后一轮）正式复审通过。首轮#1的CID证据问题与补核#2的RENAME引用source文案均已解决，当前P0/C1–C13全部通过，157槽和其他语义计划不变。模式B尚须实现B1/B2检查修正并dry通过，不能直接运行旧dry1脚本实写。本review保留前两轮及补核历史；本PASS只评当前proposal，不代表落地验证完成。

仅评 proposal，不代表 Ghidra 落地、构建或 byte-identical 验收。本 reviewer 未修改 proposal、执行 JSON、源码、数据库或进度，未 build/stage/commit。未分析 Seg-10。

## 输入与独立核验边界

- 范围：`asm/12_equip_activation_scan.s` `[0x0809b178,0x0809c3d8)`，4704 字节。
- 当前第三轮 Proposal SHA256：`9c3892c87c14f6de87fa0a001d90d373f24a3a070e176d2107f31a23cf80265b`。
- 第二轮及补核输入 Proposal SHA256：`3e1e3deb92e298db42d1e97fb9b95e9c4756737a8d705955e1930c01f87e9601`。
- 首轮 Proposal SHA256：`1eddf1ed2d7898e67f1a6d5958ae32840373fa94867595eeed827e72296cece4`。
- 当前 asm12 SHA256：`73b53f32653e0bfa05e9814b567395c937a0f90876c466262582bdcde78dd4d3`。
- 原 ROM SHA1：`9689337d6aac1ce9699ab60aac73fc2cfdccad9b`。
- 当前 exporter SHA256：`a46f8efae54994e58f5b067a34f16f7fe751df46b155b67fd0449e6c53db9fdb`。
- `data/card-stats.s` SHA256：`efd868be69db67ed1338781e955aabe0d52ba1bf96dda2166edd80166be9199e`。
- 本地 `doc/um06-deck-modification-tool/data.md` SHA256：`641c56c373287b19efa36e27c5b00c3dcc74aa1368962b0eab48687f2d973c63`。

槽集合、字节覆盖、控制流编码、ref-scan、常量数值和 CID 映射从上述实际文件独立提取；未以 executor 的计数或 JSON 自检作为证明。定位三处 CID 错误后才查看其 `seg9-cid-evidence.json`，确认该文件的首轮版本也包含错误的反序字段命中；第二轮修复复核见末节。主线程 Ghidra 只读观测仅用于说明现有 Symbol 表示；当前 exporter 的判断分支另行读取并执行源码探针。

## P0

✅ proposal 存在且完整，执行表、消费者、常量目录、七个 ASCII plate 齐备，无禁止占位标记或零容忍用语。输入 hash 与委派值一致。

## 核验 (C1-C13)

| # | 检查 | 结果 | 证据与结论 |
|---|---|---|---|
| C1 | Rule1 地址序与范围 | ✅ | 活动文档 §五第283–285行给出 Seg-8 终点 b178、Seg-9 `[b178,c3d8)` 及下一段起点 c3d8。七入口与实际模块一致，无边界扩展。段外函数表仅检查本段直接消费者所需数据和既有入口名称。 |
| C2 | Rule2 裸块完整归类 | ✅ | 段内 ROM_INCBIN、`.incbin`、`.byte` 均0。2043个带地址项加28处 `.zero` 覆盖全部4704B。128个 `.hword` 均为实际 Thumb 高寄存器指令，不能误计成未分类数据。无遗漏 carve/disasm 块。 |
| C3 | Rule3 独立 ref-scan | ✅ | 全 ROM 逐字节扫描 raw 与 `addr\|1`；两张 switch 各1/0、段外表base 1/0，所有入口、内部尾和17个case另行扫描。没有 §5.1 提案项，也没有将有引用数据或已命名代码归入 §5.1。详见下表。 |
| C4 | R1 每槽值 | ✅ | 独立逐槽读取小端 u32：104 EQ、32 REF、21 RENAME 共157全部等于 ROM；17 switch表项和15个段外表项另读一致。所有scalar值及绝对base均保留原值。 |
| C5 | R1 复用 | ✅ | 全量解析22个 constants文件的5966个定义，全部求值成功、无重复定义名。14 NEW无现有同名/同值命中；54 REUSE为52常量+2既有switch标签，值全相等。重点同值域差异见后文。 |
| C6 | R2 命名与碰撞 | ✅ | 157个新槽名均匹配小写标识符规则，唯一且不与既有 asm/data/constants 名称碰撞；14 NEW 同样无碰撞。两张switch是既有名称复用，不计作新槽名：允许且要求复用原 Symbol 对象规范 namespace/name 为完整 GAS 名，不能另增同址标签。 |
| C7 | R3 可导出与引用 | ✅ | 第三轮#2已解决：21 RENAME明确保持operand0 DATA/DEFAULT主引用，USER_DEFINED属于目标LABEL；与实际诊断和exporter目标source判断一致。104 EQ/32 REF路径及switch/base表示不变。ModeB的B1/B2仍须在实写前实施并dry通过，属于实现验收条件。 |
| C8 | R5 现名与 plate | ✅ | 七 plate 标题均为当前七个函数现名；文本不含 FUN_/DAT_/DWORD_/PTR_。所引用 helper 名均存在，保留函数入口和内部尾边界。 |
| C9 | ASCII 与长度 | ✅ | 七 plate 长度448/466/402/395/436/371/464，全部ASCII且≤500；21 RENAME EOL、5附加 EOL、14 NEW定义注释均ASCII。附加EOL地址均落于既有分类槽。 |
| C10 | 指针/Thumb 位 | ✅ | 17 switch 项为偶地址，实际 `MOV pc,r0` 保持 Thumb 状态，禁止补1；外部表14项全部为既有 Thumb函数入口+1，随后NULL。仅给外表base建LABEL/引用，不改内部函数指针和NULL，不进行外段carve。 |
| C11 | 函数与全局语义 | ✅ | 七现名覆盖实际更新、扫描、驱动或布尔查询。b178恒返回0；bebc按存储step的unsigned >8返回完成；bfd4使用全局当前player、不读取入参。内部尾依赖原frame，未创建leaf函数。无需FUNC_RENAME。 |
| C12 | R6 消费者与可追溯证据 | ✅ | #1 CID证据修复保持，35具名CID/71记录结论有效；#2的21条EOL、251行保留规则和544行说明已正确区分DEFAULT引用与USER_DEFINED目标LABEL。逐地址对照完整诊断一致，七函数消费者语义未变。 |
| C13 | 全自动槽覆盖 | ✅ | 实际134 DAT+23 PTR=157；PTR由21个gP1LifePoints池+2switch池组成，DWORD/UNK=0。提案104EQ/32REF/21RENAME互斥并恰好覆盖，漏项/额外/重复/越界/无池加载槽均0。 |

## 独立测绘与字节证据

| 入口与现名 | 函数区间 | 字节 | 自动槽 | 直接BL入度 / ROM Thumb指针命中 |
|---|---|---:|---:|---|
| update_equip_activation_display_state | `[0809b178,0809b7e0)` | 1640 | 39 | 0 / 1 |
| update_equip_zone_sprite_by_state | `[0809b7e0,0809bdfc)` | 1564 | 55 | 0 / 1 |
| scan_equip_chain_slots_for_attr_enqueue | `[0809bdfc,0809be70)` | 116 | 3 | 0 / 1 |
| advance_equip_display_phase_via_table | `[0809be70,0809bebc)` | 76 | 4 | 3 / 0 |
| tick_equip_phase_display_by_state | `[0809bebc,0809bf60)` | 164 | 9 | 0 / 0 |
| check_field_allows_new_equip_action | `[0809bf60,0809bfd4)` | 116 | 3 | 1 / 0 |
| dispatch_equip_action_sprite_by_phase_state | `[0809bfd4,0809c3d8)` | 1028 | 44 | 0 / 1 |

实际共1869个指令项、3952指令字节；174个 `.word` 共696字节，其中157池槽、17已有switch项；28处零对齐共56字节。合计4704字节，无地址缺口、重叠或越界，显式原字节与ROM相同，零对齐字节实际也为0。最后 c3d6 的2字节对齐在核验范围内。

独立解码171条PC-relative LDR，目的池地址与汇编符号解析结果全等；353条直接控制流含160条条件分支、86条B、107条BL，目标与ROM编码全等，条件分支助记符也逐项匹配。128个高寄存器 `.hword` 中仅 b806/c020 写PC，两者编码均0x4687。所有157槽均存在本段实际LDR消费者。

BL入度对25个实际模块的指令行扫描：be70的3调用在 asm12:16841、asm13:1839、asm15:9717；bf60唯一调用在 asm12:17008。仅计调用点，不将注释或池指针算作BL。

### 全ROM ref-scan

使用完整ROM逐字节查找4字节小端值，不只按4字节对齐抽样；raw与Thumb值分开计算。

| 被扫描地址 | raw命中位置 | addr\|1命中位置 |
|---|---|---|
| 0809b814 | 0809b810 | 无 |
| 0809c038 | 0809c034 | 无 |
| 09e5aaec | 0809bea4 | 无 |
| 0809b178 | 无 | 09e5ab18 |
| 0809b7e0 | 无 | 09e5ab1c |
| 0809bdfc | 无 | 09e5ab20 |
| 0809be70 | 无 | 无 |
| 0809bebc | 无 | 无 |
| 0809bf60 | 无 | 无 |
| 0809bfd4 | 无 | 09e5aac4 |
| 0809b7c6 / 0809bde6 / 0809c3ca | 各无 | 各无 |

switch@b814的9个目标为 b838/b850/b9e0/ba30/baa8/baf8/bb60/bc04/bca4；switch@c038的8个目标为 c058/c108/c1ac/c1f4/c2d0/c338/c38c/c3a8。每个目标raw恰1且位置为其表项，Thumb命中全0，无重复目标。表原值、对应case入口和消费者 `MOV pc,r0` 均核实。

外表 `[09e5aaec,09e5ab28)` 的15项原值依次为：

```text
080977a1 08097829 08097c2d 08098265 080984d1
08098565 08098a89 08099315 08099aad 08099e0d
0809a1a5 0809b179 0809b7e1 0809bdfd 00000000
```

14个非零值逐项验证等于 proposal 所列当前函数入口+1，不修改表值。`invoke_r1` 实际为 `bx r1`（asm/23_sound_cardlist_libc.s:15338），与这些奇数指针吻合。表base符号化直接服务于本段bea4池，未展开表指向的其他函数体或建立外段carve。

## 常量、基址与CID证据

14个NEW均从实际ROM槽核值，并对5966个现有定义求值后查重：

| 新名 | 值 | 独立语义核验 |
|---|---|---|
| GOBLIN_ATTACK_FORCE_CID | 00001419 | card_0900、stats:11715、data.md:886，密码78658564；asm12:16051送r2，r3=0x22才是mode。 |
| RECKLESS_GREED_CID | 00001548 | card_1131、stats:14718、data.md:1116，密码37576645；phase0链门控值。 |
| AXE_DRAGONUTE_CID | 00001993 | card_2010、stats:26145、data.md:1988，密码84914462；配对上下文CID比较值。 |
| RED_MOON_BABY_ACTIVATION_PACKED | 00501415 | CID1415与00500000组合，player符号位随后OR。 |
| HELPOEMER_ACTIVATION_PACKED | 004e1571 | CID1571与004e0000组合。 |
| MAHARAGHI_ACTIVATION_PACKED | 025014fd | CID14fd与02500000组合。 |
| MAGICAL_BLAST_ACTIVATION_PACKED | 004e1984 | CID1984与004e0000组合。 |
| FAIRY_BOX_CID_SHIFTED | 9fc80000 | `(13f9<<19)&ffffffff`，slot word左移后等值比较。 |
| MAGICAL_BLAST_CID_SHIFTED | cc200000 | `(1984<<19)&ffffffff`，4字节数组元素左移后等值比较。 |
| TRIGGER_OP_PARAM_133 | 00000133 | asm11:30568先r2=r1，30576–30579以op31派发；不是卡CID或内存offset。 |
| EQUIP_PHASE_DISPLAY_STATE_OFF | 00001d94 | 从gP1LifePoints寻址外层state，与step1d28/active1d2c分离。 |
| SPRITE_ATTR_DUEL_PHASE_P2_0C | 0000800c | 非零侧sprite记录代码0c加bit15，与0c分支成对。 |
| gEquipChainActivePhase | 0201e20c | LP+1d2c = field+1cfc，同一u32共享phase。 |
| equip_display_step_fn_table | 09e5aaec | 14个奇函数指针加NULL的表base；REF目标是数据LABEL。 |

实际数组基址与域语义：

- `PLAYER_BLOCK_STRIDE=0x868` 用于两侧player块；chain context偏移是 `chain+0x2c+player*0x38`；field/activation记录步长是0x14，未混用。
- `gDuelFieldSlots=0201c510`，`gP1LifePoints=0201c4e0`，相差0x30。`field+1cf8=LP+1d28=0201e208`；`field+1cfc=LP+1d2c=0201e20c`。
- 1cfc既有 `DISP_SET_VARIANT_OFF` 用LP基址会到0201e1dc；本段bb46的r6是未偏移field基址，故复用 `EQUIP_CHAIN_ACTIVE_FROM_FIELD_OFF` 正确，不采用同值异域名称。
- 0201e1c8既有 `gEquipZoneCountTable` 与 `EQUIP_ZONE_COUNT_TABLE` 同值。此处读取首word作当前player并xor遍历，REF复用既有全局名，EOL准确限定读法，没有将本段行为说成计数数组。
- `gP1HandSlotArray=0201c8f8=LP+418`；本段按4字节扫描，count是LP+14。`0201c8f8+fffffbfc (mod 2^32)=0201c4f4`，复用 `HAND_ARRAY_TO_COUNT_NEG_OFF`；不是0201c4ec的zone count。两处EOL纠正历史全局名所不能完整表达的具体用途。
- 801b/8023/8028分别复用既有sprite属性常量，paired代码为1b/23/28。14个NEW没有与这些现有常量同值重建。

四个packed值由 asm05:8043–8079入口实际转发，再由 asm06:18682–18753构建记录。特别独立读取 `0804c940` ROM=0000ffff，wrapper实际取得low16 CID及bit31；现有旧plate写low13不能覆盖ROM事实，未因此提出段外修改。packed分量 `(bits22:21,bits20:16,bits30:25)` 依次为 `(2,16,0)/(2,14,0)/(2,16,1)/(2,14,0)`，与实际mask/shift/strb/strh一致。

从当前卡表独立枚举全部5170记录（包括零记录宏），每个slot字段与 `098169b8+22*i` ROM halfword相等。36个相关CID中，35个具名CID共71条匹配记录，所有匹配记录的ROM字段、卡名与密码闭合；14 NEW中的3个基础CID密码如上。CID11ed在全5170记录和data.md的正确CID列均0命中，映射表对应halfword也为ffff，保留 `eval_gap_cid_11ed` 中性名称合理。首轮三处错误仅在引用行号及其采样列，不改变上述数值/名称结论；第二轮已修正，完整复核结果见末节。

## 七函数 plate/现名独立判断

- `update_equip_activation_display_state`（asm12:15021–15866）：r0侧保存在r6；phase0执行上下文与链检查后推进，phase1队列code1e。phase-six gate选择step12；BLS门控选择step2并reset；其他phase选择step1/reset。全部返回路径r0=0。b7c6回收14局部栈并恢复r8–r10和低寄存器，不能另立leaf。
- `update_equip_zone_sprite_by_state`（15869–16656）：b7ec编码4682确为 `mov r10,r0`；9case包含对应卡扫描与重试。默认分支由入口r4=LP/r6=phase_ptr直接到达，查询11ed；缺失返回1，存在则排队并清step/phase返回0。bde6回收10局部栈并恢复r8–r10。新plate未将迭代中重用寄存器带入默认路径。
- `scan_equip_chain_slots_for_attr_enqueue`（16662–16714）：r0保存r8，r9是常量1；双方field槽5..9，与FAIRY_BOX移位值作等值比较，命中enqueue。phase-six检查为0时给调用侧设置bit12，恒返回1。无mask语义。
- `advance_equip_display_phase_via_table`（16724–16764）：不检查index界限；NULL返回1；非NULL转发side，helper非零才清phase并step++，否则不推进；所有非NULL路径最终0。该返回契约与外表14项+NULL数据一致。
- `tick_equip_phase_display_by_state`（16773–16859）：r0侧/r1 extra_flag，state0设置step6/phase1、可选sprite和chain+14，再推进外state；state1调用表驱动后重新加载step，`CMP #8; BLS` 保留0，unsigned >8置1。不会把driver的返回值当作step。其余state返回0。
- `check_field_allows_new_equip_action`（16863–16919）：Yata链必须存在；本侧LP+stride+c计数、monster占用数、active equip数均须零；对侧两类Yata候选之一非零返回1，否则0。函数仅调用判定helper，不将count命名为lock flag。
- `dispatch_equip_action_sprite_by_phase_state`（16923–17445）：输入寄存器未使用，r6从LP+1ce8取侧，按LP+1d1c状态0..7派发。phase0阻塞分支返回1；phase2可返回0重试，缺节点时推进后落入phase3；phase4按条件跳到7/6/5，phase5依据eligibility字段前进或回退；phase6/7完成工作后推进并返回0；phase>7返回1。c3ca恢复本frame的r8/r9与低寄存器，不建立共享尾函数。

以上已结合原指令及callee实际读取核对，旧plate中的返回或base叙述不作为证据。现有七函数名无需改动；R4/R7无新增disasm/carve，R8无图形辨识任务，R9无未声明语义缺口。

## C6/C7 可落地表示与验收条件

当前 `ExportRangeToGas.py:506–562` 读取outgoing主引用，再读取目标primary symbol；要求USER_DEFINED，ROM仅接受LABEL，使用非qualified `sym.getName()` 再sanitize。565–584提供data-equate fallback，612–617先symbol再equate。实际执行这些原函数的API替身探针，104个EQ及32个REF均得到对应提案名；这验证源码表示能力，不替代Ghidra持久化验收。

- b814旧对象id7217、c038旧对象id7144原为namespace中的短名。仅改source/primary会导出 `switchdataD_0809b814` / `switchdataD_0809c038`，与现有GAS名不一致。提案明确复用同一Symbol对象，将namespace设global并使用表列完整GAS名，之后USER_DEFINED/primary；不新增同址alias、不改case。模式B须校验原对象ID、地址、LABEL类型、允许的旧短名/已有完整名及全局同名冲突，再核对操作后ID未变、getName准确。
- 32 REF都需要显式检查operand0指向提案目标且DATA/USER_DEFINED/primary。对同目标原DEFAULT引用须精确重建，保留非目标和其他operand引用。不能把addMemoryReference调用成功当source提升证据。
- 09e5aaec当前为动态DEFAULT数据LABEL，首项080977a1不是表自身地址。新 `equip_display_step_fn_table` 是base USER_LABEL，bea4的word输出该名；`constants/ewram.inc`的新同值绝对equate由asm/rom.s:9 include解析。没有FUNCTION主符号rename、内部指针改值或段外carve；base位于ROM不妨碍绝对equate解析，现有输出器允许该LABEL路径。
- 21 RENAME保留现有 `.word gP1LifePoints` 及引用，仅更换本地池名/EOL。补核确认这些引用source是DEFAULT，USER_DEFINED属于目标LABEL；原提案及下文历史PASS未正确区分两者；第三轮已按#2纠正，ModeB仍执行B1保留检查。EQ设operand0 data-equate后必须确认没有旧的优先symbol遮蔽。落地验收须逐槽比较最终表达式，而不是只查名字存在。
- raw值、自动槽0残留、七plate、引用source及对象ID、所有25模块重导和ROM byte-identical属于随后fixer/主线程验收；本review不预称这些已经执行。

## 首轮修改清单（第二轮已解决，保留历史）

以下保留首轮给出的错误定位和可执行修正要求；目前没有未解决修改项。

### #1 — C12 — 按data.md的CID列修复三处反序字段误命中

`doc/dev/refine/F12-Seg-9.proposal.md` 的本地CID表应修改下列三格。卡名、CID、卡表记录、ROM地址、EQ/REF/RENAME内容与plate不变：

| Proposal行 / CID | 当前错误引用与该行实际卡 | 正确引用、CID和密码 |
|---|---|---|
| 509 / 0x1512 | data.md:512 为 The Thing That Hides in the Mud，正确CID列1215，反序列1512 | **data.md:1070**，After the Struggle，CID1512，pw25345186 |
| 521 / 0x1911 | data.md:333 为 Sanga of the Thunder，正确CID列1119，反序列1911 | **data.md:1880**，Cyber Archfiend，CID1911，pw59907935 |
| 522 / 0x1915 | data.md:1074 为 Ominous Fortunetelling，正确CID列1519，反序列1915 | **data.md:1884**，Indomitable Fighter Lei Lei，CID1915，pw84173492 |

对应实际完整正确行（来自本地data.md）：

```text
| 25345186 | After the Struggle | 5448 | 1512 | 1215 |
| 59907935 | Cyber Archfiend | 6444 | 1911 | 1119 |
| 84173492 | Indomitable Fighter Lei Lei | 6454 | 1915 | 1519 |
```

同步修正 `output/refine-run-20260831-194634/seg9-cid-evidence.json` 中上述CID的 `name_rows`：当前每个都同时含错误反序行和正确行；应仅保留正确CID列相等的记录。实际字段顺序是password/name/SO-code/CID/little-endian-CID；生成或修正证据时解析列，不对整行做CID子串匹配。对36个相关CID重新按正确CID列核验映射与密码，确保没有同类误匹配；若其他派生证据保存了错误行号，同步修正。此项无需改常量或消费者代码。

复审应比较proposal差异只涉及以上证据修正与必要说明同步，保留本轮输入hash及本清单；重新验证三条正确行及对应JSON，再记录新proposal hash。未变化的157槽、ROM/asm/constant输入与C1–C11/C13证据可沿用本轮实际核验结果。

## 第二轮独立复审与首轮问题闭环（原PASS历史记录）

本轮只重核证据修订及输入未变，不重复首轮已完成的353条分支解码或完整ref-scan。首轮已经真实核验的C1–C11/C13结论继续有效；C12本轮另从实际data.md、card-stats.s及ROM重新闭合。

### 版本与修订范围

- 首轮proposal备份 `output/refine-run-20260831-194634/seg9-proposal-round1.md` 的SHA256仍为 `1eddf1ed2d7898e67f1a6d5958ae32840373fa94867595eeed827e72296cece4`。
- 首轮review备份 `seg9-review-round1.md` 的SHA256为 `700ccd9d88846ba53e80521f90cdcaad71c92ae94e8a556a79976be35bd8a789`，与首轮交付一致；首轮verdict为NEEDS_FIX(1 item)。
- 当前proposal SHA256为 `3e1e3deb92e298db42d1e97fb9b95e9c4756737a8d705955e1930c01f87e9601`。独立按行和字节比较，只有509/521/522三行有差异：引用行号分别512→1070、333→1880、1074→1884，另外这三条编辑行的行尾由CRLF变为LF；其余554行的字节保持原样。该换行差异局限于三处文档证据行，不改变执行表或注释内容。
- EQ、REF、RENAME、附加EOL、PLATE、NEW、REUSE七节分别提取后与首轮文本完全相等。仍为157槽=104EQ+32REF+21RENAME、14 NEW、54 REUSE、7 PLATE；长度448/466/402/395/436/371/464，ASCII检查再通过。
- 当前asm12、ROM、card-stats.s、data.md、exporter hash与本review输入区首轮值完全一致。独立将22个 `constants/*.inc` 与 `pre-f12-seg-9/constants/` 预备份逐文件比较，全部byte-identical；因此首轮5966定义求值与命名碰撞/复用结果保持有效。
- 当前CID证据JSON SHA256：`4c5371b45c57326a1b2c7184fd5ef4bcf098bde9c47bea73d51f0c4360b2feeb`。首轮JSON备份SHA256：`ae48c8f1ee7876c4956e514b08ef261de3f38674495cae041081740c020c6fd3`。

### 按正确列独立重建映射

重新解析实际data.md五个字段 `password/name/SO-code/CID/little-endian-CID`，仅按第四字段的数值匹配；不使用executor的修复审计作为依据。新JSON全部36个CID及其顺序与首轮相同，各CID的 `name_rows` 精确等于实际正确列匹配集合。35个具名CID均各有1条正确名字行，11ed仍无匹配。

重新从card-stats.s提取相关全部71条记录，逐条验证JSON的record编号、header文本、来源行、ROM地址、ROM halfword；并按正确CID列核对名字和密码。所有值一致。新旧JSON所有 `cards` 内容及除 `name_rows` 外的字段完全相同，没有新增记录。

JSON仅删除以下5条记录；每条都满足“正确CID列不等于待查CID、反序列等于待查CID”，不是删除有效匹配：

| 待查CID | 删除行 / 错误卡名 | 该行正确CID | 保留的正确行 |
|---|---|---|---|
| 1415 | 1071 / Blast with Chain | 1514 | 882 / Red-Moon Baby |
| 1419 | 1883 / Giant Kozaky | 1914 | 886 / Goblin Attack Force |
| 1512 | 512 / The Thing That Hides in the Mud | 1215 | 1070 / After the Struggle |
| 1911 | 333 / Sanga of the Thunder | 1119 | 1880 / Cyber Archfiend |
| 1915 | 1074 / Ominous Fortunetelling | 1519 | 1884 / Indomitable Fighter Lei Lei |

1415和1419的proposal引用原本正确，保持未改；仅清理JSON中的额外反序命中，属于首轮#1要求对36 CID统一复查的范围。1512/1911/1915三条正确来源行与上文首轮清单所列原文、密码完全一致。无需改变CID名、常量、槽值或plate。

### 审计与结论

`seg9-mode-a-fix1.json` 与 `seg9-selfcheck.json` 的新proposal hash均正确；审计列明三格修正及五条清理，记录保留既有执行检查而非重跑，未宣称落地或构建。其所记36 CID/71记录与本轮独立结果一致。

首轮#1已全部解决；本轮未发现新的P0/C1–C13问题，无未完成修订项。PASS仅授权按该proposal进入随后模式B评估/落地，仍需遵守前文C6/C7的同Symbol对象、主引用source和最终表达式检查，以及fixer/主线程的持久化、重导及byte-identical验收。reviewer本轮只修改本review，未操作Ghidra、构建、stage或commit。

## 第二轮同一输入的落地前证据补核（历史记录，#2已于第三轮解决）

本次输入仍为SHA256 `3e1e3deb92e298db42d1e97fb9b95e9c4756737a8d705955e1930c01f87e9601`。补核前第二轮review SHA256为 `dcf0ff8e41c537ad00392d7d9750c9b581b6bf0816678d1f26149fa22412dff9`，原verdict为PASS。新增实际数据库观测揭示了原评审未核实的引用source事实，当前以该证据撤回进入实写的结论；不删除或改写上述第二轮CID修复历史。

### 新证据与独立交叉检查

- `seg9-dry.log` SHA256 `78a33e2d2e3f3790582b58694911e8d125a1f7a66d7387676815ad37745e5e37`：49行DATA4@09e5ab24失败，52–72行共21个RENAME_EXISTING_REF失败，73行汇总FAIL=22，之后在写入前抛出异常。
- `seg9-diagnose-preflight-complete.log` SHA256 `4e3c2dff34a8ae290bcf352792975a7c6259246f20b9b91acaab19a21dafd794`：48–89行完整枚举21池；91行目标LABEL信息；94行NULL定义状态；95行 `STATUS: DIAGNOSTIC READ ONLY DONE`。
- `tools/ghidra-labeling/RefineF12Seg9Slots.py` 补核时SHA256 `6d481312c240e1efaa61641b9f93c5dd09ad9be0a56ba6e281bce56ad6090623`。688行先执行preflight；689–690行在FAIL时退出；692行才开始apply事务。只读诊断脚本仅调用读取接口。首次不完整诊断的RAM读取异常不是NULL的证据，本次采用完整诊断；完整日志90行的RAM value=0是脚本占位，不据此判RAM运行值。
- `seg9-backup-recheck.json` 记录15数据库文件及49份source快照hash保持一致、apply未运行。reviewer未运行Ghidra；此项为落地执行者/主线程提供的环境一致性记录。

将proposal的21个RENAME地址与完整日志独立解析后作集合相等和逐字段比较：21/21全部为唯一主引用，`to=0201c4e0, operand=0, type=DATA, source=DEFAULT, primary=True`。其地址为：

```text
0809b700 0809b7d8 0809b808 0809b848 0809b9dc 0809ba2c 0809baa0
0809baf0 0809bbfc 0809bc9c 0809bea8 0809bed4 0809bf34 0809bfc4
0809c024 0809c2b0 0809c2f0 0809c318 0809c330 0809c3a0 0809c3c0
```

目标0201c4e0的主符号是 `gP1LifePoints`、id15545、LABEL/USER_DEFINED。引用source和目标symbol source是两个不同字段。当前exporter:527–562只选择引用目标并检查目标symbol source，不检查reference source；独立执行当前原函数的API探针，把reference.getSource设为不可调用，仍得到 `gP1LifePoints`。因此保留DEFAULT引用不会阻碍这21槽现有 `.word gP1LifePoints` 输出，也无需把它们转成REF操作。

外表末项09e5ab24在完整诊断中 `value=00000000, data=None, length=None`；当前ROM独立读取对应4B同为00000000。再次读出前14个非零项仍全为已核实的奇数函数指针。函数表的raw末项是4字节NULL，不意味着Ghidra已创建4字节Data对象。base09e5aaec的Data对象长度4、值080977a1；base自身是DEFAULT数据LABEL，不是FUNCTION。当前proposal只改base的LABEL和本段bea4引用，不要求定义末项数据。

### #2 — Mode A / C7+C12 — 纠正21条RENAME引用source文案

这是本次唯一新增的proposal修订项，原#1继续保持已解决。

1. 修改proposal:252–272全部21条RENAME EOL，将错误的 `existing USER_DEFINED DATA reference` 改为真实保留契约。可直接采用以下82字符ASCII文本：

```text
gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.
```

2. 修改proposal:542同一错误叙述；在RENAME规则旁明确：21池保持 `.word gP1LifePoints` 和原operand0 DATA/DEFAULT主引用不动，目标LABEL是USER_DEFINED；不增加、删除、重建或提升这21条引用source。32个REF的DATA/USER_DEFINED新建/精确重建规则保持原样，不能套用于RENAME。
3. 同步 `seg9-plan.json` 的21条RENAME EOL和相关派生说明、selfcheck/proposal hash及修订审计；保留地址、值、槽名、分类和其他全部157槽操作不变。7 PLATE、14 NEW、54 REUSE、已修CID证据不改。不得用静默修改数据库引用的方式满足旧EOL。

### B1 — Mode B guard修正 — RENAME按真实DEFAULT状态保留

当前脚本:548–551把既有主引用source限定为USER_DEFINED，是根据错误提案文字生成的前置条件；在#2提案修复并复审通过后，fixer同步修正该guard：验证唯一主引用的目标0201c4e0、operand0、DATA、DEFAULT及primary=True，并独立确认目标主LABEL仍为gP1LifePoints/USER_DEFINED。RENAME的apply块:622–626仅改池LABEL和EOL，继续禁止调用引用重建逻辑。

现有 `all_refs` 已包含from/to/operand/type/source/primary全部字段；preflight:546保存的快照和postcheck:645–647完整相等检查应保留，保证非主引用等其他引用也不变。不能将guard简单删除而失去实际保留状态验证。随后还要检查21槽最终导出表达式均为 `.word gP1LifePoints`。

此项是#2在模式B中的实现同步，不新增槽分类，也不要求将21个DEFAULT引用升级为USER_DEFINED。

### B2 — Mode B guard修正 — 外表按原始字节与定义状态核对

当前 `verify_tables`:493–494对EXTERNAL_WORDS全部15项调用 `_check`；`_check`:425–428强制getDefinedDataAt存在且长度4，因此把原本未定义Data的NULL误报为DATA4。该要求超出proposal，无需修改表内容或carve计划。

fixer应把外表校验与本段157个池槽的definedData4校验分开：

- 对外表15个word从ROM映射只读获取u32并核对提案原值；继续核对14个非零值为Thumb奇指针、函数现名/入口一致，最后NULL=0。
- 在写入前记录外表区域现有Data定义的地址、长度和类型/范围，写入后核对定义状态相等；09e5ab24的 `getDefinedDataAt=None` 必须保持，不要求其变为definedData4。对外表已有引用也保持不动；允许的变更仅为proposal指定的base LABEL及段内bea4到base的引用。
- 不得createData/disassemble/clearListing或carve NULL；不改全局 `_check` 去放宽本段157个既有池槽要求，也不改变现有17个switch表项检查。

这是实现guard过强，C4/C10的提案原值和Thumb位结论仍通过，不登记为第二个proposal缺陷。fixer修正脚本后先再次dry；dry通过也不替代随后事务postcheck、持久化核对、全段导出及byte-identical验收。

### 当前结论及下一轮边界

本次补核后C7/C12为失败，其余C1–C6/C8–C11/C13及已修#1保持原结论。当前待办为模式A的#2，以及之后模式B的B1/B2两处guard同步。应先完成#2，再用新proposal输入进行第三轮（最后一轮）完整复审；本次仍属第二轮同输入的证据补核，不计作新proposal第三轮，不新增第四轮。

reviewer只更新本review，未修改proposal、脚本、数据库、正式源码、进度，也未build/stage/commit。当前保持停写。

补核当时结论：NEEDS_FIX(1 item)。上述问题定位与B1/B2实现要求作为历史证据保留；当前正式结论见第三轮。

## 第三轮正式复审与#2闭环

本轮为最后一轮正式proposal复审，未增加第四轮。当前输入SHA256：`9c3892c87c14f6de87fa0a001d90d373f24a3a070e176d2107f31a23cf80265b`；上轮补核review SHA256：`00653dc416fc7af5dab9ccf78ea6a16aab0e2f76c22988e54729ac2a15e25cde`。`seg9-proposal-round2.md`备份hash仍为已审的 `3e1e3deb92e298db42d1e97fb9b95e9c4756737a8d705955e1930c01f87e9601`。

### 提案差异与实际source契约

独立比较当前proposal与round2备份，修改仅为#2要求的三部分：

1. 21条RENAME EOL全部替换为上文指定82字符ASCII句子，地址、槽名、分类不变。
2. 当前251行新增RENAME保留规则：保持 `.word gP1LifePoints` 与现有operand0 DATA/DEFAULT主引用；禁止新增、删除、重建或升级引用source；USER_DEFINED属于目标主LABEL。32个REF规则保持独立且不变。
3. 原542行说明现为544行，同步写明仅改槽名/EOL、保持DEFAULT主引用与USER_DEFINED目标LABEL，保留32 REF单独验收要求。

旧错误短语 `existing USER_DEFINED DATA reference` 在当前proposal中0命中。逐项检查P0标记、语义说明和ASCII内容，无新增问题。

再次从完整只读诊断逐条解析21条REF记录，其地址集合与当前RENAME集合完全相等；全部为0201c4e0/operand0/DATA/DEFAULT/primary=True。目标 `gP1LifePoints` 为LABEL/USER_DEFINED，数据源与新文字完全一致。诊断log hash仍为 `4e3c2dff34a8ae290bcf352792975a7c6259246f20b9b91acaab19a21dafd794`；NULL事实仍为09e5ab24原始00000000、definedData=None。

exporter未变，其source过滤发生在目标Symbol，不在Reference。补核执行原源码的探针已证明无需调用reference.getSource也能输出gP1LifePoints。新提案选择保留DEFAULT引用符合实际可导出路径，无需修改32 REF规则或重分类RENAME。

### 执行计划一致性与未变证据

对 `seg9-plan-round2.json` 和当前 `seg9-plan.json` 递归比较，恰21个差异，全部为 `/slots/<index>/eol` 字段；其余start/end/functions/slots/newdefs/plates及每槽地址、值、原label、新label、kind、symbol、uses、定义来源完全相同。当前plan SHA256为 `7fd460b9b5b7e01c635a10e35c50ccf219f58e23f82a544c6d3aeeb32cfbd3ce`。

独立从proposal解析执行表，与plan及apply-plan逐项比较：

| 核验对象 | 第三轮实际结果 |
|---|---|
| EQ / REF / RENAME | 104 / 32 / 21，唯一地址合计157，无地址/值/名字/分类变化 |
| 157槽ROM u32 | 本轮再次读取，全部与当前proposal/plan相等 |
| RENAME EOL | 21条均为指定82字符ASCII文本，apply-plan与proposal逐条相等 |
| PLATE | 7条逐字未变，长度448/466/402/395/436/371/464，均ASCII且≤500 |
| 附加EOL | 5条地址/文字未变，apply-plan与proposal逐条相等 |
| NEW / REUSE | 14 / 54未变；apply-plan的14个定义名、值、路径、注释逐项相等 |
| switch / 外表 | 17个偶地址switch项、15个外表word均与本轮实际ROM再读一致 |
| 已修CID证据 | JSON hash仍为 `4c5371b45c57326a1b2c7184fd5ef4bcf098bde9c47bea73d51f0c4360b2feeb`，第二轮35具名CID/71记录及5条误匹配清理结论保持 |

当前 `seg9-apply-plan.json` SHA256为 `31c512285496759d847c9c833adf361d6c49d53b66148abebe4611234f374835`。其slots去除明确派生的new_label后与plan完全相等，eq/ref/rename、plates、extra_eol、new_definitions均与proposal一致；`proposal_sha256`准确。apply-plan同时明确旧脚本/生成器仍是dry1产物，尚未重新生成，要求本轮PASS后执行B1/B2，没有将旧脚本当作已匹配当前输入。

`seg9-selfcheck.json` 和 `seg9-mode-a-fix2.json` 的proposal hash均指向本版；审计记录21 EOL和规则/说明修正，声明此前执行检查为沿用，未宣称重跑构建或已写数据库。独立差异检查与其21字段限定一致，不以其自检布尔值替代本轮验证。

当前asm12 SHA256仍为 `73b53f32653e0bfa05e9814b567395c937a0f90876c466262582bdcde78dd4d3`，ROM SHA1仍为 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`；card-stats.s、data.md、exporter hash亦与前轮相等。22个constants文件再次与pre-f12-seg-9快照逐文件字节比较，全部未变。因此保留首轮实际测绘4704B、全ROM raw/Thumb扫描、353分支解码、5966定义复用/碰撞检查、函数语义与全部自动槽覆盖证据；本轮不虚报重做未变控制流分析。

### 完整门禁结论与落地前置条件

P0及C1–C13当前全部通过。C1/C2/C3沿用未变范围、裸块全覆盖和独立ref-scan；C4本轮重读157槽及32表项；C5/C6依据未变常量/标签计划和既有全量检查；C7以实际Reference与Symbol区分重新通过；C8/C9核对原七plate及更新后的21 EOL；C10确认原Thumb/NULL字节不变；C11保留七函数语义判断；C12的#1/#2均闭环；C13仍为134 DAT+23 PTR完整覆盖157槽。

没有未解决的proposal修改项。B1/B2是必须完成的ModeB实现工作，不因脚本尚未更新而判当前proposal失败，也不允许绕过：

- **B1**：按本版EOL重生成脚本，RENAME preflight核DEFAULT引用及USER_DEFINED目标LABEL，apply只改池名/EOL，完整all_refs前后不变；32 REF继续USER_DEFINED主引用规则。
- **B2**：外表检查读取15个原始word并保持Data定义/引用状态，NULL继续definedData=None；本段157池及17 switch的原有definedData检查不放宽，不新建NULL Data、不扩carve。
- 更新脚本后先只读dry，全部前置检查通过再允许实际apply；随后事务postcheck、数据库持久化检查、全段导出检查与ROM byte-identical由fixer/主线程执行。旧dry1脚本不得直接实写。

本轮只修改本review；未修改proposal、计划、工具、正式源码、数据库、进度，未build/stage/commit，未预析Seg-10。

## Reviewer Verdict: F12-Seg-9 = PASS
