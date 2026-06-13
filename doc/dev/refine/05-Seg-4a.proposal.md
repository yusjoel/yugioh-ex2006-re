# Refine Proposal: 05-Seg-4a  [0x0804b4f4..0x0804be38)

## 段测绘

- 函数入口: 10 个
  - 0x0804b4f4  get_card_field_summon_restriction
  - 0x0804b81c  get_card_special_group_code
  - 0x0804ba58  check_card_has_equip_placement_type
  - 0x0804ba90  check_card_not_equip_placement_type
  - 0x0804bab8  check_card_id_is_special_tribute_group
  - 0x0804bb6c  check_card_is_equip_target_eligible
  - 0x0804bc58  check_card_id_is_equip_excluded_range
  - 0x0804bc90  get_card_equip_zone_rank
  - 0x0804bd78  check_card_id_is_equip_set_a
  - 0x0804be38  get_card_effect_category  (Seg-4b 起点, 不含)

- 残留自动名槽: 101 个 DAT_ 槽 (全部为函数内嵌 literal pool .word, 均已 ROM 字节验证)
  - L5123: DAT_0804b53c = 0x000014c9
  - L5125: DAT_0804b540 = 0x00001227
  - L5127: DAT_0804b544 = 0x00001051
  - L5132: DAT_0804b54c = 0x0000100c
  - L5144: DAT_0804b560 = 0x000010b0
  - L5154: DAT_0804b570 = 0x00001152
  - L5173: DAT_0804b590 = 0x000011d8
  - L5183: DAT_0804b5a0 = 0x000011c3
  - L5200: DAT_0804b5bc = 0x000011f5
  - L5236: DAT_0804b5f8 = 0x000013ad
  - L5246: DAT_0804b608 = 0x000012a1
  - L5265: DAT_0804b628 = 0x0000136a
  - L5270: DAT_0804b630 = 0x000013ab
  - L5291: DAT_0804b654 = 0x00001413
  - L5296: DAT_0804b65c = 0x000013bd
  - L5313: DAT_0804b678 = 0x00001481
  - L5323: DAT_0804b688 = 0x00001489
  - L5363: DAT_0804b6cc = 0x0000161f
  - L5368: DAT_0804b6d4 = 0x000014fb
  - L5387: DAT_0804b6f4 = 0x00001527
  - L5392: DAT_0804b6fc = 0x00001530
  - L5411: DAT_0804b71c = 0x00001595
  - L5421: DAT_0804b72c = 0x00001590
  - L5432: DAT_0804b740 = 0x00001613
  - L5441: DAT_0804b750 = 0x00001618
  - L5462: DAT_0804b778 = 0x0000179a
  - L5473: DAT_0804b78c = 0x00001689
  - L5486: DAT_0804b7a4 = 0x000016c2
  - L5495: DAT_0804b7b4 = 0x0000178e
  - L5510: DAT_0804b7d0 = 0x000017ee
  - L5519: DAT_0804b7e0 = 0x000017ea
  - L5535: DAT_0804b7fc = 0x000018b5
  - L5548: DAT_0804b810 = 0x000018c2
  - L5598: DAT_0804b85c = 0x00001758
  - L5600: DAT_0804b860 = 0x00001466
  - L5602: DAT_0804b864 = 0x0000112e
  - L5604: DAT_0804b868 = 0x00000fe5
  - L5616: DAT_0804b87c = 0x00001117
  - L5618: DAT_0804b880 = 0x00000fe9
  - L5623: DAT_0804b888 = 0x0000111c
  - L5646: DAT_0804b8ac = 0x0000128c
  - L5658: DAT_0804b8c0 = 0x0000138a
  - L5663: DAT_0804b8c8 = 0x000013e9
  - L5684: DAT_0804b8ec = 0x00001578
  - L5696: DAT_0804b900 = 0x00001534
  - L5701: DAT_0804b908 = 0x0000154a
  - L5725: DAT_0804b930 = 0x000016c9
  - L5741: DAT_0804b948 = 0x000016cb
  - L5768: DAT_0804b978 = 0x000018b9
  - L5779: DAT_0804b98c = 0x000017c9
  - L5784: DAT_0804b994 = 0x000017d4
  - L5801: DAT_0804b9b4 = 0x00001895
  - L5806: DAT_0804b9bc = 0x0000186b
  - L5815: DAT_0804b9cc = 0x000018a4
  - L5837: DAT_0804b9f4 = 0x000019a6
  - L5846: DAT_0804ba04 = 0x00001982
  - L5863: DAT_0804ba24 = 0x000019ca
  - L5877: DAT_0804ba3c = 0x000019cd
  - L5942: DAT_0804baa0 = 0x000017c4
  - L5984: DAT_0804bae0 = 0x000018f6
  - L5986: DAT_0804bae4 = 0x000015b4
  - L5988: DAT_0804bae8 = 0x00001488
  - L5990: DAT_0804baec = 0x00001299
  - L5995: DAT_0804baf4 = 0x000015b1
  - L6006: DAT_0804bb08 = 0x0000164c
  - L6014: DAT_0804bb14 = 0x00001806
  - L6031: DAT_0804bb34 = 0x0000196e
  - L6050: DAT_0804bb54 = 0x000019aa
  - L6090: DAT_0804bb9c = 0x00001729
  - L6092: DAT_0804bba0 = 0x000015fc
  - L6101: DAT_0804bbb0 = 0x000016ec
  - L6116: DAT_0804bbcc = 0x000018ac
  - L6118: DAT_0804bbd0 = 0x00001771
  - L6123: DAT_0804bbd8 = 0x000018c9
  - L6142: DAT_0804bbfc = 0x00001987
  - L6153: DAT_0804bc10 = 0x00001956
  - L6171: DAT_0804bc30 = 0x000019ce
  - L6188: DAT_0804bc4c = 0x000019ef
  - L6218: DAT_0804bc74 = 0x000015fa
  - L6230: DAT_0804bc88 = 0x00001954
  - L6277: DAT_0804bcdc = 0x000015fc
  - L6279: DAT_0804bce0 = 0x0000148c
  - L6281: DAT_0804bce4 = 0x0000111b
  - L6286: DAT_0804bcec = 0x000013a7
  - L6297: DAT_0804bd00 = 0x000014c7
  - L6306: DAT_0804bd10 = 0x0000158a
  - L6321: DAT_0804bd2c = 0x000017c6
  - L6323: DAT_0804bd30 = 0x000016b9
  - L6332: DAT_0804bd40 = 0x00001774
  - L6346: DAT_0804bd58 = 0x0000183a
  - L6358: DAT_0804bd6c = 0x00001906
  - L6387: DAT_0804bd9c = 0x0000149d
  - L6389: DAT_0804bda0 = 0x0000123b
  - L6391: DAT_0804bda4 = 0x00000ff9
  - L6400: DAT_0804bdb4 = 0x00001009
  - L6411: DAT_0804bdc8 = 0x0000130d
  - L6420: DAT_0804bdd8 = 0x0000131a
  - L6435: DAT_0804bdf4 = 0x0000169c
  - L6437: DAT_0804bdf8 = 0x0000159c
  - L6458: DAT_0804be1c = 0x00001810
  - L6470: DAT_0804be30 = 0x0000187c

