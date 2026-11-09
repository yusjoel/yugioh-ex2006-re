# Refine Proposal: F14-Seg-6 [0x080ade8c..0x080af120)

## 段测绘

- 范围: `asm/14_equip_ai_scoring.s`, 4756 bytes.
- 独立布局门禁: `root-f14-seg6-initial-layout.json` PASS. 连续覆盖为 4100 code bytes, 143 words / 572 bytes, 84 padding bytes; 总计 4756 bytes, 无空洞和重叠.
- Typed code: 1894 InstructionDB, 其中 1785 个 native mnemonic 和 109 个 `.hword`. 109 个 `.hword` 保持 InstructionDB, 不转 Data.
- 当前 word: 143 个, 全部为自动名; 类型为 `/undefined4` 130, `/dword` 7, `/pointer` 6. `F14-Seg-6.slots.tsv` 精确冻结原 bytes, Data type, symbols, primary symbol, 6 条 source DATA refs, 147 条 PC READ refs_to, Equates, EOL 和 Function owner.
- ROM_INCBIN / `.byte`: 0.
- 当前 Function 14 个:

| entry | current name | body bytes | incoming |
|---|---|---:|---:|
| `0x080ade8c` | `find_random_empty_slot_excluding_card_id` | 162 | 1 |
| `0x080adf40` | `find_slot_by_card_type_and_player` | 68 | 23 |
| `0x080adf8c` | `check_special_card_activation_eligible` | 146 | 2 |
| `0x080ae050` | `find_empty_slot_for_card_id_dispatch` | 2636 | 3 |
| `0x080aec7a` | `exit_slot_search_with_result` | 16 | 44 |
| `0x080aec8c` | `activate_effect_slot_for_card` | 76 | 2 |
| `0x080aece4` | `fill_effect_slots_up_to_count` | 96 | 2 |
| `0x080aed4c` | `fill_effect_slots_up_to_count_with_equip_cap` | 126 | 1 |
| `0x080aedd4` | `compare_zone_max_scores_by_player` | 80 | 10 |
| `0x080aee24` | `scan_monster_slots_for_max_zone_score` | 130 | 4 |
| `0x080aeeb0` | `scan_monster_slots_for_peak_score` | 100 | 0 |
| `0x080aef1c` | `find_best_scored_slot_for_player_with_gate` | 158 | 3 |
| `0x080aefc4` | `scan_zone_slots_for_best_scored_slot` | 162 | 4 |
| `0x080af070` | `scan_monster_slots_for_best_scored_slot` | 164 | 1 |

14 个 Function 的真实 ID, source/type/namespace, body ranges/SHA256, signature/flags/params/return, EOL, incoming 和旧 PLATE 全文在 `F14-Seg-6.plates.tsv`. 其 incoming 总数为 100.

补查合同使用 `root-f14-seg6-supplement-prestate.json`: 58 个 requested Functions 全部 non-NULL, 143 words, 420 address states, 5 个静态 USER RAM targets 和 4756 units. 初始 owner 预期把 `0x080a001e/0x080a0030` 归给真实 2-byte Function `return_zero_from_equip_activation_display_phase@0x0809fb16`; `root-f14-seg6-caller-owner-correction-prestate.json` 独立确认两处实际位于 `run_equip_activation_display_phase_by_state_code@0x0809f9cc` (ID4830, 1828 bytes). 原 58 行与 `0x0809fb16` 前态保留, 再加入真实 owner, 最终上下文为 59 个 Function.

`0x080ae050` body 内有 5 个合法 DataDB words: `0x080ae230=0x0fd6`, `0x080ae234=0x11e4`, `0x080ae268=0x0fd6`, `0x080ae26c=0x11e4`, `0x080ae270=0x0fbb`. 它们保持 Data ownership, PC READ refs 和 Function body ranges; 添加 operand-0 Equate 不产生 MemoryRef.

## 数据块分类 (Rule 2/3)

本段没有 ROM_INCBIN 或 `.byte` 块, 因而没有 disasm, carve 或 §5.1 项. `root-f14-seg6-initial-layout.json` 证明除 typed InstructionDB, 143 个 4-byte Data 和 padding 外没有隐式 raw 范围.

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS

