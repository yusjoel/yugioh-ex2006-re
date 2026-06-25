# Refine Proposal: F11-Seg-9  [0x08091888..0x08093598)

Source file: asm/11_effect_slot_puzzletext.s  lines 26885-30911

## 段测绘

### 函数入口 x16

| addr        | name                                                |
|-------------|-----------------------------------------------------|
| 0x08091888  | eval_field_equip_activation_candidates (~0x1afc B, 187 pool slots) |
| 0x080931de  | flush_field_spell_equip_slot_sprites                |
| 0x08093384  | trigger_equip_activation_candidate_scan             |
| 0x08093390  | trigger_card_display_op31_if_not_active             |
| 0x080933b4  | invoke_card_display_op_0x31_sub1                    |
| 0x080933c8  | invoke_card_display_op_0x31_with_params             |
| 0x080933dc  | invoke_card_display_op_0x31_sub3_with_packed_params |
| 0x0809347c  | invoke_card_display_op_0x31_sub4                    |
| 0x08093490  | invoke_card_display_op_0x31_sub5                    |
| 0x080934a4  | invoke_card_display_op_0x31_sub6_with_packed_params |
| 0x080934c4  | invoke_card_display_op_0x31_sub7_with_packed_params |
| 0x080934e4  | invoke_card_display_op_0x31_sub8                    |
| 0x080934f8  | invoke_card_display_op_0x31_sub9                    |
| 0x08093514  | invoke_card_display_op_0x31_sub9_with_packed_params |
| 0x08093534  | invoke_card_display_op_0x31_sub10                   |
| 0x0809355c  | invoke_card_display_op_0x31                         |
| 0x08093570  | invoke_card_display_op_0x31_sub12                   |
| 0x08093584  | invoke_card_display_op_0x31_sub13                   |
| 0x08093598  | play_card_ok_ui_effect  (boundary = Seg-10 start)   |

### 残留自动名槽 x191

Total DAT_ + DWORD_ + PTR_ definition labels in [0x08091888, 0x08093598): **191**  
(DAT_/DWORD_: 184; PTR_gP1LifePoints_*: 7 -- need RENAME to ptr_lp_* per segment convention)

### ROM_INCBIN / .byte 块

None found in Seg-9.

---

## 数据块分类 (Rule 2/3) -- ref-scan

No ROM_INCBIN or .byte blocks exist in Seg-9. All residuals are literal-pool `.word` slots
inside two functions: eval_field_equip_activation_candidates (164 DAT_) and
flush_field_spell_equip_slot_sprites + invoke_card_display_op_0x31_sub3_with_packed_params
(20 DAT_/DWORD_).

---

## 符号化计划

### EQ_SLOTS (data-equate)

#### Group A: RAM-global addresses (REUSE existing ewram.inc constants)

| slot addr    | ROM value    | const_name                  | slot_label                     | status |
|--------------|--------------|-----------------------------|--------------------------------|--------|
| 0x08091904   | 0x0201bb90   | gEquipChainSlotRefs         | ptr_gEquipChainSlotRefs_1904   | REUSE ewram.inc:317 |
| 0x08091954   | 0x0201bb90   | gEquipChainSlotRefs         | ptr_gEquipChainSlotRefs_1954   | REUSE |
| 0x08091a90   | 0x0201bb90   | gEquipChainSlotRefs         | ptr_gEquipChainSlotRefs_1a90   | REUSE |
| 0x08091b60   | 0x0201bb90   | gEquipChainSlotRefs         | ptr_gEquipChainSlotRefs_1b60   | REUSE |
| 0x08091bec   | 0x0201bb90   | gEquipChainSlotRefs         | ptr_gEquipChainSlotRefs_1bec   | REUSE |
| 0x08091d88   | 0x0201bb90   | gEquipChainSlotRefs         | ptr_gEquipChainSlotRefs_1d88   | REUSE |
| 0x08091e44   | 0x0201bb90   | gEquipChainSlotRefs         | ptr_gEquipChainSlotRefs_1e44   | REUSE |
| 0x08091ef4   | 0x0201bb90   | gEquipChainSlotRefs         | ptr_gEquipChainSlotRefs_1ef4   | REUSE |
| 0x08091f94   | 0x0201bb90   | gEquipChainSlotRefs (DWORD) | ptr_gEquipChainSlotRefs_1f94   | REUSE |
| 0x0809229c   | 0x0201bb90   | gEquipChainSlotRefs         | ptr_gEquipChainSlotRefs_229c   | REUSE |
| 0x08092308   | 0x0201bb90   | gEquipChainSlotRefs         | ptr_gEquipChainSlotRefs_2308   | REUSE |
| 0x080923cc   | 0x0201bb90   | gEquipChainSlotRefs         | ptr_gEquipChainSlotRefs_23cc   | REUSE |
| 0x080924c4   | 0x0201bb90   | gEquipChainSlotRefs         | ptr_gEquipChainSlotRefs_24c4   | REUSE |
| 0x080924fc   | 0x0201bb90   | gEquipChainSlotRefs         | ptr_gEquipChainSlotRefs_24fc   | REUSE |
| 0x0809286c   | 0x0201bb90   | gEquipChainSlotRefs         | ptr_gEquipChainSlotRefs_286c   | REUSE |
| 0x08092ac4   | 0x0201bb90   | gEquipChainSlotRefs         | ptr_gEquipChainSlotRefs_2ac4   | REUSE |
| 0x08092af8   | 0x0201bb90   | gEquipChainSlotRefs         | ptr_gEquipChainSlotRefs_2af8   | REUSE |
| 0x08092b40   | 0x0201bb90   | gEquipChainSlotRefs         | ptr_gEquipChainSlotRefs_2b40   | REUSE |
| 0x08092b78   | 0x0201bb90   | gEquipChainSlotRefs         | ptr_gEquipChainSlotRefs_2b78   | REUSE |
| 0x08092bc4   | 0x0201bb90   | gEquipChainSlotRefs         | ptr_gEquipChainSlotRefs_2bc4   | REUSE |
| 0x08092c20   | 0x0201bb90   | gEquipChainSlotRefs         | ptr_gEquipChainSlotRefs_2c20   | REUSE |
| 0x08092c78   | 0x0201bb90   | gEquipChainSlotRefs         | ptr_gEquipChainSlotRefs_2c78   | REUSE |
| 0x08092cb8   | 0x0201bb90   | gEquipChainSlotRefs         | ptr_gEquipChainSlotRefs_2cb8   | REUSE |
| 0x08092ce4   | 0x0201bb90   | gEquipChainSlotRefs         | ptr_gEquipChainSlotRefs_2ce4   | REUSE |
| 0x08092de0   | 0x0201bb90   | gEquipChainSlotRefs         | ptr_gEquipChainSlotRefs_2de0   | REUSE |
| 0x08092e18   | 0x0201bb90   | gEquipChainSlotRefs         | ptr_gEquipChainSlotRefs_2e18   | REUSE |
| 0x08093188   | 0x0201bb90   | gEquipChainSlotRefs         | ptr_gEquipChainSlotRefs_3188   | REUSE |
| 0x08093248   | 0x0201bb90   | gEquipChainSlotRefs         | ptr_gEquipChainSlotRefs_3248   | REUSE |
| 0x080932cc   | 0x0201bb90   | gEquipChainSlotRefs         | ptr_gEquipChainSlotRefs_32cc   | REUSE |
| 0x0809337c   | 0x0201bb90   | gEquipChainSlotRefs         | ptr_gEquipChainSlotRefs_337c   | REUSE |
| 0x080933b0   | 0x0201e2a0   | gDuelCardCtxBase            | ptr_gDuelCardCtxBase_33b0      | REUSE ewram.inc:218 |
| 0x08092898   | 0x0201c510   | gDuelFieldSlots             | ptr_gDuelFieldSlots_2898       | REUSE ewram.inc:314 |
| 0x08092360   | 0x0201c510   | gDuelFieldSlots             | ptr_gDuelFieldSlots_2360       | REUSE |
| 0x08092c80   | 0x0201c510   | gDuelFieldSlots             | ptr_gDuelFieldSlots_2c80       | REUSE |
| 0x0809289c   | 0x0201d9c0   | gEquipNodePool              | ptr_gEquipNodePool_289c        | REUSE ewram.inc:316 |
| 0x080931b8   | 0x0201d9c0   | gEquipNodePool              | ptr_gEquipNodePool_31b8        | REUSE |
| 0x080928a0   | 0x0201c520   | gDuelFieldSlotState         | ptr_gDuelFieldSlotState_28a0   | REUSE ewram.inc:318 |
| 0x080931bc   | 0x0201c520   | gDuelFieldSlotState         | ptr_gDuelFieldSlotState_31bc   | REUSE |
| 0x08093470   | 0x0201e4f0   | gEquipEffectZoneBase        | ptr_gEquipEffectZoneBase_3470  | REUSE ewram.inc:550 |
| 0x08091d98   | 0x0201bc2c   | gEquipActivationSlotBase    | ptr_gEquipActivationSlotBase_1d98 | NEW (see REF_SLOTS; this is gEquipChainSlotRefs+0x9c absolute addr) |

