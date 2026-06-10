# Refine Proposal: F02Seg10a  [0x0803407c..0x08035280)

Split boundary: `exit_slot_activation_with_state_write` starts at 0x08035280 (fn 11 of 17).
Seg-10b = [0x08035280..0x08035f54) covers fns 11-17 (98 slots), to be handled next.

---

## Segment Survey

### Function Entries (10 functions)

| addr       | name                                   | asm line |
|------------|----------------------------------------|----------|
| 0x0803407c | eval_slot_target_eligibility_full      | 17842    |
| 0x0803412c | check_card_matches_active_effect_slot  | 17938    |
| 0x08034180 | find_paired_zone_entry_for_card        | 17984    |
| 0x08034298 | check_card_targeted_by_spell_zone_effect | 18132  |
| 0x08034358 | check_slot_field_action_eligibility    | 18236    |
| 0x080345e0 | check_field_spell_slot_placeable       | 18568    |
| 0x080346c4 | check_slot_monster_activation_eligible | 18685    |
| 0x0803495c | eval_slot_activation_guard_full        | 19026    |
| 0x080349b0 | check_slot_card_activatable            | 19072    |
| 0x08034a58 | check_slot_full_activation_eligibility | 19162    |

### Residual Auto-name Slots: 148 total

By label type:
- 10 PTR_gP1LifePoints_* (already named base; need slot_label rename only)
- 138 DAT_* slots (values below)

### ROM_INCBIN / .byte blocks: NONE

---

## Data Block Classification (Rule 2/3)

No ROM_INCBIN or .byte blocks in [0x0803407c..0x08035280).
Rule 2/3 ref-scan: N/A (no data blocks).
Section 5.1 = 0 orphan data blocks.

---

## Symbolization Plan

### EQ_SLOTS  (data-equate)

**Group A: Reuse existing constants (no new .equ needed)**

| slot addr      | value      | const_name (existing)      | slot_label                                   |
|----------------|------------|----------------------------|----------------------------------------------|
| DAT_080340bc   | 0x00000868 | PLAYER_BLOCK_STRIDE        | eval_slot_target_eligibility_full_stride     |
| DAT_080340c0   | 0x0201c510 | gDuelFieldSlots            | eval_slot_target_eligibility_full_slots      |
| DAT_08034124   | 0x00000868 | PLAYER_BLOCK_STRIDE        | eval_slot_target_eligibility_full_stride_b   |
| DAT_08034128   | 0x0201c510 | gDuelFieldSlots            | eval_slot_target_eligibility_full_slots_b    |
| DAT_080341b0   | 0x00000868 | PLAYER_BLOCK_STRIDE        | find_paired_zone_entry_for_card_stride       |
| DAT_080341b4   | 0x0201c510 | gDuelFieldSlots            | find_paired_zone_entry_for_card_slots        |
| DAT_0803428c   | 0x00000868 | PLAYER_BLOCK_STRIDE        | find_paired_zone_entry_for_card_stride_b     |
| DAT_08034290   | 0x0201c510 | gDuelFieldSlots            | find_paired_zone_entry_for_card_slots_b      |
| DAT_08034348   | 0x00000868 | PLAYER_BLOCK_STRIDE        | check_card_targeted_by_spell_zone_effect_stride |
| DAT_0803434c   | 0x0201c520 | gDuelFieldSlotState        | check_card_targeted_spell_zone_slot_state    |
| DAT_08034350   | 0x0201c510 | gDuelFieldSlots            | check_card_targeted_spell_zone_slots         |
| DAT_080343a8   | 0x00000868 | PLAYER_BLOCK_STRIDE        | check_slot_field_action_eligibility_stride   |
| DAT_080343ac   | 0x0201c510 | gDuelFieldSlots            | check_slot_field_action_eligibility_slots    |
| DAT_080343b0   | 0x0201e2a0 | gDuelCardCtxBase           | check_slot_field_action_eligibility_ctx      |
| DAT_08034518   | 0x00000868 | PLAYER_BLOCK_STRIDE        | check_slot_field_action_eligibility_stride_b |
| DAT_0803451c   | 0x0201c510 | gDuelFieldSlots            | check_slot_field_action_eligibility_slots_b  |
| DAT_08034524   | 0x0201e2a0 | gDuelCardCtxBase           | check_slot_field_action_eligibility_ctx_b    |
| DAT_080345a0   | 0x00000868 | PLAYER_BLOCK_STRIDE        | check_slot_field_action_eligibility_stride_c |
| DAT_080345a4   | 0x0201c510 | gDuelFieldSlots            | check_slot_field_action_eligibility_slots_c  |
| DAT_080345d4   | 0x0201e2a0 | gDuelCardCtxBase           | check_slot_field_action_eligibility_ctx_c    |
| DAT_08034674   | 0x00000868 | PLAYER_BLOCK_STRIDE        | check_field_spell_slot_placeable_stride      |
| DAT_08034678   | 0x0201c510 | gDuelFieldSlots            | check_field_spell_slot_placeable_slots       |
| DAT_08034738   | 0x00000868 | PLAYER_BLOCK_STRIDE        | check_slot_monster_activation_stride         |
| DAT_08034868   | 0x0201bb90 | gEquipChainSlotRefs        | check_slot_monster_activation_equip_refs     |
| DAT_08034880   | 0x00000868 | PLAYER_BLOCK_STRIDE        | check_slot_monster_activation_stride_b       |
| DAT_08034884   | 0x0201c510 | gDuelFieldSlots            | check_slot_monster_activation_slots_b        |
| DAT_080348dc   | 0x00000868 | PLAYER_BLOCK_STRIDE        | check_slot_monster_activation_stride_c       |
| DAT_080348e0   | 0x0201c510 | gDuelFieldSlots            | check_slot_monster_activation_slots_c        |
| DAT_080349f8   | 0x00000868 | PLAYER_BLOCK_STRIDE        | check_slot_card_activatable_stride           |
| DAT_080349fc   | 0x0201c510 | gDuelFieldSlots            | check_slot_card_activatable_slots            |
| DAT_08034acc   | 0x00000868 | PLAYER_BLOCK_STRIDE        | check_slot_full_activation_eligibility_stride |
| DAT_08034ad0   | 0x0201c510 | gDuelFieldSlots            | check_slot_full_activation_eligibility_slots  |
| DAT_08034ad4   | 0x0201e2a0 | gDuelCardCtxBase           | check_slot_full_activation_eligibility_ctx   |
| DAT_08034e40   | 0x00000868 | PLAYER_BLOCK_STRIDE        | check_slot_full_activation_stride_d          |
| DAT_08034e68   | 0x0201c510 | gDuelFieldSlots            | check_slot_full_activation_slots_d           |
| DAT_08034f14   | 0x00000868 | PLAYER_BLOCK_STRIDE        | check_slot_full_activation_stride_e          |
| DAT_08034f68   | 0x00000868 | PLAYER_BLOCK_STRIDE        | check_slot_full_activation_stride_f          |
| DAT_0803513c   | 0x00000868 | PLAYER_BLOCK_STRIDE        | check_slot_full_activation_stride_g          |
| DAT_08035158   | 0x0201c5d8 | gDuelFieldSlots_p2_base    | check_slot_full_activation_p2_base           |
| DAT_08035278   | 0x00000868 | PLAYER_BLOCK_STRIDE        | check_slot_full_activation_stride_h          |

