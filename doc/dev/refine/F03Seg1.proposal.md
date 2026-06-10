# Refine Proposal: F03Seg1  [0x08035f54..0x08036a78)

## 段测绘

### 函数入口 x13
| 地址 | 函数名 |
|------|--------|
| 0x08035f54 | link_equip_node_by_card_type_check |
| 0x08036014 | check_slot_equip_eligibility_by_type |
| 0x080363bc | check_slot_field_zone_card_eligible |
| 0x08036450 | check_slot_equip_whitelist_with_monster_space |
| 0x080364b0 | check_slot_card_effect_eligibility |
| 0x08036658 | query_slot_effect_eligibility_nonzero |
| 0x08036674 | check_slot_card_fieldspell_eligibility |
| 0x080366f0 | check_slot_fieldspell_eligible_by_side |
| 0x0803670c | query_slot_card_type_eligibility |
| 0x08036770 | check_zone_slot_equip_prerequisites |
| 0x08036870 | check_card_equip_eligible_for_slot |
| 0x080369a4 | check_equip_eligibility_via_request_buf |
| 0x08036a10 | check_slot_card_special_activation_eligible |

### 残留自动名槽 x84

PTR_ 槽 (2 个):
- 0x08035f8c `PTR_gP1LifePoints_08035f8c` = gP1LifePoints  x2
- 0x080365c0 `PTR_gP1LifePoints_080365c0` = gP1LifePoints  x2

DAT_ 槽 (82 个): 0x08035f90 ~ 0x08036a6c (详见符号化计划)

### ROM_INCBIN / .byte 块
本段无 ROM_INCBIN / .byte 块。

---

## 数据块分类 (Rule 2/3)

本段 0 个 ROM_INCBIN/.byte 块，无需 ref-scan 分类。

---

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate; 新建/复用)

注: 2 个 RENAME_SLOT (gap card IDs 0x1632/0x13ea + 0xffff0000) 列在 RENAME_SLOTS 节，不进 EQ_SLOTS。
实际 EQ 物理槽 = 81 个 (84 - 3 RENAME)。

#### 复用现有常量

| 物理槽 | 值 | 现有常量名 | 来源 inc |
|--------|-----|-----------|----------|
| DAT_08035f90 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_08035fcc | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_08036010 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_08036094 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_08036288 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_080362f8 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_080363a8 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_08036414 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_080364a0 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_08036500 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_080365c4 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_080366d8 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_08036840 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_080368d4 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_08036a64 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| PTR_gP1LifePoints_08035f8c | 0x0201c4e0 | gP1LifePoints | ewram.inc |
| PTR_gP1LifePoints_080365c0 | 0x0201c4e0 | gP1LifePoints | ewram.inc |
| DAT_08035fd0 | 0x0201c510 | gDuelFieldSlots | ewram.inc |
| DAT_08036098 | 0x0201c510 | gDuelFieldSlots | ewram.inc |
| DAT_080362fc | 0x0201c510 | gDuelFieldSlots | ewram.inc |
| DAT_08036418 | 0x0201c510 | gDuelFieldSlots | ewram.inc |
| DAT_08036504 | 0x0201c510 | gDuelFieldSlots | ewram.inc |
| DAT_080366dc | 0x0201c510 | gDuelFieldSlots | ewram.inc |
| DAT_08036844 | 0x0201c510 | gDuelFieldSlots | ewram.inc |
| DAT_080368d8 | 0x0201c510 | gDuelFieldSlots | ewram.inc |
| DAT_080364a4 | 0x0201c510 | gDuelFieldSlots | ewram.inc |
| DAT_08036a68 | 0x0201c510 | gDuelFieldSlots | ewram.inc |
| DAT_0803628c | 0x0201d9c0 | gEquipNodePool | ewram.inc |
| DAT_080363ac | 0x0201d9c0 | gEquipNodePool | ewram.inc |
| DAT_080360a0 | 0x0201d9c0 | gEquipNodePool | ewram.inc |
| DAT_08036290 | 0xffffeb50 | NODE_POOL_NEG_OFFSET | duel_field.inc |
| DAT_080363b0 | 0xffffeb50 | NODE_POOL_NEG_OFFSET | duel_field.inc |
| DAT_080363b4 | 0x0201c520 | gDuelFieldSlotState | ewram.inc |
| DAT_080365bc | 0x000010f4 | UMI_CARD_ID | card_info.inc |
| DAT_08036540 | 0x000013cd | LEGENDARY_FISHERMAN_CID | card_info.inc |
| DAT_08036558 | 0x0000164e | GUARDIAN_KAYEST_CID | card_info.inc |

#### 新建常量 EQ 槽

