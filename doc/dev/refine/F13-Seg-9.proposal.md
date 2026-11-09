# Refine Proposal: F13-Seg-9 [0x080a585c..0x080a689c)

## 0. 结论

- 严格主范围为 `[0x080a585c,0x080a689c)`, 长度 `0x1040 = 4160` bytes。`0x080a689c` 是 Seg-10 首地址；本提案不解释 Seg-10 的新语义。
- 段内实测既有 Function=13，均为 USER_DEFINED Global Function。保留7个现名，订正6个误名；不创建、删除、拆分或调整 Function body。
- 段内共有145个4-byte word：111个残留自动名槽和34个既有 switch pointer word。111槽组成 `DAT=60, DWORD=37, PTR=14`，逐槽动作 `EQ=44, REF=52, RENAME=15`；34个 switch word 全部 PRESERVE。
- Ghidra 布局为1689条 InstructionDB，其中1654条助记符源码行、35条 `.hword` instruction projection；DataDB共203项，其中145个4-byte word、58个1-byte padding，源码投影中的 padding 为29个连续2-byte范围。字节闭合为 `1617*2 + 72*4 + 145*4 + 58 = 4160`，覆盖无空洞或重叠。
- 主范围内没有 `ROM_INCBIN` 或 `.byte` 块。必要范围外闭包新增1个 carve：`[0x09e478b0,0x09e478bc)` 三个 Valkyrion material CID words；carve=1、disasm=0、Rule 3 / §5.1=0。
- Function rename=6。PLATE full rewrite=16，加上2条既有合规全文等值写入，共18条：段内13条、受改名影响的段外 caller 5条。18条新 PLATE 全部 ASCII，最长437字符。
- 新增常量=0。44个 EQ 槽全部复用既有常量或别名目标，其中 `0x080a5f30/0x080a5f34` 分别复用 `constants/demo_state.inc:15,20` 的 `DEMO_CLEAR_BITS_8_1` 与 `DEMO_CLEAR_BITS_16_9`。新增 ROM global=1：`valkyrion_target_material_cids`。新增 Thumb alias=7。
- `constants/card_info.inc:1152` 仅订正 `GAMMA_MAGNET_WARRIOR_CID` 现有注释中的密码 `27175001 -> 11549357`；equate 名称和值 `0x000012b8` 保持不变。
- 全 ROM 扫描确认段内7个 predicate 入口另有14个 packed Thumb source word。8个指向改名函数的既有 `/dword` source 加 equate 并导出为 `.word <new_name>_1`；6个指向保留函数的 source 只冻结前态。所有 odd target 均不创建 label/ref/data。
- BLOCKED: none。函数订正、常量、全局引用和 carve 均有控制流、消费者或原始字节证据，置信度 high。

## 1. 前态与权威证据

| artifact | role | SHA256 |
|---|---|---|
| `output/refine-run-20261011-103530/root-f13-seg9-baseline.json` | 13 Function, 4160B, InstructionDB/DataDB, ELF/source/ROM independent baseline | `4a44841594b0b90891f639fdbb3331e2f2e63ff74e77d31a1592ca6dd49af16d` |
| `output/refine-run-20261011-103530/root-f13-seg9-db-backup.json` | 15-file physical Ghidra backup manifest | `3b5d4d9090ea25f2388dd909ca3e5c402f29cedfaac5ed899311d1c3c4552135` |
| `output/refine-run-20261011-103530/root-source-baseline-f13seg9.json` | 72-file source/constants/registry/CSV baseline | `9f676a742d1729fbcc35c1c7b9a60e15bfbf94ba85cff50bc1b76ab55eba3b98` |
| `output/refine-run-20261011-103530/f13-seg9-functions-prestate.json` | segment Functions, 145 words, 111 slots, full 4160-byte code-unit prestate | `57664e39741e686544859eebcc73995ef6351230bd41f713fb4f4f1623cf7d83` |
| `output/refine-run-20261011-103530/f13-seg9-functions-prestate-db-check.json` | 15 DB hashes after first read-only query | `876ddec7a6c561433d854b2f65902afb6cf89a3b33fc00abbde3298891944c1f` |
| `output/refine-run-20261011-103530/f13-seg9-projections-prestate.json` | 11 outside Functions, 14 packed sources, 8 CALL sites, carve target, asset hit | `b63ca33dacafaef171c1e8e5c561fb8e442687de1c6a92366607271f984528c5` |
| `output/refine-run-20261011-103530/f13-seg9-projections-db-check.json` | 15 DB hashes after projection read-only query | `15b7623bb4bae3e218e8894dfb0b3dfe7006b64284e2ef4986603ccf7e8088b7` |
| `output/refine-run-20261011-103530/f13-seg9-refscan.tsv` | 111 slot-address raw/THUMB scan | `0f2a96e6a2e76a377000cd71d581d32f6421cb2d66074d3388bee047c81c6f82` |
| `output/refine-run-20261011-103530/f13-seg9-function-refscan.tsv` | 13 Function entry raw/THUMB scan | `9254fb60e8bcc687621a1f4a4d941ef44fa673275bce9dbc8d95321079adf136` |
| `output/refine-run-20261011-103530/f13-seg9-external-table-refscan.tsv` | external 12-byte table raw/THUMB scan | `d606c808c3c0a44cda44005b59130a88f6fce56ede4f12193178ef961758fc64` |
| `output/refine-run-20261011-103530/f13-seg9-switch-words-prestate.tsv` | 34 existing switch words exact freeze | `be83890edc56780637143467d3ad697b5282cf17e315537f7f5fd05626b51b37` |
| `output/refine-run-20261011-103530/f13-seg9-packed-thumb-prestate.tsv` | 14 packed Thumb source words exact freeze/action | `0bd2469e770595cb5b95e11c5a1349b50f6827533c33dc6fbc80c2b450b41a80` |
| `output/refine-run-20261011-103530/f13-seg9-executor-manifest.json` | immutable first-round executor evidence manifest; retained as historical input | `705e3081a8bff716993fa9b92decdd06b7aac50c69d6909b50bed2a431229191` |
| `doc/dev/refine/F13-Seg-9.slots.tsv` | 111 automatic-slot normative implementation contract, Mode A v2 | `2e1ddfd1d7896b39decd2884c1067276519106e98e72a0b074d02d7885050e6d` |
| `doc/dev/refine/F13-Seg-9.plates.tsv` | 18 Function/PLATE normative implementation contract, Mode A v2 | `36548a9fc69ac3916c5362e7f449749dfb86f4c3649cbe30254b69aeef22d5a4` |

两次 Ghidra 查询均使用 `-noanalysis -readOnly`。每次查询后15个 DB 文件 SHA256 与物理备份清单逐文件一致；查询不改工程。RAM target 只读取已定义 Symbol/Data 元数据，证据中的 RAM bytes 保持 `null`。

`F13-Seg-9.slots.tsv` 是111个自动槽的规范附件。每行冻结 `address, old_name, kind, original_value, action, target_symbol, target_contract, final_slot_label, reuse_status, slot_symbol_id/source/type, defined_data, existing_refs/equates/eol, raw/thumb scan, consumers, file:line, confidence, eol_ascii`。Fixer 必须逐行执行。

`F13-Seg-9.plates.tsv` 是18个 Function/PLATE 的规范附件。它冻结 Function Symbol/namespace/ID、完整 body/body SHA256、calling convention、signature/prototype、storage flags、return/parameters、incoming、旧 PLATE SHA256、新全文和 registry 合同。

111个 source slot 当前 primary Symbol 都是 dynamic DEFAULT；TSV中的 source Symbol ID只定位前态，物化唯一 USER label 时允许发生合法 ID 变化。静态 USER target、Function、既有 switch target 与外部投影对象的 ID必须精确守恒。

## 2. 段测绘

### 2.1 Function inventory

| entry | current name | final name | ID | source | body bytes | source | action |
|---|---|---|---|---|---|---|---|
| `0x080a585c` | `check_equip_sub_entry_slot_pair_with_field_scan` | `check_gate_guardian_material_slot_requirement` | 4399 | USER_DEFINED | 294 | `asm/13_equip_placement.s:17915` | RENAME_PLATE |
| `0x080a5994` | `check_equip_target_slot_eligible_by_zone_scan` | `check_valkyrion_material_slot_requirement` | 16728 | USER_DEFINED | 322 | `asm/13_equip_placement.s:18094` | RENAME_PLATE |
| `0x080a5afc` | `check_equip_target_slot_eligible_by_extended_stat` | `check_equip_target_slot_eligible_by_extended_stat` | 16729 | USER_DEFINED | 168 | `asm/13_equip_placement.s:18304` | PLATE_ONLY |
| `0x080a5bc8` | `check_equip_target_slot_eligible_by_activate_flag` | `check_masked_beast_des_gardius_material_slot_requirement` | 16730 | USER_DEFINED | 236 | `asm/13_equip_placement.s:18431` | RENAME_PLATE |
| `0x080a5cc8` | `check_equip_target_slot_eligible_by_monster_space` | `check_equip_target_slot_eligible_by_monster_space` | 16731 | USER_DEFINED | 126 | `asm/13_equip_placement.s:18577` | PLATE_ONLY |
| `0x080a5d4c` | `check_equip_target_slot_eligible_by_display_code` | `check_equip_target_slot_eligible_by_display_code` | 16732 | USER_DEFINED | 72 | `asm/13_equip_placement.s:18660` | PLATE_ONLY |
| `0x080a5da0` | `check_equip_target_slot_eligible_by_bonus_eval` | `check_ancient_gear_castle_counter_slot_requirement` | 16733 | USER_DEFINED | 114 | `asm/13_equip_placement.s:18722` | RENAME_PLATE |
| `0x080a5e28` | `init_equip_entry_sprite_fields` | `init_equip_zone_rank_state_from_slot` | 4761 | USER_DEFINED | 242 | `asm/13_equip_placement.s:18794` | RENAME_PLATE |
| `0x080a5f38` | `apply_equip_entry_sprite_from_slot_context` | `init_equip_zone_rank_state_from_lp_context` | 4762 | USER_DEFINED | 56 | `asm/13_equip_placement.s:18938` | RENAME_PLATE |
| `0x080a5f7c` | `dispatch_equip_state_by_combined_phase_index` | `dispatch_equip_state_by_combined_phase_index` | 5586 | USER_DEFINED | 1084 | `asm/13_equip_placement.s:18976` | PLATE_ONLY |
| `0x080a6508` | `dispatch_equip_confirm_action_by_phase` | `dispatch_equip_confirm_action_by_phase` | 5724 | USER_DEFINED | 256 | `asm/13_equip_placement.s:19682` | PLATE_ONLY |
| `0x080a6630` | `tick_equip_target_phase_with_lp_confirm_slot_context` | `tick_equip_target_phase_with_lp_confirm_slot_context` | 5805 | USER_DEFINED | 220 | `asm/13_equip_placement.s:19830` | PLATE_ONLY |
| `0x080a672c` | `tick_equip_target_phase_with_lp_confirm_multistep` | `tick_equip_target_phase_with_lp_confirm_multistep` | 16734 | USER_DEFINED | 332 | `asm/13_equip_placement.s:19960` | PLATE_ONLY |

精确 Function body 冻结如下：

