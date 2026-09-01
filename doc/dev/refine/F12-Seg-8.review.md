# Refine Review: F12-Seg-8

## 输入与边界

- 日期：2026-08-31；首轮独立评审，Sol + xhigh。
- 范围：`[0x0809a1a4,0x0809b178)`，`0xfd4 = 4052` 字节。
- proposal：`doc/dev/refine/F12-Seg-8.proposal.md`，SHA256 `2606ce4d5862f3f2e02171a2e22acb7ca869a56e568158a859013f5690307229`。
- 模块：`asm/12_equip_activation_scan.s`，SHA256 `6e4d94729f11e3c7607587db954db62fa7b5aa2d444baae927cac8c0ad503591`。
- 原 ROM：`roms/2343.gba`，SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`。
- exporter：`tools/asm-regen/ghidra/ExportRangeToGas.py`，SHA256 `a46f8efae54994e58f5b067a34f16f7fe751df46b155b67fd0449e6c53db9fdb`。
- 按 AGENTS.md、refine-loop skill、方法论和 reviewer C1-C13 执行。所有扫描、数值和消费者结论从实际 asm、ROM、constants 独立取得，未将 executor JSON 或自检结论用作替代证据。Seg-7 的 PASS 不自动继承到本段。
- 本轮仅写本 review，未修改 proposal、执行 JSON、Ghidra、asm、constants、进度或工具；未 build/stage/commit。本结论评定 proposal，不宣称已完成落地或 byte-identical 验收。

## P0

✅ proposal 存在、非空，三执行表、三条完整 plate、NEW/REUSE 和数据块分类齐备。全文零容忍词扫描 0 命中，无中止标记。

## 核验 (C1-C13)

| # | 检查 | 结果 | 独立证据 |
|---|---|---|---|
| C1 | Rule 1：地址序与路线图 | ✅ | 活动文档 `doc/dev/p5-refine-12-equip-activation-scan.md:266` 的 Seg-7 终点、`:267` 的 Seg-8 起止、`:268` 的 Seg-9 起点连续。本段为 1 主入口和 2 既有共享收尾，131 实际槽已计入路线图；未越界或遗漏无 push 的尾入口。 |
| C2 | Rule 2：数据块归宿 | ✅ | 独立全段扫描 ROM_INCBIN/.incbin/.byte 均为 0。1785 个显式地址项加 33 处 2 字节 `.zero` 覆盖 4052 字节；缺口、重叠、越界、ROM 字节差异均为 0。71 条 `.hword` 均为已有 Thumb 高寄存器操作。 |
| C3 | Rule 3：独立 ref-scan | ✅ | 对主入口及两共享尾分别重跑全 ROM 任意字节位置的 raw 与 addr\|1 扫描。主入口 raw=0/thumb=1，唯一位置 `0x09e5ab14`；两尾 raw=0/thumb=0，但实际 BL 和自然续接已核对。没有裸块或 §5.1 项，不把共享尾误列为孤儿。 |
| C4 | R1：值准确 | ✅ | 95 EQ 逐槽原 ROM u32 与 value 相同；33 REF 原 u32 等于目标地址；3 RENAME 均为 `gP1LifePoints=0x0201c4e0`。11 NEW 定义及 47 REUSE 求值均与使用槽相符，无原数值替换。 |
| C5 | R1：全量常量复用 | ✅ | 独立解析 5955 条现有 `.equ/.set`，含十进制、十六进制、别名和表达式；5955 项递归求值成功，未解析/重名为 0。11 NEW 的值和名字在当前 constants 均无命中；47 REUSE 全部存在且同值。重要同值域与基址的选择见下文。 |
| C6 | R2：新名与碰撞 | ✅ | 131 个 slot_label 全部匹配 `^[a-z][a-z0-9_]+$`，彼此唯一，与当前 asm 标签、constants 无碰撞；11 NEW 名称也无碰撞。旧 `cid_13b0` 实为 `0x08052114` 池标签，提案改用 `equip_pair_cid_13b0=0x13b0` 后定义及两个 EQ 槽一致，无常量/地址混淆。 |
| C7 | R3：引用接通与导出 | ✅ | 33 REF 均为 RAM，明确 USER_DEFINED LABEL 主符号和 operand0 DATA/USER_DEFINED；明确精确移除/重建同目标 DEFAULT 引用并保留非目标及其他 operand。当前 exporter 原函数的只读对象状态探针中，95 EQ、33 REF 全部返回计划名字。3 RENAME 保留现有符号表达式。无 switch namespace 或 fn+1 依赖。 |
| C8 | R5：plate 用现名 | ✅ | 三条替换 plate 不含 FUN_/DAT_/DWORD_/PTR_；引用现名与当前函数和常量一致。仅替换三个指定入口的旧 plate，不改相邻段。 |
| C9 | ASCII 与长度 | ✅ | 三条 plate 分别 481/393/354 字符，全部 ASCII、均不超过 500。3 条 RENAME EOL 及 11 条 NEW equate 的代码/注释全部 ASCII。 |
| C10 | THUMB 指针 | ✅ | 本段没有 ROM 函数指针 literal 或 switch；独立检查所有 71 条高寄存器 `.hword`，没有 MOV pc。段外主入口表值为 `0x0809a1a5`，本提案不改。无 carve 条目需要加 1，不制造奇地址标签。 |
| C11 | 现名与实际职责 | ✅ | 主函数确实处理 paired context 的资格门控及随后的显示/激活，既有 eval 名没有绑定错误全局；新 plate 明确其三相位和副作用，未描述为纯 predicate。两个尾名描述其实际递增/恢复操作，plate 明确父帧和非 APCS 入口。无需以函数改名修正本段已识别的错误，详见命名边界说明。 |
| C12 | R6：消费者、输入与返回 | ✅ | 通读整个主函数和两尾，核对 0x38 context、0x14 临时 record、0x48 局部帧、两个相位基址、负偏移、descriptor/payload/type22、41 CID、69 处 CID LDR 以及三条 BL 收尾契约。关键证据均有具体地址/行号，置信度 high。 |
| C13 | 自动槽全覆盖 | ✅ | 独立扫描实际集合为 118 DAT + 10 DWORD + 3 PTR = 131；95 EQ/33 REF/3 RENAME 互斥并集恰等于该集合。遗漏、额外地址、重复、越界均为 0；每个槽都有本段 PC-relative LDR 消费者。 |

## 测绘、引用与完整控制流

| 入口 | 模块位置 | 实际身份 |
|---|---|---|
| `0x0809a1a4` eval_equip_slot_pair_eligibility | `asm/12_equip_activation_scan.s:12903` | 主入口，建立保存帧与 0x48 字节局部空间，执行 phase0/1/2 |
| `0x0809b146` increment_counter_at_ptr | `asm/12_equip_activation_scan.s:14990` | 四条指令的共享相位递增前缀，无独立栈帧 |
| `0x0809b14e` restore_callee_high_regs_from_frame | `asm/12_equip_activation_scan.s:14997` | 使用主入口栈帧返回原 caller 的既有共享尾 |

独立扫描 `asm/12_equip_activation_scan.s:12904` 至 `:15018`：

- 显式地址项 1785；对齐块 33，每块 2 字节，ROM 中全部为零；覆盖集合与 `[0x0809a1a4,0x0809b178)` 完全相等。
- 71 条 `.hword` 均为 `0x46xx` Thumb 高寄存器指令；所有目的寄存器解码中没有 MOV pc。BL 收尾之后的 `0x0000` 对齐指令及池仍保留原表示，不新建函数。
- 独立从原始 ROM 解码 141 条 literal LDR，目标全部等于实际槽标签地址；131 槽均至少有一次本段使用。
- 独立从原始 ROM 解码 394 条 B/BL，全部命中实际 asm 目标；216 条条件分支的 condition code 与助记符逐条一致。
- 10 个 DWORD 槽独立定位为 `0x0809a330/334/338/33c/340/3dc/3e4/7e0/7e4/7ec`；它们均已计入三执行表，未只扫描 DAT 而漏计。

全 ROM 扫描未限制指针对齐，raw 和 addr\|1 分开统计：

| 目标 | raw 位置 | THUMB+1 位置 | 直接控制流 |
|---|---|---|---|
| `0x0809a1a4` | 无 | `0x09e5ab14`，值 `0x0809a1a5` | 25 个正式模块中无直接 B/BL 进入 |
| `0x0809b146` | 无 | 无 | BL `0x0809a3d6`、`0x0809a7da`；从 `0x0809b144` 自然续接 |
| `0x0809b14e` | 无 | 无 | BL `0x0809a32c`；从 `0x0809b14c` 自然续接 |

因此 Rule 2/3 的 carve、disasm、§5.1 均为空集合是有据结论；两个尾不具有原始指针不影响其已证实的控制流入口身份。

## 共享收尾与三条 plate

下列结论置信度 high。

主入口 `:12904` 先保存 r4-r7 和原 LR，再把 r8/r9/r10 分别移入 r5/r6/r7 后 push，最后 `sub sp,#0x48`。相对于主入口原 SP，局部帧底为 SP-0x68；其 `+0x48/+0x4c/+0x50` 保存原 r8/r9/r10，`+0x54..+0x60` 保存原 r4-r7，`+0x64` 保存原 caller 返回地址。

