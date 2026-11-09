# Refine Proposal: F14-Seg-2  [0x080a8c30..0x080aa120)

## 范围与冻结输入

- 正式段范围: `asm/14_equip_ai_scoring.s [0x080a8c30,0x080aa120)`, 5360 bytes.
- 必要范围外闭包: `asm/rom.s` 的 6-byte CID table carve; `0x080aa77c`, `0x080aaf64`, `0x080ab200` 的 PLATE name projection; naming registry, `doc/dev/naming-proposals.csv`, 四份 Function inventory.
- 当前 Function/word/unit 前态: `root-f14-seg2-initial-baseline.json` 与 `root-f14-seg2-supplement-prestate.json`. 后者含 31 Function rows, 54 words, 331 address states, 14 target records, 5360 byte units.
- 当前模块前态只采用完成 Seg-1 后的 `root-f14-seg1-independent-post.json`. 不采用 Seg-1 前的 module map 作为写入前态.
- 源码与 DB 备份: `root-source-baseline-f14seg2.json`, `root-f14-seg2-db-backup.json`. 两次只读 query 后 15 个物理 DB 文件 hash 全部不变.
- 完整槽合同: `F14-Seg-2.slots.tsv`, 156 rows. Function/PLATE 合同: `F14-Seg-2.plates.tsv`, 7 rows.
- R4 地址级合同: `f14-seg2-r4-cfg-map.json`, SHA256 `8d30c1f7bc2ac86184317407a1da7b2591ea1ee9c09056d37a9b0e3f0d6fe98b`.

## 段测绘

### Function 入口

| entry | current | final | action |
|---|---|---|---|
| `0x080a8c30` | `dispatch_equip_phase_by_card_id_range` | same | preserve |
| `0x080a9734` | `dispatch_equip_entry_slot_phase_b` | `dispatch_equip_mode1_phase_by_combined_index` | rename + R4 body extend |
| `0x080aa10c` | `exit_equip_phase_oob_epilogue_wide` | same | preserve body; add incoming refs |
| `0x080a9134` | no Function | `process_equip_mode1_phase_3_to_7` | R4 create Function |

`0x080a9134` 的前态 absence 已由 supplement query 明确返回 NULL. `0x080a9132` 是 2-byte zero padding, 不是 Function entry.

### word 与 raw 块

- 当前 word 共 54: 39 个自动 word 槽, 15 个已有普通 table words. 全部进入 slots TSV.
- R4 新 literal pool 共 102 words. 加上当前 54 words, final word 总数 156.
- 三个 raw 块:
  - `[0x080a9132,0x080a9264)`, 306 bytes, source `asm/14_equip_ai_scoring.s:3282`.
  - `[0x080a927c,0x080a9734)`, 1208 bytes, source `asm/14_equip_ai_scoring.s:3291`.
  - `[0x080a9798,0x080aa10c)`, 2420 bytes, source `asm/14_equip_ai_scoring.s:3347`.
- 当前布局: 551 InstructionDB / 1178 code bytes; 54 words / 216 bytes; 3934 raw bytes; 32 zero-padding bytes. 总计 5360 bytes, 无空洞或重叠.

## 数据块分类, Rule 2/3

| 块 | full-ROM raw / THUMB scan | 控制流闭包 | 判定 |
|---|---|---|---|
| `9132..9264`, 306B | 153 even candidates; only asset raw coincidence `920e`, with no true raw/THUMB pointer hit in this block | live entry is direct BL `9ba6 -> 9134`; this block is 128 InstructionDB/256 code bytes + 12 pool words/48B + one 2-byte pad | disasm |
| `927c..9734`, 1208B | five table sources at `9268..9278` point to the five raw2 targets `927c`, `932c`, `9558`, `9668`, `96f8` | belongs to new `9134` Function; 528 InstructionDB/1070 code bytes + 32 pool words/128B + five 2-byte pads; raw1+raw2 cluster totals are 656 InstructionDB/1326 code bytes + 44 pool words/176B + six 2-byte pads/12B | disasm |
| `9798..aa10c`, 2420B | 10 source entries, 6 unique targets `9798/9800/9b40/9ba4/9bac/9c2c`; `9ba4` is reused by 5 sources; asset THUMB hit `9389` is in raw2 and asset raw hit `9ed2` is in this block | cases 0..9 belong to `9734`; `9134` is a direct-BL target, not a table target; 1043 InstructionDB/2158 code bytes + 58 pool words/232B + fifteen 2-byte pads/30B | disasm |

