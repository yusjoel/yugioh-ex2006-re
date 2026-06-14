# Refine Proposal: F06-Seg-9  [0x08059de0..0x0805b480)

## Recommended split: Seg-9a / Seg-9b

Seg-9 has 147 unique label definitions (above the ~120 threshold). Recommended split at
function boundary `check_card_zone_activation_blocked` (0x0805a570, line 16814):

- **Seg-9a**: `[0x08059de0, 0x0805a570)` -- 13 named fn + 1 Block1 fn (disasm) = 34 slots
- **Seg-9b**: `[0x0805a570, 0x0805b480)` -- 9 named fn + 5 Block2 sub-fn (disasm) = 113 slots

This proposal covers the full Seg-9 range; the fixer may elect to land in two passes.

---

## Segment survey

### Function entries (23 named)

| addr | name | line |
|------|------|------|
| 0x08059de0 | tick_equip_zone14_activation_display_seq | L15895 |
| 0x08059e94 | update_equip_slot_entity_id_cache | L15995 |
| 0x08059ec0 | tick_equip_type_category_sprite_display_seq | L16029 |
| 0x08059f2c | tick_equip_effect_slot_display_seq | L16095 |
| 0x08059fc4 | tick_equip_activation_if_pair_eligible | L16177 |
| 0x0805a00c | enqueue_equip_zone_sprite_with_neg_attr | L16223 |
| 0x0805a030 | tick_equip_banisher_field_count_display_seq | L16251 |
| 0x0805a1dc | tick_equip_activation_sprite_mode2_by_type | L16328 |
| 0x0805a204 | check_neo_daedalus_placement_eligible_for_slot | L16357 |
| 0x0805a238 | check_spell_zone_slot_face_down | L16386 |
| 0x0805a280 | setup_equip_context_for_slot_activation | L16428 |
| 0x0805a354 | setup_equip_context_for_zone_activation | L16537 |
| 0x0805a3e0 | eval_equip_activation_for_slot | L16608 |
| 0x0805a570 | check_card_zone_activation_blocked | L16814 |
| 0x0805a86c | check_equip_card_can_target_partner | L17211 |
| 0x0805a9a8 | check_card_placement_rules | L17375 |
| 0x0805aea4 | apply_card_equip_activation | L18020 |
| 0x0805b034 | build_zone_activation_entry_equip | L18217 |
| 0x0805b0cc | build_zone_activation_entry_blocked | L18294 |
| 0x0805b164 | invoke_equip_zone_activation_check | L18371 |
| 0x0805b1f0 | apply_equip_activation_via_packed_attr | L18442 |
| 0x0805b2a4 | dispatch_card_effect_by_stat_type | L18533 |
| 0x0805b480 | find_zone_slot_match_by_type_in_node_list | L18794 (Seg-10 start) |

### Residual auto-name slots: 147 unique label definitions

Top repeated values (by address-deduplicated count):
- `0x00000868` (PLAYER_BLOCK_STRIDE) x13
- `0x0201b290` (gDuelPhaseFlags) x8
- `0x0201e2a0` (gDuelCardCtxBase) x8
- `0x00001d78` (ACTIVATION_STATE_B_OFF) x8
- `0x0201c510` (gDuelFieldSlots) x6
- `0xffff803f` (SCROLLBAR_CLEAR_BITS_14_6) x6
- `0xfffff03f` (OAM_ATTR2_CLR_BITS_11_6) x6
- `0x000004ac` (EQUIP_ACTIVATION_STEP_OFF) x4
- `0x000004cc` (LP_BAR_ANIM_STATE_OFF) x4
- ... and 20 unique CID values in `dispatch_card_effect_by_stat_type`

### ROM_INCBIN / .byte blocks

- Block1: `ROM_INCBIN 0x5a0aa, 0x36` at line 16316 (gap before dispatch table)
- Block2: `DAT_0805a0f8: ROM_INCBIN 0x5a0f8, 0xe4` at line 16324 (5 state sub-functions)

Note: the 5-entry dispatch table `PTR_DAT_0805a0e4` at lines 16318-16323 is BETWEEN Block1
and Block2 and is already decoded asm (.word directives), not inside either incbin.

---

## Data block classification (Rule 2/3) -- ref-scan evidence

| block | ROM range | ref-scan (raw / THUMB+1) | verdict | reason |
|-------|-----------|--------------------------|---------|--------|
| Block1 | 0x5a0aa..0x5a0df (0x36B) | raw=0, THUMB+1=2 at 0x9e42ca4+0x9e42f74 (-> 0x0805a0ad) | **R4 DISASM** | 2 THUMB+1 refs from CID dispatch table entries (CID 0x195c/0x19b1); start at 0x5a0ac (2-byte align pad at 0x5a0aa); `push {r4,r5,lr}` @ 0x0805a0ac |
| Block2 | 0x5a0f8..0x5a1db (0xe4B) | raw=5 (exactly the 5 dispatch table entries at 0x5a0e4..0x5a0f7); THUMB+1=0 | **R4 DISASM** | 5 raw-ptr refs from `PTR_DAT_0805a0e4` dispatch table (state0-4 handlers); first hwords are BL prefix 0xf7f0 / ldrb 0x78a4 / BL prefix 0xf03c -- THUMB code |

ref-scan python (2-byte-step):
```python
import struct; rom=open('roms/2343.gba','rb').read()
for a in [0x0805a0aa, 0x0805a0ac, 0x0805a0f8, 0x0805a118, 0x0805a134, 0x0805a148, 0x0805a1cc]:
    for v in (a, a|1):
        c = rom.count(struct.pack('<I', v))
        if c: print(hex(v), c)
```
Results confirmed:
- `0x0805a0ad` (Block1 fn|1): 2 hits
- `0x0805a0f8`, `0x0805a118`, `0x0805a134`, `0x0805a148`, `0x0805a1cc`: 1 hit each (raw, in dispatch table)

**Section 5.1 = 0** (both blocks have references, no orphan blocks).

---

## Symbolization plan (R1/R2/R3)

### EQ_SLOTS (data-equate; reuse existing inc)

All entries below reuse existing constants -- no new constants needed for these values.

**Seg-9a (34 slots)**:

