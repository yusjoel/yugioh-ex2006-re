# 函数/数据细化计划 — `asm/05_equip_eligibility_a.s`

> 阶段目标: 把 `asm/05_equip_eligibility_a.s` (ROM `0x08049014 ~ 0x080537C0`, 装备槽资格检查
> `check_equip_slot_eligible_*` 簇 + 效果区 LP/shape sprite 提交 + 卡字段查询 + switch 派发)
> **逐段地址序细化完成**, 全程 byte-identical
> (`SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b`)。
>
> 这是 refine 第 **6** 个文件 (file 00 / 01 / 02 / 03 / 04 已全 10 段完成, 见对应
> `p5-refine-0N-*.md`)。方法论 + R1-R9 细化清单 + 三条硬规则见
> `doc/dev/methodology/refine-loop.md` 与 file 00 doc §一。

---

## 一、细化要求 (checklist)

沿用 file 00..04 doc §一 的 **R1-R9** (常量 equate / 灭自动名 / 引用接通 / 误标代码 disasm /
注释订正用现名 / 先读消费者 / 数据 carve 进 rom.s / 图形目视 / byte-identical+备份) +
**三条硬规则** (严格地址序 Seg-1..10 不回头 / 函数间 ROM_INCBIN 必 carve 或 §5.1 / 全 ROM 0 引用→§5.1)。

**R1-R9 详版**见 `doc/dev/p5-refine-00-system-str-vija.md` §一。

**跨文件踩坑沿用** (file 00..04 沉淀, 务必遵守):
- EQ_SLOT 的 Ghidra 槽 label 名 **必须 != `.equ` 常量名** (`<func>_<const>` 式) — memory `carve-eq-label-collision`。
- Ghidra EOL/plate **一律 ASCII** (含 CJK 会 Jython 双重 UTF-8 mojibake), 中文解释走 doc/。
- **槽地址精确性 (file 04 Seg-6/8 教训)**: 每个 DAT_/PTR_ 槽地址必须用 python
  `struct.unpack_from('<I', rom, rom_addr-0x08000000)` 核对 ROM 字节值; executor 自报地址常有错,
  fixer 物化前 dry-run 暴露 WARN 即修正地址再实跑。
