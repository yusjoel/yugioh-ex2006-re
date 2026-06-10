# Refine Proposal: F03Seg2  [0x08036a78..0x08037128)

## 段测绘

### 函数入口 x13

| 地址 | 函数名 |
|------|--------|
| 0x08036a78 | sum_equip_slot_effect_values_for_player |
| 0x08036ac0 | check_slot_card_eligible_for_special_action |
| 0x08036b88 | find_effect_entry_by_player_zone |
| 0x08036c2c | build_effect_zone_entry |
| 0x08036cb8 | place_card_into_graveyard_slot |
| 0x08036d08 | place_card_into_graveyard_slot_with_seq |
| 0x08036d80 | remove_equip_slot_by_index_from_array_a |
| 0x08036de8 | erase_slot_from_equip_array_a_by_ptr |
| 0x08036e40 | insert_card_into_hand_list_by_zone_desc |
| 0x08036f0c | insert_card_into_field_list_by_zone_desc |
| 0x08037030 | find_deck_slot_by_card_pair_match |
| 0x08037088 | find_graveyard_entry_by_ptr |
| 0x080370dc | count_extra_deck_cards_by_id |

### 残留自动名槽 x37

PTR_ 槽 (8 个) — 已含 gP1LifePoints 常量引用，仅需改槽 label:
- 0x08036d78 `PTR_gP1LifePoints_08036d78` = gP1LifePoints
- 0x08036dd4 `PTR_gP1LifePoints_08036dd4` = gP1LifePoints
- 0x08036e28 `PTR_gP1LifePoints_08036e28` = gP1LifePoints
- 0x08036ee0 `PTR_gP1LifePoints_08036ee0` = gP1LifePoints
- 0x08036ffc `PTR_gP1LifePoints_08036ffc` = gP1LifePoints
- 0x08037068 `PTR_gP1LifePoints_08037068` = gP1LifePoints
- 0x080370c0 `PTR_gP1LifePoints_080370c0` = gP1LifePoints
- 0x08037120 `PTR_gP1LifePoints_08037120` = gP1LifePoints

DAT_ 槽 (29 个): 0x08036ab8 ~ 0x08037124

### ROM_INCBIN / .byte 块

本段无 ROM_INCBIN / .byte 块。

---

## 数据块分类 (Rule 2/3)

本段 0 个 ROM_INCBIN/.byte 块，无需 ref-scan 分类。

---

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate; 新建/复用)

注: 全 37 槽均为 EQ_SLOTS (PTR_ + DAT_)，无 RENAME_SLOTS (段内无纯改名槽)。

#### 复用现有常量

| 物理槽 | 值 | 现有常量名 | 来源 inc |
|--------|-----|-----------|----------|
| DAT_08036ab8 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_08036abc | 0x0201c510 | gDuelFieldSlots | ewram.inc |
| DAT_08036b0c | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_08036b10 | 0x0201c510 | gDuelFieldSlots | ewram.inc |
| DAT_08036b78 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_08036b7c | 0x0201c510 | gDuelFieldSlots | ewram.inc |
| DAT_08036bf8 | 0x0201b290 | gDuelPhaseFlags | ewram.inc |
| DAT_08036cb4 | 0xffff803f | SCROLLBAR_CLEAR_BITS_14_6 | gl_scrollbar.inc |
| DAT_08036cfc | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_08036d00 | 0x0201c8f8 | gP1HandSlotArray | ewram.inc |
| DAT_08036d7c | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| PTR_gP1LifePoints_08036d78 | 0x0201c4e0 | gP1LifePoints | ewram.inc |
| DAT_08036dd8 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| PTR_gP1LifePoints_08036dd4 | 0x0201c4e0 | gP1LifePoints | ewram.inc |
| DAT_08036e2c | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| PTR_gP1LifePoints_08036e28 | 0x0201c4e0 | gP1LifePoints | ewram.inc |
| DAT_08036ee4 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_08036ee8 | 0x0201c8f8 | gP1HandSlotArray | ewram.inc |
| PTR_gP1LifePoints_08036ee0 | 0x0201c4e0 | gP1LifePoints | ewram.inc |
| DAT_08037000 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_08037004 | 0x0201cab0 | gP1AltHandSlotArray | ewram.inc |
| PTR_gP1LifePoints_08036ffc | 0x0201c4e0 | gP1LifePoints | ewram.inc |
| DAT_0803706c | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_08037070 | 0x0201c8f8 | gP1HandSlotArray | ewram.inc |
| PTR_gP1LifePoints_08037068 | 0x0201c4e0 | gP1LifePoints | ewram.inc |
| DAT_080370c4 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| PTR_gP1LifePoints_080370c0 | 0x0201c4e0 | gP1LifePoints | ewram.inc |
| DAT_08037124 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| PTR_gP1LifePoints_08037120 | 0x0201c4e0 | gP1LifePoints | ewram.inc |

