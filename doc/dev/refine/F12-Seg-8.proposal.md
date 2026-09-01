# Refine Proposal: F12-Seg-8 [0x0809a1a4..0x0809b178)

本提案限定 `asm/12_equip_activation_scan.s` 指定半开区间, 基于 Seg-7 正式落地后的 asm 和 ROM. 不分析 Seg-9. executor 仅写提案和 seg8-* 扫描记录, 不改 Ghidra/asm/constants/进度/工具, 不 build/stage/commit.

## 段测绘

| 入口 | 现名 | 模块行 | 身份与范围 |
|---|---|---|---|
| 0x0809a1a4 | eval_equip_slot_pair_eligibility | 12903 | 主入口, 建立本段共用栈帧; 含三相位逻辑和池 |
| 0x0809b146 | increment_counter_at_ptr | 14990 | 既有共享收尾前缀, 4条指令, 递增相位后接下一尾 |
| 0x0809b14e | restore_callee_high_regs_from_frame | 14997 | 既有共享返回尾, 用主入口的保存栈帧; 尾后池到0x0809b178 |

- 入口统计: 1主函数 + 2既有共享收尾. 后两者无 push 前导, 不能仅按 push 统计排除.
- 自动槽 x131 = DAT_ 118 + DWORD_ 10 + PTR_gP1LifePoints_ 3. UNK_ x0. 原路线图128槽未计3个PTR.
- 10个DWORD地址: 0x0809a330/0x0809a334/0x0809a338/0x0809a33c/0x0809a340/0x0809a3dc/0x0809a3e4/0x0809a7e0/0x0809a7e4/0x0809a7ec.
- 每槽旧名、地址、ROM小端u32及全部ldr使用点见 `output/refine-run-20260831-194634/seg8-plan.json`. 下文三表是唯一执行分类, 不重复覆盖槽.
- 全段L12904..15018共4052字节, 1785个带地址的指令/数据项及66字节 `.zero` 对齐连续覆盖, 字节与ROM逐项相同, 无缺口或重叠.
- ROM_INCBIN x0, .byte x0; 无其他未分类裸块. 71个 `.hword` 为已表示的Thumb高寄存器指令. 无 MOV pc 分派、无 switch 表、无本段函数指针 literal.
- 旧plate3条, 长度767/643/618, 均整段ASCII重写. 重点订正 gDuelBattleState 旧基址、固定返回1、slot_idx写入及独立leaf描述.

## 数据块分类 (Rule 2/3)

| 块/入口 | 全ROM raw / THUMB+1扫描 | 判定 | 证据 |
|---|---|---|---|
| ROM_INCBIN/.byte候选 | 空集合, 全段扫描无匹配 | 无carve/disasm/5.1 | seg8-map-check.json: bare_blocks=[]; 完整字节覆盖 |
| 主入口0x0809a1a4 | raw=0 / thumb=1 | 已有Thumb函数, 不改边界 | 唯一指针0x0809a1a5存于0x09e5ab14 |
| 共享前缀0x0809b146 | raw=0 / thumb=0 | 已反汇编共享收尾, 不登记5.1 | BL @0x0809a3d6/0x0809a7da, 以及0x0809b144自然续接 |
| 共享尾0x0809b14e | raw=0 / thumb=0 | 已反汇编共享收尾, 不登记5.1 | BL @0x0809a32c及0x0809b14c自然续接 |

ref-scan按全ROM每个字节位置搜索little-endian u32, raw与addr|1分开. 无裸块需要额外按2字节步长枚举潜在入口. 两共享尾虽没有原始指针, 直接控制流引用已由ROM分支解码确认, 不能按0指针视为孤儿. 不把BL后的0x0000 nop或池认作新独立函数.

## 符号化计划 (R1/R2/R3)

保持指令、u32值、函数边界、跨段标签与既有equate. base+offset保持两个槽; 特别是gEquipNodePool与负偏移、gDuelFieldSlots与phase偏移不合并.

### EQ_SLOTS (data-equate)

95槽. 格式 `(slot, value, const_name, slot_label)`. 复用/新建由后文NEW/REUSE逐符号目录确定. 建立data-equate的operand0引用并设置槽USER_DEFINED主标签; 不创建数值到地址的无关ref.

