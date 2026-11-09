# F15-Seg-2 独立复核

## 第三轮 · PASS

本轮冻结清单 SHA-256 为 `046974768a1bb69ef2df8df3fcfedc12be7f5d171a301d6be0dfd778bc285d33`。独立核验 30 项冻结输入及第二轮归档。槽表、PLATE 表、外部表计划、全局 Equate 计划、Function 计划、R4、名称引用基线和布局图均与第二轮归档字节一致。

C5 修订通过。新增 GAS 仅 `ANTI_AIRCRAFT_FLOWER_CID`、`CATAPULT_TURTLE_CID` 和 `EQUIP_LEVEL_RESTRICTION_SCORE_THRESHOLD_2399`。其余五个名称逐行读取现有 `constants/card_info.inc`，确认名称和值吻合。八个标量 Ghidra Equate 均在前态缺失，计划值逐项与原 ROM 槽字一致。全局合同维持 213 个受影响名称、168 个新增对象、3 个退役、661 个新增绑定及 2417 个最终对象。

C1–C13 通过。方案可进入落地和整 ROM 逐字节验证。独立证据 `f15-seg2-review-round3-independent.json` SHA-256 为 `6a4ab2c4b437c45a6754f4d1817d18be5f522a5baf2b903a7252a3b33c2b1b17`。

## 第二轮 · NEEDS_FIX（1 项）

本轮冻结清单 SHA-256 为 `818393ffaaf037680f8824285c69b4f53f6f1543a6d3aac2638c9399d8d2ee7d`。独立核验 30 项冻结输入及首轮归档。87 槽表与首轮字节一致，五条现有 PLATE 发生计划内变化，另增 B4850。1008 个表字的旧态、133 个未来别名及基址 handoff 均与首轮一致。独立证据 `f15-seg2-review-round2-independent.json` SHA-256 为 `ffbb1d1da07beb9201a6d090c7fa6b41dfd14a29a857ddff8e16ca4ebb747a6b`。

原复核的四项问题均有对应修订。已按旧 Equate 前态重新计算三次退役、213 个受影响名称、661 个绑定增量和最终 2417 个对象。B771D 整 ROM 重扫恰为六条旧表源和 15 条新表源，B771C 偶址零命中。B7736–B773A 确认正值测试，B3408/B485E 是受控 BL 投影，B4850 只有 PLATE 投影。B778C 的固定 CID 和零和测试、B7934 的两条早接受路径及后续分数门槛、B7F64 的正计数和 BAD6C 的 +0x10 状态测试都已与指令对齐。B76A5 保持七表 201 条，B76A8 右边界仅增加 20 条获批 USER DATA 来向，已有记录均在最终 incoming 中。

### 1. C5 · 区分新增 GAS 定义与新增 Ghidra Equate 对象

第二轮 proposal 将八个 Ghidra 缺失名称都列成新增 GAS 常量，但其中五个已经在 `constants/card_info.inc` 定义了相同语义和数值：

| 已存在的 GAS 名称 | 值 | 行号 |
|---|---|---:|
| `ULTIMATE_BASEBALL_KID_CID` | `0x17e1` | 994 |
| `MAGICAL_DIMENSION_CID` | `0x1678` | 1485 |
| `HADE_HANE_CID` | `0x17ec` | 1640 |
| `LIGHT_OF_JUDGMENT_CID` | `0x1764` | 1771 |
| `BEAST_SOUL_SWAP_CID` | `0x1889` | 1792 |

将五项标成“复用已有 GAS 定义，首次建立 Ghidra Equate 对象”。新增源码定义仅三项，即 `ANTI_AIRCRAFT_FLOWER_CID`、`CATAPULT_TURTLE_CID`、`EQUIP_LEVEL_RESTRICTION_SCORE_THRESHOLD_2399`。同步 proposal、常量证据、机器 `new_constants`、冻结与自检计数。87 槽表的现有 `reuse existing constant` 已正确。八个新标量 Equate 对象、168 个总新增对象、三项退役、661 条绑定增量及最终 2417 个对象的 DB 合同继续有效。

## 首轮复核记录

范围 `[0x080b6c08, 0x080b79f8)`，冻结清单 SHA-256 为 `ae02b5c385f0a5b5b44b45d4384c80c5061ddb58d2dc910616225a45cc633d3f`。独立核验 28 项冻结文件。复核证据 `f15-seg2-review-independent.json` 的 SHA-256 为 `d248bf0c0dec4af120b918c6f78de6a03e3f9237638d19e3729c0bcf6059d99f`。

## C1–C13

| 项 | 结果 | 证据 |
|---|---|---|
| C1 | PASS | `doc/dev/refine-progress.md:12` 的下一段 |
| C2 | FAIL | B76A4 的 R4 分类成立，提案误计运行时表数并漏区分双消费者，见第 2 项 |
| C3 | PASS | 独立整 ROM 滑窗扫描。B76A4 偶址零命中，B76A5 201 命中均为表指针，无 §5.1 |
| C4 | PASS | 87 个段内槽、1008 个表字与原 ROM little-endian 字完全一致 |
| C5 | FAIL | 全局 Equate 合同漏 65 个标量绑定及其对象状态，见第 1 项 |
| C6 | PASS | 源标签和表首标签采用稳定命名，表首单一主标签 |
| C7 | PASS | 10 个 RAM DATA 增量、9 个既有引用保留、3 个段内 Thumb 以及外部表偶址 DATA 动作各有明确范围 |
| C8 | PASS | 拟用 PLATE 的函数名引用为当前名或本轮明确投影名 |
| C9 | PASS | 21 条拟写 PLATE 与段内 EOL 均为 ASCII，PLATE 长度不超过 500 |
| C10 | PASS | 504 个外部 callback 字均为奇值，目标为原字减一，133 个未来目标的 267 条 holder 无新增目标 ref |
| C11 | FAIL | B771C 现名与有符号正值测试的语义边界缺少闭合证据，见第 3 项 |
| C12 | FAIL | B778C、B7934 及后续两处调用者的说明缺少精确条件，见第 3–4 项 |
| C13 | PASS | 87 个现有自动字标签全部覆盖。外部 998 个隐式字计划建型，10 个已有类型保留 |

