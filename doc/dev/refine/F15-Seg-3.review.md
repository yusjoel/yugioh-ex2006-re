# F15-Seg-3 独立复核

## 第三轮 · PASS

最终冻结清单 SHA-256 为 `b9e767a93d2427aa8bcdc4219145dbddb704026b17578f5b552ab7cd7ae081d1`。独立核验 44 项冻结路径和 v3 归档 46 项。相较 v3，正式 PLATE 表仅 B88C4 文本与长度变化，Function 和语义 JSON 仅该入口的文本变化。最终证据 `f15-seg3-review-round3-final-independent.json` SHA-256 为 `2183a5da74f273dd14a193277ea008f041b0e14a560aab832b3b28bc2b7c422f`。

第二轮两项修订闭合。45 个入口的 PLATE、名称、半开范围对、引用及空列表已在被消费的合同中逐入口对齐。52 条 PC READ 在 R4、Function 与正式 PLATE 引用投影均为 operand 1，来源 DEFAULT 且 primary，三者逐对匹配。58 槽维持第二轮字节一致，原两段 raw 几何和 67 表源维持首轮批准范围。

七条 PLATE 逐项复核通过。B7BB8 保留 owner placement、node、slot 与并行状态门槛，B7CD8 匹配固定 CID 的短路，B7D6C 匹配空槽跳过与双通道交叉，B7EB8 恢复 slot 11 的早拒绝，B8698 恢复 active handler gate，B8720 区分 packed 参数与 bonus 返回值。B88C4 最终 494 字符明确区分 hand selector 与恒真 B88C0。原 ROM B88C0 为 `01207047`，B8914 加载其 Thumb 指针，B8916/B8918 设置 r2/r3，B891A 调 selector，B8922 对 selector 返回值做负值拒绝。新文本正确归属 PRNG 副作用和排除索引。

C1–C13 通过。全局 Equate 对象 2421 个、最终绑定 12238 条，203 个后续表源保持冻结。方案可进入落地及整 ROM 逐字节验证。

## 第二轮 · NEEDS_FIX（2 项）

本轮冻结清单 SHA-256 为 `06c74e13d22a5b787d76f64720495c3d1c799f3cfaa56cf60ce468dc34ce6943`。41 项冻结输入及首轮归档摘要已独立核验。全局 Equate 计划已冻结 2421 个对象和 12238 条最终绑定，C5 通过。R4 的 52 条 PC READ 主清单已改成 operand 1，CFG 和表范围保持原批准几何。独立对照证据 `f15-seg3-review-round2-independent.json` SHA-256 为 `28e6cf991d2a53022453a460adff380ea3b8828e70bbb30e304a19a09b2ba209`。

### 1. C7/C12 · 清除仍与主计划矛盾的冻结派生数据

- `f15-seg3-function-plan.json` 的 `plate` 仍含 21 条旧文本。将其与 `F15-Seg-3.plates.tsv`、`f15-seg3-semantic-plan.json` 的最终文本逐入口精确同步。
- 52 条新 PC READ 在 `f15-seg3-r4-plan.json` 主表为 operand 1，但 `F15-Seg-3.plates.tsv` 和 `f15-seg3-function-plan.json` 的最终 body refs 中仍全部为 operand 0。按 (from,to) 仅改这 52 条，所有其他 READ 和引用字段保持。复提时要求三份清单的该子集逐条一致，再在后续无保存验证确认。
- Function plan 的 B88C0 `final_body_refs` 和 B79F8/B7A48 `final_incoming` 仍为 `[null]`，正式 TSV 对应字段已是 `[]`。28 个 `final_body_ranges` 还与正式 TSV 的嵌套格式不一致。将各被消费合同统一成半开范围对数组，校验每个地址对、body 长度和 SHA 保持，空列表使用 `[]`。更新所有冻结派生物，禁止 Mode B 从旧文本或旧引用投影落地。

### 2. C12 · 补齐修订 PLATE 丢失的必经条件

