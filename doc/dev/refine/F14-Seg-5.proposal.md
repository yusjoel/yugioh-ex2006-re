# Refine Proposal: F14-Seg-5 [0x080acc30..0x080ade8c)

## 段测绘

- 范围: `asm/14_equip_ai_scoring.s`, 4700 bytes.
- 当前布局独立门禁: `root-f14-seg5-initial-layout.json` PASS. 连续覆盖为 3976 code bytes, 150 words / 600 bytes, 124 padding bytes; 总计 4700 bytes, 无空洞和重叠.
- Typed code: 1906 InstructionDB, 其中 1834 个 native mnemonic 和 72 个 `.hword`. 72 个 `.hword` 保持 InstructionDB, 不转 Data.
- 当前 word: 150 个, 全部为自动名. 类型为 `/undefined4` 138, `/pointer` 6, `/dword` 6. `F14-Seg-5.slots.tsv` 精确冻结原 bytes, Data type, symbols, primary symbol, 8 条 source DATA refs, 152 条 PC READ refs_to, equates, EOL 和 owner.
- ROM_INCBIN / `.byte`: 0.
- 当前 Function 19 个:

| entry | current name | body bytes | incoming |
|---|---|---:|---:|
| `0x080acc30` | `check_card_effect_activation_eligible_by_id` | 1336 | 7 |
| `0x080ad270` | `check_card_id_in_field_spell_bst` | 158 | 1 |
| `0x080ad340` | `check_card_id_in_effect_target_whitelist` | 204 | 2 |
| `0x080ad450` | `dispatch_equip_check_by_mode` | 20 | 1 |
| `0x080ad464` | `build_equip_eligible_slot_bitmap` | 72 | 3 |
| `0x080ad4ac` | `resolve_equip_target_slot_for_player` | 26 | 3 |
| `0x080ad4c8` | `select_equip_target_slot_by_bitmap` | 70 | 2 |
| `0x080ad510` | `eval_equip_target_slot_with_score` | 204 | 4 |
| `0x080ad5ec` | `select_equip_target_slot_by_bitmap_for_player` | 26 | 0 |
| `0x080ad608` | `select_equip_target_slot_by_bitmap_alt` | 70 | 2 |
| `0x080ad650` | `score_equip_slot_placement_for_ai` | 174 | 4 |
| `0x080ad720` | `score_equip_targets_for_monster_slot` | 108 | 1 |
| `0x080ad794` | `check_effect_zone_or_pair_slot_available` | 84 | 1 |
| `0x080ad7f0` | `find_monster_slot_by_card_id_in_player_zone` | 72 | 0 |
| `0x080ad844` | `find_monster_slot_by_card_id_in_player_zone_alt` | 72 | 0 |
| `0x080ad898` | `check_card_id_placement_allowed` | 164 | 4 |
| `0x080ad974` | `dispatch_card_effect_by_card_id` | 1038 | 1 |
| `0x080ade34` | `check_slot_palette_nonzero` | 20 | 18 |
| `0x080ade48` | `find_first_empty_slot_for_card_type` | 58 | 28 |

19 个 Function 的真实 ID, source/type/namespace, body ranges/SHA256, signature/flags/params/return, EOL, incoming 和旧 PLATE 全文在 `F14-Seg-5.plates.tsv`.

补查合同使用 `root-f14-seg5-supplement-prestate.json` 的 38 个 non-NULL requested Functions, 150 words, 7 RAM targets, 140 address states 和 4700 units. 初始请求中的 `0x08056420` / `0x0806a168` 是 call-host 内部地址, 不是 Function entry; `root-f14-seg5-caller-owner-correction-prestate.json` 将其替换为实际 owners `tick_equip_activation_state_machine@0x080563cc` (ID4351, 278 bytes) 和 `dispatch_equip_zone_sprite_by_lp_state_with_placement_check@0x0806a118` (ID16441, 258 bytes). 原 NULL rows 和内部 address states 保留为前态证据, 不作为 missing Function.

## 数据块分类 (Rule 2/3)

本段没有 ROM_INCBIN 或 `.byte` 块, 因而没有 disasm, carve 或 §5.1 项. `root-f14-seg5-initial-layout.json` 证明除 typed InstructionDB, 150 个 4-byte Data 和 padding 外没有隐式 raw 范围.

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS

- `EQ_ADD=132`. 每行复用或新增的 constant, 原值, 最终 source label, GAS expression 和 ASCII EOL 见 `F14-Seg-5.slots.tsv`.
- 其中 121 行复用现有 constants, 11 行新增 constants. 域冲突按消费者基址和操作数消解:
  - `0x1388` 的两个消费者都比较 16-bit internal card ID, 使用 `EQUIP_SLOT_CARD_ID_RANGE_MAX`, 不使用 LP 或 score 域同值名.
  - `0x1cf4` 的 source 以 `gP1LifePoints` 为 base, 使用 `P2LP_BLOCK2_OFF_1CF4`, 不使用 `FIELD_STATE_OFF`.
  - `0x10b0` 位于 card-ID decision tree, 使用 `PRINCESS_OF_TSURUGI_CID`, 不使用 field offset 同值名.
  - `0xfffffe70` 经有符号加法施加 -400, 使用新增 `ZONE_EFFECT_ATK_PENALTY_400`; 不重命名或改写旧 `ZONE_EFFECT_ATK_PENALTY_500` 及其 5 个既有 Equate 绑定.
- 每个 scalar source 只绑定 operand 0 Equate, 不增加 DATA ref. 旧 Data type/bytes, 152 条 PC READ refs_to 和原 symbol 前态保持; DEFAULT source label 物化为唯一 USER label.

### REF_SLOTS

`REF=18`, 具体 before/after CORE6 在 slots TSV:

- `REF_PRESERVE=8`: `0x080acddc`, `0x080ad698`, `0x080ad774`, `0x080ad828`, `0x080ad87c`, `0x080adc88`, `0x080addc8`, `0x080ade18` 到 `gP1LifePoints`. 原 8 条 source DATA refs 的 type/source/operand/primary 和 target USER Symbol ID15545 保持.
- `REF_ADD=10`:
  - `0x080ad9d8 -> gEquipLpScoreBase`
  - `0x080ad16c`, `0x080adba8`, `0x080adc3c`, `0x080add6c -> gDuelFieldSlots`
  - `0x080adc34`, `0x080adc64 -> gEquipChainSlotRefs`
  - `0x080adcf4 -> gDuelFieldSlots_p2_base`
  - `0x080ade70 -> gEquipLpZoneEntryBase`
  - `0x080ade88 -> gEquipEffectZoneBase`
- 静态 USER targets 的 Symbol ID/source/type 保持. `0x0201e500` 当前 primary 是 dynamic DEFAULT `DAT_0201e500`; 它物化为单一 USER label `gEquipLpZoneEntryBase`, primary ID 允许合法变化. 不在同址保留旧 alias. GAS 定义使用现有 `gEquipLpZoneEntryBase` constant, source word 直接导出该名.
- 每个 REF source 的原 Data type/bytes 和 PC READ refs_to 保持. 新 source ref 为唯一 `DATA/USER_DEFINED/operand0/primary`.

### RENAME_SLOTS

纯改名槽 0. 所有 150 source 都由 EQ 或 REF 动作覆盖.

### FUNC_RENAME

| entry | old | new | evidence |
|---|---|---|---|
| `0x080ad270` | `check_card_id_in_field_spell_bst` | `check_card_id_in_field_spell_placement_bypass_set` | the leaf set contains searchers, recruiters, equip cards and gaps rather than field spells; its sole caller `check_card_field_spell_equip_placeable@0x080b1458` returns 1 immediately when this set matches, before the general field-spell placement gates |
| `0x080ad844` | `find_monster_slot_by_card_id_in_player_zone_alt` | `find_chain_zone_slot_by_card_id_for_player` | body reads count at `gP1LifePoints + player*PLAYER_BLOCK_STRIDE + 0x18`, scans 4-byte entries at `gP1LifePoints + player*PLAYER_BLOCK_STRIDE + 0x3a0 = gP1ChainZoneArray`, and returns first matching internal CID slot or -1 |

Rename contract:

- `0x080ad270`: preserve Function ID7257, 158-byte body, body SHA256 `789a4e0bbae54a398a2a958d6edf9e3490d34ac2c74745fb202497c9d5b39649`, source/type/namespace, signature/flags/params/return and its one incoming CORE6. Update the existing registry tuple name/PLATE, asm definition, `0x080b1460` BL target text, `0x080b1458` caller PLATE, formal CSV row and canonical temp CSV/renamed rows. Only derived incoming target-primary name changes.
- `0x080ad844`: preserve Function ID16761, 72-byte body, body SHA256 `377dde9e837c3fd3ac12a2c0550671d97dcdfe16e72bf503e8d0563892029a17`, source/type/namespace, signature/flags/params/return and zero incoming. Registry has no current tuple, so add one with final name and approved PLATE. Update only the asm definition, formal CSV row and canonical temp CSV/renamed rows.
- Full-ROM unaligned scan found 0 raw/even and 0 THUMB|1 holds for both renamed entries (`0x080ad270/271`, `0x080ad844/845`); no odd alias, pointer Equate or `rom.s` projection is added. Evidence: `f14-seg5-function-pointer-scan.json`.
- Complete active-name closure and excluded historical paths are frozen in `f14-seg5-name-reference-baseline.json`.

### PLATE

- 20 rows total: 17 `PLATE_REWRITE`, 2 `RENAME_PLATE`, 1 necessary `EXTERNAL_PLATE_PROJECTION` for `check_card_field_spell_equip_placeable@0x080b1458`. All new PLATE strings are ASCII; maximum is 424 chars, below 500.
- 13 old PLATE strings are non-ASCII and several state incorrect interfaces. Rewrites are driven by instruction/caller/exit evidence, not by encoding or length alone.
- The external projection is limited to `check_card_field_spell_equip_placeable@0x080b1458`: preserve Function ID7258, name, source/type/namespace, 180-byte body, body SHA256 `747b9051b0b118b305c7fdf5fa14a05c06de5c2aaef5774a30fb4852cb91a58e`, signature/flags/params/return, and its one incoming CORE6 from `0x080b1744`. Rewrite only its full PLATE and the textual BL target at `0x080b1460`; instruction bytes, body ownership and registry name remain unchanged.
- High-register corrections:
  - `0x080ad464`: `0x4681` moves entry r0 to r9 and `0x4688` moves entry r1 to r8. Both are normal APCS inputs.
  - `0x080ad510`: `0x4689` moves entry r1 internal CID to r9. Entry r2 is an eligibility-mode flag tested only as zero or nonzero, r3 is the excluded-entry count, and the fifth stack argument supplies the packed exclusion list from `[sp,#0x40]`.
  - `0x080ad650`: `0x4690` moves entry r2 placement mode to r8; the internal CID is loaded from the field slot.
  - `0x080ad720`: `0x4691` moves entry r2 eligibility-mode flag to r9 and forwards it as r2 to `eval_equip_target_slot_with_score`; entry r1 remains the field slot index. The local `sp+4` exclusion buffer is passed as the fifth outgoing stack argument, while r3 carries the existing exclusion count. Caller `0x080bb228` passes r2=1.
- Return corrections:
  - `0x080acc30` reaches only 0/1 shared exits.
  - `0x080ad794` is a three-class result: 0, 1, or 2.
  - `0x080ad720` returns 1 after all targets and 0 when a selector returns -1.
  - `0x080ad974` returns 0/1 through shared exits after card-specific checks.
- Registry contract: update 14 existing tuples (12 PLATE-only, renamed `0x080ad270`, and external caller `0x080b1458` PLATE), then add 6 missing tuples including renamed `0x080ad844`. Preserve registry order outside the approved additions/updates.

## carve 计划 (R7)

无.

## disasm 计划 (R4)

无. 1906 current InstructionDB addresses, instruction lengths, raw ROM bytes, function ownership and padding remain identical. 72 `.hword` entries remain typed InstructionDB and retain native source fallback.

## 新增 constants / 全局

在 `constants/card_info.inc` 新增 10 个 internal CID constants:

| constant | value | structured evidence |
|---|---:|---|
| `CID_GAP_1129` | `0x1129` | `cards-ids-array.s:403` maps to `0xffff` |
| `CID_GAP_1134` | `0x1134` | `cards-ids-array.s:414` maps to `0xffff` |
| `CID_GAP_1221` | `0x1221` | `cards-ids-array.s:651` maps to `0xffff` |
| `SWORD_OF_DEEP_SEATED_CID` | `0x1309` | logical CID693, password 98495314 |
| `UNHAPPY_MAIDEN_CID` | `0x130b` | logical CID695, password 51275027 |
| `MIRROR_FORCE_CID` | `0x1317` | logical CID705, password 44095762 |
| `HEAVY_STORM_CID` | `0x131b` | logical CID709, password 19613556 |
| `EXILED_FORCE_CID` | `0x14cb` | logical CID1019, password 74131780 |
| `ZABORG_THE_THUNDER_MONARCH_CID` | `0x174d` | logical CID1528, password 51945556 |
| `HAND_OF_NEPHTHYS_CID` | `0x185d` | logical CID1758, password 98446407 |

