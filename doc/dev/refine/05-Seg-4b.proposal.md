# Refine Proposal: 05-Seg-4b  [0x0804be38..0x0804c6e8)

## 段测绘

- 函数入口 x14:
  - 0x0804be38  get_card_effect_category
  - 0x0804bf20  check_card_id_is_equip_set_b
  - 0x0804bf88  check_card_id_is_equip_set_d
  - 0x0804c014  check_card_is_equip_set_c
  - 0x0804c05c  check_card_id_is_equip_blocker
  - 0x0804c08c  check_card_id_is_equip_set_e
  - 0x0804c0e0  check_card_id_is_equip_excluded_set_f
  - 0x0804c140  check_card_id_is_field_zone_special
  - 0x0804c16c  check_card_is_zone_pair_restricted
  - 0x0804c18c  check_card_is_field_spell_type_b
  - 0x0804c1b8  get_card_effect_zone_check_sides
  - 0x0804c2e0  check_card_id_is_equip_set_g
  - 0x0804c38c  classify_card_id_summon_category
  - 0x0804c6cc  get_paired_card_id_by_variant

- 残留自动名槽 x99: 全部为 DAT_0804xxxx 格式 .word literal-pool 槽 (python 精确枚举)
  分布: get_card_effect_category x7 / check_card_id_is_equip_set_b x6 /
        check_card_id_is_equip_set_d x6 / check_card_is_equip_set_c x3 /
        check_card_id_is_equip_blocker x3 / check_card_id_is_equip_set_e x4 /
        check_card_id_is_equip_excluded_set_f x5 / check_card_id_is_field_zone_special x2 /
        check_card_is_zone_pair_restricted x2 / check_card_is_field_spell_type_b x2 /
        get_card_effect_zone_check_sides x14 / check_card_id_is_equip_set_g x9 /
        classify_card_id_summon_category x34 / get_paired_card_id_by_variant x2

- ROM_INCBIN / .byte 块 x1:
  - 0x0804becc  size 0x54  (between get_card_effect_category and check_card_id_is_equip_set_b)

---

## 数据块分类 (Rule 2/3) -- ref-scan 证据

| 块          | ref-scan (raw / THUMB+1)                      | 判定 | 理由                                                         |
|-------------|-----------------------------------------------|------|--------------------------------------------------------------|
| 0x4becc 0x54 | raw=0 / thumb=0; exhaustive 2B-step scan 0x54 | §5.1 | 0 引用; hex bytes 01 1c ... 70 47 = THUMB opcode dead code orphan |

---

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS -- card_info.inc CID equates

ROM 字节全部用 struct.unpack_from('<I', rom, addr-0x08000000) 核对, 全部 OK (spot-check 12 slots, all match).

#### A. 复用已有 card_info.inc 常量 (27 unique constants, 28 slots)