共 29 个复用槽。

#### 新建常量 EQ 槽

| 物理槽 | 值 | 新常量名 | 目标 inc | 说明 |
|--------|-----|---------|---------|------|
| DAT_08036b2c | 0x000013ea | GAP_CID_13EA | card_info.inc | gap slot (no card in card-stats.s; range [0x13E8..0x13EB]=Nuvia/Soul Exchange); also used as RENAME in Seg-1 check_slot_equip_elig_cid_13ea but no constant was created there |
| DAT_08036b30 | 0x00001231 | KUNAI_WITH_CHAIN_CID | card_info.inc | Kunai with Chain (pw=37390589); slot=0x1231; check_slot_card_eligible_for_special_action; note: Metalmorph(0x1238) computed inline as +7 |
| DAT_08036b74 | 0x00001514 | BLAST_WITH_CHAIN_CID | card_info.inc | Blast with Chain (pw=98239899); slot=0x1514; note: Hero Heyro(0x1980) computed inline as 0xcc<<5 |
| DAT_08036bfc | 0x00000594 | EFFECT_ENTRY_COUNT_OFF | ewram.inc (as offset note) | gDuelPhaseFlags+0x594 = effect entry count field; 9 raw refs in ROM |
| DAT_08036c00 | 0x0201b590 | gEffectEntryArray | ewram.inc | effect entry array base (stride=0x18, count at gDuelPhaseFlags+0x594); 23 raw refs |
| DAT_08036d04 | 0xfffffbfc | HAND_ARRAY_TO_COUNT_NEG_OFF | ewram.inc | gP1HandSlotArray(0x0201c8f8)+0xfffffbfc=gP1HandCountBase(0x0201c4f4); neg delta from hand slot array to hand count base; 5 raw refs |
| DAT_08036eec | 0xfffffbfc | HAND_ARRAY_TO_COUNT_NEG_OFF | ewram.inc (reuse above) | same value, same meaning |
| DAT_08037008 | 0xfffffa4c | ALT_HAND_ARRAY_TO_COUNT_NEG_OFF | ewram.inc | gP1AltHandSlotArray(0x0201cab0)+0xfffffa4c=gP1AltHandCountBase(0x0201c4fc); neg delta from alt-hand slot array to alt-hand count base; 3 raw refs |

共 8 个新建槽 (含 1 个重复复用 HAND_ARRAY_TO_COUNT_NEG_OFF)。

---

### EQ_SLOTS 汇总表 (Ghidra 操作用, C13 全覆盖 37 EQ + 0 RENAME = 37)

以下每行: (slot_addr, value, const_name, slot_label)

