# 函数/数据细化计划 — `asm/03_equip_chain_hand.s`

> 阶段目标: 把 `asm/03_equip_chain_hand.s` (ROM `0x08035F54 ~ 0x0804020C`, 装备节点链接 +
> slot 链最优目标查找 + 手牌区交换显示) **逐段地址序细化完成**, 全程 byte-identical
> (`SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b`)。
>
> 这是 refine 第 **4** 个文件 (file 00 / 01 / 02 已全 10 段完成, 见对应
> `p5-refine-00-system-str-vija.md` / `p5-refine-01-vija-scene-text.md` /
> `p5-refine-02-text-lp-fieldspell.md`)。方法论 + R1-R9 细化清单 + 三条硬规则见
> `doc/dev/methodology/refine-loop.md` 与 file 00 doc §一。

---

## 一、细化要求 (checklist)

沿用 file 00/01/02 doc §一 的 **R1-R9** (常量 equate / 灭自动名 / 引用接通 / 误标代码 disasm /
注释订正用现名 / 先读消费者 / 数据 carve 进 rom.s / 图形目视 / byte-identical+备份) +
**三条硬规则** (严格地址序 Seg-1..10 不回头 / 函数间 ROM_INCBIN 必 carve 或 §5.1 / 全 ROM 0 引用→§5.1)。

**跨文件踩坑沿用** (file 00/01/02 沉淀):
- EQ_SLOT 的 Ghidra 槽 label 名 **必须 != `.equ` 常量名** (`<func>_<const>` 式; 否则 GAS PC-relative
  "value too big") — 见 memory `carve-eq-label-collision`。
- Ghidra EOL/plate **一律 ASCII** (含 CJK 会 Jython 双重 UTF-8 mojibake), 中文解释走 doc/。
  (proposal/review markdown 文档可中文, 仅写入 Ghidra .rep 的 plate/EOL 须 ASCII)
- carve byte-identical: host incbin 覆盖等式 `sum(spans)==原 size`; THUMB fn-ptr 表 `.word <fn>+1`,
  数据指针/slot-index 表不 +1; `.asciz` 须含 NUL+对齐 pad; .hword RGB15 注意 bit15。
