# Refine Proposal: F10-Seg-2  [0x0807ae84..0x0807be2c)

> file 10 Seg-2 -- 18 fn, 47 DAT_/DWORD_ auto-name slots + 4 PTR_gP1LifePoints_* named slots = 51 total pool labels.
> 8 ROM_INCBIN blocks -- all are THUMB code (fn_eligible stubs + dispatch sub-stub blocks).
> No prior coverage (new segment).

---

## 段测绘

### 函数入口 x18

| addr       | name                                               |
|------------|----------------------------------------------------|
| 0x0807ae84 | commit_serial_spell_effect_node                    |
| 0x0807aea0 | enqueue_slot_card_sprite_for_all_player_zone_slots |
| 0x0807aef4 | dispatch_equip_effect_by_type_field                |
| 0x0807af28 | test_zone13_slot_on_zone_entry_and_active_flag     |
| 0x0807b0c8 | update_zone_entry_sprite_by_descriptor             |
| 0x0807b188 | enqueue_slot_sprite_for_zone_entry_count_range     |
| 0x0807b240 | tick_equip_zone_pair_bitmap_display_seq            |
| 0x0807b418 | enqueue_slot_sprite_with_field5_score_on_zone_match|
| 0x0807b490 | enqueue_slot_card_sprite_for_all_zone_slots_mode5  |
| 0x0807b6b8 | tick_equip_prng_sample_or_lp_indicator             |
| 0x0807b77c | invoke_equip_oam_for_chain_zone_slot_if_placeable  |
| 0x0807b958 | dispatch_equip_lp_bar_or_chain_pair_sprite_by_type |
| 0x0807bb30 | dispatch_equip_sprite_for_all_zone_slots_by_player |
| 0x0807bb8c | test_zone13_slot_via_side_type_from_zone_entry     |
| 0x0807bbcc | tick_draw_counter_lp_display_seq                   |
| 0x0807bc48 | tick_equip_zone_target_select_display_seq__0807bc48|
| 0x0807bdb8 | tick_equip_zone_sprite_display_seq_by_eligibility  |
| 0x0807bdf8 | dispatch_equip_oam_or_type11_sprite_by_type        |

Note: Seg-3 starts at 0x0807be2c (tick_lp_sign_flag_display_seq). 18 fn in Seg-2.

### 残留自动名槽 x47

```
DAT_0807ae9c    = 0x0000183e   fn commit_serial_spell_effect_node literal pool
DWORD_0807b13c  = 0x0201bb90   fn update_zone_entry_sprite_by_descriptor pool
DWORD_0807b180  = 0x00000868   same fn pool
DWORD_0807b184  = 0x0201c600   same fn pool
DWORD_0807b1dc  = 0x00000868   fn enqueue_slot_sprite_for_zone_entry_count_range pool
DWORD_0807b1e0  = 0x0201c510   same fn pool
DWORD_0807b268  = 0x0201b290   fn tick_equip_zone_pair_bitmap_display_seq pool
DWORD_0807b328  = 0x080507ad   same fn pool (fn-ptr check_equip_slot_eligible_by_type_query+1)
DWORD_0807b32c  = 0x08051abd   same fn pool (fn-ptr check_equip_slot_eligible_by_side_and_setcode+1)
DWORD_0807b330  = 0x0201c4e0   same fn pool (gP1LifePoints, .word already symbolic; label rename only)
DWORD_0807b334  = 0x00000868   same fn pool
DWORD_0807b338  = 0x00001cf4   same fn pool (FIELD_STATE_OFF offset used as [gP1LP+0x1cf4])
DWORD_0807b33c  = 0x0000178b   same fn pool (PROTECTOR_OF_THE_SANCTUARY_CID)
DWORD_0807b340  = 0x0201e2a0   same fn pool (gDuelCardCtxBase)
DWORD_0807b380  = 0x00000103   same fn pool (EQUIP_ACT_SCORE_MODE_103)
DWORD_0807b3a4  = 0x0201c4e0   same fn pool (gP1LifePoints dup; .word symbolic; label rename)
DWORD_0807b3c4  = 0x0201c4e0   same fn pool (gP1LifePoints dup; .word symbolic; label rename)
DWORD_0807b3cc  = 0x080507ad   same fn pool (fn-ptr dup)
DWORD_0807b3e4  = 0x08051abd   same fn pool (fn-ptr dup)
DWORD_0807b48c  = 0x0201bb90   fn enqueue_slot_sprite_with_field5_score_on_zone_match pool
DWORD_0807b6d4  = 0x0201b290   fn tick_equip_prng_sample_or_lp_indicator pool
DWORD_0807b704  = 0x0201e2a0   same fn pool
DWORD_0807b708  = 0x0201c4e0   same fn pool (gP1LifePoints; .word symbolic; label rename)
DWORD_0807b734  = 0x0201c4e0   same fn pool (gP1LifePoints dup; .word symbolic; label rename)
DWORD_0807b75c  = 0x0201c4e0   same fn pool (gP1LifePoints dup; .word symbolic; label rename)
DWORD_0807b760  = 0x00001daa   same fn pool (LP_CARD_TRACK_NEXT_OFF)
DWORD_0807b7d4  = 0x00000868   fn invoke_equip_oam_for_chain_zone_slot_if_placeable pool
DWORD_0807b7d8  = 0x0201c880   same fn pool (gP1ChainZoneArray)
DAT_0807b878    = ROM_INCBIN base label (BLK6 disasm target block label)
DAT_0807ba30    = ROM_INCBIN base label (BLK8 disasm target block label)
DWORD_0807bb88  = 0x0201e1c8   fn dispatch_equip_sprite_for_all_zone_slots_by_player pool
DAT_0807bbe8    = 0x0201b290   fn tick_draw_counter_lp_display_seq pool
DAT_0807bc20    = 0x00000868   same fn pool
DAT_0807bc44    = 0x00001da8   same fn pool (LP_CARD_TRACK_BASE_OFF)
DAT_0807bc68    = 0x0201b290   fn tick_equip_zone_target_select_display_seq pool
DAT_0807bcdc    = 0x000004a4   same fn pool (EQUIP_PHASE_FRAME_OFF, [gDuelPhaseFlags+0x4a4] iteration slot)
DAT_0807bce0    = 0x00000868   same fn pool
DAT_0807bce4    = 0x0201c510   same fn pool
DAT_0807bd24    = 0x000004a4   same fn pool (EQUIP_PHASE_FRAME_OFF dup)
DAT_0807bd4c    = 0x0201e2a0   same fn pool
DAT_0807bd50    = 0x08065991   same fn pool (fn-ptr check_equip_activation_at_slot11+1)
DAT_0807bd68    = 0x08065991   same fn pool (fn-ptr dup)
DAT_0807bda4    = 0x00001d70   same fn pool (LP_BANISHER_CTX_OFF)
DAT_0807bda8    = 0x00000868   same fn pool
DAT_0807bddc    = 0x0201b290   fn tick_equip_zone_sprite_display_seq_by_eligibility pool
```

