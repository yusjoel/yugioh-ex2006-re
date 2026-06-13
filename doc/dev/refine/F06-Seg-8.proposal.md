# Refine Proposal: F06-Seg-8  [0x08058cec..0x08059de0)

## 段测绘

- 函数入口: 22 个
  - 0x08058cec  tick_equip_score_lp_display_seq
  - 0x08058e44  tick_equip_zone_select_display_seq_with_card_check
  - 0x08058f90  tick_equip_lp_row19_sprite_display_seq
  - 0x08059008  dispatch_slot_card_sprite_by_zone_type
  - 0x08059068  check_field_sarcophagus_range_and_banisher_count
  - 0x08059110  tick_equip_activation_if_field_spell_hand_ok
  - 0x08059174  tick_equip_effect_activation_display_seq__08059174
  - 0x080592c4  dispatch_equip_activation_seq_by_type25_or_5
  - 0x080592e4  check_zone_atk_buff_active_for_equip
  - 0x0805934c  tick_equip_banisher_atk_activation_display_seq
  - 0x08059430  invoke_equip_zone14_test_for_slot_entry
  - 0x08059448  tick_equip_activation_if_neo_daedalus_with_lp_row
  - 0x080594f0  submit_equip_sprite_with_set_code_cache
  - 0x0805951c  dispatch_equip_activation_seq_by_type80
  - 0x080596ec  tick_equip_banisher_lp_display_seq
  - 0x08059760  tick_equip_banisher_slot_sprite_display_seq
  - 0x08059814  tick_equip_effect_node_count_display_seq
  - 0x080598d8  tick_equip_atk_zone_sprite_display_seq
  - 0x08059a78  tick_equip_zone_bitmap_slot_display_seq
  - 0x08059b4c  tick_equip_neo_daedalus_slot_display_seq
  - 0x08059be0  enqueue_equip_zone_sprite_with_lp_tier
  - 0x08059c08  tick_equip_lp_row_spell_zone_display_seq

- 残留自动名槽: 128 total
  - DWORD_ x38  (lines 13334-15353)
  - DAT_   x69  (lines 13553-15447)
  - PTR_DAT_ x2  (08059568, 08059cf4)
  - PTR_gP1LifePoints_ x9  (08058ef4, 08059000, 0805940c, 08059738, 080597f8, 08059880, 080598d4, 08059a2c, 08059b08)
  - switchD_080598fa__ x8  (default, switchD, caseD_0..5)
  - PTR_switchdataD_08059908_08059904 x1
  - switchD_080598fa__switchdataD_08059908 x1

- ROM_INCBIN / .byte 块: 4 blocks
  - Block1: 0x0805953a size 0x2a
  - Block2: 0x08059588 size 0x164
  - Block3: 0x08059cc8 size 0x28
  - Block4: 0x08059d14 size 0xcc

---

## 数据块分类 (Rule 2/3)

ref-scan script (python, roms/2343.gba):
  for a in [block_start, ...]:
      for v in (a, a|1):
          print(hex(v), d.count(struct.pack('<I', v)))

| 块              | ref-scan (raw / THUMB+1)                               | 判定       | 理由 |
|-----------------|--------------------------------------------------------|------------|------|
| Block1 0x0805953a 0x2a | raw=0 thumb=1 @ 0x08059539 (from 0x09e46fac) | disasm R4  | THUMB+1 ref from fn-ptr table at 0x09e46fac (row for CID 0x183a). First code byte at +2 = 0xb530 = push {r4,r5,lr}; 8-case switch dispatcher via gDuelPhaseFlags+EQUIP_ACTIVATION_STEP_OFF. |
| Block2 0x08059588 0x164 | raw=8 (from PTR_DAT_08059568 table x8 entries); thumb=1 @ 0x08059615 (from 0x086f4074) | disasm R4 | 6 unique THUMB sub-fns (0x08059588, 0x80595a8, 0x80595d4, 0x8059618, 0x8059670, 0x80596d4). Dispatch table PTR_DAT_08059568 uses raw addrs (block1's 'bx r1' from ldr). THUMB+1 cross-ref to 0x08059615 (within 0x80595d4 sub-fn) from 0x086f4074 confirms THUMB code. |
| Block3 0x08059cc8 0x28 | raw=0 thumb=1 @ 0x08059cc9 (from 0x09e451dc) | disasm R4  | THUMB+1 ref from fn-ptr table at 0x09e451dc (row for CID 0x18e0). First hwords = 0xb5f0 0x1c06 = push {r4-r7,lr}; dispatch via PTR_DAT_08059cf4 using 'mov pc, r0' (ARMv4T: no mode switch, stays THUMB). |
| Block4 0x08059d14 0xcc | raw=8 (from PTR_DAT_08059cf4 x8 entries); thumb=0 | disasm R4  | 5 unique THUMB sub-fns at 0x08059d14, 0x08059d38, 0x08059d54, 0x08059d90, 0x08059dd4. Reached via raw-addr dispatch from Block3 (no THUMB+1 because 'mov pc, r0' in ARMv4T stays in current mode). Content confirmed THUMB by first hwords (0x1c30, 0x78b6, 0x1c30, 0xf7f0, 0x2001). |

---

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate; 95 slots total)

Format: (slot_addr, value, const_name, source_inc)

STATE_BASE + STEP_OFFSET cluster (very frequent: 0x0201b290 + 0x000004ac):

