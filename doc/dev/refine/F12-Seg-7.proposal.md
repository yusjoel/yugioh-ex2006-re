# Refine Proposal: F12-Seg-7 [0x08099314..0x0809a1a4)

本提案仅覆盖 `asm/12_equip_activation_scan.s` 的指定半开区间. 依据最终 Seg-6 落地后的 asm/constants 读取, 不引用旧草案推断. executor 只产出计划和本地扫描记录, 未改 Ghidra/asm/constants, 未 build/stage/commit.

## 段测绘

| 入口 | 现名 | 模块行 | 实际范围 | 自动槽 |
|---|---|---|---|---|
| 0x08099314 | dispatch_equip_field_phase_handler | 10979 | [0x08099314,0x08099aac) | 72 |
| 0x08099aac | run_equip_slot_display_update_state_machine | 11978 | [0x08099aac,0x08099e0c) | 28 |
| 0x08099e0c | run_equip_spell_display_state_machine | 12424 | [0x08099e0c,0x0809a1a4) | 35 |

- 函数入口 x3, 独立共享尾入口 x0. 三个内部返回块为 0x08099a9a/0x08099df2/0x0809a170, 分别恢复各自主函数栈帧, 不新建函数.
- 自动槽 x135 = DAT_ 122 + PTR_gP1LifePoints_ 12 + PTR_switchdataD_ 1. DWORD_/UNK_ x0. 路线图原 122 只计 DAT_, 差额是全部 13 个 PTR 槽.
- 逐槽原名/地址/ROM u32/使用点见 `output/refine-run-20260831-194634/seg7-plan.json`; 下文 EQ/REF/RENAME 三表是唯一主分类, 无重复地址.
- ROM_INCBIN x0, .byte x0. 扫描整个 L10980..12900; 1619 个有地址的指令/数据项和 58 字节 `.zero` 对齐完整覆盖 3728 字节. 逐项字节与 ROM 相同, 无缺口/重叠. `.hword` 是已有 Thumb 指令表示, 不作为新裸块.
- 既有 switch 表 [0x08099370,0x0809939c), 11 项 u32. `.hword 0x4687` @0x0809935c 是 MOV pc,r0, 表项保留偶地址, 不加 +1.
- 三个旧 plate 全部整段重写: 修正 0x38 字节上下文步长, 输入 r0, 返回值, 相位与 LP 基址. 0x14 是 activation record 步长, 不能替换上下文步长.

## 数据块分类 (Rule 2/3)

| 块 | raw / THUMB+1 ref-scan | 判定 | 证据 |
|---|---|---|---|
| ROM_INCBIN/.byte 候选 | 空集合, 全段无匹配 | 无 carve/disasm/5.1 | seg7-map-check.json 的 bare_blocks=[] |
| 已结构化表 0x08099370, size 0x2c | raw=1 / thumb=0 | 保持结构; REF 接通池槽 | 唯一 raw 指针 @0x0809936c, L11013..11018 从表载入后 MOV pc,r0 |

全 ROM 扫描按每个字节位置查 4-byte little-endian 值, raw 与 addr|1 分开. switch 项与其目标扫描如下:

| index | 表槽 | 保留值 | raw refs | thumb refs |
|---|---|---|---|---|
| 0 | 0x08099370 | 0x0809939c | 1 | 0 |
| 1 | 0x08099374 | 0x08099520 | 1 | 0 |
| 2 | 0x08099378 | 0x0809972c | 1 | 0 |
| 3 | 0x0809937c | 0x08099844 | 1 | 0 |
| 4 | 0x08099380 | 0x08099880 | 1 | 0 |
| 5 | 0x08099384 | 0x08099888 | 1 | 0 |
| 6 | 0x08099388 | 0x0809997c | 1 | 0 |
| 7 | 0x0809938c | 0x08099a98 | 3 | 0 |
| 8 | 0x08099390 | 0x08099a98 | 3 | 0 |
| 9 | 0x08099394 | 0x08099a98 | 3 | 0 |
| 10 | 0x08099398 | 0x080999e0 | 1 | 0 |

7/8/9 三项共用目标 0x08099a98, 其 raw=3 是三条表项, 不是三块数据. 各目标已反汇编, 非 carve/disasm 新任务. 主入口 0x08099314/0x08099aac/0x08099e0c 各 raw=0, THUMB+1=1, 唯一位置依次是 0x09e5ab08/0x09e5ab0c/0x09e5ab10. 三个内部返回块 raw=0/thumb=0, 但由本函数分支和自然续接到达, 不登记 5.1. 完整扫描位置见 `seg7-map-check.json`.

## 符号化计划 (R1/R2/R3)

三表均逐地址列出. 所有 value 来自 ROM 当前字节. 不改指令、字面值、表项值、函数边界、跨段标签或旧 equate. base+offset 保持两个槽, 各自命名.

### EQ_SLOTS (data-equate)

96 槽. 格式 `(slot, value, const_name, slot_label)`. 复用或新建由后文 NEW/REUSE 目录逐符号确定. 在该 u32 数据的 operand 0 建 equate 引用, 槽改为 USER_DEFINED 主标签; 不创建无关地址引用.

