# Refine Proposal: 04-Seg-8b  [0x0804640c..0x08047990)

## 段测绘

- 函数入口 x10:
  - 0x0804640c  check_slot_equip_placement_valid
  - 0x08046538  build_equip_placement_valid_bitmap
  - 0x0804659c  check_slot_equip_target_eligibility
  - 0x08046bd0  dispatch_card_effect_zone_action_by_card_id
  - 0x08047218  handle_card_effect_zone_eligibility_by_field6
  - 0x08047724  update_equip_target_bitmap_for_field
  - 0x080478fc  query_equip_target_bitmap_default
  - 0x0804790c  prepare_slot_ctx_for_equip_bitmap
  - 0x0804794c  enqueue_equip_slot_bitmap_update
  - 0x08047970  test_equip_target_slot_in_bitmap

- 残留自动名槽 x123 (含 PTR_gP1LifePoints x5, DAT_ x118)
- ROM_INCBIN / .byte 块: 0 (纯代码 + literal pool)
- §5.1 登记: 0 (无 0 引用块)

### ROM 字节全自检 (python struct.unpack_from 逐槽核对)

所有 123 槽已用 python 读 rom 验证值与 asm 注释吻合。
重点摘录 (其余见 EQ_SLOTS / REF_SLOTS 表):

| 槽地址 | ROM 值 | asm 注释 | 一致 |
|---|---|---|---|
| 0x0804650c | 0x00000868 | PLAYER_BLOCK_STRIDE | OK |
| 0x08046510 | 0x0201c510 | gDuelFieldSlots | OK |
| 0x08046518 | 0x0000169f | PANDEMONIUM_CID | OK |
| 0x0804651c | 0x00001683 | 新 CID | OK |
| 0x08046520 | 0x00001258 | 新 CID stub | OK |
| 0x08047878 | 0x0201e1c8 | gEquipZoneCountTable | OK |
| 0x080478f0 | 0x0201d5b4 | gDuelFieldSlots+EFFECT_ZONE_PARTITION_OFF | OK |

---

## 数据块分类 (Rule 2/3) -- 无 ROM_INCBIN/inter-function 数据块

段内全为代码 + 函数内 literal pool (已由函数体直接引用, 无独立数据块需 carve)。
ref-scan 不适用 (无 .byte/.incbin 块)。

---

## 符号化计划

### EQ_SLOTS (data-equate)

共 117 EQ (下表按槽升序, 含"复用"或"新建"标注)

