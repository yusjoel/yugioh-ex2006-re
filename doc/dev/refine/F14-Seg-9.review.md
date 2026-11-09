# Refine Review: F14-Seg-9

## 第四轮状态: PASS

最终冻结清单 SHA256 为 `39fc3abcf312ac41932b2ab8dcb275c7bd02def5fd6936feadb9ca0eb63d14c9`。47 项冻结输入逐项匹配。独立审查记录 `f14-seg9-semantic-review-round4.json` 的 SHA256 为 `463bc088b15963b763be30395529e8edcea77807c6224dd9b7732ee4061d2361`。

B2028 的 Just Desserts CID 已改为 `0x1301`，B28AC 的 Fiend Comedian CID 已改为 `0x151d`。两个值分别来自原 ROM 的 `0x09e47f10` 和 `0x09e47eb0` 记录。逐字段比较 63 条 PLATE，只有这两处等长文本替换。59 条新函数 PLATE 的显式 CID 均与原 ROM callback 表对应。

提案、槽合同、CFG 和表合同与第三轮逐字节一致。此前通过的控制流、阈值域、回调返回和表边界证据仍适用。C1–C13 全部通过。

## 第三轮状态: NEEDS_FIX

本轮绑定冻结清单 SHA256 `62e6615aa565edf9f5ab2142a53db0c630a0b06ae49c6469e30032694a1b7261`。独立记录 `f14-seg9-semantic-review-round3.json` SHA256 `397af5d23253dac81bbaae6f154d10a208700773423847a575d87015c73721a2`。

C1–C11、C13 通过。两张表、CFG、body 范围及原 ROM 保持。第二轮的五项已修正。B2028 的两个判断都用对手侧。B2D38 拒绝 recorded-player 相等。B2EEC 的 B3782/B3784 记录原始 u16 返回。四个阈值的槽字节和 operand 0 绑定经独立核对，B1FA8 与上一轮逐字段一致。所列调用、比较及保存证据已与机器指令对齐。

C12 剩下两条第三轮改写引入的卡 ID 错误。用原 ROM 两表的每条 8B 记录核对过所有带 `Table identity` 的 PLATE，只有以下两条不匹配。

1. B2028 的 `Just Desserts 0x138d` 改为 `Just Desserts 0x1301`。原表 `0x09e47f10` 为 CID 0x1301、callback 0x080b2029。保留已修正的对手侧公式和证据。
2. B28AC 的 `Fiend Comedian 0x1566` 改为 `Fiend Comedian 0x151d`。原表 `0x09e47eb0` 为 CID 0x151d、callback 0x080b28ad。保留已修正的字段偏移和比较。

同步以上两条的长度和引用文本的冻结摘要。修正后逐条用原 ROM 表核对 card CID。

## 第二轮状态: NEEDS_FIX

第二轮绑定冻结清单 SHA256 `9a7df5f5c04213121ef9c0b10aab0f37fede044f43a1684a3a05b8cb67e7c33e`。独立记录 `f14-seg9-semantic-review-round2.json` SHA256 `fc50ea600a1e5e48485bbec0f22b28d882708fbba14936f5fefae4b828b4bd84`。

C1–C4、C6–C11、C13 通过。CFG 文件与首轮逐字节一致，仍覆盖 59 个函数、4317 条指令、231 个新池及 17 条保留机器 fallthrough 的 local BL。B1900 已按三只组件命名，两个池槽只改 owner 字段，三条表记录只改符号投影，表边界、字节和 bookend 不变。表扫描提前退出、B2358 证据路径、五个 Seg10 入口与 file 15 入口的交接，以及永久 include 路径均已订正。55 条通用描述均已替换，ASCII 和长度门槛通过。

C5 与 C12 仍有可由原 ROM 指令证明的差异。以下清单取代首轮清单。