**Named pool slots (PTR_ prefix, already-symbolic .word but wrong label): x4**
```
PTR_gP1LifePoints_0807bc1c  = 0x0201c4e0  fn tick_draw_counter_lp_display_seq
PTR_gP1LifePoints_0807bc40  = 0x0201c4e0  same fn
PTR_gP1LifePoints_0807bd28  = 0x0201c4e0  fn tick_equip_zone_target_select_display_seq
PTR_gP1LifePoints_0807bda0  = 0x0201c4e0  same fn
```

### ROM_INCBIN blocks x8

| BLK | ROM_INCBIN addr/size | raw refs | THUMB+1 refs | verdict |
|-----|---------------------|----------|--------------|---------|
| 1   | 0x7af66/0x3a (58B)  | 0        | 1 (+0x002)   | R4 disasm (fn_eligible THUMB stub) |
| 2   | 0x7afb8/0x110 (272B)| 6 (table[0..5])           | 0 | R4 disasm (dispatch sub-stubs x6) |
| 3   | 0x7b4d4/0x2c (44B)  | 0        | 2 (base)     | R4 disasm (fn_eligible THUMB stub, shared) |
| 4   | 0x7b574/0x144 (324B)| 1 (base) + 6 sub-entries | 0 | R4 disasm (dispatch sub-stubs x7) |
| 5   | 0x7b7dc/0x28 (40B)  | 0        | 1 (base)     | R4 disasm (fn_eligible THUMB stub) |
| 6   | 0x7b878/0xe0 (224B) | 29 (table 29-entry)       | 0 | R4 disasm (dispatch sub-stubs x7) |
| 7   | 0x7b9f4/0x28 (40B)  | 0        | 1 (base)     | R4 disasm (fn_eligible THUMB stub) |
| 8   | 0x7ba30/0x100 (256B)| 1 (base) + 4 sub-entries | 0 | R4 disasm (dispatch sub-stubs x5) |

---

## データ块分类 (Rule 2/3) -- ref-scan 証拠

Python exhaustive 2-byte-step ref-scan on all 8 blocks; 4-byte-aligned count used for dispatch table ref classification.