`0x0809b146` 的 `ldr r0,[r1] / adds r0,#1 / str r0,[r1] / movs r0,#0` 递增 r1 指定的相位字并设返回值 0。三个前驱均构造 `gP1LifePoints+EQUIP_CHAIN_ACTIVE_OFF`：`:13191` 至 `:13194`、`:13727` 至 `:13730`、`:14985` 至 `:14987`。其后自然进入 `0x0809b14e`。

`0x0809b14e` 至 `0x0809b15c` 执行 `add sp,#0x48`，pop r3-r5 后恢复 r8-r10，再恢复 r4-r7，最后 pop r1 并 bx r1。该尾不写 r0，使用的是主入口保存的 caller 返回地址；BL 写入的新 LR 没有被读取：

| BL 地址 | ROM 解码目标 | 新 LR（不作为最终返回地址） | 传入/最终 r0 |
|---|---|---|---|
| `0x0809a3d6` | `0x0809b146` | `0x0809a3db` | 前缀设为 0 |
| `0x0809a7da` | `0x0809b146` | `0x0809a7df` | 前缀设为 0 |
| `0x0809a32c` | `0x0809b14e` | `0x0809a331` | 前驱设为 1，尾保持 1 |

这支持两条尾 plate 的原 caller、父帧依赖、非独立 leaf/APCS 入口和 r0 保留约定。不能把 BL 之后的池或对齐当成返回执行路径。

