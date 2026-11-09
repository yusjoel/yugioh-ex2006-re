# Refine Proposal: F15-Seg-3 [0x080b79f8..0x080b8a24)

## 段测绘

- 段长: 4140 B。
- 现有 Function 6 个:
  - `0x080b79f8 check_effect_node_eligible_in_any_slot_with_field6_score`
  - `0x080b7a48 check_opponent_active_zone_cards_present`
  - `0x080b7f64 check_equip_eligible_with_pair_slot_and_chain_gate`
  - `0x080b7f94 check_monster_zone_has_vacancy`
  - `0x080b7fb4 check_lp_below_lp_threshold`
  - `0x080b88c4 check_hand_equip_target_meets_bonus_6`
- 现有自动 word 槽 8 个: `080b7a34, 080b7fd8, 080b7fdc, 080b8000, 080b89e0, 080b89e4, 080b89e8, 080b8a20`。
- raw 块 2 个:
  - `[0x080b7a68,0x080b7f64)` 1276 B，源码宿主 `asm/15_equip_target_summon_zoom.s:5459`。
  - `[0x080b8004,0x080b88c0)` 2236 B，源码宿主 `asm/15_equip_target_summon_zoom.s:5568`。
- `0x080b88c0..0x080b88c4` 已是两个 InstructionDB 单元，字节 `01207047`，当前无 Function/符号；`0x080b89e8` 是其唯一 THUMB 指针消费者。
- 当前段逐字节前态、Function 全属性、word、引用、Equate、注释和目标状态见 `root-f15-seg3-initial-baseline.json`、`f15-seg3-supplement-prestate.json` 及 Root 独立的 `root-f15-seg3-independent-full-prestate.json`。

## 数据块分类 (Rule 2/3)

| 块 | ref-scan | 判定 | 理由 |
|---|---:|---|---|
| `[080b7a68,080b7f64)` 1276 B | 7 个真实 THUMB 表源，另 7 个数值命中 | disasm | 7 个真实源均来自已 carve 的卡响应表；7 个额外命中逐项落入卡图 palette/tile、FS 压缩流或高熵尾填充。CFG 完整覆盖该块且无 orphan。 |
| `[080b8004,080b88c0)` 2236 B | 57 个真实 THUMB 表源，另 10 个数值命中 | disasm | 57 个真实源均为已 carve 表的 callback word；10 个额外命中已逐项证明为资产字节偶合。CFG 完整覆盖该块且无 orphan。 |

证据:

- `root-f15-seg3-raw-reference-leads.json`: 全 ROM sliding raw/THUMB 扫描，64 个真实表源，17 个额外数值命中，外部 typed BL 和 file15 typed flow 均为 0。
- `root-f15-seg3-nonreference-assets.json`: 17 个额外命中分别归入 3 个 128 B palette、10 个 4800 B 6bpp tile、1 个 FS 压缩流和 3 个 FS 尾填充窗口；原始资产区间逐字节一致。
- `f15-seg3-r4-cfg-map.json` 与 `root-f15-seg3-thumb-cfg-leads.json`: 两套独立解码均得到 38 个根、1545 条指令/3254 B、50 个池 word/200 B、29 段零填充/58 B，合计 3512 B，无重叠、空洞、非法指令或多 owner。
- 两个 raw 块都有真实引用，均不得登记为 §5.1。

## 符号化计划 (R1/R2/R3)

完整、可执行、逐槽前后态合同在 `F15-Seg-3.slots.tsv`，共 58 行，精确覆盖 8 个现有 word 与 R4 产生的 50 个新池 word。每行冻结原字节、Data 类型、全部符号、primary、`refs_from`、`refs_to`、Equate、EOL、owner、目标前态、after refs/Equates 和最终 Data 类型。

### EQ_SLOTS (29)