Note: DAT_08091da0 = 0x0201c5fc (gDuelFieldSlots+0xec) -- see REF_SLOTS.

#### Group B: PLAYER_BLOCK_STRIDE (REUSE ewram.inc:251)

| slot addr    | ROM value    | const_name           | slot_label              |
|--------------|--------------|----------------------|-------------------------|
| 0x0809190c   | 0x00000868   | PLAYER_BLOCK_STRIDE  | equip_player_stride_190c|
| 0x08091d9c   | 0x00000868   | PLAYER_BLOCK_STRIDE  | equip_player_stride_1d9c|
| 0x08092360 (wait - this is 0x0201c510, see A)  |
| 0x0809287c   | 0x00000868   | PLAYER_BLOCK_STRIDE  | equip_player_stride_287c|
| 0x08092c7c   | 0x00000868   | PLAYER_BLOCK_STRIDE  | equip_player_stride_2c7c|
| 0x08092d14   | 0x00000868   | PLAYER_BLOCK_STRIDE  | equip_player_stride_2d14|
| 0x0809235c   | 0x00000868   | PLAYER_BLOCK_STRIDE  | equip_player_stride_235c|
| 0x080923f8   | 0x00000868   | PLAYER_BLOCK_STRIDE  | equip_player_stride_23f8|
| 0x08093198   | 0x00000868   | PLAYER_BLOCK_STRIDE  | equip_player_stride_3198|

#### Group C: Known score/mask constants (REUSE)

| slot addr    | ROM value    | const_name                        | slot_label                | status |
|--------------|--------------|-----------------------------------|---------------------------|--------|
| 0x08091f94 (DWORD)  | 0x0201bb90 | (already Group A)              |                           |        |
| 0x08091f98 (DWORD)  | 0x000016a3 | DARK_SCORPION_COMBO_CID           | cid_dark_scorpion_1f98    | REUSE card_info.inc |
| 0x08091f9c (DWORD)  | 0x00001663 | ROD_OF_THE_MINDS_EYE_CID          | cid_rod_minds_eye_1f9c    | NEW (see new consts) |
| 0x08091fa0 (DWORD)  | 0x00001890 | UNION_ATTACK_CID                  | cid_union_attack_1fa0     | REUSE card_info.inc |
| 0x080921c8   | 0x00001ce8   | P1LP_BLOCK2_OFF_1CE8              | lp_block2_off_21c8        | REUSE ewram.inc:276 |
| 0x080921cc   | 0x00001cf4   | P2LP_BLOCK2_OFF_1CF4              | lp_block2_off_21cc        | REUSE ewram.inc:277 |
| 0x080921e4   | 0x0000076b   | FIELD5_SCORE_ACTIVATION_THRESHOLD | score_thresh_21e4         | REUSE duel_field.inc:184 |
| 0x080921fc   | 0xffff0000   | EQUIP_CHAIN_SENTINEL              | chain_sentinel_21fc       | REUSE duel_field.inc:272 |
| 0x08092afc   | 0xffff0000   | EQUIP_CHAIN_SENTINEL              | chain_sentinel_2afc       | REUSE |
| 0x08093380   | 0x0000ffff   | EQUIP_ACTIVATION_CNT_CAP          | act_cnt_cap_3380          | NEW (domain distinct from EQUIP_SLOT_SCORE_CAP/SLOT_CARD_EMPTY/OAM_ATTR0_HIDDEN; conf: high, ewram.inc gEquipChainSlotRefs+0x9c cap) |
| 0x08093474   | 0xffffe000   | OAM_ATTR2_TILE_CLEAR              | attr2_tile_clr_3474       | REUSE oam_attr.inc:24 |
| 0x08093478   | 0x00001fff   | SLOT_CARD_SET_CODE_MASK           | set_code_mask_3478        | REUSE card_info.inc:113 |