```text
(0x08099368, 0x00001d2c, EQUIP_CHAIN_ACTIVE_OFF, equip_field_phase_equip_chain_active_off_99368)
(0x080993b8, 0x00001d2c, EQUIP_CHAIN_ACTIVE_OFF, equip_field_phase_equip_chain_active_off_993b8)
(0x080993e4, 0x00001913, BES_CRYSTAL_CORE_CID, equip_field_phase_bes_crystal_core_cid_993e4)
(0x080993e8, 0x00001643, MIRAGE_KNIGHT_CID, equip_field_phase_mirage_knight_cid_993e8)
(0x080993f0, 0x00001837, BIG_CORE_CID, equip_field_phase_big_core_cid_993f0)
(0x08099408, 0x00001983, MYTHICAL_BEAST_CERBERUS_CID, equip_field_phase_mythical_beast_cerberus_cid_99408)
(0x0809941c, 0x000019bf, BES_COVERED_CORE_CID, equip_field_phase_bes_covered_core_cid_9941c)
(0x080994cc, 0x00000868, PLAYER_BLOCK_STRIDE, equip_field_phase_player_block_stride_994cc)
(0x080994d4, 0x00001cb8, EQUIP_ZONE_COUNT_TABLE_OFF, equip_field_phase_equip_zone_count_table_off_994d4)
(0x08099510, 0x00001512, AFTER_THE_STRUGGLE_CID, equip_field_phase_after_the_struggle_cid_99510)
(0x0809951c, 0x00001d2c, EQUIP_CHAIN_ACTIVE_OFF, equip_field_phase_equip_chain_active_off_9951c)
(0x0809954c, 0x00001913, BES_CRYSTAL_CORE_CID, equip_field_phase_bes_crystal_core_cid_9954c)
(0x08099550, 0x00001749, LEGENDARY_JUJITSU_MASTER_CID, equip_field_phase_legendary_jujitsu_master_cid_99550)
(0x08099554, 0x00001643, MIRAGE_KNIGHT_CID, equip_field_phase_mirage_knight_cid_99554)
(0x08099564, 0x0000182c, HARPIE_LADY_3_CID, equip_field_phase_harpie_lady_3_cid_99564)
(0x0809957c, 0x00001983, MYTHICAL_BEAST_CERBERUS_CID, equip_field_phase_mythical_beast_cerberus_cid_9957c)
(0x08099590, 0x000019bf, BES_COVERED_CORE_CID, equip_field_phase_bes_covered_core_cid_99590)
(0x080995e0, 0x00000868, PLAYER_BLOCK_STRIDE, equip_field_phase_player_block_stride_995e0)
(0x0809966c, 0x00000868, PLAYER_BLOCK_STRIDE, equip_field_phase_player_block_stride_9966c)
(0x08099674, 0x00001cb8, EQUIP_ZONE_COUNT_TABLE_OFF, equip_field_phase_equip_zone_count_table_off_99674)
(0x08099718, 0x00001512, AFTER_THE_STRUGGLE_CID, equip_field_phase_after_the_struggle_cid_99718)
(0x08099720, 0x0000129a, REFLECT_BOUNDER_CID, equip_field_phase_reflect_bounder_cid_99720)
(0x08099724, 0x00000868, PLAYER_BLOCK_STRIDE, equip_field_phase_player_block_stride_99724)
(0x08099794, 0x00008016, OAM_EQUIP_SPRITE_P2_16, equip_field_phase_oam_equip_sprite_p2_16_99794)
(0x08099798, 0xffff0000, SPRITE_HIGH_HALF_MASK, equip_field_phase_sprite_high_half_mask_99798)
(0x0809982c, 0x0000ffff, SPRITE_LOW_HALF_MASK, equip_field_phase_sprite_low_half_mask_9982c)
(0x08099834, 0x000013aa, KINETIC_SOLDIER_CID, equip_field_phase_kinetic_soldier_cid_99834)
(0x08099838, 0x000014cc, HUNTER_7_WEAPONS_CID, equip_field_phase_hunter_7_weapons_cid_99838)
(0x08099840, 0x00001d2c, EQUIP_CHAIN_ACTIVE_OFF, equip_field_phase_equip_chain_active_off_99840)
(0x08099860, 0x00001d28, EQUIP_CHAIN_STEP_OFF, equip_field_phase_equip_chain_step_off_99860)
(0x08099864, 0x00001d2c, EQUIP_CHAIN_ACTIVE_OFF, equip_field_phase_equip_chain_active_off_99864)
(0x0809987c, 0x00001d2c, EQUIP_CHAIN_ACTIVE_OFF, equip_field_phase_equip_chain_active_off_9987c)
(0x08099940, 0x0000ffff, EQUIP_ACTIVATION_CNT_CAP, equip_field_phase_equip_activation_cnt_cap_99940)
(0x08099944, 0x00008017, OAM_EQUIP_SPRITE_P2_17, equip_field_phase_oam_equip_sprite_p2_17_99944)
(0x08099978, 0x00001d2c, EQUIP_CHAIN_ACTIVE_OFF, equip_field_phase_equip_chain_active_off_99978)
(0x080999dc, 0x00008021, OAM_EQUIP_SPRITE_P2_21, equip_field_phase_oam_equip_sprite_p2_21_999dc)
(0x08099a70, 0x000001ff, EQUIP_PAYLOAD_LOW9_MASK, equip_field_phase_equip_payload_low9_mask_99a70)
(0x08099a74, 0xfffffe00, EQUIP_PAYLOAD_CLEAR_LOW9_MASK, equip_field_phase_equip_payload_clear_low9_mask_99a74)
(0x08099a78, 0xffffc3ff, OAM_SPRITE_ATTR_CLR_BITS13_10, equip_field_phase_oam_sprite_attr_clr_bits13_10_99a78)
(0x08099a7c, 0xffffbfff, SLOT_ACTIVE_BIT14_CLR, equip_field_phase_slot_active_bit14_clr_99a7c)
(0x08099a80, 0xfffeffff, OAM_SPRITE_ATTR_CLR_BIT16, equip_field_phase_oam_sprite_attr_clr_bit16_99a80)
(0x08099a84, 0xfffdffff, OAM_SPRITE_ATTR_CLR_BIT17, equip_field_phase_oam_sprite_attr_clr_bit17_99a84)
(0x08099a88, 0x2a200000, EQUIP_ACTIVATION_PACKED_TYPE21, equip_field_phase_equip_activation_packed_type21_99a88)
(0x08099a90, 0x00001d28, EQUIP_CHAIN_STEP_OFF, equip_field_phase_equip_chain_step_off_99a90)
(0x08099a94, 0x00001d2c, EQUIP_CHAIN_ACTIVE_OFF, equip_field_phase_equip_chain_active_off_99a94)
(0x08099b00, 0x00001d2c, EQUIP_CHAIN_ACTIVE_OFF, equip_slot_update_equip_chain_active_off_99b00)
(0x08099ba8, 0x0000ffff, EQUIP_ACTIVATION_CNT_CAP, equip_slot_update_equip_activation_cnt_cap_99ba8)
(0x08099bac, 0xffff0000, SPRITE_HIGH_HALF_MASK, equip_slot_update_sprite_high_half_mask_99bac)
(0x08099bb0, 0xfffeffff, OAM_SPRITE_ATTR_CLR_BIT16, equip_slot_update_oam_sprite_attr_clr_bit16_99bb0)
(0x08099bb4, 0xffe1ffff, OAM_SPRITE_ATTR_CLR_BITS20_17, equip_slot_update_oam_sprite_attr_clr_bits20_17_99bb4)
(0x08099bb8, 0xffdfffff, SLOT_BIT21_CLR, equip_slot_update_slot_bit21_clr_99bb8)
(0x08099bbc, 0xfc3fffff, OAM_SPRITE_ATTR_CLR_BITS25_22, equip_slot_update_oam_sprite_attr_clr_bits25_22_99bbc)
(0x08099bdc, 0x000012ac, SATELLITE_CANNON_CID, equip_slot_update_satellite_cannon_cid_99bdc)
(0x08099be0, 0x000013cb, ROCKET_WARRIOR_CID, equip_slot_update_rocket_warrior_cid_99be0)
(0x08099c34, 0x00001ce8, P1LP_BLOCK2_OFF_1CE8, equip_slot_update_p1lp_block2_off_1ce8_99c34)
(0x08099c38, 0x00001cf4, P2LP_BLOCK2_OFF_1CF4, equip_slot_update_p2lp_block2_off_1cf4_99c38)
(0x08099c74, 0x00001826, ELEMENT_MAGICIAN_CID, equip_slot_update_element_magician_cid_99c74)
(0x08099c78, 0x000016cb, BLACK_LUSTER_SOLDIER_ENVOY_CID, equip_slot_update_black_luster_soldier_envoy_cid_99c78)
(0x08099c7c, 0x000013b1, TIMEATER_CID, equip_slot_update_timeater_cid_99c7c)
(0x08099c88, 0x000017e3, ELEMENT_DRAGON_CID, equip_slot_update_element_dragon_cid_99c88)
(0x08099d5c, 0x00001861, ELEMENT_DOOM_CID, equip_slot_update_element_doom_cid_99d5c)
(0x08099d60, 0x000019d4, RUIN_QUEEN_OF_OBLIVION_CID, equip_slot_update_ruin_queen_of_oblivion_cid_99d60)
(0x08099d68, 0x0000ffff, SPRITE_LOW_HALF_MASK, equip_slot_update_sprite_low_half_mask_99d68)
(0x08099d70, 0x000013b1, TIMEATER_CID, equip_slot_update_timeater_cid_99d70)
(0x08099d78, 0x0000129a, REFLECT_BOUNDER_CID, equip_slot_update_reflect_bounder_cid_99d78)
(0x08099d7c, 0x000016bf, BERSERK_GORILLA_CID, equip_slot_update_berserk_gorilla_cid_99d7c)
(0x08099e08, 0x00001d2c, EQUIP_CHAIN_ACTIVE_OFF, equip_slot_update_equip_chain_active_off_99e08)
(0x08099e5c, 0x00001d2c, EQUIP_CHAIN_ACTIVE_OFF, equip_spell_display_equip_chain_active_off_99e5c)
(0x08099eb0, 0x2a200000, EQUIP_ACTIVATION_PACKED_TYPE21, equip_spell_display_equip_activation_packed_type21_99eb0)
(0x08099eb4, 0x00001770, MARSHMALLON_CID, equip_spell_display_marshmallon_cid_99eb4)
(0x08099ebc, 0x00001d2c, EQUIP_CHAIN_ACTIVE_OFF, equip_spell_display_equip_chain_active_off_99ebc)
(0x08099efc, 0x2a200000, EQUIP_ACTIVATION_PACKED_TYPE21, equip_spell_display_equip_activation_packed_type21_99efc)
(0x08099f00, 0x000015d9, DD_CRAZY_BEAST_CID, equip_spell_display_dd_crazy_beast_cid_99f00)
(0x08099f04, 0x0000112f, cid_112f, equip_spell_display_cid_112f_99f04)
(0x08099f10, 0x00001135, cid_1135, equip_spell_display_cid_1135_99f10)
(0x08099f28, 0x0000172c, DD_ASSAILANT_CID, equip_spell_display_dd_assailant_cid_99f28)
(0x08099f34, 0x000018e6, HOLY_KNIGHT_ISHZARK_CID, equip_spell_display_holy_knight_ishzark_cid_99f34)
(0x08099f6c, 0x00008046, OAM_EQUIP_SPRITE_P2_46, equip_spell_display_oam_equip_sprite_p2_46_99f6c)
(0x08099ff0, 0x2a200000, EQUIP_ACTIVATION_PACKED_TYPE21, equip_spell_display_equip_activation_packed_type21_99ff0)
(0x08099ff4, 0x000013b1, TIMEATER_CID, equip_spell_display_timeater_cid_99ff4)
(0x08099ff8, 0x00001130, cid_1130, equip_spell_display_cid_1130_99ff8)
(0x0809a008, 0x00001208, cid_1208, equip_spell_display_cid_1208_9a008)
(0x0809a00c, 0x00001310, WALL_OF_ILLUSION_CID, equip_spell_display_wall_of_illusion_cid_9a00c)
(0x0809a024, 0x00001657, DD_WARRIOR_LADY_CID, equip_spell_display_dd_warrior_lady_cid_9a024)
(0x0809a028, 0x000014f1, KELBEK_CID, equip_spell_display_kelbek_cid_9a028)
(0x0809a03c, 0x0000172c, DD_ASSAILANT_CID, equip_spell_display_dd_assailant_cid_9a03c)
(0x0809a040, 0x000018e6, HOLY_KNIGHT_ISHZARK_CID, equip_spell_display_holy_knight_ishzark_cid_9a040)
(0x0809a07c, 0x00008046, OAM_EQUIP_SPRITE_P2_46, equip_spell_display_oam_equip_sprite_p2_46_9a07c)
(0x0809a184, 0x000001ff, EQUIP_PAYLOAD_LOW9_MASK, equip_spell_display_equip_payload_low9_mask_9a184)
(0x0809a188, 0xfffffe00, EQUIP_PAYLOAD_CLEAR_LOW9_MASK, equip_spell_display_equip_payload_clear_low9_mask_9a188)
(0x0809a18c, 0xfffffdff, OAM_SPRITE_ATTR_CLR_BIT9, equip_spell_display_oam_sprite_attr_clr_bit9_9a18c)
(0x0809a190, 0xffffc3ff, OAM_SPRITE_ATTR_CLR_BITS13_10, equip_spell_display_oam_sprite_attr_clr_bits13_10_9a190)
(0x0809a194, 0xffffbfff, SLOT_ACTIVE_BIT14_CLR, equip_spell_display_slot_active_bit14_clr_9a194)
(0x0809a198, 0xfffeffff, OAM_SPRITE_ATTR_CLR_BIT16, equip_spell_display_oam_sprite_attr_clr_bit16_9a198)
(0x0809a19c, 0xfffdffff, OAM_SPRITE_ATTR_CLR_BIT17, equip_spell_display_oam_sprite_attr_clr_bit17_9a19c)
(0x0809a1a0, 0x00008060, OAM_EQUIP_SPRITE_P2_60, equip_spell_display_oam_equip_sprite_p2_60_9a1a0)
```