evidence: ewram.inc file:all, duel_field.inc file:all; confidence high.

**Group B: Reuse existing card_info.inc constants**

| slot addr      | value      | const_name (existing)      | slot_label                                |
|----------------|------------|----------------------------|-------------------------------------------|
| DAT_0803467c   | 0x0000164f | EQUIP_CHAIN_PAIR_CARD_MAX  | check_field_spell_slot_placeable_cmax     |
| DAT_08035150   | 0x000012d1 | EQUIP_LOCK_B_CID           | check_slot_full_activation_equip_lock_b   |

evidence: card_info.inc:EQUIP_CHAIN_PAIR_CARD_MAX, EQUIP_LOCK_B_CID; confidence high.

**Group C: New constants to add to card_info.inc**

All CIDs verified against data/card-stats.s slot_id field (high confidence).

| slot addr      | value      | proposed const_name                  | slot_label                               | card name (card-stats.s)                          |
|----------------|------------|--------------------------------------|------------------------------------------|---------------------------------------------------|
| DAT_0803414c   | 0x000010f4 | UMI_CARD_ID                          | check_card_matches_active_effect_umi_cid | Umi (card-stats: slot=0x10F4 pw=22702055)        |
| DAT_08034794   | 0x000010f4 | UMI_CARD_ID                          | check_slot_monster_activation_umi_cid    | (same as above)                                   |
| DAT_08034154   | 0x0000150b | A_LEGENDARY_OCEAN_CARD_ID            | check_card_matches_proxy_ocean_cid       | A Legendary Ocean (card-stats: slot=0x150B)       |
| DAT_08034294   | 0x00001368 | SPELL_ZONE_TARGET_CARD_ID            | find_paired_zone_target_cid              | (effect node type 0x1368; cross-player effect)    |
| DAT_08034354   | 0x00001368 | SPELL_ZONE_TARGET_CARD_ID            | check_card_targeted_spell_zone_cid       | (same)                                            |
| DAT_080343b4   | 0x00001d48 | ACTIVATION_STATE_A_OFF               | check_slot_field_action_activation_off_a | NEW: gP1LifePoints+side*0x868+0x1d48; activation write offset A; 27 raw refs |
| DAT_0803452c   | 0x00001d78 | ACTIVATION_STATE_B_OFF               | check_slot_field_action_activation_off_b | NEW: gP1LifePoints+side*0x868+0x1d78; activation write offset B; 41 raw refs |
| DAT_080345dc   | 0x00001d78 | ACTIVATION_STATE_B_OFF               | check_slot_field_action_activation_off_b2 | (same value)                                     |
| DAT_0803417c   | 0x000010d8 | ACTIVE_EFFECT_CATEGORY_OFF           | check_card_matches_category_off          | NEW: gP1LifePoints+0x10d8=0x0201D5B8; active effect slot category word offset; 16 raw refs |
| DAT_08034738   | 0x00000868 | PLAYER_BLOCK_STRIDE                  | (already listed in Group A)              | (duplicate slot, same value)                      |
| DAT_08034a00   | 0x000012b4 | TOTAL_DEFENSE_SHOGUN_CARD_ID         | check_slot_card_activatable_tds_cid      | Total Defense Shogun (card-stats: slot=0x12B4)    |
| DAT_08034a04   | 0x00001956 | EHERO_RAMPART_BLASTER_CARD_ID        | check_slot_card_activatable_erb_cid      | Elemental Hero Rampart Blaster (card-stats: slot=0x1956) |
| DAT_08034ad8   | 0x00001d48 | ACTIVATION_STATE_A_OFF               | check_slot_full_activation_off_a         | (same as above)                                   |
| DAT_0803473c   | 0x00001723 | TWINHEADED_BEAST_CARD_ID             | check_slot_monster_activation_thb_cid   | Twinheaded Beast (card-stats: slot=0x1723)        |
| DAT_08034740   | 0x000014d5 | TYRANT_DRAGON_CARD_ID                | check_slot_monster_activation_td_cid    | Tyrant Dragon (card-stats: slot=0x14D5)           |
| DAT_080348e4   | 0x0000186c | ARMED_SAMURAI_BEN_KEI_CARD_ID        | check_slot_monster_activation_asbk_cid  | Armed Samurai - Ben Kei (card-stats: slot=0x186C) |

