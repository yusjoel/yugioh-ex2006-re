# Refine Proposal: F15-Seg-2 [0x080b6c08,0x080b79f8)

## 范围与冻结输入

- 模块: `asm/15_equip_target_summon_zoom.s`.
- 段范围: `[0x080b6c08,0x080b79f8)`, 3568 bytes.
- 当前段前态: `root-f15-seg2-initial-baseline.json` SHA256 `d6cfb29eade5a2ef8ceb904e108723f56a8ca264687eb73fbba2724d23281945`.
- 当前全模块前态: `root-f15-seg1-independent-post.json` SHA256 `f8698e9566a5c2e8b0bc507da5af39db7d96620c4cfa769e86e8fff8515f4cc0`.
- 源码基线: `root-source-baseline-f15seg2.json`, 145 files, SHA256 `1679b6ff8a9d1f320798455ef45d20642602eace3ce208a1a62fe0d08f006c44`.
- DB 基线: `root-f15-seg2-db-backup.json`, 15 physical files, SHA256 `9a7a37336910d5c839d9f63c708403c5205f9fbc3546fd34e6f241eea8d835e1`.
- Executor 只读补查: `f15-seg2-supplement-prestate.json` SHA256 `bafa66b3cd4eb41b0af47db3a7b86303e57ab374d6e12f6ebd565ebfca901c66`; DB gate SHA256 `86c6781fed75614c63c199e0e5596e7d0a9bb26c7fb4bd5b17300c74409de056`, 15 files unchanged.
- Root 独立扩展前态: `root-f15-seg2-independent-full-prestate.json` SHA256 `a30835f56810b84b7c044e145bbb7444984faad45302fbb8bc2f61a67ef61f88`; 118 Function records, 1264 module words, 3190 states, 49408 module bytes. `root-f15-seg2-independent-full-prestate-gate.json` SHA256 `d85b522f133d806c1d4ef274f4fcaf61a7a5bc1e182af83c2699e2e199e781b4` confirms the physical DB gate.
- 本提案仅定义落地合同. 本阶段不修改 Ghidra, 正式源码, constants, CSV, inventories, 进度文档或构建产物.

## 段测绘

### Function 入口

| Entry | Current name | Final name | Final body bytes | Source line |
|---|---|---|---:|---:|
| 0x080b6c08 | `commit_equip_target_slot_by_card_id` | same | 958 | 3448 |
| 0x080b706c | `build_slot_bitmap_by_predicate` | same | 64 | 4078 |
| 0x080b70ac | `select_equip_target_slot_by_card_id` | same | 772 | 4115 |
| 0x080b740c | `scan_hand_and_field_cards_for_equip_activation` | same | 598 | 4600 |
| 0x080b76a4 | absent | `return_true_response_callback` | 4 | 4944 |
| 0x080b76a8 | `check_opponent_effect_node_active` | same | 30 | 4954 |
| 0x080b76c8 | `check_self_effect_node_active` | same | 26 | 4980 |
| 0x080b76e4 | `check_card_pair_slot_count_eligible` | `check_card_pair_slot_count_below_requirement` | 54 | 5009 |
| 0x080b771c | `check_effect_handler_result_nonzero` | `check_effect_handler_result_positive` | 40 | 5049 |
| 0x080b7744 | `check_hand_equip_target_available_for_zone` | same | 26 | 5076 |
| 0x080b7760 | `check_self_effect_node_active_b` | `check_self_effect_node_inactive` | 26 | 5100 |
| 0x080b777c | `check_effect_zone_available_from_zone_ptr` | same | 16 | 5117 |
| 0x080b778c | `check_dark_room_activation_slots_available` | same | 72 | 5139 |
| 0x080b77dc | `check_zone_score_advantage_for_self` | same | 26 | 5186 |
| 0x080b77f8 | `check_self_lp_advantage_by_500_margin` | `check_opponent_lp_below_self_plus_500` | 56 | 5216 |
| 0x080b7838 | `check_opponent_equip_count_exceeds_one` | same | 30 | 5261 |
| 0x080b7858 | `check_opponent_equip_whitelist_cards_present` | same | 30 | 5280 |
| 0x080b7878 | `check_premature_burial_or_coth_equip_eligible` | same | 158 | 5320 |
| 0x080b7934 | `check_equip_activation_valid_under_level_restriction` | same | 174 | 5415 |

