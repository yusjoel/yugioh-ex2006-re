# Refine Proposal: F14-Seg-9 [0x080b153c..0x080b40b8)

## 段测绘

- 模块: `asm/14_equip_ai_scoring.s`, 11132 bytes.
- 当前 typed layout: 433 个 InstructionDB 共 904 bytes, 6 个 4-byte words 共 24 bytes, 4 bytes padding, 以及 `[0x080b18e0,0x080b40b8)` 10200-byte `ROM_INCBIN`.
- 现有 Function 仅 `select_equip_placement_slot_with_score@0x080b153c`, ID7259, body 904 bytes, body SHA256 `9d9f310822a84a380c5297b2837383bfe8efc66f5518e80dd6e32e555770b017`. 名称、body、signature、incoming、PLATE 全部保持.
- 6 个 current words 与 R4 产生的 231 个 literal words 共 237 槽. `F14-Seg-9.slots.tsv` 完整冻结 source bytes/Data/Symbol/refs_from/refs_to/Equates/EOL/owner 与 after contract.
- raw 分类后新增 59 个段内 Function. 每个 canonical AddressSet、body size/SHA、全部 instruction starts、flows、PC reads、incoming table rows 在 `f14-seg9-function-projection-plan.json`.
- 59个callback body的真实entry参数、结果形态和指令证据冻结在`f14-seg9-callback-semantic-evidence-matrix-draft.md`. 55条原通用PLATE均改为body-specific; B1E04保留raw count, B207C保留raw callee result, B2D38保留conditional raw value, B2EEC保留conditional raw u16 field value. B4B52/B4B54只以r0非零判accepted.