**Group D: New constants to add to duel_field.inc (non-CID offsets)**

| slot addr      | value      | proposed const_name            | slot_label                                        | note                                          |
|----------------|------------|-------------------------------|---------------------------------------------------|-----------------------------------------------|
| DAT_080343b4   | 0x00001d48 | ACTIVATION_STATE_A_OFF        | check_slot_field_action_activation_off_a          | see Group C above, add to duel_field.inc      |
| DAT_0803452c   | 0x00001d78 | ACTIVATION_STATE_B_OFF        | check_slot_field_action_activation_off_b          | see Group C above, add to duel_field.inc      |
| DAT_0803417c   | 0x000010d8 | ACTIVE_EFFECT_CATEGORY_OFF    | check_card_matches_category_off                   | see Group C above, add to duel_field.inc      |

Note: 0x1d48 and 0x1d78 go to duel_field.inc (field slot activation state offsets, not card IDs).
0x10d8 also to duel_field.inc (effect slot category offset, related to EFFECT_ZONE_PARTITION_OFF=0x10a4).

### REF_SLOTS (USER-label + DATA-ref)

**PTR_gP1LifePoints_* slots** - 10 occurrences, all pointing to gP1LifePoints (ewram.inc).
These are already named with base label `gP1LifePoints`; slot_label needs rename only.

| slot addr                    | target       | gas_label      | slot_label                                              |
|------------------------------|--------------|----------------|---------------------------------------------------------|
| PTR_gP1LifePoints_08034150   | gP1LifePoints | gP1LifePoints | check_card_matches_active_effect_gp1lp_a               |
| PTR_gP1LifePoints_08034178   | gP1LifePoints | gP1LifePoints | check_card_matches_active_effect_gp1lp_b               |
| PTR_gP1LifePoints_08034528   | gP1LifePoints | gP1LifePoints | check_slot_field_action_gp1lp_a                        |
| PTR_gP1LifePoints_080345d8   | gP1LifePoints | gP1LifePoints | check_slot_field_action_gp1lp_b                        |
| PTR_gP1LifePoints_08034734   | gP1LifePoints | gP1LifePoints | check_slot_monster_activation_gp1lp                    |
| PTR_gP1LifePoints_08034e3c   | gP1LifePoints | gP1LifePoints | check_slot_full_activation_gp1lp_a                     |
| PTR_gP1LifePoints_08034f10   | gP1LifePoints | gP1LifePoints | check_slot_full_activation_gp1lp_b                     |
| PTR_gP1LifePoints_08034f64   | gP1LifePoints | gP1LifePoints | check_slot_full_activation_gp1lp_c                     |
| PTR_gP1LifePoints_08035138   | gP1LifePoints | gP1LifePoints | check_slot_full_activation_gp1lp_d                     |
| PTR_gP1LifePoints_08035274   | gP1LifePoints | gP1LifePoints | check_slot_full_activation_gp1lp_e                     |

**Function pointer slot**

| slot addr    | target      | gas_label                 | slot_label                                     |
|--------------|-------------|---------------------------|------------------------------------------------|
| DAT_080346c0 | 0x0804aea1  | (THUMB fn at 0x0804aea0)  | check_field_spell_slot_placeable_fnptr         |

evidence: 4 ROM raw refs of 0x0804aea1 (odd = THUMB fn ptr); consumed as `bl count_monster_slots_by_fnptr` r1 arg at 0x080346ae. The function at 0x0804aea0 is a predicate used to filter monster slots. Slot gets a REF label `check_field_spell_slot_placeable_fnptr` with `.word 0x0804aea0 + 1` form. Confidence: high (4 THUMB refs confirmed by ref-scan).

### RENAME_SLOTS (pure rename + EOL)

All remaining DAT_ slots that hold card IDs or other values without new/existing equates.
These are card IDs verified in card-stats.s (high confidence) or chain IDs (medium confidence).

#### Verified card IDs (card-stats.s confirmed):