### REF_SLOTS (USER-label + DATA-ref)

27 槽 = RAM 26 + switch 表指针 1. 格式 `(slot, target, gas_label, slot_label)`.

```text
(0x08099360, 0x0201bb90, gEquipChainSlotRefs, equip_field_phase_chain_base_99360)
(0x0809936c, 0x08099370, switchD_0809935c__switchdataD_08099370, equip_field_phase_phase_table_ptr_9936c)
(0x08099438, 0x0201bb90, gEquipChainSlotRefs, equip_field_phase_chain_base_99438)
(0x08099454, 0x0201bb90, gEquipChainSlotRefs, equip_field_phase_chain_base_99454)
(0x080994c8, 0x0201bb90, gEquipChainSlotRefs, equip_field_phase_chain_base_994c8)
(0x080994d0, 0x0201c510, gDuelFieldSlots, equip_field_phase_field_slots_base_994d0)
(0x08099514, 0x0201bb90, gEquipChainSlotRefs, equip_field_phase_chain_base_99514)
(0x080995ac, 0x0201bb90, gEquipChainSlotRefs, equip_field_phase_chain_base_995ac)
(0x080995e4, 0x0201c510, gDuelFieldSlots, equip_field_phase_field_slots_base_995e4)
(0x08099600, 0x0201bb90, gEquipChainSlotRefs, equip_field_phase_chain_base_99600)
(0x08099670, 0x0201c510, gDuelFieldSlots, equip_field_phase_field_slots_base_99670)
(0x0809971c, 0x0201bb90, gEquipChainSlotRefs, equip_field_phase_chain_base_9971c)
(0x08099728, 0x0201c510, gDuelFieldSlots, equip_field_phase_field_slots_base_99728)
(0x08099790, 0x0201bb90, gEquipChainSlotRefs, equip_field_phase_chain_base_99790)
(0x08099830, 0x0201bb90, gEquipChainSlotRefs, equip_field_phase_chain_base_99830)
(0x08099934, 0x0201bb90, gEquipChainSlotRefs, equip_field_phase_chain_base_99934)
(0x08099938, 0x0201bbbc, gDuelEquipCtx, equip_field_phase_context_base_99938)
(0x0809993c, 0x0201bbc0, gDuelEquipCtxSlotIndex, equip_field_phase_context_slot_index_base_9993c)
(0x080999d8, 0x0201bb90, gEquipChainSlotRefs, equip_field_phase_chain_base_999d8)
(0x08099af8, 0x0201bb90, gEquipChainSlotRefs, equip_slot_update_chain_base_99af8)
(0x08099d64, 0x0201bb90, gEquipChainSlotRefs, equip_slot_update_chain_base_99d64)
(0x08099d6c, 0x0201bc54, gDuelEffectChainSlots, equip_slot_update_effect_chain_slots_99d6c)
(0x08099d74, 0x0201bc2c, gEquipActivationSlotBase, equip_slot_update_activation_slots_99d74)
(0x08099e54, 0x0201bb90, gEquipChainSlotRefs, equip_spell_display_chain_base_99e54)
(0x08099f68, 0x0201bb90, gEquipChainSlotRefs, equip_spell_display_chain_base_99f68)
(0x08099fec, 0x0201bb90, gEquipChainSlotRefs, equip_spell_display_chain_base_99fec)
(0x0809a180, 0x0201bb90, gEquipChainSlotRefs, equip_spell_display_chain_base_9a180)
```