| slot_addr    | value       | const_name                    | source_inc       |
|--------------|-------------|-------------------------------|------------------|
| 0x08058d08   | 0x0201b290  | gDuelPhaseFlags               | ewram.inc (exist)|
| 0x08058d0c   | 0x000004ac  | EQUIP_ACTIVATION_STEP_OFF     | duel_field.inc (exist)|
| 0x08058db8   | 0x0201b290  | gDuelPhaseFlags               | ewram.inc (exist)|
| 0x08058dbc   | 0x000004ac  | EQUIP_ACTIVATION_STEP_OFF     | duel_field.inc (exist)|
| 0x08058e30   | 0x0201b290  | gDuelPhaseFlags               | ewram.inc (exist)|
| 0x08058e34   | 0x000004ac  | EQUIP_ACTIVATION_STEP_OFF     | duel_field.inc (exist)|
| 0x08058e64   | 0x0201b290  | gDuelPhaseFlags               | ewram.inc (exist)|
| 0x08058e68   | 0x000004ac  | EQUIP_ACTIVATION_STEP_OFF     | duel_field.inc (exist)|
| 0x08058eb8   | 0x0201b290  | gDuelPhaseFlags               | ewram.inc (exist)|
| 0x08058ebc   | 0x000004ac  | EQUIP_ACTIVATION_STEP_OFF     | duel_field.inc (exist)|
| 0x08058fa8   | 0x0201b290  | gDuelPhaseFlags               | ewram.inc (exist)|
| 0x08058fac   | 0x000004ac  | EQUIP_ACTIVATION_STEP_OFF     | duel_field.inc (exist)|
| 0x08059190   | 0x0201b290  | gDuelPhaseFlags               | ewram.inc (exist)|
| 0x08059194   | 0x000004ac  | EQUIP_ACTIVATION_STEP_OFF     | duel_field.inc (exist)|
| 0x08059270   | 0x0201b290  | gDuelPhaseFlags               | ewram.inc (exist)|
| 0x08059274   | 0x000004ac  | EQUIP_ACTIVATION_STEP_OFF     | duel_field.inc (exist)|
| 0x08059368   | 0x0201b290  | gDuelPhaseFlags               | ewram.inc (exist)|
| 0x0805936c   | 0x000004ac  | EQUIP_ACTIVATION_STEP_OFF     | duel_field.inc (exist)|
| 0x080593c0   | 0x0201b290  | gDuelPhaseFlags               | ewram.inc (exist)|
| 0x080593c4   | 0x000004ac  | EQUIP_ACTIVATION_STEP_OFF     | duel_field.inc (exist)|
| 0x080594b0   | 0x0201b290  | gDuelPhaseFlags               | ewram.inc (exist)|
| 0x080594b4   | 0x000004ac  | EQUIP_ACTIVATION_STEP_OFF     | duel_field.inc (exist)|
| 0x08059708   | 0x0201b290  | gDuelPhaseFlags               | ewram.inc (exist)|
| 0x0805970c   | 0x000004ac  | EQUIP_ACTIVATION_STEP_OFF     | duel_field.inc (exist)|
| 0x0805977c   | 0x0201b290  | gDuelPhaseFlags               | ewram.inc (exist)|
| 0x08059780   | 0x000004ac  | EQUIP_ACTIVATION_STEP_OFF     | duel_field.inc (exist)|
| 0x0805982c   | 0x0201b290  | gDuelPhaseFlags               | ewram.inc (exist)|
| 0x08059830   | 0x000004ac  | EQUIP_ACTIVATION_STEP_OFF     | duel_field.inc (exist)|
| 0x080598a8   | 0x0201b290  | gDuelPhaseFlags               | ewram.inc (exist)|
| 0x080598ac   | 0x000004ac  | EQUIP_ACTIVATION_STEP_OFF     | duel_field.inc (exist)|
| 0x080598fc   | 0x0201b290  | gDuelPhaseFlags               | ewram.inc (exist)|
| 0x08059900   | 0x000004ac  | EQUIP_ACTIVATION_STEP_OFF     | duel_field.inc (exist)|
| 0x08059934   | 0x0201b290  | gDuelPhaseFlags               | ewram.inc (exist)|
| 0x08059938   | 0x000004ac  | EQUIP_ACTIVATION_STEP_OFF     | duel_field.inc (exist)|
| 0x08059958   | 0x0201b290  | gDuelPhaseFlags               | ewram.inc (exist)|
| 0x0805995c   | 0x000004ac  | EQUIP_ACTIVATION_STEP_OFF     | duel_field.inc (exist)|
| 0x0805999c   | 0x0201b290  | gDuelPhaseFlags               | ewram.inc (exist)|
| 0x080599a0   | 0x000004ac  | EQUIP_ACTIVATION_STEP_OFF     | duel_field.inc (exist)|
| 0x08059a34   | 0x0201b290  | gDuelPhaseFlags               | ewram.inc (exist)|
| 0x08059a38   | 0x000004ac  | EQUIP_ACTIVATION_STEP_OFF     | duel_field.inc (exist)|
| 0x08059a60   | 0x0201b290  | gDuelPhaseFlags               | ewram.inc (exist)|
| 0x08059a64   | 0x000004ac  | EQUIP_ACTIVATION_STEP_OFF     | duel_field.inc (exist)|
| 0x08059a94   | 0x0201b290  | gDuelPhaseFlags               | ewram.inc (exist)|
| 0x08059a98   | 0x000004ac  | EQUIP_ACTIVATION_STEP_OFF     | duel_field.inc (exist)|
| 0x08059b44   | 0x0201b290  | gDuelPhaseFlags               | ewram.inc (exist)|
| 0x08059b48   | 0x000004ac  | EQUIP_ACTIVATION_STEP_OFF     | duel_field.inc (exist)|
| 0x08059b68   | 0x0201b290  | gDuelPhaseFlags               | ewram.inc (exist)|
| 0x08059b6c   | 0x000004ac  | EQUIP_ACTIVATION_STEP_OFF     | duel_field.inc (exist)|
| 0x08059c24   | 0x0201b290  | gDuelPhaseFlags               | ewram.inc (exist)|
| 0x08059c28   | 0x000004ac  | EQUIP_ACTIVATION_STEP_OFF     | duel_field.inc (exist)|
| 0x08059334   | 0x0201b290  | gDuelPhaseFlags               | ewram.inc (exist)|