| slot addr      | value      | name / card-stats entry                              | slot_label                                          |
|----------------|------------|------------------------------------------------------|-----------------------------------------------------|
| DAT_0803446c   | 0x000012ce | Mesmeric Control (card_0655)                         | check_slot_field_action_chain_mesmeric_ctrl         |
| DAT_08034470   | 0x0000131e | unknown (NOT in card-stats: chain effect node type)  | check_slot_field_action_chain_node_131e             |
| DAT_08034474   | 0x000017b3 | Curse of Anubis (card_1607)                          | check_slot_field_action_chain_curse_anubis          |
| DAT_08034478   | 0x00001103 | Spellbinding Circle (card_0309)                      | check_slot_field_action_chain_spellbinding          |
| DAT_0803447c   | 0x00001243 | Shadow Spell (card_0544)                             | check_slot_field_action_chain_shadow_spell          |
| DAT_08034480   | 0x000014b2 | Nightmare Wheel (card_0999)                          | check_slot_field_action_chain_nightmare_wheel       |
| DAT_08034484   | 0x00001842 | Flint (card_1734)                                    | check_slot_field_action_chain_flint                 |
| DAT_08034488   | 0x00001743 | The Unhappy Girl (card_1518)                         | check_slot_field_action_chain_unhappy_girl          |
| DAT_0803448c   | 0x00001284 | Thousand-Eyes Restrict (card_0594)                   | check_slot_field_action_restrict_cid                |
| DAT_08034514   | 0x000010ef | Dragon Capture Jar (card_0291)                       | check_slot_field_action_dcj_cid                     |
| DAT_08034520   | 0x000015fb | Final Attack Orders (card_1255)                      | check_slot_field_action_final_atk_ord               |
| DAT_080345a8   | 0x00001419 | Goblin Attack Force (card_0900)                      | check_slot_field_action_goblin_atk_force            |
| DAT_080345ac   | 0x0000165e | Gravity Axe - Grarl (card_1334)                      | check_slot_field_action_gravity_axe                 |
| DAT_080345b0   | 0x0000187c | Swords of Concealing Light (card_1789)               | check_slot_field_action_swords_conceal              |
| DAT_08034688   | 0x00001691 | Terrorking Archfiend (card_1373)                     | check_field_spell_slot_terrorking_cid               |
| DAT_08034754   | 0x000014dc | Gray Wing (card_1036)                                | check_slot_monster_activation_gw_cid                |
| DAT_08034758   | 0x0000170a | Mataza the Zapper (card_1474)                        | check_slot_monster_activation_mataza_cid            |
| DAT_08034770   | 0x000018b9 | Master Monk (card_1833)                              | check_slot_monster_activation_master_monk_cid       |
| DAT_08034774   | 0x0000174f | Mermaid Knight (card_1530)                           | check_slot_monster_activation_mermaid_knight_cid    |
| DAT_08034788   | 0x000018fc | Cyber Twin Dragon (card_1885)                        | check_slot_monster_activation_ctd_cid               |
| DAT_0803486c   | 0x000016cb | BLS - Envoy of the Beginning (card_1421)             | check_slot_monster_activation_bls_cid               |
| DAT_08034870   | 0x00001661 | Twin Swords of Flashing Light - Tryce (card_1337)    | check_slot_monster_activation_twin_swords_cid       |
| DAT_08034874   | 0x000018cb | Double Attack (card_1851)                            | check_slot_monster_activation_double_atk_cid        |
| DAT_08034878   | 0x000019ab | Hero Heart (card_2020)                               | check_slot_monster_activation_hero_heart_cid        |
| DAT_0803487c   | 0x000015ff | Diffusion Wave-Motion (card_1260)                    | check_slot_monster_activation_diffusion_cid         |
| DAT_08034888   | 0x000018a6 | Elemental Hero Avian (card_1813)                     | check_slot_monster_activation_eh_avian_cid          |
| DAT_08034914   | 0x00001505 | Asura Priest (card_1072)                             | check_slot_monster_activation_asura_priest_cid_b    |
| DAT_080348e8   | 0x00001505 | Asura Priest (card_1072)                             | check_slot_monster_activation_asura_priest_cid_a    |
| DAT_080348ec   | 0x00001644 | Berserk Dragon (card_1309)                           | check_slot_monster_activation_berserk_dragon_cid    |
| DAT_08034900   | 0x00001958 | Elemental Hero Wildedge (card_1959)                  | check_slot_monster_activation_eh_wildedge_cid       |
| DAT_08034e04   | 0x0000149d | Ekibyo Drakmord (card_0987)                          | check_slot_full_activation_ekibyo_cid               |
| DAT_08034e08   | 0x000013f3 | Mask of the Accursed (card_0864)                     | check_slot_full_activation_mask_acc_cid             |
| DAT_08034e0c   | 0x00001842 | Flint (card_1734)                                    | check_slot_full_activation_flint_cid                |
| DAT_08034e10   | 0x00001103 | Spellbinding Circle (card_0309)                      | check_slot_full_activation_spellbinding_cid         |
| DAT_08034e14   | 0x00001243 | Shadow Spell (card_0544)                             | check_slot_full_activation_shadow_spell_cid         |
| DAT_08034e18   | 0x000014b2 | Nightmare Wheel (card_0999)                          | check_slot_full_activation_nightmare_wheel_cid      |
| DAT_08034e1c   | 0x00001766 | Wall of Revealing Light ATK thresh (card_1550)       | check_slot_full_activation_wrl_atk_thresh           |
| DAT_08034e20   | 0x000014a1 | Vengeful Bog Spirit (card_0989)                      | check_slot_full_activation_vbs_cid                  |
| DAT_08034e24   | 0x0000140e | Gravity Bind (card_0889)                             | check_slot_full_activation_gravity_bind_cid         |
| DAT_08034e28   | 0x00001469 | The Dark Door (card_0940)                            | check_slot_full_activation_dark_door_cid            |
| DAT_08034e2c   | 0x0000128a | unknown chain node type 0x128a                       | check_slot_full_activation_chain_128a               |
| DAT_08034e30   | 0x00001743 | The Unhappy Girl (card_1518)                         | check_slot_full_activation_unhappy_girl_cid         |
| DAT_08034e34   | 0x00001284 | Thousand-Eyes Restrict (card_0594)                   | check_slot_full_activation_restrict_cid             |
| DAT_08034e38   | 0x00001865 | Big-Tusked Mammoth (card_1766)                       | check_slot_full_activation_btm_cid                  |
| DAT_08034e44   | 0x00001944 | Level Modulation (card_1941)                         | check_slot_full_activation_level_mod_cid            |
| DAT_08034e48   | 0x00001208 | unknown chain node type 0x1208                       | check_slot_full_activation_chain_1208               |
| DAT_08034e4c   | 0x000015ed | Tribute Doll (card_1243)                             | check_slot_full_activation_tribute_doll_cid         |
| DAT_08034e50   | 0x0000156a | Puppet Master (card_1144)                            | check_slot_full_activation_puppet_master_cid        |
| DAT_08034e54   | 0x000014f7 | Silent Fiend (card_1061)                             | check_slot_full_activation_silent_fiend_cid         |
| DAT_08034e58   | 0x00001819 | Magician's Unite (card_1695)                         | check_slot_full_activation_magicians_unite_cid      |
| DAT_08034e5c   | 0x00001890 | Union Attack (card_1807)                             | check_slot_full_activation_union_attack_cid         |
| DAT_08034e60   | 0x000015ff | Diffusion Wave-Motion (card_1260)                    | check_slot_full_activation_diffusion_cid            |
| DAT_08034e64   | 0x0000195b | Feather Shot (card_1961)                             | check_slot_full_activation_feather_shot_cid         |
| DAT_08034e6c   | 0x00001636 | Metal Reflect Slime (card_1302)                      | check_slot_full_activation_metal_reflect_cid        |
| DAT_08034e70   | 0x00000ff8 | Red-Eyes B. Dragon (card_0088)                       | check_slot_full_activation_redeyes_cid              |
| DAT_08034e74   | 0x0000175b | Burst Stream of Destruction (card_1542)              | check_slot_full_activation_burst_stream_cid         |
| DAT_08034e88   | 0x0000161b | Armor Exe (card_1279)                                | check_slot_full_activation_armor_exe_cid            |
| DAT_08034ea4   | 0x000016cb | BLS - Envoy of Beginning (card_1421)                 | check_slot_full_activation_bls_cid                  |
| DAT_08034ec0   | 0x000017c7 | Andro Sphinx (card_1622)                             | check_slot_full_activation_andro_sphinx_cid         |
| DAT_08034ec4   | 0x000019c8 | Anteatereatingant (card_2043)                        | check_slot_full_activation_anteatereatingant_cid    |
| DAT_08034ee4   | 0x000017f6 | Inferno Fire Blast (card_1667)                       | check_slot_full_activation_inferno_fire_blast_cid   |
| DAT_08034f24   | 0x00000fb6 | Time Wizard (card_0016)                              | check_slot_full_activation_time_wizard_cid          |
| DAT_08035140   | 0x00001102 | Swords of Revealing Light (card_0308)                | check_slot_full_activation_swords_reveal_cid        |
| DAT_08035144   | 0x0000130e | unknown chain node type 0x130e                       | check_slot_full_activation_chain_130e               |
| DAT_08035148   | 0x000005db | field_score threshold 1499                           | check_slot_full_activation_score_thresh_a           |
| DAT_0803514c   | 0x0000134a | Messenger of Peace (card_0751 pw=44656491)           | check_slot_full_activation_msngr_peace_cid          |
| DAT_08035150   | 0x000012d1 | EQUIP_LOCK_B_CID (existing const in card_info.inc)   | check_slot_full_activation_equip_lock_b             |
| DAT_08035154   | 0x000014d1 | Array of Revealing Light (card_1025)                 | check_slot_full_activation_array_reveal_cid         |
| DAT_0803515c   | 0x00001358 | The Regulation of Tribe (card_0761)                  | check_slot_full_activation_regulation_tribe_cid     |
| DAT_08035160   | 0x0000076b | field_score threshold 1899                           | check_slot_full_activation_score_thresh_b           |
| DAT_08035164   | 0x00001523 | Gora Turtle (card_1097)                              | check_slot_full_activation_gora_turtle_cid          |
| DAT_08035168   | 0x0000182c | Harpie Lady 3 (card_1712)                            | check_slot_full_activation_harpie_3_cid             |
| DAT_0803516c   | 0x00001886 | Threatening Roar (card_1797)                         | check_slot_full_activation_threatening_roar_cid     |
| DAT_08035170   | 0x0000172d | Teva (card_1504 pw=16469012)                         | check_slot_full_activation_teva_cid                 |
| DAT_08035174   | 0x0000180d | copy record card_2093 (slot_id=0)                    | check_slot_full_activation_cid_180d                 |
| DAT_08035178   | 0x000014db | Cave Dragon (card_1035)                              | check_slot_full_activation_cave_dragon_cid          |
| DAT_08035190   | 0x00001813 | copy record card_2094 (slot_id=0)                    | check_slot_full_activation_cid_1813                 |
| DAT_08035194   | 0x0000195a | copy record card_2095 (slot=0x195A, special token)   | check_slot_full_activation_cid_195a                 |
| DAT_080351d0   | 0x0000127f | Toon Summoned Skull (card_0591)                      | check_slot_full_activation_toon_skull_cid           |
| DAT_080351f0   | 0x000012a5 | Blue-Eyes Toon Dragon (card_0629)                    | check_slot_full_activation_betd_cid                 |
| DAT_0803527c   | 0x0000131d | Gravekeeper's Servant (card_0710)                    | check_slot_full_activation_gk_servant_cid           |

