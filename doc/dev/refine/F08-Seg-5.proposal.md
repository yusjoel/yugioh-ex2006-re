# Refine Proposal: F08-Seg-5  [0x08067fa4..0x080690dc)

## 段测绘

- 函数入口 x20 (全部已命名):
  - 0x08067fa4 `scan_effect_slots_for_equip_sprite_field6`
  - 0x080682ac `invoke_equip_zone_entry_with_sprite_mode3`
  - 0x08068350 `invoke_equip_zone_entry_with_monster_slot_and_zone14`
  - 0x0806843c `apply_equip_lp_indicator_with_slot_score`
  - 0x080684e0 `invoke_equip_zone_entry_with_lp_chain_state`
  - 0x08068618 `advance_equip_effect_display_zone_match_guard`
  - 0x08068684 `tick_equip_effect_display_state_machine`
  - 0x080687a8 `invoke_equip_hand_slot_oam_if_eligible`
  - 0x0806882c `dispatch_equip_slot_sprite_by_zone_type`
  - 0x080688dc `apply_slot_equip_activation_by_zone_slot_match`
  - 0x08068990 `dispatch_equip_slot_sprite_by_state_and_zone`
  - 0x08068b58 `apply_equip_activation_by_zone_slot_state`
  - 0x08068bf4 `dispatch_equip_lp_field_state_by_card_id`
  - 0x08068c9c `apply_equip_activation_from_zone_entry_match`
  - 0x08068cd8 `apply_equip_activation_by_zone_slot_pair_match`
  - 0x08068d8c `apply_equip_oam_entry_via_zone_descriptor_lookup`
  - 0x08068e0c `apply_equip_slot_sprite_via_zone_match_and_score`
  - 0x08068f0c `enqueue_equip_sprite_attrs_via_zone_entry_check`
  - 0x08068f78 `dispatch_equip_slot_sprite_by_lp_state_neo_daedalus`
  - 0x08069008 `dispatch_equip_zone11_sprite_or_lp_row_by_state`

