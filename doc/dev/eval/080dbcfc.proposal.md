# Naming Proposal: 0x080dbcfc

## 提案
- **proposed_name**: render_pack_card_name_to_sprite
- **confidence**: high

## plate comment (中文, ASCII 标点)
在包店卡牌槽展示时, 将卡名字符串渲染到 OBJ VRAM 精灵行缓冲区并输出宽度(以 tile 为单位). 触发条件: caller font_jp_080d4de4 已选定 VRAM 目标槽位后调用本函数, 传入 r0=VRAM 目标地址, r1=卡名字符串指针, r2=render_mode. 函数先调用 select_charset_then_load_name 取得字符串(字符集由 IWRAM language flag [0x02000000+0x6c2c] 内部读取), 再调用 setup_line_buf_pos_and_font 设置字体上下文, 然后依据 r4(=r2 入参) 分支: mode==0 渲染 OBJ_COLOR_0, mode==2 渲染小字, mode==3 渲染大字, mode>3 使用 0x100|r6 属性; 最终调用 text_render_wrapper 写入行缓冲区, commit_line_buffer_to_sprite_vram 刷新到 VRAM. 返回 r7 = (pixel_width+8)>>3 即卡名宽度(tile 数, [1..N]).

Constants:
- IWRAM_LANG_FLAG = [0x02000000+0x6c2c] (charset/language 标志)
- FONT_CTX = 0x02006ed0 (字体上下文基址)
- OBJ_ATTR_BASE = 0x00008108 (OBJ 属性常量)
- TILE_WIDTH_SHIFT = 3 (pixel->tile: (w+8)>>3)

## 参数签名
- r0: void* vram_dest (OBJ VRAM 目标地址, 精灵行缓冲区基址)
- r1: u8* card_name_ptr (卡名字符串指针)
- r2: u8 render_mode [0..4+] (渲染模式: 0=颜色0, 2=小字, 3=大字, >3=0xf属性; 保存到 r4 via adds r4,r2,#0 at 080dbd08; charset 由内部 IWRAM language flag [0x02000000+0x6c2c] 读取, 不经 APCS)
- 返回: r0 = u8 tile_width (卡名渲染宽度, 以 8px tile 为单位, [1..N])

## 副作用
- [vram_dest..vram_dest+N]: 写 OBJ 精灵行缓冲区像素数据 (via commit_line_buffer_to_sprite_vram)
- [0x02006ed0+0x4]: 写 font_ptr (字体指针, 由字体上下文设置)
- [0x02006ed0+0x8]: 写 charset mode bits
- [0x02006ed0+0x14]: 写 width_flag byte
- [0x02006ed0+0x15]: 写 color_mode byte

## 行级注释 (≤ 30 行精华)
- @ 080dbd18: select_charset_then_load_name -- 依据 language flag 选字符集并加载卡名到内部缓冲区
- @ 080dbd22: setup_line_buf_pos_and_font -- 设置渲染位置 x=0x30, font_idx=2
- @ 080dbd64: cmp r4,#0 -- 分支: render_mode==0 时仅写颜色0属性不渲染文字
- @ 080dbd70: text_render_wrapper -- 渲染卡名主色层到行缓冲区
- @ 080dbd9e: orrs r6,r0 -- 将 0x100(OBJ 大小属性) OR 进行模式编码
- @ 080dbdae: text_render_wrapper -- 渲染卡名边框/阴影层
- @ 080dbdb6: commit_line_buffer_to_sprite_vram -- 将行缓冲刷新到 OBJ VRAM 精灵行
- @ 080dbd5c: measure_string_pixel_width -- 测量像素宽度以计算 tile 数
- @ 080dbd62: asrs r7,r0,#3 -- tile 宽度 = (pixel_width+8) / 8
- @ 080dbdde: 对 mode>3 的情况: 逐列 AND 行数据, 用掩码叠加透明度
- @ 080dbe00: 返回 tile_width r7

## 调用图
- caller: addr 0x080d4de4 (tags: [vram; font_jp]; role: 包店卡牌展示初始化, 选中槽位后渲染卡名)
- callee: select_charset_then_load_name, setup_line_buf_pos_and_font, measure_string_pixel_width, text_render_wrapper, commit_line_buffer_to_sprite_vram

## 置信度证据
- L1: 函数体完整静态可读 (0x080dbcfc..0x080dbe0c, ~130 条指令)
- L2: 调用 select_charset_then_load_name + text_render_wrapper + commit_line_buffer_to_sprite_vram 三联确认为文字渲染族
- L3: caller font_jp_080d4de4 (tags: [vram; font_jp]) 在包店槽位展示语境调用, IWRAM font ctx 0x02006ed0 + OBJ_ATTR_BASE 0x8108 确认为包店 OBJ sprite 渲染; prologue .hword 0x464f=mov r7,r9 + .hword 0x4646=mov r6,r8 + .hword 0x4680=mov r8,r0 全部为 callee-save 高寄存器保存, 不涉及额外 APCS 参数