#### Previously unknown CIDs - now resolved via card-stats.s:

| value  | card name                          | card-stats entry    | action                                         |
|--------|------------------------------------|---------------------|------------------------------------------------|
| 0x170a | Mataza the Zapper                  | card_1474 pw=22609617 | RENAME slot_label = check_slot_monster_activation_mataza_cid |
| 0x17c7 | Andro Sphinx                       | card_1622 pw=15013468 | RENAME slot_label = check_slot_full_activation_andro_sphinx_cid |
| 0x172d | Teva                               | card_1504 pw=16469012 | RENAME slot_label = check_slot_full_activation_teva_cid |
| 0x180d | copy record (slot=0x180D copy=0)   | card_2093           | RENAME slot_label = check_slot_full_activation_cid_180d |
| 0x1813 | copy record (slot=0x1813 copy=0)   | card_2094           | RENAME slot_label = check_slot_full_activation_cid_1813 |
| 0x134a | Messenger of Peace                 | card_0751 pw=44656491 | RENAME slot_label = check_slot_full_activation_msngr_peace_cid |
| 0x128a | NOT in card-stats (chain node type)| confirmed absent    | RENAME slot_label = check_slot_full_activation_chain_128a |

Note: 0x180d and 0x1813 are copy records with slot_id=0 — these are special token/copy record entries. Use `<func>_cid_<hex>` RENAME form (low confidence semantic). For 0x12d1 (DAT_08035150): reuse existing EQUIP_LOCK_B_CID from card_info.inc confirmed.

