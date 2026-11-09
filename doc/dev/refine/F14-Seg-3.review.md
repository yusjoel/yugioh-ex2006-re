# Refine Review: F14-Seg-3（最终 EVEN-FUNCTION amendment）

## 复核对象与输入完整性

- 范围：`asm/14_equip_ai_scoring.s [0x080aa120,0x080aba78)`，6488 bytes。
- proposal SHA256：`de4aaf39ce3ab7f9540816a331f0df26f253451f99c7fea3455c0f2aa4bca018`。
- slots SHA256：`370def5e0e4bb363827bb8c9f47eadf512a5ee63b70d3150586eb86556fdb20f`。
- plates SHA256：`a9e41dd029dbb747f9378d17337e8026ed748387b8c6b3802acc8ea35b35bcfd`。
- projection contract SHA256：`cc60560d717af799e24da92304dd345ecd259b758ada89aa96995d57f3747776`。
- machine contract SHA256：`ecd6922ab4690225fc3c09cc1cacb25dc09589bcfc94914eb72e3494a987b989`。
- freeze manifest SHA256：`95abbfdd0be71b85449af97518002c052ab92973ac46e404df04a09919e18319`。独立重算 25 个 `review_basis` 输入，0 个 hash drift。
- 第二轮完整语义 PASS review 已不可变归档于 `output/refine-run-20261028-105948/f14-seg3-review-round2/doc/dev/refine/F14-Seg-3.review.md`，SHA256 `bf50f3dfc32f0a5ebef98ffc1cea60b123ba4ac6cd5eeaf2be9f4cee6065849a`。
- 独立最终 amendment 证据：`output/refine-run-20261028-105948/f14-seg3-final-export-amendment-audit.json`。

P0 通过：正式 proposal/slots/plates 存在且非空，未含禁止的占位或跳过标记。amendment 未改 plates、function plan、constant plan、R4 map 或 Exporter；其 hash 与第二轮 PASS 输入连续。冻结门禁记录 98 份 source 与 15 个物理 DB 文件均未被 amendment 修改。本轮没有运行 headless、build、stage 或 commit。

## 首轮证据连续性

首轮独立复核的 ROM、R4 map、full-ROM refscan、prestate 与 source-format prediction 在最终 21-input manifest 中保持原 hash，可直接延续以下已独立验证事实：

- 五个 raw block 的 1667 个偶地址候选已逐个扫描，得到 raw=25、THUMB|1=2；23 条 raw 命中属于指向 raw code 的 table sources，另 5 条 table sources 指向既有 `aaf54`，四项额外命中均已定位为资产偶合。五块均有真实 table/direct CFG 入口，Section 5.1 为 0。
- 1411 条新增指令逐 opcode 对 ROM 核验通过：2938 code bytes、90 pool words、18 zero-pad halfwords、40 maximal ranges、248 direct flows、58 calls、95 PC reads、1338 API fallthroughs，无空洞、重叠或 FlowOverride。
- 206 槽完整覆盖 116 current words 与 90 new pools；ROM 小端值、current Data/symbol/ref/equate/EOL、PC-read target set、GAS expression 值、label 唯一性和 ASCII EOL 均已逐项通过。
- 五个 Function body 的 size/SHA/ranges、5596-byte final body union、`ab278` Data/ref 保留及 27 条 shared-owner edges（`aaf54` owner 4、`ab200` owner 23）已独立通过。Mode-3 frame/prologue 与既有 shared tails 的 ABI restore 配对保持。

## 首轮五项修改闭环

### #1 `0x080ab6d0` ref-preserve

`slots.tsv` 仅将该行 action 从 `REF_ADD` 改为 `REF_PRESERVE`；原 `/dword`、source symbol、READ ref、EOL、operand-0 `DATA/USER_DEFINED/primary` ref 及 `gP1LifePoints` Symbol ID `15545` 均未变。最终计数为 `REF_ADD=30`、`REF_PRESERVE=1`、`REF_MATERIALIZE=25`，REF 总数仍为 56。机器合同明确禁止删除、重建或升级该 CORE6 ref。

### #2 `0x0201b754` LP-bar counter

- `gDuelPhaseFlags=0x0201b290`，`LP_BAR_DISPLAY_CTR_OFF=0x4c4`，算术结果精确为 `0x0201b754`。
- `asm/05_equip_eligibility_a.s:3237-3238,3304-3305,3361-3362` 的独立消费者对该域执行 LP-bar display counter 增减；`0x080ab46a` 只读取相同 counter 选择局部路径。
- 最终全局定义合同是 `.equ gLpBarDisplayCounter, gDuelPhaseFlags + LP_BAR_DISPLAY_CTR_OFF`；slot `0x080ab494` 的 exact USER target 与 GAS expression 均为 `gLpBarDisplayCounter`，不存在同址旧 symbol/alias。
- `tools/asm-regen/ghidra/ExportRangeToGas.py:527-582` 的现有 resolver 会从 primary ref 取得 RAM target 的 USER_DEFINED primary symbol并返回 sanitized label，因此原生导出为 `.word gLpBarDisplayCounter`；base+offset 复用只放在 `.equ` 定义。Exporter SHA256 `4544a6a95f922f5a1779553555180ed2184955bc4fc1e92f96ad9b500ddaeb87` 未变，无需专槽或全局放宽。