```
EQ  0x08036ab8  PLAYER_BLOCK_STRIDE            DAT_08036ab8               ->  sum_equip_slot_values_stride
EQ  0x08036abc  gDuelFieldSlots                DAT_08036abc               ->  sum_equip_slot_values_slots
EQ  0x08036b0c  PLAYER_BLOCK_STRIDE            DAT_08036b0c               ->  check_special_action_elig_stride
EQ  0x08036b10  gDuelFieldSlots                DAT_08036b10               ->  check_special_action_elig_slots
EQ  0x08036b2c  GAP_CID_13EA                   DAT_08036b2c               ->  check_special_action_elig_cid_13ea
EQ  0x08036b30  KUNAI_WITH_CHAIN_CID           DAT_08036b30               ->  check_special_action_elig_kunai_cid
EQ  0x08036b74  BLAST_WITH_CHAIN_CID           DAT_08036b74               ->  check_special_action_elig_blast_cid
EQ  0x08036b78  PLAYER_BLOCK_STRIDE            DAT_08036b78               ->  check_special_action_elig_stride_b
EQ  0x08036b7c  gDuelFieldSlots                DAT_08036b7c               ->  check_special_action_elig_slots_b
EQ  0x08036bf8  gDuelPhaseFlags                DAT_08036bf8               ->  find_effect_entry_phase_flags
EQ  0x08036bfc  EFFECT_ENTRY_COUNT_OFF         DAT_08036bfc               ->  find_effect_entry_count_off
EQ  0x08036c00  gEffectEntryArray              DAT_08036c00               ->  find_effect_entry_array
EQ  0x08036cb4  SCROLLBAR_CLEAR_BITS_14_6      DAT_08036cb4               ->  build_effect_zone_entry_mask
EQ  0x08036cfc  PLAYER_BLOCK_STRIDE            DAT_08036cfc               ->  place_card_graveyard_stride
EQ  0x08036d00  gP1HandSlotArray               DAT_08036d00               ->  place_card_graveyard_gy_base
EQ  0x08036d04  HAND_ARRAY_TO_COUNT_NEG_OFF    DAT_08036d04               ->  place_card_graveyard_count_neg_off
EQ  0x08036d78  gP1LifePoints                  PTR_gP1LifePoints_08036d78 ->  place_card_graveyard_seq_lp_ptr
EQ  0x08036d7c  PLAYER_BLOCK_STRIDE            DAT_08036d7c               ->  place_card_graveyard_seq_stride
EQ  0x08036dd4  gP1LifePoints                  PTR_gP1LifePoints_08036dd4 ->  remove_equip_slot_a_lp_ptr
EQ  0x08036dd8  PLAYER_BLOCK_STRIDE            DAT_08036dd8               ->  remove_equip_slot_a_stride
EQ  0x08036e28  gP1LifePoints                  PTR_gP1LifePoints_08036e28 ->  erase_equip_array_a_lp_ptr
EQ  0x08036e2c  PLAYER_BLOCK_STRIDE            DAT_08036e2c               ->  erase_equip_array_a_stride
EQ  0x08036ee0  gP1LifePoints                  PTR_gP1LifePoints_08036ee0 ->  insert_hand_list_lp_ptr
EQ  0x08036ee4  PLAYER_BLOCK_STRIDE            DAT_08036ee4               ->  insert_hand_list_stride
EQ  0x08036ee8  gP1HandSlotArray               DAT_08036ee8               ->  insert_hand_list_gy_base
EQ  0x08036eec  HAND_ARRAY_TO_COUNT_NEG_OFF    DAT_08036eec               ->  insert_hand_list_count_neg_off
EQ  0x08036ffc  gP1LifePoints                  PTR_gP1LifePoints_08036ffc ->  insert_field_list_lp_ptr
EQ  0x08037000  PLAYER_BLOCK_STRIDE            DAT_08037000               ->  insert_field_list_stride
EQ  0x08037004  gP1AltHandSlotArray            DAT_08037004               ->  insert_field_list_althand_base
EQ  0x08037008  ALT_HAND_ARRAY_TO_COUNT_NEG_OFF DAT_08037008              ->  insert_field_list_count_neg_off
EQ  0x08037068  gP1LifePoints                  PTR_gP1LifePoints_08037068 ->  find_deck_slot_lp_ptr
EQ  0x0803706c  PLAYER_BLOCK_STRIDE            DAT_0803706c               ->  find_deck_slot_stride
EQ  0x08037070  gP1HandSlotArray               DAT_08037070               ->  find_deck_slot_hand_base
EQ  0x080370c0  gP1LifePoints                  PTR_gP1LifePoints_080370c0 ->  find_graveyard_entry_lp_ptr
EQ  0x080370c4  PLAYER_BLOCK_STRIDE            DAT_080370c4               ->  find_graveyard_entry_stride
EQ  0x08037120  gP1LifePoints                  PTR_gP1LifePoints_08037120 ->  count_extra_deck_lp_ptr
EQ  0x08037124  PLAYER_BLOCK_STRIDE            DAT_08037124               ->  count_extra_deck_stride
```

---

### RENAME_SLOTS (纯改名 + EOL)

本段无纯 RENAME 槽 (无 gap CID 或高频通用值需单独改名)。

---

### FUNC_RENAME (误名订正)

无函数改名。

---

### PLATE_FULL (整段 setPlateComment 重写, 全 ASCII)

13 个 plate 全重写 (消除 CJK / 纯化 ASCII):

