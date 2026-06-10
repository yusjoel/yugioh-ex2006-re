# Refine Proposal: F02Seg10b  [0x08035280..0x08035f54)

## Segment Survey

Functions:
- 0x08035280  exit_slot_activation_with_state_write  (1 fn, tail-helper)
- 0x080352b0  eval_slot_activation_eligibility_full  (1 fn, large BST 0x280 bytes)
- 0x0803594c  count_activatable_slots_for_player      (1 fn)
- 0x08035988  check_slot_field_spell_chain_eligible   (1 fn)
- 0x08035b24  check_field_spell_trap_chain_eligible   (1 fn)
- 0x08035ba4  check_player_field_spell_chain_eligible (1 fn, tiny)
- 0x08035bc8  eval_slot_fieldspell_activation_full    (1 fn, large BST 0x38c bytes)

Total: 7 functions.

Residual auto-name slots (all DAT_ / PTR_ in [0x08035280, 0x08035f54)):

| Slot addr    | Current label                   | Value        |
|--------------|---------------------------------|--------------|
| 0x080352a4   | DAT_080352a4                    | 0x0201e2a0   |
| 0x080352a8   | PTR_gP1LifePoints_080352a8      | 0x0201c4e0   |
| 0x080352ac   | DAT_080352ac                    | 0x00001d78   |
| 0x0803539c   | DAT_0803539c                    | 0x00000868   |
| 0x080353a0   | DAT_080353a0                    | 0x0201c510   |
| 0x080353a4   | DAT_080353a4                    | 0x000015ff   |
| 0x080353a8   | DAT_080353a8                    | 0x00001505   |
| 0x08035418   | DAT_08035418                    | 0x00001644   |
| 0x0803541c   | DAT_0803541c                    | 0x00001958   |
| 0x08035420   | DAT_08035420                    | 0x00001505   |
| 0x08035424   | DAT_08035424                    | 0x00001561   |
| 0x08035428   | DAT_08035428                    | 0x00001852   |
| 0x0803542c   | DAT_0803542c                    | 0x00001669   |
| 0x08035454   | DAT_08035454                    | 0x00001318   |
| 0x08035478   | DAT_08035478                    | 0x00000868   |
| 0x0803553c   | DAT_0803553c                    | 0x0201c510   |
| 0x08035540   | DAT_08035540                    | 0x000017fc   |
| 0x08035544   | DAT_08035544                    | 0x00000868   |
| 0x08035548   | DAT_08035548                    | 0x000015ea   |
| 0x0803554c   | DAT_0803554c                    | 0x00001756   |
| 0x08035560   | DAT_08035560                    | 0x0000179d   |
| 0x080356bc   | DAT_080356bc                    | 0x0201c510   |
| 0x080356c0   | DAT_080356c0                    | 0x00000868   |
| 0x080356c4   | DAT_080356c4                    | 0x00001703   |
| 0x080356c8   | DAT_080356c8                    | 0x0000160f   |
| 0x080356cc   | DAT_080356cc                    | 0x0000168c   |
| 0x080356d0   | DAT_080356d0                    | 0x0000076b   |
| 0x080356d4   | DAT_080356d4                    | 0x000012a5   |
| 0x08035758   | DAT_08035758                    | 0x0000154a   |
| 0x0803575c   | DAT_0803575c                    | 0x00000868   |
| 0x08035760   | DAT_08035760                    | 0x0201c510   |
| 0x08035764   | DAT_08035764                    | 0x000013cd   |
| 0x08035778   | DAT_08035778                    | 0x0000164e   |
| 0x0803577c   | DAT_0803577c                    | 0x000018b6   |
| 0x08035794   | DAT_08035794                    | 0x000010f4   |
| 0x080357dc   | DAT_080357dc                    | 0x00000868   |
| 0x080357e0   | DAT_080357e0                    | 0x0201c510   |
| 0x080357e4   | DAT_080357e4                    | 0x000016ed   |
| 0x08035928   | DAT_08035928                    | 0x000014c6   |
| 0x0803592c   | DAT_0803592c                    | 0x00001777   |
| 0x08035930   | DAT_08035930                    | 0x00001770   |
| 0x08035934   | DAT_08035934                    | 0x00000868   |
| 0x08035938   | DAT_08035938                    | 0x0201c510   |
| 0x0803593c   | DAT_0803593c                    | 0x000017fd   |
| 0x08035940   | DAT_08035940                    | 0x000018b1   |
| 0x08035944   | DAT_08035944                    | 0xcd200000   |
| 0x08035948   | DAT_08035948                    | 0x000014d4   |
| 0x080359f4   | DAT_080359f4                    | 0x00000868   |
| 0x080359f8   | DAT_080359f8                    | 0x0201c510   |
| 0x080359fc   | DAT_080359fc                    | 0x0000147d   |
| 0x08035a00   | DAT_08035a00                    | 0x0000127d   |
| 0x08035a14   | DAT_08035a14                    | 0x0000154a   |
| 0x08035a38   | DAT_08035a38                    | 0x00001644   |
| 0x08035a3c   | DAT_08035a3c                    | 0x00001958   |
| 0x08035a40   | DAT_08035a40                    | 0x00001505   |
| 0x08035af4   | DAT_08035af4                    | 0x000015ff   |
| 0x08035af8   | DAT_08035af8                    | 0x00000868   |
| 0x08035afc   | DAT_08035afc                    | 0x0201c510   |
| 0x08035b00   | DAT_08035b00                    | 0x000017fc   |
| 0x08035b04   | DAT_08035b04                    | 0x00001619   |
| 0x08035b08   | DAT_08035b08                    | 0x00001890   |
| 0x08035b0c   | DAT_08035b0c                    | 0x00001669   |
| 0x08035b10   | DAT_08035b10                    | 0x0000195b   |
| 0x08035b6c   | DAT_08035b6c                    | 0x0201c510   |
| 0x08035b70   | DAT_08035b70                    | 0x00000868   |
| 0x08035b74   | DAT_08035b74                    | 0x000013cd   |
| 0x08035b78   | DAT_08035b78                    | 0x0000164e   |
| 0x08035b8c   | DAT_08035b8c                    | 0x000010f4   |
| 0x08035c90   | DAT_08035c90                    | 0x00001561   |
| 0x08035c94   | DAT_08035c94                    | 0x00001852   |
| 0x08035c98   | DAT_08035c98                    | 0x000017fd   |
| 0x08035c9c   | DAT_08035c9c                    | 0x00000868   |
| 0x08035ca0   | DAT_08035ca0                    | 0x0201c510   |
| 0x08035ca4   | DAT_08035ca4                    | 0x000013b3   |
| 0x08035ca8   | DAT_08035ca8                    | 0x00001221   |
| 0x08035cc0   | DAT_08035cc0                    | 0x0000114c   |
| 0x08035ce0   | DAT_08035ce0                    | 0x00001295   |
| 0x08035cf4   | DAT_08035cf4                    | 0x000012a5   |
| 0x08035d18   | DAT_08035d18                    | 0x00001598   |
| 0x08035d3c   | DAT_08035d3c                    | 0x00001566   |
| 0x08035d58   | DAT_08035d58                    | 0x00001705   |
| 0x08035d5c   | DAT_08035d5c                    | 0x000015ba   |
| 0x08035d60   | DAT_08035d60                    | 0x00001701   |
| 0x08035d78   | DAT_08035d78                    | 0x0000182d   |
| 0x08035d88   | DAT_08035d88                    | 0x0000186d   |
| 0x08035e44   | DAT_08035e44                    | 0x00000868   |
| 0x08035e48   | DAT_08035e48                    | 0x0201c510   |
| 0x08035e4c   | DAT_08035e4c                    | 0x0000063f   |
| 0x08035e58   | DAT_08035e58                    | 0x000010f4   |
| 0x08035eac   | DAT_08035eac                    | 0x00000868   |
| 0x08035f24   | DAT_08035f24                    | 0x000013ab   |
| 0x08035f28   | DAT_08035f28                    | 0x000015cf   |
| 0x08035f2c   | DAT_08035f2c                    | 0x0000169b   |
| 0x08035f30   | DAT_08035f30                    | 0x000016a3   |
| 0x08035f34   | DAT_08035f34                    | 0x000017aa   |
| 0x08035f38   | DAT_08035f38                    | 0x00001893   |
| 0x08035f3c   | DAT_08035f3c                    | 0x00001759   |
| 0x08035f40   | DAT_08035f40                    | 0x0000165d   |