| entry | exact body | body SHA256 |
|---|---|---|
| `0x080a585c` | `[[080a585c, 080a5973] [080a5984, 080a5991]]` | `27e5b17ad37022407553c38968b722ac02bea2a1d0ab4b5fabb3eddd076a33bf` |
| `0x080a5994` | `[[080a5994, 080a5a35] [080a5a48, 080a5ab7] [080a5ac4, 080a5ae1] [080a5ae8, 080a5af9]]` | `4230c98d1886112abb87bdd6516e178cfbae57b4436c49b705aa1d5d7a334fef` |
| `0x080a5afc` | `[[080a5afc, 080a5b17] [080a5b1c, 080a5b35] [080a5b44, 080a5b55] [080a5b60, 080a5b87] [080a5b90, 080a5bc7]]` | `954d9f884de7358a05e10c2de305c2c250dfc2b34b6afcd643c0fb10820af96b` |
| `0x080a5bc8` | `[[080a5bc8, 080a5bf3] [080a5bf8, 080a5c3b] [080a5c4c, 080a5cc7]]` | `5a98dfbd7b070327e0916df5005ef6ace1824a21bec3956ad05ce55a6c4a8737` |
| `0x080a5cc8` | `[[080a5cc8, 080a5d15] [080a5d1c, 080a5d4b]]` | `7a9baf866230659762b1ed27cf861cf479055f2195270becb26b5320c906f82d` |
| `0x080a5d4c` | `[[080a5d4c, 080a5d8b] [080a5d98, 080a5d9f]]` | `e03185b94a060f85c35a02e7326a2e885274fe8565189d9aaddb71f44e5cabea` |
| `0x080a5da0` | `[[080a5da0, 080a5dff] [080a5e14, 080a5e25]]` | `0cb3e458e498c9d1fdbac8132949c03965cf845cd70c8dc081a6443fbfa758b6` |
| `0x080a5e28` | `[[080a5e28, 080a5ea1] [080a5eb0, 080a5edd] [080a5ee4, 080a5f2d]]` | `69ae90280d56d6a6c74513f8d01cd35ce22caffa0109c894a593e851ef73891b` |
| `0x080a5f38` | `[[080a5f38, 080a5f6f]]` | `f9ad7fb011b59b4e4e1826f43d02265df665f42f074b687e722a8729d4edc347` |
| `0x080a5f7c` | `[[080a5f7c, 080a5fa3] [080a6038, 080a6087] [080a608c, 080a60ad] [080a60bc, 080a60d3] [080a60d8, 080a6101] [080a6110, 080a6197] [080a61b0, 080a61e5] [080a61ec, 080a6223] [080a6228, 080a6249] [080a6258, 080a6271] [080a6278, 080a6301] [080a631c, 080a6347] [080a634c, 080a63bb] [080a63c0, 080a63e1] [080a63f0, 080a6427] [080a6438, 080a6471] [080a647c, 080a64b9] [080a64cc, 080a64f1] [080a64f8, 080a6507]]` | `10b7e914d7cd1d5d74dea1d45bdc1af90600eff8f3d0386e5c76585d911bdd23` |
| `0x080a6508` | `[[080a6508, 080a6529] [080a6534, 080a6557] [080a6560, 080a65cd] [080a65dc, 080a6617] [080a6620, 080a662f]]` | `6e71d15094b686b62dc7334ba8d365fe68007f1f762dd7603cb4cdfb139700b0` |
| `0x080a6630` | `[[080a6630, 080a6643] [080a6648, 080a6685] [080a6690, 080a66d3] [080a66dc, 080a6717] [080a6720, 080a6729]]` | `5cc2e1f147d419a1b699debd2768218b49489909bb76b36bfb64d363732da757` |
| `0x080a672c` | `[[080a672c, 080a674d] [080a6754, 080a67bb] [080a67c4, 080a67fd] [080a6808, 080a6871] [080a687c, 080a6899]]` | `24d5716d244d903b4f6a891f7b4ada0c0f889724fdf38c57218de7b93add4a86` |

### 2.2 Word 和 code-unit inventory

- 自动槽111：`DAT=60, DWORD=37, PTR=14`。source Symbol 均为 DEFAULT Label；逐槽 ID 和 Data type 在 `slots.tsv`。
- 34个既有 switch pointer words 位于 `[0x080a5fb0,0x080a6038)`；第一项有 ANALYSIS namespace Symbol ID5291，其余项没有 primary Symbol，34项 Data 均为 `/pointer:4`，每项有一条 DEFAULT DATA ref 指向既有 case label。
- 111槽共有118个 PC-relative READ consumer；全部 consumer 地址与 `file:line` 在 `slots.tsv`。
- InstructionDB/DataDB 地址集合连续覆盖主范围。ROM bytes、源码字节注释、Ghidra code-unit 起址集合和 ELF 中145个 word 表达式全部一致。

## 3. 数据块分类 (Rule 2/3)

| 块 | ref-scan raw / THUMB|1 | 判定 | 理由 |
|---|---|---|---|
| 主范围 `[0x080a585c,0x080a689c)` | none | none | 仅有既有 InstructionDB、145 words 和 alignment padding；无 ROM_INCBIN/.byte block |
| `[0x09e478b0,0x09e478bc)` 12B | raw=1 at `0x080a5a38`; thumb=0 | carve | 消费者按 `gEquipZoneRankState[8]` 索引三个 u32 CID；原值为 Alpha/Beta/Gamma Magnet Warrior |
| slot-address candidate `0x080a5bf4` | raw=0; thumb=1 at ROM `0x08925741` | asset coincidence | 命中位于压缩卡图 `tb0891.bin+0x0ec1`，不是代码或指针 source |

R8 偶合证据：`graphics/bin/card-images/tiles/tb0891.bin+0x0ec1` 原始4字节为 `f55b0a08`，周围原字节为 `43bdef0b369756d2f55b0a08f3d6f34b09030282`；宿主 `data/card-image-tiles.s:897`。原始命中数保持 raw=0、THUMB|1=1，不计入引用。

本段没有 disasm range，也没有0引用块需要登记 §5.1。

## 4. 符号化计划 (R1/R2/R3)

### 4.1 EQ_SLOTS (44)

