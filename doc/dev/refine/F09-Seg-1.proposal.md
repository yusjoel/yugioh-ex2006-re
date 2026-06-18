# Refine Proposal: F09-Seg-1  [0x0806e76c..0x0806ff50)

## Section Mapping

Function entries (20 named):
- 0x0806e76c  enqueue_slot_sprite_type11_with_card_id
- 0x0806e780  enqueue_slot_sprites_by_card_id_scoring
- 0x0806e840  dispatch_equip_zone_token_or_lp_sprite_by_slot_type
- 0x0806e898  dispatch_equip_chain_state_sprite_by_slot
- 0x0806ea00  dispatch_equip_zone_entry_activation_or_bitmap
- 0x0806ebd4  dispatch_equip_lp_display_by_state_and_ref
- 0x0806ecb0  apply_equip_activation_if_zone_entry_vacant
- 0x0806ed20  tick_equip_zone_slot_sprite_display_state_machine
- 0x0806edd4  invoke_equip_oam_setup_if_neo_daedalus_zone14_eligible
- 0x0806ee54  tick_zone_slot_indicator_display_seq
- 0x0806ef88  submit_lp_indicator_if_tile_count_match
- 0x0806f1c8  dispatch_dual_zone_equip_chain_sprite_by_state
- 0x0806f2cc  enqueue_zone_subentry_sprites_with_xy_split
- 0x0806f390  dispatch_hand_card_slot_sprite_by_state_and_card_id
- 0x0806f500  submit_equip_lp_indicators_if_zone_tile_count_matched
- 0x0806f5a4  submit_equip_lp_indicators_if_hand_slot_found
- 0x0806f5d0  set_equip_player_state_bit_after_eligibility_refresh
- 0x0806f5f0  tick_lp_zone_sprite_display_seq
- 0x0806f788  enqueue_hand_to_monster_slot_equip_sprite
- 0x0806fb88  tick_equip_chain_activation_display_seq

Residual auto-name slots: 77 total (74 data + 3 block-start labels for ROM_INCBIN)

ROM_INCBIN / DISASM blocks: 6 incbin + 1 switchD(0x6e8b6, inline)

---

## Data Block Classification (Rule 2/3) -- ref-scan evidence

| Block | ROM off / size | ref-scan (raw / THUMB+1) | Judgment | Reason |
|-------|----------------|--------------------------|----------|--------|
| Block1 | 0x6f008 / 0x34 | raw=1@0x806d7(mod4=3,misaligned->false) / thumb+1=1@0x1e40958 | DISASM (fn_eligible) | THUMB+1 from FS handler table entry at 0x1e40958; CID at entry-4=0x142a (Creature Swap); fn_eligible stub for card effect |
| Block2 | 0x6f054 / 0x174 | raw=1@0x6f050(aligned,same-seg dispatch table) / thumb+1=0 | DISASM (raw dispatch) | Raw code ptr from dispatch table at 0x6f03c-0x6f053; 6 sub-stubs: 0x806f054/066/078/0ac/0cc/188 reached via MOV PC,r0 |
| Block3 | 0x6f85c / 0x138 | raw=1@0x437dc0(compressed game data,false) / thumb+1=2@0x1e40a90+0x1e43a30 | DISASM (fn_eligible) | 2x THUMB+1 from FS handler table; CID at each entry-4=0x1468 (Destiny Board, confirmed card-stats.s pw=94212438); compressed-data false-positive confirmed by surrounding bytes 0x02182524/0xfd02f9f5/0xdeddebf9 |
| Block4 | 0x6fa08 / 0x180 | raw=1@0x6fa04(aligned,same-seg dispatch table) / thumb+1=0 | DISASM (raw dispatch) | Raw code ptr from dispatch table at 0x6f994-0x6fa07; 10 sub-stubs: 0x806fa08/4c/5e/74/fb14/4c/58/64/70/76 |
| Block5 | 0x6fdec / 0x28 | raw=0 / thumb+1=2(real@0x1e46610+false@0x3d3eb6) | DISASM (fn_eligible) | Real THUMB+1 from FS handler table at 0x1e46610; CID at entry-4=0x146f (Cathedral of Nobles, card-stats.s pw=29762407); 0x3d3eb6 hit is compressed data: surrounding bytes 0x08faece3/0xe1e2edfd show non-pointer content |
| Block6 | 0x6fe88 / 0xc8 | raw=1@0x6fe84(aligned,same-seg dispatch table) / thumb+1=0 | DISASM (raw dispatch) | Raw code ptr from dispatch table at 0x6fe14-0x6fe87; 8 sub-stubs: 0x806fe88/edc/ef0/ff0a/ff1a/ff2c/ff3c/ff46 |

