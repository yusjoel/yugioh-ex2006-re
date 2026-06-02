# Naming Proposal: 0x080dffdc

## 提案
- **proposed_name**: tick_pack_card_select_overlay_scroll_step
- **confidence**: high

## plate comment (中文, ASCII 标点)
拆包卡牌选择场景的 overlay 滚动步骤函数. 由 dispatch_pack_card_select_substep (0x080e0fb8) 经函数指针表 0x09e495f4 间接分派. 读取 gPrng+0x148 bit0; 若为 1 则设置 pack_ui_state+0x1c0 bit3. 递减帧计数器 +0x30+0xe; 归零时批量清零 +0x4..+0xc 并写步骤 ID := 2. 调用 tick_pack_slot_cover_oam/render_pack_slot_cover_oam_sprite/tick_pack_oam_slots_and_overlay. 右/左 overlay 分支分别调用 render_overlay_sprite_pack_cover_right/left 并写 +0x110/+0x112 := 5. 副作用: +0x1c0 bit3, +0x30+0xe 帧计数, +0x30+0x4..+0xc 清零, +0x4/+0x110/+0x112. 返回 r0=r6 (0=继续/1=完成).

Constants:
- pack_ui_state = 0x03005850
- gPrng+0x148 = 0xa4<<1 = 输入状态字
- OVERLAY_FLAG_BIT = 0x8 (bit3 of pack_ui_state+0x1c0)
- FRAME_COUNTER_OFFSET = 0x30+0xe = slot struct 内帧计数字段

## 参数签名
- r0: void (入口 ldr r5, DAT 立即覆盖, 无 APCS 输入)
- 返回: r0 = u8 step_done [0=继续, 1=步骤完成], 经 adds r0,r6 返回

## 副作用
- [pack_ui_state+0x1c0]: strb 设置 bit3 (若 gPrng+0x148 bit0=1)
- [pack_ui_state+0x30+0xe]: strh 帧计数器递减
- [pack_ui_state+0x30+0x4..+0xc]: 归零时 strh 批量清零
- [pack_ui_state+0x4]: strh := 2 (若帧计数完成)
- [pack_ui_state+0x110]: strh := 5 (右 overlay 方向)
- [pack_ui_state+0x112]: strh := 5 (左 overlay 方向)

## 行级注释 (精华)
- @ 080dffe8: gPrng+0x148 bit0 检测 (overlay enable flag)
- @ 080dfffc: pack_ui_state+0x1c0 bit3 设置 (orrs 0x8)
- @ 080e0008: 帧计数器 -1
- @ 080e0012..080e001a: 帧归零时批量清零 +0x4..+0xc
- @ 080e001c: pack_ui_state+0x4 := 2 (新步骤)
- @ 080e0024..080e0030: tick_slot_cover/render_sprite/tick_oam
- @ 080e0042: render_overlay_sprite_pack_cover_right (向右时)
- @ 080e005e: render_overlay_sprite_pack_cover_left (向左时)

## 调用图
- caller: CALLEE-COLUMN GREP (ghidra-funcs-callgraph.csv): 0 hits; Sub-type B: 经 ROM step-table 0x09e495f4 由 dispatch_pack_card_select_substep (0x080e0fb8) 间接分派; form(c) Sub-type B
- callee: tick_pack_slot_cover_oam, render_pack_slot_cover_oam_sprite, tick_pack_oam_slots_and_overlay, render_overlay_sprite_pack_cover_right, render_overlay_sprite_pack_cover_left

## 置信度证据
- L1 (asm 行范围 382817-382893, 函数体完整)
- L2 (IO/IWRAM: pack_ui_state 多字段写入; gPrng+0x148 bit0 输入检测)
- L6 (sibling: tick_pack_slot_cover_fadein 0x080dfc74 / tick_pack_card_list_step 0x080e0604 确立命名体系)
