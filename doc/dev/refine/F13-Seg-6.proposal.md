# Refine Proposal: F13-Seg-6 [0x080a27a0..0x080a38fc)

## 0. 结论

- 严格范围: [0x080a27a0,0x080a38fc), 0x115c = 4444 bytes. 本轮从低地址到高地址完成 Seg-6, 不重开 Seg-1..5, 不进入 0x080a38fc 之后的函数.
- 既有 Function=16, 均保留现名和现有 body. 新建 Function=1: 0x080a38f8 return_equip_row_type_13_complete.
- 原残留自动槽=184: DAT=66, DWORD=101, PTR=17. 动作合同为 EQ=138, REF=14, RENAME=32. reuse_status 为 REUSE=169, NEW=15.
- 当前段布局为 1712 个既有 Thumb instruction units / 3590 code bytes, 189 个 4-byte pool or switch words / 756 bytes, 47 个 2-byte padding ranges / 94 bytes, 以及尾部 4-byte .byte 块. 对尾块执行 R4 后为 1714 instruction units / 3594 code bytes, 189 words, 47 padding ranges, 合计 4444 bytes.
- 数据块归宿: R4=1 range [0x080a38f8,0x080a38fc); carve=0; Rule 3 / §5.1=0.
- Function create=1; 既有 Function rename=0; PLATE rewrite=8; PLATE new=1; slot EOL=184.
- 新定义=11 个唯一符号: constants/duel_field.inc 新增3个常量, asm/rom.s 新增8个 Thumb callback GAS aliases. 15个 NEW 槽引用这些11个定义.
- BLOCKED: none. 所有语义决定均有 high confidence 的 caller, callee body, global usage或结构化表证据.

## 1. 权威测绘产物

| artifact | data rows | SHA256 |
|---|---:|---|
| doc/dev/refine/F13-Seg-6.slots.tsv | 184 | 2070db7653e739f32396fa55c7ca49c70575edb857f3523fb0e55416f983d1fe |
| output/refine-run-20260831-194634/F13-Seg-6.refscan.tsv | 185 | 58d491e7bd73040b7873a0cf59ea6192f432f34be72f92587c2de66285829a52 |
| output/refine-run-20260831-194634/F13-Seg-6.direct-edges.tsv | 379 | bc0b2478cc1fe1d049645b5a52a32d87e5b777965cfd1d07758b8c719398484e |
| output/refine-run-20260831-194634/F13-Seg-6.functions.tsv | 17 | cb4bee09f630de00cc798e00382f4894332a4df92eada169cc29a6465744d207 |
| output/refine-run-20260831-194634/F13-Seg-6.layout.tsv | 236 | b90c4b464a563583765093f2cffdf6a126fbfea28b7a9aa5b0171ad64b2aa506 |
| output/refine-run-20260831-194634/f13-seg6-ref-prestate.json | 5 targets + 14 REF slots | e85ecaf4fd4ce0c82376c17e9af8a3aedc17330fb17e7cd9242ade0da589e12c |
| output/refine-run-20260831-194634/f13-seg6-ref-prestate-gate.json | 15 DB files before + 15 after | e149bb3a46ef62a2b4f77e4a68c22f5681beebe9703044408f62428bfcb4c4b7 |

slots.tsv 是逐槽落地合同, 包含 address, old_name, kind, original_value, action, target_symbol, slot_label, reuse_status, packed raw/THUMB hits, PC-relative consumers, evidence和ASCII EOL. functions.tsv 给出全部17个最终Function及每个精确非连续body range. layout.tsv 精确列出184个自动槽, 5个既有switch table words和47个padding ranges. f13-seg6-ref-prestate.json 是 C7 原始 Symbol/Data/ref 查询结果。其执行事实由独立 gate manifest 直接支撑：实际 headless 参数包含 `-noanalysis -readOnly`，exit_code=0，success marker 命中，取证脚本 SHA256=`4f2aa5dbd8161f6be01de341da243242f478da614cfe4d05dcbdf0b03d185298`，raw prestate SHA256=`e85ecaf4fd4ce0c82376c17e9af8a3aedc17330fb17e7cd9242ade0da589e12c`，DB before/after 均为15个文件且完整 relative-path/size/SHA256 maps exact-equal。脚本内的 `mode` 字段不作为执行模式或DB不变证据。

## 2. Function inventory