主函数 plate 的状态说明亦与实际代码一致：

- 输入 r0 保存到 sp+0x1c；chain+4 保存到 sp+0x20。context 地址以 chain+0x2c 为基址，通过 `(side*8-side)*8` 形成 0x38 步长，另一 context 使用 `1-input_side`。证据 `:12910` 至 `:12928`。
- `chain[+8] != 0` 进入 `0x0809a32a` 设 r0=1，再 BL 返回尾。否则 `:13096` 至 `:13106` 从 gDuelFieldSlots+0x1cfc 读取 phase，phase0/1/2 分别到 `0x0809a344/0x0809a3e8/0x0809a7f0`，其余也返回 1。
- phase0 对两侧进行 card eligibility 门控；Thunder Nyan Nyan 与由 `0x13a4+0xd6` 得到的 Mystical Beast Serket 分支写 context[+0x30]=1。`:13031` 至 `:13032` 已把常量 1 放入 r9，`:13141` 至 `:13153` 写入的不是 slot_idx；另一侧直接 movs 1。`asm/11_effect_slot_puzzletext.s:20791` 至 `:20833` 的 callee 实际返回 0/1，也未提供 slot index。phase0 最后共享递增返回 0。
- phase1 的 sp+0x30/sp+0x34 门控分别覆盖两侧 card-specific enqueue、type11、ID lookup 和 equip sprite 显示；两侧路径最终汇合到 `0x0809a7d4`，BL 共享前缀后返回 0。证据 `:13202` 至 `:13731`。
- phase2 从 increment_lp_bar_display_counter 开始，根据 context[+0x30]/[+0x2c] 路径排 bitmap、构造临时显示记录或 descriptor，执行 type22 activation、两条 node 链遍历和 slot5..9 扫描。所有普通路径最终到 `0x0809b13c` 调用 decrement，再自然续接共享相位递增并返回 0。证据 `:13740` 至 `:15005`。