| 物理槽 | 值 | 新常量名 | 目标 inc |
|--------|-----|---------|---------|
| DAT_08035fd4 | 0x000018a6 | EHERO_AVIAN_CID | card_info.inc |
| DAT_0803600c | 0x000019c1 | CHAIN_THRASHER_CID | card_info.inc |
| DAT_08036120 | 0x0000148e | ROYAL_COMMAND_CID | card_info.inc |
| DAT_08036124 | 0x000014da | FIEND_SKULL_DRAGON_CID | card_info.inc |
| DAT_08036128 | 0x000014b8 | POSSESSED_DARK_SOUL_CID | card_info.inc |
| DAT_0803612c | 0x00001322 | SNATCH_STEAL_CID | card_info.inc |
| DAT_08036140 | 0x000012e2 | MAGIC_ARM_SHIELD_CID | card_info.inc |
| DAT_08036148 | 0x000012fc | CHANGE_OF_HEART_CID | card_info.inc |
| DAT_08036174 | 0x00001430 | MYSTIC_BOX_CID | card_info.inc |
| DAT_0803617c | 0x00001466 | DARK_NECROFEAR_CID | card_info.inc |
| DAT_080361a0 | 0x00001877 | BRAIN_JACKER_CID | card_info.inc |
| DAT_080361a4 | 0x00001581 | ENEMY_CONTROLLER_CID | card_info.inc |
| DAT_080361bc | 0x0000169a | FALLING_DOWN_CID | card_info.inc |
| DAT_080361c8 | 0x00001857 | OWNER_SEAL_CID | card_info.inc |
| DAT_080361f4 | 0x000018c6 | RESHEF_THE_DARK_BEING_CID | card_info.inc |
| DAT_0803620c | 0x0000195d | CHTHONIAN_POLYMER_CID | card_info.inc |
| DAT_08036294 | 0xffffeb60 | NODE_POOL_TO_SLOT_STATE_OFF | duel_field.inc |
| DAT_08036300 | 0x00001466 | DARK_NECROFEAR_CID | card_info.inc (reuse above) |
| DAT_08036304 | 0x00001322 | SNATCH_STEAL_CID | card_info.inc (reuse above) |
| DAT_08036318 | 0x0000169a | FALLING_DOWN_CID | card_info.inc (reuse above) |
| DAT_0803631c | 0x00001877 | BRAIN_JACKER_CID | card_info.inc (reuse above) |
| DAT_080363b8 | 0x000018c2 | CHARMER_RANGE_MAX_CID | card_info.inc |
| DAT_0803641c | 0x00001826 | ELEMENT_MAGICIAN_CID | card_info.inc |
| DAT_0803653c | 0x00001709 | CANNONBALL_SPEAR_SHELLFISH_CID | card_info.inc |
| DAT_08036544 | 0x000012a8 | DEEPSEA_WARRIOR_CID | card_info.inc |
| DAT_08036574 | 0x000017d3 | HORUS_LV6_CID | card_info.inc |
| DAT_08036588 | 0x00001814 | SILENT_SWORDSMAN_LV5_CID | card_info.inc |
| DAT_0803664c | 0x00001693 | METALLIZING_PARASITE_CID | card_info.inc |
| DAT_08036650 | 0x00001667 | NON_SPELLCASTING_AREA_CID | card_info.inc |
| DAT_08036654 | 0x000017a1 | DUST_BARRIER_CID | card_info.inc |
| DAT_08036508 | 0x0201b290 | gDuelPhaseFlags | ewram.inc |
| DAT_080366e0 | 0x0201b290 | gDuelPhaseFlags | ewram.inc (reuse) |
| DAT_08036848 | 0x0201b290 | gDuelPhaseFlags | ewram.inc (reuse) |
| DAT_080366e4 | 0x0000194e | EHERO_WILDHEART_CID | card_info.inc |
| DAT_0803684c | 0x000004bc | PHASE_LOCK_FLAG_OFF | duel_field.inc |
| DAT_08036850 | 0x00001388 | EQUIP_SLOT_CARD_ID_RANGE_MAX | duel_field.inc |
| DAT_08036854 | 0x0000128b | LORD_OF_D_CID | card_info.inc |
| DAT_08036858 | 0x00001879 | KING_DRAGUN_CID | card_info.inc |
| DAT_0803685c | 0x000017dc | HORUS_SERVANT_CID | card_info.inc |
| DAT_08036860 | 0x000017d4 | HORUS_LV8_CID | card_info.inc |
| DAT_080368dc | 0x0000150c | EQUIP_TYPE_A_CID | card_info.inc |
| DAT_080368e0 | 0x00001645 | EXODIA_NECROSS_CID | card_info.inc |
| DAT_08036974 | 0x0000150a | HEART_OF_CLEAR_WATER_CID | card_info.inc |
| DAT_080369a0 | 0x0000153c | TIMIDITY_CID | card_info.inc |
| DAT_08036a6c | 0x000016f8 | DARK_MAGICIAN_OF_CHAOS_CID | card_info.inc |

