# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# NOTE (2026-04-30): 中文注释必须显式 decode("utf-8") 成 unicode 后再传给 Ghidra Java API,
# 否则 Java String 把 utf-8 字节当 Latin-1 收, 存进 .rep 是 mojibake.
# 旧条目 plate comment 已经 mojibake; 单独靠 FixCommentEncoding.py 修.
# RenameKnownFunctions.py  (Jython 2.7 / Ghidra script)
#
# TG.4  把已知 FUN_xxx 批量 rename.
#   来源:
#     - doc/analysis/card-image-location.md  (卡图加载函数逆向叙事)
#     - doc/dev/data-structure/card-attributes.md / card-image-big.md / card-image-mini.md
#     - doc/dev/p2-font-location-findings.md (字体/文本渲染链)
#
# 同时往 plate comment 里写一条简短说明, 让 Listing/Decompiler 直接看见.
#
# @category Ygo-ex2006

from ghidra.program.model.symbol import SourceType
from ghidra.program.model.listing import CodeUnit

RUN_DRY = False
try:
    _args = list(getScriptArgs())
    if _args and _args[0].lower() in ("dry", "--dry", "1", "true"):
        RUN_DRY = True
except Exception:
    pass


RENAMES = [
    # (orig, new, one-line comment)
    ("FUN_0801d290", "decode_card_image_6bpp",
        "p1: 6bpp -> BG0 VRAM, 每6 ROM bytes -> 8 像素"),
    ("FUN_0801d45c", "card_info_page_init_bg0",
        "p1: 写 BG0CNT=0x0086, 清 BG0 VRAM"),
    ("FUN_0801d998", "card_image_decode_wrapper",
        "p1: 读卡片属性, 调 decode_card_image_6bpp (r1=0x10 palette offset)"),
    ("FUN_0801e440", "card_info_page_entry",
        "p1/p2: 卡牌信息页顶层, card_id=(word0<<15)>>18"),
    ("FUN_0801d448", "card_info_page_enter_with_card_id",
        "p1: FUN_0801e640 的首个 bl"),
    ("FUN_0801dbdc", "card_info_page_step_03_unknown",
        "p1/p2: 页面动画/过渡 (非 tile 写入), 待细化"),
    ("FUN_080eeb54", "card_data_query",
        "按 card_id 查卡片属性表 (0x098169B6 基址), 返回 ATK/DEF/type 等"),
    ("FUN_0801e000", "render_card_description_text",
        "p2: 字段/描述绘制入口, 字面量池含 .word 0x06010040"),
    ("FUN_0801e100", "card_info_page_finalize",
        "p2: 顶层最后一个 bl, UI 收尾"),
    ("FUN_080f2a7c", "text_render_wrapper",
        "p2: render_string_to_line_buffer 的薄包装"),
    ("FUN_080f2aa8", "render_string_to_line_buffer",
        "p2: 逐字符遍历, 处理 \\n/\\r/\\t/空格"),
    ("FUN_080f1b60", "load_glyph_row_pair",
        "p2: 从 0x09CCCA90+ch*8 读 8 bytes, 循环 4 轮每轮 2 字节 blit"),
    ("FUN_080f0f70", "blit_glyph_row_to_buffer",
        "p2: 每行 8 bit blit 到 line buffer"),
    ("FUN_080f02a4", "get_char_width_class",
        "p2: jump table @ 0x080f02d4, 返回字符宽度类别"),
    ("FUN_080f0200", "char_width_narrow_5",
        "p2: 窄字宽度 5px"),
    ("FUN_080f0210", "char_width_wide_10_or_12",
        "p2: 宽字宽度 10 或 12px"),
    ("FUN_080c33bc", "load_card_list_small_image",
        "P1 findings: 卡列表小图 (OBJ 8bpp, 1152 B/条)"),
    ("FUN_080f2e4c", "commit_line_buffer_to_sprite_vram",
        "p2: line buffer -> 0x06010040+ sprite tile"),
    # --- TG.4-next 轮（2026-04-15） ---
    ("FUN_0801e640", "card_list_on_select_to_info_page",
        "TG.4-next: 卡列表按 A 进详情页的派发, 首 bl 即 card_info_page_enter_with_card_id"),
    # --- pack banner 轮（2026-04-16） ---
    ("FUN_080d971c", "pack_list_page_init",
        "pack-banner: 卡包列表页初始化, 函数指针表 0x09E4948C[11]"),
    ("FUN_080d8d84", "pack_list_bg_setup",
        "pack-banner: BG0CNT=0x1C00, BG2CNT=0x1E0D, 清空 VRAM screenblocks"),
    ("FUN_080d8f08", "pack_list_tilemap_load",
        "pack-banner: 从 0x09CCE2B0/C0/D0 加载 BG tilemap + BG palette"),
    ("FUN_080d8e98", "pack_entry_init",
        "pack-banner: 逐 pack 初始化 (banner tile + name text + detail)"),
    ("FUN_080d8f48", "pack_banner_obj_setup",
        "pack-banner: 按 slot 计算 OBJ VRAM 地址, 调 pack_banner_tile_copy"),
    ("FUN_080db860", "pack_banner_tile_copy",
        "pack-banner: ROM 指针表 0x09CCE960[id] → OBJ VRAM, mode 1=2D stride"),
    ("FUN_080dbbc0", "pack_name_text_render",
        "pack-banner: ROM 0x09E5E2E8 查包名, text_render_wrapper x2"),
    # 2026-04-30: 重命名 pack_ui_state_machine -> banner_anim_state_machine.
    # 复审发现该函数实际读 0x0201fec0 (gBannerState), 与 pack_ui_state (0x03005850)
    # 完全无关; 内容是 banner 出/入场 7-state 动画 (BLDY/WINOUT 调制 + tile copy).
    # 2026-04-30 (后续): 修正 plate, FUN_0801ef94 实为 play_ui_effect (UI 特效派发器),
    # 不是 PageManager.
    ("banner_anim_state_machine", "banner_anim_state_machine",
        "banner 出/入场动画状态机 (7-state on [gBannerState+0x10]); 阶段: 0=init "
        "(载 palette/tiles, 启 BG3), 1-2=fade-in (BLDY 渐增 7+64f), 3-5=fade-out "
        "(BLDY 渐减 + 文本切换 8+64+8f), 6=teardown (关 BG3); sub-counter 在 "
        "[gBannerState+0x11]; 返回 1=busy / 0=done. 唯一 caller: play_ui_effect "
        "(FUN_0801ef94) case 1 (effect_id=1)."),
    ("FUN_080d8ddc", "pack_visible_count",
        "pack-banner: 返回当前可见 pack 数 (clamp 1..5)"),
    ("FUN_080d8f84", "pack_detail_bg_tile_load",
        "pack-banner: EWRAM 记录 → BG VRAM 0x06000240, 含 pack cost"),
    ("FUN_080f74d4", "tile_2d_row_copy",
        "pack-banner/通用: 按行拷贝 tile 到 2D OBJ VRAM (dest stride 0x400)"),
    # --- Data Crystal wiki 揭示的函数（2026-04-17） ---
    ("FUN_080143f0", "banlist_password_enter_char",
        "datacrystal: 禁卡密码字符录入 [gBanlistPasswordBuffer]"),
    ("FUN_0802387c", "draw_decimal_with_offset",
        "datacrystal: 通用十进制绘制（被多处调用，含 0x080242c8 入口）"),
    ("FUN_080ee76c", "internal_card_id_to_card_id",
        "datacrystal: cards_ids_array 查表，icid 4007..7078 → card_id；越界返 0"),
    ("FUN_080ee7ac", "select_charset_then_load_name",
        "datacrystal: 按 game-region/language 选字符集，分支到对应 name 加载（含 JP 特例 0x1497..0x149A）；0x080ee968 是其内部 LAB"),
    ("FUN_080eebfc", "card_name_lookup_by_internal_id",
        "datacrystal: 包装：icid → cid → 读 gSettings 取 lang_id → 调 select_charset_then_load_name"),
    # --- 卡列表小图调色板 + tile 数据定位（2026-04-18）---
    ("FUN_080fdef4", "card_list_screen_init",
        "card-mini-frame: 屏幕初始化序列；4 次 memcpy 加载静态 OBJ 调色板 (0x09E31554/74/14)；调 card_list_tile_renderer"),
    ("FUN_081011c4", "card_list_tile_renderer",
        "card-mini-frame: 卡列表小图 tile 渲染; 字面量池含 0x09326280(tile 基址) + 0x095B5C00(index 表)"),
    # --- 第五轮 (2026-04-24) FS loader + name_input + GL 基础设施 ---
    ("FUN_08014fa8", "fs_load",
        "FS loader: u8* fs_load(const char* path, int flag); 读 fs_master_struct @ 0x09E61178"),
    ("FUN_08014600", "cpu_copy_auto",
        "包装 SWI 0xB/0xC (CpuSet/CpuFastSet)，按 count 自动选；r2 转为 u32 词数"),
    # 纠正前一轮误命名：FUN_08014600 曾被命名为 fs_lz_decompress，实际是 memcpy 包装
    ("fs_lz_decompress", "cpu_copy_auto",
        "（纠正误命名）包装 SWI 0xB/0xC (CpuSet/CpuFastSet)"),
    ("FUN_0810e41c", "bios_lz77_uncomp",
        "BIOS SWI 0x11 = LZ77UnCompReadNormalWrite8bit"),
    ("FUN_0810e418", "bios_huff_uncomp",
        "BIOS SWI 0x12 = HuffUnComp"),
    ("FUN_0810e3f4", "bios_cpu_fast_set",
        "BIOS SWI 0xC = CpuFastSet (32 B chunks)"),
    ("FUN_0810e3f8", "bios_cpu_set",
        "BIOS SWI 0xB = CpuSet (word/halfword)"),
    ("FUN_0810e3fc", "bios_div",
        "BIOS SWI 0x6 = Div"),
    ("FUN_08014f54", "fs_resolve_path_to_fid",
        "FS 路径解析: 拆目录/文件名二级查表 -> FID 索引"),
    ("FUN_08017574", "name_input_page_init",
        "name_input 页 IO 初始化 (DISPCNT=0x1F40, BG0-3CNT=0x1C02/0x1D8C/0x1E8D/0x1F8F); state[0]"),
    ("FUN_080180ac", "name_input_page_load_assets",
        "name_input 页资产装载: fs_load 加载 name_o_01.* + name_b_01/02/04; state[1]"),
    ("FUN_08019494", "name_input_page_tick",
        "name_input 页主循环 (光标/输入/回显); state[2]"),
    ("FUN_080194ec", "name_input_page_exit",
        "name_input 页退出/清理; state[3]"),
    ("FUN_08019574", "page_state_dispatcher",
        "通用页面状态分派器 (跨页复用); 从 [0x03000040] 读 state, 索引状态表"),
    ("FUN_08014638", "gl_clear_vram_palram_scroll",
        "GL 基础设施: 清 VRAM (0x6000 u32) + PALRAM (0x100 u32) + 8 个 BG scroll 寄存器"),
    ("FUN_080146fc", "gl_set_brightness",
        "GL: 设置亮度 (mode=r0=0x3F, bright=r1=[-16,16]); 源 GL/GL_Common.c"),
    ("FUN_080148d0", "gl_fade_in",
        "GL: 启动 8 帧淡入 (bright -16 -> 0)"),
    ("FUN_080148e0", "gl_fade_out",
        "GL: 启动 8 帧淡出 (bright -> -16)"),
    ("FUN_08015138", "gl_state_init",
        "GL: 初始化 state struct @ EWRAM 0x02023490 (0x22B B)"),
    ("FUN_080156ac", "gl_clear_frame_callbacks",
        "GL: 清 IWRAM 回调指针槽 [0x03000BF8/BFC/C00] = 0"),
    # --- 第六轮 (2026-04-25) 日文字库 + 双字节字符渲染 ---
    ("FUN_080f0188", "char_code_to_glyph_index",
        "code > 0xEFFF: 公式 (hi&0xF)<<7|(lo&0x7F); 否则二分查找 font_jp_sjis_lookup_table[1925]"),
    ("FUN_080f1884", "render_glyph_jp_dual_layer",
        "渲染日文双字节字符: char_to_idx → font_jp_charset_table 选 (base, stride) → 8bpp 预解码 strb 到 OBJ tile; narrow+wide 双层叠加 (描边)"),
    ("FUN_080f19a4", "render_glyph_jp_single_layer",
        "渲染日文单字节字符 (高字节=0): 仅 narrow 层 (font_jp_main_*); 与 dual_layer 共享 char_to_idx 路径"),
    ("FUN_080f0274", "measure_string_pixel_width",
        "字符串总像素宽计算: 按 byte bit 7 二选一 char_width_narrow_5/wide_10_or_12 累加; 用于布局/居中决策"),

    # --- game_str logical_id 映射 (2026-04-30) ---
    ("FUN_080f4e18", "game_str_id_to_row",
        "game_str logical_id -> master_row 二分查找. arg=u16 logical_id (e.g. 0x1004); "
        "查 game_str_id_remap_table @ 0x08000250 (1651 * u16 sorted, count @ 0x08000240); "
        "返回 master_row [0..1650], 找不到返回 0. caller 用结果索引 game_str_pointer_table "
        "@ 0x08000F40 取 (lang offset, base) 拿到字符串地址."),

    # --- pack UI dialog (2026-04-30) ---
    ("FUN_080d6290", "pack_ui_show_all_opened_done",
        "Pack shop 'Open all' 完成时的终态处理. 通过 game_str_id_to_row(0x13f7) 取 row 1086 = "
        "'Opened all packs.', 调 text_overlay_create 弹模态对话框 (h=10, w=30), 然后切 "
        "pack_ui_state[+0x10]=8 把 pack 状态机推到完成态. 返回 1."),
    ("FUN_080dd53c", "text_overlay_create",
        "通用模态文本对话框/提示创建. 入参: r0 = (height<<16) | width, r1 = flags, r2 = char *text. "
        "把 size split 写进内部 struct 的 [+0xa]/[+0xc], 再调 FUN_080dd070 计算并存 [+0xe]/[+0x10], "
        "最后 FUN_080dcb54/FUN_080dced0 完成绘制. 被 13+ pack/save/dialog game_str 函数共用."),

    # 2026-04-30: 决斗场 hover-zone info 渲染 (HUD)
    ("FUN_080cb998", "render_duel_field_zone_info",
        "决斗场 hover-zone info 渲染派发器. 入参 (r0=player_flag 0=P1/1=P2, "
        "r1=mode 0..0x7f, r2=sub_idx). 主表 (table @ 0x080cb9cc) 12 entries 实际"
        "4 个 case body: mode 0..4 调 FUN_0803b618/5c0/4b0 helper 链; mode 5..a "
        "读 0x0201c510 决斗场卡 struct (P1/P2 stride 0x868); mode b 用 "
        "0x0201c600 + 0x02023130+0x50 复杂 lookup. 二级 if/else: mode c=Fusion "
        "Deck:, d=Deck:, e=Graveyard:, f=Removed Cards: (各 P1/P2 一份, "
        "logical_id 0x3ea..0x3f1) 调 game_str_id_to_row 取标签 + 数值. "
        "default(>=0x10) 经 LAB_080cbcfc 公共数字位拆分. 公共渲染路径调 "
        "text_render_wrapper x2 + commit_line_buffer_to_sprite_vram(0x0600a8e0) "
        "或 FUN_080cb1cc + FUN_080c8d30. 字体按 gSettings 语言切. 无返回值, "
        "纯写 OBJ VRAM 0x0600a8e0 (右对齐 240px)."),
    ("FUN_080cbf0c", "refresh_duel_field_zone_info",
        "render_duel_field_zone_info 的 state-driven wrapper. 读 gPageState "
        "[+0x210] u16 packed (bit7=player_flag, low7=mode, high7=sub_idx), "
        "若 mode==0xb 则 sub_idx 经 gPageState[+0x4c+player*2] 的 lookup 表"
        "重映射. 调 render_duel_field_zone_info(player, mode, sub_idx). "
        "无入参/无返回值. 用途: 光标 hover 决斗场 zone 改变后, 此函数按当前 "
        "state 重渲染. 14 个 caller 跨 PageManager / scene loader / banner 等."),

    # 2026-04-30: shuen demo 播放协调器 (play_ui_effect FUN_0801ef94 case 0x3c)
    # 2026-04-30 (后续): 修正 plate, FUN_0801ef94 实为 play_ui_effect (UI 特效派发器),
    # 不是 PageManager.
    ("play_demo_shuen", "play_demo_shuen",
        "demo 'shuen' (終焉) 过场动画播放协调器. 6-step 顺序状态机 on "
        "[gBannerState+0x10]: step 0=等帧 (FUN_080cca5c) / step 1=BG/palette "
        "setup (FUN_0801b7e8) / step 2=fs_load 资源 (FUN_0801ba4c) / step 3=播放 "
        "demo_shuen_state_machine / step 4=HUD 刷新 + refresh_duel_field_zone_info "
        "(强制推进) / step 5=等帧收尾 (FUN_080cca38) / default=cleanup (与 "
        "banner_anim_state_machine 同清理协议: 清 gBannerState[+0x0] bit1 + "
        "[0x02023345] bit0,2). 返回 1=busy / 0=done. 唯一 caller: play_ui_effect "
        "(FUN_0801ef94) case 0x3c (effect_id=0x3c). 推测是 shuen victory anim, "
        "等 runtime 验证."),

    # 2026-04-30: UI 特效派发器 (effect-id-based per-frame dispatcher)
    ("FUN_0801ef94", "play_ui_effect",
        "UI 特效派发器 (per-frame tick). r0 = effect_id (0..0x3d), 按 ID 分派到 "
        "~28 个独立的 effect handler 子状态机, busy/done 返回. dispatch table 中 "
        "重复 fallthrough 到 default 的 case = 未实现/无效 ID. 已识别 effect: "
        "0x01 = banner_anim_state_machine (pack 横幅出/入场), "
        "0x1a = play_card_zoom_in (小图→大图缩放过渡), "
        "0x3c = play_demo_shuen (终焉过场). 其他 case 子函数批量占位为 "
        "play_ui_effect_<id_hex>, 待详细分析. cmp 上限 0x3d, 大于则 default. "
        "case 0/0x18/0x19 共享 caseD_0 (state-bit 检查后选 FUN_080c4edc 或 FUN_080c4350); "
        "case 1 状态化 (banner_anim 或 FUN_080be600); case 2 三向状态分派. "
        "case 0x31/0x32 内联无 bl (特殊 readback)."),

    # 2026-04-30: 卡牌小图→大图缩放/旋转过渡动画 (play_ui_effect case 0x1a)
    ("FUN_080c3d20", "play_card_zoom_in",
        "卡牌小图→大图缩放/旋转过渡动画 (5-step on gUIEffectState[+0x0]). "
        "读 packed card_ref @ gUIEffectState[+0x4] (bit 0=side / [5:1]=row(5b) / "
        "[13:6]=col(8b) / bit 16,17=mode flag). 索引 EWRAM 卡牌信息数组 "
        "0x0201c510 + (row+col)*0x14 + side*0x868. step 0 = "
        "load_card_list_small_image x2 装载小图. step 1 = 起始帧 (FUN_080f6ccc + "
        "FUN_080c3880 stats overlay). step 2 = 4-tick affine 过渡: 用 "
        "rom_sin_table_q8 算 PA/PB/PC/PD, angle index ∈ rom_card_zoom_anim_curve "
        "{0,1,8,15}, scale = sin*5 + 0x100, 提交 OAM affine 矩阵 via FUN_080f72e8; "
        "sub_tick @ gUIEffectState[+0x18] 满 4 后主 step++. step 3 = 装第二张图 + "
        "FUN_080c38cc 全 bit-field stats. step 4 = 切大图模式 (FUN_080cb1cc, "
        "BG VRAM/palette 重磅上传). 返回 1=busy / 0=done. 唯一 caller: "
        "play_ui_effect (FUN_0801ef94) case 0x1a (effect_id=0x1a)."),

    # 2026-04-30: play_ui_effect 子 handler 占位名 (按 case_id hex 编号, 待详细分析)
    ("FUN_080cca80", "play_ui_effect_03",
        "占位名 - play_ui_effect (FUN_0801ef94) case 0x03 子状态机, 待详细分析."),
    ("FUN_080bdcfc", "play_ui_effect_04",
        "占位名 - play_ui_effect (FUN_0801ef94) case 0x04 子状态机, 待详细分析."),
    ("FUN_080bfe0c", "play_ui_effect_05",
        "占位名 - play_ui_effect (FUN_0801ef94) case 0x05 子状态机, 待详细分析."),
    ("FUN_080c91e0", "play_ui_effect_06",
        "占位名 - play_ui_effect (FUN_0801ef94) case 0x06 子状态机, 待详细分析."),
    ("FUN_080c2acc", "play_ui_effect_0b",
        "占位名 - play_ui_effect (FUN_0801ef94) case 0x0b 子状态机, 待详细分析."),
    ("FUN_080c3080", "play_ui_effect_0c",
        "占位名 - play_ui_effect (FUN_0801ef94) case 0x0c 子状态机, 待详细分析."),
    ("FUN_080bf394", "play_ui_effect_0e",
        "占位名 - play_ui_effect (FUN_0801ef94) case 0x0e 子状态机, 待详细分析."),
    ("FUN_080c25ac", "play_ui_effect_10",
        "占位名 - play_ui_effect (FUN_0801ef94) case 0x10 子状态机, 待详细分析."),
    ("FUN_080bf228", "play_ui_effect_11",
        "占位名 - play_ui_effect (FUN_0801ef94) case 0x11 子状态机, 待详细分析."),
    ("FUN_080c1ad0", "play_ui_effect_13",
        "占位名 - play_ui_effect (FUN_0801ef94) case 0x13 子状态机, 待详细分析."),
    ("FUN_080bea94", "play_ui_effect_15",
        "占位名 - play_ui_effect (FUN_0801ef94) case 0x15 子状态机, 待详细分析."),
    ("FUN_080befc0", "play_ui_effect_17",
        "占位名 - play_ui_effect (FUN_0801ef94) case 0x17 子状态机, 待详细分析."),
    ("FUN_080c0c70", "play_ui_effect_20",
        "占位名 - play_ui_effect (FUN_0801ef94) case 0x20 子状态机, 待详细分析."),
    ("FUN_080c0f38", "play_ui_effect_21",
        "占位名 - play_ui_effect (FUN_0801ef94) case 0x21 子状态机, 待详细分析."),
    ("FUN_080c17d4", "play_ui_effect_23",
        "占位名 - play_ui_effect (FUN_0801ef94) case 0x23 子状态机, 待详细分析."),
    ("FUN_080c1448", "play_ui_effect_25",
        "占位名 - play_ui_effect (FUN_0801ef94) case 0x25 子状态机, 待详细分析."),
    ("FUN_080c1c60", "play_ui_effect_2e",
        "占位名 - play_ui_effect (FUN_0801ef94) case 0x2e 子状态机, 待详细分析."),
    ("FUN_080c1e9c", "play_ui_effect_2f",
        "占位名 - play_ui_effect (FUN_0801ef94) case 0x2f 子状态机, 待详细分析."),
    ("FUN_080bd870", "play_ui_effect_30",
        "占位名 - play_ui_effect (FUN_0801ef94) case 0x30 子状态机, 待详细分析."),
    ("FUN_080c07e4", "play_ui_effect_33",
        "占位名 - play_ui_effect (FUN_0801ef94) case 0x33 子状态机, 待详细分析."),
    ("FUN_080c0a80", "play_ui_effect_34",
        "占位名 - play_ui_effect (FUN_0801ef94) case 0x34 子状态机, 待详细分析."),
    ("FUN_080bf7f8", "play_ui_effect_37",
        "占位名 - play_ui_effect (FUN_0801ef94) case 0x37 子状态机, 待详细分析."),
    ("FUN_080bf5a0", "play_ui_effect_38",
        "占位名 - play_ui_effect (FUN_0801ef94) case 0x38 子状态机, 待详细分析."),
    ("FUN_080bcbd4", "play_ui_effect_3a",
        "占位名 - play_ui_effect (FUN_0801ef94) case 0x3a 子状态机, 待详细分析."),
    ("FUN_080bc918", "play_ui_effect_3b",
        "占位名 - play_ui_effect (FUN_0801ef94) case 0x3b 子状态机, 待详细分析."),
    ("FUN_080c2544", "play_ui_effect_3d",
        "占位名 - play_ui_effect (FUN_0801ef94) case 0x3d 子状态机, 待详细分析."),

    # 2026-05-01: zone 光标单步推进函数 (按 RIGHT 时被 FUN_080c7ea0 反复调用,
    # 形成 10 步序列推进 gPageState[+0x210] packed cursor + 每次 render 一次).
    # GDB hbreak 验证: 单 caller 行 0x080c751f 命中 10 次跨多帧, mode/sub_idx
    # 序列 (0,3)→(0,4)→(0xE,0)→(0xF,0)→(0xA,0)→(0,0)→(0,1..4).
    ("FUN_080c716c", "apply_zone_cursor_step",
        "zone 光标单步推进 + 渲染. 入参 r0 = 当前 gPageState[+0x210] 的 u16 "
        "packed (bit7=player, 低7=mode, 高7=sub_idx). 流程: 解包 → 按 mode/input "
        "flag 决策新 packed (mode==0xd 走 gPrng+0x14e, 其他走 gPrng+0x146; "
        "mode==0xb 时 sub_idx 经 gPageState[+0x4c+player*2] 重映射) → 6-way "
        "switch on gP1[+0x1cf4] 选择 case 0/1/3 的 active-zone 决策路径 → "
        "可能走 LAB_080c7458 mode-bit 修正 (gPageState[+0x148] bit 0x10/20/40/80 "
        "→ FUN_080c6b04/6e9c). finalize 块: 写 gPageState[+0x210]=新packed → "
        "FUN_080c699c (zone state setter) → 若 packed 与 lookup 都未变则 return "
        "无 render, 否则 bl render_duel_field_zone_info(player,mode,sub_idx) "
        "(mode==0xb 时 sub_idx 用重映射值). 特殊路径: r4!=0 + FUN_080c707c!=0 "
        "时取 FUN_080c6638 entry → card_ids_080cc8c8 → 写 gPageState[+0x21c] "
        "card_id + 设 gPageState[+0x215] |= 4 (dirty), 不 render. 单次调用只 "
        "render 一次. caller: FUN_080c7ea0 内 0x080c7f9c (主决斗场显示统筹) + "
        "0x080ccbb2 (switchD case). runtime 验证: 按 RIGHT 触发 caller 反复调 "
        "本函数 10 次形成 cursor 推进序列."),

    # 2026-05-01: 主菜单 / 主调度循环命名族 (game_str_id_to_row 上溯链)
    # GDB 实测: 在 ss4 主菜单 Options 子页按 A, 触发 4 个 game_str_id_to_row hit
    # (id 0xbbd "Your Status" + 0xa8f "Language Selection"), lr 都在 FUN_080e58a8.
    # 静态分析 + ROM table @ 0x09E5ED24 解码出主菜单 6 子页:
    # Deck Edit / Free Duel / Challenge! / Get Cards / Forb/Ltd Card Lists / Options.
    ("FUN_080e58a8", "render_page_row_text",
        "渲染单个菜单 row 的双行文字 (标题 + 副标题/描述) 到 sprite VRAM. "
        "入参: r0 = page_idx (0..N, 决定 VRAM 偏移 0x06007480 + idx*0x600), "
        "r1 = string_id (u16, 对应 master pointer table row). 流程: memcpy "
        "ROM 0x09cf265c (0x600B template tile) 到 VRAM → font/glyph setup "
        "(FUN_080f0bb4 0x18,2) → 解 gSettings.lang (@ 0x02006c2c) 选 font_jp "
        "base → 两次 game_str_id_to_row(string_id) + text_render_wrapper "
        "(narrow 行 vs wide 行) → commit_line_buffer_to_sprite_vram. caller: "
        "FUN_080e7e0c case 4 内的 row 渲染循环."),
    ("FUN_080f48f8", "set_active_page_handler",
        "把 page handler fn_ptr 写入 IWRAM 槽供 main_dispatch_loop 间接跳转. "
        "入参 r0 = THUMB fn_ptr (e.g. 0x080e7e0d = FUN_080e7e0c+1). 内部清 "
        "多个 IWRAM 状态字 (gPrng+0x1f4/+0x1f8/+0x208 等), 重置 BG/blend "
        "寄存器, 设置 fn_ptr 到 [gPrng+0x1f0]. main_dispatch_loop 下一帧从该 "
        "槽读出执行. 多 caller (各 page 切换点)."),
    ("FUN_080f4b94", "main_dispatch_loop",
        "主调度循环 (无限循环): 每帧检查 IWRAM 状态 [0x03000184]/[gPrng+0x1f0] "
        "(active page handler fn_ptr 槽), 默认 fn = 0x080e7e0d (FUN_080e7e0c). "
        "通过 FUN_0810e5c8 间接调用 page handler. handler 返回非 0 则调 "
        "set_active_page_handler 注册 default 后继续 loop. 这是游戏的主 game "
        "loop wrapper (在 BIOS V-Blank IRQ 之外的 main thread)."),

    # 2026-05-01: 主菜单 12 个 init_fn (按 main_menu_page_table title_string_id 命名)
    # 数据源: ROM 0x09E5ED24 main_menu_page_table 12 entry + 4 sub-row arrays.
    # 静态分析 + 文本对应 (text/game-strings/en.txt) 决定命名, runtime 未逐一验证.
    ("FUN_08108ac0", "enter_deck_edit_page",
        "主菜单 'Deck Edit' (0x0bba) 子页入口. main_menu_page_table entry[0]/[6] "
        "init_fn (无 sub-row, init_fn 直接进入). 待 runtime 验证具体行为."),
    ("FUN_08108558", "enter_forb_ltd_lists_page",
        "主菜单 'Forb/Ltd Card Lists' (0x10ac) 子页入口. main_menu_page_table "
        "entry[4]/[10] init_fn (无 sub-row). 待 runtime 验证."),
    ("FUN_080e7994", "enter_campaign_page",
        "Free Duel 子菜单 'Campaign' (0x0a28) 入口. free_duel_rows row[0] "
        "init_fn. 也是 main_menu_page_table entry[7] 的 alt-mode 直进入口 "
        "(跳过 Free Duel 子菜单选择). 待 runtime 验证."),
    ("FUN_080e7a18", "enter_link_duel_page",
        "Free Duel 子菜单 'Link Duel' (0x0a29) 入口. free_duel_rows row[1] "
        "init_fn. 待 runtime 验证."),
    ("FUN_080e1a50", "enter_duel_puzzle_page",
        "Challenge! 子菜单 'Duel Puzzle' (0x0bc2) 入口. challenge_rows row[0] "
        "init_fn. 待 runtime 验证."),
    ("FUN_080e1390", "enter_limited_duel_page",
        "Challenge! 子菜单 'Limited Duel' (0x0bc3) 入口. challenge_rows row[1] "
        "init_fn. 待 runtime 验证."),
    ("FUN_080e3904", "enter_theme_duel_page",
        "Challenge! 子菜单 'Theme Duel' (0x0bc4) 入口. challenge_rows row[2] "
        "init_fn. 待 runtime 验证."),
    ("FUN_080e2c34", "enter_survival_duel_page",
        "Challenge! 子菜单 'Survival Duel' (0x0bc5) 入口. challenge_rows row[3] "
        "init_fn. 待 runtime 验证."),
    ("FUN_080dddc4", "enter_exchange_dp_page",
        "Get Cards 子菜单 'Exchange DP to Pack' (0x0bcc) 入口. get_cards_rows "
        "row[0] init_fn. 待 runtime 验证."),
    ("FUN_080dddd4", "enter_password_input_page",
        "Get Cards 子菜单 'PASSWORD' (0x0bcd) 入口. get_cards_rows row[1] "
        "init_fn. 待 runtime 验证."),
    ("FUN_080ece40", "enter_your_status_page",
        "Options 子菜单 'Your Status' (0x0bbd) 入口. options_rows row[0] "
        "init_fn. 待 runtime 验证."),
    ("FUN_080ebfb8", "enter_language_selection_page",
        "Options 子菜单 'Language Selection' (0x0a8f) 入口. options_rows row[1] "
        "init_fn. 待 runtime 验证."),

    # 2026-05-02: count_str_charlen (analysis-loop topo=2)
    ("FUN_0801455c", "count_str_charlen",
        "由 settings_080145bc/banlist_0801990c 等跨 banlist/font_jp/game_str/settings "
        "共 10 个调用方在文字渲染前调用, 用于测量字符串的字符单元数量. "
        "输入字符串遵循 1/2 字节混合编码: 若字节 bit7=1 则为双字节字符(前导+后继, ptr+2), "
        "否则单字节(ptr+1). 双字节检测由 [EWRAM+0x6c2c] & 0x7 决定(0=OCG/J 双字节, 非0=TCG 单字节). "
        "附加标志 [0x0202348c] 在 OCG 模式下可切换为字节计数路径. "
        "返回 r0=charlen (字符单元总数, 不含 0x00 终止符). 纯只读操作, 无任何内存写入."),

    # 2026-05-02: copy_str_unbounded (analysis-loop topo=1)
    ("FUN_08014470", "copy_str_unbounded",
        "无界字符串复制 wrapper. 调用方传入 r0=src, r1=dst; 本函数向 "
        "banlist_password_enter_char 传入 r2=0x05F5E0FF (99,999,999 无上限哨兵) "
        "实现不限长度的 src→dst 复制 (1/2 字节编码, 0x00 终止符). "
        "返回 r0=chars_written. 13 个 caller 覆盖 banlist/name_input/pass_input/game_str. "
        "已命名 caller: name_input_page_exit (0x080194ec)."),

    # 2026-05-02: find_substr_offset (analysis-loop topo=8)
    ("FUN_08014eb4", "find_substr_offset",
        "由 fs_load 在 GL 文件系统路径解析阶段调用，依次以 #、!、.LZ 三种前缀魔数作为 pKey 探测 pSrc 路径字符串，"
        "从而判断文件名是否携带特定标记。函数实现朴素线性 strstr 搜索：先用两次 measure_str_bytelen 确定有效搜索窗口"
        "（len_pSrc - len_pKey + 1），再逐偏移比对，首字节匹配后继续全长比对，成功返回首次命中的字节偏移（>=0），"
        "未命中返回 -1。源文件归属 GL/GL_File.c（assert 字符串泄漏锚）。"),

    # 2026-05-02: measure_str_bytelen (analysis-loop topo=6)
    ("FUN_08014ea0", "measure_str_bytelen",
        "由 FUN_08014eb4 (GL/GL_File.c 字符串搜索) 在子串搜索前调用, 分别测量 pSrc "
        "和 pKey 的字节长度以确定搜索范围上界. 逐字节遍历直到空字节, 返回不含终止符 "
        "的字节数 (等同 strlen 语义). 与 count_str_charlen (0x0801455c) 不同, "
        "本函数只做原始字节计数, 不感知游戏自定义编码宽度. "
        "调用方将两次返回值之差加一作为搜索循环次数上限."),

    # 2026-05-02: render_glyph_jp_4bpp_dual_layer (analysis-loop topo=19)
    ("FUN_080f1440", "render_glyph_jp_4bpp_dual_layer",
        "由 font_jp_080f21e8 在检测到 [0x02006ed0+0x15]&0x10==1 (4bpp 模式标志) 时调用, "
        "作为 render_glyph_jp_dual_layer 的 4bpp 替代路径. 接受 u16 char_code, 经 "
        "char_code_to_glyph_index 映射后查 font_jp_charset_table/font_jp_stride_table "
        "定位字形位图, 以 4bpp word 写 (str r0,[r4]+adds r4,#0x20 双写) 输出到 OBJ sprite "
        "tile 缓冲区 (*gfx_state). 按 glyph_width+(x&7)>16 分溢出路径 (跨 tile 列) "
        "和单列路径两支."),

    # 2026-05-02: blit_glyph_row_colored (analysis-loop topo=22)
    ("FUN_080f1180", "blit_glyph_row_colored",
        "由 render_glyph_jp_single_layer (0x080f19a4) 在逐字符渲染循环中按字符高度的一半 (每字符 2 次) 调用, "
        "仅在渲染上下文要求显式色彩覆盖时激活 (调用方 sp+0x8 标志非零时分派到本函数, 为零则改调 blit_glyph_row_to_buffer). "
        "与 blit_glyph_row_to_buffer (0x080f0f70) 处理同一 row 方向写入, 关键区别在于 r3 额外传入显式前/背景颜色 nibble "
        "(低 4 位前景, 高 4 位背景), 每次迭代同时写两个相邻像素位置, "
        "按 [0x02006ed0+0x15] bit3 区分 4bpp (nibble read-modify-write) 与 8bpp (byte write) 两路, "
        "将像素写入 EWRAM 字形 tile 缓冲区."),

    # 2026-05-02: blit_glyph_col_to_buffer (analysis-loop topo=21)
    ("FUN_080f1070", "blit_glyph_col_to_buffer",
        "由 render_glyph_jp_single_layer (0x080f19a4) 在逐字符渲染循环中每字符调用 6 次, "
        "每次处理字形一列像素的写入. 以 10 次行迭代 (r5=0..9) 遍历字形高度, 对列像素掩码 "
        "(10-bit bitmask, 经高位寄存器传入) 中每个置位行计算 VRAM tile 字节偏移, "
        "按 [0x02006ed0+0x15] bit3 区分 4bpp (nibble read-modify-write) 与 8bpp (byte write) 两路, "
        "将颜色值写入 EWRAM 字形缓冲区. 是 blit_glyph_row_to_buffer (0x080f0f70) 的列方向对称体, "
        "行处理 8 像素改为列处理 10 行."),

    # 2026-05-02: render_glyph_indexed_dual_layer (analysis-loop topo=17)
    ("FUN_080f1720", "render_glyph_indexed_dual_layer",
        "由 FUN_080f21e8 在检测到字体标志 [0x02006ed0+0x15]&0x10 后调用. "
        "直接以 u8 字形索引(0-255)查 ROM 字体位图表(窄字 10B/条目 @ 0x09ccb490, "
        "宽字 12B/条目 @ 0x09ccbe90), 将字形以 4bpp 双写方式展开并写入 OBJ tile 缓冲区 "
        "(*[0x02006ed0]). 跳过 char_code_to_glyph_index 映射, 适用于小字符集快速渲染路径. "
        "双写(两次 str 间距+0x20)对应同一字形行在 sprite tile 内的两个 4bpp 横向分区."),

    # 2026-05-02: resolve_prhlist_entry_name_ptr (analysis-loop topo=16)
    ("FUN_08016afc", "resolve_prhlist_entry_name_ptr",
        "由 card_list_screen_init/FUN_081061d0/FUN_08107198 在 banlist 界面调用. "
        "给定禁止条目结构体指针(pDst), 读 +0x201 处 u8 nameID, assert nameID!=0 "
        "(GL/PRH_Main.c:38 'pDst->nameID'), 调 game_str_id_to_row(nameID+0x1072) "
        "得 master_row, 再读 WRAM[0x02006c2c] 低3位选语言槽, "
        "返回 game_str_ja 基址+偏移 的本地化卡名字符串指针. 纯查询叶子, 无外部副作用."),

    # 2026-05-02: suppress_assert_report (analysis-loop topo=7)
    ("FUN_080fa4dc", "suppress_assert_report",
        "发布版空断言回调 (release build no-op). 由 GL/FS/nnsys/游戏各模块断言宏在条件不满足时调用; "
        "接收 filename/line/expr/assert_type 后立即 bx lr, 不产生任何输出或副作用. "
        "共 137 个调用函数、364 处调用点, 覆盖 GL_Common.c / GL_File.c / nnsys/g2d/*.c 等 26 个源文件模块."),

    # 2026-05-02: count_word_charlen (analysis-loop topo=28)
    ("FUN_080f1bbc", "count_word_charlen",
        "由 font_jp_080c76c0/font_jp_080f21e8 在行换行判断前调用, 测量下一个词元的字符数. "
        "从当前字节指针逐字节扫描: 空白/连字符停止返回; 行末禁則字符(!//:;?)计入后立即返回; "
        "转义前缀(%/@ 0x25/0x40)跳过继续扫; 句点'.'后跟'.'则连续扫否则计入停止. "
        "返回值供调用方乘以字符宽度后与行宽阈值 0x17<<3=184px 比较决定是否换行. 纯叶子函数, 无外部副作用."),

    # 2026-05-02: test_char_kinsoku_head (analysis-loop topo=27)
    ("FUN_080f05d0", "test_char_kinsoku_head",
        "由 font_jp_080c76c0/font_jp_080f21e8 调用，判断字符是否属于行頭禁則集（不允许出现在行首）。"
        "流程: char_code → char_code_to_glyph_index → font_jp_sjis_lookup_table 取 SJIS 码 → "
        "逐范围比对小假名(ぁぃぅぇぉ/ァィゥェォッャュョヶ)、标点(、。‐／)及闭括号类; 命中返回 1，否则返回 0。"
        "与 test_char_kinsoku_tail (FUN_080f0720) 共同构成 JIS X 4051 禁則处理对。"),

    # 2026-05-02: render_jp_string_glyph_loop (analysis-loop topo=29)
    ("FUN_080f21e8", "render_jp_string_glyph_loop",
        "font_jp 模块主字形渲染循环. 被 text_render_wrapper(0x080f2a7c,wrap=1)/"
        "FUN_080f2a44(wrap=0)/FUN_080f2a60(wrap=0,extra_x_offset) 三个薄包装调用. "
        "入参: r0=x_start(格), r1=y_tile_offset, r2=line_width(格), r3=str_ptr, "
        "sp+0x0=wrap_flag, sp+0x4=extra_offset. 初始化 gfx_ctx[0x02006ed0] 各字段, "
        "逐字节遍历字符串, 按编码范围+[gfx_ctx+0x15]标志位派发到四条渲染路径: "
        "render_glyph_jp_dual_layer(8bpp默认双层)/render_glyph_jp_4bpp_dual_layer"
        "(bit4=1时4bpp路径)/render_glyph_indexed_dual_layer(glyph_index直传4bpp路径)/"
        "render_glyph_jp_single_layer(单字节字符). 换行前调 count_word_charlen 测量词元宽度, "
        "调 test_char_kinsoku_head 实现行首禁則检测. "
        "推进 [gfx_ctx+0x24] 游标, 遇0x00或超行宽退出. "
        "返回 r0=cursor_end_packed ([gfx_ctx+0xe]<<6|[gfx_ctx+0xc])."),

    # 2026-05-02: dispatch_text_render_by_mode (analysis-loop topo=31)
    ("FUN_080175f4", "dispatch_text_render_by_mode",
        "由 name_input 页面族（FUN_08017cd0、FUN_080183d0 等 font_jp 簇）调用，根据第 5 个参数 render_mode "
        "在三种渲染路径之间分发：mode=0x20 将单字符偏移 (+1,+1) 后交给 text_render_wrapper 渲染；"
        "mode=0x80 向 (x,y) 的 8 邻域各调用一次 text_render_wrapper（描边/阴影 pass，使用 shadow_color），"
        "再在 (x,y) 正中追加一次前景 pass（使用 fg_color），实现 8 方向描边效果；"
        "其余 mode 值则直接在 (x,y) 渲染一次（无描边）。"
        "调用方传入 render_mode=0x80 时产生「文字描边」视觉效果，是 name_input 页面标题文字渲染的核心路径。"),

    # 2026-05-02: init_font_jp_render_context (analysis-loop topo=32)
    ("FUN_080f42b4", "init_font_jp_render_context",
        "由多个 text-box setup 函数（FUN_08017798 / FUN_08019820 等）在页面初始化阶段调用，"
        "负责将全局 font_jp 渲染上下文 (EWRAM 0x02006ed0, 104 字节) 清零后写入三项核心参数："
        "VRAM 目标基址、水平方向 tile 数（width_tiles）、垂直方向 tile 数（height_tiles）。"
        "同时查询 EWRAM[0x02006c2c] 低 3 位确定 bpp/语言模式标志，从 font_jp_base_table "
        "选出对应的渲染函数指针写入 context[+0x04]，最后在 context[+0x15] 置位 bit4（0x10）"
        "标记初始化完成。调用方随即修改 context[+0x08] 低位和 context[+0x15] 其它位完成各自的显示模式配置。"),

    # 2026-05-02: setup_font_jp_ctx_obj_vram_row (analysis-loop topo=33)
    ("FUN_080177dc", "setup_font_jp_ctx_obj_vram_row",
        "由 FUN_080183d0（名字输入页面字符串渲染包装层）在 text-box 初始化阶段调用，"
        "负责以 OBJ 区 VRAM（0x06010000）为目标，按 tile 行索引计算 VRAM 基址"
        "（基址 = 0x06010000 + r0 × 0x20），调用 init_font_jp_render_context 完成 "
        "104 字节渲染上下文清零和三项核心参数写入，之后追加置位 context[+0x15] bit5（0x20），"
        "并根据 r3 bit0 将 context[+0x8] bit1 设置为对应渲染模式标志，"
        "最后重新从 font_jp_base_table 读取函数指针写入 context[+0x04]。"
        "与使用 BG VRAM（0x06000020）的 FUN_08017798 形成对称：该函数覆盖 OBJ 精灵 VRAM 区，"
        "且 tile 行索引由调用方参数决定，适用于名字输入页面的多行文字 tile 槽配置。"),

    # 2026-04-30: demo 'shuen' (終焉) 过场动画状态机
    ("FUN_0801bd08", "demo_shuen_state_machine",
        "demo 'shuen' (終焉) 过场动画状态机 (7-state on [gDemoState+0x8c] bits 9..16). "
        "step 0 INIT: 加载 BG1 (FUN_0801b93c 'demo/shuen/shuen_bg1.LZ5bg') + BG2 "
        "(fs_load 'demo/shuen/shuen_bg2.LZ5bg' 缓存到 [gDemoState+0x88]) + OAM/window "
        "+ 启 fade-in. step 1=wait init (poll FUN_080148f4). step 2=phase A "
        "(keyframe 0x09e3d01f, sub-state 按 0x3c/0x96/0x4b/0xa5/0xe6 分支). step 3=wait A. "
        "step 4=phase B (双 keyframe 0x09e3d022/0x09e3d028, 6帧循环, sub-state==0x78 推进). "
        "step 5=fadeout (3 种 brightness/blend 模式). step 6=wait fadeout. default 路径 "
        "cleanup (FUN_0801522c sprite + FUN_08015160 + FUN_080148f4 final poll). "
        "返回 1=busy / 0=done. 唯一 caller: FUN_080bc880 case 3 (scene loader)."),
]