| entry | final name | body bytes | instructions |
|---|---|---:|---:|
| `0x080b18e0` | `check_mask_of_restrict_summon_response_eligible` | 24 | 12 |
| `0x080b1900` | `check_gate_guardian_component_summon_response_eligible` | 50 | 25 |
| `0x080b193c` | `check_injection_fairy_lily_summon_response_eligible` | 78 | 39 |
| `0x080b1998` | `check_kuriboh_summon_response_eligible` | 40 | 20 |
| `0x080b19d0` | `check_collected_power_summon_response_eligible` | 156 | 76 |
| `0x080b1a74` | `check_time_machine_summon_response_eligible` | 152 | 73 |
| `0x080b1b24` | `check_rope_of_life_summon_response_eligible` | 186 | 87 |
| `0x080b1bf4` | `check_skill_drain_summon_response_eligible` | 64 | 30 |
| `0x080b1c3c` | `check_magical_dimension_summon_response_eligible` | 66 | 30 |
| `0x080b1c80` | `check_opponent_distinct_field7_pair_summon_response_eligible` | 152 | 73 |
| `0x080b1d24` | `check_sebeks_blessing_summon_response_eligible` | 66 | 32 |
| `0x080b1d74` | `check_regulation_of_tribe_summon_response_eligible` | 82 | 39 |
| `0x080b1dd4` | `check_blind_destruction_summon_response_eligible` | 46 | 21 |
| `0x080b1e04` | `check_graverobbers_retribution_summon_response_eligible` | 20 | 9 |
| `0x080b1e18` | `check_mystical_space_typhoon_summon_response_eligible` | 88 | 43 |
| `0x080b1e80` | `check_dust_tornado_mind_haxorz_summon_response_eligible` | 98 | 49 |
| `0x080b1ef0` | `check_ring_of_destruction_summon_response_eligible` | 186 | 91 |
| `0x080b1fb8` | `check_battle_scarred_summon_response_eligible` | 22 | 10 |
| `0x080b1fd4` | `check_destruction_ring_summon_response_eligible` | 74 | 36 |
| `0x080b2028` | `check_just_desserts_summon_response_eligible` | 76 | 36 |
| `0x080b207c` | `check_gift_of_mystical_elf_summon_response_eligible` | 56 | 25 |
| `0x080b20b4` | `check_eye_of_truth_summon_response_eligible` | 20 | 10 |
| `0x080b20d0` | `check_reveal_effect_summon_response_eligible` | 280 | 138 |
| `0x080b21f8` | `check_aqua_chorus_summon_response_eligible` | 104 | 51 |
| `0x080b226c` | `check_chain_destruction_summon_response_eligible` | 210 | 102 |
| `0x080b235c` | `check_summon_removal_trap_response_eligible` | 76 | 38 |
| `0x080b23b4` | `check_torrential_tribute_summon_response_eligible` | 34 | 15 |
| `0x080b23d8` | `check_two_pronged_attack_summon_response_eligible` | 156 | 73 |
| `0x080b2480` | `check_ultimate_offering_summon_response_eligible` | 298 | 146 |
| `0x080b25d4` | `check_player_monster_zone_empty_summon_response_eligible` | 26 | 12 |
| `0x080b25f0` | `check_solomons_lawbook_summon_response_eligible` | 152 | 75 |
| `0x080b2694` | `check_skull_lair_summon_response_eligible` | 148 | 72 |
| `0x080b2734` | `check_time_seal_summon_response_eligible` | 26 | 13 |
| `0x080b27e4` | `check_reversal_of_graves_summon_response_eligible` | 188 | 92 |
| `0x080b28ac` | `check_fiend_comedian_summon_response_eligible` | 64 | 32 |
| `0x080b28f8` | `check_position_change_summon_response_eligible` | 172 | 83 |
| `0x080b29b4` | `check_burst_breath_summon_response_eligible` | 92 | 42 |
| `0x080b2a10` | `check_discard_removal_summon_response_eligible` | 66 | 30 |
| `0x080b2a54` | `check_karma_cut_summon_response_eligible` | 66 | 30 |
| `0x080b2a98` | `check_thunder_of_ruler_summon_response_eligible` | 48 | 22 |
| `0x080b2ac8` | `check_adhesion_trap_hole_summon_response_eligible` | 44 | 21 |
| `0x080b2afc` | `check_non_aggression_area_summon_response_eligible` | 72 | 33 |
| `0x080b2b44` | `check_a_hero_emerges_summon_response_eligible` | 50 | 24 |
| `0x080b2b80` | `check_taunt_summon_response_eligible` | 48 | 22 |
| `0x080b2bb0` | `check_field_count_burn_summon_response_eligible` | 80 | 39 |
| `0x080b2c10` | `check_spell_trap_cleanup_summon_response_eligible` | 64 | 29 |
| `0x080b2c50` | `check_xing_zhen_hu_summon_response_eligible` | 30 | 14 |
| `0x080b2c70` | `check_assault_on_ghq_summon_response_eligible` | 102 | 50 |
| `0x080b2ce0` | `check_same_name_card_summon_response_eligible` | 80 | 38 |
| `0x080b2d38` | `check_gateway_zoma_summon_response_eligible` | 76 | 38 |
| `0x080b2d98` | `check_threatening_roar_summon_response_eligible` | 52 | 25 |
| `0x080b2dcc` | `check_chthonian_blast_summon_response_eligible` | 140 | 68 |
| `0x080b2e64` | `check_option_hunter_summon_response_eligible` | 66 | 32 |
| `0x080b2eb0` | `check_inferno_reckless_summon_response_eligible` | 52 | 25 |
| `0x080b2eec` | `dispatch_reactive_summon_response_eligibility_by_card_id` | 2398 | 1143 |
| `0x080b398c` | `dispatch_stat_modifier_summon_response_eligibility_by_card_id` | 1364 | 661 |
| `0x080b3fa8` | `check_graverobber_summon_response_eligible` | 126 | 60 |
| `0x080b4030` | `check_disappear_summon_response_eligible` | 98 | 47 |
| `0x080b4098` | `check_cross_side_summon_response_eligible` | 32 | 16 |