| slot | old | value | const/alias | final slot label | reuse | prestate | consumer file:line | confidence | EOL ASCII |
|---|---|---|---|---|---|---|---|---|---|
| `0x080a5978` | `DAT_080a5978` | `0x00000868` | `PLAYER_BLOCK_STRIDE` | `player_block_stride_080a5978` | REUSE | ID=4611686018562283896; /undefined4:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:17940@080a588e;asm/13_equip_placement.s:18023@080a592c` | high | PLAYER_BLOCK_STRIDE: named literal value. |
| `0x080a5980` | `DAT_080a5980` | `0x00001119` | `SANGA_OF_THUNDER_CID` | `sanga_of_thunder_cid_080a5980` | REUSE | ID=4611686018562283904; /undefined4:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:17949@080a58a0;asm/13_equip_placement.s:18031@080a593c` | high | SANGA_OF_THUNDER_CID: named literal value. |
| `0x080a5a40` | `DWORD_080a5a40` | `0x00000868` | `PLAYER_BLOCK_STRIDE` | `player_block_stride_080a5a40` | REUSE | ID=4611686018562284096; /dword:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:18147@080a59fc` | high | PLAYER_BLOCK_STRIDE: named literal value. |
| `0x080a5abc` | `DWORD_080a5abc` | `0x00000868` | `PLAYER_BLOCK_STRIDE` | `player_block_stride_080a5abc` | REUSE | ID=4611686018562284220; /dword:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:18217@080a5a88` | high | PLAYER_BLOCK_STRIDE: named literal value. |
| `0x080a5b38` | `DWORD_080a5b38` | `0x000016cb` | `BLACK_LUSTER_SOLDIER_ENVOY_CID` | `black_luster_soldier_envoy_cid_080a5b38` | REUSE | ID=4611686018562284344; /dword:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:18325@080a5b22` | high | BLACK_LUSTER_SOLDIER_ENVOY_CID: named literal value. |
| `0x080a5b3c` | `DWORD_080a5b3c` | `0x00001466` | `DARK_NECROFEAR_CID` | `dark_necrofear_cid_080a5b3c` | REUSE | ID=4611686018562284348; /dword:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:18330@080a5b2c` | high | DARK_NECROFEAR_CID: named literal value. |
| `0x080a5b40` | `DWORD_080a5b40` | `0x000016c9` | `CHAOS_SORCERER_CID` | `chaos_sorcerer_cid_080a5b40` | REUSE | ID=4611686018562284352; /dword:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:18333@080a5b32` | high | CHAOS_SORCERER_CID: named literal value. |
| `0x080a5b58` | `DWORD_080a5b58` | `0x000018b4` | `MEGAROCK_DRAGON_CID` | `megarock_dragon_cid_080a5b58` | REUSE | ID=4611686018562284376; /dword:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:18343@080a5b44` | high | MEGAROCK_DRAGON_CID: named literal value. |
| `0x080a5b5c` | `DWORD_080a5b5c` | `0x000016e4` | `CHAOS_EMPEROR_DRAGON_CID` | `chaos_emperor_dragon_cid_080a5b5c` | REUSE | ID=4611686018562284380; /dword:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:18348@080a5b4e` | high | CHAOS_EMPEROR_DRAGON_CID: named literal value. |
| `0x080a5b88` | `DWORD_080a5b88` | `0x000019ca` | `DOOM_DOZER_CID` | `doom_dozer_cid_080a5b88` | REUSE | ID=4611686018562284424; /dword:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:18359@080a5b60` | high | DOOM_DOZER_CID: named literal value. |
| `0x080a5c40` | `DWORD_080a5c40` | `0x00000868` | `PLAYER_BLOCK_STRIDE` | `player_block_stride_080a5c40` | REUSE | ID=4611686018562284608; /dword:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:18474@080a5c1e` | high | PLAYER_BLOCK_STRIDE: named literal value. |
| `0x080a5c48` | `DWORD_080a5c48` | `0x000013e5` | `GRAND_TIKI_ELDER_CID` | `grand_tiki_elder_cid_080a5c48` | REUSE | ID=4611686018562284616; /dword:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:18482@080a5c2e` | high | GRAND_TIKI_ELDER_CID: named literal value. |
| `0x080a5d90` | `DWORD_080a5d90` | `0x00000868` | `PLAYER_BLOCK_STRIDE` | `player_block_stride_080a5d90` | REUSE | ID=4611686018562284944; /dword:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:18675@080a5d6a` | high | PLAYER_BLOCK_STRIDE: named literal value. |
| `0x080a5e04` | `DWORD_080a5e04` | `0x000013f2` | `MASK_OF_RESTRICT_CID` | `mask_of_restrict_cid_080a5e04` | REUSE | ID=4611686018562285060; /dword:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:18734@080a5db8` | high | MASK_OF_RESTRICT_CID: named literal value. |
| `0x080a5e08` | `DWORD_080a5e08` | `0x000019b2` | `ANCIENT_GEAR_CASTLE_CID` | `ancient_gear_castle_cid_080a5e08` | REUSE | ID=4611686018562285064; /dword:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:18738@080a5dc2` | high | ANCIENT_GEAR_CASTLE_CID: named literal value. |
| `0x080a5e0c` | `DWORD_080a5e0c` | `0x00000868` | `PLAYER_BLOCK_STRIDE` | `player_block_stride_080a5e0c` | REUSE | ID=4611686018562285068; /dword:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:18756@080a5dea` | high | PLAYER_BLOCK_STRIDE: named literal value. |
| `0x080a5eac` | `DAT_080a5eac` | `0xff8000ff` | `EQUIP_ACTIVATION_CARD_ID_CLEAR_MASK` | `equip_activation_card_id_clear_mask_080a5eac` | REUSE | ID=4611686018562285228; /undefined4:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:18815@080a5e52` | high | EQUIP_ACTIVATION_CARD_ID_CLEAR_MASK: named literal value. |
| `0x080a5ee0` | `DAT_080a5ee0` | `0x0000135d` | `LIGHT_OF_INTERVENTION_CID` | `light_of_intervention_cid_080a5ee0` | REUSE | ID=4611686018562285280; /undefined4:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:18871@080a5ebe` | high | LIGHT_OF_INTERVENTION_CID: named literal value. |
| `0x080a5f30` | `DAT_080a5f30` | `0xfffffe01` | `DEMO_CLEAR_BITS_8_1` | `equip_phase_clear_bits_8_1_mask_080a5f30` | REUSE | ID=4611686018562285360; /undefined4:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:18915@080a5f10` | high | DEMO_CLEAR_BITS_8_1: named literal value. |
| `0x080a5f34` | `DAT_080a5f34` | `0xfffe01ff` | `DEMO_CLEAR_BITS_16_9` | `equip_phase_clear_bits_16_9_mask_080a5f34` | REUSE | ID=4611686018562285364; /undefined4:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:18921@080a5f1c` | high | DEMO_CLEAR_BITS_16_9: named literal value. |
| `0x080a5f74` | `DAT_080a5f74` | `0x00001d68` | `ELIGIB_SPRITE_CTRL_OFF` | `eligib_sprite_ctrl_off_080a5f74` | REUSE | ID=4611686018562285428; /undefined4:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:18942@080a5f40` | high | ELIGIB_SPRITE_CTRL_OFF: named literal value. |
| `0x080a5f78` | `DAT_080a5f78` | `0x00001d54` | `ELIGIB_STATE_CTRL_OFF` | `eligib_state_ctrl_off_080a5f78` | REUSE | ID=4611686018562285432; /undefined4:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:18958@080a5f60` | high | ELIGIB_STATE_CTRL_OFF: named literal value. |
| `0x080a5fa4` | `DAT_080a5fa4` | `0xfffffe00` | `STACK_ALLOC_NEG_512` | `stack_alloc_neg_512_080a5fa4` | REUSE | ID=4611686018562285476; /undefined4:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:18977@080a5f7e` | high | STACK_ALLOC_NEG_512: named literal value. |
| `0x080a619c` | `DAT_080a619c` | `0x00001d68` | `ELIGIB_SPRITE_CTRL_OFF` | `eligib_sprite_ctrl_off_080a619c` | REUSE | ID=4611686018562285980; /undefined4:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:19159@080a611a` | high | ELIGIB_SPRITE_CTRL_OFF: named literal value. |
| `0x080a61a0` | `DAT_080a61a0` | `0x00001d6c` | `ELIGIB_ANIM_STATE_OFF` | `eligib_anim_state_off_080a61a0` | REUSE | ID=4611686018562285984; /undefined4:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:19162@080a6120` | high | ELIGIB_ANIM_STATE_OFF: named literal value. |
| `0x080a61a4` | `DAT_080a61a4` | `0x00001d70` | `LP_BANISHER_CTX_OFF` | `lp_banisher_ctx_off_080a61a4` | REUSE | ID=4611686018562285988; /undefined4:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:19164@080a6124` | high | LP_BANISHER_CTX_OFF: named literal value. |
| `0x080a6308` | `DAT_080a6308` | `0x00001d68` | `ELIGIB_SPRITE_CTRL_OFF` | `eligib_sprite_ctrl_off_080a6308` | REUSE | ID=4611686018562286344; /undefined4:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:19344@080a6282` | high | ELIGIB_SPRITE_CTRL_OFF: named literal value. |
| `0x080a630c` | `DAT_080a630c` | `0x00001d6c` | `ELIGIB_ANIM_STATE_OFF` | `eligib_anim_state_off_080a630c` | REUSE | ID=4611686018562286348; /undefined4:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:19347@080a6288` | high | ELIGIB_ANIM_STATE_OFF: named literal value. |
| `0x080a6310` | `DAT_080a6310` | `0x00001d70` | `LP_BANISHER_CTX_OFF` | `lp_banisher_ctx_off_080a6310` | REUSE | ID=4611686018562286352; /undefined4:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:19349@080a628c` | high | LP_BANISHER_CTX_OFF: named literal value. |
| `0x080a6434` | `DAT_080a6434` | `0x080a5189` | `check_equip_sub_entry_slot_pair_eligible_1` | `check_equip_sub_entry_slot_pair_eligible_thumb_ptr_080a6434` | NEW | ID=4611686018562286644; /undefined4:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:19557@080a641c` | high | check_equip_sub_entry_slot_pair_eligible_1: named literal value. |
| `0x080a6474` | `DAT_080a6474` | `0x080a5189` | `check_equip_sub_entry_slot_pair_eligible_1` | `check_equip_sub_entry_slot_pair_eligible_thumb_ptr_080a6474` | NEW | ID=4611686018562286708; /undefined4:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:19571@080a6438` | high | check_equip_sub_entry_slot_pair_eligible_1: named literal value. |
| `0x080a64c0` | `DAT_080a64c0` | `0x00001d68` | `ELIGIB_SPRITE_CTRL_OFF` | `eligib_sprite_ctrl_off_080a64c0` | REUSE | ID=4611686018562286784; /undefined4:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:19611@080a6486` | high | ELIGIB_SPRITE_CTRL_OFF: named literal value. |
| `0x080a64c4` | `DAT_080a64c4` | `0x00001d6c` | `ELIGIB_ANIM_STATE_OFF` | `eligib_anim_state_off_080a64c4` | REUSE | ID=4611686018562286788; /undefined4:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:19614@080a648c` | high | ELIGIB_ANIM_STATE_OFF: named literal value. |
| `0x080a652c` | `DAT_080a652c` | `0xfffffe00` | `STACK_ALLOC_NEG_512` | `stack_alloc_neg_512_080a652c` | REUSE | ID=4611686018562286892; /undefined4:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:19683@080a650a` | high | STACK_ALLOC_NEG_512: named literal value. |
| `0x080a655c` | `DAT_080a655c` | `0x080a533d` | `check_moth_evolution_slot_requirement_1` | `check_moth_evolution_slot_requirement_thumb_ptr_080a655c` | NEW | ID=4611686018562286940; /undefined4:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:19718@080a654e` | high | check_moth_evolution_slot_requirement_1: named literal value. |
| `0x080a65d0` | `DAT_080a65d0` | `0x000010bc` | `PETIT_MOTH_CID` | `petit_moth_cid_080a65d0` | REUSE | ID=4611686018562287056; /undefined4:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:19736@080a6576` | high | PETIT_MOTH_CID: named literal value. |
| `0x080a65d4` | `DAT_080a65d4` | `0x080a533d` | `check_moth_evolution_slot_requirement_1` | `check_moth_evolution_slot_requirement_thumb_ptr_080a65d4` | NEW | ID=4611686018562287060; /undefined4:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:19747@080a6592` | high | check_moth_evolution_slot_requirement_1: named literal value. |
| `0x080a661c` | `DAT_080a661c` | `0x00001d68` | `ELIGIB_SPRITE_CTRL_OFF` | `eligib_sprite_ctrl_off_080a661c` | REUSE | ID=4611686018562287132; /undefined4:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:19789@080a65e6` | high | ELIGIB_SPRITE_CTRL_OFF: named literal value. |
| `0x080a668c` | `DAT_080a668c` | `0x080a5715` | `check_special_summon_slot_requirement_with_pair_exclusions_1` | `check_special_summon_slot_requirement_with_pair_exclusions_thumb_ptr_080a668c` | NEW | ID=4611686018562287244; /undefined4:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:19869@080a667c` | high | check_special_summon_slot_requirement_with_pair_exclusions_1: named literal value. |
| `0x080a66d4` | `DAT_080a66d4` | `0x080a5715` | `check_special_summon_slot_requirement_with_pair_exclusions_1` | `check_special_summon_slot_requirement_with_pair_exclusions_thumb_ptr_080a66d4` | NEW | ID=4611686018562287316; /undefined4:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:19882@080a6698` | high | check_special_summon_slot_requirement_with_pair_exclusions_1: named literal value. |
| `0x080a671c` | `DAT_080a671c` | `0x00001d68` | `ELIGIB_SPRITE_CTRL_OFF` | `eligib_sprite_ctrl_off_080a671c` | REUSE | ID=4611686018562287388; /undefined4:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:19921@080a66e6` | high | ELIGIB_SPRITE_CTRL_OFF: named literal value. |
| `0x080a67c0` | `DWORD_080a67c0` | `0x080a5715` | `check_special_summon_slot_requirement_with_pair_exclusions_1` | `check_special_summon_slot_requirement_with_pair_exclusions_thumb_ptr_080a67c0` | NEW | ID=4611686018562287552; /dword:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:20030@080a67b2` | high | check_special_summon_slot_requirement_with_pair_exclusions_1: named literal value. |
| `0x080a6800` | `DWORD_080a6800` | `0x080a5715` | `check_special_summon_slot_requirement_with_pair_exclusions_1` | `check_special_summon_slot_requirement_with_pair_exclusions_thumb_ptr_080a6800` | NEW | ID=4611686018562287616; /dword:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:20039@080a67c4` | high | check_special_summon_slot_requirement_with_pair_exclusions_1: named literal value. |
| `0x080a6878` | `DWORD_080a6878` | `0x00001d68` | `ELIGIB_SPRITE_CTRL_OFF` | `eligib_sprite_ctrl_off_080a6878` | REUSE | ID=4611686018562287736; /dword:4; refs=none; eq=none; eol=none | `asm/13_equip_placement.s:20078@080a6812` | high | ELIGIB_SPRITE_CTRL_OFF: named literal value. |

### 4.2 REF_SLOTS (52)

| slot | old | value | target | target prestate/final contract | final slot label | source prestate | consumer file:line | confidence | EOL ASCII |
|---|---|---|---|---|---|---|---|---|---|
| `0x080a5974` | `DAT_080a5974` | `0x0201e4d0` | `gEquipZoneRankState` | id=33146;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_equip_zone_rank_state_080a5974` | ID=4611686018562283892; source=DEFAULT; data=/undefined4:4; refs=none; eol=none | `asm/13_equip_placement.s:17926@080a5870;asm/13_equip_placement.s:17962@080a58b8;asm/13_equip_placement.s:17982@080a58e2` | high | gEquipZoneRankState: install operand-0 DATA reference. |
| `0x080a597c` | `DAT_080a597c` | `0x0201c510` | `gDuelFieldSlots` | id=20369;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_duel_field_slots_080a597c` | ID=4611686018562283900; source=DEFAULT; data=/undefined4:4; refs=none; eol=none | `asm/13_equip_placement.s:17943@080a5894;asm/13_equip_placement.s:18026@080a5932` | high | gDuelFieldSlots: install operand-0 DATA reference. |
| `0x080a5a38` | `DWORD_080a5a38` | `0x09e478b0` | `valkyrion_target_material_cids` | pre:symbol=none;data=none;refs_to=0;final=USER_DEFINED Global Label + three /undefined4:4 entries | `valkyrion_target_material_cids_ptr_080a5a38` | ID=4611686018562284088; source=DEFAULT; data=/dword:4; refs=none; eol=none | `asm/13_equip_placement.s:18105@080a59aa;asm/13_equip_placement.s:18138@080a59ec` | high | valkyrion_target_material_cids: install operand-0 DATA reference. |
| `0x080a5a3c` | `DWORD_080a5a3c` | `0x0201e4d0` | `gEquipZoneRankState` | id=33146;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_equip_zone_rank_state_080a5a3c` | ID=4611686018562284092; source=DEFAULT; data=/dword:4; refs=none; eol=none | `asm/13_equip_placement.s:18106@080a59ac` | high | gEquipZoneRankState: install operand-0 DATA reference. |
| `0x080a5a44` | `DWORD_080a5a44` | `0x0201c510` | `gDuelFieldSlots` | id=20369;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_duel_field_slots_080a5a44` | ID=4611686018562284100; source=DEFAULT; data=/dword:4; refs=none; eol=none | `asm/13_equip_placement.s:18150@080a5a02` | high | gDuelFieldSlots: install operand-0 DATA reference. |
| `0x080a5ab8` | `DWORD_080a5ab8` | `0x0201e4d0` | `gEquipZoneRankState` | id=33146;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_equip_zone_rank_state_080a5ab8` | ID=4611686018562284216; source=DEFAULT; data=/dword:4; refs=none; eol=none | `asm/13_equip_placement.s:18196@080a5a5c;asm/13_equip_placement.s:18229@080a5a9e` | high | gEquipZoneRankState: install operand-0 DATA reference. |
| `0x080a5ac0` | `DWORD_080a5ac0` | `0x0201c510` | `gDuelFieldSlots` | id=20369;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_duel_field_slots_080a5ac0` | ID=4611686018562284224; source=DEFAULT; data=/dword:4; refs=none; eol=none | `asm/13_equip_placement.s:18220@080a5a8e` | high | gDuelFieldSlots: install operand-0 DATA reference. |
| `0x080a5ae4` | `DWORD_080a5ae4` | `0x0201e4d0` | `gEquipZoneRankState` | id=33146;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_equip_zone_rank_state_080a5ae4` | ID=4611686018562284260; source=DEFAULT; data=/dword:4; refs=none; eol=none | `asm/13_equip_placement.s:18251@080a5aca` | high | gEquipZoneRankState: install operand-0 DATA reference. |
| `0x080a5b18` | `DWORD_080a5b18` | `0x0201e4d0` | `gEquipZoneRankState` | id=33146;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_equip_zone_rank_state_080a5b18` | ID=4611686018562284312; source=DEFAULT; data=/dword:4; refs=none; eol=none | `asm/13_equip_placement.s:18307@080a5b02` | high | gEquipZoneRankState: install operand-0 DATA reference. |
| `0x080a5b8c` | `DWORD_080a5b8c` | `0x0201e4d0` | `gEquipZoneRankState` | id=33146;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_equip_zone_rank_state_080a5b8c` | ID=4611686018562284428; source=DEFAULT; data=/dword:4; refs=none; eol=none | `asm/13_equip_placement.s:18367@080a5b70` | high | gEquipZoneRankState: install operand-0 DATA reference. |
| `0x080a5bf4` | `DWORD_080a5bf4` | `0x0201e4d0` | `gEquipZoneRankState` | id=33146;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_equip_zone_rank_state_080a5bf4` | ID=4611686018562284532; source=DEFAULT; data=/dword:4; refs=none; eol=none | `asm/13_equip_placement.s:18440@080a5bda` | high | gEquipZoneRankState: install operand-0 DATA reference. |
| `0x080a5c3c` | `DWORD_080a5c3c` | `0x0201e4d0` | `gEquipZoneRankState` | id=33146;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_equip_zone_rank_state_080a5c3c` | ID=4611686018562284604; source=DEFAULT; data=/dword:4; refs=none; eol=none | `asm/13_equip_placement.s:18463@080a5c08` | high | gEquipZoneRankState: install operand-0 DATA reference. |
| `0x080a5c44` | `DWORD_080a5c44` | `0x0201c510` | `gDuelFieldSlots` | id=20369;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_duel_field_slots_080a5c44` | ID=4611686018562284612; source=DEFAULT; data=/dword:4; refs=none; eol=none | `asm/13_equip_placement.s:18477@080a5c24` | high | gDuelFieldSlots: install operand-0 DATA reference. |
| `0x080a5d18` | `DWORD_080a5d18` | `0x0201e4d0` | `gEquipZoneRankState` | id=33146;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_equip_zone_rank_state_080a5d18` | ID=4611686018562284824; source=DEFAULT; data=/dword:4; refs=none; eol=none | `asm/13_equip_placement.s:18582@080a5cd2` | high | gEquipZoneRankState: install operand-0 DATA reference. |
| `0x080a5d8c` | `DWORD_080a5d8c` | `0x0201e4d0` | `gEquipZoneRankState` | id=33146;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_equip_zone_rank_state_080a5d8c` | ID=4611686018562284940; source=DEFAULT; data=/dword:4; refs=none; eol=none | `asm/13_equip_placement.s:18662@080a5d50` | high | gEquipZoneRankState: install operand-0 DATA reference. |
| `0x080a5d94` | `DWORD_080a5d94` | `0x0201c600` | `gP1FieldArrayCBase` | id=21613;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_p1_field_array_c_base_080a5d94` | ID=4611686018562284948; source=DEFAULT; data=/dword:4; refs=none; eol=none | `asm/13_equip_placement.s:18678@080a5d70` | high | gP1FieldArrayCBase: install operand-0 DATA reference. |
| `0x080a5e00` | `DWORD_080a5e00` | `0x0201e4d0` | `gEquipZoneRankState` | id=33146;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_equip_zone_rank_state_080a5e00` | ID=4611686018562285056; source=DEFAULT; data=/dword:4; refs=none; eol=none | `asm/13_equip_placement.s:18724@080a5da4` | high | gEquipZoneRankState: install operand-0 DATA reference. |
| `0x080a5e10` | `DWORD_080a5e10` | `0x0201c510` | `gDuelFieldSlots` | id=20369;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_duel_field_slots_080a5e10` | ID=4611686018562285072; source=DEFAULT; data=/dword:4; refs=none; eol=none | `asm/13_equip_placement.s:18759@080a5df0` | high | gDuelFieldSlots: install operand-0 DATA reference. |
| `0x080a5ea4` | `DAT_080a5ea4` | `0x0201e4d0` | `gEquipZoneRankState` | id=33146;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_equip_zone_rank_state_080a5ea4` | ID=4611686018562285220; source=DEFAULT; data=/undefined4:4; refs=none; eol=none | `asm/13_equip_placement.s:18796@080a5e2c` | high | gEquipZoneRankState: install operand-0 DATA reference. |
| `0x080a5fa8` | `DAT_080a5fa8` | `0x0201e4d0` | `gEquipZoneRankState` | id=33146;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_equip_zone_rank_state_080a5fa8` | ID=4611686018562285480; source=DEFAULT; data=/undefined4:4; refs=none; eol=none | `asm/13_equip_placement.s:18979@080a5f82` | high | gEquipZoneRankState: install operand-0 DATA reference. |
| `0x080a5fac` | `DAT_080a5fac` | `0x080a5fb0` | `switchD_080a5fa2__switchdataD_080a5fb0` | id=5291;source=ANALYSIS;type=Label;data=/pointer:4 | `equip_phase_switch_table_ptr_080a5fac` | ID=4611686018562285484; source=DEFAULT; data=/undefined4:4; refs=none; eol=none | `asm/13_equip_placement.s:18993@080a5f9c` | high | switchD_080a5fa2__switchdataD_080a5fb0: install operand-0 DATA reference. |
| `0x080a6088` | `DAT_080a6088` | `0x0201e4d0` | `gEquipZoneRankState` | id=33146;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_equip_zone_rank_state_080a6088` | ID=4611686018562285704; source=DEFAULT; data=/undefined4:4; refs=none; eol=none | `asm/13_equip_placement.s:19070@080a6070` | high | gEquipZoneRankState: install operand-0 DATA reference. |
| `0x080a60b0` | `DAT_080a60b0` | `0x0201e2a0` | `gDuelCardCtxBase` | id=18879;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_duel_card_ctx_base_080a60b0` | ID=4611686018562285744; source=DEFAULT; data=/undefined4:4; refs=none; eol=none | `asm/13_equip_placement.s:19085@080a608c` | high | gDuelCardCtxBase: install operand-0 DATA reference. |
| `0x080a60b4` | `DAT_080a60b4` | `0x0201e4d0` | `gEquipZoneRankState` | id=33146;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_equip_zone_rank_state_080a60b4` | ID=4611686018562285748; source=DEFAULT; data=/undefined4:4; refs=none; eol=none | `asm/13_equip_placement.s:19086@080a608e` | high | gEquipZoneRankState: install operand-0 DATA reference. |
| `0x080a60d4` | `DAT_080a60d4` | `0x0201e4d0` | `gEquipZoneRankState` | id=33146;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_equip_zone_rank_state_080a60d4` | ID=4611686018562285780; source=DEFAULT; data=/undefined4:4; refs=none; eol=none | `asm/13_equip_placement.s:19117@080a60cc` | high | gEquipZoneRankState: install operand-0 DATA reference. |
| `0x080a6108` | `DAT_080a6108` | `0x0201e2a0` | `gDuelCardCtxBase` | id=18879;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_duel_card_ctx_base_080a6108` | ID=4611686018562285832; source=DEFAULT; data=/undefined4:4; refs=none; eol=none | `asm/13_equip_placement.s:19133@080a60e8` | high | gDuelCardCtxBase: install operand-0 DATA reference. |
| `0x080a610c` | `DAT_080a610c` | `0x0201e4d0` | `gEquipZoneRankState` | id=33146;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_equip_zone_rank_state_080a610c` | ID=4611686018562285836; source=DEFAULT; data=/undefined4:4; refs=none; eol=none | `asm/13_equip_placement.s:19134@080a60ea` | high | gEquipZoneRankState: install operand-0 DATA reference. |
| `0x080a61a8` | `DAT_080a61a8` | `0x0201e4d0` | `gEquipZoneRankState` | id=33146;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_equip_zone_rank_state_080a61a8` | ID=4611686018562285992; source=DEFAULT; data=/undefined4:4; refs=none; eol=none | `asm/13_equip_placement.s:19174@080a613a` | high | gEquipZoneRankState: install operand-0 DATA reference. |
| `0x080a61ac` | `DAT_080a61ac` | `0x0201e2a0` | `gDuelCardCtxBase` | id=18879;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_duel_card_ctx_base_080a61ac` | ID=4611686018562285996; source=DEFAULT; data=/undefined4:4; refs=none; eol=none | `asm/13_equip_placement.s:19206@080a617a` | high | gDuelCardCtxBase: install operand-0 DATA reference. |
| `0x080a61e8` | `DAT_080a61e8` | `0x0201e4d0` | `gEquipZoneRankState` | id=33146;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_equip_zone_rank_state_080a61e8` | ID=4611686018562286056; source=DEFAULT; data=/undefined4:4; refs=none; eol=none | `asm/13_equip_placement.s:19256@080a61da` | high | gEquipZoneRankState: install operand-0 DATA reference. |
| `0x080a624c` | `DAT_080a624c` | `0x0201e2a0` | `gDuelCardCtxBase` | id=18879;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_duel_card_ctx_base_080a624c` | ID=4611686018562286156; source=DEFAULT; data=/undefined4:4; refs=none; eol=none | `asm/13_equip_placement.s:19299@080a6228` | high | gDuelCardCtxBase: install operand-0 DATA reference. |
| `0x080a6250` | `DAT_080a6250` | `0x0201e4d0` | `gEquipZoneRankState` | id=33146;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_equip_zone_rank_state_080a6250` | ID=4611686018562286160; source=DEFAULT; data=/undefined4:4; refs=none; eol=none | `asm/13_equip_placement.s:19300@080a622a` | high | gEquipZoneRankState: install operand-0 DATA reference. |
| `0x080a6274` | `DAT_080a6274` | `0x0201e4d0` | `gEquipZoneRankState` | id=33146;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_equip_zone_rank_state_080a6274` | ID=4611686018562286196; source=DEFAULT; data=/undefined4:4; refs=none; eol=none | `asm/13_equip_placement.s:19332@080a626a` | high | gEquipZoneRankState: install operand-0 DATA reference. |
| `0x080a6314` | `DAT_080a6314` | `0x0201e4d0` | `gEquipZoneRankState` | id=33146;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_equip_zone_rank_state_080a6314` | ID=4611686018562286356; source=DEFAULT; data=/undefined4:4; refs=none; eol=none | `asm/13_equip_placement.s:19359@080a62a2` | high | gEquipZoneRankState: install operand-0 DATA reference. |
| `0x080a6318` | `DAT_080a6318` | `0x0201e2a0` | `gDuelCardCtxBase` | id=18879;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_duel_card_ctx_base_080a6318` | ID=4611686018562286360; source=DEFAULT; data=/undefined4:4; refs=none; eol=none | `asm/13_equip_placement.s:19391@080a62e2` | high | gDuelCardCtxBase: install operand-0 DATA reference. |
| `0x080a6348` | `DAT_080a6348` | `0x0201e4d0` | `gEquipZoneRankState` | id=33146;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_equip_zone_rank_state_080a6348` | ID=4611686018562286408; source=DEFAULT; data=/undefined4:4; refs=none; eol=none | `asm/13_equip_placement.s:19437@080a633c` | high | gEquipZoneRankState: install operand-0 DATA reference. |
| `0x080a63e4` | `DAT_080a63e4` | `0x0201e2a0` | `gDuelCardCtxBase` | id=18879;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_duel_card_ctx_base_080a63e4` | ID=4611686018562286564; source=DEFAULT; data=/undefined4:4; refs=none; eol=none | `asm/13_equip_placement.s:19509@080a63c0` | high | gDuelCardCtxBase: install operand-0 DATA reference. |
| `0x080a63e8` | `DAT_080a63e8` | `0x0201e4d0` | `gEquipZoneRankState` | id=33146;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_equip_zone_rank_state_080a63e8` | ID=4611686018562286568; source=DEFAULT; data=/undefined4:4; refs=none; eol=none | `asm/13_equip_placement.s:19510@080a63c2` | high | gEquipZoneRankState: install operand-0 DATA reference. |
| `0x080a642c` | `DAT_080a642c` | `0x0201e2a0` | `gDuelCardCtxBase` | id=18879;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_duel_card_ctx_base_080a642c` | ID=4611686018562286636; source=DEFAULT; data=/undefined4:4; refs=none; eol=none | `asm/13_equip_placement.s:19545@080a6406` | high | gDuelCardCtxBase: install operand-0 DATA reference. |
| `0x080a6430` | `DAT_080a6430` | `0x0201e4d0` | `gEquipZoneRankState` | id=33146;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_equip_zone_rank_state_080a6430` | ID=4611686018562286640; source=DEFAULT; data=/undefined4:4; refs=none; eol=none | `asm/13_equip_placement.s:19546@080a6408` | high | gEquipZoneRankState: install operand-0 DATA reference. |
| `0x080a6478` | `DAT_080a6478` | `0x0201e4d0` | `gEquipZoneRankState` | id=33146;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_equip_zone_rank_state_080a6478` | ID=4611686018562286712; source=DEFAULT; data=/undefined4:4; refs=none; eol=none | `asm/13_equip_placement.s:19574@080a643e` | high | gEquipZoneRankState: install operand-0 DATA reference. |
| `0x080a64c8` | `DAT_080a64c8` | `0x0201e4d0` | `gEquipZoneRankState` | id=33146;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_equip_zone_rank_state_080a64c8` | ID=4611686018562286792; source=DEFAULT; data=/undefined4:4; refs=none; eol=none | `asm/13_equip_placement.s:19626@080a64a6` | high | gEquipZoneRankState: install operand-0 DATA reference. |
| `0x080a64f4` | `DAT_080a64f4` | `0x0201e4d0` | `gEquipZoneRankState` | id=33146;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_equip_zone_rank_state_080a64f4` | ID=4611686018562286836; source=DEFAULT; data=/undefined4:4; refs=none; eol=none | `asm/13_equip_placement.s:19651@080a64d8` | high | gEquipZoneRankState: install operand-0 DATA reference. |
| `0x080a6530` | `DAT_080a6530` | `0x0201e4d0` | `gEquipZoneRankState` | id=33146;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_equip_zone_rank_state_080a6530` | ID=4611686018562286896; source=DEFAULT; data=/undefined4:4; refs=none; eol=none | `asm/13_equip_placement.s:19685@080a650e` | high | gEquipZoneRankState: install operand-0 DATA reference. |
| `0x080a6558` | `DAT_080a6558` | `0x0201e2a0` | `gDuelCardCtxBase` | id=18879;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_duel_card_ctx_base_080a6558` | ID=4611686018562286936; source=DEFAULT; data=/undefined4:4; refs=none; eol=none | `asm/13_equip_placement.s:19705@080a6534` | high | gDuelCardCtxBase: install operand-0 DATA reference. |
| `0x080a65d8` | `DAT_080a65d8` | `0x0201e4d0` | `gEquipZoneRankState` | id=33146;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_equip_zone_rank_state_080a65d8` | ID=4611686018562287064; source=DEFAULT; data=/undefined4:4; refs=none; eol=none | `asm/13_equip_placement.s:19750@080a6598` | high | gEquipZoneRankState: install operand-0 DATA reference. |
| `0x080a6644` | `DAT_080a6644` | `0x0201e4d0` | `gEquipZoneRankState` | id=33146;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_equip_zone_rank_state_080a6644` | ID=4611686018562287172; source=DEFAULT; data=/undefined4:4; refs=none; eol=none | `asm/13_equip_placement.s:19831@080a6632` | high | gEquipZoneRankState: install operand-0 DATA reference. |
| `0x080a6688` | `DAT_080a6688` | `0x0201e2a0` | `gDuelCardCtxBase` | id=18879;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_duel_card_ctx_base_080a6688` | ID=4611686018562287240; source=DEFAULT; data=/undefined4:4; refs=none; eol=none | `asm/13_equip_placement.s:19856@080a6662` | high | gDuelCardCtxBase: install operand-0 DATA reference. |
| `0x080a66d8` | `DAT_080a66d8` | `0x0201e4d0` | `gEquipZoneRankState` | id=33146;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_equip_zone_rank_state_080a66d8` | ID=4611686018562287320; source=DEFAULT; data=/undefined4:4; refs=none; eol=none | `asm/13_equip_placement.s:19885@080a669e` | high | gEquipZoneRankState: install operand-0 DATA reference. |
| `0x080a6750` | `DWORD_080a6750` | `0x0201e4d0` | `gEquipZoneRankState` | id=33146;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_equip_zone_rank_state_080a6750` | ID=4611686018562287440; source=DEFAULT; data=/dword:4; refs=none; eol=none | `asm/13_equip_placement.s:19961@080a672e` | high | gEquipZoneRankState: install operand-0 DATA reference. |
| `0x080a67bc` | `DWORD_080a67bc` | `0x0201e2a0` | `gDuelCardCtxBase` | id=18879;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_duel_card_ctx_base_080a67bc` | ID=4611686018562287548; source=DEFAULT; data=/dword:4; refs=none; eol=none | `asm/13_equip_placement.s:20017@080a6798` | high | gDuelCardCtxBase: install operand-0 DATA reference. |
| `0x080a6804` | `DWORD_080a6804` | `0x0201e4d0` | `gEquipZoneRankState` | id=33146;source=USER_DEFINED;type=Label;data=/undefined4:4 | `ptr_g_equip_zone_rank_state_080a6804` | ID=4611686018562287620; source=DEFAULT; data=/dword:4; refs=none; eol=none | `asm/13_equip_placement.s:20042@080a67ca` | high | gEquipZoneRankState: install operand-0 DATA reference. |