```text
(0x0809a204, 0x00000868, PLAYER_BLOCK_STRIDE, eval_equip_pair_player_stride_9a204)
(0x0809a240, 0x00000868, PLAYER_BLOCK_STRIDE, eval_equip_pair_player_stride_9a240)
(0x0809a338, 0x00000868, PLAYER_BLOCK_STRIDE, eval_equip_pair_player_stride_9a338)
(0x0809a340, 0x00001cfc, EQUIP_CHAIN_ACTIVE_FROM_FIELD_OFF, eval_equip_pair_chain_active_from_field_offset_9a340)
(0x0809a360, 0x000013a4, THUNDER_NYAN_NYAN_CID, eval_equip_pair_thunder_nyan_nyan_cid_9a360)
(0x0809a3a4, 0x0000146f, CATHEDRAL_OF_NOBLES_CID, eval_equip_pair_cathedral_of_nobles_cid_9a3a4)
(0x0809a3a8, 0x000013a4, THUNDER_NYAN_NYAN_CID, eval_equip_pair_thunder_nyan_nyan_cid_9a3a8)
(0x0809a3dc, 0x0000146f, CATHEDRAL_OF_NOBLES_CID, eval_equip_pair_cathedral_of_nobles_cid_9a3dc)
(0x0809a3e4, 0x00001d2c, EQUIP_CHAIN_ACTIVE_OFF, eval_equip_pair_chain_active_from_lp_offset_9a3e4)
(0x0809a408, 0x000013b0, equip_pair_cid_13b0, eval_equip_pair_cid_13b0_9a408)
(0x0809a41c, 0x000013b4, RIGRAS_LEEVER_CID, eval_equip_pair_rigras_leever_cid_9a41c)
(0x0809a420, 0x00001836, EQUIP_ELIG_EXCL_B, eval_equip_pair_fox_fire_cid_9a420)
(0x0809a47c, 0x00001529, GREAT_DEZARD_CID, eval_equip_pair_great_dezard_cid_9a47c)
(0x0809a480, 0x000012a6, SWORD_HUNTER_CID, eval_equip_pair_sword_hunter_cid_9a480)
(0x0809a494, 0x00001415, RED_MOON_BABY_CID, eval_equip_pair_red_moon_baby_cid_9a494)
(0x0809a4b8, 0x000017d8, MYSTIC_SWORDSMAN_LV4_CID, eval_equip_pair_mystic_swordsman_lv4_cid_9a4b8)
(0x0809a4c8, 0x000017da, ARMED_DRAGON_LV5_CID, eval_equip_pair_armed_dragon_lv5_cid_9a4c8)
(0x0809a5b4, 0x00000868, PLAYER_BLOCK_STRIDE, eval_equip_pair_player_stride_9a5b4)
(0x0809a5f8, 0x000017d2, HORUS_LV4_CID, eval_equip_pair_horus_lv4_cid_9a5f8)
(0x0809a5fc, 0x000013b0, equip_pair_cid_13b0, eval_equip_pair_cid_13b0_9a5fc)
(0x0809a610, 0x000013b4, RIGRAS_LEEVER_CID, eval_equip_pair_rigras_leever_cid_9a610)
(0x0809a614, 0x00001836, EQUIP_ELIG_EXCL_B, eval_equip_pair_fox_fire_cid_9a614)
(0x0809a67c, 0x00001529, GREAT_DEZARD_CID, eval_equip_pair_great_dezard_cid_9a67c)
(0x0809a680, 0x000012a6, SWORD_HUNTER_CID, eval_equip_pair_sword_hunter_cid_9a680)
(0x0809a694, 0x00001415, RED_MOON_BABY_CID, eval_equip_pair_red_moon_baby_cid_9a694)
(0x0809a6b8, 0x000017d8, MYSTIC_SWORDSMAN_LV4_CID, eval_equip_pair_mystic_swordsman_lv4_cid_9a6b8)
(0x0809a6c8, 0x000017da, ARMED_DRAGON_LV5_CID, eval_equip_pair_armed_dragon_lv5_cid_9a6c8)
(0x0809a7b4, 0x00000868, PLAYER_BLOCK_STRIDE, eval_equip_pair_player_stride_9a7b4)
(0x0809a7e4, 0x000017d2, HORUS_LV4_CID, eval_equip_pair_horus_lv4_cid_9a7e4)
(0x0809a7ec, 0x00001d2c, EQUIP_CHAIN_ACTIVE_OFF, eval_equip_pair_chain_active_from_lp_offset_9a7ec)
(0x0809a8e0, 0x000001ff, EQUIP_PAYLOAD_LOW9_MASK, eval_equip_pair_payload_low9_mask_9a8e0)
(0x0809a8e4, 0xffffbfff, SLOT_ACTIVE_BIT14_CLR, eval_equip_pair_slot_active_bit14_clr_9a8e4)
(0x0809a8e8, 0xff87ffff, OAM_SPRITE_ATTR_CLR_BITS22_19, eval_equip_pair_oam_sprite_attr_clr_bits22_19_9a8e8)
(0x0809a8ec, 0x000016f8, DARK_MAGICIAN_OF_CHAOS_CID, eval_equip_pair_dark_magician_of_chaos_cid_9a8ec)
(0x0809a8f0, 0x00001332, BANISHER_OF_THE_LIGHT_CID, eval_equip_pair_banisher_of_the_light_cid_9a8f0)
(0x0809a8f4, 0x000015d9, DD_CRAZY_BEAST_CID, eval_equip_pair_dd_crazy_beast_cid_9a8f4)
(0x0809a8f8, 0x0000147a, MYSTICAL_BEAST_SERKET_CID, eval_equip_pair_mystical_beast_serket_cid_9a8f8)
(0x0809a90c, 0x000016f8, DARK_MAGICIAN_OF_CHAOS_CID, eval_equip_pair_dark_magician_of_chaos_cid_9a90c)
(0x0809a910, 0x000018e6, HOLY_KNIGHT_ISHZARK_CID, eval_equip_pair_holy_knight_ishzark_cid_9a910)
(0x0809a968, 0x0000174b, NEEDLE_BURROWER_CID, eval_equip_pair_needle_burrower_cid_9a968)
(0x0809a96c, 0x0000147a, MYSTICAL_BEAST_SERKET_CID, eval_equip_pair_mystical_beast_serket_cid_9a96c)
(0x0809a97c, 0x00001592, WINGED_SAGE_FALCOS_CID, eval_equip_pair_winged_sage_falcos_cid_9a97c)
(0x0809a998, 0x00001704, INSECT_PRINCESS_CID, eval_equip_pair_insect_princess_cid_9a998)
(0x0809a9ac, 0x0000170b, GUARDIAN_ANGEL_JOAN_CID, eval_equip_pair_guardian_angel_joan_cid_9a9ac)
(0x0809a9d4, 0x000018c8, ELEMENTAL_HERO_FLAME_WINGMAN_CID, eval_equip_pair_elemental_hero_flame_wingman_cid_9a9d4)
(0x0809a9d8, 0x000017c8, SPHINX_TELEIA_CID, eval_equip_pair_sphinx_teleia_cid_9a9d8)
(0x0809a9e0, 0x000018ae, MILLENNIUM_SCORPION_CID, eval_equip_pair_millennium_scorpion_cid_9a9e0)
(0x0809a9fc, 0x00001987, ELEMENTAL_HERO_STEAM_HEALER_CID, eval_equip_pair_elemental_hero_steam_healer_cid_9a9fc)
(0x0809aa10, 0x000019a4, HAMON_LORD_CID, eval_equip_pair_hamon_lord_cid_9aa10)
(0x0809aae4, 0x2c200000, EQUIP_ACTIVATION_PACKED_TYPE22, eval_equip_pair_packed_type22_9aae4)
(0x0809aaec, 0x00000868, PLAYER_BLOCK_STRIDE, eval_equip_pair_player_stride_9aaec)
(0x0809aaf8, 0xffffeb50, NODE_POOL_NEG_OFFSET, eval_equip_pair_node_pool_to_field_negative_offset_9aaf8)
(0x0809ab00, 0x000015d5, DES_DENDLE_CID, eval_equip_pair_des_dendle_cid_9ab00)
(0x0809ab14, 0x000018d0, LEGENDARY_BLACK_BELT_CID, eval_equip_pair_legendary_black_belt_cid_9ab14)
(0x0809ab3c, 0x000015b3, Z_METAL_TANK_CID, eval_equip_pair_z_metal_tank_cid_9ab3c)
(0x0809abd0, 0x2c200000, EQUIP_ACTIVATION_PACKED_TYPE22, eval_equip_pair_packed_type22_9abd0)
(0x0809abd4, 0x00000868, PLAYER_BLOCK_STRIDE, eval_equip_pair_player_stride_9abd4)
(0x0809ac98, 0x000001ff, EQUIP_PAYLOAD_LOW9_MASK, eval_equip_pair_payload_low9_mask_9ac98)
(0x0809ac9c, 0xffffbfff, SLOT_ACTIVE_BIT14_CLR, eval_equip_pair_slot_active_bit14_clr_9ac9c)
(0x0809aca0, 0xff87ffff, OAM_SPRITE_ATTR_CLR_BITS22_19, eval_equip_pair_oam_sprite_attr_clr_bits22_19_9aca0)
(0x0809aca4, 0x000016f8, DARK_MAGICIAN_OF_CHAOS_CID, eval_equip_pair_dark_magician_of_chaos_cid_9aca4)
(0x0809aca8, 0x00001332, BANISHER_OF_THE_LIGHT_CID, eval_equip_pair_banisher_of_the_light_cid_9aca8)
(0x0809acac, 0x000015d9, DD_CRAZY_BEAST_CID, eval_equip_pair_dd_crazy_beast_cid_9acac)
(0x0809acb0, 0x0000147a, MYSTICAL_BEAST_SERKET_CID, eval_equip_pair_mystical_beast_serket_cid_9acb0)
(0x0809acc4, 0x000016f8, DARK_MAGICIAN_OF_CHAOS_CID, eval_equip_pair_dark_magician_of_chaos_cid_9acc4)
(0x0809acc8, 0x000018e6, HOLY_KNIGHT_ISHZARK_CID, eval_equip_pair_holy_knight_ishzark_cid_9acc8)
(0x0809ad1c, 0x0000172b, EMES_THE_INFINITY_CID, eval_equip_pair_emes_the_infinity_cid_9ad1c)
(0x0809ad20, 0x0000147a, MYSTICAL_BEAST_SERKET_CID, eval_equip_pair_mystical_beast_serket_cid_9ad20)
(0x0809ad30, 0x00001592, WINGED_SAGE_FALCOS_CID, eval_equip_pair_winged_sage_falcos_cid_9ad30)
(0x0809ad48, 0x000016c6, FENRIR_CID, eval_equip_pair_fenrir_cid_9ad48)
(0x0809ad58, 0x00001704, INSECT_PRINCESS_CID, eval_equip_pair_insect_princess_cid_9ad58)
(0x0809ad78, 0x000018ae, MILLENNIUM_SCORPION_CID, eval_equip_pair_millennium_scorpion_cid_9ad78)
(0x0809ad7c, 0x00001792, ABSORBING_KID_FROM_THE_SKY_CID, eval_equip_pair_absorbing_kid_from_the_sky_cid_9ad7c)
(0x0809ad90, 0x000017c8, SPHINX_TELEIA_CID, eval_equip_pair_sphinx_teleia_cid_9ad90)
(0x0809ada8, 0x0000194f, HYDROGEDDON_CID, eval_equip_pair_hydrogeddon_cid_9ada8)
(0x0809adc0, 0x000019a4, HAMON_LORD_CID, eval_equip_pair_hamon_lord_cid_9adc0)
(0x0809add0, 0x000019d3, DIVINE_DRAGON_EXCELION_CID, eval_equip_pair_divine_dragon_excelion_cid_9add0)
(0x0809aeac, 0x2c200000, EQUIP_ACTIVATION_PACKED_TYPE22, eval_equip_pair_packed_type22_9aeac)
(0x0809aeb0, 0x0000ffff, SPRITE_LOW_HALF_MASK, eval_equip_pair_sprite_low_half_mask_9aeb0)
(0x0809aeb8, 0x00000868, PLAYER_BLOCK_STRIDE, eval_equip_pair_player_stride_9aeb8)
(0x0809aec4, 0xffffeb50, NODE_POOL_NEG_OFFSET, eval_equip_pair_node_pool_to_field_negative_offset_9aec4)
(0x0809aecc, 0x000018d0, LEGENDARY_BLACK_BELT_CID, eval_equip_pair_legendary_black_belt_cid_9aecc)
(0x0809aed0, 0x000015d1, cid_15d1_zombie_tiger, eval_equip_pair_zombie_tiger_cid_9aed0)
(0x0809aee4, 0x0000197c, ARMED_CHANGER_CID, eval_equip_pair_armed_changer_cid_9aee4)
(0x0809af0c, 0x000015b3, Z_METAL_TANK_CID, eval_equip_pair_z_metal_tank_cid_9af0c)
(0x0809b01c, 0x2c200000, EQUIP_ACTIVATION_PACKED_TYPE22, eval_equip_pair_packed_type22_9b01c)
(0x0809b020, 0x00000868, PLAYER_BLOCK_STRIDE, eval_equip_pair_player_stride_9b020)
(0x0809b02c, 0x000015b3, Z_METAL_TANK_CID, eval_equip_pair_z_metal_tank_cid_9b02c)
(0x0809b030, 0x00001658, THOUSAND_NEEDLES_CID, eval_equip_pair_thousand_needles_cid_9b030)
(0x0809b034, 0x0000152c, GIANT_AXE_MUMMY_CID, eval_equip_pair_giant_axe_mummy_cid_9b034)
(0x0809b048, 0x000016b7, DES_KANGAROO_CID, eval_equip_pair_des_kangaroo_cid_9b048)
(0x0809b164, 0x00001493, DESTRUCTION_PUNCH_CID, eval_equip_pair_destruction_punch_cid_9b164)
(0x0809b168, 0x0000162e, CONTINUOUS_DESTRUCTION_PUNCH_CID, eval_equip_pair_continuous_destruction_punch_cid_9b168)
(0x0809b16c, 0x00001883, CROSS_COUNTER_CID, eval_equip_pair_cross_counter_cid_9b16c)
(0x0809b174, 0x00001d2c, EQUIP_CHAIN_ACTIVE_OFF, eval_equip_pair_chain_active_from_lp_offset_9b174)
```