Note: 0x131e, 0x1208, 0x130e, 0x128a are used in `check_value_in_slot_chain` calls — these are chain/effect node type IDs, not card stat IDs. They do NOT appear in card-stats.s (confirmed). They use RENAME with EOL comment "chain node type 0x<val>".

### FUNC_RENAME

No function renames required. All 10 function names are consistent with their bodies:
- `eval_slot_target_eligibility_full`: body calls resolve_slot_card_id_for_pair + check_slot_card_pair_allowed loops — confirmed name.
- `check_card_matches_active_effect_slot`: body reads category from gP1LifePoints+0x10d8 and compares — confirmed name.
- `find_paired_zone_entry_for_card`: body scans zone entries for card_id 0x1368 pair — confirmed name.
- `check_card_targeted_by_spell_zone_effect`: body scans magic/trap slots 5..9 for 0x1368 — confirmed name.
- `check_slot_field_action_eligibility`: body checks bit21, calls multiple eligibility fns — confirmed name.
- `check_field_spell_slot_placeable`: body checks equip chain head then calls 3 gate fns — confirmed name.
- `check_slot_monster_activation_eligible`: body checks bit22/bit23, branches by card_id — confirmed name.
- `eval_slot_activation_guard_full`: body wraps check_slot_card_activatable + field_spell + 5-slot loop — confirmed name.
- `check_slot_card_activatable`: body reads card_id+equip_chain_head, branches 0x12b4/0x1956 — confirmed name.
- `check_slot_full_activation_eligibility`: body is large composite gate (200+ instructions) — confirmed name.

Indeg checks (from prior analysis plates):
- eval_slot_target_eligibility_full: indeg=2
- check_card_matches_active_effect_slot: indeg=13
- find_paired_zone_entry_for_card: indeg=12
- check_card_targeted_by_spell_zone_effect: indeg=2
- check_slot_field_action_eligibility: indeg=6
- check_field_spell_slot_placeable: indeg=3
- check_slot_monster_activation_eligible: indeg=2
- eval_slot_activation_guard_full: indeg=9
- check_slot_card_activatable: indeg=8
- check_slot_full_activation_eligibility: indeg=2

### PLATE (R5)

All 10 functions have existing plates from the naming phase. The plates reference no stale FUN_ names (all callees were named before this segment). Full rewrites are not required; substring patches only where needed.

