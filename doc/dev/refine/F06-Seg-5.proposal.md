# Refine Proposal: F06-Seg-5  [0x080565e8..0x08057458)

## Segment Survey

- Function entries: 23
  - 0x080565e8 tick_equip_activation_with_lp_cost_sprite
  - 0x08056614 enqueue_equip_card_sprite_mode3
  - 0x0805663c tick_equip_activation_with_slot_sprite_mode4
  - 0x08056658 update_equip_slot_zone_flag_sprite
  - 0x080566cc tick_equip_activation_with_type11_sprite
  - 0x080566f4 trigger_equip_lp_sprite_by_activation_state
  - 0x080567a0 enqueue_lp_display_row_clear_for_card_player
  - 0x080567bc dispatch_equip_card_name_display_by_step
  - 0x08056874 check_equip_slot_zone_has_card
  - 0x080568d0 update_equip_chain_pair_sprites_and_atk_field
  - 0x08056930 tick_equip_score_sprite_display_seq
  - 0x08056ba0 dispatch_equip_direct_type_zone_sprite
  - 0x08056bc4 dispatch_equip_activation_score_by_card_id
  - 0x08057138 enqueue_chain_node_sprite_for_equip_entry
  - 0x0805715c tick_equip_activation_state_by_phase
  - 0x08057270 enqueue_lp_display_row_from_slot_id_field
  - 0x08057294 tick_equip_activation_if_neo_daedalus_eligible
  - 0x080572b8 traverse_equip_zone_nodes_for_lp_score
  - 0x08057344 enqueue_equip_slot_sprite_mode4
  - 0x0805735c enqueue_equip_slot_sprite_mode4_and_lp_cost
  - 0x0805738c tick_equip_zone14_test_display_seq
  - 0x08057430 tick_equip_activation_lp_cost_sprite_by_type
  - 0x08057458 set_lp_row_type2_fixed_for_equip_player (boundary fn, straddles Seg-5/6)
- Residual auto-name slots: 117 total (117 unique definitions)
  - 101 DAT_/DWORD_ type (19 DWORD_ + 82 DAT_), 16 PTR_gP1LifePoints_*
- ROM_INCBIN / .byte blocks: none (confirmed by grep; roadmap note was accurate)

Python slot count verification: 117 slot definitions found in lines 7237..9445
(scan extended to line 7237 to include tick_equip_activation_with_lp_cost_sprite plate area;
4 additional DWORD_gP1LifePoints slots at 0x0805673c/0x0805678c/0x0805680c/0x08056858
identified vs original 101 count).

## Data Block Classification (Rule 2/3) -- ref-scan

No ROM_INCBIN or .byte data blocks in Seg-5. All 117 slots are .word literal pool entries
embedded inline in function bodies. No carve, no disasm, no para.5.1 blocks needed.

## Symbol Plan (R1/R2/R3)

### EQ_SLOTS  (data-equate; 82 slots; all reuse existing constants or new per table below)

Values found in segment, grouped by constant:

**ewram.inc -- gP1LifePoints (0x0201c4e0):**
All 16 PTR_gP1LifePoints_* definitions carry this value.
They are REF slots (see REF_SLOTS section below).

**ewram.inc -- PLAYER_BLOCK_STRIDE (0x00000868): 11 slots**
- DWORD_08056740 @ 0x08056740  (trigger_equip_lp_sprite_by_activation_state)
- DAT_080568bc  @ 0x080568bc  (check_equip_slot_zone_has_card)
- DWORD_08056928 @ 0x08056928  (update_equip_chain_pair_sprites_and_atk_field)
- DAT_08056b2c  @ 0x08056b2c  (tick_equip_score_sprite_display_seq branch 0x1708)
- DAT_08056b58  @ 0x08056b58  (tick_equip_score_sprite_display_seq branch 0x1927)
- DAT_08056d1c  @ 0x08056d1c  (dispatch_equip_activation_score_by_card_id 0x15cf path)
- DAT_08056e5c  @ 0x08056e5c  (dispatch_equip_activation_score_by_card_id 0x1841 path)
- DAT_08056ec4  @ 0x08056ec4  (dispatch_equip_activation_score_by_card_id 0x1841 path 2)
- DAT_08057340  @ 0x08057340  (traverse_equip_zone_nodes_for_lp_score)
- DAT_0805741c  @ 0x0805741c  (tick_equip_zone14_test_display_seq)
- DAT_080570cc  @ 0x080570cc  (dispatch_equip_activation_score_by_card_id state=2 0x15cf)
  slot labels: tick_equip_score_sprite_display_seq_stride, etc.

**ewram.inc -- gDuelPhaseFlags (0x0201b290): 11 slots**
- DWORD_08056758 @ 0x08056758
- DWORD_080567e0 @ 0x080567e0
- DWORD_0805683c @ 0x0805683c
- DAT_08056954  @ 0x08056954
- DAT_08056a18  @ 0x08056a18
- DAT_08056bf4  @ 0x08056bf4
- DAT_08056fb8  @ 0x08056fb8
- DAT_080572e8  @ 0x080572e8
- DAT_08057178  @ 0x08057178
- DAT_080571d0  @ 0x080571d0
- DAT_080573a4  @ 0x080573a4
  (Each slot label: <enclosing_func>_phase_flags or _duel_flags)

