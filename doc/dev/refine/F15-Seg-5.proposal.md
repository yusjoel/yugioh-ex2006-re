# Refine Proposal: F15-Seg-5 [0x080babd4..0x080bb3dc)

## 段测绘

- 现有 Function 11 个：`080babd4 check_hand_equip_target_meets_bonus_4`、`080bacfc invoke_count_occupied_monster_zones`、`080bad10 check_lp_below_zone_count_threshold`、`080bad6c check_equip_eligible_by_slot_flag_or_pair_count`、`080badf4 check_equip_effect_zone_eligible_for_rapid_fire_and_warlock`、`080bae6c check_card_summon_eligible_by_field6`、`080baed0 try_activate_equip_for_matching_slot`、`080bb0f8 find_equip_slot_by_player_and_zone_count`、`080bb2d4 dispatch_field_spell_equip_ai_by_phase`、`080bb35c scan_all_effect_zone_entries_for_equip_activation`、`080bb38c try_activate_equip_via_two_tables`。
- 当前自动 word 48 个；R4 新增池 2 个。完整 50 槽前态与计划见 `F15-Seg-5.slots.tsv`。
- raw 块 `[080baccc,080bacfc)` 48B。当前为 implicit DataDB，TMode=0，无 Function owner。
- 既有 typed 布局为 849 InstructionDB/1784B、48 words/192B、32B padding。R4 后为 869 InstructionDB/1824B、50 words/200B、32B padding，总计 2056B。

## 数据块分类 (Rule 2/3)

| 块 | ref-scan (raw / THUMB+1) | 判定 | 理由 |
|---|---:|---|---|
| 080baccc..080bacfc, 48B | raw=0, THUMB=1 at 09e48e9c, extras=0, typed inbound=0 | disasm | 真消费者是 effect-zone response table row 176；块精确分为 20 条 Thumb 指令/40B 与两个 PC literal/8B，无 padding、无孤儿。 |

入口 `080baccc` 的行为由原始指令闭合：`player=record[2]&1`，`slot=(record[2]>>1)&31`，读取 `gDuelFieldSlots + player*0x868 + slot*20 + 12` 的无符号 dword，严格大于 1 返回 1，否则 0。表 CID `0x1810` 由 `data/cards-ids-array.s:2170`、`data/card-stats.s:21972,50328` 和 `THE_BLOCKMAN_CID` 交叉绑定为 The Blockman；函数名称保持结构语义，不给 `slot+12` 字段附加未证实的领域名。

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS

- 28 个槽执行 `EQ_ADD`，逐槽值和 operand0 绑定见 slots TSV。
- 复用现有定义：`PLAYER_BLOCK_STRIDE`、`LP_P2_LOOP_CEIL_OFF`、`DARK_ERADICATOR_WARLOCK_CID`、`HORUS_LV8_CID`、`SORCERER_OF_DARK_MAGIC_CID`、`SKULL_DESCOVERY_KNIGHT_CID`、`ACTIVATION_ENTRY_CLR_BITS_14_6`、`NORMAL_SUMMON_PLAYER_CACHE_OFF`、`LP_PLAYER_SIDE_CACHE_OFF`、`ELIGIB_ACT_COUNT_OFF`、`GILASAURUS_CID`、`MANGA_RYU_RAN_CID`、`LAVA_GOLEM_CID`、`MEGAROCK_DRAGON_CID`、`ATK_THRESHOLD_2999`、`P1LP_BLOCK2_OFF_1CE8`。
- 新增 `RAPID_FIRE_MAGICIAN_CID = 0x1964` 至 `constants/card_info.inc`。结构化证据：`data/cards-ids-array.s:2510` 与 `data/card-stats.s:25625,54168`。
- 新增 `EQUIP_ACTIVATION_READY_FLAG_OFF = 0x1c38` 至 `constants/ewram.inc`；消费者 `080bb286` 对 `gP1FieldArrayCBase+0x1c38` 写 1，且同一状态提交路径在 `080bb274` 写 player cache。

### REF_SLOTS

