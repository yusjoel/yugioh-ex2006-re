# Refine Proposal: F13-Seg-8 [0x080a46a0..0x080a585c)

## 0. 结论

- 严格主范围为 `[0x080a46a0,0x080a585c)`, 长度 `0x11bc = 4540` bytes。`0x080a585c` 是 Seg-9 首地址，本提案不解释其后函数语义。
- 段内实测既有 Function=7，均为 USER_DEFINED Global Function；保留3个现名，订正4个误名，不创建、删除、拆分或调整 Function body。
- 残留自动槽=155，组成 `DAT=138, PTR=17`。逐槽动作是 `EQ=112, REF=26, RENAME=17`，每槽设置一条 ASCII EOL；完整逐地址合同在 `F13-Seg-8.slots.tsv`。
- Ghidra布局为1799条 InstructionDB，其中1738条助记符源码行、61条 `.hword` instruction projection；DataDB共253项，其中155个4-byte pool word、98个1-byte padding，源码投影中的padding为49个连续2-byte范围。字节闭合为 `1687*2 + 112*4 + 155*4 + 98 = 4540`，覆盖无空洞或重叠。段内没有 `ROM_INCBIN` 或 `.byte` 块，因此 carve=0、disasm=0、Rule 3 / §5.1=0。
- Function rename=4，PLATE full rewrite=14，其中段内7条、必要的段外 caller 投影7条。新 PLATE 均为 ASCII，最长477字符，14条全文均不超过500字符。
- 新增定义=16：`constants/card_info.inc` 14项、`constants/duel_field.inc` 1项、`asm/rom.s` Thumb alias 1项。其余94个 EQ 槽复用既有定义。
- 全 ROM 扫描确认4个段内 Function 入口另有12个 packed Thumb pointer word；这些 word 位于后续段，只纳入 C7 前态和 caller PLATE 投影，不改名、不加引用、不提前细化其槽语义。
- BLOCKED: none。所有 Function 订正、常量和全局引用均有消费者、结构化卡数据或精确 DB 前态闭合，置信度 high。

## 1. 前态与权威证据

| artifact | role | SHA256 |
|---|---|---|
| `output/refine-run-20261011-103530/root-f13-seg8-baseline.json` | 首版历史快照；保留原文件与原SHA，不作为修订后InstructionDB/DataDB统计真值 | `929beed341f1537349479df9afead923676b569fd8f492ab9bcbf381b3d48a92` |
| `output/refine-run-20261011-103530/root-f13-seg8-baseline-v2.json` | 7 Functions、1799 InstructionDB（1738助记符+61 `.hword`）、253 DataDB（155 words+98单字节padding）与4540B连续覆盖核验 | `45289f412678d5729c893e827bbc5ecd7733cb42fb5ad3b7c08ca57b5d033c05` |
| `doc/dev/refine/F13-Seg-8.slots.tsv` | 155槽完整落地合同 | `c62a1ff6516fbfe9e51e1c584ce734d7a3d702975f1303f821f1a0e9e6842db6` |
| `doc/dev/refine/F13-Seg-8.plates.tsv` | 14条 Function/PLATE 完整合同 | `a470fdbf187bb779d4fbbea8d0fd0b5a989ad276957beb0a3896ecd770083c76` |
| `output/refine-run-20261011-103530/f13-seg8-refscan.tsv` | 155槽 raw / THUMB|1 全 ROM 扫描 | `ed203ffc545d3d6703ce19276a1ab1941a4d5972c82b2611d1690d6198abedde` |
| `output/refine-run-20261011-103530/f13-seg8-function-refscan.tsv` | 7 Function 入口 raw / THUMB|1 全 ROM 扫描 | `b532685f2d8da5ffff6e4efb4780489fd0581518b07063afa571bcfdc177e093` |
| `output/refine-run-20261011-103530/f13-seg8-slots-prestate.json` | 155槽 Symbol/Data/ref/equate/EOL 和消费者前态 | `15190faffabdd11b602dc1e034739cd1cef7c98e4cad748138d9b815eccea90c` |
| `output/refine-run-20261011-103530/f13-seg8-functions-prestate.json` | 段内7 Functions 的 ID/body/PLATE/incoming 前态 | `22aa82c42803aba697270f5a051a210c0bcd590bdd328d945064621d25d1c00d` |
| `output/refine-run-20261011-103530/f13-seg8-external-callers-prestate.json` | 6个段外 caller Function 前态 | `ed7ec22c4e30e908bceb980b6093704b631bd23925179fb2d14417e0bd1200a6` |
| `output/refine-run-20261011-103530/f13-seg8-external-caller-6508-prestate.json` | `0x080a6508` caller Function 前态 | `d448d934a78b2b495a874c2664f7f84ed43c407dcf54b5994aad89237c9b94f7` |
| `output/refine-run-20261011-103530/f13-seg8-oddword-slots-prestate.json` | 后段12个 packed Thumb word 与4个目标入口前态 | `59eead0406167835a063a936b6b317e8507c76ce0b732e3679032daa67418cd3` |
| `output/refine-run-20261011-103530/root-f13-seg8-tsv-structure.json` | 155地址/旧名/原值/新名/ASCII 机械验收 | `a7a7411ad5720345c3c4a306592f3de5a5797185b276d122581c8982fb7975e9` |
| `output/refine-run-20261011-103530/root-f13-seg8-plate-structure.json` | 首版14 PLATE机械验收历史快照 | `5dc779c6a8d139895cbdd133257933bf850d7c8086d3974ccfa046e6a9d67202` |
| `output/refine-run-20261011-103530/root-f13-seg8-plate-structure-v2.json` | 修订后14 PLATE ASCII、长度、旧自动名机械验收 | `94bf8fe4fce45cae1e9d45338886da92c21444a7bdf21d7c67cd96b395bed892` |