### #3 canonical inventory 与 CSV

最终合同明确只同步：

- `temp/ghidra-functions.csv`
- `temp/ghidra-functions-renamed.txt`
- `temp/ghidra-functions-auto.txt`
- `temp/ghidra-functions-summary.md`

当前实测为 5214 Functions / 5124 renamed / 90 auto；后态计数不变，只更新 3 个名字与 4 个 body lengths。`doc/dev/naming-proposals.csv` 当前 5079 data rows，合同只改 `aa120/aa77c/aaf64` 三个既有 row 的 `name` cell，保持顺序和其他字段。`tools/ghidra-labeling/ghidra-functions.*` 明确列为 legacy stale copies并保持不动。

### #4 `ab200` selector bitfield

`asm/14_equip_ai_scoring.s:5996-5998` 的 `ldrh; lsl #23; lsr #29` 确实提取 halfword bits `[8:6]`。proposal、function plan 和完整 PLATE 已统一为 `[8:6]`。新 PLATE 独立重算为 500 ASCII chars，SHA256 `8957ee038f630349580f704f6f0a45071836a96aeabfa95d66021300be425dda`，符合 `<=500` 合同。

### #5 `ab278` 局部 body range

最终文字明确只有受影响局部 range 从 `[080ab238,080ab27a)` 收到 `[080ab238,080ab278)`；整个 `ab200` Function 仍为 23 ranges、2424 bytes并延续到 `0x080aba50`，final SHA256 仍为 `64c7172d01bc2be293ae7c27e9ecf51b8cfb0f79890fa948a318be05f04bf940`。`ab278` 4-byte Data、READ、symbol、EOL 与 bytes 均不删除。

第二轮逐字段 delta 复核结果：206 槽中只有 `ab494` 的 7 个语义/投影字段与 `ab6d0` 的 action 改变，其余字段精确相同；5 条 plates 中只有 `ab200` 的 `new_plate/new_plate_chars/registry_contract/inventory_contract` 改变，其余 prestate、body、incoming 与其他四行精确相同。未发现新增矛盾。

## EVEN-FUNCTION native export amendment

### 五个 table sources 与两层引用

独立读取原 ROM 后，`0x080aa7c0/c4/c8/cc/d0` 五个 word 均为 bytes `54 af 0a 08`，little-endian value `0x080aaf54`。五行 TSV 均满足：

- source 仍为 4-byte `/undefined *` Data；原 operand-0 `DATA/DEFAULT/primary` MemoryReference 精确指向 `0x080aaf54`，target primary 仍是 USER Function `exit_equip_phase_oob_epilogue`，Symbol ID `16957`。
- 前态 `equates_json=[]`；后态各有一项 `{"name":"exit_equip_phase_oob_epilogue","value":"0x080aaf54","operand":0}`。
- EquateReference 属于 EquateTable 的 scalar-operand 投影，不是 ReferenceManager 的 DATA ref。amendment 因而只创建一个 global Equate 并绑定五个 operand-0 EquateReferences；五条 MemoryReference、target Function、同址 Symbol 集合和 incoming refs 的 projection delta 均为 0。
- `projection_only` 不覆盖整段职责：AAF54 的已批准 PLATE 与 R4 old+new incoming 仍分别由 plates TSV、function plan 和 R4 map 执行。

当前 slots 与第二轮不可变 slots 逐字段比较：206 行仍一一对应；新增 `after_equates_json` 列覆盖 206/206 行；旧字段只在上述五行变更 `action/consumer_evidence/id_contract` 三项，其他 201 行全部旧字段精确相同。全部后态 JSON 可解析并规范化为单项或空数组：127 行非空 = 57 `EQ_ADD` + 65 `EQ_MATERIALIZE` + 5 `TABLE_ENTRY_EQUATE_EVEN_FUNCTION`，其余 79 行为空；91 个 distinct Equate names 无同名异值冲突。

### 原生 Exporter 可实现性

`ExportRangeToGas.py` SHA256 仍为 `4544a6a95f922f5a1779553555180ed2184955bc4fc1e92f96ad9b500ddaeb87`：

- `tools/asm-regen/ghidra/ExportRangeToGas.py:549-575` 先解析 primary target Symbol；ROM target 是 `Function` 而非 `Label`，因此 symbol resolver 返回 `None`。
- `tools/asm-regen/ghidra/ExportRangeToGas.py:585-604,632-637` 随后从 source Data 地址读取 Equate，返回 sanitize 后的同名 expression。
- 现有 GAS label 定义在 `asm/14_equip_ai_scoring.s:5834`，值即 even address `0x080aaf54`。所以五槽原生导出为 `.word exit_equip_phase_oob_epilogue`，值与 ROM 一致；不使用 `+1`，不创建 odd target、同址 Label alias、Exporter 白名单或手写 source projection。
- RAM counter 路径没有被混用：`gLpBarDisplayCounter` 的 USER RAM Label 在 symbol resolver 阶段直接成功；五个 ROM Function table words 才进入 Equate fallback。