| slot addr | line | value | const_name | inc file | slot_label |
|-----------|------|-------|------------|----------|------------|
| DWORD_08059dfc | L15910 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | gDuelPhaseFlags_15910 |
| DWORD_08059e00 | L15912 | 0x000004ac | EQUIP_ACTIVATION_STEP_OFF | duel_field.inc | equip_activation_step_off_15912 |
| DWORD_08059e2c | L15934 | 0x080905e9 | -- (REF_SLOT) | -- | see REF_SLOTS |
| DWORD_08059e5c | L15957 | 0x0201c4e0 | gP1LifePoints | ewram.inc | -- (already PTR_gP1LifePoints_* rename) |
| DWORD_08059e60 | L15959 | 0x00001d68 | ELIGIB_SPRITE_CTRL_OFF | ewram.inc | eligib_sprite_ctrl_off_15959 |
| DWORD_08059e64 | L15961 | 0x00001d6c | ELIGIB_ANIM_STATE_OFF | ewram.inc | eligib_anim_state_off_15961 |
| DAT_08059efc | L16059 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | gDuelPhaseFlags_16059 |
| DAT_08059f00 | L16061 | 0x000004ac | EQUIP_ACTIVATION_STEP_OFF | duel_field.inc | equip_activation_step_off_16061 |
| DAT_08059f48 | L16110 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | gDuelPhaseFlags_16110 |
| DAT_08059f4c | L16112 | 0x000004ac | EQUIP_ACTIVATION_STEP_OFF | duel_field.inc | equip_activation_step_off_16112 |
| DAT_08059fdc | L16190 | 0x0000190a | DARK_RULER_VANDALGYON_CID | card_info.inc | dark_ruler_vandalgyon_cid_16190 |
| DWORD_0805a048 | L16264 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | gDuelPhaseFlags_16264 |
| DWORD_0805a04c | L16266 | 0x000004ac | EQUIP_ACTIVATION_STEP_OFF | duel_field.inc | equip_activation_step_off_16266 |
| DWORD_0805a090 | L16300 | 0x0201c4e0 | gP1LifePoints | ewram.inc | -- (PTR_gP1LifePoints_* rename) |
| DWORD_0805a094 | L16302 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | player_block_stride_16302 |
| PTR_DAT_0805a0e4 | L16318 | 0x0805a0f8 | -- | -- | tick_bonding_photon_state_table (see carve/disasm plan) |
| DAT_0805a0f8 | L16324 | 0xfb38f7f0 | -- | -- | (Block2 first sub-fn; see disasm plan) |
| DAT_0805a274 | L16418 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | player_block_stride_16418 |
| DAT_0805a2c0 | L16460 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | player_block_stride_16460 |
| DAT_0805a2c4 | L16462 | 0x0201c510 | gDuelFieldSlots | ewram.inc | gDuelFieldSlots_16462 |
| DAT_0805a338 | L16520 | 0xffff803f | SCROLLBAR_CLEAR_BITS_14_6 | gl_scrollbar.inc | scrollbar_clr_bits14_6_16520 |
| DAT_0805a3d4 | L16600 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | player_block_stride_16600 |
| DAT_0805a3d8 | L16602 | 0x0201c600 | gP1FieldArrayCBase | ewram.inc | gP1FieldArrayCBase_16602 |
| DAT_0805a3dc | L16604 | 0xffff803f | SCROLLBAR_CLEAR_BITS_14_6 | gl_scrollbar.inc | scrollbar_clr_bits14_6_16604 |

Note on `SCROLLBAR_CLEAR_BITS_14_6`: In `setup_equip_context_for_slot_activation` /
`setup_equip_context_for_zone_activation`, 0xffff803f is used to clear bits[14:6] of an
OAM sprite attr halfword -- same bit-field as the scrollbar range_param 9-bit field.
The equate name is correct for the mask value even in OAM context (same bit positions).
Confidence: high (asm/00_system_str_vija.s gl_scrollbar.inc; 6 hits in Seg-9 confirmed
against ROM raw bytes via python struct.pack('<I', 0xffff803f)).

**Seg-9b (113 slots)**:

| slot addr | line | value | const_name | inc file | slot_label |
|-----------|------|-------|------------|----------|------------|
| DAT_0805a4b0 | L16712 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc | gDuelCardCtxBase_16712 |
| DAT_0805a4b8 | L16718 | 0x00001d78 | ACTIVATION_STATE_B_OFF | duel_field.inc | activation_state_b_off_16718 |
| DAT_0805a4bc | L16718 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | player_block_stride_16718b |
| DAT_0805a4c0 | L16720 | 0x0201c510 | gDuelFieldSlots | ewram.inc | gDuelFieldSlots_16720 |
| DAT_0805a4c4 | L16722 | 0x0000ffff | SLOT_CARD_EMPTY | card_info.inc | slot_card_empty_16722 |
| DAT_0805a4fc | L16751 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | gDuelPhaseFlags_16751 |
| DAT_0805a500 | L16753 | 0x000004cc | LP_BAR_ANIM_STATE_OFF | ewram.inc | lp_bar_anim_state_off_16753 |
| DAT_0805a564 | L16806 | 0x000004f4 | CHAIN_NODE_CARD_ARR_OFF | ewram.inc | chain_node_card_arr_off_16806 |
| DAT_0805a568 | L16808 | 0x000004d4 | SPRITE_ROW_ENTRY_DATA_OFF | ewram.inc | sprite_row_entry_data_off_16808 |
| DAT_0805a56c | L16810 | 0xfffff03f | OAM_ATTR2_CLR_BITS_11_6 | oam_attr.inc | oam_attr2_clr_bits11_6_16810 |
| DAT_0805a5ec | L16881 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc | gDuelCardCtxBase_16881 |
| DAT_0805a5f4 | L16885 | 0x00001d78 | ACTIVATION_STATE_B_OFF | duel_field.inc | activation_state_b_off_16885 |
| DAT_0805a5f8 | L16887 | 0x00000fee | COCOON_OF_EVOLUTION_CID | card_info.inc | cocoon_of_evolution_cid_16887 |
| DAT_0805a640 | L16924 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc | p1lp_block2_off_1ce8_16924 |
| DAT_0805a644 | L16926 | 0x00001390 | ANTI_SPELL_FRAGRANCE_CID | card_info.inc (new) | anti_spell_fragrance_cid_16926 |
| DAT_0805a6dc | L17005 | 0x000014a5 | MAKYURA_THE_DESTRUCTOR_CID | card_info.inc | makyura_the_destructor_cid_17005 |
| DAT_0805a6e0 | L17007 | 0x0000198a | BUBBLE_ILLUSION_CID | card_info.inc | bubble_illusion_cid_17007 |
| DAT_0805a6e4 | L17009 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | gDuelPhaseFlags_17009 |
| DAT_0805a6e8 | L17011 | 0x000004cc | LP_BAR_ANIM_STATE_OFF | ewram.inc | lp_bar_anim_state_off_17011 |
| DAT_0805a6ec | L17013 | 0x0201bb90 | gEquipChainSlotRefs | ewram.inc | gEquipChainSlotRefs_17013 |
| DAT_0805a6f0 | L17015 | 0x000004d4 | SPRITE_ROW_ENTRY_DATA_OFF | ewram.inc | sprite_row_entry_data_off_17015 |
| DAT_0805a6f4 | L17017 | 0x000018f5 | cid_18f5 (no card-stats.s entry; low-conf neutral label) | -- | cid_18f5_17017 |
| DAT_0805a790 | L17096 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | player_block_stride_17096 |
| DAT_0805a794 | L17098 | 0x0201c510 | gDuelFieldSlots | ewram.inc | gDuelFieldSlots_17098 |
| DAT_0805a798 | L17100 | 0x0000146f | CATHEDRAL_OF_NOBLES_CID | card_info.inc | cathedral_of_nobles_cid_17100 |
| DAT_0805a79c | L17102 | 0x00001d48 | ACTIVATION_STATE_A_OFF | duel_field.inc | activation_state_a_off_17102 |
| DAT_0805a7c4 | L17122 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc | gDuelCardCtxBase_17122 |
| DAT_0805a7cc | L17126 | 0x00001d78 | ACTIVATION_STATE_B_OFF | duel_field.inc | activation_state_b_off_17126 |
| DAT_0805a7f8 | L17148 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | gDuelPhaseFlags_17148 |
| DAT_0805a7fc | L17150 | 0x000004cc | LP_BAR_ANIM_STATE_OFF | ewram.inc | lp_bar_anim_state_off_17150 |
| DAT_0805a860 | L17203 | 0x000004f4 | CHAIN_NODE_CARD_ARR_OFF | ewram.inc | chain_node_card_arr_off_17203 |
| DAT_0805a864 | L17205 | 0x000004d4 | SPRITE_ROW_ENTRY_DATA_OFF | ewram.inc | sprite_row_entry_data_off_17205 |
| DAT_0805a868 | L17207 | 0xfffff03f | OAM_ATTR2_CLR_BITS_11_6 | oam_attr.inc | oam_attr2_clr_bits11_6_17207 |
| DAT_0805a908 | L17287 | 0x0000131e | -- (special equip-target CID sentinel) | -- | special_equip_target_cid_a_17287 |
| DAT_0805a90c | L17289 | 0x000014d7 | SPIRIT_RYU_CID | card_info.inc (new) | spirit_ryu_cid_17289 |
| DAT_0805a910 | L17291 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc | gDuelCardCtxBase_17291 |
| DAT_0805a918 | L17295 | 0x00001d78 | ACTIVATION_STATE_B_OFF | duel_field.inc | activation_state_b_off_17295 |
| DAT_0805a94c | L17323 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc | p1lp_block2_off_1ce8_17323 |
| DAT_0805a950 | L17325 | 0x00001cf4 | FIELD_STATE_OFF | duel_field.inc | field_state_off_17325 |
| DAT_0805a954 | L17327 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc | gDuelCardCtxBase_17327 |
| DAT_0805a958 | L17329 | 0x00001d78 | ACTIVATION_STATE_B_OFF | duel_field.inc | activation_state_b_off_17329 |
| DAT_0805a994 | L17361 | 0x000010d0 | EFFECT_ZONE_BITMASK_OFF | duel_field.inc | effect_zone_bitmask_off_17361 |
| DAT_0805a998 | L17363 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc | gDuelCardCtxBase_17363 |
| DAT_0805a99c | L17365 | 0x00001d78 | ACTIVATION_STATE_B_OFF | duel_field.inc | activation_state_b_off_17365 |
| DAT_0805aa5c | L17465 | 0x00001407 | FIELD_SPELL_B_EFFECT_ID | card_info.inc | field_spell_b_effect_id_17465 |
| DAT_0805aa60 | L17467 | 0x000019ae | ANCIENT_GEAR_DRILL_CID | card_info.inc | ancient_gear_drill_cid_17467 |
| DAT_0805aa64 | L17469 | 0x00001944 | LEVEL_MODULATION_CID | card_info.inc (new) | level_modulation_cid_17469 |
| DAT_0805aaf8 | L17543 | 0x00001944 | LEVEL_MODULATION_CID | card_info.inc (new) | level_modulation_cid_17543 |
| DAT_0805ab00 | L17547 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc | p1lp_block2_off_1ce8_17547 |
| DAT_0805ab04 | L17549 | 0x000015ff | DIFFUSION_WAVE_MOTION_CID | card_info.inc | diffusion_wave_motion_cid_17549 |
| DAT_0805ab08 | L17551 | 0x0000148e | ROYAL_COMMAND_CID | card_info.inc | royal_command_cid_17551 |
| DAT_0805ab0c | L17553 | 0x0000188e | FORCED_CEASEFIRE_CID | card_info.inc | forced_ceasefire_cid_17553 |
| DAT_0805ab10 | L17555 | 0x00001684 | cid_1684 (no card-stats.s entry; low-conf neutral label) | -- | cid_1684_17555 |
| DAT_0805ab14 | L17557 | 0x00001679 | JUDGEMENT_OF_PHARAOH_CID | card_info.inc | judgement_of_pharaoh_cid_17557 |
| DAT_0805abf0 | L17670 | 0x00001679 | JUDGEMENT_OF_PHARAOH_CID | card_info.inc | judgement_of_pharaoh_cid_17670 |
| DAT_0805abf8 | L17674 | 0x00001cf4 | FIELD_STATE_OFF | duel_field.inc | field_state_off_17674 |
| DAT_0805abfc | L17676 | 0x0000178b | PROTECTOR_OF_THE_SANCTUARY_CID | card_info.inc | protector_of_sanctuary_cid_17676 |
| DAT_0805ac00 | L17678 | 0x00001296 | JINZO_CID | card_info.inc | jinzo_cid_17678 |
| DAT_0805ac04 | L17680 | 0x000012d3 | AMPLIFIER_CID | card_info.inc | amplifier_cid_17680 |
| DAT_0805ae2c | L17955 | 0x000015da | SPELL_CANCELLER_CID | card_info.inc (new) | spell_canceller_cid_17955 |
| DAT_0805ae30 | L17957 | 0x000018ab | ANCIENT_GEAR_GOLEM_CID | card_info.inc | ancient_gear_golem_cid_17957 |
| DAT_0805ae34 | L17959 | 0x00001390 | ANTI_SPELL_FRAGRANCE_CID | card_info.inc (new) | anti_spell_fragrance_cid_17959 |
| DAT_0805ae38 | L17961 | 0x000013bd | SONIC_JAMMER_CID | card_info.inc | sonic_jammer_cid_17961 |
| DAT_0805ae40 | L17965 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | player_block_stride_17965 |
| DAT_0805ae44 | L17967 | 0x00001910 | MECHANICAL_HOUND_CID | card_info.inc (new) | mechanical_hound_cid_17967 |
| DAT_0805ae48 | L17969 | 0x00001722 | INVADER_OF_DARKNESS_CID | card_info.inc (new) | invader_of_darkness_cid_17969 |
| DAT_0805ae4c | L17971 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | gDuelPhaseFlags_17971 |
| DAT_0805ae50 | L17973 | 0x000004cc | LP_BAR_ANIM_STATE_OFF | ewram.inc | lp_bar_anim_state_off_17973 |
| DAT_0805ae54 | L17975 | 0x000004f4 | CHAIN_NODE_CARD_ARR_OFF | ewram.inc | chain_node_card_arr_off_17975 |
| DAT_0805ae58 | L17977 | 0x00001832 | CREEPING_DOOM_MANTA_CID | card_info.inc (new) | creeping_doom_manta_cid_17977 |
| DAT_0805ae5c | L17979 | 0x00001cf4 | FIELD_STATE_OFF | duel_field.inc | field_state_off_17979 |
| DAT_0805ae60 | L17981 | 0x00001833 | PITCH_BLACK_WARWOLF_CID | card_info.inc (new) | pitch_black_warwolf_cid_17981 |
| DAT_0805ae64 | L17983 | 0x00001834 | MIRAGE_DRAGON_CID | card_info.inc (new) | mirage_dragon_cid_17983 |
| DAT_0805ae68 | L17985 | 0x000019bb | ANCIENT_GEAR_CANNON_CID | card_info.inc (new) | ancient_gear_cannon_cid_17985 |
| DAT_0805ae6c | L17987 | 0x0000184a | XING_ZHEN_HU_CID | card_info.inc | xing_zhen_hu_cid_17987 |
| DAT_0805ae70 | L17989 | 0x00001664 | FAIRY_OF_THE_SPRING_CID | card_info.inc (new) | fairy_of_the_spring_cid_17989 |
| DAT_0805ae74 | L17991 | 0x000016dd | CURSED_SEAL_FORBIDDEN_SPELL_CID | card_info.inc (new) | cursed_seal_forbidden_spell_cid_17991 |
| DAT_0805ae98 | L18012 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc | gDuelCardCtxBase_18012 |
| DAT_0805aea0 | L18016 | 0x00001d78 | ACTIVATION_STATE_B_OFF | duel_field.inc | activation_state_b_off_18016 |
| DAT_0805af50 | L18105 | 0x000019a3 | -- (special_equip_id; no card-stats entry) | -- | special_equip_sentinel_id_18105 |
| DAT_0805af54 | L18107 | 0x0000132c | CHAIN_ENERGY_CID | card_info.inc | chain_energy_cid_18107 |
| DAT_0805af5c | L18111 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | player_block_stride_18111 |
| DAT_0805af60 | L18113 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc | gDuelCardCtxBase_18113 |
| DAT_0805af64 | L18115 | 0x00001d78 | ACTIVATION_STATE_B_OFF | duel_field.inc | activation_state_b_off_18115 |
| DAT_0805b014 | L18198 | 0x0000303e | -- (zone_code combined mask; new) | -- | zone_code_mask_303e_18198 |
| DAT_0805b018 | L18200 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | player_block_stride_18200 |
| DAT_0805b0bc | L18284 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | player_block_stride_18284 |
| DAT_0805b0c0 | L18286 | 0x0201c510 | gDuelFieldSlots | ewram.inc | gDuelFieldSlots_18286 |
| DAT_0805b0c4 | L18288 | 0xffff803f | SCROLLBAR_CLEAR_BITS_14_6 | gl_scrollbar.inc | scrollbar_clr_bits14_6_18288 |
| DAT_0805b0c8 | L18290 | 0xfffff03f | OAM_ATTR2_CLR_BITS_11_6 | oam_attr.inc | oam_attr2_clr_bits11_6_18290 |
| DAT_0805b154 | L18361 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | player_block_stride_18361 |
| DAT_0805b158 | L18363 | 0x0201c510 | gDuelFieldSlots | ewram.inc | gDuelFieldSlots_18363 |
| DAT_0805b15c | L18365 | 0xffff803f | SCROLLBAR_CLEAR_BITS_14_6 | gl_scrollbar.inc | scrollbar_clr_bits14_6_18365 |
| DAT_0805b160 | L18367 | 0xfffff03f | OAM_ATTR2_CLR_BITS_11_6 | oam_attr.inc | oam_attr2_clr_bits11_6_18367 |
| DAT_0805b1e0 | L18432 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | player_block_stride_18432 |
| DAT_0805b1e4 | L18434 | 0x0201c600 | gP1FieldArrayCBase | ewram.inc | gP1FieldArrayCBase_18434 |
| DAT_0805b1e8 | L18436 | 0xffff803f | SCROLLBAR_CLEAR_BITS_14_6 | gl_scrollbar.inc | scrollbar_clr_bits14_6_18436 |
| DAT_0805b1ec | L18438 | 0xfffff03f | OAM_ATTR2_CLR_BITS_11_6 | oam_attr.inc | oam_attr2_clr_bits11_6_18438 |
| DAT_0805b298 | L18525 | 0xfffff03f | OAM_ATTR2_CLR_BITS_11_6 | oam_attr.inc | oam_attr2_clr_bits11_6_18525 |
| DAT_0805b29c | L18527 | 0x000001ff | OAM_ATTR1_X_MASK | oam_attr.inc | oam_attr1_x_mask_18527 |
| DAT_0805b2a0 | L18529 | 0xffff803f | SCROLLBAR_CLEAR_BITS_14_6 | gl_scrollbar.inc | scrollbar_clr_bits14_6_18529 |
| DAT_0805b2f0 | L18572 | 0x00001909 | SPARK_BLASTER_CID | card_info.inc | spark_blaster_cid_18572 |
| DAT_0805b318 | L18593 | 0x00001432 | GROUND_COLLAPSE_FIELD_CARD_ID | card_info.inc | ground_collapse_field_card_id_18593 |
| DAT_0805b31c | L18595 | 0x00001243 | SHADOW_SPELL_CID | card_info.inc (new) | shadow_spell_cid_18595 |
| DAT_0805b320 | L18597 | 0x00001103 | SPELLBINDING_CIRCLE_CID | card_info.inc (new) | spellbinding_circle_cid_18597 |
| DAT_0805b324 | L18599 | 0x00000fee | COCOON_OF_EVOLUTION_CID | card_info.inc | cocoon_of_evolution_cid_18599 |
| DAT_0805b334 | L18608 | 0x00001231 | KUNAI_WITH_CHAIN_CID | card_info.inc | kunai_with_chain_cid_18608 |
| DAT_0805b348 | L18619 | 0x000012de | DARK_MAGIC_CURTAIN_CID | card_info.inc | dark_magic_curtain_cid_18619 |
| DAT_0805b358 | L18628 | 0x000013eb | EQUIP_ZONE_BLOCKER_CID | card_info.inc | equip_zone_blocker_cid_18628 |
| DAT_0805b374 | L18643 | 0x00001710 | STRAY_LAMBS_CID | card_info.inc (new) | stray_lambs_cid_18643 |
| DAT_0805b378 | L18645 | 0x00001514 | BLAST_WITH_CHAIN_CID | card_info.inc | blast_with_chain_cid_18645 |
| DAT_0805b388 | L18654 | 0x0000166c | SKILL_DRAIN_CID | card_info.inc | skill_drain_cid_18654 |
| DAT_0805b3a4 | L18670 | 0x0000184b | RARE_METALMORPH_CID | card_info.inc | rare_metalmorph_cid_18670 |
| DAT_0805b3a8 | L18672 | 0x0000173f | AGENT_OF_JUDGMENT_SATURN_CID | card_info.inc (new) | agent_of_judgment_saturn_cid_18672 |
| DAT_0805b3e8 | L18706 | 0x000018d3 | IMPENETRABLE_FORMATION_CID | card_info.inc (new) | impenetrable_formation_cid_18706 |
| DAT_0805b3ec | L18708 | 0x0000150d | SMOKE_GRENADE_OF_THIEF_CID | card_info.inc (new) | smoke_grenade_of_thief_cid_18708 |
| DAT_0805b3f0 | L18710 | 0x00001232 | MAGICAL_LABYRINTH_CID | card_info.inc | magical_labyrinth_cid_18710 |
| DAT_0805b3f4 | L18712 | 0x0000146f | CATHEDRAL_OF_NOBLES_CID | card_info.inc | cathedral_of_nobles_cid_18712 |
| DAT_0805b408 | L18723 | 0x000017af | THE_FIRST_SARCOPHAGUS_CID | card_info.inc | the_first_sarcophagus_cid_18723 |
| DAT_0805b40c | L18725 | 0x000015ee | WAVE_MOTION_CANNON_CID | card_info.inc (new) | wave_motion_cannon_cid_18725 |
| DAT_0805b474 | L18781 | 0x000019d8 | TRIAL_OF_THE_PRINCESSES_CID | card_info.inc (new) | trial_of_the_princesses_cid_18781 |
| DAT_0805b478 | L18783 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | player_block_stride_18783 |
| DAT_0805b47c | L18785 | 0x0201c510 | gDuelFieldSlots | ewram.inc | gDuelFieldSlots_18785 |