| 槽地址 | ROM 值 | const_name | 来源 | slot_label |
|---|---|---|---|---|
| 0x0804650c | 0x00000868 | PLAYER_BLOCK_STRIDE | 复用 ewram.inc | check_slot_equip_placement_valid_stride |
| 0x08046510 | 0x0201c510 | gDuelFieldSlots | 复用 ewram.inc | check_slot_equip_placement_valid_slots |
| 0x08046514 | 0x000010a4 | EFFECT_ZONE_PARTITION_OFF | 复用 duel_field.inc | check_slot_equip_placement_valid_zone_off |
| 0x08046518 | 0x0000169f | PANDEMONIUM_CID | 复用 card_info.inc | check_slot_equip_placement_valid_cid_pandemonium |
| 0x0804651c | 0x00001683 | PANDEMONIUM_WATCHBEAR_CID | 新建 card_info.inc | check_slot_equip_placement_valid_cid_watchbear |
| 0x08046520 | 0x00001258 | (stub) check_slot_equip_placement_valid_cid_1258 | 低置信 RENAME only | check_slot_equip_placement_valid_cid_1258 |
| 0x0804663c | 0x00001825 | HEAVY_MECH_SUPPORT_PLATFORM_CID | 新建 card_info.inc | check_slot_equip_target_elig_cid_1825 |
| 0x08046698 | 0x000010d4 | EQUIP_BITMAP_CTRL_OFF | 新建 duel_field.inc | check_slot_equip_target_elig_ctrl_off |
| 0x0804669c | 0x000015e6 | AUTONOMOUS_ACTION_UNIT_CID | 新建 card_info.inc | check_slot_equip_target_elig_cid_15e6 |
| 0x080466a0 | 0x0000137d | CALL_OF_THE_HAUNTED_CID | 新建 card_info.inc | check_slot_equip_target_elig_cid_137d |
| 0x080466a8 | 0x00001366 | PREMATURE_BURIAL_CID | 新建 card_info.inc | check_slot_equip_target_elig_cid_1366_b |
| 0x080466c4 | 0x0000149a | SPIRIT_MESSAGE_L_CID | 新建 card_info.inc | check_slot_equip_target_elig_cid_149a |
| 0x080466d4 | 0x0000150e | SPIRITUAL_ENERGY_SETTLE_CID | 新建 card_info.inc | check_slot_equip_target_elig_cid_150e |
| 0x080466fc | 0x000017af | THE_FIRST_SARCOPHAGUS_CID | 新建 card_info.inc | check_slot_equip_target_elig_cid_17af |
| 0x08046700 | 0x000017ad | THE_THIRD_SARCOPHAGUS_CID | 新建 card_info.inc | check_slot_equip_target_elig_cid_17ad |
| 0x08046704 | 0x000016a2 | BATTLE_SCARRED_CID | 新建 card_info.inc | check_slot_equip_target_elig_cid_16a2 |
| 0x08046718 | 0x00001768 | NINJITSU_ART_OF_TRANSFORMATION_CID | 新建 card_info.inc | check_slot_equip_target_elig_cid_1768 |
| 0x08046738 | 0x00001881 | RE_FUSION_CID | 新建 card_info.inc | check_slot_equip_target_elig_cid_1881 |
| 0x0804674c | 0x000019d7 | SYMBOL_OF_HERITAGE_CID | 新建 card_info.inc | check_slot_equip_target_elig_cid_19d7 |
| 0x080467e4 | 0x00000868 | PLAYER_BLOCK_STRIDE | 复用 ewram.inc | check_slot_equip_target_elig_stride_b |
| 0x080467e8 | 0x0201c510 | gDuelFieldSlots | 复用 ewram.inc | check_slot_equip_target_elig_slots_b |
| 0x0804688c | 0x00000868 | PLAYER_BLOCK_STRIDE | 复用 ewram.inc | check_slot_equip_target_elig_stride_c |
| 0x08046890 | 0x0201c510 | gDuelFieldSlots | 复用 ewram.inc | check_slot_equip_target_elig_slots_c |
| 0x08046894 | 0x0000ffff | OAM_ATTR0_HIDDEN | 复用 oam_attr.inc | check_slot_equip_target_elig_no_pair_a |
| 0x08046954 | 0x00000868 | PLAYER_BLOCK_STRIDE | 复用 ewram.inc | check_slot_equip_target_elig_stride_d |
| 0x08046958 | 0x0201c510 | gDuelFieldSlots | 复用 ewram.inc | check_slot_equip_target_elig_slots_d |
| 0x0804695c | 0x0000ffff | OAM_ATTR0_HIDDEN | 复用 oam_attr.inc | check_slot_equip_target_elig_no_pair_b |
| 0x08046960 | 0x00001625 | BIG_BANG_SHOT_CID | 新建 card_info.inc | check_slot_equip_target_elig_cid_1625 |
| 0x08046964 | 0x00001881 | RE_FUSION_CID | 复用 (同段新建) | check_slot_equip_target_elig_cid_1881_b |
| 0x08046a28 | 0x00000868 | PLAYER_BLOCK_STRIDE | 复用 ewram.inc | check_slot_equip_target_elig_stride_e |
| 0x08046a2c | 0x0201c510 | gDuelFieldSlots | 复用 ewram.inc | check_slot_equip_target_elig_slots_e |
| 0x08046a30 | 0x00001468 | DESTINY_BOARD_CID | 新建 card_info.inc | check_slot_equip_target_elig_cid_1468 |
| 0x08046a34 | 0x0000149a | SPIRIT_MESSAGE_L_CID | 复用 (同段新建) | check_slot_equip_target_elig_cid_149a_b |
| 0x08046ab4 | 0x00000868 | PLAYER_BLOCK_STRIDE | 复用 ewram.inc | check_slot_equip_target_elig_stride_f |
| 0x08046ab8 | 0x0201c510 | gDuelFieldSlots | 复用 ewram.inc | check_slot_equip_target_elig_slots_f |
| 0x08046abc | 0x000017af | THE_FIRST_SARCOPHAGUS_CID | 复用 (同段新建) | check_slot_equip_target_elig_cid_17af_b |
| 0x08046ac0 | 0x000017ad | THE_THIRD_SARCOPHAGUS_CID | 复用 (同段新建) | check_slot_equip_target_elig_cid_17ad_b |
| 0x08046bc0 | 0x00000868 | PLAYER_BLOCK_STRIDE | 复用 ewram.inc | check_slot_equip_target_elig_stride_g |
| 0x08046bc4 | 0x0201c510 | gDuelFieldSlots | 复用 ewram.inc | check_slot_equip_target_elig_slots_g |
| 0x08046bc8 | 0x0000150e | SPIRITUAL_ENERGY_SETTLE_CID | 复用 (同段新建) | check_slot_equip_target_elig_cid_150e_b |
| 0x08046bcc | 0x0201d9c0 | gEquipNodePool | 复用 ewram.inc | check_slot_equip_target_elig_node_pool |
| 0x08046c38 | 0x00001625 | BIG_BANG_SHOT_CID | 复用 (同段新建) | disp_zone_action_cid_1625 |
| 0x08046c3c | 0x00001468 | DESTINY_BOARD_CID | 复用 (同段新建) | disp_zone_action_cid_1468 |
| 0x08046c40 | 0x000012d3 | AMPLIFIER_CID | 新建 card_info.inc | disp_zone_action_cid_12d3 |
| 0x08046c50 | 0x00001366 | PREMATURE_BURIAL_CID | 复用 (同段新建) | disp_zone_action_cid_1366 |
| 0x08046c74 | 0x0000150e | SPIRITUAL_ENERGY_SETTLE_CID | 复用 (同段新建) | disp_zone_action_cid_150e |
| 0x08046c84 | 0x000015e6 | AUTONOMOUS_ACTION_UNIT_CID | 复用 (同段新建) | disp_zone_action_cid_15e6 |
| 0x08046cac | 0x000017b7 | SOUL_RESURRECTION_CID | 新建 card_info.inc | disp_zone_action_cid_17b7 |
| 0x08046ce4 | 0x000017af | THE_FIRST_SARCOPHAGUS_CID | 复用 (同段新建) | disp_zone_action_cid_17af |
| 0x08046ce8 | 0x00000868 | PLAYER_BLOCK_STRIDE | 复用 ewram.inc | disp_zone_action_stride_a |
| 0x08046cec | 0x0201c510 | gDuelFieldSlots | 复用 ewram.inc | disp_zone_action_slots_a |
| 0x08046d08 | 0x00001881 | RE_FUSION_CID | 复用 (同段新建) | disp_zone_action_cid_1881 |
| 0x08046d18 | 0x000019d7 | SYMBOL_OF_HERITAGE_CID | 复用 (同段新建) | disp_zone_action_cid_19d7 |
| 0x08046da8 | 0x0201e1c8 | gEquipZoneCountTable | 复用 ewram.inc | disp_zone_action_equip_zone_tbl |
| 0x08046dac | 0x00000868 | PLAYER_BLOCK_STRIDE | 复用 ewram.inc | disp_zone_action_stride_b |
| 0x08046db0 | 0x0201c510 | gDuelFieldSlots | 复用 ewram.inc | disp_zone_action_slots_b |
| 0x08046db4 | 0x0201c520 | gDuelFieldSlotState | 复用 ewram.inc | disp_zone_action_slot_state |
| 0x08046e68 | 0x00000868 | PLAYER_BLOCK_STRIDE | 复用 ewram.inc | disp_zone_action_stride_c |
| 0x08046e6c | 0x0201c510 | gDuelFieldSlots | 复用 ewram.inc | disp_zone_action_slots_c |
| 0x08046e70 | 0x0000ffff | OAM_ATTR0_HIDDEN | 复用 oam_attr.inc | disp_zone_action_no_pair_a |
| 0x08046ef4 | 0x00000868 | PLAYER_BLOCK_STRIDE | 复用 ewram.inc | disp_zone_action_stride_d |
| 0x08046ef8 | 0x0201c510 | gDuelFieldSlots | 复用 ewram.inc | disp_zone_action_slots_d |
| 0x08046efc | 0x000017c8 | SPHINX_TELEIA_CID | 复用 card_info.inc | disp_zone_action_cid_17c8 |
| 0x08046fc4 | 0x00000868 | PLAYER_BLOCK_STRIDE | 复用 ewram.inc | disp_zone_action_stride_e |
| 0x08046fc8 | 0x0201c510 | gDuelFieldSlots | 复用 ewram.inc | disp_zone_action_slots_e |
| 0x08046fcc | 0x0000ffff | OAM_ATTR0_HIDDEN | 复用 oam_attr.inc | disp_zone_action_no_pair_b |
| 0x08046fd0 | 0x00001625 | BIG_BANG_SHOT_CID | 复用 (同段新建) | disp_zone_action_cid_1625_b |
| 0x08046fd4 | 0x00001881 | RE_FUSION_CID | 复用 (同段新建) | disp_zone_action_cid_1881_b |
| 0x08047094 | 0x00000868 | PLAYER_BLOCK_STRIDE | 复用 ewram.inc | disp_zone_action_stride_f |
| 0x08047098 | 0x0201c510 | gDuelFieldSlots | 复用 ewram.inc | disp_zone_action_slots_f |
| 0x0804709c | 0x00001468 | DESTINY_BOARD_CID | 复用 (同段新建) | disp_zone_action_cid_1468_b |
| 0x080470a0 | 0x0000149a | SPIRIT_MESSAGE_L_CID | 复用 (同段新建) | disp_zone_action_cid_149a |
| 0x08047104 | 0x000017af | THE_FIRST_SARCOPHAGUS_CID | 复用 (同段新建) | disp_zone_action_cid_17af_b |
| 0x08047108 | 0x00000868 | PLAYER_BLOCK_STRIDE | 复用 ewram.inc | disp_zone_action_stride_g |
| 0x0804710c | 0x0201c510 | gDuelFieldSlots | 复用 ewram.inc | disp_zone_action_slots_g |
| 0x08047110 | 0x000017ad | THE_THIRD_SARCOPHAGUS_CID | 复用 (同段新建) | disp_zone_action_cid_17ad |
| 0x08047204 | 0x00000868 | PLAYER_BLOCK_STRIDE | 复用 ewram.inc | disp_zone_action_stride_h |
| 0x08047208 | 0x0201c510 | gDuelFieldSlots | 复用 ewram.inc | disp_zone_action_slots_h |
| 0x0804720c | 0x0201e1c8 | gEquipZoneCountTable | 复用 ewram.inc | disp_zone_action_equip_zone_tbl_b |
| 0x08047210 | 0x0000150e | SPIRITUAL_ENERGY_SETTLE_CID | 复用 (同段新建) | disp_zone_action_cid_150e_b |
| 0x08047214 | 0x0201d9c0 | gEquipNodePool | 复用 ewram.inc | disp_zone_action_node_pool_b |
| 0x08047270 | 0x00000868 | PLAYER_BLOCK_STRIDE | 复用 ewram.inc | handle_zone_elig_stride |
| 0x08047274 | 0x0201c510 | gDuelFieldSlots | 复用 ewram.inc | handle_zone_elig_slots |
| 0x080472e4 | 0x00001825 | HEAVY_MECH_SUPPORT_PLATFORM_CID | 复用 (同段新建) | handle_zone_elig_cid_1825 |
| 0x080474ac | 0x00000868 | PLAYER_BLOCK_STRIDE | 复用 ewram.inc | handle_zone_elig_stride_b |
| 0x080474b0 | 0x000014fb | FIBER_JAR_CID | 新建 card_info.inc | handle_zone_elig_cid_14fb |
| 0x080474b4 | 0x000019e1 | GOBLIN_OUT_OF_FRYING_PAN_CID | 新建 card_info.inc | handle_zone_elig_cid_19e1 |
| 0x080474b8 | 0x000010d4 | EQUIP_BITMAP_CTRL_OFF | 复用 (同段新建) | handle_zone_elig_ctrl_off_b |
| 0x080474bc | 0x000016f8 | DARK_MAGICIAN_OF_CHAOS_CID | 复用 card_info.inc | handle_zone_elig_cid_16f8 |
| 0x080474c0 | 0x0201c510 | gDuelFieldSlots | 复用 ewram.inc | handle_zone_elig_slots_b |
| 0x080474c4 | 0xfffffe00 | OAM_ATTR1_X_CLEAR | 复用 oam_attr.inc | handle_zone_elig_x_clr |
| 0x080474c8 | 0xfffffdff | OAM_SPRITE_ATTR_CLR_BIT9 | 复用 oam_attr.inc | handle_zone_elig_clr_bit9 |
| 0x080474cc | 0xffffc3ff | OAM_SPRITE_ATTR_CLR_BITS13_10 | 复用 oam_attr.inc | handle_zone_elig_clr_bits13_10 |
| 0x080474d0 | 0xffffbfff | SLOT_ACTIVE_BIT14_CLR | 复用 duel_field.inc | handle_zone_elig_clr_bit14 |
| 0x080474d4 | 0xfffdffff | OAM_SPRITE_ATTR_CLR_BIT17 | 复用 oam_attr.inc | handle_zone_elig_clr_bit17 |
| 0x080474d8 | 0xfffbffff | OAM_SPRITE_ATTR_CLR_BIT18 | 新建 oam_attr.inc | handle_zone_elig_clr_bit18 |
| 0x080474dc | 0xffff7fff | SLOT_ACTIVE_BIT15_CLR | 复用 duel_field.inc | handle_zone_elig_clr_bit15 |
| 0x080474e0 | 0xff7fffff | SLOT_ACTIVE_BIT23_CLR | 复用 duel_field.inc | handle_zone_elig_clr_bit23 |
| 0x080474e4 | 0xff87ffff | OAM_SPRITE_ATTR_CLR_BITS22_19 | 新建 oam_attr.inc | handle_zone_elig_clr_bits22_19 |
| 0x080474e8 | 0x000010a4 | EFFECT_ZONE_PARTITION_OFF | 复用 duel_field.inc | handle_zone_elig_zone_off |
| 0x080474ec | 0x00008045 | OAM_ZONE_EQUIP_SPRITE_P1 | 复用 oam_attr.inc | handle_zone_elig_oam_zone_equip |
| 0x08047528 | 0x00008031 | OAM_EFFECT_ZONE_SPRITE_P1 | 新建 oam_attr.inc | handle_zone_elig_oam_effect_zone_p1 |
| 0x08047574 | 0x0000803d | OAM_EQUIP_CHAIN_PAIR_SPRITE_P1 | 复用 oam_attr.inc | handle_zone_elig_oam_pair_p1 |
| 0x080475a0 | 0x00008031 | OAM_EFFECT_ZONE_SPRITE_P1 | 复用 (同段新建) | handle_zone_elig_oam_effect_zone_p1_b |
| 0x080475cc | 0x00008033 | OAM_EQUIP_ZONE_SPRITE_P1 | 复用 oam_attr.inc | handle_zone_elig_oam_equip_zone |
| 0x08047618 | 0x00000868 | PLAYER_BLOCK_STRIDE | 复用 ewram.inc | handle_zone_elig_stride_c |
| 0x0804761c | 0x0201c510 | gDuelFieldSlots | 复用 ewram.inc | handle_zone_elig_slots_c |
| 0x08047708 | 0x00000868 | PLAYER_BLOCK_STRIDE | 复用 ewram.inc | handle_zone_elig_stride_d |
| 0x0804770c | 0x0201c510 | gDuelFieldSlots | 复用 ewram.inc | handle_zone_elig_slots_d |
| 0x0804786c | 0x000010d4 | EQUIP_BITMAP_CTRL_OFF | 复用 (同段新建) | upd_equip_bitmap_ctrl_off |
| 0x08047870 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | 复用 ewram.inc | upd_equip_bitmap_block2_off |
| 0x08047874 | 0x00001825 | HEAVY_MECH_SUPPORT_PLATFORM_CID | 复用 (同段新建) | upd_equip_bitmap_cid_1825 |
| 0x08047878 | 0x0201e1c8 | gEquipZoneCountTable | 复用 ewram.inc | upd_equip_bitmap_equip_zone_tbl_c |
| 0x0804787c | 0x00001332 | BANISHER_OF_THE_LIGHT_CID | 复用 card_info.inc | upd_equip_bitmap_cid_banisher |
| 0x08047880 | 0x00000868 | PLAYER_BLOCK_STRIDE | 复用 ewram.inc | upd_equip_bitmap_stride |
| 0x08047884 | 0x0201c510 | gDuelFieldSlots | 复用 ewram.inc | upd_equip_bitmap_slots |
| 0x080478f8 | 0x000010d4 | EQUIP_BITMAP_CTRL_OFF | 复用 (同段新建) | upd_equip_bitmap_ctrl_off_b |