- `REF_ADD=15`，`REF_PRESERVE=7`。新增引用全部为 `DATA/USER_DEFINED/operand0/primary=true`；既有 DEFAULT 或 USER reference 的 CORE6 保持，不统一升级 source type。
- 复用目标：`gP1LifePoints`、`gP1ZoneHandCount`、`gDuelFieldSlots`、`gDuelFieldSlotState`、`gP1FieldArrayCBase`、`gEquipLpScoreBase`、`equip_ai_phase_response_table`、`equip_activation_response_table`、`equip_activation_secondary_response_table`。
- `080bb3b0` 接通新 carve label `equip_activation_three_row_response_table`，目标 `09e488d8`。

### RENAME_SLOTS

- 0。所有 50 个源槽均物化语义 USER label 与 ASCII EOL；静态 USER target ID 保持，dynamic DEFAULT source label 可合法换为 USER ID。

### FUNC_RENAME

| 入口 | 旧名 | 新名 | 证据 |
|---|---|---|---|
| 080bb0f8 | find_equip_slot_by_player_and_zone_count | try_activate_equip_from_field_array_for_player | `r1` 仅在 `080bb210` 作 0/nonzero mode gate；函数扫描 field-array count，成功时写 target refs/activation state 并返回 1，不返回 slot index。incoming=3。 |
| 080bb2d4 | dispatch_field_spell_equip_ai_by_phase | dispatch_equip_activation_ai_by_phase | 三阶段均走 equip activation tables/sequence/field-array activation；phase0/1失败在同次调用内递增并顺落，phase2失败递增后返回1；成功返回0且不增加当前phase。odd holder=`09e5ab5c`，Function ID/body/signature保持。 |

BB0F8 的实际外部调用点 `080bc582`、`080bc600` 仅投影 BL 名称；对应两个 owner PLATE 全文重写，把 `r1` 订正为 mode flag。两项完整前态和 ASCII 新文见 plates TSV。BB2D4 的 `09e5ab5c` 词保持原值、类型、DEFAULT Symbol ID 和 reference CORE6，仅holder/odd派生 target name 随 Function rename 更新；BC71C 的两条holder引用只冻结同一派生名称投影，不改其PLATE、name、body或签名。

### PLATE

- 段内 12 个 Function（11 既有 + 1 CREATE）全部写入经实际指令核定的 ASCII PLATE，均不超过 500 字符。
- 外部必要投影 2 个：`080bc54c` 与 `080bc5d4`。不改其名称、body、签名或引用。
- 关键订正：BADF4 两次 effect-zone 查询均使用 record owner；BAE6C 的 0x17d4/0x17c6/0x1771 是 CID；BB0F8 的 `r1` 是 mode flag；BB2D4 是 equip activation phase dispatcher；BB38C 首表正是三行表。
- `BAED0`：槽0..10路径要求CID相等、bits5/1清；slot+8非零调用`eval_equip_activation_for_slot`，为零调用`check_card_zone_activation_blocked`，所选结果非零；另需summon==0、callback!=0。无槽提交时fallback要求index>=0、unavailable!=0、blocked!=0、summon==0、callback!=0。槽提交写`gP1LifePoints+0x1d64=player`、`+0x1d58` activation count=1及`target(player,slot,0,3)`；fallback写`gP1FieldArrayCBase+0x1c44=player`、`+0x1c38` ready=1及`target(player,11,index,3)`。
- `BB0F8`：公共门槛为field5非零和`eval_equip_target_slot_flags!=0`；CID 1488、127D..127F/12A5/154A、18B4、1578、19A5的附加条件按review表逐项冻结。成功写FieldArray player/ready、`target(player,11,index,2)`并清`gEquipLpScoreBase+0x180`；耗尽返回0。
- `BB2D4`：phase0扫描57行失败后递增并同次顺落phase1，phase1失败递增并顺落phase2；phase2以mode0调用field-array激活，失败递增并返回1。任一成功返回0且不增加当前phase，先前递增保留。
- `BC54C`：state0读取无符号`gP1FieldState`且须<=2；state0/1失败递增并同次顺落。state2先调用cache-aware score helper，仅cache无效时计算/写回，再扫五个mode0槽；耗尽返回1且不推进state2。
- `BC5D4`：mode1的state0/1同样递增顺落，state2扫五个mode1槽、耗尽返回1且不推进；本函数没有BC54C的显式score-cache调用。
- after-rich合同由单一批准Symbol图生成：50池USER label、6 carve USER label、2 rename Function、holder/odd DEFAULT label及BACF0 DEFAULT flow label逐项冻结name/type/source；仅实际新USER/DEFAULT对象的ID用地址化DYNAMIC token。