完整扫描见 `f14-seg2-full-rom-refscan.json`. 1967 个 even candidates 中 14 个地址有非零命中. 真实 code sources 为 15 个 table words:

- phase table: `927c@9268`, `932c@926c`, `9558@9270`, `9668@9274`, `96f8@9278`.
- combined-index table: `9798@9770`, `9800@9774`, `9b40@9778`, `9ba4@977c/9780/9784/9788/978c`, `9bac@9790`, `9c2c@9794`.
- The 15 table sources resolve to 11 unique targets. `9134` is reached by the separate direct BL at `9ba6` and is not counted among those table targets.

三项资产偶合保留原始命中:

- raw `0x080a920e` at ROM `0x09ee7069`, unaligned `+1`, `asm/rom.s:2093` FS-tail host, relative `0x125c5`, context `94bfcc6aef2d3f190e920a08915cf5b09c715bcf`.
- THUMB `0x080a9389` at ROM `0x086cbd86`, aligned `+2`, `data/card-image-tiles.s` card tile `tb0378.bin+0x7c6`, context `1a8191810608020089930a0882c57bf343a2fb55`.
- raw `0x080a9ed2` at ROM `0x09f3ce56`, aligned `+2`, `asm/rom.s:2093` FS-tail host, relative `0x683b2`, context `061cc3c7c4dfc521d29e0a083c4998fbd17d62ad`.

三项均处于资产 bytes, 不形成 code/data consumer. 三块都有真实 table sources 与完整 live CFG, 所以本段没有 Section 5.1 raw block.

## disasm 计划, R4

### 精确布局

`f14-seg2-r4-cfg-map.json` 的 `instructions[]` 是 1699 个新增 InstructionDB 地址的权威集合. 每项冻结 `address`, `length`, ROM little-endian `raw_bytes`, opcode halfwords, direct-flow, call, PC-read 和 fallthrough. 不能用连续区间首地址替代该集合.

- 新 InstructionDB: 1699, 3484 code bytes.
- 新 pools: 102 words, 408 bytes.
- 新 zero pads: 21 halfwords, 42 bytes.
- 新 direct flows: 248, 其中 calls 43.
- 新 PC literal reads: 126.
- 新 machine/API fallthrough edges: 1616.
- final segment: 2250 InstructionDB / 4662 code bytes; 156 words / 624 bytes; 74 padding bytes. 合计 5360 bytes.

新 `process_equip_mode1_phase_3_to_7` 的十个 maximal code ranges:

- `[9134,9234)`, `[927c,92a4)`, `[92ac,9438)`, `[9464,94be)`, `[94c4,9542)`.
- `[9558,9600)`, `[9614,965e)`, `[9668,96e2)`, `[96f8,971c)`, `[9720,9732)`.

`dispatch_equip_mode1_phase_by_combined_index` 新增的 26 个 maximal code ranges:

- `[9798,97e4)`, `[97ec,998c)`, `[99b0,99c6)`, `[99d0,99da)`, `[99e0,9a52)`, `[9a58,9a9e)`, `[9aa8,9b9a)`.
- `[9ba4,9c1e)`, `[9c2c,9c90)`, `[9c98,9e36)`, `[9e78,9e84)`, `[9e88,9ea0)`, `[9ea4,9eb0)`, `[9eb4,9ed8)`, `[9edc,9eee)`.
- `[9ef4,9f0a)`, `[9f10,9f1a)`, `[9f20,9f44)`, `[9f48,9f52)`, `[9f58,9f6c)`, `[9f70,9f7a)`, `[9f80,9fa2)`, `[9fa8,9fd8)`, `[9fdc,aa06a)`, `[aa078,aa086)`, `[aa08c,aa108)`.

21 个 zero pads:

- `9132`, `94be`, `9542`, `965e`, `96e2`, `9732`.
- `99c6`, `99da`, `9a52`, `9a9e`, `9b9a`, `9c1e`, `9e36`, `9eee`, `9f0a`, `9f1a`, `9f52`, `9f7a`, `9fa2`, `aa06a`, `aa086`.

