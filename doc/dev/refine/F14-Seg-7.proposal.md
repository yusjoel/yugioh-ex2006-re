# Refine Proposal: F14-Seg-7 [0x080af120..0x080b04a8)

## 段测绘

- 模块: `asm/14_equip_ai_scoring.s`, 5000 bytes.
- 独立布局基线 `root-f14-seg7-initial-layout.json` 为 PASS: 2115 个 InstructionDB (1985 mnemonic + 130 `.hword`) 共 4328 bytes, 149 个 4-byte words 共 596 bytes, 76 bytes padding, raw block 0. 全段连续覆盖, 无空洞或重叠.
- 149 个 words 全部为自动名. 前态类型为 `/undefined4` 130, `/dword` 12, `/pointer` 7; 现有 source DATA refs 9, PC READ refs_to 153. `F14-Seg-7.slots.tsv` 冻结每个 source 的 bytes, Data type, Symbols/primary, refs_from, refs_to, Equates, EOL 和 Function owner.
- 21 个现有 Function:

| entry | current name | body bytes |
|---|---|---:|
| `0x080af120` | `find_best_equip_target_slot_scored` | 508 |
| `0x080af374` | `sum_all_slot_scores_for_player` | 58 |
| `0x080af3b0` | `check_dual_field_slot_owner_mismatch` | 108 |
| `0x080af430` | `count_monster_slots_in_card_id_range` | 74 |
| `0x080af48c` | `count_spell_slots_in_card_id_range` | 74 |
| `0x080af4e8` | `count_monster_slots_by_card_id_range_for_player` | 58 |
| `0x080af534` | `check_card_id_in_eligible_set` | 272 |
| `0x080af6a0` | `count_effect_nodes_with_eligible_card` | 130 |
| `0x080af72c` | `count_equip_whitelist_cards_in_monster_zone` | 126 |
| `0x080af7b4` | `find_hand_slot_by_card_id_table` | 98 |
| `0x080af824` | `select_random_slot_by_callback` | 160 |
| `0x080af8cc` | `check_compound_pair_activation_eligible` | 70 |
| `0x080af914` | `check_any_pair_slot_available_for_card` | 42 |
| `0x080af940` | `check_effect_zone_available_for_player` | 50 |
| `0x080af984` | `check_spell_equip_zone_field6_match` | 50 |
| `0x080af9c0` | `check_hand_equip_target_available` | 66 |
| `0x080afa10` | `check_hand_equip_target_available_via_field_check` | 66 |
| `0x080afa60` | `check_equip_target_slot_card_eligible_by_id` | 394 |
| `0x080afc24` | `find_best_scored_spell_zone_slot` | 130 |
| `0x080afcb4` | `eval_equip_spell_placement_with_score` | 1002 |
| `0x080b011c` | `eval_monster_spell_placement_eligible_by_card` | 788 |

这 21 个 body 共 4324 bytes, 无重叠. 剩余已反汇编的 4 bytes 是 `0x080af980 movs r0,#1; 0x080af982 bx lr`, TMode=1, 当前 `getFunctionAt(0x080af980)=null`, 无 Symbol. 全 ROM byte-granular 扫描得到 even `0x080af980` 0 hit, THUMB `0x080af981` 1 hit, 唯一 source 为 word `0x080af9fc`. 因而本段新增一个 4-byte callback Function, 不改任何指令单元.

当前没有 `ROM_INCBIN` 或 `.byte` raw block. 本段另有一个被 `0x080af804` 引用的段外 ROM 表 `[0x09e5ab28,0x09e5ab5a)`, 纳入必要 carve 闭包.

## 数据块分类 (Rule 2/3)

| 块 | ref-scan (raw / THUMB\|1) | 判定 | 理由 |
|---|---:|---|---|
| 段内 | raw block 0 | none | 独立布局已把 5000 bytes 全部分为 typed code, 149 words 和 padding. |
| `[0x09e5ab28,0x09e5ab5a)` 50B | raw=1 (`0x080af804`), thumb=0 | carve | `find_hand_slot_by_card_id_table` 在 `0x080af7e4` 取表首; `0x080af810` 自增 index, `0x080af812 cmp #0x18`, `0x080af814 bls 0x080af7d8`, 明确访问 index 0..24 共 25 个 u16 internal CID. |
| `0x082979d1` 中的 `0x080af9c1` | thumb=1 | asset coupling | 命中位于未定义资产字节内部, 无 Data/Symbol/ref/Function owner; 不产生 callback 或 source 投影, 原始 bytes 保持. |