LP offsets and gDuelCardCtxBase + confirm table:

| slot_addr    | value       | const_name                    | source_inc       |
|--------------|-------------|-------------------------------|------------------|
| 0x08058d88   | 0x00001da8  | LP_CARD_TRACK_BASE_OFF        | ewram.inc (exist)|
| 0x08058de0   | 0x00001da8  | LP_CARD_TRACK_BASE_OFF        | ewram.inc (exist)|
| 0x08058d90   | 0x0201e2a0  | gDuelCardCtxBase              | ewram.inc (exist)|
| 0x08058e98   | 0x0201e2a0  | gDuelCardCtxBase              | ewram.inc (exist)|
| 0x08059220   | 0x0201e2a0  | gDuelCardCtxBase              | ewram.inc (exist)|
| 0x0805987c   | 0x0201e2a0  | gDuelCardCtxBase              | ewram.inc (exist)|
| 0x08059224   | 0x00001d10  | DISPLAY_SEQ_ACTIVE_PLAYER_OFF | duel_field.inc (exist)|
| 0x08058ef8   | 0x00001d68  | ELIGIB_SPRITE_CTRL_OFF        | ewram.inc (exist)|
| 0x08058efc   | 0x00001d70  | LP_BANISHER_CTX_OFF           | ewram.inc (exist)|
| 0x08059410   | 0x00001d68  | ELIGIB_SPRITE_CTRL_OFF        | ewram.inc (exist)|
| 0x08059414   | 0x00001d70  | LP_BANISHER_CTX_OFF           | ewram.inc (exist)|
| 0x080597fc   | 0x00001d68  | ELIGIB_SPRITE_CTRL_OFF        | ewram.inc (exist)|
| 0x08059a30   | 0x00001d68  | ELIGIB_SPRITE_CTRL_OFF        | ewram.inc (exist)|
| 0x08059b0c   | 0x00001d68  | ELIGIB_SPRITE_CTRL_OFF        | ewram.inc (exist)|
| 0x08059004   | 0x00001da8  | LP_CARD_TRACK_BASE_OFF        | ewram.inc (exist)|
| 0x080593a0   | 0x0201e2a0  | gDuelCardCtxBase              | ewram.inc (exist)|

PLAYER_BLOCK_STRIDE + field/hand arrays:

| slot_addr    | value       | const_name                    | source_inc       |
|--------------|-------------|-------------------------------|------------------|
| 0x08058f48   | 0x00000868  | PLAYER_BLOCK_STRIDE           | ewram.inc (exist)|
| 0x08058f78   | 0x00000868  | PLAYER_BLOCK_STRIDE           | ewram.inc (exist)|
| 0x080591ec   | 0x00000868  | PLAYER_BLOCK_STRIDE           | ewram.inc (exist)|
| 0x0805916c   | 0x00000868  | PLAYER_BLOCK_STRIDE           | ewram.inc (exist)|
| 0x08059104   | 0x00000868  | PLAYER_BLOCK_STRIDE           | ewram.inc (exist)|
| 0x08059338   | 0x00000484  | EQUIP_ACTIVE_CTX_OFF          | duel_field.inc (exist)|
| 0x0805933c   | 0x00000868  | PLAYER_BLOCK_STRIDE           | ewram.inc (exist)|
| 0x080594ac   | 0x00000868  | PLAYER_BLOCK_STRIDE           | ewram.inc (exist)|
| 0x0805973c   | 0x00000868  | PLAYER_BLOCK_STRIDE           | ewram.inc (exist)|
| 0x08059418   | 0x00000868  | PLAYER_BLOCK_STRIDE           | ewram.inc (exist)|
| 0x08059100   | 0x0201c510  | gDuelFieldSlots               | ewram.inc (exist)|
| 0x080591f0   | 0x0201c510  | gDuelFieldSlots               | ewram.inc (exist)|
| 0x08059170   | 0x0201c8f8  | gP1HandSlotArray              | ewram.inc (exist)|
| 0x08059340   | 0x0201c600  | gP1FieldArrayCBase            | ewram.inc (exist)|
| 0x0805904c   | 0x0201bb90  | gEquipChainSlotRefs           | ewram.inc (exist)|

Card IDs (all in card_info.inc except ABYSS_SOLDIER_CID which is new):

