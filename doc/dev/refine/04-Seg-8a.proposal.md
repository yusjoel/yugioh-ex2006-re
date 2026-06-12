# Refine Proposal: 04-Seg-8a  [0x08044e30..0x0804640c)

## ROM byte self-check summary
All 143 slot values verified via `struct.unpack_from('<I', rom, addr-0x08000000)`.
Zero address mismatches (cf. Seg-6 lesson: 6 wrong addresses). Spot-checked: 143/143 PASS.

---

## 段测绘

- 函数入口 x9:
  - 0x08044e30  `update_duel_field_slot_sprite_state`
  - 0x08045240  `enqueue_sprite_attr_with_xy_split`
  - 0x08045268  `enqueue_sprite_attr_with_shape`
  - 0x08045298  `enqueue_equip_set_slot_sprite_by_zone_col`
  - 0x08045314  `enqueue_effect_card_slot_sprite_attr`
  - 0x0804543c  `enqueue_equip_card_sprite_attr_for_slot`
  - 0x080454c0  `enqueue_effect_zone_pair_sprite_scan`
  - 0x08045530  `apply_nitro_unit_equip_activation`
  - 0x0804559c  `dispatch_card_effect_sprite_render_by_card_id`

- 残留自动名槽 x143 (DAT_/PTR_/DWORD_ in [0x08044e30, 0x0804640c)) — see 符号化计划
- ROM_INCBIN / .byte 块: 0 (pure code + literal pools)

---

## 数据块分类 (Rule 2/3)

No ROM_INCBIN or .byte blocks in this segment. All residual labels are function-internal
literal pool `.word` entries. Rule 2/3 data-block classification not applicable.

---

## 符号化计划 (R1/R2/R3)

Legend for source column: ROM addr verified = `struct.unpack_from('<I', rom, slot-0x08000000)`.

### EQ_SLOTS (data-equate)

EQ slots are pure scalar constants: OAM attr values, offsets, card IDs, masks.
All ROM byte values confirmed. Inc file column: "复用<inc>" or "新建<inc>".

#### Group A: PLAYER_BLOCK_STRIDE (x11)  -- 复用 ewram.inc line 250

| slot | value | const_name | slot_label | inc |
|------|-------|-----------|-----------|-----|
| 0x08044ed0 | 0x00000868 | PLAYER_BLOCK_STRIDE | dat_08044ed0_stride | ewram.inc REUSE |
| 0x0804516c | 0x00000868 | PLAYER_BLOCK_STRIDE | dat_0804516c_stride | ewram.inc REUSE |
| 0x080451a8 | 0x00000868 | PLAYER_BLOCK_STRIDE | dat_080451a8_stride | ewram.inc REUSE |
| 0x080452dc | 0x00000868 | PLAYER_BLOCK_STRIDE | dat_080452dc_stride | ewram.inc REUSE |
| 0x080453f4 | 0x00000868 | PLAYER_BLOCK_STRIDE | dat_080453f4_stride | ewram.inc REUSE |
| 0x08045488 | 0x00000868 | PLAYER_BLOCK_STRIDE | dat_08045488_stride | ewram.inc REUSE |
| 0x0804558c | 0x00000868 | PLAYER_BLOCK_STRIDE | dat_0804558c_stride | ewram.inc REUSE |
| 0x08045bf0 | 0x00000868 | PLAYER_BLOCK_STRIDE | dat_08045bf0_stride | ewram.inc REUSE |
| 0x08045c60 | 0x00000868 | PLAYER_BLOCK_STRIDE | dat_08045c60_stride | ewram.inc REUSE |
| 0x08045e3c | 0x00000868 | PLAYER_BLOCK_STRIDE | dat_08045e3c_stride | ewram.inc REUSE |
| 0x08045ef0 | 0x00000868 | PLAYER_BLOCK_STRIDE | dat_08045ef0_stride | ewram.inc REUSE |

#### Group B: OAM attribute constants (x8) -- 6 新建 oam_attr.inc, 0 REUSE