- ROM_INCBIN / .byte 块: 0 (段内无独立数据块; 全为函数内嵌 literal pool)
  - .zero 0x2 均为 THUMB literal pool 2 字节对齐填充, 不是独立数据块

## 数据块分类 (Rule 2/3) -- 每块给 ref-scan 证据

无独立 ROM_INCBIN / .byte 数据块。段内 101 个 .word 均为 THUMB literal pool 嵌入条目 (ldr rN, DAT_* 直接引用)，
全部值域 [0x0fe5..0x19ef] = card_id 范围 (无 ROM 地址、无 fn-ptr)。

ref-scan 结论 (python struct.pack 验证):
- 所有 101 个 .word 值均 < 0x2000, 无 ROM 地址形式 (>= 0x08000000) -> 无 fn-ptr 槽
- 段内无 ROM_INCBIN -> 无需 carve / disasm

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate)

注: 所有 101 DAT_ 槽均为 card_id 字面量. 按以下三类处理:

**A类: 复用 card_info.inc 已有常量 (32 槽)**

| 槽地址 | 值 | 现有常量名 | 卡名 |
|--------|----|-----------|----|
| 0x0804b5f8 | 0x000013ad | SLATE_WARRIOR_CID | Slate Warrior pw=78636495 |
| 0x0804b608 | 0x000012a1 | PARASITE_PARACIDE_CID | Parasite Paracide pw=27911549 |
| 0x0804b630 | 0x000013ab | JOWLS_OF_DARK_DEMISE_CID | Jowls of Dark Demise pw=05257687 |
| 0x0804b6d4 | 0x000014fb | FIBER_JAR_CID | Fiber Jar pw=78706415 |
| 0x0804b6f4 | 0x00001527 | ROYAL_KEEPER_CID | Royal Keeper pw=16509093 |
| 0x0804b71c | 0x00001595 | COBRA_JAR_CID | Cobra Jar pw=86801871 |
| 0x0804b778 | 0x0000179a | NIGHT_ASSAILANT_CID | Night Assailant pw=16226786 |
| 0x0804b7d0 | 0x000017ee | OJAMA_KING_CARD_ID | Ojama King pw=90140980 |
| 0x0804b7fc | 0x000018b5 | DUMMY_GOLEM_CID | Dummy Golem pw=13532663 -- NEW (B class) |
| 0x0804b810 | 0x000018c2 | CHARMER_RANGE_MAX_CID | Wynn the Wind Charmer pw=37744402 (range sentinel) |
| 0x0804b860 | 0x00001466 | DARK_NECROFEAR_CID | Dark Necrofear pw=31829185 |
| 0x0804b888 | 0x0000111c | GATE_GUARDIAN_CID | Gate Guardian pw=25833572 |
| 0x0804b8c8 | 0x000013e9 | upd_cid_13e9 | gap slot; no card-stats entry |
| 0x0804b8ec | 0x00001578 | LAVA_GOLEM_CID | Lava Golem pw=00102380 |
| 0x0804b908 | 0x0000154a | TOON_DARK_MAGICIAN_GIRL_CID | Toon Dark Magician Girl pw=90960358 |
| 0x0804b98c | 0x000017c9 | THEINEN_THE_GREAT_SPHINX_CID | Theinen the Great Sphinx pw=87997872 |
| 0x0804b994 | 0x000017d4 | HORUS_LV8_CID | Horus the Black Flame Dragon LV8 pw=48229808 |
| 0x0804b9bc | 0x0000186b | GEARFRIED_SWORDMASTER_CID | Gearfried the Swordmaster pw=57046845 |
| 0x0804b9f4 | 0x000019a6 | EHERO_NEO_BUBBLEMAN_CID | Elemental Hero Neo Bubbleman pw=05285665 |
| 0x0804ba24 | 0x000019ca | DOOM_DOZER_CID | Doom Dozer pw=76039636 |
| 0x0804bae4 | 0x000015b4 | XYZ_DRAGON_CANNON_CID | XYZ-Dragon Cannon pw=91998119 |
| 0x0804bba0 | 0x000015fc | DARK_PALADIN_CID | Dark Paladin pw=98502113 |
| 0x0804bbb0 | 0x000016ec | VICTORY_D_CID | Victory D. pw=44910027 |
| 0x0804bc10 | 0x00001956 | EHERO_RAMPART_BLASTER_CARD_ID | Elemental Hero Rampart Blaster pw=47737087 |
| 0x0804bc4c | 0x000019ef | EHERO_ERIKSHIELER_CID | Elemental Hero Erikshieler pw=29343734 |
| 0x0804bc74 | 0x000015fa | YZ_TANK_DRAGON_CID | YZ-Tank Dragon pw=25119460 |
| 0x0804bcdc | 0x000015fc | DARK_PALADIN_CID | Dark Paladin pw=98502113 (2nd occurrence, same equate reused) |
| 0x0804bd30 | 0x000016b9 | STRIKE_NINJA_CID | Strike Ninja pw=41006930 |
| 0x0804bd6c | 0x00001906 | WINGED_KURIBOH_LV10_CID | Winged Kuriboh LV10 pw=98585345 |
| 0x0804bda0 | 0x0000123b | CRUSH_CARD_CID | Crush Card pw=57728570 |
| 0x0804bda4 | 0x00000ff9 | CASTLE_OF_DARK_ILLUSIONS_CID | Castle of Dark Illusions pw=00062121 |
| 0x0804bdb4 | 0x00001009 | PUMPKING_CID | Pumpking the King of Ghosts pw=29155212 |