102 个 pool 地址全部在 slots TSV 标为 `R4_NEW_POOL`; `f14-seg2-r4-cfg-map.json` 分别冻结第一组 44 地址与第二组 58 地址. fixer 必须逐地址建立 4-byte Data, 不能把 pool 间 code 或 zero pads 合并成 Data.

### disasm seeds 与覆盖门禁

- 新 Function seeds: `9134`, `927c`, `932c`, `9558`, `9668`, `96f8`.
- existing Function case seeds: `9798`, `9800`, `9b40`, `9ba4`, `9bac`, `9c2c`.
- 执行 seeds 后, 将实际 InstructionDB address set 与 map 中 1699-address expected set比较. 对每个 missing address 单点补 disasm; 对每个 extra address中止落地并回滚 `.rep`.
- 全部 248 direct-flow targets, 126 PC-read targets 与 1616 machine/API fallthrough edges必须与 map 相同. 关键跨块闭包为 `0x080a9ba6 -> 0x080a9134` BL.
- shared tail 的 Function-entry incoming 精确为 `975a->aa10c` CALL 与 `9bd6->aa10c` JUMP, target primary均为 USER Function ID `16954`. Function interior `aa10e` 的 address-level incoming精确为 `9b98/9baa/9c1c/9c36/aa106 -> aa10e` JUMP. disasm在 `aa10e` 派生单一 DEFAULT code Label, 预期名 `LAB_080aa10e`; 动态ID/name从后态 `getPrimarySymbol(aa10e)`读取, type/source必须为 `Label/DEFAULT`, 不能借用 Function ID `16954`. body external incoming总数为7.
- `97a2`, `97e0`, `97fc` 三条 BL 的 default machine/Ghidra API fallthrough分别是 `97a6`, `97e4`, `9800`. 它们的调用目标 `aa0d2` 经 `aa106 -> aa10e` 丢弃 LR, 所以 map 另以 `semantic_tail_call=true` 和 `semantic_fallthrough=null` 表示逻辑终止. 不设置 FlowOverride. disasm 使用仅含 expected InstructionDB bytes 的 restricted AddressSet, 因此 `97e4` 保持 literal pool而不被默认 CALL fallthrough解码; `9800` 由独立 switch seed建立.

### source 格式预测

当前 551 InstructionDB 导出为 534 mnemonic + 17 `.hword`; 17 条均属于 `0x46xx` high-register move family. 新地址集中有 89 条同族 opcode. 按当前 exporter 规则, 新 1699 条预测为 1610 mnemonic + 89 `.hword`, final 2250 条预测为 2144 mnemonic + 106 `.hword`. 完整计数在 `f14-seg2-source-format-prediction.json`. 后态同时核对 Instruction API 地址集合、source mnemonic+`.hword` 总和与 ROM bytes.

### Function body 合同

- 新 `process_equip_mode1_phase_3_to_7@9134`: 10 maximal ranges, 1326 bytes, SHA256 `e28dcdffb8c8e742cf15f46ead97df990309ba0c3eb09129e1f505d0ff0022dd`. 新 Function ID 由 Ghidra 合法分配; namespace Global, source USER_DEFINED, default signature/flags.
- `dispatch_equip_mode1_phase_by_combined_index@9734`: 保留既有 `[9734,9768)`, 合并上述 26 ranges, final 27 ranges, 2210 bytes, SHA256 `580e1445d9ac941a9b87ae962fd1f22f3ab3d5c17f123055163488025d3abd0d`. Function ID `16953` 与 namespace/signature/flags 保持.
- `exit_equip_phase_oob_epilogue_wide@aa10c`: body `[aa10c,aa11e)`, 18 bytes, SHA256 `b5be17f53da36436b1c7b1cd31e839dd9c2bd3667566b97f07f3185fe05b6798` 保持. Function ID `16954` 保持; Function entry incoming为2, Function body external incoming为7, interior `aa10e` 的5条address-level refs按上列独立合同核对.
- `dispatch_equip_phase_by_card_id_range@8c30`: body 1108 bytes, SHA256 `53c00b296020047f20c3f0a7c347e2c6e4fd4b8fa4050d7174167ca280218ca5` 保持.
- 模块 Function count `138 -> 139`; 全工程 Function count `5213 -> 5214`.

## 符号化计划, R1/R2/R3