| slot addr  | ROM value | const_name                      | card name                       |
|------------|-----------|---------------------------------|---------------------------------|
| 0x0804c3e0 | 0x0000106d | PENGUIN_KNIGHT_CID             | Penguin Knight (Seg-1 built)   |
| 0x0804c180 | 0x000012d3 | AMPLIFIER_CID                  | Amplifier                       |
| 0x0804c3dc | 0x00001366 | PREMATURE_BURIAL_CID           | Premature Burial                |
| 0x0804c444 | 0x0000138a | VALKYRION_THE_MAGNA_WARRIOR_CID| Valkyrion the Magna Warrior     |
| 0x0804c3d8 | 0x00001488 | GILASAURUS_CID                 | Gilasaurus                      |
| 0x0804c100 | 0x000014c7 | RYU_SENSHI_CID                 | Ryu Senshi (slot 1/2)           |
| 0x0804c310 | 0x000014c7 | RYU_SENSHI_CID                 | Ryu Senshi (slot 2/2)           |
| 0x0804c110 | 0x000014da | FIEND_SKULL_DRAGON_CID         | Fiend Skull Dragon              |
| 0x0804c1f4 | 0x000014e2 | SUPER_REJUVENATION_CID         | Super Rejuvenation              |
| 0x0804c4d4 | 0x000014fb | FIBER_JAR_CID                  | Fiber Jar                       |
| 0x0804c4dc | 0x00001534 | FUSHIOH_RICHIE_CID             | Fushioh Richie                  |
| 0x0804c304 | 0x0000159d | NECROVALLEY_CID                | Necrovalley                     |
| 0x0804c4fc | 0x000015e6 | AUTONOMOUS_ACTION_UNIT_CID     | Autonomous Action Unit          |
| 0x0804be78 | 0x00001615 | MAGICAL_MARIONETTE_CID         | Magical Marionette              |
| 0x0804c598 | 0x000016a4 | EQUIP_LOCK_A_CID               | equip lock chain effect A       |
| 0x0804be90 | 0x000016de | TOWER_OF_BABEL_CID             | Tower of Babel                  |
| 0x0804c56c | 0x0000179a | NIGHT_ASSAILANT_CID            | Night Assailant                 |
| 0x0804c350 | 0x000017c2 | BLUE_EYES_SHINING_DRAGON_CID   | Blue-Eyes Shining Dragon        |
| 0x0804c370 | 0x0000183a | A_TEAM_TRAP_DISPOSAL_UNIT_CID  | A-Team: Trap Disposal Unit      |
| 0x0804c650 | 0x00001864 | BEHEMOTH_KING_CID              | Behemoth the King of All Animals|
| 0x0804c628 | 0x00001881 | RE_FUSION_CID                  | Re-Fusion                       |
| 0x0804c680 | 0x00001951 | WATER_DRAGON_CID               | Water Dragon                    |
| 0x0804c128 | 0x00001955 | CYBER_BLADER_CID               | Cyber Blader                    |
| 0x0804bf6c | 0x00001962 | BES_TETRAN_CID                 | B.E.S. Tetran                   |
| 0x0804bf80 | 0x000019b2 | ANCIENT_GEAR_CASTLE_CID        | Ancient Gear Castle             |
| 0x0804c57c | 0x0000164f | EQUIP_CHAIN_PAIR_CARD_MAX      | chain pairing upper bound = Guardian Tryce slot_id |
| 0x0804c164 | 0x000017d2 | HORUS_LV4_CID                  | Horus the Black Flame Dragon LV4 (reuse) |
| 0x0804c138 | 0x000019d6 | D3S_FROG_CID                   | D.3.S. Frog (reuse existing)   |

#### B. 新建 card_info.inc 常量 (57 unique new CID constants, covering 61 slots)

New CID constants needed (confirmed via card-stats.s passcode lookup; 57 unique new constants / 61 slots):