A 类共 32 槽 (31 个独立 card_info.inc 已建常量 + upd_cid_13e9 gap 复用; 0x15fc 两槽同映射 DARK_PALADIN_CID).

**B类: 新建 CID 常量 (63 槽, 全部新增到 card_info.inc)**

| 槽地址 | 值 | 拟建常量名 | 卡名 | pw |
|--------|----|-----------|----|-----|
| 0x0804b868 | 0x00000fe5 | HARPIE_LADY_SISTERS_CID | Harpie Lady Sisters | 12206212 |
| 0x0804b880 | 0x00000fe9 | PERFECTLY_ULTIMATE_GREAT_MOTH_CID | Perfectly Ultimate Great Moth | 48579379 |
| 0x0804b54c | 0x0000100c | MASK_OF_DARKNESS_CID | Mask of Darkness | 28933734 |
| 0x0804b560 | 0x000010b0 | PRINCESS_OF_TSURUGI_CID | Princess of Tsurugi | 51371017 |
| 0x0804b87c | 0x00001117 | WALL_SHADOW_CID | Wall Shadow | 63162310 |
| 0x0804bce4 | 0x0000111b | SUIJIN_CID | Suijin | 98434877 |
| 0x0804b864 | 0x0000112e | METALZOA_CID | Metalzoa | 50705071 |
| 0x0804b570 | 0x00001152 | MAGICIAN_OF_FAITH_CID | Magician of Faith | 31560081 |
| 0x0804b5a0 | 0x000011c3 | HANE_HANE_CID | Hane-Hane | 07089711 |
| 0x0804b590 | 0x000011d8 | NEEDLE_WORM_CID | Needle Worm | 81843628 |
| 0x0804b5bc | 0x000011f5 | MORPHING_JAR_CID | Morphing Jar | 33508719 |
| 0x0804b540 | 0x00001227 | INVADER_OF_THE_THRONE_CID | Invader of the Throne | 03056267 |
| 0x0804b8ac | 0x0000128c | RED_EYES_BLACK_METAL_DRAGON_CID | Red-Eyes Black Metal Dragon | 64335804 |
| 0x0804baec | 0x00001299 | THE_FIEND_MEGACYBER_CID | The Fiend Megacyber | 66362965 |
| 0x0804bdc8 | 0x0000130d | GERM_INFECTION_CID | Germ Infection | 24668830 |
| 0x0804bdd8 | 0x0000131a | STIM_PACK_CID | Stim-Pack | 83225447 |
| 0x0804b628 | 0x0000136a | BUBONIC_VERMIN_CID | Bubonic Vermin | 06104968 |
| 0x0804b8c0 | 0x0000138a | VALKYRION_THE_MAGNA_WARRIOR_CID | Valkyrion the Magna Warrior | 75347539 |
| 0x0804bcec | 0x000013a7 | INJECTION_FAIRY_LILY_CID | Injection Fairy Lily | 79575620 |
| 0x0804b65c | 0x000013bd | SONIC_JAMMER_CID | Sonic Jammer | 84550200 |
| 0x0804b654 | 0x00001413 | FOUR_STARRED_LADYBUG_OF_DOOM_CID | 4-Starred Ladybug of Doom | 83994646 |
| 0x0804b678 | 0x00001481 | SUMMONER_OF_ILLUSIONS_CID | Summoner of Illusions | 14644902 |
| 0x0804bae8 | 0x00001488 | GILASAURUS_CID | Gilasaurus | 45894482 |
| 0x0804b688 | 0x00001489 | TORNADO_BIRD_CID | Tornado Bird | 71283180 |
| 0x0804bce0 | 0x0000148c | MARYOKUTAI_CID | Maryokutai | 71466592 |
| 0x0804bd9c | 0x0000149d | EKIBYO_DRAKMORD_CID | Ekibyo Drakmord | 69954399 |
| 0x0804b6fc | 0x00001530 | DICE_JAR_CID | Dice Jar | 03549275 |
| 0x0804b900 | 0x00001534 | FUSHIOH_RICHIE_CID | Fushioh Richie | 39711336 |
| 0x0804b72c | 0x00001590 | A_CAT_OF_ILL_OMEN_CID | A Cat of Ill Omen | 24140059 |
| 0x0804bdf8 | 0x0000159c | DIFFERENT_DIMENSION_CAPSULE_CID | Different Dimension Capsule | 11961740 |
| 0x0804baf4 | 0x000015b1 | XY_DRAGON_CANNON_CID | XY-Dragon Cannon | 02111707 |
| 0x0804b740 | 0x00001613 | OLD_VINDICTIVE_MAGICIAN_CID | Old Vindictive Magician | 45141844 |
| 0x0804b750 | 0x00001618 | MAGICAL_PLANT_MANDRAGOLA_CID | Magical Plant Mandragola | 07802006 |
| 0x0804b6cc | 0x0000161f | MAGICAL_MERCHANT_CID | Magical Merchant | 32362575 |
| 0x0804bb08 | 0x0000164c | GUARDIAN_GRARL_CID | Guardian Grarl | 47150851 |
| 0x0804b78c | 0x00001689 | IRON_BLACKSMITH_KOTETSU_CID | Iron Blacksmith Kotetsu | 73431236 |
| 0x0804bdf4 | 0x0000169c | FINAL_COUNTDOWN_CID | Final Countdown | 95308449 |
| 0x0804b7a4 | 0x000016c2 | WITCH_DOCTOR_OF_CHAOS_CID | Witch Doctor of Chaos | 75946257 |
| 0x0804b930 | 0x000016c9 | CHAOS_SORCERER_CID | Chaos Sorcerer | 09596126 |
| 0x0804b948 | 0x000016cb | BLACK_LUSTER_SOLDIER_ENVOY_CID | Black Luster Soldier - Envoy of the Beginning | 72989439 |
| 0x0804b85c | 0x00001758 | ARCHLORD_ZERATO_CID | Archlord Zerato | 18378582 |
| 0x0804bbd0 | 0x00001771 | SKULL_DESCOVERY_KNIGHT_CID | Skull Descovery Knight (sic; card-stats.s spelling) | 78700060 |
| 0x0804b7b4 | 0x0000178e | DESERTAPIR_CID | Desertapir | 13409151 |
| 0x0804baa0 | 0x000017c4 | RARE_METAL_DRAGON_CID | Rare Metal Dragon | 25236056 |
| 0x0804bd2c | 0x000017c6 | SORCERER_OF_DARK_MAGIC_CID | Sorcerer of Dark Magic | 88619463 |
| 0x0804b7e0 | 0x000017ea | NOBLEMAN_EATER_BUG_CID | Nobleman-Eater Bug | 65878864 |
| 0x0804bb14 | 0x00001806 | THE_TRICKY_CID | The Tricky | 14778250 |
| 0x0804be1c | 0x00001810 | THE_BLOCKMAN_CID | The Blockman | 48115277 |
| 0x0804bd58 | 0x0000183a | A_TEAM_TRAP_DISPOSAL_UNIT_CID | A-Team: Trap Disposal Unit | 13026402 |
| 0x0804be30 | 0x0000187c | SWORDS_OF_CONCEALING_LIGHT_CID | Swords of Concealing Light | 12923641 |
| 0x0804b9b4 | 0x00001895 | VAMPIRE_GENESIS_CID | Vampire Genesis | 22056710 |
| 0x0804bbcc | 0x000018ac | ANCIENT_GEAR_BEAST_CID | Ancient Gear Beast | 10509340 |
| 0x0804b7fc | 0x000018b5 | DUMMY_GOLEM_CID | Dummy Golem | 13532663 |
| 0x0804b978 | 0x000018b9 | MASTER_MONK_CID | Master Monk | 49814180 |
| 0x0804bbd8 | 0x000018c9 | ELEMENTAL_HERO_THUNDER_GIANT_CID | Elemental Hero Thunder Giant | 61204971 |
| 0x0804bae0 | 0x000018f6 | CYBER_DRAGON_CID | Cyber Dragon | 70095154 |
| 0x0804bc88 | 0x00001954 | VWXYZ_DRAGON_CATAPULT_CANNON_CID | VWXYZ-Dragon Catapult Cannon | 84243274 |
| 0x0804bb34 | 0x0000196e | FAMILIAR_POSSESSED_WYNN_CID | Familiar-Possessed - Wynn | 31764353 |
| 0x0804ba04 | 0x00001982 | DARK_ERADICATOR_WARLOCK_CID | Dark Eradicator Warlock | 29436665 |
| 0x0804bbfc | 0x00001987 | ELEMENTAL_HERO_STEAM_HEALER_CID | Elemental Hero Steam Healer | 81197327 |
| 0x0804bb54 | 0x000019aa | ANCIENT_GEAR_CID | Ancient Gear | 31557782 |
| 0x0804ba3c | 0x000019cd | PRINCESS_PIKERU_CID | Princess Pikeru | 75917088 |
| 0x0804bc30 | 0x000019ce | PRINCESS_CURRAN_CID | Princess Curran | 02316186 |