---

### EQ_SLOTS 汇总表 (Ghidra 操作用, C13 全覆盖 81 EQ + 3 RENAME = 84)

以下每行: (slot_addr, value, const_name, slot_label)

```
EQ  0x08035f8c  gP1LifePoints                  PTR_gP1LifePoints_08035f8c  ->  link_equip_node_card_type_lp_ptr
EQ  0x08035f90  PLAYER_BLOCK_STRIDE            DAT_08035f90                ->  link_equip_node_card_type_stride
EQ  0x08035fcc  PLAYER_BLOCK_STRIDE            DAT_08035fcc                ->  link_equip_node_card_type_stride_b
EQ  0x08035fd0  gDuelFieldSlots                DAT_08035fd0                ->  link_equip_node_card_type_slots
EQ  0x08035fd4  EHERO_AVIAN_CID                DAT_08035fd4                ->  link_equip_node_card_type_cid_a
EQ  0x0803600c  CHAIN_THRASHER_CID             DAT_0803600c                ->  link_equip_node_card_type_cid_b
EQ  0x08036010  PLAYER_BLOCK_STRIDE            DAT_08036010                ->  link_equip_node_card_type_stride_c
EQ  0x08036094  PLAYER_BLOCK_STRIDE            DAT_08036094                ->  check_slot_equip_elig_stride
EQ  0x08036098  gDuelFieldSlots                DAT_08036098                ->  check_slot_equip_elig_slots
EQ  0x080360a0  gEquipNodePool                 DAT_080360a0                ->  check_slot_equip_elig_pool
EQ  0x08036120  ROYAL_COMMAND_CID              DAT_08036120                ->  check_slot_equip_elig_cid_a
EQ  0x08036124  FIEND_SKULL_DRAGON_CID         DAT_08036124                ->  check_slot_equip_elig_cid_b
EQ  0x08036128  POSSESSED_DARK_SOUL_CID        DAT_08036128                ->  check_slot_equip_elig_cid_c
EQ  0x0803612c  SNATCH_STEAL_CID               DAT_0803612c                ->  check_slot_equip_elig_cid_d
EQ  0x08036140  MAGIC_ARM_SHIELD_CID           DAT_08036140                ->  check_slot_equip_elig_cid_e
EQ  0x08036148  CHANGE_OF_HEART_CID            DAT_08036148                ->  check_slot_equip_elig_cid_f
EQ  0x08036174  MYSTIC_BOX_CID                 DAT_08036174                ->  check_slot_equip_elig_cid_g
EQ  0x0803617c  DARK_NECROFEAR_CID             DAT_0803617c                ->  check_slot_equip_elig_cid_h
EQ  0x080361a0  BRAIN_JACKER_CID               DAT_080361a0                ->  check_slot_equip_elig_cid_i
EQ  0x080361a4  ENEMY_CONTROLLER_CID           DAT_080361a4                ->  check_slot_equip_elig_cid_j
EQ  0x080361bc  FALLING_DOWN_CID               DAT_080361bc                ->  check_slot_equip_elig_cid_k
EQ  0x080361c8  OWNER_SEAL_CID                 DAT_080361c8                ->  check_slot_equip_elig_cid_l
EQ  0x080361f4  RESHEF_THE_DARK_BEING_CID      DAT_080361f4                ->  check_slot_equip_elig_cid_m
EQ  0x0803620c  CHTHONIAN_POLYMER_CID          DAT_0803620c                ->  check_slot_equip_elig_cid_n
EQ  0x08036288  PLAYER_BLOCK_STRIDE            DAT_08036288                ->  check_slot_equip_elig_0a_stride
EQ  0x0803628c  gEquipNodePool                 DAT_0803628c                ->  check_slot_equip_elig_0a_pool
EQ  0x08036290  NODE_POOL_NEG_OFFSET           DAT_08036290                ->  check_slot_equip_elig_0a_neg_off
EQ  0x08036294  NODE_POOL_TO_SLOT_STATE_OFF    DAT_08036294                ->  check_slot_equip_elig_0a_slotstate_off
EQ  0x080362f8  PLAYER_BLOCK_STRIDE            DAT_080362f8                ->  check_slot_equip_elig_0a_stride_b
EQ  0x080362fc  gDuelFieldSlots                DAT_080362fc                ->  check_slot_equip_elig_0a_slots
EQ  0x08036300  DARK_NECROFEAR_CID             DAT_08036300                ->  check_slot_equip_elig_0a_cid_a
EQ  0x08036304  SNATCH_STEAL_CID               DAT_08036304                ->  check_slot_equip_elig_0a_cid_b
EQ  0x08036318  FALLING_DOWN_CID               DAT_08036318                ->  check_slot_equip_elig_0a_cid_c
EQ  0x0803631c  BRAIN_JACKER_CID               DAT_0803631c                ->  check_slot_equip_elig_0a_cid_d
EQ  0x080363a8  PLAYER_BLOCK_STRIDE            DAT_080363a8                ->  check_slot_field_zone_stride
EQ  0x080363ac  gEquipNodePool                 DAT_080363ac                ->  check_slot_field_zone_pool
EQ  0x080363b0  NODE_POOL_NEG_OFFSET           DAT_080363b0                ->  check_slot_field_zone_neg_off
EQ  0x080363b4  gDuelFieldSlotState            DAT_080363b4                ->  check_slot_field_zone_slot_state
EQ  0x080363b8  CHARMER_RANGE_MAX_CID          DAT_080363b8                ->  check_slot_field_zone_charmer_range_max
EQ  0x08036414  PLAYER_BLOCK_STRIDE            DAT_08036414                ->  check_slot_field_zone_stride_b
EQ  0x08036418  gDuelFieldSlots                DAT_08036418                ->  check_slot_field_zone_slots
EQ  0x0803641c  ELEMENT_MAGICIAN_CID           DAT_0803641c                ->  check_slot_field_zone_cid_a
EQ  0x080364a0  PLAYER_BLOCK_STRIDE            DAT_080364a0                ->  check_equip_whitelist_stride
EQ  0x080364a4  gDuelFieldSlots                DAT_080364a4                ->  check_equip_whitelist_slots
EQ  0x08036500  PLAYER_BLOCK_STRIDE            DAT_08036500                ->  check_effect_elig_stride
EQ  0x08036504  gDuelFieldSlots                DAT_08036504                ->  check_effect_elig_slots
EQ  0x08036508  gDuelPhaseFlags                DAT_08036508                ->  check_effect_elig_phase_flags
EQ  0x0803653c  CANNONBALL_SPEAR_SHELLFISH_CID DAT_0803653c                ->  check_effect_elig_cid_a
EQ  0x08036540  LEGENDARY_FISHERMAN_CID        DAT_08036540                ->  check_effect_elig_cid_b
EQ  0x08036544  DEEPSEA_WARRIOR_CID            DAT_08036544                ->  check_effect_elig_cid_c
EQ  0x08036558  GUARDIAN_KAYEST_CID            DAT_08036558                ->  check_effect_elig_cid_d
EQ  0x08036574  HORUS_LV6_CID                  DAT_08036574                ->  check_effect_elig_cid_e
EQ  0x08036588  SILENT_SWORDSMAN_LV5_CID       DAT_08036588                ->  check_effect_elig_cid_f
EQ  0x080365bc  UMI_CARD_ID                    DAT_080365bc                ->  check_effect_elig_umi_cid
EQ  0x080365c0  gP1LifePoints                  PTR_gP1LifePoints_080365c0  ->  check_effect_elig_lp_ptr
EQ  0x080365c4  PLAYER_BLOCK_STRIDE            DAT_080365c4                ->  check_effect_elig_stride_b
EQ  0x0803664c  METALLIZING_PARASITE_CID       DAT_0803664c                ->  check_effect_elig_equip_ref_cid
EQ  0x08036650  NON_SPELLCASTING_AREA_CID      DAT_08036650                ->  check_effect_elig_copies_cid
EQ  0x08036654  DUST_BARRIER_CID               DAT_08036654                ->  check_effect_elig_zones_cid
EQ  0x080366d8  PLAYER_BLOCK_STRIDE            DAT_080366d8                ->  check_fieldspell_elig_stride
EQ  0x080366dc  gDuelFieldSlots                DAT_080366dc                ->  check_fieldspell_elig_slots
EQ  0x080366e0  gDuelPhaseFlags                DAT_080366e0                ->  check_fieldspell_elig_phase_flags
EQ  0x080366e4  EHERO_WILDHEART_CID            DAT_080366e4                ->  check_fieldspell_elig_cid_a
EQ  0x08036840  PLAYER_BLOCK_STRIDE            DAT_08036840                ->  check_zone_prereq_stride
EQ  0x08036844  gDuelFieldSlots                DAT_08036844                ->  check_zone_prereq_slots
EQ  0x08036848  gDuelPhaseFlags                DAT_08036848                ->  check_zone_prereq_phase_flags
EQ  0x0803684c  PHASE_LOCK_FLAG_OFF            DAT_0803684c                ->  check_zone_prereq_phase_lock_off
EQ  0x08036850  EQUIP_SLOT_CARD_ID_RANGE_MAX   DAT_08036850                ->  check_zone_prereq_cid_range_max
EQ  0x08036854  LORD_OF_D_CID                  DAT_08036854                ->  check_zone_prereq_lord_of_d_cid
EQ  0x08036858  KING_DRAGUN_CID                DAT_08036858                ->  check_zone_prereq_king_dragun_cid
EQ  0x0803685c  HORUS_SERVANT_CID              DAT_0803685c                ->  check_zone_prereq_horus_servant_cid
EQ  0x08036860  HORUS_LV8_CID                  DAT_08036860                ->  check_zone_prereq_horus_lv8_cid
EQ  0x080368d4  PLAYER_BLOCK_STRIDE            DAT_080368d4                ->  check_equip_eligible_stride
EQ  0x080368d8  gDuelFieldSlots                DAT_080368d8                ->  check_equip_eligible_slots
EQ  0x080368dc  EQUIP_TYPE_A_CID               DAT_080368dc                ->  check_equip_eligible_type_a_cid
EQ  0x080368e0  EXODIA_NECROSS_CID             DAT_080368e0                ->  check_equip_eligible_type_b_cid
EQ  0x08036974  HEART_OF_CLEAR_WATER_CID       DAT_08036974                ->  check_equip_eligible_chain_param
EQ  0x080369a0  TIMIDITY_CID                   DAT_080369a0                ->  check_equip_eligible_chain_alt_cid
EQ  0x08036a64  PLAYER_BLOCK_STRIDE            DAT_08036a64                ->  check_special_act_stride
EQ  0x08036a68  gDuelFieldSlots                DAT_08036a68                ->  check_special_act_slots
EQ  0x08036a6c  DARK_MAGICIAN_OF_CHAOS_CID     DAT_08036a6c                ->  check_special_act_dmc_cid
```