| slot_addr    | value       | const_name                    | source_inc       |
|--------------|-------------|-------------------------------|------------------|
| 0x08058d2c   | 0x0000ffff  | SLOT_CARD_EMPTY               | card_info.inc (exist)|
| 0x08058d8c   | 0x0000ffff  | SLOT_CARD_EMPTY               | card_info.inc (exist)|
| 0x08058f00   | 0x00001895  | VAMPIRE_GENESIS_CID           | card_info.inc (exist)|
| 0x08058f04   | 0x00001727  | ABYSS_SOLDIER_CID             | card_info.inc (NEW)|
| 0x08058f10   | 0x000018cb  | DOUBLE_ATTACK_CID             | card_info.inc (exist)|
| 0x08059108   | 0x000017af  | THE_FIRST_SARCOPHAGUS_CID     | card_info.inc (exist)|
| 0x0805910c   | 0x00001332  | BANISHER_OF_THE_LIGHT_CID     | card_info.inc (exist)|
| 0x080592a4   | 0x000010d6  | AXE_OF_DESPAIR_CID            | card_info.inc (exist)|
| 0x080594ec   | 0x000010d6  | AXE_OF_DESPAIR_CID            | card_info.inc (exist)|

Misc operand constants:

| slot_addr    | value       | const_name                    | source_inc       |
|--------------|-------------|-------------------------------|------------------|
| 0x08058db4   | 0x00000199  | lookup_equip_score_mooyan_p1  | duel_field.inc (exist)|
| 0x080598a4   | 0x0000013d  | OP31_EFFECT_NODE_COUNT_CODE   | duel_field.inc (NEW)|

Total EQ_SLOTS: 51 (gDuelPhaseFlags/EQUIP_ACTIVATION_STEP_OFF) + 16 (LP offsets/confirm) + 15 (stride/arrays) + 9 (card IDs) + 2 (misc) + 2 (SLOT_CARD_EMPTY) = 95 slots.

### REF_SLOTS (USER-label + DATA-ref; RAM/ROM global or fn-ptr ref)

Format: (slot_addr, target, gas_label, slot_label)

| slot_addr    | target        | gas_label                         | slot_label (new) |
|--------------|---------------|-----------------------------------|------------------|
| 0x08058d84   | 0x0201c4e0    | gP1LifePoints                     | PTR_gP1LifePoints_08058d84 -> use gP1LifePoints directly |
| 0x08058ddc   | 0x0201c4e0    | gP1LifePoints                     | PTR_gP1LifePoints_08058ddc -> use gP1LifePoints directly |
| 0x08058dfc   | 0x0201c4e0    | gP1LifePoints                     | PTR_gP1LifePoints_08058dfc -> use gP1LifePoints directly |
| 0x08058ef4   | 0x0201c4e0    | gP1LifePoints                     | PTR_gP1LifePoints_08058ef4 (keep; already correct name) |
| 0x08059000   | 0x0201c4e0    | gP1LifePoints                     | PTR_gP1LifePoints_08059000 (keep) |
| 0x0805940c   | 0x0201c4e0    | gP1LifePoints                     | PTR_gP1LifePoints_0805940c (keep) |
| 0x080592a0   | 0x0201c4e0    | gP1LifePoints                     | PTR_gP1LifePoints_080592a0 (new) |
| 0x080594a8   | 0x0201c4e0    | gP1LifePoints                     | PTR_gP1LifePoints_080594a8 (new) |
| 0x08059738   | 0x0201c4e0    | gP1LifePoints                     | PTR_gP1LifePoints_08059738 (keep) |
| 0x080597f8   | 0x0201c4e0    | gP1LifePoints                     | PTR_gP1LifePoints_080597f8 (keep) |
| 0x08059880   | 0x0201c4e0    | gP1LifePoints                     | PTR_gP1LifePoints_08059880 (keep) |
| 0x080598d4   | 0x0201c4e0    | gP1LifePoints                     | PTR_gP1LifePoints_080598d4 (keep) |
| 0x08059a2c   | 0x0201c4e0    | gP1LifePoints                     | PTR_gP1LifePoints_08059a2c (keep) |
| 0x08059b08   | 0x0201c4e0    | gP1LifePoints                     | PTR_gP1LifePoints_08059b08 (keep) |
| 0x080593a4   | 0x080592e5    | check_zone_atk_buff_active_for_equip | fn-ptr slot: dat_check_atk_buff_predicate_08059a4 |
| 0x080593bc   | 0x080592e5    | check_zone_atk_buff_active_for_equip | fn-ptr slot: dat_check_atk_buff_predicate_08059bc |
| 0x080597b0   | 0x080905e9    | ROM fn-ptr (set_equip_activation_state_by_mode_alt param) | dat_set_equip_mode_fn_ptr_080597b0 |
| 0x08059998   | 0x080905e9    | same                              | dat_set_equip_mode_fn_ptr_08059998 |
| 0x08059acc   | 0x08050ead    | ROM fn-ptr (set_equip_activation_state_by_mode param)     | dat_set_equip_mode_fn_ptr_08059acc |
| 0x08058e9c   | 0x08065991    | ROM data ptr (equip target table) | dat_equip_target_table_ptr_08058e9c |
| 0x08058eb4   | 0x08065991    | same                              | dat_equip_target_table_ptr_08058eb4 |

Note on PTR_gP1LifePoints_ naming: DWORD_08058d84, DWORD_08058ddc, DWORD_08058dfc hold 0x0201c4e0 = gP1LifePoints but are currently named DWORD_ (not PTR_gP1LifePoints_). They should become PTR_gP1LifePoints_ labels (3 new instances to rename from DWORD_ to PTR_gP1LifePoints_). DWORD_080592a0 and DWORD_080594a8 are also gP1LifePoints and need the same treatment.

### RENAME_SLOTS (rename auto-name label + optional EOL)