#### Group D: CID BST nodes -- eval_field_equip_activation_candidates first BST pass ([0x08091888..0x08091bff])

The function performs a 6-call structure with per-player equip slot scoring loops.
Each iteration uses a BST (binary search tree) over card IDs to dispatch per-card logic.

| slot addr    | ROM value    | CID const_name                             | slot_label                | REUSE/NEW |
|--------------|--------------|--------------------------------------------|---------------------------|-----------|
| 0x080919d0   | 0x000016ff   | DARK_DRICERATOPS_CID                       | cid_dark_drice_19d0       | NEW |
| 0x080919d4   | 0x0000154c   | EXARION_UNIVERSE_CID                       | cid_exarion_19d4          | REUSE card_info.inc:559 |
| 0x080919d8   | 0x00001416   | MAD_SWORD_BEAST_CID                        | cid_mad_sword_19d8        | NEW |
| 0x080919e0   | 0x000014d6   | SPEAR_DRAGON_CID                           | cid_spear_dragon_19e0     | NEW |
| 0x080919f4   | 0x00001651   | GYAKU_GIRE_PANDA_CID                       | cid_gyaku_panda_19f4      | REUSE card_info.inc:340 |
| 0x080919fc   | 0x0000168b   | MEFIST_THE_INFERNAL_GENERAL_CID            | cid_mefist_19fc           | REUSE card_info.inc |
| 0x08091a18   | 0x0000194d   | ELEMENTAL_HERO_BLADEDGE_CID                | cid_bladedge_1a18         | NEW |
| 0x08091a24   | 0x000018fd   | CYBER_END_DRAGON_CID                       | cid_cyber_end_1a24        | REUSE card_info.inc |
| 0x08091a40   | 0x00001991   | RANCER_DRAGONUTE_CID                       | cid_rancer_1a40           | NEW |
| 0x08091a50   | 0x000019c9   | SABER_BEETLE_CID                           | cid_saber_beetle_1a50     | NEW |
| 0x08091a94   | 0x000015f2   | METEORAIN_CID                              | cid_meteorain_1a94        | REUSE card_info.inc |
| 0x08091aa0   | 0x000016fc   | ENRAGED_BATTLE_OX_CID                      | cid_enraged_ox_1aa0       | NEW |
| 0x08091b50   | 0x000014e3   | DRAGONS_RAGE_CID                           | cid_dragons_rage_1b50     | NEW |
| 0x08091b54   | 0x00000fcb   | GAIA_THE_DRAGON_CHAMPION_CID               | cid_gaia_dragon_1b54      | NEW |
| 0x08091b58   | 0x0000147b   | SWIFT_GAIA_THE_FIERCE_KNIGHT_CID           | cid_swift_gaia_1b58       | NEW |
| 0x08091b5c   | 0x0000187d   | SPIRAL_SPEAR_STRIKE_CID                    | cid_spiral_spear_1b5c     | REUSE card_info.inc |
| 0x08091b64   | 0x00001408   | FAIRY_METEOR_CRUSH_CID                     | cid_fairy_meteor_1b64     | NEW |
| 0x08091b68   | 0x00001625   | BIG_BANG_SHOT_CID                          | cid_big_bang_1b68         | REUSE card_info.inc:578 |
| 0x08091b6c   | 0x00001496   | CYCLON_LASER_CID                           | cid_cyclon_laser_1b6c     | REUSE card_info.inc:862 |
| 0x08091b70   | 0x000015ce   | PITCH_DARK_DRAGON_CID                      | cid_pitch_dark_1b70       | NEW |
| 0x08091bf0   | 0x00001408   | FAIRY_METEOR_CRUSH_CID (dup)               | cid_fairy_meteor_1bf0     | NEW (dup of 1b64) |
| 0x08091bf4   | 0x00001625   | BIG_BANG_SHOT_CID (dup)                    | cid_big_bang_1bf4         | REUSE |
| 0x08091bf8   | 0x00001496   | CYCLON_LASER_CID (dup)                     | cid_cyclon_laser_1bf8     | REUSE |
| 0x08091bfc   | 0x000015ce   | PITCH_DARK_DRAGON_CID (dup)                | cid_pitch_dark_1bfc       | NEW |
| 0x08091c20   | 0x00001883   | CROSS_COUNTER_CID                          | cid_cross_counter_1c20    | NEW |
| 0x08091c5c   | 0x000019f2   | FAULT_ZONE_CID                             | cid_fault_zone_1c5c       | NEW |

#### Group E: CID BST second pass -- first block [0x08091d84..0x08091f93]

| slot addr    | ROM value    | CID const_name                             | slot_label                | REUSE/NEW |
|--------------|--------------|--------------------------------------------|---------------------------|-----------|
| 0x08091d84   | 0x00001493   | DESTRUCTION_PUNCH_CID                      | cid_dest_punch_1d84       | NEW |
| 0x08091d8c   | 0x00001883   | CROSS_COUNTER_CID (dup)                    | cid_cross_counter_1d8c    | NEW |
| 0x08091d90   | 0x0000162e   | CONTINUOUS_DESTRUCTION_PUNCH_CID           | cid_cont_dest_punch_1d90  | NEW |
| 0x08091d94   | 0x0000151e   | LAST_TURN_CID                              | cid_last_turn_1d94        | REUSE card_info.inc:1447 |
| 0x08091da4   | 0x000010f4   | UMI_CARD_ID                                | cid_umi_1da4              | REUSE card_info.inc |
| 0x08091da8   | 0x000013f7   | TORNADO_WALL_CID                           | cid_tornado_wall_1da8     | REUSE card_info.inc:508 |
| 0x08091dac   | 0x0000175e   | SANCTUARY_IN_THE_SKY_CID                   | cid_sanctuary_1dac        | REUSE card_info.inc:1234 |
| 0x08091e40   | 0x0000179d   | EMISSARY_OF_OASIS_CID                      | cid_emissary_1e40         | REUSE card_info.inc:194 |
| 0x08091e48   | 0x000018aa   | WINGED_KURIBOH_CID                         | cid_winged_kuri_1e48      | REUSE card_info.inc |
| 0x08091e4c   | 0x000017fe   | SPIRIT_BARRIER_CID                         | cid_spirit_barrier_1e4c   | NEW |
| 0x08091e50   | 0x00001989   | BUBBLE_BLASTER_CID                         | cid_bubble_blast_1e50     | NEW |
| 0x08091ef8   | 0x00001989   | BUBBLE_BLASTER_CID (dup)                   | cid_bubble_blast_1ef8     | NEW |
| 0x08091efc   | 0x00001805   | HALLOWED_LIFE_BARRIER_CID                  | cid_hallow_life_1efc      | REUSE card_info.inc |
| 0x08091f00   | 0x000015ec   | KISHIDO_SPIRIT_CID                         | cid_kishido_1f00          | NEW |
| 0x08091f04   | 0x0000168d   | SHADOWKNIGHT_ARCHFIEND_CID                 | cid_shadowknight_1f04     | NEW |
| 0x08091f10   | 0x00001750   | PIRANHA_ARMY_CID                           | cid_piranha_army_1f10     | NEW |

