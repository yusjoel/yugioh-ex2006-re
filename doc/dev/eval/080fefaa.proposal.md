# Naming Proposal: 080fefaa

## 提案
- **proposed_name**: tick_card_display_render_panel
- **confidence**: med

## plate comment (中文, ASCII 标点)
由 FUN_080fe308 (超集 banlist/card_data/card_desc/card_frame/card_ids/card_image/card_info/card_list/card_stats/deck/font_jp/frame_counter/fs/game_str/settings 场景主循环) 调用, 是 card_stats/font_jp/frame_counter 显示面板的帧级分派函数. 函数体非常短 (仅 2 条指令后跳转至 LAB_080fefae 执行主体), 作为 card_frame/card_stats 渲染子循环的入口. 其下游调用包括 tick_card_stats_render_panel (card_stats), advance_card_list_frame_counter (frame_counter), write_card_list_slot_oam_entries (OAM), tick_card_list_slot_highlight_oam 等全套显示子系统.

## 参数签名
- 参数: 无 (void)
  - asm 080fefaa: movs r5,#0 / movs r1,#0 为入口首两条指令, r0 未被读取即被覆盖, 确认无输入参数
- 返回: r0 = int (调用方不检查)

## 副作用
- 通过下游子函数间接写入 VRAM/OAM/IWRAM (见各子函数)

## 行级注释 (≤ 30 行精华)
- @ 080fefaa: r5=0, r1=0 => 初始化循环变量
- @ 080fefae: LAB_080fefae => 帧循环主体 (函数体主逻辑)

## 调用图
- caller: addr 0x080fe308 (tags: banlist/card_data/card_desc/card_frame/card_ids/card_image/card_info/card_list/card_stats/deck/font_jp/frame_counter/fs/game_str/settings, role: 顶层场景主循环)
- callee: tick_card_stats_render_panel (0x08107bdc), advance_card_list_frame_counter (0x080ff9e0), write_card_list_slot_oam_entries (0x08101574), tick_card_list_slot_highlight_oam (0x08101764)

## 置信度证据
- L5 caller 模式: caller 是全场景主循环, 本函数是 display/blend/window/bg/card_frame/card_stats/font_jp/frame_counter 子系统入口
- L6 callee 链: 4 个已命名 callee 覆盖 card_stats/frame_counter/OAM 三路渲染
- 置信度 med: 函数体仅 2 条可见指令 (LAB_080fefae 主体读取行号区间外), 完整逻辑未全量读取