每个 REF 槽物化 USER source label，并从所有列出的 PC-relative `ldr` consumer operand 0 安装 DATA ref 到静态 target；source word 仍由原 little-endian value 生成。`gEquipZoneRankState`, `gDuelFieldSlots`, `gP1FieldArrayCBase`, `gDuelCardCtxBase` 和 switch target 的既有静态 ID守恒。新 carve target 在 `0x09e478b0` 建立唯一 USER Global Label。

### 4.3 RENAME_SLOTS (15)

| slot | old | value | target | final slot label | source prestate | existing ref | consumer file:line | confidence | EOL ASCII |
|---|---|---|---|---|---|---|---|---|---|
| `0x080a5ea8` | `PTR_gP1LifePoints_080a5ea8` | `0x0201c4e0` | `gP1LifePoints` | `ptr_g_p1_life_points_080a5ea8` | ID=4611686018562285224; source=DEFAULT; data=/pointer:4 | DATA:DEFAULT:0201c4e0:op0:primary=true | `asm/13_equip_placement.s:18805@080a5e3e` | high | gP1LifePoints: preserve existing operand-0 DATA reference. |
| `0x080a5f70` | `PTR_gP1LifePoints_080a5f70` | `0x0201c4e0` | `gP1LifePoints` | `ptr_g_p1_life_points_080a5f70` | ID=4611686018562285424; source=DEFAULT; data=/pointer:4 | DATA:DEFAULT:0201c4e0:op0:primary=true | `asm/13_equip_placement.s:18941@080a5f3e` | high | gP1LifePoints: preserve existing operand-0 DATA reference. |
| `0x080a60b8` | `PTR_gP1LifePoints_080a60b8` | `0x0201c4e0` | `gP1LifePoints` | `ptr_g_p1_life_points_080a60b8` | ID=4611686018562285752; source=DEFAULT; data=/pointer:4 | DATA:DEFAULT:0201c4e0:op0:primary=true | `asm/13_equip_placement.s:19096@080a60a2` | high | gP1LifePoints: preserve existing operand-0 DATA reference. |
| `0x080a6104` | `PTR_gP1LifePoints_080a6104` | `0x0201c4e0` | `gP1LifePoints` | `ptr_g_p1_life_points_080a6104` | ID=4611686018562285828; source=DEFAULT; data=/pointer:4 | DATA:DEFAULT:0201c4e0:op0:primary=true | `asm/13_equip_placement.s:19124@080a60d8` | high | gP1LifePoints: preserve existing operand-0 DATA reference. |
| `0x080a6198` | `PTR_gP1LifePoints_080a6198` | `0x0201c4e0` | `gP1LifePoints` | `ptr_g_p1_life_points_080a6198` | ID=4611686018562285976; source=DEFAULT; data=/pointer:4 | DATA:DEFAULT:0201c4e0:op0:primary=true | `asm/13_equip_placement.s:19158@080a6118` | high | gP1LifePoints: preserve existing operand-0 DATA reference. |
| `0x080a6224` | `PTR_gP1LifePoints_080a6224` | `0x0201c4e0` | `gP1LifePoints` | `ptr_g_p1_life_points_080a6224` | ID=4611686018562286116; source=DEFAULT; data=/pointer:4 | DATA:DEFAULT:0201c4e0:op0:primary=true | `asm/13_equip_placement.s:19266@080a61ec` | high | gP1LifePoints: preserve existing operand-0 DATA reference. |
| `0x080a6254` | `PTR_gP1LifePoints_080a6254` | `0x0201c4e0` | `gP1LifePoints` | `ptr_g_p1_life_points_080a6254` | ID=4611686018562286164; source=DEFAULT; data=/pointer:4 | DATA:DEFAULT:0201c4e0:op0:primary=true | `asm/13_equip_placement.s:19310@080a623e` | high | gP1LifePoints: preserve existing operand-0 DATA reference. |
| `0x080a6304` | `PTR_gP1LifePoints_080a6304` | `0x0201c4e0` | `gP1LifePoints` | `ptr_g_p1_life_points_080a6304` | ID=4611686018562286340; source=DEFAULT; data=/pointer:4 | DATA:DEFAULT:0201c4e0:op0:primary=true | `asm/13_equip_placement.s:19343@080a6280` | high | gP1LifePoints: preserve existing operand-0 DATA reference. |
| `0x080a63bc` | `PTR_gP1LifePoints_080a63bc` | `0x0201c4e0` | `gP1LifePoints` | `ptr_g_p1_life_points_080a63bc` | ID=4611686018562286524; source=DEFAULT; data=/pointer:4 | DATA:DEFAULT:0201c4e0:op0:primary=true | `asm/13_equip_placement.s:19446@080a634c` | high | gP1LifePoints: preserve existing operand-0 DATA reference. |
| `0x080a63ec` | `PTR_gP1LifePoints_080a63ec` | `0x0201c4e0` | `gP1LifePoints` | `ptr_g_p1_life_points_080a63ec` | ID=4611686018562286572; source=DEFAULT; data=/pointer:4 | DATA:DEFAULT:0201c4e0:op0:primary=true | `asm/13_equip_placement.s:19520@080a63d6` | high | gP1LifePoints: preserve existing operand-0 DATA reference. |
| `0x080a6428` | `PTR_gP1LifePoints_080a6428` | `0x0201c4e0` | `gP1LifePoints` | `ptr_g_p1_life_points_080a6428` | ID=4611686018562286632; source=DEFAULT; data=/pointer:4 | DATA:DEFAULT:0201c4e0:op0:primary=true | `asm/13_equip_placement.s:19538@080a63f8` | high | gP1LifePoints: preserve existing operand-0 DATA reference. |
| `0x080a64bc` | `PTR_gP1LifePoints_080a64bc` | `0x0201c4e0` | `gP1LifePoints` | `ptr_g_p1_life_points_080a64bc` | ID=4611686018562286780; source=DEFAULT; data=/pointer:4 | DATA:DEFAULT:0201c4e0:op0:primary=true | `asm/13_equip_placement.s:19610@080a6484` | high | gP1LifePoints: preserve existing operand-0 DATA reference. |
| `0x080a6618` | `PTR_gP1LifePoints_080a6618` | `0x0201c4e0` | `gP1LifePoints` | `ptr_g_p1_life_points_080a6618` | ID=4611686018562287128; source=DEFAULT; data=/pointer:4 | DATA:DEFAULT:0201c4e0:op0:primary=true | `asm/13_equip_placement.s:19788@080a65e4` | high | gP1LifePoints: preserve existing operand-0 DATA reference. |
| `0x080a6718` | `PTR_gP1LifePoints_080a6718` | `0x0201c4e0` | `gP1LifePoints` | `ptr_g_p1_life_points_080a6718` | ID=4611686018562287384; source=DEFAULT; data=/pointer:4 | DATA:DEFAULT:0201c4e0:op0:primary=true | `asm/13_equip_placement.s:19920@080a66e4` | high | gP1LifePoints: preserve existing operand-0 DATA reference. |
| `0x080a6874` | `DWORD_080a6874` | `0x0201c4e0` | `gP1LifePoints` | `ptr_g_p1_life_points_080a6874` | ID=4611686018562287732; source=DEFAULT; data=/dword:4 | DATA:USER_DEFINED:0201c4e0:op0:primary=true | `asm/13_equip_placement.s:20077@080a6810` | high | gP1LifePoints: preserve existing operand-0 DATA reference. |