**duel_field.inc -- EQUIP_ACTIVATION_STEP_OFF (0x000004ac): 12 slots**
- DWORD_0805675c @ 0x0805675c
- DWORD_080567e4 @ 0x080567e4
- DWORD_08056840 @ 0x08056840
- DAT_08056958  @ 0x08056958
- DAT_08056a1c  @ 0x08056a1c
- DAT_08056bf8  @ 0x08056bf8
- DAT_08056fbc  @ 0x08056fbc
- DAT_08057208  @ 0x08057208
- DAT_0805717c  @ 0x0805717c
- DAT_080571d4  @ 0x080571d4
- DAT_080573a8  @ 0x080573a8
- DAT_080572ec  @ 0x080572ec
  (Each slot label: <enclosing_func>_step_off)

**ewram.inc -- gDuelCardCtxBase (0x0201e2a0): 4 slots**
Confirmed: ewram.inc line 218: `.equ gDuelCardCtxBase, 0x0201e2a0`
- DWORD_08056738 @ 0x08056738  (trigger_equip_lp_sprite_by_activation_state; reads [+player_id*4+8])
- DWORD_08056808 @ 0x08056808  (dispatch_equip_card_name_display_by_step)
- DAT_08056efc  @ 0x08056efc  (dispatch_equip_activation_score_by_card_id, reads activation state)
- DAT_080571b8  @ 0x080571b8  (tick_equip_activation_state_by_phase)
  slot labels: <func>_card_ctx_base

**ewram.inc -- gDuelFieldSlots (0x0201c510): 3 slots**
Confirmed: ewram.inc line 311.
- DAT_080568c0  @ 0x080568c0  (check_equip_slot_zone_has_card zone base)
- DWORD_0805692c @ 0x0805692c  (update_equip_chain_pair_sprites_and_atk_field zone base)
- DAT_080570d0  @ 0x080570d0  (dispatch_equip_activation_score_by_card_id state=2 zone base)
  slot labels: <func>_zone_base

**ewram.inc -- ELIGIB_SPRITE_CTRL_OFF (0x00001d68): 2 slots**
Confirmed: ewram.inc line 417.
- DAT_08056a64  @ 0x08056a64  (tick_equip_score_sprite_display_seq; reads activation state)
- DAT_08057418  @ 0x08057418  (tick_equip_zone14_test_display_seq; reads LP P1 field)
  slot labels: <func>_eligib_sprite_off

**ewram.inc -- ELIGIB_ANIM_STATE_OFF (0x00001d6c): 1 slot**
Confirmed: ewram.inc line 418.
- DAT_08056a68  @ 0x08056a68  (tick_equip_score_sprite_display_seq)
  slot label: tick_equip_score_sprite_display_seq_anim_off

**duel_field.inc -- FIELD_STATE_OFF (0x00001cf4): 2 slots**
Confirmed: duel_field.inc line 205.
- DAT_08056d54  @ 0x08056d54  (dispatch_equip_activation_score_by_card_id; checks [gP1LP+0x1cf4]==2)
- DAT_08056ec8  @ 0x08056ec8  (dispatch_equip_activation_score_by_card_id; reads field-spell state)
  slot labels: <func>_field_state_off

**card_info.inc -- SLOT_CARD_EMPTY (0x0000ffff) -- 3 slots**
Confirmed: card_info.inc line 386 `.equ SLOT_CARD_EMPTY, 0x0000ffff`.
Usage in each case is "clear/sentinel" or "invalid zone" -- C5 says value 0xffff must reuse.
- DAT_080566a4  @ 0x080566a4  (update_equip_slot_zone_flag_sprite; cmp r1,r0 checks 0xffff = INVALID_ZONE)
- DWORD_080567b8 @ 0x080567b8  (enqueue_lp_display_row_clear_for_card_player; set_lp_display_row_type8 with 0xffff=clear)
- DAT_08057054  @ 0x08057054  (dispatch_equip_activation_score_by_card_id; set_lp_display_row_type8 with 0xffff)
  slot labels: <func>_invalid_zone or <func>_lp_row_clear

**duel_field.inc -- SCENE_SLOT_MASK_LO (0x00000fff): 1 slot**
Confirmed: duel_field.inc line 56 `.equ SCENE_SLOT_MASK_LO, 0x00000fff`.
- DAT_08056a74  @ 0x08056a74  (tick_equip_score_sprite_display_seq; used in BST branch cmp)
  slot label: tick_equip_score_sprite_display_seq_cid_0fff

**card_info.inc -- get_card_lp_cost_by_id_cid_11cf (0x000011cf): 1 slot**
Confirmed: card_info.inc line 1052.
- DWORD_08056838 @ 0x08056838  (dispatch_equip_card_name_display_by_step; card_name_lookup_by_internal_id arg)
  slot label: dispatch_equip_card_name_display_by_step_reserved_icid

