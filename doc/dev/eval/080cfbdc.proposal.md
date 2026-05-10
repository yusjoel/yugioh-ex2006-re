# Naming Proposal: 0x080cfbdc

## 提案
- **proposed_name**: render_card_list_oam_row_by_stat_state
- **confidence**: high

## plate comment (中文, ASCII 标点)
卡牌列表 OAM 行渲染的统计状态 (stat_state) 分支, 由 FUN_080c82e4 (card display master tick) 直接调用 (indeg=1). 函数读取 gFontState[0x0a03] 行计数换算 OAM Y; 读 gFontState[0x0a04] halfword 作为 x_base; 读 gFontState[0x0a0e] halfword bits[23:16] (lsls/lsrs 提取) 作为 slot_nibble; 读 gFontState[0x0a18] word bits[23:16] 作为 state_val, 四路分派: state=0 -> 写 4 个 OAM strip (r4:0..3, write_oam_entry_from_packed_args, attr0=0x32, slot=0x60); 检查 gPrng[0x148] bit4/bit5/bit6/bit7 (0x10/0x20/0xc0/0x01) 选择子路径: 0x10 -> find_next_occupied_slot_forward + 写 gFontState[0x0a0e] nibble + strh + sync; 0x20 -> find_next_occupied_slot_backward + 写 nibble + strh + sync; 0xc0 -> mod 20 折行 + find_next_occupied_slot_backward + 写 nibble + strh + sync; 0x01 -> 写 gP1LifePoints + 写 gFontState[0x0a18] bits + sync. state=1 -> nibble B/C 更新循环 (gFontState[0x0a1b/0x0a1c]). state=2/3 -> 其他分支. 使用 callee-save r7 存储 state 等级 (3 或 4).

Constants:
- FONT_STATE_BASE = 0x0201f440
- ROW_OFFSET = 0x0a03
- X_BASE_OFFSET = 0x0a04
- SLOT_NIBBLE_OFFSET = 0x0a0e (bits[23:16] nibble, mask 0xfffff00f)
- STATE_OFFSET = 0x0a18 (bits[23:16] state_val, mask 0xfffe01ff)
- gPrng_BIT_NEXT_FWD = 0x10 (bit4)
- gPrng_BIT_NEXT_BWD = 0x20 (bit5)
- gPrng_BIT_WRAP_BWD = 0xc0 (bits 6..7)
- gPrng_BIT_LP_WRITE = 0x01 (bit0)
- gPrng_FIELD_OFFSET = 0xa4 * 2 = 0x148
- OAM_STRIP_COUNT = 4 (r4: 0..3)
- ATTR0_STRIP = 0x32 (Y位)
- OAM_SLOT = 0x60
- WRAP_MODULO = 0x14 = 20

## 参数签名
- r0: void (入口: push; .hword 0x4647 = mov r7,r0 但实际是 callee-save store; 随后 ldr r2,DAT 内部加载)
- 注: .hword 0x4647 @ 080cfbde 解码: bit7=0,bit6=0,bits[5:3]=000,bits[2:0]=111 -> mov r7,r0. 但 r0 在 push 之后未被 APCS 传入任何值 -> r7 仅为 callee-save 保存
- 返回: r0 = void

## 副作用
- OAM 写入: write_oam_entry_from_packed_args x4 (state=0, strip 循环)
- [gFontState+0x0a0e] := 更新 nibble bits[11:4] (mask 0xfffff00f)
- [gFontState+0x0a18] := 更新 state bits (mask 0xfffe01ff)
- [gP1LifePoints + 0x148] := 写 LP 相关值 (state=0 bit0 路径)
- 调用 sync_state_and_init_sprite (r0=0) -> 触发精灵初始化同步

## 行级注释 (精华)
- @ 080cfbdc: push + .hword 0x4647 (mov r7,r0) + push {r7} = callee-save r7
- @ 080cfbe2: ldr r2, DAT_080cfc20 -> gFontState 0x0201f440
- @ 080cfbe8: ldrb r0,[r2+0x0a03] -> 行计数
- @ 080cfbf0: lsls r0,r0,#3 -> OAM Y = (10-row/2)*8
- @ 080cfbf6: ldrh r1,[r2+0x0a04] -> x_base halfword
- @ 080cfbfe: ldrh r0,[r2+0x0a0e] -> slot_nibble halfword
- @ 080cfc02: lsrs r5,r1,#0x18 -> 提取 nibble bits[23:16]
- @ 080cfc08: ldr r0,[r2+0x0a18] -> state word
- @ 080cfc0a: lsls r0,r0,#0xf; lsrs r0,r0,#0x18 -> 提取 state bits[23:16]
- @ 080cfc10: cmp r0,#1; bne LAB_080cfc14 -> state==1 -> 跳至 nibble 路径
- @ 080cfc12: b LAB_080cfdca -> state==1 主路径 (nibble B/C 更新)
- @ 080cfc4a: (state=0) lsls r0,r7,#0x10 -> OAM Y pack
- @ 080cfc5c: bl write_oam_entry_from_packed_args (4x strip loop)
- @ 080cfc68: ldr r0, PTR_gPrng_080cfcb0 -> gPrng base
- @ 080cfc70: ldrh r1,[r0+0x148] -> 读帧 flags
- @ 080cfc74: ands r0,#0x10; beq -> bit4 检查
- @ 080cfc7c: bl find_next_occupied_slot_forward -> 前向槽搜索
- @ 080cfcaa: bl sync_state_and_init_sprite (r0=0)
- @ 080cfccc: ands r0,#0x20; beq -> bit5 检查
- @ 080cfcd2: bl find_next_occupied_slot_backward -> 后向槽搜索

## 调用图
- caller: addr 0x080c82e4 (tags: card_data/card_desc/card_frame/card_ids/card_image/card_info/card_list/card_name/card_stats/demo/duel_field/font_jp/frame_counter/fs/game_str/pack/prng/settings, role: card display master tick)
- callee: find_next_occupied_slot_forward (0x080cf6d8)
- callee: find_next_occupied_slot_backward (0x080cf754)
- callee: sync_state_and_init_sprite
- callee: write_oam_entry_from_packed_args

## 置信度证据
- 层 1 tag: vram/palette/font_jp/game_str 与卡牌列表 stat 渲染场景一致
- 层 2 callee 集合: find_next_occupied_slot_forward/backward + write_oam_entry_from_packed_args + sync_state_and_init_sprite 明确指示 stat 状态机渲染
- 层 3 IO 状态字: gFontState+0x0a03/0x0a04/0x0a0e/0x0a18 + gPrng+0x148 bit flags 均与兄弟簇一致
- 层 4 sibling: 与 render_card_list_oam_row_by_stat_display (0x080cf52c, batch #31) 的 state_machine 架构完全对称
- 层 5 caller: 0x080c82e4 单一调用者, 与同为 indeg=1 的兄弟簇一致
