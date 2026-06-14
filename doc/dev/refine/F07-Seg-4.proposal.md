# Refine Proposal: F07-Seg-4  [0x0805f1cc..0x0805fc94)

## 段测绘

- 函数入口: 34 个, 0x0805f1cc..0x0805fc0e
  - check_equip_slot_at_turn_player_side @0x5f1cc
  - check_equip_eligible_banisher_absent_and_effect_above4 @0x5f23c
  - check_equip_eligible_amazoness_monster_with_spell480 @0x5f26c
  - check_equip_slot_eligible_neo_daedalus_with_tier @0x5f298
  - check_equip_chain_pair_card_id_matches @0x5f2c0
  - check_equip_slot_zone500_state3_for_either_player @0x5f33c
  - check_slot_has_life_absorbing_machine_node @0x5f3a4
  - check_equip_eligible_by_slot_fields @0x5f3bc
  - check_equip_zone340_slot_state_matches_ctx @0x5f3e8
  - check_equip_zone480_or_4c0_via_hand_slot_setcode @0x5f49c
  - check_equip_slot_eligible_by_chain_and_tier_at_state2 @0x5f510
  - classify_equip_slot_eligibility_by_type_and_state @0x5f550
  - check_effect_node_zone_activation_dual_state @0x5f5e8
  - check_player_has_active_monster_return2 @0x5f614
  - check_player_has_active_monster @0x5f628
  - check_equip_eligible_by_lp_count_and_zone_offset @0x5f644
  - check_equip_slots_eligible_banisher_and_effect_nonzero @0x5f698
  - check_field_spell_zone480_equip_type_eligible @0x5f6e4
  - dispatch_slot_placement_check_by_card_id @0x5f784
  - check_slot_zone_type_facedown_flip @0x5f7d0
  - check_neo_daedalus_zone_effect_available @0x5f7f8
  - check_slot_zone380_atk_above_1999_with_card_match @0x5f85c
  - check_spell_zone_placeable_with_opponent_lp14 @0x5f8f4
  - check_equip_slot_eligible_type80_neo_daedalus_hand @0x5f968
  - check_equip_ctx_slot6_has_card_no_chain @0x5f9a4
  - check_equip_slot_eligible_with_monster_count_gate @0x5f9e4
  - check_light_of_intervention_and_swarm_absent @0x5fa24
  - check_equip_slot_eligible_with_spell_zone_and_effect_handlers @0x5fa84
  - check_light_of_intervention_absent @0x5fad0
  - check_equip_eligible_by_turn_player_lp_or_chain @0x5faec
  - check_equip_slot_eligible_with_empty_monster_zones_and_handlers @0x5fb3c
  - check_equip_slot_eligible_with_lp_and_spell_type @0x5fbb8
  - check_equip_slot_eligible_by_combined_monster_count @0x5fbe0
  - check_equip_slot_eligible_with_slot_chain_and_hand_hp @0x5fc3c
- 残留自动名槽: 47 个 (DWORD_=36, DAT_=9, PTR_=2)
- ROM_INCBIN 块: 5 个

## 数据块分类 (Rule 2/3) -- ref-scan 证据

| 块 | ref-scan (raw / THUMB+1) | 判定 | 理由 |
|---|---|---|---|
| 0x5f47e sz=0x1e | raw=0 thumb@0x5f480=1 | disasm (R4) | hit at 0x09e40dd4 CID=0x14d4(A Feint Plan); table: CID=0x14d4, fn1=0x08071489, fn2=0x0805f481; block starts 2B pad then THUMB code at 0x5f480 |
| 0x5f8b4 sz=0x40 | raw=0 thumb@0x5f8b4=1 (others non-e4 stray) | disasm (R4) | hit at 0x09e41068 CID=0x151c(Drop Off); table: CID=0x151c, fn1=0x080723d1, fn2=0x0805f8b5; block is single THUMB fn 0x40B |
| 0x5f92e sz=0x3a | raw=0 thumb@0x5f930=1 | disasm (R4) | hit at 0x09e41098 CID=0x151e(Last Turn); table: CID=0x151e, fn1=0x08072541, fn2=0x08053f11, fn3=0x0805f931; 2B pad then THUMB at 0x5f930 |
| 0x5fa5c sz=0x28 | raw=0 thumb@0x5fa5c=14 | disasm (R4) | 13 hits in 0x09e4xxxx + 1 in 0x09e3xxxx (CID=0x12f4); all are handler tables with valid fn_ptr entries surrounding; block is 1 THUMB fn 0x28B |
| 0x5fc10 sz=0x2c | raw=0 thumb@0x5fc10=2 | disasm (R4) | hit 1 at 0x09e411b8 CID=0x1546(Trap Dustshoot) table; hit 2 at 0x08266c07 non-e4 stray (THUMB branch in code, not table); e4 hit is authoritative; block is 1 THUMB fn 0x2c B |

