# Refine Proposal: F10-Seg-7b  [0x08081900..0x08082290)

## 段测绘
- 范围: [0x08081900, 0x08082290), asm 行 16793..17819
- 函数入口 x12 (named):
  - 0x08081900  tick_equip_activation_display_3state          (line 16794)
  - 0x0808198c  dispatch_equip_activation_display_by_confirm_state (line 16868)
  - 0x080819cc  lookup_slot_display_value_by_card_id          (line 16906)
  - 0x08081b84  tick_equip_slot_display_by_card_id_3state     (line 17153)
  - 0x08081c54  dispatch_equip_display_by_type_flag_and_node_activity (line 17259)
  - 0x08081ce8  tick_equip_effect_slot_display_state          (line 17336)
  - 0x08081d9c  push_effect_slot_by_player_from_node          (line 17432)
  - 0x08081db0  push_effect_slot_by_opponent_from_node        (line 17444)
  - 0x08081dcc  enqueue_equip_slot_sprite_from_base_offset    (line 17465)
  - 0x08081de4  check_effect_node_handler_for_slot            (line 17479)
  - 0x08081e10  tick_equip_activation_display_5state          (line 17510)
  - 0x08081f28  tick_equip_activation_display_with_card_routing (line 17659)
- 残留自动名槽 x55 (python exhaustive count confirmed):
  DAT_0808191c, DAT_08081948, PTR_gP1LifePoints_08081974,
  DAT_08081978, DAT_080819b8,
  DAT_08081a00, DAT_08081a04, DAT_08081a08, DAT_08081a10,
  DAT_08081a28, DAT_08081a3c, DAT_08081a5c, DAT_08081a70,
  DAT_08081a88, DAT_08081a9c,
  PTR_gP1LifePoints_08081ad0, PTR_gP1LifePoints_08081af4,
  DAT_08081b70, DAT_08081b74, DAT_08081bb8, DAT_08081bf4,
  DAT_08081c84, DAT_08081c88, DAT_08081ca8, DAT_08081cd0, DAT_08081cd4,
  DWORD_08081d04, DWORD_08081d28, DWORD_08081d2c, DWORD_08081d54,
  DWORD_08081d58, DWORD_08081d98, DWORD_08081de0,
  DAT_08081e30, DAT_08081e34, DAT_08081e64, DAT_08081e90, DAT_08081e94,
  DAT_08081ec0, DAT_08081ec4,
  PTR_gP1LifePoints_08081efc, DAT_08081f00, DAT_08081f04, DAT_08081f1c,
  DAT_08081f48, DAT_08081f7c, DAT_08081f80, DAT_08081f8c,
  DAT_08081fd8, DAT_08081fdc,
  PTR_gP1LifePoints_08082014, DAT_08082018, DAT_0808201c,
  DAT_08082020, DAT_08082038
  = 55 total unique auto-name slots
- ROM_INCBIN blocks x2:
  - BLK1: 0x82046..0x82140 (size 0xfa). DAT label not present (unlabeled incbin).
    - 0x82046: 0x0000 (2B pad/alignment)
    - 0x82048: fn_routing for PENGUIN_SOLDIER_CID (0x1200). THUMB fn, 1 genuine FS-table ref (0x08082049 at ROM off 0x1e43428 = FS entry CID=0x1200, offset +0x14 = fn_routing slot). Ref-scan: raw=0 hits, THUMB+1=1 genuine hit. BL callers: count_effect_node_activations_by_zone (0x080907f4), enqueue_equip_slot_sprite_with_code_rotation (0x08080c9c x2), format_game_text_with_int_arg (0x080aefc4), set_equip_activation_state_by_mode_alt (0x080905e8).
    - 0x82134..0x82140: literal pool (6 words: 0x0201e2a0, 0xfffc7fff, 0x00000868, 0x0201c510, 0x0201b290, 0x08082140)
    - 0x08082140: jump table start (ptr to BLK2 sub-stubs, raw-ptr dispatch via .hword 0x4687 at 0x08082134)
  - BLK2: 0x82158..0x82290 (size 0x138). DAT_08082158: ROM_INCBIN label already present.
    - 6 sub-stubs reached via raw-ptr jump table at 0x8082140 (JT has 6 entries, raw addresses, no THUMB+1):
      sub0=0x08082158, sub1=0x08082190, sub2=0x080821bc,
      sub3=0x08082214 (4B: `movs r0,#0x75; b <somewhere>`),
      sub4=0x08082218, sub5=0x08082240
    - Ref-scan confirms raw refs from JT only (no genuine THUMB+1 FS-table refs for any BLK2 sub-stub).
    - BL targets in BLK2 sub-stubs: count_effect_node_zone_activations (0x08090714), invoke_card_display_op_0x31_sub1 (0x080933b4), set_equip_activation_state_by_mode__08096a4c (0x08096a4c), enqueue_equip_slot_sprite_with_code_rotation (0x08080c9c), check_activation_display_state_is_confirmed (0x08096b14)
    - BLK2 exit: pop {r1}; bx r1 at 0x08082288 (last stub, Sub-case E)
