# Naming Proposal: 0x080abcac

## 提案
- **proposed_name**: init_equip_sub_entry_fields_from_slot
- **confidence**: high

## plate comment (中文, ASCII 标点)
由装备精灵处理簇中的四个对称函数 (0x080abbd8/0x080abd60/0x080abe54 等) 以及 FUN_08095d44 调用 (indeg=3+). 入口 r0=player_id, r1=slot_idx; 首先从 gDuelFieldSlots[player*0x868+slot*0x14] 读取装备槽数据, 提取 face/orient 编码 (bits[23:22]<<1|bit18) 写入 struct[0x0201e4d0+0x2] 高 bit 段; 提取 card_stat_field8 是否为 6 决定 struct[+0x4] 写 2 或 4; 清零 struct[+0x8]; 尾调用 init_equip_sub_entry_state_with_sprite_submit 完成精灵提交. 副作用: 修改 0x0201e4d0 子条目结构体的 byte[0], hword[2], hword[4], byte[8] 字段; 通过 init_equip_sub_entry_state_with_sprite_submit 影响精灵行缓冲区. Constants: EQUIP_STRUCT=0x0201e4d0, gDuelFieldSlots=0x0201c510, player_stride=0x868, slot_stride=0x14, FIELD8_IS_6=0x6.

## 参数签名
- r0: u8 player_id [0..1] (bit0 提取后乘以 0x868)
- r1: u8 slot_idx [0..9] (装备槽索引)
- 返回: void (尾调用 init_equip_sub_entry_state_with_sprite_submit)

## 副作用
- [0x0201e4d0+0x0] byte: player_id bit0 写入 bit0; bits[5:2] 清零 (AND ~0x1f); bit5=1 置位
- [0x0201e4d0+0x2] hword: face/orient 编码写入 bits[13:7]
- [0x0201e4d0+0x4] hword: 写 2 (field8!=6) 或 4 (field8==6)
- [0x0201e4d0+0x8] byte: 清零
- via init_equip_sub_entry_state_with_sprite_submit: 精灵行数据写入

## 行级注释 (<=30 行精华)
- @ 080abcba: 读 struct[0] byte, AND ~0x2 清 bit1, OR player_id_bit0 -> 写回 player 方向位
- @ 080abcc2: AND slot_idx & 0xf, <<1 -> face/orient 低位部分
- @ 080abce8: 加载 player_stride=0x868, 计算 player * 0x868
- @ 080abcee: 加载 gDuelFieldSlots=0x0201c510, 定位槽数据
- @ 080abcf4: 提取 bits[29:22] (face/orient), 移位组合写入 hword[+0x2]
- @ 080abd32: check_card_stat_field8_is_6(card_id) -- 判断是否双面卡效果
- @ 080abd3a: field8==6 时写 hword[+0x4]=4, 否则写 2
- @ 080abd40: 尾调用 init_equip_sub_entry_state_with_sprite_submit 完成提交

## 调用图
- caller: addr 0x08095d44 (tags: E, lp_bar pipeline, role: 直接调用无中间变量)
- caller: addr 0x080abbd8 (tags: E, equip sub entry cluster, role: 装备精灵处理四对称之一)
- caller: addr 0x080bc4a8 (tags: unknown, role: field spell handler)
- callee: check_card_stat_field8_is_6 (0x080a9f9c)
- callee: init_equip_sub_entry_state_with_sprite_submit (0x080aba8c)

## 置信度证据
- 层 1 (命名 callee 锚定): 直接调用 check_card_stat_field8_is_6 + init_equip_sub_entry_state_with_sprite_submit, 语义完整
- 层 2 (数据标签): DAT_080abd4c=0x0201e4d0 (equip sub entry struct), DAT_080abd54=0x0201c510 (gDuelFieldSlots)
- 层 3 (兄弟簇): 地址相邻 FUN_080abd60/FUN_080abe54 结构对称, 同为 equip sub entry 初始化簇成员
