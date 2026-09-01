# Refine Proposal: F13-Seg-3 [0x0809f744..0x080a0840)

本提案严格覆盖模块13第三段。executor只做测绘、证据冻结和可执行计划，不评分，不写Ghidra，不改正式asm/constants/CSV/registry，不build，不stage/commit。后续必须经过独立reviewer和fixer。

> Mode A修订：按首轮review唯一两项清单纠正ARMOR_EXE_CID密码旁证，并把段外FUN_0809ed50 registry PLATE改为受守卫的完整字段同步；动作表、函数/PLATE计数和carve范围不变。

## 段测绘

- 当前源: `asm/13_equip_placement.s`, SHA256 `634dafdad722f681b8f308cd112229f5363c7825c13f3536f0de27c9fdfbda49`。半开范围4348 B，字节覆盖连续且恰为`0x10fc`。
- fresh实测20个已有Function对象，其中10个入口无push；不新增Function。`f13-seg3-functions-before.json`冻结每个ID、body ranges、incoming、PLATE全文及body hash。
- 138个4B自动槽，共552 B：DAT=106、DWORD=15、PTR=17、UNK=0。138/138均由Thumb literal LDR机器码解码命中，禁止把旧PLATE或普通文本命中计作消费者。
- 段内ROM_INCBIN=0、`.byte`=0。段内裸块扫描为空；0x09e477ac与0x09e47884是本段literal引用的rom.s外部依赖，按Rule2 carve。
- 当前constants fresh解析6022条定义、5957个去重数值，22个inc文件hash保存在`f13-seg3-constant-values.json`。

| 入口 | 当前名 | Function ID | body B | indeg | body ranges |
| --- | --- | ---: | ---: | ---: | --- |
| 0x0809f744 | scan_all_monster_zone_slots_for_equip_activation_mirage_of_nightmare | 6859 | 178 | 0 | `[[0809f744, 0809f7d9] [0809f7ec, 0809f807]]` |
| 0x0809f808 | scan_trap_zone_for_equip_bitmap_update_bottomless_shifting_sand | 6860 | 72 | 0 | `[[0809f808, 0809f841] [0809f84c, 0809f859]]` |
| 0x0809f85c | scan_monster_zone_for_equip_activation_reserved_icid_a | 15813 | 12 | 0 | `[[0809f85c, 0809f867]]` |
| 0x0809f86c | scan_monster_zone_for_equip_activation_reserved_icid_b | 6861 | 12 | 0 | `[[0809f86c, 0809f877]]` |
| 0x0809f87c | scan_monster_zone_for_equip_activation_a_man_with_wdjat | 6862 | 12 | 0 | `[[0809f87c, 0809f887]]` |
| 0x0809f88c | scan_monster_zone_for_equip_activation_reserved_icid_c | 6863 | 12 | 0 | `[[0809f88c, 0809f897]]` |
| 0x0809f89c | get_lp_cost_by_field_spell_icid | 4532 | 138 | 5 | `[[0809f89c, 0809f8bf] [0809f8c8, 0809f8d5] [0809f8dc, 0809f8e3] [0809f8e8, 0809f8f9] [0809f900, 0809f911] [0809f918, 0809f943]]` |
| 0x0809f944 | check_slot_equippable_for_active_player | 3434 | 60 | 0 | `[[0809f944, 0809f977] [0809f984, 0809f98b]]` |
| 0x0809f98c | check_slot_effect_valid_for_active_player | 4396 | 56 | 0 | `[[0809f98c, 0809f9bb] [0809f9c4, 0809f9cb]]` |
| 0x0809f9cc | dispatch_duel_field_ai_phase_by_state_code | 4830 | 1828 | 0 | `[[0809f9cc, 0809fa45] [0809fa60, 0809fae3] [0809faec, 0809fb15] [0809fb98, 0809fbc9] [0809fbd8, 0809fc71] [0809fc84, 0809fca1] [0809fca8, 0809fcc1] [0809fcc8, 0809fcd5] [0809fcdc, 0809fd1d] [0809fd24, 0809fd61] [0809fd6c, 0809fdab] [0809fdb8, 0809fdfd] [0809fe08, 0809fe59] [0809fe6c, 0809ff5b] [0809ff78, 0809ff8f] [0809ff9c, 0809ffe7] [0809fff8, 0809ffff] [080a0004, 080a0015] [080a001c, 080a0081] [080a0090, 080a00c3] [080a00cc, 080a0109] [080a0114, 080a0137] [080a0144, 080a0161] [080a0168, 080a01ab] [080a01b4, 080a01c7] [080a01cc, 080a01e5] [080a01ec, 080a0219] [080a0228, 080a0253] [080a0258, 080a0295]]` |
| 0x0809fb16 | return_zero_from_duel_ai_main | 4499 | 108 | 8 | `[[0809fb16, 0809fb81]]` |
| 0x080a02a0 | advance_display_slot_if_zone_active | 4533 | 64 | 1 | `[[080a02a0, 080a02b7] [080a02bc, 080a02e3]]` |
| 0x080a02e8 | advance_effect_card_slot_display_if_zone_active | 4534 | 54 | 1 | `[[080a02e8, 080a0319] [080a0328, 080a032b]]` |
| 0x080a032c | set_phase_code_c8_exit_zero | 4535 | 8 | 1 | `[[080a032c, 080a0333]]` |
| 0x080a0334 | dispatch_equip_sprite_update_by_slot_icid | 4536 | 772 | 1 | `[[080a0334, 080a0367] [080a0378, 080a03f1] [080a0400, 080a0407] [080a040c, 080a0421] [080a042c, 080a0435] [080a043c, 080a0669]]` |
| 0x080a0694 | set_display_phase_code_78_exit_zero | 4537 | 6 | 1 | `[[080a0694, 080a0699]]` |
| 0x080a069a | write_display_code_exit_zero | 4500 | 6 | 8 | `[[080a069a, 080a069f]]` |
| 0x080a06a4 | return_one_from_duel_ai_main | 4538 | 2 | 5 | `[[080a06a4, 080a06a5]]` |
| 0x080a06a6 | release_duel_ai_main_frame | 4539 | 20 | 1 | `[[080a06a6, 080a06b9]]` |
| 0x080a06bc | tick_equip_display_phase_by_state_code | 16970 | 320 | 0 | `[[080a06bc, 080a06df] [080a06ec, 080a0705] [080a070c, 080a0779] [080a078c, 080a07f3] [080a0808, 080a0833]]` |

## 数据块分类 (Rule 2/3)

段内裸块扫描为空。下列两块属于本段指针槽的直接依赖；边界由真实消费者固定，而非按相邻名称推断。对每个4B候选地址均做raw和THUMB|1全ROM扫描，完整结果见`f13-seg3-rom-tables.json`。

| 块 | ref-scan(raw / THUMB|1) | 判定 | 消费者与边界证据 |
| --- | --- | --- | --- |
| 0x09e477ac..0x09e47884 / 216 B | base raw=1 at0x0809fb8c; thumb=0; 53个内部entry地址raw=0/thumb=0 | carve | 0x0809fb44读取cursor，0x0809fb46执行`cmp r1,#0x35`，0x0809fb56以cursor*4索引，故固定54项。 |
| 0x09e47884..0x09e47894 / 16 B | base raw=2 at0x0809fb84/0x0809fbcc; thumb=0; 3个内部entry地址raw=0/thumb=0 | carve | 0x0809fb24与0x0809fba6均从0开始，每次+1，`cmp r6,#3`后继续，故固定4项。 |

58个word原值均为odd THUMB Function地址，`value&~1`逐项命中当前inventory Function入口；每项`.word fn + 1`重算等于ROM。额外非对齐值命中完整保留在JSON，不是表基址引用。段内无R4 disasm范围，无§5.1零引用块。

Ghidra前态：54项表均为`/undefined *` 4 B，全部有operand0 DATA/DEFAULT到原odd地址；只首项有DEFAULT动态主标签。4项表前两word为`/undefined4`且无outref，后两word无DefinedData；首两word各有DEFAULT动态标签，后两项无符号。0x09e47894无DefinedData/符号。fixer按此差异守卫，不把原始4B字节等同已有Data。

## 符号化计划 (R1/R2/R3)

唯一动作并集为138：EQ=98、REF=21、RENAME=19。每个slot只出现一次；slot标签均匹配`^[a-z][a-z0-9_]+$`。完整机器对象、uses、前态refs/equates/comments见`f13-seg3-plan.json`。

### EQ_SLOTS (slot, value, const_name, slot_label)

