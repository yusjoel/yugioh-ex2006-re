# Refine Proposal: F12-Seg-6 [0x080984d0..0x08099314)

## 段测绘

- 活动文档: `doc/dev/p5-refine-12-equip-activation-scan.md`, 第五节 Seg-6. 前段结束地址为 0x080984d0, 后段起始地址为 0x08099314. 本段无已落地旧覆盖.
- 模块: `asm/12_equip_activation_scan.s`, L9105..10976. ROM: `roms/2343.gba`.
- 函数入口 x3, 另有已命名共享返回尾 x1:

| 地址 | 现名 | 模块行 | 范围/说明 |
|---|---|---|---|
| 0x080984d0 | activate_effect_zone_display_for_slot | 9106 | 下一函数 0x08098564 |
| 0x08098564 | tick_card_activation_phase_by_state | 9179 | 下一函数 0x08098a88 |
| 0x08098a88 | tick_equip_zone_activation_display_state | 9846 | 主体与返回尾共用同一栈帧 |
| 0x080992e2 | restore_high_regs_epilogue_equip_tick | 10951 | 首指令 add sp,#0xc, 无 push; 返回尾后仍有属于本段的 literal pool |

- 残留自动名槽: 126 = DAT_ 114 + DWORD_ 4 + PTR_gP1LifePoints_ 7 + PTR_switchdataD_ 1. 路线图 118 = DAT_ + DWORD_, 不是全部残留槽. 四个 DWORD_ 地址为 0x08098b18/1c/20/24.
- 完整原名/地址/ROM 值测绘见 `output/refine-run-20260831-194634/seg6-slots.json`. 下文三表为这些槽唯一的执行计划, 每个地址只属于一表.
- ROM_INCBIN x0, .byte x0. 段内 .hword 均为已带地址的指令表示, .zero 为对齐, 无新增 disasm/carve.
- 现有结构化 switch 表 [0x080985a0,0x080985b4), 5 个偶地址入口, 通过 MOV pc,r0 派发. 表已在 asm 中, 不作为裸数据重切.
- 旧 plate x4, 全部 ASCII, 长度分别为 937/940/1152/565 个正文字符. 都整段重写, 清除旧 DAT_/FUN_ 引用和参数/基址错误.

## 数据块分类 (Rule 2/3)

| 块 | ref-scan (raw / THUMB+1) | 判定 | 证据 |
|---|---|---|---|
| 裸 ROM_INCBIN/.byte | 0 个块, 候选集合为空 | 无 carve/disasm/5.1 | 段测绘扫描 L9107..10979 无匹配 |
| 已结构化 switch 表 0x080985a0 size 0x14 | raw=1 thumb=0 | 保持结构, REF 接通池槽 | 唯一原始值在 0x0809859c; L9199..9203 MOV pc,r0 |

补充 ref-scan: 表的五个目标 0x080985b4/0x080985c6/0x08098610/0x080987dc/0x08098a44 各 raw=1, thumb=0. 这些是同一函数内 MOV pc 的偶地址跳转目标, 不加 +1. 三个主函数地址 raw=0, THUMB+1=1, 分别位于 0x09e5aafc/0x09e5ab00/0x09e5ab04. 共享返回尾 raw=0, THUMB+1=0, 但有 BL/B/自然续接, 不能登记 5.1.

## 符号化计划 (R1/R2/R3)

约定: EQ/REF 均为 `(slot, value, const_name_or_gas_label, slot_label)`. RENAME 为 `(slot, slot_label, eol_ascii)`. 每表按地址递增. 不改指令、数值、函数体范围或跨段旧 equate.

### EQ_SLOTS (data-equate)

复用/新建由后面的逐值目录明确指定. 以下 80 槽均加 data-equate 和槽标签. 0x080987bc 另加下述辅助导航引用, 其余 EQ 槽不创建地址引用. 辅助引用不计入 REF 主分类.