| entry | current or proposed name | action |
|---|---|---|
| 0x080a27a0 | check_equip_slot_by_card_id_dispatch | preserve |
| 0x080a2884 | tick_equip_activation_slot_scan_phase | preserve |
| 0x080a2a64 | check_equip_target_slot_state_matches | preserve |
| 0x080a2ad0 | tick_equip_target_selection_display_seq | preserve |
| 0x080a2c64 | check_equip_target_slot_eligible_for_equip_card | preserve |
| 0x080a2cd4 | check_equip_target_slot_eligible_with_whitelist | preserve |
| 0x080a2d54 | check_equip_target_slot_eligible_active_card | preserve |
| 0x080a2da4 | check_equip_target_slot_eligible_with_field_checks | preserve |
| 0x080a2e18 | check_equip_target_slot_eligible_pair_check | preserve |
| 0x080a2e80 | check_equip_target_slot_eligible_via_activation_eval | preserve |
| 0x080a2ed0 | tick_equip_target_slot_select_phase | preserve |
| 0x080a3060 | tick_effect_slot_activation_phase | preserve |
| 0x080a3130 | tick_tribe_card_equip_target_seq | preserve |
| 0x080a33a0 | scan_equip_target_slots_by_attribute_mask | preserve |
| 0x080a3534 | tick_effect_display_op_single_phase | preserve |
| 0x080a35ac | tick_equip_display_op_by_card_id_phase | preserve |
| 0x080a38f8 | return_equip_row_type_13_complete | create and name |

temp/ghidra-functions.csv has all first 16 entries and no Function at 0x080a38f8. The existing 16 names agree with their bodies and consumers; no rename is requested. Their exact body ranges and instruction/byte counts are frozen by F13-Seg-6.functions.tsv. The new body is exactly [0x080a38f8,0x080a38fc).

## 3. 自动槽清点与ref-scan

| kind | count |
|---|---:|
| DAT | 66 |
| DWORD | 101 |
| PTR | 17 |
| total | 184 |

| action | count | contract |
|---|---:|---|
| EQ | 138 | create an equate reference at operand 0, rename the slot, and set the TSV EOL |
| REF | 14 | rename the slot and install the exact operand-0 DATA reference to target_symbol |
| RENAME | 32 | preserve the existing gP1LifePoints DATA reference, rename the slot, and set the TSV EOL |

The 14 REF rows resolve to gDuelCardCtxBase x7, gDuelFieldSlots x4, gEquipChainSlotRefs x1, gEquipLpActivBitmap x1, and equip_target_selection_phase_jump_table at 0x080a2b00 x1. The 32 RENAME rows are all existing gP1LifePoints pool references. Each of the 184 labels is unique and matches ^[a-z][a-z0-9_]+$.

### 3.1 C7 target Symbol contract

Target Labels and pool references are two independently verified layers. A dry or persisted check must inspect both layers through the Symbol and Reference APIs; an exported name is not evidence for either layer, and one layer must not be inferred from the other.

| target | exact pre primary Symbol | pre Data | exact post primary Symbol | ID and alias contract |
|---|---|---|---|---|
| 0x0201e2a0 | ID=18879; `gDuelCardCtxBase`; type=Label; source=USER_DEFINED; namespace=Global; global=true; primary=true; symbol_count=1; alias_count=0 | `/undefined4`, length=4 | ID=18879; `gDuelCardCtxBase`; type=Label; source=USER_DEFINED; namespace=Global; global=true; primary=true; symbol_count=1; alias_count=0; Data unchanged | Reuse this non-dynamic object; ID must not change. |
| 0x0201c510 | ID=20369; `gDuelFieldSlots`; type=Label; source=USER_DEFINED; namespace=Global; global=true; primary=true; symbol_count=1; alias_count=0 | `/undefined4`, length=4 | ID=20369; `gDuelFieldSlots`; type=Label; source=USER_DEFINED; namespace=Global; global=true; primary=true; symbol_count=1; alias_count=0; Data unchanged | Reuse this non-dynamic object; ID must not change. |
| 0x0201bb90 | ID=20367; `gEquipChainSlotRefs`; type=Label; source=USER_DEFINED; namespace=Global; global=true; primary=true; symbol_count=1; alias_count=0 | `/undefined4`, length=4 | ID=20367; `gEquipChainSlotRefs`; type=Label; source=USER_DEFINED; namespace=Global; global=true; primary=true; symbol_count=1; alias_count=0; Data unchanged | Reuse this non-dynamic object; ID must not change. |
| 0x0201e220 | ID=27407; `gEquipLpActivBitmap`; type=Label; source=USER_DEFINED; namespace=Global; global=true; primary=true; symbol_count=1; alias_count=0 | `/undefined4`, length=4 | ID=27407; `gEquipLpActivBitmap`; type=Label; source=USER_DEFINED; namespace=Global; global=true; primary=true; symbol_count=1; alias_count=0; Data unchanged | Reuse this non-dynamic object; ID must not change. |
| 0x080a2b00 | ID=5854; `switchD_080a2af0::switchdataD_080a2b00` (export projection `switchD_080a2af0__switchdataD_080a2b00`); type=Label; source=ANALYSIS; namespace=`switchD_080a2af0`; global=false; primary=true; symbol_count=1; alias_count=0 | `/pointer`, length=4 | ID=5854; `equip_target_selection_phase_jump_table`; type=Label; source=USER_DEFINED; namespace=Global; global=true; primary=true; symbol_count=1; alias_count=0; Data remains `/pointer`, length=4 | Move and rename the same ID=5854 Symbol object to Global with USER_DEFINED source before REF installation. Do not call `createLabel` at this target, create an alias, or retain the scoped automatic name. |