B 类共 63 槽 (全部新建 card_info.inc equate; 均经 card-stats.s slot_id -> 卡名 -> pw 验证, confidence: high).
注: RYU_SENSHI_CID (0x14c7, 0x0804bd00) 已在 card_info.inc -> 归入 A 类; DUMMY_GOLEM_CID (0x18b5) 为新建.

**C类: gap (未分配) card_id -> RENAME_SLOT 中性名 + EOL (7 槽)**

| 槽地址 | 值 | 拟 RENAME 标签 | 所在函数 | 说明 |
|--------|----|-----------|----|-----|
| 0x0804b53c | 0x000014c9 | get_card_field_summon_restriction_cid_14c9 | get_card_field_summon_restriction | gap: 0x14c8=Warrior_Dai_Grepher, 0x14ca=Frontier_Wiseman; unassigned in card-stats.s |
| 0x0804b544 | 0x00001051 | get_card_field_summon_restriction_cid_1051 | get_card_field_summon_restriction | gap: 0x1050=Spirit_of_the_Harp, 0x1052=Armaill; unassigned |
| 0x0804b8c8 | 0x000013e9 | upd_cid_13e9 | get_card_special_group_code | REUSE existing card_info.inc equate (already tagged as gap);归 A 类 |
| 0x0804b9cc | 0x000018a4 | get_card_special_group_code_cid_18a4 | get_card_special_group_code | gap: 0x189a=Kaibaman, 0x18a6=EHERO_Avian; unassigned |
| 0x0804bb9c | 0x00001729 | check_card_is_equip_target_eligible_cid_1729 | check_card_is_equip_target_eligible | gap: 0x1727=Abyss_Soldier, 0x172a=Inferno_Hammer; unassigned |
| 0x0804bd10 | 0x0000158a | get_card_equip_zone_rank_cid_158a | get_card_equip_zone_rank | gap: 0x1588=Gravekeeper_Spear_Soldier, 0x158c=Gravekeeper_Cannonholder; unassigned |
| 0x0804bd40 | 0x00001774 | get_card_equip_zone_rank_cid_1774 | get_card_equip_zone_rank | gap: 0x1773=Shield_Crash, 0x1775=Return_Zombie; unassigned |

