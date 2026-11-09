# Refine Proposal: F14-Seg-4  [0x080aba78..0x080acc30)

## 范围与冻结输入

- 正式段范围: `asm/14_equip_ai_scoring.s [0x080aba78,0x080acc30)`, 4536 bytes.
- 当前权威全模块前态: `root-f14-seg3-independent-post.json`, 即 Seg-3 落地后的 190 Functions / 1271 words / 55916 byte units 状态.
- 段初始前态: `root-f14-seg4-initial-baseline.json`, 19 Functions, 131 current words, 0 raw blocks, 4536 byte units.
- 机械布局前态: `root-f14-seg4-initial-layout.json`, PASS. 1873 InstructionDB, 3922 code bytes, 131 words / 524 bytes, 90 padding bytes, 总计 4536 bytes, 无空洞或重叠.
- 补充只读前态: `root-f14-seg4-supplement-prestate.json`, SHA256 `cdee816b71639cb1de7fba72c341d691d69008276072ee9d563a410a7607cd62`. 其 DB gate SHA256 `48d656bef5e2bc5962c1ccb88f9e0bf1122e3e9bbc14c7b2b6762a9afd77aaad`, 15 个物理 DB 文件查询前后完全相同.
- 源码和 DB 备份: `root-source-baseline-f14seg4.json`, `root-f14-seg4-db-backup.json`.
- 完整槽合同: `F14-Seg-4.slots.tsv`, 131 rows. Function / PLATE 合同: `F14-Seg-4.plates.tsv`, 21 rows.
- 本段无 R4, carve 或 Section 5.1 数据块. 所有 InstructionDB 地址, 原始 bytes, Function body ranges 和 padding 均保持.

## 段测绘

### Function 入口

| entry | current | final | action |
|---|---|---|---|
| `0x080aba78` | `reset_equip_entry_phase_to_zero` | `return_zero_from_equip_entry_dispatch` | rename + PLATE rewrite |
| `0x080aba7a` | `exit_equip_subentry_epilogue` | same | PLATE rewrite |
| `0x080aba8c` | `init_equip_sub_entry_state_with_sprite_submit` | same | PLATE rewrite |
| `0x080abb90` | `reset_sprite_attr_record_flags` | same | PLATE rewrite |
| `0x080abbd8` | `init_equip_slot_entry_with_copy_flag_sprite` | same | PLATE rewrite |
| `0x080abcac` | `init_equip_sub_entry_fields_from_slot` | same | PLATE rewrite |
| `0x080abd60` | `setup_equip_oam_entry_with_sprite_attr` | same | PLATE rewrite |
| `0x080abe40` | `invoke_setup_equip_oam_with_attr2` | same | PLATE rewrite |
| `0x080abe54` | `init_equip_slot_entry_with_placement_type_check` | same | PLATE rewrite |
| `0x080abf14` | `eval_zone_slot_score_for_player_with_activation_guard` | same | PLATE rewrite |
| `0x080abf64` | `eval_zone_slot_score_for_player` | same | PLATE rewrite |
| `0x080ac004` | `dispatch_zone_slot_score_by_player_flag` | same | PLATE rewrite |
| `0x080ac028` | `find_best_activatable_slot_score_for_player` | same | PLATE rewrite |
| `0x080ac0bc` | `eval_player_activation_score_and_lp_threshold` | same | PLATE rewrite |
| `0x080ac21c` | `check_equip_card_valid_for_target_slot` | same | PLATE rewrite |
| `0x080ac4e8` | `check_card_normal_summon_restricted` | same | PLATE rewrite |
| `0x080ac540` | `eval_card_activation_score_with_lp_threshold` | same | PLATE rewrite |
| `0x080ac584` | `check_card_activation_eligible_by_id` | same | PLATE rewrite |
| `0x080acbf0` | `check_player_lp_exceeds_toon_world_cost` | `check_player_lp_exceeds_chain_energy_cost` | rename + PLATE rewrite |

