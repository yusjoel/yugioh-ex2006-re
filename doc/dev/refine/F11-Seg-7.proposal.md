# Refine Proposal: F11-Seg-7  [0x0808f7c0..0x08090a78)

## Segment Survey

37 named functions (35 pre-existing + 2 new stubs), 0 ROM_INCBIN, Region C (pure symbolization).

| Addr       | Name                                          | Notes                                |
|------------|-----------------------------------------------|--------------------------------------|
| 0x0808f7c0 | enqueue_sprite_by_field_copy_count            | CONVULSION_OF_NATURE bitmap update   |
| 0x0808f800 | (switch-case body, part of above fn)          | embedded 10-case switch              |
| 0x0808f86c | scan_field_slots_for_equip_chain_node_bitmap_update | SPIRIT_REAPER+DARK_ROOM 2-CID |
| 0x0808f938 | refresh_opponent_field_slots_for_card_attached | DARK_ROOM_OF_NIGHTMARE opp scan     |
| 0x0808f9f8 | scan_field_slots_for_equip_bitmap_update      | PITCH_BLACK_POWER_STONE filter       |
| 0x0808fa4c | scan_field_for_extra_deck_equip_slot_update   | EXODIA_NECROSS + 5x RIGHT_LEG CID   |
| 0x0808fae4 | scan_field_slots_for_inactive_equip_bitmap_clear | FALLING_DOWN CID shifted filter   |
| 0x0808fbd0 | scan_field_slots_for_archfiend_equip_bitmap_update | BERSERK_GORILLA_CID filter      |
| 0x0808fc78 | scan_card_placement_for_activation            | SPHINX_TELEIA+THEINEN init scan     |
| 0x0808fdc0 | scan_effect_zone_slots_for_equip_activation   | SOUL_ABSORPTION_CID filter          |
| 0x0808fe84 | apply_equip_activation_from_zone_scan         | CRIOSPHINX_CID filter               |
| 0x0808ff44 | scan_slots_for_field_bit4_sprite_update       | SOUL_ABSORBING_BONE_TOWER shifted   |
| 0x0808ffb4 | scan_field_slots_for_equip_sprite_by_chain    | SILENT_MAGICIAN_LV4 CID filter      |
| 0x0809007c | scan_equip_set_slot_sprite_by_counter         | THE_BLOCKMAN CID shifted + counter  |
| 0x0809011c | scan_slots_for_equip_activation_by_field5     | generic 5-field filter              |
| 0x08090218 | dispatch_equip_field_scan_sequence            | 30-scanner chain hub, in-seg        |
| 0x080904ec | return_effect_node_result_0                   | NEW stub: movs r0,#0; bx lr; indeg=10 THUMB |
| 0x080904f0 | return_effect_node_result_2                   | NEW stub: movs r0,#2; bx lr; indeg=9 THUMB  |
| 0x080904f4 | find_card_effect_node_entry                   | BST 4-table dispatch                |
| 0x0809058c | check_card_has_activatable_effect_node        | query wrapper                       |
| 0x080905c0 | invoke_effect_node_handler_2arg               | node[+0xc] 2-arg invoke; indeg=7   |
| 0x080905e8 | set_equip_activation_state_by_mode_alt        | MISNOMER: see FUNC_RENAME           |
| 0x08090624 | invoke_effect_node_with_active_flag_3arg      | node[+0x8] 3-arg+flag; indeg=78    |
| 0x0809066c | query_equip_zone_bitmap_with_effect_guard     | no-flag bitmap query                |
| 0x08090690 | query_equip_zone_bitmap_with_active_flag      | flag-fenced bitmap query            |
| 0x080906cc | build_equip_zone_bitmap_for_player            | 2x11 zone bitmap builder            |
| 0x08090714 | count_effect_node_zone_activations            | 2x11 zone loop, clears 0x4bc first  |
| 0x0809077c | invoke_count_zone_pair_hits_full_range        | r2=-1 wrapper; in-seg               |
| 0x0809078c | count_zone_pair_hits_with_fn_ptr              | fn_ptr zone scan counter            |
| 0x080907f4 | count_effect_node_activations_by_zone         | single-dim 11-zone loop             |
| 0x08090848 | dispatch_card_effect_activation               | unicast+broadcast dispatch          |
| 0x08090900 | invoke_card_effect_node_handler               | node[+0x10] invoke                  |
| 0x08090928 | check_effect_node_handler_present             | bool nonzero-test for [+0x10]       |
| 0x08090944 | invoke_effect_node_action_if_found            | node[+0x14] invoke                  |
| 0x0809096c | check_card_effect_node_has_callback           | bool test for [+0x14]               |
| 0x08090988 | apply_equip_lp_delta_by_node_flag             | LP delta commit by bit5/bit2 flags  |
| 0x080909e0 | check_card_effect_node_active                 | bool test for [+0x4] activation cnt |
| 0x080909fc | scan_equip_chain_nodes_for_bitmap_update      | node-type=0xa chain scan            |

## Data Block Classification (Rule 2/3)

| Addr range             | Size | Refs (THUMB+1) | Disposition           |
|------------------------|------|----------------|-----------------------|
| 0x080904ec-0x080904ef  | 4 B  | 10             | R4 disasm + createFunction + name (return_effect_node_result_0) |
| 0x080904f0-0x080904f3  | 4 B  | 9              | R4 disasm + createFunction + name (return_effect_node_result_2) |