| slot addr(es) | ROM value | new const_name                       | card name (pw)                                    |
|---------------|-----------|--------------------------------------|---------------------------------------------------|
| 0x0804c0ac                | 0x000010a8 | BEASTKING_OF_THE_SWAMPS_CID   | Beastking of the Swamps (pw=99426834)             |
| 0x0804c0b8                | 0x000010b3 | VERSAGO_THE_DESTROYER_CID     | Versago the Destroyer (pw=50259460)               |
| 0x0804c3f0                | 0x00001138 | MONSTER_EYE_CID               | Monster Eye (pw=84133008)                         |
| 0x0804c02c                | 0x0000114f | THUNDER_DRAGON_CID            | Thunder Dragon (pw=31786629)                      |
| 0x0804c0a8                | 0x00001228 | MYSTICAL_SHEEP_1_CID          | Mystical Sheep #1 (pw=30451366)                   |
| 0x0804c074                | 0x00001232 | MAGICAL_LABYRINTH_CID         | Magical Labyrinth (pw=64389297)                   |
| 0x0804be60                | 0x0000128e | HANNIBAL_NECROMANCER_CID      | Hannibal Necromancer (pw=05640330)                |
| 0x0804bfc8                | 0x000012ce | MESMERIC_CONTROL_CID          | Mesmeric Control (pw=48642904)                    |
| 0x0804c404                | 0x000012ea | MONSTER_REBORN_CID            | Monster Reborn (pw=83764718)                      |
| 0x0804bfac + 0x0804c1f8   | 0x000012ec | POT_OF_GREED_CID              | Pot of Greed (pw=55144522)                        |
| 0x0804c308                | 0x00001302 | ROYAL_DECREE_CID              | Royal Decree (pw=51452091)                        |
| 0x0804bff4                | 0x00001307 | RESTRUCTER_REVOLUTION_CID     | Restructer Revolution (pw=99518961)               |
| 0x0804c20c                | 0x0000131f | UPSTART_GOBLIN_CID            | Upstart Goblin (pw=70368879)                      |
| 0x0804bfe8                | 0x00001325 | DELINQUENT_DUO_CID            | Delinquent Duo (pw=44763025)                      |
| 0x0804c008                | 0x0000132b | THE_FORCEFUL_SENTRY_CID       | The Forceful Sentry (pw=42829885)                 |
| 0x0804c414                | 0x0000133b | SPEAR_CRETIN_CID              | Spear Cretin (pw=58551308)                        |
| 0x0804c434                | 0x000013fe | DE_FUSION_CID                 | De-Fusion (pw=95286165)                           |
| 0x0804c45a (=0x0804c214)  | 0x0000145a | JAR_OF_GREED_CID              | Jar of Greed (pw=83968380)                        |
| 0x0804c184                | 0x0000147e | SPIRITUALISM_CID              | Spiritualism (pw=15866454)                        |
| 0x0804c1ac                | 0x00001497 | SPIRIT_MESSAGE_I_CID          | Spirit Message "I" (pw=31893528)                  |
| 0x0804c070                | 0x0000149c | FUSION_GATE_CID               | Fusion Gate (pw=33550694)                         |
| 0x0804c4b0                | 0x000014d2 | THE_WARRIOR_RETURNING_ALIVE_CID | The Warrior Returning Alive (pw=95281259)       |
| 0x0804c324                | 0x000014de | THE_DRAGONS_BEAD_CID          | The Dragon's Bead (pw=92408984)                   |
| 0x0804bf44 + 0x0804c334   | 0x00001529 | GREAT_DEZARD_CID              | Great Dezard (pw=88989706)                        |
| 0x0804c22c                | 0x00001567 | CARD_OF_SANCTITY_CID          | Card of Sanctity (pw=42664989)                    |
| 0x0804c50c                | 0x0000158f | MYSTICAL_KNIGHT_OF_JACKAL_CID | Mystical Knight of Jackal (pw=98745000)           |
| 0x0804be64                | 0x00001610 | SKILLED_WHITE_MAGICIAN_CID    | Skilled White Magician (pw=46363422)              |
| 0x0804c524                | 0x00001611 | SKILLED_DARK_MAGICIAN_CID     | Skilled Dark Magician (pw=73752131)               |
| 0x0804be5c + 0x0804c240   | 0x0000161a | ROYAL_MAGICAL_LIBRARY_CID     | Royal Magical Library (pw=70791313)               |
| 0x0804c248                | 0x0000162a | JAR_ROBBER_CID                | Jar Robber (pw=33784505)                          |
| 0x0804c3d4                | 0x00001631 | MIRACLE_RESTORING_CID         | Miracle Restoring (pw=68334074)                   |
| 0x0804c044                | 0x0000168f | DESROOK_ARCHFIEND_CID         | Desrook Archfiend (pw=72192100)                   |
| 0x0804c5a8                | 0x000016a8 | RAY_OF_HOPE_CID               | Ray of Hope (pw=82529174)                         |
| 0x0804c154                | 0x0000170a | MATAZA_THE_ZAPPER_CID         | Mataza the Zapper (pw=22609617)                   |
| 0x0804c5d8                | 0x00001713 | DEDICATION_THROUGH_LIGHT_DARK_CID | Dedication through Light and Darkness (pw=69542930) |
| 0x0804c5c8                | 0x00001745 | THE_KICK_MAN_CID              | The Kick Man (pw=90407382)                        |
| 0x0804c280                | 0x00001776 | CORPSE_OF_YATA_GARASU_CID     | Corpse of Yata-Garasu (pw=30461781)               |
| 0x0804c5f0                | 0x0000178a | ASWAN_APPARITION_CID          | Aswan Apparition (pw=88236094)                    |
| 0x0804c600                | 0x0000178c | NUBIAN_GUARD_CID              | Nubian Guard (pw=51616747)                        |
| 0x0804c054 + 0x0804c0d8   | 0x0000179c | KING_OF_THE_SWAMP_CID         | King of the Swamp (pw=79109599)                   |
| 0x0804c26c                | 0x000017a5 | CARD_7_CID                    | 7 (pw=67048711) -- card named "7"; conf med       |
| 0x0804c1b0                | 0x000017ae | THE_SECOND_SARCOPHAGUS_CID    | The Second Sarcophagus (pw=04081094)              |
| 0x0804c358                | 0x000017b9 | THE_END_OF_ANUBIS_CID         | The End of Anubis (pw=65403020)                   |
| 0x0804c638                | 0x000017f1 | DARK_FACTORY_MASS_PROD_CID    | Dark Factory of Mass Production (pw=90928333)     |
| 0x0804c00c                | 0x00001804 | CEMETARY_BOMB_CID             | Cemetary Bomb (pw=51394546)                       |
| 0x0804bf54                | 0x00001837 | BIG_CORE_CID                  | Big Core (pw=14148099)                            |
| 0x0804bea8                | 0x0000186a | BLAST_MAGICIAN_CID            | Blast Magician (pw=21051146)                      |
| 0x0804c664                | 0x0000187a | A_FEATHER_OF_THE_PHOENIX_CID  | A Feather of the Phoenix (pw=49140998)            |
| 0x0804c2a8                | 0x00001888 | GOOD_GOBLIN_HOUSEKEEPING_CID  | Good Goblin Housekeeping (pw=09744376)            |
| 0x0804c0fc                | 0x000018fd | CYBER_END_DRAGON_CID          | Cyber End Dragon (pw=01546123)                    |
| 0x0804bf3c                | 0x00001909 | SPARK_BLASTER_CID             | Spark Blaster (pw=97362768)                       |
| 0x0804c690                | 0x0000190a | DARK_RULER_VANDALGYON_CID     | Dark Ruler Vandalgyon (pw=24857466)               |
| 0x0804c384                | 0x00001936 | ALKANA_KNIGHT_JOKER_CID       | Alkana Knight Joker (pw=06150044)                 |
| 0x0804c2c0                | 0x0000196f | POT_OF_AVARICE_CID            | Pot of Avarice (pw=67169062)                      |
| 0x0804c6ac                | 0x00001979 | ROLL_OUT_CID                  | Roll Out! (pw=91597389)                           |
| 0x0804beb4                | 0x00001983 | MYTHICAL_BEAST_CERBERUS_CID   | Mythical Beast Cerberus (pw=55424270)             |
| 0x0804c2d0                | 0x0000198d | MAGICAL_MALLET_CID            | Magical Mallet (pw=85852291)                      |