`F14-Seg-4.plates.tsv` 冻结 19 个段内 Function 的 Function ID, source, namespace, body, body SHA256, signature, parameters, return, flags, EOL 和 incoming refs. 19 个 body 全部保持, 不创建 Function, 不删除 Function, 不改 shared epilogue owner. `return_zero_from_equip_entry_dispatch@0x080aba78` 的 2-byte body 与相邻 `exit_equip_subentry_epilogue@0x080aba7a` 分别保持原 Function 身份; ABA78 仅改 Function name 和唯一 incoming ref 的 derived target-primary name.

### word 与 raw 块

- 131 current words 全部是 4-byte Data, 全部带自动 source label, 全部进入 `F14-Seg-4.slots.tsv`.
- 131 个 word 的地址, bytes, little-endian value, Data type, source symbols, primary Symbol, `refs_from`, `refs_to`, equates, EOL 和 owner 均逐行冻结.
- 当前 136 条 PC `READ refs_to` 与 source DATA `refs_from` 分开记录. 不把 PC read 当作 source DATA ref.
- 段内无 `ROM_INCBIN` 或 `.byte` raw block. 不产生 R4 新 pool, switch case, carve 或 Section 5.1 项.

## 数据块分类, Rule 2/3

本段 raw block 数为 0. `root-f14-seg4-initial-layout.json` 已证明 4536 bytes 完整由 1873 InstructionDB, 131 个 4-byte Data words 和 90 padding bytes覆盖. 因此无 ref-scan block row, carve row, disasm row 或 Section 5.1 row.

## 符号化计划, R1/R2/R3

### 完整 slots 合同

`F14-Seg-4.slots.tsv` 是地址级落地真源. 131 rows 地址唯一且与 baseline 的 131 current word 集合完全相同. 每行包含完整 before state, action, constant 或 target, target prestate, final source label, GAS expression, ASCII EOL, consumer evidence, confidence, after refs 和 after equates.

| action | count | contract |
|---|---:|---|
| `EQ_ADD` | 104 | 保持 4-byte Data 和全部 PC `READ refs_to`, 将 source 自动 label 物化为 TSV 的 USER label, 在 PC literal operand 上绑定 TSV 的 equate |
| `REF_ADD` | 20 | 保持 4-byte Data 和全部 PC `READ refs_to`, 将 source 自动 label 物化为 USER label, 新建一条 operand-0 DATA ref 到现有静态 USER RAM target |
| `REF_PRESERVE` | 7 | `gP1LifePoints` 的 7 条既有 DATA refs 保持 CORE6 和 target Symbol ID, 只将 source 自动 label 物化为 TSV 的 USER label |

本段无纯 `RENAME_SLOTS`. 131 个 source 自动 labels 均由 EQ 或 REF action 同步物化为唯一 snake-case USER label. DEFAULT 动态 source Symbol ID 可随批准物化变化, 不在同址保留自动 alias. 静态 USER target Symbol ID, name, type, source 和 namespace 必须保持.

### REF_SLOTS

| target | final source refs | new | preserve | target Symbol ID |
|---|---:|---:|---:|---:|
| `gEquipZoneRankState` | 7 | 7 | 0 | 33146 |
| `gDuelFieldSlots` | 10 | 10 | 0 | 20369 |
| `gDuelCardCtxBase` | 1 | 1 | 0 | 18879 |
| `gSpriteAttrBuf` | 1 | 1 | 0 | 21747 |
| `gP1LifePoints` | 7 | 0 | 7 | 15545 |
| `gEquipLpScoreBase` | 1 | 1 | 0 | 30393 |

对 7 条 `REF_PRESERVE`, before 和 after ref 均为 TSV 冻结的 `DATA/USER_DEFINED/primary` CORE6. 对 20 条 `REF_ADD`, after ref 精确采用同一 ref contract. RAM target bytes 保持 `null`, 不读取未初始化 EWRAM bytes. 本段没有 ROM Function even pointer, odd Thumb callback 或 target alias, 因此不新增 Function-value equate, odd-address Label, odd-address Data 或 `fn+1` 投影.