### REF_SLOTS (USER-label + DATA-ref)

33槽, 全部RAM指针. 格式 `(slot, target, gas_label, slot_label)`.

```text
(0x0809a200, 0x0201bb90, gEquipChainSlotRefs, eval_equip_pair_chain_base_9a200)
(0x0809a208, 0x0201c510, gDuelFieldSlots, eval_equip_pair_field_slots_base_9a208)
(0x0809a244, 0x0201c510, gDuelFieldSlots, eval_equip_pair_field_slots_base_9a244)
(0x0809a330, 0x0201bc68, gDuelEffectChainSlotsSecond, eval_equip_pair_effect_chain_second_slot_9a330)
(0x0809a334, 0x0201bc54, gDuelEffectChainSlots, eval_equip_pair_effect_chain_slots_base_9a334)
(0x0809a33c, 0x0201c510, gDuelFieldSlots, eval_equip_pair_field_slots_base_9a33c)
(0x0809a4e8, 0x0201bb90, gEquipChainSlotRefs, eval_equip_pair_chain_base_9a4e8)
(0x0809a518, 0x0201bb90, gEquipChainSlotRefs, eval_equip_pair_chain_base_9a518)
(0x0809a574, 0x0201bb90, gEquipChainSlotRefs, eval_equip_pair_chain_base_9a574)
(0x0809a5b0, 0x0201bb90, gEquipChainSlotRefs, eval_equip_pair_chain_base_9a5b0)
(0x0809a5b8, 0x0201c510, gDuelFieldSlots, eval_equip_pair_field_slots_base_9a5b8)
(0x0809a5f4, 0x0201bb90, gEquipChainSlotRefs, eval_equip_pair_chain_base_9a5f4)
(0x0809a634, 0x0201bb90, gEquipChainSlotRefs, eval_equip_pair_chain_base_9a634)
(0x0809a678, 0x0201bb90, gEquipChainSlotRefs, eval_equip_pair_chain_base_9a678)
(0x0809a6e8, 0x0201bb90, gEquipChainSlotRefs, eval_equip_pair_chain_base_9a6e8)
(0x0809a718, 0x0201bb90, gEquipChainSlotRefs, eval_equip_pair_chain_base_9a718)
(0x0809a774, 0x0201bb90, gEquipChainSlotRefs, eval_equip_pair_chain_base_9a774)
(0x0809a7b0, 0x0201bb90, gEquipChainSlotRefs, eval_equip_pair_chain_base_9a7b0)
(0x0809a7b8, 0x0201c510, gDuelFieldSlots, eval_equip_pair_field_slots_base_9a7b8)
(0x0809a7e0, 0x0201bb90, gEquipChainSlotRefs, eval_equip_pair_chain_base_9a7e0)
(0x0809aae8, 0x0201bb90, gEquipChainSlotRefs, eval_equip_pair_chain_base_9aae8)
(0x0809aaf0, 0x0201c510, gDuelFieldSlots, eval_equip_pair_field_slots_base_9aaf0)
(0x0809aaf4, 0x0201d9c0, gEquipNodePool, eval_equip_pair_node_pool_base_9aaf4)
(0x0809aafc, 0x0201c520, gDuelFieldSlotState, eval_equip_pair_field_state_base_9aafc)
(0x0809abd8, 0x0201c510, gDuelFieldSlots, eval_equip_pair_field_slots_base_9abd8)
(0x0809aeb4, 0x0201bb90, gEquipChainSlotRefs, eval_equip_pair_chain_base_9aeb4)
(0x0809aebc, 0x0201c510, gDuelFieldSlots, eval_equip_pair_field_slots_base_9aebc)
(0x0809aec0, 0x0201d9c0, gEquipNodePool, eval_equip_pair_node_pool_base_9aec0)
(0x0809aec8, 0x0201c520, gDuelFieldSlotState, eval_equip_pair_field_state_base_9aec8)
(0x0809b024, 0x0201c510, gDuelFieldSlots, eval_equip_pair_field_slots_base_9b024)
(0x0809b028, 0x0201e1c8, gEquipZoneCountTable, eval_equip_pair_zone_count_table_base_9b028)
(0x0809b058, 0x0201bb90, gEquipChainSlotRefs, eval_equip_pair_chain_base_9b058)
(0x0809b160, 0x0201bb90, gEquipChainSlotRefs, eval_equip_pair_chain_base_9b160)
```