### REF_SLOTS (USER-label + DATA-ref)

共 6 REF (standalone: PTR_gP1LifePoints x5 + compound x1; RAM/ROM 全局地址值不适合 createEquate 的直接用 .word label):

| 槽地址 | ROM 值 | gas_label | slot_label |
|---|---|---|---|
| 0x08046524 | 0x0201c4e0 | gP1LifePoints | PTR_gP1LifePoints_08046524 |
| 0x08046694 | 0x0201c4e0 | gP1LifePoints | PTR_gP1LifePoints_08046694 |
| 0x080474a8 | 0x0201c4e0 | gP1LifePoints | PTR_gP1LifePoints_080474a8 |
| 0x08047868 | 0x0201c4e0 | gP1LifePoints | PTR_gP1LifePoints_08047868 |
| 0x080478f4 | 0x0201c4e0 | gP1LifePoints | PTR_gP1LifePoints_080478f4 |
| 0x080478f0 | 0x0201d5b4 | gDuelFieldSlots+EFFECT_ZONE_PARTITION_OFF | upd_equip_bitmap_effect_zone |

Note: 0x0201d5b4 = gDuelFieldSlots(0x0201c510) + EFFECT_ZONE_PARTITION_OFF(0x000010a4). In GAS: `.word gDuelFieldSlots+EFFECT_ZONE_PARTITION_OFF` (high-conf: 0x0201c510+0x10a4=0x0201d5b4 verified).