| BLK | ref-scan (4B-aligned raw / THUMB+1) | 判定 | 理由 |
|-----|-------------------------------------|------|------|
| 0x7af66/0x3a  | raw=0, THUMB+1=1 at +0x002 | R4 disasm | fn_eligible stub CID=0x1847 (Lighten the Load); THUMB+1=0x807af69 ref at ROM FS 0x09e46fe8; CID at 0x09e46fe4=0x1847; push{r4..r7,lr} at +0x2 confirms THUMB code |
| 0x7afb8/0x110 | raw=6 (table[0..5] at 0x7afa0..0x7afb4) | R4 disasm | 6-entry dispatch pointer table at 0x7afa0..0x7afb4 (already rendered as .word in asm) points into this block; 6 unique sub-stubs at +0x0/+0x38/+0x50/+0x74/+0xa0/+0xe0; each table entry raw=1; 6 sub-stubs confirmed (no separate base+default split) |
| 0x7b4d4/0x2c  | raw=0, THUMB+1=2 at base | R4 disasm | fn_eligible stub shared by 2 CIDs: 0x19a7 (Hero Kid) at ROM FS 0x09e45428 and 0x1867 (Hyena) at ROM FS 0x09e46028; stub ptr = 0x0807b4d5; push{r4,r5,r6,lr}+sub_sp at +0x0 |
| 0x7b574/0x144 | raw=1 (base) + 6 sub-entries raw=1 each (+0x138 raw=23) | R4 disasm | 29-entry dispatch pointer table at 0x7b500..0x7b570 (already in asm as .word) points into this block; unique targets: 7 sub-stubs; default at +0x138=0x7b6ac (raw=23 = 29-6=23 pointing to default); sub-stubs at +0x0/+0x5c/+0xbc/+0x10c/+0x11c/+0x12e confirmed raw=1 each |
| 0x7b7dc/0x28  | raw=0, THUMB+1=1 at base | R4 disasm | fn_eligible stub CID=0x1876 (Rescue Cat); THUMB+1=0x807b7dd ref at ROM FS 0x09e470f0; CID at 0x09e470ec=0x1876; literal pool confirms gDuelPhaseFlags+BLK6_table |
| 0x7b878/0xe0  | raw=1 (base) + 6 sub-entries raw=1 each (+0xd6 raw=23) | R4 disasm | 29-entry dispatch pointer table at 0x7b804..0x7b874 (already in asm as .word) points into this block; unique targets: 7 sub-stubs; default at +0xd6=0x7b94e (raw=23); sub-stubs at +0x0/+0x54/+0x68/+0x84/+0xba/+0xcc confirmed raw=1 each |
| 0x7b9f4/0x28  | raw=0, THUMB+1=1 at base | R4 disasm | fn_eligible stub CID=0x1878 (Gatling Dragon); THUMB+1=0x807b9f5 ref at ROM FS 0x09e47108; CID at 0x09e47104=0x1878; literal pool: gDuelPhaseFlags + BLK8_table=0x807ba1c |
| 0x7ba30/0x100 | raw=1 (base) + 4 sub-entries raw=1 each | R4 disasm | 5-entry dispatch pointer table at 0x7ba1c..0x7ba30 (already in asm as .word) points into this block; unique targets: 5 sub-stubs at +0x0/+0x16/+0x54/+0xa0/+0xf4 each raw=1 |

**Zero-ref blocks: none.** All 8 blocks have refs (THUMB+1 or raw). No §5.1 entries.

---

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate; 全部 REUSE; 按值 grep 证据)

| slot | value | const_name | file | slot_label |
|------|-------|-----------|------|------------|
| DAT_0807ae9c | 0x0000183e | SERIAL_SPELL_CID | card_info.inc L(grep hit confirmed) | commit_serial_spell_serial_cid |
| DWORD_0807b13c | 0x0201bb90 | gEquipChainSlotRefs | ewram.inc | update_zone_entry_chain_refs_base |
| DWORD_0807b180 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | update_zone_entry_player_stride |
| DWORD_0807b184 | 0x0201c600 | gP1FieldArrayCBase | ewram.inc | update_zone_entry_field_array_c_base |
| DWORD_0807b1dc | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | enqueue_slot_sprite_zone_entry_player_stride |
| DWORD_0807b1e0 | 0x0201c510 | gDuelFieldSlots | ewram.inc | enqueue_slot_sprite_zone_entry_slots_base |
| DWORD_0807b268 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | tick_equip_zone_pair_bitmap_phase_flags |
| DWORD_0807b334 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | tick_equip_zone_pair_bitmap_player_stride |
| DWORD_0807b338 | 0x00001cf4 | FIELD_STATE_OFF | duel_field.inc | tick_equip_zone_pair_bitmap_field_state_off |
| DWORD_0807b33c | 0x0000178b | PROTECTOR_OF_THE_SANCTUARY_CID | card_info.inc | tick_equip_zone_pair_bitmap_protector_cid |
| DWORD_0807b340 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc | tick_equip_zone_pair_bitmap_ctx_base |
| DWORD_0807b380 | 0x00000103 | EQUIP_ACT_SCORE_MODE_103 | duel_field.inc | tick_equip_zone_pair_bitmap_score_op_103 |
| DWORD_0807b48c | 0x0201bb90 | gEquipChainSlotRefs | ewram.inc | enqueue_slot_sprite_field5_chain_refs |
| DWORD_0807b6d4 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | tick_equip_prng_phase_flags |
| DWORD_0807b704 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc | tick_equip_prng_ctx_base |
| DWORD_0807b760 | 0x00001daa | LP_CARD_TRACK_NEXT_OFF | ewram.inc | tick_equip_prng_lp_track_next_off |
| DWORD_0807b7d4 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | invoke_equip_oam_chain_player_stride |
| DWORD_0807b7d8 | 0x0201c880 | gP1ChainZoneArray | ewram.inc | invoke_equip_oam_chain_zone_base |
| DWORD_0807bb88 | 0x0201e1c8 | gEquipZoneCountTable | ewram.inc | dispatch_equip_sprite_all_zones_count_table |
| DAT_0807bbe8 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | tick_draw_counter_lp_phase_flags |
| DAT_0807bc20 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | tick_draw_counter_lp_player_stride |
| DAT_0807bc44 | 0x00001da8 | LP_CARD_TRACK_BASE_OFF | ewram.inc | tick_draw_counter_lp_card_track_off |
| DAT_0807bc68 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | tick_equip_zone_target_select_phase_flags |
| DAT_0807bcdc | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc | tick_equip_zone_target_select_iter_slot_off |
| DAT_0807bce0 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | tick_equip_zone_target_select_player_stride |
| DAT_0807bce4 | 0x0201c510 | gDuelFieldSlots | ewram.inc | tick_equip_zone_target_select_slots_base |
| DAT_0807bd24 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc | tick_equip_zone_target_select_iter_slot_off_b |
| DAT_0807bd4c | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc | tick_equip_zone_target_select_ctx_base |
| DAT_0807bda4 | 0x00001d70 | LP_BANISHER_CTX_OFF | ewram.inc | tick_equip_zone_target_select_banisher_ctx_off |
| DAT_0807bda8 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | tick_equip_zone_target_select_player_stride_b |
| DAT_0807bddc | 0x0201b290 | gDuelPhaseFlags | ewram.inc | tick_equip_zone_sprite_eligib_phase_flags |

