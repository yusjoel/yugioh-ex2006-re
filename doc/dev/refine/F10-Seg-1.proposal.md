# Refine Proposal: F10-Seg-1  [0x08079e60..0x0807ae84)

> file 10 Seg-1 -- 20 fn, 61 auto-name slots, 8 ROM_INCBIN blocks.
> No prior coverage (new file).

---

## 段测绘

### 函数入口 x20

| addr | name |
|------|------|
| 0x08079e60 | enqueue_neo_daedalus_zone_oam_on_available_slot |
| 0x08079ec4 | apply_partner_flags_on_equip_pair_slot_count_hit |
| 0x08079f5c | dispatch_equip_sprite_by_zone_type_or_draw_counter |
| 0x08079f80 | dispatch_equip_sprite_by_zone_or_chain_bitmap |
| 0x0807a0f4 | enqueue_equip_sprite_and_red_eyes_lp_indicator |
| 0x0807a2c4 | enqueue_sprite_attr_for_effect_zone_hit |
| 0x0807a308 | dispatch_face_down_and_lp_counter_sprite_by_state |
| 0x0807a580 | submit_equip_lp_bar_with_slot_sprite |
| 0x0807a5a4 | dispatch_neo_daedalus_equip_sprite_by_monster_count |
| 0x0807a65c | dispatch_equip_sprite_by_zone_or_capacity_guard |
| 0x0807a814 | enqueue_slot_sprite_on_zone_count_and_state_code |
| 0x0807a8f0 | tick_hand_effect_node_match_display_seq |
| 0x0807a9c8 | dispatch_equip_banisher_activation_by_state |
| 0x0807aa98 | dispatch_equip_prng_lp_row_and_bitmap_by_state |
| 0x0807ab6c | dispatch_banisher_lp_penalty_by_field_count |
| 0x0807ac1c | enqueue_equip_slot_bitmap_update_by_count |
| 0x0807ac84 | enqueue_equip_sprite_on_zone_count_match |
| 0x0807ad14 | tick_paired_slot_counter_update |
| 0x0807ad84 | tick_equip_zone_match_lp_row_type11 |
| 0x0807ae84 | commit_serial_spell_effect_node |

Note: the roadmap listed 19 fn + Seg boundary at 0x0807ae84; commit_serial_spell_effect_node
starts exactly at 0x0807ae84 which is the segment END address, so it belongs to Seg-2.
Seg-1 has 19 functions; the 20th label detected (commit_serial_spell_effect_node) is outside range.

Corrected: 19 fn in [0x08079e60, 0x0807ae84).

### 残留自动名槽 x61

```
DWORD_08079ebc  = 0x00000868               fn enqueue_neo_daedalus_zone_oam_on_available_slot
DWORD_08079ec0  = 0x0201c600               same fn
DWORD_08079f44  = 0x00000868               fn apply_partner_flags_on_equip_pair_slot_count_hit
DWORD_08079f48  = 0x0201c510               same fn
DAT_0807a00c    = ROM_INCBIN base label    BLK2 dispatch-stub block entry
DWORD_0807a134  = 0x00000ff8               fn enqueue_equip_sprite_and_red_eyes_lp_indicator
DAT_0807a178    = ROM_INCBIN base label    BLK4 dispatch-stub block entry
DWORD_0807a32c  = 0x0201b290               fn dispatch_face_down_and_lp_counter_sprite_by_state
DWORD_0807a380  = gP1LifePoints (symbolic) same fn -- already symbolic, rename only
DWORD_0807a384  = 0x00000868               same fn
DAT_0807a464    = ROM_INCBIN base label    BLK6 dispatch-stub block entry
DWORD_0807a5d4  = 0x0201b290               fn dispatch_neo_daedalus_equip_sprite_by_monster_count
DWORD_0807a608  = 0x000004a4               same fn
DWORD_0807a640  = 0x000004a4               same fn (duplicate in state-0x7f branch)
DWORD_0807a644  = 0x0000180d               same fn (OAM sprite attr base)
PTR_DAT_0807a6d0 = dispatch-table label   equip_sprite zone-capacity jump table
DAT_0807a71c    = ROM_INCBIN base label    BLK8 dispatch-stub block entry
DWORD_0807a8e8  = 0x00000868               fn enqueue_slot_sprite_on_zone_count_and_state_code
DWORD_0807a8ec  = 0x0201c510               same fn
DWORD_0807a98c  = 0x0201b290               fn tick_hand_effect_node_match_display_seq
DWORD_0807a990  = gP1LifePoints (symbolic) same fn -- already symbolic
DWORD_0807a994  = 0x00000868               same fn
DWORD_0807a998  = 0x000012a1               same fn (zone-query tag, raw literal)
DWORD_0807aa14  = 0x0201b290               fn dispatch_equip_banisher_activation_by_state
DWORD_0807aa18  = 0x0201bb90               same fn
DWORD_0807aa1c  = 0x00000868               same fn
DWORD_0807aa20  = 0x0201c510               same fn
DWORD_0807aa24  = 0x00001d10               same fn
DWORD_0807aa44  = 0x0201e2a0               same fn
DWORD_0807aa48  = 0x00001d10               same fn (dup in branch)
DWORD_0807aa58  = 0x00000137               same fn (display op-id)
DWORD_0807aa78  = gP1LifePoints (symbolic) same fn -- already symbolic
DWORD_0807aa7c  = 0x0201bb90               same fn (dup)
DWORD_0807aa94  = 0x0201bb90               same fn (dup)
DWORD_0807aab4  = 0x0201b290               fn dispatch_equip_prng_lp_row_and_bitmap_by_state
DWORD_0807aae4  = 0x0201e2a0               same fn
DWORD_0807aae8  = gP1LifePoints (symbolic) same fn -- already symbolic
DWORD_0807ab14  = gP1LifePoints (symbolic) same fn -- already symbolic
DWORD_0807ab4c  = gP1LifePoints (symbolic) same fn -- already symbolic
DWORD_0807ab50  = 0x00001daa               same fn
DWORD_0807ab54  = 0x0201bb90               same fn
DWORD_0807abb0  = 0x0201b290               fn dispatch_banisher_lp_penalty_by_field_count
DWORD_0807abb4  = gP1LifePoints (symbolic) same fn -- already symbolic
DWORD_0807abb8  = 0x00000868               same fn
DWORD_0807ac10  = 0x00001332               same fn (Banisher of the Light CID)
DWORD_0807ac14  = gP1LifePoints (symbolic) same fn -- already symbolic
DWORD_0807ac18  = 0x00001da8               same fn
DWORD_0807ac7c  = 0x00000868               fn enqueue_equip_slot_bitmap_update_by_count
DWORD_0807ac80  = 0x0201c510               same fn
DWORD_0807ad0c  = 0x00000868               fn enqueue_equip_sprite_on_zone_count_match
DWORD_0807ad10  = 0x0201c510               same fn
DWORD_0807ad4c  = 0x0201b290               fn tick_paired_slot_counter_update
DWORD_0807ad50  = 0x0000181e               same fn (paired-slot predicate)
DWORD_0807ad54  = 0x000004a4               same fn (counter offset)
DWORD_0807ad78  = 0x000004a4               same fn (counter offset dup in state-0x7f)
DWORD_0807ae2c  = 0x0201b290               fn tick_equip_zone_match_lp_row_type11
DWORD_0807ae30  = 0x00000868               same fn
DWORD_0807ae34  = 0x0201c510               same fn
DWORD_0807ae78  = gP1LifePoints (symbolic) same fn (state 0x7f branch) -- already symbolic
DWORD_0807ae7c  = 0x00001daa               same fn
DWORD_0807ae80  = 0x00001ce4               same fn
```