表边界以 `root-f14-seg7-table-boundary-correction.json` 为准. 早期 48-byte slice 仅是候选输入; CFG 证明第 25 项 `0x0fd6=SANGAN_CID` 位于 `0x09e5ab58`. `0x09e5ab5a..5b` 两个零字节和 `0x09e5ab5c` 既有 callback pointer 单元均在表外并完整保持.

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS

- `EQ_ADD=106`. 每行 operand-0 Equate, 最终 source label, GAS expression, ASCII EOL 和真实消费者地址在 `F14-Seg-7.slots.tsv`.
- 94 source rows复用现有 constants, 10 source rows使用本段新增 scalar definitions (5 个 internal CID constants形成6个绑定, 4 个 score-domain constants形成4个绑定), 2 source rows使用新 scoped callback aliases; `94 + 10 + 2 = 106`.
- callback words 也归 EQ, 但遵守 THUMB odd-address 合同:
  - `0x080af9fc=0x080af981` 绑定 scoped Equate `accept_slot_scan_candidate_unconditionally_1`, GAS 定义为 `accept_slot_scan_candidate_unconditionally+1`.
  - `0x080afa4c=0x080af985` 绑定 scoped Equate `check_spell_equip_zone_field6_match_1`, GAS 定义为 `check_spell_equip_zone_field6_match+1`.
  - 不在 odd 地址创建 Label/Data/ref. 现有 `0x080af9c4 -> 0x080af981` 与 `0x080afa14 -> 0x080af985` 的 `PARAM/ANALYSIS/op0/primary` refs 原样保持.
- `0xfffffc18` 在 AF120 是 signed score -1000, 使用新 `SCORE_DELTA_NEG_1000`, 不复用 LP 域同值名. `0xfffffc17` 是 score -1001. `0x382` 与 `0x12b` 是 score thresholds 898 与 299.

### REF_SLOTS

`REF=43`, 逐条 CORE6 在 slots TSV:

- `REF_PRESERVE=9`: 9 个 `gP1LifePoints` sources 保持原 DATA ref type/source/operand/primary 和 USER target ID15545.
- `REF_ADD=34`:
  - `gDuelFieldSlots`: 14.
  - `gEquipLpScoreBase`: 10.
  - `gEquipChainSlotRefs`: 3.
  - `gP1FieldArrayCBase`: 3.
  - `gDuelFieldSlots_p2_base`, `gP1ZoneHandCount`, `gEquipSpellZoneScoreBase`, `equip_hand_candidate_card_id_table`: 各 1.
- 已存在的静态 USER target ID/source/type保持: `gDuelFieldSlots` ID20369, `gEquipLpScoreBase` ID30393, `gEquipChainSlotRefs` ID20367, `gP1FieldArrayCBase` ID21613, `gDuelFieldSlots_p2_base` ID21510, `gP1ZoneHandCount` ID22162, `gP1LifePoints` ID15545.
- `0x0201b00c` 当前是 dynamic DEFAULT `DAT_0201b00c`, RAM bytes=null, Data unit absent. 物化 USER `gEquipSpellZoneScoreBase` 时不创建 RAM Data. 13 条既有 refs 的 CORE6 全保持, 包括 `0x08090b28` 的 `DATA/ANALYSIS/op1/primary=false`; 其余 12 条 primary=true. 新增 source `0x080afcb0` 的 `DATA/USER_DEFINED/op0/primary=true`. DEFAULT primary ID 可合法替换, 14 条 refs 只更新 derived target-primary metadata.
- `0x09e5ab28` 表首同样允许 DEFAULT ID 替换. 保持 `0x080af7e4 -> 0x09e5ab28` 的 `READ/ANALYSIS/op1/primary=true` 和同一指令到 `0x09e5ab2a` 的 `primary=false` edge; 新增 `0x080af804 -> 0x09e5ab28` source DATA ref.

### RENAME_SLOTS

纯改名槽 0. 149 个 current words 全部由 106 EQ + 34 REF_ADD + 9 REF_PRESERVE 覆盖.

### FUNC_RENAME