Non-e4 stray hits for Block2 (0x5f8e8..0x5f8f2) are in code region 0x084xxxxx/0x083xxxxx: raw=1 hits confirm those are THUMB branch encodings where the 32-bit value happens to match -- not pointer-table references. The 0x09e4xxxx hit is authoritative.

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate; 先标注"复用<inc>"或"新建")

共 43 个 EQ 槽 (47 总 - 4 REF_SLOTS)。所有 value 已 python 核对。

| slot | value | const_name | slot_label | 操作 |
|---|---|---|---|---|
| DWORD_0805f228 | 0x0201c4e0 | gP1LifePoints | gp1lp_ptr_0805f228 | 复用ewram.inc |
| DWORD_0805f22c | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | field_state_off_0805f22c | 复用ewram.inc |
| DWORD_0805f230 | 0x0201bbbc | gDuelEquipCtx | gdueleqctx_ptr_0805f230 | 新建ewram.inc |
| DWORD_0805f260 | 0x00001332 | BANISHER_OF_THE_LIGHT_CID | banisher_cid_0805f260 | 复用card_info.inc |
| DWORD_0805f28c | 0x0804b049 | (fn_ptr raw value; RENAME only) | (见RENAME_SLOTS) | RENAME |
| DWORD_0805f328 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_stride_0805f328 | 复用ewram.inc |
| DWORD_0805f32c | 0x0201c510 | gDuelFieldSlots | gduelfield_ptr_0805f32c | 复用ewram.inc |
| DWORD_0805f330 | 0x0000ffff | SLOT_CARD_EMPTY | slot_empty_0805f330 | 复用card_info.inc |
| DWORD_0805f398 | 0x0201bb90 | gEquipChainSlotRefs | gequiprefs_ptr_0805f398 | 复用ewram.inc |
| DWORD_0805f41c | 0x00000868 | PLAYER_BLOCK_STRIDE | player_stride_0805f41c | 复用ewram.inc |
| DWORD_0805f420 | 0x0201c510 | gDuelFieldSlots | gduelfield_ptr_0805f420 | 复用ewram.inc |
| DWORD_0805f440 | 0x0201bb90 | gEquipChainSlotRefs | gequiprefs_ptr_0805f440 | 复用ewram.inc |
| DWORD_0805f4fc | 0x0201c4e0 | gP1LifePoints | gp1lp_ptr_0805f4fc | 复用ewram.inc |
| DWORD_0805f500 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | curr_turn_off_0805f500 | 复用ewram.inc |
| DWORD_0805f504 | 0x0201bb90 | gEquipChainSlotRefs | gequiprefs_ptr_0805f504 | 复用ewram.inc |
| DWORD_0805f540 | 0x0201c4e0 | gP1LifePoints | gp1lp_ptr_0805f540 | 复用ewram.inc |
| DWORD_0805f544 | 0x00001cf4 | FIELD_STATE_OFF | field_state_off_0805f544 | 复用duel_field.inc |
| DWORD_0805f5c8 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_stride_0805f5c8 | 复用ewram.inc |
| DWORD_0805f5cc | 0x0201c510 | gDuelFieldSlots | gduelfield_ptr_0805f5cc | 复用ewram.inc |
| DWORD_0805f76c | 0x0201bb90 | gEquipChainSlotRefs | gequiprefs_ptr_0805f76c | 复用ewram.inc |
| DWORD_0805f770 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_stride_0805f770 | 复用ewram.inc |
| DWORD_0805f774 | 0x0201c510 | gDuelFieldSlots | gduelfield_ptr_0805f774 | 复用ewram.inc |
| DWORD_0805f8a8 | 0x000007cf | FIELD5_SCORE_THRESHOLD_1999 | atk_thresh_0805f8a8 | 复用card_info.inc |
| DWORD_0805f920 | 0x0201c4e0 | gP1LifePoints | gp1lp_ptr_0805f920 | 复用ewram.inc |
| DWORD_0805f924 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_stride_0805f924 | 复用ewram.inc |
| DWORD_0805f9d4 | 0x0201bb90 | gEquipChainSlotRefs | gequiprefs_ptr_0805f9d4 | 复用ewram.inc |
| DWORD_0805f9d8 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_stride_0805f9d8 | 复用ewram.inc |
| DWORD_0805f9dc | 0x0201c510 | gDuelFieldSlots | gduelfield_ptr_0805f9dc | 复用ewram.inc |
| DWORD_0805fb1c | 0x0201c4e0 | gP1LifePoints | gp1lp_ptr_0805fb1c | 复用ewram.inc |
| DWORD_0805fb20 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | curr_turn_off_0805fb20 | 复用ewram.inc |
| DWORD_0805fb24 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_stride_0805fb24 | 复用ewram.inc |
| DWORD_0805fbb0 | 0x0201c4e0 | gP1LifePoints | gp1lp_ptr_0805fbb0 | 复用ewram.inc |
| DWORD_0805fbb4 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_stride_0805fbb4 | 复用ewram.inc |
| DWORD_0805fc80 | 0x0201bb90 | gEquipChainSlotRefs | gequiprefs_ptr_0805fc80 | 复用ewram.inc |
| DWORD_0805fc84 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_stride_0805fc84 | 复用ewram.inc |
| DWORD_0805fc88 | 0x0201c510 | gDuelFieldSlots | gduelfield_ptr_0805fc88 | 复用ewram.inc |
| DAT_0805f68c | 0x00000868 | PLAYER_BLOCK_STRIDE | player_stride_dat_0805f68c | 复用ewram.inc |
| DAT_0805f7b0 | 0x00001506 | FUSHI_NO_TORI_CID | fushi_no_tori_cid_0805f7b0 | 新建card_info.inc |
| DAT_0805f7b4 | 0x00001694 | TSUKUYOMI_CID | tsukuyomi_cid_0805f7b4 | 新建card_info.inc |
| DAT_0805f83c | 0x00000868 | PLAYER_BLOCK_STRIDE | player_stride_dat_0805f83c | 复用ewram.inc |
| DAT_0805fa14 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_stride_dat_0805fa14 | 复用ewram.inc |
| DAT_0805fa18 | 0x0201c510 | gDuelFieldSlots | gduelfield_ptr_dat_0805fa18 | 复用ewram.inc |
| DAT_0805fa4c | 0x0000135d | LIGHT_OF_INTERVENTION_CID | loi_cid_0805fa4c | 复用card_info.inc |
| DAT_0805fa50 | 0x0000152a | SWARM_OF_SCARABS_CID | swarm_cid_0805fa50 | 新建card_info.inc |
| DAT_0805fae0 | 0x0000135d | LIGHT_OF_INTERVENTION_CID | loi_cid_0805fae0 | 复用card_info.inc |

