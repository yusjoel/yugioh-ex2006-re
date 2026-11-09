# Refine Review: F15-Seg-4（Round 3）

本轮冻结为 Mode A v3，范围 `[080b8a24,080babd4)`，manifest SHA-256 `f0d767d4a06c24203f43a76d69f3073e3c415bdb64c17025c36ce0a45ae250f9`。41 个摘要记录（39 个不同路径）、156 个现有及快照源码和 15 个 DB 现有及备份文件均独立核验一致。复核只修改本文件和 ignored 审计 JSON。

独立证据 `f15-seg4-review-round3-independent.json` SHA-256 `70f890668e33061353dacd68cf375c3f3e5efb4ec8d03b3800bb789464b1f675`。前两轮复核和对应机器计划已归档，本轮以 round2 的三个可执行项目为检查基线。

## 核验 (C1–C13)

| # | 检查 | 结果 | 备注 |
|---|---|---|---|
| C1 | Rule 1 地址序 | PASS | 当前活动路线图 Seg-4，连续接在 Seg-3 之后，范围精确一致 |
| C2 | Rule 2 原始块归宿 | PASS | 原始 8578B 精确分为 7920B 指令、520B 池与 138B 零填充；94 CREATE 和 144 body ranges，无遗漏 |
| C3 | Rule 3 全 ROM 引用 | PASS | 本轮再次按四相滑窗扫描 raw 范围内全部值，202 真表源及 9 个数值重合与前轮逐项相同；资产和未对齐值分类证据不变，无新 §5.1 |
| C4 | R1 值与字节 | PASS | 130 槽原字节/小端值和 3714 条指令再次直接比对原 ROM；69 段零填充及范围几何与上轮精确相同 |
| C5 | R1 复用及常量域 | PASS | 3 个 GAS 新定义与 BOOK_OF_LIFE 已有定义复用清楚；2900 是对侧 LP，目的文件 duel_field.inc；完整 Equate 计划不变 |
| C6 | R2 槽名及碰撞 | PASS | 130 唯一池标签和 94 新 Function 名称不变；现有单 Function 身份保持 |
| C7 | R3 接通及 canonical | PASS | 135 PC READ operand1、43 DATA 与 2 Thumb 源合同明确；95 Function、94 R4 Function、130 Slot/CFGPool/R4Pool 逐字段一致；BA5B8 EOL 三副本修复 |
| C8 | R5 现名 | PASS | PLATE、table alias、目标与当前/最终名称一致；旧前态身份字段保留 |
| C9 | ASCII | PASS | 94 CREATE PLATE 纯 ASCII 且≤500，最大491；587字符旧 PLATE 为 PRESERVE。130 EOL 纯 ASCII |
| C10 | THUMB | PASS | 202 表词等于目标加一，94 alias 迁移与原 ROM 字节不变；两个 04AEA1 回调保持只向偶地址补 DATA 的合同 |
| C11 | 误名检查 | PASS | 94 新 Function 命名与真实主体和 CID 证据相符；本轮未变更名称或签名 |
| C12 | R6 语义证据 | PASS | 下表 9 条修正逐指令通过；此前通过的28条文本保持精确一致，未丢失已准确门槛或状态效果 |
| C13 | 残留及交接 | PASS | 整段代码/池/pad 全覆盖；202 当前表源与 Seg-5 单源保护不变。外部 04BECC 正引用 raw 依赖显式保护与交接 |

## 三组修改清单闭合

### 1. 错误谓词已订正

| 入口 | 独立确认的接受条件 | 关键指令 |
|---|---|---|
| B97B4 | byte3&0x30==0 时 target<0 拒绝；其余由 B76E4 pair-slot-count 返回值归一化决定。另一路派生 side、读取 display value，并要求 dispatch signed>0 | B97C0/B97DA/B97E0/B97E4–B97E8/B980E |
| B98F0 | owner zone maximum<0、手牌数>3；仅一次 owner 手牌扫描，任一 activation!=0 或 eligible-set!=0 拒绝，扫描全部通过直接返回1 | B9908/B9924/B9978/B9984/B999E |
| BA29C | effect-zone 和 slot-activatable 均非零；扫描 opponent 0..4 非空槽，按+6选择 channel。unsigned(score−1000)≤999 精确限定 1000..1999 | BA2AC/BA2C0/BA318/BA32A–BA332 |