NOTE: SKILLED_WHITE_MAGICIAN_CID (0x1610) and SKILLED_DARK_MAGICIAN_CID (0x1611) were listed in Seg-3's doc record as "built" but are NOT currently in constants/card_info.inc (grep confirmed empty). Creating them here.

Slots with shared value (same const applied to 2 slot addresses):
- POT_OF_GREED_CID (0x12ec): 0x0804bfac (check_card_id_is_equip_set_d) + 0x0804c1f8 (get_card_effect_zone_check_sides)
- GREAT_DEZARD_CID (0x1529): 0x0804bf44 (check_card_id_is_equip_set_b) + 0x0804c334 (check_card_id_is_equip_set_g)
- ROYAL_MAGICAL_LIBRARY_CID (0x161a): 0x0804be5c (get_card_effect_category) + 0x0804c240 (get_card_effect_zone_check_sides)
- KING_OF_THE_SWAMP_CID (0x179c): 0x0804c054 (check_card_is_equip_set_c) + 0x0804c0d8 (check_card_id_is_equip_set_e)

---

### RENAME_SLOTS (gap CIDs + structural constants; total 10)

Gap/unassigned CID slots (8): slot_id not assigned in card-stats.s (confirmed: all 8 are gaps between adjacent assigned entries).

| slot addr  | ROM value | proposed slot_label                          | EOL (ASCII)                                                                     |
|------------|-----------|----------------------------------------------|---------------------------------------------------------------------------------|
| 0x0804c460 | 0x0000144c | get_card_effect_zone_sides_cid_144c         | gap cid 0x144c; between Amazon Archer(0x144b) Fire Princess(0x144d); conf low  |
| 0x0804c470 | 0x00001452 | get_card_effect_zone_sides_cid_1452         | gap cid 0x1452; between Dancing Fairy(0x1451) Empress Mantis(0x1453); conf low |
| 0x0804c084 | 0x00001517 | check_equip_blocker_cid_1517                | gap cid 0x1517; between Disappear(0x1515) Bottomless Trap Hole(0x1518); conf low |
| 0x0804c4a0 | 0x00001549 | classify_summon_cat_cid_1549                | gap cid 0x1549; between Reckless Greed(0x1548) Toon DMG(0x154a); conf low      |
| 0x0804c534 | 0x00001616 | classify_summon_cat_cid_1616                | gap cid 0x1616; between Magical Marionette(0x1615) Breaker(0x1617); conf low   |
| 0x0804c1f0 | 0x000016c1 | get_card_effect_zone_sides_cid_16c1         | gap cid 0x16c1; between Freed the Brave(0x16c0) Witch Doctor(0x16c2); conf low |
| 0x0804bf40 | 0x000016fe | check_equip_set_b_cid_16fe                  | gap cid 0x16fe; between Don Turtle(0x16fd) Dark Driceratops(0x16ff); conf low  |
| 0x0804c28c | 0x00001790 | check_equip_set_g_cid_1790                  | gap cid 0x1790; between Sand Gambler(0x178f) Ghost Knight(0x1791); conf low    |

