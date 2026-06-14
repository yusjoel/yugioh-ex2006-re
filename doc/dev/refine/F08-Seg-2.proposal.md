# Refine Proposal: F08-Seg-2  [0x0806544c..0x08066448)

## 段测绘

- 函数入口: 20 个 (全部已命名)
  - 0x0806544c `write_equip_lp_delta_goblin_thief`
  - 0x08065458 `write_equip_lp_delta_dark_rabbit`
  - 0x08065468 `write_equip_lp_delta_granadora`
  - 0x08065484 `write_equip_lp_delta_saturn`
  - 0x080654b8 `write_equip_lp_delta_solar_ray`
  - 0x080654d8 `write_equip_lp_delta_marshmallon`
  - 0x080654e4 `write_equip_lp_delta_atomic_firefly`
  - 0x080654f8 `write_equip_lp_delta_greed`
  - 0x0806552e `write_equip_lp_delta_mecha_dog_marron`
  - 0x080655da `restore_equip_effect_frame`
  - 0x080655ec `submit_equip_lp_indicators_with_bar`
  - 0x08065698 `set_equip_partner_flags_with_bitmap_refresh`
  - 0x080656e0 `dispatch_equip_draw_counter_sprite_tick`
  - 0x08065990 `check_equip_activation_at_slot11`
  - 0x080659e8 `tick_dragon_summon_effect_display_state_machine`
  - 0x08065ce4 `check_slot_dark_magician_pair_placeable`
  - 0x080660d8 `drive_equip_slot_bitmap_or_activation_scan`
  - 0x080661fc `dispatch_equip_chain_state_by_slot_ownership`
  - 0x08066314 `enqueue_slot_player_side_sprite_attr`
  - 0x08066338 `enqueue_state2_sprites_on_equip_zone_count_match`

- 残留自动名槽: 70 DAT_/DWORD_ + 9 PTR_gP1LifePoints_* = 79 槽 总计
  - DAT_08065464=0xfffffe0c, DAT_08065480=0xfffff830, DAT_080654b4=0x868,
    DAT_080654e0=0x0201bb90, DAT_080654f4=0xfffffc18, DAT_08065554=0xfffffc18,
    DAT_08065584=0xfffffce0, DAT_080655e8=0x868,
    DAT_0806572c=0x1662, DAT_08065730=0x1403, DAT_08065734=0x11c2, DAT_08065738=0x1082,
    DAT_08065754=0x1353, DAT_0806575c=0x139f, DAT_0806577c=0x1563, DAT_08065784=0x1533,
    DAT_0806579c=0x15dc, DAT_080657a4=0x161a, DAT_080657d0=0x17d5, DAT_080657d8=0x16f7,
    DAT_080657ec=0x1748, DAT_080657f8=0x1776, DAT_08065818=0x1911, DAT_08065824=0x18f9,
    DAT_0806583c=0x1966, DAT_0806584c=0x19c7,
    PTR_gP1LifePoints_080654b0=0x0201c4e0 (x9: 080654b0/55e4/65868/65888/6593c/65b20/65c10/65c48/65cb8),
    DAT_0806586c=0x868, DAT_0806588c=0x868, DAT_08065940=0x868,
    DAT_080659d4=0x0201b290, DAT_080659d8=0x484, DAT_080659dc=0x183e,
    DAT_08065a18=0x12ca, DAT_08065a1c=0x16fd,
    DAT_08065a48=0x0201b290, DAT_08065a4c=0x08065a50,
    DAT_08065ae4=0x0201b290, DAT_08065ae8=0x4a4,
    DAT_08065b1c=0x0201e2a0, DAT_08065b54=0x0201b290, DAT_08065b58=0x4a4,
    DAT_08065b5c=0x1572, DAT_08065b60=0x12ca, DAT_08065b6c=0x153b,
    DAT_08065b84=0x1715, DAT_08065b98=0x1879, DAT_08065b9c=0x19ac,
    DAT_08065c4c=0x0201e2a0, DAT_08065c50=0x08065991, DAT_08065c60=0x08065991,
    DAT_08065cbc=0x1d70, DAT_08065cc0=0x165b, DAT_08065cc4=0x868,
    DAT_08065cc8=0x0201b290, DAT_08065ccc=0x4a4,
    DWORD_08065d64=0x868, DWORD_08065d68=0x0201c510, DWORD_08065d6c=0xfc9,
    DWORD_08066160=0x0201b290, DWORD_08066164=0x0201c510, DWORD_08066168=0x10ef,
    DWORD_0806616c=0x868, DWORD_080661dc=0x868, DWORD_080661e0=0x0201e1c8,
    DWORD_080661e4=0x0201c510, DWORD_08066228=0x0201b290, DWORD_0806622c=0x08066230,
    DWORD_08066334=0x8027, DWORD_08066440=0x868, DWORD_08066444=0x0201c510

