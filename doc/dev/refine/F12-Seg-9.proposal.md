# Refine Proposal: F12-Seg-9 [0x0809b178..0x0809c3d8)

严格限定 `asm/12_equip_activation_scan.s` 本段, 以 Seg-8 落地后的当前文本和 `roms/2343.gba` 为准. 不预析 Seg-10. executor 仅写本提案及运行目录 seg9-* 证据, 不改 Ghidra/asm/constants/工具/进度, 不 build/stage/commit.

## 段测绘

| 入口 | 函数现名 | 模块行 | 直接 BL 站点 / ROM Thumb 指针 |
|---|---|---|---|
| 0x0809b178 | update_equip_activation_display_state | 15021 | 0 / 1 |
| 0x0809b7e0 | update_equip_zone_sprite_by_state | 15869 | 0 / 1 |
| 0x0809bdfc | scan_equip_chain_slots_for_attr_enqueue | 16662 | 0 / 1 |
| 0x0809be70 | advance_equip_display_phase_via_table | 16724 | 3 / 0 |
| 0x0809bebc | tick_equip_phase_display_by_state | 16773 | 0 / 0 |
| 0x0809bf60 | check_field_allows_new_equip_action | 16863 | 1 / 0 |
| 0x0809bfd4 | dispatch_equip_action_sprite_by_phase_state | 16923 | 0 / 1 |

- 7 个主函数, 0 个另立共享收尾函数. 内部返回块 0x0809b7c6/0x0809bde6/0x0809c3ca 都使用所在主入口建立的栈帧, 不创建独立 leaf/参数签名.
- 自动槽共 157: DAT_ x134, PTR_ x23 (21个 gP1LifePoints 池和2个switch池), DWORD_/UNK_ x0. 原134初计漏23个PTR. 逐槽旧名、值、全部ldr位置见 `seg9-plan.json` 的 slots; 三张执行表恰好唯一覆盖157槽.
- 本段4704字节: 2043个带地址项共4648字节, 另有28处 `.zero` 共56字节. 3952指令字节 + 696字节 `.word` (157槽+17表项) +56对齐字节, 连续无缺口/重叠, 逐项ROM核对相同. 最后0x0809c3d6的2字节对齐也计入.
- 128个 `.hword` 均为已表示的Thumb指令, 包括两条 `MOV pc,r0` (0x4687). ROM_INCBIN x0, .byte x0, 无其他未分类裸字节块. 旧覆盖为空, 本段7条旧plate均整段重写.

## 数据块分类 (Rule 2/3)

| 块/入口 | 全ROM raw / THUMB+1 | 判定与证据 |
|---|---|---|
| ROM_INCBIN/.byte候选 | 空集合 | 全段扫描为空; `seg9-map-check.json` bare_blocks=[]; 不产生carve/disasm/5.1 |
| 0x0809b814 size 0x24 | 1 / 0 | 已结构化9项switch表; 唯一raw引用池0x0809b810; MOV pc,r0 @0x0809b806保持Thumb状态, 表项为偶地址 |
| 0x0809c038 size 0x20 | 1 / 0 | 已结构化8项switch表; 唯一raw引用池0x0809c034; MOV pc,r0 @0x0809c020保持Thumb状态, 表项为偶地址 |
| 0x09e5aaec size 0x3c | 1 / 0 | 本段外ROM函数表, raw引用仅0x0809bea4; 14个Thumb指针+NULL. 本段仅符号化其base引用, 不扩展本段carve范围 |
| 0x0809b178 主入口 | 0 / 1 | 已反汇编, 保持入口与边界; 0x09e5ab18 |
| 0x0809b7e0 主入口 | 0 / 1 | 已反汇编, 保持入口与边界; 0x09e5ab1c |
| 0x0809bdfc 主入口 | 0 / 1 | 已反汇编, 保持入口与边界; 0x09e5ab20 |
| 0x0809be70 主入口 | 0 / 0 | 已反汇编, 保持入口与边界; 直接BL x3 |
| 0x0809bebc 主入口 | 0 / 0 | 已反汇编, 保持入口与边界; 已命名函数, 无扫描到的直接BL/原始指针 |
| 0x0809bf60 主入口 | 0 / 0 | 已反汇编, 保持入口与边界; 直接BL x1 |
| 0x0809bfd4 主入口 | 0 / 1 | 已反汇编, 保持入口与边界; 0x09e5aac4 |
| 内部返回块0x0809b7c6/0x0809bde6/0x0809c3ca | 各0 / 0 | 本函数B/自然续接到达; 使用原栈帧, 不因没有raw指针而登记5.1 |

ref-scan对整个ROM逐字节查找little-endian u32, 分开扫描addr与addr|1, 位置完整保存在 `seg9-map-check.json`. 两张switch的17个case目标各raw=1/thumb=0, 唯一raw位置为对应表项, 没有压缩资产偶合命中. 表项如下, 不新增+1或改值:

```text
(0x0809b814, 0x0809b838)
(0x0809b818, 0x0809b850)
(0x0809b81c, 0x0809b9e0)
(0x0809b820, 0x0809ba30)
(0x0809b824, 0x0809baa8)
(0x0809b828, 0x0809baf8)
(0x0809b82c, 0x0809bb60)
(0x0809b830, 0x0809bc04)
(0x0809b834, 0x0809bca4)
```

```text
(0x0809c038, 0x0809c058)
(0x0809c03c, 0x0809c108)
(0x0809c040, 0x0809c1ac)
(0x0809c044, 0x0809c1f4)
(0x0809c048, 0x0809c2d0)
(0x0809c04c, 0x0809c338)
(0x0809c050, 0x0809c38c)
(0x0809c054, 0x0809c3a8)
```

外段分发表的边界由14项后NULL及消费者判NULL共同确认. 这里只读取既有入口标签识别表项, 未展开段外函数体. 下表是ROM证据, 不是carve计划:

| 索引 | 表项地址 | ROM原值 | 既有函数名 |
|---|---|---|---|
| 0 | 0x09e5aaec | 0x080977a1 | enqueue_frozen_soul_zone_sprite_or_default |
| 1 | 0x09e5aaf0 | 0x08097829 | dispatch_equip_activation_state_by_substate |
| 2 | 0x09e5aaf4 | 0x08097c2d | dispatch_equip_slot_display_state_by_phase |
| 3 | 0x09e5aaf8 | 0x08098265 | tick_activation_display_state_machine |
| 4 | 0x09e5aafc | 0x080984d1 | activate_effect_zone_display_for_slot |
| 5 | 0x09e5ab00 | 0x08098565 | tick_card_activation_phase_by_state |
| 6 | 0x09e5ab04 | 0x08098a89 | tick_equip_zone_activation_display_state |
| 7 | 0x09e5ab08 | 0x08099315 | dispatch_equip_field_phase_handler |
| 8 | 0x09e5ab0c | 0x08099aad | run_equip_slot_display_update_state_machine |
| 9 | 0x09e5ab10 | 0x08099e0d | run_equip_spell_display_state_machine |
| 10 | 0x09e5ab14 | 0x0809a1a5 | eval_equip_slot_pair_eligibility |
| 11 | 0x09e5ab18 | 0x0809b179 | update_equip_activation_display_state |
| 12 | 0x09e5ab1c | 0x0809b7e1 | update_equip_zone_sprite_by_state |
| 13 | 0x09e5ab20 | 0x0809bdfd | scan_equip_chain_slots_for_attr_enqueue |
| 14 | 0x09e5ab24 | 0x00000000 | NULL |

## 符号化计划 (R1/R2/R3)

三类槽各自独占, 顺序均按地址递增. base与offset分槽保留, 不折叠绝对地址. EQ使用data-equate operand0和槽的USER_DEFINED主标签; REF按下述LABEL主符号+DATA/USER_DEFINED落地; RENAME保留已存在的表达式和引用.

### EQ_SLOTS (data-equate)

104槽. 格式 `(slot, value, const_name, slot_label)`; NEW/REUSE由后文逐符号目录指定.