在 `constants/field_spell_bonus.inc` 追加 1 个准确的有符号 zone-score 常量:

| constant | value | structured evidence |
|---|---:|---|
| `ZONE_EFFECT_ATK_PENALTY_400` | `0xfffffe70` | `asm/14_equip_ai_scoring.s:13547-13559` 将 s32 -400 直接加到 zone score; 全局 Equate 前态为 absent |

完整 `cards-ids-array.s`, `card-stats.s`, passcode 和 `data.md` 行证据在 `f14-seg5-card-constant-evidence.json`. `root-f14-seg5-penalty-equate-prestate.json` 冻结旧 `ZONE_EFFECT_ATK_PENALTY_500=0xfffffe70` 的 5 个既有 operand-0 references 以及新 `ZONE_EFFECT_ATK_PENALTY_400` absent 前态; 新常量只绑定 `0x080adc68` operand 0. 其余 scalar 和全部 RAM globals 复用现有 constants. 新增常量总数为 11 (10 card CID + 1 field-bonus constant).

## §5.1 登记 (Rule 3)

无 raw block, 因而无登记.

## 消费者证据 (R6)

| 地址 / 组 | 消费者证据 | 结论 | 置信度 |
|---|---|---|---|
| `0x080acc30` | 7 条 BL: `0x080af9ee`, `0x080afa3e`, `0x080b11a0`, `0x080b15d4`, `0x080b1866`, `0x080b59e8`, `0x080b7310`; body `asm/14_equip_ai_scoring.s:11220` | r0 player, r1 eligibility mode, r2 internal CID; exact bool | high |
| `0x080ad464` | `asm/14_equip_ai_scoring.s:12393`, opcodes `0x4681/0x4688`, call `0x080ad480` | r0/r1 are normal inputs; bitmap is side*16+slot | high |
| `0x080ad510` | `asm/14_equip_ai_scoring.s:12490-12549`, opcode `0x4689`, `[sp,#0x40]` load at `asm/14_equip_ai_scoring.s:12512`, exclusion loop `0x080ad53a..0x080ad554` | r1 internal CID; r2 eligibility-mode flag tested zero/nonzero; r3 excluded-entry count; stack fifth arg is packed exclusion list | high |
| `0x080ad650` | `asm/14_equip_ai_scoring.s:12666`, opcode `0x4690`, field-slot read `0x080ad65c..0x080ad66c` | r2 placement mode; CID comes from slot | high |
| `0x080ad720` | `asm/14_equip_ai_scoring.s:12781-12814`, opcode `0x4691`, caller `asm/15_equip_target_summon_zoom.s:6920-6929` / `0x080bb228` | r1 field slot; r2 eligibility-mode flag forwarded to AD510; local `sp+4` buffer is fifth stack arg; caller passes r2=1; returns 0/1 | high |
| `0x080ad4c8`, `0x080ad608` | `asm/14_equip_ai_scoring.s:12461-12482,12637-12658`; AD510 decode `12553-12558` | success encoding is slot in bits 15:8 and player in bits 7:0; failure is -1 | high |
| `0x080adc68` | `asm/14_equip_ai_scoring.s:13547-13559`; `root-f14-seg5-penalty-equate-prestate.json` | s32 `0xfffffe70` is -400; add only `ZONE_EFFECT_ATK_PENALTY_400`, preserving old500 and its five bindings | high |
| `0x080ad794` | `asm/14_equip_ai_scoring.s:12845`, caller `0x080b7784` | result classes 0/1/2 are explicit `movs` exits | high |
| `0x080ad844` | `asm/14_equip_ai_scoring.s:12945`, count `+0x18`, array `+0x3a0` | chain-zone slot lookup, not an alternate monster-zone lookup | high |
| `0x080ad974` | `asm/14_equip_ai_scoring.s:13121`, caller `tick_equip_activation_state_machine@0x080563cc` uses BL at `0x08056440` and stores the result into activation state | context dispatch writes active side and returns exact bool | high |
| 150 words | `F14-Seg-5.slots.tsv` `consumer_evidence`, 152 exact refs_to | every slot has an instruction consumer; no zero-ref slot is left unnamed | high |

