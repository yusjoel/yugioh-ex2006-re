# Refine Proposal: F13-Seg-2 [0x0809e6f4..0x0809f744)

本提案仅为 executor 产物, 未评分, 未写 Ghidra, 未运行 build, 未 stage/commit. 输入以当前 asm/13_equip_placement.s 为准, 不使用建档时的旧行号或旧函数名. 执行依据: .agents/skills/refine-loop/SKILL.md, .codex/agents/refine-executor.toml, doc/dev/methodology/refine-loop.md 的 R1-R9 和 C1-C13. 用户禁止 commit 的要求覆盖旧流程文字.

## 段测绘

- 边界: [0x0809e6f4,0x0809f744), 4176 B. 当前源码 SHA256: `3218ebbbd6743fab7ebf47d96c7ad61c08fd64972dbd9fc5ea8fa62371681bd7`.
- 59 个既有 Function, 包括无 push 的 leaf 0x0809e904. 不新建 Function. dispatcher 0x0809e6f4 原不连续 body 的两个 range 均在本段.
- 原自动 4B 槽 126 = 103 DAT + 3 DWORD + 20 PTR; 另 7 个无标签 switch word 和裸块头 DAT_0809e74c. 原已定义 word 合计 133. 本次 R4 暴露 25 新池, 最终 158 个 word 全部唯一覆盖.
- 唯一裸块 [0x0809e74c,0x0809e8f4), 424 B, 分解为 145 条 Thumb 指令 / 316 B, 25 个池 / 100 B, 4 个 2B 零对齐 / 8 B. 无额外 .byte 块. 4176 B 逐字节连续覆盖见 map/projected_items.
- 操作: EQ=119, REF=20, RENAME=19, FUNC_RENAME=4, PLATE=59. 槽 EOL=158, case EOL=8. NEW constants=24, 唯一 REUSE constants=48. 数据目标 USER ROM LABEL=9 (1 表头 + 8 case, 表头同时是首 word 槽); 与158槽名合并去重后共166个静态ROM LABEL地址. 无新增 RAM global, 无 ROM_FUNCTION equate, 无外部 carve, §5.1=0.

| 入口 | 当前函数名 | 源码行 |
| --- | --- | --- |
| 0x0809e6f4 | dispatch_equip_activation_state_by_subphase | asm/13_equip_placement.s:2101 |
| 0x0809e904 | check_activation_phase_counter_is_six | asm/13_equip_placement.s:2153 |
| 0x0809e920 | scan_monster_zone_for_equip_activation_by_card | asm/13_equip_placement.s:2171 |
| 0x0809e9e0 | scan_trap_zone_for_equip_activation_by_card | asm/13_equip_placement.s:2272 |
| 0x0809eaa0 | scan_trap_zone_for_equip_activation_jam_breeding_machine | asm/13_equip_placement.s:2373 |
| 0x0809eab0 | scan_trap_zone_for_equip_activation_blind_destruction | asm/13_equip_placement.s:2383 |
| 0x0809eac0 | scan_trap_zone_for_equip_activation_ominous_fortunetelling | asm/13_equip_placement.s:2393 |
| 0x0809ead0 | scan_trap_zone_for_equip_activation_needle_wall | asm/13_equip_placement.s:2403 |
| 0x0809eae0 | scan_trap_zone_for_equip_activation_dangerous_machine_type6 | asm/13_equip_placement.s:2413 |
| 0x0809eaf0 | scan_equip_zone_for_dimensionhole | asm/13_equip_placement.s:2423 |
| 0x0809eb34 | scan_monster_zone_for_equip_activation_reserved_icid_f | asm/13_equip_placement.s:2460 |
| 0x0809eb44 | scan_monster_zone_for_equip_activation_lava_golem | asm/13_equip_placement.s:2470 |
| 0x0809eb54 | scan_monster_zone_slots_for_equip_activation_reserved_icid_g | asm/13_equip_placement.s:2480 |
| 0x0809ec04 | scan_monster_zone_for_equip_activation_spirit_of_the_breeze | asm/13_equip_placement.s:2571 |
| 0x0809ec14 | scan_monster_zone_for_equip_activation_dancing_fairy | asm/13_equip_placement.s:2581 |
| 0x0809ec24 | scan_monster_zone_for_equip_activation_cure_mermaid | asm/13_equip_placement.s:2591 |
| 0x0809ec34 | scan_monster_slots_for_equip_activation_marie_the_fallen_one | asm/13_equip_placement.s:2601 |
| 0x0809ece0 | scan_trap_zone_for_equip_activation_life_absorbing_machine | asm/13_equip_placement.s:2694 |
| 0x0809ecf0 | scan_trap_zone_for_equip_activation_senri_eye | asm/13_equip_placement.s:2704 |
| 0x0809ed00 | scan_monster_zone_for_equip_activation_white_magician_pikeru | asm/13_equip_placement.s:2714 |
| 0x0809ed10 | scan_monster_zone_for_equip_activation_ebon_magician_curran | asm/13_equip_placement.s:2724 |
| 0x0809ed20 | scan_monster_zone_for_equip_activation_princess_pikeru | asm/13_equip_placement.s:2734 |
| 0x0809ed30 | scan_monster_zone_for_equip_activation_princess_curran | asm/13_equip_placement.s:2744 |
| 0x0809ed40 | scan_monster_zone_for_equip_activation_bowganian | asm/13_equip_placement.s:2754 |
| 0x0809ed50 | scan_all_monster_zone_slots_for_equip_activation_infernalqueen_archfiend | asm/13_equip_placement.s:2764 |
| 0x0809ee14 | scan_all_zone_slots_for_equip_lp_indicator_graverobbers_retribution | asm/13_equip_placement.s:2865 |
| 0x0809eed8 | scan_all_zone_slots_for_lp_indicator_burning_land | asm/13_equip_placement.s:2967 |
| 0x0809ef88 | scan_trap_zone_for_equip_activation_mask_of_dispel | asm/13_equip_placement.s:3057 |
| 0x0809ef98 | scan_trap_zone_for_equip_activation_mask_of_accursed | asm/13_equip_placement.s:3067 |
| 0x0809efa8 | scan_trap_zone_for_equip_activation_nightmare_wheel | asm/13_equip_placement.s:3077 |
| 0x0809efb8 | scan_trap_zone_for_equip_activation_snatch_steal | asm/13_equip_placement.s:3087 |
| 0x0809efd0 | scan_trap_zone_for_equip_activation_brain_jacker | asm/13_equip_placement.s:3101 |
| 0x0809efe8 | scan_trap_zone_for_equip_activation_falling_down | asm/13_equip_placement.s:3115 |
| 0x0809f000 | scan_trap_zone_for_equip_activation_the_eye_of_truth | asm/13_equip_placement.s:3129 |
| 0x0809f018 | scan_trap_zone_for_equip_activation_minor_goblin_official | asm/13_equip_placement.s:3143 |
| 0x0809f030 | scan_trap_zone_for_equip_activation_blast_sphere | asm/13_equip_placement.s:3157 |
| 0x0809f048 | scan_trap_zone_for_equip_activation_adhesive_explosive | asm/13_equip_placement.s:3171 |
| 0x0809f060 | scan_monster_zone_for_equip_activation_malice_ascendant | asm/13_equip_placement.s:3185 |
| 0x0809f078 | scan_trap_slots_for_kiseitai_equip_chain_sprite | asm/13_equip_placement.s:3199 |
| 0x0809f158 | scan_monster_zone_chain_for_equip_activation | asm/13_equip_placement.s:3312 |
| 0x0809f1fc | scan_monster_zone_chain_for_equip_activation_sinister_serpent | asm/13_equip_placement.s:3399 |
| 0x0809f20c | scan_monster_zone_chain_for_equip_activation_treeborn_frog | asm/13_equip_placement.s:3409 |
| 0x0809f21c | scan_equip_zone_for_special_summon_activation_return_zombie | asm/13_equip_placement.s:3419 |
| 0x0809f348 | scan_monster_zone_slots_for_equip_activation_mucus_yolk | asm/13_equip_placement.s:3573 |
| 0x0809f40c | scan_monster_zone_for_equip_activation_legendary_fiend | asm/13_equip_placement.s:3674 |
| 0x0809f41c | scan_monster_zone_for_equip_activation_exodia_necross | asm/13_equip_placement.s:3684 |
| 0x0809f42c | scan_monster_zone_for_equip_activation_amazoness_blowpiper | asm/13_equip_placement.s:3694 |
| 0x0809f43c | scan_monster_zone_for_equip_activation_agent_of_wisdom_mercury | asm/13_equip_placement.s:3704 |
| 0x0809f44c | scan_field_slots_for_lv_monster_equip_activation | asm/13_equip_placement.s:3714 |
| 0x0809f538 | scan_equip_zone_for_entity_sprite_and_activation | asm/13_equip_placement.s:3843 |
| 0x0809f584 | scan_equip_zone_for_equip_activation_revival_jam | asm/13_equip_placement.s:3883 |
| 0x0809f594 | scan_equip_zone_for_equip_activation_vampire_lord | asm/13_equip_placement.s:3893 |
| 0x0809f5a4 | scan_equip_zone_for_equip_activation_sacred_phoenix | asm/13_equip_placement.s:3903 |
| 0x0809f5b4 | scan_equip_zone_for_entity_sprite_activation_curse_of_vampire | asm/13_equip_placement.s:3913 |
| 0x0809f5c4 | scan_equip_zone_for_entity_sprite_activation_curse_of_vampire_opponent | asm/13_equip_placement.s:3923 |
| 0x0809f5dc | scan_spell_trap_zone_for_equip_activation_via_packed_attr | asm/13_equip_placement.s:3937 |
| 0x0809f704 | scan_spell_trap_zone_for_equip_activation_reserved_icid_e | asm/13_equip_placement.s:4090 |
| 0x0809f71c | scan_spell_trap_zone_for_equip_activation_recycle | asm/13_equip_placement.s:4104 |
| 0x0809f72c | scan_monster_zone_for_equip_activation_aqua_spirit_opponent | asm/13_equip_placement.s:4114 |

## 数据块分类 (Rule 2/3)

| 块 | 全 ROM raw / THUMB|1 | 分类 | 闭合证据 |
| --- | --- | --- | --- |
| 0x0809e74c size 0x1a8 | raw=9, odd=0; 全部 212 个偶地址候选逐一搜索 | disasm | 8 个真引用来自既有 even switch 表; 1 个 raw 是有消费者的未压缩音频样本字节偶合. 不能以 0 引用登记. |

逐候选完整命中列表: `f13-seg2-block-refscan.json`. 真引用及额外命中如下, 所有 raw 计数均保留, 不删除偶合命中.

| 指针源 | 原值 / 目标 | 类型 |
| --- | --- | --- |
| 0x0809e72c | 0x0809e74c | 既有 DATA 表项, even Thumb case |
| 0x0809e730 | 0x0809e76c | 既有 DATA 表项, even Thumb case |
| 0x0809e734 | 0x0809e7c4 | 既有 DATA 表项, even Thumb case |
| 0x0809e738 | 0x0809e7d8 | 既有 DATA 表项, even Thumb case |
| 0x0809e73c | 0x0809e800 | 既有 DATA 表项, even Thumb case |
| 0x0809e740 | 0x0809e850 | 既有 DATA 表项, even Thumb case |
| 0x0809e744 | 0x0809e894 | 既有 DATA 表项, even Thumb case |
| 0x0809e748 | 0x0809e8b0 | 既有 DATA 表项, even Thumb case |
| 0x081feb5e | 0x0809e812 | signed audio bytes 12 e8 09 08; 目标是 e810 BL 的后半字 |

额外命中源 0x081feb5e 属于 instrument table 0x081d7ea0 的零基第 37 项: word@0x081d7f34=0x081fb9d0 (asm/24_libc_runtime.s:9637). 样本 12B 头为 {0x00000c2d,0x00003a24,0xffffffff}; payload=[0x081fb9dc,0x081ff400), 14884 B, 恰好接第 38 项. 该四字节处是样本偏移 0x3182, 有符号值 {18,-24,9,8}, 不是指针.
消费者闭合: asm/23_sound_cardlist_libc.s:13336,13357,13359 取 table[index]; :13409,13411,13415,13418,13425 读取长度, base+12 作为样本地址, 长度符号位控制压缩 flag. 本样本正长度, 不设置压缩 flag; :14856-14863 正常混音分支执行 0x0810e14c LDRSB. 完整机器码和头字段见 audio-raw-hit.json. TMode=0 的 undefined 源窗口不是 ISA 证明, 本判定不依赖强制反汇编源数据.

## 符号化计划 (R1/R2/R3)

以下三个分组在各组内按地址递增. 全部操作的单一地址序清单、原 label/value、真实 LDR uses、Ghidra 全对象前态和 EOL 在 `f13-seg2-plan.json/actions` 中. EQ/REF 使用标准四元组; RENAME 只改槽标签和 ASCII EOL, 原引用逐字段保留. 下表是该机器清单的无损投影, 不另设互相重叠的动作.

### EQ_SLOTS