```text
(0x08098560, 0x0000131d, GRAVEKEEPERS_SERVANT_CID, activate_effect_zone_gravekeepers_servant_cid_98560)
(0x08098598, 0x00001d2c, EQUIP_CHAIN_ACTIVE_OFF, tick_card_activation_chain_active_offset_98598)
(0x0809879c, 0x00001d2c, EQUIP_CHAIN_ACTIVE_OFF, tick_card_activation_chain_active_offset_9879c)
(0x080987a0, 0x00001469, THE_DARK_DOOR_CID, tick_card_activation_the_dark_door_cid_987a0)
(0x080987a8, 0x00000868, PLAYER_BLOCK_STRIDE, tick_card_activation_player_stride_987a8)
(0x080987b0, 0x9c080000, MIRROR_WALL_CID_SHIFTED, tick_card_activation_mirror_wall_shifted_987b0)
(0x080987b8, 0x0000195f, HERO_BARRIER_CID, tick_card_activation_hero_barrier_cid_987b8)
(0x080987bc, 0x0804b165, CHECK_CARD_ID_IS_NORMAL_SUMMON_TYPE_THUMB, tick_card_activation_normal_summon_predicate_987bc)
(0x080987c0, 0x000019a8, CYBER_BARRIER_DRAGON_CID, tick_card_activation_cyber_barrier_dragon_cid_987c0)
(0x080987c4, 0x00000fb6, TIME_WIZARD_CID, tick_card_activation_time_wizard_cid_987c4)
(0x080987c8, 0x00008020, SPRITE_RECORD_P2_SIDE, tick_card_activation_sprite_p2_20_987c8)
(0x080987d8, 0x00001d2c, EQUIP_CHAIN_ACTIVE_OFF, tick_card_activation_chain_active_offset_987d8)
(0x080988c4, 0x00000868, PLAYER_BLOCK_STRIDE, tick_card_activation_player_stride_988c4)
(0x080988cc, 0x000018ad, ANCIENT_GEAR_SOLDIER_CID, tick_card_activation_ancient_gear_soldier_cid_988cc)
(0x080988d4, 0x0000158d, GRAVEKEEPERS_ASSAILANT_CID, tick_card_activation_gravekeepers_assailant_cid_988d4)
(0x080988e0, 0x00001954, VWXYZ_DRAGON_CATAPULT_CANNON_CID, tick_card_activation_vwxyz_dragon_catapult_cannon_cid_988e0)
(0x08098984, 0x24200000, EQUIP_ACTIVATION_PACKED_TYPE18, tick_card_activation_packed_type18_98984)
(0x08098988, 0x00000868, PLAYER_BLOCK_STRIDE, tick_card_activation_player_stride_98988)
(0x08098994, 0x0000153f, ORDEAL_OF_A_TRAVELER_CID, tick_card_activation_ordeal_of_a_traveler_cid_98994)
(0x08098998, 0x000013f9, FAIRY_BOX_CID, tick_card_activation_fairy_box_cid_98998)
(0x08098a28, 0x00001931, PREPARE_TO_STRIKE_BACK_CID, tick_card_activation_prepare_to_strike_back_cid_98a28)
(0x08098a2c, 0x24200000, EQUIP_ACTIVATION_PACKED_TYPE18, tick_card_activation_packed_type18_98a2c)
(0x08098a38, 0x00000482, SPRITE_ROW_PROCESSED_COUNT_OFF, tick_card_activation_row_processed_count_offset_98a38)
(0x08098a40, 0x00001d2c, EQUIP_CHAIN_ACTIVE_OFF, tick_card_activation_chain_active_offset_98a40)
(0x08098a70, 0x00000482, SPRITE_ROW_PROCESSED_COUNT_OFF, tick_card_activation_row_processed_count_offset_98a70)
(0x08098b1c, 0x00000868, PLAYER_BLOCK_STRIDE, tick_equip_activation_player_stride_98b1c)
(0x08098b24, 0x00001cfc, EQUIP_CHAIN_ACTIVE_FROM_FIELD_OFF, tick_equip_activation_chain_active_offset_98b24)
(0x08098b54, 0x0000801b, OAM_EQUIP_SPRITE_TILE_P2_1B, tick_equip_activation_sprite_p2_1b_98b54)
(0x08098c04, 0x000015ff, DIFFUSION_WAVE_MOTION_CID, tick_equip_activation_diffusion_wave_motion_cid_98c04)
(0x08098c0c, 0x00000868, PLAYER_BLOCK_STRIDE, tick_equip_activation_player_stride_98c0c)
(0x08098c14, 0x000015d2, GIANT_ORC_CID, tick_equip_activation_giant_orc_cid_98c14)
(0x08098c24, 0x00001505, ASURA_PRIEST_CID, tick_equip_activation_asura_priest_cid_98c24)
(0x08098c40, 0x00001915, INDOMITABLE_FIGHTER_LEI_LEI_CID, tick_equip_activation_indomitable_fighter_lei_lei_cid_98c40)
(0x08098c44, 0x00001644, BERSERK_DRAGON_CID, tick_equip_activation_berserk_dragon_cid_98c44)
(0x08098c48, 0x00001912, GOBLIN_ELITE_ATTACK_FORCE_CID, tick_equip_activation_goblin_elite_attack_force_cid_98c48)
(0x08098c6c, 0x00001958, EHERO_WILDEDGE_CID, tick_equip_activation_ehero_wildedge_cid_98c6c)
(0x08098c74, 0x000014d6, SPEAR_DRAGON_CID, tick_equip_activation_spear_dragon_cid_98c74)
(0x08098c90, 0x000014d6, SPEAR_DRAGON_CID, tick_equip_activation_spear_dragon_cid_98c90)
(0x08098d14, 0x00001505, ASURA_PRIEST_CID, tick_equip_activation_asura_priest_cid_98d14)
(0x08098d18, 0x000017df, NINJA_GRANDMASTER_SASUKE_CID, tick_equip_activation_ninja_grandmaster_sasuke_cid_98d18)
(0x08098d2c, 0x000017d8, MYSTIC_SWORDSMAN_LV4_CID, tick_equip_activation_mystic_swordsman_lv4_cid_98d2c)
(0x08098d44, 0x00001829, SASUKE_SAMURAI_4_CID, tick_equip_activation_sasuke_samurai_4_cid_98d44)
(0x08098e04, 0x00001963, NANOBREAKER_CID, tick_equip_activation_nanobreaker_cid_98e04)
(0x08098e0c, 0x28200000, EQUIP_ACTIVATION_PACKED_TYPE20, tick_equip_activation_packed_type20_98e0c)
(0x08098e10, 0x00000868, PLAYER_BLOCK_STRIDE, tick_equip_activation_player_stride_98e10)
(0x08098e18, 0x00001829, SASUKE_SAMURAI_4_CID, tick_equip_activation_sasuke_samurai_4_cid_98e18)
(0x08098e20, 0x00001d2c, EQUIP_CHAIN_ACTIVE_OFF, tick_equip_activation_chain_active_offset_98e20)
(0x08098e3c, 0x00001cf8, EQUIP_CHAIN_STEP_FROM_FIELD_OFF, tick_equip_activation_chain_step_offset_98e3c)
(0x08098ed0, 0x00000868, PLAYER_BLOCK_STRIDE, tick_equip_activation_player_stride_98ed0)
(0x08098ed4, 0x0000129c, BIG_SHIELD_GARDNA_CID, tick_equip_activation_big_shield_gardna_cid_98ed4)
(0x08098edc, 0x00001d2c, EQUIP_CHAIN_ACTIVE_OFF, tick_equip_activation_chain_active_offset_98edc)
(0x08098f48, 0x00000868, PLAYER_BLOCK_STRIDE, tick_equip_activation_player_stride_98f48)
(0x08098f4c, 0x00001508, SUPER_ROBOYAROU_CID, tick_equip_activation_super_roboyarou_cid_98f4c)
(0x08098f50, 0x00001397, LUMINOUS_SOLDIER_CID, tick_equip_activation_luminous_soldier_cid_98f50)
(0x08098f54, 0x00001184, INSECT_SOLDIERS_OF_THE_SKY_CID, tick_equip_activation_insect_soldiers_of_the_sky_cid_98f54)
(0x08098f5c, 0x00001507, SUPER_ROBOLADY_CID, tick_equip_activation_super_robolady_cid_98f5c)
(0x08098f74, 0x000018f2, STEAMROID_CID, tick_equip_activation_steamroid_cid_98f74)
(0x08098f78, 0x000017ed, PENUMBRAL_SOLDIER_LADY_CID, tick_equip_activation_penumbral_soldier_lady_cid_98f78)
(0x08098f84, 0x00001952, ETOILE_CYBER_CID, tick_equip_activation_etoile_cyber_cid_98f84)
(0x08099038, 0x00000868, PLAYER_BLOCK_STRIDE, tick_equip_activation_player_stride_99038)
(0x080990bc, 0x00000868, PLAYER_BLOCK_STRIDE, tick_equip_activation_player_stride_990bc)
(0x080990c4, 0x00001508, SUPER_ROBOYAROU_CID, tick_equip_activation_super_roboyarou_cid_990c4)
(0x080990c8, 0x000010c6, upd_cid_10c6, tick_equip_activation_upd_cid_10c6_990c8)
(0x080990cc, 0x00001397, LUMINOUS_SOLDIER_CID, tick_equip_activation_luminous_soldier_cid_990cc)
(0x080990e4, 0x000017ed, PENUMBRAL_SOLDIER_LADY_CID, tick_equip_activation_penumbral_soldier_lady_cid_990e4)
(0x080990e8, 0x00001621, CATS_EAR_TRIBE_CID, tick_equip_activation_cats_ear_tribe_cid_990e8)
(0x080990f4, 0x000018f2, STEAMROID_CID, tick_equip_activation_steamroid_cid_990f4)
(0x08099154, 0x00001cb8, EQUIP_ZONE_COUNT_TABLE_OFF, tick_equip_activation_zone_count_table_offset_99154)
(0x080991b0, 0x00000868, PLAYER_BLOCK_STRIDE, tick_equip_activation_player_stride_991b0)
(0x08099258, 0x00001752, DISC_FIGHTER_CID, tick_equip_activation_disc_fighter_cid_99258)
(0x0809925c, 0x000018f3, DRILLROID_CID, tick_equip_activation_drillroid_cid_9925c)
(0x08099260, 0x28200000, EQUIP_ACTIVATION_PACKED_TYPE20, tick_equip_activation_packed_type20_99260)
(0x08099264, 0x00000868, PLAYER_BLOCK_STRIDE, tick_equip_activation_player_stride_99264)
(0x0809926c, 0x00001476, ANCIENT_LAMP_CID, tick_equip_activation_ancient_lamp_cid_9926c)
(0x08099270, 0x00001286, BLAST_SPHERE_CID, tick_equip_activation_blast_sphere_cid_99270)
(0x080992f4, 0x0000148a, DREAMSPRITE_CID, tick_equip_activation_dreamsprite_cid_992f4)
(0x080992f8, 0x000019bd, ADHESIVE_EXPLOSIVE_CID, tick_equip_activation_adhesive_explosive_cid_992f8)
(0x08099300, 0x28200000, EQUIP_ACTIVATION_PACKED_TYPE20, tick_equip_activation_packed_type20_99300)
(0x08099304, 0x00000868, PLAYER_BLOCK_STRIDE, tick_equip_activation_player_stride_99304)
(0x08099310, 0x00001d2c, EQUIP_CHAIN_ACTIVE_OFF, tick_equip_activation_chain_active_offset_99310)
```