四次 Ghidra 查询均使用 `-noanalysis -readOnly`。每次查询后15个 DB 文件的 SHA256 与物理备份清单完全一致；这些结果只证明提案前态，不代表 Mode B 已执行。

`slots.tsv` 是本提案不可分割的规范附件。每行冻结 `address, old_name, kind, original_value, action, target_symbol, target_contract, final_slot_label, reuse_status, slot_symbol_id/source/type, defined_data, existing_refs/equates/eol, packed_raw/thumb, consumers, file:line, confidence, eol_ascii`。Fixer 必须逐行执行，不能从汇总表推导或省略行。

155个source槽的当前Symbol均为dynamic DEFAULT；TSV中的Symbol ID只用于前态定位，物化唯一USER label时允许发生合法ID变化。3个REF target、`gP1LifePoints`及14个Function均为静态对象，其既有Symbol/Function ID必须守恒。

## 2. 段测绘

### 2.1 Function inventory

| entry | current name | final name | ID | body bytes | action |
|---|---|---|---:|---:|---|
| `0x080a46a0` | `eval_card_placement_flags_for_ai` | same | 2072 | 934 | preserve + PLATE |
| `0x080a4af4` | `eval_equip_target_slot_flags` | same | 2073 | 1406 | preserve + PLATE |
| `0x080a5188` | `check_equip_sub_entry_slot_pair_eligible` | same | 4398 | 404 | preserve + PLATE |
| `0x080a533c` | `check_equip_slot_pair_can_activate` | `check_moth_evolution_slot_requirement` | 2074 | 302 | rename + PLATE |
| `0x080a5498` | `check_equip_slot_pair_can_activate_full` | `check_special_summon_slot_requirement` | 540 | 490 | rename + PLATE |
| `0x080a5714` | `check_equip_slot_can_activate_with_context` | `check_special_summon_slot_requirement_with_pair_exclusions` | 2075 | 150 | rename + PLATE |
| `0x080a57b8` | `check_equip_slot_pair_can_activate_alt` | `check_vampire_genesis_or_neo_bubbleman_slot_requirement` | 2076 | 136 | rename + PLATE |

精确 body 冻结如下，语法原样取自只读 DB：

| entry | exact body |
|---|---|
| `080a46a0` | `[[080a46a0, 080a46ff] [080a470c, 080a472b] [080a4734, 080a47a9] [080a47c4, 080a47db] [080a47e0, 080a47e9] [080a47f0, 080a480d] [080a4818, 080a4829] [080a4830, 080a4843] [080a4848, 080a4859] [080a4860, 080a487f] [080a488c, 080a48b9] [080a48c8, 080a4915] [080a4920, 080a4955] [080a495c, 080a499b] [080a49a8, 080a4a33] [080a4a40, 080a4a91] [080a4aa0, 080a4ae7]]` |
| `080a4af4` | `[[080a4af4, 080a4b3f] [080a4b4c, 080a4b67] [080a4b70, 080a4b89] [080a4b98, 080a4ba5] [080a4bac, 080a4bd9] [080a4be4, 080a4c01] [080a4c10, 080a4c2f] [080a4c3c, 080a4c83] [080a4c94, 080a4ca5] [080a4cac, 080a4cc9] [080a4cd0, 080a4ce5] [080a4cec, 080a4cef] [080a4cf4, 080a4d1f] [080a4d24, 080a4d39] [080a4d40, 080a4d49] [080a4d50, 080a4d67] [080a4d6c, 080a4d7b] [080a4d80, 080a4d89] [080a4d90, 080a4dc1] [080a4dc8, 080a4dd9] [080a4de0, 080a4dfd] [080a4e04, 080a4e19] [080a4e20, 080a4e29] [080a4e30, 080a4e67] [080a4e6c, 080a4e83] [080a4e88, 080a4ea9] [080a4eb0, 080a4eb9] [080a4ec0, 080a4edf] [080a4ee4, 080a4f3d] [080a4f4c, 080a4f85] [080a4f98, 080a4fbb] [080a4fc4, 080a5009] [080a5014, 080a508d] [080a5094, 080a513f] [080a514c, 080a516b] [080a5178, 080a5187]]` |
| `080a5188` | `[[080a5188, 080a51bb] [080a51c0, 080a51e3] [080a51e8, 080a51ff] [080a5208, 080a5287] [080a5290, 080a52f9] [080a5300, 080a5339]]` |
| `080a533c` | `[[080a533c, 080a53c5] [080a53dc, 080a53e3] [080a53e8, 080a5483]]` |
| `080a5498` | `[[080a5498, 080a5529] [080a5548, 080a554f] [080a5554, 080a5569] [080a5570, 080a5579] [080a5580, 080a55a1] [080a55a8, 080a55b1] [080a55b8, 080a55cd] [080a55d8, 080a55e1] [080a55e8, 080a5601] [080a560c, 080a5625] [080a5630, 080a5633] [080a5638, 080a5653] [080a565c, 080a5665] [080a566c, 080a5693] [080a5698, 080a56a1] [080a56a8, 080a56b1] [080a56b8, 080a56c1] [080a56c8, 080a56d1] [080a56d8, 080a56f3] [080a56f8, 080a5711]]` |
| `080a5714` | `[[080a5714, 080a576f] [080a577c, 080a57b5]]` |
| `080a57b8` | `[[080a57b8, 080a581f] [080a5834, 080a5837] [080a583c, 080a584f] [080a5854, 080a585b]]` |