保留现名的边界：`eval_equip_slot_pair_eligibility` 仍指本体实际处理的 paired equip 资格逻辑，未绑定 gDuelBattleState 等错误全局；新 plate 明示它是有相位推进、显示和激活副作用的处理过程，其返回值表示本阶段完成而非资格真假。两个尾名所描述的递增/寄存器恢复动作均存在，plate 补足严格的父帧契约。本段没有必须通过 FUNC_RENAME 修复的全局或对象误名；不据此把这些入口视为普通可自由调用的函数。

## 常量用途、基址与新增全局

全量 5955 定义求值结果：11 NEW 无同名、无同值既有定义；47 REUSE 全部值一致。按实际消费者再核验重要同值项，结论置信度 high：

| 对象 | 实际消费者与复用判定 |
|---|---|
| gDuelEffectChainSlotsSecond | 槽 `0x0809a330` 原值 `0x0201bc68 = gDuelEffectChainSlots(0x0201bc54)+0x14`。`:12988` 至 `:12992` 为另一 context 选择此记录；`:13014` 至 `:13027` 取该记录首半字低 13 位判断非零，与第一记录检查对称。第一记录亦由 chain+0xc4 派生。context 与输入侧/另一侧绑定是运行时选择，不能给第二记录固定 player1/player2 含义。NEW 注释正确限定为第二条 fallback record。 |
| EQUIP_CHAIN_ACTIVE_FROM_FIELD_OFF | 槽 `0x0809a340=0x1cfc` 的真实基址为 gDuelFieldSlots，结果 `0x0201e20c`。同值 `DISP_SET_VARIANT_OFF` (`constants/duel_field.inc:253`) 属于另一基址；选用 `EQUIP_CHAIN_ACTIVE_FROM_FIELD_OFF` (`:575`) 正确。 |
| EQUIP_CHAIN_ACTIVE_OFF | `0x0809a3e4/0x0809a7ec/0x0809b174=0x1d2c` 各与 gP1LifePoints 配对，亦得到 `0x0201e20c`。读取 phase 和递增 phase 是同一地址，两个 offset 不可混用。 |
| NODE_POOL_NEG_OFFSET | `0x0809aaf8/0x0809aec4` 均为 `0xffffeb50`，二补数值 -0x14b0。`:14105` 至 `:14108`、`:14615` 至 `:14618` 的 gEquipNodePool+该负偏移模 32 位结果均为 `0x0201c510`。同值现有定义唯一为 `NODE_POOL_NEG_OFFSET` (`duel_field.inc:144`)。保留 base 和负偏移两个原槽，不以 field base 替换其中一个值。 |
| field/node 结构 | 现场记录以 `(side&1)*0x868+slot*0x14` 索引 gDuelFieldSlots；slot+0xa 读链首，node 以 index*8 索引 gEquipNodePool，node+6 读 next，node+2 低 nibble 筛 10/11。并行 state 指针为 gDuelFieldSlotState=gDuelFieldSlots+0x10。证据 `:14057` 至 `:14234`、`:14567` 至 `:14760`，支持各 RAM REF 名。 |
| EQUIP_PAYLOAD_LOW9_MASK | `0x0809a8e0/0x0809ac98=0x1ff` 从 context[+0xc] 取 entity 低 9 位，拼成 descriptor，并作为 r2 extra_payload 传入 activation wrapper。复用同域 EQUIP_PAYLOAD_LOW9_MASK，不采用 demo/scrollbar/OAM x 的三个同值名称。 |
| descriptor 位掩码 | `0xffffbfff` 清 bit14 后插入 context[+8] bit0；`0xff87ffff` 清 bits22:19 后置 `0x700000`，卡号和资格分支可扩为 `0x780000`。其余 descriptor 位包括 side bit9、slot bits13:10、bit15/16/17 置 1、另一侧 bit18。证据 `:13781` 至 `:13905`、`:14282` 至 `:14407`。复用两个已有位掩码，不新增重复定义。 |
| SPRITE_LOW_HALF_MASK | `0x0809aeb0=0xffff` 在 `:14552` 至 `:14554` 保留 r4 卡 ID 低半字后 OR 到 packed activation word；对应另一侧 `:14043` 的 ldrh context[+0x10]。不使用同值空卡、隐藏标记或 count cap 名。 |
| EQUIP_ACTIVATION_PACKED_TYPE22 | 四槽 `0x0809aae4/0x0809abd0/0x0809aeac/0x0809b01c=0x2c200000=(22<<25)\|(1<<21)`；实际传入 apply_equip_activation_with_id_lookup。`asm/06_equip_eligibility_b.s:18716` 至 `:18727` 把 bits22:21 映射到 record+3 bits5:4，`:18738` 至 `:18746` 把 bits30:25 映射到 record+2 bits11:6，得到 1 和 22。 |
| wrapper payload | `asm/05_equip_eligibility_a.s:8043` 至 `:8061` 保存 r2，解析/保留 entity_id 后将 r2 原样转发给 apply_equip_activation_via_packed_attr。本段 descriptor 与 extra_payload 域关系有直接代码依据。 |
| gEquipZoneCountTable | `0x0809b028=0x0201e1c8` 同值有 EQUIP_ZONE_COUNT_TABLE 和 gEquipZoneCountTable；这里是绝对 RAM 指针，选既有 USER label 并建 DATA-ref。`:14768` 至 `:14811` 读其首字 XOR 0/1 选两侧，再遍历 slot5..9。不把绝对地址作为 offset。 |
| 既有 CID 名复用 | `0x1836` 的唯一现有常量 EQUIP_ELIG_EXCL_B 与 card-stats 的 Fox Fire 相符，两槽新标签明确 fox_fire_cid；`0x15d1` 复用 cid_15d1_zombie_tiger。没有仅为命名风格另建重复常量。 |