1. **B2028 的玩家侧。** B2034 将玩家取反后计数。B204C 又将玩家取反，B2056 读取的是对手 LP。B205E 再取反，B2060 读取的仍是对手占用数。将 PLATE 的条件改为 `500 * opposingOccupied >= opposingLP || opposingOccupied > 1`，同步矩阵证据。
2. **B2D38 的拒绝方向。** B2D4A 比较 recorded player 与输入 side。B2D4C 的 BNE 在不相等时进入状态分派。相等时 B2D4E 返回 0。将 “player mismatch returns0” 改为 equality rejection。将 raw 返回证据定位到 B2D72–B2D76，布尔分支定位到 B2D7C–B2D8A。
3. **B2EEC 的原始半字返回。** B377A 的调用成功时，B3782 从 `[r7+8]` 读 u16 到 r0，B3784 跳到共享尾部 B397A。该路径绕过 B3978 的清零，也没有归一化。PLATE 和矩阵应明确普通布尔出口与此原始字段出口。B4B52/B4B54 按非零接受。17 条 local BL 的机器合同保持。
4. **阈值域。** B2AE0、B2E8E 调用同一 `get_card_extended_stat_field3@080eeed4`。B2AF8 的 1199 使用 `CARD_FIELD3_THRESHOLD_1199`，B2EA4 的 1499 复用 `constants/card_info.inc:1352` 的 `CARD_FIELD3_THRESHOLD_1499`。B35BC 的 1499 比较的是 B3592/B3594 的 `r6-r9`，采用有明确差值语义的常量。B380C 的 1799 比较 r9，该寄存器可来自 B2F68 的 field6、B2F80 的 field5 或 B2F86 的 0，采用目标评分阈值名。同步这些槽的 Equate、GAS 表达式、标签、EOL、常量计划和提案。B33F4/B3460/B353C 有直接 field5 来源。B1FA8 的主通道最大值由 080AEE72/080AEE76 取得评分记录的 `+0x14`，同样保留现有 field5 阈值。
5. **对齐更改过的证据地址。** B19D0 的特殊资格调用是 B1A4C，判定在 B1A52/B1A54，当前 “callee 1a5c–1a62” 指向循环尾和退出。B28AC 的 B28B6–B28C8 是算址和读取，无调用。两侧分别读取对方块 `+0x14`、本方块 `+0x10`，首次比较是 B28D6/B28D8 的无符号小于，第二次比较是 B28EA/B28EC 的 signed 大于 2。B1C80 的语义已正确，证据应指向 B1CB6–B1CD4 的 CID/field8 筛选、B1CD8/B1CE2/B1CFE 的 getter、B1CDC/B1CE6/B1CE8 的比较、B1CFC–B1D02 的保存以及 B1CEA–B1CF0 的接受路径。B1A74 的 type22 比较在 B1A82–B1A86，输入侧比较在 B1AE4–B1AF0。B21F8 的 eligibility call 为 B223C，B2242–B2248 判定正值成功。修正这些具体引用并重新冻结。

## 首轮记录

审查输入为冻结清单 SHA256 `e55d75f9e118c2d5e48edcc1f3cd1521d3c441f7a1f1d3c625f7f490beb4d15d`。独立机械复核记录为 `f14-seg9-review-independent-mechanical.json`，SHA256 `c822d45f49e746415057f2b895558d43447958ccf72db9d6f3391208c65d25e8`。

| # | 检查 | 结果 | 备注 |
|---|---|---|---|
| C1 | Rule 1 地址序 | ✅ | 活动路线图第 177 行与 `[0x080b153c,0x080b40b8)` 一致。四个同帧尾片段和六个后续段入口的处理范围分别明确。 |
| C2 | Rule 2 数据块分类 | ✅ | 10200B 原始块完整分为 8982B 指令、924B 池、154B 零填充及 140B §5.1。逐个重建 59 个可达 body 及 SHA256，与 158 个范围逐字节一致。 |
| C3 | Rule 3 引用扫描 | ✅ | 对全 ROM 的四种对齐起点重扫，记录段内 157 个值的 252 次命中。`[080b2758,080b27e4)` 每个 byte 的 raw 和 Thumb 值均零命中。原汇编的 Thumb 分支和新增 CFG 的直接目标均未进入该范围。B274C 结束前驱，随后是填充和前驱字面量池。 |
| C4 | EQ 数值 | ✅ | 231 个 R4 池由 240 条 PC 读取交叉解码，原 ROM 字节一致。既有 6 个池和新池均有槽合同。 |
| C5 | 常量复用 | ✅ | 新 CID 对应卡映射，shift19 对应运行时位移。0x707 的既有同值常量用于 tile 参数，与本段 field5 门槛语义不同。 |
| C6 | 槽名 | ✅ | 237 个池标签及 59 个新 Function 名满足格式，名称唯一并与现有编号模块定义无碰撞。 |
| C7 | 引用接通与保留 | ✅ | 82 新 DATA、2 既有 DATA 保留。B34D0 的 odd payload 用既有 Equate，辅助引用指向 even Function。表中 195 条已确认 callback 通过 even Function 接通，96 条后续地址记录使用 pending 表达式。 |
| C8 | PLATE 使用现名 | ✅ | 新注释使用实际函数名。B153C 是既有保留行。 |
| C9 | ASCII | ✅ | 237 个 EOL、63 行 PLATE 都是 ASCII，最长 490。 |
| C10 | Thumb carve | ✅ | 291 个原始 callback 均为非零 odd 值，582 字逐字核对。96 条 pending 记录共六个 even alias，各表达式保留 `+1`。 |
| C11 | 函数名与行为 | ❌ | B1900 实际绑定的是三只 Gate Guardian 组件，名称应体现绑定对象。 |
| C12 | 消费者和 ABI | ❌ | 55 条 PLATE 用通用句代替函数体门槛，B1E04 存在可证实的非布尔返回。B1C80 的零值语义有误，部分引用路径与外部扫描措辞需订正。 |
| C13 | 自动名覆盖 | ✅ | 六个既有池和 231 个新池全部在 TSV 中。旧 Function 的名称、body 与 PLATE 保留。 |