Both stubs have THUMB refs from effect node descriptor tables (TYPE0/1/2/3 at 0x09e40c00-0x09e42c58).
Rule 2: referenced code blocks must be disassembled and named.

## Symbolization Plan

### EQ_SLOTS

Total DAT_ slots in Seg-7 scope: 108. 107 are EQ (constant equate); 1 (DAT_0808f934) is RENAME.
9 PTR_gP1LifePoints_ are REF (RENAME as ptr_lp_xxxx).
NOTE: switchd_base_f818 and 3 seg6_pool_* labels are Seg-6 territory (< 0x0808f86c); excluded.

#### REUSE EQ (constants already in constants/*.inc)

| Slot addr  | Value      | Existing name             | Source file        |
|------------|------------|---------------------------|---------------------|
| 0x0808f898 | 0x000010d0 | EFFECT_ZONE_BITMASK_OFF   | duel_field.inc:~200 |
| 0x0808f89c | 0x00001d28 | EQUIP_CHAIN_STEP_OFF      | duel_field.inc      |
| 0x0808f924 | 0x00000868 | PLAYER_BLOCK_STRIDE       | ewram.inc:251       |
| 0x0808f928 | 0x0201e1c8 | EQUIP_ZONE_COUNT_TABLE_OFF| duel_field.inc (comment "gDuelFieldSlots+0x1cb8") |
| 0x0808f92c | 0x0201c510 | gDuelFieldSlots           | ewram.inc           |
| 0x0808f930 | 0x00001596 | SPIRIT_REAPER_CID         | card_info.inc       |
| 0x0808f9cc | 0x0000159b | DARK_ROOM_OF_NIGHTMARE_CID| card_info.inc       |
| 0x0808f9d4 | 0x00000868 | PLAYER_BLOCK_STRIDE       | ewram.inc:251       |
| 0x0808fa30 | 0x0201e1c8 | EQUIP_ZONE_COUNT_TABLE_OFF| duel_field.inc      |
| 0x0808fa34 | 0x00001624 | PITCH_BLACK_POWER_STONE_CID| card_info.inc      |
| 0x0808fab4 | 0x0201e1c8 | EQUIP_ZONE_COUNT_TABLE_OFF| duel_field.inc      |
| 0x0808fab8 | 0x00001645 | EXODIA_NECROSS_CID        | card_info.inc       |
| 0x0808fabc | 0x00000fb7 | RIGHT_LEG_FORBIDDEN_ONE_CID| card_info.inc      |
| 0x0808fac0 | 0x00000fb8 | LEFT_LEG_FORBIDDEN_ONE_CID| card_info.inc       |
| 0x0808fac4 | 0x00000fb9 | RIGHT_ARM_FORBIDDEN_ONE_CID| card_info.inc      |
| 0x0808fac8 | 0x00000fba | LEFT_ARM_FORBIDDEN_ONE_CID| card_info.inc       |
| 0x0808facc | 0x00000fbb | FORBIDDEN_ONE_CID         | card_info.inc       |
| 0x0808fb90 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8      | ewram.inc           |
| 0x0808fb94 | 0x00000868 | PLAYER_BLOCK_STRIDE       | ewram.inc:251       |
| 0x0808fb98 | 0x0201c510 | gDuelFieldSlots           | ewram.inc           |
| 0x0808fba0 | 0x0201c520 | gDuelFieldSlotState       | ewram.inc           |
| 0x0808fc48 | 0x0201e1c8 | EQUIP_ZONE_COUNT_TABLE_OFF| duel_field.inc      |
| 0x0808fc4c | 0x00000868 | PLAYER_BLOCK_STRIDE       | ewram.inc:251       |
| 0x0808fc54 | 0x0201c510 | gDuelFieldSlots           | ewram.inc           |
| 0x0808fce0 | 0x0201b290 | gDuelPhaseFlags           | ewram.inc           |
| 0x0808fce4 | 0x000004cc | LP_BAR_ANIM_STATE_OFF     | ewram.inc           |
| 0x0808fce8 | 0x000004d4 | SPRITE_ROW_ENTRY_DATA_OFF | ewram.inc           |
| 0x0808fcec (PTR)| gP1LifePoints | ptr_lp_fcec      | REF_SLOT below      |
| 0x0808fcf0 | 0x000004f4 | CHAIN_NODE_CARD_ARR_OFF   | ewram.inc           |
| 0x0808fce0 | 0x0201b290 | gDuelPhaseFlags           | ewram.inc           |
| 0x0808fd94 | 0x0201b290 | gDuelPhaseFlags           | ewram.inc           |
| 0x0808fd98 | 0x000004f4 | CHAIN_NODE_CARD_ARR_OFF   | ewram.inc           |
| 0x0808fda0 | 0x000004d4 | SPRITE_ROW_ENTRY_DATA_OFF | ewram.inc           |
| 0x0808fe50 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8      | ewram.inc           |
| 0x0808fe54 | 0x00000868 | PLAYER_BLOCK_STRIDE       | ewram.inc:251       |
| 0x0808fe58 | 0x0201c510 | gDuelFieldSlots           | ewram.inc           |
| 0x0808ff10 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8      | ewram.inc           |
| 0x0808ff14 | 0x00000868 | PLAYER_BLOCK_STRIDE       | ewram.inc:251       |
| 0x0808ff18 | 0x0201c510 | gDuelFieldSlots           | ewram.inc           |
| 0x0808ff1c | 0x000018b2 | CRIOSPHINX_CID            | card_info.inc       |
| 0x0808ffa4 | 0x0201e1c8 | EQUIP_ZONE_COUNT_TABLE_OFF| duel_field.inc      |
| 0x0808ffa8 | 0x00000868 | PLAYER_BLOCK_STRIDE       | ewram.inc:251       |
| 0x0808ffac | 0x0201c510 | gDuelFieldSlots           | ewram.inc           |
| 0x08090040 | 0x0201e1c8 | EQUIP_ZONE_COUNT_TABLE_OFF| duel_field.inc      |
| 0x08090044 | 0x00000868 | PLAYER_BLOCK_STRIDE       | ewram.inc:251       |
| 0x08090048 | 0x0201c520 | gDuelFieldSlotState       | ewram.inc           |
| 0x0809004c | 0x0201c510 | gDuelFieldSlots           | ewram.inc           |
| 0x08090050 | 0x00001817 | SILENT_MAGICIAN_LV4_CID   | card_info.inc       |
| 0x08090090 | 0x00001cf4 | FIELD_STATE_OFF           | duel_field.inc      |
| 0x0809010c | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8      | ewram.inc           |
| 0x08090110 | 0x00000868 | PLAYER_BLOCK_STRIDE       | ewram.inc:251       |
| 0x08090204 | 0x0201e1c8 | EQUIP_ZONE_COUNT_TABLE_OFF| duel_field.inc      |
| 0x08090208 | 0x00000868 | PLAYER_BLOCK_STRIDE       | ewram.inc:251       |
| 0x0809020c | 0x0201c510 | gDuelFieldSlots           | ewram.inc           |
| 0x08090210 | 0x0201c520 | gDuelFieldSlotState       | ewram.inc           |
| 0x080903d0 | 0x00001d38 | DISPATCH_ACTIVE_FLAG_OFF  | duel_field.inc:218  |
| 0x080903d4 | 0x00001d08 | P1LP_BLOCK2_OFF           | ewram.inc           |
| 0x080903d8 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8      | ewram.inc           |
| 0x080903dc | 0x0201e2a0 | gDuelCardCtxBase          | ewram.inc           |
| 0x080903e0 | 0x000010d0 | EFFECT_ZONE_BITMASK_OFF   | duel_field.inc      |
| 0x080904b0 | 0x00000868 | PLAYER_BLOCK_STRIDE       | ewram.inc:251       |
| 0x080904b4 | 0x0201e1c8 | EQUIP_ZONE_COUNT_TABLE_OFF| duel_field.inc      |
| 0x080904b8 | 0x0201c510 | gDuelFieldSlots           | ewram.inc           |
| 0x080904d0 | 0x00001d38 | DISPATCH_ACTIVE_FLAG_OFF  | duel_field.inc:218  |
| 0x080904d4 | 0x00001d3c | P1LP_EQUIP_BITMAP_CTR_OFF | ewram.inc:396       |
| 0x08090614 | 0x0201b290 | gDuelPhaseFlags           | ewram.inc           |
| 0x08090618 | 0x000004bc | PHASE_LOCK_FLAG_OFF       | duel_field.inc:189  |
| 0x08090664 | 0x0201b290 | gDuelPhaseFlags           | ewram.inc           |
| 0x08090668 | 0x000004bc | PHASE_LOCK_FLAG_OFF       | duel_field.inc:189  |
| 0x080906b8 | 0x0201b290 | gDuelPhaseFlags           | ewram.inc           |
| 0x080906bc | 0x000004bc | PHASE_LOCK_FLAG_OFF       | duel_field.inc:189  |
| 0x08090774 | 0x0201b290 | gDuelPhaseFlags           | ewram.inc           |
| 0x08090778 | 0x000004bc | PHASE_LOCK_FLAG_OFF       | duel_field.inc:189  |
| 0x080907ec | 0x0201b290 | gDuelPhaseFlags           | ewram.inc           |
| 0x080907f0 | 0x000004bc | PHASE_LOCK_FLAG_OFF       | duel_field.inc:189  |
| 0x08090840 | 0x0201b290 | gDuelPhaseFlags           | ewram.inc           |
| 0x08090844 | 0x000004bc | PHASE_LOCK_FLAG_OFF       | duel_field.inc:189  |
| 0x08090884 | 0x0201b290 | gDuelPhaseFlags           | ewram.inc           |
| 0x08090888 | 0x00000484 | EQUIP_ACTIVE_CTX_OFF      | duel_field.inc:364  |
| 0x080908d4 | 0x0201b290 | gDuelPhaseFlags           | ewram.inc           |
| 0x080908d8 | 0x000004bc | PHASE_LOCK_FLAG_OFF       | duel_field.inc:189  |
| 0x080908dc | 0x00000484 | EQUIP_ACTIVE_CTX_OFF      | duel_field.inc:364  |
| 0x080908f8 | 0x0201b290 | gDuelPhaseFlags           | ewram.inc           |
| 0x080908fc | 0x00000484 | EQUIP_ACTIVE_CTX_OFF      | duel_field.inc:364  |
| 0x08090a58 | 0x00000868 | PLAYER_BLOCK_STRIDE       | ewram.inc:251       |
| 0x08090a5c | 0x0201c510 | gDuelFieldSlots           | ewram.inc           |
| 0x08090a60 | 0x0201d9c0 | gEquipNodePool            | ewram.inc           |
| 0x08090af0 | 0x0201bb90 | gEquipChainSlotRefs        | ewram.inc           |