All gP1LifePoints DWORD_ -> PTR_gP1LifePoints_ renames (5 items that are currently DWORD_ but hold gP1LifePoints value):

| slot_addr  | current_label        | new_label                      | eol (ASCII) |
|------------|----------------------|--------------------------------|-------------|
| 0x08058d84 | DWORD_08058d84       | PTR_gP1LifePoints_08058d84     | (none) |
| 0x08058ddc | DWORD_08058ddc       | PTR_gP1LifePoints_08058ddc     | (none) |
| 0x08058dfc | DWORD_08058dfc       | PTR_gP1LifePoints_08058dfc     | (none) |
| 0x080592a0 | DWORD_080592a0       | PTR_gP1LifePoints_080592a0     | (none) |
| 0x080594a8 | DWORD_080594a8       | PTR_gP1LifePoints_080594a8     | (none) |

switchD rename plan (tick_equip_atk_zone_sprite_display_seq 6-state switch):

| current_label                          | new_label                                       |
|----------------------------------------|-------------------------------------------------|
| switchD_080598fa__default              | tick_equip_atk_zone_seq__default                |
| switchD_080598fa__switchD              | tick_equip_atk_zone_seq__dispatch               |
| PTR_switchdataD_08059908_08059904      | tick_equip_atk_zone_seq__table_ptr              |
| switchD_080598fa__switchdataD_08059908 | tick_equip_atk_zone_seq__table                  |
| switchD_080598fa__caseD_0              | tick_equip_atk_zone_seq__case_op31_0x1a         |
| switchD_080598fa__caseD_1              | tick_equip_atk_zone_seq__case_init_ctx          |
| switchD_080598fa__caseD_2              | tick_equip_atk_zone_seq__case_get_monster_slot  |
| switchD_080598fa__caseD_3              | tick_equip_atk_zone_seq__case_set_mode_alt      |
| switchD_080598fa__caseD_4              | tick_equip_atk_zone_seq__case_check_confirmed   |
| switchD_080598fa__caseD_5              | tick_equip_atk_zone_seq__case_submit_sprite     |

Also rename: PTR_DAT_08059568 -> equip_type80_dispatch_table_ptr (8-entry dispatch for Block1 fn)
Also rename: PTR_DAT_08059cf4 -> equip_lp_spell_zone_dispatch_table_ptr (8-entry dispatch for Block3 fn)
Also rename: DAT_08059588 label -> equip_type80_case_fns (Block2 start label; removed by disasm)

DAT_ -> descriptive slot labels (fn-ptr / const data slots not covered by EQ/REF above):

| slot_addr  | current_label     | new_label / action             | eol (ASCII) |
|------------|-------------------|--------------------------------|-------------|
| 0x080593a4 | DAT_080593a4      | dat_check_atk_buff_predicate_a | fn-ptr: check_zone_atk_buff_active_for_equip+1 |
| 0x080593bc | DAT_080593bc      | dat_check_atk_buff_predicate_b | fn-ptr: check_zone_atk_buff_active_for_equip+1 |
| 0x080597b0 | DAT_080597b0      | dat_set_equip_mode_fn_ptr_a    | fn-ptr: 0x080905e9 (mode_alt fn) |
| 0x08059998 | DAT_08059998      | dat_set_equip_mode_fn_ptr_b    | fn-ptr: 0x080905e9 (same) |
| 0x08059acc | DAT_08059acc      | dat_set_equip_mode_fn_ptr_c    | fn-ptr: 0x08050ead (mode fn) |
| 0x08058e9c | DAT_08058e9c      | dat_equip_target_table_ptr_a   | ROM data: equip target slot table at 0x08065991 |
| 0x08058eb4 | DAT_08058eb4      | dat_equip_target_table_ptr_b   | ROM data: equip target slot table at 0x08065991 |

### FUNC_RENAME (none)

No function renames required. All 22 function names in Seg-8 are semantically correct.

### PLATE (R5; CJK rewrite + stale FUN_ substring fix)

Three plate actions:

**PLATE-1**: asm/06_equip_eligibility_b.s line 13934 (before tick_equip_activation_if_field_spell_hand_ok @ 0x08059110)
- Current: CJK mojibake -- Chinese text contains kanji.
- Action: Full ASCII rewrite.
- New plate text (ASCII):
  "Conditional entry wrapper for equip activation state machine. Prerequisite: check_equip_slot_eligible_field_spell_by_hand_set_code_dispatch checks field-spell hand set_code; returns -1 if fails. If pass: calls tick_equip_activation_state_machine; if tick returns 1 (slot selected), extracts set_code from card_entry[+4] bits[14:6] (9-bit, lsls#0x11/lsrs#0x17), calls find_hand_slot_idx_by_set_code, then enqueue_equip_zone_sprite_by_slot_ptr. Propagates tick return value. indeg=0, Sub-type A."
- Confidence: high (asm/06_equip_eligibility_b.s line 13936-13979 consumed directly).

