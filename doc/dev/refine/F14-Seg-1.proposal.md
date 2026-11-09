# Refine Proposal: F14-Seg-1  [0x080a78dc..0x080a8c30)

## 范围与冻结输入

- 正式段范围: `asm/14_equip_ai_scoring.s [0x080a78dc,0x080a8c30)`, 4948 bytes.
- 必要范围外闭包: `init_spell_activation_context@0x080a4058` 的完整 PLATE 和 `0x080a4094` call-name 投影; `asm/rom.s` 的 3 条现存 Thumb alias 重命名与 4 条新增 alias; registry, CSV, 四份 Function inventory.
- 根前态: `root-f14-independent-map-prestate.json`, `root-f14-seg1-supplement-prestate.json`, `root-f14-source-map.json`, `root-f14-module-layout-baseline.json`.
- DB 只读门禁: 两次 query 后 15 个物理 DB 文件 hash 全部不变.
- R4 独立编码门禁: `root-f14-seg1-r4-static-gate.json` PASS; canonical body 合同: `root-f14-seg1-body-contract.json`.
- 槽合同: `F14-Seg-1.slots.tsv`, 131 个当前 word 和 36 个 R4 新池逐项覆盖, 共 167 行.
- Function/PLATE 合同: `F14-Seg-1.plates.tsv`, 13 个段内 Function 加 1 个必要外部 caller, 共 14 行.

## 段测绘

### Function 入口, 13

| entry | current | final |
|---|---|---|
| `0x080a78dc` | `tick_equip_card_phase_by_7step_table` | `tick_lava_golem_tribute_selection_phase` |
| `0x080a7acc` | `check_equip_target_slot_in_active_table` | same |
| `0x080a7b78` | `tick_equip_phase_by_lp_index_range_c` | `tick_union_fusion_material_selection_phase` |
| `0x080a7f4c` | `tick_equip_card_phase_with_placement_apply` | `tick_three_tribute_summon_placement_phase` |
| `0x080a80a8` | `check_slot_equip_target_eligible` | `check_familiar_possessed_summon_slot_eligible` |
| `0x080a81fc` | `tick_equip_card_phase_by_activation_jump_table` | `tick_familiar_possessed_summon_phase` |
| `0x080a839c` | `check_equip_target_slot_eligible_by_field6_eq17` | `check_uria_tribute_slot_eligible` |
| `0x080a840c` | `check_equip_target_slot_eligible_by_field9_eq4_field6_eq16` | `check_hamon_tribute_slot_eligible` |
| `0x080a8478` | `check_equip_target_slot_eligible_by_whitelist_or_special` | `check_anteatereatingant_tribute_slot_eligible` |
| `0x080a84e0` | `check_equip_target_slot_by_composite` | `check_uria_hamon_anteatereatingant_tribute_slot_eligible` |
| `0x080a85d0` | `tick_equip_card_phase_by_12step_table` | `tick_uria_hamon_anteatereatingant_tribute_phase` |
| `0x080a87ec` | `tick_equip_phase_normal_summon_type` | same |
| `0x080a89f8` | `tick_equip_card_phase_with_summon_type_dispatch` | same |

### word 与 raw 块

- 当前 word: 131. 其中 107 个自动 word 槽, 24 个已有普通 switch words. 全部进入 slots TSV.
- `0x080a7928` 当前 `PTR_DAT_080a7928 = 0x08607cec` 实际是 little-endian Thumb bytes `ec 7c 60 08`; R4 后不再是 word.
- 三个 raw 块:
  - `[0x080a792c,0x080a7ac0)`, 404 bytes. 与 `0x080a7928` 的两条指令合并为 408-byte R4 输入.
  - `[0x080a8250,0x080a8394)`, 324 bytes.
  - `[0x080a862c,0x080a87e0)`, 436 bytes.