```text
(0x0809b240, 0x00000868, PLAYER_BLOCK_STRIDE, equip_display_state_player_stride_9b240)
(0x0809b24c, 0x00001cf8, EQUIP_CHAIN_STEP_FROM_FIELD_OFF, equip_display_state_chain_step_from_field_offset_9b24c)
(0x0809b338, 0x000014d6, SPEAR_DRAGON_CID, equip_display_state_spear_dragon_cid_9b338)
(0x0809b33c, 0x00001993, AXE_DRAGONUTE_CID, equip_display_state_axe_dragonute_cid_9b33c)
(0x0809b344, 0x000018cd, KAMINOTE_BLOW_CID, equip_display_state_kaminote_blow_cid_9b344)
(0x0809b348, 0x00001866, KANGAROO_CHAMP_CID, equip_display_state_kangaroo_champ_cid_9b348)
(0x0809b34c, 0x0000170e, RYU_KOKKI_CID, equip_display_state_ryu_kokki_cid_9b34c)
(0x0809b354, 0x00001837, BIG_CORE_CID, equip_display_state_big_core_cid_9b354)
(0x0809b370, 0x000019a6, EHERO_NEO_BUBBLEMAN_CID, equip_display_state_ehero_neo_bubbleman_cid_9b370)
(0x0809b384, 0x000019bf, BES_COVERED_CORE_CID, equip_display_state_bes_covered_core_cid_9b384)
(0x0809b468, 0x00000868, PLAYER_BLOCK_STRIDE, equip_display_state_player_stride_9b468)
(0x0809b508, 0x00001837, BIG_CORE_CID, equip_display_state_big_core_cid_9b508)
(0x0809b50c, 0x00001703, PRICKLE_FAIRY_CID, equip_display_state_prickle_fairy_cid_9b50c)
(0x0809b510, 0x0000129c, BIG_SHIELD_GARDNA_CID, equip_display_state_big_shield_gardna_cid_9b510)
(0x0809b528, 0x0000170d, GETSU_FUHMA_CID, equip_display_state_getsu_fuhma_cid_9b528)
(0x0809b544, 0x00001962, BES_TETRAN_CID, equip_display_state_bes_tetran_cid_9b544)
(0x0809b55c, 0x000019bf, BES_COVERED_CORE_CID, equip_display_state_bes_covered_core_cid_9b55c)
(0x0809b56c, 0x000019c7, CHAINSAW_INSECT_CID, equip_display_state_chainsaw_insect_cid_9b56c)
(0x0809b680, 0x00000868, PLAYER_BLOCK_STRIDE, equip_display_state_player_stride_9b680)
(0x0809b704, 0x00001d2c, EQUIP_CHAIN_ACTIVE_OFF, equip_display_state_chain_active_from_lp_offset_9b704)
(0x0809b734, 0x00001cf8, EQUIP_CHAIN_STEP_FROM_FIELD_OFF, equip_display_state_chain_step_from_field_offset_9b734)
(0x0809b7ac, 0x000016cb, BLACK_LUSTER_SOLDIER_ENVOY_CID, equip_display_state_black_luster_soldier_envoy_cid_9b7ac)
(0x0809b7b0, 0x00001cf8, EQUIP_CHAIN_STEP_FROM_FIELD_OFF, equip_display_state_chain_step_from_field_offset_9b7b0)
(0x0809b7dc, 0x00001d2c, EQUIP_CHAIN_ACTIVE_OFF, equip_display_state_chain_active_from_lp_offset_9b7dc)
(0x0809b80c, 0x00001d2c, EQUIP_CHAIN_ACTIVE_OFF, equip_zone_state_chain_active_from_lp_offset_9b80c)
(0x0809b84c, 0x00001d2c, EQUIP_CHAIN_ACTIVE_OFF, equip_zone_state_chain_active_from_lp_offset_9b84c)
(0x0809b8b8, 0x00001ce8, P1LP_BLOCK2_OFF_1CE8, equip_zone_state_current_player_from_lp_offset_9b8b8)
(0x0809b8bc, 0x00000868, PLAYER_BLOCK_STRIDE, equip_zone_state_player_stride_9b8bc)
(0x0809b8c4, 0x000015d2, GIANT_ORC_CID, equip_zone_state_giant_orc_cid_9b8c4)
(0x0809b8cc, 0x00001566, TOON_GOBLIN_AF_CID, equip_zone_state_toon_goblin_af_cid_9b8cc)
(0x0809b8e4, 0x00001915, INDOMITABLE_FIGHTER_LEI_LEI_CID, equip_zone_state_indomitable_fighter_lei_lei_cid_9b8e4)
(0x0809b8f0, 0x00001983, MYTHICAL_BEAST_CERBERUS_CID, equip_zone_state_mythical_beast_cerberus_cid_9b8f0)
(0x0809b954, 0x000014d6, SPEAR_DRAGON_CID, equip_zone_state_spear_dragon_cid_9b954)
(0x0809b95c, 0x00001419, GOBLIN_ATTACK_FORCE_CID, equip_zone_state_goblin_attack_force_cid_9b95c)
(0x0809ba24, 0x00001ce8, P1LP_BLOCK2_OFF_1CE8, equip_zone_state_current_player_from_lp_offset_9ba24)
(0x0809ba28, 0x00001392, SWORD_OF_DRAGONS_SOUL_CID, equip_zone_state_sword_of_dragons_soul_cid_9ba28)
(0x0809ba9c, 0x000012a6, SWORD_HUNTER_CID, equip_zone_state_sword_hunter_cid_9ba9c)
(0x0809baa4, 0x00001d2c, EQUIP_CHAIN_ACTIVE_OFF, equip_zone_state_chain_active_from_lp_offset_9baa4)
(0x0809bad8, 0x00001415, RED_MOON_BABY_CID, equip_zone_state_red_moon_baby_cid_9bad8)
(0x0809badc, 0x00501415, RED_MOON_BABY_ACTIVATION_PACKED, equip_zone_state_red_moon_baby_activation_packed_9badc)
(0x0809baf4, 0x00001d2c, EQUIP_CHAIN_ACTIVE_OFF, equip_zone_state_chain_active_from_lp_offset_9baf4)
(0x0809bb4c, 0x00001ce8, P1LP_BLOCK2_OFF_1CE8, equip_zone_state_current_player_from_lp_offset_9bb4c)
(0x0809bb50, 0x00000868, PLAYER_BLOCK_STRIDE, equip_zone_state_player_stride_9bb50)
(0x0809bb58, 0x000012e2, MAGIC_ARM_SHIELD_CID, equip_zone_state_magic_arm_shield_cid_9bb58)
(0x0809bb5c, 0x00001cfc, EQUIP_CHAIN_ACTIVE_FROM_FIELD_OFF, equip_zone_state_chain_active_from_field_offset_9bb5c)
(0x0809bbe8, 0x00000868, PLAYER_BLOCK_STRIDE, equip_zone_state_player_stride_9bbe8)
(0x0809bbf0, 0x00001362, MAGICAL_HATS_CID, equip_zone_state_magical_hats_cid_9bbf0)
(0x0809bc00, 0x00001d2c, EQUIP_CHAIN_ACTIVE_OFF, equip_zone_state_chain_active_from_lp_offset_9bc00)
(0x0809bc8c, 0x00001512, AFTER_THE_STRUGGLE_CID, equip_zone_state_after_the_struggle_cid_9bc8c)
(0x0809bc94, 0x00000868, PLAYER_BLOCK_STRIDE, equip_zone_state_player_stride_9bc94)
(0x0809bca0, 0x00001d2c, EQUIP_CHAIN_ACTIVE_OFF, equip_zone_state_chain_active_from_lp_offset_9bca0)
(0x0809bd1c, 0x00000868, PLAYER_BLOCK_STRIDE, equip_zone_state_player_stride_9bd1c)
(0x0809bd20, 0x004e1571, HELPOEMER_ACTIVATION_PACKED, equip_zone_state_helpoemer_activation_packed_9bd20)
(0x0809bd28, 0xab880000, HELPOEMER_CID_SHIFTED, equip_zone_state_helpoemer_cid_shifted_9bd28)
(0x0809bd2c, 0xfffffbfc, HAND_ARRAY_TO_COUNT_NEG_OFF, equip_zone_state_card_array_to_count_neg_offset_9bd2c)
(0x0809bd30, 0x00001d2c, EQUIP_CHAIN_ACTIVE_OFF, equip_zone_state_chain_active_from_lp_offset_9bd30)
(0x0809bd54, 0x00001469, THE_DARK_DOOR_CID, equip_zone_state_the_dark_door_cid_9bd54)
(0x0809bd58, 0x000011ed, eval_gap_cid_11ed, equip_zone_state_eval_gap_cid_11ed_9bd58)
(0x0809bdc4, 0x00000868, PLAYER_BLOCK_STRIDE, equip_zone_state_player_stride_9bdc4)
(0x0809bdcc, 0x000012a6, SWORD_HUNTER_CID, equip_zone_state_sword_hunter_cid_9bdcc)
(0x0809bdf8, 0x00001d28, EQUIP_CHAIN_STEP_OFF, equip_zone_state_chain_step_from_lp_offset_9bdf8)
(0x0809be64, 0x00000868, PLAYER_BLOCK_STRIDE, scan_chain_attr_player_stride_9be64)
(0x0809be6c, 0x9fc80000, FAIRY_BOX_CID_SHIFTED, scan_chain_attr_fairy_box_cid_shifted_9be6c)
(0x0809beac, 0x00001d28, EQUIP_CHAIN_STEP_OFF, advance_equip_step_chain_step_from_lp_offset_9beac)
(0x0809beb0, 0x00001d2c, EQUIP_CHAIN_ACTIVE_OFF, advance_equip_step_chain_active_from_lp_offset_9beb0)
(0x0809bed8, 0x00001d94, EQUIP_PHASE_DISPLAY_STATE_OFF, tick_equip_phase_outer_state_from_lp_offset_9bed8)
(0x0809bf24, 0x00001d28, EQUIP_CHAIN_STEP_OFF, tick_equip_phase_chain_step_from_lp_offset_9bf24)
(0x0809bf28, 0x00001d2c, EQUIP_CHAIN_ACTIVE_OFF, tick_equip_phase_chain_active_from_lp_offset_9bf28)
(0x0809bf30, 0x0000801b, OAM_EQUIP_SPRITE_TILE_P2_1B, tick_equip_phase_oam_equip_sprite_tile_p2_1b_9bf30)
(0x0809bf38, 0x00001d94, EQUIP_PHASE_DISPLAY_STATE_OFF, tick_equip_phase_outer_state_from_lp_offset_9bf38)
(0x0809bf54, 0x00001d28, EQUIP_CHAIN_STEP_OFF, tick_equip_phase_chain_step_from_lp_offset_9bf54)
(0x0809bfc0, 0x000014ff, YATA_GARASU_CID, check_new_equip_yata_garasu_cid_9bfc0)
(0x0809bfc8, 0x00000868, PLAYER_BLOCK_STRIDE, check_new_equip_player_stride_9bfc8)
(0x0809c028, 0x00001ce8, P1LP_BLOCK2_OFF_1CE8, dispatch_equip_action_current_player_from_lp_offset_9c028)
(0x0809c02c, 0x00000868, PLAYER_BLOCK_STRIDE, dispatch_equip_action_player_stride_9c02c)
(0x0809c030, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, dispatch_equip_action_card_play_phase_from_lp_offset_9c030)
(0x0809c0a0, 0x000014ff, YATA_GARASU_CID, dispatch_equip_action_yata_garasu_cid_9c0a0)
(0x0809c0a4, 0x00001548, RECKLESS_GREED_CID, dispatch_equip_action_reckless_greed_cid_9c0a4)
(0x0809c0ac, 0x00008023, SPRITE_ATTR_DUEL_PHASE_P2_B, dispatch_equip_action_sprite_attr_duel_phase_p2_b_9c0ac)
(0x0809c0d4, 0x00000133, TRIGGER_OP_PARAM_133, dispatch_equip_action_trigger_op_param_133_9c0d4)
(0x0809c100, 0x0000800c, SPRITE_ATTR_DUEL_PHASE_P2_0C, dispatch_equip_action_sprite_attr_duel_phase_p2_0c_9c100)
(0x0809c104, 0x00008028, OAM_ZONE_SPRITE_PAIR_P2_FIRST, dispatch_equip_action_oam_zone_sprite_pair_p2_first_9c104)
(0x0809c19c, 0x00000868, PLAYER_BLOCK_STRIDE, dispatch_equip_action_player_stride_9c19c)
(0x0809c1a0, 0x00001911, CYBER_ARCHFIEND_CID, dispatch_equip_action_cyber_archfiend_cid_9c1a0)
(0x0809c1a8, 0x00001504, HINO_KAGU_TSUCHI_CID, dispatch_equip_action_hino_kagu_tsuchi_cid_9c1a8)
(0x0809c1e0, 0x000014fd, MAHARAGHI_CID, dispatch_equip_action_maharaghi_cid_9c1e0)
(0x0809c1e4, 0x025014fd, MAHARAGHI_ACTIVATION_PACKED, dispatch_equip_action_maharaghi_activation_packed_9c1e4)
(0x0809c2b4, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, dispatch_equip_action_card_play_phase_from_lp_offset_9c2b4)
(0x0809c2b8, 0x00000868, PLAYER_BLOCK_STRIDE, dispatch_equip_action_player_stride_9c2b8)
(0x0809c2bc, 0x000014c4, FREED_THE_MATCHLESS_GENERAL_CID, dispatch_equip_action_freed_the_matchless_general_cid_9c2bc)
(0x0809c2c8, 0xcc200000, MAGICAL_BLAST_CID_SHIFTED, dispatch_equip_action_magical_blast_cid_shifted_9c2c8)
(0x0809c2cc, 0x004e1984, MAGICAL_BLAST_ACTIVATION_PACKED, dispatch_equip_action_magical_blast_activation_packed_9c2cc)
(0x0809c2ec, 0x000014c4, FREED_THE_MATCHLESS_GENERAL_CID, dispatch_equip_action_freed_the_matchless_general_cid_9c2ec)
(0x0809c2f4, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, dispatch_equip_action_card_play_phase_from_lp_offset_9c2f4)
(0x0809c31c, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, dispatch_equip_action_card_play_phase_from_lp_offset_9c31c)
(0x0809c334, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, dispatch_equip_action_card_play_phase_from_lp_offset_9c334)
(0x0809c354, 0x00001d54, ELIGIB_STATE_CTRL_OFF, dispatch_equip_action_eligibility_state_from_lp_offset_9c354)
(0x0809c358, 0x00001d5c, ELIGIB_ACT_TYPE_OFF, dispatch_equip_action_eligibility_type_from_lp_offset_9c358)
(0x0809c35c, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, dispatch_equip_action_card_play_phase_from_lp_offset_9c35c)
(0x0809c374, 0x00001d58, ELIGIB_ACT_COUNT_OFF, dispatch_equip_action_eligibility_count_from_lp_offset_9c374)
(0x0809c378, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, dispatch_equip_action_card_play_phase_from_lp_offset_9c378)
(0x0809c388, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, dispatch_equip_action_card_play_phase_from_lp_offset_9c388)
(0x0809c3a4, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, dispatch_equip_action_card_play_phase_from_lp_offset_9c3a4)
(0x0809c3c4, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, dispatch_equip_action_card_play_phase_from_lp_offset_9c3c4)
```