## Source, registry, CSV 和 inventory 投影合同

- `asm/14_equip_ai_scoring.s`: 150 source word expressions/labels/EOL, 19 segment Function PLATE writes, and two Function definition renames. No instruction bytes, padding, body ranges or Function boundaries change.
- `asm/15_equip_target_summon_zoom.s`: only the approved external caller PLATE at `0x080b1458` and the `0x080b1460` BL target-name projection.
- `constants/card_info.inc`: add only the 10 CID constants listed above.
- `constants/field_spell_bonus.inc`: preserve the complete old file as a byte prefix and append only `.equ ZONE_EFFECT_ATK_PENALTY_400, 0xfffffe70`; preserve `ZONE_EFFECT_ATK_PENALTY_500` and its five existing operand-0 bindings unchanged.
- Ghidra apply script: materialize 150 unique USER source labels, bind 132 scalar Equates, preserve 8 refs, add 10 refs, materialize `gEquipLpZoneEntryBase@0x0201e500`, rewrite 20 PLATEs, and rename two Functions.
- `tools/ghidra-labeling/RenameKnownFunctions.py`: update 14 existing tuples and add 6 missing tuples. The `0x080ad270` and `0x080ad844` tuples use final names; `0x080b1458` receives the approved caller PLATE.
- `doc/dev/naming-proposals.csv`: update only the `0x080ad270` and `0x080ad844` name fields; preserve row order and all other fields.
- Canonical inventories: refresh `temp/ghidra-functions.csv`, `temp/ghidra-functions-renamed.txt`, `temp/ghidra-functions-auto.txt`, `temp/ghidra-functions-summary.md`. Only `temp/ghidra-functions.csv` and `temp/ghidra-functions-renamed.txt` change, by the two renamed Function name texts; auto/summary remain byte-identical. Counts remain total 5214, named 5124, auto 90, thunks 1, with source totals ANALYSIS 2 / DEFAULT 90 / USER_DEFINED 5122.
- The exact changed-source allowlist is 8 files: `asm/14_equip_ai_scoring.s`, `asm/15_equip_target_summon_zoom.s`, `constants/card_info.inc`, `constants/field_spell_bonus.inc`, `tools/ghidra-labeling/RenameKnownFunctions.py`, `doc/dev/naming-proposals.csv`, `temp/ghidra-functions.csv`, and `temp/ghidra-functions-renamed.txt`.
- Exporter: no segment word contains an even or odd ROM Function pointer, so no per-source Function Equate or `_1` alias is needed. Scalar Equates and DATA refs alone determine all 150 GAS expressions.

## 落地后严格门禁

1. Query 19 segment Functions, the approved external caller `0x080b1458`, and 150 source addresses; compare every frozen field in the TSVs.
2. Verify 1906 InstructionDB addresses and raw bytes unchanged, including all 72 `.hword`; verify 150 words and 124 padding bytes cover the remaining range exactly.
3. Verify 132 source Equates and 18 DATA refs match after-state JSON, with 152 PC READ refs_to preserved. Separately require old `ZONE_EFFECT_ATK_PENALTY_500` to retain exactly its five existing operand-0 references and require new `ZONE_EFFECT_ATK_PENALTY_400` to have only the `0x080adc68` operand-0 reference; the expanded post-state observer covers 1300 address states.
4. Verify static target USER Symbol IDs unchanged; allow legal ID replacement only for DEFAULT `0x0201e500` and DEFAULT source labels.
5. Verify all new EOL/PLATE text ASCII, PLATE max 424, source labels unique and `^[a-z][a-z0-9_]+$`.
6. Re-export module 14 and approved registry/CSV/inventory projections; no other module source projection is approved.
7. Build and require byte-identical ROM plus source/DB scope gates.

## 求助

无.

## Executor Report: F14-Seg-5

- 槽: EQ=132, REF=18 (`REF_ADD=10`, `REF_PRESERVE=8`), RENAME=0, FUNC_RENAME=2, PLATE writes=20.
- carve=0, disasm=0, §5.1=0.
- 新增 constants/全局: 10 internal CID constants + 1 field-bonus signed constant; no new global address constant.
- 求助: none.
- proposal: `doc/dev/refine/F14-Seg-5.proposal.md`.