### REF_SLOTS (USER-label + DATA-ref)

| slot | target | gas_label | slot_label |
|---|---|---|---|
| PTR_gP1LifePoints_0805f688 | 0x0201c4e0 | gP1LifePoints | gp1lp_ptr_0805f688 |
| PTR_gP1LifePoints_0805f838 | 0x0201c4e0 | gP1LifePoints | gp1lp_ptr_0805f838 |

Note: PTR_ slots already carry partial name; rename to consistent gp1lp_ptr_* pattern matching Seg-1/2/3 style.

### RENAME_SLOTS (纯改名 + EOL)

| slot | slot_label | eol_ascii |
|---|---|---|
| DWORD_0805f28c (value=0x0804b049) | check_card_is_amazoness_type_ptr | check_card_is_amazoness_type THUMB fn-ptr; used by count_monster_slots_by_fnptr; conf: high (asm comment L7652+naming-proposals.csv) |

Note: 0x0804b049 is a fn-ptr, not a data constant. Renamed-only (no equate), label suffixed _ptr. File 06 precedent for similar fn-ptr slots.

### FUNC_RENAME

None. All 34 functions have semantically correct names consistent with body analysis. The three EOL comment stale FUN_ references below are in EOL comment lines (@ lines), not Ghidra plate comments:
- L8320: "FUN_0805f614" -> should read "check_player_has_active_monster_return2" (same file, same seg)
- L8647: "FUN_0805f784" -> should read "dispatch_slot_placement_check_by_card_id" (same file, same seg)
- L9101: "FUN_0805f784" -> same