Note: gEquipZoneCountTable (0x0201e1c8), gEquipNodePool (0x0201d9c0), gDuelFieldSlotState (0x0201c520) -- these 3 global RAM addresses appear in EQ_SLOTS (treated as numeric equates because they appear alongside other numeric constants in the same literal pool). Total 6 standalone REF slots shown above.

PTR_gP1LifePoints x5 全部 REF -> gP1LifePoints (ewram.inc 已存在; 值 0x0201c4e0 ROM 核对一致).

### RENAME_SLOTS (纯改名 + EOL)

共 23 RENAME:

| 槽地址 | ROM 值 | slot_label | eol_ascii |
|---|---|---|---|
| 0x08046520 | 0x00001258 | check_slot_equip_placement_valid_cid_1258 | card_id 0x1258: gap in card-stats.s (no name); eligibility check gP1LifePoints+off bit2 [low-conf] |
| 0x08046c38 | 0x00001625 | disp_zone_action_cid_1625 | BIG_BANG_SHOT_CID -- see card_info.inc |
| 0x08046c3c | 0x00001468 | disp_zone_action_cid_1468 | DESTINY_BOARD_CID -- see card_info.inc |
| 0x08046c40 | 0x000012d3 | disp_zone_action_cid_12d3 | AMPLIFIER_CID -- see card_info.inc |
| 0x08046c50 | 0x00001366 | disp_zone_action_cid_1366 | PREMATURE_BURIAL_CID -- see card_info.inc |
| 0x08046c74 | 0x0000150e | disp_zone_action_cid_150e | SPIRITUAL_ENERGY_SETTLE_CID -- see card_info.inc |
| 0x08046c84 | 0x000015e6 | disp_zone_action_cid_15e6 | AUTONOMOUS_ACTION_UNIT_CID -- see card_info.inc |
| 0x08046cac | 0x000017b7 | disp_zone_action_cid_17b7 | SOUL_RESURRECTION_CID -- see card_info.inc |
| 0x08046ce4 | 0x000017af | disp_zone_action_cid_17af | THE_FIRST_SARCOPHAGUS_CID -- see card_info.inc |
| 0x08046d08 | 0x00001881 | disp_zone_action_cid_1881 | RE_FUSION_CID -- see card_info.inc |
| 0x08046d18 | 0x000019d7 | disp_zone_action_cid_19d7 | SYMBOL_OF_HERITAGE_CID -- see card_info.inc |
| 0x08046efc | 0x000017c8 | disp_zone_action_cid_17c8 | SPHINX_TELEIA_CID (range upper bound [0x17c7..0x17c8]) -- card_info.inc |
| 0x08046fd0 | 0x00001625 | disp_zone_action_cid_1625_b | BIG_BANG_SHOT_CID -- see card_info.inc |
| 0x08046fd4 | 0x00001881 | disp_zone_action_cid_1881_b | RE_FUSION_CID -- see card_info.inc |
| 0x0804709c | 0x00001468 | disp_zone_action_cid_1468_b | DESTINY_BOARD_CID |
| 0x080470a0 | 0x0000149a | disp_zone_action_cid_149a | SPIRIT_MESSAGE_L_CID |
| 0x08047104 | 0x000017af | disp_zone_action_cid_17af_b | THE_FIRST_SARCOPHAGUS_CID |
| 0x08047110 | 0x000017ad | disp_zone_action_cid_17ad | THE_THIRD_SARCOPHAGUS_CID |
| 0x08047210 | 0x0000150e | disp_zone_action_cid_150e_b | SPIRITUAL_ENERGY_SETTLE_CID |
| 0x080474b0 | 0x000014fb | handle_zone_elig_cid_14fb | FIBER_JAR_CID -- see card_info.inc |
| 0x080474b4 | 0x000019e1 | handle_zone_elig_cid_19e1 | GOBLIN_OUT_OF_FRYING_PAN_CID -- see card_info.inc |
| 0x080474bc | 0x000016f8 | handle_zone_elig_cid_16f8 | DARK_MAGICIAN_OF_CHAOS_CID -- see card_info.inc |
| 0x0804787c | 0x00001332 | upd_equip_bitmap_cid_banisher | BANISHER_OF_THE_LIGHT_CID -- see card_info.inc |