#### Group F: CID BST -- second large pass [0x08091fec..0x08092500]

| slot addr    | ROM value    | CID const_name                             | slot_label                | REUSE/NEW |
|--------------|--------------|--------------------------------------------|---------------------------|-----------|
| 0x08091fec   | 0x0000164d   | GUARDIAN_BAOU_CID                          | cid_guardian_baou_1fec    | REUSE card_info.inc:1411 |
| 0x08091ff0   | 0x000014e9   | KAISER_GLIDER_CID                          | cid_kaiser_glider_1ff0    | REUSE card_info.inc |
| 0x08091ff4   | 0x000012ac   | SATELLITE_CANNON_CID                       | cid_satellite_1ff4        | REUSE card_info.inc:497 |
| 0x08092004   | 0x000013cb   | ROCKET_WARRIOR_CID                         | cid_rocket_warrior_2004   | NEW |
| 0x08092020   | 0x000014af   | AMAZONESS_FIGHTER_CID                      | cid_amazoness_ftr_2020    | REUSE card_info.inc |
| 0x08092038   | 0x000014b6   | DARK_BALTER_THE_TERRIBLE_CID               | cid_dark_balter_2038      | REUSE card_info.inc |
| 0x08092058   | 0x00001596   | SPIRIT_REAPER_CID                          | cid_spirit_reaper_2058    | REUSE card_info.inc:1573 |
| 0x08092068   | 0x0000157e   | FGD_CID                                    | cid_fgd_2068              | REUSE card_info.inc:1552 |
| 0x0809207c   | 0x00001622   | ULTIMATE_OBEDIENT_FIEND_CID                | cid_ult_obedient_207c     | NEW |
| 0x08092094   | 0x00001642   | DARK_FLARE_KNIGHT_CID                      | cid_dark_flare_2094       | NEW |
| 0x080920c8   | 0x00001855   | CASTLE_GATE_CID                            | cid_castle_gate_20c8      | NEW |
| 0x080920d8   | 0x00001743   | UNHAPPY_GIRL_CID                           | cid_unhappy_girl_20d8     | REUSE card_info.inc:345 |
| 0x080920ec   | 0x00001827   | ELEMENT_SAURUS_CID                         | cid_element_saurus_20ec   | REUSE card_info.inc:356 |
| 0x080920fc   | 0x0000182b   | HARPIE_LADY_2_CID                          | cid_harpie_lady2_20fc     | NEW |
| 0x08092124   | 0x00001913   | BES_CRYSTAL_CORE_CID                       | cid_bes_crystal_2124      | REUSE card_info.inc |
| 0x08092134   | 0x000018b8   | MONK_FIGHTER_CID                           | cid_monk_fighter_2134     | NEW |
| 0x08092150   | 0x00001955   | CYBER_BLADER_CID                           | cid_cyber_blader_2150     | REUSE card_info.inc:373 |
| 0x08092164   | 0x00001962   | BES_TETRAN_CID                             | cid_bes_tetran_2164       | REUSE card_info.inc |
| 0x08092438   | 0x0000170d   | GETSU_FUHMA_CID                            | cid_getsu_fuhma_2438      | NEW |
| 0x0809242c   | 0x0000170e   | RYU_KOKKI_CID                              | cid_ryu_kokki_242c        | NEW |
| 0x08092450   | 0x00001866   | KANGAROO_CHAMP_CID                         | cid_kangaroo_2450         | REUSE card_info.inc:1505 |
| 0x08092464   | 0x00001950   | OXYGEDDON_CID                              | cid_oxygeddon_2464        | REUSE card_info.inc:944 |
| 0x08092500   | 0x000017d5   | DARK_MIMIC_LV1_CID                         | cid_dark_mimic_2500       | REUSE card_info.inc |

#### Group G: CID BST -- third large pass [0x08092870..0x08092e1c] (symmetric repeat of Group E+F pattern for second player slot evaluation)