REF实施和导出要求:

- 每个RAM目标使用指定USER_DEFINED LABEL主符号. 复用既有目标名; 唯一新增目标为gDuelEffectChainSlotsSecond. 不把gDuelEffectChainSlotsSecond等同某个固定player侧, 它是两条临时记录中的第二条.
- 每槽operand0必须有到列出目标的DATA/USER_DEFINED引用. 已有同目标DEFAULT引用时精确移除该operand0引用并重建, 不依赖addMemoryReference合并后提升source. 保留其他operand及非目标引用.
- 正式导出必须得到 `.word <gas_label>`, 数值由现有或NEW的 `.equ` 解析. REF后校验from/to/operand/type/source以及目标LABEL主符号.
- 当前ExportRangeToGas只按USER_DEFINED LABEL输出符号, 排除ROM FUNCTION, sanitize_label会改写加号. 本段没有THUMB函数指针槽, 不建立奇地址标签, 不需要callback equate, 不承诺REF自动输出fn+1, 不修改exporter.
- 本段无switch表或namespace表标签需要规范化; 不增加同址别名或改动已有函数主符号.

### RENAME_SLOTS (纯改名 + ASCII EOL)

3槽. 现有 `.word gP1LifePoints` 保持其符号表达式/目标/值/引用. 只改池槽名字和以下EOL, 不重复计入REF.

```text
(0x0809a3e0, eval_equip_pair_lp_base_9a3e0, "gP1LifePoints base; paired offset selects the equip display phase word.")
(0x0809a7e8, eval_equip_pair_lp_base_9a7e8, "gP1LifePoints base; paired offset selects the equip display phase word.")
(0x0809b170, eval_equip_pair_lp_base_9b170, "gP1LifePoints base; paired offset selects the equip display phase word.")
```

### FUNC_RENAME

none. 主函数现名保留, plate明确它的paired eligibility处理包含相位推进、显示及激活副作用, 不将其描述为纯predicate. increment_counter_at_ptr准确描述r1字递增动作; plate限定为共享相位返回尾, 不再称独立leaf. restore_callee_high_regs_from_frame准确描述保存帧恢复, plate明确0x48局部栈和两种返回值来源. 不新增/删除/改名函数, 不需要naming-proposals.csv同步.

入度区分: 主入口文本直接BL=0, ROM THUMB表引用=1; increment_counter_at_ptr文本BL=2+自然续接1; restore_callee_high_regs_from_frame文本BL=1+自然续接1. 后两者的BL都来自主入口逻辑, 共享的是原始caller栈帧, 不是普通可调用子程序.

### PLATE (R5, full ASCII rewrite)

仅以下三个地址整段替换. 字符数不含fence, 每条<=500. 不触碰Seg-7/Seg-9 plate.

#### 0x0809a1a4 (481 chars)

```text
Ticks paired equip display for r0=player_side with 0x38-byte contexts at gDuelEquipCtx. Phase is [gDuelFieldSlots+EQUIP_CHAIN_ACTIVE_FROM_FIELD_OFF]. Phase 0 sets special-card context flags; phase 1 queues card-specific displays; phase 2 renders descriptors, applies type-22 activations, walks equip nodes, and updates bitmaps. Phases 0..2 increment phase and return 0; nonzero gEquipChainSlotRefs[+8] or other phases return 1. Uses shared return tails and a 0x48-byte local frame.
```

#### 0x0809b146 (393 chars)

```text
Shared phase-advance tail of eval_equip_slot_pair_eligibility; requires its existing stack frame. r1 points to [gP1LifePoints+EQUIP_CHAIN_ACTIVE_OFF]. Increments that word, sets r0=0, then falls through to restore_callee_high_regs_from_frame to return to the original caller. Entered by BL at 0x0809a3d6/0x0809a7da and fall-through at 0x0809b144. This is not an independent leaf or APCS entry.
```

#### 0x0809b14e (354 chars)

```text
Shared return tail of eval_equip_slot_pair_eligibility. Releases its 0x48-byte local frame, restores r8/r9/r10 and r4-r7, then returns through the saved caller address. Preserves r0. Reached by BL at 0x0809a32c with r0=1 or by fall-through from increment_counter_at_ptr with r0=0. Requires the parent's saved frame; this is not an independent APCS entry.
```