switchD_0806e8b6: inline jump table (29 entries, cases 0x64..0x80) at 0x0806e8c0, all targets already disassembled as labeled case stubs within dispatch_equip_chain_state_sprite_by_slot. No R4 action needed; only DAT_0806e8bc (table-ptr slot) requires a REF symbolization.

---

## Symbolization Plan (R1/R2/R3)

### EQ_SLOTS (data-equate)

All values verified by python struct.unpack_from('<I', rom, slot_offset)[0].

**Reuse existing constants:**

| slot | value | const_name | source | slot_label |
|------|-------|-----------|--------|-----------|
| DWORD_0806e7b0 | 0x0000153d | PYRAMID_ENERGY_CID | card_info.inc | pyramid_energy_cid_e7b0 |
| DWORD_0806e7b4 | 0x00001409 | LIMITER_REMOVAL_CID | card_info.inc | limiter_removal_cid_e7b4 |
| DWORD_0806e7c8 | 0x000015ae | D_TRIBE_CID | card_info.inc | d_tribe_cid_e7c8 |
| DAT_0806e990  | 0x0000140b | INSECT_IMITATION_CID | card_info.inc | insect_imitation_cid_e990 |
| DWORD_0806e7e8 | 0x0000ffff | EQUIP_SLOT_SCORE_CAP | oam_attr.inc | score_cap_e7e8 |
| DWORD_0806e894 | 0x000010d0 | LP_ACTIVATION_LINK_FLAG_OFF | ewram.inc | lp_link_flag_off_e894 |
| DWORD_0806fc94 | 0x000010d0 | LP_ACTIVATION_LINK_FLAG_OFF | ewram.inc | lp_link_flag_off_fc94 |
| DAT_0806ec60  | 0x00001da8 | LP_CARD_TRACK_BASE_OFF | ewram.inc | lp_card_track_base_off_ec60 |
| DWORD_0806f6b4 | 0x00001da8 | LP_CARD_TRACK_BASE_OFF | ewram.inc | lp_card_track_base_off_f6b4 |
| DWORD_0806f734 | 0x00001da8 | LP_CARD_TRACK_BASE_OFF | ewram.inc | lp_card_track_base_off_f734 |
| DWORD_0806eedc | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc | equip_phase_frame_off_eedc |
| DWORD_0806ef7c | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc | equip_phase_frame_off_ef7c |
| DWORD_0806fc9c | 0x0000801b | OAM_EQUIP_SPRITE_TILE_P2_1B | oam_attr.inc | oam_sprite_p2_1b_fc9c |
| DWORD_0806fdd4 | 0x00008019 | OAM_SPRITE_CODE_P1_ACTIVATION | oam_attr.inc | oam_sprite_p1_act_fdd4 |
| DAT_0806eab4  | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | player_stride_eab4 |
| DAT_0806eb4c  | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | player_stride_eb4c |
| DAT_0806ebd0  | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | player_stride_ebd0 |
| DAT_0806ed18  | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | player_stride_ed18 |
| DAT_0806ed64  | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | player_stride_ed64 |
| DWORD_0806ee4c | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | player_stride_ee4c |
| DWORD_0806eee4 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | player_stride_eee4 |
| DWORD_0806ef38 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | player_stride_ef38 |
| DWORD_0806f000 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | player_stride_f000 |
| DWORD_0806f2c4 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | player_stride_f2c4 |
| DWORD_0806f388 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | player_stride_f388 |
| DWORD_0806f58c | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | player_stride_f58c |
| DWORD_0806f6b8 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | player_stride_f6b8 |
| DWORD_0806f738 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | player_stride_f738 |
| DWORD_0806f784 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | player_stride_f784 |
| DWORD_0806f854 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | player_stride_f854 |
| DWORD_0806fc98 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | player_stride_fc98 |
| DWORD_0806fd48 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | player_stride_fd48 |

**New equates (6 values, must be added to constants files):**