- ROM_INCBIN / .byte 块: 3 块
  - 0x08065d78 size 0x3c (60B)
  - 0x08065e3c size 0x29c (668B)
  - 0x080662a4 size 0x68 (104B)

- switchD: switchD_08065a44 (jump table 0x65a50..0x65ac3, 29 entries) -- INLINE within
  tick_dragon_summon_effect_display_state_machine, no separate incbin

---

## 数据块分类 (Rule 2/3)

| 块 | ref-scan (raw / THUMB+1) | 判定 | 理由 |
|---|---|---|---|
| 0x65d78 sz=0x3c | raw=0 THUMB+1=1 (at 0x9e46328, handler table 0x09e4xxxx) | R4 disasm | CID=0x0fb6 (Time Wizard) fn_eligible handler; entry at 0x9e4631c: u32[0]=0x0805a205 (fn_activate+1) u32[2]=0x0fb6 (CID) u32[3]=0x08065d79 (fn_eligible+1); block is THUMB code: push {r4-r7,lr}, checks slot[+4].bit2, reads gDuelPhaseFlags[0x4a0] state code (0x94<<3), dispatches via table at 0x65db4 (34 entries, states 0x5f..0x80) with bx pc-dispatch; conf: high |
| 0x65e3c sz=0x29c | raw=12 entries (all from dispatch table at 0x65db4..0x65e38 inside asm) THUMB+1=2 (both coincidental: 0x08065f56 from 0x084d0329 FS compressed data; 0x080660a3 from 0x08da3c43 far ROM compressed area) | R4 disasm | 12 unique THUMB code entry points reachable via raw-pointer bx dispatch from table at 0x65db4; all referers (0x65db4..0x65e38) are .word table entries already in asm (within asm range, not block2 itself); block2 contains 12 sub-fn stubs (states 0x5f/0x60/0x61/0x62-default/0x63/0x64/0x6d/0x77/0x78/0x7e/0x7f/0x80); conf: high |
| 0x662a4 sz=0x68 | raw=6 (all from dispatch_equip_chain_state_by_slot_ownership jump table at 0x66230-0x662a0 within asm); THUMB+1=1 (0x080662ba from 0x08795327 FS compressed area, coincidental) | R4 disasm | 5 active case stubs dispatched via bx r0 from jump table at 0x66230; cases: state=0x80->0x662a4, 0x7e->0x662d2, 0x7d->0x662ea, 0x78->0x662fa, 0x64->0x66306; all refs are from function's own jump table; conf: high |

---

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS

All values ROM-verified (python struct.pack('<I') match confirmed, 0 failures).

#### Group A: LP delta equates (equip_lp_delta.inc)

| slot | value | const_name | slot_label | status |
|---|---|---|---|---|
| DAT_08065464 | 0xfffffe0c (-500) | LP_EQUIP_DELTA_NEG_500 | write_equip_lp_delta_goblin_thief_neg500 | reuse equip_lp_delta.inc |
| DAT_08065480 | 0xfffff830 (-2000) | LP_EQUIP_DELTA_NEG_2000 | write_equip_lp_delta_granadora_neg2000 | reuse equip_lp_delta.inc |
| DAT_080654f4 | 0xfffffc18 (-1000) | LP_EQUIP_DELTA_NEG_1000 | write_equip_lp_delta_atomic_firefly_neg1000 | NEW equip_lp_delta.inc |
| DAT_08065554 | 0xfffffc18 (-1000) | LP_EQUIP_DELTA_NEG_1000 | write_equip_lp_delta_mecha_dog_marron_neg1000 | reuse (same as above) |
| DAT_08065584 | 0xfffffce0 (-800) | LP_EQUIP_DELTA_NEG_800 | write_equip_lp_delta_twin_swords_neg800 | reuse equip_lp_delta.inc |

Evidence: write_equip_lp_delta_atomic_firefly plate (asm/08 L2601) "LP_DELTA = 0xfffffc18 = -1000", same for mecha_dog_marron. Value 0xfffffc18 not yet in equip_lp_delta.inc (grep confirms 0 hits). Conf: high.

#### Group B: PLAYER_STRIDE (gP1LifePoints stride 0x868)

10 duplicate slots all = 0x00000868. Already defined as PLAYER_BLOCK_STRIDE in multiple inc files.
Check: `grep PLAYER_BLOCK_STRIDE constants/*.inc` -> found in ewram.inc L250 (not duel_field.inc; confirmed by reviewer grep).

| slots | value | const_name | status |
|---|---|---|---|
| DAT_080654b4, DAT_080655e8, DAT_0806586c, DAT_0806588c, DAT_08065940, DAT_08065cc4, DWORD_08065d64, DWORD_0806616c, DWORD_080661dc, DWORD_08066440 | 0x00000868 | PLAYER_BLOCK_STRIDE | reuse ewram.inc (L250) |