REF 落地要求:

- RAM 目标必须为对应地址上的 USER_DEFINED LABEL 主符号; 复用已定义名字, 新目标仅 gDuelEquipCtxSlotIndex. switch 复用既有表标签 `switchD_0809935c__switchdataD_08099370`, 在原地址确认 USER_DEFINED LABEL 主符号, 不改内部 case 标签和表值.
- 池槽 operand 0 的指向目标引用必须是 DATA/USER_DEFINED. 若既有同目标 DEFAULT 引用存在, 先精确移除该 operand 0 引用再重建, 不依赖 addMemoryReference 自动升级 source. 保留其他 operand/非目标引用. postcheck 同时验 from/to/operand/type/source.
- ExportRangeToGas 只将 USER_DEFINED LABEL 目标导为符号; ROM FUNCTION 目标被排除, `+` 会经 sanitize_label 改写. 本段无 THUMB 函数指针槽, 不建奇地址标签/函数, 不承诺 REF 导出 fn+1, 不改 exporter. switch 目标是数据 LABEL, 输出应为 `.word switchD_0809935c__switchdataD_08099370`.
- RAM 输出应为 `.word <gas_label>`; constants/ewram.inc 定义与目标地址相同. 不把数据标签提升到函数入口.

### RENAME_SLOTS (纯改名 + EOL)

12 槽. 已有 `.word gP1LifePoints` 符号表达式, 保留该目标、值及引用. 格式 `(slot, slot_label, eol_ascii)`.

```text
(0x08099364, equip_field_phase_lp_base_99364, "gP1LifePoints base for equip display state.")
(0x080993b4, equip_field_phase_lp_base_993b4, "gP1LifePoints base for equip display state.")
(0x08099518, equip_field_phase_lp_base_99518, "gP1LifePoints base for equip display state.")
(0x0809983c, equip_field_phase_lp_base_9983c, "gP1LifePoints base for equip display state.")
(0x0809985c, equip_field_phase_lp_base_9985c, "gP1LifePoints base for equip display state.")
(0x08099878, equip_field_phase_lp_base_99878, "gP1LifePoints base for equip display state.")
(0x08099974, equip_field_phase_lp_base_99974, "gP1LifePoints base for equip display state.")
(0x08099a8c, equip_field_phase_lp_base_99a8c, "gP1LifePoints base for equip display state.")
(0x08099afc, equip_slot_update_lp_base_99afc, "gP1LifePoints base for equip display state.")
(0x08099e04, equip_slot_update_lp_base_99e04, "gP1LifePoints base for equip display state.")
(0x08099e58, equip_spell_display_lp_base_99e58, "gP1LifePoints base for equip display state.")
(0x08099eb8, equip_spell_display_lp_base_99eb8, "gP1LifePoints base for equip display state.")
```

### FUNC_RENAME

none. 三个现名分别覆盖相位派发、装备槽显示更新、装备魔法显示状态机. 仅修正 plate 的事实错误, 不变更 FUNCTION 符号或函数范围. 文本直接 BL 入度均为 0; ROM 表指针各 1, 已给扫描位置. 不新增函数, 不需要 naming-proposals.csv 同步.

### PLATE (R5, full ASCII rewrite)

以下正文全部 ASCII, 字符数不含 fence, 每条 <=500. 三个入口整段替换, 不触碰相邻 Seg-6/Seg-8 plate.

#### 0x08099314 (459 chars)

```text
Dispatches equip field display phases 0..10 for r0=player_side. Uses gEquipChainSlotRefs and 0x38-byte player contexts at gDuelEquipCtx; phase is [gP1LifePoints+EQUIP_CHAIN_ACTIVE_OFF]. Phases score candidates, queue sprites, pack LP rows, scan candidates (phase 4), and apply activations. Mismatch exits write step 11 and clear phase; phase 0 instead routes to phase 10. Returns 0 while pending, 1 when complete. Cases 7/8/9 and out-of-range phases complete.
```

#### 0x08099aac (469 chars)

```text
Ticks equip slot display phases for r0=player_side. Uses two 0x38-byte contexts at gDuelEquipCtx and phase [gP1LifePoints+EQUIP_CHAIN_ACTIVE_OFF]. Phase 0 packs two 0x14-byte activation records into LP row type 14 unless chain[+0x14] is set. Phase 1 queues Satellite Cannon/Rocket Warrior displays; phase 2 applies card-specific activations and updates sprites. Brackets row/activation work with LP display counter calls. Returns 0 through phases 0..2, 1 after phase 2.
```

#### 0x08099e0c (477 chars)