#### 0x080987bc 辅助导航引用 / ASCII EOL / 导出验收

- Ghidra data-equate: `CHECK_CARD_ID_IS_NORMAL_SUMMON_TYPE_THUMB=0x0804b165`, 绑定 slot `0x080987bc`, operand 0; 数值与本节 EQ 四元组一致.
- 辅助导航引用: `0x080987bc -> 0x0804b164`, 类型 `DATA`, 来源 `USER_DEFINED`. 沿用真实偶地址入口的现名 `check_card_id_is_normal_summon_type` 及其 FUNCTION 主符号; 不重命名该函数, 不将 LABEL 提升为主符号. 不在奇地址 `0x0804b165` 创建标签或函数. 此引用不重复计入 REF 主分类.
- 当前导出器 `ExportRangeToGas.py:549..562` 对 ROM FUNCTION 主符号返回 `None`; `:612..617` 随后走 `resolve_word_equate` fallback, 输出必须为 `.word CHECK_CARD_ID_IS_NORMAL_SUMMON_TYPE_THUMB`. 不修改 exporter, 不依赖 REF 生成 `函数名+1` 表达式.
- 数值验收: `0x0804b164+1=0x0804b165`, ROM 小端字节 `65 b1 04 08`. 保持 THUMB 指针低位; 辅助导航目标的偶地址不能替代存储值.
- 该槽新增的 EOL 原文如下, 必须 ASCII:

```text
THUMB callback: check_card_id_is_normal_summon_type+1 = 0x0804b165.
```

### REF_SLOTS (USER-label + DATA-ref)

共 39 槽: RAM 38 + switch 表指针 1. 既有 RAM 目标复用 `constants/ewram.inc` 符号, 新建目标仅 gEquipSlotActivationSnapshot. 目标地址加/确认 USER 主标签, 池槽加 DATA 引用并改槽名; 输出必须为 `.word <gas_label>`. 回调槽 0x080987bc 的主分类为 EQ, 其辅助导航引用按上一节执行.

```text
(0x0809855c, 0x0201bb90, gEquipChainSlotRefs, activate_effect_zone_chain_base_9855c)
(0x08098590, 0x0201bb90, gEquipChainSlotRefs, tick_card_activation_chain_base_98590)
(0x0809859c, 0x080985a0, switchD_0809858e__switchdataD_080985a0, tick_card_activation_phase_table_ptr_9859c)
(0x08098794, 0x0201bc7c, gEquipSlotActivationSnapshot, tick_card_activation_snapshot_base_98794)
(0x080987a4, 0x0201bb90, gEquipChainSlotRefs, tick_card_activation_chain_base_987a4)
(0x080987ac, 0x0201c510, gDuelFieldSlots, tick_card_activation_field_slots_base_987ac)
(0x080987b4, 0x0201c520, gDuelFieldSlotState, tick_card_activation_field_state_base_987b4)
(0x080988c0, 0x0201bb90, gEquipChainSlotRefs, tick_card_activation_chain_base_988c0)
(0x080988c8, 0x0201c510, gDuelFieldSlots, tick_card_activation_field_slots_base_988c8)
(0x080988d0, 0x0201e2a0, gDuelCardCtxBase, tick_card_activation_card_ctx_base_988d0)
(0x08098980, 0x0201bb90, gEquipChainSlotRefs, tick_card_activation_chain_base_98980)
(0x0809898c, 0x0201c510, gDuelFieldSlots, tick_card_activation_field_slots_base_9898c)
(0x08098990, 0x0201c520, gDuelFieldSlotState, tick_card_activation_field_state_base_98990)
(0x08098a30, 0x0201bb90, gEquipChainSlotRefs, tick_card_activation_chain_base_98a30)
(0x08098a34, 0x0201b290, gDuelPhaseFlags, tick_card_activation_phase_flags_base_98a34)
(0x08098a6c, 0x0201b290, gDuelPhaseFlags, tick_card_activation_phase_flags_base_98a6c)
(0x08098b18, 0x0201bb90, gEquipChainSlotRefs, tick_equip_activation_chain_base_98b18)
(0x08098b20, 0x0201c510, gDuelFieldSlots, tick_equip_activation_field_slots_base_98b20)
(0x08098c08, 0x0201bb90, gEquipChainSlotRefs, tick_equip_activation_chain_base_98c08)
(0x08098c10, 0x0201c510, gDuelFieldSlots, tick_equip_activation_field_slots_base_98c10)
(0x08098c70, 0x0201bb90, gEquipChainSlotRefs, tick_equip_activation_chain_base_98c70)
(0x08098c8c, 0x0201bb90, gEquipChainSlotRefs, tick_equip_activation_chain_base_98c8c)
(0x08098d10, 0x0201bb90, gEquipChainSlotRefs, tick_equip_activation_chain_base_98d10)
(0x08098e08, 0x0201bb90, gEquipChainSlotRefs, tick_equip_activation_chain_base_98e08)
(0x08098e14, 0x0201c510, gDuelFieldSlots, tick_equip_activation_field_slots_base_98e14)
(0x08098fb0, 0x0201bb90, gEquipChainSlotRefs, tick_equip_activation_chain_base_98fb0)
(0x08099034, 0x0201bb90, gEquipChainSlotRefs, tick_equip_activation_chain_base_99034)
(0x0809903c, 0x0201c510, gDuelFieldSlots, tick_equip_activation_field_slots_base_9903c)
(0x080990b8, 0x0201bb90, gEquipChainSlotRefs, tick_equip_activation_chain_base_990b8)
(0x080990c0, 0x0201c510, gDuelFieldSlots, tick_equip_activation_field_slots_base_990c0)
(0x08099104, 0x0201bb90, gEquipChainSlotRefs, tick_equip_activation_chain_base_99104)
(0x08099118, 0x0201bb90, gEquipChainSlotRefs, tick_equip_activation_chain_base_99118)
(0x08099158, 0x0201bb90, gEquipChainSlotRefs, tick_equip_activation_chain_base_99158)
(0x080991ac, 0x0201bb90, gEquipChainSlotRefs, tick_equip_activation_chain_base_991ac)
(0x080991b4, 0x0201c510, gDuelFieldSlots, tick_equip_activation_field_slots_base_991b4)
(0x08099254, 0x0201bb90, gEquipChainSlotRefs, tick_equip_activation_chain_base_99254)
(0x08099268, 0x0201c510, gDuelFieldSlots, tick_equip_activation_field_slots_base_99268)
(0x080992fc, 0x0201bb90, gEquipChainSlotRefs, tick_equip_activation_chain_base_992fc)
(0x08099308, 0x0201c510, gDuelFieldSlots, tick_equip_activation_field_slots_base_99308)
```

