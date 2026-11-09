# Refine Proposal: F15-Seg-4 [0x080b8a24..0x080babd4)

## 段测绘

- 现有函数入口: `0x080b8a24 check_equip_owner_has_more_occupied_monster_zones`，46B，21 条 InstructionDB，保持 Function 身份、AddressSet、签名、PLATE 与全部引用不变。
- 自动槽: 当前源码 0；R4 产生 130 个 4B 字面量池槽。完整前态、ROM 值、PC READ、目标、Equate、EOL 与后态见 `F15-Seg-4.slots.tsv`。
- 原始块: `[0x080b8a52,0x080babd4)`，8578B，当前为 implicit DataDB，TMode=0，无 Function owner。
- R4 后函数投影: 95 行，即 1 个 PRESERVE 与 94 个 CREATE。完整属性、Body AddressSet、SHA256、incoming/body refs、PLATE 与 inventory 合同见 `F15-Seg-4.plates.tsv`。
- 机器测绘: 3714 条 Thumb 指令/7920B、130 个池/520B、69 段零填充/138B，三者精确覆盖 8578B；94 个新 Function 共 144 个半开 body ranges，无重叠、无非零空洞。

新建函数按入口地址如下；每个名称和 PLATE 均由实际函数体、调用参数、返回分支及表记录 CID 共同约束：

