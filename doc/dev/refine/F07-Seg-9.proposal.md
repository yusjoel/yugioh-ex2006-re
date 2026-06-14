# Refine Proposal: F07-Seg-9  [0x08062d28..0x08063830)

## 段测绘

- 函数入口: 35 named fn x35 (以下列出)
  - 0x08062d28 store_slot_effect_value_from_card
  - 0x08062d4c check_slot_equippable_by_effect_dispatch
  - 0x08062d90 check_equip_slot_eligible_banisher_absent_with_multi_monster_field_zone
  - 0x08062dfc check_equip_slot_eligible_by_zone_type_dispatch
  - 0x08062e1c check_equip_slot_eligible_neo_daedalus_chain_absent_effect_loop
  - 0x08062e8c check_equip_slot_eligible_neo_daedalus_chain_absent_setcode
  - **ROM_INCBIN 0x62ebe/0x3e** (Block A)
  - 0x08062efc check_extra_deck_card_below_limit
  - **ROM_INCBIN 0x62f38/0x28** (Block B)
  - 0x08062f60 check_equip_zone_multi_target_eligible
  - 0x08063020 check_phase2_opp_equip_chain_clear
  - 0x0806305c check_equip_slot_eligible_with_monster_zone_dispatch
  - 0x080630f8 check_zone_card_count_with_activation_match
  - 0x08063194 check_equip_slot_eligible_neo_daedalus_zone_descriptor_0f
  - 0x080631c0 check_zone_card_count_with_monster_slot_match
  - 0x08063254 check_equip_slot_eligible_spell_zone_by_effect_card_id
  - 0x0806327c check_equip_slot_eligible_monster_slot_field6_guard
  - 0x080632a4 check_equip_slot_eligible_chain_absent_tier_pass
  - 0x080632cc dispatch_hand_slot_setcode_in_phase2
  - 0x080632fc check_equip_slot_eligible_chain_absent_with_node_activations
  - 0x08063320 check_equip_slot_eligible_with_field_dispatch_and_zone
  - 0x080633ac check_slot_linked_card_type_spell
  - 0x080633e8 check_field_zone_field5_card_present
  - 0x08063404 check_slot_linked_card_field8_restricted
  - 0x08063440 check_equip_slot_eligible_umi_pair_with_field_zone_active
  - 0x0806348c check_equip_slot_eligible_with_effect_zone_counts
  - 0x0806357c check_equip_slot_eligible_lp_slot_neo_daedalus_guard
  - 0x080635c0 check_equip_eligible_in_phase3_for_active_player
  - 0x08063600 check_equip_slot_eligible_by_tier_class_banisher_guard
  - 0x0806363c check_equip_slot_eligible_with_dual_activation_dispatch
  - 0x080636cc check_equip_slot_eligible_vandalgyon_pair_with_neo_daedalus
  - **ROM_INCBIN 0x636f8/0x38** (Block C)
  - 0x08063730 check_equip_slot_eligible_neo_daedalus_tadpole_extra_deck
  - 0x08063794 check_equip_slot_eligible_polymerization_deck_pair_effect
  - 0x080637c0 check_spell_zone_placeable_with_hand_match
  - 0x080637f4 check_field5_paired_slot_trio_complete
  - 0x08063814 check_lp_zone_offset_substantial
  - 0x08063830 check_opponent_monster_slot_present (Seg-10 boundary)