### 完整布局

- Before: 1496 InstructionDB starts = 1422 mnemonic + 74 typed `.hword`; 3156 instruction bytes, 87 four-byte words = 348 bytes, one 4-byte raw leaf, and 60 padding bytes. Total `3156 + 348 + 4 + 60 = 3568`.
- After R4: 1498 InstructionDB starts = 1424 mnemonic + 74 typed `.hword`; 3160 instruction bytes, 87 words, no raw byte, and 60 padding bytes. Function count rises from 18 to 19.
- All 74 `.hword` rows remain InstructionDB. All 18 current Function bodies, body hashes and ownership remain exact.
- Current words: 87 automatic definitions. Types and every old reference/equate/comment are frozen in `F15-Seg-2.slots.tsv`.
- Slot action counts: `EQ_ADD=65`, `REF_ADD=10`, `REF_PRESERVE=9`, `THUMB_REF_ADD=3`. Every old word appears once.
- Exact byte coverage and new leaf body: `f15-seg2-layout-map.json` and `f15-seg2-r4-plan.json`.

## 数据块分类 (Rule 2/3)

| Block | ref-scan | Classification | Evidence |
|---|---|---|---|
| `[0x080b76a4,0x080b76a8)` 4 bytes | even `0x080b76a4`=0; Thumb `0x080b76a5`=201 | R4 disasm + Function create | Bytes `01207047` decode as `movs r0,#1; bx lr`. The 201 odd words are runtime callback fields in seven proven stride-8 response tables. |
| `[0x09e481e8,0x09e491c0)` external host slice | six base consumers; 504 affected rows and one independent 3-row table | R7 carve five affected tables; preserve 3-row gap raw | Consumer loops use inclusive bounds 56, 164, 2, 4, 206 and 69. `try_activate_equip_for_matching_slot` loads row+4 and invokes it as a callback. |

- Whole-ROM sliding scan of the raw leaf gives exactly 201 `0x080b76a5` holders across seven tables: 79 in the two prior normal-summon tables and, in address order, 9 / 37 / 2 / 54 / 20 in the five affected external tables. Even raw holders are zero. The source list is frozen in `f15-seg2-r4-plan.json`.
- Six adjacent external tables are `[09e481e8,09e483b0)` 57 rows, `[09e483b0,09e488d8)` 165, `[09e488d8,09e488f0)` 3, `[09e488f0,09e48918)` 5, `[09e48918,09e48f90)` 207, and `[09e48f90,09e491c0)` 70. BB312 / BB380 / BB3A8 / BB3CE / BB43A / BBA06 prove inclusive maxima 56 / 164 / 2 / 4 / 206 / 69 with stride 8. BB3B0 is evidence-only for the protected three-row table. BB400 drives the 207-row loop ending at BB40A and calls `check_normal_summon_eligible_for_slot`; BB488 is the distinct `try_activate_equip_for_matching_slot` path. BAEE0 reads row+0, while BAFBC loads row+4 and BAFC2 calls it indirectly. Root evidence: `root-f15-seg2-external-table-structure.json` SHA256 `44fa70723cc802a026f307d69b3345cf0edd2c701fe7f217bba739f47e0db0c5`.
- Five affected tables contain 504 rows and 1008 words. Callback classes are 115 rows to 24 current Functions, 122 rows to the new leaf, and 267 rows to 133 later raw entries. The 3-row table is not changed.
- The 267 future rows are partitioned exactly: Seg3 64 rows / 38 targets, Seg4 202 / 94, Seg5 1 / 1. Evidence: `root-f15-seg2-future-callback-handoff-leads.json` SHA256 `cec06d6803e6ce3b8bdf1304df59137d4cde1e769202a364e0ebb180ab3a493a`.
- No raw block qualifies for Section 5.1.

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS

- `EQ_ADD=65`. The TSV freezes address, old name, original bytes/value/type, symbols, refs_from, refs_to, current Equates, Function owner, final label, exact expression and EOL.
- The 65 bindings use 52 exact names: 57 rows reuse 44 existing domain-correct names, while eight rows create `ANTI_AIRCRAFT_FLOWER_CID`, `BEAST_SOUL_SWAP_CID`, `CATAPULT_TURTLE_CID`, `EQUIP_LEVEL_RESTRICTION_SCORE_THRESHOLD_2399`, `HADE_HANE_CID`, `LIGHT_OF_JUDGMENT_CID`, `MAGICAL_DIMENSION_CID`, and `ULTIMATE_BASEBALL_KID_CID`.
- `CATAPULT_TURTLE_CID` does not reuse same-valued `SCENE_SLOT_MASK_LO`; the consumer is an internal-CID dispatch, while the existing name belongs to the scene-mask domain.
- All source words retain their current Data type and READ refs. Each new scalar Equate is operand 0 and the source label becomes USER.

### REF_SLOTS

- `REF_ADD=10` adds USER DATA refs for current pointer words targeting existing USER globals: `gDuelPhaseFlags`, `gEquipLpScoreBase`, `gDuelFieldSlots`, and `gP1FieldArrayCBase`.
- `REF_PRESERVE=9` preserves existing `gP1LifePoints` DATA refs, including exact type, source, operand and primary flags. No delete/recreate or source upgrade is allowed.
- Every static target retains its existing USER Symbol ID, namespace, Data type and incoming refs. `target_prestate_json` in the TSV freezes the complete target state.

### Thumb callback source words

- `THUMB_REF_ADD=3`: `0x080b701c -> find_evolution_target_for_equip_slot_card+1`, `0x080b7234 -> score_slot_by_field5_and_zone_bounds+1`, and `0x080b727c -> classify_equip_target_slot_score_tier+1`.
- Each source receives a scoped odd-value Equate and an auxiliary USER DATA ref to the even Function entry. The ROM value is unchanged.
- No Symbol, Data unit or reference is created at an odd address. Existing PARAM/ANALYSIS odd-target display metadata is preserved.

### External table words

- The five affected tables define 1008 word sources: 504 CID words and 504 callback words.
- Before: 998 words are implicit DataDB, eight are `/dword`, and two are `/undefined4`. Landing creates `/dword` only for the 998 implicit words and preserves the ten defined types exactly.
- All 1008 sources get one stable USER source label. The first CID word at each table start uses the table label as its sole primary label; no same-address alias is added.
- All callback GAS expressions are `<Function>+1` or `pending_card_response_callback_<addr>+1`, exactly equal to the original odd word.
- 237 new-table rows receive an auxiliary even DATA ref: 115 to current Functions and 122 to the new leaf. The 267 future-raw rows receive no target mutation or even ref.
- The prior 79 normal-summon leaf words replace `pending_normal_summon_callback_080b76a4+1` with `return_true_response_callback+1`, add even DATA refs, and replace the old Equate binding. All existing source labels, `/dword` types, bytes and unrelated metadata remain exact.
- Four prior normal-summon words for `0x080b7760` replace only the old odd Equate/expression name; their DATA CORE6 is preserved.
- Global Equate delta: 213 affected final names receive 661 exact operand-0 binding additions. The B771C rename migrates six old plus fifteen new bindings from `check_effect_handler_result_nonzero_1` to `check_effect_handler_result_positive_1`. Remove three zero-reference old names, create 168 names, reuse 45 names, and end with 2417 global Equates. Exact name/value/reference multisets are in `f15-seg2-global-equate-plan.json`.

### RENAME_SLOTS

- Pure label-only rows: 0.
- Every current automatic word is covered by one TSV action. Existing `/pointer` and `/dword` types remain exact.

### FUNC_RENAME

