# Refine Proposal: F14-Seg-8 [0x080b04a8..0x080b153c)

## 段测绘

- 模块: `asm/14_equip_ai_scoring.s`, 4244 bytes.
- 独立 typed-unit 基线 `root-f14-seg8-independent-baseline-scan.json` 与当前源码/ROM/Ghidra 一致: 1819 个 InstructionDB (1659 mnemonic + 160 `.hword`) 共 3788 bytes, 101 个 4-byte words 共 404 bytes, 52 bytes padding, raw block 0. 14 个现有 Function 的 body 恰好拥有全部 3788 个 code bytes.
- 101 个 words 的前态为 `/undefined4` 95, `/pointer` 5, `/dword` 1; source DATA refs 5, PC READ refs_to 114. `F14-Seg-8.slots.tsv` 逐槽冻结 bytes, Data type, Symbols/primary, refs_from, refs_to, Equates, EOL 和 owner.
- 14 个 Function:

| entry | current name | body bytes |
|---|---|---:|
| `0x080b04a8` | `eval_fieldspell_equip_placement_full` | 492 |
| `0x080b06b4` | `score_equip_zone_slots_for_all_players` | 1038 |
| `0x080b0b64` | `save_field_slots_to_buffer` | 36 |
| `0x080b0b90` | `restore_field_slots_from_buffer` | 38 |
| `0x080b0bc0` | `prepare_effect_zone_slots_for_field_action` | 150 |
| `0x080b0c60` | `find_best_placeable_monster_slot` | 212 |
| `0x080b0d54` | `score_equip_zone_slots_for_player` | 528 |
| `0x080b0f98` | `compute_equip_zone_score_with_cache` | 76 |
| `0x080b0fe8` | `eval_equip_monster_zone_score_full` | 126 |
| `0x080b1078` | `eval_fieldspell_placement_with_zone_scores` | 136 |
| `0x080b1114` | `find_best_equip_target_slot_for_player` | 542 |
| `0x080b135c` | `select_optimal_monster_placement_slot` | 152 |
| `0x080b1400` | `select_activation_placement_slot` | 82 |
| `0x080b1458` | `check_card_field_spell_equip_placeable` | 180 |

## 数据块分类 (Rule 2/3)

| 块 | ref-scan (raw / THUMB\|1) | 判定 | 理由 |
|---|---:|---|---|
| 段内 | raw block 0 | none | 4244 bytes 已完全分类为 typed code, 101 words 和 padding, 不存在 `ROM_INCBIN` 或 `.byte` 块. |

全 ROM byte-granular raw/THUMB 扫描覆盖 101 个 pool source 和 14 个 Function entry. 四个拟改名入口 `0x080b06b4`, `0x080b0c60`, `0x080b135c`, `0x080b1400` 的 raw/even 与 THUMB|1 hit 均为 0, 因而没有 function-pointer alias 投影. pool 地址在压缩资产字节中的数值偶合保留原始 offset, 不构成 source reference; 明细在 `root-f14-seg8-independent-baseline-scan.json`.

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS

- `EQ_ADD=61`. 其中 56 行复用现有 constants, 5 行绑定 4 个新增 domain constants. 每行 operand-0 Equate, GAS expression, source bytes 与真实 refs_to 在 `F14-Seg-8.slots.tsv`.
- 新绑定:
  - `0x080b06a4=0xffff0000` -> `FIELD_PLACEMENT_SCORE_SENTINEL_NEG_65536`; 该值写入 placement result `+0x1c` 作为 signed score 初值, 不复用 equip-chain terminator 名.
  - `0x080b097c=0x174a` -> `KA_2_DES_SCISSORS_CID`; cards-ids/card-stats/passcode/data.md 四路证据见 `f14-seg8-card-constant-evidence.json`.
  - `0x080b0d0c` 与 `0x080b0f8c` 的 `0xffffe000` -> `SLOT_CARD_SET_CODE_CLEAR_MASK`; 两处都以 halfword slot field 清除低 13-bit CID/set-code, 不复用 OAM tile 域名称.
  - `0x080b1354=0x383` -> `ZONE_SCORE_THRESHOLD_899`; `0x080b12c8..12ce` 对 signed candidate score 做 `>899` gate.
- `0x080b0d14=0x1388` 复用现有 `lookup_equip_card_score_cid_1388`. ROM inverse CID 为 `0xffff`; consumer 与 `MAJU_GARZETT_CID`/`GREAT_MAJU_GARZETT_CID` 同域比较, 不赋卡名或 LP 含义.

### REF_SLOTS

`REF=40`, 包括 `REF_ADD=35` 和 `REF_PRESERVE=5`:

| target | sources | contract |
|---|---:|---|
| `gEquipLpScoreBase` | 10 | 静态 USER ID30393 保持 |
| `gDuelFieldSlots` | 12 | 静态 USER ID20369 保持 |
| `gP1LifePoints` | 5 | 5 条既有 `/pointer` DATA refs CORE6 原样保持 |
| `gEquipZoneScoreEntryBase` | 4 | 新 USER label `0x0201aff8` |
| `gEquipFieldSpellPlacementResult` | 2 | 新 USER label `0x0201b18c` |
| `gDuelFieldSlotState` | 2 | 静态 USER target 保持 |
| `gEquipChainSlotRefs`, `gEquipSpellZoneScoreValueBase`, `gEquipPlacementOccupiedZoneCount`, `gP1FieldArrayCBase`, `gP1ZoneHandCount` | 各 1 | 按 TSV 精确执行 |

四个新 RAM label 当前均为 dynamic DEFAULT primary. `f14-seg8-target-contract.json` 冻结全部既有 incoming refs, source/operand/primary 等 CORE6 不变; materialize 单一 USER primary 后只允许 derived target-primary ID/name/source 更新. `root-f14-seg8-target-consumer-prestate.json` 另冻结 11 个真实 owner Function, 19 个 direct source states 和 4 个 target states. RAM bytes 保持 null; `0x0201aff8`/`0x0201b010` 不创建 Data, `0x0201b16c`/`0x0201b18c` 保持现有 `/undefined4`.

### RENAME_SLOTS

纯改名槽 0. 101 个 current words 由 61 EQ + 35 REF_ADD + 5 REF_PRESERVE 全覆盖.

### FUNC_RENAME

| entry | old | new | indeg / evidence |
|---|---|---|---|
| `0x080b06b4` | `score_equip_zone_slots_for_all_players` | `select_fieldspell_equip_placement_result` | indeg=2 (`0x080b0f6c`, `0x080b1052`); 收集/排序候选后调用 `eval_fieldspell_equip_placement_full`, 成功复制 0x20-byte result 并返回1, 不返回累计 score. |
| `0x080b0c60` | `find_best_placeable_monster_slot` | `prepare_first_placeable_monster_slot` | indeg=2 (`0x080b126a`, `0x080b1380`); 按五项固定顺序调用 `get_first_placeable_monster_slot` 取首个可放置槽, 随后写 CID、槽状态和 selected internal CID 的特殊字段. |
| `0x080b135c` | `select_optimal_monster_placement_slot` | `populate_optimal_monster_placement_result` | indeg=2 (`0x080b142a`, `0x080b169c`); fifth argument 是 output, 成功与 fallback 都写 `result+0x18`; 调用者不把 r0 当作该评分字段. |
| `0x080b1400` | `select_activation_placement_slot` | `resolve_activation_placement_side` | indeg=3 (`0x080a97d2`, `0x080aa80e`, `0x080aafe0`); 前两级 callee 非 -1 时透传, 两级均为 -1 时比较 result `+0x14/+0x18` 返回 side 0/1. |

四项 rename 分别保持 Function IDs 5996/7167/7171/16765, 并保持 source/type/namespace, exact body ranges/SHA, signature/flags/params/return 和 incoming CORE6. fixer 以 TSV 的 `function_id` 字段为机器合同. 全部 9 个 BL source, 4 个 entry, registry, naming CSV 和四 inventory 的 name-only 投影见 `f14-seg8-function-projection-plan.json`.

### PLATE

- `F14-Seg-8.plates.tsv` 共 15 行: 段内 14 Function 加必要外部 caller `select_equip_placement_slot_with_score@0x080b153c`.
- 写入 full PLATE 14 行, PRESERVE `check_card_field_spell_equip_placeable@0x080b1458` 1 行. 全部新 PLATE 为 ASCII, 最大 439 chars.
- ABI 订正重点:
  - B0B64/B0B90 只消费 entry r0, 总是复制双方 5x0x14-byte blocks; r1 不选择 side.
  - B0BC0 用 `lsl/lsr #0x13` 取低 13-bit CID; field8 为0时调用 `check_field_spell_last_warrior_placeable`, 随后重新读取 field8. 只有 B0C2E gate 返回非零才清 field6 并把 field8 设为1; 其余拒绝路径不执行该写入.
  - B0C60 按固定五项优先序取首个可放置槽并写 CID/槽状态, 特殊路径覆盖两个 Maju Garzett ID 和未分配 CID `0x1388`.
  - B0FE8/B1078 写入 `gEquipLpScoreBase[0]` 的是 entry r0; slot filter 是低13-bit非零, 不是 bit9.
  - B1114 遍历 `gP1FieldArrayCBase` 的候选条目, 上界来自 `gP1ZoneHandCount`, 返回候选数组索引或 -1.
  - B135C 通过 output `+0x18` 交付 selected/fallback 值; 调用者不读取 r0 作为该评分.
  - B1400 具有六参数调用形态, 并透传两个资格 callee 的非 -1 返回.