Scan result: no FUN_* substrings in any of the 10 function plates in this segment
(all callees: resolve_slot_card_id_for_pair, check_slot_card_pair_allowed, classify_card_effect_category,
query_slot_effect_eligibility_nonzero, check_card_pair_allowed, find_effect_node_in_zone,
check_value_in_slot_chain, query_zone_chain_count_with_eligibility, count_equip_chain_default_flags,
count_field_copies_of_card, count_zones_by_card_and_mode, get_slot_card_state_code,
count_available_effect_zones, count_equip_set_activatable_slots_for_player,
count_paired_slots_with_field5_default, get_paired_card_id_by_variant, count_monster_slots_by_fnptr,
check_slot_card_effect_eligibility, check_slot_card_fieldspell_eligibility,
count_node_in_slot_chain, eval_slot_score_entry_full, count_equip_slots_meeting_atk_threshold,
count_occupied_monster_zones, count_slot_chain_nodes_by_card_id, get_node_entity_id_in_slot,
count_active_extended_chain_nodes, count_extra_deck_cards_by_id, count_occupied_all_field_zones,
count_monster_slots_by_state, count_equippable_slots_for_card, check_slot_has_node_by_card_id,
count_equip_zone_slots_matching_card — all named).

Plates that mention card names use ASCII only; no CJK present.
PLATE action = SKIP (no FUN_ stale text, existing plates are adequate).
If reviewer finds EOL comment additions needed for renamed slots, use ASCII only.

---

## carve Plan (R7)

N/A — No ROM_INCBIN or .byte blocks in Seg-10a range.

---

## disasm Plan (R4)

N/A — No code data blocks in Seg-10a range.

---

## New Constants / Globals

### New equates to add to duel_field.inc (Seg-10a section):

```asm
@ =============================================================================
@ file 02 Seg-10a additions: slot activation state write offsets
@ =============================================================================
.equ ACTIVATION_STATE_A_OFF,   0x00001d48  @ gP1LifePoints+side*0x868+0x1d48: activation state field A;
                                            @ written 0x3 on bit21-set guard fail; 27 raw refs; 2 Seg-10a slots
.equ ACTIVATION_STATE_B_OFF,   0x00001d78  @ gP1LifePoints+side*0x868+0x1d78: activation state field B;
                                            @ written 0x13 on exit_slot_activation_with_state_write; 41 raw refs; 2 Seg-10a slots
.equ ACTIVE_EFFECT_CATEGORY_OFF, 0x000010d8 @ gP1LifePoints+0x10d8=0x0201D5B8: active effect slot category word;
                                             @ read by check_card_matches_active_effect_slot; 16 raw refs; 1 Seg-10a slot
```

### New equates to add to card_info.inc (Seg-10a section):

```asm
@ =============================================================================
@ file 02 Seg-10a additions: card slot IDs for activation eligibility checks
@ =============================================================================
.equ UMI_CARD_ID,                    0x000010f4  @ Umi field spell (pw=22702055); special-case in check_card_matches_active_effect_slot; 31 raw refs; 2 slots
.equ A_LEGENDARY_OCEAN_CARD_ID,      0x0000150b  @ A Legendary Ocean (pw=00295517); proxy reference for Umi activation category; 18 raw refs; 1 slot
.equ SPELL_ZONE_TARGET_CARD_ID,      0x00001368  @ cross-player spell-zone effect node type ID; used in find_paired_zone_entry_for_card + check_card_targeted_by_spell_zone_effect; 11 raw refs; 2 slots
.equ TOTAL_DEFENSE_SHOGUN_CARD_ID,   0x000012b4  @ Total Defense Shogun (pw=75372290); special activation via slot[+0x10] bit5; 5 raw refs; 1 slot
.equ EHERO_RAMPART_BLASTER_CARD_ID,  0x00001956  @ Elemental Hero Rampart Blaster (pw=47737087); activation: inverted bit5 + zone count; 8 raw refs; 1 slot
.equ TWINHEADED_BEAST_CARD_ID,       0x00001723  @ Twinheaded Beast (pw=82035781); monster activation check; 4 raw refs; 1 slot
.equ TYRANT_DRAGON_CARD_ID,          0x000014d5  @ Tyrant Dragon (pw=94568601); monster activation check; 8 raw refs; 1 slot
.equ ARMED_SAMURAI_BEN_KEI_CARD_ID,  0x0000186c  @ Armed Samurai - Ben Kei (pw=84430950); monster activation check; 1 raw ref; 1 slot
```

---

## Section 5.1 Registration (Rule 3, zero-reference blocks)

None. No data blocks in Seg-10a range.

---

## Consumer Evidence (R6)