### 2.2 槽与布局 inventory

- 自动名槽：155，`DAT=138, PTR=17`。
- 所有155槽当前 primary Symbol source=`DEFAULT`, type=`Label`；逐槽 Symbol ID 在 TSV。
- 17个 PTR 槽当前 Data=`/pointer:4`，各有且只有一条 operand-0 DEFAULT DATA ref 指向 `gP1LifePoints`；138个 DAT 槽当前 Data=`/undefined4:4`，无既有 ref/equate/EOL。
- 155槽共有162个 PC-relative READ 消费者；每个 consumer 地址和 `asm/13_equip_placement.s:<line>` 均在 TSV。
- ROM 小端原值、源码字节注释及 ELF 解析值三方一致。Ghidra InstructionDB共1799条，由1738条助记符源码行与61条 `.hword` instruction projection组成；DataDB共253项，由155个4-byte words与98个1-byte padding组成，padding在源码投影为49个连续2-byte范围。InstructionDB/DataDB地址集合精确覆盖 `[0x080a46a0,0x080a585c)`，字节闭合为 `1687*2 + 112*4 + 155*4 + 98 = 4540`。

## 3. 数据块分类 (Rule 2/3)

段内没有 `ROM_INCBIN` 或 `.byte` 块，因此没有需要 carve、disasm 或登记 §5.1 的块。

| 块 | ref-scan (raw / THUMB|1) | 判定 | 理由 |
|---|---|---|---|
| none | n/a | none | 全段仅有既有 instruction、literal words 和 alignment padding |

155个槽地址本身的 packed 扫描有152个 `raw=0, thumb=0`。另3个命中均为字节偶合，不构成对槽的引用：

| slot | scan | 命中位置 | 证据 |
|---|---|---|---|
| `0x080a4700` | raw=3, thumb=0 | `0x0803d032,0x0803d472,0x0803d6ee` | 非对齐窗口跨越 `bx r0` 与后续字节；Ghidra refs-to 只有本函数 PC-relative READ |
| `0x080a4c88` | raw=0, thumb=1 | `0x08aca144` | `graphics/bin/card-images/tiles/tb1250.bin+0x0d84`，原4字节 `89 4c 0a 08`，上下文 `e0 34 29 65 89 4c 0a 08 4e 14 6b 4c 01 32 4d 14`；incbin证据 `data/card-image-tiles.s:1256`。目标槽是Data，不是Instruction/Function；Ghidra refs-to只有PC-relative READ |
| `0x080a55b4` | raw=0, thumb=1 | `0x08665b19` | `graphics/bin/card-images/tiles/tb0291.bin+0x0499`，原4字节 `b5 55 0a 08`，上下文 `a5 10 84 42 10 4a 05 9a 47 b5 55 0a 08 82 48 55`；incbin证据 `data/card-image-tiles.s:297`。目标槽是Data，不是Instruction/Function；Ghidra refs-to只有PC-relative READ |

## 4. Function rename 计划与消费者证据

### 4.1 Rename evidence

- `0x080a533c check_moth_evolution_slot_requirement`: `asm/13_equip_placement.s:17205-17388` 按 state card ID 分派 Larvae Moth、Great Moth、Perfectly Ultimate Great Moth 的2/4/6阶段阈值；目标槽必须是 Petit Moth，随后沿 Cocoon of Evolution equip chain 扫描并比较 `get_equip_card_set_code_for_slot`。`data/cards-ids-array.s:72,73,83,88,294` 和 `data/card-stats.s:795,808,977,1042,3434` 固定卡身份。置信度 high。
- `0x080a5498 check_special_summon_slot_requirement`: `asm/13_equip_placement.s:17391-17736` 对 state card ID 进行具体分派，检查 partner card、field spell、chain score/count、fusion range、active state 与 zone capacity。函数主题是 special-summon slot requirement，不是通用 equip activation。置信度 high。
- `0x080a5714 check_special_summon_slot_requirement_with_pair_exclusions`: `asm/13_equip_placement.s:17739-17822` 先检查 active card、zone capacity 与 field effect；state+8非零时拒绝 state+0x0c 中的 packed player/slot pair，然后以同一 `r0/r1/r2` 调用 `0x080a5498`。置信度 high。
- `0x080a57b8 check_vampire_genesis_or_neo_bubbleman_slot_requirement`: `asm/13_equip_placement.s:17826-17911` 仅有两条 card-ID 路径：Vampire Genesis 要求 Vampire Lord，Elemental Hero Neo Bubbleman 要求 Elemental Hero Bubbleman，最终调用 `check_slot_card_pair_allowed`。卡身份由 `data/cards-ids-array.s:1420,2303,2403,2576` 和 `data/card-stats.s:14263,23558,24481,26210` 固定。置信度 high。