- 复用 `PLAYER_BLOCK_STRIDE`: `080b7b14, 7b98, 7ccc, 7d54, 7dfc, 7eb4, 7f44, 7fdc, 8038, 81b4, 8264, 82b0, 8388, 8480, 84f8, 853c, 85a8, 8820, 8854, 889c, 89e4`。
- 复用卡 CID: `080b7d58 REVERSAL_OF_GRAVES_CID`, `080b7f40 MESMERIC_CONTROL_CID`, `080b8110 SWORDS_OF_REVEALING_LIGHT_CID`, `080b8114 MESSENGER_OF_PEACE_CID`, `080b8118 SWORDS_OF_CONCEALING_LIGHT_CID`, `080b82dc PETIT_MOTH_CID`。
- 复用 `LP_COST_1500`: `080b8000`。
- 新增 scoped 常量 `UMI_PACKED_CID_FIELD = (UMI_CARD_ID << 19)`: `080b8544 = 0x87a00000`。消费者 `080b851c..080b8564` 先提取 field-spell slot 的 low-13-bit CID，再接受 Umi 或空槽，值域与普通 CID 常量不同。

### REF_SLOTS (24 ADD + 2 PRESERVE)

- `gEquipLpScoreBase`: `080b7a34`。
- `gDuelFieldSlotState`: `080b7b0c, 080b7b90`。
- `gP1LifePoints`: ADD at `080b7b10, 7b94, 7d50, 7eb0, 8034, 8260, 82ac, 847c, 881c`; PRESERVE at `080b7fd8, 080b89e0`。
- `gDuelFieldSlots`: `080b7cd0, 7e00, 7f48, 81b8, 838c, 88a0`。
- `gEquipLpZoneEntryBase`: `080b7cd4`。
- `gDuelFieldSlots_p2_base`: `080b84fc, 8540, 85ac`。
- `gP1ZoneHandCount`: `080b8858, 080b8a20`。
- 所有静态 USER 目标符号 ID 保持；源槽新建 DATA ref 时使用 `USER_DEFINED/DATA/op0/primary=true`。现有 `080b7fd8` 与 `080b89e0` 的 DATA CORE6 原样保留。

### THUMB_REF_SLOTS (3)

- `080b8054 = check_card_stat_field8_is_7+1`。
- `080b84cc = check_card_field8_is_zero+1`。
- `080b89e8 = return_true_for_hand_equip_target_scan+1`。
- 三槽各绑定 operand-0 Equate `<fn>_1`，并从偶地址 source word 加一条 DATA ref 到偶地址 Function。奇地址不得创建 Label、Data 或 ref；`080b8055, 080b84cd, 080b88c1` 的现态保持。

### RENAME_SLOTS

- 无纯 RENAME 槽；58 个槽全部带 EQ/REF/THUMB 行动和 ASCII EOL。

### FUNC_RENAME (3)

| 地址 | 原名 | 新名 | 证据 |
|---|---|---|---|
| `080b7f94` | `check_monster_zone_has_vacancy` | `check_opponent_monster_zone_has_multiple_vacancies` | `080b7f96..080b7fae` 取 record[2] bit0 的另一侧，并要求 `count_available_monster_slots > 1`；全 ROM even=0、odd 仅 `09e49134`。 |
| `080b7fb4` | `check_lp_below_lp_threshold` | `check_opponent_lp_at_most_500_or_self_above_1500` | `080b7fba..080b7fd6` 穷尽两个返回条件；全 ROM even=0、odd 仅 `09e4913c`。 |
| `080b88c4` | `check_hand_equip_target_meets_bonus_6` | `check_hand_equip_target_bonus_above_four_eligible` | `080b89c4..080b89de` 证明 bonus 5..6 直接接受，bonus>6 另需 resolver>=0，<=4 拒绝；全 ROM even=0、odd 仅 `09e48334`。 |

三项 rename 均同步:

- Ghidra Function 名和完整 PLATE；Function ID/body/signature/参数/返回/flags 不变。
- `asm/15_equip_target_summon_zoom.s` 标签、`asm/equip_activation_response_tables.inc` 的 3 个 `fn+1` 表达式。
- `doc/dev/naming-proposals.csv` exact-address name-only 更新。
- `tools/ghidra-labeling/RenameKnownFunctions.py` 增加当前缺失的 exact tuple。
- `temp/ghidra-functions.csv`、`temp/ghidra-functions-renamed.txt` 更新名字；`auto.txt` 内容不变；summary 计数不变。