| slot | value | const_name | file | slot_label | evidence |
|------|-------|-----------|------|-----------|---------|
| DWORD_0806e7cc | 0x00001882 | BIG_MARCH_OF_ANIMALS_CID | card_info.inc | big_march_cid_e7cc | card-stats.s card_1795 pw=01689516 conf:high |
| DWORD_0806e800 | 0x00001ce4 | LP_D_TRIBE_BLOCK_OFF | ewram.inc | lp_d_tribe_off_e800 | enqueue_slot_sprites_by_card_id_scoring: D.Tribe (0x15ae) path reads [gP1LifePoints+0x1ce4] as scoring param; only 2 aligned ROM refs; conf:med |
| DWORD_0806f658 | 0x00000874 | LP_P2_LOOP_CEIL_OFF | ewram.inc | lp_p2_loop_ceil_off_f658 | 0x874 = PLAYER_BLOCK_STRIDE(0x868) + LP_LOOP_CEIL_OFF(0xc); tick_lp_zone_sprite_display_seq state 0x80 checks both [gP1LifePoints+0xc] and [gP1LifePoints+0x874] = P1 and P2 LP loop ceils; 7 aligned ROM refs; conf:high |
| DWORD_0806f40c, DWORD_0806f478 | 0x0000144c | ICID_RESERVED_D | card_info.inc | icid_reserved_d_f40c / icid_reserved_d_f478 | NOT in card-stats.s (CID 0xFFFF reserved); dispatch_hand_card_slot_sprite_by_state_and_card_id state 0x80 and 0x7e; neutral name per methodology (no card assigned); conf:high |
| DWORD_0806f420, DWORD_0806f48c | 0x00001452 | ICID_RESERVED_E | card_info.inc | icid_reserved_e_f420 / icid_reserved_e_f48c | NOT in card-stats.s (CID 0xFFFF reserved); sibling of ICID_RESERVED_D in same BST; conf:high |
| DWORD_0806fda8 | 0x0000801a | OAM_EQUIP_SPRITE_P2_1A | oam_attr.inc | oam_sprite_p2_1a_fda8 | tick_equip_chain_activation_display_seq state 0x7f: cmp r4,#0 -> 0x1a inline (P1) else 0x801a (P2); sibling of OAM_EQUIP_SPRITE_TILE_P2_1B(0x801b) and OAM_SPRITE_CODE_P1_ACTIVATION(0x8019); 119 ROM refs; conf:high |

### REF_SLOTS (USER-label + DATA-ref)

| slot | target value | gas_label | slot_label |
|------|-------------|-----------|-----------|
| DWORD_0806e7fc | 0x0201c4e0 | gP1LifePoints | gp1lp_e7fc |
| DWORD_0806e890 | 0x0201c4e0 | gP1LifePoints | gp1lp_e890 |
| DAT_0806e8b8  | 0x0201b290 | gDuelPhaseFlags | gduel_phase_e8b8 |
| DAT_0806e8bc  | 0x0806e8c0 | switchD_0806e8b6__switchdataD_0806e8c0 | switchtbl_e8bc |
| DAT_0806eab8  | 0x0201c510 | gDuelFieldSlots | gduel_slots_eab8 |
| DAT_0806eb44  | 0x0201b290 | gDuelPhaseFlags | gduel_phase_eb44 |
| PTR_gP1LifePoints_0806eb48 | 0x0201c4e0 | gP1LifePoints | gp1lp_eb48 |
| PTR_gP1LifePoints_0806eb7c | 0x0201c4e0 | gP1LifePoints | gp1lp_eb7c |
| DAT_0806ec00  | 0x0201b290 | gDuelPhaseFlags | gduel_phase_ec00 |
| PTR_gP1LifePoints_0806ec5c | 0x0201c4e0 | gP1LifePoints | gp1lp_ec5c |
| DAT_0806ed1c  | 0x0201c510 | gDuelFieldSlots | gduel_slots_ed1c |
| DAT_0806ed68  | 0x0201c510 | gDuelFieldSlots | gduel_slots_ed68 |
| DAT_0806ed6c  | 0x0201b290 | gDuelPhaseFlags | gduel_phase_ed6c |
| DWORD_0806ee50 | 0x0201c8f8 | gP1HandSlotArray | gp1hand_ee50 |
| DWORD_0806ee80 | 0x0201b290 | gDuelPhaseFlags | gduel_phase_ee80 |
| DWORD_0806eee0 | 0x0201c4e0 | gP1LifePoints | gp1lp_eee0 |
| DWORD_0806ef34 | 0x0201c4e0 | gP1LifePoints | gp1lp_ef34 |
| DWORD_0806f004 | 0x0201c510 | gDuelFieldSlots | gduel_slots_f004 |
| DWORD_0806f25c | 0x0201b290 | gDuelPhaseFlags | gduel_phase_f25c |
| DWORD_0806f2c8 | 0x0201c510 | gDuelFieldSlots | gduel_slots_f2c8 |
| DWORD_0806f38c | 0x0201c510 | gDuelFieldSlots | gduel_slots_f38c |
| DWORD_0806f3d8 | 0x0201b290 | gDuelPhaseFlags | gduel_phase_f3d8 |
| DWORD_0806f590 | 0x0201c510 | gDuelFieldSlots | gduel_slots_f590 |
| DWORD_0806f61c | 0x0201b290 | gDuelPhaseFlags | gduel_phase_f61c |
| DWORD_0806f654 | 0x0201c4e0 | gP1LifePoints | gp1lp_f654 |
| DWORD_0806f6b0 | 0x0201c4e0 | gP1LifePoints | gp1lp_f6b0 |
| DWORD_0806f730 | 0x0201c4e0 | gP1LifePoints | gp1lp_f730 |
| DWORD_0806f780 | 0x0201c4e0 | gP1LifePoints | gp1lp_f780 |
| DWORD_0806f858 | 0x0201c510 | gDuelFieldSlots | gduel_slots_f858 |
| DWORD_0806fbb0 | 0x0201b290 | gDuelPhaseFlags | gduel_phase_fbb0 |
| DWORD_0806fc90 | 0x0201c4e0 | gP1LifePoints | gp1lp_fc90 |
| DWORD_0806fd44 | 0x0201bb90 | gEquipChainSlotRefs | gequip_chain_refs_fd44 |
| DWORD_0806fd4c | 0x0201c510 | gDuelFieldSlots | gduel_slots_fd4c |
| DWORD_0806fda4 | 0x0201bb90 | gEquipChainSlotRefs | gequip_chain_refs_fda4 |