```text
Ticks equip spell display phases for r0=player_side using paired 0x38-byte contexts at gDuelEquipCtx. State is [gP1LifePoints+EQUIP_CHAIN_ACTIVE_OFF]. Nonzero chain[+8] returns 1. Phase 0 polls two sprite scanners, applies the Marshmallon path, then advances phase; scanner activity returns 0 without advancing. Phase 1 queues card-specific displays and applies packed type-21 activations without advancing phase locally. Returns 0 in phase 0 and 1 for phase 1 or other phases.
```

## carve 计划 (R7)

none. 无 rom.s 切割, 无新 ROM 数据块. 既有 11 项 switch 表保持 u32 偶地址数值, 不作 THUMB callback 表处理.

## disasm 计划 (R4)

none. 不清 listing, 不设 TMode, 不建函数. 全段已有指令/数据/对齐完整覆盖; switch 目标逐项已是 Thumb 基本块.

## 新增 constants / 全局与复用目录

全量解析 `constants/*.inc` 的 5932 条 `.equ/.set`, 递归求值 5932 成功, 0 未解析; 检查十六进制、十进制、别名及表达式. 逐值结果见 `seg7-constant-values-evaluated.json`. 新增 22 个常量 + 1 个 RAM 全局, 合计 23 定义, 复用已有 inc, 不新建 include 文件.

### NEW (按文件添加)

`constants/card_info.inc`:

```asm
.equ cid_112f, 0x0000112f  @ Unassigned internal card ID 0x112f; cards-ids-array.s maps to 0xffff.
.equ cid_1130, 0x00001130  @ Unassigned internal card ID 0x1130; cards-ids-array.s maps to 0xffff.
.equ cid_1135, 0x00001135  @ Unassigned internal card ID 0x1135; cards-ids-array.s maps to 0xffff.
.equ cid_1208, 0x00001208  @ Unassigned internal card ID 0x1208; cards-ids-array.s maps to 0xffff.
.equ WALL_OF_ILLUSION_CID, 0x00001310  @ Wall of Illusion; slot CID; card-stats.s card_0698; pw=13945283.
.equ TIMEATER_CID, 0x000013b1  @ Timeater; slot CID; card-stats.s card_0831; pw=44913552.
.equ KELBEK_CID, 0x000014f1  @ Kelbek; slot CID; card-stats.s card_1057; pw=54878498.
.equ AFTER_THE_STRUGGLE_CID, 0x00001512  @ After the Struggle; slot CID; card-stats.s card_1085; pw=25345186.
.equ DD_CRAZY_BEAST_CID, 0x000015d9  @ D.D. Crazy Beast; slot CID; card-stats.s card_1228; pw=48148828.
.equ DD_WARRIOR_LADY_CID, 0x00001657  @ D.D. Warrior Lady; slot CID; card-stats.s card_1327; pw=07572887.
.equ DD_ASSAILANT_CID, 0x0000172c  @ D. D. Assailant; slot CID; card-stats.s card_1503; pw=70074904.
.equ ELEMENT_DOOM_CID, 0x00001861  @ Element Doom; slot CID; card-stats.s card_1762; pw=23118924.
.equ HOLY_KNIGHT_ISHZARK_CID, 0x000018e6  @ Holy Knight Ishzark; slot CID; card-stats.s card_1871; pw=57902462.
.equ RUIN_QUEEN_OF_OBLIVION_CID, 0x000019d4  @ Ruin, Queen of Oblivion; slot CID; card-stats.s card_2055; pw=46427957.
```

`constants/oam_attr.inc`:

```asm
.equ OAM_EQUIP_SPRITE_P2_16, 0x00008016  @ Equip display sprite code for nonzero player side; side zero uses 0x16; enqueue_sprite_attr_record argument 0.
.equ OAM_EQUIP_SPRITE_P2_17, 0x00008017  @ Equip display sprite code for nonzero player side; side zero uses 0x17; enqueue_sprite_attr_record argument 0.
.equ OAM_EQUIP_SPRITE_P2_21, 0x00008021  @ Equip display sprite code for nonzero player side; side zero uses 0x21; enqueue_sprite_attr_record argument 0.
.equ OAM_EQUIP_SPRITE_P2_46, 0x00008046  @ Equip display sprite code for nonzero player side; side zero uses 0x46; enqueue_sprite_attr_record argument 0.
.equ OAM_EQUIP_SPRITE_P2_60, 0x00008060  @ Equip display sprite code for nonzero player side; side zero uses 0x60; enqueue_sprite_attr_record argument 0.
```

`constants/duel_field.inc`:

```asm
.equ EQUIP_PAYLOAD_LOW9_MASK, 0x000001ff  @ Low 9-bit entity field of packed equip activation extra_payload; read context[+0xc] before packing.
.equ EQUIP_PAYLOAD_CLEAR_LOW9_MASK, 0xfffffe00  @ Clear low 9 bits of packed equip activation extra_payload before inserting context[+0xc] low bits.
.equ EQUIP_ACTIVATION_PACKED_TYPE21, 0x2a200000  @ Packed activation: type 21 in bits 30:25 plus bit21; record +2 bits 11:6 = 21, +3 bits 5:4 = 1.
```

`constants/ewram.inc`:

```asm
.equ gDuelEquipCtxSlotIndex, 0x0201bbc0  @ gDuelEquipCtx+4: slot-index word of the first equip context; corresponding player entries use stride 0x38.
```

NEW 的同值检索结果:

- 新增定义中, 除下列 3 个值外, 现有 constants 求值后均为 0 命中; 所有新增名字均无既有定义.
- `cid_1130=0x1130` 已有 EQUIP_CHAIN_STEP_BASE_OFF (duel_field.inc:262), 该旧定义是地址偏移, 本槽是与 context[+0x10] 比较的卡 ID, 域不同. 不复用偏移名称.
- `EQUIP_PAYLOAD_LOW9_MASK=0x1ff` 已有 DEMO_KEEP_BITS_8_0/SCROLLBAR_KEEP_BITS_8_0/OAM_ATTR1_X_MASK. 本段取 context[+0xc] 的 entity bits 并装入 equip extra_payload, 不是 demo/scrollbar 状态或 OAM x 坐标. 新名字明确 payload 位域, 不引入坐标含义.
- `EQUIP_PAYLOAD_CLEAR_LOW9_MASK=0xfffffe00` 已有 STACK_ALLOC_NEG_512/OAM_ATTR1_X_CLEAR. 本段 AND 清 extra_payload 低 9 位再 OR entity bits, 不是栈大小或 OAM x 字段. 新建与上一掩码配对的 payload 名称.
- 四个中性 CID 的本地映射都是 0xffff, card-stats.s 无对应 slot 记录. 活动文档 L34 明确未分配 ID 使用 cid_<hex>; 不凭效果分支赋卡名. 这四个命名的数值与分类置信度为 high, 没有待裁决的卡名.

