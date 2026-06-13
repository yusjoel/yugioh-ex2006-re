# Refine Proposal: F06-Seg-2  [0x080541cc..0x08054ba0)

## 段测绘

- 函数入口: x23 (所有已命名)
  - 0x080541cc check_equip_slot_eligible_by_side_setcode_prereqs_and_type
  - 0x08054234 check_equip_slot_eligible_by_field8_9_and_type
  - 0x08054284 check_equip_slot_eligible_by_opposite_side_and_field6
  - 0x080542f0 check_equip_slot_eligible_by_field8_9_prereqs_and_type
  - 0x08054364 check_equip_slot_eligible_by_opposite_side_whitelist
  - 0x080543b4 check_equip_slot_eligible_by_field6_zero_and_type
  - 0x0805440c check_equip_slot_eligible_by_icid_mismatch_and_prereqs
  - 0x08054468 check_equip_slot_eligible_by_no_field8_9_and_monster
  - 0x080544d4 check_equip_slot_eligible_by_icid_match
  - 0x08054518 check_equip_slot_eligible_by_monster_and_chain_score
  - 0x08054570 check_equip_slot_eligible_by_pair_count_triple
  - 0x08054614 check_equip_slot_eligible_by_side_and_zone_for_desert_sunlight
  - 0x0805465c check_equip_slot_type_and_score_match
  - 0x080546bc check_equip_slot_eligible_with_prereqs_and_score_guard
  - 0x080546e0 check_equip_slot_eligible_with_score_guard
  - 0x0805474c check_equip_slot_score_and_field6_flags
  - 0x080547b4 check_equip_slot_eligible_by_evolution_target_and_space
  - 0x08054834 check_equip_slot_eligible_by_same_side_prereqs_and_type
  - 0x08054898 check_equip_slot_eligible_by_same_side_and_prereqs
  - 0x080548ec check_equip_slot_eligible_by_card_specific_activation
  - 0x08054acc check_equip_slot_eligible_by_union_type_and_occupied
  - 0x08054b18 check_equip_slot_eligible_with_whitelist_prereqs_and_type
  - 0x08054b80 invoke_serial_spell_effect_node_handler
- 残留自动名槽: 52 total
  - DAT_ prefix x48: literal pool entries (STRIDE/gDuelFieldSlots/CIDs/masks) including 2 new from 0x08054614 block
  - DWORD_ prefix x4: 0x08054b08, 0x08054b0c, 0x08054b70, 0x08054b74 (all STRIDE/gDuelFieldSlots)
- ROM_INCBIN / .byte 块: 1 (now disasm -> 0 残留)
  - 0x08054614 size 0x48 (72 bytes) -> disasm, see disasm 计划 (R4)

## 数据块分类 (Rule 2/3) -- ref-scan 证据

| 块 | ref-scan (raw / THUMB+1) | 判定 | 理由 |
|---|---|---|---|
| 0x08054614 sz=0x48 | raw=0 (2 asset-region false hits outside code area) thumb+1=1 (at 0x09e421d4 confirmed) | disasm | THUMB+1 hit at 0x09e421d4 verified by python: ROM[0x09e421d4]=0x08054615; surrounding context: CID 0x000017b4 (Desert Sunlight) at 0x09e421cc, fn-ptr1 0x08079595 at 0x09e421d0, fn-ptr2 0x08054615 at 0x09e421d4 -- card effect handler dispatch table entry (same format as all other Seg-2 fn-ptrs). Valid THUMB predicate function: same-side + zone[0..4] + occupied + slot[+8]/[+6] checks, literal pool PLAYER_BLOCK_STRIDE(0x868)/gDuelFieldSlots(0x0201c510) at 0x08054650/0x08054654, bx lr at 0x0805465a. Rule 2: referenced fn-ptr -> must disasm, not S5.1. |

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS  (47 reuse + 5 new = 52 total)

All slots verified via python struct.unpack_from('<I', rom, addr-0x08000000).

#### REUSE PLAYER_BLOCK_STRIDE = 0x00000868 (ewram.inc, 21 slots)