### 完整 slots 合同

`F14-Seg-2.slots.tsv` 精确覆盖 54 个当前 words 与 102 个 R4 新 pools, 地址唯一且 ROM word 全相等:

| action | count | contract |
|---|---:|---|
| `EQ_ADD` | 31 | 当前 Data 保持; 新增或复用 equate; source refs/PC READ refs 分列冻结 |
| `EQ_MATERIALIZE` | 73 | R4 undefined bytes 物化 4-byte Data + equate + USER slot label |
| `REF_ADD` | 36 | source Data/label + USER DATA ref; static USER target ID 保持 |
| `REF_PRESERVE` | 1 | `9264 -> 9268` 既有 DATA ref CORE6 原样保持 |
| `TABLE_ENTRY_MATERIALIZE` | 15 | 既有 table Data/ref对象保持; target DEFAULT label物化为单一 USER primary |

TSV 的 `refs_from_json` 是 source reference 前态, `refs_to_json` 是 PC READ consumers, `equates_json` 与 EOL 分开冻结. RAM targets 的 `bytes` 保持 null; 不读取未初始化 RAM bytes.

### EQ_SLOTS

- 共 104: `EQ_ADD=31`, `EQ_MATERIALIZE=73`.
- 每行 `original_value`, `const_or_target`, `final_slot_label`, `gas_expression`, `new_eol_ascii`, consumer address 与 confidence 见 slots TSV.
- 值域复用优先; 87 个 distinct non-table values 已由 `f14-seg2-slot-value-plan.json` 完整映射, 无遗漏.

### REF_SLOTS

- 共 37: `REF_ADD=36`, `REF_PRESERVE=1`.
- static USER targets: `gEquipZoneRankState`, `gDuelFieldSlots`, `gDuelPhaseFlags`, `gP1LifePoints`, `gDuelCardCtxBase`, `gEquipZoneCountTable`. 其 Symbol ID/source/type 保持.
- ROM target `equip_mode1_counter_trap_cids@09e478c8` 前态无 Symbol/Data/ref; 本 proposal 允许新增 target ID, 但只建一个 USER primary label 与一个 6-byte structured Data range.
- table-base targets `9268` 与 `9770` 物化为单一 USER primary; `9264` 既有 DATA ref保持, `976c` 新增 DATA ref.

### RENAME_SLOTS

无纯 RENAME slot. 所有 156 rows 属于 EQ, REF 或 table entry action.

### switch table labels

- `9268..927c`: base `equip_mode1_phase_3_to_7_jump_table`; targets `equip_mode1_phase_3` through `equip_mode1_phase_7`.
- `9770..9798`: base `equip_mode1_combined_index_jump_table`; targets case 0, 1, 2, shared `equip_mode1_combined_case_3_to_7` for five rows, case 8, case 9.
- 15 source Data units与15 DATA reference对象保持. 动态 DEFAULT target primary 在物化为 USER primary 后允许 derived target ID/name变化; 不新增同址 alias. 其余 static USER Symbol IDs 不变.

## carve 计划, R7

`0x080a9458` pool word 唯一 raw reference 为 `0x09e478c8`; THUMB `0x09e478c9` count=0. consumer `0x080a9340` 以 halfword index读取三项 CID.

- carve ROM range `[0x09e478c8,0x09e478ce)`, file offsets `[0x01e478c8,0x01e478ce)`, raw `0013fd123219`.
- host `asm/rom.s:1558`: 当前 `.incbin "roms/2343.gba", 0x1e478c8, 0x2444`.
- replacement:
  - `equip_mode1_counter_trap_cids:`
  - `.hword HORN_OF_HEAVEN_CID`
  - `.hword SOLEMN_JUDGMENT_CID`
  - `.hword TRIAGE_CID`
  - remainder `.incbin "roms/2343.gba", 0x1e478ce, 0x243e`.
- left bookends: `09e478c0=0x0000129b`, `09e478c4=0x000012b8`; preceding structured table ends exactly at `09e478c8`.
- right bookends: bytes at `09e478ce` are `0000`; `09e478d0=0x000016a7`; original incbin end remains `0x09e49d0c`.
- code side: `9458` label `equip_mode1_counter_trap_cids_ptr_080a9458`, GAS `.word equip_mode1_counter_trap_cids`, one USER_DEFINED DATA ref.