### REF_SLOTS (USER-label + DATA-ref)

These slots hold THUMB fn-ptr values (addr|1); rename to fn-label reference.

| slot addr | line | raw value | target fn | gas_expr | slot_label |
|-----------|------|-----------|-----------|----------|------------|
| DWORD_08059e2c | L15934 | 0x080905e9 | set_equip_activation_state_by_mode_alt (asm/11, 0x080905e8) | .word set_equip_activation_state_by_mode_alt+1 | set_equip_activation_state_mode_alt_ptr_15934 |

Verify: 0x080905e8|1 = 0x080905e9 = ROM[0x59e2c..0x59e2f] = e9050908 little-endian. Confirmed.

PTR_gP1LifePoints_* slots (already named with PTR_ convention by prior work, no rename needed):
- L15957 DWORD_08059e5c -> PTR_gP1LifePoints_08059e5c (rename to match convention)
- L16300 DWORD_0805a090 -> PTR_gP1LifePoints_0805a090 (rename to match convention)
and various PTR_gP1LifePoints_* already decoded in the file -- these need only RENAME to
strip DWORD_/DAT_ prefix and add PTR_gP1LifePoints_ prefix. All hold value 0x0201c4e0 =
gP1LifePoints.

### RENAME_SLOTS (rename + optional EOL)