### REF_SLOTS (USER-label + DATA-ref)

32槽. 格式 `(slot, target, gas_label, slot_label)`; NEW/REUSE由后文逐符号目录指定.

```text
(0x0809b23c, 0x0201bb90, gEquipChainSlotRefs, equip_display_state_chain_base_9b23c)
(0x0809b244, 0x0201c510, gDuelFieldSlots, equip_display_state_field_base_9b244)
(0x0809b248, 0x0201e20c, gEquipChainActivePhase, equip_display_state_active_phase_ptr_9b248)
(0x0809b340, 0x0201bb90, gEquipChainSlotRefs, equip_display_state_chain_base_9b340)
(0x0809b3d8, 0x0201bb90, gEquipChainSlotRefs, equip_display_state_chain_base_9b3d8)
(0x0809b464, 0x0201bb90, gEquipChainSlotRefs, equip_display_state_chain_base_9b464)
(0x0809b46c, 0x0201c510, gDuelFieldSlots, equip_display_state_field_base_9b46c)
(0x0809b4b8, 0x0201bb90, gEquipChainSlotRefs, equip_display_state_chain_base_9b4b8)
(0x0809b504, 0x0201bb90, gEquipChainSlotRefs, equip_display_state_chain_base_9b504)
(0x0809b684, 0x0201c510, gDuelFieldSlots, equip_display_state_field_base_9b684)
(0x0809b6dc, 0x0201bb90, gEquipChainSlotRefs, equip_display_state_chain_base_9b6dc)
(0x0809b738, 0x0201e20c, gEquipChainActivePhase, equip_display_state_active_phase_ptr_9b738)
(0x0809b7b4, 0x0201e20c, gEquipChainActivePhase, equip_display_state_active_phase_ptr_9b7b4)
(0x0809b810, 0x0809b814, switchD_0809b806__switchdataD_0809b814, equip_zone_state_switch_table_9b810)
(0x0809b8c0, 0x0201c510, gDuelFieldSlots, equip_zone_state_field_base_9b8c0)
(0x0809b958, 0x0201c510, gDuelFieldSlots, equip_zone_state_field_base_9b958)
(0x0809bb54, 0x0201c510, gDuelFieldSlots, equip_zone_state_field_base_9bb54)
(0x0809bbe4, 0x0201e1c8, gEquipZoneCountTable, equip_zone_state_current_player_ptr_9bbe4)
(0x0809bbec, 0x0201c510, gDuelFieldSlots, equip_zone_state_field_base_9bbec)
(0x0809bc90, 0x0201e1c8, gEquipZoneCountTable, equip_zone_state_current_player_ptr_9bc90)
(0x0809bc98, 0x0201c510, gDuelFieldSlots, equip_zone_state_field_base_9bc98)
(0x0809bd24, 0x0201c8f8, gP1HandSlotArray, equip_zone_state_card_word_array_base_9bd24)
(0x0809bdc8, 0x0201c510, gDuelFieldSlots, equip_zone_state_field_base_9bdc8)
(0x0809be68, 0x0201c510, gDuelFieldSlots, scan_chain_attr_field_base_9be68)
(0x0809bea4, 0x09e5aaec, equip_display_step_fn_table, advance_equip_step_handler_table_9bea4)
(0x0809bf2c, 0x0201bb90, gEquipChainSlotRefs, tick_equip_phase_chain_base_9bf2c)
(0x0809c034, 0x0809c038, switchD_0809c020__switchdataD_0809c038, dispatch_equip_action_switch_table_9c034)
(0x0809c0a8, 0x0201e2a0, gDuelCardCtxBase, dispatch_equip_action_display_ctx_base_9c0a8)
(0x0809c1a4, 0x0201c4ec, gP1ZoneHandCount, dispatch_equip_action_zone_count_base_9c1a4)
(0x0809c2c0, 0x0201c510, gDuelFieldSlots, dispatch_equip_action_field_base_9c2c0)
(0x0809c2c4, 0x0201c8f8, gP1HandSlotArray, dispatch_equip_action_card_word_array_base_9c2c4)
(0x0809c314, 0x0201e2a0, gDuelCardCtxBase, dispatch_equip_action_display_ctx_base_9c314)
```