---

### RENAME_SLOTS (纯改名 + EOL)

3 个 RENAME 槽 (gap card IDs + 高频通用值):

```
RENAME  0x0803609c  DAT_0803609c  ->  check_slot_equip_elig_zone_cid_1632
  EOL: "card_id=0x1632 (gap slot; passed as r0 to count_zones_by_card_and_mode; not in card-stats.s; range [0x1631..0x1633] has Miracle Restoring/Disarmament); low-conf"

RENAME  0x08036160  DAT_08036160  ->  check_slot_equip_elig_cid_13ea
  EOL: "card_id=0x13ea (gap slot; not in card-stats.s; range [0x13E8..0x13EB] has Nuvia the Wicked/Soul Exchange); equip BST branch; low-conf"

RENAME  0x08036914  DAT_08036914  ->  check_equip_eligible_chain_sentinel
  EOL: "0xffff0000: find_equip_chain_pair_across_field return<<16 == 0xffff0000 -> no valid pair found; 7587 raw refs (ROM-wide common pattern, not EQ)"
```

---

### FUNC_RENAME (误名订正)

经检查所有 13 个函数名语义与函数体操作一致，无明显误名。

---

### PLATE (R5; 含 stale FUN_ 字符串扫描)

13 个函数各需一条 setPlateComment。所有 plate 文本为纯 ASCII (无 CJK)。按现有函数名写入，无 stale `FUN_` 字面量。