| Entry | Old | New | Evidence | Current direct indeg |
|---|---|---|---|---:|
| 0x080b76e4 | `check_card_pair_slot_count_eligible` | `check_card_pair_slot_count_below_requirement` | `asm/15_equip_target_summon_zoom.s:5009-5041`: returns 1 for count<=1 when type<=10 and count<=0 when type>10. | 2 |
| 0x080b771c | `check_effect_handler_result_nonzero` | `check_effect_handler_result_positive` | `asm/15_equip_target_summon_zoom.s:5049-5074`: B7736-B773A returns 1 only for a signed handler result greater than zero. | 2 BL + 6 old DATA + 15 new DATA |
| 0x080b7760 | `check_self_effect_node_active_b` | `check_self_effect_node_inactive` | `asm/15_equip_target_summon_zoom.s:5100-5115`: returns 1 exactly when activation count is zero. | 4 DATA before; 12 DATA after |
| 0x080b77f8 | `check_self_lp_advantage_by_500_margin` | `check_opponent_lp_below_self_plus_500` | `asm/15_equip_target_summon_zoom.s:5216-5254`: returns 1 for `opponent_lp < self_lp + 500`. | 0 before; 1 DATA after |

Rename closure:

- Preserve each Function ID, USER source, Global namespace, body ranges/SHA, signature, flags, parameters and return metadata.
- Whole-ROM unaligned holds are exact in `f15-seg2-name-reference-baseline.json`: B76E4 odd=26/even=0, B7760 odd=12/even=0, B77F8 odd=1/even=0.
- B76E4 direct calls at `0x080b7f6a` and `0x080bad80` project the new name. Their two caller PLATEs are fully rewritten within the 500-character limit.
- B771C direct calls at `0x080b3408` and `0x080b485e` project `check_effect_handler_result_positive`; six old and fifteen new odd expressions project the same name with `+1`. The B4850 caller PLATE is fully rewritten. Function ID 16011 and every reference CORE6 remain exact.
- B7760 projects four prior normal-summon expressions and eight new external-table expressions to `check_self_effect_node_inactive+1`.
- B77F8 projects its one new external-table expression to `check_opponent_lp_below_self_plus_500+1`.
- Update only the name field in `doc/dev/naming-proposals.csv`, `temp/ghidra-functions.csv`, and `temp/ghidra-functions-renamed.txt` for the four renames. Add exact tuples to `tools/ghidra-labeling/RenameKnownFunctions.py`. The created Function adds one CSV/renamed row and updates summary counts; `temp/ghidra-functions-auto.txt` remains content-identical. Legacy `tools/ghidra-labeling/ghidra-functions.*` inventory snapshots and historical eval documents remain byte-exact.

### PLATE

- `F15-Seg-2.plates.tsv` contains 22 full ASCII PLATE writes: 18 current segment Functions, one created Function, and three necessary external caller projections (B4850, B7F64, BAD6C). Every final PLATE is at most 500 characters.
- Key corrections:
  - `0x080b6c08`, `0x080b70ac`, and `0x080b740c` commit target refs and return through saved LR in r0; they have no semantic return value.
  - `0x080b76e4` and both callers describe the below-requirement result polarity.
  - `0x080b7760` describes zero active nodes, not active-node presence.
  - `0x080b771c` tests the signed handler result strictly greater than zero; the name is projected through both direct calls, 21 odd table expressions, and B4850.
  - `0x080b778c` always uses the fixed Dark Room CID; the first nonzero count returns 1 immediately, and only a zero first count reaches the two-count zero-sum fallback.
  - `0x080b7934` rejects zero opponent active equips, has two explicit early-accept count branches, then requires the remaining card/precondition gates, score >= opponent LP or score >2399, and a positive final comparison.
  - `0x080b7f64` requires the signed chain-field count result strictly greater than zero. `0x080bad6c` tests bit7 in the parallel state dword at slot base +0x10, not the CID word.
  - `0x080b77f8` states the exact LP inequality.
  - `0x080b7878` states all success paths, including the missing-pair and Sangan/Witch cases.
- PLATE writes preserve Function body, identity, signature and all EOL comments. Only approved incoming DATA refs and rename-derived target names change.

## 新增 constants / 全局

All eight absent Ghidra names become new scalar Equate objects. Only three require new GAS definitions; five reuse same-named, same-valued definitions already present in `constants/card_info.inc`:

| Name | Value | GAS action | Structured evidence |
|---|---:|---|---|
| `ANTI_AIRCRAFT_FLOWER_CID` | 0x00001702 | add definition | cards-ids-array:1900; card-stats:19073; card-passcodes:1488; data.md:1446 |
| `BEAST_SOUL_SWAP_CID` | 0x00001889 | reuse `constants/card_info.inc:1792` | cards-ids-array:2291; card-stats:23415; card-passcodes:1822; data.md:1779 |
| `CATAPULT_TURTLE_CID` | 0x00000fff | add definition | cards-ids-array:105; card-stats:1276; card-passcodes:119; data.md:102 |
| `EQUIP_LEVEL_RESTRICTION_SCORE_THRESHOLD_2399` | 0x0000095f | add definition | `asm/15_equip_target_summon_zoom.s:5483-5485`; score <=0x095f fails |
| `HADE_HANE_CID` | 0x000017ec | reuse `constants/card_info.inc:1640` | cards-ids-array:2134; card-stats:21556; card-passcodes:1679; data.md:1637 |
| `LIGHT_OF_JUDGMENT_CID` | 0x00001764 | reuse `constants/card_info.inc:1771` | cards-ids-array:1998; card-stats:20152; card-passcodes:1571; data.md:1529 |
| `MAGICAL_DIMENSION_CID` | 0x00001678 | reuse `constants/card_info.inc:1485` | cards-ids-array:1762; card-stats:17552; card-passcodes:1371; data.md:1329 |
| `ULTIMATE_BASEBALL_KID_CID` | 0x000017e1 | reuse `constants/card_info.inc:994` | cards-ids-array:2123; card-stats:21413; card-passcodes:1668; data.md:1626 |

- Exact evidence and domain decisions: `f15-seg2-constant-evidence.json`.
- New Function: `return_true_response_callback` at `0x080b76a4`, dynamic USER Function ID, exact body `[080b76a4,080b76a8)`, 201 incoming DATA refs.
- New odd Equate names and bindings are specified by `f15-seg2-global-equate-plan.json`. Odd addresses remain without USER symbols or Data.

## carve 计划 (R7)

- Current host: `asm/rom.s:1567`, `.incbin "roms/2343.gba", 0x1e481e8, 0x1b24`, range `[09e481e8,09e49d0c)`.
- Replace its prefix with `.include "asm/equip_activation_response_tables.inc"` covering `[09e481e8,09e491c0)`, 4056 bytes.
- The tracked include contains five structured tables and preserves `[09e488d8,09e488f0)` as a byte-exact independent 3-row raw table.
- Preserve suffix `[09e491c0,09e49d0c)` as `.incbin "roms/2343.gba", 0x1e491c0, 0xb4c`.
- Preserve host start/end and every ROM byte. Do not place the new include under ignored `data/`.
- Six later affected-table base literal sources `0x080bb340`, `0x080bb378`, `0x080bb3d8`, `0x080bb400`, `0x080bb488`, and `0x080bbb28` are evidence only and remain completely unchanged for their owning later segments. Evidence-only `0x080bb3b0` identifies the protected three-row table and also remains exact.
- `f15-seg2-external-table-carve-plan.json` is the complete per-word, per-row and bookend contract.

## disasm 计划 (R4)

- Clear only implicit units `[0x080b76a4,0x080b76a8)`, set TMode=1 across the exact four bytes, and disassemble starts `0x080b76a4` and `0x080b76a6`.
- Require exact instructions `movs r0,#1` bytes `0120` and `bx lr` bytes `7047`; no extra or missing instruction start.
- Create one USER Function at `0x080b76a4`, exact 4-byte body, name `return_true_response_callback`. No same-address alias.
- Add 201 incoming USER DATA refs while preserving every source ref's CORE6. The newly allocated Function ID becomes the derived target-primary ID for all 201 refs.
- No Function, label, Data, ref or TMode mutation occurs at the 133 future raw callback targets.

## Section 5.1 登记 (Rule 3)