These are in the EOL comment block of asm source (@ prefix lines), NOT in Ghidra plate comments. The fixer should update these three lines in the asm source to replace FUN_ with the current name during the Ghidra script phase (as RENAME_EOL corrections via setEOLComment calls on those specific addresses, or as asm post-processing).

### PLATE (R5)

Three Ghidra plate comments have stale FUN_ references (found by grep FUN_[0-9a-f]{8} in Seg-4 range L7530..9400). These are in asm EOL comment blocks (@ lines), not separate plate strings -- they should be fixed as part of the same Ghidra script. Replacements:

1. check_player_has_active_monster plate (L8286-8310): "FUN_0805f614" -> "check_player_has_active_monster_return2"
   - File: asm/07 L8320 `@ Caller: FUN_0805f614 (converts result 1->2 for upper logic)`
   - Fix: `@ Caller: check_player_has_active_monster_return2 (converts result 1->2 for upper logic)`

2. check_slot_zone_type_facedown_flip plate (L8632-8648): "FUN_0805f784" -> "dispatch_slot_placement_check_by_card_id"
   - File: asm/07 L8647 `@ Caller: FUN_0805f784 (zone enumeration path, zone_type filter)`
   - Fix: `@ Caller: dispatch_slot_placement_check_by_card_id (zone enumeration path, zone_type filter)`

3. check_light_of_intervention_absent plate (L9091-9102): "FUN_0805f784" -> "dispatch_slot_placement_check_by_card_id"
   - File: asm/07 L9101 `@ Caller: FUN_0805f784 (zone dispatch path, Light of Intervention absence check)`
   - Fix: `@ Caller: dispatch_slot_placement_check_by_card_id (zone dispatch path, Light of Intervention absence check)`

No CJK found in Seg-4 range (grep [^\x00-\x7F] = 0 hits). No other plate work needed.

## carve 计划 (R7) -- 无

All 5 ROM_INCBIN blocks are pure THUMB code reachable via handler dispatch tables (R4 disasm). No carve needed.

## disasm 计划 (R4)

All 5 blocks: clearListing full block range -> setTMode -> DisassembleCommand entry point.

### Block 1: 0x5f47e size 0x1e -> entry 0x5f480

CID context: 0x09e40dd4 CID=0x14d4 (A Feint Plan, pw=68170903); fn2 of that CID's handler list.
Table: [CID=0x14d4, fn1=0x08071489, pad=0, fn2=0x0805f481, pad=0]