---

## carve 计划 (R7)

本段无函数间 ROM_INCBIN 块，无需 carve。

---

## disasm 计划 (R4)

本段无误标数据块，无需 disasm。

---

## 新增 constants / 全局

### card_info.inc 新增 (共 35 条)

ROM bytes 验证: python `struct.unpack('<I', d[addr-0x8000000:addr-0x8000000+4])[0]` 对照每行值全部通过。

```
.equ EHERO_AVIAN_CID,               0x000018a6  @ Elemental Hero Avian (pw=21844576); link_equip_node_by_card_type_check card_type_A; 12 raw refs; data.md Starter/Opp=0x18A6
.equ CHAIN_THRASHER_CID,            0x000019c1  @ Chain Thrasher (pw=88190453); link_equip_node_by_card_type_check card_type_B; 9 raw refs; data.md=0x19C1
.equ ROYAL_COMMAND_CID,             0x0000148e  @ Royal Command (pw=33950246); check_slot_equip_eligibility_by_type BST; 10 raw refs; data.md=0x148E
.equ FIEND_SKULL_DRAGON_CID,        0x000014da  @ Fiend Skull Dragon (pw=66235877); BST; 12 raw refs; data.md=0x14DA
.equ POSSESSED_DARK_SOUL_CID,       0x000014b8  @ Possessed Dark Soul (pw=52860176); BST; 8 raw refs; data.md=0x14B8
.equ SNATCH_STEAL_CID,              0x00001322  @ Snatch Steal (pw=45986603); BST; 20 raw refs; data.md=0x1322
.equ MAGIC_ARM_SHIELD_CID,          0x000012e2  @ Magic-Arm Shield (pw=96008713); BST; 9 raw refs; data.md=0x12E2
.equ CHANGE_OF_HEART_CID,           0x000012fc  @ Change of Heart (pw=04031928); BST; 8 raw refs; data.md=0x12FC
.equ MYSTIC_BOX_CID,                0x00001430  @ Mystic Box (pw=25774450); BST; 100 raw refs; data.md=0x1430; ROM@0x08036174 verified
.equ DARK_NECROFEAR_CID,            0x00001466  @ Dark Necrofear (pw=31829185); BST (3 slots: 0x8036174+8, 0x80363b0c, 0x8036300); 19 raw refs; data.md=0x1466
.equ BRAIN_JACKER_CID,              0x00001877  @ Brain Jacker (pw=40267580); BST; 10 raw refs; data.md=0x1877
.equ ENEMY_CONTROLLER_CID,          0x00001581  @ Enemy Controller (pw=98045062); BST; 10 raw refs; data.md=0x1581
.equ FALLING_DOWN_CID,              0x0000169a  @ Falling Down (pw=32919136); BST (2 slots); 15 raw refs; data.md=0x169A
.equ OWNER_SEAL_CID,                0x00001857  @ Owner's Seal (pw=09720537); BST; 5 raw refs; data.md=0x1857
.equ RESHEF_THE_DARK_BEING_CID,     0x000018c6  @ Reshef the Dark Being (pw=62420419); BST; 7 raw refs; data.md=0x18C6; ROM@0x080361f4 verified
.equ CHTHONIAN_POLYMER_CID,         0x0000195d  @ Chthonian Polymer (pw=72287557); BST; 7 raw refs; card-stats.s card_1963 slot=0x195D
.equ CHARMER_RANGE_MAX_CID,         0x000018c2  @ Wynn the Wind Charmer (pw=37744402); range_max of charmer block [0x18BF..0x18C2] (Aussa/Eria/Hiita/Wynn); 7 raw refs; ROM@0x080363b8 verified; card-stats.s card_1842
.equ ELEMENT_MAGICIAN_CID,          0x00001826  @ Element Magician (pw=65260293); check_slot_field_zone_card_eligible; 12 raw refs; data.md=0x1826
.equ CANNONBALL_SPEAR_SHELLFISH_CID,0x00001709  @ Cannonball Spear Shellfish (pw=95614612); check_slot_card_effect_eligibility whitelist; 7 raw refs; data.md=0x1709
.equ DEEPSEA_WARRIOR_CID,           0x000012a8  @ Deepsea Warrior (pw=24128274); check_slot_card_effect_eligibility whitelist; 9 raw refs; card-stats.s card_0632 slot=0x12A8; ROM@0x08036544 verified
.equ LEGENDARY_FISHERMAN_CID already exists (reuse)
.equ GUARDIAN_KAYEST_CID already exists (reuse)
.equ HORUS_LV6_CID,                 0x000017d3  @ Horus the Black Flame Dragon LV6 (pw=11224103); check_slot_card_effect_eligibility; 9 raw refs; data.md=0x17D3
.equ HORUS_LV8_CID,                 0x000017d4  @ Horus the Black Flame Dragon LV8 (pw=48229808); check_zone_slot_equip_prerequisites range; 12 raw refs; data.md=0x17D4
.equ HORUS_SERVANT_CID,             0x000017dc  @ Horus' Servant (pw=09264485); check_zone_slot_equip_prerequisites; 6 raw refs; data.md=0x17DC
.equ SILENT_SWORDSMAN_LV5_CID,      0x00001814  @ Silent Swordsman LV5 (pw=74388798); check_slot_card_effect_eligibility whitelist; 22 raw refs; data.md=0x1814; 0x181A computed as +6
.equ METALLIZING_PARASITE_CID,      0x00001693  @ Metallizing Parasite - Lunatite (pw=07369217); count_slot_equip_list_matches ref; 9 raw refs; data.md=0x1693
.equ NON_SPELLCASTING_AREA_CID,     0x00001667  @ Non-Spellcasting Area (pw=20065549); count_field_copies_of_card param; 4 raw refs; data.md=0x1667
.equ DUST_BARRIER_CID,              0x000017a1  @ Dust Barrier (pw=31476755); count_available_effect_zones param; 8 raw refs; data.md=0x17A1
.equ EHERO_WILDHEART_CID,           0x0000194e  @ Elemental Hero Wildheart (pw=86188410); check_slot_card_fieldspell_eligibility; 9 raw refs; data.md=0x194E
.equ LORD_OF_D_CID,                 0x0000128b  @ Lord of D. (pw=17985575); check_zone_slot_equip_prerequisites; 6 raw refs; data.md=0x128B
.equ KING_DRAGUN_CID,               0x00001879  @ King Dragun (pw=13756293); check_zone_slot_equip_prerequisites; 11 raw refs; data.md=0x1879
.equ HEART_OF_CLEAR_WATER_CID,      0x0000150a  @ Heart of Clear Water (pw=64801562); query_zone_chain_count_with_eligibility param; 22 raw refs; data.md=0x150A
.equ TIMIDITY_CID,                  0x0000153c  @ Timidity (pw=40350910); check_slot_card_eligible_for_special_action; 8 raw refs; data.md=0x153C
.equ EXODIA_NECROSS_CID,            0x00001645  @ Exodia Necross (pw=12600382); check_card_equip_eligible_for_slot TYPE_B; 21 raw refs; data.md=0x1645
.equ EQUIP_TYPE_A_CID,              0x0000150c  @ Fusion Sword Murasame Blade (pw=37684215); check_card_equip_eligible_for_slot TYPE_A; 14 raw refs; data.md=0x150C
.equ DARK_MAGICIAN_OF_CHAOS_CID,    0x000016f8  @ Dark Magician of Chaos (pw=40737112); check_slot_card_special_activation_eligible; 17 raw refs; data.md=0x16F8
```