### EQ_SLOTS

- 104 个 EQ rows 使用 72 个唯一 equate names.
- 85 rows 复用现有 constants, 具体 include 和表达式见 TSV `const_status`, `const_or_target`, `gas_expression`.
- 19 rows 使用 15 个批准的新 constants. 同值多消费者复用同一新 constant.
- 既有 7 个 global Equates 不删除. 每个 source operand 的 before 和 after equate list 以 TSV 为唯一合同.
- `0x080ac608` 的 `0x1cf4` 使用 `P2LP_BLOCK2_OFF_1CF4`, 因为消费者基址是 `gP1LifePoints`; 不使用以 `gDuelFieldSlots` 为基址的 field-state offset 名.
- `0x1813` 复用 `NEO_SPACE_SPAWN_CAT_1813`.

### RENAME_SLOTS

None.

## FUNC_RENAME

| entry | current | final | indeg | evidence | confidence |
|---|---|---|---:|---|---|
| `0x080aba78` | `reset_equip_entry_phase_to_zero` | `return_zero_from_equip_entry_dispatch` | 1 direct BL | 2-byte body only sets `r0=0`; falls through to the shared epilogue; upper caller treats zero as continue; no phase or entry store | high |
| `0x080acbf0` | `check_player_lp_exceeds_toon_world_cost` | `check_player_lp_exceeds_chain_energy_cost` | 3 direct BL | body loads CID `0x132c`, counts that card, computes `count * 500`, and returns whether selected player LP exceeds the cost | high |

`0x080aba78` 的唯一 incoming 是 `dispatch_equip_entry_slot_by_mode` 在 `0x080ab240` 的 `UNCONDITIONAL_CALL/DEFAULT/primary` ref. 条件为 `gEquipZoneRankState` byte `+0x12` bit4 clear. 该 2-byte Function 仅执行 `movs r0,#0`, 随后 fall through 到 `exit_equip_subentry_epilogue`, 由后者恢复 dispatcher frame 并直接返回 `tick_equip_activation_main_sequence`; 上层将 0 作为 continue status. Rename 后 Function ID16959、source/type/namespace、body、signature/flags/params/return 和 incoming CORE6 保持, 仅 Function name 与 derived target-primary name更新. Full-ROM unaligned scan 对 `0x080aba78`, `0x080aba79`, `0x080aba7a`, `0x080aba7b` 均为0命中, 因此不增加 pointer projection、odd alias 或 source Equate.

结构化 card evidence:

- `data/cards-ids-array.s:918` 将 logical CID slot `0x132c` 对应到 Chain Energy.
- `data/card-stats.s:9414` 的结构化 record 是 Chain Energy, passcode 79323590.
- `CHAIN_ENERGY_CID=0x132c` 已存在, `0x080acc24` 直接复用该 constant.
- `asm/14_equip_ai_scoring.s:11203-11224` 的 Function body 读取 `0x132c`, 累加该卡的持有数, 乘以 500, 并与 `gP1LifePoints + (player & 1) * 0x868` 的 LP 比较.

实际 direct callers 固定为:

| call address | host Function | source |
|---|---|---|
| `0x080bc1e4` | `dispatch_equip_activation_by_field_state@0x080bc168` | `asm/15_equip_target_summon_zoom.s:9063` |
| `0x080bc2fa` | `dispatch_equip_activation_by_field_state@0x080bc168` | `asm/15_equip_target_summon_zoom.s:9203` |
| `0x080bc39e` | `try_execute_toon_world_equip_placement@0x080bc388` | `asm/15_equip_target_summon_zoom.s:9289` |

`root-f14-seg4-supplement-prestate.json` 证明三条 call refs 均为 `UNCONDITIONAL_CALL/DEFAULT/primary`, target 是 Function ID 5587. Rename 后 ref 对象与 Function ID 保持, 仅 derived target primary name 更新. Full-ROM unaligned raw/even 和 THUMB|1 scan 对 `0x080acbf0` 的命中均为 0, 见 `f14-seg4-function-pointer-scan.json`. 因此无 ROM pointer table, odd callback, `_1` alias, source equate 或 `rom.s` projection.