EQ count: 31 slots (all REUSE; grep-by-value confirmed against existing constants).

Note: C5 dedup -- all duplicate values (PLAYER_BLOCK_STRIDE x9, gDuelPhaseFlags x5, gP1LifePoints x8, gDuelCardCtxBase x3, EQUIP_PHASE_FRAME_OFF x2, fn-ptrs x2+x2) each get independent pool labels (distinct functions, same constant).

### REF_SLOTS (USER-label + DATA-ref)

These slots contain ROM function pointers (THUMB+1 form). They receive named pool labels pointing to the target function.

| slot | value | fn name | slot_label |
|------|-------|---------|------------|
| DWORD_0807b328 | 0x080507ad | check_equip_slot_eligible_by_type_query+1 | tick_equip_zone_pair_bitmap_zone_pred_fn_a |
| DWORD_0807b32c | 0x08051abd | check_equip_slot_eligible_by_side_and_setcode+1 | tick_equip_zone_pair_bitmap_zone_pred_fn_b |
| DWORD_0807b3cc | 0x080507ad | check_equip_slot_eligible_by_type_query+1 | tick_equip_zone_pair_bitmap_zone_pred_fn_a_b |
| DWORD_0807b3e4 | 0x08051abd | check_equip_slot_eligible_by_side_and_setcode+1 | tick_equip_zone_pair_bitmap_zone_pred_fn_b_b |
| DAT_0807bd50 | 0x08065991 | check_equip_activation_at_slot11+1 | tick_equip_zone_target_select_activation_fn |
| DAT_0807bd68 | 0x08065991 | check_equip_activation_at_slot11+1 | tick_equip_zone_target_select_activation_fn_b |

Target function addresses: check_equip_slot_eligible_by_type_query at 0x080507ac (asm/05 L16635 confirmed); check_equip_slot_eligible_by_side_and_setcode at 0x08051abc (asm/05 L19585 confirmed); check_equip_activation_at_slot11 at 0x08065990 (asm/08 L3334 confirmed).

.word syntax: `.word  check_equip_slot_eligible_by_type_query+1`  (GAS THUMB+1 = even_addr + 1)

REF count: 6 slots.

### RENAME_SLOTS (auto-name label rename + EOL)

All remaining DAT_/DWORD_ slots after EQ + REF processing:

| slot | value | slot_label | EOL note |
|------|-------|-----------|----------|
| DWORD_0807b330 | 0x0201c4e0 | tick_equip_zone_pair_bitmap_lp_base | .word already gP1LifePoints |
| DWORD_0807b3a4 | 0x0201c4e0 | tick_equip_zone_pair_bitmap_lp_base_b | .word already gP1LifePoints |
| DWORD_0807b3c4 | 0x0201c4e0 | tick_equip_zone_pair_bitmap_lp_base_c | .word already gP1LifePoints |
| DWORD_0807b708 | 0x0201c4e0 | tick_equip_prng_lp_base | .word already gP1LifePoints |
| DWORD_0807b734 | 0x0201c4e0 | tick_equip_prng_lp_base_b | .word already gP1LifePoints |
| DWORD_0807b75c | 0x0201c4e0 | tick_equip_prng_lp_base_c | .word already gP1LifePoints |
| DAT_0807b878 | ROM_INCBIN | equip_sprite_dispatch_stubs_b878 | BLK6 block label after disasm |
| DAT_0807ba30 | ROM_INCBIN | equip_sprite_dispatch_stubs_ba30 | BLK8 block label after disasm |
| DAT_0807afb8 | ROM_INCBIN | lighten_the_load_dispatch_stubs | BLK2 block label after disasm |
| DAT_0807b574 | ROM_INCBIN | hero_kid_hyena_dispatch_stubs | BLK4 block label after disasm |

**Note**: DAT_0807afb8 and DAT_0807b574 appear in the asm text as base labels for ROM_INCBIN; after disasm they become the first sub-stub label.

RENAME_SLOTS for the 4 PTR_gP1LifePoints_ labels:

| slot | slot_label |
|------|-----------|
| PTR_gP1LifePoints_0807bc1c | tick_draw_counter_lp_lp_base |
| PTR_gP1LifePoints_0807bc40 | tick_draw_counter_lp_lp_base_b |
| PTR_gP1LifePoints_0807bd28 | tick_equip_zone_target_select_lp_base |
| PTR_gP1LifePoints_0807bda0 | tick_equip_zone_target_select_lp_base_b |

RENAME count: 14 total (10 DAT_/DWORD_ + 4 PTR_).

### FUNC_RENAME (誤名訂正)