唯一 switch 指针复用既有表标签, 不改表内 5 个偶地址, 不加 +1. 回调槽的按名导出和数值验收见 EQ 节.

### RENAME_SLOTS (纯改名 + EOL)

共 7 槽. 现有 `.word gP1LifePoints` 已符号化; 保持目标符号/值/引用不变.

```text
(0x08098594, tick_card_activation_lp_base_98594, "gP1LifePoints base; paired offset addresses the equip activation phase.")
(0x08098798, tick_card_activation_lp_base_98798, "gP1LifePoints base; paired offset addresses the equip activation phase.")
(0x080987d4, tick_card_activation_lp_base_987d4, "gP1LifePoints base; paired offset addresses the equip activation phase.")
(0x08098a3c, tick_card_activation_lp_base_98a3c, "gP1LifePoints base; paired offset addresses the equip activation phase.")
(0x08098e1c, tick_equip_activation_lp_base_98e1c, "gP1LifePoints base; paired offset addresses the equip activation phase.")
(0x08098ed8, tick_equip_activation_lp_base_98ed8, "gP1LifePoints base; paired offset addresses the equip activation phase.")
(0x0809930c, tick_equip_activation_lp_base_9930c, "gP1LifePoints base; paired offset addresses the equip activation phase.")
```

### FUNC_RENAME

none. 三个主函数现名覆盖行为, 共享尾现名覆盖寄存器恢复. 只修正 plate 的全局、输入、返回值与控制流说明. 不新增函数, 不需要 function inventory/CSV 同步.

### PLATE (R5, full ASCII rewrite)

仅以下 4 个函数/共享尾的 plate 整段替换. 字符数不含 Markdown fence, 均 <=500.

#### 0x080984d0 (379 chars)

```text
Activates Gravekeeper's Servant and Toll display effects for r0=player_side. Reads the paired player and slot from gEquipChainSlotRefs. Sets chain[+0x10]=1 once; repeated calls return without requeueing. Tests the eligibility result's bit1 before counting Gravekeeper's Servant zones and queuing their display. Counts Toll zones and queues one 500-unit sprite per hit. Returns 1.
```

#### 0x08098564 (464 chars)

```text
Ticks the 0..4 card activation display phases for r0=player_side. State is [gP1LifePoints+EQUIP_CHAIN_ACTIVE_OFF]. Phases cache activation state, display card-specific triggers, apply packed activations, then poll for refresh completion. Uses gEquipChainSlotRefs and gDuelFieldSlots; clears the processed sprite-row count at phase 3 and after its phase-4 notification. Returns 0 while pending, 1 when complete. Called through advance_equip_display_phase_via_table.
```

#### 0x08098a88 (459 chars)

```text
Ticks equip activation display phases 0..3 for r0=player_side. Uses gEquipChainSlotRefs for the player/slot pair. State is [gDuelFieldSlots+EQUIP_CHAIN_ACTIVE_FROM_FIELD_OFF], the same word as [gP1LifePoints+EQUIP_CHAIN_ACTIVE_OFF]. Caches slot state, queues card-specific displays, and applies packed activations. A phase-2 mismatch writes step 11 and clears the phase. Returns 0 while pending, 1 when complete, through restore_high_regs_epilogue_equip_tick.
```

#### 0x080992e2 (334 chars)

```text
Shared return tail of tick_equip_zone_activation_display_state; requires its existing stack frame. Releases 0xc local bytes, restores r8/r9/r10 and r4-r7, then returns through the saved caller address. Preserves r0. Reached by BL at 0x08098b12, B at 0x08098e38, and fall-through from 0x080992e0. This is not an independent APCS entry.
```

## carve 计划 (R7)

none. 无 rom.s 切割, 无新 ROM 数据块. 既有 jump table 保持原样.

## disasm 计划 (R4)

none. 不清 listing, 不设 TMode, 不新建函数. 共享返回尾已反汇编, 本次只整写 plate.

## 新增 constants / 全局及复用目录

对 `constants/*.inc` 的 5909 条 `.equ/.set` 全量解析并递归求值, 5909 成功, 0 未解析. 包括十六进制、十进制、别名及表达式, 按 value 双向核对. 结果见 `output/refine-run-20260831-194634/seg6-constant-values-evaluated.json`. 本次 22 个新常量 + 1 个新 RAM 全局, 共 23 个新增定义; 不新建 inc 文件. 新补 THUMB equate 的名称与数值 0x0804b165 均无既有命中, 依据本轮 review 修改项 #1 的逐值复核记录.