NEW 分配为 card_info 9 项（8 个具名 CID 和 1 个中性 CID）、duel_field 1 项、ewram 1 项，共 10 常量和 1 全局；不新增 include。

## CID 与常量/地址碰撞核对

独立读取 proposal 的 41 行 CID 使用表，再以实际源文件及 ROM 核验：40 个具名值、1 个未分配值，69 处消费者 LDR。每个消费者的 PC-relative 目标及该目标的原始 u32 与该 CID 一致，未把算术派生值当作 literal 原值。

- ID 映射使用 ROM 偏移 `0x015b7ccc+(internal_id-4007)*2`；40 个具名值的 card 编号均与 `data/card-stats.s` 标题相符。
- card-stats 的原始 slot_id 读取偏移 `0x018169b8+card_id*22`。40 个值均相符，源 `.hword slot_id` 亦相符。该导出表从首记录 slot_id 开始，首个 zero0 在前一区域，不能额外加 2。
- 8 个新增具名 CID 的卡名、slot、card 编号和密码均与具体源标题相符；见下表。
- `0x13b0` 的原始 ROM 映射为 `0xffff`，`data/cards-ids-array.s:1050` 一致，完整 card-stats 无对应 slot；活动文档 `:34` 允许使用中性 ID。
- 独立定位 `asm/05_equip_eligibility_a.s:20492` 的 `cid_13b0`，其地址是 `0x08052114`，内容为 `0x13b0`。它不是数值 equate。新名 `equip_pair_cid_13b0` 与旧地址符号分离，在 NEW 与 `0x0809a408/0x0809a5fc` 两个 EQ 槽完全同步；未改旧段标签。`0x13b0-3=0x13ad` 仅为比较派生值，不另造 literal 槽。