```text
(0x0809f7e0, 0x00001d24, EQUIP_ACTIVATION_SCAN_CURSOR_OFF, equip_activation_scan_cursor_off_9f7e0)
(0x0809f7e4, 0x00000868, PLAYER_BLOCK_STRIDE, player_block_stride_9f7e4)
(0x0809f7e8, 0x00001539, MIRAGE_OF_NIGHTMARE_CID, mirage_of_nightmare_cid_9f7e8)
(0x0809f848, 0x00000868, PLAYER_BLOCK_STRIDE, player_block_stride_9f848)
(0x0809f868, 0x00001282, EQUIP_ACTIVATION_UNMAPPED_CID_1282, equip_activation_unmapped_cid_1282_9f868)
(0x0809f878, 0x000011ea, EQUIP_ACTIVATION_UNMAPPED_CID_11EA, equip_activation_unmapped_cid_11ea_9f878)
(0x0809f888, 0x0000158e, A_MAN_WITH_WDJAT_CID, a_man_with_wdjat_cid_9f888)
(0x0809f898, 0x00001147, EQUIP_ACTIVATION_UNMAPPED_CID_1147, equip_activation_unmapped_cid_1147_9f898)
(0x0809f8c0, 0x0000168c, VILEPAWN_ARCHFIEND_CID, vilepawn_archfiend_cid_9f8c0)
(0x0809f8c4, 0x00001381, MIRROR_WALL_CID, mirror_wall_cid_9f8c4)
(0x0809f8d8, 0x000013f9, FAIRY_BOX_CID, fairy_box_cid_9f8d8)
(0x0809f8e4, 0x00001639, TOKEN_1639_CID, token_1639_cid_9f8e4)
(0x0809f8fc, 0x0000168f, DESROOK_ARCHFIEND_CID, desrook_archfiend_cid_9f8fc)
(0x0809f914, 0x00001691, TERRORKING_ARCHFIEND_CID, terrorking_archfiend_cid_9f914)
(0x0809f97c, 0x00001ce8, P1LP_BLOCK2_OFF_1CE8, p1lp_block2_off_1ce8_9f97c)
(0x0809f980, 0x00001d24, EQUIP_ACTIVATION_SCAN_CURSOR_OFF, equip_activation_scan_cursor_off_9f980)
(0x0809f9c0, 0x00001ce8, P1LP_BLOCK2_OFF_1CE8, p1lp_block2_off_1ce8_9f9c0)
(0x0809fa48, 0xfffffd68, EQUIP_PHASE_FRAME_ALLOC_NEG_0X298, equip_phase_frame_alloc_neg_0x298_9fa48)
(0x0809fa50, 0x00001ce8, P1LP_BLOCK2_OFF_1CE8, p1lp_block2_off_1ce8_9fa50)
(0x0809fa54, 0x00000868, PLAYER_BLOCK_STRIDE, player_block_stride_9fa54)
(0x0809fa58, 0x0000137e, SOLOMONS_LAWBOOK_CID, solomons_lawbook_cid_9fa58)
(0x0809fa5c, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, card_play_phase_ctr_off_9fa5c)
(0x0809fae8, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, card_play_phase_ctr_off_9fae8)
(0x0809fb1c, 0x0000800d, OAM_EQUIP_SPRITE_P2_0D, oam_equip_sprite_p2_0d_9fb1c)
(0x0809fb20, 0x00001d24, EQUIP_ACTIVATION_SCAN_CURSOR_OFF, equip_activation_scan_cursor_off_9fb20)
(0x0809fb90, 0x00001d24, EQUIP_ACTIVATION_SCAN_CURSOR_OFF, equip_activation_scan_cursor_off_9fb90)
(0x0809fb94, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, card_play_phase_ctr_off_9fb94)
(0x0809fbd4, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, card_play_phase_ctr_off_9fbd4)
(0x0809fc74, 0x00001d24, EQUIP_ACTIVATION_SCAN_CURSOR_OFF, equip_activation_scan_cursor_off_9fc74)
(0x0809fc7c, 0x00000868, PLAYER_BLOCK_STRIDE, player_block_stride_9fc7c)
(0x0809fca4, 0x000013f4, MASK_OF_BRUTALITY_CID, mask_of_brutality_cid_9fca4)
(0x0809fcc4, 0x0000144a, EQUIP_ACTIVATION_UNMAPPED_CID_144A, equip_activation_unmapped_cid_144a_9fcc4)
(0x0809fcd8, 0x0000161b, ARMOR_EXE_CID, armor_exe_cid_9fcd8)
(0x0809fd68, 0x00001cec, P1LP_TIMER_OFF, p1lp_timer_off_9fd68)
(0x0809fdac, 0x00000868, PLAYER_BLOCK_STRIDE, player_block_stride_9fdac)
(0x0809fdb4, 0x00001cec, P1LP_TIMER_OFF, p1lp_timer_off_9fdb4)
(0x0809fe04, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, card_play_phase_ctr_off_9fe04)
(0x0809fe5c, 0x00001d24, EQUIP_ACTIVATION_SCAN_CURSOR_OFF, equip_activation_scan_cursor_off_9fe5c)
(0x0809fe64, 0x00000868, PLAYER_BLOCK_STRIDE, player_block_stride_9fe64)
(0x0809ff5c, 0x00001692, SKULL_ARCHFIEND_OF_LIGHTNING_CID, skull_archfiend_of_lightning_cid_9ff5c)
(0x0809ff60, 0x00000868, PLAYER_BLOCK_STRIDE, player_block_stride_9ff60)
(0x0809ff68, 0x00001cf4, P2LP_BLOCK2_OFF_1CF4, p2lp_block2_off_1cf4_9ff68)
(0x0809ff6c, 0x000016a2, BATTLE_SCARRED_CID, battle_scarred_cid_9ff6c)
(0x0809ff98, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, card_play_phase_ctr_off_9ff98)
(0x0809ffe8, 0x00001d24, EQUIP_ACTIVATION_SCAN_CURSOR_OFF, equip_activation_scan_cursor_off_9ffe8)
(0x0809ffec, 0x00000868, PLAYER_BLOCK_STRIDE, player_block_stride_9ffec)
(0x0809fff4, 0x00001381, MIRROR_WALL_CID, mirror_wall_cid_9fff4)
(0x080a0000, 0x00001639, TOKEN_1639_CID, token_1639_cid_a0000)
(0x080a0018, 0x00001770, LP_DELTA_6000, lp_delta_6000_a0018)
(0x080a0088, 0x00001d24, EQUIP_ACTIVATION_SCAN_CURSOR_OFF, equip_activation_scan_cursor_off_a0088)
(0x080a008c, 0x00000868, PLAYER_BLOCK_STRIDE, player_block_stride_a008c)
(0x080a00c8, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, card_play_phase_ctr_off_a00c8)
(0x080a010c, 0x00001d24, EQUIP_ACTIVATION_SCAN_CURSOR_OFF, equip_activation_scan_cursor_off_a010c)
(0x080a0110, 0x00000868, PLAYER_BLOCK_STRIDE, player_block_stride_a0110)
(0x080a0138, 0x00001d24, EQUIP_ACTIVATION_SCAN_CURSOR_OFF, equip_activation_scan_cursor_off_a0138)
(0x080a0140, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, card_play_phase_ctr_off_a0140)
(0x080a01ac, 0x00001d24, EQUIP_ACTIVATION_SCAN_CURSOR_OFF, equip_activation_scan_cursor_off_a01ac)
(0x080a01b0, 0x00000868, PLAYER_BLOCK_STRIDE, player_block_stride_a01b0)
(0x080a01c8, 0x0809f945, CHECK_SLOT_EQUIPPABLE_FOR_ACTIVE_PLAYER_THUMB_PTR, check_slot_equippable_for_active_player_thumb_ptr_a01c8)
(0x080a01e8, 0x00001d24, EQUIP_ACTIVATION_SCAN_CURSOR_OFF, equip_activation_scan_cursor_off_a01e8)
(0x080a021c, 0x00001d68, ELIGIB_SPRITE_CTRL_OFF, eligib_sprite_ctrl_off_a021c)
(0x080a0220, 0x00001d6c, ELIGIB_ANIM_STATE_OFF, eligib_anim_state_off_a0220)
(0x080a0224, 0x00001d24, EQUIP_ACTIVATION_SCAN_CURSOR_OFF, equip_activation_scan_cursor_off_a0224)
(0x080a0298, 0x00001d24, EQUIP_ACTIVATION_SCAN_CURSOR_OFF, equip_activation_scan_cursor_off_a0298)
(0x080a029c, 0x00000868, PLAYER_BLOCK_STRIDE, player_block_stride_a029c)
(0x080a02b8, 0x0809f98d, CHECK_SLOT_EFFECT_VALID_FOR_ACTIVE_PLAYER_THUMB_PTR, check_slot_effect_valid_for_active_player_thumb_ptr_a02b8)
(0x080a02e4, 0x00001d24, EQUIP_ACTIVATION_SCAN_CURSOR_OFF, equip_activation_scan_cursor_off_a02e4)
(0x080a031c, 0x00001d68, ELIGIB_SPRITE_CTRL_OFF, eligib_sprite_ctrl_off_a031c)
(0x080a0320, 0x00001d6c, ELIGIB_ANIM_STATE_OFF, eligib_anim_state_off_a0320)
(0x080a0324, 0x00001d24, EQUIP_ACTIVATION_SCAN_CURSOR_OFF, equip_activation_scan_cursor_off_a0324)
(0x080a0368, 0x00000868, PLAYER_BLOCK_STRIDE, player_block_stride_a0368)
(0x080a0370, 0x00000ff9, CASTLE_OF_DARK_ILLUSIONS_CID, castle_of_dark_illusions_cid_a0370)
(0x080a0374, 0x000014ac, VISER_DES_CID, viser_des_cid_a0374)
(0x080a03f4, 0x00000868, PLAYER_BLOCK_STRIDE, player_block_stride_a03f4)
(0x080a03fc, 0x0000131a, STIM_PACK_CID, stim_pack_cid_a03fc)
(0x080a0408, 0x0000159c, DIFFERENT_DIMENSION_CAPSULE_CID, different_dimension_capsule_cid_a0408)
(0x080a0424, 0x000017a1, DUST_BARRIER_CID, dust_barrier_cid_a0424)
(0x080a0428, 0x000015ee, WAVE_MOTION_CANNON_CID, wave_motion_cannon_cid_a0428)
(0x080a0438, 0x0000187c, SWORDS_OF_CONCEALING_LIGHT_CID, swords_of_concealing_light_cid_a0438)
(0x080a066c, 0x000012c8, LIGHTFORCE_SWORD_CID, lightforce_sword_cid_a066c)
(0x080a0670, 0x00000868, PLAYER_BLOCK_STRIDE, player_block_stride_a0670)
(0x080a0678, 0xffffff00, FIELD_SPELL_TO_ZONE_COUNT_DELTA_NEG_0X100, field_spell_to_zone_count_delta_neg_0x100_a0678)
(0x080a0680, 0x000fffff, EQUIP_NODE_TAG_MASK, equip_node_tag_mask_a0680)
(0x080a0684, 0x000112c8, LIGHTFORCE_SWORD_CHAIN_NODE_TAG, lightforce_sword_chain_node_tag_a0684)
(0x080a0688, 0x0000803b, OAM_EQUIP_SET_SLOT_P2, oam_equip_set_slot_p2_a0688)
(0x080a0690, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, card_play_phase_ctr_off_a0690)
(0x080a06a0, 0x00001cec, P1LP_TIMER_OFF, p1lp_timer_off_a06a0)
(0x080a06e4, 0x00001ce8, P1LP_BLOCK2_OFF_1CE8, p1lp_block2_off_1ce8_a06e4)
(0x080a06e8, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, card_play_phase_ctr_off_a06e8)
(0x080a0708, 0x00008003, OAM_EQUIP_SPRITE_P2_03, oam_equip_sprite_p2_03_a0708)
(0x080a077c, 0x00000868, PLAYER_BLOCK_STRIDE, player_block_stride_a077c)
(0x080a0788, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, card_play_phase_ctr_off_a0788)
(0x080a07f4, 0x00001cec, P1LP_TIMER_OFF, p1lp_timer_off_a07f4)
(0x080a07f8, 0x00000868, PLAYER_BLOCK_STRIDE, player_block_stride_a07f8)
(0x080a07fc, 0x00001cfc, DISP_SET_VARIANT_OFF, disp_set_variant_off_a07fc)
(0x080a0804, 0x000010dc, LP_DISCARD_ZONE_OFF, lp_discard_zone_off_a0804)
(0x080a0834, 0x00008004, OAM_EQUIP_SPRITE_P2_04, oam_equip_sprite_p2_04_a0834)
(0x080a083c, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, card_play_phase_ctr_off_a083c)
```

### REF_SLOTS (slot, target, gas_label, slot_label)

```text
(0x0809fb84, 0x09e47884, equip_activation_phase1_callbacks, equip_activation_phase1_callbacks_9fb84)
(0x0809fb8c, 0x09e477ac, equip_activation_phase3_callbacks, equip_activation_phase3_callbacks_9fb8c)
(0x0809fbcc, 0x09e47884, equip_activation_phase1_callbacks, equip_activation_phase1_callbacks_9fbcc)
(0x0809fc80, 0x0201c510, gDuelFieldSlots, gduelfieldslots_9fc80)
(0x0809fd20, 0x0201c510, gDuelFieldSlots, gduelfieldslots_9fd20)
(0x0809fd64, 0x0201c510, gDuelFieldSlots, gduelfieldslots_9fd64)
(0x0809fdb0, 0x0201c510, gDuelFieldSlots, gduelfieldslots_9fdb0)
(0x0809fe60, 0x0201e204, gEquipActivationScanCursor, gequipactivationscancursor_9fe60)
(0x0809fe68, 0x0201c510, gDuelFieldSlots, gduelfieldslots_9fe68)
(0x0809ff64, 0x0201c510, gDuelFieldSlots, gduelfieldslots_9ff64)
(0x0809ff74, 0x0201e204, gEquipActivationScanCursor, gequipactivationscancursor_9ff74)
(0x0809ff90, 0x0201e204, gEquipActivationScanCursor, gequipactivationscancursor_9ff90)
(0x0809fff0, 0x0201e2a0, gDuelCardCtxBase, gduelcardctxbase_9fff0)
(0x080a0164, 0x0201e2a0, gDuelCardCtxBase, gduelcardctxbase_a0164)
(0x080a0254, 0x0201e2a0, gDuelCardCtxBase, gduelcardctxbase_a0254)
(0x080a036c, 0x0201c510, gDuelFieldSlots, gduelfieldslots_a036c)
(0x080a03f8, 0x0201c510, gDuelFieldSlots, gduelfieldslots_a03f8)
(0x080a0674, 0x0201c5ec, gDuelFieldSpellZoneBase, gduelfieldspellzonebase_a0674)
(0x080a067c, 0x0201d9c0, gEquipNodePool, gequipnodepool_a067c)
(0x080a0780, 0x0201c510, gDuelFieldSlots, gduelfieldslots_a0780)
(0x080a0800, 0x0201e2a0, gDuelCardCtxBase, gduelcardctxbase_a0800)
```

### RENAME_SLOTS (slot, slot_label, eol_ascii)

```text
(0x0809f7dc, gp1lp_base_9f7dc, "gP1LifePoints base; preserve the existing DATA reference and its source.")
(0x0809f844, gp1lp_base_9f844, "gP1LifePoints base; preserve the existing DATA reference and its source.")
(0x0809f978, gp1lp_base_9f978, "gP1LifePoints base; preserve the existing DATA reference and its source.")
(0x0809f9bc, gp1lp_base_9f9bc, "gP1LifePoints base; preserve the existing DATA reference and its source.")
(0x0809fa4c, gp1lp_base_9fa4c, "gP1LifePoints base; preserve the existing DATA reference and its source.")
(0x0809fae4, gp1lp_base_9fae4, "gP1LifePoints base; preserve the existing DATA reference and its source.")
(0x0809fb88, gp1lp_base_9fb88, "gP1LifePoints base; preserve the existing DATA reference and its source.")
(0x0809fbd0, gp1lp_base_9fbd0, "gP1LifePoints base; preserve the existing DATA reference and its source.")
(0x0809fc78, gp1lp_base_9fc78, "gP1LifePoints base; preserve the existing DATA reference and its source.")
(0x0809fe00, gp1lp_base_9fe00, "gP1LifePoints base; preserve the existing DATA reference and its source.")
(0x0809ff70, gp1lp_base_9ff70, "gP1LifePoints base; preserve the existing DATA reference and its source.")
(0x0809ff94, gp1lp_base_9ff94, "gP1LifePoints base; preserve the existing DATA reference and its source.")
(0x080a0084, gp1lp_base_a0084, "gP1LifePoints base; preserve the existing DATA reference and its source.")
(0x080a00c4, gp1lp_base_a00c4, "gP1LifePoints base; preserve the existing DATA reference and its source.")
(0x080a013c, gp1lp_base_a013c, "gP1LifePoints base; preserve the existing DATA reference and its source.")
(0x080a068c, gp1lp_base_a068c, "gP1LifePoints base; preserve the existing DATA reference and its source.")
(0x080a06e0, gp1lp_base_a06e0, "gP1LifePoints base; preserve the existing DATA reference and its source.")
(0x080a0784, gp1lp_base_a0784, "gP1LifePoints base; preserve the existing DATA reference and its source.")
(0x080a0838, gp1lp_base_a0838, "gP1LifePoints base; preserve the existing DATA reference and its source.")
```