- `(0x0809e720, 0x00001ce8, P1LP_BLOCK2_OFF_1CE8, equip_scan_player_offset_9e720)` - REUSE constants/ewram.inc:276
- `(0x0809e724, 0x00001d34, EQUIP_ACTIVATION_SUBPHASE_OFF, equip_scan_subphase_offset_9e724)` - NEW constants/duel_field.inc
- `(0x0809e760, 0x00001cf8, EQUIP_ACTIVATION_SAVED_PHASE_OFF, equip_scan_saved_phase_offset_9e760)` - NEW constants/duel_field.inc
- `(0x0809e764, 0x00001cf4, P2LP_BLOCK2_OFF_1CF4, equip_scan_phase_offset_9e764)` - REUSE constants/ewram.inc:277
- `(0x0809e768, 0x00001d34, EQUIP_ACTIVATION_SUBPHASE_OFF, equip_scan_subphase_offset_9e768)` - NEW constants/duel_field.inc
- `(0x0809e7a0, 0x0000151e, LAST_TURN_CID, equip_scan_cid_9e7a0)` - REUSE constants/card_info.inc:1447
- `(0x0809e7a4, 0x0000011d, CARD_DISPLAY_OP31_LP_BAR_SUB, equip_scan_display_op31_subtype_9e7a4)` - REUSE constants/card_info.inc:1512
- `(0x0809e7ac, 0x00001d34, EQUIP_ACTIVATION_SUBPHASE_OFF, equip_scan_subphase_offset_9e7ac)` - NEW constants/duel_field.inc
- `(0x0809e7c0, 0x00001d34, EQUIP_ACTIVATION_SUBPHASE_OFF, equip_scan_subphase_offset_9e7c0)` - NEW constants/duel_field.inc
- `(0x0809e7d4, 0x0000151e, LAST_TURN_CID, equip_scan_cid_9e7d4)` - REUSE constants/card_info.inc:1447
- `(0x0809e7f4, 0x151e0000, LAST_TURN_SETUP_EXTRA_WORD, equip_scan_last_turn_extra_9e7f4)` - NEW constants/duel_field.inc
- `(0x0809e7fc, 0x00001d34, EQUIP_ACTIVATION_SUBPHASE_OFF, equip_scan_subphase_offset_9e7fc)` - NEW constants/duel_field.inc
- `(0x0809e84c, 0x00001d34, EQUIP_ACTIVATION_SUBPHASE_OFF, equip_scan_subphase_offset_9e84c)` - NEW constants/duel_field.inc
- `(0x0809e86c, 0x00001cf8, EQUIP_ACTIVATION_SAVED_PHASE_OFF, equip_scan_saved_phase_offset_9e86c)` - NEW constants/duel_field.inc
- `(0x0809e870, 0x00001d28, EQUIP_CHAIN_STEP_OFF, equip_scan_chain_step_offset_9e870)` - REUSE constants/duel_field.inc:229
- `(0x0809e888, 0x00001d28, EQUIP_CHAIN_STEP_OFF, equip_scan_chain_step_offset_9e888)` - REUSE constants/duel_field.inc:229
- `(0x0809e88c, 0x00001d2c, EQUIP_CHAIN_ACTIVE_OFF, equip_scan_chain_active_offset_9e88c)` - REUSE constants/duel_field.inc:230
- `(0x0809e890, 0x00001d34, EQUIP_ACTIVATION_SUBPHASE_OFF, equip_scan_subphase_offset_9e890)` - NEW constants/duel_field.inc
- `(0x0809e8ac, 0x00001d34, EQUIP_ACTIVATION_SUBPHASE_OFF, equip_scan_subphase_offset_9e8ac)` - NEW constants/duel_field.inc
- `(0x0809e8ec, 0x00001cf8, EQUIP_ACTIVATION_SAVED_PHASE_OFF, equip_scan_saved_phase_offset_9e8ec)` - NEW constants/duel_field.inc
- `(0x0809e8f0, 0x00001d34, EQUIP_ACTIVATION_SUBPHASE_OFF, equip_scan_subphase_offset_9e8f0)` - NEW constants/duel_field.inc
- `(0x0809e91c, 0x00001d34, EQUIP_ACTIVATION_SUBPHASE_OFF, equip_scan_subphase_offset_9e91c)` - NEW constants/duel_field.inc
- `(0x0809e9b4, 0x00001d24, EQUIP_ACTIVATION_SCAN_CURSOR_OFF, equip_scan_cursor_offset_9e9b4)` - REUSE constants/duel_field.inc:605
- `(0x0809e9b8, 0x0000ffff, EQUIP_ACTIVATION_CID_U16_MASK, equip_scan_cid_mask_9e9b8)` - REUSE constants/duel_field.inc:606
- `(0x0809e9bc, 0x00000868, PLAYER_BLOCK_STRIDE, equip_scan_player_stride_9e9bc)` - REUSE constants/ewram.inc:251
- `(0x0809ea74, 0x00001d24, EQUIP_ACTIVATION_SCAN_CURSOR_OFF, equip_scan_cursor_offset_9ea74)` - REUSE constants/duel_field.inc:605
- `(0x0809ea78, 0x0000ffff, EQUIP_ACTIVATION_CID_U16_MASK, equip_scan_cid_mask_9ea78)` - REUSE constants/duel_field.inc:606
- `(0x0809ea7c, 0x00000868, PLAYER_BLOCK_STRIDE, equip_scan_player_stride_9ea7c)` - REUSE constants/ewram.inc:251
- `(0x0809eaac, 0x000013ff, JAM_BREEDING_MACHINE_CID, equip_scan_cid_9eaac)` - REUSE constants/card_info.inc:405
- `(0x0809eabc, 0x00001494, BLIND_DESTRUCTION_CID, equip_scan_cid_9eabc)` - NEW constants/card_info.inc
- `(0x0809eacc, 0x00001519, OMINOUS_FORTUNETELLING_CID, equip_scan_cid_9eacc)` - REUSE constants/card_info.inc:1022
- `(0x0809eadc, 0x00001545, NEEDLE_WALL_CID, equip_scan_cid_9eadc)` - NEW constants/card_info.inc
- `(0x0809eaec, 0x00001738, DANGEROUS_MACHINE_TYPE6_CID, equip_scan_cid_9eaec)` - REUSE constants/card_info.inc:1522
- `(0x0809eb24, 0x0000140c, DIMENSIONHOLE_CID, equip_scan_cid_9eb24)` - NEW constants/card_info.inc
- `(0x0809eb28, 0x0450140c, DIMENSIONHOLE_PACKED_ACTIVATION_ATTR, equip_scan_dimensionhole_attr_9eb28)` - NEW constants/duel_field.inc
- `(0x0809eb40, 0x000011cf, get_card_lp_cost_by_id_cid_11cf, equip_scan_cid_9eb40)` - REUSE constants/card_info.inc:1061
- `(0x0809eb50, 0x00001578, LAVA_GOLEM_CID, equip_scan_cid_9eb50)` - REUSE constants/card_info.inc:403
- `(0x0809ebe0, 0x00001d24, EQUIP_ACTIVATION_SCAN_CURSOR_OFF, equip_scan_cursor_offset_9ebe0)` - REUSE constants/duel_field.inc:605
- `(0x0809ebe4, 0x00001338, EQUIP_ACTIVATION_UNMAPPED_CID_1338, equip_scan_cid_9ebe4)` - NEW constants/card_info.inc
- `(0x0809ebe8, 0x00000868, PLAYER_BLOCK_STRIDE, equip_scan_player_stride_9ebe8)` - REUSE constants/ewram.inc:251
- `(0x0809ec10, 0x00001450, SPIRIT_OF_THE_BREEZE_CID, equip_scan_cid_9ec10)` - NEW constants/card_info.inc
- `(0x0809ec20, 0x00001451, DANCING_FAIRY_CID, equip_scan_cid_9ec20)` - NEW constants/card_info.inc
- `(0x0809ec30, 0x00001454, CURE_MERMAID_CID, equip_scan_cid_9ec30)` - NEW constants/card_info.inc
- `(0x0809ec50, 0x00001d24, EQUIP_ACTIVATION_SCAN_CURSOR_OFF, equip_scan_cursor_offset_9ec50)` - REUSE constants/duel_field.inc:605
- `(0x0809ecc8, 0x00000868, PLAYER_BLOCK_STRIDE, equip_scan_player_stride_9ecc8)` - REUSE constants/ewram.inc:251
- `(0x0809eccc, 0x00201fff, CARD_WORD_CID_AND_BIT21_MASK, equip_scan_cid_bit21_mask_9eccc)` - NEW constants/duel_field.inc
- `(0x0809ecd0, 0x00001459, MARIE_THE_FALLEN_ONE_CID, equip_scan_cid_9ecd0)` - REUSE constants/card_info.inc:1285
- `(0x0809ecd4, 0x044e0000, EQUIP_ACTIVATION_CARD_ARRAY_ATTR_PREFIX, equip_scan_array_attr_prefix_9ecd4)` - NEW constants/duel_field.inc
- `(0x0809ecdc, 0x00001d24, EQUIP_ACTIVATION_SCAN_CURSOR_OFF, equip_scan_cursor_offset_9ecdc)` - REUSE constants/duel_field.inc:605
- `(0x0809ecfc, 0x00001628, SENRI_EYE_CID, equip_scan_cid_9ecfc)` - REUSE constants/card_info.inc:1752
- `(0x0809ed0c, 0x00001757, WHITE_MAGICIAN_PIKERU_CID, equip_scan_cid_9ed0c)` - REUSE constants/card_info.inc:874
- `(0x0809ed1c, 0x0000191d, EBON_MAGICIAN_CURRAN_CID, equip_scan_cid_9ed1c)` - REUSE constants/card_info.inc:881
- `(0x0809ed2c, 0x000019cd, PRINCESS_PIKERU_CID, equip_scan_cid_9ed2c)` - REUSE constants/card_info.inc:772
- `(0x0809ed3c, 0x000019ce, PRINCESS_CURRAN_CID, equip_scan_cid_9ed3c)` - REUSE constants/card_info.inc:773
- `(0x0809ed4c, 0x00001637, BOWGANIAN_CID, equip_scan_cid_9ed4c)` - NEW constants/card_info.inc
- `(0x0809edec, 0x00001d24, EQUIP_ACTIVATION_SCAN_CURSOR_OFF, equip_scan_cursor_offset_9edec)` - REUSE constants/duel_field.inc:605
- `(0x0809edf0, 0x00000868, PLAYER_BLOCK_STRIDE, equip_scan_player_stride_9edf0)` - REUSE constants/ewram.inc:251
- `(0x0809edf4, 0x00001690, INFERNALQUEEN_ARCHFIEND_CID, equip_scan_cid_9edf4)` - REUSE constants/card_info.inc:905
- `(0x0809eeac, 0x00001d24, EQUIP_ACTIVATION_SCAN_CURSOR_OFF, equip_scan_cursor_offset_9eeac)` - REUSE constants/duel_field.inc:605
- `(0x0809eeb0, 0x00001491, GRAVEROBBERS_RETRIBUTION_CID, equip_scan_cid_9eeb0)` - NEW constants/card_info.inc
- `(0x0809eeb4, 0x00000868, PLAYER_BLOCK_STRIDE, equip_scan_player_stride_9eeb4)` - REUSE constants/ewram.inc:251
- `(0x0809ef64, 0x00001d24, EQUIP_ACTIVATION_SCAN_CURSOR_OFF, equip_scan_cursor_offset_9ef64)` - REUSE constants/duel_field.inc:605
- `(0x0809ef68, 0x00001406, BURNING_LAND_CID, equip_scan_cid_9ef68)` - NEW constants/card_info.inc
- `(0x0809ef6c, 0x00000868, PLAYER_BLOCK_STRIDE, equip_scan_player_stride_9ef6c)` - REUSE constants/ewram.inc:251
- `(0x0809ef94, 0x000013f0, MASK_OF_DISPEL_CID, equip_scan_cid_9ef94)` - REUSE constants/card_info.inc:1581
- `(0x0809efa4, 0x000013f3, MASK_OF_THE_ACCURSED_CID, equip_scan_cid_9efa4)` - NEW constants/card_info.inc
- `(0x0809efb4, 0x000014b2, NIGHTMARE_WHEEL_CID, equip_scan_cid_9efb4)` - REUSE constants/card_info.inc:1287
- `(0x0809efcc, 0x00001322, SNATCH_STEAL_CID, equip_scan_cid_9efcc)` - REUSE constants/card_info.inc:218
- `(0x0809efe4, 0x00001877, BRAIN_JACKER_CID, equip_scan_cid_9efe4)` - REUSE constants/card_info.inc:223
- `(0x0809effc, 0x0000169a, FALLING_DOWN_CID, equip_scan_cid_9effc)` - REUSE constants/card_info.inc:225
- `(0x0809f014, 0x0000137b, EYE_OF_TRUTH_CID, equip_scan_cid_9f014)` - REUSE constants/card_info.inc:274
- `(0x0809f02c, 0x00001355, MINOR_GOBLIN_OFFICIAL_CID, equip_scan_cid_9f02c)` - REUSE constants/card_info.inc:1162
- `(0x0809f044, 0x00001286, BLAST_SPHERE_CID, equip_scan_cid_9f044)` - REUSE constants/card_info.inc:1360
- `(0x0809f05c, 0x000019bd, ADHESIVE_EXPLOSIVE_CID, equip_scan_cid_9f05c)` - REUSE constants/card_info.inc:884
- `(0x0809f074, 0x000019d0, MALICE_ASCENDANT_CID, equip_scan_cid_9f074)` - REUSE constants/card_info.inc:1347
- `(0x0809f12c, 0x00001d24, EQUIP_ACTIVATION_SCAN_CURSOR_OFF, equip_scan_cursor_offset_9f12c)` - REUSE constants/duel_field.inc:605
- `(0x0809f130, 0x00001370, KISEITAI_CID, equip_scan_cid_9f130)` - NEW constants/card_info.inc
- `(0x0809f134, 0x0000ffff, EQUIP_CHAIN_PAIR_MISSING, equip_scan_chain_pair_missing_f134)` - NEW constants/duel_field.inc
- `(0x0809f138, 0x00000868, PLAYER_BLOCK_STRIDE, equip_scan_player_stride_9f138)` - REUSE constants/ewram.inc:251
- `(0x0809f1d0, 0x00000868, PLAYER_BLOCK_STRIDE, equip_scan_player_stride_9f1d0)` - REUSE constants/ewram.inc:251
- `(0x0809f1d8, 0x044e0000, EQUIP_ACTIVATION_CARD_ARRAY_ATTR_PREFIX, equip_scan_array_attr_prefix_9f1d8)` - NEW constants/duel_field.inc
- `(0x0809f1f8, 0x00000868, PLAYER_BLOCK_STRIDE, equip_scan_player_stride_9f1f8)` - REUSE constants/ewram.inc:251
- `(0x0809f208, 0x00001181, SINISTER_SERPENT_CID, equip_scan_cid_9f208)` - NEW constants/card_info.inc
- `(0x0809f218, 0x000019cb, TREEBORN_FROG_CID, equip_scan_cid_9f218)` - REUSE constants/card_info.inc:377
- `(0x0809f2fc, 0x00000868, PLAYER_BLOCK_STRIDE, equip_scan_player_stride_9f2fc)` - REUSE constants/ewram.inc:251
- `(0x0809f304, 0x00201fff, CARD_WORD_CID_AND_BIT21_MASK, equip_scan_cid_bit21_mask_9f304)` - NEW constants/duel_field.inc
- `(0x0809f308, 0x00001775, RETURN_ZOMBIE_CID, equip_scan_cid_9f308)` - REUSE constants/card_info.inc:1038
- `(0x0809f30c, 0xfffff03f, ACTIVATION_ENTRY_CLR_BITS_11_6, equip_scan_clear_bits_11_6_9f30c)` - REUSE constants/duel_field.inc:551
- `(0x0809f310, 0xffff803f, ACTIVATION_ENTRY_CLR_BITS_14_6, equip_scan_clear_bits_14_6_9f310)` - REUSE constants/duel_field.inc:552
- `(0x0809f314, 0x044e0000, EQUIP_ACTIVATION_CARD_ARRAY_ATTR_PREFIX, equip_scan_array_attr_prefix_9f314)` - NEW constants/duel_field.inc
- `(0x0809f344, 0x00000868, PLAYER_BLOCK_STRIDE, equip_scan_player_stride_9f344)` - REUSE constants/ewram.inc:251
- `(0x0809f3dc, 0x00001d24, EQUIP_ACTIVATION_SCAN_CURSOR_OFF, equip_scan_cursor_offset_9f3dc)` - REUSE constants/duel_field.inc:605
- `(0x0809f3e0, 0x00000868, PLAYER_BLOCK_STRIDE, equip_scan_player_stride_9f3e0)` - REUSE constants/ewram.inc:251
- `(0x0809f3e8, 0x000013b2, MUCUS_YOLK_CID, equip_scan_cid_9f3e8)` - REUSE constants/card_info.inc:506
- `(0x0809f418, 0x0000154d, LEGENDARY_FIEND_CID, equip_scan_cid_9f418)` - REUSE constants/card_info.inc:1412
- `(0x0809f428, 0x00001645, EXODIA_NECROSS_CID, equip_scan_cid_9f428)` - REUSE constants/card_info.inc:245
- `(0x0809f438, 0x0000160e, AMAZONESS_BLOWPIPER_CID, equip_scan_cid_9f438)` - NEW constants/card_info.inc
- `(0x0809f498, 0x00001d24, EQUIP_ACTIVATION_SCAN_CURSOR_OFF, equip_scan_cursor_offset_9f498)` - REUSE constants/duel_field.inc:605
- `(0x0809f49c, 0x00000868, PLAYER_BLOCK_STRIDE, equip_scan_player_stride_9f49c)` - REUSE constants/ewram.inc:251
- `(0x0809f4a0, 0x00001812, SILENT_SWORDSMAN_LV3_CID, equip_scan_cid_9f4a0)` - REUSE constants/card_info.inc:682
- `(0x0809f4a8, 0x000017d9, ARMED_DRAGON_LV3_CID, equip_scan_cid_9f4a8)` - NEW constants/card_info.inc
- `(0x0809f4c0, 0x00001817, SILENT_MAGICIAN_LV4_CID, equip_scan_cid_9f4c0)` - REUSE constants/card_info.inc:354
- `(0x0809f518, 0x00001822, ULTIMATE_INSECT_LV3_CID, equip_scan_cid_9f518)` - REUSE constants/card_info.inc:355
- `(0x0809f520, 0x00001cf4, FIELD_STATE_OFF, equip_scan_cursor_from_field_offset_f520)` - REUSE constants/duel_field.inc:207
- `(0x0809f57c, 0x0000ffff, EQUIP_ACTIVATION_CID_U16_MASK, equip_scan_cid_mask_9f57c)` - REUSE constants/duel_field.inc:606
- `(0x0809f580, 0x044e0000, EQUIP_ACTIVATION_CARD_ARRAY_ATTR_PREFIX, equip_scan_array_attr_prefix_9f580)` - NEW constants/duel_field.inc
- `(0x0809f590, 0x000013c7, REVIVAL_JAM_CID, equip_scan_cid_9f590)` - REUSE constants/card_info.inc:1174
- `(0x0809f5a0, 0x00001522, VAMPIRE_LORD_CID, equip_scan_cid_9f5a0)` - REUSE constants/card_info.inc:557
- `(0x0809f5b0, 0x0000185c, SACRED_PHOENIX_CID, equip_scan_cid_9f5b0)` - REUSE constants/card_info.inc:539
- `(0x0809f5c0, 0x0000188f, CURSE_OF_VAMPIRE_CID, equip_scan_cid_9f5c0)` - NEW constants/card_info.inc
- `(0x0809f5d8, 0x0000188f, CURSE_OF_VAMPIRE_CID, equip_scan_cid_9f5d8)` - NEW constants/card_info.inc
- `(0x0809f680, 0x00001d24, EQUIP_ACTIVATION_SCAN_CURSOR_OFF, equip_scan_cursor_offset_9f680)` - REUSE constants/duel_field.inc:605
- `(0x0809f684, 0x0000ffff, EQUIP_ACTIVATION_CID_U16_MASK, equip_scan_cid_mask_9f684)` - REUSE constants/duel_field.inc:606
- `(0x0809f688, 0x00000868, PLAYER_BLOCK_STRIDE, equip_scan_player_stride_9f688)` - REUSE constants/ewram.inc:251
- `(0x0809f6dc, 0x00001da8, LP_CARD_TRACK_BASE_OFF, equip_scan_lp_track_offset_9f6dc)` - REUSE constants/ewram.inc:247
- `(0x0809f6e0, 0x00000868, PLAYER_BLOCK_STRIDE, equip_scan_player_stride_9f6e0)` - REUSE constants/ewram.inc:251
- `(0x0809f718, 0x00001367, EQUIP_ACTIVATION_UNMAPPED_CID_1367, equip_scan_cid_9f718)` - NEW constants/card_info.inc
- `(0x0809f728, 0x000016d5, RECYCLE_CID, equip_scan_cid_9f728)` - REUSE constants/card_info.inc:1293
- `(0x0809f740, 0x00001485, AQUA_SPIRIT_CID, equip_scan_cid_9f740)` - REUSE constants/card_info.inc:1414

### REF_SLOTS

- `(0x0809e728, 0x0809e72c, equip_activation_subphase_targets, equip_scan_subphase_table_9e728)`
- `(0x0809e72c, 0x0809e74c, equip_activation_subphase_case0, equip_activation_subphase_targets)`
- `(0x0809e730, 0x0809e76c, equip_activation_subphase_case1, equip_activation_subphase_case1_ptr)`
- `(0x0809e734, 0x0809e7c4, equip_activation_subphase_case2, equip_activation_subphase_case2_ptr)`
- `(0x0809e738, 0x0809e7d8, equip_activation_subphase_case3, equip_activation_subphase_case3_ptr)`
- `(0x0809e73c, 0x0809e800, equip_activation_subphase_case4, equip_activation_subphase_case4_ptr)`
- `(0x0809e740, 0x0809e850, equip_activation_subphase_case5, equip_activation_subphase_case5_ptr)`
- `(0x0809e744, 0x0809e894, equip_activation_subphase_case6, equip_activation_subphase_case6_ptr)`
- `(0x0809e748, 0x0809e8b0, equip_activation_subphase_case7, equip_activation_subphase_case7_ptr)`
- `(0x0809e7a8, 0x0201c4e0, gP1LifePoints, equip_scan_lp_base_9e7a8)`
- `(0x0809e7bc, 0x0201c4e0, gP1LifePoints, equip_scan_lp_base_9e7bc)`
- `(0x0809e7f8, 0x0201c4e0, gP1LifePoints, equip_scan_lp_base_9e7f8)`
- `(0x0809e848, 0x0201c4e0, gP1LifePoints, equip_scan_lp_base_9e848)`
- `(0x0809e8a8, 0x0201c4e0, gP1LifePoints, equip_scan_lp_base_9e8a8)`
- `(0x0809e8e8, 0x0201c4e0, gP1LifePoints, equip_scan_lp_base_9e8e8)`
- `(0x0809eeb8, 0x0201c510, gDuelFieldSlots, equip_scan_field_base_9eeb8)`
- `(0x0809f1d4, 0x0201c8f8, gP1HandSlotArray, equip_scan_card_array_base_9f1d4)`
- `(0x0809f300, 0x0201c8f8, gP1HandSlotArray, equip_scan_card_array_base_9f300)`
- `(0x0809f3e4, 0x0201c510, gDuelFieldSlots, equip_scan_field_base_9f3e4)`
- `(0x0809f51c, 0x0201c510, gDuelFieldSlots, equip_scan_field_base_9f51c)`