- 外部 B153C 只做 B135C 新名投影与准确 caller 描述; Function name/body/signature/instructions保持.

## carve 计划 (R7)

无. 本段无 raw block, 也没有必要段外 carve.

## disasm 计划 (R4)

无. 1819 个 InstructionDB 地址、长度、raw bytes、TMode 和 source-format保持, 包括 160 个 `.hword`.

## 新增 constants / 全局

### `constants/card_info.inc`

- `KA_2_DES_SCISSORS_CID = 0x0000174a`.
- `SLOT_CARD_SET_CODE_CLEAR_MASK = 0xffffe000`.

### `constants/duel_field.inc`

- `FIELD_PLACEMENT_SCORE_SENTINEL_NEG_65536 = 0xffff0000`.
- `ZONE_SCORE_THRESHOLD_899 = 0x00000383`.

### `constants/ewram.inc`

- `gEquipZoneScoreEntryBase = 0x0201aff8`.
- `gEquipSpellZoneScoreValueBase = 0x0201b010`.
- `gEquipPlacementOccupiedZoneCount = 0x0201b16c`.
- `gEquipFieldSpellPlacementResult = 0x0201b18c`.

## §5.1 登记 (Rule 3)

无. 本段 raw block为0.

## 消费者证据 (R6)

| 地址 / 组 | 消费者证据 | 结论 | 置信度 |
|---|---|---|---|
| B04A8 | `asm/14_equip_ai_scoring.s:19117-19345` | 写 r3 指向的0x20-byte placement result, terminal returns均为0/1 | high |
| B06B4 | `asm/14_equip_ai_scoring.s:19387-20047`; calls B0F6C/B1052 | 排序候选并选择 result, 返回success bool | high |
| B0B64/B0B90 | `asm/14_equip_ai_scoring.s:20049-20096` | r0-only buffer ABI, 双方固定copy | high |
| B0BC0 | `asm/14_equip_ai_scoring.s:20097-20179` | 低13-bit CID, `check_field_spell_last_warrior_placeable`, field8 reload, 仅 B0C2E 非零路径清 field6/设 field8=1 | high |
| B0C60/masks | `asm/14_equip_ai_scoring.s:20180-20305`, callers B126A/B1380 | 固定五项优先序取首个可放置槽并写 CID/槽状态, selected internal CIDs 特殊路径 | high |
| B0D54/B0FE8/B1078 | `asm/14_equip_ai_scoring.s:20307-20808` | zone-score table构建及selector/evaluator返回链 | high |
| B1114 | `asm/14_equip_ai_scoring.s:20809-21103`, callers B0C262/B0C274 | 按 `gP1ZoneHandCount` 遍历 `gP1FieldArrayCBase` 4B候选条目, 返回候选数组索引或-1 | high |
| B135C | `asm/14_equip_ai_scoring.s:21105-21180`, callers B142A/B169C | fifth-arg output 的 `result+0x18` 交付 selected/fallback 值; callers不消费r0评分 | high |
| B1400 | `asm/14_equip_ai_scoring.s:21183-21228`, three phase callers | six-arg resolver及非-1 passthrough | high |
| 101 words | `F14-Seg-8.slots.tsv`, 114 exact PC READ refs_to | 每个自动word都有动作与消费者 | high |

## 求助

无.

## 落地边界

- 允许修改: 本段 Ghidra labels/equates/refs/EOL/13 PLATE/4 Function names, 外部 B153C PLATE, `constants/card_info.inc`, `constants/duel_field.inc`, `constants/ewram.inc`, registry/naming CSV/四 inventories 的批准投影, 以及 re-export 后 `asm/14_equip_ai_scoring.s` 对应名称/注释/word表达式.
- 禁止改变: 4244 ROM bytes, 1819 InstructionDB, 14 body ranges/SHA/Function IDs, padding, 101 source Data bytes/types, 114 PC READ refs, 5 existing source DATA CORE6, 其他 Function/模块语义.

## Executor Report: F14-Seg-8

- 槽: EQ=61 REF=40 (ADD=35, PRESERVE=5) RENAME=0 FUNC_RENAME=4 PLATE=15 rows / 14 writes (13 segment + 1 external), with B1458 preserved.
- carve=0 disasm=0 §5.1=0.
- 新增 constants/全局: 4 constants, 4 RAM globals.
- 求助: none.
- proposal: `doc/dev/refine/F14-Seg-8.proposal.md`.