REUSE special-context (same value, different semantic domain):
| Slot addr  | Value      | Existing name (same value, same domain) | Note                  |
|------------|------------|------------------------------------------|------------------------|
| 0x080900c0 | 0x0000ffff | EQUIP_SLOT_SCORE_CAP                    | oam_attr.inc:156 (score domain, NOT OAM_ATTR0_HIDDEN); high conf |
| 0x08090214 | 0x0000ffff | EQUIP_SLOT_SCORE_CAP                    | same domain           |
| 0x08090118 | 0x00001cbc | CHAIN_LINK_COUNTER_OFF                  | ewram.inc             |

#### NEW EQ (not in any constants/*.inc as of grep-date 2026-06-26)

All ROM-verified (python struct read, all match=True).

| Slot addr(s)     | Value       | Proposed const_name                    | Source .inc          | Evidence                                                        |
|------------------|-------------|----------------------------------------|----------------------|-----------------------------------------------------------------|
| 0x0808fc50       | 0x000016bf  | BERSERK_GORILLA_CID                    | card_info.inc        | card-stats.s card_1410 pw=39168895; C5 grep=0 hits; conf: high  |
| 0x0808fb9c       | 0xb4d00000  | FALLING_DOWN_CID_SHIFTED               | card_info.inc        | 0xb4d00000>>19=0x169a=FALLING_DOWN_CID; lsls r0,#0x13 pattern; conf: high |
| 0x0808ffb0       | 0xba200000  | SOUL_ABSORBING_BONE_TOWER_CID_SHIFTED  | card_info.inc        | 0xba200000>>19=0x1744; card-stats.s card_1519; conf: high       |
| 0x08090114       | 0xc0800000  | THE_BLOCKMAN_CID_SHIFTED               | card_info.inc        | 0xc0800000>>19=0x1810; card-stats.s card_1689; conf: high       |
| 0x0808fda4       | 0x005017c9  | THEINEN_ACTIVATION_PACKED              | card_info.inc        | CID=THEINEN_THE_GREAT_SPHINX_CID(0x17c9) | 0x00500000 flag bits; scan_card_placement_for_activation orrs into OAM attr at 0x0808fd7c; C5 grep=0; conf: high |
| 0x0808fcdc       | 0x09e3f18c  | SPHINX_ACTIVATION_INIT_TEMPLATE        | duel_field.inc       | 4-word template loaded via ldmia; raw=1, thumb=0 refs in ROM; scan_card_placement_for_activation init path; conf: high |
| 0x08090520       | 0x09e3f19c  | EFFECT_NODE_TABLE_TYPE0_BASE           | duel_field.inc       | find_card_effect_node_entry type=0 dispatch; raw=1, thumb=0 in ROM; 0x2a3 entries x 0xc stride; conf: high |
| 0x08090530       | 0x09e430fc  | EFFECT_NODE_TABLE_TYPE1_BASE           | duel_field.inc       | find_card_effect_node_entry type=1 dispatch; raw=1, thumb=0; 0x187 entries; conf: high |
| 0x08090540       | 0x09e455bc  | EFFECT_NODE_TABLE_TYPE2_BASE           | duel_field.inc       | find_card_effect_node_entry type=2 dispatch; raw=1, thumb=0; 0x8e entries; conf: high |
| 0x0809054c       | 0x09e46324  | EFFECT_NODE_TABLE_TYPE3_BASE           | duel_field.inc       | find_card_effect_node_entry type=3 dispatch; raw=1, thumb=0; 0xb7 entries; conf: high |
| 0x08090524       | 0x000002a3  | EFFECT_NODE_TABLE_TYPE0_COUNT          | duel_field.inc       | binary search upper bound; 0x2a3=675 entries; conf: high        |
| 0x08090534       | 0x00000187  | EFFECT_NODE_TABLE_TYPE1_COUNT          | duel_field.inc       | binary search upper bound for type=1 (DAT_08090534, ldr r2 in find_card_effect_node_entry type=1 branch); 0x187=391 entries; conf: high |