| 入口 | 名称 |
|---|---|
| 080b8a54 | check_mystic_box_zone_count_response_eligible |
| 080b8a84 | check_snatch_steal_high_value_target_response_eligible |
| 080b8b38 | check_falling_down_archfiend_target_response_eligible |
| 080b8b64 | check_mind_control_zone_response_eligible |
| 080b8bb8 | check_monster_reborn_target_response_eligible |
| 080b8c54 | check_silent_fiend_target_attribute_response_eligible |
| 080b8c8c | check_grave_revival_target_response_eligible |
| 080b8d6c | check_shallow_grave_dual_target_response_eligible |
| 080b8e2c | check_tribute_doll_target_score_response_eligible |
| 080b8e68 | check_dark_magic_curtain_handler_response_eligible |
| 080b8eac | check_graverobber_target_response_eligible |
| 080b8f68 | check_stop_defense_target_score_response_eligible |
| 080b9090 | check_curse_of_anubis_multi_target_response_eligible |
| 080b90d0 | check_block_attack_target_score_response_eligible |
| 080b91f8 | check_enemy_controller_target_score_response_eligible |
| 080b9310 | check_reverse_trap_zone_score_response_eligible |
| 080b9398 | check_shield_and_sword_zone_score_response_eligible |
| 080b93f0 | check_card_destruction_hand_response_eligible |
| 080b94fc | check_exchange_hand_target_response_eligible |
| 080b9514 | check_megamorph_target_score_response_eligible |
| 080b95a4 | check_metalmorph_effect_zone_response_eligible |
| 080b95c8 | check_discard_recovery_spell_response_eligible |
| 080b96c4 | check_blast_with_chain_target_score_response_eligible |
| 080b9734 | check_generic_equip_target_score_response_eligible |
| 080b9770 | check_generic_equip_target_available_response_eligible |
| 080b978c | check_equip_pair_and_target_response_eligible |
| 080b97b4 | check_special_equip_target_handler_response_eligible |
| 080b981c | check_heart_of_clear_water_target_response_eligible |
| 080b9868 | check_equip_debuff_target_score_response_eligible |
| 080b98bc | check_riryoku_chain_match_response_eligible |
| 080b98f0 | check_hand_reload_response_eligible |
| 080b99b0 | check_magical_mallet_hand_response_eligible |
| 080b9abc | check_mass_revive_zone_capacity_response_eligible |
| 080b9b3c | check_level_limit_area_b_response_eligible |
| 080b9b7c | check_big_wave_small_wave_response_eligible |
| 080b9bb8 | check_beckoning_light_response_eligible |
| 080b9bf0 | check_level_modulation_target_response_eligible |
| 080b9c28 | check_pot_draw_count_response_eligible |
| 080b9c50 | check_makiu_target_score_response_eligible |
| 080b9cdc | check_knights_title_handler_response_eligible |
| 080b9d08 | check_inferno_fire_blast_active_equip_response_eligible |
| 080b9d28 | check_rescue_cat_handler_response_eligible |
| 080b9d50 | check_slot_chain_value_absent_response_eligible |
| 080b9d70 | check_call_of_the_mummy_response_eligible |
| 080b9d8c | check_toon_table_contents_search_response_eligible |
| 080b9e34 | check_excavation_mage_stones_response_eligible |
| 080b9e6c | check_level_up_evolution_target_response_eligible |
| 080b9eb4 | check_jade_insect_whistle_chain_response_eligible |
| 080b9ed0 | check_earthquake_pair_response_eligible |
| 080b9ef0 | check_metal_reflect_slime_pair_response_eligible |
| 080b9f08 | check_metamorphosis_nonspell_target_response_eligible |
| 080b9f5c | check_monster_reincarnation_source_response_eligible |
| 080b9fc0 | check_overpowering_eye_peak_score_response_eligible |
| 080ba018 | check_tribute_handler_response_eligible |
| 080ba090 | check_catapult_turtle_target_score_response_eligible |
| 080ba134 | check_cannon_soldier_target_response_eligible |
| 080ba194 | check_ultimate_baseball_kid_threshold_response_eligible |
| 080ba1d4 | check_time_wizard_zone_score_response_eligible |
| 080ba1f0 | check_jowgen_zone_activation_absent_response_eligible |
| 080ba20c | check_amazon_archer_monster_count_response_eligible |
| 080ba24c | check_forgiving_maiden_target_response_eligible |
| 080ba29c | check_karate_man_slot_score_response_eligible |
| 080ba358 | check_valkyrion_opponent_zone_empty_response_eligible |
| 080ba388 | check_cyber_stein_target_response_eligible |
| 080ba3cc | check_goddess_of_whim_slot_response_eligible |
| 080ba400 | check_xyz_dragon_cannon_zone_response_eligible |
| 080ba450 | check_vw_tiger_catapult_zone_response_eligible |
| 080ba488 | check_ritual_field_clear_response_eligible |
| 080ba518 | apply_blast_magician_slot_value_and_check_response |
| 080ba53c | check_neo_daedalus_field_clear_response_eligible |
| 080ba5c4 | mark_swarm_effect_mode_and_check_response |
| 080ba628 | check_union_equip_chain_absent_response_eligible |
| 080ba678 | check_breaker_whitelist_response_eligible |
| 080ba6ac | check_agent_saturn_lp_ratio_response_eligible |
| 080ba708 | check_thunder_dragon_zone_pair_response_eligible |
| 080ba71c | check_king_of_swamp_fusion_response_eligible |
| 080ba774 | check_gear_golem_slot_score_response_eligible |
| 080ba7e0 | check_chaos_banish_response_eligible |
| 080ba84c | check_diffusion_wave_motion_response_eligible |
| 080ba890 | check_checkmate_archfiend_count_response_eligible |
| 080ba8e4 | check_dark_scorpion_combination_response_eligible |
| 080ba914 | check_discard_bounce_target_response_eligible |
| 080ba948 | check_battery_charger_response_eligible |
| 080ba988 | check_armed_dragon_lv5_response_eligible |
| 080ba9a8 | check_armed_dragon_lv7_response_eligible |
| 080ba9f4 | check_armed_dragon_lv10_response_eligible |
| 080baa2c | check_gaia_soul_target_response_eligible |
| 080baa88 | check_zorc_opponent_monster_present_response_eligible |
| 080baaa8 | check_super_robolady_opponent_zone_empty_response_eligible |
| 080baac8 | check_gatling_dragon_multiple_opponents_response_eligible |
| 080baae8 | check_hand_of_nephthys_target_response_eligible |
| 080bab1c | check_elemental_hero_tempest_whitelist_response_eligible |
| 080bab3c | check_raviel_token_pair_response_eligible |
| 080baba8 | check_archlord_zerato_field_spell_response_eligible |

## 数据块分类 (Rule 2/3)

| 块 | ref-scan | 判定 | 理由 |
|---|---:|---|---|
| 080b8a52..080babd4, 8578B | raw/even=0 true Function holders; THUMB|1=202 true table words to 94 roots; typed inbound branch=0 | disasm | 202 个 `asm/equip_activation_response_tables.inc` 回调词由真实表消费者间接调用；完整 Thumb CFG 将块精确分为 7920B 指令、520B 池与 138B 零填充。 |