### RENAME_SLOTS (label-only rename + EOL)

The following block-start labels get renamed to reflect their content after disasm:

| slot | new_label | eol_comment |
|------|-----------|-------------|
| DAT_0806f054 | eligible_sub_stubs_f054 | THUMB dispatch sub-functions for slot-sprite dispatch table |
| DAT_0806fa08 | eligible_sub_stubs_fa08 | THUMB dispatch sub-functions for equip LP state dispatch table |
| DAT_0806fe88 | eligible_sub_stubs_fe88 | THUMB dispatch sub-functions for equip chain activation dispatch table |

### FUNC_RENAME

None. All 20 function names verified correct by body inspection (no name-body contradiction detected).

### PLATE (R5)

One stale FUN_ in existing plate text:

| function | location | old text | fix |
|----------|---------|---------|-----|
| dispatch_equip_zone_token_or_lp_sprite_by_slot_type | asm/09 line 148 | "same caller also calls FUN_0806e898" | substring replace: FUN_0806e898 -> dispatch_equip_chain_state_sprite_by_slot |

---

## Disasm Plan (R4)

All 6 blocks are DISASM. Required Ghidra actions per block:

**Block1** (0x0806f008..0x0806f03b, 0x34 bytes): fn_eligible stub for Creature Swap (CID=0x142a)
- clearListing 0x0806f008..0x0806f03b
- setTMode(0x0806f008, THUMB)
- DisassembleCommand(0x0806f008)
- Label: `eligible_creature_swap_f008`
- EOL at 0x0806f008: `fn_eligible stub: Creature Swap (CID=0x142a); FS table THUMB+1 ref @0x1e40958`

**Block2** (0x0806f054..0x0806f1c7, 0x174 bytes): raw dispatch sub-stubs (6 entry points)
- clearListing 0x0806f054..0x0806f1c7
- setTMode(0x0806f054, THUMB)
- DisassembleCommand per stub: 0x0806f054, 0x0806f066, 0x0806f078, 0x0806f0ac, 0x0806f0cc, 0x0806f188
- Labels: `equip_disp_sub_f054`, `equip_disp_sub_f066`, `equip_disp_sub_f078`, `equip_disp_sub_f0ac`, `equip_disp_sub_f0cc`, `equip_disp_sub_f188`
- Dispatch table at 0x0806f03c (label: `equip_disp_table_f03c`, 6 .word entries)