**PLATE-2**: asm/06_equip_eligibility_b.s line 14404 (before tick_equip_activation_if_neo_daedalus_with_lp_row @ 0x08059448)
- Current: CJK mojibake + stale name "FUN_08058550".
- stale FUN_: FUN_08058550 = tick_equip_activation_neo_daedalus_gate (from commit log / asm/06_equip_eligibility_b.s grep).
- Action: Full ASCII rewrite, replacing FUN_08058550 with tick_equip_activation_neo_daedalus_gate.
- New plate text (ASCII):
  "Conditional entry wrapper for equip activation state machine combining Neo Daedalus eligibility check and effect dispatch. Called by tick_equip_activation_neo_daedalus_gate (indeg=1). Prerequisite: check_neo_daedalus_placement_eligible; returns -1 if fails. If pass: iterates effect node chain and drives tick_equip_activation_state_machine. Step counter [gDuelPhaseFlags+0x4ac]==0: calls trigger_card_display_op31_if_not_active(op=0x122); ==1: calls set_lp_display_row_all_slots(opponent, AXE_OF_DESPAIR_CID). Exit: pop{r1}; bx r1 Sub-case E."
- Confidence: high (asm/06_equip_eligibility_b.s lines 14406-14491 + caller grep).

**PLATE-3**: asm/06_equip_eligibility_b.s line 14198 (before check_zone_atk_buff_active_for_equip @ 0x080592e4)
- Current: contains stale "FUN_0805934c".
- stale FUN_: FUN_0805934c = tick_equip_banisher_atk_activation_display_seq (from asm line 14271).
- Action: substring replace "FUN_0805934c" with "tick_equip_banisher_atk_activation_display_seq".
- Confidence: high (asm/06_equip_eligibility_b.s line 14271 shows the renamed function).

---

## disasm 计划 (R4)

**Block1 @ 0x0805953a (0x2a bytes)**
- Effective code range: 0x0805953c..0x08059563 (skip 2 leading .zero bytes)
- Structure: push {r4,r5,lr}; loads gDuelPhaseFlags+EQUIP_ACTIVATION_STEP_OFF; cmp r0,#7; bhi default; 8-case dispatch via PTR_DAT_08059568 (ldr + bx r1)
- Literal pool at 0x0805955c..0x08059567: LP[0]=gDuelPhaseFlags, LP[1]=EQUIP_ACTIVATION_STEP_OFF, LP[2]=PTR_DAT_08059568
- Default branch target: 0x080596e4 (return 0 stub inside Block2)
- GAS label for function: equip_type80_activation_case_dispatch (or reuse context from existing `dispatch_equip_activation_seq_by_type80`)
- Note: The 2-byte .zero at 0x0805953a is alignment padding; code starts at 0x0805953c
- PTR_DAT_08059568 (8-entry table) becomes labeled within disasm output; no separate carve needed

**Block2 @ 0x08059588 (0x164 bytes)**
- 6 unique THUMB sub-fns:
  - equip_type80_case0_and_1_init_sprite @ 0x08059588 (cases 0 and 1)
  - equip_type80_case1_also @ 0x080595a8 (case 1 second entry)
  - equip_type80_case2_and_5_no_op @ 0x080595d4 (cases 2 and 5)
  - equip_type80_case3_and_6_select_target @ 0x08059618 (cases 3 and 6)
  - equip_type80_case4_enqueue @ 0x08059670 (case 4)
  - equip_type80_case7_and_return0 @ 0x080596d4 (case 7 + default return 0)