- 残留自动名槽 x65 (全部落在 [0x08067fa4, 0x080690dc)):

  | slot addr    | name                       | raw value    |
  |---|---|---|
  | 0x0806805c   | DWORD_0806805c             | 0x00000868   |
  | 0x08068060   | DWORD_08068060             | 0x0201c510   |
  | 0x08068064   | DWORD_08068064             | 0x0000131c   |
  | 0x08068068   | DWORD_08068068             | 0x000011f0   |
  | 0x0806806c   | DWORD_0806806c             | 0x00000ffa   |
  | 0x0806807c   | DWORD_0806807c             | 0x00001246   |
  | 0x08068098   | DWORD_08068098             | 0x0000134d   |
  | 0x080680b0   | DWORD_080680b0             | 0x0000149b   |
  | 0x080680b4   | DWORD_080680b4             | 0x00001364   |
  | 0x08068174   | DWORD_08068174             | 0x000016b8   |
  | 0x08068178   | DWORD_08068178             | 0x00000868   |
  | 0x0806817c   | DWORD_0806817c             | 0x0201c510   |
  | 0x080681fc   | DWORD_080681fc             | 0x00000868   |
  | 0x08068200   | DWORD_08068200             | 0x0201c510   |
  | 0x080682a4   | DWORD_080682a4             | 0x00000868   |
  | 0x080682a8   | DWORD_082a8               | 0x0201c510   |
  | 0x08068348   | DWORD_08068348             | 0x00000868   |
  | 0x0806834c   | DWORD_0806834c             | 0x0201c510   |
  | 0x08068418   | DAT_08068418               | 0x00000868   |
  | 0x0806841c   | DAT_0806841c               | 0x0201c510   |
  | 0x080684b8   | DAT_080684b8               | 0x00000868   |
  | 0x080684bc   | DAT_080684bc               | 0x0201c510   |
  | 0x08068548   | DWORD_08068548             | 0x00000868   |
  | 0x0806854c   | DWORD_0806854c             | 0x0201c510   |
  | 0x08068600   | DWORD_08068600             | 0x00001286   |
  | 0x0806865c   | DAT_0806865c               | 0x0201b290   |
  | 0x08068680   | DAT_08068680               | 0x00001daa   |
  | 0x080686a4   | DAT_080686a4               | 0x0201b290   |
  | 0x080686a8   | DAT_080686a8               | 0x080686ac   |
  | 0x08068760   | DAT_08068760               | 0x0000139d   |
  | 0x08068820   | DAT_08068820               | 0x00000868   |
  | 0x08068824   | DAT_08068824               | 0x0201c8f8   |
  | 0x080688d4   | DAT_080688d4               | 0x00000868   |
  | 0x080688d8   | DAT_080688d8               | 0x0201c510   |
  | 0x08068988   | DAT_08068988               | 0x00000868   |
  | 0x0806898c   | DAT_0806898c               | 0x0201c510   |
  | 0x08068a44   | DAT_08068a44               | 0x00000868   |
  | 0x08068a48   | DAT_08068a48               | 0x0201c510   |
  | 0x08068a64   | DAT_08068a64               | 0x0201b290   |
  | 0x08068abc   | DAT_08068abc               | 0x00000868   |
  | 0x08068ac0   | DAT_08068ac0               | 0x0201c600   |
  | 0x08068ad0   | DAT_08068ad0               | 0x000004a4   |
  | 0x08068b14   | DAT_08068b14               | 0x000004a4   |
  | 0x08068b18   | DAT_08068b18               | 0x00000868   |
  | 0x08068b1c   | DAT_08068b1c               | 0x0201c600   |
  | 0x08068bec   | DAT_08068bec               | 0x00000868   |
  | 0x08068bf0   | DAT_08068bf0               | 0x0201c510   |
  | 0x08068c34   | DAT_08068c34               | 0x0201b290   |
  | 0x08068c70   | DAT_08068c70               | 0x00008056   |
  | 0x08068c74   | DAT_08068c74               | 0x0201e500   |
  | 0x08068d84   | DWORD_08068d84             | 0x00000868   |
  | 0x08068d88   | DWORD_08068d88             | 0x0201c510   |
  | 0x08068f00   | DWORD_08068f00             | 0x00000868   |
  | 0x08068f04   | DWORD_08068f04             | 0x0201c510   |
  | 0x08068f08   | DWORD_08068f08             | 0x0000ffff   |
  | 0x08068f70   | DWORD_08068f70             | 0x0000801b   |
  | 0x08068f74   | DWORD_08068f74             | 0x0000801c   |
  | 0x08068fb0   | DWORD_08068fb0             | 0x0201b290   |
  | 0x08068ff0   | DWORD_08068ff0             | 0x000014f8   |
  | 0x08069058   | DWORD_08069058             | 0x0201b290   |
  | 0x0806905c   | DWORD_0806905c             | gP1LifePoints (=0x0201c4e0) |
  | 0x08069060   | DWORD_08069060             | 0x00000868   |
  | 0x080690d0   | DWORD_080690d0             | gP1LifePoints (=0x0201c4e0) |
  | 0x080690d4   | DWORD_080690d4             | 0x00001da8   |
  | 0x080690d8   | DWORD_080690d8             | 0x00001ce8   |

  ROM byte verification (python read_word): all 65 slots verified byte-identical to ASM values. conf: high.

- ROM_INCBIN / .byte 块: 0 (段内无 ROM_INCBIN; 唯一 .byte 为嵌入 4B THUMB stub @ 0x08068828,
  详见下方 disasm 计划)

- 嵌入 4B THUMB stub @ 0x08068828: `.byte 0x00, 0x20, 0x70, 0x47`
  = `movs r0,#0; bx lr` (return 0)
  THUMB+1 ptr = 0x08068829; raw refs=0; THUMB+1 refs=3 (at 0x09e3fed8/0x09e40478/0x09e40bc8)
  3 caller entries in card effect dispatch table (0x09e4xxxx, fn_eligible slot):
    - 0x09e3fed8: fn_eligible for CID 0x1302 = Royal Decree (pw=51452091, card-stats.s L8959)
    - 0x09e40478: fn_eligible for CID 0x1360 = Imperial Order (no existing constant; card-stats.s L9986)
    - 0x09e40bc8: fn_eligible for CID 0x1495 = The Emperor's Holiday (existing THE_EMPERORS_HOLIDAY_CID)
  判定: disasm THUMB stub -> 新函数 `check_equip_eligible_always_false`
  (CID at fn_ptr-4 per entry layout; fn_activate=0 for all 3 = null activate handler)
  conf: high (3 confirmed THUMB+1 dispatch table refs; byte-sequence = canonical return-0 stub)