Actual new card_info.inc entries: 35 (excluding 2 reused: LEGENDARY_FISHERMAN_CID + GUARDIAN_KAYEST_CID).

### ewram.inc 新增 (1 条)

```
.equ gDuelPhaseFlags,       0x0201b290  @ duel phase flags struct base; +0x4bc=phase lock byte, +0x594=effect entry count; 676 raw refs
```

### duel_field.inc 新增 (3 条)

```
.equ PHASE_LOCK_FLAG_OFF,           0x000004bc  @ gDuelPhaseFlags+0x4bc = phase lock global inhibit byte; 11 raw refs; check_zone_slot_equip_prerequisites DAT_0803684c verified
.equ EQUIP_SLOT_CARD_ID_RANGE_MAX,  0x00001388  @ upper bound for Horus-adjacent equip block card_id range [0x1386..0x1388]; not in card-stats.s; 28 raw refs
.equ NODE_POOL_TO_SLOT_STATE_OFF,   0xffffeb60  @ gEquipNodePool+0xffffeb60 = gDuelFieldSlotState (= gDuelFieldSlots+0x10); distinct from NODE_POOL_NEG_OFFSET=0xffffeb50; 2 raw refs (both Seg-1)
```

---

## §5.1 登記 (Rule 3) -- 0 引用块