## FUNC_RENAME 与 PLATE

### FUNC_RENAME

| addr | old | final | evidence |
|---|---|---|---|
| `0x080a9734` | `dispatch_equip_entry_slot_phase_b` | `dispatch_equip_mode1_phase_by_combined_index` | sole caller `asm/14_equip_ai_scoring.s:4013`; computes `(state[0x14]&1)<<7 | state[0x13]>>1`; table `9770` covers indices 0..9; high cases share wide epilogue |

新 Function `process_equip_mode1_phase_3_to_7@9134` 不是 rename. 它只有 `9ba6` 一条 direct BL, 输入 `r0=0x1f`, 对 `combined_index-3` 使用 `9268` 五项 table, 并在 phase cases 中处理三项 counter-trap CID、slot scanning、sprite/activation submission 与 backtracking. `94ba` 设置 `r0=0`, `94bc` 跳到 `9722` 后返回0; `9228/92cc` 跳到 `9720`, 由 `9720` 设置 `r0=1` 后返回1.

### PLATE contract

`F14-Seg-2.plates.tsv` 冻结 Function ID/source/type/namespace/body/signature/flags/current incoming/old plate hash/final body/final incoming. 7 rows 中:

- `8c30`: exact PRESERVE, 不写 PLATE.
- `9134`: new PLATE.
- `9734`: rename + body extend + full PLATE rewrite.
- `aa10c`: body/name保持, full PLATE rewrite; Function entry登记2条final incoming, `aa10e`另按5条address-level interior incoming合同核对, body external incoming总数7.
- `aa77c`, `aaf64`, `ab200`: 仅必要 old-name projection 的 full PLATE rewrite; Function name, ID, body, signature与incoming保持.

写入的 6 条 new PLATE 全部 ASCII, 长度分别 471, 436, 406, 429, 405, 454, 最大471, 均不超过 500 chars. `8c30` 保留 446-char ASCII PLATE.

### rename projection

- source label与 `asm/14_equip_ai_scoring.s:4013` BL operand改为新名.
- old-name PLATE consumers位于当前 `asm/14_equip_ai_scoring.s:3349-3355`, `3435`, `3826-3827`, `3921`; 由 `aa10c`, `aa77c`, `aaf64`, `ab200` 四条完整 PLATE 合同覆盖.
- `doc/dev/naming-proposals.csv:3326` 仅替换 address `0x080a9734` 的 name column; 新 `0x080a9134` 增加一行.
- naming registry: `8c30` 现有 tuple保持; `9134`, `9734`, `aa10c`, `aa77c`, `aaf64`, `ab200` 按 plates TSV 增加 missing tuples.
- refresh canonical inventories `temp/ghidra-functions.csv`, `temp/ghidra-functions-renamed.txt`, `temp/ghidra-functions-auto.txt`, `temp/ghidra-functions-summary.md`. 门禁要求新 `9134` 行size为1326B, `9734` 使用新名且size为2210B, 全工程Function count `5213 -> 5214`, named `5123 -> 5124`, auto保持90; 其余 rows/fields保持. 正式 `doc/dev/naming-proposals.csv` 仅1个既有name cell更新并新增1行.
- 新 `9134` 只由 direct BL调用, 不建立 Thumb odd alias; 本段没有 odd callback target写入.

## 新增 constants / 全局

### `constants/card_info.inc`

- `HORN_OF_HEAVEN_CID = 0x00001300`
- `MOISTURE_CREATURE_CID = 0x000013b5`
- `MAJU_GARZETT_CID = 0x00001654`
- `OCEAN_DRAGON_LORD_NEO_DAEDALUS_CID = 0x000018e8`
- `CID_GAP_1985 = 0x00001985`

结构化卡证据在 `f14-seg2-card-constant-evidence.json`: `data/cards-ids-array.s` 的 icid->cid, `data/card-stats.s` 的 slot/card/passcode, 以及 consumer address闭合. `CID_GAP_1985` 在 cards-ids 映射为 `0xffff`, card-stats 与 passcode均无该 slot; 它只作为 hub range boundary.

### `constants/duel_field.inc`

- `EQUIP_STATE_CLEAR_BITS_8_1_MASK = 0xfffffe01`
- `EQUIP_STATE_CLEAR_BITS_16_9_MASK = 0xfffe01ff`