## 数据块分类 (Rule 2/3) -- 每块给 ref-scan 证据

| 块 | ref-scan (raw / THUMB|1) | 判定 | 理由 |
|---|---|---|---|
| 0x08068828 sz=4 (.byte stub) | raw=0, THUMB+1=3 (0x09e3fed8/0x09e40478/0x09e40bc8) | disasm THUMB | 3 THUMB+1 refs from 0x09e4xxxx dispatch table; fn_eligible slot for Royal Decree/Imperial Order/The Emperor's Holiday |

No ROM_INCBIN blocks; no §5.1 candidates.

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate)

共 62 槽: 全部 ROM bytes 已 python 核对 (conf: high)

**高频复用 (EQ, reuse existing constants):**

| slot(s) | value | const_name | inc | slot_label |
|---|---|---|---|---|
| 0806805c / 8178 / 81fc / 82a4 / 8348 / 8418 / 84b8 / 8548 / 88d4 / 8988 / 8a44 / 8abc / 8b18 / 8bec / 8d84 / 8f00 / 9060 (x17) + DAT_08068820 (x1) = 18 total | 0x00000868 | PLAYER_BLOCK_STRIDE | duel_field.inc | `scan_effect_stride / invoke_sprite3_stride / ...` (按函数缩写命名) |
| 8060 / 817c / 8200 / 82a8 / 834c / 841c / 84bc / 854c / 88d8 / 898c / 8a48 / 8bf0 / 8d88 / 8f04 (x14) | 0x0201c510 | gDuelFieldSlots | ewram.inc | `scan_field_slots_base / ...` |
| 865c / 86a4 / 8a64 / 8c34 / 8fb0 / 9058 (x6) | 0x0201b290 | gDuelPhaseFlags | ewram.inc | `advance_guard_phase_flags / tick_sm_phase_flags / ...` |
| 8ac0 / 8b1c (x2) | 0x0201c600 | gP1FieldArrayCBase | ewram.inc | `dispatch_state_zone_field_c_base / ...` |
| 8ad0 / 8b14 (x2) | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc | `dispatch_state_zone_phase_frame_off / ...` |
| 0806824 (x1) | 0x0201c8f8 | gP1HandSlotArray | ewram.inc | `invoke_hand_slot_oam_hand_base` |
| 8c70 (x1) | 0x00008056 | OAM_EFFECT_SLOT_TILE_P1 | oam_attr.inc | `dispatch_lp_field_tile_p2` (caller uses player_id==1 path) |
| 8680 (x1) | 0x00001daa | LP_CARD_TRACK_NEXT_OFF | ewram.inc | `advance_guard_lp_track_next_off` |
| 90d4 (x1) | 0x00001da8 | LP_CARD_TRACK_BASE_OFF | ewram.inc | `dispatch_zone11_lp_track_base_off` |
| 90d8 (x1) | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc | `dispatch_zone11_lp_block2_off` |

**CID reuse (value grep in card_info.inc 命中):**

| slot | value | const_name | evidence |
|---|---|---|---|
| DWORD_08068064 | 0x0000131c | cid_131c | card_info.inc L1134; 0 hits -> already named cid_131c |
| DWORD_08068068 | 0x000011f0 | GREENKAPPA_CID | card_info.inc L1128 |
| DWORD_0806806c | 0x00000ffa | REAPER_OF_CARDS_CID | card_info.inc L1129 |
| DWORD_0806807c | 0x00001246 | HARPIES_FEATHER_DUSTER_CID | card_info.inc L1130 |
| DWORD_08068098 | 0x0000134d | DRIVING_SNOW_CID | card_info.inc L1131 |
| DWORD_080680b0 | 0x0000149b | BAIT_DOLL_CID | card_info.inc L1133 |
| DWORD_080680b4 | 0x00001364 | NOBLEMAN_EXTERMINATION_CID | card_info.inc L1132 |
| DWORD_08068174 | 0x000016b8 | CRIMSON_NINJA_CID | card_info.inc L744 |