当前 `tools/ghidra-labeling/RefineF14Seg3.py` SHA256 `b4676b5771c84117f7cd5b9f4f7db3dbfb4e31d413761a702a74fb4a04784784` 是 amendment 前、尚未 apply 的 Phase-1 draft，不是冻结 proposal 的既成后态。Mode B 在 apply 前必须按 `after_equates_json` 增加 `TABLE_ENTRY_EQUATE_EVEN_FUNCTION` 的 apply 与 persisted-check 分支：create/reuse 单一 exact-value Equate、精确添加五个 operand-0 EquateReferences，并断言原 DATA refs及 Function ID16957 不变。该实现动作已由当前 amendment 合同完整规定，不构成 proposal 缺口。

## 核验（C1-C13）

| # | 检查 | 结果 | 备注 |
|---|---|---|---|
| C1 | Rule 1 地址序 | ✅ | 活动路线图的 Seg-3 为 `[080aa120,080aba78)`；Seg-1/2 已完成，地址序连续。 |
| C2 | Rule 2 raw 块归宿 | ✅ | 5 块 raw、3334B 全部进入 40-range R4 disasm，无静默保留。 |
| C3 | Rule 3 / full-ROM ref-scan | ✅ | 1667 候选的独立 raw/THUMB 扫描证据 hash 未变；真实 table/direct-CFG 与四项资产偶合已分离，Section 5.1=0。 |
| C4 | R1 槽值 | ✅ | 206/206 槽的 ROM 4-byte little-endian 值与合同一致；Mode A 未改任何 raw value。 |
| C5 | R1 常量复用 | ✅ | 15 项新增定义中，LP counter 正确复用 `gDuelPhaseFlags + LP_BAR_DISPLAY_CTR_OFF`；其余 14 项维持首轮已通过的同值/同域审计。definition expression 与 native slot expression 已明确分离。 |
| C6 | R2 命名形式 | ✅ | source/target labels 均合法且唯一；`gLpBarDisplayCounter` 语义与全局消费者一致，无同址 alias。 |
| C7 | R3 DATA ref 接通 | ✅ | `ab6d0` 现为严格 `REF_PRESERVE`；最终 REF 计数 30 ADD + 1 PRESERVE + 25 MATERIALIZE。28 table refs及16 unique targets守恒；其中五个 even Function sources 保持 DATA ref CORE6，并另以一个 global Equate/五个 operand-0 EquateReferences提供 native source projection，MemoryReference 与 scalar Equate 层明确分离。 |
| C8 | R5 PLATE 现名与事实 | ✅ | 5 条 PLATE 均用 final names；`ab200` 已订正 bits `[8:6]` 与 affected local range，whole Function end 明确为 `aba50`。 |
| C9 | ASCII | ✅ | 5 条完整 PLATE 与所有新增 EOL 均为 ASCII；长度 419/489/343/412/500，全部不超过 500。 |
| C10 | carve / THUMB `+1` | ✅ | carve=0；五槽 ROM raw value 与 GAS Function label 均为 even `0x080aaf54`，明确不加 `+1`、不建立 odd label/Data/ref。三个 rename entries 的 full-ROM raw/THUMB pointer hit 均为 0。 |
| C11 | 函数误名 | ✅ | 三个 rename 与 controller selector、combined-index dispatch和真实 callers一致；`aaf54/ab200` 名称与 body/shared-tail职责不矛盾。 |
| C12 | R6 证据与可执行合同 | ✅ | LP counter、selector、local range、REF preserve、native exporter、canonical inventory/CSV合同均有具体 file:line/value/ID 证据；27 shared-owner edges及ABI合同保持。新增 projection action 的 apply/persisted-check、Equate singleton/value/ref set及DATA-ref/Function不变量均已冻结为可执行后态。 |
| C13 | 自动槽残留覆盖 | ✅ | 116 current words + 90 pools 完整唯一覆盖；206 行均冻结 `after_equates_json`，127 equated slots=122 literal+5 projection，TABLE=23 materialize+5 even-Function projection；40 code ranges、18 pads、16 table targets均有后态。 |

## 状态：PASS

首轮 #1-#5 与 EVEN-FUNCTION native export amendment 全部关闭，当前 25-input 冻结合同未发现新问题。允许恢复 Mode B；仍须先把 amendment action/materialized-check 实现进尚未 apply 的 draft，再按 proposal 的 ROM byte-identical、Instruction/API、ref CORE6、Equate singleton/ref set、Function body/incoming、registry/CSV/canonical inventory 与 98-source/15-DB 后态门禁执行。

## Reviewer Verdict: F14-Seg-3 = PASS