### REUSE (名字和值均保持)

| value | symbol | 既有定义 |
|---|---|---|
| 0x00000868 | PLAYER_BLOCK_STRIDE | constants/ewram.inc:251 |
| 0x0000129a | REFLECT_BOUNDER_CID | constants/card_info.inc:1281 |
| 0x000012ac | SATELLITE_CANNON_CID | constants/card_info.inc:497 |
| 0x000013aa | KINETIC_SOLDIER_CID | constants/card_info.inc:1866 |
| 0x000013cb | ROCKET_WARRIOR_CID | constants/card_info.inc:1912 |
| 0x000014cc | HUNTER_7_WEAPONS_CID | constants/card_info.inc:1867 |
| 0x00001643 | MIRAGE_KNIGHT_CID | constants/card_info.inc:1673 |
| 0x000016bf | BERSERK_GORILLA_CID | constants/card_info.inc:1855 |
| 0x000016cb | BLACK_LUSTER_SOLDIER_ENVOY_CID | constants/card_info.inc:750 |
| 0x00001749 | LEGENDARY_JUJITSU_MASTER_CID | constants/card_info.inc:1504 |
| 0x00001770 | MARSHMALLON_CID | constants/card_info.inc:192 |
| 0x000017e3 | ELEMENT_DRAGON_CID | constants/card_info.inc:348 |
| 0x00001826 | ELEMENT_MAGICIAN_CID | constants/card_info.inc:230 |
| 0x0000182c | HARPIE_LADY_3_CID | constants/card_info.inc:644 |
| 0x00001837 | BIG_CORE_CID | constants/card_info.inc:831 |
| 0x00001913 | BES_CRYSTAL_CORE_CID | constants/card_info.inc:690 |
| 0x00001983 | MYTHICAL_BEAST_CERBERUS_CID | constants/card_info.inc:841 |
| 0x000019bf | BES_COVERED_CORE_CID | constants/card_info.inc:1348 |
| 0x00001cb8 | EQUIP_ZONE_COUNT_TABLE_OFF | constants/duel_field.inc:156 |
| 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | constants/ewram.inc:276 |
| 0x00001cf4 | P2LP_BLOCK2_OFF_1CF4 | constants/ewram.inc:277 |
| 0x00001d28 | EQUIP_CHAIN_STEP_OFF | constants/duel_field.inc:229 |
| 0x00001d2c | EQUIP_CHAIN_ACTIVE_OFF | constants/duel_field.inc:230 |
| 0x0000ffff | EQUIP_ACTIVATION_CNT_CAP | constants/duel_field.inc:514 |
| 0x0000ffff | SPRITE_LOW_HALF_MASK | constants/duel_field.inc:557 |
| 0x0201bb90 | gEquipChainSlotRefs | constants/ewram.inc:317 |
| 0x0201bbbc | gDuelEquipCtx | constants/ewram.inc:459 |
| 0x0201bc2c | gEquipActivationSlotBase | constants/ewram.inc:566 |
| 0x0201bc54 | gDuelEffectChainSlots | constants/ewram.inc:319 |
| 0x0201c4e0 | gP1LifePoints | constants/ewram.inc:79 |
| 0x0201c510 | gDuelFieldSlots | constants/ewram.inc:314 |
| 0xfc3fffff | OAM_SPRITE_ATTR_CLR_BITS25_22 | constants/oam_attr.inc:90 |
| 0xffdfffff | SLOT_BIT21_CLR | constants/duel_field.inc:237 |
| 0xffe1ffff | OAM_SPRITE_ATTR_CLR_BITS20_17 | constants/oam_attr.inc:89 |
| 0xfffdffff | OAM_SPRITE_ATTR_CLR_BIT17 | constants/oam_attr.inc:41 |
| 0xfffeffff | OAM_SPRITE_ATTR_CLR_BIT16 | constants/oam_attr.inc:40 |
| 0xffff0000 | SPRITE_HIGH_HALF_MASK | constants/duel_field.inc:556 |
| 0xffffbfff | SLOT_ACTIVE_BIT14_CLR | constants/duel_field.inc:232 |
| 0xffffc3ff | OAM_SPRITE_ATTR_CLR_BITS13_10 | constants/oam_attr.inc:39 |
| 0xfffffdff | OAM_SPRITE_ATTR_CLR_BIT9 | constants/oam_attr.inc:38 |

复用域说明:

- 0x1cb8 在本段与 gDuelFieldSlots 相加, 结果 0x0201e1c8, 使用 EQUIP_ZONE_COUNT_TABLE_OFF, 不用 gP1LifePoints 相对的 DUEL_ACTIVE_PLAYER_OFF.
- 0x1ce8/0x1cf4 在 L12152..12161 与 r4=gP1LifePoints 相加, 分别到 0x0201e1c8/0x0201e1d4. 第二槽使用 P2LP_BLOCK2_OFF_1CF4, 不用同值 FIELD_STATE_OFF (旧定义明确基址 gDuelFieldSlots). 本段只记录该值与 3 比较, 不替旧定义扩展字段语义.
- 0x1d28/0x1d2c 保持 gP1LifePoints 相对 EQUIP_CHAIN_STEP_OFF/EQUIP_CHAIN_ACTIVE_OFF, 不套用 Seg-6 的 FROM_FIELD_OFF 常量.
- 0xffff 在 0x08099940/0x08099ba8 是 chain+0x9c 激活计数上限, 用 EQUIP_ACTIVATION_CNT_CAP; 0x0809982c/0x08099d68 是低半字 AND 掩码, 用 SPRITE_LOW_HALF_MASK. 0xffff0000 两槽是拼接行参数的高半字保留掩码, 用 SPRITE_HIGH_HALF_MASK, 不用 chain sentinel.
- OAM_SPRITE_ATTR_CLR_BIT9/BITS13_10/BIT16/BIT17 与 SLOT_ACTIVE_BIT14_CLR 用于同形 slot display descriptor 位清除; OAM_SPRITE_ATTR_CLR_BITS20_17/BITS25_22、SLOT_BIT21_CLR 用于 LP row packed word. 此处只沿用名字明确的清位操作, 不从其他使用点的注释继承本段字段的业务含义.
- MARSHMALLON_CID 与 LP_DELTA_6000 同值 0x1770, 此处 compare context[+0x10], 选择 CID.

## 5.1 登记 (Rule 3)

none. 没有未引用裸数据块. 不把通过分支到达的内部返回尾登记为孤儿.

## 消费者证据 (R6)

所有模块行号对应提案生成时的最终 Seg-6 之后 asm. 每个槽的 ldr 使用点已写入 `seg7-plan.json`; 原槽标签仅用来追溯, 落地后的新 plate/EOL 不含旧自动名.

### 结构、相位和掩码