### 2. 必经门槛、槽过滤和状态效果已补齐

| 入口 | 本轮确认结果 | 关键指令 |
|---|---|---|
| B8EAC | owner LP signed>2000；stride8表扫描在CID0x1379结束。候选先写局部record，field6==0x16、opponent extra-deck count!=0、indirect!=0、zone-block!=0；仅最终成功把CID提交到gEquipLpScoreBase+0x14并返回1，失败继续 | B8ECE–B8ED6/B8EFE/B8F08/B8F20/B8F2E/B8F3A/B8F40→B8EE4–B8EEA |
| B8F68 | effect-zone!=0且opponent occupied count>0；owner0..4仅CID!=0和+6==0更新初值0的field5最大值。opponent候选CID!=0、+6!=0，channel1≥max>channel0 | B8F82/B8F9C/B8FC8/B8FDE/B903A/B9050/B9064–B906C |
| B90D0 | 同样的前置门槛与owner初值/过滤；opponent候选CID!=0、+6==0，channel0≥max>channel1 | B90EA/B9104/B9130/B9146/B91A2/B91B8/B91CC–B91D4 |
| B91F8 | effect-zone!=0；owner0..4同样由初值0过滤取max。opponent handler!=0；+6==0时channel0≥max>channel1，非零时channel1≥max>channel0 | B9214/B9240/B9256/B92A2/B92CC–B92F2 |
| B9C50 | pair!=0；opponent0..4的CID!=0、半字+8!=0；signed field6≤固定2500接受，全部耗尽给0 | B9C64/B9C90/B9CA2/B9CB2–B9CBA，literal B9CD8=0x9c4 |
| B9D8C | Toon World或Exodia compound pair!=0早接受；owner0..10仅CID!=0、半字+8!=0且外部八CID谓词!=0接受；耗尽给0 | B9DA4/B9DB6/B9DE6/B9DF6/B9E0A/B9E12/B9E1A |

九条修改都只改变 `new_plate` 和字符数。semantic 对应九行只改变 `decision/plate/plate_chars`，且 decision 是正式 PLATE 的实际行为前缀。其余86行 PLATE 的每个字段和此前28条已通过改写精确不变；未增减命名、属性、body、签名、引用或 machine flow。

### 3. EOL canonical 已订正

`0x080ba5b8` 的 formal slots、slot-plan、R4 pools、CFG pools 现在逐字相同：

> RESPONSE_OPPONENT_LP_THRESHOLD_2900: opponent LP threshold used by 0x080ba578.

BA53C 的 BA578 READ rich target label 保持新 LP 名称；所有源槽字段与上一轮 byte-exact。

## 约束与落地基线

- 三份正式文件摘要：proposal `cbe4c37a5b71531e69ab029133ae49a8c073e51befe744569eee4b4a73d62db9`；slots `b57275962233f17053935dc6f54dfd1b417b4b03540ae975f543cd3211f44dc9`；plates `3c9a154f7952834f47ec04256cb46bd9eb4b027c54d4427b37881e530f38390e`。
- 全局计划保持上轮独立完整重算的2425对象/12325绑定，文件摘要 `fceec1f397a4699fb813cef815cd787f3c0ecf45cf7f7a528b8e4c3428321ee7`；现有作用域与引用多重集不变。
- 表源计划摘要 `a17e6b19f78fdaaaa1631e9fc5b6706cacba1442d6cd5085a5f08b84d512e3e4`；202当前词、94迁移及Seg-5的09E48E9C→080BACCC+1精确保护。
- 04BECC `[0804becc,0804bf20)` 84B 是既有正引用覆盖缺口。只读前态摘要 `5455d01ee7d57829e4e4cf278aa367b7e85542945f11c23a4477ec32114b646b`、现有BL04D374和本段新BLB9E0A已绑定。当前落地保持外部raw和身份；驱动器落地后须同步历史§5.1重分类及后续单独闭合交接。
- 本轮为 proposal 静态批准。Mode B 必须绑定此冻结，按原批准的94创建、130池、144ranges与引用/Equate合同实施，并完成事务前后守卫、持久化检查和ROM逐字节验证。

## 状态: PASS

## Reviewer Verdict: F15-Seg-4 = PASS