注: 0x13e9 (`upd_cid_13e9`) 在 A 类中计入; C 类实际 RENAME 槽 = 6 个.

### RENAME_SLOTS (纯改名 + EOL)

**全部 6 个 gap CID 槽** (已在 C 类表格说明):

| 槽地址 | 原名 | 新标签 | EOL |
|--------|------|--------|-----|
| 0x0804b53c | DAT_0804b53c | get_card_field_summon_restriction_cid_14c9 | unassigned card slot between Warrior_Dai_Grepher(0x14c8) and Frontier_Wiseman(0x14ca) |
| 0x0804b544 | DAT_0804b544 | get_card_field_summon_restriction_cid_1051 | unassigned card slot between Spirit_of_the_Harp(0x1050) and Armaill(0x1052) |
| 0x0804b9cc | DAT_0804b9cc | get_card_special_group_code_cid_18a4 | unassigned card slot between Kaibaman(0x189a) and EHERO_Avian(0x18a6) |
| 0x0804bb9c | DAT_0804bb9c | check_card_is_equip_target_eligible_cid_1729 | unassigned card slot between Abyss_Soldier(0x1727) and Inferno_Hammer(0x172a) |
| 0x0804bd10 | DAT_0804bd10 | get_card_equip_zone_rank_cid_158a | unassigned card slot between Gravekeeper_Spear_Soldier(0x1588) and Gravekeeper_Cannonholder(0x158c) |
| 0x0804bd40 | DAT_0804bd40 | get_card_equip_zone_rank_cid_1774 | unassigned card slot between Shield_Crash(0x1773) and Return_Zombie(0x1775) |

### FUNC_RENAME (误名订正)

なし (0件). 全 10 個関数名は consumer 証拠と一致 (naming-proposals.csv 確認済み).