Structural constant slots (2):

| slot addr  | ROM value   | proposed slot_label                           | EOL (ASCII)                                                                   |
|------------|-------------|-----------------------------------------------|-------------------------------------------------------------------------------|
| 0x0804c6e0 | 0xffffe9b6  | get_paired_card_id_by_variant_base_sub        | = -0x164a (negate Guardian Elma CID range base; r0 -= 0x164a to get variant index) |
| 0x0804c6e4 | 0x0804c6e8  | get_paired_card_id_by_variant_table_ptr       | = &switchD_0804c6dc__switchdataD_0804c6e8; pointer to 6-entry jump table      |

---

### FUNC_RENAME

None required. All 14 function names match observed behavior (plate/body alignment confirmed).

---

### PLATE (R5; all ASCII)

1. `classify_card_id_summon_category` (0x0804c38c) -- 1 stale FUN_:
   - Stale ref: `FUN_0803088c`
   - Verified current name: `check_effect_slot_summon_path_eligible`
     (grep asm/02_text_lp_fieldspell.s shows label at 0x0803088c; confidence: high)
   - Action: full plate rewrite (substring replace FUN_0803088c -> check_effect_slot_summon_path_eligible)
   - Proposed ASCII plate:
     "Large BST: classifies card_id r0 into 3 summon/effect categories. Returns 0=no category, 1=category-1 (primary range up to 0x1631=MIRACLE_RESTORING_CID), 2=category-2 (special subset). Used by check_effect_slot_summon_path_eligible (0x0803088c) to decide activation path. r0=u16 card_id. Returns u32 category [0..2]."

2. All other 13 functions: 0 stale FUN_, 0 non-ASCII. No plate action needed.

---

## carve 计划 (R7)

None. No inter-function ROM_INCBIN in Seg-4b. The ROM_INCBIN at 0x4becc is intra-segment dead code -> §5.1.

---

## disasm 计划 (R4)

None. The ROM_INCBIN at 0x4becc (0x54 bytes): 0 references (raw=0, THUMB+1=0, exhaustive 2B-step scan over all 42 sub-addresses). Dead code -> §5.1 only.

The `switchD_0804c6dc` at 0x4c6dc is already Ghidra-labeled switch dispatch (not a THUMB-stub table needing R4 disasm). Case handlers (0x4c700..0x4c732) and jump table (0x4c6e8+) are in Seg-5; they need no processing here.

---

## 新增 constants / 全局 (card_info.inc +57)

