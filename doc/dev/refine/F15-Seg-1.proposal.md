# Refine Proposal: F15-Seg-1 [0x080b5348,0x080b6c08)

## 范围与冻结输入

- 模块: `asm/15_equip_target_summon_zoom.s`.
- 段范围: `[0x080b5348,0x080b6c08)`, 6336 bytes.
- 当前前态: `root-f15-seg1-initial-baseline.json` SHA256 `90c77f9718e34a664ff9de229e4e5ee209a06aa8c4f1ea147f8a80f3c4be1b99`.
- 当前全模块只读前态: `root-f15-independent-map-prestate.json` SHA256 `f02555574d3297b4d118f13111267d3d54b2e7bc3ca1f96c67d08cd035f1f893`.
- 源码基线: `root-source-baseline-f15seg1.json`, 140 files, SHA256 `138577d4a50ad76e78381497e5f9a5023af42c94640ec1eb915054dd5c9cd22d`.
- DB 基线: `root-f15-seg1-db-backup.json`, 15 physical files, SHA256 `0b1bd275245c474965305c52e59ed1392379ce5f27e5305afd67e3aa304dc068`.
- 路线图: `root-f15-roadmap-final.json` SHA256 `eb459b72dc9fe478b430c377f594cfebef70ab9a7f3c4a6b648f359cb365ef1c`.
- Root 独立布局证据: `root-f15-seg1-baseline-layout-verified.json` 与 `root-f15-seg1-expected-layout.json`; 前者状态为 `ROOT_SEGMENT_BYTES_AND_ELF_PASS`.
- 本 executor 未启动 headless. 现有全模块前态已经覆盖 118 Function requests, 1264 words, 1359 requested states, 318 pointer targets 和 49408 module bytes. 追加查询需求为 none.
- 本提案仅定义落地合同. 本阶段不修改 Ghidra, 正式源码, constants, registry, CSV, inventories 或进度文档.

## 段测绘

### Function 入口

| Entry | Current name | Final name | Body bytes | Source |
|---|---|---|---:|---|
| 0x080b5348 | `select_equip_target_slot_with_eligibility_check` | same | 354 | asm/15_equip_target_summon_zoom.s:5 |
| 0x080b54c0 | `select_equip_target_slot_by_eligible_set` | same | 228 | asm/15_equip_target_summon_zoom.s:202 |
| 0x080b55ac | `select_equip_target_slot_full` | same | 744 | asm/15_equip_target_summon_zoom.s:327 |
| 0x080b58e8 | `scan_hand_for_best_equip_target_slot` | same | 436 | asm/15_equip_target_summon_zoom.s:762 |
| 0x080b5ad4 | `find_equip_target_by_random_order` | same | 124 | asm/15_equip_target_summon_zoom.s:1025 |
| 0x080b5b50 | `classify_equip_target_slot_score_tier` | same | 80 | asm/15_equip_target_summon_zoom.s:1098 |
| 0x080b5bac | `score_slot_by_no_summon_restriction` | `score_slot_by_summon_restriction_without_chain` | 54 | asm/15_equip_target_summon_zoom.s:1155 |
| 0x080b5bec | `score_slot_by_equip_chain_presence` | same | 54 | asm/15_equip_target_summon_zoom.s:1196 |
| 0x080b5c2c | `score_slot_by_equip_type_eligibility` | same | 60 | asm/15_equip_target_summon_zoom.s:1237 |
| 0x080b5c70 | `score_slot_by_field5_and_zone_bounds` | same | 100 | asm/15_equip_target_summon_zoom.s:1280 |
| 0x080b5ce8 | `score_slot_by_zone_lock_and_type` | same | 54 | asm/15_equip_target_summon_zoom.s:1354 |
| 0x080b5d28 | `find_evolution_target_for_equip_slot_card` | same | 100 | asm/15_equip_target_summon_zoom.s:1406 |
| 0x080b5d98 | `select_equip_target_slot_by_effect_strategy` | same | 2186 | asm/15_equip_target_summon_zoom.s:1464 |
| 0x080b675c | `exec_equip_target_by_best_field7_score` | same | 84 | asm/15_equip_target_summon_zoom.s:2840 |
| 0x080b67b0 | `exec_equip_target_by_active_side_bitmap` | same | 50 | asm/15_equip_target_summon_zoom.s:2891 |
| 0x080b67e8 | `exec_equip_target_by_field5_score_scan` | same | 248 | asm/15_equip_target_summon_zoom.s:2925 |
| 0x080b68f4 | `exec_equip_target_fallback_to_field_side` | same | 8 | asm/15_equip_target_summon_zoom.s:3069 |
| 0x080b68fc | `exec_equip_target_select_opponent_first` | same | 64 | asm/15_equip_target_summon_zoom.s:3089 |
| 0x080b693c | `exec_equip_target_select_by_direction_bit` | same | 38 | asm/15_equip_target_summon_zoom.s:3137 |
| 0x080b6962 | `exec_equip_target_by_effect_chain_match` | same | 98 | asm/15_equip_target_summon_zoom.s:3163 |
| 0x080b6a34 | `exec_equip_target_by_field6_score_and_effect` | same | 60 | asm/15_equip_target_summon_zoom.s:3282 |
| 0x080b6a70 | `exec_equip_target_by_chain_effect_type_mask` | same | 82 | asm/15_equip_target_summon_zoom.s:3321 |
| 0x080b6ac2 | `exec_equip_target_by_chain_effect_with_field_check` | same | 138 | asm/15_equip_target_summon_zoom.s:3370 |
| 0x080b6b50 | `exec_equip_target_by_comparator_then_scored_fallback` | same | 62 | asm/15_equip_target_summon_zoom.s:3447 |
| 0x080b6b94 | `exec_equip_target_by_comparator_field5_scored` | same | 38 | asm/15_equip_target_summon_zoom.s:3486 |
| 0x080b6bd8 | `enqueue_equip_slot_sprite_success` | same | 8 | asm/15_equip_target_summon_zoom.s:3532 |
| 0x080b6be0 | `select_equip_target_for_opponent_random` | same | 24 | asm/15_equip_target_summon_zoom.s:3538 |
| 0x080b6bf8 | `restore_equip_dispatch_frame` | same | 16 | asm/15_equip_target_summon_zoom.s:3556 |