## 数据块分类 (Rule 2/3)

| 块 | ref-scan (raw / THUMB\|1) | 判定 | 理由 |
|---|---:|---|---|
| `[080b18e0,080b2758)` | 59 callback roots中前33项有真实odd table refs; 全内部flow/PC读闭合 | disasm | callback表消费者 `080b499c` 从record+4取Thumb pointer并经`invoke_r2`调用; CFG按真实分支/BL/PC literal到达. |
| `[080b2758,080b27e4)` 140B | 对范围内每个byte做全ROM sliding raw/odd扫描均0; 外部Thumb BL/B/Bcond目标0; 内部branch 5 | §5.1 | 前驱callback在`080b274c bx lr`结束, `[2750,2758)`为其literal pool, 无fallthrough. 原字节SHA256 `0b9cf850506224ff9903af4733ac4171abd785f51ccc539988c0c794c58088b5`. |
| `[080b27e4,080b40b8)` | 后26 callback roots有真实odd table refs; 全内部flow/PC读闭合 | disasm | 同一291-row callback表提供真实入口; independent CFG与本提案59个AddressSet逐项一致. |

完整 raw partition 为 code 8982B + literal pools 924B + zero padding 154B + §5.1 140B = 10200B. `f14-seg9-r4-cfg-map.json` 有4317条精确 instruction address/length/raw bytes, 231个pool words, 77个padding ranges, 938 direct flows, 240 PC reads和3978 architectural fallthrough. `root-f14-seg9-cfg-contract-gate.json` 已从ROM独立复算同值.

全ROM byte-granular扫描在157个raw数值上记录252个命中. `root-f14-seg9-raw-reference-leads.json` 保留每个原始source offset: `09e478d4..09e481e4`的结构化odd callback rows由真实consumer闭合; 其余unaligned/资产命中没有typed external call、没有相邻CID+callback row结构、也不进入CFG. 它们作为资产偶合原样留证, 不计Function incoming. 另对231个reachable literals和当前`asm/all.s`所有typed words复扫, 除两张表外没有指向Seg9 raw的真实pointer source.

`dispatch_reactive_summon_response_eligibility_by_card_id@080b2eec` 的17条local BL进入 `080b3854/080b38bc/080b3918/080b3978` 同frame尾片段. 这些BL在InstructionDB保留source+4默认机器fallthrough; 语义CFG从同frame尾片段继续到共享出栈路径并标记nonreturning local link. 不设FlowOverride, 不在四个片段建Function.

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS

- `EQ_ADD=153`: 6个current words中的3个与231个新pool中的150个. 每行 exact value/bytes/consumer/Equate/GAS expression见TSV.
- 复用既有常量包括 `PLAYER_BLOCK_STRIDE`, CID常量, field offsets, score deltas和 `CHECK_CARD_ID_IS_NORMAL_SUMMON_TYPE_THUMB`.
- `0x080b34d0=0x0804b165` 使用现有odd Thumb Equate, 并从source word添加到even Function `check_card_id_is_normal_summon_type@0804b164` 的辅助DATA ref; 不在odd地址新建Label/Data/ref, 既有odd地址DEFAULT `check_card_id_is_normal_summon_type+1` 前态保持.

### REF_SLOTS

`REF_ADD=82`, `REF_PRESERVE=2`:

| target | planned sources | contract |
|---|---:|---|
| `gP1LifePoints` | 42 new + 2 preserve | static USER ID15545; 两个既有 `/pointer` DATA refs CORE6原样保持 |
| `gDuelFieldSlots` | 26 | static USER ID20369 |
| `gDuelPhaseFlags` | 4 | static USER ID25230 |
| `gEquipChainSlotRefs` | 4 | static USER ID20367 |
| `gEquipLpScoreBase` | 2 | static USER ID30393 |
| `gP1FieldArrayCBase` | 2 new + 1 current | static USER ID21613 |
| `gDuelSpriteRowEntryCount` | 1 | 新USER label `0x0201b75c = gDuelPhaseFlags + LP_BAR_ANIM_STATE_OFF`; 现有 `/undefined4` 和全部incoming CORE6保持 |