EQ只把equate附到slot地址operand0，不把常量附到LDR指令。两个odd callback槽0x080a01c8/0x080a02b8以NEW equate输出原odd值，并各加一条operand0 DATA/USER_DEFINED辅助引用到偶Function入口0x0809f944/0x0809f98c；保留Function主符号，不创建odd USER alias。ExportRangeToGas排除ROM FUNCTION且sanitize会改写`+`，因此不能承诺普通REF自动输出`fn+1`。

19个RENAME槽仍输出`.word gP1LifePoints`。现有refs中17条是DATA/DEFAULT、2条(0x080a06e0/0x080a0784)是DATA/USER_DEFINED；全部原样保留，只改槽标签和EOL。目标USER LABEL不等于引用source。

21个REF分别为gDuelFieldSlots×9、gDuelFieldSpellZoneBase×1、gEquipNodePool×1、gEquipActivationScanCursor×3、gDuelCardCtxBase×4、phase3 table×1、phase1 table×2。为每个slot重建/建立精确operand0 DATA/USER_DEFINED primary引用；保留其他operand及非目标引用。RAM DefinedData前态必须保持：gDuelFieldSpellZoneBase/gEquipNodePool为None，gEquipActivationScanCursor为`/undefined4`。不读取RAM值。

### REF目标前态与动作

| 目标 | 输出名 | 前态 | 动作 |
| --- | --- | --- | --- |
| 0x0201c510 | gDuelFieldSlots | symbol 20369/USER_DEFINED/gDuelFieldSlots; Data /undefined4 4B; incoming 980 | reuse existing USER primary label; preserve Data/incoming |
| 0x0201c5ec | gDuelFieldSpellZoneBase | symbol 32172/USER_DEFINED/gDuelFieldSpellZoneBase; Data None; incoming 2 | reuse existing USER primary label; preserve Data/incoming |
| 0x0201d9c0 | gEquipNodePool | symbol 20380/USER_DEFINED/gEquipNodePool; Data None; incoming 134 | reuse existing USER primary label; preserve Data/incoming |
| 0x0201e204 | gEquipActivationScanCursor | symbol 4611686018461065732/DEFAULT/DAT_0201e204; Data /undefined4 4B; incoming 202 | create USER primary label; preserve Data/incoming |
| 0x0201e2a0 | gDuelCardCtxBase | symbol 18879/USER_DEFINED/gDuelCardCtxBase; Data /undefined4 4B; incoming 55 | reuse existing USER primary label; preserve Data/incoming |
| 0x09e477ac | equip_activation_phase3_callbacks | symbol 4611686018593355692/DEFAULT/PTR_scan_equip_zone_for_dimensionhole+1_09e477ac; Data /undefined * 4B; incoming 1 | create USER primary label; preserve Data/incoming |
| 0x09e47884 | equip_activation_phase1_callbacks | symbol 4611686018593355908/DEFAULT/DAT_09e47884; Data /undefined4 4B; incoming 2 | create USER primary label; preserve Data/incoming |

## FUNC_RENAME

```text
(0x0809f744, scan_all_monster_zone_slots_for_equip_activation_mirage_of_nightmare, scan_all_spell_trap_zone_slots_for_equip_activation_mirage_of_nightmare)
(0x0809f89c, get_lp_cost_by_field_spell_icid, get_maintenance_lp_cost_by_icid)
(0x0809f9cc, dispatch_duel_field_ai_phase_by_state_code, run_equip_activation_display_phase_by_state_code)
(0x0809fb16, return_zero_from_duel_ai_main, return_zero_from_equip_activation_display_phase)
(0x080a06a4, return_one_from_duel_ai_main, return_one_from_equip_activation_display_phase)
(0x080a06a6, release_duel_ai_main_frame, release_equip_activation_display_phase_frame)
```

| 地址 / ID | 旧名 | 新名 | Ghidra indeg | ROM even / odd |
| --- | --- | --- | ---: | --- |
| 0x0809f744 / 6859 | scan_all_monster_zone_slots_for_equip_activation_mirage_of_nightmare | scan_all_spell_trap_zone_slots_for_equip_activation_mirage_of_nightmare | 0 | 0 / 1 |
| 0x0809f89c / 4532 | get_lp_cost_by_field_spell_icid | get_maintenance_lp_cost_by_icid | 5 | 0 / 0 |
| 0x0809f9cc / 4830 | dispatch_duel_field_ai_phase_by_state_code | run_equip_activation_display_phase_by_state_code | 0 | 0 / 1 |
| 0x0809fb16 / 4499 | return_zero_from_duel_ai_main | return_zero_from_equip_activation_display_phase | 8 | 0 / 0 |
| 0x080a06a4 / 4538 | return_one_from_duel_ai_main | return_one_from_equip_activation_display_phase | 5 | 0 / 0 |
| 0x080a06a6 / 4539 | release_duel_ai_main_frame | release_equip_activation_display_phase_frame | 1 | 0 / 0 |

- 0x0809f744: actual instructions compute `side=(cursor/5)^player` and `slot=cursor%5+5` before `test_slot_has_active_card`; the old `monster_zone` object is false. Ghidra indeg=0, and its one ROM odd pointer is table word0x09e47814. Keep Function ID6859/body and change that carve entry to the new name. Confidence high.
- 0x0809f89c: the pure BST maps maintenance cards to periodic costs: Messenger100, Imperial Order700, Mirror Wall2000, Mask of Brutality1000, Fairy Box500, token1639=1000, Vilepawn500, Shadowknight900, Darkbishop500, Desrook500, Infernalqueen500, Terrorking800, Skull Archfiend500. These are not all field spells. Five real BL callers are0x0809fd4c/0x0809fec4/0x0809fed0/0x080a00a4/0x080a00fc. Keep Function ID4532/body. Confidence high.

- 0x0809f9cc: `tick_equip_activation_dispatch_hub` uses the odd pointer at0x09e5aac8 from `EQUIP_PHASE_FN_TABLE_ROM`; its return advances the equip main phase. The body reads equip-display state, runs the phase-1/phase-3 callback tables, scans equip slots, renders LP indicators, and writes display phase codes. It contains no AI choice inputs or AI result structure. Keep Function ID4830 and its existing discontiguous body ranges. Confidence high.
- 0x0809fb16/0x080a06a4/0x080a06a6 are the return-zero entry, return-one entry, and 0x298-byte frame-release tail of the same 0x0809f9cc display-phase frame. Their instructions, eight/five/one explicit incoming references, the fallthrough from0x080a06a4, Function IDs4499/4538/4539, and body ranges remain unchanged. The grouped names remove the false `duel_ai_main` owner while preserving each entry contract. Confidence high.

正式同步范围：
- `asm/13_equip_placement.s`: 改6个Function定义名及所有真实BL/B/条件分支操作数；20个审定全文PLATE同时清除旧AI/FUN描述。机器码、Function body和引用对象不变。
- `asm/rom.s`: 新carve的0x09e47814项使用f744新名并保持raw `0x0809f745`。0x09e5aac8继续位于既有incbin，raw `0x0809f9cd`不改，不为本次rename扩大carve。
- `doc/dev/naming-proposals.csv`: 按地址仅改0x0809f744/0x0809f89c/0x0809f9cc/0x0809fb16/0x080a06a4/0x080a06a6六行name单元格，其余列不变。
- `tools/ghidra-labeling/RenameKnownFunctions.py`: 更新已有f744地址tuple的name+审定plate，并为当前缺tuple的其余5个地址补入`FUN_<addr>`到新name+审定plate的registry项；不得全仓库盲替。
- registry-only依赖：key=`FUN_0809ed50`、target=`scan_all_monster_zone_slots_for_equip_activation_infernalqueen_archfiend`的第三字段当前为630字符，写前须全文相等或SHA256=`93c4ad8ba5f608c53307a5e3cd98628a7525395d7ebed53f713e833675c0afcc`。禁止在旧字段上做substring替换；必须把第三字段完整替换为以下Seg-2已审定的347字符ASCII全文：
```text
r0=player. Resume ten monster slots with LP+0x1d24 cursor: side=(cursor/5)^player, slot=cursor%5. For active Infernalqueen Archfiend, pack the actual entry CID, side and slot, then call activation with decoded flags. Ignore its result; advance cursor and return 0 after the first match. Other entries advance and continue. Return 1 after cursor 9.
```
- 上述目标全文SHA256=`a4e4cb281edffe3e3534690a3883fdd4b69ae802c1c14e6732199205273b27e1`。这是registry tuple完整字段同步；当前真实0x0809ed50 Ghidra/asm PLATE已是该全文，不新增Ghidra PLATE，不改其Function/body/refs/EOL/机器字节。本段Ghidra PLATE仍为20；本轮会触及的6个改名tuple PLATE和该sibling tuple PLATE共7个payload必须全部ASCII且<=500字符。
- 保存Ghidra后用真实ExportFunctionInventory流程刷新4份inventory；只允许六个name变化及其派生文本，不手工编辑inventory。历史proposal/review/冻结证据保留原文。精确当前生产旧名命中见`f13-seg3-rename-dependencies.json`。

## PLATE (R5)

20个已有Function的PLATE全部全文替换。每段以下文字均为ASCII且<=500；旧全文和hash在`f13-seg3-plates.json`，fixer先做全文或SHA256守卫。8行旧PLATE中的FUN_引用随全文替换清零，段内SUB_命中为0。

### 0x0809f744 scan_all_spell_trap_zone_slots_for_equip_activation_mirage_of_nightmare

新长度327；旧SHA256 `18d50d36f9b335e2c0e76c964af4509aad4359fcfaf6929ddad7ce656fe23731`；Function ID6859，body `[[0809f744, 0809f7d9] [0809f7ec, 0809f807]]`。

```text
r0=player. Resume cursor 0..9 at gP1LifePoints+EQUIP_ACTIVATION_SCAN_CURSOR_OFF. Decode side=player^(cursor/5) and spell/trap slot=cursor%5+5. On an active Mirage of Nightmare, pack the slot entry and call apply_equip_activation_with_id_lookup, advance the cursor, and return0. Misses advance and continue; exhaustion returns1.
```

### 0x0809f808 scan_trap_zone_for_equip_bitmap_update_bottomless_shifting_sand

新长度258；旧SHA256 `570da51a7beb85eb20686fddb7af062c70714b8fe489fb11cf54879042ef4757`；Function ID6860，body `[[0809f808, 0809f841] [0809f84c, 0809f859]]`。

```text
r0=player. If the per-player zone count at base+0xc exceeds4, return1. Otherwise scan spell/trap slots5..9 for Bottomless Shifting Sand (ICID 0x1540). On the first active match, enqueue its equip-slot bitmap and return0. Return1 when no active match remains.
```

### 0x0809f85c scan_monster_zone_for_equip_activation_reserved_icid_a

新长度234；旧SHA256 `e35ebbe3f1def06f00a32495ad19bc50e4b5452fb5c11c3f2533b1523b36e0f9`；Function ID15813，body `[[0809f85c, 0809f867]]`。

```text
r0=player. Call scan_monster_zone_for_equip_activation_by_card with the unmapped internal CID 0x1282. Return the callee result: 0 after one activation, 1 after scan exhaustion. The wrapper uses BL and returns through its own epilogue.
```

### 0x0809f86c scan_monster_zone_for_equip_activation_reserved_icid_b

新长度234；旧SHA256 `f56c23174d2567e4da380de925ddbfe010889bcb7fb7302d5bc8adc059b5dc5e`；Function ID6861，body `[[0809f86c, 0809f877]]`。

```text
r0=player. Call scan_monster_zone_for_equip_activation_by_card with the unmapped internal CID 0x11ea. Return the callee result: 0 after one activation, 1 after scan exhaustion. The wrapper uses BL and returns through its own epilogue.
```

### 0x0809f87c scan_monster_zone_for_equip_activation_a_man_with_wdjat

新长度222；旧SHA256 `7af8fef1feb6a72bf059c793a378e3dcb780b1989e3a80253bae00c5f38b68ef`；Function ID6862，body `[[0809f87c, 0809f887]]`。

```text
r0=player. Call scan_monster_zone_for_equip_activation_by_card with A_MAN_WITH_WDJAT_CID. Return the callee result: 0 after one activation, 1 after scan exhaustion. The wrapper uses BL and returns through its own epilogue.
```

### 0x0809f88c scan_monster_zone_for_equip_activation_reserved_icid_c

新长度234；旧SHA256 `9719055f6a51b9fa2893a4ed3fe2f5a86d0949c99dd9f752d6fd6437764020f3`；Function ID6863，body `[[0809f88c, 0809f897]]`。