### 完整布局

- 2710 current InstructionDB starts: 2542 mnemonic lines and 168 typed `.hword` instructions.
- Instruction bytes: 5702. Of these, 5580 bytes are owned by existing Function bodies; 59 InstructionDB starts covering the remaining 122 bytes have no Function owner (for example `0x080b69c4`). All 5702 bytes keep their current InstructionDB type and machine flow, and every existing Function body remains exact. The 168 `.hword` rows remain InstructionDB and are not retyped as Data.
- Current words: 141, exactly 128 `/undefined4`, 10 `/pointer`, and 3 `/dword`; all 141 current labels are automatic.
- Word bytes: 564. Padding bytes: 70. Total `5702 + 564 + 70 = 6336`.
- Current word references: 151 READ refs to word sources and 10 existing DATA refs from `/pointer` sources. The 10 DATA refs retain their exact CORE6 and primary flags.
- `ROM_INCBIN` / `.byte` blocks: 0.
- Complete per-word before and after contract is `F15-Seg-1.slots.tsv`. Complete Function/PLATE contract is `F15-Seg-1.plates.tsv`.

## 数据块分类 (Rule 2/3)

| Block | ref-scan | Classification | Evidence |
|---|---|---|---|
| none | none | no R4, no carve, no Section 5.1 | The segment is fully partitioned into typed InstructionDB, 141 four-byte words and 70 padding bytes. |

- Whole-ROM unaligned scan for all 28 Function entries found even/raw hits=0 and Thumb|1 hits=8 across seven entries. Evidence: `root-f15-seg1-name-pointer-leads.json` and `f15-seg1-refscan-evidence.json`.
- Five in-segment Thumb words are `0x080b655c`, `0x080b6578`, `0x080b69dc`, `0x080b6b6c`, and `0x080b6bb8`.
- Future Seg-2 words `0x080b701c`, `0x080b7234`, and `0x080b727c` remain byte, Data, label and reference exact. Their targets are not renamed in this proposal except no target among those three is the approved rename.

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS

- `EQ_ADD=102` scalar source bindings.
- These 102 rows use 77 distinct scalar Equate names. 61 names already exist in the current Ghidra global Equate table. 16 scalar names are absent and are created during landing; 15 of those also require new source definitions, while `LEAGUE_UNIFORM_NOMENCLATURE_CID` already exists in `constants/card_info.inc` and needs only its first Ghidra Equate object.
- Every row preserves source bytes, current Data type, all READ refs to the source and every existing source MemoryRef. It adds one operand-0 Equate and materializes the source label as USER.
- The complete address, value, expression, old symbols, old refs, final label and ASCII EOL contract is in the TSV.

### REF_SLOTS