## carve 计划 (R7)

none. 无rom.s切割, 无新增ROM数据标签或函数指针表.

## disasm 计划 (R4)

none. 不clearListing、不设TMode、不createFunction. 两个共享尾现已反汇编, 只订正plate. 指令/池/对齐连续覆盖完整段.

## 新增 constants / 全局及复用目录

全量解析 `constants/*.inc` 的5955条 `.equ/.set`, 包括十六进制、十进制、别名及表达式, 递归求值5955成功、0未解析. 逐值记录为 `seg8-constant-values-evaluated.json`. 已包含Seg-7的23个新增定义.

本段新增10常量+1 RAM全局, 共11定义; 所有NEW的值和名字在当前constants中均0命中, 无同值例外. 复用既有inc文件, 不新增include.

### NEW (按文件添加)

`constants/card_info.inc`:

```asm
.equ SWORD_HUNTER_CID, 0x000012a6  @ Sword Hunter; slot CID; card-stats.s card_0630; pw=51345461.
.equ equip_pair_cid_13b0, 0x000013b0  @ Unassigned internal card ID 0x13b0; cards-ids-array.s maps to 0xffff.
.equ RIGRAS_LEEVER_CID, 0x000013b4  @ Rigras Leever; slot CID; card-stats.s card_0834; pw=39180960.
.equ GIANT_AXE_MUMMY_CID, 0x0000152c  @ Giant Axe Mummy; slot CID; card-stats.s card_1106; pw=78266168.
.equ WINGED_SAGE_FALCOS_CID, 0x00001592  @ Winged Sage Falcos; slot CID; card-stats.s card_1174; pw=87523462.
.equ THOUSAND_NEEDLES_CID, 0x00001658  @ Thousand Needles; slot CID; card-stats.s card_1328; pw=33977496.
.equ DES_KANGAROO_CID, 0x000016b7  @ Des Kangaroo; slot CID; card-stats.s card_1403; pw=78613627.
.equ NEEDLE_BURROWER_CID, 0x0000174b  @ Needle Burrower; slot CID; card-stats.s card_1526; pw=98162242.
.equ ABSORBING_KID_FROM_THE_SKY_CID, 0x00001792  @ Absorbing Kid from the Sky; slot CID; card-stats.s card_1578; pw=49771608.
```

`constants/duel_field.inc`:

```asm
.equ EQUIP_ACTIVATION_PACKED_TYPE22, 0x2c200000  @ Packed activation: type 22 in bits 30:25 plus bit21; record +2 bits 11:6 = 22, +3 bits 5:4 = 1.
```

`constants/ewram.inc`:

```asm
.equ gDuelEffectChainSlotsSecond, 0x0201bc68  @ Second 0x14-byte effect-context slot at gDuelEffectChainSlots+0x14; paired-slot fallback record, not a fixed player-side base.
```

中性常量使用 `equip_pair_cid_13b0` 前缀避开现有 `asm/05_equip_eligibility_a.s:20492` 的池标签 `cid_13b0`. 该旧符号是ROM池地址, 不是值为0x13b0的equate; 不移动或重命名旧槽.

### REUSE (名字/数值均保持)

| value | symbol | 既有定义 |
|---|---|---|
| 0x000001ff | EQUIP_PAYLOAD_LOW9_MASK | constants/duel_field.inc:584 |
| 0x00000868 | PLAYER_BLOCK_STRIDE | constants/ewram.inc:251 |
| 0x00001332 | BANISHER_OF_THE_LIGHT_CID | constants/card_info.inc:452 |
| 0x000013a4 | THUNDER_NYAN_NYAN_CID | constants/card_info.inc:1836 |
| 0x00001415 | RED_MOON_BABY_CID | constants/card_info.inc:1175 |
| 0x0000146f | CATHEDRAL_OF_NOBLES_CID | constants/card_info.inc:962 |
| 0x0000147a | MYSTICAL_BEAST_SERKET_CID | constants/card_info.inc:1838 |
| 0x00001493 | DESTRUCTION_PUNCH_CID | constants/card_info.inc:1894 |
| 0x00001529 | GREAT_DEZARD_CID | constants/card_info.inc:809 |
| 0x000015b3 | Z_METAL_TANK_CID | constants/card_info.inc:865 |
| 0x000015d1 | cid_15d1_zombie_tiger | constants/card_info.inc:1687 |
| 0x000015d5 | DES_DENDLE_CID | constants/card_info.inc:871 |
| 0x000015d9 | DD_CRAZY_BEAST_CID | constants/card_info.inc:1975 |
| 0x0000162e | CONTINUOUS_DESTRUCTION_PUNCH_CID | constants/card_info.inc:1895 |
| 0x000016c6 | FENRIR_CID | constants/card_info.inc:1217 |
| 0x000016f8 | DARK_MAGICIAN_OF_CHAOS_CID | constants/card_info.inc:247 |
| 0x00001704 | INSECT_PRINCESS_CID | constants/card_info.inc:1413 |
| 0x0000170b | GUARDIAN_ANGEL_JOAN_CID | constants/card_info.inc:702 |
| 0x0000172b | EMES_THE_INFINITY_CID | constants/card_info.inc:527 |
| 0x000017c8 | SPHINX_TELEIA_CID | constants/card_info.inc:264 |
| 0x000017d2 | HORUS_LV4_CID | constants/card_info.inc:675 |
| 0x000017d8 | MYSTIC_SWORDSMAN_LV4_CID | constants/card_info.inc:678 |
| 0x000017da | ARMED_DRAGON_LV5_CID | constants/card_info.inc:679 |
| 0x00001836 | EQUIP_ELIG_EXCL_B | constants/card_info.inc:133 |
| 0x00001883 | CROSS_COUNTER_CID | constants/card_info.inc:1892 |
| 0x000018ae | MILLENNIUM_SCORPION_CID | constants/card_info.inc:543 |
| 0x000018c8 | ELEMENTAL_HERO_FLAME_WINGMAN_CID | constants/card_info.inc:1299 |
| 0x000018d0 | LEGENDARY_BLACK_BELT_CID | constants/card_info.inc:878 |
| 0x000018e6 | HOLY_KNIGHT_ISHZARK_CID | constants/card_info.inc:1979 |
| 0x0000194f | HYDROGEDDON_CID | constants/card_info.inc:943 |
| 0x0000197c | ARMED_CHANGER_CID | constants/card_info.inc:1810 |
| 0x00001987 | ELEMENTAL_HERO_STEAM_HEALER_CID | constants/card_info.inc:770 |
| 0x000019a4 | HAMON_LORD_CID | constants/card_info.inc:207 |
| 0x000019d3 | DIVINE_DRAGON_EXCELION_CID | constants/card_info.inc:1351 |
| 0x00001cfc | EQUIP_CHAIN_ACTIVE_FROM_FIELD_OFF | constants/duel_field.inc:575 |
| 0x00001d2c | EQUIP_CHAIN_ACTIVE_OFF | constants/duel_field.inc:230 |
| 0x0000ffff | SPRITE_LOW_HALF_MASK | constants/duel_field.inc:557 |
| 0x0201bb90 | gEquipChainSlotRefs | constants/ewram.inc:317 |
| 0x0201bc54 | gDuelEffectChainSlots | constants/ewram.inc:319 |
| 0x0201c4e0 | gP1LifePoints | constants/ewram.inc:79 |
| 0x0201c510 | gDuelFieldSlots | constants/ewram.inc:314 |
| 0x0201c520 | gDuelFieldSlotState | constants/ewram.inc:318 |
| 0x0201d9c0 | gEquipNodePool | constants/ewram.inc:316 |
| 0x0201e1c8 | gEquipZoneCountTable | constants/ewram.inc:397 |
| 0xff87ffff | OAM_SPRITE_ATTR_CLR_BITS22_19 | constants/oam_attr.inc:76 |
| 0xffffbfff | SLOT_ACTIVE_BIT14_CLR | constants/duel_field.inc:232 |
| 0xffffeb50 | NODE_POOL_NEG_OFFSET | constants/duel_field.inc:144 |