RAM bytes保持null. dynamic DEFAULT target `DAT_0201b75c`物化成单一USER primary后, 只允许既有refs的derived target-primary metadata跟随; source/target/operand/type/source/primary六字段保持.

### RENAME_SLOTS

纯改名槽0. 237行由153 EQ +82 REF_ADD +2 REF_PRESERVE完整覆盖.

### FUNC_RENAME

现有Function改名0. 本段创建59个新Function; old Function/Symbol均不存在, TMode0. 最终名、body AddressSet/SHA、table incoming和internal CALL incoming见 `f14-seg9-function-projection-plan.json`. 每个新增Function追加registry tuple、正式naming CSV row和四份Function inventory; 不改任何既有Function名称.

### PLATE

- `F14-Seg-9.plates.tsv` 共63行: 1 PRESERVE, 59 `FUNCTION_CREATE_PLATE`, 3段外必要 `PLATE_REWRITE`.
- 新写入62条全部ASCII且每条不超过500 chars; 最大490.
- `select_equip_placement_slot_with_score@080b153c` 当前ASCII PLATE 439 chars语义与body一致, 保持不写DB.
- 段外只重写:
  - `check_normal_summon_eligible_for_slot@080b499c`: record布局订正为CID@+0、Thumb callback@+4, 并说明真实间接调用.
  - `check_normal_summon_eligible_any_slot@080b4ba8`: `cmp #0xdd; bls`是indices 0..221, 共222条, 不是221.
  - `check_normal_summon_eligible_by_card_tables@080b4be8`: 首表`cmp #0x44; bls`为69条, 次表222条, 不是68/221.
- 三个段外Function仅full PLATE变化; name/ID/body/signature/EOL/instructions/refs均保持.

## carve 计划 (R7)

必要段外结构化数据是两张normal-summon response表. 真实consumer `080b499c` 在 `080b49ae`读取record+0 CID, 在`080b4b46..080b4b4e`读取record+4并经`invoke_r2`调用. Bounds由两个真实循环确定:

- `[09e478d0,09e47fc0)`: 222 x 8B, SHA256 `fb20c7aa936a6c69a0a1b12c1a3cc57df79725fc799897cdebe4c24f38b82aa2`.
- `[09e47fc0,09e481e8)`: 69 x 8B, bounds consumer为`cmp #0x44; bls`.
- 每条结构为`.word internal_cid` + `.word callback_name+1`; 291个callback words全部odd且非0.

`asm/rom.s:1565`当前host `.incbin ...,0x1e478ce,0x243e` 精确拆为:

1. prefix `0x1e478ce,0x2`;
2. primary table `0x1e478d0,0x6f0`;
3. secondary table `0x1e47fc0,0x228`;
4. suffix `0x1e481e8,0x1b24`.

四段和仍为`0x243e`, 原host终点`0x1e49d0c`不变. 生成永久源码 `asm/normal_summon_response_tables.inc`, 由`asm/rom.s`在原位置`.include`; 不写入会被`.gitignore`和`clean-all.bat`处理的`data/`. `f14-seg9-table-carve-plan.json`逐条冻结582个word前态与after contract. 当前仅4个`/dword`+DEFAULT label, 其余578个为implicit DataDB; 最终物化582个`/dword` USER labels. 原6条incoming refs_to CORE6保持, 右bookend `09e481e8` 的独立`/dword`、值、label、incoming ref完全保持.

Callback投影分类:

- 140 rows -> 本段59个新Function: source odd Equate + auxiliary DATA ref to even Function.
- 55 rows -> 既有Function: 保持Function ID, source odd Equate + auxiliary DATA ref to even Function.
- 17 rows -> Seg10五个raw entries `080b46cc/4728/47f4/4820/4850`.
- 79 rows -> file15的raw leaf `080b76a4` (`01 20 70 47`, `movs r0,#1; bx lr`).

后两类96行仅用单一per-target pending even-address GAS alias并写`.word pending_name+1`; Seg9只落地表源, 不在这些target建Function/Label/Data/ref或改TMode. 五个`080b46cc/4728/47f4/4820/4850`目标交Seg10, `080b76a4`交file15对应段. 永久源`asm/normal_summon_response_tables.inc`由原host固定位置包含, 原odd payload逐条保持.

## disasm 计划 (R4)

- RestrictedAddressSet严格等于 `f14-seg9-r4-cfg-map.json` 的4317个instruction starts/lengths/raw bytes. 先seed 59个Function entries, 再逐项补齐全部missing expected starts; 不只对40个连续range起点调用一次disassembler.
- 新Function canonical body为158个最大连续ranges, 8982 code bytes, 每个body SHA在plan中.
- 231个literal words创建`/undefined4`与USER source label; 77个padding ranges保持implicit bytes; §5.1块不进RestrictedAddressSet.
- 最终整段: 4750 InstructionDB / 9886 codeB, 237 words / 948B, 158 paddingB, 140 §5.1B, 合计11132B.
- exporter原生输出允许mnemonic或`.hword`; 后验按InstructionDB地址/长度/raw bytes计数, 不把`.hword`当Data.

## 新增 constants / 全局

完整定义式和结构化证据在 `f14-seg9-constant-global-plan.json`.

### `constants/card_info.inc`

- `STONE_STATUE_OF_THE_AZTECS_CID = 0x1292`.
- `RUSH_RECKLESSLY_CID = 0x1329`.
- `SNAKE_FANG_CID = 0x1330`.
- `MASK_OF_WEAKNESS_CID = 0x13ee`.
- `JAM_DEFENDER_CID = 0x1402`.
- `DARK_SPIRIT_OF_THE_SILENT_CID = 0x146b`.
- `GILFORD_THE_LIGHTNING_CID = 0x154b`.
- `CALAMITY_OF_THE_WICKED_CID = 0x1575`.
- `STONE_STATUE_OF_THE_AZTECS_CID_SHIFT19 = STONE_STATUE_OF_THE_AZTECS_CID << 19`.
- `CYBER_TWIN_DRAGON_CID_SHIFT19 = CYBER_TWIN_DRAGON_CID << 19`.
- `CARD_FIELD3_THRESHOLD_1199 = 0x4af`; B2AF8由`get_card_extended_stat_field3`消费者证明.
- B2EA4复用既有`CARD_FIELD3_THRESHOLD_1499 = 0x5db` (`constants/card_info.inc:1352`), 不新增定义.

CID均有`data/cards-ids-array.s`、`data/card-stats.s`、password/data.md三路证据. 两个shift19常量由消费者先`lsl #19`再比较的实际位域证明.

### `constants/duel_field.inc`

- `SCORE_DIFFERENCE_THRESHOLD_1499 = 0x5db`; B35BC比较`r6-r9`.
- `TARGET_SCORE_THRESHOLD_1799 = 0x707`; B380C的r9来自field6、field5或0.
- `SCORE_DELTA_NEG_4000 = 0xfffff060`; signed32精确值-4000.

### `constants/ewram.inc`

- `gDuelSpriteRowEntryCount = gDuelPhaseFlags + LP_BAR_ANIM_STATE_OFF = 0x0201b75c`.

## §5.1 登记 (Rule 3)