**Block3** (0x0806f85c..0x0806f993, 0x138 bytes): fn_eligible stub for Destiny Board (CID=0x1468)
- clearListing 0x0806f85c..0x0806f993
- setTMode(0x0806f85c, THUMB)
- DisassembleCommand(0x0806f85c) [main stub]; check for additional sub-stubs within range
- Label: `eligible_destiny_board_f85c`
- EOL at 0x0806f85c: `fn_eligible stub: Destiny Board (CID=0x1468); 2x FS table THUMB+1 ref @0x1e40a90+0x1e43a30`

**Block4** (0x0806fa08..0x0806fb87, 0x180 bytes): raw dispatch sub-stubs (10 entry points)
- clearListing 0x0806fa08..0x0806fb87
- setTMode(0x0806fa08, THUMB)
- DisassembleCommand per stub: 0x0806fa08, 0x0806fa4c, 0x0806fa5e, 0x0806fa74, 0x0806fb14, 0x0806fb4c, 0x0806fb58, 0x0806fb64, 0x0806fb70, 0x0806fb76
- Labels: `equip_lp_sub_fa08`, `equip_lp_sub_fa4c`, `equip_lp_sub_fa5e`, `equip_lp_sub_fa74`, `equip_lp_sub_fb14`, `equip_lp_sub_fb4c`, `equip_lp_sub_fb58`, `equip_lp_sub_fb64`, `equip_lp_sub_fb70`, `equip_lp_sub_fb76`
- Dispatch table at 0x0806f994 (label: `equip_lp_disp_table_f994`, 29 .word entries)

**Block5** (0x0806fdec..0x0806fe13, 0x28 bytes): fn_eligible stub for Cathedral of Nobles (CID=0x146f)
- clearListing 0x0806fdec..0x0806fe13
- setTMode(0x0806fdec, THUMB)
- DisassembleCommand(0x0806fdec)
- Label: `eligible_cathedral_of_nobles_fdec`
- EOL at 0x0806fdec: `fn_eligible stub: Cathedral of Nobles (CID=0x146f); 2x FS table THUMB+1 ref @0x1e46610; false-positive at 0x3d3eb6 (compressed data)`

**Block6** (0x0806fe88..0x0806ff4f, 0xc8 bytes): raw dispatch sub-stubs (8 entry points)
- clearListing 0x0806fe88..0x0806ff4f
- setTMode(0x0806fe88, THUMB)
- DisassembleCommand per stub: 0x0806fe88, 0x0806fedc, 0x0806fef0, 0x0806ff0a, 0x0806ff1a, 0x0806ff2c, 0x0806ff3c, 0x0806ff46
- Labels: `equip_chain_act_sub_fe88`, `equip_chain_act_sub_fedc`, `equip_chain_act_sub_fef0`, `equip_chain_act_sub_ff0a`, `equip_chain_act_sub_ff1a`, `equip_chain_act_sub_ff2c`, `equip_chain_act_sub_ff3c`, `equip_chain_act_sub_ff46`
- Dispatch table at 0x0806fe14 (label: `equip_chain_act_disp_table_fe14`, 29 .word entries)

---

## Carve Plan (R7)

None. No ROM data table with structured content requiring carve into rom.s. All ROM_INCBIN blocks are THUMB code (disasm only). Dispatch tables are already structured as inline .word entries in the asm file.

---

## New Constants / Globals

**card_info.inc additions:**
```
.equ BIG_MARCH_OF_ANIMALS_CID,  0x00001882  @ The Big March of Animals (card_1795 pw=01689516); enqueue_slot_sprites_by_card_id_scoring scoring branch; conf:high
.equ ICID_RESERVED_D,           0x0000144c  @ reserved internal CID (CID=0xFFFF, not in card-stats.s); dispatch_hand_card_slot_sprite_by_state_and_card_id BST; conf:high
.equ ICID_RESERVED_E,           0x00001452  @ reserved internal CID (CID=0xFFFF, not in card-stats.s); sibling of ICID_RESERVED_D in same BST; conf:high
.equ CREATURE_SWAP_CID,         0x0000142a  @ Creature Swap (card_0910 pw=31036355); Block1 FS handler fn_eligible CID=0x142a; conf:high
```

Note: CREATURE_SWAP_CID is referenced only as the FS table CID for Block1's fn_eligible stub, not directly as a literal pool slot within Seg-1 code. Adding for completeness and future use.