全 ROM sliding scan 的另 9 个数值命中均不构成控制流或 DATA 引用。8 个命中位于已验证的 palette/tile/高熵尾部资产；`0x081a5693 -> 0x080b8c1a` 是未对齐 packed-stream 数值重合，目标为 `0x080b8bb8` body 内依赖已恢复 frame 的普通指令，源偶/奇精确地址命中均为 0。证据为 `root-f15-seg4-raw-reference-leads.json` 与 `root-f15-seg4-nonreference-assets.json`。

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS

- 85 个槽执行 `EQ_ADD`；完整值、Equate 名、GAS 表达式、复用状态及消费者地址见 `F15-Seg-4.slots.tsv`。
- 81 个绑定复用现有 Ghidra Equate；4 个名称在 Ghidra 全局 Equate 前态中缺失，其中 `BOOK_OF_LIFE_CID` 已有 GAS 定义，只新增 Ghidra 绑定。
- 新增 GAS 常量 3 个：
  - `CARD_FIELD3_THRESHOLD_1700 = 0x000006a4`，放入 `constants/card_info.inc`；三个消费者均比较 `get_card_extended_stat_field3` 结果。
  - `CHAOS_COMMAND_MAGICIAN_CID = 0x00001614`，放入 `constants/card_info.inc`；`data/card-stats.s:16564,44614` 与 `data/cards-ids-array.s:1662` 将 internal CID `0x1614` 绑定到 Chaos Command Magician。
  - `RESPONSE_OPPONENT_LP_THRESHOLD_2900 = 0x00000b54`，放入 `constants/duel_field.inc`；消费者比较对侧 LP `<=2900`；定义继续放入 `constants/duel_field.inc`，域为 response/opponent LP，不是 zone score。
- `BOOK_OF_LIFE_CID = 0x1536` 复用 `constants/card_info.inc:1213`，不新增 GAS 常量。

### REF_SLOTS

- 43 个池槽执行 `REF_ADD`：物化池 USER label，保持静态 USER target Symbol ID，新增一条源池到目标的 `DATA/USER_DEFINED/operand0/primary=true` 引用。完整目标前态和后态引用见 slots TSV。
- RAM 目标不读取未初始化字节；`target_prestate_json.bytes=null` 保持。

### THUMB_REF_SLOTS

- `0x080b8b58` 与 `0x080ba8d8` 的值均为 `0x0804aea1`。复用 `check_card_is_archfiend_type_1`，源池 Equate 使用奇值，并仅向偶地址 `0x0804aea0` 添加辅助 DATA ref；不在奇地址创建 Symbol、Data 或 reference target。

### RENAME_SLOTS / FUNC_RENAME

- 纯槽改名 0；现有 Function rename 0。
- 94 个入口是从 raw 创建的新 USER Function，不属于 rename。全局 canonical `temp/ghidra-functions.csv` 检测到 0 个名称冲突。

### PLATE

- `0x080b8a24` 为 PRESERVE，不写 DB；其既有 ASCII PLATE 长度 587，不因长度单独改写。
- 94 个 CREATE 均写入逐函数 ASCII PLATE，最大 491 字符。PLATE 明确入口实际使用的寄存器、关键短路顺序、接受极性、返回形状与副作用；全文在 `F15-Seg-4.plates.tsv` 和 `f15-seg4-semantic-plan.json`。
- Mode A v3 保留 round2 已通过的 28 条正文，并按完整函数体再次收紧 9 条 after-PLATE：B8EAC、B8F68、B90D0、B91F8、B97B4、B98F0、B9C50、B9D8C、BA29C。formal、semantic、Function 与 R4 投影逐 entry 等值；所有文本 ASCII 且不超过 500 字符。

## 外部回调表投影

- 202 个现有回调源词覆盖 94 个新入口。逐源保持原字节、Data type、USER 源 label ID、EOL 与已有 CORE6；把 `pending_card_response_callback_<addr>_1` 替换为 `<final_name>_1`，GAS 表达式写 `<final_name>+1`，并向偶 Function 添加 DATA ref。
- 清除 94 个 pending Equate 的条件是其引用数变为 0。新增 94 个最终 Function `_1` Equate，202 个绑定数量保持。
- `0x09e48e9c -> 0x080baccc+1` 属 F15-Seg-5，保持 pending alias、原词和引用不变。
- 精确合同为 `f15-seg4-external-table-source-plan.json`。全局 Equate 从 2421 objects/12238 bindings 变为 2425/12325：新增 98、退休 94、扩展 37 个既有名称。