复用域核对:

- 0x1cfc对应gDuelFieldSlots+0x1cfc=0x0201e20c, 与gP1LifePoints+0x1d2c是同一相位字. 复用Seg-6新增EQUIP_CHAIN_ACTIVE_FROM_FIELD_OFF; 不用同值DISP_SET_VARIANT_OFF (基址gP1LifePoints). 三个0x1d2c槽则确实与gP1LifePoints相加, 使用EQUIP_CHAIN_ACTIVE_OFF.
- 0x0201e1c8同时有EQUIP_ZONE_COUNT_TABLE和gEquipZoneCountTable. 此处是RAM指针, 选择USER LABEL gEquipZoneCountTable并DATA-ref; 消费者读取该地址的首字后XOR循环index选player, 不把常量值当地址偏移.
- 0xffffeb50为32位二补数-0x14b0. gEquipNodePool(0x0201d9c0)+NODE_POOL_NEG_OFFSET=0x0201c510. 两槽分别保留node_pool_base和node_pool_to_field_negative_offset, 不能用单个gDuelFieldSlots值替掉任一原槽.
- 0x1ff复用Seg-7的EQUIP_PAYLOAD_LOW9_MASK. 本段从context+c取entity低9位, 拼装r6 descriptor, 既用于render_slot_card_sprite_from_descriptor也作为r2 extra_payload传给激活wrapper; 与Seg-7 payload域一致, 不用OAM_ATTR1_X_MASK.
- 0xffff在0x0809aeb0用于AND card ID后OR进packed activation word, 与另一侧ldrh取16位的路径配对. 这是低半字保留操作, 复用SPRITE_LOW_HALF_MASK, 不用SLOT_CARD_EMPTY或计数上限名称.
- 0xff87ffff和0xffffbfff是descriptor位清除, 复用OAM_SPRITE_ATTR_CLR_BITS22_19与SLOT_ACTIVE_BIT14_CLR. 不从名称之外继承其他使用点的业务解释.
- 0x1836的既有CID常量是EQUIP_ELIG_EXCL_B, card-stats.s确认Fox Fire. 复用该常量, 两个新池名明确fox_fire_cid, 不另建FOX_FIRE_CID重复定义.
- 0x15d1复用既有cid_15d1_zombie_tiger; 不因大小写或命名风格不同再造ZOMBIE_TIGER_CID.
- 0x13b0由cards-ids-array.s:1050映射0xffff, card-stats.s无slot记录. 依据活动文档L34的未分配ID规则使用中性equip_pair_cid_13b0; 算术派生的0x13ad比较不构成新的literal槽, 不猜卡名.

## 5.1 登记 (Rule 3)

none. 全段无未引用裸块. 两共享尾具有直接控制流引用, 不登记为0引用数据.

## 消费者证据 (R6)

行号对应本提案读取的最终Seg-7之后 `asm/12_equip_activation_scan.s`. 每个槽的全部使用点保存在 `seg8-plan.json`; 每条四元组仍须按本槽独立施加, 同值其他段不受影响.

### 状态、内存结构与相位

| 项目 | 直接证据 | 结论 | 置信度 |
|---|---|---|---|
| 输入/上下文 | asm/12_equip_activation_scan.s:12910..12928 | r0保存到sp+1c; chain+4保存到sp+20; current/other context以chain+2c为base, 索引步长0x38, 不是gDuelBattleState或0x14 | high |
| 现场/替代槽 | asm/12_equip_activation_scan.s:12929..12992 | context+2c为0时选gDuelFieldSlots+(side&1)*0x868+slot*0x14; 非0时选gDuelEffectChainSlots或其第二记录, 保存到sp+28/sp+2c | high |
| 新RAM第二记录 | asm/12_equip_activation_scan.s:12988..12992,13014..13026,13110..13113; constants/ewram.inc:319..320 | 0x0201bc68=0x0201bc54+0x14; 对第二记录首半字低13位判非零, 与第一记录检查对称 | high |
| 两组局部状态 | asm/12_equip_activation_scan.s:12993..13090 | sp+30/sp+34记录context+30为0且fallback记录有card; sp+38/sp+3c记录现场entity匹配且slot+8非零, 后续显示/触发分支使用这些布尔值 | high |
| 相位基址 | asm/12_equip_activation_scan.s:13091..13119 | chain+8非0直接完成; 否则从gDuelFieldSlots+0x1cfc分派phase0/1/2, 其他值完成 | high |
| phase0 | asm/12_equip_activation_scan.s:13120..13201; asm/11_effect_slot_puzzletext.s:20791..20838 | Thunder Nyan Nyan / Mystical Beast Serket通过各自门控后把context+30写1; r9是常量1, 不是slot_idx; 末尾递增相位并返回0 | high |
| phase1第一侧 | asm/12_equip_activation_scan.s:13202..13458 | sp+30门控; 当前card和另一context的card驱动enqueue模式、type11、ID lookup及装备卡显示 | high |
| phase1第二侧 | asm/12_equip_activation_scan.s:13459..13739 | sp+34对称门控并检查卡号; 对两侧显示后BL共享前缀推进相位并返回0 | high |
| phase2 descriptor | asm/12_equip_activation_scan.s:13740..13905,14235..14407 | bracket起点increment_lp_bar_display_counter; 根据context+30/+2c路径选择bitmap/临时记录或r6 descriptor; descriptor低9=entity, bit9=侧, bits13:10=slot, bit14来自context+8, bit15/16/17置1, bit18为另侧 | high |
| descriptor高字段 | asm/12_equip_activation_scan.s:13812..13901,14317..14407 | 先用0xff87ffff清bits22:19再设0x700000; field8==9、Dark Magician of Chaos、Banisher及对方卡号检查可将其设0x780000 | high |
| packed type22 | asm/12_equip_activation_scan.s:14033..14047,14200..14229,14541..14557,14726..14755; asm/06_equip_eligibility_b.s:18716..18746 | 0x2c200000=(22<<25) OR (1<<21); 配合side/slot/card字段后送apply_equip_activation_with_id_lookup; unpack得到type22及bit21模式1 | high |
| 卡ID低16掩码 | asm/12_equip_activation_scan.s:14541..14557与14033..14047 | 第二侧AND0xffff对应第一侧ldrh context+10, 装入packed word低半字; 不是空卡比较或数值上限 | high |
| node池/负偏移 | asm/12_equip_activation_scan.s:14057..14234,14567..14760 | field slot+a为链首, 节点stride8, +6为next; 节点低nibble类型只取10/11; node_pool+负偏移返回field base, +0x10全局取并行state位; 符合既有node结构 | high |
| 两侧slot扫描 | asm/12_equip_activation_scan.s:14765..14811 | gEquipZoneCountTable首字XOR0/1选两侧, 遍历slot5..9, 对Z-Metal Tank链命中排bitmap更新 | high |
| 末段专用触发 | asm/12_equip_activation_scan.s:14812..14982 | 相对context字段/侧与卡ID检查, 随后Destruction Punch/Continuous Destruction Punch/Cross Counter链门控显示及bitmap更新 | high |
| phase2尾 | asm/12_equip_activation_scan.s:14983..15018 | decrement_lp_bar_display_counter后构造gP1LifePoints+EQUIP_CHAIN_ACTIVE_OFF, 自然续接共享前缀, 相位++且返回0 | high |
| 共享尾栈契约 | asm/12_equip_activation_scan.s:12904..12910,13107..13109,13190..13195,13726..13731,14989..15005 | 仅主入口push并sub sp,#0x48; BL收尾不返回BL后地址, 而是释放原frame并pop原caller PC; 保留r0=0/1 | high |