| 项目 | 消费者证据 | 结论 | 置信度 |
|---|---|---|---|
| 输入和 context | asm/12_equip_activation_scan.s:10985..11007,11985..12007,12431..12461 | r0=player_side; (side*8-side)*8=side*0x38, base=chain+0x2c; 与 phase base 分开 | high |
| 新 RAM 全局 | asm/12_equip_activation_scan.s:11704..11730; asm/08_equip_oam_neodaed.s:5272..5298 | gDuelEquipCtx+4 的 word 与 activation record slot 字段比对; 外部消费者乘 0x14 后索引字段槽, 同时 +0 word 选择 player stride; gDuelEquipCtxSlotIndex 指第一个 context 的 slot word | high |
| chain/field/global pointers | asm/12_equip_activation_scan.s:10987..11003,11182..11205,11382..11402,12339..12403 | chain records 与 gDuelFieldSlots 玩家区分别使用 0x38/0x868 步长; activation slots 和 effect-chain 基址按已有结构取字段 | high |
| phase0 mismatch | asm/12_equip_activation_scan.s:11041..11050 | 非零 mismatch 改 phase=10, 返回0; 不能写成直接 step11 | high |
| phase2/3/4 | asm/12_equip_activation_scan.s:11508..11528,11659..11687 | phase2/3 mismatch 到 step11/reset phase; phase4 执行 candidate scan | high |
| phase5 match/cap | asm/12_equip_activation_scan.s:11689..11749 | 按两个 player context 匹配 chain activation record 的 player/slot, count 饱和 0xffff, 两个结果打包 | high |
| field phase 完成 | asm/12_equip_activation_scan.s:11828..11865,11931..11974 | phase6 返回1; phase10 和 mismatch 写 step11/phase0 返回0; case7/8/9 或越界返回1 | high |
| slot update phase0 | asm/12_equip_activation_scan.s:12013..12108 | 两条 0x14 activation records, count+9c/flag+a0/state+a4/player+a8/slot+ac 打包低16/bit16/bits20:17/bit21/bits25:22, row type14 | high |
| halfword masks | asm/12_equip_activation_scan.s:11529..11570,12040..12068,12324..12343 | 0xffff0000/0xffff 为参数位拼接, 与空卡 sentinel 不同 | high |
| slot update phase1/2 | asm/12_equip_activation_scan.s:12124..12234,12235..12416 | phase1 为 Satellite Cannon/Rocket Warrior 条件显示; phase2 才执行 packed activation 与 setup_equip_slot_sprite_attr_by_card; 返回0直到 phase>2 | high |
| spell display phase0 | asm/12_equip_activation_scan.s:12445..12518 | chain+8 非零完成; 两个 scanner 非零保持相位并返回0; Marshmallon 后 phase++ | high |
| spell display phase1 | asm/12_equip_activation_scan.s:12519..12873 | 两方卡 ID 和资格门控后显示/激活; phase1不自增, 返回1 | high |
| payload low9 和其余位 | asm/12_equip_activation_scan.s:11879..11930,12817..12855; asm/05_equip_eligibility_a.s:8043..8063 | context+c entity low9, side bit9, slot bits13:10, state bit14, bit15置1, bit16/17清零; 作为 r2 extra_payload 转发 | high |
| packed type21 | asm/12_equip_activation_scan.s:11914..11930,12479..12518,12622..12641; asm/06_equip_eligibility_b.s:18716..18746 | 0x2a200000=(21<<25)\|(1<<21); unpack 后 record+2 bits11:6=21, record+3 bits5:4=1 | high |

### 新定义来源

| symbol | value | 直接证据 | 置信度 |
|---|---|---|---|
| cid_112f | 0x0000112f | data/cards-ids-array.s:409 -> 0xffff; card-stats.s has no matching slot | high |
| cid_1130 | 0x00001130 | data/cards-ids-array.s:410 -> 0xffff; card-stats.s has no matching slot | high |
| cid_1135 | 0x00001135 | data/cards-ids-array.s:415 -> 0xffff; card-stats.s has no matching slot | high |
| cid_1208 | 0x00001208 | data/cards-ids-array.s:626 -> 0xffff; card-stats.s has no matching slot | high |
| WALL_OF_ILLUSION_CID | 0x00001310 | data/card-stats.s:9089 (card_0698, pw=13945283) | high |
| TIMEATER_CID | 0x000013b1 | data/card-stats.s:10818 (card_0831, pw=44913552) | high |
| KELBEK_CID | 0x000014f1 | data/card-stats.s:13756 (card_1057, pw=54878498) | high |
| AFTER_THE_STRUGGLE_CID | 0x00001512 | data/card-stats.s:14120 (card_1085, pw=25345186) | high |
| DD_CRAZY_BEAST_CID | 0x000015d9 | data/card-stats.s:15979 (card_1228, pw=48148828) | high |
| DD_WARRIOR_LADY_CID | 0x00001657 | data/card-stats.s:17266 (card_1327, pw=07572887) | high |
| DD_ASSAILANT_CID | 0x0000172c | data/card-stats.s:19554 (card_1503, pw=70074904) | high |
| ELEMENT_DOOM_CID | 0x00001861 | data/card-stats.s:22921 (card_1762, pw=23118924) | high |
| HOLY_KNIGHT_ISHZARK_CID | 0x000018e6 | data/card-stats.s:24338 (card_1871, pw=57902462) | high |
| RUIN_QUEEN_OF_OBLIVION_CID | 0x000019d4 | data/card-stats.s:26730 (card_2055, pw=46427957) | high |
| OAM_EQUIP_SPRITE_P2_16 | 0x00008016 | asm/12_equip_activation_scan.s:11516..11528 | high |
| OAM_EQUIP_SPRITE_P2_17 | 0x00008017 | asm/12_equip_activation_scan.s:11750..11808 | high |
| OAM_EQUIP_SPRITE_P2_21 | 0x00008021 | asm/12_equip_activation_scan.s:11828..11864 | high |
| OAM_EQUIP_SPRITE_P2_46 | 0x00008046 | asm/12_equip_activation_scan.s:12591..12600,12740..12748 | high |
| OAM_EQUIP_SPRITE_P2_60 | 0x00008060 | asm/12_equip_activation_scan.s:12858..12867 | high |
| EQUIP_PAYLOAD_LOW9_MASK | 0x000001ff | asm/12_equip_activation_scan.s:11879..11884,12817..12823; asm/05_equip_eligibility_a.s:8043..8063 | high |
| EQUIP_PAYLOAD_CLEAR_LOW9_MASK | 0xfffffe00 | asm/12_equip_activation_scan.s:11879..11884,12817..12823 | high |
| EQUIP_ACTIVATION_PACKED_TYPE21 | 0x2a200000 | asm/12_equip_activation_scan.s:11914..11930,12479..12518,12622..12641; asm/06_equip_eligibility_b.s:18716..18746 | high |
| gDuelEquipCtxSlotIndex | 0x0201bbc0 | asm/12_equip_activation_scan.s:11704..11730; asm/08_equip_oam_neodaed.s:5272..5298 | high |