Note: 0x000016da=SOUL_ABSORPTION_CID, 0x000017c7=SPHINX_TELEIA_CID, 0x000017c9=THEINEN_THE_GREAT_SPHINX_CID,
0x000016bf=BERSERK_GORILLA_CID (NEW), 0x00001817=SILENT_MAGICIAN_LV4_CID, 0x00001762=BACKFIRE_CID,
0x0000186b=GEARFRIED_SWORDMASTER_CID, 0x00001862=MAJI_GIRE_PANDA_CID, 0x00001875=FIREBIRD_CID
-- all card IDs are used raw (not shifted); shifted-mask variants require separate NEW equates.

Additional REUSE (dedup confirmed at proposal write time):
- 0x000004bc: PHASE_LOCK_FLAG_OFF (duel_field.inc:189) -- 8 slots, all REUSE
- 0x00000484: EQUIP_ACTIVE_CTX_OFF (duel_field.inc:364) -- 3 slots, all REUSE
- 0x00001d38: DISPATCH_ACTIVE_FLAG_OFF (duel_field.inc:218) -- 2 slots
- 0x0808fe5c (0x000016da): SOUL_ABSORPTION_CID (card_info.inc) -- REUSE
- 0x080904bc (0x00001762): BACKFIRE_CID (card_info.inc) -- REUSE
- 0x080904c0 (0x0000186b): GEARFRIED_SWORDMASTER_CID (card_info.inc) -- REUSE
- 0x080904c4 (0x00001862): MAJI_GIRE_PANDA_CID (card_info.inc) -- REUSE
- 0x080904c8 (0x00001875): FIREBIRD_CID (card_info.inc) -- REUSE
- 0x0808fcf4 (0x000017c7): SPHINX_TELEIA_CID (card_info.inc) -- REUSE
- 0x0808fd9c (0x000017c9): THEINEN_THE_GREAT_SPHINX_CID (card_info.inc) -- REUSE