### RENAME_SLOTS

- `(0x0809e71c, equip_scan_lp_base_9e71c, "Base/target gP1LifePoints; preserve the stored address and all unrelated references.")`
- `(0x0809e918, equip_scan_lp_base_9e918, "Base/target gP1LifePoints; preserve the stored address and all unrelated references.")`
- `(0x0809e9b0, equip_scan_lp_base_9e9b0, "Base/target gP1LifePoints; preserve the stored address and all unrelated references.")`
- `(0x0809e9dc, equip_scan_lp_base_9e9dc, "Base/target gP1LifePoints; preserve the stored address and all unrelated references.")`
- `(0x0809ea70, equip_scan_lp_base_9ea70, "Base/target gP1LifePoints; preserve the stored address and all unrelated references.")`
- `(0x0809ea9c, equip_scan_lp_base_9ea9c, "Base/target gP1LifePoints; preserve the stored address and all unrelated references.")`
- `(0x0809ebdc, equip_scan_lp_base_9ebdc, "Base/target gP1LifePoints; preserve the stored address and all unrelated references.")`
- `(0x0809ec4c, equip_scan_lp_base_9ec4c, "Base/target gP1LifePoints; preserve the stored address and all unrelated references.")`
- `(0x0809ecd8, equip_scan_lp_base_9ecd8, "Base/target gP1LifePoints; preserve the stored address and all unrelated references.")`
- `(0x0809ede8, equip_scan_lp_base_9ede8, "Base/target gP1LifePoints; preserve the stored address and all unrelated references.")`
- `(0x0809eea8, equip_scan_lp_base_9eea8, "Base/target gP1LifePoints; preserve the stored address and all unrelated references.")`
- `(0x0809ef60, equip_scan_lp_base_9ef60, "Base/target gP1LifePoints; preserve the stored address and all unrelated references.")`
- `(0x0809f128, equip_scan_lp_base_9f128, "Base/target gP1LifePoints; preserve the stored address and all unrelated references.")`
- `(0x0809f1cc, equip_scan_lp_base_9f1cc, "Base/target gP1LifePoints; preserve the stored address and all unrelated references.")`
- `(0x0809f2f8, equip_scan_lp_base_9f2f8, "Base/target gP1LifePoints; preserve the stored address and all unrelated references.")`
- `(0x0809f340, equip_scan_lp_base_9f340, "Base/target gP1LifePoints; preserve the stored address and all unrelated references.")`
- `(0x0809f3d8, equip_scan_lp_base_9f3d8, "Base/target gP1LifePoints; preserve the stored address and all unrelated references.")`
- `(0x0809f494, equip_scan_lp_base_9f494, "Base/target gP1LifePoints; preserve the stored address and all unrelated references.")`
- `(0x0809f67c, equip_scan_lp_base_9f67c, "Base/target gP1LifePoints; preserve the stored address and all unrelated references.")`

### C7 导出与引用契约

1. `tools/asm-regen/ghidra/ExportRangeToGas.py:508-562` 只有目标 primary USER_DEFINED LABEL 可经 REF 输出. 本段 20 REF 的目标均为 RAM LABEL 或 even case/table LABEL, 不使用 ROM FUNCTION 伪装数据标签, 不承诺 fn+1. MOV pc,r0 不切换 Thumb 状态, 8 表项保持原偶数地址.
2. e728 既有 operand0 DATA/DEFAULT -> e72c; 8 个表 word 既有 operand0 DATA/DEFAULT -> case. 目标都为 DEFAULT 动态标签, 不属于 Seg1 scoped ANALYSIS 对象. 新建各地址唯一 USER_DEFINED primary LABEL, 不叠加别名; 动态默认名随 static primary 消失. 不要求保留动态 symbol id. 原先 7 个无标签表 word 只新增自己的具名池标签.
3. 9 条表引用采用 operand0 DATA/USER_DEFINED primary. 此 Ghidra 版本 addMemoryReference 不会提升已合并 DEFAULT 的 source; 精确删除并重建相同 operand0+target 的原 DEFAULT 引用, 其他 operand/target/source 保留. 不改 table word DataType / length / 原值. 新 6 个 LP 指针池与原 5 个无引用 RAM 指针槽各新增 operand0 DATA/USER_DEFINED primary.
4. 19 RENAME 中 e71c 原引用是 DATA/USER_DEFINED; 其他 18 个原 LP PTR 是 DATA/DEFAULT. 全部保留原 source/operand/primary, 不重建. 不能由目标 gP1LifePoints 的 USER source 推断引用 source.
5. RAM 只复用现有 USER 主 LABEL: gP1LifePoints id15545, gDuelFieldSlots id20369, gP1HandSlotArray id21609. 保留原 Data4 和全部既有 incoming/outgoing, 不读 RAM 值, 不重定义 RAM. 原 metadata 在 root slots/targets snapshots 中.
6. 新 25 池统一建立 /dword length4. 原前态每个字节均无 DefinedData/Instruction, 不是已有 Data4. 新 literal LDR 由解码产生 operand1 READ/DEFAULT primary 到池;每个 uses 的期望引用已逐项列 plan. 原已定义槽和既有指令 READ refs 保留. EQ 只设 data equate 与新槽名, 无需伪 DATA ref.

## FUNC_RENAME (R6)

| 地址 / ID | 旧名 | 新名 | 调用证据 |
| --- | --- | --- | --- |
| 0x0809ec34 / 6829 | scan_monster_slots_for_equip_activation_marie_the_fallen_one | scan_player_card_array_for_equip_activation_marie_the_fallen_one | Ghidra indeg=0; ROM even=0, odd=1 |
| 0x0809f158 / 6849 | scan_monster_zone_chain_for_equip_activation | scan_player_card_array_for_equip_activation_by_cid | Ghidra indeg=2; ROM even=0, odd=0 |
| 0x0809f1fc / 6864 | scan_monster_zone_chain_for_equip_activation_sinister_serpent | scan_player_card_array_for_equip_activation_sinister_serpent | Ghidra indeg=0; ROM even=0, odd=1 at 0x09e4788c |
| 0x0809f20c / 6865 | scan_monster_zone_chain_for_equip_activation_treeborn_frog | scan_player_card_array_for_equip_activation_treeborn_frog | Ghidra indeg=0; ROM even=0, odd=1 at 0x09e47890 |

ec34/f158 两个扫描核心均用 LP+0x14 的 count 和 gP1HandSlotArray+(player&1)*0x868+index*4, 检查 CID 与 bit21; 未扫描 20B monster slot. f1fc/f20c 两个12B wrapper分别加载固定CID 0x1181/0x19cb并以普通BL调用f158, 因而正式名同步为player card-array语义. 0x0809ec34 证据 asm13:2601-2689, 0x0809f158 证据 :3312-3394, wrapper证据 :3399-3418. 保留历史 RAM 全局名, plate 以 4-byte card-word array 描述, 不扩展全局重命名. confidence=high.
四个改名Function均保留原ID/body字节/prototype/incoming/EOL/PLATE前态; 只改Function主名和本批审定PLATE. ec34 odd指针0x09e477c0=0x0809ec35保持/undefined * length4及唯一operand0 DATA/DEFAULT primary ref本体, 不重建引用; 仅target_primary展示名随ec34改名派生变化. f1fc/f20c odd指针0x09e4788c=0x0809f1fd、0x09e47890=0x0809f20d当前均为undefined1容器, getDefinedDataAt=None, 无symbol及from/to ref; 后态仍不得建立Data/ref/symbol. 三个raw word均even命中0/odd命中1, 不改值、不carve、不改host切割. f158的两条CALL@0x0809f200/@0x0809f210及BL机器码保持.

- `asm/13_equip_placement.s`: Rename four Function definitions and the two true BL operands that name f158; replace all 59 reviewed full PLATE texts. The two wrapper definitions gain the new names without changing either BL instruction.
- `asm/rom.s`: No change. Preserve raw words 09e477c0=0809ec35, 09e4788c=0809f1fd, and 09e47890=0809f20d inside the same incbin. Do not carve or change host boundaries.
- `doc/dev/naming-proposals.csv`: Change exactly four `name` cells at addresses 0809ec34, 0809f158, 0809f1fc, and 0809f20c; preserve proposed_name/score/tags and every other cell.
- `tools/ghidra-labeling/RenameKnownFunctions.py`: Change exactly the four address-matched tuples to name+plate updates for ec34/f158/f1fc/f20c; preserve every other tuple. Do not run a historical full-registry rewrite.
- `inventory`: After saved Ghidra rename, run the real ExportFunctionInventory flow for temp/ghidra-functions.csv, temp/ghidra-functions-renamed.txt, temp/ghidra-functions-auto.txt, and temp/ghidra-functions-summary.md. Exactly four names change; dispatcher length/body metadata changes from 54 to 370 where represented; total 5209, named 5119, auto 90 and auto/summary statistics otherwise remain unchanged.
- `history`: Do not edit historical proposals/reviews/scripts, or globally replace old strings.