- 残留自动名槽: 43 个 (7 DAT_ + 33 DWORD_ + 3 PTR_) — 精确 python 核对

  | 槽名 | 地址 | 值 |
  |------|------|-----|
  | DAT_08062de8 | 0x08062de8 | 0x00001332 |
  | PTR_gP1LifePoints_08062dec | 0x08062dec | 0x0201c4e0 |
  | DAT_08062df0 | 0x08062df0 | 0x00000868 |
  | DWORD_08062e84 | 0x08062e84 | 0x0201c4e0 |
  | DWORD_08062e88 | 0x08062e88 | 0x00000868 |
  | DWORD_08062f30 | 0x08062f30 | 0x0201c4e0 |
  | DWORD_08062f34 | 0x08062f34 | 0x00000868 |
  | DWORD_08062fd8 | 0x08062fd8 | 0x00000868 |
  | DWORD_08062fdc | 0x08062fdc | 0x0201c510 |
  | DWORD_08063048 | 0x08063048 | 0x0201c4e0 |
  | DWORD_0806304c | 0x0806304c | 0x00001cf4 |
  | DWORD_08063050 | 0x08063050 | 0x00001318 |
  | DWORD_080630f0 | 0x080630f0 | 0x0201c4e0 |
  | DWORD_080630f4 | 0x080630f4 | 0x00000868 |
  | DWORD_08063180 | 0x08063180 | 0x00000868 |
  | DWORD_08063184 | 0x08063184 | 0x0201c510 |
  | DWORD_08063240 | 0x08063240 | 0x00000868 |
  | DWORD_08063244 | 0x08063244 | 0x0201c510 |
  | PTR_gP1LifePoints_080632ec | 0x080632ec | 0x0201c4e0 |
  | DAT_080632f0 | 0x080632f0 | 0x00001cf4 |
  | DWORD_0806339c | 0x0806339c | 0x0201c4e0 |
  | DWORD_080633a0 | 0x080633a0 | 0x00000868 |
  | DWORD_080633e4 | 0x080633e4 | 0x0201c4e0 |
  | DWORD_0806343c | 0x0806343c | 0x0201c4e0 |
  | DWORD_0806347c | 0x0806347c | 0x0201c4e0 |
  | DWORD_08063480 | 0x08063480 | 0x00000868 |
  | DWORD_080634f4 | 0x080634f4 | 0x0201c4e0 |
  | DWORD_080634f8 | 0x080634f8 | 0x00000868 |
  | DWORD_080634fc | 0x080634fc | 0x00001cf4 |
  | DWORD_08063500 | 0x08063500 | 0x0000178b |
  | DWORD_080635b0 | 0x080635b0 | 0x0201c4e0 |
  | DWORD_080635b4 | 0x080635b4 | 0x00000868 |
  | DWORD_080635ec | 0x080635ec | 0x0201c4e0 |
  | DWORD_080635f0 | 0x080635f0 | 0x00001ce8 |
  | DWORD_080635f4 | 0x080635f4 | 0x00001cf4 |
  | DWORD_080636c4 | 0x080636c4 | 0x0201c4e0 |
  | DWORD_080636c8 | 0x080636c8 | 0x00000868 |
  | DAT_080636ec | 0x080636ec | 0x0000190a |
  | PTR_gP1LifePoints_08063780 | 0x08063780 | 0x0201c4e0 |
  | DAT_08063784 | 0x08063784 | 0x00000868 |
  | DAT_08063788 | 0x08063788 | 0x00001919 |
  | DAT_080637b4 | 0x080637b4 | 0x000012e5 |
  | DWORD_08063810 | 0x08063810 | 0x00001918 |

- ROM_INCBIN / .byte 块: 3 块
  - 0x08062ebe size 0x3e (Block A: between check_equip_slot_eligible_neo_daedalus_chain_absent_setcode and check_extra_deck_card_below_limit)
  - 0x08062f38 size 0x28 (Block B: between check_extra_deck_card_below_limit and check_equip_zone_multi_target_eligible)
  - 0x080636f8 size 0x38 (Block C: between check_equip_slot_eligible_vandalgyon_pair_with_neo_daedalus and check_equip_slot_eligible_neo_daedalus_tadpole_extra_deck)

---

## 数据块分类 (Rule 2/3) — 每块给 ref-scan 证据

| 块 | ref-scan (raw / THUMB+1) | 判定 | 理由 |
|---|---|---|---|
| 0x08062ebe sz=0x3e | raw=0 thumb+1=4 total: 3 at 0x08062ec0+1 (fn_start) + 1 at 0x08062ee6+1 (mid-code) | disasm R4 | 3 real hits at 0x09e4xxxx handler table (file offsets 0x1e42358/0x1e426e8/0x1e42ce8): [CID_word][fn_act+1][0x00][fn_elig+1=0x08062ec1][0x00][0x00]; CIDs 0x17fd/0x1886/0x195f confirmed. 4th hit for 0x08062ee6+1=0x08062ee7 at file_off=0x83aef1 (GBA 0x0883aef1): outside 0x09e4xxxx; context[-4]=0xdffc0028 is not a valid CID (>>0x2000) = compression coincidence, not a real fn pointer |
| 0x08062f38 sz=0x28 | raw=0 thumb+1=1 (at +0x00=0x08062f38+1) | disasm R4 | 1 hit at 0x1e42760: entry [CID=0x188b][fn_act=0x080655ed+1][0x00][fn_elig=0x08062f39][0x00][fn_next=0x08061db1]; fn_elig value 0x08062f39 == 0x08062f38+1 confirmed |
| 0x080636f8 sz=0x38 | raw=0 thumb+1=1 (at +0x00=0x080636f8+1) | disasm R4 | 1 hit at 0x1e45268: entry [CID=0x1911][fn_act=0x0807c7f1][0x00][fn_elig=0x080636f9=0x080636f8+1][0x00][0x00] confirmed |

---

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate; 全部 reuse 现有常量, 1 个 new)

全部 43 个现有自动名槽 + 7 个 disasm 新增 literal pool 槽, 共 50 EQ 槽:

| 槽 | value | const_name | slot_label | reuse/new |
|---|---|---|---|---|
| DAT_08062de8 | 0x00001332 | BANISHER_OF_THE_LIGHT_CID | banisher_cid_08062de8 | REUSE card_info.inc |
| DWORD_08062e84 | 0x0201c4e0 | gP1LifePoints | gp1lp_ref_08062e84 | REUSE ewram.inc |
| DWORD_08062e88 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_stride_08062e88 | REUSE ewram.inc |
| DWORD_08062f30 | 0x0201c4e0 | gP1LifePoints | gp1lp_ref_08062f30 | REUSE ewram.inc |
| DWORD_08062f34 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_stride_08062f34 | REUSE ewram.inc |
| DWORD_08062fd8 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_stride_08062fd8 | REUSE ewram.inc |
| DWORD_08062fdc | 0x0201c510 | gDuelFieldSlots | duel_field_slots_08062fdc | REUSE ewram.inc |
| DWORD_08063048 | 0x0201c4e0 | gP1LifePoints | gp1lp_ref_08063048 | REUSE ewram.inc |
| DWORD_0806304c | 0x00001cf4 | FIELD_STATE_OFF | field_state_off_0806304c | REUSE duel_field.inc |
| DWORD_08063050 | 0x00001318 | RING_OF_MAGNETISM_CID | ring_mag_cid_08063050 | REUSE card_info.inc (scan param same value as CID; consistent with asm/07 Seg-5 precedent at 0x0805fd20) |
| DWORD_080630f0 | 0x0201c4e0 | gP1LifePoints | gp1lp_ref_080630f0 | REUSE ewram.inc |
| DWORD_080630f4 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_stride_080630f4 | REUSE ewram.inc |
| DWORD_08063180 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_stride_08063180 | REUSE ewram.inc |
| DWORD_08063184 | 0x0201c510 | gDuelFieldSlots | duel_field_slots_08063184 | REUSE ewram.inc |
| DWORD_08063240 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_stride_08063240 | REUSE ewram.inc |
| DWORD_08063244 | 0x0201c510 | gDuelFieldSlots | duel_field_slots_08063244 | REUSE ewram.inc |
| DAT_080632f0 | 0x00001cf4 | FIELD_STATE_OFF | field_state_off_080632f0 | REUSE duel_field.inc |
| DWORD_0806339c | 0x0201c4e0 | gP1LifePoints | gp1lp_ref_0806339c | REUSE ewram.inc |
| DWORD_080633a0 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_stride_080633a0 | REUSE ewram.inc |
| DWORD_080633e4 | 0x0201c4e0 | gP1LifePoints | gp1lp_ref_080633e4 | REUSE ewram.inc |
| DWORD_0806343c | 0x0201c4e0 | gP1LifePoints | gp1lp_ref_0806343c | REUSE ewram.inc |
| DWORD_0806347c | 0x0201c4e0 | gP1LifePoints | gp1lp_ref_0806347c | REUSE ewram.inc |
| DWORD_08063480 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_stride_08063480 | REUSE ewram.inc |
| DWORD_080634f4 | 0x0201c4e0 | gP1LifePoints | gp1lp_ref_080634f4 | REUSE ewram.inc |
| DWORD_080634f8 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_stride_080634f8 | REUSE ewram.inc |
| DWORD_080634fc | 0x00001cf4 | FIELD_STATE_OFF | field_state_off_080634fc | REUSE duel_field.inc |
| DWORD_08063500 | 0x0000178b | PROTECTOR_OF_SANCTUARY_CID | protector_cid_08063500 | REUSE card_info.inc (plate: "EFFECT_ZONE_SCAN_PARAM=0x178b Protector of the Sanctuary"; same value; consistent with Seg-8 precedent) |
| DWORD_080635b0 | 0x0201c4e0 | gP1LifePoints | gp1lp_ref_080635b0 | REUSE ewram.inc |
| DWORD_080635b4 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_stride_080635b4 | REUSE ewram.inc |
| DWORD_080635ec | 0x0201c4e0 | gP1LifePoints | gp1lp_ref_080635ec | REUSE ewram.inc |
| DWORD_080635f0 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | p1lp_block2_off_080635f0 | REUSE ewram.inc |
| DWORD_080635f4 | 0x00001cf4 | FIELD_STATE_OFF | field_state_off_080635f4 | REUSE duel_field.inc |
| DWORD_080636c4 | 0x0201c4e0 | gP1LifePoints | gp1lp_ref_080636c4 | REUSE ewram.inc |
| DWORD_080636c8 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_stride_080636c8 | REUSE ewram.inc |
| DAT_080636ec | 0x0000190a | DARK_RULER_VANDALGYON_CID | vandalgyon_cid_080636ec | REUSE card_info.inc |
| DAT_08063784 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_stride_08063784 | REUSE ewram.inc |
| DAT_08063788 | 0x00001919 | TADPOLE_CID | tadpole_cid_08063788 | REUSE card_info.inc |
| DAT_080637b4 | 0x000012e5 | POLYMERIZATION_CID | poly_cid_080637b4 | REUSE card_info.inc |
| DWORD_08063810 | 0x00001918 | DES_FROG_CID | des_frog_cid_08063810 | **NEW** card_info.inc (Des Frog pw=84451804; card_1909 slot=0x1918; sibling of TADPOLE_CID=0x1919; confirmed card-stats.s L23454) |
| DAT_08062df0 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_stride_08062df0 | REUSE ewram.inc |
| (Block A disasm) gp1lp_ref_08062edc | 0x0201c4e0 | gP1LifePoints | gp1lp_ref_08062edc | REUSE ewram.inc |
| (Block A disasm) p1lp_block2_off_08062ee0 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | p1lp_block2_off_08062ee0 | REUSE ewram.inc |
| (Block A disasm) field_state_off_08062ef8 | 0x00001cf4 | FIELD_STATE_OFF | field_state_off_08062ef8 | REUSE duel_field.inc |
| (Block B disasm) gp1lp_ref_08062f58 | 0x0201c4e0 | gP1LifePoints | gp1lp_ref_08062f58 | REUSE ewram.inc |
| (Block B disasm) player_stride_08062f5c | 0x00000868 | PLAYER_BLOCK_STRIDE | player_stride_08062f5c | REUSE ewram.inc |
| (Block C disasm) gp1lp_ref_08063724 | 0x0201c4e0 | gP1LifePoints | gp1lp_ref_08063724 | REUSE ewram.inc |
| (Block C disasm) player_stride_08063728 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_stride_08063728 | REUSE ewram.inc |