Slot labels: `<func>_player_stride` per consumer function (e.g. `write_equip_lp_delta_saturn_stride`, etc.)

#### Group C: Global pointers (ewram.inc)

| slot | value | const_name | slot_label | status |
|---|---|---|---|---|
| DAT_080654e0 | 0x0201bb90 | gEquipChainSlotRefs | write_equip_lp_delta_marshmallon_ctx_ptr | reuse ewram.inc; reads [+0]=player_id via EQUIP_CTX_PLAYER_OFF=0 |
| DAT_080659d4, DAT_08065a48, DAT_08065ae4, DAT_08065b54, DAT_08065cc8, DWORD_08066160, DWORD_08066228 | 0x0201b290 | gDuelPhaseFlags | per-func label | reuse ewram.inc |
| DWORD_08065d68, DWORD_08066164, DWORD_080661e4, DWORD_08066444 | 0x0201c510 | gDuelFieldSlots | per-func label | reuse ewram.inc |
| DAT_08065b1c, DAT_08065c4c | 0x0201e2a0 | gDuelCardCtxBase | per-func label | reuse ewram.inc (442 raw refs confirmed) |
| DWORD_080661e0 | 0x0201e1c8 | gEquipZoneCountTable | drive_equip_slot_bitmap_equip_zone_table | reuse ewram.inc (55 ROM refs confirmed) |

Slot labels pattern: `<func>_<global_short>` (e.g. `check_equip_activation_at_slot11_phase_flags`)

#### Group D: gDuelPhaseFlags offsets (duel_field.inc / ewram.inc)

| slot | value | const_name | slot_label | status |
|---|---|---|---|---|
| DAT_080659d8 | 0x00000484 | EQUIP_ACTIVE_CTX_OFF | check_equip_activation_at_slot11_ctx_off | reuse duel_field.inc (46 ROM refs, conf: high) |
| DAT_08065ae8, DAT_08065b58, DAT_08065ccc | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | per-func label | NEW ewram.inc (241 ROM refs) |

New constant: `.equ EQUIP_PHASE_FRAME_OFF, 0x000004a4  @ [gDuelPhaseFlags+0x4a4] dragon-summon/equip effect frame display counter (adjacent to phase code node +0x4a0); 241 ROM refs; Seg-2 tick_dragon_summon_effect_display_state_machine`
Placement: ewram.inc after `SPRITE_ROW_QUEUE_STATE_OFF = 0x49c` block.
Evidence: asm/08 L3388 plate "gDuelFieldState[+0x4a4] frame count" + gDuelPhaseFlags=0x0201b290 (conf: high). Note: 0x4a0 (EQUIP_PHASE_CODE_OFF) is computed inline (0x94<<3) and not stored as literal in Seg-2, so only 0x4a4 needs a new constant here.

#### Group E: gP1LifePoints offsets

| slot | value | const_name | slot_label | status |
|---|---|---|---|---|
| DAT_08065cbc | 0x00001d70 | LP_BANISHER_CTX_OFF | tick_dragon_summon_display_ctr_off | reuse ewram.inc (39 ROM refs confirmed) |

#### Group F: Card IDs

All card IDs verified via data/card-stats.s by slot_id field lookup (python re scan).
All passcodes verified by card-stats.s record.

Reuse from card_info.inc (grep confirmed present by name and by value):
| value | const_name | card | card_info.inc line |
|---|---|---|---|
| 0x0fc9 | DARK_MAGICIAN_CID | Dark Magician | multiple |
| 0x1082 | MASKED_SORCERER_CID | Masked Sorcerer | L587 |
| 0x1353 | APPROPRIATE_CID | Appropriate | L621 |
| 0x1563 | TOON_MASKED_SORCERER_CID | Toon Masked Sorcerer | L595 |
| 0x15dc | HELPING_ROBO_FOR_COMBAT_CID | Helping Robo for Combat | confirmed |
| 0x163f | GRANADORA_CID | Granadora | confirmed |
| 0x161a | ROYAL_MAGICAL_LIBRARY_CID | Royal Magical Library | L808 |
| 0x165b | CONTRACT_WITH_EXODIA_CID | Contract with Exodia | confirmed |
| 0x1715 | ULTRA_EVOLUTION_PILL_CID | Ultra Evolution Pill | L962 |
| 0x1761 | GOBLIN_THIEF_CID | Goblin Thief | confirmed |
| 0x1767 | SOLAR_RAY_CID | Solar Ray | confirmed |
| 0x1770 | MARSHMALLON_CID | Marshmallon | L192 |
| 0x17d5 | DARK_MIMIC_LV1_CID | Dark Mimic LV1 | confirmed |
| 0x1776 | CORPSE_OF_YATA_GARASU_CID | Corpse of Yata-Garasu | L816 |
| 0x1802 | GREED_CID | Greed | L625 |
| 0x183e | SERIAL_SPELL_CID | Serial Spell | confirmed |
| 0x1869 | MECHA_DOG_MARRON_CID | Mecha-Dog Marron | confirmed |
| 0x1879 | KING_DRAGUN_CID | King Dragun | confirmed |
| 0x18f9 | EHERO_BUBBLEMAN_CID | Elemental Hero Bubbleman | L686 |
| 0x1911 | CYBER_ARCHFIEND_CID | Cyber Archfiend | L629 |
| 0x1966 | BROWW_HUNTSMAN_OF_DARK_WORLD_CID | Broww, Huntsman of Dark World | L469 |