15个 RENAME 槽的 target 均为 USER_DEFINED `gP1LifePoints` Symbol ID15545。前14槽保留 `/pointer:4` 及 operand-0 source=`DEFAULT` DATA ref；`0x080a6874` 单独保留 `/dword:4` 及 operand-0 source=`USER_DEFINED` DATA ref。15槽只将 source primary Symbol 改为 TSV final label并写 ASCII EOL；reference source 与 target Symbol source 分别按上述合同守恒。

### 4.4 既有 switch words (34, 全部 PRESERVE)

| word | value/expression | bytes | symbol ID | symbol | symbol source | Data | DATA-ref target | target ID | action |
|---|---|---|---|---|---|---|---|---|---|
| `0x080a5fb0` | `0x080a6038` | `38600a08` | 5291 | `switchdataD_080a5fb0` | ANALYSIS | /pointer | `switchD_080a5fa2::caseD_0` | 5257 | PRESERVE |
| `0x080a5fb4` | `0x080a64f8` | `f8640a08` | none | `none` | none | /pointer | `switchD_080a5fa2::caseD_1` | 5258 | PRESERVE |
| `0x080a5fb8` | `0x080a64f8` | `f8640a08` | none | `none` | none | /pointer | `switchD_080a5fa2::caseD_1` | 5258 | PRESERVE |
| `0x080a5fbc` | `0x080a64f8` | `f8640a08` | none | `none` | none | /pointer | `switchD_080a5fa2::caseD_1` | 5258 | PRESERVE |
| `0x080a5fc0` | `0x080a64f8` | `f8640a08` | none | `none` | none | /pointer | `switchD_080a5fa2::caseD_1` | 5258 | PRESERVE |
| `0x080a5fc4` | `0x080a64f8` | `f8640a08` | none | `none` | none | /pointer | `switchD_080a5fa2::caseD_1` | 5258 | PRESERVE |
| `0x080a5fc8` | `0x080a64f8` | `f8640a08` | none | `none` | none | /pointer | `switchD_080a5fa2::caseD_1` | 5258 | PRESERVE |
| `0x080a5fcc` | `0x080a64f8` | `f8640a08` | none | `none` | none | /pointer | `switchD_080a5fa2::caseD_1` | 5258 | PRESERVE |
| `0x080a5fd0` | `0x080a64f8` | `f8640a08` | none | `none` | none | /pointer | `switchD_080a5fa2::caseD_1` | 5258 | PRESERVE |
| `0x080a5fd4` | `0x080a64f8` | `f8640a08` | none | `none` | none | /pointer | `switchD_080a5fa2::caseD_1` | 5258 | PRESERVE |
| `0x080a5fd8` | `0x080a63c0` | `c0630a08` | none | `none` | none | /pointer | `switchD_080a5fa2::caseD_a` | 5267 | PRESERVE |
| `0x080a5fdc` | `0x080a63f8` | `f8630a08` | none | `none` | none | /pointer | `switchD_080a5fa2::caseD_b` | 5268 | PRESERVE |
| `0x080a5fe0` | `0x080a647c` | `7c640a08` | none | `none` | none | /pointer | `switchD_080a5fa2::caseD_c` | 5269 | PRESERVE |
| `0x080a5fe4` | `0x080a64f8` | `f8640a08` | none | `none` | none | /pointer | `switchD_080a5fa2::caseD_1` | 5258 | PRESERVE |
| `0x080a5fe8` | `0x080a64f8` | `f8640a08` | none | `none` | none | /pointer | `switchD_080a5fa2::caseD_1` | 5258 | PRESERVE |
| `0x080a5fec` | `0x080a64f8` | `f8640a08` | none | `none` | none | /pointer | `switchD_080a5fa2::caseD_1` | 5258 | PRESERVE |
| `0x080a5ff0` | `0x080a64f8` | `f8640a08` | none | `none` | none | /pointer | `switchD_080a5fa2::caseD_1` | 5258 | PRESERVE |
| `0x080a5ff4` | `0x080a64f8` | `f8640a08` | none | `none` | none | /pointer | `switchD_080a5fa2::caseD_1` | 5258 | PRESERVE |
| `0x080a5ff8` | `0x080a64f8` | `f8640a08` | none | `none` | none | /pointer | `switchD_080a5fa2::caseD_1` | 5258 | PRESERVE |
| `0x080a5ffc` | `0x080a64f8` | `f8640a08` | none | `none` | none | /pointer | `switchD_080a5fa2::caseD_1` | 5258 | PRESERVE |
| `0x080a6000` | `0x080a6228` | `28620a08` | none | `none` | none | /pointer | `switchD_080a5fa2::caseD_14` | 5277 | PRESERVE |
| `0x080a6004` | `0x080a60d8` | `d8600a08` | none | `none` | none | /pointer | `switchD_080a5fa2::caseD_15` | 5278 | PRESERVE |
| `0x080a6008` | `0x080a6278` | `78620a08` | none | `none` | none | /pointer | `switchD_080a5fa2::caseD_16` | 5279 | PRESERVE |
| `0x080a600c` | `0x080a634c` | `4c630a08` | none | `none` | none | /pointer | `switchD_080a5fa2::caseD_17` | 5280 | PRESERVE |
| `0x080a6010` | `0x080a64f8` | `f8640a08` | none | `none` | none | /pointer | `switchD_080a5fa2::caseD_1` | 5258 | PRESERVE |
| `0x080a6014` | `0x080a64f8` | `f8640a08` | none | `none` | none | /pointer | `switchD_080a5fa2::caseD_1` | 5258 | PRESERVE |
| `0x080a6018` | `0x080a64f8` | `f8640a08` | none | `none` | none | /pointer | `switchD_080a5fa2::caseD_1` | 5258 | PRESERVE |
| `0x080a601c` | `0x080a64f8` | `f8640a08` | none | `none` | none | /pointer | `switchD_080a5fa2::caseD_1` | 5258 | PRESERVE |
| `0x080a6020` | `0x080a64f8` | `f8640a08` | none | `none` | none | /pointer | `switchD_080a5fa2::caseD_1` | 5258 | PRESERVE |
| `0x080a6024` | `0x080a64f8` | `f8640a08` | none | `none` | none | /pointer | `switchD_080a5fa2::caseD_1` | 5258 | PRESERVE |
| `0x080a6028` | `0x080a608c` | `8c600a08` | none | `none` | none | /pointer | `switchD_080a5fa2::caseD_1e` | 5287 | PRESERVE |
| `0x080a602c` | `0x080a60d8` | `d8600a08` | none | `none` | none | /pointer | `switchD_080a5fa2::caseD_15` | 5278 | PRESERVE |
| `0x080a6030` | `0x080a6110` | `10610a08` | none | `none` | none | /pointer | `switchD_080a5fa2::caseD_20` | 5289 | PRESERVE |
| `0x080a6034` | `0x080a61ec` | `ec610a08` | none | `none` | none | /pointer | `switchD_080a5fa2::caseD_21` | 5290 | PRESERVE |