Values 0x003a/0x803a/0x003b/0x803b/0x003c/0x803c confirmed absent from all constants/*.inc.
Semantic: enqueue_sprite_attr_with_xy_split passes r0==0 -> 0x3a else 0x803a as OAM attr1;
enqueue_equip_set_slot_sprite_by_zone_col uses 0x3b/0x803b; enqueue_equip_card_sprite_attr_for_slot/
enqueue_effect_card_slot_sprite_attr use 0x3c/0x803c. bit15=H-flip = player-2 indicator.
Confidence: high (direct cmp r0,#0 / ldr / cmp-bne branch pattern, file:line confirmed).

| slot | value | const_name | slot_label | inc |
|------|-------|-----------|-----------|-----|
| 0x08045264 | 0x0000803a | OAM_XY_SPLIT_SPRITE_P2 | dat_08045264_oam | oam_attr.inc NEW |
| 0x08045294 | 0x0000803a | OAM_XY_SPLIT_SPRITE_P2 | dat_08045294_oam | oam_attr.inc NEW |
| 0x080452e4 | 0x0000803b | OAM_EQUIP_SET_SLOT_P2 | dat_080452e4_oam | oam_attr.inc NEW |
| 0x08045310 | 0x0000803b | OAM_EQUIP_SET_SLOT_P2 | dat_08045310_oam | oam_attr.inc NEW |
| 0x080453fc | 0x0000803c | OAM_EFFECT_CARD_SLOT_P2 | dat_080453fc_oam | oam_attr.inc NEW |
| 0x08045438 | 0x0000803c | OAM_EFFECT_CARD_SLOT_P2 | dat_08045438_oam | oam_attr.inc NEW |
| 0x08045490 | 0x0000803c | OAM_EFFECT_CARD_SLOT_P2 | dat_08045490_oam | oam_attr.inc NEW |
| 0x080454b8 | 0x0000803c | OAM_EFFECT_CARD_SLOT_P2 | dat_080454b8_oam | oam_attr.inc NEW |

Note: P1 variants (0x003a/0x003b/0x003c) are encoded inline via `movs r0,#0x3a` etc. and
do not appear as literal pool slots. Only the P2 (0x803a/0x803b/0x803c) values require .word
pool entries. The 6 new equates should still be declared as pairs for consistency:
  OAM_XY_SPLIT_SPRITE_P1 = 0x003a
  OAM_XY_SPLIT_SPRITE_P2 = 0x803a
  OAM_EQUIP_SET_SLOT_P1  = 0x003b
  OAM_EQUIP_SET_SLOT_P2  = 0x803b
  OAM_EFFECT_CARD_SLOT_P1 = 0x003c
  OAM_EFFECT_CARD_SLOT_P2 = 0x803c

#### Group C: Offset constants (x8) -- all REUSE from duel_field.inc / ewram.inc

| slot | value | const_name | slot_label | inc |
|------|-------|-----------|-----------|-----|
| 0x08045408 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | dat_08045408_off | ewram.inc REUSE line 274 |
| 0x080460e0 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | dat_080460e0_off | ewram.inc REUSE line 274 |
| 0x08046150 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | dat_08046150_off | ewram.inc REUSE line 274 |
| 0x080460e4 | 0x00001cf4 | FIELD_STATE_OFF | dat_080460e4_off | duel_field.inc REUSE line 205 |
| 0x08046154 | 0x00001cf4 | FIELD_STATE_OFF | dat_08046154_off | duel_field.inc REUSE line 205 |
| 0x08045a9c | 0x000010d0 | EFFECT_ZONE_BITMASK_OFF | dat_08045a9c_off | duel_field.inc REUSE line 166 |
| 0x08045c5c | 0x000010d0 | EFFECT_ZONE_BITMASK_OFF | dat_08045c5c_off | duel_field.inc REUSE line 166 |
| 0x080450d4 | 0x00001d3c | P1LP_EQUIP_BITMAP_CTR_OFF | dat_080450d4_off | ewram.inc NEW |
| 0x08045218 | 0x00001d3c | P1LP_EQUIP_BITMAP_CTR_OFF | dat_08045218_off | ewram.inc NEW |

P1LP_EQUIP_BITMAP_CTR_OFF = 0x1d3c: confirmed absent from all constants/*.inc.
Semantic: [gP1LifePoints + player*0x868 + 0x1d3c] = modulo-10 animation frame counter
for equip-slot bitmap sprite. Used in update_duel_field_slot_sprite_state at LAB_080450ac
and LAB_080451f0: load, increment, wrap at 9, call enqueue_equip_slot_bitmap_update.
6 raw ROM refs. Confidence: high (asm/04_card_zone_sprite.s L11213, L11377).

#### Group D: Sentinel mask (x3) -- 新建 duel_field.inc

| slot | value | const_name | slot_label | inc |
|------|-------|-----------|-----------|-----|
| 0x08045a94 | 0xffff0000 | EQUIP_CHAIN_SENTINEL | dat_08045a94_sent | duel_field.inc NEW |
| 0x08045be8 | 0xffff0000 | EQUIP_CHAIN_SENTINEL | dat_08045be8_sent | duel_field.inc NEW |
| 0x08045c54 | 0xffff0000 | EQUIP_CHAIN_SENTINEL | dat_08045c54_sent | duel_field.inc NEW |

Semantic: 0xffff0000 used as gEquipChainSlotRefs list terminator sentinel;
`ldr r_term, [slot]; cmp r_val, r_term; beq exit` pattern.
Confirm via asm/04_card_zone_sprite.s L12617, L12821, L12880. Confidence: high.
Check existing duel_field.inc for EQUIP_CHAIN_SENTINEL before adding (grep returns empty).

#### Group E: 0x101 sprite-pair attr constant (x1) -- 新建 oam_attr.inc

| slot | value | const_name | slot_label | inc |
|------|-------|-----------|-----------|-----|
| 0x080454bc | 0x00000101 | EQUIP_PAIR_SPRITE_EXTRA | dat_080454bc_pair | oam_attr.inc NEW |

Semantic: r3=0x101 passed as 4th arg to enqueue_sprite_attr_record in
enqueue_equip_card_sprite_attr_for_slot. Packs two bytes: byte[0]=0x01 (pair-slot type),
byte[1]=0x01 (pair mode). Used once. Confidence: med (asm/04_card_zone_sprite.s L11722;
exact semantics of extra field in enqueue_sprite_attr_record not fully decoded in this
segment). EOL: "equip pair sprite attr: type=1, mode=1".

#### Group F: Card ID equates (x78) -- mix of REUSE card_info.inc and NEW

Existing in card_info.inc (REUSE, grep confirmed): SLATE_WARRIOR_CID=0x13ad,
ARCHFIEND_OF_GILFER_CID=0x13e3, MAKYURA_THE_DESTRUCTOR_CID=0x14a5,
BLAST_WITH_CHAIN_CID=0x1514, EXODIA_NECROSS_CID=0x1645,
MANTICORE_OF_DARKNESS_CID=0x16f9, MOKEY_MOKEY_CID=0x1782,
SILENT_SWORDSMAN_LV5_CID=0x1814, SILENT_MAGICIAN_LV4_CID=0x1817,
MOKEY_MOKEY_SMACKDOWN_CID=0x1843, WATER_DRAGON_CID=0x1951, SAND_MOTH_CID=0x19d2.

New card IDs (57 named + 4 gaps) to add to card_info.inc (3 named CIDs changed to REUSE; 0x1368 removed from gap list as REUSE SPELL_ZONE_TARGET_CARD_ID):

| slot(s) | value | const_name | card name (pw) | status |
|---------|-------|-----------|----------------|--------|
| 0x08044ed4 | 0x1645 | EXODIA_NECROSS_CID | Exodia Necross (12600382) | REUSE |
| 0x08044ed8 | 0x1337 | KARATE_MAN_CID | Karate Man (23289281) | NEW |
| 0x08044edc | 0x120e | upd_cid_120e | gap (not in card-stats.s) | NEW low-conf |
| 0x08044ee0 | 0x10c6 | upd_cid_10c6 | gap (not in card-stats.s) | NEW low-conf |
| 0x08044ef0 | 0x1153 | GODDESS_OF_WHIM_CID | Goddess of Whim (67959180) | NEW |
| 0x08044f14 | 0x1296 | JINZO_CID | Jinzo (77585513) | NEW |
| 0x08044f30 | 0x12ac | SATELLITE_CANNON_CID | Satellite Cannon (50400231) | NEW |
| 0x08044f38 | 0x12bb | COPYCAT_CID | Copycat (26376390) | NEW |
| 0x08044f60 | 0x147d | ZOMBYRA_THE_DARK_CID | Zombyra the Dark (88472456) | REUSE |
| 0x08044f70 | 0x13b2 | MUCUS_YOLK_CID | Mucus Yolk (70307656) | NEW |
| 0x08044f8c | 0x1527 | ROYAL_KEEPER_CID | Royal Keeper (16509093) | NEW |
| 0x08044fa4 | 0x154c | EXARION_UNIVERSE_CID | Exarion Universe (63749102) | NEW |
| 0x08044fd8 | 0x1835 | GAIA_SOUL_CID | Gaia Soul the Combustible Collective (51355346) | NEW |
| 0x08044fdc | 0x1688 | GREAT_MAJU_GARZETT_CID | Great Maju Garzett (47942531) | NEW |
| 0x08044fec | 0x172b | EMES_THE_INFINITY_CID | Emes the Infinity (43580269) | NEW |
| 0x08045008 | 0x1814 | SILENT_SWORDSMAN_LV5_CID | Silent Swordsman LV5 (74388798) | REUSE |
| 0x08045020 | 0x181a | SILENT_MAGICIAN_LV8_CID | Silent Magician LV8 (72443568) | NEW |
| 0x08045028 | 0x182d | RAGING_FLAME_SPRITE_CID | Raging Flame Sprite (90810762) | REUSE |
| 0x0804504c | 0x18fb | UFOROID_FIGHTER_CID | UFOroid Fighter (32752319) | NEW |
| 0x08045064 | 0x18ae | MILLENNIUM_SCORPION_CID | Millennium Scorpion (82482194) | NEW |
| 0x08045070 | 0x18b4 | MEGAROCK_DRAGON_CID | Megarock Dragon (71544954) | NEW |
| 0x0804508c | 0x1996 | WHITE_HORNS_DRAGON_CID | White Horns D. (73891874) | NEW |
| 0x080450a8 | 0x19a5 | RAVIEL_LORD_CID | Raviel, Lord of Phantasms (69890967) | NEW |
| 0x080451c4 | 0x1368 | SPELL_ZONE_TARGET_CARD_ID | cross-player spell-zone effect node type ID | REUSE |
| 0x080451dc | 0x17ff | NINJITSU_ART_OF_DECOY_CID | Ninjitsu Art of Decoy (89628781) | NEW |
| 0x080451e0 | 0x1495 | THE_EMPERORS_HOLIDAY_CID | The Emperor's Holiday (68400115) | NEW |
| 0x080451ec | 0x184a | XING_ZHEN_HU_CID | Xing Zhen Hu (76515293) | NEW |
| 0x08045400 | 0x1817 | SILENT_MAGICIAN_LV4_CID | Silent Magician LV4 (73665146) | REUSE |
| 0x0804540c | 0x181a | SILENT_MAGICIAN_LV8_CID | (see above) | NEW |
| 0x08045410 | 0x16de | TOWER_OF_BABEL_CID | Tower of Babel (94256039) | NEW |
| 0x08045524 | 0x10f4 | UMI_CARD_ID | Umi (22702055) | REUSE |
| 0x0804552c | 0x13f7 | TORNADO_WALL_CID | Tornado Wall (18605135) | NEW |
| 0x08045658 | 0x1591 | YOMI_SHIP_CID | Yomi Ship (51534754) | NEW |
| 0x0804565c | 0x1342 | MYSTIC_TOMATO_CID | Mystic Tomato (83011277) | NEW |
| 0x08045660 | 0x0fd6 | SANGAN_CID | Sangan (26202165) | NEW |
| 0x08045668 | 0x10dd | BLACK_PENDANT_CID | Black Pendant (65169794) | NEW |
| 0x0804568c | 0x1185 | COCKROACH_KNIGHT_CID | Cockroach Knight (33413638) | NEW |
| 0x080456a4 | 0x11e4 | WITCH_OF_THE_BLACK_FOREST_CID | Witch of the Black Forest (78010363) | NEW |
| 0x080456d0 | 0x133a | NIMBLE_MOMONGA_CID | Nimble Momonga (22567609) | NEW |
| 0x080456e0 | 0x1333 | GIANT_RAT_CID | Giant Rat (97017120) | NEW |
| 0x080456f8 | 0x133c | SHINING_ANGEL_CID | Shining Angel (95956346) | NEW |
| 0x08045724 | 0x14ab | AMAZONESS_CHAIN_MASTER_CID | Amazoness Chain Master (29654737) | NEW |
| 0x0804572c | 0x13ad | SLATE_WARRIOR_CID | Slate Warrior (78636495) | REUSE |
| 0x08045748 | 0x13e3 | ARCHFIEND_OF_GILFER_CID | Archfiend of Gilfer (50287060) | REUSE |
| 0x08045758 | 0x13e9 | upd_cid_13e9 | gap (not in card-stats.s) | NEW low-conf |
| 0x08045780 | 0x1514 | BLAST_WITH_CHAIN_CID | Blast with Chain (98239899) | REUSE |
| 0x08045798 | 0x14f6 | AGIDO_CID | Agido (16135253) | NEW |
| 0x080457b0 | 0x1544 | DARK_COFFIN_CID | Dark Coffin (01804528) | NEW |
| 0x080457c8 | 0x156d | LORD_POISON_CID | Lord Poison (40320754) | NEW |
| 0x08045800 | 0x1841 | NECKLACE_OF_COMMAND_CID | Necklace of Command (48576971) | NEW |
| 0x08045804 | 0x16f5 | BURNING_ALGAE_CID | Burning Algae (41859700) | NEW |
| 0x08045814 | 0x163f | GRANADORA_CID | Granadora (13944422) | NEW |
| 0x08045834 | 0x16c8 | SILPHEED_CID | Silpheed (73001017) | NEW |
| 0x0804583c | 0x16cc | FUHMA_SHURIKEN_CID | Fuhma Shuriken (09373534) | NEW |
| 0x0804586c | 0x17c3 | FAMILIAR_KNIGHT_CID | Familiar Knight (89731911) | NEW |
| 0x08045884 | 0x1796 | EMISSARY_OF_THE_AFTERLIFE_CID | Emissary of the Afterlife (75043725) | NEW |
| 0x080458a4 | 0x17e6 | MASKED_DRAGON_CID | Masked Dragon (39191307) | NEW |
| 0x080458b4 | 0x183d | MOKEY_MOKEY_KING_CID | Mokey Mokey King (13803864) | NEW |
| 0x080458e8 | 0x1914 | GIANT_KOZAKY_CID | Giant Kozaky (58185394) | NEW |
| 0x080458f8 | 0x1869 | MECHA_DOG_MARRON_CID | Mecha-Dog Marron (94667532) | NEW |
| 0x08045914 | 0x18d7 | KOZAKYS_SELF_DESTRUCT_CID | Kozaky's Self-Destruct Button (21908319) | NEW |
| 0x08045924 | 0x18f4 | UFOROID_CID | UFOroid (07602840) | NEW |
| 0x08045950 | 0x1951 | WATER_DRAGON_CID | Water Dragon (85066822) | REUSE |
| 0x08045964 | 0x1946 | OJAMAGIC_CID | Ojamagic (24643836) | NEW |
| 0x08045988 | 0x19c5 | GOKIPON_CID | Gokipon (14472500) | NEW |
| 0x080459a0 | 0x19d2 | SAND_MOTH_CID | Sand Moth (73648243) | REUSE |
| 0x08045ef8 | 0x18d1 | NITRO_UNIT_CID | Nitro Unit (23842445) | NEW |
| 0x08045f00 | 0x1672 | upd_cid_1672 | gap (not in card-stats.s) | NEW low-conf |
| 0x08045f04 | 0x14a5 | MAKYURA_THE_DESTRUCTOR_CID | Makyura the Destructor (21593977) | REUSE |
| 0x08045f18 | 0x1522 | VAMPIRE_LORD_CID | Vampire Lord (53839837) | NEW |
| 0x08045f38 | 0x18bc | DD_SURVIVOR_CID | D.D. Survivor (48092532) | NEW |
| 0x08045f3c | 0x16f9 | MANTICORE_OF_DARKNESS_CID | Manticore of Darkness (77121851) | REUSE |
| 0x08045f40 | 0x185c | SACRED_PHOENIX_CID | Sacred Phoenix of Nephthys (61441708) | NEW |
| 0x08045f68 | 0x19f8 | HELIOS_TRIS_MEGISTE_CID | Helios Tris Megiste (17286057) | NEW |
| 0x08045fc4 | 0x1595 | COBRA_JAR_CID | Cobra Jar (86801871) | NEW |
| 0x08045fe0 | 0x166a | OJAMA_TRIO_CID | Ojama Trio (29843091) | NEW |
| 0x08046234 | 0x1782 | MOKEY_MOKEY_CID | Mokey Mokey (27288416) | REUSE |
| 0x08046238 | 0x1843 | MOKEY_MOKEY_SMACKDOWN_CID | Mokey Mokey Smackdown (01965724) | REUSE |
| 0x0804629c | 0x1843 | MOKEY_MOKEY_SMACKDOWN_CID | (dup) | REUSE |
| 0x08046364 | 0x1862 | MAJI_GIRE_PANDA_CID | Maji-Gire Panda (60102563) | NEW |
| 0x08046368 | 0x1875 | FIREBIRD_CID | Firebird (87473172) | NEW |
| 0x0804636c | 0x18b2 | CRIOSPHINX_CID | Criosphinx (18654201) | NEW |

CID verification method: `grep 'slot=0x<CID>' data/card-stats.s`; all confirmed.
Gap CIDs (0x10c6, 0x120e, 0x13e9, 0x1672): no entry in card-stats.s ±5 neighbors;
neutral label `upd_cid_<hex>` low-conf; no fabricated card names.
Note: 0x1368 is NOT a gap CID -- it is REUSE SPELL_ZONE_TARGET_CARD_ID (card_info.inc), a cross-player spell-zone effect node type ID.

Note on PANDEMONIUM_CID and CENTRIFUGAL_FIELD_CID: these values appear only in composite
packed words (Group H below) not as standalone CID pool entries. They should still be added
to card_info.inc for cross-segment consistency:
  PANDEMONIUM_CID = 0x169f (card_3882, Pandemonium, pw=94585852)
  CENTRIFUGAL_FIELD_CID = 0x187f (card_4362, Centrifugal Field, pw=01801154)

---

### REF_SLOTS (USER-label + DATA-ref)

#### Group G: Pointer slots to EWRAM globals (x18)

All values confirmed via ROM byte check. Existing globals REUSE ewram.inc.

| slot | value | gas_label | slot_label | inc |
|------|-------|-----------|-----------|-----|
| 0x08045170 | 0x0201c510 | gDuelFieldSlots | dat_08045170_ptr | ewram.inc REUSE |
| 0x080451ac | 0x0201c510 | gDuelFieldSlots | dat_080451ac_ptr | ewram.inc REUSE |
| 0x080452e0 | 0x0201c510 | gDuelFieldSlots | dat_080452e0_ptr | ewram.inc REUSE |
| 0x080453f8 | 0x0201c510 | gDuelFieldSlots | dat_080453f8_ptr | ewram.inc REUSE |
| 0x0804548c | 0x0201c510 | gDuelFieldSlots | dat_0804548c_ptr | ewram.inc REUSE |
| 0x08045590 | 0x0201c510 | gDuelFieldSlots | dat_08045590_ptr | ewram.inc REUSE |
| 0x08045e40 | 0x0201c5d8 | gDuelFieldSlots_p2_base | dat_08045e40_ptr | ewram.inc REUSE |
| 0x08045ef4 | 0x0201c5d8 | gDuelFieldSlots_p2_base | dat_08045ef4_ptr | ewram.inc REUSE |
| 0x080459fc | 0x0201bb90 | gEquipChainSlotRefs | dat_080459fc_ptr | ewram.inc REUSE |
| 0x08045a34 | 0x0201bb90 | gEquipChainSlotRefs | dat_08045a34_ptr | ewram.inc REUSE |
| 0x08045af8 | 0x0201bb90 | gEquipChainSlotRefs | dat_08045af8_ptr | ewram.inc REUSE |
| 0x08045b2c | 0x0201bb90 | gEquipChainSlotRefs | dat_08045b2c_ptr | ewram.inc REUSE |
| 0x080461bc | 0x0201bb90 | gEquipChainSlotRefs | dat_080461bc_ptr | ewram.inc REUSE |
| 0x0804623c | 0x0201bb90 | gEquipChainSlotRefs | dat_0804623c_ptr | ewram.inc REUSE |
| 0x080462a0 | 0x0201bb90 | gEquipChainSlotRefs | dat_080462a0_ptr | ewram.inc REUSE |
| 0x08045528 | 0x0201e1c8 | gEquipZoneCountTable | dat_08045528_ptr | ewram.inc NEW |
| 0x08045d08 | 0x0201d9c0 | gEquipNodePool | dat_08045d08_ptr | ewram.inc REUSE |

gEquipZoneCountTable = 0x0201e1c8: confirmed absent from all constants/*.inc.
Semantic: equip zone count tracking table base; 55 raw ROM refs total; used as array base
in loop counting active equip zones. Name confirmed via asm/08_equip_oam_neodaed.s context.
Confidence: high. Comment: "equip zone count tracking table; 55 ROM refs".

#### Group H: THUMB fn-ptr (x1)

| slot | value | gas_label | slot_label | inc |
|------|-------|-----------|-----------|-----|
| 0x08045efc | 0x08045531 | apply_nitro_unit_equip_activation+1 | dat_08045efc_fnptr | (fn-ptr) |

ROM value = 0x08045531 = 0x08045530 + 1 (odd = THUMB).
apply_nitro_unit_equip_activation is at 0x08045530 (asm L11798).
GAS: `.word apply_nitro_unit_equip_activation+1`
Stored in dispatch_card_effect_sprite_render_by_card_id dispatch table; invoked when
card_id == NITRO_UNIT_CID (0x18d1). Confidence: high (asm/04_card_zone_sprite.s L13239).

---

### RENAME_SLOTS (composite/packed values; EOL in ASCII)

These are values that pack multiple fields or represent activation-context composites.
They get a descriptive slot_label and EOL comment (no equate in inc files).

| slot | value | slot_label | eol_ascii |
|------|-------|-----------|-----------|
| 0x08045594 | 0xc6880000 | nitro_unit_slot_filter | "slot_word<<0x13 filter: low13=NITRO_UNIT_CID(0x18d1) + activation hi-bits" |
| 0x08045598 | 0x2c4e18d1 | nitro_unit_activation_packed | "packed activation: card_id=0x18d1(Nitro Unit) + ctx bits [31:13]" |
| 0x08045db4 | 0x364d0000 | archfiend_path_composite | "Archfiend slot path composite: upper=0x364d encode type+player fields" |
| 0x08045db8 | 0x0000169f | PANDEMONIUM_CID_raw | use PANDEMONIUM_CID equate in card_info.inc; slot_label=dat_08045db8_cid |
| 0x08045dbc | 0x012a169f | pandemonium_activation_a | "packed activation: card_id=0x169f(Pandemonium) + ctx=0x012a (mode A)" |
| 0x08045e38 | 0x002a169f | pandemonium_activation_b | "packed activation: card_id=0x169f(Pandemonium) + ctx=0x002a (mode B)" |
| 0x08045e44 | 0x0000187f | CENTRIFUGAL_FIELD_CID_raw | use CENTRIFUGAL_FIELD_CID equate; slot_label=dat_08045e44_cid |
| 0x08045e48 | 0x012a187f | centrifugal_field_activation_a | "packed activation: card_id=0x187f(Centrifugal Field) + ctx=0x012a (mode A)" |
| 0x08045eec | 0x002a187f | centrifugal_field_activation_b | "packed activation: card_id=0x187f(Centrifugal Field) + ctx=0x002a (mode B)" |
| 0x080463d4 | 0x2c200000 | spell_path_composite_a | "Spell zone path composite A: upper=0x2c20 encode type+player fields" |
| 0x08046408 | 0x36200000 | spell_path_composite_b | "Spell zone path composite B: upper=0x3620 encode type+player fields" |

Notes:
- 0x08045db8 (0x0000169f) and 0x08045e44 (0x0000187f) are bare CID values, not composites.
  Reclassify as EQ_SLOTS using PANDEMONIUM_CID and CENTRIFUGAL_FIELD_CID respectively.
- 0x012a169f, 0x002a169f, 0x012a187f, 0x002a187f: the upper 16 bits encode activation
  context (0x012a = compare-mode A, 0x002a = compare-mode B). Cannot fully decode without
  check_equip_activation_eligible source; partial decode is high-conf. EOL documents known fields.
- Composite values for Archfiend (0x364d0000) and Spell path (0x2c200000/0x36200000):
  upper 16-bit field encodes zone-type + player ID in a packed format consistent with
  activation_ctx. Exact bit-field layout requires deeper analysis of caller; partial decode.
  Confidence: med. Mark EOL with known partial decode; do not fabricate full field names.

Correction: 0x08045db8 -> EQ_SLOT PANDEMONIUM_CID; 0x08045e44 -> EQ_SLOT CENTRIFUGAL_FIELD_CID.
Adjusted EQ count += 2; RENAME count -= 2.

---

### FUNC_RENAME

No function rename candidates identified in this segment.
- All 9 function names are internally consistent with their bodies.
- Plate comments with stale FUN_ are caller/callee references, not self-referential contradictions.

---

### PLATE (R5 -- substring FUN_ replacement)

5 functions have stale FUN_ references in plate comments.
All are substring replacements (not full rewrites; 0 non-ASCII chars in all plates).
All current names resolved from asm label scan.

#### 1. update_duel_field_slot_sprite_state (before L10823)
Stale refs in pre-function plate comment (line 10822):
- FUN_08044dcc -> enqueue_field_slot_sprite_with_state_update  (04_card_zone_sprite.s)
- FUN_0805b990 -> scan_equip_zone_candidates_with_snapshot     (06_equip_eligibility_b.s)

Action: substr replace both. No ASCII issue.

#### 2. enqueue_sprite_attr_with_xy_split (before L11400)
Stale refs:
- FUN_080432bc -> enqueue_zone_slot_sprite_attr_by_card_type   (04_card_zone_sprite.s)
- FUN_08043d90 -> scan_equip_chain_list_for_activation_sprite  (04_card_zone_sprite.s)
- FUN_08044e30 -> update_duel_field_slot_sprite_state          (04_card_zone_sprite.s, this seg)
- FUN_0805847c -> enqueue_equip_slot_sprite_with_field_bit_update (06_equip_eligibility_b.s)
- FUN_08058f90 -> tick_equip_lp_row19_sprite_display_seq       (06_equip_eligibility_b.s)

Action: substr replace all 5.

#### 3. enqueue_sprite_attr_with_shape (before L11423)
Stale refs:
- FUN_0804559c -> dispatch_card_effect_sprite_render_by_card_id (04_card_zone_sprite.s, this seg)
- FUN_0808e45c -> scan_trap_zone_slots_for_equip_shape_sprite  (11_effect_slot_puzzletext.s)
- FUN_0808e770 -> scan_effect_zones_for_equip_activation_forced_requisition (11_effect_slot_puzzletext.s)
- FUN_0808e85c -> scan_field_slots_for_equip_sprite            (11_effect_slot_puzzletext.s)

Action: substr replace all 4.

#### 4. enqueue_equip_set_slot_sprite_by_zone_col (before L11450)
Stale refs:
- FUN_080432bc -> enqueue_zone_slot_sprite_attr_by_card_type   (04_card_zone_sprite.s)
- FUN_08043d90 -> scan_equip_chain_list_for_activation_sprite  (04_card_zone_sprite.s)
- FUN_0808dc48 -> enqueue_relinquished_slot_sprite_attrs       (11_effect_slot_puzzletext.s)
- FUN_0808dd5c -> scan_field_for_equip_set_slot_sprite_update  (11_effect_slot_puzzletext.s)
- FUN_0808f2f0 -> enqueue_exchange_slot_sprite_attrs           (11_effect_slot_puzzletext.s)

Action: substr replace all 5.

#### 5. enqueue_effect_zone_pair_sprite_scan (before L11735)
Stale refs:
- FUN_08064760 -> dispatch_equip_sprite_update_by_card_type    (08_equip_oam_neodaed.s)
- FUN_0808db90 -> dispatch_equip_pair_sprites_by_state         (11_effect_slot_puzzletext.s)

Note: FUN_08064760 appears twice in this plate (same name, duplicate ref). Replace both instances.

Action: substr replace 2 unique addresses (both occurrences).

#### 6. dispatch_card_effect_sprite_render_by_card_id (before L11855)
Stale refs:
- FUN_08047218 -> handle_card_effect_zone_eligibility_by_field6 (04_card_zone_sprite.s)
- FUN_08047f50 -> render_slot_card_sprite_from_descriptor       (04_card_zone_sprite.s)
- FUN_08048020 -> render_slot_card_sprite_and_effects           (04_card_zone_sprite.s)
- FUN_08048364 -> render_slot_card_sprite_with_chaos_equip_check (04_card_zone_sprite.s)

Action: substr replace all 4.

Total PLATE actions: 6 functions, 20 FUN_ occurrences (18 unique + 2 dups), all substr replace.

---

## carve 计划 (R7)

None. No ROM_INCBIN or inter-function data blocks in this segment.

---

## disasm 计划 (R4)

None. No misidentified data blocks requiring disassembly.

---

## 新增 constants / 全局

### constants/oam_attr.inc  -- 6 new equates (pairs)
```
.equ OAM_XY_SPLIT_SPRITE_P1,   0x0000003a  @ xy-split sprite OAM attr1; player 1 (no H-flip); 2 pool refs
.equ OAM_XY_SPLIT_SPRITE_P2,   0x0000803a  @ xy-split sprite OAM attr1; player 2 (bit15=H-flip); 2 pool refs
.equ OAM_EQUIP_SET_SLOT_P1,    0x0000003b  @ equip-set slot sprite OAM attr1; player 1; inline imm
.equ OAM_EQUIP_SET_SLOT_P2,    0x0000803b  @ equip-set slot sprite OAM attr1; player 2; 2 pool refs
.equ OAM_EFFECT_CARD_SLOT_P1,  0x0000003c  @ effect-card slot sprite OAM attr1; player 1; inline imm
.equ OAM_EFFECT_CARD_SLOT_P2,  0x0000803c  @ effect-card slot sprite OAM attr1; player 2; 4 pool refs
```

### constants/ewram.inc  -- 2 new equates
```
.equ P1LP_EQUIP_BITMAP_CTR_OFF, 0x00001d3c  @ [gP1LP+player*PLAYER_BLOCK_STRIDE+0x1d3c] modulo-10 equip-slot bitmap anim frame counter; 6 ROM refs
.equ gEquipZoneCountTable,      0x0201e1c8  @ equip zone count tracking table base (EWRAM); 55 ROM refs
```

### constants/card_info.inc  -- 61 new CID equates
(57 named + 2 bare-CID renames for Pandemonium + Centrifugal Field, + 4 gap stubs;
 UMI_CARD_ID/ZOMBYRA_THE_DARK_CID/RAGING_FLAME_SPRITE_CID changed to REUSE;
 SPELL_ZONE_TARGET_CARD_ID changed to REUSE, removed from gap list)
See Group F + RENAME_SLOTS correction above.
Full list:
```
.equ SANGAN_CID,                       0x00000fd6  @ Sangan (26202165)
.equ upd_cid_10c6,                     0x000010c6  @ card gap; no card-stats entry
.equ BLACK_PENDANT_CID,                0x000010dd  @ Black Pendant (65169794)
@ UMI_CARD_ID = 0x000010f4 already in card_info.inc -- REUSE
.equ GODDESS_OF_WHIM_CID,              0x00001153  @ Goddess of Whim (67959180)
.equ COCKROACH_KNIGHT_CID,             0x00001185  @ Cockroach Knight (33413638)
.equ WITCH_OF_THE_BLACK_FOREST_CID,    0x000011e4  @ Witch of the Black Forest (78010363)
.equ upd_cid_120e,                     0x0000120e  @ card gap; no card-stats entry
.equ JINZO_CID,                        0x00001296  @ Jinzo (77585513)
.equ SATELLITE_CANNON_CID,             0x000012ac  @ Satellite Cannon (50400231)
.equ COPYCAT_CID,                      0x000012bb  @ Copycat (26376390)
.equ GIANT_RAT_CID,                    0x00001333  @ Giant Rat (97017120)
.equ KARATE_MAN_CID,                   0x00001337  @ Karate Man (23289281)
.equ NIMBLE_MOMONGA_CID,               0x0000133a  @ Nimble Momonga (22567609)
.equ SHINING_ANGEL_CID,                0x0000133c  @ Shining Angel (95956346)
.equ MYSTIC_TOMATO_CID,                0x00001342  @ Mystic Tomato (83011277)
@ SPELL_ZONE_TARGET_CARD_ID = 0x00001368 already in card_info.inc -- REUSE (not a gap CID)
.equ MUCUS_YOLK_CID,                   0x000013b2  @ Mucus Yolk (70307656)
.equ upd_cid_13e9,                     0x000013e9  @ card gap; no card-stats entry
.equ TORNADO_WALL_CID,                 0x000013f7  @ Tornado Wall (18605135)
@ ZOMBYRA_THE_DARK_CID = 0x0000147d already in card_info.inc -- REUSE
.equ THE_EMPERORS_HOLIDAY_CID,         0x00001495  @ The Emperor Holiday (68400115)
.equ AMAZONESS_CHAIN_MASTER_CID,       0x000014ab  @ Amazoness Chain Master (29654737)
.equ AGIDO_CID,                        0x000014f6  @ Agido (16135253)
.equ DARK_COFFIN_CID,                  0x00001544  @ Dark Coffin (01804528)
.equ LORD_POISON_CID,                  0x0000156d  @ Lord Poison (40320754)
.equ YOMI_SHIP_CID,                    0x00001591  @ Yomi Ship (51534754)
.equ COBRA_JAR_CID,                    0x00001595  @ Cobra Jar (86801871)
.equ GRANADORA_CID,                    0x0000163f  @ Granadora (13944422)
.equ OJAMA_TRIO_CID,                   0x0000166a  @ Ojama Trio (29843091)
.equ upd_cid_1672,                     0x00001672  @ card gap; no card-stats entry
.equ GREAT_MAJU_GARZETT_CID,           0x00001688  @ Great Maju Garzett (47942531)
.equ PANDEMONIUM_CID,                  0x0000169f  @ Pandemonium (94585852)
.equ SILPHEED_CID,                     0x000016c8  @ Silpheed (73001017)
.equ FUHMA_SHURIKEN_CID,               0x000016cc  @ Fuhma Shuriken (09373534)
.equ TOWER_OF_BABEL_CID,               0x000016de  @ Tower of Babel (94256039)
.equ BURNING_ALGAE_CID,                0x000016f5  @ Burning Algae (41859700)
.equ EMES_THE_INFINITY_CID,            0x0000172b  @ Emes the Infinity (43580269)
.equ EMISSARY_OF_THE_AFTERLIFE_CID,    0x00001796  @ Emissary of the Afterlife (75043725)
.equ FAMILIAR_KNIGHT_CID,              0x000017c3  @ Familiar Knight (89731911)
.equ MASKED_DRAGON_CID,                0x000017e6  @ Masked Dragon (39191307)
.equ NINJITSU_ART_OF_DECOY_CID,        0x000017ff  @ Ninjitsu Art of Decoy (89628781)
.equ SILENT_MAGICIAN_LV8_CID,          0x0000181a  @ Silent Magician LV8 (72443568)
@ RAGING_FLAME_SPRITE_CID = 0x0000182d already in card_info.inc -- REUSE
.equ GAIA_SOUL_CID,                    0x00001835  @ Gaia Soul the Combustible Collective (51355346)
.equ MOKEY_MOKEY_KING_CID,             0x0000183d  @ Mokey Mokey King (13803864)
.equ NECKLACE_OF_COMMAND_CID,          0x00001841  @ Necklace of Command (48576971)
.equ XING_ZHEN_HU_CID,                 0x0000184a  @ Xing Zhen Hu (76515293)
.equ SACRED_PHOENIX_CID,               0x0000185c  @ Sacred Phoenix of Nephthys (61441708)
.equ MECHA_DOG_MARRON_CID,             0x00001869  @ Mecha-Dog Marron (94667532)
.equ FIREBIRD_CID,                     0x00001875  @ Firebird (87473172)
.equ CENTRIFUGAL_FIELD_CID,            0x0000187f  @ Centrifugal Field (01801154)
.equ MILLENNIUM_SCORPION_CID,          0x000018ae  @ Millennium Scorpion (82482194)
.equ CRIOSPHINX_CID,                   0x000018b2  @ Criosphinx (18654201)
.equ MEGAROCK_DRAGON_CID,              0x000018b4  @ Megarock Dragon (71544954)
.equ DD_SURVIVOR_CID,                  0x000018bc  @ D.D. Survivor (48092532)
.equ NITRO_UNIT_CID,                   0x000018d1  @ Nitro Unit (23842445)
.equ KOZAKYS_SELF_DESTRUCT_CID,        0x000018d7  @ Kozaky's Self-Destruct Button (21908319)
.equ UFOROID_CID,                      0x000018f4  @ UFOroid (07602840)
.equ UFOROID_FIGHTER_CID,              0x000018fb  @ UFOroid Fighter (32752319)
.equ GIANT_KOZAKY_CID,                 0x00001914  @ Giant Kozaky (58185394)
.equ OJAMAGIC_CID,                     0x00001946  @ Ojamagic (24643836)
.equ WHITE_HORNS_DRAGON_CID,           0x00001996  @ White Horns D. (73891874)
.equ RAVIEL_LORD_CID,                  0x000019a5  @ Raviel, Lord of Phantasms (69890967)
.equ GOKIPON_CID,                      0x000019c5  @ Gokipon (14472500)
.equ HELIOS_TRIS_MEGISTE_CID,          0x000019f8  @ Helios Tris Megiste (17286057)
```

### constants/duel_field.inc  -- 1 new equate
```
.equ EQUIP_CHAIN_SENTINEL,      0xffff0000  @ gEquipChainSlotRefs list terminator sentinel; 3 pool refs in Seg-8a
```

---

## §5.1 登记 (Rule 3) -- 0 引用块

None. No ROM_INCBIN or .byte blocks exist in this segment. Rule 3 not applicable.

---

## 消费者证据 (R6) -- 关键槽语义

| 槽 | value | 证据 file:line | 置信度 |
|----|-------|---------------|--------|
| 0x080450d4/0x08045218 | 0x1d3c | asm/04_card_zone_sprite.s L11213,L11377: ldr rN,[base+stride+0x1d3c]; add 1; cmp 9; blt wrap; bl enqueue_equip_slot_bitmap_update | high |
| 0x08045528 | 0x0201e1c8 | asm/04_card_zone_sprite.s L11787: ldr r7,DAT_08045528; used as array base in slot loop | high |
| 0x08045524 | 0x10f4 (UMI_CARD_ID REUSE) | asm/04_card_zone_sprite.s L11744-L11746: ldr r5,DAT_08045524; adds r0,r5,#0; bl check_card_matches_active_effect_slot -> r5=CID arg | high |
| 0x08045efc | 0x08045531 | asm/04_card_zone_sprite.s L13239: .word 0x08045531; apply_nitro_unit_equip_activation is at 0x08045530; 0x08045531=addr+1 THUMB ptr | high |
| 0x08045594 | 0xc6880000 | asm/04_card_zone_sprite.s L11849: loaded, lsl/lsr with slot_word to check low13 == 0x18d1 (NITRO_UNIT_CID) | high |
| 0x08045598 | 0x2c4e18d1 | asm/04_card_zone_sprite.s L11851: composite used in cmp/beq activation path for Nitro Unit | med |
| 0x08045a94/0xbe8/0xc54 | 0xffff0000 | asm/04_card_zone_sprite.s L12617,L12821,L12880: ldr rN,[sentinel_slot]; cmp rval,rN; beq exit_loop | high |
| 0x080454bc | 0x101 | asm/04_card_zone_sprite.s L11722-L11723: ldr r3,DAT_080454bc; bl enqueue_sprite_attr_record -> r3=extra param | med |

---

## 求助

1. **Composite packed activation values** (0x2c4e18d1, 0x012a169f, 0x002a169f, 0x012a187f,
   0x002a187f, 0x364d0000, 0x2c200000, 0x36200000): upper 16-bit activation context fields
   partially decoded (card_id in low 13 bits confirmed; bits [28:13] = activation context type).
   Full bit-field naming requires reading check_equip_activation_eligible or
   apply_equip_activation_with_id_lookup internals. Current proposal uses partial EOL.
   Confidence: med. Request fixer to accept partial EOL or flag for deeper analysis.

2. **0x080454bc = 0x101**: r3 param to enqueue_sprite_attr_record. Exact semantics of
   the 4th argument ("extra" field) in enqueue_sprite_attr_record is not decoded in this
   segment. Proposed name EQUIP_PAIR_SPRITE_EXTRA is functional description only.
   Confidence: med. Accept with EOL or defer to when enqueue_sprite_attr_record is decoded.

---

## Coverage check (C13)

Total slots in [0x08044e30, 0x0804640c): **143**

Breakdown:
- EQ_SLOTS: PLAYER_BLOCK_STRIDE x11 + OAM x8 + offsets x9 + sentinel x3 + 0x101 x1 + CIDs x78 = **110**
- REF_SLOTS: gDuelFieldSlots x6 + gDuelFieldSlots_p2_base x2 + gEquipChainSlotRefs x7 + gEquipZoneCountTable x1 + gEquipNodePool x1 + fn-ptr x1 = **18**
- RENAME_SLOTS: composites x9 (0x2c4e18d1/0xc6880000/0x364d0000/0x012a169f/0x002a169f/0x012a187f/0x002a187f/0x2c200000/0x36200000) = **9**
  + 0x08045db8 (PANDEMONIUM_CID) and 0x08045e44 (CENTRIFUGAL_FIELD_CID) reclassified as EQ = **+2 EQ**

Final:
- EQ: 110 + 2 = **112**
- REF: **18**
- RENAME: **9**
- PLATE: **6** functions
- Total covered: 112 + 18 + 9 = **139**

Wait: 139 != 143. Recount:

Missing 4 slots. Let me enumerate uncovered:

Checking group sizes again:
- PLAYER_BLOCK_STRIDE (Group A): 11 slots
- OAM P2 (Group B): 8 slots (only P2 values appear as pool entries)
- Offsets (Group C): 9 slots (3x 0x1ce8 + 2x 0x1cf4 + 2x 0x10d0 + 2x 0x1d3c)
- Sentinel (Group D): 3 slots
- 0x101 (Group E): 1 slot
- CIDs from Group F: 78 slots (need exact count from table above)
- PANDEMONIUM_CID (0x08045db8): 1 slot -> EQ
- CENTRIFUGAL_FIELD_CID (0x08045e44): 1 slot -> EQ
Subtotal EQ: 11+8+9+3+1+78+1+1 = 112

CID count from Group F table: let me count rows...
Slots with CID values (Group F, excluding 0x08045db8 PANDEMONIUM and 0x08045e44 CENTRIFUGAL
which are separate):
Row count in table: 78 rows listed. Verify:
Rows listed in CID table above total = 78 entries covering 78 unique slot addresses.

REF (Group G + H): 17+1 = 18 slots

RENAME composites:
0x08045594, 0x08045598, 0x08045db4, 0x08045dbc, 0x08045e38, 0x08045e48, 0x08045eec, 0x080463d4, 0x08046408
= 9 slots

112 + 18 + 9 = 139. Total = 143. Difference = 4.

The 4 uncounted slots are the PANDEMONIUM and CENTRIFUGAL plain-CID slots plus 2 others.
Already counted PANDEMONIUM (0x08045db8) and CENTRIFUGAL (0x08045e44) in EQ (+2).
That gives 112 + 18 + 9 = 139. Still 4 short.

Additional uncovered slots identified in full slot list not yet assigned:
- gEquipNodePool slot count: listed 1 (0x08045d08) -- check gEquipChainSlotRefs count

Re-examining REF group: gEquipChainSlotRefs x7 = 7 slots.
Listed: 0x080459fc, 0x08045a34, 0x08045af8, 0x08045b2c, 0x080461bc, 0x0804623c, 0x080462a0 = 7 OK.

Let me check against the complete slot list for unassigned entries:
Complete slot list has 143 entries.
After assigning all groups, verify no slot is double-counted or missed.

EQ Group A (PLAYER_BLOCK_STRIDE x11): covers slots with value=0x868.
From complete list: 0x08044ed0, 0x0804516c, 0x080451a8, 0x080452dc, 0x080453f4, 0x08045488,
  0x0804558c, 0x08045bf0, 0x08045c60, 0x08045e3c, 0x08045ef0 = 11 confirmed.

EQ Group B (OAM x8): 0x08045264, 0x08045294, 0x080452e4, 0x08045310, 0x080453fc, 0x08045438,
  0x08045490, 0x080454b8 = 8 confirmed.

EQ Group C (offsets x9): 0x08045408, 0x080460e0, 0x08046150 (0x1ce8 x3) +
  0x080460e4, 0x08046154 (0x1cf4 x2) + 0x08045a9c, 0x08045c5c (0x10d0 x2) +
  0x080450d4, 0x08045218 (0x1d3c x2) = 9 confirmed.

EQ Group D (sentinel x3): 0x08045a94, 0x08045be8, 0x08045c54 = 3 confirmed.

EQ Group E (0x101 x1): 0x080454bc = 1 confirmed.

EQ bare-CID for Pandemonium and Centrifugal: 0x08045db8, 0x08045e44 = 2.

CID Group F: 78 slots.
Let me count from the CID table rows above:
1. 0x08044ed4 (0x1645) ... 2. 0x08044ed8 ... 3. 0x08044edc ... 4. 0x08044ee0 ...
5. 0x08044ef0 ... 6. 0x08044f14 ... 7. 0x08044f30 ... 8. 0x08044f38 ...
9. 0x08044f60 ... 10. 0x08044f70 ... 11. 0x08044f8c ... 12. 0x08044fa4 ...
13. 0x08044fd8 ... 14. 0x08044fdc ... 15. 0x08044fec ... 16. 0x08045008 ...
17. 0x08045020 ... 18. 0x08045028 ... 19. 0x0804504c ... 20. 0x08045064 ...
21. 0x08045070 ... 22. 0x0804508c ... 23. 0x080450a8 ... 24. 0x080451c4 ...
25. 0x080451dc ... 26. 0x080451e0 ... 27. 0x080451ec ... 28. 0x08045400 ...
29. 0x0804540c ... 30. 0x08045410 ... 31. 0x08045524 ... 32. 0x0804552c ...
33. 0x08045658 ... 34. 0x0804565c ... 35. 0x08045660 ... 36. 0x08045668 ...
37. 0x0804568c ... 38. 0x080456a4 ... 39. 0x080456d0 ... 40. 0x080456e0 ...
41. 0x080456f8 ... 42. 0x08045724 ... 43. 0x0804572c ... 44. 0x08045748 ...
45. 0x08045758 ... 46. 0x08045780 ... 47. 0x08045798 ... 48. 0x080457b0 ...
49. 0x080457c8 ... 50. 0x08045800 ... 51. 0x08045804 ... 52. 0x08045814 ...
53. 0x08045834 ... 54. 0x0804583c ... 55. 0x0804586c ... 56. 0x08045884 ...
57. 0x080458a4 ... 58. 0x080458b4 ... 59. 0x080458e8 ... 60. 0x080458f8 ...
61. 0x08045914 ... 62. 0x08045924 ... 63. 0x08045950 ... 64. 0x08045964 ...
65. 0x08045988 ... 66. 0x080459a0 ... 67. 0x08045ef8 ... 68. 0x08045f00 ...
69. 0x08045f04 ... 70. 0x08045f18 ... 71. 0x08045f38 ... 72. 0x08045f3c ...
73. 0x08045f40 ... 74. 0x08045f68 ... 75. 0x08045fc4 ... 76. 0x08045fe0 ...
77. 0x08046234 ... 78. 0x08046238 ... 79. 0x0804629c ... 80. 0x08046364 ...
81. 0x08046368 ... 82. 0x0804636c

= 82 CID slots in Group F table. (Not 78 as stated above.)

Corrected total: 11+8+9+3+1+82+2 (Group F) + 18 (REF) + 9 (RENAME) = 143. CHECK: 143 = 143. PASS.

Corrected summary:
- EQ: 11 + 8 + 9 + 3 + 1 + 82 + 2 = **116**
- REF: **18**
- RENAME: **9**
- Total: 116 + 18 + 9 = **143** PASS

---

## Executor Report: 04-Seg-8a

- 槽: EQ=116  REF=18  RENAME=9  FUNC_RENAME=0  PLATE=6
- carve=0  disasm=0  §5.1=0
- 新增 constants/全局:
  - oam_attr.inc: OAM_XY_SPLIT_SPRITE_P1/P2, OAM_EQUIP_SET_SLOT_P1/P2, OAM_EFFECT_CARD_SLOT_P1/P2 (6 new)
  - ewram.inc: P1LP_EQUIP_BITMAP_CTR_OFF=0x1d3c, gEquipZoneCountTable=0x0201e1c8 (2 new)
  - duel_field.inc: EQUIP_CHAIN_SENTINEL=0xffff0000 (1 new)
  - card_info.inc: 61 new CID equates (57 named + 2 bare-CID renames for Pandemonium/Centrifugal + 4 gap stubs; UMI_CARD_ID/ZOMBYRA_THE_DARK_CID/RAGING_FLAME_SPRITE_CID/SPELL_ZONE_TARGET_CARD_ID changed to REUSE)
- 求助: med-conf partial decode for 9 composite packed activation values; med-conf for 0x101 EQUIP_PAIR_SPRITE_EXTRA 4th-arg semantics
- proposal: doc/dev/refine/04-Seg-8a.proposal.md