PTR_gP1LifePoints_* renames (all value 0x0201c4e0):

| slot | current name | new name | EOL |
|------|-------------|----------|-----|
| L15957 0x08059e5c | DWORD_08059e5c | PTR_gP1LifePoints_08059e5c | gP1LifePoints base ptr |
| L16300 0x0805a090 | DWORD_0805a090 | PTR_gP1LifePoints_0805a090 | gP1LifePoints base ptr |

All other slots with identified equate constants (see EQ_SLOTS table above): add EOL comment
indicating the semantic, e.g. `@ player_block_stride stride between P0/P1 field blocks`.

### FUNC_RENAME

No function renames needed in this segment. All 23 named functions have semantically correct
names verified against their plate comments and code bodies. No contradictions found.

### PLATE (R5) -- CJK mojibake repair + stale FUN_ replacement

7 functions need plate rewrites: 4 CJK mojibake (Jython double-UTF-8 -> ASCII) + 3 ASCII
plates with stale FUN_ names replaced by current function names. All plate text is pure ASCII.
After landing, grep segment range for `FUN_[0-9a-f]\{8\}` must return 0 matches.

**L16176 -- tick_equip_activation_if_pair_eligible (0x08059fc4)**

Current plate (mojibake): `@ ????...indeg=0, Sub-type A. ?? card_entry_ptr(r0)...`
Replace with ASCII plate:

```
@ Equip activation state-machine dispatcher. Driven by [gDuelPhaseFlags+0x4ac].
@ Checks pair eligibility before dispatching to Vandalgyon or Water Dragon activation paths.
@ indeg=0, Sub-type A. r0=card_entry_ptr, r1=secondary_ptr.
@ Returns u32 bool (1=activated, 0=waiting/failed).
```

**L16327 -- tick_equip_activation_sprite_mode2_by_type (0x0805a1dc)**

Current plate (mojibake): `@ ???...mode 2...0x08058550...card_entry[+2] bits[11:2] (mask 0xfc0)...0xf0<<2...`
Replace with ASCII plate:

```
@ Equip activation sprite routing for mode 2 cards. Symmetric to 0x08058550:
@ extracts card_entry[+2] bits[11:2] (mask 0xfc0); tests 0xf0<<2 = 0x3c0 for r0/r1 path.
@ r0=card_entry_ptr. Returns u32 (result of activation dispatch).
```

**L17374 -- check_card_placement_rules (0x0805a9a8)**

Current plate (ASCII, stale FUN_0802fc90): contains "FUN_0802fc90 (continuous effect quota)"
Current name of 0x0802fc90: `check_value_in_slot_chain` (asm/02_text_lp_fieldspell.s L8072)
Replace stale reference: "FUN_0802fc90" -> "check_value_in_slot_chain" throughout the plate.
Full rewritten plate (ASCII):

```
@ Comprehensive placement rule validator for card placement request.
@ Sequentially checks: (1) find_paired_zone_entry_for_card (paired zone conflict);
@ (2) check_card_field5_is_nonzero + check_value_in_slot_chain (continuous effect quota);
@ (3) find_effect_node_in_zone (effect zone occupation);
@ (4) get_card_field_summon_restriction (field-dependent summon limit);
@ (5) get_card_extended_stat_field6/9 (extended attribute filters);
@ (6) check_card_is_zone_pair_restricted (pair-restriction dual card check);
@ (7) get_card_effect_zone_check_sides + count_available_effect_zones (side mask check).
@ Any rule trigger: writes flag to gP1LifePoints-related player state and returns 1.
@ All rules pass: returns 0.
@ r8 is caller-set non-APCS player_state_base used for internal state writes.
@ r0=ptr card_info ([+0]=card_id, [+2]=player_side+zone_index packed, [+3]=flag_bits).
@ r8=ptr player_state_base (non-APCS, caller-set).
@ Returns u8 (0=placement allowed, 1=placement blocked).
@ Side-effect: [gP1LifePoints+0x1d78] may be written 0x14 on block path.
```

**L18216 -- build_zone_activation_entry_equip (0x0805b034)**

Current plate (mojibake): `@ ???...eval_equip_activation_for_slot...indeg=1...build_zone_activation_entry_blocked...FUN_080...`
Replace with ASCII plate:

```
@ Constructs a zone activation entry for an equip-type card target.
@ Called from eval_equip_activation_for_slot when target is an equip slot (indeg=1).
@ Symmetric structure to build_zone_activation_entry_blocked.
@ r0=card_ptr, r1=partner_ptr, r2=extra_payload. Returns u32 dispatch result.
```

**L18293 -- build_zone_activation_entry_blocked (0x0805b0cc)**

Current plate (mojibake): `@ ???...???...indeg=3...0x18 byte buf...memset...r2(card_id) -> [buf+0]...[buf+2]...`
Replace with ASCII plate:

```
@ Constructs a zone activation entry for a blocked equip target check (indeg=3).
@ Allocates 0x18-byte stack buffer, memset 0; writes r2(card_id) to [buf+0];
@ writes player/slot fields to [buf+2]. Calls apply_card_equip_activation.
@ r0=card_attr_packed, r1=entity_id, r2=card_id. Returns u32 bool.
```

**L18441 -- apply_equip_activation_via_packed_attr (0x0805b1f0)**