**ewram.inc additions:**
```
.equ LP_D_TRIBE_BLOCK_OFF,  0x00001ce4  @ [gP1LifePoints+0x1ce4] D.Tribe LP score field; enqueue_slot_sprites_by_card_id_scoring D_TRIBE_CID(0x15ae) path reads dword here as scoring param; adjacent to P1LP_BLOCK2_OFF_1CE8(0x1ce8)-4; 2 aligned ROM refs; conf:med
.equ LP_P2_LOOP_CEIL_OFF,   0x00000874  @ [gP1LifePoints+0x874] P2 LP loop ceiling = PLAYER_BLOCK_STRIDE(0x868) + LP_LOOP_CEIL_OFF(0xc); tick_lp_zone_sprite_display_seq state 0x80 reads P2 ceil at this offset; 7 aligned ROM refs; conf:high
```

**oam_attr.inc addition:**
```
.equ OAM_EQUIP_SPRITE_P2_1A,  0x0000801a  @ equip sprite OAM attr0 P2 (bit15+0x1a); tick_equip_chain_activation_display_seq state 0x7f: P2 path uses 0x801a, P1 inline 0x1a; sibling of OAM_EQUIP_SPRITE_TILE_P2_1B(0x801b) and OAM_SPRITE_CODE_P1_ACTIVATION(0x8019); 119 ROM refs; conf:high
```

---

## Section 5.1 Registration (Rule 3) -- 0-reference blocks

None. All 6 ROM_INCBIN blocks have confirmed references (THUMB+1 from FS table or raw from same-segment dispatch table). No 0-reference orphan blocks in Seg-1.

---

## Consumer Evidence (R6)

Key slot semantics with file:line + confidence:

| slot | semantic | consumer | file:line | conf |
|------|---------|---------|---------|------|
| DWORD_0806e800 = 0x1ce4 | LP field for D.Tribe score | enqueue_slot_sprites_by_card_id_scoring D.Tribe(0x15ae) branch: ldr r0,DWORD_0806e7fc; ldr r1,DWORD_0806e800; adds r0,r0,r1; ldr r2,[r0,0] -> r2 used as scoring param to enqueue_slot_card_sprite_if_eligible | asm/09 L105-114 | med |
| DWORD_0806f658 = 0x874 | P2 LP loop ceil field offset | tick_lp_zone_sprite_display_seq state 0x80: ldr r1,DWORD_0806f654(=gP1LifePoints); ldr r3,DWORD_0806f658; adds r0,r1,r3; ldr r0,[r0,0]; cmp r0,0 -- guards LP row type5 setup | asm/09 L1962-1970 | high |
| DWORD_0806fda8 = 0x801a | P2 equip chain sprite code | tick_equip_chain_activation_display_seq state 0x7f: movs r0,0x1a; cmp r4,0; beq skip; ldr r0,DWORD_0806fda8 -- r0 passed to enqueue_sprite_attr_record | asm/09 L2580-2590 | high |
| Block1 stub (0x806f008) | fn_eligible for Creature Swap | FS handler table @0x1e40958: entry [CID=0x142a, fn_activate=..., fn_eligible+1=0x0806f009] | roms/2343.gba @0x1e40958 | high |
| Block3 stub (0x806f85c) | fn_eligible for Destiny Board | FS handler table @0x1e40a90 and @0x1e43a30: both CID=0x1468 | roms/2343.gba @0x1e40a90 | high |
| Block5 stub (0x806fdec) | fn_eligible for Cathedral of Nobles | FS handler table @0x1e46610: CID=0x146f | roms/2343.gba @0x1e46610 | high |
| DAT_0806e8bc = 0x0806e8c0 | switchD table pointer | dispatch_equip_chain_state_sprite_by_slot: ldr r1,DAT_0806e8bc; adds r0,r0,r1; ldr r0,[r0,0]; bx r0 -- jump via switchD | asm/09 L229-232 | high |

---

## Clarification Requests

None. All semantics confirmed by consumer evidence or by inspection.

---

## Self-check Results

1. All EQ values verified by python struct.unpack_from('<I', rom, offset)[0] against stated values -- confirmed matching.
2. All THUMB+1 pointer table entries verified: CID at entry_off-4 checked for each FS table ref.
3. No CJK characters in any plate/EOL text in this proposal (ASCII only).
4. Section 5.1 has 0 entries; all 6 blocks have confirmed references (no misclassification).
5. Slot labels follow ^[a-z][a-z0-9_]+$ pattern throughout.
6. C5 dedup: all new equates grepped with value check against all constants/*.inc -- none already exist.