全 ROM 滑窗重扫 B76E5、B7761、B77F9 分别精确命中 26、12、1 条，三个对应偶址均零。B7761 的 12 条含四条旧表绑定。B76A4 原 ROM 为 `01207047`，即 `movs r0,#1` 与 `bx lr`，四字节单一 Function 计划成立。两处 B76E4 直接调用在 B7F6A 和 BAD80，其名称及所在 PLATE 属于后续模块内的有限投影。

## 状态 NEEDS_FIX（4 项）

### 1. C5 · 补齐全局 Equate 绑定与对象数量

`f15-seg2-global-equate-plan.json` 当前只覆盖 590 个 odd 类绑定。独立读 87 行 TSV 得到另外 65 个 EQ_ADD，分属 52 个名称，全部与该计划 161 个名称不交叠。以独立前态为基准把 52 个名称的准确旧值和完整旧绑定、拟增绑定与最终多重集写进机器合同。八个原缺失名称为 `ANTI_AIRCRAFT_FLOWER_CID`、`BEAST_SOUL_SWAP_CID`、`CATAPULT_TURTLE_CID`、`EQUIP_LEVEL_RESTRICTION_SCORE_THRESHOLD_2399`、`HADE_HANE_CID`、`LIGHT_OF_JUDGMENT_CID`、`MAGICAL_DIMENSION_CID`、`ULTIMATE_BASEBALL_KID_CID`。按当前动作范围更新为 213 个受影响最终名称、167 个新增、46 个复用、655 条绑定增量、两个退役，最终 2417 对象。同步 proposal、机器计划和校验计数。若第 3 项选择更名，按其闭包重新计算并解释相应净变化。

### 2. C2/C12 · 核正表分布、别名和消费者说明

B76A5 新表的分布按地址排序为 9、37、2、54、20，和两个旧 normal-summon 表的 79 条合计 201 条，覆盖七张表。修改“八张”的表述。六张相邻表的 57/165/3/5/207/70 行有独立指令证据，分别由 BB312、BB380、BB3A8、BB3CE、BB43A 和 BBA06 的 BLS 上界及 +8 步长确定。207 行表的另一基址源是 BB400，循环在 BB40A 截止，调用 `check_normal_summon_eligible_for_slot`。区分它与 BB488 的 `try_activate_equip_for_matching_slot` 路径，并登记证据专用的 BB3B0 为三行保留表基址源。后者仍维持原始 24 字节和 DB 状态。六处拟保留的受影响表基址字和 suffix 2892 字节继续精确保持。Equip 路径由 BAFBC 加载 row+4 并在 BAFC2 间接调用，row+0 在 BAEE0 读取。

### 3. C11/C12 · 现有谓词的名字与判定

- **B771C** · B7736–B773A 对 handler 结果做有符号 `>0`。当前 `check_effect_handler_result_nonzero` 若要保留，需给出该 handler 分派结果域非负的完整证据。分派函数在 `asm/11_effect_slot_puzzletext.s:18544` 将共享结果域清零、调用所选 handler、重新读取 32 位结果，本体没有非负限定。否则用 `check_effect_handler_result_positive`，按全 ROM 和调用闭包更新指针、两个直接 BL（B3408、B485E）、涉及该现名的 PLATE、Equate 及清单，并精确保留引用与函数身份。
- **B778C** · B7796–B779E 无条件传固定的 Dark Room CID，zone record 只供应侧别。第一次计数非零立即返回 1。第一次计数为零才以同一固定 CID 求另外两个计数，B77CC–B77D2 在二者之和等于零时返回 1。改掉“for CID ... otherwise”引出的按输入 CID 选路含义。
- **B7934** · B7948/B794A 先拒绝对手 active equip 为零。B7966 在对手 eligible-card 计数大于己方时立即接受，B796A–B7978 在对手 active-equip 计数大于 1 且大于己方时也立即接受。余下路径才需要限制卡、前置检查和 zone-score 门槛。B79C2–B79CA 精确条件为 activatable score 至少为对手 LP 或严格大于 2399，再要求 B79D2/B79D4 的正值比较。将短路分支与 score 组合明确写入 PLATE。

### 4. C12 · 两个外部调用者的精确测试

- **B7F64** · B7F80 调用 `count_slots_with_chain_field_match(opponent, 0, 1)` 后在 B7F84/B7F86 要求有符号结果严格大于零。用该阈值替代“checks the opposing player”。
- **BAD6C** · BADAC–BADB2 测槽 `[+0]` 的低 13 位 CID，BADBE–BADC2 测同槽半字 `[+8]==0`，BAD98/BAD9C 先把基址加 `0x10` 存到 r12，BADCC–BADD6 测平行状态 dword 的 bit7。把“slot word”明确成槽 `[+0x10]` 的状态字，避免指向存放 CID 的第一个字。保留条件分支及原 BL。

## Reviewer Verdict: F15-Seg-2 = PASS