- `REF_ADD=24` for current RAM pointer words without a source DATA ref.
- Targets are existing USER globals: `gEquipLpScoreBase`, `gEquipChainSlotRefs`, `gDuelFieldSlots`, `gDuelFieldSlotState`, and `gP1FieldArrayCBase`.
- `REF_PRESERVE=10` for the existing `gP1LifePoints` `/pointer` rows. Their DATA / DEFAULT / operand 0 / primary true refs are preserved byte-for-byte in CORE6; they are not deleted, recreated or source-upgraded.
- All six RAM targets keep their static USER primary Symbol IDs, namespaces, Data types and existing incoming references. `target_prestate_json` freezes each target state.

### Thumb callback source words

- `THUMB_REF_ADD=5`: `0x080b655c`, `0x080b6578`, `0x080b69dc`, `0x080b6b6c`, and `0x080b6bb8`.
- Final GAS uses `<Function>+1`, equal to each original odd ROM value.
- Four global odd-value Equates are created with five total bindings: `score_slot_by_equip_type_eligibility_1`, `score_slot_by_summon_restriction_without_chain_1`, `score_slot_by_equip_chain_presence_1` twice, and `score_slot_by_zone_lock_and_type_1`.
- Each source also receives one auxiliary USER DATA ref to the even Function entry. This appends the exact ref to the Function incoming list.
- No Symbol, Data unit or reference is created at an odd address. The existing odd dynamic DEFAULT label and its PARAM/ANALYSIS consumers remain derived metadata. The even Function ID and body remain exact.

### RENAME_SLOTS

- Pure label-only rows: 0.
- All 141 current automatic word definitions are covered exactly once by `EQ_ADD`, `REF_ADD`, `REF_PRESERVE` or `THUMB_REF_ADD`.
- All current `/pointer` and `/dword` types remain exact. No word is retyped.

### FUNC_RENAME

| Entry | Old | New | Evidence | indeg |
|---|---|---|---|---:|
| 0x080b5bac | `score_slot_by_no_summon_restriction` | `score_slot_by_summon_restriction_without_chain` | `asm/15_equip_target_summon_zoom.s:1166-1179`: zero restriction branches to result 0 at `0x080b5bd0`; only nonzero restriction plus `[slot+8]==0` reaches result 1 at `0x080b5bd8`. | 0 direct calls; one Thumb source |

Rename closure:

- Preserve Function ID 15815, USER Function source, Global namespace, exact 54-byte body, signature, flags, params, return and body refs.
- Full-ROM scan gives even/raw holders=0 and Thumb|1 holders exactly `{0x080b6578}`.
- At `0x080b6578`, replace the native expression with `score_slot_by_summon_restriction_without_chain+1`, add the approved `_1` Equate binding and auxiliary even DATA ref. Preserve bytes `ad5b0b08`, Data type and READ ref from `0x080b6562`.
- The odd address `0x080b5bad` remains without USER Symbol/Data/ref. Its dynamic DEFAULT display name follows the renamed Function.
- `tools/ghidra-labeling/RenameKnownFunctions.py` has no exact address tuple at prestate; add one exact tuple for this address and final name.
- Update only the name field in `doc/dev/naming-proposals.csv` and canonical `temp/ghidra-functions.csv` / `temp/ghidra-functions-renamed.txt`.
- Preserve `temp/ghidra-functions-auto.txt`, `temp/ghidra-functions-summary.md`, legacy `tools/ghidra-labeling/ghidra-functions.*`, and historical eval documents byte-identical.
- No external asm module or external PLATE requires a text projection. Exact xrefs are frozen in `f15-seg1-name-reference-baseline.json`.

### PLATE