### 卡 ID 使用点核对

卡名取自原 ROM 导出的 card-stats.s, 不用旧 plate 的猜测. 下列所有具名 CID 均能匹配 slot_id; 四个中性 CID 仅保留已证实内部 ID. 同一常量用于算术派生其他比较值时, 不为派生值另造 literal 槽.

| constant | value | local card source | 本段 ldr 消费者行 |
|---|---|---|---|
| cid_112f | 0x112f | data/cards-ids-array.s:409 (none) | L12537 |
| cid_1130 | 0x1130 | data/cards-ids-array.s:410 (none) | L12664 |
| cid_1135 | 0x1135 | data/cards-ids-array.s:415 (none) | L12554 |
| cid_1208 | 0x1208 | data/cards-ids-array.s:626 (none) | L12685 |
| REFLECT_BOUNDER_CID | 0x129a | data/card-stats.s:8023 card_0616 / Reflect Bounder | L11448, L12312 |
| SATELLITE_CANNON_CID | 0x12ac | data/card-stats.s:8244 card_0633 / Satellite Cannon | L12128 |
| WALL_OF_ILLUSION_CID | 0x1310 | data/card-stats.s:9089 card_0698 / Wall of Illusion | L12688 |
| KINETIC_SOLDIER_CID | 0x13aa | data/card-stats.s:10766 card_0827 / Kinetic Soldier | L11579, L11605 |
| TIMEATER_CID | 0x13b1 | data/card-stats.s:10818 card_0831 / Timeater | L12211, L12272, L12659 |
| ROCKET_WARRIOR_CID | 0x13cb | data/card-stats.s:11013 card_0846 / Rocket Warrior | L12131 |
| HUNTER_7_WEAPONS_CID | 0x14cc | data/card-stats.s:13275 card_1020 / The Hunter with 7 Weapons | L11582, L11608 |
| KELBEK_CID | 0x14f1 | data/card-stats.s:13756 card_1057 / Kelbek | L12701 |
| AFTER_THE_STRUGGLE_CID | 0x1512 | data/card-stats.s:14120 card_1085 / After the Struggle | L11209, L11424 |
| DD_CRAZY_BEAST_CID | 0x15d9 | data/card-stats.s:15979 card_1228 / D.D. Crazy Beast | L12532 |
| MIRAGE_KNIGHT_CID | 0x1643 | data/card-stats.s:17019 card_1308 / Mirage Knight | L11071, L11258 |
| DD_WARRIOR_LADY_CID | 0x1657 | data/card-stats.s:17266 card_1327 / D.D. Warrior Lady | L12696 |
| BERSERK_GORILLA_CID | 0x16bf | data/card-stats.s:18345 card_1410 / Berserk Gorilla | L12315 |
| BLACK_LUSTER_SOLDIER_ENVOY_CID | 0x16cb | data/card-stats.s:18488 card_1421 / Black Luster Soldier - Envoy of the Beginning | L12206 |
| DD_ASSAILANT_CID | 0x172c | data/card-stats.s:19554 card_1503 / D. D. Assailant | L12561, L12711 |
| LEGENDARY_JUJITSU_MASTER_CID | 0x1749 | data/card-stats.s:19827 card_1524 / Legendary Jujitsu Master | L11253 |
| MARSHMALLON_CID | 0x1770 | data/card-stats.s:20256 card_1557 / Marshmallon | L12488 |
| ELEMENT_DRAGON_CID | 0x17e3 | data/card-stats.s:21439 card_1648 / Element Dragon | L12221 |
| ELEMENT_MAGICIAN_CID | 0x1826 | data/card-stats.s:22193 card_1706 / Element Magician | L12200 |
| HARPIE_LADY_3_CID | 0x182c | data/card-stats.s:22271 card_1712 / Harpie Lady 3 | L11269 |
| BIG_CORE_CID | 0x1837 | data/card-stats.s:22414 card_1723 / Big Core | L11081 |
| ELEMENT_DOOM_CID | 0x1861 | data/card-stats.s:22921 card_1762 / Element Doom | L12229 |
| HOLY_KNIGHT_ISHZARK_CID | 0x18e6 | data/card-stats.s:24338 card_1871 / Holy Knight Ishzark | L12574, L12714 |
| BES_CRYSTAL_CORE_CID | 0x1913 | data/card-stats.s:24767 card_1904 / B.E.S. Crystal Core | L11061, L11247 |
| MYTHICAL_BEAST_CERBERUS_CID | 0x1983 | data/card-stats.s:25989 card_1998 / Mythical Beast Cerberus | L11086, L11278 |
| BES_COVERED_CORE_CID | 0x19bf | data/card-stats.s:26457 card_2034 / B.E.S. Covered Core | L11100, L11292 |
| RUIN_QUEEN_OF_OBLIVION_CID | 0x19d4 | data/card-stats.s:26730 card_2055 / Ruin, Queen of Oblivion | L12234 |

## 自检与落地验收清单

- 135 个自动槽与三执行表地址集合完全一致: EQ=96, REF=27, RENAME=12; 每槽仅出现于一表, ROM u32 与所列 value/target 一致.
- 所有 slot_label 满足 `^[a-z][a-z0-9_]+$`, 互不重复, 不与当前 asm 标签碰撞. 新定义名字未存在, 复用定义值已逐一求值验证.
- 三条 PLATE 及 12 条 RENAME EOL 全部 ASCII; PLATE 长度459/469/477. 所有新增 `.equ` 注释也为 ASCII.
- 全段 3728 字节注记/对齐与 ROM 一致, 0 gap/overlap; 无 ROM_INCBIN/.byte. switch 表 11 项值独立读 ROM, 全为偶地址, MOV pc,r0 保持原语义.
- 机器留痕: `seg7-slots.json`, `seg7-constant-values-evaluated.json`, `seg7-map-check.json`, `seg7-plan.json`, `seg7-selfcheck.json`, 均在 `output/refine-run-20260831-194634/`.
- fixer apply 前应只读预检原槽名/值、目标符号、equate 冲突和 plate. 写入后检查 REF 的 DATA/USER_DEFINED source; 重导后核验指令字节不变, 所有135槽正式表达式与表一致, 11项switch保留原值. 最终以全ROM byte-identical及保存后只读检查为准.
- 本提案未执行 build, 未声称落地已经通过. 不 stage/commit.

## 求助

none. 所有计划项以 high 置信度证据闭合; 未分配 CID 按已授权中性规则命名, 无需卡名裁决.

## Executor Report: F12-Seg-7

- 槽: EQ=96 REF=27 RENAME=12 FUNC_RENAME=0 PLATE=3.
- carve=0 disasm=0 range 5.1=0.
- 新增 constants/全局: 22 constants + gDuelEquipCtxSlotIndex.
- 求助: none.
- proposal: doc/dev/refine/F12-Seg-7.proposal.md