Current plate (ASCII, stale FUN_ refs):
- "FUN_0804c910" -> `apply_equip_activation_with_id_lookup` (asm/05_equip_eligibility_a.s L8043)
- "FUN_08096f20" -> `apply_equip_activation_with_fixed_type_a` (asm/12_equip_activation_scan.s L6042)
- "FUN_08096f40" -> `apply_equip_activation_via_deck_slot_lookup` (asm/12_equip_activation_scan.s L6066)
- "FUN_08099e0c" -> `run_equip_spell_display_state_machine` (asm/12_equip_activation_scan.s L12279)
- "FUN_0809d5f4" -> `scan_hand_equip_slot_for_activation_with_name_display` (asm/12_equip_activation_scan.s L19764)
Full rewritten plate (ASCII):

```
@ Equip activation record constructor: allocates 24-byte stack record, memset 0,
@ unpacks 8 bit fields from r0 packed_attr to record offsets:
@ sign bit -> [+2] bit0; bits[24..23] -> [+3] bits[6..7];
@ bits[20..18] -> [+3] bits[5..4]; bits[15..11] -> [+2] bits[2..7];
@ bits[31..26] -> [+2..3].
@ r1 (u16 entity_id, 9 bits) lsls #6 -> [+4] mask 0xffff803f.
@ r2 -> sp[0x14] (callee 4th arg). Then bl apply_card_equip_activation.
@ r0=u32 card_attr_packed; r1=u16 entity_id [0..0xffff]; r2=u32 extra_payload.
@ Returns u32 (decided by apply_card_equip_activation).
@ Direct callee of apply_equip_activation_with_id_lookup when r1!=0;
@ also called by apply_equip_activation_with_fixed_type_a /
@ apply_equip_activation_via_deck_slot_lookup /
@ run_equip_spell_display_state_machine /
@ scan_hand_equip_slot_for_activation_with_name_display.
@ Constants: BUF_SIZE=0x18, ENTITY_SHIFT=6, ATTR_MASK=0xffff803f.
```

**L18532 -- dispatch_card_effect_by_stat_type (0x0805b2a4)**

Current plate (ASCII, stale FUN_080954e8):
- "FUN_080954e8" -> `step_prng_anim_frame` (asm/12_equip_activation_scan.s L2580)
Full rewritten plate (ASCII):

```
@ Dispatches card effect processing based on card stat type fields and special card IDs.
@ r0=ptr card_entry (saved to r7).
@ Step 1: checks [r7+0x4] bit1 (processed_bit=0x2); if set returns 0 (already handled).
@ Step 2: calls check_card_effect_node_active; if node missing returns 0.
@ Step 3: checks [r7+0x4] bit2 (alt_path_bit=0x4); if clear jumps to LAB_0805b3c2.
@ Step 4: calls get_card_extended_stat_field9; matches field9 [2..3] range.
@ Step 5: checks [r7+0x3] AND 0x30 (stat3_bits); if card_id==0x1909 returns 0 (special skip).
@ Whole function is pure read; all exit paths are movs r0,#0 or movs r0,#1.
@ Called by step_prng_anim_frame (duel scene main loop).
@ Returns u32 should_continue (0=skip, 1=proceed).
@ Constants: processed_bit=0x2, alt_path_bit=0x4, stat3_bits=0x30,
@ card_id_special=0x1909, field9_range=[2..3].
```

---

## Disasm plan (R4)

### Block1: 0x0805a0aa..0x0805a0df (0x36 bytes)

- Bytes 0x0805a0aa..0x0805a0ab: `.zero 2` (alignment padding -- leave as-is)
- Disassemble THUMB range: **0x0805a0ac..0x0805a0df** (0x34 bytes = 52 B = 26 THUMB hwords = 1 new function)

Note: 0x5a0e0..0x5a0e3 holds `.word 0x0805a0e4` (asm L16317), already decoded asm OUTSIDE
the ROM_INCBIN range (ROM_INCBIN 0x5a0aa/0x36 covers 0x5a0aa..0x5a0df only). Do NOT include
0x5a0e0..0x5a0e3 in the disasm command. Literal pool 0x5a0d4..0x5a0df (CID 0x195c /
gDuelPhaseFlags 0x0201b290 / EQUIP_ACTIVATION_STEP_OFF 0x4ac) is inside the range and will
be decoded as data by Ghidra automatically.

**New function**: `tick_bonding_or_photon_activation_seq` @ 0x0805a0ac

Semantics (decoded from raw bytes):
- 5-state dispatcher: reads `[gDuelPhaseFlags + EQUIP_ACTIVATION_STEP_OFF]`
- Dispatch through state table at `PTR_DAT_0805a0e4` (5 raw entries)
- Dead code: `r5 := 3` if CID==0x195c (Bonding-H2O), else `r5 := 2` (Photon Generator Unit);
  r5 is set but never used after -- compiler artifact
- State > 4: returns 1 (sequence complete)
- Referenced via THUMB+1 = 0x0805a0ad from CID dispatch table at 0x9e42ca4 (CID 0x195c)
  and 0x9e42f74 (CID 0x19b1)

The dispatch table `PTR_DAT_0805a0e4` (5 .word entries already decoded, lines 16318-16323)
holds raw pointers (non-THUMB+1) to Block2 sub-functions. Leave dispatch table as-is.
Remove the `DAT_0805a0f8` label from line 16324 -- Block2 ROM_INCBIN label conflicts with
the disasm result; after disasm the ROM_INCBIN replaces with actual code.

### Block2: 0x0805a0f8..0x0805a1db (0xe4 bytes)

Disassemble THUMB range: **0x0805a0f8..0x0805a1db** (5 new sub-functions)

All 5 are state handlers for the dispatch table above. Raw pointers (NOT THUMB+1) stored in
dispatch table at 0x0805a0e4. After disasm, label each:

| entry addr | label | semantics |
|------------|-------|-----------|
| 0x0805a0f8 | tick_bonding_photon_state0_start_lp_bar | bl increment_lp_bar_display_counter; step++; return 0 |
| 0x0805a118 | tick_bonding_photon_state1_trigger_display | ldrb player_id; bl trigger_card_display_op31_if_not_active(player, 0x12); step++; return 0 |
| 0x0805a134 | tick_bonding_photon_state2_set_activation | ldrb player_id; bl set_equip_activation_state_by_mode(player, 1, set_equip_activation_state_by_mode_alt+1); step++; return 0 |
| 0x0805a148 | tick_bonding_photon_state3_confirm_sprite | bl check_activation_display_state_is_confirmed; if confirmed -> read gP1LP+ELIGIB_SPRITE_CTRL_OFF/ELIGIB_ANIM_STATE_OFF; bl submit_equip_sprite_if_slot_eligible; step++; else step--; return 0 |
| 0x0805a1cc | tick_bonding_photon_state4_end_lp_bar | bl decrement_lp_bar_display_counter; return 1 |

Note: dispatch table entries are raw pointers (no +1). The `PTR_DAT_0805a0e4` label is
correct; entries do NOT need +1 because this is NOT a THUMB fn-ptr jump via BX -- instead
the dispatcher loads the table entry into r3 and does `bl` to r3 via a computed BL pattern.

---

## New constants / globals (required)