## PLATE, R5

完整 old PLATE JSON, old chars, old ASCII flag, old SHA256, action 和 full `new_plate` 全文在 `F14-Seg-4.plates.tsv`. 所有实际写入的新 PLATE 均为单行 ASCII, 最大 458 chars, 每条不超过 500 chars.

| entry | action | old chars | new chars | scope |
|---|---|---:|---:|---|
| `0x080aba78` | `RENAME_PLATE` | 602 | 406 | segment |
| `0x080aba7a` | `PLATE_REWRITE` | 548 | 324 | segment |
| `0x080aba8c` | `PLATE_REWRITE` | 919 | 321 | segment |
| `0x080abb90` | `PLATE_REWRITE` | 662 | 211 | segment |
| `0x080abbd8` | `PLATE_REWRITE` | 1316 | 351 | segment |
| `0x080abcac` | `PLATE_REWRITE` | 623 | 315 | segment |
| `0x080abd60` | `PLATE_REWRITE` | 1553 | 357 | segment |
| `0x080abe40` | `PLATE_REWRITE` | 464 | 291 | segment |
| `0x080abe54` | `PLATE_REWRITE` | 1366 | 352 | segment |
| `0x080abf14` | `PLATE_REWRITE` | 698 | 280 | segment |
| `0x080abf64` | `PLATE_REWRITE` | 981 | 325 | segment |
| `0x080ac004` | `PLATE_REWRITE` | 386 | 308 | segment |
| `0x080ac028` | `PLATE_REWRITE` | 660 | 306 | segment |
| `0x080ac0bc` | `PLATE_REWRITE` | 777 | 330 | segment |
| `0x080ac21c` | `PLATE_REWRITE` | 1189 | 303 | segment |
| `0x080ac4e8` | `PLATE_REWRITE` | 311 | 304 | segment |
| `0x080ac540` | `PLATE_REWRITE` | 839 | 347 | segment |
| `0x080ac584` | `PLATE_REWRITE` | 522 | 342 | segment |
| `0x080acbf0` | `RENAME_PLATE` | 450 | 274 | segment |
| `0x080bc168` | `EXTERNAL_PLATE_PROJECTION` | 1116 | 458 | `asm/15_equip_target_summon_zoom.s` |
| `0x080bc388` | `EXTERNAL_PLATE_PROJECTION` | 891 | 409 | `asm/15_equip_target_summon_zoom.s` |

21 rows 全部进行 full PLATE rewrite. `0x080aba78` 的新全文只陈述 return-zero dispatch exit, 不保留无依据的 phase-store 语义. `0x080aba7a` 的新全文按 ROM/typed InstructionDB 写明 `r8<-r3`, `r9<-r4`, `r10<-r5`; Function ID16960、16-byte body、接口、incoming `0x080ab272` 和 EOL/refs保持. 其余 Function name, ID, body, signature, flags, EOL 和 refs保持, 仅 `0x080aba78` 与 `0x080acbf0` 同步批准的 rename. `0x080abb90` 的 byte `+0x14` mask 由 `movs r0,#2; rsbs r0,r0,#0` 形成 `0xfffffffe`, 因而清 bit0. `0x080abe40` 的 57 个 incoming CALLs 进入普通 BL wrapper: r0-r2 原样, entry r3 作为 stack 第五参数, callee r3=2, void 和副作用来自 callee. `0x080ac21c` 仅接收 `r0=player_side, r1=slot_index`, entry r2 在使用前被覆盖, 并只读 low 19-bit CID 后分派 card-specific predicates. `0x080bc168` 无静态 incoming caller 证据; stored-advance 路径写 next state 后返回 0, no-store completion 路径返回 0, states 2/3 的 nonzero sub-call result 会 reset state=0 并返回 0, default/reject 返回 1. `0x080bc388` 仅在 initial state 0 的 gate/no-slot/nonzero-placement 分支 advance 后返回 0; entry state nonzero 直接返回 1, zero placement 成功返回 0 且不 advance.