None of these five target Symbols is a dynamic DEFAULT object, so no target ID change is legal. For the 14 pool slots below, each pre primary label is a dynamic DEFAULT object: DEFAULT-to-USER_DEFINED materialization may allocate a new Symbol ID only at that same address. Such a slot-ID change is legal only when post-state has exactly one global primary USER_DEFINED Label with the approved slot name, the old DEFAULT name is absent, and alias_count=0. The apply receipt must record every actual post ID, and fresh persisted check must require those recorded IDs exactly. Any target ID change, second same-address Symbol, or unlisted slot-ID change is a failure.

### 3.2 C7 REF slot Symbol and reference contract

All 14 slots have pre `references_from=[]`. Their sole current slot Symbol is the listed global primary DEFAULT Label (`type=Label`, `symbol_count=1`, `alias_count=0`). Post-state must reuse or materialize that address as the listed global primary USER_DEFINED slot Label (`type=Label`, `symbol_count=1`, `alias_count=0`) and contain exactly the listed single memory-reference tuple. The listed Data object and its four ROM bytes are immutable: REF installation and Symbol materialization must not retype, clear, delete or rebuild it. No additional reference at another operand, non-DATA reference, or alias is allowed.

| from | exact pre slot Symbol / reference | exact pre and post Data | exact post slot Symbol | exact post reference tuple |
|---|---|---|---|---|
| 0x080a29c8 | ID=4611686018562271688 `DAT_080a29c8`; references_from=[] | address=0x080a29c8; type=`/undefined4`; length=4; object span and bytes unchanged | `ptr_g_duel_card_ctx_base_080a29c8` | `(from=0x080a29c8, operand=0, to=0x0201e2a0, type=DATA, source=USER_DEFINED, primary=true)` |
| 0x080a2afc | ID=4611686018562271996 `DAT_080a2afc`; references_from=[] | address=0x080a2afc; type=`/undefined4`; length=4; object span and bytes unchanged | `equip_target_selection_phase_jump_table_ptr_080a2afc` | `(from=0x080a2afc, operand=0, to=0x080a2b00, type=DATA, source=USER_DEFINED, primary=true)` |
| 0x080a2b78 | ID=4611686018562272120 `DAT_080a2b78`; references_from=[] | address=0x080a2b78; type=`/undefined4`; length=4; object span and bytes unchanged | `ptr_g_duel_card_ctx_base_080a2b78` | `(from=0x080a2b78, operand=0, to=0x0201e2a0, type=DATA, source=USER_DEFINED, primary=true)` |
| 0x080a2f98 | ID=4611686018562273176 `DWORD_080a2f98`; references_from=[] | address=0x080a2f98; type=`/dword`; length=4; object span and bytes unchanged | `ptr_g_equip_chain_slot_refs_080a2f98` | `(from=0x080a2f98, operand=0, to=0x0201bb90, type=DATA, source=USER_DEFINED, primary=true)` |
| 0x080a2ff4 | ID=4611686018562273268 `DWORD_080a2ff4`; references_from=[] | address=0x080a2ff4; type=`/dword`; length=4; object span and bytes unchanged | `ptr_g_duel_card_ctx_base_080a2ff4` | `(from=0x080a2ff4, operand=0, to=0x0201e2a0, type=DATA, source=USER_DEFINED, primary=true)` |
| 0x080a30c4 | ID=4611686018562273476 `DWORD_080a30c4`; references_from=[] | address=0x080a30c4; type=`/dword`; length=4; object span and bytes unchanged | `ptr_g_duel_card_ctx_base_080a30c4` | `(from=0x080a30c4, operand=0, to=0x0201e2a0, type=DATA, source=USER_DEFINED, primary=true)` |
| 0x080a31ec | ID=4611686018562273772 `DWORD_080a31ec`; references_from=[] | address=0x080a31ec; type=`/dword`; length=4; object span and bytes unchanged | `ptr_g_duel_field_slots_080a31ec` | `(from=0x080a31ec, operand=0, to=0x0201c510, type=DATA, source=USER_DEFINED, primary=true)` |
| 0x080a31f0 | ID=4611686018562273776 `DWORD_080a31f0`; references_from=[] | address=0x080a31f0; type=`/dword`; length=4; object span and bytes unchanged | `ptr_g_duel_card_ctx_base_080a31f0` | `(from=0x080a31f0, operand=0, to=0x0201e2a0, type=DATA, source=USER_DEFINED, primary=true)` |
| 0x080a327c | ID=4611686018562273916 `DWORD_080a327c`; references_from=[] | address=0x080a327c; type=`/dword`; length=4; object span and bytes unchanged | `ptr_g_duel_field_slots_080a327c` | `(from=0x080a327c, operand=0, to=0x0201c510, type=DATA, source=USER_DEFINED, primary=true)` |
| 0x080a3354 | ID=4611686018562274132 `DWORD_080a3354`; references_from=[] | address=0x080a3354; type=`/dword`; length=4; object span and bytes unchanged | `ptr_g_duel_field_slots_080a3354` | `(from=0x080a3354, operand=0, to=0x0201c510, type=DATA, source=USER_DEFINED, primary=true)` |
| 0x080a3480 | ID=4611686018562274432 `DWORD_080a3480`; references_from=[] | address=0x080a3480; type=`/dword`; length=4; object span and bytes unchanged | `ptr_g_duel_card_ctx_base_080a3480` | `(from=0x080a3480, operand=0, to=0x0201e2a0, type=DATA, source=USER_DEFINED, primary=true)` |
| 0x080a3488 | ID=4611686018562274440 `DWORD_080a3488`; references_from=[] | address=0x080a3488; type=`/dword`; length=4; object span and bytes unchanged | `ptr_g_duel_field_slots_080a3488` | `(from=0x080a3488, operand=0, to=0x0201c510, type=DATA, source=USER_DEFINED, primary=true)` |
| 0x080a3490 | ID=4611686018562274448 `DWORD_080a3490`; references_from=[] | address=0x080a3490; type=`/dword`; length=4; object span and bytes unchanged | `ptr_g_equip_lp_activ_bitmap_080a3490` | `(from=0x080a3490, operand=0, to=0x0201e220, type=DATA, source=USER_DEFINED, primary=true)` |
| 0x080a3574 | ID=4611686018562274676 `DWORD_080a3574`; references_from=[] | address=0x080a3574; type=`/dword`; length=4; object span and bytes unchanged | `ptr_g_duel_card_ctx_base_080a3574` | `(from=0x080a3574, operand=0, to=0x0201e2a0, type=DATA, source=USER_DEFINED, primary=true)` |