- `F15-Seg-1.plates.tsv` contains 28 full PLATE rewrites, including the one renamed Function. Every final PLATE is ASCII and at most 500 characters.
- The current body of `0x080b5d98` contains three DataDB words at `0x080b6344`, `0x080b6390`, and `0x080b63f8`. Body ranges, size and SHA remain exact. `final_eol_json` appends all three approved EOL entries, and `final_body_refs_json` appends only the new DATA refs from the first two `gEquipChainSlotRefs` words. All old body refs remain exact.
- The rewrites remove stale auto names, mojibake and contradicted facts. Key corrections include:
  - `0x080b5348`: candidate shuffling runs only with more than one candidate and advances the shared PRNG through `sample_prng_scaled` at `0x080b5394`; the current fallback target name is retained.
  - `0x080b54c0`: mode-0 CID checks build an accepted mask, XOR it with the original bitmap, score the difference, and sample the original bitmap on failure; shuffle and sampling both advance the shared PRNG.
  - `0x080b55ac`: entry `r0` supplies the side used for the bit offset, while entry `r2` is saved at `sp+0x54` and checked before the final score threshold; shuffle and original-bitmap sampling advance the shared PRNG.
  - `0x080b58e8`: the callback receives `(player, 0xb, hand_index)` and must return nonzero; the two candidate groups are `(activation==0 && type==3)` and `(activation!=0 || type!=3)`, and replacement sampling occurs only after the group has a first candidate.
  - `0x080b5ad4`: search begins on the side supplied by entry `r1`, flips side after failure, reuses the shuffled order, and advances the shared PRNG during shuffle.
  - `0x080b5b50`: runtime holder `0x080b727c` exists and its caller scans slot indices 0 through 10.
  - `0x080b5bac`: summon restriction zero is rejection, not acceptance.
  - `0x080b5c70`: r2 is replaced by a local stack output buffer at `0x080b5c88`; the two arithmetic paths and Patrician packed CID comparison are stated exactly.
  - `0x080b5d28`: the current CID must first pass `check_card_id_is_effect_monster_type_b` before its final evolution target is considered.
  - `0x080b5d98`: entry `r1` is saved in `r5` as the effect-chain entry, the helper result bitmap is saved in `r9`, a zero bitmap returns 1 without enqueue, and a nonzero bitmap stores the two-field XOR side before `r2` CID dispatch.
  - `0x080b675c` / `0x080b67b0`: the score scan requires a value strictly above initial `-1`; the bitmap case selects `[+0x1c]` or `[+0x20]` by comparing inherited `r8.bit0` with global `[+0]` and tests the inherited `r9` bitmap.
  - `0x080b6962`: `LSL #14; LSR #29` extracts packed link count bits[20:18].
  - `0x080b6a70` / `0x080b6ac2`: mask `0x38000` is the independent packed category bits[17:15], not the link-count field; the direct path additionally checks entry type, opposite-side global state and the inherited bitmap before comparator/scored fallback.
  - `0x080b68f4`: `lsls #31; lsrs #31` extracts bit0.
- `0x080b5d98` through `0x080b6c08` keeps every current Function identity and body range. The parent owns the 0x2c-byte stack frame; the case fragments and restore stub reuse that frame. Same-frame BL edges remain current machine/API flows and are not reclassified as ordinary independent ABI calls.

## 新增 constants / 全局

All 15 definitions go to `constants/card_info.inc`:

| Name | Value | Structured evidence |
|---|---:|---|
| `CID_GAP_10D3` | 0x000010d3 | `data/cards-ids-array.s:317` maps the internal slot to `0xffff`; consumer is a low-13-bit CID dispatch. The same-valued `TRIGGER_OP_PARAM_10D3` is a different domain. |
| `STOP_DEFENSE_CID` | 0x000010e6 | `data/cards-ids-array.s:336`, `data/card-stats.s:3772` |
| `MEGAMORPH_CID` | 0x00001237 | `data/cards-ids-array.s:673`, `data/card-stats.s:7009` |
| `CASTLE_WALLS_CID` | 0x000012f2 | `data/cards-ids-array.s:860`, `data/card-stats.s:8816` |
| `TRIBUTE_TO_THE_DOOMED_CID` | 0x000012f8 | `data/cards-ids-array.s:866`, `data/card-stats.s:8842` |
| `BLOCK_ATTACK_CID` | 0x0000130a | `data/cards-ids-array.s:884`, `data/card-stats.s:9037` |
| `MYSTICAL_SPACE_TYPHOON_CID` | 0x0000132d | `data/cards-ids-array.s:919`, `data/card-stats.s:9427` |
| `RIRYOKU_CID` | 0x00001391 | `data/cards-ids-array.s:1019`, `data/card-stats.s:10493` |
| `MAKIU_CID` | 0x00001475 | `data/cards-ids-array.s:1247`, `data/card-stats.s:12352` |
| `INFERNO_HAMMER_CID` | 0x0000172a | `data/cards-ids-array.s:1940`, `data/card-stats.s:19528` |
| `FLINT_CID` | 0x00001842 | `data/cards-ids-array.s:2220`, `data/card-stats.s:22557` |
| `GUARDIAN_STATUE_CID` | 0x000018ba | `data/cards-ids-array.s:2340`, `data/card-stats.s:23857` |
| `MEDUSA_WORM_CID` | 0x000018bb | `data/cards-ids-array.s:2341`, `data/card-stats.s:23870` |
| `RISING_ENERGY_CID` | 0x0000192d | `data/cards-ids-array.s:2455`, `data/card-stats.s:25105` |
| `PATRICIAN_OF_DARKNESS_PACKED_CID_FIELD` | 0x9ce00000 | `PATRICIAN_OF_DARKNESS_CID << 19`; consumer `0x080b5cb6-0x080b5cbe` isolates the low-13-bit CID before comparison. |