## carve 计划 (R7)

把 `asm/equip_activation_response_tables.inc` 中 `[09e488d8,09e488f0)` 的 24B raw 替换为三行结构：

```asm
equip_activation_three_row_response_table:
    .word WILD_NATURES_RELEASE_CID
    .word check_effect_node_eligible_in_any_slot_with_field6_score+1
    .word METEORAIN_CID
    .word check_opponent_active_zone_cards_present+1
    .word DRAGONS_RAGE_CID
    .word check_opponent_active_zone_cards_present+1
```

- 三个 CID 和两个回调名均复用现有定义/Function；每个 odd word 精确等于 ROM。
- Ghidra 前态仅 `09e488d8`、`09e488e0` 为 `/dword`，其余四词 implicit。落地时保留两既有 Data/Symbol 前态并物化其余四个 `/dword`；所有六个源词加 operand Equate，三个回调词另加到偶 Function 的 DATA ref，奇地址不创建 Symbol/Data/ref。
- 邻接 `09e488d4` 与 `09e488f0` 字节、Data、Symbol、引用保持。

## disasm 计划 (R4)

- `[080baccc,080bacf4)` 按 20 个精确 instruction starts 反汇编并创建 `check_selected_slot_word12_above_one_response_eligible`，body 为单一半开 range，40B SHA256 由 machine plan 冻结。
- `080bacf4=PLAYER_BLOCK_STRIDE`、`080bacf8=gDuelFieldSlots` 物化 `/undefined4` pool；PC READ 分别来自 `080bacde`、`080bace4`，均保持 `READ/DEFAULT/operand1/primary=true`。
- 不 clear/retype 任何范围外 code/data，不写 FlowOverride。

## 外部回调绑定闭合

- `09e48e9c` 原值 `080baccd` 不变：把 `pending_card_response_callback_080baccc_1` 替换为 `check_selected_slot_word12_above_one_response_eligible_1`，GAS 写 `Function+1`，并新增到偶 Function 的 DATA ref。
- 仅在 pending alias 引用数变 0 后退休旧 Equate。此前 17 项 sticky GAS projections、模块 05 的 84B positive-backlog raw 和正式 exporter 均不改。

## 新增 constants / 全局

- GAS constants: `RAPID_FIRE_MAGICIAN_CID`, `EQUIP_ACTIVATION_READY_FLAG_OFF`。`SKULL_DESCOVERY_KNIGHT_CID`复用既有GAS/Ghidra对象，保留0804BBD0并新增BAEC0绑定；最终全局Equate为2429对象/12359绑定，不增加第18项GAS pin。
- ROM label: `equip_activation_three_row_response_table`。
- USER Function: `check_selected_slot_word12_above_one_response_eligible`。

## §5.1 登记

- 无。48B raw 有真实 THUMB table 引用并完整 R4；24B 外表有 BB38C 真消费者并在本段 carve。

## 消费者证据 (R6)

- `080baccc-080bacf2`: raw callback 参数拆分、slot stride 和返回比较，confidence=high。
- `080bb0f8-080bb2d0`: mode gate、CID-specific branches、提交 side effects 和所有返回，confidence=high。
- `080bb2d4-080bb356`: 三 phase 分支与返回极性，confidence=high。
- `080bb38c-080bb3d6`: 三行/五行表循环边界与 retry gate，confidence=high。
- `asm/equip_activation_response_tables.inc:1628-1630`: The Blockman CID 与 pending callback word，confidence=high。

## 求助

- none

## Executor Report: F15-Seg-5

- 槽: EQ=28 REF_ADD=15 REF_PRESERVE=7 RENAME=0 FUNC_RENAME=2 PLATE=14
- carve=1 table/24B disasm=1 range/1 Function §5.1=0
- 新增 constants/全局: RAPID_FIRE_MAGICIAN_CID; EQUIP_ACTIVATION_READY_FLAG_OFF; equip_activation_three_row_response_table; check_selected_slot_word12_above_one_response_eligible
- 求助: none
- proposal: `doc/dev/refine/F15-Seg-5.proposal.md`