- `EQ_ADD=110`. 每行原值, 复用或新增 constant, 最终 source label, GAS expression, refs_to 和 ASCII EOL 在 `F14-Seg-6.slots.tsv`.
- 102 个 source rows 复用现有 constants, 8 个 source rows 使用本段 7 个唯一新增 definitions; `0x080ae74c` 与 `0x080ae76c` 共同绑定新增 `CYBER_TWIN_DRAGON_CID`, 其余 6 个新增 definitions 各绑定一个 source, 因而 `102 + 8 = 110 EQ_ADD`. 域判断以真实消费者为准:
  - effect-zone packed word 的 `lsls #0x13; lsrs #0x13` 提取 bits12:0 internal CID; `lsls #0x12; lsrs #0x1f` 提取 bit13 player. 不使用旧 PLATE 的 19-bit 字段描述.
  - `0xc1a80000` 是 `GAIA_SOUL_CID << 19`, 只用于与 packed word 左移结果比较.
  - `0x0001869f` 是十进制 99999, `0x080af070` 只在 candidate score 小于当前界时替换, 因而命名 `ZONE_SCORE_CEILING_99999`.
  - `0x1388` 的消费者比较 internal CID, 复用 `EQUIP_SLOT_CARD_ID_RANGE_MAX`; `0x1cf4` 的 base 是 `gP1LifePoints`, 复用 `P2LP_BLOCK2_OFF_1CF4`.
- 每个 scalar source 只绑定 operand 0 Equate, 不增加 DATA ref. 原 Data type/bytes, 147 条 PC READ refs_to 和 Function owner 保持; DEFAULT source label 物化为唯一 USER label.

### REF_SLOTS

`REF=33`, 所有 before/after CORE6 在 slots TSV:

- `REF_PRESERVE=6`: `0x080ae4b4`, `0x080ae6c8`, `0x080ae9f4`, `0x080aecd4`, `0x080aed48`, `0x080aedd0 -> gP1LifePoints`. 原 6 条 DATA refs 的 type/source/operand/primary 及 target USER Symbol ID15545 保持.
- `REF_ADD=27`:
  - `gEquipEffectZoneBase`: `0x080adee8`, `0x080adf3c`, `0x080adf88`, `0x080ae108`.
  - `gEquipLpZoneEntryBase`: `0x080adeec`, `0x080adf38`, `0x080adf70`, `0x080adfdc`, `0x080ae040`, `0x080ae594`, `0x080ae5dc`, `0x080ae634`, `0x080ae674`, `0x080ae71c`, `0x080aea60`, `0x080aeadc`, `0x080aeb80`, `0x080aec08`.
  - `gEquipLpScoreBase`: `0x080ae598`, `0x080aecd0`, `0x080aed08`, `0x080aed90`.
  - `gDuelFieldSlots`: `0x080aeeac`, `0x080aeef8`, `0x080aef74`, `0x080af020`, `0x080af0d0`.
- 5 个 target 都是当前静态 USER symbols: `gEquipLpScoreBase` ID30393, `gP1LifePoints` ID15545, `gDuelFieldSlots` ID20369, `gEquipEffectZoneBase` ID29996, `gEquipLpZoneEntryBase` ID34428. ID/source/type 保持. RAM bytes 为 null.
- 新 source ref 是唯一 `DATA/USER_DEFINED/operand0/primary`. REF_PRESERVE 保持原 source 为 DEFAULT 的 DATA ref, 不重建.

### RENAME_SLOTS

纯改名槽 0. 143 个 source 全部由 EQ 或 REF 动作覆盖.

### FUNC_RENAME