### NEW (按文件, fixer 添加如下定义)

除 EQUIP_CHAIN_ACTIVE_FROM_FIELD_OFF 外, 以下每个值在现有 constants 全目录求值后均 0 命中. 0x1cfc 的唯一既有命中 DISP_SET_VARIANT_OFF 以 gP1LifePoints 为基址, 指向 0x0201e1dc; 本段基址为 gDuelFieldSlots, 指向 0x0201e20c. 两者域不同, 因此新增基址明确的 offset 名. 不改既有定义.

`constants/card_info.inc`:

```asm
.equ INSECT_SOLDIERS_OF_THE_SKY_CID, 0x00001184  @ Insect Soldiers of the Sky; slot CID; card-stats.s card_0403; pw=07019529.
.equ BIG_SHIELD_GARDNA_CID, 0x0000129c  @ Big Shield Gardna; slot CID; card-stats.s card_0618; pw=65240384.
.equ LUMINOUS_SOLDIER_CID, 0x00001397  @ Luminous Soldier; slot CID; card-stats.s card_0808; pw=57482479.
.equ FAIRY_BOX_CID, 0x000013f9  @ Fairy Box; slot CID; card-stats.s card_0870; pw=21598948.
.equ THE_DARK_DOOR_CID, 0x00001469  @ The Dark Door; slot CID; card-stats.s card_0940; pw=30606547.
.equ CATS_EAR_TRIBE_CID, 0x00001621  @ Cat's Ear Tribe; slot CID; card-stats.s card_1285; pw=95841282.
.equ DISC_FIGHTER_CID, 0x00001752  @ Disc Fighter; slot CID; card-stats.s card_1533; pw=19612721.
.equ PENUMBRAL_SOLDIER_LADY_CID, 0x000017ed  @ Penumbral Soldier Lady; slot CID; card-stats.s card_1658; pw=64751286.
.equ SASUKE_SAMURAI_4_CID, 0x00001829  @ Sasuke Samurai #4; slot CID; card-stats.s card_1709; pw=64538655.
.equ ANCIENT_GEAR_SOLDIER_CID, 0x000018ad  @ Ancient Gear Soldier; slot CID; card-stats.s card_1821; pw=56094445.
.equ DRILLROID_CID, 0x000018f3  @ Drillroid; slot CID; card-stats.s card_1877; pw=71218746.
.equ GOBLIN_ELITE_ATTACK_FORCE_CID, 0x00001912  @ Goblin Elite Attack Force; slot CID; card-stats.s card_1903; pw=85306040.
.equ PREPARE_TO_STRIKE_BACK_CID, 0x00001931  @ Prepare to Strike Back; slot CID; card-stats.s card_1934; pw=04483989.
.equ ETOILE_CYBER_CID, 0x00001952  @ Etoile Cyber; slot CID; card-stats.s card_1953; pw=11460577.
.equ NANOBREAKER_CID, 0x00001963  @ Nanobreaker; slot CID; card-stats.s card_1969; pw=70948327.
.equ MIRROR_WALL_CID_SHIFTED, 0x9c080000  @ MIRROR_WALL_CID << 19; compare against field slot word shifted left by 19.
```

`constants/duel_field.inc`:

```asm
.equ EQUIP_CHAIN_STEP_FROM_FIELD_OFF, 0x00001cf8  @ gDuelFieldSlots+0x1cf8 = gP1LifePoints+EQUIP_CHAIN_STEP_OFF; equip display step word.
.equ EQUIP_CHAIN_ACTIVE_FROM_FIELD_OFF, 0x00001cfc  @ gDuelFieldSlots+0x1cfc = gP1LifePoints+EQUIP_CHAIN_ACTIVE_OFF; equip activation phase word.
.equ EQUIP_ACTIVATION_PACKED_TYPE18, 0x24200000  @ Packed activation: type 18 in bits 30:25 plus bit21; record +2 bits 11:6 = 18, +3 bits 5:4 = 1.
.equ EQUIP_ACTIVATION_PACKED_TYPE20, 0x28200000  @ Packed activation: type 20 in bits 30:25 plus bit21; record +2 bits 11:6 = 20, +3 bits 5:4 = 1.
.equ CHECK_CARD_ID_IS_NORMAL_SUMMON_TYPE_THUMB, 0x0804b165  @ check_card_id_is_normal_summon_type+1; THUMB predicate for count_monster_slots_by_fnptr.
```

`constants/ewram.inc`:

```asm
.equ SPRITE_ROW_PROCESSED_COUNT_OFF, 0x00000482  @ gDuelPhaseFlags+0x482: u16 processed sprite-row count; iterates records from +0x300.
.equ gEquipSlotActivationSnapshot, 0x0201bc7c  @ gEquipChainSlotRefs+0xec: 0x44-byte cached slot activation snapshot written by fill_slot_activation_state_array.
```

### REUSE (按值确认, 每个名字必须沿用)