| slot | value | const_name | slot_label |
|---|---|---|---|
| 0x08054224 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_side_setcode_prereqs_and_type_stride |
| 0x08054274 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_field8_9_and_type_stride |
| 0x080542c0 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_opposite_side_and_field6_stride |
| 0x08054354 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_field8_9_prereqs_and_type_stride |
| 0x080543a4 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_opposite_side_whitelist_stride |
| 0x080543fc | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_field6_zero_and_type_stride |
| 0x08054458 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_icid_mismatch_and_prereqs_stride |
| 0x080544c4 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_no_field8_9_and_monster_stride |
| 0x080544f8 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_icid_match_stride |
| 0x08054560 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_monster_and_chain_score_stride |
| 0x080545cc | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_pair_count_triple_stride |
| 0x08054650 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_side_and_zone_for_desert_sunlight_stride |
| 0x080546ac | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_type_and_score_match_stride |
| 0x0805473c | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_with_score_guard_stride |
| 0x08054784 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_score_and_field6_flags_stride |
| 0x08054824 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_evolution_target_and_space_stride |
| 0x08054888 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_same_side_prereqs_and_type_stride |
| 0x080548dc | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_same_side_and_prereqs_stride |
| 0x08054940 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_card_specific_activation_stride |
| 0x08054b08 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_union_type_and_occupied_stride |
| 0x08054b70 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_with_whitelist_prereqs_and_type_stride |

#### REUSE gDuelFieldSlots = 0x0201c510 (ewram.inc, 22 slots)

| slot | value | const_name | slot_label |
|---|---|---|---|
| 0x08054228 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_side_setcode_prereqs_and_type_slots |
| 0x08054278 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_field8_9_and_type_slots |
| 0x080542c4 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_opposite_side_and_field6_slots |
| 0x08054358 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_field8_9_prereqs_and_type_slots |
| 0x080543a8 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_opposite_side_whitelist_slots |
| 0x08054400 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_field6_zero_and_type_slots |
| 0x0805445c | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_icid_mismatch_and_prereqs_slots |
| 0x080544c8 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_no_field8_9_and_monster_slots |
| 0x080544fc | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_icid_match_slots |
| 0x08054564 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_monster_and_chain_score_slots |
| 0x080545d0 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_pair_count_triple_slots_a |
| 0x08054610 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_pair_count_triple_slots_b |
| 0x08054654 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_side_and_zone_for_desert_sunlight_slots |
| 0x080546b0 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_type_and_score_match_slots |
| 0x08054740 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_with_score_guard_slots |
| 0x08054788 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_score_and_field6_flags_slots |
| 0x08054828 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_evolution_target_and_space_slots |
| 0x0805488c | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_same_side_prereqs_and_type_slots |
| 0x080548e0 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_same_side_and_prereqs_slots |
| 0x08054944 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_card_specific_activation_slots |
| 0x08054b0c | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_union_type_and_occupied_slots |
| 0x08054b74 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_with_whitelist_prereqs_and_type_slots |

#### REUSE SCROLLBAR_KEEP_BITS_8_0 = 0x000001ff (gl_scrollbar.inc, 2 slots)

| slot | value | const_name | slot_label |
|---|---|---|---|
| 0x08054a2c | 0x000001ff | SCROLLBAR_KEEP_BITS_8_0 | check_equip_slot_eligible_by_card_specific_activation_field_mask_a |
| 0x08054ab4 | 0x000001ff | SCROLLBAR_KEEP_BITS_8_0 | check_equip_slot_eligible_by_card_specific_activation_field_mask_a_b |

Note: 0x000001ff used to mask equip_slot[+0xa] bits[8:0] before shifting to bits[14:6] of target slot[+4]. Same bit-field mask as scrollbar range_param field. C5 reuse (value match, not semantic match required).

#### REUSE SCROLLBAR_CLEAR_BITS_14_6 = 0xffff803f (gl_scrollbar.inc, 2 slots)

| slot | value | const_name | slot_label |
|---|---|---|---|
| 0x08054a30 | 0xffff803f | SCROLLBAR_CLEAR_BITS_14_6 | check_equip_slot_eligible_by_card_specific_activation_clear_mask |
| 0x08054ab8 | 0xffff803f | SCROLLBAR_CLEAR_BITS_14_6 | check_equip_slot_eligible_by_card_specific_activation_clear_mask_b |

Note: 0xffff803f clears bits[14:6] of target slot[+4] before inserting equip_flag bits. Same mask as Seg-1 (gl_scrollbar.inc). C5 reuse.

#### NEW constants (5 slots)