Preflight must validate every target pre-state, all 14 empty pre-reference sets and every exact slot Data address/type/length/byte tuple before mutation. Postcheck, apply receipt and fresh persisted check must separately validate the five exact target post Symbols/Data objects, 14 exact slot Symbols, 14 unchanged slot Data objects and byte tuples, and 14 exact reference tuples. Any slot Data change fails immediately.

All 184 slots were scanned as raw 32-bit address and THUMB|1 across the full ROM. All THUMB|1 packed counts are zero. 182 slots have raw packed count zero. Slot 0x080a2800 has four unaligned raw coincidences inside data/card-stats.s. Slot 0x080a2968 has one unaligned raw coincidence inside data/card-image-tiles.s. These five asset-byte coincidences are not address references. Every slot has at least one decoded PC-relative LDR consumer listed in refscan.tsv and slots.tsv.

The 5 non-auto words at 0x080a2b00..0x080a2b14 are the existing five-way switch table targets 0x080a2b14, 0x080a2b44, 0x080a2b5c, 0x080a2b9c and 0x080a2c28. The table base is loaded through slot 0x080a2afc. They remain structured switch data and receive no duplicate labels.

## 4. 数据块分类

| block | size | full-ROM packed ref-scan | decoded control flow | decision |
|---|---:|---|---|---|
| 0x080a38f8..0x080a38fc | 4 | raw=0, THUMB|1=0 | BL 0x080a187a -> 0x080a38f8 | R4 disasm and Function create |