函数名语义核对:
- get_card_field_summon_restriction: indeg=18; callers in asm/02..06 均以 `cmp r0,#1; beq -> count_field_copies_of_card` 消费返回值; 名称准确 (high).
- get_card_special_group_code: indeg=3 (check_card_has_equip_placement_type / check_card_id_is_special_tribute_group / check_card_is_equip_target_eligible); 返回 [0..5] group code; 名称准确 (high).
- check_card_has_equip_placement_type: indeg=20; asm/02/03/05/07 均直接以返回值 bool 过滤; 名称准确 (high).
- check_card_not_equip_placement_type: indeg=2; 为前者取反 + 0x17c4 豁免; 名称准确 (high).
- check_card_id_is_special_tribute_group: indeg=0 (静态 bl 为零; 无 fn-ptr 引用); 名称描述功能准确 (high). 注: indeg=0 属 form(c) leaf (已在 plate 中注明).
- check_card_is_equip_target_eligible: indeg=5; asm/03 多处 `bl -> cmp r0,#0 -> bne excluded`; 名称准确 (high).
- check_card_id_is_equip_excluded_range: indeg=5 (含 check_card_is_equip_target_eligible); 返回语义反转 (0=excluded); 名称准确 (high).
- get_card_equip_zone_rank: indeg=6 (asm/05@0x4f20e + asm/06 x5); 返回 [1..3] rank; 名称准确 (high).
- check_card_id_is_equip_set_a: indeg=3 (asm/02/03/04); set A 判断; 名称准确 (high).

### PLATE (R5; 全 ASCII)

段内 10 个函数均已有 plate (@ 注释). 检查无 stale FUN_ (grep 0 hit confirmed).
检查无 CJK (所有 plate 均为 ASCII -- verified).

无需 plate 修改 (0件). 现有 plate 内容准确且 ASCII clean.

## carve 计划 (R7)

无 (段内无 inter-function ROM_INCBIN).

## disasm 计划 (R4)

无 (段内无误标数据块; 所有 ROM_INCBIN 在段外; 全 .zero 0x2 均为正常对齐填充).

## 新增 constants / 全局

### card_info.inc 新增 63 个 CID equate

全部为 card-stats.s 已证实的 slot_id -> 卡名 -> pw 三元组 (confidence: high).
注: EKIBYO_DRAKMORD_CID (0x149d) 不与现有 EKIBYO_DRAKMORD_CID_SHIFTED (0xa4e80000) 冲突 (值域不同, 名称不同).