**CID new (value grep in card_info.inc = 0 命中):**

| slot | value | card name | card-stats.s | const_name |
|---|---|---|---|---|
| DWORD_08068600 | 0x00001286 | Blast Sphere | L7763 slot=0x1286 pw=26302522 | BLAST_SPHERE_CID |
| DAT_08068760 | 0x0000139d | Birdface | L10597 slot=0x139D pw=45547649 | BIRDFACE_CID |

**其他新建常量 (domain 裁定):**

| slot | value | domain | const_name | inc | 理由 |
|---|---|---|---|---|---|
| DAT_08068c74 | 0x0201e500 | EWRAM 全局基址 | gEquipLpZoneEntryBase | ewram.inc | 28 raw ROM refs; 非 card sentinel; 非 OAM attr; EWRAM equip LP zone entry buffer base; used in dispatch_equip_lp_field_state_by_card_id to read card_type word; conf: high |
| DWORD_08068f08 | 0x0000ffff | sprite score cap | EQUIP_SLOT_SCORE_CAP | card_info.inc or oam_attr.inc | 域裁定: SLOT_CARD_EMPTY=0xffff (card domain, L386 card_info.inc) + OAM_ATTR0_HIDDEN=0xffff (OAM domain, L13 oam_attr.inc) 均同值但语义不同; 本处=`apply_equip_slot_sprite_via_zone_match_and_score` 内 score saturate cap; Seg-4 域裁定先例适用; conf: high |
| DWORD_08068f70 | 0x0000801b | OAM sprite tile | OAM_EQUIP_SPRITE_TILE_P2_1B | oam_attr.inc | value grep = 0; player_id==1 path; pattern (0x8000 | 0x1b); sibling of OAM_EFFECT_SLOT_TILE_P1=0x8056; conf: high |
| DWORD_08068f74 | 0x0000801c | OAM sprite tile | OAM_EQUIP_SPRITE_TILE_P2_1C | oam_attr.inc | value grep = 0; player_id==1 path; second sprite attr code for same zone check fn; sibling of OAM_EQUIP_SPRITE_TILE_P2_1B; conf: high |
| DWORD_08068ff0 | 0x000014f8 | OAM entry attr | EQUIP_OAM_ENTRY_ATTR_14F8 | ewram.inc or oam_attr.inc | 8 raw ROM refs; value grep = 0; used in dispatch_equip_slot_sprite_by_lp_state_neo_daedalus as `setup_equip_oam_entry_with_sprite_attr` sp[0x4] entry attr word; conf: med (semantic is OAM attr entry, full decoding not done) |

### REF_SLOTS (USER-label + DATA-ref)

| slot | target | gas_label | slot_label |
|---|---|---|---|
| PTR_gP1LifePoints_0806867c | gP1LifePoints (already in .word) | gP1LifePoints | advance_guard_lp_track_base_ptr |
| DAT_080686a8 | 0x080686ac = switchD_080686a2__switchdataD_080686ac | switchD_080686a2__switchdataD_080686ac | tick_sm_switch_table_ptr |
| DWORD_0806905c | gP1LifePoints (already in .word) | gP1LifePoints | dispatch_zone11_gp1lp_base_a |
| DWORD_080690d0 | gP1LifePoints (already in .word) | gP1LifePoints | dispatch_zone11_gp1lp_base_b |

Note: PTR_gP1LifePoints_0806867c and DWORD_0806905c/d0 already emit `.word gP1LifePoints` symbol; only slot label rename needed.
DAT_080686a8 also needs .word value changed from raw 0x080686ac to `switchD_080686a2__switchdataD_080686ac`.

### RENAME_SLOTS (纯改名 + EOL)

All 65 auto-name slots get descriptive label renames. Key slots listed (others follow fn-prefix_value pattern):