## carve 计划, R7

None.

## disasm 计划, R4

None. 保持 `root-f14-seg4-initial-layout.json` 的 1873 个 InstructionDB 地址和 raw bytes, 其中 1734 条 native mnemonic 和 139 条 `.hword` InstructionDB. 139 条 `.hword` 不转成 Data. 保持 3922 code bytes, 524 Data bytes, 90 padding bytes和全部 Function body ranges.

## 新增 constants / 全局

### `constants/card_info.inc`

| name | value | evidence |
|---|---:|---|
| `DREAM_CLOWN_CID` | `0x101e` | structured logical CID and `check_card_activation_eligible_by_id` compare |
| `CANNON_SOLDIER_CID` | `0x11a6` | structured logical CID and same consumer |
| `THOUSAND_EYES_RESTRICT_CID` | `0x1284` | structured logical CID and same consumer |
| `GRAVITY_BIND_CID` | `0x140e` | structured logical CID and same consumer |
| `GORA_TURTLE_CID` | `0x1523` | structured logical CID and same consumer |
| `TRICKY_TOKEN_CID` | `0x180d` | cards-ids slot maps to cid2093; card name/passcode/image/stat identify Tricky Token; consumer compares card ID |
| `PROTO_CYBER_DRAGON_CID` | `0x19bc` | structured logical CID and same consumer |

`0x180d` 已有 OAM-domain name `NEO_DAEDALUS_OAM_SPRITE_BASE`; 本段消费者比较提取后的 card ID. `data/cards-ids-array.s:2167` 映射到 cid2093, `data/card-names.s:28718,28722` 命名 Tricky Token, `data/card-passcodes.s:2115` 标记 token/no passcode, `data/card-image-index.s:2112` 标记 Token13, `data/card-stats.s:27224` 冻结同一 slot. 因此新增 `TRICKY_TOKEN_CID`, 不复用 sprite-domain name.

### `constants/duel_field.inc`

| name | value | evidence |
|---|---:|---|
| `EQUIP_STATE_CLEAR_BITS_8_6_MASK` | `0xfffffe3f` | four 16-bit consumers clear selector bits 8:6, then set mode 1/2/3/4 with `0x40/0x80/0xc0/0x100` |
| `EQUIP_SLOT_SCORE_FIELD5_HIGH` | `0x834` | score evaluator field-5 high return value |
| `EQUIP_SCORE_THRESHOLD_1500` | `0x5dc` | equip score comparisons at `0x080ac154` and `0x080ac1e8` |
| `EQUIP_SCORE_THRESHOLD_999` | `0x3e7` | equip score comparison at `0x080ac15c` |
| `EQUIP_SCORE_THRESHOLD_1699` | `0x6a3` | equip score comparison at `0x080ac1d4` |
| `EQUIP_ACTIVATION_LP_THRESHOLD_3999` | `0xf9f` | LP threshold consumer at `0x080aca82` |
| `EQUIP_ACTIVATION_SCORE_RANGE_NEG_1101` | `0xfffffbb3` | signed score-range lower normalization at `0x080acab6` |
| `EQUIP_ACTIVATION_SCORE_RANGE_WIDTH_798` | `0x31e` | unsigned score-range width at `0x080acaba` |

`0x5dc` 和 `0x3e7` 的现有 names 属于 LP 或 stat domain. 当前消费者比较 equip activation score, 因此新增 score-domain aliases. 15 个新 names 在现有 constants 中无同语义可复用项. 其余 57 个唯一 equate names 全部复用现有 constants.

`EQUIP_STATE_CLEAR_BITS_8_6_MASK=0xfffffe3f` 的低16位反掩码为 `0x01c0`, 精确清除 halfword bits `[8:6]`. 四个消费者均对 `gEquipZoneRankState+0x12` 执行 `ldrh -> AND mask -> OR 0x40/0x80/0xc0/0x100 -> strh`, 分别写 selector 1/2/3/4; reader `dispatch_equip_entry_slot_by_mode` 以 `lsls #0x17; lsrs #0x1d` 读取相同 bits `[8:6]`. 不复用位域不同的 `EQUIP_STATE_CLEAR_BITS_8_1_MASK` 或 `EQUIP_STATE_CLEAR_BITS_16_9_MASK`.