### FUNC_RENAME

段内 10 函数均已命名准确; 函数体操作与函数名一致, 无误名信号。无 FUNC_RENAME 候选。

### PLATE (R5)

4 函数 plate 含 stale FUN_ 需 substring 替换 (update_equip_target_bitmap_for_field plate 无 FUN_, 免操作):

**check_slot_equip_target_eligibility (0x0804659c)**:
旧 plate 含 2 处 FUN_:
- `FUN_08047724` -> `update_equip_target_bitmap_for_field` (asm/04 同文件 confirmed)
- `FUN_08046538` -> `build_equip_placement_valid_bitmap` (asm/04 同文件 confirmed)
操作: 2-token substring 替换. 全 ASCII 无 CJK.

**dispatch_card_effect_zone_action_by_card_id (0x08046bd0)**:
旧 plate 含 8 处 FUN_:
- `FUN_08047114` -> `dispatch_card_effect_zone_action_by_card_id` (内部 LAB; addr=0x08047114 falls inside fn body [0x08046bd0..0x08047202]; plate incorrectly labels as external call)
- `FUN_080470a4` -> `dispatch_card_effect_zone_action_by_card_id` (same: internal LAB_080470a4)
- `FUN_08047218` -> `handle_card_effect_zone_eligibility_by_field6`
- `FUN_08047f50` -> `render_slot_card_sprite_from_descriptor`
- `FUN_08048020` -> `render_slot_card_sprite_and_effects`
- `FUN_08048268` -> `render_zone_sprite_with_effect_dispatch_by_slot`
- `FUN_08048364` -> `render_slot_card_sprite_with_chaos_equip_check` (asm/04 line 18223 confirmed)
- `FUN_0804559c` -> `dispatch_card_effect_sprite_render_by_card_id`
操作: 8-token substring 替换. 全 ASCII.