34项值、bytes、Data type、source Symbol、incoming PARAM/DATA refs、outgoing DATA ref 和 case target ID 均按 `f13-seg9-switch-words-prestate.tsv` 冻结。Fixer 不对这些 words 创建新标签、equate、EOL 或 ref。

## 5. FUNC_RENAME (6)

| entry | old | new | indeg/source evidence | 理由 | confidence |
|---|---|---|---|---|---|
| `0x080a585c` | `check_equip_sub_entry_slot_pair_with_field_scan` | `check_gate_guardian_material_slot_requirement` | packed Thumb sources=2; direct CALL=0 | 消费者读取 `SANGA_OF_THUNDER_CID + gEquipZoneRankState[8]`，按三个材料阶段检查槽位；对应 Gate Guardian 三材料连续 CID。 | high |
| `0x080a5994` | `check_equip_target_slot_eligible_by_zone_scan` | `check_valkyrion_material_slot_requirement` | packed Thumb sources=2; direct CALL=0 | 消费者从新 carve 的 Alpha/Beta/Gamma CID 表按 state[8] 取值，再验证候选槽；对应 Valkyrion 三材料。 | high |
| `0x080a5bc8` | `check_equip_target_slot_eligible_by_activate_flag` | `check_masked_beast_des_gardius_material_slot_requirement` | packed Thumb sources=2; direct CALL=0 | phase 0 只接受 Grand Tiki Elder 或 Melchid the Four-Face Beast，随后处理重复槽和空间；对应 Masked Beast Des Gardius 材料。 | high |
| `0x080a5da0` | `check_equip_target_slot_eligible_by_bonus_eval` | `check_ancient_gear_castle_counter_slot_requirement` | packed Thumb sources=2; direct CALL=0 | 要求无 Mask of Restrict、目标是 active Ancient Gear Castle，并按 bonus/counter 阈值验收。 | high |
| `0x080a5e28` | `init_equip_entry_sprite_fields` | `init_equip_zone_rank_state_from_slot` | direct CALL=1 at 0x080a5f5c | 写入对象是 `gEquipZoneRankState` 的 card/slot/mode/phase bits；旧名的 sprite-fields 语义与实际全局不一致。 | high |
| `0x080a5f38` | `apply_equip_entry_sprite_from_slot_context` | `init_equip_zone_rank_state_from_lp_context` | direct CALL=7 | 从 LP offsets 读取 pending slot/card context，调用 0x080a5e28 初始化 `gEquipZoneRankState`，再清 pending field。 | high |

6个 Function 的 Function ID、USER_DEFINED source、Global namespace、body/body SHA256、signature、return、parameters、storage flags 和 incoming ref 全部守恒；只改 Function name 和 PLATE。

## 6. PLATE (18, full rewrite)

| entry | host | action | old chars | new chars | full new PLATE |
|---|---|---|---|---|---|
| `0x080a585c` | `asm/13_equip_placement.s` | RENAME_PLATE | 1197 | 405 | Gate Guardian material-slot predicate for player r0, zone r1, and offset r2. Requires total slot <=4, an equip-eligible active card whose ID equals SANGA_OF_THUNDER_CID + gEquipZoneRankState[8], and available monster space or an unblocked matching slot. It scans recorded player/slot pairs and then material phases 1..2 across slots 0..4. Returns 0x800 on the first valid material slot, else 0. Read-only. |
| `0x080a5994` | `asm/13_equip_placement.s` | RENAME_PLATE | 1192 | 373 | Valkyrion material-slot predicate for player r0, zone type r1, and offset r2. Loads the required Alpha, Beta, or Gamma Magnet Warrior CID from valkyrion_target_material_cids[gEquipZoneRankState[8]], verifies the requested entity, and scans candidate slots for equip eligibility plus field blocking. Returns 0x800 when the required material slot is valid, else 0. Read-only. |
| `0x080a5afc` | `asm/13_equip_placement.s` | PLATE_ONLY | 1485 | 402 | Special-summon target predicate for player r0 and slot r1+r2. Requires the stored player and total slot <=4. Card-specific branches compare the slot state code with the stored card extended-stat field or call check_slot_zone_bit_eligible using an extended-stat field. Covered IDs include Dark Necrofear, the Chaos envoys, Megarock Dragon, and Doom Dozer. Returns 0x800 on acceptance, else 0. Read-only. |
| `0x080a5bc8` | `asm/13_equip_placement.s` | RENAME_PLATE | 1247 | 325 | Masked Beast Des Gardius material-slot predicate for player r0 and slot r1+r2. After equip eligibility passes, phase 0 accepts Grand Tiki Elder or Melchid the Four-Face Beast. Later phases reject recorded player/slot duplicates, then require monster space or an unblocked slot. Returns 0x800 on acceptance, else 0. Read-only. |
| `0x080a5cc8` | `asm/13_equip_placement.s` | PLATE_ONLY | 1084 | 366 | Opponent monster-space target predicate for player r0 and slot r1+r2. Requires r0 to be the opponent of the player stored in gEquipZoneRankState and the slot to pass equip eligibility. Phase 0 requires available monster space or an unblocked slot; later phases require a player/slot pair absent from the recorded list. Returns 0x800 on acceptance, else 0. Read-only. |
| `0x080a5d4c` | `asm/13_equip_placement.s` | PLATE_ONLY | 1142 | 273 | Display-code mismatch target predicate. Requires player r0 to match gEquipZoneRankState player, zone type r1 to equal 0xb, and compares the stored display code with the code extracted from the selected slot word. Returns 0x800 only when the codes differ, else 0. Read-only. |
| `0x080a5da0` | `asm/13_equip_placement.s` | RENAME_PLATE | 1227 | 355 | Ancient Gear Castle counter-slot predicate for player r0 and spell/trap slot r1+r2 in 5..9. Requires the stored player, no Mask of Restrict on the field, and an active Ancient Gear Castle in the slot. It accepts when the evaluated bonus and the slot counter satisfy either bonus>6 with counter>1 or bonus<=6 with counter!=0. Returns 0x800 or 0. Read-only. |
| `0x080a5e28` | `asm/13_equip_placement.s` | RENAME_PLATE | 691 | 370 | Initializes gEquipZoneRankState from player r0, slot r1, mode r2, and extra flag r3. Copies the slot card field, stores slot<<7, clears phase fields, sets activation bits, and applies mode 0/1/2 behavior. Mode 0 also tests LIGHT_OF_INTERVENTION_CID field presence. It finishes by clearing phase bit fields with DEMO_CLEAR_BITS_8_1 and DEMO_CLEAR_BITS_16_9. Returns void. |
| `0x080a5f38` | `asm/13_equip_placement.s` | RENAME_PLATE | 575 | 372 | Initializes gEquipZoneRankState from pending LP context. Loads the callee player and slot arguments from gP1LifePoints+ELIGIB_SPRITE_CTRL_OFF and +ACTIVATION_STATE_A_OFF. When mode_flag r1 is zero it uses input r0 as mode; otherwise it uses mode 2. It passes extra flag r2 to init_equip_zone_rank_state_from_slot, clears gP1LifePoints+ELIGIB_STATE_CTRL_OFF, and returns 1. |
| `0x080a5f7c` | `asm/13_equip_placement.s` | PLATE_ONLY | 1309 | 374 | Dispatches the 34-case equip phase table selected by ((gEquipZoneRankState[0x14]&1)<<7)\|(state[0x13]>>1). It allocates a 512-byte frame, rejects indices above 0x21 through the default case, and executes card, slot, display, and placement handlers for the indexed phase. The table at 0x080a5fb0 remains 34 existing pointer words. Returns each case result; default returns -1. |
| `0x080a6508` | `asm/13_equip_placement.s` | PLATE_ONLY | 437 | 437 | Equip confirmation phase callback using gEquipZoneRankState. State 0 reads player control: value 1 selects a target through check_moth_evolution_slot_requirement; otherwise formats the card name and starts prompt 0x12. State 1 waits for confirmation, dispatches card op 0x28 with LP deltas, stores the result byte at +8 and target bytes at +0x0c, and returns 1; wait returns -1. Other states return 0. Updates phase bytes at +0x13/+0x14. |
| `0x080a6630` | `asm/13_equip_placement.s` | PLATE_ONLY | 382 | 382 | Equip target phase callback. If activation bit1 at gEquipZoneRankState+0x12 is clear, returns dispatch_equip_state_by_combined_phase_index(). With bit1 set, state 0 selects through check_special_summon_slot_requirement_with_pair_exclusions or starts prompt 0x12 and returns 0; state 1 returns 1 after confirmed op 0x28 and target storage, or -1 while waiting; later states return 0. |
| `0x080a672c` | `asm/13_equip_placement.s` | PLATE_ONLY | 1184 | 378 | Multistep equip confirmation callback. State 0 clears gEquipZoneRankState[8], starts prompt 0x12, advances the combined phase, and returns 0. State 1 commits card op 0x28 after confirmation, increments the substep, and either repeats or advances when the card-specific activation count is reached; a pending confirmation dispatches op 0x29 and returns -1. Later states return 1. |
| `0x08069e40` | `asm/08_equip_oam_neodaed.s` | PLATE_ONLY | 2186 | 393 | Equip monster-zone placement state machine for the effect slot in r0. It validates the slot and dispatches field states 0x77..0x80. State 0x7f scans equip activation; state 0x7e reads pending LP context and calls init_equip_zone_rank_state_from_lp_context for modes 4 or 6; later states test zone eligibility, enqueue display work, or advance the field state. Returns the next state code or 0. |
| `0x08097070` | `asm/12_equip_activation_scan.s` | PLATE_ONLY | 702 | 236 | Stores slot reference r0 at gP1LifePoints+ELIGIB_SPRITE_CTRL_OFF and extra value r2 at +ACTIVATION_STATE_A_OFF, then calls init_equip_zone_rank_state_from_lp_context(1,1,0). Returns 0. This is the first of two symmetric table callbacks. |
| `0x080970a0` | `asm/12_equip_activation_scan.s` | PLATE_ONLY | 745 | 237 | Stores slot reference r0 at gP1LifePoints+ELIGIB_SPRITE_CTRL_OFF and extra value r2 at +ACTIVATION_STATE_A_OFF, then calls init_equip_zone_rank_state_from_lp_context(1,1,0). Returns 0. This is the second of two symmetric table callbacks. |
| `0x080bbde8` | `asm/15_equip_target_summon_zoom.s` | PLATE_ONLY | 999 | 401 | Selects and initializes field-spell equip placement for player r0, equip slot r1, and mode r2. It scores candidates, applies summon and card-pair restrictions, stores the selected target and card data in gP1LifePoints, calls init_equip_zone_rank_state_from_lp_context, and clears the field-state flag at 0x0201b160. Returns 1 on success, 0 when placement is unavailable, or -1 when no target is found. |
| `0x080bbf38` | `asm/15_equip_target_summon_zoom.s` | PLATE_ONLY | 1034 | 330 | Checks field-spell equip placement for player r0. It requires strict placement eligibility and positive LP, scans field entries, applies per-card occupancy, chain, pair, and handler rules, then stores the successful player context and calls init_equip_zone_rank_state_from_lp_context. Returns 1 after applying the context, else 0. |