- **C5 按值去重不分语义域**: 新建常量前必扫全 constants/*.inc 确认无同值常量
  (file 04 反复抓到 UMI/ZOMBYRA/SPELL_ZONE_TARGET/RAGING_FLAME/TYRANT_DRAGON 等碰撞);
  REF/RENAME 不绕过已存在常量值; 不建孤儿常量 (段内无槽持该值)。
- **C13 残留 100% 覆盖**: 段内所有 DAT_/DWORD_/PTR_ 须被 EQ+REF+RENAME 去重全覆盖; executor 必
  python 精确清点段内 .word 槽总数 (file 04 反复漏数), 勿留"低优先级不处理"。
- **C8 stale 函数名**: plate 中 `FUN_xxxx`/`PTR_FUN_xxxx` **完整字符串**匹配替换现名 (禁子串);
  **含 CJK 全文的旧 plate 必须整段 ASCII 重写** (substring 替换对 CJK plate 静默 no-op, file 04 Seg-5/6 踩坑);
  整段 setPlateComment 重写, 落地后 grep 段范围 FUN_ == 0 + 无 CJK 验收。
- **卡牌 ID 常量 (file 02/03/04 教训)**: 命名前必查 `data/card-stats.s` 坐实 passcode→slot_id→卡名;
  slot_id 范围内未分配的值 → 中性 `<func>_cid_<hex>` 低置信 RENAME, 勿臆造卡名 (红线 3); pw 注释取正确 passcode;
  plate 卡名与 card-stats.s 矛盾即**命名期误名信号** (file 04 Seg-9 订正 0x1814 All-Seeing→Silent Swordsman LV5)。
- **packed/bitfield 值部分解码**: 单个 packed 32-bit 值语义不明 → 中性 RENAME 标签 + med/low-conf EOL
  记录字节分解 (high16/low16), **不臆造完整位域语义, 不 BLOCK 整段** (file 04 Seg-8a/10 范式)。
- **switch 跳转表 (file 05 新特征)**: 段内 `switchD_*`/`switchdataD_*` Ghidra 自动名是 switch 派发数据块;
  jump table 目标存裸 THUMB 地址 (R4 disasm 跳转表逐 stub) 或字节偏移表; carve/disasm 处理参 file 00 Seg-5c。
- **fn-ptr +1 永久踩坑**: Ghidra 把 THUMB fn-ptr 数据 ref 导出为偶地址, build diff 差 1 字节; 手改 `.word <fn>+1`。
  每次 re-export 后须重补。已知周期性修复槽 (跨文件累积):
  asm/03: 0x37884 / 0x389dc / 0x389f8 / 0x3aa74;
  asm/04: 0x40ab4 (zone_monster_field_bonus_table+7*16) / 0x42638 (tick_draw_card_switch_table) /
          0x45efc (apply_nitro_unit_equip_activation+1) / 0x478f0 (gDuelFieldSlots+EFFECT_ZONE_PARTITION_OFF)。
  file 05 若出现新 fn-ptr 槽同样处理。
- 复用 file 00..04 已建 constants/*.inc 与 carve label (见下方资产清单)。

**file 02/03/04 已建可复用资产** (新建前必 grep 确认无同值):
- `ewram.inc`: gDuelFieldSlots=0x0201c510 / gEquipNodePool=0x0201d9c0 / gEquipChainSlotRefs /
  gDuelFieldSlotState / gDuelEffectChainSlots=0x0201bcc0 / PLAYER_BLOCK_STRIDE=0x868 /
  gP1SlotCountBase / gP1SlotSetCodeArray / gP1HandCountBase / gP1HandSlotArray /
  gDuelFieldSlots_p2_base=0x0201c5d8 / gDuelFieldSpellZoneBase=0x0201c5ec / gP1FieldArrayCBase=0x0201c600 /
  gEffectEntryArray=0x0201b590 / gDuelDisplaySeqState=0x0201bcc0 / gSpriteAttrBuf=0x0201b870 /
  gDuelChainStepCounter=0x0201c4d0 / gDuelChainDescBase=0x0201c4d8 / gDuelCardCtxBase=0x0201e2a0 /
  gEquipChainEntryBase=0x0201e288 / gEquipZoneCountTable=0x0201e1c8 / P1LP_BACKUP_DST_OFF=0x1cf0 /
  LP_CARD_TRACK_BASE_OFF=0x1da8 / LP_CARD_TRACK_NEXT_OFF=0x1daa / LP_CARD_TRACK_AUX_OFF=0x1db2 /
  P1LP_EQUIP_BITMAP_CTR_OFF=0x1d3c / LP_DISCARD_ZONE_OFF
- `duel_field.inc`: 众多 *_OFF 字段偏移 + SLOT_*_CLR 位清除掩码 (file 02/03/04 累积 ~80+ 项);
  EQUIP_MAIN_PHASE_OFF=0x1d18 / DISP_SET_VARIANT_OFF=0x1cfc / SET_DISPLAY_STATE_SLOT_OFF=0x894 /
  HAND_SLOT_FACE_ARRAY_OFF=0x41a / ALT_HAND_SLOT_FACE_ARRAY_OFF=0x5d2 / EQUIP_CHAIN_STEP_BASE_OFF /
  EQUIP_MULTI_SLOT_CTL_OFF=0x1ce0 / EQUIP_CHAIN_SENTINEL=0xffff0000 / EQUIP_BITMAP_CTRL_OFF /
  FIELD_COPY_COUNT_FLAG=0x10002 / EQUIP_ZONE_EFFECT_ATTR_OR=0x1e501511 (file 04 Seg-10 low-conf) /
  EQUIP_SLOT_ACTIVE_TAG=0xa5600000 / FIELD_SLOT_COUNT_OFF=0x1cb4 / SLOT_FACE_STATUS_ARRAY_OFF=0x10b1 等
- `card_info.inc`: SLOT_CARD_SET_CODE_MASK=0x00001fff + file 01..04 已建 **~250+ CID 常量**
  (复用前必 grep card_info.inc; file 04 单文件新增 ~130 CID)
- `oam_attr.inc`: OAM_ATTR0_HIDDEN=0x0000ffff / OAM_ATTR1_X_CLEAR / OAM_ATTR2_TILE_CLEAR=0xffffe000 /
  众多 OAM_*_SPRITE_P1/P2 调色板选择子 (0x80xx 系列, file 04 累积 ~30 项) /
  OAM_SPRITE_ATTR_CLR_BIT* / OAM_SPRITE_ATTR_CLR_BITS* 位清除掩码 (file 04 累积)
- `bitops.inc`: 8 POPCOUNT_MASK_*
- 全局: gVijaState=0x02029eb0 / gDemoState=0x02029ec0 / gDuelSceneBase=0x02023360 /
  gDuelCardCtxBase=0x0201e2a0 / gDuelDispCtx=0x0203eeb0
- 跨文件 caller hub: `dispatch_duel_event_display_seq` (0x0803be4c, file 03 Seg-7) — tick_*_display_seq 的 bl 目标 + plate 引用 (C8 高频)。

---

## 二、落地工作流 (pipeline)

同 file 00..04 doc §二「代码侧 pipeline」:
```
备份 .rep → Ghidra 脚本 (RefineF05Seg<N>*.py: equate/label/ref/rename/plate/disasm)
→ ghidra-export-range.bat 080000c0 084c7637 → inject_modes.py → split_all_s.py
→ build + byte-identical SHA1 9689337d → (改函数名才) ExportFunctionInventory + sync CSV → commit
```
3-agent: executor (proposal) → reviewer (C1-C13 review) → fixer (模式A改proposal / 模式B落地)。
重段 (>~150 槽) 按函数边界拆 Seg-Na/Nb (地址序不回头)。

---

## 三、当前进度 (05_equip_eligibility_a.s)

| Seg | 范围 | ~fn | ~slots | 内含 ROM_INCBIN | 状态 | commit |
|-----|------|-----|--------|-----------------|------|--------|
| 1 | 0x49014..0x4a5b8 | 24 | 152 | — | ✅ | 6dd6fec |
| 2 | 0x4a5b8..0x4ad48 | 24 | 68 | — | ✅ | 68c1e28 |
| 3 | 0x4ad48..0x4b4f4 | 24+5 | 73 | 3 disasm blocks | ✅ | bd9ce13 |
| 4a | 0x4b4f4..0x4be38 | 10 | 101 | — | ✅ | — |
| 4b | 0x4be38..0x4c6e8 | ~14 | ~99 | — | ✅ | 8a924b3 |
| 5 | 0x4c6e8..0x4d124 | 7 | 75 | 3 orphan | ✅ | 20cbc8b |
| 6 | 0x4d124..0x4ffba | 24 | 128 | 5 disasm blocks | ✅ | pending |
| 7 | 0x4ffba..0x50e40 | 24 | 73 | — | ⬜ | — |
| 8 | 0x50e40..0x51cc4 | 24 | 83 | — | ⬜ | — |
| 9 | 0x51cc4..0x52df8 | 24 | 117 | — | ⬜ | — |
| 10 | 0x52df8..0x537c0 | 23 | 51 | — | ⬜ | — |

图例: ✅ 完成 / 🟡 进行中 / ⬜ 未开始。
重段提示: Seg-4 (200 槽, switch 派发 + check_card_is_equip_set 簇) / Seg-1 (152 槽, sprite 提交簇) /
Seg-6 (128 槽) / Seg-9 (117 槽) 较重, 必要时拆 Seg-Na/Nb (地址序边界=函数结束处, 不回头)。
switchD_/switchdataD_ 自动名 (Seg-2/4/5/6 含) 是 switch 派发数据块, 按 file 00 Seg-5c R4 disasm 范式处理。

---

## 四、逐段完成记录

(各段落地后由 fixer 追加 4.0N 小节: 函数列表 / 符号化统计 / 新建 constants / carve / 踩坑 / commit)

### 4.01 Seg-1 完成记录 (0x08049014..0x0804a5b8, 24 fn, 152 slots)

**函数列表 (24)**:
submit_effect_zone_lp_and_shape_sprites / tick_duel_field_zone_sprite_update_pipeline /
tick_zone_sprite_pipeline_with_update_flag / enqueue_slot_sprite_attr_by_player /
enqueue_equip_zone_sprite_attr_full / render_spell_zone_card_sprite_with_id_tree /
render_pair_zone_sprites_if_field_card_present / render_spell_zone_sprite_with_field_copy_check /
render_matched_pair_zone_sprites / enqueue_equip_zone_sprite_with_mode /
enqueue_pair_zone_sprite_attr_by_card_id / enqueue_effect_slot_sprites_descending /
enqueue_equip_slot_sprite_with_card_check / submit_equip_slot_sprite_zone11 /
enqueue_equip_slot_sprite_zone13 / enqueue_equip_slot_sprite_zone12 /
render_monster_slot_card_with_lp_bar / enqueue_sprite_attr_type11 /
enqueue_sprite_attr_with_type_select / check_zone_eligible_with_deck_flag /
enqueue_lp_field_state_sprite_by_player / enqueue_lp_counter_sprite_by_player /
enqueue_duel_field_card_slot_sprite / enqueue_sprite_attr_for_card_slot

**符号化统计**: EQ=99 / REF=14 / RENAME=39 / FUNC_RENAME=0 / PLATE=33 fn_subs

**新建 constants**:
- card_info.inc +16 CID (PENGUIN_KNIGHT / BAD_REACTION_TO_SIMOCHI / HIROS_SHADOW_SCOUT /
  CRUSH_CARD / APPROPRIATE / PROTECTOR_OF_THE_SANCTUARY / HEART_OF_THE_UNDERDOG /
  REGENERATING_MUMMY / GREED / PETEN_THE_DARK_CLOWN / DECK_DEVASTATION_VIRUS /
  PIKERU_SECOND_SIGHT / CYBER_ARCHFIEND / BUBBLE_ILLUSION / DANDYLION / KAISER_GLIDER)
- oam_attr.inc +21 (10 P1/P2 tile attr0 pairs + OAM_CARD_SLOT_SPRITE + 3 CLR masks + 4 ATTR2_OR)

**carve**: 0 (no ROM_INCBIN in this segment)

**踩坑**: fn-ptr +1 periodic fix (7 slots in asm/03 x4 + asm/04 x3) after re-export; all recovered

**byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b

**plate FUN_ residual**: 4 instances remain in plates; all are cross-references to functions in
other segments (0x08073d84, 0x0806d960, 0x08049e44, 0x080718c4) not in Seg-1 mapping list;
will be resolved when those segments are refined.

**commit**: 6dd6fec

### 4.02 Seg-2 完成记录 (0x0804a5b8..0x0804ad48, 12 fn, 68 slots)

**函数列表 (12)**:
enqueue_monster_zone_equip_sprites_and_lp_counters /
enqueue_sprite_attr_type10_halfword /
increment_lp_bar_display_counter /
increment_lp_bar_counter_no_player /
decrement_lp_bar_display_counter /
set_slot_occupy_bit_with_sprite_update /
set_player_state_bit_with_sprite_update /
set_field_slot_bit_with_sprite_update /
map_field8_to_card_type_category (contains switchD_0804a9ee) /
check_card_pair_allowed /
map_card_id_to_banlist_canonical /
check_card_ids_banlist_compatible

**符号化统计**: EQ=33 / REF=1 / card_id_EQ=34 / FUNC_RENAME=0 / PLATE=4 subs (3 fn)

**新建 constants**:
- ewram.inc +2 (LP_BAR_DISPLAY_CTR_OFF=0x4c4 / LP_BAR_ANIM_STATE_OFF=0x4cc)
- duel_field.inc +2 (EQUIP_SPRITE_X_DELTA_A=0xffffe730 / EQUIP_SPRITE_X_DELTA_B=0xffffe32c)
- oam_attr.inc +2 (OAM_PLAYER_STATE_BIT_SPRITE_P1=0x8022 / OAM_FIELD_SLOT_BIT_SPRITE_P1=0x802a)
- card_info.inc +5 (POLYMERIZATION_CID_1303 / CYBER_HARPIE_LADY_CID / HARPIE_LADY_1_CID / HARPIE_LADY_3_CID / BEWD_RANGE_CHECK_BIAS)

**carve**: 0 (no fn-ptr ROM_INCBIN in this segment; §5.1 orphan block 0x4aa5e/0xee)

**plate FUN_ residual after landing**: 0 stale FUN_ in Seg-2 range (grep confirmed)

**踩坑**: fn-ptr +1 periodic fix -- asm/03 x4 (eval_equip_bonus_for_slot_pred_fn / eval_amazoness_fnptr_a / eval_amazoness_fnptr_b / eval_equip_chain_pred_fnptr) + asm/04 x3 (tick_equip_scan_destiny_chain_table now +7*16 / dat_08045efc_fnptr +1 / upd_equip_bitmap_effect_zone gP1LifePoints+EQUIP_BITMAP_CTRL_OFF fix) after re-export

**byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b

**commit**: 68c1e28

### 4.04a Seg-4a 完成记录 (0x0804b4f4..0x0804be38, 10 fn, 101 slots)

**函数列表 (10)**:
get_card_field_summon_restriction / get_card_special_group_code /
check_card_has_equip_placement_type / check_card_not_equip_placement_type /
check_card_id_is_special_tribute_group / check_card_is_equip_target_eligible /
check_card_id_is_equip_excluded_range / get_card_equip_zone_rank /
check_card_id_is_equip_set_a / (get_card_effect_category = Seg-4b start)

**符号化统计**: EQ=95 / RENAME=6 / SCALAR_EQ=5 / FUNC_RENAME=0 / REF=0 / PLATE=0

**新建 constants** (card_info.inc +68):
- 63 B-class CID: HARPIE_LADY_SISTERS / PERFECTLY_ULTIMATE_GREAT_MOTH / MASK_OF_DARKNESS /
  PRINCESS_OF_TSURUGI / WALL_SHADOW / SUIJIN / METALZOA / MAGICIAN_OF_FAITH / HANE_HANE /
  NEEDLE_WORM / MORPHING_JAR / INVADER_OF_THE_THRONE / RED_EYES_BLACK_METAL_DRAGON /
  THE_FIEND_MEGACYBER / GERM_INFECTION / STIM_PACK / BUBONIC_VERMIN /
  VALKYRION_THE_MAGNA_WARRIOR / INJECTION_FAIRY_LILY / SONIC_JAMMER /
  FOUR_STARRED_LADYBUG_OF_DOOM / SUMMONER_OF_ILLUSIONS / GILASAURUS / TORNADO_BIRD /
  MARYOKUTAI / EKIBYO_DRAKMORD / DICE_JAR / FUSHIOH_RICHIE / A_CAT_OF_ILL_OMEN /
  DIFFERENT_DIMENSION_CAPSULE / XY_DRAGON_CANNON / OLD_VINDICTIVE_MAGICIAN /
  MAGICAL_PLANT_MANDRAGOLA / MAGICAL_MERCHANT / GUARDIAN_GRARL / IRON_BLACKSMITH_KOTETSU /
  FINAL_COUNTDOWN / WITCH_DOCTOR_OF_CHAOS / CHAOS_SORCERER / BLACK_LUSTER_SOLDIER_ENVOY /
  ARCHLORD_ZERATO / SKULL_DESCOVERY_KNIGHT / DESERTAPIR / RARE_METAL_DRAGON /
  SORCERER_OF_DARK_MAGIC / NOBLEMAN_EATER_BUG / THE_TRICKY / THE_BLOCKMAN /
  A_TEAM_TRAP_DISPOSAL_UNIT / SWORDS_OF_CONCEALING_LIGHT / VAMPIRE_GENESIS /
  ANCIENT_GEAR_BEAST / DUMMY_GOLEM / MASTER_MONK / ELEMENTAL_HERO_THUNDER_GIANT /
  CYBER_DRAGON / VWXYZ_DRAGON_CATAPULT_CANNON / FAMILIAR_POSSESSED_WYNN /
  DARK_ERADICATOR_WARLOCK / ELEMENTAL_HERO_STEAM_HEALER / ANCIENT_GEAR / PRINCESS_PIKERU /
  PRINCESS_CURRAN
- 3 inline CID: KURIBOH_CID=0xfe0 / PENGUIN_SOLDIER_CID=0x1200 / DARK_SNAKE_SYNDROME_CID=0x15a0
- 2 field6 type: CARD_FIELD6_EQUIP_CONTINUOUS=0x16 / CARD_FIELD6_EQUIP_RITUAL=0x17

**carve**: 0 (no ROM_INCBIN / inter-function data in this segment)

**scalar equate** (Ghidra inline operand): PENGUIN_SOLDIER_CID @ 0x4b5c0 / KURIBOH_CID @ 0x4bcd6 /
DARK_SNAKE_SYNDROME_CID @ 0x4bdfc / CARD_FIELD6_EQUIP_CONTINUOUS @ 0x4bca0 /
CARD_FIELD6_EQUIP_RITUAL @ 0x4bca4

**CJK grep in Seg-4a range**: 0 non-ASCII lines confirmed

**byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b

**commit**: 3155175

### 4.04b Seg-4b 完成记录 (0x0804be38..0x0804c6e8, 14 fn, 99 slots)

**函数列表 (14)**:
get_card_effect_category / check_card_id_is_equip_set_b /
check_card_id_is_equip_set_d / check_card_is_equip_set_c /
check_card_id_is_equip_blocker / check_card_id_is_equip_set_e /
check_card_id_is_equip_excluded_set_f / check_card_id_is_field_zone_special /
check_card_is_zone_pair_restricted / check_card_is_field_spell_type_b /
get_card_effect_zone_check_sides / check_card_id_is_equip_set_g /
classify_card_id_summon_category / get_paired_card_id_by_variant

**符号化统计**: EQ=89 / RENAME=10 / FUNC_RENAME=0 / REF=0 / PLATE=1 (classify_card_id_summon_category plate rewrite FUN_0803088c -> check_effect_slot_summon_path_eligible)

**新建 constants** (card_info.inc +57 new CIDs):
BEASTKING_OF_THE_SWAMPS / VERSAGO_THE_DESTROYER / MONSTER_EYE / THUNDER_DRAGON /
MYSTICAL_SHEEP_1 / MAGICAL_LABYRINTH / HANNIBAL_NECROMANCER / MESMERIC_CONTROL /
MONSTER_REBORN / POT_OF_GREED / ROYAL_DECREE / RESTRUCTER_REVOLUTION /
UPSTART_GOBLIN / DELINQUENT_DUO / THE_FORCEFUL_SENTRY / SPEAR_CRETIN /
DE_FUSION / JAR_OF_GREED / SPIRITUALISM / SPIRIT_MESSAGE_I / FUSION_GATE /
THE_WARRIOR_RETURNING_ALIVE / THE_DRAGONS_BEAD / GREAT_DEZARD / CARD_OF_SANCTITY /
MYSTICAL_KNIGHT_OF_JACKAL / SKILLED_WHITE_MAGICIAN / SKILLED_DARK_MAGICIAN /
ROYAL_MAGICAL_LIBRARY / JAR_ROBBER / MIRACLE_RESTORING / DESROOK_ARCHFIEND /
RAY_OF_HOPE / MATAZA_THE_ZAPPER / DEDICATION_THROUGH_LIGHT_DARK / THE_KICK_MAN /
CORPSE_OF_YATA_GARASU / ASWAN_APPARITION / NUBIAN_GUARD / KING_OF_THE_SWAMP /
CARD_7 / THE_SECOND_SARCOPHAGUS / THE_END_OF_ANUBIS / DARK_FACTORY_MASS_PROD /
CEMETARY_BOMB / BIG_CORE / BLAST_MAGICIAN / A_FEATHER_OF_THE_PHOENIX /
GOOD_GOBLIN_HOUSEKEEPING / CYBER_END_DRAGON / SPARK_BLASTER / DARK_RULER_VANDALGYON /
ALKANA_KNIGHT_JOKER / POT_OF_AVARICE / ROLL_OUT / MYTHICAL_BEAST_CERBERUS / MAGICAL_MALLET
(3 reuses not new: EQUIP_CHAIN_PAIR_CARD_MAX / HORUS_LV4 / D3S_FROG already existed)

**carve**: 0 (no inter-function ROM_INCBIN in segment)

**disasm**: 0

**fn-ptr periodic fix** (post re-export): asm/03 x4 (eval_equip_bonus_for_slot_pred_fn / eval_amazoness_fnptr_a / eval_amazoness_fnptr_b / eval_equip_chain_pred_fnptr) + asm/04 x3 (tick_equip_scan_destiny_chain_table zone_monster_field_bonus_table+7*16 / dat_08045efc_fnptr apply_nitro_unit_equip_activation+1 / upd_equip_bitmap_effect_zone gDuelFieldSlots+EFFECT_ZONE_PARTITION_OFF)

**plate FUN_ in Seg-4b range after landing**: 0 stale FUN_ (grep confirmed)

**CJK in Seg-4b range**: 0 non-ASCII bytes (grep confirmed)

**byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b

**Seg-4 (4a+4b) 全完成** (4a commit 3155175 + 4b this commit)

### 4.05 Seg-5 完成记录 (0x0804c6e8..0x0804d124, 7 fn body, 75 slots)

**函数列表 (7)**:
- submit_slot_card_sprite_row_entry (0x0804c76c)
- apply_equip_activation_with_id_lookup (0x0804c910)
- init_card_sprite_row_entry (0x0804c958)
- init_card_sprite_row_entry_alt (0x0804caf0)
- submit_slot_card_sprite_row_packed (0x0804cc8c)
- check_card_slot_activation_eligible (0x0804cdd8)
- dispatch_card_eligibility_state_machine (0x0804ce78; body spans into Seg-6 to 0x4d1d2)

Note: switchdataD_0804c6e8 (6-entry jump table for classify_card_id_summon_category caseD) + case stubs occupy 0x4c6e8..0x4c732 (segment prefix from Seg-4b function).

**符号化统计**: EQ=67 / REF=0 / RENAME=8 / FUNC_RENAME=0 / PLATE=0

**新建 constants**:
- card_info.inc +7 new CID: BUTTERFLY_DAGGER_ELMA_CID (0x165c) / GRAVITY_AXE_GRARL_CID (0x165e) / WICKED_BREAKING_FLAMBERGE_BAOU_CID (0x165f) / TWIN_SWORDS_FLASHING_LIGHT_TRYCE_CID (0x1661) / COCOON_OF_EVOLUTION_CID (0xfee) / SWORDS_OF_REVEALING_LIGHT_CID (0x1102) / METALMORPH_CID (0x1238)
- oam_attr.inc +2: OAM_ATTR2_CLR_BITS_11_6 (0xfffff03f) / SPRITE_ATTR_TYPE_HIDDEN_Y97 (0x8061)
- ewram.inc +9: SPRITE_ROW_ENTRY_DATA_OFF (0x4d4) / ELIGIB_STATE_OFF (0x574) / ELIGIB_RESULT_OFF (0x584) / ELIGIB_CARD_ID_OFF (0x1d44) / ELIGIB_STATE_CTRL_OFF (0x1d54) / ELIGIB_ACT_COUNT_OFF (0x1d58) / ELIGIB_ACT_TYPE_OFF (0x1d5c) / ELIGIB_SPRITE_CTRL_OFF (0x1d68) / ELIGIB_ANIM_STATE_OFF (0x1d6c)

**C5 碰撞处理**: ELIGIB_RESULT_OFF=0x584 与 duel_field.inc GPRNG_SCENE_CTX_DISPLAY_FLAG_OFF=0x584 数值碰撞; 用户裁定新建独立常量 (不同 base 寄存器/不同 EWRAM 结构体的字段偏移, 良性碰撞).

**carve**: 0 (无外部引用 ROM_INCBIN; 3 orphan 块全 §5.1)

**disasm**: 0 (orphan THUMB code 无外部 caller, §5.1 留待)

**§5.1 新增 3 孤儿块**:
- 0x0804c734 / 0x38 (56B): gap bytes between classify tail and submit_slot_card_sprite_row_entry; 0 raw/thumb refs
- 0x0804cca2 / 0xea (234B): orphan THUMB code (2 bx lr), loads PTR_DAT ptr; raw=1 from 0x086bb944 (compressed resource, non-code); 0 external code refs
- 0x0804cdac / 0x2c (44B): orphan THUMB stubs (3 entry pts); raw=7 all from internal PTR_DAT_0804cd90 table (orphan island); 0 external refs

**fn-ptr periodic fix** (post re-export): asm/03 x4 (eval_equip_bonus_for_slot_pred_fn / eval_amazoness_fnptr_a / eval_amazoness_fnptr_b / eval_equip_chain_pred_fnptr) + asm/04 x3 (zone_monster_field_bonus_table+7*16 / apply_nitro_unit_equip_activation+1 / gDuelFieldSlots+EFFECT_ZONE_PARTITION_OFF)

**plate FUN_ in Seg-5 range**: 11 occurrences, all are caller references from Seg-6+ callers (FUN_080432bc/08043714/080439e0/08043d90/080440b8 / FUN_08095ba8/08095ca0/08095d84); deferred to Seg-6 / file-09 refinement per proposal C8 approval

**CJK in new EOL/plate**: 0 (all text from this segment is pure ASCII)

**byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b

**commit**: 20cbc8b

---

### 4.06 Seg-6 完成记录 (0x0804d124..0x0804ffba, 24 fn + secondary stubs, 128 slots)

**函数列表 (24)**:
switchD_0804ce98__caseD_1e / switchD_0804ce98__caseD_1f / switchD_0804ce98__caseD_3 /
dispatch_sprite_row_anim_by_state / reset_sprite_row_queue_tail /
dispatch_sprite_row_queue_by_state / clear_sprite_row_queue_overflow_flag /
flush_sprite_row_queue_partial / compact_equip_zone_rank3_entries /
dispatch_equip_field_update_by_anim_state / advance_equip_zone_rank_state /
check_equip_slot_eligibility_with_whitelist / check_equip_slot_eligible_with_owner_and_type /
check_equip_slot_eligible_triple_predicate / check_equip_slot_eligible_by_owner_and_prereqs /
check_equip_slot_eligible_with_whitelist_and_type / check_equip_target_matches_card_owner /
check_slot_card_eligible_by_card_id / return_zero_unconditional /
check_card_state_code_eq_15 / check_card_state_code_eq_16 / check_card_state_code_eq_13 /
check_card_state_code_eq_11 / check_card_state_code_eq_3

**Secondary stubs from 5 disasm regions**:
- Block 1 (0x4d294..0x4daf5, 13 THUMB stubs): dispatch_sprite_row_anim_case_0..12
- Block 2 (0x4dd58..0x4f0c1, 12 THUMB stubs): dispatch_sprite_row_queue_case_0..11
- Region A (0x4cca2..0x4cd8b, 3 helpers): SUB_0804cca4 / SUB_0804cd00 / SUB_0804cd74
- Region C (0x4cdac..0x4cdd7, 4 orphan handlers): orphan_slot_card_eligible_handler_0/1/2 + LAB_0804cdd2
- Region D (0x4f098..0x4f0c1, 2 helpers): SUB_0804f098 / SUB_0804f0b8

**符号化统计**: EQ=129 (Seg-6a ~68 + Seg-6b ~61) / REF=2 / RENAME=2 / PLATE=13 occurrences (9 unique FUN_ replaced)

**新建 constants**:
- ewram.inc +8: SPRITE_ROW_WRITE_PTR_OFF / SPRITE_ROW_COUNT_OFF / SPRITE_ROW_ANIM_STATE_OFF / SPRITE_ROW_QUEUE_STATE_A_OFF / SPRITE_ROW_ANIM_CTL_OFF / SPRITE_ROW_QUEUE_ACTIVE_OFF / SPRITE_ROW_QUEUE_STATE_OFF / gEquipZoneRankState
- card_info.inc +25 named CID: PETIT_MOTH / LABYRINTH_WALL / CYCLON_LASER / BUSTER_RANCHER / Y_DRAGON_HEAD / Z_METAL_TANK / DARK_BLADE / DECAYED_COMMANDER / GIANT_ORC / SECOND_GOBLIN / VAMPIRE_ORCHIS / DES_DENDLE / BURNING_BEAST / AITSU / WHITE_MAGICIAN_PIKERU / RITUAL_WEAPON / CHU_SKE_MOUSE_FIGHTER / EHERO_SPARKMAN / LEGENDARY_BLACK_BELT / SOITSU / INDOMITABLE_FIGHTER_LEI_LEI / EBON_MAGICIAN_CURRAN / DIVINE_SWORD_PHOENIX_BLADE / V_TIGER_JET / ADHESIVE_EXPLOSIVE
- card_info.inc +10 unallocated: cid_10d4 / cid_10da / cid_10e2 / cid_10e5 / cid_10ea / cid_10eb / cid_10ed / cid_10ee / cid_12c6 / cid_12ef
- card_info.inc +1 threshold: FIELD5_SCORE_THRESHOLD_1299 (0x513)

**carve**: 0 (no inter-function ROM_INCBIN; all 5 disasm regions resolved by R4)

**R4 disasm** (5 regions):
- Block 1: jump table PTR_DAT_0804d258 (15 entries, raw ptrs); 13 case stubs; 128 literal pool DWORDs forced via RefineF05Seg6PoolLabels.py
- Block 2: jump table PTR_DAT_0804dbb8 (104 entries, 12 unique + default); 12 case stubs; 4 additional pool DWORDs at 0x4e41c/4e4d0/4e604/4e77c (0x0201c520, gDuelFieldSlots+0x10) forced to DWORD
- Region A: 3 helpers called from Block 1; discovered only after Block 1/2 disasm revealed bl targets; 6 literal pool DWORDs forced
- Region C: 4 orphan handlers (jump table dispatch from SUB_0804cd74); LAB_0804cdd2 = bhi target from SUB_0804cd74
- Region D: 2 helpers called from Block 2 SUB_0804e7f0

**Ghidra scripts**:
- RefineF05Seg6Apply.py: EQ=129 / REF=2 / RENAME=2 / PLATE=12 subs
- DisassembleF05Seg6Blocks.py: Block1 13 stubs (901 inst) + Block2 12 stubs (2032 inst)
- DisassembleF05Seg6Secondary.py: Region A 3 stubs + Region B 2 stubs
- DisassembleF05Seg6Tertiary.py: Region C 4 stubs (21 inst) + Region D 2 stubs (18 inst)
- RefineF05Seg6PoolLabels.py: 138 total clearListing+DWord+label (128 original + 6 Region A + 4 Block2 decoded-as-instruction fixes)

**踩坑**:
- Literal pool words decoded as THUMB by disassembler (NOT separate DWORD): must use clearListing+createData(DWordDataType) NOT createLabel alone; total 138 pool fixes
- Block 1/2 disasm revealed secondary helper functions (SUB_0804cca4/cd00/cd74 in ROM_INCBIN 0x4cca2; SUB_0804e7f0/e888 in ROM_INCBIN 0x4e7ec) that were misclassified as 0-ref orphans in Seg-5 - these were only revealed as needed after Block 1/2 disasm
- Region C (0x4cdac) misclassified as "7 internal refs only, orphan" in Seg-5; becomes needed because bhi from SUB_0804cd74 targets LAB_0804cdd2 inside
- Region D (0x4f098): SUB_0804f0b8 called from Region B SUB_0804e7f0 in cascading discovery chain
- 4 literal pool words at 0x4e41c/4e4d0/4e604/4e77c each = 0x0201c520 (gDuelFieldSlots+0x10); after clearListing+setTMode across Block 2, disassembler decoded them as stmia+lsls; fixed by adding to pool labels script
- fn-ptr periodic fix (post re-export): asm/03 x4 + asm/04 x3 (same slots as Seg-5 and prior segs)

**plate FUN_ in Seg-6 range**: 0 stale FUN_ in code positions (all in `@` comments = cross-file references deferred)

**CJK in new EOL/plate**: 0 (all Ghidra-set text is pure ASCII)

**byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b

**commit**: pending

---

### 4.03 Seg-3 完成记录 (0x0804ad48..0x0804b4f4, 24+5 fn, 73+20 slots, 3 disasm blocks)

**函数列表 (24 original)**:
check_card_has_stat_with_bit_13 / check_card_has_spell_counter /
check_card_field5_high_byte_match / check_card_field5_word_match /
check_card_is_union_type / check_card_is_amazon_type /
check_card_is_sea_serpent_type / check_card_is_fairy_type /
check_card_is_insect_type / check_card_is_rock_type /
check_card_is_plant_type / check_card_is_machine_type /
check_card_is_thunder_type / check_card_is_beast_type /
check_card_is_beast_warrior_type / check_card_is_dinosaur_type /
check_card_is_reptile_type / check_card_is_aqua_type /
check_card_is_pyro_type / check_card_is_wind_type /
check_card_is_earth_type / check_card_is_water_type /
check_card_is_fire_type / check_card_is_ninja_type (FUNC_RENAME from check_card_id_in_special_set)

**函数列表 (5 new from R4 disasm)**:
check_card_is_toon_type (0x0804ae40) /
check_card_is_guardian_type (0x0804af88) /
check_card_is_dark_scorpion_type (0x0804b004) /
check_card_is_batteryman_type (0x0804b250) /
check_card_is_dark_world_range_type (0x0804b26c)

**符号化统计**: EQ=87 (70 main-segment + 17 disasm literal pool)
/ REF=2 / RENAME=3 / FUNC_RENAME=1 (check_card_id_in_special_set->check_card_is_ninja_type)
/ PLATE=7 (6 FUN_ subs + 1 ASCII rewrite for ninja_type)

**新建 constants**:
- card_info.inc +50 CID:
  main-segment (40): B_SKULL_DRAGON_CID / SERPENTINE_PRINCESS_CID / PARASITE_PARACIDE_CID /
  DREAM_CLOWN_CID / THOUSAND_EYES_RESTRICT_CID / RELINQUISHED_CID / THOUSAND_EYES_IDOL_CID /
  AMAZONESS_ARCHER_CID / AMAZONESS_CHAIN_MASTER_CID / AMAZONESS_FIGHTER_CID /
  AMAZONESS_PALADIN_CID / AMAZONESS_SWORDSWOMAN_CID / AMAZONESS_TIGER_CID /
  AMAZONESS_BLOWPIPER_CID / AMAZONESS_SPELLCASTER_CID / AMAZONESS_TRAINEE_CID /
  PRINCESS_OF_TSURUGI_CID / INJECT_FAIRY_LEN_CID / CELTIC_GUARDIAN_CID /
  BREAKER_THE_MAGICAL_WARRIOR_CID / DARK_MAGICIAN_GIRL_CID / MAGICAL_MARIONETTE_CID /
  COPYCAT_CID / SKILLED_WHITE_MAGICIAN_CID / SKILLED_DARK_MAGICIAN_CID /
  APPRENTICE_MAGICIAN_CID / DARK_RED_ENCHANTER_CID / MYTHICAL_BEAST_CERBERUS_CID /
  ENDYMION_THE_MASTER_MAGIC_SWORDSMAN_CID / MAGICIAN_OF_FAITH_CID /
  NINJA_GRANDMASTER_SASUKE_CID / NINJA_SHADOW_SASUKE_CID / NINJA_YOSENJU_SASUKE_CID /
  ARMED_SAMURAI_BEN_KEI_CID / DISCIPLE_OF_THE_FORBIDDEN_SPELL_CID /
  WATER_DRAGON_CID / HYDROGEDDON_CID / OXYGEDDON_CID /
  ANCIENT_GEAR_GOLEM_CID / ANCIENT_GEAR_DRILL_CID
  disasm blocks (10): TOON_ALLIGATOR_CID / METAL_GUARDIAN_CID / GATE_GUARDIAN_CID /
  GUARDIAN_OF_THRONE_ROOM_CID / SKULL_GUARDIAN_CID / GUARDIAN_ANGEL_JOAN_CID /
  LOST_GUARDIAN_CID / DARK_SCORPION_CHICK_CID / DARK_SCORPION_MEANAE_CID /
  MUSTERING_DARK_SCORPIONS_CID

**R4 disasm**: 3 ROM_INCBIN blocks disassembled into 5 THUMB functions
- Block A (0x0804ae40..0x0804b003, 6 CID toon check): check_card_is_toon_type; literal pool 6 x 4B forced DWORD via FixF05Seg3SplitLiteralPools.py
- Block B (0x0804b004..0x0804b24f, 8 CID guardian + 3 CID dark_scorpion + 1 CID batteryman):
  check_card_is_guardian_type / check_card_is_dark_scorpion_type / check_card_is_batteryman_type;
  literal pool 12 x 4B forced DWORD
- Block C (0x0804b26c..0x0804b287, 2 CID dark_world_range check; switch table 0x0804b288..0x0804b2d3 19xDWORD; inline stub 0x0804b2d4..0x0804b2db):
  check_card_is_dark_world_range_type; FixF05Seg3BlockCStubTable.py split switch table DWORDs
  + disasm inline stub; dark_world_range_case1_ret @ 0x0804b2d4 / dark_world_range_ret0 @ 0x0804b2d8

**carve**: 0 (no inter-function ROM_INCBIN; 3 intra-function disasm blocks resolved by R4)

**Ghidra 脚本**:
- RefineF05Seg3Slots.py: A=70 EQ / B=1 REF / C=1 RENAME / D=1 FUNC_RENAME / E=8 PLATE_SUBS / E2=1 PLATE_REWRITE
- DisassembleF05Seg3Blocks.py: 3 blocks clearListing+setTMode+disasm; 5 createFunction; RENAME2+REF1+PLATE5
- FixF05Seg3SplitLiteralPools.py: 20 slots clearListing+createDWord+label+equate (forced DWORD split)
- FixF05Seg3BlockCStubTable.py: 19 switch table DWORDs + 8B inline stub disasm + 2 labels

**踩坑**:
- EQ FAIL "no 4B data": disasm 后 literal pool 被 Ghidra 当 code/raw bytes; 必须
  clearListing+createData(DWordDataType) 强制转 DWORD 才能单独 export label
- Block C switch table 0x0804b288..0x0804b2d3 + inline stub 0x0804b2d4..0x0804b2db 须分开处理;
  bhi LAB_0804b2d8 在链接时无定义 -> FixF05Seg3BlockCStubTable.py 补 disasm stub + label
- fn-ptr +1 periodic fix: asm/04 x3 (zone_monster_field_bonus_table+7*16 / apply_nitro_unit_equip_activation+1 / gDuelFieldSlots+EFFECT_ZONE_PARTITION_OFF) after re-export

**byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b

**commit**: bd9ce13

---

## 五、批次路线图 (地址序, Seg-1..Seg-10)

> 按 file 05 范围 `[0x08049014, 0x080537c0)` (239 named fn, 1010 DAT_/DWORD_/PTR_ 槽,
> **0 ROM_INCBIN/inter-function 数据块** — 文件全为代码 + 函数内 literal pool +
> switchD/switchdataD 函数内跳转表) 按**函数数**均分 10 段 (~24 fn/段, 边界=函数结束处=下一函数起点)。

| Seg | 地址范围 | ~fn | ~slots | 内含 ROM_INCBIN | 主题 (初判) |
|---|---|---|---|---|---|
| Seg-1 | 0x49014..0x4a5b8 | 24 | 152 | — | 效果区 LP/shape sprite 提交 + equip slot sprite + monster zone equip sprite/lp counter 簇 |
| Seg-2 | 0x4a5b8..0x4ad48 | 24 | 68 | — | monster zone equip sprite 尾 + switchD_0804a9ee 派发 + card field5 查询簇头 |
| Seg-3 | 0x4ad48..0x4b4f4 | 24 | 73 | — | card 字段查询 (field5/field8/stat) 谓词簇 + summon restriction 查询头 |
| Seg-4 | 0x4b4f4..0x4c6e8 | 24 | 200 | — | 重: get_card_field_summon_restriction + check_card_is_equip_set 簇 + switchD_0804c6dc 大型派发表 |
| Seg-5 | 0x4c6e8..0x4d124 | 24 | 65 | — | switchdataD_0804c6e8 跳转表 + slot card sprite row packed 提交簇 |
| Seg-6 | 0x4d124..0x4ffba | 24 | 128 | — | switchD_0804ce98 派发 + check_equip_slot_eligible_with_owner_and_type 资格检查簇头 |
| Seg-7 | 0x4ffba..0x50e40 | 24 | 73 | — | check_slot_zone_bit3 + eligible_type_and_card_match 资格检查簇 |
| Seg-8 | 0x50e40..0x51cc4 | 24 | 83 | — | eligible_with_whitelist_prereqs + by_opposite_side_and_prereqs 资格检查簇 |
| Seg-9 | 0x51cc4..0x52df8 | 24 | 117 | — | eligible_by_card_id_bst_and_pairs + dispatch_alt 大型 card_id 资格分发簇 |
| Seg-10 | 0x52df8..0x537c0 | 23 | 51 | — | eligible_by_prereqs_and_active_player_match + by_owner_mismatch 资格检查簇 (文件末) |

执行约定同 file 00..04: 每段走 §二 pipeline; Seg 内可多次提交但地址序不回头; 已干净函数跳过只补 gap;
每完成一段更新 §三 + §四 + refine-progress。

### 5.1 未引用数据登记表 (规则 3)

| 地址 | 大小 | 所在 Seg | 初判内容 | 状态 |
|---|---|---|---|---|
| (各段 ref-scan 0 引用块由 executor/fixer 追加) | | | | |
| 0x0804aa5e | 0xee (238B) | Seg-2 | 孤立 THUMB 代码块 (BST 比较器形态, 与 check_card_pair_allowed 结构相似但独立); 全 ROM raw=0 fn-ptr 及 THUMB+1=0 (2B step exhaustive scan, reviewer 独立确认) | defer |
| 0x0804becc | 0x54 (84B) | Seg-4b | THUMB dead code orphan (01 1c...70 47 等 opcode); no named function; 全 ROM raw=0 / THUMB+1=0 (穷举 2B-step scan [4becc,4bf20), reviewer 独立确认) | defer |

---

## 六、相关文档
- `doc/dev/methodology/refine-loop.md` (方法论)
- `doc/dev/p5-refine-00-system-str-vija.md` (file 00 完整记录 + §一 R1-R9 详版)
- `doc/dev/p5-refine-04-card-zone-sprite.md` (file 04 完整记录, card_info.inc CID 批量沉淀 / oam_attr P1/P2 / packed 值 / 重段 8a/8b 拆分 / fn-ptr +1 踩坑)
- `doc/dev/refine-progress.md` (25 文件跨文件总进度)