| value | symbol | 既有定义 |
|---|---|---|
| 0x00000868 | PLAYER_BLOCK_STRIDE | constants/ewram.inc:251 |
| 0x00000fb6 | TIME_WIZARD_CID | constants/card_info.inc:1311 |
| 0x000010c6 | upd_cid_10c6 | constants/card_info.inc:489 |
| 0x00001286 | BLAST_SPHERE_CID | constants/card_info.inc:1360 |
| 0x0000131d | GRAVEKEEPERS_SERVANT_CID | constants/card_info.inc:661 |
| 0x00001476 | ANCIENT_LAMP_CID | constants/card_info.inc:1211 |
| 0x0000148a | DREAMSPRITE_CID | constants/card_info.inc:1212 |
| 0x000014d6 | SPEAR_DRAGON_CID | constants/card_info.inc:1882 |
| 0x00001505 | ASURA_PRIEST_CID | constants/card_info.inc:168 |
| 0x00001507 | SUPER_ROBOLADY_CID | constants/card_info.inc:1728 |
| 0x00001508 | SUPER_ROBOYAROU_CID | constants/card_info.inc:1729 |
| 0x0000153f | ORDEAL_OF_A_TRAVELER_CID | constants/card_info.inc:1023 |
| 0x0000158d | GRAVEKEEPERS_ASSAILANT_CID | constants/card_info.inc:667 |
| 0x000015d2 | GIANT_ORC_CID | constants/card_info.inc:868 |
| 0x000015ff | DIFFUSION_WAVE_MOTION_CID | constants/card_info.inc:176 |
| 0x00001644 | BERSERK_DRAGON_CID | constants/card_info.inc:179 |
| 0x000017d8 | MYSTIC_SWORDSMAN_LV4_CID | constants/card_info.inc:678 |
| 0x000017df | NINJA_GRANDMASTER_SASUKE_CID | constants/card_info.inc:681 |
| 0x000018f2 | STEAMROID_CID | constants/card_info.inc:1869 |
| 0x00001915 | INDOMITABLE_FIGHTER_LEI_LEI_CID | constants/card_info.inc:880 |
| 0x00001954 | VWXYZ_DRAGON_CATAPULT_CANNON_CID | constants/card_info.inc:767 |
| 0x00001958 | EHERO_WILDEDGE_CID | constants/card_info.inc:205 |
| 0x0000195f | HERO_BARRIER_CID | constants/card_info.inc:1255 |
| 0x000019a8 | CYBER_BARRIER_DRAGON_CID | constants/card_info.inc:1709 |
| 0x000019bd | ADHESIVE_EXPLOSIVE_CID | constants/card_info.inc:884 |
| 0x00001cb8 | EQUIP_ZONE_COUNT_TABLE_OFF | constants/duel_field.inc:156 |
| 0x00001d2c | EQUIP_CHAIN_ACTIVE_OFF | constants/duel_field.inc:230 |
| 0x0000801b | OAM_EQUIP_SPRITE_TILE_P2_1B | constants/oam_attr.inc:154 |
| 0x00008020 | SPRITE_RECORD_P2_SIDE | constants/oam_attr.inc:176 |
| 0x0201b290 | gDuelPhaseFlags | constants/ewram.inc:353 |
| 0x0201bb90 | gEquipChainSlotRefs | constants/ewram.inc:317 |
| 0x0201c4e0 | gP1LifePoints | constants/ewram.inc:79 |
| 0x0201c510 | gDuelFieldSlots | constants/ewram.inc:314 |
| 0x0201c520 | gDuelFieldSlotState | constants/ewram.inc:318 |
| 0x0201e2a0 | gDuelCardCtxBase | constants/ewram.inc:218 |

复用选择说明:

- 0x0fb6: `check_value_in_slot_chain` 的 card-ID 过滤和显示参数使用 TIME_WIZARD_CID, 不用同值 EQUIP_ZONE_SPRITE_ATTR. 证据 L9406..9407/L9424..9426.
- 0x1cb8: r9=gDuelFieldSlots, L10720..10724 形成 gDuelFieldSlots+0x1cb8, 因此使用 EQUIP_ZONE_COUNT_TABLE_OFF. 不用 gP1LifePoints 相对的 DUEL_ACTIVE_PLAYER_OFF. 本段只描述该地址首字与 player_side 的比较, 不扩展旧全局的业务含义.
- 0x1cf8/0x1cfc: 保留 base+offset 两槽. gDuelFieldSlots-gP1LifePoints=0x30, 对应 EQUIP_CHAIN_STEP_OFF-0x30/EQUIP_CHAIN_ACTIVE_OFF-0x30. 绝不把 gDuelFieldSlots 槽换成 gP1LifePoints, 也不把 offset 数值改成 0x1d28/0x1d2c.
- 0x18f1: GYROID_CID 已存在于 constants/card_info.inc:1905. 本段无存储该值的 literal 槽, 不新增/重复定义它. 0x18f2 的三个槽复用 STEAMROID_CID, 0x18f3 独立新增 DRILLROID_CID.

## 5.1 登记 (Rule 3)

none. 本段无未引用裸数据块. 不把共享返回尾列入未引用登记.

## 消费者证据 (R6)

下列模块行号均指生成本 proposal 时的 `asm/12_equip_activation_scan.s`. 范围内池槽使用点已逐个读取; 完整旧名、值、使用点列表在 `output/refine-run-20260831-194634/seg6-plan.json`.

### 关键结构与常量

| 项目 | 消费者/ROM 证据 | 结论 | 置信度 |
|---|---|---|---|
| gEquipChainSlotRefs | L9111..9116, L9854..9872 | +0/+4 为 player pair, +0x1c/+0x20 为 slot pair; +0x10 为一次执行闩锁, 不是旧板的 effect_flags | high |
| gDuelFieldSlots, PLAYER_BLOCK_STRIDE | L9236..9246, L9875..9898, L10631..10642 | 地址为 base+(side&1)*0x868+slot*0x14; 首字低13位为 CID | high |
| gDuelFieldSlotState | L9293..9306, L9677..9686 | 与 field slot 基址相差 0x10; 读取 bit1/bit5 等状态 | high |
| gDuelCardCtxBase | L9570..9576 | 读取 +4 与输入 player_side 比较, 决定 display index 更新 | high |
| gEquipSlotActivationSnapshot | L9219..9220, L9953..9955; fill_slot_activation_state_array L6991..7056 | 0x0201bc7c=gEquipChainSlotRefs+0xec. 输出 +0/+4, +8+i*4/+0x1c+i*4/+0x30+i*4, i=0..4; 最大写入 offset 0x40, 共0x44字节 | high |
| SPRITE_ROW_PROCESSED_COUNT_OFF | L9781..9785, L9816..9825; asm/05_equip_eligibility_a.s:9992..10036 and :12916..12929 | gDuelPhaseFlags+0x482 的 u16 当前已处理行数. case8 从该值迭代到 +0x480 行数, 每条0x18字节并递增; 另一消费者从 count-1 反向遍历 | high |
| EQUIP_CHAIN_ACTIVE_FROM_FIELD_OFF | L9883..9904 | r4=gDuelFieldSlots, DWORD_08098b24=0x1cfc; 0x0201c510+0x1cfc=0x0201e20c=0x0201c4e0+0x1d2c | high |
| EQUIP_CHAIN_STEP_FROM_FIELD_OFF | L10319..10328 | 检测 mismatch 非0时写 [gDuelFieldSlots+0x1cf8]=11, 并清 phase; 0x0201e208=gP1LifePoints+0x1d28 | high |
| EQUIP_ZONE_COUNT_TABLE_OFF | L10720..10724 | r9=gDuelFieldSlots, ldr [r9+0x1cb8] 后与 r10(配对 player) 比较; 使用现有同地址域常量 | high |
| MIRROR_WALL_CID_SHIFTED | L9288..9292; data/card-stats.s:10363 | (slot_word<<19)==0x9c080000 等价低13位 CID==0x1381. 0x1381<<19=0x9c080000 | high |
| EQUIP_ACTIVATION_PACKED_TYPE18/20 | L9637..9671, L10222..10248; asm/06_equip_eligibility_b.s:18716..18746 | 0x24200000=(18<<25)|(1<<21); 0x28200000=(20<<25)|(1<<21). 解包至 record+2 bits[11:6]=18/20, record+3 bits[5:4]=1. 不命名为 field-slot card type 或硬件 OAM mask | high |
| THUMB predicate 0x0804b165 | L9355..9357; asm/05_equip_eligibility_a.s:4538..4545 | 传给 count_monster_slots_by_fnptr 的 r1 回调; 函数现名 check_card_id_is_normal_summon_type, 指针保留+1 | high |
| SPRITE_RECORD_P2_SIDE / OAM_EQUIP_SPRITE_TILE_P2_1B | L9438..9449, L9932..9942 | P1 用 inline0x20/0x1b, P2 从 literal 取0x8020/0x801b; 复用已定义符号 | high |