```text
r0=player. Call scan_monster_zone_for_equip_activation_by_card with the unmapped internal CID 0x1147. Return the callee result: 0 after one activation, 1 after scan exhaustion. The wrapper uses BL and returns through its own epilogue.
```

### 0x0809f89c get_maintenance_lp_cost_by_icid

新长度320；旧SHA256 `54bd9ee9326773f17a89b70f5ef302bccc5002f388c61f8e511d11a15a5df9ea`；Function ID4532，body `[[0809f89c, 0809f8bf] [0809f8c8, 0809f8d5] [0809f8dc, 0809f8e3] [0809f8e8, 0809f8f9] [0809f900, 0809f911] [0809f918, 0809f943]]`。

```text
r0=internal CID. Return the periodic LP maintenance cost, or0 when unmatched. Mappings are Messenger100, Imperial Order700, Mirror Wall2000, Mask of Brutality1000, Fairy Box500, token1639=1000, Vilepawn500, Shadowknight900, Darkbishop500, Desrook500, Infernalqueen500, Terrorking800, and Skull Archfiend500. Pure lookup.
```

### 0x0809f944 check_slot_equippable_for_active_player

新长度280；旧SHA256 `f46168962310441c8ce2dea5dcdfbc913b6023e731b75a5265aecdd799351d33`；Function ID3434，body `[[0809f944, 0809f977] [0809f984, 0809f98b]]`。

```text
r0=player, r1+r2=monster slot. Require slot<=4, player equal to the active selector at gP1LifePoints+0x1ce8, check_slot_card_can_be_equipped nonzero, and slot different from the shared scan cursor. Return0x800 when all checks pass, else0. Stored as a THUMB callback at 0x080a01c8.
```

### 0x0809f98c check_slot_effect_valid_for_active_player

新长度225；旧SHA256 `b9920dea7dbbae4e387b3e151aed4da39c5e57709b6331281dac2e3a16167de2`；Function ID4396，body `[[0809f98c, 0809f9bb] [0809f9c4, 0809f9cb]]`。

```text
r0=player, r1+r2=slot. Require player to match the XOR-derived side from gP1LifePoints+0x1ce8/+0x1d20, slot<=10, and get_slot_effect_card_value nonzero. Return0x800 on success, else0. Stored as a THUMB callback at 0x080a02b8.
```

### 0x0809f9cc run_equip_activation_display_phase_by_state_code

新长度405；旧SHA256 `19cfa37ac5a5270bda85cb00dc1aa3ce0cbfaaf90ace886f9ec13f417166f37f`；Function ID4830，body `[[0809f9cc, 0809fa45] [0809fa60, 0809fae3] [0809faec, 0809fb15] [0809fb98, 0809fbc9] [0809fbd8, 0809fc71] [0809fc84, 0809fca1] [0809fca8, 0809fcc1] [0809fcc8, 0809fcd5] [0809fcdc, 0809fd1d] [0809fd24, 0809fd61] [0809fd6c, 0809fdab] [0809fdb8, 0809fdfd] [0809fe08, 0809fe59] [0809fe6c, 0809ff5b] [0809ff78, 0809ff8f] [0809ff9c, 0809ffe7] [0809fff8, 0809ffff] [080a0004, 080a0015] [080a001c, 080a0081] [080a0090, 080a00c3] [080a00cc, 080a0109] [080a0114, 080a0137] [080a0144, 080a0161] [080a0168, 080a01ab] [080a01b4, 080a01c7] [080a01cc, 080a01e5] [080a01ec, 080a0219] [080a0228, 080a0253] [080a0258, 080a0295]]`。

```text
No APCS inputs. Allocate0x298 bytes, read player and equip-display phase from gP1LifePoints, and drive the large phase tree. Paths run the 4-entry phase-1 callbacks, resume the 54-entry phase-3 callbacks by cursor, scan slots, render maintenance LP values, initialize validation callbacks, or dispatch special equip sprites. Return0 while work remains and1 when complete through the shared frame epilogue.
```

### 0x0809fb16 return_zero_from_equip_activation_display_phase

新长度353；旧SHA256 `1623aa658afe0ffa0ee22b6a46a966dd1b281292c14a50d1d59fb949671f2d78`；Function ID4499，body `[[0809fb16, 0809fb81]]`。

```text
Entry sets r0=0 and calls release_equip_activation_display_phase_frame. Ghidra body also owns pools at0x0809fb1c/20 and the parent phase fragment at0x0809fb24..80, reached from the parent branch at0x0809fa32. That fragment runs four phase-1 callbacks, then resumes one of 54 phase-3 callbacks by cursor. Preserve the discontiguous parent-flow ownership.
```

### 0x080a02a0 advance_display_slot_if_zone_active

新长度306；旧SHA256 `57a3deea5a866ba73aa484b06c4d1163fe458d3dc46f1605011db9e0235a9fa4`；Function ID4533，body `[[080a02a0, 080a02b7] [080a02bc, 080a02e3]]`。

```text
Shared parent fragment; non-APCS r4=state base, r1=slot, r7=slot-index pointer. If state+0x1d40 is set, advance *r7, initialize the effect-valid callback, and return0. Otherwise enqueue the slot bitmap using state+0x1d20, advance the shared cursor, write phase0x65, and return0 through the parent epilogue.
```

### 0x080a02e8 advance_effect_card_slot_display_if_zone_active

新长度266；旧SHA256 `9a511f600bd4d2bd12e125994312334ac1a877425112c92fdd55ff9bd7f933b3`；Function ID4534，body `[[080a02e8, 080a0319] [080a0328, 080a032b]]`。

```text
Shared parent fragment; non-APCS r4=state base and r7=phase pointer. If display state is unconfirmed, write phase0x82 and return0. Otherwise enqueue an effect-card slot sprite from offsets0x1d68/0x1d6c/0x1d74, advance the shared cursor, write phase0x65, and return0.
```

### 0x080a032c set_phase_code_c8_exit_zero

新长度170；旧SHA256 `a3df75af8fdef54d94e81c365fa877b7e826bfe452b0decc2d6fee5671024cb6`；Function ID4535，body `[[080a032c, 080a0333]]`。

```text
Shared parent exit with non-APCS r7=phase pointer. Write0xc8 to *r7, then call return_zero_from_equip_activation_display_phase. Returns0 after releasing the parent frame.
```

### 0x080a0334 dispatch_equip_sprite_update_by_slot_icid

新长度345；旧SHA256 `83a0bbb7f48f7eca867984ce2f43465ec227529eb0984fbfdca12bde0daceca0`；Function ID4536，body `[[080a0334, 080a0367] [080a0378, 080a03f1] [080a0400, 080a0407] [080a040c, 080a0421] [080a042c, 080a0435] [080a043c, 080a0669]]`。

```text
Shared parent fragment with non-APCS r8=player. Scan monster slots0..4 for Castle of Dark Illusions and Viser Des sprite paths, then spell/trap slots5..9 for card-specific set-slot, bitmap, and LP indicator paths. After the slot scan, handle Lightforce Sword chain nodes, advance the equip-display phase, and return0 through the parent epilogue.
```

### 0x080a0694 set_display_phase_code_78_exit_zero

新长度209；旧SHA256 `78d0f6907a8670e2bd918710eb5f5fe5a988f9eb0f64221e79b3442383b837e4`；Function ID4537，body `[[080a0694, 080a0699]]`。

```text
Shared parent entry with non-APCS r4=state base. Form r1=r4+P1LP_TIMER_OFF and r0=0x78, then fall through to write_display_code_exit_zero. The combined path writes0x78 and returns0 through the parent epilogue.
```

### 0x080a069a write_display_code_exit_zero

新长度225；旧SHA256 `4aa895535f3d842cdac2bb93a0694953509527a6efc0efb2cf2989fb465d6c81`；Function ID4500，body `[[080a069a, 080a069f]]`。

```text
Shared parent exit. Inputs r0=value and r1=target word. Store r0 to *r1, then call return_zero_from_equip_activation_display_phase. Returns0 after releasing the parent frame. Eight explicit incoming jumps/calls are preserved.
```

### 0x080a06a4 return_one_from_equip_activation_display_phase

新长度187；旧SHA256 `3a55a8cbea554455766e3a69c20d0b34c8911f505b1a640bff36b8016c4ced5b`；Function ID4538，body `[[080a06a4, 080a06a5]]`。

```text
Shared parent return entry. Set r0=1 and fall through to release_equip_activation_display_phase_frame. Returns1 after the common frame release. Five explicit incoming jumps are preserved.
```

### 0x080a06a6 release_equip_activation_display_phase_frame

新长度264；旧SHA256 `3661a33039b9ce408887fd92bf02f0a8bd04fd6d0befe0a7367c3dccb6d91cf2`；Function ID4539，body `[[080a06a6, 080a06b9]]`。

```text
Shared epilogue for run_equip_activation_display_phase_by_state_code. Preserve incoming r0, add0x298 to sp, restore r8-r10 and r4-r7, then return through the saved link register. The explicit incoming call is from return_zero; return_one reaches it by fallthrough.
```

### 0x080a06bc tick_equip_display_phase_by_state_code

新长度361；旧SHA256 `5898757ce90138458dd27480d30b76a950ce47cc8d62a8165a11a57ac723bb42`；Function ID16970，body `[[080a06bc, 080a06df] [080a06ec, 080a0705] [080a070c, 080a0779] [080a078c, 080a07f3] [080a0808, 080a0833]]`。

```text
No APCS inputs. Read player and display phase from gP1LifePoints. Phase0 enqueues side-specific sprite code3. Phase1 scans five monster slots for CID0x1740 and advances the phase. Phase2 compares timer/LP state, writes DISP_SET_VARIANT_OFF and LP_DISCARD_ZONE_OFF, and enqueues side-specific code4. All handled paths advance CARD_PLAY_PHASE_CTR_OFF and return0.
```

## carve计划 (R7)

把`asm/rom.s`现有`.incbin "roms/2343.gba", 0x1e477ac, 0x2560`替换为两张表和尾部incbin。表项必须按下列完整顺序输出，且保留空格形式`.word fn + 1`。