不新增 RAM global. 六个 RAM targets 均为现有静态 USER symbols.

## Section 5.1 登记, Rule 3

None.

## 消费者证据, R6

完整 131-slot consumer map 在 `f14-seg4-consumer-evidence.json`, 共 136 条 PC `READ refs_to`. 下表列关键跨域证据, 其余逐槽 file:line, instruction, owner 和 confidence 在该 JSON 与 slots TSV 中冻结.

| slot | value / target | consumer | evidence | confidence |
|---|---|---|---|---|
| `0x080abb74` | `gEquipZoneRankState` | `init_equip_sub_entry_state_with_sprite_submit` | `asm/14_equip_ai_scoring.s:8781,8849,8867` | high |
| `0x080abb80` | `gDuelFieldSlots` | same | `asm/14_equip_ai_scoring.s:8815` | high |
| `0x080abb88` | `gDuelCardCtxBase` | same | `asm/14_equip_ai_scoring.s:8866` | high |
| `0x080abb8c` | `gSpriteAttrBuf` | same | `asm/14_equip_ai_scoring.s:8886` | high |
| `0x080abfec` | `EQUIP_SLOT_SCORE_FIELD5_HIGH` | `eval_zone_slot_score_for_player` | `asm/14_equip_ai_scoring.s:9490` | high |
| `0x080ac018` | `gEquipLpScoreBase` | `dispatch_zone_slot_score_by_player_flag` | `asm/14_equip_ai_scoring.s:9520` | high |
| `0x080ac1c4` | `EQUIP_SCORE_THRESHOLD_1500` | `eval_player_activation_score_and_lp_threshold` | `asm/14_equip_ai_scoring.s:9687` | high |
| `0x080ac30c` | `TRICKY_TOKEN_CID` | `check_equip_card_valid_for_target_slot` | `asm/14_equip_ai_scoring.s:9921`; low 19-bit CID compare; cid2093=Tricky Token evidence above | high |
| `0x080ac624` | `DREAM_CLOWN_CID` | `check_card_activation_eligible_by_id` | `asm/14_equip_ai_scoring.s:10362` | high |
| `0x080aca94` | `EQUIP_ACTIVATION_LP_THRESHOLD_3999` | same | `asm/14_equip_ai_scoring.s:11015` | high |
| `0x080acac4` | `EQUIP_ACTIVATION_SCORE_RANGE_NEG_1101` | same | `asm/14_equip_ai_scoring.s:11044` | high |
| `0x080acc24` | `CHAIN_ENERGY_CID` | renamed Function | `asm/14_equip_ai_scoring.s:11206` | high |
| `0x080acc28` | `gP1LifePoints` | renamed Function | `asm/14_equip_ai_scoring.s:11214` | high |

## Source, registry, CSV 和 inventory 投影合同

### 正式 source scope

- `asm/14_equip_ai_scoring.s`: 131 source word expressions / labels / EOL 投影, 19 段内 PLATE writes, 2 Function label renames. 另将 `0x080ab240` 的 BL name投影到 `return_zero_from_equip_entry_dispatch`; Instruction bytes和 body布局保持.
- `asm/15_equip_target_summon_zoom.s`: 仅 `0x080bc1e4`, `0x080bc2fa`, `0x080bc39e` 三条 BL 的 target name projection, 加 `0x080bc168` 和 `0x080bc388` 两条 full PLATE projection. 不改其他 source bytes, labels 或 Function names.
- `constants/card_info.inc`: 新增 7 个 CID constants.
- `constants/duel_field.inc`: 新增 8 个 duel/equip constants.

### `RenameKnownFunctions.py`

