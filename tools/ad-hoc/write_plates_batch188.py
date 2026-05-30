#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Write plate.txt files for batch #188 (20 functions)."""
import os

BASE = "E:/Workspace/yugioh-ex2006-re/doc/dev/eval"

plates = {
    "0807f974": (
        "check_equip_slot_eligible_with_criteria_and_target",
        u"装备槽合规性综合校验谓词. 接收 effect_node_ptr(r0), player_id(r1), slot_idx(r2). 若 slot_idx<=4 则走标准路径: 先调用 check_equip_slot_criteria_by_state_code_any 检查状态码, 再调用 check_card_id_is_equip_set_e 验证卡组类别, 再调用 get_first_placeable_monster_slot 查找可放置怪兽槽, 最后调用 check_slot_placement_blocked_by_field_effect 判断场地效果阻塞; 若 slot_idx==0xb 则改走 find_paired_zone_entry_for_card 路径. 返回 0 表示不合法, 1 表示合法. 由 0x0807fad8 和 0x0807fb14 直接调用.\n\nConstants:\n- SLOT_IDX_MAX = 4 (普通槽上界)\n- ZONE_IDX_PAIR = 0xb (配对区索引)\n- ATTR_MASK = 0xfffc7fff (清除 bits[14:15] 的 AND 掩码)"
    ),
    "08080348": (
        "check_equip_slot_eligible_with_criteria_and_prerequisites",
        u"装备槽合规性综合校验谓词, 是 check_equip_slot_eligible_with_criteria_and_target 的近似对称兄弟. 接收 effect_node_ptr(r0), player_id(r1), slot_idx(r2). 走 slot_idx<=4 路径: 调用 check_equip_slot_criteria_by_state_code_any 筛状态码, 调用 check_card_id_is_equip_set_e 验证卡组类别, 调用 get_first_placeable_monster_slot 查可放置怪兽槽, 调用 check_slot_placement_blocked_by_field_effect 判场地阻塞, 最后追加调用 check_zone_slot_equip_prerequisites 验证区域前置条件; 另有 slot_idx==0xe 的扩展路径. 返回 0/1.\n\nConstants:\n- SLOT_IDX_MAX = 4\n- ZONE_IDX_EXT = 0xe (扩展区索引)\n- ATTR_MASK = 0xfffc7fff"
    ),
    "08081900": (
        "tick_equip_activation_display_3state",
        u"装备激活显示三状态机. 接收 effect_node_ptr(r0). 从 [IWRAM_BASE+0x96*8] 读当前状态. 状态 0: 调用 count_effect_node_zone_activations 计数激活区, 再调用 dispatch_equip_card_display_op_by_card_id 派发卡显示操作, 再调用 set_equip_activation_state_by_mode 设置激活状态, 步进计数器+1, 返回 0. 状态 1: 调用 check_activation_display_state_is_confirmed 查确认标志, 若已确认则调用 enqueue_equip_slot_sprite_with_code_rotation 入队精灵并步进+1, 未确认则步进-1, 返回 0. 状态>=2: 步进计数器+1 并返回 1 表示完成.\n\nConstants:\n- IWRAM_BASE = 0x0201b290\n- STATE_OFFSET = 0x96*8 = 0x4b0"
    ),
    "08081b84": (
        "tick_equip_slot_display_by_card_id_3state",
        u"装备槽显示三状态机, 以卡 ID 查值分派. 接收 effect_node_ptr(r0). 先调用 lookup_slot_display_value_by_card_id 查 card_id 对应显示值. 从 [IWRAM_BASE+0x4b0] 读状态. 状态 0: 调用 dispatch_effect_handler_by_card_id; 若 handler 返回非零则调用 trigger_card_display_op31_if_not_active 触发显示后步进+1 返回 0(进行中); 若 handler 返回 0 且位域条件不满足则 movs r0,#1; rsbs r0,r0,#0 返回 -1(dispatch 失败). 状态 1: 调用 trigger_card_display_op31_if_not_active + init_effect_slot_display_context 后步进+1 返回 0(进行中). 状态 2: 调用 pack_equip_slot_sprite_with_code_attr 打包精灵属性后落入 LAB_08081c4a movs r0,#1 返回 1(完成). 其他状态值同样跳转 LAB_08081c4a 返回 1(完成).\n\nConstants:\n- IWRAM_BASE = 0x0201b290\n- STATE_OFFSET = 0x4b0 (0x96*8)\n- STATE2_OFFSET = 0x4b4"
    ),
    "08081dcc": (
        "enqueue_equip_slot_sprite_from_base_offset",
        u"小型装备精灵入队函数. 接收 effect_node_ptr(r0). 从固定基址 [0x0201bb90]+0 和 [0x0201bb90]+0x1c 分别读取两个参数, 再以 r0 和这两个参数调用 enqueue_equip_slot_sprite_with_code_rotation 入队精灵旋转属性. 固定返回 1 表示完成.\n\nConstants:\n- BASE_PTR = 0x0201bb90 (IWRAM 装备基址)\n- OFFSET_A = 0x0 (字段偏移 0)\n- OFFSET_B = 0x1c (字段偏移 0x1c)"
    ),
    "08081de4": (
        "check_effect_node_handler_for_slot",
        u"effect_node 双重校验谓词, 被多处 fn-ptr 表引用. 接收 effect_node_ptr(r0). 先调用 invoke_effect_node_handler_3arg 调用节点 3 参数处理器; 若返回非零, 则调用 find_effect_slot_by_side_and_type 查询匹配槽; 若找到则返回 0. 若处理器返回 0 且无匹配槽, 则返回 1. 即返回 0 表示\"有效激活条件成立\", 返回 1 表示\"条件未成立\". fn-ptr 地址 0x08081de5 被 5 个不同调用方加载到函数指针表中."
    ),
    "08081e10": (
        "tick_equip_activation_display_5state",
        u"装备激活显示五状态机. 接收 effect_node_ptr(r0). 从 [IWRAM_BASE+0x4b0] 读状态. 状态 0: count_effect_node_zone_activations; 状态 1: trigger_card_display_op31_if_not_active(op_code=0x94)+set_equip_activation_state_by_mode, 步进+1, 返回 0; 状态 2: check_activation_display_state_is_confirmed, 若确认则 enqueue_equip_slot_sprite_with_code_rotation 并步进+1; 状态 3: trigger_card_display_op31_if_not_active(op_code=0x6a)+set_equip_activation_state_by_mode, 步进+1, 返回 0; 默认(>=4): 步进+1 返回 1. 与 tick_equip_activation_display_3state (0x08081900) 为扩展 5 状态版本.\n\nConstants:\n- IWRAM_BASE = 0x0201b290\n- STATE_OFFSET = 0x4b0 (0x96*8)\n- OP_CODE_A = 0x94 (状态 1 用)\n- OP_CODE_B = 0x6a (状态 3 用)"
    ),
    "08081f28": (
        "tick_equip_activation_display_with_card_routing",
        u"装备激活显示四状态机, 带 card_id 路由. 接收 effect_node_ptr(r0). 读 [IWRAM_BASE+0x4b0] 状态. 状态 0: 调用 count_effect_node_zone_activations; 若卡 ID 匹配 0x11f0 (Greenkappa) 或 0x184a (Xing Zhen Hu) 则调用 format_game_text_with_int_arg 格式化文本再 trigger; 否则直接 trigger+set_equip_activation_state_by_mode. 状态 1: 调用 set_equip_activation_state_by_mode_alt 设置替代模式, 步进+1. 状态 2: check_activation_display_state_is_confirmed -> enqueue_equip_slot_sprite_with_code_rotation, 步进+1. 状态 3: 同状态 2.\n\nConstants:\n- IWRAM_BASE = 0x0201b290\n- STATE_OFFSET = 0x4b0\n- CARD_ID_A = 0x11f0 (Greenkappa)\n- CARD_ID_B = 0x184a (Xing Zhen Hu)\n- FORMAT_TEXT_SLOT = 0x9b (格式化文本槽编号)"
    ),
    "08082744": (
        "enqueue_equip_slot_sprite_with_attr_strip",
        u"装备槽精灵入队函数, 先剥离 attr 位域再入队. 接收 effect_node_ptr(r0). 将 [r0+4] 与 0xfffc7fff 做 AND 清除高属性位, 将 [r0+6] 与 ~0x1d=0xe2 做 AND 清除状态标志位. 从 [r0+0x14] 提取 bits[13:9] 作为 slot_idx. 调用 enqueue_equip_slot_sprite_with_code_rotation 以 node_ptr, player_id, slot_idx 入队精灵. 固定返回 1.\n\nConstants:\n- ATTR_MASK = 0xfffc7fff (清除 bits[15:14])\n- FLAG_MASK = ~0x1d = 0xe2 (清除 bits[4:0] 中的状态标志)\n- SLOT_IDX_SHIFT_LO = 0x9 (bits[13:9] 提取: lsls#0x12 / lsrs#0x17 = shift net 5)"
    ),
    "08082770": (
        "check_effect_slot_zone_field_by_type",
        u"effect_slot 区域字段三路校验谓词. 接收 effect_node_ptr(r0), player_id_or_side(r1), slot_type_qualifier(r2). 入口 push {r4,r5,r6,r7,lr} 后 adds r5,r0,#0 / adds r6,r1,#0 / adds r7,r2,#0 将三个 APCS 参数 spill 到 callee-save. 先调用 invoke_effect_node_handler_3arg 触发节点处理器. 然后读取 [r5+6] bits[4:3] 作为 case 索引 (0/1/2). case 0 (LAB_080827be): 提取 effect_slot player_id 位与 r6(r1) 比较. case 1 (LAB_080827a8): 组合 r6/r7 为 16-bit 后与 read_effect_slot_side_and_type 结果比较. case 2 (LAB_08082794): XOR effect_slot player_id 与 r6(r1) 后判非零. 返回 0 (不匹配) 或 1 (匹配).\n\nConstants:\n- ZONE_FIELD_BITS = bits[4:3] of [r5+6] (case 索引, [0..2])"
    ),
    "080829bc": (
        "tick_equip_display_by_card_id_group_a_4state",
        u"装备显示四状态机, 由卡 ID 组 A 路由显示类型码. card_id BST 分派: 0x12ed(Gravedigger Ghoul)->type 1, 0x1515(Disappear)->type 2, 0x183c(Dark Blade the Dragon Knight)->type 3, 0x14a4(Amazoness Swords Woman)->type 5, 0x1996(White Horns D.)->type 5. 查表后读 IWRAM 状态 [IWRAM_BASE+0x4b0]. 状态 0: 清 attr_bits + dispatch_card_effect_activation + format_game_text + trigger. 状态 1: check_confirmed -> enqueue_sprite 或 步进-1. 状态 2: 加载 [IWRAM+0x4b4] 为 palette_id, 调用 get_effect_slot_entry_ptr_by_palette_id + find_slot_by_palette_id_in_table + pack_equip_slot_sprite_with_code_attr. 状态>=3: 步进+1 返回 1.\n\nConstants:\n- IWRAM_BASE = 0x0201b290\n- STATE_OFFSET = 0x4b0\n- SLOT_PALETTE_OFFSET = 0x4b4\n- ATTR_MASK = 0xfffc7fff\n- FLAG_MASK_INV = ~0x1d = 0xe2\n- CARD_ID_A = 0x12ed (Gravedigger Ghoul, type 1)\n- CARD_ID_B = 0x1515 (Disappear, type 2)\n- CARD_ID_C = 0x183c (Dark Blade the Dragon Knight, type 3)\n- CARD_ID_D = 0x14a4 (Amazoness Swords Woman, type 5)\n- CARD_ID_E = 0x1996 (White Horns D., type 5)"
    ),
    "08082b88": (
        "tick_equip_display_with_fn_ptr_routing_3state",
        u"装备显示三状态机, 带函数指针路由. 接收 effect_node_ptr(r0). 先对 card_id 做三路 BST: 0x1327(Fairy's Hand Mirror), 0x140a(Shift), 0x1719(Fiend's Hand Mirror) 各映射到不同显示操作函数指针 (加载到 r7). 之后读 IWRAM 状态 [IWRAM_BASE+0x4b0]. 状态 0: 清 attr_bits + 调用 format_game_text_with_int_arg + trigger + set_equip_activation_state_by_mode, 步进+1, 返回 0. 状态 1: check_activation_display_state_is_confirmed -> enqueue_equip_slot_sprite_with_code_rotation, 步进+1. 状态 2: 写 [IWRAM+0x484] := r5 (存储激活 slot 快照), 步进+1.\n\nConstants:\n- IWRAM_BASE = 0x0201b290\n- STATE_OFFSET = 0x4b0\n- SLOT_SNAPSHOT_OFFSET = 0x484\n- ATTR_MASK = 0xfffc7fff\n- CARD_ID_A = 0x1327 (Fairy's Hand Mirror)\n- CARD_ID_B = 0x140a (Shift)\n- CARD_ID_C = 0x1719 (Fiend's Hand Mirror)"
    ),
    "08082c8c": (
        "build_equip_chain_pair_slot_entry",
        u"装备链配对校验与槽条目构建谓词. 接收 effect_node_ptr(r0). 读取 effect slot 的 side/type (read_effect_slot_side_and_type). 调用 find_equip_chain_pair_across_field 在全场查找装备链配对. 若找到则调用 check_zone_slot_equip_prerequisites 验证区域前置条件, 通过后调用 build_equip_chain_slot_entry 构建槽条目. 返回 0 表示成功, 1 表示失败. fn-ptr 地址 0x08082c8d 被 0x08082dbc 引用."
    ),
    "08082f44": (
        "tick_equip_display_by_card_id_group_b_3state",
        u"装备显示三状态机, 卡 ID 组 B 路由. card_id BST 覆盖 11 张卡: 0x1359(Backup Soldier), 0x149e(Miracle Dig), 0x14e7(Keldo), 0x1630(Hidden Book of Spell), 0x16a8(Ray of Hope), 0x16d6(Primal Seed), 0x17f1(Dark Factory of Mass Production), 0x17f7(The Graveyard in the Fourth Dimension), 0x1864(Behemoth the King of All Animals), 0x196f(Pot of Avarice), 0x1974(The Forces of Darkness). 分派 r4=op_code, r7=sub_code. 0x17f7->special(count_available_monster_slots 动态计算 sub_code). 之后读 IWRAM 状态 [IWRAM_BASE+0x4b0]. 状态 0: 清 attr + dispatch_card_effect_activation + format_game_text + trigger, 步进+1, 返回 0. 状态 1: init_effect_slot_display_context, 写 [IWRAM+0x4b4]:=0, 步进+1. 状态 2: 读 palette 计数, get_effect_slot_entry_ptr + find_slot + get_current_slot_palette_color + pack_equip_slot_sprite, 步进+1.\n\nConstants:\n- IWRAM_BASE = 0x0201b290\n- STATE_OFFSET = 0x4b0\n- SLOT_PALETTE_OFFSET = 0x4b4 (palette 计数器)\n- ATTR_MASK = 0xfffc7fff\n- SUB_CODE_DEFAULT = 0x37\n- CARD_ID_01 = 0x1359 (Backup Soldier, r4=8)\n- CARD_ID_02 = 0x149e (Miracle Dig, r4=8)\n- CARD_ID_03 = 0x14e7 (Keldo, r4=8)\n- CARD_ID_04 = 0x1630 (Hidden Book of Spell, r4=8)\n- CARD_ID_05 = 0x16a8 (Ray of Hope, r4=8)\n- CARD_ID_06 = 0x16d6 (Primal Seed, r4=8)\n- CARD_ID_07 = 0x17f1 (Dark Factory of Mass Production, r4=8)\n- CARD_ID_08 = 0x17f7 (The Graveyard in the Fourth Dimension, r7=0x011d, r4=8)\n- CARD_ID_09 = 0x1864 (Behemoth the King of All Animals, r4=0xb)\n- CARD_ID_10 = 0x196f (Pot of Avarice, r4=8, r7=0x4c)\n- CARD_ID_11 = 0x1974 (The Forces of Darkness, r4=8, r7=0x4c)\n- OP_CODE_42 = 0x2a (r4=0x2a for default unmatched)\n- MAX_PALETTE_COUNT = 0x20"
    ),
    "08083170": (
        "tick_equip_lp_display_by_node_state_4state",
        u"装备 LP 显示四状态机. 接收 effect_node_ptr(r0). 先从 [gP1LifePoints+0x1ce8] XOR [IWRAM+0x4b4] 计算 r4 值. 读 [IWRAM+0x4b4] 为状态. 状态 0: 清 attr_bits + 写 [IWRAM+0x4b4]:=0, 步进跳至 state-advance. 状态 1: count_available_monster_slots 检可用怪兽槽; 若 >0 且 check_field_spell_neo_daedalus_group_placeable 通过, 则调用 dispatch_effect_handler_by_card_id + set_lp_display_row_type14; 步进+1. 若失败则步进+2. 状态 2: find_hand_slot_idx_by_set_code 查手牌槽 + pack_equip_slot_sprite_with_code_attr 打包精灵. 状态 3: 递增 [IWRAM+0x4b4]+1, 若 >1 则返回 4 (完成), 否则返回 1.\n\nConstants:\n- IWRAM_BASE = 0x0201b290\n- STATE_OFFSET = 0x4b4 (此函数使用 0x4b4 非 0x4b0)\n- LP_OFFSET = 0x1ce8\n- ATTR_MASK = 0xfffc7fff\n- SET_CODE_OFFSET = 0x1da8 (gP1LifePoints+0x1da8)\n- PALETTE_STEP = 0x868"
    ),
    "080833bc": (
        "enqueue_equip_slot_sprites_for_pair_loop",
        u"装备槽精灵配对循环入队函数. 接收 effect_node_ptr(r0). 初始化循环索引 r6=0, 加载配对数据基址 0x09e3f140 到 r7. 循环 r6 从 0 到 2 (含): 从数组[r6*4] 取 card_pair 标识, 调用 find_deck_slot_by_card_pair_match 查找匹配槽. 若返回 -1 (未找到) 则立即返回 -1. 若找到 (返回 >=0 的 slot_idx), 则计算精灵属性偏移并调用 pack_equip_slot_sprite_with_code_attr(op_code=0xe) 打包. 三槽全部处理完毕后返回 1.\n\nConstants:\n- PAIR_TABLE_BASE = 0x09e3f140 (ROM 配对数据表基址)\n- PAIR_STEP = 0x868 (每条目步长)\n- LOOP_COUNT = 3 (r6 in [0..2])\n- OP_CODE = 0xe (精灵属性操作码)"
    ),
    "08083968": (
        "check_effect_slot_zone_player_by_type",
        u"effect_slot 区域玩家双路校验谓词, 被 fn-ptr 表引用. 接收 effect_node_ptr(r0). 读 [r4+6] bits[4:3] 作为 case 索引. case 0: XOR player_id 与 r5 比较. case 1: 直接比较 player_id 与 r5. 返回 0 (不匹配) 或 1 (匹配). r4/r5 是 caller-frame 继承的 effect_node 和比较值. fn-ptr 0x08083969 被 tick_equip_activation_display_with_card_routing (0x08081f28) 的 literal pool @ 08083aec 引用.\n\nConstants:\n- ZONE_FIELD_BITS = bits[4:3] of [r4+6] (case 索引 [0..1])"
    ),
    "080839b4": (
        "tick_equip_placement_bitmap_display_4state",
        u"装备放置 bitmap 显示四状态机. 接收 effect_node_ptr(r0). 读 [IWRAM_BASE+0x4b0] 状态. 状态 0: 调用 check_effect_activations_both_sides; 若 [activation_ctx+player_id*4+8]==1, 调用 find_best_slot_from_equip_bitmap_with_gate; 迭代有效槽 0..4 调用 invoke_effect_node_handler_3arg 查找匹配; 找到后 invoke_effect_node_handler_3arg + enqueue_equip_slot_sprite_with_code_rotation 反向遍历; 步进+1, 返回 0. 状态 1 (通过 check_effect_slot_zone_player_by_type fn-ptr): trigger_card_display_op31_if_not_active(op=0x94)+set_equip_activation_state_by_mode, 步进+1. 状态 2: check_activation_display_state_is_confirmed -> enqueue_equip_slot_sprite_with_code_rotation, 步进+1. 状态>=3: 步进+1 返回 1.\n\nConstants:\n- IWRAM_BASE = 0x0201b290\n- STATE_OFFSET = 0x4b0\n- SLOT_IDX_MAX = 4\n- FN_PTR_PREDICATE = 0x08083969 (check_effect_slot_zone_player_by_type)"
    ),
    "08083ba0": (
        "tick_equip_activation_sprite_array_4state",
        u"装备激活四状态机, 含精灵压入操作. 接收 effect_node_ptr(r0). 读 [IWRAM_BASE+0x4b0] 状态. 状态 0: 清 attr_bits + format_game_text_with_int_arg(slot=0x9b) + trigger_card_display_op31_if_not_active, 步进+1, 返回 0. 状态 1/3 共享: check_activation_display_state_is_confirmed; 若确认则从 [gP1LifePoints+0x1d68]/[+0x1d6c]/[+0x1d70] 读三字段合成参数, enqueue_sprite_attr_row_0x29_with_flag2, 然后 push_to_effect_slot_array, 步进+1. 若未确认则步进-1. 状态 2: 清 attr_bits + set_equip_activation_state_by_mode_alt, 步进+1.\n\nConstants:\n- IWRAM_BASE = 0x0201b290\n- STATE_OFFSET = 0x4b0\n- ATTR_MASK = 0xfffc7fff\n- FLAG_MASK_INV = ~0x1d = 0xe2\n- FORMAT_TEXT_SLOT = 0x9b\n- LP_FIELD_A = gP1LifePoints+0x1d68\n- LP_FIELD_B = gP1LifePoints+0x1d6c (offset diff = 4)\n- LP_FIELD_C = gP1LifePoints+0x1d70 (offset diff = 8)\n- FN_PTR_CHECK = 0x08083b55 (check_equip_slot_pair_blocked)"
    ),
    "08083e14": (
        "tick_equip_lamp_dream_activation_3state",
        u"装备激活三状态机, 专用于 Ancient Lamp / Dreamsprite 卡组. 接收 effect_node_ptr(r0). 读 [IWRAM_BASE+0x4b0] 状态. 状态 0: 清 attr_bits + count_effect_node_zone_activations; 若激活数 >0, 对 card_id 做三路比较 (0x1476=Ancient Lamp, 0x140a(=0x1476-0x6c)=Shift, 0x148a=Dreamsprite): Ancient Lamp/Shift 路径调用 trigger_card_display_op31_if_not_active(op=0xf) 并写 [gP1LP+0xea<<5]:=1; Dreamsprite 路径读 [0x0201e2a0+player_id*4] 判断 [ptr+8]==1 后写 [gP1LP+0xea<<5]:=1 或 invoke_card_display_op_0x31_sub1(op=0xe2). 步进+1, 返回 0. 状态 1: 检查 [gP1LP+0x1d40] 是否非零; 若为 0 则返回 -1; 否则 set_equip_activation_state_by_mode, 步进+1, 返回 0. 状态 2: check_activation_display_state_is_confirmed -> enqueue_equip_slot_sprite_with_code_rotation + 步进+1. 默认: 返回 1.\n\nConstants:\n- IWRAM_BASE = 0x0201b290\n- STATE_OFFSET = 0x4b0\n- ATTR_MASK = 0xfffc7fff\n- FLAG_MASK_INV = ~0x1d = 0xe2\n- CARD_ID_A = 0x1476 (Ancient Lamp)\n- CARD_ID_B = 0x148a (Dreamsprite)\n- CARD_ID_C = 0x140a (Shift; 0x1476-0x6c)\n- OP_CODE_TRIGGER = 0xf\n- OP_CODE_ALT = 0xe2\n- ACTIVATION_FLAG_FIELD = gP1LifePoints + 0x1d40 (0xea<<5=0x1d40)\n- DREAM_DATA_BASE = 0x0201e2a0\n- FN_PTR_MODE = 0x080905e9 (invoke_effect_node_handler_3arg+1, fn-ptr)"
    ),
}

ok_count = 0
for addr, (name, plate_text) in plates.items():
    plate_path = os.path.join(BASE, addr + ".plate.txt")
    with open(plate_path, "w", encoding="utf-8") as f:
        f.write(plate_text)
    # Verify no problematic non-ASCII
    bad = [c for c in plate_text if ord(c) > 0x7f and not (0x4e00 <= ord(c) <= 0x9fff) and not (0x3400 <= ord(c) <= 0x4dbf) and not (0x3000 <= ord(c) <= 0x303f) and not (0x2e80 <= ord(c) <= 0x2eff) and not (0x20000 <= ord(c) <= 0x2a6df)]
    if bad:
        print("BAD {}: {}".format(addr, [(c, hex(ord(c))) for c in bad[:5]]))
    else:
        print("OK {} -> {}".format(addr, name))
        ok_count += 1

print("\nTotal: {}/{}".format(ok_count, len(plates)))