### PLATE (45)

- 6 个现有 Function 均按实际 body/ABI/返回路径全文重写。
- 38 个 raw callback 与 `080b88c0` typed leaf 均新增 ASCII PLATE。
- 完整旧前态、完整新 PLATE、字符数、ASCII 检查、Function metadata、incoming/body-ref 前后态和各类同步合同在 `F15-Seg-3.plates.tsv`。
- 45 条新 PLATE 最大 494 字符，全部 ASCII，均不超过 500 字符。

## 外部卡响应表 source 闭包

- `asm/equip_activation_response_tables.inc` 中 64 个 pending callback word 对应 38 个本段 raw 根；全部值为 `<entry>+1`，运行时字节不变。
- 每个 source word:
  - 保持字节、Data 类型、USER source label ID/name/type/namespace、EOL 及现有 CORE6；
  - operand-0 Equate 从 `pending_card_response_callback_<addr>_1` 改为 `<final_name>_1`；
  - native 表达式从 pending alias `+1` 改为 `<final_name>+1`；
  - 新增一条 source-even 到 Function-even 的 USER DATA ref；
  - pending Equate 零引用后移除对应的 38 条 pending base alias。
- 三个既有 rename source `09e48334, 09e49134, 09e4913c` 仅替换函数名/Equate 名和 derived target name；原 Function ID 与 DATA CORE6 不变。
- 完整全局 Equate 后态冻结在 `f15-seg3-global-equates-plan.json`: 2417 -> 2421 objects, 45 new, 41 retired after zero refs, 8 reused/extended, and 12206 -> 12238 exact `(address,operand)` bindings. The 203 future table sources and their bindings remain exact.
- Seg4 的 202 个 pending source 与 Seg5 的 1 个 pending source，连同其别名、字节、符号、refs 和 Equates，全部保持。逐 source 合同见 `f15-seg3-external-table-source-plan.json`。

## carve 计划 (R7)

- 无新 carve。卡响应表已在前段永久结构化；本段只做上述 67 个精确 source-expression/Equate/ref 投影。

## disasm 计划 (R4)

- `[080b7a68,080b7f64)` 和 `[080b8004,080b88c0)` 按 `f15-seg3-r4-plan.json` 的 1545 个 exact instruction starts 反汇编为 THUMB。 The same plan freezes 52 LDR PC READ references as `READ/DEFAULT/operand1/primary=true`; pool Equates remain operand 0. Canonical Function body ranges use ordered half-open pair lists.
- 仅在两个批准 raw range 内 disassemble；现态为 implicit 1-byte DataDB，不执行 clear/retype 已定义 Data。
- 50 个 pool word 物化为 `/undefined4` USER source label，并按 `F15-Seg-3.slots.tsv` 加 EQ/REF/EOL。
- 29 段 2 B 零填充保持 implicit DataDB 和原字节，不物化为代码或 word。
- 创建 38 个 raw Function；canonical body AddressSet、长度和 SHA256 逐函数冻结在 `f15-seg3-function-plan.json`。
- `080b84d8` 和 `080b8720` 同时是 callback root 和本段 BL target，分别保留 `080b8514 -> 080b84d8`、`080b88b0 -> 080b8720` 的 `UNCONDITIONAL_CALL`。
- `080b88c0..080b88c4` 不重反汇编；保留两个现有 InstructionDB 单元，仅创建 `return_true_for_hand_equip_target_scan` Function/符号/PLATE。
- 后态严格计数: 本段 45 Function，module15 157 Function，1825 InstructionDB/3840 B，58 words/232 B，68 B padding；两个 raw 块清零。

## 新增 constants / 全局