| slot addr    | ROM value    | const_name                             | slot_label                | REUSE/NEW |
|--------------|--------------|--------------------------------------------|---------------------------|-----------|
| 0x08092870   | 0x00001663   | ROD_OF_THE_MINDS_EYE_CID                   | cid_rod_minds_eye_2870    | NEW |
| 0x08092874   | 0x00001890   | UNION_ATTACK_CID                           | cid_union_attack_2874     | REUSE |
| 0x08092880   | 0x00001594   | CHARM_OF_SHABTI_CID                        | cid_charm_shabti_2880     | NEW |
| 0x08092884   | 0x00001805   | HALLOWED_LIFE_BARRIER_CID (dup)            | cid_hallow_life_2884      | REUSE |
| 0x08092888   | 0x0000150a   | HEART_OF_CLEAR_WATER_CID                   | cid_heart_clear_2888      | REUSE card_info.inc |
| 0x0809288c   | 0x000017ff   | NINJITSU_ART_OF_DECOY_CID                  | cid_ninjitsu_288c         | REUSE card_info.inc:532 |
| 0x08092890   | 0x00001992   | MISTOBODY_CID                              | cid_mistobody_2890        | NEW |
| 0x08092894   | 0x00001957   | ELEMENTAL_HERO_TEMPEST_CID                 | cid_eh_tempest_2894       | REUSE card_info.inc |
| 0x080928a4   | 0x00001989   | BUBBLE_BLASTER_CID (dup)                   | cid_bubble_blast_28a4     | NEW |
| 0x080928a8   | 0x000015b3   | Z_METAL_TANK_CID                           | cid_z_metal_28a8          | REUSE card_info.inc |
| 0x080928ac   | 0x000015ff   | DIFFUSION_WAVE_MOTION_CID                  | cid_diffusion_28ac        | REUSE card_info.inc |
| 0x080928b0   | 0x0000165f   | WICKED_BREAKING_FLAMBERGE_BAOU_CID         | cid_wicked_flamberge_28b0 | REUSE card_info.inc |
| 0x080928b4   | 0x000014b5   | DARK_RULER_HA_DES_CID                      | cid_dark_ruler_28b4       | NEW |
| 0x080928b8   | 0x000018cd   | KAMINOTE_BLOW_CID                          | cid_kaminote_28b8         | REUSE card_info.inc |
| 0x080928bc   | 0x0000164d   | GUARDIAN_BAOU_CID (dup)                    | cid_guardian_baou_28bc    | REUSE |
| 0x080928c0   | 0x000014e9   | KAISER_GLIDER_CID (dup)                    | cid_kaiser_glider_28c0    | REUSE |
| 0x080928e8   | 0x000012ac   | SATELLITE_CANNON_CID (dup)                 | cid_satellite_28e8        | REUSE |
| 0x080928f8   | 0x000013cb   | ROCKET_WARRIOR_CID (dup)                   | cid_rocket_warrior_28f8   | NEW |
| 0x08092914   | 0x000014af   | AMAZONESS_FIGHTER_CID (dup)                | cid_amazoness_ftr_2914    | REUSE |
| 0x08092924   | 0x000014b6   | DARK_BALTER_THE_TERRIBLE_CID (dup)         | cid_dark_balter_2924      | REUSE |
| 0x08092944   | 0x00001596   | SPIRIT_REAPER_CID (dup)                    | cid_spirit_reaper_2944    | REUSE |
| 0x08092954   | 0x0000157e   | FGD_CID (dup)                              | cid_fgd_2954              | REUSE |
| 0x08092968   | 0x00001622   | ULTIMATE_OBEDIENT_FIEND_CID (dup)          | cid_ult_obedient_2968     | NEW |
| 0x08092980   | 0x00001642   | DARK_FLARE_KNIGHT_CID (dup)                | cid_dark_flare_2980       | NEW |
| 0x080929b4   | 0x00001855   | CASTLE_GATE_CID (dup)                      | cid_castle_gate_29b4      | NEW |
| 0x080929c4   | 0x00001743   | UNHAPPY_GIRL_CID (dup)                     | cid_unhappy_girl_29c4     | REUSE |
| 0x080929d8   | 0x00001827   | ELEMENT_SAURUS_CID (dup)                   | cid_element_saurus_29d8   | REUSE |
| 0x080929e8   | 0x0000182b   | HARPIE_LADY_2_CID (dup)                    | cid_harpie_lady2_29e8     | NEW |
| 0x08092a10   | 0x00001913   | BES_CRYSTAL_CORE_CID (dup)                 | cid_bes_crystal_2a10      | REUSE |
| 0x08092a20   | 0x000018b8   | MONK_FIGHTER_CID (dup)                     | cid_monk_fighter_2a20     | NEW |
| 0x08092a3c   | 0x00001955   | CYBER_BLADER_CID (dup)                     | cid_cyber_blader_2a3c     | REUSE |
| 0x08092a54   | 0x00001962   | BES_TETRAN_CID (dup)                       | cid_bes_tetran_2a54       | REUSE |
| 0x08092abc   | 0x00001ce8   | P1LP_BLOCK2_OFF_1CE8 (dup)                 | lp_block2_off_2abc        | REUSE |
| 0x08092ac0   | 0x00001cf4   | P2LP_BLOCK2_OFF_1CF4 (dup)                 | lp_block2_off_2ac0        | REUSE |
| 0x08092adc   | 0x0000076b   | FIELD5_SCORE_ACTIVATION_THRESHOLD (dup)    | score_thresh_2adc         | REUSE |
| 0x08092d48   | 0x0000170e   | RYU_KOKKI_CID (dup)                        | cid_ryu_kokki_2d48        | NEW |
| 0x08092d54   | 0x0000170d   | GETSU_FUHMA_CID (dup)                      | cid_getsu_fuhma_2d54      | NEW |
| 0x08092d6c   | 0x00001866   | KANGAROO_CHAMP_CID (dup)                   | cid_kangaroo_2d6c         | REUSE |
| 0x08092d80   | 0x00001950   | OXYGEDDON_CID (dup)                        | cid_oxygeddon_2d80        | REUSE |
| 0x08092e1c   | 0x000017d5   | DARK_MIMIC_LV1_CID (dup)                   | cid_dark_mimic_2e1c       | REUSE |

#### Group H: CID BST -- fourth pass [0x08093188..0x080931d4] (flush_field_spell_equip_slot_sprites sub-dispatch)