def do_rename(old, new, comment):
    st = currentProgram.getSymbolTable()
    syms = st.getSymbols(old)
    target = None
    for s in syms:
        if s.getSymbolType().toString() == "Function":
            target = s
            break
    if target is None:
        # 也许已被改名, 按地址抓
        print("[miss] %s -> %s (symbol not found, maybe already renamed)" % (old, new))
        return False
    if RUN_DRY:
        print("[dry] %s @ %s -> %s" % (old, target.getAddress(), new))
        return True
    try:
        target.setName(new, SourceType.USER_DEFINED)
    except Exception as e:
        print("[fail] rename %s -> %s: %s" % (old, new, e))
        return False

    # plate comment (函数上方)
    # 规则:
    #   - first arg 是 FUN_xxxxxxxx (首次命名): 仅在无 plate 时写, 不覆盖手工编辑
    #   - first arg 是 user-defined name (重命名旧 entry): 强制覆盖, 因为名字变了
    #     plate 也得同步, 旧 plate 如果有 mojibake 也顺便修了
    is_rename_userdefined = not old.startswith("FUN_")
    try:
        # 显式 utf-8 decode -> Java String. 若已是 unicode 直接用.
        if isinstance(comment, str):
            comment_u = comment.decode("utf-8")
        else:
            comment_u = comment
        func = getFunctionAt(target.getAddress())
        if func is not None:
            listing = currentProgram.getListing()
            cu = listing.getCodeUnitAt(func.getEntryPoint())
            if cu is not None:
                existing = cu.getComment(CodeUnit.PLATE_COMMENT)
                if is_rename_userdefined or not existing:
                    cu.setComment(CodeUnit.PLATE_COMMENT, comment_u)
    except Exception as e:
        print("[warn] plate comment %s: %s" % (new, e))

    print("[ok] %s -> %s" % (old, new))
    return True


def main():
    ok = 0
    for old, new, comment in RENAMES:
        if do_rename(old, new, comment):
            ok += 1
    print("[done] RenameKnownFunctions: %d/%d" % (ok, len(RENAMES)))


main()