| entry | old | new | evidence |
|---|---|---|---|
| `0x080ade48` | `find_first_empty_slot_for_card_type` | `find_first_empty_slot_by_card_id` | `asm/14_equip_ai_scoring.s:13814-13830`, 28 callers inside AE050; body extracts packed bits12:0 with `LSL/LSR #19`, compares an internal CID and returns the first palette-empty matching slot |
| `0x080ade8c` | `find_random_empty_slot_excluding_card_id` | `select_empty_slot_preferring_different_card_id` | `asm/14_equip_ai_scoring.s:13854`, caller `0x080ae25e`: first pass counts palette-empty slots with different bits12:0 CID; when count is zero it returns the first palette-empty slot regardless of CID, so exclusion is a preference rather than an invariant |
| `0x080adf40` | `find_slot_by_card_type_and_player` | `find_empty_slot_by_card_id_and_player` | `asm/14_equip_ai_scoring.s:13954`, 23 callers inside AE050 pass named internal CIDs; body requires palette-empty, compares bits12:0 CID and bit13 player, then returns slot or -1 |
| `0x080aef1c` | `find_best_scored_slot_for_player_with_gate` | `compute_peak_monster_zone_score_with_gates` | `asm/14_equip_ai_scoring.s:16127`, callers `0x080ac0f0/0x080ac102/0x080b6868`; terminal `mov r0,r8` returns the maximum enabled score, not a slot index |
| `0x080af070` | `scan_monster_slots_for_best_scored_slot` | `find_lowest_scored_monster_slot` | `asm/14_equip_ai_scoring.s:16316`, caller `0x080acab2`; r8 starts at 99999 and updates only for candidate `< r8`, while r9 retains the selected slot index |

Rename contract:

- Preserve Function IDs 555/556/557/4768/4769, source/type/namespace, exact body ranges/SHA256, signature/flags/params/return and incoming CORE6. Only derived target-primary names change at approved call refs.
- Direct-call projections: AE050 has 28 calls to `0x080ade48`, 1 call to `0x080ade8c` and 23 calls to `0x080adf40`; AC0BC has 2 calls to `0x080aef1c`; B67E8 has 1 call to `0x080aef1c`; AC584 has 1 call to `0x080af070`.
- Full-ROM unaligned scan found 0 raw/even and 0 THUMB|1 holds for all five entries. No odd alias, pointer Equate or `rom.s` projection is added. Evidence: `f14-seg6-function-pointer-scan.json` and the reviewer audit for ADE48.
- Update five formal CSV name fields and their existing registry tuples. Refresh four canonical inventories; CSV and renamed lists project the new names, auto/summary content and all counts remain unchanged.

### PLATE

- 16 writes total: 4 segment `RENAME_PLATE`, 1 `EXTERNAL_RENAME_PLATE`, 10 segment `PLATE_REWRITE`, and 1 necessary `EXTERNAL_PLATE_PROJECTION`. All new strings are ASCII; maximum is 440 chars.
- `find_first_empty_slot_by_card_id@0x080ade48`: rename from `find_first_empty_slot_for_card_type` while preserving ID555, 58-byte body, SHA256 `af0a281c9e3d711eb56a64229f24706fed3192d373f0f98860b83144f095ae36`, signature, two previously refined Data words, EOL, 28 incoming CORE6 and all refs. Rewrite the full PLATE to state bits12:0 internal CID rather than low19/card type; only approved name/prototype and derived target-primary-name projections change.
- `exec_equip_target_by_field5_score_scan@0x080b67e8`: preserve name, ID6173, 248-byte body, SHA256 `3872b047000a91161215e8967959f624a15bb0cc21481f999f3c18637c10887f`, signature and incoming. Rewrite the full PLATE and project the `0x080b6868` call target name; the fallback consumes the score returned by renamed AEF1C and then clears slot-byte bits2..4.
- Segment ABI/return corrections:
  - ADE8C returns a preferred empty slot or first empty fallback, and -1 only when no palette-empty slot exists.
  - AE050 inputs are r0 player and r1 internal CID; r2 is not consumed. Its 44 transfers to AEC7A comprise 16 BL and 28 B, sharing one parent frame.
  - AEC8C/AECE4/AED4C use r2 as effect-handler auxiliary value; AECE4/AED4C use r3 requested count. Their return values are selected slot or actual completed count as documented in the TSV.
  - AEE24 inputs are r0 player, r1/r2 output pointers, r3 nonzero-slot-field8 gate. AEEB0 returns a peak score and has zero incoming code refs and zero ROM pointer holds.
  - AEF1C/AEFC4/AF070 inputs are r0 scoring player, r1 scanned player, r2 excluded slot, r3 primary-score flag, fifth stack argument secondary-score flag. AEF1C returns a score; AEFC4 returns greatest-score slot; AF070 returns lowest-score slot.