| addr       | old name                                            | new name                                   | reason |
|------------|-----------------------------------------------------|--------------------------------------------|--------|
| 0x0807bc48 | tick_equip_zone_target_select_display_seq__0807bc48 | tick_equip_zone_target_select_display_seq | Trailing __ADDR suffix is naming-phase auto-deconflict residue; indeg=0 (CALLEE-COLUMN GREP: 0 hits, asm/10 L3442); the function is the only one with this name, suffix not needed; plate comment correct already |

---

## disasm 計画 (R4)

All 8 ROM_INCBIN blocks require R4 disasm. They follow the same "fn_eligible + dispatch sub-stub" pattern as file 10 Seg-1.

**Pattern reference**: Seg-1 BLK1/3/5/7 = fn_eligible THUMB stubs; Seg-1 BLK2/4/6/8 = dispatch sub-stub blocks. Same structure here.

### BLK1: fn_eligible Lighten the Load  [0x0807af66, 0x0807afa0)

- THUMB+1=1 ref from FS handler table at ROM FS 0x09e46fe8 (fn_eligible ptr = 0x0807af69)
- CID=0x1847 (Lighten the Load, card-stats.s L22621 slot=0x1847 confirmed)
- Structure: 2B padding (0x0000) at +0x0 then THUMB stub at +0x2 = 0x0807af68
- push {r4,r5,r6,r7,lr} at 0x0807af68 (halfword 0xb5f0)
- Literal pool within stub: gDuelPhaseFlags at +0x32 (0x7af98 = 0x0201b290) + dispatch table ptr at +0x36 (0x7af9c = 0x0807afa0)
- The dispatch table itself is at 0x7afa0..0x7afb4 (already rendered as .word in asm, NOT part of BLK1 incbin)
- Ghidra createFunction: 0x0807af68 named fn_eligible_lighten_the_load (CID=0x1847)
- createDWord force-split: 0x0807af98 (gDuelPhaseFlags literal), 0x0807af9c (dispatch table ptr)
- 2B padding at 0x0807af66 -> setBytes 0x0000 + .hword 0x0000 label

**fn_eligible function entry**: 0x0807af68 -> fn_eligible_lighten_the_load

### BLK2: Lighten the Load dispatch sub-stubs  [0x0807afb8, 0x0807b0c8)