**oam_attr.inc -- OAM_ATTR1_X_CLEAR (0xfffffe00): 1 slot**
Confirmed: oam_attr.inc line 19. C5 strict dedup applies.
Usage: DAT_08056950 loaded into r4 then `add sp,r4` to sub 512 from sp (stack frame setup).
Semantically a negative stack-frame-delta but C5 forbids new constant with same value.
- DAT_08056950  @ 0x08056950  (tick_equip_score_sprite_display_seq; sub sp,#0x200 idiom via add sp,r4)
  slot label: tick_equip_score_sprite_display_seq_frame_neg
  EOL: "sub sp,#0x200 idiom: add sp,r4 where r4=0xfffffe00 (= -512); stack frame alloc"

**duel_field.inc -- TRIGGER_OP_PARAM_107 (0x00000107): 1 slot**
Confirmed: duel_field.inc line 311.
- DAT_080572f0  @ 0x080572f0  (traverse_equip_zone_nodes_for_lp_score; trigger_card_display_op31_if_not_active second arg)
  slot label: traverse_equip_zone_nodes_for_lp_score_op_param

**Card ID equates -- reuse from card_info.inc (23 CIDs, 29 slots):**

| slot | addr | value | existing_const | source |
|---|---|---|---|---|
| DAT_08056980 | 0x08056980 | 0x1713 | DEDICATION_THROUGH_LIGHT_DARK_CID | card_info.inc line 812 |
| DAT_08056984 | 0x08056984 | 0x167d | KNIGHTS_TITLE_CID | card_info.inc line 958 |
| DAT_0805699c | 0x0805699c | 0x192a | SPIRITUAL_WIND_ART_MIYABI_CID | card_info.inc line 934 |
| DAT_080569a8 | 0x080569a8 | 0x19b5 | ATTACK_REFLECTOR_UNIT_CID | NEW -- see below |
| DAT_080569b4 | 0x080569b4 | 0x0fc9 | DARK_MAGICIAN_CID_0FC9 | card_info.inc line 310 |
| DAT_080569bc | 0x080569bc | 0x13c3 | GEARFRIED_IRON_KNIGHT_CID | card_info.inc line 446 |
| DAT_080569c4 | 0x080569c4 | 0x18f6 | CYBER_DRAGON_CID | card_info.inc line 762 |
| DAT_08056a6c | 0x08056a6c | 0x1708 | ORCA_MEGA_FORTRESS_OF_DARKNESS_CID | card_info.inc line 928 |
| DAT_08056a70 | 0x08056a70 | 0x140b | INSECT_IMITATION_CID | card_info.inc line 952 |
| DAT_08056a74 | 0x08056a74 | 0x0fff | SCENE_SLOT_MASK_LO | duel_field.inc line 56 (CID domain: Catapult Turtle, but C5 dedup applies) |
| DAT_08056a88 | 0x08056a88 | 0x14e4 | BURST_BREATH_CID | card_info.inc line 905 |
| DAT_08056aa4 | 0x08056aa4 | 0x1927 | SPIRITUAL_EARTH_ART_CID | card_info.inc line 968 |
| DAT_08056aa8 | 0x08056aa8 | 0x1768 | NINJITSU_ART_OF_TRANSFORMATION_CID | card_info.inc line 572 |
| DAT_08056abc | 0x08056abc | 0x1929 | SPIRITUAL_FIRE_ART_CID | NEW -- see below |
| DAT_08056c2c | 0x08056c2c | 0x15e7 | POISON_OF_THE_OLD_MAN_CID | NEW -- see below |
| DAT_08056c30 | 0x08056c30 | 0x1298 | CYBER_RAIDER_CID | NEW -- see below |
| DAT_08056c48 | 0x08056c48 | 0x15cf | KIRYU_CID | card_info.inc line 174 |
| DAT_08056c50 | 0x08056c50 | 0x15d3 | SECOND_GOBLIN_CID | card_info.inc line 861 |
| DAT_08056c74 | 0x08056c74 | 0x1679 | JUDGEMENT_OF_PHARAOH_CID | card_info.inc line 400 |
| DAT_08056c90 | 0x08056c90 | 0x1841 | NECKLACE_OF_COMMAND_CID | card_info.inc line 534 |
| DAT_08056c9c | 0x08056c9c | 0x1916 | PROTECTIVE_SOUL_AILIN_CID | card_info.inc line 1042 |
| DAT_08056d58 | 0x08056d58 | 0x13f2 | EQUIP_LOCKDOWN_CID | card_info.inc line 128 |
| DAT_08056d84 | 0x08056d84 | 0x15d3 | SECOND_GOBLIN_CID | card_info.inc line 861 (2nd ref) |
| DAT_08056db8 | 0x08056db8 | 0x1332 | BANISHER_OF_THE_LIGHT_CID | card_info.inc line 452 |
| DAT_08056e28 | 0x08056e28 | 0x167a | FRIENDSHIP_CID | NEW -- see below |
| DAT_08056e2c | 0x08056e2c | 0x167b | UNITY_CID | NEW -- see below |
| DAT_08056ecc | 0x08056ecc | 0x178b | PROTECTOR_OF_THE_SANCTUARY_CID | card_info.inc line 621 |
| DAT_08056f00 | 0x08056f00 | 0x1599 | CARD_SHUFFLE_CID | card_info.inc line 1017 |
| DAT_08056f04 | 0x08056f04 | 0x1298 | CYBER_RAIDER_CID | NEW (same as above, 2nd slot) |
| DAT_08056f18 | 0x08056f18 | 0x1679 | JUDGEMENT_OF_PHARAOH_CID | card_info.inc line 400 (2nd ref) |
| DAT_08057008 | 0x08057008 | 0x15d3 | SECOND_GOBLIN_CID | card_info.inc line 861 (3rd ref) |
| DAT_08057014 | 0x08057014 | 0x15cf | KIRYU_CID | card_info.inc line 174 (2nd ref) |
| DAT_0805702c | 0x0805702c | 0x1679 | JUDGEMENT_OF_PHARAOH_CID | card_info.inc line 400 (3rd ref) |
| DAT_08057038 | 0x08057038 | 0x1916 | PROTECTIVE_SOUL_AILIN_CID | card_info.inc line 1042 (2nd ref) |
| DAT_08057100 | 0x08057100 | 0x15d3 | SECOND_GOBLIN_CID | card_info.inc line 861 (4th ref) |
| DWORD_08057158 | 0x08057158 | 0x12a1 | PARASITE_PARACIDE_CID | card_info.inc line 390 |
| DAT_08057234 | 0x08057234 | 0x14de | THE_DRAGONS_BEAD_CID | card_info.inc line 800 |
| DAT_08057238 | 0x08057238 | 0x12f3 | ULTIMATE_OFFERING_CID | card_info.inc line 261 |
| DAT_08057244 | 0x08057244 | 0x1624 | PITCH_BLACK_POWER_STONE_CID | NEW -- see below |

Note on 0x0fff (DAT_08056a74): value is used in BST CID comparison (`cmp r1,r0` where r1=card_id).
Slot_id 0x0FFF = Catapult Turtle per card-stats.s (line 1275). However SCENE_SLOT_MASK_LO already has
this value (duel_field.inc line 56). Per C5 strict dedup (CID/mask/thresholds: same value = reuse),
use SCENE_SLOT_MASK_LO. EOL note: "in BST context = card_id 0x0fff (Catapult Turtle slot)".
conf: med -- the BST dispatch is comparing card IDs and value semantics differ from mask usage.
Alternative: if reviewer finds semantic mismatch unjustifiable, new CATAPULT_TURTLE_CID_0FFF
can be added; but C5 rule as stated requires reuse.

### REF_SLOTS (gP1LifePoints pointers + fn-ptr table entries)

**gP1LifePoints REF slots -- 20 total (16 PTR_ + 4 DWORD_), all value = 0x0201c4e0:**
All map to `gP1LifePoints` (ewram.inc line 79).

PTR_ prefix entries (16):

| slot | addr | slot_label |
|---|---|---|
| PTR_gP1LifePoints_08056a60 | 0x08056a60 | tick_equip_score_sprite_display_seq_gp1lp |
| PTR_gP1LifePoints_08056d18 | 0x08056d18 | dispatch_equip_activation_score_b_gp1lp |
| PTR_gP1LifePoints_08056d50 | 0x08056d50 | dispatch_equip_activation_score_c_gp1lp |
| PTR_gP1LifePoints_08056e58 | 0x08056e58 | dispatch_equip_activation_score_d_gp1lp |
| PTR_gP1LifePoints_08056ec0 | 0x08056ec0 | dispatch_equip_activation_score_e_gp1lp |
| PTR_gP1LifePoints_08056f38 | 0x08056f38 | dispatch_equip_activation_score_f_gp1lp |
| PTR_gP1LifePoints_08056f54 | 0x08056f54 | dispatch_equip_activation_score_g_gp1lp |
| PTR_gP1LifePoints_08056f70 | 0x08056f70 | dispatch_equip_activation_score_h_gp1lp |
| PTR_gP1LifePoints_08056f80 | 0x08056f80 | dispatch_equip_activation_score_i_gp1lp |
| PTR_gP1LifePoints_08056fe4 | 0x08056fe4 | dispatch_equip_activation_score_j_gp1lp |
| PTR_gP1LifePoints_080571bc | 0x080571bc | tick_equip_activation_state_by_phase_gp1lp_a |
| PTR_gP1LifePoints_080571e4 | 0x080571e4 | tick_equip_activation_state_by_phase_gp1lp_b |
| PTR_gP1LifePoints_08057204 | 0x08057204 | tick_equip_activation_state_by_phase_gp1lp_c |
| PTR_gP1LifePoints_08057230 | 0x08057230 | tick_equip_activation_state_by_phase_gp1lp_d |
| PTR_gP1LifePoints_0805733c | 0x0805733c | traverse_equip_zone_nodes_for_lp_score_gp1lp |
| PTR_gP1LifePoints_08057414 | 0x08057414 | tick_equip_zone14_test_display_seq_gp1lp |

DWORD_ prefix entries (4; Ghidra auto-label still DWORD_, but .word already gP1LifePoints in asm):

| slot | addr | enclosing_func | slot_label |
|---|---|---|---|
| DWORD_0805673C | 0x0805673c | trigger_equip_lp_sprite_by_activation_state | trigger_equip_lp_sprite_by_activation_state_gp1lp_c |
| DWORD_0805678C | 0x0805678c | trigger_equip_lp_sprite_by_activation_state | trigger_equip_lp_sprite_by_activation_state_gp1lp_d |
| DWORD_0805680C | 0x0805680c | dispatch_equip_card_name_display_by_step | dispatch_equip_card_name_display_by_step_gp1lp_b |
| DWORD_08056858 | 0x08056858 | dispatch_equip_card_name_display_by_step | dispatch_equip_card_name_display_by_step_gp1lp_c |

ROM verify: all 4 = 0x0201c4e0 (gP1LifePoints). Asm: .word gP1LifePoints already present.
Action: createLabel(slot, slot_label, USER) + addMemoryReference to clear DWORD_ auto-name.
conf: high (ROM value + asm symbol already correct; only Ghidra label needs update).

**fn-ptr REF slots -- 3 slots containing THUMB function pointers:**

| slot | addr | raw_value | target | slot_label |
|---|---|---|---|---|
| DAT_0805697c | 0x0805697c | 0x080905e9 | invoke_effect_node_handler_3arg+1 | tick_equip_score_sprite_display_seq_mode_fn |
| DAT_080569ec | 0x080569ec | 0x08050ead | check_equip_slot_eligible_by_card_id_tree+1 | tick_equip_score_sprite_display_seq_fallback_fn |
| DAT_080573cc | 0x080573cc | 0x080905e9 | invoke_effect_node_handler_3arg+1 | tick_equip_zone14_test_display_seq_mode_fn |

Verification:
- 0x080905e9: ROM @ 0x080905e8 = `70b5 041c` = push {r4,r5,r6,lr}; function = invoke_effect_node_handler_3arg
  (asm/11_effect_slot_puzzletext.s line 11787). THUMB fn-ptr = addr|1 = 0x080905e9. Verified.
- 0x08050ead: ROM @ 0x08050eac = `70b5 89b0` = push {r4,r5,r6,lr}; function = check_equip_slot_eligible_by_card_id_tree
  (asm/05_equip_eligibility_a.s line 17731). THUMB fn-ptr = 0x08050eac|1 = 0x08050ead. Verified.
- GAS: `.word invoke_effect_node_handler_3arg+1` / `.word check_equip_slot_eligible_by_card_id_tree+1`

### RENAME_SLOTS (inline slots without semantic equate -- for DWORD_08056638, DAT_08056d20, DAT_08056bf0)

These three have values not matching any existing constant and warrant new EQ equates (see NEW section):

- DWORD_08056638 @ 0x08056638 = 0x1119  -> EQ EQUIP_SPRITE_CARD_DATA
  slot_label: enqueue_equip_card_sprite_mode3_card_data
  EOL: "enqueue_sprite_attr_with_mode arg r2=card_data fixed 0x1119; mode=3"
  conf: high (single use in enqueue_equip_card_sprite_mode3, passed as r2 to enqueue_sprite_attr_with_mode)

- DAT_08056bf0 @ 0x08056bf0 = 0x0103  -> EQ EQUIP_ACT_SCORE_MODE_103
  slot_label: dispatch_equip_activation_score_by_card_id_mode_a
  EOL: "set_equip_activation_state_by_mode mode code 0x103; loaded into r8 via mov r8,r0 (.hword 0x4680)"
  conf: med (mode semantics not further decoded from callee body in this scope)

- DAT_08056d20 @ 0x08056d20 = 0x0117  -> EQ EQUIP_ACT_SCORE_MODE_117
  slot_label: dispatch_equip_activation_score_by_card_id_mode_b
  EOL: "set_equip_activation_state_by_mode mode code 0x117; loaded into r8 via mov r8,r1 (.hword 0x4688)"
  conf: med

### FUNC_RENAME

None -- all 23 functions have correct semantic names consistent with their bodies.
`tick_equip_activation_lp_cost_sprite_by_type` is correctly named (routes by type_flag mask to
`tick_equip_activation_with_lp_cost_sprite`). No body/name contradiction detected.

### PLATE (R5)

Exhaustive stale FUN_ scan: grep `FUN_[0-9a-f]{8}` lines 7237..9445 (inclusive of all plate lines):
- line 7237 (tick_equip_activation_with_lp_cost_sprite): `FUN_08057430`
- line 9253 (enqueue_equip_slot_sprite_mode4): `FUN_0805663c`, `FUN_080563cc`
Total stale FUN_ occurrences: 3, in 2 plates. Both plates handled below.

Additional CJK plates (grep `[^\x00-\x7F]` lines 7237..9445): lines 7237/7297/7378/9157/9411 (5 plates).
All 5 require PLATE_SET (full ASCII rewrite). Post-apply grep `[^\x00-\x7F]` on segment range must = 0.

**P0 -- tick_equip_activation_with_lp_cost_sprite (0x080565e8)**
Plate at asm line 7237: CJK mojibake + stale `FUN_08057430`.
Action: PLATE_SET (full ASCII rewrite; fixes CJK and FUN_ in one operation).
ASCII plate text:
  "Wrapper: calls tick_equip_activation_state_machine; if returns 1 (slot selected), extracts
  player_id (bit0) from card_entry[+2], calls get_card_lp_cost_by_id to get LP cost for active
  card, then calls enqueue_sprite_attr_clamped(player_id, lp_cost) to enqueue LP-cost sprite attr.
  Always passes through tick return value.
  Called by tick_equip_activation_lp_cost_sprite_by_type when bits[11:6]==type_code matches."
conf: high (function body verified; FUN_08057430 = tick_equip_activation_lp_cost_sprite_by_type
confirmed at asm/06 line 9412).

**P1 -- tick_equip_activation_with_slot_sprite_mode4 (0x0805663c)**
Plate at asm line 7297: CJK mojibake.
Action: PLATE_SET (full ASCII rewrite).
ASCII plate text:
  "Wrapper: calls tick_equip_activation_state_machine; if returns 1 (slot selected), calls
  enqueue_equip_slot_sprite_mode4(card_entry_ptr, secondary_ptr) to enqueue mode=4 equip zone
  slot sprite. Passes through tick return value.
  indeg=0, Sub-type A (no direct callers in callgraph; not in fn-ptr table)."
conf: high (function body at asm/06 lines 7299-7312 verified).

**P2 -- tick_equip_activation_with_type11_sprite (0x080566cc)**
Plate at asm line 7378: CJK mojibake.
Action: PLATE_SET (full ASCII rewrite).
ASCII plate text:
  "Wrapper: calls tick_equip_activation_state_machine; saves return to r5. If r5 < 0 (negative
  signal), extracts player_id (bit0) from card_entry[+2] and card_id (u16 at [+0]), then calls
  enqueue_sprite_attr_type11(player_id, card_id, 1, 0) to enqueue type11 sprite attr.
  Passes through r5 return value.
  indeg=0, Sub-type A."