### `constants/oam_attr.inc`

- `OAM_SPRITE_ATTR_CLR_BITS19_18 = 0xfff3ffff`
- `EQUIP_MODE1_CASE2_SPRITE_CODE_SIDE1 = 0x0000802c`
- `EQUIP_MODE1_CASE8_SPRITE_CODE_SIDE1 = 0x00008044`
- `EQUIP_MODE1_LIST_ENTRY_SPRITE_CODE_SIDE1 = 0x00008049`
- `EQUIP_MODE1_RESULT_SPRITE_CODE_SIDE1 = 0x0000804e`
- `EQUIP_MODE1_PRIMARY_SPRITE_CODE_SIDE1 = 0x0000805f`

其余 equates 与全局全部复用现有 constants/labels. 新全局仅 `equip_mode1_counter_trap_cids`.

## 消费者证据, R6

- 当前 54 words: slots TSV 的 `source_file_line` 已按当前 `asm/14_equip_ai_scoring.s` 重新定位, 并与每行 address annotation一致; `consumer_evidence` 给出 exact PC READ address. Confidence: high.
- hub words: `asm/14_equip_ai_scoring.s:2570-3281`; card-ID comparisons与当前 source words由 refs_to闭合. Confidence: high.
- phase table与新 Function: `asm/14_equip_ai_scoring.s:3282-3291`, plus `f14-seg2-r4-cfg-map.json` addresses `9134..9732`; `9ba6` direct BL证实 live consumer. Confidence: high.
- mode-1 dispatcher/table: `asm/14_equip_ai_scoring.s:3305-3347`, sole caller `asm/14_equip_ai_scoring.s:4013`; cases与 shared tail由 direct-flow map闭合. Confidence: high.
- shared tail: `asm/14_equip_ai_scoring.s:3358-3367`; current CALL `975a` 与六条 R4 JUMP refs精确登记. Confidence: high.
- carved CID table: `0x080a9340` indexed halfword load; structured CID证据见 `f14-seg2-card-constant-evidence.json`; ROM host/bookends见 supplement query. Confidence: high.

## Section 5.1 登记

无. 三个 raw 块均按 R4 disasm; 唯一外部数据表按 R7 carve.

## 落地后门禁

1. 156 slot values 与原 ROM逐项相等; source refs_from, refs_to, equates与 EOL按 TSV核对.
2. 1699 新 InstructionDB address set, length, raw bytes, 248 direct flows, 43 calls, 126 PC reads, 1616 machine/API fallthrough与 map完全相同; 三条 semantic tail calls不使用 FlowOverride.
3. 三个 Function body ranges/size/SHA按 plates TSV核对; `aa10c` Function entry incoming精确为2条, `aa10e` interior incoming精确为5条, body external incoming合计7条. `aa10e` 必须有单一primary `Label/DEFAULT`, 动态ID/name取实际primary且不得等于Function ID `16954`; 其原字节、Instruction、owner、refs_from与EOL保持.
4. 15 switch Data/ref对象保持, 对应11个unique targets; dynamic table target primary只发生批准的 USER materialization变化. Raw3为10 sources/6 unique targets, `9ba4`精确复用5次.
5. carve bytes、left/right bookends与原 incbin end保持; `9458` DATA ref接通.
6. 全部写入 PLATE/EOL ASCII; 6条 new PLATE <=500 chars.
7. re-export, inject modes, split, build 后 ROM byte-identical; source/DB/inventory/CSV/registry scope只包含本 proposal批准项. 四份Function inventory只接受上述 `temp/` canonical paths, 并核对 `9134`/1326B、`9734`新名/2210B、5214/5124/90统计.

## 求助

none.

## Executor Report: F14-Seg-2

- 槽: EQ=104, REF=37, RENAME=0, TABLE=15, total=156; FUNC_RENAME=1; NEW_FUNCTION=1; PLATE_WRITE=6, PLATE_PRESERVE=1.
- carve=1 (6 bytes), disasm=36 maximal ranges / 1699 InstructionDB, Section 5.1=0.
- 新增 constants/全局: 13 constants; `equip_mode1_counter_trap_cids`.
- 求助: none.
- proposal: `doc/dev/refine/F14-Seg-2.proposal.md`.