Note: SATURN_AGENT (0x173f) and KOZAKY_SDB (0x18d7) have no DAT_ slots in Seg-2 (appear only as raw hex values in plate comment text); their existing card_info.inc names are AGENT_OF_JUDGMENT_SATURN_CID (L1098) and KOZAKYS_SELF_DESTRUCT_CID (L546) respectively. No EQ action needed for these two -- plate comments may reference values inline.

New (value-grep confirmed 0 hits in card_info.inc -- each of the 17 values below verified absent by `grep -iE '0x0*<hex>\b'`; see C5 double-check note below):
| value | proposed_name | card | card-stats record |
|---|---|---|---|
| 0x0fb6 | TIME_WIZARD_CID | Time Wizard | card_0016 slot=0x0fb6 |
| 0x10ef | DRAGON_CAPTURE_JAR_CID | Dragon Capture Jar | card_0291 slot=0x10ef |
| 0x1126 | DARK_RABBIT_CID | Dark Rabbit | card_0341 slot=0x1126 |
| 0x11c2 | SKELENGEL_CID | Skelengel | card_0450 slot=0x11c2 |
| 0x12ca | FLUTE_SUMMONING_DRAGON_CID | The Flute of Summoning Dragon | card_0651 slot=0x12ca |
| 0x139f | AIRKNIGHT_PARSHATH_CID | Airknight Parshath | card_0816 slot=0x139f |
| 0x1403 | CARD_OF_SAFE_RETURN_CID | Card of Safe Return | card_0878 slot=0x1403 |
| 0x1533 | DES_LACOODA_CID | Des Lacooda | card_1112 slot=0x1533 |
| 0x153b | CALL_OF_THE_MUMMY_CID | Call of the Mummy | card_1119 slot=0x153b |
| 0x1572 | HIDDEN_SOLDIER_CID | Hidden Soldier | card_1149 slot=0x1572 |
| 0x1662 | PRECIOUS_CARDS_FROM_BEYOND_CID | Precious Cards from Beyond | card_1338 slot=0x1662 |
| 0x16f7 | MOLTEN_ZOMBIE_CID | Molten Zombie | card_1456 slot=0x16f7 |
| 0x16fd | DON_TURTLE_CID | Don Turtle | card_1462 slot=0x16fd |
| 0x1748 | AVATAR_OF_THE_POT_CID | Avatar of The Pot | card_1523 slot=0x1748 |
| 0x174e | ATOMIC_FIREFLY_CID | Atomic Firefly | card_1529 slot=0x174e |
| 0x19ac | MAGNET_CIRCLE_LV2_CID | Magnet Circle LV2 | card_2021 slot=0x19ac |
| 0x19c7 | CHAINSAW_INSECT_CID | Chainsaw Insect | card_2042 slot=0x19c7 |

C5 value-grep double-check results (iter-2 fix, 2026-06-14): All 17 New values verified by `grep -iE '0x0*<hex>\b' constants/card_info.inc` -- 16 values returned 0 hits (clean). Exception: 0x1662 hit `CARD_STAT_LP_THRESHOLD_5730` (L85) -- benign same-value collision (LP threshold constant, not a CID); PRECIOUS_CARDS_FROM_BEYOND_CID is correctly New (distinct semantic domain). See fixer note below.
Correction history: iter-1 moved 8 from New->Reuse (MASKED_SORCERER/APPROPRIATE/TOON_MASKED_SORCERER/ROYAL_MAGICAL_LIBRARY/ULTRA_EVOLUTION_PILL/MARSHMALLON/GREED/CYBER_ARCHFIEND); BROWW_HUNTSMAN_OF_DARK_WORLD_CID moved to Reuse (L469); SATURN_AGENT/KOZAKY_SDB removed (no DAT_ slots). iter-2 moved 2 more from New->Reuse (CORPSE_OF_YATA_GARASU_CID L816; EHERO_BUBBLEMAN_CID L686); net New count: 27 - 8 (iter-1) - 2 (iter-2) = 17.
Reuse values also confirmed by value-grep: 0x1776 hits L816 CORPSE_OF_YATA_GARASU_CID; 0x18f9 hits L686 EHERO_BUBBLEMAN_CID -- both confirmed present.