- **B7BB8** · 保留第二轮准确的 available+1 与 dispatcher 等值条件。补回 B7BCC/B7BD2 己方 field-spell placement、B7BEA/B7BF0 非零 node handler、B7C06/B7C0C 非零 slot eligibility，以及 B7C38/B7C3A 的 bit22/23 至少一位设置。门槛 helper 在 B7C76 为 `get_equip_display_type_code_by_card_id`。
- **B7CD8** · B7D10 在第一个固定 CID 计数非零时跳过第二次调用。将 “gets two pair counts” 改为按实际短路求值。
- **B7D6C** · B7DAC 和 B7DC2 跳过空 CID 或 +8 为零的对侧槽，再应用已修正的严格交叉条件。max 是 B7D82 写入 `sp[0x24]` 的主通道最大值。
- **B7EB8** · 补回 B7ED0–B7ED8 的短路。对侧 slot 11 已含 Mesmeric Control CID 时直接拒绝，然后才求 peak 并扫描。
- **B8698** · B86C6–B86CC 要求 active node handler 非零才读取 field5 参与 best 比较。补回该条件。
- **B8720** · B87AE/B87B8/B87C6 分别要求 hand CID 的 field5 非零、无 equip-placement type、己方可用怪兽槽计数非零。packed 表达式 `2*bits[29:22]+bit13` 是 B87FE 的参数，bonus 是该调用的返回值。明确 5–6 接受、>6 才调用 resolver(owner,1)、≤4 或 resolver 负值仅跳过当项。
- **B88C4** · 补回 B88E0/B88E6 的对侧 placement count >0、B890A/B8910 的己方 LP-block +0x11c bit17 清零，以及 B8974/B897E/B898C 的三个逐项门槛。B891A 的 selector 在候选替换时可由 B5A02/B5A16 推进共享 PRNG。保留已修订的 selector 负值拒绝和非负索引排除。

第二轮已通过 B7A68、B7B18、B8090、B80BC、B8208、B8330、B8398、B849C、B8568、B85B0、B85D4、B860C、B8658、B885C 的语义修订。上述两项闭合时保留它们及当前批准名称、函数 ABI、64+3 表源和 203 个未来源。

## 首轮复核记录

范围 `[080b79f8,080b8a24)`。冻结清单 SHA-256 为 `bb35d72cd50c85e9f5b5152d0839a3e7baa8f30a887730f3cfe7b5c2472f26b5`。独立核验 38 项输入。证据 `f15-seg3-review-independent.json` SHA-256 为 `0ec6c038e4ec1493812ec54b8574214f616b9dffe8910fb761847ba6858f4f94`。

## C1–C13

| 项 | 结果 | 依据 |
|---|---|---|
| C1 | PASS | `doc/dev/refine-progress.md:12` 顺序段 |
| C2 | PASS | 两个原始块共 3512 字节，1545 条指令、50 个池字和 29 段零填充 |
| C3 | PASS | 按全部 ROM 字节偏移重扫两范围内所有值，64 表引用和 17 资产重合。各资产文件及尾部窗口与 ROM 一致 |
| C4 | PASS | 58 槽原值和原字节一致 |
| C5 | FAIL | 完整全局 Equate 合同未冻结 |
| C6 | PASS | 稳定源标签 |
| C7 | FAIL | 52 个 R4 PC READ 的 operand 需核正 |
| C8 | PASS | 当前或计划名称引用 |
| C9 | PASS | 58 EOL 和 45 PLATE 全部 ASCII，长度符合限制 |
| C10 | PASS | 67 表源、3 段内 Thumb 槽的奇值到偶址合同，203 后续表源受保护 |
| C11 | FAIL | B885C 的接受极性与现行语义投影不符 |
| C12 | FAIL | 多条分支、返回和副作用说明与指令不符 |
| C13 | PASS | 8 现有自动槽、50 新池、38 raw Function 和 B88C0 typed leaf 均覆盖 |

## 状态 NEEDS_FIX（5 项）

### 1. C5 · 全局 Equate 合同

合并 29 标量、3 段内 Thumb、67 表源的逐名称、值和 operand 绑定多重集。41 个旧对象只在全部绑定迁移且零引用时退役。当前命名下，Root 独立推导为 2417→2421 对象、45 新建、41 退役、8 复用扩展，绑定 12206→12238。绑定 `root-f15-seg3-global-equates-expected.json`（SHA-256 `911075bcde9b64fb9f8154525955e57635c453ecd6ee349e5d677be1e8a5db4c`）或其语义更名后的等价冻结结果，并保护 203 个后续表源及其全局绑定。

### 2. C7 · PC READ 与序列化

新池 52 个 PC-relative LDR 的 READ 当前记 operand 0，同型 typed B79FE→B7A34 实际为 operand 1。按同型修订，并在无保存反汇编中复核 exact CORE6 与反向列表。池字的 Equate 保持 operand 0。清理 TSV 中 29 个 `after_refs_from_json`、26 个 `after_equates_json`、2 个 `final_incoming_json`、1 个 `final_body_refs_json` 的 `[null]`，空列表统一为 `[]`。R4 plan 的平面范围与 PLATE 的嵌套范围需统一为半开范围对列表，或冻结无歧义的字段级解析规则。保留 B8514→B84D8、B88B0→B8720 的真实 BL 与 B88C0 的既有两条指令。

### 3. C12 · 首半段谓词及 De-Fusion