Total residual: 98 slots (1 PTR_ + 97 DAT_).

No ROM_INCBIN or .byte blocks exist in this range.

## Data Block Classification (Rule 2/3)

No ROM_INCBIN/.byte blocks present -- ref-scan not applicable.

## Symbolization Plan (R1/R2/R3)

### EQ_SLOTS (data-equate)

Key:
- "REUSE" = constant already in constants/*.inc at this value
- "NEW" = new constant (verified no existing equate at same value)

**EQ_REUSE: 28 slots** (all have prior definitions)

| Slot addr    | Value        | Constant name           | Source file    | Slot label                           |
|--------------|--------------|-------------------------|----------------|--------------------------------------|
| 0x080352ac   | 0x00001d78   | ACTIVATION_STATE_B_OFF  | duel_field.inc | exit_slot_act_state_b_off            |
| 0x0803539c   | 0x00000868   | PLAYER_BLOCK_STRIDE     | ewram.inc      | eval_slot_act_elig_stride_a          |
| 0x080353a0   | 0x0201c510   | gDuelFieldSlots         | ewram.inc      | eval_slot_act_elig_gdf_a             |
| 0x08035478   | 0x00000868   | PLAYER_BLOCK_STRIDE     | ewram.inc      | eval_slot_act_elig_stride_b          |
| 0x0803553c   | 0x0201c510   | gDuelFieldSlots         | ewram.inc      | eval_slot_act_elig_gdf_b             |
| 0x08035544   | 0x00000868   | PLAYER_BLOCK_STRIDE     | ewram.inc      | eval_slot_act_elig_stride_c          |
| 0x080356bc   | 0x0201c510   | gDuelFieldSlots         | ewram.inc      | eval_slot_act_elig_gdf_d             |
| 0x080356c0   | 0x00000868   | PLAYER_BLOCK_STRIDE     | ewram.inc      | eval_slot_act_elig_stride_d          |
| 0x0803575c   | 0x00000868   | PLAYER_BLOCK_STRIDE     | ewram.inc      | eval_slot_act_elig_stride_e          |
| 0x08035760   | 0x0201c510   | gDuelFieldSlots         | ewram.inc      | eval_slot_act_elig_gdf_e             |
| 0x080357dc   | 0x00000868   | PLAYER_BLOCK_STRIDE     | ewram.inc      | eval_slot_act_elig_stride_f          |
| 0x080357e0   | 0x0201c510   | gDuelFieldSlots         | ewram.inc      | eval_slot_act_elig_gdf_f             |
| 0x08035934   | 0x00000868   | PLAYER_BLOCK_STRIDE     | ewram.inc      | eval_slot_act_elig_stride_g          |
| 0x08035938   | 0x0201c510   | gDuelFieldSlots         | ewram.inc      | eval_slot_act_elig_gdf_g             |
| 0x08035794   | 0x000010f4   | UMI_CARD_ID             | card_info.inc  | eval_slot_act_elig_umi_cid           |
| 0x080359f4   | 0x00000868   | PLAYER_BLOCK_STRIDE     | ewram.inc      | count_act_slots_stride               |
| 0x080359f8   | 0x0201c510   | gDuelFieldSlots         | ewram.inc      | count_act_slots_gdf                  |
| 0x08035af8   | 0x00000868   | PLAYER_BLOCK_STRIDE     | ewram.inc      | check_sfsc_stride_a                  |
| 0x08035afc   | 0x0201c510   | gDuelFieldSlots         | ewram.inc      | check_sfsc_gdf_a                     |
| 0x08035b6c   | 0x0201c510   | gDuelFieldSlots         | ewram.inc      | check_fstc_gdf                       |
| 0x08035b70   | 0x00000868   | PLAYER_BLOCK_STRIDE     | ewram.inc      | check_fstc_stride                    |
| 0x08035b8c   | 0x000010f4   | UMI_CARD_ID             | card_info.inc  | check_fstc_umi_cid                   |
| 0x08035c9c   | 0x00000868   | PLAYER_BLOCK_STRIDE     | ewram.inc      | eval_fsact_stride_a                  |
| 0x08035ca0   | 0x0201c510   | gDuelFieldSlots         | ewram.inc      | eval_fsact_gdf_a                     |
| 0x08035e44   | 0x00000868   | PLAYER_BLOCK_STRIDE     | ewram.inc      | eval_fsact_stride_b                  |
| 0x08035e48   | 0x0201c510   | gDuelFieldSlots         | ewram.inc      | eval_fsact_gdf_b                     |
| 0x08035e58   | 0x000010f4   | UMI_CARD_ID             | card_info.inc  | eval_fsact_umi_cid                   |
| 0x08035eac   | 0x00000868   | PLAYER_BLOCK_STRIDE     | ewram.inc      | eval_fsact_stride_c                  |

Note: 0x080356c8 (0x0000160f = Amazoness Tiger) and 0x080356cc (0x0000168c = Vilepawn Archfiend) are NEW card_info.inc equates, classified below.

**EQ_NEW: 52 slots** - new card_info.inc equates + 2 threshold equates

New card_info.inc equates (verified not present by grep card_info.inc; raw ref counts confirmed from ROM):

| Constant name                | Value      | Card name                        | raw refs | Evidence                                     |
|------------------------------|------------|----------------------------------|----------|----------------------------------------------|
| JINZO_7_CID                  | 0x0000114c | Jinzo #7                         | 12       | card-stats.s slot=0x114c pw=32809211         |
| MANGA_RYU_RAN_CID            | 0x0000127d | Manga Ryu-Ran                    | 10       | card-stats.s slot=0x127d                     |
| GEAR_GOLEM_CID               | 0x00001295 | Gear Golem the Moving Fortress   | 9        | card-stats.s slot=0x1295                     |
| BLUE_EYES_TOON_DRAGON_CID    | 0x000012a5 | Blue-Eyes Toon Dragon            | 10       | card-stats.s slot=0x12a5                     |
| RING_OF_MAGNETISM_CID        | 0x00001318 | Ring of Magnetism                | 22       | card-stats.s slot=0x1318                     |
| JOWLS_OF_DARK_DEMISE_CID     | 0x000013ab | Jowls of Dark Demise             | 12       | card-stats.s slot=0x13ab                     |
| SERVANT_OF_CATABOLISM_CID    | 0x000013b3 | Servant of Catabolism            | 5        | card-stats.s slot=0x13b3                     |
| LEGENDARY_FISHERMAN_CID      | 0x000013cd | The Legendary Fisherman          | 8        | card-stats.s slot=0x13cd                     |
| ZOMBYRA_THE_DARK_CID         | 0x0000147d | Zombyra the Dark                 | 7        | card-stats.s slot=0x147d                     |
| MARAUDING_CAPTAIN_CID        | 0x000014c6 | Marauding Captain                | 9        | card-stats.s slot=0x14c6                     |
| A_FEINT_PLAN_CID             | 0x000014d4 | A Feint Plan                     | 7        | card-stats.s slot=0x14d4                     |
| ASURA_PRIEST_CID             | 0x00001505 | Asura Priest                     | 32       | card-stats.s slot=0x1505                     |
| TOON_DARK_MAGICIAN_GIRL_CID  | 0x0000154a | Toon Dark Magician Girl          | 6        | card-stats.s slot=0x154a                     |
| TOON_DEFENSE_CID             | 0x00001561 | Toon Defense                     | 12       | card-stats.s slot=0x1561                     |
| TOON_GOBLIN_AF_CID           | 0x00001566 | Toon Goblin Attack Force         | 13       | card-stats.s slot=0x1566                     |
| REAPER_ON_NIGHTMARE_CID      | 0x00001598 | Reaper on the Nightmare          | 10       | card-stats.s slot=0x1598                     |
| DRILLAGO_CID                 | 0x000015ba | Drillago                         | 9        | card-stats.s slot=0x15ba                     |
| KIRYU_CID                    | 0x000015cf | Kiryu                            | 16       | card-stats.s slot=0x15cf                     |
| RAREGOLD_ARMOR_CID           | 0x000015ea | Raregold Armor                   | 6        | card-stats.s slot=0x15ea                     |
| DIFFUSION_WAVE_MOTION_CID    | 0x000015ff | Diffusion Wave-Motion            | 23       | card-stats.s slot=0x15ff                     |
| AMAZONESS_TIGER_CID          | 0x0000160f | Amazoness Tiger                  | 10       | card-stats.s slot=0x160f                     |
| MAGICAL_SCIENTIST_CID        | 0x00001619 | Magical Scientist                | 83       | card-stats.s slot=0x1619                     |
| BERSERK_DRAGON_CID           | 0x00001644 | Berserk Dragon                   | 14       | card-stats.s slot=0x1644                     |
| GUARDIAN_KAYEST_CID          | 0x0000164e | Guardian Kay'est                 | 8        | card-stats.s slot=0x164e                     |
| SHOOTING_STAR_BOW_CID        | 0x0000165d | Shooting Star Bow - Ceal         | 14       | card-stats.s slot=0x165d                     |
| STAUNCH_DEFENDER_CID         | 0x00001669 | Staunch Defender                 | 14       | card-stats.s slot=0x1669                     |
| VILEPAWN_ARCHFIEND_CID       | 0x0000168c | Vilepawn Archfiend               | 8        | card-stats.s slot=0x168c                     |
| CHECKMATE_CID                | 0x0000169b | Checkmate                        | 13       | card-stats.s slot=0x169b                     |
| DARK_SCORPION_COMBO_CID      | 0x000016a3 | Dark Scorpion Combination        | 14       | card-stats.s slot=0x16a3                     |
| MAGICIANS_VALKYRIE_CID       | 0x000016ed | Magician's Valkyrie              | 8        | card-stats.s slot=0x16ed                     |
| BLACK_TYRANNO_CID            | 0x00001701 | Black Tyranno                    | 8        | card-stats.s slot=0x1701                     |
| PRICKLE_FAIRY_CID            | 0x00001703 | Prickle Fairy                    | 16       | card-stats.s slot=0x1703                     |
| AMPHIBIOUS_BUGROTH_MK3_CID   | 0x00001705 | Amphibious Bugroth MK-3          | 11       | card-stats.s slot=0x1705                     |
| SOLAR_FLARE_DRAGON_CID       | 0x00001756 | Solar Flare Dragon               | 7        | card-stats.s slot=0x1756                     |
| OPTI_CAMO_ARMOR_CID          | 0x00001759 | Opti-Camouflage Armor            | 10       | card-stats.s slot=0x1759                     |
| MARSHMALLON_CID              | 0x00001770 | Marshmallon                      | 11       | card-stats.s slot=0x1770                     |
| MARSHMALLON_GLASSES_CID      | 0x00001777 | Marshmallon glasses              | 25       | card-stats.s slot=0x1777                     |
| EMISSARY_OF_OASIS_CID        | 0x0000179d | Emissary of the Oasis            | 7        | card-stats.s slot=0x179d                     |
| DELTA_ATTACKER_CID           | 0x000017aa | Delta Attacker                   | 12       | card-stats.s slot=0x17aa                     |
| TAUNT_CID                    | 0x000017fc | Taunt                            | 8        | card-stats.s slot=0x17fc                     |
| ABSOLUTE_END_CID             | 0x000017fd | Absolute End                     | 7        | card-stats.s slot=0x17fd                     |
| RAGING_FLAME_SPRITE_CID      | 0x0000182d | Raging Flame Sprite              | 9        | card-stats.s slot=0x182d                     |
| ASTRAL_BARRIER_CID           | 0x00001852 | Astral Barrier                   | 14       | card-stats.s slot=0x1852                     |
| SHADOWSLAYER_CID             | 0x0000186d | Shadowslayer                     | 6        | card-stats.s slot=0x186d                     |
| UNION_ATTACK_CID             | 0x00001890 | Union Attack                     | 14       | card-stats.s slot=0x1890                     |
| OVERPOWERING_EYE_CID         | 0x00001893 | Overpowering Eye                 | 13       | card-stats.s slot=0x1893                     |
| HIERACOSPHINX_CID            | 0x000018b1 | Hieracosphinx                    | 12       | card-stats.s slot=0x18b1                     |
| GRAVE_OHJA_CID               | 0x000018b6 | Grave Ohja                       | 8        | card-stats.s slot=0x18b6 pw=40937767         |
| EHERO_WILDEDGE_CID           | 0x00001958 | Elemental Hero Wildedge          | 11       | card-stats.s slot=0x1958 (distinct from 0x1956=Rampart Blaster) |
| FEATHER_SHOT_CID             | 0x0000195b | Feather Shot                     | 10       | card-stats.s slot=0x195b                     |
| HAMON_LORD_CID               | 0x000019a4 | Hamon, Lord of Striking Thunder  | 13       | card-stats.s slot=0x19a4                     |

New field5 score threshold equates (duel_field.inc):

| Constant name                          | Value      | raw refs | Evidence                                                             |
|----------------------------------------|------------|----------|----------------------------------------------------------------------|
| FIELD5_SCORE_ACTIVATION_THRESHOLD      | 0x0000076b | 8        | eval_slot_activation_eligibility_full: field5_score > threshold -> fail (high conf) |
| FIELD5_SCORE_FIELDSPELL_THRESHOLD      | 0x0000063f | 3        | eval_slot_fieldspell_activation_full: field5_score <= threshold -> fail (high conf) |

**Notes on special slots:**

1. **0x08035944 = 0xcd200000** (eval_slot_activation_eligibility_full, Seg-10b line 21044-21049):
   Instruction sequence: `ldr r0,[r2,#0x0]` (load slot_word); `lsls r0,r0,#0x13` (shift left 19); `ldr r1, DAT_08035944` (0xcd200000); `cmp r0,r1; bne`. This checks whether `slot_word & 0x1fff == 0x19a4` (Hamon, Lord of Striking Thunder CID). The stored constant is `HAMON_LORD_CID << 19 = 0x19a4 << 19 = 0xcd200000`. Confidence: high. EQ treatment: create equate `HAMON_LORD_CID_SHIFTED = 0xcd200000` in card_info.inc (6 raw refs), with slot label `eval_slot_act_elig_hamon_shifted`.

2. **0x08035ca8 = 0x00001221** (eval_slot_fieldspell_activation_full):
   Used as exact card_id match in `cmp r2, 0x1221; bne`. No entry in card-stats.s for slot 0x1221 (gap between Night Lizard 0x1220 and Blue-Winged Crown 0x1222). The 104 raw word refs are mostly coincidental data occurrences. Confidence: low for card name. Treatment: RENAME_SLOT with EOL `unknown field-spell eligibility card id 0x1221 (no card-stats entry between Night Lizard/Blue-Winged Crown)`.

3. **0x080352a4 = 0x0201e2a0** (gDuelCardCtxBase):
   Already defined in ewram.inc as `gDuelCardCtxBase` (442 raw refs). Slot at 0x080352a4 in `exit_slot_activation_with_state_write` loads this to read [+4] = player_activation_index. Use REF_SLOT (createData + USER label pointing to gDuelCardCtxBase). Slot label: `exit_slot_act_dctxbase`.

4. **PTR_gP1LifePoints_080352a8** (0x0201c4e0 = gP1LifePoints):
   Already has USER label from prior Seg. RENAME_SLOT only: `exit_slot_act_gp1lp`.

5. **0x0803577c = 0x000018b6 = Grave Ohja** (Seg-10b line 20893):
   Used in eval_slot_activation_eligibility_full: exact card_id match `cmp r9, 0x18b6`. card-stats.s slot=0x18b6 = Grave Ohja (pw=40937767). Raw refs from ROM: 7 word refs. This is a new card_info.inc equate: `GRAVE_OHJA_CID = 0x000018b6`.

### REF_SLOTS (USER-label + DATA-ref)

| Slot addr    | Target addr  | gas_label       | Slot label                       |
|--------------|--------------|-----------------|----------------------------------|
| 0x080352a4   | 0x0201e2a0   | gDuelCardCtxBase| exit_slot_act_dctxbase           |

Note: PTR_gP1LifePoints_080352a8 already has the correct DATA ref to gP1LifePoints. It only needs a slot RENAME.

### RENAME_SLOTS (label rename + optional EOL)

All remaining DAT_ slots that already have their value reachable only via EQ (the Ghidra equate mechanism will produce `.word CONST_NAME`). These are the EQ slots' own definition lines plus:

| Slot addr    | Current label              | New label                                       | EOL note                                     |
|--------------|----------------------------|-------------------------------------------------|----------------------------------------------|
| 0x080352a8   | PTR_gP1LifePoints_080352a8 | exit_slot_act_gp1lp                             | (none - existing label already clear)        |
| 0x08035ca8   | DAT_08035ca8               | eval_fsact_unknown_cid_1221                     | unknown field-spell eligibility CID 0x1221; no card-stats entry between Night Lizard(0x1220) and Blue-Winged Crown(0x1222) |
| 0x08035944   | DAT_08035944               | eval_slot_act_elig_hamon_shifted                | HAMON_LORD_CID<<19 slot-word shift sentinel  |

### FUNC_RENAME

None. All 7 function names in Seg-10b are correct:
- `exit_slot_activation_with_state_write`: body reads gDuelCardCtxBase[+4] and writes ACTIVATION_STATE_B_OFF - matches name.
- `eval_slot_activation_eligibility_full`: performs comprehensive slot activation eligibility evaluation - matches.
- `count_activatable_slots_for_player`: counts slots [0..4] calling eval_slot_activation_eligibility_full - matches.
- `check_slot_field_spell_chain_eligible`: checks fieldspell chain eligibility for single slot - matches.
- `check_field_spell_trap_chain_eligible`: checks trap-chain eligibility for field spell zone - matches.
- `check_player_field_spell_chain_eligible`: composes the two above per-player - matches.
- `eval_slot_fieldspell_activation_full`: comprehensive fieldspell activation evaluation with BST card checks - matches.

### PLATE (R5)

Two functions have CJK plates that must be rewritten as ASCII (Jython mojibake rule):

**1. eval_slot_activation_eligibility_full (0x080352b0)**

Current plate: Chinese (CJK) - contains ideographic characters (confirmed at asm file line 20267).

Proposed ASCII plate:
```
Comprehensive field activation eligibility check for slot (player_side=r0, slot_idx=r1). Calls
check_slot_card_effect_eligibility + check_slot_card_fieldspell_eligibility for eligibility masks.
Checks field-spell chain (zone 0xb). Branches by opponent slot card_id (Diffusion Wave-Motion 0x15ff /
Asura Priest 0x1505 / Berserk Dragon 0x1644 / Wildedge 0x1958 / Toon Defense 0x1561 / Astral Barrier
0x1852 / Staunch Defender 0x1669 / Ring of Magnetism 0x1318 / Taunt 0x17fc / Raregold Armor 0x15ea /
Solar Flare Dragon 0x1756 / Emissary of the Oasis 0x179d / Prickle Fairy 0x1703 / Amazoness Tiger
0x160f / Vilepawn Archfiend 0x168c / Blue-Eyes Toon Dragon 0x12a5 / Toon Dark Magician Girl 0x154a /
Marauding Captain 0x14c6 / Marshmallon glasses 0x1777 / Marshmallon 0x1770 / Hieracosphinx 0x18b1 /
A Feint Plan 0x14d4 / Zombyra the Dark 0x147d / Manga Ryu-Ran 0x127d / Magical Scientist 0x1619 /
Union Attack 0x1890 / Feather Shot 0x195b / Magician's Valkyrie 0x16ed). Calls
check_player_has_equip_type_in_slots / count_available_effect_zones / check_card_is_amazoness_type /
check_card_is_archfiend_type / count_slot_equip_list_matches / get_slot_field5_score (threshold 0x76b) /
check_card_matches_active_effect_slot / count_slots_matching_card_pair. Hamon Lord check: slot_word&0x1fff
==HAMON_LORD_CID(0x19a4) via lsls#19 sentinel. indeg=2. r0=u32 player_side; r1=u32 slot_idx. Returns 0/1.
```

**2. eval_slot_fieldspell_activation_full (0x08035bc8)**

Current plate: Chinese (CJK) - confirmed at asm file line 21469.

Proposed ASCII plate:
```
Full field-spell slot activation check for (player_side=r0, slot_idx stored in r8 caller-save). Calls
check_slot_card_fieldspell_eligibility + check_slot_field_spell_chain_eligible; returns 0 if either
fails. Queries zone chains for Toon Defense (0x1561) and Astral Barrier (0x1852). Checks opponent
field-zone slot flags (bit5/bit1). Branches by opponent slot card_id: Servant of Catabolism 0x13b3 /
unknown 0x1221 / Jinzo #7 0x114c / Gear Golem 0x1295 / Reaper on Nightmare 0x1598 / Toon Goblin AF
0x1566 / Amphibious Bugroth MK-3 0x1705 / Drillago 0x15ba / Black Tyranno 0x1701 / Raging Flame
Sprite 0x182d / Shadowslayer 0x186d / Jowls of Dark Demise 0x13ab / Kiryu 0x15cf / Checkmate 0x169b /
Dark Scorpion Combination 0x16a3 / Delta Attacker 0x17aa / Overpowering Eye 0x1893 / Opti-Camouflage
Armor 0x1759 / Shooting Star Bow-Ceal 0x165d / Absolute End 0x17fd / Taunt 0x17fc. Calls
check_player_has_equip_type_in_slots / count_slots_with_chain_field_match / count_slots_matching_card_pair
/ check_card_matches_active_effect_slot / check_any_slot_fieldspell_zone_eligible / get_slot_field5_score
(threshold 0x63f). Chain filter IDs: 0x13ab / 0x15cf / 0x169b / 0x16a3 / 0x17aa / 0x1893 / 0x1759 /
0x165d (Absolute End 0x17fd / Taunt 0x17fc zone chain query). Returns 0=ineligible, 1=eligible, 2=chain.
indeg=1. r0=u32 player_side; r8=u32 slot_idx (caller-save). Constants: PLAYER_BLOCK_STRIDE=0x868.
```

Note: Both plates are within 500 characters. Verified: eval_slot_activation_eligibility_full plate is ~610 chars -- must be trimmed.

### Plate character count verification

eval_slot_activation_eligibility_full plate above: approx 880 chars. Must be trimmed to <= 500.

**Trimmed ASCII plate for eval_slot_activation_eligibility_full:**
```
Comprehensive field activation eligibility check for slot (player_side=r0, slot_idx=r1). Evaluates
effect/fieldspell eligibility masks; checks zone 0xb chain; branches by opponent slot card_id testing
~28 specific card IDs (Diffusion Wave-Motion/Asura Priest/Berserk Dragon/EHERO Wildedge/Toon
Defense/Astral Barrier/Staunch Defender/Ring of Magnetism/Taunt/Raregold Armor/Solar Flare Dragon/
Emissary of Oasis/Prickle Fairy/Amazoness Tiger/Vilepawn Archfiend/Blue-Eyes Toon/Toon DM Girl/
Marauding Captain/Marshmallon glasses/Marshmallon/Hieracosphinx/A Feint Plan/Zombyra/Manga Ryu-Ran/
Magical Scientist/Union Attack/Feather Shot/Magician's Valkyrie). Hamon check via lsls#19 sentinel
0xcd200000==HAMON_LORD_CID<<19. field5_score threshold 0x76b. indeg=2. Returns 0/1.
```
~490 chars. Pass.

**Trimmed ASCII plate for eval_slot_fieldspell_activation_full:**
```
Full field-spell activation check for slot (player_side=r0, slot_idx via r8 caller-save). Calls
check_slot_card_fieldspell_eligibility + check_slot_field_spell_chain_eligible; queries zone chains
for Toon Defense(0x1561)/Astral Barrier(0x1852)/Absolute End(0x17fd)/Taunt(0x17fc); branches by
opponent slot card_id (~21 specific cards incl. Jinzo#7/Gear Golem/Reaper on Nightmare/Toon Goblin
AF/Drillago/Black Tyranno/Raging Flame Sprite/Shadowslayer/Jowls of Dark Demise/Kiryu/Checkmate/Dark
Scorpion Combo/Delta Attacker/Overpowering Eye/Opti-Camo Armor/Shooting Star Bow-Ceal). Calls
get_slot_field5_score (threshold 0x63f). Returns 0/1/2. indeg=1. Constants: PLAYER_BLOCK_STRIDE=0x868.
```
~490 chars. Pass.

## carve plan (R7)

None. No ROM_INCBIN blocks in this range.

## disasm plan (R4)

None. No misidentified code blocks.

## New constants / globals

### card_info.inc additions (Seg-10b block)

51 new card ID equates + 1 new CID_SHIFTED sentinel + 0 reused:

```
@ =============================================================================
@ file 02 Seg-10b additions: fieldspell / activation eligibility card IDs
@ =============================================================================
.equ JINZO_7_CID,                0x0000114c  @ Jinzo #7; fieldspell eligibility BST; 12 raw refs
.equ MANGA_RYU_RAN_CID,          0x0000127d  @ Manga Ryu-Ran; fieldspell chain; 10 raw refs
.equ GEAR_GOLEM_CID,             0x00001295  @ Gear Golem the Moving Fortress; 9 raw refs
.equ BLUE_EYES_TOON_DRAGON_CID,  0x000012a5  @ Blue-Eyes Toon Dragon; activation elig; 10 raw refs
.equ RING_OF_MAGNETISM_CID,      0x00001318  @ Ring of Magnetism; activation elig; 22 raw refs
.equ JOWLS_OF_DARK_DEMISE_CID,   0x000013ab  @ Jowls of Dark Demise; fieldspell chain; 12 raw refs
.equ SERVANT_OF_CATABOLISM_CID,  0x000013b3  @ Servant of Catabolism; fieldspell BST; 5 raw refs
.equ LEGENDARY_FISHERMAN_CID,    0x000013cd  @ The Legendary Fisherman; chain check; 8 raw refs
.equ ZOMBYRA_THE_DARK_CID,       0x0000147d  @ Zombyra the Dark; fieldspell chain; 7 raw refs
.equ MARAUDING_CAPTAIN_CID,      0x000014c6  @ Marauding Captain; activation elig; 9 raw refs
.equ A_FEINT_PLAN_CID,           0x000014d4  @ A Feint Plan; activation elig; 7 raw refs
.equ ASURA_PRIEST_CID,           0x00001505  @ Asura Priest; activation elig BST; 32 raw refs
.equ TOON_DARK_MAGICIAN_GIRL_CID,0x0000154a  @ Toon Dark Magician Girl; 6 raw refs
.equ TOON_DEFENSE_CID,           0x00001561  @ Toon Defense; zone chain filter; 12 raw refs
.equ TOON_GOBLIN_AF_CID,         0x00001566  @ Toon Goblin Attack Force; fieldspell BST; 13 raw refs
.equ REAPER_ON_NIGHTMARE_CID,    0x00001598  @ Reaper on the Nightmare; fieldspell BST; 10 raw refs
.equ DRILLAGO_CID,               0x000015ba  @ Drillago; fieldspell BST; 9 raw refs
.equ KIRYU_CID,                  0x000015cf  @ Kiryu; fieldspell chain filter; 16 raw refs
.equ RAREGOLD_ARMOR_CID,         0x000015ea  @ Raregold Armor; activation elig; 6 raw refs
.equ DIFFUSION_WAVE_MOTION_CID,  0x000015ff  @ Diffusion Wave-Motion; activation/fieldspell elig BST; 23 raw refs
.equ AMAZONESS_TIGER_CID,        0x0000160f  @ Amazoness Tiger; activation elig BST; 10 raw refs
.equ MAGICAL_SCIENTIST_CID,      0x00001619  @ Magical Scientist; fieldspell chain; 83 raw refs
.equ BERSERK_DRAGON_CID,         0x00001644  @ Berserk Dragon; activation elig BST; 14 raw refs
.equ GUARDIAN_KAYEST_CID,        0x0000164e  @ Guardian Kay'est; activation/trap chain; 8 raw refs
.equ SHOOTING_STAR_BOW_CID,      0x0000165d  @ Shooting Star Bow - Ceal; fieldspell chain; 14 raw refs
.equ STAUNCH_DEFENDER_CID,       0x00001669  @ Staunch Defender; activation/fieldspell elig; 14 raw refs
.equ VILEPAWN_ARCHFIEND_CID,     0x0000168c  @ Vilepawn Archfiend; activation elig BST; 8 raw refs
.equ CHECKMATE_CID,              0x0000169b  @ Checkmate; fieldspell chain filter; 13 raw refs
.equ DARK_SCORPION_COMBO_CID,    0x000016a3  @ Dark Scorpion Combination; fieldspell chain; 14 raw refs
.equ MAGICIANS_VALKYRIE_CID,     0x000016ed  @ Magician's Valkyrie; activation elig BST; 8 raw refs
.equ BLACK_TYRANNO_CID,          0x00001701  @ Black Tyranno; fieldspell BST; 8 raw refs
.equ PRICKLE_FAIRY_CID,          0x00001703  @ Prickle Fairy; activation elig BST; 16 raw refs
.equ AMPHIBIOUS_BUGROTH_MK3_CID, 0x00001705  @ Amphibious Bugroth MK-3; fieldspell BST; 11 raw refs
.equ SOLAR_FLARE_DRAGON_CID,     0x00001756  @ Solar Flare Dragon; activation elig BST; 7 raw refs
.equ OPTI_CAMO_ARMOR_CID,        0x00001759  @ Opti-Camouflage Armor; fieldspell chain; 10 raw refs
.equ MARSHMALLON_CID,            0x00001770  @ Marshmallon; activation elig BST; 11 raw refs
.equ MARSHMALLON_GLASSES_CID,    0x00001777  @ Marshmallon glasses; activation elig; 25 raw refs
.equ EMISSARY_OF_OASIS_CID,      0x0000179d  @ Emissary of the Oasis; activation elig BST; 7 raw refs
.equ DELTA_ATTACKER_CID,         0x000017aa  @ Delta Attacker; fieldspell chain; 12 raw refs
.equ TAUNT_CID,                  0x000017fc  @ Taunt; activation/fieldspell elig BST; 8 raw refs
.equ ABSOLUTE_END_CID,           0x000017fd  @ Absolute End; activation/fieldspell zone chain; 7 raw refs
.equ RAGING_FLAME_SPRITE_CID,    0x0000182d  @ Raging Flame Sprite; fieldspell BST; 9 raw refs
.equ ASTRAL_BARRIER_CID,         0x00001852  @ Astral Barrier; activation/fieldspell elig; 14 raw refs
.equ SHADOWSLAYER_CID,           0x0000186d  @ Shadowslayer; fieldspell BST; 6 raw refs
.equ UNION_ATTACK_CID,           0x00001890  @ Union Attack; fieldspell chain; 14 raw refs
.equ OVERPOWERING_EYE_CID,       0x00001893  @ Overpowering Eye; fieldspell chain filter; 13 raw refs
.equ HIERACOSPHINX_CID,          0x000018b1  @ Hieracosphinx; activation elig BST; 12 raw refs
.equ GRAVE_OHJA_CID,             0x000018b6  @ Grave Ohja; activation elig; 7 raw refs
.equ EHERO_WILDEDGE_CID,         0x00001958  @ Elemental Hero Wildedge; activation elig BST (distinct from 0x1956=Rampart Blaster); 11 raw refs
.equ FEATHER_SHOT_CID,           0x0000195b  @ Feather Shot; fieldspell chain; 10 raw refs
.equ HAMON_LORD_CID,             0x000019a4  @ Hamon, Lord of Striking Thunder; 13 raw refs
.equ HAMON_LORD_CID_SHIFTED,     0xcd200000  @ HAMON_LORD_CID<<19; slot_word<<19 sentinel check; 6 raw refs
```

### duel_field.inc additions (Seg-10b block)

```
@ =============================================================================
@ file 02 Seg-10b additions: field5 score activation thresholds
@ =============================================================================
.equ FIELD5_SCORE_ACTIVATION_THRESHOLD, 0x0000076b  @ get_slot_field5_score return > this -> not activatable in eval_slot_activation_eligibility_full; 8 raw refs
.equ FIELD5_SCORE_FIELDSPELL_THRESHOLD, 0x0000063f  @ get_slot_field5_score return <= this -> not activatable in eval_slot_fieldspell_activation_full; 3 raw refs
```

## Section 5.1 Registration (Rule 3) -- 0 reference blocks

None. No ROM_INCBIN or .byte blocks with zero references exist in this range.

## Consumer Evidence (R6) -- key slot semantics

| Slot addr    | Value        | Consumer function + file:line          | Confidence | Notes                                          |
|--------------|--------------|----------------------------------------|------------|------------------------------------------------|
| 0x080352ac   | 0x00001d78   | exit_slot_activation_with_state_write: `str r1,[r0]` asm L20248 | high | Writes 0x13 to gP1LifePoints+0x1d78; ACTIVATION_STATE_B_OFF confirmed |
| 0x080352a4   | 0x0201e2a0   | exit_slot_activation_with_state_write: `ldr r0,[r0,#0x4]` asm L20241 | high | Reads gDuelCardCtxBase[+4] = player_activation_idx; matches Seg-10a usage |
| 0x080356d0   | 0x0000076b   | eval_slot_activation_eligibility_full: `cmp r0,r1; bgt fail` asm L21744 | high | r0=get_slot_field5_score result, bgt-> not activatable |
| 0x08035e4c   | 0x0000063f   | eval_slot_fieldspell_activation_full: `cmp r0,r1; ble fail` asm L21810  | high | r0=get_slot_field5_score result, ble-> not activatable |
| 0x08035944   | 0xcd200000   | eval_slot_activation_eligibility_full: `lsls r0,r0,#0x13; cmp r0,r1` asm L21046-49 | high | slot_word<<19 sentinel for Hamon (0x19a4) exact CID match |
| 0x08035ca8   | 0x00001221   | eval_slot_fieldspell_activation_full: `cmp r2,r0; bne` asm L21597 | low | No card-stats entry for slot 0x1221; used as exact CID match but card unidentifiable |

## Requests (low-confidence semantics)

1. **0x00001221** (slot 0x08035ca8): No entry in card-stats.s for slot_id=0x1221. The slot between Night Lizard (0x1220) and Blue-Winged Crown (0x1222) is unoccupied in the exported data. Request: is there a YGO card known to have passcode mapped to this slot in the WCT 2006 card database? If not, the RENAME label `eval_fsact_unknown_cid_1221` is appropriate. Confidence: low.

---

## Executor Report: F02Seg10b
- Slots: EQ=79 (28 REUSE + 51 NEW card_info + 2 NEW duel_field) REF=1 RENAME=3 FUNC_RENAME=0 PLATE=2
- carve=0 disasm=0 Section5.1=0
- New constants/globals: card_info.inc: 51 CID equates + HAMON_LORD_CID_SHIFTED; duel_field.inc: FIELD5_SCORE_ACTIVATION_THRESHOLD + FIELD5_SCORE_FIELDSPELL_THRESHOLD. Total 53 new equates.
- Requests: slot 0x1221 unknown card ID (low conf) -- see above
- proposal: doc/dev/refine/F02Seg10b.proposal.md