**handle_card_effect_zone_eligibility_by_field6 (0x08047218)**:
旧 plate 含 4 处 FUN_:
- `FUN_0804559c` -> `dispatch_card_effect_sprite_render_by_card_id`
- `FUN_08046bd0` -> `dispatch_card_effect_zone_action_by_card_id`
- `FUN_08047724` -> `update_equip_target_bitmap_for_field`
- `FUN_0804adf0` -> `check_card_field8_is_9` (asm/05_equip_eligibility_a.s line 3995 confirmed)
操作: 4-token substring 替换. 全 ASCII.

**update_equip_target_bitmap_for_field (0x08047724)**:
旧 plate 无 FUN_ (函数已命名). 但检查原始 plate 是否含 FUN_ 引用其 callee:
- 该函数 plate 已由 Seg-8a naming-phase 写入正确名. 无 stale FUN_ 待替换.
操作: 0 替换.

**test_equip_target_slot_in_bitmap (0x08047970)**:
旧 plate 含 1 处 FUN_:
- `FUN_080478fc` -> `query_equip_target_bitmap_default`
操作: 1-token substring 替换. 全 ASCII.

PLATE 汇总: 4 函数, 15 FUN_ token 替换 (2+8+4+1). update_equip_target_bitmap_for_field plate 无 FUN_. 落地后 grep Seg-8b range FUN_ == 0 验收.

---

## carve 计划 (R7) -- 无

段内无 ROM_INCBIN / inter-function 数据块; 全为代码 + 函数内 literal pool.

## disasm 计划 (R4) -- 无

段内无 .byte / ROM_INCBIN 需要 disasm. 函数内含 .hword (literal pool) 已由 Ghidra 正确识别.

---

## 新增 constants / 全局

### card_info.inc (19 新建)