conf: high (function body at asm/06 lines 7379-7395 verified).

**P3 -- tick_equip_activation_if_neo_daedalus_eligible (0x08057294)**
Plate at asm line 9157: CJK mojibake.
Action: PLATE_SET (full ASCII rewrite).
ASCII plate text:
  "Conditional wrapper: calls check_neo_daedalus_placement_eligible(card_entry_ptr) first.
  If returns 0 (not eligible), immediately returns -1 (rsbs r0,r0,#0).
  If eligible, calls tick_equip_activation_state_machine and passes through its return value.
  indeg=0, Sub-type A."
conf: high (function body at asm/06 lines 9159-9174 verified).

**P4 -- tick_equip_activation_lp_cost_sprite_by_type (0x08057430)**
Plate at asm line 9411: CJK mojibake.
Action: PLATE_SET (full ASCII rewrite).
ASCII plate text:
  "Type-gate stub: reads card_entry[+2] bits[11:2] (mask 0xfc0) to extract slot_type_code.
  If slot_type_code != 0x580 (0xb0<<3), returns 1 immediately (skip).
  If matches, forwards r0/r1 to tick_equip_activation_with_lp_cost_sprite and passes through
  its return value. Used as fn-ptr table entry for type-conditional LP-cost sprite dispatch."
conf: high (function body at asm/06 lines 9413-9429 verified).

Note: stale FUN_ in original P1 plate (line 9253, enqueue_equip_slot_sprite_mode4) is now
renumbered -- that plate is ASCII (no CJK) and only needs PLATE_SUB:

**P5 -- enqueue_equip_slot_sprite_mode4 (0x08057344)**
Stale FUN_ refs in plate at asm line 9253:
  - `FUN_0805663c` -> `tick_equip_activation_with_slot_sprite_mode4`
  - `FUN_080563cc` -> `tick_equip_activation_state_machine`
Action: PLATE_SUB (substring replace FUN_ with current names; plate is ASCII, no CJK).
conf: high (grep line 9253 confirmed both patterns).

## Carve Plan (R7)

None -- no ROM_INCBIN blocks in Seg-5.

## Disasm Plan (R4)

None -- no ROM_INCBIN blocks misidentified as code in Seg-5.

## New Constants / Globals (must-create; grep confirmed absent from all constants/*.inc)

**card_info.inc additions (7 new CID equates):**

1. `POISON_OF_THE_OLD_MAN_CID = 0x000015e7`
   Evidence: data/card-stats.s line 16121: `card_1239: @ Poison of the Old Man slot=0x15E7 pw=08842266`
   Python ROM verify: struct.unpack_from('<H', rom, 0x08056c2c-0x08000000) = 0x15e7. Confirmed.
   Consumer: dispatch_equip_activation_score_by_card_id (multiple BST branches)
   grep card_info.inc `0x000015e7` = 0 hits. NEW.
   conf: high

2. `CYBER_RAIDER_CID = 0x00001298`
   Evidence: data/card-stats.s line 7997: `card_0614: @ Cyber Raider slot=0x1298 pw=39978267`
   Python ROM verify: struct.unpack_from('<I', rom, 0x08056c30-0x08000000) = 0x1298. Confirmed.
   Consumer: dispatch_equip_activation_score_by_card_id + dispatch_equip_activation_score_by_card_id state=1
   grep constants/ `0x00001298` = 0 hits. NEW.
   conf: high

3. `SPIRITUAL_FIRE_ART_CID = 0x00001929`
   Evidence: data/card-stats.s line 25052: `card_1926: @ Spiritual Fire Art - Kurenai slot=0x1929 pw=42945701`
   Python ROM verify: struct.unpack_from('<I', rom, 0x08056abc-0x08000000) = 0x1929. Confirmed.
   Note: distinct from SPIRITUAL_WIND_ART_MIYABI_CID=0x192a (card_info.inc line 934) and
   SPIRITUAL_EARTH_ART_CID=0x1927 (card_info.inc line 968). Three different Spiritual Art cards.
   Consumer: dispatch_equip_activation_score_by_card_id BST branch
   grep constants/ `0x00001929` = 0 hits. NEW.
   conf: high

4. `FRIENDSHIP_CID = 0x0000167a`
   Evidence: data/card-stats.s line 17577: `card_1351: @ Friendship slot=0x167A pw=81332143`
   Python ROM verify: struct.unpack_from('<I', rom, 0x08056e28-0x08000000) = 0x167a. Confirmed.
   Consumer: dispatch_equip_activation_score_by_card_id (0x167a path: count_extra_deck_cards_by_id)
   Note: adjacent to UNITY_CID=0x167b; these two are used together in a pair-check.
   grep constants/ `0x0000167a` = 0 hits. NEW.
   conf: high

5. `UNITY_CID = 0x0000167b`
   Evidence: data/card-stats.s line 17590: `card_1352: @ Unity slot=0x167B pw=14731897`
   Python ROM verify: struct.unpack_from('<I', rom, 0x08056e2c-0x08000000) = 0x167b. Confirmed.
   Consumer: dispatch_equip_activation_score_by_card_id (0x167b path: count_extra_deck_cards_by_id)
   grep constants/ `0x0000167b` = 0 hits. NEW.
   conf: high

6. `ATTACK_REFLECTOR_UNIT_CID = 0x000019b5`
   Evidence: data/card-stats.s line 26378: `card_2028: @ Attack Reflector Unit slot=0x19B5 pw=91989718`
   Python ROM verify: struct.unpack_from('<I', rom, 0x080569a8-0x08000000) = 0x19b5. Confirmed.
   Consumer: tick_equip_score_sprite_display_seq BST branch (DAT_080569a8)
   grep constants/ `0x000019b5` = 0 hits. NEW.
   conf: high

7. `PITCH_BLACK_POWER_STONE_CID = 0x00001624`
   Evidence: data/card-stats.s line 16746: `card_1287: @ Pitch-Black Power Stone slot=0x1624 pw=34029630`
   Python ROM verify: struct.unpack_from('<I', rom, 0x08057244-0x08000000) = 0x1624. Confirmed.
   Consumer: tick_equip_activation_state_by_phase phase=1 BST branch -> enqueue_equip_zone_sprite_at_slot
   grep constants/ `0x00001624` = 0 hits. NEW.
   conf: high

**duel_field.inc additions (3 new scalar equates):**

8. `EQUIP_SPRITE_CARD_DATA = 0x00001119`
   Evidence: DWORD_08056638 @ 0x08056638 = 0x1119; passed as r2 to enqueue_sprite_attr_with_mode(mode=3)
   in enqueue_equip_card_sprite_mode3. Only occurrence of 0x1119 in this context.
   grep constants/ `0x00001119` = 0 hits. NEW.
   conf: high (single dedicated sprite card-data constant for mode=3 equip sprite display)

9. `EQUIP_ACT_SCORE_MODE_103 = 0x00000103`
   Evidence: DAT_08056bf0 @ 0x08056bf0 = 0x103; in dispatch_equip_activation_score_by_card_id,
   loaded into r8 via `.hword 0x4680` (mov r8,r0) before call to set_equip_activation_state_by_mode.
   grep constants/ `0x00000103` = 0 hits. NEW.
   conf: med (mode value semantics not decoded from callee; named after context)

10. `EQUIP_ACT_SCORE_MODE_117 = 0x00000117`
    Evidence: DAT_08056d20 @ 0x08056d20 = 0x117; in dispatch_equip_activation_score_by_card_id
    (0x15cf / Second Goblin path), loaded into r8 via `.hword 0x4688` (mov r8,r1) before
    set_equip_activation_state_by_mode call.
    grep constants/ `0x00000117` = 0 hits. NEW.
    conf: med

## Para.5.1 Registration (Rule 3) -- 0-reference blocks

None. No ROM_INCBIN or .byte blocks in Seg-5.

## Consumer Evidence (R6) -- key slot semantics

1. **gDuelCardCtxBase+8+player_id*4** (DWORD_08056738 in trigger_equip_lp_sprite_by_activation_state):
   asm/06 line 7429-7436: `ldr r1,[DWORD_08056738]; lsrs r0,r5,#0x1f; lsls r0,r0,#0x2; adds r1,#8; adds r0,r0,r1; ldr r4,[r0,#0]`
   -- reads activation_state from gDuelCardCtxBase[player_id*4+8]. Consumer evidence: plate comment
   on trigger_equip_lp_sprite_by_activation_state (line 7404: "ACTIVATION_STATE_BASE = 0x0201e2a0").
   conf: high (ewram.inc line 220 confirms gDuelCardCtxBase=ACTIVATION_STATE_BASE).

2. **EQUIP_ACTIVATION_STEP_OFF** (multiple 0x4ac slots):
   asm/06 lines 7469-7482: `ldr r0,[DWORD_08056758]; ldr r1,[DWORD_0805675c]; adds r4,r0,r1; ldr r0,[r4,#0]`
   -- reads [gDuelPhaseFlags+0x4ac] = step counter. duel_field.inc line 310 confirms.
   conf: high.

3. **ELIGIB_SPRITE_CTRL_OFF** (DAT_08056a64 = 0x1d68 in tick_equip_score_sprite_display_seq):
   asm/06 line 7950: `ldr r1,DAT_08056a64 @ =0x1d68; adds r0,r3,r1; ldr r1,[r0,#0]` reads
   [gP1LifePoints+0x1d68]. ewram.inc line 417: ELIGIB_SPRITE_CTRL_OFF=0x1d68. Consumer plate at
   line 7404 lists `LP_OFFSET_P1=0x1d68`. conf: high.

4. **fn-ptr DAT_0805697c** (=0x080905e9 = invoke_effect_node_handler_3arg+1):
   asm/06 line 7819: `ldr r4,DAT_0805697c` then line 7900-7931: r4 passed as fn-ptr mode to
   set_equip_activation_state_by_mode. asm/11 line 11787 confirms function at 0x080905e8.
   conf: high.

5. **fn-ptr DAT_080569ec** (=0x08050ead = check_equip_slot_eligible_by_card_id_tree+1):
   asm/06 line 7900: `ldr r4,DAT_080569ec @ 0x08050ead` used as fallback fn-ptr when card_id
   not matched in BST. asm/05 line 17731 confirms function at 0x08050eac.
   conf: high.

6. **SLOT_CARD_EMPTY as zone sentinel** (DAT_080566a4 = 0xffff):
   asm/06 line 7344-7347: `ldr r0,DAT_080566a4; cmp r1,r0; beq LAB_080566ae` -- high 16 bits
   of zone_descriptor compared against 0xffff to detect INVALID_ZONE.
   card_info.inc line 386: SLOT_CARD_EMPTY=0xffff (same value; distinct semantic usage). conf: med.

## Requests for Clarification

None. All slot semantics resolved with evidence at high or med confidence.
Med-confidence items: EQUIP_ACT_SCORE_MODE_103/117 (mode params for set_equip_activation_state_by_mode;
callee semantics not decoded within this scope), SCENE_SLOT_MASK_LO reuse for CID comparison context.

---

## Executor Report: F06-Seg-5
- Slots: total=117 (19 DWORD_ + 82 DAT_ + 16 PTR_gP1LifePoints)
  EQ=82 REF=23 (16 PTR_gP1LP + 3 fn-ptr + 4 DWORD_gP1LP) RENAME=0 FUNC_RENAME=0
  PLATE=5 (P0-P4: PLATE_SET x5 ASCII rewrite) + P5 (PLATE_SUB x1 stale FUN_)
- carve=0 disasm=0 para.5.1=0
- New constants/globals: card_info.inc +7 CID (POISON_OF_THE_OLD_MAN/CYBER_RAIDER/SPIRITUAL_FIRE_ART/FRIENDSHIP/UNITY/ATTACK_REFLECTOR_UNIT/PITCH_BLACK_POWER_STONE); duel_field.inc +3 scalar (EQUIP_SPRITE_CARD_DATA/EQUIP_ACT_SCORE_MODE_103/EQUIP_ACT_SCORE_MODE_117)
- Requests for clarification: none
- Proposal: doc/dev/refine/F06-Seg-5.proposal.md