REF实际导出约束:

- 所有目标必须以表列 `gas_label` 为 USER_DEFINED LABEL 主符号; operand0为 DATA/USER_DEFINED 主引用. RAM地址均用已有`.equ`, 新RAM全局和新ROM表base在NEW目录给绝对equate, 使GAS可解析其值.
- 两switch已有LABEL对象: 0x0809b814 symbol id7217, full=`switchD_0809b806::switchdataD_0809b814`; 0x0809c038 id7144, full=`switchD_0809c020::switchdataD_0809c038`. 当前均ANALYSIS/primary. 必须复用同一对象, 将namespace/name规范为对应表列的完整GAS名并设USER_DEFINED/primary, 不能只改source/primary后让getName()保留短名. 不增同址别名、不改case标签或17表项.
- 上述两个池当前为operand0 DATA/DEFAULT. 本Ghidra版本仅重复addMemoryReference不会提升source. fixer需精确重建此operand0到目标的引用, 显式DATA/USER_DEFINED/primary, 保留其他operand与其他目标引用. 其余REF槽同样验证实际source, 不以调用成功代替检查.
- 0x09e5aaec当前primary为动态DEFAULT LABEL `PTR_enqueue_frozen_soul_zone_sprite_or_default+1_09e5aaec`, data=undefined*, 自身首项指向0x080977a1. 将该表base设为新USER_DEFINED LABEL `equip_display_step_fn_table`; 不改它内部首项或后续函数指针、不重命名函数. 仅本段池0x0809bea4建立指向表base的DATA/USER_DEFINED主引用.
- `tools/asm-regen/ghidra/ExportRangeToGas.py:506` resolve_word_symbol先检查引用目标primary的source, ROM只接受LABEL, 返回sanitize_label(sym.getName()); `:612` 对4字节先走symbol再走equate. 本段32个REF目标均为RAM或ROM数据LABEL, 没有FUNCTION目标. 不依赖fn+1文本导出, 不改全局exporter.
- 主线程只读类型观测见 `root-seg9-symbol-observation.log` (STATUS: READ_ONLY_OBSERVATION_COMPLETE). 表外函数指针仍保留ROM原奇数值, 此提案不会将其导为偶地址函数名.

### RENAME_SLOTS (纯改名 + EOL)

21槽. 格式 `(slot, slot_label, eol_ascii)`; NEW/REUSE由后文逐符号目录指定.

RENAME保留规则: 21池保持`.word gP1LifePoints`及现有operand0 DATA/DEFAULT主引用不动; 不新增、删除、重建或升级这21条引用source. USER_DEFINED属于目标`gP1LifePoints`主LABEL, 不代表引用source. 32个REF的DATA/USER_DEFINED创建或精确重建规则保持原样, 不套用于RENAME.

```text
(0x0809b700, equip_display_state_lp_base_9b700, "gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.")
(0x0809b7d8, equip_display_state_lp_base_9b7d8, "gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.")
(0x0809b808, equip_zone_state_lp_base_9b808, "gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.")
(0x0809b848, equip_zone_state_lp_base_9b848, "gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.")
(0x0809b9dc, equip_zone_state_lp_base_9b9dc, "gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.")
(0x0809ba2c, equip_zone_state_lp_base_9ba2c, "gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.")
(0x0809baa0, equip_zone_state_lp_base_9baa0, "gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.")
(0x0809baf0, equip_zone_state_lp_base_9baf0, "gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.")
(0x0809bbfc, equip_zone_state_lp_base_9bbfc, "gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.")
(0x0809bc9c, equip_zone_state_lp_base_9bc9c, "gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.")
(0x0809bea8, advance_equip_step_lp_base_9bea8, "gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.")
(0x0809bed4, tick_equip_phase_lp_base_9bed4, "gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.")
(0x0809bf34, tick_equip_phase_lp_base_9bf34, "gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.")
(0x0809bfc4, check_new_equip_lp_base_9bfc4, "gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.")
(0x0809c024, dispatch_equip_action_lp_base_9c024, "gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.")
(0x0809c2b0, dispatch_equip_action_lp_base_9c2b0, "gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.")
(0x0809c2f0, dispatch_equip_action_lp_base_9c2f0, "gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.")
(0x0809c318, dispatch_equip_action_lp_base_9c318, "gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.")
(0x0809c330, dispatch_equip_action_lp_base_9c330, "gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.")
(0x0809c3a0, dispatch_equip_action_lp_base_9c3a0, "gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.")
(0x0809c3c0, dispatch_equip_action_lp_base_9c3c0, "gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.")
```