- raw=6 (6-entry table at 0x7afa0..0x7afb4); 6 unique sub-stubs
- dispatch table at 0x7afa0 has 6 entries, each pointing to a unique sub-stub
- Sub-stub entry points (all raw-ref'd from table):
  - 0x0807afb8 (table[0]): lighten_the_load_dispatch_default
  - 0x0807aff0: lighten_the_load_dispatch_zone_check
  - 0x0807b02c: lighten_the_load_dispatch_state_write
  - 0x0807b058: lighten_the_load_dispatch_slot_lookup
  - 0x0807b098: lighten_the_load_dispatch_slot_sprite
  - 0x0807b0ac: lighten_the_load_dispatch_player_extract
- Note: 0x0807b008 (ref-scan hit at 2B step) is literal pool data, NOT a code entry (4B-aligned scan = 0 refs, confirmed false positive from unaligned match at 0x806e3)
- Literal pools within stubs at:
  - 0x0807afb8+0x38 area: 0x7afec (gP1LifePoints=0x0201c4e0), 0x7aff0 is next stub not pool
  - Multiple ldr [pc,#N] within each sub-stub -> createDWord for each
- clearListing 0x0807afb8..0x0807b0c7 -> setTMode -> DisassembleCommand per stub

### BLK3: fn_eligible Hero Kid + Hyena  [0x0807b4d4, 0x0807b500)

- THUMB+1=2 refs: CID=0x19a7 (Hero Kid, card-stats.s L26222) at ROM FS 0x09e45424; CID=0x1867 (Hyena, L22998) at ROM FS 0x09e46024
- Single shared stub at 0x0807b4d4 (push {r4,r5,r6,lr} at +0x0)
- Literal pool: gDuelPhaseFlags at +0x24 (0x7b4f8=0x0201b290), dispatch table ptr at +0x28 (0x7b4fc=0x0807b500)
- Ghidra createFunction: 0x0807b4d4 named fn_eligible_hero_kid_hyena (shared stub; note in plate that CIDs 0x19a7+0x1867 both route here)
- createDWord: 0x0807b4f8 (gDuelPhaseFlags), 0x0807b4fc (dispatch table ptr)
- Note: 0x0807b4f4 = 0x4687 = THUMB MOV PC,r0 (indirect jump, code not data); consumed by DisassembleCommand. 0x0807b4f6 = 0x0000 = alignment pad, auto-consumed with the preceding code halfword. DO NOT createDWord at 0x0807b4f4.

**fn_eligible function entry**: 0x0807b4d4 -> fn_eligible_hero_kid_hyena

### BLK4: Hero Kid/Hyena dispatch sub-stubs  [0x0807b574, 0x0807b6b8)

- raw=1 at base + 6 additional raw=1 refs + default at +0x138 raw=23
- 29-entry dispatch table at 0x7b500..0x7b570 (already in asm as .word)
- 7 unique sub-stubs (6 specialized + 1 default):
  - 0x0807b574 (base, 1 ref from table[28]): hero_kid_hyena_dispatch_base
  - 0x0807b5d0 (+0x5c, 1 ref from table[27]): hero_kid_hyena_dispatch_5d0
  - 0x0807b630 (+0xbc, 1 ref from table[26]): hero_kid_hyena_dispatch_630
  - 0x0807b680 (+0x10c, 1 ref from table[25]): hero_kid_hyena_dispatch_680
  - 0x0807b690 (+0x11c, 1 ref from table[20]): hero_kid_hyena_dispatch_690
  - 0x0807b6a2 (+0x12e, 1 ref from table[0] at 0x0807b500): hero_kid_hyena_dispatch_6a2
  - 0x0807b6ac (+0x138, 23 refs = default for 23 of 29 table entries): hero_kid_hyena_dispatch_default
- Literal pools within stubs contain gP1LifePoints, gDuelPhaseFlags, gDuelCardCtxBase -> createDWord each
- clearListing 0x0807b574..0x0807b6b7 -> setTMode -> DisassembleCommand per stub

### BLK5: fn_eligible Rescue Cat  [0x0807b7dc, 0x0807b804)

- THUMB+1=1 ref: CID=0x1876 (Rescue Cat, card-stats.s L23193) at ROM FS 0x09e470ec; fn_eligible ptr=0x0807b7dd
- Stub starts push {r4,r5,lr} at +0x0 (halfword 0xb530)
- Literal pool: gDuelPhaseFlags at +0x20 (0x7b7fc=0x0201b290), dispatch table ptr at +0x24 (0x7b800=0x0807b804)
- Note: literal pool at 0x0807b800 (.word dispatch_table_ptr=0x0807b804); createDWord mandatory to prevent code re-analysis; actual raw refs=0 (no other ROM address stores 0x0807b800)
- Ghidra createFunction: 0x0807b7dc named fn_eligible_rescue_cat (CID=0x1876)
- createDWord: 0x0807b7fc (gDuelPhaseFlags), 0x0807b800 (dispatch table ptr)

**fn_eligible function entry**: 0x0807b7dc -> fn_eligible_rescue_cat

### BLK6: Rescue Cat dispatch sub-stubs  [0x0807b878, 0x0807b958)

- raw=1 at base + 6 additional raw=1 refs + default at +0xd6 raw=23
- 29-entry dispatch table at 0x7b804..0x7b874 (already in asm as .word)
- 7 unique sub-stubs:
  - 0x0807b878 (+0x000, 1 ref): rescue_cat_dispatch_base
  - 0x0807b8cc (+0x054, 1 ref): rescue_cat_dispatch_8cc
  - 0x0807b8e0 (+0x068, 1 ref from table[25]): rescue_cat_dispatch_8e0
  - 0x0807b8fc (+0x084, 1 ref): rescue_cat_dispatch_8fc
  - 0x0807b932 (+0x0ba, 1 ref): rescue_cat_dispatch_932
  - 0x0807b944 (+0x0cc, 1 ref): rescue_cat_dispatch_944
  - 0x0807b94e (+0x0d6, 23 refs): rescue_cat_dispatch_default
- Note: 0x0807b8e0 raw=1 (only table[25] at 0x0807b868 points to it; independent ref-scan confirmed)
- Literal pools within stubs -> createDWord each
- clearListing 0x0807b878..0x0807b957 -> setTMode -> DisassembleCommand per stub

### BLK7: fn_eligible Gatling Dragon  [0x0807b9f4, 0x0807ba1c)

- THUMB+1=1 ref: CID=0x1878 (Gatling Dragon, card-stats.s verified) at ROM FS 0x09e47104; fn_eligible ptr=0x0807b9f5
- Stub starts push {r4,r5,lr} at +0x0 (halfword 0xb530)
- Literal pool: gDuelPhaseFlags at +0x20 (0x7ba14=0x0201b290), dispatch table ptr at +0x24 (0x7ba18=0x0807ba1c)
- Ghidra createFunction: 0x0807b9f4 named fn_eligible_gatling_dragon (CID=0x1878)
- createDWord: 0x0807ba14 (gDuelPhaseFlags), 0x0807ba18 (dispatch table ptr)

**fn_eligible function entry**: 0x0807b9f4 -> fn_eligible_gatling_dragon

### BLK8: Gatling Dragon dispatch sub-stubs  [0x0807ba30, 0x0807bb30)

- raw=1 at base + 4 additional raw=1 refs (5-entry dispatch table at 0x7ba1c..0x7ba30)
- Table (already in asm as .word): 5 entries -> 5 sub-stubs, all unique (no default needed):
  - 0x0807ba30 (+0x000, 1 ref from table[4]): gatling_dragon_dispatch_ba30
  - 0x0807ba46 (+0x016, 1 ref from table[3]): gatling_dragon_dispatch_ba46
  - 0x0807ba84 (+0x054, 1 ref from table[2]): gatling_dragon_dispatch_ba84
  - 0x0807bad0 (+0x0a0, 1 ref from table[1]): gatling_dragon_dispatch_bad0
  - 0x0807bb24 (+0x0f4, 1 ref from table[0]): gatling_dragon_dispatch_bb24
- Literal pools within stubs contain gP1LifePoints (0x0201c4e0), gDuelFieldSlots (0x0201c510), PLAYER_BLOCK_STRIDE (0x868), LP_BANISHER_CTX_OFF (0x1d70), gEquipZoneCountTable (0x0201e1c8) -> createDWord each
- clearListing 0x0807ba30..0x0807bb2f -> setTMode -> DisassembleCommand per stub

### R4 zero-residue proof

After disasm:
- BLK1: 2B padding + fn_eligible stub (0x38 bytes THUMB) + 2 literal pool dwords -> 0 incbin residue
- BLK2: 6 sub-stubs (0x110 bytes THUMB) + literal pools -> 0 incbin residue
- BLK3: fn_eligible stub (0x2c bytes THUMB) + MOV PC,r0 (0x4687) + pad consumed by disasm + 2 literal pool dwords (0x7b4f8, 0x7b4fc) -> 0 incbin residue
- BLK4: 7 sub-stubs (0x144 bytes THUMB) + literal pools -> 0 incbin residue
- BLK5: fn_eligible stub (0x28 bytes THUMB) + literal pools -> 0 incbin residue
- BLK6: 7 sub-stubs (0xe0 bytes THUMB) + literal pools -> 0 incbin residue
- BLK7: fn_eligible stub (0x28 bytes THUMB) + literal pools -> 0 incbin residue
- BLK8: 5 sub-stubs (0x100 bytes THUMB) + literal pools -> 0 incbin residue

Key: literal pool createDWord mandatory for every ldr [pc,#N] target in each stub. The Seg-1 BLK5 trap (0x4687 = MOV PC,r0 mistaken for data) DOES apply to BLK3: 0x0807b4f4 = 0x4687 = MOV PC,r0 (code, consumed by DisassembleCommand); 0x0807b4f6 = 0x0000 = alignment pad; literal pool starts at 0x0807b4f8. BLK2 also contains 0x4687 at 0x0807af96 (within code range) -- both are THUMB indirect jumps, NOT pool data.

---

## fn_eligible function-naming list (for fixer createFunction)

| ROM addr (even) | THUMB+1 fn-ptr | name | CID | card name |
|-----------------|----------------|------|-----|-----------|
| 0x0807af68 | 0x0807af69 | fn_eligible_lighten_the_load | 0x1847 | Lighten the Load |
| 0x0807b4d4 | 0x0807b4d5 | fn_eligible_hero_kid_hyena | 0x19a7/0x1867 | Hero Kid / Hyena (shared stub) |
| 0x0807b7dc | 0x0807b7dd | fn_eligible_rescue_cat | 0x1876 | Rescue Cat |
| 0x0807b9f4 | 0x0807b9f5 | fn_eligible_gatling_dragon | 0x1878 | Gatling Dragon |

Note: BLK3 shares one THUMB stub for two CIDs (0x19a7 Hero Kid + 0x1867 Hyena). Both FS handler table entries point to 0x0807b4d5. Create one function at 0x0807b4d4 with plate noting both CIDs.

Plate text (ASCII only): "Shared fn_eligible stub for Hero Kid (CID=0x19a7) and Hyena (CID=0x1867). Both FS handler table entries at ROM FS 0x09e45428 and 0x09e46028 route here. Dispatch table: 0x0807b500 (29 entries)."

---

## carve 計画 (R7)

None. All ROM_INCBIN blocks are code (THUMB), not data. No carve into rom.s needed.

---

## §5.1 登記 (Rule 3) -- 0 引用块

None. All 8 ROM_INCBIN blocks have refs (THUMB+1 or raw). §5.1 table remains empty for this segment.

---

## 新増 constants / 全局

None. Every value in every slot maps to an existing constant in constants/*.inc (all REUSE, grep-by-value confirmed).

Verified: SERIAL_SPELL_CID (0x183e), PLAYER_BLOCK_STRIDE (0x868), gEquipChainSlotRefs (0x0201bb90), gP1FieldArrayCBase (0x0201c600), gDuelFieldSlots (0x0201c510), gDuelPhaseFlags (0x0201b290), gP1LifePoints (0x0201c4e0), FIELD_STATE_OFF (0x1cf4), PROTECTOR_OF_THE_SANCTUARY_CID (0x178b), gDuelCardCtxBase (0x0201e2a0), EQUIP_ACT_SCORE_MODE_103 (0x103), EQUIP_PHASE_FRAME_OFF (0x4a4), gP1ChainZoneArray (0x0201c880), gEquipZoneCountTable (0x0201e1c8), LP_CARD_TRACK_NEXT_OFF (0x1daa), LP_CARD_TRACK_BASE_OFF (0x1da8), LP_BANISHER_CTX_OFF (0x1d70).

---

## C5 去重証拠 (grep BY VALUE)

All equates are REUSE (grep-by-value confirms existing .equ in constants/*.inc):

| value | existing const | file |
|-------|---------------|------|
| 0x0000183e | SERIAL_SPELL_CID | card_info.inc (confirmed) |
| 0x0201bb90 | gEquipChainSlotRefs | ewram.inc (confirmed) |
| 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc (confirmed) |
| 0x0201c600 | gP1FieldArrayCBase | ewram.inc (confirmed) |
| 0x0201c510 | gDuelFieldSlots | ewram.inc (confirmed) |
| 0x0201b290 | gDuelPhaseFlags | ewram.inc (confirmed) |
| 0x00001cf4 | FIELD_STATE_OFF | duel_field.inc (confirmed) |
| 0x0000178b | PROTECTOR_OF_THE_SANCTUARY_CID | card_info.inc (confirmed) |
| 0x0201e2a0 | gDuelCardCtxBase | ewram.inc (confirmed) |
| 0x00000103 | EQUIP_ACT_SCORE_MODE_103 | duel_field.inc (confirmed) |
| 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc (confirmed) |
| 0x0201c880 | gP1ChainZoneArray | ewram.inc (confirmed) |
| 0x0201e1c8 | gEquipZoneCountTable | ewram.inc (confirmed) |
| 0x00001daa | LP_CARD_TRACK_NEXT_OFF | ewram.inc (confirmed) |
| 0x00001da8 | LP_CARD_TRACK_BASE_OFF | ewram.inc (confirmed) |
| 0x00001d70 | LP_BANISHER_CTX_OFF | ewram.inc (confirmed) |

No NEW .equ creation needed.

---

## C8 stale FUN_ scan

Python grep for FUN_[0-9a-f]{8} in Seg-2 asm range: 0 hits. No stale FUN_ refs.
No plate/EOL FUN_ text present (all plates use current semantic names).

---

## C13 残留 100% 覆蓋証明

Total residual slots in [0x0807ae84, 0x0807be2c):

- Auto-name DAT_/DWORD_ labels: 47
- Named PTR_gP1LifePoints_* labels: 4
- Total: 51

Plan coverage:
- EQ_SLOTS: 31 (DAT_/DWORD_ with equate values)
- REF_SLOTS: 6 (fn-ptr ROM addr slots)
- RENAME_SLOTS: 14 (10 gP1LifePoints dups + 4 PTR_gP1LifePoints_ labels)
- Total covered: 31 + 6 + 14 = 51

Union == 51 == total. Coverage = 100%.

ROM_INCBIN labels (DAT_0807afb8, DAT_0807b574, DAT_0807b878, DAT_0807ba30) are included in the 47 DAT_ count and are handled by R4 disasm (they become the first sub-stub label after disasm).

Post-landing verification: python grep for `DAT_\|DWORD_\|PTR_DAT_` in asm/10 range [0x7ae84, 0x7be2c) should return 0 matches.

---

## 消費者証拠 (R6) -- キー槽語義

1. SERIAL_SPELL_CID (0x183e): commit_serial_spell_effect_node body writes 0x183e to [r4+0] after applying LP delta. asm/10 L2248 `.word 0x0000183e`. card_info.inc confirms. conf: high.

2. gP1ChainZoneArray (0x0201c880): invoke_equip_oam_for_chain_zone_slot_if_placeable computes EWRAM 0x0201c880 + player*0x868 + slot*4. asm/10 L3133 DWORD_0807b7d8=0x0201c880. ewram.inc entry confirms gP1ChainZoneArray. conf: high.

3. gEquipZoneCountTable (0x0201e1c8): dispatch_equip_sprite_for_all_zone_slots_by_player loads DWORD_0807bb88=[base] then [base+0] as player loop index. ewram.inc entry 0x0201e1c8=gEquipZoneCountTable. conf: high.

4. LP_BANISHER_CTX_OFF (0x1d70): tick_equip_zone_target_select_display_seq state 0x7c path: gP1LifePoints + LP_BANISHER_CTX_OFF offset to read slot index then invoke_setup_equip_oam_with_attr2. asm/10 L3623 DAT_0807bda4=0x00001d70. ewram.inc confirms LP_BANISHER_CTX_OFF=0x1d70. conf: high.

5. EQUIP_PHASE_FRAME_OFF (0x4a4): tick_equip_zone_pair_bitmap_display_seq and tick_equip_zone_target_select_display_seq both read [gDuelPhaseFlags+0x4a4] as iteration slot (str r3,[r0]). ewram.inc EQUIP_PHASE_FRAME_OFF=0x4a4. conf: high.

6. fn-ptrs 0x080507ad / 0x08051abd: tick_equip_zone_pair_bitmap_display_seq calls invoke_count_zone_pair_hits_full_range(node, r1) twice, passing these two values as r1. asm/07 comments and asm/05 function names confirm these are check_equip_slot_eligible_by_type_query+1 and check_equip_slot_eligible_by_side_and_setcode+1. conf: high.

7. FUNC_RENAME tick_equip_zone_target_select_display_seq__0807bc48: indeg=0 (CALLEE-COLUMN GREP asm/10 L3442). Double-underscore is auto-deconflict; no other function has this name; safe to drop suffix. conf: high.

---

## 求助

None. All blocks are classified with high confidence. fn_eligible CIDs verified against card-stats.s. All equate values have existing constants. No BLOCKED items.

---

## Executor Report: F10-Seg-2

- 槽: EQ=31 REF=6 RENAME=14 FUNC_RENAME=1 PLATE=1 (fn_eligible_hero_kid_hyena shared-stub plate)
- disasm=8 blocks (BLK1..8, all THUMB: 4 fn_eligible stubs + 4 dispatch sub-stub blocks)
- fn_eligible function entries: 4 (fn_eligible_lighten_the_load / fn_eligible_hero_kid_hyena / fn_eligible_rescue_cat / fn_eligible_gatling_dragon)
- carve=0, §5.1=0
- 新増 constants/全局: none (all REUSE)
- 求助: none
- proposal: doc/dev/refine/F10-Seg-2.proposal.md