| slot addr | slot_label | eol_ascii |
|---|---|---|
| 0x0806865c | advance_guard_phase_flags_base | @ gDuelPhaseFlags |
| 0x08068680 | advance_guard_lp_track_next_off | @ LP_CARD_TRACK_NEXT_OFF |
| 0x080686a4 | tick_sm_phase_flags_base | @ gDuelPhaseFlags |
| 0x080686a8 | tick_sm_switch_table_ptr | @ switchD_080686a2__switchdataD_080686ac |
| 0x08068600 | invoke_lp_chain_blast_sphere_cid | @ BLAST_SPHERE_CID |
| 0x08068760 | tick_sm_birdface_cid | @ BIRDFACE_CID |
| 0x08068ac0 | dispatch_state_zone_field_c_base | @ gP1FieldArrayCBase |
| 0x08068ad0 | dispatch_state_zone_phase_frame_off | @ EQUIP_PHASE_FRAME_OFF |
| 0x08068b14 | dispatch_state_zone_phase_frame_off_b | @ EQUIP_PHASE_FRAME_OFF |
| 0x08068b1c | dispatch_state_zone_field_c_base_b | @ gP1FieldArrayCBase |
| 0x08068c70 | dispatch_lp_field_tile_p2 | @ OAM_EFFECT_SLOT_TILE_P1 |
| 0x08068c74 | dispatch_lp_field_zone_entry_base | @ gEquipLpZoneEntryBase |
| 0x08068f08 | apply_slot_score_cap | @ EQUIP_SLOT_SCORE_CAP |
| 0x08068f70 | enqueue_sprite_tile_p2_1b | @ OAM_EQUIP_SPRITE_TILE_P2_1B |
| 0x08068f74 | enqueue_sprite_tile_p2_1c | @ OAM_EQUIP_SPRITE_TILE_P2_1C |
| 0x08068ff0 | dispatch_neo_daedalus_oam_entry_attr | @ EQUIP_OAM_ENTRY_ATTR_14F8 |
| 0x0806905c | dispatch_zone11_gp1lp_base_a | @ gP1LifePoints |
| 0x08069060 | dispatch_zone11_stride | @ PLAYER_BLOCK_STRIDE |
| 0x080690d0 | dispatch_zone11_gp1lp_base_b | @ gP1LifePoints |
| 0x080690d4 | dispatch_zone11_lp_track_base_off | @ LP_CARD_TRACK_BASE_OFF |
| 0x080690d8 | dispatch_zone11_lp_block2_off | @ P1LP_BLOCK2_OFF_1CE8 |

### FUNC_RENAME (误名订正)

None. 全部 20 个函数名经消费者证据核查无矛盾。

注: 第一个 Seg-6 函数 `tick_dragon_summon_display_if_slots_paired` (0x080690dc) 的 plate 中
"0x128b (Stamping Destruction)" 有误 (0x128b = Lord of D., card-stats.s L7802 pw=17985575);
函数名本身无误 (Lord of D. 是龙族联动召唤套路牌); 该 plate 属 Seg-6 范围, 在 Seg-6 修正。

### PLATE (R5; 全 ASCII)

**Seg-5 内 CJK plate (2 处, 均需整段重写):**

1. `dispatch_equip_slot_sprite_by_zone_type` @ 0x0806882c (asm line 10092):
   Current plate: CJK mojibake (装备槽精灵派发函数...)
   ASCII replacement:
   ```
   Dispatches equip slot sprite based on zone_type code in effect_slot[+0xc].
   type==1: calls invoke_equip_slot_eligibility_via_effect_node_bitmap(slot).
   type==2: aggregates col_nibble from both player sides of gDuelFieldSlots (stride 0x868),
     compares sum with slot[+0x4] bits[14:8] target; on match calls
     check_effect_slot_matches_zone_entry + read_effect_slot_side_and_type +
     invoke_effect_node_with_active_flag_3arg; on activation extracts player_id/slot_group
     and calls enqueue_equip_chain_slot_sprite_with_pair_lookup.
   Other type or mismatch: returns 0. indeg=0, Sub-type A.
   ```

2. `tick_dragon_summon_display_if_slots_paired` @ 0x080690dc (asm line 11400) [Seg-6 boundary]:
   This plate is technically the pre-entry comment for the first Seg-6 function.
   Correction note: wrong card name "Stamping Destruction" -> "Lord of D."
   Flagged for Seg-6 to fix. ASCII replacement for Seg-6:
   ```
   Checks whether Lord of D. (CID=0x128b) paired slots exist via count_paired_slots_both_sides;
   if count > 0, delegates to tick_dragon_summon_effect_display_state_machine(card_entry, scene).
   Returns 0 if no paired slots. indeg=0, fn-ptr table driven.
   ```