There is no ROM_INCBIN in this range. The only residual block is 01 20 70 47, decoded as:

```text
0x080a38f8  2001  movs r0,#1
0x080a38fa  4770  bx lr
```

The decoded BL overrides the packed-count result. The block is reachable code and cannot enter §5.1. There is no fall-through from 0x080a38ea across the 0x080a38ec..0x080a38f8 pool/padding area.

## 5. R4 and Function plan for 0x080a38f8

- Caller: asm/13_equip_placement.s:8863 is case 13 of tick_equip_display_row_by_type. At 0x080a1874..0x080a1878 it loads the equip context player value into r0, then 0x080a187a calls 0x080a38f8.
- Callee: asm/13_equip_placement.s:13575 contains 01 20 70 47. The body does not read inbound r0 and returns 1 unconditionally.
- Call graph: the full direct-edge scan yields one inbound caller for this entry.
- Contract: row type 13 requires no extra display operation and reports completion immediately. Confidence: high.
- Clear only the undefined/data listing in [0x080a38f8,0x080a38fc), disassemble it in Thumb mode, create the exact Function body, and replace DEFAULT SUB_080a38f8 with USER_DEFINED return_equip_row_type_13_complete.
- APCS signature: u32 return_equip_row_type_13_complete(void). Return r0=1; no input is read; no side effect.
- No local label, literal pool, padding, EOL, carve, or constant is needed inside this body.

New ASCII PLATE:

```text
No APCS input is read. Returns 1 unconditionally. The only decoded caller is tick_equip_display_row_by_type case 13 at 0x080a187a, so row type 13 completes without additional work.
```

## 6. New and reused definitions

Add exactly three constants to constants/duel_field.inc:

```asm
.equ EQUIP_DISPLAY_HANDLER_SUCCESS_OP31_SUB, 0x00000121
.equ EQUIP_TARGET_SELECTION_DELAY_OFF, 0x00001d9e
.equ EQUIP_LP_ACTIV_BITMAP_FROM_FIELD_SLOTS_OFF, 0x00001d10
```

Evidence is high confidence: 0x121 is passed at 0x080a36cc after a nonzero handler result. In tick_equip_target_selection_display_seq, input r2 is truncated to low8 and retained in r4; case 0 at 0x080a2b22..0x080a2b26 stores r4 with `strh r4` to `[gP1LifePoints+0x1d9e]`, initializing the delay from that caller-supplied value. The caller at 0x080a17e8..0x080a17ea loads r2 from `EQUIP_REROLL_COUNT_TARGET_OFF`; case 4 at 0x080a2c28..0x080a2c34 reads the delay and decrements it only when the value is greater than 1. The 0x1d10 value is added to gDuelFieldSlots at 0x080a3450..0x080a3458 and reaches gEquipLpActivBitmap. DISPLAY_SEQ_ACTIVE_PLAYER_OFF is not reused for the base-specific 0x1d10 consumer. A constants scan found no same-domain reusable symbol for these three values.

Add exactly eight GAS aliases to asm/rom.s:

```asm
.equ check_equip_slot_by_card_id_dispatch_1, check_equip_slot_by_card_id_dispatch+1
.equ check_equip_target_slot_state_matches_1, check_equip_target_slot_state_matches+1
.equ check_equip_target_slot_eligible_for_equip_card_1, check_equip_target_slot_eligible_for_equip_card+1
.equ check_equip_target_slot_eligible_with_whitelist_1, check_equip_target_slot_eligible_with_whitelist+1
.equ check_equip_target_slot_eligible_active_card_1, check_equip_target_slot_eligible_active_card+1
.equ check_equip_target_slot_eligible_with_field_checks_1, check_equip_target_slot_eligible_with_field_checks+1
.equ check_equip_target_slot_eligible_pair_check_1, check_equip_target_slot_eligible_pair_check+1
.equ check_equip_target_slot_eligible_via_activation_eval_1, check_equip_target_slot_eligible_via_activation_eval+1
```