- `[080b2758,080b27e4)` 140B, SHA256 `0b9cf850506224ff9903af4733ac4171abd785f51ccc539988c0c794c58088b5`.
- `root-f14-seg9-orphan-interior-scan.json`: 任一byte的全ROM 32-bit sliding hit=0, 所有偶地址的外部Thumb BL/B/Bcond target=0, 仅5条块内branch.
- `root-f14-seg9-orphan-head-direct-scan.json`: head raw/even和Thumb|1 hit=0.
- 源码继续保留原raw bytes; 不建Function、不改TMode、不建Data/label/ref/comment.

## 消费者证据 (R6)

| subject | consumer evidence | conclusion | confidence |
|---|---|---|---|
| callback ABI | `080b49ae`, `080b4b46..080b4b4e`; `root-f14-seg9-table-reference-evidence.json` | record+0是internal CID, +4是Thumb callback, 由`invoke_r2`执行 | high |
| table bounds | primary `080b4bc6/4bc8` and second-pass `080b4c5a/4c5c`; secondary `080b4c08/4c0a` | 物理表含222与69 rows; 扫描在首个accepted row提前退出 | high |
| 59 roots | 两表140个真实odd pointers; `root-f14-seg9-callback-cid-identities.json` | 每个新Function的卡身份与table source逐项闭合 | high |
| callback body semantics | `f14-seg9-callback-semantic-evidence-matrix-draft.md` 59 rows | 每条PLATE写明实际入参、关键工作/结果与指令地址; B1E04/B207C/B2D38/B2EEC含非普通BOOL出口 | high |
| `080b1c80` | `1cb6..1cd4` CID/field8筛选; getters `1cd8/1ce2/1cfe`; compares `1cdc/1ce6..1ce8`; save `1cfc..1d02`; accept `1cea..1cf0` | 首个保存field7必须非零; 后续不同值只要求signed<=6且可为0, 命中返回1 | high |
| `080b2028` | `2034..2048`, `204c..205a`, `205e..2068`三次取反侧选择 | 两条接受路径均使用对手占用数和对手LP | high |
| `080b2d38` | `2d4a..2d4e`, `2d72..2d76`, `2d7c..2d8a` | recorded-player相等拒绝; 不等进入分派; raw与BOOL出口分离 | high |
| `080b2eec` | `377a..3784`, `3978..397a`, caller `4b52..4b54` | 普通BOOL出口之外有绕过清零的raw u16 field出口 | high |
| corrected callback evidence | B19D0 call/test `1a4c/1a52..1a54`; B1A74 type22/input-side `1a82..1a86/1ae4..1af0`; B21F8 call/test `223c/2242..2248`; B28AC loads/comparisons `28b6..28c8/28d6..28d8/28ea..28ec` | 仅订正物理证据地址; body/CFG/返回合同不变 | high |
| `080b25d4` | `080b25dc`调用`count_occupied_monster_zones`, 随后比较0 | 玩家monster zone为空时返回1 | high |
| `080b34d0` | `080b3498`加载odd callback, 交给`count_monster_slots_by_fnptr` | normal-summon type predicate为真实Thumb callback | high |
| `080b2358` | `080b2340..2346`按unsigned count读取; `asm/07_equip_effect_chain.s:20459`将0x4cc标为chain slot count | `0201b75c`是chain slot count全局 | high |
| score constants | B2AE0/B2E8E field3 getters; B3592/B3594 r6-r9; B2F68/B2F80/B2F86 r9 sources; B1FA8 main +0x14 source | 1199/1499/1799按field3、score difference、target score和既有field5域分离; -4000保持signed delta | high |

## 求助

none.

## Executor Report: F14-Seg-9

- 槽: EQ=153 REF_ADD=82 REF_PRESERVE=2 RENAME=0 FUNC_RENAME=0 FUNC_CREATE=59 PLATE=63.
- carve=2 tables / 291 records; disasm=59 Functions / 158 body ranges / 4317 instructions; §5.1=1 range / 140B.
- 新增 constants/全局: 14 constants + `gDuelSpriteRowEntryCount`.
- 求助: none.
- proposal: `doc/dev/refine/F14-Seg-9.proposal.md`.