| 新 CID | 值 | 本地来源 |
|---|---|---|
| SWORD_HUNTER_CID | `0x12a6` | `data/card-stats.s:8205`，card_0630，pw 51345461 |
| RIGRAS_LEEVER_CID | `0x13b4` | `data/card-stats.s:10857`，card_0834，pw 39180960 |
| GIANT_AXE_MUMMY_CID | `0x152c` | `data/card-stats.s:14393`，card_1106，pw 78266168 |
| WINGED_SAGE_FALCOS_CID | `0x1592` | `data/card-stats.s:15277`，card_1174，pw 87523462 |
| THOUSAND_NEEDLES_CID | `0x1658` | `data/card-stats.s:17279`，card_1328，pw 33977496 |
| DES_KANGAROO_CID | `0x16b7` | `data/card-stats.s:18254`，card_1403，pw 78613627 |
| NEEDLE_BURROWER_CID | `0x174b` | `data/card-stats.s:19853`，card_1526，pw 98162242 |
| ABSORBING_KID_FROM_THE_SKY_CID | `0x1792` | `data/card-stats.s:20529`，card_1578，pw 49771608 |
| equip_pair_cid_13b0 | `0x13b0` | `data/cards-ids-array.s:1050`，ROM 映射 `0xffff`，无 card-stats slot |

## C7：当前 exporter 路径与落地条件

读取当前 exporter 原函数，在只读内存探针中模拟提案规定的对象状态；不执行 Ghidra，不修改工具。

- `ExportRangeToGas.py:527` 至 `:562` 选择 primary outgoing ref（或首个 ref），查询目标 USER_DEFINED 主符号并输出 sanitize 后的短名。33 个 REF 均为 EWRAM 指针，拟用名字无需 namespace 拼接或字符改写，探针全部返回所列 gas_label。
- `:612` 至 `:617` 在 symbol 路径为空时进入 `resolve_word_equate`；95 个 EQ 按提案建立 data operand0 equate 后全部返回所列常量名。不存在必须依赖裸值回退、ROM FUNCTION 或 function+1 的槽。
- 三个 RENAME 槽当前已为 `.word gP1LifePoints`，其目标、引用与值保留；只改槽标签和 ASCII EOL。
- 真实 Ghidra 中必须满足所列 LABEL 主符号和 DATA/USER_DEFINED ref 条件；已有同目标 DEFAULT ref 要精确移除该 operand0 引用再重建，不能仅假定 addMemoryReference 自动升级 source。其他 operand/非目标引用须保留。
- exporter 使用其选中的引用，因此模式 B 须确认实际 primary 引用仍指向计划目标，并核查 from/to/operand/type/source、最终符号表达式及保存后的持久状态。只读探针不替代实际数据库验收；131 槽正式 asm/ELF 和全 ROM byte-identical 仍是后续落地门禁。

## 状态: PASS

P0、C1-C13 全部通过。没有需修订项；支持进入模式 B。当前结论仅针对本次 hash 对应的提案，不代表后续落地已通过。

## 修改清单

无。

## Reviewer Verdict: F12-Seg-8 = PASS