Note: DAT_08062de8 (BANISHER_OF_THE_LIGHT_CID) and DAT_08062df0 (PLAYER_BLOCK_STRIDE) are used by check_equip_slot_eligible_banisher_absent_with_multi_monster_field_zone.

### REF_SLOTS (USER-label + DATA-ref)

None. The 3 PTR_gP1LifePoints_ slots are RENAME (not data-ref type used as pointer), same as Seg-1..8 convention.

### RENAME_SLOTS (纯改名 + EOL)

| 槽 | slot_label | eol_ascii |
|---|---|---|
| PTR_gP1LifePoints_08062dec | gp1lp_ptr_08062dec | "gP1LifePoints ptr" |
| PTR_gP1LifePoints_080632ec | gp1lp_ptr_080632ec | "gP1LifePoints ptr" |
| PTR_gP1LifePoints_08063780 | gp1lp_ptr_08063780 | "gP1LifePoints ptr" |

Evidence: Consistent with Seg-1 RENAME=9 (PTR_gP1LifePoints_* -> gp1lp_ptr_*) pattern; asm/07 lines 165/339/481/620/857+ all use gp1lp_ptr_ prefix.

### FUNC_RENAME

None identified. All 35 named functions were inspected; function bodies match the semantic names already assigned.

### PLATE (R5; 全 ASCII)

None required.
- No stale FUN_ references found in lines 17403-18936 (grep `FUN_[0-9a-f]{8}` = 0 matches).
- No non-ASCII characters found (grep `[^\x00-\x7F]` = 0 matches).

---

## disasm 计划 (R4)

### Block A: ROM_INCBIN 0x08062ebe / 0x3e

**函数**: `check_opp_active_player_duel_phase_leq3` @ 0x08062ec0