Pre-scan: `grep -i "BEASTKING_OF_THE_SWAMPS\|VERSAGO\|MONSTER_EYE\|THUNDER_DRAGON\|MYSTICAL_SHEEP\|MAGICAL_LABYRINTH\|HANNIBAL" constants/card_info.inc` -> empty (confirmed no collision).

All 57 new constants go in `constants/card_info.inc`. No new constants in other .inc files.

card_info.inc additions:
```asm
.equ BEASTKING_OF_THE_SWAMPS_CID,        0x000010a8  @ Beastking of the Swamps (pw=99426834); equip set E
.equ VERSAGO_THE_DESTROYER_CID,          0x000010b3  @ Versago the Destroyer (pw=50259460); equip set E
.equ MONSTER_EYE_CID,                    0x00001138  @ Monster Eye (pw=84133008); summon category BST
.equ THUNDER_DRAGON_CID,                 0x0000114f  @ Thunder Dragon (pw=31786629); equip set C
.equ MYSTICAL_SHEEP_1_CID,               0x00001228  @ Mystical Sheep #1 (pw=30451366); equip set E
.equ MAGICAL_LABYRINTH_CID,              0x00001232  @ Magical Labyrinth (pw=64389297); equip blocker
.equ HANNIBAL_NECROMANCER_CID,           0x0000128e  @ Hannibal Necromancer (pw=05640330); effect category BST
.equ MESMERIC_CONTROL_CID,               0x000012ce  @ Mesmeric Control (pw=48642904); equip set D range bound
.equ MONSTER_REBORN_CID,                 0x000012ea  @ Monster Reborn (pw=83764718); summon category BST
.equ POT_OF_GREED_CID,                   0x000012ec  @ Pot of Greed (pw=55144522); equip set D + effect zone check
.equ ROYAL_DECREE_CID,                   0x00001302  @ Royal Decree (pw=51452091); equip set G
.equ RESTRUCTER_REVOLUTION_CID,          0x00001307  @ Restructer Revolution (pw=99518961); equip set D
.equ UPSTART_GOBLIN_CID,                 0x0000131f  @ Upstart Goblin (pw=70368879); effect zone check
.equ DELINQUENT_DUO_CID,                 0x00001325  @ Delinquent Duo (pw=44763025); equip set D
.equ THE_FORCEFUL_SENTRY_CID,            0x0000132b  @ The Forceful Sentry (pw=42829885); equip set D
.equ SPEAR_CRETIN_CID,                   0x0000133b  @ Spear Cretin (pw=58551308); summon category BST
.equ DE_FUSION_CID,                      0x000013fe  @ De-Fusion (pw=95286165); summon category BST
.equ JAR_OF_GREED_CID,                   0x0000145a  @ Jar of Greed (pw=83968380); effect zone check
.equ SPIRITUALISM_CID,                   0x0000147e  @ Spiritualism (pw=15866454); zone pair restriction
.equ SPIRIT_MESSAGE_I_CID,               0x00001497  @ Spirit Message "I" (pw=31893528); field spell type B range [0x1497..0x149a]
.equ FUSION_GATE_CID,                    0x0000149c  @ Fusion Gate (pw=33550694); equip blocker
.equ THE_WARRIOR_RETURNING_ALIVE_CID,    0x000014d2  @ The Warrior Returning Alive (pw=95281259); summon category BST
.equ THE_DRAGONS_BEAD_CID,               0x000014de  @ The Dragon's Bead (pw=92408984); equip set G
.equ GREAT_DEZARD_CID,                   0x00001529  @ Great Dezard (pw=88989706); equip sets B + G
.equ CARD_OF_SANCTITY_CID,               0x00001567  @ Card of Sanctity (pw=42664989); effect zone check
.equ MYSTICAL_KNIGHT_OF_JACKAL_CID,      0x0000158f  @ Mystical Knight of Jackal (pw=98745000); summon category BST
.equ SKILLED_WHITE_MAGICIAN_CID,         0x00001610  @ Skilled White Magician (pw=46363422); effect category BST
.equ SKILLED_DARK_MAGICIAN_CID,          0x00001611  @ Skilled Dark Magician (pw=73752131); summon category BST
.equ ROYAL_MAGICAL_LIBRARY_CID,          0x0000161a  @ Royal Magical Library (pw=70791313); effect category BST root + effect zone check
.equ JAR_ROBBER_CID,                     0x0000162a  @ Jar Robber (pw=33784505); effect zone check
.equ MIRACLE_RESTORING_CID,              0x00001631  @ Miracle Restoring (pw=68334074); summon category upper bound
.equ DESROOK_ARCHFIEND_CID,              0x0000168f  @ Desrook Archfiend (pw=72192100); equip set C
.equ RAY_OF_HOPE_CID,                    0x000016a8  @ Ray of Hope (pw=82529174); summon category BST
.equ MATAZA_THE_ZAPPER_CID,              0x0000170a  @ Mataza the Zapper (pw=22609617); field zone special
.equ DEDICATION_THROUGH_LIGHT_DARK_CID, 0x00001713  @ Dedication through Light and Darkness (pw=69542930); summon category BST
.equ THE_KICK_MAN_CID,                   0x00001745  @ The Kick Man (pw=90407382); summon category BST
.equ CORPSE_OF_YATA_GARASU_CID,          0x00001776  @ Corpse of Yata-Garasu (pw=30461781); effect zone check
.equ ASWAN_APPARITION_CID,               0x0000178a  @ Aswan Apparition (pw=88236094); summon category BST
.equ NUBIAN_GUARD_CID,                   0x0000178c  @ Nubian Guard (pw=51616747); summon category BST
.equ KING_OF_THE_SWAMP_CID,              0x0000179c  @ King of the Swamp (pw=79109599); equip set C + E
.equ CARD_7_CID,                         0x000017a5  @ 7 (pw=67048711); effect zone check; card named "7" (conf med)
.equ THE_SECOND_SARCOPHAGUS_CID,         0x000017ae  @ The Second Sarcophagus (pw=04081094); field spell type B range [0x17ad..0x17ae]
.equ THE_END_OF_ANUBIS_CID,              0x000017b9  @ The End of Anubis (pw=65403020); equip set G
.equ DARK_FACTORY_MASS_PROD_CID,         0x000017f1  @ Dark Factory of Mass Production (pw=90928333); summon category BST
.equ CEMETARY_BOMB_CID,                  0x00001804  @ Cemetary Bomb (pw=51394546); equip set D
.equ BIG_CORE_CID,                       0x00001837  @ Big Core (pw=14148099); equip set B
.equ BLAST_MAGICIAN_CID,                 0x0000186a  @ Blast Magician (pw=21051146); effect category BST
.equ A_FEATHER_OF_THE_PHOENIX_CID,       0x0000187a  @ A Feather of the Phoenix (pw=49140998); summon category BST
.equ GOOD_GOBLIN_HOUSEKEEPING_CID,       0x00001888  @ Good Goblin Housekeeping (pw=09744376); effect zone check
.equ CYBER_END_DRAGON_CID,               0x000018fd  @ Cyber End Dragon (pw=01546123); equip excluded set F
.equ SPARK_BLASTER_CID,                  0x00001909  @ Spark Blaster (pw=97362768); equip set B root
.equ DARK_RULER_VANDALGYON_CID,          0x0000190a  @ Dark Ruler Vandalgyon (pw=24857466); summon category BST
.equ ALKANA_KNIGHT_JOKER_CID,            0x00001936  @ Alkana Knight Joker (pw=06150044); equip set G + summon cat
.equ POT_OF_AVARICE_CID,                 0x0000196f  @ Pot of Avarice (pw=67169062); effect zone check
.equ ROLL_OUT_CID,                       0x00001979  @ Roll Out! (pw=91597389); summon category BST
.equ MYTHICAL_BEAST_CERBERUS_CID,        0x00001983  @ Mythical Beast Cerberus (pw=55424270); effect category BST
.equ MAGICAL_MALLET_CID,                 0x0000198d  @ Magical Mallet (pw=85852291); effect zone check
```