四个函数均使用 `r0=u32 player_side, r1=u32 base_slot_idx, r2=u32 slot_offset`，返回 `r0=0x800` 或0，且只读。名称均符合 `^[a-z][a-z0-9_]+$` 和 verb-object-qualified 形式。

### 4.2 Incoming closure

| target | direct CALL from | packed Thumb word locations |
|---|---|---|
| `080a5188` preserved | none | `080a6434,080a6474` store `0x080a5189` |
| `080a533c` renamed | `080a3aba` | `080a655c,080a65d4` store `0x080a533d` |
| `080a5498` renamed | `080a3bca,080a57a8` | none |
| `080a5714` renamed | `080a3b22` | `080a668c,080a66d4,080a67c0,080a6800` store `0x080a5715` |
| `080a57b8` renamed | `080a3d46` | `080a6900,080a6948,080a6a74,080a6abc` store `0x080a57b9` |

`0x080a46a0` 有10条 Ghidra direct CALL，`0x080a4af4` 有6条；两者名称保留。完整 caller 地址在 Functions 前态 JSON。全 ROM function-refscan 对7个入口 raw 命中均为0，Thumb 命中仅为表中12个 word。

## 5. 符号化计划 (R1/R2/R3)

### 5.1 EQ_SLOTS

动作总数112。每行执行：在 operand0 附加 TSV 指定的 equate，按 `final_slot_label` 改名，设置 `eol_ascii`；Data 类型、地址、长度和4字节 ROM 值保持不变，不创建 DATA ref。94行复用既有 equate，18行使用16个新定义。

完整 `(slot, value, const_name, slot_label)` 列表是 `F13-Seg-8.slots.tsv` 中 `action=EQ` 的112行。该列表已经逐行核对 ROM，并包含全部旧名、Symbol ID、消费者和 EOL，不能用本节的分组统计替代。

高频复用包括 `ACTIVATION_STATE_B_OFF` 14行、`PLAYER_BLOCK_STRIDE` 11行；其余复用项为既有 card CID、状态偏移和范围定义。`0x080a4be0` 与 `0x080a4c08` 必须使用 `P2LP_BLOCK2_OFF_1CF4`：两处 consumer 的 base 是 `gP1LifePoints`，不是 field-state base。

新定义及落点：

```asm
@ constants/card_info.inc
.equ GREAT_MOTH_CID,                       0x00000fdf
.equ BLUE_EYES_ULTIMATE_DRAGON_CID,        0x00001122
.equ ZOA_CID,                              0x0000112d
.equ CAVE_DRAGON_CID,                      0x000014db
.equ LEVIA_DRAGON_DAEDALUS_CID,            0x00001707
.equ CID_GAP_1725,                         0x00001725
.equ CID_GAP_1729,                         0x00001729
.equ WARRIOR_OF_ZERA_CID,                  0x0000173b
.equ MAZERA_DEVILLE_CID,                   0x0000176c
.equ PYRAMID_OF_LIGHT_CID,                 0x000017bf
.equ FUSILIER_DRAGON_CID,                  0x00001838
.equ CID_GAP_1986,                         0x00001986
.equ PETIT_MOTH_CID_SHIFTED,               0x85e00000
.equ COCOON_OF_EVOLUTION_CID_SHIFTED,      0x7f700000

@ constants/duel_field.inc
.equ EQUIP_SLOT_CARD_ID_RANGE_MIN,         0x00001386

@ asm/rom.s
.equ check_card_is_archfiend_type_1, check_card_is_archfiend_type+1
```

CID 证据：`data/cards-ids-array.s:73,396,407,1349,1905,1957,2006,2089,2210` 与 `data/card-stats.s:808,4396,4552,13470,19138,19645,20243,21023,22427` 固定命名卡值。`CID_GAP_1725/1729/1986` 在 `data/cards-ids-array.s:1935,1939,2544` 均为 `.hword 0xffff`，故使用中性 gap 名。`0x1386..0x1388` 在 `data/cards-ids-array.s:1008-1010` 均无卡记录；MIN 与既有 `EQUIP_SLOT_CARD_ID_RANGE_MAX` 成对。两项 shifted 值分别等于 Petit Moth `0x10bc << 19` 和 Cocoon of Evolution `0x0fee << 19` 的32位结果，卡身份由 `data/cards-ids-array.s:294,88` 与 `data/card-stats.s:3434,1042` 双重固定。

`0x080a4958` 的原值是 `0x0804aea1`。现态 odd address 有 DEFAULT dynamic Label ID `4611686018561912481`，even address `0x0804aea0` 是 USER_DEFINED Function ID418。落地只在 `asm/rom.s` 增加 GAS `+1` alias 并给槽 operand0 设置 equate；不得在 odd address 创建 Label/Data/Function 或 DATA ref。

### 5.2 REF_SLOTS

动作总数26。每行按 TSV 改槽名、安装唯一 operand-0 DATA ref、设置 EOL；槽 Data 仍为 `/undefined4:4`，目标对象地址与类型不变。