| slot | value | const_name | slot_label | file | evidence |
|---|---|---|---|---|---|
| 0x08054948 | 0x0000180e | TRICKYS_MAGIC_4_CID | check_equip_slot_eligible_by_card_specific_activation_icid_trickys | card_info.inc | card-stats.s card_1688: slot=0x180E pw=75622824 "Tricky's Magic 4"; high-conf |
| 0x0805495c | 0x00001938 | GILFORD_THE_LEGEND_CID | check_equip_slot_eligible_by_card_specific_activation_icid_gilford | card_info.inc | card-stats.s card_1937: slot=0x1938 pw=69933858 "Gilford the Legend"; high-conf |
| 0x080549b4 | 0xc0300000 | THE_TRICKY_TARGET_SLOT_PATTERN | check_equip_slot_eligible_by_card_specific_activation_tricky_pattern | card_info.inc | THE_TRICKY_CID (0x1806) << 19 == 0xc0300000 verified by python; checks (slot_word<<19)==pattern i.e. slot_word bits[12:0]==0x1806 (The Tricky); high-conf |
| 0x08054ab0 | 0x000010b0 | EQUIP_FLAG_TARGET_ICID_TABLE_OFF | check_equip_slot_eligible_by_card_specific_activation_table_off | duel_field.inc | Roll Out! branch: ldrh r0,[gDuelFieldSlots+0x10b0+equip_flag*4] -- u16 table indexed by equip_slot[+0xa]; offset 0x10b0 != SLOT_FACE_STATUS_ARRAY_OFF (0x10b1 byte array); != PRINCESS_OF_TSURUGI_CID (card ID); C5 offset relaxation applies; med-conf |
| 0x08054b9c | 0x0000183e | SERIAL_SPELL_CID | invoke_serial_spell_effect_node_handler_icid | card_info.inc | card-stats.s card_1730: slot=0x183E pw=49398568 "Serial Spell"; high-conf |

### REF_SLOTS: none

No fn-ptr data slots in Seg-2.

### RENAME_SLOTS: none

All DWORD_ auto-named slots (0x08054b08, 0x08054b0c, 0x08054b70, 0x08054b74) are covered by the EQ equates above (PLAYER_BLOCK_STRIDE and gDuelFieldSlots). No separate RENAME needed.

### FUNC_RENAME: none

All 23 functions in Seg-2 are correctly named (22 pre-existing + 1 new from disasm: check_equip_slot_eligible_by_side_and_zone_for_desert_sunlight at 0x08054614).

### PLATE (R5)

One stale FUN_ in check_equip_slot_eligible_by_same_side_and_prereqs plate (asm line 2494):

```
old: "called by FUN_0809077c (callback iterator)"
new: "called by invoke_count_zone_pair_hits_full_range (0x0809077c, callback iterator)"
```

Evidence: asm/11_effect_slot_puzzletext.s line 12026: `invoke_count_zone_pair_hits_full_range:` at `0x0809077c`. high-conf.

Replacement: substring `FUN_0809077c` -> `invoke_count_zone_pair_hits_full_range (0x0809077c,`. Full plate substring replace (existing text is ASCII, no CJK mojibake -- verified by python byte scan of Seg-2 lines 1488-2973).

## carve 計画 (R7): none

## disasm 計画 (R4)

### Block 0x08054614..0x0805465b (0x48 = 72 bytes)

- Range: 0x08054614..0x0805465b (inclusive; next function check_equip_slot_type_and_score_match starts at 0x0805465c)
- Procedure: clearListing(0x08054614, 0x48) -> setTMode(THUMB=1) -> DisassembleCommand(0x08054614, 0x48)
- createFunction(0x08054614) -> setName("check_equip_slot_eligible_by_side_and_zone_for_desert_sunlight", USER)
- Plate (ASCII): "Desert Sunlight (CID 0x17B4) equip eligibility predicate #2; reached via card effect handler dispatch table 0x09e421d4 (fn-ptr2=0x08054615); checks same-side + zone[0..4] boundary + slot occupied + slot[+8]/[+6] predicates; no push lr -- leaf function"
- Literal pool: 2 slots covered by EQ above (0x08054650=PLAYER_BLOCK_STRIDE, 0x08054654=gDuelFieldSlots)
- Note: block body 0x08054614..0x08054657 is THUMB code + literal pool; 0x08054658/0x0805465a are movs r0,#1 / bx lr (2 instructions, not pool data); Ghidra DisassembleCommand covers full range cleanly