### 额外 EOL (ASCII)

下列5条附着于已分类槽, 不构成额外槽操作分类:

```text
(0x0809bb5c, "Byte offset from gDuelFieldSlots to gEquipChainActivePhase; not DISP_SET_VARIANT_OFF from gP1LifePoints.")
(0x0809bbe4, "Current player selector word; gP1LifePoints+P1LP_BLOCK2_OFF_1CE8.")
(0x0809bc90, "Current player selector word; gP1LifePoints+P1LP_BLOCK2_OFF_1CE8.")
(0x0809bd24, "Card-word array at gP1LifePoints+0x418; count at +0x14; four-byte entries. Retain existing global name.")
(0x0809c2c4, "Card-word array at gP1LifePoints+0x418; count at +0x14; four-byte entries. Retain existing global name.")
```

### FUNC_RENAME

none. 7个既有名称分别覆盖状态更新、槽显示、链扫描、表驱动及布尔检查. 更精确的输入/返回/基址/扫描区间由plate订正, 不改FUNCTION主符号或函数范围, 不新增函数, 无CSV同步. 直接BL站点与表引用分开统计, 不把无raw指针当无控制流引用.

### PLATE (full rewrite, ASCII)

#### 0x0809b178 update_equip_activation_display_state (448 chars)

```text
r0=player_side. Uses the shared equip phase at gEquipChainActivePhase. Phase 0 checks paired slot contexts and card chains, queues card-specific activation/display work, then advances phase. Phase 1 queues code 0x1e; the phase-six gate selects step 12, while an eligible Black Luster Soldier chain selects step 2 and resets phase. Other phases set step 1 and reset phase. Step uses gDuelFieldSlots+EQUIP_CHAIN_STEP_FROM_FIELD_OFF. Always returns 0.
```

#### 0x0809b7e0 update_equip_zone_sprite_by_state (466 chars)

```text
r0=player_side, saved in r10. Dispatches shared EQUIP_CHAIN_ACTIVE_OFF states 0..8: row setup, card-specific field scans, Sword Hunter/Red-Moon Baby work, Magic-Arm Shield, Magical Hats, After the Struggle and an opposing Helpoemer array scan. Work paths return 0; selected paths advance phase or retry it. Default queues The Dark Door; absent CID 0x11ed returns 1, otherwise queues that CID and clears step/phase. Internal return tail at 0x0809bde6 uses this frame.
```

#### 0x0809bdfc scan_equip_chain_slots_for_attr_enqueue (402 chars)

```text
r0=player_side. Scan both players, field slots 5..9 (stride 0x14), comparing slot_word<<19 with FAIRY_BOX_CID_SHIFTED. Matching slots call enqueue_equip_chain_attrs_for_slot_range(player, slot). If check_activation_phase_counter_is_six returns 0, set caller player state bit 0x12 with sprite update. Always returns 1. Uses the field base and PLAYER_BLOCK_STRIDE; no mask test and no scan of slots 0..4.
```

#### 0x0809be70 advance_equip_display_phase_via_table (395 chars)

```text
r0=player_side. Index equip_display_step_fn_table by [gP1LifePoints+EQUIP_CHAIN_STEP_OFF], without a bounds check. A null entry returns 1. Otherwise invoke the Thumb handler with player_side; a nonzero result clears EQUIP_CHAIN_ACTIVE_OFF and increments the step. A zero result leaves both unchanged. Every non-null entry path returns 0. Table contains 14 handlers followed by a null terminator.
```

#### 0x0809bebc tick_equip_phase_display_by_state (436 chars)

```text
r0=player_side; r1=extra_flag. Outer state is [gP1LifePoints+EQUIP_PHASE_DISPLAY_STATE_OFF]. State 0 sets step=6 and active phase=1, updates occupancy, optionally queues sprite code 0x1b/0x801b from chain context, sets chain+0x14=1 and advances outer state; returns 0. State 1 calls advance_equip_display_phase_via_table, then returns whether the stored unsigned step exceeds 8; it does not test that call result. Other states return 0.
```

#### 0x0809bf60 check_field_allows_new_equip_action (371 chars)

```text
r0=player_side. Require a Yata-Garasu node in zone 0xb, zero player count at gP1LifePoints+player*PLAYER_BLOCK_STRIDE+0xc, no occupied monster zones, and no active equip slots. Then return 1 if the opposing player has a valid monster-pair slot or an available effect zone for Yata-Garasu; otherwise return 0. Pure checks; the +0xc word is a count, not an equip-lock flag.
```

#### 0x0809bfd4 dispatch_equip_action_sprite_by_phase_state (464 chars)

```text
Input registers unused. Read current player from gP1LifePoints+P1LP_BLOCK2_OFF_1CE8; dispatch CARD_PLAY_PHASE_CTR_OFF states 0..7. Handles draw-block display, Cyber Archfiend/Hino-Kagu-Tsuchi, Maharaghi, Freed/Magical Blast, display-context waits, zone pipeline and LP row update. Phase 2 can retry or fall through to phase 3. Returns 0 after work, phase updates or retries; returns 1 on blocked phase 0 or phase>7. Internal tail at 0x0809c3ca restores this frame.
```

## carve 计划 (R7)

none. 本段无ROM_INCBIN/.byte, 两switch已经是结构化word表. 0x09e5aaec是位于本段外的ROM全局base, 仅建立地址LABEL和同值equate, 不修改外段表内容或rom.s.

## disasm 计划 (R4)

none. 所有指令与池/对齐已完整表示; 无待逐stub反汇编的块. 两条0x4687保持MOV pc,r0及其偶地址case目标.

## 新增 constants / 全局及复用目录

已将 `constants/*.inc` 全部5966条`.equ/.set`递归求值, 成功5966, 未解析0. 包含十六进制、十进制、别名与表达式, 全量按value查询而非名称关键词. 证据 `seg9-constant-values-evaluated.json`. 14个NEW值均无既有同值定义; NEW名字也与constants/asm/data现有符号不冲突. 复用54个既有符号 (52个constants定义+2个switch LABEL). 不新建include文件.

### NEW

共12个数值常量+1个RAM全局+1个ROM表base. 全部值先读ROM;以下为准确新增定义:

`constants/card_info.inc`

```asm
.equ GOBLIN_ATTACK_FORCE_CID, 0x00001419  @ Goblin Attack Force; slot CID; card-stats.s card_0900; pw=78658564.
.equ RECKLESS_GREED_CID, 0x00001548  @ Reckless Greed; slot CID; card-stats.s card_1131; pw=37576645.
.equ AXE_DRAGONUTE_CID, 0x00001993  @ Axe Dragonute; slot CID; card-stats.s card_2010; pw=84914462.
.equ RED_MOON_BABY_ACTIVATION_PACKED, 0x00501415  @ Red-Moon Baby CID | 0x00500000; packed activation input before player bit31.
.equ HELPOEMER_ACTIVATION_PACKED, 0x004e1571  @ Helpoemer CID | 0x004e0000; packed activation input before player bit31.
.equ MAHARAGHI_ACTIVATION_PACKED, 0x025014fd  @ Maharaghi CID | 0x02500000; packed activation input before player bit31.
.equ MAGICAL_BLAST_ACTIVATION_PACKED, 0x004e1984  @ Magical Blast CID | 0x004e0000; packed activation input before player bit31.
.equ FAIRY_BOX_CID_SHIFTED, 0x9fc80000  @ FAIRY_BOX_CID << 19, truncated to u32; equality test after shifting a slot word.
.equ MAGICAL_BLAST_CID_SHIFTED, 0xcc200000  @ MAGICAL_BLAST_CID << 19, truncated to u32; equality test after shifting a slot word.
```

`constants/duel_field.inc`

```asm
.equ TRIGGER_OP_PARAM_133, 0x00000133  @ Second argument to trigger_card_display_op31_if_not_active; forwarded as dispatch op31 parameter.
.equ EQUIP_PHASE_DISPLAY_STATE_OFF, 0x00001d94  @ Byte offset from gP1LifePoints to the outer equip display state word; distinct from step and active phase.
```