- Dispatch table PTR_DAT_08059568 already labeled; 8 entries map to these 6 fns
- Note: sub-fns are reached via `ldr r1, [pc,#offset]; bx r1` from Block1; entries are raw THUMB addrs without +1 (the bx instruction checks lsb of r1 = lsb of raw THUMB addr = 0, so this switches to ARM... 
  - Actually: 0x08059588 lsb=0 -> ARM mode would be selected by BX. BUT 0x2000 = movs r0,#0 is THUMB. This means the dispatch table must also have lsb=0 and the code remains THUMB. Check: ARMv4T BX with even addr -> switches to ARM. But 0x2000 at 0x08059588 is definitely THUMB. Contradiction - verify by checking if the entries actually have +1 in the table.
  - Re-reading PTR_DAT_08059568 entries from asm (line 14546-14553): values are 0x08059588, 0x080595a8, etc. - all even (lsb=0). When BX r1 with lsb=0 -> ARM mode. But 0x2000 at 0x08059588 is THUMB...
  - Resolution: In ARMv4T, if you BX to an even address, execution switches to ARM. The `movs r0,#0` in ARM 32-bit encoding is different from THUMB. ARM `movs r0,#0` = 0xe3b00000. But ROM at 0x08059588 = 0x2000 (16-bit). This is inconsistent if BX switches to ARM.
  - Most likely the dispatch in Block1 uses different mechanism. Re-read Block1: `ldr r1,[pc,#0xc]` at +0x1a in Block1 loads LP[2]=0x08059568 (the table ptr). Then `adds r0,r0,r1` and `ldr r0,[r0]` = loads table entry into r0. Then at +0x1c = `bx r1` where r1 is still the step-indexed value? No. Let me re-check Block1 decode.

  Actually re-reading Block1 more carefully:
  - Block1 literal pool: LP[0]=0x0201b290 (gDuelPhaseFlags), LP[1]=0x000004ac (EQUIP_STEP_OFF), LP[2]=0x08059568 (table ptr)
  - Code: ldr r0,[pc,#offset] -> LP[0]; ldr r1,[pc,#offset] -> LP[1]; adds r0,r0,r1; ldr r0,[r0] -> state step word; cmp r0,#7; bhi default; lsls r0,r0,#2; ldr r1,[pc,#offset] -> LP[2]=0x08059568; adds r0,r0,r1; ldr r0,[r0] -> table[step]; bx r0
  - So BX r0 with r0 = 0x08059588 (lsb=0) -> ARM mode switch. Hmm.
  - BUT actual GBA ROMs use this pattern where BX to even address works as THUMB if the table uses THUMB+1 entries. Let me re-verify by re-reading PTR_DAT_08059568 actual bytes.

  Re-read asm lines 14545-14553: these are the .word entries already disassembled showing:
    .word 0x08059588  @ 08059568 88950508
  The raw bytes at ROM offset 0x59568 would be 0x88 0x95 0x05 0x08 which as LE word = 0x08059588.
  0x08059588 lsb=0 -> ARM mode if BX'd. But 0x2000 at 0x59588 is THUMB `movs r0,#0`.

  The only resolution: this dispatch must NOT use BX. Block1 actually uses a different mechanism. Given our decoded bytes: at +0x1c = 0x4687 = 'mov pc, r0' (stays THUMB). So Block1 dispatches to table entries via 'mov pc,r0', NOT 'bx r0'. ARMv4T: MOV PC, Rn does NOT change mode. So all sub-fns are THUMB, and table entries are raw (even) addresses. This is consistent.

  Block2 sub-fns are THUMB; entries in PTR_DAT_08059568 are raw THUMB addresses (no +1 needed because dispatch is via 'mov pc, r0', not BX).

**Block3 @ 0x08059cc8 (0x28 bytes)**
- Function: equip_lp_spell_zone_case_dispatch
- push {r4-r7,lr}; loads gDuelPhaseFlags+EQUIP_ACTIVATION_STEP_OFF; cmp r0,#7; bhi @ +0xe07b (far jump); dispatch via PTR_DAT_08059cf4 (lsls r0,r0,#2; ldr r1,[pc,#0x10]; adds r0,r0,r1; ldr r0,[r0]; mov pc, r0)
- Literal pool at 0x08059ce0 (+0x18 from code start): [0x08059cf0]=0x08059cf4 (table ptr at 0x08059cf0), but the LP load is from [pc+#0x10] at 0x08059cde = PC=0x08059ce2 & ~2 + 0x10 = 0x08059cf0
- THUMB+1 ref from 0x09e451dc confirmed (fn-ptr table for CID 0x18e0)

**Block4 @ 0x08059d14 (0xcc bytes)**
- 5 unique THUMB sub-fns (reached via raw-addr dispatch from Block3):
  - equip_lp_spell_zone_case_shared_abc @ 0x08059d14 (cases 0,1,2)
  - equip_lp_spell_zone_case5_op31 @ 0x08059d38 (case 5)
  - equip_lp_spell_zone_case6_something @ 0x08059d54 (case 6)
  - equip_lp_spell_zone_case7_something @ 0x08059d90 (case 7)
  - equip_lp_spell_zone_case34_return1 @ 0x08059dd4 (cases 3,4)
- Dispatch table PTR_DAT_08059cf4 (8 entries, all raw addrs in Block4) already labeled

Disasm approach for all 4 blocks: R4 per-entry DisassembleCommand (not single-range), clear listing first, setTMode for THUMB before disasm.

---

## carve 計画 (R7)

None required. All 4 ROM_INCBIN blocks are THUMB code -> R4 disasm, not data carve.

PTR_DAT_08059568 and PTR_DAT_08059cf4 dispatch tables are already present in asm as labeled .word entries and will be properly labeled after Block1/Block3 disasm provides context labels for their entries.

---

## §5.1 登記 (Rule 3) -- 0 引用块

None. All 4 ROM_INCBIN blocks have real references:
- Block1: 1 THUMB+1 ref (0x09e46fac)
- Block2: cross-refs from Block1 dispatch table + external THUMB+1 ref
- Block3: 1 THUMB+1 ref (0x09e451dc)
- Block4: 8 raw refs from Block3 dispatch table

---

## 消費者証拠 (R6)

| 槽 / 全局                                   | file:line                                      | 置信度 |
|---------------------------------------------|------------------------------------------------|--------|
| gDuelPhaseFlags=0x0201b290                   | asm/06_equip_eligibility_b.s:13335             | high   |
| EQUIP_ACTIVATION_STEP_OFF=0x000004ac        | asm/06_equip_eligibility_b.s:13337 (added r0+r1 = step counter addr) | high |
| gP1LifePoints=0x0201c4e0                     | asm/06_equip_eligibility_b.s:13401 (already labeled DWORD_08058d84 -> gP1LifePoints .word) | high |
| LP_CARD_TRACK_BASE_OFF=0x00001da8           | asm/06_equip_eligibility_b.s:13403 (adds r1,r5,r2 = gP1LifePoints+player*stride+0x1da8) | high |
| VAMPIRE_GENESIS_CID=0x00001895              | asm/06_equip_eligibility_b.s:13631 (cmp r1,r0 where r0 from DAT_08058f00=0x1895; card_entry icid comparison) | high |
| ABYSS_SOLDIER_CID=0x00001727               | asm/06_equip_eligibility_b.s:13633 (cmp r1,r0 where r0 from DAT_08058f04=0x1727); data/card-stats.s line ~19515 (CID 0x1727 = Abyss Soldier, pw=18318842) | high |
| DOUBLE_ATTACK_CID=0x000018cb               | asm/06_equip_eligibility_b.s:13640 (cmp r1,r0 where r0 from DAT_08058f10=0x18cb) | high |
| THE_FIRST_SARCOPHAGUS_CID=0x000017af       | asm/06_equip_eligibility_b.s:13930 (DWORD_08059108 = 0x17af; cmp in sarcophagus range check) | high |
| BANISHER_OF_THE_LIGHT_CID=0x00001332       | asm/06_equip_eligibility_b.s:13932 (DWORD_0805910c = 0x1332; arg to count_field_copies_of_card) | high |
| AXE_OF_DESPAIR_CID=0x000010d6              | asm/06_equip_eligibility_b.s:14154 (DWORD_080592a4 = 0x10d6; arg to set_lp_display_row_all_slots) | high |
| ELIGIB_SPRITE_CTRL_OFF=0x00001d68          | asm/06_equip_eligibility_b.s:13627 (DAT_08058ef8 = 0x1d68; adds r0,r6+r1 = gP1LifePoints+player*stride+0x1d68) | high |
| LP_BANISHER_CTX_OFF=0x00001d70             | asm/06_equip_eligibility_b.s:13629 (DAT_08058efc = 0x1d70) | high |
| DISPLAY_SEQ_ACTIVE_PLAYER_OFF=0x00001d10   | asm/06_equip_eligibility_b.s:14092 (DWORD_08059224 = 0x1d10; str to confirm table) | high |
| gDuelCardCtxBase=0x0201e2a0                 | asm/06_equip_eligibility_b.s:13407 (DWORD_08058d90; used as confirm table base) | high |
| gDuelFieldSlots=0x0201c510                  | asm/06_equip_eligibility_b.s:13926 (DWORD_08059100 = 0x0201c510) | high |
| gEquipChainSlotRefs=0x0201bb90             | asm/06_equip_eligibility_b.s:13820 (DAT_0805904c = 0x0201bb90; ldr r3 then r1=[r3+4]) | high |
| gP1FieldArrayCBase=0x0201c600              | asm/06_equip_eligibility_b.s:14250 (DAT_08059340 = 0x0201c600) | high |
| gP1HandSlotArray=0x0201c8f8                | asm/06_equip_eligibility_b.s:13984 (DWORD_08059170 = 0x0201c8f8; hand slot array base) | high |
| EQUIP_ACTIVE_CTX_OFF=0x00000484            | asm/06_equip_eligibility_b.s:14246 (DAT_08059338 = 0x484; adds r6,r0+r3 = gDuelPhaseFlags+0x484 = active ctx ptr) | high |
| lookup_equip_score_mooyan_p1=0x00000199    | asm/06_equip_eligibility_b.s:13426 (DWORD_08058db4 = 0x199; arg to invoke_card_display_op_0x31_sub3_with_packed_params) | high |
| OP31_EFFECT_NODE_COUNT_CODE=0x0000013d     | asm/06_equip_eligibility_b.s:14826 (DAT_080598a4 = 0x13d; first arg to invoke_card_display_op_0x31_sub10) | high |
| check_zone_atk_buff_active_for_equip fn-ptr | asm/06_equip_eligibility_b.s:14316 (DAT_080593a4 = 0x080592e5; passed to select_equip_target_slot_by_card_id) | high |

---

## 新增 constants / 全局

1. **card_info.inc** (add):
   ```
   ABYSS_SOLDIER_CID = 0x00001727
   ```
   Evidence: data/card-stats.s line ~19515 (CID slot 0x1727, password=18318842 = Abyss Soldier).
   Usage: asm/06_equip_eligibility_b.s lines 13632-13633 (DAT_08058f04 used in cmp after card_id reads).
   C5 check: grep constants/card_info.inc shows no 0x1727 value (verified pre-survey). New entry needed.

2. **duel_field.inc** (add):
   ```
   OP31_EFFECT_NODE_COUNT_CODE = 0x0000013d
   ```
   Evidence: asm/06_equip_eligibility_b.s line 14826 (DAT_080598a4 = 0x13d passed as first arg to invoke_card_display_op_0x31_sub10). Function name "invoke_card_display_op_0x31_sub10" confirms this is sub-op #10 dispatch code 0x13d.
   C5 check: grep constants/ for 0x13d shows no existing match. Value is also not 0x9f<<1=0x13e (which is the LP_ROW_OFF used 2 slots above) so no collision. New entry needed.

---

## 求助

None. All slots and blocks have high-confidence semantic evidence.

---

## Executor Report: F06-Seg-8

- 槽: EQ=95 REF=21 RENAME=17 (5 DWORD_->PTR_gP1LP_ + 10 switchD_/PTR_switchdataD_ + 2 PTR_DAT_ table names + 7 DAT_ fn-ptr/table slots) FUNC_RENAME=0 PLATE=3
- disasm=4 ranges: Block1 0x0805953c/0x28B + Block2 0x08059588/0x164B + Block3 0x08059cc8/0x28B + Block4 0x08059d14/0xCCB
- carve=0
- §5.1=0 (all 4 ROM_INCBIN blocks have real references)
- 新增 constants/全局: card_info.inc +1 (ABYSS_SOLDIER_CID=0x1727), duel_field.inc +1 (OP31_EFFECT_NODE_COUNT_CODE=0x13d)
- 求助: none
- proposal: doc/dev/refine/F06-Seg-8.proposal.md
- 落地备注: fixer 落地时须同步订正活动 refine doc §五 Seg-9 路线图行: 删除其中 "ROM_INCBIN 0x59cc8/0x28" 和 "ROM_INCBIN 0x59d14/0xcc" 两项 (实际属 Seg-8 范围, 已在本段 disasm 处理); Seg-9 实际仅剩 ROM_INCBIN 0x5a0aa/0x36 + 0x5a0f8/0xe4.