| target | target prestate | slots |
|---|---|---|
| `gDuelCardCtxBase` | `0x0201e2a0`, ID18879, USER_DEFINED Label, `/undefined4:4` | `4704,472c,47b0,4880,48bc,499c,4a34,4a94,4ae8,4b44,4b68,4c30,5140,516c` |
| `gDuelFieldSlots` | `0x0201c510`, ID20369, USER_DEFINED Label, `/undefined4:4` | `5288,53d0,5488,5530,5774,5828` |
| `gEquipZoneRankState` | `0x0201e4d0`, ID33146, USER_DEFINED Label, `/undefined4:4` | `51bc,52fc,53c8,552c,5778,5820` |

表中槽地址均带 `0x080a` 前缀。目标必须保持一个 Global primary Symbol，不添加 alias，不改变目标 Data。postcheck 要求每个 REF 槽恰有一条到表中地址的 operand-0 DATA ref。

### 5.3 RENAME_SLOTS

动作总数17，地址为：

`080a4700,080a4884,080a48c0,080a4918,080a49a0,080a4a38,080a4a98,080a4aec,080a4b40,080a4c04,080a4c34,080a4f40,080a4f8c,080a4fbc,080a500c,080a5144,080a5170`。

这17个 PTR 槽只改为 TSV 的唯一 `ptr_g_p1_life_points_<addr>` 标签并设置 EOL。必须保留 `/pointer:4` Data 以及现有唯一 operand-0 DEFAULT DATA ref 到 `gP1LifePoints` (`0x0201c4e0`, ID15545, USER_DEFINED Label)。不得删除再重建引用。

### 5.4 C7 packed Thumb word 前态合同

后段12个 source word 当前均为 dynamic DEFAULT auto label、refs-from=0、equates=0，各有唯一 incoming DEFAULT READ，正式源码按原始 hex `.word` 导出。前6槽的Data为`/undefined4:4`，后6槽为`/dword:4`；下表逐槽冻结 source Symbol ID、Data类型和incoming READ。本段落地不修改这些 word，不创建 odd Symbol/ref/equate，也不把它们纳入155槽计数。证据为 `output/refine-run-20261011-103530/f13-seg8-oddword-slots-prestate.json`，置信度 high。

| source word | Data | source Symbol ID/name | unique incoming READ | current source line | value | even Function / odd prestate |
|---|---|---|---|---|---|---|
| `080a6434` | `/undefined4:4` | `4611686018562286644`, `DAT_080a6434`, dynamic DEFAULT | `080a641c`, operand1, DEFAULT | `asm/13_equip_placement.s:19574` | `080a5189` | Function ID4398; odd DEFAULT Label ID4611686018562281865, refs-to=2 |
| `080a6474` | `/undefined4:4` | `4611686018562286708`, `DAT_080a6474`, dynamic DEFAULT | `080a6438`, operand1, DEFAULT | `asm/13_equip_placement.s:19608` | `080a5189` | same target |
| `080a655c` | `/undefined4:4` | `4611686018562286940`, `DAT_080a655c`, dynamic DEFAULT | `080a654e`, operand1, DEFAULT | `asm/13_equip_placement.s:19731` | `080a533d` | Function ID2074; odd DEFAULT Label ID4611686018562282301, refs-to=2 |
| `080a65d4` | `/undefined4:4` | `4611686018562287060`, `DAT_080a65d4`, dynamic DEFAULT | `080a6592`, operand1, DEFAULT | `asm/13_equip_placement.s:19787` | `080a533d` | same target |
| `080a668c` | `/undefined4:4` | `4611686018562287244`, `DAT_080a668c`, dynamic DEFAULT | `080a667c`, operand1, DEFAULT | `asm/13_equip_placement.s:19883` | `080a5715` | Function ID2075; odd DEFAULT Label ID4611686018562283285, refs-to=2 |
| `080a66d4` | `/undefined4:4` | `4611686018562287316`, `DAT_080a66d4`, dynamic DEFAULT | `080a6698`, operand1, DEFAULT | `asm/13_equip_placement.s:19919` | `080a5715` | same target |
| `080a67c0` | `/dword:4` | `4611686018562287552`, `DWORD_080a67c0`, dynamic DEFAULT | `080a67b2`, operand1, DEFAULT | `asm/13_equip_placement.s:20043` | `080a5715` | same target |
| `080a6800` | `/dword:4` | `4611686018562287616`, `DWORD_080a6800`, dynamic DEFAULT | `080a67c4`, operand1, DEFAULT | `asm/13_equip_placement.s:20076` | `080a5715` | same target |
| `080a6900` | `/dword:4` | `4611686018562287872`, `DWORD_080a6900`, dynamic DEFAULT | `080a68f2`, operand1, DEFAULT | `asm/13_equip_placement.s:20210` | `080a57b9` | Function ID2076; odd address has no Symbol/ref |
| `080a6948` | `/dword:4` | `4611686018562287944`, `DWORD_080a6948`, dynamic DEFAULT | `080a690c`, operand1, DEFAULT | `asm/13_equip_placement.s:20246` | `080a57b9` | same target |
| `080a6a74` | `/dword:4` | `4611686018562288244`, `DWORD_080a6a74`, dynamic DEFAULT | `080a6a64`, operand1, DEFAULT | `asm/13_equip_placement.s:20399` | `080a57b9` | same target |
| `080a6abc` | `/dword:4` | `4611686018562288316`, `DWORD_080a6abc`, dynamic DEFAULT | `080a6a80`, operand1, DEFAULT | `asm/13_equip_placement.s:20435` | `080a57b9` | same target |