## disasm 计划 (R4)

**Embedded THUMB stub @ 0x08068828 (4B: 0x00, 0x20, 0x70, 0x47)**

- Range: 0x08068828..0x0806882c (4 bytes)
- Instruction decode: `movs r0,#0x0` (0x2000) + `bx lr` (0x4770) = return 0
- THUMB+1 refs: 3 callers at 0x09e3fed8, 0x09e40478, 0x09e40bc8 (all 0x09e4xxxx dispatch table fn_eligible slots)
- CIDs served:
  - 0x1302 = Royal Decree (entry at 0x09e3fed8-4; pw=51452091; card-stats.s L8959)
  - 0x1360 = Imperial Order (entry at 0x09e40478-4; pw=61740673; card-stats.s L9986)
  - 0x1495 = The Emperor's Holiday (entry at 0x09e40bc8-4; pw=68400115; card-stats.s L12742)
- Plan: Ghidra RefineF08Seg5.py:
  1. createLabel(0x08068828, "check_equip_eligible_always_false", PUBLIC)
  2. setTMode(0x08068828, True)
  3. DisassembleCommand(0x08068828, 4)
  4. createFunction(0x08068828, "check_equip_eligible_always_false")
  5. plate: "Always-false equip eligibility stub; referenced by Royal Decree (0x1302), Imperial Order (0x1360), The Emperor's Holiday (0x1495) handler table fn_eligible slots; movs r0,#0; bx lr. indeg=0 (dispatch table only)."
- New CID constant needed: IMPERIAL_ORDER_CID = 0x1360 (new; card_info.inc)
  (ROYAL_DECREE_CID=0x1302 already exists L790; THE_EMPERORS_HOLIDAY_CID=0x1495 already exists L509)

**switchD_080686a2 status: already inline disassembled**
- Jump table at 0x080686ac (28 entries, state - 0x64 range [0..0x1c]) is already fully laid out as .word entries
- All 5 case stubs (caseD_80/7f/7e/78/64) and default (caseD_65) already have labels
- No additional R4 disasm action needed

## carve 计划 (R7)

None (no ROM_INCBIN or data table blocks in Seg-5).

## 新增 constants / 全局

**card_info.inc (新建 2 CID + 1 off):**
- `BLAST_SPHERE_CID = 0x00001286` (value grep = 0; card-stats.s L7763 slot=0x1286 pw=26302522; conf: high)
- `BIRDFACE_CID = 0x0000139d` (value grep = 0; card-stats.s L10597 slot=0x139D pw=45547649; conf: high)
- `IMPERIAL_ORDER_CID = 0x00001360` (value grep = 0; card-stats.s L9986 slot=0x1360 pw=61740673; for stub labeling; conf: high)

**ewram.inc (新建 1 全局 + 1 constant):**
- `gEquipLpZoneEntryBase = 0x0201e500` (28 raw ROM refs; new global between gEquipZoneRankState=0x0201e4d0 and next; reads as zone entry descriptor word; plate comment in this file calls it "ZONE_ENTRY_BASE" and "OAM_DATA_PTR" -- both usages in file 08: DAT_08068c74 + DAT_08069828 in Seg-6; conf: med -- naming based on Seg-5 usage; Seg-6 may refine)
- `EQUIP_OAM_ENTRY_ATTR_14F8 = 0x000014f8` (8 raw ROM refs; used as sprite attr entry value in setup_equip_oam_entry_with_sprite_attr call; conf: med)

**oam_attr.inc (新建 3):**
- `OAM_EQUIP_SPRITE_TILE_P2_1B = 0x0000801b` (0 raw refs in constants; pattern 0x8000|0x1b; player_id==1 path in enqueue_equip_sprite_attrs_via_zone_entry_check; conf: high)
- `OAM_EQUIP_SPRITE_TILE_P2_1C = 0x0000801c` (24 raw ROM refs; sibling of P2_1B; second sprite code; conf: high)
- `EQUIP_SLOT_SCORE_CAP = 0x0000ffff` (domain exception: SLOT_CARD_EMPTY=0xffff card domain + OAM_ATTR0_HIDDEN=0xffff OAM domain; this is score saturation cap in apply_equip_slot_sprite_via_zone_match_and_score; Seg-4 precedent; conf: high)