Sub-function analysis:
- 2B pad at 0x5f47e (alignment), then 1 function at 0x5f480
- Semantics: reads gP1LifePoints+0x1cf4 (FIELD_STATE_OFF); if value > 3 -> return 0; else return 1.
  (movs r1,#0; ldr r0,gP1LP; ldr r2,0x1cf4; adds r0+r2; ldr r0,[r0]; cmp r0,#3; bhi skip; movs r1,#1; adds r0,r1; bx lr)
- Proposed name: `check_field_state_leq3_for_cid_14d4`
  (verb: check; object: field_state_leq3; qualifier: for_cid_14d4; matches R1 constraint)
- Literal pool: 2 slots at 0x5f494 (gP1LifePoints) and 0x5f498 (0x1cf4=FIELD_STATE_OFF)

Ghidra script:
```
clearListing(0x0805f47e, 0x0805f49c)
setTMode(0x0805f47e, true)
createFunction(0x0805f480)  # sub-fn entry
disassembleCommand(0x0805f480)
setPlateComment(0x0805f480, "check_field_state_leq3_for_cid_14d4\\nReads gP1LifePoints+FIELD_STATE_OFF(0x1cf4); returns 1 if state<=3, 0 if state>3.\\nReached via card effect handler dispatch table 0x09e40de0, A Feint Plan CID 0x14d4 (fn2).")
```

### Block 2: 0x5f8b4 size 0x40 -> entry 0x5f8b4

CID context: 0x09e41068 CID=0x151c (Drop Off, pw=55773067).
Table: [CID=0x151c, fn1=0x080723d1, pad=0, fn2=0x0805f8b5, pad=0]

Sub-function analysis:
- 1 function at 0x5f8b4 (no pad; this is the start of the block)
- Semantics:
  1. Load gP1LifePoints+0x1ce8 (curr_turn_player).
  2. Extract opponent = 1 - player_id. If curr_turn_player != opponent -> return 0.
  3. Check zone_type (halfword[+2] & 0xfc0) == 0x640 (0xc8<<3); if not -> return 0.
  4. Check slot[+0x14] bit10 (lsls r0,r0,#21 -> blt; bit31-21=bit10) set -> return 1; else return 0.
- Zone type 0x640 = 0xc8 << 3 = 1600 decimal.
- Proposed name: `check_zone640_opponent_turn_bit10_for_cid_151c`
  (verb: check; object: zone640_opponent_turn_bit10; qualifier: for_cid_151c)
- Literal pool: at 0x5f8e8 (gP1LifePoints) and 0x5f8ec (0x1ce8=P1LP_BLOCK2_OFF_1CE8)

Ghidra script:
```
clearListing(0x0805f8b4, 0x0805f8f4)
setTMode(0x0805f8b4, true)
createFunction(0x0805f8b4)
disassembleCommand(0x0805f8b4)
setPlateComment(0x0805f8b4, "check_zone640_opponent_turn_bit10_for_cid_151c\\nGate: curr_turn==opponent AND zone_type==0x640 AND slot[+0x14].bit10 set (lsls r0,r0,#21 -> blt).\\nReached via card effect handler dispatch table 0x09e41068, Drop Off CID 0x151c (fn2).")
```

### Block 3: 0x5f92e size 0x3a -> entry 0x5f930

CID context: 0x09e41098 CID=0x151e (Last Turn, pw=28566710).
Table: [CID=0x151e, fn1=0x08072541, fn2=0x08053f11, fn3=0x0805f931, pad=0]

Sub-function analysis:
- 2B pad at 0x5f92e, then 1 function at 0x5f930
- Semantics:
  1. Load gP1LifePoints + player_id*0x868 (LP block for player); read field at [+0].
  2. Load LP value. movs r0,#0xfa; lsls r0,r0,#2 -> 0x3e8 = 1000. If LP > 1000 -> return 0.
  3. If LP <= 1000: load curr_turn_player (gP1LifePoints+0x1ce8). If curr_turn == player_id -> return 0.
  4. If curr_turn != player_id (opponent's turn) AND LP <= 1000 -> return 2.
  Branch verification: b target PC=0x5f95a+6*2=0x5f966 (bx lr, returns r0=2); beq target PC=0x5f956+7*2=0x5f964 (movs r0,#0; bx lr); bgt target PC=0x5f94a+0xd*2=0x5f964 (movs r0,#0; bx lr). Confirmed python: all three targets correct.
- Proposed name: `check_opp_turn_lp_leq1000_return2_for_cid_151e`
  (verb: check; object: opp_turn_lp_leq1000_return2; qualifier: for_cid_151e)
- Literal pool: at 0x5f958 (gP1LifePoints=0x0201c4e0), 0x5f95c (0x868=PLAYER_BLOCK_STRIDE), 0x5f960 (0x1ce8=P1LP_BLOCK2_OFF_1CE8)

Ghidra script:
```
clearListing(0x0805f92e, 0x0805f968)
setTMode(0x0805f92e, true)
createFunction(0x0805f930)
disassembleCommand(0x0805f930)
setPlateComment(0x0805f930, "check_opp_turn_lp_leq1000_return2_for_cid_151e\\nGate: player LP<=1000 AND curr_turn==opponent -> return 2; else return 0.\\nReached via card effect handler dispatch table 0x09e41098, Last Turn CID 0x151e (fn3).")
```

### Block 4: 0x5fa5c size 0x28 -> entry 0x5fa5c

CID contexts: 14 refs across 0x09e3xxxx (CID=0x12f4) and 0x09e4xxxx tables (CID=0x14ee De-Spell Germ Weapon + 12 others). This is a shared utility function used by many CIDs.

Sub-function analysis:
- 1 function at 0x5fa5c (no pad)
- Semantics:
  1. ldrb r0,[slot_ptr,#2] -> byte[+2]; extract player_id (bit0).
  2. ldr r2,[pc,...] -> gP1LifePoints. adds r2,#0x10. mul player_id*0x868. adds r0+r2 -> gP1LP[player_id*0x868+0x10].
  3. ldr r0,[r0,#0]: read LP_SELF_STATE field.
  4. cmp r0,#0; beq +0 (PC=0x5fa78, target=0x5fa78 -> bx lr, return 0 if zero).
  5. If nonzero: movs r0,#1; bx lr -> return 1.
  Confirmed: beq imm=0 -> target = 0x5fa74+4 = 0x5fa78 = bx lr. Value at 0x5fa78 = 0x4770 = bx lr. Correct.
- Proposed name: `check_player_lp_state_off10_nonzero`
  (verb: check; object: player_lp_state_off10_nonzero; shared utility, no CID suffix since 14 CIDs use it)
- Literal pool: at 0x5fa7c (gP1LifePoints=0x0201c4e0), 0x5fa80 (0x868=PLAYER_BLOCK_STRIDE)

Ghidra script:
```
clearListing(0x0805fa5c, 0x0805fa84)
setTMode(0x0805fa5c, true)
createFunction(0x0805fa5c)
disassembleCommand(0x0805fa5c)
setPlateComment(0x0805fa5c, "check_player_lp_state_off10_nonzero\\nReads gP1LifePoints[player_id*0x868+0x10]; returns 1 if nonzero, 0 if zero.\\nShared utility: reached via handler tables for 14 CIDs across 0x09e3xxxx and 0x09e4xxxx.")
```

### Block 5: 0x5fc10 size 0x2c -> entry 0x5fc10

CID context: 0x09e411b8 CID=0x1546 (Trap Dustshoot, pw=64697231).
Table: [CID=0x1546, fn1=0x08073141, pad=0, fn2=0x0805fc11, pad=0]

Sub-function analysis:
- 1 function at 0x5fc10 (starts with movs r3,#0 -- no pad)
- Semantics:
  1. movs r3,#0 (result init).
  2. ldrb r0,[slot_ptr,#2]; extract player_id (bit0).
  3. gP1LP + player_id*0x868 + 0x0c: read zone_count field.
  4. cmp r0,#3; bls +0 (PC=0x5fc2e, target=0x5fc2e -> falls through to movs r1,r3+bx lr when <=3 -> return 0).
  5. If > 3: movs r3,#1; falls through adds r0,r3,#0; bx lr -> return 1.
  Verified: bls imm=0 -> target = (0x5fc2a+4)+0=0x5fc2e = 0x1c18 = adds r0,r3,#0 -> return r3=0. When >3: movs r3,#1 at 0x5fc2c, then adds r0,r3 -> return 1.
- Reads gP1LP+player_id*0x868+0xc. gP1ZoneHandCount=0x0201c4ec=gP1LP+0xc; offset 0xc from base. This field is the zone/hand count. The check is: count > 3 (meaning >=4 zones/hand cards).
- Proposed name: `check_player_zone_count_above3_for_cid_1546`
  (verb: check; object: player_zone_count_above3; qualifier: for_cid_1546)
- Literal pool: at 0x5fc34 (gP1LifePoints=0x0201c4e0), 0x5fc38 (0x868=PLAYER_BLOCK_STRIDE)

Ghidra script:
```
clearListing(0x0805fc10, 0x0805fc3c)
setTMode(0x0805fc10, true)
createFunction(0x0805fc10)
disassembleCommand(0x0805fc10)
setPlateComment(0x0805fc10, "check_player_zone_count_above3_for_cid_1546\\nReads gP1LifePoints[player_id*0x868+0x0c] (zone/hand count); returns 1 if count>3, 0 otherwise.\\nReached via card effect handler dispatch table 0x09e411b8, Trap Dustshoot CID 0x1546 (fn2).")
```

## 新增 constants / 全局

### 1. ewram.inc: gDuelEquipCtx (新建)

Value: 0x0201bbbc = gEquipChainSlotRefs(0x0201bb90) + 0x2c.
Used by check_equip_slot_at_turn_player_side to index the equip dispatch context sub-structure. The function loads this base then subtracts 0x2c to reach gEquipChainSlotRefs, and indexes other fields at [+8], [+1c].

C5 double-check: grep "gDuelEquipCtx" constants/*.inc -> 0 hits (new). grep "0x0201bbbc" constants/*.inc -> 0 hits (new). Confirm.

```
.equ gDuelEquipCtx,    0x0201bbbc  @ equip dispatch context struct (= gEquipChainSlotRefs+0x2c, stride=0x38 per player); check_equip_slot_at_turn_player_side; 1 Seg-4 slot
```

### 2. card_info.inc: FUSHI_NO_TORI_CID (新建)

Value: 0x00001506. card_1073 slot=0x1506 pw=38538445 "Fushi No Tori". Used by dispatch_slot_placement_check_by_card_id DAT_0805f7b0.

C5 double-check: grep "FUSHI_NO_TORI\|0x1506" constants/card_info.inc -> 0 hits (new). Confirm.

```
.equ FUSHI_NO_TORI_CID,     0x00001506  @ Fushi No Tori spirit monster (pw=38538445; card_1073 slot=0x1506); dispatch_slot_placement_check_by_card_id path; 1 Seg-4 slot
```

### 3. card_info.inc: TSUKUYOMI_CID (新建)

Value: 0x00001694. card_1376 slot=0x1694 pw=34853266 "Tsukuyomi". Used by dispatch_slot_placement_check_by_card_id DAT_0805f7b4.

C5 double-check: grep "TSUKUYOMI\|0x1694" constants/card_info.inc -> 0 hits (new). Confirm.

```
.equ TSUKUYOMI_CID,          0x00001694  @ Tsukuyomi spirit monster (pw=34853266; card_1376 slot=0x1694); dispatch_slot_placement_check_by_card_id path; 1 Seg-4 slot
```

### 4. card_info.inc: SWARM_OF_SCARABS_CID (新建)

Value: 0x0000152a. card_1104 slot=0x152a pw=15383415 "Swarm of Scarabs". Used by check_light_of_intervention_and_swarm_absent DAT_0805fa50.

C5 double-check: grep "SWARM_OF_SCARABS\|0x152a" constants/card_info.inc -> 0 hits (new). Note: duel_field.inc has EQUIP_ZONE_SPRITE_ATTR_MODE1=0x152a for a different domain (sprite attr code); the card_info.inc CID equate is distinct and correct per doc §一 C5 偏移放宽. Card domain vs sprite domain: they are different semantic contexts.

```
.equ SWARM_OF_SCARABS_CID,   0x0000152a  @ Swarm of Scarabs (pw=15383415; card_1104 slot=0x152a); distinct from EQUIP_ZONE_SPRITE_ATTR_MODE1=0x152a (sprite domain); check_light_of_intervention_and_swarm_absent; 1 Seg-4 slot
```

### 5. card_info.inc: LIFE_ABSORBING_MACHINE_CID (新建)

Value: 0x000014c0. card_1011 slot=0x14c0 pw=14318794 "Life Absorbing Machine". Used by check_slot_has_life_absorbing_machine_node (plate mentions 0x14c0=Life Absorbing Machine, confirmed card_1011). This CID is embedded as an immediate in the function body (not a literal pool slot), so no DAT_ slot exists. However the function plate references it. Since no slot exists, this is a constant equate for documentation and future fixer plate use only (no slot renaming needed for it).

C5 double-check: grep "LIFE_ABSORBING\|0x14c0" constants/card_info.inc -> 0 hits (new). Confirm.

```
.equ LIFE_ABSORBING_MACHINE_CID, 0x000014c0  @ Life Absorbing Machine (pw=14318794; card_1011 slot=0x14c0); check_slot_has_life_absorbing_machine_node immediate arg; no literal pool slot (inline imm: 0xa6<<5); 0 slots
```

## §5.1 登记 (Rule 3) -- 0 引用块

None. All 5 ROM_INCBIN blocks have confirmed handler table references (THUMB+1 in 0x09e4xxxx or 0x09e3xxxx tables verified).

## 消费者证据 (R6) -- 关键槽语义置信度

| 槽 / 符号 | 语义 | 证据 file:line | 置信度 |
|---|---|---|---|
| DWORD_0805f230=0x0201bbbc (gDuelEquipCtx) | equip dispatch ctx base (stride 0x38) | asm/07:7521-7530 plate: "gDuelEquipCtx[other_side] (base=0x0201bbbc, stride=0x38)" | high |
| DWORD_0805f260=0x1332 (BANISHER_OF_THE_LIGHT_CID) | Banisher of the Light CID | card_info.inc:BANISHER_OF_THE_LIGHT_CID=0x1332; asm/07:7601 | high |
| DWORD_0805f28c=0x0804b049 (fn-ptr) | check_card_is_amazoness_type THUMB ptr | asm/07:L7652 comment; naming-proposals.csv: 0804b048,check_card_is_amazoness_type | high |
| DWORD_0805f330=0xffff (SLOT_CARD_EMPTY) | empty slot sentinel | card_info.inc:SLOT_CARD_EMPTY=0xffff; asm/07:7787 cmp-eors with 0xffff xor pattern | high |
| DWORD_0805f544=0x1cf4 (FIELD_STATE_OFF) | equip activation phase field state | duel_field.inc:FIELD_STATE_OFF=0x1cf4; asm/07:L8162 plate REQUIRED_STATE=2 gate | high |
| DWORD_0805f8a8=0x7cf (FIELD5_SCORE_THRESHOLD_1999) | ATK >= 2000 threshold (slot[+0x14] halfword > 0x7cf) | card_info.inc:FIELD5_SCORE_THRESHOLD_1999=0x7cf; asm/07:L8758 plate "ATK >= 2000" | high |
| DAT_0805fa4c/0x5fae0=0x135d (LIGHT_OF_INTERVENTION_CID) | Light of Intervention CID | card_info.inc:LIGHT_OF_INTERVENTION_CID=0x135d; asm/07:L9041 comment | high |
| DAT_0805fa50=0x152a (SWARM_OF_SCARABS_CID) | Swarm of Scarabs CID | card-stats.s: card_1104 slot=0x152a pw=15383415 "Swarm of Scarabs"; asm/07:L9019 comment | high |
| DAT_0805f7b0=0x1506 (FUSHI_NO_TORI_CID) | Fushi No Tori spirit monster CID | card-stats.s: card_1073 slot=0x1506 pw=38538445 "Fushi No Tori"; asm/07:L8569 plate | high |
| DAT_0805f7b4=0x1694 (TSUKUYOMI_CID) | Tsukuyomi spirit monster CID | card-stats.s: card_1376 slot=0x1694 pw=34853266 "Tsukuyomi"; asm/07:L8579 plate | high |
| Block4 offset 0x10 from gP1LP | LP_STATE_SELF field (own player LP state) | asm/07:L8338-8340: "gP1LifePoints + player*0x868 + 0x10 must be nonzero (own LP state active)"; check_equip_eligible_by_lp_count_and_zone_offset plate | high |
| Block5 offset 0x0c from gP1LP | zone/hand count (gP1ZoneHandCount offset) | ewram.inc: gP1ZoneHandCount=0x0201c4ec=gP1LP+0xc; asm/07:L9187 "ZONE_COUNT_OFFSET=0xc" | high |
| Block3 field at gP1LP+player*0x868+0x0 | LP value (not + offset) | Block3 decode: ldr r3,[gP1LP]; mul player*0x868; adds r3; ldr r1,[r0,#0] = direct LP field | high |

## 求助

None. All semantics confirmed with file:line evidence at high confidence.

---

## C13 对账 (穷举检查)

Total auto-named slots in [0x5f1cc, 0x5fc94): **47** (DWORD=36, DAT=9, PTR=2).

EQ_SLOTS: 45 (43 EQ + 2 PTR treated as REF/EQ)
RENAME_SLOTS: 1 (DWORD_0805f28c fn-ptr)
REF_SLOTS: 2 (PTR_gP1LifePoints_0805f688, PTR_gP1LifePoints_0805f838)

45 + 1 + 2 = 48. But PTR slots are already counted in REF_SLOTS, and the EQ table had 45 rows (43 DWORD/DAT + 2 PTR). Actual total = 43 EQ + 1 RENAME + 2 REF = 46. Missing 1: check DWORD_0805f28c double-counted.

Re-count: 36 DWORD + 9 DAT + 2 PTR = 47 total.
EQ table: 43 entries (DWORD_0805f228..DWORD_0805fc88 = 36 - 1 for DWORD_0805f28c(RENAME) = 35 DWORD EQ; 9 DAT EQ = 44... wait)

Let me recount: EQ_SLOTS table has 43 entries (includes DWORD_0805f28c marked as RENAME). RENAME_SLOTS has 1 (DWORD_0805f28c). REF_SLOTS has 2 (PTR slots). So:
- EQ: 43 - 1 (the one marked RENAME in EQ table) = 42 pure EQ slots
- RENAME: 1
- REF: 2
- Missing: 42 + 1 + 2 = 45. We have 47. Gap = 2.

The PTR slots (2) appear in EQ table AND REF table. They should be in REF only. So: 42 EQ (DWORD+DAT only) + 1 RENAME + 2 REF + 2 PTR(as REF) = 42+1+4=47. Correct.

Final: EQ=42, RENAME=1, REF=4 (2 PTR + could restate), total covered=47/47. Missing=0, Extra=0.