```
.equ HARPIE_LADY_SISTERS_CID,              0x00000fe5  @ Harpie Lady Sisters (pw=12206212)
.equ PERFECTLY_ULTIMATE_GREAT_MOTH_CID,    0x00000fe9  @ Perfectly Ultimate Great Moth (pw=48579379)
.equ MASK_OF_DARKNESS_CID,                 0x0000100c  @ Mask of Darkness (pw=28933734)
.equ PRINCESS_OF_TSURUGI_CID,              0x000010b0  @ Princess of Tsurugi (pw=51371017)
.equ WALL_SHADOW_CID,                      0x00001117  @ Wall Shadow (pw=63162310)
.equ SUIJIN_CID,                           0x0000111b  @ Suijin (pw=98434877)
.equ METALZOA_CID,                         0x0000112e  @ Metalzoa (pw=50705071)
.equ MAGICIAN_OF_FAITH_CID,                0x00001152  @ Magician of Faith (pw=31560081)
.equ HANE_HANE_CID,                        0x000011c3  @ Hane-Hane (pw=07089711)
.equ NEEDLE_WORM_CID,                      0x000011d8  @ Needle Worm (pw=81843628)
.equ MORPHING_JAR_CID,                     0x000011f5  @ Morphing Jar (pw=33508719)
.equ INVADER_OF_THE_THRONE_CID,            0x00001227  @ Invader of the Throne (pw=03056267)
.equ RED_EYES_BLACK_METAL_DRAGON_CID,      0x0000128c  @ Red-Eyes Black Metal Dragon (pw=64335804)
.equ THE_FIEND_MEGACYBER_CID,              0x00001299  @ The Fiend Megacyber (pw=66362965)
.equ GERM_INFECTION_CID,                   0x0000130d  @ Germ Infection (pw=24668830)
.equ STIM_PACK_CID,                        0x0000131a  @ Stim-Pack (pw=83225447)
.equ BUBONIC_VERMIN_CID,                   0x0000136a  @ Bubonic Vermin (pw=06104968)
.equ VALKYRION_THE_MAGNA_WARRIOR_CID,      0x0000138a  @ Valkyrion the Magna Warrior (pw=75347539)
.equ INJECTION_FAIRY_LILY_CID,             0x000013a7  @ Injection Fairy Lily (pw=79575620)
.equ SONIC_JAMMER_CID,                     0x000013bd  @ Sonic Jammer (pw=84550200)
.equ FOUR_STARRED_LADYBUG_OF_DOOM_CID,     0x00001413  @ 4-Starred Ladybug of Doom (pw=83994646)
.equ SUMMONER_OF_ILLUSIONS_CID,            0x00001481  @ Summoner of Illusions (pw=14644902)
.equ GILASAURUS_CID,                       0x00001488  @ Gilasaurus (pw=45894482)
.equ TORNADO_BIRD_CID,                     0x00001489  @ Tornado Bird (pw=71283180)
.equ MARYOKUTAI_CID,                       0x0000148c  @ Maryokutai (pw=71466592)
.equ EKIBYO_DRAKMORD_CID,                  0x0000149d  @ Ekibyo Drakmord (pw=69954399)
.equ DICE_JAR_CID,                         0x00001530  @ Dice Jar (pw=03549275)
.equ FUSHIOH_RICHIE_CID,                   0x00001534  @ Fushioh Richie (pw=39711336)
.equ A_CAT_OF_ILL_OMEN_CID,               0x00001590  @ A Cat of Ill Omen (pw=24140059)
.equ DIFFERENT_DIMENSION_CAPSULE_CID,      0x0000159c  @ Different Dimension Capsule (pw=11961740)
.equ XY_DRAGON_CANNON_CID,                 0x000015b1  @ XY-Dragon Cannon (pw=02111707)
.equ OLD_VINDICTIVE_MAGICIAN_CID,          0x00001613  @ Old Vindictive Magician (pw=45141844)
.equ MAGICAL_PLANT_MANDRAGOLA_CID,         0x00001618  @ Magical Plant Mandragola (pw=07802006)
.equ MAGICAL_MERCHANT_CID,                 0x0000161f  @ Magical Merchant (pw=32362575)
.equ GUARDIAN_GRARL_CID,                   0x0000164c  @ Guardian Grarl (pw=47150851)
.equ IRON_BLACKSMITH_KOTETSU_CID,          0x00001689  @ Iron Blacksmith Kotetsu (pw=73431236)
.equ FINAL_COUNTDOWN_CID,                  0x0000169c  @ Final Countdown (pw=95308449)
.equ WITCH_DOCTOR_OF_CHAOS_CID,            0x000016c2  @ Witch Doctor of Chaos (pw=75946257)
.equ CHAOS_SORCERER_CID,                   0x000016c9  @ Chaos Sorcerer (pw=09596126)
.equ BLACK_LUSTER_SOLDIER_ENVOY_CID,       0x000016cb  @ Black Luster Soldier - Envoy of the Beginning (pw=72989439)
.equ ARCHLORD_ZERATO_CID,                  0x00001758  @ Archlord Zerato (pw=18378582)
.equ SKULL_DESCOVERY_KNIGHT_CID,           0x00001771  @ Skull Descovery Knight (pw=78700060)
.equ DESERTAPIR_CID,                       0x0000178e  @ Desertapir (pw=13409151)
.equ RARE_METAL_DRAGON_CID,                0x000017c4  @ Rare Metal Dragon (pw=25236056)
.equ SORCERER_OF_DARK_MAGIC_CID,           0x000017c6  @ Sorcerer of Dark Magic (pw=88619463)
.equ NOBLEMAN_EATER_BUG_CID,               0x000017ea  @ Nobleman-Eater Bug (pw=65878864)
.equ THE_TRICKY_CID,                       0x00001806  @ The Tricky (pw=14778250)
.equ THE_BLOCKMAN_CID,                     0x00001810  @ The Blockman (pw=48115277)
.equ A_TEAM_TRAP_DISPOSAL_UNIT_CID,        0x0000183a  @ A-Team: Trap Disposal Unit (pw=13026402)
.equ SWORDS_OF_CONCEALING_LIGHT_CID,       0x0000187c  @ Swords of Concealing Light (pw=12923641)
.equ VAMPIRE_GENESIS_CID,                  0x00001895  @ Vampire Genesis (pw=22056710)
.equ ANCIENT_GEAR_BEAST_CID,               0x000018ac  @ Ancient Gear Beast (pw=10509340)
.equ DUMMY_GOLEM_CID,                      0x000018b5  @ Dummy Golem (pw=13532663)
.equ MASTER_MONK_CID,                      0x000018b9  @ Master Monk (pw=49814180)
.equ ELEMENTAL_HERO_THUNDER_GIANT_CID,     0x000018c9  @ Elemental Hero Thunder Giant (pw=61204971)
.equ CYBER_DRAGON_CID,                     0x000018f6  @ Cyber Dragon (pw=70095154)
.equ VWXYZ_DRAGON_CATAPULT_CANNON_CID,     0x00001954  @ VWXYZ-Dragon Catapult Cannon (pw=84243274)
.equ FAMILIAR_POSSESSED_WYNN_CID,          0x0000196e  @ Familiar-Possessed - Wynn (pw=31764353)
.equ DARK_ERADICATOR_WARLOCK_CID,          0x00001982  @ Dark Eradicator Warlock (pw=29436665)
.equ ELEMENTAL_HERO_STEAM_HEALER_CID,      0x00001987  @ Elemental Hero Steam Healer (pw=81197327)
.equ ANCIENT_GEAR_CID,                     0x000019aa  @ Ancient Gear (pw=31557782)
.equ PRINCESS_PIKERU_CID,                  0x000019cd  @ Princess Pikeru (pw=75917088)
.equ PRINCESS_CURRAN_CID,                  0x000019ce  @ Princess Curran (pw=02316186)
```