| slot addr    | ROM value    | const_name                             | slot_label                | REUSE/NEW |
|--------------|--------------|--------------------------------------------|---------------------------|-----------|
| 0x0809318c   | 0x00001663   | ROD_OF_THE_MINDS_EYE_CID (dup)             | cid_rod_minds_eye_318c    | NEW |
| 0x08093190   | 0x00001890   | UNION_ATTACK_CID (dup)                     | cid_union_attack_3190     | REUSE |
| 0x0809319c   | 0x00001594   | CHARM_OF_SHABTI_CID (dup)                  | cid_charm_shabti_319c     | NEW |
| 0x080931a0   | 0x00001805   | HALLOWED_LIFE_BARRIER_CID (dup)            | cid_hallow_life_31a0      | REUSE |
| 0x080931a4   | 0x0000150a   | HEART_OF_CLEAR_WATER_CID (dup)             | cid_heart_clear_31a4      | REUSE |
| 0x080931a8   | 0x000017ff   | NINJITSU_ART_OF_DECOY_CID (dup)            | cid_ninjitsu_31a8         | REUSE |
| 0x080931ac   | 0x00001992   | MISTOBODY_CID (dup)                        | cid_mistobody_31ac        | NEW |
| 0x080931b0   | 0x00001957   | ELEMENTAL_HERO_TEMPEST_CID (dup)           | cid_eh_tempest_31b0       | REUSE |
| 0x080931b4   | 0x0201c510   | gDuelFieldSlots (dup)                      | ptr_duel_slots_31b4       | REUSE |
| 0x080931c0   | 0x00001989   | BUBBLE_BLASTER_CID (dup)                   | cid_bubble_blast_31c0     | NEW |
| 0x080931c4   | 0x000015b3   | Z_METAL_TANK_CID (dup)                     | cid_z_metal_31c4          | REUSE |
| 0x080931c8   | 0x0000165f   | WICKED_BREAKING_FLAMBERGE_BAOU_CID (dup)   | cid_wicked_flamberge_31c8 | REUSE |
| 0x080931cc   | 0x000014b5   | DARK_RULER_HA_DES_CID (dup)                | cid_dark_ruler_31cc       | NEW |
| 0x080931d0   | 0x000018cd   | KAMINOTE_BLOW_CID (dup)                    | cid_kaminote_31d0         | REUSE |
| 0x080931d4   | 0x00001392   | SWORD_OF_DRAGONS_SOUL_CID                  | cid_sword_dragon_31d4     | NEW |
| 0x0809324c   | 0x000018f1   | GYROID_CID                                 | cid_gyroid_324c           | NEW |
| 0x08093250   | 0x00000fb6   | TIME_WIZARD_CID                            | cid_time_wizard_3250      | REUSE card_info.inc |
| 0x080932c8   | 0x000018f1   | GYROID_CID (dup)                           | cid_gyroid_32c8           | NEW |
| 0x080932d0   | 0x00000fb6   | TIME_WIZARD_CID (dup)                      | cid_time_wizard_32d0      | REUSE |

#### Group I: SANCTUARY_IN_THE_SKY_CID check

DAT_08091dac = 0x0000175e. C5 check:

- card_info.inc:367: `.equ SANCTUARY_CID_SHIFTED, 0xbaf00000` -- SHIFTED form, not CID 0x175e  
- card_info.inc:1234: `.equ SANCTUARY_IN_THE_SKY_CID, 0x0000175e` -- exact match, added Seg-7

REUSE card_info.inc:1234. No new .equ needed. Slot 0x08091dac handled in Group E above.

---

### REF_SLOTS (USER-label + DATA-ref for RAM addresses not yet labeled)

| slot addr    | target addr  | gas_label                          | slot_label                       | evidence |
|--------------|--------------|------------------------------------|----------------------------------|---------|
| 0x08091d98   | 0x0201bc2c   | gEquipActivationSlotBase           | ptr_equip_act_slot_base_1d98     | gEquipChainSlotRefs(0x0201bb90)+0x9c; plate says "Reads gEquipChainSlotRefs[+0x9c] (is_activated)"; code: adds r2,#0x9c; iterates 2-entry struct at 0x9c/0xb0 (stride 0x14); 2 raw ROM refs; conf: high |
| 0x08091da0   | 0x0201c5fc   | gDuelFieldSlotState_ec             | ptr_duel_field_state_ec_1da0     | gDuelFieldSlots(0x0201c510)+0xec; code: muls r0,player_stride; adds r0,r0,0x0201c5fc -> reads dword at [gDuelFieldSlots+player*0x868+0xec]; lsrs r0,#0x16 extracts 2-bit field; 1 raw ROM ref; conf: med (exact field semantics unclear; use base+offset labeling) |

Note: DAT_08091d98 can also be handled as EQ (absolute address value) rather than REF if only used as
a literal. Given 2 refs, REF (createLabel on 0x0201bc2c + addMemRef from 0x08091d98) is preferred.

---

### RENAME_SLOTS (pure rename + EOL)

The DWORD_ labels (lines 30808-30815: DWORD_08091f94..DWORD_08091fa0) are just DAT_ with different prefix;
they should be renamed to match EQ pattern same as other DAT_ slots.
The PTR_gP1LifePoints_* labels must be renamed to ptr_lp_* per Seg-5/6/7/8 convention (value=0x0201c4e0=gP1LifePoints; RENAME-only, the .word exports as `.word gP1LifePoints` after relabel).

| slot addr    | current_label                    | new_slot_label                  | eol_ascii |
|--------------|----------------------------------|---------------------------------|-----------|
| 0x08091f94   | DWORD_08091f94                   | ptr_gEquipChainSlotRefs_1f94    | (none) |
| 0x08091f98   | DWORD_08091f98                   | cid_dark_scorpion_1f98          | DARK_SCORPION_COMBO_CID |
| 0x08091f9c   | DWORD_08091f9c                   | cid_rod_minds_eye_1f9c          | ROD_OF_THE_MINDS_EYE_CID |
| 0x08091fa0   | DWORD_08091fa0                   | cid_union_attack_1fa0           | UNION_ATTACK_CID |
| 0x08091908   | PTR_gP1LifePoints_08091908       | ptr_lp_91908                    | gP1LifePoints (0x0201c4e0) |
| 0x080921c4   | PTR_gP1LifePoints_080921c4       | ptr_lp_921c4                    | gP1LifePoints (0x0201c4e0) |
| 0x080923f4   | PTR_gP1LifePoints_080923f4       | ptr_lp_923f4                    | gP1LifePoints (0x0201c4e0) |
| 0x08092878   | PTR_gP1LifePoints_08092878       | ptr_lp_92878                    | gP1LifePoints (0x0201c4e0) |
| 0x08092ab8   | PTR_gP1LifePoints_08092ab8       | ptr_lp_92ab8                    | gP1LifePoints (0x0201c4e0) |
| 0x08092d10   | PTR_gP1LifePoints_08092d10       | ptr_lp_92d10                    | gP1LifePoints (0x0201c4e0) |
| 0x08093194   | PTR_gP1LifePoints_08093194       | ptr_lp_93194                    | gP1LifePoints (0x0201c4e0) |

---

### FUNC_RENAME