- **B7A68/B7B18** · B7AB8–B7AD0、B7B54–B7B6C 测 owner 并行槽状态字 bit22/23 至少一位为 1，替换 “score relation”。B7B88–B7B8A 只要求 signed field5 ≤4。
- **B7BB8** · B7C76 的候选 CID helper 返回门槛 r4。B7C82–B7C8A 要求己方可用怪兽槽数 **加 1** 不小于门槛，B7C92–B7C9C 要求 activation-record CID 的 dispatcher 返回值恰等于同一门槛。B7CA2/B7CA8 以候选 CID 和 `gEquipLpZoneEntryBase` 调 criteria builder，非零接受。bit22/23 位于并行状态字 +0x10。
- **B7CD8** · B7D00–B7D02 在对侧 LP-block [+0x14] >4 时直接返回 1。否则以固定 Reversal of Graves CID 求 pair count，两个 count 至少一个非零便继续（B7D10 跳过第二计数）。随后要求自己 LP >1000（B7D36/B7D38）及自己的 [+0x14] >14（B7D46/B7D48）。删除有界扫描和双正值门槛。
- **B7D6C** · B7DF2–B7E10 对侧槽 [+6] 非零时要求 `sp[0x18]>max>sp[0x14]`，为零时要求 `sp[0x14]>max>sp[0x18]`。
- **B7EB8** · B7F0E/B7F10 要求非零 CID，B7F20/B7F22 要求 [+8]==0。B7F2E 后仅要求 score < peak。将三项分别写明。

### 4. C12 · 分支极性与参数

- **B8090** · B8094–B809C 按 record[3]&0x30 二选一。非零时返回 resolver(owner,0) 非负，零时以原 record 调 pair gate。
- **B80BC** · B8104 按 record type ≤10 分流。四计数之和在 type ≤10 时要求 ≤1，否则要求 ≤0。通过后返回 zone-max 的符号位。
- **B8208** · B8214 在 record[3]&0x30 为零时直接接受。非零时，B8246 对侧计数 ≤1000×set_code 也直接接受。超界才同时要求 available effect zones >1（B8256）及 set_code >1（B825A）。
- **B8330** · B835C 在己方占用槽的 tier 非零时立即接受。扫描无命中才要求己方 occupied count 恰为 1（B8374），且己方 zone-max 比较 <0（B8382）。
- **B8398** · record[3]&0x30 为零直接走 B83D8 pair gate。非零时只有对手 whitelist count 和 occupied monster count 均为零才给 1（B83BC/B83CC/B83D2）。
- **B849C** · B84BE 要求 zone-max 正值后才到 pair gate。
- **B8568** · B8574–B857C 要求对侧 active-equip count 非零，B8598–B859E 只在己方场地槽 CID 为零时给 1。
- **B85B0/B85D4** · B85BC–B85C0 和 B85F4–B85F8 均传 (other,1,0)。B85D4 第一 gate 是 hand helper 非零（B85E4），链计数才要求正值。
- **B860C/B8658** · Dark Hole 在 score/LP gate 非零或 owner zone-max <0 时接受（B861C/B862A）。Raigeki/Lightning Vortex 将两者作为早接受，均失败才检查 effect-node count >1（B8668/B8676/B868A）。
- **B8698** · B86B4 允许 owner zone-max ≤0。B86E6/B86E8 扫两侧各五槽。best 初始 -1，只在 field5 严格升高时更新获胜侧，B86F6 比较获胜侧是否为对手。

### 5. C11/C12 · B8720、B885C、B88C4

- **B8720** · B873A 要求 `count_equip_placements_with_chain_check(other,0,1)>0`，B875C–B8764 测己方 LP-block +0x11c bit17 清零。B87FE 的 bonus 输入用手牌 packed 字 `2*bits[29:22]+bit13`，B880E resolver 参数为 (owner,1)。bonus≤4 或 resolver 为负仅淘汰当项，扫描继续到 B8840。
- **B885C** · B8872 从对侧读取槽。B8890 的 eligibility 非零时 B8898 立即返回 0。只有五槽都未触发 blocker 才在调用点 B88B0 委托 B8720 并原样返回。名称和注释须准确体现这一极性。
- **B88C4** · B891A 以恒真 B88C0 和 r2=r3=1 调 hand selector。B8922 在返回负值时直接拒绝，非负才在后续扫描排除该索引。selector 的 B5A02/B5A16 可推进共享 PRNG。后续候选 bonus 5–6 直接接受，>6 要求 resolver(owner,1) 非负，≤4 或 resolver 负值只淘汰当前候选。名称宜使用 bonus，与 `eval_equip_bonus_for_slot` 一致。

同步 PLATE、语义与 Function 计划、表名投影、Equate 和冻结摘要。保持原 ROM 字、当前 Function ABI、B88C0 的 typed 指令及未来 203 个表源。

## Reviewer Verdict: F15-Seg-3 = PASS