完整旧/新 PLATE, Function 全属性, registry/CSV/inventory/source 投影合同在 `F14-Seg-6.plates.tsv`, `f14-seg6-plate-plan.json`, `f14-seg6-function-projection-plan.json` 和 `f14-seg6-registry-plan.json`.

## carve 计划 (R7)

无.

## disasm 计划 (R4)

无. 1894 个 current InstructionDB 地址、长度、raw ROM bytes、TMode、Function ownership 和 42 段 / 84 bytes padding 全部保持. 109 个 `.hword` 保持 typed InstructionDB 和 native source fallback.

## 新增 constants / 全局

在 `constants/card_info.inc` 新增 5 个 internal CID constants 和 1 个 packed-field derived constant:

| constant | value | structured evidence |
|---|---:|---|
| `CYBER_JAR_CID` | `0x1331` | logical CID728, password 34124316 |
| `EXCAVATION_OF_MAGE_STONES_CID` | `0x1638` | logical CID1304, password 98494543 |
| `UNSHAVEN_ANGLER_CID` | `0x17e8` | logical CID1653, password 92084010 |
| `WHIRLWIND_PRODIGY_CID` | `0x1873` | logical CID1780, password 15090429 |
| `CYBER_TWIN_DRAGON_CID` | `0x18fc` | logical CID1885, password 74157028 |
| `GAIA_SOUL_PACKED_CID_FIELD` | `0xc1a80000` | `GAIA_SOUL_CID << 19`, consumer `asm/14_equip_ai_scoring.s:14084-14098` |

在 `constants/duel_field.inc` 新增:

| constant | value | evidence |
|---|---:|---|
| `ZONE_SCORE_CEILING_99999` | `0x0001869f` | AF070 initializes its minimum-score bound to 99999 and replaces it only on a lower candidate |

5 个 CID 的 `cards-ids-array.s`, `card-stats.s`, passcode 和 `data.md` 四重证据在 `f14-seg6-card-constant-evidence.json`. 102 个 EQ source rows 复用当前 constants; 8 个新 source rows 使用 7 个唯一新增 definitions, 其中 `CYBER_TWIN_DRAGON_CID` 由 `0x080ae74c` 与 `0x080ae76c` 共享, 其余 6 个 definitions 各一槽. 不新增 RAM global.

## §5.1 登记 (Rule 3)

无 raw block, 因而无登记.

## 消费者证据 (R6)

| 地址 / 组 | 消费者证据 | 结论 | 置信度 |
|---|---|---|---|
| ADE8C | `asm/14_equip_ai_scoring.s:13854`, call `asm/14_equip_ai_scoring.s:14367` | two-pass preference/fallback slot selection; rename required | high |
| ADF40 | `asm/14_equip_ai_scoring.s:13954`, 23 incoming calls in AE050 | palette-empty + bits12:0 internal CID + bit13 player | high |
| ADF8C | `asm/14_equip_ai_scoring.s:13998` | card-specific eligibility for UFO Turtle/equip cards and paired Kozaky state | high |
| AE050/AEC7A | `asm/14_equip_ai_scoring.s:14107,15753`; 44 exact incoming refs to AEC7A | shared parent frame with 16 BL and 28 B exits; slot/-1 result | high |
| AEC8C/AECE4/AED4C | `asm/14_equip_ai_scoring.s:15765,15810,15865` | exact player/CID/aux/count interfaces and slot/count returns | high |
| AEDD4 | `asm/14_equip_ai_scoring.s:15938`; callers `asm/13_equip_placement.s:5561,5571`; corrected owner 09F9CC | compares four maxima and returns +2/-2/0 | high |
| AEE24/AEEB0 | `asm/14_equip_ai_scoring.s:15984,16066` | output maxima vs selected-channel peak score are distinct contracts | high |
| AEF1C | `asm/14_equip_ai_scoring.s:16127`; calls `asm/14_equip_ai_scoring.s:9629,9637`, `asm/15_equip_target_summon_zoom.s:2999` | returns peak enabled score; stack fifth flag verified | high |
| AEFC4/AF070 | `asm/14_equip_ai_scoring.s:16221,16316`; AF070 caller `asm/14_equip_ai_scoring.s:11025` | greatest-score and lowest-score slot selectors use opposite comparisons | high |
| 143 words | `F14-Seg-6.slots.tsv`, 147 exact refs_to | every source has a real instruction consumer; no auto word is omitted | high |