### CID 证据 (含所有 CID 值)

每行列出同值池槽的全部直接 LDR 使用点. BST 比较的值来自 slot_word 低13位或配对 slot CID; count/check/queue 调用的 CID 参数由相应寄存器传递. 所有已分配 CID 均由本地 card-stats 确认, 不依赖旧 proposal 的卡名.

| CID | 常量 | 卡表证据 | 模块直接使用行 | 置信度 |
|---|---|---|---|---|
| 0x0fb6 | TIME_WIZARD_CID | data/card-stats.s:223, Time Wizard | 9406, 9424 | high |
| 0x10c6 | upd_cid_10c6 | data/cards-ids-array.s:304, icid=0x10c6 -> 0xffff | 10655 | high |
| 0x1184 | INSECT_SOLDIERS_OF_THE_SKY_CID | data/card-stats.s:5254, Insect Soldiers of the Sky | 10461 | high |
| 0x1286 | BLAST_SPHERE_CID | data/card-stats.s:7763, Blast Sphere | 10866 | high |
| 0x129c | BIG_SHIELD_GARDNA_CID | data/card-stats.s:8049, Big Shield Gardna | 10389 | high |
| 0x131d | GRAVEKEEPERS_SERVANT_CID | data/card-stats.s:9245, Gravekeeper's Servant | 9126 | high |
| 0x1397 | LUMINOUS_SOLDIER_CID | data/card-stats.s:10519, Luminous Soldier | 10456, 10658 | high |
| 0x13f9 | FAIRY_BOX_CID | data/card-stats.s:11325, Fairy Box | 9701 | high |
| 0x1469 | THE_DARK_DOOR_CID | data/card-stats.s:12235, The Dark Door | 9228 | high |
| 0x1476 | ANCIENT_LAMP_CID | data/card-stats.s:12365, Ancient Lamp | 10860 | high |
| 0x148a | DREAMSPRITE_CID | data/card-stats.s:12599, Dreamsprite | 10891 | high |
| 0x14d6 | SPEAR_DRAGON_CID | data/card-stats.s:13405, Spear Dragon | 10088, 10104 | high |
| 0x1505 | ASURA_PRIEST_CID | data/card-stats.s:13951, Asura Priest | 10049, 10117 | high |
| 0x1507 | SUPER_ROBOLADY_CID | data/card-stats.s:13977, Super Robolady | 10474 | high |
| 0x1508 | SUPER_ROBOYAROU_CID | data/card-stats.s:13990, Super Roboyarou | 10451, 10650 | high |
| 0x153f | ORDEAL_OF_A_TRAVELER_CID | data/card-stats.s:14614, Ordeal of a Traveler | 9696 | high |
| 0x158d | GRAVEKEEPERS_ASSAILANT_CID | data/card-stats.s:15212, Gravekeeper's Assailant | 9595 | high |
| 0x15d2 | GIANT_ORC_CID | data/card-stats.s:15901, Giant Orc | 10025 | high |
| 0x15ff | DIFFUSION_WAVE_MOTION_CID | data/card-stats.s:16395, Diffusion Wave-Motion | 9956, 9990 | high |
| 0x1621 | CATS_EAR_TRIBE_CID | data/card-stats.s:16720, Cat's Ear Tribe | 10680 | high |
| 0x1644 | BERSERK_DRAGON_CID | data/card-stats.s:17032, Berserk Dragon | 10063 | high |
| 0x1752 | DISC_FIGHTER_CID | data/card-stats.s:19944, Disc Fighter | 10822 | high |
| 0x17d8 | MYSTIC_SWORDSMAN_LV4_CID | data/card-stats.s:21309, Mystic Swordsman LV4 | 10183 | high |
| 0x17df | NINJA_GRANDMASTER_SASUKE_CID | data/card-stats.s:21387, Ninja Grandmaster Sasuke | 10163 | high |
| 0x17ed | PENUMBRAL_SOLDIER_LADY_CID | data/card-stats.s:21569, Penumbral Soldier Lady | 10484, 10675 | high |
| 0x1829 | SASUKE_SAMURAI_4_CID | data/card-stats.s:22232, Sasuke Samurai #4 | 10194, 10262 | high |
| 0x18ad | ANCIENT_GEAR_SOLDIER_CID | data/card-stats.s:23688, Ancient Gear Soldier | 9534 | high |
| 0x18f2 | STEAMROID_CID | data/card-stats.s:24403, Steamroid | 10479, 10690 | high |
| 0x18f3 | DRILLROID_CID | data/card-stats.s:24416, Drillroid | 10825 | high |
| 0x1912 | GOBLIN_ELITE_ATTACK_FORCE_CID | data/card-stats.s:24754, Goblin Elite Attack Force | 10066 | high |
| 0x1915 | INDOMITABLE_FIGHTER_LEI_LEI_CID | data/card-stats.s:24793, Indomitable Fighter Lei Lei | 10058 | high |
| 0x1931 | PREPARE_TO_STRIKE_BACK_CID | data/card-stats.s:25157, Prepare to Strike Back | 9721 | high |
| 0x1952 | ETOILE_CYBER_CID | data/card-stats.s:25404, Etoile Cyber | 10494 | high |
| 0x1954 | VWXYZ_DRAGON_CATAPULT_CANNON_CID | data/card-stats.s:25430, VWXYZ-Dragon Catapult Cannon | 9615 | high |
| 0x1958 | EHERO_WILDEDGE_CID | data/card-stats.s:25482, Elemental Hero Wildedge | 10078 | high |
| 0x195f | HERO_BARRIER_CID | data/card-stats.s:25560, Hero Barrier | 9348 | high |
| 0x1963 | NANOBREAKER_CID | data/card-stats.s:25612, Nanobreaker | 10208 | high |
| 0x19a8 | CYBER_BARRIER_DRAGON_CID | data/card-stats.s:26236, Cyber Barrier Dragon | 9393 | high |
| 0x19bd | ADHESIVE_EXPLOSIVE_CID | data/card-stats.s:26431, Adhesive Explosive | 10895 | high |