```asm
equip_activation_phase3_callbacks:
    .word scan_equip_zone_for_dimensionhole + 1    @ 0x09e477ac = 0x0809eaf1
    .word scan_monster_zone_slots_for_equip_activation_reserved_icid_g + 1    @ 0x09e477b0 = 0x0809eb55
    .word scan_monster_zone_for_equip_activation_spirit_of_the_breeze + 1    @ 0x09e477b4 = 0x0809ec05
    .word scan_monster_zone_for_equip_activation_dancing_fairy + 1    @ 0x09e477b8 = 0x0809ec15
    .word scan_monster_zone_for_equip_activation_cure_mermaid + 1    @ 0x09e477bc = 0x0809ec25
    .word scan_player_card_array_for_equip_activation_marie_the_fallen_one + 1    @ 0x09e477c0 = 0x0809ec35
    .word scan_trap_zone_for_equip_activation_life_absorbing_machine + 1    @ 0x09e477c4 = 0x0809ece1
    .word scan_monster_zone_for_equip_activation_white_magician_pikeru + 1    @ 0x09e477c8 = 0x0809ed01
    .word scan_monster_zone_for_equip_activation_princess_pikeru + 1    @ 0x09e477cc = 0x0809ed21
    .word scan_monster_zone_for_equip_activation_bowganian + 1    @ 0x09e477d0 = 0x0809ed41
    .word scan_all_zone_slots_for_equip_lp_indicator_graverobbers_retribution + 1    @ 0x09e477d4 = 0x0809ee15
    .word scan_trap_zone_for_equip_activation_mask_of_dispel + 1    @ 0x09e477d8 = 0x0809ef89
    .word scan_trap_zone_for_equip_activation_mask_of_accursed + 1    @ 0x09e477dc = 0x0809ef99
    .word scan_trap_zone_for_equip_activation_nightmare_wheel + 1    @ 0x09e477e0 = 0x0809efa9
    .word scan_trap_zone_for_equip_activation_ominous_fortunetelling + 1    @ 0x09e477e4 = 0x0809eac1
    .word scan_monster_zone_for_equip_activation_ebon_magician_curran + 1    @ 0x09e477e8 = 0x0809ed11
    .word scan_monster_zone_for_equip_activation_princess_curran + 1    @ 0x09e477ec = 0x0809ed31
    .word scan_monster_zone_for_equip_activation_reserved_icid_b + 1    @ 0x09e477f0 = 0x0809f86d
    .word scan_monster_zone_for_equip_activation_a_man_with_wdjat + 1    @ 0x09e477f4 = 0x0809f87d
    .word scan_monster_zone_for_equip_activation_reserved_icid_c + 1    @ 0x09e477f8 = 0x0809f88d
    .word scan_trap_zone_for_equip_activation_blind_destruction + 1    @ 0x09e477fc = 0x0809eab1
    .word scan_trap_zone_for_equip_activation_needle_wall + 1    @ 0x09e47800 = 0x0809ead1
    .word scan_trap_zone_for_equip_activation_dangerous_machine_type6 + 1    @ 0x09e47804 = 0x0809eae1
    .word scan_monster_zone_slots_for_equip_activation_mucus_yolk + 1    @ 0x09e47808 = 0x0809f349
    .word scan_monster_zone_for_equip_activation_legendary_fiend + 1    @ 0x09e4780c = 0x0809f40d
    .word scan_monster_zone_for_equip_activation_exodia_necross + 1    @ 0x09e47810 = 0x0809f41d
    .word scan_all_spell_trap_zone_slots_for_equip_activation_mirage_of_nightmare + 1    @ 0x09e47814 = 0x0809f745
    .word scan_monster_zone_for_equip_activation_agent_of_wisdom_mercury + 1    @ 0x09e47818 = 0x0809f43d
    .word scan_monster_zone_for_equip_activation_amazoness_blowpiper + 1    @ 0x09e4781c = 0x0809f42d
    .word scan_field_slots_for_lv_monster_equip_activation + 1    @ 0x09e47820 = 0x0809f44d
    .word scan_monster_zone_for_equip_activation_reserved_icid_a + 1    @ 0x09e47824 = 0x0809f85d
    .word scan_monster_zone_for_equip_activation_reserved_icid_f + 1    @ 0x09e47828 = 0x0809eb35
    .word scan_all_zone_slots_for_lp_indicator_burning_land + 1    @ 0x09e4782c = 0x0809eed9
    .word scan_monster_zone_for_equip_activation_lava_golem + 1    @ 0x09e47830 = 0x0809eb45
    .word scan_trap_slots_for_kiseitai_equip_chain_sprite + 1    @ 0x09e47834 = 0x0809f079
    .word scan_trap_zone_for_equip_activation_blast_sphere + 1    @ 0x09e47838 = 0x0809f031
    .word scan_trap_zone_for_equip_activation_adhesive_explosive + 1    @ 0x09e4783c = 0x0809f049
    .word scan_trap_zone_for_equip_activation_minor_goblin_official + 1    @ 0x09e47840 = 0x0809f019
    .word scan_monster_zone_for_equip_activation_malice_ascendant + 1    @ 0x09e47844 = 0x0809f061
    .word scan_trap_zone_for_equip_activation_snatch_steal + 1    @ 0x09e47848 = 0x0809efb9
    .word scan_trap_zone_for_equip_activation_brain_jacker + 1    @ 0x09e4784c = 0x0809efd1
    .word scan_trap_zone_for_equip_activation_the_eye_of_truth + 1    @ 0x09e47850 = 0x0809f001
    .word scan_trap_zone_for_equip_activation_falling_down + 1    @ 0x09e47854 = 0x0809efe9
    .word scan_equip_zone_for_equip_activation_vampire_lord + 1    @ 0x09e47858 = 0x0809f595
    .word scan_equip_zone_for_equip_activation_sacred_phoenix + 1    @ 0x09e4785c = 0x0809f5a5
    .word scan_equip_zone_for_equip_activation_revival_jam + 1    @ 0x09e47860 = 0x0809f585
    .word scan_equip_zone_for_entity_sprite_activation_curse_of_vampire + 1    @ 0x09e47864 = 0x0809f5b5
    .word scan_equip_zone_for_entity_sprite_activation_curse_of_vampire_opponent + 1    @ 0x09e47868 = 0x0809f5c5
    .word scan_trap_zone_for_equip_activation_jam_breeding_machine + 1    @ 0x09e4786c = 0x0809eaa1
    .word scan_all_monster_zone_slots_for_equip_activation_infernalqueen_archfiend + 1    @ 0x09e47870 = 0x0809ed51
    .word scan_spell_trap_zone_for_equip_activation_reserved_icid_e + 1    @ 0x09e47874 = 0x0809f705
    .word scan_spell_trap_zone_for_equip_activation_recycle + 1    @ 0x09e47878 = 0x0809f71d
    .word scan_monster_zone_for_equip_activation_aqua_spirit_opponent + 1    @ 0x09e4787c = 0x0809f72d
    .word scan_trap_zone_for_equip_activation_senri_eye + 1    @ 0x09e47880 = 0x0809ecf1
equip_activation_phase1_callbacks:
    .word scan_trap_zone_for_equip_bitmap_update_bottomless_shifting_sand + 1    @ 0x09e47884 = 0x0809f809
    .word scan_equip_zone_for_special_summon_activation_return_zombie + 1    @ 0x09e47888 = 0x0809f21d
    .word scan_player_card_array_for_equip_activation_sinister_serpent + 1    @ 0x09e4788c = 0x0809f1fd
    .word scan_player_card_array_for_equip_activation_treeborn_frog + 1    @ 0x09e47890 = 0x0809f20d
.incbin "roms/2343.gba", 0x1e47894, 0x2478
```

C7落地守卫：表头0x09e477ac/0x09e47884设USER_DEFINED主LABEL；54项原`/undefined *`及原DATA/DEFAULT odd refs全部保留，不升级source、不改偶Function主符号。4项表只在rom.s手工投影为4个`.word fn + 1`；Ghidra前两项原`/undefined4`且无outref、后两项原Data=None且无outref，全部保持，不创建Data或odd引用。只为表头和本段两个代码池建立已列USER标签/REF。rom.s手工`.word fn + 1`是导出真源，不修改全局exporter。

## disasm计划 (R4)

无。段内没有ROM_INCBIN/.byte；不设TMode、不clearListing、不createFunction、不调整任何Function body。

## 新增constants / 全局

全库按数值和用途扫描后新增17项；同值异域项不复用。

| 名称 | 值 | 文件 | 依据 |
| --- | ---: | --- | --- |
| EQUIP_ACTIVATION_UNMAPPED_CID_1147 | 0x00001147 | constants/card_info.inc | Unmapped internal CID; inverse table entry is 0xffff and no card-stat record exists. |
| EQUIP_ACTIVATION_UNMAPPED_CID_11EA | 0x000011ea | constants/card_info.inc | Unmapped internal CID; inverse table entry is 0xffff and no card-stat record exists. |
| EQUIP_ACTIVATION_UNMAPPED_CID_1282 | 0x00001282 | constants/card_info.inc | Unmapped internal CID; inverse table entry is 0xffff and no card-stat record exists. |
| EQUIP_ACTIVATION_UNMAPPED_CID_144A | 0x0000144a | constants/card_info.inc | Unmapped internal CID; inverse table entry is 0xffff and no card-stat record exists. |
| LIGHTFORCE_SWORD_CID | 0x000012c8 | constants/card_info.inc | Lightforce Sword; logical CID 650, password 49587034. |
| MASK_OF_BRUTALITY_CID | 0x000013f4 | constants/card_info.inc | Mask of Brutality; logical CID 865, password 82432018. |
| MIRAGE_OF_NIGHTMARE_CID | 0x00001539 | constants/card_info.inc | Mirage of Nightmare; logical CID 1118, password 41482598. |
| ARMOR_EXE_CID | 0x0000161b | constants/card_info.inc | Armor Exe; logical CID 1279, password 07180418. |
| OAM_EQUIP_SPRITE_P2_03 | 0x00008003 | constants/oam_attr.inc | Equip display sprite code 3 with player-side bit15 set. |
| OAM_EQUIP_SPRITE_P2_04 | 0x00008004 | constants/oam_attr.inc | Equip display sprite code 4 with player-side bit15 set. |
| OAM_EQUIP_SPRITE_P2_0D | 0x0000800d | constants/oam_attr.inc | Equip display sprite code 0x0d with player-side bit15 set. |
| LIGHTFORCE_SWORD_CHAIN_NODE_TAG | 0x000112c8 | constants/card_info.inc | Low-20-bit equip-chain node tag combining prefix 1 and LIGHTFORCE_SWORD_CID. |
| CHECK_SLOT_EQUIPPABLE_FOR_ACTIVE_PLAYER_THUMB_PTR | 0x0809f945 | constants/duel_field.inc | THUMB callback value check_slot_equippable_for_active_player+1. |
| CHECK_SLOT_EFFECT_VALID_FOR_ACTIVE_PLAYER_THUMB_PTR | 0x0809f98d | constants/duel_field.inc | THUMB callback value check_slot_effect_valid_for_active_player+1. |
| EQUIP_PHASE_FRAME_ALLOC_NEG_0X298 | 0xfffffd68 | constants/duel_field.inc | Signed -0x298 used by add sp in run_equip_activation_display_phase_by_state_code. |
| FIELD_SPELL_TO_ZONE_COUNT_DELTA_NEG_0X100 | 0xffffff00 | constants/duel_field.inc | Signed -0x100 converts gDuelFieldSpellZoneBase to the per-player zone-count base. |
| gEquipActivationScanCursor | 0x0201e204 | constants/ewram.inc | Absolute u32 cursor address equal to gP1LifePoints+EQUIP_ACTIVATION_SCAN_CURSOR_OFF and gDuelFieldSlots+FIELD_STATE_OFF. |

复用项按当前实际定义：

| 名称 | 值 | 定义 | 槽数 |
| --- | ---: | --- | ---: |
| A_MAN_WITH_WDJAT_CID | 0x0000158e | constants/card_info.inc:1590 | 1 |
| BATTLE_SCARRED_CID | 0x000016a2 | constants/card_info.inc:574 | 1 |
| CARD_PLAY_PHASE_CTR_OFF | 0x00001d1c | constants/ewram.inc:587 | 12 |
| CASTLE_OF_DARK_ILLUSIONS_CID | 0x00000ff9 | constants/card_info.inc:312 | 1 |
| DESROOK_ARCHFIEND_CID | 0x0000168f | constants/card_info.inc:817 | 1 |
| DIFFERENT_DIMENSION_CAPSULE_CID | 0x0000159c | constants/card_info.inc:739 | 1 |
| DISP_SET_VARIANT_OFF | 0x00001cfc | constants/duel_field.inc:253 | 1 |
| DUST_BARRIER_CID | 0x000017a1 | constants/card_info.inc:239 | 1 |
| ELIGIB_ANIM_STATE_OFF | 0x00001d6c | constants/ewram.inc:423 | 2 |
| ELIGIB_SPRITE_CTRL_OFF | 0x00001d68 | constants/ewram.inc:422 | 2 |
| EQUIP_ACTIVATION_SCAN_CURSOR_OFF | 0x00001d24 | constants/duel_field.inc:605 | 16 |
| EQUIP_NODE_TAG_MASK | 0x000fffff | constants/duel_field.inc:493 | 1 |
| FAIRY_BOX_CID | 0x000013f9 | constants/card_info.inc:1949 | 1 |
| LP_DELTA_6000 | 0x00001770 | constants/duel_field.inc:415 | 1 |
| LP_DISCARD_ZONE_OFF | 0x000010dc | constants/ewram.inc:390 | 1 |
| MIRROR_WALL_CID | 0x00001381 | constants/card_info.inc:321 | 2 |
| OAM_EQUIP_SET_SLOT_P2 | 0x0000803b | constants/oam_attr.inc:67 | 1 |
| P1LP_BLOCK2_OFF_1CE8 | 0x00001ce8 | constants/ewram.inc:276 | 4 |
| P1LP_TIMER_OFF | 0x00001cec | constants/ewram.inc:244 | 4 |
| P2LP_BLOCK2_OFF_1CF4 | 0x00001cf4 | constants/ewram.inc:277 | 1 |
| PLAYER_BLOCK_STRIDE | 0x00000868 | constants/ewram.inc:251 | 17 |
| SKULL_ARCHFIEND_OF_LIGHTNING_CID | 0x00001692 | constants/card_info.inc:669 | 1 |
| SOLOMONS_LAWBOOK_CID | 0x0000137e | constants/card_info.inc:799 | 1 |
| STIM_PACK_CID | 0x0000131a | constants/card_info.inc:725 | 1 |
| SWORDS_OF_CONCEALING_LIGHT_CID | 0x0000187c | constants/card_info.inc:760 | 1 |
| TERRORKING_ARCHFIEND_CID | 0x00001691 | constants/card_info.inc:967 | 1 |
| TOKEN_1639_CID | 0x00001639 | constants/card_info.inc:1463 | 2 |
| VILEPAWN_ARCHFIEND_CID | 0x0000168c | constants/card_info.inc:183 | 1 |
| VISER_DES_CID | 0x000014ac | constants/card_info.inc:1584 | 1 |
| WAVE_MOTION_CANNON_CID | 0x000015ee | constants/card_info.inc:1100 | 1 |

CID证据使用data.md逻辑CID列，不用全行首次数字命中。32个本段/派生CID候选均交叉核对inverse table、cards-ids-array.s、card-stats.s和password；4个unmapped值的inverse为0xffff且无stat记录，TOKEN_1639走独立token记录。详见`f13-seg3-cid-proof.json`。

## §5.1登记 (Rule 3)