- 当前 code-unit 覆盖: 1540 InstructionDB / 3208 bytes; 131 4-byte Data words / 524 bytes; 1216 1-byte DataDB / 1216 bytes. 总计 4948 bytes, 无空洞和重叠.
- 当前 source 投影: 1540 instruction lines, 其中 1484 mnemonic 和 56 `.hword`; 26 个 `.zero 0x2`.

## 数据块分类, Rule 2/3

| 块 | full-ROM ref-scan | 内部闭包 | 判定 |
|---|---|---|---|
| `7928..7ac0`, 408B | 7 个真实 raw jump-table sources; 3 个资产偶合 | table at `790c..7928`, 8 code ranges, 15 pools, 5 pads | disasm |
| `8250..8394`, 324B | 6 个真实 raw jump-table sources | table at `8238..8250`, 5 code ranges, 10 pools, 3 pads | disasm |
| `862c..87e0`, 436B | 12 个 table source entries 总计: 5 个 sources 命中半开区间 `[0x080a862c,0x080a87e0)` 内的 5 个 unique targets; 另 7 个 sources 重复命中范围外既有 tail `0x080a87e0` | table at `85fc..862c`, 5 code ranges, 11 pools, 1 pad; 7 个外部 tail sources 不计入 R4 块内 sources | disasm |

完整 raw/THUMB|1 扫描在 `f14-seg1-refscan.tsv`.

真实入口命中:

- block 1 raw: `7928@790c`, `7958@7910`, `79d4@7914`, `79ec@791c`, `7a34@7918/7920`, `7abc@7924`.
- block 2 raw: `8250@8238`, `8262@8240`, `82d8@823c/8244`, `835e@8248`, `8390@824c`.
- block 3 raw: `862c@85fc`, `863e@8604`, `8698@8600`, `8750@8624`, `87dc@8628`. 7 个表项保持指向已有 tail `0x080a87e0`.

资产偶合原始命中保持:

- raw `0x080a79d6` at ROM `0x0871f55a` = `data/card-image-tiles.s:455`, `tb0449.bin+0xc5a`.
- raw `0x080a7a18` at ROM `0x088d4fdd` = `data/card-image-tiles.s:829`, `tb0823.bin+0x25d`.
- THUMB `0x080a7a3d` at ROM `0x08846db9` = `data/card-image-tiles.s:707`, `tb0701.bin+0xfb9`.

三项位于压缩卡图 tile bytes, 不对应 code/data consumer. 三块均有真实 jump-table 引用和完整可达控制流, 所以没有 carve 或 Section 5.1 项.

## disasm 计划, R4

### 完整布局

`f14-seg1-r4-map.json` 冻结每条指令的 address, length, ROM little-endian `raw_bytes`, objdump opcode, mnemonic, operands, direct-flow, call, PC literal consumer, pool 和 padding. `raw_bytes` 是落地字节权威; objdump opcode 仅保留显示半字.

总计:

- 482 instructions / 1006 code bytes.
- 36 literal words / 144 bytes.
- 9 padding halfwords / 18 bytes.
- 54 direct flows, 其中 21 calls.
- 39 PC literal reads.
- R4 输入覆盖 1168 bytes = 1006 + 144 + 18.

Block 1 code ranges:

`[7928,797a), [7988,79d0), [79d4,79e8), [79ec,7a12), [7a20,7a2a), [7a34,7a7e), [7a90,7ab6), [7abc,7ac0)`.

Pools: `797c,7980,7984,79d0,79e8,7a14,7a18,7a1c,7a2c,7a30,7a80,7a84,7a88,7a8c,7ab8`.
Pads: `797a,7a12,7a2a,7a7e,7ab6`.

Block 2 code ranges:

`[8250,8288), [8294,82ce), [82d8,8346), [8358,838a), [8390,8394)`.

Pools: `8288,828c,8290,82d0,82d4,8348,834c,8350,8354,838c`.
Pads: `82ce,8346,838a`.

Block 3 code ranges:

`[862c,8664), [8670,8690), [8698,8702), [8718,87d8), [87dc,87e0)`.