`constants/oam_attr.inc`

```asm
.equ SPRITE_ATTR_DUEL_PHASE_P2_0C, 0x0000800c  @ Sprite record code 0x0c with side bit15 for nonzero player; enqueue_sprite_attr_record arg0.
```

`constants/ewram.inc`

```asm
.equ gEquipChainActivePhase, 0x0201e20c  @ u32 active phase; gP1LifePoints+EQUIP_CHAIN_ACTIVE_OFF = gDuelFieldSlots+EQUIP_CHAIN_ACTIVE_FROM_FIELD_OFF.
.equ equip_display_step_fn_table, 0x09e5aaec  @ ROM table base: 14 Thumb handler pointers and a null terminator; indexed by EQUIP_CHAIN_STEP_OFF word.
```

### REUSE

| 名称 | 值 | 既有定义 | 本段槽数 |
|---|---|---|---|
| AFTER_THE_STRUGGLE_CID | 0x00001512 | constants/card_info.inc:1974 | 1 |
| BES_COVERED_CORE_CID | 0x000019bf | constants/card_info.inc:1348 | 2 |
| BES_TETRAN_CID | 0x00001962 | constants/card_info.inc:691 | 1 |
| BIG_CORE_CID | 0x00001837 | constants/card_info.inc:831 | 2 |
| BIG_SHIELD_GARDNA_CID | 0x0000129c | constants/card_info.inc:1947 | 1 |
| BLACK_LUSTER_SOLDIER_ENVOY_CID | 0x000016cb | constants/card_info.inc:750 | 1 |
| CARD_PLAY_PHASE_CTR_OFF | 0x00001d1c | constants/ewram.inc:587 | 10 |
| CHAINSAW_INSECT_CID | 0x000019c7 | constants/card_info.inc:1327 | 1 |
| CYBER_ARCHFIEND_CID | 0x00001911 | constants/card_info.inc:631 | 1 |
| EHERO_NEO_BUBBLEMAN_CID | 0x000019a6 | constants/card_info.inc:694 | 1 |
| ELIGIB_ACT_COUNT_OFF | 0x00001d58 | constants/ewram.inc:420 | 1 |
| ELIGIB_ACT_TYPE_OFF | 0x00001d5c | constants/ewram.inc:421 | 1 |
| ELIGIB_STATE_CTRL_OFF | 0x00001d54 | constants/ewram.inc:419 | 1 |
| EQUIP_CHAIN_ACTIVE_FROM_FIELD_OFF | 0x00001cfc | constants/duel_field.inc:575 | 1 |
| EQUIP_CHAIN_ACTIVE_OFF | 0x00001d2c | constants/duel_field.inc:230 | 11 |
| EQUIP_CHAIN_STEP_FROM_FIELD_OFF | 0x00001cf8 | constants/duel_field.inc:574 | 3 |
| EQUIP_CHAIN_STEP_OFF | 0x00001d28 | constants/duel_field.inc:229 | 4 |
| FREED_THE_MATCHLESS_GENERAL_CID | 0x000014c4 | constants/card_info.inc:1427 | 2 |
| GETSU_FUHMA_CID | 0x0000170d | constants/card_info.inc:1913 | 1 |
| GIANT_ORC_CID | 0x000015d2 | constants/card_info.inc:868 | 1 |
| HAND_ARRAY_TO_COUNT_NEG_OFF | 0xfffffbfc | constants/ewram.inc:360 | 1 |
| HELPOEMER_CID_SHIFTED | 0xab880000 | constants/card_info.inc:431 | 1 |
| HINO_KAGU_TSUCHI_CID | 0x00001504 | constants/card_info.inc:1437 | 1 |
| INDOMITABLE_FIGHTER_LEI_LEI_CID | 0x00001915 | constants/card_info.inc:880 | 1 |
| KAMINOTE_BLOW_CID | 0x000018cd | constants/card_info.inc:973 | 1 |
| KANGAROO_CHAMP_CID | 0x00001866 | constants/card_info.inc:1505 | 1 |
| MAGICAL_HATS_CID | 0x00001362 | constants/card_info.inc:1166 | 1 |
| MAGIC_ARM_SHIELD_CID | 0x000012e2 | constants/card_info.inc:219 | 1 |
| MAHARAGHI_CID | 0x000014fd | constants/card_info.inc:1021 | 1 |
| MYTHICAL_BEAST_CERBERUS_CID | 0x00001983 | constants/card_info.inc:841 | 1 |
| OAM_EQUIP_SPRITE_TILE_P2_1B | 0x0000801b | constants/oam_attr.inc:154 | 1 |
| OAM_ZONE_SPRITE_PAIR_P2_FIRST | 0x00008028 | constants/oam_attr.inc:55 | 1 |
| P1LP_BLOCK2_OFF_1CE8 | 0x00001ce8 | constants/ewram.inc:276 | 4 |
| PLAYER_BLOCK_STRIDE | 0x00000868 | constants/ewram.inc:251 | 14 |
| PRICKLE_FAIRY_CID | 0x00001703 | constants/card_info.inc:188 | 1 |
| RED_MOON_BABY_CID | 0x00001415 | constants/card_info.inc:1175 | 1 |
| RYU_KOKKI_CID | 0x0000170e | constants/card_info.inc:1914 | 1 |
| SPEAR_DRAGON_CID | 0x000014d6 | constants/card_info.inc:1882 | 2 |
| SPRITE_ATTR_DUEL_PHASE_P2_B | 0x00008023 | constants/duel_field.inc:526 | 1 |
| SWORD_HUNTER_CID | 0x000012a6 | constants/card_info.inc:1986 | 2 |
| SWORD_OF_DRAGONS_SOUL_CID | 0x00001392 | constants/card_info.inc:1904 | 1 |
| THE_DARK_DOOR_CID | 0x00001469 | constants/card_info.inc:1950 | 1 |
| TOON_GOBLIN_AF_CID | 0x00001566 | constants/card_info.inc:171 | 1 |
| YATA_GARASU_CID | 0x000014ff | constants/card_info.inc:1435 | 2 |
| eval_gap_cid_11ed | 0x000011ed | constants/card_info.inc:418 | 1 |
| gDuelCardCtxBase | 0x0201e2a0 | constants/ewram.inc:218 | 2 |
| gDuelFieldSlots | 0x0201c510 | constants/ewram.inc:314 | 11 |
| gEquipChainSlotRefs | 0x0201bb90 | constants/ewram.inc:317 | 8 |
| gEquipZoneCountTable | 0x0201e1c8 | constants/ewram.inc:397 | 2 |
| gP1HandSlotArray | 0x0201c8f8 | constants/ewram.inc:334 | 2 |
| gP1LifePoints | 0x0201c4e0 | constants/ewram.inc:79 | 21 |
| gP1ZoneHandCount | 0x0201c4ec | constants/ewram.inc:232 | 1 |
| switchD_0809b806__switchdataD_0809b814 | 0x0809b814 | asm/12_equip_activation_scan.s:15899 | 1 |
| switchD_0809c020__switchdataD_0809c038 | 0x0809c038 | asm/12_equip_activation_scan.s:16978 | 1 |

同值辨析:

- 0x1cfc同时有DISP_SET_VARIANT_OFF (基址gP1LifePoints) 与EQUIP_CHAIN_ACTIVE_FROM_FIELD_OFF (基址gDuelFieldSlots). 0x0809bb46使用r6=gDuelFieldSlots, 故只复用后者. gDuelFieldSlots+0x1cfc=0x0201e20c, gP1LifePoints+0x1cfc=0x0201e1dc, 不能互换.
- 0x1cf8均与未偏移的gDuelFieldSlots相加, 得0x0201e208, 等于gP1LifePoints+EQUIP_CHAIN_STEP_OFF. 不加player_stride.
- 0x0201e1c8已有gEquipZoneCountTable和EQUIP_ZONE_COUNT_TABLE两名; 为REF复用现有RAM全局gEquipZoneCountTable, 消费者读其首word作为当前player并xor迭代两侧, 不将其描述为本段的计数数组.
- 0x0201c8f8保留既有gP1HandSlotArray名. 本段精确行为是从gP1LifePoints+0x14取count, 以4字节扫该数组; 负偏移0xfffffbfc准确到gP1HandCountBase=0x0201c4f4, 不是gP1ZoneHandCount=0x0201c4ec. 不扩大本段去改共享RAM全局的历史命名.
- MAGICAL_BLAST_CID=0x1984已存在, 本次仅新增其移位比较值和packed输入值; FAIRY_BOX_CID=0x13f9与HELPOEMER_CID=0x1571也复用作分量依据, HELPOEMER_CID_SHIFTED已有则直接复用. 本段没有为这些CID基础值新增别名.