## §5.1 登记 (Rule 3) -- 0 引用块

None. 段内唯一 .byte 块 (0x08068828/4B) 有 3 THUMB+1 引用, 归 disasm 计划。

## 消费者证据 (R6) -- 关键槽语义

- BLAST_SPHERE_CID (0x1286) @ DWORD_08068600: `invoke_equip_zone_entry_with_lp_chain_state` L9814
  `ldr r0, DWORD_08068600; ldrh r2,[r7,#0x0]; cmp r2,r0; bne LAB_08068586` -- cmp card_id == 0x1286
  then calls `enqueue_equip_slot_bitmap_update` / `get_slot_field5_score` / `submit_lp_change_indicator_with_chain_check`
  conf: high (card_id branch dispatch)

- BIRDFACE_CID (0x139d) @ DAT_08068760: `tick_equip_effect_display_state_machine` caseD_7f L9973
  `ldr r0, DAT_08068760; ldrh r1,[r4,#0x0]; cmp r1,r0; bne LAB_08068764`
  then calls `init_effect_slot_display_context(player, card_id, mode=6, 0)` (special case path)
  conf: high (named card branch in state machine)

- gEquipLpZoneEntryBase (0x0201e500) @ DAT_08068c74: `dispatch_equip_lp_field_state_by_card_id` L10713
  `ldr r0, DAT_08068c74; ldr r2,[r0,#0x0]` then extracts card_type bits (lsls/lsrs) for sprite_code selection
  Secondary ref: asm/08 L12526 (Seg-6) same pattern. conf: med (semantic: equip LP zone entry buffer; exact struct TBD)

- OAM_EQUIP_SPRITE_TILE_P2_1B/P2_1C @ DWORD_08068f70/74: `enqueue_equip_sprite_attrs_via_zone_entry_check` L11171/11173
  `cmp r6,#0; beq; ldr r0, DWORD_08068f70` (player_id==1 selects 0x801b for first sprite)
  `cmp r0,#0; beq; ldr r1, DWORD_08068f74` (player_id==1 selects 0x801c for second sprite)
  conf: high (P2-side sprite tile region pattern consistent with OAM_EFFECT_SLOT_TILE_P1=0x8056)

- EQUIP_OAM_ENTRY_ATTR_14F8 @ DWORD_08068ff0: `dispatch_equip_slot_sprite_by_lp_state_neo_daedalus` L11255
  `ldr r2, DWORD_08068ff0; lsls r1,r1,#0xd; orrs r1,r2; str r1,[sp,#0x4]` -- builds sprite entry word
  then `add r1,sp,#0x4; movs r2,#0x1; bl setup_equip_oam_entry_with_sprite_attr`
  conf: med (builds attr word via OR with 0x14f8; exact OAM attr structure TBD)

- EQUIP_SLOT_SCORE_CAP (0xffff) @ DWORD_08068f08: `apply_equip_slot_sprite_via_zone_match_and_score` L11103
  `ldr r3, DWORD_08068f08; cmp r0,r3; ble; adds r0,r3,#0` -- saturate sp[0x1c] at 0xffff
  `cmp r2,r3; ble; adds r2,r3,#0` -- saturate sp[0x20] at 0xffff
  conf: high (explicit saturation pattern; unambiguous score cap use)

## 求助

- EQUIP_OAM_ENTRY_ATTR_14F8 = 0x14f8: semantics partially unclear (conf: med). Fixer should check all 8 raw refs to determine if a more descriptive name is warranted (e.g., if it's always combined with player_id<<0xd). Current name is conservative; fixer may rename after cross-checking other occurrences.

- gEquipLpZoneEntryBase = 0x0201e500: name based on Seg-5 usage only. Seg-6 (asm line 12439) describes it as "OAM_DATA_PTR". Two different plate descriptions suggest this global may have multiple uses. Fixer should cross-check Seg-6 usage before finalizing ewram.inc entry.