Pools: `8664,8668,866c,8690,8694,8704,8708,870c,8710,8714,87d8`.
Pad: `8702`.

### Function body canonical contract

- `0x080a78dc`: old 48B -> final 386B. Canonical ranges:
  `[78dc,7902),[7928,797a),[7988,79d0),[79d4,79e8),[79ec,7a12),[7a20,7a2a),[7a34,7a7e),[7a90,7ab6),[7abc,7aca)`.
  Final body SHA256 `07bb58bf2129ef0d3bdc0433cc0fdfee4f7f8edba08a3d35de304ea1f3803e98`.
- `0x080a81fc`: old 58B -> final 336B. Canonical ranges:
  `[81fc,8210),[8214,8232),[8250,8288),[8294,82ce),[82d8,8346),[8358,838a),[8390,839c)`.
  Final body SHA256 `bf9ec01f1b77d3a92cadfc8fdb9190dead7c138485bf2304ffb0e758ac13d9b1`.
- `0x080a85d0`: old 46B -> final 436B. Canonical ranges:
  `[85d0,85f4),[862c,8664),[8670,8690),[8698,8702),[8718,87d8),[87dc,87ea)`.
  Final body SHA256 `5d6fbc130171b8ac555eb617fdcc028a4ed11885d0563e41a800f2c0cf1734e9`.

Function ID, entry, signature, namespace, flags and existing body fragments remain unchanged. Only the three listed Functions extend their AddressSet.

### switch source/target contract

- 25 source words preserve raw value, 4-byte Data and each existing DATA reference CORE6: from, to, type, source, operand, primary.
- The 25 source words resolve to 17 total unique targets: 16 new R4 code targets plus the existing tail `0x080a87e0`. All 17 currently use dynamic DEFAULT labels. Final materializes exactly one USER_DEFINED Global primary label at each target; dynamic target Symbol ID may change. No same-address alias is retained or added.
- The three table-base labels are `lava_golem_phase_jump_table@790c`, `familiar_possessed_phase_jump_table@8238`, and `uria_hamon_anteater_phase_jump_table@85fc`.
- `7908/8234/85f8` become REF slots to these bases.
- `7928` loses current `PTR_DAT`, /dword Data, and bogus `7928->08607cec` DATA ref. Its incoming `790c->7928` switch reference remains and resolves to `lava_golem_phase_case_0`.
- All source refs, target prestates, final labels, and ID rules are explicit in slots TSV.

## 符号化计划, R1/R2/R3

Action totals across 167 rows:

- EQ = 63: `EQ_ADD=61`, `EQ_PRESERVE=2`.
- REF = 77: `REF_ADD=64`, `REF_PRESERVE=13`.
- RENAME = 1.
- TABLE_ENTRY_MATERIALIZE = 25.
- DISASM_WORD_TO_CODE = 1.

### EQ_SLOTS

主要复用组:

- `PLAYER_BLOCK_STRIDE`: 8 current slots.
- `EQUIP_CRITERIA_DISPLAY_ARR_OFF`: 8 current slots.
- `EQUIP_CRITERIA_TARGETED_FLAG_OFF`: 3 current slots.
- `ELIGIB_SPRITE_CTRL_OFF / ELIGIB_ANIM_STATE_OFF / LP_BANISHER_CTX_OFF`.
- `slot_field_mask_ffff803f`.
- 已有 CIDs: XZ, YZ, VW, VWXYZ, Y Dragon Head, V-Tiger Jet, XYZ, Light of Intervention, Hamon, Anteatereatingant, Elemental HERO Necroshade, Ancient Gear Castle.
- `CHARMER_RANGE_MAX_CID` is reused for `0x18c2`.

Thumb callbacks:

- current `7d38/7d44 = check_equip_target_slot_in_active_table+1`.
- current `8b30/8b70` preserve existing `check_ancient_gear_castle_counter_slot_requirement_1`.
- new `7a1c/7a2c = check_equip_target_slot_eligible_by_monster_space+1`.
- new `8290/82d0 = check_familiar_possessed_summon_slot_eligible+1`.
- new `866c/8690 = check_uria_hamon_anteatereatingant_tribute_slot_eligible+1`.

