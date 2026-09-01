# Refine Review: F12-Seg-7

## 输入与评审边界

- 评审日期：2026-08-31；首轮独立评审。
- 段：`[0x08099314,0x0809a1a4)`，`0xe90 = 3728` 字节。
- proposal：`doc/dev/refine/F12-Seg-7.proposal.md`，SHA256 `5463ac0f317237ce2af3e3c998a0bceb2f31af53e2179253a8e540d18e0df51d`。
- 模块：`asm/12_equip_activation_scan.s`，SHA256 `98fe66ac4fccf4d47e9133b0a856a52906d85e012f1d3e8390751a02e19b56ca`。
- ROM：`roms/2343.gba`，SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`。
- 当前 exporter：`tools/asm-regen/ghidra/ExportRangeToGas.py`，SHA256 `a46f8efae54994e58f5b067a34f16f7fe751df46b155b67fd0449e6c53db9fdb`。
- 已读取 AGENTS.md、refine-loop skill、完整方法论及 reviewer C1-C13 要求。本轮从实际 asm、ROM、constants 和消费者独立取证，未以 executor JSON 或自检结论代替复核。Seg-6 的 PASS 不作为本段证据。
- reviewer 仅写本 review；未修改 proposal、执行 JSON、源码、常量、进度或 Ghidra，未 build/stage/commit。以下 PASS 评定提案质量与现有工具可执行性，不代表落地或 byte-identical 验收已经完成。

## P0

✅ proposal 存在且非空；执行表、三个 plate、NEW/REUSE、数据分类和消费者证据齐备。全文零容忍词扫描为 0 命中，未发现中止标记。

## 核验 (C1-C13)

| # | 检查 | 结果 | 独立证据 |
|---|---|---|---|
| C1 | Rule 1：地址序与范围 | ✅ | 活动文档 `doc/dev/p5-refine-12-equip-activation-scan.md:247` 的 Seg-6 终点为 `0x08099314`；`:248` 的 Seg-7 区间与提案一致，`:249` 的 Seg-8 起点为 `0x0809a1a4`。`doc/dev/refine-progress.md:12` 当前任务为 Seg-7。三函数实际连续结束，无越界或共享尾遗漏。 |
| C2 | Rule 2：全部数据块归宿 | ✅ | 独立扫描段内 `ROM_INCBIN/.incbin/.byte` 均为 0。1619 个显式地址项加 29 处 2 字节 `.zero` 覆盖全部 3728 字节，缺口/重叠为 0，逐项与 ROM 一致。既有 11 项 switch 表被提案明确保留并接通池槽，不产生无归宿块。 |
| C3 | Rule 3：引用扫描 | ✅ | 独立按全 ROM 每个字节位置扫描 little-endian raw 与 `addr\|1`。表基址、全部唯一 case 目标、三个主入口、三个内部返回块的计数与位置全部复核；见下表。§5.1 空集合正确，内部返回块有直接分支/自然续接，不因 raw=0 而归为孤儿。 |
| C4 | R1：数值一致 | ✅ | 96 EQ 槽逐个 ROM u32 核对为 0 差异；27 REF 目标值与原始字节一致；12 RENAME 槽仍为 `gP1LifePoints=0x0201c4e0`。23 NEW 定义与引用它们的槽值一致；11 个 switch 项保持原值。 |
| C5 | R1：常量复用与用途 | ✅ | 独立解析并递归求值现有 5932 条 `.equ/.set`，成功 5932、未解析 0、重名 0。全量按值核对 23 NEW 和 40 REUSE；三个同值异域新建项有消费者依据，其他 20 个新值无既有定义。`0xffff/0xffff0000/0x1cb8/0x1cf4/0x1770` 的复用选择均按实际用途或基址核验，见下文。 |
| C6 | R2：标签与碰撞 | ✅ | 135 个新 slot_label 全部匹配 `^[a-z][a-z0-9_]+$`，槽标签之间无重名；与当前 asm 标签及 constants 定义无碰撞。23 个新增定义名均无现有定义或 asm 标签碰撞。既有 switch 必须复用原 LABEL 对象；允许将其 namespace/短名规范化为提案指定的全局 GAS 名，并设 USER_DEFINED/primary，不新造同址标签，不改内部 case。独立核对实现的精确匹配与碰撞防护，见 C6/C7 补充。 |
| C7 | R3：符号接通 | ✅ | 27 REF 明列目标 USER_DEFINED LABEL 主符号、槽 operand 0 的 DATA/USER_DEFINED 引用和 DEFAULT 同目标引用的精确移除/重建要求；12 RENAME 保持已导出的 gP1LifePoints 引用。读取当前 exporter，并以其原函数对计划对象状态做内存探针，96 EQ、27 REF 全部返回计划符号。switch 原对象名称规范化满足 exporter 的 getName() 路径。无 FUNCTION 目标或 `+1` 表达式导出依赖，详见下文。 |
| C8 | R5：plate 现名 | ✅ | 三条替换 plate 不含旧 `FUN_/DAT_/DWORD_/PTR_` 名；引用 `gEquipChainSlotRefs/gDuelEquipCtx/gP1LifePoints/EQUIP_CHAIN_ACTIVE_OFF` 均为当前符号。没有跨段替换或函数改名要求。 |
| C9 | ASCII 与长度 | ✅ | 三条 plate 长度分别 459/469/477，均纯 ASCII 且不超过 500。12 条 EOL 全部 ASCII；所有 NEW `.equ` 的名字、值与注释也均 ASCII。 |
| C10 | 指针与 THUMB 位 | ✅ | switch 消费者 `0x0809935c` ROM 字节 `87 46`，解码 `MOV pc,r0`；表中 11 项为偶地址跳转目标，不应加 1。主入口的外部表值各为入口地址加 1，均在段外，仅作扫描取证，本提案不改动。无新增 carve 或 callback 表。 |
| C11 | 现名与实际函数职责 | ✅ | 通读三函数及其返回块：分别为 field phase 派发、slot display phase 更新、spell display phase 处理，现名与各自状态操作一致。旧 plate 的上下文步长、输入寄存器、基址和返回路径错误均由新 plate 订正；未发现必须列入 FUNC_RENAME 的职责矛盾。 |
| C12 | R6：语义与消费者证据 | ✅ | 独立核对输入 r0、0x38 context、0x14 activation record、count 饱和、field/LP 基址、slot index、payload low9、packed type21 和三套状态转换；CID 使用表的 31 个值均以本地映射及 ROM 核对。关键结论均有具体消费者行号、置信度 high，见下文。 |
| C13 | 自动槽全覆盖 | ✅ | 实际集合 135 槽 = 122 DAT + 12 PTR_gP1LifePoints + 1 PTR_switchdataD；DWORD/UNK 为 0。EQ=96、REF=27、RENAME=12 三集合互斥，其并集等于全部自动槽；遗漏、重复、额外地址、越界均为 0。 |

## 独立测绘与控制流复核

| 函数 | 实际范围 | 字节数 | 自动槽 | EQ / REF / RENAME |
|---|---|---:|---:|---:|
| dispatch_equip_field_phase_handler | `[0x08099314,0x08099aac)` | 1944 | 72 | 45 / 19 / 8 |
| run_equip_slot_display_update_state_machine | `[0x08099aac,0x08099e0c)` | 864 | 28 | 22 / 4 / 2 |
| run_equip_spell_display_state_machine | `[0x08099e0c,0x0809a1a4)` | 920 | 35 | 29 / 4 / 2 |
| 合计 | `[0x08099314,0x0809a1a4)` | 3728 | 135 | 96 / 27 / 12 |

扫描实际模块 `:10980` 至 `:12900` 的地址/字节注记，以 ROM 逐字节核对。1619 个显式项与 58 个对齐字节无缺口、无重叠；29 处 `.zero 0x2` 在 ROM 中均为零。134 个 `.hword` 均为已有 `0x46xx` Thumb 高寄存器操作表示，结合相邻指令和局部控制流可解释，不构成未分类裸数据。

另从原始 ROM 独立解码全部 143 条 PC-relative LDR 和 285 条直接分支/BL，并与实际 asm 标签地址比对，目标差异为 0。三个内部尾分别恢复本函数的栈帧与保存寄存器；它们没有独立函数输入契约，也没有需要 carve 的附带块。

全 ROM raw/THUMB 扫描结果如下，位置均为 ROM 映射地址。扫描匹配所有字节位置，不限制 4 字节对齐。

| 扫描目标 | raw 命中位置 | `target\|1` 命中位置 |
|---|---|---|
| switch 基址 `0x08099370` | `0x0809936c` | 无 |
| case 0 `0x0809939c` | `0x08099370` | 无 |
| case 1 `0x08099520` | `0x08099374` | 无 |
| case 2 `0x0809972c` | `0x08099378` | 无 |
| case 3 `0x08099844` | `0x0809937c` | 无 |
| case 4 `0x08099880` | `0x08099380` | 无 |
| case 5 `0x08099888` | `0x08099384` | 无 |
| case 6 `0x0809997c` | `0x08099388` | 无 |
| case 7/8/9 `0x08099a98` | `0x0809938c`、`0x08099390`、`0x08099394` | 无 |
| case 10 `0x080999e0` | `0x08099398` | 无 |
| 主入口 `0x08099314` | 无 | `0x09e5ab08` |
| 主入口 `0x08099aac` | 无 | `0x09e5ab0c` |
| 主入口 `0x08099e0c` | 无 | `0x09e5ab10` |
| 内部返回块 `0x08099a9a` | 无 | 无 |
| 内部返回块 `0x08099df2` | 无 | 无 |
| 内部返回块 `0x0809a170` | 无 | 无 |

## 常量、RAM 与消费者语义

所有下列结论置信度为 high。值相等只作为检索入口，命名判定按实际消费操作进行。

| 核验对象 | 实际证据及判定 |
|---|---|
| 两种步长 | `asm/12_equip_activation_scan.s:10990`、`:11989`、`:12435` 的 `(side*8-side)*8` 得到 `0x38`；context 基址为 `gEquipChainSlotRefs+0x2c = gDuelEquipCtx`。`:11709` 和 `:12027` 开始的 activation record 循环使用 `0x14`，不是 context 步长。 |
| gDuelEquipCtxSlotIndex | 槽 `0x0809993c` 原值 `0x0201bbc0 = gDuelEquipCtx+4`。`:11704` 至 `:11730` 以同一 `side*0x38` 分别索引 context 与 slot word，并与 activation record 的 player/slot 字段比对。`asm/08_equip_oam_neodaed.s:5251` 至 `:5297` 从 gDuelEquipCtx 派生同一 context，`[+0]` 选择 player、`[+4]*0x14` 索引 field slot，`[+0xc]` 比较派生 entity ID。新全局名称准确。 |
| cid_1130 同值异域 | 现有 `EQUIP_CHAIN_STEP_BASE_OFF=0x1130` 位于 `constants/duel_field.inc:262`，用途为地址偏移。本段 `asm/12_equip_activation_scan.s:12664` 对 context 的卡 ID 比较，且 ROM ID 映射未分配，因此保留 `cid_1130`，不复用 offset 名。 |
| EQUIP_PAYLOAD_LOW9_MASK | `0x1ff` 现有同值为 `DEMO_KEEP_BITS_8_0` (`demo_state.inc:21`)、`SCROLLBAR_KEEP_BITS_8_0` (`gl_scrollbar.inc:11`)、`OAM_ATTR1_X_MASK` (`oam_attr.inc:18`)。本段 `:11879` 和 `:12817` 取 context[+0xc] 的 entity 低 9 位，拼入 r2 extra_payload；与 demo、scrollbar、OAM 坐标域不同。 |
| EQUIP_PAYLOAD_CLEAR_LOW9_MASK | `0xfffffe00` 现有同值为 `STACK_ALLOC_NEG_512` (`duel_field.inc:444`) 与 `OAM_ATTR1_X_CLEAR` (`oam_attr.inc:19`)。本段在相同 payload 序列中 AND 清低 9 位后 OR entity bits，不是栈分配或 OAM x；与上一掩码配对的新定义成立。 |
| payload 字段 | `:11879` 至 `:11930`、`:12817` 至 `:12855` 确认 entity bits8:0、side bit9、slot bits13:10、context[+8] bit0 写 bit14、bit15 置 1、bit16/17 清 0。`asm/05_equip_eligibility_a.s:8043` 至 `:8061` 保存并转发 r2 到 packed activation callee。提案没有宣称其他高位被清零。 |
| EQUIP_ACTIVATION_PACKED_TYPE21 | ROM 值 `0x2a200000 = (21<<25)\|(1<<21)`。`asm/06_equip_eligibility_b.s:18716` 至 `:18727` 将 bits22:21 放入 record[+3] bits5:4；`:18738` 至 `:18746` 将 bits30:25 放入 record[+2] bits11:6。因此新常量注释中的 1 与 21 均成立。 |
| count cap 与 halfword mask | `:11735` 至 `:11740`、`:12040` 至 `:12054` 对 count 做 `0xffff` 饱和；其他 `0xffff` 与 `0xffff0000` 消费点执行位拼接。复用目录分别采用 count cap、低/高半字掩码，没有把 count 或 payload 当成空卡 sentinel。 |
| `0x1cb8` 与 `0x1cf4` | `:11181` 至 `:11205`、`:11396` 至 `:11402` 的 `0x1cb8` 加到 gDuelFieldSlots，实际地址 `0x0201e1c8`，支持 `EQUIP_ZONE_COUNT_TABLE_OFF`。`:12151` 至 `:12161` 的 `0x1cf4` 加到保存于 r4 的 gP1LifePoints，支持现有 `P2LP_BLOCK2_OFF_1CF4`，不套用另一基址的同值字段名。 |
| MARSHMALLON_CID | `0x1770` 与 `LP_DELTA_6000` 数值相等，但 `:12488` 比较 context[+0x10]，本地卡映射指向 Marshmallon，复用 CID 名正确。 |
| 新 sprite 常量 | `0x8016/0x8017/0x8021/0x8046/0x8060` 分别在 `:11516`、`:11750`、`:11828`、`:12591`/`:12740`、`:12858` 附近由非零 side 分支选择；零 side 使用低位对应编号，传给 enqueue_sprite_attr_record 的 r0。名称沿用既有 OAM_EQUIP_SPRITE_P2 系列，注释准确说明非零 side。 |

其余新值未命中任何现有常量；40 项 REUSE 全部存在且求值相等。新定义分配为 card_info 14 项、oam_attr 5 项、duel_field 3 项、ewram 1 项，共 22 常量和 1 RAM 全局；不需要新增 include 文件。

## CID 独立核对

提案使用表共 31 个 CID：27 个具名值、4 个中性值。独立核对 `data/card-stats.s` 标题的名称、slot、card 编号、实际 `.hword slot_id`，以及 ROM 中两个数据表：

- ID 映射 ROM 偏移：`0x015b7ccc + (internal_id-4007)*2`。
- card-stats slot_id ROM 偏移：`0x018169b8 + card_id*22`。此处导出的表从 card_0000.slot_id 开始；首个 zero0 的 2 字节归属前一区域，不能再额外加 2。
- 27 个具名值的映射与 card-stats 原始 slot_id 全部相符；提案每个 CID 的消费者行均为实际 literal LDR。
- 新增 10 个具名常量的名称、slot、密码与源标题相符；新增 4 个中性 ID 的原始 ROM 映射均为 `0xffff`，全 card-stats 无对应 slot。活动文档 `:34` 已明确未分配 ID 使用 `cid_<hex>`。

| 新 CID | 值 | 独立映射/来源 |
|---|---|---|
| cid_112f | `0x112f` | ROM 映射 `0xffff`；`data/cards-ids-array.s:409` |
| cid_1130 | `0x1130` | ROM 映射 `0xffff`；`data/cards-ids-array.s:410` |
| cid_1135 | `0x1135` | ROM 映射 `0xffff`；`data/cards-ids-array.s:415` |
| cid_1208 | `0x1208` | ROM 映射 `0xffff`；`data/cards-ids-array.s:626` |
| WALL_OF_ILLUSION_CID | `0x1310` | card_0698，pw 13945283；`data/card-stats.s:9089` |
| TIMEATER_CID | `0x13b1` | card_0831，pw 44913552；`data/card-stats.s:10818` |
| KELBEK_CID | `0x14f1` | card_1057，pw 54878498；`data/card-stats.s:13756` |
| AFTER_THE_STRUGGLE_CID | `0x1512` | card_1085，pw 25345186；`data/card-stats.s:14120` |
| DD_CRAZY_BEAST_CID | `0x15d9` | card_1228，pw 48148828；`data/card-stats.s:15979` |
| DD_WARRIOR_LADY_CID | `0x1657` | card_1327，pw 07572887；`data/card-stats.s:17266` |
| DD_ASSAILANT_CID | `0x172c` | card_1503，pw 70074904；`data/card-stats.s:19554` |
| ELEMENT_DOOM_CID | `0x1861` | card_1762，pw 23118924；`data/card-stats.s:22921` |
| HOLY_KNIGHT_ISHZARK_CID | `0x18e6` | card_1871，pw 57902462；`data/card-stats.s:24338` |
| RUIN_QUEEN_OF_OBLIVION_CID | `0x19d4` | card_2055，pw 46427957；`data/card-stats.s:26730` |

## 三条 plate 的状态与返回值

全部以下检查均来自实际函数体，置信度 high。

- `dispatch_equip_field_phase_handler`：r0 在 `:10985` 至 `:10986` 保存为 player side；phase 从 gP1LifePoints+EQUIP_CHAIN_ACTIVE_OFF 读取。phase0 的 mismatch 分支 `:11041` 至 `:11050` 写 phase10 后返回 0。phase2/3 的 mismatch 进入 `0x08099a5a` 写 step11、清 phase、返回 0；phase4 调用 candidate scan。phase5 按 player/slot 匹配两条 activation records 并对 count 饱和。phase6 及 case7/8/9、越界直接完成返回 1；phase10 在资格门控及 activation 后写 step11/phase0 返回 0。新 plate 区分了 phase0 mismatch 与后续 mismatch，没有混写返回约定。
- `run_equip_slot_display_update_state_machine`：输入 side 保存在 r10，两个 context 步长 0x38。phase0 遍历两条 0x14 activation records；chain[+0x14] 非零则不做 row 工作，零 count 不提交，其余 count 饱和并组成 type14 LP row，row 工作由 counter 调用包围。phase1 检查 Satellite Cannon/Rocket Warrior 后排显示；phase2 在 counter 调用之间执行 card-specific activation 与 sprite 更新。phase0/1/2 最后均自增 phase 并返回 0；再次进入 phase3 才返回 1。对应 `:12013` 至 `:12108`、`:12124` 至 `:12416`。
- `run_equip_spell_display_state_machine`：chain[+8] 非零在读 phase 前返回 1。phase0 两个 scanner 任一非零直接返回 0且不推进；均空闲后走 Marshmallon 条件激活并 phase++，返回 0。phase1 完成两方 CID/资格分支、显示和 type21 activation 后返回 1，本函数内不自增 phase1；其他 phase 返回 1。对应 `:12445` 至 `:12518`、`:12519` 至 `:12873`。

三条 plate 分别 459/469/477 字符，修正这些实际错误后仍保留准确输入、使用基址与返回值；无需 FUNC_RENAME。

## C7：现有 exporter 的可执行路径

读取并在只读内存探针中调用当前 `ExportRangeToGas.py` 的原始 `sanitize_label`、`resolve_word_symbol`、`resolve_word_equate` 函数；仅模拟提案规定的对象状态，没有执行 Ghidra 或改工具。

- `:527` 至 `:537` 选择 outgoing primary reference 或首个引用；`:549` 至 `:562` 要求目标 USER_DEFINED 主符号，ROM 目标还须为 LABEL。本段 26 个 RAM REF 及 1 个 switch REF 按计划均通过此路径，得到期望名字，27 项差异为 0。
- switch 目标 `switchD_0809935c__switchdataD_08099370` 为既有表标签；大小写不触发 `SWITCH_` 自动名前缀过滤，sanitize 不改变名字。导出的 `.word switchD_0809935c__switchdataD_08099370` 数值就是 `0x08099370`。
- `:612` 至 `:617` 在 symbol 路径为空时进入 equate fallback。本段 96 个纯数值 EQ 按提案建立数据 operand0 equate 后均得到期望常量名，96 项差异为 0。全部名称均不需要算术表达式或字符改写。
- 12 个 RENAME 槽当前已导出 `.word gP1LifePoints`，计划只改槽标签与 EOL，明确保留值、目标和引用。
- 提案明确处理既有同目标 DEFAULT 引用：精确删除该 operand0 引用后重建 DATA/USER_DEFINED，并核验 from/to/operand/type/source。不能仅调用 addMemoryReference 后假定 source 已升级；此约束已在提案内，不构成待修订项。
- 模式 B 仍需检查真实引用的选择结果、实际主符号、equate、导出表达式以及保存后的持久状态；本次源码探针只证明提案可由现有路径实现，不替代真实数据库验收。最终 135 槽和 11 项 switch 值仍须以正式 asm/ELF/ROM 核对。

## C6/C7 补充：switch 标签的 Ghidra 表示规范化

2026-08-31 落地前专项复核，仅补充标签表示和脚本实现的静态证据；不重跑已完成的槽位/CID 审核。proposal SHA256 保持 `5463ac0f317237ce2af3e3c998a0bceb2f31af53e2179253a8e540d18e0df51d`。仅读 `tools/ghidra-labeling/RefineF12Seg7Slots.py`，本次读取版本 SHA256 为 `5b1d8ed398b9400fc2ac7eebfa4b41482092f63e525c31714c477312e99c72a1`。

**结论：符合已通过的计划，C6/C7 保持通过。** 提案 `:188` 要求复用既有表标签及原地址，`:190` 指定 `.word switchD_0809935c__switchdataD_08099370`。当前 exporter `:557` 调用 `sym.getName()`，并非 qualified name，因此原 Ghidra 若为 `switchD_0809935c::switchdataD_08099370`，仅升级 source/primary 无法得到所需 GAS 名。将同一个 LABEL 对象移入 global namespace，再将短名设为 `switchD_0809935c__switchdataD_08099370`，属于实现指定符号表达式的表示规范化，不改变表地址、表值或函数边界。

| 检查 | 脚本证据及允许条件 |
|---|---|
| 精确旧状态匹配 | `RefineF12Seg7Slots.py:375` 至 `:380` 仅在 `0x08099370` 上选择 LABEL，要求 `getName(True).replace('::', '__')` 与指定完整 GAS 名完全相等且唯一。可接受原 scoped 名或已规范化的 global 完整名；错误 namespace 的短名、其他名称、非 LABEL、多个匹配都不通过。这里只使用受限的 qualified-name 规范化，不接受仅按地址任选对象。 |
| 名称碰撞防护 | `:337` 至 `:340`、`:373` 检查指定完整名的全部 global 符号，异地址同名会在写入前失败；同址旧 scoped 标签与同址 global 完整名同时存在时，唯一匹配检查会失败。`:381` 至 `:383` 拒绝 FUNCTION 主符号。setNamespace/setName 若因 Ghidra 名称约束抛出异常，事务回滚，不允许改用另建标签绕过。 |
| 复用同一 LABEL 对象 | `:440` 优先取得已有 global 完整名；不存在时，`:443` 至 `:450` 再次要求唯一匹配，直接对 `candidates[0]` 调用 setNamespace(global) 和 setName(USER_DEFINED)。switch 分支没有 delete/createLabel；创建分支 `:451` 至 `:452` 仅在该 switch 分支不进入时使用。已有 global 完整名直接复用并升级 source/primary。 |
| 修改范围 | 仅移动表标签自身，不修改 namespace 对象或其余 case 标签；保持表标签地址、LABEL 类型与对象身份。`:401` 至 `:402`、`:503` 至 `:504` 前后检查全部 11 项 u32 表值。函数名亦由 `:501` 至 `:502` 检查。 |
| postcheck 与导出条件 | `:478` 至 `:488` 检查目标 primary 的精确短名、USER_DEFINED，以及唯一 primary DATA 引用的 from/to/operand0/source。`:419` 至 `:427` 显式将该引用设为 primary，满足 exporter 的引用选择路径；名称规范化后 getName() 返回指定 GAS 名。此 postcheck 未单独快照 symbol ID、namespace 或全部 case 名；对象身份及 LABEL 类型保留来自上述受限 API 路径的静态证据，不能将其写成已经完成的数据库快照验证。 |
| 失败处理 | `:508` 至 `:510` 在 preflight 失败时禁止写入；`:512` 至 `:521` 把实际修改和 postcheck 放在同一事务，任一异常或 postcheck 失败都以 success=False 结束。原状态未满足精确匹配时，应停止该落地流程，不扩大候选或创建替代标签。 |

此次补充不变更 proposal 或原评审数值/语义结论，也未执行 Ghidra。真实数据库的落地与保存后验收仍由模式 B 完成。

## 状态: PASS

P0、C1-C13 全部通过。未发现需修订的提案项；独立扫描和消费者核验支持进入模式 B。

## 修改清单

无。

## Reviewer Verdict: F12-Seg-7 = PASS