- none. The only segment raw block has 201 true runtime references and is handled by R4.

## 消费者证据 (R6)

| Evidence | Conclusion | Confidence |
|---|---|---|
| `asm/15_equip_target_summon_zoom.s:4944`, bytes `01207047` | The raw leaf returns 1 unconditionally. | high |
| `asm/15_equip_target_summon_zoom.s:5009-5041` | B76E4 returns the below-requirement predicate with thresholds split by type<=10. | high |
| `asm/15_equip_target_summon_zoom.s:5100-5115` | B7760 returns 1 exactly when self activation count is zero. | high |
| `asm/15_equip_target_summon_zoom.s:5139-5182` | B778C always uses the fixed Dark Room CID; a nonzero first count returns 1, while a zero first count reaches the same-CID two-count zero-sum test. | high |
| `asm/15_equip_target_summon_zoom.s:5216-5254` | B77F8 tests `opponent_lp < self_lp + 500`. | high |
| `asm/15_equip_target_summon_zoom.s:5320-5411` | B7878 has the Premature Burial, opponent/self monster/equip, missing-pair, and Sangan/Witch success paths stated in its new PLATE. | high |
| `asm/15_equip_target_summon_zoom.s:5415-5485` | B7934 first rejects zero opponent active equips, then has eligible-count and active-equip-count early accepts; remaining paths require restriction/precondition gates, score >= opponent LP or >2399, and a positive final comparison. | high |
| `asm/15_equip_target_summon_zoom.s:5592-5615`, `:6141-6198` | B7F64 requires the signed chain-field count >0; BAD6C checks low-13-bit CID at +0, zero halfword at +8, and bit7 in the parallel state dword at slot base +0x10. | high |
| `asm/14_equip_ai_scoring.s:25581,28389-28398` | B3408 and B485E call B771C; only B4850 PLATE contains the old predicate name and is rewritten to the positive gate before B46CC. | high |
| `root-f15-seg2-external-table-structure.json` | Six loops establish exact table starts, inclusive row counts and row+4 callback consumption. | high |

Every main word row carries source line, complete consumers and confidence in `F15-Seg-2.slots.tsv`. Every external row carries complete old state and final action in the carve plan.

## Machine contracts

- `f15-seg2-layout-map.json`: complete before/after byte partition.
- `f15-seg2-r4-plan.json`: raw-leaf refscan, instructions, Function and 201-source closure.
- `f15-seg2-external-table-carve-plan.json`: 504 affected rows, 1008 words, protected gap/suffix, 133-target future handoff and old-table transitions.
- `f15-seg2-global-equate-plan.json`: exact affected global Equate values and reference multisets.
- `f15-seg2-function-source-plan.json`: four renames, new Function, source/CSV/inventory scope, external PLATE scope and ordered handoff.
- `f15-seg2-name-reference-baseline.json`: exact old-name text and full-ROM raw/Thumb holds.
- `f15-seg2-constant-evidence.json`: structured new-constant evidence.
- `F15-Seg-2.slots.tsv`: 87 current source-word contracts.
- `F15-Seg-2.plates.tsv`: 21 Function/PLATE contracts.
- `f15-seg2-selfcheck.json`: final mechanical validation.
- `f15-seg2-freeze-manifest.json`: final hashes and sizes for review inputs and frozen artifacts.

## 求助

- none.

## Executor Report: F15-Seg-2

- 槽: EQ=65, REF_ADD=10, REF_PRESERVE=9, THUMB_REF_ADD=3, FUNC_RENAME=4, FUNC_CREATE=1, PLATE=22.
- External carve: 5 structured tables / 504 rows / 1008 words; protected raw 3-row gap=1.
- disasm=1 range / 4 bytes; Section 5.1=0.
- 新增 constants/global: 3 new GAS definitions, 5 existing GAS definitions reused, 8 new scalar Ghidra Equate objects, 168 new global Equate names, 661 binding additions across 213 affected final names, 316 new even Function refs from response tables, 3 main callback refs, one USER Function.
- 求助: none.
- proposal: `doc/dev/refine/F15-Seg-2.proposal.md`.