本段无 ROM_INCBIN 块，无 §5.1 登记。

---

## 消费者证据 (R6) -- 关键槽语义置信度

| 槽/全局 | 语义 | file:line | 置信度 |
|---------|------|-----------|--------|
| 0x08035fd4=0x18a6 (EHERO_AVIAN_CID) | link_equip_node BST card_type_A check | asm/03_equip_chain_hand.s:74 + data.md Starter/Opp col 0x18A6 | high |
| 0x0803600c=0x19c1 (CHAIN_THRASHER_CID) | link_equip_node BST card_type_B check | asm/03_equip_chain_hand.s:105 + data.md 0x19C1 | high |
| 0x080368dc=0x150c (EQUIP_TYPE_A_CID) | check_card_equip_eligible TYPE_A dispatch | asm/03_equip_chain_hand.s:1322 + data.md 0x150C | high |
| 0x080368e0=0x1645 (EXODIA_NECROSS_CID) | check_card_equip_eligible TYPE_B dispatch | asm/03_equip_chain_hand.s:1325 + data.md 0x1645 | high |
| 0x08036508=0x0201b290 (gDuelPhaseFlags) | phase flags struct base; +0x4bc path | asm/03_equip_chain_hand.s:799 (DAT_08036508) | high |
| 0x0803684c=0x4bc (PHASE_LOCK_FLAG_OFF) | gDuelPhaseFlags+0x4bc = phase lock byte | asm/03_equip_chain_hand.s:1245 (DAT_0803684c) | high |
| 0x080365bc=0x10f4 (UMI_CARD_ID) | passed to check_card_matches_active_effect_slot | asm/03_equip_chain_hand.s:894 (DAT_080365bc) | high (reuse) |
| 0x08036a6c=0x16f8 (DARK_MAGICIAN_OF_CHAOS_CID) | special case in check_slot_card_special_activation | asm/03_equip_chain_hand.s:1533 + data.md 0x16F8 | high |
| 0x080363b4=0x0201c520 (gDuelFieldSlotState) | slot state parallel array (gDuelFieldSlots+0x10) | asm/03_equip_chain_hand.s:616 (DAT_080363b4) | high (reuse) |
| 0x08036290=0xffffeb50 (NODE_POOL_NEG_OFFSET) | gEquipNodePool-0x14b0 = gDuelFieldSlots | asm/03_equip_chain_hand.s:463 | high (reuse) |
| 0x08036294=0xffffeb60 (NODE_POOL_TO_SLOT_STATE_OFF) | gEquipNodePool-0x14a0 = gDuelFieldSlotState; gEquipNodePool(0x0201d9c0)+0xffffeb60=0x0201c520 verified | asm/03_equip_chain_hand.s:465 | high |
| 0x08036914=0xffff0000 (RENAME sentinel) | find_equip_chain_pair_across_field return<<16; cmp 0xffff0000 tests if low halfword==0xffff | asm/03_equip_chain_hand.s:1344-1346 | med (RENAME not EQ; 7587 raw refs) |
| 0x0803609c=0x1632 (RENAME cid_1632) | r0 arg to count_zones_by_card_and_mode (plate: r0=card_id [0..0x19b7]); gap slot not in card-stats.s | asm/03_equip_chain_hand.s:139 + asm/02_text_lp_fieldspell.s:14528 | med (RENAME; card name unknown) |
| 0x08036160=0x13ea (RENAME cid_13ea) | BST node in check_slot_equip_eligibility_by_type; gap slot not in card-stats.s | asm/03_equip_chain_hand.s:187 + card-stats.s gap [0x13E8..0x13EB] | med (RENAME; card name unknown) |
| 0x080363b8=0x18c2 (CHARMER_RANGE_MAX_CID) | range upper bound [0x18BF..0x18C2]: Aussa/Eria/Hiita/Wynn; cmp r1,r0; bgt -> subs r0,#3 | asm/03_equip_chain_hand.s:576-580 + card-stats.s card_1839/1840/1841/1842 | high |
| 0x08036174=0x1430 (MYSTIC_BOX_CID) | BST node; Mystic Box pw=25774450 | asm/03_equip_chain_hand.s:188 + data.md 0x1430; ROM@0x08036174 verified | high |