GAS uses `fn+1` aliases with identical raw odd values. Ghidra equates use the alias name on the even source word. No label, Data or ref is created at any odd target address.

### REF_SLOTS

| target | current | new R4 pools | target ID |
|---|---:|---:|---:|
| `gEquipZoneRankState` | 22 | 14 | 33146 |
| `gP1LifePoints` | 12 | 5 | 15545 |
| `gDuelCardCtxBase` | 5 | 4 | 18879 |
| `gDuelFieldSlots` | 6 | 0 | 20369 |
| `gDuelPhaseFlags` | 4 | 0 | 25230 |
| `gP1HandSlotArray` | 2 | 0 | frozen in TSV |
| three jump-table bases | 3 | 0 | dynamic target materialization |

The 13 existing DATA refs are preserved exactly: 12 target `gP1LifePoints`, and `0x080a8234 -> 0x080a8238` targeting the familiar-possessed table base. For `0x080a8234`, source Data and reference CORE6 remain exactly `from=080a8234`, `to=080a8238`, `type=DATA`, `source=DEFAULT`, `operand=0`, `primary=true`; no duplicate reference is added and the source reference is not upgraded. Only derived `target_primary_id/name` may change when the dynamic DEFAULT target becomes the approved USER_DEFINED table-base primary. New refs are operand-0 USER DATA refs. RAM target bytes remain `null`; no uninitialized EWRAM bytes are read.

### RENAME_SLOTS

- `0x080a8060 = 0x00000123` -> `placement_failure_display_op_id_080a8060`.
- EOL: `Display operation 0x0123 used after placement activation failure.`
- Consumer: `asm/14_equip_ai_scoring.s:779-780@0x080a8038`.
- No equate or DATA ref is added.

## 新增 constants / globals

### constants/card_info.inc

```asm
.equ FAMILIAR_POSSESSED_ERIA_CID, 0x0000196c
.equ FAMILIAR_POSSESSED_HIITA_CID, 0x0000196d
.equ AUSSA_THE_EARTH_CHARMER_CID, 0x000018bf
.equ HIITA_THE_FIRE_CHARMER_CID, 0x000018c1
```

每项由 `cards-ids-array.s` 的 logical slot/icid, `card-stats.s` name, `card-passcodes.s` password 和 `data.md` logical CID 四类结构化字段闭合. 精确行见 `f14-seg1-card-routing-evidence.json`. 当前 constants 无同名或同语义 equate.

### constants/duel_field.inc

```asm
.equ EQUIP_CRITERIA_DISPLAY_THIRD_OFF, 0x000005b4
.equ EQUIP_SELECTED_SLOT_ARRAY_OFF,    0x000005c4
```

- `0x5b4 = EQUIP_CRITERIA_DISPLAY_ARR_OFF + 8`; `0x080a7c44..7c4a` writes the third fusion-material display CID.
- `0x5c4` is the selected-slot array base; `0x080a7e7a..7eaa` iterates it while the count resides at `gDuelPhaseFlags+0x5c0`.

### asm/rom.s aliases

Add:

```asm
.equ check_equip_target_slot_in_active_table_1, check_equip_target_slot_in_active_table+1
.equ check_equip_target_slot_eligible_by_monster_space_1, check_equip_target_slot_eligible_by_monster_space+1
.equ check_familiar_possessed_summon_slot_eligible_1, check_familiar_possessed_summon_slot_eligible+1
.equ check_uria_hamon_anteatereatingant_tribute_slot_eligible_1, check_uria_hamon_anteatereatingant_tribute_slot_eligible+1
```

Rename the three existing aliases at current `rom.s:97-99` to the final Uria, Hamon, and Anteatereatingant predicate names. Their file13 source-word expressions follow the same projection and preserve values `0x080a839d/840d/8479`.