### NEW来源

| symbol | value | 本地证据 | 置信度 |
|---|---|---|---|
| SWORD_HUNTER_CID | 0x000012a6 | data/card-stats.s:8205 (card_0630, pw=51345461) | high |
| equip_pair_cid_13b0 | 0x000013b0 | data/cards-ids-array.s:1050 -> 0xffff; card-stats.s has no matching slot | high |
| RIGRAS_LEEVER_CID | 0x000013b4 | data/card-stats.s:10857 (card_0834, pw=39180960) | high |
| GIANT_AXE_MUMMY_CID | 0x0000152c | data/card-stats.s:14393 (card_1106, pw=78266168) | high |
| WINGED_SAGE_FALCOS_CID | 0x00001592 | data/card-stats.s:15277 (card_1174, pw=87523462) | high |
| THOUSAND_NEEDLES_CID | 0x00001658 | data/card-stats.s:17279 (card_1328, pw=33977496) | high |
| DES_KANGAROO_CID | 0x000016b7 | data/card-stats.s:18254 (card_1403, pw=78613627) | high |
| NEEDLE_BURROWER_CID | 0x0000174b | data/card-stats.s:19853 (card_1526, pw=98162242) | high |
| ABSORBING_KID_FROM_THE_SKY_CID | 0x00001792 | data/card-stats.s:20529 (card_1578, pw=49771608) | high |
| EQUIP_ACTIVATION_PACKED_TYPE22 | 0x2c200000 | asm/12_equip_activation_scan.s:14033..14047,14200..14229,14541..14557,14726..14755; asm/06_equip_eligibility_b.s:18716..18746 | high |
| gDuelEffectChainSlotsSecond | 0x0201bc68 | constants/ewram.inc:319..320; asm/12_equip_activation_scan.s:12988..12992,13014..13026,13110..13113 | high |

### 卡ID与使用点

下表以ROM导出card-stats.s坐实卡名; 常量EQUIP_ELIG_EXCL_B及cid_15d1_zombie_tiger保留既有拼法. consumer行均为本段实际ldr. 同一常量用作算术比较基准时, 其literal仍以ROM存储值命名, 不把派生值替写进槽.