| 常量名 | 值 | 卡名 | pw | card-stats.s slot |
|---|---|---|---|---|
| PANDEMONIUM_WATCHBEAR_CID | 0x00001683 | Pandemonium Watchbear | 75375465 | card_1360 |
| HEAVY_MECH_SUPPORT_PLATFORM_CID | 0x00001825 | Heavy Mech Support Platform | 23265594 | card_1705 |
| AUTONOMOUS_ACTION_UNIT_CID | 0x000015e6 | Autonomous Action Unit | 71453557 | card_1238 |
| CALL_OF_THE_HAUNTED_CID | 0x0000137d | Call of the Haunted | 97077563 | card_0793 |
| PREMATURE_BURIAL_CID | 0x00001366 | Premature Burial | 70828912 | card_0773 |
| SPIRIT_MESSAGE_L_CID | 0x0000149a | Spirit Message L | 30170981 | card_0984 |
| SPIRITUAL_ENERGY_SETTLE_CID | 0x0000150e | Spiritual Energy Settle Machine | 99173029 | card_1081 |
| THE_FIRST_SARCOPHAGUS_CID | 0x000017af | The First Sarcophagus | 31076103 | card_1605 |
| THE_THIRD_SARCOPHAGUS_CID | 0x000017ad | The Third Sarcophagus | 78697395 | card_1603 |
| BATTLE_SCARRED_CID | 0x000016a2 | Battle-Scarred | 94463200 | card_1389 |
| NINJITSU_ART_OF_TRANSFORMATION_CID | 0x00001768 | Ninjitsu Art of Transformation | 70861343 | card_1552 |
| RE_FUSION_CID | 0x00001881 | Re-Fusion | 74694807 | card_1794 |
| SYMBOL_OF_HERITAGE_CID | 0x000019d7 | Symbol of Heritage | 45305419 | card_2058 |
| BIG_BANG_SHOT_CID | 0x00001625 | Big Bang Shot | 61127349 | card_1288 |
| DESTINY_BOARD_CID | 0x00001468 | Destiny Board | 94212438 | card_0939 |
| AMPLIFIER_CID | 0x000012d3 | Amplifier | 00303660 | card_0660 |
| SOUL_RESURRECTION_CID | 0x000017b7 | Soul Resurrection | 92924317 | card_1611 |
| FIBER_JAR_CID | 0x000014fb | Fiber Jar | 78706415 | card_1062 |
| GOBLIN_OUT_OF_FRYING_PAN_CID | 0x000019e1 | Goblin Out of the Frying Pan | 69632396 | card_2068 |

Note: 0x1258 不在 card-stats.s (gap; 近邻 0x1257=Reverse Trap / 0x125a=Turtle Oath, 均无 0x1258). 以 RENAME stub `check_slot_equip_placement_valid_cid_1258` 低置信处理, 不新建常量.
Note: SPHINX_TELEIA_CID 0x17c8 已在 card_info.inc (复用, 非新建).
Note: DARK_MAGICIAN_OF_CHAOS_CID 0x16f8 已在 card_info.inc (复用).
Note: BANISHER_OF_THE_LIGHT_CID 0x1332 已在 card_info.inc (复用).
Note: PANDEMONIUM_CID 0x169f 已在 card_info.inc (复用).