### REF_SLOTS (PTR_gP1LifePoints_ RENAME)

9 pointer slots; all hold value gP1LifePoints (0x0201c4e0).
Naming convention: ptr_lp_<hex_addr_4lsb> for disambiguation.

| Slot addr  | GAS label       |
|------------|-----------------|
| 0x0808f894 | ptr_lp_f894     |
| 0x0808f9d0 | ptr_lp_f9d0     |
| 0x0808fb8c | ptr_lp_fb8c     |
| 0x0808fcec | ptr_lp_fcec     |
| 0x0808fe4c | ptr_lp_fe4c     |
| 0x0808ff0c | ptr_lp_ff0c     |
| 0x0809008c | ptr_lp_008c     |
| 0x080903cc | ptr_lp_03cc     |
| 0x080904cc | ptr_lp_04cc     |

Slot EOL text for each: "gP1LifePoints ptr"

### RENAME_SLOTS (switchd, seg6_pool, and raw fn-ptr)

The switchd_base_f818 slot holds the switch jump-table base address 0x0808f81c.
This slot is auto-named by Ghidra and already named correctly in the asm (switchd_base_f818 was preserved
from prior segment). No rename needed -- already descriptive. NOTE: this slot is at 0x0808f818, which is
in Seg-6 territory (< 0x0808f86c); it is NOT counted in Seg-7 C13 coverage.

The 3 seg6_pool_ slots (seg6_pool_cid_con_f7e8, seg6_pool_lpflag_f7f0, seg6_pool_cid_ron_f854) are
already named from Seg-6 pool carry-over; no change needed. NOTE: these slots are also in Seg-6 territory
(< 0x0808f86c) and are NOT counted in Seg-7 C13 coverage.

**DAT_0808f934 raw fn-ptr RENAME (Seg-7 in-scope):**

| Slot addr  | Value      | GAS label          | EOL text                                                          |
|------------|------------|--------------------|-------------------------------------------------------------------|
| 0x0808f934 | 0x0808f801 | ptr_case_body_f934 | switch case body fn-ptr for find_equip_chain_node_by_pred callback |

Decode: 0x0808f801 is THUMB+1 fn-ptr to 0x0808f800 (switch-case body within Seg-6
enqueue_sprite_by_field_copy_count). Used at L22598: `ldr r2, DAT_0808f934` passed as predicate
callback to find_equip_chain_node_by_pred. Raw value stored as-is (.word 0x0808f801) -- byte-identical.
ROM raw refs: 1 (this literal pool slot only). This is a RENAME only; value unchanged.

### FUNC_RENAME

| Addr       | Old name                               | Proposed new name                     | Indeg | Evidence                                                                      |
|------------|----------------------------------------|---------------------------------------|-------|--------------------------------------------------------------------------------|
| 0x080905e8 | set_equip_activation_state_by_mode_alt | invoke_effect_node_handler_3arg       | 18    | Body: find_card_effect_node_entry -> reads node[+0x8] (target ptr, not state) -> clears [gDuelPhaseFlags+0x4bc] -> invoke_r3(card_ptr, param1, param2). No state bits are written; no "mode_alt" parameter exists. Sibling family: invoke_effect_node_handler_2arg (node[+0xc] 2-arg, indeg=7) / this (node[+0x8] 3-arg flag-clear, indeg=18) / invoke_effect_node_with_active_flag_3arg (node[+0x8] 3-arg flag-set+clear fence, indeg=78). The name "set_equip_activation_state_by_mode_alt" contradicts body which never sets equip state and has no mode parameter. Conf: high (asm/11 L24337-24372 = 0x080905e8 body). |

### PLATE (C8 stale FUN_ substitutions + CJK rewrite)

All 35 named functions have plates. Operations:

**C8 stale FUN_ substring replacements** (apply to each plate in which they appear):

| Stale FUN_       | Current name                                     | Source file/line                                        |
|------------------|--------------------------------------------------|---------------------------------------------------------|
| FUN_080487dc     | submit_lp_change_indicator_with_chain_check      | asm/04_card_zone_sprite.s:18842                         |
| FUN_0804f2e0     | dispatch_equip_field_update_by_anim_state        | asm/05_equip_eligibility_a.s:13421                      |
| FUN_08050eac     | set_equip_activation_state_by_mode               | asm/05_equip_eligibility_a.s:17732                      |
| FUN_0807ae84     | commit_serial_spell_effect_node                  | asm/10_equip_effect_dispatch.s:2236                     |
| FUN_08084cec     | invoke_effect_action_with_temp_card_id           | asm/10_equip_effect_dispatch.s:24154                    |
| FUN_0808daf0     | find_matching_slot_by_player_zone_card           | asm/11_effect_slot_puzzletext.s:18579                   |
| FUN_08090218     | dispatch_equip_field_scan_sequence               | asm/11_effect_slot_puzzletext.s:23832 (in-seg)          |
| FUN_0809077c     | invoke_count_zone_pair_hits_full_range           | asm/11_effect_slot_puzzletext.s:24583 (in-seg)          |
| FUN_08090a78     | build_equip_candidate_score_table                | asm/11_effect_slot_puzzletext.s:25030 (next seg entry)  |
| FUN_08099e0c     | run_equip_spell_display_state_machine            | asm/12_equip_activation_scan.s:12317                    |
| FUN_080a08fc     | dispatch_equip_effect_by_slot_state              | asm/13_equip_placement.s:6554                           |
| FUN_080a09c8     | dispatch_equip_lp_delta_by_slot_status           | asm/13_equip_placement.s:6671                           |
| FUN_080a1bc0     | apply_lp_delta_if_slot_active                    | asm/13_equip_placement.s:7833                           |
| FUN_0810e5d0     | invoke_r2                                        | asm/23_sound_cardlist_libc.s:15343                      |
| FUN_0810e5d4     | invoke_r3                                        | asm/23_sound_cardlist_libc.s:15349                      |
| FUN_0810e5e8     | invoke_r8                                        | asm/23_sound_cardlist_libc.s:15368                      |