Exporter poststate仍应保留这12行原始 `.word 0x080a....` 表达。必要的名称涟漪只通过 caller Function 的完整 PLATE 重写收口。

## 6. PLATE 计划

`F13-Seg-8.plates.tsv` 冻结14个 Function 的 current/final name、Function ID/source、exact body、旧/新长度和完整新文本。Mode B 对每一行执行 full rewrite，不能做局部字符串替换。所有文本为 ASCII 且全文不超过500字符。

### 6.1 段内7条

`0x080a46a0 eval_card_placement_flags_for_ai`:

```text
Evaluates AI placement flags for player r0, slot selector r1, and mode r2. Loads card_id from gP1LifePoints+r1*4+0x10e0, rejects empty or field5-zero cards, applies spell-target and LP gates, then dispatches card-specific placement checks. Returns combined flags. On active-player block paths writes 0x10, 0x11, 0x17, or 0x0b to gP1LifePoints+ACTIVATION_STATE_B_OFF.
```

`0x080a4af4 eval_equip_target_slot_flags`:

```text
Evaluates target-slot flags for player r0 and slot selector r1. Loads card_id from gP1LifePoints+r1*4+0x10e0, applies common spell and LP gates, then dispatches concrete card IDs to material, target, field, zone-capacity, and pair checks. Returns flags in r0. Active-player block paths write phase codes through gP1LifePoints+ACTIVATION_STATE_B_OFF; 0x1cf4 reads use P2LP_BLOCK2_OFF_1CF4.
```

`0x080a5188 check_equip_sub_entry_slot_pair_eligible`:

```text
Checks player r0 and slot r1+r2 (<=4) against gEquipZoneRankState. Activation flag bit1 selects direct check_slot_card_can_be_equipped. Otherwise it validates stored card-ID whitelists and ranges, active pair variants, chain vacancy, zone capacity, field blocking, and exclusions. Returns 0x800 or 0 and writes no state. Full-ROM scan finds packed Thumb pointers at 0x080a6434 and 0x080a6474; Ghidra has no direct CALL reference.
```

`0x080a533c check_moth_evolution_slot_requirement`:

```text
Checks whether slot r1+r2 satisfies the moth evolution card stored in gEquipZoneRankState. Requires Petit Moth in the slot, scans Cocoon of Evolution chain nodes, and compares get_equip_card_set_code_for_slot against stage thresholds 2, 4, or 6 for Larvae Moth, Great Moth, or Perfectly Ultimate Great Moth. Returns 0x800 on success, else 0. Read-only.
```

`0x080a5498 check_special_summon_slot_requirement`:

```text
Checks whether slot r1+r2 satisfies the special-summon card_id stored in gEquipZoneRankState. After player, slot, active-card, zone-capacity, and field-effect gates, dispatches concrete card IDs to required partner, field spell, active-effect, chain score/count, fusion range, or card-state tests. Returns 0x800 on success, else 0. r0=player, r1=base slot, r2=offset; read-only.
```

`0x080a5714 check_special_summon_slot_requirement_with_pair_exclusions`:

```text
Applies pair exclusions before check_special_summon_slot_requirement. Validates slot r1+r2, active-card state, zone capacity, and field-effect gates; when gEquipZoneRankState+8 is nonzero, rejects packed player/slot pairs in the list at +0x0c. Otherwise forwards r0/r1/r2 to the core checker. Returns 0x800 or 0; read-only.
```

`0x080a57b8 check_vampire_genesis_or_neo_bubbleman_slot_requirement`:

```text
Checks two upgrade summons for slot r1+r2. Vampire Genesis requires Vampire Lord; Elemental Hero Neo Bubbleman requires Elemental Hero Bubbleman. Enforces current-player, slot-range, active-card, zone-capacity, and field-effect gates, then calls check_slot_card_pair_allowed. Returns 0x800 on success, else 0. r0=player, r1=base slot, r2=offset; read-only.
```

### 6.2 必要的段外 caller 投影7条

`0x080a3a80 scan_activatable_equip_slots_init`:

```text
Initializes gEquipZoneRankState from player r0 and card context r1: player bit0, card-ID bits, activation flag bit1 at +0x12, and mode byte +8=0. Scans players 0..1 and monster slots 0..4 with check_moth_evolution_slot_requirement(player,slot,0). Returns 1 on the first accepted slot, else 0. Writes only the state fields above.
```

`0x080a3ae8 scan_equip_activation_for_player`:

```text
Initializes gEquipZoneRankState from player r0 and card context r1: player bit0, card-ID bits, activation flag bit1 at +0x12, and mode byte +8=0. Scans players 0..1 and monster slots 0..4 with check_special_summon_slot_requirement_with_pair_exclusions(player,slot,0). Returns 1 on the first accepted slot, else 0. Writes only the state fields above.
```

`0x080a3b74 scan_equip_activation_with_mode`:

```text
Gets mode from get_equip_activation_mode_by_card_id(r1), initializes gEquipZoneRankState for player r0, and scans players 0..1 and slots 0..4 with check_special_summon_slot_requirement. Each hit decrements the remaining required count; a same-player hit sets the success flag only if check_slot_placement_blocked_by_field_effect passes. Returns 0 while the required count remains. Otherwise returns 1 if that flag is set or count_available_monster_slots(r0) is nonzero, else 0.
```