## 消费者证据 (R6)

全部157槽的每个ldr使用点都在 `seg9-plan.json` 逐槽列出. 下列矩阵说明消费者含义和关键分歧; 槽身份、ROM值和基址均high, 卡名来自本地表, 不从旧plate或卡效果反推.

| 槽/值组 | 实际消费者与依据 | 置信度 |
|---|---|---|
| gEquipChainSlotRefs / gDuelFieldSlots / 0x868 | asm/12 L15029..15105: chain+0x2c+player*0x38两侧上下文, chain+0x18字段; gDuelFieldSlots+r_stride+slot*0x14与实体值/halfword比较. r8保持全局field基址, stride仅用于具体slot. | high |
| 0x0201e20c / 0x1cf8 / 0x1d2c | asm/12 L15108..15121读取绝对phase, 默认step=1+phase=0; L15768..15777设置step12, L15821..15830设置step2. L15751..15754和L15844..15849则从LP基址定位同一phase. 三种base+offset逐项算术核对. | high |
| CID 0x1993, 0x14d6, 0x18cd, 0x1866, 0x170e, 0x1837, 0x19a6, 0x19bf | asm/12 L15163..15340: 读上下文CID后比较树及chain查询, 后续组包/精确槽状态门控. Axe Dragonute与Spear Dragon为分支比较值, Kaminote Blow为chain节点目标. | high |
| CID 0x1703, 0x129c, 0x170d, 0x1962, 0x19c7, 0x16cb | asm/12 L15467..15616: 对侧上下文CID比较; L15787..15835: BLS chain+player状态bit23+eligibility gate, 成功后step2并display op0xb. | high |
| 状态机1返回契约 | asm/12 L15750..15866: phase0结束/phase1分支/默认分支均到movs r0,#0或持有0的同帧尾0x0809b7c6. 没有返回1路径. | high |
| 0x1ce8 / gEquipZoneCountTable | asm/12 L15926..15938、L16126..16135、L16271..16283以[LP+1ce8] xor 0/1遍历两侧; L16326..16338及L16416..16428读同一绝对地址201e1c8的首word. | high |
| CID 0x15d2/0x1566/0x1915/0x1983/0x1419 | asm/12 L15965..16067比较Giant Orc/Toon Goblin/Lei Lei/Cerberus; L16051..16054把Goblin Attack Force CID1419作为enqueue_sprite_attr_with_mode的r2, mode=0x22. 名称由卡表证实, 不称1419为动作mode. | high |
| Sword Hunter / Red-Moon Baby / Magic-Arm Shield | asm/12 L16171..16216查slot与zone descriptor; 成功续到L16581..16630的Sword Hunter路径. L16226..16260查Red-Moon Baby, packed输入OR side<<31后调用. L16271..16310遍历5field槽的Magic-Arm Shield链并推进phase. | high |
| Magical Hats / After the Struggle / Helpoemer | asm/12 L16322..16400和L16406..16473构造两侧slot位图并调用prepare_slot_ctx_for_equip_bitmap; L16487..16549扫描对方201c8f8数组, word<<19==HELPOEMER_CID_SHIFTED后解实体ID并传packed Helpoemer. | high |
| 四个*_ACTIVATION_PACKED | 槽0809badc/bd20/c1e4/c2cc在asm/12 L16235/L16504/L17166/L17271被加载, 与player<<31合并后传apply_equip_activation_with_id_lookup. asm/05 L8043..8078读取low16 CID及sign, 再调asm/06 L18682函数; L18716..18746把packed的mode/slot/type分量解入局部record. | high |
| packed分解 | 00501415=00500000|RED_MOON_BABY_CID; 004e1571=004e0000|HELPOEMER_CID; 025014fd=02500000|MAHARAGHI_CID; 004e1984=004e0000|MAGICAL_BLAST_CID. 分量(bits22:21,bits20:16,bits30:25)依次为(2,16,0),(2,14,0),(2,16,1),(2,14,0). | high |
| 0x9fc80000 / 0xcc200000 | asm/12 L16672..16696扫描双方field槽5..9, word<<19与9fc80000比较; L17259..17286按4字节逆扫201c8f8, word<<19与cc200000比较. 等式分别为(13f9<<19)&ffffffff和(1984<<19)&ffffffff. 非bitmask测试. | high |
| 0x09e5aaec / 0x1d28 / 0x1d2c | asm/12 L16727..16749: table[step]非NULL时通过invoke_r1转发player, CMP返回与0后BEQ不推进, 仅非0清phase并step++. NULL分支L16763返回1. 其余返回0. | high |
| 0x1d94 / 0x801b | asm/12 L16777..16824: LP+1d94外层state0设step6/phase1, extra_flag条件sprite, chain+14=1后外state++; L16841..16850: 调表驱动后重新读step并CMP8,BHI完成, 不以call结果为step. | high |
| check_field_allows_new_equip_action | asm/12 L16866..16916: Yata chain门控, LP+player*868+c零count、monster count与active equip count都零; 对手两种候选计数之一非零返回1. 纯读取判定. | high |
| 0x1548 / 0x0133 / 0x800c / 0x8023 / 0x8028 | asm/12 L16988..17068: Yata/Reckless Greed链及player状态flags决定phase0分支; 133送trigger_card_display_op31_if_not_active第二参数, asm/11 L30566..30583原样转dispatch op31的r2. 800c/8023/8028与0c/23/28按side分支配对, 为enqueue_sprite_attr_record首参数. | high |
| CID 0x1911/0x1504/0x14fd/0x14c4/0x1984 | asm/12 L17075..17324: Cyber Archfiend空count候选、Hino-Kagu-Tsuchi两侧计数循环、Maharaghi chain node packed输入及重试; Freed在field槽触发, Magical Blast在201c8f8数组触发. CID均本地表映射. | high |
| 0x1d1c / 0x1d54 / 0x1d58 / 0x1d5c | asm/12 L16928..16965从LP+1d1c取phase; L17325..17399等待displayctx, eligibility_state/type, 设置eligibility_count=1或phase--重试; L17421..17444统一存phase并返回0, terminal返回1. 均以LP为byte-offset基址. | high |
| CID 0x11ed | asm/12 L16568..16576和L16637..16647精确chain查询与显示参数. 全部5170卡表记录slot_id无11ed, data.md也无映射; 复用已存在eval_gap_cid_11ed中性名字, 不赋卡名. 数值/消费者high, 未分配卡名不作推断. | high / 名称语义med |

七个函数的输入与共享尾契约:

- update_equip_activation_display_state: r0=player_side, 保存到r6; 0x0809b7c6先回收0x14局部栈再恢复r8-r10与低寄存器.
- update_equip_zone_sprite_by_state: 0x4682@0x0809b7ec是mov r10,r0, 不是从r2取secondary_player. 尾0x0809bde6回收0x10局部栈再恢复r8-r10. default分支沿入口r4=LP/r6=phase_ptr清step/phase, 不将其视为其他case的迭代寄存器值.
- scan_equip_chain_slots_for_attr_enqueue: r0保存到r8, r9=常量1, 非额外入参; 两侧field槽5..9, 每槽0x14字节, 恒返回1.
- advance_equip_display_phase_via_table: r0=player_side, handler非0推进, NULL为唯一直接返回1路径.
- tick_equip_phase_display_by_state: r0=player_side,r1=extra_flag; 完成条件为存储的unsigned step>8. 当前无直接BL或raw/Thumb指针命中, 仍保留已有已反汇编函数.
- check_field_allows_new_equip_action: r0=player_side, 返回bool, +0xc是count而非flag.
- dispatch_equip_action_sprite_by_phase_state: 入参寄存器未使用, r6来自全局当前player; 0x0809c3ca只恢复本入口保存的r8/r9和低寄存器. phase0阻塞路径直接返回1, phase2有重试/落入phase3, 不写死每次phase++的描述.