## carve 计划 (R7)

- 无。外部 response tables 已在先前段结构化，本段只做 202 个源表达式与 Ghidra Equate/ref 投影。

## disasm 计划 (R4)

- 只在 `[0x080b8a52,0x080babd4)` 内，按 `f15-seg4-r4-plan.json` 的 144 个半开 code ranges、3714 个精确 instruction starts 与 94 个 root seeds 反汇编。
- 创建 94 个 Function，AddressSet 不强制连续；两个内部 BL 目标 `0x080b8a84`、`0x080b9734` 同时是表 root，保持独立 Function。
- 130 个池地址不反汇编，物化 `/undefined4` 与 slots TSV 指定的 USER label；135 条 PC READ 保持 `READ/DEFAULT/operand1/primary=true`。
- 69 段零填充保持字节，不物化数据。不得在批准 code/pool 之外 clear、retype 或创建 Function。
- `0x0804becc` 的 `[0x0804becc,0x0804bf20)` 84B raw 块是已有正引用依赖：既有 typed BL `0x0804d374`，本段新增已批准 BL `0x080b9e0a`。它不属于零引用 §5.1；本段保持地址序，只冻结 exact AddressState/raw/DEFAULT Label/既有来向并新增该 BL 的只读后验，禁止在 module05 创建 Function、反汇编或改源码。后续由驱动器按补漏清单单独闭合。

## 新增 constants / 全局

- GAS 新增: `CARD_FIELD3_THRESHOLD_1700`, `CHAOS_COMMAND_MAGICIAN_CID`, `RESPONSE_OPPONENT_LP_THRESHOLD_2900`。
- Ghidra 新增 Equate objects: 上述 3 个、`BOOK_OF_LIFE_CID`、94 个最终 Function `_1` aliases。
- 新建 94 个 Function、130 个池 USER labels；不在奇地址建 label，不为表基址或数值偶合增加引用。

## §5.1 登记

- 无。原始块全部由 202 个真实回调源引用并由闭合 CFG 覆盖。

## 消费者证据 (R6)

- `asm/equip_activation_response_tables.inc` 的 202 个 callback words 是新 Function 的真实 incoming；源词、CID/card 关联与最终函数名逐项冻结在 external-table plan 和 callback CID evidence 中，置信度 high。
- `asm/15_equip_target_summon_zoom.s:7647` 是当前 raw host；R4 后原生源码必须按地址导出相同指令、池与 padding，置信度 high。
- 130 个池的 135 个 PC consumers、operand 与目标记录在 slots TSV 和 `f15-seg4-r4-plan.json`，置信度 high。
- `0x0804becc` 的只读 raw body 对 CID 集合 `{1610,1611,1615,161a,1695,16de,186a,1983}` 返回 1；`0x0804d374` 与 `0x080b9e0a` 是明确正引用，因此该块进入后续正引用补漏交接而非 §5.1。前态证据 `root-f15-seg4-external-04becc-prestate.json` SHA-256 `5455d01ee7d57829e4e4cf278aa367b7e85542945f11c23a4477ec32114b646b`，置信度 high。

## 不变量与落地边界

- 字节红线: 原 ROM `[0x080b8a24,0x080babd4)` 8624B 必须逐字节不变。
- 静态 USER target Symbol/Function ID 不变；新 USER Function/池 label 允许分配新 ID；同址 alias 禁止。
- 正式 inventory 只更新 `doc/dev/naming-proposals.csv` 与 `temp/ghidra-functions.{csv,renamed.txt,auto.txt,summary.md}`；`tools/ghidra-labeling` 历史快照保持。
- Sticky native GAS projections 保持：F14 三个 table bases、F15-Seg1 五个 Thumb、F15-Seg2 三个 Thumb，不由本段改写。

## 求助

- none

## Executor Report: F15-Seg-4

- 槽: EQ=85 REF=43 THUMB_REF=2 RENAME=0 FUNC_RENAME=0 PLATE=95 (94 CREATE + 1 PRESERVE)
- carve=0 disasm=144 body ranges / 94 Functions §5.1=0
- 新增 constants/全局: 3 GAS constants; 4 scalar Ghidra Equates; 94 Function `_1` Equates; 94 Functions; 130 pool labels
- 求助: none
- proposal: `doc/dev/refine/F15-Seg-4.proposal.md`