注: `find_deck_slot_by_card_pair_match` (0x08037030) 当前 plate 含 CJK 乱码 (Line 2334 of asm), **必须重写**。其余 12 个 plate 目前无 CJK 但一并重写以保一致性和格式规范化。

```
PLATE  0x08036a78  sum_equip_slot_effect_values_for_player:
"Sums effect card values for all active equip slots of a player. r0=player_id [0..1].
Iterates slots 0..10 (stride=PLAYER_BLOCK_STRIDE=0x868, slot_stride=0x14).
Per slot: tests bit19 of slot[0] (activation flag); if set, checks slot[+0x8] card_id nonzero;
on both: calls get_slot_effect_card_value(player, slot_idx) and accumulates.
Returns r7 = sum of effect values across all 11 active equip slots.
Constants: gDuelFieldSlots, PLAYER_BLOCK_STRIDE, activation_bit=19."

PLATE  0x08036ac0  check_slot_card_eligible_for_special_action:
"Checks equip activation eligibility for 5 special card_ids.
r0=player_id [0..1]; r1=slot_idx [0..0xb]; r2=card_id [0..0x172f].
Steps: (1) card_id==0 -> return 0; (2) slot in [5..9] -> check_card_field5_is_nonzero, hit->1;
(3) get_card_extended_stat_field9==3 -> slot in [5..0xa] active_bit check at gDuelFieldSlots+8;
(4) field9!=3 -> match against 5 special CIDs:
  GAP_CID_13EA(0x13ea,gap), KUNAI_WITH_CHAIN_CID(0x1231), KUNAI+7=Metalmorph(0x1238),
  BLAST_WITH_CHAIN_CID(0x1514), 0xcc<<5=Hero_Heyro(0x1980);
  on match: slot in [0..4] and active_bit nonzero and [slot+0x10].bit1==0 -> return 1.
Returns 1 if eligible, 0 if not. Read-only."

PLATE  0x08036b88  find_effect_entry_by_player_zone:
"Reverse-scans effect entry array (gEffectEntryArray=0x0201b590, stride=0x18)
for an entry matching player_side and zone_type.
count = [gDuelPhaseFlags + EFFECT_ENTRY_COUNT_OFF(0x594)].
Per candidate: [+2].bit0==r10(player_side) and [+2].bits[1..5]==r9(zone_type).
Inner loop: calls read_effect_slot_side_and_type(entry, sub_slot_idx) for each sub-slot,
compares packed result (slot_idx<<8|player_side) against key; returns 1 on first full match.
r0=u32 player_side [0..1], r1=u32 slot_idx [0..4] (stacked), r2=player_side->r10, r3=zone_type->r9.
Returns u32 bool (1=match found, 0=not found). Read-only."

PLATE  0x08036c2c  build_effect_zone_entry:
"Builds and submits an effect zone entry for player_side(r0), zone_idx(r1 >=5).
zone_idx<=4 returns 0 immediately (monster zone ignored).
Steps: (1) get_zone_slot_ptr(player_side, zone_idx) -> slot_ptr r4;
(2) alloca 0x18 bytes stack, zero-fill via memset;
(3) write player_side&1 to buf[+2].bit0 and zone_idx&0x1f to buf[+2].bits[1..5];
(4) read card_id bits[12:0] from slot_ptr, write to buf[+0];
(5) pack extra fields into buf[+4] using mask SCROLLBAR_CLEAR_BITS_14_6(0xffff803f);
(6) clear buf[+3] bits 0x31;
(7) call check_card_placement_rules(buf) and return result.
Returns 0 on early exit, else check_card_placement_rules result."

PLATE  0x08036cb8  place_card_into_graveyard_slot:
"Places a card into the player graveyard array (gP1HandSlotArray+0x418 path).
r0=card_slot_ptr. Extracts player_id from card_slot_ptr[0].bit14.
Reads graveyard count from [gP1HandCountBase + player*PLAYER_BLOCK_STRIDE].
Graveyard array base = gP1HandSlotArray + player*PLAYER_BLOCK_STRIDE.
(HAND_ARRAY_TO_COUNT_NEG_OFF maps gP1HandSlotArray -> gP1HandCountBase.)
If card_type(bits[18:0])!=0 and check_card_field8_is_9==0:
  calls write_word_from_deref_src to write; increments count.
Simpler variant (no sequence word); caller FUN_08032280 case 0xe (zone_type=14)."

PLATE  0x08036d08  place_card_into_graveyard_slot_with_seq:
"Places a card into the player graveyard array with an attached sequence word.
r0=card_slot_ptr (->r9 via 0x4681), r1=sequence_word (->r10 via 0x468a).
Extracts player_id from card_slot_ptr[0].bit14.
Count field: [gP1LifePoints + player*PLAYER_BLOCK_STRIDE + 0x1c].
Array base: gP1LifePoints + player*PLAYER_BLOCK_STRIDE + 0xba*8 (=0x5d0).
If card_type!=0 and check_card_field8_is_9==0:
  write_word_from_deref_src(slot_ptr), store sequence halfword at array+count*2+gP1LP+0xf1*8,
  increment count.
Caller FUN_08032280 case 0xf (zone_type=15)."

PLATE  0x08036d80  remove_equip_slot_by_index_from_array_a:
"Removes element by index from equip array A and left-shifts subsequent elements.
r0=player_id [0..1], r1=slot_idx [0..count-1].
Array A base: gP1LifePoints + player*PLAYER_BLOCK_STRIDE + 0x83*8 (=0x418).
Count field: gP1LifePoints + player*PLAYER_BLOCK_STRIDE + 0x14.
If slot_idx>=count returns 0; else: decrement count; shift elements [idx+1..new_count]
  left via write_word_from_deref_src loop; return 1.
Called by erase_slot_from_equip_array_a_by_ptr after ptr match."

PLATE  0x08036de8  erase_slot_from_equip_array_a_by_ptr:
"Searches equip array A for element matching card_ptr; deletes it via remove_equip_slot_by_index_from_array_a.
r0=player_id [0..1], r1=card_ptr (->r7).
Array A base: gP1LifePoints + player*PLAYER_BLOCK_STRIDE + 0x83*8 (=0x418).
Count field offset: 0x14. Backward scan from count-1 to 0 via check_deref_words_equal.
Returns 1 on success, 0 if not found.
Caller FUN_08032194 (duel_field) cleans up equip array A when a card leaves the field."

PLATE  0x08036e40  insert_card_into_hand_list_by_zone_desc:
"Searches player hand list for target card by zone descriptor; shifts it to front via swap_deref_words.
r0=player_side (bit0), r1=target zone_desc (u16 [0..0xffff]).
Hand count: gP1LifePoints + player*PLAYER_BLOCK_STRIDE + 0x14.
Hand array A: gP1LifePoints + player*PLAYER_BLOCK_STRIDE + 0x83*8 (=0x418).
(HAND_ARRAY_TO_COUNT_NEG_OFF maps gP1HandSlotArray -> gP1HandCountBase.)
Zone desc match: bits[23:16] and bit[13] of slot word.
On match: swap_deref_words then write_word_from_deref_src to shift subsequent slots.
Symmetric to insert_card_into_field_list_by_zone_desc (zone_type=0xe path)."

PLATE  0x08036f0c  insert_card_into_field_list_by_zone_desc:
"Searches player field slot list for target by zone descriptor; inserts via write_word_from_deref_src + strh.
r0=player_side (bit0), r1=target zone_desc (u16 [0..0xffff]).
Alt-hand count: gP1LifePoints + player*PLAYER_BLOCK_STRIDE + 0x1c.
Array A: gP1AltHandSlotArray + player*PLAYER_BLOCK_STRIDE (0xba*8=0x5d0 offset base).
Array B: gP1LifePoints + player*PLAYER_BLOCK_STRIDE + 0xf1*8 (=0x788).
(ALT_HAND_ARRAY_TO_COUNT_NEG_OFF maps gP1AltHandSlotArray -> gP1AltHandCountBase.)
Zone desc match same as insert_card_into_hand_list_by_zone_desc.
On match: dual array shift (write_word_from_deref_src + strh for both A and B).
Symmetric to insert_card_into_hand_list (zone_type=0xf path)."

PLATE  0x08037030  find_deck_slot_by_card_pair_match:
"Searches extra-deck array for a card_id passing check_card_pair_allowed(card_id, filter).
r0=player_id, r1=card_id_filter (->r6, low 16 bits).
Extra-deck count: gP1LifePoints + player*PLAYER_BLOCK_STRIDE + 0x14.
Array: gP1HandSlotArray + player*PLAYER_BLOCK_STRIDE (0x83*8=0x418 offset).
Backward scan from count-1 to 0; extracts card_id bits[12:0] from each word;
calls check_card_pair_allowed(card_id, filter); on hit returns index.
Returns -1 if no match (movs r0,#1; rsbs r0,r0,#0).
indeg>=7; callers: FUN_080bb4c2, duel_field at 0x080637a2/0x08063bd2/0x08066d74/0x0807ecbe/0x080833e0."

PLATE  0x08037088  find_graveyard_entry_by_ptr:
"Searches player graveyard array for an entry matching target_ptr; returns 1-based index.
r0=player_id [0..1], r1=target_ptr (->r7).
Graveyard base: gP1LifePoints + player*PLAYER_BLOCK_STRIDE + 0x83*8 (=0x418).
Count: gP1LifePoints + player*PLAYER_BLOCK_STRIDE + 0x14.
Forward scan; calls check_deref_words_equal each step; on match returns index+1 (1-based).
Returns 0 if not found. Read-only.
3 callers: 0x08044674, 0x08044714, 0x080448a0 (duel_field)."

PLATE  0x080370dc  count_extra_deck_cards_by_id:
"Counts extra-deck entries matching target card_id.
r0=player_id, r1=card_id filter (low 16 bits extracted to r6 via lsls/lsrs #0x10).
Extra-deck count: gP1LifePoints + player*PLAYER_BLOCK_STRIDE + 0x14.
Array: gP1LifePoints + player*PLAYER_BLOCK_STRIDE + 0x83*8 (=0x418).
For i=0..count-1: extract card_id bits[12:0]; compare with r6; hit -> r4++.
Returns r4 = total matching count. Non-APCS entry (r6 set from r1 at top).
indeg=0; referenced by runtime fn-ptr or dead code."
```