No function name vs body contradiction detected.  
`eval_field_equip_activation_candidates` name matches body (iterates field slots for equip activation scoring).  
`flush_field_spell_equip_slot_sprites` name matches body (clears activation bits + enqueues OAM).  
Other invoke_card_display_op_0x31_subN stubs match names.

---

### PLATE (R5)

#### C8: plates with CJK (must rewrite to ASCII)

1. **flush_field_spell_equip_slot_sprites** (0x080931de, line 30340): plate is entirely CJK.
   Current: `@ [CJK text referencing FUN_08091888]`
   Replacement (full ASCII rewrite, <=500 chars, len=486):
   ```
   Callee of eval_field_equip_activation_candidates (indeg=6+). Guards: gEquipChainSlotRefs[+0x8] (busy) or sp[0x8] (ctx_flag) nonzero -> return. If [r4+0x2c] (activation_pending) set and r7==0: tests [r4+0x10] via check_value_in_slot_chain(TIME_WIZARD_CID=0x0fb6, 5 entries); on miss: clears [r4+0x2c], enqueues up to 3 OAM calls; on hit: 1 OAM call. P2 mirror at sp[0x10]. Side effects: [r4+0x2c]=0; up to 3 enqueue_sprite_attr calls. FUN_08091888=eval_field_equip_activation_candidates.
   ```

2. **invoke_card_display_op_0x31_sub1** (0x080933b4, line 30586): plate is entirely CJK.
   Current: `@ [CJK text about 3-instruction thunk]`
   Replacement (full ASCII rewrite, <=500 chars):
   ```
   3-instruction thunk (indeg=36). Fixed params op=0x31, sub=0x1; remaps entry r0 as dispatch_card_display_op 3rd arg (r2), r3=0. Call form: dispatch_card_display_op(0x31, 0x1, r0_in, 0). op=0x31 = copy_game_text_to_card_name_vram cluster; sub=0x1 vs sub=0x2 variant (invoke_card_display_op_0x31_with_params at 0x080933c8). Called by duel_field/card_frame/card_stats/game_str/font_jp modules. Side effects: via dispatch_card_display_op op=0x31: card-name VRAM buffer write. Constants: OP=0x31, SUB=0x1.
   ```

#### C8: stale FUN_ substring replacement

| function name                          | plate line | stale ref       | replace with |
|----------------------------------------|------------|-----------------|--------------|
| flush_field_spell_equip_slot_sprites   | 30340      | FUN_08091888    | eval_field_equip_activation_candidates |
| (also full CJK rewrite above)          |            |                 | |

(Other stale FUN_* in plates at lines 30557/30696/30780/30801/30847/30889 reference unnamed callers
in other files; not block-level errors, leave as-is per standard -- only fixing CJK plates and
the one FUN_08091888 stale ref since that function is named in this file.)

---

## carve 計画 (R7)

None. No ROM_INCBIN blocks found in Seg-9.

---

## disasm 計画 (R4)

None. No `.byte`-as-code stubs found via ref-scan in [0x08091888, 0x08093598).

---

## 新增 constants / 全局

All added to existing files (no new .inc file needed):

### card_info.inc (new CID equates -- C5 grep all confirmed 0 hits before adding)

```
DARK_DRICERATOPS_CID           = 0x000016ff  @ card_3978 slot=0x16FF; BST node eval_field_equip_activation_candidates
MAD_SWORD_BEAST_CID            = 0x00001416  @ card_3233; BST node
SPEAR_DRAGON_CID               = 0x000014d6  @ card_3425; BST node
ELEMENTAL_HERO_BLADEDGE_CID    = 0x0000194d  @ card_2150+; BST node
RANCER_DRAGONUTE_CID           = 0x00001991  @ card_2002 area; BST node
SABER_BEETLE_CID               = 0x000019c9  @ BST node eval_field_equip
ENRAGED_BATTLE_OX_CID          = 0x000016fc  @ card_3975; BST node
DRAGONS_RAGE_CID               = 0x000014e3  @ card_3438; BST node
GAIA_THE_DRAGON_CHAMPION_CID   = 0x00000fcb  @ card_2134; BST node
SWIFT_GAIA_THE_FIERCE_KNIGHT_CID = 0x0000147b @ card_3334; BST node
FAIRY_METEOR_CRUSH_CID         = 0x00001408  @ card_3233 area; BST node
PITCH_DARK_DRAGON_CID          = 0x000015ce  @ BST node
CROSS_COUNTER_CID              = 0x00001883  @ card_4366; BST node
FAULT_ZONE_CID                 = 0x000019f2  @ card_2002 area; BST node
DESTRUCTION_PUNCH_CID          = 0x00001493  @ card_3358; BST node
CONTINUOUS_DESTRUCTION_PUNCH_CID = 0x0000162e @ card_3769; BST node
@ EMISSARY_OF_OASIS_CID (0x0000179d) -- REUSE card_info.inc:194 (no _THE_); no new .equ
SPIRIT_BARRIER_CID             = 0x000017fe  @ card_4233; BST node
BUBBLE_BLASTER_CID             = 0x00001989  @ card_2002 Bubble Blaster; BST node (4 refs in Seg-9)
KISHIDO_SPIRIT_CID             = 0x000015ec  @ card_3703; BST node
SHADOWKNIGHT_ARCHFIEND_CID     = 0x0000168d  @ card_3864; BST node
PIRANHA_ARMY_CID               = 0x00001750  @ card_4059; BST node
ROD_OF_THE_MINDS_EYE_CID       = 0x00001663  @ BST node eval_field + flush_field; conf: high
CHARM_OF_SHABTI_CID            = 0x00001594  @ card_3615; BST node
DARK_RULER_HA_DES_CID          = 0x000014b5  @ card_3392; BST node
SWORD_OF_DRAGONS_SOUL_CID      = 0x00001392  @ card_3101; BST node flush_field
GYROID_CID                     = 0x000018f1  @ card_4476 Gyroid; BST node + check_value_in_slot_chain trigger
ULTIMATE_OBEDIENT_FIEND_CID    = 0x00001622  @ card_3757; BST node
DARK_FLARE_KNIGHT_CID          = 0x00001642  @ card_3789; BST node
CASTLE_GATE_CID                = 0x00001855  @ card_4320; BST node
HARPIE_LADY_2_CID              = 0x0000182b  @ card_4187 area; BST node
MONK_FIGHTER_CID               = 0x000018b8  @ card_4419; BST node
MISTOBODY_CID                  = 0x00001992  @ BST node; conf: med (card name from card-stats.s card_2002 area)
ROCKET_WARRIOR_CID             = 0x000013cb  @ card_3101 area; BST node
GETSU_FUHMA_CID                = 0x0000170d  @ card_3992; BST node
RYU_KOKKI_CID                  = 0x0000170e  @ card_3993; BST node
@ SANCTUARY_IN_THE_SKY_CID (0x0000175e) -- REUSE card_info.inc:1234; no new .equ
```