## FUNC_RENAME, 10

| entry | ID | old | new | routing evidence |
|---|---:|---|---|---|
| `78dc` | 16938 | `tick_equip_card_phase_by_7step_table` | `tick_lava_golem_tribute_selection_phase` | hub `8f48`, CID `1578` |
| `7b78` | 16748 | `tick_equip_phase_by_lp_index_range_c` | `tick_union_fusion_material_selection_phase` | hub `8f4e`, CIDs `15b1/15b4/15f9/15fa` |
| `7f4c` | 16749 | `tick_equip_card_phase_with_placement_apply` | `tick_three_tribute_summon_placement_phase` | hub `8f54`, CIDs `13b5/154b` |
| `80a8` | 2077 | `check_slot_equip_target_eligible` | `check_familiar_possessed_summon_slot_eligible` | CID-to-Charmer mapping `196b..196e -> 18bf..18c2` |
| `81fc` | 16939 | `tick_equip_card_phase_by_activation_jump_table` | `tick_familiar_possessed_summon_phase` | hub `8e9c`, CIDs `196b..196e` |
| `839c` | 16750 | field6 generic name | `check_uria_tribute_slot_eligible` | caller `84e0` selects only CID `19a3` |
| `840c` | 16751 | field9/field6 generic name | `check_hamon_tribute_slot_eligible` | caller `84e0` selects only CID `19a4` |
| `8478` | 16752 | whitelist/special generic name | `check_anteatereatingant_tribute_slot_eligible` | caller `84e0` selects only CID `19c8` |
| `84e0` | 16753 | `check_equip_target_slot_by_composite` | `check_uria_hamon_anteatereatingant_tribute_slot_eligible` | three explicit CID branches |
| `85d0` | 16940 | `tick_equip_card_phase_by_12step_table` | `tick_uria_hamon_anteatereatingant_tribute_phase` | hub `8f78`, CIDs `19a3/19a4/19c8` |

Card names, passwords, logical CID rows and dispatcher calls are frozen in `f14-seg1-card-routing-evidence.json`.

### name projection contract

- `asm/14_equip_ai_scoring.s`: update 10 Function labels, hub calls at `8e9c/8f48/8f4e/8f54/8f78`, internal calls at `85a6/85b2/85be`, R4 callback expressions, and rewritten PLATE text only. Opcodes remain unchanged.
- `asm/13_equip_placement.s`: update `0x080a4094` call to the Familiar-Possessed predicate and rewrite only the `init_spell_activation_context@4058` PLATE. Update the three existing callback word expressions for `839c/840c/8478`; raw odd words remain unchanged.
- `asm/rom.s`: apply the alias contract above.
- `naming-proposals.csv`: replace name column only for the 10 renamed addresses; other columns and the 3 unchanged segment rows remain.
- `RenameKnownFunctions.py`: UPDATE existing tuples at `7b78` and `80a8`; ADD missing tuples for the other 8 renamed Functions and unchanged `7acc/87ec/89f8`; update existing `4058` tuple PLATE only.
- Refresh `temp/ghidra-functions.csv`, `temp/ghidra-functions-renamed.txt`, `temp/ghidra-functions-auto.txt`, and `temp/ghidra-functions-summary.md`.
- Function IDs, namespaces, signatures, flags, incoming call objects and all non-R4 body bytes stay fixed. Exact current and final metadata are in plates TSV.

## PLATE, 14

- 10 renamed Functions receive full ASCII PLATE rewrites.
- `87ec` and `89f8` receive full ASCII PLATE rewrites to remove stale automatic-token descriptions while preserving names and bodies.
- External caller `4058` receives one full ASCII PLATE rewrite because its old PLATE names `check_slot_equip_target_eligible`.
- `7acc` retains its existing accurate 673-char ASCII PLATE with no write. It is not rewritten solely for length.
- 13 new PLATE writes are ASCII, each <=500 chars; maximum is 449 chars.
- Existing Function EOL arrays are empty and remain empty.
- Full text, current chars/hash, Function metadata, incoming refs, and registry/CSV/inventory contracts are in `F14-Seg-1.plates.tsv`.