---

## 新建 constants 计划

### `card_info.inc` 追加 (3 新条)

```asm
@ file 03 Seg-2 additions
.equ GAP_CID_13EA,              0x000013ea  @ gap slot (not in card-stats.s; range [0x13E8..0x13EB]: Nuvia the Wicked/Soul Exchange); check_slot_card_eligible_for_special_action
.equ KUNAI_WITH_CHAIN_CID,      0x00001231  @ Kunai with Chain (pw=37390589); check_slot_card_eligible_for_special_action; note: Metalmorph=+7 computed inline
.equ BLAST_WITH_CHAIN_CID,      0x00001514  @ Blast with Chain (pw=98239899); check_slot_card_eligible_for_special_action; note: Hero_Heyro(0x1980)=0xcc<<5 inline
```

### `ewram.inc` 追加 (4 新条)

```asm
@ file 03 Seg-2 additions
.equ gEffectEntryArray,           0x0201b590  @ effect entry array base (stride=0x18, count at gDuelPhaseFlags+EFFECT_ENTRY_COUNT_OFF); 23 raw refs
.equ EFFECT_ENTRY_COUNT_OFF,      0x00000594  @ gDuelPhaseFlags+0x594 = effect entry count field; 9 raw refs
.equ HAND_ARRAY_TO_COUNT_NEG_OFF, 0xfffffbfc  @ gP1HandSlotArray+0xfffffbfc = gP1HandCountBase (delta=-0x404; maps hand slot array to hand count base); 5 raw refs
.equ ALT_HAND_ARRAY_TO_COUNT_NEG_OFF, 0xfffffa4c  @ gP1AltHandSlotArray+0xfffffa4c = gP1AltHandCountBase (delta=-0x5b4; maps alt-hand slot array to alt-hand count base); 3 raw refs
```

共新建 constants: card_info.inc +3, ewram.inc +4 (7 条总)。

---

## 符号化统计

| 类型 | 数量 |
|------|------|
| EQ_SLOTS (复用) | 29 |
| EQ_SLOTS (新建) | 8 |
| EQ_SLOTS 合计 | 37 |
| RENAME_SLOTS | 0 |
| FUNC_RENAME | 0 |
| PLATE_FULL | 13 |

**新建常量**: card_info.inc +3, ewram.inc +4 = 共 7 条

---

## §5.1 登记

无全 ROM 0-引用数据块 (本段无 ROM_INCBIN)。
