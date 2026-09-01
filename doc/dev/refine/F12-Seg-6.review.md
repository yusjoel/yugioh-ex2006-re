# Refine Review: F12-Seg-6

## 输入与独立复核范围

- 日期：2026-08-31；当前为第二轮复审结论，保留首轮独立证据与问题记录。
- 段：`[0x080984d0, 0x08099314)`，共 `0xe44` / 3652 字节。
- Proposal：`doc/dev/refine/F12-Seg-6.proposal.md`。
- 模块：`asm/12_equip_activation_scan.s:9105` 至本段最后一个池槽所在的第 10976 行。
- 活动文档：`doc/dev/p5-refine-12-equip-activation-scan.md`，第五节 Seg-6；Seg-5 已完成，Seg-7 未开始。
- 原始 ROM：`roms/2343.gba`，独立读取的 SHA1 为 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`。
- 本次直接读取 proposal、模块、ROM、全部 `constants/*.inc` 和消费者代码；没有采用 executor 的扫描 JSON 或自检结论代替复核。
- 当前 Proposal SHA256：`93f23b649fb8608e14278e60094b7c4dda05a8ed85812cbc61441b64644ee9a5`。
- 首轮 Proposal SHA256：`390ec44dc0edc6263b157f5a6aa9c1a150750dbbf04b8199e6a00d42b1f076ac`；复审直接读取 `output/refine-run-20260831-194634/F12-Seg-6.proposal.before-fix1.md`，确认其字节摘要一致。
- 模块 SHA256：`90b2c6f82e4d4a645fb88dc832ce870d7056b8396fbe83701045576400c23d5d`。

P0 通过：proposal 非空，禁用标记与零容忍词命中均为 0。

第二轮重新核对 ROM SHA1、模块 SHA256、完整槽表、全部常量目录及新增导出表示。未改变的 plate、消费者证据、REUSE、carve/disasm 章节逐段比较完全一致，沿用首轮已完成的引用扫描、控制流与语义证据。以下 C1-C13 表为第二轮的当前结论。

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|---|---|---|
| C1 | Rule1 地址序与路线图 | ✅ | 起止地址与活动文档第五节、总进度下一任务一致。三个主函数与一个共享返回尾均在本段；末尾 literal pool 到 `0x08099310`，下一函数从 `0x08099314` 开始。 |
| C2 | Rule2 每个裸数据块均有归宿 | ✅ | 独立扫描 `ROM_INCBIN/.incbin/.byte` 为 0；99 条 `.hword` 全部为 `0x46xx` 高寄存器指令。17 处 `.zero` 各 2 字节，ROM 均为零。地址覆盖 3652/3652 字节，无遗漏裸块。既有 5 项 switch 表保持结构。 |
| C3 | Rule3 零引用判定 | ✅ | 本段新增 §5.1、carve、disasm 集合均为空。另独立重跑既有 switch 表、五个目标、三个主入口及共享尾的全 ROM raw/THUMB 扫描，结果见下表。共享尾虽为 0/0，但有实际控制流入口，proposal 未将其登记 §5.1。 |
| C4 | R1 ROM 值 | ✅ | 第二轮按 80 EQ、39 REF、7 RENAME 共 126 槽重新逐槽读取 ROM 四字节小端，0 个值差异。段内 asm 地址/字节注记与 ROM 一致。模块未变，沿用首轮 153 条 PC-relative LDR 的独立解码结果。 |
| C5 | R1 常量复用与域 | ✅ | 第二轮再次独立解析并递归求值 5909 条 `.equ/.set`，全部成功。23 个拟新增定义中仅 `0x1cfc` 有既有同值；其基址域不同，有实际地址计算支持。新增 THUMB equate 同名/同值均 0 命中，35 项 REUSE 不变。 |
| C6 | R2 槽名与碰撞 | ✅ | 126 个新槽名均满足 `^[a-z][a-z0-9_]+$`；三表内无重复名，与现有 `asm/*.s`、`constants/*.inc` 定义无碰撞。地址后缀保留了同类槽区分。 |
| C7 | R3 按名引用可落地 | ✅ | 38 个 RAM 槽及 switch 表槽保留 USER 主标签、DATA-ref 和 GAS 定义计划。`0x080987bc` 已改为 THUMB data-equate，辅助 DATA/USER_DEFINED 引用指向 `0x0804b164` 并保留 FUNCTION 主符号；按现有导出器走 equate fallback。首轮 #1 已闭环。 |
| C8 | R5 plate 使用现名 | ✅ | 四个新 plate 无旧自动名引用，完整覆盖原 plate 所在行 9105、9178、9845、10950。引用的 `advance_equip_display_phase_via_table` 与共享返回尾名称均为当前定义。 |
| C9 | ASCII 与 plate 长度 | ✅ | 四个 plate 实测正文长度仍为 379/464/459/334，均不超过 500；四板、7 条 RENAME EOL、1 条新增 EQ EOL、23 个新增定义的注释全部 ASCII。新增 EOL 为 67 字符。 |
| C10 | THUMB 位与指针值 | ✅ | 第二轮重读 `0x080987bc` 的 ROM 字节为 `65 b1 04 08`，即函数入口 `0x0804b164+1`；THUMB equate 同值。switch 表仍经 `MOV pc,r0` 派发，五项全为偶地址，不加 1。 |
| C11 | 误名与函数行为 | ✅ | 三个主函数均处理对应显示/发动阶段，共享尾只恢复主函数保存的寄存器和栈。新板修正输入、返回和基址，不需要新增或改名函数。独立解码本段 249 条 B/条件分支/BL，目标全部与 asm 标签一致。 |
| C12 | R6 消费者证据 | ✅ | 新增地址、偏移、位域与 CID 均有 file:line 和 high 置信度证据。独立核对基址差 `0x30`、snapshot 最大写入偏移 `0x40`、处理行数、packed type 解包、全部 38 个已分配 CID 及未分配 `0x10c6`。未使用卡牌效果常识替代代码证据。 |
| C13 | 自动名完整覆盖 | ✅ | 第二轮重新清点 DAT_=114、DWORD_=4、PTR_=8，共 126；EQ=80、REF=39、RENAME=7。三表两两无交集、并集等于自动名全集，缺项/多项/重复/越界均为 0。辅助导航引用不重复计入 REF；四个 DWORD 地址与末尾池槽仍已覆盖。 |

## 独立 ref-scan 与字节核验

使用 `d.count(struct.pack("<I", addr))` 和 `addr|1` 对完整 ROM 扫描，并用 `find` 定位命中。

| 地址/对象 | raw | THUMB+1 | 实际命中位置 |
|---|---:|---:|---|
| `0x080985a0` switch 表基址 | 1 | 0 | `0x0809859c` |
| `0x080985b4` case 0 | 1 | 0 | `0x080985a0` |
| `0x080985c6` case 1 | 1 | 0 | `0x080985a4` |
| `0x08098610` case 2 | 1 | 0 | `0x080985a8` |
| `0x080987dc` case 3 | 1 | 0 | `0x080985ac` |
| `0x08098a44` case 4 | 1 | 0 | `0x080985b0` |
| `0x080984d0` 主入口 | 0 | 1 | `0x09e5aafc` |
| `0x08098564` 主入口 | 0 | 1 | `0x09e5ab00` |
| `0x08098a88` 主入口 | 0 | 1 | `0x09e5ab04` |
| `0x080992e2` 共享返回尾 | 0 | 0 | 直接控制流：`BL@0x08098b12`、`B@0x08098e38`、`0x080992e0` 自然续接 |

`asm/12_equip_activation_scan.s:9199` 至第 9203 行加载 switch 表项并执行 `0x4687`，即 `MOV pc,r0`。共享尾第 10952 行先释放 `0xc` 局部字节，随后恢复 r8/r9/r10、r4-r7，并从原调用者保存地址返回；不改 r0。

本次仅核验原始 ROM 和计划值，未执行构建，也不将源 ROM 的 SHA1 结果当作落地后的 byte-identical 验收。

## 常量与消费者复核

### 同值复用

- 第二轮 23 个新增定义中，22 个值在现有 constants 全目录求值后为 0 命中；相对首轮只新增 `CHECK_CARD_ID_IS_NORMAL_SUMMON_TYPE_THUMB=0x0804b165`。
- `EQUIP_CHAIN_ACTIVE_FROM_FIELD_OFF=0x1cfc` 唯一同值项是 `DISP_SET_VARIANT_OFF`，定义于 `constants/duel_field.inc:253`。后者以 `gP1LifePoints` 为基址，地址为 `0x0201e1dc`；本段 `asm/12_equip_activation_scan.s:9883` 加载 `gDuelFieldSlots=0x0201c510`，第 9902 行加载 `0x1cfc`，第 9903 行相加，地址为 `0x0201e20c`。新增不同基址的名称成立。
- `0x1cf8` 在 `asm/12_equip_activation_scan.s:10322` 加到仍为 `gDuelFieldSlots` 的 r4，形成 `0x0201e208`，等于 `gP1LifePoints+0x1d28`；第 10324 行赋值 11。两槽原始值必须保持。
- `0x1cb8` 的两个既有名字分别以 `gP1LifePoints`、`gDuelFieldSlots` 为基址。本段第 10625、10626 行令 r9=`gDuelFieldSlots`，第 10720 至 10723 行读取 `[r9+0x1cb8]`，因此复用 `EQUIP_ZONE_COUNT_TABLE_OFF` 的地址域正确。
- `0x0fb6` 进入 `check_value_in_slot_chain` 的 CID 参数以及后续显示调用，见第 9406、9424 行，因此复用 `TIME_WIZARD_CID`，不使用同值的 `EQUIP_ZONE_SPRITE_ATTR`。
- 35 项 REUSE 的名字和值全部重新核对，含 `SPRITE_RECORD_P2_SIDE=0x8020`、`OAM_EQUIP_SPRITE_TILE_P2_1B=0x801b` 与六个 RAM 基址。

### 新地址、位域与 plate

- `gEquipSlotActivationSnapshot=0x0201bc7c`：第 9219 行直接传给 `fill_slot_activation_state_array`；第 9953 至 9955 行以 `gEquipChainSlotRefs+0xec` 传入同一目标。callee 在第 6998、7008、7034、7045、7056 行写 `+0/+4/+8+i*4/+0x1c+i*4/+0x30+i*4`，第 7059 行限制 i 到 4，覆盖 0x44 字节。
- `SPRITE_ROW_PROCESSED_COUNT_OFF=0x482`：本段第 9781 至 9785 行清零、第 9816 至 9825 行读后通知并清零。`asm/05_equip_eligibility_a.s:9992` 至第 10036 行以该 u16 为处理位置，逐条递增到 `+0x480` 总量；记录步长为 `0x18`。第 12916 至 12929 行从该值减一反向处理，支持 processed count 名称。
- `0x24200000=(18<<25)|(1<<21)`、`0x28200000=(20<<25)|(1<<21)`。本段第 9641、10226 行与槽号/CID/player 位组合后传给 `apply_equip_activation_with_id_lookup`。wrapper 见 `asm/05_equip_eligibility_a.s:8044` 至第 8061 行；实际解包见 `asm/06_equip_eligibility_b.s:18716` 至第 18746 行，目标为 record+2 bits[11:6] 和 record+3 bits[5:4]，proposal 位域正确。
- 首函数第 9114 行返回 eligibility 到 r8，随后检查 bit1；第 9116 至 9120 行处理一次闩锁。Toll 的立即数为 `0x99<<5=0x1320`，每次循环显示参数为 `0xfa<<1=500`。新板没有沿用旧板对 r1 和第二次 enqueue 调用的错误描述。
- 两个 tick 入口均以 `0x4680` 保存输入 r0 到 r8；返回 0/1 的路径与新板一致。上游 `asm/12_equip_activation_scan.s:16725` 至第 16747 行转发 player_side，子函数返回非零时推进 step。
- phase 2 的检测 callee 在第 7284、7299、7326 行将不匹配跳转至第 7341 行返回 1；匹配路径第 7353 行返回 0。本段第 10319 至 10328 行在非零时写 step 11 并清 phase，新板条件正确。

### CID 与回调

- 逐行读取 proposal 所引用的 `data/card-stats.s` 卡表记录，38 个已分配 CID 的 slot 值、卡名均一致；`MIRROR_WALL_CID_SHIFTED` 另由 `data/card-stats.s:10363` 的 `slot=0x1381` 和本段第 9289 行左移 19 验证。
- `data/cards-ids-array.s:304` 的内部 ID `0x10c6` 映射为 `0xffff`，card-stats 无该 slot；复用既有中性符号 `upd_cid_10c6` 正确。本段第 10655 至 10711 行的 mode=1 路径也与 proposal 描述一致。
- `0x18f2` 是 Steamroid，`0x18f3` 是 Drillroid；卡表分别在 `data/card-stats.s:24403`、`:24416`，且 `data/cards-ids-array.s:2397` 指向 Drillroid。proposal 未重复新增既有 `GYROID_CID`。
- 回调槽 `0x080987bc` 在本段第 9355 行载入 r1，随后调用 `count_monster_slots_by_fnptr`。该 callee 在 `asm/02_text_lp_fieldspell.s:15797` 将 r1 保存到 r7，第 15811 至 15814 行提取 CID 低 13 位并经 `invoke_r7` 调用。目标当前入口是 `asm/05_equip_eligibility_a.s:4538` 的 `check_card_id_is_normal_summon_type@0x0804b164`。

## 首轮问题与修改清单（第二轮已完成）

首轮结论为 `NEEDS_FIX(1 items)`。以下保留原问题及五项修订要求，第二轮解决证据见后节；这些内容不是当前未完成事项。

### #1 — C7 — 为 `0x080987bc` 指定当前导出器可实现的 THUMB equate 表示

首轮问题证据：

- 首轮 proposal 将该槽列为 REF，并要求导出 `.word check_card_id_is_normal_summon_type+1`。
- `tools/asm-regen/ghidra/ExportRangeToGas.py:549` 读取目标主符号，第 554 至 555 行明确拒绝 ROM FUNCTION；第 562 行直接返回 `sanitize_label(name)`，没有附加 `+1` 的路径。
- 同文件第 66 至 76 行把 `+` 替换成 `_`；将表达式当作标签名也不能实现目标。
- 同文件第 612 至 617 行仅在 symbol 解析失败后尝试 equate，二者都为空时输出裸数值。因此只加到偶地址函数的 DATA-ref 不满足本段要求的按名输出。

首轮要求在 proposal 内完整指定以下方案，无需改 exporter：

1. 把 `0x080987bc` 从 `REF_SLOTS` 的唯一主分类移入 `EQ_SLOTS`，保留当前槽名，使用下列四元组：

   ```text
   (0x080987bc, 0x0804b165, CHECK_CARD_ID_IS_NORMAL_SUMMON_TYPE_THUMB, tick_card_activation_normal_summon_predicate_987bc)
   ```

2. 在 `constants/duel_field.inc` 的新增目录补入下列定义；Ghidra data-equate 的数值也明确为 `0x0804b165`。Reviewer 已对 5909 个现有定义重新按值求值，`0x0804b165` 同值命中为 0，该名称不存在。

   ```asm
   .equ CHECK_CARD_ID_IS_NORMAL_SUMMON_TYPE_THUMB, 0x0804b165  @ check_card_id_is_normal_summon_type+1; THUMB predicate for count_monster_slots_by_fnptr.
   ```

3. 另列该 EQ 槽的辅助导航引用：`0x080987bc -> 0x0804b164`，类型为 DATA/USER_DEFINED。沿用目标的现名 FUNCTION 主符号，不重命名它，不将 LABEL 提升为主符号，不在 `0x0804b165` 建标签或函数。此辅助引用不重复计入 REF 主分类。这样 `resolve_word_symbol` 返回 None，`resolve_word_equate` 明确输出该 THUMB equate。

4. 为该槽增加一条 ASCII EOL，并把导出验收改成 `.word CHECK_CARD_ID_IS_NORMAL_SUMMON_TYPE_THUMB`；数值验收保持 `0x0804b164+1=0x0804b165` 和 ROM 字节 `65 b1 04 08`：

   ```text
   THUMB callback: check_card_id_is_normal_summon_type+1 = 0x0804b165.
   ```

5. 同步 proposal 的说明、自检和计数：EQ=80、REF=39（RAM 38 + switch 1）、RENAME=7、总槽=126；新增定义总数从 22 改为 23（22 常量 + 1 RAM 全局）。删除仅靠 REF 自动产生 `函数名+1` 的承诺，保留五项偶地址 switch 表的现状。

## 第二轮修复核验

独立比较首轮保存版本与当前 proposal：唯一发生变化的主分类四元组是 `0x080987bc`，其余 125 个槽逐项相同。唯一新增 `.equ` 为 THUMB 回调常量；原 22 个定义不变。新增辅助引用、EOL、导出验收和计数/审计说明均属于首轮 #1，没有引入范围外语义修改。

| 首轮子项 | 第二轮证据 | 结果 |
|---|---|---|
| #1.1 主分类由 REF 移入 EQ | `doc/dev/refine/F12-Seg-6.proposal.md:47` 的四元组与要求完全一致；REF 中不再含该槽；其他三表记录不变。 | ✅ |
| #1.2 THUMB equate 定义与数值 | proposal 第 124 行指定 slot/operand/value，第 272 行新增定义。重新求值全部 5909 个现有 constants，名称及 `0x0804b165` 值均无命中；扫描当前 asm/constants 也无名称碰撞。ROM 原始四字节重新核对一致。 | ✅ |
| #1.3 偶地址导航与 FUNCTION 主符号 | proposal 第 125 行明确 `0x080987bc -> 0x0804b164`、DATA/USER_DEFINED、保留现名 FUNCTION 主符号、不提升 LABEL、不在奇地址建标签或函数，并明确不重复计数。 | ✅ |
| #1.4 ASCII EOL 与导出路径 | proposal 第 126 至 131 行指定 equate fallback、按名输出及数值验收；实际 EOL 与首轮要求逐字符相同，67 字符、纯 ASCII。原 `.word check_card_id_is_normal_summon_type+1` 导出承诺已删除。 | ✅ |
| #1.5 计数与说明同步 | 当前主表实测 EQ=80、REF=39、RENAME=7，共 126 个唯一地址；新增定义实测 23。辅助引用独立说明，四板、REUSE、carve/disasm 与消费者章节完全不变。 | ✅ |

为检查 C7 的具体输出路径，第二轮从当前 `ExportRangeToGas.py` 直接提取 `sanitize_label`、`iter_any`、`resolve_word_symbol`、`resolve_word_equate` 四个函数，在内存中提供与新计划一致的最小对象：slot=`0x080987bc`，引用目标=`0x0804b164`，目标主符号为 USER_DEFINED/FUNCTION，槽上含指定 equate。执行结果为 `resolve_word_symbol -> None`、`resolve_word_equate -> CHECK_CARD_ID_IS_NORMAL_SUMMON_TYPE_THUMB`，与第 612 至 617 行的输出分支一致。这是对现有导出逻辑的受控验证，没有修改源码，也不代表已运行真实 Ghidra 落地。

输入稳定性：第二轮 ROM SHA1 仍为 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`，模块 SHA256 与首轮完全相同；因此保留首轮全段 ref-scan、153 条 LDR、249 条分支解码和消费者语义证据。

## 状态: PASS

首轮唯一问题 #1 的五项要求全部落实，当前无未完成修订项。通过的是 proposal 评审；模式 B 仍须执行备份、dry-run、完整导出、残留检查和 byte-identical 验证。Reviewer 两轮仅写本 review 文档，未改 proposal、JSON、asm、constants、工具代码或 Ghidra，未 build、未 commit。

## Reviewer Verdict: F12-Seg-6 = PASS