- **executor 严守段上界** (reviewer C1 逐槽地址裁定)。
- **C5 按值去重不分语义域**: 新建常量前必扫全 19 个 constants/*.inc 确认无同值常量;
  REF/RENAME 不得绕过已存在常量值; 不建孤儿常量 (段内无槽持该值)。
- **C13 残留 100% 覆盖**: 段内 incbin 块外所有 DAT_/DWORD_/PTR_ 净数须被 EQ+REF+RENAME 去重全覆盖,
  勿留"低优先级不处理"。
- **C8 stale 函数名**: plate 中 `FUN_xxxx`/`PTR_FUN_xxxx` **完整字符串**匹配替换现名 (禁子串匹配);
  整段 setPlateComment 重写, 落地后 grep 段范围 FUN_ == 0 验收。
- **R4 大块 disasm**: flow-disasm 会把 literal pool 当 THUMB 解码 → reference-manager 扫 PC-relative
  ldr 目标 createDWord 一次性全覆盖; mov pc,r0 派发表存裸 THUMB 地址; 重跑前 clearListing 整 range
  再 setTMode (避 ContextChangeException)。
- **卡牌 ID 常量 (file 02 Seg-8/10 教训)**: 命名前必查 `data/card-stats.s` passcode→slot_id 坐实
  card_id→卡名映射 (file 02 Seg-8 Yami/Sanctuary 误判, 经 data.md 订正)。无对应卡 → 降级
  `<func>_cid_<hex>` 低置信 RENAME, 勿臆造卡名 (触发红线 3)。
- 复用 file 00/01/02 已建 constants/*.inc 与 carve label (见 §一末尾资产清单)。

**file 02 已建可复用资产** (新建前必 grep 确认无同值):
- `ewram.inc`: gDuelFieldSlots=0x0201c510 / gEquipNodePool / gEquipChainSlotRefs / gDuelFieldSlotState /
  gDuelEffectChainSlots=0x0201bc54 / PLAYER_BLOCK_STRIDE=0x868 / ZONE_CHAIN_CARD_ID_OFF=0x10e2 /
  gP1SlotCountBase / gP1SlotSetCodeArray / gP1HandCountBase / gP1HandSlotArray / gP1ChainZoneCountBase /
  gP1ChainZoneArray / gP1AltHandCountBase / gP1AltHandSlotArray / gP1ZoneHandCount /
  gDuelFieldSlots_p2_base=0x0201c5d8 / gDuelFieldSpellZoneBase=0x0201c5ec
- `duel_field.inc`: FIELD_SLOT_PHASE_MASK / EQUIP_NODE_BASE_OFFSET / NODE_POOL_NEG_OFFSET /
  EQUIP_CHAIN_LINK_OFFSET / FIELD_SLOT_COUNT_OFF=0x1cb4 / SLOT_FACE_STATUS_ARRAY_OFF=0x10b1 /
  FIELD_SPELL_CARD_REF_OFF=0x1390 / DUEL_ACTIVE_PLAYER_OFF=0x1cb8 / EQUIP_SLOT_ACTIVE_TAG=0xa5600000 /
  EFFECT_ZONE_PARTITION_OFF=0x10a4 / EFFECT_ZONE_BITMASK_OFF=0x10d0 / ACTIVATION_STATE_A_OFF=0x1d48 /
  ACTIVATION_STATE_B_OFF=0x1d78 / ACTIVE_EFFECT_CATEGORY_OFF=0x10d8 /
  FIELD5_SCORE_ACTIVATION_THRESHOLD=0x76b / FIELD5_SCORE_FIELDSPELL_THRESHOLD=0x63f
- `card_info.inc`: SLOT_CARD_SET_CODE_MASK=0x00001fff / FIELD_SPELL_B_EFFECT_ID=0x1407 + file 02 已建
  众多 *_CARD_ID / EQUIP_*_CID / HAMON_LORD_CID 等 (复用前必 grep card_info.inc)
- `oam_attr.inc`: OAM_ATTR0_HIDDEN / OAM_ATTR2_TILE_CLEAR=0xffffe000
- `bitops.inc`: 8 POPCOUNT_MASK_*
- 全局: gVijaState=0x02029eb0 / gDemoState=0x02029ec0 / gDuelSceneBase=0x02023360 /
  gDuelCardCtxBase=0x0201e2a0 / gDuelDispCtx=0x0203eeb0

---

## 二、落地工作流 (pipeline)

同 file 00/01/02 doc §二「代码侧 pipeline」:
```
备份 .rep → Ghidra 脚本 (RefineF03Seg<N>*.py: equate/label/ref/rename/plate/disasm)
→ ghidra-export-range.bat 080000c0 084c7637 → inject_modes.py → split_all_s.py
→ build + byte-identical SHA1 9689337d → (改函数名才) ExportFunctionInventory + sync CSV → commit
```
3-agent: executor (proposal) → reviewer (C1-C13 review) → fixer (模式A改proposal / 模式B落地)。

---

## 三、当前进度 (03_equip_chain_hand.s)

| Seg | 范围 | ~fn | ~slots | 内含 ROM_INCBIN | 状态 | commit |
|-----|------|-----|--------|-----------------|------|--------|
| 1 | 0x35f54..0x36a78 | 13 | 82 | — | ✅ | c410d1d |
| 2 | 0x36a78..0x37128 | 13 | 37 | — | ✅ | 6ec659f |
| 3 | 0x37128..0x37904 | 13 | 37 | — | ✅ | b90b81f |
| 4a | 0x37904..0x37ec0 | 12 | 43 | — | ✅ | b56ee3e |
| 4b | 0x37ec0..0x3a7f0 | 1+subs | 140+ | **0x39350/0x10ce** | ✅ | c0cf7ca |
| 5 | 0x3a7f0..0x3b3a8 | 13 | 79 | **0x3b24e/0x66** | ⬜ | |
| 6 | 0x3b3a8..0x3bba4 | 13 | 79 | — | ⬜ | |
| 7 | 0x3bba4..0x3c774 | 13 | 51 | **0x3be38/0x14** | ⬜ | |
| 8 | 0x3c774..0x3d91c | 13 | 121 | — | ⬜ | |
| 9 | 0x3d91c..0x3efcc | 13 | 143 | — | ⬜ | |
| 10 | 0x3efcc..0x4020c | 13 | 109 | — | ⬜ | |

图例: ✅ 完成 / 🟡 进行中 / ⬜ 未开始。
重段提示: Seg-4 (183 槽 + 大 incbin 0x10ce) / Seg-9 (143 槽) / Seg-8 (121) / Seg-10 (109) 较重,
必要时拆 Seg-Na/Nb (地址序边界=函数结束处, 不回头)。

---

## 四、逐段完成记录

(各段落地后由 fixer 追加 4.0N 小节: 函数列表 / 符号化统计 / 新建 constants / carve / 踩坑 / commit)

### 4.01 Seg-1 完成记录 [0x08035f54..0x08036a78)

**函数列表 (13 fn)**:
link_equip_node_by_card_type_check / check_slot_equip_eligibility_by_type /
check_slot_field_zone_card_eligible / check_slot_equip_whitelist_with_monster_space /
check_slot_card_effect_eligibility / query_slot_effect_eligibility_nonzero /
check_slot_card_fieldspell_eligibility / check_slot_fieldspell_eligible_by_side /
query_slot_card_type_eligibility / check_zone_slot_equip_prerequisites /
check_card_equip_eligible_for_slot / check_equip_eligibility_via_request_buf /
check_slot_card_special_activation_eligible

**符号化统计**: EQ=81 (reuse 46 + new 35) / REF=0 / RENAME=3 / FUNC_RENAME=0 / PLATE=13

**新建 constants**:
- `card_info.inc` +35: EHERO_AVIAN_CID / CHAIN_THRASHER_CID / ROYAL_COMMAND_CID / FIEND_SKULL_DRAGON_CID / POSSESSED_DARK_SOUL_CID / SNATCH_STEAL_CID / MAGIC_ARM_SHIELD_CID / CHANGE_OF_HEART_CID / MYSTIC_BOX_CID / DARK_NECROFEAR_CID / BRAIN_JACKER_CID / ENEMY_CONTROLLER_CID / FALLING_DOWN_CID / OWNER_SEAL_CID / RESHEF_THE_DARK_BEING_CID / CHTHONIAN_POLYMER_CID / CHARMER_RANGE_MAX_CID / ELEMENT_MAGICIAN_CID / CANNONBALL_SPEAR_SHELLFISH_CID / DEEPSEA_WARRIOR_CID / HORUS_LV6_CID / HORUS_LV8_CID / HORUS_SERVANT_CID / SILENT_SWORDSMAN_LV5_CID / METALLIZING_PARASITE_CID / NON_SPELLCASTING_AREA_CID / DUST_BARRIER_CID / EHERO_WILDHEART_CID / LORD_OF_D_CID / KING_DRAGUN_CID / HEART_OF_CLEAR_WATER_CID / TIMIDITY_CID / EXODIA_NECROSS_CID / EQUIP_TYPE_A_CID / DARK_MAGICIAN_OF_CHAOS_CID
- `ewram.inc` +1: gDuelPhaseFlags (0x0201b290)
- `duel_field.inc` +3: PHASE_LOCK_FLAG_OFF / EQUIP_SLOT_CARD_ID_RANGE_MAX / NODE_POOL_TO_SLOT_STATE_OFF

**carve**: 0 (no ROM_INCBIN in Seg-1)
**disasm**: 0
**§5.1**: 0

**C8 验收**: Seg-1 范围内无 stale FUN_ (0x08036a78 后的 FUN_ 属 Seg-2+)
**Non-ASCII**: Seg-1 范围内无新增 CJK (文件头行 2 为预存标题注释)
**byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b

**commit**: c410d1d

### 4.02 Seg-2 完成记录 [0x08036a78..0x08037128)

**函数列表 (13 fn)**:
sum_equip_slot_values / check_slot_card_eligible_for_special_action /
check_slot_card_eligible_for_special_action_b / find_effect_entry_by_card_id /
build_effect_zone_entry / place_card_into_graveyard_slot /
place_card_into_graveyard_slot_with_seq / remove_equip_slot_by_index_from_array_a /
erase_slot_from_equip_array_a_by_ptr / insert_card_into_hand_list /
insert_card_into_field_list / find_deck_slot_by_card_pair_match /
find_graveyard_entry_by_card_id / count_extra_deck_cards_by_player

**符号化统计**: EQ=37 (reuse 29 + new 8) / REF=0 / RENAME=0 / FUNC_RENAME=0 / PLATE=13

**新建 constants**:
- `card_info.inc` +3: GAP_CID_13EA=0x13ea (gap slot, low-conf) / KUNAI_WITH_CHAIN_CID=0x1231 / BLAST_WITH_CHAIN_CID=0x1514
- `ewram.inc` +4: gEffectEntryArray=0x0201b590 / EFFECT_ENTRY_COUNT_OFF=0x594 / HAND_ARRAY_TO_COUNT_NEG_OFF=0xfffffbfc / ALT_HAND_ARRAY_TO_COUNT_NEG_OFF=0xfffffa4c

**carve**: 0 (no ROM_INCBIN in Seg-2)
**disasm**: 0
**§5.1**: 0

**C8 验收**: Seg-2 范围 (asm lines 1530-2482) FUN_ stale label count=0; prose mentions in plates are informational caller references, not stale labels.
**Non-ASCII**: Seg-2 范围内 non-ASCII count=0 (CJK plate at find_deck_slot_by_card_pair_match line 2334 already replaced with pure-ASCII plate)
**byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b

**commit**: 6ec659f

**C8 plate fix-forward (独立审计补, 2026-06-11)**: 4 stale FUN_ 改现名
- place_card_into_graveyard_slot (0x08036cb8): FUN_08032280 → dispatch_card_placement_by_zone_type
- place_card_into_graveyard_slot_with_seq (0x08036d08): FUN_08032280 → dispatch_card_placement_by_zone_type
- erase_slot_from_equip_array_a_by_ptr (0x08036de8): FUN_08032194 → erase_slot_from_zone_array_by_type
- find_deck_slot_by_card_pair_match (0x08037030): FUN_080bb4c2 (bl-site) → dispatch_equip_activation_full_sequence (caller ref)
脚本: tools/ghidra-labeling/RefineF03Seg2PlateFix.py
C8 验收后: asm lines 1530-2449 FUN_=0 / Non-ASCII=0 / byte-identical SHA1 9689337d

### 4.03 Seg-3 完成记录 [0x08037128..0x08037904)

**函数列表 (13 fn + 1 unlabeled)**:
count_graveyard_entries_by_card_id / remove_slot_by_index_from_graveyard_arrays /
erase_slot_from_graveyard_arrays_by_ptr / remove_slot_from_field_array_by_player /
count_hand_cards_with_field5 / count_graveyard_normal_summon_cards /
count_zone_slots_with_card_field5 / check_zone_slot_equip_eligible /
check_zone_slot_equip_eligible_alt / place_equip_card_if_type_matches /
erase_slot_from_field_array_c_by_ptr / eval_equip_bonus_for_slot /
find_field_zone_slot_with_fieldspell
+ unlabeled fn: check_level_conv_lab_node_match @ 0x0803777c (createLabel)

**符号化统计**: EQ=36 (reuse 25 + new 11) / REF=13 (12 PTR_gP1LP + 1 fn-ptr) / RENAME=0 / FUNC_RENAME=0 / PLATE=13

**新建 constants**:
- `card_info.inc` +9: GRADIUS_OPTION_CID / GRADIUS_CID / ULTIMATE_OFFERING_CID / XYZ_DRAGON_CANNON_CID / HELPOEMER_CID / SPHINX_TELEIA_CID / YZ_TANK_DRAGON_CID / LEVEL_CONVERSION_LAB_CID / COST_DOWN_CID
- `ewram.inc` +1: gP1FieldArrayCBase=0x0201c600
- `duel_field.inc` +1: FIELD_ARRAY_C_TO_COUNT_NEG_OFF=0xfffffeec

**carve**: 0 / **disasm**: 0 / **§5.1**: 0

**fn-ptr +1 踩坑**: Ghidra DATA ref 指向偶地址 0x0803777c, 导出的 .word 为 even addr; build 后 diff 发现 0x37884 差 1 字节. 手动在 asm 中改为 `.word check_level_conv_lab_node_match+1` (THUMB odd = 0x0803777d), 重 build byte-identical.

**C8 验收**: asm lines 2452-3526 FUN_=0 (line 3527 的 FUN_0805e170 属 Seg-4 函数 find_field_zone_slot_with_equip_type 的预存 plate, 非 Seg-3 引入)
**Non-ASCII**: asm lines 2452-3526 non-ASCII=0
**byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b

**commit**: b90b81f

### 4.04a Seg-4a 完成记录 [0x08037904..0x08037ec0)

**函数列表 (12 fn)**:
find_field_zone_slot_with_equip_type / count_field_zone_cards_by_field6 (renamed from count_gy_cards_by_field6) /
count_field_zone_cards_by_field7 / count_valid_monster_pair_slots /
find_zone_slot_idx_allowed_for_card / count_field_zone_cards_with_field5 /
count_monster_slots_with_field5_ge_threshold / get_player_deck_flag_bit1 /
check_field_effect_zone_activation_eligible / shuffle_hand_by_player_deck_flag /
compute_zone_effect_atk_delta

**符号化统计**: EQ=32 REF=11 RENAME=33 FUNC_RENAME=1 PLATE=11

**新建 constants**:
- `constants/field_spell_bonus.inc` (新建, 2 constants: FIELD_SPELL_TABLE_IDX_BIAS=0xffffef10 / ZONE_EFFECT_ATK_PENALTY_500=0xfffffe70)
- `card_info.inc` +9 CID: EYE_OF_TRUTH_CID / MIND_ON_AIR_CID / RESPECT_PLAY_CID / YAMI_CID / MOLTEN_DESTRUCTION_CID / GAIA_POWER_CID / MYSTIC_PLASMA_ZONE_CID / NECROVALLEY_CID / HARPIES_HUNTING_GROUND_CID

**carve-1**: field_spell_atk_bonus_table @ROM 0x1E3EF74 (0x120B): 6x24 s16 ATK bonus table for classic field spells (Forest/Wasteland/Mountain/Sogen/Umi/Yami). DAT_08037ddc改名 compute_zone_effect_atk_delta_table_base.

**FUNC_RENAME**: count_gy_cards_by_field6 -> count_field_zone_cards_by_field6 (函数体读 gP1FieldArrayCBase+0x120, 非墓地+0x5d0; ExportFunctionInventory + CSV sync 完成)

**fn-ptr +1 踩坑 (已知问题)**: Ghidra再导出后 0x08037884 (.word check_level_conv_lab_node_match) 变回偶地址; 已在 asm/03 手动补 +1 (THUMB fn-ptr). 源自 Seg-3 已知问题, 每次 re-export 后须重补.

**C8 验收**: asm lines 3529..4335 (Seg-4a) FUN_=0; Non-ASCII=0
**byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b

**commit**: b56ee3e

### 4.04b Seg-4b 完成记录 [0x08037ec0..0x0803a7f0)

**函数列表 (15 fn)**:
eval_slot_score_entry_full (0x08037ec0, 大型 LP-cost 分发) /
compute_lp_cost_by_occupied_monster_zones (0x08038a1a) /
compute_lp_cost_by_hand_field6 (0x08038c60) /
compute_lp_cost_by_extra_deck_card_id (0x08038d34) /
compute_lp_cost_by_zone_field5_x100 (0x08038e84) /
compute_lp_cost_by_zone_field5_x200 (0x08038e90) /
compute_lp_cost_by_zone_field5_both_players (0x08038e9c) /
apply_slot_score_bonus_by_state (0x08038e34) /
dispatch_equip_node_by_type (0x080392da) /
eval_equip_node_type_1_to_4 (R4 disasm 0x08039350) /
eval_equip_node_type_5 (R4 disasm 0x08039a62) /
eval_equip_node_type_6_to_9 (R4 disasm 0x08039a7c) /
eval_equip_node_type_10_to_11 (R4 disasm 0x08039c1c) /
eval_equip_node_type_12 (R4 disasm 0x0803a3c4) /
eval_equip_node_type_13 (R4 disasm 0x0803a2fc) /
advance_equip_node_chain_step (0x0803a41e) /
adjust_slot_score_by_chain_and_zone (0x0803a428) /
cleanup_slot_score_entry_epilogue (0x0803a520) /
check_slot_equip_chain_rule (0x0803a540) /
classify_equip_target_eligibility (0x0803a658)

**符号化统计**: EQ=118 / REF=21 / RENAME=21 / FUNC_RENAME=0 / PLATE=14+4(stale-fix)=18

**R4 disasm**: 6 stubs (eval_equip_node_type_1_to_4/5/6_to_9/10_to_11/12/13) via mov pc,r0 jump table dispatch.
Fix scripts: RefineF03Seg4bFixMcr2.py (4 ARM-decoded literal pools, value 0xfffffe0c),
RefineF03Seg4bFixLiteralPools.py (52 missing pool labels).

**新建 constants**:
- `card_info.inc` +70: SKULL_SERVANT_CID / DARK_MAGICIAN_CID_0FC9 / HARPIE_LADY_CID / CASTLE_OF_DARK_ILLUSIONS_CID / PUMPKING_CID / MACHINE_KING_CID / MUKA_MUKA_CID / MAHA_VAILO_CID / REVERSE_TRAP_CID / MAGICIAN_OF_BLACK_CHAOS_CID / DARK_MAGICIAN_GIRL_CID / SHIELD_AND_SWORD_CID / MIRROR_WALL_CID / AQUA_CHORUS_CID / COMMAND_KNIGHT_CID / FLASH_ASSAILANT_CID / SLATE_WARRIOR_CID / NUVIA_THE_WICKED_CID / LIGHTNING_BLADE_CID / YELLOW_LUSTER_SHIELD_CID / DARK_MAGICIAN_CID_142D / EMBODIMENT_OF_APOPHIS_CID / SOUL_OF_PURITY_CID / ROCK_SPIRIT_CID / THE_A_FORCES_CID / MUDORA_CID / MASTER_OF_DRAGON_SOLDIER_CID / BANNER_OF_COURAGE_CID / DARK_PALADIN_CID / MAGICAL_MARIONETTE_CID / METAL_REFLECT_SLIME_CID / GYAKU_GIRE_PANDA_CID / NIGHTMARE_PENGUIN_CID / PERFECT_MACHINE_KING_CID / SKULL_ZOMA_CID / AGENT_OF_FORCE_MARS_CID / UNHAPPY_GIRL_CID / MOKEY_MOKEY_CID / THEBAN_NIGHTMARE_CID / ELEMENT_DRAGON_CID / ENRAGED_MUKA_MUKA_CID / GREEN_GADGET_CID / STRONGHOLD_CID / RED_GADGET_CID / YELLOW_GADGET_CID / SILENT_MAGICIAN_LV4_CID / ULTIMATE_INSECT_LV3_CID / ELEMENT_SAURUS_CID / MOKEY_MOKEY_SMACKDOWN_CID / BEHEMOTH_KING_CID / ULTIMATE_INSECT_LV5_CID / RED_EYES_DARKNESS_DRAGON_CID / KING_OF_SKULL_SERVANTS_CID / DORIADO_CID / BATTERYMAN_AA_CID=0x18c3 / BATTERYMAN_AA_CID_SHIFTED=0xc6180000 / BATTERYMAN_C_CID / BATTERYMAN_C_CID_SHIFTED / SANCTUARY_CID_SHIFTED / DARK_DREADROUTE_CID / TADPOLE_CID / TYRANNO_INFINITY_CID / EHERO_SHINING_FLARE_WINGMAN_CID / WATER_DRAGON_CID / CYBER_BLADER_CID / MACHINE_KING_PROTOTYPE_CID / ANCIENT_GEAR_CASTLE_CID / PARASITIC_TICKY_CID / TREEBORN_FROG_CID / BEELZE_FROG_CID / SAND_MOTH_CID / D3S_FROG_CID / EHERO_ERIKSHIELER_CID / GREAT_SPIRIT_CID / HELIOS_CID / HELIOS_DUO_MEGISTE_CID / GOBLIN_KING_CID=0x1755 / SLOT_CARD_EMPTY=0xffff
- `duel_field.inc` +7: LP_COST_3000 / LP_COST_1500 / SCORE_DELTA_NEG_300 / SCORE_DELTA_NEG_500 / SCORE_DELTA_NEG_700 / FIELD_STATE_OFF / CHAIN_LINK_COUNTER_OFF / EQUIP_PHASE_STATE_OFF
- `ewram.inc` +2: HAND_COUNT_TO_SLOT_OFF / gP1FieldState

**carve-1**: zone_monster_field_bonus_table @ROM 0x1E3F094 (0x130B = 304B, 19 entries x 16B).
Entries [0..6]=ATK bonuses, [7..12]=CID-encoded associated-card entries, [13]=sentinel 0xffff*8, [14..18]=trailing garbage.
Structured as labeled .hword table in asm/rom.s; remainder incbin trimmed accordingly.

**§5.1**: 0 (none in Seg-4b)

**C8 验收**: asm lines 4335..7634 FUN_=0 (4 inner-block stale plates fixed by RefineF03Seg4bFixStalePlates.py)
**Non-ASCII**: asm lines 4335..7634 non-ASCII=0

**踩坑**:
1. fn-ptr +1 (已知问题): 3 slots (0x08037884 check_level_conv_lab_node_match, 0x080389dc/0x080389f8 check_card_is_amazoness_type) 每次 re-export 变回偶地址，手动补 +1。
2. mcr2 ARM 解码: 4 literal pool slots 含 0xfffffe0c (SCORE_DELTA_NEG_500), Ghidra R4 disasm 将其解为 ARM mcr2 指令 — clearListing+createDWord 修正 (RefineF03Seg4bFixMcr2.py)。
3. 52 missing literal pool labels: R4 disasm 后 52 个 PC-relative ldr 目标缺 DAT_ 标签, 导出为 .byte 序列, 引发 GAS "value too big" 错误 — createDWord 修正 (RefineF03Seg4bFixLiteralPools.py)。
4. carve 大小: 初始 14 entries (0xE0B) 漏掉 5 条 trailing garbage entries (0x50B), 补全后 total=0x130B。
5. GOBLIN_KING_CID = 0x1755 (DAT_080384d0 slot=0x1755), NOT Solar Flare Dragon 0x1756 — card-stats.s 坐实。
6. 4 inner-block stale FUN_ plates: PLATE_SLOTS 键为函数入口地址 (0x08038c60 etc.) 但 Ghidra 在内部 code block 地址 (0x08038c02 etc.) 也有旧 plate — 补跑 RefineF03Seg4bFixStalePlates.py 清除。

**byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b

**commit**: c0cf7ca

---

## 五、批次路线图 (地址序, Seg-1..Seg-10)

> 按 file 03 范围 `[0x08035f54, 0x0804020c)` (130 named fn, 913 DAT_/DWORD_/PTR_ 槽,
> 3 ROM_INCBIN) 按**函数数**均分 10 段 (13 fn/段, 边界=函数起点)。

| Seg | 地址范围 | ~fn | ~slots | 内含 ROM_INCBIN | 主题 (初判) |
|---|---|---|---|---|---|
| Seg-1 | 0x35f54..0x36a78 | 13 | 82 | — | equip 节点链接 by card_type + slot 链查找 |
| Seg-2 | 0x36a78..0x37128 | 13 | 29 | — | equip chain 簇 (cont) |
| Seg-3 | 0x37128..0x37904 | 13 | 37 | — | equip chain 簇 (cont) |
| Seg-4 | 0x37904..0x3a7f0 | 13 | 183 | **0x39350/0x10ce** | 重: slot 链最优目标 + incbin (ref-scan 分类) |
| Seg-5 | 0x3a7f0..0x3b3a8 | 13 | 79 | **0x3b24e/0x66** | incbin (ref-scan 分类) |
| Seg-6 | 0x3b3a8..0x3bba4 | 13 | 79 | — | |
| Seg-7 | 0x3bba4..0x3c774 | 13 | 51 | **0x3be38/0x14** | incbin (ref-scan 分类) |
| Seg-8 | 0x3c774..0x3d91c | 13 | 121 | — | |
| Seg-9 | 0x3d91c..0x3efcc | 13 | 143 | — | 重 |
| Seg-10 | 0x3efcc..0x4020c | 13 | 109 | — | 手牌区交换显示 (file 末) |

执行约定同 file 00/01/02: 每段走 §二 pipeline; Seg 内可多次提交但地址序不回头; 已干净函数跳过只补 gap;
每完成一段更新 §三 + §四 + refine-progress。

### 5.1 未引用数据登记表 (规则 3)

| 地址 | 大小 | 所在 Seg | 初判内容 | 状态 |
|---|---|---|---|---|
| (各段 ref-scan 0 引用块由 executor/fixer 追加) | | | | |

---

## 六、相关文档
- `doc/dev/methodology/refine-loop.md` (方法论)
- `doc/dev/p5-refine-00-system-str-vija.md` (file 00 完整记录 + §一 R1-R9 详版)
- `doc/dev/p5-refine-01-vija-scene-text.md` (file 01 完整记录)
- `doc/dev/p5-refine-02-text-lp-fieldspell.md` (file 02 完整记录, equip chain / card_id 常量与 carve label)
- `doc/dev/refine-progress.md` (25 文件跨文件总进度)