### ewram.inc (new absolute-address constants)

```
gEquipActivationSlotBase = 0x0201bc2c  @ gEquipChainSlotRefs+0x9c; 2-entry is_activated array; stride 0x14; 2 raw ROM refs; eval_field_equip_activation_candidates
gDuelFieldSlotState_ec   = 0x0201c5fc  @ gDuelFieldSlots+0xec; word with 2-bit field at bits[23:22]; player*0x868 offset applied at runtime; 1 raw ROM ref
```

### duel_field.inc (new saturation cap)

```
EQUIP_ACTIVATION_CNT_CAP = 0x0000ffff  @ gEquipChainSlotRefs+0x9c activation count saturation cap; flush_field_spell_equip_slot_sprites 30534; domain distinct from EQUIP_SLOT_SCORE_CAP(score)/SLOT_CARD_EMPTY(card sentinel)/OAM_ATTR0_HIDDEN(OAM)/LP_ROW_TYPE8_ALL_SLOTS_MASK; conf: high
```

---

## §5.1 登記 (Rule 3) -- 0 引用块

No §5.1 orphan blocks. No `.byte` or `ROM_INCBIN` blocks exist in Seg-9.

---

## 消费者証拠 (R6) -- 关键槽语义

| slot addr    | value       | const_name                          | evidence (file:line + conf) |
|--------------|-------------|-------------------------------------|-----------------------------|
| 0x08091904   | 0x0201bb90  | gEquipChainSlotRefs                 | asm/11 line 26948: `.word 0x0201bb90`; ldr r3, [+0x0] -> [+0x4] -> gDuelBattleState offsets; conf: high (260 raw ROM refs) |
| 0x0809190c   | 0x00000868  | PLAYER_BLOCK_STRIDE                 | asm/11 line 26952: muls r1, r5 where r5=DAT_0809190c; multiplies player_id; ewram.inc:251; conf: high (2146 refs) |
| 0x08091d98   | 0x0201bc2c  | gEquipActivationSlotBase            | asm/11 line 27473: ldr r0, DAT_08091d98; adds r4,r3,r0; iterates [r4+0x0],[r4+0xc] activation fields; plate confirms gEquipChainSlotRefs[+0x9c]=is_activated; conf: high |
| 0x080921e4   | 0x0000076b  | FIELD5_SCORE_ACTIVATION_THRESHOLD   | asm/11 line 28154: cmp r1, r0; bgt LAB_080921dc; duel_field.inc:184 confirms 8 raw refs; conf: high |
| 0x08091f98   | 0x000016a3  | DARK_SCORPION_COMBO_CID             | asm/11 line 27766: ldr r2, DWORD_08091f98; bl check_value_in_slot_chain; card_info.inc confirms; conf: high |
| 0x080933b0   | 0x0201e2a0  | gDuelCardCtxBase                    | asm/11 line 30569: ldr r1, DAT_080933b0; adds r1,#0x8; lsls r0,#2; ldr r0,[r0+r1]; state slot check; ewram.inc:218; conf: high |

---

## C13 覆盖声明

Total auto-name labels in [0x08091888..0x08093598):
- DAT_* labels: **180**
- DWORD_* labels: **4** (DWORD_08091f94..DWORD_08091fa0)
- PTR_gP1LifePoints_* labels: **7** (PTR_gP1LifePoints_08091908, _080921c4, _080923f4, _08092878, _08092ab8, _08092d10, _08093194)
- **Total: 191**

Disposition coverage:
- EQ_SLOTS (Groups A-I): 180 DAT_ slots accounted for (groups A:30 + B:8 + C:12 + D:26 + E:18 + F:23 + G:40 + H:19 = 176 DAT_ EQ slots; remainder 4 DWORD_ in Group C handled via EQ+RENAME)
- RENAME_SLOTS: 11 slots (4 DWORD_ + 7 PTR_gP1LifePoints_*)
- Note: Several slots appear duplicated (same CID value in both player-1 and player-2 BST passes); each is a separate slot label.

**All 191 auto-name labels (DAT_/DWORD_/PTR_) have a disposition assigned. 0 uncovered.**

Explicit DWORD_ list:
- DWORD_08091f94 (0x0201bb90) -> EQ gEquipChainSlotRefs + RENAME label
- DWORD_08091f98 (0x000016a3) -> EQ DARK_SCORPION_COMBO_CID + RENAME label
- DWORD_08091f9c (0x00001663) -> EQ ROD_OF_THE_MINDS_EYE_CID (NEW) + RENAME label
- DWORD_08091fa0 (0x00001890) -> EQ UNION_ATTACK_CID + RENAME label

Explicit PTR_gP1LifePoints_* list (all value=0x0201c4e0, RENAME-only -> ptr_lp_*):
- PTR_gP1LifePoints_08091908 -> ptr_lp_91908
- PTR_gP1LifePoints_080921c4 -> ptr_lp_921c4
- PTR_gP1LifePoints_080923f4 -> ptr_lp_923f4
- PTR_gP1LifePoints_08092878 -> ptr_lp_92878
- PTR_gP1LifePoints_08092ab8 -> ptr_lp_92ab8
- PTR_gP1LifePoints_08092d10 -> ptr_lp_92d10
- PTR_gP1LifePoints_08093194 -> ptr_lp_93194

---

## 求助

None. All slots have high or medium confidence semantic assignments backed by code evidence.

Two medium-confidence items:
1. `gDuelFieldSlotState_ec` (0x0201c5fc): exact field semantics of gDuelFieldSlots+0xec bits[23:22] are unclear; named as state-indicator by analogy with gDuelFieldSlotState pattern; conf: med.
2. `MISTOBODY_CID` (0x00001992): card_2002 area per card-stats.s; name from card-stats.s but not verified against card_info.inc previously; conf: med.