| entry | old | new | indeg / evidence |
|---|---|---|---|
| `0x080af3b0` | `check_dual_field_slot_owner_mismatch` | `check_field_spell_placement_available_by_card_id` | indeg=1, caller `0x080bbac6`; field9==2 分支要求 resident CID 与输入不同, 其他分支拒绝重复 CID 且要求至少两个空位; nonzero 表示可放置. |
| `0x080af72c` | `count_equip_whitelist_cards_in_monster_zone` | `count_equip_eligible_cards_across_field_zones` | indeg=3; loop 明确覆盖 slot 0..10, 只有 0..4 额外调用 whitelist predicate, 返回跨 field zones 的 qualifying count. |
| `0x080af940` | `check_effect_zone_available_for_player` | `check_effect_zone_unavailable_for_player` | indeg=3; zone count >6 或 available count==0 时返回1, 有可用 zone 时返回0; 旧名与布尔极性相反. |
| `0x080afc24` | `find_best_scored_spell_zone_slot` | `compute_peak_spell_zone_score_excluding_slot` | indeg=4; 返回最大 signed score 或 -1, 不返回 slot index. |

四个旧入口的 full-ROM raw/even 和 THUMB|1 hit 均为 0, 因而无 pointer alias. 保持 Function IDs 566/4401/570/5726, source/type/namespace, exact bodies/SHA, signature/flags/params/return 和 incoming CORE6. BL text, PLATE, formal CSV name 和 inventory name 按 `f14-seg7-function-projection-plan.json` 投影.

### CREATE_FUNCTION

- 创建 `accept_slot_scan_candidate_unconditionally@0x080af980`, USER Function, body `[0x080af980,0x080af984)`, bytes `01207047`, SHA256 `64d23481cb6a254816fb9c4c9b22031f78ed0a6ece5a6b0f6849a3ee7f77a2bb`.
- 两条现有 InstructionDB 和 TMode保持; 不 clear/disassemble. callback 忽略 r0/r1/r2并返回1.
- before: Function absent, Symbol absent. after: 单一 USER Function Symbol, 动态分配新 ID, 不留同址 alias. 新增 registry tuple, naming CSV row 和四 inventory 的一致投影.

### PLATE

- 写入 25 个 full PLATE: 段内 21 个现有 Function, 新建 AF980, 以及必要外部 name/semantics projections `0x080b7858`, `0x080b7934`, `0x080bb9b8`.
- 4 个 rename rows, 17 个段内 preserve-name rewrites, 1 个 create row, 3 个外部 rewrites. 全部 ASCII, 最大 435 chars.
- `F14-Seg-7.plates.tsv` 冻结所有现有 Function 的 ID/source/type/namespace, exact body ranges/SHA, signature/flags/params/return, EOL, incoming 和旧 PLATE全文/hash. 外部三行只改 full PLATE; name/body/signature保持.
- ABI 订正重点:
  - AF120 的 r2 是 excluded slot, r3 是 eligibility-only fallback flag; 返回 slot 或 -1.
  - AF824 两次扫描的 side 均是 opponent=`1-player`.
  - AF4E8 只以 r0=player 为输入; CID 范围固定为 `RIGHT_LEG_FORBIDDEN_ONE_CID..EXODIA_THE_FORBIDDEN_ONE_CID`, r1/r2 不是输入.
  - AF8CC 只消费 r0/r1; 前三个 count 检查使用 r1 低 16 bits, 第四个使用 r1 全值, 任一返回非零即返回 1, r2 不消费.
  - AF940 把原始 player 传给 `count_available_effect_zones`, 不计算 opponent.
  - AFC24 可选调用 `check_slot_full_activation_eligibility`, 返回 score, 不是 slot.
  - AFCB4 的 r3 是 gate flag, 第五个 stack argument 是 output pointer; 结果状态写入 output structure.
  - BB9B8 只处理 phase 0/1: phase 0 扫描耗尽后递增 phase 并进入 phase 1; phase 0/1 成功都直接返回 0, 其他 phase 和 phase-1 失败返回 1.

## carve 计划 (R7)

在 `asm/rom.s:2034` 的 `scene_scroll_table` host incbin (`offset=0x01e59dd4,size=0x0e28`) 内切割:

1. prefix incbin: `0x01e59dd4, 0x0d54`.
2. `equip_hand_candidate_card_id_table:` 25 个 `.hword` internal CID constants, ROM `[0x09e5ab28,0x09e5ab5a)`, 50 bytes.
3. suffix incbin: `0x01e5ab5a, 0x00a2`.

`0x0d54 + 0x32 + 0x00a2 = 0x0e28`. 原始 bytes 和 25 values 在 `f14-seg7-carve-contract.json`. Ghidra 保持 AB28/AB2A 两个现有 `/undefined2`, 在 AB2C..AB58 创建 23 个新 `/undefined2`; 物化一个 USER table-base label, 不创建 per-entry aliases. AB5A padding 和 AB5C pointer 单元保持.

## disasm 计划 (R4)

无 disasm. AF980 已是两条 typed InstructionDB, 本段仅 createFunction ownership. 2115 个 InstructionDB 的地址、长度、raw bytes、TMode 和 source-format分类保持, 包括 130 个 `.hword`.

## 新增 constants / 全局

### `constants/card_info.inc`

新增 9 个 internal CID constants:

| constant | value | logical CID | password |
|---|---:|---:|---:|
| `DIMENSIONAL_WARRIOR_CID` | `0x10a6` | 241 | 37043180 |
| `PANTHER_WARRIOR_CID` | `0x128f` | 604 | 42035044 |
| `MESSENGER_OF_PEACE_CID` | `0x134a` | 751 | 44656491 |
| `OBNOXIOUS_CELTIC_GUARD_CID` | `0x147c` | 954 | 52077741 |
| `SASUKE_SAMURAI_CID` | `0x1524` | 1098 | 16222645 |
| `MAGIC_JAMMER_CID` | `0x12fe` | 684 | 77414722 |
| `GEMINI_ELF_CID` | `0x11ba` | 442 | 69140098 |
| `VORSE_RAIDER_CID` | `0x138c` | 800 | 14898066 |
| `CYBER_TECH_ALLIGATOR_CID` | `0x12b6` | 639 | 48766543 |

每项均有 cards-ids, card-stats, passcode 和 `data.md` 四路结构证据, 见 `f14-seg7-card-constant-evidence.json`.

### `constants/duel_field.inc`

- `SCORE_DELTA_NEG_1000 = 0xfffffc18`.
- `SCORE_DELTA_NEG_1001 = 0xfffffc17`.
- `ZONE_SCORE_THRESHOLD_898 = 0x00000382`.
- `ZONE_SCORE_THRESHOLD_299 = 0x0000012b`.

### `constants/ewram.inc`

- `gEquipSpellZoneScoreBase = 0x0201b00c`. 真实消费者使用 `player*0xb4 + slot*0x24` 访问 signed score entries; 与 `gEquipLpScoreBase` 域和布局不同.

### `asm/rom.s`

- 新 table label和结构化 25×u16 entries.
- 新增两个 GAS aliases: `accept_slot_scan_candidate_unconditionally_1 = accept_slot_scan_candidate_unconditionally+1` 和 `check_spell_equip_zone_field6_match_1 = check_spell_equip_zone_field6_match+1`.

## §5.1 登记 (Rule 3)

无. 本段 raw block为0; 唯一段外数据块有真实 source和loop consumer, 已纳 carve.

## 消费者证据 (R6)

