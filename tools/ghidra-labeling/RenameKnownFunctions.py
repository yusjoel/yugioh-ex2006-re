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

    # 2026-05-02: render_jp_text_to_vram_obj (analysis-loop topo=34)
    ("FUN_080183d0", "render_jp_text_to_vram_obj",
        "name_input 页面文字渲染的薄包装函数。由 name_input 页面渲染子树的两个上层函数调用："
        "addr 0x08017b44（tags: game_str;name_input，场景文字行列渲染，调用 3 次）和 addr 0x08018774"
        "（tags: font_jp;name_input，当前被选中字符高亮显示，调用 1 次）；两者均尚未命名，通过 name_input "
        "EWRAM 缓冲区 0x02029250 + FUN_08018400 计算 vram_row 后压栈传入本函数；本函数先调 "
        "setup_font_jp_ctx_obj_vram_row 配置 JP 字体渲染上下文（目标 VRAM OBJ 行 + 图层模式），"
        "再以硬编码的模式参数（r1=1, r2=1, r3=7, arg5=8, arg6=0x80）调 dispatch_text_render_by_mode，"
        "将字符串渲染到 VRAM OBJ 瓦片（精灵层）。0x80 模式对应 dispatch 内的 JP 8 行字形 OBJ 渲染路径。"),

    # 2026-05-02: refresh_selected_char_obj_tile (analysis-loop topo=36)
    ("FUN_08018774", "refresh_selected_char_obj_tile",
        "banlist/font_jp/settings callers (0x080187e0/0x08018838/0x0801950c) "
        "name_input 界面每次切换/确认字符时触发. "
        "读 IWRAM 0x02029564 (游戏状态基址 0x02029250 + 0xc5*4) 处的 2-bit ping-pong 槽位选择子, "
        "切换到对端槽位 (bit0 XOR 1), 调 zero_obj_vram_tiles 清空该槽位的 34 块 OBJ VRAM 瓦片, "
        "再调 render_jp_text_to_vram_obj 把当前选中假名写入那 34 块瓦片, "
        "最后将翻转后的槽位值写回原地址, 完成双缓冲换页, 防止字符更新时 OBJ VRAM 可见撕裂."),

    # 2026-05-02: zero_obj_vram_tiles (analysis-loop topo=35)
    ("FUN_08018400", "zero_obj_vram_tiles",
        "render_jp_text_to_vram_obj OBJ tile CpuSet fill. "
        "name_input addr 0x08017b44 (x3) + addr 0x08018774 (x1) "
        "render_jp_text_to_vram_obj. "
        "BIOS CpuSet SWI 0x0B fill+word mode: "
        "OBJ VRAM [0x06010000 + tile_idx*32, +num_tiles*32) := 0."),

    # 2026-05-02: commit_input_name_to_buf (analysis-loop topo batch)
    ("FUN_0801950c", "commit_input_name_to_buf",
        "由 page_state_dispatcher (0x08019574, tags: banlist,font_jp,name_input,settings) "
        "在玩家确认输入名称时调用. 将 r0 指向的已输入名称串复制到 EWRAM 名称缓冲区 [0x02029512], "
        "同时将字符计数写入 [0x0202956e], 最后调用 refresh_selected_char_obj_tile 刷新光标 "
        "OBJ tile 显示. 返回 1 表示确认成功, 是名称输入页 (禁止牌/设置/玩家名) confirm 动作的最终落地函数."),

    # 2026-05-02: return_void_handler (analysis-loop topo batch)
    ("FUN_080fa4d4", "return_void_handler",
        "空回调函数体, 单指令 bx lr 立即返回. "
        "由 page_state_dispatcher (0x08019574, tags: banlist,font_jp,name_input,settings) "
        "及其他 8 个页面状态机函数注册为 no-op 页面处理器槽位 (init/tick/exit 等). "
        "不接受任何参数, 无任何副作用, 无返回值. "
        "与同簇 0x080fa4c0/0x080fa4d8 均为相同结构的空 handler 占位, "
        "区别于 suppress_assert_report (0x080fa4dc, 4 参数断言 nop)."),

    # 2026-05-02: copy_bytes_by_halfword (analysis-loop topo batch)
    ("FUN_080f4ea4", "copy_bytes_by_halfword",
        "通用内存复制工具函数, 以 16 位 (halfword) 步长为主循环单元, 处理末尾奇数字节. "
        "由 card_info_page_init_bg0 (0x0801d45c), card_image_decode_wrapper (0x0801d998), "
        "card_info_page_finalize (0x0801e100) 等 150 个调用方在 VRAM/PALRAM/EWRAM 数据搬运场景下调用. "
        "参数 r0=dst, r1=src, r2=byte_count; 先以 ldrh/strh 对拷 byte_count/2 次, "
        "若 byte_count 为奇数则额外拷贝末 1 字节. 无返回值."),

    # 2026-05-02: BATCH-10 落地 (topo=42/44/46/47/48/49/50/51/52/53)
    ("FUN_080f4f08", "copy_memory_dma3_with_cpu_fallback",
        "向目标地址复制 byte_count 字节，根据 gPrng+0x174 的模式控制位选择传输后端: "
        "bit12 置位时退化为 CPU halfword 循环 (copy_bytes_by_halfword), "
        "bit13 置位时调用 BIOS CpuSet 字对齐拷贝, "
        "否则使用 DMA3 以 1024 字节 (0x200 halfword) 为块分多次触发, "
        "等待 DMA_ENABLE 位清零后继续下一块, 尾余 (<= 0x3ff 字节) 由最后一次 DMA3 搬完. "
        "由 decode_card_image_6bpp (addr 0x0801d290) 及多个 scene_pack/card_image 场景调用, "
        "是游戏 VRAM/EWRAM 大块数据搬运的统一入口."),
    ("FUN_080f4e74", "zero_fill_by_halfword",
        "将 dst 起始的 byte_count 字节全部清零, 内循环以 strh 双字节步进写 0, "
        "最后若字节数为奇数则补 strb 写末尾 1 字节. "
        "indeg=130, 是全 ROM 最高频使用的零填充 utility; "
        "由 card_info_page_enter_with_card_id、card_info_page_init_bg0、draw_decimal_with_offset "
        "等覆盖 card_info/font_jp/vram 全模块的函数在 VRAM、PALRAM、EWRAM 缓冲区清零场景下广泛调用."),
    ("FUN_080f42a0", "store_ewram_ctx_ptr_and_clear_mode_flags",
        "将 r0 (指针值) 存入 EWRAM 固定槽 0x02006ed0, 随后读取该结构体偏移 0x15 的标志字节, "
        "清除 bit0 和 bit4 后写回. indeg=24, 由 card_info_page_init_bg0 及多个 "
        "bg/vram/display/palette 组合的页面初始化函数调用, 作用是在页面切换时登记当前显示上下文指针"
        "并将模式/dirty 标志复位为初始状态, 为后续 BG 渲染做前置清理."),
    ("FUN_080f5a10", "reset_bg_hscroll_regs_and_shadows",
        "将全部 4 个 BG 层的水平滚动硬件寄存器 (BG0HOFS~BG3HOFS, 步长 +4) 清零, "
        "同时将 IWRAM 影子寄存器 gPrng+0x1e0、+0x1e2、+0x1e4、+0x1e6 "
        "(对应 BG0..BG3 HOFS 软件副本) 一并清零. "
        "仅被 reset_all_bg_scroll_regs_and_shadows (FUN_080f5a88) 调用 (作为 HOFS 分支), "
        "由后者在页面初始化时与 VOFS 分支 (FUN_080f5a4c) 配对调用, 完成全 BG 滚动归零."),
    ("FUN_080f5a4c", "reset_bg_vscroll_regs_and_shadows",
        "将全部 4 个 BG 层的垂直滚动硬件寄存器 (BG0VOFS~BG3VOFS, 步长 +4) 清零, "
        "同时将 IWRAM 影子寄存器 gPrng+0x1e8、+0x1ea、+0x1ec、+0x1ee "
        "(对应 BG0..BG3 VOFS 软件副本) 一并清零. "
        "与 sibling reset_bg_hscroll_regs_and_shadows (FUN_080f5a10) 结构完全对称, "
        "仅被 reset_all_bg_scroll_regs_and_shadows (FUN_080f5a88) 调用作为 VOFS 分支, "
        "在页面初始化时完成垂直滚动归零."),
    ("FUN_080f5a88", "reset_all_bg_scroll_regs_and_shadows",
        "依次调用 reset_bg_hscroll_regs_and_shadows (FUN_080f5a10) 和 "
        "reset_bg_vscroll_regs_and_shadows (FUN_080f5a4c), "
        "将全部 8 个 BG 滚动硬件寄存器 (BG0HOFS~BG3VOFS) 及 8 个 IWRAM 影子值 "
        "(gPrng+0x1e0~+0x1ee) 全部归零. indeg=24, 是页面初始化链的标准清理步骤, "
        "由 card_info_page_init_bg0 及多个 bg/display/palette 组合的场景初始化函数在进入新页面时调用, "
        "确保上一页面的滚动偏移不影响新 BG 布局."),
    ("FUN_080f4e98", "zero_fill_halfword_wrapper",
        "对 zero_fill_by_halfword (FUN_080f4e74) 的单层包装: "
        "以标准 push/bl/pop 调用约定封装, 参数直传 (r0=dst, r1=byte_count), 无额外逻辑. "
        "indeg=29, 是 scene_pack/card_image 等模块优先使用的清零入口; "
        "其直接 callee FUN_080f4e74 indeg=130, "
        "两者共同服务于全 ROM 的 VRAM/EWRAM 缓冲区清零需求."),
    ("FUN_080f5e98", "clear_obj_list_entries_range",
        "遍历 OBJ 列表 [start_idx, end_idx), 将每个 8 字节条目的前 8 字节清零 (stmia + str), "
        "再对条目内偏移 +5 和 +1 的字节做位域清除操作. "
        "列表基址从 IWRAM 固定地址 0x030001fc (= gPrng+0x1bc) 加载, 每条目步长 = idx*8. "
        "由 init_scene_obj_list (FUN_080f5ef4, 初始化全部 128 条目) 及 "
        "FUN_080f4adc (scene_duel_puzzle;sprite 场景复位) 调用, "
        "用途是在场景切换或 OBJ 列表重建前批量重置条目状态. "
        "[SB-080f5e98-1] 条目 +5/+1 bit mask 操作语义待 runtime 验证."),
    ("FUN_080f5ef4", "init_scene_obj_list",
        "初始化场景 OBJ 列表: 调用 clear_obj_list_entries_range(0, 0x80) 清零全部 128 条目, "
        "然后在列表末尾写入容量标记 [base+0x400]=0x80 (capacity=128) "
        "和计数标记 [base+0x401]=0 (count=0), 完成 OBJ 列表的空初始化. "
        "由 reset_display_and_obj_vram (FUN_080f7674) 以及两个 scene_card_list "
        "palette/display 初始化函数调用, 是进入卡牌列表或调色板初始化场景前的必备前置步骤."),
    ("FUN_080f7674", "reset_display_and_obj_vram",
        "读取 DISPCNT (0x04000000) 当前视频模式 (bits 2:0), "
        "将 OBJ PALRAM (0x05000200, 0x200 字节) 清零, "
        "再按模式分支清零对应的 VRAM OBJ tile 区域 "
        "(mode 0/1/2: 0x06010000 起 0x8000 字节; mode 3/4/5: 0x06014000 起 0x4000 字节); "
        "若 r5 (r0 输入) 不为 0 则将其写入 gPrng+0x1bc (OBJ 列表指针槽); "
        "最后调用 init_scene_obj_list (FUN_080f5ef4) 重建空 OBJ 列表. "
        "indeg=22, 由 card_info_page_init_bg0 及多个 bg/vram/display/palette 场景初始化链"
        "在页面切换时调用, 是显示状态完全重置的标准入口."),

    # 2026-05-02: BATCH-15 落地 (topo=56/59/60/61/62/64/66/68/69/70/72/73/74/75/76)
    ("FUN_080ee988", "resolve_card_gfx_pointer_by_type",
        "按卡片 ID 查卡片属性表 (card_stats_table), 先读 [0x080000ae] 判断区域码是否为 0x4a (日版特判), "
        "再用属性字段 (offsets 0x16*id+0x0) 与多个边界值 (0x1497/0x1498/0x1499) 做多路分支, "
        "结合 IWRAM [0x02000000+0x6c2c] 中的 byte&0x7 作为阵营/属性子类索引, "
        "最终返回图形数据指针 (ROM 段内地址, 供调用方写入 sprite 参数). 该函数是卡面辅助图形 "
        "(怪兽属性图标/魔陷/效果等) 的路由核心, 每次绘制卡片信息页时被调用."),
    ("FUN_0801d510", "render_card_name_to_line_buf",
        "接收卡片索引 (r0), 从 card_stats_table 读取卡种字段判断是否为特殊宽度 (0x16/0x17), "
        "再从 IWRAM 状态字 [0x02006c2c] 读取语言/charset 标志调用 select_charset_then_load_name "
        "加载卡名字符串, 然后按双字节 JP 编码逐字素调用 render_glyph_jp_dual_layer 将卡名渲染进行缓冲区. "
        "限宽逻辑 (cmp #0x5c) 防止卡名溢出单行. 被 FUN_0801d6b4 (card_image_decode_wrapper 下一级) "
        "调用, 构成绘制卡片详情页卡名行的核心路径."),
    ("FUN_080f0bb4", "setup_line_buf_pos_and_font",
        "初始化 IWRAM 渲染状态结构体 [0x02006ed0] 中的行缓冲位置字段和字体指针字段, "
        "为随后的字素渲染函数 (render_glyph_jp_dual_layer / blit_glyph_row_to_buffer 等) 准备上下文. "
        "r0 传入 X 坐标 (低 8 bit 写入 OAM 位置字), r1 传入行号/Y 坐标, "
        "函数通过多个 mask/orr 操作拼接 OAM 属性字 ([0x02006ed0+0x8]/[+0xa]/[+0xb]/[+0xc]), "
        "最后从 font_jp_base_table 选取字体位图指针写入 [0x02006ed0+0x4]. "
        "indeg=57 确认其为所有 JP 字符渲染路径的公共 setup 入口."),
    ("FUN_080f35e8", "blit_tile_color_to_vram_region",
        "从 IWRAM 渲染状态结构体 [0x02006ed0] 读取 tile 列数和行数, 然后以双色 (r1 低字节=前景色 4bpp 索引, "
        "r1 高字节=背景色 4bpp 索引) 对一块矩形 tile 区域执行像素级 OR-mask 写入. "
        "外层循环按 tile 行 (从结构体读取行/列计数乘积), 内层按列步进 0x40 字节/tile 行, "
        "对每个非零像素 tile 执行 strh 到 VRAM 基址 (r0). r0 入口保存至 r2 供内层循环使用. "
        "被 commit_line_buffer_to_sprite_vram 和两个未命名邻居调用, 是将行缓冲区内容刷入 "
        "OBJ VRAM 的最后一步位操作核心."),
    ("FUN_080f4ed0", "copy_words_aligned",
        "将 r1 指向的源缓冲区以 word (32 bit) 为单位复制 ceil(r2/4) 个 word 到 r0 (r3) 指向的目标. "
        "r2 传入字节数, 函数对其执行 (r2+3)>>2 向上取整得 word 计数, 然后以 ldmia/stmia 对循环复制. "
        "r2==0 时直接返回. 纯工具函数, 被 commit_line_buffer_to_sprite_vram / pack_detail_bg_tile_load "
        "等多个 VRAM 写入路径调用, 负责将内存块对齐复制到目标区域."),
    ("FUN_0801d6b4", "draw_card_name_label_to_vram",
        "作为 card_image_decode_wrapper 的直接子调用, 负责将卡名文本行渲染并提交到 OBJ VRAM. "
        "步骤固定三段: (1) 调用 setup_line_buf_pos_and_font (FUN_080f0bb4) 以 x=0xe/y=2 初始化 "
        "行缓冲区位置和字体指针, 目标 tile 基址 0x06001c00<<2=0x06007000; "
        "(2) 调用 render_card_name_to_line_buf (FUN_0801d510) 以卡片索引渲染卡名到行缓冲区; "
        "(3) 调用 commit_line_buffer_to_sprite_vram 将行缓冲区内容刷新到 VRAM 地址 0x06008500. "
        "indeg=1 (唯一来自 card_image_decode_wrapper), 确认是卡名行的专属绘制函数."),
    ("FUN_080f1b0c", "blit_glyph_columns_to_buf",
        "从 r0 指向的字符数据流 (JP 双字节编码序列) 按列循环读取字素 halfword, "
        "对每个 halfword 分离低字节 (glyph_index&0xff) 后调用 blit_glyph_row_to_buffer "
        "将字素列数据写入行缓冲区指定位置 (r2=dst_col_start, r3=palette_idx). "
        "内部计数器初值 0x3 控制循环 (r9 递减至 -1 共 4 次, 处理双字节流中 4 个字素). "
        "被 FUN_0801d70c 以固定 r1=0x1a/0x22/0x40/0x48 四次调用, 对应 ATK/DEF 数字各位."),
    ("FUN_0801d70c", "render_atk_def_digits_to_buf",
        "接收卡片 ATK (r0) 和 DEF (r1) 值, 通过 __umodsi3/__udivsi3 逐位分解十进制数字, "
        "对 ATK 的个/十/百/千位分别以固定列偏移 (0x36, 0x32, ...) 调用 FUN_080f1b0c "
        "将数字字素渲染到行缓冲区中对应列; DEF 同理以另一组列偏移渲染. "
        "行缓冲区基址从 DAT_0801d7c8 (0x0984f59c) 读取, 数字字素基址从 DAT_0801d7cc (0x0984f54c). "
        "被 FUN_0801d7d0 (draw_atk_def_label_to_vram) 调用, 是 ATK/DEF 数值渲染的计算核心."),
    ("FUN_0801d7d0", "draw_atk_def_label_to_vram",
        "card_image_decode_wrapper 的第二个直接子调用, 负责将卡片 ATK/DEF 数值渲染并提交到 OBJ VRAM. "
        "步骤三段: (1) 调用 setup_line_buf_pos_and_font 以 x=0xe/y=2 + tile 基址 0x06001c00 "
        "初始化行缓冲区; (2) 调用 render_atk_def_digits_to_buf (FUN_0801d70c) 将 ATK (r0) 和 "
        "DEF (r1) 数字字素渲染到缓冲区; (3) 调用 commit_line_buffer_to_sprite_vram 以目标地址 "
        "0x06008580 刷新到 VRAM. 与 draw_card_name_label_to_vram (FUN_0801d6b4) 结构完全对称, "
        "两者均被 card_image_decode_wrapper 以 indeg=1 调用."),
    ("FUN_080f54e0", "count_bytes_until_null",
        "从 r0 指向的字节序列起始处向后扫描, 统计非零字节个数 (即 C strlen 语义), "
        "结果以 r0 返回. 常量 r2 从 0 自增, r1 指针逐字节步进, 遇到 0x00 停止. "
        "indeg=22 (高 indeg util), 被 draw_decimal_with_offset 等字符串处理函数调用, "
        "用于在渲染前获取字符串/字素序列的字节长度."),
    ("FUN_0801d830", "render_card_level_text_to_buf",
        "接收 level 字符串表索引 (r0, 来自 lookup_level_glyph_index 返回值), 从 ROM 字符串表 "
        "(0x09e5f726 = level/type 文字表) 定位对应文本, "
        "先以固定 4 次调用 blit_glyph_columns_to_buf (FUN_080f1b0c, r1=0x1a/0x22/0x40/0x48) "
        "将 \"LEVEL\"/\"RANK\" 等标签字素写入缓冲区, "
        "再调用 count_bytes_until_null 取文本长度, 然后逐字节解码数字 (0x30-0x39 -> %10 取余, "
        "特殊码 0x3f/'?'->0xe, 0x58/'X'->0xf) 并以 FUN_080f1b0c 渲染各数字字素到对应列. "
        "被 FUN_0801d92c (draw_card_level_label_to_vram) 调用, 是 Level/Rank 数值行的渲染核心."),
    ("FUN_080ef454", "lookup_level_glyph_index",
        "接收卡片索引 (r0, u16 截断), 以步长 0x16 (22 bytes/entry) 在 card_stats_table 中定位该卡行, "
        "读取 level 字段 (halfword at offset 0), 然后与 level_signature_table 中的特征值逐项比对 "
        "(最多 0xd=13 项, 步长 0x14=20), 返回匹配项的索引 (0-12), 未找到返回 -1. "
        "返回值被调用方 FUN_0801d92c 用于选择对应等级字素图案 (Level/Rank 星图)."),
    ("FUN_0801d92c", "draw_card_level_label_to_vram",
        "card_image_decode_wrapper 的第三个直接子调用, 负责将卡片等级 (Level/Rank) 星图渲染并提交到 OBJ VRAM. "
        "先调用 lookup_level_glyph_index (FUN_080ef454) 以卡片索引查 level_signature_table 取等级索引; "
        "若返回 -1 (无等级数据, 如魔法/陷阱) 则直接返回 0. "
        "否则调用 setup_line_buf_pos_and_font (FUN_080f0bb4) 以 x=0xe/y=2 初始化行缓冲区, "
        "再调用 render_card_level_text_to_buf (FUN_0801d830) 渲染等级文字/星图到缓冲区, "
        "最后 commit_line_buffer_to_sprite_vram 写入 VRAM (目标地址 DAT_0801d994). "
        "indeg=1, 唯一 caller card_image_decode_wrapper."),
    ("FUN_080ef2cc", "resolve_card_type_icon_ptr",
        "按卡片索引 (r0, u16) 从 card_stats_table 读取卡种字段 (偏移 0xb*idx+0x6, halfword), "
        "先检查 card_index 是否超出总卡数上限 [0x095b7cca]; 超出则返回默认图标指针 (0x0984cfec). "
        "在范围内时: 字段值 0x16 -> 返回 0x0984cfac (魔法?), 0x17 -> 返回 0x0984cfcc (陷阱?), "
        "其余: 查辅助索引表 (0x09e4f1c4, 步长 (card_type_subidx+8)*2) 取子类型值 1/2/3/other, "
        "分别对应返回 0x0984cf4c / 0x0984cf6c / 0x0984cf8c / 0x0984cf2c (各类型图标 ROM 指针). "
        "被 card_image_decode_wrapper 和 FUN_080c05b4 调用, 为卡片信息页类型图标提供 sprite 源地址."),
    ("FUN_080edf00", "upload_tile_and_palette_from_struct",
        "将一个复合数据结构中的 tile 图像数据和调色板数据分两次通过 copy_bytes_by_halfword "
        "分别上传到 OBJ VRAM (0x06004000+) 和调色板 RAM (0x05000000+). "
        "r0=tile_index (用于调色板 RAM 写偏移: tile_index*2 + 0x05000000; u16 截断存入 r4), "
        "r1=src_tile_ref (用于 VRAM 写偏移: src_tile_ref*32 + 0x06004000; lsls r1,#16 >> r0,#11 计算), "
        "r2=data_struct 指针, [r2+0]=width halfword, r6=r2+width*2+8 为调色板子结构. "
        "被两个 bg/vram/palette 相关 caller 调用, 是将字体/图标资源一次性写入 VRAM 和调色板的工具函数. "
        "返回 [r6] (调色板子结构第一个 halfword)."),

    # 2026-05-02: BATCH-15 落地 #2 (topo=77/78/79/82/83/85/86/88/89/90/91/92/93/94/95)
    ("FUN_080edf4c", "write_tile_row_to_vram",
        "被 load_pack_tile_and_map_to_vram (FUN_080ee010) 和 FUN_08023b6c (duel_field) 调用. "
        "以 r3 指向的 tile 结构体为数据源, 按行迭代将 tile 数据写入 VRAM 目标地址 (0x06000800 区域). "
        "每次迭代从源结构体读 2 个 u16 (tile_index/attr), 计算目标行偏移后以 strh 写入 VRAM. "
        "副作用: 写入 [VRAM 0x06000800+按行偏移] 若干 halfword."),
    ("FUN_080ee010", "load_pack_tile_and_map_to_vram",
        "scene_pack 场景的 VRAM tile/palette/map 加载入口. 接收 tile_slot(r0), palette_index(r1), "
        "struct_ptr(r2) 三个参数, 先调用 upload_tile_and_palette_from_struct 完成 tile 图形数据和调色板上传, "
        "再调用 write_tile_row_to_vram (FUN_080edf4c) 将 tile map 数据写入 BG VRAM. "
        "被 card_image_decode_wrapper/FUN_08023b6c/FUN_0802b590 等多个场景初始化函数调用, "
        "是 pack/卡图 BG tile 加载的二合一封装."),
    ("FUN_080ef3bc", "check_card_atk_in_valid_range",
        "被 card_image_decode_wrapper (0x0801d998) 和 FUN_080c0180 (card_stats/font_jp) 调用. "
        "接收卡片索引 (r0, u16 截断), 以步长 0x16 在 card_stats_table 中定位该卡行, "
        "读取第一个 halfword 字段 (ATK 值), 与 7 个阈值逐一比较, "
        "判断 ATK 是否落在某个有效/特殊区间内. "
        "返回 1 (有效) 或 0 (无效/超限). 用于过滤需要特殊处理的高 ATK 卡片."),
    ("FUN_0801dfa0", "tick_scroll_frame_and_update_pos",
        "被 FUN_0801e714 (card_info 场景主循环) 唯一调用, 是卡片信息场景的逐帧滚动位置更新函数. "
        "从 EWRAM 结构体 0x0201afb0 读取字段 [+0x14] (帧计数器), 若超过 0xe8=232 "
        "则将帧计数器继续递增并以帧数计算滚动偏移量, 写入 [+0x18] (像素 Y 偏移) 和 [+0x1c] (子计数器); "
        "若帧计数器未超阈值则清零并停止滚动. "
        "最终写 VRAM 0x03000240 (gFrameCounter 偏移处) 的对应字段以同步 HW 位置."),
    ("FUN_080f0cc0", "setup_line_buf_with_font_and_align",
        "font_jp 模块高频工具函数 (indeg=32). 先调用 setup_line_buf_pos_and_font 完成基础行缓冲区位置和字体设置, "
        "再写入 EWRAM 0x02006ed0 结构体中的两个字节字段: "
        "[+0x15] 的 bit1 根据 r2 (align_flag) 决定左/右对齐; "
        "[+0x14] 的 bits[7:2] 根据 r3 (color_index & 0x1f) 设置文字颜色索引. "
        "被 render_card_description_text/play_ui_effect_37 等多个文字渲染入口调用, 是行对齐+颜色二合一配置函数."),
    ("FUN_080ef488", "resolve_card_flag_table_ptr",
        "仅被 FUN_080ef4bc (scene_card_info) 调用. 接收卡片索引 (r0, u16 截断), "
        "与常量 FIELD_card_flag_table_idx=0x0fa6=4006 比较: "
        "若 <= FIELD_card_flag_table_idx 则返回 0; "
        "若在 PTR_card_flag_table 所指扩展表范围内, "
        "则计算 base-relative 偏移 (card_index - 0x0fa7 得扩展区行号) 并返回指向 ROM 卡片标志表的指针; "
        "否则返回 0."),
    ("FUN_080ef4bc", "test_card_flag_bit",
        "scene_card_info 场景中用于检测特定卡片是否设有某标志位的工具函数. "
        "接收卡片索引 (r0) 和标志位编号 (r1, 0..0x1f), "
        "先调用 resolve_card_flag_table_ptr 获取指向该卡片 ROM 标志表行的指针; "
        "若指针为 0 或 r1 超过 0x1f 则返回 0. "
        "否则以 r1>>4 作行内 u16 偏移 (每 16 bit 一组), r1 & 0xf 作位索引, "
        "读取 flag halfword 并测试目标 bit. 返回 1 表示标志位置位, 0 表示未置位. "
        "被 card_info_page_finalize 和 FUN_08104130/FUN_0810a52c (card_stats) 调用."),
    ("FUN_080f55d4", "disable_blend_and_clear_step",
        "blend+frame_counter 工具族的清除变体 (indeg=26). "
        "清除 gFrameCounter (0x03000240) byte 中的 bit6 (blend_active 标志位), "
        "然后将 BLDCNT (0x04000050) 和 BLDY (0x04000054) 均写 0, 彻底禁用 GBA 混合效果. "
        "被 FUN_080f58b8 在 blend_step 归零时调用, "
        "也被 play_ui_effect_3b/play_ui_effect_30 等特效函数直接调用以重置混合状态."),
    ("FUN_080f58b8", "tick_blend_step_by_delta",
        "blend+frame_counter 工具族的递减变体 (indeg=17). "
        "从 gFrameCounter byte (gPrng+0x200 = 0x03000240) 提取 bits[5:0] (当前 blend_step, 0..63), "
        "减去入参 r0 (delta). 若结果 > 0 则将新 blend_step 写回 gFrameCounter 并将 BLDY (0x04000054) 设为新值; "
        "若 blend_step 递减至 <= 0 则调用 disable_blend_and_clear_step 彻底关闭混合, 返回 1. "
        "返回 0 表示混合仍在进行."),
    ("FUN_0801e328", "tick_blend_fadeout_and_set_dispcnt",
        "被 FUN_0801e714 (card_info 场景主循环) 唯一调用. "
        "先向 DISPCNT (0x04000000) 写入 0x1f00|当前值 (置位 bits[12:8] = BG0-BG3+OBJ 显示使能位), "
        "然后以 delta=4 调用 tick_blend_step_by_delta 递减 blend_step. "
        "实质是卡片信息场景每帧的混合淡出+显示模式锁定组合. "
        "返回 tick_blend_step_by_delta 的返回值 (1=淡出完成, 0=进行中)."),
    ("FUN_080f5840", "start_blend_fadein_with_target",
        "blend+frame_counter 工具族的启动/递增变体 (indeg=21). "
        "先写 BLDCNT (0x04000050) = 0x3fff (bits[13:0] 全置 1: 所有 BG 层作为 blend source 1+2), "
        "然后从 gFrameCounter bits[5:0] 读取当前 blend_step, 将 r0 (target_step) 加上 blend_step, "
        "& 0x3f 夹紧, 若结果 <= BLDY_NEAR_MAX=0x1e 则写回; "
        "若 > BLDY_NEAR_MAX 则夹紧到 BLDY_MAX=0x1f. "
        "若新 blend_step 超过 BLDY_NEAR_MAX 返回 1 (达到目标), 否则返回 0 (仍在过渡). "
        "与 tick_blend_step_by_delta 互为反向."),
    ("FUN_0801e344", "tick_blend_fadein_and_poll_done",
        "被 FUN_0801e714 (card_info 场景) 和 FUN_080fa3a8 调用. "
        "以 target_step=4 调用 start_blend_fadein_with_target 递增 blend_step; "
        "若返回 0 (仍在过渡) 则将返回值继续传递为 0; "
        "若返回 1 (混合完成) 则读 DISPCNT (0x04000000), "
        "与 DISPCNT_PRESERVE_MASK=0xe0ff 做 AND (保留 bits[7:0]+bits[15:13], 清除 bits[12:8] = BG0-BG3+OBJ 使能位), "
        "写回 DISPCNT 关闭高位显示标志, 并返回 1. "
        "实质是 blend fade-in 的每帧驱动函数, 完成时自动清理 DISPCNT."),
    ("FUN_0810d150", "init_sprite_entry_by_id",
        "IWRAM sprite 管理结构体 (0x030050cc) 的 entry 初始化函数 (indeg=10). "
        "接收 sprite/entity ID (r0). 若 r0 bit15 置位则先在结构体偏移 0x89*4=0x224 处的 0x28-byte entry 数组中"
        "线性搜索 [+0x1f] bit7=1 且 [+0xe] signed==r0 的已有 entry; "
        "若找到则复用, 否则在固定槽位写入初始化数据: "
        "halfword[0xda*4]:=r0 (entity_id), byte[0x387]:=0x10 (sprite_type), "
        "halfword[0x36e/0x370/0x372/0x37a]:=0, halfword[0xde*4]:=0xffff, halfword[0xdf*4]:=0x3f3f. "
        "被 sync_state_and_init_sprite (FUN_080f9ab4, indeg=77) 驱动, 服务于卡片/场景对象的 OBJ/sprite 状态初始化."),
    ("FUN_080f9ab4", "sync_state_and_init_sprite",
        "高频工具函数 (indeg=77), 负责监测 IWRAM 状态变量并在变化时触发 sprite 初始化. "
        "读取 gPrng+0x20c (0x0300024c, 旧状态快照 halfword) 与 gPrng+0x218 (0x03000258, 当前状态 halfword), "
        "若两者相同则直接返回 (无变化); "
        "若不同则将 0x0300024c 的值同步到 0x03000258, 再以入参 r0 (callback_data) 调用 init_sprite_entry_by_id. "
        "被 banlist/settings/card_info 等多个模块在 UI 状态切换时调用, 实质是状态脏标记+sprite 重建触发器."),
    ("FUN_0801e36c", "update_card_info_page_state",
        "card_info 场景的每帧状态更新函数, 被 FUN_0801e714 (card_info 场景主循环) 唯一调用. "
        "共执行四步逻辑: "
        "(1) 读 IWRAM gPrng+0x148 (0x03000188) bits[1:0], 若非零则调用 sync_state_and_init_sprite(1) 触发 sprite 初始化; "
        "(2) 读 [0x0201afb0+0x6] 倒计时字段, 若非零则递减并在归零时返回 1; "
        "(3) 根据 gPrng+0x146 的显示标志 bit7/bit6 调整 [struct+0x20] 的滚动偏移值; "
        "(4) 若 gPrng+0x148 bit2 设置且 [0x02006c2c] bits[2:0]==0, 则翻转 [struct+0x0] bit0 并调用 card_info_page_step_03_unknown. "
        "最终返回 0 (继续更新) 或 1 (触发场景切换)."),

    # 2026-05-02: BATCH-15 落地 #3 (topo=98/99/100/101/102/104/105/106/107/108/109/110/112/113/114)
    ("FUN_080f6450", "write_oam_entry_with_tile_inc",
        "OAM write helper (indeg=16) for card_stats render path. "
        "r0 low16=sprite_slot, high16=oam_y; r1=tile_y_offset; r2=x_coord (9-bit); r3=attr2 base. "
        "Locates entry in gPrng sprite table (offset 0x1bc), writes attr0/attr1/attr2 halfwords, "
        "then increments tile count byte. Skips write if tile_y_offset==0x80 (invalid slot). "
        "Variant of write_oam_entry_from_packed_args with different arg packing."),
    ("FUN_080f616c", "write_oam_entry_from_packed_args",
        "High-frequency OAM write primitive (indeg=83), called by card_stats/font_jp/opp_wins. "
        "r0 low16=x_coord (9-bit), high16=oam_y; r1=tile_index; r2=attr2. "
        "Locates gPrng sprite table entry, writes attr0/attr1/attr2 halfwords, "
        "increments tile count byte. DAT_080f61dc=0xfffffe00 masks attr1 X field. "
        "Same structure as write_oam_entry_with_tile_inc but different arg layout."),
    ("FUN_0801e490", "draw_card_stat_digits_to_oam",
        "Called by render_card_stats_oam_for_current_card (FUN_0801e620). "
        "Reads card_id (r0 low16), looks up card_stats_table row (stride=11 halfwords), "
        "reads ATK (offset+6)/DEF (offset+5)/type (offset+9), then calls "
        "write_oam_entry_from_packed_args to write digit sprites to OAM buffer. "
        "Skips render if ATK not in 1..20 range (Spell/Trap have no ATK). "
        "For type 22 (Quick-Play Trap) with field[9]!=0, renders a second digit group."),
    ("FUN_0801e594", "draw_stat_row_sprites_to_oam",
        "Called by render_card_stats_oam_for_current_card (FUN_0801e620). "
        "r0=row_count (signed; negative values rounded up by +7 before >>3). "
        "Folds row_count by 8 to get column/row indices, then loops writing 4 sprite entries "
        "per row at Y positions 0x70/0x90/0xb0/0xd0 (32px steps) via write_oam_entry_from_packed_args. "
        "Loop terminates when r6 > 0x8f (GBA screen height-1=143)."),
    ("FUN_0801e620", "render_card_stats_oam_for_current_card",
        "Called every frame by tick_card_info_page_by_state (FUN_0801e714). "
        "Reads current card_id from global state struct 0x0201afb0 (+0x0 bits[17:2]) "
        "and row_count (+0x20), then calls draw_card_stat_digits_to_oam and "
        "draw_stat_row_sprites_to_oam to write all card stat sprites to OAM buffer."),
    ("FUN_0801e714", "tick_card_info_page_by_state",
        "card_info page per-frame main loop. Reads state halfword from 0x0201afb0+0x4, "
        "dispatches 4 paths: 0=init (read VCOUNT, call card_info_page_entry), "
        "1/2/3=each calls render_card_stats_oam_for_current_card + tick_scroll_frame_and_update_pos, "
        "then tick_blend_fadeout_and_set_dispcnt / update_card_info_page_state / "
        "tick_blend_fadein_and_poll_done respectively. Increments state each frame; "
        "returns 1 (page exit) when state overflows, restoring VCOUNT."),
    ("FUN_0801e7b8", "get_card_data_format_id",
        "No-arg leaf; returns constant 0x81 (card data format ID / FS entry type tag). "
        "Called by deck/banlist scene callers (card_ids/card_stats/fs tags) as a "
        "format version discriminator. Body: movs r0,#0x81; bx lr."),
    ("FUN_0801e7bc", "lookup_card_entry_by_index",
        "Word-indexed table lookup: computes r0*4 + DAT_0801e7c8 (0x09e58b08) "
        "and returns the 32-bit value at that address. "
        "Standard ROM table fetch primitive used by card_ids/fs callers."),
    ("FUN_0801e7cc", "load_card_fs_entry_to_struct",
        "Called by FUN_08103524 (card_ids/fs). r0=slot_index, r1=fs_file_id. "
        "Computes IWRAM struct offset: 0x0201e2b4 + slot*0x108 (slot*33*8). "
        "Calls fs_load(r1,0), then parses FS data header: reads +0x8 halfword as count1 -> [r4+0x0], "
        "copies count1 halfwords from +0xA -> [r4+0xC], reads next halfword as count2 -> [r4+0x8], "
        "copies count2 halfwords -> [r4+0xCA]. Fills deck card FS data block into IWRAM struct."),
    ("FUN_0804ab4c", "check_card_pair_allowed",
        "Boolean card-pair whitelist checker (indeg=41), called by duel_field scene. "
        "r0=card_id_a, r1=card_id_b. Returns 1 if pair is allowed, 0 otherwise. "
        "Checks: same ID -> 1; ID-tree of known special card IDs "
        "(0x12e5/0xfc9/0xfe4/0x1477/0x1303/0x142d/0x150b/0x182c/0x182a/0x10f4 etc.) "
        "via cmp/beq branches. Used to validate fusion material pairs and special combos."),
    ("FUN_080ee050", "upload_sprite_tiles_and_write_oam",
        "Called by FUN_08105bfc (vram/banlist/deck scene). "
        "r0=x_base, r1=y_base, r2=tile_slot, r3=sprite_frame_desc ptr, [sp+0x30]=packed_extra. "
        "Reads tile_count from r3, calls copy_bytes_by_halfword twice to upload tile data "
        "to OBJ VRAM (0x06000800+tile_slot*32 and 0x06008000 second bank), "
        "then iterates OAM entry list writing attr0/attr1/attr2 via strh. "
        "Returns tile count written (u16)."),
    ("FUN_080ee264", "upload_sprite_tiles_with_palette_blend",
        "Palette-blending variant of upload_sprite_tiles_and_write_oam, same caller FUN_08105bfc. "
        "r0=x_base, r1=y_base, r2=tile_slot, r3=packed_pal (low byte=palette_id), "
        "[sp+0x30]=sprite_frame_desc ptr. "
        "Like upload_sprite_tiles_and_write_oam but adds per-entry palette blend: "
        "checks attr1 palette flag; if set, ORs palette_id<<8 into attr1 before strh write. "
        "Used when sprite rendering requires runtime palette index adjustment."),
    ("FUN_080f0cf8", "setup_line_buf_font_align_and_tile_fields",
        "Called by setup_line_buf_font_with_char_index (FUN_080f0d8c). "
        "Wraps setup_line_buf_with_font_and_align (r0=font_ptr, r1=line_buf_ptr, align=1, line_type=2), "
        "then writes tile coordinate fields to IWRAM line-buf state 0x02006ed0: "
        "[+0xA] bits[9:0] := r2 & 0x3ff (tile_x), "
        "[+0xB] bits[7:4] := (r3 & 0xf)<<4 (color nibble), "
        "[+0xC] bits[5:0] := (r3>>16) & 0x3f (tile_y)."),
    ("FUN_080f0d8c", "setup_line_buf_font_with_char_index",
        "Called by FUN_08107198 (banlist/card_frame/font_jp). "
        "Wraps setup_line_buf_font_align_and_tile_fields (r0-r3 passthrough), "
        "then reads [sp+0xC] (5th arg) as char_index (5-bit), writes "
        "[0x02006ed0+0x14] bits[6:1] := (char_index & 0x1f)<<1 (char slot / tile index field). "
        "Completes full line-buf state initialization for font_jp rendering."),
    ("FUN_080f506c", "append_text_to_buf_end",
        "String append utility (indeg=10), called by scene_pack/duel_field/result_screen. "
        "r0=dst_str (null-terminated), r1=src_str. Scans r0 to find trailing null, "
        "then copies r1 byte-by-byte to that position, appending a null terminator. "
        "Equivalent to strcat(r0,r1) with no bounds check."),

    # 2026-05-02: BATCH-15 落地 #4 (topo=115/116/117/118/119/121/122/123/125/126/127/128/129/130/131)
    ("FUN_080f508c", "format_decimal_halfword_to_buf",
        "format_decimal_halfword_to_buf: r1 (decimal int) -> up to 10 halfword-encoded digits "
        "(magic base 0x4f82, each digit: (digit+0x4f)<<8 | 0x82) in stack frame, "
        "then append_text_to_buf_end to r0 dst_buf. "
        "Called by expand_format_decimal_to_buf (0x080f5228/0x080f528c) when gSettings bits[2:0]==0 "
        "(non-JP mode). Clears gSettings+0x16 halfword as side effect."),
    ("FUN_080f50f0", "format_decimal_byte_to_buf",
        "format_decimal_byte_to_buf: r1 (decimal int) -> up to 10 ASCII digit bytes "
        "('0'+digit, 0x30 initial fill) in stack frame, "
        "then append_text_to_buf_end to r0 dst_buf. "
        "Sister of format_decimal_halfword_to_buf (0x080f508c): this outputs ASCII byte digits "
        "(JP/wide-char mode), that outputs halfword-encoded digits (non-JP mode). "
        "Called by expand_format_decimal_to_buf when gSettings bits[2:0]!=0."),
    ("FUN_080f5148", "expand_format_text_to_buf",
        "expand_format_text_to_buf: scans r1 fmt_str byte-by-byte into r0 dst_buf; "
        "on '%%s' (0x25 0x73): writes NUL, calls append_text_to_buf_end twice "
        "(current content, then r2 arg_str). Non-'%%s' bytes copied directly. "
        "Minimal single-%%s printf-like expander used by scene_pack/card_name/font_jp modules "
        "to embed card names into display templates."),
    ("FUN_080f5228", "expand_format_decimal_to_buf",
        "expand_format_decimal_to_buf: scans r1 fmt_str; on '%%d' (0x25 0x64): "
        "reads gSettings byte bits[2:0] to select encoding path -- "
        "0: format_decimal_halfword_to_buf (0x080f508c); non-0: format_decimal_byte_to_buf (0x080f50f0). "
        "Appends remaining fmt via append_text_to_buf_end. Non-'%%d' bytes copied directly. "
        "Implements locale-aware '%%d' expansion; called by result_screen/duel_field/vram modules."),
    ("FUN_080f57d0", "apply_blend_fadeout_flat",
        "apply_blend_fadeout_flat: no args. "
        "Reads gPrng+0x200 (0x03000240, gFrameCounter byte), clears bit6 (blend_active), "
        "sets bits[4:0]=0x1f (BLDY_MAX), writes back. "
        "Then sets BLDCNT (0x04000050)=0x3fff (all BG layers as blend source), "
        "BLDY (0x04000054)=0x1f (max fade-out). "
        "Immediately forces screen to maximum dark blend with no transition. "
        "Called by 10+ duel_field/pack/display/palette scene init or clear-screen callers."),
    ("FUN_080f5d1c", "bsearch_index_by_callback",
        "bsearch_index_by_callback: binary search on sorted array of r2 elements, stride r3. "
        "r0=base_ptr (->r8), r1=key (->r9), [sp+0x28]=compare callback (->r10, called via bx r10). "
        "Callback returns 0=hit, neg=go-low, pos=go-high. "
        "On hit: writes found_index+1 to IWRAM 0x030001b6 halfword, returns index+1. "
        "On miss: writes r4 to gPrng+0x17a, returns original count. "
        "Used by card_stats callers to locate entries in sorted tables."),
    ("FUN_080f61e4", "write_obj_attr_packed",
        "write_obj_attr_packed: writes one sprite entry (attr0/attr1/attr2) to "
        "OBJ attribute shadow buffer at gPrng+0x1bc (0x030001fc). "
        "r0 low16=attr0 (Y/shape/mode), r0 high16=attr_extra (X/size), r1=attr1_x, r2=attr2_tile. "
        "Applies 0xfffffe00 mask to attr0, writes 3 halfwords to 8-byte aligned slot, "
        "increments use-count byte at [entry+0x400]. Skips if count==0x80 (slot full). "
        "Called by batch/grid/conditional OBJ write paths; sibling of write_obj_attr_with_priority."),
    ("FUN_080f6578", "write_obj_attr_with_priority",
        "write_obj_attr_with_priority: priority/affine variant of write_obj_attr_packed (0x080f61e4). "
        "Same OBJ shadow buffer at gPrng+0x1bc; same 3-halfword write structure. "
        "Key difference: attr0 synthesis ORs 0x2400 (bit10=double-size/R/S, bit13=affine flag). "
        "r0 low16=attr0, r0 high16=attr_extra, r1=attr1_x, r2=attr2_tile. "
        "Increments use-count byte at [entry+0x400]. "
        "Unique caller: FUN_08107b90 (OBJ mode dispatch, priority/affine path)."),
    ("FUN_0810cf10", "init_sound_channel_entry",
        "init_sound_channel_entry: initializes key fields of a sound channel entry "
        "in IWRAM management struct at 0x030050cc. "
        "r0=channel_id (written to [base+0x366] halfword), r1=channel_flag (written to [base+0x386]). "
        "Also clears: [base+0x38b]=0 (status), [base+0x10]=0 (counter), "
        "[base+0x39c]=0xff (end_marker), [base+0x374]=r0+1 (next_id halfword). "
        "Called by reset_sound_channel_entry (r1=0) and FUN_0810cf60 (r1 from caller)."),
    ("FUN_0810cf54", "reset_sound_channel_entry",
        "reset_sound_channel_entry: calls init_sound_channel_entry (0x0810cf10) with r1=0, "
        "clearing channel_flag and resetting all other fields of the channel entry "
        "in IWRAM struct at 0x030050cc. "
        "'Clear/reset' wrapper variant of init_sound_channel_entry. "
        "Called by set_channel_if_changed (FUN_080f9adc) and 5 other callers "
        "on scene exit or sound stop."),
    ("FUN_080f9adc", "set_channel_if_changed",
        "set_channel_if_changed: reads EWRAM 0x0200af10 halfword (active channel_id), "
        "compares with r0; if equal returns immediately (lazy update, no-op). "
        "If different: writes r0 to [0x0200af10], calls reset_sound_channel_entry (0x0810cf54). "
        "Standard lazy-update pattern. indeg=15, called by demo_shuen_state_machine, "
        "banner_anim_state_machine, and display/palette/demo/fs scene functions."),
    ("FUN_080f9bc4", "copy_puzzle_seed_to_wram",
        "copy_puzzle_seed_to_wram: copies 8 bytes from ROM 0x09e4f568 (puzzle seed data) "
        "to EWRAM 0x02000000 via fixed-count ldrb/strb loop (r1=7, countdown to 0). "
        "No args, no return value. "
        "Called by init_puzzle_wram_and_checksum (0x080f9c68) during puzzle state init "
        "to load the ROM-stored initial seed into working memory."),
    ("FUN_080f9c08", "compute_puzzle_checksum",
        "compute_puzzle_checksum: computes 16-bit rolling checksum over EWRAM 0x02000000, "
        "length 0x6ecc halfwords. Init value 0x5847 (magic). Per-halfword: "
        "acc = (acc + halfword) << 16, XOR 0xffff0000, >> 16. "
        "No args; returns r0=u16 checksum. No external writes (pure compute). "
        "Called by init_puzzle_wram_and_checksum (stores result) and FUN_080f9c40 (verifies)."),
    ("FUN_080f9c68", "init_puzzle_wram_and_checksum",
        "init_puzzle_wram_and_checksum: scene_duel_puzzle EWRAM init entry. "
        "Calls copy_puzzle_seed_to_wram (0x080f9bc4) to load ROM seed to EWRAM 0x02000000, "
        "then compute_puzzle_checksum (0x080f9c08) for the data block, "
        "then writes checksum to EWRAM [0x02000000+0x6ecc] halfword. "
        "Called by 12 callers covering scene_duel_puzzle/money/pack on init or reward update nodes."),
    ("FUN_0810e460", "copy_bytes_with_waitcnt",
        "copy_bytes_with_waitcnt: configures WAITCNT (0x04000204) bits[1:0]:=3 "
        "(SRAM 8 wait cycles) before byte-by-byte copy of r2 bytes from r0 (src) to r1 (dst). "
        "r2==-1 skips copy. SRAM requires 8-bit-only access; WAITCNT setup ensures correct timing. "
        "Called 3 times by FUN_0810e588 (scene_duel_puzzle) for SRAM save-data write."),

    # 2026-05-03: BATCH-15 落地 #5 (topo=133/134/135/136/137/138/139/141/142/143/144/145/146/147/148)
    ("FUN_0810e588", "copy_with_waitcnt_and_verify_loop",
        "在 duel_puzzle 场景初始化路径下被 FUN_080f9c88 调用, 以固定源地址 r0 (EWRAM 0x02000000) "
        "向目标 r1 (SRAM 0x0E000000) 拷贝 r2 (0x6ed0) 字节, 拷贝完成后调用 FUN_0810e5d4 进行校验; "
        "若校验失败则重试, 最多循环 3 次 (r7 从 0 到 2). 副作用: 写入 r1 目标内存区域, "
        "并通过 [0x02029ea4] 读取某计数/校验辅助状态. 拷贝通过 copy_bytes_with_waitcnt 完成, "
        "保证等待总线就绪."),
    ("FUN_080f9c88", "init_puzzle_wram_then_copy",
        "duel_puzzle 场景进入时的轻量封装函数. 依次调用 init_puzzle_wram_and_checksum 完成谜题 WRAM 初始化, "
        "再以固定源 0x02000000 + 长度 0x6ed0 调用 copy_with_waitcnt_and_verify_loop "
        "将谜题数据拷贝到目标区域. 被 enter_duel_puzzle_page / enter_limited_duel_page / "
        "enter_theme_duel_page 等多个场景入口调用, 是 duel_puzzle 所有变体共享的 WRAM 预备序列."),
    ("FUN_08103280", "read_card_list_field_by_row_col",
        "card_list 场景双参字段读取函数, 与 read_card_list_field_by_index (0x08103244) "
        "为同一翻译单元内的兄弟对. 以 r0 (行) 和 r1 (列/偏移) 计算二维索引 (r0*7+r1)*2, "
        "从 IWRAM 0x0202a4d0 + 偏移 0xa9*4=0x2a4 处读取有符号半字. "
        "FUN_081014fc 在调用 read_card_list_field_by_index 后立即调用本函数, "
        "传入行计数 r4+1 和列参数, 说明用于访问 card_list 的二维布局."),
    ("FUN_08103244", "read_card_list_field_by_index",
        "card_list 场景通用字段读取函数. 以 r0 为下标 (halfword 步长 *2), "
        "从 IWRAM 0x0202a4d0 + 偏移 0xa7*4=0x29c 处读取一个有符号半字并返回. "
        "被 FUN_081014fc (vram/scene_card_list) 和 FUN_081021dc (card_ids/card_stats) "
        "等多个 card_list 子系统函数调用, 用于查询卡片列表内某一索引对应的字段值 "
        "(确切字段语义待 runtime 确认)."),
    ("FUN_08109848", "resolve_card_gfx_row_by_type",
        "根据卡片类型编号 (r0, 有效值 2-12, 内部先减 2) 从 ROM 跳转表选出对应图形数据块的起始指针 (r1) "
        "和条目数 (r3), 然后在该块中线性搜索与 r1 (传入值 = r4) 匹配的条目, "
        "返回该条目偏移 +2 处的 s16 值 (图形行索引). 若超出范围或未找到则返回 -1. "
        "各 case 数据位于 ROM 0x09e60fc0-0x09e610d4, "
        "是 card_list 场景显示时 per-type 图形行查找的核心函数."),
    ("FUN_08109788", "resolve_card_frame_palette_by_type",
        "根据卡片类型编号 (r0, 范围 0-12) 从 ROM 查找对应卡框调色板数据指针, "
        "合并 r1 (子偏移, 移位 8 位) 后返回. "
        "各 case 加载 ROM 地址 0x09e265b4-0x09e2ddb4 段内的调色板数据指针 (per-type 调色板块). "
        "返回值 = palette_ptr + (r3<<8), 即调色板基地址加行偏移; 若 r2==0 则返回 0 (无效类型). "
        "在 FUN_081014fc 中由 FUN_08109848 的返回值作为 r1 传入, 两者构成 type->palette 的两级分派."),
    ("FUN_081014fc", "setup_card_list_tile_rows",
        "card_list 场景 VRAM tile 初始化函数. 从 IWRAM 0x0202a4d0 (r7) 读取当前选中卡片字段, "
        "调用 read_card_list_field_by_index / resolve_card_gfx_row_by_type / "
        "resolve_card_frame_palette_by_type 构成三级查表链, "
        "再以 tile_2d_row_copy 将卡框 palette 数据拷贝到 VRAM 0x06010880 (r6). "
        "外层循环 r4=0..5 执行 6 次, 每次偏移 VRAM 目标地址 r4*128 字节, 覆盖 6 行 tile 数据. "
        "由 card_list_screen_init 和 FUN_080fffc4 调用, 是卡片列表界面卡框 tile 批量写入的核心."),
    ("FUN_08100980", "render_card_name_label",
        "card_list / card_stats 场景中渲染单张卡片名称的核心函数. r0 为卡片 ID, r1 为渲染模式标志 "
        "(bit1 为 0 = 走 resolve_card_gfx_pointer_by_type 路径, "
        "bit1 为 1 = 走 select_charset_then_load_name 路径; "
        "caller FUN_08100968 通过 lsls/lsrs 提取 [0x0202a4d0+0x16] 的 bit1 后传入). "
        "名称加载后若长度 <= 26 则直接 strcpy 到栈缓冲区, 否则截断为 26 字节并补 NUL. "
        "随后调用 text_render_wrapper 渲染名称 (含阴影/双行), "
        "并更新 [0x02006ed0+8] 的字体标志位 (bit1 控制当前字体 charset). "
        "副作用: 向 OBJ VRAM 写入字符 tile (通过 text_render_wrapper)."),
    ("FUN_08100968", "dispatch_render_card_name_with_flags",
        "render_card_name_label (0x08100980) 的一层轻量封装. "
        "从 IWRAM 0x0202a4d0 (card_list 状态基地址) 偏移 0x16 处读取一个字节, "
        "取 bit1 (lsls/lsrs 提取) 作为 r1 渲染标志, "
        "连同 r0 (card_id, 由外部 FUN_08100238 传入) 一起调用 render_card_name_label. "
        "目的是将 IWRAM 中的 charset/display 状态标志透明地注入渲染调用, 调用方无需感知标志字段位置."),
    ("FUN_08102494", "search_card_list_subtable_by_key",
        "根据模式参数 r0 (0-3) 从 IWRAM 0x0202a4d0 中选取对应子表偏移 (0x140c/0x160c/0x180c/0x1a0c), "
        "读取该子表的条目数 (halfword), 若非零则以 r1 的低 12 位 (r1 & 0xfff, card_id) 为关键字 "
        "调用 bsearch_index_by_callback 在子表中二分查找匹配条目, 返回命中条目的高 4 bit (lsrs 0x4). "
        "若子表为空或未命中则返回 0. 被 FUN_08100238 (vram/card_stats/font_jp) 调用, "
        "用于 card_list 场景卡片信息显示前的分类子表定位."),
    ("FUN_08102914", "read_card_list_type_hi_nibble",
        "从 IWRAM 0x02000006 + r0*2 处读取一个字节, 右移 4 位取高 nibble 后返回. r0 为下标参数. "
        "被 FUN_08100238 / FUN_080ff56c / FUN_080ffe38 三个 card_list 相关函数调用, "
        "用于提取 card_list IWRAM 某表中每个条目字节的类型高位编码. 函数体为纯只读叶子, 4 条指令."),
    ("FUN_08100238", "render_card_list_entry_row",
        "card_list 场景每行卡片信息的完整渲染函数. "
        "从 IWRAM 0x0202f3c0 (r0 at entry via [sp+0]) 读取当前行配置, "
        "以 [base+2] 的 bit 位掩码判断哪些列启用, 对每列执行: "
        "zero_fill_by_halfword 清 VRAM Sprite 行, commit_line_buffer_to_sprite_vram 写字符, "
        "调用 dispatch_render_card_name_with_flags (0x08100968) 渲染卡名, "
        "调用 search_card_list_subtable_by_key (0x08102494) 查子表, "
        "调用 read_card_list_type_hi_nibble (0x08102914) 读类型高位. "
        "外层以 r4 迭代 4 个 card_list 列 (0-3), 内层对每列最多 9 个条目 (r7=0-8) 循环. "
        "由 card_list_screen_init 和 FUN_080fffc4 调用."),
    ("FUN_08100f38", "render_game_text_centered_label",
        "card_list 界面字符串标签居中渲染函数. 从 IWRAM 0x0202a4d0 (r6) 读取当前状态, "
        "检查 [r6+0] 是否 == 3; 若是则配置字体 charset (通过 PTR_font_jp_base_table), "
        "以 [r6+4] 的偏移量加常数 0xd9*8=0x6c8 调用 game_str_id_to_row 获取字符串行号, "
        "再从 game_str_pointer_table 定位目标字符串, "
        "调用 strlen 测量宽度后计算居中起始 X 坐标 (0x60 - len*12/4 = 居中偏移, 最小 1). "
        "随后以 text_render_wrapper 连续渲染 3 遍该字符串 (含阴影偏移 r0/r0+1 两行), "
        "最后 zero_fill_by_halfword+commit_line_buffer_to_sprite_vram 完成 sprite 写入. "
        "由 card_list_screen_init 和 FUN_080fe308 调用."),
    ("FUN_0810133c", "setup_card_list_bg2_tilemap",
        "card_list 场景 BG2 tilemap 初始化函数. "
        "检查 IWRAM 0x0202a4d0+0x16 的 bit0 启用标志; "
        "若置位则先对 VRAM 0x0600f000 (r8 由 DAT_081013e0 = 0x0600f000 加载) "
        "调用 zero_fill_by_halfword 清零 0x800 halfword (0x1000 字节), "
        "再以双重循环 (外层 r4=0..3 共 4 列, 内层 r3=0..9 共 10 行) "
        "计算 tilemap 序号并 strh 写入目标地址, 构建 4x10 卡片列表 tilemap. "
        "若 bit0 未置位则走另一路径 (LAB_081013ec), 同样清零 0x800 halfword 后写 4x4 tilemap. "
        "函数末尾将 BG2HOFS 设为 0xfffc 或 0xffd0 (含列方向偏移). "
        "由 card_list_screen_init / FUN_080fe308 / FUN_080fffc4 调用."),
    ("FUN_080ff9c0", "reset_card_list_scroll_state",
        "card_list 场景滚动/选择状态重置函数. "
        "将 IWRAM 0x0202f3c0 结构体中偏移 0xe-0x1a 共 7 个 halfword 字段清零, "
        "唯独将偏移 0x12 设为 0xffff (无效/哨兵值). 随后返回 1. "
        "被 card_list_screen_init 在初始化时调用一次, "
        "也被 FUN_080ff4f0 / FUN_080ff980 / FUN_080ffaf8 (均为 scene_card_list) "
        "在导航操作后调用, 说明这些字段记录当前滚动位置/光标/帧计数等状态, "
        "每次切换显示模式时需整体归零并将某个字段置 sentinel."),

    # 2026-05-03: BATCH-15 落地 #6 (topo=149/151/152/153/154/155/156/157/158/159/160/161/163/164/165)
    ("FUN_081016c0", "load_card_mini_frame_tiles_by_type",
        "card_list 界面初始化时调用, 根据 IWRAM 0x0202a4d0[+0] (card_type, int16) 分 3 路分支: "
        "==1 走小卡框路径(0x06016a80, 0x09e25934), ==3 走大卡框路径(0x06016a80, 0x09e25c34), 其余直接返回. "
        "两路均循环 tile_2d_row_copy 将 ROM 卡框 tile 拷贝到 VRAM OBJ 区, "
        "并以 copy_bytes_by_halfword 将对应调色板写入 PAL_OBJ(0x05000360). "
        "由 card_list_screen_init(0x080fdef4) 唯一调用."),
    ("FUN_08100048", "resolve_card_scroll_offset_by_mode",
        "card_list 界面多处调用, 以 IWRAM 0x0202a4d0[+4] (display_mode, int16, [0..3]) "
        "和 0x0202f3c0 (scroll_state) 为输入, 按 mode 分支查找或计算当前卡片列表的滚动偏移量并写回 "
        "0x0202f3c0[+0x74]. mode==0 直接取固定基础偏移 0x4acc; "
        "mode==1 按卡片 foil bit (ldrb [r2+0x16] & 1) 选 4ede/4ed6, "
        "再用 __divsi3 计算水平像素偏移并写入 +0x7a; mode==2/3 同理选不同 offset 表. "
        "最终将解析到的滚动目标指针存入 [r4+0x74], 像素偏移写入 [r4+0x7a]."),
    ("FUN_081044ac", "clear_card_list_slot_flag_by_index",
        "card_list 场景槽位标志清除工具函数. 接收 r0=slot_index ([0..12]), "
        "以 1<<slot_index 计算位掩码, 对 IWRAM 0x0202a4d0[+0x30] (slot_flags 字段) 执行 bics 清除对应位, "
        "并将 0x0202a4d0[+0x32] 置 0 (标记刷新状态). "
        "被 clear_all_card_list_slot_flags 以 r4=0..12 循环调用(批量清除所有槽), "
        "也被 FUN_081078d4 / FUN_081095e8 单次调用."),
    ("FUN_081014e4", "clear_all_card_list_slot_flags",
        "card_list 场景槽位标志批量清零入口. 以 r4=0 到 r4=0xd(13) 为循环变量, "
        "逐一调用 clear_card_list_slot_flag_by_index(r4), 共执行 14 次(索引 0..13). "
        "被 init_card_list_display_and_objs 在场景初始化阶段调用, "
        "也被 FUN_080ff434 / dispatch_card_frame_tile_load_by_type 在刷新/切换时调用. "
        "函数体仅 6 条指令, 是典型的 batch-clear 包装."),
    ("FUN_0810445c", "load_card_frame_tile_row_by_index",
        "card_list 界面卡框 tile 行加载函数. 接收 r0=frame_index ([0..0xd]), "
        "乘以 12(r0*3<<2) 计算 ROM 卡框数据偏移, 从 0x0202a4d0[+0] (card_type, int16) "
        "查表取对应 tile 行数据地址, 调用 tile_2d_row_copy 将 4x4 tile 块写入 VRAM 目标行. "
        "写完后对 0x0202a4d0[+0x30] 置对应位(orrs), 并清零 0x0202a4d0[+0x32] 触发刷新. "
        "由 dispatch_card_frame_tile_load_by_type 按解析后的 frame_index 调用."),
    ("FUN_08101454", "dispatch_card_frame_tile_load_by_type",
        "card_list 界面的卡框 tile 行加载调度器. 读取 IWRAM 0x0202a4d0[+6] (card_frame_type, int16), "
        "先调用 clear_all_card_list_slot_flags 重置所有槽, 再按 type 分支选择 frame_index([0..0xd]) "
        "并调用 load_card_frame_tile_row_by_index. "
        "type==0: 根据 [+0]/[+8] 字段选 index 4/5; type==1: 根据 [+0] 选 3/6; "
        "type==2: 根据 foil bit 选 10/11; type==3: 根据 [+0x12] 选 12/13. "
        "由 card_list_screen_init 及多个场景切换函数调用(indeg=5), 是卡框 tile 重载的统一入口."),
    ("FUN_08101068", "load_card_full_frame_tiles_and_palettes",
        "card_list 界面初始化时由 card_list_screen_init 唯一调用, "
        "将完整的卡框 tile 套件和调色板批量写入 VRAM/PAL. "
        "包含多轮 copy_bytes_by_halfword 和 tile_2d_row_copy 调用: "
        "先从 ROM 0x09e24934 拷贝 0x1c0 字节 tile 数据到 VRAM OBJ 0x0600c040, "
        "再从多个 ROM 源分别拷贝 tile 行到 0x0600c200/0x06016800/0x06016c00/0x06017000/0x06017400. "
        "最后将 card_mini_frame_pal_128/pal_144/pal_main 写入 PAL_OBJ 0x05000140/0x05000300/0x05000320/0x05000200."),
    ("FUN_08100b70", "render_card_list_visible_slots",
        "card_list 界面可见槽位 tile 渲染函数. 读取 0x0202f3c0[+0](slot_vis_flags, uint16), "
        "若 bit4(0x10) 置位则先调用 zero_fill_by_halfword 清零 VRAM OBJ 0x0600e000(0x800 字节). "
        "随后以 r3=0..5 循环, 每次从 slot_vis_flags 右移 r3 位取 bit0 判断槽是否可见; "
        "若可见则进一步检查 0x0202a4d0[+0x16] & 1 (foil bit). "
        "可见槽按 display_mode 分别从 4 个 ROM tile 表中取偏移, "
        "加 VRAM 基址后将 tile 数据以 strh 写入 VRAM OBJ."),
    ("FUN_0810a0e8", "format_decimal_with_sign_pos",
        "settings/card_list 数值渲染工具函数, 正数路径包装. "
        "接收目标缓冲区指针(r0)和正整数值(r1), 将 r1 移入 r2 后以固定格式串 (ROM 0x09e56cf4) "
        "调用 expand_format_decimal_to_buf, 格式化出 \"+N\" 形式的带正号十进制字符串并写入 r0 缓冲区. "
        "由 render_deck_count_diff_label 和 FUN_08107198 在 r5>0 分支调用, "
        "为 sibling format_decimal_with_sign_neg(0x0810a0fc) 的对偶函数."),
    ("FUN_0810a0fc", "format_decimal_with_sign_neg",
        "settings/card_list 数值渲染工具函数, 负数或无符号绝对值路径包装. "
        "接收目标缓冲区指针(r0)和有符号整数值(r1), 取 r1 的绝对值(bge skip / rsbs r4,r5,0)后 "
        "以十进制逐位分解(循环 __modsi3/__divsi3 /10 提取各位, 最多 15 位). "
        "若原值为负则从 game_str_ja 取负号字形写入 [r1+0]; "
        "最后按倒序将各位数字以 stmia 填入输出缓冲, "
        "与 format_decimal_with_sign_pos 构成正负对."),
    ("FUN_08100d70", "render_deck_count_diff_label",
        "card_list/settings 界面中展示卡组数量差值标签的渲染函数. "
        "读取 IWRAM 0x0202a4d0[+0](mode, uint16), 若不等于 1 则直接退出. "
        "读取 0x0202a4d0[0x1a16] 和 [0x1a1e] 两个 uint16 值相减得差值 r5. "
        "根据 r5==0 查 game_str_id 0x6c1; r5!=0 分支按符号选 "
        "format_decimal_with_sign_pos 或 format_decimal_with_sign_neg 格式化差值. "
        "连续调 text_render_wrapper 三次(含阴影), "
        "最后 zero_fill_by_halfword + commit_line_buffer_to_sprite_vram 写入 sprite VRAM."),
    ("FUN_0810017c", "write_card_list_slot_tiles_to_vram",
        "card_list 界面单槽 OBJ tile 写入函数. 接收 r0=slot_index ([0..N]), "
        "以 r0*24(r0*3<<3) 计算到 ROM 数据表 (0x09e5fda0) 中该槽结构体偏移. "
        "外层循环 r5=0 to [base+0xf]-1 (row_count), 内层循环 r3=0 to [base+0xe]-1 (col_count), "
        "每次以 ldrh 取 tile_id, 加 [base+0x10](tile_base_offset) 再 OR [base+0x14](pal_idx)<<0xc, "
        "用 strh 写入 VRAM OBJ 0x0600f800 目标行列偏移. "
        "循环后以 copy_bytes_by_halfword 追加第二 tile 层."),
    ("FUN_080fe2b4", "reset_card_list_scene_state",
        "card_list 场景状态重置函数. 读取 IWRAM 0x0202a4d0[+0] (mode, int16), "
        "若在有效范围 [0..3] 之外则不写 [+6]; 若为 0/1/3 则将 mode 值写入 [+6](last_mode); "
        "==2 时写 0. 随后无条件将 [+8]/[+a]/[+c]/[+e]/[+10]/[+12] 六个 uint16 字段清零. "
        "由 4 个不同的场景初始化函数调用, 在进入 card_list 界面前统一重置场景状态."),
    ("FUN_080fe2e8", "init_card_list_display_and_objs",
        "card_list 界面显示硬件初始化函数. "
        "调用 clear_all_card_list_slot_flags 批量清零所有槽标志, "
        "再将 DISPCNT(0x04000000) 和 PAL_BG 基址(0x05000000) 均写 0 以关闭显示并清调色板首字, "
        "最后调用 init_scene_obj_list 初始化场景 OBJ 列表. "
        "由 6 个不同场景的过渡/切换函数调用, 是进入 card_list 界面前的硬件准备步骤."),
    ("FUN_080ff418", "return_zero_epilogue_stub",
        "单指令入口点, 仅执行 movs r0,#0 后落入紧邻下方 FUN_080ff41a 的共享 epilogue "
        "(add sp,0x1c / pop 多寄存器 / bx r1). "
        "本质是外层大函数(FUN_080fe308 区域, 0x080ff408 处 b 跳入)的失败/0 返回出口路径. "
        "Ghidra 将其标记为独立函数, 但实际是 FUN_080fe308 内部的 tail-shared early-exit 片段. "
        "由 FUN_080fe308(0x080fe308) 以 b 指令无条件跳入, 无其他 caller."),

    # --- batch7 (2026-05-03): deck slot / card_frame 渲染簇 ---
    ("FUN_080ff41a", "restore_regs_epilogue",
        "该入口点是 FUN_080fe308 大函数内部共享的尾部 epilogue 片段. "
        "调用方通过 b 无条件跳入 (0x080ff41a), 从 r0 已清零 (由紧邻上方的 return_zero_epilogue_stub 负责) "
        "的状态开始执行: 恢复 sp+0x1c, 弹出 r3/r4/r5 及高寄存器别名 "
        "(mov r8,r3; mov r9,r1; mov r10,r2), 再弹出 r4-r7 和 r1, 最后 bx r1 返回. "
        "本质是一段被 Ghidra 独立标记的 shared restore_regs_epilogue 代码片段, 并非独立语义函数."),
    ("FUN_08102538", "count_valid_cards_by_slot_type",
        "在卡组构建场景中被调用, 按 r0 指定的 slot 类型 (0=主卡, 1=融合, 2=魔法/陷阱, 3=仪式等) "
        "遍历 IWRAM 0x0202a4d0 所指向的卡片结构, 调用 check_card_pair_allowed 验证每张候选卡是否可加入该 slot, "
        "统计满足条件的卡片数量并写入 r7 结构的输出区域. "
        "返回 r0=满足条件的计数, 供上层 find_best_slot_for_card 汇总三路结果后判断最优 deck slot."),
    ("FUN_08102620", "find_best_slot_for_card",
        "在卡组构建场景中被 FUN_080fe308 和 FUN_08103100 调用. "
        "函数对 deck 的四种 slot 类型 (r7=0..3) 逐一遍历: 每轮对当前候选卡列表分别调用 "
        "count_valid_cards_by_slot_type 三次 (type 1/2/3), 将结果求和后与该 slot 的卡组上限比较. "
        "若总数超出上限, 则提取该卡的 ATK 等级字段并将该 slot 索引作为候选. "
        "循环结束后返回最优 slot 索引 (r0=找到的 slot_idx), 0 表示未找到或不满足."),
    ("FUN_081044c0", "write_slot_display_coords",
        "在多个 UI 场景 (card_stats 展示, settings 面板, banlist 画面) 中被调用, "
        "负责将显示坐标写入 IWRAM slot 描述符. "
        "函数以 r0 为 slot 索引, 以 4 字节步长偏移到 IWRAM 基址 0x0202a4d0 对应条目, "
        "将 r1 写入偏移 +0x34 (x 坐标或宽度), r2 写入偏移 +0x36 (y 坐标或高度), 返回 r0=1 表示成功."),
    ("FUN_081078f8", "render_jp_text_pair_with_flag",
        "由 render_card_frame_scene (banlist/card_frame/settings 综合渲染函数) 唯一调用, "
        "负责在指定位置渲染一对日文字符串. "
        "函数首先将 IWRAM 0x02006ed0+8 处的状态字节置位 bit1 (标记 'jp 渲染进行中'), "
        "然后以 (r0+1, r1+1) 和宽度 0x104 (0x82<<1) 调用 text_render_wrapper 渲染第一行; "
        "若 r2 非零则对第二次调用的宽度参数减去 7, 再次调用 text_render_wrapper 以 (r0, r1) 渲染第二行内容. "
        "r3 传入字符串指针或格式标识."),
    ("FUN_08107a48", "calc_card_stat_bonus_by_type",
        "由 FUN_0810796c (settings/card_frame 渲染函数) 循环调用, "
        "用于计算特定 slot 位置上指定卡片的能力值加成 (bonus). "
        "函数根据 IWRAM 0x0202f3c0+0x6c2c 中的 lang_flag bit[2:0] 选取两套卡片数据表 "
        "(EN 版: 0x09e606f4; JP 版: 0x09e60894), 然后 switch 卡片类型字段 (偏移 0 处的 halfword, [1..4]): "
        "type3 对应 +(-19) 行偏移, type4 对应 +(-10) 行偏移, type1/2 走默认分支. "
        "r2 和 r3 为两个输出指针 (分别指向调用方栈上的 y_delta 槽和 x_bonus 槽), "
        "将计算出的 y_delta 和 x_bonus 分别写入 *r2/*r3 供调用方合成 OBJ 属性."),
    ("FUN_0810793c", "load_card_mini_frame_tile_and_pal",
        "由 render_card_frame_scene (banlist/card_frame/settings 综合渲染函数) 唯一调用, "
        "负责将卡片迷你外框的 tile 数据和调色板一次性加载到 VRAM/CRAM. "
        "函数调用 tile_2d_row_copy 将 ROM 中 9 行 x 1 列的 tile 数据 (步进=1) 复制到 VRAM 0x06017800; "
        "再调用 copy_bytes_by_halfword 将 32 个 halfword (64 字节) 的 card_mini_frame_pal_144 "
        "调色板写入 CRAM 0x05000320 (BG/OBJ 调色板区). "
        "整体用于切换到迷你框显示时的资源初始化."),
    ("FUN_08107198", "render_card_frame_scene",
        "该函数是 banlist/card_frame/settings 场景的核心渲染入口, "
        "由三个上层函数 (dispatch_card_type_and_render_frame, FUN_081045c4, FUN_081047e8) 调用. "
        "函数首先根据 lang_flag (IWRAM 0x0202f3c0+0x6c2c bits[2:0]) 选择 EN/JP 卡片数据表 "
        "并复制 0x120 字节 tile 数据到 VRAM 0x06009400; "
        "然后对卡片外框网格每个单元格写入 OBJ tile 索引 (VRAM 0x06009800); "
        "再写入 banlist/deck 状态标志对应的 OBJ 属性; "
        "切换调色板 (card_mini_frame_pal_144 至 0x05000160/0x05000166); "
        "调用 select_charset_then_load_name 加载卡片名称; "
        "最后链式调用 load_card_mini_frame_tile_and_pal / render_jp_text_pair_with_flag / "
        "calc_card_stat_bonus_by_type / write_slot_display_coords 完成全帧渲染."),
    ("FUN_080ff824", "dispatch_card_type_and_render_frame",
        "由 FUN_080fe308 (大型 deck/card 场景主函数) 唯一调用. "
        "函数读取 IWRAM 0x0202f3c0 偏移 +6 处的 halfword, 减 1 后作为 switch 索引 ([0..10]): "
        "各 case 将内部枚举值 (0,1,2,3,4,5,0x10,0x11,0x12,0x19,0xf) 写入 r4 (对应卡片展示类型); "
        "再读取 deck_slot [0x0202a4d0+6] 的当前类型值, 置 5, "
        "然后调用 dispatch_card_frame_tile_load_by_type 加载对应帧 tile, "
        "最后调用 render_card_frame_scene 渲染目标 slot. "
        "用于将外部卡片类型 ID 映射为内部枚举再触发帧渲染."),
    ("FUN_0810372c", "copy_deck_slot_card_data",
        "由 init_deck_slot_data (deck slot 总调度函数) 以 r1=1 调用, "
        "负责将指定 deck_type (r0=[0..3]) 对应的卡片数据复制到目标缓冲区. "
        "函数从 IWRAM 0x0202a4d0 选取对应 deck_type 的源区偏移 "
        "(type0: +0x2b9c/+0x1a6c, type1: +0x3ecc/+0x3ccc, type2: +0x44cc/+0x42cc, type3: +0x4acc/+0x48cc), "
        "根据 r1 标志决定使用哪个源指针, "
        "然后调用 copy_bytes_by_halfword 复制 0x200 字节卡片数据; "
        "type0 特殊路径复制 0x1130 字节. "
        "用于在场景切换时刷新 deck slot 数据缓冲区."),
    ("FUN_08103c3c", "apply_card_obj_attr_by_type",
        "由 init_deck_slot_data 和 FUN_08102c6c (均属 card_stats 场景) 调用, "
        "负责将 deck slot 中第 r0 个位置的卡片设置 OBJ 属性. "
        "函数从 IWRAM 0x0202a4d0 偏移 +0xa7*2+r0*2 读取已排序卡片的 card_id (有符号 16 位); "
        "以 1<<card_id 构造 tile 位图并写入 IWRAM 0x0202f3c0+0x7c; "
        "若 card_id 非零且非 7, 则额外 OR 0x8000 (bit15=暗背景标志); "
        "若 card_id 为 0 或 7 则进入扩展标志分支 OR 0x800000. 返回 r0=1."),
    ("FUN_08104130", "check_card_valid_for_deck_slot",
        "由 filter_deck_slot_candidates 和 FUN_08102c6c (均属 card_stats 场景) 调用, "
        "对候选卡片验证是否满足当前 deck slot 的限制条件. "
        "函数读取 IWRAM 0x0202f3c0+0x7e 的 flag halfword: "
        "若 bit0=1 则取候选卡的 ATK 等级字段 (card_type_table bits[7:4]) 与 "
        "slot 对应的 ATK 上限 (0x0202a4d0+0x2a6+slot_idx*14) 比较, 不满足则返回 0; "
        "若 bit1=1 则检查 cost/level 是否在允许范围; "
        "若 bit2=1 则检查等级等条件; 最终通过全部检查后返回 1 (合法)."),
    ("FUN_081035f4", "filter_deck_slot_candidates",
        "由 init_deck_slot_data 和 FUN_08102c6c (card_stats 场景) 调用, "
        "负责对指定 deck_type (r0=[0..3]) 的候选卡片列表进行合法性过滤. "
        "函数根据 deck_type 从 IWRAM 0x0202a4d0 选取对应源列表偏移 "
        "(type0: +0x1a6c, type1: +0x3ccc, type2: +0x42cc, type3: +0x48cc), "
        "清零目标区 0x0202f3c0+0x7e 的计数字段; "
        "然后遍历源列表每对 (card_entry), 对每张卡调用 check_card_valid_for_deck_slot 验证; "
        "通过验证的写入结果区并更新计数; "
        "最后将计数写入 0x0202a4d0+0x4ecc 偏移. 返回 r0=1."),
    ("FUN_081038fc", "build_deck_slot_count_table",
        "由 init_deck_slot_data (deck 初始化最后一步) 以及 FUN_08102c6c (card_stats 场景) 调用, "
        "负责根据已过滤卡片列表构建 deck slot 的 count 统计表. "
        "函数按 deck_type r0 ([0..3]) 选取对应的两组指针, "
        "清零目标区域 (IWRAM r9 基址 +0x1a34 偏移 8 字节); "
        "遍历已排序列表, 按 card_stats_table 查找对应属性类型 (switch 0-8), "
        "在 count_table +0x1a24 对应偏移累加计数; "
        "最后在 +0x1a4c 写入结果摘要. 返回 r0=1."),
    ("FUN_081031a4", "init_deck_slot_data",
        "被 9 个 caller 调用 (indeg=9), 是 card_stats 场景下 deck slot 数据初始化的核心调度函数. "
        "接收 deck_type r0 ([0..3]), 顺序执行五步: "
        "(1) 调用 filter_deck_slot_candidates 以 r0 过滤候选卡片; "
        "(2) 调用 copy_deck_slot_card_data 以 (r0, 1) 复制 deck slot 数据; "
        "(3) 调用 apply_card_obj_attr_by_type 设置 OBJ 属性; "
        "(4) 以比较函数调用 qsort 对结果排序; "
        "(5) 调用 build_deck_slot_count_table 构建统计表. "
        "返回 r0=1."),

    # 2026-05-03: BATCH-8 落地 (topo=183/184/185/186/187/188/189/190/191/192/193/194/195/196/197)
    ("FUN_08101c40", "query_deck_timer_remaining",
        "当 gPrng+0x20e 处存有当前回合计时器值时, 计算距离一局结束还剩余多少秒. "
        "被决斗/卡牌列表场景的多个 caller 在帧更新中调用, 用于控制倒计时显示. "
        "若当前不满足[正在游戏]条件 (state!=1 或 bit5 未置) 则直接返回 0; "
        "否则计算 (0x2a6b - timer_value) / 0x3c, 负数截断为 0 后返回."),
    ("FUN_08106d88", "render_card_name_tiles_to_vram",
        "在卡牌信息显示页面中, 将卡名字符 tile 数据批量写入 VRAM (0x0600e800 区域). "
        "由 FUN_081067e0 在每帧卡名区域刷新时调用. "
        "函数根据 gPrng/state 中的字体宽度标志 (bit2 of byte+0x1e) 选择 6 格或 7 格列宽, "
        "计算出每字符在 tile 网格中的行列位置, 再用 strh 逐 tile 写入目标 VRAM; "
        "对每行最多写 16 个 halfword (0xf+1). "
        "副作用: 修改 0x0600e800 起始的 OBJ tile VRAM 区域."),
    ("FUN_08106c10", "render_card_name_text_to_bg",
        "在卡牌信息页面的 BG 图层上渲染当前选中卡的卡名文字. "
        "函数首先清空 0x0600e800 区域 (0x800 halfword), 再通过 card_data_query 查询卡名字符串; "
        "配置 font_jp 渲染管线 (setup_line_buf_with_font_and_align, align=中央), "
        "置 bit6 标志后调用 text_render_wrapper 输出至 BG tile 缓冲区. "
        "若卡名需要两行渲染 (ldrh+0x0e 判断超过阈值), 则清除 bit5 标志后再次配置并渲染第二行. "
        "最终更新 [0x0202f3c0+0x6a] 为按字体宽度折算的行宽. "
        "由 FUN_081067e0 在卡名区域需要刷新时调用."),
    ("FUN_08106e38", "copy_card_name_font_row_to_sprite_vram",
        "将当前卡名指定行的 font_jp tile 数据复制到 OBJ sprite VRAM (0x06009400 区域), "
        "并将渲染结果提交至 sprite 属性表. "
        "函数根据 bit2 字体宽度标志决定每行 tile 列数 (6 或 7), "
        "按行索引 r1 计算目标 VRAM 偏移 (r1 * cols * 0x400), "
        "从 font_jp 源地址 (0x0200af20) 复制 cols*0x400 字节, "
        "再清零同尺寸区域后调用 commit_line_buffer_to_sprite_vram 提交; "
        "最后将行索引写回 [state+0x6e+row*2]. 由 FUN_081067e0 在字体行刷新时调用."),
    ("FUN_081067e0", "update_card_info_name_display",
        "卡牌信息页面中, 每帧驱动卡名显示区域的更新逻辑. "
        "函数检查全局状态 (gPrng+0x146 = 0x2a3*2 halfword 与 bit1/bit4 标志), "
        "根据当前渲染阶段分派到 FUN_08106c10 (渲染卡名文字到 BG) 或后续 VRAM tile 复制分支. "
        "仅有一个 caller (FUN_080ff528), 属于卡牌列表场景中卡名区域的专用更新驱动函数."),
    ("FUN_080ff528", "trigger_card_name_render_if_idle",
        "在卡牌列表/决斗场景帧更新中, 检查当前是否处于[游戏进行中且计时器未耗尽]状态, "
        "若满足条件则调用 query_deck_timer_remaining 判断是否仍有时间; "
        "若结果为 0 (时间归零) 则置 [0x0202f3c0+0x1e] bit5, "
        "并在成功后调用 FUN_081067e0 驱动卡名区域刷新. "
        "主要被卡牌列表总帧循环 (FUN_080fe308) 调用."),
    ("FUN_08101a88", "apply_card_frame_palette_animated",
        "根据当前选中卡的属性 (attribute) 计算卡框调色板动画帧, "
        "将对应调色板数据写入 OBJ 调色板区域 (0x05000360). "
        "函数读取 [0x0202a4d0] game state 与 card_mini_frame_pal_gap 调色板数据; "
        "通过 __divsi3/__modsi3 将属性值折算为 5 种旋转循环中的位置, "
        "选出对应颜色写入目标 strh 序列. "
        "最后更新 [0x0202f3c0+0xa] (帧计数) 并溢出归零. "
        "被显示/blend/BG/card_frame 相关的帧更新函数调用."),
    ("FUN_08107b4c", "dispatch_oam_write_by_mode",
        "根据当前场景模式标志决定调用哪个 OAM 写入函数: "
        "若 [0x0202f3c0+0x1e] halfword 的 bits[13:12] == 0xc000>>7 (即 0x6002) 且 r3!=0, "
        "则调用 write_obj_attr_packed (仅写属性); "
        "否则调用 write_oam_entry_from_packed_args (完整 OAM 写入). "
        "被多个 (indeg=14) 场景渲染函数频繁调用, 是 OAM 写入的中心分派点."),
    ("FUN_08101d0c", "write_digit_sprites_for_score",
        "在卡牌详情/决斗场景中, 遍历多个数值槽 (r4 in [0..8]), "
        "从 ROM 数字 tile 表中取出对应数字 sprite 属性并调用 dispatch_oam_write_by_mode 写入 OAM. "
        "每个槽读取 [0x09e60068 + slot*4] 中存储的 sprite 描述符, "
        "并通过 mod/div 对数值 (0x0202a4d0+offset) 进行十进制拆位, "
        "计算出在 VRAM tile 中的行列坐标后组装 OAM entry. "
        "被 FUN_080fefaa (显示/BG/card_frame 帧更新) 调用."),
    ("FUN_08101c94", "compute_card_frame_palette_index",
        "根据 [0x0202f3c0+0xc] (卡属性值, s16) 计算当前帧应使用的调色板槽序号, "
        "并将结果写入 OBJ 调色板区 (0x05000162). "
        "属性值 <= 0x13 时, 直接取 round(attr/2)+0x15 作为槽号; "
        "超过时取 0x1f - round((attr-0x14)/2). "
        "随后从 card_mini_frame_pal_gap 基址拷贝 4 个 halfword 至 0x05000162, "
        "并递增帧计数 [0x0202f3c0+0xc] 模 0x27+1 滚动. "
        "由 FUN_080fefaa 在卡框调色板动画帧更新时调用."),
    ("FUN_08107eb0", "clear_card_display_flag_bits",
        "清除 [0x0202f3c0+0x1f] 中的 bit0+bit3 (掩码 0x9 取反写回), "
        "用于在卡牌统计/详情显示初始化时复位显示控制标志. "
        "函数体极小 (6 指令叶子), "
        "被 FUN_080fefaa / FUN_080ff918 / FUN_080ff94c 三个 card_stats 相关函数调用."),
    ("FUN_080ffaa4", "compute_card_list_scroll_position",
        "根据当前场景状态计算卡牌列表的滚动偏移量. "
        "函数读取 [0x0202a4d0+0x10] 与 [+0x0e] 的两个 s16 值求和后乘以 5 再乘以 2 "
        "(公式: (a+b)*5*2), 得出列表行偏移; "
        "再与 [0x0202f3c0+0x78] 处的最大行数比较截断; "
        "若未激活 (bit0=0) 则直接取 [+0x10] 和 [+0x0e] 之和. "
        "返回最终滚动偏移值 (可为负, 截断为 -1). "
        "indeg=10 高频工具函数, 被多个场景初始化和帧更新 caller 共用."),
    ("FUN_0810a8e4", "copy_card_icon_tiles_to_vram",
        "将卡牌图标 tile 数据从 ROM (0x06017280 区域) 分两批通过 tile_2d_row_copy 写入 sprite VRAM, "
        "再在 4 行 x 4 列的迭代中对每行以 copy_bytes_by_halfword 将 0x20 halfword 块 "
        "从 0x060172a0 复制至 0x06017300. "
        "被 FUN_0810a52c (渲染卡牌 stats 时) 和 FUN_08107e5c 调用, 属 vram 图标贴图工具函数."),
    ("FUN_0810a52c", "render_card_stats_panel",
        "渲染卡牌统计面板 (ATK/DEF/Level 等数值及图标). "
        "函数接受卡牌列表行序号作为参数, 从 card_stats_table 中读取对应卡的属性字段; "
        "通过 read_card_list_field_by_row_col 和 test_card_flag_bit 获取卡牌标志位; "
        "然后对 ATK/DEF 数值进行十进制拆位 (mod/div 循环), 将拆出的数字写入显示缓冲区; "
        "根据卡型是否含特殊 Level 字段决定渲染路径, "
        "最终调用 copy_card_icon_tiles_to_vram 更新图标区域, "
        "并刷新 card_stats 相关 flag 字节."),
    ("FUN_0810a8c0", "clear_card_stats_render_flags",
        "清除 [0x0202f3c0+0x1f] 中的 bit0+bit1 (掩码 0x3 取反写回), "
        "复位卡牌统计面板的渲染就绪标志. "
        "函数体极小 (6 指令叶子, 无 push/pop), indeg=5, "
        "被多个 scene_card_list/card_stats caller 在场景切换或面板清理时调用. "
        "与 clear_card_display_flag_bits (0x08107eb0) 操作同一 flag 字节但清除不同位."),

    # 2026-05-04: BATCH-9 落地 (topo=198/199/200/201/202/203/204/206/207/208/209/210/211/212/213)
    ("FUN_080ff918", "render_card_stats_panel_if_scrolled",
        "由 FUN_080fefaa (display/blend/window/bg/card_stats/font_jp 场景帧主循环) 调用, "
        "触发条件为卡牌列表帧更新时. 先重置 clear_card_stats_render_flags / "
        "clear_card_display_flag_bits 两项标志, 再调用 compute_card_list_scroll_position "
        "取得当前滚动索引; 若滚动索引 >= 0, 以该索引 *2 偏移读取 [0x0202f3c0+0x74] 表中的卡牌 "
        "entry, 经 lsls/lsrs 20 位掩码提取 12 位字段后传入 render_card_stats_panel 渲染卡牌详情面板. "
        "返回 1 表示成功渲染, 0 表示无有效滚动位置跳过渲染."),
    ("FUN_081081a0", "set_card_stats_display_position",
        "由 FUN_080fefaa (display/blend/window/bg/card_stats/font_jp 场景帧主循环) 调用, "
        "用于写入卡牌统计显示区域的坐标. 函数将 r0 (x) 写入 [0x0202f3c0+0x34], "
        "将 r1 (y) 写入 [0x0202f3c0+0x36]; 0x0202f3c0 为卡牌统计显示状态结构体基地址, "
        "+0x34/+0x36 在同模块多处被 strh 写入, 对应显示坐标 halfword 对. 返回常量 1."),
    ("FUN_08107b90", "write_oam_entry_priority_aware",
        "被 FUN_08100cc4 / FUN_08101574 (scene_card_list) / FUN_081016a4 / "
        "FUN_08107bdc (card_stats/font_jp) / FUN_0810903c (card_stats/font_jp/game_str) "
        "等 6 处共享调用, 是卡牌列表场景的通用 OAM 写入中间层. "
        "读取 [0x0202f3c0+0x1e] 的 bits[13:12] (掩码 0x6000), 与常量 0xC000 比较: "
        "相等且 r3==0 则调用 write_obj_attr_with_priority (覆写 OAM priority 字段), "
        "否则调用 write_oam_entry_with_tile_inc (按 tile 递增方式写 OAM). "
        "r0=OAM 参数包, r1=属性 1 (尺寸/形状), r2=属性 0 (坐标), r3=标志 (0 时启用 priority 路径)."),
    ("FUN_081016a4", "write_fixed_card_list_cursor_oam",
        "由 FUN_080fefaa (display/blend/window/bg/card_frame/card_stats/font_jp/frame_counter "
        "场景帧主循环) 唯一调用, 触发时机为每帧更新卡牌列表光标/指示图标的 OAM 属性. "
        "函数以硬编码参数调用 write_oam_entry_priority_aware: "
        "r0=0x00020028 (attr0: y=0x28=40, 16x16 size), r1=0x40 (attr1: x=64), "
        "r2=0x0c22 (attr2: tile=0x22, palette=12), r3=0 (允许 priority 路径). "
        "所有参数均为字面量, 推测为固定位置光标/箭头精灵的初始化写入."),
    ("FUN_08101ba8", "render_deck_timer_digits_oam",
        "由 FUN_080fefaa (display/blend/window/bg/card_frame/card_stats/font_jp/frame_counter "
        "场景帧主循环) 唯一调用, 触发条件为: [0x0202a4d0+0x0] == 1 (card_type 字段为 1) "
        "且 [0x0202a4d0+0x16] bit5 != 0 (计时器使能标志). 满足条件后调用 "
        "query_deck_timer_remaining 取剩余秒数, 依次以 /60 得到分钟数, "
        "%60 再 /10 / %10 得到秒十位/秒个位, 共 4 个十进制数字; "
        "在 0x09e60058 ROM 字形表中按索引找到对应 halfword 属性, "
        "循环 4 次调用 dispatch_oam_write_by_mode 将每位数字精灵写入 OAM. "
        "若条件不满足则跳过, 直接返回 1."),
    ("FUN_08101e2c", "render_card_list_scrollbar_oam",
        "由 FUN_080fefaa (display/blend/window/bg/card_frame/card_stats/font_jp/frame_counter "
        "场景帧主循环) 唯一调用, 每帧负责绘制卡牌列表滚动条的 OAM 精灵组. "
        "首先检查 [0x0202f3c0+0x7a] 当前列表长度是否 > 4, 若否则跳过整个渲染. "
        "满足条件后读取 [0x0202a4d0+0x10] 作为滚动位置基准, "
        "从 [0x0202f3c0+0x7a] 减 4 得到可滚动范围, "
        "以 SCROLLBAR_BASE_Y=0x52 * 4 / __divsi3 计算 thumb 块高度; "
        "循环对 N 个 thumb tile 调用 dispatch_oam_write_by_mode, "
        "并对两端固定端帽精灵 (top: 0x002f00ec, bot: 0x008900ec) 写固定 OAM 条目; "
        "最终将 thumb 中心 x 坐标写入 [0x0202f3c0+0x1c]."),
    ("FUN_0810ab90", "render_card_type_icon_oam",
        "由 FUN_0810a22c (card_stats/font_jp) 唯一调用, "
        "用于在卡牌统计面板中渲染卡牌属性图标 OAM 精灵组. "
        "函数首先检查 [0x0202f3c0+0x1f] bit1 是否置位; 若未置位则直接返回 0. "
        "通过 [0x0202f3c0+0x54] (card_type s16) 计算 x 偏移: type * 5 OAM slots per type group, "
        "再加 [+0x4e] * 14 bytes 行偏移; bit2 置位时额外加 0x16 (=22) 行间距校正. "
        "检查 [0x0202a4d0+0x16] bits[0:2]==5 则 r10 减 8. "
        "最终以两次 dispatch_oam_write_by_mode 写 OAM slot 0x9b94/0x9b96 (图标主体), "
        "再循环写 0x9b98 (N 个附加 tile), 返回 1."),
    ("FUN_0810a944", "render_card_name_text_to_vram",
        "由 FUN_0810a22c (card_stats/font_jp) 唯一调用, "
        "触发条件为 [0x0202f3c0+0x1f] bit1 置位. "
        "函数先对 VRAM 0x0600e800 区域调用 zero_fill_by_halfword 两次清空 sprite tile 缓冲; "
        "调用 setup_line_buf_pos_and_font 初始化行缓冲位置与字体 (mode=0x20, font=2). "
        "根据 [0x02006ed0+0x6c2c] 处 bit0-2 判断走 resolve_card_gfx_pointer_by_type "
        "(卡图指针路径) 还是 select_charset_then_load_name (字符集名称路径), "
        "将卡牌名称字符串写入行缓冲; strlen 截断至 50 字符后调用 text_render_wrapper + "
        "commit_line_buffer_to_sprite_vram 将名称文本提交到 sprite VRAM. "
        "最终循环 2x32 次通过 strh 将 tile 索引写入 0xffff9000 区域 (相对基址负偏移 -0x7000), "
        "并将文本起始 x 写入 [0x0202f3c0+0x4a], 字形宽度写入 [+0x4c/+0x52/+0x54]."),
    ("FUN_0810a22c", "render_card_name_panel",
        "由 FUN_080fefaa (display/blend/window/bg/card_frame/card_stats/font_jp/frame_counter "
        "场景帧主循环) 唯一调用, 每帧负责渲染卡牌名称显示面板的全部内容. "
        "首先检查 [0x0202f3c0+0x1f] bit1 是否置位 (名称面板使能), 未置位则跳过全部逻辑. "
        "置位后再检查 bit6 是否置位: 若置位, 调用 render_card_name_text_to_vram 将卡牌名称文本渲染到 "
        "sprite VRAM 并清除 bit6; 随后无条件调用 render_card_type_icon_oam 写图标 OAM 精灵. "
        "其后根据 bit2 分支, 进一步更新名称面板的坐标和 OAM 精灵属性. 返回 1."),
    ("FUN_08100cc4", "render_card_list_row_sprites_oam",
        "由 FUN_080fefaa (display/blend/window/bg/card_frame/card_stats/font_jp/frame_counter "
        "场景帧主循环) 唯一调用, 负责将卡牌列表中 4 行 (r6: 0..3) 的行指示精灵写入 OAM. "
        "函数首先检查 [0x0202a4d0+0x16] bit0 是否置位, 若未置位则跳过所有写 OAM. "
        "对每行: 从 [0x0202f3c0+0x78] 处的行数组首地址读当前行 entry, "
        "以 [entry+0x10] 取 y 偏移加当前行索引作为新 y; "
        "计算 OAM attr0 (y | 0xC00, bits[10:11] = OBJ mode field), "
        "连续调用两次 write_oam_entry_priority_aware 写两个相邻 sprite."),
    ("FUN_08107ec4", "render_card_attribute_badge_oam",
        "被 FUN_080fefaa (display/blend/window/bg/card_stats) 和 FUN_080ff94c (card_stats) "
        "两处调用, 用于在卡牌统计面板中渲染卡牌属性徽章 OAM 精灵. "
        "函数首先对 [0x0202f3c0+0x5a..+0x5d] 四字节执行 OR 0xFF (标记已用 tile 槽), "
        "再读取 [0x0202a4d0] 作为卡牌索引, 调用 read_card_list_field_by_index 取属性字段值后减 2, "
        "对结果做 9 路 switch (case 0-8) 分派不同的属性类型处理块. "
        "各 case 从 card_stats_table 按行读取对应属性的 tile 坐标数据 (11 列, 含 0xffff 边界检查), "
        "以 __divsi3/__modsi3 计算 tile 行列后调用 dispatch_oam_write_by_mode 写 OAM 精灵."),
    ("FUN_08107e5c", "init_card_icon_tile_slots",
        "由 FUN_080ff94c (card_stats) 唯一调用, 在图标路径卡牌统计渲染前执行 tile 槽初始化. "
        "先调用 copy_card_icon_tiles_to_vram 将卡牌图标 tile 数据复制到 VRAM sprite 区; "
        "随后对 [0x0202f3c0+0x5a..+0x5d] 四字节各 OR 0xFF (标记 tile 槽为已分配); "
        "再将 [0x0202f3c0+0x50], [+0x56], [+0x58], [+0x60] 四个 halfword 清零; "
        "最后读 [+0x1f] OR bit3 写回, 读 [+0x1e] AND ~0x11 (清除 bit0+bit4) 写回. 函数返回 1."),
    ("FUN_080ff94c", "render_card_stats_panel_with_icon",
        "由 FUN_080fefaa (display/blend/window/bg/card_frame/card_stats/font_jp/frame_counter "
        "场景帧主循环) 唯一调用, 是图标路径的卡牌统计面板渲染编排函数, "
        "与 render_card_stats_panel_if_scrolled 构成同一 caller 下的两变体. "
        "函数先调用 clear_card_display_flag_bits 和 clear_card_stats_render_flags 重置标志, "
        "再调用 init_card_icon_tile_slots 将图标 tile 复制到 VRAM 并初始化槽位; "
        "调用 compute_card_list_scroll_position 取滚动索引, 若 >= 0 则以 index*2 偏移读取 "
        "[0x0202f3c0+0x74] 表中的 entry, lsls/lsrs 20 位提取卡牌 id 字段后传入 "
        "render_card_attribute_badge_oam 渲染属性徽章. 固定返回 1."),
    ("FUN_0810a8d4", "set_card_stats_sprite_position",
        "由 FUN_080fefaa (display/blend/window/bg/card_frame/card_stats/font_jp/frame_counter "
        "场景帧主循环) 唯一调用, 将 r0 (x) 和 r1 (y) 以 strh 写入 "
        "[0x0202f3c0+0x34] 和 [0x0202f3c0+0x36]. "
        "与 0x081081a0 (set_card_stats_display_position) 为写相同偏移对的两个叶子函数变体: "
        "本函数无 push/pop (纯叶子, bx lr 直接返回), 0x081081a0 有 lr push 但逻辑等价. "
        "0x0202f3c0 是卡牌统计显示状态结构体基地址, +0x34/+0x36 halfword 对统一表示精灵显示坐标."),
    ("FUN_081083b0", "render_card_type_badge_oam",
        "由 FUN_08107bdc (card_stats/font_jp) 唯一调用, "
        "在 scene_card_list 卡牌统计面板中渲染卡牌类型徽章 (monster/spell/trap 等) 的 OAM 精灵. "
        "函数首先检查 [0x0202f3c0+0x1f] bit3 是否置位 (类型徽章显示使能); 未置位则返回 0. "
        "置位后调用 read_card_list_field_by_index 读卡牌类型字段, 减 2 后对 0..8 做 9-case switch: "
        "case 0-1 (monster 分支) 设置 11 tiles (88px); "
        "case 2-3 / case 4 设置 6 tiles (48px); case 5 / case 6-7 / case 8 设置 5 tiles (40px). "
        "以 (width+7)/8 向上取整 tile 高度, 循环调用 dispatch_oam_write_by_mode "
        "写 OAM slot 0x9b94/0x9b96 (主/副徽章) 及 0x9b98 (附加 tile 组), "
        "结构与 render_card_type_icon_oam (0x0810ab90) 完全对称."),

    # 2026-05-04: BATCH-10 落地 (topo=213..228)
    ("FUN_081081bc", "render_card_atk_def_to_vram",
        "FUN_08107bdc (card_stats/font_jp) bit3 set -> zero_fill_by_halfword(0x0600e800, 0x800) "
        "clear ATK/DEF tile buf, then 2x2 coord grid loop strh tile indices; "
        "zero_fill_by_halfword(0x06009800, 0x800) second clear. Returns 1 or 0 (bit3 unset)."),
    ("FUN_0810a190", "lookup_sjis_font_index_by_char",
        "Called by render_card_name_glyph_to_vram (0x0810823c). "
        "r0=uint16 char_code. <=0xFF: direct table ROM 0x09e61158 halfword fetch. "
        ">0xFF: bsearch_index_by_callback on sorted SJIS table ROM 0x09e6115c. "
        "Both paths return byte-swapped glyph_index (hi/lo swap). Read-only ROM tables."),
    ("FUN_0810823c", "render_card_name_glyph_to_vram",
        "Called by tick_card_stats_render_panel (0x08107bdc) when bit4 set. "
        "Reads card_list_field index from IWRAM 0x0202a4d0[+4], calls read_card_list_field_by_index. "
        "r7<=0: write empty glyph. r7>0: charset flag [0x02006c2c] bit[2:0] -> "
        "resolve_card_gfx_pointer_by_type + char_code_to_glyph_index + lookup_sjis_font_index_by_char "
        "or select_charset_then_load_name. strb glyph hi/lo bytes to VRAM. switch(r7-2) per card type."),
    ("FUN_08107bdc", "tick_card_stats_render_panel",
        "Called by tick_card_display_render_panel (0x080fefaa) every frame. "
        "bit3 set: call render_card_atk_def_to_vram, clear bit0+bit6. "
        "bit4 set: call render_card_name_glyph_to_vram, clear bit4+bit0. "
        "read_card_list_field_by_index -> r6 card type -> cmp 2/7 -> render_card_type_badge_oam. "
        "switch(r6-2) dispatch per card type OAM/coord calc."),
    ("FUN_080ff9e0", "advance_card_list_frame_counter",
        "Called by tick_card_display_render_panel (0x080fefaa) every frame. "
        "Reads IWRAM 0x0202a4d0[+6] display_mode; if !=2 zeroes frame_counter. "
        "If ==2, compares 5 fields ([+4]/[+0xe]/[+0x10] vs [0x0202f3c0+0x12]/[+0x18]/[+0x1a]); "
        "all match: increment [0x0202f3c0+0xe] frame_counter up to max 0x1d(29); "
        "any mismatch: zero it."),
    ("FUN_08101764", "tick_card_list_slot_highlight_oam",
        "Called by tick_card_display_render_panel (0x080fefaa). "
        "Outer loop r7=0..3. Reads display_mode from IWRAM 0x0202a4d0[0], "
        "branches on enum 0/1/2/3 to compute tile offsets and write OAM sprite attrs. "
        "Uses ROM table 0x09e60010 for tile/slot params. "
        "Maintains card_list slot highlight/selection OAM each frame."),
    ("FUN_08101574", "write_card_list_slot_oam_entries",
        "Called by tick_card_display_render_panel (0x080fefaa). "
        "Calls write_oam_entry_priority_aware(tile=0x40, y=0, ...) for row 0; "
        "outer loop r5=0..5 (6 rows): read_card_list_field_by_row_col, "
        "[0x0202f3c0+0x1f] bit5 -> priority flag, write_oam_entry_priority_aware per row (r2=0x24 step). "
        "Second pass col=0 entries: for r6>0 rows writes extra sprites at y=0xa8+row*0x10, x=0x2a."),
    ("FUN_080fefaa", "tick_card_display_render_panel",
        "Called by FUN_080fe308 (scene main loop). "
        "Display panel frame dispatcher for card_stats/font_jp/frame_counter subsystems. "
        "Entry: movs r5,#0 / movs r1,#0 then jumps to main body at LAB_080fefae. "
        "Downstream callees: tick_card_stats_render_panel, advance_card_list_frame_counter, "
        "write_card_list_slot_oam_entries, tick_card_list_slot_highlight_oam."),
    ("FUN_080ff434", "apply_card_list_scroll_selection",
        "Called by FUN_080fe308 (scene main loop). "
        "compute_card_list_scroll_position -> if <0 return 0. "
        "Read card_id from [0x0202f3c0+0x74] offset table (20-bit). "
        "card_list_on_select_to_info_page; [0x02006c2c] bit[2:0] lang -> strb update [0x0201afb0] bit1. "
        "strh 0 -> REG_DISPCNT (0x04000000), strh 0 -> PAL_RAM_BASE (0x05000000). "
        "clear_all_card_list_slot_flags. Returns 1."),
    ("FUN_080ff4b8", "dispatch_card_info_list_tick_by_state",
        "Called by FUN_080fe308 (scene main loop). "
        "Reads IWRAM 0x0202a4d0[0] display_mode: !=1 -> tick_card_info_page_by_state. "
        "==1: check [+0x16] bit5 deck_timer enable; not set -> tick_card_info_page_by_state. "
        "Set: query_deck_timer_remaining; !=0 -> tick_card_info_page_by_state. "
        "==0 (timer done): card_list_screen_init, return 1 (scene switch)."),
    ("FUN_080fffc4", "dispatch_card_list_render_by_scroll_mode",
        "Called by FUN_080fe308 (scene main loop). "
        "resolve_card_scroll_offset_by_mode updates [0x0202f3c0+0x74]/[+0x7a]. "
        "Reads IWRAM 0x0202a4d0[0] display_mode 0/1/2/3 -> write_card_list_slot_tiles_to_vram with mode-specific offset. "
        "Then: card_list_tile_renderer, setup_card_list_bg2_tilemap, strh 0xf dirty flag x3, "
        "render_card_list_visible_slots, render_card_list_entry_row, "
        "dispatch_card_frame_tile_load_by_type, setup_card_list_tile_rows. Returns 1."),
    ("FUN_08106bfc", "clear_card_list_mode_bits",
        "Called by FUN_080fe308 (scene main loop). Leaf function. "
        "rsbs r0,#3 -> mask 0xFFFFFFFD (~3). ldrb [0x0202f3c0+0x1e], ands, strb -> clears bit0+bit1. "
        "Returns 1. Resets card_list mode low 2 bits on state transition."),
    ("FUN_0810796c", "tick_card_stat_bonus_oam",
        "Called by tick_card_slot_sprite_animation (0x08106ebc). "
        "Check [0x0202f3c0+0x1e] bit7 (render enable); return 0 if unset. "
        "[0x02000000+0x6c2c] bit[2:0] -> EN table 0x09e606f4 or JP table 0x09e60894. "
        "ldrsh [r5+0x38] slot type; switch(2/3/4) -> r6=1/3/1, r7=-19/-19/-10. "
        "Loop r4=0..r6-1: calc_card_stat_bonus_by_type + dispatch_oam_write_by_mode. Returns 1."),
    ("FUN_08106ebc", "tick_card_slot_sprite_animation",
        "Called by dispatch_settings_card_display_by_mode (0x080ff8d0) and FUN_081047e8. "
        "Reads gPrng+0x148/+0x14e random halfwords -> state mask. "
        "bit7 of [0x0202f3c0+0x1e]: animation enable gate. bit4: sub-state flag. "
        "Lang table select 0x09e606f4/0x09e60894. slot_type 0-4 -> anim counter inc/dec, "
        "sync_state_and_init_sprite, strb anim attr [r6+0x16]. "
        "Tail: bit5 unset -> tick_card_stat_bonus_oam + calc_card_stat_bonus_by_type + write_slot_display_coords. Returns 1."),
    ("FUN_080ff8d0", "dispatch_settings_card_display_by_mode",
        "Called by FUN_080fe308 (scene main loop). "
        "Reads IWRAM 0x0202a4d0[0] display_mode: !=1 -> return 0. "
        "==1: [+0x16] bit5 deck_timer enable; not set -> return 0. "
        "query_deck_timer_remaining: !=0 -> return 0. "
        "[0x0202f3c0+0x38]==0x12 -> return 0 (special state). "
        "Otherwise: orrs [0x0202f3c0+0x1e] bit5 (0x20), strb, tick_card_slot_sprite_animation. Returns 1."),

    # 2026-05-05: BATCH-11 落地 (topo=229/230/231/232/233/234/235/236/237/238/239/240/241/242/243)
    ("FUN_081078d4", "clear_card_list_slots_and_anim_flag",
        "由 FUN_080fe308 (卡牌列表场景主循环) 和 FUN_081047e8 (deck 编辑场景主循环) 各调用一次, "
        "用于在场景状态切换时清理槽位与动画标志. "
        "函数依次以 slot_index=1 和 slot_index=2 调用 clear_card_list_slot_flag_by_index 清除对应槽位标志位; "
        "随后对 [0x0202f3c0+0x1e] 执行 ands 0x7F, 即清除 bit7 (动画/渲染进行中标志), 完成双重重置. "
        "返回 r0=1 表示操作完成."),
    ("FUN_0810325c", "write_card_list_field_by_row_col",
        "由 FUN_080feede 区域 (卡牌列表场景行渲染) 以 r0=card_id, r1=col_index [1..6], r2=-1 连续调用 6 次, "
        "以及 FUN_08102034/08102124/081021dc/0810236c (均属 card_stats 场景) 调用. "
        "函数计算二维索引 (r0*7+r1)*2 并加基址偏移 0xa9*4=0x2A4 写入 IWRAM 0x0202a4d0, "
        "将 r2 (halfword) 存储到对应槽位字段. "
        "与已命名的 read_card_list_field_by_row_col (0x08103280) 构成完全对称的写操作版本, 同一翻译单元内的读写对."),
    ("FUN_08109e08", "render_card_stats_text_full",
        "由 FUN_0810903c (card_stats+font_jp+game_str 场景渲染协调器) 唯一调用. "
        "函数入口检查 [0x0202f3c0+0x1e] bit3 (0x8) 是否置位; 若未置位则直接返回 0, 表示渲染条件未满足. "
        "满足条件时分配 0x60 字节栈帧并执行完整的卡片属性文字渲染流程 (含 card_stats 和 game_str 数据). "
        "为 0810903c 调用的两个渲染子函数之一, 与 08109a50 (含 vram 写入) 并列, "
        "本函数侧重纯文字内容 (card_stats/game_str) 渲染."),
    ("FUN_08109a50", "render_card_jp_text_to_vram",
        "由 FUN_0810903c (card_stats+font_jp+game_str 场景渲染协调器) 唯一调用. "
        "函数入口检查 [0x0202f3c0+0x1e] bit3 (0x8) 是否置位; 若未置位则直接返回 0. "
        "满足条件时分配 0x2C 字节栈帧, 执行日文字体 (font_jp) 驱动的文字渲染并写入 VRAM. "
        "为 0810903c 调用的两个渲染子函数之一, 与 08109e08 (card_stats/game_str 纯文字) 并列, "
        "本函数侧重 VRAM 直写路径的日文字符渲染. "
        "VRAM 目标: 0x0600e800 (zero_fill_by_halfword 清零) 和 0x06009800 (commit_line_buffer_to_sprite_vram 写入)."),
    ("FUN_0810903c", "dispatch_card_stats_text_render",
        "由 FUN_080ff7e0 (card_stats/font_jp/game_str 场景帧更新器) 唯一调用. "
        "函数入口检查 [0x0202f3c0+0x1e] bit3 (0x8) 是否置位; 若未置位则尝试置 bit4 (0x10) 并返回; "
        "满足条件后加载 gPrng 偏移处的两个 halfword (偏移 0xA4*2 和 0xA7*2) 做 BIC 运算得到渲染区域掩码. "
        "随后检查 [0x0202f3c0+0x1e] bit3 再次确认, 按条件分派调用两个渲染子函数: "
        "render_card_jp_text_to_vram (08109a50) 和 render_card_stats_text_full (08109e08), "
        "分别负责日文 VRAM 渲染和 card_stats 文字渲染."),
    ("FUN_080ff7e0", "trigger_card_stats_render_on_timeout",
        "由 FUN_080fe308 (卡牌列表场景大型主循环) 唯一调用. "
        "函数首先读取 [0x0202a4d0+0] (display_mode) 与 [+0x16] bit5 (deck_timer_enable); "
        "若 display_mode!=1 或 deck_timer 未启用则跳至 fallback 分支. "
        "否则调用 query_deck_timer_remaining 查询剩余时间; 若仍有时间 (返回非 0) 则跳过渲染. "
        "当计时器归零时对 [0x0202f3c0+0x1e] OR 0x20 (bit5) 置位, 标记卡片统计区需要渲染; "
        "之后调用 dispatch_card_stats_text_render (0810903c) 触发文字渲染. "
        "Fallback 分支直接调用 dispatch_card_stats_text_render. "
        "返回 dispatch_card_stats_text_render 的返回值 (r0), 或固定 1."),
    ("FUN_081095e8", "clear_card_list_slot0_and_mode_bits",
        "由 FUN_080fe308 (卡牌列表场景主循环) 在 tick_card_display_render_panel 之后唯一调用, "
        "用于场景状态切换时清理 slot=0 及模式标志. "
        "函数以 slot_index=0 调用 clear_card_list_slot_flag_by_index 清除第 0 槽; "
        "随后对 [0x0202f3c0+0x1e] 执行 rsbs #0 生成掩码 ~0x9 = 0xFFFFFFF6, "
        "即 AND 清除 bit0 (slot_active) 和 bit3 (render_en); 返回 r0=1. "
        "与 081078d4 构成同 family 的对称清除操作 (081078d4 清除 slot=1+2 及 bit7; 本函数清除 slot=0 及 bit0+bit3)."),
    ("FUN_081099f0", "copy_card_frame_tile_rows_to_vram",
        "由 FUN_08109300 (vram+palette+scene_card_list+settings 场景渲染器) 在 load_card_frame_tile_row_by_index 之后唯一调用, "
        "负责将卡帧 tile 行数据批量复制到 VRAM. "
        "函数以固定参数调用 tile_2d_row_copy 两次: "
        "第一次以目标 r0=DAT_08109a40, row=0, cols=4, rows=4; "
        "第二次以同一目标, 另一调色板 r1=DAT_08109a44, cols=3, rows=3. "
        "两次调用覆盖卡帧的大/小两种 tile 区域, 完成 VRAM 数据写入. 固定返回 r0=0."),
    ("FUN_081096d4", "compute_card_slot_display_offset",
        "由 FUN_080ff56c (card_stats+settings 场景) 和 FUN_08109300 (vram+palette+scene_card_list+settings 场景渲染器) 各调用一次. "
        "函数入口检查 [0x0202f3c0+0x1e] bit3 (0x8) 是否置位; 未置位则返回 0. "
        "满足条件后读取 [0x02006c2c] bit[2:0] (语言/设置模式); "
        "bit[2:0]=0 时从 [0x0202f3c0+0x38] 读取 slot_type (s16), 计算 slot_type*5*4 并以 DAT_0810971c (ROM 基址) 为基准定位 slot_entry; "
        "bit[2:0]!=0 时从另一路径获取. "
        "在 slot_entry 中搜索匹配 [r8=card_id, caller-set non-APCS] 的条目 (cmp r0,r8 @ 0810975c), "
        "找到后将 tile_col*0x40+0x8 / tile_row*0x40+0x8 写入 [0x0202f3c0+0x40] 和 [+0x42] 两个 halfword 字段. "
        "最终返回 1."),
    ("FUN_08109300", "render_card_frame_slot_to_vram",
        "由 FUN_080ff56c (card_stats+settings 场景) 唯一调用, 负责将指定卡帧槽位的 tile 数据和调色板写入 VRAM. "
        "函数接收三个参数 (r0=slot_index, r1=palette_id, r2=card_type), 保存至栈; "
        "读取 [0x02006c2c] bit[2:0] 选择两套 ROM 查找表 (DAT_08109340=0x09e60cc8 或 DAT_081094c0=0x09e60e44); "
        "按 slot_index*5*4 定位目标 slot_entry. "
        "调用 copy_bytes_by_halfword 复制 0x280 字节 tile 数据至 VRAM 0x06009400; "
        "对 slot_entry 的每个 col/row 调用 resolve_card_frame_palette_by_type + tile_2d_row_copy 将调色板索引写入 VRAM 0x06011000. "
        "最后调用 copy_bytes_by_halfword 向 VRAM 0x0600E800 写入 OAM tile 头信息, "
        "再调用 load_card_frame_tile_row_by_index 和 copy_card_frame_tile_rows_to_vram (081099f0) 完成 tile 行复制; "
        "对 [0x0202f3c0+0x1e] OR 0x8 (bit3) 置位标记渲染完成. "
        "r2==-1 (无效 slot) 时直接返回 0."),
    ("FUN_08109608", "compute_card_slot_size_bounds",
        "由 FUN_080ff56c (card_stats+settings 场景) 唯一调用, 在 render_card_frame_slot_to_vram (08109300) 之后调用. "
        "函数接收 r0=x_pos, r1=y_pos 两个坐标参数, 检查 [0x0202f3c0+0x1e] bit3; 未置位则直接返回 0. "
        "满足条件后读取 [0x02006c2c] bit[2:0] 选择查找表 (0x09e60cc8 或 0x09e60e44), "
        "按 [0x0202f3c0+0x38]*20 定位 slot_entry. "
        "从 slot_entry [+0x8] / [+0x9] 读取 tile_w / tile_h (各 4 位), "
        "计算 x_bound = x_pos - tile_w*16 (clamped >= 4); y_bound = y_pos - tile_h*16 (clamped >= 4), "
        "写入 [0x0202f3c0+0x34] 和 [0x0202f3c0+0x36] (各 halfword). "
        "若 bit3 仍置位则调用 write_slot_display_coords 写出最终坐标. 返回 1."),
    ("FUN_080ff56c", "dispatch_card_frame_render_by_mode",
        "由 FUN_080fe308 (卡牌列表场景大型主循环) 唯一调用. "
        "函数读取 [0x0202a4d0+6] (display_mode, s16) 作为一级 switch 分支键 ([0..3]): "
        "mode=0 进入子分支检查 [+0x8] 和 [+0x6], 分派到 render_card_frame_slot_to_vram (08109300) + "
        "compute_card_slot_size_bounds (08109608) + compute_card_slot_display_offset (081096d4); "
        "mode=1 检查 [+0x16] bit6 (扩展标志) 后调用 read_card_list_type_hi_nibble 并路由; "
        "mode=2 调用 compute_card_list_scroll_position 后对选中 card_id 定位 card_stats_table entry, "
        "再按 [+0] 枚举 (0/1/2/3) 调用 render_card_frame_slot_to_vram + compute_card_slot_size_bounds + "
        "resolve_card_gfx_row_by_type + compute_card_slot_display_offset; "
        "mode=3 直接调用 dispatch_card_frame_tile_load_by_type. "
        "每条路径末尾均置 [0x0202f3c0+0x1e] 相关 bit 并返回 1."),
    ("FUN_08106b94", "init_card_list_scroll_entry",
        "由 FUN_080ff4f0 (scene_card_list 场景重置协调器) 在 reset_card_list_scroll_state 之后唯一调用, "
        "传入从 card_list 指针表读取的 card_id (20-bit 提取后的低 20 位). "
        "函数向 scene_card_list 结构写入目标 card_id 的滚动入口参数: "
        "对 [0x0202f3c0+0x64] 写入 r0 (card_id); 对 [0x0202f3c0+0x66]/[+0x68] 写入 0 (滚动偏移清零); "
        "随后在 [0x0202f3c0+0x70..0x74] 区域 OR 写入 DAT_08106bf8 (0x0000ffff) 位掩码 (3 次循环, stride=2); "
        "对 [0x0202f3c0+0x34] 写入 0x38 (初始 x 坐标); "
        "根据 [0x0202f3c0+0x1e] bit2 选择 [+0x36] := 0x18 或 0x20 (y 坐标); "
        "最后对 [+0x1e] OR 0x2 (bit1), AND ~0x11 (清除 bit0+bit4), 标记入口就绪并清除旧状态位. 返回 1."),
    ("FUN_080ff4f0", "reinit_card_list_scroll_view",
        "由 FUN_080fe308 (卡牌列表场景大型主循环) 唯一调用, "
        "重新初始化滚动视图状态 (重新定位滚动位置 + 清除渲染脏标志 + 重置并初始化滚动条目). "
        "函数首先调用 compute_card_list_scroll_position 计算滚动位置; "
        "若返回值 <0 (无有效卡片) 则跳过后续操作返回 0. "
        "位置有效时依次调用: clear_card_stats_render_flags (清除卡片统计渲染脏标志), "
        "reset_card_list_scroll_state (重置滚动状态), "
        "然后从 [0x0202f3c0+0x74] 指针表读取 scroll_pos 对应的 card_id (lsls/lsrs 提取低 20 位), "
        "最后调用 init_card_list_scroll_entry (08106b94) 写入目标 card_id 的显示坐标和滚动入口参数. "
        "返回 1 表示重置完成."),
    ("FUN_08103b3c", "collect_valid_card_pairs_to_buf",
        "由 FUN_081026f4 (card_ids+card_stats+fs 联合场景) 唯一调用, "
        "负责从 deck slot 的三个卡片分区 (main/extra/side) 中收集满足配对条件的卡片 ID 到输出缓冲区. "
        "函数从 r0=deck_slot 指针 (r5), r1=partner_card_type, r10=output_buf (非 APCS, prologue mov r7,r10) 获取参数. "
        "三重循环分别遍历 [r5+0x18] 个 main 卡 (偏移 0x1C), [r5+0x19] 个 extra 卡 (偏移 0xBC), "
        "[r5+0x1A] 个 side 卡 (偏移 0xDA); "
        "每次对当前 card_id * 0x16 定位 card_stats_table entry 后调用 check_card_pair_allowed(card_entry, partner_card_type); "
        "若允许则将 card_id 写入 output_buf (str r4,[r7]) 并推进 r7; 同时计数 r2. "
        "返回 r0 = 收集到的有效配对卡数量."),

    # 2026-05-05: BATCH-12 落地 (topo=244/245/246/247/248/249/250/251/252/253/254/255/256/257/258)
    ("FUN_08103524", "load_card_name_from_fs_by_index",
        "以卡牌索引号 r1 查找 FS 条目 (lookup_card_entry_by_index), 再通过 load_card_fs_entry_to_struct "
        "将文件系统字符串加载到结构体; 随后对 r0 指向的目标缓冲区调用 zero_fill_by_halfword 清零 "
        "(大小 0x8c*2=0x118 字节), 然后 strncpy 复制卡名字符串并写入终止符. "
        "最后从 IWRAM [0x02000000+0x6c2c] 读取语言 bit[2:0] 并写入 [r7+0x17]. "
        "由三个 card_ids/card_stats/fs 上下文调用方 (FUN_081021dc, FUN_081026f4, FUN_08103020) 调用, "
        "用于将单张卡的卡名字符串填入卡片信息结构体指定字段."),
    ("FUN_081026f4", "check_card_entry_by_mode",
        "由场景主循环 (FUN_080fe308) 和 FUN_08105964 调用, 根据模式参数 r0 "
        "(0=新卡/无状态, 1=已有索引) 以及索引参数 r1 对卡片条目执行有效性检查并选择加载路径. "
        "r0=0 时检查 IWRAM banlist 位图 (0x0202a4d0+0xc2*2) 中对应位是否为零; "
        "r0=1 时调用 get_card_data_format_id 并比较范围. 检查失败返回 r0=-1; "
        "通过后根据模式分发到 copy_bytes_by_halfword (模式0) / load_card_name_from_fs_by_index (模式1) / "
        "copy_bytes_by_halfword (模式2+). 函数完成后将结果写回 IWRAM 并通过多段 "
        "bl insert_card_into_deck_slot 按 deck_type 更新 deck slot 状态."),
    ("FUN_08102828", "find_card_slot_by_id_and_mode",
        "被 update_card_list_scroll_page_state (scene_card_list) 调用, "
        "以卡牌 ID (r1 经 0x0fff 掩码处理后的值) 在 IWRAM [0x0202a4d0] 的 deck slot 数组中 "
        "按模式 r3 (0-3) 查找匹配条目. 模式 0/1/2/3 各对应不同的 slot 起始偏移 "
        "(0x2b9c/0x3ecc/0x40cc/0x3ccc 等), 使用 bsearch_index_by_callback 进行二分查找; "
        "找到则返回在 slot 中的下标, 否则返回 0. r0 经初始化后清零其指向的 halfword ([r0]=0); "
        "r2 为输出指针, 写入掩码后 card ID (strh). 配合 update_card_list_scroll_page_state 的滚动/分页逻辑使用."),
    ("FUN_080ffaf8", "update_card_list_scroll_page_state",
        "由场景主循环 tick_card_list_scene_frame (FUN_080fe308) 调用, "
        "负责更新卡片列表的滚动/翻页状态. 检查 [r4+0x78] (scroll pending flag) 是否为零: "
        "若为零则切换 [r6+0x16] bit0 (奇偶翻页标记), 并将 strh 0 写入 [r6+0xc/0xe/0x10] 三个状态字段; "
        "若非零则调用 compute_card_list_scroll_position 计算滚动位置, "
        "再调用 find_card_slot_by_id_and_mode 找到对应 slot 下标, "
        "之后通过 __modsi3 / __divsi3 计算行内列偏移和行号, 分别 strh 到 [r6+0xc] (列) 和 [r6+0xe] (行). "
        "最后调用 reset_card_list_scroll_state 并返回 1."),
    ("FUN_080fe308", "tick_card_list_scene_frame",
        "card_list 场景每帧主 tick 函数, 由四个高层场景管理函数 "
        "(FUN_08108788/08108cdc/08108fd8/0810af00) 调用. "
        "从 IWRAM gPrng 区域读取状态标记: [gPrng+0xa4*2] (r1) 和 [gPrng+0xa7*2] (r0), "
        "计算 r5 = r1 & ~r0 (活跃 tick 掩码); 检查 [r7+0x1e] bit0, 若为零则直接跳过; "
        "若非零则调用 dispatch_card_info_list_tick_by_state 执行状态机 tick. "
        "若 dispatch 返回 0 则再调用 return_zero_epilogue_stub. "
        "dispatch 返回非零时清除 [r7+0x1e] bit1 并再次调用 return_zero_epilogue_stub."),
    ("FUN_080ff430", "return_one_scene_card_list",
        "scene_card_list 场景的固定返回值存根, 函数体仅 movs r0,#0x1 + bx lr 两条指令. "
        "由四个高层场景容器 (FUN_08108788/08108cdc/08108fd8/0810af00) 调用, "
        "语义为'当前帧无需进一步处理, 返回已完成状态 1'. "
        "根据 release-noop-stub 指纹 (2字节体 + indeg>=4), 属于类型 B 零参数场景处理器占位."),
    ("FUN_08102924", "insert_card_into_deck_slot",
        "由 populate_deck_slots_from_card_list (card_stats) 和 reset_all_deck_slots (card_stats) "
        "以 deck_type=0/1/2/3 批量调用, 将一张卡插入指定 deck slot 数组中的有序位置. "
        "r0=IWRAM 基址 (->r8), r1=deck_slot_mode (->r4) 决定目标 slot 偏移 "
        "(0->0xb7*4, 1->0x140c, 2->0x160c, 3->0x180c), r2=card_id (->r7, & 0x0fff), "
        "r3=insert_mode (->stack). 使用 bsearch_index_by_callback 在已排序数组中定位插入点; "
        "若找到则更新现有条目的 type nibble; 若未找到则在末尾追加并通过 strh/移位更新计数字段 "
        "[slot+0x1a0c] 和 [slot+0x1a14]. 返回 0 (插入成功) 或当前计数."),
    ("FUN_08103350", "populate_deck_slots_from_card_list",
        "由 reinit_deck_slots_and_data/FUN_08102124/FUN_0810230c/FUN_081021dc (均含 card_stats tag) 调用, "
        "负责将 IWRAM [0x0202a4d0+0x6c] 卡片列表中的已排序条目批量插入 deck slot. "
        "两段循环分别处理 slot 类型 1 (偏移 +0x1c, 循环上限 [base+0x18]) 和 slot 类型 2 "
        "(偏移 +0xbc, 循环上限 [base+0x19]): 每次从对应 halfword 读取 card_id, "
        "以 deck_type=1/2, r1=0, r3=1 调用 insert_card_into_deck_slot 逐条插入. 返回 r0=1."),
    ("FUN_08103820", "zero_deck_slot_range_by_type",
        "由 reset_all_deck_slots (批量 type 0..3 调用) 和 FUN_0810236c (card_stats) 调用, "
        "根据 deck_type (r0, [0..3]) 和 flag (r1, 0=主/1=副) 选择目标 slot 的 IWRAM 偏移, "
        "调用 zero_fill_by_halfword 将对应区域清零. "
        "四种 deck_type 分别对应偏移 0x3ecc/0x3ccc/0x140c/0x160c (flag=0) "
        "或 0x40cc/0x3ecc/0x3ccc/0x42cc (flag=1); "
        "大小固定为 0x200 halfword (0x400 字节) 或 0x1130 halfword. 返回 r0=1."),
    ("FUN_0810329c", "reset_all_deck_slots",
        "被五个 card_stats 调用方调用 (FUN_08102124/081021dc/0810230c/081030c4/081030e0), "
        "是 deck slot 重置的核心入口. 循环 type=0..3 调用 zero_deck_slot_range_by_type(type, 0) "
        "将全部四种 deck slot 区域清零; 随后以 banlist 位图 (IWRAM 0x02000006) 为外层循环, "
        "对每个设置了对应 bit 的索引, 读取标记 byte (0xb7*4 偏移), 提取 type nibble, "
        "并调用 write_card_list_field_by_row_col 写入对应 row/col. "
        "最后将计数 r5/r6 分别 strh 到 [r8+0x1a0c] 和 [r8+0x1a14]. 返回 r0=1."),
    ("FUN_081030e0", "reinit_deck_slots_and_data",
        "由 init_card_stats_display_fields (card_stats) 和 FUN_08103020 (card_ids/card_stats/fs) 调用, "
        "是 deck slot 完整初始化序列的组合函数. 依次调用: "
        "(1) reset_all_deck_slots() 清零全部 slot 状态; "
        "(2) populate_deck_slots_from_card_list() 将卡片列表重新填入 slot; "
        "(3) 循环 slot_idx=0..3 调用 init_deck_slot_data(slot_idx) 初始化每个 slot 的详细数据. "
        "返回 r0=1."),
    ("FUN_0810322c", "write_card_list_field_by_index",
        "被 FUN_08102034/08102124/081021dc/0810236c (均含 card_stats) 调用, "
        "是卡片列表字段写入的最小工具函数. 以 r0 为字段下标 (halfword 步长 *2), "
        "在 IWRAM 0x0202a4d0+0xa7*4=0x29c 偏移处写入 halfword r1. "
        "函数体 7 条指令, 返回 r0=1. "
        "与已命名的 write_card_list_field_by_row_col 语义相似但参数不同 "
        "(本函数用线性下标, 彼函数用 row/col 二维坐标)."),
    ("FUN_08102034", "init_card_stats_display_fields",
        "由高层场景容器 FUN_08108b38 (含 banlist/card_frame/card_list/card_stats/deck/font_jp/settings) 调用, "
        "是卡片统计显示字段的初始化入口. 函数先 copy_bytes_by_halfword 将 0x0201138 的 0x118 字节 "
        "复制到 IWRAM 0x0202a4d0+0x6c; 随后调用 write_card_list_field_by_index 依次写入4个字段: "
        "(index=0, value=0), (index=1, value=1), (index=2, value=1), (index=3, value=1); "
        "之后对每个 slot (r5=0..3) 读取 [r6+slot] 的原始值, 经 clamp [1..5] 后调用 "
        "write_card_list_field_by_row_col 写入7列显示字段; "
        "最后调用 reinit_deck_slots_and_data() 重建 deck slot. 返回 r0=1."),
    ("FUN_081033c4", "build_card_list_slot_display_entries",
        "由 refresh_card_list_slot_display/FUN_081021ac/FUN_081021dc/FUN_08102fc4 "
        "(均含 scene_card_list tag) 调用, 负责将 IWRAM deck slot 数据构建为卡片列表槽位的显示条目 "
        "(halfword 数组). 函数使用 r9 (implicit 参数, IWRAM 基址相关) 作为基址: "
        "先 zero_fill_by_halfword 清零目标区域 (r9+0xc2*2 偏移, 大小 0x118 字节), "
        "再 copy_bytes_by_halfword 从 r9+0x6c 复制 0x17 halfword 的头部数据; "
        "读取 [r9+0x83] 写入 [dest+0x17] (类型标记). 随后以 r12 (implicit) 为循环上限, "
        "遍历三组 slot 数组 (偏移 0x1a0c/0x1a34/0x1a3c/0x180c), "
        "将每个 slot entry 的低 20-bit 提取后 strh 写入输出缓冲区, "
        "并累加 r6 计数 (写入 [dest+0x18] 和 [dest+0x19]). 返回 r0=1."),
    ("FUN_081020e0", "refresh_card_list_slot_display",
        "由 FUN_08108c4c (scene_duel_puzzle/card_list) 调用, 是 card_list 槽位显示的刷新入口. "
        "函数对 slot_idx=0..3 循环: (1) read_card_list_field_by_row_col(slot_idx, 0) 读取当前槽位字段值, "
        "strb 写入 [0x02006c34+slot_idx] (IWRAM 槽位状态字节); "
        "(2) 调用 build_card_list_slot_display_entries 构建显示条目; "
        "(3) 最后 copy_bytes_by_halfword 将 0x0202a4d0+0x6c 的 0x118 字节复制到 0x02001138. "
        "返回 r0=1."),

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