#### Group G: OAM attribute / display constants (oam_attr.inc / new)

| slot | value | proposed_name | status |
|---|---|---|---|
| DWORD_08066334 | 0x00008027 | OAM_ATTR_P1_SPRITE | NEW oam_attr.inc |

Evidence: enqueue_slot_player_side_sprite_attr plate (asm/08 L4146-4157) "OAM_ATTR_P1=0x8027 (player 1 sprite attr; 0x8000=obj palette bank select bit)". Grep `oam_attr.inc` for 0x8027: 0 hits. Slot 0x27 is P0 (movs r0,#0x27 inline; no slot), 0x8027 has a slot. Conf: high.

---

### REF_SLOTS

| slot | target addr | gas_label | slot_label | evidence |
|---|---|---|---|---|
| PTR_gP1LifePoints_080654b0 | 0x0201c4e0 | gP1LifePoints | write_equip_lp_delta_saturn_lp_base | ewram.inc `gP1LifePoints = 0x0201C4E0` confirmed |
| PTR_gP1LifePoints_080655e4 | 0x0201c4e0 | gP1LifePoints | check_lp_side_for_twin_swords_lp_base | same |
| PTR_gP1LifePoints_08065868 | 0x0201c4e0 | gP1LifePoints | dispatch_draw_ctr_helping_robo_lp_base | same |
| PTR_gP1LifePoints_08065888 | 0x0201c4e0 | gP1LifePoints | dispatch_draw_ctr_royal_lib_lp_base | same |
| PTR_gP1LifePoints_0806593c | 0x0201c4e0 | gP1LifePoints | dispatch_draw_ctr_bubbleman_lp_base | same |
| PTR_gP1LifePoints_08065b20 | 0x0201c4e0 | gP1LifePoints | tick_dragon_summon_lp_bar_flag_base | same |
| PTR_gP1LifePoints_08065c10 | 0x0201c4e0 | gP1LifePoints | tick_dragon_summon_case7f_lp_base | same |
| PTR_gP1LifePoints_08065c48 | 0x0201c4e0 | gP1LifePoints | tick_dragon_summon_case7e_lp_base | same |
| PTR_gP1LifePoints_08065cb8 | 0x0201c4e0 | gP1LifePoints | tick_dragon_summon_case7d_lp_base | same |
| DAT_08065c50 | 0x08065991 (= check_equip_activation_at_slot11 + 1) | check_equip_activation_at_slot11+1 | tick_dragon_summon_case7e_act_cb | ROM verify: 0x08065990 hw=0xb570 (push {r4,r5,r6,lr}); THUMB ptr = fn+1 = 0x08065991; used as callback to select_equip_target_slot_by_card_id; conf: high |
| DAT_08065c60 | 0x08065991 | check_equip_activation_at_slot11+1 | tick_dragon_summon_case7e_act_cb2 | same; second copy used in init_zone_activation_display_fields call path |
| DAT_08065a4c | 0x08065a50 (switchD_08065a44__switchdataD_08065a50) | switchD_08065a44__switchdataD_08065a50 | tick_dragon_summon_state_table | asm label `switchD_08065a44__switchdataD_08065a50:` at 0x08065a50; .word 0x08065cd0 (first entry verified); conf: high |
| DWORD_0806622c | 0x08066230 (start of dispatch_equip_chain_state jump table) | dispatch_equip_chain_state_jump_table | dispatch_equip_chain_state_table_ptr | ROM verify: d[0x66230:0x66234]=0x08066306 (case 0x64 entry); table has 29 entries; no named label at 0x66230 yet -- fixer must add label `dispatch_equip_chain_state_jump_table:` at 0x66230 in asm then reference it; conf: high |

---

### RENAME_SLOTS (EOL)

Stale FUN_ in plate comments within Seg-2 (grep `FUN_08064880`, `FUN_080655da`, `FUN_080712a0` in seg2 range):

| occurrence | stale | replacement | location |
|---|---|---|---|
| 8x FUN_08064880 | FUN_08064880 | dispatch_equip_lp_delta_by_card_id | asm/08 L2484,2500,2558,2582,2596,2617,2650,2752 (plate comments) |
| 1x FUN_080655da | FUN_080655da | restore_equip_effect_frame | asm/08 L2752 (same plate) |
| 1x FUN_080712a0 | FUN_080712a0 | dispatch_equip_chain_state_if_tile_count_valid | asm/08 L4069 (dispatch_equip_chain_state_by_slot_ownership plate) |

No CJK chars detected in Seg-2 range (grep `[^\x00-\x7F]` = 0 hits). Plate text is fully ASCII.

---

### FUNC_RENAME

None identified. All 20 function names in Seg-2 match their function bodies. No misname signal detected.

Note: `write_equip_lp_delta_marshmallon` plate (L2586) uses "gEquipEffectCtx = 0x0201bb90" which is the established name `gEquipChainSlotRefs`. The plate text should be corrected (replace "gEquipEffectCtx" with "gEquipChainSlotRefs") as part of plate fix. This is a plate-text correction, not a FUNC_RENAME.

---

### PLATE (R5)

Plate corrections needed (substring replacements, all ASCII):

1. All plates containing `FUN_08064880`: replace with `dispatch_equip_lp_delta_by_card_id` (8 plates: write_equip_lp_delta_dark_rabbit, granadora, solar_ray, marshmallon, atomic_firefly, greed, mecha_dog_marron + restore_equip_effect_frame)
2. `FUN_080655da` -> `restore_equip_effect_frame` (1 plate in restore_equip_effect_frame itself)
3. `FUN_080712a0` -> `dispatch_equip_chain_state_if_tile_count_valid` (1 plate in dispatch_equip_chain_state_by_slot_ownership)
4. `gEquipEffectCtx` -> `gEquipChainSlotRefs` in write_equip_lp_delta_marshmallon plate (1 plate; L2586)

Total plate fixes: 11 substring replacements across 10 plate comments.

---

## carve 计划 (R7)

None. No OAM data tables or structured ROM data blocks found in Seg-2.
All 3 ROM_INCBIN blocks are THUMB code (R4 disasm).

---

## disasm 计划 (R4)

### Block 1: 0x08065d78 / 0x3c (60B)

- CID: 0x0fb6 (Time Wizard, card_0016 in card-stats.s, slot=0x0fb6)
- Handler table entry at 0x09e4631c: u32[0]=0x0805a205 (fn_activate+1), u32[2]=0x0fb6 (CID), u32[3]=0x08065d79 (fn_eligible+1)
- Entry: fn_eligible+1 stored at 0x09e46328; entry base at 0x09e4631c = fn_ptr - 0xc
- Proposed label: `check_equip_eligible_state_dispatch_for_time_wizard`
- Function semantics: checks slot[+4].bit2 (block flag); if set returns 0; reads gDuelPhaseFlags[0x4a0] state code (movs #0x94; lsls #3 = 0x4a0); subtracts 0x5f; checks <= 0x21 (states 0x5f..0x80 = 34 values); dispatches via 34-entry raw-address jump table at 0x08065db4; note: literal pools at 0x65da8 (0xfffffd00 = -768, unknown use), 0x65dac (gDuelPhaseFlags=0x0201b290), 0x65db0 (0x08065db4 = table base)
- R4 disasm procedure: clearListing 0x08065d78 len=0x3c, setTMode THUMB, DisassembleCommand 0x08065d78
- Literal pool at end (0x08065da8..0x65db3): createDWord at 0x65da8, 0x65dac, 0x65db0 to force split

### Block 2: 0x08065e3c / 0x29c (668B)

- Dispatch table at 0x08065db4..0x08065e3b (34 entries, already in asm as .word lines) points to 12 unique sub-fn entry points within this block
- 12 entry points and their state assignments:

| state | entry addr | first hw | notes |
|---|---|---|---|
| 0x80 | 0x08065e3c | 0x4809 | state 0x80: dispatch starting sub-fn |
| 0x7f | 0x08065e76 | 0x78a9 | state 0x7f |
| 0x7e | 0x08065e98 | 0x4815 | state 0x7e |
| 0x78 | 0x08065f58 | 0x4808 | state 0x78 |
| 0x77 | 0x08065fb8 | 0x480f | state 0x77 |
| 0x6d | 0x08066004 | 0xf030 | state 0x6d |
| 0x64 | 0x08066038 | 0x78a9 | state 0x64 |
| 0x63 | 0x0806604c | 0x78ad | state 0x63 |
| 0x61 | 0x08066066 | 0x78aa | state 0x61 |
| 0x60 | 0x0806608c | 0x78ad | state 0x60 |
| 0x5f | 0x080660a4 | 0x78ab | state 0x5f |
| default (0x62+) | 0x080660c8 | 0x2000 (movs r0,#0) | default return 0 |

- All entry points reached via raw-address bx dispatch (not THUMB+1); the two coincidental THUMB refs (0x08065f56 from FS data at 0x084d0329; 0x080660a3 from compressed area at 0x08da3c43) are not real fn-ptrs
- Proposed stub naming: `equip_state_stub_<hex_state>_time_wizard` per entry (e.g. `equip_state_stub_80_time_wizard` at 0x08065e3c, etc.)
- R4 disasm procedure: clearListing 0x08065e3c len=0x29c, setTMode THUMB; DisassembleCommand each entry point individually (12 calls); literal pools within each sub-fn: createDWord at each literal pool address

### Block 3: 0x080662a4 / 0x68 (104B)

- 5 case stubs for dispatch_equip_chain_state_by_slot_ownership (jump table at 0x08066230)
- Entry points:

| state | entry addr | first hw |
|---|---|---|
| 0x80 | 0x080662a4 | 0x8814 (ldrh r4,[r0]) |
| 0x7e | 0x080662d2 | 0x8814 |
| 0x7d | 0x080662ea | 0xf02d |
| 0x78 | 0x080662fa | 0x2001 |
| 0x64 | 0x08066306 | 0x1c28 |

- All refs from dispatch_equip_chain_state_by_slot_ownership's own jump table (0x66230); coincidental THUMB ref (0x080662ba from FS data at 0x08795327) is not a real fn-ptr
- Proposed stub naming: `equip_chain_state_stub_<hex_state>` (e.g. `equip_chain_state_stub_80` at 0x080662a4, etc.)
- R4 disasm procedure: clearListing 0x080662a4 len=0x68, setTMode THUMB; DisassembleCommand each of 5 entry points; note: block ends at 0x0806630b (next fn `LAB_0806630c` at 0x0806630c is already in asm)

### switchD_08065a44

Fully inline within tick_dragon_summon_effect_display_state_machine. Jump table at 0x08065a50 (labeled `switchD_08065a44__switchdataD_08065a50`) already structured in asm. All 6 unique targets (0x65ac4, 0x65aec, 0x65c1e, 0x65c64, 0x65cd0, 0x65cd4) are inline case labels within the parent function. No disasm action needed.

---

## 新增 constants / 全局

### equip_lp_delta.inc (新建 1 equate)
```
.equ LP_EQUIP_DELTA_NEG_1000, 0xfffffc18  @ -1000 (s32); Marshmallon/Atomic Firefly/Mecha-Dog Marron LP penalty; 3 Seg-2 slots
```
Verification: grep `equip_lp_delta.inc` for 0xfffffc18 = 0 hits confirmed; -1000 = 0xfffffc18 two's complement verified.

### ewram.inc (新建 1 offset)
```
.equ EQUIP_PHASE_FRAME_OFF, 0x000004a4  @ [gDuelPhaseFlags+0x4a4] dragon-summon/equip effect phase frame counter; adjacent to phase code node +0x4a0 (= 0x94<<3); 241 ROM refs; Seg-2 tick_dragon_summon_effect_display_state_machine
```
Place after `SPRITE_ROW_QUEUE_STATE_OFF = 0x49c` in ewram.inc gDuelPhaseFlags block.
Verification: grep for 0x000004a4 in constants/*.inc = 0 hits (except ewram which will contain it); 241 ROM raw refs verified.

### oam_attr.inc (新建 1 equate)
```
.equ OAM_ATTR_P1_SPRITE,  0x00008027  @ player 1 side sprite attr (0x8000=OBJ palette select; 0x27=tile region); enqueue_slot_player_side_sprite_attr; 1 Seg-2 slot
```
Verification: grep `oam_attr.inc` for 0x8027 = 0 hits confirmed.

### card_info.inc (新建 17 CID, per C5 双向核订正后)

New CIDs confirmed by: (1) grep card_info.inc by name = 0 hits; (2) grep card_info.inc by value `grep -iE '0x0*<hex>\b'` = 0 hits (16 clean; 0x1662 has benign LP-threshold collision -- see note); (3) card-stats.s slot_id verified; (4) plate comments in asm/08.
Derivation: original proposal 27 New - 8 moved to Reuse (iter-1 fix) - 2 moved to Reuse (iter-2 fix: CORPSE_OF_YATA_GARASU_CID + EHERO_BUBBLEMAN_CID) = 17 New.

Full list (17): TIME_WIZARD_CID (0x0fb6), DRAGON_CAPTURE_JAR_CID (0x10ef), DARK_RABBIT_CID (0x1126), SKELENGEL_CID (0x11c2), FLUTE_SUMMONING_DRAGON_CID (0x12ca), AIRKNIGHT_PARSHATH_CID (0x139f), CARD_OF_SAFE_RETURN_CID (0x1403), DES_LACOODA_CID (0x1533), CALL_OF_THE_MUMMY_CID (0x153b), HIDDEN_SOLDIER_CID (0x1572), PRECIOUS_CARDS_FROM_BEYOND_CID (0x1662), MOLTEN_ZOMBIE_CID (0x16f7), DON_TURTLE_CID (0x16fd), AVATAR_OF_THE_POT_CID (0x1748), ATOMIC_FIREFLY_CID (0x174e), MAGNET_CIRCLE_LV2_CID (0x19ac), CHAINSAW_INSECT_CID (0x19c7)

Reuse (21 entries, all confirmed present by name grep AND value grep): DARK_MAGICIAN_CID (0x0fc9), MASKED_SORCERER_CID (0x1082, L587), APPROPRIATE_CID (0x1353, L621), TOON_MASKED_SORCERER_CID (0x1563, L595), HELPING_ROBO_FOR_COMBAT_CID (0x15dc), GRANADORA_CID (0x163f), ROYAL_MAGICAL_LIBRARY_CID (0x161a, L808), CONTRACT_WITH_EXODIA_CID (0x165b), ULTRA_EVOLUTION_PILL_CID (0x1715, L962), GOBLIN_THIEF_CID (0x1761), SOLAR_RAY_CID (0x1767), MARSHMALLON_CID (0x1770, L192), DARK_MIMIC_LV1_CID (0x17d5), CORPSE_OF_YATA_GARASU_CID (0x1776, L816), GREED_CID (0x1802, L625), SERIAL_SPELL_CID (0x183e), MECHA_DOG_MARRON_CID (0x1869), KING_DRAGUN_CID (0x1879), EHERO_BUBBLEMAN_CID (0x18f9, L686), CYBER_ARCHFIEND_CID (0x1911, L629), BROWW_HUNTSMAN_OF_DARK_WORLD_CID (0x1966, L469)

Fixer note (non-blocking): PRECIOUS_CARDS_FROM_BEYOND_CID (0x1662) and CARD_STAT_LP_THRESHOLD_5730 (0x1662, L85) are same-value constants with distinct semantic domains (card ID vs LP threshold). GAS allows multiple equates to same value. Fixer must add PRECIOUS_CARDS_FROM_BEYOND_CID as an independent new line in card_info.inc; must NOT replace or remove CARD_STAT_LP_THRESHOLD_5730. Precedent: SANGA/0x1119 criti.

No-slot plate-only references (no EQ action): AGENT_OF_JUDGMENT_SATURN_CID (0x173f, L1098 in card_info.inc; plate text only, no DAT_ slot in Seg-2), KOZAKYS_SELF_DESTRUCT_CID (0x18d7, L546 in card_info.inc; plate text only, no DAT_ slot in Seg-2)

---

## §5.1 登记 (Rule 3)

None. All 3 ROM_INCBIN blocks have confirmed ROM references (handler table or jump table within function). No zero-reference blocks in Seg-2.

---

## 消费者证据 (R6)

| 槽/全局 | file:line | 语义 | 置信度 |
|---|---|---|---|
| 0xfffffc18 (-1000) | asm/08 L2601-2602 write_equip_lp_delta_atomic_firefly plate "LP_DELTA = 0xfffffc18 = -1000 (fixed LP penalty)" | LP penalty equate | high |
| 0xfffffe0c (-500) | asm/08 L2473-2474 write_equip_lp_delta_goblin_thief plate "LP_DELTA_STEAL = 0xfffffe0c = -500 (opponent penalty)" | LP penalty (reuse) | high |
| gDuelPhaseFlags+0x4a4 | asm/08 L3388-3389 tick_dragon_summon plate "+0x4a4 frame count; str r1,[r0,#0x0] clears frame field" | display frame counter | high |
| gEquipChainSlotRefs[0] | asm/08 L2586 write_equip_lp_delta_marshmallon "[+0x0] = current_player_id"; ewram.inc L448 EQUIP_CTX_PLAYER_OFF=0 | player id field via EQUIP_CTX_PLAYER_OFF | high |
| EQUIP_ACTIVE_CTX_OFF (0x484) | duel_field.inc L360 "46 ROM refs; ACTIVATION_OFFSET=0x484"; asm/08 L3339 check_equip_activation_at_slot11 uses DAT_080659d8=0x484 to index gDuelPhaseFlags | equip ctx slot ptr | high |
| Block1 handler (Time Wizard) | handler table 0x09e4631c: u32[2]=0x0fb6, u32[3]=0x08065d79; card-stats.s card_0016 slot=0x0fb6 name="Time Wizard" | fn_eligible for Time Wizard CID | high |
| 0x08065991 (THUMB callback) | asm/08 L3683 `bl select_equip_target_slot_by_card_id` with DAT_08065c50=0x08065991; fn at 0x08065990 confirmed = check_equip_activation_at_slot11 (push opcode 0xb570 at 0x65990) | THUMB fn ptr to check_equip_activation_at_slot11 | high |

---

## 求助

None. All semantics resolved with evidence. Low-confidence items:

- The 34 entry point names for Block2 sub-fns (`equip_state_stub_XX_time_wizard`) are structural labels; actual semantic names cannot be determined without full R4 disasm of each stub (blocked until disasm). Fixer should apply structural `equip_state_stub_<hex>_time_wizard` labels and leave semantic plate comments as TODO for post-disasm.
- Block3 stub names similarly structural (`equip_chain_state_stub_XX`).
- `0xfffffd00 (-768)` literal pool value at 0x08065da8 inside Block1: usage context unclear from static decode alone. Fixer should note as unnamed literal in the disasm.