### 本地CID证据

`tools/rom-export/export_card_data.py:371`规定首记录20字节、后续22字节. 第i条slot字段地址为0x098169b8+22*i; 对全部相关CID的全部匹配记录逐一读取ROM halfword验证. 卡名使用当前data/card-stats.s及doc/um06-deck-modification-tool/data.md对照, 包括新CID与所有packed/shifted分量. 完整重复记录和名字行见 `seg9-cid-evidence.json`.

| CID | 当前stats首记录 / 行 | ROM slot字段地址 | 本地名字行 | 卡名 |
|---|---|---|---|---|
| 0x000011ed | 无, 5170记录扫描0 | 无匹配 | 无匹配 | 保留eval_gap_cid_11ed |
| 0x0000129c | card_0618 / 8049 | 0x09819ed4 | data.md:609 | Big Shield Gardna |
| 0x000012a6 | card_0630 / 8205 | 0x09819fdc | data.md:618 | Sword Hunter |
| 0x000012e2 | card_0666 / 8673 | 0x0981a2f4 | data.md:653 | Magic-Arm Shield |
| 0x00001362 | card_0769 / 10012 | 0x0981abce | data.md:756 | Magical Hats |
| 0x00001392 | card_0807 / 10506 | 0x0981af12 | data.md:793 | Sword of Dragon's Soul |
| 0x000013f9 | card_0870 / 11325 | 0x0981b47c | data.md:856 | Fairy Box |
| 0x00001415 | card_0896 / 11663 | 0x0981b6b8 | data.md:882 | Red-Moon Baby |
| 0x00001419 | card_0900 / 11715 | 0x0981b710 | data.md:886 | Goblin Attack Force |
| 0x00001469 | card_0940 / 12235 | 0x0981ba80 | data.md:926 | The Dark Door |
| 0x000014c4 | card_1013 / 13184 | 0x0981c0c6 | data.md:998 | Freed the Matchless General |
| 0x000014d6 | card_1030 / 13405 | 0x0981c23c | data.md:1015 | Spear Dragon |
| 0x000014fd | card_1064 / 13847 | 0x0981c528 | data.md:1049 | Maharaghi |
| 0x000014ff | card_1066 / 13873 | 0x0981c554 | data.md:1051 | Yata-Garasu |
| 0x00001504 | card_1071 / 13938 | 0x0981c5c2 | data.md:1056 | Hino-Kagu-Tsuchi |
| 0x00001512 | card_1085 / 14120 | 0x0981c6f6 | data.md:1070 | After the Struggle |
| 0x00001548 | card_1131 / 14718 | 0x0981caea | data.md:1116 | Reckless Greed |
| 0x00001566 | card_1142 / 14861 | 0x0981cbdc | data.md:1126 | Toon Goblin Attack Force |
| 0x00001571 | card_1148 / 14939 | 0x0981cc60 | data.md:1132 | Helpoemer |
| 0x000015d2 | card_1222 / 15901 | 0x0981d2bc | data.md:1204 | Giant Orc |
| 0x000016cb | card_1421 / 18488 | 0x0981e3d6 | data.md:1401 | Black Luster Soldier - Envoy of the Beginning |
| 0x00001703 | card_1467 / 19086 | 0x0981e7ca | data.md:1447 | Prickle Fairy |
| 0x0000170d | card_1477 / 19216 | 0x0981e8a6 | data.md:1457 | Getsu Fuhma |
| 0x0000170e | card_1478 / 19229 | 0x0981e8bc | data.md:1458 | Ryu Kokki |
| 0x00001837 | card_1723 / 22414 | 0x0981fdca | data.md:1702 | Big Core |
| 0x00001866 | card_1767 / 22986 | 0x09820192 | data.md:1746 | Kangaroo Champ |
| 0x000018cd | card_1853 / 24104 | 0x098208f6 | data.md:1831 | Kaminote Blow |
| 0x00001911 | card_1902 / 24741 | 0x09820d2c | data.md:1880 | Cyber Archfiend |
| 0x00001915 | card_1906 / 24793 | 0x09820d84 | data.md:1884 | Indomitable Fighter Lei Lei |
| 0x00001962 | card_1968 / 25599 | 0x098212d8 | data.md:1946 | B.E.S. Tetran |
| 0x00001983 | card_1998 / 25989 | 0x0982156c | data.md:1976 | Mythical Beast Cerberus |
| 0x00001984 | card_1999 / 26002 | 0x09821582 | data.md:1977 | Magical Blast |
| 0x00001993 | card_2010 / 26145 | 0x09821674 | data.md:1988 | Axe Dragonute |
| 0x000019a6 | card_2015 / 26210 | 0x098216e2 | data.md:1993 | Elemental Hero Neo Bubbleman |
| 0x000019bf | card_2034 / 26457 | 0x09821884 | data.md:2012 | B.E.S. Covered Core |
| 0x000019c7 | card_2042 / 26561 | 0x09821934 | data.md:2020 | Chainsaw Insect |

所有新CID值都可对应卡名, 无未决语义. 已有constants部分历史card_NNNN注释与当前重导记录编号不同, 本表以当前ROM字段和slot_id为权威, 不扩大范围改既有常量注释.

## 5.1 登记 (Rule 3)

none. 本段裸块集合为空, 不改已有5.1表. 已反汇编的内部返回块或无raw指针函数不按裸数据孤儿登记.

## 自检与实施验收点

- `seg9-map-check.json`: 4704字节完整覆盖, 157槽值逐一吻合原ROM, 17 switch项逐一偶地址, 0x09e5aaec表14奇指针+NULL. 全ROMraw/Thumb扫描包含所有本段函数、内部尾、switch表/目标及外段表base.
- `seg9-plan.json`: 三类互斥, 104+32+21=157, 槽地址/标签各唯一且标签形式合规; 全部ldr列入uses. 14NEW均无同值/同名冲突, 52既有constants按用途复用, 2switch LABEL复用.
- 7 PLATE长度448/466/402/395/436/371/464, 全部ASCII且<=500. 21 RENAME EOL与5附加EOL、14NEW定义注释也均ASCII. 无函数改名, 无命名CSV变更.
- 既有gP1LifePoints的21池仅改槽名/EOL, 保留`.word gP1LifePoints`及operand0 DATA/DEFAULT主引用, 不新增、删除、重建或升级; 目标gP1LifePoints主LABEL保持USER_DEFINED; 32REF必须独立检查目标LABEL主符号、getName()实际值、operand0 source/type/primary及导出表达式.
- 落地后由fixer/主线程验证全段自动槽残留0, REF按名输出, EQ值与定义相同, 7条plate对应现名且无旧FUN/DAT伪说明. 25模块重导及构建byte-identical属于后续落地阶段, executor未运行构建, 不预称已通过.
- 无图形资源变更, 无图形辨识命名; R8不产生目视任务. 不修改全局exporter, 不变更scope外函数/表项/指令字节.

## 求助

none. 无需用户选择低置信语义; CID11ed继续使用已有已证实值的中性标识, 未猜卡名.

## Executor Report: F12-Seg-9

- 范围: [0x0809b178,0x0809c3d8), 4704B; 7主函数, 0独立共享尾.
- 槽: EQ=104 REF=32 RENAME=21 FUNC_RENAME=0 PLATE=7.
- carve=0 disasm=0 range 5.1=0; ROM_INCBIN/.byte=0.
- 新增定义: 12数值常量+gEquipChainActivePhase+equip_display_step_fn_table, 共14; 复用54既有符号.
- 求助: none.
- proposal: doc/dev/refine/F12-Seg-9.proposal.md