0x10c6 调查闭环: data/card-stats.s 对 slot=0x10C6 无匹配; data/cards-ids-array.s:304 明确 `.hword 0xFFFF`, 因而没有对应 cid 卡名/描述条目. 本段 L10655..10657 的比较走 0x080990f8, L10697..10701 设置 mode=1 并跳转至 L10711 的 check_slot_zone_bit_eligible. 中性符号 `upd_cid_10c6` 已由 constants/card_info.inc:489 定义, 本次复用该符号, 不给未分配 ID 赋卡名. `constants/rom_data.inc` 的 `card_10C6` 是 0x0982daba 数据地址标签, 不表示内部 CID 0x10c6.

0x18f3 调查闭环: data/cards-ids-array.s:2397 指向 cid1877; data/card-stats.s:24416/52889 均为 Drillroid, 密码71218746; data/card-names.s:25696..25708 与 text/card-names/en.txt:5505 均给出 Drillroid. L10822..10829 比较 DISC_FIGHTER_CID 或 DRILLROID_CID 后进入同一个 packed-type20 发动路径.

### PLATE 订正证据

- 0x080984d0: L9113..9115 的 r1 为 slot index, eligibility flags 是 callee 返回到 r8 的值. L9121..9125 检查其 bit1; L9137..9141 分别是 enqueue_sprite_attr_by_sign 与 enqueue_equip_zone_sprite_attr_full, 旧板的两次同调用描述错误. L9143..9148 构造 TOLL_CID=0x1320, L9160..9162 构造500. 一次闩锁在 L9116..9120.
- 0x08098564: 0x4680@0x08098570 = mov r8,r0, 输入 player_side 未被废弃. L9253/L9266/L9346/L9550 使用 r8; L9451 为返回0, L9833 为返回1. 状态0..4由池槽0x1d2c驱动. 不再写无 APCS 输入/void 返回.
- 0x08098a88: 0x4680@0x08098a94 = mov r8,r0. L9883..9904 表明 phase 的真实基址是 gDuelFieldSlots. L10319..10328 属于 phase2, 非旧板 phase3; mismatch非0重启 step=11. L9917..9918 返回1, L10948返回0.
- 0x080992e2: L10952..10958 的实际字节为 add sp,#0xc; pop r3-r5; mov r8/r9/r10; pop r4-r7; pop r1; bx r1. 不修改 r0. L9918 是 BL, L10328 是 B, L10948 自然续接; 该尾依赖主函数栈帧, 没有独立 push.
- 上游函数指针表位于 0x09e5aaec. 三个主函数各一个 THUMB 指针, table consumer 为 advance_equip_display_phase_via_table, asm/12_equip_activation_scan.s:16725..16747. consumer 保留并转发 player_side, 子函数返回非0时推进 step.

## 自检记录 (executor 原记录 + fixer 模式 A 同步, 不作评分)

- EQ=80, REF=39 (RAM 38 + switch 1), RENAME=7. 三表交集为空, 并集=126 个原始自动名槽; 区间外项=0, 重复地址=0, 缺项=0. 辅助 DATA/USER_DEFINED 导航引用 1 条, 不参与主分类计数.
- 126 个槽值沿用 executor 的 ROM/asm 核对记录, 本轮未更改数值. 分类同步为 80 个 EQ、39 个 REF、7 个 RENAME; 0x080987bc 的主分类改为 EQ, 值仍为 0x0804b165.
- 22 个新常量+1个新 RAM 全局, 共23个定义. 原有定义的逐值检查沿用 executor 记录, 新增 THUMB equate 的无同名/同值命中沿用 review #1. 唯一非0命中新增项为0x1cfc, 以上给出异基址证据. 无重复新增 Gyroid 或未分配 CID 名.
- 126 个新槽标签均匹配 `^[a-z][a-z0-9_]+$`, 唯一且与当前 asm/constants 既有标签无碰撞.
- 全部 PLATE、RENAME EOL、EQ 回调 EOL、拟写 constants 注释为 ASCII; 4 块 PLATE 每块 <=500字符. PLATE full rewrite覆盖本段全部4个旧板, 包括共享返回尾, 无遗留 FUN_/DAT_ 引用.
- ROM_INCBIN/.byte=0, carve=0, disasm=0, 5.1=0. 既有 switch 表偶地址不变, 回调指针 +1 保持 ROM 值0x0804b165.
- Executor 仅写此 proposal 和指定 output 扫描文件. 未改 Ghidra/asm/constants/进度表, 未 build, 未 commit.

### Fixer 模式 A: review #1 五个子项完成自检

1. 0x080987bc 已从 REF 主表移入 EQ 主表, 使用指定四元组并保留槽名; 三表仍为80/39/7, 总槽126.
2. NEW 的 `constants/duel_field.inc` 目录已补 THUMB equate, 数值为0x0804b165; Ghidra data-equate 值也明确为同值.
3. 已列辅助 `DATA/USER_DEFINED` 引用到0x0804b164, 保留现名 FUNCTION 主符号, 不提升 LABEL, 不在0x0804b165创建标签或函数; 不重复计入REF.
4. 已增加指定 ASCII EOL, 明确 `resolve_word_symbol=None -> resolve_word_equate` fallback 的按名输出, 保留等式与ROM四字节验收.
5. 提案说明、自检、报告与 `seg6-plan.json`/`seg6-selfcheck.json` 已同步到80EQ/39REF/7RENAME、22常量+1RAM全局; 五项偶地址switch表保持原状. 本轮只检查修改项是否落实, 未重新评分或修改review, 未落地Ghidra/asm/constants, 未build、未commit.

执行输入: 本提案为唯一真源, `output/refine-run-20260831-194634/seg6-plan.json` 已同步主表、辅助引用、EOL及导出验收; `seg6-selfcheck.json` 区分沿用的原检查与本轮五项完成检查. 已评审的修改前版本保存在 `output/refine-run-20260831-194634/F12-Seg-6.proposal.before-fix1.md`, SHA256 `390ec44dc0edc6263b157f5a6aa9c1a150750dbbf04b8199e6a00d42b1f076ac`.

## 求助

none. 0x10c6 的未分配状态有本地映射表证据且已有中性常量, 0x18f3 已确认 Drillroid, 无低置信度未决语义.

## Executor Report: F12-Seg-6

- 槽: EQ=80 REF=39 RENAME=7 FUNC_RENAME=0 PLATE=4; EQ辅助导航引用=1, EQ EOL=1
- carve=0 disasm=0 range 5.1=0
- 新增 constants/全局: constants/card_info.inc 16个, constants/duel_field.inc 5个, constants/ewram.inc 1个常量+1个RAM全局; 总数23 (22常量+1RAM全局)
- 求助: none
- proposal: doc/dev/refine/F12-Seg-6.proposal.md