- Exact structured proof and consumer slots: `f15-seg1-constant-evidence.json`.
- Other scalar rows reuse existing source constants. Same-valued constants from unrelated domains are not reused.
- Final slot bindings contain 81 distinct Equate names: 61 current global Equates reused and 20 new Ghidra Equate objects. The 20 are 16 scalar names plus four `_1` callback names. Total operand-0 bindings added are 107.
- Existing `pending_normal_summon_callback_080b76a4_1` and all 79 bindings remain exact. Evidence: `f15-seg1-equate-prestate.json`.

## carve 计划 (R7)

- none.

## disasm 计划 (R4)

- none. All 5702 instruction bytes are already typed InstructionDB; 5580 bytes keep their existing Function ownership and the 59 starts / 122 bytes with no Function owner remain unowned. No instruction is cleared, retyped or disassembled, and all current Function bodies remain exact.

## Section 5.1 登记 (Rule 3)

- none. The segment has no raw block.

## 消费者证据 (R6)

| Evidence | Conclusion | Confidence |
|---|---|---|
| `asm/15_equip_target_summon_zoom.s:1166-1179` | `0x080b5bac` accepts nonzero summon restriction with no chain halfword; approved rename. | high |
| `asm/15_equip_target_summon_zoom.s:1207-1221` | `0x080b5bec` also requires nonzero restriction and returns whether `[slot+8]` is nonzero; existing name remains accurate with corrected PLATE. | high |
| `asm/15_equip_target_summon_zoom.s:1285-1332` | `0x080b5c70` uses local stack output, two distinct arithmetic paths, and the packed Patrician CID field. | high |
| `asm/15_equip_target_summon_zoom.s:2573,2588,3230,3462,3505` | Five odd words are comparator callback payloads consumed by `find_best_slot_from_bitmap_by_comparator`. | high |
| `asm/15_equip_target_summon_zoom.s:3163-3278` | `0x080b6962` extracts link count from bits[20:18] and independently tests decoded side, type and bitmap membership. | high |
| `asm/15_equip_target_summon_zoom.s:3322-3360` | `0x080b6a70` tests category `(word & 0x38000)==0x8000`, decoded link-zero type and bitmap membership. | high |
| `asm/15_equip_target_summon_zoom.s:3371-3436` | `0x080b6ac2` adds exact entry-type, opposite-side global and inherited-bitmap gates before comparator/scored fallback. | high |
| `asm/15_equip_target_summon_zoom.s:3532-3564` | Success, randomized fallback and shared restore fragments preserve the parent frame and final r0. | high |

Every other word row carries its exact `source_file_line`, complete READ consumers, final expression and confidence in `F15-Seg-1.slots.tsv`.

## Machine contracts

- `f15-seg1-decisions.json`: address-independent semantic decisions, constants and final PLATE text.
- `f15-seg1-plan.json`: complete action list and derived counts.
- `f15-seg1-selfcheck.json`: mechanical completeness, bytes, types, refs, ASCII and count checks.
- `f15-seg1-refscan-evidence.json`: full-ROM Function raw/Thumb holds and future Seg-2 preservation.
- `f15-seg1-constant-evidence.json`: structured CID and packed-field proof.
- `f15-seg1-equate-prestate.json`: full Equate-table counts/hashes and pending B76A4 preservation.
- `f15-seg1-name-reference-baseline.json`: exact rename source, CSV, registry and inventory closure.
- `f15-seg1-query-request.json`: records that no additional headless query is required.
- `root-f15-seg1-baseline-layout-verified.json` / `root-f15-seg1-expected-layout.json`: independent ASM/ELF/ROM and exact instruction/word/padding cross-check inputs.
- `f15-seg1-freeze-manifest.json`: final SHA256 and sizes for every frozen artifact and review input.

## 求助

- none.

## Executor Report: F15-Seg-1

- 槽: EQ=102, REF_ADD=24, REF_PRESERVE=10, THUMB_REF_ADD=5, FUNC_RENAME=1, PLATE=28.
- carve=0, disasm=0, Section 5.1=0.
- 新增 constants/global: 15 source constants, 20 new Ghidra Equate objects, 24 RAM refs, 5 auxiliary even Function refs.
- 求助: none.
- proposal: `doc/dev/refine/F15-Seg-1.proposal.md`.