Total: 61 definitions confirmed by python count (matching roadmap estimate exactly).

### ROM_INCBIN blocks x8

| # | ROM_INCBIN | size | ROM abs addr |
|---|-----------|------|-------------|
| BLK1 | 0x79fac | 0x30 (48B) | 0x08079fac |
| BLK2 | 0x7a00c | 0xe8 (232B) | 0x0807a00c |
| BLK3 | 0x7a138 | 0x28 (40B) | 0x0807a138 |
| BLK4 | 0x7a178 | 0x14c (332B) | 0x0807a178 |
| BLK5 | 0x7a3b8 | 0x38 (56B) | 0x0807a3b8 |
| BLK6 | 0x7a464 | 0x11c (284B) | 0x0807a464 |
| BLK7 | 0x7a688 | 0x44 (68B) | 0x0807a688 |
| BLK8 | 0x7a71c | 0xf8 (248B) | 0x0807a71c |

---

## 数据块分类 (Rule 2/3) -- 每块 ref-scan 证据

ref-scan method: python rom.count(struct.pack('<I', addr)) for raw and addr|1 for THUMB;
plus 2B-step sweep of every entry within block.

| 块 | ref-scan (raw / THUMB+1) | 判定 | 理由 |
|---|---|---|---|
| BLK1 0x08079fac/0x30 | raw=0 THUMB+1=1 (at 0x9e42290) | R4 disasm (fn_eligible stub) | THUMB+1 ref in FS handler table entry [+0xc]; CID at [+0x8]=0x000017f4 (Abyssal Designator ABYSSAL_DESIGNATOR_CID, card_info.inc line verified); fn starts push {r4-r7,lr}; uses MOV PC,r0 to dispatch into adjacent dispatch table then BLK2 sub-stubs |
| BLK2 0x0807a00c/0xe8 | raw=1 at base + raw hits at 7 inner addrs (0xa03a, 0xa0a8, 0xa0bc, 0xa0cc, 0xa0da, 0xa0ea x6) | R4 disasm (dispatch sub-stubs) | raw refs are from dispatch table at 0x08079fdc (12 .word entries already structured in ASM); BLK1 stub loads table ptr via ldr [pc] then MOV PC,r0; sub-stubs are raw-addressed THUMB code (not BLX+1); first bytes confirmed THUMB at each entry; BLK2 contains 7 unique sub-stub entry-points |
| BLK3 0x0807a138/0x28 | raw=0 THUMB+1=1 (at 0x9e422f0) | R4 disasm (fn_eligible stub) | THUMB+1 ref in FS handler entry [+0xc]; CID at [+0x8]=0x000017f9 (Big Wave Small Wave BIG_WAVE_SMALL_WAVE_CID card_info.inc verified); fn starts push {r4,r5,lr} (0xb530); adjacent dispatch table at 0x0807a160 (6 .words already structured) feeds BLK4 |
| BLK4 0x0807a178/0x14c | raw=1 at base + inner hits at 5 addrs (0xa1ae, 0xa21a, 0xa240, 0xa25e, 0xa278) | R4 disasm (dispatch sub-stubs) | raw refs from dispatch table at 0x0807a160 (6 .word entries before DAT label, already structured); BLK3 stub uses MOV PC; sub-stubs at each raw-addressed entry confirmed THUMB; 6 unique entry-points (including base) |
| BLK5 0x0807a3b8/0x38 | raw=0 THUMB+1=2 (at 0x9e42398 and 0x9e442b8) | R4 disasm (fn_eligible stub, shared) | Two FS handler entries share the same fn_eligible pointer 0x0807a3b9; CIDs: [+0x8]=0x00001803 (unassigned, no card-stats.s entry) and 0x000015de (unassigned, exists as equip_cid_15de_08048a68 in card_info.inc); fn starts push {r4-r7,lr} (0xb5f0); stub followed by .zero 2 alignment padding at +0x2e then literal pool at +0x30 (0x7a3e8: .word 0x0201b290 gDuelPhaseFlags) and +0x34 (0x7a3ec: .word 0x0807a3f0 dispatch table ptr). Note: +0x2c (0x7a3e4) = 0x4687 THUMB MOV PC,r0 instruction, NOT a pool word. |
| BLK6 0x0807a464/0x11c | raw=1 at base + inner hits at 5 addrs (0xa4ac, 0xa534, 0xa544, 0xa560, 0xa570 x24) | R4 disasm (dispatch sub-stubs) | raw refs from dispatch table at 0x0807a3f0 (29 .word entries already structured in ASM after ROM_INCBIN 0x7a3b8/0x38); BLK5 stub uses MOV PC (0x4687 at +0x26); sub-stubs at each raw-addressed entry confirmed THUMB; 6 unique entry-points (0xa570 default case appears 24 times); block 0xa570 (movs r0,#0; ...; bx r1) is default-return stub |
| BLK7 0x0807a688/0x44 | raw=0 THUMB+1=1 (at 0x9e42410) | R4 disasm (fn_eligible stub) | THUMB+1 ref in FS handler entry [+0xc]; CID at [+0x8]=0x00001818 (Magician's Circle, slot=0x1818 in card-stats.s, NOT in card_info.inc yet -> NEW equate needed); fn starts push {r4,r5,lr} sub sp,#4 (0xb530/0x81b0); literal pool at +0x34 (.word 0x0201c4e0=gP1LifePoints), +0x38 (.word 0x00001ce8), +0x3c (.word 0x0201b290), +0x40 (.word 0x000004a4) -- these are within BLK7 bytes; adjacent dispatch table 0x0807a6d0 (19 .word entries at PTR_DAT_0807a6d0) already structured |
| BLK8 0x0807a71c/0xf8 | raw=1 at base + inner hits at 7 addrs (0xa730, 0xa764, 0xa77c, 0xa786, 0xa7a8, 0xa7ec, 0xa804 x12) | R4 disasm (dispatch sub-stubs) | raw refs from dispatch table PTR_DAT_0807a6d0 (19 entries, base 0x0807a6d0, already structured); BLK7 stub uses MOV PC (0x4687 at +0x30); sub-stubs confirmed THUMB at each entry; 8 unique entry-points (0xa804 default-return stub appears 12 times); block 0xa804 (movs r0,#0; add sp,#?; pop; bx r1) is default-return |

No zero-ref blocks in this segment. All 8 blocks have confirmed references (zero §5.1 entries for blocks).

### BLK7 literal pool note

BLK7 (0x7a688/0x44=68B) ends at 0x7a6cb. Within BLK7 bytes +0x34..+0x43 are a 4-word literal pool:
- +0x34 (0x7a6bc): 0x0201c4e0 (gP1LifePoints)
- +0x38 (0x7a6c0): 0x00001ce8 (P1LP_BLOCK2_OFF_1CE8, ewram.inc line 275 -- REUSE)
- +0x3c (0x7a6c4): 0x0201b290 (gDuelPhaseFlags)
- +0x40 (0x7a6c8): 0x000004a4 (EQUIP_PHASE_FRAME_OFF)

These literal pool words are INSIDE the ROM_INCBIN and will be consumed by the disasm
(Ghidra createDWord or auto-split during DisassembleCommand). The .word 0x0807a6d0 at 0x0807a6cc
(after BLK7) is the table-base literal pool, already extracted as a structured .word line in the ASM.

---

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate; createEquate in Ghidra)

All 51 unique-value slot uses below; duplicates of the same value share the equate.

| slot | value | equate_name | source | status |
|------|-------|-------------|--------|--------|
| DWORD_08079ebc | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | REUSE |
| DWORD_08079ec0 | 0x0201c600 | gP1FieldArrayCBase | ewram.inc | REUSE |
| DWORD_08079f44 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | REUSE (dup) |
| DWORD_08079f48 | 0x0201c510 | gDuelFieldSlots | ewram.inc | REUSE |
| DWORD_0807a134 | 0x00000ff8 | RED_EYES_B_DRAGON_CID | card_info.inc | REUSE |
| DWORD_0807a32c | 0x0201b290 | gDuelPhaseFlags | ewram.inc | REUSE |
| DWORD_0807a384 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | REUSE (dup) |
| DWORD_0807a5d4 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | REUSE (dup) |
| DWORD_0807a608 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc | REUSE |
| DWORD_0807a640 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc | REUSE (dup) |
| DWORD_0807a644 | 0x0000180d | NEO_DAEDALUS_OAM_SPRITE_BASE | NEW (equip_lp_delta.inc or new file) | NEW |
| DWORD_0807a8e8 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | REUSE (dup) |
| DWORD_0807a8ec | 0x0201c510 | gDuelFieldSlots | ewram.inc | REUSE (dup) |
| DWORD_0807a98c | 0x0201b290 | gDuelPhaseFlags | ewram.inc | REUSE (dup) |
| DWORD_0807a994 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | REUSE (dup) |
| DWORD_0807a998 | 0x000012a1 | zone_query_hand_tag_12a1 | NEW (duel_field.inc or inline) | EOL-only; createEquate to clear DWORD_ label; do NOT reuse PARASITE_PARACIDE_CID (adjudicated) |
| DWORD_0807aa14 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | REUSE (dup) |
| DWORD_0807aa18 | 0x0201bb90 | gEquipChainSlotRefs | ewram.inc | REUSE |
| DWORD_0807aa1c | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | REUSE (dup) |
| DWORD_0807aa20 | 0x0201c510 | gDuelFieldSlots | ewram.inc | REUSE (dup) |
| DWORD_0807aa24 | 0x00001d10 | DISPLAY_SEQ_ACTIVE_PLAYER_OFF | duel_field.inc | REUSE |
| DWORD_0807aa44 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc | REUSE |
| DWORD_0807aa48 | 0x00001d10 | DISPLAY_SEQ_ACTIVE_PLAYER_OFF | duel_field.inc | REUSE (dup) |
| DWORD_0807aa58 | 0x00000137 | CARD_DISPLAY_OP_ID_137 | NEW (duel_field.inc) | NEW |
| DWORD_0807aa7c | 0x0201bb90 | gEquipChainSlotRefs | ewram.inc | REUSE (dup) |
| DWORD_0807aa94 | 0x0201bb90 | gEquipChainSlotRefs | ewram.inc | REUSE (dup) |
| DWORD_0807aab4 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | REUSE (dup) |
| DWORD_0807aae4 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc | REUSE (dup) |
| DWORD_0807ab50 | 0x00001daa | LP_CARD_TRACK_NEXT_OFF | ewram.inc | REUSE |
| DWORD_0807ab54 | 0x0201bb90 | gEquipChainSlotRefs | ewram.inc | REUSE (dup) |
| DWORD_0807abb0 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | REUSE (dup) |
| DWORD_0807abb8 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | REUSE (dup) |
| DWORD_0807ac10 | 0x00001332 | BANISHER_OF_THE_LIGHT_CID | card_info.inc | REUSE |
| DWORD_0807ac18 | 0x00001da8 | LP_CARD_TRACK_BASE_OFF | ewram.inc | REUSE |
| DWORD_0807ac7c | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | REUSE (dup) |
| DWORD_0807ac80 | 0x0201c510 | gDuelFieldSlots | ewram.inc | REUSE (dup) |
| DWORD_0807ad0c | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | REUSE (dup) |
| DWORD_0807ad10 | 0x0201c510 | gDuelFieldSlots | ewram.inc | REUSE (dup) |
| DWORD_0807ad4c | 0x0201b290 | gDuelPhaseFlags | ewram.inc | REUSE (dup) |
| DWORD_0807ad50 | 0x0000181e | EQUIP_PAIRED_SLOT_PRED | NEW (duel_field.inc) | NEW |
| DWORD_0807ad54 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc | REUSE (dup) |
| DWORD_0807ad78 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc | REUSE (dup) |
| DWORD_0807ae2c | 0x0201b290 | gDuelPhaseFlags | ewram.inc | REUSE (dup) |
| DWORD_0807ae30 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | REUSE (dup) |
| DWORD_0807ae34 | 0x0201c510 | gDuelFieldSlots | ewram.inc | REUSE (dup) |
| DWORD_0807ae7c | 0x00001daa | LP_CARD_TRACK_NEXT_OFF | ewram.inc | REUSE (dup) |
| DWORD_0807ae80 | 0x00001ce4 | LP_D_TRIBE_BLOCK_OFF | ewram.inc | REUSE |

Notes:
- DWORD_0807a998 = 0x000012a1: used as 3rd argument to find_effect_node_in_zone (zone-query tag/
  node-type attribute code). Numerically coincides with PARASITE_PARACIDE_CID (card_info.inc) but
  the call site is find_effect_node_in_zone not a card lookup. ADJUDICATED: do NOT reuse
  PARASITE_PARACIDE_CID. Use createEquate with name zone_query_hand_tag_12a1 + EOL annotation
  "zone query node-type tag for find_effect_node_in_zone (hand zone=0xb)".
  Confidence: high (asm/10 L821: movs r1,#0xb; ldr r2,DWORD_0807a998; bl find_effect_node_in_zone).
- DWORD_0807a380, DWORD_0807a990, DWORD_0807aa78, DWORD_0807aae8, DWORD_0807ab14, DWORD_0807ab4c,
  DWORD_0807abb4, DWORD_0807ac14, DWORD_0807ae78: all contain .word gP1LifePoints -- ALREADY
  SYMBOLIC in ASM, no createEquate needed; only slot label rename required.

### RENAME_SLOTS (auto-name -> semantic label; plain slot rename)

These slots are already symbolically valued (gP1LifePoints) or need only a label rename:

| slot | current | new label | evidence |
|------|---------|-----------|----------|
| DWORD_0807a380 | DWORD_ | lp_state_base_a32c | already .word gP1LifePoints; rename slot label only |
| DWORD_0807a990 | DWORD_ | player_life_ptr_a990 | already .word gP1LifePoints |
| DWORD_0807aa78 | DWORD_ | player_life_ptr_aa78 | already .word gP1LifePoints |
| DWORD_0807aae8 | DWORD_ | player_life_ptr_aae8 | already .word gP1LifePoints |
| DWORD_0807ab14 | DWORD_ | player_life_ptr_ab14 | already .word gP1LifePoints |
| DWORD_0807ab4c | DWORD_ | player_life_ptr_ab4c | already .word gP1LifePoints |
| DWORD_0807abb4 | DWORD_ | player_life_ptr_abb4 | already .word gP1LifePoints |
| DWORD_0807ac14 | DWORD_ | player_life_ptr_ac14 | already .word gP1LifePoints |
| DWORD_0807ae78 | DWORD_ | player_life_ptr_ae78 | already .word gP1LifePoints |

Alternative approach: since all these store the same gP1LifePoints, the Ghidra rename is
setEolComment "gP1LifePoints literal pool" on each. The ASM slot label can use the function-scoped
pattern `<fn>_player_life_b` / `_c` to avoid collisions.

### REF_SLOTS (USER-label + DATA-ref for ROM_INCBIN bases and dispatch tables)

| slot | current | new label | type |
|------|---------|-----------|------|
| DAT_0807a00c | DAT_ | equip_sprite_zone_type_stubs | R4 disasm entry base (after clearListing) |
| DAT_0807a178 | DAT_ | equip_sprite_red_eyes_stubs | R4 disasm entry base |
| DAT_0807a464 | DAT_ | equip_sprite_player_stubs | R4 disasm entry base |
| PTR_DAT_0807a6d0 | PTR_DAT_ | equip_sprite_capacity_jump_table | structured dispatch table (already as .word entries in ASM; keep label, rename to meaningful) |
| DAT_0807a71c | DAT_ | equip_sprite_capacity_stubs | R4 disasm entry base |

### FUNC_RENAME (误名订正)

No function name contradictions detected in Seg-1. All 19 function names match their
observed body behavior. No FUNC_RENAME candidates.

### PLATE (R5)

No plate rewrites required for named functions; all plates are ASCII (grep confirmed 0 non-ASCII
lines in Seg-1). No stale FUN_ references found (C8 scan: 0 hits).

For the 4 newly disassembled stub blocks, plates/EOL comments will be added during R4 disasm
(describing sub-stub semantics per entry). All must be ASCII.

---

## carve 计划 (R7)

No inter-function data tables need carving into rom.s in Seg-1.

The dispatch tables (at 0x08079fdc, 0x0807a160, 0x0807a3f0, PTR_DAT_0807a6d0) are ALREADY
structured as .word lines in the ASM (between the ROM_INCBIN blocks). They do NOT need
additional carving -- they are already byte-identical .word sequences.

The fn_eligible stub literal pools (last few words inside BLK1/BLK3/BLK5/BLK7) will be
handled automatically by DisassembleCommand + createDWord force-splits. No separate rom.s
carve required for these.

---

## disasm 计划 (R4)

Four ROM_INCBIN blocks contain THUMB code. For each, the procedure is:
1. clearListing over the entire block range
2. setTMode on first instruction address
3. DisassembleCommand per sub-stub entry-point (not a single range command)
4. createDWord for literal pool words at block tail (to force clean split)

### BLK1: 0x08079fac / 0x30 = fn_eligible stub (Abyssal Designator CID=0x17f4)

Entry: 0x08079fac (single fn_eligible function)
Procedure: clearListing(0x79fac, 0x79fdc); setTMode(0x79fac); DisassembleCommand(0x79fac, None, True)
Literal pool (2 words, BLK1+0x28..+0x2f):
  createDWord at 0x79fd4  (.word gDuelPhaseFlags = 0x0201b290)  -- LDR r0,[PC,#24] at BLK1+0x0c targets 0x79fd4
  createDWord at 0x79fd8  (.word dispatch table ptr = 0x08079fdc)
Note: 0x79fdc..0x7a00b are .word dispatch table entries (already structured, do not disasm)
EOL at 0x79fac: "fn_eligible Abyssal Designator CID=ABYSSAL_DESIGNATOR_CID (0x17f4)"
Post-disasm: 0x79fac..0x79fdb = code, 0x79fd4..0x79fdb = literal pool (2 words)
  -> createDWord(0x79fd4) and createDWord(0x79fd8) force pool split before dispatch table

### BLK2: 0x0807a00c / 0xe8 = dispatch sub-stubs (zone-type sprite routing)

7 unique entry-points (from dispatch table at 0x79fdc):
  0x0807a00c (default entry base / last dispatch table slot)
  0x0807a03a (entry index+1)
  0x0807a0a8
  0x0807a0bc
  0x0807a0cc
  0x0807a0da
  0x0807a0ea (default-return stub; 6 dispatch table slots point here)

Order: clearListing(0x7a00c, 0x7a0f4); setTMode(0x7a00c); DisassembleCommand per entry in address order:
  DisassembleCommand(0x7a00c, None, True)
  DisassembleCommand(0x7a03a, None, True)
  DisassembleCommand(0x7a0a8, None, True)
  DisassembleCommand(0x7a0bc, None, True)
  DisassembleCommand(0x7a0cc, None, True)
  DisassembleCommand(0x7a0da, None, True)
  DisassembleCommand(0x7a0ea, None, True)
Verify each stub stops at unconditional b/bx before the next entry.
Zero-residue proof: union of 7 stubs must cover all bytes 0x7a00c..0x7a0f3 exactly.
EOL per entry: "zone-type sprite dispatch case N: calls <callee>"

### BLK3: 0x0807a138 / 0x28 = fn_eligible stub (Big Wave Small Wave CID=0x17f9)

Entry: 0x0807a138 (single fn_eligible function)
Procedure: clearListing(0x7a138, 0x7a160); setTMode(0x7a138); DisassembleCommand(0x7a138, None, True)
Literal pool within BLK3: approximately at 0x7a158..0x7a15f (last 8B = 2 .word)
  createDWord as needed for literal pool
Note: 0x7a160..0x7a177 are 6 .word dispatch entries already structured
EOL at 0x7a138: "fn_eligible Big Wave Small Wave CID=BIG_WAVE_SMALL_WAVE_CID (0x17f9)"

### BLK4: 0x0807a178 / 0x14c = dispatch sub-stubs (Red-Eyes LP routing)

6 unique entry-points (from dispatch table at 0x7a160):
  0x0807a178 (base, last dispatch entry)
  0x0807a1ae
  0x0807a21a
  0x0807a240
  0x0807a25e
  0x0807a278

clearListing(0x7a178, 0x7a2c4); setTMode(0x7a178); DisassembleCommand per entry:
  DisassembleCommand(0x7a178, None, True) -- note: base does NOT start with push;
    starts with adds r0,r7,#0 / bl check_effect_slot_matches_zone_entry style sequence
  DisassembleCommand(0x7a1ae, None, True)
  DisassembleCommand(0x7a21a, None, True)
  DisassembleCommand(0x7a240, None, True)
  DisassembleCommand(0x7a25e, None, True)
  DisassembleCommand(0x7a278, None, True)
Verify zero-residue: union covers 0x7a178..0x7a2c3.
Note: 0x7a2c4 is start of enqueue_sprite_attr_for_effect_zone_hit (already named).

### BLK5: 0x0807a3b8 / 0x38 = fn_eligible stub (shared; CID 0x1803 and 0x15de)

Entry: 0x0807a3b8 (single fn_eligible function, used by two CID handler entries)
Procedure: clearListing(0x7a3b8, 0x7a3f0); setTMode(0x7a3b8); DisassembleCommand(0x7a3b8, None, True)
Literal pool within BLK5 at +0x30..+0x37 (last 8B, after .zero 2 alignment at +0x2e):
  IMPORTANT: +0x2c (0x7a3e4) = 0x4687 = THUMB MOV PC,r0 instruction -- DO NOT createDWord here.
  +0x30 (0x7a3e8): gDuelPhaseFlags (0x0201b290)  -> createDWord at 0x7a3e8
    [LDR r0,[PC,#28] at BLK5+0x12 (0x7a3ca) targets 0x7a3e8 -- ROM-confirmed]
  +0x34 (0x7a3ec): dispatch table ptr (0x0807a3f0) -> createDWord at 0x7a3ec
    [LDR r1,[PC,#12] at BLK5+0x26 (0x7a3de) targets 0x7a3ec -- ROM-confirmed]
Note: the .word at 0x7a3ec points to the dispatch table that follows (0x7a3f0..0x7a463),
  already structured as 29 .word lines in ASM.
EOL at 0x7a3b8: "fn_eligible shared stub CID 0x1803 (unassigned) and CID=equip_cid_15de (0x15de)"

### BLK6: 0x0807a464 / 0x11c = dispatch sub-stubs (player-type equip sprite)

6 unique entry-points (from dispatch table 0x7a3f0, 29 entries):
  0x0807a464 (base, dispatch table slot[28])
  0x0807a4ac
  0x0807a534
  0x0807a544
  0x0807a560
  0x0807a570 (default-return stub; 24 dispatch slots point here)

clearListing(0x7a464, 0x7a580); setTMode(0x7a464); DisassembleCommand per entry:
  DisassembleCommand(0x7a464, None, True)
  DisassembleCommand(0x7a4ac, None, True)
  DisassembleCommand(0x7a534, None, True)
  DisassembleCommand(0x7a544, None, True)
  DisassembleCommand(0x7a560, None, True)
  DisassembleCommand(0x7a570, None, True)
Verify zero-residue: union covers 0x7a464..0x7a57f.
Note: 0x7a580 = submit_equip_lp_bar_with_slot_sprite (already named). 
  Check: 0x7a57f is last byte of BLK6 (0x7a464 + 0x11c - 1 = 0x7a57f). Correct.

### BLK7: 0x0807a688 / 0x44 = fn_eligible stub (Magician's Circle CID=0x1818)

Entry: 0x0807a688 (single fn_eligible function)
Procedure: clearListing(0x7a688, 0x7a6cc); setTMode(0x7a688); DisassembleCommand(0x7a688, None, True)
Literal pool within BLK7 at +0x34..+0x43 (last 16B = 4 .word):
  0x7a6bc: 0x0201c4e0 (gP1LifePoints)
  0x7a6c0: 0x00001ce8 (P1LP_BLOCK2_OFF_1CE8, ewram.inc line 275 -- REUSE; NOT raw literal)
  0x7a6c4: 0x0201b290 (gDuelPhaseFlags)
  0x7a6c8: 0x000004a4 (EQUIP_PHASE_FRAME_OFF)
  createDWord at each of these 4 addresses.
  After createDWord(0x7a6c0): add createEquate or EOL "P1LP_BLOCK2_OFF_1CE8" to reference ewram.inc constant.
Note: 0x7a6cc is the .word 0x0807a6d0 (dispatch table base ptr), which is OUTSIDE BLK7
  (BLK7 = 0x7a688..0x7a6cb, 0x44=68 bytes, ends at 0x7a6cb).
  The .word at 0x7a6cc is already structured in ASM and outside the ROM_INCBIN.
EOL at 0x7a688: "fn_eligible Magicians Circle CID=0x1818; uses dispatch table at 0x0807a6d0"

### BLK8: 0x0807a71c / 0xf8 = dispatch sub-stubs (zone-capacity equip sprite)

8 unique entry-points (from dispatch table PTR_DAT_0807a6d0, 19 entries):
  0x0807a71c (base, dispatch table slot[18])
  0x0807a730
  0x0807a764
  0x0807a77c
  0x0807a786
  0x0807a7a8
  0x0807a7ec
  0x0807a804 (default-return stub; 12 dispatch slots point here)

clearListing(0x7a71c, 0x7a814); setTMode(0x7a71c); DisassembleCommand per entry:
  DisassembleCommand(0x7a71c, None, True)
  DisassembleCommand(0x7a730, None, True)
  DisassembleCommand(0x7a764, None, True)
  DisassembleCommand(0x7a77c, None, True)
  DisassembleCommand(0x7a786, None, True)
  DisassembleCommand(0x7a7a8, None, True)
  DisassembleCommand(0x7a7ec, None, True)
  DisassembleCommand(0x7a804, None, True)
Verify zero-residue: union covers 0x7a71c..0x7a813.
Note: 0x7a814 = enqueue_slot_sprite_on_zone_count_and_state_code (already named; starts 0xb5f0).

---

## 新增 constants / 全局

C5 dedup-by-value verified for ALL new candidates:

### 1. NEO_DAEDALUS_OAM_SPRITE_BASE = 0x0000180d

grep by value 0x0000180d across all constants/*.inc: 0 hits (confirmed NEW).
Consumer: dispatch_neo_daedalus_equip_sprite_by_monster_count (asm/10 L540):
  `ldr r2, DWORD_0807a644` then `orrs r1,r2` -- r2 is OAM attr base ORed with player_id<<13.
  The value 0x180d is an OAM sprite attr2 base (0x180d = OBJ size/shape bits for Neo-Daedalus
  sprite), not a card ID.
File: equip_lp_delta.inc (or new neo_daedalus.inc -- recommend equip_lp_delta.inc as it groups
  equip-system sprite constants).
Confidence: high (asm/10 L540-L546, orrs r1,r2 at 0807a622).

### 2. CARD_DISPLAY_OP_ID_137 = 0x00000137

grep by value 0x00000137 across all constants/*.inc: 0 hits (confirmed NEW).
Note: 0x0000137b (EYE_OF_TRUTH_CID) exists but does NOT match 0x137.
Consumer: dispatch_equip_banisher_activation_by_state (asm/10 L954):
  `ldr r0, DWORD_0807aa58; bl invoke_card_display_op_0x31_sub1`
  -- 0x137 is the op-id argument for the Banisher activation display operation.
File: duel_field.inc (display op codes section).
Confidence: high (asm/10 L954-L955, single consumer, direct operand to invoke fn).

### 3. EQUIP_PAIRED_SLOT_PRED = 0x0000181e

grep by value 0x0000181e across all constants/*.inc: 0 hits (confirmed NEW).
Consumer: tick_paired_slot_counter_update (asm/10 L1391):
  `ldr r1, DWORD_0807ad50; bl count_equipped_paired_slots_for_player`
  -- 0x181e is the predicate/slot-type filter passed to count_equipped_paired_slots_for_player.
  Likely encodes a paired-slot type attribute (0x181e = bit pattern for specific equip pair).
File: duel_field.inc or equip_lp_delta.inc.
Confidence: med (the predicate semantics of 0x181e depend on count_equipped_paired_slots_for_player
  internals which are not in this segment; name is structurally correct based on usage).

### 4. CID for Magician's Circle = 0x00001818

grep by value 0x00001818 across all constants/*.inc: 0 hits (confirmed NEW).
card-stats.s: card_1694 @ Magicians Circle slot=0x1818 pw=00050755 -- confirmed.
Usage: BLK7 fn_eligible stub for FS handler entry with CID=0x1818.
Name: MAGICIANS_CIRCLE_CID
File: card_info.inc.
Confidence: high (card-stats.s line verified; FS entry structure [+0x8]=0x00001818 at 0x9e4240c).

### Summary

| name | value | file | status |
|------|-------|------|--------|
| NEO_DAEDALUS_OAM_SPRITE_BASE | 0x0000180d | equip_lp_delta.inc | NEW |
| CARD_DISPLAY_OP_ID_137 | 0x00000137 | duel_field.inc | NEW |
| EQUIP_PAIRED_SLOT_PRED | 0x0000181e | duel_field.inc | NEW |
| MAGICIANS_CIRCLE_CID | 0x00001818 | card_info.inc | NEW |

### CID equates for fn_eligible stubs -- reuse summary

| block | CID hex | decimal | card | equate_name | status |
|-------|---------|---------|------|-------------|--------|
| BLK1 | 0x17f4 | 6132 | Abyssal Designator | ABYSSAL_DESIGNATOR_CID | REUSE (card_info.inc) |
| BLK3 | 0x17f9 | 6137 | Big Wave Small Wave | BIG_WAVE_SMALL_WAVE_CID | REUSE (card_info.inc) |
| BLK5 | 0x1803 | 6147 | unassigned | equip_cid_1803_stub (need new) | NEW (low conf) |
| BLK5 | 0x15de | 5598 | unassigned | equip_cid_15de_08048a68 | REUSE (card_info.inc) |
| BLK7 | 0x1818 | 6168 | Magician's Circle | MAGICIANS_CIRCLE_CID | NEW |

Note on CID 0x1803: unassigned slot (not in card-stats.s between 0x1802 Greed and 0x1804 Cemetery Bomb).
The BLK5 fn_eligible stub serves both 0x1803 and 0x15de entries, so the stub label should be neutral:
  `equip_fn_eligible_shared_1803_15de` (or simply use raw address in Ghidra).
The EOL on the disassembled code: "fn_eligible: CID 0x1803 (unassigned) + equip_cid_15de_08048a68 (0x15de)"

---

## §5.1 登记 (Rule 3) -- 0 引用块

None. All 8 ROM_INCBIN blocks have at least 1 confirmed reference (raw or THUMB+1).

---

## 消费者证据 (R6) -- 关键槽语义

| slot | value | evidence | confidence |
|------|-------|----------|-----------|
| DWORD_0807a644 = 0x180d | NEO_DAEDALUS_OAM_SPRITE_BASE | asm/10 L540-L546: `ldr r2,DWORD_0807a644; ... lsls r1,r1,#0xd; orrs r1,r2` then `setup_equip_oam_entry_with_sprite_attr` | high |
| DWORD_0807aa58 = 0x137 | CARD_DISPLAY_OP_ID_137 | asm/10 L954-L955: `ldr r0,DWORD_0807aa58; bl invoke_card_display_op_0x31_sub1` | high |
| DWORD_0807ad50 = 0x181e | EQUIP_PAIRED_SLOT_PRED | asm/10 L1391-L1392: `ldr r1,DWORD_0807ad50; bl count_equipped_paired_slots_for_player` | med |
| DWORD_0807a998 = 0x12a1 | zone_query_tag (NOT card) | asm/10 L821: `movs r1,#0xb; ldr r2,DWORD_0807a998; bl find_effect_node_in_zone` -- third arg is node type code | high |
| BLK1 fn_eligible = ABYSSAL_DESIGNATOR | FS table 0x9e42290: entry[+0xc]=0x08079fad (+1), entry[+0x8]=0x000017f4; card-stats.s card_1665 slot=0x17F4 | high |
| BLK3 fn_eligible = BIG_WAVE_SMALL_WAVE | FS table 0x9e422f0: entry[+0xc]=0x0807a139 (+1), entry[+0x8]=0x000017f9; card-stats.s card_1670 slot=0x17F9 | high |
| BLK7 fn_eligible = MAGICIANS_CIRCLE | FS table 0x9e42410: entry[+0xc]=0x0807a689 (+1), entry[+0x8]=0x00001818; card-stats.s card_1694 slot=0x1818 | high |

---

## C5 双向核 (dedup-by-value)

All EQ_SLOTS: grep by VALUE in constants/*.inc before declaring NEW.

REUSE confirmed (value found):
- 0x00000868 -> PLAYER_BLOCK_STRIDE (ewram.inc grep match confirmed)
- 0x0201c600 -> gP1FieldArrayCBase (ewram.inc confirmed)
- 0x0201c510 -> gDuelFieldSlots (ewram.inc confirmed)
- 0x00000ff8 -> RED_EYES_B_DRAGON_CID (card_info.inc confirmed)
- 0x0201b290 -> gDuelPhaseFlags (ewram.inc confirmed)
- 0x000004a4 -> EQUIP_PHASE_FRAME_OFF (ewram.inc confirmed)
- 0x0201bb90 -> gEquipChainSlotRefs (ewram.inc confirmed)
- 0x00001d10 -> DISPLAY_SEQ_ACTIVE_PLAYER_OFF (duel_field.inc confirmed)
- 0x0201e2a0 -> gDuelCardCtxBase (ewram.inc confirmed)
- 0x00001daa -> LP_CARD_TRACK_NEXT_OFF (ewram.inc confirmed)
- 0x00001332 -> BANISHER_OF_THE_LIGHT_CID (card_info.inc confirmed)
- 0x00001da8 -> LP_CARD_TRACK_BASE_OFF (ewram.inc confirmed)
- 0x00001ce4 -> LP_D_TRIBE_BLOCK_OFF (ewram.inc confirmed)
- 0x000017f4 -> ABYSSAL_DESIGNATOR_CID (card_info.inc confirmed)
- 0x000017f9 -> BIG_WAVE_SMALL_WAVE_CID (card_info.inc confirmed)
- 0x000015de -> equip_cid_15de_08048a68 (card_info.inc confirmed)
- 0x00001ce8 -> P1LP_BLOCK2_OFF_1CE8 (ewram.inc line 275 confirmed; BLK7 literal pool at 0x7a6c0 -- REUSE, not raw literal)

NEW confirmed (value not found by grep):
- 0x0000180d -> NEO_DAEDALUS_OAM_SPRITE_BASE (grep=0 hits)
- 0x00000137 -> CARD_DISPLAY_OP_ID_137 (grep=0 hits; 0x137b exists but != 0x137)
- 0x0000181e -> EQUIP_PAIRED_SLOT_PRED (grep=0 hits)
- 0x00001818 -> MAGICIANS_CIRCLE_CID (grep=0 hits)
- 0x00001803 -> equip_cid_1803 (grep=0 hits; unassigned slot)

---

## C8 stale FUN_ scan

grep FUN_[0-9a-f]{8} in asm/10 Seg-1 range: 0 hits. No stale FUN_ references to fix.

---

## C13 残留 100% 覆盖证据 (独立 python 精确清点)

Python count of DWORD_/DAT_/PTR_DAT_ definition lines in Seg-1:
  - Scan from enqueue_neo_daedalus_zone_oam_on_available_slot: to first occurrence of 0807ae84
  - Result: 61 definition lines (matches roadmap estimate exactly)

Coverage accounting:
  - EQ_SLOTS via createEquate (REUSE/NEW): 47 slots
    (excluding 9 already-symbolic gP1LifePoints slots and 5 ROM_INCBIN base labels)
  - RENAME_SLOTS (already-symbolic gP1LifePoints, DWORD->named): 9 slots
  - REF_SLOTS (ROM_INCBIN base labels, dispatch table label): 5 slots
    (DAT_0807a00c, DAT_0807a178, DAT_0807a464, PTR_DAT_0807a6d0, DAT_0807a71c)
  Total classified: 47 + 9 + 5 = 61 = all slots

R4 disasm eliminates 8 ROM_INCBIN blocks (no §5.1 entries for blocks).
Post-landing residue target: 0 DAT_/DWORD_/PTR_DAT_ + 0 ROM_INCBIN.

Literal pools inside BLK1/BLK3/BLK5/BLK7: handled by createDWord during disasm phase;
these do NOT create new auto-name slots (they become part of the disassembled function body).

Note: DWORD_0807a998 (0x12a1) is in the EQ_SLOT count. Reviewer adjudicated EOL-only acceptable
(independent zone-query tag; do NOT reuse PARASITE_PARACIDE_CID). The slot label DWORD_ still
requires createEquate or a USER label rename to clear the DWORD_ prefix for zero-residue.
Recommended: createEquate(0x0807a998, "zone_query_hand_tag_12a1", 0x12a1) + EOL annotation.

---

## 求助

- CID 0x1803 (BLK5, second FS entry): ADJUDICATED (reviewer裁定1). Confirmed unassigned
  (card-stats.s: 0x1802=Greed, 0x1804=Cemetery Bomb, gap confirmed). Use neutral EOL comment
  "CID 0x1803 (unassigned)" -- no independent .equ needed. Proposal handling correct.

- DWORD_0807a998 = 0x12a1 (zone_query_tag): ADJUDICATED (reviewer裁定2). Do NOT reuse
  PARASITE_PARACIDE_CID. This is an independent zone-query node-type tag passed to
  find_effect_node_in_zone (semantic collision, not card-ID context). Use EOL-only annotation:
  "zone query node-type tag for find_effect_node_in_zone (hand zone=0xb)". No createEquate needed.
  Proposal EOL-only recommendation confirmed correct.

- 0x00001ce8 inside BLK7 literal pool (at +0x38 / 0x7a6c0 within BLK7): RESOLVED (reviewer
  裁定3 / #FIX1). P1LP_BLOCK2_OFF_1CE8 = 0x1ce8 already exists at ewram.inc line 275. REUSE
  confirmed. Ghidra will reference P1LP_BLOCK2_OFF_1CE8 via createEquate or EOL after
  createDWord(0x7a6c0).

---

## Split decision

Seg-1 has 19 fn + 61 slots + 8 ROM_INCBIN. The workload is heavy but uniform:
all 8 blocks are clearly classified (4 fn_eligible stubs -> R4 disasm; 4 dispatch tables of
sub-stubs -> R4 disasm; 0 §5.1). The slot list is dense with repeating equates (PLAYER_BLOCK_STRIDE,
gDuelPhaseFlags, etc.) and only 4 NEW constants. This is manageable as a single Seg-1 proposal
without an a/b split.

Recommendation: proceed as F10-Seg-1 without split.