---

## §5.1 登记 (Rule 3) -- 0 引用块

| 地址       | 大小  | 初判内容                                                              | ref-scan 证据                                             |
|------------|-------|-----------------------------------------------------------------------|-----------------------------------------------------------|
| 0x0804becc | 0x54  | THUMB dead code orphan (01 1c...70 47 等 opcode); no named function | raw=0 / thumb+1=0; exhaustive 2B-step scan over [4becc, 4bf20) |

---

## 消费者证据 (R6) -- 关键槽语义

1. **get_card_effect_category** (0x0804be38):
   - plate @ asm line 6477: "Called by get_slot_effect_card_value (returns 0/non-0) and addr 0x0804513c"
   - CID 0x161a=Royal Magical Library (Spell Counter); 0x128e=Hannibal Necromancer; range 0x1610..0x1615=Skilled Mage / Magical Marionette cluster; 0x16de=Tower of Babel; 0x186a=Blast Magician; 0x1983=Mythical Beast Cerberus
   - Return codes: 0=none / 1=type_B / 3=type_C / 5=type_D / 0xff=type_A; confidence: high

2. **check_card_is_zone_pair_restricted** (0x0804c16c):
   - plate @ line 6939: "9 callers all use cmp r0,#0; bne -> special branch"
   - 0x12d3=Amplifier (AMPLIFIER_CID exists) / 0x147e=Spiritualism; confidence: high