| constant | value | 卡表证据 | 本段consumer行 |
|---|---|---|---|
| SWORD_HUNTER_CID | 0x12a6 | data/card-stats.s:8205 card_0630 / Sword Hunter | L13272, L13538 |
| BANISHER_OF_THE_LIGHT_CID | 0x1332 | data/card-stats.s:9492 card_0729 / Banisher of the Light | L13831, L14336 |
| THUNDER_NYAN_NYAN_CID | 0x13a4 | data/card-stats.s:10688 card_0821 / Thunder Nyan Nyan | L13127, L13161 |
| equip_pair_cid_13b0 | 0x13b0 | data/cards-ids-array.s:1050 (none) | L13208, L13465 |
| RIGRAS_LEEVER_CID | 0x13b4 | data/card-stats.s:10857 card_0834 / Rigras Leever | L13223, L13484 |
| RED_MOON_BABY_CID | 0x1415 | data/card-stats.s:11663 card_0896 / Red-Moon Baby | L13287, L13554 |
| CATHEDRAL_OF_NOBLES_CID | 0x146f | data/card-stats.s:12300 card_0945 / Cathedral of Nobles | L13146, L13182 |
| MYSTICAL_BEAST_SERKET_CID | 0x147a | data/card-stats.s:12391 card_0952 / Mystical Beast Serket | L13851, L13925, L14356, L14428 |
| DESTRUCTION_PUNCH_CID | 0x1493 | data/card-stats.s:12716 card_0977 / Destruction Punch | L14908 |
| GREAT_DEZARD_CID | 0x1529 | data/card-stats.s:14354 card_1103 / Great Dezard | L13265, L13531 |
| GIANT_AXE_MUMMY_CID | 0x152c | data/card-stats.s:14393 card_1106 / Giant Axe Mummy | L14838 |
| WINGED_SAGE_FALCOS_CID | 0x1592 | data/card-stats.s:15277 card_1174 / Winged Sage Falcos | L13936, L14438 |
| Z_METAL_TANK_CID | 0x15b3 | data/card-stats.s:15641 card_1202 / Z-Metal Tank | L14179, L14696, L14793 |
| cid_15d1_zombie_tiger | 0x15d1 | data/card-stats.s:15888 card_1221 / Zombie Tiger | L14643 |
| DES_DENDLE_CID | 0x15d5 | data/card-stats.s:15940 card_1225 / Des Dendle | L14128 |
| DD_CRAZY_BEAST_CID | 0x15d9 | data/card-stats.s:15979 card_1228 / D.D. Crazy Beast | L13844, L14351 |
| CONTINUOUS_DESTRUCTION_PUNCH_CID | 0x162e | data/card-stats.s:16850 card_1295 / Continuous Destruction Punch | L14926 |
| THOUSAND_NEEDLES_CID | 0x1658 | data/card-stats.s:17279 card_1328 / Thousand Needles | L14833 |
| DES_KANGAROO_CID | 0x16b7 | data/card-stats.s:18254 card_1403 / Des Kangaroo | L14858 |
| FENRIR_CID | 0x16c6 | data/card-stats.s:18423 card_1416 / Fenrir | L14447 |
| DARK_MAGICIAN_OF_CHAOS_CID | 0x16f8 | data/card-stats.s:18956 card_1457 / Dark Magician of Chaos | L13823, L13874, L14328, L14378 |
| INSECT_PRINCESS_CID | 0x1704 | data/card-stats.s:19099 card_1468 / Insect Princess | L13945, L14460 |
| GUARDIAN_ANGEL_JOAN_CID | 0x170b | data/card-stats.s:19190 card_1475 / Guardian Angel Joan | L13960 |
| EMES_THE_INFINITY_CID | 0x172b | data/card-stats.s:19541 card_1502 / Emes the Infinity | L14410 |
| NEEDLE_BURROWER_CID | 0x174b | data/card-stats.s:19853 card_1526 / Needle Burrower | L13909 |
| ABSORBING_KID_FROM_THE_SKY_CID | 0x1792 | data/card-stats.s:20529 card_1578 / Absorbing Kid from the Sky | L14474 |
| SPHINX_TELEIA_CID | 0x17c8 | data/card-stats.s:21114 card_1623 / Sphinx Teleia | L13976, L14488 |
| HORUS_LV4_CID | 0x17d2 | data/card-stats.s:21231 card_1632 / Horus the Black Flame Dragon LV4 | L13453, L13720 |
| MYSTIC_SWORDSMAN_LV4_CID | 0x17d8 | data/card-stats.s:21309 card_1638 / Mystic Swordsman LV4 | L13298, L13565 |
| ARMED_DRAGON_LV5_CID | 0x17da | data/card-stats.s:21335 card_1640 / Armed Dragon LV5 | L13320, L13587 |
| EQUIP_ELIG_EXCL_B | 0x1836 | data/card-stats.s:22401 card_1722 / Fox Fire | L13226, L13487 |
| CROSS_COUNTER_CID | 0x1883 | data/card-stats.s:23363 card_1796 / Cross Counter | L14944 |
| MILLENNIUM_SCORPION_CID | 0x18ae | data/card-stats.s:23701 card_1822 / Millennium Scorpion | L13995, L14469 |
| ELEMENTAL_HERO_FLAME_WINGMAN_CID | 0x18c8 | data/card-stats.s:24039 card_1848 / Elemental Hero Flame Wingman | L13971 |
| LEGENDARY_BLACK_BELT_CID | 0x18d0 | data/card-stats.s:24143 card_1856 / Legendary Black Belt | L14155, L14638 |
| HOLY_KNIGHT_ISHZARK_CID | 0x18e6 | data/card-stats.s:24338 card_1871 / Holy Knight Ishzark | L13877, L14381 |
| HYDROGEDDON_CID | 0x194f | data/card-stats.s:25365 card_1950 / Hydrogeddon | L14500 |
| ARMED_CHANGER_CID | 0x197c | data/card-stats.s:25924 card_1993 / Armed Changer | L14672 |
| ELEMENTAL_HERO_STEAM_HEALER_CID | 0x1987 | data/card-stats.s:26015 card_2000 / Elemental Hero Steam Healer | L14000 |
| HAMON_LORD_CID | 0x19a4 | data/card-stats.s:26184 card_2013 / Hamon, Lord of Striking Thunder | L14016, L14513 |
| DIVINE_DRAGON_EXCELION_CID | 0x19d3 | data/card-stats.s:26717 card_2054 / Divine Dragon - Excelion | L14527 |

### 关键比较/地址机器核

- 对141条PC-relative literal load独立从ROM解码, 目标公式为 `((instruction_address+4)&~3)+(imm8<<2)`, 逐条等于其实际池槽地址. 每个131槽均有本段消费者.
- 394条B/BL从ROM解码目标, 本模块具名目标与asm标注一致; 216条条件B另外核对条件码与beq/bne/bcc/bcs/bhi/bls/bge/blt/bgt/ble等助记符一致.
- 相位比较链0x0809a31c/0x0809a320/0x0809a324及其分支证明phase0/1/2分别到0x0809a344/0x0809a3e8/0x0809a7f0. chain+8非0或phase非0..2到0x0809a32a, 设置r0=1并BL共享返回尾.
- phase0的0x13a4加0xd6确为0x147a; 0x13b0减3确为0x13ad. 类型/名称始终与literal原值绑定, 不为派生值新增槽或替换ROM字节.
- 两条node负偏移均按32位模加验证为gDuelFieldSlots; type22 bitpack按表达式逐位复核. 本段无switch, 无MOV pc, 无THUMB callback值需要转换.

## 自检与落地验收清单

- 全集131槽与EQ95/REF33/RENAME3三表并集完全相等, 地址各出现一次; ROM u32与每表value/target一致, 旧PTR没有遗漏.
- 新slot_label全部满足 `^[a-z][a-z0-9_]+$`, 名字唯一且不与当前asm标签冲突. NEW值/名字均无现有constant命中, REUSE定义值逐一相等.
- 三条plate长度481/393/354; 所有plate、3条RENAME EOL和11条新增equate注释均ASCII. 不含过时FUN_/DAT_/DWORD_引用的目标注释.
- 字节覆盖4052, 无gap/overlap, 全段注记/对齐与ROM相同; .hword71条全部属于高寄存器Thumb编码; 无裸块/switch/MOV pc.
- 留痕: `seg8-slots.json`, `seg8-card-sources.json`, `seg8-constant-values-evaluated.json`, `seg8-map-check.json`, `seg8-plan.json`, `seg8-selfcheck.json`, 均在 `output/refine-run-20260831-194634/`.
- fixer落地前读原槽名/值并检测目标符号/equate冲突; 落地后验证131槽表达式和REF DATA/USER_DEFINED source, 三plate和三EOL, 不改变相邻函数/数值/指令. 正式ROM必须byte-identical, 保存后只读复核.
- 本提案未build, 未声称已落地, 不stage/commit.

## 求助

none. 计划语义均有high置信度本地证据. 唯一未分配卡ID依据明确规则保留中性equip_pair_cid_13b0, 无卡名裁决需求.

## Executor Report: F12-Seg-8

- 槽: EQ=95 REF=33 RENAME=3 FUNC_RENAME=0 PLATE=3.
- carve=0 disasm=0 range 5.1=0.
- 新增constants/全局: 10 constants + gDuelEffectChainSlotsSecond.
- 求助: none.
- proposal: doc/dev/refine/F12-Seg-8.proposal.md