- 新增 `constants/card_info.inc` scoped Equate:
  - `UMI_PACKED_CID_FIELD = (UMI_CARD_ID << 19)`，值 `0x87a00000`，唯一新定义。
- 其余 28 个 EQ binding 全部复用现有常量；所有 RAM/ROM 目标复用现有 USER 符号。

## §5.1 登记

- 无。两个 raw 块均有真实 THUMB 表引用并完整反汇编；17 个额外数值命中已单独证明为资产偶合，不产生残留 raw block。

## 消费者证据 (R6)

- `asm/equip_activation_response_tables.inc:308,445,1049,1778`: 代表性 callback source；完整 64+3 source 清单和前态在 `f15-seg3-external-table-source-plan.json`，置信度 high。
- `asm/15_equip_target_summon_zoom.s:5459`: raw1 宿主；7 个真实 callback roots 及其 20 个新池 word，置信度 high。
- `asm/15_equip_target_summon_zoom.s:5568`: raw2 宿主；57 个真实 callback sources、31 个 callback roots和 30 个新池 word，置信度 high。
- `asm/15_equip_target_summon_zoom.s:5495`: `080b7f94` 实际检查对侧空位数大于 1，置信度 high。
- `asm/15_equip_target_summon_zoom.s:5524`: `080b7fb4` 的 500/1500 双阈值，置信度 high。
- `asm/15_equip_target_summon_zoom.s:5581`: `080b88c4` 的 bonus 5..6 与 >6 分支，置信度 high。
- 卡身份使用 `f15-seg3-semantic-skeleton.json` 的表 row CID、`constants/card_info.inc` 与响应表 source row 交叉；函数名以 body 行为为主，不用资产字符串单独定名。

## 不变量与落地门禁

- 原 ROM 两 raw SHA256、现有 8 word、全部 4140 B 段字节保持。
- 6 个现有 Function 的 ID/source/type/namespace/body SHA/ranges/signature/flags/参数/返回保持；仅批准 3 rename 和 6 PLATE 写入。
- 39 个新 Function 使用新分配 USER Function ID；同址禁止附加 alias。
- 58 槽旧 Data/type/symbol/ref/equate/EOL 前态严格对照 supplemental prestate；静态 USER 目标 ID 保持。
- 64 pending source、3 rename source 和 203 个未来 pending source 严格按白名单区分；不得改 future source。
- 11 个既有 native GAS projection 原样保持。
- Ghidra 新 PLATE/EOL 全 ASCII，PLATE 全文 <=500。
- byte-identical SHA1 不一致即中止并回滚 `.rep`；本 executor 不执行落地、build 或 commit。

## 求助

- none。

## Executor Report: F15-Seg-3

- 槽: EQ=29 REF_ADD=24 REF_PRESERVE=2 THUMB_REF=3 FUNC_RENAME=3 PLATE=45。
- carve=0，disasm=2 ranges / 1545 instructions，§5.1=0。
- Function create=39，其中 raw=38、既有 typed leaf=1。
- 新增 constants/全局: `UMI_PACKED_CID_FIELD` 1 个；其余复用。
- 求助: none。
- proposal: `doc/dev/refine/F15-Seg-3.proposal.md`。

## Mode A reviewer corrections

- Applied all five formal review items: complete Equate map, operand-1 PC READs, canonical arrays/ranges, corrected callback predicates/branches/arguments, and B885C/B88C4 polarity/name projection.
- `B8514 -> B84D8`, `B88B0 -> B8720`, the typed B88C0 leaf, all ROM bytes, current Function ABI, and 203 future table sources remain frozen.

## Mode A round2 reviewer corrections

- Seven PLATE texts now retain every reviewed prerequisite, short-circuit, per-candidate gate, packed-input distinction, and shared-PRNG side effect.
- All 45 semantic and Function projections are regenerated from the formal TSV. Their plate, ordered half-open ranges, incoming arrays, body-reference arrays, body size, and body SHA are exact.
- The 52 raw-block PC READ rows are operand 1 in the R4 plan, formal TSV, and Function plan; empty arrays are canonical `[]`.