Grep confirmed these values do NOT exist in any constants/*.inc:

| value | suggested name | suggested inc | evidence |
|-------|---------------|---------------|---------|
| 0x000019a3 | SPECIAL_EQUIP_SENTINEL_ID | card_info.inc | apply_card_equip_activation plate (asm/06 L18020): "Constants: special_equip_id=0x19a3"; no card-stats.s entry; acts as sentinel CID for equip dispatch path; confidence: high |
| 0x0000303e | ZONE_STATUS_MASK | card_info.inc | check_card_normal_summon_eligible_full plate (asm/06 L19781, L19867): "slot[+2] & 0x303e==0x201c"; 2 refs in Seg-9 (DAT_0805b014), 1 ref at 0x0805bf00; 16-bit zone flags mask; confidence: high |
| 0x0000131e | SPECIAL_EQUIP_TARGET_CID_A | card_info.inc | check_equip_card_can_target_partner (L17211): compared with card_id after get_card_equip_zone_rank<=1; noted in asm/02 as "chain effect node type 0x131e; no card-stats entry"; special-cases this CID as allowed equip target regardless of rank; confidence: high (asm/06 L17250-17252) |

New CID equates -- to be added to card_info.inc (20 new; 9 reuse existing; 2 reuse existing
under different name; 1 new with same value as duel_field.inc offset but different domain):

**REUSE existing card_info.inc (9 values already present, same name -- no new .equ needed):**

| value | existing name | slots |
|-------|--------------|-------|
| 0x00000fee | COCOON_OF_EVOLUTION_CID | 2 slots in Seg-9 |
| 0x0000132c | CHAIN_ENERGY_CID | 1 slot |
| 0x0000146f | CATHEDRAL_OF_NOBLES_CID | 2 slots |
| 0x00001232 | MAGICAL_LABYRINTH_CID | 1 slot |
| 0x000012de | DARK_MAGIC_CURTAIN_CID | 1 slot |
| 0x0000166c | SKILL_DRAIN_CID | 1 slot |
| 0x0000184a | XING_ZHEN_HU_CID | 1 slot |
| 0x0000184b | RARE_METALMORPH_CID | 1 slot |
| 0x00001909 | SPARK_BLASTER_CID | 1 slot |

**REUSE existing card_info.inc (2 values present under different name -- reuse existing name):**

| value | existing name | do NOT create | note |
|-------|--------------|---------------|------|
| 0x000013eb | EQUIP_ZONE_BLOCKER_CID | ~~SOUL_EXCHANGE_CID~~ | card-stats.s L11182 = Soul Exchange pw=68005187; existing name is semantic desc; reuse EQUIP_ZONE_BLOCKER_CID; add EOL "= Soul Exchange CID" |
| 0x00001432 | GROUND_COLLAPSE_FIELD_CARD_ID | ~~GROUND_COLLAPSE_CID~~ | same card; reuse GROUND_COLLAPSE_FIELD_CARD_ID |

**Reverse-verification (iter-2 fixer, 2026-06-14)**: all entries marked "reuse" in EQ_SLOTS
and the REUSE tables above were independently grepped against `constants/card_info.inc`.
Results:
- 9 reuse-same-name: COCOON_OF_EVOLUTION_CID/CHAIN_ENERGY_CID/CATHEDRAL_OF_NOBLES_CID/
  MAGICAL_LABYRINTH_CID/DARK_MAGIC_CURTAIN_CID/SKILL_DRAIN_CID/XING_ZHEN_HU_CID/
  RARE_METALMORPH_CID/SPARK_BLASTER_CID -- all confirmed present (name + value match).
- 2 reuse-diff-name: EQUIP_ZONE_BLOCKER_CID (0x13eb) / GROUND_COLLAPSE_FIELD_CARD_ID (0x1432)
  -- both confirmed present.
- Additional reuse entries in EQ_SLOTS (not in the "9" grouping):
  SLOT_CARD_EMPTY/FIELD_SPELL_B_EFFECT_ID/DARK_RULER_VANDALGYON_CID/MAKYURA_THE_DESTRUCTOR_CID/
  BUBBLE_ILLUSION_CID/ANCIENT_GEAR_DRILL_CID/ANCIENT_GEAR_GOLEM_CID/SONIC_JAMMER_CID/
  AMPLIFIER_CID/JINZO_CID/JUDGEMENT_OF_PHARAOH_CID/PROTECTOR_OF_THE_SANCTUARY_CID/
  KUNAI_WITH_CHAIN_CID/BLAST_WITH_CHAIN_CID/THE_FIRST_SARCOPHAGUS_CID
  -- all confirmed present.
- SPIRIT_RYU_CID (0x14d7): grep returned 0 hits -- absent. Correctly reclassified as NEW.
- No other reuse entries found absent. Zero additional mis-tags.

**NEW in card_info.inc (20 values, genuinely absent or new domain):**

| value | name | card name | evidence |
|-------|------|-----------|---------|
| 0x00001390 | ANTI_SPELL_FRAGRANCE_CID | Anti-Spell Fragrance (pw=58921041) | card-stats.s L9831 (approx); 2 slots; same value as FIELD_SPELL_CARD_REF_OFF in duel_field.inc but different domain (CID vs offset) -- new entry in card_info.inc only; duel_field.inc left unchanged |
| 0x00001944 | LEVEL_MODULATION_CID | Level Modulation (pw=61850482) | card-stats.s L25219; 2 slots |
| 0x000015da | SPELL_CANCELLER_CID | Spell Canceller (pw=84636823) | card-stats.s L16186 (0x15DA); 1 slot |
| 0x00001910 | MECHANICAL_HOUND_CID | Mechanical Hound (pw=22512237) | card-stats.s L25082; 1 slot |
| 0x00001722 | INVADER_OF_DARKNESS_CID | Invader of Darkness (pw=56647086) | card-stats.s L22386; 1 slot |
| 0x00001832 | CREEPING_DOOM_MANTA_CID | Creeping Doom Manta (pw=52571838) | card-stats.s L23985; 1 slot |
| 0x00001833 | PITCH_BLACK_WARWOLF_CID | Pitch-Black Warwolf (pw=88975532) | card-stats.s L23998; 1 slot |
| 0x00001834 | MIRAGE_DRAGON_CID | Mirage Dragon (pw=15960641) | card-stats.s L24011; 1 slot |
| 0x000019bb | ANCIENT_GEAR_CANNON_CID | Ancient Gear Cannon (pw=80045583) | card-stats.s L26833; 1 slot |
| 0x00001664 | FAIRY_OF_THE_SPRING_CID | Fairy of the Spring (pw=20188127) | card-stats.s L17382; 1 slot |
| 0x000016dd | CURSED_SEAL_FORBIDDEN_SPELL_CID | Cursed Seal of the Forbidden Spell (pw=58851034) | card-stats.s L18694; 1 slot |
| 0x00001243 | SHADOW_SPELL_CID | Shadow Spell (pw=29267084) | card-stats.s L8646; 1 slot |
| 0x00001103 | SPELLBINDING_CIRCLE_CID | Spellbinding Circle (pw=18807108) | card-stats.s L8984; 1 slot |
| 0x00001710 | STRAY_LAMBS_CID | Stray Lambs (pw=60764581) | card-stats.s L19540; 1 slot |
| 0x0000173f | AGENT_OF_JUDGMENT_SATURN_CID | The Agent of Judgment - Saturn (pw=91345518) | card-stats.s L19696; 1 slot |
| 0x000018d3 | IMPENETRABLE_FORMATION_CID | Impenetrable Formation (pw=96631852) | card-stats.s L24181; 1 slot |
| 0x0000150d | SMOKE_GRENADE_OF_THIEF_CID | Smoke Grenade of the Thief (pw=63789924) | card-stats.s L14054; 1 slot |
| 0x000015ee | WAVE_MOTION_CANNON_CID | Wave-Motion Cannon (pw=38992735) | card-stats.s L16186 (0x15EE); 1 slot |
| 0x000019d8 | TRIAL_OF_THE_PRINCESSES_CID | Trial of the Princesses (pw=72709014) | card-stats.s L26781; 1 slot |
| 0x000014d7 | SPIRIT_RYU_CID | Spirit Ryu (pw=67957315) | card-stats.s L13418 (card_1031 slot=0x14D7); 1 slot (DAT_0805a90c L17289); check_equip_card_can_target_partner |

**UNMAPPED CID (2 values -- neutral low-confidence labels, per file-05 convention):**
- `0x000018f5` at DAT_0805a6f4 (L17017): consumer context (L16986: `ldr r2, DAT_0805a6f4` then
  `bl test_slot_has_active_card`) confirms r2 is a card_id comparison argument -- this is
  definitively a card_id context. card-stats.s has no entry for 0x18f5 (no known card).
  No card_info.inc equate. Label as `cid_18f5` (neutral low-conf, cannot fabricate card name).
  Rationale for neutral label: card-stats.s absence = unknown card; naming from context alone
  would be speculative. Convention: file-05 unmapped-CID pattern.
- `0x00001684` at DAT_0805ab10 (L17555): consumer context (L17538 area: `ldr r2, DAT_0805ab10`
  then `bl find_effect_node_in_zone`) confirms r2 is a card_id parameter -- definitively
  card_id context. card-stats.s has no entry for 0x1684. Label as `cid_1684` (neutral low-conf).
  Same rationale as above.
- `0x0000131e` at DAT_0805a908 (L17287): no card-stats.s entry (gap between 0x131D
  Gravekeeper's Servant and 0x131F Upstart Goblin); noted in asm/02 as "chain effect node
  type 0x131e". In `check_equip_card_can_target_partner` it's compared with card_id as
  a special-case CID. Use name `SPECIAL_EQUIP_TARGET_CID_A` (new const).

---

## Section 5.1 (Rule 3) -- 0-reference blocks

None. Both ROM_INCBIN blocks have confirmed code references (see ref-scan results above).

---

## Consumer evidence (R6) -- key slot semantics

| slot | value | function | file:line | confidence |
|------|-------|----------|-----------|------------|
| DWORD_08059e2c | 0x080905e9 | tick_equip_zone14_activation_display_seq | asm/06 L15934; set_equip_activation_state_by_mode_alt+1 in asm/11 L11787 | high |
| DAT_08059fdc | 0x0000190a | tick_equip_activation_if_pair_eligible | asm/06 L16190; plate: "checks Vandalgyon (0x190a)"; DARK_RULER_VANDALGYON_CID confirmed in card_info.inc | high |
| DAT_0805a4c4 | 0x0000ffff | eval_equip_activation_for_slot | asm/06 L16697; `cmp r2,r0` after `find_equip_chain_pair_across_field` upper-halfword extract; SLOT_CARD_EMPTY sentinel | high |
| DAT_0805a6dc | 0x000014a5 | tick_equip_banisher_field_count_display_seq | asm/06 L17005; MAKYURA_THE_DESTRUCTOR_CID in card_info.inc | high |
| DAT_0805af50 | 0x000019a3 | apply_card_equip_activation | asm/06 L18105; plate (L18020): "Constants: special_equip_id=0x19a3"; compared with CID at dispatch branch | high |
| DAT_0805b014 | 0x0000303e | check_card_normal_summon_eligible_full | asm/06 L18199; plates at L19781 + L19867: "slot[+2] & 0x303e == 0x201c"; 2 occurrences in Seg-9 + 1 at 0x0805bf00 | high |
| DAT_0805a908 | 0x0000131e | check_equip_card_can_target_partner | asm/06 L17250-17252; `ldrh r1,[r5,#0x0]; ldr r0,DAT_0805a908; cmp r1,r0`; asm/02 L34470: "chain effect node type 0x131e; no card-stats entry" | high |

---

## Seek help (low-confidence items)

1. **CID 0x000018f5** (DAT_0805a6f4, L17017): No card-stats.s entry, no card_info.inc match.
   Consumer context (L16986: `ldr r2, DAT_0805a6f4` then `bl test_slot_has_active_card`)
   confirms this is definitively a card_id comparison argument. Card name cannot be determined
   from ROM data alone (card-stats.s absent). Resolution: use neutral label `cid_18f5`
   (low-confidence, per file-05 unmapped-CID convention). No fabricated card name.

2. **CID 0x00001684** (DAT_0805ab10, L17555): No card-stats.s entry. Consumer context
   (L17538 area: `ldr r2, DAT_0805ab10` then `bl find_effect_node_in_zone`) confirms
   definitively a card_id parameter. Resolution: use neutral label `cid_1684`
   (low-confidence, same convention). No fabricated card name.

3. **Block2 dispatch table pointer semantics**: dispatch table at 0x0805a0e4 uses raw pointers
   (NOT THUMB+1) for state-handler sub-functions. This is unusual -- normally GBA THUMB fn-ptrs
   are addr|1. The calling code must be using a PC-relative BL via computed offset, not BX.
   Confidence: high (confirmed: ref-scan shows raw=1 for each entry, THUMB+1=0).

---

## Executor Report: F06-Seg-9

- Slots: EQ=131 REF=1 RENAME=2 FUNC_RENAME=0 PLATE=7 (4 CJK mojibake repair + 3 stale-FUN_ ASCII rewrite)
- carve=0 disasm=2 ranges (Block1: 0x0805a0ac..0x0805a0df = 1fn; Block2: 0x0805a0f8..0x0805a1db = 5fn) sec5.1=0
- New constants/globals: SPECIAL_EQUIP_SENTINEL_ID(0x19a3) + ZONE_STATUS_MASK(0x303e) + SPECIAL_EQUIP_TARGET_CID_A(0x131e) in card_info.inc; 20 new CID equates in card_info.inc; 9 CID reuse (same name); 2 CID reuse (different name: EQUIP_ZONE_BLOCKER_CID/GROUND_COLLAPSE_FIELD_CARD_ID); 1 new CID in card_info.inc with same value as duel_field.inc offset (different domain -- ANTI_SPELL_FRAGRANCE_CID=0x1390 vs FIELD_SPELL_CARD_REF_OFF=0x1390)
- Unmapped CIDs: 0x18f5 -> cid_18f5_17017 (card-stats.s absent, confirmed card_id context, neutral label); 0x1684 -> cid_1684_17555 (same); Block2 raw-ptr dispatch table pattern confirmed correct (not a bug)
- Post-land grep check: grep segment range FUN_[0-9a-f]{8} must == 0 matches
- proposal: doc/dev/refine/F06-Seg-9.proposal.md