`0x080a3d0c scan_activatable_equip_slots_alt`:

```text
Initializes gEquipZoneRankState from player r0 and card context r1, then scans both players and slots 0..4 with check_vampire_genesis_or_neo_bubbleman_slot_requirement. Returns 1 at the first accepted slot, else 0. Writes the state header, activation flag, and mode byte.
```

`0x080a6508 dispatch_equip_confirm_action_by_phase`:

```text
Equip confirmation phase callback using gEquipZoneRankState. State 0 reads player control: value 1 selects a target through check_moth_evolution_slot_requirement; otherwise formats the card name and starts prompt 0x12. State 1 waits for confirmation, dispatches card op 0x28 with LP deltas, stores the result byte at +8 and target bytes at +0x0c, and returns 1; wait returns -1. Other states return 0. Updates phase bytes at +0x13/+0x14.
```

`0x080a6630 tick_equip_target_phase_with_lp_confirm_slot_context`:

```text
Equip target phase callback. If activation bit1 at gEquipZoneRankState+0x12 is clear, returns dispatch_equip_state_by_combined_phase_index(). With bit1 set, state 0 selects through check_special_summon_slot_requirement_with_pair_exclusions or starts prompt 0x12 and returns 0; state 1 returns 1 after confirmed op 0x28 and target storage, or -1 while waiting; later states return 0.
```

`0x080a6a20 tick_equip_target_phase_with_bitmap_query_confirm`:

```text
Equip target bitmap-query phase callback. State 0 selects a target with check_vampire_genesis_or_neo_bubbleman_slot_requirement when player control is 1, otherwise starts prompt 0x7e. State 1 waits for confirmation, calls query_equip_target_bitmap_with_zone_struct, and advances; state 2 returns done. Returns -1 for wait, 0 for advance, or 1 for done. Updates gEquipZoneRankState phase fields.
```

段外7条均只改同一 Function ID 的完整 PLATE；名称、body、calling convention、return/parameter storage 和源码指令保持不变。其当前 Function ID/body 全量在 `plates.tsv`。原 PLATE 中6条超过500字符；本合同将14条统一约束到271..477字符。

## 7. 消费者证据 (R6)

| subject | source evidence | conclusion | confidence |
|---|---|---|---|
| AI placement evaluator | `asm/13_equip_placement.s:15446-16033` | slot selector读取 `gP1LifePoints+0x10e0` card ID，执行 card-specific placement 分派并写 activation phase | high |
| target-slot evaluator | `asm/13_equip_placement.s:16036-16976` | 多卡 ID 分派；`asm/13_equip_placement.s:16148-16183` 的 `0x1cf4` 以 gP1LifePoints 为 base | high |
| sub-entry eligibility | `asm/13_equip_placement.s:16979-17203` | 读取 gEquipZoneRankState whitelist/range/pair list 并验证 slot chain/field/zone | high |
| moth evolution | `asm/13_equip_placement.s:17205-17388`; `data/cards-ids-array.s:73,88,294`; `data/card-stats.s:808,3434` | Petit Moth + Cocoon chain满足 Larvae/Great/Perfect moth 阶段阈值 | high |
| special summon core | `asm/13_equip_placement.s:17391-17736`; TSV中 5498 body 的 card CID consumers | 逐 card ID 检查 special-summon partner/field/chain/range/state | high |
| pair-exclusion wrapper | `asm/13_equip_placement.s:17739-17822` | state+0x0c packed pair list 是 core checker 的额外排除层 | high |
| Vampire/Neo Bubbleman | `asm/13_equip_placement.s:17826-17911` | 两条 upgrade 路径分别要求 Vampire Lord/Bubbleman | high |
| packed callbacks | `asm/13_equip_placement.s:19574,19608,19731,19787,19883,19919,20043,20076,20210,20246,20399,20435` | 12个 raw word 保存4个段内入口的 Thumb 地址 | high |

162个 literal consumer 的逐地址证据、目标动作和 EOL 在 slots.tsv，不以本表概括替代。

## 8. constants / 全局、carve、disasm 与 §5.1

- 新增 constants/alias 共16项，精确定义见5.1。对现有 `constants/*.inc` 的 exact-name 和 value-domain 扫描未找到可复用语义名；94个其余 EQ 行全部复用既有定义。
- 新增 global label: none。3个 REF target 与 `gP1LifePoints` 均为既有 USER_DEFINED globals。
- carve: none。
- disasm: none。
- §5.1: none。

## 9. Mode B 落地与投影合同

Reviewer PASS 后，Fixer 必须按活动方法论的完整 backup/dry/apply/persisted/export/build/rollback 流程执行，并额外满足下列本段精确条件：