18条全文全部 ASCII 且 `new_plate_chars <= 500`。`0x080a6508` 和 `0x080a6630` 的既有 ASCII PLATE 已合规，合同要求等值全文写入；其余16条替换旧全文。任何 PLATE 写入后再次读取全文核对长度、ASCII 和旧函数名残留。

`0x08069e40` 的旧 DB PLATE 含 CRLF，DB 原文长度2186字符且旧全文 SHA256 已冻结在 `plates.tsv`；当前 exporter 将行尾规范化为 LF 后为2163字符。该 CRLF-to-LF 变化仅属于明确的旧注释导出规范化，本提案最终仍以 `plates.tsv` 的393字符新全文重写该 PLATE。

## 7. carve 计划 (R7)

- carve ROM range: `[0x09e478b0,0x09e478bc)`, file offsets `[0x1e478b0,0x1e478bc)`, exact bytes `881200009b120000b8120000`。
- 原宿主 directive: `asm/rom.s:1530` 的 `.incbin "roms/2343.gba", 0x1e478b0, 0x245c`，覆盖 `[0x09e478b0,0x09e49d0c)`。
- 前 bookend: `valkyrion_material_cids` 位于 `[0x09e478a4,0x09e478b0)`，末字节地址 `0x09e478af`；其三个 words 保持不变。
- 后 bookend: `assert_pdst_null` 起于 `0x09e49d0c`；原 incbin 末地址精确等于该 label 起址。
- 替换结构：

```asm
valkyrion_target_material_cids:
    .word ALPHA_MAGNET_WARRIOR_CID
    .word BETA_MAGNET_WARRIOR_CID
    .word GAMMA_MAGNET_WARRIOR_CID
    .incbin "roms/2343.gba", 0x1e478bc, 0x2450
```

- 切割后结构化12B加尾 incbin 0x2450 合计仍为0x245c，末地址仍为 `0x09e49d0c`；不与相邻结构重叠。
- Ghidra：在 `0x09e478b0` 建 USER Global Label `valkyrion_target_material_cids`，在 b0/b4/b8 定义三个 `/undefined4:4`，从 `0x080a5a38` consumer literal 安装 DATA ref。原目标三地址均无 Symbol/Data/ref；新对象 ID允许由 Ghidra 分配。
- GAS values：三个 `.word` 分别为 `0x00001288`, `0x0000129b`, `0x000012b8`，与原 bytes逐项一致。

三项值是 `slot/icid` 卡牌标识，不是运行时 `set_code` 字段，也不是按整行首个相似十六进制文本匹配出的顺序 `cid`。结构化身份链如下：

| slot/icid word | cid evidence | card name evidence | logical CID evidence | password evidence |
|---|---|---|---|---|
| `0x1288` | `data/cards-ids-array.s:754` -> cid 598 | `data/card-stats.s:7789` -> Alpha The Magnet Warrior | `doc/um06-deck-modification-tool/data.md:591` | `data/card-passcodes.s:620` -> `99785935` |
| `0x129b` | `data/cards-ids-array.s:773` -> cid 617 | `data/card-stats.s:8036` -> Beta The Magnet Warrior | `doc/um06-deck-modification-tool/data.md:608` | `data/card-passcodes.s:639` -> `39256679` |
| `0x12b8` | `data/cards-ids-array.s:802` -> cid 640 | `data/card-stats.s:8335` -> Gamma The Magnet Warrior | `doc/um06-deck-modification-tool/data.md:628` | `data/card-passcodes.s:662` -> `11549357` |

`constants/card_info.inc:1152` 当前 `GAMMA_MAGNET_WARRIOR_CID` 注释中的 `pw=27175001` 与四条结构化证据不一致。Mode B 只把该注释改为 `pw=11549357`；名称、值 `0x000012b8`、行内其余文字及 `constants/card_info.inc` 其他字节保持不变。

## 8. disasm 与 §5.1

- disasm=0 range。主范围所有 bytes 已由1689 InstructionDB和203 DataDB连续覆盖。
- §5.1=0。主范围无函数间 ROM block；唯一范围外12B块有真实 raw ref，按 carve 处理。

## 9. constants / globals / aliases 与批准注释订正

| file | definition | value | consumers | status |
|---|---|---|---|---|
| `asm/rom.s` | `valkyrion_target_material_cids` | `0x09e478b0` | slot `0x080a5a38`; consumers `0x080a59aa,0x080a59ec` | NEW carve global |
| `constants/card_info.inc:1152` | `GAMMA_MAGNET_WARRIOR_CID` comment only | equate remains `0x000012b8` | structured identity chain in section 7 | `pw=27175001 -> pw=11549357`; no other byte change |

现有 constants 全库扫描已证明36个 EQ 槽复用 `constants/card_info.inc`, `constants/ewram.inc`, `constants/duel_field.inc`, `constants/demo_state.inc` 中的既有定义；其余8个 EQ 槽使用本节新建的3个 GAS Thumb aliases。精确定义位置在 `slots.tsv target_contract`。新增常量数为0，不新增同值常量。

在 `asm/rom.s` 新增7个 GAS Thumb aliases，全部为 `symbol + 1`，用于 packed function-pointer words：

| alias | value | source slots |
|---|---|---|
| `check_equip_sub_entry_slot_pair_eligible_1` | `0x080a5189` | `0x080a6434, 0x080a6474` |
| `check_moth_evolution_slot_requirement_1` | `0x080a533d` | `0x080a655c, 0x080a65d4` |
| `check_special_summon_slot_requirement_with_pair_exclusions_1` | `0x080a5715` | `0x080a668c, 0x080a66d4, 0x080a67c0, 0x080a6800` |
| `check_gate_guardian_material_slot_requirement_1` | `0x080a585d` | `0x080a6b84, 0x080a6be8` |
| `check_valkyrion_material_slot_requirement_1` | `0x080a5995` | `0x080a6d20, 0x080a6d88` |
| `check_masked_beast_des_gardius_material_slot_requirement_1` | `0x080a5bc9` | `0x080a6edc, 0x080a6f50` |
| `check_ancient_gear_castle_counter_slot_requirement_1` | `0x080a5da1` | `0x080a8b30, 0x080a8b70` |

## 10. packed Thumb source 闭包 (14 words)

| source | host | raw | source Symbol ID | source name | Data | incoming READ | action | target contract |
|---|---|---|---|---|---|---|---|---|
| `0x080a6b84` | `asm/13_equip_placement.s:20535` | `0x080a585d` | 4611686018562288516 | `DWORD_080a6b84` | /dword | 080a6b76:READ:DEFAULT | EQUATE check_gate_guardian_material_slot_requirement_1 | even target 0x080a585c; raw 0x080a585d; do not create odd label/ref/data |
| `0x080a6be8` | `asm/13_equip_placement.s:20583` | `0x080a585d` | 4611686018562288616 | `DWORD_080a6be8` | /dword | 080a6ba8:READ:DEFAULT | EQUATE check_gate_guardian_material_slot_requirement_1 | even target 0x080a585c; raw 0x080a585d; do not create odd label/ref/data |
| `0x080a6d20` | `asm/13_equip_placement.s:20750` | `0x080a5995` | 4611686018562288928 | `DWORD_080a6d20` | /dword | 080a6d12:READ:DEFAULT | EQUATE check_valkyrion_material_slot_requirement_1 | even target 0x080a5994; raw 0x080a5995; do not create odd label/ref/data |
| `0x080a6d88` | `asm/13_equip_placement.s:20800` | `0x080a5995` | 4611686018562289032 | `DWORD_080a6d88` | /dword | 080a6d48:READ:DEFAULT | EQUATE check_valkyrion_material_slot_requirement_1 | even target 0x080a5994; raw 0x080a5995; do not create odd label/ref/data |
| `0x080a6edc` | `asm/13_equip_placement.s:20991` | `0x080a5bc9` | 4611686018562289372 | `DWORD_080a6edc` | /dword | 080a6ecc:READ:DEFAULT | EQUATE check_masked_beast_des_gardius_material_slot_requirement_1 | even target 0x080a5bc8; raw 0x080a5bc9; do not create odd label/ref/data |
| `0x080a6f50` | `asm/13_equip_placement.s:21046` | `0x080a5bc9` | 4611686018562289488 | `DWORD_080a6f50` | /dword | 080a6f0e:READ:DEFAULT | EQUATE check_masked_beast_des_gardius_material_slot_requirement_1 | even target 0x080a5bc8; raw 0x080a5bc9; do not create odd label/ref/data |
| `0x080a712c` | `asm/13_equip_placement.s:21303` | `0x080a5d4d` | 4611686018562289964 | `DWORD_080a712c` | /dword | 080a711e:READ:DEFAULT | PRESERVE | even target 0x080a5d4c; raw 0x080a5d4d; do not create odd label/ref/data |
| `0x080a7174` | `asm/13_equip_placement.s:21339` | `0x080a5d4d` | 4611686018562290036 | `DWORD_080a7174` | /dword | 080a7138:READ:DEFAULT | PRESERVE | even target 0x080a5d4c; raw 0x080a5d4d; do not create odd label/ref/data |
| `0x080a7574` | `asm/13_equip_placement.s:21443 incbin [0x080a7234,0x080a763e)` | `0x080a5afd` | none | `none` | none | none:none:none | PRESERVE | even target 0x080a5afc; raw 0x080a5afd; do not create odd label/ref/data |
| `0x080a7594` | `asm/13_equip_placement.s:21443 incbin [0x080a7234,0x080a763e)` | `0x080a5afd` | none | `none` | none | none:none:none | PRESERVE | even target 0x080a5afc; raw 0x080a5afd; do not create odd label/ref/data |
| `0x080a7a1c` | `asm/14_equip_ai_scoring.s:40 incbin [0x080a792c,0x080a7ac0)` | `0x080a5cc9` | none | `none` | none | none:none:none | PRESERVE | even target 0x080a5cc8; raw 0x080a5cc9; do not create odd label/ref/data |
| `0x080a7a2c` | `asm/14_equip_ai_scoring.s:40 incbin [0x080a792c,0x080a7ac0)` | `0x080a5cc9` | none | `none` | none | none:none:none | PRESERVE | even target 0x080a5cc8; raw 0x080a5cc9; do not create odd label/ref/data |
| `0x080a8b30` | `asm/14_equip_ai_scoring.s:1876` | `0x080a5da1` | 4611686018562296624 | `DWORD_080a8b30` | /dword | 080a8b1c:READ:DEFAULT | EQUATE check_ancient_gear_castle_counter_slot_requirement_1 | even target 0x080a5da0; raw 0x080a5da1; do not create odd label/ref/data |
| `0x080a8b70` | `asm/14_equip_ai_scoring.s:1909` | `0x080a5da1` | 4611686018562296688 | `DWORD_080a8b70` | /dword | 080a8b34:READ:DEFAULT | EQUATE check_ancient_gear_castle_counter_slot_requirement_1 | even target 0x080a5da0; raw 0x080a5da1; do not create odd label/ref/data |

8个 EQUATE source 都保留 source Symbol ID/name/source、`/dword:4`、incoming DEFAULT READ、无 outgoing ref、无既有 equate、无 EOL；只在 source operand 0 加对应 alias equate，导出 `.word <new_name>_1`。

