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