## carve 计划, R7

none.

## 消费者证据, R6

| semantic | consumer | conclusion | confidence |
|---|---|---|---|
| Lava Golem phase | hub `asm/14_equip_ai_scoring.s:2462@8f48`; R4 block 1 | sole card route CID `1578`; two-slot selection through monster-space predicate | high |
| Union fusion phase | hub `2465@8f4e`; body `7be0..7d08` | explicit XZ/YZ/VW/VWXYZ/Y-Head/V-Tiger/XYZ material CIDs | high |
| three-tribute placement | hub `2468@8f54`; body `7f7a..8060` | Moisture/Gilford routes, >2 placement gate, Light of Intervention, placement activation | high |
| Familiar-Possessed predicate | `asm/13_equip_placement.s:14593@4094`; body `80f2..8148` | active CID `196b..196e` maps to matching Charmer `18bf..18c2` | high |
| Familiar-Possessed phase | hub `2370@8e9c`; R4 block 2 | six-phase selection calls the renamed predicate through two odd callback words | high |
| Uria/Hamon/Anteater predicates | body `8572..85be`; R4 block 3 callbacks | exact CID dispatch to three dedicated predicates | high |
| shared tribute phase | hub `2486@8f78`; R4 block 3 | Uria/Hamon collect three; Anteatereatingant compares CID `19c8` for two-target flow | high |
| new `5b4` offset | `asm/14_equip_ai_scoring.s:254-257@7c44` | third material CID at display array base + 8 | high |
| new `5c4` offset | `asm/14_equip_ai_scoring.s:546-571@7e7a` | selected-slot array iterated against count at +5c0 | high |
| all 167 words | `F14-Seg-1.slots.tsv` | each row gives source file:line/address, full refs/equates/EOL prestate, action and confidence | high |

## 最终门禁预期

- Segment remains 4948 bytes and 13 Functions. Global Function count remains unchanged.
- InstructionDB: `1540 + 482 = 2022`, 4214 bytes.
- Source instruction projection: 1966 mnemonic plus 56 `.hword`.
- 4-byte Data words: `131 - 1 + 36 = 166`, 664 bytes.
- Padding/one-byte Data: existing 52 bytes + new 18 bytes = 70 bytes. Expected final DataDB: 236 units / 734 bytes.
- `2022 InstructionDB` byte coverage + `166 words` + `70 padding bytes` = 4948 bytes.
- Three raw blocks are eliminated. All 107 old automatic word slots are resolved; `7928` becomes code; all 36 new pools are USER-labeled Data.
- 54 direct-flow set, 39 PC-read set, 25 switch source refs, 17 total unique case targets (16 new R4 targets plus existing tail `0x080a87e0`) and three canonical Function body hashes match the frozen evidence.
- No residual `DAT_/DWORD_/PTR_DAT_/UNK_` data symbol remains in the segment. Ordinary `LAB_` control-flow labels are allowed.
- New slot EOL and written PLATE text are ASCII.
- Landing then runs export, mode injection, split, build, byte-identical ROM verification, source-scope verification and DB invariant checks.

## Section 5.1 登记

none.

## 求助

none.

## Executor Report: F14-Seg-1

- Slots: EQ=63 REF=77 RENAME=1 TABLE=25 DISASM_WORD=1 FUNC_RENAME=10 PLATE=14.
- carve=0, disasm=18 code ranges / 1006 code bytes, Section 5.1=0.
- New constants: 4 card CIDs, `EQUIP_CRITERIA_DISPLAY_THIRD_OFF`, `EQUIP_SELECTED_SLOT_ARRAY_OFF`.
- New GAS aliases: 4; renamed existing aliases: 3.
- Help: none.
- proposal: `doc/dev/refine/F14-Seg-1.proposal.md`.