`0x080a712c/0x080a7174` 指向保留名 `check_equip_target_slot_eligible_by_display_code`，只冻结。`0x080a7574/0x080a7594` 和 `0x080a7a1c/0x080a7a2c` 位于后段 incbin，分别指向保留名 `0x080a5afc` 与 `0x080a5cc8`，不改其 block。所有14个 odd target 当前都无 Symbol/Data/ref；落地后仍保持该状态，even Function ID保持16729/16731等既有值。

## 11. direct CALL 与必要范围外文本投影

| CALL site | source | caller/host | target prestate | approved projection |
|---|---|---|---|---|
| `0x080a5f5c` | `asm/13_equip_placement.s:18957` | `0x080a5f38` | `0x080a5e28` ID4761 | call operand -> `init_equip_zone_rank_state_from_slot` |
| `0x08069f9e` | `asm/08_equip_oam_neodaed.s:13641` | `0x08069e40` ID4818 | `0x080a5f38` ID4762 | call operand + caller PLATE |
| `0x08095298` | `asm/12_equip_activation_scan.s:2350` | conceptual host `0x08095220` ID16933 | `0x080a5f38` ID4762 | call operand only |
| `0x080952a4` | `asm/12_equip_activation_scan.s:2356` | conceptual host `0x08095220` ID16933 | `0x080a5f38` ID4762 | call operand only |
| `0x08097086` | `asm/12_equip_activation_scan.s:6332` | `0x08097070` ID15783 | `0x080a5f38` ID4762 | call operand + caller PLATE |
| `0x080970b6` | `asm/12_equip_activation_scan.s:6365` | `0x080970a0` ID5719 | `0x080a5f38` ID4762 | call operand + caller PLATE |
| `0x080bbf02` | `asm/15_equip_target_summon_zoom.s:8680` | `0x080bbde8` ID7261 | `0x080a5f38` ID4762 | call operand + caller PLATE |
| `0x080bc116` | `asm/15_equip_target_summon_zoom.s:8955` | `0x080bbf38` ID7272 | `0x080a5f38` ID4762 | call operand + caller PLATE |

7个实际段外 caller/host 的严格白名单如下：

| entry | actual host module | Function ID/body SHA | approved text/source projection | PLATE |
|---|---|---|---|---|
| `0x08069e40` | `asm/08_equip_oam_neodaed.s` | 4818 / `dcb266a336ff1bcda4b07df9496ff512c3f727e80d26b956dbd639e1decb55b1` | `0x08069f9e` call target name | full rewrite, plates.tsv |
| `0x08095220` | `asm/12_equip_activation_scan.s` | 16933 / `725abc19cf3ecd19f1b4860b07bf8c27818d22940c5ccd9f85e357132b3d8499` | `0x08095298,0x080952a4` call target names | preserve exact 429-char plate |
| `0x08097070` | `asm/12_equip_activation_scan.s` | 15783 / `31db7dd4e19dd2fbeb8dc72ef40a7f8ff0499148259edbc5bc0516e422184c37` | `0x08097086` call target name | full rewrite, plates.tsv |
| `0x080970a0` | `asm/12_equip_activation_scan.s` | 5719 / `3c02b4b1413ebd913e3afaa940eeb79abacff87b3ca4ee9e5e73f5b74ce96eb2` | `0x080970b6` call target name | full rewrite, plates.tsv |
| `0x080bbde8` | `asm/15_equip_target_summon_zoom.s` | 7261 / `339464ca2a9631249a2522a5df43944535e21f7b076673e3c865c5e3cbd4d2bd` | `0x080bbf02` call target name | full rewrite, plates.tsv |
| `0x080bbf38` | `asm/15_equip_target_summon_zoom.s` | 7272 / `dee16a4cb4c11bc86c5d876ca951b38784b37e27779927f2151971b37bd09925` | `0x080bc116` call target name | full rewrite, plates.tsv |
| `0x080a89f8` | `asm/14_equip_ai_scoring.s` | 16755 / `7d14a535c7491766e1db23888fd4f59e310bb6be348f534aa78025d5f6eb3ba6` | packed sources `0x080a8b30,0x080a8b70` -> renamed alias equates | preserve exact 747-char plate |

另外4个 packed-source host Functions `0x080a6b38` ID16737, `0x080a6cc8` ID16739, `0x080a6e74` ID16740, `0x080a70d8` ID16744 只允许 source-word equate 投影；Function name/body/signature/PLATE 全部冻结。`0x080a6b38/6cc8/6e74/70d8/89f8/95220` 的 PLATE 不写。

外部 caller 的所有 Function 身份属性、body bytes、signature、incoming refs 和除批准 CALL/source word/PLATE 外的内容逐项守恒。`0x08095298/0x080952a4` 位于 computed-case 区，Ghidra `function_containing` 为 null；提案按 exporter 的概念宿主 `0x08095220` 冻结，不能创建新 Function。

## 12. Registry / CSV 同步合同

- `doc/dev/naming-proposals.csv` 仅更新6个地址的第2列 name；每行其余列逐字节保持：

| CSV line | address | old name | new name |
|---|---|---|---|
| 3286 | `0x080a585c` | `check_equip_sub_entry_slot_pair_with_field_scan` | `check_gate_guardian_material_slot_requirement` |
| 3287 | `0x080a5994` | `check_equip_target_slot_eligible_by_zone_scan` | `check_valkyrion_material_slot_requirement` |
| 3289 | `0x080a5bc8` | `check_equip_target_slot_eligible_by_activate_flag` | `check_masked_beast_des_gardius_material_slot_requirement` |
| 3292 | `0x080a5da0` | `check_equip_target_slot_eligible_by_bonus_eval` | `check_ancient_gear_castle_counter_slot_requirement` |
| 3293 | `0x080a5e28` | `init_equip_entry_sprite_fields` | `init_equip_zone_rank_state_from_slot` |
| 3294 | `0x080a5f38` | `apply_equip_entry_sprite_from_slot_context` | `init_equip_zone_rank_state_from_lp_context` |

- `tools/ghidra-labeling/RenameKnownFunctions.py` 现有 tuple：`0x080a5e28` line11911 与 `0x080a5f38` line11924 更新 name+plate；`0x080bbde8` line11933 与 `0x080bbf38` line12243 更新 plate-only；`0x080a6508/0x080a6630` lines13094-13095 保持 tuple 内容。
- 向 registry 增加当前缺失的12个 tuple：段内 `0x080a585c,5994,5afc,5bc8,5cc8,5d4c,5da0,5f7c,672c`，段外 `0x08069e40,0x08097070,0x080970a0`。name 和完整 PLATE 取 `plates.tsv`。
- registry 中 `0x080bbde8/0x080bbf38` name 不变。`0x080a6508/0x080a6630` 的既有 name/plate 不重复新增。
- CSV 中未改名的7个段内 row 与所有外部 caller row 保持原字节。运行 inventory/sync 后只允许上述6个 name-only diff。

## 13. 消费者证据 (R6)

| 语义 | 消费者证据 | 结论 | confidence |
|---|---|---|---|
| Gate Guardian material CID | `asm/13_equip_placement.s:17943-18031`; slots `0x080a5980`, state[8], sequential material scan | `SANGA_OF_THUNDER_CID + phase` identifies the three Gate Guardian materials | high |
| Valkyrion material table | `asm/13_equip_placement.s:18105@080a59aa`, `:18138@080a59ec`; slot `0x080a5a38`; section 7 four-source identity chains | indexes the external Alpha/Beta/Gamma slot/icid table by state[8]; these are not set_code values or row-text guesses | high |
| Des Gardius materials | `asm/13_equip_placement.s:18431-18561`; `0x080a5c48` Grand Tiki Elder and value+2 Melchid | phase-0 material predicate plus later duplicate/space gates | high |
| Ancient Gear Castle counters | `asm/13_equip_placement.s:18722-18787`; slots `0x080a5e04/08/0c/10` | Mask of Restrict exclusion, active Castle target, bonus/counter thresholds | high |
| zone-rank initializer | `asm/13_equip_placement.s:18794-18955`; writes `0x0201e4d0`; call at `0x080a5f5c` | initializes gEquipZoneRankState fields, not sprite object fields | high |
| LP-context initializer | `asm/13_equip_placement.s:18938-18967`; direct calls listed in section 11 | reads LP pending offsets, initializes zone-rank state, clears pending field | high |
| switch-table pointer | slot `0x080a5fac`, consumer `asm/13_equip_placement.s:18993@080a5f9c`; target ID5291 | existing ANALYSIS switch table base retained as REF target | high |
| gP1LifePoints pointers | 15 RENAME rows and 15 existing DATA refs in slots.tsv | pointer identity is established by existing refs and target ID15545 | high |

每个单独槽的消费者地址、精确 `file:line`、target contract 和 confidence 均在 `slots.tsv`；本节列出决定函数/全局语义的关键证据。

## 14. 可实施落地顺序与守恒合同

1. 不新增常量；`0x080a5f30/0x080a5f34` 复用 `constants/demo_state.inc` 的两个现有清位掩码。在 `asm/rom.s` 添加7个 Thumb aliases，并按 section 7 carve 外部12B表。先核对每个新 `.word` 的 ROM little-endian value。
2. Ghidra只对111个 automatic slots执行 `slots.tsv` 的 EQ/REF/RENAME/EOL；不触碰34个 switch words。对新 carve 建 global label/Data，并从 `0x080a5a38` 安装 DATA ref。
3. 对6个 Function 只改 name；对18个批准 Function 写完整 ASCII PLATE。Function ID、body、signature 和其他属性保持 `plates.tsv` 前态。
4. 对8个批准 packed source word只加 operand-0 equate；其余6个 packed source word和全部14个 odd targets冻结。
5. 重导 asm 后只接受 section 11 白名单模块的名称/PLATE/source-word 投影：`asm/08_equip_oam_neodaed.s`, `asm/12_equip_activation_scan.s`, `asm/13_equip_placement.s`, `asm/14_equip_ai_scoring.s`, `asm/15_equip_target_summon_zoom.s`。不允许借此解释或改写 Seg-10 新语义。
6. 同步 registry 与 CSV，CSV只允许6个 name-only row diff；registry 按 section 12 精确增改。另只允许 `constants/card_info.inc:1152` 的 Gamma 密码注释 `27175001 -> 11549357`，equate 名称/值和该文件其他字节保持 source baseline。
7. 重新查询111槽、34 switch words、18批准 Function、6个冻结外 Function、14 packed source/odd target、8 CALL sites和 carve target，逐字段比较前态合同。
8. 运行 inject/split/build 与 byte-identical 检查；ROM SHA/逐字节必须与 `roms/2343.gba` 一致。任何字节差异都终止落地并回滚 Ghidra `.rep`。

写入范围白名单：`asm/rom.s`, `constants/card_info.inc:1152` 的单处 comment-only 密码订正, 上述5个 asm 模块, `tools/ghidra-labeling/RenameKnownFunctions.py`, `doc/dev/naming-proposals.csv`, 本段 proposal/review/slots/plates 与按流程更新的活动进度文档。`constants/duel_field.inc` 不再允许写入；其他 source/constants/registry 内容保持 source baseline。

## 15. 自检结果

- 111槽地址与原自动名集合精确覆盖 baseline；`EQ=44, REF=52, RENAME=15`，无重复 final label。
- 两个 mask 槽复用 `DEMO_CLEAR_BITS_8_1/16_9`，新增常量=0；15个 RENAME 精确为14个 `/pointer:4`+DEFAULT DATA ref与一个 `0x080a6874 /dword:4`+USER_DEFINED DATA ref。
- 111个 `original_value` 逐项等于 ROM little-endian word；145 words 的源码表达式与 ELF 值一致。
- 18条 PLATE 与111条 EOL 全部 ASCII；PLATE 最大437字符。
- 34个既有 switch word 的 value/Data/ref/target 已逐项冻结。
- carve 三个 `.word` 值与原12B一致，尾 incbin 起止和两个 bookend 精确闭合。
- 三个 carve word 的 `slot/icid -> cid -> card name -> password` 四源证据闭合；Gamma 正确密码为 `11549357`，Mode B 的常量文件变更限定为单处注释。
- 14个 packed word 中8个 action、6个 preserve；所有 raw value 都等于 `(even Function entry)|1`。
- ref-scan 复核：外表 raw=1/thumb=0；主范围无数据 block；唯一 slot-address THUMB hit 已用资产原文件和 offset 证明为偶合。
- 求助: none。

## Executor Report: F13-Seg-9

- 槽: EQ=44 REF=52 RENAME=15 FUNC_RENAME=6 PLATE=18
- existing words: PRESERVE=34
- carve=1 disasm=0 range §5.1=0
- 新增 constants=0；新增 globals/aliases: `valkyrion_target_material_cids`, 7 Thumb aliases；comment-only: `GAMMA_MAGNET_WARRIOR_CID pw=27175001 -> 11549357`
- 求助: none
- proposal: `doc/dev/refine/F13-Seg-9.proposal.md`