The 11 NEW callback slots are odd ROM values equal to one of these entries plus one. The remaining EQ values reuse existing card IDs, equip/LP offsets, strides, display states and display operations. At 0x080a2878, 0x12a1 reuses zone_query_hand_tag_12a1 because its consumer is find_effect_node_in_zone; it does not reuse PARASITE_PARACIDE_CID.

## 7. PLATE and EOL plan

Eight existing PLATE comments require full ASCII rewrite. Two contain stale FUN_ caller names; six contain obsolete automatic DAT anchors. The other eight existing Function PLATE comments are preserved.

| entry | replacement PLATE |
|---|---|
| 0x080a27a0 | Dispatches equip-slot eligibility checks by card ID. Inputs: r0=player_side, r1=target_type, r2=slot_index. Returns 0x800 when eligible and 0 otherwise. Called by tick_equip_activation_slot_scan_phase. |
| 0x080a2a64 | Checks whether a candidate equip target slot matches the requested player, slot, and state. Inputs: r0=player_side, r1=zone_index, r2=slot_offset. Returns 0x800 on a match and 0 otherwise. Called by tick_equip_target_selection_display_seq through its callback table. |
| 0x080a2c64 | Equip target predicate for the Dark Coffin dispatch path. Inputs: r0=player_side, r1=zone_index, r2=slot_offset. Requires a valid face-up slot. Rejects the candidate when query_slot_effect_eligibility_nonzero returns nonzero. Returns 0x800 when eligible and 0 otherwise. |
| 0x080a2cd4 | Equip target predicate with player, active-card, Creature Swap whitelist, and effect-eligibility checks. Inputs: r0=player_side, r1=zone_index, r2=slot_offset. Returns 0x800 when eligible and 0 otherwise. |
| 0x080a2d54 | Equip target predicate requiring matching player and active-card state. Inputs: r0=player_side, r1=zone_index, r2=slot_offset. Returns 0x800 when eligible and 0 otherwise. |
| 0x080a2da4 | Equip target predicate requiring matching player, active-card state, nonzero card field 5, card field 8 not equal to 9, and final composite eligibility. Returns 0x800 when eligible and 0 otherwise. |
| 0x080a2e18 | Equip target predicate for full-field pair checks. Rejects an already-selected packed player and slot pair. Inputs: r0=player_side, r1=zone_index, r2=slot_offset. Returns 0x800 when eligible and 0 otherwise. |
| 0x080a2e80 | Equip target predicate using eval_slot_activation_eligibility_full. Inputs: r0=player_side, r1=zone_index, r2=slot_offset. Returns 0x800 when eligible and 0 otherwise. |

Together with the new tail PLATE, exact PLATE=9. All nine strings are ASCII and below 500 bytes. The 184 slot EOL strings are taken verbatim from slots.tsv and are ASCII. No instruction EOL is added.

## 8. Direct-edge closure

- Segment sources [0x080a27a0,0x080a38f8) contain 378 decoded direct B, conditional B, or BL edges.
- 296 land inside Seg-6: 295 local targets and one existing Function entry. The other 82 land at 34 unique out-of-segment addresses; every target is an existing Function entry in temp/ghidra-functions.csv.
- The ledger adds the controlling inbound edge 0x080a187a -> 0x080a38f8, giving 379 rows.
- No target lands in an active or historical §5.1 range. No target is an unapproved non-Function address outside Seg-6.
- Mandatory anti-confusion guard: 0x080a187a -> 0x080a38f8 is the Seg-6 tail edge. 0x080a18ba -> 0x080a0b20 is the separate Seg-5 historical reopen edge. Pre-apply must require both exact pairs and reject a swapped source.

## 9. Landing scope and synchronization plan

This executor does not land changes. After reviewer PASS, fixer scope is:

1. Ghidra changes only in [0x080a27a0,0x080a38fc): 184 slot actions, eight PLATE rewrites, tail R4, one Function create/name and one new PLATE.
2. One approved cross-range source projection exists: asm/13_equip_placement.s:8863 changes its call operand from SUB_080a38f8 to return_equip_row_type_13_complete after export. No instruction, Function, PLATE or EOL change is authorized at 0x080a187a.
3. Formal source scope is asm/13_equip_placement.s, constants/duel_field.inc for three constants and asm/rom.s for eight aliases. carve=0; no other asm module is in scope.
4. After normal export, mode injection and split, require no DAT_, DWORD_, PTR_DAT_, SUB_080a38f8 or .byte residue inside [0x080a27a0,0x080a38fc).
5. Refresh all four Function inventory outputs. Expected counts change from total=5212, named=5122, auto=90 to total=5213, named=5123, auto=90.
6. doc/dev/naming-proposals.csv has no row for 0x080a38f8. Do not create a historical scoring row for this refine-created Function. Existing Function rename=0, so name-cell sync=0.
7. Update activity and total progress only after persisted state, export, byte-identical build, inventory and source-scope gates pass. Until then Seg-6 remains pending R4 closure.

### 9.1 R9 backup, source snapshot and rollback gates