- switchD_08081e2c: fully decoded -- 5 case labels (switchD_08081e2c__caseD_0/1/2/3/default) present in asm. No R4 action needed. Jump table at DAT_08081e38 (5 entries = cases 0..4, case 4 same as case 2).
  Evidence: asm lines 17526-17644 have all case labels. Confirmed.

## 数据块分类 (Rule 2/3) -- ref-scan

| 块 | ref-scan (raw / THUMB+1) | 判定 | 理由 |
|-----|--------------------------|------|------|
| BLK1 0x82046/0xfa | raw=0 / THUMB+1=1 (genuine FS table 0x1e43428) | R4 disasm | THUMB fn at 0x82048 = fn_routing for PENGUIN_SOLDIER (CID=0x1200), confirmed by FS entry layout: entry base 0x1e43414 -> [+0x00]=0x1200, [+0x04]=0x080676e1, [+0x08]=0x080509fd, [+0x14]=0x08082049 |
| BLK2 0x82158/0x138 | sub0: raw=1 (JT), sub3: raw=2 (JT+0x8a0c456 compressed), THUMB+1 hits all in compressed data | R4 disasm | 6 sub-stubs reached via raw-ptr jump table at 0x8082140; raw refs outside JT are in compressed card data (0x08a0c456, 0x08d8a9cc, 0xe28943) = coincidental; no genuine FS THUMB+1 refs; R4 disasm all 6 stubs |

Note: 0x08082049 is mid-code (BLK1 fn+1). No USER label may be added at +1 addr per THUMB fn-ptr rule. The FS table entry already refers to it as raw 0x08082049.

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate)

All 55 slots are literal-pool words. Classified by value:

**REUSE (constants already in constants/*.inc):**

| slot | value | const_name | inc_file |
|------|-------|-----------|---------|
| DAT_0808191c | 0x0201b290 | gDuelPhaseFlags | ewram.inc |
| DAT_08081bb8 | 0x0201b290 | gDuelPhaseFlags | ewram.inc |
| DWORD_08081d04 | 0x0201b290 | gDuelPhaseFlags | ewram.inc |
| DWORD_08081d58 | 0x0201b290 | gDuelPhaseFlags | ewram.inc |
| DAT_08081e30 | 0x0201b290 | gDuelPhaseFlags | ewram.inc |
| DAT_08081e64 | 0x0201b290 | gDuelPhaseFlags | ewram.inc |
| DAT_08081e94 | 0x0201b290 | gDuelPhaseFlags | ewram.inc |
| DAT_08081ec4 | 0x0201b290 | gDuelPhaseFlags | ewram.inc |
| DAT_08081f04 | 0x0201b290 | gDuelPhaseFlags | ewram.inc |
| DAT_08081f1c | 0x0201b290 | gDuelPhaseFlags | ewram.inc |
| DAT_08081f48 | 0x0201b290 | gDuelPhaseFlags | ewram.inc |
| DAT_08081fdc | 0x0201b290 | gDuelPhaseFlags | ewram.inc |
| DAT_08082020 | 0x0201b290 | gDuelPhaseFlags | ewram.inc |
| DAT_08082038 | 0x0201b290 | gDuelPhaseFlags | ewram.inc |
| DAT_080819b8 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc |
| DAT_08081ca8 | 0x0201b290 | gDuelPhaseFlags | ewram.inc |
| DAT_08081c84 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc |
| DWORD_08081d28 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc |
| DAT_08081b70 | 0x00000868 | PLAYER_BLOCK_STRIDE | duel_field.inc |
| DAT_08081b74 | 0x0201c510 | gDuelFieldSlots | ewram.inc |
| DAT_08081bf4 | 0xfffc7fff | DISPLAY_CODE_CLEAR_MASK | (new in 7a -- duel_field.inc) |
| DAT_08081978 | 0x00001d68 | ELIGIB_SPRITE_CTRL_OFF | ewram.inc |
| DAT_08081f00 | 0x00001d68 | ELIGIB_SPRITE_CTRL_OFF | ewram.inc |
| DAT_08082018 | 0x00001d68 | ELIGIB_SPRITE_CTRL_OFF | ewram.inc |
| DAT_0808201c | 0x00001d6c | ELIGIB_ANIM_STATE_OFF | ewram.inc |
| DAT_08081c88 | 0x000010d3 | TRIGGER_OP_PARAM_10D3 | duel_field.inc |
| DAT_08081cd0 | 0x000010d3 | TRIGGER_OP_PARAM_10D3 | duel_field.inc |
| DWORD_08081d54 | 0x00000197 | lookup_equip_score_mooyan_p0 | duel_field.inc |
| DWORD_08081de0 | 0x0201bb90 | gEquipChainSlotRefs | ewram.inc |
| DAT_08081a00 | 0x000017f5 | (new) LEVEL_UP_CID | card_info.inc |
| DAT_08081a04 | 0x0000169f | PANDEMONIUM_CID | card_info.inc |
| DAT_08081a08 | 0x0000140b | INSECT_IMITATION_CID | card_info.inc |
| DAT_08081a28 | 0x00001745 | THE_KICK_MAN_CID | card_info.inc |
| DAT_08081a3c | 0x00001768 | NINJITSU_ART_OF_TRANSFORMATION_CID | card_info.inc |
| DAT_08081a5c | 0x0000198e | (new) INFERNO_RECKLESS_SUMMON_CID | card_info.inc |
| DAT_08081a88 | 0x000019d8 | TRIAL_OF_THE_PRINCESSES_CID | card_info.inc |
| DAT_08081a9c | 0x000019dd | GENERATION_SHIFT_CID | (new in 7a -- card_info.inc) |
| DAT_08081a70 | 0x00001927 | SPIRITUAL_EARTH_ART_CID | card_info.inc |
| DAT_08081a10 | 0x0000164a | (new) GUARDIAN_ELMA_CID | card_info.inc |
| DAT_08081f7c | 0x000017ea | NOBLEMAN_EATER_BUG_CID | card_info.inc |
| DAT_08081f80 | 0x000011f0 | GREENKAPPA_CID | card_info.inc |
| DAT_08081f8c | 0x0000184a | XING_ZHEN_HU_CID | card_info.inc |

**C5 dedup notes (by value, grep constants/*.inc):**
- 0x0201b290: gDuelPhaseFlags -- REUSE (ewram.inc line 317+)
- 0xfffc7fff: DISPLAY_CODE_CLEAR_MASK -- new in 7a proposal, 0 hits in current constants
- 0x000010d3: TRIGGER_OP_PARAM_10D3 -- REUSE (duel_field.inc line 314)
- 0x00000197: lookup_equip_score_mooyan_p0 -- REUSE (duel_field.inc line 321)
- 0x0201bb90: gEquipChainSlotRefs -- REUSE (ewram.inc line 317)
- 0x000017f5: 0 hits in constants/ -> NEW LEVEL_UP_CID
- 0x0000198e: 0 hits in constants/ -> NEW INFERNO_RECKLESS_SUMMON_CID
- 0x0000164a: 0 hits in constants/ -> NEW GUARDIAN_ELMA_CID
- All others above: confirmed present in respective inc files

**RENAME_SLOTS (label rename; no equate):**

Three categories of slots that get a rename (label change) rather than equate:

1. **THUMB fn-ptr slots** (raw fn-ptr +1 = cannot be a GAS label; keep raw hex + EOL comment):

| slot | value | action |
|------|-------|--------|
| DAT_08081948 | 0x080905e9 | RENAME -> tick_equip_act_3state_mode_alt_ptr; EOL: "set_equip_activation_state_by_mode_alt+1 (THUMB fn-ptr)" |
| DAT_08081cd4 | 0x080905e9 | RENAME -> disp_by_type_mode_alt_ptr; EOL: "set_equip_activation_state_by_mode_alt+1 (THUMB fn-ptr)" |
| DAT_08081e90 | 0x08081de5 | RENAME -> effect_node_handler_slot_check_ptr_a; EOL: "check_effect_node_handler_for_slot+1 (THUMB fn-ptr)" |
| DAT_08081ec0 | 0x08081de5 | RENAME -> effect_node_handler_slot_check_ptr_b; EOL: "check_effect_node_handler_for_slot+1 (THUMB fn-ptr)" |
| DAT_08081fd8 | 0x08081de5 | RENAME -> effect_node_handler_slot_check_ptr_c; EOL: "check_effect_node_handler_for_slot+1 (THUMB fn-ptr)" |

Note: The value 0x08081de5 = check_effect_node_handler_for_slot+1 (fn at 0x08081de4). Three occurrences in 7b; each gets a distinct suffix _a/_b/_c per fn context (switchD caseD_1, caseD_3, tick_equip_activation_display_with_card_routing state 1/2).

2. **PTR_gP1LifePoints_xxxxxxxx** slots (already correctly point to gP1LifePoints symbol; keep as is, no action needed -- label is auto-generated name but value is a REF to known symbol. Fixer: skip PTR_ class per scope conventions):

Slots: PTR_gP1LifePoints_08081974, PTR_gP1LifePoints_08081ad0, PTR_gP1LifePoints_08081af4, PTR_gP1LifePoints_08081efc, PTR_gP1LifePoints_08082014 -- all = gP1LifePoints (already a named symbol). No equate needed; existing label acceptable per refine-batch-scope-conventions (shared global single label). Skip.

3. **switchD data pointer** slot:

| slot | value | action |
|------|-------|--------|
| DAT_08081e34 | 0x08081e38 | RENAME -> tick_equip_5state_switch_table_ptr; EOL: "ptr to switchdataD_08081e38 (5-entry jump table)" |

### FUNC_RENAME (misname corrections)
None detected. All 12 named functions have plate descriptions consistent with function bodies.
Evidence: plates read at lines 16793-17819, all ASCII (except mojibake lines handled in PLATE section).

### PLATE (R5; mojibake ASCII rewrites)

**Mojibake lines in 7b (UTF-8 CJK encoded double-UTF-8 mojibake via Ghidra Jython):**

13 plate/comment lines contain CJK bytes (latin-1 multi-byte sequences). Each must be rewritten as ASCII via setPlateComment/setEOLComment.

| line | addr | fn | ASCII rewrite |
|------|------|-------|------|
| 16867 | 0x0808198c | dispatch_equip_activation_display_by_confirm_state | "Equip activation display routing hub (indeg=8). Called by 8 callers (0x080833a8/0x0808416c/0x08084180/0x08084460/0x08084594/0x08084d08/0x08084e2c/0x080852e4, all equip/activation routing layer). Receives card_entry_ptr(r0) and secondary_ptr(r1). Reads gActivationConfirmTable(0x0201e2a0)+[player_id*4+8] confirm_flag; if==1 calls select_equip_target_slot_by_effect_strategy; else calls tick_equip_activation_display_3state. Exit pop {r1};bx r1 Sub-case E." |
| 17147 | 0x08081b84 | tick_equip_slot_display_by_card_id_3state | "Equip slot display 3-state machine, dispatches by card_id. Receives effect_node_ptr(r0). Calls lookup_slot_display_value_by_card_id for card_id display value. Reads state from [IWRAM_BASE+0x4b0]. State 0: calls dispatch_effect_handler_by_card_id; if handler returns nonzero calls trigger_card_display_op31_if_not_active then advances +1 returns 0 (in-progress); if 0 and flag not set returns -1. State 1: trigger_card_display_op31_if_not_active + init_effect_slot_display_context then advances +1 returns 0. State 2: pack_equip_slot_sprite_with_code_attr then returns 1 (done). Other states: returns 1." |
| 17258 | 0x08081c54 | dispatch_equip_display_by_type_flag_and_node_activity | "Equip display routing fn (indeg=4). Called by 0x08083c98/0x080843fc/0x08084674/0x08084d3c. Reads card_entry[+3] bits[5:4]: if==0x20 (direct type flag) returns 1 directly; if confirm_flag==1 calls select_equip_target_slot_by_effect_strategy(strategy=0x10d3); else by count_effect_node_zone_activations result: nonzero -> trigger_card_display_op31_if_not_active(op=0x65) + set_equip_activation_state_by_mode; zero -> tick_equip_activation_display_3state. Exit pop {r1};bx r1 Sub-case E." |
| 17459 | 0x08081dcc | enqueue_equip_slot_sprite_from_base_offset | "Small equip sprite enqueue fn. Receives effect_node_ptr(r0). Reads from fixed base [0x0201bb90]+0 and [0x0201bb90]+0x1c as two params, then calls enqueue_equip_slot_sprite_with_code_rotation to enqueue sprite rotation attr. Always returns 1." |
| 17462 | 0x08081dcc | enqueue_equip_slot_sprite_from_base_offset (Constants comment) | "Constants: BASE_PTR=0x0201bb90 (gEquipChainSlotRefs), OFFSET_A=0x0, OFFSET_B=0x1c" |
| 17463 | same | field offset comment A | Remove (merge into 17462 rewrite above) |
| 17464 | same | field offset comment B | Remove (merge into 17462 rewrite above) |
| 17478 | 0x08081de4 | check_effect_node_handler_for_slot | "Effect node dual-check predicate, referenced by multiple fn-ptr tables. Receives effect_node_ptr(r0). First calls invoke_effect_node_handler_3arg to invoke node 3-arg handler; if nonzero calls find_effect_slot_by_side_and_type to find matching slot; if found returns 0. If handler returns 0 and no matching slot, returns 1. Return 0 means active condition holds; return 1 means condition not met. fn-ptr addr 0x08081de5 loaded into fn-ptr tables by 5 callers." |
| 17503 | 0x08081e10 | tick_equip_activation_display_5state | "Equip activation display 5-state machine. Receives effect_node_ptr(r0). Reads state from [IWRAM_BASE+0x4b0]. State 0: count_effect_node_zone_activations; State 1: trigger_card_display_op31_if_not_active(op=0x94)+set_equip_activation_state_by_mode, advance +1, return 0; State 2: check_activation_display_state_is_confirmed, if confirmed enqueue_equip_slot_sprite_with_code_rotation and advance +1; State 3: trigger_card_display_op31_if_not_active(op=0x6a)+set_equip_activation_state_by_mode, advance +1, return 0; Default(>=4): advance +1 returns 1. Extension of tick_equip_activation_display_3state (0x08081900) with 2 extra states." |
| 17508 | 0x08081e10 | tick_equip_activation_display_5state (Constants comment A) | "Constants: IWRAM_BASE=0x0201b290, STATE_OFFSET=0x4b0 (0x96*8)" |
| 17509 | same (Constants comment B) | "OP_CODE_A=0x94 (state 1), OP_CODE_B=0x6a (state 3)" |
| 17651 | 0x08081f28 | tick_equip_activation_display_with_card_routing | "Equip activation display 4-state machine with card_id routing. Receives effect_node_ptr(r0). Reads [IWRAM_BASE+0x4b0] state. State 0: count_effect_node_zone_activations; if card_id==0x17ea (Nobleman-Eater Bug) or 0x184a (Xing Zhen Hu) calls format_game_text_with_int_arg then trigger; if card_id==0x11f0 (Greenkappa) calls format_game_text_with_int_arg(slot=0x71); else direct trigger+set_equip_activation_state_by_mode_alt. States 2/3: check_activation_display_state_is_confirmed -> enqueue_equip_slot_sprite_with_code_rotation, advance +1. Exit pop {r1};bx r1 Sub-case E." |
| 17658 | 0x08081f28 | tick_equip_activation_display_with_card_routing (Constants comment) | "Constants: IWRAM_BASE=0x0201b290, STATE_OFFSET=0x4b0, CARD_ID_A=0x17ea (Nobleman-Eater Bug), CARD_ID_B=0x11f0 (Greenkappa), CARD_ID_C=0x184a (Xing Zhen Hu), FORMAT_TEXT_SLOT=0x9b" |

**C8 stale FUN_ in 7b range:**

| line | plate text | fix |
|------|-----------|-----|
| 16902 | "FUN_08081900" in plate of lookup_slot_display_value_by_card_id | replace FUN_08081900 -> tick_equip_activation_display_3state |

Evidence: line 16902 plate: "Called by FUN_08081900 (card-display activation flow) and over ten duel_field activation functions..." -- fn at 0x08081900 is named tick_equip_activation_display_3state.

## carve 计划 (R7) -- BLK2 DAT_08082158 already labeled

BLK2 (0x82158..0x82290) has DAT_08082158 label. The 6 sub-stubs accessed via raw-ptr jump table from BLK1 fn do NOT require carving from rom.s (they are already part of the asm file as ROM_INCBIN 0x82158/0x138 with label). The fixer's R4 disasm action (below) will disassemble them in place.

BLK1 (0x82046..0x82140) has no label. The fn at 0x82048 (fn_routing for Penguin Soldier CID=0x1200) is reached only via THUMB+1 FS table ref. The jump table at 0x82140..0x82157 is between BLK1 and BLK2 and is already decoded as `.word` entries (lines 17812-17817). No carve into rom.s needed for BLK1 since it is an incbin block within the main asm file -- R4 disasm will handle it in Ghidra.

## disasm 计划 (R4)

**BLK1 fn (0x82048..0x82133, size 0xec bytes = fn body; literal pool 0x82134..0x8213f):**
- createFunction at 0x08082048 (THUMB mode already set by surrounding code)
- Name: `route_penguin_soldier_equip_display`
  Evidence: FS table entry CID=0x1200 (PENGUIN_SOLDIER_CID) -> fn_routing slot at +0x14 -> 0x08082049. BL callers include count_effect_node_activations_by_zone, enqueue_equip_slot_sprite_with_code_rotation, set_equip_activation_state_by_mode_alt. Plate: "fn_routing for PENGUIN_SOLDIER_CID(0x1200). Received via FS table entry 0x09e43414 [CID=0x1200, fn_activate=0x080676e1, fn_eligible=0x080509fd, fn_routing=0x08082049]. Drives equip display state machine with sub-stub dispatch via raw-ptr jump table at 0x08082140."
  [confidence: high; FS table evidence ROM off 0x1e43414]
- setTMode for range [0x08082046, 0x08082140) to ensure THUMB decoding
- DisassembleCommand per-instruction (not single range; sub-stub dispatch body contains .hword 0x4687 = mov pc,r0)
- Note: 0x82046..0x82047 = 0x0000 padding; skip (not a fn entry)
- Literal pool entries needing equates within BLK1 fn:
  - 0x0808210c: gDuelCardCtxBase (REUSE)
  - 0x08082110: DISPLAY_CODE_CLEAR_MASK (new in 7a)
  - 0x08082114: PLAYER_BLOCK_STRIDE (REUSE)
  - 0x08082118: gDuelFieldSlots (REUSE)
  - 0x08082138: gDuelPhaseFlags (REUSE)
  - 0x0808213c: 0x08082140 -> rename to `route_penguin_soldier_jump_table_ptr`; EOL "ptr to raw-ptr jump table for 6 equip display sub-stubs"

**BLK2 sub-stubs (0x82158..0x82290):**
- 6 sub-stubs accessed via raw-ptr jump table from BLK1 fn:
  - sub0: 0x08082158, size=0x38. Name: `route_penguin_soldier_equip_sub0`
    BL callers: count_effect_node_zone_activations (0x08090714), invoke_card_display_op_0x31_sub1 (0x080933b4). Plate: "Sub-stub 0 of Penguin Soldier equip display: reached via JT[0]=0x08082158. Calls count_effect_node_zone_activations + invoke_card_display_op_0x31_sub1."
  - sub1: 0x08082190, size=0x2c. Name: `route_penguin_soldier_equip_sub1`
    BL caller: set_equip_activation_state_by_mode__08096a4c (0x08096a4c). Plate: "Sub-stub 1: reached via JT[1]=0x08082190. Calls set_equip_activation_state_by_mode__08096a4c."
  - sub2: 0x080821bc, size=0x58. Name: `route_penguin_soldier_equip_sub2`
    BL callers: check_activation_display_state_is_confirmed (0x08096b14), enqueue_equip_slot_sprite_with_code_rotation (0x08080c9c), count_effect_node_zone_activations (0x08090714). Plate: "Sub-stub 2: reached via JT[2]=0x080821bc. Calls check_activation_display_state_is_confirmed; if confirmed calls enqueue_equip_slot_sprite_with_code_rotation."
  - sub3: 0x08082214, size=0x4. Name: `route_penguin_soldier_equip_sub3`
    Body: `movs r0,#0x75; b <somewhere>`. Plate: "Sub-stub 3: reached via JT[3]=0x08082214. 4-byte stub: sets r0=0x75 then branches."
  - sub4: 0x08082218, size=0x28. Name: `route_penguin_soldier_equip_sub4`
    BL caller: set_equip_activation_state_by_mode__08096a4c. Plate: "Sub-stub 4: reached via JT[4]=0x08082218. Calls set_equip_activation_state_by_mode__08096a4c."
  - sub5: 0x08082240, size=0x50. Name: `route_penguin_soldier_equip_sub5`
    BL callers: check_activation_display_state_is_confirmed (0x08096b14), enqueue_equip_slot_sprite_with_code_rotation (0x08080c9c). Exit: pop {r1};bx r1 at 0x08082288. Plate: "Sub-stub 5: reached via JT[5]=0x08082240. Calls check_activation_display_state_is_confirmed; if confirmed calls enqueue_equip_slot_sprite_with_code_rotation. Exit Sub-case E."
- Per-stub DisassembleCommand: issue DisassembleCommand per 2-byte unit starting at each sub-stub (not single range -- Ghidra may mis-identify boundaries without per-unit disasm)
- setTMode for range [0x08082158, 0x08082290) before disasm

## 新増 constants (7b)

**card_info.inc additions (NEW, C5 confirmed 0 hits in constants/ by value):**
- LEVEL_UP_CID = 0x000017f5  (Level Up! pw=25290459; card-stats.s L21673)
- INFERNO_RECKLESS_SUMMON_CID = 0x0000198e  (Inferno Reckless Summon pw=12247206; card-stats.s L26106)
- GUARDIAN_ELMA_CID = 0x0000164a  (Guardian Elma pw=74367458; card-stats.s L17110)

Note: DISPLAY_CODE_CLEAR_MASK (0xfffc7fff) and GENERATION_SHIFT_CID (0x000019dd) are listed as new in 7a; when 7a is applied they will exist in constants/ before 7b fixer runs.
Note: TRIGGER_OP_PARAM_10D3 (0x000010d3) is already in duel_field.inc -- REUSE, no new addition.

## §5.1 登记 (Rule 3)
No 0-reference blocks in [0x08081900, 0x08082290).
- BLK1 (0x82048): 1 genuine FS-table THUMB+1 ref at 0x1e43428 -> must disasm (R4, not §5.1)
- BLK2 (0x82158): reached via raw-ptr JT from BLK1 fn -> must disasm (R4, not §5.1)
- switchD_08081e2c: already decoded, no §5.1

## 消費者証拠 (R6) -- 重要槽語義

- DAT_0808191c (0x0201b290): tick_equip_activation_display_3state line 16798 `ldr r0, DAT_0808191c; movs r1,#0x96; lsls r1,r1,#3; adds r5,r0,r1` -> gDuelPhaseFlags+0x4b0 state counter [confidence: high]
- DAT_08081948 (0x080905e9): line 16823 loaded as r2 for `bl set_equip_activation_state_by_mode__08096a4c @ 0808193c` [confidence: high; set_equip_activation_state_by_mode_alt at 0x080905e8, +1 = THUMB fn-ptr]
- DAT_08081978 (0x00001d68): line 16836 `ldr r3, DAT_08081978; adds r1,r0,r3; ldr r1,[r1,#0x0]` -> [gP1LifePoints+0x1d68] = ELIGIB_SPRITE_CTRL_OFF access [confidence: high]
- DAT_08081a00 (0x000017f5): line 16910 `ldr r0, DAT_08081a00; cmp r1,r0` = BST root cmp in lookup_slot_display_value_by_card_id; card 0x17f5 = Level Up! (card-stats.s L21673) [confidence: high]
- DAT_08081a10 (0x0000164a): line 16945 `ldr r0, DAT_08081a10; b LAB_08081a20; cmp r1,r0; beq LAB_08081aa0` -> Guardian Elma CID 0x164a from card-stats.s L17110 [confidence: high]
- DAT_08081a5c (0x0000198e): line 16988 BST node cmp for Inferno Reckless Summon (card-stats.s L26106) [confidence: high]
- DAT_08081bf4 (0xfffc7fff): line 17187 `ldr r1, DAT_08081bf4; ands r0,r1` -> DISPLAY_CODE_CLEAR_MASK, clear bits[17:15] from effect_node [+4] display_code rotation field [confidence: high; same semantic as 7a DAT_08080d14/d68]
- DAT_08081ca8 (0x0201b290): line 17302 `ldr r0, DAT_08081ca8` -> gDuelPhaseFlags base; used in dispatch_equip_display_by_type_flag_and_node_activity to read state offset [confidence: high; same value 0x0201b290 = gDuelPhaseFlags, ewram.inc line 317+]
- DAT_08081c84 (0x0201e2a0): line 17268 `ldr r0, DAT_08081c84; lsls r1,r1,#2; adds r0,#8; adds r1,r1,r0; ldr r0,[r1]` -> gDuelCardCtxBase + player_id*4+8 confirm_flag read [confidence: high]
- DAT_08081c88 (0x000010d3): line 17278 `ldr r2, DAT_08081c88; bl select_equip_target_slot_by_effect_strategy` -> strategy param 0x10d3 = TRIGGER_OP_PARAM_10D3 (duel_field.inc line 314) [confidence: high]
- DWORD_08081d54 (0x00000197): line 17377 `ldr r2, DWORD_08081d54` -> r2=0x197 = 2nd param to `invoke_card_display_op_0x31_sub3_with_packed_params`. Context: plate says "r1=0xcb*2=0x196, r2=0x197"; 0x197 is pre-existing lookup_equip_score_mooyan_p0 equate (duel_field.inc line 321). REUSE -- same value, distinct semantic but same constant [confidence: high; C5 grep confirmed 0x00000197 = 1 hit]
- DWORD_08081de0 (0x0201bb90): line 17467 `ldr r2, DWORD_08081de0; ldr r1,[r2,#0x0]; ldr r2,[r2,#0x1c]; bl enqueue_equip_slot_sprite_with_code_rotation` -> gEquipChainSlotRefs base [confidence: high]
- DAT_08081e90/ec0/fd8 (0x08081de5): check_effect_node_handler_for_slot+1 (THUMB fn-ptr) loaded as r2 to set_equip_activation_state_by_mode__08096a4c as mode selector fn-ptr [confidence: high; fn at 0x08081de4 confirmed by asm]
- DAT_08081f7c (0x000017ea): line 17694 BST cmp in tick_equip_activation_display_with_card_routing for Nobleman-Eater Bug CID [confidence: high; card_info.inc line 756]
- DAT_08082018 (0x00001d68): line 17784 `ldr r2, DAT_08082018; adds r1,r0,r2; ldr r1,[r1,#0x0]` -> [gP1LifePoints+0x1d68] ELIGIB_SPRITE_CTRL_OFF [confidence: high]
- DAT_0808201c (0x00001d6c): line 17786 `ldr r3, DAT_0808201c; adds r2,r0,r3` -> [gP1LifePoints+0x1d6c] ELIGIB_ANIM_STATE_OFF [confidence: high; ewram.inc line 423]

## C13 残留 100% 覆盖 (Seg-7b)

Python count of unique auto-name slots with addresses in [0x8081900, 0x8082290): **55 slots**

Breakdown (python-verified):
- EQ_SLOTS (pure equate, excludes PTR_/gP1LifePoints DWORD + THUMB fn-ptr + switchD table ptr): 42  (41 previously listed + DAT_08081ca8 added per review #2)
- RENAME_SLOTS: 6
  - THUMB fn-ptr renames: 5 (DAT_08081948, DAT_08081cd4, DAT_08081e90, DAT_08081ec0, DAT_08081fd8)
  - switchD table ptr: 1 (DAT_08081e34)
- PTR_/gP1LifePoints skip: 7
  - PTR_gP1LifePoints_*: 5 (08081974, 08081ad0, 08081af4, 08081efc, 08082014)
  - DWORD_gP1LifePoints: 2 (DWORD_08081d2c, DWORD_08081d98)
  Per scope conventions: shared global gP1LifePoints symbol, single label, no rename/equate action.
- Total covered: 42 EQ + 6 RENAME + 7 PTR_skip = 55 = 100%

C13 summary: 55 slots, 100% coverage.
EQ=42, RENAME=6 (5 THUMB fn-ptr + 1 switchD table ptr), PTR_skip=7 (5 PTR_gP1LifePoints + 2 DWORD_gP1LifePoints at d2c/d98).

## Executor Report: F10-Seg-7b
- 槽: EQ=42 REF=0 RENAME=6 FUNC_RENAME=0 PLATE=13mojibake+1(C8)=14
- carve=0 disasm=BLK1(1fn+literal pool)+BLK2(6sub-stubs) §5.1=0
- switchD=already decoded (no action)
- 新增 constants/全局: LEVEL_UP_CID(0x17f5), INFERNO_RECKLESS_SUMMON_CID(0x198e), GUARDIAN_ELMA_CID(0x164a) -> card_info.inc; DISPLAY_CODE_CLEAR_MASK/GENERATION_SHIFT_CID from 7a applied first
- 求助: none
- proposal: doc/dev/refine/F10-Seg-7b.proposal.md