### 内联 immediate EQ (非 DAT_ 槽; Ghidra scalar equate)

以下 3 个计算式 CID 和 2 个 field6 type 常量为 THUMB `movs+lsls` / `cmp #imm` 内联 immediate:

| 地址 | 指令 | 计算值 | 拟 EQ 名 | 卡名/含义 |
|------|------|--------|----------|---------|
| 0x0804b5c0 | movs r0,#0x90; lsls r0,r0,#5 | 0x1200 = Penguin Soldier | PENGUIN_SOLDIER_CID | pw=93920745; get_card_field_summon_restriction BST range boundary |
| 0x0804bcd6 | movs r0,#0xfe; lsls r0,r0,#4 | 0x0fe0 = Kuriboh | KURIBOH_CID | pw=40640057; get_card_equip_zone_rank BST boundary |
| 0x0804bdfc | movs r0,#0xad; lsls r0,r0,#5 | 0x15a0 = Dark Snake Syndrome | DARK_SNAKE_SYNDROME_CID | pw=47233801; check_card_id_is_equip_set_a BST boundary |
| 0x0804bca0 | cmp r5,#0x16 | 0x16 | CARD_FIELD6_EQUIP_CONTINUOUS | field6 value = continuous equip spell type |
| 0x0804bca4 | cmp r5,#0x17 | 0x17 | CARD_FIELD6_EQUIP_RITUAL | field6 value = ritual spell type (used with field9==1 check) |

注: `movs+lsls` 内联 immediate 对 Ghidra 而言两条指令 operand 均可加 equate,
但通常 fixer 对首条 `movs r0,#0x90` 的 `#0x90` 加 equate (该 scalar 在 Ghidra 显示); 
`cmp` immediate 同理. 这些不计入 101 DAT_ 槽覆盖计数, 作为附加 EQ 处理.

新增建议: PENGUIN_SOLDIER_CID / KURIBOH_CID / DARK_SNAKE_SYNDROME_CID 加入 card_info.inc (+3 条);
CARD_FIELD6_EQUIP_CONTINUOUS=0x16 / CARD_FIELD6_EQUIP_RITUAL=0x17 加入新文件或 card_info.inc (+2 条).

field6 值语义证据: asm/05_equip_eligibility_a.s L2578 plate "FIELD6_EQUIP=0x16" (confidence: high);
L6237 plate "equip_type_continuous=0x16, equip_type_ritual=0x17" (confidence: high);
L6715 plate "continuous equip (field6==0x16)" (confidence: high).

## §5.1 登记 (Rule 3) -- 0 引用块

无 (段内无 0 引用独立数据块; 全为代码+嵌入 literal pool).

## 消费者证据 (R6)

| 函数 | 消费者 | file:line | 置信度 |
|------|--------|-----------|--------|
| get_card_field_summon_restriction | asm/03_equip_chain_hand.s L207 `bl` + `cmp r0,#1; beq -> count_field_copies` | asm/03 L207-L213 | high |
| get_card_field_summon_restriction | asm/02_text_lp_fieldspell.s L14129 `bl` + `cmp r0,#1` | asm/02 L14129-14134 | high |
| check_card_has_equip_placement_type | asm/03 L2899 + L3062 + L12848 `bl` -> `cmp r0,#0; beq skip_equip` | asm/03 L2899-2902 | high |
| check_card_is_equip_target_eligible | asm/03 L2895 + L3058 + L12844 `bl` -> `cmp r0,#0; beq excluded` | asm/03 L2895-2897 | high |
| check_card_id_is_equip_set_a | asm/04 L11468 `bl` + `cmp r0,#0` | asm/04 L11468-11470 | high |
| get_card_equip_zone_rank | asm/05 L9522 `bl` + return [1..3] used in priority compare | asm/05 L9520-9525 | high |
| get_card_equip_zone_rank | asm/06 L16373/16376/16380/16394 x4 callers + L17191/17195 x2 | asm/06 multiple | high |

## 求助

なし (全槽 card-stats.s 验证通过, gap CID 均标中性名, 置信度充分).

## C13 精确清点

DAT_/DWORD_/PTR_ 槽总数 (python `re.match(DAT_|DWORD_|PTR_DAT_)` 精确计数): 101
ROM 字节验证: struct.unpack_from('<I', rom, addr-0x08000000) ALL MATCH (101/101)

覆盖拆分:
  A 类 (EQ 复用已有常量): 32 槽
    - 31 个独立 card_info.inc 已建 CID 常量
    - 1 个 upd_cid_13e9 (gap, card_info.inc 已有)
    - 0x15fc (DARK_PALADIN_CID) 两槽 (0x0804bba0 + 0x0804bcdc) 均映射同一 equate (合规)
  B 类 (EQ 新建常量):     63 槽 (全部新增 card_info.inc)
  C 类 (RENAME gap):       6 槽 (中性 `<func>_cid_<hex>` 标签)
  合计:                   101 槽 -- 覆盖差集为空

## ROM 字节自检结果

python struct.unpack_from('<I', rom, addr-0x08000000) 对全部 101 槽执行 -- ALL MATCH (verified).