| 地址 / 组 | 消费者证据 | 结论 | 置信度 |
|---|---|---|---|
| AF120 | `asm/14_equip_ai_scoring.s:16436-16748`, incoming `0x08082430/0x0808360c/0x080b6468/0x080b6484` | r2 excluded slot, r3 fallback flag, returns selected slot or -1 | high |
| AF3B0 | `asm/14_equip_ai_scoring.s:16792`, caller `asm/15_equip_target_summon_zoom.s:8103` | field-spell placement availability by duplicate CID and free-slot rules | high |
| AF72C | `asm/14_equip_ai_scoring.s:17312-17389`, callers `asm/15_equip_target_summon_zoom.s:5420,5582,5587` | scans slots0..10, not only monster slots | high |
| AF7B4/table | `asm/14_equip_ai_scoring.s:17390-17454`; boundary evidence `AF810/AF812/AF814` | 25-entry internal-CID table, inclusive index0..24 | high |
| AF824 | `asm/14_equip_ai_scoring.s:17455-17545`, caller `0x080a267a` | count/sample/select on opponent slots using callback | high |
| AF940 | `asm/14_equip_ai_scoring.s:17608-17647`, three incoming calls | return1 means unavailable, return0 means available | high |
| AF980/AF9FC | bytes `01207047`; `0x080af9c4` loads source `0x080af9fc=0x080af981` | unconditional callback, Function creation required | high |
| AF984/AFA4C | `asm/14_equip_ai_scoring.s:17652-17684`, source `0x080afa4c=0x080af985` | zone0xb + field6==0x16 predicate callback | high |
| AFC24/B00C | `asm/14_equip_ai_scoring.s:18022-18098`, B00C target consumer closure | returns peak signed score; score table stride player0xb4/slot0x24 | high |
| AFCB4/B011C | `asm/14_equip_ai_scoring.s:18099-19165` | complete output-pointer ABI, score consumers, and terminal returns | high |
| 149 words | `F14-Seg-7.slots.tsv`, 153 exact refs_to | every current auto word has an action and real consumer evidence | high |

## Source, registry, CSV 和 inventory 投影合同

- `asm/14_equip_ai_scoring.s`: 149 word labels/expressions/EOL, 21 existing full PLATEs, create AF980 Function label/PLATE, four Function definition renames, and approved BL name projections. No instruction bytes or padding change.
- `asm/15_equip_target_summon_zoom.s`: only approved BL operand-name projections and three full PLATE rewrites.
- `asm/rom.s`: exact carve split, 25 `.hword` entries, two callback aliases.
- constants: only 9 card CIDs, 4 score constants, and 1 EWRAM global listed above.
- `tools/ghidra-labeling/RenameKnownFunctions.py`: update 10 existing tuples and add 15 missing tuples for the exact 25 PLATE rows. Exact old tuple source and final text在 `f14-seg7-registry-plan.json`.
- `doc/dev/naming-proposals.csv`: four name-only updates and one new AF980 row; preserve all unrelated rows/columns.
- 四个 canonical inventories: four rename projections and one new USER Function. CSV/renamed reflect names; total/named count increases only for AF980; auto/summary regenerate consistently.
- 旧名引用基线 `f14-seg7-name-reference-baseline.json` 冻结 44 个 formal hits: AF3B0 8, AF72C 11, AF940 10, AFC24 15. 只允许批准的 definition/BL/PLATE/registry/CSV/inventory投影.
- 完整 source allowlist 见 `f14-seg7-machine-plan.json`; 其余正式文件保持.

## 落地后严格门禁

1. Query 21 existing segment Functions, new AF980, three external PLATE Functions, 149 words, 9 target values, table bytes/bookends, two odd callback targets and所有 consumer states; 对照 TSV 和 machine plans.
2. 保持 2115 InstructionDB/4328 code bytes和76 padding bytes; Function creation不得 clear/disassemble.
3. 核验 106 Equates, 34 new source DATA refs, 9 preserved refs, 153 PC READ refs_to, 149 source labels/EOL; bytes和Data types不变.
4. B00C 保持13条旧CORE6和各自primary flag, 再加AFcb0 source; AB28/AB2A 保持两条旧READ edges, 再加AF804 source.
5. 核验 25 u16 table values, `[09e5ab28,09e5ab5a)` 50B边界, AB5A pad和AB5C pointer unit.
6. 核验 four existing Function IDs/body/signature守恒; AF980新增单一USER Function, body SHA精确, odd地址无新对象.
7. 所有新 PLATE/EOL ASCII, PLATE <=500, labels唯一并匹配 `^[a-z][a-z0-9_]+$`.
8. Re-export批准范围, build和byte-identical ROM仍为红线.

## 求助

无.

## Executor Report: F14-Seg-7

- 槽: EQ=106, REF=43 (`REF_ADD=34`, `REF_PRESERVE=9`), RENAME=0, FUNC_RENAME=4, FUNC_CREATE=1, PLATE writes=25.
- carve=1 (50B / 25 u16), disasm=0, §5.1=0.
- 新增 constants/全局: 9 internal CID constants, 4 score constants, `gEquipSpellZoneScoreBase`, 1 ROM table label, 2 THUMB callback aliases.
- 求助: none.
- proposal: `doc/dev/refine/F14-Seg-7.proposal.md`.