3. **check_card_is_field_spell_type_b** (0x0804c18c):
   - plate @ line 6961: "Called by check_field_spell_b_placeable (0x080309fc)"
   - Range [0x1497..0x149a] = Spirit Message series (I/L/A/N, pw chain starting 31893528)
   - Range [0x17ad..0x17ae] = First/Second Sarcophagus; confidence: high

4. **get_card_effect_zone_check_sides** (0x0804c1b8):
   - plate @ line 6989: "Caller 0x0805a9a8 tests each bit and calls count_available_effect_zones per side"
   - Return 0=no check / 1=check opponent / 2=check self / 3=check both; confidence: high

5. **classify_card_id_summon_category** (0x0804c38c):
   - FUN_0803088c -> confirmed as check_effect_slot_summon_path_eligible (grep asm/02); confidence: high
   - 0x1631=Miracle Restoring = upper bound (ble check at function start); 0x1488=Gilasaurus

6. **get_paired_card_id_by_variant** (0x0804c6cc):
   - indeg=5; maps Guardian 0x164a..0x164f -> equip 0x165c..0x1661
   - 0x164a=Guardian Elma, 0x164f=Guardian Tryce, 0x165c=Butterfly Dagger, 0x1661=Twin Swords
   - GUARDIAN_KAYEST_CID=0x164e and GUARDIAN_GRARL_CID=0x164c and SHOOTING_STAR_BOW_CID=0x165d already in card_info.inc
   - DAT_0804c6e0 = -0x164a (subtract base); DAT_0804c6e4 = &jump_table; confidence: high

---

## C13 精确清点 (Rule)

Seg-4b [0x0804be38, 0x0804c6e8) DAT_/PTR_/DWORD_ 自动名槽总数: **99** (python re.match 枚举验证)

覆盖分配:
- EQ_SLOTS (reuse existing): 28 slots (27 unique constants; RYU_SENSHI at 2 slots; EQUIP_CHAIN_PAIR_CARD_MAX/HORUS_LV4_CID/D3S_FROG_CID moved from new-build)
- EQ_SLOTS (new card_info.inc): 61 slots (57 unique new constants; 4 constants at 2 slots each)
- RENAME_SLOTS (gap CID): 8 slots
- RENAME_SLOTS (structural): 2 slots
- Total: 28 + 61 + 8 + 2 = **99** checksum OK

ASCII self-check: all plate text and const comments above are ASCII-only (no CJK). Verified by visual inspection.
Slot label format check: all proposed labels match `^[a-z][a-z0-9_]+$`. OK.

---

## 求助

None. All card IDs verified against card-stats.s. All 8 gap CIDs confirmed as unassigned (no card between neighbors). Structural constants verified by arithmetic (-0x164a = 0xffffe9b6, ROM byte OK). FUN_0803088c resolved to check_effect_slot_summon_path_eligible by grep.