无。段内裸块为0；两张外部依赖表均有直接raw引用并已进入carve。

## 消费者证据 (R6)

下表逐槽列出机器解码LDR源地址/当前源行和动作；用途全文与前态对象在plan。

| slot / old label / value | action | LDR source(s) | EOL |
| --- | --- | --- | --- |
| 0x0809f7dc / PTR_gP1LifePoints_0809f7dc / 0x0201c4e0 | RENAME gP1LifePoints | 0x0809f750 asm/13_equip_placement.s:4354 | gP1LifePoints base; preserve the existing DATA reference and its source. |
| 0x0809f7e0 / DAT_0809f7e0 / 0x00001d24 | EQ EQUIP_ACTIVATION_SCAN_CURSOR_OFF | 0x0809f752 asm/13_equip_placement.s:4355 | Byte offset from gP1LifePoints to the shared activation scan cursor. |
| 0x0809f7e4 / DAT_0809f7e4 / 0x00000868 | EQ PLAYER_BLOCK_STRIDE | 0x0809f788 asm/13_equip_placement.s:4381 | Byte stride between the two player state blocks. |
| 0x0809f7e8 / DAT_0809f7e8 / 0x00001539 | EQ MIRAGE_OF_NIGHTMARE_CID | 0x0809f79c asm/13_equip_placement.s:4391 | Internal CID 0x1539 for Mirage of Nightmare; card mapping and password cross-check are recorded. |
| 0x0809f844 / PTR_gP1LifePoints_0809f844 / 0x0201c4e0 | RENAME gP1LifePoints | 0x0809f80c asm/13_equip_placement.s:4451 | gP1LifePoints base; preserve the existing DATA reference and its source. |
| 0x0809f848 / DAT_0809f848 / 0x00000868 | EQ PLAYER_BLOCK_STRIDE | 0x0809f812 asm/13_equip_placement.s:4454 | Byte stride between the two player state blocks. |
| 0x0809f868 / DAT_0809f868 / 0x00001282 | EQ EQUIP_ACTIVATION_UNMAPPED_CID_1282 | 0x0809f85e asm/13_equip_placement.s:4497 | Unmapped internal CID 0x1282; inverse table is 0xffff and no card-stat record exists. |
| 0x0809f878 / DAT_0809f878 / 0x000011ea | EQ EQUIP_ACTIVATION_UNMAPPED_CID_11EA | 0x0809f86e asm/13_equip_placement.s:4507 | Unmapped internal CID 0x11ea; inverse table is 0xffff and no card-stat record exists. |
| 0x0809f888 / DAT_0809f888 / 0x0000158e | EQ A_MAN_WITH_WDJAT_CID | 0x0809f87e asm/13_equip_placement.s:4517 | Internal CID 0x158e for A Man with Wdjat; card mapping and password cross-check are recorded. |
| 0x0809f898 / DAT_0809f898 / 0x00001147 | EQ EQUIP_ACTIVATION_UNMAPPED_CID_1147 | 0x0809f88e asm/13_equip_placement.s:4527 | Unmapped internal CID 0x1147; inverse table is 0xffff and no card-stat record exists. |
| 0x0809f8c0 / DAT_0809f8c0 / 0x0000168c | EQ VILEPAWN_ARCHFIEND_CID | 0x0809f89e asm/13_equip_placement.s:4537 | Internal CID 0x168c for Vilepawn Archfiend; card mapping and password cross-check are recorded. |
| 0x0809f8c4 / DAT_0809f8c4 / 0x00001381 | EQ MIRROR_WALL_CID | 0x0809f8a8 asm/13_equip_placement.s:4542 | Internal CID 0x1381 for Mirror Wall; card mapping and password cross-check are recorded. |
| 0x0809f8d8 / DAT_0809f8d8 / 0x000013f9 | EQ FAIRY_BOX_CID | 0x0809f8c8 asm/13_equip_placement.s:4559 | Internal CID 0x13f9 for Fairy Box; card mapping and password cross-check are recorded. |
| 0x0809f8e4 / DAT_0809f8e4 / 0x00001639 | EQ TOKEN_1639_CID | 0x0809f8dc asm/13_equip_placement.s:4570 | Special token CID 0x1639; inverse index 2090 has no ordinary card-stat record. |
| 0x0809f8fc / DAT_0809f8fc / 0x0000168f | EQ DESROOK_ARCHFIEND_CID | 0x0809f8e8 asm/13_equip_placement.s:4578 | Internal CID 0x168f for Desrook Archfiend; card mapping and password cross-check are recorded. |
| 0x0809f914 / DAT_0809f914 / 0x00001691 | EQ TERRORKING_ARCHFIEND_CID | 0x0809f900 asm/13_equip_placement.s:4591 | Internal CID 0x1691 for Terrorking Archfiend; card mapping and password cross-check are recorded. |
| 0x0809f978 / PTR_gP1LifePoints_0809f978 / 0x0201c4e0 | RENAME gP1LifePoints | 0x0809f94e asm/13_equip_placement.s:4650 | gP1LifePoints base; preserve the existing DATA reference and its source. |
| 0x0809f97c / DAT_0809f97c / 0x00001ce8 | EQ P1LP_BLOCK2_OFF_1CE8 | 0x0809f950 asm/13_equip_placement.s:4651 | Byte offset from gP1LifePoints to the active-player selector word. |
| 0x0809f980 / DAT_0809f980 / 0x00001d24 | EQ EQUIP_ACTIVATION_SCAN_CURSOR_OFF | 0x0809f968 asm/13_equip_placement.s:4662 | Byte offset from gP1LifePoints to the shared activation scan cursor. |
| 0x0809f9bc / PTR_gP1LifePoints_0809f9bc / 0x0201c4e0 | RENAME gP1LifePoints | 0x0809f996 asm/13_equip_placement.s:4695 | gP1LifePoints base; preserve the existing DATA reference and its source. |
| 0x0809f9c0 / DAT_0809f9c0 / 0x00001ce8 | EQ P1LP_BLOCK2_OFF_1CE8 | 0x0809f998 asm/13_equip_placement.s:4696 | Byte offset from gP1LifePoints to the active-player selector word. |
| 0x0809fa48 / DAT_0809fa48 / 0xfffffd68 | EQ EQUIP_PHASE_FRAME_ALLOC_NEG_0X298 | 0x0809f9d6 asm/13_equip_placement.s:4732 | Signed frame allocation used by add sp. |
| 0x0809fa4c / PTR_gP1LifePoints_0809fa4c / 0x0201c4e0 | RENAME gP1LifePoints | 0x0809f9da asm/13_equip_placement.s:4734, 0x0809fa14 asm/13_equip_placement.s:4764 | gP1LifePoints base; preserve the existing DATA reference and its source. |
| 0x0809fa50 / DAT_0809fa50 / 0x00001ce8 | EQ P1LP_BLOCK2_OFF_1CE8 | 0x0809f9dc asm/13_equip_placement.s:4735 | Byte offset from gP1LifePoints to the active-player selector word. |
| 0x0809fa54 / DAT_0809fa54 / 0x00000868 | EQ PLAYER_BLOCK_STRIDE | 0x0809f9e8 asm/13_equip_placement.s:4741 | Byte stride between the two player state blocks. |
| 0x0809fa58 / DAT_0809fa58 / 0x0000137e | EQ SOLOMONS_LAWBOOK_CID | 0x0809fa02 asm/13_equip_placement.s:4754 | Internal CID 0x137e for Solomon's Lawbook; card mapping and password cross-check are recorded. |
| 0x0809fa5c / DAT_0809fa5c / 0x00001d1c | EQ CARD_PLAY_PHASE_CTR_OFF | 0x0809fa16 asm/13_equip_placement.s:4765 | Byte offset from gP1LifePoints to the equip display phase word. |
| 0x0809fae4 / PTR_gP1LifePoints_0809fae4 / 0x0201c4e0 | RENAME gP1LifePoints | 0x0809fada asm/13_equip_placement.s:4875 | gP1LifePoints base; preserve the existing DATA reference and its source. |
| 0x0809fae8 / DAT_0809fae8 / 0x00001d1c | EQ CARD_PLAY_PHASE_CTR_OFF | 0x0809fadc asm/13_equip_placement.s:4876 | Byte offset from gP1LifePoints to the equip display phase word. |
| 0x0809fb1c / DWORD_0809fb1c / 0x0000800d | EQ OAM_EQUIP_SPRITE_P2_0D | 0x0809faf4 asm/13_equip_placement.s:4889 | Player-side sprite code 0x0d with bit15 set. |
| 0x0809fb20 / DWORD_0809fb20 / 0x00001d24 | EQ EQUIP_ACTIVATION_SCAN_CURSOR_OFF | 0x0809fb10 asm/13_equip_placement.s:4903 | Byte offset from gP1LifePoints to the shared activation scan cursor. |
| 0x0809fb84 / DAT_0809fb84 / 0x09e47884 | REF equip_activation_phase1_callbacks | 0x0809fb26 asm/13_equip_placement.s:4917 | Base of the 4-entry phase-1 THUMB callback table. |
| 0x0809fb88 / PTR_gP1LifePoints_0809fb88 / 0x0201c4e0 | RENAME gP1LifePoints | 0x0809fb3c asm/13_equip_placement.s:4928, 0x0809fb74 asm/13_equip_placement.s:4957 | gP1LifePoints base; preserve the existing DATA reference and its source. |
| 0x0809fb8c / DAT_0809fb8c / 0x09e477ac | REF equip_activation_phase3_callbacks | 0x0809fb4a asm/13_equip_placement.s:4935 | Base of the 54-entry phase-3 THUMB callback table. |
| 0x0809fb90 / DAT_0809fb90 / 0x00001d24 | EQ EQUIP_ACTIVATION_SCAN_CURSOR_OFF | 0x0809fb50 asm/13_equip_placement.s:4938 | Byte offset from gP1LifePoints to the shared activation scan cursor. |
| 0x0809fb94 / DAT_0809fb94 / 0x00001d1c | EQ CARD_PLAY_PHASE_CTR_OFF | 0x0809fb76 asm/13_equip_placement.s:4958 | Byte offset from gP1LifePoints to the equip display phase word. |
| 0x0809fbcc / DAT_0809fbcc / 0x09e47884 | REF equip_activation_phase1_callbacks | 0x0809fba8 asm/13_equip_placement.s:4983 | Base of the 4-entry phase-1 THUMB callback table. |
| 0x0809fbd0 / PTR_gP1LifePoints_0809fbd0 / 0x0201c4e0 | RENAME gP1LifePoints | 0x0809fbbe asm/13_equip_placement.s:4994 | gP1LifePoints base; preserve the existing DATA reference and its source. |
| 0x0809fbd4 / DAT_0809fbd4 / 0x00001d1c | EQ CARD_PLAY_PHASE_CTR_OFF | 0x0809fbc0 asm/13_equip_placement.s:4995 | Byte offset from gP1LifePoints to the equip display phase word. |
| 0x0809fc74 / DAT_0809fc74 / 0x00001d24 | EQ EQUIP_ACTIVATION_SCAN_CURSOR_OFF | 0x0809fbe2 asm/13_equip_placement.s:5014, 0x0809fbfc asm/13_equip_placement.s:5029 | Byte offset from gP1LifePoints to the shared activation scan cursor. |
| 0x0809fc78 / PTR_gP1LifePoints_0809fc78 / 0x0201c4e0 | RENAME gP1LifePoints | 0x0809fbec asm/13_equip_placement.s:5020, 0x0809fc1a asm/13_equip_placement.s:5046, 0x0809fc20 asm/13_equip_placement.s:5050 | gP1LifePoints base; preserve the existing DATA reference and its source. |
| 0x0809fc7c / DAT_0809fc7c / 0x00000868 | EQ PLAYER_BLOCK_STRIDE | 0x0809fc12 asm/13_equip_placement.s:5042, 0x0809fc3e asm/13_equip_placement.s:5065 | Byte stride between the two player state blocks. |
| 0x0809fc80 / DAT_0809fc80 / 0x0201c510 | REF gDuelFieldSlots | 0x0809fc44 asm/13_equip_placement.s:5068 | Field-slot array base; consumers add player stride and 20-byte slot offsets. |
| 0x0809fca4 / DAT_0809fca4 / 0x000013f4 | EQ MASK_OF_BRUTALITY_CID | 0x0809fc8a asm/13_equip_placement.s:5107 | Internal CID 0x13f4 for Mask of Brutality; card mapping and password cross-check are recorded. |
| 0x0809fcc4 / DAT_0809fcc4 / 0x0000144a | EQ EQUIP_ACTIVATION_UNMAPPED_CID_144A | 0x0809fcb4 asm/13_equip_placement.s:5130 | Unmapped internal CID 0x144a; inverse table is 0xffff and no card-stat record exists. |
| 0x0809fcd8 / DAT_0809fcd8 / 0x0000161b | EQ ARMOR_EXE_CID | 0x0809fcc8 asm/13_equip_placement.s:5141 | Internal CID 0x161b for Armor Exe; card mapping and password cross-check are recorded. |
| 0x0809fd20 / DAT_0809fd20 / 0x0201c510 | REF gDuelFieldSlots | 0x0809fce8 asm/13_equip_placement.s:5159 | Field-slot array base; consumers add player stride and 20-byte slot offsets. |
| 0x0809fd64 / DAT_0809fd64 / 0x0201c510 | REF gDuelFieldSlots | 0x0809fd30 asm/13_equip_placement.s:5194 | Field-slot array base; consumers add player stride and 20-byte slot offsets. |
| 0x0809fd68 / DAT_0809fd68 / 0x00001cec | EQ P1LP_TIMER_OFF | 0x0809fd58 asm/13_equip_placement.s:5212 | Byte offset from gP1LifePoints to the duel display timer word. |
| 0x0809fdac / DAT_0809fdac / 0x00000868 | EQ PLAYER_BLOCK_STRIDE | 0x0809fd78 asm/13_equip_placement.s:5228 | Byte stride between the two player state blocks. |
| 0x0809fdb0 / DAT_0809fdb0 / 0x0201c510 | REF gDuelFieldSlots | 0x0809fd7e asm/13_equip_placement.s:5231 | Field-slot array base; consumers add player stride and 20-byte slot offsets. |
| 0x0809fdb4 / DAT_0809fdb4 / 0x00001cec | EQ P1LP_TIMER_OFF | 0x0809fda2 asm/13_equip_placement.s:5247 | Byte offset from gP1LifePoints to the duel display timer word. |
| 0x0809fe00 / PTR_gP1LifePoints_0809fe00 / 0x0201c4e0 | RENAME gP1LifePoints | 0x0809fddc asm/13_equip_placement.s:5278, 0x0809fdf0 asm/13_equip_placement.s:5289 | gP1LifePoints base; preserve the existing DATA reference and its source. |
| 0x0809fe04 / DAT_0809fe04 / 0x00001d1c | EQ CARD_PLAY_PHASE_CTR_OFF | 0x0809fdf2 asm/13_equip_placement.s:5290 | Byte offset from gP1LifePoints to the equip display phase word. |
| 0x0809fe5c / DAT_0809fe5c / 0x00001d24 | EQ EQUIP_ACTIVATION_SCAN_CURSOR_OFF | 0x0809fe08 asm/13_equip_placement.s:5301 | Byte offset from gP1LifePoints to the shared activation scan cursor. |
| 0x0809fe60 / DAT_0809fe60 / 0x0201e204 | REF gEquipActivationScanCursor | 0x0809fe1c asm/13_equip_placement.s:5313 | Absolute u32 shared equip activation scan cursor. |
| 0x0809fe64 / DAT_0809fe64 / 0x00000868 | EQ PLAYER_BLOCK_STRIDE | 0x0809fe26 asm/13_equip_placement.s:5318 | Byte stride between the two player state blocks. |
| 0x0809fe68 / DAT_0809fe68 / 0x0201c510 | REF gDuelFieldSlots | 0x0809fe2e asm/13_equip_placement.s:5322 | Field-slot array base; consumers add player stride and 20-byte slot offsets. |
| 0x0809ff5c / DAT_0809ff5c / 0x00001692 | EQ SKULL_ARCHFIEND_OF_LIGHTNING_CID | 0x0809fe72 asm/13_equip_placement.s:5360 | Internal CID 0x1692 for Skull Archfiend of Lightning; card mapping and password cross-check are recorded. |
| 0x0809ff60 / DAT_0809ff60 / 0x00000868 | EQ PLAYER_BLOCK_STRIDE | 0x0809fe96 asm/13_equip_placement.s:5377, 0x0809fefc asm/13_equip_placement.s:5423, 0x0809ff2a asm/13_equip_placement.s:5445 | Byte stride between the two player state blocks. |
| 0x0809ff64 / DAT_0809ff64 / 0x0201c510 | REF gDuelFieldSlots | 0x0809fe9e asm/13_equip_placement.s:5381 | Field-slot array base; consumers add player stride and 20-byte slot offsets. |
| 0x0809ff68 / DAT_0809ff68 / 0x00001cf4 | EQ P2LP_BLOCK2_OFF_1CF4 | 0x0809fede asm/13_equip_placement.s:5409 | Byte offset from gP1LifePoints to the paired LP/display state word. |
| 0x0809ff6c / DAT_0809ff6c / 0x000016a2 | EQ BATTLE_SCARRED_CID | 0x0809fee6 asm/13_equip_placement.s:5413, 0x0809ff1c asm/13_equip_placement.s:5439 | Internal CID 0x16a2 for Battle-Scarred; card mapping and password cross-check are recorded. |
| 0x0809ff70 / PTR_gP1LifePoints_0809ff70 / 0x0201c4e0 | RENAME gP1LifePoints | 0x0809ff10 asm/13_equip_placement.s:5433 | gP1LifePoints base; preserve the existing DATA reference and its source. |
| 0x0809ff74 / DAT_0809ff74 / 0x0201e204 | REF gEquipActivationScanCursor | 0x0809ff12 asm/13_equip_placement.s:5434, 0x0809ff52 asm/13_equip_placement.s:5465 | Absolute u32 shared equip activation scan cursor. |
| 0x0809ff90 / DAT_0809ff90 / 0x0201e204 | REF gEquipActivationScanCursor | 0x0809ff78 asm/13_equip_placement.s:5485 | Absolute u32 shared equip activation scan cursor. |
| 0x0809ff94 / PTR_gP1LifePoints_0809ff94 / 0x0201c4e0 | RENAME gP1LifePoints | 0x0809ff86 asm/13_equip_placement.s:5493 | gP1LifePoints base; preserve the existing DATA reference and its source. |
| 0x0809ff98 / DAT_0809ff98 / 0x00001d1c | EQ CARD_PLAY_PHASE_CTR_OFF | 0x0809ff88 asm/13_equip_placement.s:5494 | Byte offset from gP1LifePoints to the equip display phase word. |
| 0x0809ffe8 / DAT_0809ffe8 / 0x00001d24 | EQ EQUIP_ACTIVATION_SCAN_CURSOR_OFF | 0x0809ffa2 asm/13_equip_placement.s:5508 | Byte offset from gP1LifePoints to the shared activation scan cursor. |
| 0x0809ffec / DAT_0809ffec / 0x00000868 | EQ PLAYER_BLOCK_STRIDE | 0x0809ffae asm/13_equip_placement.s:5514 | Byte stride between the two player state blocks. |
| 0x0809fff0 / DAT_0809fff0 / 0x0201e2a0 | REF gDuelCardCtxBase | 0x0809ffc0 asm/13_equip_placement.s:5523 | Duel card activation context base. |
| 0x0809fff4 / DAT_0809fff4 / 0x00001381 | EQ MIRROR_WALL_CID | 0x0809ffd6 asm/13_equip_placement.s:5534 | Internal CID 0x1381 for Mirror Wall; card mapping and password cross-check are recorded. |
| 0x080a0000 / DAT_080a0000 / 0x00001639 | EQ TOKEN_1639_CID | 0x0809fff8 asm/13_equip_placement.s:5552 | Special token CID 0x1639; inverse index 2090 has no ordinary card-stat record. |
| 0x080a0018 / DAT_080a0018 / 0x00001770 | EQ LP_DELTA_6000 | 0x080a000a asm/13_equip_placement.s:5562 | LP threshold value 6000; this consumer compares an LP word, not a CID. |
| 0x080a0084 / PTR_gP1LifePoints_080a0084 / 0x0201c4e0 | RENAME gP1LifePoints | 0x080a0040 asm/13_equip_placement.s:5592 | gP1LifePoints base; preserve the existing DATA reference and its source. |
| 0x080a0088 / DAT_080a0088 / 0x00001d24 | EQ EQUIP_ACTIVATION_SCAN_CURSOR_OFF | 0x080a0042 asm/13_equip_placement.s:5593 | Byte offset from gP1LifePoints to the shared activation scan cursor. |
| 0x080a008c / DAT_080a008c / 0x00000868 | EQ PLAYER_BLOCK_STRIDE | 0x080a004e asm/13_equip_placement.s:5599 | Byte stride between the two player state blocks. |
| 0x080a00c4 / PTR_gP1LifePoints_080a00c4 / 0x0201c4e0 | RENAME gP1LifePoints | 0x080a00b8 asm/13_equip_placement.s:5649 | gP1LifePoints base; preserve the existing DATA reference and its source. |
| 0x080a00c8 / DAT_080a00c8 / 0x00001d1c | EQ CARD_PLAY_PHASE_CTR_OFF | 0x080a00ba asm/13_equip_placement.s:5650 | Byte offset from gP1LifePoints to the equip display phase word. |
| 0x080a010c / DAT_080a010c / 0x00001d24 | EQ EQUIP_ACTIVATION_SCAN_CURSOR_OFF | 0x080a00de asm/13_equip_placement.s:5669 | Byte offset from gP1LifePoints to the shared activation scan cursor. |
| 0x080a0110 / DAT_080a0110 / 0x00000868 | EQ PLAYER_BLOCK_STRIDE | 0x080a00ea asm/13_equip_placement.s:5675 | Byte stride between the two player state blocks. |
| 0x080a0138 / DAT_080a0138 / 0x00001d24 | EQ EQUIP_ACTIVATION_SCAN_CURSOR_OFF | 0x080a0114 asm/13_equip_placement.s:5695, 0x080a0126 asm/13_equip_placement.s:5704 | Byte offset from gP1LifePoints to the shared activation scan cursor. |
| 0x080a013c / PTR_gP1LifePoints_080a013c / 0x0201c4e0 | RENAME gP1LifePoints | 0x080a0124 asm/13_equip_placement.s:5703 | gP1LifePoints base; preserve the existing DATA reference and its source. |
| 0x080a0140 / DAT_080a0140 / 0x00001d1c | EQ CARD_PLAY_PHASE_CTR_OFF | 0x080a0130 asm/13_equip_placement.s:5709 | Byte offset from gP1LifePoints to the equip display phase word. |
| 0x080a0164 / DAT_080a0164 / 0x0201e2a0 | REF gDuelCardCtxBase | 0x080a0144 asm/13_equip_placement.s:5720 | Duel card activation context base. |
| 0x080a01ac / DAT_080a01ac / 0x00001d24 | EQ EQUIP_ACTIVATION_SCAN_CURSOR_OFF | 0x080a0170 asm/13_equip_placement.s:5743 | Byte offset from gP1LifePoints to the shared activation scan cursor. |
| 0x080a01b0 / DAT_080a01b0 / 0x00000868 | EQ PLAYER_BLOCK_STRIDE | 0x080a017c asm/13_equip_placement.s:5749 | Byte stride between the two player state blocks. |
| 0x080a01c8 / DAT_080a01c8 / 0x0809f945 | EQ CHECK_SLOT_EQUIPPABLE_FOR_ACTIVE_PLAYER_THUMB_PTR | 0x080a01c4 asm/13_equip_placement.s:5783 | Stored THUMB callback value; the auxiliary reference targets the even Function entry. |
| 0x080a01e8 / DAT_080a01e8 / 0x00001d24 | EQ EQUIP_ACTIVATION_SCAN_CURSOR_OFF | 0x080a01cc asm/13_equip_placement.s:5788 | Byte offset from gP1LifePoints to the shared activation scan cursor. |
| 0x080a021c / DAT_080a021c / 0x00001d68 | EQ ELIGIB_SPRITE_CTRL_OFF | 0x080a01f4 asm/13_equip_placement.s:5807 | Byte offset from gP1LifePoints to the eligibility sprite-control word. |
| 0x080a0220 / DAT_080a0220 / 0x00001d6c | EQ ELIGIB_ANIM_STATE_OFF | 0x080a01fa asm/13_equip_placement.s:5810 | Byte offset from gP1LifePoints to the eligibility animation-state word. |
| 0x080a0224 / DAT_080a0224 / 0x00001d24 | EQ EQUIP_ACTIVATION_SCAN_CURSOR_OFF | 0x080a020c asm/13_equip_placement.s:5818 | Byte offset from gP1LifePoints to the shared activation scan cursor. |
| 0x080a0254 / DAT_080a0254 / 0x0201e2a0 | REF gDuelCardCtxBase | 0x080a0238 asm/13_equip_placement.s:5842 | Duel card activation context base. |
| 0x080a0298 / DAT_080a0298 / 0x00001d24 | EQ EQUIP_ACTIVATION_SCAN_CURSOR_OFF | 0x080a025c asm/13_equip_placement.s:5861 | Byte offset from gP1LifePoints to the shared activation scan cursor. |
| 0x080a029c / DAT_080a029c / 0x00000868 | EQ PLAYER_BLOCK_STRIDE | 0x080a0268 asm/13_equip_placement.s:5867 | Byte stride between the two player state blocks. |
| 0x080a02b8 / DAT_080a02b8 / 0x0809f98d | EQ CHECK_SLOT_EFFECT_VALID_FOR_ACTIVE_PLAYER_THUMB_PTR | 0x080a02b0 asm/13_equip_placement.s:5903 | Stored THUMB callback value; the auxiliary reference targets the even Function entry. |
| 0x080a02e4 / DAT_080a02e4 / 0x00001d24 | EQ EQUIP_ACTIVATION_SCAN_CURSOR_OFF | 0x080a02ca asm/13_equip_placement.s:5917 | Byte offset from gP1LifePoints to the shared activation scan cursor. |
| 0x080a031c / DAT_080a031c / 0x00001d68 | EQ ELIGIB_SPRITE_CTRL_OFF | 0x080a02f0 asm/13_equip_placement.s:5938 | Byte offset from gP1LifePoints to the eligibility sprite-control word. |
| 0x080a0320 / DAT_080a0320 / 0x00001d6c | EQ ELIGIB_ANIM_STATE_OFF | 0x080a02f6 asm/13_equip_placement.s:5941 | Byte offset from gP1LifePoints to the eligibility animation-state word. |
| 0x080a0324 / DAT_080a0324 / 0x00001d24 | EQ EQUIP_ACTIVATION_SCAN_CURSOR_OFF | 0x080a030c asm/13_equip_placement.s:5951 | Byte offset from gP1LifePoints to the shared activation scan cursor. |
| 0x080a0368 / DAT_080a0368 / 0x00000868 | EQ PLAYER_BLOCK_STRIDE | 0x080a033e asm/13_equip_placement.s:5983 | Byte stride between the two player state blocks. |
| 0x080a036c / DAT_080a036c / 0x0201c510 | REF gDuelFieldSlots | 0x080a0346 asm/13_equip_placement.s:5988 | Field-slot array base; consumers add player stride and 20-byte slot offsets. |
| 0x080a0370 / DAT_080a0370 / 0x00000ff9 | EQ CASTLE_OF_DARK_ILLUSIONS_CID | 0x080a035a asm/13_equip_placement.s:5998 | Internal CID 0x0ff9 for Castle of Dark Illusions; card mapping and password cross-check are recorded. |
| 0x080a0374 / DAT_080a0374 / 0x000014ac | EQ VISER_DES_CID | 0x080a0360 asm/13_equip_placement.s:6001 | Internal CID 0x14ac for Viser Des; card mapping and password cross-check are recorded. |
| 0x080a03f4 / DAT_080a03f4 / 0x00000868 | EQ PLAYER_BLOCK_STRIDE | 0x080a03a6 asm/13_equip_placement.s:6036 | Byte stride between the two player state blocks. |
| 0x080a03f8 / DAT_080a03f8 / 0x0201c510 | REF gDuelFieldSlots | 0x080a03ae asm/13_equip_placement.s:6040 | Field-slot array base; consumers add player stride and 20-byte slot offsets. |
| 0x080a03fc / DAT_080a03fc / 0x0000131a | EQ STIM_PACK_CID | 0x080a03e2 asm/13_equip_placement.s:6070 | Internal CID 0x131a for Stim-Pack; card mapping and password cross-check are recorded. |
| 0x080a0408 / DAT_080a0408 / 0x0000159c | EQ DIFFERENT_DIMENSION_CAPSULE_CID | 0x080a0400 asm/13_equip_placement.s:6087 | Internal CID 0x159c for Different Dimension Capsule; card mapping and password cross-check are recorded. |
| 0x080a0424 / DAT_080a0424 / 0x000017a1 | EQ DUST_BARRIER_CID | 0x080a040c asm/13_equip_placement.s:6094 | Internal CID 0x17a1 for Dust Barrier; card mapping and password cross-check are recorded. |
| 0x080a0428 / DAT_080a0428 / 0x000015ee | EQ WAVE_MOTION_CANNON_CID | 0x080a0418 asm/13_equip_placement.s:6101 | Internal CID 0x15ee for Wave-Motion Cannon; card mapping and password cross-check are recorded. |
| 0x080a0438 / DAT_080a0438 / 0x0000187c | EQ SWORDS_OF_CONCEALING_LIGHT_CID | 0x080a042c asm/13_equip_placement.s:6114 | Internal CID 0x187c for Swords of Concealing Light; card mapping and password cross-check are recorded. |
| 0x080a066c / DAT_080a066c / 0x000012c8 | EQ LIGHTFORCE_SWORD_CID | 0x080a059a asm/13_equip_placement.s:6290, 0x080a05f0 asm/13_equip_placement.s:6334 | Internal CID 0x12c8 for Lightforce Sword; card mapping and password cross-check are recorded. |
| 0x080a0670 / DAT_080a0670 / 0x00000868 | EQ PLAYER_BLOCK_STRIDE | 0x080a05ae asm/13_equip_placement.s:6299, 0x080a0640 asm/13_equip_placement.s:6371 | Byte stride between the two player state blocks. |
| 0x080a0674 / DAT_080a0674 / 0x0201c5ec | REF gDuelFieldSpellZoneBase | 0x080a05b2 asm/13_equip_placement.s:6301 | Field-spell slot base; this consumer derives the zone-count base with -0x100. |
| 0x080a0678 / DAT_080a0678 / 0xffffff00 | EQ FIELD_SPELL_TO_ZONE_COUNT_DELTA_NEG_0X100 | 0x080a05c2 asm/13_equip_placement.s:6309 | Signed delta from gDuelFieldSpellZoneBase to the per-player zone-count base. |
| 0x080a067c / DAT_080a067c / 0x0201d9c0 | REF gEquipNodePool | 0x080a05ca asm/13_equip_placement.s:6314 | Equip-chain node pool base; entries use an 8-byte stride. |
| 0x080a0680 / DAT_080a0680 / 0x000fffff | EQ EQUIP_NODE_TAG_MASK | 0x080a05d4 asm/13_equip_placement.s:6319 | Mask selecting the low 20-bit equip-chain node tag. |
| 0x080a0684 / DAT_080a0684 / 0x000112c8 | EQ LIGHTFORCE_SWORD_CHAIN_NODE_TAG | 0x080a05d8 asm/13_equip_placement.s:6321 | Equip-chain node low-20-bit tag for Lightforce Sword. |
| 0x080a0688 / DAT_080a0688 / 0x0000803b | EQ OAM_EQUIP_SET_SLOT_P2 | 0x080a05ee asm/13_equip_placement.s:6332 | Player-side equip set-slot sprite code. |
| 0x080a068c / PTR_gP1LifePoints_080a068c / 0x0201c4e0 | RENAME gP1LifePoints | 0x080a065e asm/13_equip_placement.s:6387 | gP1LifePoints base; preserve the existing DATA reference and its source. |
| 0x080a0690 / DAT_080a0690 / 0x00001d1c | EQ CARD_PLAY_PHASE_CTR_OFF | 0x080a0660 asm/13_equip_placement.s:6388 | Byte offset from gP1LifePoints to the equip display phase word. |
| 0x080a06a0 / DAT_080a06a0 / 0x00001cec | EQ P1LP_TIMER_OFF | 0x080a0694 asm/13_equip_placement.s:6417 | Byte offset from gP1LifePoints to the duel display timer word. |
| 0x080a06e0 / DWORD_080a06e0 / 0x0201c4e0 | RENAME gP1LifePoints | 0x080a06c4 asm/13_equip_placement.s:6453 | gP1LifePoints base; preserve the existing DATA reference and its source. |
| 0x080a06e4 / DWORD_080a06e4 / 0x00001ce8 | EQ P1LP_BLOCK2_OFF_1CE8 | 0x080a06c6 asm/13_equip_placement.s:6454 | Byte offset from gP1LifePoints to the active-player selector word. |
| 0x080a06e8 / DWORD_080a06e8 / 0x00001d1c | EQ CARD_PLAY_PHASE_CTR_OFF | 0x080a06cc asm/13_equip_placement.s:6457 | Byte offset from gP1LifePoints to the equip display phase word. |
| 0x080a0708 / DWORD_080a0708 / 0x00008003 | EQ OAM_EQUIP_SPRITE_P2_03 | 0x080a06f2 asm/13_equip_placement.s:6477 | Player-side sprite code 3 with bit15 set. |
| 0x080a077c / DWORD_080a077c / 0x00000868 | EQ PLAYER_BLOCK_STRIDE | 0x080a0710 asm/13_equip_placement.s:6493 | Byte stride between the two player state blocks. |
| 0x080a0780 / DWORD_080a0780 / 0x0201c510 | REF gDuelFieldSlots | 0x080a072a asm/13_equip_placement.s:6507 | Field-slot array base; consumers add player stride and 20-byte slot offsets. |
| 0x080a0784 / DWORD_080a0784 / 0x0201c4e0 | RENAME gP1LifePoints | 0x080a0758 asm/13_equip_placement.s:6531, 0x080a0764 asm/13_equip_placement.s:6538 | gP1LifePoints base; preserve the existing DATA reference and its source. |
| 0x080a0788 / DWORD_080a0788 / 0x00001d1c | EQ CARD_PLAY_PHASE_CTR_OFF | 0x080a075a asm/13_equip_placement.s:6532 | Byte offset from gP1LifePoints to the equip display phase word. |
| 0x080a07f4 / DWORD_080a07f4 / 0x00001cec | EQ P1LP_TIMER_OFF | 0x080a078c asm/13_equip_placement.s:6558 | Byte offset from gP1LifePoints to the duel display timer word. |
| 0x080a07f8 / DWORD_080a07f8 / 0x00000868 | EQ PLAYER_BLOCK_STRIDE | 0x080a07a4 asm/13_equip_placement.s:6570 | Byte stride between the two player state blocks. |
| 0x080a07fc / DWORD_080a07fc / 0x00001cfc | EQ DISP_SET_VARIANT_OFF | 0x080a07ca asm/13_equip_placement.s:6590 | Byte offset from gP1LifePoints to display variant 1/2. |
| 0x080a0800 / DWORD_080a0800 / 0x0201e2a0 | REF gDuelCardCtxBase | 0x080a07ce asm/13_equip_placement.s:6592 | Duel card activation context base. |
| 0x080a0804 / DWORD_080a0804 / 0x000010dc | EQ LP_DISCARD_ZONE_OFF | 0x080a07ec asm/13_equip_placement.s:6608 | Byte offset from gP1LifePoints to LP discard-zone tracking. |
| 0x080a0834 / DAT_080a0834 / 0x00008004 | EQ OAM_EQUIP_SPRITE_P2_04 | 0x080a080e asm/13_equip_placement.s:6626 | Player-side sprite code 4 with bit15 set. |
| 0x080a0838 / PTR_gP1LifePoints_080a0838 / 0x0201c4e0 | RENAME gP1LifePoints | 0x080a081a asm/13_equip_placement.s:6633 | gP1LifePoints base; preserve the existing DATA reference and its source. |
| 0x080a083c / DAT_080a083c / 0x00001d1c | EQ CARD_PLAY_PHASE_CTR_OFF | 0x080a081c asm/13_equip_placement.s:6634 | Byte offset from gP1LifePoints to the equip display phase word. |