- Entry: 0x08062ebe = .zero 2 (alignment pad); fn THUMB+1 handler pointer = 0x08062ec1 -> fn start = 0x08062ec0.
- Literal pool interleaved at 0x08062eda..0x08062ee3 (between two code segments) and 0x08062ef6..0x08062efb (at end).
- Function semantics (machine-code verified):
  - ldr r3,[pc,#0x18] at 0x08062ec0 (lit=0x08062edc -> gP1LifePoints); ldr r1,[pc,#0x1c] at 0x08062ec2 (lit=0x08062ee0 -> P1LP_BLOCK2_OFF_1CE8=0x1ce8); adds r2,r3,r1 -> r2 = gP1LP + 0x1ce8 (active player base).
  - ldrb r0,[r0,#2] (0x7880 at 0x08062ec6: ldrb with imm5=2) -> r0 = slot[+2] byte.
  - lsls r0,r0,#31 (0x07c0 at 0x08062ec8); lsrs r0,r0,#31 (0x0fc0 at 0x08062eca) -> r0 = player_id = slot[+2] & 1.
  - movs r1,#1; subs r1,r1,r0 (0x1a09 at 0x08062ece: bits[9]=1=sub, Rm=r0, Rn=r1, Rd=r1 confirmed) -> r1 = opp_player_id.
  - ldr r0,[r2,#0] at 0x08062ed0 -> r0 = active_player_id = [gP1LP+0x1ce8]; cmp r0,r1 (0x4288 at 0x08062ed2).
  - beq target verification: 0xd006 at 0x08062ed4; PC=0x08062ed8; target=0x08062ed8+0x0c=0x08062ee4 (confirmed python).
  - If NOT equal (active player is not opp): movs r0,#0 at 0x08062ed6; e00c branch at 0x08062ed8 -> target=0x08062ef4 (bx lr) -> return 0.
  - If equal (opp IS active player): loads FIELD_STATE_OFF (0x1cf4); ldr from [gP1LP+0x1cf4].
  - At 0x08062ee4: movs r1,#0 (clear r1); ldr r2,[pc,#0x10] at 0x08062ee6 (PC=0x08062ee8, lit=0x08062ef8 -> FIELD_STATE_OFF=0x1cf4); adds r0,r3,r2 at 0x08062ee8 -> r0 = gP1LP + 0x1cf4; ldr r0,[r0,#0] -> r0 = duel_phase.
  - cmp phase, 3; bhi 0x08062ef2: 0xd800 at 0x08062eee; offset=0; PC=0x08062ef2; bhi taken if phase>3 -> fall through to adds r0,r1,#0 where r1=0 -> r0=0; bx lr at 0x08062ef4 -> return 0.
  - If not taken (phase<=3): movs r1,#1 at 0x08062ef0; adds r0,r1,#0 at 0x08062ef2 -> r0=1; bx lr -> return 1.
  - Summary: returns 1 iff opp is active player AND duel_phase <= 3.
- **3 handler table entries share this fn_eligible**: CIDs 0x17fd (Absolute End), 0x1886 (Threatening Roar), 0x195f (Hero Barrier).
  - 0x17fd = ABSOLUTE_END_CID: REUSE (card_info.inc confirmed: `.equ ABSOLUTE_END_CID, 0x000017fd`).
  - 0x1886 = THREATENING_ROAR_CID: NEW (card-stats.s line 23376: `@ Threatening Roar slot=0x1886 pw=36361633`).
  - 0x195f = HERO_BARRIER_CID: NEW (card-stats.s line 54103: `@ Hero Barrier slot=0x195F pw=44676200`).
- Plate (ASCII): "fn_eligible shared by CIDs: ABSOLUTE_END (0x17fd), THREATENING_ROAR (0x1886), HERO_BARRIER (0x195f). Reached via handler table 0x09e4xxxx. Returns 1 if opp is active player AND phase <= 3."
- Literal pool EQ slots: gp1lp_ref_08062edc (gP1LifePoints), p1lp_block2_off_08062ee0 (P1LP_BLOCK2_OFF_1CE8), field_state_off_08062ef8 (FIELD_STATE_OFF).

**Ghidra DisassembleCommand range**: 0x08062ec0 (start); disassembly covers two code segments with interleaved literal pool. createDWord at 0x08062edc (gP1LP), 0x08062ee0 (P1LP_BLOCK2_OFF_1CE8), 0x08062ef8 (FIELD_STATE_OFF); createFunction at 0x08062ec0. bx lr at 0x08062ef4. Block layout: 2B pad(0xebe-0xebf), 0x1a code(0xec0-0xed9), 2B zero(0xeda-0xedb), 8B litpool(0xedc-0xee3), 0x12 code(0xee4-0xef5), 2B zero(0xef6-0xef7), 4B litpool(0xef8-0xefb). Total=0x3e.

### Block B: ROM_INCBIN 0x08062f38 / 0x28

**函数**: `check_opp_alt_hand_count_nonzero_for_cid_188b` @ 0x08062f38

- Entry: fn THUMB+1 pointer = 0x08062f39 -> fn start = 0x08062f38 (no leading pad).
- Function semantics (machine-code verified):
  - ldr r2,[pc,#0x1c] at 0x08062f38 (0x4a07: Rd=2, imm8=7; PC=0x08062f3c; lit=0x08062f3c+0x1c=0x08062f58 -> 0x0201c4e0 = gP1LifePoints confirmed).
  - ldrb r0,[r0,#2] (0x7880 at 0x08062f3a); lsls r0,r0,#31 (0x07c0); lsrs r0,r0,#31 (0x0fc0) -> r0 = player_id = slot[+2] & 1.
  - movs r1,#1 (0x2101 at 0x08062f40); 0x4048 at 0x08062f42: eors r0,r1 (ALU bits[15:10]=010000, bits[9:6]=0001=EOR, Rs=r1, Rd=r0 machine-code confirmed) -> r0 = player_id XOR 1 = 1-player_id = OPP player_id.
  - ldr r1,[pc,#0x14] at 0x08062f44 (0x4905: Rd=1, imm8=5; PC=0x08062f48; lit=0x08062f48+0x14=0x08062f5c -> 0x00000868 = PLAYER_BLOCK_STRIDE confirmed).
  - muls r0,r1 (0x4348 at 0x08062f46) -> r0 = opp_player * 0x868.
  - adds r2,#0x1c (0x321c at 0x08062f48) -> r2 = gP1LP + 0x1c = gP1AltHandCountBase (ewram.inc: `gP1AltHandCountBase = 0x0201c4fc = gP1LP+0x1c`).
  - adds r0,r0,r2 -> r0 = gP1AltHandCountBase + opp_player * PLAYER_BLOCK_STRIDE.
  - ldr r0,[r0,#0] (0x6800 at 0x08062f4c) -> alt_hand_count[opp_player] (opponent banished card count).
  - cmp r0,#0 (0x2800); d000 at 0x08062f50: beq target = 0x08062f50+4+0*2 = 0x08062f54 (bx lr) -> if 0: return 0.
  - movs r0,#1 (0x2001); bx lr (0x4770 at 0x08062f54) -> if nonzero: return 1.
  - Summary: returns 1 if OPPONENT's banished zone card count > 0; returns 0 if opponent has no banished cards.
  - Semantic note: D.D. Dynamite deals damage = opponent banished cards * 300; this eligibility gate ensures opponent has at least 1 banished card (otherwise card is useless).
- CID: 0x188b = D.D. Dynamite (card-stats.s line 23441: `@ D.D. Dynamite slot=0x188B pw=08628798`). NEW: D_D_DYNAMITE_CID.
- Literal pool EQ slots: gp1lp_ref_08062f58 (gP1LifePoints), player_stride_08062f5c (PLAYER_BLOCK_STRIDE). Offset 0x1c encoded as immediate in adds r2,#0x1c.
- Plate (ASCII): "fn_eligible for D.D. Dynamite CID 0x188b. Reached via handler table 0x09e42754. eors player_id to get opp_player (0x4048=EOR not AND). Checks opp alt-hand (banished) count at [gP1LP+opp*0x868+0x1c]. Returns 1 if opp has banished cards, 0 if none."

**Ghidra DisassembleCommand range**: 0x08062f38 (start); bx lr at 0x08062f54. createDWord at 0x08062f58 (gP1LP), 0x08062f5c (PLAYER_BLOCK_STRIDE); createFunction at 0x08062f38. Block layout: 0x1e code(0xf38-0xf55), 2B zero(0xf56-0xf57), 4B litpool(0xf58-0xf5b), 4B litpool(0xf5c-0xf5f). Total=0x28.

### Block C: ROM_INCBIN 0x080636f8 / 0x38

**函数**: `check_zone_non_field_type_or_has_monsters_for_cid_1911` @ 0x080636f8

- Entry: fn THUMB+1 pointer = 0x080636f9 -> fn start = 0x080636f8 (no leading pad).
- Function semantics (machine-code verified):
  - adds r3,r0,#0 -> r3 = slot_ptr (save r0).
  - movs r0,#0xfc; 0x0100 at 0x080636fc: lsls r0,r0,#4 (bits[15:11]=00000, imm5=4, rm=r0, rd=r0) -> r0 = 0xfc0 (ZONE_TYPE_MASK).
  - ldrh r1,[r3,#2] -> r1 = slot[+2] halfword; 0x8859 at 0x080636fe: bits[15:11]=10001=ldrh, imm5=1, offset=imm5*2=2, Rb=r3, Rd=r1 (machine-code confirmed: slot[+2] NOT slot[+4]; consistent with all Seg-9 plate comments using ldrh[+0x2] for zone type, e.g. asm/07 lines 17523/18215/18288/18339).
  - ands r0,r1 -> r0 = slot[+2] & 0xfc0 (zone_type).
  - movs r1,#0xa0; 0x0049 at 0x08063704: lsls r1,r1,#1 (lsl fmt: imm5=0 but stored as 0x0049; re-check: 0x0049=0000 0000 0100 1001 -> 000 00 imm5=1 rm=r1 rd=r1 -> lsls r1,r1,#1) -> r1 = 0x140 (FIELD_ZONE_TYPE, 0xa0<<1).
    - Note: 0x0049 decode: bits[15:11]=00000=LSL; bits[10:6]=00001=imm5=1; bits[5:3]=001=r1; bits[2:0]=001=r1 -> lsls r1,r1,#1. Confirmed by target value: 0xa0<<1=0x140.
  - cmp r0,r1 -> compare zone_type with 0x140.
  - d110 at 0x08063708: bne target = 0x08063708+4+0x10*2 = 0x0806372c (python: 0x0806372c). At 0x0806372c: movs r0,#1; bx lr -> if zone_type != 0x140: return 1.
  - If zone_type == 0x140 (field zone type): continue.
  - ldr r2,[pc,#0x18] at 0x0806370a (0x4a06: Rd=2, imm8=6; PC=0x0806370c; lit=0x0806370c+0x18=0x08063724 -> 0x0201c4e0 = gP1LifePoints confirmed).
  - ldrb r3,[r3,#2] (0x789b at 0x0806370c) -> r3 = slot[+2] byte (player_id byte, reusing r3 as slot ptr).
  - lsls r0,r3,#31 (0x07d8 at 0x0806370e); lsrs r0,r0,#31 (0x0fc0 at 0x08063710) -> r0 = player_id.
  - ldr r1,[pc,#0x14] at 0x08063712 (0x4905: Rd=1, imm8=5; PC=0x08063714; lit=0x08063714+0x14=0x08063728 -> 0x00000868 = PLAYER_BLOCK_STRIDE confirmed).
  - muls r0,r1 -> r0 = player_id * 0x868.
  - adds r2,#0x0c -> r2 = gP1LP + 0x0c.
  - adds r0,r0,r2 -> r0 = gP1LP + player*0x868 + 0x0c (monster count offset).
  - ldr r0,[r0,#0] -> load monster_count.
  - cmp r0,#0; d006 at 0x0806371e: beq target = 0x0806371e+4+6*2 = 0x0806372e (python: 0x0806372e) -> bx lr with r0=0 -> return 0.
  - movs r0,#1; e004 at 0x08063722: b target = 0x08063722+4+4*2 = 0x0806372e -> bx lr with r0=1 -> return 1.
  - Monster count path: 0x0806370c ldrb r3,[r3,#2] (player_id byte from slot[+2]); lsls/lsrs r0,r3,#31 -> player_id; ldr r1,[pc,#0x14] at 0x08063712 -> PLAYER_BLOCK_STRIDE; muls r0,r1; adds r2,#0x0c at 0x08063716 (r2=gP1LP+0x0c); adds r0,r0,r2; ldr r0,[r0,#0] -> monster_count at [gP1LP+player_id*0x868+0x0c].
  - Summary: if slot[+2] & 0xfc0 != 0x140 (FIELD_ZONE_TYPE): return 1; if field zone and monster_count[player] > 0: return 1; else: return 0.
- CID: 0x1911 = CYBER_ARCHFIEND_CID. REUSE (card_info.inc confirmed: `.equ CYBER_ARCHFIEND_CID, 0x00001911`).
- Literal pool EQ slots: gp1lp_ref_08063724 (gP1LifePoints), player_stride_08063728 (PLAYER_BLOCK_STRIDE).
- Plate (ASCII): "fn_eligible for Cyber Archfiend CID 0x1911. Reached via handler table 0x09e4525c. If slot[+2]&0xfc0 != 0x140 (FIELD_ZONE_TYPE 0xa0<<1): return 1. If field zone type: check [gP1LP+player*0x868+0x0c] (monster_count); nonzero->1, zero->0."

**Ghidra DisassembleCommand range**: 0x080636f8 (start); bx lr at 0x0806372e. createDWord at 0x08063724 (gP1LP), 0x08063728 (PLAYER_BLOCK_STRIDE); createFunction at 0x080636f8. Block layout: 0x2c code(0x636f8-0x63723 incl), 8B litpool(0x63724-0x6372b), 4B code(0x6372c movs r0,#1; 0x6372e bx lr). Total=0x38.

---

## carve 计划 (R7)

None. All 3 ROM_INCBIN blocks are THUMB code (R4 disasm), not data tables requiring carve.

---

## 新增 constants / 全局

### card_info.inc 新增 4 CID equates

All verified new (grep card_info.inc for each = 0 matches):

1. `THREATENING_ROAR_CID = 0x00001886` — Threatening Roar (pw=36361633; card-stats.s line 23376 `card_1797: @ Threatening Roar slot=0x1886`). Used as fn_eligible CID for Block A.
2. `HERO_BARRIER_CID = 0x0000195f` — Hero Barrier (pw=44676200; card-stats.s line 54103 `card_4586: @ Hero Barrier slot=0x195F`). Used as fn_eligible CID for Block A.
3. `D_D_DYNAMITE_CID = 0x0000188b` — D.D. Dynamite (pw=08628798; card-stats.s line 23441 `card_1802: @ D.D. Dynamite slot=0x188B`). Used as fn_eligible CID for Block B.
4. `DES_FROG_CID = 0x00001918` — Des Frog (pw=84451804; card-stats.s line 23454 `card_1909: @ Des Frog slot=0x1918`). Used at DWORD_08063810 in check_field5_paired_slot_trio_complete as count_paired_slots_with_field5_default param.

C5 double-check (reverse: confirm none exist):
- `grep THREATENING_ROAR card_info.inc` = 0 hits -> NEW confirmed.
- `grep HERO_BARRIER card_info.inc` = 0 hits -> NEW confirmed.
- `grep D_D_DYNAMITE card_info.inc` = 0 hits -> NEW confirmed.
- `grep DES_FROG card_info.inc` = 0 hits -> NEW confirmed.

---

## §5.1 登记 (Rule 3) — 0 引用块

None. All 3 ROM_INCBIN blocks have confirmed 0x09e4xxxx handler table THUMB+1 references.

---

## 消费者证据 (R6) — 关键槽语义的 file:line + 置信度

| 槽 / 全局 | 消费者 file:line | 置信度 |
|---|---|---|
| gP1LifePoints (12 EQ slots) | ewram.inc: `.equ gP1LifePoints, 0x0201C4E0` + asm/07 17497/18165/18778 ldr usage | high |
| PLAYER_BLOCK_STRIDE (13 EQ slots) | ewram.inc: `.equ PLAYER_BLOCK_STRIDE, 0x868` | high |
| gDuelFieldSlots (3 EQ slots) | ewram.inc: `.equ gDuelFieldSlots, 0x0201c510` | high |
| FIELD_STATE_OFF (4 EQ slots) | duel_field.inc: `.equ FIELD_STATE_OFF, 0x00001cf4` | high |
| P1LP_BLOCK2_OFF_1CE8 (1 EQ slot) | ewram.inc: `.equ P1LP_BLOCK2_OFF_1CE8, 0x1ce8` | high |
| BANISHER_OF_THE_LIGHT_CID | card_info.inc: `.equ BANISHER_OF_THE_LIGHT_CID, 0x00001332` | high |
| RING_OF_MAGNETISM_CID (0x1318) | card_info.inc: `.equ RING_OF_MAGNETISM_CID, 0x00001318`; asm/07 line 9535 plate: "0x1318: count_equip_slots_with_active_chain config constant" | high |
| PROTECTOR_OF_SANCTUARY_CID (0x178b) | card_info.inc: `.equ PROTECTOR_OF_SANCTUARY_CID, 0x0000178b`; asm/07 lines 15027/16815/17053 plates confirm "Protector of the Sanctuary" as count_available_effect_zones param | high |
| DARK_RULER_VANDALGYON_CID | card_info.inc: `.equ DARK_RULER_VANDALGYON_CID, 0x0000190a` | high |
| TADPOLE_CID | card_info.inc: `.equ TADPOLE_CID, 0x00001919`; asm/07 18766 plate "ICID_TADPOLE=0x1919 T.A.D.P.O.L.E." | high |
| POLYMERIZATION_CID | card_info.inc: `.equ POLYMERIZATION_CID, 0x000012e5` | high |
| ABSOLUTE_END_CID (0x17fd, Block A) | card_info.inc: `.equ ABSOLUTE_END_CID, 0x000017fd @ Absolute End; activation/fieldspell zone chain` | high |
| THREATENING_ROAR_CID (0x1886, Block A) | card-stats.s line 23376: `@ Threatening Roar slot=0x1886 pw=36361633`; handler table entry at 0x09e426dc confirmed structure | high |
| HERO_BARRIER_CID (0x195f, Block A) | card-stats.s line 54103: `@ Hero Barrier slot=0x195F pw=44676200`; handler table entry at 0x09e42cdc confirmed structure | high |
| D_D_DYNAMITE_CID (0x188b, Block B) | card-stats.s line 23441: `@ D.D. Dynamite slot=0x188B pw=08628798`; handler table entry at 0x09e42754 confirmed structure | high |
| CYBER_ARCHFIEND_CID (0x1911, Block C) | card_info.inc: `.equ CYBER_ARCHFIEND_CID, 0x00001911`; handler table entry at 0x09e4525c confirmed | high |
| DES_FROG_CID (0x1918) | card-stats.s line 23454: `@ Des Frog slot=0x1918 pw=84451804`; DWORD_08063810 read as count_paired_slots_with_field5_default param (asm/07 line 17888); sibling of TADPOLE_CID=0x1919 | high |
| Block A fn check_opp_active_player_duel_phase_leq3 | handler table 0x09e4234c entry CID=0x17fd + fn_elig=0x08062ec1; machine-code branch trace confirmed | high |
| Block B fn check_opp_alt_hand_count_nonzero_for_cid_188b | handler table 0x09e42754 entry CID=0x188b + fn_elig=0x08062f39; eors r0,r1 (0x4048=EOR not AND) computes opp_player; reads [gP1LP+opp*0x868+0x1c]=opp banished count | high |
| Block C fn check_zone_non_field_type_or_has_monsters_for_cid_1911 | handler table 0x09e4525c entry CID=0x1911 + fn_elig=0x080636f9; zone type 0x140 = FIELD_ZONE_TYPE (asm/07 line 15134 plate "FIELD_ZONE_TYPE=0x140 (0xa0 << 1)")  | high |

---

## 求助

None. All semantics resolved with high confidence from machine-code traces + handler table verification + card-stats.s lookup.

---

## C13 穷举对账

- 段内自动名槽总数 (python 精确): **43** (DAT_=7, DWORD_=33, PTR_=3)
- EQ 表覆盖: 40 existing slots (43 - 3 PTR_ which are RENAME)
- RENAME 表: 3 PTR_ slots
- EQ + RENAME = 43 = 43 total (missing=0, extra=0)
- 越界检查: 最低槽 0x08062de8 >= Seg-9 start 0x08062d28 OK; 最高槽 0x08063810 < Seg-9 end 0x08063830 OK
- disasm 新增 literal pool 槽: 7 (分属 3 blocks, 落地后 Ghidra 导出为新 DWORD_/DAT_ 槽再补符号化)