## Source, registry, CSV 和 inventory 投影合同

- `asm/14_equip_ai_scoring.s`: 143 source word expressions/labels/EOL, 14 segment full PLATE writes, 4 segment Function definition renames, plus the approved ADE48 external Function definition rename, 28 BL operand-name projections and full PLATE rewrite. Instruction bytes, padding and Function boundaries remain unchanged.
- `asm/15_equip_target_summon_zoom.s`: only B67E8 full PLATE and the `0x080b6868` BL target-name projection.
- `constants/card_info.inc`: add only the 6 listed constants. `constants/duel_field.inc`: add only `ZONE_SCORE_CEILING_99999`.
- Ghidra apply script: materialize 143 unique USER source labels; bind 110 scalar Equates; preserve 6 refs and add 27 refs; rewrite 16 PLATEs; rename 5 Functions. It does not clear/re-disassemble code or alter bodies.
- `tools/ghidra-labeling/RenameKnownFunctions.py`: update 13 existing tuples and add 3 missing tuples (`0x080aeeb0`, `0x080aefc4`, `0x080b67e8`). Approved exact old/new tuples are frozen in `f14-seg6-registry-plan.json`.
- `doc/dev/naming-proposals.csv`: update only five name fields; preserve row order and other fields.
- Canonical inventories: refresh `temp/ghidra-functions.csv`, `temp/ghidra-functions-renamed.txt`, `temp/ghidra-functions-auto.txt`, `temp/ghidra-functions-summary.md`. Only CSV/renamed name text changes; total/named/auto/thunk/source counts remain current.
- Exact source allowlist: `asm/14_equip_ai_scoring.s`, `asm/15_equip_target_summon_zoom.s`, `constants/card_info.inc`, `constants/duel_field.inc`, `tools/ghidra-labeling/RenameKnownFunctions.py`, `doc/dev/naming-proposals.csv`, `temp/ghidra-functions.csv`, `temp/ghidra-functions-renamed.txt`. Auto/summary inventories are regenerated and required byte-identical.
- Exporter: no segment word contains an even or odd ROM Function pointer. No per-source Function Equate, `_1` alias or exporter edit is required.

## 落地后严格门禁

1. Query 14 segment Functions, ADE48, B67E8, 143 source words, 5 RAM targets and corrected caller owner 09F9CC; compare every frozen TSV field.
2. Verify 1894 InstructionDB addresses/raw bytes unchanged, including all 109 `.hword`; verify 143 words and 84 padding bytes cover the remaining range exactly.
3. Verify 110 operand-0 Equates, 27 new DATA refs and 6 preserved DATA refs match after-state JSON; preserve all 147 source PC READ refs_to.
4. Preserve all five static RAM target USER Symbol IDs/source/type. DEFAULT source labels may materialize USER with legal ID replacement; no same-address alias remains.
5. Preserve AE050 body ranges and the five in-body DataDB words/READ refs; Equate additions must not change Function body refs.
6. Verify all new EOL/PLATE text ASCII, PLATE max 440, labels unique and `^[a-z][a-z0-9_]+$`.
7. Re-export only approved source/registry/CSV/inventory projections, build, and require byte-identical ROM plus source/DB scope gates.

## 求助

无.

## Executor Report: F14-Seg-6

- 槽: EQ=110, REF=33 (`REF_ADD=27`, `REF_PRESERVE=6`), RENAME=0, FUNC_RENAME=5, PLATE writes=16.
- carve=0, disasm=0, §5.1=0.
- 新增 constants/全局: 5 internal CID constants + 1 packed CID-field constant + 1 score ceiling; no new RAM global.
- 求助: none.
- proposal: `doc/dev/refine/F14-Seg-6.proposal.md`.