---

## 自检 (Phase 4)

1. **EQ value vs ROM bytes**: python ref-scan 对全部 81 个 EQ 槽验证 struct.unpack('<I',...) == expected_value。发现 3 处初稿错误 (0x08036160/0x08036174/0x080363b8) 均已修正。
2. **carve 指针表**: 本段无 carve，跳过。
3. **plate/EOL 纯 ASCII**: 3 条 RENAME EOL 文本均无 CJK 字符 (grep 确认)。
4. **§5.1 复核**: 无 incbin 块，跳过。
5. **槽名格式检查**: 所有 slot_label 符合 `^[a-z][a-z0-9_]+$`；RENAME slot `check_slot_equip_elig_cid_13ea` / `check_slot_equip_elig_zone_cid_1632` 含十六进制后缀合规。
6. **ELEMENT_SOLDIER_CID / ELEMENT_VALKYRIE_CID / SILENT_MAGICIAN_LV8_CID**: 三者均为计算得出 (0x1826-0x42 / 0xc3<<5 / 0x1814+6)，无独立 DAT_ 槽，不建新常量。

---

## Executor Report: F03Seg1

- 槽: EQ=81 REF=0 RENAME=3 FUNC_RENAME=0 PLATE=13
- carve=0 disasm=0 §5.1=0
- 新增 constants/全局:
  - card_info.inc: EHERO_AVIAN_CID / CHAIN_THRASHER_CID / ROYAL_COMMAND_CID / FIEND_SKULL_DRAGON_CID / POSSESSED_DARK_SOUL_CID / SNATCH_STEAL_CID / MAGIC_ARM_SHIELD_CID / CHANGE_OF_HEART_CID / MYSTIC_BOX_CID / DARK_NECROFEAR_CID / BRAIN_JACKER_CID / ENEMY_CONTROLLER_CID / FALLING_DOWN_CID / OWNER_SEAL_CID / RESHEF_THE_DARK_BEING_CID / CHTHONIAN_POLYMER_CID / CHARMER_RANGE_MAX_CID / ELEMENT_MAGICIAN_CID / CANNONBALL_SPEAR_SHELLFISH_CID / DEEPSEA_WARRIOR_CID / HORUS_LV6_CID / HORUS_LV8_CID / HORUS_SERVANT_CID / SILENT_SWORDSMAN_LV5_CID / METALLIZING_PARASITE_CID / NON_SPELLCASTING_AREA_CID / DUST_BARRIER_CID / EHERO_WILDHEART_CID / LORD_OF_D_CID / KING_DRAGUN_CID / HEART_OF_CLEAR_WATER_CID / TIMIDITY_CID / EXODIA_NECROSS_CID / EQUIP_TYPE_A_CID / DARK_MAGICIAN_OF_CHAOS_CID (35 entries)
  - ewram.inc: gDuelPhaseFlags (1 entry)
  - duel_field.inc: PHASE_LOCK_FLAG_OFF / EQUIP_SLOT_CARD_ID_RANGE_MAX / NODE_POOL_TO_SLOT_STATE_OFF (3 entries)
- 求助: none (4 items resolved: 0x1632=gap CID->RENAME; 0x13ea=gap CID->RENAME; 0xffff0000=RENAME not EQ; 0xffffeb60=new NODE_POOL_TO_SLOT_STATE_OFF constant)
- proposal: doc/dev/refine/F03Seg1.proposal.md