**CJK plate rewrites** (two functions contain CJK in plates):

1. Function `count_effect_node_activations_by_zone` (0x080907f4, asm line 24653):
   Plate text (CJK): "由多个装备/字段效果触发路径调用 (indeg=16). 入口 r0=card_info_ptr -> r6, r1=effect_param -> r8 (via .hword 0x4688=mov r8,r1). 调用 find_card_effect_node_entry(r6, r8) 获取效果节点 r5; 清零全局计数器 [0x0201b290+0x4bc]. 若节点为 0 或 node[+0x8]==0 则返回 0. 否则循环 r4=0..0xa (11 zones), 每次调用 FUN_0810e5d4(r6, r8, r4); 返回非零则成功计数 r7++. 返回 r7 (成功激活 zone 数). 与 dispatch_card_effect_activation (0x08090848) 构成兄弟对 (后者含单播路径). Side effects: [0x0201b290+0x4bc] := 0; via FUN_0810e5d4: zone 效果节点激活状态. Constants: GLOBAL_CTR_ADDR=0x0201b290, CTR_OFFSET=0x4bc, ZONE_MAX=0xa."
   
   ASCII replacement: "Called by multiple equip/field effect paths (indeg=16). r0=card_info_ptr (r6), r1=effect_param (r8 via mov). Calls find_card_effect_node_entry; clears [gDuelPhaseFlags+PHASE_LOCK_FLAG_OFF]. If node=0 or node[+0x8]=0: return 0. Else loop r4=0..0xa (11 zones): invoke_r3(card_info_ptr, effect_param, r4); non-zero -> r7++. Returns r7=activation zone count. Sibling: dispatch_card_effect_activation (0x08090848) adds unicast path. Side effects: [gDuelPhaseFlags+0x4bc]:=0; via invoke_r3: zone effect node activation state. Constants: ZONE_MAX=0xa."

2. Function `scan_equip_chain_nodes_for_bitmap_update` (0x080909fc, asm line 24961):
   Plate text (CJK): "被 FUN_08090a78 (equip 激活主循环) 调用 (indeg=6). 入口 r0=packed_player_slot (bit0=player_side, 高位=slot index 编码), r1=slot_idx, r2=unused(由 callee-save 覆盖), r3=callback_flag. 函数体: 从 gDuelFieldSlots (0x0201c510, stride=0x868) 根据 r0/r1 计算目标格子基址, 读取 slot[+0xa] 的 chain_head 指针; 若为 0 则直接返回. 否则遍历 gDuelNodePool (0x0201d9c0, stride=8) 的链表节点: 检查 node[+2].bits[3:0] 是否==0xa; 若是, 提取 node[+0] 的 player 和 slot 字段, 调用 test_slot_has_active_card 确认目标槽位有激活卡; 若 r3 (callback_flag) 非零, 调用 enqueue_equip_slot_bitmap_update 将该槽位加入位图更新队列; 若 r3 为 0, 仅设置内部标志 r7=1. 副作用: 间接通过 enqueue_equip_slot_bitmap_update 更新 OAM 位图队列. Constants: gDuelFieldSlots=0x0201c510, gDuelNodePool=0x0201d9c0, player_stride=0x868, slot_entry=20, node_type_equip=0xa, node_stride=8."
   
   ASCII replacement: "Called by build_equip_candidate_score_table (0x08090a78, equip activation main loop, indeg=6). r0=packed_player_slot (bit0=player_side, upper=slot_idx encoded), r1=slot_idx, r3=callback_flag. Reads gDuelFieldSlots+player*PLAYER_BLOCK_STRIDE+slot*0x14; loads chain_head at slot[+0xa]; if 0 returns. Traverses gEquipNodePool (stride=8) linked list: checks node[+2].bits[3:0]==0xa (equip node type). If match: extracts player/slot from node[+0], calls test_slot_has_active_card; if r3!=0: calls enqueue_equip_slot_bitmap_update; if r3==0: sets internal flag r7=1. Constants: PLAYER_BLOCK_STRIDE=0x868, node_type_equip=0xa, node_stride=8."