## 状态: NEEDS_FIX

### 1. C12 — 为 55 条通用 PLATE 写出可从函数体验证的门槛与返回值

去掉 `The body applies the card-specific slot, field, score, or state gates named by this Function`。逐条标明实际输入使用、关键分支或比较、以及从返回路径能证明的结果。用明确地址提供证据。公共 ABI 说明可以复用，功能说明必须能区分不同回调。B4B52/B4B54 只验证 callback 的 r0 非零。

- B1E04 从 B1E06–B1E0E 取 `1 - (slot[+2] & 1)`，B1E10 调 `count_zone_slots_with_card_field5`，接着 B1E14/B1E16 直接返回。该 callee 在 `asm/03_equip_chain_hand.s:2857` 附近累加 r6，在 0803741E 将计数移到 r0。PLATE 记录原始计数及调用方非零约定。
- B18E0 读取 `gP1LifePoints + 0x1ce8` 的全局 word，与槽 side bit 做异或并归一化非零。B20B4 对 `gP1LifePoints + 0x1cf4` 做无符号大于 1 判定。B2734 对 `gP1LifePoints + 0x1ce8` 做 side 相等判定。分别写出这些可区分的条件。
- B4098 在 B409C 检查 r1 非空，在 B40A4–B40AE 比较两个结构 `+2` 的 bit 0。只有 side 不同时返回 1。B3FA8 也有明确的 r1 空指针拒绝分支 B3FAC–B3FB0。

### 2. C12 — 订正 B1C80 的 field7 接受条件

B1CDC 拒绝与 r7 相同的值，B1CE6/B1CE8 拒绝 signed 大于 6 的值，B1CEA 检查的是已保存的 r7。首个保存值必须非零，后一个不同值没有独立非零门槛。先有非零 r7 时，后续零值可通过这些比较。把 PLATE 和 proposal 的 “distinct nonzero” 改成保存首个合格非零值，之后接受一个不同且 signed 不大于 6 的值。保留 occupied CID 和 field8 门槛。

### 3. C11 — B1900 的绑定名与实际组件一致

两表的 B1900 记录只有 `0x1119` Sanga of the Thunder、`0x111a` Kazejin、`0x111b` Suijin。使用 `check_gate_guardian_component_summon_response_eligible` 或同义的精确名称。B1904 读取输入半字 `+0x16`，B1918 读取对侧 LP。B191A–B191E 的 LP 比较先决定接受，B192E–B1934 再比较 `+0x14` 与 `+0x16`。同步更新函数、PLATE、registry 和三条 callback 行的投影。

### 4. C12 — 修订表扫描、引用路径和后续交接的措辞

- B4BA8/B4BE8 可在首个接受记录处提前退出。PLATE 的 “scans exactly” 改为 “scans up to” 或 “table contains”，仍明确物理记录数分别是 222 和 69。第二遍 primary 的 `cmp #0xdd; bls` 是 B4C5A/B4C5C。B49AE 读 CID，B4B48 读 callback，B4B4E 经 `invoke_r2` 调用的合同正确。
- proposal 的 B2358 证据路径改为 `asm/07_equip_effect_chain.s:20459`，该处将 0x4cc 标为 chain slot count。B2340–B2346 将 0201B75C 读作无符号循环计数。
- `f14-seg9-table-carve-plan.json` 的交接句当前把六个 pending 目标统一指向 Seg10。明确五个 080b46cc–080b4850 目标归 Seg10，080b76a4 归 file 15 对应段。现段继续只落地表源。永久源路径 `asm/normal_summon_response_tables.inc` 可直接随源码跟踪，由原 host 的固定位置包含。

执行修正后重新冻结。17 条 local BL 的机器 fallthrough 保持为 `source+4`，语义 CFG 跟随同帧尾片段到共享出栈路径。该双层合同、两个表的原始范围及 140B §5.1 范围均通过本轮复核。