C5 全自检: 以上 19 值逐一 grep constants/*.inc 无碰撞, 确认新建.

### duel_field.inc (1 新建)

| 常量名 | 值 | 说明 | ROM refs |
|---|---|---|---|
| EQUIP_BITMAP_CTRL_OFF | 0x000010d4 | [gP1LifePoints+0x10d4] equip target bitmap control word; update_equip_target_bitmap_for_field writes combined sprite flags here | 12 |

C5 全自检: EQUIP_BITMAP_CTRL_OFF 0x10d4 -- grep duel_field.inc/ewram.inc -- LP_DISCARD_ZONE_OFF=0x10dc (不同); ACTIVE_EFFECT_CATEGORY_OFF=0x10d8 (不同); 无碰撞.

### oam_attr.inc (3 新建)

| 常量名 | 值 | 说明 | ROM refs |
|---|---|---|---|
| OAM_SPRITE_ATTR_CLR_BIT18 | 0xfffbffff | AND mask clearing OAM sprite attr bit18 (zone effect flag); follows OAM_SPRITE_ATTR_CLR_BIT17 naming convention | 687 |
| OAM_SPRITE_ATTR_CLR_BITS22_19 | 0xff87ffff | AND mask clearing OAM sprite attr bits[22:19] (equip zone shape field) | 14 |
| OAM_EFFECT_ZONE_SPRITE_P1 | 0x00008031 | OAM attr0 P1 for zone effect card sprite (bit15+0x31); handle_card_effect_zone_eligibility_by_field6 field8==9 path; 55 raw ROM refs | 55 |

C5 全自检: 0xfffbffff -- grep all constants: 无碰撞 (OAM_SPRITE_ATTR_CLR_BIT17=0xfffdffff, SLOT_ACTIVE_BIT14_CLR=0xffffbfff 不同).
0xff87ffff -- grep all constants: 无碰撞.
0x8031 -- grep oam_attr.inc: 无已有常量; 最近 OAM_EQUIP_SLOT_SPRITE_P2=0x8029, OAM_ZONE_CARD_SPRITE_P1=0x8035 (不同值). 无碰撞.

---

## §5.1 登记 (Rule 3) -- 0 引用块

Seg-8b 无任何 .byte / ROM_INCBIN 块; §5.1 登记表无新条目.

---

## 消费者证据 (R6) -- 关键槽语义

| 槽/常量 | 消费者 file:line | 置信度 |
|---|---|---|
| EQUIP_BITMAP_CTRL_OFF=0x10d4 | asm/04 line 16629 `ldr r0, DAT_0804786c` -> update_equip_target_bitmap_for_field stores combined sprite flags; line 16697 same fn final read-write | high |
| HEAVY_MECH_SUPPORT_PLATFORM_CID=0x1825 | asm/04 line 14231 check_slot_equip_target_eligibility: count_equip_chain_default_flags(player,slot,0x1825); line 16700 update_equip_target_bitmap_for_field same usage | high |
| BIG_BANG_SHOT_CID=0x1625 | asm/04 line 15053 dispatch_card_effect_zone_action_by_card_id BST root; line 14670 check_slot_equip_target_eligibility side-match check | high |
| DESTINY_BOARD_CID=0x1468 | asm/04 line 14780 loop over [0x1468..0x149a] range (Destiny Board -> Spirit Message series); line 15055 dispatch cmp r8,0x1468 | high |
| 0x1258 (stub) | asm/04 line 14084 check_slot_equip_placement_valid: cmp r7,0x1258 -> gP1LifePoints+off+0x40 bit2 check | low (no card-stats.s match) |
| OAM_EFFECT_ZONE_SPRITE_P1=0x8031 | asm/04 line 16241/16313 handle_card_effect_zone_eligibility_by_field6: P1-side (r1==0) path of field8==9 sprite; sibling 0x8032 is P2 | med (pattern consistent with P1/P2 OAM convention) |
| OAM_SPRITE_ATTR_CLR_BIT18=0xfffbffff | asm/04 line 16113 `ands r7,r0` bic-then-or building sprite attr packed word bit18 (zone effect flip flag); follows OAM_SPRITE_ATTR_CLR_BIT17 naming | med |
| OAM_ATTR0_HIDDEN=0x0000ffff (4 slots) | asm/04 lines 14514/14611/15318/15496: compare extracted bits[15:0] of find_equip_chain_pair_across_field return; 0xffff = no pair found; pattern matches asm/04 line 8505 existing use of OAM_ATTR0_HIDDEN for same sentinel | high |
| PANDEMONIUM_WATCHBEAR_CID=0x1683 | asm/04 line 14079 check_slot_equip_placement_valid: Pandemonium Watchbear eligible placement check (same function as PANDEMONIUM_CID 0x169f) | high |
| gDuelFieldSlots+EFFECT_ZONE_PARTITION_OFF=0x0201d5b4 | asm/04 line 16766 `str r0,[r3,#0x0]` in update_equip_target_bitmap_for_field; EFFECT_ZONE_PARTITION_OFF confirmed in duel_field.inc comment | high |

---

## 求助

1. **card_id 0x1258** (slot_label: `check_slot_equip_placement_valid_cid_1258`): slot 未出现在 card-stats.s (0x1257=Reverse Trap, 0x125a=Turtle Oath, 0x1258 gap). 函数 check_slot_equip_placement_valid 第六步 `if (card_id==0x1258) check gP1LifePoints+0x40+slot*0xc bit2`. 不建常量, 以中性 RENAME stub 处理. 若后续发现该 slot 的卡名请补全.

2. **OAM_EFFECT_ZONE_SPRITE_P1=0x8031 置信度 med**: 从同段函数 handle_card_effect_zone_eligibility_by_field6 的 field8==9 路径推断为 P1 效果区精灵. P2 sibling 应为 0x8032 (但 0x8032 出现 42 次, 未在本段明确引用). 如确认卡名 / 精灵类型可升为 high.

---

## 自检报告

1. 所有 123 EQ value 与 ROM 字节核对: python struct.unpack_from 全部一致.
   - 4 sentinel slots (0x08046894/5c/e70/fcc) ROM=0x0000ffff -- OAM_ATTR0_HIDDEN (NOT EQUIP_CHAIN_SENTINEL=0xffff0000, corrected from draft).
   - Slot 0x08047878 ROM=0x0201e1c8 = gEquipZoneCountTable (was missing from draft, now added as upd_equip_bitmap_equip_zone_tbl_c).
2. 无 fn-ptr 表 / carve / .word <fn>+1 条目.
3. Ghidra-facing texts (RENAME EOL + PLATE replacement strings): all pure ASCII confirmed per-row check above.
4. §5.1 块: 0 (无需核对).
5. 槽名规范: 全部 ^[a-z][a-z0-9_]+$, 同函数同值用 _b/_c/_d 后缀避碰撞.
6. C5 去重: 19 card_info 新建 + 1 duel_field 新建 + 3 oam_attr 新建, 逐项 grep constants/*.inc 确认无同值碰撞.
7. card_id 0x1258 gap confirmed (无 card-stats.s 条目); 以 low-conf RENAME 处理.
8. C13: EQ=117 + REF=6 = 123 unique slots; RENAME=23 (all subset of EQ, provide EOL text). Total covered = 123 = ASM total. Diff = 0.
9. PLATE: 4 functions, 15 FUN_ tokens total (2+8+4+1). FUN_08048364 -> render_slot_card_sprite_with_chaos_equip_check added (was missing from draft).