| slot / value   | semantic                              | evidence source                                          | confidence |
|----------------|---------------------------------------|----------------------------------------------------------|------------|
| 0x1d48         | activation state write offset A       | check_slot_field_action_eligibility @ 0x0803439e: `str r0,[gP1LifePoints+side*0x868+0x1d48]` with r0=3 | high |
| 0x1d78         | activation state write offset B       | exit_slot_activation_with_state_write @ 0x08035290: `str r1,[gP1LifePoints+0x1d78]` with r1=0x13 | high |
| 0x10d8         | active effect slot category offset    | check_card_matches_active_effect_slot @ 0x08034166: `ldr r1,[gP1LifePoints+0x10d8]` then `cmp r1,r0` (r0=classify_card_effect_category result) | high |
| 0x0804aea1     | filter predicate fn ptr               | check_field_spell_slot_placeable @ 0x080346ae: `bl count_monster_slots_by_fnptr` with r1=DAT_080346c0; 4 THUMB refs in ROM | high |
| 0x1368         | spell zone effect node type           | find_paired_zone_entry_for_card @ 0x08034206: `cmp r5,#0x1368` on slot card_id; check_card_targeted_by_spell_zone_effect @ 0x080342dc similar | high |
| 0x10f4 (Umi)   | Umi CID substitute proxy activation   | check_card_matches_active_effect_slot @ 0x08034132: `cmp r5,r0 (0x10f4)` -> special path using 0x150b proxy | high |
| 0x150b (Ocean) | A Legendary Ocean proxy for Umi       | check_card_matches_active_effect_slot @ 0x08034138: `subs r0,#0x1c` from 0x150b (0x150b-0x1c=0x10ef, classify_card_effect_category on Ocean) | high |
| gDuelFieldSlots (0x0201c510) | field slot base | All 10 functions; 14 slots in Seg-10a | high |
| PLAYER_BLOCK_STRIDE (0x868) | inter-player stride | All 10 functions; 19 slots in Seg-10a | high |

---

## Pending Verification (Fixer Gate)

All 7 originally-unknown CID values have been verified in card-stats.s during Phase 4:

1. 0x170a = Mataza the Zapper (card_1474 pw=22609617) - CONFIRMED
2. 0x17c7 = Andro Sphinx (card_1622 pw=15013468) - CONFIRMED
3. 0x172d = Teva (card_1504 pw=16469012) - CONFIRMED
4. 0x180d = copy record card_2093 (slot_id=0, copy record) - CONFIRMED low-semantic
5. 0x1813 = copy record card_2094 (slot_id=0, copy record) - CONFIRMED low-semantic
6. 0x134a = Messenger of Peace (card_0751 pw=44656491) - CONFIRMED
7. 0x12d1 = EQUIP_LOCK_B_CID (existing const in card_info.inc) - CONFIRMED reuse

No fixer pre-verification gates remain. Proposal is complete.

Note on 0x128a, 0x131e, 0x1208, 0x130e: These are chain node type IDs (NOT in card-stats.s; confirmed 0 matches). Use RENAME with EOL `@ chain node type ID; no card-stats entry`. These are medium confidence (20/9/16/7 raw refs respectively — widely used across ROM as chain effect types).

---

## Self-Check (Phase 4)

1. **EQ values vs ROM bytes**: All gDuelFieldSlots=0x0201c510, PLAYER_BLOCK_STRIDE=0x868, gDuelCardCtxBase=0x0201e2a0, gP1LifePoints=0x0201c4e0 verified against ewram.inc definitions. New constants 0x1d48, 0x1d78, 0x10d8 confirmed by ref-scan (27/41/16 raw refs). Confidence: high.

2. **carve fn-ptr table .word**: DAT_080346c0 holds raw 0x0804aea1 = THUMB fn ptr; already odd address as stored in ROM. No +1 manipulation needed in asm (the stored value is already the THUMB ptr). Confidence: high.

3. **plate/EOL text ASCII only**: No CJK in any proposed EOL comments or plate text. All strings use ASCII 0x00-0x7F. Verified by inspection.

4. **Section 5.1 = 0**: No ROM_INCBIN or .byte blocks in Seg-10a. Confirmed by grep.

5. **Slot name uniqueness**: All slot_labels follow `<func>_<desc>` pattern with `_b/_c/...` suffixes for multiple slots of same value in same function. No collision detected.

6. **C13 coverage**: 148 total slots = 10 PTR_ (REF) + 40 EQ_SLOTS (Group A+B) + 17 EQ_SLOTS (Group C+D new const) + 81 RENAME_SLOTS. Total = 148. Coverage: 100%.

---

## Executor Report: F02Seg10a

- Slots: EQ=57 REF=11 RENAME=80 FUNC_RENAME=0 PLATE=0
- carve=0 disasm=0 section5.1=0
- New constants/globals:
  - duel_field.inc: ACTIVATION_STATE_A_OFF=0x1d48, ACTIVATION_STATE_B_OFF=0x1d78, ACTIVE_EFFECT_CATEGORY_OFF=0x10d8
  - card_info.inc: UMI_CARD_ID=0x10f4, A_LEGENDARY_OCEAN_CARD_ID=0x150b, SPELL_ZONE_TARGET_CARD_ID=0x1368, TOTAL_DEFENSE_SHOGUN_CARD_ID=0x12b4, EHERO_RAMPART_BLASTER_CARD_ID=0x1956, TWINHEADED_BEAST_CARD_ID=0x1723, TYRANT_DRAGON_CARD_ID=0x14d5, ARMED_SAMURAI_BEN_KEI_CARD_ID=0x186c
- Seg-10b range: [0x08035280..0x08035f54), 7 functions, 98 slots (to be handled next)
- Pending verification: NONE (all 7 originally-unknown CIDs resolved in Phase 4 self-check)
- proposal: doc/dev/refine/F02Seg10a.proposal.md