正式旧名命中清单 (注释命中仅在本批全文 PLATE 或 registry 四 tuple 内处理; 历史不盲替):
| 旧入口 | 文件:行 | 原内容 |
| --- | --- | --- |
| 0x0809ec34 | asm/13_equip_placement.s:2601 | scan_monster_slots_for_equip_activation_marie_the_fallen_one: |
| 0x0809ec34 | doc/dev/naming-proposals.csv:3133 | 0x0809ec34,scan_monster_slots_for_equip_activation_marie_the_fallen_one,,,duel_field |
| 0x0809ec34 | tools/ghidra-labeling/RenameKnownFunctions.py:10905 |     ("FUN_0809ec34", "scan_monster_slots_for_equip_activation_marie_the_fallen_one", |
| 0x0809ec34 | temp/ghidra-functions.csv:3264 | 0x0809ec34,scan_monster_slots_for_equip_activation_marie_the_fallen_one,USER_DEFINED,0,0,140,Global |
| 0x0809f158 | asm/13_equip_placement.s:3312 | scan_monster_zone_chain_for_equip_activation: |
| 0x0809f158 | asm/13_equip_placement.s:3398 | @ 由 duel_field 主调度枢纽 run_equip_activation_phase_by_counter 及辅助扫描调用. 4 条指令 thin wrapper: r0=player_id 透传, r1=DAT_0809f208=0x1181 (Sinister Serpent card_id), tail-call scan_monster_zone_chain_for_equip_activation. 与 scan_monster_zone_chain_for_equip_activation_treeborn_frog (0x0809f20c, card_id=0x19cb) 构成同族 sibling 对. Side effects: via callee on hit. Constants: CARD_ID=0x1181 (Sinister Serpent). |
| 0x0809f158 | asm/13_equip_placement.s:3402 |     bl scan_monster_zone_chain_for_equip_activation @ 0809f200 fff7aaff |
| 0x0809f158 | asm/13_equip_placement.s:3408 | @ Called by FUN_0809d984 and FUN_0809fb16 (each once). 4-instruction thin wrapper stub: r0=player_id [0..1] (pass-through); fixed r1=0x19cb. Calls scan_monster_zone_chain_for_equip_activation (FUN_0809f158). Returns r0=u32 pass-through. Sibling with FUN_0809f1fc (card_id=0x1181). Constants: CARD_ID=0x19cb. |
| 0x0809f158 | asm/13_equip_placement.s:3412 |     bl scan_monster_zone_chain_for_equip_activation @ 0809f210 fff7a2ff |
| 0x0809f158 | doc/dev/naming-proposals.csv:3156 | 0x0809f158,scan_monster_zone_chain_for_equip_activation,,,duel_field |
| 0x0809f158 | tools/ghidra-labeling/RenameKnownFunctions.py:10759 |     ("FUN_0809f158", "scan_monster_zone_chain_for_equip_activation", |
| 0x0809f158 | tools/ghidra-labeling/RenameKnownFunctions.py:10778 |         "Calls scan_monster_zone_chain_for_equip_activation (FUN_0809f158). " |
| 0x0809f158 | tools/ghidra-labeling/RenameKnownFunctions.py:11898 |         "tail-call scan_monster_zone_chain_for_equip_activation. " |
| 0x0809f158 | temp/ghidra-functions.csv:3287 | 0x0809f158,scan_monster_zone_chain_for_equip_activation,USER_DEFINED,0,0,142,Global |
| 0x0809f1fc | asm/13_equip_placement.s:3399 | scan_monster_zone_chain_for_equip_activation_sinister_serpent: |
| 0x0809f1fc | doc/dev/naming-proposals.csv:3157 | 0x0809f1fc,scan_monster_zone_chain_for_equip_activation_sinister_serpent,,,duel_field |
| 0x0809f1fc | tools/ghidra-labeling/RenameKnownFunctions.py:11894 | name+plate tuple currently uses scan_monster_zone_chain_for_equip_activation_sinister_serpent |
| 0x0809f1fc | temp/ghidra-functions.csv:3288 | 0x0809f1fc,scan_monster_zone_chain_for_equip_activation_sinister_serpent,USER_DEFINED,0,0,12,Global |
| 0x0809f20c | asm/13_equip_placement.s:3398,3409 | old sibling text and definition use scan_monster_zone_chain_for_equip_activation_treeborn_frog |
| 0x0809f20c | doc/dev/naming-proposals.csv:3158 | 0x0809f20c,scan_monster_zone_chain_for_equip_activation_treeborn_frog,,,duel_field |
| 0x0809f20c | tools/ghidra-labeling/RenameKnownFunctions.py:10774,11899 | tuple name and old sibling text use scan_monster_zone_chain_for_equip_activation_treeborn_frog |
| 0x0809f20c | temp/ghidra-functions.csv:3289 | 0x0809f20c,scan_monster_zone_chain_for_equip_activation_treeborn_frog,USER_DEFINED,0,0,12,Global |

temp 另三个 inventory 是真实ExportFunctionInventory重导的派生产物, 不手工改表. registry四个地址tuple均只改name+审定plate, 总计4 name cells和4 plate cells; CSV按address只改4个name cells. 正式生产输出中四个旧Function名命中必须为0; 冻结round1、review证据、expected_old_*守卫和历史文档不属于生产输出, 不做盲目全库替换. asm/rom.s不变.

## disasm 计划 (R4)

严格逐 case 解码, 不对整个 424B 盲目 linear sweep. `plan.disasm.instructions` 逐条列出 145 个指令地址、长度、原机器码、mnemonic 和 operands; `f13-seg2-static-projection.s` 给可读符号投影. 8 case 共用 dispatcher r4=player/r2=LP 与同一个保存 r8 的栈帧. 0x0809e6f6 的 0x4647 是 mov r7,r8, 0x0809e71a 的 0x4687 是 mov pc,r0, 修正旧 plate 的两处寄存器事实.
保持 Function 0x0809e6f4 id16934 身份, 仅把原 body54B 扩为下表 370B 的精确 union, 不建立 case Function. 原 range [e6f4,e71c) 和 [e8f4,e902) 完整保留; 原 27 条指令字节/长度/flow/既有引用不变. MOV pc@e71a原flows/outrefs均为空, 保持原样, 不新增computed跳转引用. 其余 58 Function body 不变. Function总数仍5209. 所有 pool/padding 排除出 body.

| 新 body 半开 range | 大小 |
| --- | --- |
| 0x0809e6f4..0x0809e71c | 40 B |
| 0x0809e74c..0x0809e75e | 18 B |
| 0x0809e76c..0x0809e79e | 50 B |
| 0x0809e7b0..0x0809e7bc | 12 B |
| 0x0809e7c4..0x0809e7d2 | 14 B |
| 0x0809e7d8..0x0809e7f4 | 28 B |
| 0x0809e800..0x0809e848 | 72 B |
| 0x0809e850..0x0809e86c | 28 B |
| 0x0809e874..0x0809e888 | 20 B |
| 0x0809e894..0x0809e8a6 | 18 B |
| 0x0809e8b0..0x0809e8e8 | 56 B |
| 0x0809e8f4..0x0809e902 | 14 B |

现有导出 25 个代码模块的真实指令机器码扫描, 指向裸块的直接 branch/call=0, literal LDR=0; 内部入口由 switch 的 8 条 DATA 引用闭合. 表前/块后的相邻单元是数据 word, 不是代码 fallthrough. 新内部所有条件/无条件 branch 目标均是本次指令起点或原共享尾 e8f4/e8f6; 无跳入池/对齐/BL后半字. `f13-seg2-control-evidence.json` 保留扫描和逐 branch 清单.

| case入口 | USER主LABEL | ASCII EOL |
| --- | --- | --- |
| 0x0809e74c | equip_activation_subphase_case0 | Case 0: copy LP+0x1cf4 to LP+0x1cf8, increment subphase, return 0. |
| 0x0809e76c | equip_activation_subphase_case1 | Case 1: require available slot, group placement and Last Turn effect gates; failure sets subphase 8, success emits op31 and advances. |
| 0x0809e7c4 | equip_activation_subphase_case2 | Case 2: initialize player display context with zone 6, Last Turn CID and zero flags, then advance. |
| 0x0809e7d8 | equip_activation_subphase_case3 | Case 3: submit monster-entry pointer with flags 1, mode 0 and stack extra Last Turn CID in high16, then advance. |
| 0x0809e800 | equip_activation_subphase_case4 | Case 4: require own entity-1 and opponent entity-0 slots plus both activation checks; reject with 1 or advance with 0. |
| 0x0809e850 | equip_activation_subphase_case5 | Case 5: write chain step 1 iff saved phase equals 3, else 0; clear chain active word and advance. |
| 0x0809e894 | equip_activation_subphase_case6 | Case 6: wait until display advance returns nonzero; then increment subphase. Return 0 in both paths. |
| 0x0809e8b0 | equip_activation_subphase_case7 | Case 7: unless saved phase is 3, enqueue type saved_phase+12 with player side bit; increment subphase and return 0. |

新普通内部 branch label 可由 disassembler 建立 ANALYSIS LAB; 不更改已有 e8f4/e8f6 label. 每条新增 CALL 在下表按 source 单列, 13 条 CALL 恰为 13 个去重 callee, 不把去重数当调用数. 各 callee 原 Function name/ID/body/plate/prototype 和原 incoming 完整保留, 仅新增对应 DEFAULT UNCONDITIONAL_CALL operand0 primary incoming. 普通 BL fallthrough 也必须保持真实下一条指令地址.

| BL源 | 机器码 | callee目标 | 当前callee名 |
| --- | --- | --- | --- |
| 0x0809e76e | 94f723ff | 0x080335b8 | count_available_monster_slots |
| 0x0809e778 | 9df700fa | 0x0803bb7c | check_field_spell_neo_daedalus_group_placeable |
| 0x0809e786 | eff793f9 | 0x0808dab0 | dispatch_effect_handler_by_card_id |
| 0x0809e792 | f4f7fdfd | 0x08093390 | trigger_card_display_op31_if_not_active |
| 0x0809e7cc | f5f7fafc | 0x080941c4 | init_effect_slot_display_context |
| 0x0809e7d8 | f5f780fd | 0x080942dc | get_monster_slot_entry_ptr |
| 0x0809e7e8 | 0df0bafa | 0x080abd60 | setup_equip_oam_entry_with_sprite_attr |
| 0x0809e802 | fff727ff | 0x0809e654 | find_equip_slot_idx_with_entity_id_one |
| 0x0809e810 | fff748ff | 0x0809e6a4 | find_equip_slot_idx_with_entity_id_zero |
| 0x0809e824 | 96f7c4f8 | 0x080349b0 | check_slot_card_activatable |
| 0x0809e838 | 96f73afd | 0x080352b0 | eval_slot_activation_eligibility_full |
| 0x0809e896 | fdf7ebfa | 0x0809be70 | advance_equip_display_phase_via_table |
| 0x0809e8d4 | 9df72afa | 0x0803bd2c | enqueue_sprite_attr_record |

新池 25 项已包括在 EQ/REF 的唯一158槽清单, 不重复增加动作. 具体地址: 0x0809e760, 0x0809e764, 0x0809e768, 0x0809e7a0, 0x0809e7a4, 0x0809e7a8, 0x0809e7ac, 0x0809e7bc, 0x0809e7c0, 0x0809e7d4, 0x0809e7f4, 0x0809e7f8, 0x0809e7fc, 0x0809e848, 0x0809e84c, 0x0809e86c, 0x0809e870, 0x0809e888, 0x0809e88c, 0x0809e890, 0x0809e8a8, 0x0809e8ac, 0x0809e8e8, 0x0809e8ec, 0x0809e8f0.
4个 padding 为 e75e/e79e/e7d2/e8a6 各2B原始0000. 每个保留两个独立 /undefined length1 DataDB, getDefinedDataAt=None, 无 Instruction/Function/新label/equate/ref. ExportRangeToGas.py:734-739 读取连续全零 undefined run 输出 `.zero 0x2`. 不建 undefined2/short Data, 不将它们纳入 body.

## carve 计划 (R7) 与 §5.1

carve=0. 既有 8-word switch 已在模块内按 .word 输出, 本次改目标 LABEL/引用/槽名并保留偶地址. 段外0x09e477c0/0x09e4788c/0x09e47890三个raw odd Function指针仅是rename依赖保值项, 不新增carve; 其中仅09e477c0有既有Data/ref, 后两项保持无DefinedData/ref/symbol. §5.1=0: 唯一裸块有 8 条真引用且全部代码/池/零对齐已闭合.

## 新增 constants 与复用 (C5)

当前全部 constants/*.inc 共5998条 equate, 每个表达式已计算为实际u32并建立按值索引, 22个文件SHA256保存于constant-values.json. 以下24个NEW均先查全库同值, 包含2项NEW同值分域, 另对既有0x1cf4作双基址选择. 其余48个唯一值/名称复用现有文件, 每个EQ槽附来源行.

| NEW名称 | 值 | 文件 | ASCII定义注释 | 新增依据 |
| --- | --- | --- | --- | --- |
| SINISTER_SERPENT_CID | 0x00001181 | constants/card_info.inc | Internal CID for Sinister Serpent. | No current equate has this numeric value; exact CID/ROM/password proof in cid-proof JSON. |
| EQUIP_ACTIVATION_UNMAPPED_CID_1338 | 0x00001338 | constants/card_info.inc | Unmapped internal CID 0x1338; inverse table is 0xffff and all 5170 stat records exclude it. | No current equate has this numeric value; exact CID/ROM/password proof in cid-proof JSON. |
| EQUIP_ACTIVATION_UNMAPPED_CID_1367 | 0x00001367 | constants/card_info.inc | Unmapped internal CID 0x1367; inverse table is 0xffff and all 5170 stat records exclude it. | No current equate has this numeric value; exact CID/ROM/password proof in cid-proof JSON. |
| KISEITAI_CID | 0x00001370 | constants/card_info.inc | Internal CID for Kiseitai. | No current equate has this numeric value; exact CID/ROM/password proof in cid-proof JSON. |
| MASK_OF_THE_ACCURSED_CID | 0x000013f3 | constants/card_info.inc | Internal CID for Mask of the Accursed. | No current equate has this numeric value; exact CID/ROM/password proof in cid-proof JSON. |
| BURNING_LAND_CID | 0x00001406 | constants/card_info.inc | Internal CID for Burning Land. | No current equate has this numeric value; exact CID/ROM/password proof in cid-proof JSON. |
| DIMENSIONHOLE_CID | 0x0000140c | constants/card_info.inc | Internal CID for Dimensionhole. | No current equate has this numeric value; exact CID/ROM/password proof in cid-proof JSON. |
| SPIRIT_OF_THE_BREEZE_CID | 0x00001450 | constants/card_info.inc | Internal CID for Spirit of the Breeze. | No current equate has this numeric value; exact CID/ROM/password proof in cid-proof JSON. |
| DANCING_FAIRY_CID | 0x00001451 | constants/card_info.inc | Internal CID for Dancing Fairy. | No current equate has this numeric value; exact CID/ROM/password proof in cid-proof JSON. |
| CURE_MERMAID_CID | 0x00001454 | constants/card_info.inc | Internal CID for Cure Mermaid. | No current equate has this numeric value; exact CID/ROM/password proof in cid-proof JSON. |
| GRAVEROBBERS_RETRIBUTION_CID | 0x00001491 | constants/card_info.inc | Internal CID for Graverobber's Retribution. | No current equate has this numeric value; exact CID/ROM/password proof in cid-proof JSON. |
| BLIND_DESTRUCTION_CID | 0x00001494 | constants/card_info.inc | Internal CID for Blind Destruction. | No current equate has this numeric value; exact CID/ROM/password proof in cid-proof JSON. |
| NEEDLE_WALL_CID | 0x00001545 | constants/card_info.inc | Internal CID for Needle Wall. | No current equate has this numeric value; exact CID/ROM/password proof in cid-proof JSON. |
| AMAZONESS_BLOWPIPER_CID | 0x0000160e | constants/card_info.inc | Internal CID for Amazoness Blowpiper. | No current equate has this numeric value; exact CID/ROM/password proof in cid-proof JSON. |
| BOWGANIAN_CID | 0x00001637 | constants/card_info.inc | Internal CID for Bowganian. | No current equate has this numeric value; exact CID/ROM/password proof in cid-proof JSON. |
| ARMED_DRAGON_LV3_CID | 0x000017d9 | constants/card_info.inc | Internal CID for Armed Dragon LV3. | No current equate has this numeric value; exact CID/ROM/password proof in cid-proof JSON. |
| CURSE_OF_VAMPIRE_CID | 0x0000188f | constants/card_info.inc | Internal CID for Curse of Vampire. | No current equate has this numeric value; exact CID/ROM/password proof in cid-proof JSON. |
| EQUIP_ACTIVATION_SAVED_PHASE_OFF | 0x00001cf8 | constants/duel_field.inc | Byte offset from gP1LifePoints to saved activation phase; copied from LP+0x1cf4. | Existing EQUIP_CHAIN_STEP_FROM_FIELD_OFF uses gDuelFieldSlots base and denotes LP+0x1d28, not this LP+0x1cf8 field. |
| EQUIP_ACTIVATION_SUBPHASE_OFF | 0x00001d34 | constants/duel_field.inc | Byte offset from gP1LifePoints to the u32 activation subphase counter. | No equate has value 0x1d34; dispatcher and leaf checker both use LP base. |
| CARD_WORD_CID_AND_BIT21_MASK | 0x00201fff | constants/duel_field.inc | Keep card-word CID bits 0..12 and exclusion bit 21 for exact CID comparisons. | No equate has this value; exact equality rejects bit21-set entries. |
| EQUIP_ACTIVATION_CARD_ARRAY_ATTR_PREFIX | 0x044e0000 | constants/duel_field.inc | Packed activation prefix: bits 16..20=14 and bits 21..26=34; player and CID supplied separately. | No equate has this value; retained as bit-exact packed prefix without inventing field semantics. |
| DIMENSIONHOLE_PACKED_ACTIVATION_ATTR | 0x0450140c | constants/duel_field.inc | Packed activation word 0x0450140c: Dimensionhole CID 0x140c, upper half 0x0450; player bit supplied separately. | No equate has this packed value; low CID independently verified; upper bits stay literal-defined. |
| LAST_TURN_SETUP_EXTRA_WORD | 0x151e0000 | constants/duel_field.inc | Setup extra word: low16=0, high16=Last Turn CID; callee stores halves at context+4 and +6. | No equate has this value; caller stores stack arg and callee reads [sp+0x1c] at 080abdfc/080abe02. |
| EQUIP_CHAIN_PAIR_MISSING | 0x0000ffff | constants/duel_field.inc | Missing player/slot pair returned as 0xffff by find_equip_chain_pair_across_field. | Existing same-valued constants are card-empty, LP row mask, activation cap, LP init guard, sprite mask, CID mask, OAM attr, score cap; none denotes the packed pair sentinel. |

0x1cf8 本段基址LP, 与现有 EQUIP_CHAIN_STEP_FROM_FIELD_OFF 的field-base不同, 不能只按数值复用. 0x1cf4@e764 基址LP, 复用 P2LP_BLOCK2_OFF_1CF4; @f520 基址gDuelFieldSlots, 复用 FIELD_STATE_OFF, 两者相差0x30物理地址. 后者恰等价 LP+0x1d24 的共享cursor. 0xffff@f134 是链 pair 缺失哨兵, 不使用 CID mask 或 LP init guard;其余本段0xffff槽实际按位AND低16,复用EQUIP_ACTIVATION_CID_U16_MASK.

| REUSE名称 | 来源 | 原表达式 |
| --- | --- | --- |
| ACTIVATION_ENTRY_CLR_BITS_11_6 | constants/duel_field.inc:551 | 0xfffff03f |
| ACTIVATION_ENTRY_CLR_BITS_14_6 | constants/duel_field.inc:552 | 0xffff803f |
| ADHESIVE_EXPLOSIVE_CID | constants/card_info.inc:884 | 0x000019bd |
| AQUA_SPIRIT_CID | constants/card_info.inc:1414 | 0x00001485 |
| BLAST_SPHERE_CID | constants/card_info.inc:1360 | 0x00001286 |
| BRAIN_JACKER_CID | constants/card_info.inc:223 | 0x00001877 |
| CARD_DISPLAY_OP31_LP_BAR_SUB | constants/card_info.inc:1512 | 0x0000011d |
| DANGEROUS_MACHINE_TYPE6_CID | constants/card_info.inc:1522 | 0x00001738 |
| EBON_MAGICIAN_CURRAN_CID | constants/card_info.inc:881 | 0x0000191d |
| EQUIP_ACTIVATION_CID_U16_MASK | constants/duel_field.inc:606 | 0x0000ffff |
| EQUIP_ACTIVATION_SCAN_CURSOR_OFF | constants/duel_field.inc:605 | 0x00001d24 |
| EQUIP_CHAIN_ACTIVE_OFF | constants/duel_field.inc:230 | 0x00001d2c |
| EQUIP_CHAIN_STEP_OFF | constants/duel_field.inc:229 | 0x00001d28 |
| EXODIA_NECROSS_CID | constants/card_info.inc:245 | 0x00001645 |
| EYE_OF_TRUTH_CID | constants/card_info.inc:274 | 0x0000137b |
| FALLING_DOWN_CID | constants/card_info.inc:225 | 0x0000169a |
| FIELD_STATE_OFF | constants/duel_field.inc:207 | 0x00001cf4 |
| INFERNALQUEEN_ARCHFIEND_CID | constants/card_info.inc:905 | 0x00001690 |
| JAM_BREEDING_MACHINE_CID | constants/card_info.inc:405 | 0x000013ff |
| LAST_TURN_CID | constants/card_info.inc:1447 | 0x0000151e |
| LAVA_GOLEM_CID | constants/card_info.inc:403 | 0x00001578 |
| LEGENDARY_FIEND_CID | constants/card_info.inc:1412 | 0x0000154d |
| LP_CARD_TRACK_BASE_OFF | constants/ewram.inc:247 | 0x00001da8 |
| MALICE_ASCENDANT_CID | constants/card_info.inc:1347 | 0x000019d0 |
| MARIE_THE_FALLEN_ONE_CID | constants/card_info.inc:1285 | 0x00001459 |
| MASK_OF_DISPEL_CID | constants/card_info.inc:1581 | 0x000013f0 |
| MINOR_GOBLIN_OFFICIAL_CID | constants/card_info.inc:1162 | 0x00001355 |
| MUCUS_YOLK_CID | constants/card_info.inc:506 | 0x000013b2 |
| NIGHTMARE_WHEEL_CID | constants/card_info.inc:1287 | 0x000014b2 |
| OMINOUS_FORTUNETELLING_CID | constants/card_info.inc:1022 | 0x00001519 |
| P1LP_BLOCK2_OFF_1CE8 | constants/ewram.inc:276 | 0x1ce8 |
| P2LP_BLOCK2_OFF_1CF4 | constants/ewram.inc:277 | 0x1cf4 |
| PLAYER_BLOCK_STRIDE | constants/ewram.inc:251 | 0x868 |
| PRINCESS_CURRAN_CID | constants/card_info.inc:773 | 0x000019ce |
| PRINCESS_PIKERU_CID | constants/card_info.inc:772 | 0x000019cd |
| RECYCLE_CID | constants/card_info.inc:1293 | 0x000016d5 |
| RETURN_ZOMBIE_CID | constants/card_info.inc:1038 | 0x00001775 |
| REVIVAL_JAM_CID | constants/card_info.inc:1174 | 0x000013c7 |
| SACRED_PHOENIX_CID | constants/card_info.inc:539 | 0x0000185c |
| SENRI_EYE_CID | constants/card_info.inc:1752 | 0x00001628 |
| SILENT_MAGICIAN_LV4_CID | constants/card_info.inc:354 | 0x00001817 |
| SILENT_SWORDSMAN_LV3_CID | constants/card_info.inc:682 | 0x00001812 |
| SNATCH_STEAL_CID | constants/card_info.inc:218 | 0x00001322 |
| TREEBORN_FROG_CID | constants/card_info.inc:377 | 0x000019cb |
| ULTIMATE_INSECT_LV3_CID | constants/card_info.inc:355 | 0x00001822 |
| VAMPIRE_LORD_CID | constants/card_info.inc:557 | 0x00001522 |
| WHITE_MAGICIAN_PIKERU_CID | constants/card_info.inc:874 | 0x00001757 |
| get_card_lp_cost_by_id_cid_11cf | constants/card_info.inc:1061 | 0x000011cf |


## CID / packed值证据

59个唯一CID包含53个literal CID、2个wrapper移位立即数CID和4个LV差值CID. data.md只结构化读 Password/Card Name/SO/逻辑CID/小端CID 五列, SO==CID*4且小端列与原u16一致. 56个有映射CID全部与ROM card-ids逆映射、5170条主副card-stats记录、ROM passcode解密交叉一致. 3个缺项11cf/1338/1367在逆表为ffff且5170条record均无该CID;不赋卡名. 前者复用已存在中性常量, 后两者新建中性常量.

| 逻辑CID | data.md行 / 卡名 | 密码 | 逆表地址 -> index | 全部stats索引 / 行 |
| --- | --- | --- | --- | --- |
| 0x00001181 | 400 / Sinister Serpent | 08131171 | 0x095b8080 -> 0x00000190 | 400 / 5215, 2572 / 32481 |
| 0x000011cf | 缺项, 不命名卡片 | - | 0x095b811c -> 0x0000ffff | 无 |
| 0x00001286 | 589 / Blast Sphere | 26302522 | 0x095b828a -> 0x00000254 | 596 / 7763, 2833 / 35154 |
| 0x00001322 | 701 / Snatch Steal | 45986603 | 0x095b83c2 -> 0x000002ca | 714 / 9297, 2989 / 36742 |
| 0x00001338 | 缺项, 不命名卡片 | - | 0x095b83ee -> 0x0000ffff | 无 |
| 0x00001355 | 745 / Minor Goblin Official | 01918087 | 0x095b8428 -> 0x000002f6 | 758 / 9869, 3040 / 37335 |
| 0x00001367 | 缺项, 不命名卡片 | - | 0x095b844c -> 0x0000ffff | 无 |
| 0x00001370 | 767 / Kiseitai | 04266839 | 0x095b845e -> 0x0000030c | 780 / 10155, 3067 / 37636 |
| 0x0000137b | 778 / The Eye of Truth | 34694160 | 0x095b8474 -> 0x00000317 | 791 / 10298, 3078 / 37779 |
| 0x000013b2 | 818 / Mucus Yolk | 70307656 | 0x095b84e2 -> 0x00000340 | 832 / 10831, 3133 / 38344 |
| 0x000013c7 | 829 / Revival Jam | 31709826 | 0x095b850c -> 0x0000034b | 843 / 10974, 3154 / 38517 |
| 0x000013f0 | 848 / Mask of Dispel | 20765952 | 0x095b855e -> 0x0000035e | 862 / 11221, 3195 / 38830 |
| 0x000013f3 | 850 / Mask of the Accursed | 56948373 | 0x095b8564 -> 0x00000360 | 864 / 11247, 3198 / 38859 |
| 0x000013ff | 860 / Jam Breeding Machine | 21770260 | 0x095b857c -> 0x0000036a | 874 / 11377, 3210 / 39005 |
| 0x00001406 | 867 / Burning Land | 24294108 | 0x095b858a -> 0x00000371 | 881 / 11468, 3217 / 39096 |
| 0x0000140c | 873 / Dimensionhole | 22959079 | 0x095b8596 -> 0x00000377 | 887 / 11546, 3223 / 39174 |
| 0x00001450 | 903 / Spirit of the Breeze | 53530069 | 0x095b861e -> 0x00000395 | 917 / 11936, 3291 / 39688 |
| 0x00001451 | 904 / Dancing Fairy | 90925163 | 0x095b8620 -> 0x00000396 | 918 / 11949, 3292 / 39701 |
| 0x00001454 | 906 / Cure Mermaid | 85802526 | 0x095b8626 -> 0x00000398 | 920 / 11975, 3295 / 39730 |
| 0x00001459 | 911 / Marie the Fallen One | 57579381 | 0x095b8630 -> 0x0000039d | 925 / 12040, 3300 / 39795 |
| 0x00001485 | 949 / Aqua Spirit | 40916023 | 0x095b8688 -> 0x000003c3 | 963 / 12534, 3344 / 40307 |
| 0x00001491 | 961 / Graverobber's Retribution | 33737664 | 0x095b86a0 -> 0x000003cf | 975 / 12690, 3356 / 40463 |
| 0x00001494 | 964 / Blind Destruction | 32015116 | 0x095b86a6 -> 0x000003d2 | 978 / 12729, 3359 / 40502 |
| 0x000014b2 | 984 / Nightmare Wheel | 54704216 | 0x095b86e2 -> 0x000003e7 | 999 / 13002, 3389 / 40792 |
| 0x000014c0 | 996 / Life Absorbing Machine | 14318794 | 0x095b86fe -> 0x000003f3 | 1011 / 13158, 3403 / 40954 |
| 0x00001519 | 1074 / Ominous Fortunetelling | 56995655 | 0x095b87b0 -> 0x00000441 | 1089 / 14172, 3492 / 42031 |
| 0x0000151e | 1078 / Last Turn | 28566710 | 0x095b87ba -> 0x00000445 | 1093 / 14224, 3497 / 42086 |
| 0x00001522 | 1081 / Vampire Lord | 53839837 | 0x095b87c2 -> 0x00000448 | 1096 / 14263, 3501 / 42128 |
| 0x00001545 | 1114 / Needle Wall | 38299233 | 0x095b8808 -> 0x00000469 | 1129 / 14692, 3536 / 42563 |
| 0x0000154d | 1120 / Legendary Fiend | 99747800 | 0x095b8818 -> 0x00000470 | 1136 / 14783, 3544 / 42647 |
| 0x00001578 | 1136 / Lava Golem | 00102380 | 0x095b886e -> 0x00000480 | 1152 / 14991, 3587 / 42946 |
| 0x0000160e | 1247 / Amazoness Blowpiper | 73574678 | 0x095b899a -> 0x000004f3 | 1267 / 16486, 3737 / 44536 |
| 0x00001628 | 1271 / Senri Eye | 60391791 | 0x095b89ce -> 0x0000050b | 1291 / 16798, 3763 / 44854 |
| 0x00001637 | 1283 / Bowganian | 52090844 | 0x095b89ec -> 0x00000517 | 1303 / 16954, 3778 / 45019 |
| 0x00001645 | 1290 / Exodia Necross | 12600382 | 0x095b8a08 -> 0x0000051e | 1310 / 17045, 3792 / 45141 |
| 0x00001690 | 1352 / Infernalqueen Archfiend | 08581705 | 0x095b8a9e -> 0x0000055c | 1372 / 17851, 3867 / 45996 |
| 0x0000169a | 1362 / Falling Down | 32919136 | 0x095b8ab2 -> 0x00000566 | 1382 / 17981, 3877 / 46126 |
| 0x000016d5 | 1410 / Recycle | 96316857 | 0x095b8b28 -> 0x00000596 | 1430 / 18605, 3936 / 46783 |
| 0x00001738 | 1487 / Dangerous Machine TYPE-6 | 76895648 | 0x095b8bee -> 0x000005e3 | 1507 / 19606, 4035 / 47860 |
| 0x00001740 | 1495 / The Agent of Wisdom - Mercury | 38730226 | 0x095b8bfe -> 0x000005eb | 1515 / 19710, 4043 / 47964 |
| 0x00001757 | 1518 / White Magician Pikeru | 81383947 | 0x095b8c2c -> 0x00000602 | 1538 / 20009, 4066 / 48263 |
| 0x00001775 | 1540 / Return Zombie | 03072077 | 0x095b8c68 -> 0x00000618 | 1560 / 20295, 4096 / 48573 |
| 0x000017d1 | 1611 / Ultimate Insect LV1 | 49441499 | 0x095b8d20 -> 0x0000065f | 1631 / 21218, 4188 / 49559 |
| 0x000017d5 | 1615 / Dark Mimic LV1 | 74713516 | 0x095b8d28 -> 0x00000663 | 1635 / 21270, 4192 / 49611 |
| 0x000017d9 | 1619 / Armed Dragon LV3 | 00980973 | 0x095b8d30 -> 0x00000667 | 1639 / 21322, 4196 / 49663 |
| 0x00001812 | 1669 / Silent Swordsman LV3 | 01995985 | 0x095b8da2 -> 0x0000069a | 1690 / 21985, 4253 / 50344 |
| 0x00001814 | 1670 / Silent Swordsman LV5 | 74388798 | 0x095b8da6 -> 0x0000069b | 1691 / 21998, 4255 / 50370 |
| 0x00001817 | 1672 / Silent Magician LV4 | 73665146 | 0x095b8dac -> 0x0000069d | 1693 / 22024, 4258 / 50399 |
| 0x00001822 | 1682 / Ultimate Insect LV3 | 34088136 | 0x095b8dc2 -> 0x000006a7 | 1703 / 22154, 4269 / 50532 |
| 0x0000185c | 1736 / Sacred Phoenix of Nephthys | 61441708 | 0x095b8e36 -> 0x000006dd | 1757 / 22856, 4327 / 51246 |
| 0x0000185e | 1738 / Ultimate Insect LV5 | 34830502 | 0x095b8e3a -> 0x000006df | 1759 / 22882, 4329 / 51272 |
| 0x00001877 | 1763 / Brain Jacker | 40267580 | 0x095b8e6c -> 0x000006f8 | 1784 / 23207, 4354 / 51597 |
| 0x0000188f | 1785 / Curse of Vampire | 34294855 | 0x095b8e9c -> 0x0000070e | 1806 / 23493, 4378 / 51889 |
| 0x0000191d | 1892 / Ebon Magician Curran | 46128076 | 0x095b8fb8 -> 0x0000077a | 1914 / 24897, 4520 / 53385 |
| 0x000019bd | 2010 / Adhesive Explosive | 53828396 | 0x095b90f8 -> 0x000007f0 | 2032 / 26431, 4680 / 55065 |
| 0x000019cb | 2024 / Treeborn Frog | 12538374 | 0x095b9114 -> 0x000007fe | 2046 / 26613, 4694 / 55247 |
| 0x000019cd | 2026 / Princess Pikeru | 75917088 | 0x095b9118 -> 0x00000800 | 2048 / 26639, 4696 / 55273 |
| 0x000019ce | 2027 / Princess Curran | 02316186 | 0x095b911a -> 0x00000801 | 2049 / 26652, 4697 / 55286 |
| 0x000019d0 | 2029 / Malice Ascendant | 14255590 | 0x095b911e -> 0x00000803 | 2051 / 26678, 4699 / 55312 |

完整22B主副record、逆表源行、ROM密码word/key/解密值见 cid-proof.json. data/card-stats.s 的 card_NNNN 索引按十进制读, 不误当十六进制. 0x151e0000 的第五栈参数在 e7e0..e7e8 建立, setup_equip_oam_entry_with_sprite_attr 在 asm/14_equip_ai_scoring.s:4974-4979 实读 [sp+0x1c], lo16 OR4写context+4, hi16写context+6; 0x151e已证实Last Turn. 0x0450140c低CID为Dimensionhole, 0x044e0000只按已解码位域命名prefix, 不推造类型名.

## 消费者证据 (R6)

以下uses均由实际Thumb LDR opcode (op&0xf800)==0x4800, pool=((PC+4)&~3)+(imm8*4)解码, 排除旧plate/注释中的伪命中. 原指令给当前asm行, 新指令给objdump证据行. 8个table words由共同MOV-pc消费者解释, 不伪造literal LDR. confidence=high指机器码/基址/返回分支闭合; 未映射CID仅数值用途为high, 无卡名推断.

| 槽 / 原label / 原值 | 动作 / 语义 | 真实消费者 |
| --- | --- | --- |
| 0x0809e71c / DWORD_0809e71c / 0x0201c4e0 | RENAME gP1LifePoints | 0x0809e6fc asm/13_equip_placement.s:2106 |
| 0x0809e720 / DWORD_0809e720 / 0x00001ce8 | EQ P1LP_BLOCK2_OFF_1CE8 | 0x0809e6fe asm/13_equip_placement.s:2107 |
| 0x0809e724 / DWORD_0809e724 / 0x00001d34 | EQ EQUIP_ACTIVATION_SUBPHASE_OFF | 0x0809e704 asm/13_equip_placement.s:2110 |
| 0x0809e728 / PTR_PTR_0809e728 / 0x0809e72c | REF equip_activation_subphase_targets | 0x0809e714 asm/13_equip_placement.s:2119 |
| 0x0809e72c / PTR_DAT_0809e72c / 0x0809e74c | REF equip_activation_subphase_case0 | table[e6f4 subphase] -> MOV pc,r0 @0809e71a |
| 0x0809e730 / (unlabeled table word) / 0x0809e76c | REF equip_activation_subphase_case1 | table[e6f4 subphase] -> MOV pc,r0 @0809e71a |
| 0x0809e734 / (unlabeled table word) / 0x0809e7c4 | REF equip_activation_subphase_case2 | table[e6f4 subphase] -> MOV pc,r0 @0809e71a |
| 0x0809e738 / (unlabeled table word) / 0x0809e7d8 | REF equip_activation_subphase_case3 | table[e6f4 subphase] -> MOV pc,r0 @0809e71a |
| 0x0809e73c / (unlabeled table word) / 0x0809e800 | REF equip_activation_subphase_case4 | table[e6f4 subphase] -> MOV pc,r0 @0809e71a |
| 0x0809e740 / (unlabeled table word) / 0x0809e850 | REF equip_activation_subphase_case5 | table[e6f4 subphase] -> MOV pc,r0 @0809e71a |
| 0x0809e744 / (unlabeled table word) / 0x0809e894 | REF equip_activation_subphase_case6 | table[e6f4 subphase] -> MOV pc,r0 @0809e71a |
| 0x0809e748 / (unlabeled table word) / 0x0809e8b0 | REF equip_activation_subphase_case7 | table[e6f4 subphase] -> MOV pc,r0 @0809e71a |
| 0x0809e760 / (new pool) / 0x00001cf8 | EQ EQUIP_ACTIVATION_SAVED_PHASE_OFF | 0x0809e74c f13-seg2-block-objdump.txt:8 |
| 0x0809e764 / (new pool) / 0x00001cf4 | EQ P2LP_BLOCK2_OFF_1CF4 | 0x0809e750 f13-seg2-block-objdump.txt:10 |
| 0x0809e768 / (new pool) / 0x00001d34 | EQ EQUIP_ACTIVATION_SUBPHASE_OFF | 0x0809e758 f13-seg2-block-objdump.txt:14 |
| 0x0809e7a0 / (new pool) / 0x0000151e | EQ LAST_TURN_CID | 0x0809e780 f13-seg2-block-objdump.txt:32 |
| 0x0809e7a4 / (new pool) / 0x0000011d | EQ CARD_DISPLAY_OP31_LP_BAR_SUB | 0x0809e78e f13-seg2-block-objdump.txt:38 |
| 0x0809e7a8 / (new pool) / 0x0201c4e0 | REF gP1LifePoints | 0x0809e796 f13-seg2-block-objdump.txt:41 |
| 0x0809e7ac / (new pool) / 0x00001d34 | EQ EQUIP_ACTIVATION_SUBPHASE_OFF | 0x0809e798 f13-seg2-block-objdump.txt:42 |
| 0x0809e7bc / (new pool) / 0x0201c4e0 | REF gP1LifePoints | 0x0809e7b0 f13-seg2-block-objdump.txt:54 |
| 0x0809e7c0 / (new pool) / 0x00001d34 | EQ EQUIP_ACTIVATION_SUBPHASE_OFF | 0x0809e7b2 f13-seg2-block-objdump.txt:55 |
| 0x0809e7d4 / (new pool) / 0x0000151e | EQ LAST_TURN_CID | 0x0809e7c4 f13-seg2-block-objdump.txt:64 |
| 0x0809e7f4 / (new pool) / 0x151e0000 | EQ LAST_TURN_SETUP_EXTRA_WORD | 0x0809e7de f13-seg2-block-objdump.txt:75 |
| 0x0809e7f8 / (new pool) / 0x0201c4e0 | REF gP1LifePoints | 0x0809e7ec f13-seg2-block-objdump.txt:81 |
| 0x0809e7fc / (new pool) / 0x00001d34 | EQ EQUIP_ACTIVATION_SUBPHASE_OFF | 0x0809e7ee f13-seg2-block-objdump.txt:82 |
| 0x0809e848 / (new pool) / 0x0201c4e0 | REF gP1LifePoints | 0x0809e840 f13-seg2-block-objdump.txt:119 |
| 0x0809e84c / (new pool) / 0x00001d34 | EQ EQUIP_ACTIVATION_SUBPHASE_OFF | 0x0809e842 f13-seg2-block-objdump.txt:120 |
| 0x0809e86c / (new pool) / 0x00001cf8 | EQ EQUIP_ACTIVATION_SAVED_PHASE_OFF | 0x0809e850 f13-seg2-block-objdump.txt:127 |
| 0x0809e870 / (new pool) / 0x00001d28 | EQ EQUIP_CHAIN_STEP_OFF | 0x0809e85a f13-seg2-block-objdump.txt:132 |
| 0x0809e888 / (new pool) / 0x00001d28 | EQ EQUIP_CHAIN_STEP_OFF | 0x0809e874 f13-seg2-block-objdump.txt:145 |
| 0x0809e88c / (new pool) / 0x00001d2c | EQ EQUIP_CHAIN_ACTIVE_OFF | 0x0809e87c f13-seg2-block-objdump.txt:149 |
| 0x0809e890 / (new pool) / 0x00001d34 | EQ EQUIP_ACTIVATION_SUBPHASE_OFF | 0x0809e882 f13-seg2-block-objdump.txt:152 |
| 0x0809e8a8 / (new pool) / 0x0201c4e0 | REF gP1LifePoints | 0x0809e89e f13-seg2-block-objdump.txt:165 |
| 0x0809e8ac / (new pool) / 0x00001d34 | EQ EQUIP_ACTIVATION_SUBPHASE_OFF | 0x0809e8a0 f13-seg2-block-objdump.txt:166 |
| 0x0809e8e8 / (new pool) / 0x0201c4e0 | REF gP1LifePoints | 0x0809e8b0 f13-seg2-block-objdump.txt:174, 0x0809e8d8 f13-seg2-block-objdump.txt:193 |
| 0x0809e8ec / (new pool) / 0x00001cf8 | EQ EQUIP_ACTIVATION_SAVED_PHASE_OFF | 0x0809e8b2 f13-seg2-block-objdump.txt:175 |
| 0x0809e8f0 / (new pool) / 0x00001d34 | EQ EQUIP_ACTIVATION_SUBPHASE_OFF | 0x0809e8da f13-seg2-block-objdump.txt:194 |
| 0x0809e918 / PTR_gP1LifePoints_0809e918 / 0x0201c4e0 | RENAME gP1LifePoints | 0x0809e906 asm/13_equip_placement.s:2155 |
| 0x0809e91c / DAT_0809e91c / 0x00001d34 | EQ EQUIP_ACTIVATION_SUBPHASE_OFF | 0x0809e908 asm/13_equip_placement.s:2156 |
| 0x0809e9b0 / PTR_gP1LifePoints_0809e9b0 / 0x0201c4e0 | RENAME gP1LifePoints | 0x0809e92e asm/13_equip_placement.s:2179 |
| 0x0809e9b4 / DAT_0809e9b4 / 0x00001d24 | EQ EQUIP_ACTIVATION_SCAN_CURSOR_OFF | 0x0809e930 asm/13_equip_placement.s:2180 |
| 0x0809e9b8 / DAT_0809e9b8 / 0x0000ffff | EQ EQUIP_ACTIVATION_CID_U16_MASK | 0x0809e970 asm/13_equip_placement.s:2212 |
| 0x0809e9bc / DAT_0809e9bc / 0x00000868 | EQ PLAYER_BLOCK_STRIDE | 0x0809e97c asm/13_equip_placement.s:2218 |
| 0x0809e9dc / PTR_gP1LifePoints_0809e9dc / 0x0201c4e0 | RENAME gP1LifePoints | 0x0809e9c6 asm/13_equip_placement.s:2255 |
| 0x0809ea70 / PTR_gP1LifePoints_0809ea70 / 0x0201c4e0 | RENAME gP1LifePoints | 0x0809e9ee asm/13_equip_placement.s:2280 |
| 0x0809ea74 / DAT_0809ea74 / 0x00001d24 | EQ EQUIP_ACTIVATION_SCAN_CURSOR_OFF | 0x0809e9f0 asm/13_equip_placement.s:2281 |
| 0x0809ea78 / DAT_0809ea78 / 0x0000ffff | EQ EQUIP_ACTIVATION_CID_U16_MASK | 0x0809ea32 asm/13_equip_placement.s:2314 |
| 0x0809ea7c / DAT_0809ea7c / 0x00000868 | EQ PLAYER_BLOCK_STRIDE | 0x0809ea3e asm/13_equip_placement.s:2320 |
| 0x0809ea9c / PTR_gP1LifePoints_0809ea9c / 0x0201c4e0 | RENAME gP1LifePoints | 0x0809ea86 asm/13_equip_placement.s:2356 |
| 0x0809eaac / DAT_0809eaac / 0x000013ff | EQ JAM_BREEDING_MACHINE_CID | 0x0809eaa2 asm/13_equip_placement.s:2375 |
| 0x0809eabc / DAT_0809eabc / 0x00001494 | EQ BLIND_DESTRUCTION_CID | 0x0809eab2 asm/13_equip_placement.s:2385 |
| 0x0809eacc / DAT_0809eacc / 0x00001519 | EQ OMINOUS_FORTUNETELLING_CID | 0x0809eac2 asm/13_equip_placement.s:2395 |
| 0x0809eadc / DAT_0809eadc / 0x00001545 | EQ NEEDLE_WALL_CID | 0x0809ead2 asm/13_equip_placement.s:2405 |
| 0x0809eaec / DAT_0809eaec / 0x00001738 | EQ DANGEROUS_MACHINE_TYPE6_CID | 0x0809eae2 asm/13_equip_placement.s:2415 |
| 0x0809eb24 / DAT_0809eb24 / 0x0000140c | EQ DIMENSIONHOLE_CID | 0x0809eaf4 asm/13_equip_placement.s:2426 |
| 0x0809eb28 / DAT_0809eb28 / 0x0450140c | EQ DIMENSIONHOLE_PACKED_ACTIVATION_ATTR | 0x0809eb04 asm/13_equip_placement.s:2433 |
| 0x0809eb40 / DAT_0809eb40 / 0x000011cf | EQ get_card_lp_cost_by_id_cid_11cf | 0x0809eb36 asm/13_equip_placement.s:2462 |
| 0x0809eb50 / DAT_0809eb50 / 0x00001578 | EQ LAVA_GOLEM_CID | 0x0809eb46 asm/13_equip_placement.s:2472 |
| 0x0809ebdc / PTR_gP1LifePoints_0809ebdc / 0x0201c4e0 | RENAME gP1LifePoints | 0x0809eb5e asm/13_equip_placement.s:2486 |
| 0x0809ebe0 / DAT_0809ebe0 / 0x00001d24 | EQ EQUIP_ACTIVATION_SCAN_CURSOR_OFF | 0x0809eb60 asm/13_equip_placement.s:2487 |
| 0x0809ebe4 / DAT_0809ebe4 / 0x00001338 | EQ EQUIP_ACTIVATION_UNMAPPED_CID_1338 | 0x0809eb76 asm/13_equip_placement.s:2499 |
| 0x0809ebe8 / DAT_0809ebe8 / 0x00000868 | EQ PLAYER_BLOCK_STRIDE | 0x0809eb94 asm/13_equip_placement.s:2512 |
| 0x0809ec10 / DAT_0809ec10 / 0x00001450 | EQ SPIRIT_OF_THE_BREEZE_CID | 0x0809ec06 asm/13_equip_placement.s:2573 |
| 0x0809ec20 / DAT_0809ec20 / 0x00001451 | EQ DANCING_FAIRY_CID | 0x0809ec16 asm/13_equip_placement.s:2583 |
| 0x0809ec30 / DAT_0809ec30 / 0x00001454 | EQ CURE_MERMAID_CID | 0x0809ec26 asm/13_equip_placement.s:2593 |
| 0x0809ec4c / PTR_gP1LifePoints_0809ec4c / 0x0201c4e0 | RENAME gP1LifePoints | 0x0809ec3c asm/13_equip_placement.s:2606 |
| 0x0809ec50 / DAT_0809ec50 / 0x00001d24 | EQ EQUIP_ACTIVATION_SCAN_CURSOR_OFF | 0x0809ec3e asm/13_equip_placement.s:2607 |
| 0x0809ecc8 / DAT_0809ecc8 / 0x00000868 | EQ PLAYER_BLOCK_STRIDE | 0x0809ec5a asm/13_equip_placement.s:2622 |
| 0x0809eccc / DAT_0809eccc / 0x00201fff | EQ CARD_WORD_CID_AND_BIT21_MASK | 0x0809ec82 asm/13_equip_placement.s:2643 |
| 0x0809ecd0 / DAT_0809ecd0 / 0x00001459 | EQ MARIE_THE_FALLEN_ONE_CID | 0x0809ec86 asm/13_equip_placement.s:2645 |
| 0x0809ecd4 / DAT_0809ecd4 / 0x044e0000 | EQ EQUIP_ACTIVATION_CARD_ARRAY_ATTR_PREFIX | 0x0809ec90 asm/13_equip_placement.s:2650 |
| 0x0809ecd8 / PTR_gP1LifePoints_0809ecd8 / 0x0201c4e0 | RENAME gP1LifePoints | 0x0809ecb0 asm/13_equip_placement.s:2667 |
| 0x0809ecdc / DAT_0809ecdc / 0x00001d24 | EQ EQUIP_ACTIVATION_SCAN_CURSOR_OFF | 0x0809ecb2 asm/13_equip_placement.s:2668 |
| 0x0809ecfc / DAT_0809ecfc / 0x00001628 | EQ SENRI_EYE_CID | 0x0809ecf2 asm/13_equip_placement.s:2706 |
| 0x0809ed0c / DAT_0809ed0c / 0x00001757 | EQ WHITE_MAGICIAN_PIKERU_CID | 0x0809ed02 asm/13_equip_placement.s:2716 |
| 0x0809ed1c / DAT_0809ed1c / 0x0000191d | EQ EBON_MAGICIAN_CURRAN_CID | 0x0809ed12 asm/13_equip_placement.s:2726 |
| 0x0809ed2c / DAT_0809ed2c / 0x000019cd | EQ PRINCESS_PIKERU_CID | 0x0809ed22 asm/13_equip_placement.s:2736 |
| 0x0809ed3c / DAT_0809ed3c / 0x000019ce | EQ PRINCESS_CURRAN_CID | 0x0809ed32 asm/13_equip_placement.s:2746 |
| 0x0809ed4c / DAT_0809ed4c / 0x00001637 | EQ BOWGANIAN_CID | 0x0809ed42 asm/13_equip_placement.s:2756 |
| 0x0809ede8 / PTR_gP1LifePoints_0809ede8 / 0x0201c4e0 | RENAME gP1LifePoints | 0x0809ed5c asm/13_equip_placement.s:2771 |
| 0x0809edec / DAT_0809edec / 0x00001d24 | EQ EQUIP_ACTIVATION_SCAN_CURSOR_OFF | 0x0809ed5e asm/13_equip_placement.s:2772 |
| 0x0809edf0 / DAT_0809edf0 / 0x00000868 | EQ PLAYER_BLOCK_STRIDE | 0x0809ed94 asm/13_equip_placement.s:2798 |
| 0x0809edf4 / DAT_0809edf4 / 0x00001690 | EQ INFERNALQUEEN_ARCHFIEND_CID | 0x0809eda8 asm/13_equip_placement.s:2808 |
| 0x0809eea8 / PTR_gP1LifePoints_0809eea8 / 0x0201c4e0 | RENAME gP1LifePoints | 0x0809ee20 asm/13_equip_placement.s:2872 |
| 0x0809eeac / DAT_0809eeac / 0x00001d24 | EQ EQUIP_ACTIVATION_SCAN_CURSOR_OFF | 0x0809ee22 asm/13_equip_placement.s:2873 |
| 0x0809eeb0 / DAT_0809eeb0 / 0x00001491 | EQ GRAVEROBBERS_RETRIBUTION_CID | 0x0809ee38 asm/13_equip_placement.s:2885 |
| 0x0809eeb4 / DAT_0809eeb4 / 0x00000868 | EQ PLAYER_BLOCK_STRIDE | 0x0809ee6a asm/13_equip_placement.s:2909 |
| 0x0809eeb8 / DAT_0809eeb8 / 0x0201c510 | REF gDuelFieldSlots | 0x0809ee70 asm/13_equip_placement.s:2912 |
| 0x0809ef60 / PTR_gP1LifePoints_0809ef60 / 0x0201c4e0 | RENAME gP1LifePoints | 0x0809eee0 asm/13_equip_placement.s:2972 |
| 0x0809ef64 / DAT_0809ef64 / 0x00001d24 | EQ EQUIP_ACTIVATION_SCAN_CURSOR_OFF | 0x0809eee2 asm/13_equip_placement.s:2973 |
| 0x0809ef68 / DAT_0809ef68 / 0x00001406 | EQ BURNING_LAND_CID | 0x0809ef0e asm/13_equip_placement.s:2994, 0x0809ef50 asm/13_equip_placement.s:3025 |
| 0x0809ef6c / DAT_0809ef6c / 0x00000868 | EQ PLAYER_BLOCK_STRIDE | 0x0809ef22 asm/13_equip_placement.s:3003 |
| 0x0809ef94 / DAT_0809ef94 / 0x000013f0 | EQ MASK_OF_DISPEL_CID | 0x0809ef8a asm/13_equip_placement.s:3059 |
| 0x0809efa4 / DAT_0809efa4 / 0x000013f3 | EQ MASK_OF_THE_ACCURSED_CID | 0x0809ef9a asm/13_equip_placement.s:3069 |
| 0x0809efb4 / DAT_0809efb4 / 0x000014b2 | EQ NIGHTMARE_WHEEL_CID | 0x0809efaa asm/13_equip_placement.s:3079 |
| 0x0809efcc / DAT_0809efcc / 0x00001322 | EQ SNATCH_STEAL_CID | 0x0809efc0 asm/13_equip_placement.s:3092 |
| 0x0809efe4 / DAT_0809efe4 / 0x00001877 | EQ BRAIN_JACKER_CID | 0x0809efd8 asm/13_equip_placement.s:3106 |
| 0x0809effc / DAT_0809effc / 0x0000169a | EQ FALLING_DOWN_CID | 0x0809eff0 asm/13_equip_placement.s:3120 |
| 0x0809f014 / DAT_0809f014 / 0x0000137b | EQ EYE_OF_TRUTH_CID | 0x0809f008 asm/13_equip_placement.s:3134 |
| 0x0809f02c / DAT_0809f02c / 0x00001355 | EQ MINOR_GOBLIN_OFFICIAL_CID | 0x0809f020 asm/13_equip_placement.s:3148 |
| 0x0809f044 / DAT_0809f044 / 0x00001286 | EQ BLAST_SPHERE_CID | 0x0809f038 asm/13_equip_placement.s:3162 |
| 0x0809f05c / DAT_0809f05c / 0x000019bd | EQ ADHESIVE_EXPLOSIVE_CID | 0x0809f050 asm/13_equip_placement.s:3176 |
| 0x0809f074 / DAT_0809f074 / 0x000019d0 | EQ MALICE_ASCENDANT_CID | 0x0809f068 asm/13_equip_placement.s:3190 |
| 0x0809f128 / PTR_gP1LifePoints_0809f128 / 0x0201c4e0 | RENAME gP1LifePoints | 0x0809f084 asm/13_equip_placement.s:3206 |
| 0x0809f12c / DAT_0809f12c / 0x00001d24 | EQ EQUIP_ACTIVATION_SCAN_CURSOR_OFF | 0x0809f086 asm/13_equip_placement.s:3207 |
| 0x0809f130 / DAT_0809f130 / 0x00001370 | EQ KISEITAI_CID | 0x0809f0ac asm/13_equip_placement.s:3227 |
| 0x0809f134 / DAT_0809f134 / 0x0000ffff | EQ EQUIP_CHAIN_PAIR_MISSING | 0x0809f0c8 asm/13_equip_placement.s:3239 |
| 0x0809f138 / DAT_0809f138 / 0x00000868 | EQ PLAYER_BLOCK_STRIDE | 0x0809f0e4 asm/13_equip_placement.s:3252 |
| 0x0809f1cc / PTR_gP1LifePoints_0809f1cc / 0x0201c4e0 | RENAME gP1LifePoints | 0x0809f170 asm/13_equip_placement.s:3324 |
| 0x0809f1d0 / DAT_0809f1d0 / 0x00000868 | EQ PLAYER_BLOCK_STRIDE | 0x0809f176 asm/13_equip_placement.s:3327 |
| 0x0809f1d4 / DAT_0809f1d4 / 0x0201c8f8 | REF gP1HandSlotArray | 0x0809f190 asm/13_equip_placement.s:3341 |
| 0x0809f1d8 / DAT_0809f1d8 / 0x044e0000 | EQ EQUIP_ACTIVATION_CARD_ARRAY_ATTR_PREFIX | 0x0809f1a8 asm/13_equip_placement.s:3353 |
| 0x0809f1f8 / DAT_0809f1f8 / 0x00000868 | EQ PLAYER_BLOCK_STRIDE | 0x0809f1de asm/13_equip_placement.s:3380 |
| 0x0809f208 / DAT_0809f208 / 0x00001181 | EQ SINISTER_SERPENT_CID | 0x0809f1fe asm/13_equip_placement.s:3401 |
| 0x0809f218 / DAT_0809f218 / 0x000019cb | EQ TREEBORN_FROG_CID | 0x0809f20e asm/13_equip_placement.s:3411 |
| 0x0809f2f8 / PTR_gP1LifePoints_0809f2f8 / 0x0201c4e0 | RENAME gP1LifePoints | 0x0809f22c asm/13_equip_placement.s:3428 |
| 0x0809f2fc / DAT_0809f2fc / 0x00000868 | EQ PLAYER_BLOCK_STRIDE | 0x0809f232 asm/13_equip_placement.s:3431 |
| 0x0809f300 / DAT_0809f300 / 0x0201c8f8 | REF gP1HandSlotArray | 0x0809f250 asm/13_equip_placement.s:3447 |
| 0x0809f304 / DAT_0809f304 / 0x00201fff | EQ CARD_WORD_CID_AND_BIT21_MASK | 0x0809f25a asm/13_equip_placement.s:3452 |
| 0x0809f308 / DAT_0809f308 / 0x00001775 | EQ RETURN_ZOMBIE_CID | 0x0809f25e asm/13_equip_placement.s:3454 |
| 0x0809f30c / DAT_0809f30c / 0xfffff03f | EQ ACTIVATION_ENTRY_CLR_BITS_11_6 | 0x0809f29e asm/13_equip_placement.s:3485 |
| 0x0809f310 / DAT_0809f310 / 0xffff803f | EQ ACTIVATION_ENTRY_CLR_BITS_14_6 | 0x0809f2ba asm/13_equip_placement.s:3499 |
| 0x0809f314 / DAT_0809f314 / 0x044e0000 | EQ EQUIP_ACTIVATION_CARD_ARRAY_ATTR_PREFIX | 0x0809f2d6 asm/13_equip_placement.s:3512 |
| 0x0809f340 / PTR_gP1LifePoints_0809f340 / 0x0201c4e0 | RENAME gP1LifePoints | 0x0809f31a asm/13_equip_placement.s:3546 |
| 0x0809f344 / DAT_0809f344 / 0x00000868 | EQ PLAYER_BLOCK_STRIDE | 0x0809f31c asm/13_equip_placement.s:3547 |
| 0x0809f3d8 / PTR_gP1LifePoints_0809f3d8 / 0x0201c4e0 | RENAME gP1LifePoints | 0x0809f356 asm/13_equip_placement.s:3581 |
| 0x0809f3dc / DAT_0809f3dc / 0x00001d24 | EQ EQUIP_ACTIVATION_SCAN_CURSOR_OFF | 0x0809f358 asm/13_equip_placement.s:3582 |
| 0x0809f3e0 / DAT_0809f3e0 / 0x00000868 | EQ PLAYER_BLOCK_STRIDE | 0x0809f376 asm/13_equip_placement.s:3598 |
| 0x0809f3e4 / DAT_0809f3e4 / 0x0201c510 | REF gDuelFieldSlots | 0x0809f37c asm/13_equip_placement.s:3601 |
| 0x0809f3e8 / DAT_0809f3e8 / 0x000013b2 | EQ MUCUS_YOLK_CID | 0x0809f38c asm/13_equip_placement.s:3609, 0x0809f39a asm/13_equip_placement.s:3615 |
| 0x0809f418 / DAT_0809f418 / 0x0000154d | EQ LEGENDARY_FIEND_CID | 0x0809f40e asm/13_equip_placement.s:3676 |
| 0x0809f428 / DAT_0809f428 / 0x00001645 | EQ EXODIA_NECROSS_CID | 0x0809f41e asm/13_equip_placement.s:3686 |
| 0x0809f438 / DAT_0809f438 / 0x0000160e | EQ AMAZONESS_BLOWPIPER_CID | 0x0809f42e asm/13_equip_placement.s:3696 |
| 0x0809f494 / PTR_gP1LifePoints_0809f494 / 0x0201c4e0 | RENAME gP1LifePoints | 0x0809f450 asm/13_equip_placement.s:3717 |
| 0x0809f498 / DAT_0809f498 / 0x00001d24 | EQ EQUIP_ACTIVATION_SCAN_CURSOR_OFF | 0x0809f452 asm/13_equip_placement.s:3718 |
| 0x0809f49c / DAT_0809f49c / 0x00000868 | EQ PLAYER_BLOCK_STRIDE | 0x0809f466 asm/13_equip_placement.s:3728 |
| 0x0809f4a0 / DAT_0809f4a0 / 0x00001812 | EQ SILENT_SWORDSMAN_LV3_CID | 0x0809f47c asm/13_equip_placement.s:3740 |
| 0x0809f4a8 / DAT_0809f4a8 / 0x000017d9 | EQ ARMED_DRAGON_LV3_CID | 0x0809f4a4 asm/13_equip_placement.s:3761 |
| 0x0809f4c0 / DAT_0809f4c0 / 0x00001817 | EQ SILENT_MAGICIAN_LV4_CID | 0x0809f4ac asm/13_equip_placement.s:3766 |
| 0x0809f518 / DAT_0809f518 / 0x00001822 | EQ ULTIMATE_INSECT_LV3_CID | 0x0809f4c4 asm/13_equip_placement.s:3780 |
| 0x0809f51c / DAT_0809f51c / 0x0201c510 | REF gDuelFieldSlots | 0x0809f4d8 asm/13_equip_placement.s:3791 |
| 0x0809f520 / DAT_0809f520 / 0x00001cf4 | EQ FIELD_STATE_OFF | 0x0809f50a asm/13_equip_placement.s:3815 |
| 0x0809f57c / DAT_0809f57c / 0x0000ffff | EQ EQUIP_ACTIVATION_CID_U16_MASK | 0x0809f55e asm/13_equip_placement.s:3862 |
| 0x0809f580 / DAT_0809f580 / 0x044e0000 | EQ EQUIP_ACTIVATION_CARD_ARRAY_ATTR_PREFIX | 0x0809f562 asm/13_equip_placement.s:3864 |
| 0x0809f590 / DAT_0809f590 / 0x000013c7 | EQ REVIVAL_JAM_CID | 0x0809f586 asm/13_equip_placement.s:3885 |
| 0x0809f5a0 / DAT_0809f5a0 / 0x00001522 | EQ VAMPIRE_LORD_CID | 0x0809f596 asm/13_equip_placement.s:3895 |
| 0x0809f5b0 / DAT_0809f5b0 / 0x0000185c | EQ SACRED_PHOENIX_CID | 0x0809f5a6 asm/13_equip_placement.s:3905 |
| 0x0809f5c0 / DAT_0809f5c0 / 0x0000188f | EQ CURSE_OF_VAMPIRE_CID | 0x0809f5b6 asm/13_equip_placement.s:3915 |
| 0x0809f5d8 / DAT_0809f5d8 / 0x0000188f | EQ CURSE_OF_VAMPIRE_CID | 0x0809f5cc asm/13_equip_placement.s:3928 |
| 0x0809f67c / PTR_gP1LifePoints_0809f67c / 0x0201c4e0 | RENAME gP1LifePoints | 0x0809f5ec asm/13_equip_placement.s:3946, 0x0809f670 asm/13_equip_placement.s:4012 |
| 0x0809f680 / DAT_0809f680 / 0x00001d24 | EQ EQUIP_ACTIVATION_SCAN_CURSOR_OFF | 0x0809f5ee asm/13_equip_placement.s:3947 |
| 0x0809f684 / DAT_0809f684 / 0x0000ffff | EQ EQUIP_ACTIVATION_CID_U16_MASK | 0x0809f602 asm/13_equip_placement.s:3957 |
| 0x0809f688 / DAT_0809f688 / 0x00000868 | EQ PLAYER_BLOCK_STRIDE | 0x0809f642 asm/13_equip_placement.s:3989 |
| 0x0809f6dc / DAT_0809f6dc / 0x00001da8 | EQ LP_CARD_TRACK_BASE_OFF | 0x0809f68c asm/13_equip_placement.s:4027 |
| 0x0809f6e0 / DAT_0809f6e0 / 0x00000868 | EQ PLAYER_BLOCK_STRIDE | 0x0809f6a0 asm/13_equip_placement.s:4037 |
| 0x0809f718 / DAT_0809f718 / 0x00001367 | EQ EQUIP_ACTIVATION_UNMAPPED_CID_1367 | 0x0809f70c asm/13_equip_placement.s:4095 |
| 0x0809f728 / DAT_0809f728 / 0x000016d5 | EQ RECYCLE_CID | 0x0809f71e asm/13_equip_placement.s:4106 |
| 0x0809f740 / DAT_0809f740 / 0x00001485 | EQ AQUA_SPIRIT_CID | 0x0809f734 asm/13_equip_placement.s:4119 |

重要返回契约按真实分支订正: 通用e920/e9e0只有activation非零时提前return0; ed50/f44c/f538忽略该结果仍return0; ec34整数组扫描后即使无匹配也cursor++并return0. ee14的count helper只设r0=opponent,不是额外传CID; f21c special-summon helper恰以零为通过. f5dc初次扫描与非零cursor回访是两个路径,耗尽cursor10不清零. 具体完整契约见下列59plate.

## PLATE (R5, 全文替换)

59个新PLATE全部ASCII且最长469 chars. `f13-seg2-plates.json` 保存每个完整旧plate、旧SHA256、FunctionID/body/hash/incoming/EOL和完整新文本; root functions snapshot为真实Ghidra来源. 除8个新case EOL与158槽EOL外, 原Function内既有EOL不变. dispatcher body扩展是唯一body变化; 四个rename只改正式名, 其余55个Function名称不变.

### 0x0809e6f4 dispatch_equip_activation_state_by_subphase

ID=16934, old_plate_sha256=`6fe6ba67e0af89d933f2e31a92a3839847f1b78bd14daa7d72f224f4359f3038`, new_chars=469.

```text
No arguments. Dispatch LP+0x1d34 subphase 0..7 through eight even Thumb targets using MOV pc,r0. Player comes from LP+0x1ce8. Cases share this frame and return path: save phase, gate Last Turn, set display context, set sprite data, validate slots, set chain state, advance display, submit final sprite. Returns 1 for subphase >7 or case-4 rejection; otherwise 0. Case-1 rejection sets subphase=8; case 6 waits for a nonzero helper result. No independent case functions.
```

### 0x0809e904 check_activation_phase_counter_is_six

ID=7181, old_plate_sha256=`fbddba0f3f3d409b4e91e00f85366f66b8b2e3d870225c83af022e3539142c71`, new_chars=137.

```text
No arguments. Return 1 exactly when the u32 activation subphase at gP1LifePoints+0x1d34 equals 6, else 0. Read-only leaf; no stack frame.
```

### 0x0809e920 scan_monster_zone_for_equip_activation_by_card

ID=6813, old_plate_sha256=`956588055d1b66897230dfbf3e5e0281553778df3903160334e2a043e40059c2`, new_chars=374.

```text
r0=player, r1=internal CID. Resume monster slots 0..4 using the u32 cursor at LP+0x1d24. For each active CID match, build player/slot/CID packed attributes and pass decoded entry flags to apply_equip_activation_with_id_lookup. A nonzero helper result advances the cursor once and returns 0; zero continues scanning. Every rejected slot also advances. Return 1 on exhaustion.
```

### 0x0809e9e0 scan_trap_zone_for_equip_activation_by_card

ID=6814, old_plate_sha256=`3a4063e4477f5b6677605c36516d0bd8a04693c1d978cbc2a8d56fc71a6ea235`, new_chars=339.

```text
r0=player, r1=internal CID. Resume five spell/trap slots cursor+5 using LP+0x1d24 cursor 0..4. For active CID matches, pack player/slot/CID and decoded entry flags for apply_equip_activation_with_id_lookup. A nonzero helper result advances cursor and returns 0; zero continues scanning. Rejected slots also advance. Return 1 on exhaustion.
```

### 0x0809eaa0 scan_trap_zone_for_equip_activation_jam_breeding_machine

ID=6817, old_plate_sha256=`4115e2839fc59291765ccca4cf85c33d5411f570023f572d081dcfe658ccc51b`, new_chars=184.

```text
r0=player. Call scan_trap_zone_for_equip_activation_by_card(player, CID 0x13ff) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

### 0x0809eab0 scan_trap_zone_for_equip_activation_blind_destruction

ID=6818, old_plate_sha256=`3d32b9279877ddb558c1695155355e9991ab14847c0c011e1bf0b32f1b506d70`, new_chars=184.

```text
r0=player. Call scan_trap_zone_for_equip_activation_by_card(player, CID 0x1494) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

### 0x0809eac0 scan_trap_zone_for_equip_activation_ominous_fortunetelling

ID=6819, old_plate_sha256=`08ca05d3db591d8a26cd6050e14572e378e0cb1e60d8c9b2a9bdac9a05e52e64`, new_chars=184.

```text
r0=player. Call scan_trap_zone_for_equip_activation_by_card(player, CID 0x1519) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

### 0x0809ead0 scan_trap_zone_for_equip_activation_needle_wall

ID=6820, old_plate_sha256=`429d2cc228ef195f4bff5e5015047e373c2f14912eae0a9fba235cfe321a51e8`, new_chars=184.

```text
r0=player. Call scan_trap_zone_for_equip_activation_by_card(player, CID 0x1545) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

### 0x0809eae0 scan_trap_zone_for_equip_activation_dangerous_machine_type6

ID=6821, old_plate_sha256=`219d721e6b31d9f005287f9cd8f1edba1ac88f886fc538d8ffaf530a1ecdba34`, new_chars=184.

```text
r0=player. Call scan_trap_zone_for_equip_activation_by_card(player, CID 0x1738) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

### 0x0809eaf0 scan_equip_zone_for_dimensionhole

ID=6822, old_plate_sha256=`fa5dcef63eef932db8ef6916edbe33443020abe46ff236eaf94fe4be7071a40a`, new_chars=319.

```text
r0=player. Query zone 11 for Dimensionhole. Missing entity returns 1. Otherwise call apply_equip_activation_with_id_lookup with player bit OR 0x0450140c and zero entity/payload. If it returns zero, enqueue the zone-11 Dimensionhole sprite. Return 0 whenever the entity query succeeded, independent of activation result.
```

### 0x0809eb34 scan_monster_zone_for_equip_activation_reserved_icid_f

ID=6823, old_plate_sha256=`2cf97c11e58303af4e69e229885834ebf4805ce8456af0573c362882d3b081e8`, new_chars=187.

```text
r0=player. Call scan_monster_zone_for_equip_activation_by_card(player, CID 0x11cf) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

### 0x0809eb44 scan_monster_zone_for_equip_activation_lava_golem

ID=6824, old_plate_sha256=`a8e5bbab825293ac197cc122148501c26facc9825df1a56ec6796876a648e968`, new_chars=187.

```text
r0=player. Call scan_monster_zone_for_equip_activation_by_card(player, CID 0x1578) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

### 0x0809eb54 scan_monster_zone_slots_for_equip_activation_reserved_icid_g

ID=6825, old_plate_sha256=`648f4c869e23253fb5cbfaa3288e7f7ab9bf95f1dd3afc60a0a217823516d39f`, new_chars=342.

```text
r0=player. Resume monster slots 0..4 via LP+0x1d24. Require active CID 0x1338 and exactly one occupied monster slot. Enqueue entry flags; if entry+6 is zero, invoke activation with zero arguments. Set slot field bit 0x15, advance cursor and return 0. Other slots advance without emission; exhaustion returns 1. CID 0x1338 has no card mapping.
```

### 0x0809ec04 scan_monster_zone_for_equip_activation_spirit_of_the_breeze

ID=6826, old_plate_sha256=`8693f0868e0229af3e717411160e6bfc6905e720ef6befbcc61401fbd628057a`, new_chars=187.

```text
r0=player. Call scan_monster_zone_for_equip_activation_by_card(player, CID 0x1450) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

### 0x0809ec14 scan_monster_zone_for_equip_activation_dancing_fairy

ID=6827, old_plate_sha256=`33c6c490e3fb13bc8191c4c01d02a1dd3c3ce7da7302b407bc9d5548ddcae6da`, new_chars=187.

```text
r0=player. Call scan_monster_zone_for_equip_activation_by_card(player, CID 0x1451) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

### 0x0809ec24 scan_monster_zone_for_equip_activation_cure_mermaid

ID=6828, old_plate_sha256=`bb24933bb700203105d7780747ed2af534b3ff58d27fd2797d2bb521e1cc3230`, new_chars=187.

```text
r0=player. Call scan_monster_zone_for_equip_activation_by_card(player, CID 0x1454) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

### 0x0809ec34 scan_player_card_array_for_equip_activation_marie_the_fallen_one

ID=6829, old_plate_sha256=`18d8428070a4b512558374c62cdf4f849d8bb74c854b9d61ef38c40842c27256`, new_chars=379.

```text
r0=player. If LP+0x1d24 is nonzero, return 1. Otherwise scan the player 4-byte card-word array at gP1HandSlotArray with count LP+0x14 and stride 0x868. Match (word & 0x00201fff)==MARIE_THE_FALLEN_ONE_CID, pack each match with 0x044e0000 and player bit, and call activation with decoded flags. Ignore each result. Increment the shared cursor and return 0 even if no entry matched.
```

### 0x0809ece0 scan_trap_zone_for_equip_activation_life_absorbing_machine

ID=15806, old_plate_sha256=`01878404853ec7c92b852a0c7b571302a82ba41173db5b40baf720885d7817ce`, new_chars=184.

```text
r0=player. Call scan_trap_zone_for_equip_activation_by_card(player, CID 0x14c0) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

### 0x0809ecf0 scan_trap_zone_for_equip_activation_senri_eye

ID=15807, old_plate_sha256=`d1a560e2d14b237cc0cf8bd9b8c07c007aa2ef9e8c177abb44b30029b8ebdce6`, new_chars=184.

```text
r0=player. Call scan_trap_zone_for_equip_activation_by_card(player, CID 0x1628) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

### 0x0809ed00 scan_monster_zone_for_equip_activation_white_magician_pikeru

ID=6830, old_plate_sha256=`f87ec6fa9a16f0b36dda707377000889d437bc506cf4414b9dcc9dfc9d25e4ef`, new_chars=187.

```text
r0=player. Call scan_monster_zone_for_equip_activation_by_card(player, CID 0x1757) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

### 0x0809ed10 scan_monster_zone_for_equip_activation_ebon_magician_curran

ID=6831, old_plate_sha256=`a75739b3d310ed88f22cde94956a375e64c13f71e000abf08c76bcb3ecde908e`, new_chars=187.

```text
r0=player. Call scan_monster_zone_for_equip_activation_by_card(player, CID 0x191d) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

### 0x0809ed20 scan_monster_zone_for_equip_activation_princess_pikeru

ID=6832, old_plate_sha256=`8d8279ee7b241be35d721ecadf3e794cff75f24257e6f29938a3191566065e25`, new_chars=187.

```text
r0=player. Call scan_monster_zone_for_equip_activation_by_card(player, CID 0x19cd) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

### 0x0809ed30 scan_monster_zone_for_equip_activation_princess_curran

ID=6833, old_plate_sha256=`6965162eca2e6a9403247cfb37f5a9ed9f4dddfd5ead12bed5274288f9a1f71c`, new_chars=187.

```text
r0=player. Call scan_monster_zone_for_equip_activation_by_card(player, CID 0x19ce) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

### 0x0809ed40 scan_monster_zone_for_equip_activation_bowganian

ID=6834, old_plate_sha256=`1d9b755b92f94437e09146a24dcd6033be88796df32a808134fce2e3f59aa922`, new_chars=187.

```text
r0=player. Call scan_monster_zone_for_equip_activation_by_card(player, CID 0x1637) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

### 0x0809ed50 scan_all_monster_zone_slots_for_equip_activation_infernalqueen_archfiend

ID=6835, old_plate_sha256=`93c4ad8ba5f608c53307a5e3cd98628a7525395d7ebed53f713e833675c0afcc`, new_chars=347.

```text
r0=player. Resume ten monster slots with LP+0x1d24 cursor: side=(cursor/5)^player, slot=cursor%5. For active Infernalqueen Archfiend, pack the actual entry CID, side and slot, then call activation with decoded flags. Ignore its result; advance cursor and return 0 after the first match. Other entries advance and continue. Return 1 after cursor 9.
```

### 0x0809ee14 scan_all_zone_slots_for_equip_lp_indicator_graverobbers_retribution

ID=6836, old_plate_sha256=`98e8e2194fb060717182fe167dd4c71e881b1ab9792fd88274f21083b1116f0a`, new_chars=359.

```text
r0=player. Start LP+0x1d24 at 5 when zero and scan spell/trap slots through 9. Require active Graverobber's Retribution and nonzero count_zone_slots_with_card_field5(1-player). Enqueue entry flags, then the opponent LP indicator with amount=count*100, mode=1 and this CID. Advance cursor and return 0 on emission; rejected slots advance. Exhaustion returns 1.
```

### 0x0809eed8 scan_all_zone_slots_for_lp_indicator_burning_land

ID=6837, old_plate_sha256=`6f6e757c6f212e4aabe171380a0351718bb46e3add40f3edb349e44384650e29`, new_chars=318.

```text
r0=player. Resume ten spell/trap slots: side=(cursor/5)^player, slot=cursor%5+5, cursor at LP+0x1d24. On active Burning Land, enqueue entry flags and an LP indicator for the input player, amount 500, mode=(side!=player), CID Burning Land. Advance cursor and return 0; rejected entries advance. Return 1 after cursor 9.
```

### 0x0809ef88 scan_trap_zone_for_equip_activation_mask_of_dispel

ID=15808, old_plate_sha256=`e4610634f225cbc1c0b24fca4442c5dabe031c3ade9eb4fcc57504cba09a37b2`, new_chars=184.

```text
r0=player. Call scan_trap_zone_for_equip_activation_by_card(player, CID 0x13f0) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

### 0x0809ef98 scan_trap_zone_for_equip_activation_mask_of_accursed

ID=6838, old_plate_sha256=`fa3d11e01d3141a35735f39d8a3cf2ef89aa5909c3b532840be7d23638811297`, new_chars=184.

```text
r0=player. Call scan_trap_zone_for_equip_activation_by_card(player, CID 0x13f3) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

### 0x0809efa8 scan_trap_zone_for_equip_activation_nightmare_wheel

ID=6839, old_plate_sha256=`6117d2d50a8b5f7a8b1102a1dfa45b348efbded04b84c2c5c1c1dc2f42b25226`, new_chars=184.

```text
r0=player. Call scan_trap_zone_for_equip_activation_by_card(player, CID 0x14b2) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

### 0x0809efb8 scan_trap_zone_for_equip_activation_snatch_steal

ID=6840, old_plate_sha256=`081a50a5ca9fcc36ff4e894283993a9ddc9022c1ed83201faf6560dd8cc5dfda`, new_chars=186.

```text
r0=player. Call scan_trap_zone_for_equip_activation_by_card(1-player, CID 0x1322) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

### 0x0809efd0 scan_trap_zone_for_equip_activation_brain_jacker

ID=6841, old_plate_sha256=`da2fc9d1bdd083a04fb05fb4c69093e365f59b891dd74577565d00b05f8d520e`, new_chars=186.

```text
r0=player. Call scan_trap_zone_for_equip_activation_by_card(1-player, CID 0x1877) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

### 0x0809efe8 scan_trap_zone_for_equip_activation_falling_down

ID=6842, old_plate_sha256=`3315434495b6bb765ce8f7c4d05b3f56e80e708bb18a90e88eb1da21acdd5551`, new_chars=186.

```text
r0=player. Call scan_trap_zone_for_equip_activation_by_card(1-player, CID 0x169a) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

### 0x0809f000 scan_trap_zone_for_equip_activation_the_eye_of_truth

ID=6843, old_plate_sha256=`7a58ecc3c6cab94b89edb6f9f1bb583d2af57d27fade6b4f1c3d5eec8cb08dec`, new_chars=186.

```text
r0=player. Call scan_trap_zone_for_equip_activation_by_card(1-player, CID 0x137b) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

### 0x0809f018 scan_trap_zone_for_equip_activation_minor_goblin_official

ID=6844, old_plate_sha256=`d73fc492a2ca129330b50fd3b1f817771e9cd7b7579f8ac6315d05e06547da4b`, new_chars=186.

```text
r0=player. Call scan_trap_zone_for_equip_activation_by_card(1-player, CID 0x1355) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

### 0x0809f030 scan_trap_zone_for_equip_activation_blast_sphere

ID=6845, old_plate_sha256=`aaf55af73c49d3ba73062545d66ab6beafda5f9a6d1707e6e019d128e3adc857`, new_chars=186.

```text
r0=player. Call scan_trap_zone_for_equip_activation_by_card(1-player, CID 0x1286) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

### 0x0809f048 scan_trap_zone_for_equip_activation_adhesive_explosive

ID=6846, old_plate_sha256=`d6f0426ed487975fd6e4f658f41e15ed190cfa8f517d5d622996c1c2fc4ac638`, new_chars=186.

```text
r0=player. Call scan_trap_zone_for_equip_activation_by_card(1-player, CID 0x19bd) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

### 0x0809f060 scan_monster_zone_for_equip_activation_malice_ascendant

ID=6847, old_plate_sha256=`bb32ba3d10611182fec95dfcf2bbce70f152f81b978204e39ca474421b703d62`, new_chars=189.

```text
r0=player. Call scan_monster_zone_for_equip_activation_by_card(1-player, CID 0x19d0) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

### 0x0809f078 scan_trap_slots_for_kiseitai_equip_chain_sprite

ID=6848, old_plate_sha256=`0d75e3eed6894df5fd3a35357a5a1b8a530c77412995ced744e256f036a5d636`, new_chars=340.

```text
r0=player. Scan opponent slots cursor+5 for cursor 0..4 at LP+0x1d24. Require active Kiseitai, a non-0xffff equip pair, and pair lookup result 0xa. Enqueue opponent slot flags and submit opponent LP/shape sprites with (get_slot_field5_score(pair)+1)>>1. Advance cursor and return 0 on emission. Rejected slots advance; exhaustion returns 1.
```

### 0x0809f158 scan_player_card_array_for_equip_activation_by_cid

ID=6849, old_plate_sha256=`c8e55eaa97cc4b9bf59f65d8bcab32160d55bd970975fc01b56e344aca78b606`, new_chars=386.

```text
r0=player, r1=internal CID. Return 1 if zone-11 chain already contains the CID. Scan the player 4-byte card array at gP1HandSlotArray, count LP+0x14, stride 0x868; require matching low13 CID and clear bit21. Pack 0x044e0000, player and CID, and call activation with decoded flags. Return 0 on a nonzero helper result; return 1 when all entries fail. Does not use the shared scan cursor.
```

### 0x0809f1fc scan_player_card_array_for_equip_activation_sinister_serpent

ID=6864, old_plate_sha256=`a1e925d2765d2bc7ed0395bac36cf2528f0bc5269c74cf84b6d23ddc51b3a59c`, new_chars=191.

```text
r0=player. Call scan_player_card_array_for_equip_activation_by_cid(player, CID 0x1181) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

### 0x0809f20c scan_player_card_array_for_equip_activation_treeborn_frog

ID=6865, old_plate_sha256=`b17229fd93039bfbbd977d8a5ef65cc13444cec1dacdaa97c2031ecd235ad160`, new_chars=191.

```text
r0=player. Call scan_player_card_array_for_equip_activation_by_cid(player, CID 0x19cb) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

### 0x0809f21c scan_equip_zone_for_special_summon_activation_return_zombie

ID=6866, old_plate_sha256=`8b72c6e9d47edb9cf5dca044c45e38697202524993477f56ea5354e28ccce222`, new_chars=406.

```text
r0=player. Scan the player 4-byte card-word array, count LP+0x14, stride 0x868. Match Return Zombie with bit21 clear. Build a zeroed 0x18-byte local entry, set CID/player/decoded flags and the eligibility fields. Only check_card_special_summon_eligible_full(entry)==0 proceeds to packed activation with prefix 0x044e0000. Return 0 on a nonzero activation result; continue otherwise. Return 1 on exhaustion.
```

### 0x0809f348 scan_monster_zone_slots_for_equip_activation_mucus_yolk

ID=5583, old_plate_sha256=`28a117b12f9f6f5c86a0caffd72b85ccd2d0fac077cebb142ae91eefe46024c5`, new_chars=325.

```text
r0=player. Resume monster slots 0..4 with cursor at LP+0x1d24. Require active Mucus Yolk and a nonzero check_node_in_slot_chain(player,slot,CID,2). Enqueue entry flags and enqueue_sprite_attr_with_mode(player,slot,actual_entry_CID,3,1). Advance cursor and return 0 on emission; rejected slots advance. Return 1 on exhaustion.
```

### 0x0809f40c scan_monster_zone_for_equip_activation_legendary_fiend

ID=15809, old_plate_sha256=`9b8c0f218bb8a250a32363d8314a05324d819048d106d60807827f1b14a3dff1`, new_chars=187.

```text
r0=player. Call scan_monster_zone_for_equip_activation_by_card(player, CID 0x154d) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

### 0x0809f41c scan_monster_zone_for_equip_activation_exodia_necross

ID=6850, old_plate_sha256=`2d0e1891ec30c50e24d40ad27052ce86b065d05f3ab53564245017796096cfc8`, new_chars=187.

```text
r0=player. Call scan_monster_zone_for_equip_activation_by_card(player, CID 0x1645) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

### 0x0809f42c scan_monster_zone_for_equip_activation_amazoness_blowpiper

ID=6851, old_plate_sha256=`10a7688bf7262e50320a10a9170df663e82983b6fa5d2c0ecded9cabf91c0e67`, new_chars=187.

```text
r0=player. Call scan_monster_zone_for_equip_activation_by_card(player, CID 0x160e) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

### 0x0809f43c scan_monster_zone_for_equip_activation_agent_of_wisdom_mercury

ID=15810, old_plate_sha256=`cb02207948edded8d761659b6a996802e485a58c88378c97d50c10e8af6dd939`, new_chars=187.

```text
r0=player. Call scan_monster_zone_for_equip_activation_by_card(player, CID 0x1740) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

### 0x0809f44c scan_field_slots_for_lv_monster_equip_activation

ID=15811, old_plate_sha256=`dd7f089a701c6beddca126c691e639aa510e3600bc029a7d62315e387641df12`, new_chars=365.

```text
r0=player. Resume monster slots 0..4 with cursor at LP+0x1d24. Match CID in {0x1812,0x17d5,0x17d1,0x17d9,0x1817,0x1814,0x1822,0x185e} and require nonzero entry+8. Pack entry CID/player/slot and call activation with decoded flags, ignoring its result. Increment the same cursor via gDuelFieldSlots+0x1cf4 and return 0. Rejected entries advance; exhaustion returns 1.
```

### 0x0809f538 scan_equip_zone_for_entity_sprite_and_activation

ID=6815, old_plate_sha256=`00be46f96b3fe1f08171b4488656edf47a0636e518e1888a7d893bb14d0cab6c`, new_chars=310.

```text
r0=player, r1=internal CID. Query zone 11 for a matching entity; a negative result returns 1. Otherwise enqueue the chain-match sprite, build player bit OR 0x044e0000 OR CID low16, and call apply_equip_activation_with_id_lookup with the entity low16 and zero payload. Ignore the activation result and return 0.
```

### 0x0809f584 scan_equip_zone_for_equip_activation_revival_jam

ID=6852, old_plate_sha256=`07139ff57af277ddb1024537530973f2b983b8701b66cf37033758a34c2965e1`, new_chars=189.

```text
r0=player. Call scan_equip_zone_for_entity_sprite_and_activation(player, CID 0x13c7) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

### 0x0809f594 scan_equip_zone_for_equip_activation_vampire_lord

ID=6853, old_plate_sha256=`f73a34838911e2178fdad934ca95fe6dee2b1139c9d40f1a9c71ad301eacd356`, new_chars=189.

```text
r0=player. Call scan_equip_zone_for_entity_sprite_and_activation(player, CID 0x1522) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

### 0x0809f5a4 scan_equip_zone_for_equip_activation_sacred_phoenix

ID=6854, old_plate_sha256=`50fd24dc66293baeff7707f8f6127a9e38ef94c2cc93b26628677260bcf81d2f`, new_chars=189.

```text
r0=player. Call scan_equip_zone_for_entity_sprite_and_activation(player, CID 0x185c) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

### 0x0809f5b4 scan_equip_zone_for_entity_sprite_activation_curse_of_vampire

ID=6855, old_plate_sha256=`75a44e9baf8267990d86272e8063cba0c24d31f06003763eaded75874d17cfe3`, new_chars=189.

```text
r0=player. Call scan_equip_zone_for_entity_sprite_and_activation(player, CID 0x188f) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

### 0x0809f5c4 scan_equip_zone_for_entity_sprite_activation_curse_of_vampire_opponent

ID=6856, old_plate_sha256=`e3f9e8e419a75cc7a93e2787c20bb8cad89c656e62f093eccae361648027ea90`, new_chars=191.

```text
r0=player. Call scan_equip_zone_for_entity_sprite_and_activation(1-player, CID 0x188f) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

### 0x0809f5dc scan_spell_trap_zone_for_equip_activation_via_packed_attr

ID=6816, old_plate_sha256=`9226b668707aca191a6c7779ef40a721c82498add6b5a50891f8f3180b3f1878`, new_chars=367.

```text
r0=player, r1=internal CID. Cursor LP+0x1d24==0 starts a scan at slot 5 through 9. On successful packed activation, set the LP row and return 0 without advancing that slot. Exhaustion returns 1 with cursor 10. On entry with nonzero cursor, zero u16 at LP+0x1da8 returns 1 unchanged; nonzero submits that cursor slot as packed sprite data, clears cursor and returns 0.
```

### 0x0809f704 scan_spell_trap_zone_for_equip_activation_reserved_icid_e

ID=15812, old_plate_sha256=`b01b8075a79da1ed4dd7063be9dc6be875d8a1daa1416be7db74ea952e8da052`, new_chars=200.

```text
r0=player. Call scan_spell_trap_zone_for_equip_activation_via_packed_attr(1-player, CID 0x1367) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

### 0x0809f71c scan_spell_trap_zone_for_equip_activation_recycle

ID=6857, old_plate_sha256=`f4c19800ecb9064acbe734fd0d1824f3b96fa1ca2ce583f44a7115eaa3f3a798`, new_chars=198.

```text
r0=player. Call scan_spell_trap_zone_for_equip_activation_via_packed_attr(player, CID 0x16d5) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

### 0x0809f72c scan_monster_zone_for_equip_activation_aqua_spirit_opponent

ID=6858, old_plate_sha256=`f97cec033cf7d252e1770befc97c53a8bef7188049bca25678b2bbed81864874`, new_chars=189.

```text
r0=player. Call scan_monster_zone_for_equip_activation_by_card(1-player, CID 0x1485) with an ordinary BL and return its result unchanged. The callee owns scan state and sprite side effects.
```

## C13 完整覆盖与落地守卫

- 段外既有代码/ROM数据/常量仅允许本提案明确的NEW constants与rename registry/CSV/inventory同步;不分析Seg3,不改音频样本和后续表.
- 原126自动word+7匿名tableword+25新pool=158,各槽只出现一次EQ/REF/RENAME;块头DAT由case0静态label取代. 非case Function入口不新增标签别名.
- 落地前比较完整root快照. 25newpool和145新instruction覆盖区必须仍无DefinedData/Instruction;8case动态LABEL及原table incoming一致;不可clearListing整个424B后丢失非目标对象.
- 原54B dispatcher指令/body两个range/原flow/原引用逐条保持,新增仅plan列出的指令、literal READ、branch、13CALL和8case数据目标. Body实际设为370B精确union. 不准因auto-analysis新建Function或触及池/对齐.
- 四padding必须仍各两undefined1,不创建Data2;25pool类型/dword长度4;158所有word原字节与ROM一致,case指针even不变;所有旧被保留引用逐字段核验.
- 四个FUNC_RENAME逐地址守卫Function ID 6829/6849/6864/6865、body bytes/ranges、prototype、incoming、原EOL及原PLATE前态; dispatcher以外Function body均不变, 全局Function总数仍5209.
- 段外odd指针按root-f13-seg2-odd-pointers-before.json逐字段守卫: 09e477c0的/undefined * length4与DATA/DEFAULT operand0 primary ref本体完全不变, 只允许target_primary显示名派生变化; 09e4788c/90的raw值保持且继续无DefinedData/symbol/ref, 不可新建Data或引用.
- ModeB后仅在正式生产asm/CSV/registry/四inventory和本批审定PLATE范围检查四个旧Function名为0; expected_old_*、冻结输入、review证据与历史记录保持. CSV仅4个name单元格, registry仅4个name+plate tuple, inventory仅4个name与dispatcher 54->370 metadata差异.
- Ghidra新plate/EOL及constant注释ASCII,59plate<=500. 全量export/inject_modes/split后验证段内自动DAT/DWORD/PTR/UNK定义为0,无未登记ROM_INCBIN/.byte;既有LAB标签可保留.
- fixer在review通过后负责完整export/build/byte-identical与保存后只读检查. executor这里只做静态ROM覆盖与值检查,不将其声称为build成功.
- 不stage/commit. 模块/DB任一前态偏离guard时停止写入并报告,不回滚他人未提交改动.

## 自检与复跑入口

运行目录统一为 `output/refine-run-20260831-194634/`. 首轮自检入口与结果保持为冻结历史; 本次ModeA可复跑入口为`python output/refine-run-20260831-194634/f13-seg2-modea1-check.py`, 输出exact-diff与新版selfcheck. 新版selfcheck逐项区分原80项中本轮实际重跑与依赖未变哈希复用, 不声称重新执行headless或build. 静态投影只用于review,没有作为正式asm提交或编译.

## 求助

无未闭合语义决策. 1338/1367的缺映射采用有ROM证据的中性CID名称,不猜卡名;LP/card-array历史全局名原样复用. 提案交独立reviewer,不在此自评PASS或评分.

## Executor Report: F13-Seg-2
- 槽: EQ=119 REF=20 RENAME=19 FUNC_RENAME=4 PLATE=59.
- disasm=1 range,145 instructions,316B; new pools=25/100B; padding=4/8B; carve=0; §5.1=0.
- 新增constants=24;复用唯一constants=48;数据目标ROM标签=9 (含1个与槽名重合的表头);无新增RAMglobal/Function.
- proposal: doc/dev/refine/F13-Seg-2.proposal.md; 求助: none.