关键域选择：0x080a0018读取的是LP word并与6000比较，复用LP_DELTA_6000而非同值MARSHMALLON_CID；0x0809ff68基址是gP1LifePoints，复用P2LP_BLOCK2_OFF_1CF4；0x080a07fc写显示variant1/2，复用DISP_SET_VARIANT_OFF；0x0201e204等于gP1LifePoints+0x1d24，也等于gDuelFieldSlots+0x1cf4，统一新全局gEquipActivationScanCursor。Confidence high。

## 落地守卫与自检

- `f13-seg3-preflight.log`与`f13-seg3-rom-table-preflight.log`均以`-noanalysis -readOnly`运行；两批15个DB文件SHA256前后逐项相同。
- 138槽ROM little-endian值、机器LDR target、动作唯一覆盖、slot命名、NEW/REUSE数值、四个新具名CID的正确CID列/card-stats/passcode三方一致、两个callback odd值、58个carve pointer+1、incbin长度、20个Function ID/body/oldPLATE，以及7个registry PLATE payload的完整字段/hash/ASCII/长度均由`f13-seg3-selfcheck-command.txt`重跑。
- Fixer落地后须全量重导、inject_modes、split、build并验证ROM byte-identical；任一SHA1差异按红线回滚.rep。禁止stage/commit。

## 求助

无。所有语义决策均由机器码消费者、ROM表边界和本地卡表闭合。

## Executor Report: F13-Seg-3

- 槽: EQ=98 REF=21 RENAME=19 FUNC_RENAME=6 PLATE=20
- carve=2块/58项 disasm=0 §5.1=0
- 新增constants/全局: 17；复用项见表
- 求助: none
- proposal: doc/dev/refine/F13-Seg-3.proposal.md