1. Before any Ghidra dry or apply, create a new timestamped physical copy of `ghidra/Yu-Gi-Oh WCT 2006.rep`. Enumerate current and backup recursively, require exactly 15 files on each side, and require every relative path, size and SHA256 to match. Preserve this backup until every landing gate has passed.
2. Freeze SHA256 for proposal, slots TSV, review, generated plan and final materialized script before dry. A hash mismatch is a closed-gate failure; the script must not widen or reduce the approved 184 slots, one R4 range, Function create, PLATE or EOL actions.
3. Before any formal export or source edit, take one physical source/scope snapshot over the complete landing surface, using the current working tree rather than Git as the baseline. Cover every present `asm/*.s` file, explicitly including all 25 `asm/NN_*.s` modules plus `asm/rom.s`; also cover `asm/includes.inc`, every `constants/*.inc`, the function-symbol registry `tools/ghidra-labeling/RenameKnownFunctions.py`, `doc/dev/naming-proposals.csv`, `temp/ghidra-functions.csv`, `temp/ghidra-functions-renamed.txt`, `temp/ghidra-functions-auto.txt`, `temp/ghidra-functions-summary.md`, `doc/dev/p5-refine-13-equip-placement.md`, `doc/dev/refine-progress.md`, and planned `tools/ghidra-labeling/RefineF13Seg6.py` plus `output/refine-run-20260831-194634/f13-seg6-plan.json`. Add every other formal path that the finalized landing runner can write before freezing this manifest. Record every path's prestate existence, size and SHA256; assert that the module glob resolves to exactly 25 `asm/NN_*.s` files. A prestate-absent path is recorded explicitly rather than omitted.
4. Run dry with fresh headless `-noanalysis -readOnly`; require preflight/final `FAIL=0` and the exact counts in section 10. Hash all 15 DB files before and after the process and require identical relative path, size and SHA256 tuples. Any dry failure, exception or DB mismatch triggers physical restore, 15/15 verification and fresh prestate verification, then stops the run.
5. Real apply must use one transaction and execute preflight, action, postcheck and save in that order. A failure or exception in transaction, postcheck or save requires transaction rollback when still open, immediate physical restore from the new `.rep` backup, deletion of extra database generations, 15/15 size+SHA256 equality, complete source/scope snapshot restore, and a fresh read-only full prestate check. Restore every prestate-present path byte-for-byte and delete every path recorded absent that the attempt created. Stop without export, build, success receipt, inventory sync or progress update.
6. After a successful save, start a separate fresh `-noanalysis -readOnly` process. Recheck all 184 actions and ROM values, five target Symbol/Data contracts, 14 REF slot Symbol/Data/reference contracts including unchanged bytes, 32 preserved references, R4 bytes/instructions/Function/body/APCS, nine PLATE, 184 EOL, direct-edge closure, carve=0 and §5.1=0. Hash the 15 DB files immediately before and after this persisted query and require exact equality.
7. Full-range export, mode removal, mode injection, split, 25-module boundary checks, `python tools/rom-export/export_all.py`, `NOPAUSE=1 build.bat`, source-scope checks and inventory checks are closed gates. Compare the complete snapshot surface path-by-path after the pipeline so that changes in any non-authorized asm module, includes file, constant file, registry, CSV, inventory, progress document or planned script/plan path are detectable. Only section 9 items 1-7 and their explicitly planned script/plan evidence may differ. Failure or an out-of-scope delta at any gate requires physical `.rep` restore, restoration of every prestate-present snapshot path, deletion of every prestate-absent path created by the attempt, and fresh prestate verification as in item 5; stop without recording a successful landing.
8. The final `output/2343.gba` must be exactly 33554432 bytes, byte-identical to `roms/2343.gba`, and have SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`. Only after ROM, persisted, source-scope and inventory gates pass may the landing receipt and progress documents record success.

## 10. C1-C13 executable acceptance

| criterion | required gate |
|---|---|
| C1 | Exact range [0x080a27a0,0x080a38fc), 16 preserved Functions plus one tail create, no address at or after 0x080a38fc. |
| C2 | Sole .byte block becomes two Thumb instructions and one Function; carve=0 and residual block=0. |
| C3 | §5.1=0; require tail packed raw=0 and THUMB|1=0 together with BL 0x080a187a -> 0x080a38f8. |
| C4 | Re-read all 184 ROM words; require EQ=138 and all five switch words byte exact. |
| C5 | Resolve every REUSE value; require exactly three new constants and eight new aliases without a same-domain conflict. |
| C6 | Require 184 unique lowercase slot labels and 11 collision-free new definition names. |
| C7 | Require the five exact target pre/post Symbol/Data contracts, 14 exact slot pre/post Symbol/Data/byte contracts and empty-to-exact REF tuples, 32 preserved gP1LifePoints refs and 138 EQ tuples; reject any alias, Data mutation or unapproved Symbol ID change. |
| C8 | Require nine final PLATE strings with no stale automatic symbol or caller. |
| C9 | Require nine PLATE and 184 EOL strings ASCII; every PLATE <=500 bytes. |
| C10 | Require all 11 odd callback slots equal Function+1; require five even switch targets byte exact. |
| C11 | Require exact tail body, two instructions, APCS contract, indegree=1 and existing Function rename=0. |
| C12 | Require a listed PC-relative consumer for each slot and recheck the three new constant semantics plus the 0x12a1 collision. |
| C13 | Require 184 slots, 189 words, 47 padding ranges, 1714 final instruction units, 3594 code bytes and 4444 total bytes without gaps or overlaps; require 378 segment-source edges plus one inbound edge and zero unapproved targets. |

Dry-run must fail closed unless the new physical backup and frozen-input gates pass and exact counts are EQ=138, REF=14, RENAME=32, Function create=1, existing Function rename=0, PLATE=9, EOL=184, R4=1 range, carve=0, §5.1=0 and errors=0. Persisted-state and regenerated-source checks must repeat the same counts and C7 dual-layer contracts before build verification. Any later gate failure follows the physical `.rep` plus source-snapshot restoration path in section 9.1.

## 11. 求助

None.

## Executor Report: F13-Seg-6

- 槽: EQ=138 REF=14 RENAME=32 FUNC_RENAME=0 PLATE=9
- Function create=1; EOL=184
- carve=0; disasm=1 range; §5.1=0
- 新增 constants/全局: 3 duel-field constants + 8 Thumb callback GAS aliases
- 求助: none
- proposal: doc/dev/refine/F13-Seg-6.proposal.md

## Fixer Mode A Report

Review items #1 through #4 are applied: C7 now freezes five target Symbol/Data objects and 14 REF slot/reference pre/post contracts; the 0x1d9e consumer evidence now records r2 low8 initialization and case-4 decrement; the 0x080a2c64 PLATE now states that a nonzero query result rejects the candidate; and R9 now defines physical `.rep` backup, source snapshot, failure restoration and fresh read-only DB-hash gates. Action counts remain EQ=138, REF=14 and RENAME=32; Function create=1, existing Function rename=0, PLATE=9 and EOL=184 are unchanged. This Mode A edit does not materialize or run a landing script and does not modify Ghidra, formal sources, progress, activity, CSV, inventory, build products, index or commits.

### Round 2 Mode A Fix Report

Round-2 items #1 through #3 are applied. Every REF slot now freezes its pre/post Data address, exact type, length=4, unchanged span and unchanged ROM bytes, with preflight/postcheck/receipt/fresh-persisted enforcement. The C7 observation is backed by a real headless gate manifest containing the complete command and arguments, `-noanalysis`, `-readOnly`, exit code 0, script/raw hashes, and exact-equal 15-file before/after DB manifests. The source/scope baseline now covers the complete exporter, split, inventory, registry, CSV, progress and planned-script surface, restores all prestate-present files, deletes attempt-created prestate-absent files, and does not use Git as the rollback baseline. Counts and semantic decisions are unchanged; no Mode B action, formal source edit, build, stage or commit was performed.