- 已有 tuples 的 PLATE-only update: `080aba8c`, `080abb90`, `080abcac`, `080abf14`, `080abf64`, `080ac004`, `080ac028`, `080ac0bc`, `080ac4e8`, `080ac584`, `080bc168`, `080bc388`.
- 缺失 tuple 且有批准 PLATE write: 为 `080aba78`, `080aba7a`, `080abbd8`, `080abd60`, `080abe40`, `080abe54`, `080ac21c`, `080ac540` 新增 tuple; `080aba78` 使用批准的最终名, 其余 Function name保持.
- `080acbf0`: 更新已有 tuple 的 name 和 full plate.

### CSV 和 inventories

- `doc/dev/naming-proposals.csv`: `0x080aba78` 与 `0x080acbf0` 两个现有 row 各仅改 name field, 总行数保持5079.
- 刷新 canonical temp inventories: `temp/ghidra-functions.csv`, `temp/ghidra-functions-renamed.txt`, `temp/ghidra-functions-auto.txt`, `temp/ghidra-functions-summary.md`.
- 总 Function 数 5214, named 5124, auto 90 保持. CSV 和 renamed inventory 中只有 `0x080aba78` 与 `0x080acbf0` 两行的 name text变化; body lengths、auto 和 summary counts保持.
- `tools/ghidra-labeling/ghidra-functions.*` 是已登记 stale copies, 保持不动.
- `f14-seg4-name-reference-baseline.json` 冻结两个旧名的活动命中: ABA78 的 asm14 definition、AB240 BL、CSV 与 canonical temp 两份name inventory, 以及 ACBF0 的12个批准 projection occurrences. ABA78/79 与 ABA7A/7B 的ROM raw/even/THUMB|1 pointer命中均为0. 历史 proposal / review / eval 文档不回写.

## 落地顺序与后态门禁

1. 校验 fresh source / DB baseline 与本提案冻结输入一致.
2. 新增 15 个 constants, 不改变任何现有 constant value.
3. 对 131 slots 按 TSV 物化 source USER labels, 执行 104 EQ actions和27 REF actions. 先保持 existing refs, 再补 20 refs; 禁止同址 alias.
4. Rename Function ID16959到 `return_zero_from_equip_entry_dispatch`, Function ID5587到 `check_player_lp_exceeds_chain_energy_cost`; 两者的 source, namespace, body, signature和incoming ref对象保持, 仅 derived target-primary names同步.
5. 对 plates TSV 的21 rows全部调用PLATE写入; 所有新PLATE以full text写入.
6. 更新 registry, CSV 和 canonical inventories, 再重新导出 module 14 和必要 module 15 projection.
7. 校验 1873 InstructionDB地址和raw bytes不变, 131 Data words值不变, 90 padding bytes不变, 19段内Function body / ID / signature不变.
8. 校验 131 slots 全覆盖, 104 after equates, 27 after source DATA refs, 136 PC READ refs_to; 静态 target Symbol IDs按本提案保持.
9. 校验两个旧 Function names只在明确排除的 stale inventories和历史文档存在, 批准source / registry / CSV / canonical inventory范围内为0.
10. 执行 exporter, split, build和byte-identical门禁. ROM bytes必须与原ROM完全一致.

## 求助

None.

## Executor Report: F14-Seg-4

- 槽: EQ=104, REF=27 (`REF_ADD=20`, `REF_PRESERVE=7`), RENAME=0, FUNC_RENAME=2, PLATE writes=21.
- Function/PLATE rows=21 (`PLATE_REWRITE=17`, `RENAME_PLATE=2`, `EXTERNAL_PLATE_PROJECTION=2`, `PRESERVE=0`). Registry: missing-tuple ADD=8, existing PLATE-only UPDATE=12, rename+PLATE UPDATE=1, preserve-missing=0.
- carve=0, disasm=0 ranges, Section 5.1=0.
- 新增 constants: `card_info.inc` 7, `duel_field.inc` 8. 新增 globals: none.
- 求助: none.
- proposal: `doc/dev/refine/F14-Seg-4.proposal.md`.