**FUNC_RENAME plate update**: After renaming 0x080905e8 to invoke_effect_node_handler_3arg, update
all plates in this and other files that reference set_equip_activation_state_by_mode_alt or FUN_080905e8.
Scope: grep asm/*.s for "set_equip_activation_state_by_mode_alt" to find cross-module plate references.

## Carve Plan (R7)

None. No ROM_INCBIN or .byte blocks in this segment.

## Disasm Plan (R4)

Two 4-byte THUMB callback stubs between `dispatch_equip_field_scan_sequence` (ends 0x080904ea) and
`find_card_effect_node_entry` (starts 0x080904f4) must be disassembled and named.

ROM byte verification:
- rom[0x4ec:0x4f0] = 00 20 70 47  => `movs r0,#0; bx lr`  (returns 0)
- rom[0x4f0:0x4f4] = 02 20 70 47  => `movs r0,#2; bx lr`  (returns 2)

Steps:
1. clearListing range 0x080904ec to 0x080904f4
2. setTMode THUMB=1 for range 0x080904ec..0x080904f4
3. DisassembleCommand at 0x080904ec (4 bytes) -> createFunction at 0x080904ec
4. DisassembleCommand at 0x080904f0 (4 bytes) -> createFunction at 0x080904f0
5. getFunctionAt(0x080904ec).setName("return_effect_node_result_0", USER)
6. getFunctionAt(0x080904f0).setName("return_effect_node_result_2", USER)
7. setComment(PLATE_COMMENT, 0x080904ec, "Effect-node callback stub: returns 0. Stored as fn_activate/fn_eligible pointer in effect node descriptor tables (TYPE0/1/2/3 at 0x09e40xxx-0x09e42c58); 10 THUMB+1 refs.")
8. setComment(PLATE_COMMENT, 0x080904f0, "Effect-node callback stub: returns 2. Stored as fn_activate/fn_eligible pointer in effect node descriptor tables (TYPE0/1/2/3 at 0x09e3f6xx-0x09e452xx); 9 THUMB+1 refs.")

### New functions (CSV sync required)

| Addr       | Name                          | Notes                               |
|------------|-------------------------------|-------------------------------------|
| 0x080904ec | return_effect_node_result_0   | 4 bytes; movs r0,#0; bx lr; indeg=10 THUMB |
| 0x080904f0 | return_effect_node_result_2   | 4 bytes; movs r0,#2; bx lr; indeg=9 THUMB  |

CSV rows to add to naming-proposals.csv:
```
0x080904ec,return_effect_node_result_0,Effect-node callback stub returning 0; fn_activate/fn_eligible default in effect node tables; 10 THUMB+1 refs,high,,,
0x080904f0,return_effect_node_result_2,Effect-node callback stub returning 2; fn_activate/fn_eligible value in effect node tables; 9 THUMB+1 refs,high,,,
```

## New Constants (C5 grep-confirmed NEW)

File: `constants/card_info.inc` (append to CID section):
```
.equ BERSERK_GORILLA_CID,               0x000016bf  @ card_1410 pw=39168895; scan_field_slots_for_archfiend_equip_bitmap_update; conf: high
.equ FALLING_DOWN_CID_SHIFTED,          0xb4d00000  @ FALLING_DOWN_CID(0x169a) << 19; scan_field_slots_for_inactive_equip_bitmap_clear lsls #0x13 compare; conf: high
.equ SOUL_ABSORBING_BONE_TOWER_CID_SHIFTED, 0xba200000  @ SOUL_ABSORBING_BONE_TOWER_CID(0x1744) << 19; scan_slots_for_field_bit4_sprite_update; conf: high
.equ THE_BLOCKMAN_CID_SHIFTED,          0xc0800000  @ THE_BLOCKMAN_CID(0x1810) << 19; scan_equip_set_slot_sprite_by_counter; conf: high
.equ THEINEN_ACTIVATION_PACKED,         0x005017c9  @ THEINEN_THE_GREAT_SPHINX_CID(0x17c9)|0x00500000 flag bits; scan_card_placement_for_activation orrs r0,r1 @ 0x0808fd7c; conf: high
```

File: `constants/duel_field.inc` (append to effect node section):
```
.equ SPHINX_ACTIVATION_INIT_TEMPLATE,   0x09e3f18c  @ 4-word init template; scan_card_placement_for_activation ldmia r0!,{r2,r3,r4} @ 0x0808fc84; raw=1 thumb=0 ROM refs; conf: high
.equ EFFECT_NODE_TABLE_TYPE0_BASE,      0x09e3f19c  @ effect node BST table type=0; 0x2a3 entries x 0xc stride; find_card_effect_node_entry; raw=1 thumb=0; conf: high
.equ EFFECT_NODE_TABLE_TYPE0_COUNT,     0x000002a3  @ entry count for EFFECT_NODE_TABLE_TYPE0_BASE; conf: high
.equ EFFECT_NODE_TABLE_TYPE1_BASE,      0x09e430fc  @ effect node BST table type=1; 0x187 entries; conf: high
.equ EFFECT_NODE_TABLE_TYPE2_BASE,      0x09e455bc  @ effect node BST table type=2; 0x8e entries; conf: high
.equ EFFECT_NODE_TABLE_TYPE3_BASE,      0x09e46324  @ effect node BST table type=3; 0xb7 entries; conf: high
```

Note: EFFECT_NODE_TABLE_TYPE1_COUNT (0x187) grepped as REUSE hit against unrelated card_info.inc entry
EQUIP_PAIR_RANGE_MAX=0x00001874 which is a different value (0x1874 != 0x187). Grep hit was a false
partial match (0x187 is a substring of 0x1874). Therefore 0x00000187 requires a NEW equate:
```
.equ EFFECT_NODE_TABLE_TYPE1_COUNT,     0x00000187  @ entry count for EFFECT_NODE_TABLE_TYPE1_BASE; conf: high
```

## Section 5.1 Registration (Rule 3) -- 0 Reference Blocks

None. All data in this segment is contained in named literal pool slots within named functions.
No standalone unreferenced byte blocks exist.

## Consumer Evidence (R6)

Key semantic assignments with evidence:

| Slot/constant           | Value       | Semantic source                                                          | Conf |
|-------------------------|-------------|--------------------------------------------------------------------------|------|
| BERSERK_GORILLA_CID     | 0x16bf      | asm/11 L22980-23000: test_slot_has_active_card(card_id=0x16bf) in scan_field_slots_for_archfiend_equip_bitmap_update; card-stats.s card_1410 pw=39168895 | high |
| FALLING_DOWN_CID_SHIFTED| 0xb4d00000  | asm/11 L22951: lsls r0,r0,#0x13; cmp r0, DAT_0808fb9c(0xb4d00000); decode: 0xb4d00000>>19=0x169a | high |
| SOUL_ABSORBING_BONE_TOWER_CID_SHIFTED| 0xba200000 | asm/11 L23502: DAT_0808ffb0 in scan_slots_for_field_bit4_sprite_update; 0xba200000>>19=0x1744 | high |
| THE_BLOCKMAN_CID_SHIFTED | 0xc0800000 | asm/11 L23691: DAT_08090114 in scan_equip_set_slot_sprite_by_counter; 0xc0800000>>19=0x1810 | high |
| SPHINX_ACTIVATION_INIT_TEMPLATE | 0x09e3f18c | asm/11 L23121: DAT_0808fcdc loaded; ldmia r0!,{r2,r3,r4} @ 0x0808fc84 initializes 4-word sp buffer | high |
| EFFECT_NODE_TABLE_TYPE0_BASE | 0x09e3f19c | asm/11 L24220: DAT_08090520 in find_card_effect_node_entry type=0 branch; binary search entry_size=0xc | high |
| THEINEN_ACTIVATION_PACKED | 0x005017c9 | asm/11 L23223: DAT_0808fda4; orrs r0,r1 @ 0x0808fd7c builds OAM attr with CID+flag bits | high |
| PHASE_LOCK_FLAG_OFF (x8 slots) | 0x4bc | duel_field.inc:189; asm/11 L24365,24414,24462,24574,24650,24695,24774,24795: all str 0,[gDuelPhaseFlags+0x4bc] | high |
| EQUIP_ACTIVE_CTX_OFF (x3 slots) | 0x484 | duel_field.inc:364; asm/11 L24731,24776,24795: [gDuelPhaseFlags+0x484]=equip activation context slot ptr | high |
| EQUIP_SLOT_SCORE_CAP (x2) | 0xffff | oam_attr.inc:156; asm/11 L23644,23827: ands r4,r3 then immediate compare in score-cap path | high |
| invoke_effect_node_handler_3arg rename | 0x080905e8 | asm/11 L24337-24372: body reads node[+0x8], calls invoke_r3; no state write | high |

## C13 Coverage Statement

Seg-7 scope: code range 0x0808f86c..0x08090a78. Labels strictly within this range only.
NOTE: switchd_base_f818 (0x0808f818) and 3 seg6_pool_* labels (0x0808f7e8/f7f0/f854 and
seg6_pool_cid_ron_f854) are all at addresses < 0x0808f86c and belong to Seg-6's
enqueue_sprite_by_field_copy_count function body. They are NOT counted in Seg-7 coverage.

Actual Seg-7 auto-name slots (independent Python scan confirms 108 DAT_ + 9 PTR_ = 117):
- 108 DAT_ slots (all addrs in [0x0808f86c, 0x08090a78))
- 9 PTR_gP1LifePoints_ slots

Total in-scope: 108 + 9 = 117 slots.

Actions covering each:
- 9 PTR = 9 REF_SLOTS (RENAME as ptr_lp_xxxx)
- 107 DAT = EQ (92 REUSE + 11 NEW EQ: BERSERK_GORILLA_CID, 3 shifted CIDs,
  THEINEN_ACTIVATION_PACKED, SPHINX_ACTIVATION_INIT_TEMPLATE, 4 effect node table bases,
  EFFECT_NODE_TABLE_TYPE0_COUNT + TYPE1_COUNT)
- 1 DAT = DAT_0808f934 -> RENAME as ptr_case_body_f934 (raw THUMB+1 fn-ptr to Seg-6
  switch-case body; used as predicate callback in find_equip_chain_node_by_pred)

Total: 9 REF + 107 EQ + 1 RENAME(fn-ptr) = 117/117 slots -> 100% coverage.

Additionally: 2 new functions discovered via R4 disasm (.byte block at L24190):
- return_effect_node_result_0 @ 0x080904ec (indeg=10 THUMB+1)
- return_effect_node_result_2 @ 0x080904f0 (indeg=9 THUMB+1)
These are not DAT_ auto-name slots but referenced code stubs requiring disasm+createFunction+naming.
Both require CSV sync (new fn rows). Combined with FUNC_RENAME invoke_effect_node_handler_3arg:
total CSV impact = 3 (2 new fns + 1 FUNC_RENAME).

C13 = 100% coverage (no unaddressed DAT_/PTR_ label in Seg-7 scope remains).

## Seek Help

None. All semantics supported by file:line evidence at high confidence.
The FUNC_RENAME for 0x080905e8 is high-conf based on body analysis (asm/11 L24337-24372).