1. 冻结本 proposal、slots.tsv、plates.tsv、review、7份关键只读 evidence 和 `root-f13-seg8-baseline-v2.json` 的 SHA256；首版 `root-f13-seg8-baseline.json` 只作为历史快照保留。新建写入脚本前必须从这些冻结输入生成 plan；脚本 dry/apply 计数一致。
2. Ghidra 一次 transaction 完成 `EQ=112, REF=26, RENAME=17, EOL=155, FUNC_RENAME=4, PLATE=14`。任何断言失败必须 rollback transaction。
3. 155个槽保持原地址、原4字节、原 Data 类型/长度；所有 final labels 唯一且匹配 `^[a-z][a-z0-9_]+$`。112 EQ 槽只有指定 equate 且无 DATA ref；26 REF 槽只有指定 DATA ref 且无 equate；17 RENAME 槽保留原 DATA ref。
4. 7个段内和7个段外 Function 保持前态 ID、entry、body、source、namespace、calling convention、return/parameter storage。只允许4个段内 name 和14条完整 PLATE 变化；Function create/delete/resize=0。
5. `doc/dev/naming-proposals.csv` 只更新地址 `080a533c,080a5498,080a5714,080a57b8` 的既有4行 `name` cell，不新增历史行。
6. `tools/ghidra-labeling/RenameKnownFunctions.py` 更新已有 `080a533c/5498/5714/57b8` 的 name+PLATE，以及已有 `080a3a80/3ae8/3b74/3d0c/46a0/4af4` 的 PLATE；为此前缺失的 `080a5188,080a6508,080a6630,080a6a20` 各增加一个唯一 tuple。不得产生重复地址、旧名或 final name。
7. source projection 限于 `asm/13_equip_placement.s`, `asm/rom.s`, `constants/card_info.inc`, `constants/duel_field.inc`, CSV、registry、四份 inventory、proposal/review/plan/evidence 与两份 progress 文档。模块13在段外仅允许7条已批准 caller PLATE 导出变化；12个 packed callback word 的 label、Data/ref/equate和原始 `.word 0x...` 表达保持前态。
8. 导出后必须验证4个新函数名在定义与 direct call 中收敛，14条 PLATE 精确相等，旧4函数名以及14条新 PLATE 内的 auto-name token 扫描为0。`FUN_080a5188`, `DAT_`, `DWORD_`, `PTR_DAT_` 不得出现在新 PLATE。
9. 新增 GAS alias 解析必须等于 `0x0804aea1`；所有16个新定义的槽表达式通过 ELF/nm 解析后必须等于 ROM word。所有 comments ASCII；14 PLATE 全文长度不超过500。
10. fresh persisted check 必须由独立 `-noanalysis -readOnly` 进程复核完整 poststate，并确认查询前后15个 DB 文件 hash 完全一致。之后才可导出、split、同步 inventory 和执行标准 export/build/byte-identical 验证。
11. 构建接受条件为 `output/2343.gba` 大小33554432、与 `roms/2343.gba` byte-for-byte 相等、SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`。任一 DB、source、export、inventory、build 或 ROM gate 失败时，按物理 DB 备份和完整 source baseline 恢复，清除本轮新增文件，并以 fresh read-only prestate 复核。
12. 本轮不得 stage 或 commit；用户另行明确授权后才可执行版本控制提交动作。

## 10. C1-C13 自检矩阵

| criterion | proposal evidence |
|---|---|
| C1 inventory | 7 Functions、155槽；DAT138/PTR17；1799 InstructionDB=1738助记符+61 `.hword`，253 DataDB=155 words+98单字节padding（49个2B源码范围）；`1687*2 + 112*4 + 155*4 + 98 = 4540` |
| C2 raw/THUMB scan | 155槽地址对与7个 Function 入口全 ROM 扫描已记录；3个槽地址偶合逐项排除 |
| C3 block classification | 无裸块，carve/disasm/§5.1 均为0 |
| C4 ROM values | 155槽源码、ROM、ELF 三方同值；root机械验收通过 |
| C5 constant reuse | 94 EQ行复用；18行对应16个新增定义，CID和domain证据列明 |
| C6 consumer semantics | 162个 literal consumers逐行在TSV；7个函数及12个 callbacks 给出 file:line |
| C7 target references | 26 REF、17 preserved refs、1个EQ-only odd alias和12个后段 packed word 均有精确合同 |
| C8 names/comments | 4误名订正、14条完整 ASCII PLATE、155条 ASCII EOL |
| C9 body integrity | 7段内与7段外 Function ID/body前态冻结；create/delete/resize=0 |
| C10 edge closure | direct CALL与12个 packed Thumb word均闭合；无未知 block target |
| C11 source projection | module13、rom.s、2 constants、CSV/registry/inventory/docs 白名单明确 |
| C12 build identity | standard export/build + size/fc/SHA1 gate |
| C13 rollback/layout evidence | 15-file物理 DB 备份、source baseline、transaction rollback、fresh persisted/prestate gate；布局真值引用 `root-f13-seg8-baseline-v2.json` SHA256 `45289f412678d5729c893e827bbc5ecd7733cb42fb5ad3b7c08ca57b5d033c05`，V1原文件与SHA保留为历史快照 |

## 求助

none。

## Executor Report: F13-Seg-8

- 槽: `EQ=112 REF=26 RENAME=17 FUNC_RENAME=4 PLATE=14 EOL=155`
- `carve=0; disasm=0; §5.1=0`
- 新增 constants/全局: `15 constants + 1 Thumb alias; global labels=none`
- Functions: `7 segment Functions; preserve-name=3; rename=4; create/delete=0`
- 段外必要投影: `7 caller PLATE full rewrites; 12 packed callback words preserve`
- 求助: none
- proposal: `doc/dev/refine/F13-Seg-8.proposal.md`