## 新增 constants / 全局

### card_info.inc (4 new CIDs)

```asm
.equ ULTIMATE_BASEBALL_KID_CID,  0x000017e1  @ Ultimate Baseball Kid (pw=67934141); equip BST dispatch computed: TRICKYS_MAGIC_4_CID-0x2d
.equ TRICKYS_MAGIC_4_CID,        0x0000180e  @ Tricky's Magic 4 (pw=75622824); equip BST dispatch literal pool
.equ GILFORD_THE_LEGEND_CID,     0x00001938  @ Gilford the Legend (pw=69933858); equip BST dispatch literal pool
.equ SERIAL_SPELL_CID,           0x0000183e  @ Serial Spell (pw=49398568); invoke_serial_spell_effect_node_handler
.equ THE_TRICKY_TARGET_SLOT_PATTERN, 0xc0300000  @ THE_TRICKY_CID<<19; Tricky's Magic 4 target check: (slot_word<<19)==pattern iff slot_word bits[12:0]==THE_TRICKY_CID
```

Note: ULTIMATE_BASEBALL_KID_CID (0x17e1) is computed at runtime (0x180e - 0x2d) and has no literal pool slot in Seg-2, but is added to card_info.inc for EOL documentation completeness. ROLL_OUT_CID (0x1979) already exists at card_info.inc line 832 and is similarly computed (0x1938 + 0x41) with no literal pool slot here.

### duel_field.inc (1 new offset)

```asm
.equ EQUIP_FLAG_TARGET_ICID_TABLE_OFF, 0x000010b0  @ gDuelFieldSlots+0x10b0: u16[] indexed by equip_slot[+0xa] (equip_flag); Roll Out! (0x1979) uses to resolve target card ICID; distinct from SLOT_FACE_STATUS_ARRAY_OFF (0x10b1 byte array) by 1 byte; med-conf
```

## S5.1 登记 (Rule 3) -- 0 引用块

(none -- 0x08054614/0x48 改判 disasm, 见 disasm 計画 (R4))

## 消費者証据 (R6) -- 关键槽语义 file:line + 置信度

| 槽 | 語义 | 証据 file:line | 置信度 |
|---|---|---|---|
| 0x08054948 (0x180e) | Tricky's Magic 4 ICID -- equip BST dispatch target | data/card-stats.s:21959 "Tricky's Magic 4 slot=0x180E"; asm/06:2601-2654 BST branch | high |
| 0x0805495c (0x1938) | Gilford the Legend ICID -- equip BST dispatch target | data/card-stats.s:25196 "Gilford the Legend slot=0x1938"; asm/06:2617-2688 BST branch | high |
| 0x080549b4 (0xc0300000) | Tricky's Magic 4 target slot pattern -- (slot_word<<19) check identifies The Tricky (CID 0x1806) in target zone | python: (0x1806<<19)&0xffffffff==0xc0300000 verified; constants/card_info.inc:753 THE_TRICKY_CID=0x1806; asm/06:2663-2672 comparison sequence | high |
| 0x08054ab0 (0x10b0) | gDuelFieldSlots+0x10b0 = equip_flag->ICID table base offset; Roll Out! branch reads target ICID from this u16 table | asm/06:2765-2771 ldrh r0,[gDuelFieldSlots+0x10b0+equip_flag*4]; duel_field.inc SLOT_FACE_STATUS_ARRAY_OFF=0x10b1 (adjacent but distinct) | med |
| 0x08054b9c (0x183e) | Serial Spell ICID -- written to card_entry[+0] after effect node handler | data/card-stats.s:22505 "Serial Spell slot=0x183E"; asm/06:2952-2953 strh to card_entry[+0] | high |
| 0x08054615 (fn-ptr) | check_equip_slot_eligible_by_side_and_zone_for_desert_sunlight -- Desert Sunlight (CID 0x17B4, card_1608) equip predicate #2, fn-ptr2 in card effect handler dispatch table | python: ROM[0x09e421d4]=0x08054615 verified; ROM[0x09e421cc]=0x000017b4 (Desert Sunlight CID); data/card-stats.s:20919 "Desert Sunlight slot=0x17B4 pw=93747864" | high |

## 求助: none

All slots resolved at high or med confidence. 0xc0300000 derivation verified by python computation. 0x10b0 offset is med-conf (structural, not runtime-observable from static analysis alone).
